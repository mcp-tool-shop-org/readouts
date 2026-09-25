# Text-to-motion & motion synthesis
_Generative motion models (text->motion / motion synthesis): MDM, MoMask, MotionGPT, T2M-GPT, OmniControl — existence + license-decisive (many TRAIN on AMASS and inherit its non-commercial terms in the output)._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

10 recipes · 0 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 6 | MDM — Human Motion Diffusion Model (Tevet et al. 2022) | python | text-to-motion | ▸ reproduced | ⛔ no | 4 | 1 | ✓ |
| 6 | MLD — Motion Latent Diffusion (Chen et al. 2023) | python | text-to-motion | ▸ reproduced | ⛔ no | 4 | 1 | ✓ |
| 6 | MoMask — Generative Masked Modeling of 3D Human Motions (Guo et al. 2024) | python | text-to-motion | ▸ reproduced | ⛔ no | 4 | 2 | ✓ |
| 6 | MotionGPT — Human Motion as a Foreign Language (Jiang et al. 2023) | python | text-to-motion | ▸ reproduced | ⛔ no | 4 | 1 | ✓ |
| 6 | OmniControl — Spatial Joint Control for Motion Generation (Xie et al. 2023) | python | text-to-motion | ▸ reproduced | ⛔ no | 4 | 2 | ✓ |
| 6 | T2M-GPT — Text-to-Motion via VQ-VAE + GPT (Zhang et al. 2023) | python | text-to-motion | ▸ reproduced | ⛔ no | 4 | 1 | ✓ |
| 9 | CharacterShot — pose to multi-view to 4D | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | MVAnimate — multi-view pose optimization | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | MultiAnimate — multi-character identity-pose | comfy | all-motion | paper | check | 4 | 4 | · |
| 11 | FlowMDM — Seamless Human Motion Composition (Barquero et al. 2024) | python | text-to-motion | ▸ reproduced | ⛔ no | 3 | 1 | ✓ |

## Detail

