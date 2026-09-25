# Wave 1 — Sprite recipe & model landscape (study swarm)

**Date:** 2026-06-07 · **Agents:** 12 (6 research + 6 adversarial verify) · **Recipes:** 53 (52 verified) · **Decisive axis:** `commercial_use`

Six web-grounded research lanes, each run through a different-lens adversarial retrieval-verifier (sources WebFetched, licenses corrected). `render-finish-craft` was split into `render-light` + `downsample-finish` on load. evidence_strength is research-level (reproduced-from-source / community-claim) — the on-rig-measured half is wave 0.

## Findings by lane

**mesh-360 (9)** — the recon-model landscape behind our proven TRELLIS.2 lane.
- Commercial-clean leaders: **TRELLIS.2-4B (MIT)**, **Step1X-3D (Apache-2.0, built-in LoRA)**, **TripoSG**. These ship clean and a style LoRA inherits the permissive base.
- License hazards: **Hunyuan3D-2.1** is top-quality but *conditional* — &lt;1M MAU AND its grant **excludes EU/UK/South Korea** (disqualifying for a worldwide release without legal sign-off). SF3D/Hi3DGen conditional; **Sparc3D is non-commercial → avoid** for shipped assets.

**render-light (5)** — corroborates wave-0: **Standard/Raw, not AgX, for sprite albedo**. Plus inverse-hull (backface-solidify) outline, Freestyle/Line-Art outline pass, and **normal/depth/AO passes for in-engine re-lighting** (so a flat sprite can take dynamic light).

**downsample-finish (4)** — **supersample + Lanczos/area** 512→48/64; the **Hiive adaptive pixel-art downscaler** (majority-block, edge-preserving) for a true pixel look; quantization + dithering + palette discipline at small sizes; orthographic camera + **foot-anchor registration** (matches wave-0).

**nvs-direct (8)** — the mesh-free turnaround lane. **MV-Adapter is the ONE commercial-clean option** (Apache, SDXL/anime base). The entire **Zero123 lineage is non-commercial** (Zero123++, Era3D → avoid; Stable-Zero123, SV3D, Hunyuan3D-2mv → conditional). Confirms the studio's mesh-path-over-NVS verdict on license grounds.

**sheet-direct (9)** — diffusion-native sheets: **PixelArtRedmond** + Pixel-Art-XL LoRAs, **ControlNet OpenPose pose-grids**, **IP-Adapter FaceID** for identity-locked multi-pose, **FLUX.1 Kontext** single-image→5-view turnaround, and **PixelLab.ai** (SaaS, native 4/8-direction). The load-bearing note: the **base-license inheritance rule** (SDXL/Pony/Illustrious/NoobAI) decides commercial fate.

**eval-qa (9)** — an automatable verifier gate: **VQAScore** + **SigLIP 2** (weapon/class/silhouette presence), **MEt3R** (multi-view/turnaround consistency), **LPIPS / DISTS / DreamSim** (downscale + identity fidelity), MLLM-as-judge, and pixel-art-specific palette/grid metrics. This is the candidate gate for the sprite pipeline (ties to ai-eyes-mcp).

**animation-locomotion (9)** — rig + render: **UniRig (SIGGRAPH 2025)**, AccuRIG, Mixamo, Auto-Rig Pro → animate a TRELLIS mesh and render an 8-direction locomotion set; plus **AnimateDiff** and **RIFE / FILM** interpolation for in-betweens.

## Cross-lane through-line
License is destiny: the commercial-clean spine is **TRELLIS.2/Step1X-3D (mesh) → Blender render (Standard tonemap, outline, passes) → Lanczos/pixel downscale → SigLIP2/VQAScore gate**, with **MV-Adapter** as the only clean mesh-free alternative and base-model license inheritance governing every LoRA.
