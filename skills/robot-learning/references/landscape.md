# Robot Learning Landscape — verified snapshot

**Verified: 2026-08-05.** Entries were confirmed against live sources on this date — re-verify anything before relying on it if this snapshot is more than ~6 months old.

Entry format: **Name** — one-line what-it-is. Status: maintained / research / commercial. Source: `<url>`

---

## Imitation-learning toolkits & dataset standards

- **LeRobot** — Hugging Face's end-to-end robot learning library; `LeRobotDataset` v3.0 stores synced video (MP4) + state/action as Parquet, streamable from the HF Hub without full download. Ships trainable implementations of ACT, Diffusion Policy, pi0, SmolVLA behind one CLI. Status: maintained. Source: https://huggingface.co/docs/lerobot/lerobot-dataset-v3 (also https://github.com/huggingface/lerobot)
- **Open X-Embodiment / RT-X** — cross-embodiment dataset standard assembled from 22 robots across 21 institutions (527 skills, 160k+ tasks); the RT-X models trained on it show positive transfer across robots. Status: research (dataset actively used as a pretraining source). Source: arXiv 2310.08864 — https://arxiv.org/abs/2310.08864
- **AgiBot World** — Shanghai-based AgiBot's dataset: 1M+ trajectories across 217 tasks in 5 deployment scenarios, extensible to dexterous hands and visuo-tactile sensors; underlies the GO-1 policy. Status: maintained (open-sourced). Source: arXiv 2503.06669 — https://arxiv.org/abs/2503.06669

## Data quality, scaling, and corrective data

- **Data Scaling Laws in Imitation Learning** — 40k+ demos / 15k+ real rollouts; generalization follows a rough power law in number of *environments* and *objects*, and diversity matters far more than absolute demo count — past a per-environment/per-object threshold, extra demos add little. Status: research (widely cited practical guidance). Source: arXiv 2410.18647 — https://arxiv.org/abs/2410.18647
- **The Curse of Precision** — data scaling law for high-precision closed-world tasks: demos needed for a fixed success rate grow super-exponentially as target precision approaches a limit c, log(N) ∝ 1/(P−c); c is an emergent system property (sensors, expert), lowered by e.g. adding a wrist camera. Status: research. Source: arXiv 2607.23108 — https://arxiv.org/abs/2607.23108
- **RINSE (smoothness-driven data quality)** — policy-agnostic demo scoring from trajectories alone using Spectral Arc Length and a contact-aware Trajectory-Envelope Distance; SAL filtering gave 16% higher success with one-sixth of the data on RoboMimic, TED 20% higher with half the data on real hardware. Status: research (practical offline diagnostic). Source: arXiv 2604.23000 — https://arxiv.org/abs/2604.23000
- **SARM / RA-BC** — stage-aware video reward model used to filter and reweight demonstrations of inconsistent quality; T-shirt folding 83% vs 8% for vanilla BC from the flattened state. Status: research. Source: arXiv 2509.25358 — https://arxiv.org/abs/2509.25358
- **PGDG** — physics-grounded generation of recovery behaviors around risky off-manifold states from a single demonstration; RotateBox-Pitch 35% → 82% real-world, and lifts GR00T fine-tuning 46% → 77%. Status: research. Source: arXiv 2605.21710 — https://arxiv.org/abs/2605.21710
- **RoboPocket** — robot-free interactive policy iteration from a phone: AR "visual foresight" shows the policy's predicted trajectory so collectors record where the policy is weak, with asynchronous online finetuning; reports ~2x data efficiency over offline scaling. Status: research. Source: arXiv 2603.05504 — https://arxiv.org/abs/2603.05504
- **HiL-ResRL** — model-agnostic residual policy trained with human-in-the-loop RL on top of a frozen BC/VLA policy to correct imitation distribution shift; >95% average real-robot success after ~1.5 h of online training. Status: research. Source: arXiv 2606.22860 — https://arxiv.org/abs/2606.22860

## Policy architectures (arXiv IDs)

- **ACT (Action Chunking with Transformers)** — generative model over action-chunk sequences for low-cost bimanual manipulation; basis of the ALOHA stack. Status: maintained (widely reused). Source: arXiv 2304.13705 — https://arxiv.org/abs/2304.13705
- **Diffusion Policy** — represents visuomotor policies as a conditional denoising-diffusion process over action sequences; handles multimodal action distributions well. Status: maintained. Source: arXiv 2303.04137 — https://arxiv.org/abs/2303.04137
- **π₀ (pi0)** — flow-matching VLA architecture from Physical Intelligence built on a pretrained VLM backbone, trained across single-arm, dual-arm, and mobile-manipulator platforms. Status: maintained/commercial. Source: arXiv 2410.24164 — https://arxiv.org/abs/2410.24164
- **SmolVLA** — ~450M-parameter compact VLA (compact VLM + flow-matching action expert) trained on 481 community LeRobot datasets; trains on one GPU, runs on consumer GPU/CPU. Status: maintained. Source: arXiv 2506.01844 — https://arxiv.org/abs/2506.01844
- **Why Does Action Chunking Improve BC?** — controlled study (sim + real) rejecting temporal consistency, horizon reduction, and representation learning as explanations; the real mechanisms are non-Markovian expressivity plus reduced compounding error, and an *implicit ensembling* effect from learning many temporal relationships at once. Chunk-size behavior is reproducible with randomized-delay policy ensembles. Status: research (mechanism explanation, directly actionable for chunk-size tuning). Source: arXiv 2608.02547 — https://arxiv.org/abs/2608.02547

