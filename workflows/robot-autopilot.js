export const meta = {
  name: 'robot-autopilot',
  description: 'Diagnose and fix a robot problem end to end without further prompting: triage, investigate, blind verification, test-first patches in git worktrees reviewed by a critic (3 rounds at most), and a report whose pending approvals are exact commands the team never runs',
  phases: [
    { title: 'Triage', detail: 'robot-triage-router classifies the request and picks the specialists' },
    { title: 'Investigate', detail: 'the chosen specialists, in parallel or in sequence' },
    { title: 'Verify', detail: 'one blind skeptic per high or medium finding' },
    { title: 'Fix', detail: 'builder in a worktree, then critic, at most 3 rounds per finding' },
    { title: 'Report', detail: 'assembled in code' },
  ],
}

// args: { request: "<symptom or goal>", root: "<repo path>", records?: ["<decision record files>"], scope?: ["<files>"],
//         maxFix?: n, maxVerify?: n, maxRounds?: n, agentPrefix?: "robotics-skills:" }   (a JSON string is accepted too; caller limits can lower the caps, never raise them)
// agentPrefix is put in front of each agent name. The default fits a plugin install; pass "" when the agents are
// installed bare (symlinks into ~/.claude/agents, or --plugin-dir).
// Launch it from inside the project repository: the builder's worktree is cut from the session's working directory.
// The runtime has no clock, so the wall-clock limit belongs to the caller, for example `timeout 3600 claude -p ...`.

let input = args
if (typeof input === 'string') {
  try { input = JSON.parse(input) } catch (e) {
    return { error: 'args is a string that is not valid JSON (' + e.message + '); nothing ran' }
  }
}
if (!input || typeof input !== 'object' || typeof input.request !== 'string' || !input.request.trim() ||
    typeof input.root !== 'string' || !input.root.trim()) {
  return { error: 'robot-autopilot needs args {request, root, records?, scope?, maxFix?, maxVerify?, maxRounds?, agentPrefix?}; nothing ran' }
}

const request = input.request.trim()
const root = input.root.replace(/\/+$/, '')
const asList = v => (Array.isArray(v) ? v.filter(x => typeof x === 'string' && x) : [])
const records = asList(input.records)
const scope = asList(input.scope)

// Hard ceilings live here, in code. Caller values can only lower them.
const HARD = { fix: 5, verify: 12, rounds: 3, steps: 6, agents: 60 }
const cap = (v, hard, min) => (Number.isInteger(v) && v >= min ? Math.min(v, hard) : hard)
const MAX_FIX = cap(input.maxFix, HARD.fix, 0)
const MAX_VERIFY = cap(input.maxVerify, HARD.verify, 1)
const MAX_ROUNDS = cap(input.maxRounds, HARD.rounds, 1)
log(`caps: fix ${MAX_FIX}, verify ${MAX_VERIFY}, critic rounds ${MAX_ROUNDS}, steps ${HARD.steps}, agents ${HARD.agents}`)

const PREFIX = input.agentPrefix !== undefined ? input.agentPrefix : 'robotics-skills:'
if (typeof PREFIX !== 'string') return { error: 'agentPrefix must be a string ("" for bare agent names); nothing ran' }
const AGENT = name => PREFIX + name
let spawned = 0
const failed_stages = []
const dropped = []
const drop = (what, why) => { dropped.push({ what, why }); log(`dropped: ${what} (${why})`) }

async function spawn(prompt, opts) {
  if (spawned >= HARD.agents) {
    failed_stages.push({ stage: opts.phase, id: opts.label, why: `agent cap ${HARD.agents} reached` })
    log(`agent cap ${HARD.agents} reached; skipped ${opts.label}`)
    return null
  }
  spawned++
  const out = await agent(prompt, opts)
  if (!out) failed_stages.push({ stage: opts.phase, id: opts.label, why: 'agent returned null (failed or skipped)' })
  return out
}

function clip(text, n, label) {
  const s = typeof text === 'string' ? text : JSON.stringify(text || '')
  if (s.length <= n) return s
  log(`clipped ${label} from ${s.length} to ${n} chars`)
  return s.slice(0, n) + ' ...[clipped]'
}

