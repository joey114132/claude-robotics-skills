---
type: llm
---
Decaying specifics are things that go stale or that a reader cannot check from the name alone: prices, masses, payloads, release dates, edition years or withdrawal dates, version-support windows, benchmark figures, failure-rate or latency numbers quoted as facts about a named product.

Stable identifiers do not count and must not be penalised: standard numbers (ISO 13849-1, ISO 13850, IEC 60204-1, IEC 61508, IEC 62061, IEC 61800-5-2, with or without a part number), package names, textbook concepts, category names (Category 3), PL letters, physical relationships, and Linux or ROS 2 feature names such as SCHED_FIFO.

PASS if every decaying specific in the reply either carries a source link or is absent. A reply with no such figures at all passes.
FAIL if the reply states a decaying specific with no source: for example an edition year or transition deadline for a standard, a price, a measured jitter or latency figure, a PFHd value for a named product, or a vendor product specification, with no link.
