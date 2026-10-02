---
type: llm
---
Decaying specifics are prices, masses, payloads, release dates, version-support windows, library or firmware version claims, latency or throughput figures for specific hardware, and benchmark or success-rate figures. Stable identifiers do not count: package, class and parameter names (for example chunk_size, n_action_steps, temporal ensembling), paper or method names, and physical or arithmetic relationships. The user's own figures (30 fps, 120 ms, 8 Hz, chunk_size 100, about 60 demos, the SO-101 and Jetson names) and the user's own plan do not count either.

PASS if every decaying specific in the reply either carries a source link next to it or is absent. A reply that states no decaying specifics passes.

FAIL if the reply states such a figure with no source, for example a success rate or speedup from a paper, the inference time of some other model or runtime on a Jetson, a TensorRT or library version that added a feature, or the rate used by a named system, without a link next to it.
