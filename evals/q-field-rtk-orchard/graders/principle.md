---
type: llm
---
PASS only if the reply explains the mechanism well enough for a practitioner to act on. It must state the physical cause: foliage and trunks attenuate or block satellite signals, leaving fewer usable satellites, and reflected signals cause multipath. It must also state the consequence for RTK: carrier-phase ambiguity resolution is lost or degraded, so the receiver drops to float or standalone, or can report a wrong fixed solution with a small covariance. It must also say what to do about the consequence, for example gating on fix type, covariance and agreement with dead reckoning, a degraded-fix policy, or testing under full leaf canopy.

FAIL if it only says "GNSS is unreliable under trees" with no cause, or names the cause with no consequence for the fix state, or gives neither a gating nor a test implication.
