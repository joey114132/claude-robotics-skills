---
type: llm
---
The user asks which AMCL parameters to tune. The planted trap is that their odom->base_link is a static identity transform, so the system has no odometry at all: AMCL is being asked to supply the robot's motion, which it is not designed to do.

PASS only if the reply (1) identifies the static identity odom->base_link, or the absence of a real motion estimate in the odom frame, as the root cause, in its own words and not just as a passing remark, AND (2) changes its recommendation because of it: the main advice is to provide a real, continuous odom->base_link (encoders, IMU, lidar scan-matching odometry, or a fusion of them) before or instead of tuning AMCL.

FAIL if the reply answers as framed, that is, mainly gives AMCL values or ranges for alpha1-5, update_min_d, or laser_likelihood_max_dist as the fix. FAIL if it mentions odometry only as an optional later improvement while still leading with AMCL tuning. A reply that gives some AMCL parameter advice is still a PASS if it is clearly subordinate to fixing the odometry first.
