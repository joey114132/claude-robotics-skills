export const meta = {
  name: 'robot-preflight',
  description: 'Read-only go/no-go review before a change reaches a shared robot: a confirmed per-robot profile, then the command gate, model drift (four lenses), sync config and gain-change gate in parallel, a blind skeptic per high or medium finding, and a finish gate computed in code',
  phases: [
    { title: 'Profile', detail: 'check the confirmed per-robot profile, or draft one and stop' },
    { title: 'Check', detail: 'command gate, model drift x4 lenses, sync config, gain gate; only those that apply' },
    { title: 'Verify', detail: 'one blind skeptic per high or medium finding, capped' },
    { title: 'Sheet', detail: 'dedupe, blocker ledger, finish gate and the sheet, all in code' },
  ],
}

// args: { change: "<the change or session plan in a sentence>", root: "<repo path>", scope?: ["<files>"], records?: ["<decision records>"],
//         machines?: ["<label: absolute path>"], plannedCommands?: [{machine, command}], profile?: "<absolute path>", profileConfirmed?: true,
//         modelCopies?: [{label, path}], canonicalCopy?: "<label>", hosts?: [{label, files: ["<paths>"]}],
//         touches?: ["gains" | "limits" | "controller"], gainEvidence?: ["<diff, sim logs, criteria, rollback files>"],
//         hashesBefore?: {"<path>": "<sha256>"}, reviewedClosures?: true, maxVerify?: n, agentPrefix?: "robotics-skills:" }
// Second call, no agents: args = { recheck: { verdict, hashesBefore, hashesAfter, attempt? } } compares the hashes in code and returns the final verdict.
// agentPrefix is put in front of each agent name. The default fits a plugin install; pass "" when the agents are
// installed bare (symlinks into ~/.claude/agents, or --plugin-dir). A JSON string for args is accepted too.
//
// What this script cannot do: it has no shell, no filesystem and no clock. So it cannot hash files and cannot time itself.
// The caller takes `sha256sum` of the files before launching (hashesBefore) and of `hash_check.files_to_hash` after the run, then
// calls this script again with `recheck`; the STALE verdict and the one-rerun cap are computed there, in code. Without a
// hashesBefore baseline the verdict cannot be GO. The wall-clock limit belongs to the launcher, for example
// `timeout 1800 claude -p ...`. The caps below are on agent calls, and they live in code.

let input = args
if (typeof input === 'string') {
  try { input = JSON.parse(input) } catch (e) { return { error: 'args is a string that is not valid JSON (' + e.message + '); nothing ran' } }
}
if (input && typeof input === 'object' && input.recheck) {
  const r = input.recheck
  const before = r.hashesBefore && typeof r.hashesBefore === 'object' ? r.hashesBefore : {}
  const after = r.hashesAfter && typeof r.hashesAfter === 'object' ? r.hashesAfter : {}
  const keys = Object.keys(before)
  if (r.verdict !== 'GO' && r.verdict !== 'NO-GO') return { error: 'recheck.verdict must be the GO or NO-GO the run returned; nothing compared' }
  if (!keys.length) return { verdict: 'NO-GO', reasons: ['recheck has no hashesBefore, so a change during the run cannot be ruled out'], changed: [] }
  const changed = keys.filter(k => after[k] !== before[k]) // a path missing from hashesAfter counts as changed
  const attempt = Number.isInteger(r.attempt) && r.attempt >= 1 ? r.attempt : 1
  const stale = r.verdict === 'GO' && changed.length > 0
  return {
    verdict: stale ? 'STALE' : r.verdict, changed, attempt,
    rerun: stale && attempt < 2, // one rerun only; a second STALE is reported as STALE
    note: stale ? (attempt < 2 ? 'a file the team had read changed: rerun the whole preflight once with fresh hashes and attempt: 2' : 'second STALE: report it as STALE and stop; do not turn it into GO') : 'hashes match the baseline',
  }
}
if (!input || typeof input !== 'object' || typeof input.change !== 'string' || !input.change.trim() ||
    typeof input.root !== 'string' || !input.root.trim()) {
  return { error: 'robot-preflight needs args {change, root, scope?, records?, machines?, plannedCommands?, profile?, profileConfirmed?, modelCopies?, hosts?, touches?, gainEvidence?, hashesBefore?, reviewedClosures?, maxVerify?, agentPrefix?} or {recheck}; nothing ran' }
}

