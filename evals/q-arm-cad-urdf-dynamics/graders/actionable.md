---
type: llm
---
PASS if the reply answers the user's actual question (what damping and step values) by redirecting: it says to fix the inertial values first and that raising damping or shrinking the step would only mask the error or not cure it, and it gives a concrete order of work with a check afterwards. A good check is a hand estimate per link (such as 1/12*m*L^2), that gravity torques come out at a plausible magnitude for the real arm, or that each inertia tensor is positive definite and satisfies the triangle inequality.

FAIL if the reply only lists options without recommending one, only asks the user questions, or supplies damping and step values as the fix without telling the user to correct the inertials first.
