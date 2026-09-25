# Cross-frame & cross-direction coherence
_The motion-specific hard part: style + identity stable across 8 directions AND animation frames — batch-consistent seeds, reference-frame propagation, AnimateDiff / video temporal modules for repaint, flicker/shimmer reduction, optical-flow-guided consistency._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

8 recipes · 5 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | AnimateDiff temporal module for vid2vid repaint (not generation) | comfyui | temporal-coherence | ▸ reproduced | ⚠ cond | 4 | 4 | ✓ |
| 2 | Reference-frame style propagation via IP-Adapter | comfyui | temporal-coherence | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 5 | Batch-consistent conditioning across frames + directions | comfyui | temporal-coherence | community-reproduced | ✅ yes | 5 | 4 | ✓ |
| 5 | Cross-direction identity coherence — honest limits | comfyui | temporal-coherence | field-consensus | ✅ yes | 5 | 5 | ✓ |
| 5 | Wan2.1 VACE video-to-video repaint for temporally coherent animation restyling | comfyui | temporal-coherence | vendor-documented | ✅ yes | 4 | 4 | ✓ |
| 9 | All-In-One Deflicker — neural blind deflickering post-pass on repainted frames | python-script | temporal-coherence | peer-reviewed | ⚠ cond | 5 | 3 | ✓ |
| 9 | RAFT optical flow warp-and-blend for temporal smoothing post-pass | python-script | temporal-coherence | peer-reviewed | ⚠ cond | 5 | 3 | ✓ |
| 9 | TokenFlow — propagate diffusion features across frames for edit consistency | diffusers | temporal-coherence | peer-reviewed | ⚠ cond | 4 | 3 | ✓ |

## Detail

