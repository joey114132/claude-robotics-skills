---
id: 0001
title: Robots that must drive and manipulate have no owning skill
originator: robotics-radar coverage-gap audit, 2026-10-02
type: feature
status: draft
priority: med
tags: [coverage-gap, robot-mobile, robot-arm, robot-legged]
created: 2026-10-02
---

## What hurts

A robot that carries an arm on a moving base and must move while it manipulates (a wheeled manipulator, a humanoid on wheels) falls between skills. `skills/robot-mobile/SKILL.md` hands manipulators to `robot-arm`. `skills/robot-arm/SKILL.md` has no decision step for base and arm coordination, although its intro now claims "the base-arm coordination decisions". `skills/robot-legged/SKILL.md` owns only loco-manipulation on legs (step 6). A search of `skills/` for "mobile manipulat" on 2026-10-02 finds no decision guidance. The only hits are the `robot-arm` and `robot-mobile` division-of-labor lines and one `robot-learning` landscape entry about VLA fine-tuning.

Evidence the category is durable, fetched 2026-10-02: five or more independent groups, maintained software, and real hardware.

- `hello-robot/stretch_ros2` pushed 2026-09-15 and `stretch_ai` pushed 2026-07-02. The `stretch_ai` README says parts are "derived from the Meta HomeRobot project", and `home-robot` itself was last pushed 2024-06-08.
- `pal-robotics/tiago_robot` pushed 2026-04-24.
- `leggedrobotics/ocs2` pushed 2026-09-29. Its README lists "end-to-end MPC examples ... mobile manipulator".
- Boston Dynamics Spot arm docs: "The robot's base will move in response to the hand's position, allowing the arm to reach beyond its current workspace." (https://dev.bostondynamics.com/docs/concepts/arm/arm_concepts)
- Research: HoMMI "learns whole-body mobile manipulation directly from robot-free human demonstrations" (https://arxiv.org/abs/2603.03243), Mobile ALOHA (https://arxiv.org/abs/2401.02117), BiGym with "40 diverse tasks set in home environments" (https://github.com/NeuracoreAI/bigym, paper https://arxiv.org/abs/2407.07788), and `umi-on-legs` pushed 2026-07-20.

## What we want

A question such as "my wheeled arm has to pick from shelves, should the base stop first or move with the arm?" reaches a skill that answers with a verdict and the base-arm coordination decisions: whole-body versus base-then-arm, who owns the reaction wrench and the task priority, and how the navigation stack hands a pose to the arm. Success is observable. One new routing case and one new quality case in `evals/` pass for that skill, and the existing 30 routing cases still route as before.

## Out of scope

Legged loco-manipulation (stays in `robot-legged`), arm-only integration (stays in `robot-arm`), policies and datasets (stay in `robot-learning`), and commercial warehouse picking, which is a separate and weaker case. The existing Mobile ALOHA entry in `skills/robot-learning/references/landscape.md` and the ALOHA entries in `skills/robot-arm/references/landscape.md` stay where they are and get cross-references. The `## How to answer` blocks are not touched.

## Alternatives considered

A new skill, `robot-mobile-manipulation`, with a `SKILL.md` and a `references/landscape.md`. The lighter option is a base-arm coordination step in `robot-arm` plus a pointer in `robot-mobile`. Choose after checking whether the decisions fit in one more step without pushing `robot-arm` past 130 lines.

## If a skill is built

Routing edits: change the `robot-mobile` division-of-labor line to send "a base that carries an arm and must move while manipulating" to the new skill, add the same pointer to `robot-arm`, and point `robot-legged` step 6 at it for wheeled and humanoid-on-wheels cases. Consistency edits in the same commit: bump `plugin.json` to the next minor version, update the skill counts in `README.md` (badge, skills table), `assets/skill-map.svg`, `intent.md`, and both manifest descriptions, then run `scripts/check_sources.py`.

## Open questions

- The gotchas. `CLAUDE.md` requires real, expensive, domain-specific traps. None have been confirmed against a source or hardware yet, so ship only the ones that are.
- Whether the HoMMI paper names a venue. The audit could not find one, so the landscape entry carries no venue until a source shows it.
- Whether the lighter `robot-arm` option is enough. Check by writing the two eval cases first and seeing whether `robot-arm` already answers them well.
