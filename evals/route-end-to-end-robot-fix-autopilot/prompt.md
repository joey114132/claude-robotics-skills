---
name: route-end-to-end-robot-fix-autopilot
description: "Collision: a one-shot request to diagnose, fix and test a robot teleoperation bug unattended (robot-autopilot) versus a read-only audit of the same command path (robot-audit-team)."
tags: [routing]
expected_outcome: "Expected robot-autopilot. The user states the symptom once and asks for the cause found, a tested patch written, and the commands for the real robot handed back to run themselves, with no questions in between. robot-audit-team's own text covers a read-only audit with blind verification and no fixes."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
Our dual-arm teleoperation bridge lets the follower arm jerk toward the last pose whenever a wrist camera feed freezes for a second or two. The repo is checked out here. Find the cause, fix it with a test that fails before the fix and passes after, and run the whole thing without stopping to ask me anything. Anything that has to run on the real robot, like restarting the bridge or switching controllers, don't run it, just give me the exact commands at the end.
