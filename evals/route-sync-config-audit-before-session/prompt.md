---
name: route-sync-config-audit-before-session
description: "Collision: comparing DDS profile, network interface binding and time sync across two hosts before a session (the robot-sync-config-auditor agent) versus a code-path audit (robot-audit-team) or an unattended diagnose-and-fix run (robot-autopilot)."
tags: [routing]
expected_outcome: "Expected none of robot-preflight-team, robot-audit-team or robot-autopilot to fire. Nothing is failing and no command, gain change or model copy is in play: the user wants host configuration (RMW and DDS profile, interface binding, time source) compared before a session, with read-only commands handed back. That is the robot-sync-config-auditor agent alone; robot-preflight-team would be the wrong winner because it owns a go/no-go sheet over commands, gains and model copies (see route-preflight-before-shared-robot-session, which has those and expects it). This runner does not record Agent or Task calls (graders on both tools saw 0 calls, 2026-10-13, evals/results/2026-10-13T00-34-36-039Z and later), so the case can only fail when a neighboring skill fires. It passes if nothing fires at all; it does not prove the agent was chosen."
max_turns: 4
timeout_seconds: 240
allowed_tools: [Read, Grep, Glob, Skill]
---
We have a robot PC and an operator laptop that will run one ROS 2 session together tomorrow. Nothing is broken at the moment. Before we start, check that both machines have the same RMW and DDS profile, that the profile binds to the network interface the robot link really uses (the laptop also has WiFi), and that they take time from the same source. The config files for both hosts and our troubleshooting notes are in this repo. Don't run anything on either machine. Give me the table of what matches and what doesn't, and the read-only commands I should run on each machine to confirm the rest.
