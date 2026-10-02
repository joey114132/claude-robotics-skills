---
name: route-drone-ros2-graph-vs-aerial
description: "Collision: ROS 2 node graph for a drone companion computer, ros2-master versus aerial."
tags: [routing]
expected_outcome: "Expected ros2-master. robot-aerial's own text routes 'ROS 2 graph and node architecture to ros2-master', even though robot-aerial's description lists companion computers and ROS 2 offboard control."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I'm designing the ROS 2 node graph for our inspection drone's companion computer. Should mission commands be a topic, a service, or an action? Which nodes should be lifecycle nodes, should I use a single- or multi-threaded executor, and how do I split packages and launch files?
