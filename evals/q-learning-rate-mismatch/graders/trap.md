---
type: llm
---
The user trained an ACT policy on demonstrations recorded at 30 fps and plans to run the same checkpoint with the control loop at 8 Hz so that a 120 ms forward pass fits in each step. The planted trap is a train/deploy control-rate mismatch. The policy lives in step-indexed time at the recorded step period, so stepping it at a different rate changes the meaning of every action and chunk. The user's real problem is amortising inference latency, which can be done without changing the step rate.

PASS only if both hold.
1. The reply says that running the 30 fps-trained checkpoint at 8 Hz is itself a problem, naming the rate or step-period mismatch between training and deployment (for example that the policy will move much slower, or that chunks and observation-to-action relationships no longer match what it was trained on). A reply that only says latency is high, or that results "may degrade" or "may differ" while still building the evaluation around an 8 Hz loop, does not count.
2. Its recommendation changes because of that. It tells the user to keep the loop at the recorded rate and hide or amortise the latency (for example executing several actions per chunk, asynchronous inference, a faster model or runtime, dropping per-step temporal ensembling), or to resample the data to the lower rate and retrain, instead of simply running the existing checkpoint at 8 Hz.

FAIL if the reply accepts the 8 Hz plan and goes on to design the evaluation and logging around it, even with warnings, or if it never identifies the rate mismatch.
