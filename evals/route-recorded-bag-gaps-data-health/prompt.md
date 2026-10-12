---
name: route-recorded-bag-gaps-data-health
description: "Collision: checking recorded rosbag2 episodes for camera frame loss (robot-data-health) versus training and dataset advice (robot-learning)."
tags: [routing]
expected_outcome: "Expected robot-data-health. The user has recorded mcap episodes and wants to know which have frozen or missing camera frames before training. robot-learning covers whether to learn, dataset design, training and evaluation, and its own text does not scan finished recordings for gaps."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I have about 80 teleoperation episodes recorded as rosbag2 mcap files with two wrist cameras each. When I replay them in Rerun the video stutters, and some episodes seem to lose a camera for a few seconds. Before I send them to imitation-learning training, how do I find out which episodes are bad and why the frames went missing?
