---
type: llm
---
PASS if the reply commits to a concrete recommended path forward and gives the reasoning for it, for example: "implement the standard-DH transform that matches the datasheet and check it against the vendor's stated pose", or "convert the table to modified parameters by shifting a and alpha by one index and re-deriving the tool transform", with a stated reason for choosing that route over the alternative. A concrete way to confirm the fix (such as comparing against a known vendor pose or a reference library) is a plus but not required.

FAIL if the reply only lists several options or possible causes without recommending one, or only asks the user clarifying questions without delivering a recommendation, or defers the answer behind a question the user must answer first. Brief follow-up questions placed after a delivered recommendation are fine.
