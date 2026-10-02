---
type: llm
---
Look at every figure in the reply that decays over time: prices, masses of specific products, payloads, release dates, version-support windows, software version numbers, benchmark figures. Stable items do not count. These include package and function names, standard numbers, physical relationships and unit conversions (1 g = 1e-3 kg, 1 g*mm^2 = 1e-9 kg*m^2), the user's own numbers, and arithmetic derived from them.

PASS if every such decaying figure either carries a source link or is absent. A reply with no decaying figures at all PASSES.

FAIL if the reply states a decaying figure with no source. Examples: "Gazebo Harmonic supports X as of version N", a recommended step size or damping value presented as a vendor or documentation default, or a claim of what a specific release added.
