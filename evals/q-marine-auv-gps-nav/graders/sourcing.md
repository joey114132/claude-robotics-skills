---
type: llm
weight: 1
---
PASS if every figure in the reply that decays over time (prices, masses, payloads, release dates, version-support windows, benchmark or accuracy figures for specific products, vendor depth or altitude ratings) either carries a source link next to it or is absent from the reply. A reply that contains no such figures passes.
FAIL if the reply states such a figure with no source link, for example a specific DVL model's price, altitude range or accuracy, a named product's release date, or a ROS distribution's support window, without a link.
Stable identifiers do not count and must not cause a FAIL: package and node names (robot_localization, navsat_transform_node, Nav2), standard numbers, textbook concepts, and physical relationships (for example drift growing with time, radio attenuation in seawater, sound speed in water as a general physical fact without a product-specific number).
