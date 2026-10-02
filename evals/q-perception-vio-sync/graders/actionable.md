---
type: llm
---
PASS if the reply commits to one concrete recommended path forward with reasoning, for example an ordered plan of what to do first and why, rather than a menu. The path may include confirming the diagnosis cheaply, such as logging the IMU and image timestamp deltas, or testing slow versus fast motion.

FAIL if the reply only lists options without recommending one, or only asks the user clarifying questions without giving a recommendation, or defers the answer until the user replies. Closing questions placed after a committed recommendation are fine.
