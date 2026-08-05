#!/usr/bin/env python3
"""Check that every landscape.md entry carries a source and that its URL still resolves.

Run from the repo root:
    python3 scripts/check_sources.py              # check every skill
    python3 scripts/check_sources.py robot-arm    # check one skill
    python3 scripts/check_sources.py --offline    # format checks only, no network

Exit code is non-zero when any entry is unsourced or any URL is dead, so this
works as a pre-commit or CI gate. Standard library only — no install step.
"""

from __future__ import annotations

import concurrent.futures
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ENTRY = re.compile(r"^- \*\*")
URL = re.compile(r"https?://[^\s<>()\[\]]+")
VERIFIED = re.compile(r"\*\*Verified:\s*(\d{4}-\d{2}-\d{2})")
STALE_DAYS = 180
TIMEOUT = 15
BOT_BLOCKED = {403, 429}  # publisher/CDN refusing automated clients, not a dead page
UA = "claude-robotics-skills-linkcheck/1.0 (+https://github.com/joey114132/claude-robotics-skills)"


def probe(url: str) -> tuple[str, int | str]:
    """Return (url, status). HEAD first, fall back to GET — some hosts reject HEAD."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return url, resp.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue  # host dislikes HEAD; retry as GET
            return url, e.code
        except Exception as e:  # noqa: BLE001 — any transport failure is a finding
            if method == "HEAD":
                continue
            return url, type(e).__name__
    return url, "unreachable"


def check(paths: list[Path], offline: bool) -> int:
    problems = 0
    urls: dict[str, list[str]] = {}

    for path in paths:
        skill = path.parts[-3]
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        m = VERIFIED.search(text)
        if not m:
            print(f"[{skill}] MISSING '**Verified: YYYY-MM-DD**' header")
            problems += 1
        else:
            age = (date.today() - datetime.strptime(m.group(1), "%Y-%m-%d").date()).days
            flag = "  <-- STALE, re-run robotics-radar" if age > STALE_DAYS else ""
            print(f"[{skill}] verified {m.group(1)} ({age}d ago){flag}")

        entries = [ln for ln in lines if ENTRY.match(ln)]
        if not entries:
            print(f"[{skill}] no entries found")
            problems += 1

        for ln in entries:
            name = ln[4:].split("**")[0]
            if "Source:" not in ln and "arXiv:" not in ln:
                print(f"[{skill}] UNSOURCED: {name}")
                problems += 1
                continue
            for u in URL.findall(ln):
                urls.setdefault(u.rstrip(".,);"), []).append(f"{skill}/{name}")

    print(f"\n{len(urls)} unique URLs across {len(paths)} files")
    if offline:
        print("--offline: skipping network checks")
        return problems

    dead, blocked = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for i, (url, status) in enumerate(pool.map(probe, urls), 1):
            if isinstance(status, int) and status < 400:
                pass
            elif status in BOT_BLOCKED:
                # Anti-bot / rate-limit responses mean "we refuse robots", not
                # "this page is gone" — surface them but do not fail on them.
                blocked.append((url, status))
            else:
                dead.append((url, status))
            print(f"\r  checked {i}/{len(urls)}", end="", flush=True)
    print()

    for url, status in blocked:
        print(f"blocked [{status}, likely anti-bot — check by hand] {url}")
    for url, status in dead:
        print(f"DEAD [{status}] {url}\n     cited by: {', '.join(urls[url])}")
    problems += len(dead)

    print(f"\n{'FAIL' if problems else 'OK'} — {problems} problem(s)")
    return problems


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    offline = "--offline" in sys.argv

    paths = sorted(REPO.glob("skills/*/references/landscape.md"))
    if args:
        paths = [p for p in paths if p.parts[-3] in args]
        if not paths:
            print(f"no landscape.md for: {', '.join(args)}")
            return 1

    return 1 if check(paths, offline) else 0


def _self_check() -> None:
    """Smallest check that fails if the parsing logic breaks."""
    good = "- **Foo** — a thing. Status: maintained. Source: https://example.com/x"
    bad = "- **Bar** — a thing. Status: research."
    assert ENTRY.match(good) and ENTRY.match(bad)
    assert URL.findall(good) == ["https://example.com/x"]
    assert not URL.findall(bad)
    assert VERIFIED.search("**Verified: 2026-08-05.** blah").group(1) == "2026-08-05"
    assert VERIFIED.search("no header here") is None
    print("self-check OK")


if __name__ == "__main__":
    if "--self-check" in sys.argv:
        _self_check()
    else:
        sys.exit(main())
