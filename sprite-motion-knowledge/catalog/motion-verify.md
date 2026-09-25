# Motion verification & QA
_The local verifier gate for motion: root/anchor stability, foot-contact (no slide), hand-to-weapon attachment + weapon length/tip continuity, no frame-to-frame face mutation, silhouette readability, canvas/size consistency; automatable temporal-consistency metrics._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

23 recipes · 8 recommended · 1 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 1 | Anchor the cross-family vision jury with a bug-free reference image (kill false positives on dark/ornate characters) | n/a | all-motion | ▣ measured | ✅ yes | 5 | 5 | · |
| 2 | Frame-to-frame face identity / no-mutation detector | python | verify | ▸ reproduced | ⚠ cond | 4 | 4 | ✓ |
| 2 | Frame-to-frame temporal LPIPS / SSIM consistency | python | verify | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 6 | FVD clip-level motion quality distribution check | python | verify | ▸ reproduced | ✅ yes | 4 | 3 | ✓ |
| 6 | Foot-contact / no-slide detector | python | verify | · community | ⚠ cond | 5 | 4 | ✓ |
| 6 | Root / foot-anchor canvas stability check | python | verify | · community | ✅ yes | 5 | 5 | ✓ |
| 6 | SigLIP2 / CLIP identity-to-reference across animation frames | python | verify | · community | ✅ yes | 5 | 5 | ✓ |
| 6 | Silhouette readability check (thumbnail-scale alpha legibility) | python | verify | · community | ✅ yes | 5 | 5 | ✓ |
| 6 | Weapon length/tip continuity detector | python | verify | · community | ✅ yes | 5 | 5 | ✓ |
| 9 | Animator Survival Kit — keys/extremes analog | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | Flicker fusion threshold — frame budget analog | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | GlitchBench — LMM game-glitch detection (Taesiri et al. 2023) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | LLVM phi / SSA — cross-frame identity analog | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | LPIPS PerceptualSimilarity site | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | LPIPS arXiv — perceptual similarity gate | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | LPIPS perceptual metric literature (Zhang et al. 2018) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | TLA stuttering steps — hit-stop analog | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | Twelve principles — pose-to-pose analog | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | Unity IK — foot lock analog | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | Unity Root Motion — feet-based root lock | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | Unity Transform rigid weapon-chain hold | docs | all-motion | docs | check | 4 | 4 | · |
| 10 | Optical-flow warping error for temporal coherence | python | verify | · community | ⚠ cond | 5 | 3 | ✓ |
| 15 | Cross-family vision-LLM QA jury (reasoning-stripped, refute-by-default) | custom | verify | · community | ✅ yes | 5 | 5 | · |

## Detail

### Anchor the cross-family vision jury with a bug-free reference image (kill false positives on dark/ornate characters) · `recommended` · ▣ measured
**A refute-by-default cross-family vision jury with a defect taxonomy but NO bug-free reference image hallucinates defects ('melted', 'collapsed', 'detached', 'shards') on dark plate-armor + tattered-cloth + spiky-silhouette characters — failing even a CLEAN bind pose. The fix (grounded, not optional) is to give each check an explicit bug-free REFERENCE render so the jury compares against known-clean instead of free-associating.**
MEASURED ON RIG (2026-06-25, blackguard): the jury fails the CLEAN re-rigged bind pose (rest front 1/3, back 1/3) and the clean posed guard (side/back), flagging 'melted forearm', 'collapsed lower body', 'foot shards' that full-res inspection shows are NOT present (solid greaves, solid sabatons, clean creased elbow). The intended tattered cape/loincloth reads as 'torn' and the intentionally spiky pauldrons read as 'blobby protrusions'. minimax-m3 is the reliable juror here; kimi-k2.6 and the gemini canary over-refute the aesthetic. This is the PREDICTED failure mode of reference-less VLM visual-QA: GlitchBench (Taesiri et al.) shows VLM QA needs explicit defect categories AND a bug-free reference image to be reliable. FIX: (1) pass a known-clean reference render of the same character per check (the bind-pose render, jury-passed) so the prompt says 'compare to this clean reference; flag only NEW defects'; (2) tell the jury which features are intended (ragged cloth, spiked pauldrons, horns); (3) weight the jurors (minimax > kimi/gemini on ornate dark characters) or expand the roster; (4) keep the human full-res look as the final arbiter (the full-res law). Self-certification is still forbidden; the reference anchor makes the external verifier trustworthy.
- **For the pipeline:** Before batching 68 mostly-dark-armored characters through the jury, add the reference-anchor: store each character's jury-passed bind-pose render as its reference, and have _rigqa.py pass it alongside the test image with a 'flag only deviations from this clean reference' prompt + an intended-features note. Re-tune the consensus rule (canary stays advisory; consider minimax-weighted). Without this, the jury blocks clean assets and the batch stalls on false positives.
- **Engine:** n/a · **Applies to:** all-motion · **Kind:** technique
- **VRAM:** n/a (cloud jury, server-side)
- **Validated under:** ollama-cloud jury (minimax-m3 / kimi-k2.6 / gemini-3-flash canary), refute-by-default 2-of-3; blackguard clean hifi rig fails rest+guard on hallucinated defects contradicted by full-res inspection.
- **Output license:** commercial **yes** (license: n/a) — Verifier tooling; no license constraint.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Jury fails a clean asset, flagging melted/collapsed/detached geometry not present at full-res | Reference-less refute-by-default VLM QA free-associates defects on dark/ornate/ragged characters; intended cloth and spikes read as damage | Pass a bug-free reference render per check + an intended-features note; weight reliable jurors; confirm any flag at full-res before acting | summary |

