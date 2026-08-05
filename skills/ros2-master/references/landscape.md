# ROS 2 Ecosystem Landscape — verified snapshot

**Verified: 2026-08-05.** Entries were confirmed against live sources on this date — re-verify anything before relying on it if this snapshot is more than ~6 months old.

Entry format: **Name** — one-line what-it-is. Status: maintained / research / commercial. Source: `<url>`

---

## Active distros (from REP-2000 + release docs)

REP-2000 (fetched live) covers all releases through Kilted Kaiju; per the REP itself, platform/EOL info for releases after Kilted is published in each release's own documentation rather than the REP. Source: https://reps.openrobotics.org/rep-2000/

- **Jazzy Jalisco** — LTS, released May 2024, EOL May 2029. Status: maintained (LTS). Source: https://reps.openrobotics.org/rep-2000/
- **Kilted Kaiju** — non-LTS (1.5-year support), released May 2025, EOL November 2026. Status: maintained (approaching EOL). Source: https://reps.openrobotics.org/rep-2000/
- **Lyrical Luth** — LTS, released May 22, 2026, supported through May 2031. Newest ROS 2 distro; per REP-2000's own note, its platform/EOL details live in its release docs rather than the REP table. Tier 1 platforms: Ubuntu 26.04 (Resolute) amd64/arm64 and Windows 11 (VS 2022) amd64; Tier 2 RHEL 10; Tier 3 includes Ubuntu 24.04 Noble, macOS, Debian Trixie, OpenEmbedded. Headline changes: a Callback Group Events Executor (announcement claims 10–15% lower CPU than existing executors), `AsyncNode` bringing asyncio to rclpy, and `rosidl::Buffer` replacing `std::vector<uint8_t>` to enable zero-copy GPU data transfer. Status: maintained (current LTS). Source: https://discourse.openrobotics.org/t/ros-2-lyrical-luth-released/55021 (release announcement; the docs.ros.org mirror is behind an Anubis anti-bot gate and may not fetch)
- **Humble Hawksbill** — LTS, released May 2022, EOL May 2027 — still within support window but past its midpoint; plan migrations off it. Status: maintained (LTS, aging). Source: https://reps.openrobotics.org/rep-2000/
- **Rolling Ridley** — the rolling development distro, released June 2020, no fixed EOL (continuously developed; always tracks the next release). Status: maintained (dev target only, not for production pins). Source: https://reps.openrobotics.org/rep-2000/
- **Iron Irwini** — EOL'd November 2024. Do not start new work on it. Status: EOL. Source: https://reps.openrobotics.org/rep-2000/

## Middleware (DDS implementations + Zenoh)

- **Fast DDS (eProsima)** — the default RMW implementation (`rmw_fastrtps_cpp`) across every currently supported distro except EOL Galactic. Status: maintained (default). Source: https://fast-dds.docs.eprosima.com/en/latest/fastdds/ros2/ros2.html
- **Cyclone DDS (Eclipse)** — alternative Tier-1 DDS RMW (`rmw_cyclonedds_cpp`), used as the default only in the EOL Galactic distro; commonly swapped in for its lower resource footprint. Status: maintained. Source: https://github.com/ros2/rmw_cyclonedds
- **rmw_zenoh** — non-DDS RMW built on the Zenoh pub/sub/query protocol; officially supported as an installable alternative from Jazzy onward, targeting constrained/fog/cloud deployments where DDS discovery overhead is a problem. DDS remains the default — Zenoh is an opt-in alternative, not a replacement. Repo carries formal Quality Declarations and ships binaries for Tier-1 platforms, with per-distro branches. Status: maintained (official alternative). Source: https://github.com/ros2/rmw_zenoh

## ros2_control

- **ros2_control** — the standard actuator-control framework (hardware interfaces, controller manager, JointTrajectoryController etc.); maintainer count has doubled and the project is now under OSRA (Open Source Robotics Alliance) governance. MoveIt 2 only plans motion — ros2_control is what actually executes it on hardware. **Distro coverage as of 2026-08-05: stable releases for Kilted, Jazzy, Humble; Rolling and Lyrical listed as in-development.** That lag matters — a project pinning the newest LTS (Lyrical) may be ahead of its actuator stack. Re-check before pinning. Status: maintained (actively growing). Source: https://control.ros.org/rolling/doc/release_notes/release_notes.html

## Notable ecosystem tools / shifts

- **Nav2** — the industry-standard ROS 2 navigation stack (successor to the ROS 1 Navigation Stack), stewarded by Open Navigation LLC with contributions credited to 300+ companies. Status: maintained (commercial-backed). Source: https://docs.nav2.org/about/index.html (also https://github.com/ros-navigation/navigation2)
- **MoveIt 2** — the standard ROS 2 motion-planning framework; plans trajectories that ros2_control then executes via the JointTrajectoryController interface. Status: maintained. Source: https://moveit.ai/about/distribution/
- **Gazebo Harmonic** — current LTS release of "new" Gazebo (the Ignition-lineage rewrite, distinct from the retired "classic" Gazebo); released Sept 2023, supported through 2028, and is the default simulator target for new ROS 2 projects. Status: maintained (default sim). Source: https://gazebosim.org/docs/harmonic/ros2_overview/
- **Isaac Sim / Isaac Lab as a ROS 2 sim target** — NVIDIA's GPU-accelerated simulator is increasingly used alongside/instead of Gazebo for ROS 2 projects needing photorealistic rendering or large-scale parallel RL training, per 2026 ecosystem coverage pairing Nav2/MoveIt2/Gazebo with Isaac Sim/MuJoCo/LeRobot workflows. Status: maintained (NVIDIA-backed, growing adoption). Source: https://github.com/isaac-sim/IsaacLab
