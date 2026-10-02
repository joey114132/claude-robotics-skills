---
name: route-learning-vla-vs-diffusion
description: "Single-skill routing: fine-tune a pretrained VLA versus train a policy from scratch."
tags: [routing]
expected_outcome: "Routes to robot-learning: the decision to learn, the policy class, dataset design and evaluation of success rate all belong to the robot-learning skill."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
We have about 200 demonstrations of a tabletop assembly task. Should we fine-tune a pretrained vision-language-action model on them or train a diffusion policy from scratch? How should we structure the dataset, and how do we measure success rate in a way that isn't noise?
