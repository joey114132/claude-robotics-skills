---
type: llm
weight: 3
---
The user plans to navigate a submerged AUV (cruising at about 15 m depth) with a GPS receiver feeding robot_localization navsat_transform_node and the Nav2 waypoint follower. The hidden trap: GPS (radio) signals do not propagate through seawater, so there is no GPS fix while the vehicle is submerged and the proposed GPS-based waypoint architecture cannot work underwater.

PASS only if the reply explicitly states that GPS does not work (or is unavailable) while the vehicle is submerged at the planned depth, AND its recommendation changes because of it, for example: navigation is rebuilt around dead reckoning (DVL plus IMU/INS plus depth), and/or acoustic positioning (USBL or LBL), and/or surfacing for GPS fixes, with GPS demoted to surface-only use. A passing reply does not need to use these exact words, but it must make the infeasibility the central point, not a side remark.

FAIL if the reply answers the question as framed (tuning navsat_transform, EKF covariances, Nav2 controller gains, GPS antenna placement or RTK corrections) without recognising that the GPS stream disappears underwater. FAIL if GPS loss is mentioned only in passing (for example a single "GPS dropouts" caveat) while the recommended architecture still depends on GPS as the primary position source during the dive.
