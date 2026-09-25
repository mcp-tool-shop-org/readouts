# Flux-family style-LoRA recipes
_A SEPARATE recipe space from SDXL (flow-matching, not DDPM). Commercial-safe Apache-2.0 bases only (FLUX.2 [klein], Chroma1-HD); FLUX.1-dev/FLUX.2-dev are non-commercial and must not be a training base here. Higher rank, NL captions, frozen T5, fp8 base, no prior-preservation by default._ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

14 techniques · 10 recommended · 5 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 1 | Chroma LoRA eval/inference on the rig — kohya samplers give NOISE; use flux_minimal_inference fp8 + REAL CFG (the scriptable path) | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Chroma LoRA rank/dim sweep (8/16/32) — MEASURED on the 5090 (size linear; higher rank binds the saturated palette more completely — unlike SDXL) | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Chroma discrete_flow_shift sweep (1/3/6) — MEASURED (footprint-neutral; shift 6 marginally best fidelity; weakest lever) | lora | diffusion | ▣ measured | ✅ yes | 5 | 4 | ✓ |
| 1 | Chroma1-HD base-swap style-LoRA (kohya flux_train_network --model_type chroma) — measured on the 5090 | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | fp8_base is REQUIRED for Chroma LoRA on 32 GB — bf16 + live T5 spills the card (MEASURED 31974 MiB / 34 s/it) | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 2 | FLUX.2 [klein] 4B Apache-2.0 undistilled-base style-LoRA (Qwen3 encoder, real CFG, 32GB-comfortable) | lora | diffusion | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 2 | Flow-matching shift schedule depth - discrete_flow_shift, resolution-aware shift, and sigmoid vs shift vs flux_shift | lora | diffusion | ▸ reproduced | ✅ yes | 4 | 4 | ✓ |
| 2 | Flow-matching training schedule (sigmoid/shift timestep + raw prediction) — why Flux is a separate recipe space from SDXL/DDPM | lora | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Flux LoRA serving - keep it as a runtime adapter, merge only to bake fp8, and there is no generic LoRA->base converter | lora | diffusion | ▸ reproduced | ✅ yes | 4 | 5 | ✓ |
| 2 | Rank/dim/alpha choice for Flux DiT style-LoRA vs SDXL UNet - lower ranks go further on Flux | lora | diffusion | ▸ reproduced | ✅ yes | 4 | 5 | ✓ |
| 2 | fp8 vs bf16 base precision for Flux LoRA training in 32GB - bf16 is the quality floor, fp8/int8 buys headroom not speed-for-free | lora | diffusion | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 6 | NL captioning depth for frozen-encoder Flux/klein - JoyCaption vs Florence-2 vs CogVLM2, length budget, and the T5/Qwen3 freeze | lora | diffusion | · community | ⚠ cond | 4 | 5 | ✓ |
| 6 | Natural-language caption craft for frozen-encoder Flux LoRA (JoyCaption / Florence-2) | lora | diffusion | · community | ⚠ cond | 5 | 5 | ✓ |
| 6 | The guidance-distilled-base training problem (FLUX.1-dev/FLUX.2-dev) - train at guidance_scale=1.0, reintroduce CFG at sampling | lora | diffusion | ▸ reproduced | ⛔ no | 4 | 3 | ✓ |

## Detail

