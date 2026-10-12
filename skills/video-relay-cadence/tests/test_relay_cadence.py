# Pure functions of relay_cadence: skip pattern of relayed frames against the source, and the judder verdict per fps pair (no ROS, no network)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import relay_cadence as fc  # noqa: E402


def test_30fps_sampled_at_24fps_gives_1112_pattern():
    src = [f"h{i}" for i in range(300)]                       # 10 s of a 30 fps source
    sent = [src[int(k * 30 / 24)] for k in range(240)]          # pick the latest frame at 24 fps
    r = fc.skip_pattern(src, sent)
    assert r["matched"] == 240 and r["unmatched"] == 0
    assert r["steps"] == {1: 180, 2: 59} or r["steps"].get(2, 0) >= 55
    assert r["judder"] is True
    assert "1112" in r["pattern"]


def test_sending_every_frame_has_no_judder():
    src = [f"h{i}" for i in range(90)]
    r = fc.skip_pattern(src, list(src))
    assert r["steps"] == {1: 89} and r["judder"] is False


def test_exact_halving_is_an_even_2():
    src = [f"h{i}" for i in range(90)]
    r = fc.skip_pattern(src, src[::2])
    assert r["steps"] == {2: 44} and r["judder"] is False


def test_reencoded_frames_give_no_verdict():
    r = fc.skip_pattern(["a", "b", "c"], ["x", "y", "z"])
    assert r["matched"] == 0 and r["judder"] is None


def test_fps_advice():
    assert fc.advise(30, 24)["judder"] is True
    assert fc.advise(30, 30)["judder"] is False
    assert fc.advise(30, 15)["judder"] is False
    assert fc.advise(30, 24)["suggest"] == [30, 15, 10]


def test_repeat_pattern_from_a_timer_faster_than_the_source_is_judder():
    src = [f"h{i}" for i in range(300)]
    sent = [src[int(k * 30 / 40)] for k in range(400)]          # 40 fps timer over a 30 fps source repeats some frames
    r = fc.skip_pattern(src, sent)
    assert r["steps"].get(0, 0) > 0 and r["steps"].get(1, 0) > 0
    assert r["judder"] is True


def test_rate_at_or_above_source_is_smooth_only_for_a_relay_driven_by_new_frames():
    a = fc.advise(30, 40)
    assert a["judder"] is False
    assert "timer" in a["why"] and "new-frame" in a["why"]
    assert "timer" not in fc.advise(30, 15)["why"]
