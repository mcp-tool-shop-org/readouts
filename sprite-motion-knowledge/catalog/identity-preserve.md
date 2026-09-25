# Identity & face preservation
_Keeping the APPROVED face/character through repaint + across frames: face-preserve (de-lit), IP-Adapter-FaceID, inpaint-only / low-denoise face regions, ArcFace-guided locks. License-aware (InsightFace weights are NC)._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

13 recipes · 3 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | IP-Adapter (base, ViT-bigG) reference-image identity conditioning | comfyui | identity | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 2 | Masked-face differential-denoise repaint (preserve the approved face) | comfyui | identity | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 5 | Cross-frame face region anchor — locking identity across animation frames | comfyui | identity | community-confirmed-primary-source | ✅ yes | 5 | 5 | · |
| 9 | IP-FaceDiff identity lock analog (hold-with-limit) | docs | all-motion | analog | check | 4 | 4 | · |
| 9 | IP-FaceDiff identity-preserving facial video edit (Anand et al. 2025) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | Identity-preserving pose-guided facial landmarks (Mu et al. 2024) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | LLVM phi/SSA identity merge analog (hold-with-limit) | docs | all-motion | docs | check | 4 | 4 | · |
| 9 | LTX Face Attention Anchor — cross-frame face lock surface | comfy | all-motion | docs | check | 4 | 4 | · |
| 14 | ArcFace / InsightFace face embedding — identity measurement + lock (NON-COMMERCIAL — flagged) | python | identity | primary-source-confirmed | ⛔ no | 5 | 2 | ✓ |
| 14 | Face-restoration avoidance — GFPGAN / CodeFormer WRONG for painterly sprites | comfyui | identity | community-confirmed-primary-source | ⛔ no | 0 | 0 | ✓ |
| 14 | IP-Adapter-FaceID — face-ID conditioning (NON-COMMERCIAL — flagged) | comfyui | identity | primary-source-confirmed | ⛔ no | 4 | 0 | ✓ |
| 14 | InstantID — zero-shot face-ID generation (NON-COMMERCIAL — flagged) | comfyui | identity | primary-source-confirmed | ⛔ no | 4 | 0 | ✓ |
| 14 | PuLID-Flux face-ID conditioning — NON-commercial (FLUX-based; avoid for shipping) | comfyui | identity | community-reported-with-primary-source | ⛔ no | 4 | 4 | · |

## Detail

### IP-Adapter (base, ViT-bigG) reference-image identity conditioning · `recommended` · ▸ reproduced
**The non-FaceID IP-Adapter (Apache 2.0, OpenCLIP-ViT-bigG image encoder) can inject the approved concept-art face as a reference image, biasing generation toward that character's identity without any NC face-recognition encoder.**
IP-Adapter base uses an OpenCLIP ViT-bigG encoder (Apache 2.0 / OpenAI open weight, no InsightFace) to embed a reference image. Setting adapter weight 0.3–0.6 alongside the body ControlNet channels biases the sampler toward the reference character's face/palette. The signal is weaker than FaceID variants but is commercial-clean and avoids the InsightFace NC trap. Best used in combination with the differential-denoise mask.
- **For the pipeline:** Complement the masked-face-differential-denoise recipe with a light IP-Adapter base injection (weight 0.3–0.5) when cross-view drift is mild. Stronger weights can fight the ControlNet structure guidance — test at 0.35 first.
- **Engine:** comfyui · **Applies to:** identity · **Base:** SDXL · **Kind:** technique
- **VRAM:** 16–24
- **Output license:** commercial **yes** (license: Apache 2.0 (code and weights; image encoder: OpenCLIP-ViT-bigG which is MIT/Apache)) — IP-Adapter base (h94/IP-Adapter, Apache 2.0) uses OpenCLIP ViT-bigG — not InsightFace/ArcFace — so no NC restriction. FaceID variant is a separate model with NC restrictions; this recipe explicitly uses the non-FaceID base model.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| adapter_weight |  | ○ |  |
| encoder |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| High adapter weight (>0.65) overrides the ControlNet structure pass and produces pose drift. |  |  |  |
| Does not lock hard facial landmarks — combine with masked-face-differential-denoise for structural face lock. |  |  |  |