const MACHINE_CMD = { type: 'object', properties: { machine: { type: 'string' }, command: { type: 'string' }, why: { type: 'string' } }, required: ['command', 'why'] }

const PLAN = {
  type: 'object',
  properties: {
    classification: { type: 'string', enum: ['live_fault', 'intermittent_fault', 'recorded_data', 'video_relay', 'policy_deployment', 'code_path_audit', 'design_question'] },
    confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
    reasoning: { type: 'string' },
    shape: { type: 'string', enum: ['parallel', 'sequence'] },
    steps: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          specialist: { type: 'string', enum: ['robot-fault-hunter', 'harness-axis-auditor', 'general-reader'] },
          axis: { type: 'string' },
          skills: { type: 'array', items: { type: 'string' } },
          brief: { type: 'string' },
          files: { type: 'array', items: { type: 'string' } },
        },
        required: ['id', 'specialist', 'brief'],
      },
    },
    records: { type: 'array', items: { type: 'string' } },
    fixable: { type: 'boolean' },
    hardware_checks: { type: 'array', items: MACHINE_CMD },
    open_questions: { type: 'array', items: { type: 'string' } },
  },
  required: ['classification', 'confidence', 'reasoning', 'shape', 'steps', 'fixable'],
}

const INVESTIGATION = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          axis: { type: 'string' },
          title: { type: 'string' },
          file: { type: 'string' },
          line: { type: 'integer' },
          status: { type: 'string', enum: ['missing', 'partial'] },
          severity: { type: 'string', enum: ['high', 'medium', 'low'] },
          evidence: { type: 'string' },
          already_recorded: { type: 'boolean' },
          record_ref: { type: 'string' },
        },
        required: ['axis', 'title', 'file', 'line', 'status', 'severity', 'evidence', 'already_recorded'],
      },
    },
    hardware_commands: { type: 'array', items: MACHINE_CMD },
    notes: { type: 'string' },
  },
  required: ['findings'],
}

const HUNT = {
  type: 'object',
  properties: {
    evidence_summary: { type: 'string' },
    hypotheses: {
      type: 'array',
      items: {
        type: 'object',
        properties: { layer: { type: 'string' }, hypothesis: { type: 'string' }, falsifying_check: { type: 'string' }, likelihood: { type: 'string' } },
        required: ['layer', 'hypothesis', 'falsifying_check', 'likelihood'],
      },
    },
    capture_plan: {
      type: 'array',
      items: {
        type: 'object',
        properties: { step: { type: 'string' }, machine: { type: 'string' }, command: { type: 'string' }, duration: { type: 'string' }, separates: { type: 'string' } },
        required: ['step', 'command'],
      },
    },
    would_change_ranking: { type: 'string' },
    not_checked: { type: 'string' },
  },
  required: ['evidence_summary', 'hypotheses', 'capture_plan'],
}

const VERDICT = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    real: { type: 'boolean' },
    severity_ok: { type: 'boolean' },
    closed_by_record: { type: 'boolean' },
    reason: { type: 'string' },
  },
  required: ['id', 'real', 'severity_ok', 'closed_by_record', 'reason'],
}

const BUILD = {
  type: 'object',
  properties: {
    status: { type: 'string', enum: ['patched', 'declined'] },
    worktree_path: { type: 'string' },
    branch: { type: 'string' },
    files_changed: { type: 'array', items: { type: 'string' } },
    test_command: { type: 'string' },
    red_output: { type: 'string' },
    green_output: { type: 'string' },
    tests_pass: { type: 'boolean' },
    diff: { type: 'string' },
    notes: { type: 'string' },
    objection_replies: { type: 'array', items: { type: 'string' } },
    hardware_commands: { type: 'array', items: MACHINE_CMD },
  },
  required: ['status', 'files_changed', 'test_command', 'red_output', 'green_output', 'tests_pass', 'diff'],
}

