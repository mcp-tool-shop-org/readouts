# readouts — training-knowledge

> Verified knowledge base of portable TRAINING CRAFT — methods, recipes, hyperparameter values, dataset & eval know-how — for training LoRAs / fine-tunes on the single RTX 5090 (Blackwell / Windows / WSL2) rig. The how-to-train layer between the weights (model-knowledge) and the software (tensor-engine-knowledge).
>
> **204 techniques · 101 verified · 432 sources · 16 waves · generated 2026-09-25.**  
> Decisive axis: single-RTX-5090 training viability + reproducibility (fits 32 GB, commercial-clean output, complete replay provenance) — which method/recipe/data/eval you feed the engine and why, not which weights or which software.

## Domains

| Domain | Techniques | Verified | Top pick | License | Readout |
|---|--:|--:|---|---|---|
| PEFT methods & adapter theory | 37 | 6/37 | LoRA: rank and alpha as a coupled scaling pair (alpha/rank = effective-LR multiplier) | commercial | [`readout-peft-methods.html`](readout-peft-methods.html) |
| SDXL style-LoRA recipes (priority) | 19 | 19/19 | AdamW8bit SDXL LoRA — MEASURED (no VRAM saving for LoRA; ~4% faster than fp32) | commercial | [`readout-diffusion-sdxl-lora.html`](readout-diffusion-sdxl-lora.html) |
| Flux-family style-LoRA recipes | 14 | 14/14 | Chroma discrete_flow_shift sweep (1/3/6) — MEASURED (footprint-neutral; shift 6 marginally best fidelity; weakest lever) | commercial | [`readout-diffusion-flux-lora.html`](readout-diffusion-flux-lora.html) |
| Dataset construction & caption craft | 17 | 11/17 | Augmentation safety policy (flip / random-crop / color) for style sets | commercial | [`readout-dataset-caption.html`](readout-dataset-caption.html) |
| Local LLM fine-tuning (SFT + preference + RL) | 19 | 15/19 | DPO (LoRA) preference tuning (stage 2) — paired data, needs ref model | conditional | [`readout-llm-finetune.html`](readout-llm-finetune.html) |
| Single-GPU efficiency & training-VRAM technique | 12 | 5/12 | gradient_checkpointing is mandatory for lycoris.kohya LoRA on 32 GB (MEASURED 27.7 -> 14.5 GB) | commercial | [`readout-efficiency.html`](readout-efficiency.html) |
| Training evaluation & validation methodology | 44 | 11/44 | Diffusion style-fidelity eval panel — MEASURED (CLIP-sim + CMMD, n=20) on the wave-4 SDXL LoRAs | commercial | [`readout-evaluation.html`](readout-evaluation.html) |
| Failure modes & debugging | 4 | 4/4 | Catastrophic forgetting: LoRA as the regularizer, plus the rank/effective-LR/replay levers | commercial | [`readout-debugging.html`](readout-debugging.html) |
| Diffusion Qwen Lora | 5 | 5/5 | Clean (on-canon) dataset = no late embedding-cloud collapse — 3rd cross-run confirmation; pick the ship checkpoint by geometry, not CLIP-sim | commercial | [`readout-diffusion-qwen-lora.html`](readout-diffusion-qwen-lora.html) |
| Still Current | 22 | 0/22 | Calendar Versioning (CalVer) | — | [`readout-still-current.html`](readout-still-current.html) |
| Trl Grpo Mechanics | 4 | 4/4 | clip_ratio is identically zero at the default num_iterations=1 | commercial | [`readout-trl-grpo-mechanics.html`](readout-trl-grpo-mechanics.html) |
| Rl Measurement Methodology | 4 | 4/4 | Generations per item, not items, is usually the cheap lever on eval power | commercial | [`readout-rl-measurement-methodology.html`](readout-rl-measurement-methodology.html) |
| Rlvr Sharpening And Latent Capability | 3 | 3/3 | An RLVR pass-rate lift is not licensed to be called new capability | commercial | [`readout-rlvr-sharpening-and-latent-capability.html`](readout-rlvr-sharpening-and-latent-capability.html) |