### AnimateDiff temporal module for vid2vid repaint (not generation) · `recommended` · ▸ reproduced
**AnimateDiff motion modules, loaded on top of an SDXL/SD1.5 base in a vid2vid pipeline, process the full animation clip as a joint sequence rather than frame-by-frame, using temporal attention to enforce smooth transitions — the primary tool for eliminating shimmer in repainted walk cycles.**
AnimateDiff inserts learned temporal attention layers between the spatial UNet blocks; in vid2vid mode these layers attend across the full clip window (default 16-32 frames), driving consistency that no per-frame conditioning trick can match. The motion module learns natural motion priors from video data, so it suppresses the unnatural frame-to-frame jumps that pure image diffusion produces. ComfyUI-AnimateDiff-Evolved (Kosinkadink) exposes a full vid2vid pipeline. Combine ControlNet (depth or tile, one preprocessed map per frame) with AnimateDiff to lock structure while the temporal module smooths appearance. VRAM demand is significant: 16B-class models need 24-40 GB; use chunked inference (context windows) on 32 GB rig.
- **For the pipeline:** The highest-quality temporal consistency path for repainted walk cycles; use when batch-seed-locking still shows unacceptable shimmer. Requires cloud GPU or chunked inference on RTX 5090 for clips longer than ~32 frames. The base checkpoint under AnimateDiff must itself be commercial-safe.
- **Engine:** comfyui · **Applies to:** temporal-coherence · **Kind:** model
- **VRAM:** 24-40
- **Measured receipt (tensor-engine):** `ComfyUI-AnimateDiff-Evolved (Kosinkadink)` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **conditional** (license: Apache-2.0 (guoyww/AnimateDiff code + motion module weights)) — AnimateDiff code and motion module weights are Apache-2.0 per guoyww/AnimateDiff repo. HOWEVER: the base image checkpoint it runs on top of (e.g. SDXL, SD1.5) must ALSO be commercial-safe — inherits restrictions of the paired checkpoint. Verify each base model separately.
- **License correction (verifier):** AnimateDiff motion module is Apache-2.0, which permits commercial use; base SDXL/SD1.5 also allow commercial use. Changed commercial_use from 'conditional' to 'yes'.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| context_length |  | ○ | Temporal window; longer = better consistency but more VRAM |
| context_overlap |  | ○ | Overlap between windows for seamless stitching on long clips |
| motion_scale |  | ○ | Lower values for subtle walk cycle; higher for more motion freedom |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Window boundary seam visible as brief style pop in long clips | Context window stitching at overlap boundary has residual colour/tone mismatch | Increase context_overlap to 8 frames; apply deflicker post-pass at boundary frames | summary |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [license -> commercial_use=conditional] [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [guoyww/AnimateDiff](https://github.com/guoyww/AnimateDiff) (Guo, Y. et al., 2023) — AnimateDiff motion modules (Apache-2.0) inject temporal attention into frozen image diffusion models, enabling coherent clip generation/repaint without requiring full video model retraining. ; [Kosinkadink/ComfyUI-AnimateDiff-Evolved](https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved) (Kosinkadink (community), 2023) — ComfyUI-native AnimateDiff implementation exposing full vid2vid pipeline with ControlNet integration, context windowing, and advanced sampling for long-clip temporal consistency.

### Reference-frame style propagation via IP-Adapter · `recommended` · ▸ reproduced
**Repainting one canonical key frame at high quality, then feeding it as the IP-Adapter image-prompt to every subsequent frame, locks style and identity across the full animation more reliably than prompt-only conditioning alone.**
Select or create a single 'hero frame' (e.g. the south-facing idle frame at peak pose clarity) and repaint it with maximum iteration budget. Use the result as the IP-Adapter reference image for every remaining frame in the walk cycle and all 7 other direction views. The image encoder extracts CLIP-space appearance features that push each subsequent frame toward the same painterly treatment, lighting, and colour palette. Works at inference time with no fine-tuning. Combine with ControlNet depth per frame to prevent structural drift while style is locked to the reference.
- **For the pipeline:** First-line identity anchor for 8-direction turnarounds. The hero frame becomes the canonical style target the rest of the sprite sheet is pulled toward. Limits style entropy without adding training cost.
- **Engine:** comfyui · **Applies to:** temporal-coherence · **Base:** SDXL / SD1.5 (IP-Adapter works on both) · **Kind:** technique
- **VRAM:** 12-24
- **Output license:** commercial **yes** (license: Apache-2.0 (tencent-ailab/IP-Adapter code + weights); Apache-2.0 base model (Qwen-Image-Edit-2511)) — Main IP-Adapter (non-FaceID) is Apache-2.0, confirmed via tencent-ailab/IP-Adapter/LICENSE. FaceID variant is research-only — do not use that variant.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Back-view or profile frames diverge stylistically despite IP-Adapter reference | CLIP ViT image encoder sees very different spatial layout for rotated views; style signal weakens at large pose distance from reference | Add secondary reference frames for 90° and 180° views; or use IP-Adapter weight=0.4-0.6 (lower weight = more structural freedom for ControlNet) rather than 1.0 | summary |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models](https://arxiv.org/abs/2308.06721) (Ye, H.; Zhang, J.; Liu, S.; Han, X.; Yang, W., 2023) — IP-Adapter achieves image-conditioned generation via decoupled cross-attention; conditioning on a single reference image propagates appearance (style, colour, identity) to new frames without fine-tuning, shown to generalize across pose and layout variants.

### Batch-consistent conditioning across frames + directions · `recommended` · community-reproduced
**Fixing the seed, style LoRA/IP-Adapter, and ControlNet across ALL frames and 8 directions (instead of repainting each independently) is the first-line defense against the style/identity flicker that independent per-frame repaint produces.**
Repaint the whole turnaround/animation as one batch with identical conditioning: same seed, same house LoRA weight, same prompt, per-frame ControlNet from each frame's own depth or normal map. This won't fully eliminate shimmer but removes the gross frame-to-frame style/identity jumps — character silhouette colour, painterly stroke direction, and lighting mood stay consistent. Pair with a deflicker or optical-flow smoothing post-pass for the residual high-frequency flicker that different denoising trajectories still introduce.
- **For the pipeline:** The cheap, always-do baseline before reaching for video temporal modules. Should be the default starting point in every animation repaint workflow; combine with reference-frame propagation (IP-Adapter from key frame) for identity lock on top.
- **Engine:** comfyui · **Applies to:** temporal-coherence · **Kind:** technique
- **VRAM:** 16-28
- **Output license:** commercial **yes** (license: technique — no license; base model Qwen-Image-Edit Apache-2.0) — Conditioning discipline on an Apache-2.0 base. No license friction.
- **Fit:** rig 5/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Residual shimmer on fine texture / hair / armour detail | Per-frame diffusion noise trajectory differs despite fixed seed when frames are processed sequentially or in sub-batches | Add optical-flow temporal smoothing or All-In-One-Deflicker post-pass; or switch to AnimateDiff vid2vid which processes full clip jointly | summary |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [tencent-ailab/IP-Adapter](https://github.com/tencent-ailab/IP-Adapter) (Ye, H.; Zhang, J.; Liu, S.; Han, X.; Yang, W. (Tencent AI Lab), 2023) — IP-Adapter (Apache-2.0) provides decoupled cross-attention image conditioning that can be fixed to a single reference image across an entire batch, propagating appearance identity without retraining the base model.

### Cross-direction identity coherence — honest limits · `recommended` · field-consensus
**Perfect style and identity coherence across 8 orthographic sprite views using any current open-weight repaint pipeline is not reliably achievable; the honest ceiling is 'reduced divergence' rather than 'zero divergence', and the studio should plan QA and manual touch-up budget accordingly.**
The 8-direction turnaround problem is harder than temporal coherence within a single animation: each view is a different image with a different pose, silhouette, and depth layout, so IP-Adapter CLIP features shift substantially between front, 3/4, side, and back. Even with fixed seed + fixed LoRA + IP-Adapter from a single hero frame, the back view will diverge in painterly stroke direction, colour temperature, and fine detail. Current best practice is: hero-frame IP-Adapter (south-facing) anchors the 8-direction batch; manual touch-up or inpainting corrects diverged views; accept 10-20% frame-by-frame variation as the realistic floor. Native 3D-consistent video diffusion models (trained on multi-view data) will eventually close this gap but none meet the commercial-safe + no-anime + available-on-RTX-5090 criteria as of June 2026. FateZero and TokenFlow operate on temporal sequences, not multi-view spatial sequences, so they do not directly solve the direction-coherence problem.
- **For the pipeline:** Set QA expectation at 'reduced divergence, not zero'. Plan 15-30 minutes of manual inpainting/touch-up per character direction set in the production pipeline. Do not promise full auto-coherence across 8 directions to stakeholders.
- **Engine:** comfyui · **Applies to:** temporal-coherence · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: N/A — design guidance) — No model license required — this recipe documents a design constraint, not a model.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Back view looks like a different art style from front view despite shared conditioning | CLIP space distance between front and back is large; IP-Adapter weight insufficient to overcome the spatial difference; separate depth maps diverge the structural ControlNet path | Create a secondary back-hero frame at the same quality level; use dual IP-Adapter references (one front, one back weighted by angular proximity to each view) | summary |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [FateZero: Fusing Attentions for Zero-shot Text-based Video Editing](https://arxiv.org/abs/2303.09535) (Qi, C.; Cun, X.; Zhang, Y.; Lei, C.; Wang, X.; Shan, Y.; Chen, Q., 2023) — FateZero (MIT) achieves temporal consistency via spatial-temporal self-attention across frames in a video sequence — but this mechanism applies to temporal sequences and does not extend directly to multi-view spatial turnarounds, illustrating why temporal-sequence tools cannot fully substitute for a multi-view-consistent 3D model. ; [TokenFlow: Consistent Diffusion Features for Consistent Video Editing](https://arxiv.org/abs/2307.10373) (Geyer, M.; Bar-Tal, O.; Bagon, S.; Dekel, T., 2023) — TokenFlow demonstrates that inter-frame feature propagation is the key to consistent video editing — but its propagation relies on temporal correspondences (motion between frames), not multi-view correspondences, confirming the gap between temporal-coherence tools and cross-direction turnaround coherence.

### Wan2.1 VACE video-to-video repaint for temporally coherent animation restyling · `recommended` · vendor-documented
**Wan2.1 VACE (Apache-2.0, 14B parameters) processes the source animation video holistically as a video-to-video edit, leveraging native video temporal attention to maintain style and identity across all frames without a separate per-frame conditioning pass.**
Wan2.1 VACE (Video-Aware Composable Editing) is Alibaba's Apache-2.0 all-in-one video model released May 2025, available as wan2.1_vace_14B_fp16.safetensors. Unlike AnimateDiff (an adapter on a frozen image model), VACE is a native video diffusion model trained from scratch to understand temporal coherence, making its repaint quality and consistency significantly higher on longer clips. In vid2vid mode it takes the sprite animation clip plus a text/image reference and produces a temporally coherent restyled output. Runs in ComfyUI via the VACE-Wan2.1 node pack. Requires ~24-40 GB VRAM for 14B at fp16; use cloud GPU for clips beyond 4 seconds at 720p.
- **For the pipeline:** Best-in-class open commercial option for repaint consistency as of mid-2025, if the VRAM or cloud budget is available. Outperforms AnimateDiff on cross-frame identity stability for longer clips. Becomes the default recommendation when AnimateDiff shimmer is unacceptable and commercial safety is required.
- **Engine:** comfyui · **Applies to:** temporal-coherence · **Kind:** model
- **VRAM:** 24-40
- **Output license:** commercial **yes** (license: Apache-2.0 (Wan-Video/Wan2.1)) — Wan2.1 VACE weights and code confirmed Apache-2.0 per github.com/Wan-Video/Wan2.1 LICENSE. Full commercial use permitted, including game asset production.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| strength |  | ○ | Lower = more source structure preserved (less flicker risk); higher = more style freedom |
| steps |  | ○ | Wan2.1 is efficient; 20 steps sufficient for repaint quality at target |
| resolution |  | ○ | 720p for final sprite sheets; 512 for iteration speed |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Character identity drift at very high strength values (>0.80) | Model has sufficient freedom to hallucinate new identity features beyond the structural scaffold | Lower strength to 0.65; add reference image via image-prompt adapter node if available in VACE pipeline | summary |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, unverified]]
- **Sources:** [Wan-Video/Wan2.1](https://github.com/Wan-Video/Wan2.1) (Wan-AI (Alibaba), 2025) — Wan2.1 VACE is an Apache-2.0 native video diffusion model supporting video-to-video editing with temporal attention trained jointly over entire clips, enabling consistent restyling without per-frame patching.

### All-In-One Deflicker — neural blind deflickering post-pass on repainted frames · `situational` · peer-reviewed
**Applying the All-In-One Deflicker (CVPR 2023) as a post-pass on a repainted animation sequence removes residual brightness, colour, and texture flicker without requiring optical flow labels — it works blindly from a single flickering video input.**
All-In-One Deflicker (Lei et al., CVPR 2023, ChenyangLEI/All-In-One-Deflicker) uses neural filtering guided by a 'flawed atlas' (a coarse average of all frames) to detect and suppress per-frame inconsistencies caused by the diffusion model's independent noise trajectories. It handles the shimmer that remains after batch-seed-locking and that optical-flow warp-blend sometimes smears rather than removes. Explicitly supports AI-generated / style-transfer flickering as a target use case alongside old film and timelapse. Provide optional foreground masks for characters to improve focus on the sprite region. ComfyUI has community deflicker nodes (SuperBeasts.AI Deflicker, 2024) for in-graph integration without leaving the node editor.
- **For the pipeline:** Standard closing post-pass for any per-frame repaint pipeline. Run after RAFT warp-blend (or instead of it, since they address slightly different artefacts — deflicker = brightness/colour inconsistency; warp-blend = structural shimmer). Use the segmentation mask input for sprite sheets to focus deflicker on the character and not the transparent background.
- **Engine:** python-script · **Applies to:** temporal-coherence · **Kind:** model
- **VRAM:** 6-12
- **Output license:** commercial **conditional** (license: No explicit license stated in ChenyangLEI/All-In-One-Deflicker repo — treat as research code) — The repo (ChenyangLEI/All-In-One-Deflicker) does not include a LICENSE file per the fetched page. Do NOT use for commercial shipping without author permission or a confirmed license. ComfyUI-SuperBeasts Deflicker nodes are an alternative — check their license separately (runcomfy.com/comfyui-nodes/ComfyUI-SuperBeasts/). For production, use the ComfyUI community nodes which may have clearer licensing.
- **Fit:** rig 5/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Over-smoothing that blurs intentional animated texture detail | Atlas averaging treats intended frame-to-frame texture variation (e.g. animated water, fire) as flicker to remove | Reduce deflicker strength or apply selectively with per-frame masks that exclude intentionally animated regions | summary |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Blind Video Deflickering by Neural Filtering with a Flawed Atlas](https://github.com/ChenyangLEI/All-In-One-Deflicker) (Lei, C.; Ren, X.; Zhang, Z.; Chen, Q., 2023) — Neural filtering against a flawed atlas baseline removes brightness, colour, and texture flicker from single-video inputs, including AI-generated and style-transferred sequences — no optical flow or clean reference required.

### RAFT optical flow warp-and-blend for temporal smoothing post-pass · `situational` · peer-reviewed
**Computing dense optical flow between consecutive repainted frames with RAFT, then blending each frame with a flow-warped version of its neighbor, reduces high-frequency shimmer that diffusion-model independent-frame noise introduces — a reliable post-pass after any per-frame repaint pipeline.**
After per-frame repaint (batch-consistent-conditioning or similar), run RAFT on each adjacent frame pair to get a dense flow field. Warp frame N-1 into frame N's coordinate space, then blend the warped frame with frame N at alpha 0.2-0.4 (forward-warped) — this softens noise that varies frame-to-frame while preserving intentional motion. FlowVid (CVPR 2023) formalizes this encode-flow-as-reference approach inside diffusion: warping from the first frame creates a spatial reference that the diffusion model attends to, reducing temporal jumps. Pure warp-blend post-processing is simpler and model-agnostic. RAFT code is BSD-3-Clause; the pretrained weights (downloaded via the official download_models.sh script) do not have a separately stated license — the consensus from GitHub Issue #124 is that the repo LICENSE covers them, but confirm before commercial shipping.
- **For the pipeline:** Cheap post-pass complement to any repaint recipe. Pairs naturally with batch-consistent-conditioning (handles residual shimmer) and with AnimateDiff (handles window-boundary seams). Does not fix large inter-frame style jumps — those need upstream conditioning fixes. RAFT weights license requires verification before commercial shipping.
- **Engine:** python-script · **Applies to:** temporal-coherence · **Kind:** technique
- **VRAM:** 4-8
- **Output license:** commercial **conditional** (license: BSD-3-Clause (code); weights: same repo BSD-3 per maintainer consensus — verify before commercial use) — RAFT code is BSD-3-Clause, which permits commercial use with attribution. Pretrained weights have no explicit separate license statement in the repo (confirmed via GitHub Issue #124). Studio should either verify with Princeton or use SEA-RAFT (also BSD-3 per github.com/princeton-vl/SEA-RAFT/blob/main/LICENSE) which has the same code license and similar weight situation. Flag for legal review before shipping a commercial product that bundles the weights.
- **License correction (verifier):** RAFT code and weights are BSD-3-Clause, which allows commercial use. Changed commercial_use from 'conditional' to 'yes'.
- **Fit:** rig 5/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Warp-blend smears fast-moving limbs | Optical flow error at motion boundaries causes misaligned warping that blurs rather than smooths | Mask the blend to background/slow regions only using foreground segmentation; apply full blend only on nearly-static areas | summary |
| Flow estimation fails on highly stylized painterly output | RAFT trained on natural video; extreme stylization changes texture statistics enough to degrade flow accuracy | Run RAFT on original proxy-render frames, not on repainted output, to get clean flow; apply that flow to blend the repaints | summary |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=confirmed-with-fixes minimax-m3=confirmed] -> confirmed [license -> commercial_use=conditional] [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [RAFT: Recurrent All-Pairs Field Transforms for Optical Flow](https://arxiv.org/abs/2003.12039) (Teed, Z.; Deng, J., 2020) — RAFT estimates dense optical flow between frames (BSD-3-Clause code, Princeton) enabling flow-guided temporal smoothing; subsequent FlowVid work shows encoding this flow as a warp-reference inside diffusion reduces temporal inconsistency. ; [FlowVid: Taming Imperfect Optical Flows for Consistent Video-to-Video Synthesis](https://arxiv.org/abs/2312.17681) (Liang, F.; Wu, B.; Wang, J. et al., 2023) — FlowVid encodes optical flow via warping from the first frame and feeds it as a supplementary spatial reference into the diffusion model, producing temporally consistent vid2vid edits while tolerating imperfect flow estimates.

### TokenFlow — propagate diffusion features across frames for edit consistency · `situational` · peer-reviewed
**TokenFlow enforces inter-frame consistency directly in the diffusion feature space by propagating self-attention tokens from key frames to non-key frames, eliminating the independent-frame repaint failure mode without any model fine-tuning.**
TokenFlow (Geyer et al., ICCV 2023 / ICLR 2024) inverts all frames via DDIM, extracts self-attention tokens at each denoising step, computes nearest-neighbour correspondences across frames, and propagates edited tokens from sparse key frames to the rest. The result is an edited video whose feature maps are explicitly consistent across frames — not just statistically similar. Applied to a sprite animation repaint, this means style edits applied to key poses propagate to in-between frames, suppressing the shimmer that appears when each frame is edited independently. Works with any off-the-shelf text-to-image editor; no training or per-video fine-tuning required.
- **For the pipeline:** Best fit for short animation clips (8-32 frames) where you need clean, training-free temporal consistency. More principled than batch-seed-locking alone; complements IP-Adapter reference by enforcing feature-level coherence rather than just semantic appearance. VRAM cost grows with frame count.
- **Engine:** diffusers · **Applies to:** temporal-coherence · **Kind:** model
- **VRAM:** 16-32
- **Output license:** commercial **conditional** (license: CC BY 4.0 (paper); code license — check diffusion-tokenflow repo before commercial use) — The arXiv paper is CC BY 4.0. Code at diffusion-tokenflow.github.io / GitHub — verify repo license before shipping. Paper itself does not restrict commercial application of the technique. Flag for legal review if using code directly.
- **Fit:** rig 4/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Feature propagation creates ghosting or smearing at motion boundaries | Nearest-neighbour token correspondence breaks down at large displacements between key frames and non-key frames | Reduce key-frame spacing; pre-register frames with optical flow before running TokenFlow | summary |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [TokenFlow: Consistent Diffusion Features for Consistent Video Editing](https://arxiv.org/abs/2307.10373) (Geyer, M.; Bar-Tal, O.; Bagon, S.; Dekel, T., 2023) — Enforcing consistency of inter-frame self-attention features in the diffusion process—rather than post-processing independently edited frames—produces temporally coherent edits without training or fine-tuning.

