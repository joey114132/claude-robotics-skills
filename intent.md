# claude-robotics-skills — intent

If `CLAUDE.md` is "how this is run," this file is "why this repo exists." Individual units of work accumulate one at a time in [intent/](intent/README.md) (currently just the backlog table, no entries yet).

## Why this exists

An AI answering robotics questions from memory alone fails two ways: it recommends an archived repo as if it were current, or it skips the textbook method (classic IK, say) and reaches straight for a flashy, unverified library (`README.md` "The problem"). This repo takes a single answer loop — ground the classic method first, then layer on current options a live search just confirmed — and hardens it by applying it across 18 robot-domain skills. Without it, every question falls back to the base model's unaided answer and both failures come back.

## Success & failure

- **Sources & freshness.** `scripts/check_sources.py` exits 0. The `**Verified:**` date at the top of each file stays within 180 days (`scripts/check_sources.py:27`, `STALE_DAYS`). A direct `--offline` run (format only) found 16 landscape.md files (of 18 skills, `robotics-advisor` and `robotics-radar` don't have one), 485 URLs, 0 format issues, all passing at 34 days since 2026-08-05 (checked 2026-09-08). The full run including network calls wasn't done this time — see "Open questions."
- **Benchmark.** `EVAL.md` — latest of 9 rounds (v9): skill 93% vs baseline 93% (14 questions, blind judge). The bar isn't "win," it's "parity or better while holding a 100% vs 79% citation rate"; fabrication at 71% vs 100% remains an unresolved weakness. Reproduce with `python3 scripts/make_bench_chart.py <workspace>...`.
- **Format.** `SKILL.md` stays under 130 lines (`CLAUDE.md`) — measured max is 100 lines (`robotics-advisor`), and all 18 pass.
- Failure signals: a dead link, a snapshot left unverified past 180 days, a spec number with no source behind it.

## Out of scope

- No application code — `CLAUDE.md`: "No application code — markdown skill definitions plus one maintenance script." (`skills/ros2-master/scripts/qos_audit.py` is a recent exception — see "Decisions and why.")
- No Korean commits or content — English-only (owner request, 2026-08-05, `CLAUDE.md`). This took effect at `v0.3.0` (`05b7e71`); only 5 earlier commits are in Korean.
- An answer given without a live search is never normal operation — that's the exact failure this repo exists to prevent (`README.md` "Why you'd trust it").

## Invariants

- **Every landscape entry has a source.** No `Source:` URL or `arXiv:` ID gets flagged UNSOURCED by `scripts/check_sources.py:77`. Basis: `CLAUDE.md` "Every landscape entry needs a live source."
- **Every SKILL.md follows the six-part structure.** Title/division of labor → (optional) fundamentals → decision sequence → Loop modes → Modern scan (must include "Live scan on every invocation.") → 5+ Gotchas. Basis: `CLAUDE.md` "Skill structure" section, cross-checked against the real `skills/robot-arm/SKILL.md`.
- **No landscape update is trusted without adversarial verification.** `robotics-radar` stage 3 — a separate agent tries to disprove the authoring agent's findings. Basis: `skills/robotics-radar/SKILL.md` "Verify adversarially."
- **`.wiki/` is never committed** (`.gitignore:1`). Opened it and found a scaffold — section headers only, no content — so a project decision written there is invisible to the next person.

## Decisions and why

- **Fixed structure, not wording.** Three rounds of added rules barely moved the score; one structural change — flipping the decision sequence from "table of contents for the answer" to "completeness checklist" (`v0.5.0`, `3bf0c2d`) — took the scope score from 56% to 89–100% (`EVAL.md` "Structure beat wording"). To reverse: next time the answer format needs work, suspect the structure before adding more wording.
- **Chose not to force the fabrication score (71%) up.** Four attempts (69→75→79→75→71%) each cost some other metric, like the citation rate. Rejected "add stronger verification wording" and settled instead for a rule splitting two categories — checkable identifiers vs. numbers that decay (`v0.6.0`, `3a6a184`) (`EVAL.md` "Four targeted attempts never moved fabrication up").
- **Retracted a benchmark headline twice.** "100% vs 83.8%" (a measurement that rewarded the skills' own output format) and "8 wins vs 4" (noise that swings 4–8 from round to round) were both walked back for insufficient evidence; the repo now cites only the criterion-level number averaged over 14 cases (`EVAL.md` "Read this before any tally," "Also retracted"). To reverse: check how many rounds a criterion average has held its direction, not one round's win count.
- **Allowed a skill-specific script as an exception.** `ros2-master` added a domain static-analysis script (`skills/ros2-master/scripts/qos_audit.py`, `9b17997`) inside its skill folder, on the strength of a measured finding: ast-based static analysis caught a QoS mismatch a 156K-token agent audit had missed. Judged not to conflict with "no application code," since it verifies a fact before the answer instead of standing in for the answer.

## Open questions

- **`plugin.json`'s version lags the commit log.** Commit messages climb from v0.4.0 to v0.6.1 within a single day (2026-08-05), but the value in `.claude-plugin/plugin.json` stalled at 0.4.0 that day and ticked up only one step, to 0.4.1, a month later (2026-09-03, `9b17997`). Whether that's deliberate decoupling or a missed bump is unclear — ask the repo owner directly, or diff the full `git log -p -- .claude-plugin/plugin.json` against each version-bump commit.
- **The link check wasn't run with network calls this time.** Whether all 485 URLs are actually live right now isn't known from the `--offline` (format-only) result. Run `python3 scripts/check_sources.py` to find out (up to 15s × 2 timeouts per URL, so a full run can take several minutes).
- **Whether this checkout matches what's deployed on the marketplace hasn't been checked.** Diff it against the installed copy after a `/plugin marketplace` refresh, or check GitHub releases/tags.
