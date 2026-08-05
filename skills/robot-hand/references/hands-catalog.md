# Hand & Gripper Catalog — taxonomy, dexterous techniques, retargeting

Reference for `robot-hand` decision 1 (hand type) and decision 6 (teleop/retargeting). Named products/models are **search keywords to verify at use time**, not asserted facts — availability, DOF counts, and prices change.

## Taxonomy — from simplest to most dexterous

| Type | Actuated DOF (typical) | Strengths | Costs | When it wins | Examples (verify) |
|------|------------------------|-----------|-------|--------------|-------------------|
| Vacuum / suction | 0–1 | Flat/smooth surfaces, speed, simplicity | Needs sealable surfaces, compressor | Bin picking of boxes, glass, sheets | Piab/Schmalz-style cups, foam multi-cup arrays |
| Parallel-jaw (2-finger) | 1 | Reliable, cheap, analyzable, easy force control | Object size range limited by stroke | Most pick-and-place; the default answer | Robotiq 2F-85/140, servo-driven hobby grippers |
| 3-finger adaptive | 2–4 | Centering, round objects, power grasps | Bulkier, slower | Cylinders, variable object sizes | Robotiq 3-Finger, BarrettHand-class |
| 4-finger dexterous | 12–16 | In-hand manipulation research, tool use | Cost, fragility, control complexity | Research: regrasping, finger gaiting | Allegro Hand, LEAP Hand (open-source, low-cost) |
| 5-finger anthropomorphic | 15–24+ | Human tool/environment compatibility, teleop naturalness | Highest cost & maintenance; tendon wear | Humanoid platforms, prosthetics research, human-tool tasks | Shadow Dexterous Hand, Schunk SVH, Inspire RH56-class, open-source designs |
| Underactuated / adaptive | few motors, many joints | Passive shape conformity, robust grasps cheaply | Finger pose unobservable, limited precision | Grasping varied objects without sensing | Yale OpenHand-style, spring-linkage designs |
| Soft / compliant | continuum | Delicate & irregular objects, food | Low precision, hard to model | Food handling, fragile items | Festo-style pneumatic fingers, silicone jamming grippers |

Selection rule of thumb: climb this table only when the task demonstrably defeats the row above. A 5-finger hand on a pick-and-place task is a maintenance bill, not a capability.

## Grasp fundamentals (terminology to ground first)

- **Power vs precision grasp** — palm-enclosing force vs fingertip control; the classic grasp-taxonomy axis (Cutkosky taxonomy — search "GRASP taxonomy" for the modern catalog).
- **Force closure / form closure** — friction-dependent restraint vs pure geometric caging.
- **Antipodal grasp** — two opposing contacts through the object's friction cones; what parallel-jaw planning actually computes.
- **Grasp wrench space** — the set of wrenches a grasp can resist; the analytic quality measure behind "is this grasp stable".

## Dexterous manipulation techniques (search directions)

- **In-hand manipulation** — reorienting without releasing: finger gaiting (sequential contact switching), rolling, sliding, pivoting against gravity.
- **Learned dexterity** — RL/IL policies for in-hand reorientation and contact-rich skills; verify the current state via arXiv before citing capabilities.
- **Tendon vs linkage vs direct drive** — tendon: remote actuation, compact fingers, elasticity/wear; linkage: robust, precise, bulkier; direct: simple, heavy fingers.
- **Tactile sensing** — fingertip vision-based sensors (GelSight-class), magnetic/capacitive arrays, joint-current proprioception as the zero-cost fallback.

## Teleop retargeting (human hand → robot hand)

- **Joint-space copy** — only for kinematically similar hands (5-finger anthropomorphic); simple, but transmits human tremor.
- **Fingertip-space retargeting** — match fingertip positions via IK; the standard for dissimilar kinematics (human → 4-finger).
- **Learned retargeting** — optimization/network mappings trained per hand pair; search current methods before proposing.
- Input devices: vision-based hand tracking, gloves, leader hands (miniature replicas) — leader-follower gives the cleanest force/latency behavior for data collection.

## Servo-driven hands specifically (Feetech/Dynamixel-class)

- Grip with **current/torque limit or stop-on-load** — never bare position (see SKILL.md Gotchas).
- Budget one bus per hand when finger count is high — a 15+ servo daisy-chain at high polling rates saturates half-duplex TTL buses; verify bus bandwidth against desired control rate.
- Thermal duty cycle matters more than peak torque for sustained grasps — check stall specs against hold-time requirements, and prefer mechanically self-locking (worm/linkage) designs for long holds.
