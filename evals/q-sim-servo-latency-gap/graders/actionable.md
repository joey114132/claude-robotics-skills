---
type: llm
weight: 2
---
PASS if the reply recommends one concrete path forward and gives its reasoning. The path should include at least a measurement step on the real arm (for example logging commanded versus measured position under step or chirp commands, or replaying logged real actions open-loop in sim and comparing) and a concrete modeling or mitigation step (for example adding a fitted lag plus delay to the sim actuator, matching the servo gain settings, randomizing delay and gain around measured values, an action-smoothness penalty, or reducing the command gain or rate). It must be clear what the user should do first.

FAIL if the reply only lists options without choosing one, only asks clarifying questions, defers the whole answer until the user replies, or recommends generic steps with no first action.
