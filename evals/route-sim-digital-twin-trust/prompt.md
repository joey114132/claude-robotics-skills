---
name: route-sim-digital-twin-trust
description: "Single-skill routing: calibrating a digital twin and measuring the sim-to-real gap."
tags: [routing]
expected_outcome: "Routes to robot-sim: simulator fidelity, system identification and sim-to-real validation are what the simulation skill owns."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I'm building a digital twin of our conveyor cell. How do I calibrate friction and actuator models so the simulation predicts the real hardware, how do I measure the sim-to-real gap, and when can I trust the simulator's answers?
