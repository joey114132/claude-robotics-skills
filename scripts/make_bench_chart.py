#!/usr/bin/env python3
"""Aggregate blind-judged benchmark grades into assets/benchmark.svg.

    python3 scripts/make_bench_chart.py <workspace-dir>

The workspace holds one directory per case containing grade.json, whose
answer_one/answer_two blocks each name the file they scored — that filename is
what maps a blindly-judged answer back to its condition.

Palette validated with the dataviz validator (categorical, 2 slots):
light  #D97757 / #5B8DEF  — all six checks PASS
dark   #CF6E4E / #5B8DEF  — all six checks PASS
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets" / "benchmark.svg"

CRITERIA = [
    ("trap_caught", "Caught the expert trap"),
    ("fundamentals", "Explained the principle"),
    ("sources", "Cited verifiable sources"),
    ("real_options", "Gave real options"),
    ("no_fabrication", "No fabricated claims"),
    ("scope", "Answered what was asked"),
]
MAX_PER_CASE = 2

# Chart geometry
W, ROW, PAD_T, PAD_B = 900, 62, 116, 66
TRACK_X = 262
TRACK_W = W - TRACK_X - 92
BAR_H, GAP = 20, 2


def load(ws: Path) -> tuple[dict, dict, int]:
    """Return (skill_totals, base_totals, n_cases)."""
    skill = {k: 0 for k, _ in CRITERIA}
    base = {k: 0 for k, _ in CRITERIA}
    n = 0
    for gf in sorted(ws.glob("*/grade.json")):
        g = json.loads(gf.read_text())
        n += 1
        for block in ("answer_one", "answer_two"):
            a = g[block]
            target = skill if "with_skill" in a["file"] else base
            for key, _ in CRITERIA:
                target[key] += int(a.get(key, 0))
    if not n:
        sys.exit(f"no grade.json found under {ws}")
    return skill, base, n


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(skill: dict, base: dict, n: int) -> str:
    top = n * MAX_PER_CASE
    H = PAD_T + len(CRITERIA) * ROW + PAD_B
    F = "ui-sans-serif,-apple-system,Segoe UI,Inter,Helvetica,Arial,sans-serif"

    s_total = sum(skill.values()) / (top * len(CRITERIA)) * 100
    b_total = sum(base.values()) / (top * len(CRITERIA)) * 100

    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="Grouped bar chart: skill-guided answers versus baseline across six '
        f'expert-quality criteria, {n} blind-judged robotics cases">'
    )
    p.append(f"""<style>
    .surface {{ fill: #FAF9F7; }}
    .h1   {{ fill: #1A1A1A; }}
    .h2   {{ fill: #6B645C; }}
    .lab  {{ fill: #3D3934; }}
    .val  {{ fill: #6B645C; }}
    .ax   {{ fill: #A79E95; }}
    .grid {{ stroke: #E6E1DB; }}
    .s1   {{ fill: #D97757; }}
    .s2   {{ fill: #5B8DEF; }}
    @media (prefers-color-scheme: dark) {{
      .surface {{ fill: #16151A; }}
      .h1   {{ fill: #F5F3F0; }}
      .h2   {{ fill: #A9A29A; }}
      .lab  {{ fill: #D8D3CC; }}
      .val  {{ fill: #A9A29A; }}
      .ax   {{ fill: #6E675F; }}
      .grid {{ stroke: #322F3A; }}
      .s1   {{ fill: #CF6E4E; }}
    }}
  </style>""")
    p.append(f'<rect class="surface" width="{W}" height="{H}" rx="16"/>')
    p.append(f'<g font-family="{F}">')

    p.append('<text class="h1" x="40" y="46" font-size="19" font-weight="700">Does the skill actually make the answer more expert?</text>')
    p.append(
        f'<text class="h2" x="40" y="70" font-size="13">{n} robotics questions, each with one planted trap a novice misses. '
        f"Both answers scored blind by an independent judge, 0–2 per case.</text>"
    )

    # Legend — always present for two or more series
    p.append('<circle class="s1" cx="46" cy="92" r="5.5"/>')
    p.append('<text class="lab" x="58" y="97" font-size="13" font-weight="600">With skill</text>')
    p.append(f'<text class="val" x="132" y="97" font-size="13">{s_total:.0f}% overall</text>')
    p.append('<circle class="s2" cx="238" cy="92" r="5.5"/>')
    p.append('<text class="lab" x="250" y="97" font-size="13" font-weight="600">Baseline</text>')
    p.append(f'<text class="val" x="318" y="97" font-size="13">{b_total:.0f}% overall</text>')

    for frac in (0, 0.25, 0.5, 0.75, 1.0):
        x = TRACK_X + TRACK_W * frac
        p.append(f'<line class="grid" x1="{x:.1f}" y1="{PAD_T - 16}" x2="{x:.1f}" y2="{PAD_T + len(CRITERIA) * ROW - 18}" stroke-width="1"/>')
        p.append(f'<text class="ax" x="{x:.1f}" y="{PAD_T + len(CRITERIA) * ROW + 2}" font-size="11" text-anchor="middle">{int(frac * 100)}%</text>')

    for i, (key, label) in enumerate(CRITERIA):
        y = PAD_T + i * ROW
        p.append(f'<text class="lab" x="{TRACK_X - 16}" y="{y + 20}" font-size="13.5" font-weight="600" text-anchor="end">{esc(label)}</text>')
        for j, (data, cls) in enumerate(((skill, "s1"), (base, "s2"))):
            pct = data[key] / top * 100
            w = max(TRACK_W * pct / 100, 2)
            by = y + j * (BAR_H + GAP)
            # square at the baseline, 4px rounded data-end
            p.append(f'<path class="{cls}" d="M{TRACK_X} {by} h{w - 4:.1f} a4 4 0 0 1 4 4 v{BAR_H - 8} a4 4 0 0 1 -4 4 h-{w - 4:.1f} z"/>')
            p.append(f'<text class="val" x="{TRACK_X + w + 10:.1f}" y="{by + 14}" font-size="12.5" font-weight="600">{pct:.0f}%</text>')

    p.append(f'<text class="ax" x="40" y="{H - 24}" font-size="11.5">Score = share of the maximum across all {n} cases. Judge saw both answers unlabeled, with presentation order alternated.</text>')
    p.append("</g></svg>")
    return "\n".join(p)


def main() -> int:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ws = Path(sys.argv[1])
    skill, base, n = load(ws)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(build(skill, base, n))

    top = n * MAX_PER_CASE
    print(f"{n} cases graded\n")
    print(f"{'criterion':28} {'skill':>8} {'baseline':>9}")
    for key, label in CRITERIA:
        print(f"{label:28} {skill[key] / top * 100:7.0f}% {base[key] / top * 100:8.0f}%")
    print(f"\nwrote {OUT.relative_to(REPO)}")
    return 0


def _self_check() -> None:
    skill = {k: 16 for k, _ in CRITERIA}
    base = {k: 8 for k, _ in CRITERIA}
    svg = build(skill, base, 8)
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert svg.count("<path") == len(CRITERIA) * 2, "one bar path per series per criterion"
    assert "100%" in svg and "50%" in svg, "value labels rendered from the data"
    assert "prefers-color-scheme: dark" in svg, "dark mode present"
    print("self-check OK")


if __name__ == "__main__":
    if "--self-check" in sys.argv:
        _self_check()
    else:
        sys.exit(main())
