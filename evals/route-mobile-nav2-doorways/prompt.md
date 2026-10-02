---
name: route-mobile-nav2-doorways
description: "Single-skill routing: Nav2 oscillation in doorways and AMCL loss in a corridor."
tags: [routing]
expected_outcome: "Routes to robot-mobile: Nav2 controllers, AMCL localization and odometry fusion for one robot moving through a space."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
My differential-drive AMR runs Nav2. It oscillates when it goes through narrow doorways, and AMCL loses localization in a long featureless corridor. Which controller plugin should I use, and how should I fuse odometry to fix this?
