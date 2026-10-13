---
name: route-model-drift-auditor
description: "Agent routing: comparing several copies of one robot model for silently diverging limits, inertias or structure goes to robot-model-drift-auditor, not to a skill."
tags: [routing]
expected_outcome: "Expected the robot-model-drift-auditor subagent. The user has the same arm URDF in a laptop checkout, a robot PC checkout and an installed share directory, and wants every disagreement in joint limits listed read-only, with no model fixed. That is the agent's one-lens comparison job, so the Agent tool should be called with that subagent_type."
max_turns: 4
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Agent, Skill]
---
The same 6-DoF arm model lives in three places here: my checkout at /work/laptop/arm_description, a copy of the robot PC checkout at /work/robot_pc/arm_description, and the installed share directory at /work/install/share/arm_description. Someone tightened an effort limit on one of them and I think the others drifted. List every joint where the velocity or effort limits differ between the three copies, with the file and line for each value. Don't change any file, just report.
