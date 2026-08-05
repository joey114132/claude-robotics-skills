# claude-robotics-skills

Collection of Claude Code robotics skills. No code — markdown skill definitions only.

## Layout

- `.claude-plugin/marketplace.json` + `plugin.json` — Claude Code plugin manifests (distribution: `/plugin marketplace add joey114132/claude-robotics-skills`)
- `skills/<name>/SKILL.md` — skill body (frontmatter: name, description, allowed_tools)
- `skills/<name>/references/landscape.md` — dated, source-verified snapshot of that domain's current tooling/research
- `skills/robotics-advisor/references/craig3-map.md` — chapter/section page map for the fundamentals text
- On this local machine the skills are symlinked into `~/.claude/skills` (no duplicate plugin install needed)

## Conventions

- **English only** — all repo content and commit messages are English (owner request, 2026-08-05).
- Descriptions must be "Use when …" triggers; declare `allowed_tools`; include `## Gotchas` with 3+ items; keep SKILL.md around 120 lines or less.
- All skills share the choose-and-loop pattern (fundamentals → verified modern options → AskUserQuestion gate → decision stack). New skills must keep the pattern and cross-reference their siblings.
- **Live search on every invocation** — skills never answer from static content alone. `references/landscape.md` is a starting point with a Verified date; each invocation re-verifies live and updates the file (bumping the date) when the field has moved.
- Bump `plugin.json` version whenever skill content changes.
