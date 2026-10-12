---
name: robot-data-health
description: "Use when recorded robot episodes (rosbag2, mcap or sqlite3) need checking before training or review: rerun playback looks choppy, cameras freeze or stutter in recordings, a dataset is about to go to imitation-learning training, or someone asks which episodes are bad. Scans every episode's camera topics for coverage, mid-episode gaps, multi-camera gaps that happen together (and whether they span publishers), duplicate publishers and publisher clock offset, then writes a keep/warn/drop CSV. Not for live topics (ros2 topic hz, bw), relay judder (video-relay-cadence), or training config and policy choice (robot-learning)."
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
---

# Robot Data Health

Act as the engineer who decides which recorded episodes are safe to train or review on, before anyone spends a GPU day on them. robot-learning owns whether to learn, the policy class and the training config. robot-perception owns sensor choice, calibration and time sync design. video-relay-cadence owns judder in a live relay. This skill owns the recorded bag: are the frames actually there, and if not, which side lost them.

Stutter in a replay is usually frames missing from the bag, not a viewer problem. `scripts/data_health.py` turns that check into one read-only command. A hand-made version of this scan on a dual-arm teleoperation robot found 19 of 76 episodes with wrist-camera loss.

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

## The data-health decision sequence

1. **Scope.** Which episodes (one, a day, the whole dataset) and which streams. The script reads camera topics only (`CompressedImage` and `Image`). It says nothing about joint states, actions or force, so a clean verdict covers the cameras and no more. Default: every episode under the dataset root, every camera topic.
2. **Thresholds.** Set `--hz` to the real camera rate (one number for all cameras, plus `--hz /topic=15` for each camera that runs at another rate, such as depth), `--gap` (seconds, default 1.0) to the longest hole a policy could tolerate, and `--min-cover` (percent, default 90). Coverage is frames divided by `hz * duration`, so a wrong `--hz` drops or flags healthy episodes. Deviate from the defaults when the task is slow enough to survive a longer gap, and say so in the answer.
3. **Run the scan.** Needs a ROS 2 environment (`rosbag2_py`); ask which distro, and for an mcap bag the `rosbag2_storage_mcap` plugin must be installed (the storage type is read from each bag's `metadata.yaml`). It only reads. On a shared robot, stream the script over stdin so nothing is left on the machine.
4. **Read verdicts, then causes.** Verdicts come first, causes second. The cause line for gaps that start together is the useful part: a gap spanning two publisher hosts points at the receiving side (recorder host, kernel, switch), and a gap inside one host points at that publisher.
5. **Decide per episode.** Drop means exclude from training. Warn means trim or fix and keep. Never delete a bag on a verdict. Write the CSV, keep the bags, and let the training manifest do the excluding.
6. **Prevent the next one.** Take the cause to its owner: the recorder (messages lost, disk, drain rate), the network (fragmentation, discovery), the publisher (clock sync, duplicate node). If the cause is unknown and the fault is intermittent, call the robot-fault-hunter agent for a capture plan. Add this scan to the end of each recording session so a bad day is found on that day.

## Run

```bash
bash -c 'set +u; source /opt/ros/<distro>/setup.bash; python3 ${CLAUDE_SKILL_DIR}/scripts/data_health.py <dataset_root> --hz 30 --hz /<depth_topic>=15 --csv <out.csv>'
# on a remote robot, without copying a file there:
ssh <robot-host> 'bash -c "set +u; source /opt/ros/<distro>/setup.bash; python3 - <dataset_root>"' < ${CLAUDE_SKILL_DIR}/scripts/data_health.py
```

| Verdict | Meaning | Action |
|---|---|---|
| drop | a camera below min coverage, a mid-episode gap, or cameras gapped together | exclude from training |
| warn | late start or early stop, duplicate publisher, header clock offset | trim or fix, keep |
| keep | nothing found | use |

Speed was 2.5 s for two episodes (1.5 GB) on a laptop. The host key in the cause line is the topic minus its last two segments.

## Modern scan

**Live scan on every invocation.** Start from `references/landscape.md`, a dated snapshot in which every entry carries its source, then re-verify with fresh search before presenting: confirm that the entries you use still hold and look for newer options. When the live scan contradicts or postdates the snapshot, answer from the fresh finding. Write it back into `references/landscape.md`, bumping its Verified date, only when this skill directory is a git checkout that the user maintains; a marketplace install lives in a plugin cache that the next update overwrites.

## Gotchas

- **Coverage above 150% is not a good sign.** It means two nodes publish the same topic, which showed up as 238% to 633% on head camera episodes of a teleoperation robot. The data doubles and timestamps interleave from two sources.
- **Header clock offset does not drop an episode, but it breaks anything that syncs on header stamps.** Single-board computers on the robot's hands were hours off in different weeks. Align on record time, or fix NTP on the publisher. The scan samples only the first 30 header stamps per topic, so a clock that steps mid-episode is missed.
- **A late camera start is trimmable, not fatal.** A 104 s episode whose left cameras came up 2.2 s late is a warn with a trim range. Dropping it would throw away 102 s of good data.
- **The rosbag2 "messages lost on the transport layer" count is not in the bag.** Read it from the recorder log. Values near 2^31 are counter wrap and mean nothing.
- **Gaps of about 30 s that recur across every camera point at IP fragment reassembly** (`net.ipv4.ipfrag_time`, default 30 s, per the ROS 2 DDS tuning guide). Check `ReasmFails` in `/proc/net/snmp` on the receiver before blaming the cameras. Large image samples fragment, so this hits camera topics first.
- **A wrong `--hz` fakes a whole dataset of failures.** A 15 fps camera scanned at `--hz 30` shows 50% coverage on every episode, and one `--hz` for a rig that mixes RGB at 30 with depth at 15 fails every episode. Check the real rate of each camera with one episode, then set `--hz /topic=N` for the odd ones.
- **A bag with no camera topic is a drop, not a keep.** The scan reports "no camera topics" so a joint-only or mis-named recording cannot pass as clean.
- **On a shared robot, `pgrep -af "<text>"` inside an ssh command matches the ssh command itself.** Use `pgrep -f "^ros2 bag record"` or read `/proc/<pid>/cmdline`. A false "recording" result once let a probe run beside what looked like a live recording.
- **A clean camera verdict says nothing about action alignment.** Frames can all be present and still sit seconds away from the joint stream that labels them, so check camera-to-state alignment separately before training.