const change = input.change.trim()
const root = input.root.replace(/\/+$/, '')
const list = v => (Array.isArray(v) ? v.filter(x => x != null && x !== '') : [])
const scope = list(input.scope)
const machines = list(input.machines)
const commands = list(input.plannedCommands).filter(c => c && typeof c.command === 'string' && c.command.trim())
const copies = list(input.modelCopies).filter(c => c && c.path)
const hosts = list(input.hosts).filter(h => h && h.label)
const touches = list(input.touches).filter(t => ['gains', 'limits', 'controller'].includes(t))
const gainEvidence = list(input.gainEvidence)
const hashesBefore = input.hashesBefore && typeof input.hashesBefore === 'object' ? input.hashesBefore : null

// Hard ceilings, in code. A caller can only lower them.
const HARD = { agents: 14, verify: 12 }
const MAX_VERIFY = Number.isInteger(input.maxVerify) && input.maxVerify >= 0 ? Math.min(input.maxVerify, HARD.verify) : HARD.verify
const MIN_BUDGET_TO_VERIFY = 150000
const PREFIX = input.agentPrefix !== undefined ? input.agentPrefix : 'robotics-skills:'
if (typeof PREFIX !== 'string') return { error: 'agentPrefix must be a string ("" for bare agent names); nothing ran' }
const AGENT = name => PREFIX + name

let spawned = 0
const failed = []
async function spawn(prompt, opts) {
  if (spawned >= HARD.agents) { failed.push({ id: opts.label, why: `agent cap ${HARD.agents} reached` }); log(`agent cap ${HARD.agents} reached; skipped ${opts.label}`); return null }
  spawned++
  const out = await agent(prompt, opts)
  if (!out) failed.push({ id: opts.label, why: 'agent returned null (failed or skipped)' })
  return out
}

// ---------------------------------------------------------------- what applies
const runCmd = commands.length > 0
const runDrift = copies.length >= 2
const runSync = hosts.length >= 2
const runGain = touches.length > 0
if (!runCmd && !runDrift && !runSync && !runGain) {
  return { error: 'nothing to preflight: no planned commands, fewer than two model copies, fewer than two hosts and no gain, limit or controller change. For one command use robot-command-gate alone; nothing ran' }
}
const LENSES = ['limits', 'inertia', 'collision', 'structure']
const planned = (runCmd ? 1 : 0) + (runDrift ? LENSES.length : 0) + (runSync ? 1 : 0) + (runGain ? 1 : 0)
const SKEPTIC_SLOTS = Math.max(0, Math.min(MAX_VERIFY, HARD.agents - planned - 1)) // one slot is kept for vetting agent-proposed commands
log(`applies: command gate ${runCmd}, model drift ${runDrift}, sync config ${runSync}, gain gate ${runGain}; ${planned} check agent(s), ${SKEPTIC_SLOTS} skeptic slot(s), cap ${HARD.agents} agent calls`)

