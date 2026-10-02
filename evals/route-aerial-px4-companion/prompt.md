---
name: route-aerial-px4-companion
description: "Single-skill routing: PX4 offboard companion computer with failsafe design."
tags: [routing]
expected_outcome: "Routes to robot-aerial: a drone with an autopilot, offboard companion computer and failsafes is a vehicle that stays up only while actively controlled."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I'm putting a Jetson Orin NX on a quad that runs PX4 on a Pixhawk 6C. The Jetson will stream velocity setpoints in offboard mode. What do I have to get right so the vehicle doesn't fall out of the sky if the Jetson hangs mid-flight, and how should I set the failsafes?
