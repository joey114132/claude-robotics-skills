---
name: route-web-camera-judder-relay
description: "Collision: judder in a relayed web camera stream (video-relay-cadence) versus ROS 2 transport and QoS (ros2-master)."
tags: [routing]
expected_outcome: "Expected video-relay-cadence. The topic rate and arrival intervals are fine and the picture is jerky only in the browser relay, which points at frame sampling inside the relay. ros2-master covers QoS, discovery and executors, which the user has already ruled out."
max_turns: 3
timeout_seconds: 180
allowed_tools: [Read, Grep, Glob, Skill]
---
Our robot's wrist camera publishes 30 fps on a ROS 2 topic and `ros2 topic hz` shows a steady 30. But in the browser through our MJPEG web camera page the video judders every fraction of a second, even over a wired connection, and the relay is set to a max of 24 fps. Arrival times look even. What's going on and what should I change?
