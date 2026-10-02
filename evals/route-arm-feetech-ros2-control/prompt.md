---
name: route-arm-feetech-ros2-control
description: "Single-skill routing: bring up a hobby Feetech arm from URDF to motion."
tags: [routing]
expected_outcome: "Routes to robot-arm: the ordered URDF, ros2_control hardware interface, MoveIt 2 and trajectory-execution pipeline for a servo-driven arm is the arm pipeline."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I built a 6-DOF arm out of Feetech STS3215 servos and finished the URDF. What are the steps from here to get it moving through ros2_control and MoveIt 2? I need to know how to wire the serial bus in as a hardware interface, set joint limits, and execute trajectories safely.
