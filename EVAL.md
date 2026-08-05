# Evaluation

Nine rounds of blind measurement. The honest summary is **parity with two large opposing effects** — not the win the previous version of this file claimed.

## Headline

Latest round, 14 blind-judged questions: skills 93%, baseline 93%.

![Benchmark: skill-guided vs baseline across six expert-quality criteria, 14 cases](assets/benchmark.svg)

| Criterion | With skill | Baseline |
|---|---|---|
| Cited verifiable sources | **100%** | 79% |
| Caught the trap / delivered the expert value | **100%** | 96% |
| Explained the principle | **100%** | 96% |
| Gave real options | 100% | 100% |
| Answered what was asked | 89% | 89% |
| No fabricated claims | 71% | **100%** |

Two effects are large and reproduce across rounds; the rest is close to a wash. The skills **cite roughly 20 points better** and **score roughly 25 points worse on fabrication discipline**. Those cancel.

## Read this before any tally

Baseline answers were generated once and reused unchanged in every round, so their score measures pure judge noise on fixed text: **94%, 93%, 93%** across the last three rounds — about a point. Skill answers are regenerated each round, and their totals ran **92%, 96%, 93%** on the same 14 cases with the same rubric.

At case level that is:

| Round | Cases (skill-baseline-tie) | Skill total |
|---|---|---|
| v7 | 6-7-1 | 92% |
| v8 | 8-4-2 | 96% |
| v9 | 4-6-4 | 93% |

Wins swing from 4 to 8 on identical questions. **A single round cannot resolve a difference of two or three cases**, and an earlier version of this file reported the 8-4-2 round as a headline win. That was reading noise as signal; it is retracted here. Criterion-level scores, which average over 14 cases, are the only numbers worth quoting.

## Method

Two question shapes, one rubric. **Diagnostic** (8 cases): "why is this happening" questions each carrying a planted trap — e.g. "12-DOF quadruped on hobby RC servos, MPC or RL for trotting?", where the right answer refuses the framing because position-only servos cannot do dynamic locomotion at all. **Design** (6 cases): "we're building X, how should we approach it", where imposing the right decision order is the graded value.

Each question answered twice — once following the relevant skill, once by the same model unaided. An independent judge scored both **without knowing which was which**, presentation order alternated. Each case directory keeps both answers and the judge's `grade.json`.

## What is actually established

**The citation gain is real and reproduced.** Sources scored 100% against a 79-82% baseline in two consecutive rounds. The cause is mechanical: `references/landscape.md` carries a source URL per entry, and the skills now pass that link into the answer instead of asserting the fact bare. The single largest jump in the whole project came from using an asset that was already sitting in the files.

**Structure beat wording.** Three early rounds of added rules moved almost nothing. What worked was inverting the document — making the decision sequence an internal completeness checklist rather than the reply's outline, and putting delivery rules first. Scope went from 56% to consistently 89-100%.

**"Fabrication" is not measuring fabrication.** This is the finding worth carrying away. Judges flagged unverifiable arXiv IDs every round, so we checked: of **29 arXiv IDs cited across the answers, 29 came from the verified snapshots and 0 were invented.** The criterion is largely measuring *whether a judge with no search can confirm a reference* — not whether the model made it up. Two things did turn out to be genuinely wrong: paper IDs were being emitted as bare numbers with no link (fixed — 98 snapshot entries now carry canonical `arxiv.org/abs/` URLs), and one answer quoted a platform mass that was not in its snapshot at all (a real rule violation, now explicitly barred).

**Four targeted attempts never moved fabrication up** (69% → 75% → 79% → 75% → 71%). Every attempt to make the skills more careful cost something elsewhere: v7's tightening made them drop verifiable tool names too, and sources fell 96% → 82% before the two-class rule recovered it.

## Limitations

- **Live search was unavailable in all nine rounds** — the mechanism these skills are built on is verify-then-speak, and every measurement ran with the verify step amputated. That is precisely why snapshot-sourced references kept scoring as unverifiable.
- One run per condition, with the variance documented above.
- Single-turn evaluation penalizes an interactive design; the judge is a language model applying a rubric, not a practicing roboticist.
- The author of the skills also designed the benchmark. Blind judging and a fixed rubric limit that conflict without eliminating it.

## Also retracted

An early iteration reported **100% vs 83.8%** for the skills. Its assertions rewarded the skills' own output format rather than answer quality. Recorded only so nobody re-quotes it.

## What would settle it

Live search enabled, three or more runs per condition so the variance above stops dominating, multi-turn scenarios where decision gates actually get answered, and a human robotics reviewer alongside the model judge.

## Reproducing

```sh
python3 scripts/make_bench_chart.py <workspace> [<workspace> ...]
python3 scripts/check_sources.py            # re-validate every snapshot source URL
```
