# AI motion models
_Character-animation models that propose or drive motion: video-diffusion + pose-conditioned generation, AnimateDiff, image-to-animation DiTs. LICENSE-DECISIVE (research/academic-only weights are the trap; base-model license is inherited)._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

20 recipes · 2 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | ControlNet OpenPose / DWPose — pose-driven repaint pass | comfyui | walk, idle, attack, hurt, death — POSE REPAINT only; rigid props still require separate rig layer | ▸ reproduced | ⚠ cond | 5 | 4 | ✓ |
| 4 | Qwen-Image-Edit-2511 — painterly style repaint / face-preserve pass | python | style recovery, face-preserve repaint, idle/walk frame polish — all animation stages after proxy render | · single-run | ✅ yes | 4 | 4 | ✓ |
| 8 | Animate-X — universal character animation from driving video | python | walk, idle, hurt — humanoid AND non-humanoid character animation reference — NOT rigid props | · single-run | ✅ yes | 3 | 3 | ✓ |
| 8 | AnimateDiff motion module (SD1.5) — idle / ambient shimmer pass | comfyui | idle, ambient cloth/hair motion — NOT combat, NOT locomotion with weapons | · single-run | ⚠ cond | 5 | 2 | ✓ |
| 8 | AnimateDiff motion module (SDXL beta) — idle / ambient motion at higher resolution | comfyui | idle, ambient motion at 1024×1024 resolution — NOT combat, NOT locomotion | · single-run | ⚠ cond | 4 | 2 | ✓ |
| 8 | Champ — 3D parametric (SMPL) guided human animation | python | walk, idle, hurt — humanoid-only motion reference from SMPL body sequences | · single-run | ⚠ cond | 3 | 3 | ✓ |
| 8 | MimicMotion — confidence-aware pose-sequence video drive | python | walk, idle, hurt — humanoid soft-body motion reference from pose sequence — NOT rigid props | · single-run | ✅ yes | 4 | 3 | ✓ |
| 8 | Wan2.1 Image-to-Video — motion proposal source (non-rigid only) | python | idle, ambient motion, walk rough-pass — NOT rigid prop / weapon sequences | · single-run | ✅ yes | 3 | 2 | ✓ |
| 9 | Animate Anyone 2 — env affordance / object guider (Hu et al. 2025) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | Animate Anyone 2 — environment/object affordance | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | Animate-X++ — Pose Indicator anthropomorphic anim | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | Animate-X++ — Pose Indicator for game characters (Tan et al. 2025) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | CharacterShot — pose to multi-view to 4DGS (Gao et al. 2025) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | MVAnimate — multi-view pose optimization (Sun et al. 2026) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | MultiAnimate — multi-character identity-aware pose (Zhang et al. 2026) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | RealisDance-DiT HF — controllable char anim peer | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | RealisDance-DiT — Wan-2.1 DiT character animation | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | RealisDance-DiT — Wan-2.1 DiT character animation (Zhou et al. 2025) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | Spiritus — 2D layered char + mesh-skeleton + BVH/MDM (Sun et al. 2025) | comfy | all-motion | paper | check | 4 | 4 | · |
| 11 | UniAnimate — research/non-commercial only (AVOID for commercial game) | python | N/A — ruled out for commercial use | ▸ reproduced | ⛔ no | 0 | 0 | ✓ |

## Detail

