#!/usr/bin/env python3
"""Self-check for qos_audit.py against a small fixture ROS 2 package.

Run: python3 test_qos_audit.py
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "qos_audit.py"

FIXTURE = '''
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy, qos_profile_sensor_data
import rclpy

def unresolvable_qos():
    return build_qos_from_config()  # not a QoSProfile literal -> UNKNOWN


class Node:
    def __init__(self):
        # inline QoSProfile BEST_EFFORT publisher
        self.pub = self.create_publisher(
            Msg, "/leader/stream",
            QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT,
                       durability=DurabilityPolicy.VOLATILE, history=HistoryPolicy.KEEP_LAST))

        # bare-int RELIABLE subscriber on the SAME topic -> INCOMPATIBLE
        self.create_subscription(Msg, "/leader/stream", self._cb, 10)

        # variable-assigned QoSProfile, used later
        stream_qos = QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT,
                                 history=HistoryPolicy.KEEP_LAST)
        self.create_subscription(Msg, "/other/stream", self._cb, stream_qos)

        # f-string topic inside a dict comprehension
        self.hand_pub = {
            s: self.create_publisher(Msg, f"/hand/{s}/grip", stream_qos)
            for s in ("left", "right")
        }

        # preset qos on a sensor-data subscriber
        self.create_subscription(Msg, "/camera/image", self._cb, qos_profile_sensor_data)

        # unresolvable qos -> UNKNOWN
        self.create_subscription(Msg, "/weird/topic", self._cb, unresolvable_qos())

    def reassigned_a(self):
        # same local name, DIFFERENT profiles in sibling methods -> ambiguous under a
        # whole-module scan; both uses must come back UNKNOWN(q), never a borrowed value
        q = QoSProfile(depth=1, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.create_publisher(Msg, "/reassign/first", q)

    def reassigned_b(self):
        q = QoSProfile(depth=9, reliability=ReliabilityPolicy.RELIABLE)
        self.create_subscription(Msg, "/reassign/second", self._cb, q)

    def _cb(self, msg):
        pass
'''


def run(src_root: Path) -> dict:
    out = subprocess.run([sys.executable, str(SCRIPT), str(src_root), "--json"],
                          capture_output=True, text=True)
    return json.loads(out.stdout), out.returncode


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        pkg = Path(tmp) / "fixture_pkg"
        pkg.mkdir()
        (pkg / "node.py").write_text(FIXTURE, encoding="utf-8")

        result, code = run(Path(tmp))

        topics = {e["topic"]: e for e in result["entries"]}
        assert "/leader/stream" in topics
        assert any(e["topic"] == "/hand/{s}/grip" for e in result["entries"]), \
            "f-string topic in dict comprehension not found verbatim"

        stream_entries = [e for e in result["entries"] if e["topic"] == "/other/stream"]
        assert stream_entries and stream_entries[0]["reliability"] == "BEST_EFFORT", \
            "variable-assigned QoSProfile did not resolve"

        cam = [e for e in result["entries"] if e["topic"] == "/camera/image"][0]
        assert (cam["reliability"], cam["durability"], cam["history"], cam["depth"]) == \
            ("BEST_EFFORT", "VOLATILE", "KEEP_LAST", "5"), "qos_profile_sensor_data preset wrong"

        weird = [e for e in result["entries"] if e["topic"] == "/weird/topic"][0]
        assert weird["reliability"].startswith("UNKNOWN("), "unresolvable qos call should be UNKNOWN"
        assert any(e["topic"] == "/weird/topic" for e in result["unresolved"])

        assert len(result["incompatible"]) == 1, result["incompatible"]
        inc = result["incompatible"][0]
        assert inc["topic"] == "/leader/stream"
        assert inc["pub"]["reliability"] == "BEST_EFFORT" and inc["sub"]["reliability"] == "RELIABLE"

        assert code == 1, "exit code should be 1 when an INCOMPATIBLE pair exists"

        hand_side = [e for e in result["one_sided"] if e["topic"] == "/hand/{s}/grip"]
        assert hand_side and hand_side[0]["kind"] == "PUB"

        first = [e for e in result["entries"] if e["topic"] == "/reassign/first"][0]
        second = [e for e in result["entries"] if e["topic"] == "/reassign/second"][0]
        assert first["reliability"] == "UNKNOWN(q)" and second["reliability"] == "UNKNOWN(q)", \
            f"ambiguous variable must not resolve to a borrowed value: {first}, {second}"
        assert {"/reassign/first", "/reassign/second"} <= {e["topic"] for e in result["unresolved"]}

    print("all assertions passed")


if __name__ == "__main__":
    main()
