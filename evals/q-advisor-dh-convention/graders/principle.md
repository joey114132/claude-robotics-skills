---
type: llm
---
PASS only if the reply explains the mechanism behind the DH convention trap well enough for a practitioner to act on it. The mechanism: the two conventions attach the link parameters to different links and order the four elementary transforms differently. In the modified (proximal, Craig) convention, a_{i-1} and alpha_{i-1} describe the link before joint i and are applied before the joint rotation theta_i and translation d_i, with frame i placed on joint axis i. In the standard (distal) convention, a_i and alpha_i describe the link after joint i and are applied after theta_i and d_i, with frames placed differently. Consequently the same numbers read with the other convention end up one index off and with a different frame layout, so the geometry is wrong by a structural amount that varies with pose rather than by a constant offset.

The reply must convey at least: (1) that the transform order and/or which index a and alpha attach to differs between the conventions, and (2) that this is why numerically correct table entries still give a wrong pose. It must give enough detail that the reader could write or fix the transform, for example stating both transform orders, or stating the one-index shift of a and alpha between the conventions.

FAIL if it only says the conventions "differ" or "are not compatible" without saying how, or if the stated mechanism is wrong (for example claiming the two conventions only differ in a sign, in units, or in the direction of the z axis).
