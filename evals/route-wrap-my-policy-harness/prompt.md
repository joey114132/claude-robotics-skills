---
name: route-wrap-my-policy-harness
description: "Bare request to wrap a policy before it moves an arm (physical-ai-harness) versus robot-learning or robot-safety."
tags: [routing]
expected_outcome: "Expected physical-ai-harness. The request names no failure case, only the need to wrap a policy before it moves the arm, which is the runtime contract on the actuator path."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
Wrap my policy before it moves the arm.
