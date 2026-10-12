#!/usr/bin/env python3
# Measures how many source frames a video relay (MJPEG server etc.) skips per relayed frame, to separate judder (even arrivals, uneven motion) from a smooth stream
"""Live use (ROS 2 environment, on the machine that runs the relay, briefly, never during a recording):
    relay_cadence.py --topic /hand/right/cam0/compressed --url "http://127.0.0.1:26602/stream?topic=/hand/right/cam0/compressed" [--secs 10]
Offline math:
    relay_cadence.py --advise SRC_FPS RELAY_FPS

It matches each relayed JPEG to a source frame by md5, so it only works when the relay passes the JPEG through
unchanged. A re-encoding relay gives matched=0 and no verdict.
"""
import argparse
import collections
import hashlib
import sys
import threading
import time


def skip_pattern(src_hashes, sent_hashes):
    """src_hashes: source frames in arrival order. sent_hashes: relayed frames in order.
    Returns how many source frames the relay advanced per relayed frame. Uneven steps (a mix of 1 and 2) are judder."""
    pos = {h: i for i, h in enumerate(src_hashes)}
    idx = [pos[h] for h in sent_hashes if h in pos]
    steps = [b - a for a, b in zip(idx, idx[1:])]
    hist = dict(sorted(collections.Counter(steps).items()))
    judder = None if len(idx) < 2 else len([s for s in hist if s > 0]) > 1
    return {"matched": len(idx), "unmatched": len(sent_hashes) - len(idx), "steps": hist, "judder": judder,
            "pattern": "".join(str(min(s, 9)) for s in steps[:40])}


def advise(src_fps, relay_fps):
    """A relay that samples a src_fps stream at relay_fps judders unless relay_fps >= src_fps or src_fps/relay_fps is
    a whole number. Suggest the source rate and its whole-number divisors."""
    src, rel = round(src_fps), round(relay_fps)
    even = rel >= src or (rel > 0 and src % rel == 0)
    return {"judder": not even, "suggest": [src] + [src // k for k in (2, 3) if src % k == 0][:2],
            "why": "steps alternate between 1 and 2 source frames" if not even else "every step is the same size"}


def measure(topic, url, secs):
    import socket
    from urllib.parse import urlparse
    import rclpy
    from rclpy.qos import qos_profile_sensor_data
    from sensor_msgs.msg import CompressedImage
    src, sent = [], []
    u = urlparse(url)

    def pull():
        s = socket.create_connection((u.hostname, u.port or 80), timeout=5)
        s.sendall(f"GET {u.path}?{u.query} HTTP/1.1\r\nHost: {u.hostname}\r\n\r\n".encode())
        buf, t0 = b"", time.monotonic()
        while time.monotonic() - t0 < secs:
            d = s.recv(65536)
            if not d:
                break
            buf += d
            while True:
                i = buf.find(b"Content-Length: ")
                j, k = buf.find(b"\r\n", i), buf.find(b"\r\n\r\n", i)
                if i < 0 or j < 0 or k < 0:
                    buf = buf if i >= 0 else buf[-32:]
                    break
                n = int(buf[i + 16:j])
                if len(buf) < k + 4 + n:
                    break
                sent.append(hashlib.md5(buf[k + 4:k + 4 + n]).hexdigest())
                buf = buf[k + 4 + n:]

    rclpy.init()
    node = rclpy.create_node("relay_cadence_probe")
    node.create_subscription(CompressedImage, topic, lambda m: src.append(hashlib.md5(bytes(m.data)).hexdigest()),
                             qos_profile_sensor_data)
    th = threading.Thread(target=pull, daemon=True)
    end, started = time.monotonic() + secs + 1, False
    while time.monotonic() < end:
        rclpy.spin_once(node, timeout_sec=0.01)
        if not started and len(src) > 5:                     # start the relay pull exactly once, after the source topic is flowing
            th.start()
            started = True
    node.destroy_node()
    rclpy.shutdown()
    r = skip_pattern(src, sent)
    r["source_fps"] = round(len(src) / (secs + 1), 1)
    r["relay_fps"] = round(len(sent) / secs, 1)
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--topic")
    ap.add_argument("--url")
    ap.add_argument("--secs", type=float, default=10.0)
    ap.add_argument("--advise", nargs=2, type=float, metavar=("SRC_FPS", "RELAY_FPS"))
    a = ap.parse_args(argv)
    if a.advise:
        print(advise(*a.advise))
        return 0
    if not (a.topic and a.url):
        ap.error("--topic and --url, or --advise")
    r = measure(a.topic, a.url, a.secs)
    print(r)
    if r["judder"] is None:
        print("no verdict: relayed frames did not match source frames (relay re-encodes?)", file=sys.stderr)
        return 1
    print(advise(r["source_fps"], r["relay_fps"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
