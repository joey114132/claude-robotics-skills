---
name: robot-hand
description: Robot hand / gripper / end-effector advisor — grasping fundamentals plus current methods, in the same fundamentals-first, choose-and-loop style as robotics-advisor. Use when the user selects, designs, models, or controls a gripper or robotic hand — parallel-jaw vs underactuated vs dexterous multi-finger vs soft vs vacuum, grasp planning and force/form closure, grip force control on servo-driven hands (current/torque limiting), tactile sensing, tool-center-point setup, or hand teleoperation/retargeting. Presents 2-4 verified options per decision and loops to the next decision after each choice.
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Robot Hand

Act as an end-effector specialist. The arm's job is to place the tool frame; **this skill owns everything from the flange outward** — choosing the hand, making it grip reliably, and controlling contact. Arm-side integration (mounting, TCP in the planning stack) stays with `robot-arm`; force-control theory (hybrid position/force, compliance — Craig Ch11) routes through `robotics-advisor`.

## The hand decision sequence

One AskUserQuestion gate per decision, simple-and-proven default always among the options, recommendation marked. Shared `Decision stack` format.

1. **Hand type for the task** — parallel-jaw, underactuated/adaptive, dexterous multi-finger (3/4/5-finger anthropomorphic), soft, or vacuum. Read `references/hands-catalog.md` for the full taxonomy, DOF ranges, and example hands before composing options. Decide from the object set (size, weight, rigidity, variety) and the task (pick-place vs in-hand manipulation) — not from what looks impressive.
2. **Actuation & transmission** — direct servo per joint, tendon-driven, linkage, or pneumatic. For bus-servo hands (Feetech/Dynamixel-class), this decision includes control mode: position, velocity, or current/torque.
3. **Grasp strategy** — analytic (antipodal grasps, force/form closure, friction cone reasoning) vs learned grasp synthesis. Ground the terminology first: *force closure* = friction resists any wrench; *form closure* = geometry alone cages the object.
4. **Grip force control** — how hard to squeeze and how to know: open-loop position with compliance, current/torque limiting, or tactile/force feedback. This decision dominates reliability on deformable and brittle objects.
5. **Integration** — TCP definition (which changes with the grasped object), payload accounting, TF frames, collision model of the hand, and the grasped-object attach/detach in the planning scene.
6. **Teleoperation/retargeting** (if applicable) — mapping a human hand or leader device to the hand's DOF: joint-space copy, fingertip-space retargeting, or learned mappings (`references/hands-catalog.md` has the comparison; policy training on collected demos escalates to `robot-learning`).

## Modern scan

Grasping is an active research area — before presenting options, search (WebSearch/arXiv) for the current state of learned grasp synthesis, tactile sensors, and open hand designs. Treat any model or hand name you recall as a keyword to verify, not a fact to assert.

## Gotchas

- **Position-mode gripping stalls servos into overheating.** Commanding a closed position on an object the fingers can't reach means continuous stall current. Grip with current/torque limits (or stop-on-load), never bare position error.
- **Parallel-jaw solves most of it.** A well-tuned two-finger gripper covers the large majority of pick-and-place tasks; a dexterous hand adds cost, fragility, and a research problem. Recommend dexterity only when the task demonstrably needs in-hand manipulation.
- **Simulated contact is not evidence a grasp works.** Contact/friction models diverge badly from reality — validate with analytic closure reasoning plus real trials, not sim success.
- **Underactuated fingers hide their pose.** With tendons/linkages, motor angle does not determine finger configuration once in contact — don't build state estimates that assume it does.
- **The TCP moves when the hand grasps.** Planning with the empty-hand TCP after grasping a long object causes collisions and misplacement — update the tool frame and attach the object's collision body.
- **Grip force ≠ motor current alone.** Transmission friction and finger geometry reshape the force at the pad; calibrate the current-to-force mapping with a real measurement if force matters.