const CRITIC = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['PASS', 'FAIL'] },
    failures: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          check: { type: 'integer' },
          severity: { type: 'string', enum: ['blocker', 'minor'] },
          file: { type: 'string' },
          line: { type: 'integer' },
          problem: { type: 'string' },
          needs: { type: 'string' },
        },
        required: ['severity', 'problem'],
      },
    },
    notes: { type: 'string' },
  },
  required: ['verdict', 'failures'],
}

const pending = []
const addPending = (source, c) => {
  if (!c || !c.command || pending.some(p => p.command === c.command)) return
  pending.push({ source, machine: c.machine || '', command: c.command, why: c.why || '' })
}

// ---------------------------------------------------------------- Triage
phase('Triage')
const plan = await spawn(
  `Plan an autonomous diagnosis. The request, stated once by the user:\n${request}\n\n` +
  `Repository root: ${root}\nFiles the user pointed at: ${scope.length ? scope.join(', ') : '(none; find them)'}\n` +
  `Decision records the user listed: ${records.length ? records.join(', ') : '(none; search the repository for intent, ADR, troubleshooting and handoff files)'}`,
  { agentType: AGENT('robot-triage-router'), label: 'triage', phase: 'Triage', schema: PLAN })
if (!plan) return { error: 'triage failed; nothing else ran', failed_stages, dropped }
log(`triage: ${plan.classification} (${plan.confidence}), shape ${plan.shape}, fixable ${plan.fixable}`)
for (const c of plan.hardware_checks || []) addPending('triage', c)

const AXES = ['projection', 'isolation', 'input_staleness', 'transfer']
const steps = []
const usedAxes = new Set()
for (const s of plan.steps) {
  if (steps.length >= HARD.steps) { drop(`step ${s.id}`, `step cap ${HARD.steps}`); continue }
  if (s.specialist === 'harness-axis-auditor') {
    if (!AXES.includes(s.axis)) { drop(`step ${s.id}`, `auditor needs one of ${AXES.join(', ')}, got "${s.axis}"`); continue }
    if (usedAxes.has(s.axis)) { drop(`step ${s.id}`, `axis ${s.axis} already assigned`); continue }
    usedAxes.add(s.axis)
  }
  steps.push(s)
}
if (!steps.length) return { error: 'triage returned no usable step; nothing else ran', plan, failed_stages, dropped }

const allRecords = [...new Set([...records, ...(plan.records || [])])]

// ---------------------------------------------------------------- Investigate
const HARD_LIMITS = `HARD LIMITS. This is a read-only investigation of a possibly shared robot. You never restart, publish, call a service, set a parameter, ` +
  `switch a controller, send a bus frame, start a recording, bring anything up, ssh anywhere, or edit any file. If a measurement on the live system would help, ` +
  `put the exact command in hardware_commands (with the machine it runs on) for a human to run later; nobody on this team will run it.`

const READER_RULES = `You are a general reader. Read code, configuration, logs and recorded data files you were pointed at. ` +
  `If a listed skill applies, invoke it first and follow it; its bundled scripts may run only against recorded files, never against a live robot. ` +
  `Every finding needs a file and line you opened. Report gaps and defects only (status missing or partial) with severity by consequence on the robot. ` +
  `Read the decision records before reporting; mark already_recorded with the record line when a record covers it. An open question is not a closing record.`

function stepPrompt(s, prior) {
  const head = `Request: ${request}\nRepository root: ${root}\nClassified as ${plan.classification}.\n` +
    `Decision records you MUST read before reporting: ${allRecords.length ? allRecords.join(', ') : '(none listed; search the repository and say what you found)'}.\n${HARD_LIMITS}\n`
  const task = `Task ${s.id}: ${s.brief}\nFiles in scope: ${(s.files && s.files.length ? s.files : scope).join(', ') || '(find them)'}.\n` +
    (s.skills && s.skills.length ? `Skills to invoke first: ${s.skills.join(', ')}.\n` : '')
  const axis = s.specialist === 'harness-axis-auditor' ? `Your axis: ${s.axis}. Stay on it; other auditors cover the others.\n` : ''
  const rules = s.specialist === 'general-reader' ? READER_RULES + '\n' : ''
  return head + task + axis + rules + (prior ? `\nEarlier steps found:\n${prior}\n` : '')
}

