---
name: route-advisor-computed-torque
description: "Single-skill routing: computed-torque versus PD with gravity compensation, from fundamentals."
tags: [routing]
expected_outcome: "Routes to robotics-advisor: choosing controller math from manipulator-dynamics fundamentals is method selection."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I'm working through manipulator dynamics for a controls course. For a two-link planar arm, when is computed-torque control actually worth it over PD with gravity compensation, and what exactly do I need to model for it to work?
