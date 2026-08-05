# claude-robotics-skills

Claude Code robotics skill 모음 repo. 코드 없음 — markdown skill 정의만 있다.

## Layout

- `.claude-plugin/marketplace.json` + `plugin.json` — Claude Code plugin manifest (배포 경로: `/plugin marketplace add joey114132/claude-robotics-skills`)
- `skills/<name>/SKILL.md` — skill 본체 (frontmatter: name, description, allowed_tools)
- `skills/robotics-advisor/references/craig3-map.md` — Craig 3rd ed. PDF page map (pdf = book + 8)
- 이 로컬 머신에서는 `~/.claude/skills`로 symlink 연결돼 있음 (plugin 중복 설치 불필요)
- Skill 내용이 바뀌면 `plugin.json`의 `version`을 함께 올릴 것

## Conventions

- Description은 반드시 "Use when …" trigger 형식, `allowed_tools` 명시, `## Gotchas` 3개 이상, SKILL.md는 ~120줄 이하.
- 네 skill은 같은 choose-and-loop 패턴(fundamentals → verified modern options → AskUserQuestion → decision stack)을 공유한다. 새 skill을 추가하면 이 패턴과 상호 cross-reference를 유지할 것.
- Craig PDF는 저작권 문제로 절대 repo에 넣지 않는다 (page map 같은 사실 metadata만 허용).
- Commit message는 한국어.
