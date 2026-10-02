---
name: route-field-rtk-row-following
description: "Single-skill routing: RTK/NTRIP dropout under a tree line for a weeding robot."
tags: [routing]
expected_outcome: "Routes to robot-field: RTK/GNSS failure modes, NTRIP corrections and crop-row following are absolute positioning and connectivity problems that appear when the robot leaves the building."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
Our weeding robot loses its RTK fix under the tree line at the edge of the field and the row following drifts for a few meters. Corrections come over NTRIP on a cellular modem. What should we change so it degrades gracefully instead of wandering?
