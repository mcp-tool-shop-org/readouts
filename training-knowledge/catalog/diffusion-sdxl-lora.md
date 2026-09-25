# SDXL style-LoRA recipes (priority)
_The studio #1 workload: full hyperparameter recipes for SDXL-family style LoRAs (kohya/ComfyUI as engine references only). rank+alpha, optimizer<->LR, booru-tag captioning + style-tag pruning, regularization, 1024px bucketing, repeats/epochs, min-SNR-gamma, per-rank quality signature._ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

19 techniques · 12 recommended · 9 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 1 | AdamW8bit SDXL LoRA — MEASURED (no VRAM saving for LoRA; ~4% faster than fp32) | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Checkpoint selection — MEASURED: best != last (peak ~600, plateau 450-900; <=150 undertrains) | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Multi-concept repeat-balancing — MEASURED: distinct triggers protect own-fidelity; imbalance shows as cross-bleed, not collapse | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Network-type choice for SDXL style — MEASURED 3-way (DoRA +52% time / LoKr 6 MB) | lokr | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Prodigy SDXL style-LoRA — MEASURED on the 5090 (auto-LR works; ~1.8-2x the per-step cost of AdamW) | lora | diffusion | ▣ measured | ✅ yes | 4 | 5 | ✓ |
| 1 | SDXL style-LoRA with text-encoder + non-word trigger token (+ optional regularization gating) | lora | diffusion | ▣ measured | ⚠ cond | 5 | 5 | ✓ |
| 1 | SDXL style-LoRA, UNet-only baseline (kohya/sd-scripts, dim16/alpha8, AdamW @1e-4 constant, 1024px bf16) | lora | diffusion | ▣ measured | ⚠ cond | 5 | 5 | ✓ |
| 1 | min_snr_gamma 5 — MEASURED fidelity win for SDXL style-LoRA (+0.049 CLIP-sim, ~2.3 SEM) | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | noise_offset 0.1 breaks the SDXL #165 blue-ceiling — MEASURED (+0.049 CLIP-sim, ~2.3 SEM); ztsnr neutral-to-worse on eps-pred SDXL | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 2 | Adapter post-processing: merge-into-checkpoint, SVD resize/dim-reduction, extraction | lora | diffusion | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 2 | Booru-tag captioning with style-tag pruning + non-word trigger (style-LoRA curation) | lora | diffusion | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 2 | Checkpoint selection: save cadence + sample-during-training + best-epoch eval grid | lora | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Multi-concept / multi-folder repeat-balancing + token separation (SDXL) | lora | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Network-type choice for SDXL style: LoRA vs LoCon vs LoKr vs DoRA | lycoris | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Prodigy parameter-free optimizer for SDXL style LoRA (LR=1.0 sentinel) | lora | diffusion | ▸ reproduced | ✅ yes | 4 | 5 | ✓ |
| 4 | AdamW8bit + cosine-with-warmup schedule for SDXL LoRA (warmup as first-class axis) | lora | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 4 | Min-SNR-gamma loss weighting (gamma=5) for SDXL LoRA | lora | diffusion | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 6 | Inference-validation settings for a fresh SDXL style LoRA (weight/CFG/sampler/steps) | lora | diffusion | · community | ✅ yes | 5 | 5 | ✓ |
| 6 | Noise/schedule levers for SDXL style LoRA: noise_offset + zero-terminal-SNR (with min_snr_gamma) | lora | diffusion | ▸ reproduced | ✅ yes | 4 | 4 | ✓ |

## Detail

### AdamW8bit SDXL LoRA — MEASURED (no VRAM saving for LoRA; ~4% faster than fp32) · `recommended` · ▣ measured
**MEASURED on the 5090: AdamW8bit is ~4% FASTER than fp32 AdamW (1.52 vs 1.46 it/s) but gives essentially NO VRAM saving for LoRA (19.7 vs 19.4 GB) — a LoRA's optimizer state is already tiny, so 8-bit quantizing it saves nothing (bitsandbytes block overhead even nudges it up). The 8-bit VRAM win is full-fine-tune-only.**
Run 2, 600 steps, matched to #166 v2 (swap optimizer fp32->8bit + schedule constant->cosine+warmup): 1.52 it/s, peak 19.7 GB, loss 0.105, style bound across ship/loco/portrait at 600 (quality parity). Corrects the wave-3 'AdamW8bit roughly halves optimizer-state VRAM -> more headroom for higher rank/res' claim for the LoRA case.
- **For the pipeline:** Use AdamW8bit as a small free speedup. Do NOT cite it as a memory lever to fit higher rank/resolution for LoRA — it isn't. For real LoRA VRAM headroom use gradient_checkpointing (measured -13 GB on the lycoris path).
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Seed:** 42 · **Runs:** 1
- **Validated under:** RTX 5090 32GB; SDXL base 1.0; stdstyl set; dim16/alpha16 TE-on no-reg; AdamW8bit; cosine+30-warmup; bf16 sdpa cache_latents; 600 steps. 2026-06-06.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-proven-blackwell-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — output license = base + dataset.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| optimizer | AdamW8bit | ● |  |
| learning_rate | 1e-4 | ● |  |
| scheduler | cosine | ○ |  |
| warmup | 30 steps | ○ |  |
| network_dim | 16 | ○ |  |
| alpha | 16 | ○ |  |
| steps | 600 | ○ |  |
| measured_it_s | 1.52 it/s | ○ | vs fp32 AdamW 1.46 |
| measured_peak_vram | 19.7 GB | ○ | vs fp32 19.4 — NO saving |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| expected VRAM drop from AdamW8bit didn't materialize (LoRA) | LoRA optimizer state already negligible; 8-bit block overhead | don't rely on AdamW8bit for LoRA headroom; use gradient_checkpointing | optimizer |

