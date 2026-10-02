# claude-robotics-skills

Collection of Claude Code robotics skills. No application code: markdown skill definitions plus small maintenance scripts (`scripts/check_sources.py`, `scripts/make_bench_chart.py`, and one skill-local audit script, `skills/ros2-master/scripts/qos_audit.py`, an allowed exception).

## Layout

- `.claude-plugin/marketplace.json` + `plugin.json` — plugin manifests (`/plugin marketplace add joey114132/claude-robotics-skills`)
- `skills/<name>/SKILL.md` — skill body (frontmatter: name, description, allowed-tools)
- `skills/<name>/references/landscape.md` — dated, source-verified snapshot of that domain's tooling and research
- `skills/robotics-radar/` — the maintenance sweep that refreshes the other skills
- `scripts/check_sources.py` — link and format checker; stdlib only, non-zero exit on failure (`test_check_sources.py` tests it)
- `scripts/make_bench_chart.py` — charts per-grader pass rates from `claude plugin eval --json` files into an SVG
- `evals/` — the `claude plugin eval` suite (14 `quality` cases, 30 `routing` cases); `evals/results/` is gitignored
- `EVAL.md` — benchmark history and how to run the suite; `intent.md` and `intent/` — why the repo exists and its backlog
- `assets/*.svg` — README graphics, theme-aware (light/dark via `prefers-color-scheme`)
- On this machine the skills are symlinked into `~/.claude/skills` (no duplicate plugin install needed)

## Skill structure (every skill follows this)

1. Title paragraph naming the role to act as, plus explicit division of labor with sibling skills.
2. `## How to answer` — the shared delivery rules (verdict first, one pass, pause only when you can ask, two-class citation rule, machinery invisible, `/loop` means fast-forward). Copy it verbatim from a sibling skill. It was tuned over nine blind rounds (`EVAL.md`), so change its wording only with a measured eval. `robotics-advisor` carries its own variant.
3. Optional "What makes X different" — the load-bearing fundamentals, plain language first, term second.
4. `## The X decision sequence` — 5-7 decisions in dependency order, each with its boring default and what makes you deviate. First decision is an honest scoping question. It is an internal completeness checklist, not the reply's outline. (Some skills title it "The X pipeline" or "The loop".)
5. `## Modern scan` — must contain the `**Live scan on every invocation.**` paragraph, copied from a sibling skill.
6. `## Gotchas` — 5+ real, expensive, domain-specific traps. Not generic advice. Highest-value section.

Keep SKILL.md under ~130 lines. The description must be a "Use when …" trigger with concrete nouns, not a summary. Declare `allowed-tools` with a hyphen: Claude Code silently ignores `allowed_tools`. The key pre-approves tools for the turn and does not restrict them, so list only read and search tools (Read, Grep, Glob, WebSearch, WebFetch) and never unscoped Write, Edit or Bash.

The Guided / Fast-forward / Audit "Loop modes" section exists only in `robotics-radar`. The other skills had it until `3bf0c2d` replaced it with `## How to answer`.

## Conventions

- **English only** — all repo content and commit messages (owner request, 2026-08-05).
- **Live search on every invocation** — skills never answer from static content alone. `landscape.md` is a starting point with a Verified date; each invocation re-verifies it. The skill writes a changed finding back into `landscape.md` (bumping the date) only when its directory is a git checkout the user maintains. A marketplace install lives in a plugin cache that the next update overwrites, so a write there is lost.
- **Every landscape entry needs a live source** — a `Source: <url>` (an `arxiv.org/abs/` link for papers), verified at write time. A bare `arXiv:` ID does not count. Never from memory. Include Chinese-language / China-market queries; a large share of new hardware ships there first. When you change entries, rewrite the Verified line as `**Verified: <today> (changed entries; rest <previous date>).**` and keep any earlier partial dates. The checker uses the oldest date for its 180-day staleness rule.
- **Verify with adversarial agents** — when a research agent writes a landscape, a second agent should try to disprove it and delete what it can't confirm. Authors over-claim.
- Run `python3 scripts/check_sources.py` before committing landscape changes. It fails on an entry without a source URL, a dead URL, or a snapshot older than 180 days. 403/429 are anti-bot responses, not dead links, and the script reports them separately. `--offline` checks format only.

## Evals

Run from the repo root. `--no-publish` keeps the HTML report local. Results go to `evals/results/`, which is gitignored.

```bash
# Routing cases: does the intended skill fire? One arm, no baseline.
claude plugin eval . --no-publish --tag routing --ablation none --runs 2

# Quality cases: with and without the plugin. The extra grant gives the skills their live search.
claude plugin eval . --no-publish --tag quality --allow-tools WebSearch WebFetch --model <id> --json quality.json
python3 scripts/make_bench_chart.py quality.json
```

Re-run the routing cases after any description change. Descriptions are routing triggers, so edit them only to fix a factual or portability error.

## Versioning

`plugin.json` pins `version`, and Claude Code keeps every installed user on the cached copy until that string changes. Bump it on every content change (minor for new skills or structure changes, patch for refreshes), or the change never ships. After the bump commit, tag it with `claude plugin tag`.
