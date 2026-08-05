# Evaluation

Everything here is the measured result, through seven rounds of fix-and-remeasure. The final verdict is parity, not superiority — published as measured.

## Headline

Final round, all **14 blind-judged robotics questions**: skills won 6, baseline won 7, 1 tie. Total rubric score 92% vs 94%.

That is a draw within single-run noise — and it took seven rounds to get there from a clear loss. The first blind measurement was 2 wins against 10.

![Benchmark: skill-guided vs baseline across six expert-quality criteria, 14 cases](assets/benchmark.svg)

| Criterion | With skill | Baseline |
|---|---|---|
| Caught the trap / delivered the expert value | **100%** | 96% |
| Answered what was asked | **100%** | 82% |
| Explained the principle | 96% | **100%** |
| Gave real options | 96% | **100%** |
| Cited verifiable sources | 82% | **86%** |
| No fabricated claims | 79% | **100%** |

The shape of the result is stable across rounds: **the skills are strongest on substance** (they caught every planted trap, and judges repeatedly called their answers the deeper ones) **and lose on fabrication discipline** — carrying specifics out of their snapshots that a reader of one page cannot verify.

## Method

Two question shapes, same six-criteria rubric, same protocol. **Diagnostic** (8 cases): "why is this happening" questions, each with one planted trap an expert catches — e.g. "12-DOF quadruped on hobby RC servos, MPC or RL for trotting?", where the right answer refuses the framing because position-only servos cannot do dynamic locomotion. **Design** (6 cases): "we're building X, how should we approach it", where imposing the right decision order is the graded value.

Each question answered twice — once following the relevant skill, once by the same model unaided. An independent judge scored both **without knowing which was which**, presentation order alternated. Every case directory keeps both answers and the judge's `grade.json`.

## The seven rounds — what moved and what didn't

| Round | Change | Cases (S-B-T) | Scope | Fabrication |
|---|---|---|---|---|
| v2 | original skills | 2-5-1 (of 8) | 56% | 69% |
| v3-v4 | gate the mode menu; hedge unverifiables | 2-5-1 (of 8) | 69% | 75% |
| design set | (same skills, right question shape) | 1-5-0 (of 6) | 50% | 75% |
| v5 | **structural inversion** | 4-7-1 (of 12) | 96% | 83% |
| v6 | inline source attribution | 6-6-0 (of 12) | 100% | 83% |
| v7 (final) | snapshot as hard citation boundary | **6-7-1 (of 14)** | **100%** | 79% |

Two findings matter more than the tally:

**Structure beat wording.** Three rounds of added rules moved almost nothing. What worked was inverting the document: the decision sequence became an internal completeness checklist instead of the reply's outline, and delivery rules ("verdict first, deliver everything in one pass, defer only when you can actually ask") moved to the top. Scope went from the skills' worst criterion (56%) to their best (100%) — they now both answer the question *and* out-cover the baseline.

**Fabrication is the unsolved criterion, and the last fix overcorrected.** Judges consistently flagged specifics the answer could not stand behind — feature lists, prices, reconstructed arXiv IDs. Tightening the citation boundary helped some cases and hurt others: one final-round answer was scored down for being "correct but generic, cites no specific tools", exactly the over-caution the rule induced. Calibrating "say the checkable specific, drop the unverifiable one" is genuinely hard for a one-page answer with live search disabled.

## Limitations

- **Live search was unavailable in every run** — the mechanism the skills are built around (verify, then speak) was disabled, which is precisely why snapshot specifics kept scoring as unverifiable.
- Single-turn evaluation penalizes an interactive design; one run per condition; the judge is a language model applying a rubric, not a practicing roboticist.
- Author and fixer of the skills also designed the benchmark. The blindness and fixed rubric limit, but do not eliminate, that conflict.

## An earlier number, retracted

An earlier iteration reported **100% vs 83.8%** in favor of the skills. Do not trust it: its assertions rewarded the skills' own output format rather than answer quality. The blind rubric replaced it. Recorded here only so nobody re-quotes it.

## What this means for using the collection

For a robotics question you could just ask, **asking directly is fine** — the base model catches the classic traps on its own. What the measurements say the skills actually add:

- **Completeness under pressure** (100% expert value, 100% scope): the internal checklist reliably surfaces the parts of a build the unaided answer covers only at 82-96%.
- **The verified snapshots**: `references/landscape.md` records what a model's memory gets wrong — archived repos, superseded standards — and `scripts/check_sources.py` re-validates every source URL on demand.
- With **live search enabled** (normal operation, unlike this benchmark), the fabrication weakness is addressed by design: the rule is verify-then-speak, and what was measured here is the skills running with their verification amputated.

That last point is the fair-test question this benchmark leaves open: whether verify-then-speak, actually allowed to verify, converts the fabrication deficit into a strength. Measuring that needs live search, multi-turn scenarios, and recency-sensitive questions.

## Reproducing

```sh
python3 scripts/make_bench_chart.py <workspace> [<workspace> ...]
```
