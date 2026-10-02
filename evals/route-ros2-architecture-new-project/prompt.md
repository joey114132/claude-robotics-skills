---
name: route-ros2-architecture-new-project
description: "Single-skill routing: new ROS 2 project architecture decisions."
tags: [routing]
expected_outcome: "Routes to ros2-master: topic vs service vs action, lifecycle nodes, executor choice and package and launch layout are ROS 2 architecture decisions."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I'm starting a new ROS 2 Jazzy robot project. For a go-to-pose command, should I use a topic, a service, or an action? Which of my nodes should be lifecycle nodes, which executor should I pick, and how should I lay out packages and launch files?