// ---------------------------------------------------------------- Profile (step 0)
phase('Profile')
const PROFILE = {
  type: 'object',
  properties: {
    bus_map: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, role: { type: 'string', enum: ['motor_command', 'status_query', 'free_test', 'unknown'] }, source: { type: 'string' } }, required: ['id', 'role', 'source'] } },
    shared_hosts: { type: 'array', items: { type: 'object', properties: { label: { type: 'string' }, who_else_uses_it: { type: 'string' }, source: { type: 'string' } }, required: ['label', 'source'] } },
    canonical_model_copy: { type: 'string' },
    speed_caps: { type: 'array', items: { type: 'object', properties: { what: { type: 'string' }, value: { type: 'string' }, source: { type: 'string' } }, required: ['what', 'value', 'source'] } },
    restart_rights: { type: 'array', items: { type: 'object', properties: { who: { type: 'string' }, what: { type: 'string' }, source: { type: 'string' } }, required: ['who', 'what', 'source'] } },
    gaps: { type: 'array', items: { type: 'string' } },
  },
  required: ['bus_map', 'shared_hosts', 'canonical_model_copy', 'speed_caps', 'restart_rights', 'gaps'],
}
const records = list(input.records)
const profilePath = typeof input.profile === 'string' && input.profile ? input.profile : ''
if (profilePath && input.profileConfirmed !== true) {
  return { error: `the profile at ${profilePath} is not marked confirmed. A human must read it and rerun with profileConfirmed: true; nothing ran`, verdict: 'NO-GO' }
}
if (!profilePath) {
  const draft = await spawn(
    `Draft a per-robot profile from the repository's records. Nobody has confirmed one yet, and a human will read your draft before anything else runs.\n` +
    `Change under review: ${change}\nRepository root: ${root}\nMachines in scope: ${machines.join('; ') || '(none listed)'}\n` +
    `Decision records: ${records.length ? records.join(', ') : '(none listed; search the repository for intent, ADR, troubleshooting, handoff and wiki files and say which you found)'}.\n` +
    `Read only. Fill: the bus map (which IDs are motor command addresses, status-query only, or free for tests), the shared hosts and who else uses them, the canonical copy of the robot model, the speed caps, and who may restart or switch what. ` +
    `Give a source file and line for every entry. Anything the records do not state goes in gaps. Never fill an entry from memory or from another robot's layout.`,
    { agentType: AGENT('robot-triage-router'), label: 'profile-draft', phase: 'Profile', schema: PROFILE })
  log('no confirmed profile: stopping after the draft')
  return {
    status: 'PROFILE_UNCONFIRMED', verdict: 'NO-GO',
    next: 'A human reads profile_draft, fixes it, saves it as a file, then reruns this workflow with profile: "<absolute path>" and profileConfirmed: true. Nothing else ran.',
    profile_draft: draft, failed,
  }
}
const allRecords = [...new Set([...records, profilePath])]
const RECORDS_LINE = `Decision records you MUST read before reporting (the last one is the human-confirmed per-robot profile, treat it as a decision record): ${allRecords.join(', ')}.`

// ---------------------------------------------------------------- Check (step 1)
const HARD_LIMITS = `HARD LIMITS. Read-only review before a change reaches a possibly shared robot. You never restart, publish, call a service, set a parameter, switch a controller, send a bus frame, ssh anywhere, write a file, or run anything. ` +
  `Anything a human must run goes in commands_for_human (or your own command list) with the machine it runs on. Another agent owns each other area; stay inside yours. List every file you opened in files_read.`
const BASE = `Change under review: ${change}\nRepository root: ${root}\nMachines in scope: ${machines.join('; ') || '(none listed)'}\nFiles in scope: ${scope.join(', ') || '(none listed)'}\n${RECORDS_LINE}\n${HARD_LIMITS}\n`