async function runStep(s, prior) {
  const hunter = s.specialist === 'robot-fault-hunter'
  const opts = { label: `investigate:${s.id}`, phase: 'Investigate', schema: hunter ? HUNT : INVESTIGATION }
  if (s.specialist !== 'general-reader') opts.agentType = AGENT(s.specialist)
  return spawn(stepPrompt(s, prior), opts)
}

phase('Investigate')
let outs
if (plan.shape === 'sequence') {
  // A later step reads the earlier steps' findings, so these are real edges and run in order.
  outs = []
  let prior = ''
  for (const s of steps) {
    const out = await runStep(s, prior)
    outs.push(out)
    if (out && out.findings) prior += `${s.id}: ${clip(out.findings.map(f => `${f.title} (${f.file}:${f.line})`).join('; '), 3000, `prior ${s.id}`)}\n`
  }
} else {
  outs = await parallel(steps.map(s => () => runStep(s, '')))
}

const raw = []
const hunts = []
steps.forEach((s, i) => {
  const out = outs[i]
  if (!out) return
  if (s.specialist === 'robot-fault-hunter') {
    hunts.push({ step: s.id, ...out })
    for (const c of out.capture_plan || []) addPending(`${s.id} capture plan`, { machine: c.machine, command: c.command, why: c.separates || c.step })
    return
  }
  for (const c of out.hardware_commands || []) addPending(s.id, c)
  for (const f of out.findings || []) raw.push({ ...f, from: s.id })
})

// Dedupe in code across ALL investigators before verification: this barrier is justified because the same line is often
// reported by two axes, and one defect should cost one skeptic.
const RANK = { high: 0, medium: 1, low: 2 }
raw.sort((x, y) => RANK[x.severity] - RANK[y.severity])
const seen = new Set()
const merged = []
const recorded = []
for (const f of raw) {
  const k = `${f.file.split('/').pop()}:${Math.round(f.line / 5)}`
  if (seen.has(k)) { drop(`finding "${f.title}"`, `duplicate of an earlier finding at ${k}`); continue }
  seen.add(k)
  const item = { ...f, id: `F${merged.length + recorded.length + 1}` }
  if (f.already_recorded) { recorded.push(item); continue }
  merged.push(item)
}
log(`investigated ${steps.length} step(s): ${raw.length} findings, ${merged.length} distinct open, ${recorded.length} already recorded, ${hunts.length} hunter plan(s)`)

// ---------------------------------------------------------------- Verify
phase('Verify')
const urgent = merged.filter(f => f.severity !== 'low')
const toVerify = urgent.slice(0, MAX_VERIFY)
const unverified = merged.filter(f => f.severity === 'low').map(f => ({ ...f, why: 'low severity, not verified by design' }))
for (const f of urgent.slice(MAX_VERIFY)) {
  unverified.push({ ...f, why: `verification cap ${MAX_VERIFY}` })
  drop(`verification of ${f.id} "${f.title}"`, `verification cap ${MAX_VERIFY}`)
}

const verdicts = await pipeline(toVerify, f => spawn(
  `Verify finding ${f.id}. Claimed defect at ${root}:\n` +
  `title: ${f.title}\nfile: ${f.file}\nline: ${f.line}\nseverity: ${f.severity}\nevidence: ${f.evidence}\n\n` +
  `Try to REFUTE it. Open the cited file and line and the code it depends on, and check these decision records for an entry that fixes, rejects or deliberately scopes it out: ` +
  `${allRecords.length ? allRecords.join(', ') : '(none listed; search the repository for intent, ADR, troubleshooting and handoff files)'}. Return id "${f.id}".`,
  { agentType: AGENT('finding-skeptic'), label: `verify:${f.id}`, phase: 'Verify', schema: VERDICT }))

const confirmed = []
const refuted = []
const closed = []
toVerify.forEach((f, i) => {
  const v = verdicts[i]
  if (!v) { unverified.push({ ...f, why: 'skeptic failed or was skipped' }); return }
  const item = { ...f, verdict: v }
  if (!v.real) refuted.push(item)
  else if (v.closed_by_record) closed.push(item)
  else confirmed.push(item)
})
log(`verified ${toVerify.length - unverified.filter(u => u.why.startsWith('skeptic')).length}/${toVerify.length}: confirmed ${confirmed.length}, refuted ${refuted.length}, closed by record ${closed.length}`)

