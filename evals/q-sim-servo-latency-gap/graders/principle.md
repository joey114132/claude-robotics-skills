---
type: llm
weight: 2
---
PASS only if the reply explains a causal mechanism, in its own words, for why the policy shakes on the real arm. Both parts must be present. (a) The simulated joints respond to the policy's commands immediately and with simplified dynamics, while the real chain adds delay (serial bus, sensing, control-loop timing) and/or the servo's own inner position loop and actuator lag (its P/I/D gains, speed or torque limits, deadband or backlash). (b) Why that produces overshoot and oscillation: the policy was optimized against a plant that reacts faster and with less phase lag than the real one, so the added lag or delay reduces the stability margin of the closed loop and the policy overshoots and chatters (equivalent wording such as "it acts like a high-gain loop on a delayed plant" or "it exploits the fast response" passes). Mentioning only the word "latency" or "actuator" with no account of why it causes shaking is a FAIL.

FAIL if the explanation is only about mass, friction, contact or a generic "sim-to-real gap", or if the mechanism is stated incorrectly, for example blaming the 2 ms physics step or the 30 Hz policy rate alone without tying it to delay or actuator lag.
