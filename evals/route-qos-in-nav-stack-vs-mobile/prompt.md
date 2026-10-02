---
name: route-qos-in-nav-stack-vs-mobile
description: "Collision: standardizing QoS across a Nav2-based AMR stack."
tags: [routing]
expected_outcome: "Expected ros2-master. QoS is ROS 2 architecture ('node/QoS/executor architecture belongs to ros2-master', robot-perception's text; robot-aerial and robot-marine say the same of ROS 2 architecture), and robot-mobile's own text limits it to one robot moving through a space, from wheels and odometry up to navigation behaviors."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
On our AMR the Nav2 stack is up, but a custom node never receives /map and lidar scans arrive intermittently. I suspect QoS mismatches. How should I standardize QoS profiles for sensor data, the map, and command topics across every node in the stack, and what durability should the map use?
