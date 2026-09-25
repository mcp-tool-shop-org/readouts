# Wave 6 — Verification receipt (Chroma measurement)

> The oracle is the rig + looked-at eval grids + the CLIP-sim/CMMD harness — NOT the study-swarm adversarial verifier · 2026-06-07.

## Perf / VRAM / size / health (all measured, 5 Chroma runs, #168 recipe, 600 steps, fp8_base)

| config | dim/alpha | shift | s/it | peak VRAM | peak temp | peak power | adapter |
|---|---|---|---|---|---|---|---|
| chroma_dim8 | 8 | 3.0 | 2.67 | 18.8 GB | 74 °C | 525 W | 53.5 MB |
| chroma_dim16 (= shift3) | 16 | 3.0 | ~2.69 | 19.1 GB | 74 °C | 525 W | 107.0 MB |
| chroma_dim32 | 32 | 3.0 | ~2.70 | 19.6 GB | 74 °C | 525 W | 213.8 MB |
| chroma_shift1 | 16 | 1.0 | 2.76 | 19.4 GB | 74 °C | 525 W | 107.0 MB |
| chroma_shift6 | 16 | 6.0 | 2.76 | 19.6 GB | 74 °C | 521 W | 107.0 MB |

Perf + VRAM flat across rank AND shift; adapter size linear in rank only. **Campaign health (742 samples / ~62 min): peak 74 °C, mean 70 °C, peak 525 W, zero thermal throttle, zero alerts** (standalone `_health_log.csv`).

## Eval (CLIP-sim to the 16-img cyanotype style centroid + CMMD, n=20 = 10 held-out subjects × 2 seeds)

| config | CLIP-sim ↑ | ±std | SEM | CMMD ↓ |
|---|---|---|---|---|
| shift6 | 0.7313 | 0.059 | 0.013 | 0.2148 |
| dim32 | 0.7224 | 0.070 | 0.016 | **0.1857** |
| dim16 (=shift3) | 0.7143 | 0.057 | 0.013 | 0.2197 |
| shift1 | 0.7127 | 0.060 | 0.013 | 0.2327 |
| dim8 | 0.7034 | 0.054 | 0.012 | 0.2175 |

All clear the ≥0.70 in-style bar (calibrated in wave 5). **Cross-base caveat:** the centroid is REAL cyanotype blue, so this is the correct *within-Chroma* reference — do NOT compare these absolute CLIP-sims to the SDXL panel's to rank bases (different generators, #165 vs Chroma palette).

## Looked-at (the decisive signal where CLIP-sim is noisy)

Same subject (ship, seed 42) across configs:
- **dim8** — naturalistic warm-hulled ship, blue only in the background: the saturated palette is **under-bound**.
- **dim16** — clear cyanotype: blue field + white-linework sails + canvas texture.
- **dim32** — **strongest**: uniform Prussian-blue field, white linework, the ship fully cyanotype. Matches its best CMMD (0.186).
- **shift1** — more naturalistic/textured; **shift6** — clean deep-blue field (matches its top CLIP-sim).
- Isolated subjects (portrait, owl) render as white-engraving on a dark field (clean cyanotype linework), not the #167 white-bg — a flux_minimal_inference-path difference, consistent across configs.

**Finding (differs from SDXL):** for Chroma's saturated-palette base-swap, **rank capacity carries the global palette transform** — dim8 leaves it naturalistic, dim32 fully binds it (CMMD + eyes agree; CLIP-sim monotonic at ~1 SEM/step). SDXL style (wave 4/5) was rank-neutral; this is not. The cost is adapter size (53/107/214 MB). Shift is the weakest lever (shift6 marginally best, within noise). **Methodology note:** for a global-palette question, CMMD + looked-at separated the configs where CLIP-ViT-B/32 cosine alone was within the noise floor at n=20.

## fp8 vs bf16 base

bf16 + live T5 spills (31974/32607 MiB, 34 s/it via WDDM paging — measured #167, 2026-06-03); `--fp8_base` required (~20 GB, 2.65–2.71 s/it). **No fresh spill re-run** (Mike's call) — #167 is a complete A/B and this wave's 5 fp8 runs corroborate the fp8 side (18.8–19.6 GB).

## Not measurable (recorded, not faked)

**`flux2-klein-4b-apache-undistilled-style-lora`** — FLUX.2-klein base is NOT on the rig → cannot be run. Stays reproduced-from-source; flagged here + in memory. No silent skip, no measured tag.

## Provenance

5 Chroma rig runs on the RTX 5090, 2026-06-07. Every measured technique carries `evidence_strength=measured-on-rig` + `engine_recipe_ref=training-chroma-flux-lora-baseswap-cyanotype-recipe-5090` + the receipt + the looked-at grids in `E:/AI/training/eval_grid_chroma/`. Eval JSON `E:/AI/training/_eval_chroma.json`. 3 wave-3 research techniques superseded (flux-rank-dim-alpha-vs-sdxl, flux-shift-schedule-depth, flux-fp8-vs-bf16-base-precision-32gb) + 1 net-new eval-inference method.
