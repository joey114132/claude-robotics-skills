# Mobile Robot Navigation Landscape — verified snapshot

**Verified: 2026-08-05.** Entries were confirmed against live sources on this date — re-verify anything before relying on it if this snapshot is more than ~6 months old.

## SLAM packages

- **slam_toolbox** — 2D lifelong SLAM/localization for potentially massive maps; the currently supported ROS 2 SLAM library (built by Steve Macenski). Status: maintained. Source: https://github.com/SteveMacenski/slam_toolbox
- **Cartographer / cartographer_ros** — 2D/3D real-time SLAM across multiple sensor configs. The core `cartographer` library is no longer actively developed (rare PR merges only); the `cartographer_ros` integration package carries a MAINTAINED status and still gets compatibility updates. Status: limited/maintained (core is stalled, ROS wrapper maintained). Source: https://github.com/cartographer-project/cartographer_ros
- **RTAB-Map (rtabmap_ros)** — RGB-D/stereo/LiDAR graph-based SLAM with real-time constraints; ROS 2 port is functional (same params/topics as ROS 1), minimum ROS 2 Foxy. Status: maintained. Source: https://index.ros.org/p/rtabmap_ros/

## Localization

- **nav2_amcl** — Adaptive (KLD-sampling) Monte Carlo Localization particle filter against a known map; ships as part of Nav2. Status: maintained. Source: https://docs.nav2.org/configuration/packages/configuring-amcl.html
- **robot_localization** — EKF/UKF-based sensor fusion (IMU, wheel odometry, GPS, etc.) for continuous state estimation; commonly paired with or substituted for AMCL. Status: maintained. Source: https://github.com/cra-ros-pkg/robot_localization

## Nav2 core & plugins

- **Nav2 (navigation2)** — production-grade ROS 2 navigation framework (perception, planning, control, localization) described as trusted by 100+ companies; successor to the ROS 1 Navigation Stack. Status: maintained. Source: https://github.com/ros-navigation/navigation2
- **nav2_regulated_pure_pursuit_controller** — pure-pursuit local trajectory controller with regulation heuristics for velocity/collision constraints; best for exact path-following without dynamic-obstacle deviation. Status: maintained. Source: https://github.com/ros-navigation/navigation2/blob/main/nav2_regulated_pure_pursuit_controller/README.md
- **nav2_mppi_controller** — Model Predictive Path Integral local controller with plugin-based critics, adaptive collision avoidance; runs 50+ Hz on a modest 4th-gen i5; supports diff-drive, omni, and Ackermann robots. Status: maintained. Source: https://github.com/ros-navigation/navigation2/tree/main/nav2_mppi_controller
- **nav2_smac_planner** — templated A*-family global planner family: `SmacPlanner2D` (circular diff/omni robots), `SmacPlannerHybrid` (car/ackermann/legged, Hybrid-A*), `SmacPlannerLattice` (arbitrary-shaped vehicles, State Lattice). Status: maintained. Source: https://github.com/ros-navigation/navigation2/tree/main/nav2_smac_planner
- **nav2_bt_navigator / nav2_behavior_tree** — behavior-tree orchestration layer that coordinates Nav2's independent task servers (planner, controller, recovery, etc.) over ROS action/service interfaces. Status: maintained. Source: https://docs.nav2.org/concepts/index.html

## Docking / charging

- **opennav_docking (nav2_docking)** — Nav2-compatible docking task server with pluggable `ChargingDock` implementations (vision-servoed spiral controller, dock database for multiple dock instances); migrated into Nav2 core in June 2024, sponsored by NVIDIA. Status: maintained. Source: https://github.com/open-navigation/opennav_docking

## Sensor drivers of note

- **rplidar_ros (Slamtec)** — official ROS driver for the RPLIDAR series (A1/A2/A3/S1/S2/S3/T1); ROS 2 support on the `ros2` branch. Status: maintained. Source: https://github.com/Slamtec/rplidar_ros/tree/ros2
- **velodyne (ros-drivers/velodyne)** — ROS 2 packages for Velodyne 3D LiDARs (64E S2/S2.1/S3, 32E, 32C, VLP-16). Status: maintained. Source: https://github.com/ros-drivers/velodyne/tree/ros2
- **realsense-ros** — official Intel RealSense ROS 2 wrapper for D400-series, SR300, and T265 tracking module. Status: maintained. Source: https://github.com/realsenseai/realsense-ros

## Simulators for navigation

- **Gazebo (Harmonic) + ros_gz** — modern Gazebo simulator with a dedicated Nav2 setup guide; `ros_gz` bridges sensor data and joint commands with minimal glue code. Used with ROS 2 Jazzy+. Status: maintained. Source: https://docs.nav2.org/setup_guides/gazebo.html
- **webots_ros2 (Cyberbotics)** — official ROS 2 integration for the Webots simulator; Nav2 support added in the Iron timeframe, ships with 200+ prebuilt robot models exposing standard ROS 2 interfaces. Status: maintained. Source: https://github.com/cyberbotics/webots_ros2
- **NVIDIA Isaac Sim (ROS 2 Navigation tutorials)** — Omniverse-based simulator with documented single- and multi-robot Nav2 navigation tutorials. Status: maintained (commercial platform, free tier). Source: https://docs.isaacsim.omniverse.nvidia.com/5.1.0/ros2_tutorials/tutorial_ros2_multi_navigation.html
- **nav2_loopback_sim** — standalone non-physical "loopback" simulator that stands in for a physics simulator (Gazebo/Bullet/Isaac Sim) or real hardware for fast Nav2-only testing. Status: maintained. Source: https://docs.ros.org/en/jazzy/p/nav2_loopback_sim/
