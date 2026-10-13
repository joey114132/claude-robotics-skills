---
name: route-preflight-before-shared-robot-session
description: "Collision: a go/no-go review before a session on a shared robot that combines planned commands, a gain change, several model copies and two hosts (robot-preflight-team) versus a code-path audit (robot-audit-team) and an unattended diagnose-and-fix run (robot-autopilot)."
tags: [routing]
expected_outcome: "Expected robot-preflight-team. The user has no defect to fix and no code path to audit: they want one verdict on whether tomorrow's session on a shared arm is safe to start, covering the commands they plan to run, a gain change, two copies of the arm model and the config on two machines. robot-audit-team covers a code audit and robot-autopilot covers diagnose-and-fix; neither produces a go/no-go sheet with the commands left for the user."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
Tomorrow morning I'm starting a session on our shared 6-axis arm. Before I touch it I want one go or no-go from you, with anything blocking spelled out. The plan: raise the position gain on joints 2 and 3 and switch to the new controller, restart the bridge on the robot PC, and send a few test frames on the CAN bus. The arm model lives in two copies (my laptop checkout and the robot PC), and the two machines are supposed to share the same DDS profile and time source. Don't run anything on the robot yourself; list the commands I have to run and tell me which of them are risky.