### MDM — Human Motion Diffusion Model (Tevet et al. 2022) · `situational` · ▸ reproduced
**MDM generates human motion from text and its CODE is MIT, but it trains on HumanML3D (AMASS-derived) and the SMPL body model — both explicitly non-commercial — so generated clips are NOT clean for a commercial game.**
A classifier-free diffusion model producing SMPL joint-rotation motion from a text prompt (also action-to-motion and in-betweening). Outputs.npy joint positions and optional SMPL mesh.obj files per frame. Strong baseline for exploring motion ideas quickly; runs on modest VRAM. Foundational paper that most successors cite and extend.
- **For the pipeline:** Use ONLY as a blocking / prototyping tool to explore timing and motion arcs — never as a shipping motion source. The AMASS license explicitly prohibits training models for commercial use; any output clip inherits that restriction. No verified open clean-data text-to-motion model exists — a 'clean-data' candidate claimed this wave was fabricated and dropped (cross-family jury catch) — so the only clean paths are a commercial text-to-animation SaaS (verify its training-data licence) or retraining one of these architectures on permissively-licensed mocap.
- **Engine:** python · **Applies to:** text-to-motion · **Kind:** model
- **VRAM:** 6-12
- **Output license:** commercial **no** (license: MIT (code); trained on HumanML3D (AMASS-derived, non-commercial) + SMPL body model (research-only, Max Planck)) — The AMASS license (amass.is.tue.mpg.de/license.html) explicitly forbids use of the dataset 'to train methods/algorithms/neural networks/etc. for commercial use of any kind.' HumanML3D is built from AMASS + HumanAct12 and inherits this restriction. SMPL is likewise research-only (smpl.is.tue.mpg.de/modellicense.html). The MIT code license covers the Python scripts, NOT the weights or generated motion. All SMPL-parameterized outputs embed the body model's research-only constraint.
- **Fit:** rig 4/5 · studio 1/5
- **Best for:** research-reference (-, fit -) ; prototyping (-, fit -) ; motion-blocking (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [GuyTevet/motion-diffusion-model](https://github.com/GuyTevet/motion-diffusion-model) (Guy Tevet, Sigal Raab, Brian Gordon, Yonatan Shafir, Daniel Cohen-Or, Amit H. Bermano, 2022) — MIT-licensed code; trains on HumanML3D (AMASS-derived) and uses SMPL body model — both non-commercial. Confirmed from README and dependency list. ; [Human Motion Diffusion Model](https://arxiv.org/abs/2209.14916) (Guy Tevet et al., 2022) — Introduced transformer-based classifier-free diffusion for motion; benchmarked on HumanML3D and KIT datasets. ; [AMASS Dataset License — Max-Planck-Gesellschaft](https://amass.is.tue.mpg.de/license.html) (Max-Planck-Gesellschaft, 2019) — Prohibits use of dataset to train models for commercial use of any kind. Non-commercial research only.

### MLD — Motion Latent Diffusion (Chen et al. 2023) · `situational` · ▸ reproduced
**MLD (CVPR 2023) runs diffusion in a motion VAE latent space achieving 2 orders of magnitude speedup over raw-sequence diffusion, but trains on AMASS-derived HumanML3D + SMPL, making all outputs non-commercial.**
Learns a motion VAE to project sequences into a compact latent space, then runs a standard diffusion process there — dramatically faster at inference than sequence-space models. Outputs (nframe, 22, 3) joint positions plus optional SMPL meshes. Two repositories exist: ChenFengYe (canonical) and an independent AmballaAvinash fork. Both MIT licensed; both share the same AMASS training data problem.
- **For the pipeline:** The latent-space speedup makes MLD the most practical choice for high-volume prototyping: iterating over dozens of motion ideas in a session is feasible. The AMASS restriction remains unchanged — use for blocking reference only. The VAE architecture is also retraining-friendly if clean mocap data is acquired.
- **Engine:** python · **Applies to:** text-to-motion · **Kind:** model
- **VRAM:** 6-12
- **Output license:** commercial **no** (license: MIT (code); trained on HumanML3D (AMASS-derived, non-commercial) + SMPL (research-only)) — AMASS distribution policy prevents the MLD authors from even redistributing the raw data; their README links to the AMASS site for access. Training on AMASS-derived HumanML3D means weights are produced by a prohibited-commercial-use training run. SMPL dependency adds second non-commercial layer. MIT code license does not cure either issue.
- **Fit:** rig 4/5 · studio 1/5
- **Best for:** prototyping (-, fit -) ; blocking (-, fit -) ; fast-iteration (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [ChenFengYe/motion-latent-diffusion](https://github.com/ChenFengYe/motion-latent-diffusion) (Xin Chen, Biao Jiang, Wen Liu, Zilong Huang, Bin Fu, Tao Chen, Gang Yu, 2023) — MIT-licensed code. Trains on HumanML3D (AMASS-derived). AMASS distribution policy noted in README — authors cannot redistribute data. Uses SMPL for mesh rendering. ; [Executing your Commands via Motion Diffusion in Latent Space](https://arxiv.org/abs/2212.04048) (Xin Chen et al., 2023) — CVPR 2023 paper; introduces VAE latent space for motion diffusion, achieving 100× speedup vs. sequence-space diffusion models.

### MoMask — Generative Masked Modeling of 3D Human Motions (Guo et al. 2024) · `situational` · ▸ reproduced
**MoMask (CVPR 2024) achieves high-fidelity motion generation via hierarchical masked token modeling and even exports BVH for retargeting, but it is trained on HumanML3D (AMASS-derived) and depends on SMPL/SMPL-X — so BVH outputs still inherit non-commercial training restrictions.**
Hierarchical generative masked modeling framework representing motion as multi-layer discrete tokens. Produces (nframe, 22, 3) numpy arrays and BVH files at 20 FPS. The BVH export is pipeline-convenient for Blender/Spine retargeting, but the underlying data provenance blocks commercial shipping. State-of-the-art quality among academic text-to-motion models as of mid-2024.
- **For the pipeline:** The BVH export is the most retargeting-friendly output in this model family — worth running in the blocking phase to generate motion reference you then clean/recreate. Do not use BVH outputs directly in the shipped game; they are contaminated by HumanML3D licensing. The retarget pass must be authored from scratch using the BVH only as timing reference.
- **Engine:** python · **Applies to:** text-to-motion · **Kind:** model
- **VRAM:** 8-16
- **Output license:** commercial **no** (license: MIT (code); trained on HumanML3D (AMASS-derived, non-commercial) + SMPL/SMPL-X body model (research-only)) — HumanML3D is derived from AMASS, which prohibits training models for commercial use. SMPL-X (Max Planck) is likewise research-only for free tier. Even though MoMask exports BVH — a retargetable format — the clip content was generated by a model trained on restricted data, meaning legal use in a commercial title requires a clean-data re-animation pass, NOT a direct BVH import.
- **Fit:** rig 4/5 · studio 2/5
- **Best for:** motion-reference (-, fit -) ; prototyping (-, fit -) ; blocking (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [EricGuo5513/momask-codes](https://github.com/EricGuo5513/momask-codes) (Chuan Guo, Yuxuan Mu, Muhammad Gohar Javed, Sen Wang, Li Cheng, 2024) — MIT-licensed code; trains on HumanML3D and KIT-ML; uses SMPL and SMPL-X; outputs numpy arrays and BVH files at 20 FPS. Confirmed from repository README. ; [MoMask: Generative Masked Modeling of 3D Human Motions](https://arxiv.org/abs/2312.00063) (Chuan Guo et al., 2024) — CVPR 2024 paper introducing hierarchical residual quantization approach for text-driven 3D human motion generation.

### MotionGPT — Human Motion as a Foreign Language (Jiang et al. 2023) · `situational` · ▸ reproduced
**MotionGPT (NeurIPS 2023) treats motion tokens as a second language within an LLM, enabling unified motion understanding and generation; code is MIT but SMPL + HumanML3D (AMASS-derived) training makes all outputs non-commercial.**
Tokenizes motion clips via a motion VQ-VAE, then fine-tunes a language model (T5-based) to generate motion tokens from text alongside natural language tasks (motion QA, captioning, prediction). Outputs.npy (nframe, 22, 3) and optional PLY meshes for Blender. The multi-task framing makes it the most versatile in this family for R&D purposes. A MotionGPT3 (2026) successor exists on the same repo org with the same training data constraints.
- **For the pipeline:** The LLM framing is useful for generating annotated motion descriptions alongside the clip — helpful for labeling a reference library during preproduction. Do not import the generated clips into the shipped title. MotionGPT3 (MIT, arXiv:2506.24086) is architecturally improved but trains on the same HumanML3D data — no change in commercial status.
- **Engine:** python · **Applies to:** text-to-motion · **Kind:** model
- **VRAM:** 12-24
- **Output license:** commercial **no** (license: MIT (code); trained on HumanML3D (AMASS-derived, non-commercial) + SMPL (research-only)) — MotionGPT README explicitly notes dependency on SMPL, SMPL-X, and PyTorch3D with their own licenses. HumanML3D is the training dataset — AMASS-derived, non-commercial. MIT code license covers training scripts and model architecture. The instruction data prepared from HumanML3D also inherits AMASS restrictions. MotionGPT3 (2026) is the same situation — MIT code, HumanML3D data, no commercial clearance.
- **Fit:** rig 4/5 · studio 1/5
- **Best for:** research-reference (-, fit -) ; prototyping (-, fit -) ; motion-captioning (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [OpenMotionLab/MotionGPT](https://github.com/OpenMotionLab/MotionGPT) (Biao Jiang, Xin Chen, Wen Liu, Jingyi Yu, Gang Yu, Tao Chen, 2023) — MIT-licensed code; NeurIPS 2023; trains on HumanML3D (AMASS-derived); uses SMPL skeleton (22 joints); README explicitly notes SMPL, SMPL-X, PyTorch3D dependencies with separate licenses. ; [OpenMotionLab/MotionGPT3](https://github.com/OpenMotionLab/MotionGPT3) (OpenMotionLab, 2026) — MIT-licensed successor (2026); bimodal motion-language VAE architecture; still trains on HumanML3D — same AMASS inheritance trap applies.

### OmniControl — Spatial Joint Control for Motion Generation (Xie et al. 2023) · `situational` · ▸ reproduced
**OmniControl (ICLR 2024) adds precise spatial joint control signals (pelvis position, hand placement, foot contact) on top of text conditioning and MDM architecture; MIT code but trained on HumanML3D (AMASS-derived) — non-commercial.**
Extends MDM with ControlNet-style spatial conditioning so you can anchor specific joints to 3D positions at specific frames while generating the rest of the motion from text. Output format mirrors MDM:.npy joint XYZ + optional SMPL meshes at (nframe, 22, 3). The spatial control capability is highly relevant for compositing sprites with scene geometry, but the licensing barrier is identical to the rest of this family.
- **For the pipeline:** OmniControl's joint-pinning capability (anchor the feet at specific world positions, control the spine trajectory) is the most scene-aware motion control in this family — directly useful for prototyping characters that must interact with terrain or props. For the commercial game, use it to generate reference poses for keyframe/Spine animators to recreate, not to import directly.
- **Engine:** python · **Applies to:** text-to-motion · **Kind:** model
- **VRAM:** 12-24
- **Output license:** commercial **no** (license: MIT (code); trained on HumanML3D (AMASS-derived, non-commercial) + SMPL (research-only)) — OmniControl's README notes code depends on CLIP, SMPL, SMPL-X, and PyTorch3D with their own licenses. Training dataset is HumanML3D (built on AMASS + HumanAct12). AMASS license prohibits commercial model training. MIT covers the Python control mechanism; the weights and outputs inherit AMASS restriction. KIT-ML support listed as TODO — would add a second non-commercial dataset.
- **Fit:** rig 4/5 · studio 2/5
- **Best for:** prototyping (-, fit -) ; scene-aware-motion (-, fit -) ; pose-reference (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [neu-vi/OmniControl](https://github.com/neu-vi/OmniControl) (Yiming Xie, Varun Jampani, Lei Zhong, Deqing Sun, Huaizu Jiang, 2023) — MIT-licensed code; ICLR 2024; trains on HumanML3D; uses SMPL body model; outputs.npy joint XYZ and SMPL mesh.obj files. ; [OmniControl: Control Any Joint at Any Time for Human Motion Generation](https://arxiv.org/abs/2310.08580) (Yiming Xie et al., 2023) — ICLR 2024 paper introducing spatial joint control signals (position anchors) layered on top of diffusion-based text-to-motion generation.

### T2M-GPT — Text-to-Motion via VQ-VAE + GPT (Zhang et al. 2023) · `situational` · ▸ reproduced
**T2M-GPT (CVPR 2023) uses a CNN-based VQ-VAE and autoregressive GPT to generate human motion from text; code is Apache-2.0 but training on HumanML3D (AMASS-derived) and SMPL mesh rendering means generated motion clips are non-commercial.**
Treats text-to-motion as a discrete token prediction problem: VQ-VAE encodes motion into tokens, GPT autoregressively predicts them conditioned on text. Outputs.npy files and optional SMPL mesh sequences. Extremely clean codebase, well-documented, competitive benchmark numbers at CVPR 2023. The Apache-2.0 code license is more permissive than MIT but changes nothing about the training data restriction.
- **For the pipeline:** The two-stage VQ-VAE + GPT architecture is easy to retrain — if you can acquire a permissively-licensed mocap dataset, T2M-GPT is among the better-structured repos to adapt for a clean-data fine-tune. Until that dataset exists, treat identically to MDM: prototyping only.
- **Engine:** python · **Applies to:** text-to-motion · **Kind:** model
- **VRAM:** 6-12
- **Output license:** commercial **no** (license: Apache-2.0 (code); trained on HumanML3D (AMASS-derived, non-commercial) + SMPL (research-only)) — Apache-2.0 code license is permissive and covers the Python scripts and VQ-VAE/GPT architecture. It does not cover the pre-trained weights, which were produced by training on AMASS-derived HumanML3D data. AMASS license prohibits model training for commercial use; weights and outputs inherit this restriction. SMPL mesh rendering adds a second non-commercial dependency.
- **Fit:** rig 4/5 · studio 1/5
- **Best for:** prototyping (-, fit -) ; architecture-reference (-, fit -) ; clean-retrain-candidate (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Mael-zys/T2M-GPT](https://github.com/Mael-zys/T2M-GPT) (Jianrong Zhang, Yangsong Zhang, Xiaodong Cun, Shaoli Huang, Yong Zhang, Hongbo Fu, Yujun Shen, Ying Shan, 2023) — Apache-2.0 licensed code; trains on HumanML3D and KIT-ML datasets; uses SMPL mesh rendering. Confirmed from GitHub repository. ; [T2M-GPT: Generating Human Motion from Textual Descriptions with Discrete Representations](https://arxiv.org/abs/2301.06052) (Jianrong Zhang et al., 2023) — CVPR 2023 paper; VQ-VAE tokenizes motion, GPT autoregressively generates token sequences from text descriptions.

### CharacterShot — pose to multi-view to 4D · `situational` · paper
**Single character image + 2D pose to multi-view video to neighbor-constrained 4DGS; turnaround/spatial-view consistency.**
Single character image + 2D pose to multi-view video to neighbor-constrained 4DGS; turnaround/spatial-view consistency.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [CharacterShot — pose to multi-view to 4D](https://arxiv.org/abs/2508.07409) — Single character image + 2D pose to multi-view video to neighbor-constrained 4DGS; turnaround/spatial-view consistency.

### MVAnimate — multi-view pose optimization · `situational` · paper
**Hybrid 2D+3D pose guidance with multi-view attention and MV-Opt loss to cut texture contamination and complex-gesture failure.**
Hybrid 2D+3D pose guidance with multi-view attention and MV-Opt loss to cut texture contamination and complex-gesture failure.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [MVAnimate — multi-view pose optimization](https://arxiv.org/abs/2602.08753) — Hybrid 2D+3D pose guidance with multi-view attention and MV-Opt loss to cut texture contamination and complex-gesture failure.

### MultiAnimate — multi-character identity-pose · `situational` · paper
**Identity-specific ReferenceNet + identity-aware pose encoder so multiple characters keep identity-pose binding.**
Identity-specific ReferenceNet + identity-aware pose encoder so multiple characters keep identity-pose binding.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [MultiAnimate — multi-character identity-pose](https://arxiv.org/abs/2607.13415) — Identity-specific ReferenceNet + identity-aware pose encoder so multiple characters keep identity-pose binding.

### FlowMDM — Seamless Human Motion Composition (Barquero et al. 2024) · `avoid` · ▸ reproduced
**FlowMDM (CVPR 2024) generates long continuous motion sequences composed from multiple sequential text prompts using Blended Positional Encodings; however its code LICENSE is explicitly non-commercial academic-only, and it trains on BABEL and HumanML3D (AMASS-derived).**
Addresses compositional long-sequence generation: given a list of ordered text prompts, produce a single seamless motion clip that transitions coherently between them. Uses Blended Positional Encodings alternating absolute (global coherence) and relative (smooth transitions) phases. Particularly relevant for complex multi-action character sequences like run→attack→recover. The LICENSE file is a custom Universitat de Barcelona academic license, stricter than CC BY-NC.
- **For the pipeline:** The multi-prompt composition is the most useful prototyping tool in this set for sequencing full combat or traversal animations. However FlowMDM has a double non-commercial lock: the code itself is academic-only licensed (not MIT/Apache), AND the training data (BABEL + HumanML3D from AMASS) is non-commercial. Do not even host or distribute this internally without academic affiliation. Useful only as ideation reference.
- **Engine:** python · **Applies to:** text-to-motion · **Kind:** model
- **VRAM:** 12-24
- **Output license:** commercial **no** (license: Custom academic non-commercial (Universitat de Barcelona); trained on HumanML3D (AMASS-derived, non-commercial) + BABEL dataset) — FlowMDM's LICENSE file explicitly restricts use to 'noncommercial research purposes' by academic institutions or non-profit organizations. Commercial use requires written permission from Universitat de Barcelona. On top of the code restriction, training data includes HumanML3D (AMASS-derived, prohibited for commercial model training) and BABEL (also AMASS-based). This is the most restrictively licensed model in this lane — both code and data layers are blocked for commercial use.
- **Fit:** rig 3/5 · studio 1/5
- **Best for:** ideation-only (-, fit -) ; compositional-reference (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [BarqueroGerman/FlowMDM](https://github.com/BarqueroGerman/FlowMDM) (German Barquero, Sergio Escalera, Cristina Palmero, 2024) — Custom academic-only license (not MIT/Apache) — explicitly non-commercial, derivatives become property of Universitat de Barcelona. Trains on BABEL and HumanML3D (AMASS-derived). CVPR 2024. ; [Seamless Human Motion Composition with Blended Positional Encodings](https://arxiv.org/abs/2402.15509) (German Barquero et al., 2024) — CVPR 2024 paper; introduces Blended Positional Encodings for seamless multi-prompt long-motion composition.