// ---------------------------------------------------------------- Fix
phase('Fix')
const relPath = file => (file.startsWith(root + '/') ? file.slice(root.length + 1) : file)
const inRoot = file => file.startsWith(root + '/') || !file.startsWith('/')
const MOVES_ROBOT = /\bros2\s+(launch|run|topic\s+pub|service\s+call|param\s+set|control)\b|\b(cansend|candump|ssh|scp)\b/

// Disputed severity sorts after agreed severity within the same label; the cap then keeps the strongest.
confirmed.sort((a, b) => RANK[a.severity] - RANK[b.severity] || Number(!a.verdict.severity_ok) - Number(!b.verdict.severity_ok))
const fixable = plan.fixable ? confirmed.filter(f => inRoot(f.file)) : []
const notPatched = []
if (!plan.fixable) log('triage marked this request not fixable in code: no patches attempted')
for (const f of confirmed) {
  if (!plan.fixable) notPatched.push({ ...f, why: 'triage: not fixable in code or config without hardware' })
  else if (!inRoot(f.file)) notPatched.push({ ...f, why: 'file is outside the repository root' })
}
const selected = fixable.slice(0, MAX_FIX)
for (const f of fixable.slice(MAX_FIX)) {
  notPatched.push({ ...f, why: `fix cap ${MAX_FIX}` })
  drop(`patch for ${f.id} "${f.title}"`, `fix cap ${MAX_FIX}`)
}

function gateError(b) {
  if (b.status !== 'patched') return 'builder did not report a patch'
  if (!b.tests_pass) return 'builder did not observe the tests passing'
  if (!b.red_output || !b.red_output.trim()) return 'no failing-before output: a fix without a failing-first test is not verified'
  if (!b.green_output || !b.green_output.trim()) return 'no passing-after output'
  if (!b.diff || !b.diff.trim()) return 'empty diff'
  if (!b.files_changed.some(p => /test/i.test(p))) return 'no test file in the change'
  if (b.worktree_path && b.files_changed.some(p => p.startsWith('/') && !p.startsWith(b.worktree_path + '/'))) return 'edit outside the worktree'
  if (MOVES_ROBOT.test(b.test_command)) return 'test command looks like it could touch a robot or a remote machine'
  return ''
}

const joinFailures = fs => fs.map(x => `- [${x.severity}]${x.file ? ` ${x.file}${x.line ? ':' + x.line : ''}` : ''} ${x.problem}${x.needs ? ` Needs: ${x.needs}` : ''}`).join('\n')

