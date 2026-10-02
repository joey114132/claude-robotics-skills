---
name: route-gripper-selection-vs-arm
description: "Collision: choosing a gripper type for a UR arm, hand versus arm."
tags: [routing]
expected_outcome: "Expected robot-hand. robot-hand 'owns everything from the flange outward: choosing the hand', and robot-arm's own text limits it to the arm pipeline. The arm's job is only to place the tool frame."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I have a UR10e at a pick station handling mixed items: boxed goods, bagged snacks, and the occasional bottle. What kind of gripper should I put on it: parallel-jaw, vacuum, or something underactuated?
