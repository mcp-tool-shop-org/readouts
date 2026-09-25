# Wave 0 — Local seed: TRELLIS.2 sprite pipeline proven on the RTX 5090

**Date:** 2026-06-07 · **Type:** local (no research swarm) · **Lanes:** mesh-360, render-light, downsample-finish

This wave is not a study swarm — it is the **measured-on-rig** seed: recipes the studio executed end-to-end and looked at on 2026-06-07, during the trellis-sprite-pipeline bring-up. Everything here carries `evidence_strength = measured-on-rig` and `verified = 1` (the receipt is the actual run, not a citation).

## What was proven

**mesh-360**
- `trellis2-4b-rtx5090-image-to-glb` — TRELLIS.2-4B turns one front image into a textured GLB on the 5090 via a dedicated torch-2.10+cu130 venv (NOT the ComfyUI node), `ATTN_BACKEND=sdpa` + grafted Blackwell sparse-attention, ungated BiRefNet for input bg-removal. 512³: gen 60s, ~3.4 GB peak. 1024_cascade: gen 37s, ~3.5 GB. Commercial-clean (mesh is MIT).
- `trellis2-1024-cascade-vs-512-thin-features` — 1024_cascade is visibly sharper (face, armor, folds) at ~identical VRAM/time; thin staff survives at both; head-side smear is a single-view *data* limit, not resolution. The ~24 GB OOM fear was 5080-era.
- `trellis2-skip-v1-cleanup-ovoxel-is-clean` — clean_mesh + the mesh-gate's `trimesh.split()` on a 1M-face/4096² mesh is a system-RAM hog that tripped the aborting watchdog at 99% RAM. TRELLIS.2 O-Voxel meshes are clean → skip cleanup (`--no-cleanup --no-mesh-gate`).
- `sprite-pipeline-trellis-v3-end-to-end` — `pipeline.py --backend trellis_v3` (new `generate_mesh_v3.py`, direct trellis2-env call) → mesh → Blender 8-dir → 64px downsample = **8 sprites in 159.5s**, no ComfyUI.

**render-light**
- `blender-headless-8dir-camera-parented-rig` — camera-parented 3-point + shadowless lens-fill rig on **Blender 5.0.1** (installed this session); the bpy API verified compatible (`BLENDER_EEVEE` is valid in 5.0).
- `tonemap-per-character-value` — AgX+exposure washes out bright characters; **Standard + exposure 0** restores saturation. A/B/C/D proven; added a `--view-transform` flag. Per-character choice (AgX for dark villains, Standard for bright).
- `studio-hdri-ambient-fill` — CC0 Studio Kontrast 04 HDRI for directional form; flat-ambient fallback works.

**downsample-finish**
- `lanczos-512-to-64-foot-anchored` — auto-crop → union-bbox → foot-anchor → Lanczos → unsharp → contact sheet; 8× 64px game sprites, consistent framing.

## Receipts
Work tree: `E:/AI/trellis-work/` (input, mesh, preview, sprites, `_OUTBOX/generic-mage-knight/`). Code: `mcp-tool-shop-org/trellis-sprite-pipeline` (`generate_mesh_v3.py`, `pipeline.py`, `render_views.py`, `downsample_sprites.py`). Full recipe context in memory `trellis2-5090-recipe.md`.
