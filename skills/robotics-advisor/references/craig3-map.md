# Craig, *Introduction to Robotics: Mechanics and Control*, 3rd ed. — PDF Map

**File:** `~/Downloads/Introduction-to-Robotics-3rd-edition.pdf` (408 pages, scanned/OCR — expand `~` to the user's home; edit if your copy lives elsewhere. Page numbers below assume this exact 408-page scan; a different scan shifts them.)

**Page rule:** `pdf page = book page + 8`. All numbers below are **PDF pages** (use directly in the Read tool's `pages` param, max 20 pages per request). OCR quality is mediocre ("will" → "wifi") — read for structure and definitions, re-derive equations yourself rather than trusting OCR'd math.

## Chapter map (verified against this PDF)

| Ch | Title | PDF pages | Core concepts & terminology |
|----|-------|-----------|------------------------------|
| 1 | Introduction | 9–26 | manipulator anatomy, DOF, notation conventions, forward/inverse problem overview |
| 2 | Spatial descriptions and transformations | 27–69 | frames, rotation matrices, homogeneous transforms, mappings vs operators, Euler angles, fixed angles, angle-axis, transform equations (§2.2–2.8) |
| 3 | Manipulator kinematics | 70–108 | link parameters, **DH convention** (§3.4), forward kinematics, actuator/joint/Cartesian space (§3.6), standard frames {B}{S}{W}{T}{G} (§3.8) |
| 4 | Inverse manipulator kinematics | 109–142 | solvability, workspace, subspace, algebraic vs geometric solutions, **Pieper's solution** (§4.6, three intersecting axes), repeatability vs accuracy (§4.10) |
| 5 | Jacobians: velocities and static forces | 143–172 | velocity propagation (§5.3 p146, §5.4 p149), **Jacobian** (§5.7 p157), singularities, static forces (§5.9 p161), force-domain Jacobian |
| 6 | Manipulator dynamics | 173–208 | mass distribution/inertia tensor (§6.3), Newton-Euler iterative formulation (§6.5), **Lagrangian formulation** (§6.9), M-V-G structure (§6.8), Cartesian-space dynamics (§6.10), simulation (§6.12) |
| 7 | Trajectory generation | 209–237 | joint-space schemes: cubic/quintic polynomials, linear-with-parabolic-blends (§7.3 p211), Cartesian-space schemes (§7.4 p224), geometric path problems (§7.5 p227), runtime generation (§7.6 p230), dynamics-aware planning (§7.8 p232) |
| 8 | Manipulator-mechanism design | 238–269 | task-based design (§8.2 p239), workspace metrics (§8.4 p247), redundant & closed-chain structures (§8.5 p249), stiffness/deflection (§8.7 p255), position sensing (§8.8 p260) |
| 9 | Linear control of manipulators | 270–297 | second-order systems (§9.3 p272), **control-law partitioning** (§9.5), trajectory-following, disturbance rejection, single-joint modeling (§9.9), industrial controller architecture (§9.10) |
| 10 | Nonlinear control of manipulators | 298–324 | **computed-torque control** (§10.4), MIMO control, Lyapunov stability (§10.7), Cartesian-based control (§10.8), adaptive control (§10.9) |
| 11 | Force control of manipulators | 325–346 | natural/artificial constraints (§11.3), **hybrid position/force control** (§11.4–11.6), assembly tasks |
| 12 | Robot programming languages and systems | 347–360 | three levels of robot programming (§12.2), teach pendant vs offline |
| 13 | Off-line programming systems | 361–373 | OLP central issues, simulation, calibration, automating subtasks |
| — | Appendices A–C, solutions, index | ~374–408 | trig identities, inverse-kinematics formulas, unit conversions |

## Topic → chapter routing

| User's problem sounds like… | Read |
|-----------------------------|------|
| "pose, frame, rotation, quaternion vs Euler, transform" | Ch2 |
| "FK, DH parameters, where is the end-effector" | Ch3 |
| "IK, reachability, workspace, multiple solutions" | Ch4 (+Ch3) |
| "velocity, singularity, force at tip, torque mapping" | Ch5 |
| "equations of motion, inertia, simulation, gravity compensation" | Ch6 |
| "smooth motion, waypoints, velocity profile, blending" | Ch7 |
| "how many joints, actuator sizing, stiffness, encoder choice" | Ch8 |
| "PID, tuning, tracking error, one joint oscillates" | Ch9 |
| "model-based control, computed torque, adaptive" | Ch10 |
| "contact, insertion, polishing, compliance, force feedback" | Ch11 |
| "robot programming workflow, simulation-first" | Ch12–13 |

## Modern counterparts to search for (starting keywords, not asserted facts — verify via WebSearch/arxiv before presenting)

| Craig topic | Modern directions to search |
|-------------|------------------------------|
| Ch2 orientation representations | quaternion/SO(3) libraries, Lie group methods (micro Lie theory), `manif`, SciPy `Rotation` |
| Ch3–4 FK/IK | TRAC-IK, IKFast, Pinocchio-based differential IK, learning-based IK, Drake, MoveIt |
| Ch5 Jacobians/singularity | damped least squares (DLS), manipulability optimization, QP-based whole-body IK |
| Ch6 dynamics | Pinocchio, MuJoCo, Drake; ABA/RNEA/CRBA algorithms (Featherstone) |
| Ch7 trajectories | Ruckig (online jerk-limited), TOPP-RA, OMPL/CHOMP/STOMP, MPC-based planning |
| Ch9–10 control | operational-space control, impedance control, MPC, RL-based control |
| Ch11 force control | admittance vs impedance control, series-elastic actuation, learned contact-rich manipulation |
| Ch12–13 programming | ROS 2, behavior trees, task-and-motion planning (TAMP), LLM-based task planning |
