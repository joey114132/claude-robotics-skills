---
name: route-is-my-policy-safe-safety
description: "Collision: whether a learned policy is safe or allowed to run near people (robot-safety) versus the runtime wrapper around it (physical-ai-harness)."
tags: [routing]
expected_outcome: "Expected robot-safety. The question is whether a fine-tuned VLA is safe and defensible to run next to operators, which is a risk-assessment and protective-layer question. physical-ai-harness designs the gate, staleness and fallback layers, and robot-safety points to it for that design."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
We fine-tuned a vision-language-action model and want to run it on a collaborative arm in our lab where people work at the next bench. Is it safe to run? What would an auditor expect us to say about it in the risk assessment?
