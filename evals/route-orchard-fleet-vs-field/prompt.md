---
name: route-orchard-fleet-vs-field
description: "Collision: coordinating twelve orchard machines, fleet coordination versus outdoor robotics."
tags: [routing]
expected_outcome: "Expected robot-fleet. robot-field's text routes 'multi-machine coordination to robot-fleet', and robot-fleet 'owns everything that only exists because there is more than one robot: coordination, contention'. The outdoor setting does not change that."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
We run twelve autonomous platforms in one orchard, with rows 4 m apart, shared headland turning lanes, and a single charging dock. How do we deconflict the headlands, allocate rows to machines, and handle one machine dying mid-row, from the coordination side?
