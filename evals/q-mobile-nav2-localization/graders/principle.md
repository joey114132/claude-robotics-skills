---
type: llm
---
The mechanism behind the trap is the division of labor between the odom and map frames. The odom->base_link transform must be a smooth, continuous, drifting-but-never-jumping estimate of motion, and Nav2 also needs nav_msgs/Odometry for velocity. AMCL consumes odom->base_link as its motion input (prediction step; filter updates are gated by movement of update_min_d and update_min_a) and publishes only a slow correction as map->odom, so map pose jumps are absorbed there, not in odom. With a static identity transform, AMCL sees no motion, and the local costmap and controller, which work in the odom frame, see a cart that never moves with zero measured velocity.

PASS only if the reply explains this mechanism well enough for a practitioner to act on, covering at least: (a) that AMCL needs odom->base_link as its motion model input and a stationary identity transform gives it no motion information (or no filter updates), and (b) that odom must be continuous with map->odom carrying the corrections, or that controllers and the local costmap rely on odom pose and velocity. Both (a) and (b) must be present in some form.

FAIL if the reply only asserts that odometry is needed without saying why, or gives a mechanism that is wrong (for example claiming AMCL estimates motion from the lidar by itself, or that a static identity transform is fine as long as alpha values are raised).