## Install-first shortlist (recommended, by KB download priority)

1. **AdamW8bit SDXL LoRA — MEASURED (no VRAM saving for LoRA; ~4% faster than fp32)** (SDXL style-LoRA recipes (priority)) — commercial
2. **Checkpoint selection — MEASURED: best != last (peak ~600, plateau 450-900; <=150 undertrains)** (SDXL style-LoRA recipes (priority)) — commercial
3. **Chroma discrete_flow_shift sweep (1/3/6) — MEASURED (footprint-neutral; shift 6 marginally best fidelity; weakest lever)** (Flux-family style-LoRA recipes) — commercial
4. **Chroma LoRA eval/inference on the rig — kohya samplers give NOISE; use flux_minimal_inference fp8 + REAL CFG (the scriptable path)** (Flux-family style-LoRA recipes) — commercial
5. **Chroma LoRA rank/dim sweep (8/16/32) — MEASURED on the 5090 (size linear; higher rank binds the saturated palette more completely — unlike SDXL)** (Flux-family style-LoRA recipes) — commercial
6. **Chroma1-HD base-swap style-LoRA (kohya flux_train_network --model_type chroma) — measured on the 5090** (Flux-family style-LoRA recipes) — commercial
7. **Clean (on-canon) dataset = no late embedding-cloud collapse — 3rd cross-run confirmation; pick the ship checkpoint by geometry, not CLIP-sim** (Diffusion Qwen Lora) — commercial
8. **clip_ratio is identically zero at the default num_iterations=1** (Trl Grpo Mechanics) — commercial
9. **Diffusion style-fidelity eval panel — MEASURED (CLIP-sim + CMMD, n=20) on the wave-4 SDXL LoRAs** (Training evaluation & validation methodology) — commercial
10. **DPO (LoRA) preference tuning (stage 2) — paired data, needs ref model** (Local LLM fine-tuning (SFT + preference + RL)) — conditional
11. **fp8_base is REQUIRED for Chroma LoRA on 32 GB — bf16 + live T5 spills the card (MEASURED 31974 MiB / 34 s/it)** (Flux-family style-LoRA recipes) — commercial
12. **Generations per item, not items, is usually the cheap lever on eval power** (Rl Measurement Methodology) — commercial
13. **gradient_checkpointing is mandatory for lycoris.kohya LoRA on 32 GB (MEASURED 27.7 -> 14.5 GB)** (Single-GPU efficiency & training-VRAM technique) — commercial
14. **min_snr_gamma 5 — MEASURED fidelity win for SDXL style-LoRA (+0.049 CLIP-sim, ~2.3 SEM)** (SDXL style-LoRA recipes (priority)) — commercial
15. **Multi-concept repeat-balancing — MEASURED: distinct triggers protect own-fidelity; imbalance shows as cross-bleed, not collapse** (SDXL style-LoRA recipes (priority)) — commercial
16. **Network-type choice for SDXL style — MEASURED 3-way (DoRA +52% time / LoKr 6 MB)** (SDXL style-LoRA recipes (priority)) — commercial
17. **noise_offset 0.1 breaks the SDXL #165 blue-ceiling — MEASURED (+0.049 CLIP-sim, ~2.3 SEM); ztsnr neutral-to-worse on eps-pred SDXL** (SDXL style-LoRA recipes (priority)) — commercial
18. **Pooled eval statistics measure the item mix as well as the behaviour** (Rl Measurement Methodology) — commercial

## Go deeper

- **Per-domain readout:** `readout-<slug>.html` — filterable table + sources + verify trail
- **Wave dispatches** (research log): `waves.md` / `waves.html`
- **Verification receipt** (trust trail): `verification.md` / `verification.html`
- **Query the DB:** `training.db (views v_recommended, v_best_for; FTS techniques_fts)`
- **Resolve via loadout:** `ai-loadout resolve --project ./training-knowledge`
- **Programmatic map:** `index.json`

## Provenance

Every fact carries a **wave id** and a **verified** flag; sources are retrieval-checked by a different-family verifier. 16 waves; 101/204 techniques verified.
