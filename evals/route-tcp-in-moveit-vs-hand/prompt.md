---
name: route-tcp-in-moveit-vs-hand
description: "Collision: setting up a gripper TCP and collision model in MoveIt 2, arm versus hand."
tags: [routing]
expected_outcome: "Expected robot-arm. robot-hand's text says 'Arm-side integration (mounting, TCP in the planning stack) stays with robot-arm', even though robot-hand's frontmatter description lists 'tool-center-point setup'."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I bolted a two-finger gripper onto my Franka flange. In MoveIt 2, how should I set the TCP and tool frame and add the gripper to the planning scene and collision model, so plans account for the mounting offset?
