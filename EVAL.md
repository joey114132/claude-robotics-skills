# Evaluation

Everything here is the measured result, including the parts where the skills lost.

## Where it stands

On **single diagnostic questions with live search disabled**, these skills do **not** beat a strong model answering unaided. Measured blind across 8 cases: the skill won 2, the baseline won 4, 2 tied.

![Benchmark: skill-guided vs baseline across six expert-quality criteria](assets/benchmark.svg)

The pattern is consistent and worth stating plainly: the skill-guided answers are **deeper** — judges repeatedly noted they were the only ones to quantify a clearance budget, state an actual capability ceiling, or carry real citations — but they **pay for that depth** in two ways a reader feels immediately.

| Criterion | With skill | Baseline |
|---|---|---|
| Caught the expert trap | 100% | 100% |
| Explained the principle | 100% | 100% |
| Cited verifiable sources | 88% | 88% |
| Gave real options | 100% | 88% |
| No fabricated claims | 75% | 88% |
| Answered what was asked | 69% | 94% |

## Method

8 robotics questions across hand, legged, fleet, mobile, safety, perception, learning, and simulation. Each has one **planted trap** — a root cause an expert catches and a plausible-sounding answer misses. Example: "12-DOF quadruped on hobby RC servos, MPC or RL for trotting?" The correct answer refuses the framing, because position-only high-reduction servos cannot do dynamic locomotion at all.

Each question was answered twice — once by an agent following the relevant skill, once by the same model unaided. An independent judge then scored both on six criteria (0–2 each) **without being told which was which**, with presentation order alternated across cases to cancel position bias.

## What the benchmark actually found

**The planted traps did not discriminate.** The baseline caught all 8. These are traps a strong model already knows, so this benchmark cannot show a knowledge advantage — only a presentation difference.

**The skills leaked their own machinery into user-facing answers.** Asked one question about an overheating gripper, a skill-guided answer would still present a "Guided / Fast-forward / Audit" mode menu and mention its own file paths and search tooling. Judges scored that as failing to answer what was asked. *Fixed* — loop modes are now offered only when the work spans multiple decisions, and skills are told to answer from the field, not from their own machinery. Scope scores moved 56% → 69%.

**Snapshot facts were asserted with more precision than could be backed.** Specific versions and dates from `landscape.md` were stated flat while live re-verification was unavailable, which a judge correctly reads as fabrication risk. *Partly fixed*: 69% → 75%.

**One fix backfired, and the second run caught it.** Telling the skills to hedge unverifiable specifics made them drop standard *numbers* entirely — "the national robot safety standard" instead of the citable identifier — which cost source quality (100% → 88%). The instruction now hedges a claim's *currency* while keeping its identity, so a reader always has something to look up.

## Limitations — why this is a weak test of the actual design

- **Live search was unavailable during both runs**, which disables the mechanism these skills are built around. The result measures the snapshots alone, not the skills as designed.
- **One-shot diagnostics are the wrong shape.** These skills are advisory loops for multi-decision work; the option gate that reads as noise on "why is my servo hot?" is the entire point when scoping a build. This benchmark tested the wrong mode.
- One run per condition; no variance estimate.
- The judge is a language model applying a rubric, not a practicing roboticist.

## A note on the earlier number

An earlier iteration reported **100% vs 83.8%** in favor of the skills. That figure should not be trusted: the assertions were written by the same author as the skills and rewarded the skills' own output format (present options, cite the textbook, stop at a gate) rather than answer quality. The blind rubric above replaced it and reached the opposite conclusion. The old number is recorded here only so nobody re-quotes it.

## What would be a fair test

Live search enabled, multi-turn advisory scenarios rather than one-shot questions, questions whose answers actually turned over recently (so a stale answer is detectably wrong), and a human robotics reviewer alongside the model judge.

## Reproducing

```sh
python3 scripts/make_bench_chart.py <workspace-with-grade-json>
```

Each case directory holds both answers and the judge's `grade.json`, so the scoring can be re-read rather than taken on trust.
