---
name: route-simulator-choice-vs-ros2
description: "Collision: picking a simulator inside a ROS 2 project, simulation versus ROS 2 architecture."
tags: [routing]
expected_outcome: "Expected robot-sim. ros2-master's text says 'Which simulator to use and how far to trust it belong to robot-sim', even though the project is ROS 2."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
My ROS 2 Jazzy arm project needs a simulator for contact-rich grasping tests. Gazebo, MuJoCo, or Isaac Sim: which should I pick, and how far can I trust its contact results before testing on the real gripper?
