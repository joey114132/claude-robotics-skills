---
name: route-swarm-argos-aggregation
description: "Single-skill routing: decentralized aggregation and line formation for many e-puck-class robots."
tags: [routing]
expected_outcome: "Routes to robot-swarm: decentralized local-interaction rules and robustness to unit failure with many simple robots."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I want fifty e-puck-class robots in ARGoS to aggregate and then form a line using only local communication. What decentralized rules should I use, and how do I keep the collective working when some units fail?
