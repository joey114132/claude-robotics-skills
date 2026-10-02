---
type: llm
---
Check every decaying specific in the reply: prices, masses, payloads, release dates, version-support windows (for example which ROS distro supports which package or when a package was released), and benchmark figures (accuracy or error numbers for a particular odometry method or sensor).

PASS if every such figure either carries a source link or is absent. A reply with no decaying specifics passes. FAIL if any such figure is stated without a source link.

Do not count stable identifiers: package names (nav2_amcl, robot_localization), parameter names and default values taken from configuration, standard numbers (REP 105), textbook concepts, and physical relationships.
