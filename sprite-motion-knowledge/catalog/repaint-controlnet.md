# Structure-preserving repaint (ControlNet)
_Repaint a 3D mesh/proxy render to the painterly house style while HOLDING structure: ControlNet depth/lineart/canny/tile/softedge stacks on Qwen-Image-Edit-2511; denoise + control-strength schedules. The mesh-render -> painterly-skin core that closes the §D style gap._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

14 recipes · 5 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 4 | Depth-from-mesh + Qwen-Image-Edit-2511 + InstantX ControlNet-Union repaint | comfyui | repaint | · single-run | ✅ yes | 5 | 5 | · |
| 6 | Depth + Lineart/AnyLine ControlNet stack for 3D-render-to-painterly repaint | comfyui | repaint | · community | ⚠ cond | 5 | 4 | ✓ |
| 6 | Render depth + normal passes directly from the TRELLIS.2 mesh (Blender Cycles) for ControlNet input | custom | repaint | · community | ✅ yes | 5 | 5 | ✓ |
| 6 | Structure-from-ControlNet, style-from-LoRA decomposition principle | n/a | repaint | · community | ✅ yes | 5 | 5 | ✓ |
| 6 | Tile ControlNet + Ultimate SD Upscale for painterly detail recovery after repaint | comfyui | repaint | · community | ⚠ cond | 5 | 4 | ✓ |
| 6 | xinsir controlnet-union-sdxl-1.0 ProMax multi-condition repaint (SDXL base) | comfyui | repaint | · single-run | ✅ yes | 5 | 4 | ✓ |
| 8 | SoftEdge/HED ControlNet for painterly boundary-aware repaint | comfyui | repaint | · single-run | ⚠ cond | 5 | 4 | ✓ |
| 9 | ControlNet spatial conditioning literature (Zhang et al. 2023) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | Diffusers AnimateDiff API — temporal pipelines | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | InstantX Qwen-Image-ControlNet-Union peer | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | Qwen-Image-Edit-2511 repaint peer | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | control_v11p_sd15_openpose — OpenPose ControlNet v1.1 | comfy | all-motion | docs | check | 4 | 4 | · |
| 9 | lllyasviel ControlNet v1.1 depth + openpose peers | comfy | all-motion | docs | check | 4 | 4 | · |
| 10 | Normal BAE ControlNet from mesh — surface orientation lock during repaint | comfyui | repaint | · community | ⚠ cond | 5 | 3 | ✓ |

## Detail

### Depth-from-mesh + Qwen-Image-Edit-2511 + InstantX ControlNet-Union repaint · `recommended` · · single-run
**Rendering a depth pass directly from the TRELLIS.2 mesh and feeding it into Qwen-Image-Edit-2511 via InstantX Qwen-Image-ControlNet-Union repaints the 3D render to painterly house style while holding silhouette, pose, and rigid weapon position.**
Because you already have the mesh from TRELLIS.2, render a clean depth pass (Blender Cycles, 16-bit PNG, Mist pass normalized) rather than estimating depth post hoc with MiDaS. This ground-truth depth is sharper at object boundaries and locks the weapon's Z-position exactly. Feed the mesh render as img2img input (denoise 0.5-0.65) plus the depth map into Qwen-Image-Edit-2511 with InstantX Qwen-Image-ControlNet-Union (canny+depth modes, control weight 0.6-0.8). Drive the style with the sfhd_style_v1 house LoRA and a painterly prompt. Structure comes from ControlNet; style comes from the LoRA — the decomposition that prevents drift.
- **For the pipeline:** This is the primary §D repaint pass for the captain prototype. Depth-from-mesh is cleaner than any estimated depth and hard-locks the rigid weapon across all 8 directions; switching to estimated depth introduces weapon-position drift.
- **Engine:** comfyui · **Applies to:** repaint · **Base:** Qwen-Image · **Kind:** workflow
- **VRAM:** 20-28
- **Base model (model-knowledge):** `Qwen/Qwen-Image-Edit-2511`
- **Output license:** commercial **yes** (license: Qwen-Image-Edit-2511: Apache-2.0; InstantX Qwen-Image-ControlNet-Union: Apache-2.0) — Both Apache-2.0. Outputs are studio-owned. House LoRA studio-owned on commercial base. No NC weights in this path.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| img2img_denoise |  | ○ | Below 0.50 preserves 3D shading artifacts; above 0.65 loses weapon shape |
| controlnet_weight |  | ○ | Depth mode; reduce to 0.5 if painterly style is being over-constrained |
| lora_weight |  | ○ | sfhd_style_v1 house LoRA |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Denoise > 0.70 with weak ControlNet weight causes weapon drift — keep depth weight >= 0.6 |  |  |  |
| Qwen-Image-ControlNet-Union supports canny/softedge/depth/pose but NOT tile; use separate tile pass for detail recovery |  |  |  |

