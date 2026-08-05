# Robot Arm Manipulation Landscape — verified snapshot
**Verified: 2026-08-05.** Entries were confirmed against live sources on this date — re-verify anything before relying on it if this snapshot is more than ~6 months old.

## IK solvers
- **TRAC-IK** — hybrid IK solver (KDL Newton-based extension + SQP nonlinear optimization run concurrently) that handles joint limits far better than plain KDL; standard MoveIt kinematics plugin. Status: maintained (ROS 2 ports active). Source: https://traclabs.com/projects/trac-ik/ (ROS 2 port: https://github.com/aprotyas/trac_ik)
- **Pink** — Python differential/task-space inverse kinematics built on Pinocchio + QP solvers; define weighted tasks, get joint velocities. Status: maintained (v4.3.0, active CI). Source: https://github.com/stephane-caron/pink
- **ikpy** — pure-Python universal IK library; imports URDF/MJCF directly, has an experimental JAX backend as of v4 (requires Python 3.10+). Status: maintained. Source: https://github.com/Phylliade/ikpy

## Motion planning frameworks
- **MoveIt 2** — the standard ROS 2 manipulation stack (planning, perception, execution); pluggable planners with OMPL as the default backend. Status: maintained, PickNik-led, ~9.5k commits, multi-distro CI (Rolling/Jazzy/Humble). Source: https://github.com/moveit/moveit2
- **OMPL (Open Motion Planning Library)** — sampling-based planning core (RRT/PRM family and variants) used underneath MoveIt and other stacks. OMPL 2.0 (announced 2026) targets hardware-accelerated, real-time planning and tighter integration with AI research workflows. Status: maintained, ~18 years continuous development. Source: https://arxiv.org/abs/2605.29301 (OMPL 2.0 paper)
- **cuRobo** — NVIDIA CUDA-accelerated motion generation: GPU-parallel FK/IK, collision checking, trajectory optimization, and geometric planning, scaling from single arms to humanoids; reported ~50-100x faster than CPU-based Tesseract on RTX 3090/Jetson Orin AGX. Status: maintained (NVIDIA Labs). Source: https://github.com/NVlabs/curobo
- **Tesseract** — ROS-Industrial's lightweight motion-planning environment (Eigen/Boost/Orocos deps only), pairs with the TrajOpt trajectory optimizer; core is ROS-agnostic with a standalone Python package. Status: maintained. Source: https://github.com/tesseract-robotics/tesseract

## Trajectory generation
- **Ruckig** — real-time, jerk-constrained, time-optimal trajectory generation from any initial state to a target waypoint; jointly computes path and time parametrization for intermediate waypoints (RSS 2021 paper). Status: maintained. Source: https://github.com/pantor/ruckig
- **TOPP-RA (toppra)** — reachability-analysis-based time-optimal path parameterization given joint velocity/acceleration/tool-Cartesian constraints; `pip install toppra`. Status: maintained. Source: https://github.com/hungpham2511/toppra

## Dynamics / rigid-body libraries
- **Pinocchio** — fast rigid-body dynamics (RNEA, ABA, CRBA) with analytical derivatives, built on Eigen + FCL, Python bindings via Conda; the base layer under Pink and many optimization-based IK/planning stacks. Status: maintained. Source: https://github.com/stack-of-tasks/pinocchio
- **RBDL** — C++ rigid-body dynamics library (ABA/RNEA/CRBA, contact/collision constraints) originally from Heidelberg University's ORB group; the ORB-HD fork adds error handling and polymorphic constraints and is packaged in vcpkg. Status: maintained (via ORB-HD fork). Source: https://github.com/ORB-HD/rbdl-orb (origin: https://github.com/rbdl/rbdl)
- **MuJoCo** — contact-rich physics engine with soft-contact/implicit integration widely treated as the reference for manipulation and grasping dynamics; monthly release cadence, maintained by Google DeepMind. Also used directly as a simulator (see below). Status: maintained. Source: https://github.com/google-deepmind/mujoco