### Chroma LoRA eval/inference on the rig — kohya samplers give NOISE; use flux_minimal_inference fp8 + REAL CFG (the scriptable path) · `recommended` · ▣ measured
**MEASURED this wave: generating a scriptable Chroma LoRA eval grid is NOT the SDXL lycoris trick. kohya's flux training-sampler (--sample_at_first) emits PURE RGB NOISE for Chroma, and so does flux_minimal_inference.py at cfg_scale 1.0. The fix: Chroma needs REAL CFG (--cfg_scale ~4 + a negative prompt), not the flux distilled-guidance path. The working, RAM-lean eval path is flux_minimal_inference.py --model_type chroma --flux_dtype fp8 (NO --offload; ~25-28 GB VRAM, ~30% system RAM), --guidance 0 --cfg_scale 4 --negative_prompt, 26 steps, LoRA strength ~3.0.**
#168 always validated Chroma in ComfyUI (UNETLoader + ModelSamplingAuraFlow shift 1.0 + CFGGuider cfg 4); kohya CLI Chroma inference was never proven. This wave establishes a scriptable CLI eval path. Strength ~3.0 is needed (vs ComfyUI's ~1.5) because flux_minimal_inference does not replicate AuraFlow shift 1.0 — a consistent, fair inference for within-Chroma comparison. Interactive mode loads the model once and batches all 20 prompts/config. The earlier bf16 + --offload + disable_mmap loads were the RAM-heavy path (spiked ~90% system RAM); fp8 + no-offload is the lean fix (RAM ~30%).
- **For the pipeline:** To score a Chroma/Flux LoRA, use flux_minimal_inference.py fp8 + real CFG (cfg ~4 + negative) at strength ~2.5-3.0 — NOT the kohya training-sampler (noise) and NOT cfg_scale 1.0 (noise). For the strongest cyanotype, ComfyUI with ModelSamplingAuraFlow shift 1.0 at strength ~1.5 remains the reference (#168); the CLI path is the scriptable batch alternative.
- **Method:** lora · **Applies to:** diffusion · **Base:** Chroma · **Kind:** failure-fix
- **Runs:** 1
- **Validated under:** RTX 5090; Chroma1-HD fp8 DiT, t5xxl_fp8, ae; flux_minimal_inference.py --interactive; cfg 1.0 (noise) vs cfg 4 + neg (works); strength sweep 1/2/3 -> cyanotype onset ~3.0. 2026-06-07.
- **Measured receipt (tensor-engine):** `training-chroma-flux-lora-baseswap-cyanotype-recipe-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `chroma1-hd`
- **Output license:** commercial **yes** — inference/eval method; metric models measure only.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| inference_script | flux_minimal_inference.py --model_type chroma --flux_dtype fp8 | ● | NO --offload; ~25-28 GB VRAM, ~30% RAM |
| cfg | --guidance 0 --cfg_scale 4 --negative_prompt | ● | REAL CFG mandatory; cfg_scale 1.0 -> pure noise |
| strength | ~2.5-3.0 | ○ | higher than ComfyUI ~1.5 (no AuraFlow shift in this path) |
| kohya_training_sampler | BROKEN for Chroma (pure noise) | ○ | --sample_at_first emits RGB static; do not use |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Chroma LoRA samples are pure RGB noise | kohya training-sampler, or cfg_scale 1.0 (flux distilled-guidance path) — Chroma needs real CFG | flux_minimal_inference fp8 + --cfg_scale 4 + negative prompt | cfg_scale |
| system RAM spikes ~90% during Chroma inference | bf16 DiT (17 GB) + --offload (T5 resident in RAM) + disable_mmap full-file read | --flux_dtype fp8, drop --offload (~30% RAM, ~25-28 GB VRAM) | flux_dtype |

- **Best for:** scriptable Chroma/Flux LoRA eval-grid generation (eval, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-07 | the eval path itself, looked-at (noise vs faithful)
- **Sources:** [training-knowledge wave-6 A0 de-risk (Chroma inference path)](https://github.com/mcp-tool-shop-org/readouts) — rig-tested 2026-06-07: kohya sampler + cfg1.0 = noise; fp8+realCFG+strength3 = faithful cyanotype (looked-at) ; [kohya-ss flux_minimal_inference.py (--model_type chroma, --lora_weights, real CFG)](https://github.com/kohya-ss/sd-scripts) (kohya-ss, 2024) — supports chroma + lora_weights path;multiplier + cfg_scale + negative_prompt

### Chroma LoRA rank/dim sweep (8/16/32) — MEASURED on the 5090 (size linear; higher rank binds the saturated palette more completely — unlike SDXL) · `recommended` · ▣ measured
**MEASURED 3-way on the 5090 (Chroma1-HD, networks.lora_flux, fp8_base, #168 recipe, dim/alpha 8/16/32): training perf + VRAM are FLAT across rank (2.67-2.70 s/it, 18.8-19.6 GB — the 8.9B DiT forward dominates), so rank's only training cost is adapter SIZE, linear at 53.5 / 107.0 / 213.8 MB. On fidelity, unlike SDXL (where rank was ~neutral), higher rank binds the saturated cyanotype palette MORE completely: dim32 has the best CMMD (0.186 vs dim8 0.218) and a visibly more uniform Prussian-blue field with white-linework, where dim8 leaves the ship naturalistic/warm. CLIP-sim is monotonic (0.7034/0.7143/0.7224) but each step ~1 SEM, so CMMD + the looked-at grid carry the signal.**
Held the #168 recipe constant, varied only --network_dim/--network_alpha. 600 steps, seed 42, fp8_base. Eval = 10 held-out subjects x 2 seeds (n=20) per rank via the validated flux_minimal_inference fp8 + real-CFG path (strength 3.0), scored CLIP-sim to the 16-img cyanotype style centroid + CMMD, plus looked-at grids. Result (s/it / peak VRAM / MB / CLIP-sim / CMMD): dim8 2.67 / 18.8 / 53.5 / 0.7034 / 0.2175; dim16 2.69 / 19.1 / 107.0 / 0.7143 / 0.2197; dim32 2.70 / 19.6 / 213.8 / 0.7224 / 0.1857. All clear the >=0.70 in-style bar. The looked-at ships: dim8 = naturalistic warm hull (palette under-bound), dim32 = strong uniform blue field + white linework (palette fully transformed). For a strong-palette base-swap style the rank capacity is what carries the global palette transform; SDXL's subtler style did not need it (wave 4/5).
- **For the pipeline:** For Chroma saturated-palette styles, default dim16 (sweet spot) but step to dim32 when palette fidelity matters — the +CMMD/visible-blue gain is real, at 2x the adapter (107->214 MB). Use dim8 only when size-constrained (half the MB, ~1 SEM lower CLIP-sim, visibly weaker palette). Note this DIFFERS from the SDXL finding (rank ~fidelity-neutral there); the difference is the saturated-palette transform, which needs capacity.
- **Method:** lora · **Applies to:** diffusion · **Base:** Chroma · **Kind:** recipe
- **Seed:** 42 · **Runs:** 3 · **Tuning budget:** 3 matched runs (dim 8/16/32) · **Search:** same-recipe 3-way A/B, eval n=20 + looked-at
- **Variance:** n=20/config (SEM 0.012-0.016 CLIP-sim). Rank steps are ~1 SEM on CLIP-sim individually; CMMD (dim32 best by ~0.03) and the looked-at grid are the decisive signals.
- **Validated under:** RTX 5090 32GB; Chroma1-HD + fp8_base, t5xxl_fp8, ae; networks.lora_flux; #168 recipe; dim/alpha 8/16/32; AdamW lr 1e-4 constant; 600 steps; eval via flux_minimal_inference fp8 + cfg 4 + neg, strength 3.0, 26 steps. Health: peak 74C, no throttle. 2026-06-07.
- **Measured receipt (tensor-engine):** `training-chroma-flux-lora-baseswap-cyanotype-recipe-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `chroma1-hd`
- **Output license:** commercial **yes** — Chroma1-HD Apache-2.0 (LoRA inherits); output license = base + dataset.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| rank_dim8 | 2.67 s/it / 18.8 GB / 53.5 MB / CLIP 0.7034 / CMMD 0.2175 | ○ |  |
| rank_dim16 | 2.69 s/it / 19.1 GB / 107.0 MB / CLIP 0.7143 / CMMD 0.2197 | ○ | = shift 3.0 default; the sweet spot |
| rank_dim32 | 2.70 s/it / 19.6 GB / 213.8 MB / CLIP 0.7224 / CMMD 0.1857 | ○ | best CMMD + strongest visible cyanotype |
| network_module | networks.lora_flux | ● | Flux/Chroma DiT LoRA module — NOT networks.lora |
| fp8_base | required | ● | bf16+live-T5 spills 32 GB; see chroma-fp8-base |
| adapter_size_scaling | linear in rank | ○ | 53.5/107/214 MB for dim 8/16/32 |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| cyanotype palette stays naturalistic / under-bound | rank too low (dim8) for a strong global-palette transform | raise rank to 16-32; palette binding scales with capacity for Chroma | network_dim |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | CLIP-sim-to-style-centroid | 0.7224 | >=0.70 | ✓ | clip-vit-b32 |
| diffusion-style | CLIP-sim-to-style-centroid | 0.7034 | >=0.70 | ✓ | clip-vit-b32 |

- **Best for:** strongest cyanotype palette fidelity (Chroma) (chroma, fit 5) ; smallest Chroma style adapter at acceptable fidelity (chroma, fit 4)
- **Verify:** verdict=confirmed | currency=measured 2026-06-07 | rig measurement + n=20 eval + looked-at grids; oracle = rig + harness, not the study-swarm verifier
- **Sources:** [training-knowledge wave-6 Chroma rank sweep (dim 8/16/32, n=20 eval + looked-at)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured RTX 5090 2026-06-07; _chroma_dim{8,16,32}_result.txt + eval_grid_chroma + _eval_chroma.json ; [kohya-ss sd-scripts flux_train_network (LoRA rank/dim)](https://github.com/kohya-ss/sd-scripts/blob/main/docs/flux_train_network.md) (kohya-ss, 2024) — Flux/Chroma LoRA via networks.lora_flux; rank/alpha control adapter capacity ; [Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) (Jayasumana et al., 2024) — CLIP-MMD is a more reliable small-sample distribution metric than FID — the discriminating signal here

### Chroma discrete_flow_shift sweep (1/3/6) — MEASURED (footprint-neutral; shift 6 marginally best fidelity; weakest lever) · `recommended` · ▣ measured
**MEASURED at fixed dim16 on the 5090: --discrete_flow_shift (the flow-matching Euler schedule shift) is FOOTPRINT-neutral (2.76 s/it, ~19.5 GB, 107 MB at all values) and the WEAKEST fidelity lever of the wave. shift 6.0 gives the best fidelity (CLIP-sim 0.7313, CMMD 0.2148), shift 1.0 ~ shift 3.0 (0.7127 / 0.7143), but shift6-vs-shift3 is only ~0.9 SEM. The kohya training default 3.0 is fine; nudge to 6.0 for a marginal palette edge.**
Held the #168 recipe constant at dim16, varied only --discrete_flow_shift (1.0 / 3.0-default / 6.0). 3.0 is the dim16 rank-sweep datapoint. Eval n=20 (held-out subjects x 2 seeds), CLIP-sim to the cyanotype centroid + CMMD + looked-at. Result (CLIP-sim / CMMD): shift1 0.7127 / 0.2327; shift3 0.7143 / 0.2197; shift6 0.7313 / 0.2148. Looked-at: shift6 = clean deep-blue field, shift1 = more naturalistic/textured. The trend favors higher shift but stays within ~1 SEM, so shift is a fine-tuning lever, not a primary one.
- **For the pipeline:** Leave discrete_flow_shift at the 3.0 default for Chroma cyanotype; optionally raise to ~6.0 for a marginal fidelity/palette nudge (free — no perf/VRAM/size cost). Do not expect a large effect; rank (capacity) and strength (inference) move fidelity far more.
- **Method:** lora · **Applies to:** diffusion · **Base:** Chroma · **Kind:** recipe
- **Seed:** 42 · **Runs:** 2 · **Tuning budget:** 2 new matched runs + the dim16 midpoint · **Search:** same-recipe shift A/B at fixed rank, eval n=20 + looked-at
- **Variance:** 2 new runs (shift 1.0, 6.0) + the dim16 shift-3.0 datapoint; n=20/config; shift6-vs-shift3 ~0.9 SEM (marginal).
- **Validated under:** RTX 5090 32GB; Chroma1-HD fp8_base; networks.lora_flux dim16; AdamW lr 1e-4 constant; --discrete_flow_shift 1/3/6; 600 steps; eval flux_minimal_inference fp8 + cfg 4, strength 3.0. Health peak 74C. 2026-06-07.
- **Measured receipt (tensor-engine):** `training-chroma-flux-lora-baseswap-cyanotype-recipe-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `chroma1-hd`
- **Output license:** commercial **yes** — Chroma1-HD Apache-2.0; output license = base + dataset.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| shift1 | 2.76 s/it / 19.4 GB / CLIP 0.7127 / CMMD 0.2327 | ○ |  |
| shift3_default | CLIP 0.7143 / CMMD 0.2197 | ○ | = the dim16 rank run; kohya default |
| shift6 | 2.76 s/it / 19.6 GB / CLIP 0.7313 / CMMD 0.2148 | ○ | marginally best fidelity |
| discrete_flow_shift | 3.0 | ○ | kohya default; footprint-neutral across 1-6 |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | CLIP-sim-to-style-centroid | 0.7313 | >=0.70 | ✓ | clip-vit-b32 |

- **Best for:** marginal free fidelity nudge on Chroma cyanotype (chroma, fit 3)
- **Verify:** verdict=confirmed | currency=measured 2026-06-07 | rig measurement + n=20 eval + looked-at
- **Sources:** [training-knowledge wave-6 Chroma shift sweep (1/3/6, n=20 eval + looked-at)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured RTX 5090 2026-06-07; _chroma_shift{1,6}_result.txt + eval_grid_chroma + _eval_chroma.json ; [kohya-ss sd-scripts --discrete_flow_shift (FlowMatch Euler scheduler)](https://github.com/kohya-ss/sd-scripts/blob/main/docs/flux_train_network.md) (kohya-ss, 2024) — discrete_flow_shift sets the flow-matching Euler schedule shift; default 3.0

### Chroma1-HD base-swap style-LoRA (kohya flux_train_network --model_type chroma) — measured on the 5090 · `recommended` · ▣ measured
**Swapping the SDXL base for Apache-2.0 Chroma1-HD lands a saturated non-natural palette (deep Prussian-blue cyanotype) plus crisp token gating and high base quality together — the thing SDXL base 1.0 could never do — on one 32 GB card.**
kohya sd-scripts flux_train_network.py with --model_type chroma trains a DiT-only LoRA (network_module=networks.lora_flux) on Chroma1-HD, an 8.9B FLUX.1-schnell-derived Apache-2.0 base explicitly built as a neutral fine-tuning vehicle. Chroma is T5-only: pass --t5xxl + --ae, omit --clip_l (kohya substitutes a dummy_clip_l), and Chroma REQUIRES --guidance_scale 0.0 and --apply_t5_attn_mask. T5 is frozen (0 TE modules trained) — style gating comes from the regularization contrast on the DiT, not from text-encoder training. dim16/alpha16, AdamW, lr 1e-4, constant scheduler, 600 steps, sigmoid timestep sampling, raw model-prediction type, seed 42. Two load-bearing gotchas were earned hands-on (see failures). Inference in ComfyUI uses LoraLoaderModelOnly (DiT-only LoRA) at strength ~1.3-1.5 with ModelSamplingAuraFlow shift 1.0.
- **For the pipeline:** This is the studio's proof that the Flux/Chroma recipe space is real and distinct from SDXL — and the answer to 'can a commercial-safe flexible base render a strong stylized palette.' Use Chroma1-HD as the default Flux-family training base for stylized-palette LoRAs; the measured it/s and VRAM peak live in tensor-engine, not here.
- **Method:** lora · **Applies to:** diffusion · **Base:** Chroma · **Kind:** recipe
- **Seed:** 42 · **Runs:** 1 · **Tuning budget:** Manual: base-swap + the two crash/spill gotchas resolved in one session; dim/alpha/lr carried over from the apples-to-apples wave-7 SDXL run for a controlled comparison. · **Search:** manual
- **Variance:** Single proven config on 2026-06-03; not a multi-seed sweep. Palette strength is a deterministic function of inference LoRA strength (swept 1.0-2.0 at fixed train seed), not a re-train variance result.
- **Validated under:** Chroma1-HD (bf16 17.8GB) + --fp8_base, t5xxl_fp8_e4m3fn, ae.safetensors; 1024px; cyanotype dataset + reg set; trigger 'stdstyl'; kohya sd-scripts on native-Windows RTX 5090, ComfyUI 0.23.0 for validation. fp8_base is REQUIRED — bf16 + live T5 pins 32 GB and balloons step time.
- **Measured receipt (tensor-engine):** `training-chroma-flux-lora-baseswap-cyanotype-recipe-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `chroma1-hd`
- **Output license:** commercial **yes** — Chroma1-HD is Apache 2.0; the LoRA inherits it. Output is commercial-clean provided the training dataset is also clean. This is the commercial-safe answer to FLUX.1-dev's training restriction.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | networks.lora_flux | ● | NOT networks.lora — Flux/Chroma DiT uses the flux LoRA module; trains the 228 FLUX blocks (DiT) only. |
| rank | 16 dim | ● | --network_dim 16; Flux/Chroma tolerate higher rank than SDXL but 16 was sufficient for this style. |
| alpha | 16 | ● | --network_alpha 16; alpha==dim (scale 1.0). |
| learning_rate | 1e-4 | ● | DiT learning rate; no separate te_lr — T5 is frozen. |
| optimizer | AdamW | ○ | --optimizer_type AdamW. |
| scheduler | constant | ○ | --lr_scheduler constant. |
| steps | 600 steps | ● | --max_train_steps 600; ~27 min at fp8_base on the 5090 (timing lives in tensor-engine). |
| precision | bf16 + fp8_base | ● | --mixed_precision bf16 --save_precision bf16 --fp8_base. fp8_base REQUIRED: bf16+live-T5 spills the 32 GB card. |
| resolution | 1024 px | ○ | 1024px training. |

- **Datasets:** Cyanotype regularization set (white background) — token-gating contrast (regularization, license Studio-owned (synthetic). Verify generation provenance for commercial cleanliness.) ; Cyanotype 'stdstyl' style set (Flux/Chroma) (training, license Studio-owned (synthetic, generated in-house). Commercial-clean when the generating base is Apache-2.0/clean — verify generation provenance before shipping.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Crash at step 0: TypeError 'NoneType' object is not iterable in process_batch (train_network.py:432) | --cache_text_encoder_outputs is incompatible with --apply_t5_attn_mask — the cached path leaves batch['input_ids_list']=None, and Chroma REQUIRES the attn mask. | Drop --cache_text_encoder_outputs (T5 runs live each step); keep --cache_latents. | cache_text_encoder_outputs |
| VRAM pinned at ~32 GB and step time balloons 5 -> 34 s/it (WDDM paging GPU memory to system RAM) | bf16 Chroma + live (un-cached) T5 exceeds the 32 GB card. | Add --fp8_base (Chroma quantized to ~fp8): VRAM drops to ~20 GB and step time recovers to ~2.65-2.71 s/it. | precision |
| Isolated subjects (portrait) render white-line-on-white-background even at strength 2.0, while scenes get the full blue field | The regularization images were generated on 'plain white background', so the reg contrast taught WHITE as the neutral bg, which bleeds into the trigger case for subjects lacking a natural sky/sea region. | Regenerate the reg set with varied/colored backgrounds (not white) so 'blue field' isn't contrasted away — universal palette binding. | reg_image_count |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | human-A/B gating + palette check (base / LoRA+no-trigger / LoRA+trigger at one seed) | Gating crisp and cleaner than SDXL: no-trigger = photorealistic/normal color (matches reg set); trigger = trained cyanotype style. Strong Prussian-blue achieved at strength 1.5-2.0. | trigger must produce strong saturated cyanotype AND no-trigger must stay neutral (both, not two-of-three) | ✓ | human |

- **Best for:** Commercial-safe stylized-palette style-LoRA (flux, fit 5) ; Single-GPU Flux LoRA training under 32 GB (single-gpu, fit 5)
- **Verify:** verdict=confirmed | currency=Current as of 2026. Chroma1-HD confirmed Apache-2.0, FLUX.1-schnell-derived, 8.9B, designed as LoRA base. Kohya sd-scripts flags for Chroma (--timestep_sampling sigmoid, --model_prediction_type raw, --guidance_scale 0.0) confirmed in current docs. network_dim 16 and lr 1e-4 appear as example values in the docs (not formally designated as 'recommended defaults,' but consistent with community practice). | All three sources verify. The receipt source identifier points at an internal config_recipes slug with the correct kohya docs URL as the external anchor — valid structure. No VRAM scalars stored; measured numbers correctly deferred to engine_recipe_ref. Boundary is clean: recipe craft only, no model weight cataloguing, no rig-measured performance numbers in the technique body.
- **Sources:** [RECIPE (PROVEN): kohya Chroma LoRA — exact command + the 2 gotchas + strength/reg palette tuning (tensor-engine config_recipes #168)](https://github.com/kohya-ss/sd-scripts/blob/main/docs/flux_train_network.md) (studio (rig-measured), 2026) — The exact working kohya Chroma LoRA command, the two crash/spill gotchas, and the strength/reg palette tuning, measured hands-on on the RTX 5090. ; [lodestones/Chroma1-HD](https://huggingface.co/lodestones/Chroma1-HD) (lodestones, 2026) — Chroma1-HD is an 8.9B FLUX.1-schnell-derived, fully Apache-2.0 text-to-image base intentionally designed as a neutral starting point for finetuning and LoRA. ; [LoRA Training for FLUX.1 — sd-scripts (flux_train_network.md)](https://github.com/kohya-ss/sd-scripts/blob/main/docs/flux_train_network.md) (kohya-ss, 2025) — For Chroma models use --timestep_sampling sigmoid, --model_prediction_type raw, --guidance_scale 0.0; network_dim 16 and lr 1e-4 are baseline values.

### fp8_base is REQUIRED for Chroma LoRA on 32 GB — bf16 + live T5 spills the card (MEASURED 31974 MiB / 34 s/it) · `recommended` · ▣ measured
**MEASURED on this rig: bf16 Chroma1-HD + live T5 (Chroma requires --apply_t5_attn_mask which is incompatible with --cache_text_encoder_outputs, so T5 runs live) SPILLS the 32 GB card — VRAM pinned 31974/32607 MiB and step time ballooned 5 -> 34 s/it via WDDM paging. --fp8_base is REQUIRED: ~20 GB, 2.65-2.71 s/it, ~27 min/600 steps. Corroborated this wave: all 5 fp8_base rank/shift runs sat 18.8-19.6 GB at 2.67-2.76 s/it with zero spill.**
The bf16-spill A/B was measured hands-on in the #167 baseline session (2026-06-03; engine-room receipt training-chroma-flux-lora-baseswap-cyanotype-baseline-5090). No fresh spill re-run was needed (Mike's call 2026-06-07) — the #167 data is a complete A/B and this wave's 5 fp8_base runs independently confirm the fp8 side on the same rig (18.8-19.6 GB, 2.67-2.76 s/it, peak 74C, no throttle). The two load-bearing Chroma gotchas: (1) --cache_text_encoder_outputs + --apply_t5_attn_mask crashes at step 0 (input_ids_list=None) so TE caching must be dropped (T5 live); (2) that live bf16 T5 is what spills, so fp8_base is mandatory on 32 GB.
- **For the pipeline:** Always pass --fp8_base for Chroma LoRA on a 32 GB card. Never try bf16 base here — it pages to system RAM and runs ~13x slower. Keep --cache_latents, drop --cache_text_encoder_outputs.
- **Method:** lora · **Applies to:** diffusion · **Base:** Chroma · **Kind:** failure-fix
- **Runs:** 6
- **Variance:** bf16-spill from #167 (1 run); fp8 confirmed across this wave's 5 runs.
- **Validated under:** RTX 5090 32GB; Chroma1-HD; bf16 vs --fp8_base; t5xxl_fp8 live (--apply_t5_attn_mask, no TE cache). bf16 from #167 2026-06-03; fp8 corroborated 2026-06-07.
- **Measured receipt (tensor-engine):** `training-chroma-flux-lora-baseswap-cyanotype-recipe-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `chroma1-hd`
- **Output license:** commercial **yes** — Chroma1-HD Apache-2.0.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| bf16_base_live_t5 | 31974/32607 MiB pinned -> 34 s/it (WDDM paging) | ○ | from #167 — unusable on 32 GB |
| fp8_base | ~20 GB / 2.65-2.71 s/it / ~27 min per 600 steps | ● | REQUIRED; corroborated 18.8-19.6 GB across 5 wave-6 runs |
| cache_text_encoder_outputs | MUST OMIT | ○ | incompatible with --apply_t5_attn_mask (crash at step 0); T5 runs live |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Chroma training pins VRAM ~32 GB and runs ~34 s/it | bf16 base + live bf16 T5 exceeds 32 GB -> WDDM pages to system RAM | --fp8_base (~20 GB, 2.65 s/it) | fp8_base |
| crash at step 0: 'NoneType' object is not iterable (input_ids_list=None) | --cache_text_encoder_outputs combined with --apply_t5_attn_mask (Chroma needs the mask) | drop --cache_text_encoder_outputs (run T5 live); keep --cache_latents | cache_text_encoder_outputs |

- **Best for:** fitting Chroma/Flux LoRA training on a 32 GB card (single-gpu, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-03 (#167) + corroborated 2026-06-07 | bf16-spill from #167; fp8 side confirmed across 5 wave-6 runs
- **Sources:** [tensor-engine #167 Chroma baseline (bf16-spill vs fp8 A/B, measured 2026-06-03)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured bf16 spill 31974 MiB/34 s/it; fp8 ~20 GB/2.65 s/it ; [training-knowledge wave-6 fp8 corroboration (5 runs)](https://github.com/mcp-tool-shop-org/readouts) — 5 fp8_base runs 18.8-19.6 GB / 2.67-2.76 s/it / no spill

### FLUX.2 [klein] 4B Apache-2.0 undistilled-base style-LoRA (Qwen3 encoder, real CFG, 32GB-comfortable) · `recommended` · ▸ reproduced
**FLUX.2 [klein] 4B BASE is the studio's second commercial-safe Flux training vehicle: Apache-2.0, explicitly UNDISTILLED (no guidance/step distillation, no guidance embeddings), with a bundled Qwen3-4B text encoder - so it trains with normal CFG semantics, frozen TE, rank 16, bf16 on one 32GB card with headroom to spare.**
FLUX.2 [klein] 4B base (Apache-2.0; the 9B base is FLUX Non-Commercial) was built undistilled precisely as a fine-tuning vehicle - BFL states it preserves the complete training signal and recommends the 50-step BASE (not the 4-step distilled) variant for LoRA. Two architecture facts drive the recipe: (1) the text encoder is a bundled Qwen3-4B LLM (the 9B pairs Qwen3-8B), with hidden states pulled from layers 9/18/27 concatenated to 7680-dim - this CORRECTS the wave-1 caption row which said FLUX.2 [klein] uses 'a single 24B Mistral encoder' (Mistral-Small-3.1/3.2 is the encoder for big FLUX.2 dev/pro, not klein; the klein 24B figure was wrong - see flag). (2) Because the base is undistilled there is NO guidance embedding, so kohya/SimpleTuner guidance-training options are IGNORED and you sample with real CFG (unlike dev's distilled g=1-train/g=3.5-sample, unlike Chroma's g=0). Recipe (SimpleTuner/ai-toolkit, reproduced from BFL + community docs, not yet measured on the 5090): network rank 16, lr 8e-5 for style (1e-4 for character), bf16 mixed precision, batch 1 + grad-accum, latent + text-embed caching, gradient checkpointing; ~12GB bf16 / ~8GB int8 footprint for the 4B - far under 32GB, so the 5090 can run higher resolution (1024+) and larger batch than dev/Chroma allow. Text encoder + VAE frozen; leave pretrained_text_encoder unset to use the bundled Qwen3. Style LoRAs 1500-2500 steps, start 512 then 1024+. This is the lighter-weight commercial-safe sibling to wave-1's 8.9B Chroma1-HD recipe - smaller, faster, undistilled, FLUX.2-architecture.
- **For the pipeline:** Add FLUX.2 [klein] 4B base as the studio's SECOND blessed commercial-safe Flux base alongside Chroma1-HD - choose klein-4B when you want FLUX.2 architecture + Qwen3 prompt understanding + max VRAM headroom, choose Chroma1-HD when you want the proven cyanotype-palette result and FLUX.1 ecosystem tooling. Update the wave-1 caption row's encoder claim: klein = Qwen3, not Mistral. Hard-gate the 9B base out of any commercial pack (non-commercial license).
- **Method:** lora · **Applies to:** diffusion · **Base:** flux · **Kind:** recipe
- **Validated under:** Settings reproduced from BFL klein training docs, SimpleTuner FLUX2 quickstart, and HF diffusers blog; VRAM figures are doc-reported (~12GB bf16 / ~8GB int8 for 4B), NOT measured on the 5090 this wave. Holds for the 4B BASE (Apache-2.0); does not transfer to the 4-step distilled klein.
- **Base model (model-knowledge):** `flux2-klein-base-4b`
- **Builds on (stage 2):** Chroma1-HD base-swap style-LoRA (kohya flux_train_network --model_type chroma) — measured on the 5090
- **Output license:** commercial **yes** — FLUX.2 [klein] 4B base + outputs are Apache-2.0 - commercial-safe for training and shipping. CRITICAL: the 9B base is FLUX Non-Commercial - do not train/ship on it commercially. BFL encourages safety filters on deployment.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | lora enum | ● | DiT-only LoRA on the FLUX.2 transformer; TE frozen. |
| rank | 16 dim | ● | Style default; bump to 32 for complex styles. |
| alpha | 16 scalar | ● | alpha=rank (scale 1.0); or rank/2 for gentler updates. |
| learning_rate | 8e-5 scalar | ● | Style; raise to 1e-4 for character. BFL klein doc range 8e-5-1e-4. |
| optimizer | adamw8bit enum | ○ | 8-bit AdamW keeps optimizer state small; plain AdamW fine given 32GB headroom on 4B. |
| precision | bf16 enum | ● | bf16 mixed; int8 base optional to free VRAM but unnecessary for 4B on 32GB. |
| resolution | 1024 px | ○ | Start 512 for fast iteration, finish 1024+; klein-4B's small footprint allows it on 32GB. |
| steps | 2000 steps | ○ | Style 1500-2500; monitor samples for overfit. |
| timestep_sampling | shift enum | ○ | Flow-matching shift schedule (see flux-shift-schedule-depth). |
| model_prediction_type | raw enum | ● | Flow-matching raw prediction. |

- **Datasets:** Cyanotype regularization set (white background) — token-gating contrast (regularization, license Studio-owned (synthetic). Verify generation provenance for commercial cleanliness.) ; Cyanotype 'stdstyl' style set (Flux/Chroma) (train, license Studio-owned (synthetic, generated in-house). Commercial-clean when the generating base is Apache-2.0/clean — verify generation provenance before shipping.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Trainer errors or silently ignores guidance settings on klein. | klein base is undistilled and has no guidance embeddings; guidance-training options are no-ops. | Drop guidance options for klein; sample with normal CFG at inference. | guidance_scale |
| Captions written as comma-separated booru tags produce weak style binding. | Qwen3-4B is an LLM encoder expecting fluent NL; tag-soup wastes its capacity (same failure class as wave-1's frozen-T5 captions). | Use NL captions (JoyCaption/Florence-2/CogVLM2) - see flux-nl-caption-depth-vlm. | caption_strategy |
| Pack ships commercially but uses klein-9B. | 9B base is FLUX Non-Commercial. | Use ONLY the 4B Apache-2.0 base for commercial work. | base_model_slug |

- **Best for:** Commercial-safe FLUX.2-architecture style LoRA (style-lora, fit 5) ; Max VRAM headroom on 32GB (high-res / larger batch) (vram-headroom, fit 5)
- **Verify:** verdict=confirmed | currency=FLUX.2 klein released January 2026 per BFL and search results. Fully current. | All four sources verified: HF model card confirms Apache-2.0, undistilled, fine-tune suitable. docs.bfl.ml/flux_2/flux2_klein_training exists and confirms lr 8e-5-1e-4, style 1500-2500 steps, 512→1024 resolution ladder. SimpleTuner FLUX2.md confirmed (Qwen3 bundled encoder, no guidance embeddings, rank 16, lr 1e-4, bf16). Geronimo medium post confirmed (Qwen3-4B, layers 9/18/27 concatenated to 7680-dim, 512 max tokens). The claim that '4B uses Qwen3-4B, 9B uses Qwen3-8B' is confirmed by web search cross-check. evidence_strength 'reproduced-from-source' is fully justified. DEDUP: wave-1 covers Chroma base-swap; this entry introduces klein as a second distinct commercial vehicle (Apache-2.0, undistilled, different encoder). Genuinely new.
- **Sources:** [FLUX.2-klein-base-4B model card](https://huggingface.co/black-forest-labs/FLUX.2-klein-base-4B) (Black Forest Labs, 2026) — Apache-2.0; undistilled (trained without step or guidance distillation); ideal for fine-tuning and LoRA; outputs commercial-usable. ; [FLUX.2 [klein] Training](https://docs.bfl.ml/flux_2/flux2_klein_training) (Black Forest Labs, 2026) — Use Base (50-step) for fine-tuning/LoRA; lr 8e-5-1e-4 (lower for style); style 1500-2500 steps; start 512 then 1024+. ; [SimpleTuner FLUX.2 quickstart - klein config](https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/FLUX2.md) (bghira, 2026) — klein uses bundled Qwen3 text encoder, no guidance embeddings (guidance options ignored); klein-4B ~12GB bf16 / ~8GB int8; rank 16, lr 1e-4, bf16. ; [FLUX.2 Klein - How Inference Works (Qwen3 encoder layers 9/18/27 -> 7680-dim)](https://medium.com/@geronimo7/flux-2-klein-how-inference-works-05553fcdbe7e) (Geronimo, 2026) — 4B uses Qwen3-4B, 9B uses Qwen3-8B; hidden states from layers 9/18/27 concatenated to 7680-dim - confirms encoder is Qwen3 not Mistral.

### Flow-matching shift schedule depth - discrete_flow_shift, resolution-aware shift, and sigmoid vs shift vs flux_shift · `superseded` · ▸ reproduced
**Beyond 'use sigmoid' (wave-1), the flow-matching shift parameter biases WHICH timesteps the LoRA sees - higher shift concentrates training on high-noise/structural steps (good for composition-level style), and the correct shift is resolution-dependent because Flux's noise schedule is resolution-shifted at sampling.**
Wave-1 established sigmoid/shift/flux_shift exist and that flux_shift is the FLUX.1-dev default. This row goes a layer deeper on the lever itself. The shift s reparameterizes the sigma->timestep mapping t' = s*t / (1 + (s-1)*t): s>1 pushes the sampled timesteps toward the high-noise (early/structural) end, s<1 toward the low-noise (late/detail) end. kohya exposes --discrete_flow_shift (default 3.1582 for FLUX.1) which is ONLY honored when --timestep_sampling=shift; with sigmoid/flux_shift the shift is computed differently. Practical depth: (1) flux_shift = dynamic, resolution-aware shift matching FLUX.1-dev's own sampling schedule (BFL shifts the schedule by sequence length / resolution) - use it when training resolution will match inference resolution, so train and sample see the same timestep density. (2) Plain sigmoid (wave-1's Chroma pick) is resolution-agnostic and biases toward middle timesteps - robust default when you train and sample at different resolutions. (3) shift + explicit discrete_flow_shift gives manual control: raise it (e.g. 3.5-6) to spend more steps on coarse structure for a style that lives in composition/palette (the cyanotype case), lower it (~1.0-2.0, as wave-1's ModelSamplingAuraFlow shift 1.0 at inference) for fine-texture styles. The inference-side shift (ComfyUI ModelSamplingAuraFlow / ModelSamplingFlux) should ROUGHLY mirror the training-side intent; a large train/inference shift mismatch is a quiet quality leak. None of this maps to an SDXL knob - there is no SDXL equivalent of timestep-density shaping in DDPM training (min_snr_gamma is the closest cousin and it is meaningless here).
- **For the pipeline:** Promote shift from a single template constant to a per-style choice with a documented rationale: resolution-matched -> flux_shift; cross-resolution -> sigmoid; structure-dominant style -> shift + higher discrete_flow_shift. Always pin BOTH the training shift and the inference (ModelSamplingFlux/AuraFlow) shift together in the recipe so they cannot drift apart.
- **Method:** lora · **Applies to:** diffusion · **Base:** flux · **Kind:** protocol
- **Validated under:** Behavior of --discrete_flow_shift / --timestep_sampling reproduced from kohya sd-scripts flux docs and the Flow Matching / FLUX schedule literature; the structure-vs-detail shift heuristic is a community-reasoned guideline, not a 5090-measured ablation this wave.
- **Builds on (stage 3):** Flow-matching training schedule (sigmoid/shift timestep + raw prediction) — why Flux is a separate recipe space from SDXL/DDPM
- **Output license:** commercial **yes** — Schedule theory is base-agnostic and license-free; applies to Apache-2.0 bases (Chroma1-HD, klein-4B).
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| timestep_sampling | shift / sigmoid / flux_shift enum | ● | shift = manual discrete_flow_shift; sigmoid = resolution-agnostic mid-bias; flux_shift = dynamic resolution-aware (dev default). |
| discrete_flow_shift | 3.1582 scalar | ○ | FLUX.1 default; ONLY honored with timestep_sampling=shift. Raise for structure-dominant styles, lower for fine-texture. |
| model_prediction_type | raw enum | ● | Flow-matching raw prediction (pairs with all shift modes). |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| discrete_flow_shift set but appears to have no effect. | It is only read when timestep_sampling=shift; with sigmoid/flux_shift it is ignored. | Switch to timestep_sampling=shift to use a manual discrete_flow_shift. | timestep_sampling |
| Style is strong at training resolution but weak/soft at a different inference resolution. | flux_shift trained at one resolution but sampled at another -> timestep density mismatch. | Either train with sigmoid (resolution-agnostic) or match train/inference resolution + shift. | timestep_sampling |

- **Best for:** Tuning where in the noise schedule a style binds (flux-schedule, fit 5)
- **Verify:** verdict=confirmed | currency=Current for 2026. discrete_flow_shift and resolution-aware shift are still the relevant levers in kohya and SimpleTuner. | arXiv:2210.02747 confirmed real (correct title, authors, year). SimpleTuner FLUX.md confirmed exists and supports resolution-shifted schedule claim (PARTIAL support as marked). kohya-ss sd-scripts source is a repo root link rather than a specific doc URL — PARTIAL as marked is appropriate and honest. The resolution-dependent shift insight is not contradicted by any source. evidence_strength 'reproduced-from-source' is reasonable given the primary paper is verified. DEDUP: wave-1 flux-flow-matching-timestep-prediction-theory covers sigmoid/shift at a conceptual level; this entry adds discrete_flow_shift parameter mechanics, resolution-dependence, and the composition-vs-detail tradeoff of shift value. Genuine depth extension, not restatement.
- **Sources:** [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) (Lipman, Chen, Ben-Hamu, Nickel, Le, 2023) — Defines the conditional probability path / vector-field regression that the shift parameter reparameterizes; basis for rectified-flow timestep schedules. ; [kohya sd-scripts FLUX.1 LoRA training - timestep_sampling and discrete_flow_shift](https://github.com/kohya-ss/sd-scripts) (kohya-ss, 2025) — discrete_flow_shift (default 3.1582) is only honored with timestep_sampling=shift; flux_shift is the dev default; sigmoid/shift/flux_shift select the noise-level sampling distribution. ; [SimpleTuner FLUX.1 quickstart - schedule/shift settings](https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/FLUX.md) (bghira, 2026) — Flux schedule is resolution-shifted; training shift should track intended inference resolution/shift.

### Flow-matching training schedule (sigmoid/shift timestep + raw prediction) — why Flux is a separate recipe space from SDXL/DDPM · `recommended` · ▸ reproduced
**Flux/Chroma are rectified-flow (flow-matching) transformers, not DDPM ε-prediction UNets, so SDXL knobs do not transfer: min_snr_gamma is meaningless, and the correct levers are timestep_sampling (sigmoid/shift/flux_shift), model_prediction_type=raw, discrete_flow_shift, and guidance_scale set to disable distillation guidance during training.**
Flow Matching (Lipman et al., ICLR 2023) trains a model to regress the vector field of a conditional probability path between noise and data, subsuming diffusion paths as a special case and using straighter Optimal-Transport trajectories. FLUX is built on this rectified-flow formulation. Practically, in kohya: --timestep_sampling chooses how noise levels are sampled (sigma|uniform|sigmoid|shift|flux_shift); flux_shift is the FLUX.1-dev default, sigmoid is recommended for Chroma; --model_prediction_type=raw uses the prediction as-is (vs sigma_scaled for DDPM); --discrete_flow_shift (default 3.1582 for FLUX.1) shifts the schedule and is only honored when timestep_sampling=shift; --guidance_scale must be set to 1.0 for FLUX.1-dev (to disable its distilled guidance) or 0.0 for Chroma. There is no min-SNR-gamma, no v-prediction-vs-epsilon choice, and the SDXL noise-offset family does not apply.
- **For the pipeline:** Maintain a SEPARATE recipe template for Flux-family LoRAs — never fork the SDXL recipe. The portable lane invariants are: timestep_sampling+model_prediction_type+guidance_scale per base (sigmoid/raw/0.0 for Chroma; flux_shift or shift+3.1582/raw/1.0 for FLUX.1-dev-style), and explicitly DROP every DDPM-only knob.
- **Method:** lora · **Applies to:** diffusion · **Base:** Flux · **Kind:** method-theory
- **Tuning budget:** Library defaults; the Chroma settings were confirmed in one measured run. · **Search:** none
- **Variance:** Theory + vendor/library defaults; the Chroma half of these settings is corroborated by the measured-on-rig recipe in this lane (sigmoid/raw/0.0 worked).
- **Validated under:** kohya sd-scripts FLUX.1/Chroma trainer; settings as documented and (for Chroma) confirmed on the 5090.
- **Measured receipt (tensor-engine):** `training-chroma-flux-lora-baseswap-cyanotype-recipe-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **yes** — Method-level; commercial cleanliness is inherited from the chosen base + dataset, not from the schedule.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| timestep_sampling | sigmoid (Chroma) / flux_shift (FLUX.1-dev) | ● | kohya choices: sigma/uniform/sigmoid/shift/flux_shift. Recommended per-base. |
| loss_type | raw (model_prediction_type) | ● | --model_prediction_type raw is recommended; sigma_scaled is the DDPM-style default and is wrong for these bases. |
| scheduler | discrete_flow_shift 3.1582 | ○ | --discrete_flow_shift default 3.1582 for FLUX.1; only used when timestep_sampling=shift. Not applicable to Chroma (sigmoid, scale 1.0). |
| min_snr_gamma | N/A | ○ | Does NOT exist for flow-matching — an SDXL/DDPM knob. Do not set it. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Flux LoRA trains but never converges / output is noise or washed out | Reused an SDXL recipe: wrong model_prediction_type (sigma_scaled) and/or guidance_scale left at the distilled value and/or min_snr_gamma set. | Use model_prediction_type=raw; set guidance_scale to 1.0 (FLUX.1-dev) or 0.0 (Chroma) to disable distillation guidance during training; remove min_snr_gamma and noise-offset. | model_prediction_type |

- **Best for:** Understanding why SDXL recipes do not transfer to Flux (flux, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Flow matching theory (Lipman et al. 2023) is foundational and current. The claim that SDXL DDPM knobs (min_snr_gamma) do not transfer to rectified-flow models is accurate. Kohya flags confirmed. | Minor precision issue: the technique states the recommended FLUX.1 config is 'shift + discrete_flow_shift 3.1582' but kohya docs separately call flux_shift the 'recommended' method for FLUX.1, while the example command shown in the docs uses shift+3.1582. Both options appear in the docs and both work; the claim is not wrong but slightly imprecise about which is the primary recommendation. arXiv:2210.02747 is real, author list matches exactly (Lipman, Chen, Ben-Hamu, Nickel, Le), and the content (simulation-free flow matching, Optimal Transport paths) supports the claim. Boundary is clean: pure architectural theory and recipe-space explanation with no model cataloguing or rig numbers.
- **Sources:** [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747) (Lipman, Chen, Ben-Hamu, Nickel, Le, 2023) — Flow Matching regresses vector fields of conditional probability paths (subsuming diffusion paths), enabling simulation-free training and straighter Optimal-Transport trajectories — the rectified-flow formulation FLUX is built on. ; [LoRA Training for FLUX.1 — sd-scripts (flux_train_network.md)](https://github.com/kohya-ss/sd-scripts/blob/main/docs/flux_train_network.md) (kohya-ss, 2025) — timestep_sampling can be sigma/uniform/sigmoid/shift/flux_shift; recommended FLUX.1 config is shift + discrete_flow_shift 3.1582 + model_prediction_type raw + guidance_scale 1.0; Chroma uses sigmoid + raw + guidance_scale 0.0.

### Flux LoRA serving - keep it as a runtime adapter, merge only to bake fp8, and there is no generic LoRA->base converter · `recommended` · ▸ reproduced
**Flux/Chroma style LoRAs should be SERVED as runtime adapters (ComfyUI LoraLoaderModelOnly), not statically merged - Flux's custom DiT architecture has no generic 'convert LoRA into original checkpoint' tooling, and merging is only worth it to bake a single shipped style into an fp8 checkpoint for inference speed/VRAM at the cost of flexibility.**
Wave-1 ended at inference (ComfyUI LoraLoaderModelOnly, DiT-only LoRA at strength 1.3-1.5, ModelSamplingAuraFlow shift 1.0) but did not cover the serving/merge decision. This row owns it. Three facts: (1) Unlike SD1.5/SDXL, Flux has a custom architecture with NO official convert_to_original_* path - you serve via runtime bridges (ComfyUI's loader nodes, diffusers load_lora_weights) and architecture-specific wrappers, not file-format conversion. (2) Keeping the LoRA as a runtime adapter is the studio default: one base in VRAM, many style LoRAs hot-swapped, strength dialable per render - exactly what a multi-style game-art pipeline wants. The DiT-only LoRA is loaded model-only (no TE/CLIP side), matching the frozen-encoder training. (3) Merging (fuse_lora / baking) is worth it only in narrow cases: shipping ONE locked style as a standalone checkpoint, or producing an fp8 merged checkpoint so the served model is smaller/faster - recent ComfyUI commits changed model-detection logic so fp8 Flux merges load correctly, and diffusers can load an fp8 transformer from safetensors and pass it to FluxPipeline. The tradeoffs of merging: you lose strength control and hot-swap, you must re-merge per base, a merged fp8 checkpoint inherits the fp8 quality floor (see precision row), and the merged file is base-sized (GBs) vs a rank-16 adapter (tens of MB). Format hygiene: train and ship the LoRA in the kohya/ComfyUI safetensors key convention (not raw diffusers PEFT keys) so the loader recognizes it without a wrapper; mismatched key namespaces are the usual 'LoRA does nothing / errors on load' cause. Cross-base portability is NOT free: a Chroma-trained LoRA is keyed to Chroma's DiT and will not cleanly apply to FLUX.1-dev or klein - serve each LoRA on the base it was trained against.
- **For the pipeline:** Default serving = runtime adapter (ComfyUI LoraLoaderModelOnly), one base + many hot-swappable style LoRAs, strength as a render-time dial. Merge-to-checkpoint ONLY to ship a single locked style or to bake an fp8 served checkpoint for speed - document the lost flexibility. Standardize on the kohya/ComfyUI safetensors key convention at export so loaders need no wrapper, and pin each LoRA to its training base (no cross-base serving).
- **Method:** lora · **Applies to:** diffusion · **Base:** flux · **Kind:** protocol
- **Validated under:** Serving/merge behavior reproduced from ComfyUI + diffusers docs and community merge threads; the 'no generic Flux LoRA->base converter' and 'fp8 merge loads on recent ComfyUI' claims are community/doc-reported, not 5090-measured this wave.
- **Builds on (stage 4):** Chroma1-HD base-swap style-LoRA (kohya flux_train_network --model_type chroma) — measured on the 5090
- **Output license:** commercial **yes** — Serving mechanics are license-neutral, but a MERGED checkpoint inherits the BASE license - merging a LoRA into FLUX.1-dev/FLUX.2-dev yields a non-commercial checkpoint; merge only into Apache-2.0 bases (Chroma1-HD, klein-4B) for commercial distribution.
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | lora enum | ● | Served DiT-only via LoraLoaderModelOnly; no TE side loaded. |
| precision | bf16 enum | ○ | Serve adapter in bf16; only bake fp8 when speed/VRAM at inference demands it (inherits fp8 quality floor). |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| LoRA loads but visibly does nothing, or errors on load in ComfyUI. | Key namespace mismatch (raw diffusers PEFT keys vs kohya/ComfyUI safetensors convention) or wrong loader node. | Export in the kohya/ComfyUI safetensors key convention; use LoraLoaderModelOnly for DiT-only Flux LoRAs. | network_type |
| Chroma-trained LoRA applied to FLUX.1-dev/klein produces garbage. | LoRA keys are bound to the training base's DiT; cross-base application is invalid. | Serve each LoRA on the exact base it trained against. | base_model_slug |
| Merged checkpoint is non-commercial despite an Apache LoRA. | Merged file inherits the BASE license; base was dev (non-commercial). | Merge only into Apache-2.0 bases (Chroma1-HD, klein-4B) for commercial distribution. | base_model_slug |

- **Best for:** Serving many style packs off one base (serving, fit 5) ; Shipping one locked style as a checkpoint (merge, fit 3)
- **Verify:** verdict=confirmed-with-fixes | currency=Current for 2026. Runtime adapter approach confirmed as recommended; fp8 + LoRA merge friction confirmed in 2026 community reports. | nextdiffusion.ai tutorial confirmed real (ComfyUI LoraLoaderModelOnly, models/loras path). HF diffusers 'other-formats' page returns PARTIAL support — it says custom-arch models need architecture-specific tooling but does not explicitly state 'no generic LoRA->base converter exists.' The 'no generic converter' sub-claim is a community consensus that lacks a strong direct citation; it should be downgraded to community-claim on that specific point or softened to 'no well-documented generic converter in mainstream tooling as of 2026.' HaileyStorm HF discussion is PARTIAL as marked. The fp8-merge-causes-mixed-precision-errors finding is confirmed by 2026 community reports. DEDUP: no wave-1 coverage of LoRA serving. New knowledge. Fix: soften 'no generic LoRA->base converter' to community-claim level, not reproduced-from-source.
- **Sources:** [How to Use Flux LoRAs in ComfyUI (LoraLoaderModelOnly, models/loras)](https://www.nextdiffusion.ai/tutorials/how-to-use-flux-lora-in-comfyui) (Next Diffusion, 2025) — Flux LoRA safetensors go in models/loras and are served via ComfyUI loader nodes at runtime; DiT-only LoRAs use model-only loading. ; [Diffusers Model formats - Flux custom architecture has no generic original-format converter](https://huggingface.co/docs/diffusers/en/using-diffusers/other-formats) (Hugging Face, 2026) — Newer custom-architecture models (Flux) require architecture-specific tooling/wrappers rather than generic convert-to-original scripts; bridge at runtime. ; [FLUX.1 merges - fp8 merge loading on recent ComfyUI](https://huggingface.co/HaileyStorm/FLUX.1-Merges/discussions/3) (HaileyStorm / community, 2025) — fp8 Flux merges load after ComfyUI changed model-detection logic; diffusers can load an fp8 transformer from safetensors into FluxPipeline.

### Rank/dim/alpha choice for Flux DiT style-LoRA vs SDXL UNet - lower ranks go further on Flux · `superseded` · ▸ reproduced
**A Flux/Chroma DiT style-LoRA reaches strong style binding at lower rank than the equivalent SDXL UNet LoRA - rank 16 (often 8-16) is a strong style default on Flux, where SDXL style often wants 32+, because the larger transformer base needs less per-layer adaptation capacity and over-ranking Flux overfits and inflates file size fast.**
Wave-1's Chroma recipe pinned dim16/alpha16 as a measured choice but did not generalize the rank theory across the Flux<->SDXL gap. This row does. On SDXL (2.6B UNet), style LoRAs commonly need rank 32-64 because the convolutional UNet has less raw capacity to lean on. On Flux (12B) / Chroma (8.9B) / klein (4B) the DiT base is far larger and the LoRA only has to nudge a high-capacity manifold, so style binds at lower rank: HF's QLoRA FLUX.1-dev reference trained usable LoRAs at rank as low as 4; community consensus puts simple styles at 8-16 and complex/multi-element styles at 32-64, with 'anything above 32 is style-reserved' and 'very high ranks (256+) rarely help and increase overfitting.' Alpha policy is the same family as SDXL: alpha=rank (scale 1.0) is the safe default; alpha=rank/2 gives gentler updates (useful when a style binds too hard); alpha=1.5-2x rank pushes stronger updates at fixed lr. Two Flux-specific consequences: (1) rank drives file size and inference VRAM more than on SDXL because Flux LoRA touches more/larger DiT matrices - rank 32 Flux LoRAs are noticeably heavier to serve, which matters for a serving pipeline shipping many style packs. (2) DiT-only (no TE) means ALL the rank budget goes to the transformer, so an over-ranked Flux style LoRA overfits the training set's CONTENT (not just style) faster than the SDXL split-budget case. Studio rule: start Flux style at rank 16/alpha 16 (matching the proven Chroma recipe), only escalate to 32 if a held-out style eval shows under-binding, and treat 64 as the ceiling for a single style.
- **For the pipeline:** Set the studio Flux style default at rank 16 / alpha 16 and make rank an explicitly-justified escalation (16 -> 32 -> 64) gated on a held-out style eval, NOT a free dial copied from the SDXL recipe. Keep SDXL style at its own higher default. Track LoRA file size as a serving cost when ranks rise.
- **Method:** lora · **Applies to:** diffusion · **Base:** flux · **Kind:** protocol
- **Validated under:** Rank-vs-base-size relationship reproduced from HF QLoRA FLUX.1-dev report (rank 4 usable) + community rank guides; the specific 16/alpha16 Flux default is corroborated by wave-1's on-rig Chroma recipe. Cross-rank quality ablation not re-measured this wave.
- **Builds on (stage 3):** Chroma1-HD base-swap style-LoRA (kohya flux_train_network --model_type chroma) — measured on the 5090
- **Output license:** commercial **yes** — Rank/alpha selection is base-agnostic; the recommendations target Apache-2.0 bases (Chroma1-HD, klein-4B).
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| rank | 16 dim | ● | Flux style default; 8 for simple, 32 for complex, 64 ceiling. Lower than SDXL's typical 32+. |
| alpha | 16 scalar | ● | alpha=rank (scale 1.0) default; rank/2 gentler; 1.5-2x rank stronger. |
| network_type | lora enum | ● | DiT-only on Flux - entire rank budget is the transformer (no TE split). |

- **Datasets:** Held-out style eval set (frozen prompt list + pinned style-exemplar plate) (eval, license studio-internal canon art (commercial-clean by construction); the exemplar plate's license follows the canon-bound source it is drawn from)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Flux LoRA memorizes training-set content (subjects/backgrounds leak), not just style. | Rank too high for a DiT-only LoRA; over-capacity overfits content. | Drop rank (32->16->8); strengthen the regularization/no-trigger contrast set. | rank |
| SDXL-tuned rank (e.g. 64) copied to Flux gives bloated files and overfit. | Flux's larger base needs less per-layer capacity than SDXL. | Use a separate Flux rank default (16) rather than reusing the SDXL number. | rank |
| Style under-binds at rank 8-16 for a visually complex style. | Rank too low for the style's complexity. | Escalate to 32 (then 64 ceiling), gated on a held-out style eval. | rank |

- **Best for:** Picking Flux style rank without copying SDXL (rank-policy, fit 5)
- **Verify:** verdict=confirmed | currency=Current for 2026. | HF flux-qlora blog confirmed real (rank 4 usable, ~9GB peak, Sayak Paul et al., June 2025). Diffusion Doodles substack by Chris Green is a confirmed real publication (cross-referenced via search results). Modal blog is PARTIAL as marked. The core claim — Flux DiT needs lower rank than SDXL UNet for equivalent style binding — is well-supported by the rank-4 result in the HF blog. evidence_strength 'reproduced-from-source' is justified. DEDUP: no wave-1 technique addresses rank selection. New knowledge.
- **Sources:** [(LoRA) Fine-Tuning FLUX.1-dev on Consumer Hardware (QLoRA, rank 4)](https://huggingface.co/blog/flux-qlora) (Hugging Face / Sayak Paul et al., 2025) — Usable FLUX.1-dev LoRA trained at rank 4, lr 1e-4, 8-bit AdamW, bf16; text encoders + VAE frozen; ~9GB peak vs 26GB plain bf16 LoRA. ; [How to Train a LoRA (Ostris AI Toolkit) - rank guidance](https://diffusiondoodles.substack.com/p/how-to-train-a-lora-ostris-ai-toolkit) (Chris Green, 2025) — Simple styles rank 4-16, complex styles 32-64; >32 is style-reserved; alpha = rank or rank/2; very high ranks rarely help and overfit. ; [Fine-tuning a FLUX.1-dev style LoRA](https://modal.com/blog/fine-tuning-flux-style-lora) (Modal, 2025) — Practical Flux style LoRA rank/alpha and step ranges corroborating low-rank style binding.

### fp8 vs bf16 base precision for Flux LoRA training in 32GB - bf16 is the quality floor, fp8/int8 buys headroom not speed-for-free · `superseded` · ▸ reproduced
**On a 32GB Blackwell card the right default is bf16 base precision for the LoRA's own weights/grads and an fp8/NF4-quantized FROZEN base only when VRAM forces it - quantizing the frozen base trades a small, mostly-recoverable quality hit for headroom, while bf16 keeps the trainable path at full quality; fp8 is not a free quality win even though Blackwell has fp8 tensor cores.**
The 5090 (compute capability 12.0, Blackwell) clears the CC 8.9+ bar fp8 training needs, so the question is not 'can it' but 'should it.' Three regimes: (1) Full bf16 LoRA - base + trainable path in bf16. Highest quality, but a 12B FLUX.1-dev base in bf16 plus optimizer state can approach/exceed 24GB (HF measured 26GB plain bf16 LoRA on a 4090); on 32GB it fits with care but eats the resolution/batch budget. (2) Quantized frozen base (--fp8_base, NF4/QLoRA, or int8) + bf16 trainable LoRA + bf16 mixed precision compute. This is the consumer-standard: the frozen base is stored in fp8/NF4 (it is never updated, so its precision loss is bounded), while the LoRA weights, gradients, and optimizer math stay bf16. HF's QLoRA path hit ~9GB peak vs 26GB this way with 'nearly identical' results to bf16 LoRA. (3) Aggressive fp8 everywhere (incl. compute) - maximum speed/VRAM, but community quality rankings for diffusion put fp16 > bf16 > fp8_scaled > fp8_e4m3fn, so this is the quality floor, used only under hard VRAM pressure. Studio reasoning for the 5090's 32GB: the smaller commercial-safe bases (Chroma1-HD 8.9B, klein-4B 4B) fit comfortably in bf16 with headroom - so PREFER bf16 there and spend the freed VRAM on resolution/batch, NOT on fp8. Reserve fp8/NF4 base quantization for the 12B+ dev-class bases or when training at 1536px+ where bf16 base would spill. Key nuance: fp8 on Blackwell can raise tensor throughput, but for a small LoRA the bottleneck is rarely the matmul precision - so 'fp8 is faster' does not reliably translate to faster LoRA training, and you pay the quality risk for an uncertain gain. (Honest note: this is a RESEARCH wave - these are reproduced-from-source / community-ranked claims, not 5090-measured this wave; the rig-measured precision/throughput receipts belong in tensor-engine.)
- **For the pipeline:** Studio precision policy by base size on the 32GB rig: Chroma1-HD / klein-4B -> bf16 base (it fits; spend headroom on resolution/batch). 12B dev-class or >=1536px -> fp8/NF4 frozen base + bf16 trainable + bf16 compute. Never quantize the trainable LoRA path or optimizer state to fp8 for quality work. Do not assume fp8 = faster for LoRA; verify on the rig (tensor-engine) before adopting for speed.
- **Method:** lora · **Applies to:** diffusion · **Base:** flux · **Kind:** method-theory
- **Validated under:** VRAM figures (26GB bf16 / ~9GB QLoRA) are HF-measured on a 4090, NOT on the 5090; the fp16>bf16>fp8 quality ordering is community-ranked for diffusion inference/training; fp8-throughput-on-Blackwell is vendor-claimed. No 5090 measurement this wave - rig receipts go to tensor-engine.
- **Output license:** commercial **yes** — Precision choice is base-agnostic; applies to Apache-2.0 bases. NF4/bitsandbytes and torchao fp8 are permissively licensed tooling (catalogued as instruments, not weights).
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| precision | bf16 enum | ● | Default mixed-precision compute + trainable path. Quality floor for the LoRA itself. |
| fp8_base | false bool | ○ | Quantize the FROZEN base to fp8 only under VRAM pressure (12B dev / >=1536px). Never the trainable path. |
| optimizer | adamw8bit enum | ○ | 8-bit AdamW shrinks optimizer state - often enough headroom to avoid fp8 base entirely on the small Apache bases. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| OOM training 12B dev-class base in full bf16 at high resolution on 32GB. | bf16 base + optimizer state spills past 32GB. | Switch the FROZEN base to fp8/NF4 (keep trainable path bf16); or use 8-bit AdamW; or drop resolution. | fp8_base |
| Subtle banding / loss of fine gradient in outputs after going fp8-everywhere. | fp8 compute on the trainable path is below the quality floor for diffusion. | Keep trainable path + compute at bf16; only the frozen base may be quantized. | precision |
| Adopted fp8 for speed but training is no faster. | Small LoRA matmuls are not precision-bound; fp8 throughput gains do not materialize. | Use bf16 for quality; only adopt fp8 after a rig-measured speed win (tensor-engine). | precision |

- **Best for:** Choosing training precision on a 32GB card (precision-policy, fit 5)
- **Verify:** verdict=confirmed | currency=Current for 2026. fp8 via torchao requiring compute capability 8.9+ (Blackwell satisfies) is the current state. | HF flux-qlora confirmed (QLoRA NF4 ~9GB vs bf16 ~26GB). HF flux-2 blog confirmed (fp8 torchao + NF4 bitsandbytes options, ~20GB free VRAM for 4-bit). SECourses Medium post on quality ranking is a community-claim source, PARTIAL marking appropriate. The key principle — bf16 trainable path is the quality floor, quantize only the frozen base — is coherent and supported. evidence_strength 'reproduced-from-source' is borderline generous given the quality-ranking finding comes from a community benchmark, but the bf16-as-floor claim traces to the HF official blog. Acceptable. DEDUP: no wave-1 technique covers training precision. New knowledge.
- **Sources:** [(LoRA) Fine-Tuning FLUX.1-dev on Consumer Hardware - QLoRA/NF4 vs bf16 VRAM](https://huggingface.co/blog/flux-qlora) (Hugging Face / Sayak Paul et al., 2025) — QLoRA (NF4 frozen base + bf16) ~9GB peak vs 26GB plain bf16 LoRA, nearly identical results; text encoders + VAE frozen. ; [Diffusers welcomes FLUX-2 - fp8 (torchao) and NF4 training on 24-32GB](https://huggingface.co/blog/flux-2) (Hugging Face, 2026) — fp8 training via torchao needs compute capability 8.9+; NF4 via bitsandbytes as alternative; example uses bf16 mixed precision + fp8 training + grad checkpointing for constrained hardware. ; [BF16 vs GGUF FP8 Scaled NVFP4 Speed and Quality Compared (FLUX.2 Klein)](https://medium.com/@furkangozukara/bf16-vs-gguf-fp8-scaled-nvfp4-speed-quality-compared-comfyui-cuda-13-gains-flux-2-klein-9b-dd7f64edcd89) (Furkan Gozukara (SECourses), 2026) — Community quality ranking fp16 > bf16 > fp8_scaled > fp8_e4m3fn for Flux workflows; fp8 buys VRAM/speed at a quality cost.

### NL captioning depth for frozen-encoder Flux/klein - JoyCaption vs Florence-2 vs CogVLM2, length budget, and the T5/Qwen3 freeze · `recommended` · · community
**Captioner choice and caption LENGTH are load-bearing for frozen-encoder Flux LoRA: JoyCaption (uncensored, diffusion-training-built) for full-scene NL, Florence-2 for dense/grounded detail, CogVLM2 for the richest long-form descriptions - and the caption must fit the encoder budget (T5 ~256 tok for FLUX.1/Chroma; Qwen3 ~512 tok for klein) without overrunning it, because the encoder is frozen and cannot learn new tokens.**
Wave-1 established the principle (NL captions, frozen encoder, style-vs-content pruning toward a trigger, JoyCaption/Florence-2 as captioners). This row deepens the captioner SELECTION and the length/budget mechanics, and folds in the klein/Qwen3 correction. Captioner tradeoffs: (1) JoyCaption - purpose-built for diffusion training, uncensored, produces fluent full-scene paragraphs; best default for stylized game art (won't refuse stylized violence/skin). (2) Florence-2 - dense captioning + grounding (region-level); produces tighter, more literal descriptions, good when you need precise object/composition naming but its prose is terser. (3) CogVLM2 - the richest long-form describer, strong for complex scenes where you want maximum descriptive coverage; heavier to run. The length mechanic is the new depth: each frozen encoder has a token budget - T5-XXL ~256 tokens for FLUX.1/Chroma, Qwen3 ~512 for klein-4B (max sequence 512). A caption that overruns the budget is silently truncated, so the tail (often the composition/lighting detail) is dropped from conditioning; a caption far UNDER budget wastes capacity the LLM encoder could use. Target a caption that fills most of the budget with content description while keeping the STYLE attributes OUT (so they bind to the trigger, not the words) - this is the wave-1 style-vs-content rule, now quantified against the budget. Two corrections for this lane: (a) klein's encoder is Qwen3, not the 24B Mistral wave-1's caption row stated - Qwen3 being an instruction-tuned LLM means it parses fluent, even structured NL especially well, reinforcing the NL-over-tags rule. (b) The TE stays FROZEN in all cases (0 TE modules trained) - captions exploit what the encoder already knows; you never caption to 'teach' the encoder. Pin one captioner + one normalization pass + one trigger convention per style pack so the dataset is replayable.
- **For the pipeline:** In style-dataset-lab, expose captioner as a per-pack choice with a default: JoyCaption for stylized game art, Florence-2 when composition precision matters, CogVLM2 for complex multi-element scenes. Enforce a caption-length check against the target base's encoder budget (256 for T5/Chroma, 512 for Qwen3/klein) at curation time - flag truncation. Update the wave-1 caption row's encoder claim (klein = Qwen3, not Mistral). Keep the encoder frozen and keep style attributes out of the words.
- **Method:** lora · **Applies to:** diffusion · **Base:** flux · **Kind:** curation
- **Validated under:** Captioner-strength tradeoffs and token budgets reproduced from VLM/captioner docs and the FLUX.2 klein architecture writeups (Qwen3, 512 max seq); the per-captioner 'best for' mapping is a community/studio-reasoned guideline, not a measured caption-ablation this wave.
- **Builds on (stage 2):** Natural-language caption craft for frozen-encoder Flux LoRA (JoyCaption / Florence-2)
- **Output license:** commercial **conditional** — Captioners are TOOLS (cited as instruments). JoyCaption/Florence-2/CogVLM2 weights have their own licenses - the GENERATED captions are usually fine to ship with a studio-owned dataset, but verify each captioner's output-use terms before shipping commercially; the base-model commercial gate (Apache bases only) is separate and binding.
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| caption_strategy | natural-language enum | ● | Fluent NL paragraphs, not booru tags - frozen LLM/T5 encoder expects language. |
| te_lr | 0 scalar | ● | Text encoder frozen (T5/Qwen3); 0 TE modules trained in all Flux-family LoRAs. |

- **Datasets:** Cyanotype regularization set (white background) — token-gating contrast (regularization, license Studio-owned (synthetic). Verify generation provenance for commercial cleanliness.) ; Cyanotype 'stdstyl' style set (Flux/Chroma) (train, license Studio-owned (synthetic, generated in-house). Commercial-clean when the generating base is Apache-2.0/clean — verify generation provenance before shipping.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Composition/lighting detail in the caption seems ignored during training. | Caption overran the encoder token budget (256 T5 / 512 Qwen3) and was silently truncated, dropping the tail. | Trim captions to fit the target base's budget; put content first, style out. | caption_strategy |
| Captioner refuses or sanitizes stylized game-art content (violence/skin). | Using a censored VLM captioner. | Use JoyCaption (uncensored, diffusion-training-built) for stylized content. | caption_strategy |
| Style described in words bleeds into content; trigger under-binds the style. | Style attributes left in the caption text instead of reserved for the trigger token. | Style-vs-content pruning: describe content in NL, keep style attributes on the trigger only. | caption_strategy |

- **Best for:** Captioning stylized game art for Flux/klein (caption, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current for 2026. Qwen3 encoder for klein, Mistral for full FLUX.2, confirmed. | Geronimo medium post confirmed (Qwen3-4B, 512 max tokens for klein). HF flux-2 blog confirms Mistral Small 3.1 for full FLUX.2 dev/pro, NOT for klein — this is correctly distinguished in the technique. JoyCaption HF card confirmed (uncensored, diffusion-training-built, fancyfeast). DEDUP flag: wave-1 'flux-natural-language-caption-frozen-t5' explicitly covers JoyCaption and Florence-2 for frozen-encoder Flux captioning. The wave-3 entry partially restates that. The genuine extension is the encoder-budget differential (T5 ~256 tok for FLUX.1/Chroma vs Qwen3 ~512 tok for klein) and the explicit CogVLM2 addition. The technique should be reframed to lead with the encoder-budget differential as the primary contribution, positioning JoyCaption/Florence-2 as prior-art from wave-1 rather than new findings. evidence_strength 'community-claim' is correctly modest given the T5 256-token figure and 'JoyCaption is best' are community consensus rather than paper-cited.
- **Sources:** [FLUX.2 Klein - How Inference Works (Qwen3 encoder, 512 max sequence)](https://medium.com/@geronimo7/flux-2-klein-how-inference-works-05553fcdbe7e) (Geronimo, 2026) — klein uses Qwen3 (4B/8B) text encoder with hidden states from layers 9/18/27; max sequence length 512 - the caption budget for klein and the Mistral correction. ; [Diffusers welcomes FLUX-2 - Mistral Small 3.1 is the big-FLUX.2 encoder (not klein)](https://huggingface.co/blog/flux-2) (Hugging Face, 2026) — FLUX.2 (dev/pro) uses Mistral Small 3.1, max sequence 512; clarifies Mistral is the big-model encoder, distinct from klein's bundled Qwen3. ; [JoyCaption - uncensored captioner built for diffusion training](https://huggingface.co/fancyfeast/llama-joycaption-alpha-two-hf-llava) (fancyfeast, 2025) — Open, uncensored VLM purpose-built to produce diffusion-training captions; default captioner for stylized content.

### Natural-language caption craft for frozen-encoder Flux LoRA (JoyCaption / Florence-2) · `recommended` · · community
**Because Flux/Chroma freeze the text encoder during LoRA (no TE training) and feed a long-context T5/Mistral encoder, captions must be rich natural-language descriptions — not the comma-separated booru tags that work for SDXL — with a trigger token carrying the style.**
Flux-family LoRAs train the DiT only; the text encoder (T5-XXL for FLUX.1/Chroma, Mistral-3 for FLUX.2) is frozen, so the encoder cannot be taught new token semantics — captions must lean on what the encoder already understands, which is fluent natural language with a high token budget (T5 ~256 tokens vs CLIP's 77). The studio practice: auto-caption with JoyCaption (free/open/uncensored VLM built for diffusion-training captions) or Florence-2 (detailed/dense captioning), normalize class names, prepend a unique trigger token for the style, and describe content (subject, composition, lighting) in natural sentences while NOT describing the style attributes you want bound to the trigger. For FLUX.2 [klein]'s single 24B Mistral encoder this matters even more — comma-tag captions waste the VLM's capacity.
- **For the pipeline:** The dataset-caption lane owns generic caption theory; THIS row is the Flux-specific override: NL captions, frozen encoder, style-vs-content pruning aimed at a trigger token rather than tag pruning. Wire JoyCaption/Florence-2 as the captioner in style-dataset-lab for any Flux/Chroma pack; keep booru-tag captioning on the SDXL path only.
- **Method:** lora · **Applies to:** diffusion · **Base:** Flux · **Kind:** curation
- **Tuning budget:** None measured; practitioner consensus + the measured Chroma run used NL-style captions with a 'stdstyl' trigger successfully. · **Search:** none
- **Variance:** Captioner-tooling and NL-vs-tag guidance are community/practitioner consensus plus tool docs; not a controlled on-rig ablation. The frozen-encoder fact is from the kohya trainer (DiT-only). Tagged no higher than community-claim for the caption-strategy half.
- **Output license:** commercial **conditional** — Caption craft is license-neutral, but the CAPTIONER's license matters for the pipeline: JoyCaption is free/open with no restrictions; Florence-2 is MIT. Captioner choice does not encumber the trained LoRA, but verify each tool's license before shipping the pipeline.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| te_lr | 0 (frozen) | ● | Text encoder is frozen for Flux/Chroma LoRA — no TE modules trained; captions must use existing encoder semantics. |

- **Datasets:** Cyanotype 'stdstyl' style set (Flux/Chroma) (training, license Studio-owned (synthetic, generated in-house). Commercial-clean when the generating base is Apache-2.0/clean — verify generation provenance before shipping.)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Style fails to bind to the trigger / leaks into all generations or none | Style attributes were described in the captions, so the model attributed the style to those words instead of the trigger token; or only booru tags were used so the frozen NL encoder got weak signal. | Describe content in natural language, NEVER describe the style you want bound; reserve a unique trigger token (e.g. 'stdstyl') for the style; caption with JoyCaption/Florence-2 then normalize. | captions |

- **Best for:** Captioning a Flux/Chroma style-LoRA training set (flux, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. Frozen-encoder LoRA behavior for Flux is accurate. NL caption vs. booru tags guidance is well-established practitioner consensus. JoyCaption Beta One (2025) and Florence-2 are both current tools. | Two minor issues. (1) Title says 'frozen-T5' but Chroma freezes a different encoder (no T5) and FLUX.2 klein freezes Qwen3 — the frozen-encoder principle is correct but the T5 label is outdated for the full scope of models covered by the studio workflow. Low severity since the technique body says 'T5/Mistral encoder' acknowledging variance. (2) Florence-2 arXiv:2311.06242 is real, authors match (Xiao et al.), content supports captioning use. JoyCaption repo confirmed (fpgaminer/joycaption, Llama 3.1 + SigLIP). Kohya discussions/1497 is a real community thread. Evidence strength community-claim is honestly tagged. The partial support flag on the kohya discussion source is appropriate. No overclaiming detected.
- **Sources:** [Florence-2: Advancing a Unified Representation for a Variety of Vision Tasks](https://arxiv.org/abs/2311.06242) (Xiao, Wu, Xu, Dai, Hu, Lu, Zeng, Liu, Yuan, 2023) — Florence-2 is a prompt-driven vision foundation model with strong zero-shot and fine-tuned captioning/dense-region capability — usable as a dataset captioner. ; [JoyCaption — free, open, uncensored captioning VLM built for training diffusion models](https://github.com/fpgaminer/joycaption) (fpgaminer (fancyfeast), 2025) — JoyCaption is a free/open/uncensored VLM (Llama 3.1 + SigLIP) built specifically to generate descriptive captions for diffusion-model training, with no usage restrictions. ; [What Exactly to Caption for Flux LoRA Training? / flux lora training TIPs (kohya-ss Discussion #1497)](https://github.com/kohya-ss/sd-scripts/discussions/1497) (community, 2024) — Flux uses long-context natural-language captioning (T5 ~256 tokens); practitioners caption with NL (and optionally tags) and the encoder is frozen during LoRA, so captions rely on existing encoder semantics.

### The guidance-distilled-base training problem (FLUX.1-dev/FLUX.2-dev) - train at guidance_scale=1.0, reintroduce CFG at sampling · `situational` · ▸ reproduced
**FLUX.1-dev (and FLUX.2 [dev]) ship guidance-distilled - the CFG operation is baked into a single forward pass conditioned on a guidance-embedding input - so a LoRA must be trained at guidance_scale=1.0 to PRESERVE that distillation, and any non-1.0 training value silently de-distills the base and can collapse the model on long runs.**
Guidance distillation (Meng et al., CVPR 2023, arXiv:2210.03142) folds the two-model classifier-free-guidance evaluation into one network that takes the guidance weight as a conditioning input, so the dev models do a straight-shot trajectory and do NOT consume negative prompts at inference. The training consequence is load-bearing and separate from the flow-matching schedule (wave-1): in kohya/SimpleTuner/ai-toolkit you set --guidance_scale 1.0 during training, which feeds the distilled guidance embedding its expected value and leaves the distillation intact; the LoRA then learns style on top of a frozen-guidance manifold. Setting a training guidance >1.0 (e.g. 3.5) tells the model to RELEARN explicit CFG - it begins unlearning the distillation, which (a) burns capacity on re-introducing CFG instead of your style and (b) destroys the guidance embedding and collapses outputs if the run is long enough. At SAMPLING you do the opposite: dev models want guidance 2.0-4.0 (the distilled embedding interprets this as CFG strength) - so a LoRA trained at guidance 1.0 is then served at guidance ~3.5. This is the inverse of Chroma (wave-1: guidance 0.0 at train because Chroma is schnell-derived and de-distilled) and the inverse of FLUX.2 [klein] base (undistilled - full real CFG at sampling, see sibling recipe). The decision tree: distilled base -> train g=1.0, sample g=2-4; de-distilled/schnell base -> train g=0.0; undistilled base -> train with normal CFG semantics.
- **For the pipeline:** Every Flux-family recipe template MUST carry an explicit per-base guidance policy with TWO values - train_guidance and sample_guidance - never one. Bake the table into the studio's flux recipe: FLUX.1-dev = train 1.0 / sample 2.0-4.0 (distilled); Chroma1-HD = train 0.0 (de-distilled schnell); FLUX.2 [klein] base = undistilled, no guidance embedding, options ignored. Treating guidance as a single SDXL-style CFG slider is the single most common Flux-LoRA collapse cause.
- **Method:** lora · **Applies to:** diffusion · **Base:** flux · **Kind:** method-theory
- **Validated under:** Holds for guidance-distilled BFL bases (FLUX.1-dev, FLUX.2 [dev]); does NOT apply to Chroma (de-distilled schnell) or FLUX.2 [klein] base (undistilled, guidance options ignored). Not measured on the 5090 this wave.
- **Base model (model-knowledge):** `flux1-dev`
- **Builds on (stage 2):** Flow-matching training schedule (sigmoid/shift timestep + raw prediction) — why Flux is a separate recipe space from SDXL/DDPM
- **Output license:** commercial **no** — FLUX.1-dev and FLUX.2 [dev] are under the FLUX Non-Commercial License - training a LoRA ON them or serving outputs commercially is prohibited. The THEORY here is portable to any guidance-distilled base; apply it commercially only on an Apache-2.0 undistilled/de-distilled base (Chroma1-HD, FLUX.2 [klein] 4B).
- **Fit:** rig 4/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| guidance_scale | 1.0 scalar | ● | TRAINING value for distilled dev bases - preserves the distilled guidance embedding. Never raise it during training. |
| learning_rate | 1e-4 scalar | ○ | Typical dev LoRA lr; lower (8e-5) for style, higher for character. |
| timestep_sampling | flux_shift enum | ○ | FLUX.1-dev default sampler family (vs sigmoid for Chroma). |
| model_prediction_type | raw enum | ● | Flow-matching raw prediction, same as Chroma. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Outputs progressively wash out / lose contrast / collapse to mush as training proceeds, despite a sane lr. | Trained at guidance_scale > 1.0 on a distilled dev base, unlearning the guidance distillation and destroying the guidance embedding. | Set --guidance_scale 1.0 for training; only raise guidance (2-4) at sampling. | guidance_scale |
| LoRA trained on dev looks flat/under-saturated at inference even at sane strength. | Sampling at guidance 1.0 (training value) instead of the distilled inference range. | Sample at guidance 2.0-4.0; the distilled embedding reads this as CFG strength. | guidance_scale |

- **Best for:** Understanding why dev-base LoRAs collapse (flux-theory, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current for 2026. FLUX.1-dev and FLUX.2-dev remain guidance-distilled; training at guidance_scale=1.0 is the standing recommendation across all major trainer docs. | arXiv:2210.03142 confirmed real (CVPR 2023, correct authors/title). SimpleTuner FLUX.md confirmed exists and supports the 1.0 guidance preservation claim. The overclaim to fix: SimpleTuner says non-1.0 'reintroduces CFG and affects inference compatibility / requires a different inference pipeline' — NOT that it 'collapses the model on long runs.' The collapse language is not supported by the cited source. Remove or soften to 'de-distills the base and requires a modified inference pipeline.' Medium blog (John Shi) is PARTIAL as marked — acceptable. evidence_strength 'reproduced-from-source' is justified. DEDUP: wave-1 flux-flow-matching-timestep-prediction-theory mentions guidance_scale briefly as a lever; this wave-3 entry goes substantially deeper into the distillation mechanism and inference re-introduction at 2-4. Not a duplicate.
- **Sources:** [On Distillation of Guided Diffusion Models](https://arxiv.org/abs/2210.03142) (Meng, Rombach, Gao, Kingma, Ermon, Ho, Salimans, 2023) — Distills classifier-free guidance into a single network conditioned on the guidance weight - the mechanism BFL applies to make FLUX.1-dev guidance-distilled. ; [SimpleTuner FLUX.1 quickstart - guidance_scale training behavior](https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/FLUX.md) (bghira, 2026) — guidance_scale=1.0 preserves the dev distillation; non-1.0 values reintroduce CFG and can collapse the model on long runs; train at 1, inference at 2-4. ; [Why Flux LoRA So Hard to Train and How to Overcome It](https://medium.com/@zhiwangshi28/why-flux-lora-so-hard-to-train-and-how-to-overcome-it-a0c70bc59eaf) (John Shi, 2025) — Flux-dev is guidance-distilled and does not use negative prompts; training implications of the distilled embedding.

