# Inbetweening & interpolation
_Keyframe -> tween frame generation: FILM, RIFE/Practical-RIFE, optical-flow interpolation; multiply sparse keyposes into a smooth cycle; large-displacement vs smooth-motion tradeoffs._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

14 recipes · 5 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | ComfyUI-Frame-Interpolation (Fannovel16) — production integration node | comfyui | walk-cycle, attack-swing, any-sprite-animation, comfyui-pipeline | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 2 | FILM: Frame Interpolation for Large Motion (Google, ECCV 2022) | python | attack-swing, dodge-burst, sparse-2-key-poses, large-displacement | ▸ reproduced | ✅ yes | 4 | 5 | ✓ |
| 4 | Large-displacement vs smooth-displacement: FILM vs RIFE decision principle | n/a | attack-swing, walk-cycle, any-sprite-animation | · single-run | ✅ yes | 5 | 5 | ✓ |
| 4 | Thin-limb and contact-pose artifact cleanup (post-interpolation) | n/a | attack-swing, walk-cycle, any-thin-limb-sprite | · single-run | ✅ yes | 5 | 5 | · |
| 6 | 4-6 Keypose → Inbetween → Palette Cleanup workflow | comfyui | walk-cycle, attack-swing, any-sprite-animation | · community | ✅ yes | 5 | 5 | · |
| 6 | Practical-RIFE v4.x (hzwer / Megvii, ECCV 2022) — smooth low-displacement motion | python | walk-cycle, idle-breathe, low-displacement-smooth, dense-keyframe-fill | ▸ reproduced | ⚠ cond | 5 | 4 | ✓ |
| 8 | EMA-VFI: Extracting Motion and Appearance via Inter-Frame Attention (CVPR 2023) | python | walk-cycle, attack-swing, texture-rich-sprites, high-fidelity | · single-run | ⚠ cond | 4 | 3 | ✓ |
| 9 | AnimateDiff SparseCtrl keyframe interpolation docs | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | Awesome-2D-Animation inventory peer (STUDY-058) | docs | all-motion | docs | check | 4 | 4 | · |
| 9 | FILM large-motion frame interpolation (Reda et al. 2022) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | FILM large-motion interpolation analog (hold-with-limit) | docs | all-motion | analog | check | 4 | 4 | · |
| 9 | Pose-to-pose / keys-vs-extremes hold-with-limit | docs | all-motion | docs | check | 4 | 4 | · |
| 9 | RIFE real-time intermediate flow interpolation (Huang et al. 2020) | comfy | all-motion | paper | check | 4 | 4 | · |
| 11 | GIMM-VFI: Generalizable Implicit Motion Modeling (NeurIPS 2024) — non-commercial reference only | python | research-reference | ▸ reproduced | ⛔ no | 3 | 0 | ✓ |

## Detail

