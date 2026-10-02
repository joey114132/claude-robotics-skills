#!/usr/bin/env python3
"""Chart per-grader pass rates, with and without the plugin, from `claude plugin eval --json` output.

    claude plugin eval . --no-publish --tag quality --allow-tools WebSearch WebFetch --json run.json
    python3 scripts/make_bench_chart.py run.json [run2.json ...] [--out assets/eval-quality.svg]

Each JSON file has cases[], and each case has arms.with[] and arms.without[] runs. Every run lists
graders[] {name, passed, scored}. Pass rate = passed runs / scored runs, pooled over all cases, runs
and files. Only the four quality graders are charted; `skill-fired` is an indicator, not a score.
A file with no `without` arm (--ablation none) charts the with arm alone.
`--self-check` runs a built-in test and exits.

Palette validated with the dataviz validator (categorical, 2 slots):
light  #D97757 / #5B8DEF  - all six checks PASS
dark   #CF6E4E / #5B8DEF  - all six checks PASS
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets" / "eval-quality.svg"

GRADERS = [
    ("trap", "Caught the trap / gave the expert call"),
    ("principle", "Explained the principle"),
    ("actionable", "Committed to a recommendation"),
    ("sourcing", "Sourced decaying figures"),
]
ARMS = ("with", "without")

# Chart geometry
W, ROW, PAD_T, PAD_B = 900, 62, 116, 66
TRACK_X = 262
TRACK_W = W - TRACK_X - 92
BAR_H, GAP = 20, 2


def load(files: list[Path]) -> tuple[dict, int, dict]:
    """Return (counts, n_cases, runs_per_arm); counts[arm][grader] = [passed, scored]."""
    counts = {arm: {k: [0, 0] for k, _ in GRADERS} for arm in ARMS}
    runs = {arm: 0 for arm in ARMS}
    n = 0
    for f in files:
        for case in json.loads(f.read_text())["cases"]:
            n += 1
            for arm in ARMS:
                for run in case.get("arms", {}).get(arm, []):
                    runs[arm] += 1
                    for g in run.get("graders", []):
                        if g["name"] in counts[arm] and g.get("scored", True):
                            counts[arm][g["name"]][0] += bool(g["passed"])
                            counts[arm][g["name"]][1] += 1
    if not any(c[1] for arm in ARMS for c in counts[arm].values()):
        sys.exit(f"no scored {'/'.join(k for k, _ in GRADERS)} graders in {[str(f) for f in files]}")
    return counts, n, runs


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rate(counts: dict, arm: str, key: str) -> float | None:
    passed, scored = counts[arm][key]
    return passed / scored * 100 if scored else None


def build(counts: dict, n: int, runs: dict) -> str:
    H = PAD_T + len(GRADERS) * ROW + PAD_B
    F = "ui-sans-serif,-apple-system,Segoe UI,Inter,Helvetica,Arial,sans-serif"
    arms = [a for a in ARMS if runs[a]]  # draw only arms that have runs
    series = {"with": ("s1", "With skill"), "without": ("s2", "Baseline")}

    def overall(arm: str) -> float:
        passed = sum(c[0] for c in counts[arm].values())
        scored = sum(c[1] for c in counts[arm].values())
        return passed / scored * 100 if scored else 0.0

    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="Grouped bar chart: pass rate of skill-guided answers versus baseline on '
        f'{len(GRADERS)} graders, {n} robotics cases">'
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
    per_arm = " / ".join(f"{runs[a]} {series[a][1].lower()}" for a in arms)
    p.append(
        f'<text class="h2" x="40" y="70" font-size="13">{n} cases. '
        f"Each reply graded pass or fail by an LLM judge on four checks ({esc(per_arm)} runs).</text>"
    )

    # Legend, always present
    lx = 46
    for a in arms:
        cls, name = series[a]
        p.append(f'<circle class="{cls}" cx="{lx}" cy="92" r="5.5"/>')
        p.append(f'<text class="lab" x="{lx + 12}" y="97" font-size="13" font-weight="600">{name}</text>')
        p.append(f'<text class="val" x="{lx + 12 + 8 * len(name)}" y="97" font-size="13">{overall(a):.0f}% overall</text>')
        lx += 192

    for frac in (0, 0.25, 0.5, 0.75, 1.0):
        x = TRACK_X + TRACK_W * frac
        p.append(f'<line class="grid" x1="{x:.1f}" y1="{PAD_T - 16}" x2="{x:.1f}" y2="{PAD_T + len(GRADERS) * ROW - 18}" stroke-width="1"/>')
        p.append(f'<text class="ax" x="{x:.1f}" y="{PAD_T + len(GRADERS) * ROW + 2}" font-size="11" text-anchor="middle">{int(frac * 100)}%</text>')

    for i, (key, label) in enumerate(GRADERS):
        y = PAD_T + i * ROW
        p.append(f'<text class="lab" x="{TRACK_X - 16}" y="{y + 20}" font-size="13.5" font-weight="600" text-anchor="end">{esc(label)}</text>')
        for j, a in enumerate(arms):
            pct = rate(counts, a, key)
            if pct is None:
                continue
            w = max(TRACK_W * pct / 100, 2)
            by = y + j * (BAR_H + GAP)
            # square at the baseline, 4px rounded data-end
            p.append(f'<path class="{series[a][0]}" d="M{TRACK_X} {by} h{w - 4:.1f} a4 4 0 0 1 4 4 v{BAR_H - 8} a4 4 0 0 1 -4 4 h-{w - 4:.1f} z"/>')
            p.append(f'<text class="val" x="{TRACK_X + w + 10:.1f}" y="{by + 14}" font-size="12.5" font-weight="600">{pct:.0f}%</text>')

    p.append(f'<text class="ax" x="40" y="{H - 24}" font-size="11.5">Pass rate = passed runs / scored runs, pooled over all cases. The skill-fired check is an indicator and is not charted.</text>')
    p.append("</g></svg>")
    return "\n".join(p)


def main() -> int:
    ap = argparse.ArgumentParser(description="Chart per-grader pass rates from `claude plugin eval --json` files.")
    ap.add_argument("files", nargs="*", type=Path, help="JSON files written by `claude plugin eval --json <path>`")
    ap.add_argument("--self-check", action="store_true", help="run the built-in test and exit")
    ap.add_argument("--out", type=Path, default=OUT, help=f"SVG to write (default: {OUT.relative_to(REPO)})")
    ns = ap.parse_args()
    if ns.self_check:
        _self_check()
        return 0
    if not ns.files:
        ap.error("give at least one JSON file")

    counts, n, runs = load(ns.files)
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(build(counts, n, runs))

    print(f"{n} cases, runs per arm: {runs}\n")
    print(f"{'grader':32} {'with':>7} {'without':>8}")
    for key, label in GRADERS:
        cells = [rate(counts, a, key) for a in ARMS]
        print(f"{label:32} " + " ".join(f"{c:7.0f}%" if c is not None else f"{'-':>8}" for c in cells))
    print(f"\nwrote {ns.out}")
    return 0


def _self_check() -> None:
    def run(*results: bool) -> dict:
        return {"graders": [{"name": k, "passed": r, "scored": True} for (k, _), r in zip(GRADERS, results)]
                + [{"name": "skill-fired", "passed": True, "scored": True, "withOnly": True}]}

    doc = {"cases": [{"name": "c", "arms": {"with": [run(True, True, True, True)] * 2, "without": [run(True, False, True, False)] * 2}}]}
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "r.json"
        f.write_text(json.dumps(doc))
        counts, n, runs = load([f])
    assert n == 1 and runs == {"with": 2, "without": 2}
    assert rate(counts, "with", "trap") == 100 and rate(counts, "without", "principle") == 0
    assert "skill-fired" not in counts["with"], "indicator grader is not charted"
    svg = build(counts, n, runs)
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert svg.count("<path") == len(GRADERS) * 2, "one bar path per arm per grader"
    assert "prefers-color-scheme: dark" in svg, "dark mode present"
    single = build(counts, n, {"with": 2, "without": 0})
    assert single.count("<path") == len(GRADERS), "a with-only file draws one series"
    print("self-check OK")


if __name__ == "__main__":
    sys.exit(main())
