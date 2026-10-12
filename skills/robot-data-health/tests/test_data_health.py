# Checks that data_health catches simultaneous gaps, duplicate publishers and header clock offset on synthetic bags, and keeps a clean bag (needs a ROS environment)
import os
import sys

import pytest

rosbag2_py = pytest.importorskip("rosbag2_py")
from rclpy.serialization import serialize_message  # noqa: E402
from sensor_msgs.msg import CompressedImage, JointState  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import data_health as eh  # noqa: E402

T0 = 1_000_000_000 * 1_790_000_000


def _bag(path, streams, dur=10.0, storage="mcap"):
    """streams: [(topic, type_name, msg_class, hz, gap=(a, b) or None, header_offset_s)]"""
    w = rosbag2_py.SequentialWriter()
    w.open(rosbag2_py.StorageOptions(uri=str(path), storage_id=storage), rosbag2_py.ConverterOptions("cdr", "cdr"))
    msgs = []
    for i, (topic, tname, cls, hz, gap, off) in enumerate(streams):
        w.create_topic(rosbag2_py.TopicMetadata(id=i, name=topic, type=tname, serialization_format="cdr"))
        for k in range(int(dur * hz)):
            t = k / hz
            if gap and gap[0] <= t < gap[1]:
                continue
            m = cls()
            ns = T0 + int((t + off) * 1e9)
            m.header.stamp.sec, m.header.stamp.nanosec = ns // 10**9, ns % 10**9
            msgs.append((T0 + int(t * 1e9), topic, serialize_message(m)))
    for ts, topic, data in sorted(msgs):
        w.write(topic, data, ts)
    del w
    return str(path)


CAM = ("sensor_msgs/msg/CompressedImage", CompressedImage)


def test_catches_shared_gap_duplicate_publisher_and_clock_offset(tmp_path):
    p = _bag(tmp_path / "bad", [
        ("/hand/left/cam0/compressed", *CAM, 30, (3.0, 6.0), 0.0),
        ("/hand/right/cam0/compressed", *CAM, 30, (3.0, 6.0), 100.0),
        ("/camera/head/compressed", *CAM, 60, None, 0.0),
        ("/arm/joint_states", "sensor_msgs/msg/JointState", JointState, 100, None, 0.0),
    ])
    r = eh.scan_episode(p, expected_hz=30, gap_s=1.0, min_cover=90)
    left = r["topics"]["/hand/left/cam0/compressed"]
    assert 65 <= left["coverage_pct"] <= 75
    assert len(left["gaps"]) == 1 and abs(left["gaps"][0][0] - 3.0) < 0.1 and abs(left["gaps"][0][1] - 3.0) < 0.1
    assert r["simultaneous_gaps"] and r["simultaneous_gaps"][0]["n_topics"] == 2
    assert r["simultaneous_gaps"][0]["cause"] == "receive-side"          # spans the two publisher hosts /hand/left and /hand/right
    assert r["verdict"] == "drop"
    assert r["topics"]["/camera/head/compressed"]["coverage_pct"] > 150
    assert any("duplicate" in w for w in r["warnings"])
    assert abs(r["topics"]["/hand/right/cam0/compressed"]["header_offset_s"] - 100.0) < 0.5
    assert any("clock" in w for w in r["warnings"])
    assert "/arm/joint_states" not in r["topics"]          # only camera topics are read


def test_clean_episode_is_keep(tmp_path):
    p = _bag(tmp_path / "ok", [("/hand/left/cam0/compressed", *CAM, 30, None, 0.0),
                               ("/hand/right/cam0/compressed", *CAM, 30, None, 0.0)])
    r = eh.scan_episode(p, expected_hz=30, gap_s=1.0, min_cover=90)
    assert r["verdict"] == "keep" and not r["reasons"] and not r["warnings"]


def test_folder_walk_finds_episodes(tmp_path):
    _bag(tmp_path / "d1" / "ep1", [("/hand/left/cam0/compressed", *CAM, 30, None, 0.0)])
    _bag(tmp_path / "d2" / "ep2", [("/hand/left/cam0/compressed", *CAM, 30, None, 0.0)])
    assert len(eh.find_episodes([str(tmp_path)])) == 2


def test_gap_inside_one_publisher_host_is_not_blamed_on_the_receiver(tmp_path):
    p = _bag(tmp_path / "one_host", [
        ("/hand/left/cam0/compressed", *CAM, 30, (3.0, 6.0), 0.0),
        ("/hand/left/cam1/compressed", *CAM, 30, (3.0, 6.0), 0.0),
        ("/hand/right/cam0/compressed", *CAM, 30, None, 0.0),
    ])
    r = eh.scan_episode(p, expected_hz=30, gap_s=1.0, min_cover=60)
    assert r["simultaneous_gaps"][0]["cause"] == "same-publisher-host"


def test_edge_gaps_are_trimmed_not_dropped(tmp_path):
    p = _bag(tmp_path / "late", [("/hand/left/cam0/compressed", *CAM, 30, (0.0, 1.5), 0.0),
                                 ("/hand/right/cam0/compressed", *CAM, 30, None, 0.0)], dur=60.0)
    r = eh.scan_episode(p, expected_hz=30, gap_s=1.0, min_cover=90)
    assert r["verdict"] == "warn" and not r["reasons"]
    assert any("trim" in w for w in r["warnings"])


def test_bag_without_camera_topics_is_not_keep(tmp_path):
    p = _bag(tmp_path / "nocam", [("/arm/joint_states", "sensor_msgs/msg/JointState", JointState, 100, None, 0.0)])
    r = eh.scan_episode(p)
    assert r["verdict"] == "drop" and "no camera topics" in r["reasons"]


def test_storage_id_comes_from_metadata_not_a_hardcoded_mcap(tmp_path):
    p = _bag(tmp_path / "sq", [("/hand/left/cam0/compressed", *CAM, 30, None, 0.0)], storage="sqlite3")
    assert eh.storage_id(p) == "sqlite3"
    r = eh.scan_episode(p, expected_hz=30)
    assert r["verdict"] == "keep" and r["topics"]["/hand/left/cam0/compressed"]["frames"] == 300


def test_per_topic_hz_override_stops_a_slow_camera_faking_a_failure(tmp_path):
    p = _bag(tmp_path / "mixed", [("/hand/left/cam0/compressed", *CAM, 30, None, 0.0),
                                  ("/hand/left/depth/compressed", *CAM, 15, None, 0.0)])
    assert eh.scan_episode(p, expected_hz=30)["verdict"] == "drop"
    r = eh.scan_episode(p, expected_hz=30, hz_overrides={"/hand/left/depth/compressed": 15.0})
    assert r["verdict"] == "keep"


def test_hz_arguments_split_into_default_and_overrides():
    assert eh.parse_hz(["30", "/depth=15"]) == (30.0, {"/depth": 15.0})
    assert eh.parse_hz([]) == (30.0, {})
    assert eh.parse_hz(["/a=10", "/b=5"]) == (30.0, {"/a": 10.0, "/b": 5.0})
