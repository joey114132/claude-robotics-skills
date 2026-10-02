---
type: llm
---
Look for decaying specifics in the reply: prices, robot or actuator masses, payloads, torque or speed ratings of specific products, release dates, software version-support windows, and benchmark figures (speeds, success rates, training times). Figures that the user gave in the question (2.5 kg, 20 kg·cm, 0.5 m/s) do not count. Control-loop rates of published controllers (for example the MPC and WBC rates in the Mini Cheetah paper) and the 50 Hz RC servo frame rate are textbook-level facts and do not count. Stable identifiers (package or tool names such as Isaac Lab, OCS2, Pinocchio, standard numbers, textbook concepts) and physical relationships (for example, that a higher gear ratio reduces backdrivability) do not count either.

PASS if every such decaying specific either carries a source link (a URL the reader can open) or is absent from the reply. A reply that contains no decaying specifics passes.

FAIL if at least one such figure is stated with no source link, for example a quoted price of an actuator or servo, a specific mass or peak torque of a named commercial quadruped or actuator, a release date, or a benchmark number, with no link.
