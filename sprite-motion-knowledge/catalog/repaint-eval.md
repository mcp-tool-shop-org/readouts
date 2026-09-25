# Repaint QA gate
_QA specific to repaint: identity preserved (face-distance), weapon continuity, style-match to the house reference (SigLIP/CLIP), no over-smoothing / detail-loss, palette adherence. Extends motion-verify to the repaint stage._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

8 recipes · 8 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | Identity-preserved check (CLIP/DINOv2 face-crop distance, repaint-vs-approved) | python | verify | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 2 | Over-smoothing / detail-loss detection (Laplacian-variance + GLCM energy before-vs-after) | python | verify | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Palette adherence (Earth Mover's Distance on color histograms vs. approved palette) | python | verify | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Style-match score (SigLIP2/CLIP cosine) to the approved house baseline | python | verify | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Temporal-flicker metric for repainted cycle (LPIPS frame-delta + optical-flow warping error) | python | verify | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 6 | Cross-family vision-LLM jury for repaint style + painterly + not-anime verdict | custom | verify | · community | ✅ yes | 5 | 5 | · |
| 6 | Repaint accept/reject gate: assembling all sub-metrics into a single admission decision | python | verify | · community | ✅ yes | 5 | 5 | · |
| 6 | Weapon-continuity check post-repaint (length + tip position, reuse wave-1 detector) | python | verify | · community | ✅ yes | 5 | 5 | · |

## Detail

### Identity-preserved check (CLIP/DINOv2 face-crop distance, repaint-vs-approved) · `recommended` · ▸ reproduced
**After the AI repaint step, the character's identity (face region) must match the approved sprite baseline. Cosine distance between CLIP or DINOv2 embeddings of the face crop — repainted frame vs. approved reference — gates identity drift without requiring NC-restricted ArcFace/InsightFace weights.**
Crop the face region (using the existing bounding-box detector from the wave-1 face-lock step) from each repainted frame and the approved identity reference. Embed both crops with DINOv2 ViT-B/14 (Apache-2.0) or CLIP ViT-L/14 and compute cosine similarity. A tuned threshold (calibrated on a small approved-vs-rejected sprite set) gates admission. InsightFace ArcFace weights give a tighter identity metric but are non-commercial — flag and use CLIP/DINOv2 as the production fallback. LPIPS on the face crop is a complementary low-cost signal.
- **For the pipeline:** The repaint pipeline must not alter face identity (painterly style should affect rendering, not character likeness). This gate runs immediately post-repaint before any sprite-sheet assembly. DINOv2 features are strong enough for character consistency without NC weight risk.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 2-4
- **Output license:** commercial **conditional** (license: DINOv2 Apache-2.0; CLIP MIT (OpenAI); ArcFace/InsightFace weights NON-COMMERCIAL — see commercial_notes) — DINOv2 (Apache-2.0) and CLIP (MIT) are commercial-clean. InsightFace pre-trained model weights (buffalo_l, antelopev2) are NC research-only — confirmed by maintainers and community reports (HN 2024). Contact recognition-oss-pack@insightface.ai for commercial licensing. Studio MUST use DINOv2/CLIP path in production.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| ArcFace weights are NC: do NOT ship InsightFace embeddings in the commercial gate without a commercial license. |  |  |  |
| CLIP face crops may conflate style change with identity change — always compare same render style (approved repainted reference, not mesh render). |  |  |  |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | DINOv2-ViT-B14-cosine (face crop) |  | >=0.85 (tune on approved-vs-rejected set) | — | python / torch.nn.functional.cosine_similarity |
| metric | LPIPS (face crop, repaint vs. approved) |  | <=0.15 (tune) | — | lpips PyPI package |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193) (Oquab, Darcet, et al. (Meta AI), 2023) — DINOv2 ViT features (Apache-2.0) produce strong all-purpose visual representations suitable for identity similarity scoring without labeled data. ; [ArcFace: Additive Angular Margin Loss for Deep Face Recognition](https://arxiv.org/abs/1801.07698) (Deng, Guo, Xue, Zafeiriou, 2019) — ArcFace (via InsightFace) is the state-of-the-art face embedding; pre-trained weights are NC-restricted and require commercial licensing. ; [deepinsight/insightface — license notice](https://github.com/deepinsight/insightface) (InsightFace maintainers, 2024) — Pre-trained model packs (buffalo_l, antelopev2) are for non-commercial research only; commercial licensing required from maintainers. ; [Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020) (Radford, Kim, Hallacy, et al. (OpenAI), 2021) — CLIP ViT image encoder (MIT license) provides commercial-clean cross-modal image similarity embeddings suitable as an identity-distance fallback.

### Over-smoothing / detail-loss detection (Laplacian-variance + GLCM energy before-vs-after) · `recommended` · ▸ reproduced
**AI repaints commonly over-smooth the mesh render, erasing cloth wrinkles, armor scratches, and fine edge work. Comparing Laplacian-variance (edge sharpness) and GLCM texture energy between the mesh-render source and the repainted output detects unacceptable detail loss before the sprite sheet is assembled.**
For each repainted frame, compute (1) Laplacian-variance of the grayscale repainted frame vs. the mesh-render source — a low-variance repaint relative to source signals blur; (2) GLCM energy (homogeneity / contrast features) before and after — a sharp rise in GLCM energy/homogeneity signals texture erasure toward flat color. Both metrics require no model weights and run in milliseconds per frame. Thresholds are per-asset (different characters have different natural texture density), so calibrate on a 'golden' accepted repaint set. A dedicated FFT high-frequency energy ratio is an optional third signal.
- **For the pipeline:** Detail-loss is a production risk specific to img2img pipelines with too-high denoising strength. This gate catches it quantitatively before visual QA. Pair with hparam search on denoising_strength to find the sweet spot for each character/weapon combo.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 0
- **Output license:** commercial **yes** (license: scikit-image BSD-3; OpenCV Apache-2.0; all no NC restriction) — Pure signal-processing metrics via scikit-image and OpenCV; no model weights involved.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| glcm_distances |  | ○ | Pixel-pair offsets for co-occurrence matrix. |
| glcm_angles |  | ○ | Four orientations, averaged. |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | Laplacian-variance ratio (repaint / mesh-render source) |  | >=0.7 (ratio; tune per character) | — | cv2.Laplacian + np.var |
| metric | GLCM contrast delta (repaint - source) |  | >= -0.15 (drop; tune per character) | — | skimage.feature.graycomatrix / graycoprops |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Textural Features for Image Classification](https://ieeexplore.ieee.org/document/4309314) (Haralick, Shanmugam, Dinstein, 1973) — Established GLCM texture features (energy, contrast, homogeneity) as discriminative texture descriptors; skimage.feature implements these directly. ; [OpenCV blur detection via Laplacian variance (cv2.Laplacian + np.var)](https://docs.opencv.org/4.x/) (OpenCV contributors, 2024) — Laplacian-variance is the standard focus/sharpness metric in production CV pipelines; a low variance relative to a reference frame signals over-smoothing.

### Palette adherence (Earth Mover's Distance on color histograms vs. approved palette) · `recommended` · ▸ reproduced
**The house palette is part of the style contract. After repainting, each frame's Lab-space color histogram must stay within Earth Mover's Distance (EMD / Wasserstein-1) of the approved palette — catching drifts such as desaturation, hue shift, or introduction of out-of-palette colors.**
Extract the 3D Lab-space color histogram (or a k-means palette vector) of each repainted frame and compare to the approved-palette histogram using scipy.stats.wasserstein_distance (per-channel 1D) or a full EMD implementation. A low EMD means the frame's color distribution closely matches the approved palette. This is especially important for 2.5D sprites where consistent color signatures distinguish factions, moods, and character roles. Run on the non-transparent pixels only (mask out alpha=0). Threshold tuned on approved-vs-rejected repaint pairs.
- **For the pipeline:** Palette drift is a silent quality failure that passes visual spot-checks but degrades the game's chromatic cohesion. Gate on per-frame EMD; flag frames with palette drift for targeted repaint retries with adjusted color conditioning.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 0
- **Output license:** commercial **yes** (license: scipy BSD-3; no NC restriction) — scipy.stats.wasserstein_distance (1D EMD) is BSD-3, commercial-clean. Full EMD via POT library is MIT.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| colorspace |  | ○ | Perceptually uniform; better than RGB for palette distance. |
| histogram_bins |  | ○ | Balance between granularity and compute. |
| alpha_mask |  | ○ | Exclude transparent pixels from histogram. |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | Wasserstein-1 distance (per-channel Lab, repainted vs. approved palette) |  | <=0.05 (normalized 0-1 Lab; tune on approved set) | — | scipy.stats.wasserstein_distance per channel, averaged |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [The Earth Mover's Distance as a Metric for Image Retrieval](https://link.springer.com/article/10.1023/A:1026543900054) (Rubner, Tomasi, Guibas, 2000) — EMD / Wasserstein distance on color histograms better reflects perceptual color similarity than chi-square or L2 histogram distance; widely used in content-based image retrieval. ; [scipy.stats.wasserstein_distance](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wasserstein_distance.html) (SciPy contributors, 2024) — scipy implements 1D Wasserstein-1 distance directly; applying it per Lab channel is a standard palette-distance approach.

### Style-match score (SigLIP2/CLIP cosine) to the approved house baseline · `recommended` · ▸ reproduced
**Scoring each repainted frame's SigLIP2 (or CLIP) cosine similarity to the approved house-style baseline set gates whether the repaint actually landed the painterly style — catching both 'still looks 3D' and 'over-stylized off-model' failures.**
Embed the approved style baseline (a few shipped sprites) and each repainted output with SigLIP2; flag any frame whose cosine to the baseline centroid falls below a tuned threshold. SigLIP2 is Apache-2.0 and is already used by the studio's ai-eyes-mcp evaluator, making this zero-additional-dependency. Pairs with the cross-family vision-LLM jury for the qualitative 'is it painterly / not anime' call. The metric alone cannot distinguish 'painterly but wrong character' from 'painterly correct character' — use alongside the identity gate.
- **For the pipeline:** The core repaint admission metric — a repaint that does not match the house baseline is rejected before it reaches the sprite sheet. Reuses ai-eyes-mcp (SigLIP2). Approved baseline must be version-controlled as part of the style canon.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 2-6
- **Output license:** commercial **yes** (license: SigLIP2 Apache-2.0; CLIP MIT) — SigLIP2 weights Apache-2.0; CLIP MIT; both commercial-clean.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| baseline_set_size |  | ○ | Number of approved canonical sprites used to form the style centroid. More is better up to ~32. |
| embed_model |  | ○ | Swap to CLIP ViT-L/14 if SigLIP2 unavailable. |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | SigLIP2-cosine-to-house-centroid |  | >=0.x (tune on shipped sprite set) | — | ai-eyes-mcp (studio SigLIP2 evaluator) |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features](https://arxiv.org/abs/2502.14786) (Tschannen, Gritsenko, et al. (Google), 2025) — SigLIP2 image encoder (Apache-2.0) outperforms SigLIP on zero-shot classification and image-text retrieval; robust image-similarity embeddings for style matching. ; [Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020) (Radford, Kim, Hallacy, et al. (OpenAI), 2021) — CLIP cosine similarity is a proven style-distance proxy and commercial-clean fallback when SigLIP2 is unavailable.

### Temporal-flicker metric for repainted cycle (LPIPS frame-delta + optical-flow warping error) · `recommended` · ▸ reproduced
**Frame-independent repaints of a sprite cycle produce temporal flickering that is invisible in single-frame review. Computing LPIPS between consecutive repainted frames — normalized by the mesh-render LPIPS as a baseline — and the optical-flow warping error on the repainted sequence quantifies repaint-induced flicker beyond natural motion.**
For each consecutive pair of repainted frames (f_t, f_{t+1}): (1) compute LPIPS(f_t, f_{t+1}) and normalize by LPIPS(m_t, m_{t+1}) where m is the mesh-render source — a ratio >1 means the repaint added temporal variation beyond what the pose change explains; (2) compute the optical-flow warping error using RAFT flow estimated on the repainted sequence — warp f_t to f_{t+1} using RAFT flow, measure pixel-error between warped f_t and f_{t+1}. The relational warping error (RWE) variant (subtract GT frame difference) corrects for natural motion. Frames exceeding either threshold are flagged for re-render or coherence post-processing.
- **For the pipeline:** Temporal coherence is the hardest repaint QA axis because it requires evaluating the full cycle, not individual frames. Flag cycles (not just frames) that fail the temporal gate; the remedy is often adjusting img2img seed consistency or adding a temporal consistency post-pass (e.g., blind video prior or flow-guided coherence). This extends the wave-1 temporal-stability metric to the repainted cycle.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 2-4
- **Output license:** commercial **conditional** (license: LPIPS BSD; RAFT Apache-2.0) — LPIPS weights BSD-licensed (lpips PyPI); RAFT implementation Apache-2.0 (princeton-vl/RAFT). Both commercial-clean.
- **License correction (verifier):** RAFT original repo (princeton-vl/RAFT) does not carry an Apache-2.0 license; use torchvision's RAFT implementation (BSD-3-Clause) for commercial-clean access. The RWE citation (arXiv:2102.05822) could not be independently confirmed — verify before relying on it.; RAFT weights (princeton-vl/RAFT) are released for NON-COMMERCIAL research use and inherit restrictions from Sintel/FlyingChairs/KITTI training data; not Apache-2.0. Use RAFT only with commercial-licensed weights/retrains, or substitute a commercial-clean flow model (e.g. torchvision RAFT with appropriate backbone) for production. The LPIPS license is correctly BSD-2-Clause, and the RWE concept is real but the specific arxiv id 2102.05822 could not be independently confirmed as the canonical RWE paper — recommend citing the original temporal-consistency work (e.g. Lai et al. or the stylized-video RWE paper) with a verified id.
- **Fit:** rig 5/5 · studio 5/5

**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | LPIPS-ratio (repainted pair / mesh-render pair) |  | <=1.3 (ratio; tune per action type) | — | lpips PyPI package (AlexNet backbone) |
| metric | Optical-flow warping error (RAFT, repainted sequence) |  | <=0.05 RMSE (normalized; tune) | — | princeton-vl/RAFT + custom warping error script |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [license -> commercial_use=conditional] [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [The Unreasonable Effectiveness of Deep Features as a Perceptual Metric (LPIPS)](https://arxiv.org/abs/1801.03924) (Zhang, Isola, Efros, Shechtman, Wang, 2018) — LPIPS deep perceptual metric aligns with human judgment on image patch similarity; using frame-pair LPIPS as a temporal flicker signal is a standard practice in video quality research. ; [RAFT: Recurrent All-Pairs Field Transforms for Optical Flow](https://arxiv.org/abs/2003.12039) (Teed, Deng, 2020) — RAFT achieves SOTA optical flow estimation (Sintel EPE 2.855 px) and is the standard backbone for warping-error temporal consistency evaluation; Apache-2.0. ; [Frame Difference-Based Temporal Loss for Video Stylization](https://arxiv.org/abs/2102.05822) (Chen et al., 2021) — Establishes relational warping error (RWE) — subtract GT frame difference from warp error — as a more accurate temporal consistency metric than raw warping error in stylized video.

### Cross-family vision-LLM jury for repaint style + painterly + not-anime verdict · `recommended` · · community
**Quantitative metrics cannot catch 'technically within threshold but qualitatively wrong' repaint failures. The studio's existing cross-family vision-LLM jury (_concept_vision_qa.py: minimax-m3 / kimi / gemini, refute-by-default, 2-of-3 consensus, gemini as hyper-strict canary) is extended to the repaint axis: did the frame land a genuine painterly look, avoid the anime aesthetic, and preserve approved character design?**
Submit a 2-up comparison image (approved reference | repainted candidate) to the existing _concept_vision_qa.py jury with a repaint-specific rubric: (1) is the style painterly and consistent with the approved reference (not over-rendered, not flat-shaded, not 3D-looking, not anime)? (2) is character identity preserved? (3) is any palette deviation noticeable? Each model returns accept/reject + a reasoning note; 2-of-3 consensus is required for acceptance; a gemini reject alone triggers manual review (canary rule). The jury is the final qualitative gate before sprite-sheet assembly — only frames that pass all metric gates AND the jury are admitted.
- **For the pipeline:** The vision-LLM jury is the catch-all for metric-blind failures. Because the jury is already built and proven on concept QA, the marginal cost of adding a repaint rubric is low. Repaint-specific jury calls run per-cycle (one call per action, not per frame) to manage API cost. Log all jury outputs with reasoning for audit.
- **Engine:** custom · **Applies to:** verify · **Kind:** eval
- **VRAM:** 0
- **Output license:** commercial **yes** (license: External cloud APIs (minimax-m3, kimi, gemini) — no local weight NC issue) — API-based models; commercial use governed by each provider's API ToS. Gemini (Google), kimi (Moonshot AI), minimax-m3 (MiniMax) — verify ToS before shipping outputs derived from their APIs. As of 2025, all three permit commercial output under standard API agreements.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| jury_models |  | ○ | Studio-standard non-Qwen cloud family; refute-by-default framing. |
| call_frequency |  | ○ | Submit a representative frame from the cycle; full cycle review on borderline cases. |
| rubric_version |  | ○ | Version-control the rubric prompt; a prompt change invalidates prior baselines. |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| qualitative | 2-of-3 cross-family vision-LLM jury verdict (accept/reject) |  | 2-of-3 accept; gemini reject → manual escalation | — | _concept_vision_qa.py (studio harness) — repaint rubric extension |

- **Verify:** cross-family jury [deepseek-v4-pro=unverified glm-5.2=unverified minimax-m3=unverified] -> unverified [only 0 of 3 juror(s) confirmed [unverified]]

### Repaint accept/reject gate: assembling all sub-metrics into a single admission decision · `recommended` · · community
**Each sub-metric (identity, weapon rigidity, style match, detail loss, palette adherence, temporal flicker, jury verdict) is a necessary but not sufficient gate. The combined repaint gate runs all six metric checks and the jury check; a frame/cycle passes only if all checks pass, and failures are tagged with which gate(s) triggered for actionable diagnosis.**
A thin Python orchestrator runs the six quantitative metric recipes in sequence (identity-check → weapon-rigidity → style-match → detail-loss → palette-adherence → temporal-flicker) and then submits passing frames/cycles to the vision-LLM jury. Output is a per-frame/per-cycle structured record: {slug, frame_id, passed, failures: [{gate, metric, value, threshold}]}. A failed gate short-circuits downstream sprite-sheet assembly and routes the frame to the retry queue with the failure tag. All thresholds are externally configurable (YAML/JSON) to support per-character tuning without code changes. This gate is the admission checkpoint between the repaint pipeline and sprite-sheet assembly.
- **For the pipeline:** Tag-based failure routing enables targeted re-renders: a 'palette' failure → retry with stronger palette conditioning; a 'temporal' failure → retry with seed pinning or coherence post-pass; a 'identity' failure → retry with higher face-preservation ControlNet weight. The gate design is an andon stop (ANDON_AUTHORITY, workflow standard) — bad output does not propagate downstream.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 0
- **Output license:** commercial **yes** (license: Studio orchestrator code (no external weights)) — Orchestrator is pure studio Python; commercial-clean. Depends only on sub-metric licenses documented per recipe above.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| thresholds_file |  | ○ | Per-character, per-action threshold overrides. Version-controlled alongside canon. |
| short_circuit |  | ○ | Skip remaining metric gates after first failure to save compute. |
| jury_gate_on_metric_pass_only |  | ○ | Vision-LLM jury runs only if all 6 metric gates pass; avoids API spend on clearly-failed frames. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Thresholds are to-be-tuned: ship with conservative (wide) defaults and tighten per character as golden approved-repaint sets accumulate. |  |  |  |
| Do not lock thresholds into code — any hardcoded threshold that cannot be overridden per-character is a maintenance hazard. |  |  |  |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| gate | all-pass (6 metric gates AND jury pass) |  | all sub-gates pass (see individual recipes for per-metric thresholds) | — | repaint_gate.py (studio orchestrator) |

- **Verify:** cross-family jury [deepseek-v4-pro=unverified glm-5.2=unverified minimax-m3=unverified] -> unverified [only 0 of 3 juror(s) confirmed [unverified]]
- **Sources:** [The Unreasonable Effectiveness of Deep Features as a Perceptual Metric (LPIPS)](https://arxiv.org/abs/1801.03924) (Zhang, Isola, Efros, Shechtman, Wang, 2018) — LPIPS is used as a temporal-flicker sub-metric in the gate; cited here as the primary external metric paper underpinning the gate assembly.

### Weapon-continuity check post-repaint (length + tip position, reuse wave-1 detector) · `recommended` · · community
**The repaint step must not deform the weapon geometry. Reusing the wave-1 weapon-length and tip-position detector on the repainted frame versus the mesh-render source frame catches any repaint-induced weapon deformation (smearing, inpainting artifacts, style hallucination).**
Run the wave-1 weapon geometry extractor (length in pixels, tip-point coordinates) on the mesh-render frame and the corresponding repainted output. Compare: length deviation must be under a pixel tolerance and tip displacement under a fixed threshold. Because the wave-1 detector already handles this, the repaint gate simply adds a 'repainted frame' input channel and reuses all existing logic. Failures indicate the diffusion/img2img step hallucinated or smeared the weapon.
- **For the pipeline:** Repaint QA does not need a new weapon detector — extend the wave-1 harness to accept a (mesh_render, repainted) pair and report delta. Keeps the gate cheap and the harness unified.
- **Engine:** python · **Applies to:** verify · **Kind:** eval
- **VRAM:** 0
- **Output license:** commercial **yes** (license: Pipeline logic (studio code); no external weight restriction) — Pure geometry measurement on pixel data; no licensed model weights involved.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| High-strength repaint (high denoising strength / low img2img strength) is the most common cause of weapon smear — pair threshold with strength hparam. |  |  |  |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Harness |
|---|---|---|---|---|---|
| metric | weapon-length-delta (pixels, repaint vs. mesh-render source) |  | <=3 px (tune per sprite resolution) | — | wave-1 weapon detector, repaint extension |
| metric | tip-displacement (pixels) |  | <=5 px | — | wave-1 weapon detector, repaint extension |

- **Verify:** cross-family jury [deepseek-v4-pro=unverified glm-5.2=unverified minimax-m3=unverified] -> unverified [only 0 of 3 juror(s) confirmed [unverified]]

