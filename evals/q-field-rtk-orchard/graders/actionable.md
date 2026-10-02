---
type: llm
---
PASS if the reply commits to a concrete recommended path forward with reasoning, for example: use GNSS for coarse localization and headland/row selection, add a row-following sensor (LiDAR or camera) to hold lateral offset, fuse with IMU and wheel odometry, define slow/stop behaviour on fix degradation, and validate under full canopy before spraying.

FAIL if it only lists options or tradeoffs without choosing one, or only asks the user clarifying questions without giving a recommendation. Closing questions after a committed recommendation are fine.
