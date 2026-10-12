# Harness gate template (ROS 2, no middleware support)

ROS 2 does not host the Projection, Isolation and Transfer mechanisms itself. Build them as one gate node between the
model and the controller, driven by one profile. Keep the model node unaware of the gate.

```text
camera topics ──▶ policy node ──/policy/cmd_raw──▶ harness gate ──/cmd──▶ controller
                                  /policy/ood_score ──▶ │  │
                                                        │  └─ lifecycle: deactivate policy, activate baseline
                       baseline node (hold / gravity) ◀─┘
```

The profile lives beside the launch file. It extends the position paper's Listing 1 (model node, output topic, output
region, maximum staleness, inference budget, transport budget, operating regime, fallback node; Source:
https://arxiv.org/abs/2606.09416) with input staleness and the return rule, which the paper leaves out.

```yaml
harness_profile:
  model_node: /policy
  output_topic: /policy/cmd_raw        # gate republishes admitted samples on /cmd
  output_region:                       # per joint, in the controller's units
    position: {min: [...], max: [...]}
    max_step: 0.05                     # largest change between consecutive admitted samples
  max_staleness_ms: 50                 # action stamp vs now
  inputs:                              # every observation stream the model reads
    - {topic: /camera/wrist/compressed, max_gap_ms: 100}
    - {topic: /joint_states, max_gap_ms: 20}
  inference_budget: {wcet_ms: 40, rate_hz: 10}
  transport_budget: {max_payload_bytes: 4096, deadline_ms: 20}
  operating_regime: {signal: /policy/ood_score, max: 0.7}
  fallback_node: /hold_position
  transfer:
    trip_after_rejects: 3              # consecutive Projection rejects
    return_after_clean_s: 2.0          # positive signal required to hand authority back
```

Every number above is a placeholder. Derive each from a measurement on the deployment hardware, and keep the profile in
version control next to the launch file so a threshold change shows up in review.

Gate node rules:

- Each check writes one JSONL line per decision (admit, reject with the reason, transfer, return) and flushes it, so a
  gate that dies still leaves its last decisions behind. A harness that leaves no trace cannot be audited later.
- Reject before clamping. If a sample is out of region, hold the last admitted value and count a reject. Never
  silently clamp a learned output into range, because clamping hides the drift Transfer needs to see.
- Revoke authority on stale inputs. When any listed input exceeds its `max_gap_ms`, treat it like repeated rejects and
  Transfer, because a model fed frozen frames publishes in-range, on-time, wrong commands.
- Transfer goes through lifecycle transitions. Deactivate the policy, then activate the baseline. Both nodes are
  managed nodes, so the switch is observable with `ros2 lifecycle get`.
- Give the downstream controller its own command timeout, so that a dead gate process also ends in the baseline
  behavior instead of the last target held under a stiff gain.
- Declare ranges on every harness parameter and validate in an on-set callback, so a runtime `ros2 param set` cannot
  widen the envelope without the consistency checks running again.
- Size the gate's own latency against the control rate before deployment. The paper leaves the per-sample cost open,
  so measure it rather than assume it.

Write a **harness card** with the deployment, meaning the profile actually enforced plus the measured inference time
and reject rate. Then two deployments of the same policy can be compared on governance, not only on success rate.