### ControlNet OpenPose / DWPose — pose-driven repaint pass · `recommended` · ▸ reproduced
**OpenPose/DWPose ControlNet lets a frozen SD1.5 or SDXL checkpoint repaint a mesh-rendered frame at the correct pose; it adds painterly style recovery on top of rig truth without inventing motion.**
A skeleton/keypoint map extracted from a proxy render (or constructed manually) is fed through a ControlNet conditioning node in ComfyUI; the frozen text-to-image checkpoint then generates a stylized frame that matches the pose. DWPose (IDEA-Research, Apache 2.0) supersedes classic OpenPose within this workflow — it detects full body + hands + face (68 landmarks) giving higher-fidelity conditioning. The result is NOT a motion model — it is a frame-by-frame repaint layer on top of rig truth. Commercial fitness depends on the base checkpoint license: the ControlNet v1.1 SD1.5 openpose model card carries CreativeML OpenRAIL-M (commercial use permitted, behavioral restrictions apply); xinsir union SDXL ControlNet is Apache 2.0.
- **For the pipeline:** Use this as the REPAINT stage of the doctrine spine: mesh/proxy render supplies rigid prop truth, DWPose supplies the skeleton conditioning, a commercial-clean base checkpoint supplies style. Do not use it as a motion source — it cannot invent poses, only repaint them.
- **Engine:** comfyui · **Applies to:** walk, idle, attack, hurt, death — POSE REPAINT only; rigid props still require separate rig layer · **Kind:** technique
- **VRAM:** 8-14
- **Output license:** commercial **conditional** (license: Apache-2.0 (DWPose, xinsir union SDXL); CreativeML OpenRAIL-M (lllyasviel SD1.5 openpose v1.1)) — DWPose preprocessor is Apache 2.0. xinsir/controlnet-union-sdxl-1.0 is Apache 2.0. lllyasviel/control_v11p_sd15_openpose is CreativeML OpenRAIL-M — commercial use permitted; behavioral restrictions (no CSAM, no disinformation, no discriminatory use) must be enforced. All ControlNet outputs further inherit the BASE checkpoint license — only safe on a verified-commercial base.
- **Fit:** rig 5/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Cannot invent poses — only repaints a supplied pose |  |  |  |
| Rigid held props still drift across frames unless rig/mesh provides pixel-stable prop layer |  |  |  |
| Multi-frame temporal consistency is the caller's responsibility (not built in) |  |  |  |

- **Best for:** pose-driven-repaint (-, fit -) ; style-recovery (-, fit -) ; frame-by-frame-polish (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) (Lvmin Zhang, Anyi Rao, Maneesh Agrawala, 2023) — ControlNet architecture for conditioning a frozen T2I model on spatial maps (skeleton, depth, edge); Apache-2.0 code repo at lllyasviel/ControlNet. ; [Effective Whole-body Pose Estimation with Two-stages Distillation](https://arxiv.org/abs/2307.15880) (Zhendong Yang, Ailing Zeng, Chun Yuan, Yu Li, 2023) — DWPose whole-body estimator (body + hands + face); ICCV 2023 CV4Metaverse; repo IDEA-Research/DWPose under Apache 2.0; preferred over classic OpenPose in ControlNet workflows for fidelity. ; [xinsir/controlnet-union-sdxl-1.0 model card](https://huggingface.co/xinsir/controlnet-union-sdxl-1.0) (xinsir, 2024) — SDXL union ControlNet supporting 10+ conditioning modes including OpenPose simultaneously; license apache-2.0.

### Qwen-Image-Edit-2511 — painterly style repaint / face-preserve pass · `recommended` · · single-run
**Qwen-Image-Edit-2511 (Apache 2.0, Alibaba) is the studio's verified commercial-safe repaint path: instruction-driven image editing that recovers painterly style from a mesh-rendered or diffusion-rough frame while preserving character identity, including face.**
Qwen-Image-Edit-2511 (Qwen/Qwen-Image-Edit-2511 on HuggingFace, released December 2025, Apache 2.0) is a 20B diffusion-based image editor that takes an input image plus a natural-language instruction and outputs an edited image. Architecture routes the input through Qwen2.5-VL for semantic understanding and a VAE encoder for appearance preservation. The November 2025 revision specifically improved character consistency and mitigated image drift — directly relevant to the sprite repaint use case. It handles style transfer, element modification, and texture recovery. This is the polish/repaint ceiling of the doctrine spine, applied per-frame after rig/proxy render.
- **For the pipeline:** Apply per-frame after rig/mesh render: input is the proxy render, instruction is a style/repaint directive, output is the painterly sprite frame. The face-preserve improvement in the -2511 revision makes this the recommended path for character portrait and sprite head consistency. Does NOT drive motion — it repaints a supplied frame.
- **Engine:** python · **Applies to:** style recovery, face-preserve repaint, idle/walk frame polish — all animation stages after proxy render · **Kind:** model
- **VRAM:** 24+ (20B model; cloud GPU recommended)
- **Output license:** commercial **yes** (license: Apache 2.0) — Qwen/Qwen-Image-Edit-2511 HuggingFace model card declares Apache 2.0. Distinct model from Qwen2.5-VL-7B-Instruct (which is vision Q&A only, not image editing). No commercial restriction in the license; Alibaba official release.
- **Fit:** rig 4/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| 20B model — exceeds single RTX 5090 32GB for batched inference; cloud GPU needed for throughput |  |  |  |
| Does not drive motion — repaint only, not a pose or animation model |  |  |  |
| Instruction-following quality varies for highly technical style directives |  |  |  |

- **Best for:** style-recovery (-, fit -) ; face-preserve-repaint (-, fit -) ; painterly-polish (-, fit -) ; per-frame-finish (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, confirmed-with-fixes, unverified]]
- **Sources:** [Qwen/Qwen-Image-Edit-2511 model card](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) (Qwen Team, Alibaba Group, 2025) — Instruction-driven image editor (not vision-language Q&A); Apache 2.0; November 2025 revision with improved character consistency and reduced image drift; 20B model on diffusers QwenImageEditPipeline.

