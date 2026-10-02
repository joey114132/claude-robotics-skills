#!/usr/bin/env python3
"""Check that every landscape.md entry carries a source and that its URL still resolves.

Run from the repo root:
    python3 scripts/check_sources.py              # check every skill
    python3 scripts/check_sources.py robot-arm    # check one skill
    python3 scripts/check_sources.py --offline    # format checks only, no network
    python3 scripts/check_sources.py --self-check # test the parser, no files read

Exit code is non-zero when an entry has no source URL, a URL is dead, or a
snapshot is older than 180 days, so this works as a pre-commit or CI gate.

Status handling:
  - 404, 410 and DNS failures are DEAD and fail the run.
  - 403 and 429 are anti-bot refusals. They are listed as "blocked" and do not fail the run.
  - A 5xx answer, a timeout, or a refused/reset connection or TLS failure is often transient (asam.net and docs.ros.org each returned
    500 once and 200 seconds later), so the probe waits about 3 seconds and retries once.
    If the retry succeeds the URL is fine. If it still fails, the URL is listed as
    "server error, check by hand" and does not fail the run.
Unknown flags print usage and exit 2. Standard library only, no install step.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ENTRY = re.compile(r"^- \*\*")
URL = re.compile(r"https?://[^\s<>()\[\]]+")
VERIFIED = re.compile(r"\*\*Verified:[^\n]*?\*\*")  # the whole header, partial dates included
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
STALE_DAYS = 180
TIMEOUT = 15
BOT_BLOCKED = {403, 429}  # publisher/CDN refusing automated clients, not a dead page
RETRY_WAIT = 3  # seconds to wait before the one retry of a 5xx or timeout
UA = "claude-robotics-skills-linkcheck/1.0 (+https://github.com/joey114132/claude-robotics-skills)"


def _cause(e: Exception) -> Exception:
    """urllib wraps connect failures in URLError; the real error is in .reason."""
    r = getattr(e, "reason", None)
    return r if isinstance(r, Exception) else e


def _classify(e: Exception) -> str:
    """Name a transport failure. Only DNS failure is proof the host is gone."""
    c = _cause(e)
    if isinstance(c, TimeoutError):
        return "timeout"
    if isinstance(c, (ConnectionError, ssl.SSLError)):  # refused, reset, aborted, TLS handshake
        return "conn_error"
    return type(c).__name__  # includes socket.gaierror, which stays DEAD


def _transient(status: int | str) -> bool:
    return status in ("timeout", "conn_error") or (isinstance(status, int) and 500 <= status < 600)


def probe(url: str) -> tuple[str, int | str]:
    """Return (url, status). A 5xx or timeout is retried once after RETRY_WAIT seconds."""
    status = _probe_once(url)[1]
    if _transient(status):
        time.sleep(RETRY_WAIT)
        status = _probe_once(url)[1]
    return url, status


def _probe_once(url: str) -> tuple[str, int | str]:
    """HEAD first, fall back to GET if the host rejects HEAD. A timeout is final: GET would only stall again."""
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
            status = _classify(e)
            if method == "HEAD" and status not in ("timeout", "conn_error"):
                continue
            return url, status
    return url, "unreachable"


def check(paths: list[Path], offline: bool) -> int:
    problems = 0
    urls: dict[str, list[str]] = {}

    for path in paths:
        skill = path.parts[-3]
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()

        m = VERIFIED.search(text)
        if not m or not DATE.search(m.group(0)):
            print(f"[{skill}] MISSING '**Verified: YYYY-MM-DD**' header")
            problems += 1
        else:
            # "2026-10-02 (changed entries; rest 2026-08-05)": the oldest date is the real age
            oldest = min(DATE.findall(m.group(0)))
            try:
                age = (date.today() - datetime.strptime(oldest, "%Y-%m-%d").date()).days
            except ValueError:  # the regex matches digit shape only, so 2026-13-45 gets here
                print(f"[{skill}] INVALID date in Verified header: {oldest}")
                problems += 1
            else:
                flag = ""
                if age > STALE_DAYS:
                    flag = "  <-- STALE, re-run robotics-radar"
                    problems += 1
                print(f"[{skill}] verified {oldest} ({age}d ago){flag}")

        entries = [ln for ln in lines if ENTRY.match(ln)]
        if not entries:
            print(f"[{skill}] no entries found")
            problems += 1

        for ln in entries:
            name = ln[4:].split("**")[0]
            if not URL.search(ln):  # a bare "arXiv:NNNN" or "Source:" with no link is not a source
                print(f"[{skill}] UNSOURCED: {name}")
                problems += 1
                continue
            for u in URL.findall(ln):
                urls.setdefault(u.rstrip(".,);"), []).append(f"{skill}/{name}")

    print(f"\n{len(urls)} unique URLs across {len(paths)} files")
    if offline:
        print("--offline: skipping network checks")
        return problems

    dead, blocked, server_err = [], [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        for i, (url, status) in enumerate(pool.map(probe, urls), 1):
            if isinstance(status, int) and status < 400:
                pass
            elif status in BOT_BLOCKED:
                # Anti-bot / rate-limit responses mean "we refuse robots", not
                # "this page is gone" — surface them but do not fail on them.
                blocked.append((url, status))
            elif _transient(status):
                # Still 5xx or timing out after the retry: the server may be down
                # for a while, but it is not proof the page is gone.
                server_err.append((url, status))
            else:
                dead.append((url, status))
            if sys.stdout.isatty():
                print(f"\r  checked {i}/{len(urls)}", end="", flush=True)
    if sys.stdout.isatty():
        print()

    for url, status in blocked:
        print(f"blocked [{status}, likely anti-bot — check by hand] {url}")
    for url, status in server_err:
        print(f"server error [{status}, still failing after one retry — check by hand] {url}")
    for url, status in dead:
        print(f"DEAD [{status}] {url}\n     cited by: {', '.join(urls[url])}")
    problems += len(dead)

    print(f"\n{'FAIL' if problems else 'OK'} — {problems} problem(s)")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Check that every landscape.md entry has a live source.")
    ap.add_argument("skills", nargs="*", help="skill names to check (default: all)")
    ap.add_argument("--offline", action="store_true", help="format checks only, no network")
    ap.add_argument("--self-check", action="store_true", help="run the built-in parser test and exit")
    ns = ap.parse_args()
    if ns.self_check:
        _self_check()
        return 0
    args, offline = ns.skills, ns.offline

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
    assert DATE.findall(VERIFIED.search("**Verified: 2026-08-05.** blah").group(0)) == ["2026-08-05"]
    partial = VERIFIED.search("**Verified: 2026-10-02 (changed entries; rest 2026-08-05).** blah")
    assert min(DATE.findall(partial.group(0))) == "2026-08-05"
    assert VERIFIED.search("no header here") is None
    print("self-check OK")


if __name__ == "__main__":
    sys.exit(main())
