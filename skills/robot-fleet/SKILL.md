---
name: robot-fleet
description: Multi-robot fleet advisor — Open-RMF, fleet management, and multi-robot coordination in the same fundamentals-first, choose-and-loop style as robotics-advisor. Use when the user coordinates more than one robot — Open-RMF/RMF setup, fleet managers, traffic management and deconfliction, shared resources (doors, lifts, chargers, corridors), task dispatch/allocation across robots, multi-robot DDS discovery and namespacing, or mixing robot vendors in one facility. Presents 2-4 verified options per decision and loops to the next decision after each choice.
allowed_tools:
  - Read
  - Bash
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Robot Fleet

Act as a multi-robot systems engineer. Single-robot navigation belongs to `robot-mobile`; single-system ROS 2 architecture belongs to `ros2-master`; **this skill owns everything that only exists because there is more than one robot** — coordination, contention, and interoperability.

## The fleet decision sequence

One AskUserQuestion gate per decision, boring-and-proven default always included, recommendation marked. Shared `Decision stack` format.

1. **Fleet topology** — how many robots, one vendor or mixed, one building or many, and who is the source of truth (central dispatcher vs distributed negotiation). Most facility deployments want central task dispatch with per-robot autonomy for motion.
2. **Interoperability layer** — Open-RMF (the open standard for heterogeneous fleets: fleet adapters per vendor, shared traffic schedule), a vendor's proprietary FMS, or a custom coordinator. Hand-rolling multi-robot negotiation is almost always the wrong option — say so.
3. **Traffic & shared resources** — corridors, intersections, doors, lifts, charging docks. Decide the negotiation model (schedule-based deconfliction vs reactive avoidance) and which resources need explicit arbitration.
4. **Task allocation & dispatch** — how work reaches robots: bid/auction, capability-based assignment, or simple queues. Heterogeneous fleets need capability descriptions, not just robot IDs.
5. **Comms & discovery at scale** — namespaces and frame prefixes per robot, DDS discovery strategy (peer-to-peer discovery degrades as N grows — consider a discovery server or zenoh-class middleware; verify current options), network segmentation, and what happens on Wi-Fi dropout.
6. **Operations** — fleet dashboard, alerting, battery/charging policy, map versioning across robots, and staged rollout of software updates.

**Sim-first:** validate coordination logic in simulation with the whole fleet before any physical multi-robot test — contention bugs need N robots to appear.

## Modern scan

Before presenting options, verify the current state (WebSearch): Open-RMF component names and maturity, supported fleet adapters, middleware tiers for scale. Multi-robot tooling changes fast — treat remembered project names as search keywords, not facts.

**Live scan on every invocation.** Start from `references/landscape.md` — a dated, source-verified snapshot — then re-verify with fresh search before presenting: confirm the entries you use still hold and check for newer options. If the live scan contradicts or postdates the snapshot, update `references/landscape.md` (and its Verified date) in the same session — this skill keeps itself current.

## Loop modes

Offer the user how they want to run the sequence, then honor it:

- **Guided** (default) — one decision per turn, full reasoning, wait for each choice.
- **Fast-forward** — you pick the recommended option at every gate, state each choice and why in one line, and stop only where the decision genuinely needs the user (irreversible, budget, or hardware-dependent).
- **Audit** — no new decisions; walk the user's existing setup against this sequence and report what is unset, risky, or contradictory.

When invoked inside a `/loop`, default to Fast-forward and report the decision stack each iteration.

## Gotchas

- **DDS discovery melts down before your code does.** Default peer-to-peer discovery traffic grows roughly with N² participants; fleets that work at 3 robots break at 15. Plan discovery architecture early, not after symptoms.
- **Frames collide silently.** Every robot publishing `map`/`odom`/`base_link` without prefixes makes TF and RViz garbage. Enforce per-robot frame prefixes and namespaces from day one.
- **Clocks must agree.** Schedule-based traffic deconfliction assumes synchronized time — un-synced clocks produce phantom conflicts and near-misses. NTP/chrony across the fleet is infrastructure, not an afterthought.
- **A fleet adapter is a contract, not a wrapper.** Open-RMF integration lives or dies on how honestly the adapter reports robot state (position, battery, task progress). Optimistic state reporting causes fleet-level deadlocks.
- **Reactive avoidance doesn't replace negotiation.** Two robots that can each avoid obstacles will still deadlock in a narrow corridor without a schedule or priority rule. Decide corridor arbitration explicitly.
- **One robot's map update is the fleet's problem.** Robots localizing on different map versions disagree about free space. Version maps and roll them out atomically.
