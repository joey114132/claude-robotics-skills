---
name: route-legged-biped-balance
description: "Single-skill routing: biped walking control with ZMP versus whole-body MPC."
tags: [routing]
expected_outcome: "Routes to robot-legged: gait generation, ZMP and capture-point balance criteria and whole-body control are contact-balancing problems."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I'm writing the walking controller for a small biped. Should I use ZMP preview control on a linear inverted pendulum model, or go to whole-body MPC? Which balance criteria matter for recovering from a push?