- **Best for:** small free speedup at a known LR (sdxl, fit 4)
- **Verify:** verdict=confirmed | currency=measured 2026-06-06 | direct rig measurement + looked-at samples
- **Sources:** [training-knowledge wave-4 measurement (AdamW8bit Run 2)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured RTX 5090 2026-06-06; samples looked-at ; [bitsandbytes 8-bit optimizers](https://arxiv.org/abs/2110.02861) (Dettmers et al., 2022) — 8-bit optimizer states cut memory for the optimizer — material only when optimizer state is large (full FT), not LoRA

### Checkpoint selection — MEASURED: best != last (peak ~600, plateau 450-900; <=150 undertrains) · `recommended` · ▣ measured
**MEASURED on the 5090 (one run, noise_offset 0.1, 900 steps, save every 150, eval each checkpoint n=20): the BEST checkpoint is step 600 (CLIP-sim 0.7865), NOT the last (900 = 0.7818). Fidelity rises to a peak by ~450-600 then PLATEAUS / marginally declines (450/600/750/900 all ~0.78, within noise). At step 150 the style binds but UNDERTRAINS visibly — the trigger leaks as literal 'STDSYL' text (looked-at). So picking the final checkpoint is wrong, and training past ~600 wastes compute on a 16-img set.**
Confirms the checkpoint-selection thesis on the rig: save intermediate checkpoints and pick by eval rather than assuming the last is best. The curve: 150 (0.7727, undertrained text artifact) -> 300 (0.7595 dip) -> 450 (0.7817) -> 600 (0.7865, peak) -> 750 (0.7842) -> 900 (0.7818). Style binds fast (StyleDrop) but the trigger absorbs into style only by ~450-600.
- **For the pipeline:** Save every ~150 steps and EVAL each checkpoint; pick the peak (here ~600), don't default to the last. For a 16-img SDXL style-LoRA, ~450-600 steps is sufficient; >=900 is past the peak with no fidelity gain. Treat a visible trigger-as-text artifact as an undertraining signal.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Seed:** 42 · **Runs:** 1 · **Search:** single run, 6 checkpoints, eval each n=20 + looked-at
- **Variance:** n=20/checkpoint, SEM ~0.015; 600-vs-900 ~within noise -> 'plateau then marginal decline'.
- **Validated under:** RTX 5090; SDXL base 1.0; stdstyl 16-img; dim16; AdamW lr 1e-4 cosine+warmup; noise_offset 0.1; 900 steps save_every 150. 2026-06-07.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-proven-blackwell-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes**
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| best_checkpoint | step 600 (CLIP-sim 0.7865) | ○ | NOT the last (900=0.7818) |
| curve | 150:0.7727 300:0.7595 450:0.7817 600:0.7865 750:0.7842 900:0.7818 | ○ |  |
| save_every_n_steps | 150 | ○ | cadence to capture the peak |
| undertraining_signal | trigger renders as literal text at ~150 steps | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| final checkpoint isn't the best / overtrained | fidelity plateaus/declines after ~600 steps on a 16-img set | save every N + pick the peak by eval | save_every_n_steps |
| trigger token appears as literal text in outputs | undertraining (~150 steps) | train to ~450-600 so the trigger absorbs into style | max_train_steps |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | CLIP-sim-to-style-centroid | 0.7865 | >=0.70 | ✓ | clip-vit-b32 |

- **Best for:** pick the best style-LoRA checkpoint (not the last) (sdxl, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-07 | rig + per-checkpoint n=20 + looked-at; best=600 != last=900
- **Sources:** [training-knowledge wave-7 B2 checkpoint curve (6 checkpoints, n=20)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured 2026-06-07; _stdstyl_ckpt_result.txt + _eval_ckpt.json + looked-at ; [StyleDrop: Text-to-Image Generation in Any Style](https://arxiv.org/abs/2306.00983) (Sohn et al., 2023) — a coherent style binds from very few images / few steps — grounds the fast-binding + early-plateau (Stage-2 PARTIAL: '<1% params/few imgs' supported, '16 ample' is our extrapolation)

### Multi-concept repeat-balancing — MEASURED: distinct triggers protect own-fidelity; imbalance shows as cross-bleed, not collapse · `recommended` · ▣ measured
**MEASURED on the 5090: ONE SDXL LoRA jointly trained on two well-separated concepts (A=cyanotype 'stdstyl', B=warm impasto-oil 'oilpst', 16 imgs each, noise_offset 0.1, 1600 steps), sweeping the num_repeats ratio 10:10 / 30:10 / 10:30 (= effective exposure 1:1 / 3:1 / 1:3). RESULT: BOTH concepts keep high own-fidelity (A 0.774-0.794, B 0.771-0.784) across ALL ratios (spreads ~1 SEM) — no concept collapse even at 3:1. The dominance signature is in CROSS-BLEED: B-dominant shows the highest A->B bleed (cyanotype outputs picking up warm-oil character, 0.678) and the lowest B->A bleed (oilpst outputs purest, 0.675); A-dominant the reverse. Looked-at confirms: the dominated concept keeps its identity but takes a subtle tint of the dominant style.**
The study-swarm-grounded design (distinct rare triggers + a maximally-separable concept B + num_repeats as the lever, no reg) produced a clean, interpretable measurement. H4 (distinct triggers prevent token collapse) and H3 (dominance -> cross-bleed) supported; the naive H1 own-fidelity trade-off is WEAKER than predicted at these ratios/steps — distinct triggers + adequate capacity (dim16) + 1600 steps let both concepts co-train robustly through moderate (<=3:1) imbalance. The cross-centroid CLIP gap (own 0.77-0.79 >> cross 0.65-0.70) confirms the concepts are genuinely separated.
- **For the pipeline:** For 2-concept SDXL LoRA training: give each concept a distinct RARE trigger and pick concepts that are visually separable; then moderate repeat imbalance (<=3:1) does NOT starve a concept's core identity (own-fidelity holds) — it only tints the under-represented concept's outputs with the dominant style (cross-bleed). Balance num_repeats to ~1:1 effective exposure to minimize that tint; reach for merge-time fixes (ZipLoRA/gradient-fusion) only if single-LoRA bleed is unacceptable.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Seed:** 42 · **Runs:** 3 · **Tuning budget:** 3 ratio configs (study-swarm experimental design) · **Search:** num_repeats ratio sweep, dual-trigger eval n=20 each + cross-bleed + looked-at
- **Variance:** n=20/config/trigger, SEM ~0.015; own-fidelity spreads across ratios ~1 SEM (no collapse); cross-bleed differences ~0.02-0.03, directional + looked-at-confirmed.
- **Validated under:** RTX 5090; SDXL base 1.0; concept A cyanotype + concept B impasto-oil (16 imgs each); networks.lora dim16; AdamW lr 1e-4 cosine+warmup; noise_offset 0.1; 1600 steps; NO reg; num_repeats 10:10/30:10/10:30. Eval dual-trigger vs two CLIP centroids + cross. 2026-06-07.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-proven-blackwell-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — concept B synthetic from SDXL base (OpenRAIL++-M); output license = base + dataset.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| balanced_10:10 | A_fid 0.7738 / B_fid 0.7710 / A->B 0.6489 / B->A 0.6984 | ○ |  |
| A_dominant_30:10 | A_fid 0.7793 / B_fid 0.7787 / A->B 0.6541 / B->A 0.7000 | ○ | B->A bleed highest -> oilpst tinted cool |
| B_dominant_10:30 | A_fid 0.7937 / B_fid 0.7843 / A->B 0.6783 / B->A 0.6751 | ○ | A->B bleed highest -> cyanotype tinted painterly |
| own_vs_cross_gap | own 0.77-0.79 >> cross 0.65-0.70 | ○ | concepts genuinely separated |
| num_repeats_lever | effective exposure = imgs x repeats; ratio is the lever | ● |  |

- **Datasets:** oilpst — warm impasto-oil style concept (synthetic, SDXL base 1.0) (concept-b, license CreativeML OpenRAIL++-M (inherits SDXL base 1.0; royalty-free commercial use, Licensor claims no rights over generated outputs))

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| the over-represented concept's style tints the other concept's outputs | num_repeats imbalance (cross-bleed; the dominated concept keeps identity but takes a tint) | balance num_repeats to ~1:1 effective exposure; distinct triggers already prevent full collapse | num_repeats |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | A-fidelity (cyanotype centroid) | 0.7738 | >=0.70 | ✓ | clip-vit-b32 |
| diffusion-style | B-fidelity (oilpst centroid) | 0.7710 | >=0.70 | ✓ | clip-vit-b32 |

- **Best for:** train two distinct styles into one SDXL LoRA without collapse (sdxl, fit 5) ; understand how num_repeats imbalance manifests (cross-bleed) (sdxl, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-07 | rig + dual-trigger n=20 + cross-bleed + looked-at; study-swarm-grounded concept B, Stage-1+Stage-2 citation-verified (1 source dropped on Stage-2)
- **Sources:** [training-knowledge wave-7 B3 multi-concept repeat-balancing (3 ratios, dual-trigger n=20 + cross-bleed + looked-at)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured 2026-06-07; _mc_{balanced,adom,bdom}_result.txt + _eval_multiconcept.json ; [Multi-Concept Customization of Text-to-Image Diffusion (Custom Diffusion)](https://arxiv.org/abs/2212.04488) (Kumari et al., 2023) — distinct per-concept modifier tokens let concepts co-train without collapse — grounds the distinct-trigger design (Stage-1 real; Stage-2 textbook) ; [kohya-ss sd-scripts num_repeats (per-folder effective exposure)](https://github.com/kohya-ss/sd-scripts/blob/main/docs/config_README-en.md) (kohya-ss, 2024) — per-epoch exposure = image_count x num_repeats; the balancing lever — Stage-2 SUPPORTED (mistral+granite) ; [Implicit Style-Content Separation using B-LoRA](https://arxiv.org/abs/2403.14572) (Frenkel et al., 2024) — SDXL style/content block separation — grounds the maximally-separable concept-B choice; Stage-2 SUPPORTED

### Network-type choice for SDXL style — MEASURED 3-way (DoRA +52% time / LoKr 6 MB) · `recommended` · ▣ measured
**MEASURED 3-way on the 5090 (lycoris.kohya, same codepath, gradient-checkpointed, matched dim16/600-step): plain LoRA 1.06 s/it / 121.8 MB; DoRA 1.61 s/it (+52% wall-clock) / 125.6 MB for a MARGINAL quality edge — NOT 'near-free'; LoKr 1.15 s/it / 6.1 MB (~20x smaller) at comparable style quality — the portability win.**
All three bound the style at 600 steps (ship engraving, portrait drawn). DoRA's ship was the crispest of the campaign but the +52% training cost is real (the 'zero overhead' is inference-post-merge only). LoKr delivered ship-quality style binding in a 6.1 MB adapter at ~9% over LoRA's speed. Corrects the wave-3 'DoRA = near-free quality upgrade' framing; confirms + quantifies the LoKr efficiency claim. [EVAL-QUANTIFIED wave-5, n=20]: CLIP-sim/CMMD overturned the n=3 quality reads — DoRA is statistically INDISTINGUISHABLE from LoRA on style fidelity (0.739 vs 0.734, <1 SEM), so its +52% training cost buys NO measurable fidelity gain (the 'crispest ship' was a sampling artifact); LoKr is measurably LOWER fidelity (0.673 vs 0.734, ~3.5 SEM) — the 6MB/20x-smaller is a real size-vs-fidelity tradeoff, not 'comparable.' See diffusion-style-fidelity-eval-panel-measured-5090.
- **For the pipeline:** Default to plain LoRA. Use LoKr when adapter SIZE/portability matters (6 MB vs 122 MB, comparable quality, ~9% slower). Reserve DoRA for when a marginal fidelity edge justifies +52% training time.
- **Method:** lokr · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Seed:** 42 · **Runs:** 3 · **Tuning budget:** 3 matched runs (LoRA/DoRA/LoKr) · **Search:** same-codepath 3-way A/B
- **Validated under:** RTX 5090 32GB; SDXL base 1.0; stdstyl set; lycoris.kohya algo=lora / lora+dora_wd / lokr; dim16/alpha16; AdamW; cosine+30-warmup; bf16 sdpa cache_latents --gradient_checkpointing; 600 steps. 2026-06-06.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-proven-blackwell-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — LyCORIS Apache-2.0; output license = base + dataset.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| lora_measured | 1.06 s/it / 14.2 GB / 121.8 MB | ○ | lycoris control (gradient-checkpointed) |
| dora_measured | 1.61 s/it / 14.3 GB / 125.6 MB | ○ | +52% time, marginal quality edge |
| lokr_measured | 1.15 s/it / 13.5 GB / 6.1 MB | ○ | ~20x smaller adapter, comparable quality |
| network_module | lycoris.kohya | ● | this sd-scripts has no native DoRA |
| gradient_checkpointing | required | ● | else lycoris spills 32 GB — see efficiency lane |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| DoRA picked for a 'free' quality bump but training is +50% | DoRA magnitude decomposition adds real per-step compute | only use DoRA when the marginal fidelity is worth it; default LoRA, or LoKr for size | network_type |

- **Best for:** smallest portable style adapter at full quality (lokr, fit 5) ; marginal fidelity edge regardless of train time (dora, fit 3)
- **Verify:** verdict=confirmed | currency=measured 2026-06-06 | direct rig measurement + looked-at samples
- **Sources:** [training-knowledge wave-4 measurement (network-type 3-way Run 3)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured RTX 5090 2026-06-06; all 6 sample grids looked-at

### Prodigy SDXL style-LoRA — MEASURED on the 5090 (auto-LR works; ~1.8-2x the per-step cost of AdamW) · `recommended` · ▣ measured
**Prodigy's lr=1.0 sentinel auto-finds a working LR (no manual sweep) and binds the style at 600 steps — but MEASURED on the 5090 it costs ~1.8-2.2x wall-clock per step vs AdamW (1.21-1.44 vs 0.685 s/it) + ~1.2 GB more VRAM. It is a CONVENIENCE optimizer, not a free one.**
Matched A/B vs AdamW-fp32 baseline #166 v2 (stdstyl 16-img cyanotype set, dim16/alpha16, TE on, no reg). Run 1 (400 steps): 1.21 s/it, 20.5 GB, loss 0.094 — only the weakest-prior subject (ship) bound; locomotive + portrait stayed photoreal (UNDERTRAINED). Run 1b (600 steps, matched): 1.44 s/it (ran hotter -> mild clock throttle), 20.6 GB, loss 0.105 — ship + locomotive bound (engraving), portrait shifted to a drawn look. Binding follows the subject-prior gradient (ship > loco > portrait), the #165 base-bounds-the-style interaction, optimizer-independent. The auto-LR mechanism works; the wave-3 'slightly higher state' wording understated a material throughput tax.
- **For the pipeline:** Use Prodigy ONLY for the first pass on an unknown style set (it skips the LR sweep). For any retrain at a known LR, use AdamW at 1x. Breakeven: Prodigy (1 run @ ~1.8x, no sweep) beats AdamW (S sweep runs + 1 production run @ 1x) when S >= 1.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Seed:** 42 · **Runs:** 2 · **Tuning budget:** 2 matched runs · **Search:** matched A/B vs #166 v2
- **Variance:** 2 runs (400, 600 steps); the 1.21->1.44 s/it rise is sustained-load clock throttle, not a step-count effect.
- **Validated under:** RTX 5090 sm_120 32GB; E:/AI/training/sd-scripts .venv torch 2.12.0+cu130; SDXL base 1.0; stdstyl 16-img set; dim16/alpha16 TE-on no-reg; bf16 sdpa cache_latents; Prodigy decouple/wd=0.01/d_coef=2/use_bias_correction/safeguard_warmup; cosine + 30-step warmup. 2026-06-06.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-proven-blackwell-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Prodigy MIT (konstmish/prodigy); output license = base + dataset.
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| optimizer | Prodigy | ● |  |
| learning_rate | 1.0 | ● | SENTINEL — auto-estimated; never set a real LR |
| d_coef | 2 | ○ | control aggressiveness here instead of LR |
| safeguard_warmup | True | ● | with lr_warmup_steps>0 |
| network_dim | 16 | ○ |  |
| alpha | 16 | ○ |  |
| scheduler | cosine | ○ |  |
| warmup | 30 steps | ○ |  |
| steps | 600 | ○ | needs full budget for consistent binding |
| measured_s_per_it | 1.21-1.44 s/it | ○ | vs AdamW 0.685 |
| measured_peak_vram | 20.5-21.1 GB | ○ | vs AdamW 19.4 |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| style binds only some subjects | undertraining (400 steps) | use the full ~600-step budget; binding follows subject prior | steps |
| run ~2x slower than AdamW | d-estimate + extra optimizer state (inherent) | use AdamW at a known LR for retrains; reserve Prodigy for unknown sets | optimizer |

- **Best for:** first LoRA on an unknown style set (no LR sweep) (sdxl, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-06 | direct rig measurement + looked-at samples (no adversarial verifier needed; the rig is the oracle)
- **Sources:** [training-knowledge wave-4 measurement (Prodigy Run 1 + 1b)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured on RTX 5090, 2026-06-06; samples looked-at ; [Prodigy: An Expeditiously Adaptive Parameter-Free Learner](https://arxiv.org/abs/2306.06101) (Mishchenko & Defazio, 2023) — parameter-free LR via distance-to-solution estimation; fixed lr=1.0

### SDXL style-LoRA with text-encoder + non-word trigger token (+ optional regularization gating) · `recommended` · ▣ measured
**Adding text-encoder training + a NON-WORD trigger token (dim16/alpha16, unet_lr=te_lr=1e-4, 300-600 steps) binds the style to a token; an optional regularization set turns that token into a GATE (style only when the trigger fires), at ~20-25% it/s cost.**
Extends the UNet-only baseline by removing --network_train_unet_only so the text encoders train, and adding a non-word trigger (e.g. 'stdstyl') as the caption prefix: caption = '<TRIGGER>, <subject>' with NO style words and a neutral class folder name, so the style's only source is the token. network_dim 16 / network_alpha 16 (alpha=dim, full-strength scaling), learning_rate=unet_lr=text_encoder_lr=1e-4, AdamW, lr_scheduler constant, max_train_steps 300-600, 1024,1024 bf16, --sdpa, --cache_latents, seed 42. THE load-bearing fix: pass --caption_extension .txt — kohya defaults to .caption and SILENTLY ignores .txt captions (training on the bare class token instead, which is exactly how an earlier trigger never trained); verify the log says 'read caption: N/N', not 'No caption file found'. COMMAND B adds gating: a regularization set of the SAME subjects in NORMAL style captioned WITHOUT the trigger, passed via --reg_data_dir, so kohya applies prior-preservation: no trigger => base/normal, trigger => style.
- **For the pipeline:** Use this when the studio needs a style that activates ONLY on a token (clean base output otherwise) — e.g. shipping a base + a togglable house style. Validation requires a 3-way LOOK at one seed: base+trigger (control), LoRA+no-trigger, LoRA+trigger; style in (LoRA+trigger) but not (LoRA+no-trigger) proves the gate. Caveat: SDXL base 1.0 RESISTS saturated non-natural palettes — 5 configs proved no knob recovers a strong cyanotype blue while keeping strong style + gating. For a saturated palette WITH gating, train on a more-flexible Apache-2.0 base (e.g. Z-Image-Turbo) instead; for palette WITHOUT gating, fall back to the light unet-only floor.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Seed:** 42 · **Runs:** 5 · **Tuning budget:** ~5 manual configs across two waves probing the TE+trigger path and the palette/gating trade-off. · **Search:** manual
- **Variance:** Runs v1-v5 (2026-06-03): v1/v2 exposed the silent caption_extension bug; v3 validated gating (crisp on ship/portrait, weak on strongly-colored subjects); v4/v5 proved no kohya knob recovers a base-resisted deep-blue palette while keeping gating. Adapter sha256 hashes pinned in the engine baseline.
- **Validated under:** SDXL base 1.0, 1024,1024, batch 1, bf16, single RTX 5090, native Windows, sd-scripts; TE training on; non-word trigger; optional reg set same-subjects-normal-style.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-te-trigger-reg-gating-recipe-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Builds on (stage 2):** SDXL style-LoRA, UNet-only baseline (kohya/sd-scripts, dim16/alpha8, AdamW @1e-4 constant, 1024px bf16)
- **Output license:** commercial **conditional** — LoRA inherits the base license (SDXL base 1.0 = OpenRAIL++). Both base and dataset (training + regularization images) must be commercial-clean; if a saturated palette forces a base swap, Z-Image-Turbo (Apache-2.0) keeps the output commercial-clean.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | lora | ● | networks.lora |
| rank | 16 dim | ● | --network_dim 16 |
| alpha | 16 | ● | --network_alpha 16; alpha=dim => full-strength scaling (vs the alpha8 floor) |
| unet_lr | 1e-4 | ● | --unet_lr 1e-4 |
| te_lr | 1e-4 | ● | --text_encoder_lr 1e-4; removing --network_train_unet_only is what turns TE training ON |
| learning_rate | 1e-4 | ● | AdamW base LR |
| optimizer | AdamW | ● | --optimizer_type AdamW |
| scheduler | constant | ○ | lr_scheduler constant |
| steps | 300-600 | ● | max_train_steps; light end (~300) holds more of a base-resisted color |
| repeats | 10 | ● | '10_<neutralclass>' folder; class name is NOT the trigger |
| resolution | 1024,1024 px | ● | SDXL native |
| precision | bf16 | ● | mixed + save bf16 |
| batch_size | 1 | ● | train_batch_size 1 |

- **Datasets:** SDXL style-LoRA regularization set (same subjects, normal style, no trigger) — the gating contrast (regularization, license studio-owned (synthetic via commercial-clean base); same commercial-clean gate as the training set) ; SDXL style-LoRA training set (non-word trigger, style-pruned booru captions) (training, license studio-owned (synthetic via commercial-clean base); commercial-clean only if the generating base is commercial-clean — verify per project)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Trigger token never fires; style appears unconditionally or not at all even with TE training enabled | kohya defaults caption_extension to .caption and SILENTLY ignores .txt files, training on the folder class-token instead of the captions | pass --caption_extension .txt and verify the log prints 'read caption: N/N' (not 'No caption file found') | captions |
| Style leaks into LoRA+no-trigger generations (no clean gate) | no regularization/contrast set, so the token isn't forced to carry the style alone | add --reg_data_dir with the SAME subjects in normal style captioned WITHOUT the trigger (prior-preservation); costs ~20-25% it/s | regularization |
| Saturated/non-natural palette (e.g. deep cyanotype blue) drifts to grayscale/desaturated under training | SDXL base 1.0 resists strongly-colored non-natural palettes; no rank/scaling/steps/reg-weight knob recovers it while keeping strong style + gating | drop gating and train light (alpha8, ~300 steps, no reg) to keep palette, OR switch to a more-flexible Apache-2.0 base (Z-Image-Turbo) for palette + gating | alpha |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | 3-way trigger-gating A/B look-at-images | style present in (LoRA+trigger), absent in (LoRA+no-trigger) and base control => trigger gates | style appears ONLY with the trigger; control proves the style is trained not prompted (non-word trigger) | ✓ | human / ai-eyes (different family from the SDXL generator) |

- **Best for:** togglable token-gated SDXL house style (sdxl, fit 5) ; bind a style to a trigger token (diffusion, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. TE + trigger + reg gating remains standard kohya practice through 2026. The 20-25% it/s cost is deferred to the engine KB. | One citation fix required: the claim text says DreamBooth PPL is 'the mechanism kohya's --reg_data_dir implements' — this overstates the match. DreamBooth PPL was designed for subject/instance prior preservation, not style-token gating; the conceptual parallel is reasonable but not a direct mechanism identity. The PARTIAL tag on finding_supported is correctly applied, but the technique's own claim text should add a qualifier (e.g., 'analogous to' rather than 'implements'). The Tech Tactician source (techtactician.com, confirmed real, Dec 2025) is cited for training-caption trigger discipline but the page's actual focus is inference-side SDXL prompting; the cited finding is not the page's primary content — weak source match, not fabricated. Evidence_strength='measured-on-rig' is properly backed by the engine KB receipt; no overclaim.
- **Sources:** [RECIPE (PROVEN): kohya SDXL style-LoRA with text-encoder + trigger token (+ optional reg gating) — the caption_extension fix](https://github.com/kohya-ss/sd-scripts) (studio (tensor-engine-knowledge KB), 2026) — TE+trigger SDXL LoRA (dim16/alpha16, unet_lr=te_lr=1e-4, 300-600 steps) with --caption_extension .txt fix and optional --reg_data_dir gating; measured hashes/it/s/VRAM in the engine KB. ; [DreamBooth: Fine Tuning Text-to-Image Diffusion Models for Subject-Driven Generation](https://arxiv.org/abs/2208.12242) (Ruiz, Li, Jampani, Pritch, Rubinstein, Aberman, 2022) — Class-specific prior-preservation loss (regularization images under the class prompt) preserves the base prior and gates a unique identifier token — the mechanism kohya's --reg_data_dir implements. ; [Booru-Style Tagging and How To Use It With SDXL Anime Model Prompts](https://techtactician.com/booru-style-tagging-sdxl-anime-prompts-guide/) (Tech Tactician, 2024) — Trigger words placed at the start of captions, kept consistent across the set, are how a LoRA learns to recreate the concept on that token.

### SDXL style-LoRA, UNet-only baseline (kohya/sd-scripts, dim16/alpha8, AdamW @1e-4 constant, 1024px bf16) · `recommended` · ▣ measured
**A UNet-only SDXL LoRA at rank16/alpha8, AdamW 1e-4 constant, 1024,1024 bf16 with --sdpa (never xformers on Blackwell) is the proven minimal style-LoRA that trains end-to-end on the single RTX 5090.**
The floor recipe: train only the UNet (--network_train_unet_only), network_dim 16 / network_alpha 8 (alpha=dim/2 dampens the effective LR, a deliberately conservative style floor), AdamW @ learning_rate 1e-4, lr_scheduler constant, resolution 1024,1024 (SDXL native, NOT 512), train_batch_size 1, mixed/save precision bf16, --sdpa attention, --cache_latents, --gradient_checkpointing, seed 42. Dataset layout is a parent dir containing one '10_<concept>' folder (leading int = repeats) of image + matching .txt caption pairs. Two Blackwell/Windows gotchas are load-bearing and live in the engine receipt: PYTHONUTF8=1 (sd-scripts logs Japanese strings that crash a cp1252 console at loop start) and --sdpa instead of xformers (xformers is the Blackwell trap). It trains fine on torch 2.12/cu130 with no code changes.
- **For the pipeline:** This is the studio's house-style LoRA starting point: cheapest, most reproducible SDXL style adapter that fits 32 GB with headroom. Use it when you want the style applied at a chosen LoRA strength and do NOT need token gating. Scale knobs from here: AdamW8bit + --fp8_base to cut VRAM, raise network_dim for capacity, or drop --network_train_unet_only to add the text encoder (the next stage).
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Seed:** 42 · **Runs:** 1 · **Tuning budget:** Manual single-config proving pass (recipe-proving wave), not a hyperparameter search. · **Search:** manual
- **Variance:** Single proving run on 2026-06-02 establishing the working env + command; not a multi-seed variance study. Throughput/VRAM are pinned in the engine receipt, not here.
- **Validated under:** SDXL base 1.0 .safetensors, 1024,1024, batch 1, bf16, single RTX 5090 (Blackwell sm_120), Windows 11 native, sd-scripts on uv py3.11 + torch 2.12.0+cu130, AdamW.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-proven-blackwell-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **conditional** — The LoRA inherits the base-model license. SDXL base 1.0 (OpenRAIL++) and Illustrious-XL (Open RAIL-M) are commercial-permissible; the trained adapter is commercial-clean only if BOTH the base and every training image are commercial-clean. Verify the dataset license separately.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | lora | ● | networks.lora (--network_module networks.lora) |
| rank | 16 dim | ● | --network_dim 16; raise for more style capacity |
| alpha | 8 | ● | --network_alpha 8; alpha/rank=0.5 scales (dampens) the effective LR per LoRA's alpha/r scaling |
| learning_rate | 1e-4 | ● | AdamW real LR (not a Prodigy sentinel) |
| optimizer | AdamW | ● | --optimizer_type AdamW; AdamW8bit (bnb) is the VRAM-saving swap |
| scheduler | constant | ○ | lr_scheduler constant |
| batch_size | 1 | ● | train_batch_size 1 |
| repeats | 10 | ● | leading int on the '10_<concept>' folder name |
| resolution | 1024,1024 px | ● | SDXL native; do NOT train at 512 for SDXL |
| precision | bf16 | ● | --mixed_precision bf16 --save_precision bf16 |

- **Datasets:** SDXL style-LoRA training set (non-word trigger, style-pruned booru captions) (training, license studio-owned (synthetic via commercial-clean base); commercial-clean only if the generating base is commercial-clean — verify per project)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| UnicodeEncodeError crash right as the training loop starts (SDXL load + latent cache + LoRA build already succeeded) | accelerate child inherits a cp1252 console; sd-scripts logs Japanese strings | set PYTHONUTF8=1 and PYTHONIOENCODING=utf-8 before accelerate launch | env |
| Install pulls a wrong torch / CUDA mismatch on Blackwell, cuda.is_available False or attention crashes | diffusers[torch] resolves a non-Blackwell torch; xformers has no sm_120 path | install torch+torchvision from the cu130 index FIRST, then requirements; use --sdpa, never install xformers | precision |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | held-out-subject A/B look-at-images | style present with LoRA, absent in base control | style visibly applied without subject-identity bleed or frying | ✓ | human / ai-eyes (different family from generator) |

- **Best for:** studio house-style SDXL LoRA (apply at strength) (sdxl, fit 5) ; single-GPU 32GB SDXL training floor (single-gpu, fit 5)
- **Verify:** verdict=confirmed | currency=Current. xformers incompatibility with Blackwell sm_120 is confirmed by open issues (bmaltais/kohya_ss #3276, #3096, AUTOMATIC1111/stable-diffusion-webui #16818 as of 2025-2026); --sdpa is the correct alternative and the claim reflects this accurately. | Boundary clean: measured it/s and VRAM are correctly deferred to engine_recipe_ref. 'Never xformers on Blackwell' is how-to-train backend selection, not tensor-engine software cataloging. All three sources confirmed real and on-point: arXiv:2106.09685 (Hu et al. LoRA) confirmed; Discussion #1093 confirmed to exist and to discuss alpha/rank dampening; engine KB receipt is internal and consistent with the claim.
- **Sources:** [RECIPE (PROVEN): kohya_ss SDXL LoRA on Blackwell — uv py3.11 + cu130 torch + UTF-8/sdpa gotchas + exact command](https://github.com/kohya-ss/sd-scripts) (studio (tensor-engine-knowledge KB), 2026) — Exact working SDXL UNet-only LoRA command (dim16/alpha8, AdamW 1e-4, 1024px bf16, --sdpa, seed 42) on the RTX 5090; measured it/s + VRAM pinned in the engine KB. ; [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) (Hu, Shen, Wallis, Allen-Zhu, Li, Wang, Wang, Chen, 2021) — ΔW = BA scaled by alpha/r (h = W0x + (alpha/r)BAx); alpha is a magnitude/scaling knob coupled to rank, not an independent LR. ; [Network Alpha — kohya-ss/sd-scripts Discussion #1093](https://github.com/kohya-ss/sd-scripts/discussions/1093) (kohya-ss community, 2024) — alpha/rank is the strength multiplier on the LR; alpha < dim reduces learning-rate efficiency (so alpha=8 with dim=16 is a deliberate dampened floor).

### min_snr_gamma 5 — MEASURED fidelity win for SDXL style-LoRA (+0.049 CLIP-sim, ~2.3 SEM) · `recommended` · ▣ measured
**MEASURED on the 5090 (matched baseline, eval n=20): --min_snr_gamma 5 lifts cyanotype fidelity to CLIP-sim 0.7747 vs baseline 0.7257 (+0.049, ~2.3 SEM) with the best CMMD of the B1 set (0.1348). The min-SNR loss reweighting measurably improves style binding for this set — comparable to noise_offset's gain, and the two also render the saturated blue (looked-at).**
Corrects the wave-3 reproduced-from-source framing to a measured win. min_snr_gamma 5 (the Hang et al. recommended value) reweights the loss toward harder timesteps and measurably improves fidelity + distribution match. Stacks conceptually with noise_offset (different mechanisms: loss-reweighting vs brightness-range); both were measured individually here.
- **For the pipeline:** Use --min_snr_gamma 5 as a near-free fidelity improvement for SDXL style-LoRA. Combined with noise_offset 0.1 it is the recommended saturated-palette SDXL recipe (each measured individually as ~+0.05; a combined run is the natural follow-up).
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Seed:** 42 · **Runs:** 1 · **Search:** matched A/B vs baseline, eval n=20
- **Variance:** n=20, SEM 0.018; vs baseline ~2.3 SEM (significant).
- **Validated under:** RTX 5090; SDXL base 1.0; stdstyl 16-img; dim16 TE-on no-reg; AdamW lr 1e-4 cosine+warmup; 600 steps; --min_snr_gamma 5. 2026-06-07.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-proven-blackwell-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes**
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| min_snr_gamma | 5 | ○ | Hang et al. recommended |
| result_min_snr | CLIP-sim 0.7747 / CMMD 0.1348 | ○ | best CMMD of B1; vs baseline 0.7257/0.1782 |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | CLIP-sim-to-style-centroid | 0.7747 | >=0.70 | ✓ | clip-vit-b32 |

- **Best for:** near-free SDXL style-LoRA fidelity gain (sdxl, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-07 | rig + n=20 eval
- **Sources:** [training-knowledge wave-7 B1 min_snr_gamma (n=20)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured 2026-06-07; _sdxl_minsnr_result.txt + _eval_sdxl_noise.json ; [Efficient Diffusion Training via Min-SNR Weighting Strategy](https://arxiv.org/abs/2303.09556) (Hang et al., 2023) — min-SNR loss reweighting (gamma~5) speeds/improves diffusion training

### noise_offset 0.1 breaks the SDXL #165 blue-ceiling — MEASURED (+0.049 CLIP-sim, ~2.3 SEM); ztsnr neutral-to-worse on eps-pred SDXL · `recommended` · ▣ measured
**MEASURED on the 5090 (matched AdamW-fp32 baseline, stdstyl 16-img, dim16, 600 steps, eval n=20): --noise_offset 0.1 lifts cyanotype style-fidelity to CLIP-sim 0.7748 vs baseline 0.7257 (+0.049, ~2.3 SEM, + CMMD 0.137 vs 0.178) — and the looked-at grids show WHY: the baseline ship renders near-GRAYSCALE (the SDXL #165 blue-ceiling that held across waves 4/5, none of which used noise_offset), while noise_offset renders a deep Prussian-blue cyanotype. So noise_offset substantially BREAKS the #165 ceiling for a saturated/high-contrast palette. --zero_terminal_snr is neutral-to-worse (0.7176, kohya warns 'zero_terminal_snr enabled but v_parameterization is not' — SDXL is eps-pred).**
Corrects the wave-3 'situational' framing: for a saturated dark palette like cyanotype, noise_offset (which targets brightness extremes — exactly the deep-blue darks) is a measured, significant win, not merely situational. Gives the studio a CHEAPER path to the saturated cyanotype palette than the Chroma base-swap (wave 6): SDXL+noise_offset is 109 MB in the SDXL ecosystem vs Chroma's 17 GB base + Chroma-specific inference. ztsnr on eps-pred SDXL is not worth it.
- **For the pipeline:** Add --noise_offset 0.1 by default when training a saturated/high-contrast style-LoRA on SDXL base 1.0 — it is the lever that lets the palette render. Do NOT use --zero_terminal_snr on eps-pred SDXL (no v_parameterization). For the cyanotype palette specifically, SDXL+noise_offset is a viable cheaper alternative to the Chroma base-swap.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Seed:** 42 · **Runs:** 2 · **Tuning budget:** baseline + 2 levers (noise_offset, ztsnr) · **Search:** matched A/B vs baseline, eval n=20 + looked-at
- **Variance:** n=20/config, SEM ~0.015; noise_offset-vs-baseline ~2.3 SEM (significant); ztsnr-vs-baseline ~1 SEM (neutral-worse).
- **Validated under:** RTX 5090 32GB; SDXL base 1.0; stdstyl 16-img; networks.lora dim16/alpha16 TE-on no-reg; AdamW lr 1e-4 cosine+30-warmup; 600 steps; bf16 sdpa cache_latents; eval sdxl_gen_img euler_a 24 steps. Watchdog overwatch, peak 58C. 2026-06-07.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-proven-blackwell-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — output license = base + dataset.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| noise_offset | 0.1 | ○ | the lever that breaks the #165 blue-ceiling for saturated palettes |
| result_noise_offset | CLIP-sim 0.7748 / CMMD 0.1373 | ○ | vs baseline 0.7257 / 0.1782 — +0.049, ~2.3 SEM |
| result_baseline | CLIP-sim 0.7257 / CMMD 0.1782 | ○ | renders near-grayscale (the #165 ceiling) |
| result_ztsnr | CLIP-sim 0.7176 / CMMD 0.1878 | ○ | neutral-to-worse; eps-pred SDXL, no v_parameterization |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| SDXL style-LoRA can't render a saturated non-natural palette (renders grayscale) | the #165 base blue-ceiling without noise_offset | --noise_offset 0.1 (measured: gray -> deep blue) | noise_offset |
| zero_terminal_snr gives no gain / slight loss | eps-prediction SDXL without v_parameterization | don't use ztsnr on eps-pred SDXL | zero_terminal_snr |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | CLIP-sim-to-style-centroid | 0.7748 | >=0.70 | ✓ | clip-vit-b32 |
| diffusion-style | CLIP-sim-to-style-centroid | 0.7257 | >=0.70 | ✓ | clip-vit-b32 |

- **Best for:** render a saturated/high-contrast style on SDXL base (sdxl, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-07 | rig + n=20 eval + looked-at (baseline gray vs noise_offset deep blue); oracle = rig + harness, not the study-swarm verifier
- **Sources:** [training-knowledge wave-7 B1 noise levers (n=20 eval + looked-at)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured RTX 5090 2026-06-07; _sdxl_{baseline,noiseoffset,ztsnr}_result.txt + _eval_sdxl_noise.json

### Adapter post-processing: merge-into-checkpoint, SVD resize/dim-reduction, extraction · `recommended` · ▸ reproduced
**After training you can (a) bake a LoRA into a checkpoint (merge_lora) for a frozen distributable model, (b) shrink an over-ranked LoRA losslessly-ish via SVD resize (sv_ratio/sv_cumulative/sv_fro) — only ever downward, and (c) extract a LoRA from a full fine-tune difference; each is a named, reversible-by-keeping-the-source step.**
Three sd-scripts/kohya tools cover the adapter lifecycle after training. MERGE (merge_lora.py / svd_merge_lora.py): bakes one or more LoRAs into the base UNet/TE at chosen weights, producing a standalone checkpoint — useful to freeze a shipping art model so inference needs no adapter stack, or to merge several style/char LoRAs into one model via SVD (svd_merge_lora handles rank reconciliation). RESIZE (networks/resize_lora.py): re-approximates a LoRA at a LOWER rank via SVD (torch.svd_lowrank, --svd_lowrank_niter default 2). dynamic_method picks the new per-layer rank automatically: sv_ratio (largest/smallest singular-value ratio), sv_cumulative (keep until cumulative SV fraction), or sv_fro (Frobenius-norm fraction); it reports 'fro retained' so you see how much signal survived. Use it to ship a small file from a high-rank training run — the header warns it should ONLY go to lower rank. EXTRACT (extract_lora_from_models.py, lineage: cloneofsimo cli_svd): SVD-diffs a full DreamBooth/fine-tune against the base to recover a LoRA, controllable by target dim or sv ratio. All three are NAMED_COMPENSATOR-friendly: the source LoRA/checkpoint is the undo — keep it and the operation is reversible.
- **For the pipeline:** Standardize the studio's distribution path: train at a generous rank (e.g. 32), then SVD-resize down (sv_fro, watch 'fro retained' >= ~0.95) to ship a small adapter — rather than guessing the final rank up front. Provide a 'bake' step (merge into checkpoint) only for frozen distributable art models, and ALWAYS keep the source adapter + the resize report as the named compensator (re-resize or re-merge if a downstream artifact is wrong). Use extract to convert any legacy full fine-tune in the pipeline into a composable LoRA. Trainer-software specifics (exact flags/versions) live in the tensor-engine lane; this lane owns the WHEN/WHY.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** protocol
- **Validated under:** Tool behavior and dynamic_method options are from kohya source/docs; 'fro retained' thresholds are practitioner guidance, not rig-measured this wave.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — kohya tooling (Apache-2.0); merging does not change weight provenance — merged checkpoint inherits base + dataset license obligations.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| rank | train 32 -> resize to 8-16 dim | ○ | resize only DOWNWARD |
| network_type | sv_fro / sv_ratio / sv_cumulative dynamic_method | ○ | auto per-layer new rank; watch 'fro retained' |

- **Datasets:** SDXL style set trained at high rank for SVD resize-down distribution (train, license Internal / project-canon only — source plates gated for commercial cleanliness per image; not redistributable. Base SDXL terms apply.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Resized LoRA loses the style | target rank too low / 'fro retained' dropped far below ~0.95 | Raise target rank or use sv_fro with a higher retained fraction | rank |
| resize_lora.py TypeError dim/alpha None | metadata missing network_dim/alpha (e.g. on extracted LoRAs) | Pass --model_dim/--model_alpha or use a build with the metadata fix | network_type |
| Merged checkpoint over-baked | merge weight too high (e.g. 1.0 of an already-strong LoRA) | Merge at the validated inference weight (often 0.7-0.9), re-merge from source as the undo | network_type |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| resize-fidelity | fro retained + visual A/B vs source LoRA | fro retained >= 0.95 visually indistinguishable | fro retained >= 0.95 | ✓ | ai-eyes / human |

- **Best for:** Ship a small adapter from a high-rank training run (style-lora, fit 5) ; Freeze a distributable art checkpoint (style-lora, fit 4) ; Convert a legacy full fine-tune into a composable LoRA (character-lora, fit 4)
- **Verify:** verdict=confirmed | currency=Current. SVD-based LoRA resize and merge remain supported in kohya sd-scripts in 2026. | resize_lora.py fully verified: sv_ratio, sv_cumulative, sv_fro methods present; torch.svd_lowrank used for large matrices; downward-only constraint enforced in code. PR#243 citation is plausible for lineage provenance. 'Reversible by keeping the source' framing is accurate. evidence_strength 'reproduced-from-source' warranted.
- **Sources:** [sd-scripts networks/resize_lora.py](https://github.com/kohya-ss/sd-scripts/blob/main/networks/resize_lora.py) (kohya-ss, 2024) — Re-approximates LoRA to lower rank via SVD; dynamic_method sv_ratio/sv_cumulative/sv_fro; uses torch.svd_lowrank; reports fro retained; downward-only. ; [Enable ability to resize lora dim based off sv ratios (PR #243)](https://github.com/kohya-ss/sd-scripts/pull/243) (mgz-dev, 2023) — Dynamic SV-ratio resize derived from extract_lora_from_models.py (lineage cloneofsimo cli_svd); svd_merge_lora for merging.

### Booru-tag captioning with style-tag pruning + non-word trigger (style-LoRA curation) · `recommended` · ▸ reproduced
**For a STYLE LoRA, captions should describe only the varying SUBJECT in comma-separated booru tags while a non-word trigger prefix carries the style — pruning style-descriptor tags forces the style to bind to the token, not to scattered words.**
Caption-format craft, not a hyperparameter: SDXL-family models respond to comma-separated booru/wd14 tags, not grammatical sentences. The style-LoRA rule inverts the subject-LoRA rule: keep the tags that VARY across the set (subject, pose, composition) and PRUNE the tags that describe the constant you are training (the style), so the style has no caption anchor and binds to the trigger token instead. Use a non-word trigger (e.g. 'stdstyl') placed first and kept consistent across every caption, with NO style words anywhere. Dataset discipline is consistent STYLE + varied SUBJECTS (the inverse of subject LoRAs). A neutral class folder name (not the trigger) ensures the trigger's only source is the captions. Pairs directly with the TE+trigger recipe.
- **For the pipeline:** This is the input lever that drives style-LoRA outcome more than rank/LR. The pruning decision is the style-bleed control: under-prune and the style smears across many tokens (no clean gate); over-prune subject tags and the set loses variety (overfit/replication). For the studio's canon-bound sets from style-dataset-lab, the pruning rule is part of the datasheet, applied once per dataset. Caption files are .txt (and the recipe must pass --caption_extension .txt or they are silently ignored).
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** curation
- **Tuning budget:** Practice rule, not a search; pruning aggressiveness is the tunable per dataset. · **Search:** manual
- **Variance:** Captioning practice consolidated from community training guides + the rig's own #166 run where caption discipline (and the .caption/.txt bug) was the decisive factor in whether the trigger trained.
- **Validated under:** SDXL-family, booru/wd14 tag captions, style-LoRA (consistent style / varied subjects). Validated qualitatively on the rig's stdstyl set.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **conditional** — Captioning method is unencumbered, but the commercial-clean gate is the IMAGE source: every training and regularization image must be license-clean. The auto-captioner's weights (wd14 etc.) are catalogued in model-knowledge, not here.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| caption_strategy | non-word trigger first + comma-separated booru subject tags, style tags pruned | ● | trigger consistent across the whole set; no style words |

- **Datasets:** SDXL style-LoRA training set (non-word trigger, style-pruned booru captions) (training, license studio-owned (synthetic via commercial-clean base); commercial-clean only if the generating base is commercial-clean — verify per project)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Style smears across many tokens; can't gate it to the trigger | style-descriptor tags left in the captions give the style multiple anchors | prune every tag that describes the constant style; keep only varying-subject tags + the trigger | captions |
| LoRA replicates training subjects / poor subject variety | over-pruned subject tags or too-uniform subjects, so the model memorizes instead of generalizing the style | keep subject/pose/composition tags varied and the subject set diverse; prune only the style constant | captions |

- **Best for:** caption a style (not subject) LoRA set (dataset, fit 5) ; make a trigger token gate a style (sdxl, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. Booru-tag style-pruning for style LoRA captioning is standard practice with no superseding approach identified through 2026. | One citation fix required: the Tech Tactician source (techtactician.com/booru-style-tagging-sdxl-anime-prompts-guide/, confirmed real, Dec 2025) is cited to support training-caption trigger discipline, but the page is actually about inference-side prompting workflows for SDXL anime models, not training captioning. The claimed finding ('trigger words placed at the start of captions, kept consistent across the set, are how a LoRA learns to recreate the concept on that token') is training advice that is not the page's subject. This is a source-claim domain mismatch: the URL is real, but it is attributed to support a claim outside its scope. Should be replaced with a training-focused source (e.g., the Haoming02 guide already cited, or sd-scripts training docs) or the claim should be attributed only to config_recipes #166. The Haoming02 AIO guide source is confirmed accurate and on-point. evidence_strength='reproduced-from-source' is appropriate given the correctly-cited sources.
- **Sources:** [All-in-One-Stable-Diffusion-Guide — LoRA Training (caption pruning rules)](https://github.com/Haoming02/All-in-One-Stable-Diffusion-Guide/blob/main/LoRATraining.md) (Haoming02, 2024) — Prune caption tags that describe the constant you are training so that trait binds to the trigger word; keep only the variable tags. ; [Booru-Style Tagging and How To Use It With SDXL Anime Model Prompts](https://techtactician.com/booru-style-tagging-sdxl-anime-prompts-guide/) (Tech Tactician, 2024) — SDXL-family tagging uses standardized comma-separated booru keywords (not sentences); trigger words go first and stay consistent across the dataset. ; [config_recipes #166 — DATASET DISCIPLINE (style LoRA, not subject LoRA)](https://github.com/kohya-ss/sd-scripts) (studio (tensor-engine-knowledge KB), 2026) — Consistent style + varied subjects, caption '<TRIGGER>, <subject>' with a non-word trigger and NO style words, neutral class folder so the trigger's only source is the captions.

### Checkpoint selection: save cadence + sample-during-training + best-epoch eval grid · `superseded` · ▸ reproduced
**Save every epoch, sample fixed seeds/prompts every N steps, then pick the best checkpoint by an XYZ grid (epoch x LoRA-weight) on HELD-OUT prompts — the final epoch is usually NOT the best; 60-80% completion checkpoints frequently win because the last epochs overcook style.**
The single most leverage-per-effort decision in style-LoRA training is WHICH saved epoch you ship, and the only reliable way to choose is an external eval grid, not the loss curve (diffusion loss is near-useless for quality). Protocol: (1) set save_every_n_epochs=1 (or every ~10-20% of steps) so you have a ladder of candidates; (2) set sample_every_n_steps with a FIXED seed list and a FIXED held-out prompt set (disjoint from training captions, including out-of-distribution subjects to test style transfer, not memorization) so progress is comparable across checkpoints; (3) after training, build an XYZ grid with X=checkpoint(epoch), Y=LoRA weight {0.6,0.8,1.0}, fixed seeds, and judge for style-match WITHOUT subject-collapse or frying. Community-consistent finding: test 60-80% checkpoints first — they often beat 100% because the final epochs trade flexibility for memorization. Early-stopping signals: sample images stop improving / start fusing into training compositions / colors over-saturate / unprompted style bleed appears on neutral prompts. This is an EXTERNAL_VERIFIER pattern — the grid + a different judge (human or ai-eyes-mcp), not the generator's own loss.
- **For the pipeline:** Bake a 'pick-the-epoch' gate into the studio pipeline: every style-LoRA run emits a checkpoint ladder + a fixed-seed held-out sample sheet, and shipping is gated on an XYZ epoch-grid review (ANDON_AUTHORITY: a bad ladder halts before merge). Never ship the last epoch by default. The held-out prompt set must be versioned alongside the dataset snapshot and contain OOD subjects so the grid measures style generalization, not training-prompt recall (guards train_eval_overlap).
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** eval-method
- **Validated under:** Save-cadence/sampling knobs are kohya-documented; '60-80% beats final' and overtraining signals are strongly community-consistent, not rig-measured this wave.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Selection/eval protocol; no license impact.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| epochs | save_every_n_epochs=1 | ● | produce a candidate ladder |
| steps | sample_every_n_steps with fixed seeds | ● | comparable progress sheet across checkpoints |
| caption_strategy | held-out validation prompts disjoint from train, include OOD subjects | ● | measures style transfer not memorization |

- **Datasets:** Held-out style eval set (frozen prompt list + pinned style-exemplar plate) (eval, license studio-internal canon art (commercial-clean by construction); the exemplar plate's license follows the canon-bound source it is drawn from)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Shipped LoRA is rigid / only reproduces training compositions | picked the final (overtrained) epoch | Grid-test 60-80% epochs; ship the most flexible style-faithful one | epochs |
| Cannot compare checkpoints meaningfully | samples used random seeds/prompts per checkpoint | Fix seed list + prompt set across the whole run | steps |
| Validation looks great but real prompts fail | validation prompts overlapped training captions (memorization) | Use disjoint OOD held-out prompts; check train/eval overlap | caption_strategy |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| xyz-grid | style-fidelity vs flexibility per epoch | best epoch typically 60-80% of run | no fry, no subject-collapse, style holds on OOD prompt | ✓ | ai-eyes / human (external) |

- **Best for:** Choosing which epoch to ship (style-lora, fit 5) ; Detecting overtraining before it ships (character-lora, fit 5)
- **Verify:** verdict=confirmed | currency=Current. XYZ-grid checkpoint selection and mid-training sampling remain standard practice in 2026. | ThinkDiffusion source confirmed (save cadence, sample-during-training, 60-80% completion heuristic). The kohya_ss wiki citation is PARTIAL as rated — confirms cadence mechanics but not XYZ grid comparison specifically. evidence_strength 'reproduced-from-source' is reasonable given the ThinkDiffusion source is substantive. No dedup issue vs wave-1.
- **Sources:** [SDXL LoRA Training with Kohya (save/sample cadence, checkpoint testing)](https://learn.thinkdiffusion.com/new-kohya-training/) (ThinkDiffusion, 2024) — save_every_n_epochs and sample_every_n_steps used to detect under/overtraining; checkpoints at 20/40/60/80/100% should be compared; 60-80% often best. ; [LoRA training parameters (bmaltais/kohya_ss Wiki)](https://github.com/bmaltais/kohya_ss/wiki/LoRA-training-parameters) (bmaltais et al., 2024) — Saving intermediate epochs and XYZ-grid comparison is the documented way to select the best checkpoint and spot overtraining.

### Multi-concept / multi-folder repeat-balancing + token separation (SDXL) · `superseded` · ▸ reproduced
**To train N concepts in one LoRA, set per-folder num_repeats so each concept contributes a comparable image-count per epoch (repeats_i ≈ target / count_i), and give each concept a DISTINCT non-word trigger so the network does not blend them — unbalanced repeats are the #1 cause of one concept dominating the LoRA.**
kohya's per-folder `N_classname` convention (the integer before the underscore is num_repeats) was designed to balance imbalanced datasets. Effective images per concept per epoch = count_i * repeats_i; total steps = sum(count_i*repeats_i) * epochs / batch_size. To balance, pick a target effective-count T (e.g. the largest folder's count) and set repeats_i ≈ round(T / count_i): a 100-image concept gets repeats=1 while a 20-image concept gets repeats=5, so both expose ~100 images/epoch. The same lever doubles as a QUALITY weight — give high-quality images a separate higher-repeat folder. Token separation is the second half: each concept needs its own distinct trigger (ideally a rare/non-word token per the wave-1 trigger technique) and captions that share NO subject tokens across concepts, or the LoRA averages them. For a style + character combo in one LoRA, use a style trigger that is constant across all folders plus per-character triggers. Multi-concept LoRAs are harder to keep separated than N single-concept LoRAs; prefer separate LoRAs unless the concepts must interact.
- **For the pipeline:** Add a repeat-balancing calculator to the style-dataset-lab snapshot step: it should emit per-folder repeats from image counts so the operator never eyeballs them. Enforce a 'distinct trigger per concept + zero shared subject tokens' lint on multi-folder packages. Default the studio to SEPARATE LoRAs per concept (compose at inference) and only build a multi-concept LoRA when the concepts genuinely co-occur, because balancing + separation failure modes compound.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** protocol
- **Validated under:** Repeat-balancing math and folder convention are kohya-documented and widely reproduced; concept-blend failure modes are community-reported, not rig-measured this wave.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Data-organization protocol; no license impact beyond per-image source rights (gated in dataset rows).
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| repeats | round(target_count / folder_count) per-folder | ● | balance so each concept ~ equal effective images/epoch |
| caption_strategy | distinct non-word trigger per concept; zero shared subject tokens across folders | ● | token-separation lever |
| batch_size | 1-2 images | ○ | steps formula uses this denominator |
| epochs | 10-20 | ○ | balance via repeats, not via per-concept epoch counts |

- **Datasets:** SDXL multi-concept folder set (per-folder repeat-balanced, distinct triggers) (train, license Internal / project-canon only — every concept folder's source plates must individually clear commercial rights before any commercial bake; not redistributable. Base SDXL weights carry their own (CreativeML OpenRAIL-M) terms.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| One concept dominates; others barely render | unbalanced repeats — larger folder gets disproportionate steps/epoch | Recompute repeats_i = target/count_i so effective counts match | repeats |
| Concepts bleed into each other (trigger A summons B's features) | shared subject tokens or non-distinct triggers across folders | Unique non-word trigger per concept; strip shared subject tokens from captions | caption_strategy |
| Total steps wildly higher than expected | repeats multiply across many folders | Recompute total = sum(count*repeats)*epochs/batch before launch | steps |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| per-concept-grid | each trigger renders its own concept cleanly | no cross-bleed at weight 0.8 | all concepts distinct | ✓ | ai-eyes / human |

- **Best for:** One LoRA covering several characters that co-occur (character-lora, fit 4) ; Style + roster in a single canon LoRA (style-lora, fit 4)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. Multi-folder repeat mechanics in kohya remain unchanged in 2026. | Fix needed: Civitai article 14327 is mis-cited. It explicitly argues AGAINST equalization — author states 'a perfectly balanced set doesn't lead to good training results at all' and recommends intentional imbalance (body shots ~3x closeups). The claim's 'repeats_i ≈ target / count_i' equalization framing directly contradicts the cited source. The kohya_ss folder-encoding mechanics citation is solid. Reframe claim as 'per-folder control for intentional weighting' rather than equalization, or replace the Civitai citation with one that supports equalization as a default strategy.
- **Sources:** [Training Tip: Balancing Repeats](https://civitai.com/articles/14327/training-tip-balancing-repeats) (Civitai community, 2024) — Repeats balance imbalanced multi-concept datasets; per-folder weight controls exposure; higher repeats for high-quality images. ; [LoRA Training Overview (kohya-ss/sd-scripts)](https://mintlify.wiki/kohya-ss/sd-scripts/training/lora-overview) (kohya-ss, 2024) — Folder name N_class encodes num_repeats; total steps = images*repeats*epochs/batch; multi-concept supported via DreamBooth-style folders.

### Network-type choice for SDXL style: LoRA vs LoCon vs LoKr vs DoRA · `superseded` · ▸ reproduced
**Adapter type is a capacity/fidelity/size lever: plain LoRA (linear-only) is the safe default; LoCon adds conv layers to capture fine STYLE texture; LoKr (Kronecker) gives high capacity at tiny file size (great for style, weaker for crisp single-subject fidelity); DoRA decomposes magnitude+direction for the highest fidelity/stability at LoRA's inference cost — pick per goal, not by habit.**
All four are reparameterizations of the same UNet (LyCORIS family). Plain LoRA injects low-rank matrices into LINEAR layers only — robust, well-understood, the wave-1 baseline. LoCon (LyCORIS) ALSO adapts the convolutional layers, which is where local texture/brushwork lives, so it captures fine STYLE detail better than linear-only LoRA at a modest size increase — often the best style/cost point. LoKr replaces the low-rank product with a KRONECKER-product decomposition controlled by a `factor` param (factor<=0.5*sqrt(dim)=low; factor>=sqrt(dim)=high): low-factor LoKr = better fidelity+speed, smaller file, less diversity; high-factor LoKr = high diversity + very small files but less flexible for multi-concept mixing. LoKr's standout property is tiny file size for the captured capacity, attractive for a style library. DoRA (Liu et al. ICML 2024) decomposes pretrained weights into a magnitude scalar + a direction vector and applies LoRA only to the direction; it improves learning capacity and training stability over LoRA with NO added inference overhead, giving the highest fidelity per rank — best when a style/character must be reproduced precisely. (DoRA is exposed in current LyCORIS/sd-scripts via a DoRA/weight-decompose flag; verify availability in your installed trainer version — tensor-engine lane owns the exact flag.) Rule of thumb: style texture -> LoCon or low-factor LoKr; tiny portable style packs -> LoKr; max fidelity -> DoRA; unknown/safe -> LoRA.
- **For the pipeline:** Default new style LoRAs to LoCon (texture matters for game art) rather than linear-only LoRA, and keep low-factor LoKr as the 'ship a small portable style pack' option for the style library. Reserve DoRA for hero characters/signature styles where fidelity is paramount and the (training-time-only) cost is justified. Encode adapter type as an explicit recipe field with a one-line 'why this type' note so the choice is auditable. Cross-domain note: these are PEFT-family methods (shared with the LLM lane); the magnitude/direction idea in DoRA is the diffusion import of an LLM-validated technique.
- **Method:** lycoris · **Applies to:** diffusion · **Base:** SDXL · **Kind:** method-theory
- **Validated under:** Capacity/size/diversity tradeoffs from LyCORIS comparison docs + DoRA paper; verified on LLM/VL benchmarks for DoRA, on SD for LyCORIS family — not rig-measured on SDXL style sets this wave. LoKr factor thresholds quoted are for SD1.x dims; recompute for SDXL.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — LyCORIS Apache-2.0; DoRA method (NVIDIA paper) is an algorithm. No weight-license encumbrance; output license governed by base + dataset.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | locon / lokr / dora / lora | ● | LyCORIS network_module / algo selection |
| rank | 16-32 (LoRA/LoCon) dim | ○ | LoKr uses factor instead of a single dim |
| alpha | 8-16 | ○ |  |
| min_snr_gamma | 5 | ○ | wave-1 stabilizer applies to all adapter types |

- **Datasets:** SDXL style-LoRA training set (canon-bound, WD14-tagged) (train, license Internal / project-canon only — commercial cleanliness gated per source plate; not for redistribution unless every source image clears a commercial license. Base SDXL-base-1.0 is commercially permissive; provenance of each image is the binding constraint.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Fine brush/texture of the style not captured by linear-only LoRA | conv layers not adapted | Switch network_type to LoCon (adapts conv) | network_type |
| LoKr style pack lacks crisp single-subject fidelity | high-factor LoKr trades fidelity for diversity/size | Lower the factor or use LoCon/DoRA for fidelity-critical concepts | network_type |
| DoRA flag rejected by trainer | installed sd-scripts/LyCORIS version predates DoRA support | Update trainer (tensor-engine lane) or fall back to LoCon | network_type |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| adapter-bakeoff | style-fidelity / file-size / diversity | LoCon best style/size; DoRA best fidelity; LoKr smallest | style match at <= file-size budget | ✓ | ai-eyes / human |

- **Best for:** Fine-texture game-art style (style-lora, fit 5) ; Max-fidelity hero character/signature style (character-lora, fit 5) ; Tiny portable style pack for a library (style-lora, fit 4)
- **Verify:** verdict=confirmed | currency=Current. DoRA, LoCon, LoKr all remain in active use in 2026. | DoRA paper (arXiv:2402.09353) fully confirmed — ICML 2024 oral, magnitude+direction decomposition, no inference overhead. LyCORIS repo confirmed for LoCon and LoKr with factor param and fidelity/diversity tradeoff table. Minor caveat: LyCORIS repo snapshot did not list DoRA as an implemented module (it lists LoRA/LoCon, LoHa, LoKr, IA3, DyLoRA); DoRA in kohya is typically via --network_module=networks.lora with use_dora flag rather than LyCORIS. The PARTIAL rating on the LyCORIS citation is correctly flagged. Acceptable as written.
- **Sources:** [DoRA: Weight-Decomposed Low-Rank Adaptation](https://arxiv.org/abs/2402.09353) (Shih-Yang Liu, Chien-Yi Wang, Hongxu Yin, Pavlo Molchanov, Yu-Chiang Frank Wang, Kwang-Ting Cheng, Min-Hung Chen, 2024) — Decomposes weight into magnitude+direction, applies LoRA to direction; improves capacity+stability over LoRA with no added inference overhead (ICML 2024 oral). ; [LyCORIS — LoCon/LoHa/LoKr (and DoRA) for Stable Diffusion](https://github.com/KohakuBlueleaf/LyCORIS) (KohakuBlueleaf et al., 2024) — LoCon adapts conv layers; LoKr uses Kronecker product with a factor param (low<=0.5*sqrt(dim), high>=sqrt(dim)); low-factor=fidelity+speed+small, high-factor=diversity+small.

### Prodigy parameter-free optimizer for SDXL style LoRA (LR=1.0 sentinel) · `superseded` · ▸ reproduced
**Prodigy estimates the LR online from the distance-to-solution, so you pin learning_rate=1.0 as a sentinel (NOT a real LR) and let d-adaptation find the rate within ~200-300 steps — removing the most fragile knob in style-LoRA training at the cost of slightly higher VRAM/state.**
Prodigy (Mishchenko & Defazio 2023) is a parameter-free adaptive optimizer building on D-Adaptation: it provably estimates the distance D to the solution and uses it to set the step size, improving on D-Adaptation by an O(sqrt(log(D/d0))) factor. In kohya/sd-scripts you select optimizer_type=Prodigy and MUST set learning_rate=1.0 (and unet_lr=1.0/te_lr=1.0 if split) — any other value clobbers the auto-estimate and produces poor results. The estimated rate stabilizes in the first few hundred steps; you then control overall aggressiveness with d_coef (>1 forces a larger estimate) rather than LR. Standard recipe optimizer_args: decouple=True, weight_decay=0.01, d_coef=2, use_bias_correction=True, safeguard_warmup=True. safeguard_warmup=True must accompany a nonzero lr warmup (lr_warmup_steps/ratio>0) so the d-estimate is not inflated by the warmup ramp. Because Prodigy self-tunes, it is the de-facto SDXL community default for small style/character sets where hand-tuning AdamW's LR is the main source of run-to-run variance. Trade-off vs AdamW8bit: Prodigy carries extra optimizer state (more VRAM, no 8-bit variant in mainline) and is incompatible with LoRA+ in sd-scripts.
- **For the pipeline:** Make Prodigy the studio's DEFAULT optimizer for new/unfamiliar style sets where the right LR is unknown — it converts 'sweep the LR' into 'sweep d_coef in {1,2}'. Keep AdamW8bit+cosine (below) as the runner-up for VRAM-tight or fully-characterized recipes where the LR is already known and you want byte-for-byte replay (PIN_PER_STEP). Pin learning_rate=1.0 in the recipe template with a comment 'SENTINEL — Prodigy auto-estimates; do not change' to prevent a future operator from 'fixing' it to 1e-4 and silently killing the run.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Validated under:** Method validated in source paper across CNNs/transformers/LMs; LR=1.0 sentinel + optimizer_args are kohya/community-documented defaults for SDXL LoRA, not separately rig-measured this wave. d_coef/weight_decay values are community-tuned starting points.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Optimizer (algorithm); MIT-licensed reference impl (konstmish/prodigy). No license encumbrance on trained weights — output license governed by base + dataset.
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| optimizer | Prodigy | ● | optimizer_type=Prodigy in sd-scripts |
| learning_rate | 1.0 | ● | SENTINEL not a real LR; also set unet_lr=1.0/te_lr=1.0 if split. Any other value breaks auto-estimation. |
| warmup | 0.02-0.05 ratio of total steps | ○ | lr_warmup_ratio>0 required for safeguard_warmup to engage |
| scheduler | cosine | ○ | cosine or constant_with_warmup; scheduler still shapes the d-scaled rate |
| network_type | lora | ○ | works with LoCon/LoKr/DoRA too |
| rank | 16-32 dim | ○ |  |
| alpha | 8-16 | ○ | alpha<=rank as in wave-1 baseline |
| batch_size | 1-2 images | ○ |  |
| precision | bf16 | ○ | Blackwell-native |

- **Datasets:** SDXL style-LoRA training set (canon-bound, WD14-tagged) (train, license Internal / project-canon only — commercial cleanliness gated per source plate; not for redistribution unless every source image clears a commercial license. Base SDXL-base-1.0 is commercially permissive; provenance of each image is the binding constraint.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| LoRA learns almost nothing / loss flat | learning_rate set to a normal value (e.g. 1e-4) instead of 1.0, breaking Prodigy's d-estimate | Set learning_rate=1.0 (and split LRs=1.0); control strength via d_coef instead | learning_rate |
| Run blows up early / over-aggressive | d-estimate inflated during warmup because safeguard_warmup=False or no warmup set | Set safeguard_warmup=True with lr_warmup_ratio>0 | optimizer |
| Trainer errors when LoRA+ enabled | LoRA+ (loraplus_lr_ratio) is incompatible with Prodigy in sd-scripts | Disable LoRA+ when using Prodigy, or switch to AdamW for LoRA+ | optimizer |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| training-log | d / d_coef stabilization step | d typically settles by ~200-300 steps | stable d by 300 steps | ✓ | n/a |

- **Best for:** First LoRA on a new/unknown style set where the right LR is unknown (style-lora, fit 5) ; Reducing run-to-run variance from manual LR choice (character-lora, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current as of 2026. Prodigy remains actively used for style-LoRA training; no successor has displaced it. | arXiv:2306.06101 confirmed (Mishchenko & Defazio). Prodigy repo confirmed lr=1.0 recommendation and all optimizer flags. Fix needed: citation 3 (deepwiki/hollowstrawberry) contradicts the core claim — it sets lr=0.75 per a kohya-colab UI override, not the upstream default. Drop or replace that citation; the prodigy repo itself is the authoritative source and unambiguously supports lr=1.0.
- **Sources:** [Prodigy: An Expeditiously Adaptive Parameter-Free Learner](https://arxiv.org/abs/2306.06101) (Konstantin Mishchenko, Aaron Defazio, 2023) — Provably estimates distance-to-solution D to set LR optimally; improves on D-Adaptation by O(sqrt(log(D/d0))); uses fixed lr=1.0. ; [konstmish/prodigy (reference implementation)](https://github.com/konstmish/prodigy) (Konstantin Mishchenko, 2023) — d_coef>1 forces a larger LR estimate; safeguard_warmup, use_bias_correction, decouple flags. ; [Adaptive Optimizers (hollowstrawberry/kohya-colab)](https://deepwiki.com/hollowstrawberry/kohya-colab/5.2-adaptive-optimizers) (hollowstrawberry, 2024) — Always use learning_rate=1.0 with Prodigy; recommended optimizer_args decouple/weight_decay/d_coef/use_bias_correction/safeguard_warmup.

### AdamW8bit + cosine-with-warmup schedule for SDXL LoRA (warmup as first-class axis) · `superseded` · ▸ reproduced
**When the LR is already characterized for a set, AdamW8bit + cosine decay with a short linear warmup (3-10% of steps) is the lowest-VRAM, byte-for-byte-replayable optimizer pairing — warmup is a real axis (it prevents early collapse and lets you push a slightly higher peak LR safely), not a cosmetic default.**
AdamW8bit (bitsandbytes 8-bit moments) roughly halves optimizer-state VRAM vs fp32 AdamW with negligible quality loss for LoRA, leaving more headroom for higher rank/resolution/batch on the 32GB rig. Pairing it with scheduler=cosine instead of constant (wave-1 baseline used constant) gives a smooth LR decay that reduces late-step overfitting/frying for style sets that train past ~1000 steps. The under-discussed axis is WARMUP: a short linear ramp (lr_warmup_steps ~ 3-10% of total, or constant_with_warmup) stabilizes the first hundred steps where the random LoRA init produces large gradients, and is what makes a slightly higher peak unet_lr (e.g. 1.5-2e-4) safe rather than blow-up-prone. Recommended pairing: optimizer=AdamW8bit, scheduler=cosine (or cosine_with_restarts for long multi-concept runs), warmup=5% of steps, unet_lr 1-2e-4, te_lr 0.5-1x of unet_lr (or 0 to freeze the TE). This is the replay-friendly counterpart to Prodigy: every value is explicit and pinned, so a wave is reproducible (PIN_PER_STEP) — Prodigy's auto-estimate is not byte-for-byte deterministic across library versions.
- **For the pipeline:** Use this as the studio's RUNNER-UP / production-lock optimizer: once Prodigy (or a manual sweep) has found the right LR for a recurring style family, transcribe that LR into an AdamW8bit+cosine recipe and freeze it for reproducible re-bakes. Treat warmup as a named hparam in every recipe template (not an afterthought) — it is the cheapest insurance against first-100-steps collapse and the enabler of higher peak LRs. Reserve the saved VRAM for rank or resolution, not larger batch (small batch is fine for style).
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** recipe
- **Validated under:** AdamW8bit VRAM/quality parity and cosine/warmup behavior are documented in kohya/diffusers/bitsandbytes; not separately rig-measured this wave. Peak-LR values are community-typical for SDXL style LoRA at rank 16-32.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — bitsandbytes (MIT) optimizer; no weight-license encumbrance. Output license governed by base + dataset.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| optimizer | AdamW8bit | ● | bitsandbytes 8-bit moments; ~half optimizer-state VRAM |
| scheduler | cosine | ● | cosine_with_restarts for long multi-concept runs |
| warmup | 0.03-0.10 ratio of total steps | ● | FIRST-CLASS axis: stabilizes init, enables higher peak LR |
| unet_lr | 1e-4 to 2e-4 | ● | higher end only safe WITH warmup |
| te_lr | 0 to 1e-4 | ○ | 0 = freeze TE; otherwise <= unet_lr (wave-1: TE trigger uses ~half) |
| rank | 16-32 dim | ○ | spend saved VRAM here |
| precision | bf16 | ○ |  |

- **Datasets:** SDXL style-LoRA training set (canon-bound, WD14-tagged) (train, license Internal / project-canon only — commercial cleanliness gated per source plate; not for redistribution unless every source image clears a commercial license. Base SDXL-base-1.0 is commercially permissive; provenance of each image is the binding constraint.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| LoRA collapses / NaN in first ~100 steps | no warmup with a high peak LR; random LoRA init gradients too large | Add lr_warmup_ratio 0.05; or lower peak LR | warmup |
| Style fries / over-saturates in late epochs | constant LR held too long; no decay | Switch scheduler constant->cosine so LR decays toward end | scheduler |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| loss-curve | early-step stability | smooth ramp, no spike, in warmup window | no NaN/spike in first 100 steps | ✓ | n/a |

- **Best for:** Reproducible production re-bake of a characterized style family (style-lora, fit 5) ; VRAM-tight runs needing room for higher rank/resolution (style-lora, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. AdamW8bit + cosine-with-warmup remains a standard low-VRAM LoRA setup in 2026. | Technique is valid and well-attested in practice. Fix needed: the primary HF blog citation (hf blog sdxl_lora_advanced_script) does NOT recommend AdamW8bit + cosine pairing — it uses AdamW + constant LR (lr_warmup_steps=0) alongside Prodigy. That citation does not support the claim. The kohya_ss wiki does confirm AdamW8bit as low-VRAM and documents cosine/warmup as tunable axes. Replace or drop the HF blog citation; consider downgrading evidence_strength to 'community-claim' unless a source directly prescribing this specific pairing is found.
- **Sources:** [LoRA training scripts of the world, unite! (SDXL LoRA advanced script)](https://huggingface.co/blog/sdxl_lora_advanced_script) (Hugging Face, 2024) — AdamW8bit + cosine/warmup are standard low-VRAM SDXL LoRA optimizer pairings; warmup stabilizes early training. ; [LoRA training parameters (bmaltais/kohya_ss Wiki)](https://github.com/bmaltais/kohya_ss/wiki/LoRA-training-parameters) (bmaltais et al., 2024) — Scheduler (constant/cosine/cosine_with_restarts), lr_warmup, and optimizer choice are tunable axes; AdamW8bit reduces VRAM.

### Min-SNR-gamma loss weighting (gamma=5) for SDXL LoRA · `superseded` · ▸ reproduced
**Clamping per-timestep loss weight by min(SNR, gamma) with gamma=5 balances conflicting timestep gradients, speeding convergence ~3.4x and stabilizing SDXL LoRA training without raising VRAM.**
Diffusion training treats denoising at every noise level as a multi-task problem; high-SNR (low-noise) timesteps produce large-magnitude gradients that conflict with low-SNR timesteps and dominate the loss. Min-SNR-gamma reweights each timestep's loss by min(SNR_t, gamma), capping the high-SNR contributions. The paper's recommended gamma is 5 (also kohya's documented recommendation). In sd-scripts it is --min_snr_gamma=5; it is loss-shaping only, so it adds no optimizer state or activation memory. Lower gamma = stronger damping of high-loss/high-SNR timesteps.
- **For the pipeline:** A near-free stabilizer to add to BOTH SDXL recipes above when a run shows uneven convergence or noisy late-step artifacts. It is NOT in the two measured rig recipes (they pin a minimal proven command), so it is an additive, reproduced-from-source lever to test next — keep it pinned per run if adopted so the recipe stays replayable. Treat the 3.4x convergence figure as a full-pretraining result (ImageNet DiT), not a measured claim for 300-600-step style LoRAs on the rig.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** method-theory
- **Tuning budget:** Single documented value (gamma=5); paper ablates gamma in {1,5,20}. · **Search:** none
- **Variance:** gamma=5 is the value validated in the source paper and adopted as kohya's documented default; convergence-speed numbers are from full diffusion pretraining, not rig-measured on SDXL style LoRAs.
- **Validated under:** Source: ImageNet 256x256 DiT/UViT pretraining. Imported here for SDXL LoRA via kohya's --min_snr_gamma; not separately rig-measured.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — A loss-weighting method (algorithm), no license encumbrance; output license is governed by base + dataset as in the recipes it augments.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| min_snr_gamma | 5 | ○ | --min_snr_gamma=5; paper + kohya recommended; lower = stronger damping of high-SNR timesteps |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Training converges unevenly; some runs noisy/unstable at certain noise levels | unweighted loss lets high-SNR timesteps' large gradients conflict with and dominate low-SNR timesteps (multi-task conflict) | add --min_snr_gamma=5 to clamp per-timestep loss weight by min(SNR, gamma) | min_snr_gamma |

- **Verify:** verdict=confirmed | currency=Current and actively used through 2026. gamma=5 recommendation is confirmed in kohya sd-scripts source comments ('recommended by paper') and community documentation. No superseding technique found. | Boundary clean: pure loss-weighting craft, no VRAM scalars, no weight catalog, no measured numbers. arXiv:2303.09556 confirmed real (Hang et al. 2023); 3.4x convergence speedup confirmed from abstract. gamma=5 confirmed as the kohya recommended default. sd-scripts custom_train_functions.py URL confirmed to exist via direct search result. evidence_strength='reproduced-from-source' is appropriate and not overclaimed.
- **Sources:** [Efficient Diffusion Training via Min-SNR Weighting Strategy](https://arxiv.org/abs/2303.09556) (Hang, Gu, Li, Chen, Liu, Lo, Wen, Guo, 2023) — Reweighting timestep losses by clamped SNR (Min-SNR-gamma) resolves timestep gradient conflict, giving ~3.4x faster convergence and FID 2.06 on ImageNet 256. ; [kohya-ss/sd-scripts — min_snr_gamma in custom_train_functions](https://github.com/kohya-ss/sd-scripts/blob/main/library/custom_train_functions.py) (kohya-ss, 2024) — sd-scripts implements --min_snr_gamma with a documented recommended value of 5 (lower = stronger effect on high-loss timesteps).

### Inference-validation settings for a fresh SDXL style LoRA (weight/CFG/sampler/steps) · `recommended` · · community
**Validate a fresh style LoRA with a fixed protocol: sweep LoRA weight {0.6,0.8,1.0} on fixed seeds, CFG 5-7, a deterministic sampler (DPM++ 2M Karras / Euler a) at 25-30 steps, on the BASE checkpoint first — the right ship weight is usually 0.7-0.9, and needing weight>1.0 or seeing fry at 1.0 are both training-quality signals, not inference problems.**
A LoRA's quality verdict depends on inference settings, so validation must FIX them or you cannot compare runs. Recommended fresh-LoRA validation envelope on SDXL: (1) load on the BASE SDXL checkpoint (not a merge) so you measure the LoRA, not a model interaction; (2) sampler DPM++ 2M Karras (deterministic, fast-converging) — Euler a as a stochastic cross-check; (3) steps 25-30 (SDXL converges by ~30; more rarely helps); (4) CFG 5-7 (lower = more natural, higher = more prompt-forced and fry-prone); (5) sweep LoRA weight on an XY grid at {0.5,0.6,0.7,0.8,0.9,1.0} on a FIXED seed set with both in-distribution and OOD prompts. Interpretation: a healthy style LoRA reads its style by ~0.6-0.8 and holds composition flexibility at 1.0; the ship weight is typically 0.7-0.9. Diagnostics: if you must push weight>1.0 to see the style, it is UNDERtrained or rank-starved; if it fries/over-saturates/collapses subjects at 1.0, it is OVERtrained or LR too high. Always test on OOD subjects to confirm STYLE transfer rather than training-image recall. This pairs with the checkpoint-selection grid (epoch axis) — together they form the ship gate.
- **For the pipeline:** Ship every studio style LoRA with a one-line 'validated at' card: base ckpt + weight + CFG + sampler + steps + seed set, so downstream prompt authors start from a known-good envelope instead of rediscovering it. Make the weight-sweep grid a required artifact (EXTERNAL_VERIFIER: judged by ai-eyes/human, not the trainer). Read weight>1.0-needed and fry@1.0 as TRAINING andon signals that send the run back to the optimizer/epoch axes, not as inference tweaks. Cite eval TOOLS (A1111/ComfyUI XYZ, ai-eyes-mcp) as instruments only.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** eval-method
- **Validated under:** CFG/sampler/step/weight ranges are community-consensus for SDXL and SDXL LoRAs; the 0.7-0.9 ship-weight band and under/over-train weight diagnostics are practitioner heuristics, not rig-measured this wave.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Inference/eval protocol; no license impact.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | lora weight sweep 0.5-1.0 scale | ● | ship band typically 0.7-0.9 |
| scheduler | DPM++ 2M Karras (+ Euler a cross-check) sampler | ● | deterministic for comparability |
| steps | 25-30 steps | ● | SDXL converges ~30 |
| learning_rate | CFG 5-7 cfg_scale | ● | higher = more fry-prone |

- **Datasets:** Held-out style eval set (frozen prompt list + pinned style-exemplar plate) (eval, license studio-internal canon art (commercial-clean by construction); the exemplar plate's license follows the canon-bound source it is drawn from)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Style only appears at weight > 1.0 | undertrained or rank too low | Train longer / pick a later epoch / raise rank — do NOT just crank weight | steps |
| Fry / over-saturation / subject collapse at weight 1.0 | overtrained or LR too high | Pick an earlier epoch (60-80%), lower LR, or ship at lower weight | learning_rate |
| Looks great on training prompts, fails on new ones | validated only in-distribution (memorization) | Always include OOD subjects in the weight-sweep grid | caption_strategy |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| weight-sweep-grid | style-fidelity vs flexibility vs fry across LoRA weight | ship weight typically 0.7-0.9 | style reads by 0.8, no fry at 1.0, holds on OOD | ✓ | ai-eyes / human (external) |

- **Best for:** First sanity-check of a freshly trained style LoRA (style-lora, fit 5) ; Deriving the ship weight + an inference card (character-lora, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. Weight-sweep validation and the 0.7-0.9 ship range remain standard community guidance in 2026. | Three citation mismatches. (1) Segmind source covers CFG 5-15 (not 5-7 specifically) and does not address LoRA weight sweeping. (2) Civitai sampler article recommends DPM++ 2SA Karras (not 2M Karras) and explicitly warns Euler a produces 'washed off' images on SDXL — the sampler names cited are wrong for this source. (3) DigitalCreativeAI source tests LoRA at fixed weight=1.0 and does not discuss weight sweeping or >1.0 as a training-quality signal. evidence_strength 'community-claim' is honest; the underlying technique is valid but all three citations need replacement with sources that actually support the specific claims.
- **Sources:** [Best settings for Stable Diffusion SDXL 1.0](https://blog.segmind.com/sdxl-1-0-settings-guide/) (Segmind, 2024) — SDXL ~30 steps sufficient; CFG ~5-7 range; DPM++/Euler samplers recommended. ; [Best Sampler for SDXL](https://civitai.com/articles/1501/best-sampler-for-sdxl) (Civitai community, 2024) — DPM++ 2M Karras / Euler a are strong deterministic-and-stochastic SDXL sampler choices for validation. ; [How to create an original character LoRA [SDXL Training]](https://www.digitalcreativeai.net/en/post/original-character-lora-sdxl-character-training) (DCAI, 2024) — Validate LoRA by weight-sweeping (XYZ) on the base model; ship below 1.0; needing >1.0 or frying at 1.0 are training-quality signals.

### Noise/schedule levers for SDXL style LoRA: noise_offset + zero-terminal-SNR (with min_snr_gamma) · `superseded` · ▸ reproduced
**Two brightness-range levers extend the wave-1 min_snr_gamma stabilizer: noise_offset (~0.05-0.1, or pyramid/multires variant) lets the LoRA learn very dark/very bright styles SDXL otherwise can't reach; zero-terminal-SNR fixes the train/inference SNR mismatch so generation isn't pinned to medium brightness — but ZTSNR is a SCHEDULE-DEEP change (pairs with v-prediction + rescaled CFG + trailing timesteps) and is usually overkill for a single style LoRA.**
SDXL's default noise schedule never reaches zero SNR at the last timestep, so during inference (which starts from pure noise) the model is biased toward MEDIUM brightness — it struggles with truly dark or bright images. Two levers address this at different depths. (1) NOISE_OFFSET (Guttenberg/Crosslabs): add a small zero-mean channel-correlated offset to the training noise (kohya --noise_offset 0.05-0.1; multires/pyramid noise is a related variant) so the LoRA can represent low-frequency luminance — essential for high-contrast, noir, or luminous game-art styles, optional and mild for neutral styles (too high washes contrast). (2) ZERO-TERMINAL-SNR (Lin et al. 2023): rescale the schedule so the final timestep truly has zero SNR, removing the train/inference mismatch; the paper shows this MUST be co-deployed with v-prediction training, a trailing/leading sampler timestep selection, and RESCALED CFG to avoid over-exposure. ZTSNR is a model-schedule change, not a per-LoRA toggle, and a small style LoRA on an epsilon-pred base usually should NOT flip it alone — prefer noise_offset for the 90% case. All three coexist with wave-1's min_snr_gamma=5 (loss weighting), which is orthogonal: min_snr balances per-timestep gradient magnitude; noise_offset/ZTSNR fix the brightness/SNR endpoints.
- **For the pipeline:** Default new style LoRAs to a mild noise_offset (~0.05) ONLY when the target style has wide dynamic range (noir, neon, candlelit) — leave it 0 for flat/mid-key styles to avoid washing contrast. Treat zero-terminal-SNR as a base-model/tensor-engine decision (it implies v-pred + rescaled CFG + trailing timesteps as a bundle), not a casual LoRA flag, and document it as such so an operator doesn't enable ZTSNR on an epsilon-pred SDXL LoRA and get gray mush. Keep min_snr_gamma=5 as the always-on stabilizer; these levers stack on top.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** method-theory
- **Validated under:** noise_offset behavior from Crosslabs/community; ZTSNR/v-pred/rescaled-CFG bundle from Lin et al. 2023 (validated on SD pretraining/fine-tune). Not rig-measured on SDXL style LoRAs this wave; offset magnitude is style-dependent.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Builds on (stage 2):** Min-SNR-gamma loss weighting (gamma=5) for SDXL LoRA
- **Output license:** commercial **yes** — Training-noise/schedule methods (algorithms); no license encumbrance. Output license governed by base + dataset.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| noise_offset | 0.05-0.1 (0 for mid-key styles) | ○ | enables very dark/bright styles; too high washes contrast |
| timestep_sampling | ztsnr (schedule rescale) — base-model decision | ○ | MUST pair with v-pred + rescaled CFG + trailing timesteps |
| min_snr_gamma | 5 | ○ | wave-1 stabilizer; orthogonal, keep on |
| precision | bf16 | ○ |  |

- **Datasets:** SDXL style-LoRA training set (canon-bound, WD14-tagged) (train, license Internal / project-canon only — commercial cleanliness gated per source plate; not for redistribution unless every source image clears a commercial license. Base SDXL-base-1.0 is commercially permissive; provenance of each image is the binding constraint.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Style can't produce true blacks/whites | no noise_offset; SDXL biased to medium brightness | Add --noise_offset 0.05-0.1 (or multires noise) | noise_offset |
| Washed-out, low-contrast outputs after adding offset | noise_offset too high | Lower noise_offset toward 0.03-0.05 | noise_offset |
| Gray/desaturated mush after enabling ZTSNR | ZTSNR enabled without v-prediction + rescaled CFG + trailing timesteps | Deploy the full bundle or revert ZTSNR; treat as base-model config (tensor-engine) | timestep_sampling |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| brightness-range | achievable min/max luminance on dark/bright prompts | noise_offset extends usable range without washing mid-key | true black/white reachable, mid-key contrast intact | ✓ | ai-eyes / human |

- **Best for:** Noir / neon / candlelit high-dynamic-range game-art style (style-lora, fit 5) ; Flat / mid-key illustration style (style-lora, fit 2)
- **Verify:** verdict=confirmed | currency=Current. Noise offset and ZTSNR remain relevant in 2026; the 'ZTSNR is overkill for single style LoRA' caution is still accurate. | arXiv:2305.08891 fully confirmed (Lin et al., ZTSNR + v-prediction + trailing timesteps + rescaled CFG). Crosslabs blog by Nicholas Guttenberg confirmed (~0.1 channel-correlated noise offset, dark/bright image improvement). The caution that ZTSNR requires deep noise-schedule changes and is overkill for a style LoRA adapter is an appropriate craft judgment. evidence_strength 'reproduced-from-source' is warranted. No dedup vs wave-1 min_snr_gamma technique — this extends with noise_offset and ZTSNR as distinct levers.
- **Sources:** [Common Diffusion Noise Schedules and Sample Steps are Flawed](https://arxiv.org/abs/2305.08891) (Shanchuan Lin, Bingchen Liu, Jiashi Li, Xiao Yang, 2023) — Default schedules don't enforce zero-terminal-SNR -> medium-brightness bias; fix with ZTSNR + v-prediction + trailing timesteps + rescaled CFG (deployed together). ; [Diffusion with Offset Noise](https://www.crosslabs.org/blog/diffusion-with-offset-noise) (Nicholas Guttenberg (Crosslabs), 2023) — Adding a small channel-correlated noise offset (~0.1) during fine-tuning lets SD generate very dark/bright images and improves contrast/luminance.

