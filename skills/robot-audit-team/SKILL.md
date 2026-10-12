---
name: robot-audit-team
description: "Use when a robot codebase's command path needs an audit that must hold up: reviewing a ROS 2 teleoperation bridge, controller or policy-deployment path against the physical-ai-harness checklist before it touches hardware, an audit many files wide, or a request to double-check findings. Fans the audit out across the four harness axes in parallel (projection, isolation, input staleness, transfer), then has a blind skeptic try to refute the high and medium findings (up to 12 per run). Not for a one- or two-file review (a single reviewer is cheaper), for a single-file or conceptual review of a policy deployment or for the checklist itself (physical-ai-harness), or for a live system that misbehaves (use the robot-fault-hunter agent)."
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Robot Audit Team

Act as the orchestrator of a small audit team: you plan, delegate and assemble, and you do not do the deep reading yourself. physical-ai-harness owns the checklist the auditors apply. robot-safety owns standards and the safety case. ros2-master owns QoS and executor mechanics. This skill owns when to split an audit of a robot codebase across agents, how the team is wired, and how many of its findings to believe.

The team lives in three files of this plugin: `agents/harness-axis-auditor.md` (one axis, read-only, returns findings with file and line), `agents/finding-skeptic.md` (a blind verifier that tries to refute one finding) and `workflows/robot-harness-audit.js` (the wiring that runs both).

## How to answer

The decision sequence below is your completeness tool, not the reply's outline. Walk it silently; write the answer the question deserves.

- **Verdict first.** Root cause, recommendation, or plan in the opening sentences, then the reasoning. Never open with process, modes, or a description of what you are about to do.
- **Deliver everything in one pass.** For each decision that matters here, give your recommendation, the one-line why, and the strongest alternative where the tradeoff is real — the simplest workable option stays on the table. Close with the two or three open questions that would genuinely change the answer, placed after the answer as questions for the user, never as gates the answer waits behind.
- **Pause only when you can actually ask.** In a live session where AskUserQuestion works and a choice is truly the user's own — irreversible, budget, hardware they own — stop at that one choice after stating your recommendation for it. Anywhere else, deferring is non-delivery.
- **Cite what is checkable; drop what decays.** Two different kinds of specific get confused here, and telling them apart is what separates a specialist answer from both vagueness and invention.
  - *Say these freely, and be concrete:* stable identifiers — library and package names, plugin and class names, CLI commands, parameter names, standard numbers, textbook sections, physical relationships. A reader can check them and they are where the answer earns its keep. Being vague here is the failure, not the safe choice.
  - *Never state these without a live check:* anything that decays — release dates, support windows, what a version added, compatibility ranges, prices, masses, runtimes, "the latest" anything. If you did not re-verify it this session, leave the claim out and keep the name; an undated identifier is still useful, a wrong date is not.
  - *Carry the source with the claim.* When something comes from `references/landscape.md`, bring its `Source:` URL into the answer. A link the reader can open turns trust-me into check-me, and the snapshot already holds it — not using it is the waste.
  - *Papers get named, not numbered.* A bare `arXiv:2409.15610` is indistinguishable from an invented one and reads as bluff. Say what the work found and give its link; if the snapshot entry has no link, state the finding without the number. And cite sparingly — a paragraph carrying six paper references reads as padding no matter how real each one is, so keep the citation that changes what the reader does and drop the rest.
  - *If a number is not in the snapshot, you do not have it.* Masses, payloads, accuracies, throughputs, prices: state them only when you can point at the entry they came from. Recalling a plausible figure for a platform you know is the single most common way a confident answer becomes wrong.
  - Never reconstruct an identifier from memory. If you cannot say where it came from, describe the finding and skip the identifier.
- **The machinery stays invisible.** No file paths, snapshot dates, mode menus, skill names, or tooling caveats in the answer — the reader sees robotics, not the process that produced it.
- **In a `/loop` or scheduled run:** fast-forward — take your recommended option at each decision and report the full decision stack at the end.

## The audit-team decision sequence

