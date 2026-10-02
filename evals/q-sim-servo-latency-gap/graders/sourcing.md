---
type: llm
weight: 1
---
PASS if every decaying specific in the reply either carries a source link or is absent. Decaying specifics are prices, masses, payloads, release dates, firmware or software version-support windows, and benchmark or performance figures (for example the servo's torque, stall current or bus baud rate, firmware release facts, a throughput number, or a success-rate figure attributed to a paper). Stable identifiers do not count: package and library names, register names such as P_Coefficient, MuJoCo options, standard numbers, textbook concepts, physical relationships, and values the user supplied in the prompt.

FAIL if the reply states such a decaying specific with no source link next to it.
