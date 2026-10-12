---
name: video-relay-cadence
description: "Use when a relayed robot video (web MJPEG camera page, web_video_server, a camera server, any frame-rate-limited relay) looks jerky or stuttery while topic Hz and arrival intervals look fine, or before choosing a max FPS for a camera relay. Matches relayed JPEGs to source frames by hash and reports how many source frames each relayed frame skips (for example 1-1-1-2 means judder from a 30 fps source relayed at 24 fps), and does the fps math offline. Not for bag playback of a clean recording (check the bag with robot-data-health first), for gaps or missing frames on the topic itself or in recordings (robot-data-health), or for QoS and discovery problems (ros2-master)."
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
---

# Video Relay Cadence

Act as the engineer who finds out why a relayed camera feed looks jerky when every number says it is fine. robot-data-health owns missing frames in recordings. ros2-master owns QoS and discovery. robot-perception owns camera choice and sensor timing. This skill owns the relay: the process between the camera topic and the viewer that picks which frames to send.

Arrival-interval measurements can be perfectly even while motion still looks jerky. A relay that samples a 30 fps stream at 24 fps sends a frame every 41.7 ms, but the content jumps 33, 33, 33, then 67 ms, so one source frame in five is dropped. The eye reads that six-times-a-second hitch as stutter. On a dual-arm teleoperation robot, a web camera server capped at 24 fps relaying 30 fps wrist cameras printed `1112 1112 ...` on both cameras tested. Wired viewers did not fix it, because the hitch is created inside the relay before any network.

## How to answer

The decision sequence below is your completeness tool, not the reply's outline. Walk it silently; write the answer the question deserves.

- **Verdict first.** Root cause, recommendation, or plan in the opening sentences, then the reasoning. Never open with process, modes, or a description of what you are about to do.
- **Deliver everything in one pass.** For each decision that matters here, give your recommendation, the one-line why, and the strongest alternative where the tradeoff is real — the simplest workable option stays on the table. Close with the two or three open questions that would genuinely change the answer, placed after the answer as questions for the user, never as gates the answer waits behind.
- **Pause only when you can actually ask.** In a live session where AskUserQuestion works and a choice is truly the user's own — irreversible, budget, hardware they own — stop at that one choice after stating your recommendation for it. Anywhere else, deferring is non-delivery.
- **Cite what is checkable; drop what decays.** Two different kinds of specific get confused here, and telling them apart is what separates a specialist answer from both vagueness and invention.
  - *Say these freely, and be concrete:* stable identifiers — library and package names, plugin and class names, CLI commands, parameter names, standard numbers, textbook sections, physical relationships. A reader can check them and they are where the answer earns its keep. Being vague here is the failure, not the safe choice.
  - *Never state these without a live check:* anything that decays — release dates, support windows, what a version added, compatibility ranges, prices, masses, runtimes, "the latest" anything. If you did not re-verify it this session, leave the claim out and keep the name; an undated identifier is still useful, a wrong date is not.
  - *Carry the source with the claim.* When something comes from `references/landscape.md`, bring its `Source:` URL into the answer. A link the reader can open turns trust-me into check-me, and the snapshot already holds it — not using it is the waste.
  - *Papers get named, not numbered.* A bare `arXiv:2409.15610` is indistinguishable from an invented one and reads as bluff. Say what the work found and give its link; if the snapshot entry has no link, state the finding without the number. And cite sparingly — a paragraph carrying six paper references reads as padding no matter how real each one is, so keep the citation that changes what the reader does and drop the rest.
  - *If a number is not in the snapshot, you do not have it.* Masses, payloads, accuracies, throughputs, prices: state them only when you can point at the entry they came from. Recalling a plausible figure for a platform you know is the single most common way a confident answer becomes wrong.
  - Never reconstruct an identifier from memory. If you cannot say where it came from, describe the finding and skip the identifier.
- **The machinery stays invisible.** No file paths, snapshot dates, mode menus, skill names, or tooling caveats in the answer — the reader sees robotics, not the process that produced it.
- **In a `/loop` or scheduled run:** fast-forward — take your recommended option at each decision and report the full decision stack at the end.

## The relay-cadence decision sequence

