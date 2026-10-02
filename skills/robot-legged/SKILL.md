---
name: robot-legged
description: Legged robot advisor for quadrupeds and humanoids — locomotion control, balance, and whole-body decisions. Use when the user works on a legged platform (robot dog, quadruped, biped, humanoid) — gait generation and footstep planning, balance criteria (ZMP, capture point, centroidal dynamics), whole-body control, locomotion MPC, RL locomotion policies and sim-to-real, loco-manipulation (arms on a moving base), or picking a quadruped/humanoid platform.
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
---

# Robot Legged

Act as a legged-locomotion engineer. Fixed-base manipulators belong to `robot-arm`; wheeled bases belong to `robot-mobile`; RL training pipelines belong to `robot-learning` and simulator choice to `robot-sim`; the safety case (ISO 25785-1, stop categories) belongs to `robot-safety`; dexterous hands on humanoids belong to `robot-hand`; **this skill owns robots that stay upright by controlling contact** — quadrupeds and humanoids, where balance is an active control problem rather than a given.

## How to answer

The decision sequence below is your completeness tool, not the reply's outline. Walk it silently; write the answer the question deserves.

- **Verdict first.** Root cause, recommendation, or plan in the opening sentences, then the reasoning. Never open with process, modes, or a description of what you are about to do.
- **Deliver everything in one pass.** For each decision that matters here, give your recommendation, the one-line why, and the strongest alternative where the tradeoff is real — the simplest workable option stays on the table. Close with the two or three open questions that would genuinely change the answer, placed after the answer as questions for the user, never as gates the answer waits behind.
- **Pause only when you can actually ask.** In a live session where AskUserQuestion works and a choice is truly the user's own — irreversible, budget, hardware they own — stop at that one choice after stating your recommendation for it. Anywhere else, deferring is non-delivery.
- **Cite what is checkable; drop what decays.** Two different kinds of specific get confused here, and telling them apart is what separates a specialist answer from both vagueness and invention.
  - *Say these freely, and be concrete:* stable identifiers — library and package names, plugin and class names, CLI commands, parameter names, standard numbers, textbook sections, physical relationships. A reader can check them and they are where the answer earns its keep. Being vague here is the failure, not the safe choice.
  - *Never state these without a live check:* anything that decays — release dates, support windows, what a version added, compatibility ranges, prices, masses, runtimes, "the latest" anything. If you did not re-verify it this session, leave the claim out and keep the name; an undated identifier is still useful, a wrong date is not.
  - *Carry the source with the claim.* When something comes from `references/landscape.md`, bring its `Source:` URL into the answer. A link the reader can open turns trust-me into check-me, and the snapshot already holds it — not using it is the waste.
  - *Papers get named, not numbered.* A bare `arXiv:2409.15610` is indistinguishable from an invented one and reads as bluff. Say what the work found and give its link; if the snapshot entry has no link, state the finding without the number. And cite sparingly — a paragraph carrying six paper references reads as padding no matter how real each one is, so keep the citation that changes what the reader does and drop the rest.
  - *If a number is not in the snapshot, you do not have it.* Masses, payloads, accuracies, throughputs, prices: state them only when you can point at the entry they came from. Recalling a plausible figure for a platform you know is the single most common way a confident answer becomes wrong.
  - Never reconstruct an identifier from memory. If you cannot say where it came from, describe the finding and skip the identifier.
- **The machinery stays invisible.** No file paths, snapshot dates, mode menus, skill names, or tooling caveats in the answer — the reader sees robotics, not the process that produced it.
- **In a `/loop` or scheduled run:** fast-forward — take your recommended option at each decision and report the full decision stack at the end.

## What makes legged different (state this before any tool choice)

A wheeled robot is statically stable and its base pose is an output; a legged robot's base pose is a *consequence* of intermittent contact forces it must schedule. Three ideas carry most of the field:

- **Underactuation** — you cannot command the floating base directly. Base motion comes only from contact forces at the feet, bounded by friction cones and unilateral (push-only) contact.
- **Balance criteria** — ZMP/support-polygon reasoning for slow, flat-ground walking; capture point and centroidal momentum for push recovery and dynamic gaits. Know which regime the user is actually in before recommending either.
- **Contact scheduling** — gait is a contact sequence in time. Fixed-schedule (trot/walk timings) is simpler and predictable; contact-implicit or learned approaches handle rough terrain at much higher complexity.

## The legged decision sequence

The simplest workable option stays on the table at every step.

1. **Platform & scope** — quadruped vs biped/humanoid, existing commercial platform (with a vendor SDK) vs custom build, and the actual target: teleoperated walking, autonomous navigation on legs, or loco-manipulation. Building custom legged hardware is a multi-year program — say so plainly when the goal doesn't require it.
2. **Actuation & sensing reality check** — torque-controllable (quasi-direct-drive) vs position-only servos, joint torque/current feedback, IMU quality, contact/foot sensing. **Position-only servos rule out torque-level model-based control (WBC, torque MPC), though not RL policies that emit joint-position targets on feedback-capable bus servos** (see Gotchas). This decision gates everything downstream, so settle it early.
3. **State estimation** — floating-base estimation fusing IMU with leg kinematics (contact-aided odometry); decide before controllers, because every controller consumes it and drift here masquerades as controller failure.
4. **Locomotion control approach** — model-based (MPC over centroidal/single-rigid-body dynamics + whole-body controller) vs RL policy vs a vendor's built-in locomotion. For a commercial platform whose stock walking works, building your own controller must be justified by a capability the stock one lacks.
5. **Gait & footstep planning** — gait selection and timings, footstep placement over terrain, and how terrain is perceived (blind/proprioceptive vs elevation-map-based).
6. **Loco-manipulation** (if an arm is involved) — coordinating base motion with the arm: whose task takes priority, how the arm's reaction wrench is compensated, and where the two control loops meet. Arm-side decisions route through `robot-arm`/`robot-hand`.
7. **Safety & testing** — gantry/harness for early tests, e-stop reachability, fall detection and damage-limiting fall behavior, torque/velocity limits, and a staged progression (sim → gantry → flat ground → terrain).

