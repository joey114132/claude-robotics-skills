#!/usr/bin/env python3
"""Every plugin agent must declare `tools`, and only robot-fix-builder may hold Write, Edit or Bash.

An agent with no `tools` line inherits everything, so a missing line fails the test too.
Run: python3 scripts/test_agent_tools.py
"""

import re
from pathlib import Path

AGENTS = sorted((Path(__file__).resolve().parent.parent / "agents").glob("*.md"))
WRITERS_ALLOWED = {"robot-fix-builder"}
FORBIDDEN = {"Write", "Edit", "NotebookEdit", "Bash"}


def tools_of(path: Path):
    m = re.search(r"^---\n(.*?)\n---", path.read_text(), re.S)
    line = re.search(r"^tools:\s*(.+)$", m.group(1), re.M) if m else None
    # strip argument lists so Bash(git:*) counts as Bash; split only on commas outside parentheses
    return None if line is None else {t.strip().split("(")[0] for t in re.split(r",(?![^(]*\))", line.group(1))}


def test_every_agent_declares_tools():
    assert AGENTS, "no agents found"
    missing = [p.name for p in AGENTS if tools_of(p) is None]
    assert not missing, f"agents with no tools line: {missing}"


def test_only_the_builder_can_write_or_run_shell():
    bad = {p.stem: sorted(tools_of(p) & FORBIDDEN) for p in AGENTS if p.stem not in WRITERS_ALLOWED and tools_of(p) & FORBIDDEN}
    assert not bad, f"read-only agents holding write or shell tools: {bad}"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("ok")
