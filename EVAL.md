# Evaluation

Eight rounds of blind measurement, published as measured — including the six rounds where the skills lost.

## Headline

Final round, all **14 blind-judged robotics questions**: skills won 8, baseline won 4, 2 tied. Total rubric score **96% vs 93%**.

The first blind measurement was 2 wins against 10.

![Benchmark: skill-guided vs baseline across six expert-quality criteria, 14 cases](assets/benchmark.svg)

| Criterion | With skill | Baseline |
|---|---|---|
| Caught the trap / delivered the expert value | **100%** | 93% |
| Cited verifiable sources | **100%** | 82% |
| Answered what was asked | **100%** | 89% |
| Gave real options | **100%** | 96% |
| Explained the principle | 100% | 100% |
| No fabricated claims | 75% | **96%** |

Five of six criteria at 100%. One criterion — fabrication discipline — is still behind, and it is the same one that has resisted every round.

## Method

Two question shapes, one rubric, one protocol. **Diagnostic** (8 cases): "why is this happening" questions each carrying a planted trap an expert catches — e.g. "12-DOF quadruped on hobby RC servos, MPC or RL for trotting?", where the right answer refuses the framing because position-only servos cannot do dynamic locomotion at all. **Design** (6 cases): "we're building X, how should we approach it", where imposing the right decision order is the graded value.

Each question answered twice — once following the relevant skill, once by the same model unaided. An independent judge scored both **without knowing which was which**, presentation order alternated across cases. Baselines were generated once and reused unchanged through every round, so only the skills varied. Each case directory keeps both answers and the judge's `grade.json`.

## Eight rounds — what moved and what didn't

| Round | Change | Cases (S-B-T) | Scope | Sources | Fabrication |
|---|---|---|---|---|---|
| v2 | original skills | 2-5-1 /8 | 56% | — | 69% |
| v3–v4 | gate the mode menu; hedge unverifiables | 2-5-1 /8 | 69% | — | 75% |
| design | (same skills, right question shape) | 1-5-0 /6 | 50% | — | 75% |
| v5 | **structural inversion** | 4-7-1 /12 | 96% | — | 83% |
| v6 | inline source attribution | 6-6-0 /12 | 100% | 96% | 83% |
| v7 | snapshot as hard citation boundary | 6-7-1 /14 | 100% | 82% | 79% |
| v8 | **two-class citation rule + carry source URLs** | **8-4-2 /14** | **100%** | **100%** | 75% |

Three findings are worth more than the tally.

**Structure beat wording.** Three rounds of added rules moved almost nothing. What worked was inverting the document: the decision sequence became an internal completeness checklist instead of the reply's outline, and delivery rules — verdict first, deliver in one pass, defer only when interaction is genuinely available — moved to the top. Scope went from the skills' worst criterion (56%) to a perfect score.

**Over-caution costs as much as over-claiming.** v7 told the skills to drop unverifiable specifics; they responded by dropping *verifiable* ones too, and sources fell 96% → 82%. One answer was marked down for being "correct but generic, cites no specific tools". The v8 rule splits the two classes explicitly — stable identifiers (library and plugin names, CLI commands, parameter names, standard numbers) are said freely and concretely; things that decay (release dates, support windows, prices, masses, "latest" anything) do not leave the snapshot without a live check. Sources recovered to 100%.

**Use the asset you already have.** The snapshots carry a `Source:` URL per entry, and until v8 the answers never passed it through — they said "per REP-2000" and asked the reader to trust it. Carrying the actual link is what moved sources 18 points in one round. It was sitting there the whole time.

## The one criterion still behind

Fabrication stayed at 75%. The v8 judge notes name the cause precisely and consistently: **unverifiable arXiv IDs and vendor spec numbers**. "Asserts five unhedged arXiv IDs", "~7 unverifiable post-cutoff claims", "marketing-blog citations for hard specs including a ~30 kg ANYmal mass". Two-class splitting did not fix it, because a paper ID *looks* like a stable identifier while being exactly the kind a model reconstructs wrongly.

The honest read: this is the deficit that **live search exists to close**, and live search was unavailable in all eight rounds. The rule these skills are built on is verify-then-speak; every round measured them with the verify step amputated. Whether verify-then-speak, actually allowed to verify, converts this deficit into a strength is the open question this benchmark cannot answer.

## Limitations — read the result narrowly

- **One run per condition.** v7 was 6-7-1 and v8 is 8-4-2 on the same cases; part of that swing is noise. The claim this supports is "no longer behind, and clearly ahead on five criteria" — not a precise effect size.
- **Live search disabled throughout**, which both handicaps the skills' core mechanism and makes the fabrication criterion harsher than normal operation.
- Single-turn evaluation penalizes an interactive design; the judge is a language model applying a rubric, not a practicing roboticist.
- The author of the skills also designed the benchmark. Blind judging and a fixed rubric limit that conflict without eliminating it.

## An earlier number, retracted

An earlier iteration reported **100% vs 83.8%** for the skills. Do not trust it: its assertions rewarded the skills' own output format rather than answer quality. The blind rubric replaced it, and immediately showed the opposite. Recorded here only so nobody re-quotes it.

## Reproducing

```sh
python3 scripts/make_bench_chart.py <workspace> [<workspace> ...]
```