- **Best for:** vision-qa (-, fit -) ; verifier (-, fit -) ; batch-gate (-, fit -)
- **Verify:** no external verdict — not checked
- **Sources:** [GlitchBench: Can Large Multimodal Models Detect Video Game Glitches?](https://arxiv.org/abs/2312.05291) (Mohammad Reza Taesiri et al., 2024) — VLM visual-QA needs explicit defect categories and a bug-free reference image to be reliable; without a reference, models miss real defects and hallucinate false ones. ; [Prometheus / panel-of-LLM-judges robustness (cross-family verification)](https://arxiv.org/abs/2404.18796) (Verga et al. (PoLL), 2024) — A disjoint-family judge panel is less biased than a single judge; juror reliability varies, supporting reliability-weighting over flat consensus.

### Frame-to-frame face identity / no-mutation detector · `recommended` · ▸ reproduced
**Computing ArcFace (or equivalent) embedding distance between a reference face crop and every animation frame detects frame-to-frame face mutation — AI polish steps that redraw or hallucinate facial features across frames.**
Crop the face region from a designated reference frame and from each animation frame. Extract a 512-d identity embedding with an ArcFace-family model. Compute cosine distance between each frame's embedding and the reference. Flag any frame exceeding a tuned identity-drift threshold. For painterly 2.5D sprites the face is stylized, so perceptual similarity (LPIPS on the face crop) may complement or replace embedding distance if ArcFace struggles with the art style. IMPORTANT: InsightFace pre-trained model weights (buffalo_l, etc.) are non-commercial by default — use the perceptual fallback or obtain commercial licensing.
- **For the pipeline:** Face mutation is a canonical AI artifact — the model redraws eyebrows, eye shape, or skin tone between frames. This check blocks a frame set from shipping until mutation frames are re-fixed or masked.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 2
- **Output license:** commercial **conditional** (license: Code: MIT (InsightFace repo). Model weights: non-commercial research only (InsightFace pre-trained weights); commercial license available via insightface.ai.) — InsightFace MODEL WEIGHTS (buffalo_l, antelopev2, etc.) are explicitly non-commercial for research purposes only. Commercial use of weights requires separate licensing from InsightFace (contact recognition-oss-pack@insightface.ai). The LPIPS-face-crop fallback avoids this restriction entirely and is recommended for commercial production.
- **Fit:** rig 4/5 · studio 4/5

**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | ArcFace cosine distance vs reference |  | cosine distance < 0.30 (lower = more similar; community heuristic for same-identity) | — | InsightFace python-package or manual ArcFace |
| metric | LPIPS face-crop distance (fallback for commercial; avoids weight license issue) |  | LPIPS < 0.10 between consecutive face crops | — | lpips python package (Zhang et al. 2018) |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [ArcFace: Additive Angular Margin Loss for Deep Face Recognition](https://arxiv.org/abs/1801.07698) (Jiankang Deng, Jia Guo, Jing Yang, Niannan Xue, Irene Kotsia, Stefanos Zafeiriou, 2019) — ArcFace produces 512-d angular-margin identity embeddings; cosine distance between embeddings of the same person is reliably low, making it a practical same-identity gate. ; [InsightFace — State-of-the-art 2D and 3D Face Analysis Project](https://github.com/deepinsight/insightface) (deepinsight, 2025) — InsightFace provides the buffalo_l ArcFace model for face embedding extraction; code is MIT-licensed but pre-trained weights are non-commercial research use only — commercial license required for product deployment. ; [InsightFace Enterprise Face Recognition Model Licensing](https://www.insightface.ai/services/models-commercial-licensing) (InsightFace, 2025) — Pre-trained InsightFace models (buffalo_l, antelopev2, etc.) require separate commercial licensing; available via recognition-oss-pack@insightface.ai.

### Frame-to-frame temporal LPIPS / SSIM consistency · `recommended` · ▸ reproduced
**Computing per-consecutive-frame LPIPS and SSIM across an animation sequence catches sudden large perceptual changes (AI redraws, flicker, inpainting artifacts) that are invisible in single-frame review.**
For each pair of consecutive frames in an animation clip, compute SSIM (Wang et al. 2004) and LPIPS (Zhang et al. 2018). Track the distribution over the clip. Frames with LPIPS spike above a threshold indicate an inpainting discontinuity or AI hallucination frame. SSIM drops below a threshold indicate global structure break. Plot the per-frame curves for visual debug. This is a temporal extension of the static-sprite LPIPS gate already used in sprites-knowledge for turnaround consistency.
- **For the pipeline:** Surfaces flicker frames and AI artifact frames that single-frame review misses. A failing frame halts the animation from entering the sprite-sheet assembler.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 1
- **Output license:** commercial **yes** (license: BSD / MIT (lpips, torchmetrics, scikit-image)) — LPIPS python package (BSD-3-Clause). scikit-image SSIM is BSD-3-Clause. No restrictive weights for the metric itself (uses pretrained AlexNet/VGG internally; commercially permissive).
- **License correction (verifier):** torchmetrics is Apache-2.0, not BSD/MIT; scikit-image is BSD-3-Clause, not MIT. LPIPS (lpips package) is BSD-2-Clause.
- **Fit:** rig 5/5 · studio 5/5

**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | per-frame LPIPS (consecutive pairs) |  | mean LPIPS < 0.10; no single frame > 0.20 | — | lpips python (pip install lpips) |
| metric | per-frame SSIM (consecutive pairs) |  | SSIM > 0.85 between consecutive frames | — | scikit-image structural_similarity |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed] -> confirmed [license -> commercial_use=yes] [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [The Unreasonable Effectiveness of Deep Features as a Perceptual Metric](https://arxiv.org/abs/1801.03924) (Richard Zhang, Phillip Isola, Alexei A. Efros, Eli Shechtman, Oliver Wang, 2018) — LPIPS measures perceptual distance between image patches using deep CNN features; applied frame-to-frame it detects perceptual discontinuities that PSNR/SSIM miss. ; [Image quality assessment: From error visibility to structural similarity](https://ece.uwaterloo.ca/~z70wang/research/ssim/) (Zhou Wang, Alan C. Bovik, Hamid R. Sheikh, Eero P. Simoncelli, 2004) — SSIM captures luminance, contrast, and structural similarity between images; a drop in consecutive-frame SSIM flags global structural breaks in animation sequences.

### FVD clip-level motion quality distribution check · `situational` · ▸ reproduced
**Fréchet Video Distance measures the distributional distance between a set of generated animation clips and a reference set in I3D feature space, capturing both visual quality and temporal coherence as a population-level metric.**
FVD (Unterthiner et al. 2018) uses a pre-trained I3D network to embed video clips, then computes Fréchet distance between the multivariate Gaussians of generated and reference clip sets. For studio use: build a small reference set of hand-approved 'gold' animation clips per character class (walk/attack/idle). FVD of new generation batches against the gold set flags distributional drift — systematic AI degradation across a batch run. FVD is a batch metric, not a per-clip gate; use per-frame LPIPS/SSIM for individual clip gating.
- **For the pipeline:** FVD catches systematic pipeline degradation (e.g., a ComfyUI sampler change that degrades temporal quality across all outputs) that per-clip checks might miss. Run at the end of a full batch generation to validate the generation run before review.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 4
- **Output license:** commercial **yes** (license: Apache-2.0 (Google Research FVD implementation)) — Google Research FVD implementation is Apache-2.0. I3D weights (Kinetics pre-trained) used in FVD are from DeepMind; the kinetics-i3d weights on GitHub are Apache-2.0. Verify current license at the repo before production use.
- **Fit:** rig 4/5 · studio 3/5

**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | FVD (lower = better; 0 = identical distributions) |  | FVD vs gold-set < 50 (to-be-calibrated on studio character set; community FVD thresholds are dataset-specific) | — | google-research/frechet_video_distance |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Towards Accurate Generative Models of Video: A New Metric & Challenges](https://arxiv.org/abs/1812.01717) (Thomas Unterthiner, Sjoerd van Steenkiste, Karol Kurach, Raphael Marinier, Marcin Michalski, Sylvain Gelly, 2018) — FVD uses I3D features to measure distributional distance between sets of real and generated videos; achieved 74.9–81% agreement with human quality judgments across 3,000 models, outperforming PSNR/SSIM/FID. ; [frechet_video_distance — Google Research implementation](https://github.com/google-research/google-research/tree/master/frechet_video_distance) (Google Research, 2024) — Reference Apache-2.0 implementation of FVD using I3D embeddings.

### Foot-contact / no-slide detector · `recommended` · · community
**Tracking the foot pixel cluster between the contact frame and the next frame detects foot-slide — the contact-pose foot should not translate horizontally while the ground contact is held.**
Identify contact frames by heuristic (lowest non-transparent pixel cluster centroid touches the canvas bottom band) or from the animation manifest. Between consecutive contact-region frames, compute the horizontal displacement of the foot-pixel centroid using optical flow (RAFT) or direct pixel-cluster centroid delta. If the foot centroid translates more than a threshold while contact is held, flag as slide. For 8-direction sprites, apply per-direction horizontal-axis separately.
- **For the pipeline:** Foot-slide is immediately visible on the ground plane and breaks physical believability. This gate must pass before walk-cycle frames are composited into the sprite sheet.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 2
- **Output license:** commercial **conditional** (license: Apache-2.0 (RAFT code); see commercial_notes for model weights) — RAFT code is BSD/MIT licensed on GitHub. The pre-trained RAFT weights (princeton-vl/RAFT) have no explicit commercial restriction in their repo (BSD-3-Clause), but always verify the current license before commercial deployment. Centroid-only approach avoids weights entirely.
- **License correction (verifier):** RAFT code (princeton-vl/RAFT) is MIT-licensed, not Apache-2.0. Correct claimed_license to 'MIT (RAFT code)'; weights remain research-use so commercial_use stays conditional.; RAFT code license is BSD-3-Clause (princeton-vl/RAFT), not Apache-2.0 as claimed.; RAFT code license is BSD-3-Clause, not Apache-2.0; the weights are under the same permissive license, so commercial use is yes, not conditional.
- **Fit:** rig 5/5 · studio 4/5

**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | foot-centroid-horizontal-delta (px) between held-contact frames |  | < 2 px horizontal drift during contact hold | — | custom python; optional RAFT flow for sub-pixel precision |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [license -> commercial_use=conditional] [confirmed by 3 of 3 juror(s) [confirmed-with-fixes]]
- **Sources:** [RAFT: Recurrent All-Pairs Field Transforms for Optical Flow](https://arxiv.org/abs/2003.12039) (Zachary Teed, Jia Deng, 2020) — RAFT computes dense pixel-level optical flow with state-of-the-art accuracy; the flow field can track the displacement of the foot pixel cluster between frames to measure slide.

### Root / foot-anchor canvas stability check · `recommended` · · community
**Comparing the foot-anchor pixel coordinate (or bounding-box bottom-center) across every frame of an animation detects root/anchor jitter — frames where the character 'floats' relative to the canvas grid.**
Parse each frame's alpha channel bounding box. The bottom-center Y of the bounding box (or an explicit anchor pixel marked in the sprite manifest) should be constant across all frames of an idle/walk cycle. Record the per-frame Y value; flag any frame where the anchor drifts beyond a 1–2 pixel tolerance. Extend to canvas-size consistency: all frames must share identical W×H pixel dimensions and the same foot-anchor definition from the export manifest.
- **For the pipeline:** A jitter-failing sprite will bob or teleport in-engine, breaking the ground plane illusion. This check runs before canvas assembly and catches AI-inpainting artifacts that shift the character up or down.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a (method)) — Pure NumPy/OpenCV alpha-channel bounding box logic; no external weights.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| AI polish step that crops or pads alpha unevenly |  |  |  |
| Per-frame canvas size mismatch from export pipeline |  |  |  |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | anchor-Y-jitter (px max deviation from median) |  | ≤ 1 px for idle; ≤ 2 px for walk/run | — | custom python (numpy alpha bbox) |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [NumPy nonzero / where for alpha-channel bounding box](https://numpy.org/doc/stable/reference/generated/numpy.nonzero.html) (NumPy contributors, 2025) — np.nonzero on the alpha channel returns row/col indices of non-transparent pixels; min/max give the bounding box and thus the foot-anchor row.

### SigLIP2 / CLIP identity-to-reference across animation frames · `recommended` · · community
**Computing SigLIP2 or CLIP image-embedding cosine similarity between each animation frame and a canonical reference image of the character detects gradual identity drift — AI repaint steps that slowly shift the character's visual identity across frames or views.**
Embed the approved reference sprite (front-facing, rest pose) and each animation frame with SigLIP2 (arXiv:2502.14786) or CLIP. Compute cosine similarity between each frame embedding and the reference. Track the per-frame similarity curve — a drop signals identity drift in that frame. This is a temporal extension of the static-sprite turnaround consistency gate used in the sibling sprites-knowledge KB (which uses SigLIP2/CLIP for 8-direction turnaround consistency). The motion-verify lane applies the same pattern temporally across animation frames rather than across directions.
- **For the pipeline:** Identity drift is subtle and often missed in frame-by-frame review but shows as character 'aging' or 'shape-shifting' in playback. This gate surfaces drifting frames before they enter the sprite sheet.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 2
- **Output license:** commercial **yes** (license: Apache-2.0 (open_clip / transformers SigLIP2 implementation)) — SigLIP2 weights released by Google with Apache-2.0 license via HuggingFace. CLIP (OpenAI) weights are MIT-licensed. Both are commercially permissive.
- **Fit:** rig 5/5 · studio 5/5

**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | SigLIP2 cosine similarity to reference (higher = more similar) |  | cosine similarity > 0.85 for all frames vs reference | — | transformers SigLIP2 or open_clip |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](https://arxiv.org/abs/2502.14786) (Michael Tschannen, Alexey Gritsenko, Xiao Wang, Muhammad Ferjad Naeem, Ibrahim Alabdulmohsin, Nikhil Parthasarathy, Talfan Evans, Lucas Beyer, Ye Xia, Basil Mustafa, Olivier Hénaff, Jeremiah Harmsen, Andreas Steiner, Xiaohua Zhai, 2025) — SigLIP 2 improves on SigLIP with captioning-based pretraining and self-supervised losses; outperforms SigLIP on zero-shot classification, image-text retrieval, and visual representation at all model scales — making its image embeddings strong identity-similarity signals.

### Silhouette readability check (thumbnail-scale alpha legibility) · `recommended` · · community
**Downscaling the sprite to 64×64 and 32×32 and measuring the alpha-channel convex-hull compactness and silhouette continuity catches unreadable or fragmented silhouettes before the sprite reaches the engine.**
Load each frame's RGBA. Extract the alpha mask. Compute the contour and convex hull of the alpha region. Measure: (1) solidity = contour-area / convex-hull-area — a low value indicates a fragmented or spiky silhouette; (2) bounding-box fill ratio; (3) at thumbnail scale (32px height), check that the alpha silhouette remains a single connected component with no isolated islands. Flag frames where silhouette breaks into disconnected components at thumbnail scale or where solidity drops below a tuned threshold. This catches AI inpainting that introduces hair/weapon fragments outside the main alpha region.
- **For the pipeline:** Unreadable silhouettes are a design axiom in the JRPG tradition — characters must be instantly readable in 8-direction combat. A failed frame at thumbnail scale will be indistinguishable from environment clutter in-game.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a (method using OpenCV)) — Pure OpenCV alpha-channel contour analysis; no restrictive weights.
- **Fit:** rig 5/5 · studio 5/5

**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | alpha-silhouette solidity (contour area / convex hull area) |  | solidity > 0.75; single connected component at 32px-height thumbnail | — | custom python (cv2 contourArea + convexHull) |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [OpenCV structural analysis and shape descriptors — convexHull, contourArea](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html) (OpenCV contributors, 2025) — cv2.convexHull + cv2.contourArea give solidity = filled-area / hull-area; a measure of silhouette compactness and fragmentation directly applicable to sprite alpha-channel readability. ; [The Power of Silhouette: Designing Readable Characters In Motion](https://binus.ac.id/bandung/dkv/2025/11/04/the-power-of-silhouette-designing-readable-characters-in-motion/) (BINUS DKV, 2025) — Strong silhouettes that read clearly at a glance are a foundational design principle for game characters; used here to justify the thumbnail-scale silhouette gate.

### Weapon length/tip continuity detector · `recommended` · · community
**Segmenting the weapon per frame/view and checking its pixel length and tip-vector variance is the primary automatable gate for the #1 motion defect: per-view weapon drift and detachment.**
For each frame and each 8-direction view, isolate the weapon via color-range or instance segmentation, then measure grip-to-tip pixel distance and the tip vector angle (via contour moments). Compute variance of length and angle across the full animation and turnaround set. A variance spike beyond a tuned threshold is a hard fail. The rig's bone chain should guarantee rigidity by construction — a fail therefore indicates that the AI polish or composite step broke rigidity and must be re-run.
- **For the pipeline:** Hard-fail gate for any weapon-bearing character before sprite-sheet export. A fail blocks shipping and triggers re-inpainting or recompositing — not a warning, a stop.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a (method)) — Method uses OpenCV contour/moment analysis only. No restrictive weights involved.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| length_variance_pct |  % | ○ | Tune on reference set |
| tip_angle_delta_deg |  degrees | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| AI inpainting that redraws the weapon free-hand across views |  |  |  |
| Composite that clips the weapon tip outside canvas on some views |  |  |  |
| Perspective foreshortening on 3/4 views producing legitimate apparent shortening — threshold should account for known-good foreshortening per-view-slot |  |  |  |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | weapon-length-variance (px, % of mean length) |  | < 5% length variance across views/frames; tip-angle delta < 8° | — | custom python (cv2 contour + moments) |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [OpenCV contour and moments documentation](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html) (OpenCV contributors, 2025) — cv2.moments() on a segmented region yields pixel area, centroid, and orientation; combined with bounding-rect or min-enclosing-rect, gives grip-to-tip length and angle per frame.

### Animator Survival Kit — keys/extremes analog · `situational` · docs
**Analog: storytelling keys and contact extremes before straight-ahead fills. Holds for authored battle keyposes.**
Analog: storytelling keys and contact extremes before straight-ahead fills. Holds for authored battle keyposes.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Animator Survival Kit — keys/extremes analog](https://archive.org/details/TheAnimatorsSurvivalKitRichardWilliams) — Analog: storytelling keys and contact extremes before straight-ahead fills. Holds for authored battle keyposes.

### Flicker fusion threshold — frame budget analog · `situational` · docs
**Analog: below ~48-60 Hz flicker/jerk is visible. Holds for JRPG frame-budget / hit-stop readability.**
Analog: below ~48-60 Hz flicker/jerk is visible. Holds for JRPG frame-budget / hit-stop readability.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Flicker fusion threshold — frame budget analog](https://en.wikipedia.org/wiki/Flicker_fusion_threshold) — Analog: below ~48-60 Hz flicker/jerk is visible. Holds for JRPG frame-budget / hit-stop readability.

### GlitchBench — LMM game-glitch detection (Taesiri et al. 2023) · `situational` · paper
**LMM game-glitch detection; jury/defect taxonomy — STUDY-058 deepen peer**
STUDY-058 Scholar deepen.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [GlitchBench](https://arxiv.org/abs/2312.05291) — LMM game-glitch detection; jury/defect taxonomy.

### LLVM phi / SSA — cross-frame identity analog · `situational` · docs
**Analog: one identity value chosen per predecessor edge at a merge. Holds for cross-frame face/identity as single-assignment.**
Analog: one identity value chosen per predecessor edge at a merge. Holds for cross-frame face/identity as single-assignment.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [LLVM phi / SSA — cross-frame identity analog](https://llvm.org/docs/LangRef.html#phi-instruction) — Analog: one identity value chosen per predecessor edge at a merge. Holds for cross-frame face/identity as single-assignment.

### LPIPS PerceptualSimilarity site · `situational` · docs
**Zhang et al. PerceptualSimilarity project page for LPIPS.**
Zhang et al. PerceptualSimilarity project page for LPIPS.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [LPIPS PerceptualSimilarity site](https://richzhang.github.io/PerceptualSimilarity/) — Zhang et al. PerceptualSimilarity project page for LPIPS.

### LPIPS arXiv — perceptual similarity gate · `situational` · paper
**Analog: deep-feature distance as perceptual similarity. Holds for frame-to-frame temporal LPIPS/SSIM gates.**
Analog: deep-feature distance as perceptual similarity. Holds for frame-to-frame temporal LPIPS/SSIM gates.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [LPIPS arXiv — perceptual similarity gate](https://arxiv.org/abs/1801.03924) — Analog: deep-feature distance as perceptual similarity. Holds for frame-to-frame temporal LPIPS/SSIM gates.

### LPIPS perceptual metric literature (Zhang et al. 2018) · `situational` · paper
**LPIPS deep-feature perceptual distance — admission-gate literature; not a flip of 33/117/486.**
STUDY-037 Scholar deepen.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT. [no external verdict — not checked]
- **Sources:** [LPIPS](https://arxiv.org/abs/1801.03924) — Deep features as perceptual metric.

### TLA stuttering steps — hit-stop analog · `situational` · docs
**Analog: steps that leave relevant vars unchanged are allowed. Partial hold for hit-stop / freeze frames.**
Analog: steps that leave relevant vars unchanged are allowed. Partial hold for hit-stop / freeze frames.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [TLA stuttering steps — hit-stop analog](https://lamport.azurewebsites.net/tla/rhtml/stuttering-step.html) — Analog: steps that leave relevant vars unchanged are allowed. Partial hold for hit-stop / freeze frames.

### Twelve principles — pose-to-pose analog · `situational` · docs
**Analog: pose-to-pose + anticipation to action to follow-through before inbetweens. Holds for keypose-first combat craft.**
Analog: pose-to-pose + anticipation to action to follow-through before inbetweens. Holds for keypose-first combat craft.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Twelve principles — pose-to-pose analog](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation) — Analog: pose-to-pose + anticipation to action to follow-through before inbetweens. Holds for keypose-first combat craft.

### Unity IK — foot lock analog · `situational` · docs
**Analog: foot IK + Bake Into Pose / feet-based root lock kill slide. Holds for foot-contact and root/anchor stability gates.**
Analog: foot IK + Bake Into Pose / feet-based root lock kill slide. Holds for foot-contact and root/anchor stability gates.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Unity IK — foot lock analog](https://docs.unity3d.com/Manual/InverseKinematics.html) — Analog: foot IK + Bake Into Pose / feet-based root lock kill slide. Holds for foot-contact and root/anchor stability gates.

### Unity Root Motion — feet-based root lock · `situational` · docs
**Analog: Bake Into Pose / feet-based root lock kill slide. Holds for root/anchor stability gates.**
Analog: Bake Into Pose / feet-based root lock kill slide. Holds for root/anchor stability gates.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Unity Root Motion — feet-based root lock](https://docs.unity3d.com/Manual/RootMotion.html) — Analog: Bake Into Pose / feet-based root lock kill slide. Holds for root/anchor stability gates.

### Unity Transform rigid weapon-chain hold · `situational` · docs
**Child inherits parent; tip rigidly offset from grip — hold for hand→weapon_grip→weapon_tip checks**
STUDY-037 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT. [no external verdict — not checked]
- **Sources:** [Unity Transform](https://docs.unity3d.com/Manual/class-Transform.html) — Parent-child rigid transform hierarchy.

### Optical-flow warping error for temporal coherence · `situational` · · community
**Warping frame N to frame N+1 using estimated optical flow and measuring the pixel-level residual error detects temporal incoherence — AI flicker, ghosting, and motion discontinuities not caught by LPIPS alone.**
Estimate optical flow between frame pairs using RAFT. Warp frame N to frame N+1 using backward warping with the flow field and an occlusion mask. Compute per-pixel L1 residual between the warped prediction and the actual frame N+1. Report mean warping error across the clip. Note: warping error has known limitations — ground-truth video naturally has non-zero warping error due to flow estimation noise and legitimate inter-frame change (Relational Warping Error/RWE subtracts a reference ground-truth baseline to compensate). Treat as a relative comparison metric, not an absolute pass/fail criterion.
- **For the pipeline:** Warping error exceeding baseline provides a motion-coherence signal that complements frame-to-frame LPIPS. Spikes on specific frames pinpoint AI artifact frames for targeted re-fix.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 3
- **Output license:** commercial **conditional** (license: BSD-3-Clause (RAFT code, princeton-vl/RAFT); check current repo for weight license) — RAFT code is BSD-3-Clause. Pre-trained weights from princeton-vl/RAFT GitHub are BSD-3-Clause as of 2024; verify before commercial release. Alternative: use torchvision's built-in RAFT which inherits PyTorch BSD license.
- **License correction (verifier):** RAFT code is MIT-licensed at princeton-vl/RAFT, not BSD-3-Clause. Update claimed_license to 'MIT (RAFT code); weights research-use, check repo for current terms'.
- **Fit:** rig 5/5 · studio 3/5

**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | mean per-pixel warping error (L1, normalized 0–1) |  | relative: flag frames with warping error > 2× clip median | — | custom python: RAFT flow + backward warp + L1 residual |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [license -> commercial_use=conditional] [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [RAFT: Recurrent All-Pairs Field Transforms for Optical Flow](https://arxiv.org/abs/2003.12039) (Zachary Teed, Jia Deng, 2020) — RAFT produces accurate dense optical flow; used as the flow estimator for backward warping in temporal coherence measurement.

### Cross-family vision-LLM QA jury (reasoning-stripped, refute-by-default) · `avoid` · · community
**A jury of 3 non-same-family cloud vision models — with reasoning hidden from other jurors, a strict refute-by-default posture, and 2-model consensus required to pass — catches defects that automated metrics miss, including contextual weapon drift, pose implausibility, and face mutation that survives embedding checks.**
This is a codified version of the studio's existing _concept_vision_qa.py pattern: route each animation clip or suspicious-frame set to a jury of 3 non-Qwen cloud vision models (e.g., Gemini-2.5-Pro as hyper-strict canary, MiniMax-M3, Kimi Vision). Each model receives the frame set plus a defect checklist (weapon drift, foot slide, face mutation, silhouette break, anchor jitter) with instructions to refute by default — assume defective unless evidence is clear. Reasoning is not shown to other jurors. 2-of-3 PASS required for the frame set to proceed. Gemini's solo flag is treated as a soft warning requiring human review even if 2-of-3 pass. Reference: Hidden Clones (arXiv:2603.17111) demonstrates that same-family VLM ensembles produce correlated errors; cross-family is load-bearing for this pattern.
- **For the pipeline:** The QA jury is the final gate before sprite-sheet assembly. Automated metrics pass first; the jury catches semantic defects. This pattern is already proven in the studio's concept pipeline (_concept_vision_qa.py) — the motion-verify lane extends it to animation frame sets.
- **Engine:** custom · **Applies to:** verify · **Kind:** eval
- **VRAM:** 0
- **Output license:** commercial **yes** (license: n/a (cloud API calls; no local weights)) — All three cloud vision APIs (Gemini, MiniMax, Kimi) are commercially available. Check current API ToS for game-asset production use cases.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Same-family model ensemble produces correlated misses (all miss the same defect) — cross-family is load-bearing |  |  |  |
| Models hallucinate defects on stylized painterly art more than photorealistic; refute-by-default posture must be balanced with art-style context in the prompt |  |  |  |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| qualitative | jury-consensus (2-of-3 PASS) |  | 2-of-3 cloud vision models PASS the defect checklist | — | _concept_vision_qa.py pattern extended to animation frame sets |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=refuted] -> confirmed; not-found x1 [refuted by 1 of 3 juror(s) [confirmed, confirmed-with-fixes, refuted]]
- **Sources:** [Hidden Clones: Exposing and Fixing Family Bias in Vision-Language Model Ensembles](https://arxiv.org/abs/2603.17111) (Anonymous (under review), 2026) — VLM ensembles built from same-family models (sharing architecture, training data, pre-training) produce correlated errors; cross-family diversity is necessary for ensemble gains — directly motivates using non-same-family models in the QA jury. ; [VideoGameQA-Bench: Evaluating Vision-Language Models for Video Game Quality Assurance](https://arxiv.org/abs/2505.15952) (Mrigank Pawagi et al. (asgaardlab), 2025) — VLMs can generate useful bug reports for >50% of glitches in video game QA tasks (GPT-4o: 54% image, 52% video); benchmarks game-asset visual defect detection, validating VLM-as-QA-judge applicability for game production. ; [LLM Juries for Evaluation — Comet blog](https://www.comet.com/site/blog/llm-juries-for-evaluation/) (Comet ML, 2025) — An LLM jury uses multiple models from distinct families; consensus reduces single-model bias and improves evaluation reliability over single-judge approaches.

