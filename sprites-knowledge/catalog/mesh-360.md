# Mesh-path 360 (image to 3D to multi-view)
_Single image -> textured 3D mesh -> rendered multi-direction sprites. The recon-model landscape + the proven TRELLIS.2 path._ · wave 5 · 2026-09-07 · [‹ catalog index](README.md)

16 recipes · 7 recommended · 4 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 1 | 1024_cascade vs 512 for thin features (5090) | trellis2 | turnaround | ▣ measured | ✅ yes | 5 | 5 | · |
| 1 | Re-pointed pipeline (generate_mesh_v3 -> Blender -> downsample) | python | game-sprite | ▣ measured | ✅ yes | 5 | 5 | · |
| 1 | Skip the v1-era trimesh cleanup for TRELLIS.2 (RAM trap) | python | turnaround | ▣ measured | ✅ yes | 5 | 4 | · |
| 1 | TRELLIS.2-4B image -> textured GLB on RTX 5090 (Blackwell) | trellis2 | turnaround | ▣ measured | ✅ yes | 5 | 5 | · |
| 2 | Step1X-3D (StepFun) | comfyui | game-sprite | ▸ reproduced | ✅ yes | 5 | 5 | · |
| 2 | TRELLIS.2-4B (Microsoft) | comfyui | game-sprite | ▸ reproduced | ✅ yes | 5 | 5 | · |
| 2 | TripoSG (VAST AI / Tripo) | comfyui | game-sprite | ▸ reproduced | ✅ yes | 5 | 4 | · |
| 6 | Direct3D-S2 (DreamTech) | comfyui | game-sprite | ▸ reproduced | ✅ yes | 5 | 4 | · |
| 6 | Hi3DGen (ByteDance / Stable-X) | comfyui | game-sprite | ▸ reproduced | ⚠ cond | 5 | 4 | · |
| 6 | Hunyuan3D-2.1 (Tencent) | comfyui | game-sprite | ▸ reproduced | ⚠ cond | 5 | 2 | · |
| 6 | SF3D / Stable Fast 3D (Stability AI) | comfyui | game-sprite | ▸ reproduced | ⚠ cond | 5 | 3 | · |
| 9 | ASME Y14.3 — orthographic multi-view analog (paywall unverified) | docs | all | analog | check | 4 | 4 | · |
| 9 | TripoSG — image-to-3D mesh for sprite path | blender | sprites | paper | check | 4 | 4 | · |
| 9 | TripoSG — rectified-flow image-to-mesh (Li et al. 2025) | comfy | all | paper | check | 4 | 4 | · |
| 9 | Unique3D (AiuniAI) | comfyui | game-sprite | ▸ reproduced | ✅ yes | 4 | 3 | · |
| 11 | Sparc3D / SparC (academic) | python | game-sprite | ▸ reproduced | ⛔ no | 4 | 1 | · |

## Detail