## VLA / generalist models — global

- **RT-2** — Google DeepMind VLA that co-fine-tunes a VLM on robot trajectories and web vision-language data, expressing actions as text tokens; showed emergent semantic generalization. Status: research (superseded internally by Gemini Robotics line). Source: arXiv 2307.15818 — https://arxiv.org/abs/2307.15818
- **OpenVLA** — open-source 7B VLA (Llama-2 + DINOv2/SigLIP visual features) trained on 970k Open X-Embodiment demonstrations; outperformed the closed 55B RT-2-X at 7x fewer parameters. Status: maintained (open weights). Source: arXiv 2406.09246 — https://arxiv.org/abs/2406.09246
- **Octo** — open-source generalist transformer policy trained on 800k Open X-Embodiment trajectories, fine-tunable to new sensors/action spaces in hours on a consumer GPU. Status: maintained (research release). Source: arXiv 2405.12213 — https://arxiv.org/abs/2405.12213
- **Physical Intelligence π-series (π0 → π0.7)** — commercial generalist robot foundation model line: π0 (Oct 2024, prototype), π0-FAST (Feb 2025), π0.5 (Apr 2025, open-world generalization), π0.6 (Nov 2025, RL-improved success/throughput), π0.7 (Apr 2026, steerable generalist with emergent capabilities). Status: commercial. Source: https://www.pi.website/blog
- **Gemini Robotics 2** — Google DeepMind's current VLA generation: Gemini Robotics 2 (whole-body humanoid + dual-arm control), Gemini Robotics-ER 2 (embodied reasoning/multi-robot planning), Gemini Robotics On-Device 2 (local inference, few-shot embodiment adaptation). Status: commercial/research preview. Source: https://deepmind.google/models/gemini-robotics/

## VLA / generalist models — Chinese ecosystem

- **AgiBot GO-1 (Genie Operator-1)** — Shanghai AgiBot's ViLLA (Vision-Language-Latent-Action) generalist policy: InternVL-2B VLM + latent-action planner + MoE action expert; +30% over Open-X-trained baselines, deployable across embodiments. Status: maintained (open-sourced). Source: arXiv 2503.06669 — https://arxiv.org/abs/2503.06669
- **RoboBrain 2.0** — BAAI (Beijing Academy of AI) embodied vision-language foundation model (7B/32B variants) unifying spatial understanding (affordance, trajectory forecasting) and temporal decision-making for embodied tasks. Status: maintained (open checkpoints). Source: arXiv 2507.02029 — https://arxiv.org/abs/2507.02029
- **Unitree UnifoLM-VLA-0** — Unitree's open-sourced VLA (built on Qwen2.5-VL-7B, continually pretrained on robot + general data) for general-purpose humanoid manipulation on the G1 platform; completed 12 manipulation-task categories with a single policy. Status: maintained (open-sourced Jan 2026). Source: https://github.com/unitreerobotics/unifolm-vla
- **UBTech Thinker stack (Thinker VLA / Thinker WM)** — UBTech's embodied large-model stack (VLA + world model) underlying its commercial humanoid deployments (Airbus, Foxconn, Audi FAW partnerships in early 2026). Status: commercial. Source: https://www.techtimes.com/articles/318641/20260618/humanoid-robots-china-ships-90-global-units-now-leads-ai-benchmarks.htm

## RL frameworks for robotics

- **NVIDIA Isaac Lab** — GPU-accelerated, open-source robot-learning framework (successor to Isaac Gym/OmniIsaacGymEnvs/Orbit) built on Isaac Sim; integrates RL-Games/RSL-RL/SKRL, 30+ ready environments, domain randomization, multi-frequency sensor sim. Status: maintained (official NVIDIA framework). Source: arXiv 2511.04831 — https://arxiv.org/abs/2511.04831 (also https://github.com/isaac-sim/IsaacLab)
- **Isaac Gym (Preview Release) — deprecated.** NVIDIA's legacy standalone RL simulator; no longer supported, migration path is Isaac Lab. Status: deprecated. Source: https://developer.nvidia.com/isaac-gym
- **Genesis** — open-source, Python-native generative physics platform; reports 430,000x real-time simulation speed for a Franka arm on a single RTX 4090, plus a VLM-driven scene/task generator. ~14k GitHub stars. Status: maintained. Source: https://github.com/Genesis-Embodied-AI/genesis-world (project page https://genesis-embodied-ai.github.io/)
- **MuJoCo Playground** — Google DeepMind's open-source GPU-accelerated robot-learning suite built on MuJoCo MJX (JAX) with optional MuJoCo Warp backend; 50+ environments (locomotion, manipulation, dexterous hands) with demonstrated sim-to-real transfer to Unitree Go1/G1, Berkeley Humanoid. Status: maintained. Source: https://github.com/google-deepmind/mujoco_playground

