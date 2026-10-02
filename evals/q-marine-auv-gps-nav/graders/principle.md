---
type: llm
weight: 2
---
PASS only if the reply explains, in its own words, why GPS fails underwater and what replaces it, well enough for a practitioner to act on.

Required, all three:
1. Why: radio-frequency signals, GPS satellite signals included, do not reach a submerged receiver because seawater absorbs/attenuates them (conductivity of seawater, or simply "radio does not penetrate water"). Saying only "GPS doesn't work underwater" with no reason FAIL.
2. What replaces it: dead reckoning from DVL (or other bottom/water-relative velocity) plus heading/IMU or INS plus pressure depth, and the reply says this estimate drifts, with error growing over time or distance.
3. How drift is bounded: an absolute reference, either acoustic positioning (USBL or LBL) or a surfacing GPS fix. Naming DVL/USBL without saying dead reckoning drifts and needs an absolute reference FAIL.

Not required: sound speed, bandwidth or latency limits of acoustic links, or any specific product figure. A reply that adds them correctly is fine.

Also FAIL if the explanation is materially wrong, for example claiming that a better antenna or RTK corrections can restore a fix at 15 m depth, or that DVL dead reckoning does not drift.
