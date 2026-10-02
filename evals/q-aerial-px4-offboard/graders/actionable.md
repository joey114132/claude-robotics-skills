---
type: llm
---
PASS if the reply commits to one concrete path forward for this user (for example: run a fixed-rate timer publishing the offboard heartbeat and a setpoint from node start, hold a safe setpoint such as the current position until the operator presses the button, then send the mode command and check the vehicle's reported state), with the reasoning for it. Secondary alternatives are fine as long as one recommendation is clear.

FAIL if the reply only lists options without choosing one, only asks clarifying questions, or only explains the cause without telling the user what to change in their node.