### 1024_cascade vs 512 for thin features (5090) · `recommended` · ▣ measured
**1024_cascade yields visibly sharper faces/armor/folds than 512 at near-identical VRAM and time on the 5090; thin features survive at both.**
Same character meshed at pipeline_type='512' vs '1024_cascade', identical to_glb. 1024 generated ~3.9x the geometry (2.26M vs 0.58M verts) and looked sharper (face reads as a face, armor filigree, robe folds) EVEN after decimating both to ~1M faces — better generation survives decimation. A thin vertical staff (shaft + ornate head + finial) reconstructed cleanly at BOTH resolutions. The RESEARCH-REPORT's ~24GB OOM fear for 1024 was 5080-era pessimism: on the 5090, 1024_cascade peaked 3.5GB allocator (~16GB total).
- **For the pipeline:** Use 1024_cascade for hero/portrait/close characters (face-as-face survives the 64px downscale). 512 is fine for tiny background mobs where the gain washes out. Cost is ~nil on the 5090, so default to 1024_cascade unless batching at scale.
- **Engine:** trellis2 · **Applies to:** turnaround · **Base:** TRELLIS · **Kind:** technique
- **VRAM:** 3.5 allocator / ~16 total at 1024_cascade
- **Validated under:** RTX 5090; 512 gen 60s/3.4GB, 1024_cascade gen 37s/3.5GB; both looked-at from 8 angles 2026-06-07.
- **Output license:** commercial **yes** (license: n/a (technique))
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** A/B looked-at on the rig. [no external verdict — not checked]
- **Sources:** [TRELLIS.2 (resolution tiers)](https://arxiv.org/abs/2512.14692) — 1024 cascade credited with finer detail / structural stability.

### Re-pointed pipeline (generate_mesh_v3 -> Blender -> downsample) · `recommended` · ▣ measured
**pipeline.py --backend trellis_v3 drives image -> TRELLIS.2 mesh -> Blender 8-dir render -> 64px downsample to 8 directional sprites in ~160s, no ComfyUI server.**
generate_mesh_v3.py replaces the dead ComfyUI-API generate_mesh_v2.py with a direct trellis2-env call. It self-locates the TRELLIS repo (sets sys.path + chdir so 'import trellis2' resolves) and sets its own env, so pipeline.py can shell out to it. Because trimesh+PIL import cleanly in trellis2-env, one interpreter drives mesh+clean+downsample; only render_views.py runs in Blender's bundled Python. Wired pipeline.py with --backend trellis_v3 --ptype.
- **For the pipeline:** This is the studio's sprite-from-character pipeline, runnable headless. Stage chaining: mesh-360 -> render-light -> downsample-finish.
- **Engine:** python · **Applies to:** game-sprite · **Base:** TRELLIS · **Kind:** pipeline
- **Validated under:** RTX 5090; e2e trellis_v3 512 + --no-cleanup --no-mesh-gate --hdri = 8 sprites in 159.5s (mesh 117s, render 7s, downsample <1s) 2026-06-07.
- **Output license:** commercial **yes** (license: n/a (orchestration))
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** Full chain produced 8 looked-at 64px sprites on the rig. [no external verdict — not checked]
- **Sources:** [trellis-sprite-pipeline (generate_mesh_v3.py, pipeline.py)](https://github.com/mcp-tool-shop-org/trellis-sprite-pipeline) — The re-pointed pipeline + v3 mesh generator.

### Skip the v1-era trimesh cleanup for TRELLIS.2 (RAM trap) · `recommended` · ▣ measured
**clean_mesh.py and the mesh-gate's trimesh.split() on a ~1M-face/4096^2-texture TRELLIS GLB are a system-RAM hog that can trip the watchdog; TRELLIS.2 O-Voxel meshes are clean, so skip them.**
The parked clean_mesh.py (split + component filter + fix_normals) and the pipeline mesh-gate both call trimesh.split() on the high-poly textured GLB. That is CPU/RAM-heavy; stacked with a resident ComfyUI it pushed system RAM to 99% and the aborting watchdog killed the run. clean_mesh is TRELLIS-v1-era (built to remove v1's floating artifacts); TRELLIS.2's O-Voxel output is a clean single component, so cleanup adds RAM cost + texture-loss risk for ~no benefit. Blender render + Lanczos downsample are RAM-light and unaffected.
- **For the pipeline:** Run the sprite pipeline with --no-cleanup --no-mesh-gate for the trellis_v3 backend. If a gate is wanted, run it on a decimated copy, not the full 1M-face mesh. Keep the aborting watchdog up for every GPU run — it caught this correctly.
- **Engine:** python · **Applies to:** turnaround · **Base:** TRELLIS · **Kind:** technique
- **Validated under:** RTX 5090, 64GB RAM; watchdog _watchdog.ps1 fired RAM>=90% (99%) during cleanup 2026-06-07; re-run with --no-cleanup --no-mesh-gate completed clean.
- **Output license:** commercial **yes** (license: n/a)
- **Fit:** rig 5/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Pipeline killed mid-'Cleaning mesh' with no traceback | trimesh.split on 1M-face mesh spikes system RAM; watchdog aborts at 90% | --no-cleanup --no-mesh-gate, or gate on a decimated copy |  |

- **Verify:** Reproduced the RAM trip + the clean re-run on the rig. [no external verdict — not checked]
- **Sources:** [watchdog kill log + e2e reruns (trellis-sprite-pipeline)](https://github.com/mcp-tool-shop-org/trellis-sprite-pipeline) — clean step tripped the RAM watchdog; --no-cleanup run completed in 159.5s.

### TRELLIS.2-4B image -> textured GLB on RTX 5090 (Blackwell) · `recommended` · ▣ measured
**TRELLIS.2-4B runs on the 5090 in a dedicated torch-2.10+cu130 venv and turns one front image into a textured GLB; commercial-clean (mesh is MIT).**
Run TRELLIS.2 in a dedicated env (E:/AI-Models/trellis2-env, torch 2.10.0+cu130) against the standalone repo (E:/AI-Models/TRELLIS.2-repo), NOT the ComfyUI-Trellis2 node (its wheels are torch-2.10-locked vs ComfyUI's 2.12 -> DLL/ABI mismatch). Load with Trellis2ImageTo3DPipeline.from_pretrained('microsoft/TRELLIS.2-4B').cuda(); mesh = pipe.run(img, pipeline_type=...)[0]; mesh.simplify(); o_voxel.postprocess.to_glb(...). dinov3 image encoder is gated (HF token, cached). Background removal patched from gated RMBG-2.0 to ungated ZhengPeng7/BiRefNet (input-only, commercial-clean).
- **For the pipeline:** This is the studio's proven 360 engine. The mesh is MIT (shippable); BiRefNet touches only the input (not a shipped asset). Generate the source character on a commercial-clean base (SDXL base 1.0 or Apache Z-Image/Chroma) and the whole chain stays commercial.
- **Engine:** trellis2 · **Applies to:** turnaround · **Base:** TRELLIS · **Kind:** model
- **Runs:** 3 · **VRAM:** 15-16 total (3.4-3.5 allocator peak) at both 512 and 1024_cascade
- **Validated under:** RTX 5090 32GB, Win11, trellis2-env torch 2.10.0+cu130, ATTN_BACKEND=sdpa + grafted Blackwell sparse-attention (_sdpa_varlen), HF_HOME=E:/AI-Models/hf-cache. 512^3: gen 60s, gen-peak 3.4GB (allocator), 582k->482k verts, 35.9MB GLB. 1024_cascade: gen 37s, gen-peak 3.5GB, 2.26M->477k verts, 38.3MB GLB. Watchdog clean.
- **Measured receipt (tensor-engine):** `trellis2-env (tensor-engine-knowledge candidate)` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **yes** (license: MIT (TRELLIS.2 code+mesh); BiRefNet MIT (input preprocessing only); dinov3 gated research license (encoder, not shipped)) — Shipped asset = the mesh (MIT) rendered to 2D in Blender. AVOID the nvdiffrast/nvdiffrec render path (non-commercial NVIDIA license) — render in Blender instead.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| pipeline_type | 512 / 1024 / 1024_cascade / 1536_cascade | ○ | run() arg; default is 1024_cascade. Call explicitly. Both DiTs load at from_pretrained. |
| to_glb.decimation_target | 1000000 | ○ | 1M faces ~ game-appropriate; raise to 4M-10M to keep 1024 detail (heavier RAM downstream) |
| to_glb.texture_size | 4096 | ○ | PBR texture bake; webp via extension_webp=True |
| to_glb.remesh / remesh_band / remesh_project | True / 1 / 0 | ○ | smoke-test baseline; remesh=False + project~1 better preserves thin features per research |
| ATTN_BACKEND | sdpa | ● | xformers is DEAD on Blackwell sm_120; flash_attn won't build on Windows |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Side/back of head is a featureless white smear | single front-view input gives TRELLIS no data for head sides | feed a back/side reference view, or paint-fix; NOT fixable by resolution |  |
| Back textures desaturated/hallucinated (never black with AgX lift) | TRELLIS hallucinates unseen back from a front image | acceptable at sprite size; tonemap keeps them readable |  |
| expandable_segments not supported warning | Windows CUDA allocator | benign — ignore |  |

- **Verify:** Run end-to-end on the rig 2026-06-07; outputs looked-at from 8 angles. [no external verdict — not checked]
- **Sources:** [microsoft/TRELLIS.2](https://github.com/microsoft/TRELLIS.2) — Official TRELLIS.2 repo (MIT); O-Voxel image-to-3D. ; [TRELLIS.2](https://arxiv.org/abs/2512.14692) — TRELLIS.2 method paper; 512^3 vs 1024^3 O-Voxel representation. ; [microsoft/TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B) — The 4B checkpoint used; ships 512 + 1024 DiTs. ; [ZhengPeng7/BiRefNet](https://huggingface.co/ZhengPeng7/BiRefNet) — Ungated MIT background remover swapped in for gated RMBG-2.0.

### Step1X-3D (StepFun) · `recommended` · ▸ reproduced
**Apache-2.0 textured-3D pipeline (geometry DiT + SDXL-based texture) with first-class LoRA support — the cleanest fully-permissive license alongside TRELLIS.2.**
StepFun's open framework generates watertight geometry (hybrid VAE-DiT producing TSDF) plus a texture module fine-tuned from Stable Diffusion XL guided by normal and position maps for tight texture-geometry alignment. Explicitly supports LoRA to control symmetry and geometric-detail level via tags. Apache-2.0 across the repo (verified via GitHub license API).
- **For the pipeline:** Strong commercial-safe alternative to TRELLIS.2 with a built-in LoRA story — you can train a style/symmetry LoRA on it for consistent JRPG turnarounds and keep an Apache-2.0 license trail. Good fit when you want controllable geometric detail per-asset (weapons vs. cloth).
- **Engine:** comfyui · **Applies to:** game-sprite · **Base:** VAE-DiT + SDXL texture · **Kind:** model
- **VRAM:** 16-24
- **Output license:** commercial **yes** (license: Apache-2.0) — GitHub license API returns Apache-2.0 for stepfun-ai/Step1X-3D. No MAU/revenue/territory caps. A LoRA trained on Apache-2.0 weights stays commercial-clean. The SDXL-derived texture module's lineage is worth a note (SDXL is CreativeML OpenRAIL-M) but the Step1X release is Apache-2.0.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| geometry_rep | watertight TSDF | ○ | hybrid VAE-DiT |
| texture_base | SDXL fine-tune | ○ | normal+position guided |
| lora | supported | ○ | tag-controlled symmetry/detail |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| texture seams on UV islands | SDXL texture module per-view inpainting | regenerate texture stage; rely on geometry stage for silhouette and bake later |  |

- **Verify:** Both sources resolve. GitHub explicitly states Apache License 2.0; arXiv 2505.07747 confirms hybrid VAE-DiT geometry + SD-XL texture and LoRA transfer to 3D. License Apache-2.0 + commercial=yes accurate. [no external verdict — not checked]
- **Sources:** [stepfun-ai/Step1X-3D: Towards High-Fidelity and Controllable Generation of Textured 3D Assets](https://github.com/stepfun-ai/Step1X-3D) (StepFun AI, 2025) — Apache-2.0 framework generating textured 3D (VAE-DiT geometry + SDXL texture) with LoRA support for symmetry/detail control. ; [Step1X-3D: Towards High-Fidelity and Controllable Generation of Textured 3D Assets](https://arxiv.org/html/2505.07747v1) (StepFun AI, 2025) — Hybrid VAE-DiT produces watertight TSDF geometry; texture module fine-tuned on SDXL with normal/position-map guidance for geometry-texture alignment.

### TRELLIS.2-4B (Microsoft) · `recommended` · ▸ reproduced
**MIT-licensed 4B image-to-3D that outputs full-PBR textured meshes with GLB export at 512/1024/1536 voxel tiers — the strongest fully-commercial option on this list.**
Microsoft's successor to the CVPR-2025 TRELLIS, built on a 'field-free' sparse-voxel (O-Voxel) latent. Single-image to 3D, outputs a mesh with full PBR materials (Base Color, Roughness, Metallic, Opacity/translucency) and exports GLB via o_voxel.postprocess.to_glb() at up to 4096px texture. Three resolution tiers (512/1024/1536) trade speed for thin-feature fidelity — the 1024/1536 tiers are what you want for weapons and sharp silhouette edges before rendering to sprite directions.
- **For the pipeline:** Best default for a commercial JRPG sprite turnaround pipeline on a 32GB 5090: MIT means zero license drag on shipped assets or on any style LoRA you train. Run the 1024 or 1536 tier for weapon/thin-feature fidelity, export GLB, render N directions in Blender. Repo notes Linux + NVIDIA; on Windows expect to run via WSL2 or the ComfyUI-TRELLIS path.
- **Engine:** comfyui · **Applies to:** game-sprite · **Base:** TRELLIS · **Kind:** model
- **VRAM:** 24-32
- **Output license:** commercial **yes** (license: MIT (code + weights)) — MIT on both the microsoft/TRELLIS.2 repo and the microsoft/TRELLIS.2-4B model card. No MAU/revenue caps, no territorial exclusions. A LoRA you train on this inherits MIT — clean for a commercial studio.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| resolution_tiers | 512 / 1024 / 1536 | ○ | ~3s / ~17s / ~60s on H100; higher tier = sharper thin features |
| texture_resolution | up to 4096px | ○ | configurable in to_glb() |
| min_vram | 24GB stated | ○ | fits the 5090's 32GB with headroom |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| thin weapons/blades thicken or fuse to body | low voxel tier under-resolves sub-voxel features | use 1024 or 1536 tier; clean alpha-matted input with weapon clearly separated from silhouette |  |

- **Verify:** Both sources resolve. microsoft/TRELLIS.2 GitHub (8.2k stars) and HF model card both state MIT License for code + weights. Confirmed: PBR mesh output (Base Color/Roughness/Metallic/Opacity) with GLB export, 24GB+ VRAM, 512/1024/1536 tiers, transparency/translucency. License + commercial=yes accurate. [no external verdict — not checked]
- **Sources:** [microsoft/TRELLIS.2: Native and Compact Structured Latents for 3D Generation](https://github.com/microsoft/TRELLIS.2) (Microsoft Research, 2025) — Released under MIT License; outputs textured PBR meshes (Base Color/Roughness/Metallic/Opacity) with GLB export via to_glb(), needs >=24GB VRAM, tiers 512/1024/1536. ; [microsoft/TRELLIS.2-4B](https://huggingface.co/microsoft/TRELLIS.2-4B) (Microsoft, 2025) — Model card states MIT License and that output is a 'Mesh with PBR Materials' including transparency/translucency.

### TripoSG (VAST AI / Tripo) · `recommended` · ▸ reproduced
**MIT, low-VRAM (~8GB), high-fidelity GEOMETRY-only image-to-3D — excellent silhouettes and sharp edges but you must texture/paint separately.**
VAST AI's large-scale rectified-flow transformer turns a single image into a high-fidelity mesh with sharp geometric features. Both code and weights are MIT (verified via GitHub license API + HF model card). Key caveat: TripoSG generates SHAPE/geometry, not PBR texture — pair it with a texture pass (e.g., a paint/bake step or a separate texture model) for finished sprites.
- **For the pipeline:** MIT + low VRAM makes it a safe, cheap geometry workhorse on the 5090. Because output is untextured, it fits a 2.5D sprite flow where you render geometry to depth/normal/AO passes and then style-paint in your diffusion sprite pipeline rather than relying on baked PBR. Strong silhouette fidelity helps thin features survive to the sprite render.
- **Engine:** comfyui · **Applies to:** game-sprite · **Base:** Rectified-flow transformer · **Kind:** model
- **VRAM:** 8-16
- **Output license:** commercial **yes** (license: MIT (code + weights)) — VAST-AI-Research/TripoSG repo and VAST-AI/TripoSG model card both MIT. No caps. Note the hosted Tripo3D web service has its own ToS — the MIT grant applies to the open-weights model you run locally, which is what matters for a self-hosted studio pipeline.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| min_vram | >=8GB | ○ | low-VRAM friendly |
| output | geometry/mesh, no PBR texture | ○ | texture separately |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| no color/material on output | model is shape-only | add a texture/paint stage or render geometry passes into the diffusion sprite step |  |

- **Verify:** Both sources resolve. HF model card header shows 'mit'; GitHub footer shows 'MIT license'. Confirmed image-to-mesh, >8GB VRAM, sharp geometric features (geometry-focused, not PBR). License MIT + commercial=yes accurate. [no external verdict — not checked]
- **Sources:** [VAST-AI/TripoSG](https://huggingface.co/VAST-AI/TripoSG) (VAST AI Research / Tripo, 2025) — Released under MIT license; high-fidelity image-to-mesh, needs CUDA GPU with >8GB VRAM. ; [VAST-AI-Research/TripoSG](https://github.com/VAST-AI-Research/TripoSG) (VAST AI Research, 2025) — GitHub license API confirms MIT for the TripoSG repository; produces meshes with sharp geometric features (geometry, not PBR texture).

### Direct3D-S2 (DreamTech) · `situational` · ▸ reproduced
**NeurIPS-2025 MIT model with Spatial Sparse Attention enabling native 1024-resolution geometry — high detail for sharp features, geometry-focused output.**
DreamTech's Direct3D-S2 introduces Spatial Sparse Attention (SSA) on sparse volumes, giving ~3.9x faster forward / ~9.6x faster backward passes and enabling 1024-resolution generation. It is geometry-focused (high-resolution shape). MIT-licensed (verified via GitHub license API), so commercially clean. A Gradio demo does image-to-mesh.
- **For the pipeline:** MIT + native 1024 resolution makes it a credible high-detail geometry source on the 5090 for assets where thin features and silhouette precision dominate. Like TripoSG/Hi3DGen it is geometry-first, so slot it into a render-then-paint sprite flow. Verify the weight checkpoint license once before shipping.
- **Engine:** comfyui · **Applies to:** game-sprite · **Base:** Sparse-volume DiT (SSA) · **Kind:** model
- **VRAM:** 16-24
- **Output license:** commercial **yes** (license: MIT) — GitHub license API returns MIT for DreamTechAI/Direct3D-S2. No caps/territory limits. Confirm the released weight checkpoint on HF carries the same MIT (code repos sometimes differ from weight cards) — but the repo license is clean.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| resolution | 1024 (native) | ○ | via Spatial Sparse Attention |
| speedup | 3.9x fwd / 9.6x bwd | ○ | vs dense attention |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Windows build friction | sparse-attention CUDA kernels | use WSL2 or provided container; the 5090 sm_120 may need recent CUDA/torch builds |  |

- **Verify:** Both sources resolve. GitHub states 'released under the MIT License'; arXiv 2505.17412 confirms Spatial Sparse Attention, 1024-res training on 8 GPUs, 3.9x/9.6x fwd/bwd speedups, image-to-mesh Gradio demo. License MIT + commercial=yes accurate. [no external verdict — not checked]
- **Sources:** [DreamTechAI/Direct3D-S2: Gigascale 3D Generation Made Easy with Spatial Sparse Attention (NeurIPS 2025)](https://github.com/DreamTechAI/Direct3D-S2) (DreamTech AI, 2025) — MIT-licensed; SSA enables 1024-resolution 3D generation with 3.9x/9.6x fwd/bwd speedups and an image-to-mesh Gradio demo. ; [Direct3D-S2: Gigascale 3D Generation Made Easy with Spatial Sparse Attention](https://arxiv.org/abs/2505.17412) (DreamTech AI, 2025) — Spatial Sparse Attention makes high-resolution (1024) sparse-volume 3D generation practical and accurate.

### Hi3DGen (ByteDance / Stable-X) · `situational` · ▸ reproduced
**ICCV-2025 normal-bridging pipeline rated best-in-class for GEOMETRY detail/sharp edges; MIT code but rides Stable-X/trellis-normal weights — confirm the weight license before commercial shipping.**
Hi3DGen estimates surface normals from the input image then uses normal-regularized latent diffusion to reconstruct geometry, yielding sharper edges and fewer artifacts than direct geometry predictors — community consensus rates it top for geometric fidelity. It is geometry-focused (no native PBR texture). The repo (bytedance/Hi3DGen) is MIT, but it loads Stable-X/trellis-normal-v0-1 weights derived from the TRELLIS line.
- **For the pipeline:** Best pick when weapon/edge fidelity is the priority and you texture downstream — the normal-bridge specifically preserves the thin-feature and sharp-silhouette detail that JRPG weapons need. The license is MIT-favorable but is a two-layer check (code vs. weights); do the weight-card verification once and record it before it touches a shipped asset.
- **Engine:** comfyui · **Applies to:** game-sprite · **Base:** TRELLIS (normal-bridged) · **Kind:** model
- **VRAM:** 16-24
- **Output license:** commercial **conditional** (license: MIT (code); weights = Stable-X/trellis-normal (TRELLIS-derived, verify)) — Code repo is MIT (verified, github.com/Stable-X/Hi3DGen LICENSE and bytedance/Hi3DGen both MIT). BUT the actual generation weights are Stable-X/trellis-normal-v0-1; since a LoRA/derivative inherits the WEIGHT license, you must confirm that specific HF model card's license (TRELLIS base is MIT, which is favorable, but the normal-bridged checkpoint should be checked individually before commercial shipping). Treat as conditional until the weight card is verified.
- **License correction (verifier):** MIT (code + weights); commercial_use: yes
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| pipeline | image->normal->geometry | ○ | normal bridging |
| weights | Stable-X/trellis-normal-v0-1 | ○ | TRELLIS-derived; geometry only |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| uncertain weight license at ship time | code MIT but weights from a separate HF card | open the Stable-X/trellis-normal-v0-1 model card, record its license, before commercial use |  |

- **Verify:** All sources resolve. GitHub bytedance/Hi3DGen is MIT (code). Crucially, the weights at Stable-X/trellis-normal-v0-1 HF card state license 'mit' — NOT conditional/encumbered as the entry hedged. ICCV 2025 paper confirmed (Ye/Chongjie Ye et al., arXiv 2503.22236). Correction: weights are MIT, so commercial_use should be 'yes', not 'conditional', and the 'verify' hedge on weights is resolved. [no external verdict — not checked]
- **Sources:** [bytedance/Hi3DGen (High-fidelity 3D Geometry Generation from Images via Normal Bridging)](https://github.com/bytedance/Hi3DGen) (ByteDance; CUHK-Shenzhen; AIR, Tsinghua, 2025) — MIT-licensed repo that generates high-fidelity 3D geometry via normal bridging and loads the Stable-X/trellis-normal-v0-1 weights. ; [Hi3DGen: High-fidelity 3D Geometry Generation from Images via Normal Bridging (ICCV 2025)](https://openaccess.thecvf.com/content/ICCV2025/papers/Ye_Hi3DGen_High-fidelity_3D_Geometry_Generation_from_Images_via_Normal_Bridging_ICCV_2025_paper.pdf) (Ye et al., 2025) — Normal-bridged latent diffusion produces sharper geometry and fewer artifacts than direct geometry predictors.

### Hunyuan3D-2.1 (Tencent) · `situational` · ▸ reproduced
**Production-grade PBR image-to-3D (albedo/roughness/metallic/normal) but under the Tencent Community License: commercial OK only under 1M MAU and excludes EU/UK/South Korea.**
Tencent's open-weights 2.1 line produces high-fidelity meshes with a real PBR material pipeline (albedo, roughness, metallic, normal) intended for engine use. Shape and texture are separate stages. The license is the decisive caveat — it permits commercial distribution of generated assets WITH attribution ('Created with Hunyuan 3D-2.1') but caps at <1M MAU and carves out the EU, UK, and South Korea from the licensed territory.
- **For the pipeline:** Quality is top-tier and 29GB fits the 5090, but the EU/UK/SK territorial carve-out is disqualifying for a worldwide commercial JRPG unless legal sign-off accepts the geo-restriction or you stay under 1M MAU and accept the attribution. Use TRELLIS.2 or Step1X-3D for shipped assets; reserve Hunyuan only if you can live with the license. Hunyuan3D-2GP community fork lowers VRAM for poorer GPUs.
- **Engine:** comfyui · **Applies to:** game-sprite · **Base:** Hunyuan3D-DiT · **Kind:** model
- **VRAM:** 29 (shape+texture)
- **Output license:** commercial **conditional** (license: Tencent Hunyuan 3D 2.1 Community License) — VERIFIED from LICENSE file: commercial use permitted under <1M MAU; if you exceed 1M MAU on release date you must request a license from Tencent (hunyuan3d@tencent.com). Territory EXCLUDES EU/UK/South Korea — meaning a game sold in those markets is outside the grant. Attribution required. A LoRA trained on it inherits these terms. For a global commercial Steam release this is a real legal hazard, not a formality.
- **Fit:** rig 5/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| vram_shape | ~10GB | ○ | shape stage only |
| vram_texture | ~21GB | ○ | PBR texture stage |
| vram_combined | ~29GB | ○ | full pipeline; fits 5090 32GB |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| asset legally unusable for EU/UK/SK distribution | license territory excludes those regions | do not use for worldwide commercial release; switch to an MIT/Apache base |  |

- **Verify:** Both sources resolve. LICENSE confirms Tencent Hunyuan 3D 2.1 Community License: commercial use permitted but Section 4 requires separate license at >1M MAU; territory explicitly excludes EU/UK/South Korea. Repo confirms PBR meshes and VRAM (~10GB shape, ~21GB texture, ~29GB combined). commercial_use=conditional accurate. [no external verdict — not checked]
- **Sources:** [Hunyuan3D-2.1 LICENSE (Tencent Hunyuan 3D 2.1 Community License Agreement)](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE) (Tencent Hunyuan, 2025) — Commercial use permitted but >1M MAU requires a separate Tencent license and territory excludes the EU, UK, and South Korea (Sections 1.l and 4). ; [Hunyuan3D-2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material](https://github.com/tencent-hunyuan/hunyuan3d-2.1) (Tencent Hunyuan, 2025) — Generates PBR meshes; ~10GB VRAM shape, ~21GB texture, ~29GB combined.

### SF3D / Stable Fast 3D (Stability AI) · `situational` · ▸ reproduced
**Fast (~0.5s) UV-unwrapped textured mesh with delighting at ~6-7GB VRAM, but under the Stability Community License: free commercial ONLY under $1M/yr revenue.**
SF3D turns a single image into a UV-unwrapped, textured, low-poly mesh with material params and a delighting step that strips baked lighting — game-engine friendly out of the box, and very fast (~0.5s, ~7GB). The license is the catch: Stability AI Community License is free for commercial use only for entities under $1M annual revenue; above that you need an enterprise license.
- **For the pipeline:** The fastest turnaround and the only one here that hands you a delit, UV-unwrapped, engine-ready textured mesh in one shot — attractive for rapid greybox/iteration. But the $1M revenue gate means it is a temporary/early-stage choice; if the studio scales past $1M the license flips and any asset/LoRA built on it needs an enterprise deal. Prefer MIT/Apache bases for the canonical shipped pipeline.
- **Engine:** comfyui · **Applies to:** game-sprite · **Base:** Large reconstruction model · **Kind:** model
- **VRAM:** 6-7
- **Output license:** commercial **conditional** (license: Stability AI Community License) — Free for research/non-commercial AND for commercial use by orgs/individuals under US$1M annual revenue; at/above $1M you must obtain a Stability enterprise license before commercial use of SF3D, its derivatives, or its outputs. A LoRA/derivative inherits this. For a small studio under the threshold it is usable today, but it is a revenue-gated commercial license, not unconditional.
- **Fit:** rig 5/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| speed | ~0.5s | ○ | single image |
| vram | ~6-7GB | ○ | default options |
| output | UV-unwrapped textured + delighting | ○ | engine-ready |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| license flips at $1M revenue | Stability Community License revenue gate | track studio revenue; migrate canonical assets to MIT/Apache base before crossing threshold |  |

- **Verify:** Both sources resolve. HF card and Stability news confirm Stability AI Community License: free for commercial use only for orgs/individuals under $1M annual revenue, enterprise license required above. Single-image UV-unwrapped textured mesh with delighting, sub-second, ~7GB. commercial_use=conditional accurate. [no external verdict — not checked]
- **Sources:** [stabilityai/stable-fast-3d](https://huggingface.co/stabilityai/stable-fast-3d) (Stability AI, 2024) — Single image to UV-unwrapped textured mesh with delighting in ~0.5s at ~7GB VRAM, under the Stability AI Community License. ; [Introducing Stable Fast 3D: Rapid 3D Asset Generation From Single Images](https://stability.ai/news-updates/introducing-stable-fast-3d) (Stability AI, 2024) — Community License is free for commercial use only for organizations/individuals under US$1M annual revenue; above that an enterprise license is required.

### ASME Y14.3 — orthographic multi-view analog (paywall unverified) · `situational` · analog
**Fixed front/side/top views with shared scale and registration — hold for mesh→8-dir / pose-grid cell registration; limit ≠ painterly SDXL sheets.**
STUDY-059 Analogist #1 paywall unverified. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 Verifier: Analogist #1/#2 paywall unverified — do not land as verified. Flip 486: 0. [no external verdict — not checked]
- **Sources:** [ASME Y14.3 Orthographic and Pictorial Views](https://www.asme.org/codes-standards/find-codes-standards/y14-3-orthographic-pictorial-views) — Orthographic/pictorial views with shared scale and registration.

### TripoSG — image-to-3D mesh for sprite path · `situational` · paper
**Large rectified-flow mesh synthesis from images — commercial-leaning mesh-360 path that feeds Blender orthographic sprite renders.**
Large rectified-flow mesh synthesis from images — commercial-leaning mesh-360 path that feeds Blender orthographic sprite renders.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [TripoSG — image-to-3D mesh for sprite path](https://arxiv.org/abs/2502.06608) — Large rectified-flow mesh synthesis from images — commercial-leaning mesh-360 path that feeds Blender orthographic sprite renders.

### TripoSG — rectified-flow image-to-mesh (Li et al. 2025) · `situational` · paper
**Rectified-flow image-to-mesh for mesh-360 sprite path — deepen; flip 486: 0.**
STUDY-059 Scholar deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** comfy · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [TripoSG](https://arxiv.org/abs/2502.06608) — Rectified-flow image-to-mesh for mesh-360.

### Unique3D (AiuniAI) · `legacy` · ▸ reproduced
**MIT NeurIPS-2024 single-image-to-textured-mesh in ~30s — older but fully commercial; quality now trails the 2025 sparse-voxel models.**
Unique3D generates a high-fidelity, diverse, TEXTURED mesh from a single wild image in ~30s via a multi-view diffusion + reconstruction approach. MIT-licensed (verified via GitHub license API: AiuniAI/Unique3D = MIT). It is a 2024-era model, so geometric detail and thin-feature fidelity lag the 2025 sparse-voxel/DiT generation (TRELLIS.2, Step1X-3D, Direct3D-S2).
- **For the pipeline:** A commercially-clean, textured-output fallback that runs comfortably on the 5090, but in 2026 it is effectively legacy — only reach for it if its specific multi-view texture look suits a stylized JRPG asset better than the newer models. For new pipeline standardization, prefer TRELLIS.2 or Step1X-3D.
- **Engine:** comfyui · **Applies to:** game-sprite · **Base:** Multi-view diffusion + recon · **Kind:** model
- **VRAM:** 16-24
- **Output license:** commercial **yes** (license: MIT) — GitHub license API confirms MIT for AiuniAI/Unique3D. No caps. The hosted aiuni.ai service has separate ToS; the MIT grant covers the open implementation you self-host. Clean for commercial use and LoRA derivation.
- **Fit:** rig 4/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| speed | ~30s | ○ | single image to textured mesh |
| output | textured mesh | ○ | multi-view diffusion |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| soft/blurry fine geometry vs 2025 models | 2024-era multi-view recon resolution | use for stylized assets; switch to TRELLIS.2/Step1X-3D for sharp weapons |  |

- **Verify:** Both sources resolve. GitHub AiuniAI/Unique3D shows 'MIT license' and NeurIPS 2024 designation; arXiv 2405.20343 confirms (Wu/Kailu Wu et al., ISOMER reconstruction). Single-view to textured mesh ~30s. License MIT + commercial=yes accurate. [no external verdict — not checked]
- **Sources:** [AiuniAI/Unique3D: High-Quality and Efficient 3D Mesh Generation from a Single Image (NeurIPS 2024)](https://github.com/AiuniAI/Unique3D) (Wu et al. (AiuniAI / Tsinghua), 2024) — MIT-licensed (per GitHub license API); generates high-fidelity textured meshes from a single wild image in ~30s. ; [Unique3D: High-Quality and Efficient 3D Mesh Generation from a Single Image](https://arxiv.org/abs/2405.20343) (Wu et al., 2024) — Multi-view diffusion plus reconstruction yields diverse textured meshes from single-view images efficiently.

### Sparc3D / SparC (academic) · `avoid` · ▸ reproduced
**State-of-the-art 1024-resolution watertight GEOMETRY (open surfaces, disconnected parts) — but the repo ships NO LICENSE file, so it is legally all-rights-reserved and unsafe to ship commercially.**
Sparc3D (paper 'SparC') combines a sparse deformable marching-cubes representation (Sparcubes) with a sparse-conv VAE (Sparconv-VAE) to reconstruct high-resolution (1024) watertight meshes from challenging inputs including open surfaces, disconnected components, and intricate geometry — exactly the thin-feature regime JRPG weapons stress. It is geometry-only. The decisive problem: the GitHub repo (lizhihao6/Sparc3D) has no LICENSE file (GitHub license API returns 404), which under default copyright means all rights reserved.
- **For the pipeline:** Best-in-class for thin/disconnected geometry (open surfaces, fine weapon parts), which is tempting for JRPG sprites — but with no license it cannot legally feed a commercial pipeline or a shipped LoRA. Treat as research-only / inspiration; if the studio wants this quality, push the authors for an MIT release or use Direct3D-S2/Hi3DGen for similarly high-res geometry under a real license.
- **Engine:** python · **Applies to:** game-sprite · **Base:** Sparse marching cubes + Sparconv-VAE · **Kind:** model
- **VRAM:** 16-24
- **Output license:** commercial **no** (license: NONE PUBLISHED (repo has no LICENSE file; default = all rights reserved)) — VERIFIED: GitHub license API returns 404 for lizhihao6/Sparc3D and the LICENSE URL 404s. Absence of a license means no grant of any rights — default copyright is all-rights-reserved, so commercial use (and shipping any LoRA/derivative) is not permitted absent an explicit license or written permission from the authors. Academic/research only until a license is added.
- **Fit:** rig 4/5 · studio 1/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| resolution | 1024 watertight | ○ | <30s mesh conversion |
| strength | open surfaces / disconnected parts | ○ | thin-feature fidelity |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| no legal right to use output commercially | repo ships no LICENSE (all rights reserved) | do not use commercially; request explicit license from authors or choose a licensed alternative |  |

- **Verify:** Both sources resolve. GitHub lizhihao6/Sparc3D confirmed to have NO LICENSE file / no license badge (all-rights-reserved by default); arXiv 2505.14521 confirmed (Zhihao Li, Yufei Wang, Heliang Zheng, Yihao Luo, Bihan Wen) — Sparcubes + Sparconv-VAE, watertight 1024-res. License claim 'NONE PUBLISHED' and commercial_use=no are accurate. [no external verdict — not checked]
- **Sources:** [Sparc3D / SparC: Sparse Representation and Construction for High-Resolution 3D Shapes Modeling](https://arxiv.org/abs/2505.14521) (Li et al., 2025) — Sparcubes + Sparconv-VAE reconstruct watertight 1024-resolution meshes from open surfaces, disconnected components, and intricate geometry at SOTA fidelity. ; [lizhihao6/Sparc3D (official repo)](https://github.com/lizhihao6/Sparc3D) (Li et al., 2025) — Repository has no LICENSE file (GitHub license API and /blob/main/LICENSE both return 404), so default copyright applies and commercial use is not granted.

