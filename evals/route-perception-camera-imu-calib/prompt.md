---
name: route-perception-camera-imu-calib
description: "Single-skill routing: camera-IMU extrinsics and stale depth timestamps."
tags: [routing]
expected_outcome: "Routes to robot-perception: camera-IMU calibration, time synchronization and depth-data problems sit between the physical sensor and the pose consumers receive."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
The point cloud from my RealSense D435i has a systematic offset, I need camera-to-IMU extrinsic calibration for visual-inertial odometry, and the timestamps look stale compared to the IMU. How should I calibrate and synchronize this?