## Teleop data-collection rigs

- **ALOHA / Mobile ALOHA** — low-cost bimanual (and mobile, whole-body) teleoperation rig; Mobile ALOHA adds a mobile base and co-training with static-ALOHA data for tasks like cooking and elevator use. Status: maintained (widely replicated hardware design). Source: arXiv 2401.02117 — https://arxiv.org/abs/2401.02117
- **UMI (Universal Manipulation Interface)** — hand-held gripper + interface design that captures in-the-wild human demonstrations and deploys the resulting policy hardware-agnostically across robot platforms. Status: maintained (open hardware+software). Source: arXiv 2402.10329 — https://arxiv.org/abs/2402.10329
- **GELLO** — low-cost, 3D-printed, kinematically-matched leader arm for intuitive teleoperation of Franka/UR5/xArm followers; outperforms VR controllers and spacemice in a user study for demonstration quality. Status: maintained (open hardware+software). Source: arXiv 2309.13037 — https://arxiv.org/abs/2309.13037

## Evaluation benchmarks

- **LIBERO** — lifelong-robot-learning benchmark, 4 task suites (130 tasks total) with human-teleoperated demos, targeting declarative vs. procedural knowledge transfer questions. Status: maintained. Source: arXiv 2306.03310 — https://arxiv.org/abs/2306.03310
- **RoboCasa** — large-scale kitchen-focused household simulation benchmark; 150+ object categories, generative-AI-authored assets/textures, 100 systematic tasks (25 atomic + 75 composite), 100k+ generated trajectories. Status: maintained. Source: arXiv 2406.02523 — https://arxiv.org/abs/2406.02523
- **SIMPLER (SimplerEnv)** — simulated evaluation suite that mitigates real/sim control and visual gaps to correlate simulated policy performance with real-world results on Google Robot / WidowX+Bridge setups. Status: maintained. Source: arXiv 2405.05941 — https://arxiv.org/abs/2405.05941
- **RoboDojo** — unified sim-and-real benchmark for generalist manipulation policies: 42 sim tasks (generalization, memory, precision, long-horizon, open-vocabulary) + 18 real tasks, with RoboDojo-RealEval offering remote standardized real hardware, scene reset, and a fixed protocol; 30 policies integrated on a public leaderboard. Status: maintained. Source: arXiv 2607.04434 — https://arxiv.org/abs/2607.04434
- **AutoEval** — autonomous around-the-clock real-world policy evaluation with automatic success detection and scene resets; results track hand-run ground-truth evaluations, public scenes on BridgeData WidowX setups. Status: maintained. Source: arXiv 2503.24278 — https://arxiv.org/abs/2503.24278

## Evaluation methodology (protocol, not benchmarks)

- **Robot Learning as an Empirical Science** — TRI position paper on policy-evaluation best practice: report experimental conditions, number of runs, and success criteria; use metrics complementary to binary success; do statistical analysis; describe failure modes qualitatively. Status: research (methodology). Source: arXiv 2409.09491 — https://arxiv.org/abs/2409.09491
- **Beyond Binary Success** — sample-efficient, statistically rigorous policy comparison via safe anytime-valid inference (sequential testing, early stopping at a pre-specified confidence); reports up to 70% less evaluation burden than batch methods, and shows fine-grained task-progress metrics separate policies faster than binary success. Status: research. Source: arXiv 2603.13616 — https://arxiv.org/abs/2603.13616
- **Test-time feedback (DoPr)** — names and measures the training/validation-loss vs task-success mismatch in rollout-deployed one-step-supervised policies, and shows downstream gains that do not accompany validation-loss improvements. Direct evidence that BC validation loss is not a checkpoint-selection signal. Status: research. Source: arXiv 2606.06418 — https://arxiv.org/abs/2606.06418
- **Per-Group Error, Not Total MSE** — VLA fine-tuning on an 11-DoF mobile manipulator where the *lowest-aggregate-MSE checkpoint was not the best on hardware*: collapsing heterogeneous joint groups (arm / gripper / head / base) into one loss lets easy joints mask failing ones. 60 real trials; per-group (arm) offline error predicted real ranking, total MSE did not. Practical checkpoint-selection fix: break validation loss out per action group. Status: research. Source: arXiv 2606.00253 — https://arxiv.org/abs/2606.00253
