---
type: llm
---
PASS if the reply commits to one concrete recommended path forward and gives its reasoning, for example: add a real odometry source to this cart (retrofit encoders, or lidar scan-matching odometry, optionally plus an IMU fused through an EKF), verify the odom->base_link transform is continuous by driving and watching it in RViz or tf tools, then tune AMCL. Naming a specific package or concrete step counts. Recommending one path while mentioning alternatives is fine.

FAIL if the reply only lists several options without picking one, only asks clarifying questions, or only restates the diagnosis without saying what to do next.
