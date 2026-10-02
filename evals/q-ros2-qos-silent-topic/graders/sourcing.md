---
type: llm
---
Decaying specifics are prices, masses, payloads, release dates, version-support windows (for example "distro X is supported until year Y", "feature Z was added in release N"), and benchmark figures. Stable identifiers do not count: package names, CLI commands, QoS policy names, parameter names, class and message type names, standard numbers, and conceptual rules.

PASS if every decaying specific in the reply either carries a source link or is absent. A reply that contains no decaying specifics passes.

FAIL if the reply states any such figure or date, such as an EOL date, a Hz or latency benchmark, or the release a feature first appeared in, with no source link.