### ComfyUI-Frame-Interpolation (Fannovel16) — production integration node · `recommended` · ▸ reproduced
**ComfyUI-Frame-Interpolation (MIT node package) is the canonical ComfyUI integration point for RIFE, FILM, EMA-VFI, IFRNet, and a dozen other VFI models, giving the studio a single workflow node to swap between interpolators without leaving ComfyUI.**
The Fannovel16 custom node set exposes RIFE (v4.0–v4.26), FILM, EMA-VFI, IFRNet, AMT, FLAVR, and others as first-class ComfyUI nodes under category 'ComfyUI-Frame-Interpolation/VFI'. Each node accepts an IMAGE batch (minimum 2 frames) and a multiplier; scheduling multipliers allow non-uniform frame pacing. The node package itself is MIT-licensed. Each underlying VFI model retains its own weight license (see per-model recipes). Recommended companion nodes: LoadImagesFromDirectory (VideoHelperSuite) for batch ingestion, and VideoHelperSuite's VHS_VideoCombine for sprite-sheet export.
- **For the pipeline:** Wire sprite keyposes as IMAGE → RIFE-VFI (multiplier=4) → palette-cleanup → SpriteSheetExport. Swap RIFE for FILM node when working on attack animations. This single node set covers all inbetweening needs inside ComfyUI without Python script exits. The multiplier=4 setting (4x frame count = 3 new frames between each pair) is a practical default for 12-fps game animation source going to 48-fps intermediate.
- **Engine:** comfyui · **Applies to:** walk-cycle, attack-swing, any-sprite-animation, comfyui-pipeline · **Kind:** technique
- **VRAM:** 4-12
- **Measured receipt (tensor-engine):** `comfyui-frame-interpolation-node` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **conditional** (license: MIT (node package); each model's own license applies to its weights) — The node wrapper is MIT. Commercial use of the interpolated output depends on the underlying model weight license (FILM = yes Apache-2.0; RIFE = conditional MIT-Megvii; EMA-VFI = conditional Apache-2.0). Do not mix in GIMM-VFI via this node for shipping frames.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| multiplier |  | ○ |  |
| model |  | ○ |  |

- **Best for:** inbetween (-, fit -) ; pipeline-integration (-, fit -) ; comfyui (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Fannovel16/ComfyUI-Frame-Interpolation](https://github.com/Fannovel16/ComfyUI-Frame-Interpolation) (Fannovel16, 2023) — MIT-licensed ComfyUI node set supporting RIFE v4.0–v4.26, FILM, EMA-VFI, IFRNet, AMT, FLAVR, STMFNet, and others; accepts IMAGE batch with scheduling multiplier values.

### FILM: Frame Interpolation for Large Motion (Google, ECCV 2022) · `recommended` · ▸ reproduced
**FILM is the safest-licensed inbetweener for a commercial studio: Apache-2.0 covers both code and pretrained weights, and its scale-agnostic multi-scale estimator outperforms flow-only methods on large-displacement (fast attack slash, jump) keyframe pairs.**
FILM (Frame Interpolation for Large Motion) uses a single unified network with a multi-scale feature extractor that shares weights across scales, building a scale-agnostic bidirectional motion estimator. The key insight is that large motion at fine scales resembles small motion at coarse scales, giving the model generalisation over fast-moving sprites without separate optical-flow or depth networks. It optimises with a Gram matrix loss for perceptually crisp synthesis. Benchmark winner on Xiph large-motion dataset (ECCV 2022). Entire release — code and TF2 SavedModels — is Apache-2.0.
- **For the pipeline:** Use FILM as the default inbetweener for attack animations, jump arcs, and any motion where key poses are far apart (>40 px displacement at sprite scale). Accept 5-15 fps throughput on the RTX 5090 (vs RIFE's 50-100 fps) — the license safety and large-motion quality justify the batch cost for final-delivery frames. For walk cycles and idle breathing, switch to RIFE.
- **Engine:** python · **Applies to:** attack-swing, dodge-burst, sparse-2-key-poses, large-displacement · **Kind:** model
- **VRAM:** 8-12
- **Output license:** commercial **yes** (license: Apache-2.0 (code + pretrained TF2 SavedModels)) — Apache-2.0 covers both the repository source and the released pretrained models on Google Drive. No separate weight license. This is the decisive commercial advantage over RIFE, whose Megvii-copyrighted weights carry an MIT notice that is cleaner but originates from a corporate research lab — FILM's Google Apache-2.0 release is the benchmark for unambiguous permissive coverage.
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| num_recursions |  | ○ |  |
| model_variant |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Softness in synthesised midframes for very fast contact poses — requires manual cleanup or a sharpening pass. |  |  |  |
| Does not understand sprite palette constraints; interpolated pixels will introduce sub-palette colours that need quantisation post-process. |  |  |  |
| Slower than RIFE by ~7x; unsuitable for interactive preview iteration loops. |  |  |  |

- **Best for:** inbetween (-, fit -) ; large-displacement (-, fit -) ; sparse-keyframe-fill (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [FILM: Frame Interpolation for Large Motion](https://arxiv.org/abs/2202.04901) (Fitsum Reda, Janne Kontkanen, Eric Tabellion, Deqing Sun, Caroline Pantofaru, Brian Curless, 2022) — Scale-agnostic multi-scale feature extractor achieves SOTA on Xiph large-motion benchmark; full release under Apache-2.0. ; [google-research/frame-interpolation](https://github.com/google-research/frame-interpolation) (Google Research, 2022) — Repository LICENSE file is Apache-2.0; pretrained TF2 SavedModels (L1/Style/VGG variants) distributed from Google Drive under the same license.

### Large-displacement vs smooth-displacement: FILM vs RIFE decision principle · `recommended` · · single-run
**The single most load-bearing decision in VFI for sprites is displacement magnitude: use FILM for fast attacks (large displacement, sparse 2-key), use RIFE for walk/idle (small displacement, dense smooth motion).**
FILM's scale-agnostic multi-scale estimator was designed for large camera/object motion — it generalises from coarse-scale small motion to fine-scale large motion via weight sharing. RIFE's IFNet is optimised for speed on well-conditioned dense optical flow and breaks down on large displacements (>40 px at sprite resolution) with stretching and ghosting. Empirical community benchmarks confirm RIFE processes 50-100 fps vs FILM's 5-15 fps at 1080p on RTX 4090-class hardware, so the throughput tradeoff is real. For sprite resolution (256-512 px tall), large-displacement is anything where a limb sweeps >25% of sprite height between keyposes.
- **For the pipeline:** Decision gate at the inbetween step: measure inter-keypose displacement. If max limb motion > ~25% sprite height → FILM. If < 25% → RIFE. For attack animations authoring 2 keyposes (windup + contact), always prefer FILM. For walk cycles with 4 keyposes, try RIFE first and switch to FILM only if ghosting appears at foot-contact frames.
- **Engine:** n/a · **Applies to:** attack-swing, walk-cycle, any-sprite-animation · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Decision principle has no license; applies to any VFI tool selected.
- **Fit:** rig 5/5 · studio 5/5
- **Best for:** principle (-, fit -) ; model-selection (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, confirmed-with-fixes, unverified]]
- **Sources:** [RIFE vs FILM Frame Interpolation Comparison Guide 2025](https://apatero.com/blog/rife-vs-film-video-frame-interpolation-comparison-2025) (Apatero Blog, 2025) — FILM processes 5-15 fps vs RIFE 50-100 fps on RTX 4090 at 1080p; FILM superior for large motion, RIFE for smooth dense motion — confirmed with direct comparison. ; [FILM: Frame Interpolation for Large Motion](https://arxiv.org/abs/2202.04901) (Fitsum Reda et al. (Google), 2022) — Scale-agnostic multi-scale weight sharing explicitly designed to handle large motion that defeats flow-only methods.

### Thin-limb and contact-pose artifact cleanup (post-interpolation) · `recommended` · · single-run
**All current VFI methods produce characteristic artifacts on 2D sprite thin limbs (sword edges, fingers, hair) and fast contact poses — a mandatory cleanup stage is required before shipping interpolated frames.**
Neural VFI fails in predictable ways on sprite-specific content: thin limbs (1-3 px wide) are blurred or ghosted because optical flow treats them as texture edges without semantic awareness; fast contact poses (foot strike, weapon impact) involve occlusion and appearance/disappearance of regions that confuse flow estimators. A 2021/ECCV2022 paper (Chen & Zwicker) specifically addresses aberrations in solid-colour regions of 2D animation, proposing a Distance Transform Module for correction. In practice the studio cleanup pass is: (1) flag frames with high-frequency content loss using a sharpness metric or manual review, (2) replace worst offenders with hand-redrawn keyposes, (3) apply palette quantisation to all interpolated frames to remove sub-palette anti-alias colours, (4) use a sharpening pass (unsharp mask or neural upscaler on the thin-limb region) as needed.
- **For the pipeline:** Budget cleanup time proportional to animation complexity: fast attack with 2 keyposes → expect 30-50% of interpolated frames to need review; smooth walk with 4 keyposes → expect 10-20%. The cleanup is NOT optional for shipping — sub-palette colours and blurred thin limbs are visually conspicuous at sprite scale. The Distance Transform Module approach (Chen & Zwicker 2022) is a research pointer, not a packaged tool; treat it as inspiration for a custom cleanup step.
- **Engine:** n/a · **Applies to:** attack-swing, walk-cycle, any-thin-limb-sprite · **Kind:** post-process
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Cleanup technique has no license constraints.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Skipping cleanup and shipping interpolated frames directly — blurred thin limbs and sub-palette pixels are visually conspicuous. |  |  |  |
| Applying palette quantisation BEFORE interpolation — reduces the colour information the VFI model uses and worsens quality. |  |  |  |

- **Best for:** post-process (-, fit -) ; artifact-cleanup (-, fit -) ; quality-gate (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=unverified] -> unverified [only 1 of 3 juror(s) confirmed [confirmed, unverified]]
- **Sources:** [Improving the Perceptual Quality of 2D Animation Interpolation](https://arxiv.org/abs/2111.12792) (Shuhong Chen, Matthias Zwicker, 2021) — Identifies aberrations in solid-colour regions as the primary artifact class in 2D animation VFI; proposes Distance Transform Module for correction; establishes LPIPS and Chamfer distance as more appropriate quality metrics than PSNR/SSIM for animation. ; [Thin-Plate Spline-based Interpolation for Animation Line Inbetweening](https://arxiv.org/abs/2408.09131) (Tianyi Zhu, Wei Shang, Dongwei Ren, Wangmeng Zuo, 2024) — Thin-limb sparse pixel distribution causes disconnected lines in VFI; TPS-based geometric transform handles large motion better than optical-flow alone for animation line inbetweening; introduces Weighted Chamfer Distance metric.

### 4-6 Keypose → Inbetween → Palette Cleanup workflow · `recommended` · · community
**The correct production workflow for 2.5D JRPG sprite animation is: author 4-6 intentional keyposes from rig/mesh truth, interpolate to fill gaps, then apply a mandatory palette quantisation and thin-limb cleanup pass — NOT to rely on interpolation to invent poses.**
Neural VFI inbetweeners are a multiplier on authored keyposes, not a substitute for them. The studio authors 4-6 poses per animation cycle using the rig/mesh/proxy motion truth, renders those to sprite frames, then feeds them to FILM or RIFE via ComfyUI-Frame-Interpolation. Interpolation fills the in-between frames. Because VFI injects sub-palette colours and blurs thin limbs (sword edges, finger outlines), a cleanup pass is mandatory: palette quantisation (e.g. Aseprite indexed mode, RGBA→palette clamp, or PixelRefiner) reduces back to the game's fixed colour budget, and thin-limb frames with ghosting are hand-corrected or redone as keyposes.
- **For the pipeline:** Budget: 4 keyposes for a 4-frame walk cycle, 2 keyposes for a fast 2-frame attack (FILM handles the 2-key case). Do NOT attempt to inbetween a full 8-pose walk from a single start and end frame — VFI cannot invent mid-cycle poses accurately. Interpolation quality degrades with distance; keep keypose gaps to ≤3 blank frames for RIFE, ≤5 for FILM.
- **Engine:** comfyui · **Applies to:** walk-cycle, attack-swing, any-sprite-animation · **Kind:** workflow
- **VRAM:** 4-12
- **Output license:** commercial **yes** (license: n/a) — Workflow pattern has no license; tool licenses (FILM Apache-2.0, RIFE MIT, ComfyUI-Frame-Interpolation MIT) govern the software used.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| keypose_count |  | ○ |  |
| palette_depth |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Attempting to interpolate a walk from only a start and end frame — VFI cannot invent mid-cycle body positions accurately. |  |  |  |
| Skipping palette cleanup — interpolated frames carry anti-alias sub-palette pixels that look wrong at sprite scale. |  |  |  |
| Over-interpolating: multiplier=8 between two far-apart poses compounds error multiplicatively. |  |  |  |

- **Best for:** workflow (-, fit -) ; keypose-fill (-, fit -) ; pipeline (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=unverified] -> unverified [only 1 of 3 juror(s) confirmed [confirmed, unverified]]
- **Sources:** [MarkMoHR/Awesome-2D-Animation](https://github.com/MarkMoHR/Awesome-2D-Animation) (MarkMoHR, 2024) — Curated survey of inbetweening tools and papers confirming sparse-keyframe → inbetween → cleanup as the standard 2D animation production pattern.

### Practical-RIFE v4.x (hzwer / Megvii, ECCV 2022) — smooth low-displacement motion · `situational` · ▸ reproduced
**RIFE is the fastest production inbetweener (50-100 fps on RTX 4090-class hardware) and the right choice for smooth walk cycles where adjacent key poses are close together; code and weights both carry MIT from Megvii Inc., but studios should note the weight copyright holder is a Chinese AI company.**
RIFE (Real-Time Intermediate Flow Estimation) uses IFNet to estimate intermediate optical flows end-to-end without a pre-trained flow estimator, achieving real-time throughput. Practical-RIFE (hzwer) is the actively maintained derivative with model versions through v4.26. MIT code and weight license allows commercial use. For sprites, RIFE shines on smooth, low-displacement motion (walk, hover, idle) where the flow field is well-conditioned. On large-displacement or non-linear motion (fast slash) it produces stretching and ghosting artifacts that FILM handles better.
- **For the pipeline:** Use Practical-RIFE v4.6+ for walk cycles, idle animations, hover loops, and any motion where consecutive key poses differ by <30 px at sprite resolution. Preferred for preview-loop iteration because of throughput. For final shipping frames of attack animations, prefer FILM. Evaluate the Megvii copyright on weights per your studio's legal posture — MIT is permissive but the corporate provenance is a due-diligence flag.
- **Engine:** python · **Applies to:** walk-cycle, idle-breathe, low-displacement-smooth, dense-keyframe-fill · **Kind:** model
- **VRAM:** 4-6
- **Output license:** commercial **conditional** (license: MIT (code; pretrained weights explicitly noted as same MIT license per Practical-RIFE README)) — MIT license permits commercial use. However: (1) copyright holder for ECCV2022-RIFE weights is Megvii Inc. — a PRC AI company subject to US entity-list considerations; (2) the weight license note ('we respect the commercial behavior') is informal, not a formal grant — the MIT file is the operative document. Flag with legal before shipping. Practical-RIFE README states 'The content of these links is under the same MIT license as this project,' which is the clearest available weight-license claim.
- **License correction (verifier):** Commercial use is 'yes' (MIT license for both code and weights), not 'conditional'.; claimed_commercial_use should be 'yes' not 'conditional'; MIT explicitly permits commercial use. The note about the weight copyright holder being a Chinese AI company is a supply-chain observation, not a legal restriction under MIT. Also, Practical-RIFE is maintained by hzwer (an individual), not Megvii — Megvii is affiliated with the original RIFE paper authors.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| scale |  | ○ |  |
| exp |  | ○ |  |
| model_version |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Stretching/warping at sprite limb boundaries on fast non-linear swings — ghosting artifacts around contact frames. |  |  |  |
| Poor generalisation to large displacements (>40 px) — optical flow degrades and the synthesised frame looks smeared. |  |  |  |
| Sub-palette colour injection same as FILM — requires quantisation post-process. |  |  |  |

- **Best for:** inbetween (-, fit -) ; smooth-motion (-, fit -) ; fast-preview (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [license -> commercial_use=conditional] [confirmed by 3 of 3 juror(s) [confirmed-with-fixes]]
- **Sources:** [Real-Time Intermediate Flow Estimation for Video Frame Interpolation](https://arxiv.org/abs/2011.06294) (Zhewei Huang, Tianyuan Zhang, Wen Jia, Wenlei Chi, Cheng Chi, Song Hai, 2022) — IFNet end-to-end intermediate flow estimation achieves real-time VFI without a pre-trained flow estimator. ; [hzwer/Practical-RIFE](https://github.com/hzwer/Practical-RIFE) (hzwer (Zhewei Huang), 2022) — MIT license for code; README states weights links carry 'the same MIT license as this project.' Model versions through v4.26 available.

### EMA-VFI: Extracting Motion and Appearance via Inter-Frame Attention (CVPR 2023) · `situational` · · single-run
**EMA-VFI uses inter-frame attention to jointly extract motion and appearance, achieving better perceptual quality on texture-rich sprites than pure optical-flow methods, under an Apache-2.0 license that covers the codebase.**
EMA-VFI (CVPR 2023, MCG-NJU) exploits inter-frame attention to extract both motion correspondences and appearance cues simultaneously, feeding these into a hybrid CNN-Transformer architecture. Correlation information hidden in the attention map enhances appearance synthesis while modelling motion, giving a better quality-efficiency trade-off than prior flow-only methods. Especially useful for painterly high-fidelity sprites where texture detail matters. Apache-2.0 code; weight license not separately documented but the repo LICENSE covers 'the work.'
- **For the pipeline:** Consider EMA-VFI as a quality-ceiling alternative to RIFE when sprite textures are dense (detailed armour, robes, painterly brushwork) and throughput is less critical. Slower than RIFE, faster than FILM in practice. Validate weight license status with MCG-NJU maintainers before shipping, as Apache-2.0 scope on weights is inferred not explicit.
- **Engine:** python · **Applies to:** walk-cycle, attack-swing, texture-rich-sprites, high-fidelity · **Kind:** model
- **VRAM:** 8-16
- **Output license:** commercial **conditional** (license: Apache-2.0 (code; weight license inferred same, not explicitly stated)) — Repository LICENSE file is Apache-2.0. The README states 'This project is released under the Apache 2.0 license' without carving out weights separately. In practice Apache-2.0 is interpreted to cover all distributed artifacts, but the maintainers have not published an explicit weight-specific statement. Flag as conditional pending direct confirmation from MCG-NJU.
- **License correction (verifier):** Commercial use is 'yes' (Apache-2.0 license), not 'conditional'.
- **Fit:** rig 4/5 · studio 3/5
- **Best for:** inbetween (-, fit -) ; high-fidelity (-, fit -) ; texture-rich (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [license -> commercial_use=conditional] [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Extracting Motion and Appearance via Inter-Frame Attention for Efficient Video Frame Interpolation](https://arxiv.org/abs/2303.00440) (Guozhen Zhang, Yuhan Zhu, Haonan Wang, Yourun Zhu, Gangshan Wu, Limin Wang, 2023) — Inter-frame attention simultaneously models motion and enhances appearance, outperforming flow-only methods on perceptual metrics at CVPR 2023. ; [MCG-NJU/EMA-VFI](https://github.com/MCG-NJU/EMA-VFI) (MCG-NJU (Guozhen Zhang et al.), 2023) — Repository states Apache-2.0 license; pretrained model checkpoints distributed from the same repo.

### AnimateDiff SparseCtrl keyframe interpolation docs · `situational` · docs
**Diffusers AnimateDiff SparseControlNet/vid2vid — keyframe animation / sparse-frame interpolation surface; not recipe invent.**
STUDY-037 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT. [no external verdict — not checked]
- **Sources:** [Diffusers AnimateDiff API](https://huggingface.co/docs/diffusers/main/en/api/pipelines/animatediff) — SparseCtrl keyframe / interpolation pipelines.

### Awesome-2D-Animation inventory peer (STUDY-058) · `situational` · docs
**Inbetweening/2D animation tools/datasets/papers collection — inventory peer, not a named tween recipe.**
STUDY-058 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Awesome-2D-Animation](https://github.com/MarkMoHR/Awesome-2D-Animation) — Inbetweening/2D animation tools/datasets/papers collection.

### FILM large-motion frame interpolation (Reda et al. 2022) · `situational` · paper
**Frame interpolation for large motion — keypose→inbetween craft; not a named studio tween recipe.**
STUDY-037 Scholar deepen.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT. [no external verdict — not checked]
- **Sources:** [FILM](https://arxiv.org/abs/2202.04901) — Frame interpolation for large motion.

### FILM large-motion interpolation analog (hold-with-limit) · `situational` · analog
**Synthesize intermediates across large motion — hold as keypose→inbetween method class; FILM ≠ named studio tween recipe.**
STUDY-058 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [FILM](https://arxiv.org/abs/2202.04901) — Frame interpolation for large motion.

### Pose-to-pose / keys-vs-extremes hold-with-limit · `situational` · docs
**Key frames first then inbetweens; storytelling keys ≠ extremes — hold for authored battle keyposes**
STUDY-037 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT. [no external verdict — not checked]
- **Sources:** [Adobe 12 principles pose-to-pose](https://www.adobe.com/creativecloud/animation/discover/principles-of-animation.html) — Pose to Pose: keys then intervals. ; [Keys or extremes](https://theregurge.wordpress.com/2015/02/15/keys-or-extremes-the-big-difference-explained/) — Storytelling keys separate from extremes.

### RIFE real-time intermediate flow interpolation (Huang et al. 2020) · `situational` · paper
**RIFE optical-flow intermediate frames — second inbetween class beside FILM**
STUDY-037 Scholar deepen.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT. [no external verdict — not checked]
- **Sources:** [RIFE](https://arxiv.org/abs/2011.06294) — Real-time intermediate flow estimation.

### GIMM-VFI: Generalizable Implicit Motion Modeling (NeurIPS 2024) — non-commercial reference only · `avoid` · ▸ reproduced
**GIMM-VFI achieves arbitrary-timestep interpolation via implicit neural motion fields but is licensed under S-Lab License 1.0 which explicitly restricts commercial use — it is a benchmark reference, NOT usable in a shipping game without explicit permission from S-Lab.**
GIMM-VFI (NeurIPS 2024, GSeanCDAT) encodes bidirectional optical flows into spatiotemporal motion latents and decodes arbitrary-timestep flows via a coordinate-based neural network, enabling arbitrary-speed interpolation (not just 2x or 4x). Technically impressive for arbitrary-pacing game animations but gated by S-Lab License 1.0 which requires contacting contributors for any commercial redistribution. Include here as a known reference so it does not get mistakenly adopted.
- **For the pipeline:** Do not use GIMM-VFI for any frame that ships in a commercial game. If S-Lab relicenses to Apache/MIT in future, revisit. Monitor the repo for license changes.
- **Engine:** python · **Applies to:** research-reference · **Kind:** model
- **VRAM:** 12-16
- **Output license:** commercial **no** (license: S-Lab License 1.0 (non-commercial only)) — S-Lab License 1.0 explicitly permits use 'for non-commercial purpose only.' Commercial redistribution requires written permission from contributors. This is a hard blocker for a shipping JRPG.
- **Fit:** rig 3/5 · studio 0/5
- **Best for:** research-reference (-, fit -) ; arbitrary-timestep (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, unverified]]
- **Sources:** [Generalizable Implicit Motion Modeling for Video Frame Interpolation](https://arxiv.org/abs/2407.08680) (Zujin Guo, Wei Li, Chen Change Loy, 2024) — Implicit neural motion fields allow arbitrary-timestep VFI; NeurIPS 2024. ; [GSeanCDAT/GIMM-VFI](https://github.com/GSeanCDAT/GIMM-VFI) (Zujin Guo (S-Lab, NTU), 2024) — LICENSE file is S-Lab License 1.0; non-commercial only, commercial use requires contributor permission — confirmed from LICENSE file.

