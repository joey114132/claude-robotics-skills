export const meta = {
  name: 'robot-harness-audit',
  description: 'Audit a robot actuator path against the physical-ai-harness checklist: four axis auditors in parallel, code dedupe, then a blind skeptic per high or medium finding, with one planted canary to prove the skeptic can refute',
  phases: [
    { title: 'Audit', detail: '4 axis auditors in parallel' },
    { title: 'Verify', detail: 'one blind skeptic per high or medium finding (capped), plus one canary' },
  ],
}

// args: { root: "<repo path>", scope: ["<files>"], records: ["<decision record files>"], maxVerify?: 12, agentPrefix?: "robotics-skills:" }
// agentPrefix is put in front of each agent name. The default fits a plugin install; pass "" when the agents are
// installed bare (symlinks into ~/.claude/agents, or --plugin-dir).
// Pass args as an object. A JSON string is accepted and parsed, because a stringified object is a common slip.
let input = args
if (typeof input === 'string') {
  try { input = JSON.parse(input) } catch (e) { return { error: 'args arrived as a string that is not JSON; pass an object {root, scope, records}' } }
}
const root = input && input.root
const scope = input && Array.isArray(input.scope) ? input.scope : []
const records = input && Array.isArray(input.records) ? input.records : []
const MAX_VERIFY = (input && input.maxVerify) ?? 12
const PREFIX = input && input.agentPrefix !== undefined ? input.agentPrefix : 'robotics-skills:'
if (typeof PREFIX !== 'string') return { error: 'agentPrefix must be a string ("" for bare agent names); nothing was audited' }
const AGENT = name => PREFIX + name
const MIN_BUDGET_TO_VERIFY = 150000
if (!root || !scope.length) return { error: 'needs args {root, scope: [files], records: [decision record files]}; nothing was audited' }

const BRIEF = `Read-only audit of the command path in ${root}. Edit nothing and run nothing that touches a robot.
Treat the producer of commands (a learned policy, a teleoperation input, any non-deterministic source) as a participant on the actuator path that must be held to an output region, an inference or loop budget and an operating regime.
Audit against the physical-ai-harness checklist.
Files in scope: ${scope.join(', ')}. You may follow imports out of these files when needed.
Decision records you MUST read before reporting anything: ${records.length ? records.join(', ') : '(none listed: search the repository for intent, ADR, troubleshooting and handoff files and say which you found)'}.
If a record already documents a gap as fixed, rejected or deliberately out of scope, drop it or report it with already_recorded=true and the record line. An open question or pending decision is not a closing record.
Never report a path you have not opened. Every finding needs a real file and line you read.
Report only gaps (status missing or partial) with severity. Quality over count.
List every decision record and file you actually opened in records_read.`

const FINDINGS = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          axis: { type: 'string', enum: ['projection', 'isolation', 'input_staleness', 'transfer', 'composition'] },
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
    records_read: { type: 'array', items: { type: 'string' } },
  },
  required: ['findings', 'records_read'],
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

const AXES = [
  { key: 'projection', focus: 'Projection: per-sample output region checks on commands (range, step size, workspace, staleness of the command stamp), clamping versus rejecting, lifecycle-state gating before a command reaches the controller.' },
  { key: 'isolation', focus: 'Isolation: timing and resource bounds of the command loop (executor, callback groups, timers, loop rate, publish cadence), what happens when a callback overruns, QoS deadline and lifespan on command topics.' },
  { key: 'input_staleness', focus: 'Input staleness: how a stale or frozen input or feedback is detected (timestamps, gaps, lag clamp) for every stream the producer reads, and whether staleness revokes command authority instead of acting on the last value.' },
  { key: 'transfer', focus: 'Transfer: fallback to a verified baseline (hold, park, stop, gravity compensation), who triggers it automatically, how authority returns (positive signal versus absence of fault), a controller-side command timeout if the gate dies, and whether thresholds live in one profile or are scattered across nodes and runtime-settable parameters.' },
]

phase('Audit')
const res = await parallel(AXES.map(a => () =>
  agent(`${BRIEF}\n\nYour axis: ${a.focus} Stay on this axis; another auditor covers each other axis.`,
    { agentType: AGENT('harness-axis-auditor'), label: `audit:${a.key}`, phase: 'Audit', schema: FINDINGS })))

const failed_axes = AXES.filter((a, i) => !res[i]).map(a => a.key)
const records_read = {}
AXES.forEach((a, i) => { if (res[i]) records_read[a.key] = res[i].records_read })
const axes_without_records = records.length ? AXES.filter((a, i) => res[i] && !res[i].records_read.length).map(a => a.key) : []

