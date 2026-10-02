---
type: llm
---
PASS if the reply recommends one concrete path forward and gives the reasoning for it. A concrete path here means naming the architecture it would build: for example a safety-rated dual-channel e-stop device into a safety relay or safety PLC that removes power via contactors or drive STO, with the ROS 2 node reading the stop state for graceful behaviour and logging, and the achieved PL calculated and documented. It must say what to do with the existing node and what to do about the PL d claim (verify the achieved PL with calculation, document it, or push back on the spec if needed). Naming an alternative is fine as long as one option is clearly recommended.

FAIL if the reply only lists options without choosing one. FAIL if it only asks clarifying questions or defers the recommendation until the user answers. FAIL if its recommendation is just to continue the software node design with minor tweaks.
