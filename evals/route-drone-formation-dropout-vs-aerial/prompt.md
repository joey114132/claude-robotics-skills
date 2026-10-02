---
name: route-drone-formation-dropout-vs-aerial
description: "Collision: formation recovery for 40 drones after dropouts, swarm versus aerial."
tags: [routing]
expected_outcome: "Expected robot-swarm. robot-swarm's text says robot-aerial owns what keeps one drone flying and a drone swarm 'settles that there first and comes here only for the inter-vehicle layer'. Decentralized re-formation after dropouts is that inter-vehicle layer, though robot-aerial's description lists 'swarm' work."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
We're flying forty Crazyflies in an indoor formation show. Each drone only talks to its few nearest neighbors. If a handful drop out mid-show, how should the remaining ones re-form the shape without a central controller?
