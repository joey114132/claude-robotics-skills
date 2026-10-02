---
name: route-handeye-calibration-vs-arm
description: "Collision: eye-in-hand calibration of a wrist camera, perception versus arm."
tags: [routing]
expected_outcome: "Expected robot-perception. Its description names hand-eye / eye-in-hand calibration and its text owns 'sensor choice, calibration, synchronization' between the physical sensor and the pose. robot-perception's text assigns only 'motion execution' to robot-arm, so calibrating the sensor is not the arm pipeline."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I mounted a RealSense on the wrist of my xArm and need eye-in-hand calibration. How many poses should I collect, which solver should I use (Tsai, Park, Daniilidis), and how do I check the result is good?
