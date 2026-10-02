---
type: llm
---
The mechanism behind the trap: PX4 treats Offboard as externally supplied control that must be continuously proven alive. The offboard stream is a proof-of-life signal. PX4 refuses to enter Offboard if it has not recently received it, and leaves Offboard (applying the offboard-loss failsafe) if it stops for longer than a timeout. A timeout parameter therefore cannot substitute for a stream that was never started, and a publisher that sends only on events, or stalls, will keep tripping it.

PASS only if the reply explains this mechanism well enough for a practitioner to act on: it says the stream is checked both at the moment of switching and continuously afterwards, that a loss of stream beyond a timeout makes PX4 exit Offboard into a failsafe, and it gives an actionable publishing pattern (a steady periodic timer-driven publisher at a rate above the roughly 2 Hz minimum, kept running the whole time the vehicle is in Offboard). It must say or clearly imply the stream is not optional once started, not merely that it is "recommended".

FAIL if the reply only asserts "stream first" without explaining why PX4 behaves this way, gives no publishing pattern or rate guidance, or treats the stream as needed only at the instant of the switch.
