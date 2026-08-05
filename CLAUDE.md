# claude-robotics-skills

Collection of Claude Code robotics skills. No application code — markdown skill definitions plus one maintenance script.

## Layout

- `.claude-plugin/marketplace.json` + `plugin.json` — plugin manifests (`/plugin marketplace add joey114132/claude-robotics-skills`)
- `skills/<name>/SKILL.md` — skill body (frontmatter: name, description, allowed_tools)
- `skills/<name>/references/landscape.md` — dated, source-verified snapshot of that domain's tooling and research
- `skills/robotics-radar/` — the maintenance sweep that refreshes the other skills
- `scripts/check_sources.py` — link/format checker; stdlib only, non-zero exit on failure
- `assets/*.svg` — README graphics, theme-aware (light/dark via `prefers-color-scheme`)
- On this machine the skills are symlinked into `~/.claude/skills` (no duplicate plugin install needed)

## Skill structure (every skill follows this)

1. Title paragraph naming the role to act as, plus explicit division of labor with sibling skills.
2. Optional "What makes X different" — the load-bearing fundamentals, plain language first, term second.
3. "## The X decision sequence" — 5-7 decisions in dependency order, each with its boring default and what makes you deviate. First decision is an honest scoping question.
4. "## Loop modes" — Guided / Fast-forward / Audit, standard wording.
5. "## Modern scan" — must contain the `**Live scan on every invocation.**` paragraph.
6. "## Gotchas" — 5+ real, expensive, domain-specific traps. Not generic advice. Highest-value section.

Keep SKILL.md under ~130 lines. Description must be a "Use when …" trigger, not a summary. Declare `allowed_tools`.

## Conventions

- **English only** — all repo content and commit messages (owner request, 2026-08-05).
- **Live search on every invocation** — skills never answer from static content alone. `landscape.md` is a starting point with a Verified date; each invocation re-verifies and updates the file (bumping the date) when the field has moved.
- **Every landscape entry needs a live source** — a `Source: <url>` or an `arXiv:` ID, verified at write time. Never from memory. Include Chinese-language / China-market queries; a large share of new hardware ships there first.
- **Verify with adversarial agents** — when a research agent writes a landscape, a second agent should try to disprove it and delete what it can't confirm. Authors over-claim.
- Run `python3 scripts/check_sources.py` before committing landscape changes. 403/429 are anti-bot responses, not dead links — the script reports them separately.
- Bump `plugin.json` version whenever skill content changes (minor for new skills, patch for refreshes).
