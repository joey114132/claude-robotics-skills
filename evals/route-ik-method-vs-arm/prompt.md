---
name: route-ik-method-vs-arm
description: "Collision: choosing an IK method for a 6R arm, theory versus arm pipeline."
tags: [routing]
expected_outcome: "Expected robotics-advisor. robot-arm's own text says 'theory and method selection (which IK, which controller math) belongs to robotics-advisor', although robot-arm's frontmatter description lists 'IK solver choice'. Choosing between IK methods near singularities is method selection, not arm bring-up."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I'm choosing an IK approach for a 6R arm with a spherical wrist: closed-form, Jacobian pseudo-inverse, or damped least squares. Which one should I use for real-time teleop where I keep hitting wrist singularities, and why?