// Dedupe in code. Key = path relative to root + line bucket of 8, so utils.py in two directories stay apart.
// Highest severity goes first so it is the finding kept; the axis of a merged-away finding is kept in also_axes.
const RANK = { high: 0, medium: 1, low: 2 }
const rel = f => (f.startsWith(root + '/') ? f.slice(root.length + 1) : f).replace(/^\.\//, '')
const all = res.filter(Boolean).flatMap(r => r.findings).sort((x, y) => RANK[x.severity] - RANK[y.severity])
const byKey = new Map()
const merged = []
for (const f of all) {
  const k = `${rel(f.file)}:${Math.floor(f.line / 8)}`
  if (byKey.has(k)) {
    const kept = byKey.get(k)
    if (f.axis !== kept.axis && !kept.also_axes.includes(f.axis)) kept.also_axes.push(f.axis)
    log(`dedup merged "${f.title}" (${f.axis}) into ${kept.id} (${k})`)
    continue
  }
  const kept = { ...f, id: `F${merged.length + 1}`, also_axes: [] }
  byKey.set(k, kept)
  merged.push(kept)
}
log(`auditors returned ${all.length}, merged ${merged.length}, failed axes: ${failed_axes.join(', ') || 'none'}`)

phase('Verify')
const eligible = merged.filter(f => f.severity === 'high' || f.severity === 'medium')
const low = merged.filter(f => f.severity === 'low')

if (budget.total && budget.remaining() < MIN_BUDGET_TO_VERIFY) {
  log(`budget guard: ${Math.round(budget.remaining() / 1000)}k tokens left, below ${MIN_BUDGET_TO_VERIFY / 1000}k; verification skipped`)
  return { findings: merged, verdicts: [], failed_axes, records_read, axes_without_records,
           unverified: merged.map(f => ({ id: f.id, title: f.title, severity: f.severity, reason: 'verification skipped: budget' })),
           skeptic_failed: 0, canary_caught: null, auditors_over_claimed: null }
}

const toVerify = eligible.slice(0, MAX_VERIFY)
const overflow = eligible.slice(MAX_VERIFY)
if (overflow.length) log(`verify cap ${MAX_VERIFY}: not verified: ${overflow.map(f => `${f.id} ${f.title}`).join('; ')}`)
const unverified = [
  ...overflow.map(f => ({ id: f.id, title: f.title, severity: f.severity, reason: `over the verify cap of ${MAX_VERIFY}` })),
  ...low.map(f => ({ id: f.id, title: f.title, severity: f.severity, reason: 'low severity, not verified by design' })),
]

// Canary: a planted false finding, indistinguishable from the real ones, that points at line 1 of a scoped file.
// A skeptic that confirms it is rubber-stamping, and every "confirmed" in this run is then worthless.
const CANARY_ID = `F${merged.length + 1}`
const canary = {
  id: CANARY_ID, severity: 'high', file: scope[0], line: 1,
  title: 'Command is published before any range check runs',
  evidence: 'The publish call at this line sends the command before the range check, so an out-of-range sample reaches the controller.',
}
const stages = [...toVerify, canary]

const verdicts = await pipeline(stages, f => agent(
  `Verify finding ${f.id}. Claimed defect in the command path at ${root}:\n` +
  `title: ${f.title}\nfile: ${f.file}\nline: ${f.line}\nseverity: ${f.severity}\nevidence: ${f.evidence}\n\n` +
  `Try to REFUTE it. Open the cited file and line and the code it depends on, and check these decision records for an entry that fixes, rejects or deliberately scopes it out: ` +
  `${records.length ? records.join(', ') : '(none listed: search the repository for intent, ADR, troubleshooting and handoff files)'}. ` +
  `Return id "${f.id}".`,
  { agentType: AGENT('finding-skeptic'), label: `verify:${f.id}`, phase: 'Verify', schema: VERDICT }))

const canaryVerdict = verdicts.find(x => x && x.id === CANARY_ID)
const v = verdicts.filter(x => x && x.id !== CANARY_ID)
const skeptic_failed = toVerify.length - v.length
const canary_caught = canaryVerdict ? canaryVerdict.real === false : null
const refuted = v.filter(x => !x.real).length
const auditors_over_claimed = v.length ? refuted * 2 > v.length : null
log(`verified ${v.length}/${toVerify.length}; real ${v.length - refuted}; refuted ${refuted}; closed by record ${v.filter(x => x.closed_by_record).length}; skeptic failures ${skeptic_failed}`)
log(`canary caught: ${canary_caught}`)
if (auditors_over_claimed) log('more than half of the verified findings were refuted: the auditors over-claimed; do not start another round')
log(`not verified: ${unverified.map(f => `${f.id} ${f.title} (${f.reason})`).join('; ') || 'none'}`)

const out = { findings: merged, verdicts: v, failed_axes, records_read, axes_without_records, unverified, skeptic_failed, canary_caught, auditors_over_claimed }
if (canary_caught === false) {
  out.error = `CANARY CONFIRMED: the skeptic called the planted false finding real (${canaryVerdict.reason}). Its verdicts cannot be trusted; do not report any finding as confirmed.`
  log(out.error)
} else if (canary_caught === null) {
  log('canary skeptic failed to return: this run is uncalibrated, report its verdicts as unchecked')
}
return out