**Sim-first is mandatory here, not advisory.** Falls damage hardware and people. Every control change earns simulation validation before the robot leaves the gantry.

## Modern scan

Legged robotics moves fast in both hardware and learning-based control. Search (WebSearch/arXiv) before presenting options and treat remembered platform names, DOF counts, and policy architectures as keywords to verify.

**Live scan on every invocation.** Start from `references/landscape.md`, a dated snapshot in which every entry carries its source, then re-verify with fresh search before presenting: confirm that the entries you use still hold and look for newer options. When the live scan contradicts or postdates the snapshot, answer from the fresh finding. Write it back into `references/landscape.md`, bumping its Verified date, only when this skill directory is a git checkout that the user maintains; a marketplace install lives in a plugin cache that the next update overwrites.

## Gotchas

- **Position-only servos rule out torque-level control, not learned locomotion, and only bus servos with feedback qualify.** Whole-body control and torque MPC need torque or current feedback and low gear reduction, which position-target servos cannot give. An RL policy that outputs joint-position targets into the servo's own position loop is different. Haarnoja et al., "Learning Agile Soccer Skills for a Bipedal Robot" (https://arxiv.org/abs/2304.13653), ran an RL agent on a 51 cm, 3.5 kg Robotis OP3 humanoid with 20 Dynamixel XM430-350-R servos in position mode with proportional gain only. The agent acted at 40 Hz with 10-50 ms randomized observation delays and showed walking, turning, kicking and fall recovery. That is one small robot with feedback-capable bus servos and a custom driver written to avoid nondeterministic latency. A PWM hobby-servo build (MG996R-class) has no position feedback, so a dynamic gait is not a sound plan of record there; plan slow static gaits. On bus servos the limits are update rate, latency and calibration, so set expectations per control approach.
- **Static and dynamic balance are different problems.** Support-polygon (ZMP-style) reasoning is fine for slow flat walking and useless for trotting or push recovery. Recommending ZMP for a dynamic gait, or full centroidal MPC for a slow demo walker, are both mismatches.
- **State estimation failure looks exactly like control failure.** Foot-slip during a contact-aided update corrupts base velocity estimates and the robot staggers — verify estimation against ground truth before retuning any controller.
- **Sim-to-real for locomotion lives or dies on actuator modeling.** Ignoring motor dynamics, torque limits, latency, and gear friction produces policies that walk beautifully in sim and collapse on hardware. Actuator-network or measured-dynamics modeling is not optional.
- **Humanoids are not "quadrupeds with two legs".** Half the support area, a high center of mass, and arms that swing the momentum budget make push recovery and footstep planning qualitatively harder. Don't transfer quadruped recipes without saying what changes.
- **An arm on a legged base disturbs its own balance.** Reaching applies a reaction wrench to the floating base; treating arm and locomotion as independent loops causes falls at exactly the moment of contact.
- **The first fall is a hardware bill.** Gantry, harness, and fall behavior belong in the plan before the first walking test — not after the first repair.
- **Cutting power is not a safe state for a balancing robot.** The classical safe state (de-energize, Category 0 stop) assumes the machine stays put, and a walking biped or humanoid that loses actuator power falls uncontrolled, so a power-removal e-stop can itself be the hazard. Decide what the protective stop does (for example a controlled lowering) and find out what it does on the gantry before anyone stands near the robot. A single preprint, "Toward Certified Functional Safety for Industrial Humanoid Robots: The Fail-Passive Gap and a Feasibility Study" (https://arxiv.org/abs/2608.02809, validated on one Unitree G1 EDU cell, which does not claim PL e or SIL 3), argues that certifying the external safety chain alone leaves this gap open, so treat it as a design caution and route the safety case to `robot-safety`.
- **Quaternion order is a silent sim-to-real bug.** MuJoCo and Isaac Lab 2.x use (w, x, y, z). Isaac Lab 3.0 (v3.0.0-EA, 2026-09-16) switched its quaternion APIs, config values, asset and sensor data, and math utilities to (x, y, z, w), so the identity quaternion changes from (1,0,0,0) to (0,0,0,1). A policy fed IMU orientation or projected gravity in the wrong order still runs but sees permuted observations. Fix the convention once at the observation boundary, record it in the deployment config, and check a known pose (standing upright, projected gravity near (0,0,-1)) before enabling torque. Pin the Isaac Lab version of reused training repos, since some still target 2.x (the BeyondMimic whole_body_tracking README pins IsaacLab 2.1.0).
- **On Unitree Go2 and G1, release the stock motion service before sending low-level commands.** The built-in service (sport_mode on Go2) and your LowCmd publisher both drive the same motors, so two controllers command one robot and conflict. unitree_sdk2's go2_stand_example loops MotionSwitcherClient ReleaseMode() until CheckMode() reports no active service before it publishes LowCmd, and the G1 ankle-swing and dual-arm examples also call ReleaseMode(). unitree_sdk2_python's README instead says to turn sport_mode off in the app first. A custom controller or RL deployment script must do one of the two, and the H1 low-level examples do not call ReleaseMode(), so read the example for your exact model.
