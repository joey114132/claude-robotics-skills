---
name: route-radar-refresh-collection
description: "Single-skill routing: sweep the robotics skill collection for staleness."
tags: [routing]
expected_outcome: "Routes to robotics-radar: the self-maintenance sweep that refreshes the collection's snapshots."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
I set up my robotics skills about six months ago and suspect their reference notes have drifted from the field. Go look for what has changed since then, such as new robot platforms, revised standards, and repos that got archived, and update the skills to match.
