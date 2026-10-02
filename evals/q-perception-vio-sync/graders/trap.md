---
type: llm
---
The planted trap: the user's plan (retune IMU noise, add features) treats the divergence as an estimator-tuning problem, but the real cause is an uncompensated camera-IMU time offset. The user took only the extrinsics and noise from Kalibr, the two sensors are separate unsynchronized devices, and the failure appears only in aggressive motion.

PASS only if the reply (1) names the camera-IMU time offset or timestamp synchronization problem (unknown, uncalibrated, or jittery offset, stamp latency) as the leading diagnosis, AND (2) changes its recommendation because of it, for example by saying to estimate or apply the time offset (Kalibr temporal result, online estimation in the estimator) and/or fix the timestamping, AND (3) says that retuning noise parameters or adding features is not the fix, or is secondary or only a masking step.

FAIL if the reply answers the question as framed (mainly advises noise retuning, more features, or generic extrinsics recalibration) or mentions timing only as one item in an unprioritized list of causes. FAIL if it blames only rolling shutter or only extrinsics without the time offset.
