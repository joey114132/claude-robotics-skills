#!/usr/bin/env python3
# Scans recorded rosbag2 episodes for camera health and sorts each into keep/warn/drop: coverage, gaps, simultaneous multi-camera gaps, duplicate publishers, header clock offset
"""Usage (inside a ROS 2 environment):
    data_health.py <root or episode dir>... [--hz 30 [--hz /topic=15 ...]] [--gap 1.0] [--min-cover 90] [--csv out.csv]

A bare --hz number is the default camera rate; --hz /topic=N overrides it for that topic (repeat the flag).
The storage plugin (mcap, sqlite3) is read from each bag's metadata.yaml; an mcap bag needs rosbag2_storage_mcap installed.
Read-only. Reads only camera topics (CompressedImage / Image). Prints one line per episode and, with --csv,
writes a keep/drop list you can feed to training-data selection.
"""
import argparse
import csv
import os
import re
import statistics
import sys

import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

CAM_TYPES = ("sensor_msgs/msg/CompressedImage", "sensor_msgs/msg/Image")
HEADER_SAMPLES = 30          # header stamps read per topic; deserializing every frame is slow on 10 GB bags
DUP_PCT = 150                # coverage above this means two publishers on one topic
CLOCK_WARN_S = 1.0           # |header - record time| above this means the publisher's clock is off


def find_episodes(roots):
    """Directories that hold a rosbag2 metadata.yaml, searched recursively."""
    out = []
    for root in roots:
        for d, _, files in os.walk(root):
            if "metadata.yaml" in files:
                out.append(d)
    return sorted(out)


def storage_id(path):
    """The storage plugin a bag was written with, from its metadata.yaml (mcap on Jazzy by choice, sqlite3 on Humble by default)."""
    with open(os.path.join(path, "metadata.yaml")) as f:
        m = re.search(r"^\s*storage_identifier:\s*(\S+)", f.read(), re.M)
    return m.group(1) if m else ""            # empty lets rosbag2 pick the plugin itself


def parse_hz(values):
    """--hz values to (default rate, {topic: rate}). A bare number sets the default, /topic=N overrides one topic."""
    default, over = 30.0, {}
    for v in values:
        if "=" in v:
            topic, _, n = v.rpartition("=")
            over[topic] = float(n)
        else:
            default = float(v)
    return default, over


def _host(topic):
    """Publisher-host key: the topic minus its last two segments (/hand/left/cam0/compressed -> /hand/left)."""
    parts = topic.strip("/").split("/")
    return "/" + "/".join(parts[:-2]) if len(parts) > 2 else topic


def _overlap(a, b):
    lo, hi = max(a[0], b[0]), min(a[0] + a[1], b[0] + b[1])
    return max(0.0, hi - lo)