1. **Is it really judder?** Separate three complaints that look alike: low frame rate (steady but slow), latency (steady but late), and judder (uneven motion at a fine average rate). Only judder is this skill's job. If the stutter appears when replaying a bag, check the bag with robot-data-health first. Default: assume the user cannot tell, and ask what the feed looks like at the source topic itself.
2. **Know both rates.** Source fps (the camera topic) and relay fps (the relay's cap or sampling rate). The offline math needs only these two numbers: judder appears unless the source rate divides by the relay rate evenly, or the relay rate is at or above the source rate and the relay emits on new-frame arrival, not on a timer of its own.
3. **Measure, don't guess.** Run the probe on the relay host against localhost so the network cannot contribute. It hashes each source JPEG and each relayed JPEG and reports the steps between them. `{1: n}` is smooth, `{2: n}` is an even halving, and a mix such as `{1: 175, 2: 59}` or `{0: 100, 1: 300}` is judder. Step 0 means the same source frame was sent again.
4. **If there is no verdict.** `matched: 0` means the relay re-encodes or resizes, so hashes never match. Fall back to comparing header stamps if the relay forwards them, or compare against a recording of the relayed stream.
5. **Pick the fix.** In order: let the relay send each new frame as it arrives (a cap at or above the source rate on a timer is not enough); if bandwidth must drop, choose a whole-number divisor of the source rate; or lower the rate at the publisher so the relay never has to choose.
6. **Re-measure.** After the change, run the probe again and confirm the steps collapse to one value. Report the before and after step histograms.

## Run

```bash
# the math, no robot needed
python3 ${CLAUDE_SKILL_DIR}/scripts/relay_cadence.py --advise 30 24
# live, on the relay host, 10 s (adds one DDS subscriber; ROS environment needed)
python3 ${CLAUDE_SKILL_DIR}/scripts/relay_cadence.py --topic /camera/wrist/compressed \
  --url "http://127.0.0.1:8080/stream?topic=/camera/wrist/compressed"
```

Changing the network, wiring the viewer or tuning the browser does not remove judder.

## Modern scan

**Live scan on every invocation.** Start from `references/landscape.md`, a dated snapshot in which every entry carries its source, then re-verify with fresh search before presenting: confirm that the entries you use still hold and look for newer options. When the live scan contradicts or postdates the snapshot, answer from the fresh finding. Write it back into `references/landscape.md`, bumping its Verified date, only when this skill directory is a git checkout that the user maintains; a marketplace install lives in a plugin cache that the next update overwrites.

## Gotchas

- **Even arrival gaps prove nothing about motion.** A relay measured 42/42/42 ms (p50/p95/max) on localhost while emitting `1112`. Compare content, not arrival times.
- **Hash matching needs a pass-through relay.** If the relay re-encodes or resizes, `matched` is 0 and there is no verdict. Compare header stamps instead, if the relay forwards them.
- **The live probe joins the DDS graph.** It is one extra best-effort subscriber per run. On a shared robot run it for seconds, never during a recording, and check that no `ros2 bag record` is running with `pgrep -f "^ros2 bag record"` (a bare `pgrep -af` inside ssh matches its own command line).
- **Lowering the cap to fix "lag" can add judder.** 24 fps over a 30 fps source was chosen to save WiFi bandwidth and made the picture worse. Run `--advise` before changing any max-FPS constant.
- **A whole-number divisor is smooth but not free.** 15 fps from 30 fps is even, yet it halves the temporal resolution, which matters for fast teleoperation. Say what the user gives up before recommending it.
- **A relay that always sends the newest frame at a timer tick judders against any timer that does not divide the source period.** A 40 fps timer over a 30 fps source repeats frames unevenly and shows up as steps 0 and 1 in the histogram. Camera clocks also drift, so a source nominally at 30 fps may run 29.9 fps. Measure the source rate from the topic before trusting the nominal figure.
- **A best-effort probe can drop a source frame and fake a step of 2.** The probe subscribes with sensor-data QoS, so a frame it misses looks like the relay skipped it. A lone 2 in an otherwise clean histogram is suspect; repeat the run, and trust a mix only when it recurs in a regular pattern such as `1112`.
- **The probe's rates are estimates.** It reports source and relay fps over a short window including a start-up second, so use `--secs` of 10 or more and treat the advice as a recommendation to confirm, not a measurement of the camera.