const FINDING = {
  type: 'object',
  properties: {
    title: { type: 'string' },
    file: { type: 'string', description: 'absolute path of the file you opened' },
    line: { type: 'integer' },
    severity: { type: 'string', enum: ['high', 'medium', 'low'] },
    evidence: { type: 'string', description: 'what you read; for a disagreement between copies or hosts, the value per copy or host with file:line' },
    already_recorded: { type: 'boolean' },
    record_ref: { type: 'string' },
  },
  required: ['title', 'file', 'line', 'severity', 'evidence', 'already_recorded'],
}
const HUMAN_CMD = { type: 'object', properties: { machine: { type: 'string' }, command: { type: 'string' }, why: { type: 'string' } }, required: ['machine', 'command', 'why'] }
const STRS = { type: 'array', items: { type: 'string' } }
const FINDINGS = {
  type: 'object',
  properties: { findings: { type: 'array', items: FINDING }, commands_for_human: { type: 'array', items: HUMAN_CMD }, files_read: STRS, not_checked: STRS },
  required: ['findings', 'commands_for_human', 'files_read', 'not_checked'],
}
const CMD_VERDICTS = {
  type: 'object',
  properties: {
    commands: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          command: { type: 'string' }, machine: { type: 'string' },
          verdict: { type: 'string', enum: ['READ_ONLY', 'NEEDS_APPROVAL', 'FORBIDDEN'] },
          rule: { type: 'string' }, record_cited: { type: 'string' }, why: { type: 'string' }, safer_alternative: { type: 'string' },
        },
        required: ['command', 'machine', 'verdict', 'rule', 'why', 'safer_alternative'],
      },
    },
    overall: { type: 'string', enum: ['BLOCK', 'APPROVAL_NEEDED', 'CLEAR'] },
    files_read: STRS, not_checked: STRS,
  },
  required: ['commands', 'overall', 'files_read', 'not_checked'],
}
const GAIN = {
  type: 'object',
  properties: {
    verdict: { type: 'string', enum: ['PASS', 'BLOCK'] },
    checks: { type: 'array', items: { type: 'object', properties: { check: { type: 'integer' }, status: { type: 'string', enum: ['pass', 'fail', 'not-evidenced'] }, file: { type: 'string' }, line: { type: 'integer' }, missing: { type: 'string' } }, required: ['check', 'status', 'missing'] } },
    pending_approvals: { type: 'array', items: HUMAN_CMD },
    files_read: STRS, not_checked: STRS,
  },
  required: ['verdict', 'checks', 'pending_approvals', 'files_read', 'not_checked'],
}
const VERDICT = {
  type: 'object',
  properties: { id: { type: 'string' }, real: { type: 'boolean' }, severity_ok: { type: 'boolean' }, closed_by_record: { type: 'boolean' }, reason: { type: 'string' } },
  required: ['id', 'real', 'severity_ok', 'closed_by_record', 'reason'],
}

const copyLines = copies.map(c => `${c.label || 'copy'}: ${c.path}`).join('; ')
const hostLines = hosts.map(h => `${h.label}: ${list(h.files).join(', ') || '(no files given)'}`).join('\n')
const jobs = []
if (runCmd) jobs.push({ key: 'command-gate', kind: 'cmd', agent: 'robot-command-gate', schema: CMD_VERDICTS, prompt:
  `Vet these planned commands before anyone types them. Keep each command text unchanged and in order.\n` +
  commands.map((c, i) => `${i + 1}. machine: ${c.machine || '(not stated; treat as the robot)'}\n   command: ${c.command}`).join('\n') + '\n' + BASE })
if (runDrift) for (const lens of LENSES) jobs.push({ key: `drift:${lens}`, kind: 'find', agent: 'robot-model-drift-auditor', schema: FINDINGS, prompt:
  `Your lens: ${lens}. Stay on it; three other auditors cover the other lenses.\nCopies (label: absolute path): ${copyLines}\n` +
  `Canonical copy named by the records: ${input.canonicalCopy || '(none named; report pure disagreement)'}\n` +
  `Return one finding per disagreement, with file and line of the first copy you opened in file and line, and every copy's value with its file:line in evidence. Put intended_by_record in record_ref and set already_recorded.\n` + BASE })
if (runSync) jobs.push({ key: 'sync-config', kind: 'find', agent: 'robot-sync-config-auditor', schema: FINDINGS, prompt:
  `Compare the hosts' configuration with each other and with the records.\nHosts (label: files):\n${hostLines}\n` +
  `Return one finding per mismatch or missing setting, with the file and line of the first host in file and line, and the value per host with its file:line in evidence. Put your capture list in commands_for_human.\n` + BASE })
