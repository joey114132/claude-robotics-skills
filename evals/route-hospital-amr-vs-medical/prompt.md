---
name: route-hospital-amr-vs-medical
description: "Collision: hospital delivery AMR navigation, mobile versus medical."
tags: [routing]
expected_outcome: "Expected robot-mobile. robot-medical's text routes 'hospital delivery-robot navigation to robot-mobile' and limits itself to robots whose workspace contains a human body."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
Our hospital linen-delivery AMR runs Nav2 and keeps freezing in crowded corridors near nurses' stations and when it meets bed transports. How should I tune costmap inflation, the controller, and the recovery behaviors?