async function fixLoop(f) {
  let prevDiff = ''
  let objections = []
  let best = null
  let outcome = 'no_valid_draft'
  const history = []
  for (let round = 1; round <= MAX_ROUNDS; round++) {
    const label = `${f.id}:r${round}`
    const b = await spawn(
      `Fix finding ${f.id} with a failing-first test, in your own worktree.\n` +
      `title: ${f.title}\nfile: ${relPath(f.file)}\nline: ${f.line}\nseverity: ${f.severity}\nevidence: ${f.evidence}\n` +
      `skeptic's reading: ${f.verdict.reason}\n` +
      `Decision records to read first: ${allRecords.length ? allRecords.join(', ') : '(none listed; search the repository)'}.\n` +
      `Round ${round} of ${MAX_ROUNDS}.` +
      (prevDiff ? `\n\nPrevious draft (reapply it in your fresh worktree, then address the objections):\n${prevDiff}\n\nCritic objections:\n${joinFailures(objections)}` : ''),
      { agentType: AGENT('robot-fix-builder'), isolation: 'worktree', label: `build:${label}`, phase: 'Fix', schema: BUILD })
    if (!b) { history.push({ round, result: 'builder failed' }); outcome = best ? 'open_objections' : 'no_valid_draft'; break }
    for (const c of b.hardware_commands || []) addPending(`${f.id} fix verification`, c)
    if (b.status === 'declined') {
      history.push({ round, result: 'declined: ' + (b.notes || '') })
      outcome = 'declined'
      break
    }
    if (b.diff) prevDiff = b.diff
    const gate = gateError(b)
    if (gate) {
      history.push({ round, result: 'gate: ' + gate })
      objections = [{ severity: 'blocker', problem: gate }]
      continue
    }
    const c = await spawn(
      `Review the patch for finding ${f.id}. Round ${round} of ${MAX_ROUNDS}.\n` +
      `Finding: ${f.title} at ${relPath(f.file)}:${f.line}. Evidence: ${f.evidence}\n` +
      `Worktree (read files here): ${b.worktree_path || '(unknown)'}\nTest command: ${b.test_command}\n\nFailing output before the patch:\n${clip(b.red_output, 3000, 'red ' + label)}\n\n` +
      `Passing output after the patch:\n${clip(b.green_output, 3000, 'green ' + label)}\n\nDiff:\n${b.diff}\n\n` +
      `Builder notes: ${b.notes || '(none)'}\nBuilder replies to earlier objections: ${(b.objection_replies || []).join(' | ') || '(none)'}\n` +
      `Decision records: ${allRecords.length ? allRecords.join(', ') : '(none listed; search the repository)'}.`,
      { agentType: AGENT('robot-change-critic'), label: `critic:${label}`, phase: 'Fix', schema: CRITIC })
    if (!c) { best = { draft: b, blockers: 99, failures: [] }; outcome = 'unreviewed'; history.push({ round, result: 'critic failed; patch is unreviewed' }); break }
    const blockers = c.failures.filter(x => x.severity === 'blocker').length
    history.push({ round, result: c.verdict, blockers })
    if (!best || blockers <= best.blockers) best = { draft: b, blockers, failures: c.failures }
    if (c.verdict === 'PASS') { outcome = 'pass'; best = { draft: b, blockers: 0, failures: c.failures }; break }
    objections = c.failures
    outcome = 'open_objections'
  }
  if (outcome === 'open_objections' && history.length >= MAX_ROUNDS) log(`${f.id}: critic did not pass in ${MAX_ROUNDS} rounds; returning the best draft with open objections`)
  return { finding: f, outcome, rounds: history.length, history, best }
}

const patchResults = selected.length ? await pipeline(selected, fixLoop) : []
const patches = []
selected.forEach((f, i) => {
  const r = patchResults[i]
  if (!r) { failed_stages.push({ stage: 'Fix', id: f.id, why: 'fix loop threw' }); notPatched.push({ ...f, why: 'fix loop failed' }); return }
  if (!r.best) { notPatched.push({ ...f, why: `${r.outcome}: ${r.history.map(h => h.result).join('; ')}` }); return }
  patches.push(r)
})
log(`patches: ${patches.length} with a draft, ${patches.filter(p => p.outcome === 'pass').length} passed the critic; ${notPatched.length} confirmed finding(s) without a patch`)

// ---------------------------------------------------------------- Report
phase('Report')
const fence = text => { const t = text || ''; const f = t.includes('```') ? '````' : '```'; return `${f}\n${t.trim()}\n${f}` }
const L = []
L.push('# Robot autopilot report', '')
L.push(`Request: ${request}`)
L.push(`Classified as ${plan.classification} (${plan.confidence} confidence), ${steps.length} investigation step(s), shape ${plan.shape}. ${plan.reasoning}`)
if ((plan.open_questions || []).length) L.push('', 'Open questions that could change this:', ...plan.open_questions.map(q => `- ${q}`))

L.push('', '## Verified findings', '')
const open = [...confirmed]
if (!open.length) L.push('None confirmed.')
for (const f of open) {
  L.push(`- ${f.id} [${f.severity}${f.verdict.severity_ok ? '' : ', severity disputed by the skeptic'}] ${f.title} at ${f.file}:${f.line}. ${f.evidence} Skeptic: ${f.verdict.reason}`)
}

