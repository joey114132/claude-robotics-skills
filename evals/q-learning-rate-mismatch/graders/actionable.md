---
type: llm
---
PASS if the reply commits to one concrete recommended path forward and gives the reasoning for it. Examples of what counts are keeping the loop at the recorded rate and amortising inference with a named technique, or resampling the dataset to a lower rate and retraining with a rescaled chunk size, with an explanation of why that path was chosen. Mentioning one alternative alongside the recommendation is fine.

FAIL if the reply only lists several options without picking one, only asks the user clarifying questions, or only critiques the plan without saying what to do instead.
