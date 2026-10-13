---
name: route-robot-command-gate
description: "Collision: vetting a list of commands before they are typed on a robot and its CAN bus (robot-command-gate agent) versus reviewing whether the code behind them is correct (robot-change-critic) or diagnosing a fault (robot-fault-hunter)."
tags: [routing]
expected_outcome: "Expected the Agent tool to be called with subagent_type robot-command-gate. The user pastes five concrete shell lines for a shared robot PC and its CAN bus and asks which are safe to run. Nothing is being diagnosed and no code is being judged. robot-change-critic reviews a patch and robot-fault-hunter plans a capture for an unknown fault; neither sorts commands by verdict."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Agent]
---
Before I sit down at the arm, can you vet these lines? The robot PC is shared with two other people and the arm's CAN bus is on can0. I want each line marked as safe to run, needs someone's approval, or not to be run at all:

1. candump can0 -L > /tmp/bus.log
2. cansend can0 001#0000000000000000
3. ssh robot-pc "echo restarting bridge -> $(date) && sudo systemctl restart arm_bridge"
4. ros2 topic hz /joint_states
5. rm -rf "$HOME/ws/build"

Give me the verdicts.
