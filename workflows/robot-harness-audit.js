export const meta = {
  name: 'robot-harness-audit',
  description: 'Audit a robot actuator path against the physical-ai-harness checklist: four axis auditors in parallel, code dedupe, then a blind skeptic per high or medium finding',
  phases: [
    { title: 'Audit', detail: '4 axis auditors in parallel' },
    { title: 'Verify', detail: 'one blind skeptic per high or medium finding' },
  ],
}

// args: { root: "<repo path>", scope: ["<files>"], records: ["<decision record files>"] }
const root = args && args.root
const scope = args && Array.isArray(args.scope) ? args.scope : []
const records = args && Array.isArray(args.records) ? args.records : []
if (!root || !scope.length) {
  log('robot-harness-audit needs args {root, scope: [files], records: [decision record files]}; nothing to do')
  return { findings: [], verdicts: [] }
}

const BRIEF = `Read-only audit of the command path in ${root}. Edit nothing and run nothing that touches a robot.
Treat the producer of commands (a learned policy, a teleoperation input, any non-deterministic source) as a participant on the actuator path that must be held to an output region, an inference or loop budget and an operating regime.
Audit against the physical-ai-harness checklist.
Files in scope: ${scope.join(', ')}. You may follow imports out of these files when needed.
Decision records you MUST read before reporting anything: ${records.length ? records.join(', ') : '(none listed: search the repository for intent, ADR, troubleshooting and handoff files and say which you found)'}.
If a record already documents a gap as fixed, rejected or deliberately out of scope, drop it or report it with already_recorded=true and the record line. An open question or pending decision is not a closing record.
Never report a path you have not opened. Every finding needs a real file and line you read.
Report only gaps (status missing or partial) with severity. Quality over count.`

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
  },
  required: ['findings'],
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
  { key: 'transfer', focus: 'Transfer and composition: fallback to a verified baseline (hold, park, stop, gravity compensation), who triggers it automatically, how authority returns (positive signal versus absence of fault), a controller-side command timeout if the gate dies, and whether thresholds live in one profile or are scattered across nodes and runtime-settable parameters.' },
]

phase('Audit')
const res = await parallel(AXES.map(a => () =>
  agent(`${BRIEF}\n\nYour axis: ${a.focus} Stay on this axis; another auditor covers each other axis.`,
    { agentType: 'harness-axis-auditor', label: `audit:${a.key}`, phase: 'Audit', schema: FINDINGS })))

// Dedupe in code: same file basename and nearby line bucket is one issue. Highest severity goes first so it is the one kept.
const RANK = { high: 0, medium: 1, low: 2 }
const all = res.filter(Boolean).flatMap(r => r.findings).sort((x, y) => RANK[x.severity] - RANK[y.severity])
const seen = new Set()
const merged = []
for (const f of all) {
  const k = `${f.file.split('/').pop()}:${Math.round(f.line / 5)}`
  if (seen.has(k)) { log(`dedup dropped "${f.title}" (${k})`); continue }
  seen.add(k)
  merged.push({ ...f, id: `F${merged.length + 1}` })
}
log(`auditors returned ${all.length}, merged ${merged.length}, failed auditors ${res.filter(r => !r).length}`)

phase('Verify')
const toVerify = merged.filter(f => f.severity === 'high' || f.severity === 'medium')
const unverified = merged.filter(f => f.severity === 'low')
const verdicts = await pipeline(toVerify, f => agent(
  `Verify finding ${f.id}. Claimed defect in the command path at ${root}:\n` +
  `title: ${f.title}\nfile: ${f.file}\nline: ${f.line}\nseverity: ${f.severity}\nevidence: ${f.evidence}\n\n` +
  `Try to REFUTE it. Open the cited file and line and the code it depends on, and check these decision records for an entry that fixes, rejects or deliberately scopes it out: ` +
  `${records.length ? records.join(', ') : '(none listed: search the repository for intent, ADR, troubleshooting and handoff files)'}. ` +
  `Return id "${f.id}".`,
  { agentType: 'finding-skeptic', label: `verify:${f.id}`, phase: 'Verify', schema: VERDICT }))

const v = verdicts.filter(Boolean)
log(`verified ${v.length}/${toVerify.length}; real ${v.filter(x => x.real).length}; closed by record ${v.filter(x => x.closed_by_record).length}`)
log(`not verified by design (low severity): ${unverified.map(f => `${f.id} ${f.title}`).join('; ') || 'none'}`)

return { findings: merged, verdicts: v }
