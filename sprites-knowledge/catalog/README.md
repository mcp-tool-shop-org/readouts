# Catalog — sprite-pipeline recipes (mesh · render · downsample · NVS · sheets · eval · animation)

Generated from `recipes.db` · wave 5 · 2026-09-07. NEVER hand-edited — regenerated from the DB.

The portable **concept-art -> game-ready 2.5D JRPG sprite** craft for this rig (RTX 5090 · Blackwell · 32 GB · Win 11 / WSL2). Sibling KBs: [model-knowledge](../../model-knowledge/catalog/README.md) (the *weights*) · [tensor-engine-knowledge](../../tensor-engine-knowledge/catalog/README.md) (the *software* + rig-measured receipts) · [training-knowledge](../../training-knowledge/catalog/README.md) (the *training craft*). This one owns the *sprite-pipeline recipes* — and points at measured numbers via `engine_recipe_ref` (tensor-engine) and base weights via `base_model_slug` (model-knowledge), never restating them.

## Proven on-rig

Recipes whose `evidence_strength` is ▣ **measured-on-rig** — validated on this exact machine.

| Lane | Recipe | Engine | Applies | Comm | Validated under | ✓ |
|---|---|---|---|---|---|---|
| Mesh-path 360 (image to 3D to multi-view) | 1024_cascade vs 512 for thin features (5090) | trellis2 | turnaround | ✅ yes | RTX 5090; 512 gen 60s/3.4GB, 1024_cascade gen 37s/3.5GB; both looked-at from 8 angles 2026-06-07. | · |
| Mesh-path 360 (image to 3D to multi-view) | Re-pointed pipeline (generate_mesh_v3 -> Blender -> downsample) | python | game-sprite | ✅ yes | RTX 5090; e2e trellis_v3 512 + --no-cleanup --no-mesh-gate --hdri = 8 sprites in 159.5s (mesh 117s, render 7s, downsample <1s) 2026-06-07. | · |
| Mesh-path 360 (image to 3D to multi-view) | Skip the v1-era trimesh cleanup for TRELLIS.2 (RAM trap) | python | turnaround | ✅ yes | RTX 5090, 64GB RAM; watchdog _watchdog.ps1 fired RAM>=90% (99%) during cleanup 2026-06-07; re-run with --no-cleanup --no-mesh-gate completed clean. | · |
| Mesh-path 360 (image to 3D to multi-view) | TRELLIS.2-4B image -> textured GLB on RTX 5090 (Blackwell) | trellis2 | turnaround | ✅ yes | RTX 5090 32GB, Win11, trellis2-env torch 2.10.0+cu130, ATTN_BACKEND=sdpa + grafted Blackwell sparse-attention (_sdpa_varlen), HF_HOME=E:/AI-Models/hf-cache. 512^3: gen 60s, gen-peak 3.4GB (allocator), 582k->482k verts, 35.9MB GLB. 1024_cascade: gen 37s, gen-peak 3.5GB, 2.26M->477k verts, 38.3MB GLB. Watchdog clean. | · |
| Render & lighting | Blender 5.0.1 headless 8-direction camera-parented light rig | blender | game-sprite | ✅ yes | Blender 5.0.1 headless on RTX 5090; 8 views ~7s; API probed 2026-06-07. | · |
| Render & lighting | Studio HDRI ambient fill (Studio Kontrast 04, CC0) | blender | game-sprite | ✅ yes | Rendered with + without HDRI, looked-at on the rig 2026-06-07. | · |
| Render & lighting | Tonemap per character value: AgX for dark, Standard for bright | blender | game-sprite | ✅ yes | 4-variant render compared + looked-at on the rig 2026-06-07. | · |
| Downsample & pixel finish | Lanczos 512->64px, foot-anchored, union-bbox | python | game-sprite | ✅ yes | Ran on the 8 Blender renders; 64px contact sheet looked-at 2026-06-07. | · |

## Recommended shortlist

Top `recommended` / `runner-up` picks per lane, by try-first order. `Evidence` ▣ measured-on-rig is the strongest tier.

