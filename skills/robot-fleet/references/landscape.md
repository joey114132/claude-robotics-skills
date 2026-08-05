# Multi-Robot & Fleet Landscape — verified snapshot

**Verified: 2026-08-05.** Entries were confirmed against live sources on this date — re-verify anything before relying on it if this snapshot is more than ~6 months old.

## Open-RMF components & status

- **Open-RMF (root repo)** — "the Open-RMF platform for multi-fleet robot management"; vendor-agnostic orchestration for heterogeneous robot fleets sharing space, lifts, doors, and other building infrastructure. Actively supports ROS 2 Humble, Jazzy, Kilted, and Rolling with binary packages and nightly Docker builds. Status: maintained. Source: https://github.com/open-rmf/rmf
- **rmf_ros2** — internal ROS 2 infrastructure for RMF, including the `rmf_fleet_adapter` package (the C++ API fleets integrate against); last updated Jul 29, 2026 at verification time. Status: maintained. Source: https://github.com/open-rmf/rmf_ros2
- **rmf_traffic** — core algorithms and data structures for scheduling and negotiating mobile-robot traffic between multiple agents. Status: maintained. Source: https://github.com/open-rmf/rmf_traffic
- **rmf-web** — TypeScript web dashboard for visualizing and controlling Open-RMF deployments; updated Aug 3, 2026 at verification time. Status: maintained. Source: https://github.com/open-rmf/rmf-web
- **rmf_demos** — reference demonstrations/simulations of Open-RMF deployments. Status: maintained. Source: https://github.com/open-rmf/rmf_demos
- **free_fleet** — free, open fleet-management component for robots exposing native ROS navigation endpoints; updated Jul 28, 2026 at verification time. Status: maintained. Source: https://github.com/open-rmf/free_fleet
- **fleet_adapter_template** — starting-point template repo for integrating a new robot fleet with Open-RMF; updated Jul 11, 2026 at verification time. Status: maintained. Source: https://github.com/open-rmf/fleet_adapter_template
- **osrf/rmf_core (legacy)** — the original centralized RMF scheduling repo; archived by the owner on Jul 22, 2021 and now read-only. Development moved to the `open-rmf` GitHub org (above). Status: archived/superseded — do not build against this repo. Source: https://github.com/osrf/rmf_core

## Fleet management systems (open + commercial + China-market)

- **Robofleet** — open-source, web-based multi-robot control/visualization for ROS, presented at IROS 2021; robots run a client that exchanges data with a central server. Status: research/low-activity open source. Source: https://github.com/ut-amrl/robofleet
- **RobotFleet** — open-source framework for centralized multi-robot task planning/scheduling that wraps robots as containerized services and leverages LLMs for planning. Status: research. Source: https://arxiv.org/pdf/2510.10379
- **Seer Robotics (SEER Intelligent Technology)** — China-based AGV/AMR navigation-controller and fleet-software platform vendor; SRC-series controllers reported to power 200+ AGV/AMR brands and hold #1 global robot-controller market share (24.8% global / 45.2% China, cited for 2025). Status: commercial. Source: https://www.mobile-robots.com/manufacturer/seer-robotics/
- **Geek+ (极智嘉)** — Beijing-headquartered AMR/warehouse-robotics vendor; self-developed dispatch system reported to process ~10k instructions/sec and coordinate 5,000+ robots per warehouse; reported #1 global AMR market share for 6 consecutive years. Status: commercial. Source: https://www.geekpark.net/news/350876
- **Hikrobot** — Hangzhou-based industrial AMR and machine-vision vendor (Hikvision ecosystem); offers LMR/FMR/CMR robot lines plus a proprietary iWMS and RCS 2000 fleet-management/robot-control system for mixed fleets. Status: commercial. Source: https://www.agvnetwork.com/agv-producers/hikrobot
- **Youibot (YOUIFleet)** — Shenzhen-based AMR maker; YOUIFleet fleet-management software offers dynamic task scheduling, path planning, and congestion prediction for narrow-aisle warehouse scenarios. Status: commercial. Source: https://en.youibot.com/products-category/youifleet.html
- **Quicktron** — Alibaba-backed AGV vendor focused on high-throughput e-commerce fulfillment/sorting; reports 1,000+ enterprise customers across 30+ countries. Status: commercial. Source: https://www.mobile-robots.com/manufacturer/quicktron/

## Multi-robot middleware / discovery at scale

- **rmw_zenoh** — ROS 2 RMW implementation built on the Zenoh protocol; currently Quality Level 2 (not yet Tier-1), with Tier-1 promotion targeted for a subsequent release per an open tracking issue; available on ROS 2 Jazzy and later only (not Humble) — per the repo README, distro branches exist but Humble cannot communicate with Iron-and-newer distros over rmw_zenoh because type hashes are embedded in Zenoh keyexpressions. Status: maintained, pre-Tier-1. Source: https://github.com/ros2/rmw_zenoh and https://github.com/ros2/rmw_zenoh/issues/265
- **Fast DDS Discovery Server** — centralized discovery mode for DDS/ROS 2 (vs. default peer-to-peer multicast discovery); traffic scales linearly with fleet size instead of quadratically, and new robots don't require config changes on existing ones. Cited as enabling OTTO Motors to scale to 100+ robots per facility after migrating to ROS 2. Status: maintained. Source: https://husarnet.com/blog/ros2-dds-discovery-server

## Task allocation research (arXiv)

- **Very Large-scale Multi-Robot Task Allocation in Challenging Environments via Robot Redistribution** (arXiv:2506.07293) — MRTA in obstacle-dense/narrow-passage environments using a Generalized-Voronoi-Diagram roadmap to minimize makespan while avoiding collisions/deadlocks. Status: research. Source: https://arxiv.org/abs/2506.07293
- **Uncertainty-Aware Multi-Robot Task Allocation With Strongly Coupled Inter-Robot Rewards** (arXiv:2509.22469) — market-based decentralized MRTA that optimizes coupled team rewards under task-requirement uncertainty, with a polynomial-time decentralized solution. Status: research. Source: https://arxiv.org/abs/2509.22469
- **Efficient Human-Aware Task Allocation for Multi-Robot Systems in Shared Environments** (arXiv:2508.19731) — incorporates human motion patterns into MRTA decision-making for human-populated workspaces. Status: research. Source: https://arxiv.org/abs/2508.19731
- **Large Language Models for Multi-Robot Systems: A Survey** (arXiv:2502.03814) — survey categorizing LLM integration into multi-robot systems across high-level task allocation, mid-level motion planning, low-level action generation, and human intervention. Status: research. Source: https://arxiv.org/abs/2502.03814
