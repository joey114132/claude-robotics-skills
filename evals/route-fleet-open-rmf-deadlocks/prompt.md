---
name: route-fleet-open-rmf-deadlocks
description: "Single-skill routing: multi-vendor AMRs deadlocking at shared lifts and aisle junctions."
tags: [routing]
expected_outcome: "Routes to robot-fleet: traffic deconfliction, shared lifts and corridors, task allocation and mixing vendors only exist because there is more than one robot."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
We run eight AMRs from two different vendors in one warehouse. They deadlock at narrow aisle junctions and fight over the freight elevator. How should we set up traffic management and task allocation across them? Is Open-RMF the right tool?
