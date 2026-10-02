# Robotics Method Advisor Landscape — verified snapshot
**Verified: 2026-10-02.** Entries were confirmed against live sources on this date — re-verify anything before relying on it if this snapshot is more than ~6 months old.

Modern counterparts to the classic methods in Craig's book. The chapter map and the keyword table of counterparts live in `craig3-map.md`; this file holds only entries that were checked against a source.

## Inverse kinematics
- **mink** — Python differential inverse-kinematics library based on MuJoCo: task specification in configuration or operational space, limits on joint positions and velocities, collision avoidance between any geom pair, and closed-chain kinematics (loop closures) via MuJoCo equality constraints. A modern counterpart to the Jacobian-inverse IK of Craig Ch5 for MuJoCo users. Status: maintained, Apache-2.0, v1.3.0 released 2026-08-18, last push 2026-09-30. Source: https://github.com/kevinzakka/mink

## Inverse kinematics (research)
- **Planning along Differentiable Charts of Constraint Manifolds with General-Purpose IK Solvers (Cohn, Shaw, Biggie, Manderson, Roy, Tedrake, 2026-09-09)** — makes analytic IK, including IKFast output, usable inside gradient-based trajectory optimization by recovering IK gradients from the forward-kinematic Jacobian via the inverse function theorem, with a least-squares domain extension that keeps gradient signal outside the reachable workspace; demonstrated on an RB-Y1 box pick-and-place. Combines the closed-form IK idea of Craig Ch4 with modern optimization-based planning. Status: preprint, v1, 8 pages, under review. Source: https://arxiv.org/abs/2609.10905

## Motion generation and trajectory optimization
- **cuRobo (cuRoboV2)** — CUDA-accelerated library for forward and inverse kinematics, collision checking, trajectory optimization, geometric planning and whole-body motion generation, built on PyTorch, CUDA and Warp. Status: maintained, Apache-2.0; the v0.8.0 release (2026-04-18) is a significant rewrite whose public API differs from v1, so pin tag v0.7.8 if code depends on the v1 API. Source: https://github.com/NVlabs/curobo
