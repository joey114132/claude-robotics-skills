---
name: physical-ai-harness
description: "Use when a learned model (VLA, diffusion or ACT policy, RL policy, learned planner) is about to drive, or already drives, a real robot's actuators through ROS 2: deploying a trained policy on hardware, reviewing a policy deployment, adding a safety wrapper, gate or fallback controller, or asking what must wrap a policy before it touches the robot. Audits whether the deployment holds the model to one contract across control, computing and communication (Projection, Isolation, Transfer) and writes a Harness Profile plus a gate node. Not for training, datasets or policy choice (robot-learning), standards and safety cases (robot-safety), or a perception model whose output a verified controller already bounds."
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
---

# Physical AI Harness

Act as the engineer who wraps a learned model before it is allowed to move hardware. robot-learning owns the decision to learn, the data, the training and the latency budget. robot-safety owns standards, the safety case and the independent protective layer. ros2-master owns QoS, lifecycle and executor mechanics. This skill owns the layer in between: the runtime contract a learned model is held to on the actuator path, and what happens when it breaks it.

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

## What makes a learned model different

A classical controller came with its bounds built in. Its output range was specified, its execution time had a closed-form bound, and its operating conditions were fixed at design time. A learned model provides none of these. Its output is a sample from a distribution, its inference time depends on the input, and its payload and cadence vary. One model on the control path therefore disturbs three axes at once: the trajectory (control), the executor schedule (computing) and the link (communication). Each lower layer guards only its own axis. A command can be stable, late and stuck behind a large frame all at once, and no single layer sees that the late stable command is now unsafe.

The harness holds the model to **three declarations as one contract**: an output region, an inference budget and an operating regime. It enforces them with three mechanisms that only work together. **Projection** gates each sample at publish time. **Isolation** gives the model one reservation covering its compute slot and its link window. **Transfer** hands authority to a pre-staged verified baseline when Projection keeps rejecting or the regime signal crosses its bound, and returns authority only on a positive signal. The framing is from a 2026 position paper with no experiments, so use its structure and measure your own numbers.

## The harness decision sequence

1. **Does this model need a harness at all?** Only when it is a real-time causal participant on the actuator path. A perception output that a verified controller re-bounds, a plan a human vets, or an offline planner already has a classical component holding the bounds. Say so and stop.
2. **Output region.** Per command topic: joint position, velocity and torque bounds, a step limit between consecutive samples, a workspace box, and a maximum staleness of the action stamp. Default to rejecting and holding the last admitted sample. Clamping is the exception and must be counted.
3. **Inputs.** List every observation stream the model reads, with a maximum gap for each. A model fed frozen frames emits in-range, on-time, wrong commands. Input staleness must revoke authority, not just log.
4. **Inference budget and isolation.** Measure WCET and rate on the deployment hardware. Put the model in its own process or callback group so an overrun cannot starve the control loop. Check the compute and link budget together, because a load that fits each axis alone can fail when both are claimed.
5. **Baseline and Transfer.** Pick the verified baseline (hold position, gravity compensation, teleop, a classical controller) and switch through lifecycle transitions: deactivate the policy, then activate the baseline. Trip on consecutive rejects or the regime signal. Return only after the model has run inside its bounds for a set time.
6. **One profile, one gate.** Put every threshold in one Harness Profile YAML beside the launch file and enforce it in one gate node between the model and the controller. Scattered thresholds fail the composition test even when each is right.
7. **Evidence.** Log one JSONL line per gate decision and ship a harness card (the profile enforced, measured inference time, reject rate) so two deployments can be compared on governance.

> See references/gate-template.md for the gate topology, the Harness Profile template and the gate node rules.

## Modern scan

**Live scan on every invocation.** Start from `references/landscape.md`, a dated snapshot in which every entry carries its source, then re-verify with fresh search before presenting: confirm that the entries you use still hold and look for newer options. When the live scan contradicts or postdates the snapshot, answer from the fresh finding. Write it back into `references/landscape.md`, bumping its Verified date, only when this skill directory is a git checkout that the user maintains; a marketplace install lives in a plugin cache that the next update overwrites.

## Gotchas

- **Output bounds alone pass a blind policy.** On a dual-arm teleoperation robot, a recording lost all four wrist cameras at once for about 24 s while live topics looked healthy before and after. A policy fed by those cameras would have kept publishing in-range actions from frozen frames. Only input staleness wired to Transfer catches that, so audit inputs first.
- **Clamping is not Projection.** Clamping a learned sample into range hides the drift Transfer needs to see, and the model keeps steering into the wall at the clamp. Reject, hold the last admitted sample and count it.
- **"No fault" is not a return signal.** A watchdog that clears on the first good sample makes the robot flap between policy and baseline every few seconds. Require the model to stay inside its bounds for a hold time, and re-seed the command from the measured pose before handing back.
- **Stopping publication is not a fallback.** A gate that just goes silent leaves the downstream controller holding its last target, which can sit at the lag limit from the real pose with a stiff gain still pushing. Transfer must command the baseline, and the controller needs its own command timeout for the case where the gate process dies.
- **Runtime parameter changes can widen the whole envelope.** Without ParameterDescriptor ranges or an on-set callback that validates, a single `ros2 param set` lifts the speed cap or disables the lag clamp. Bound every harness parameter and re-run the consistency checks on change.
- **The gate itself costs latency.** The per-sample check sits in the control path. Measure its cost on the target hardware at the real control rate before trusting it, and keep heavy checks (collision, learned OOD scores) off the per-sample path or give them their own budget.
- **A software harness is not the safety function.** It reduces risk, but drive-level limits, Safe Torque Off and the e-stop stay independent of it. A learned policy cannot be argued to a Performance Level, so design as if it will occasionally do the worst thing it can.
