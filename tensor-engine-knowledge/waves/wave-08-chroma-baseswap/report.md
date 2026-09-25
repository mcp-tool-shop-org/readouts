# Wave 8 — Blue-fidelity base swap: Chroma1-HD LoRA (resolves the wave-7 SDXL blue ceiling)

**Date:** 2026-06-03 · **Rig:** RTX 5090 · **Engine:** kohya `flux_train_network.py --model_type chroma` (sd-scripts, engine #48) · Recorded as **#167 (baseline) + #168 (recipe)**; wave-7 **#165** cross-linked.

Wave 7 proved SDXL base 1.0 can't render the saturated cyanotype **blue** with style+gating — it's the base's color prior. Wave 8 swaps the base to a flexible one and tests whether "have it all" lands.

## Why Chroma, not Z-Image/Lumina2

The originally-named path is **infeasible here**: Z-Image-Turbo's text encoder is **Qwen3-4B**, but kohya's `lumina_train_network.py` is hardcoded for Lumina-Image-2.0's **Gemma-2** TE. Z-Image only shares ComfyUI's "lumina2" *loader type* — it's not a Lumina-2 model and has no kohya trainer installed. **Chroma1-HD** is the better vehicle anyway: 8.9B FLUX.1-schnell-derived, **Apache-2.0** (LoRA inherits it), explicitly a neutral base for LoRA across *artistic* styles, on-disk, kohya-native (`library/chroma_models.py`).

## Two gotchas earned (both load-bearing)

1. **`--cache_text_encoder_outputs` ✗ `--apply_t5_attn_mask`** — the cached path leaves `batch['input_ids_list']=None` → crash at **step 0** (`train_network.py:432`). Chroma *requires* the attn mask, so TE caching must be **off** (T5 runs live). Keep `--cache_latents`.
2. **bf16 Chroma + live T5 spills the 32 GB card** — VRAM pinned at **31974/32607 MiB**, step time ballooned **5 → 34 s/it** (WDDM paging). **`--fp8_base`** → ~20 GB, **2.65 s/it**, ~27 min / 600 steps.

## Proven config

`Chroma1-HD.safetensors` + `--fp8_base`, `t5xxl_fp8_e4m3fn`, `ae`; `networks.lora_flux` dim16/alpha16; AdamW; `--guidance_scale 0.0 --timestep_sampling sigmoid --model_prediction_type raw --apply_t5_attn_mask`; `--sdpa --gradient_checkpointing --cache_latents` (no TE cache); reg gating via TOML; 600 steps; seed 42. LoRA `b90176156eaa546b`, 107 MB.

## Result — the base swap resolves the blue ceiling

- **Gating: crisp and cleaner than SDXL.** B (no trigger) = photorealistic/normal color (matches reg); C (trigger) = trained style. Base quality far higher.
- **Strong cyanotype BLUE achieved** — SDXL base 1.0 never did this at any setting. Strength sweep: the **ship saturates to white linework on deep Prussian blue at LoRA strength 1.5–2.0**. The blue *is* in the LoRA; recommended inference strength **~1.3–1.5**.
- **Subject-dependent residual:** scenes (ship) get the full blue field; **isolated subjects (portrait) render white-line on a *white* bg** even at strength 2.0. Root cause: the **reg images used "plain white background,"** so the contrast taught white as the neutral bg. **Fix for universal blue:** regenerate the reg set with varied/colored backgrounds.

**Conclusion:** on a flexible commercial-safe base (Chroma, Apache-2.0) the cyanotype blue + linework style + token gating + high base quality all land together (strength ~1.5), where SDXL base 1.0 could only ever get two of the three. Proof: `proof/01_chroma_ABC.png`, `proof/02_chroma_strength_sweep.png`.

## Standards compliance (per `.claude/rules/workflow-standards.md`)

| Standard | Score | Evidence |
|---|---|---|
| PIN_PER_STEP | **2** | Pinned: base (Chroma1-HD), model_type, network_module/dim/alpha, lr, trigger, seed 42, steps, all Flux/Chroma flags; LoRA sha256 in #167; dataset TOML archived. *Gap (P3):* base sha256 filename-only. |
| ANDON_AUTHORITY | **3** | Two real halts fired and were fixed before proceeding: the step-0 `input_ids_list` crash (config halt) and the VRAM-spill (caught by the 34 s/it andon check → killed + fixed). Every image looked at; bad config never propagated to the long run. |
| NAMED_COMPENSATORS | **3** | Idempotent recorder (DELETE wave 8 + ids 167/168), git-revertable DB; LoRA/dataset files `rm`-able + reproducible from seed+config. No external irreversible action. |
| DECOMPOSE_BY_SECRETS | **2** | Clean split: dataset TOML (data) / flux_train_network flags (engine) / Chroma inference graph (validation) / recorder (DB). |
| UNCERTAINTY_GATED_HUMANS | **2** | Surfaced the Z-Image→Chroma pivot decision with reasons before committing; the strength sweep (not assertion) settled the blue question. |
| EXTERNAL_VERIFIER | **3** | Trigger-fires A/B (Chroma generator vs base-only control, image is the only evidence) **plus** an independent strength sweep cross-checking the blue claim. |

**Total: 15 / 18 (83%).**

## Irreversible actions and compensators

| Action | Compensator | Owner | Window |
|---|---|---|---|
| Insert wave 8 + recipes #167/#168, cross-link #165 (`engines.db`) | Idempotent recorder; `git revert <sha>` | advisor | forever |
| Write `stdstyl_chroma_lora.safetensors` (+ ComfyUI `loras/` copy) | `rm` (reproduces from seed+config) | user | session-bound |
| Archive proof/scripts into `waves/wave-08-chroma-baseswap/` (git) | `git revert <sha>` | advisor | forever |

No npm/release/Pages/push of shared state — local repo + local ComfyUI only.

## Artifacts

`proof/` — 01 Chroma A/B/C grid · 02 strength sweep (the cyanotype money shot: ship @ 1.5–2.0) · `_lora_validate_chroma.py` · `_chroma_strength_sweep.py` · `chroma_dataset.toml` · `train_chroma.log`. Trained LoRA (107 MB, gitignored) at `E:\AI\training\output\` + ComfyUI `loras/`.

## Open (wave-9 candidate)

Universal-subject blue: regenerate the reg set with **varied/colored backgrounds** (not white) so the blue field isn't contrasted away for isolated subjects, then retrain. Expected to extend the strong cyanotype from scenes to portraits/objects.
