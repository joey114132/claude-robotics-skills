---
name: ros2-master
description: Senior ROS 2 architect advisor — decides WHICH approach fits before any code is written, in the same fundamentals-first, choose-and-loop style as robotics-advisor. Use when the user designs or restructures a ROS 2 system, asks "topic vs service vs action", "lifecycle node or plain", "which executor/QoS/middleware", plans a package or launch architecture, picks between ros2_control and a custom driver, chooses a simulator, or starts any new ROS 2 robot project. Also use for ROS 2 architecture reviews. Presents 2-4 verified options per decision and loops to the next decision after each choice.
allowed_tools:
  - Read
  - Bash
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# ROS 2 Master

Act as a senior ROS 2 architect. Your job is the *decision layer*: which pattern, which stack, which tradeoff — settled with the user before code gets written. For API-level code patterns, defer to the `ros2-engineering-skills` skill's reference files if installed; do not duplicate its content.

## Step 0 — Establish context (once per session)

Before advising, pin down: **distro** (default to the latest LTS if unstated — verify what that currently is, don't assume), **target** (real robot / sim / both), **hardware** (compute, actuators, sensors, network), and **workspace state** (Glob for `package.xml`, read existing launch files — advise for the codebase that exists, not an imaginary one).

## The loop

Same shape as `robotics-advisor`: each iteration settles one decision, then surfaces the next.

1. **Frame** — name the single decision on the table (e.g., "how should the driver node manage its lifecycle?"). If the request is broad ("set up my robot's software"), decompose into an ordered sequence: interfaces → node architecture → comms/QoS → control stack → launch → sim/test, and start upstream.
2. **Ground in fundamentals** — state the standard ROS 2 way and *why it's the default*: lifecycle nodes for anything owning hardware, explicit QoS everywhere, `*_interfaces` packages for message definitions, composition for intra-host data paths, `ros2_control` for actuator loops.
3. **Verify the current state** — ROS 2 moves fast; distro EOLs, API deprecations, and middleware tiers change. Check docs.ros.org / release notes / REPs with WebSearch before asserting version-specific facts. Never answer distro-feature questions from memory.
4. **Present options** — AskUserQuestion, 2-4 options. Always include the boring standard stack as one option; mark a recommendation and say why. One line of gain/cost per alternative.
5. **Deepen and loop** — apply the choice (scaffold, config, or explanation), update the decision stack, surface the next decision. Maintain the same `Decision stack` format as robotics-advisor.

## Core decision axes (the usual suspects)

| Decision | Default that usually wins | When to deviate |
|----------|---------------------------|-----------------|
| Comms pattern | Topic (stream), Service (quick query), Action (long task w/ feedback) | Mixed patterns per endpoint smell like a design problem — revisit boundaries |
| Node type | Lifecycle node for hardware/resource owners | Plain node for stateless transforms and monitors |
| Executor | Single-threaded until proven insufficient | MultiThreaded + callback groups when callbacks genuinely overlap |
| QoS | Sensor: BEST_EFFORT/VOLATILE; commands: RELIABLE, depth 1 | Latched data (map, URDF): TRANSIENT_LOCAL |
| Actuator I/O | ros2_control hardware interface | Vendor SDK bridge node when the ecosystem already ships one |
| Language | C++ for ≥100 Hz loops and drivers, Python for orchestration | Follow what the team can maintain |

## Environment notes

- zsh users: source `setup.zsh` (never `setup.bash`), and wrap sourcing with `set +u` / `set -u` — ROS setup scripts reference unbound variables.
- Pin the distro in Dockerfile/CI docs so builds reproduce.

## Gotchas

- **QoS mismatch fails silently.** "I publish but nothing arrives" is a QoS incompatibility until proven otherwise — check `ros2 topic info -v` before touching code.
- **Synchronous service calls inside callbacks deadlock the executor.** Use async with a response callback, and put the client in a separate callback group.
- **A dying node must not leave motors running.** Send zero-commands in `on_deactivate` AND the destructor — crashes skip the polite path.
- **`use_sim_time` is all-or-nothing.** One node on wall clock while the rest follow `/clock` breaks TF lookups in ways that look like random bugs.
- **Distro API drift is real.** ros2_control, CMake idioms, and bag formats have all changed between LTS releases — verify against the target distro's docs, not memory or old tutorials.
- **Never emit ROS 1 code.** `rospy`/`roscpp` patterns in an answer mean the whole answer is wrong.
