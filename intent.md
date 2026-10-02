# claude-robotics-skills — intent

If `CLAUDE.md` is "how this is run," this file is "why this repo exists." Individual units of work accumulate one at a time in [intent/](intent/README.md) (currently one draft entry).

## Why this exists

An AI answering robotics questions from memory alone fails two ways: it recommends an archived repo as if it were current, or it skips the textbook method (classic IK, say) and reaches straight for a flashy, unverified library (`README.md` "The problem"). This repo takes a single answer loop — ground the classic method first, then layer on current options a live search just confirmed — and hardens it by applying it across 18 robot-domain skills. Without it, every question falls back to the base model's unaided answer and both failures come back.

## Success & failure

- **Sources & freshness.** `scripts/check_sources.py` exits 0. The `**Verified:**` date at the top of each file stays within 180 days (`scripts/check_sources.py:27`, `STALE_DAYS`). The checker fails on a snapshot older than 180 days, judged by the oldest date in the Verified line (`rest 2026-08-05` counts, not the newest partial date). A full run with network calls on 2026-10-02 found 8 dead and 12 bot-blocked URLs. The dead ones are fixed in the skill files, and the bot-blocked ones (403/429) are reported but do not fail the run. The `--offline` run on the same day found 17 landscape.md files (`robotics-radar` has none) and about 600 URLs, with no format issues.
- **Benchmark.** `EVAL.md`: latest of 9 rounds (v9) scored skill 93% vs baseline 93% (14 questions, blind judge).
  Success means parity or better while holding a 100% vs 79% citation rate. Fabrication at 71% vs 100% remains an unresolved weakness.
  Those nine rounds cannot be re-run from this repository. The current suite is `evals/` (`claude plugin eval`): 14 `quality` cases graded on trap, principle, actionable and sourcing, and 30 `routing` cases.
  Routing baseline on 2026-10-02: 30 of 30 cases and 60 of 60 runs routed to the intended skill, so descriptions are not rewritten for routing.
  Quality runs are recorded in `EVAL.md` and charted with `scripts/make_bench_chart.py`. On 2026-10-02 the same 14 cases were run on Opus 5.5 and on Sonnet 5.5 (one run per case and arm). With skill vs baseline: trap 14/14 vs 14/14 on both, sourcing 9/14 vs 9/14 on Opus 5.5 and 7/14 vs 9/14 on Sonnet 5.5, and the skill fired in 9 of 14 runs on both. The baseline sits at the ceiling on these cases, so they cannot yet show a gain.
- **Format.** `SKILL.md` stays under 130 lines (`CLAUDE.md`). Measured 2026-10-02: the max is 104 lines (`robotics-advisor`), and all 18 pass.
- Failure signals: a dead link, a snapshot left unverified past 180 days, a spec number with no source behind it.

## Out of scope

- No application code — `CLAUDE.md`: "No application code: markdown skill definitions plus small maintenance scripts." (`skills/ros2-master/scripts/qos_audit.py` is an allowed skill-local exception, see "Decisions and why.")
- No Korean commits or content — English-only (owner request, 2026-08-05, `CLAUDE.md`). This took effect at `v0.3.0` (`05b7e71`); only 5 earlier commits are in Korean.
- An answer given without a live search is never normal operation — that's the exact failure this repo exists to prevent (`README.md` "Why you'd trust it").

## Invariants

- **Every landscape entry has a source URL.** An entry without any URL is flagged UNSOURCED by `scripts/check_sources.py`, and a bare `arXiv:` ID does not count. Papers cite an `arxiv.org/abs/` link. Basis: `CLAUDE.md` "Every landscape entry needs a live source," and v0.6.1, which fixed 98 entries that carried paper IDs with no link (`EVAL.md`).
- **Every domain SKILL.md follows the house structure.** Title/division of labor → How to answer → (optional) fundamentals → decision sequence → Modern scan (must include "Live scan on every invocation.") → 5+ Gotchas. Measured 2026-10-02: 17 of 18 start with How to answer and all 18 have 5+ Gotchas. The exception is `skills/robotics-radar/SKILL.md`, which keeps the only "Loop modes" section. "Loop modes" was removed from the other 17 in `3bf0c2d`. Basis: `3bf0c2d` and the real `skills/robot-arm/SKILL.md`; `CLAUDE.md` "Skill structure" carries the same list.
- **No landscape update is trusted without adversarial verification.** `robotics-radar` stage 3 — a separate agent tries to disprove the authoring agent's findings. Basis: `skills/robotics-radar/SKILL.md` "Verify adversarially."
- **`.wiki/` is never committed** (`.gitignore:1`). Opened it and found a scaffold — section headers only, no content — so a project decision written there is invisible to the next person.