if (runGain) jobs.push({ key: 'gain-gate', kind: 'gain', agent: 'robot-gain-change-gate', schema: GAIN, prompt:
  `The change touches: ${touches.join(', ')}. Evidence files (diff, simulation logs, criteria, rollback): ${gainEvidence.join(', ') || '(none given; report every check not-evidenced)'}\n` +
  `Return all eight checks, each with the file and line you opened. Put the rollback and the first supervised application in pending_approvals.\n` + BASE })

phase('Check')
const outs = await parallel(jobs.map(j => () => spawn(j.prompt, { agentType: AGENT(j.agent), label: j.key, phase: 'Check', schema: j.schema })))

// ---------------------------------------------------------------- collect, in code
const RANK = { high: 0, medium: 1, low: 2 }
const rel = f => (String(f).startsWith(root + '/') ? String(f).slice(root.length + 1) : String(f)).replace(/^\.\//, '')
const agentsSummary = []          // one row per agent that was planned
const raw = []                    // findings from the finding agents
const direct = []                 // blockers that need no skeptic: forbidden commands, failed gain checks
const pending = []                // commands for the human
const cmdVerdicts = []
const notChecked = []
const filesRead = new Set()
// A command is identified by where it runs and its text: the same text on the laptop and on the robot is two commands.
const normMachine = m => (/^\(not stated/.test(String(m || '')) ? '' : String(m || '').trim())
const sameCmd = (a, b) => a.command === b.command && normMachine(a.machine) === normMachine(b.machine)
const addPending = (source, c) => {
  if (!c || !c.command || pending.some(p => sameCmd(p, c))) return
  pending.push({ source, machine: c.machine || '', command: c.command, why: c.why || '' })
}
jobs.forEach((j, i) => {
  const o = outs[i]
  if (!o) { agentsSummary.push({ agent: j.key, ran: true, returned: false, passed: false, note: 'did not return' }); return }
  for (const f of o.files_read || []) filesRead.add(f)
  for (const n of o.not_checked || []) notChecked.push(`${j.key}: ${n}`)
  if (j.kind === 'cmd') {
    for (const c of o.commands) {
      cmdVerdicts.push(c)
      if (c.verdict === 'FORBIDDEN') direct.push({ owner: j.key, severity: 'high', title: `Planned command is FORBIDDEN: ${c.command} on ${c.machine || 'the robot'}`, evidence: `${c.rule}. ${c.why}${c.record_cited && c.record_cited !== 'none' ? ' Record: ' + c.record_cited : ''}`, closes: 'remove or replace the command in the plan, then rerun' })
    }
    if (o.overall === 'BLOCK' && !o.commands.some(c => c.verdict === 'FORBIDDEN')) direct.push({ owner: j.key, severity: 'high', title: 'Command gate returned BLOCK with no FORBIDDEN command listed', evidence: (o.not_checked || []).join('; ') || 'no reason given', closes: 'read the gate output, fix the plan, then rerun' })
    agentsSummary.push({ agent: j.key, ran: true, returned: true, overall: o.overall })
  } else if (j.kind === 'gain') {
    for (const c of o.checks) if (c.status !== 'pass') direct.push({ owner: j.key, severity: 'high', title: `Gain gate check ${c.check} ${c.status}`, evidence: `${c.file ? c.file + (c.line ? ':' + c.line : '') + ': ' : ''}${c.missing}`, closes: 'supply the missing evidence, then rerun' })
    if (o.verdict === 'BLOCK' && !o.checks.some(c => c.status !== 'pass')) direct.push({ owner: j.key, severity: 'high', title: 'Gain gate returned BLOCK with no failed check listed', evidence: (o.not_checked || []).join('; ') || 'no reason given', closes: 'read the gate output, supply the evidence, then rerun' })
    for (const p of o.pending_approvals) addPending(j.key, p)
    agentsSummary.push({ agent: j.key, ran: true, returned: true, overall: o.verdict })
  } else {
    for (const f of o.findings) raw.push({ ...f, owner: j.key })
    for (const p of o.commands_for_human) addPending(j.key, p)
    agentsSummary.push({ agent: j.key, ran: true, returned: true })
  }
})
const skipped = []
if (!runCmd) skipped.push('robot-command-gate: no planned commands')
if (!runDrift) skipped.push('robot-model-drift-auditor: fewer than two model copies in scope')
if (!runSync) skipped.push('robot-sync-config-auditor: fewer than two hosts in scope')
if (!runGain) skipped.push('robot-gain-change-gate: the change does not touch gains, limits or controller selection')

// Dedupe in code, inside one agent only: owner, path relative to the root and a line bucket of 8. Findings from different
// lenses or agents are never merged, because a lens can report a different defect at the same lines. The highest severity is
// kept, the dropped finding's title and evidence are appended so the skeptic sees them, and the merge counts as recorded
// only if every merged finding was.
raw.sort((x, y) => RANK[x.severity] - RANK[y.severity])
const byKey = new Map()
const merged = []
for (const f of raw) {
  const k = `${f.owner}|${rel(f.file)}:${Math.floor(f.line / 8)}`
  if (byKey.has(k)) {
    const kept = byKey.get(k)
    kept.evidence += `\nAlso reported at ${f.file}:${f.line} (${f.severity}): ${f.title}. ${f.evidence}`
    kept.already_recorded = kept.already_recorded && f.already_recorded
    log(`dedup merged "${f.title}" into "${kept.title}" (${k})`); continue
  }
  const kept = { ...f }
  byKey.set(k, kept); merged.push(kept)
}
log(`check agents returned ${raw.length} finding(s), ${merged.length} after dedupe; ${direct.length} direct blocker(s); failed: ${failed.map(f => f.id).join(', ') || 'none'}`)

// ---------------------------------------------------------------- Verify (step 2)
phase('Verify')
const needSkeptic = merged.filter(f => f.severity !== 'low' && !f.already_recorded)
let toVerify = needSkeptic.slice(0, SKEPTIC_SLOTS)
if (budget.total && budget.remaining() < MIN_BUDGET_TO_VERIFY) {
  log(`budget guard: ${Math.round(budget.remaining() / 1000)}k tokens left, below ${MIN_BUDGET_TO_VERIFY / 1000}k; verification skipped, those findings stay open`)
  toVerify = []
}
needSkeptic.forEach((f, i) => { f.id = `B${i + 1}` })
const unverified = needSkeptic.filter(f => !toVerify.includes(f))
if (unverified.length) log(`not verified, left open: ${unverified.map(f => `${f.id} ${f.title}`).join('; ')}`)
const verdicts = toVerify.length ? await pipeline(toVerify, f => spawn(
  `Verify finding ${f.id}. Claimed difference or defect, ${root}:\ntitle: ${f.title}\nfile: ${f.file}\nline: ${f.line}\nseverity: ${f.severity}\nevidence: ${f.evidence}\n\n` +
  `Try to REFUTE it. Open the cited file and line and the code it depends on, and check these decision records for an entry that fixes, rejects or deliberately scopes it out: ${allRecords.join(', ')}. Return id "${f.id}".`,
  { agentType: AGENT('finding-skeptic'), label: `verify:${f.id}`, phase: 'Verify', schema: VERDICT })) : []

// ---------------------------------------------------------------- Sheet (step 3)
phase('Sheet')
const ledger = []
let nextB = needSkeptic.length
const entry = (e) => ledger.push(e)
needSkeptic.forEach(f => {
  const i = toVerify.indexOf(f)
  const v = i >= 0 ? verdicts[i] : null
  let status = 'open'
  let note = i < 0 ? 'not verified (cap or budget); counted as open' : (!v ? 'skeptic did not return; counted as open' : v.reason)
  if (v && !v.real) status = 'refuted'
  else if (v && v.closed_by_record) status = 'closed-by-record'
  entry({ id: f.id, owner: f.owner, severity: f.severity, title: f.title, evidence: `${f.file}:${f.line}`, status, note })
})
for (const f of merged.filter(f => f.already_recorded && f.severity !== 'low')) {
  entry({ id: `B${++nextB}`, owner: f.owner, severity: f.severity, title: f.title, evidence: `${f.file}:${f.line}`, status: 'closed-by-record', note: `claimed by the agent, record ${f.record_ref || 'not cited'}; no skeptic checked it` })
}
for (const d of direct) entry({ id: `B${++nextB}`, owner: d.owner, severity: d.severity, title: d.title, evidence: d.evidence, status: 'open', note: d.closes })
const lows = merged.filter(f => f.severity === 'low')

// A high finding that left the ledger without an independent second look blocks GO until a human has read the row:
// the skeptic returns real=false when it cannot confirm, and an agent's own already_recorded claim is unchecked.
const closedHigh = ledger.filter(b => b.severity === 'high' && (b.status === 'refuted' || b.status === 'closed-by-record'))
if (input.reviewedClosures !== true) for (const b of closedHigh) { b.note = `was ${b.status}, now review: ${b.note}`; b.status = 'review' }
const isOpen = b => b.status === 'open' || b.status === 'review'
const openBlockers = ledger.filter(isOpen)
const failedAgents = agentsSummary.filter(a => !a.returned).map(a => a.agent)
const agentsRow = agentsSummary.map(a => {
  const mine = ledger.filter(b => isOpen(b) && b.owner.startsWith(a.agent))
  if (!a.returned) return { ...a, result: 'DID NOT RETURN' }
  return { ...a, result: mine.length ? `${mine.length} open blocker(s)` : 'PASS' }
})
const hasBaseline = !!hashesBefore && Object.keys(hashesBefore).length > 0
const reasons = []
if (!hasBaseline) reasons.push('no hashesBefore baseline, so a change during the run cannot be ruled out')
if (failedAgents.length) reasons.push(`agent(s) did not return: ${failedAgents.join(', ')}`)
if (openBlockers.length) reasons.push(`${openBlockers.length} open blocker(s): ${openBlockers.map(b => b.id).join(', ')}`)
const verdict = reasons.length ? 'NO-GO' : 'GO'

// Pending approvals are vetted by the command gate again when agents proposed commands the first call never saw.
const unvetted = pending.filter(p => !commands.some(c => sameCmd(c, p)))
if (unvetted.length) {
  const g = await spawn(
    `Vet these ${unvetted.length} commands that other reviewers proposed for a human to run. Keep each command text unchanged and in order.\n` +
    unvetted.map((p, i) => `${i + 1}. machine: ${p.machine || '(not stated; treat as the robot)'}\n   command: ${p.command}`).join('\n') + '\n' + BASE,
    { agentType: AGENT('robot-command-gate'), label: 'command-gate:captures', phase: 'Sheet', schema: CMD_VERDICTS })
  for (const c of (g && g.commands) || []) cmdVerdicts.push(c)
  if (!g) notChecked.push('the commands other reviewers proposed were not vetted by the command gate (it did not return); run none of them without a check')
}
const gateRow = p => cmdVerdicts.find(c => sameCmd(c, p))
for (const c of commands) addPending('plan', c)
const cmdRows = pending.map(p => ({ ...p, verdict: (gateRow(p) || {}).verdict || 'NOT VETTED' }))
const runnable = cmdRows.filter(c => c.verdict !== 'FORBIDDEN')
const forbidden = cmdRows.filter(c => c.verdict === 'FORBIDDEN')

const cell = s => String(s == null ? '' : s).replace(/\|/g, '\\|').replace(/\n+/g, ' ')
const S = []
S.push('# Preflight sheet', '', `Change: ${change}`, machines.length ? `Machines in scope: ${machines.join('; ')}` : '', '')
S.push(`## Verdict: ${verdict} (provisional until the file-hash check)`, '')
S.push(verdict === 'GO' ? 'Every agent that ran returned and passed in this cycle, and no blocker is open.' : `Not cleared: ${reasons.join('; ')}.`)
S.push(`File-hash check: pending. The orchestrator hashes the files in hash_check.files_to_hash and calls this script again with recheck. Any difference turns this into STALE and the team reruns once.`, '')
const closedRows = ledger.filter(b => b.status === 'refuted' || b.status === 'closed-by-record' || b.status === 'review')
if (closedRows.length) {
  S.push('Closed without confirmation, read these before acting on the verdict (a high one blocks GO until you rerun with reviewedClosures: true):')
  for (const b of closedRows) S.push(`- ${b.id} ${b.severity} ${b.status}: ${cell(b.title)} (${cell(b.evidence)})`)
  S.push('')
}
S.push('## Agents', '', '| Agent | Result |', '|---|---|')
for (const a of agentsRow) S.push(`| ${cell(a.agent)} | ${cell(a.result)}${a.overall ? ' (' + cell(a.overall) + ')' : ''} |`)
for (const s of skipped) S.push(`| ${cell(s.split(':')[0])} | skipped:${cell(s.slice(s.indexOf(':') + 1))} |`)
S.push('', '## Blocker ledger', '')
if (!ledger.length) S.push('No blockers.')
else {
  S.push('| ID | Owner | Severity | Blocker | Evidence | Status | Note |', '|---|---|---|---|---|---|---|')
  for (const b of ledger) S.push(`| ${b.id} | ${cell(b.owner)} | ${b.severity} | ${cell(b.title)} | ${cell(b.evidence)} | ${b.status} | ${cell(b.note)} |`)
}
S.push('', '## Commands for you to run', '')
if (!runnable.length) S.push('None.')
else {
  S.push('| Verdict | Machine | Command | Why |', '|---|---|---|---|')
  for (const c of runnable) S.push(`| ${c.verdict} | ${cell(c.machine)} | \`${cell(c.command)}\` | ${cell(c.why)} |`)
}
if (forbidden.length) {
  S.push('', 'Do not run these (FORBIDDEN):', '')
  for (const c of forbidden) S.push(`- \`${cell(c.command)}\` on ${c.machine || 'the robot'}. ${cell((gateRow(c) || {}).why)}`)
}
if (lows.length) { S.push('', '## Low-severity notes (not blockers)', ''); for (const f of lows) S.push(`- ${f.title} at ${f.file}:${f.line}`) }
const uncovered = hasBaseline ? [...filesRead].filter(f => !(f in hashesBefore)) : []
const nc = [
  'No measurement on the live robot or network: every verdict is about files and records.',
  'The file-hash check runs outside this script.',
  hasBaseline ? '' : 'No hashesBefore was supplied, so a change during the run cannot be detected. The verdict cannot be GO.',
  uncovered.length ? `No hash baseline for ${uncovered.length} file(s) the agents read, so a change to them goes unseen: ${uncovered.join(', ')}` : '',
  ...skipped, ...notChecked,
].filter(Boolean)
S.push('', '## Not checked', '', ...nc.map(x => `- ${x}`))

const files_to_hash = [...new Set([...(hashesBefore ? Object.keys(hashesBefore) : []), ...filesRead])]
log(`verdict ${verdict}: ${reasons.join('; ') || 'no reasons against'}; agent calls used ${spawned} of ${HARD.agents}`)
return {
  verdict, verdict_note: 'provisional: becomes STALE if the file-hash check finds a difference', reasons,
  agents: agentsRow, skipped, ledger, commands: cmdRows, low_notes: lows, not_checked: nc, failed,
  hash_check: { status: 'pending', files_to_hash, hashes_before: hashesBefore },
  agent_calls: spawned, sheet: S.join('\n'),
}
