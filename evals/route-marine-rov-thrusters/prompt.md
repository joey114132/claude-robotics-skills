---
name: route-marine-rov-thrusters
description: "Single-skill routing: tethered ROV thruster allocation, depth rating and DVL navigation."
tags: [routing]
expected_outcome: "Routes to robot-marine: thruster layout and control allocation, depth rating, DVL navigation and tether failsafe are the water-environment vehicle problem."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I'm building a tethered ROV with six thrusters for 100 m depth. How should I do control allocation, what do I need for DVL-based station keeping without GPS, and what should happen if the tether is cut?
