# Wave 6 — Chroma/Flux measurement (rank · flow-shift · fp8-vs-bf16)

> Measurement dispatch · 2026-06-07 · training-knowledge KB · the Chroma GPU pass (the priority loop's other half).

**Goal:** turn the wave-3 reproduced-from-source **Chroma/Flux** claims into measured-on-rig receipts by running them on the
RTX 5090 against the proven recipe — tensor-engine #168 `training-chroma-flux-lora-baseswap-cyanotype-recipe-5090`. The SDXL
half was measured in waves 4–5; this wave measures the saturated-palette base (Chroma1-HD, Apache-2.0, the #165 blue-ceiling
resolver).

**Constant (the #168 recipe):** `flux_train_network.py --model_type chroma`, `networks.lora_flux`, `--fp8_base`,
`--guidance_scale 0.0 --timestep_sampling sigmoid --model_prediction_type raw --apply_t5_attn_mask`, `--sdpa
--gradient_checkpointing --cache_latents` (NO `--cache_text_encoder_outputs`), `--dataset_config chroma_dataset.toml`
(16-img cyanotype + reg, trigger `stdstyl`), AdamW lr 1e-4, constant scheduler, 600 steps, seed 42. T5+ae passed, no clip_l.

**Method:** 5 real Chroma training runs on the RTX 5090, each capturing steady-state s/it + 1 Hz peak VRAM/RAM/**GPU-temp/power**
+ adapter size. Eval grids (10 held-out subjects × 2 seeds = 20/config) generated post-hoc and scored with the CLIP-sim/CMMD
harness, plus LOOKED-AT samples. **Oracle = the rig + looked-at grids + the eval harness — NOT the study-swarm adversarial
verifier.** A standalone health logger ran the whole campaign (peak 74 °C, mean 70 °C, peak 525 W, zero thermal throttle).

## A0 — the load-bearing inference finding (earned this wave)

The SDXL lycoris eval trick (kohya training-sampler `--sample_at_first`) **produces pure RGB noise for Chroma** — and so does
`flux_minimal_inference.py` at `cfg_scale 1.0`. Root cause: **Chroma needs real CFG** (`--cfg_scale ~4` + a negative prompt),
not the flux distilled-guidance-only path. The working, RAM-lean eval path: `flux_minimal_inference.py --model_type chroma
--flux_dtype fp8` (NO `--offload`; ~25–28 GB VRAM peak, ~30% system RAM), `--guidance 0 --cfg_scale 4 --negative_prompt
"blurry, low quality"`, 26 steps, LoRA strength **~3.0** (higher than #168's ComfyUI strength ~1.5 because this path does not
replicate ComfyUI's `ModelSamplingAuraFlow shift 1.0`). #168's own validation was always done in ComfyUI — kohya CLI Chroma
inference was never the proven path; this wave establishes a scriptable one.

## Runs (perf / VRAM / size / health — all measured)

| config | dim/alpha | shift | s/it | peak VRAM | peak temp | adapter |
|---|---|---|---|---|---|---|
| chroma_dim8 | 8 | 3.0 (default) | 2.67 | 18.8 GB | 74 °C | **53.5 MB** |
| chroma_dim16 (= shift 3.0) | 16 | 3.0 (default) | ~2.69 | 19.1 GB | 74 °C | **107.0 MB** |
| chroma_dim32 | 32 | 3.0 (default) | ~2.70 | 19.6 GB | 74 °C | **213.8 MB** |
| chroma_shift1 | 16 | 1.0 | ~2.76 | 19.4 GB | 74 °C | 107.0 MB |
| chroma_shift6 | 16 | 6.0 | ~2.76 | 19.6 GB | 74 °C | 107.0 MB |

**Perf + VRAM are flat across rank AND shift** (the 8.9B DiT forward dominates; the LoRA rank is tiny relative). So the rank
lever's only *training* cost is **adapter size** — linear: 53.5 → 107 → 214 MB per rank doubling. The flow-shift lever changes
the noise schedule, not the footprint. Whether rank/shift buy *fidelity* is the eval's question (see verification.md).

## fp8 vs bf16 base

Measured on this rig in the #167 baseline session (2026-06-03): **bf16 + live T5 SPILLS the 32 GB card** — VRAM pinned
**31974/32607 MiB**, step time ballooned **5 → 34 s/it** (WDDM paging GPU memory to system RAM) → `--fp8_base` REQUIRED
(~20 GB, 2.65–2.71 s/it, ~27 min/600 steps). **No fresh spill re-run** (Mike's call, 2026-06-07): the #167 data is a complete
A/B, and this wave's **5 fp8_base runs independently corroborate the fp8 side** (all sat 18.8–19.6 GB at 2.67–2.76 s/it, zero
spill, peak 74 °C). Supersedes the reproduced `flux-fp8-vs-bf16-base-precision-32gb`.

## Not measurable (recorded, not faked)

**`flux2-klein-4b-apache-undistilled-style-lora`** — the FLUX.2-klein base is NOT on the rig → cannot be run. Left
reproduced-from-source; flagged unmeasurable with the reason. No silent skip.

## Techniques folded (measured-on-rig, `engine_recipe_ref = training-chroma-flux-lora-baseswap-cyanotype-recipe-5090`)

1. Chroma rank/dim sweep — supersedes `flux-rank-dim-alpha-vs-sdxl`.
2. Chroma flow-shift sweep — supersedes `flux-shift-schedule-depth`.
3. Chroma fp8-vs-bf16 base — supersedes `flux-fp8-vs-bf16-base-precision-32gb`.
4. Chroma eval-grid inference method (the A0 finding) — the scriptable fp8 + real-CFG path.
