# Robot Learning Landscape — verified snapshot

**Verified: 2026-08-05.** Entries were confirmed against live sources on this date — re-verify anything before relying on it if this snapshot is more than ~6 months old.

Entry format: **Name** — one-line what-it-is. Status: maintained / research / commercial. Source: `<url>`

---

## Imitation-learning toolkits & dataset standards

- **LeRobot** — Hugging Face's end-to-end robot learning library; `LeRobotDataset` v3.0 stores synced video (MP4) + state/action as Parquet, streamable from the HF Hub without full download. Ships trainable implementations of ACT, Diffusion Policy, pi0, SmolVLA behind one CLI. Status: maintained. Source: https://huggingface.co/docs/lerobot/lerobot-dataset-v3 (also https://github.com/huggingface/lerobot)
- **Open X-Embodiment / RT-X** — cross-embodiment dataset standard assembled from 22 robots across 21 institutions (527 skills, 160k+ tasks); the RT-X models trained on it show positive transfer across robots. Status: research (dataset actively used as a pretraining source). Source: arXiv 2310.08864 — https://arxiv.org/abs/2310.08864
- **AgiBot World** — Shanghai-based AgiBot's dataset: 1M+ trajectories across 217 tasks in 5 deployment scenarios, extensible to dexterous hands and visuo-tactile sensors; underlies the GO-1 policy. Status: maintained (open-sourced). Source: arXiv 2503.06669 — https://arxiv.org/abs/2503.06669

## Policy architectures (arXiv IDs)

- **ACT (Action Chunking with Transformers)** — generative model over action-chunk sequences for low-cost bimanual manipulation; basis of the ALOHA stack. Status: maintained (widely reused). Source: arXiv 2304.13705 — https://arxiv.org/abs/2304.13705
- **Diffusion Policy** — represents visuomotor policies as a conditional denoising-diffusion process over action sequences; handles multimodal action distributions well. Status: maintained. Source: arXiv 2303.04137 — https://arxiv.org/abs/2303.04137
- **π₀ (pi0)** — flow-matching VLA architecture from Physical Intelligence built on a pretrained VLM backbone, trained across single-arm, dual-arm, and mobile-manipulator platforms. Status: maintained/commercial. Source: arXiv 2410.24164 — https://arxiv.org/abs/2410.24164
- **SmolVLA** — ~450M-parameter compact VLA (compact VLM + flow-matching action expert) trained on 481 community LeRobot datasets; trains on one GPU, runs on consumer GPU/CPU. Status: maintained. Source: arXiv 2506.01844 — https://arxiv.org/abs/2506.01844

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
