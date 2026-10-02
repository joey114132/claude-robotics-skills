---
name: route-sensor-noise-sim-vs-perception
description: "Collision: modeling realistic depth and LiDAR noise inside a simulator."
tags: [routing]
expected_outcome: "Expected robot-sim. robot-sim 'owns the simulator itself: what it models, what it silently approximates'. robot-perception's text starts at the physical sensor ('everything between the physical sensor and the pose'), so a simulated sensor model is outside it."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
In Isaac Sim my simulated depth camera and LiDAR output is far cleaner than the real sensors. How should I model realistic noise, dropouts, and multipath in the simulated sensors so sim output matches the real hardware, and how do I check that it does?
