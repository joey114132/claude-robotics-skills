---
name: route-teleop-demos-vs-arm
description: "Collision: recording demos on a leader-follower pair and training ACT, learning versus arm."
tags: [routing]
expected_outcome: "Expected robot-learning. robot-learning 'owns the decision to learn at all, and everything after it: data, policy class, training, evaluation, deployment', and says arm integration belongs to robot-arm. The arm already works; the questions are all data and policy questions, although robot-arm's description lists leader-follower teleoperation."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
My SO-101 leader-follower pair works. I want to record demonstrations and train ACT on a pick-and-place task. How many episodes do I need, how should I structure the dataset, and how do I evaluate the success rate?