## Real-time servoing / teleop
- **MoveIt Servo** — collision- and singularity-aware real-time Cartesian/joint servoing for ROS 2 manipulators; consumes `TwistStamped` from gamepads, VR controllers, 6-DoF mice, or other nodes. Status: maintained, part of moveit2. Source: https://moveit.picknik.ai/humble/doc/examples/realtime_servo/realtime_servo_tutorial.html
- **GELLO** — low-cost, 3D-printed, kinematically-isomorphic leader-follower teleoperation controller (UC Berkeley) for collecting imitation-learning demonstrations; supports Franka, UR, xArm, and others. Status: maintained (515 stars, ongoing ROS 2 support work). Source: https://github.com/wuphilipp/gello_software
- **ALOHA** — low-cost open-source bimanual teleoperation hardware + software (master-puppet arms) for fine-manipulation demonstration collection (Stanford); ALOHA 2 is the enhanced-hardware follow-up. Status: usable/stable but low commit velocity (ROS 2 support still marked in-progress). Source: https://github.com/tonyzhaozh/aloha ; ALOHA 2 paper: https://arxiv.org/pdf/2405.02292

## Simulators for manipulation
- **Isaac Sim / Isaac Lab** — NVIDIA RTX-based photorealistic simulation plus a GPU-parallel robot-learning framework (RL/IL/motion planning) with 30+ prebuilt environments and thousands of parallel envs. Status: maintained (v3.0 beta as of this check), arXiv paper 2511.04831. Source: https://github.com/isaac-sim/IsaacLab
- **Genesis** — unified multi-physics simulation platform (rigid body, MPM, SPH, FEM, PBD) with a Pythonic interface and generative data engine; reports extreme simulation throughput (millions of FPS for a single arm on one RTX 4090). Now backed by Genesis AI. Status: maintained, ~30k stars. Source: https://github.com/Genesis-Embodied-AI/Genesis
- **Gazebo (gz-sim)** — general-purpose open-source robotics simulator, the long-standing ROS-ecosystem default, with multi-physics-engine support and Gazebo Fuel model libraries. Status: maintained (Intrinsic-led). Source: https://github.com/gazebosim/gz-sim
- **MuJoCo** — see Dynamics above; also used standalone as a simulator (MJX for JAX/GPU parallelism, MuJoCo Warp beta with NVIDIA) and is the common choice specifically for contact-rich manipulation and grasping. Source: https://github.com/google-deepmind/mujoco

## China-market / Chinese-language ecosystem
- **AgileX PiPER (松灵机器人)** — Dongguan-based AgileX Robotics' desktop dual-arm teleoperation platform (four 6-DoF arms, depth cameras, controllers) for embodied-AI data collection, imitation learning, and VLA research; ships with development interfaces/sample programs. Company also recently released a 7-DoF NERO arm. Status: commercial, active product line. Source: https://www.agilex.ai/product/69cce7c9f70ae516ed948dc9
- **Unitree Z1 SDK** — Unitree Robotics' official C++/Python SDK for its Z1 6-DoF manipulator arm, BSD-3-licensed. Status: maintained by manufacturer. Source: https://github.com/unitreerobotics/z1_sdk
- **Dummy-Robot** — popular Chinese open-source mini robotic-arm project (peng-zhihui): full hardware, closed-loop stepper-driven firmware, and Unity-based host software, with inverse kinematics and CAN-bus control. Status: open-source hobby/reference project, ~15.3k GitHub stars. Source: https://github.com/peng-zhihui/Dummy-Robot

## Notable recent research directions (arXiv-verified)
- **Diffusion Policy** (Chi, Xu, Feng et al., 2023) — represents a visuomotor manipulation policy as a conditional denoising-diffusion process; now a standard imitation-learning baseline. arXiv:2303.04137
- **ACT / fine-grained bimanual manipulation** (Zhao et al., 2023) — action-chunking transformer paired with the low-cost ALOHA hardware for fine bimanual manipulation from demonstrations. arXiv:2304.13705
- **OpenVLA** (Kim, Pertsch, Karamcheti et al., 2024) — 7B-parameter open-source vision-language-action model trained on 970k robot demonstrations, fine-tunable on consumer GPUs via LoRA. arXiv:2406.09246
- **Octo** (Octo Model Team et al., 2024) — open-source generalist transformer policy trained on 800k Open X-Embodiment trajectories, finetunable to new sensors/action spaces within hours. arXiv:2405.12213
- **π0** (Physical Intelligence — Black, Brown, Driess et al., 2024) — flow-matching vision-language-action model built on a pretrained VLM, trained across single-arm, dual-arm, and mobile-manipulator platforms. arXiv:2410.24164
- **OMPL 2.0** (Guo, Tyrovouzis, Flores et al., 2026) — major evolution of the sampling-based planning core toward hardware-accelerated, real-time planning integrated with modern AI research workflows. arXiv:2605.29301
