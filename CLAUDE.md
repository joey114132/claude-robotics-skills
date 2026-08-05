# claude-robotics-skills

Claude Code robotics skill 모음 repo. 코드 없음 — markdown skill 정의만 있다.

## Layout

- `skills/<name>/SKILL.md` — skill 본체 (frontmatter: name, description, allowed_tools)
- `skills/robotics-advisor/references/craig3-map.md` — Craig 3rd ed. PDF page map (pdf = book + 8)
- 설치는 README 참조 (`~/.claude/skills`로 symlink; 로컬에서는 이미 연결돼 있음)

## Conventions

- Description은 반드시 "Use when …" trigger 형식, `allowed_tools` 명시, `## Gotchas` 3개 이상, SKILL.md는 ~120줄 이하.
- 네 skill은 같은 choose-and-loop 패턴(fundamentals → verified modern options → AskUserQuestion → decision stack)을 공유한다. 새 skill을 추가하면 이 패턴과 상호 cross-reference를 유지할 것.
- Craig PDF는 저작권 문제로 절대 repo에 넣지 않는다 (page map 같은 사실 metadata만 허용).
- Commit message는 한국어.