## Decisions and why

- **Fixed structure, not wording.** Three rounds of added rules barely moved the score; one structural change — flipping the decision sequence from "table of contents for the answer" to "completeness checklist" (`v0.5.0`, `3bf0c2d`) — took the scope score from 56% to 89–100% (`EVAL.md` "Structure beat wording"). To reverse: next time the answer format needs work, suspect the structure before adding more wording.
- **Chose not to force the fabrication score (71%) up.** Four attempts (69→75→79→75→71%) each cost some other metric, like the citation rate. Rejected "add stronger verification wording" and settled instead for a rule splitting two categories — checkable identifiers vs. numbers that decay (`v0.6.0`, `3a6a184`) (`EVAL.md` "Four targeted attempts never moved fabrication up").
- **Retracted a benchmark headline twice.** "100% vs 83.8%" (a measurement that rewarded the skills' own output format) and "8 wins vs 4" (noise that swings 4–8 from round to round) were both walked back for insufficient evidence; the repo now cites only the criterion-level number averaged over 14 cases (`EVAL.md` "Read this before any tally," "Also retracted"). To reverse: check how many rounds a criterion average has held its direction, not one round's win count.
- **Allowed a skill-specific script as an exception.** `ros2-master` added a domain static-analysis script (`skills/ros2-master/scripts/qos_audit.py`, `9b17997`) inside its skill folder, on the strength of a measured finding: ast-based static analysis caught a QoS mismatch a 156K-token agent audit had missed. Judged not to conflict with "no application code," since it verifies a fact before the answer instead of standing in for the answer.
- **Pin the plugin version and bump it on every content change.** Claude Code keeps an installed plugin on its cached copy until the manifest's `version` string changes (docs: code.claude.com/docs/en/plugins/loading, checked 2026-10-02). `plugin.json` stayed at 0.4.0/0.4.1 while v0.4.2 to v0.6.1 shipped, so nobody who installed earlier received that work. It is now 0.7.0. Dropping the field would make every commit SHA a version, but the owner chose an explicit pin.
- **Rewriting a snapshot in place is for maintained checkouts only.** A marketplace install lives in a versioned cache that the next update overwrites, so a write-back there is lost and never reaches the repo. Skills write findings back only when the skill directory is a git checkout the user maintains. Durable refreshes come from `robotics-radar` run in a checkout.
- **Do not rewrite descriptions for routing.** Measured on the descriptions as they stood on 2026-10-02: 30 of 30 cases and 60 of 60 runs routed correctly, including 12 sibling-collision prompts. A description changes only to fix a factual or portability error. To reverse: re-run the routing cases (`EVAL.md`) and find a miss first.
- **Stale snapshots fail the check.** The 180-day rule was only a printed flag, so intent.md's own failure signal never turned the run red. `scripts/check_sources.py` now counts a stale snapshot as a problem.

## Open questions

- **The marketplace copy still lags until the 0.7.0 commit is pushed.** Checked 2026-10-02: `origin/main` has `plugin.json` at 0.4.0 and the repository has no tags or releases. Anyone who installed at 0.4.0 or 0.4.1 stays on that copy until a push carries the 0.7.0 pin. To close it: push, run `claude plugin tag`, then install from the marketplace and diff the cached copy against this checkout.
- **Can the quality cases show a gain at all?** Not yet. The first runs (2026-10-02, `EVAL.md`) put the baseline at 14/14 on trap and actionable and at 13 or 14 of 14 on principle, on both models. Next: harder traps that depend on facts newer than the training data, at least 3 runs per arm, and a look at why the skill fires in only 9 of 14 runs.
- **Mobile manipulation has no owning skill.** `intent/0001-mobile-manipulation.md` holds the case and what must be verified before a skill is written.
- **Does commercial warehouse picking and palletizing need its own skill?** The evidence is vendor pages only, with no open-source ecosystem. The lighter option is one gotcha in `skills/robot-hand/SKILL.md` and one boundary line in `skills/robot-fleet/SKILL.md`. Decide after a measured miss, not before.
