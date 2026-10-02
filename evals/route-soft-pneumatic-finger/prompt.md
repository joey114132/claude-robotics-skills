---
name: route-soft-pneumatic-finger
description: "Single-skill routing: modeling and sensing a fiber-reinforced pneumatic bending actuator."
tags: [routing]
expected_outcome: "Routes to robot-soft: a bending elastomer actuator whose shape is part of the state, with its modeling, sensing and fabrication choices."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I'm making a fiber-reinforced silicone pneumatic bending actuator. Should I model it with constant curvature, Cosserat rod, or FEM, how can I embed a stretchable sensor to estimate its curvature, and what molding approach works for the chambers?