| Lane | ↓ | Recipe | Engine | Applies | Evidence | Comm | ✓ |
|---|---|---|---|---|---|---|---|
| Mesh-path 360 (image to 3D to multi-view) | 1 | [1024_cascade vs 512 for thin features (5090)](mesh-360.md) | trellis2 | turnaround | ▣ measured | ✅ yes |  |
| Mesh-path 360 (image to 3D to multi-view) | 1 | [Re-pointed pipeline (generate_mesh_v3 -> Blender -> downsample)](mesh-360.md) | python | game-sprite | ▣ measured | ✅ yes |  |
| Mesh-path 360 (image to 3D to multi-view) | 1 | [Skip the v1-era trimesh cleanup for TRELLIS.2 (RAM trap)](mesh-360.md) | python | turnaround | ▣ measured | ✅ yes |  |
| Mesh-path 360 (image to 3D to multi-view) | 1 | [TRELLIS.2-4B image -> textured GLB on RTX 5090 (Blackwell)](mesh-360.md) | trellis2 | turnaround | ▣ measured | ✅ yes |  |
| Mesh-path 360 (image to 3D to multi-view) | 2 | [Step1X-3D (StepFun)](mesh-360.md) | comfyui | game-sprite | ▸ reproduced | ✅ yes |  |
| Mesh-path 360 (image to 3D to multi-view) | 2 | [TRELLIS.2-4B (Microsoft)](mesh-360.md) | comfyui | game-sprite | ▸ reproduced | ✅ yes |  |
| Mesh-path 360 (image to 3D to multi-view) | 2 | [TripoSG (VAST AI / Tripo)](mesh-360.md) | comfyui | game-sprite | ▸ reproduced | ✅ yes |  |
| Render & lighting | 1 | [Blender 5.0.1 headless 8-direction camera-parented light rig](render-light.md) | blender | game-sprite | ▣ measured | ✅ yes |  |
| Render & lighting | 1 | [Studio HDRI ambient fill (Studio Kontrast 04, CC0)](render-light.md) | blender | game-sprite | ▣ measured | ✅ yes |  |
| Render & lighting | 1 | [Tonemap per character value: AgX for dark, Standard for bright](render-light.md) | blender | game-sprite | ▣ measured | ✅ yes |  |
| Render & lighting | 2 | [Blender headless multi-direction render rig (--background + --python)](render-light.md) | blender | game-sprite | ▸ reproduced | ✅ yes |  |
| Render & lighting | 2 | [Color-management discipline: Standard/Raw (not AgX) for sprite albedo](render-light.md) | blender | both | ▸ reproduced | ✅ yes |  |
| Render & lighting | 2 | [Inverse-hull (backface solidify) outline for toon sprites](render-light.md) | blender | both | ▸ reproduced | ✅ yes |  |
| Render & lighting | 2 | [Normal / depth / AO passes for in-engine sprite re-lighting](render-light.md) | blender | both | ▸ reproduced | ✅ yes |  |
| Downsample & pixel finish | 1 | [Lanczos 512->64px, foot-anchored, union-bbox](downsample-finish.md) | python | game-sprite | ▣ measured | ✅ yes |  |
| Downsample & pixel finish | 2 | [Color quantization + dithering + palette discipline at small sizes](downsample-finish.md) | python | both | ▸ reproduced | ✅ yes |  |
| Downsample & pixel finish | 2 | [Supersample + Lanczos/area downsample (512 -> 48/64px)](downsample-finish.md) | python | both | ▸ reproduced | ✅ yes |  |
| Downsample & pixel finish | 6 | [Orthographic camera + foot-anchor (bottom-center) registration](downsample-finish.md) | blender | both | · community | ✅ yes |  |
| NVS-direct turnaround (no mesh) | 2 | [MV-Adapter](nvs-direct.md) | comfyui | turnaround | ▸ reproduced | ✅ yes | ✓ |
| Diffusion sprite-sheet direct | 2 | [ControlNet OpenPose pose-grid / concept-sheet (SDXL, thibaud)](sheet-direct.md) | comfyui | both | ▸ reproduced | ✅ yes | ✓ |
| Diffusion sprite-sheet direct | 2 | [PixelArtRedmond SDXL LoRA (artificialguybr)](sheet-direct.md) | comfyui | both | ▸ reproduced | ⚠ cond | ✓ |
| Diffusion sprite-sheet direct | 2 | [PixelLab.ai (commercial SaaS, native 4/8-direction + skeleton animation)](sheet-direct.md) | custom | both | ▸ reproduced | ✅ yes | ✓ |
| Diffusion sprite-sheet direct | 2 | [SDXL / Pony / Illustrious / NoobAI base-license axis (the inheritance rule)](sheet-direct.md) | comfyui | both | ▸ reproduced | ⚠ cond | ✓ |
| Diffusion sprite-sheet direct | 6 | [IP-Adapter FaceID + OpenPose identity-locked multi-pose](sheet-direct.md) | comfyui | both | · community | ⚠ cond | ✓ |
| Sprite evaluation / QA gate | 2 | [DISTS — structure+texture similarity (texture-substitution robust)](eval-qa.md) | python | both | ▸ reproduced | ✅ yes |  |
| Sprite evaluation / QA gate | 2 | [DreamSim — mid-level perceptual similarity for character identity](eval-qa.md) | python | both | ▸ reproduced | ⚠ cond |  |
| Sprite evaluation / QA gate | 2 | [LPIPS — learned perceptual patch similarity for downscale fidelity](eval-qa.md) | python | both | ▸ reproduced | ✅ yes |  |
| Sprite evaluation / QA gate | 2 | [MLLM-as-a-Judge — VLM rubric scoring & pairwise selection](eval-qa.md) | python | game-sprite | ▸ reproduced | ⚠ cond |  |
| Sprite evaluation / QA gate | 2 | [SigLIP 2 — zero-shot class/weapon/silhouette classifier](eval-qa.md) | python | both | ▸ reproduced | ✅ yes |  |
| Sprite evaluation / QA gate | 2 | [VQAScore (t2v_metrics) — grounded weapon/class/silhouette presence gate](eval-qa.md) | python | game-sprite | ▸ reproduced | ⚠ cond |  |
| Sprite evaluation / QA gate | 4 | [MEt3R — multi-view/turnaround 3D-consistency metric](eval-qa.md) | python | turnaround | · single-run | ⚠ cond |  |
| Sprite evaluation / QA gate | 4 | [Pixel-art-specific quality: palette adherence + grid/block-size consistency](eval-qa.md) | python | tile | · single-run | ✅ yes |  |
| Animation & locomotion | 2 | [Blender 3D-to-sprite locomotion pipeline (rig + orthographic multi-direction render)](animation-locomotion.md) | blender | animation | ▸ reproduced | ✅ yes |  |
| Animation & locomotion | 2 | [UniRig (VAST-AI / Tsinghua, SIGGRAPH 2025)](animation-locomotion.md) | blender | animation | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [A face starves below a hard pixel floor](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [A good seed does NOT transfer across different models or…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [A negative prompt is a CONCEPT to move away from, not a…](prompt-craft.md) | CLIP/T5/Qwen | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [A negative prompt is literally the CFG unconditional term…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [A negative prompt is not a 'filter](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [A negative should TARGET a specific observed defect, not…](prompt-craft.md) | CLIP/T5/Qwen | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [Before rewriting a prompt for a 'missing element', check CFG](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Both Qwen encoders are NATIVELY bilingual (CN/EN) and read…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [CFG SCALE is the dial on negative strength](prompt-craft.md) | CLIP/T5/Qwen | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [CFG controls HOW HARD the prompt steers the trajectory away…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [CFG scale — not the seed — is the dial for 'follow the…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [CLIP cannot do NEGATION in a positive prompt](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [CLIP is a 'bag of concepts' with weak grammar](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [CLIP's effective attention dies around token ~20, not token 77](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [CLIP's effective attention span is ~20 tokens, not 77](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [CLIP/OpenCLIP behave like a bag-of-words cross-modally](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [Cross-attention has a FIXED budget](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Describe what is VISIBLE, not what is TRUE' is forced by…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Distilled/turbo models (FLUX-dev, FLUX-schnell,…](prompt-craft.md) | CLIP/T5/Z-Image | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Encoder type dictates token-ORDER sensitivity](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [Even the SD1.5 negative embeddings are ANIME-trained on…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Even within 77 tokens, CLIP's EFFECTIVE length is only ~20…](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [FLUX splits labor](prompt-craft.md) | T5 | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Hard token limits differ wildly per encoder and ALL…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Identity does NOT come from the text encoder](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [LICENSE / commercial-safety of these embeddings is UNVERIFIED](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [LLM-based encoders (Qwen2.5-VL for Qwen-Image, Qwen3-4B for…](prompt-craft.md) | Qwen | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [NAG (Normalized Attention Guidance) restores real…](prompt-craft.md) | CLIP/T5/Z-Image | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Negative TEXTUAL-INVERSION embeddings (EasyNegative,…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [Negative prompts are a CFG mechanic, not a 'forbidden…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [Negatives bite LATE in sampling and only after the positive…](prompt-craft.md) | CLIP/T5/Qwen | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Negatives share the SAME 77-token CLIP budget as the positive](prompt-craft.md) | CLIP/T5 | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Non-depictable / narrative tokens DILUTE the embedding](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [On T5 (FLUX/Chroma), narrative/abstract prose is not 'free…](prompt-craft.md) | T5 | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [Once the prompt is RIGHT, run a BATCH of N seeds to explore…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [PAG (Perturbed-Attention Guidance) is the other…](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Qwen-Image is the trap](prompt-craft.md) | Qwen | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Qwen-Image silently prepends a FIXED system prompt and…](prompt-craft.md) | Qwen | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [Qwen-Image's REAL token budget is huge vs CLIP/T5](prompt-craft.md) | Qwen | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Qwen-Image's encoder is Qwen2.5-VL](prompt-craft.md) | Qwen | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Qwen-Image-Edit uses a DIFFERENT, instruction-shaped system…](prompt-craft.md) | Qwen | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [Qwen2.5-VL (Qwen-Image) and Qwen3-4B (Z-Image) are…](prompt-craft.md) | Qwen | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [Reference-conditioning (IP-Adapter/FaceID/InstantID) runs…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [SDXL feeds TWO 77-token CLIP encoders whose token features…](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [SDXL runs TWO CLIP encoders in parallel and concatenates them](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Stacking negatives can BACKFIRE and generate the very thing…](prompt-craft.md) | CLIP/T5/Qwen | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [T5 is a full encoder-decoder language model with a…](prompt-craft.md) | T5 | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [T5 truncation is SILENT](prompt-craft.md) | T5 | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [T5-XXL (FLUX/Chroma) gives token-level structure and…](prompt-craft.md) | T5 | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [T5-XXL in FLUX-dev/Chroma reads 512 tokens](prompt-craft.md) | T5 | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [T5-based diffusion models (FLUX, Chroma) do NOT respond to…](prompt-craft.md) | T5 | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [T5-based diffusion models do NOT respond to non-depictable…](prompt-craft.md) | T5 | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [The fix for high-CFG frying is Rescale-CFG (a.k.a. guidance…](prompt-craft.md) | CLIP/T5/Qwen | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [The giant 50-term 'worst quality, lowres, bad anatomy, bad…](prompt-craft.md) | CLIP/T5/Qwen | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [The hard ceiling is 77 tokens (75 content + start + end)](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [The negative token must itself be DEPICTABLE (the…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [The official 'positive magic' quality tail is a real,…](prompt-craft.md) | Qwen | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [The production loop is](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [The seed is the initial noise latent (z_T)](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [The seed only chooses the starting Gaussian noise latent](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [The seed only sets the START of the denoising trajectory…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [There is a PROVEN geometric ceiling](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes |  |
| Prompt craft & text encoders | 2 | [To A/B a prompt change cleanly, LOCK the seed and change…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Token limits are HARD and truncation is SILENT](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Whether a defect is even seed-fixable depends on the text…](prompt-craft.md) | CLIP | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Z-Image wraps prompts in a chat template and can run a…](prompt-craft.md) | Qwen | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [Z-Image's encoder is Qwen3-4B](prompt-craft.md) | Qwen | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 2 | [there is no UNIVERSAL magic/lucky seed. 'Golden' seeds…](prompt-craft.md) | all | both | ▸ reproduced | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [A fixed seed does NOT deliver character consistency across…](prompt-craft.md) | all | both | · community | ✅ yes |  |
| Prompt craft & text encoders | 6 | [A good seed does NOT survive a resolution change. Changing…](prompt-craft.md) | all | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [A weak/underspecified prompt produces a generic…](prompt-craft.md) | all | both | · community | ✅ yes |  |
| Prompt craft & text encoders | 6 | [Ancestral and SDE samplers (Euler a, DPM2 a, DPM++ 2S a,…](prompt-craft.md) | all | both | · community | ✅ yes |  |
| Prompt craft & text encoders | 6 | [BREAK and 75-token chunking are CLIP-ONLY plumbing](prompt-craft.md) | CLIP | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [BREAK starts a fresh 77-token chunk](prompt-craft.md) | CLIP | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [CFG scale ranges are model-family-specific and NOT…](prompt-craft.md) | all | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [Correct CFG range is model-family-specific](prompt-craft.md) | T5 | both | · community | ✅ yes |  |
| Prompt craft & text encoders | 6 | [Distilled/turbo models ignore negative prompts because…](prompt-craft.md) | CLIP/T5/Z-Image | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [Exact reproducibility requires the WHOLE stack to match,…](prompt-craft.md) | all | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [Longer prose helps T5 only up to a concrete-detail ceiling](prompt-craft.md) | T5 | both | · community | ✅ yes |  |
| Prompt craft & text encoders | 6 | [MINIMAL DEFENSIBLE DEFAULTS per family](prompt-craft.md) | all | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [On T5, punctuation is SEMANTIC](prompt-craft.md) | T5 | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [Per-encoder syntax differs](prompt-craft.md) | CLIP/T5/Qwen | both | · community | ✅ yes |  |
| Prompt craft & text encoders | 6 | [Prompt weighting (word:1.3) is a CLIP/embedding-scaling trick](prompt-craft.md) | all | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [Quality-WORD negatives ('worst quality, low quality,…](prompt-craft.md) | CLIP | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [Same seed + edited prompt = global structure preserved with…](prompt-craft.md) | all | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [Tag-style vs sentence-style is NOT a CLIP fact](prompt-craft.md) | CLIP | both | · community | ✅ yes |  |
| Prompt craft & text encoders | 6 | [The diagnostic: RIGHT KIND of thing, unlucky INSTANCE ->…](prompt-craft.md) | all | both | · community | ✅ yes |  |
| Prompt craft & text encoders | 6 | [The sampler determines the PATH from the seed's noise to…](prompt-craft.md) | all | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [The seed primarily fixes COMPOSITION, POSE, FRAMING, and…](prompt-craft.md) | all | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [There is a length sweet spot, and it is encoder-specific](prompt-craft.md) | all | both | · community | ✅ yes |  |
| Prompt craft & text encoders | 6 | [Token ORDER and front-loading materially change the image](prompt-craft.md) | CLIP | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [copy-pasted 50-80 word negative blocklists ('worst quality,…](prompt-craft.md) | all | both | · community | ✅ yes | ✓ |
| Prompt craft & text encoders | 6 | [long copy-pasted 'cargo' negatives ('deformed, ugly, poorly…](prompt-craft.md) | CLIP/T5/Qwen | both | · community | ✅ yes |  |

## Lanes

- [Mesh-path 360 (image to 3D to multi-view)](mesh-360.md) — Single image -> textured 3D mesh -> rendered multi-direction sprites. The recon-model landscape + the proven TRELLIS.2 path. (16 recipes)
- [Render & lighting](render-light.md) — Blender headless render: camera-parented rig, color-management/tonemap per character value, render passes, outline/toon. (9 recipes)
- [Downsample & pixel finish](downsample-finish.md) — 512px master -> 48/64px game sprite: Lanczos/area downscale, foot-anchor, union bbox, quantization/dithering, palette. (19 recipes)
- [NVS-direct turnaround (no mesh)](nvs-direct.md) — Image -> multiple consistent 2D views via multi-view diffusion / novel-view synthesis. License-decisive (Zero123 lineage is NC). (8 recipes)
- [Diffusion sprite-sheet direct](sheet-direct.md) — Text/image -> sprite sheet or 8-direction set directly via diffusion: charturn + pixel-art LoRAs, ControlNet pose sheets. (28 recipes)
- [Sprite evaluation / QA gate](eval-qa.md) — Grounded evaluators (SigLIP2/CLIP), turnaround-consistency + perceptual metrics, AI-judge gates for an automatable sprite verifier. (17 recipes)
- [Animation & locomotion](animation-locomotion.md) — Walk cycles / locomotion / frame sequences for sprites: auto-rig + animated render, image-to-animation diffusion, interpolation. (14 recipes)
- [Prompt craft & text encoders](prompt-craft.md) — How each text encoder (CLIP / T5 / Qwen) actually reads a prompt: token & character truncation limits, what it attends to, depictability, negative prompts, and the anti-patterns -- the rules that stop a session from prose-dumping an encoder. (104 recipes)

## Legend

- **↓** try-first order (lower = try first; derived from status + evidence strength).
- **Evidence** ▣ measured-on-rig > ▸ reproduced-from-source > · single-run / community / untested. The ordinal disciplines a single-reported claim from wearing the authority of an on-rig measurement. Proven (▣ measured-on-rig) vs research (everything else) is the spine of this KB.
- **Comm** commercial use of the OUTPUT: ✅ yes / ⚠ conditional / ⛔ no / ? unknown. A sprite inherits its base model's + recon model's license — the decisive axis (Zero123-lineage NVS is non-commercial).
- **Rig** fit 0–5 for this exact rig (RTX 5090 · 32 GB · Win 11 / WSL2). **Studio** fit 0–5 for commercial 2.5D JRPG sprite production.
- **✓** retrieval-verified this wave (existence + attribution + currency). Blank/· = unverified lead.
- **Boundary:** rig-measured it/s & VRAM peaks live in tensor-engine-knowledge (linked via `engine_recipe_ref`); base weights live in model-knowledge (linked via `base_model_slug`); never restated here.
