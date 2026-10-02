---
type: llm
---
Decaying specifics are prices, masses, payloads, release dates, version-support windows, benchmark figures, and statements about what a specific PX4 release added or changed. Stable identifiers (package names, message names, parameter names, standard numbers, physical or protocol relationships) do not count, nor does the roughly 2 Hz offboard proof-of-life minimum or the existence of a timeout parameter, and neither does generic advice like "publish at a steady rate" or an engineering-recommended rate stated as advice.

PASS if every decaying specific in the reply either carries a source link or is absent. A reply containing no such specifics passes.

FAIL if the reply states a decaying specific with no source link, for example "since PX4 v1.14 the minimum rate is ...", a release date, a version-support claim, or a benchmark figure with no link.
