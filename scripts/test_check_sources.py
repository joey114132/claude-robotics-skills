#!/usr/bin/env python3
"""Minimal tests for check_sources.py: argument handling and source/stale judgments.

Run: python3 scripts/test_check_sources.py
"""

import contextlib
import io
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "check_sources.py"
sys.path.insert(0, str(SCRIPT.parent))
import check_sources as cs  # noqa: E402


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def test_unknown_flag_exits_2_without_network():
    r = run("--offine")
    assert r.returncode == 2 and "unrecognized arguments" in r.stderr


def test_help_prints_usage():
    r = run("--help")
    assert r.returncode == 0 and "usage:" in r.stdout


def test_offline_finds_no_unsourced_entries_in_repo():
    # Stale-snapshot judgment is covered by the hermetic test below; asserting the exit code here
    # would turn red by itself once a real snapshot passes 180 days.
    r = run("--offline")
    assert "UNSOURCED" not in r.stdout and "MISSING" not in r.stdout, r.stdout
    assert "\r" not in r.stdout, "no carriage-return progress when stdout is not a TTY"


def test_bare_arxiv_id_is_unsourced():
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "s" / "references" / "landscape.md"
        f.parent.mkdir(parents=True)
        f.write_text("**Verified: 2026-10-02.**\n- **Foo** - a paper. Status: research. arXiv:2401.00001\n")
        assert cs.check([f], offline=True) == 1
        f.write_text("**Verified: 2026-10-02.**\n- **Foo** - a paper. Status: research. Source: https://arxiv.org/abs/2401.00001\n")
        assert cs.check([f], offline=True) == 0


def test_stale_snapshot_fails_using_oldest_partial_date():
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "s" / "references" / "landscape.md"
        f.parent.mkdir(parents=True)
        f.write_text("**Verified: 2099-01-01 (changed entries; rest 2000-01-01).**\n- **Foo** - x. Source: https://example.com\n")
        assert cs.check([f], offline=True) == 1


def test_impossible_verified_date_is_reported_not_raised():
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "s" / "references" / "landscape.md"
        f.parent.mkdir(parents=True)
        f.write_text("**Verified: 2026-13-45.**\n- **Foo** - x. Source: https://example.com\n")
        assert cs.check([f], offline=True) == 1


class _Stub(BaseHTTPRequestHandler):
    """Local server: /flaky 500s once, /slow stalls once, /hang always stalls, /down always 503, /gone 404."""

    hits: dict[str, int] = {}

    def _answer(self):
        n = _Stub.hits[self.path] = _Stub.hits.get(self.path, 0) + 1
        if self.path == "/flaky":
            code = 500 if n == 1 else 200
        elif self.path == "/slow":
            time.sleep(1 if n == 1 else 0)
            code = 200
        elif self.path == "/hang":
            time.sleep(1)
            code = 200
        elif self.path == "/down":
            code = 503
        elif self.path == "/gone":
            code = 404
        else:
            code = 200
        self.send_response(code)
        self.send_header("Content-Length", "0")
        self.end_headers()

    do_HEAD = do_GET = _answer

    def log_message(self, *a):
        pass


@contextlib.contextmanager
def stub_server():
    _Stub.hits = {}
    srv = ThreadingHTTPServer(("127.0.0.1", 0), _Stub)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    old = (cs.RETRY_WAIT, cs.TIMEOUT)
    cs.RETRY_WAIT, cs.TIMEOUT = 0, 0.3
    try:
        yield f"http://127.0.0.1:{srv.server_port}"
    finally:
        cs.RETRY_WAIT, cs.TIMEOUT = old
        srv.shutdown()


def check_url(path_url: str) -> tuple[int, str]:
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "s" / "references" / "landscape.md"
        f.parent.mkdir(parents=True)
        f.write_text(f"**Verified: 2026-10-02.**\n- **Foo** - x. Source: {path_url}\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            return cs.check([f], offline=False), buf.getvalue()


def test_retry_wait_defaults_to_three_seconds():
    assert cs.RETRY_WAIT == 3


def test_5xx_then_200_is_fine():
    with stub_server() as base:
        assert cs.probe(base + "/flaky") == (base + "/flaky", 200)
        assert _Stub.hits["/flaky"] == 2


def test_timeout_then_200_is_fine():
    # The HEAD stalls, so probe() must go through its own retry (hit 2) rather than a GET fallback.
    with stub_server() as base:
        assert cs.probe(base + "/slow")[1] == 200
        assert _Stub.hits["/slow"] == 2


def test_persistent_timeout_costs_one_request_per_attempt():
    with stub_server() as base:
        assert cs.probe(base + "/hang")[1] == "timeout"
        assert _Stub.hits["/hang"] == 2  # HEAD, retry HEAD; no GET fallback after a timeout


def test_connection_refused_is_non_fatal():
    import socket

    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()  # nothing listens on this port now
    problems, out = check_url(f"http://127.0.0.1:{port}/x")
    assert problems == 0 and "DEAD" not in out and "server error" in out, out


def test_persistent_5xx_retries_once_then_reports_status():
    with stub_server() as base:
        assert cs.probe(base + "/down")[1] == 503
        assert _Stub.hits["/down"] == 2  # first try plus exactly one retry


def test_404_is_not_retried():
    with stub_server() as base:
        assert cs.probe(base + "/gone")[1] == 404
        assert _Stub.hits["/gone"] == 1


def test_persistent_5xx_is_a_separate_group_and_does_not_fail():
    with stub_server() as base:
        problems, out = check_url(base + "/down")
    assert problems == 0, out
    assert "server error" in out and "DEAD" not in out and "503" in out


def test_404_still_fails_as_dead():
    with stub_server() as base:
        problems, out = check_url(base + "/gone")
    assert problems == 1 and "DEAD [404]" in out, out


def test_dns_failure_still_fails_as_dead():
    problems, out = check_url("http://no-such-host.invalid/x")
    assert problems == 1 and "DEAD" in out, out


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
    print("ok")