- **Best for:** mesh-to-painterly repaint (-, fit -) ; weapon rigidity (-, fit -) ; pose lock (-, fit -) ; 8-direction consistency (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=unverified] -> unverified [only 1 of 3 juror(s) confirmed [confirmed, unverified]]
- **Sources:** [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) (Qwen Team, 2025) — Apache-2.0 instruction-following image editor with improved character consistency and multi-image input; commercial use permitted. ; [InstantX/Qwen-Image-ControlNet-Union](https://huggingface.co/InstantX/Qwen-Image-ControlNet-Union) (InstantX Team, 2025) — Apache-2.0 unified ControlNet for Qwen-Image supporting canny, soft edge, depth, and pose conditioning; trained 50K steps on 10M images at 1328x1328. ; [Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) (Lvmin Zhang, Anyi Rao, Maneesh Agrawala, 2023) — ControlNet uses zero-initialized convolutions to add spatial conditioning (depth, edges, pose) to pretrained diffusion models without degrading base model quality.

### Depth + Lineart/AnyLine ControlNet stack for 3D-render-to-painterly repaint · `recommended` · · community
**Stacking a mesh-rendered depth map with an AnyLine/lineart pass from the same mesh render as dual ControlNet inputs gives the strongest structure lock for mesh-render-to-painterly repaint: depth governs large-scale silhouette + weapon position, lineart governs fine edge sharpness.**
Render two passes from the TRELLIS.2 mesh in Blender: a normalized depth pass (16-bit PNG, Mist pass) and the mesh render itself passed through AnyLine or the ControlNet lineart preprocessor to extract a clean edge map. Use both simultaneously as ControlNet inputs with separate weights (depth: 0.5-0.7, lineart: 0.4-0.6). The depth pass controls silhouette and spatial layout; the lineart pass locks fine weapon and costume edges. Together they prevent the 3D-to-painterly transition from softening or relocating rigid-body parts. Run with the sfhd_style_v1 LoRA for style injection.
- **For the pipeline:** The two-pass stack is the workhorse technique for the §D gap: depth alone can miss fine edges; lineart alone can lose spatial depth. Stacking both is more stable than using either alone. Render both passes from the mesh — they are zero-cost once the mesh exists.
- **Engine:** comfyui · **Applies to:** repaint · **Kind:** technique
- **VRAM:** 12-24
- **Output license:** commercial **conditional** (license: ComfyUI ControlNet auxiliary preprocessors: Apache-2.0 (Fannovel16/comfyui_controlnet_aux); ControlNet v1.1 models: CreativeML OpenRAIL-M) — OpenRAIL-M permits commercial use with responsible-use clauses. Apache-2.0 preprocessors are permissive. Verify your diffusion base model's license separately.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| depth_controlnet_weight |  | ○ |  |
| lineart_controlnet_weight |  | ○ |  |
| img2img_denoise |  | ○ |  |
| lineart_preprocessor |  | ○ | AnyLine (TheMistoAI/ComfyUI-Anyline) recommended for mesh renders with hard edges |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| If both weights are too high (>0.8), the repaint looks like a filtered 3D render rather than painterly — reduce lineart weight first |  |  |  |
| Anime lineart preprocessor variant must not be selected (no-anime rule) |  |  |  |

- **Best for:** weapon rigidity (-, fit -) ; dual-condition structure lock (-, fit -) ; edge fidelity (-, fit -) ; depth-plus-lineart stack (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [ComfyUI ControlNet Auxiliary Preprocessors](https://github.com/Fannovel16/comfyui_controlnet_aux) (Fannovel16, 2024) — Apache-2.0 ComfyUI node set providing depth (MiDaS, Depth Anything V2), lineart (standard, realistic, AnyLine), normal (BAE, DSINE), softedge (HED, PiDiNet, TEED), and canny preprocessors. ; [ComfyUI-Anyline (AnyLine preprocessor)](https://github.com/TheMistoAI/ComfyUI-Anyline) (TheMistoAI, 2024) — AnyLine is a fast, accurate line detection preprocessor based on TEED (arXiv:2308.06468) that extracts object edges, fine image details, and text content; integrated into comfyui_controlnet_aux. ; [Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) (Lvmin Zhang, Anyi Rao, Maneesh Agrawala, 2023) — ControlNet adds spatial conditioning to pretrained diffusion models; multi-condition stacking is supported by running parallel ControlNet branches.

### Render depth + normal passes directly from the TRELLIS.2 mesh (Blender Cycles) for ControlNet input · `recommended` · · community
**Exporting a normalized depth map and world-space normal map as 16-bit PNG directly from Blender Cycles (via View Layer passes + compositor) produces cleaner ControlNet conditioning than any post-hoc monocular estimator (MiDaS, Depth Anything) because the geometry is known exactly.**
In Blender's View Layer Properties, enable the Depth (Mist) pass and the Normal pass. In the Compositor, use a Render Layers node, Map Range/Normalize the depth to 0-1, and output as a 16-bit PNG. The normal pass (blue=front, red=left, green=top, matching ControlNet normalbae convention) can be exported directly. These passes are zero-cost given the existing TRELLIS.2 mesh and lock the weapon's position to sub-pixel accuracy — MiDaS-estimated depth on a 3D render will have estimation error at the weapon boundary. Use the depth PNG as input to ControlNet-depth and the normal PNG as input to ControlNet-normalbae.
- **For the pipeline:** This is the upstream step that makes the depth+lineart stack recipe valid. The mesh already exists — never estimate what you can render. This is the single most important best practice for the §D gap.
- **Engine:** custom · **Applies to:** repaint · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: Blender: GPL-2.0+ (output images are unencumbered studio assets)) — Blender's GPL applies to the software, not to rendered image outputs. Depth/normal pass images are the studio's assets.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| depth_output_bit_depth |  | ○ | 32-bit EXR also works but requires conversion; 8-bit loses precision |
| normal_convention |  | ○ | Blender world-space normal matches ControlNet normalbae (blue=front, red=left, green=top — NYU-V2 protocol) |
| mist_pass_normalize |  | ○ | Map Range node: clip and normalize depth to 0-1 before export |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Raw Mist pass values are in meters and appear all-white — must normalize with Map Range node before export |  |  |  |
| Invert colors (CTRL-I in Krita) if ControlNet expects near=white rather than near=dark |  |  |  |

- **Best for:** ground-truth depth for ControlNet (-, fit -) ; weapon-position lock (-, fit -) ; normal pass for surface shading (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [How to Render Blender 3D Models in Stable Diffusion](https://sandner.art/how-to-render-blender-3d-models-in-stable-diffusion/) (Daniel Sandner, 2023) — Export Blender depth (Mist) as 16-bit PNG with color inversion; ControlNet depth conditioning weight tested 0.45-1.0 with guidance start/end timing; gives 'creative results' matching 3D layout to 2D painterly output. ; [Blender Manual — Render Layers Passes](https://docs.blender.org/manual/en/latest/render/layers/passes.html) (Blender Foundation, 2024) — Z/Depth pass gives distance to nearest visible surface; Normal pass gives world-space surface orientation; both accessible via Render Layers node in Compositor.

### Structure-from-ControlNet, style-from-LoRA decomposition principle · `recommended` · · community
**Explicitly separating the structural signal (ControlNet handles pose, depth, edges) from the style signal (LoRA + prompt handles painterly house style) is the architectural principle that prevents style drift and structural collapse in mesh-render repaint — each axis has a dedicated mechanism.**
When both structure and style are driven by a single channel (e.g., prompt alone, or img2img alone), they compete: a stronger style prompt softens structure; a stronger denoise loses style. The correct decomposition: ControlNet takes responsibility for structure (depth, lineart, normal from mesh), the house LoRA + prompt takes responsibility for style (sfhd_style_v1, painterly descriptors). The img2img denoise is the mix dial — set it in the range 0.50-0.65 so neither axis dominates. The ControlNet end-step can also be set to 0.5-0.6 so the style has breathing room in the late diffusion steps. This principle is architecture-agnostic and applies to both the Qwen-Image-Edit path and the SDXL path.
- **For the pipeline:** This is the operating principle behind every repaint recipe in this lane. If a repaint attempt is failing (structure lost OR style not matching), the first diagnostic is which axis is broken — then tune the responsible mechanism independently.
- **Engine:** n/a · **Applies to:** repaint · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: n/a) — Architectural principle; no specific weight. Commercial viability depends on weights used in the implementing recipe.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| img2img_denoise |  | ○ | Primary mix dial between structure preservation and style injection |
| controlnet_end_step |  | ○ | Stop ControlNet influence at 50-60% of sampling steps to give style breathing room in late diffusion |
| controlnet_weight_range |  | ○ | Structure axis; reduce if style is being over-constrained |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Driving style through ControlNet (e.g., using a stylized image as ControlNet input) causes the two axes to collapse into one — keep them separate |  |  |  |
| Over-constraining: both high denoise AND high ControlNet weight causes the model to fight itself; tune one axis at a time |  |  |  |

- **Best for:** architectural principle (-, fit -) ; style-structure decomposition (-, fit -) ; drift prevention (-, fit -) ; repaint diagnostics (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [ControlNet SoftEdge — painterly weight settings and structure/style interaction](https://blog.segmind.com/introduction-to-controlnet-softedge/) (Segmind, 2024) — SoftEdge/HED weight 0.3-0.6 for painterly subtlety; img2img denoising 0.35-0.55 for strong structure retention; ControlNet End set to 0.5-0.6 allows style to breathe in late sampling steps. ; [Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) (Lvmin Zhang, Anyi Rao, Maneesh Agrawala, 2023) — ControlNet locks spatial structure (pose, depth, edges) while the pretrained diffusion model's locked weights retain text-driven style — the architecture inherently separates structural and style conditioning.

### Tile ControlNet + Ultimate SD Upscale for painterly detail recovery after repaint · `recommended` · · community
**Tile ControlNet (lllyasviel/control_v11f1e_sd15_tile) used as a second pass after the initial depth+lineart repaint recovers fine painterly detail (brushwork, fabric texture, weapon surface) that mid-denoise img2img softens, without disturbing the structural lock already applied.**
The initial depth+ControlNet repaint at denoise 0.5-0.65 replaces the 3D style but can soften fine detail. A second tile-ControlNet pass at lower denoise (0.2-0.35) over the already-resampled image adds painterly texture and detail without moving large structures. Combined with Ultimate SD Upscale (ssitu/ComfyUI_UltimateSDUpscale, GPL-3.0) in ComfyUI, this also handles upscaling to final sprite resolution in one pass — each tile is independently conditioned so brushwork is consistent. The tile ControlNet ignores global composition and generates new local detail, making it safe to run after the structural pass.
- **For the pipeline:** Schedule as the final polish pass: run after depth+lineart repaint is approved. Keeps sprite resolution at 2x-4x output without re-running the expensive Qwen-Image-Edit pass.
- **Engine:** comfyui · **Applies to:** repaint · **Kind:** technique
- **VRAM:** 8-16
- **Output license:** commercial **conditional** (license: control_v11f1e_sd15_tile: CreativeML OpenRAIL-M; ComfyUI_UltimateSDUpscale: GPL-3.0) — OpenRAIL-M permits commercial use with usage clauses. GPL-3.0 applies to the node code, not to generated images. Verify base diffusion model license.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| tile_denoise |  | ○ | Low enough to not move weapon or silhouette; high enough to add real painterly texture |
| tile_controlnet_weight |  | ○ |  |
| upscale_factor |  | ○ | 4x-UltraSharp upscaler recommended for sprite work |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Tile denoise > 0.45 can create tile-boundary seams — keep it below 0.40 |  |  |  |
| Running tile pass before structural repaint is approved wastes compute — always sequence after depth+lineart pass |  |  |  |

- **Best for:** painterly detail recovery (-, fit -) ; upscale + detail (-, fit -) ; tile-consistent brushwork (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [lllyasviel/control_v11f1e_sd15_tile](https://huggingface.co/lllyasviel/control_v11f1e_sd15_tile) (Lvmin Zhang, 2023) — CreativeML OpenRAIL-M; conditions on tiled image inputs to generate or enhance local detail at target resolution without global composition changes; acts as super-resolution ControlNet for detail-aware img2img. ; [ComfyUI_UltimateSDUpscale](https://github.com/ssitu/ComfyUI_UltimateSDUpscale) (ssitu, 2023) — GPL-3.0 ComfyUI nodes for tile-based img2img diffusion on large images; each tile is independently conditioned, preventing cross-tile misalignment when combined with Tile ControlNet.

### xinsir controlnet-union-sdxl-1.0 ProMax multi-condition repaint (SDXL base) · `runner-up` · · single-run
**xinsir controlnet-union-sdxl-1.0 (Apache-2.0) stacks depth + lineart + canny from the mesh render in a single checkpoint pass, repainting the 3D render to painterly while holding structure — the Apache SDXL alternative to the Qwen path.**
ControlNet++ (xinsir/controlnet-union-sdxl-1.0, Apache-2.0) unifies 10+ conditioning types in one checkpoint with condition fusion learned during training — no hyperparameter juggling between separate ControlNet models. For mesh-render repaint, run depth (from mesh) + lineart (AnyLine from mesh silhouette) + canny simultaneously at SDXL resolution (1024px+). This is the preferred path when the base diffusion model is SDXL rather than Qwen-Image. The ProMax variant (July 2024) adds tile super-resolution editing on top.
- **For the pipeline:** Apache-2.0 runner-up for studios that prefer SDXL as the diffusion backbone. Multi-condition fusion is learned, not manually weighted, reducing per-project tuning. Use alongside sfhd_style_v1 as an SDXL LoRA if that base is trained on SDXL.
- **Engine:** comfyui · **Applies to:** repaint · **Base:** SDXL · **Kind:** technique
- **VRAM:** 12-20
- **Base model (model-knowledge):** `xinsir/controlnet-union-sdxl-1.0`
- **Output license:** commercial **yes** (license: Apache-2.0) — Apache-2.0; ControlNet++ GitHub repo and HuggingFace model card both confirm. Check SDXL base model's license separately.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| conditions_used |  | ○ | All sourced from mesh render or AnyLine preprocessor on mesh render |
| img2img_denoise |  | ○ |  |
| controlnet_weight |  | ○ | Single weight applies to fused condition vector |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Anime lineart conditioning type is present — never select it (studio no-anime rule) |  |  |  |
| Condition fusion is learned for general images; may need weight reduction for painterly sprites to avoid over-sharpening |  |  |  |

- **Best for:** SDXL-path repaint (-, fit -) ; multi-condition stacking (-, fit -) ; no-weight-juggling structure lock (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [xinsir/controlnet-union-sdxl-1.0](https://huggingface.co/xinsir/controlnet-union-sdxl-1.0) (xinsir, 2024) — Apache-2.0 all-in-one SDXL ControlNet supporting 10+ conditions (depth, canny, lineart, normal, tile, scribble, HED, PIDI, TEED, segmentation) with multi-condition fusion learned during training. ; [ControlNetPlus (ControlNet++)](https://github.com/xinsir6/ControlNetPlus) (xinsir6, 2024) — Apache-2.0 repository with inference scripts; ProMax variant released July 2024 adds tile super-resolution, inpainting, and outpainting editing modes.

### SoftEdge/HED ControlNet for painterly boundary-aware repaint · `situational` · · single-run
**SoftEdge/HED ControlNet (lllyasviel/control_v11p_sd15_softedge, CreativeML OpenRAIL-M) conditions on gentle boundary maps — softer than canny — making it ideal for painterly repaint where hard canny edges would fight the brushstroke aesthetic.**
Canny ControlNet enforces hard pixel-accurate edges that conflict with painterly softness. SoftEdge (HED or PIDI preprocessor) produces a boundary map where edges fade at their periphery, matching how painterly linework naturally thickens and fades. For the mesh-render repaint, extract a soft edge map from the mesh render using the PIDI (safe) or HED preprocessor and use it at moderate weight (0.3-0.5) alongside the depth ControlNet. This lets the diffusion model respect major silhouettes while having freedom to render edges in a painterly style. ControlNet v1.1 SoftEdge improved over v1.0 HED by filtering out corrupted greyscale artifacts hidden in the edge map.
- **For the pipeline:** Use softedge INSTEAD of canny when the depth-alone pass produces too clean/hard a silhouette. Stack depth (weight 0.6) + softedge (weight 0.35) for the best painterly-boundary result.
- **Engine:** comfyui · **Applies to:** repaint · **Kind:** technique
- **VRAM:** 8-16
- **Output license:** commercial **conditional** (license: CreativeML OpenRAIL-M) — OpenRAIL-M permits commercial use with responsible-use clauses. Check base diffusion model license.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| softedge_preprocessor |  | ○ | PIDI safe recommended; 75% safe-filtering removes corrupted greyscale artifacts in v1.1 |
| softedge_controlnet_weight |  | ○ | Lower than depth; softer boundary — don't over-constrain the painterly style |
| depth_controlnet_weight |  | ○ | Depth remains primary structural anchor |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| SoftEdge weight > 0.60 with high denoise produces a filtered 3D render look rather than painterly |  |  |  |
| HED v1.0 models (not v1.1) hide corrupted greyscale in edge maps — use v1.1 softedge only |  |  |  |

- **Best for:** painterly boundary conditioning (-, fit -) ; soft-edge structure lock (-, fit -) ; alternative to canny for painterly output (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [lllyasviel/control_v11p_sd15_softedge](https://huggingface.co/lllyasviel/control_v11p_sd15_softedge) (Lvmin Zhang, 2023) — CreativeML OpenRAIL-M; soft edge v1.1 improved over HED 1.0 by training with 75% safe-filtered HED/PIDI maps to remove corrupted greyscale hidden in older edge models; produces gentle painterly-compatible boundary conditioning.

### ControlNet spatial conditioning literature (Zhang et al. 2023) · `situational` · paper
**ControlNet depth/pose/edges conditioning — control receipt for mesh-depth / pose-conditioned repaint**
STUDY-037 Scholar deepen.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT. [no external verdict — not checked]
- **Sources:** [ControlNet](https://arxiv.org/abs/2302.05543) — Adding conditional control to T2I diffusion.

### Diffusers AnimateDiff API — temporal pipelines · `situational` · docs
**Official pipelines: AnimateDiffPipeline, ControlNet/SparseControlNet/SDXL/vid2vid; MotionAdapter + OpenposeDetector + load_ip_adapter.**
Official pipelines: AnimateDiffPipeline, ControlNet/SparseControlNet/SDXL/vid2vid; MotionAdapter + OpenposeDetector + load_ip_adapter.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Diffusers AnimateDiff API — temporal pipelines](https://huggingface.co/docs/diffusers/main/en/api/pipelines/animatediff) — Official pipelines: AnimateDiffPipeline, ControlNet/SparseControlNet/SDXL/vid2vid; MotionAdapter + OpenposeDetector + load_ip_adapter.

### InstantX Qwen-Image-ControlNet-Union peer · `situational` · docs
**Unified ControlNet canny/soft-edge/depth/pose — sourced peer; not a verified flip.**
STUDY-037 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT. [no external verdict — not checked]
- **Sources:** [InstantX Qwen-Image-ControlNet-Union](https://huggingface.co/InstantX/Qwen-Image-ControlNet-Union) — Unified CN: canny/soft edge/depth/pose.

### Qwen-Image-Edit-2511 repaint peer · `situational` · docs
**Edit model with better character consistency vs 2509 — Apache 2.0 repaint peer; not a verified flip.**
STUDY-037 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT. [no external verdict — not checked]
- **Sources:** [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) — Better character consistency / less drift.

### control_v11p_sd15_openpose — OpenPose ControlNet v1.1 · `situational` · docs
**ControlNet v1.1 openpose checkpoint; CreativeML OpenRAIL-M; Diffusers StableDiffusionControlNetPipeline + OpenposeDetector.**
ControlNet v1.1 openpose checkpoint; CreativeML OpenRAIL-M; Diffusers StableDiffusionControlNetPipeline + OpenposeDetector.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [control_v11p_sd15_openpose — OpenPose ControlNet v1.1](https://huggingface.co/lllyasviel/control_v11p_sd15_openpose) — ControlNet v1.1 openpose checkpoint; CreativeML OpenRAIL-M; Diffusers StableDiffusionControlNetPipeline + OpenposeDetector.

### lllyasviel ControlNet v1.1 depth + openpose peers · `situational` · docs
**Depth CN works with real 3D engine depth; OpenPose CN hand+face — pose/face-region control peers.**
STUDY-037 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT. [no external verdict — not checked]
- **Sources:** [control_v11f1p_sd15_depth](https://huggingface.co/lllyasviel/control_v11f1p_sd15_depth) — Depth CN; 3D engine depth OK. ; [control_v11p_sd15_openpose](https://huggingface.co/lllyasviel/control_v11p_sd15_openpose) — OpenPose CN with hand+face.

### Normal BAE ControlNet from mesh — surface orientation lock during repaint · `situational` · · community
**Exporting the world-space normal pass from the TRELLIS.2 mesh and feeding it to ControlNet NormalBAE (lllyasviel/control_v11p_sd15_normalbae) locks surface orientation across repaint, preventing flat-shading artifacts on armor, weapons, and curved costume elements.**
ControlNet NormalBAE v1.1 uses the NYU-V2 protocol for normal maps (blue=front, red=left, green=top) which directly matches what Blender Cycles' Normal pass outputs. Export the normal pass as a 16-bit PNG from Blender. Feed it into NormalBAE ControlNet at moderate weight (0.4-0.6) alongside depth or lineart. The normal signal tells the diffusion model which surfaces face the viewer vs. tilt away, preventing the painted surface from losing the convex/concave cues that give 2.5D sprites believable volume. Most useful on armored characters and metallic weapons where surface orientation is visible as specular highlights in the painterly style.
- **For the pipeline:** Add to the stack when weapon or armor repaints come out flat. Normal maps from mesh are exact; do not run the NormalBAE preprocessor on the 3D render — it will re-estimate from pixels and introduce error.
- **Engine:** comfyui · **Applies to:** repaint · **Kind:** technique
- **VRAM:** 8-16
- **Output license:** commercial **conditional** (license: CreativeML OpenRAIL-M) — OpenRAIL-M permits commercial use with responsible-use clauses.
- **Fit:** rig 5/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| normalbae_weight |  | ○ | Higher than 0.65 can over-constrain style; normal is a refinement signal, not the primary anchor |
| source |  | ○ | Never run NormalBAE preprocessor on the 3D render — use the mesh-rendered pass directly |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Normal weight > 0.70 competes with depth ControlNet and causes confused surface gradients |  |  |  |
| Running NormalBAE preprocessor on the 3D render reintroduces estimation error — use the raw Blender Normal pass |  |  |  |

- **Best for:** surface volume preservation (-, fit -) ; specular cue retention (-, fit -) ; armored character repaint (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [lllyasviel/control_v11p_sd15_normalbae](https://huggingface.co/lllyasviel/control_v11p_sd15_normalbae) (Lvmin Zhang, 2023) — CreativeML OpenRAIL-M; NormalBAE v1.1 uses Bae's normal estimation (NYU-V2 protocol: blue=front, red=left, green=top) which matches Blender Cycles world-space normal output — significant improvement over the 'physically incorrect' MiDaS-based normal in v1.0.

