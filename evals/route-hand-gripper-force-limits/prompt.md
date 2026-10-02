---
name: route-hand-gripper-force-limits
description: "Single-skill routing: choosing a hand type and limiting grip force on servo fingers."
tags: [routing]
expected_outcome: "Routes to robot-hand: choosing the hand type and controlling grip force and contact is everything from the flange outward."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
We need an end effector that can pick up wine glasses and also screwdrivers. Should I go with parallel-jaw, underactuated, or a full dexterous hand? And how do I limit grip force on servo-driven fingers so they don't crush the glass?
