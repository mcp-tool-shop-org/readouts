# Catalog — training craft (methods · recipes · datasets · eval · debug)

Generated from `training.db` · wave 16 · 2026-09-13. Narrative + plan: [wave-01 dispatch](../waves/wave-01-foundation/dispatch.md). Verification receipt: [verification.md](../waves/wave-01-foundation/verification.md).

The portable **how-to-train** layer for this rig (RTX 5090 · Blackwell · 32 GB · Win 11 / WSL2). Sibling KBs: [model-knowledge](../../model-knowledge/catalog/README.md) (the *weights*) · [tensor-engine-knowledge](../../tensor-engine-knowledge/catalog/README.md) (the *software* + rig-measured receipts). This one owns the *methods, recipes, hyperparameter values, dataset & eval craft* — and points at the measured numbers via `engine_recipe_ref`, never restates them.

## Try-first shortlist

Top `recommended` picks per lane, by try-first order. `Evidence` ▣ measured-on-rig is the strongest tier.

| Lane | ↓ | Technique | Method | Applies | Evidence | Comm | ✓ |
|---|---|---|---|---|---|---|---|
| PEFT methods & adapter theory | 2 | [LoRA: rank and alpha as a coupled scaling pair (alpha/rank = effective-LR multiplier)](peft-methods.md) | lora | both | ▸ reproduced | ✅ yes | ✓ |
| PEFT methods & adapter theory | 2 | [LyCORIS: the diffusion adapter family (LoCon conv, LoKr Kronecker, LoHa Hadamard)](peft-methods.md) | lokr | diffusion | ▸ reproduced | ⚠ cond | ✓ |
| PEFT methods & adapter theory | 2 | [QLoRA: LoRA over a 4-bit NF4 frozen base (NF4 + double-quant + paged optimizers)](peft-methods.md) | qlora | llm | ▸ reproduced | ⚠ cond | ✓ |
| SDXL style-LoRA recipes (priority) | 1 | [AdamW8bit SDXL LoRA — MEASURED (no VRAM saving for LoRA; ~4% faster than fp32)](diffusion-sdxl-lora.md) | lora | diffusion | ▣ measured | ✅ yes | ✓ |
| SDXL style-LoRA recipes (priority) | 1 | [Checkpoint selection — MEASURED: best != last (peak ~600, plateau 450-900; <=150 undertrains)](diffusion-sdxl-lora.md) | lora | diffusion | ▣ measured | ✅ yes | ✓ |
| SDXL style-LoRA recipes (priority) | 1 | [Multi-concept repeat-balancing — MEASURED: distinct triggers protect own-fidelity; imbalance shows as cross-bleed, not collapse](diffusion-sdxl-lora.md) | lora | diffusion | ▣ measured | ✅ yes | ✓ |
| Flux-family style-LoRA recipes | 1 | [Chroma LoRA eval/inference on the rig — kohya samplers give NOISE; use flux_minimal_inference fp8 + REAL CFG (the scriptable path)](diffusion-flux-lora.md) | lora | diffusion | ▣ measured | ✅ yes | ✓ |
| Flux-family style-LoRA recipes | 1 | [Chroma LoRA rank/dim sweep (8/16/32) — MEASURED on the 5090 (size linear; higher rank binds the saturated palette more completely — unlike SDXL)](diffusion-flux-lora.md) | lora | diffusion | ▣ measured | ✅ yes | ✓ |
| Flux-family style-LoRA recipes | 1 | [Chroma discrete_flow_shift sweep (1/3/6) — MEASURED (footprint-neutral; shift 6 marginally best fidelity; weakest lever)](diffusion-flux-lora.md) | lora | diffusion | ▣ measured | ✅ yes | ✓ |
| Dataset construction & caption craft | 2 | [Augmentation safety policy (flip / random-crop / color) for style sets](dataset-caption.md) | dataset-construction | diffusion | ▸ reproduced | ✅ yes | ✓ |
| Dataset construction & caption craft | 2 | [Caption format keyed to the base model's text encoder](dataset-caption.md) | lora | diffusion | ▸ reproduced | ⚠ cond | ✓ |
| Dataset construction & caption craft | 2 | [Concept isolation for multi-concept LoRAs (anti-bleed)](dataset-caption.md) | dataset-construction | diffusion | ▸ reproduced | ✅ yes | ✓ |
| Local LLM fine-tuning (SFT + preference + RL) | 1 | [DPO (LoRA) preference tuning (stage 2) — paired data, needs ref model](llm-finetune.md) | dpo | llm | ▣ measured | ⚠ cond | ✓ |
| Local LLM fine-tuning (SFT + preference + RL) | 1 | [QLoRA-NF4 SFT with chat template (stage 1) — 8-34B on one 5090](llm-finetune.md) | qlora | llm | ▣ measured | ⚠ cond | ✓ |
| Local LLM fine-tuning (SFT + preference + RL) | 1 | [Unsloth LLM-QLoRA MEASURED baseline (native-Win 5090, Qwen3-4B) + the xformers/torchvision install-churn fix](llm-finetune.md) | qlora-sft | llm | ▣ measured | ✅ yes | ✓ |
| Single-GPU efficiency & training-VRAM technique | 1 | [gradient_checkpointing is mandatory for lycoris.kohya LoRA on 32 GB (MEASURED 27.7 -> 14.5 GB)](efficiency.md) | lora | diffusion | ▣ measured | ✅ yes | ✓ |
| Single-GPU efficiency & training-VRAM technique | 2 | [8-bit / paged AdamW (bitsandbytes) — cut and spill the optimizer-state addend](efficiency.md) | qlora | both | ▸ reproduced | ✅ yes | ✓ |
| Single-GPU efficiency & training-VRAM technique | 2 | [Gradient-checkpointing + bf16 + grad-accum — the activation-addend trio](efficiency.md) | lora | both | ▸ reproduced | ✅ yes | ✓ |
| Training evaluation & validation methodology | 1 | [Diffusion style-fidelity eval panel — MEASURED (CLIP-sim + CMMD, n=20) on the wave-4 SDXL LoRAs](evaluation.md) | lora | diffusion | ▣ measured | ✅ yes | ✓ |
| Training evaluation & validation methodology | 2 | [Acceptance threshold calibration + bare-scalar ban (delta-vs-base, pre-declared, held-out)](evaluation.md) | diffusion-acceptance-gating | diffusion | ▸ reproduced | ✅ yes | ✓ |
| Training evaluation & validation methodology | 2 | [Bias-controlled different-family LLM judge (order-swap + length-match)](evaluation.md) | dpo | llm | ▸ reproduced | ✅ yes | ✓ |
| Failure modes & debugging | 2 | [Catastrophic forgetting: LoRA as the regularizer, plus the rank/effective-LR/replay levers](debugging.md) | lora | both | ▸ reproduced | ✅ yes | ✓ |
| Failure modes & debugging | 2 | [Frying / saturation: the effective-LR = unet_lr x (alpha/rank) runaway and its cure](debugging.md) | lora | diffusion | ▸ reproduced | ✅ yes | ✓ |
| Failure modes & debugging | 2 | [Overfit/replication and style-bleed: the caption+pruning+regularization fix, not the LR fix](debugging.md) | dreambooth | diffusion | ▸ reproduced | ⚠ cond | ✓ |
| Diffusion Qwen Lora | 1 | [Clean (on-canon) dataset = no late embedding-cloud collapse — 3rd cross-run confirmation; pick the ship checkpoint by geometry, not CLIP-sim](diffusion-qwen-lora.md) | evaluation | diffusion | ▣ measured | ✅ yes | ✓ |
| Diffusion Qwen Lora | 1 | [Qwen-Image literalizes NOUNS in style descriptors — name light by material, not object (58/58 lantern-prop rate; negatives lose)](diffusion-qwen-lora.md) | dataset | diffusion | ▣ measured | ✅ yes | ✓ |
| Diffusion Qwen Lora | 1 | [Qwen-Image style-LoRA on 32GB (AI-Toolkit uint3+ARA) — MEASURED on the 5090 (the first Qwen-Image-as-base row)](diffusion-qwen-lora.md) | lora | diffusion | ▣ measured | ✅ yes | ✓ |
| Trl Grpo Mechanics | 1 | [clip_ratio is identically zero at the default num_iterations=1](trl-grpo-mechanics.md) | grpo | text | ▣ measured | ✅ yes | ✓ |
| Trl Grpo Mechanics | 5 | [A group-constant reward term has exactly zero gradient under GRPO](trl-grpo-mechanics.md) | grpo | text | measured-in-source | ✅ yes | ✓ |
| Trl Grpo Mechanics | 5 | [GRPOConfig.seed does not control LoRA initialisation](trl-grpo-mechanics.md) | peft | both | measured-in-source | ✅ yes | ✓ |
| Rl Measurement Methodology | 1 | [Generations per item, not items, is usually the cheap lever on eval power](rl-measurement-methodology.md) | eval | both | ▣ measured | ✅ yes | ✓ |
| Rl Measurement Methodology | 1 | [Pooled eval statistics measure the item mix as well as the behaviour](rl-measurement-methodology.md) | eval | both | ▣ measured | ✅ yes | ✓ |
| Rl Measurement Methodology | 1 | [Run-to-run variance can exceed the effect being measured](rl-measurement-methodology.md) | rl | text | ▣ measured | ✅ yes | ✓ |
| Rlvr Sharpening And Latent Capability | 5 | [An RLVR pass-rate lift is not licensed to be called new capability](rlvr-sharpening-and-latent-capability.md) | rl | text | paper | ✅ yes | ✓ |
| Rlvr Sharpening And Latent Capability | 5 | [Plain GRPO sharpens the output prior rather than flattening it](rlvr-sharpening-and-latent-capability.md) | grpo | text | paper+measured | ✅ yes | ✓ |
| Rlvr Sharpening And Latent Capability | 5 | [Verbalized Sampling as a $0 probe for capability the policy has but never samples](rlvr-sharpening-and-latent-capability.md) | prompting | text | paper+measured | ✅ yes | ✓ |

## Lanes

- [PEFT methods & adapter theory](peft-methods.md) — Cross-cutting parameter-efficient fine-tuning theory both domains share — LoRA/QLoRA/DoRA/LoRA+/rsLoRA, diffusion LyCORIS (LoKr/LoHa/LoCon), LLM PiSSA/GaLore + merging. Rank vs alpha as a coupled scaling pair. Weights->model-knowledge; library-as-software->tensor-engine. (37 techniques)
- [SDXL style-LoRA recipes (priority)](diffusion-sdxl-lora.md) — The studio #1 workload: full hyperparameter recipes for SDXL-family style LoRAs (kohya/ComfyUI as engine references only). rank+alpha, optimizer<->LR, booru-tag captioning + style-tag pruning, regularization, 1024px bucketing, repeats/epochs, min-SNR-gamma, per-rank quality signature. (19 techniques)
- [Flux-family style-LoRA recipes](diffusion-flux-lora.md) — A SEPARATE recipe space from SDXL (flow-matching, not DDPM). Commercial-safe Apache-2.0 bases only (FLUX.2 [klein], Chroma1-HD); FLUX.1-dev/FLUX.2-dev are non-commercial and must not be a training base here. Higher rank, NL captions, frozen T5, fp8 base, no prior-preservation by default. (14 techniques)
- [Dataset construction & caption craft](dataset-caption.md) — The inputs that drive outcome more than hyperparameters: curation/dedup, caption format keyed to base model, style-vs-subject pruning, regularization sets, real:synthetic discipline, and Datasheets-style license/provenance (commercial-clean gate). Captioner weights->model-knowledge; pipeline tooling->tensor-engine. (17 techniques)
- [Local LLM fine-tuning (SFT + preference + RL)](llm-finetune.md) — 24-34B at Q-quant on one 32 GB GPU: QLoRA-NF4 SFT + chat templates, then the preference/RL family selected by the DATA you have — DPO/ORPO/KTO/SimPO and GRPO/RLVR. Light reverse-KL/on-policy distillation lives here too. (19 techniques)
- [Single-GPU efficiency & training-VRAM technique](efficiency.md) — Fitting TRAINING on one 32 GB Blackwell GPU — the binding constraint, orthogonal to method choice. The training-VRAM arithmetic (optimizer-state + gradient + activation sizing) and the decision heuristics; paged/8-bit optimizers, gradient checkpointing/accumulation, FSDP2 CPU-offload, NF4 vs fp8 training. Measured peaks->tensor-engine; inference placement->docker-knowledge. (12 techniques)
- [Training evaluation & validation methodology](evaluation.md) — How to attest a trained adapter with receipts. Diffusion STYLE eval (CMMD/HPSv2/PickScore/LPIPS + ai-eyes A/B, not DreamBooth subject metrics); LLM eval via pinned lm-eval-harness + a bias-controlled DIFFERENT-FAMILY judge. Never a bare FID/CLIP scalar. Eval tool-as-software->tensor-engine. (44 techniques)
- [Failure modes & debugging](debugging.md) — The symptom->cause->fix taxonomy that closes the recipe->result->fix loop, portable across engines: overfit/replication, frying/saturation, style-bleed, NaN/loss-spike, catastrophic forgetting, OOM-on-32GB, reward-hacking. Each maps back to the recipe field that causes and cures it. Engine-version crash receipts->tensor-engine. (4 techniques)
- [Diffusion Qwen Lora](diffusion-qwen-lora.md) — auto-created from wave lane (5 techniques)
- [Still Current](still-current.md) — auto-created from wave lane (22 techniques)
- [Trl Grpo Mechanics](trl-grpo-mechanics.md) — auto-created from wave lane (4 techniques)
- [Rl Measurement Methodology](rl-measurement-methodology.md) — auto-created from wave lane (4 techniques)
- [Rlvr Sharpening And Latent Capability](rlvr-sharpening-and-latent-capability.md) — auto-created from wave lane (3 techniques)

## Legend

- **↓** try-first order (lower = try first; derived from status + evidence strength).
- **Evidence** ▣ measured-on-rig > ▸ reproduced-from-source > · single-run / community / untested. The ordinal disciplines a single-reported claim from wearing the authority of an on-rig measurement.
- **Comm** commercial use of the OUTPUT: ✅ yes / ⚠ conditional / ⛔ no / ? unknown. A LoRA/fine-tune inherits its base model's + dataset's license.
- **Rig** fit 0–5 for this exact rig (RTX 5090 · 32 GB · Win 11 / WSL2). **Studio** fit 0–5 for the studio's actual training workloads.
- **✓** retrieval-verified this wave (existence + attribution + currency). Blank/· = unverified lead.
- **Boundary:** rig-measured it/s & VRAM peaks live in tensor-engine-knowledge (linked via `engine_recipe_ref`); base weights live in model-knowledge; inference placement in docker-knowledge.
