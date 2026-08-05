# Evaluation — iteration 1 (2026-08-05)

The first four skills were evaluated on realistic test prompts. Each case ran as two subagents on the same model (Sonnet): one following the skill (with-skill) and one without it (baseline), graded against 4-5 objective assertions per case. Since the runs were headless, the interactive AskUserQuestion gate was replaced with "write the options into the answer and stop".

## Summary

| Metric | With Skill | Baseline | Delta |
|--------|------------|----------|-------|
| Assertion pass rate | **100%** (17/17) | 83.8% (14/17) | +16.2pp |
| Mean time | 275s | 193s | +82s |
| Mean tokens | 130k | 112k | +18k |

Test cases: ① IK method selection for a 6-DOF spherical-wrist arm (`robotics-advisor`) ② ROS 2 servo driver architecture (`ros2-master`) ③ URDF explodes in Gazebo (`robot-arm`) ④ Servo gripper overheating (`robot-hand`).

## Observations

- **The IK case showed the clearest gap.** The with-skill run grounded its answer in the classic textbook treatment (citing §4.6 Pieper's solution), verified libraries with live search, and stopped at the option gate. The baseline cited no sources and jumped straight into unrequested implementation and benchmarking — exactly the behavior the skill is designed to prevent.
- **Gripper case**: both diagnosed stall current correctly, but the baseline omitted the explicit "never grip with bare position control" warning that the skill's Gotcha supplies.
- **The ROS 2 and URDF cases did not discriminate** — the baseline also passed every assertion. The base model is already strong there; the next iteration needs sharper assertions or harder prompts.

## Limitations

- One run per configuration — no variance estimate.
- The interactive loop (proceeding to the next decision after a choice) is not exercised by headless evaluation; it's validated through real use.
- Skills 5-7 (`robot-mobile`, `robot-fleet`, `robot-learning`) have not been evaluated yet.