def scan_episode(path, expected_hz=30.0, gap_s=1.0, min_cover=90.0, hz_overrides=None):
    r = rosbag2_py.SequentialReader()
    r.open(rosbag2_py.StorageOptions(uri=path, storage_id=storage_id(path)), rosbag2_py.ConverterOptions("cdr", "cdr"))
    meta = r.get_metadata()
    t0 = meta.starting_time.nanoseconds / 1e9
    dur = meta.duration.nanoseconds / 1e9
    cams = {t.name: t.type for t in r.get_all_topics_and_types() if t.type in CAM_TYPES}
    if not cams:                                                     # nothing to measure is not a clean bill of health
        return {"path": path, "duration_s": round(dur, 2), "topics": {}, "simultaneous_gaps": [], "verdict": "drop",
                "reasons": ["no camera topics"], "warnings": []}
    r.set_filter(rosbag2_py.StorageFilter(topics=list(cams)))
    ts = {c: [] for c in cams}
    offs = {c: [] for c in cams}
    while r.has_next():
        topic, data, t_ns = r.read_next()
        t = t_ns / 1e9
        ts[topic].append(t - t0)
        if len(offs[topic]) < HEADER_SAMPLES:
            h = deserialize_message(data, get_message(cams[topic])).header.stamp
            offs[topic].append(h.sec + h.nanosec / 1e9 - t)
    topics, reasons, warnings = {}, [], []
    for c, x in ts.items():
        x.sort()
        gaps = [(round(a, 3), round(b - a, 3)) for a, b in zip(x, x[1:]) if b - a > gap_s]
        if x and x[0] > gap_s:
            gaps.insert(0, (0.0, round(x[0], 3)))                      # camera started late
        if x and dur - x[-1] > gap_s:
            gaps.append((round(x[-1], 3), round(dur - x[-1], 3)))      # camera stopped early
        hz = (hz_overrides or {}).get(c, expected_hz)
        cover = 100.0 * len(x) / (hz * dur) if dur > 0 else 0.0
        off = statistics.median(offs[c]) if offs[c] else None
        topics[c] = {"frames": len(x), "coverage_pct": round(cover, 1), "gaps": gaps,
                     "header_offset_s": None if off is None else round(off, 3)}
        if cover < min_cover:
            reasons.append(f"{c} coverage {cover:.0f}%")
        mid = [g for g in gaps if g[0] > 0 and g[0] + g[1] < dur - 1e-6]
        edge = [g for g in gaps if g not in mid]
        if mid:
            reasons.append(f"{c} {len(mid)} gap(s) mid-episode, longest {max(g[1] for g in mid):.1f}s")
        for g in edge:                                               # a camera that started late or stopped early can be trimmed
            warnings.append(f"{c} no frames {g[0]:.1f}-{g[0] + g[1]:.1f}s: trim that edge before training")
        if cover > DUP_PCT:
            warnings.append(f"{c} coverage {cover:.0f}%: duplicate publisher on this topic?")
        if off is not None and abs(off) > CLOCK_WARN_S:
            warnings.append(f"{c} header clock off by {off:+.1f}s: publisher clock not synced")
    # Several cameras gapped at the same time. Spanning two or more publisher hosts points at the receiving side (recorder host, switch, kernel); inside one host it points at that publisher
    sim = []
    allg = [(c, g) for c, t in topics.items() for g in t["gaps"]]
    for i, (c, g) in enumerate(allg):
        group = {c} | {c2 for c2, g2 in allg if c2 != c and _overlap(g, g2) >= 0.5 * min(g[1], g2[1])}
        if len(group) >= 2 and not any(_overlap(g, (s["t"], s["len"])) > 0 for s in sim):
            hosts = {_host(t) for t in group}
            sim.append({"t": g[0], "len": g[1], "n_topics": len(group), "hosts": sorted(hosts),
                        "cause": "receive-side" if len(hosts) >= 2 else "same-publisher-host"})
    sim = [s_ for s_ in sim if s_["t"] > 0 and s_["t"] + s_["len"] < dur - 1e-6]   # leading and trailing gaps are already handled by the trim warning above
    for s_ in sim:
        where = "receiver, switch or kernel (spans publishers " if s_["cause"] == "receive-side" else "one publisher host ("
        reasons.append(f"cameras gapped together at {s_['t']:.1f}s for {s_['len']:.1f}s: {where}{', '.join(s_['hosts'])})")
    verdict = "drop" if reasons else "warn" if warnings else "keep"
    return {"path": path, "duration_s": round(dur, 2), "topics": topics, "simultaneous_gaps": sim,
            "verdict": verdict, "reasons": reasons, "warnings": warnings}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("roots", nargs="+")
    ap.add_argument("--hz", action="append", default=[], metavar="N|/TOPIC=N",
                    help="expected camera rate: a number for all cameras (default 30), or /topic=N for one topic; repeatable")
    ap.add_argument("--gap", type=float, default=1.0, help="gap threshold in seconds")
    ap.add_argument("--min-cover", type=float, default=90.0, help="coverage below this percent drops the episode")
    ap.add_argument("--csv", help="write path,verdict,duration,min_coverage,reasons,warnings")
    a = ap.parse_args(argv)
    hz, hz_over = parse_hz(a.hz)
    eps = find_episodes(a.roots)
    if not eps:
        print("no rosbag2 episode (metadata.yaml) under the given roots", file=sys.stderr)
        return 2
    rows = []
    for p in eps:
        try:
            res = scan_episode(p, hz, a.gap, a.min_cover, hz_over)
        except Exception as e:                       # a broken bag is a finding, not a crash of the whole scan
            res = {"path": p, "duration_s": 0, "topics": {}, "verdict": "drop", "reasons": [f"unreadable: {e}"], "warnings": []}
        covers = [t["coverage_pct"] for t in res["topics"].values()]
        mc = min(covers) if covers else 0.0
        print(f"{res['verdict']:5s} {res['duration_s']:7.1f}s  min-cam {mc:5.1f}%  {os.path.relpath(p)}"
              + ("".join(f"\n        - {x}" for x in res["reasons"] + res["warnings"])))
        rows.append([p, res["verdict"], res["duration_s"], mc, " | ".join(res["reasons"]), " | ".join(res["warnings"])])
    n = {v: sum(r[1] == v for r in rows) for v in ("keep", "warn", "drop")}
    print(f"\n{len(rows)} episodes: keep {n['keep']}, warn {n['warn']}, drop {n['drop']}")
    if a.csv:
        with open(a.csv, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["path", "verdict", "duration_s", "min_camera_coverage_pct", "reasons", "warnings"])
            w.writerows(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
