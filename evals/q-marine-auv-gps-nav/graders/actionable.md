---
type: llm
weight: 2
---
PASS if the reply recommends one concrete path forward, with its reasoning, for how this AUV should navigate its 12 waypoints (for example: a specific sensor stack and estimator layout, which sensor feeds which state, what GPS is still used for, what the vehicle does if the DVL loses bottom lock or the fix is gone, and what to build or test first). It may name an alternative where the tradeoff is real, but it must commit to a recommendation.
FAIL if it only lists options or architectures without choosing one, or only asks clarifying questions without delivering a recommendation, or if its recommendation is still the GPS-driven stack as the primary submerged navigation source.