### Animate-X — universal character animation from driving video · `situational` · · single-run
**Animate-X (antgroup, Apache 2.0, ICLR 2025) animates any reference character image using a driving video with a Pose Indicator encoding motion implicitly and explicitly; broader character coverage than human-specific models but carries the same video-domain weapon-drift failure.**
Animate-X (arXiv:2410.10306, antgroup / Ant Group, accepted ICLR 2025) takes a reference character image and a driving video and generates an animation of the reference character following the driving motion. Its Pose Indicator captures both implicit motion cues (appearance flow) and explicit skeleton keypoints, enabling it to generalize to non-human/anthropomorphic characters beyond typical SMPL-based approaches. Default output: 32-frame videos at 768×512. Repository (antgroup/animate-x) is Apache 2.0 with no non-commercial restriction. The deprecated Lucaria-Academy fork should be ignored; the active canonical repo is antgroup/animate-x.
- **For the pipeline:** Useful for non-humanoid or stylized characters where SMPL-body models (Champ) break down. Same doctrine position as MimicMotion: motion-reference draft for non-rigid elements, not a delivery path for weapon frames. VRAM requirements not published in README — test on rig before committing to pipeline.
- **Engine:** python · **Applies to:** walk, idle, hurt — humanoid AND non-humanoid character animation reference — NOT rigid props · **Kind:** model
- **VRAM:** unknown
- **Output license:** commercial **yes** (license: Apache 2.0) — antgroup/animate-x README explicitly states 'released under the Apache-2.0 license as found in the LICENSE file'; no non-commercial restriction. Model weights on HuggingFace should be verified on the specific card before commercial deployment.
- **Fit:** rig 3/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| VRAM requirements not published — must benchmark on rig before committing |  |  |  |
| Rigid prop / weapon drift — same video-domain failure as all video generators |  |  |  |
| Deprecated Lucaria-Academy fork still indexed; use antgroup/animate-x only |  |  |  |

