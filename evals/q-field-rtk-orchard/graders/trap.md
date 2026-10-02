---
type: llm
---
The user plans GNSS-only row following in a pear orchard, citing 2 cm tracking error measured in an open field, and asks only how to configure RTK to keep that accuracy in the orchard.

The trap: tree canopy blocks and attenuates satellite signals and causes multipath, so RTK degrades (fixed to float or standalone, or a wrong fixed solution with small reported covariance) in the tree rows. The open-field result does not transfer, and no RTK configuration restores it. The design needs row-relative perception (LiDAR or camera tracking the tree rows or trunks) fused with IMU and odometry, rather than GNSS alone.

PASS only if the reply (1) says RTK accuracy/fix availability will degrade under the orchard canopy or in the tree rows because of signal blockage and/or multipath, and (2) changes its recommendation because of it, by recommending row-relative perception or fusion with other sensors instead of, or in addition to, the GNSS-only plan.

FAIL if the reply mainly answers as framed (NTRIP caster choice, antenna placement, RTCM settings, waypoint recording) and mentions canopy only as a passing caveat without changing the recommendation, or if it promises the open-field accuracy can be kept with GNSS alone.
