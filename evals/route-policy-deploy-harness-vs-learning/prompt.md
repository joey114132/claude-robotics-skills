---
name: route-policy-deploy-harness-vs-learning
description: "Collision: wrapping a trained policy before it drives a real arm (physical-ai-harness) versus the policy itself (robot-learning)."
tags: [routing]
expected_outcome: "Expected physical-ai-harness. The policy is already trained and the question is what must wrap it between the model and the actuators on a ROS 2 robot (output limits, stale camera frames, fallback controller). robot-learning's own text covers whether to learn, the data, training and evaluation, not the runtime contract on the actuator path."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
We trained an ACT policy for our 6-DOF arm and it works in the lab. Next week it runs on the real robot through ROS 2, publishing joint targets at 30 Hz straight to the controller. What should sit between the policy node and the controller so it can't slam the arm into the table if it outputs garbage or its camera feed freezes, and how should we fall back to a safe controller when that happens?
