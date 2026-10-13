---
name: route-gain-change-gate
description: "Collision: a request to confirm a joint gain change was simulated and is safe to apply on the robot (robot-gain-change-gate agent) versus asking for gain values (robot-arm), a code review of the diff (robot-change-critic) or a verdict on the commands themselves (robot-command-gate)."
tags: [routing]
expected_outcome: "Expected the robot-gain-change-gate subagent. The user already has new gains, a simulation log and a rollback plan and wants a go or no-go on applying them, which is an evidence check. Choosing gains belongs to robot-arm and reviewing a code diff belongs to robot-change-critic."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Agent, Skill]
---
I changed the joint 2 and joint 3 position gains in config/gains.yaml (the old values are in config/gains.yaml.bak). I ran a simulation last week and the log is in sim_runs/gain_test.log. Before I apply this on the real arm, check whether the change is actually backed by that run, whether my acceptance criteria and rollback are in place, and tell me BLOCK or PASS. Don't suggest different gains and don't apply anything.