L.push('', '## Patches', '')
if (!patches.length) L.push('No patch was produced.')
for (const p of patches) {
  const d = p.best.draft
  L.push(`### ${p.finding.id} ${p.finding.title}`, '')
  L.push(`Outcome: ${p.outcome === 'pass' ? 'critic PASS' : p.outcome === 'unreviewed' ? 'UNREVIEWED, the critic did not return' : 'critic did not pass; open objections below'} after ${p.rounds} round(s) (${p.history.map(h => h.result).join(' > ')}).`)
  L.push(`Files: ${d.files_changed.join(', ')}. Test command: \`${d.test_command}\`.`)
  L.push(`Worktree: ${d.worktree_path || 'unknown'} on branch ${d.branch || 'unknown'}. It may be removed, so the diff below is the record.`, '')
  L.push('Failing before the patch:', fence(clip(d.red_output, 2000, 'report red ' + p.finding.id)))
  L.push('Passing after the patch:', fence(clip(d.green_output, 2000, 'report green ' + p.finding.id)))
  L.push('Diff:', fence(d.diff))
  if (p.outcome !== 'pass' && p.best.failures && p.best.failures.length) L.push('Open objections:', joinFailures(p.best.failures))
  L.push('')
}

if (notPatched.length) {
  L.push('## Confirmed but not patched', '')
  for (const f of notPatched) L.push(`- ${f.id} [${f.severity}] ${f.title} at ${f.file}:${f.line}. Not patched: ${f.why}`)
}

if (refuted.length || closed.length || recorded.length) {
  L.push('', '## Refuted, already closed, or already recorded', '')
  for (const f of refuted) L.push(`- ${f.id} refuted: ${f.title}. ${f.verdict.reason}`)
  for (const f of closed) L.push(`- ${f.id} closed by a record: ${f.title}. ${f.verdict.reason}`)
  for (const f of recorded) L.push(`- ${f.id} already recorded (${f.record_ref || 'no ref'}): ${f.title}`)
}

for (const h of hunts) {
  L.push('', `## Hypotheses and capture plan (${h.step})`, '', h.evidence_summary, '')
  for (const x of h.hypotheses) L.push(`- ${x.layer}: ${x.hypothesis}. Falsified by: ${x.falsifying_check}. Likelihood: ${x.likelihood}`)
  if (h.would_change_ranking) L.push('', `What would change the ranking: ${h.would_change_ranking}`)
  if (h.not_checked) L.push('', `Not checked: ${h.not_checked}`)
}

L.push('', '## Pending approvals', '')
L.push('The team ran none of these. They touch real hardware, a shared robot, or send something off this machine. Run them yourself, in order, when you are ready.', '')
if (!pending.length) L.push('None collected.')
pending.forEach((p, i) => {
  L.push(`${i + 1}. ${p.machine ? `On ${p.machine}` : 'Where it applies'}, from ${p.source}: ${p.why}`, '', fence(p.command))
})
L.push('', 'Pushing a branch or applying a patch to a shared robot is yours to do; the team stopped before both.')

L.push('', '## What was not verified', '')
L.push('- Nothing was run against a robot. Behaviour on the real system, timing and hardware effects are unverified.')
for (const u of unverified) L.push(`- ${u.id} [${u.severity}] ${u.title} at ${u.file}:${u.line}: ${u.why}`)
for (const d of dropped) L.push(`- Dropped ${d.what}: ${d.why}`)
for (const s of failed_stages) L.push(`- Stage failed: ${s.stage} ${s.id}: ${s.why}`)

return {
  report: L.join('\n'),
  classification: plan.classification,
  confirmed: confirmed.map(f => ({ id: f.id, title: f.title, file: f.file, line: f.line, severity: f.severity })),
  patches: patches.map(p => ({ id: p.finding.id, outcome: p.outcome, rounds: p.rounds, worktree_path: p.best.draft.worktree_path, branch: p.best.draft.branch })),
  pending_approvals: pending,
  unverified,
  failed_stages,
  dropped,
  caps: { fix: MAX_FIX, verify: MAX_VERIFY, rounds: MAX_ROUNDS, agents_spawned: spawned, agents_max: HARD.agents },
}