- **Best for:** motion-reference (-, fit -) ; driving-video-transfer (-, fit -) ; non-humanoid-character-animation (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Animate-X: Universal Character Image Animation with Enhanced Motion Representation](https://arxiv.org/abs/2410.10306) (Shuai Tan et al. (Ant Group), 2024) — Universal character animation via Pose Indicator (implicit + explicit motion); ICLR 2025; Apache 2.0; supports non-humanoid characters beyond SMPL body models. ; [antgroup/animate-x](https://github.com/antgroup/animate-x) (Ant Group, 2024) — Canonical Animate-X repo (not deprecated Lucaria-Academy fork); Apache-2.0 explicitly stated in README.

### AnimateDiff motion module (SD1.5) — idle / ambient shimmer pass · `situational` · · single-run
**AnimateDiff adds temporal motion to a frozen SD1.5 checkpoint via an Apache-2.0 motion module; commercial fitness is INHERITED from the base checkpoint, and frame-to-frame identity is too weak for crisp locomotion or weapon frames.**
A motion module that animates the latent space of an existing SD1.5 text-to-image model, generating short clips (8-16 frames typical) with temporal consistency. Best used for idle-shimmer passes — cloth ripple, hair sway, ambient breathing — where soft frame-to-frame drift is acceptable. Not suitable as a primary walk-cycle or combat-frame source because pixel-level identity across frames is insufficient. The repo README contains 'released for academic use' language but the governing license file is Apache 2.0, which permits commercial use; commercial fitness ultimately hinges on the base SD1.5 checkpoint.
- **For the pipeline:** Reserve for ambient idle/cloth shimmer on a commercial-clean SD1.5 base (e.g., SD1.5 base with CreativeML OpenRAIL++ or a fully Apache-licensed fine-tune). Keep all locomotion, attack, and weapon frames on the rig/mesh path.
- **Engine:** comfyui · **Applies to:** idle, ambient cloth/hair motion — NOT combat, NOT locomotion with weapons · **Base:** SD1.5 · **Kind:** model
- **VRAM:** 10-18
- **Output license:** commercial **conditional** (license: Apache-2.0 (motion module); base SD1.5 checkpoint license governs outputs) — AnimateDiff motion modules (guoyww/animatediff-motion-adapter-* on HuggingFace) declare apache-2.0 where a license is present; the GitHub repo LICENSE.txt is Apache 2.0. However, README contains 'released for academic use' framing — legally non-binding (Apache governs) but a flag for legal review. Generated animation inherits BASE checkpoint license; only commercially clean on a verified-commercial base checkpoint.
- **Fit:** rig 5/5 · studio 2/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Frame-to-frame pixel identity too weak for crisp locomotion frames |  |  |  |
| Weapon/prop drift: rigid prop warps unpredictably across frames |  |  |  |
| README 'academic use' language creates legal ambiguity despite Apache license file |  |  |  |

- **Best for:** idle-shimmer (-, fit -) ; ambient-motion (-, fit -) ; cloth-hair-animation (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [AnimateDiff: Animate Your Personalized Text-to-Image Diffusion Models without Specific Tuning](https://arxiv.org/abs/2307.04725) (Yuwei Guo, Ceyuan Yang, Anyi Rao, Zhengyang Liang, Yaohui Wang, Yu Qiao, Maneesh Agrawala, Dahua Lin, Bo Dai, 2024) — Motion module animating a frozen T2I model; GitHub repo guoyww/AnimateDiff is Apache 2.0; README notes 'academic use' framing (non-binding); motion module adapters published on HuggingFace. ; [guoyww/AnimateDiff](https://github.com/guoyww/AnimateDiff) (Yuwei Guo et al., 2024) — Canonical AnimateDiff repo; LICENSE.txt is Apache 2.0; SD1.5 primary target, SDXL via sdxl-beta branch.

### AnimateDiff motion module (SDXL beta) — idle / ambient motion at higher resolution · `situational` · · single-run
**The SDXL-beta motion adapter from AnimateDiff targets 1024×1024×16-frame generation; same conditional-commercial status as the SD1.5 module but requires ~13 GB VRAM and is less community-tested.**
The sdxl-beta branch and associated adapter (guoyww/animatediff-motion-adapter-sdxl-beta) apply the AnimateDiff approach to SDXL checkpoints for higher-resolution ambient motion. The HuggingFace model card for the SDXL adapter explicitly declares apache-2.0. Temporal consistency limitations from the SD1.5 version carry over — this is idle-shimmer and style-atmospheric only, not locomotion.
- **For the pipeline:** Prefer SD1.5 AnimateDiff for speed and community support; use SDXL beta only if your sprite resolution demands 1024+ and you have the VRAM headroom.
- **Engine:** comfyui · **Applies to:** idle, ambient motion at 1024×1024 resolution — NOT combat, NOT locomotion · **Base:** SDXL · **Kind:** model
- **VRAM:** 13-18
- **Builds on (stage 2):** AnimateDiff motion module (SD1.5) — idle / ambient shimmer pass
- **Output license:** commercial **conditional** (license: Apache-2.0 (adapter card); SDXL base checkpoint license governs outputs) — guoyww/animatediff-motion-adapter-sdxl-beta HuggingFace card declares apache-2.0. Output inherits SDXL base license (CreativeML OpenRAIL++ permits commercial use with behavioral restrictions). Same academic-use README disclaimer as SD1.5 — legally non-binding per Apache license file.
- **Fit:** rig 4/5 · studio 2/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Less community-tested than SD1.5 variant |  |  |  |
| Rigid prop drift — same as SD1.5 module |  |  |  |
| High VRAM floor limits accessibility |  |  |  |

- **Best for:** idle-shimmer (-, fit -) ; ambient-motion (-, fit -) ; high-resolution-atmospheric (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [guoyww/animatediff-motion-adapter-sdxl-beta model card](https://huggingface.co/guoyww/animatediff-motion-adapter-sdxl-beta) (Yuwei Guo et al., 2024) — SDXL motion adapter; license declared apache-2.0 on the HuggingFace model card; targets 1024x1024x16 frames.

### Champ — 3D parametric (SMPL) guided human animation · `situational` · · single-run
**Champ (Fudan, MIT license) drives human image animation from SMPL body model sequences providing depth/normal/semantic maps alongside skeleton for richer 3D-aware conditioning; MIT license permits commercial use but SMPL body model itself has its own academic license that must be verified separately.**
Champ (arXiv:2403.14781, Fudan University, ECCV 2024) uses SMPL parametric body sequences as the motion driver, generating depth maps, normal maps, and semantic segmentation maps alongside standard skeleton keypoints. This multi-layer 3D guidance produces more anatomically grounded animation than 2D-keypoint-only approaches. The repository (fudan-generative-vision/champ) is MIT licensed — the most permissive option in this lane. However, SMPL itself (the body model used to generate driving sequences) is distributed under a separate academic-use license by Max Planck Institute — that must be cleared independently for a commercial pipeline.
- **For the pipeline:** Best for humanoid walk/idle/hurt cycles where you can supply SMPL motion sequences from a motion capture library or rig. The 3D guidance reduces silhouette errors on limb crossings. Same doctrine position: motion-reference draft only — rigid props still require rig layer. Verify SMPL body model license separately before commercial deployment.
- **Engine:** python · **Applies to:** walk, idle, hurt — humanoid-only motion reference from SMPL body sequences · **Kind:** model
- **VRAM:** 12-16
- **Output license:** commercial **conditional** (license: MIT (repo code); SMPL body model has separate academic license) — fudan-generative-vision/champ repo is MIT — code and model weights under this license permit commercial use. However, SMPL body model (Max Planck Institute) is required to generate driving sequences and carries a separate academic-use-only license for its model weights. A commercial pipeline using Champ must independently license or avoid SMPL, or use pre-baked SMPL sequences without distributing SMPL weights.
- **Fit:** rig 3/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Requires SMPL body sequences as input — SMPL model itself has academic-only weights license |  |  |  |
| Humanoid-only: SMPL body model does not generalize to non-humanoid characters |  |  |  |
| Rigid prop / weapon drift — same video-domain failure |  |  |  |

- **Best for:** motion-reference (-, fit -) ; smpl-driven-animation (-, fit -) ; 3d-parametric-guidance (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Champ: Controllable and Consistent Human Image Animation with 3D Parametric Guidance](https://arxiv.org/abs/2403.14781) (Shenhao Zhu et al. (Fudan University), 2024) — SMPL-driven human animation with depth/normal/semantic multi-layer conditioning; ECCV 2024; repo fudan-generative-vision/champ under MIT license. ; [fudan-generative-vision/champ](https://github.com/fudan-generative-vision/champ) (Fudan University, 2024) — Canonical Champ repo; MIT license; SMPL motion driver — SMPL body model license must be verified separately for commercial use.

### MimicMotion — confidence-aware pose-sequence video drive · `situational` · · single-run
**MimicMotion (Tencent / SJTU, Apache 2.0) generates plausible human figure video from a reference image + pose keypoint sequence using confidence-aware weighting; it is a commercially safe motion-reference source for non-rigid body motion but shares the weapon-drift failure of all video-based generators.**
MimicMotion (arXiv:2406.19680, Tencent + Shanghai Jiao Tong University, 2024) takes a static reference character image and a sequence of pose keypoints (skeleton frames) as driving signal and generates a short video of that character performing the motion. The confidence-aware pose guidance weights keypoints by detection confidence, improving robustness on occluded or partial poses. Supports long-video extension via progressive latent fusion. The repo is Apache 2.0 with no non-commercial restriction in the license or README. VRAM: 8 GB minimum for 16-frame inference; 16 GB with on-GPU VAE decoder.
- **For the pipeline:** Use as a motion-reference stage: rig animator provides pose sequence, MimicMotion generates a reference video draft for soft-body elements (body sway, cloth, hair). Do NOT use for any frame containing a rigid held weapon — prop drift is severe. Strip to keyframes and pass through rig + ControlNet repaint before delivery.
- **Engine:** python · **Applies to:** walk, idle, hurt — humanoid soft-body motion reference from pose sequence — NOT rigid props · **Kind:** model
- **VRAM:** 8-16
- **Output license:** commercial **yes** (license: Apache 2.0) — GitHub repo Tencent/MimicMotion is Apache 2.0; no non-commercial restriction found in license or README. Model weights on HuggingFace should be verified on the specific weight card before commercial deployment — the code license is confirmed Apache 2.0.
- **Fit:** rig 4/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Rigid prop / weapon drift — no rigid-body understanding |  |  |  |
| Output is video, not sprite sheet — extraction step required |  |  |  |
| Model weight HuggingFace card should be independently verified before commercial use |  |  |  |

- **Best for:** motion-reference (-, fit -) ; pose-driven-video-draft (-, fit -) ; soft-body-motion (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [MimicMotion: High-Quality Human Motion Video Generation with Confidence-aware Pose Guidance](https://arxiv.org/abs/2406.19680) (Yuang Zhang et al. (Tencent, Shanghai Jiao Tong University), 2024) — Pose-sequence-driven human video generation with confidence-aware keypoint weighting and progressive latent fusion for long video; repo Tencent/MimicMotion Apache 2.0. ; [Tencent/MimicMotion](https://github.com/Tencent/MimicMotion) (Tencent, 2024) — Canonical MimicMotion repo; Apache License 2.0; VRAM: 8GB min (16-frame), 16GB with GPU VAE decoder.

### Wan2.1 Image-to-Video — motion proposal source (non-rigid only) · `situational` · · single-run
**Wan2.1 I2V (Apache 2.0, Alibaba) generates plausible human-figure motion from a still reference image and is commercially safe, but warps rigid props and held weapons — use only as a motion-proposal draft for non-rigid elements, never as a final combat or weapon-bearing frame source.**
Wan2.1 is an open-weight video generation model family (1.3B and 14B) from Alibaba, released under Apache 2.0 with users retaining rights to generated content. The 14B I2V variant takes a reference image plus text prompt and generates a short video clip, which can serve as a motion rough-pass for idle/ambient/walk cycles. However, the model has no understanding of rigid-body physics — held weapons and props translate and warp across frames, consistent with the studio's canon weapon-drift finding (also documented in arXiv:2605.14815 for video/orbit approaches). The 1.3B variant requires ~8.19 GB VRAM; 14B requires offloading on a single GPU.
- **For the pipeline:** Wan2.1 I2V is useful as a MOTION PROPOSAL for soft elements (cloth, hair, idle breathing, ambient sway) to be composited or used as reference for the rig animator. It must never be the final delivery path for combat frames or any frame containing a rigid held prop. Strip the video output back to keyframe references, then re-render through rig + ControlNet repaint.
- **Engine:** python · **Applies to:** idle, ambient motion, walk rough-pass — NOT rigid prop / weapon sequences · **Kind:** model
- **VRAM:** 8 (1.3B T2V); 24+ (14B I2V, offload required on single GPU)
- **Output license:** commercial **yes** (license: Apache 2.0) — Wan2.1 model card explicitly states Apache 2.0 and that users retain rights to generated content; no commercial exclusion. Alibaba / Wan-AI official release under Wan-Video GitHub org and Wan-AI HuggingFace org. Content-conduct restrictions (no illegal content, no targeted harm) apply but are not commercial prohibitions.
- **Fit:** rig 3/5 · studio 2/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Rigid held props warp and translate across frames — weapon drift is severe |  |  |  |
| 14B VRAM requirements exceed single-GPU capacity without offloading |  |  |  |
| Output is a video clip, not a sprite sheet — extraction and cleanup step required |  |  |  |
| No pose control input — motion is inferred from image + text, not skeleton-driven |  |  |  |

- **Best for:** motion-proposal (-, fit -) ; idle-reference (-, fit -) ; cloth-hair-rough-pass (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Wan: Open and Advanced Large-Scale Video Generative Models](https://arxiv.org/abs/2503.20314) (Team Wan (Alibaba Group / DAMO Academy), 2025) — Wan2.1 technical report; covers T2V (1.3B, 14B) and I2V (14B) variants; Apache 2.0 license; 1.3B T2V requires 8.19 GB VRAM. ; [Wan-Video/Wan2.1](https://github.com/Wan-Video/Wan2.1) (Wan-Video / Alibaba, 2025) — Official Wan2.1 repo under Apache 2.0; I2V 14B model in 480P and 720P variants; single-GPU offload required for 14B.

### Animate Anyone 2 — env affordance / object guider (Hu et al. 2025) · `situational` · paper
**Env affordance + object guider for held props — STUDY-058 deepen peer**
STUDY-058 Scholar deepen.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Animate Anyone 2](https://arxiv.org/abs/2502.06145) — Env affordance + object guider for held props.

### Animate Anyone 2 — environment/object affordance · `situational` · paper
**Pose-conditioned character animation adds environment affordance plus an object guider so held props and scene context stay coherent with the driven motion.**
Pose-conditioned character animation adds environment affordance plus an object guider so held props and scene context stay coherent with the driven motion.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Animate Anyone 2 — environment/object affordance](https://arxiv.org/abs/2502.06145) — Pose-conditioned character animation adds environment affordance plus an object guider so held props and scene context stay coherent with the driven motion.

### Animate-X++ — Pose Indicator anthropomorphic anim · `situational` · paper
**DiT Pose Indicator animates anthropomorphic/game characters without strict pose alignment; multi-task TI2V adds background dynamics.**
DiT Pose Indicator animates anthropomorphic/game characters without strict pose alignment; multi-task TI2V adds background dynamics.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Animate-X++ — Pose Indicator anthropomorphic anim](https://arxiv.org/abs/2508.09454) — DiT Pose Indicator animates anthropomorphic/game characters without strict pose alignment; multi-task TI2V adds background dynamics.

### Animate-X++ — Pose Indicator for game characters (Tan et al. 2025) · `situational` · paper
**Pose Indicator for game/anthropomorphic characters — STUDY-058 deepen peer**
STUDY-058 Scholar deepen.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Animate-X++](https://arxiv.org/abs/2508.09454) — Pose Indicator for game/anthropomorphic characters.

### CharacterShot — pose to multi-view to 4DGS (Gao et al. 2025) · `situational` · paper
**Pose → multi-view → 4DGS turnaround craft — STUDY-058 deepen**
STUDY-058 Scholar deepen.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [CharacterShot](https://arxiv.org/abs/2508.07409) — Pose → multi-view → 4DGS turnaround craft.

### MVAnimate — multi-view pose optimization (Sun et al. 2026) · `situational` · paper
**Multi-view pose opt; cut texture contamination — STUDY-058 deepen peer**
STUDY-058 Scholar deepen.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [MVAnimate](https://arxiv.org/abs/2602.08753) — Multi-view pose opt; cut texture contamination.

### MultiAnimate — multi-character identity-aware pose (Zhang et al. 2026) · `situational` · paper
**Multi-character identity-aware pose binding — STUDY-058 deepen**
STUDY-058 Scholar deepen.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [MultiAnimate](https://arxiv.org/abs/2607.13415) — Multi-character identity-aware pose binding.

### RealisDance-DiT HF — controllable char anim peer · `situational` · docs
**Controllable char anim; ref+SMPL/HaMeR; academic disclaimer — beyond STUDY-037 AnimateDiff**
STUDY-058 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [RealisDance-DiT HF](https://huggingface.co/theFoxofSky/RealisDance-DiT) — Controllable char anim; ref+SMPL/HaMeR; academic disclaimer.

### RealisDance-DiT — Wan-2.1 DiT character animation · `situational` · paper
**Wan-2.1 DiT baseline with minimal mods; strong on stylized characters, rare poses, and character-object interactions. License-check before shortlist.**
Wan-2.1 DiT baseline with minimal mods; strong on stylized characters, rare poses, and character-object interactions. License-check before shortlist.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [RealisDance-DiT — Wan-2.1 DiT character animation](https://arxiv.org/abs/2504.14977) — Wan-2.1 DiT baseline with minimal mods; strong on stylized characters, rare poses, and character-object interactions. License-check before shortlist.

### RealisDance-DiT — Wan-2.1 DiT character animation (Zhou et al. 2025) · `situational` · paper
**Wan-2.1 DiT; stylized / rare pose / object interaction — STUDY-058 deepen**
STUDY-058 Scholar deepen.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [RealisDance-DiT](https://arxiv.org/abs/2504.14977) — Wan-2.1 DiT; stylized / rare pose / object interaction.

### Spiritus — 2D layered char + mesh-skeleton + BVH/MDM (Sun et al. 2025) · `situational` · paper
**2D layered char + mesh-skeleton + BVH/MDM — STUDY-058 deepen peer**
STUDY-058 Scholar deepen.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Spiritus](https://arxiv.org/abs/2503.09127) — 2D layered char + mesh-skeleton + BVH/MDM.

### UniAnimate — research/non-commercial only (AVOID for commercial game) · `avoid` · ▸ reproduced
**UniAnimate (Alibaba ali-vilab) explicitly states RESEARCH/NON-COMMERCIAL USE ONLY in its README; it must be avoided for any commercial game pipeline.**
UniAnimate (arXiv:2406.01188, ali-vilab / Alibaba, 2024) generates human video from a reference portrait and DWPose skeleton guidance. Technically capable (32-frame, high-resolution output), but the README contains an explicit disclaimer: 'This open-source model is intended for RESEARCH/NON-COMMERCIAL USE ONLY.' No permissive open-source license file was found in the repo to supersede this. For a commercial game studio this is a hard block.
- **For the pipeline:** Do not use in the sprite pipeline. MimicMotion (Apache 2.0) or Animate-X (Apache 2.0) cover the same motion-reference use case without the non-commercial restriction.
- **Engine:** python · **Applies to:** N/A — ruled out for commercial use · **Kind:** model
- **VRAM:** 12-36
- **Output license:** commercial **no** (license: Non-commercial research only (per README disclaimer; no open-source license file found)) — README explicitly states 'RESEARCH/NON-COMMERCIAL USE ONLY'; no Apache/MIT/BSD license file found to supersede this. Alibaba ali-vilab org. Use MimicMotion or Animate-X instead.
- **Fit:** rig 0/5 · studio 0/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Explicitly non-commercial per README — hard block for commercial game |  |  |  |
| No open-source license file found to permit commercial use |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [UniAnimate: Taming Unified Video Diffusion Models for Consistent Human Image Animation](https://arxiv.org/abs/2406.01188) (Xiang Wang et al. (Alibaba, ali-vilab), 2024) — Unified video diffusion for human animation from portrait + DWPose skeleton; README explicitly restricts to research/non-commercial use only. ; [ali-vilab/UniAnimate](https://github.com/ali-vilab/UniAnimate) (Alibaba ali-vilab, 2024) — Canonical UniAnimate repo (not AlibabaResearch/UniAnimate which 404s); README states 'RESEARCH/NON-COMMERCIAL USE ONLY'; no permissive license file found.

