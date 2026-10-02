---
type: llm
---
The mechanism: the estimator fuses each image with the IMU-propagated state at the image's timestamp. If the stamp is off by a time error td, each image is paired with the state from the wrong instant, so the visual residual is wrong by about the motion rate times td (angular rate times td for orientation, velocity times td for position). During slow motion this is small and the filter absorbs it. During sharp turns or bumps it grows large, and a jittering stamp (variable delay) cannot be removed by one constant offset.

PASS only if the reply (a) connects the error to the image being associated with the wrong inertial state or time, (b) explains why it shows up under fast rotation or bumps but not at slow speed (error scales with motion rate), and (c) gives at least one concrete way to act on it, such as estimating the offset offline or online, obtaining better (driver, exposure-time, or hardware) timestamps, or checking timestamp jitter.

FAIL if the reply only says the problem is "synchronization" with no explanation of why it scales with motion. FAIL if it explains the mechanism but gives nothing to act on.
