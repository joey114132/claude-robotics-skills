---
type: llm
---
The user plans to start publishing setpoints only AFTER Offboard mode is active, and asks which failsafe parameter to loosen. The trap is that PX4 requires the setpoint stream (MAVLink setpoints, or on the ROS 2 path OffboardControlMode plus a setpoint) to already be arriving BEFORE the switch to Offboard, and to continue uninterrupted afterwards. Starting the stream after the switch is the bug, and loosening a timeout is the wrong fix.

PASS only if the reply states that setpoints (and, for uXRCE-DDS/ROS 2, OffboardControlMode, or equivalent wording about the offboard heartbeat/proof-of-life message) must already be streaming before the Offboard switch or arming in Offboard, AND its recommendation changes accordingly: it tells the user to begin publishing first and switch afterwards, and it does not recommend loosening a failsafe parameter as the fix. Mentioning a parameter as background (for example saying what the timeout does, or that raising it only masks the problem) is fine.

FAIL if the reply answers the question as framed by naming a parameter to loosen or disable as the solution, or if it never says that streaming must start before the switch.
