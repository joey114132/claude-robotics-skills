---
type: llm
---
The trap: the user blames DDS discovery or networking and plans to switch RMW, pin the domain, and sniff UDP multicast. The real likely cause is a QoS incompatibility. An rclpy subscription created with depth 10 defaults to RELIABLE, many lidar drivers publish BEST_EFFORT (sensor-data profile), and a RELIABLE subscription cannot match a BEST_EFFORT publisher, so the callback silently never runs. Both nodes are on the same Pi, which makes network discovery an unlikely cause.

PASS only if the reply names a reliability (or durability) QoS incompatibility between the subscriber and the publisher as the probable or leading cause (hedging such as "most likely, confirm with ros2 topic info" is fine), AND its recommendation changes because of it: the first step is to inspect the QoS of both endpoints (for example `ros2 topic info /scan --verbose`) and/or to change the subscriber's QoS to match (for example sensor-data / BEST_EFFORT), and the CycloneDDS switch and UDP sniffing are demoted, deferred, or called unnecessary.

FAIL if the reply endorses the user's plan (RMW switch, domain pinning, UDP listener) as the first step, treats QoS only as an afterthought in a list of equal options, never identifies QoS mismatch as the likely cause, or blames the callback code.