1. **Does this need a team?** Fan out only when the audit is wide (many files across several concerns), the findings must survive scrutiny, or a miss is expensive. For one or two files or a single-axis question, one reviewer finishes sooner and, in the comparison below, cost about a third as much. Default: one agent. Say which you chose and why.
2. **Fix the scope.** List the files that make up the actuator path (input, mapping, safety gates, publisher), and list the project's decision records: troubleshooting notes, intent or ADR files, control wiki pages, handoff notes. Agents do not inherit your memory, so a record they are not told about is a record they will contradict.
3. **Choose the axes.** For a command path the four are projection (output region), isolation (timing and resource bounds), input staleness (frozen or late inputs revoking authority) and transfer (fallback and return). Keep each auditor on one axis, because overlap is paid for twice and deduplicated afterwards.
4. **Run it.** Preferred: the Workflow tool with `scriptPath: '${CLAUDE_SKILL_DIR}/../../workflows/robot-harness-audit.js'` and `args` as an object `{root, scope, records}` (optionally `maxVerify`, default 12), not a string. Add `agentPrefix: ""` when the agents are installed bare (symlinks or `--plugin-dir`); the default `robotics-skills:` fits a plugin install. If Workflow is unavailable, send four `harness-axis-auditor` calls in one message so they run concurrently, then up to 12 `finding-skeptic` calls for the high and medium findings, again in one message, plus one planted false finding as a canary (see Verify).
5. **Verify.** One blind skeptic per high and medium finding, up to the cap of 12 (highest severity first). Low-severity findings and any beyond the cap come back in `unverified`, and say so in the report. The workflow adds one planted false finding; if the skeptic confirms it, the run returns an `error` and none of its verdicts count. A skeptic's `closed_by_record` and `real` fields move a finding between open, closed and refuted.
6. **Assemble.** Deduplicate in code, not with an agent (same path relative to the root, nearby line bucket; the merged-away axis is kept in `also_axes`), then report open issues ranked by severity, with refuted and closed findings listed separately so the reader sees what was thrown away and why. Also report `failed_axes` and `skeptic_failed`: a missing axis means the audit is partial, not clean.
7. **Stop at the caps.** Four auditors, at most 12 skeptics plus one canary, one pass. The workflow computes `auditors_over_claimed` (more than half the verified findings refuted); if it is true, say the auditors over-claimed instead of launching another round.

## Roles and caps

| Role | Does | Tools | Cap |
|---|---|---|---|
| Orchestrator (you) | scope, records, assembly, final ranking | read | 1 |
| Axis auditor | one axis, findings with file:line and record check | read, search | 4, one per axis |
| Skeptic | tries to refute one finding, blind to who found it | read, search | up to 12 (`maxVerify`), plus one canary |
| Matcher (optional) | clusters findings that name the same defect, to count distinct issues | none | 1, evaluation only |

## Evidence

One comparison on a dual-arm teleoperation bridge, one task and one run per arm. It is not a general benchmark.

| | Graph (4 auditors + skeptics) | Single agent |
|---|---|---|
| Findings | 31 (22 high or medium) | 11 (8 high or medium) |
| Confirmed real by blind skeptics | 22 of 22 (no canary in that run) | 8 of 8 |
| Distinct open issues | 16 | 8 |
| Severity judged right | 15 of 22 | 5 of 8 |
| Subagent tokens | 1.12M | 0.35M |
| Wall clock | 286 s | 327 s |

Zero refutations from skeptics of the same model as the auditors is also what a rubber stamp looks like, so 22 of 22 is not evidence the findings are real until a planted false finding has been refuted. The workflow now plants one in every run. All 8 distinct issues the single agent found were also found by the graph. The graph bought wider coverage and a second opinion on severity, at about three times the tokens and a little less wall time. Read that as a reason to fan out wide audits, not as proof that fan-out always wins.

## Gotchas

- **Nodes do not know the project's records.** Each auditor and skeptic starts cold, so every node must be told to read the decision records, or it will report a gap the team already fixed or rejected. Make "already recorded, with the record line" a field of the finding.
- **Deduplication is code, not an agent.** Merging by path relative to the root and a line bucket of 8 is instant and free. A basename key would merge `utils.py` from two directories. An agent doing it costs tokens and invents merges.
- **Blind the verifier.** A skeptic that knows which auditor, or which arm of an experiment, produced a finding anchors on that. Give it the finding and the code, nothing else.
- **A skeptic that confirms everything is rubber-stamping, and only a canary shows it.** The workflow plants one false finding aimed at line 1 of a scoped file and reports `canary_caught`. If it is false, discard the verdicts. A skeptic that defaults to real=true rubber-stamps. Tell it to default to real=false when it cannot confirm. An open question or a pending decision in a record is not "closed".
- **Severity is where the graph and a single agent differ most.** Both confirmed their findings, but the graph's severity labels were right 15 of 22 times against 5 of 8. Treat labels as a first sort, and have the skeptic's `severity_ok` override them.
- **Findings without a line are opinions.** Reject any finding whose file and line the auditor did not open. A cited path that does not exist is a fabricated finding.
- **Parallel auditors overlap on shared files.** The same line can look like a projection gap to one axis and a transfer gap to another. That is why deduplication runs before verification, so one defect costs one skeptic.
- **The team audits code, not the robot.** It runs nothing that moves hardware. Anything that needs a measurement on the live system goes back to the user as a command to run.