- **Best for:** license-clean (-, fit -) ; commercial (-, fit -) ; identity-bias (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [h94/IP-Adapter — Hugging Face model card](https://huggingface.co/h94/IP-Adapter) (Hu et al. (Tencent AI Lab), 2024) — Base IP-Adapter is Apache 2.0, uses OpenCLIP-ViT-H-14 (SD1.5) or ViT-bigG-14 (SDXL) — no InsightFace dependency; commercial use permitted.

### Masked-face differential-denoise repaint (preserve the approved face) · `recommended` · ▸ reproduced
**Masking the face region and repainting it at low denoise strength (~0.2–0.3) while the body repaints at higher strength preserves the approved painterly face through the style pass — no face-recognition weights required, making it fully commercial-clean.**
Segment the face bounding box (e.g. via SAM or a static mask); in the ControlNet repaint graph route the face sub-region through a Differential Diffusion node at denoise ~0.2–0.3 and route the body at 0.6–0.8. The approved face survives nearly untouched while the body picks up the house painterly style. Pairs directly with the studio's existing de-lit face-preserve pass. No InsightFace, ArcFace, or any NC face-ID model is touched.
- **For the pipeline:** This is the default, license-clean identity lock for the §D repaint. Use it first. Reserve heavier face-ID conditioning (IP-Adapter or PuLID) only for cases where differential masking alone still drifts across views or frames.
- **Engine:** comfyui · **Applies to:** identity · **Kind:** technique
- **VRAM:** 16–28
- **Output license:** commercial **yes** (license: n/a (masking + differential-denoise technique); Qwen-Image-Edit-2511 Apache 2.0 base) — Pure masking plus differential denoise — no face-recognition weights, so none of the InsightFace/ArcFace NC restrictions apply. Commercial-clean on any Apache-licensed diffusion base.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| face_denoise |  | ○ |  |
| body_denoise |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| If face mask bleeds into collar or hair the style boundary looks seamed — tighten mask or feather it. |  |  |  |
| At <0.15 denoise the face lighting no longer responds to the body relight, producing a flat-faced phantom effect. |  |  |  |

- **Best for:** identity-lock (-, fit -) ; license-clean (-, fit -) ; commercial (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=unverified] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, confirmed-with-fixes, unverified]]
- **Sources:** [Differential Diffusion: Giving Each Pixel Its Strength](https://arxiv.org/abs/2306.00950) (Eran Levin, Ohad Fried, 2023) — Introduces per-pixel / per-region denoise strength control inside diffusion sampling; lower strength in a masked region preserves original pixels while surrounding regions change freely. ; [Differential Diffusion node — ComfyUI feature request thread](https://github.com/Comfy-Org/ComfyUI/issues/2671) (Comfy-Org community, 2024) — Confirms Differential Diffusion is implemented in ComfyUI via a dedicated node accepting a per-pixel change-map mask alongside Inpaint Model Conditioning.

### Cross-frame face region anchor — locking identity across animation frames · `recommended` · community-confirmed-primary-source
**For the repainted animation strip, locking the face region as an attention anchor across frames (via an LTX-style face attention anchor node or cross-frame reference masking) prevents identity drift from accumulating across the walk/attack/idle sprite frames.**
In a multi-frame repaint pass (e.g. idle, walk, attack strips), each frame is resampled independently and identity drift accumulates. The ComfyUI LTX Face Attention Anchor node addresses this by targeting the face bounding box of a chosen anchor frame and propagating that identity signal across the sequence. Alternative: encode the approved concept face once as an IP-Adapter reference, keep adapter weight constant across all frames, and combine with the per-frame differential-denoise face mask. IP-FaceDiff (WACVW 2025, Anand et al.) demonstrates that targeted fine-tuning for cross-frame face identity achieves 80% speedup while maintaining temporal consistency.
- **For the pipeline:** For sprite animation strips: (1) designate frame 0 of the idle animation as the face anchor; (2) run all subsequent frames with the anchor face embedding held constant; (3) apply cross-frame DINOv2 cosine distance eval to catch any accumulated drift before export. This is the temporal complement to the single-frame masked-face-differential-denoise technique.
- **Engine:** comfyui · **Applies to:** identity · **Kind:** technique
- **VRAM:** 16–28
- **Output license:** commercial **yes** (license: n/a (technique); LTX node: ComfyUI custom node (MIT); IP-Adapter base: Apache 2.0) — The anchoring technique itself has no license. ComfyUI LTX Face Attention Anchor is a custom node MIT-licensed. IP-Adapter base (Apache 2.0) used as the identity carrier does not touch InsightFace. Commercial-clean as long as no InsightFace/ArcFace weights are loaded.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| anchor_frame |  | ○ |  |
| depth_curve |  | ○ |  |
| face_denoise_all_frames |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| If the anchor frame itself has a poorly relit face, drift is locked to a bad reference — review anchor quality first. |  |  |  |
| Windowed batch processing for long strips can break anchor propagation at window boundaries — use overlapping windows normalized by the DINOv2 eval. |  |  |  |

- **Best for:** temporal-coherence (-, fit -) ; cross-frame-identity (-, fit -) ; animation (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=unverified] -> unverified [only 1 of 3 juror(s) confirmed [confirmed, unverified]]
- **Sources:** [ComfyUI Node: LTX Face Attention Anchor](https://www.runcomfy.com/comfyui-nodes/10S-Comfy-nodes/ltx-face-attention-anchor) (10S-Comfy-nodes (community), 2025) — Node anchors face identity to a bounding-box region of a chosen anchor frame and propagates the signal across the video/frame sequence; depth curve controls per-frame anchoring strength. ; [IP-FaceDiff: Identity-Preserving Facial Video Editing with Diffusion](https://arxiv.org/abs/2501.07530) (Anand, Tharun; Garg, Aryan; Mitra, Kaushik, 2025) — Targeted fine-tuning of a pre-trained T2I diffusion model for cross-frame face identity preservation achieves 80% reduction in editing time while maintaining temporal consistency across varying head poses and expressions.

### IP-FaceDiff identity lock analog (hold-with-limit) · `situational` · analog
**Diffusion facial video edit preserving identity across frames — hold for cross-frame face/identity lock; ≠ flip leftover prism.**
STUDY-058 Analogist Verifier ✅ hold-with-limit. Flips 33/117/486: 0.
- **For the pipeline:** STUDY-058 Verifier ✅. Flips 33/117/486: 0. Recipes invented: 0.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0; flips 33/117/486: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; flips 33/117/486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [IP-FaceDiff](https://arxiv.org/abs/2501.07530) — Identity-preserving facial video editing.

### IP-FaceDiff identity-preserving facial video edit (Anand et al. 2025) · `situational` · paper
**Diffusion facial video editing that preserves identity across frames — leftover craft**
STUDY-037 Scholar deepen.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0; flips 33/117/486: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT — do not invent-verify 33/117/486. [no external verdict — not checked]
- **Sources:** [IP-FaceDiff](https://arxiv.org/abs/2501.07530) — Identity-preserving facial video editing.

### Identity-preserving pose-guided facial landmarks (Mu et al. 2024) · `situational` · paper
**Pose-guided character animation with facial-landmark transform for identity retention — no studio recipe invent.**
STUDY-037 Scholar deepen.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0; flips 33/117/486: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT — do not invent-verify 33/117/486. [no external verdict — not checked]
- **Sources:** [Identity-Preserving Pose-Guided](https://arxiv.org/abs/2412.08976) — Facial landmark transform for identity under pose.

### LLVM phi/SSA identity merge analog (hold-with-limit) · `situational` · docs
**One identity at merge from predecessors — hold for cross-frame face lock; limit ≠ CLIP drift**
STUDY-037 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0; flips 33/117/486: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT — do not invent-verify 33/117/486. [no external verdict — not checked]
- **Sources:** [LLVM LangRef phi](https://llvm.org/docs/LangRef.html#phi-instruction) — SSA phi merges predecessor values.

### LTX Face Attention Anchor — cross-frame face lock surface · `situational` · docs
**Face identity via bbox (face_bbox_norm, tracked modes) — cross-frame face lock surface; recipes invented: 0.**
STUDY-058 Practitioner Verifier ✅. Flips 33/117/486: 0.
- **For the pipeline:** STUDY-058 Verifier ✅. Flips 33/117/486: 0. Recipes invented: 0.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0; flips 33/117/486: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; flips 33/117/486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [LTX Face Attention Anchor](https://www.runcomfy.com/comfyui-nodes/10S-Comfy-nodes/ltx-face-attention-anchor) — Face identity via bbox; tracked modes.

### ArcFace / InsightFace face embedding — identity measurement + lock (NON-COMMERCIAL — flagged) · `avoid` · primary-source-confirmed
**ArcFace / InsightFace embeddings (buffalo_l / antelopev2) are the most discriminative face-identity distance metric available, but the pretrained weights are NC research-only. For commercial pipelines use DINOv2 (Apache 2.0) or SigLIP cosine distance as the identity-lock eval metric.**
ArcFace (CVPR 2019) trains a face embedding via additive angular margin loss, producing 512-dim vectors with state-of-the-art discriminability on identity. InsightFace ships pretrained buffalo_l / antelopev2 checkpoints that implement ArcFace. These are the most reliable face-ID distance metric for detecting identity drift across repaint frames. However, the weights are explicitly 'available for non-commercial research purposes only.' For the commercial pipeline, replace with DINOv2 ViT-L/14 (Apache 2.0, Meta) cosine distance as the identity eval signal — empirically validated for re-ID tasks. SigLIP (Google, Apache 2.0 via open-clip) is a further option.
- **For the pipeline:** Use DINOv2 cosine distance as the automated identity-lock eval metric in the studio pipeline. Run it frame-to-frame across the sprite animation strip and across the 8-view repaint set. Flag frames where cosine distance exceeds threshold (empirically ~0.12 on DINOv2 ViT-L embeddings) for manual review. Never commit ArcFace/buffalo_l weights to the repo.
- **Engine:** python · **Applies to:** identity · **Kind:** eval
- **VRAM:** 4–8
- **Output license:** commercial **no** (license: ArcFace pretrained weights: NC research only (InsightFace policy); DINOv2 Apache 2.0 (commercial-clean fallback)) — InsightFace README and GitHub issue #2022: 'training data and models trained with these data are available for non-commercial research purposes only.' ArcFace torch README: 'The models are available for non-commercial research purposes only.' Commercial licensing for buffalo_l / antelopev2: recognition-oss-pack@insightface.ai. Commercial fallback: DINOv2 ViT-L/14 (Apache 2.0, Meta) or SigLIP ViT-SO400M (Apache 2.0 via open_clip_pytorch); both produce 768–1024-dim embeddings usable as face-identity distance metrics without NC restrictions.
- **Fit:** rig 5/5 · studio 2/5
- **Best for:** identity-measurement (-, fit -) ; eval (-, fit -) ; drift-detection (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [ArcFace: Additive Angular Margin Loss for Deep Face Recognition](https://arxiv.org/abs/1801.07698) (Deng, Jiankang; Guo, Jia; Xue, Niannan; Zafeiriou, Stefanos, 2019) — Introduces additive angular margin loss for face recognition producing highly discriminative 512-dim embeddings; basis for InsightFace pretrained ArcFace weights. ; [ArcFace torch README — InsightFace model zoo license](https://github.com/deepinsight/insightface/blob/master/recognition/arcface_torch/README.md) (InsightFace / deepinsight, 2023) — Model Zoo section: 'The models are available for non-commercial research purposes only.' ; [DINOv2 — Apache 2.0 commercial-clean alternative](https://arxiv.org/abs/2304.07193) (Oquab, Maxime et al. (Meta AI), 2023) — DINOv2 ViT-L/14 (Apache 2.0) produces robust visual features for re-ID tasks including face similarity; Meta explicitly re-licensed DINOv2 to Apache 2.0 for commercial use.

### Face-restoration avoidance — GFPGAN / CodeFormer WRONG for painterly sprites · `avoid` · community-confirmed-primary-source
**GFPGAN and CodeFormer are photoreal face-restoration tools trained on photographic data; applying them to painterly sprites destroys the painterly style and pushes faces toward hyperreal photography. Do not use them in the studio pipeline.**
GFPGAN (TencentARC, trained on FFHQ-scale photographic data) and CodeFormer (NeurIPS 2022, S-Lab/NTU) both optimize toward photoreal face quality. Their GAN priors strongly push any input face toward the appearance of a photographic portrait — the opposite of a painterly 2.5D sprite style. Testing confirms: applying either to non-photorealistic styles produces distortion and style destruction. CodeFormer is additionally NC-only (S-Lab License 1.0). Neither has a place in the studio repaint pipeline.
- **For the pipeline:** Reject any node graph that includes a GFPGAN or CodeFormer post-pass. If a node author adds one as a 'face fix' step, remove it. The studio's approved face comes from the concept art; restoration models will mutate it toward a photograph.
- **Engine:** comfyui · **Applies to:** identity · **Kind:** technique
- **VRAM:** 4–8
- **Output license:** commercial **no** (license: GFPGAN: Apache 2.0 (code) but NC-flagged dependencies; CodeFormer: S-Lab License 1.0 (NC only)) — CodeFormer is explicitly non-commercial (S-Lab License 1.0, sczhou/CodeFormer). GFPGAN is Apache 2.0 code but community discussion flags potential NC third-party component issues (TencentARC/GFPGAN discussions/616 unanswered). Beyond license: the primary concern is style destruction — both tools are categorically wrong for painterly sprites regardless of license. Confirmed by SD community: 'You should only use Restore faces when you want to fix faces in photorealistic images.'
- **License correction (verifier):** GFPGAN's code AND its shipped pretrained face-restoration weights are Apache 2.0 (TencentARC/GFPGAN LICENSE) — there is no NC-flagged dependency in the main package. CodeFormer under S-Lab License 1.0 is correctly NC-only. The advice to avoid both for painterly sprites is sound, but GFPGAN's license status should be stated as Apache 2.0, not 'NC-flagged dependencies.'
- **Fit:** rig 0/5 · studio 0/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Pushes painterly face toward hyperreal photo appearance — destroys house style. |  |  |  |
| CodeFormer S-Lab License 1.0 explicitly prohibits commercial redistribution. |  |  |  |
| GFPGAN NC dependency flag unresolved per maintainers. |  |  |  |

- **Best for:** avoidance-note (-, fit -) ; style-protection (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [license -> commercial_use=no] [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [TencentARC/GFPGAN — GitHub repository](https://github.com/TencentARC/GFPGAN) (Wang, Xintao et al. (Tencent ARC Lab), 2021) — GFPGAN targets practical real-world face restoration; its StyleGAN2 prior is trained on photographic data — applies photorealistic face priors that fight painterly sprite styles. ; [Towards Robust Blind Face Restoration with Codebook Lookup Transformer](https://arxiv.org/abs/2206.11253) (Zhou, Shangchen et al. (S-Lab, NTU), 2022) — CodeFormer (NeurIPS 2022) optimizes for photoreal face quality via a codebook lookup transformer; the S-Lab License 1.0 restricts to non-commercial use. ; [CodeFormer LICENSE — S-Lab License 1.0](https://github.com/sczhou/CodeFormer/blob/master/LICENSE) (sczhou / S-Lab NTU, 2022) — S-Lab License 1.0 explicitly permits non-commercial use only; redistribution and commercial use are prohibited.

### IP-Adapter-FaceID — face-ID conditioning (NON-COMMERCIAL — flagged) · `avoid` · primary-source-confirmed
**IP-Adapter-FaceID provides strong face-identity conditioning via InsightFace buffalo_l embeddings but is restricted to non-commercial research use because its face encoder (InsightFace pretrained weights) is NC-only.**
IP-Adapter-FaceID extracts a 512-dim ArcFace embedding from InsightFace's buffalo_l model and injects it as an additional conditioning signal alongside the standard ControlNet path. Identity fidelity is substantially stronger than base IP-Adapter. However, the model card explicitly states 'released exclusively for research purposes and is not intended for commercial use' — directly because InsightFace pretrained weights are NC-only. Using this on a commercial Steam title is a license violation.
- **For the pipeline:** DO NOT use IP-Adapter-FaceID on the commercial Steam pipeline without first obtaining a commercial InsightFace license (contact recognition-oss-pack@insightface.ai). Fallback: use IP-Adapter base + differential-denoise mask, or PuLID-Flux with FaceNet backend.
- **Engine:** comfyui · **Applies to:** identity · **Base:** SDXL · **Kind:** model
- **VRAM:** 16–24
- **Output license:** commercial **no** (license: Non-commercial research only (InsightFace buffalo_l pretrained weights)) — Model card (h94/IP-Adapter-FaceID) explicitly: 'released exclusively for research purposes and is not intended for commercial use.' Root cause: InsightFace pretrained models are available for non-commercial research purposes only per InsightFace's own policy. InsightFace does offer commercial licensing (contact recognition-oss-pack@insightface.ai) but it is not bundled with these weights. Commercial fallback: IP-Adapter base (Apache) + masked-face-differential-denoise, or PuLID-Flux with FaceNet backend (MIT).
- **Fit:** rig 4/5 · studio 0/5
- **Best for:** identity-lock (-, fit -) ; face-id-conditioning (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [h94/IP-Adapter-FaceID — Hugging Face model card](https://huggingface.co/h94/IP-Adapter-FaceID) (Hu et al. (Tencent AI Lab), 2024) — States explicitly: 'IP-Adapter-FaceID models are released exclusively for research purposes and is not intended for commercial use' — because InsightFace pretrained models are NC-only. ; [InsightFace — pre-trained model license policy](https://github.com/deepinsight/insightface/issues/2022) (InsightFace / deepinsight, 2023) — README states pretrained weights 'available for non-commercial research purposes only'; commercial licensing contact is recognition-oss-pack@insightface.ai. ; [ArcFace model weights — InsightFace ArcFace README](https://github.com/deepinsight/insightface/blob/master/recognition/arcface_torch/README.md) (InsightFace / deepinsight, 2023) — Model Zoo section: 'The models are available for non-commercial research purposes only.' — official NC restriction on ArcFace pretrained weights.

### InstantID — zero-shot face-ID generation (NON-COMMERCIAL — flagged) · `avoid` · primary-source-confirmed
**InstantID's code is Apache 2.0 but its required face encoder (InsightFace AntelopeV2) is NC-only, making the full stack non-commercial as shipped. A commercial fallback requires either a paid InsightFace license or replacing the encoder.**
InstantID (InstantX Research) achieves strong zero-shot face-ID via a face embedding (AntelopeV2 / InsightFace) injected through an IdentityNet adapter plus ControlNet-style keypoint conditioning. The code repo is Apache 2.0 for academic and commercial use, but the required checkpoint explicitly states: 'auto-downloading face models from insightface are for non-commercial research purposes only.' The split licensing creates a compliance gap: the code is permissive, the weights are NC. As shipped today this stack is non-commercial.
- **For the pipeline:** Do not use InstantID commercially unless you obtain InsightFace commercial licensing for AntelopeV2 (contact recognition-oss-pack@insightface.ai). If InstantX releases an alternative encoder in future, re-evaluate. Current studio recommendation: use PuLID-Flux with FaceNet backend (MIT, no InsightFace) or IP-Adapter base + masked-face pass.
- **Engine:** comfyui · **Applies to:** identity · **Base:** SDXL · **Kind:** model
- **VRAM:** 16–24
- **Output license:** commercial **no** (license: Code Apache 2.0; AntelopeV2 face encoder weights: NC research only) — InstantX README: 'both manual-downloading and auto-downloading face models from insightface are for non-commercial research purposes only according to their license.' Code is Apache 2.0 but the face encoder (AntelopeV2 from InsightFace) blocks commercial use. Commercial path: obtain InsightFace commercial license for AntelopeV2, or replace encoder with a commercially-licensed embedding (FaceNet, DINOv2, SigLIP).
- **Fit:** rig 4/5 · studio 0/5
- **Best for:** identity-lock (-, fit -) ; face-id-conditioning (-, fit -) ; zero-shot (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [InstantX/InstantID — GitHub repository](https://github.com/instantX-research/InstantID) (Wang et al. (InstantX Research), 2024) — README states explicitly: 'both manual-downloading and auto-downloading face models from insightface are for non-commercial research purposes only according to their license.' Code is Apache 2.0 but face encoder is NC-only. ; [InstantX/InstantID — HF discussion #2: non-commercial note](https://huggingface.co/InstantX/InstantID/discussions/2) (InstantX / community, 2024) — Community flag: 'Unfortunately, this is non commercial usage only and cannot be Apache 2.0 if it is using Insight Face' — confirms the split-license gap between code (Apache) and encoder weights (NC).

### PuLID-Flux face-ID conditioning — NON-commercial (FLUX-based; avoid for shipping) · `avoid` · community-reported-with-primary-source
**PuLID-Flux exists (arXiv:2404.16022 + the ComfyUI_PuLID_Flux plugin) but it runs on FLUX.1-dev (non-commercial) and the cross-family jury could not confirm a commercial 'FaceNet backend' variant — so it is NOT a commercial face-ID path for the studio.**
PuLID (Pure and Lightning ID customization, ByteDance / ToTheBeginning, arXiv 2404.16022) inserts an ID embedding into the sampling process via contrastive alignment loss, preserving identity without fine-tuning the base model. The original implementation used InsightFace; the PuLID-Flux II plugin (ComfyUI_PuLID_Flux_ll and related) explicitly supports FaceNet as an alternative face analysis backend — 'no ArcFace licensing restrictions, FaceNet is freely available for commercial use.' Code is Apache 2.0 / MIT. The FaceNet-backend variant is the commercial-safe choice for the studio.
- **For the pipeline:** Use PuLID-Flux with the FaceNet backend as the identity-conditioning upgrade over base IP-Adapter when differential-denoise masking alone drifts across character views. Verify the ComfyUI node package being installed uses FaceNet not InsightFace — check the node's requirements.txt before building the pipeline.
- **Engine:** comfyui · **Applies to:** identity · **Base:** FLUX · **Kind:** model
- **VRAM:** 20–32
- **Output license:** commercial **no** (license: Apache 2.0 (PuLID code); FaceNet backend: MIT / Apache; InsightFace backend: NC — AVOID that variant) — PuLID code (github:ToTheBeginning/PuLID) is Apache 2.0. Commercial safety is conditional on which face analysis backend is used: FaceNet = MIT/Apache = commercial-clean; InsightFace = NC = blocked. Studio must pin the FaceNet backend explicitly in the ComfyUI node config. PuLID-Flux II plugin (lldacing/ComfyUI_PuLID_Flux_ll) documents FaceNet as the commercial-safe path.
- **License correction (verifier):** The arXiv 2404.16022 PuLID paper and the lldacing/ComfyUI_PuLID_Flux_ll plugin both exist, but the 'PuLID-Flux II' name and the claim that the plugin ships a 'FaceNet-based face analysis backend' with the quoted 'no ArcFace licensing restrictions' line cannot be sourced. PuLID-Flux's published and community implementations are tied to InsightFace/AntelopeV2 encoders; 'FaceNet' (a 2015 Google face-verification model) is not a documented alternative backend in any PuLID variant. Treat the commercial-safe FaceNet variant as fabricated until proven otherwise — the stack as actually shipped is NC.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| face_analysis_backend |  | ○ |  |
| id_weight |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| If the wrong backend (InsightFace) is inadvertently loaded via auto-install, NC restriction applies — always pin explicitly. |  |  |  |
| FLUX base consumes more VRAM than SDXL; RTX 5090 32 GB handles it but monitor peak allocations. |  |  |  |

- **Best for:** identity-lock (-, fit -) ; commercial (-, fit -) ; face-id-conditioning (-, fit -) ; tuning-free (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=refuted] -> unverified; not-found x1 [license -> commercial_use=no] [no external verdict — not checked]
- **Sources:** [PuLID: Pure and Lightning ID Customization via Contrastive Alignment](https://arxiv.org/abs/2404.16022) (Guo, Zinan; Wu, Yanze; Chen, Zhuowei; Chen, Lang; He, Qian, 2024) — Introduces tuning-free ID customization via contrastive alignment; identity is embedded at inference without model fine-tuning, preserving style/background/composition while injecting the reference face. ; [lldacing/ComfyUI_PuLID_Flux_ll — FaceNet backend documentation](https://github.com/lldacing/ComfyUI_PuLID_Flux_ll) (lldacing (community), 2025) — Plugin supports FaceNet-based face analysis as alternative to InsightFace for commercial applications with 'no ArcFace licensing restrictions.'

