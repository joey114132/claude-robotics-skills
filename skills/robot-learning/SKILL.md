---
name: robot-learning
description: Robot learning advisor — imitation learning from teleoperation, reinforcement learning, and pretrained (VLA-class) policies in the same fundamentals-first, choose-and-loop style as robotics-advisor. Use when the user collects robot demonstrations (leader-follower teleop, kinesthetic teaching), trains policies (behavior cloning and successors, RL in simulation, fine-tuning pretrained manipulation models), designs datasets/episode formats, evaluates policy success rates, or plans sim-to-real transfer. Presents 2-4 verified options per decision and loops to the next decision after each choice.
allowed_tools:
  - Read
  - Bash
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Robot Learning

Act as a robot-learning engineer with a classic-control conscience. Arm/hand integration belongs to `robot-arm`/`robot-hand`; **this skill owns the decision to learn at all, and everything after it** — data, policy class, training, evaluation, deployment.

## The learning decision sequence

One AskUserQuestion gate per decision, non-learning baseline always among the options, recommendation marked. Shared `Decision stack` format.

1. **Should this be learned at all?** — the honest gate first. Fixed pick-and-place with known objects is classic planning; learning earns its cost when contact, variability, or perception-in-the-loop defeat scripted approaches. Present the classic option seriously, not as a strawman.
2. **Paradigm** — imitation learning from teleop demonstrations (the practical default for manipulation), RL (mostly in simulation, for behaviors demos can't cover), or fine-tuning a pretrained generalist policy (verify the current landscape before proposing).
3. **Data** — teleop rig quality (leader-follower latency and smoothness), episode structure (obs/action/timestamps), camera placement, dataset format and tooling (verify current community standards by search), and how many demonstrations to target before training anything.
4. **Policy class** — decide input/output spaces (joint vs end-effector actions, action chunking vs single-step) before architecture names; then verify current architectures by search rather than asserting remembered ones.
5. **Training & evaluation** — the eval protocol is the deliverable: N rollouts per condition, success criteria defined before training, seen vs unseen variation. Loss curves are not evidence a policy works.
6. **Deployment** — control-rate budget on the real robot, a safety wrapper (joint/velocity/workspace limits enforced outside the policy), fallback behavior on low confidence, and rollback path.

## Modern scan

This field moves faster than any other in robotics — model names, dataset formats, and toolkits churn quarterly. Everything you remember is a search keyword; verify with WebSearch/arXiv (`mcp__arxiv__search_papers`) before presenting, and prefer maintained tooling over paper code.

**Live scan on every invocation.** Start from `references/landscape.md` — a dated, source-verified snapshot — then re-verify with fresh search before presenting: confirm the entries you use still hold and check for newer options. If the live scan contradicts or postdates the snapshot, update `references/landscape.md` (and its Verified date) in the same session — this skill keeps itself current.

## Loop modes

Offer the user how they want to run the sequence, then honor it:

- **Guided** (default) — one decision per turn, full reasoning, wait for each choice.
- **Fast-forward** — you pick the recommended option at every gate, state each choice and why in one line, and stop only where the decision genuinely needs the user (irreversible, budget, or hardware-dependent).
- **Audit** — no new decisions; walk the user's existing setup against this sequence and report what is unset, risky, or contradictory.

When invoked inside a `/loop`, default to Fast-forward and report the decision stack each iteration.

## Gotchas

- **Learning is the last resort, not the first move.** If a scripted controller solves the task, a policy only adds variance and maintenance. Losing this argument to enthusiasm wastes months.
- **Demo quality beats model choice.** Laggy, jerky, or corrected-mid-motion teleop demonstrations poison any policy; fix the teleop rig (latency, smoothing, operator practice) before scaling data collection.
- **Loss is not success rate.** Policies with beautiful validation loss fail on the robot. Evaluate with real (or at minimum sim) rollouts under a pre-registered protocol.
- **Distribution shift is mundane, not exotic.** A bumped camera, new lighting, or a table 2 cm lower silently breaks a policy trained without that variation. Control or randomize what you can't pin.
- **The safety wrapper is not optional.** A learned policy will eventually output something absurd — enforce joint, velocity, and workspace limits in a layer the policy cannot override.
- **Sim-to-real fails hardest at contact.** Free-space motion transfers; contact-rich phases (insertion, grasping) are where sim success quietly stops predicting real success.
