---
name: route-surgical-safety-case-vs-safety
description: "Collision: safety case for a teleoperated surgical robot, medical versus industrial safety."
tags: [routing]
expected_outcome: "Expected robot-medical. Its text owns what changes when the workspace contains a human body: the intended-use claim, the standards that follow from it, and the evidence for the safety case. It also says industrial functional safety (ISO 10218, safety PLCs) is 'a different regime from the medical one' that belongs to robot-safety only for the industrial side."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
We're building a teleoperated surgical robot with a remote-center-of-motion mechanism. How do we build the safety case, and which standards and regulatory route apply to get it cleared for patient use?
