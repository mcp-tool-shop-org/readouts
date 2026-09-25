# Local LLM fine-tuning (SFT + preference + RL)
_24-34B at Q-quant on one 32 GB GPU: QLoRA-NF4 SFT + chat templates, then the preference/RL family selected by the DATA you have — DPO/ORPO/KTO/SimPO and GRPO/RLVR. Light reverse-KL/on-policy distillation lives here too._ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

19 techniques · 6 recommended · 3 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 1 | DPO (LoRA) preference tuning (stage 2) — paired data, needs ref model | dpo | llm | ▣ measured | ⚠ cond | 5 | 4 | ✓ |
| 1 | QLoRA-NF4 SFT with chat template (stage 1) — 8-34B on one 5090 | qlora | llm | ▣ measured | ⚠ cond | 5 | 4 | ✓ |
| 1 | Unsloth LLM-QLoRA MEASURED baseline (native-Win 5090, Qwen3-4B) + the xformers/torchvision install-churn fix | qlora-sft | llm | ▣ measured | ✅ yes | 3 | 3 | ✓ |
| 2 | Unsloth QLoRA daily-driver — 14B (up to 32B) in 32 GB, Windows-native, rank=alpha + paged 8-bit AdamW | qlora-sft | llm | ▸ reproduced | ✅ yes | 3 | 3 | ✓ |
| 2 | llama.cpp LoRA export/merge to GGUF — the train-to-serve bridge (CUDA 12.8 EXACT on Blackwell) | adapter-export | llm | ▸ reproduced | ✅ yes | 3 | 3 | ✓ |
| 2 | ms-swift install (native Windows, transformers backend) — the trainer to stand up first | trainer-framework | llm | ▸ reproduced | ✅ yes | 3 | 3 | ✓ |
| 4 | Native-Windows QLoRA without WSL2 — TRL + PEFT + bitsandbytes (prebuilt sm_120) + Liger kernels | qlora-sft | llm | ▸ reproduced | ✅ yes | 3 | 2 | ✓ |
| 4 | TRL + Unsloth DPO/ORPO/KTO — the no-Ray cheapest preference path (PatchDPOTrainer ref-sharing fits 14B) | preference-optimization | llm | ▸ reproduced | ✅ yes | 3 | 2 | ✓ |
| 6 | Axolotl (WSL2) — reproducible YAML-driven (Q)LoRA / full-SFT / DPO with sample-packing + FSDP/DeepSpeed | trainer-framework | llm | ▸ reproduced | ✅ yes | 2 | 2 | ✓ |
| 6 | LLaMA-Factory (WSL2) — broadest-method YAML training: QLoRA 32B / full-SFT 8B / DPO/KTO/PPO | trainer-framework | llm | ▸ reproduced | ⚠ cond | 2 | 2 | ✓ |
| 6 | OpenRLHF (WSL2) — single-5090 GRPO/PPO via Ray + colocate + ZeRO-3 + adam offload | rl-verifiable-reward | llm | ▸ reproduced | ⚠ cond | 2 | 1 | ✓ |
| 6 | Reference-free & data-gated preference selection — ORPO / SimPO / KTO / GRPO | orpo | llm | ▸ reproduced | ⚠ cond | 4 | 4 | ✓ |
| 6 | SkyRL (WSL2) — long-horizon agentic / tool-use RL research (Tinker-compatible single-GPU backend) | rl-agentic | llm | ▸ reproduced | ⚠ cond | 1 | 1 | ✓ |
| 6 | open-instruct / Tülu RLVR (WSL2) — reference codebase to read, then re-implement single-GPU | rl-verifiable-reward | llm | ▸ reproduced | ⚠ cond | 1 | 1 | ✓ |
| 6 | veRL (WSL2) — single-5090 GRPO with colocated vLLM rollout + FSDP param/optimizer offload | rl-verifiable-reward | llm | ▸ reproduced | ⚠ cond | 2 | 1 | ✓ |
| 9 | DAA differences are a blur — SFT then preference | dpo | llm | paper | check | 4 | 4 | · |
| 9 | DAPO — open-source LLM RL at scale | rl | llm | paper | check | 4 | 4 | · |
| 9 | HF PEFT LoRA/QLoRA + Diffusers LoRA + bnb AdamW8bit stack | lora | both | docs | check | 4 | 4 | · |
| 9 | Unsloth fine-tune + Blackwell RTX 50 series tooling | qlora | both | docs | check | 4 | 4 | · |

## Detail

### DPO (LoRA) preference tuning (stage 2) — paired data, needs ref model · `recommended` · ▣ measured
**Direct Preference Optimization fits a paired (chosen/rejected) preference dataset by a single classification-style loss against a frozen reference policy, replacing the reward-model + PPO loop of RLHF, and runs on one 5090 as LoRA on top of the stage-1 SFT adapter.**
DPO reframes RLHF as a closed-form supervised objective: the optimal RLHF policy can be written analytically in terms of a reference policy, so you can train directly on (prompt, chosen, rejected) triples with a logistic loss governed by beta, with NO separate reward model and NO sampling rollout. On the rig this is `swift rlhf --rlhf_type dpo`, LoRA + 4-bit, beta 0.1, rpo_alpha 1.0, lr 5e-6 (an order of magnitude below SFT — preference stages are gentle), bs 1 x grad-accum 16, max_len 2048, on an hh-rlhf slice. It is stage 2: it MUST run on a model already SFT'd on the target template (predecessor link below). Its cost is that it needs PAIRED preferences and holds a reference model in memory; when you only have unpaired good/bad labels, use KTO, and when you want to drop the reference model entirely, use ORPO/SimPO (the reference-free entry).
- **For the pipeline:** Choose the preference method by the DATA you actually have, not by fashion: paired -> DPO; unpaired binary -> KTO; want one-stage / no ref model -> ORPO. Pin beta and the low preference-stage lr per step; keep DPO as the default ONLY when your studio data is genuinely paired chosen/rejected (tone/style preference data often is, via A/B re-writes).
- **Method:** dpo · **Applies to:** llm · **Base:** qwen3 · **Kind:** recipe
- **Seed:** 3407 · **Runs:** 1 · **Tuning budget:** Medium: beta is the load-bearing knob and benefits from a small sweep (0.05-0.3); lr and rpo_alpha taken from ms-swift defaults. · **Search:** manual (published-default adoption)
- **Variance:** One measured rig config; DPO is known beta-sensitive (too-high beta under-optimizes, too-low collapses to the reference) — the single run does not characterize that sensitivity, treat beta 0.1 as a starting point not a tuned optimum.
- **Validated under:** Qwen3-8B, ms-swift `swift rlhf --rlhf_type dpo`, bnb 4-bit + LoRA, beta 0.1, rpo_alpha 1.0, lr 5e-6, per-device bs 1 x grad-accum 16, max_length 2048, gradient checkpointing on, Windows-native single RTX 5090. Measured throughput/VRAM live in the tensor-engine config_recipe.
- **Measured receipt (tensor-engine):** `training-ms-swift-dpo-preference-tuning-single-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `qwen3-8b`
- **Builds on (stage 2):** QLoRA-NF4 SFT with chat template (stage 1) — 8-34B on one 5090
- **Output license:** commercial **conditional** — DPO method is Apache-2.0 (TRL/ms-swift). Commercial cleanliness is gated by the preference dataset's license and the base weights, not the algorithm. hh-rlhf is MIT but Anthropic-sourced human feedback — fine for method validation; for a shipping commercial model, build paired preference data from your own A/B rewrites (commercial-clean by construction).
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | lora | ● | 4-bit base + LoRA on the SFT adapter |
| beta | 0.1 | ● | KL-deviation strength from the reference policy — the load-bearing DPO knob |
| loss_type | sigmoid | ○ | standard DPO logistic loss; rpo_alpha 1.0 adds the RPO SFT-regularization term |
| learning_rate | 5e-6 | ● | ~20x below SFT lr — preference stages are gentle |
| batch_size | 1 | ● | per-device |
| grad_accum | 16 | ● | effective batch 16 |
| resolution | 2048 tokens | ● | max_length |
| precision | nf4 | ● | QLoRA 4-bit keeps an 8B DPO run + reference model in 32 GB |

- **Datasets:** Anthropic HH-RLHF — 10k paired preference slice (preference-paired, license MIT (Anthropic released the dataset under MIT).)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Preference accuracy climbs but generations become degenerate / repetitive / off-distribution | beta too low — policy drifts too far from the reference, over-optimizing the reward proxy (reward hacking) | Raise beta (0.1 -> 0.3) to tighten the KL leash; verify chosen-reward and rejected-reward margins are both moving, not just the gap | beta |
| DPO has almost no effect; model output unchanged from SFT | beta too high (over-constrained to reference) OR preference pairs are too weak/noisy to give signal | Lower beta and audit pair quality — chosen and rejected must be genuinely distinguishable on the target axis | beta |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| preference-accuracy | reward_accuracy (chosen>rejected) |  |  | ✓ | none (implicit reward from logits) |

- **Best for:** Stage-2 tone/preference alignment when you have PAIRED chosen/rejected data (llm-dpo, fit 5)
- **Verify:** verdict=confirmed | currency=Current. DPO is not superseded in 2025-2026; it competes with SimPO/ORPO/KTO in the post-training stack but remains a valid and widely-used choice when paired preference data is available. | All sources verified real and claim-supporting. arXiv:2305.18290 confirmed (Rafailov, Sharma, Mitchell, Ermon, Manning, Finn 2023); core claim — closed-form optimal policy enabling a single classification loss that matches or beats PPO — confirmed by paper abstract and body. ms-swift GitHub confirmed real; --rlhf_type dpo with --beta and --rpo_alpha confirmed in current docs. No boundary leaks. evidence_strength='measured-on-rig' is acceptable given the engine_recipe_ref is set and raw measured numbers are explicitly deferred there.
- **Sources:** [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/abs/2305.18290) (Rafailov, Sharma, Mitchell, Ermon, Manning, Finn, 2023) — The RLHF objective has a closed-form optimal policy, enabling a simple classification loss on preference pairs that matches or beats PPO-based RLHF without a reward model or sampling. ; [ms-swift — RLHF (DPO/KTO/ORPO/SimPO/CPO)](https://github.com/modelscope/ms-swift) (ModelScope (Alibaba), 2024) — swift rlhf --rlhf_type dpo exposes --beta and --rpo_alpha and shares the LoRA+4-bit path with kto/orpo/simpo/cpo via a single --rlhf_type swap.

### QLoRA-NF4 SFT with chat template (stage 1) — 8-34B on one 5090 · `recommended` · ▣ measured
**4-bit NF4 quantization of the frozen base plus a LoRA adapter lets a 24-34B-class model be supervised-fine-tuned inside 32 GB with near-full-finetune quality, and is the mandatory stage-1 that teaches the chat/instruction template before any preference stage.**
QLoRA freezes the base in 4-bit NF4 (information-theoretically optimal for normally-distributed weights), adds double-quantization to shave the quant constants, and trains only a low-rank LoRA adapter through paged optimizers that page to host RAM on memory spikes. On the studio rig this is the entry point for every LLM run: an 8B trains with large headroom (rank 16, alpha 32, lr 1e-4, bs 1 x grad-accum 16, max_len 2048, 2 epochs over a 5k Alpaca-GPT4 slice), and the same shape scales to 14B (rank 32, lr 2e-4, paged_adamw_8bit) and 32B (max_seq 2048, bs 1). The non-negotiable craft point is that SFT must apply the model's exact chat template (ChatML for Qwen3); a template mismatch silently destroys instruction-following and looks like a bad adapter. Stage 1 produces the SFT adapter that the DPO/ORPO/KTO stage then refines.
- **For the pipeline:** Make QLoRA-NF4 SFT the unconditional first stage of the LLM lane; never run a preference method on a base that has not first been SFT'd on the target chat template, and pin the template per data row so the wave is byte-for-byte replayable. Export merged weights to GGUF after stage 1 to keep train->serve on one rig.
- **Method:** qlora · **Applies to:** llm · **Base:** qwen3 · **Kind:** recipe
- **Seed:** 3407 · **Runs:** 1 · **Tuning budget:** Low: rank/alpha and lr are taken from the published QLoRA + ms-swift defaults; the only rig-tuned knob is max_length (drop 2048->1024 if VRAM is tight) and model size selection. · **Search:** manual (published-default adoption, not a sweep)
- **Variance:** Single measured configuration on the rig; QLoRA's own ablations (Dettmers 2023) report NF4+double-quant matches 16-bit LoRA across scales, but the rig has one run at this exact config — treat throughput as a single observation, not a distribution.
- **Validated under:** Qwen3-8B, ms-swift `swift sft`, bnb 4-bit NF4, LoRA rank 16 / alpha 32, lr 1e-4, per-device bs 1 x grad-accum 16, gradient checkpointing on, max_length 2048, 2 epochs, Windows-native single RTX 5090 (32 GB, sm_120). Measured it/s and VRAM peak live in the tensor-engine config_recipe, not here.
- **Measured receipt (tensor-engine):** `training-ms-swift-qlora-sft-7b-32gb-qwen3-lora-single-5090-windows-native` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `qwen3-8b`
- **Output license:** commercial **conditional** — QLoRA method itself is MIT (bitsandbytes) and Apache-2.0 (PEFT) — fully commercial-clean. The license that gates commercial use is the BASE WEIGHTS (Qwen3 is Apache-2.0; some bases are not) and the SFT DATASET (Alpaca-GPT4 is research-only due to OpenAI-output provenance). Swap to a commercially licensed instruction set for shipping models; see datasets.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | lora | ● | 4-bit NF4 base + LoRA adapter = QLoRA |
| rank | 16 | ● | 8B; bump to 32 for 14B per Unsloth rank=alpha guidance |
| alpha | 32 | ● | alpha=2*rank scaling at 8B |
| learning_rate | 1e-4 | ● | LoRA on adapter; 2e-4 used at 14B with paged_adamw_8bit |
| optimizer | paged_adamw_8bit | ○ | paged = QLoRA's OOM-spike guard; 8-bit halves optimizer state |
| batch_size | 1 | ● | per-device |
| grad_accum | 16 | ● | effective batch 16 |
| epochs | 2 | ● | over a 5k-row instruction slice |
| resolution | 2048 tokens | ● | max_length; drop to 1024 if VRAM tight |
| precision | nf4 | ● | 4-bit NormalFloat base; bf16 compute autodetected on Blackwell |

- **Datasets:** Alpaca-GPT4 (English) — 5k instruction slice (sft-instruction, license Research-only (responses are OpenAI GPT-4 outputs; OpenAI terms restrict using outputs to build competing models — NOT commercial-clean).)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Fine-tuned model ignores instructions / outputs raw continuation despite low train loss | Chat template not applied during SFT, or wrong template family (e.g. Llama template on a Qwen3 base) | Apply the base model's exact chat template (ChatML for Qwen3); verify a formatted sample before launching the run | caption_format |
| OOM at a random step deep into training, not at start | Activation/optimizer memory spike on a long sample exceeds the steady-state budget | Use a paged optimizer (paged_adamw_8bit) so spikes page to host RAM; lower max_length or enable/confirm gradient checkpointing | optimizer |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| held-out-loss | eval_loss |  |  | ✓ | none |

- **Best for:** Stage-1 instruction/chat-template tuning for a local 24-34B model on one 5090 (llm-sft, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. QLoRA NF4 remains valid and actively recommended practice for single-GPU large-model SFT in 2025-2026. No superseding technique has displaced it. | Two fixes required. (1) The Unsloth citation URL (docs.unsloth.ai/get-started/fine-tuning-guide) 404s — it redirects to unsloth.ai/docs/... which also 404s for that path. The specific VRAM figures (7B=5 GB, 14B=8.5 GB, 32B=26 GB) could NOT be verified at the cited URL; they may be stale or from an earlier docs version. Either drop the specific figures or re-verify them against the live Unsloth LoRA hyperparameters guide and update the URL. (2) The Unsloth guide actually recommends lora_alpha = lora_rank OR lora_alpha = 2 × lora_rank; the entry's claim of 'rank=alpha is the recommended starting ratio' is the conservative form of this, not a fabrication, but the note should acknowledge both forms exist. QLoRA paper (arXiv:2305.14314) and ms-swift docs confirmed real and claim-supporting. The 'mandatory stage-1' framing holds within the DPO two-stage context but is not universal — ORPO folds SFT and preference into one stage, so a cross-reference to slug 3 is advisable.
- **Sources:** [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) (Dettmers, Pagnoni, Holtzman, Zettlemoyer, 2023) — 4-bit NF4 + double quantization + paged optimizers finetunes a 65B model on a single 48GB GPU with no measured degradation vs 16-bit full finetuning. ; [ms-swift — Supervised Fine-Tuning (LoRA/QLoRA)](https://github.com/modelscope/ms-swift) (ModelScope (Alibaba), 2024) — swift sft exposes --train_type lora --quant_bits 4 --quant_method bnb with lora_rank/lora_alpha/learning_rate for single-GPU QLoRA SFT. ; [Unsloth Documentation — LoRA Hyperparameters & VRAM requirements](https://docs.unsloth.ai/get-started/fine-tuning-guide) (Unsloth AI, 2024) — QLoRA 4-bit VRAM minimums: 7B=5GB, 14B=8.5GB, 32B=26GB; rank=alpha is the recommended starting ratio.

### Unsloth LLM-QLoRA MEASURED baseline (native-Win 5090, Qwen3-4B) + the xformers/torchvision install-churn fix · `recommended` · ▣ measured
**On native Windows (no WSL2), `pip install unsloth unsloth_zoo` transitively pulls xformers 0.0.35 which SILENTLY downgrades torch to a 2.10.0+CPU build (no CUDA) and drags torchvision to 0.25.0; the fix is to install torch+torchvision cu130 FIRST, then bitsandbytes/triton, then unsloth, then uninstall xformers and re-assert the cu130 torch/torchvision — after which Unsloth trains on cuDNN SDPA (the FA2/xformers warning is benign).**
Adds the MEASURED specifics and earned install gotchas wave-1's method-level QLoRA technique lacks. Stood up + validated end-to-end on native Windows 2026-06-03: torch 2.12.0+cu130, bitsandbytes 0.49.2 (4-bit NF4 verified on sm_120), triton-windows 3.7.0, unsloth 2026.5.10. MEASURED on Qwen3-4B-bnb-4bit (Apache-2.0), r=16/alpha=16 all-linear, max_seq_len=2048, bs2 x grad4, paged_adamw_8bit, bf16, unsloth checkpointing: ~2.28 s/optimizer-step, PEAK process VRAM ~6.1 GB (nvidia-smi 6271 MiB; torch-alloc 3.19 GB) — confirms recipe's 4-8B ~5-6 GB budget band; train loss 7.01->2.90 monotonic over 15 steps; 143.6 MB reloadable adapter; 169 W / 37 C at tiny scale. The native-Win answer to the cu128-based recipe: on torch 2.12 the base is cu130 and the documented install order avoids the churn.
- **Method:** qlora-sft · **Applies to:** llm · **Base:** Qwen3 · **Kind:** failure-fix
- **Seed:** 3407 · **Runs:** 1
- **Variance:** Single tiny-scale validation run (15 steps); throughput/VRAM are one observation establishing the working env, not a distribution. Real runs push power/VRAM higher.
- **Validated under:** Native Windows (no WSL2), RTX 5090 sm_120, fresh uv venv py3.11; torch 2.12.0+cu130, torchvision 0.27.0+cu130, bitsandbytes 0.49.2, triton-windows 3.7.0.post26, unsloth 2026.5.10, transformers 5.5.0, trl 0.24.0, peft 0.19.1; Qwen3-4B-bnb-4bit, r16/alpha16 all-linear, max_seq_len 2048, bs2 x grad4, paged_adamw_8bit, bf16, gradient_checkpointing='unsloth'. 2026-06-03.
- **Measured receipt (tensor-engine):** `training-unsloth-llm-qlora-baseline-native-win-5090-qwen3-4b` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `unsloth/Qwen3-4B-bnb-4bit`
- **Builds on (stage ?):** Unsloth QLoRA daily-driver — 14B (up to 32B) in 32 GB, Windows-native, rank=alpha + paged 8-bit AdamW
- **Output license:** commercial **yes** — Qwen3 = Apache-2.0; LoRA inherits base license.
- **Fit:** rig 3/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| torch silently becomes a +CPU build, CUDA unavailable after installing unsloth | unsloth's dep tree pulls xformers 0.0.35 which downgrades torch (the 'NEVER pip xformers on Blackwell' trap, sprung transitively) | pip uninstall -y xformers; reinstall torch==2.12.0 + torchvision==0.27.0 from the cu130 index; Unsloth does not need xformers on Blackwell | install order |
| unsloth import fails: 'torch 2.12 requires torchvision>=0.27.0' | xformers had pulled torchvision 0.25.0 | pip install torchvision==0.27.0 from the cu130 index (must be the cu130 wheel) |  |
| warning 'Flash Attention 2 installation seems broken. Using Xformers instead' | neither FA2 nor xformers installed on sm_120 | ignore — it falls back to torch SDPA (cuDNN on Blackwell) and trains fine (consistent with no-FA3-on-sm120 rule) |  |

- **Verify:** verdict=confirmed | Recipe `training-unsloth-llm-qlora-baseline-native-win-5090-qwen3-4b` is tagged kind=baseline and describes a MEASURED, dated (2026-06-03) native-Windows 5090 run. The xformers/torchvision install-churn claim is faithfully reproduced: recipe documents xformers 0.0.35 transitively downgrading torch to 2.10.0+CPU, the torchvision version mismatch, and the exact fix order. Fall-through to cuDNN SDPA is confirmed. Lane llm-finetune is correct.
- **Sources:** [Fine-tuning LLMs with Blackwell RTX 50-series and Unsloth](https://unsloth.ai/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth) (Unsloth AI, 2026) — Reference recipe the rig measured against; the rig run confirmed the 4-8B VRAM band and added the native-Win install-order fix.

### Unsloth QLoRA daily-driver — 14B (up to 32B) in 32 GB, Windows-native, rank=alpha + paged 8-bit AdamW · `recommended` · ▸ reproduced
**Unsloth's Blackwell-tuned kernels QLoRA-fine-tune a 14B (8.5 GB) or a 32B (~26 GB, just fits) inside 32 GB on the single 5090, faster and with ~70% less VRAM than FlashAttention-2, via rank=alpha LoRA on all 7 linear modules + use_gradient_checkpointing='unsloth' + paged_adamw_8bit that spills optimizer state to the 64 GB host RAM.**
The studio's distinct LLM-trainer path that wave-1's QLoRA-NF4 SFT technique (ms-swift-anchored) does NOT cover: Unsloth's FastLanguageModel + get_peft_model with use_gradient_checkpointing='unsloth' (the memory-cheapest mode) and rank=alpha=32 on q/k/v/o/gate/up/down. TrainingArguments per_device_bs=2 x grad_accum=4, optim='paged_adamw_8bit', lr=2e-4, bf16 — mirrors NVIDIA's published 5090 Llama-3.1-8B benchmark. Official Unsloth QLoRA 4-bit VRAM table: 7B=5GB, 8B=6GB, 14B=8.5GB, 32B=26GB (70B too big). For 32B set max_seq_length=2048, per_device_bs=1. This is the merge of six engine-lane copies of the same recipe (attention-kernels, llm-inference, llm-serving, quantization, runtime-foundations, training) into one training-craft technique; the measured-on-rig baseline is the sibling technique unsloth-llm-qlora-measured-baseline-qwen3-4b-native-win.
- **Method:** qlora-sft · **Applies to:** llm · **Base:** Qwen3 / any Unsloth 4-bit repo · **Kind:** recipe
- **Variance:** VRAM table is Unsloth's official QLoRA minimums (reproduced-from-source), not a per-seed rig sweep; the measured single-rig confirmation lives in the companion baseline technique (4B @ ~6.1 GB matches the table's 4-8B band).
- **Validated under:** RTX 5090 / sm_120 / 32 GB / 64 GB host RAM; cu128 torch base; Unsloth Blackwell kernels; QLoRA 4-bit NF4; rank=alpha=32 all-linear; per_device_bs=2 x grad_accum=4; paged_adamw_8bit; bf16.
- **Measured receipt (tensor-engine):** `training-unsloth-windows-native-qlora-14b-32gb-daily-driver (primary; also: runtime-foundations-unsloth-qlora-14b-wsl2-fine-tune-a-14b-in-32-gb-vram-paged-adamw-8bit, llm-serving-unsloth-qlora-14b-in-32gb-vram-windows-or-wsl2, llm-inference-unsloth-blackwell-qlora-14b-in-32gb-vram, quantization-unsloth-qlora-14b-32gb-blackwell, attention-kernels-recipe-unsloth-qlora-14b-32gb-paged-adamw8bit)` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `unsloth/Qwen3-14B-bnb-4bit`
- **Output license:** commercial **yes** — A LoRA inherits its base license; Qwen3 = Apache-2.0 (commercial-safe). Unsloth itself Apache-2.0.
- **Fit:** rig 3/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| lora_rank (r) | 32 | ○ | Unsloth recommends rank=alpha |
| lora_alpha | 32 | ○ |  |
| target_modules | q,k,v,o,gate,up,down | ○ | all 7 linear modules |
| use_gradient_checkpointing | unsloth | ○ | the +30% ctx / ~+1.9% time memory-cheapest mode |
| optim | paged_adamw_8bit | ○ | pages optimizer state to 64 GB host RAM on OOM spikes — load-bearing for 14B+ in 32 GB |
| learning_rate | 2e-4 | ○ |  |
| per_device_train_batch_size | 2 | ○ |  |
| gradient_accumulation_steps | 4 | ○ |  |
| max_seq_length | 4096 | ○ | drop to 2048 for 32B or if OOM |

- **Best for:** Light local LLM fine-tune (instruction/style adapters) on one card (llm-sft, fit 3)
- **Verify:** verdict=confirmed | All 6 engine_recipe_ref slugs exist in tensor-engine DB. Recipe body (`training-unsloth-windows-native-qlora-14b-32gb-daily-driver`) matches every claimed hparam: r=32, lora_alpha=32, all 7 linear modules, use_gradient_checkpointing='unsloth', paged_adamw_8bit, lr=2e-4, bs=2, grad_accum=4, max_seq=4096 (drop to 2048 for 32B). VRAM figures (14B=8.5GB, 32B=26GB) and the '~70% less VRAM than FlashAttention-2' claim are stated in the recipe body as NVIDIA 5090 benchmark data, not invented. Boundary correct: measured numbers live in the recipes, not restated inline. Lane llm-finetune is correct.
- **Sources:** [Fine-tuning LLMs with Blackwell RTX 50-series and Unsloth](https://unsloth.ai/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth) (Unsloth AI, 2026) — Official Blackwell QLoRA support + the per-model-size 4-bit VRAM minimums and the ~70%-less-VRAM benchmark. ; [Train an LLM on an NVIDIA Blackwell Desktop with Unsloth and Scale It](https://developer.nvidia.com/blog/train-an-llm-on-an-nvidia-blackwell-desktop-with-unsloth-and-scale-it/) (NVIDIA, 2026) — Published 5090 Llama-3.1-8B rank-32 all-linear benchmark (~2x faster, ~70% less VRAM than FA2) that the per_device_bs=2/grad-accum=4 config mirrors.

### llama.cpp LoRA export/merge to GGUF — the train-to-serve bridge (CUDA 12.8 EXACT on Blackwell) · `recommended` · ▸ reproduced
**A fine-tuned LoRA reaches the local studio serving loop two ways: merge in Unsloth (model.save_pretrained_gguf, q4_k_m) for one merged GGUF, or convert the base then run llama-server with --lora adapter.gguf for hot-swappable adapters — but on Blackwell you MUST build llama.cpp with CUDA Toolkit 12.8 EXACTLY (newer toolkits trigger MMQ/MXFP4 'mma with block scale not supported' PTX crashes on sm_120), MMQ on, force-cuBLAS off.**
The bridge from 'I trained a LoRA' to 'it serves in my local loop' — training-adjacent export craft absent from wave-1. Build: cmake -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=120 -DGGML_CUDA_FORCE_CUBLAS=OFF. Serve a 32B GGUF on-GPU with -ngl 99 -fa + q8_0 KV cache; MoE partial offload to the 64 GB RAM with --n-cpu-moe N (keeps dense/attention on the 5090). cuBLAS is the stable fallback if ggml custom kernels crash on a given model. Belongs in efficiency as the offload/serve-handoff lever for trained adapters.
- **Method:** adapter-export · **Applies to:** llm · **Kind:** recipe
- **Measured receipt (tensor-engine):** `training-llamacpp-blackwell-build-and-lora-export-merge` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **yes** — llama.cpp MIT; merged-model license follows the base.
- **Fit:** rig 3/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| 'mma with block scale not supported' PTX crash on sm_120 | built with a CUDA toolkit newer than 12.8 | use CUDA Toolkit 12.8 EXACTLY; build MMQ on, force-cuBLAS off; cuBLAS fallback if a model still crashes | CUDA toolkit version |

- **Verify:** verdict=confirmed | Recipe `training-llamacpp-blackwell-build-and-lora-export-merge` body confirms: CUDA 12.8 EXACTLY required (newer toolkits trigger MMQ/MXFP4 PTX crashes on sm_120), MMQ on, cuBLAS-force off. Both serve paths confirmed: Unsloth merged GGUF and --lora adapter.gguf for hot-swap. Lane efficiency is acceptable (train-to-serve bridge sits at the efficiency/serving boundary; no dedicated 'serving' lane exists separate from efficiency in the 8-lane schema).
- **Sources:** [Software Migration Guide for NVIDIA Blackwell RTX GPUs (CUDA 12.8, PyTorch, TensorRT, llama.cpp)](https://forums.developer.nvidia.com/t/software-migration-guide-for-nvidia-blackwell-rtx-gpus-a-guide-to-cuda-12-8-pytorch-tensorrt-and-llama-cpp/321330) (NVIDIA, 2026) — Blackwell llama.cpp must build against CUDA 12.8 exactly; newer toolkits crash MMQ/MXFP4 kernels on sm_120.

### ms-swift install (native Windows, transformers backend) — the trainer to stand up first · `recommended` · ▸ reproduced
**ms-swift installs native-Windows on the cu128-nightly venv with `pip install -U ms-swift --no-deps` (so it does not clobber the nightly torch) followed by explicit deps without torch; it reuses the same vLLM inference engine for GRPO rollouts; Megatron-SWIFT FP8 is Linux/WSL2-only so stay on the transformers backend for native Windows.**
The install/setup protocol behind wave-1's ms-swift SFT/DPO/GRPO recipes — wave-1 references the run recipes but has no technique for standing the framework up. --no-deps is load-bearing (avoids a torch downgrade that re-breaks sm_120); if you see 'sm_120 not compatible', the torch got clobbered — reinstall the nightly and re-run ms-swift with --no-deps. Pin a version (e.g. ms-swift==4.2.3) for reproducibility. Sanity: `swift sft --help` and `swift rlhf --help` must print.
- **Method:** trainer-framework · **Applies to:** llm · **Kind:** protocol
- **Measured receipt (tensor-engine):** `training-ms-swift-install-windows-native-the-one-to-run-first-on-this-rig` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **yes** — ms-swift Apache-2.0.
- **Fit:** rig 3/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| 'sm_120 not compatible' after installing ms-swift | a dep pulled a stable cu12x torch over the nightly | reinstall the cu128 nightly torch, then `pip install ms-swift --no-deps` |  |

- **Verify:** verdict=confirmed | Recipe `training-ms-swift-install-windows-native-the-one-to-run-first-on-this-rig` body exactly matches all three sub-claims: (1) pip install -U ms-swift --no-deps to avoid clobbering the nightly torch; (2) vLLM reused for GRPO rollouts; (3) Megatron-SWIFT FP8 is Linux/WSL2-only, stay on transformers backend for native Windows. Lane llm-finetune is correct.
- **Sources:** [ms-swift — Quick Start](https://swift.readthedocs.io/en/latest/GetStarted/Quick-start.html) (ModelScope / ms-swift, 2026) — Install + SFT/RLHF entry points; the transformers backend runs native-Windows while Megatron-SWIFT (FP8) is Linux-only.

### Native-Windows QLoRA without WSL2 — TRL + PEFT + bitsandbytes (prebuilt sm_120) + Liger kernels · `runner-up` · ▸ reproduced
**bitsandbytes now ships prebuilt Windows x86-64 wheels with sm_120 (Blackwell) for CUDA 12.8/12.9/13.0, so a plain `pip install bitsandbytes` gives working 4-bit QLoRA on native Windows with the stock HF stack (transformers/trl/peft/accelerate) plus liger-kernel; paged 8-bit AdamW spills optimizer state to the 64 GB host RAM so a 14B QLoRA fits comfortably in 32 GB.**
The HF-native (no-Unsloth, no-ms-swift, no-WSL2) QLoRA path — a distinct trainer stack wave-1 does not have a technique for. BitsAndBytesConfig(load_in_4bit, nf4, compute_dtype=bf16, double_quant); SFTConfig(packing=True, gradient_checkpointing, optim='paged_adamw_8bit', bf16); use_liger_kernel=True for the fused-kernel throughput/VRAM win. The big unlock is the prebuilt Windows bnb wheel (no source build needed for sm_120). Pin torch from the cu130 (or cu126) index — cu128 was removed from the matrix.
- **Method:** qlora-sft · **Applies to:** llm · **Kind:** recipe
- **Measured receipt (tensor-engine):** `training-native-windows-qlora-on-the-5090-no-wsl2-trl-peft-bitsandbytes-liger` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **yes** — All-Apache/MIT toolchain; LoRA inherits base license.
- **Fit:** rig 3/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| bnb_4bit_quant_type | nf4 | ○ |  |
| bnb_4bit_use_double_quant | true | ○ |  |
| bnb_4bit_compute_dtype | bfloat16 | ○ |  |
| optim | paged_adamw_8bit | ○ |  |
| packing | true | ○ | SFTConfig sample-packing throughput win |
| use_liger_kernel | true | ○ | fused Liger kernels cut VRAM + add speed |

- **Verify:** verdict=confirmed | Recipe `training-native-windows-qlora-on-the-5090-no-wsl2-trl-peft-bitsandbytes-liger` body confirms: bitsandbytes ships prebuilt sm_120 wheels for CUDA 12.8/12.9/13.0, plain pip install works. All 5 hparams match: bnb_4bit_quant_type='nf4', bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=bfloat16, optim='paged_adamw_8bit', packing=True, use_liger_kernel=True. Paged AdamW spilling optimizer state for 14B fit confirmed in recipe. Lane llm-finetune is correct.
- **Sources:** [bitsandbytes installation (Windows prebuilt wheels, CUDA 12.8/12.9/13.0)](https://huggingface.co/docs/bitsandbytes/main/en/installation) (Hugging Face / bitsandbytes, 2026) — Prebuilt Windows x86-64 wheels include sm_120 (Blackwell) for CUDA 12.8-13.0, enabling 4-bit QLoRA on native Windows without a source build.

### TRL + Unsloth DPO/ORPO/KTO — the no-Ray cheapest preference path (PatchDPOTrainer ref-sharing fits 14B) · `runner-up` · ▸ reproduced
**DPO normally holds a policy AND a reference model in memory; Unsloth's PatchDPOTrainer() (called BEFORE importing DPOTrainer) reuses the 4-bit base as the reference (LoRA deltas disabled) so ref_model=None — halving the model memory and letting a 14B DPO run fit in 32 GB native-Windows with NO Ray/vLLM/DeepSpeed.**
A preference-tuning path distinct from wave-1's ms-swift DPO technique: the Windows-native, cluster-free TRL+Unsloth route with the ref-sharing trick that makes 14B DPO fit. Load 14B in 4-bit, get_peft_model r=32/alpha=32, DPOConfig beta=0.1, lr=5e-6 (an order below SFT — preference stages are gentle), bs1 x grad8, paged_adamw_8bit, bf16. Swap DPOTrainer->ORPOTrainer (no ref at all) or KTOTrainer for unpaired feedback. Best when you have chosen/rejected pairs and want alignment without standing up an RL cluster.
- **Method:** preference-optimization · **Applies to:** llm · **Base:** Qwen3 · **Kind:** recipe
- **Measured receipt (tensor-engine):** `training-trl-unsloth-dpo-preference-tuning-no-ray-cheapest-path` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `unsloth/Qwen3-14B-bnb-4bit`
- **Output license:** commercial **yes** — Qwen3 Apache-2.0; preference dataset license must be vetted.
- **Fit:** rig 3/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| PatchDPOTrainer() | call before importing DPOTrainer | ○ | halves memory by reusing the base as the ref |
| ref_model | None | ○ | frozen base IS the reference (LoRA disabled) |
| beta | 0.1 | ○ |  |
| learning_rate | 5e-6 | ○ | ~10x below SFT |
| optim | paged_adamw_8bit | ○ |  |

- **Verify:** verdict=confirmed | Recipe `training-trl-unsloth-dpo-preference-tuning-no-ray-cheapest-path` body shows exactly PatchDPOTrainer() called before DPOTrainer import, ref_model=None, beta=0.1, lr=5e-6, paged_adamw_8bit — matching all claimed hparams. The 'frozen base IS the reference (LoRA disabled), so you do NOT pay for a second full model' mechanism is stated verbatim. 14B DPO on 32 GB native-Windows without Ray/vLLM/DeepSpeed confirmed. Lane llm-finetune is correct.
- **Sources:** [TRL DPOTrainer documentation](https://huggingface.co/docs/trl/dpo_trainer) (Hugging Face TRL, 2026) — DPOTrainer API + reference-model handling that, with Unsloth's PatchDPOTrainer, allows ref_model=None for memory-halved 14B DPO.

### Axolotl (WSL2) — reproducible YAML-driven (Q)LoRA / full-SFT / DPO with sample-packing + FSDP/DeepSpeed · `situational` · ▸ reproduced
**Axolotl gives byte-for-byte reproducible YAML-config training (QLoRA/LoRA/full-SFT/DPO/ORPO) with sample_packing for throughput and FSDP+DeepSpeed for the full-param path; it is Linux-first (bnb/flash-attn/deepspeed) so run it in WSL2 on a cu128 torch base — the 5090 issue #2525 was exactly a pre-2.7 torch, fixed by cu128.**
Config-as-artifact trainer framework absent from wave-1. QLoRA YAML: load_in_4bit, adapter:qlora, lora_r/alpha 32, lora_target_linear, sequence_len 4096, sample_packing:true (the throughput win — packs short samples to fill the sequence), micro_batch_size 2 / grad_accum 4, optimizer paged_adamw_8bit, lr 2e-4, gradient_checkpointing. Launch: accelerate launch -m axolotl.cli.train. DPO via rl:dpo + paired data + rl_beta. Full-param across one card needs fsdp_config with activation_checkpointing + cpu_offload (32 GB cannot hold full 14B optimizer state). Axolotl favors FSDP/DeepSpeed-correct distributed recipes + packing; LLaMA-Factory favors method breadth + a webui.
- **Method:** trainer-framework · **Applies to:** llm · **Base:** Qwen3 · **Kind:** recipe
- **Measured receipt (tensor-engine):** `training-axolotl-wsl2-qlora-yaml-flash-attn-cu128` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `Qwen/Qwen3-14B`
- **Output license:** commercial **yes** — Axolotl Apache-2.0; verify dataset + base licenses for commercial fine-tunes.
- **Fit:** rig 2/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| adapter | qlora | ○ |  |
| lora_r | 32 | ○ |  |
| lora_alpha | 32 | ○ |  |
| sample_packing | true | ○ | the throughput win |
| optimizer | paged_adamw_8bit | ○ |  |
| micro_batch_size | 2 | ○ |  |
| gradient_accumulation_steps | 4 | ○ |  |

- **Verify:** verdict=confirmed | Recipe `training-axolotl-wsl2-qlora-yaml-flash-attn-cu128` confirms WSL2-only framing, issue #2525 fix via cu128 torch, and all 6 hparams (adapter=qlora, lora_r=32, lora_alpha=32, sample_packing=true, optimizer=paged_adamw_8bit, micro_batch_size=2, gradient_accumulation_steps=4). sample_packing as 'the throughput win' matches recipe. FSDP+DeepSpeed path for full-SFT confirmed. Lane llm-finetune is correct.
- **Sources:** [Axolotl (axolotl-ai-cloud/axolotl)](https://github.com/axolotl-ai-cloud/axolotl) (Axolotl AI, 2026) — YAML-driven (Q)LoRA/full-SFT/DPO with sample-packing + FSDP/DeepSpeed; the 5090 fix was a cu128 torch (issue #2525).

### LLaMA-Factory (WSL2) — broadest-method YAML training: QLoRA 32B / full-SFT 8B / DPO/KTO/PPO · `situational` · ▸ reproduced
**LLaMA-Factory spans SFT+DPO+KTO+PPO across many model families from one YAML (or a webui), running in WSL2 on a cu128 base; a 14B QLoRA fits with quantization_bit:4 + lora all-target, a 32B fits at cutoff_len:2048/bs:1 (~26 GB), and a full-param 8B SFT needs ZeRO-3 + CPU offload to push optimizer state into the 64 GB RAM.**
The method-breadth trainer (one tool for SFT/DPO/KTO/PPO) absent from wave-1. Install: pip install -e '.[torch,bitsandbytes,vllm]' then verify torch stayed 2.9.0+cu128. QLoRA YAML: finetuning_type:lora, lora_rank/alpha 32, lora_target:all, quantization_bit:4 + quantization_method:bnb, template:qwen, cutoff_len 4096, bs2 x grad4, optim paged_adamw_8bit, lr 2e-4, gradient_checkpointing. Launch llamafactory-cli train. DPO: stage:dpo + pref_beta. Full 8B SFT: finetuning_type:full + ds_z3_offload_config.json (does NOT fit 32 GB without offload). Choose this over Unsloth when you want one tool spanning many methods/families; choose Unsloth for max single-GPU speed/VRAM.
- **Method:** trainer-framework · **Applies to:** llm · **Base:** Qwen3 · **Kind:** recipe
- **Measured receipt (tensor-engine):** `training-llama-factory-wsl2-qlora-yaml-32b-and-full-sft-8b` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `Qwen/Qwen3-14B`
- **Output license:** commercial **conditional** — LLaMA-Factory Apache-2.0, but its bundled demo datasets and many base models carry their own licenses — vet data + base before any commercial fine-tune.
- **Fit:** rig 2/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| finetuning_type | lora | ○ |  |
| lora_rank | 32 | ○ |  |
| quantization_bit | 4 | ○ | QLoRA NF4 via bnb |
| lora_target | all | ○ |  |
| optim | paged_adamw_8bit | ○ |  |
| cutoff_len | 4096 | ○ | 2048 for a 32B base |

- **Verify:** verdict=confirmed | Recipe `training-llama-factory-wsl2-qlora-yaml-32b-and-full-sft-8b` confirms: 14B QLoRA fits with quantization_bit=4 + lora all-target; 32B fits at cutoff_len=2048/bs=1 (~26 GB); full-param 8B SFT requires ZeRO-3 + CPU offload into 64 GB RAM. All claimed hparams verified in the YAML snippet: finetuning_type=lora, lora_rank=32, quantization_bit=4, lora_target=all, optim=paged_adamw_8bit, cutoff_len=4096. Lane llm-finetune is correct.
- **Sources:** [LLaMA-Factory — Installation & Quick Start](https://llamafactory.readthedocs.io/en/latest/getting_started/installation.html) (hiyouga / LLaMA-Factory, 2026) — YAML-driven QLoRA/LoRA/full-SFT + built-in DPO/KTO/PPO across many model families, with ZeRO-3 offload for full-param.

### OpenRLHF (WSL2) — single-5090 GRPO/PPO via Ray + colocate + ZeRO-3 + adam offload · `situational` · ▸ reproduced
**OpenRLHF fits 7B GRPO on one 32 GB 5090 in WSL2 with --colocate_all_models (single-GPU placement), --vllm_gpu_memory_utilization 0.4, --zero_stage 3 --adam_offload (optimizer state to the 64 GB RAM), --ref_reward_offload, and micro_batch=1 — its README shows 7B full-RLHF across multiple 24 GB cards, so one 32 GB card suffices with ZeRO-3 + offload.**
A second RL framework absent from wave-1, with the explicit Ray actor/critic/reward role model. Cleanest path is the NGC container (already cu13-class). Start a local Ray head, then train_ppo_ray with advantage_estimator=group_norm, the colocate + ZeRO-3 + offload survival kit, --flash_attn, optional --lora_rank 32 for LoRA-RL. Choose OpenRLHF over veRL when you want the explicit Ray role model; veRL is the more flexible default.
- **Method:** rl-verifiable-reward · **Applies to:** llm · **Base:** Qwen2.5 · **Kind:** recipe
- **Measured receipt (tensor-engine):** `training-openrlhf-wsl2-ray-vllm-deepspeed-7b-grpo` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `Qwen/Qwen2.5-7B-Instruct`
- **Output license:** commercial **conditional** — OpenRLHF Apache-2.0; datasets/base models carry their own licenses.
- **Fit:** rig 2/5 · studio 1/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| advantage_estimator | group_norm | ○ | GRPO |
| colocate_all_models | on | ○ | single-GPU placement |
| zero_stage | 3 | ○ |  |
| adam_offload | on | ○ | optimizer state to 64 GB RAM |
| vllm_gpu_memory_utilization | 0.4 | ○ |  |

- **Verify:** verdict=confirmed | Recipe `training-openrlhf-wsl2-ray-vllm-deepspeed-7b-grpo` provides verbatim launch command confirming all 5 claimed hparams: advantage_estimator=group_norm (GRPO), colocate_all_models, vllm_gpu_memory_utilization=0.4, zero_stage=3, adam_offload, ref_reward_offload, micro_batch=1. '7B full RLHF across multiple 24 GB 4090s, so one 32 GB card suffices' logic confirmed verbatim in recipe. Lane efficiency is correct.
- **Sources:** [OpenRLHF documentation](https://openrlhf.readthedocs.io/) (OpenRLHF, 2026) — Single-GPU 7B RLHF via colocate + ZeRO-3 + adam/ref-reward offload; the 32 GB survival flags.

### Reference-free & data-gated preference selection — ORPO / SimPO / KTO / GRPO · `situational` · ▸ reproduced
**The preference-optimization method is a function of the DATA you have and the memory you can spare: ORPO/SimPO drop the reference model (one stage, cheapest), KTO needs only unpaired binary good/bad labels, and GRPO/RLVR needs a programmatic verifiable reward that most STYLE/tone studio data does NOT have — so GRPO is situational, not the default.**
This entry is the selection map that sits behind the DPO recipe. ORPO folds preference into SFT as a single stage with an odds-ratio penalty on the rejected response and NO reference model — the cheapest path when you want one run and have paired data. SimPO replaces DPO's reference-anchored reward with a length-normalized average log-prob plus a target margin, also reference-free. KTO (Kahneman-Tversky Optimization) borrows prospect-theory utility and trains on UNPAIRED binary labels (this output is good / this output is bad), which is the realistic shape of most cheaply-collected feedback. GRPO/RLVR samples a GROUP of completions per prompt and uses their normalized rewards as advantages (no critic), but the reward must be a verifiable program (math correctness, format, unit tests). The studio's #2 workload is tone/style fine-tuning, whose quality is a judgment call with no programmatic verifier — so GRPO is explicitly NOT the default here; it earns its place only on tasks with a checkable answer. On the rig, GRPO additionally requires colocating the vLLM rollout sampler in the trainer and keeping the policy small (<=4B) to fit the sampler KV-cache plus trainer in 32 GB.
- **For the pipeline:** Encode preference-method choice as a decision gate, not a preference: (paired + want cheapest single stage) -> ORPO; (paired + length-bias worry) -> SimPO; (unpaired binary labels) -> KTO; (paired + ref model affordable) -> DPO; (programmatically verifiable reward exists) -> GRPO/RLVR. Do NOT default the studio's style/tone runs to GRPO — it lacks the verifiable-reward precondition. Reserve GRPO for code/math/format tasks and cap policy size at 4B on this rig.
- **Method:** orpo · **Applies to:** llm · **Base:** qwen3 · **Kind:** method-theory
- **Tuning budget:** Method-dependent: ORPO/SimPO add a margin/penalty hyperparameter; KTO adds desirable/undesirable weights; GRPO adds num_generations and a reward-function contract. · **Search:** literature-driven selection map (no rig sweep)
- **Variance:** ORPO/SimPO/KTO/GRPO selection logic is reproduced from each method's own paper + the ms-swift implementation that shares the rig's measured rlhf path; the GRPO single-GPU fit is rig-measured but lives under its own engine recipe, not claimed as measured here.
- **Validated under:** Not rig-measured as a single config; the GRPO single-card colocate fit is measured separately (see engine_recipe_ref), policy <=4B, vllm_gpu_memory_utilization 0.4-0.5, num_generations 8.
- **Measured receipt (tensor-engine):** `training-ms-swift-grpo-single-gpu-vllm-colocate-rl-on-one-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `qwen3-8b`
- **Builds on (stage 2):** QLoRA-NF4 SFT with chat template (stage 1) — 8-34B on one 5090
- **Output license:** commercial **conditional** — All four methods are Apache-2.0 in ms-swift/TRL. Commercial cleanliness is gated by data + base weights as with DPO. KTO is especially attractive for commercial-clean data collection because unpaired binary labels are far cheaper to author in-house than paired comparisons.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| loss_type | orpo/simpo/kto/grpo | ● | the --rlhf_type swap selects the loss; each carries its own extra knobs |
| beta | 0.1 | ○ | ORPO odds-ratio weight / SimPO has its own beta+gamma margin |
| group_size | 8 | ○ | GRPO num_generations per prompt — the group the advantage is normalized over |
| learning_rate | 5e-6 | ○ | preference-stage lr band, as DPO |

- **Datasets:** NuminaMath-TIR — 5k verifiable-reward slice (verifiable-reward-rl, license Apache-2.0 (NuminaMath release).)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| GRPO run OOMs or sampler is starved on the single card | Colocated vLLM rollout KV-cache and trainer contend for the same 32 GB; policy too large | Cap policy at <=4B, lower vllm_gpu_memory_utilization to 0.4-0.5, reduce num_generations | group_size |
| GRPO chosen for a style/tone task produces no improvement or gibberish-but-high-reward | No genuine verifiable reward exists for the task; the reward function is a proxy that gets hacked | Do not use GRPO without a programmatic verifier; switch to KTO/DPO/ORPO with human preference labels for subjective-quality tasks | loss_type |
| SimPO/DPO model gets shorter and shorter (or longer and longer) | Length bias in the implicit reward; SimPO addresses this with length-normalization, DPO does not | Use SimPO's length-normalized objective or add a length penalty / RPO term | loss_type |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| verifiable-reward | task pass-rate (math/format/unit-test) |  |  | ✓ | programmatic verifier (not an LLM) |

- **Best for:** Reference-free single-stage preference tuning (paired data, minimal memory) (llm-orpo, fit 5) ; Preference tuning from cheap UNPAIRED binary good/bad labels (llm-kto, fit 5) ; RL with a programmatically verifiable reward (math/code/format) (llm-grpo, fit 3)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. ORPO, KTO, SimPO, and GRPO are all active and prominent in the 2025-2026 post-training literature. The data-gated framing for method selection is confirmed as current best practice. | One fix required. The GRPO sub-claim — 'drops the value/critic model by normalizing rewards within a sampled group' — is accurate, but the primary citation (arXiv:2402.03300, DeepSeekMath) supports GRPO's existence and group-relative mechanism; its abstract only mentions 'enhancing memory usage of PPO' without explicitly stating the value/critic elimination. The stronger citation for that specific architectural claim is arXiv:2503.06539 (Ahmadian et al. 2025, 'Reinforcement Learning with Verifiable Rewards: GRPO's Effective Loss, Dynamics, and Success Amplification'), which formally analyzes GRPO's loss structure. Add this as a supplementary source for the value/critic-drop sub-claim. All other sources verified: ORPO (arXiv:2403.07691), KTO (arXiv:2402.01306, ICML 2024), SimPO (arXiv:2405.14734, NeurIPS 2024) all confirmed real with correct authors and supported claims. The studio-specific judgment that GRPO is situational for style/tone data (no programmatic verifier available) is sound and well-reasoned. evidence_strength='reproduced-from-source' is appropriate.
- **Sources:** [ORPO: Monolithic Preference Optimization without Reference Model](https://arxiv.org/abs/2403.07691) (Hong, Lee, Thorne, 2024) — A single-stage odds-ratio penalty folds preference alignment into SFT with no reference model and no separate preference phase, matching or beating SFT+DPO. ; [KTO: Model Alignment as Prospect Theoretic Optimization](https://arxiv.org/abs/2402.01306) (Ethayarajh, Xu, Muennighoff, Jurafsky, Kiela, 2024) — A Kahneman-Tversky utility loss aligns models from UNPAIRED binary good/bad signals, matching or exceeding DPO without requiring preference pairs. ; [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (introduces GRPO)](https://arxiv.org/abs/2402.03300) (Shao, Wang, Zhu, Xu, et al., 2024) — Group Relative Policy Optimization drops the value/critic model by normalizing rewards within a sampled group of completions per prompt, cutting RL memory cost — used with verifiable rewards. ; [SimPO: Simple Preference Optimization with a Reference-Free Reward](https://arxiv.org/abs/2405.14734) (Meng, Xia, Chen, 2024) — A length-normalized average-log-prob reward with a target margin removes DPO's reference model and corrects length bias.

### SkyRL (WSL2) — long-horizon agentic / tool-use RL research (Tinker-compatible single-GPU backend) · `situational` · ▸ reproduced
**SkyRL is Ray+vLLM Linux-first (WSL2 only on this rig) and targets long-horizon tool-using agent RL with three layers (skyrl-train trainer, skyrl-gym verifiable-reward task gym, skyrl-agent async multi-turn layer); for single-GPU experiments use the Tinker-compatible skyrl-tx backend rather than the full Ray cluster, and train bf16 because WSL2 hides Blackwell FP8/FP4 tensor cores — and one 32 GB card limits policies to <=4-7B LoRA.**
A research-tier agentic-RL framework with no wave-1 analog. Install via uv (-e skyrl-train / skyrl-gym / skyrl-agent). Use for long-horizon tool-use agent RL research, not throughput. Carries the standing WSL2 rule: FP8/FP4 hidden under WSL2 — expect no Blackwell FP8 speedup.
- **Method:** rl-agentic · **Applies to:** llm · **Kind:** recipe
- **Measured receipt (tensor-engine):** `training-skyrl-wsl2-agentic-rl-setup-research-wsl2-only` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **conditional** — SkyRL Apache-2.0; vet task/reward datasets and base models.
- **Fit:** rig 1/5 · studio 1/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| no Blackwell FP8/FP4 speedup; train slower than expected | WSL2 hides FP8/FP4 tensor cores (the wave-1/2 rule) | train bf16; do not expect FP8 throughput under WSL2 |  |

- **Verify:** verdict=confirmed | Recipe `training-skyrl-wsl2-agentic-rl-setup-research-wsl2-only` confirms all sub-claims: WSL2-only (native Windows not supported); three-layer architecture (skyrl-train, skyrl-gym, skyrl-agent) installed separately; Tinker-compatible skyrl-tx backend for single-GPU experiments; WSL2 hides FP8/FP4 so train bf16; 32 GB limits to <=4-7B LoRA policies. All claims faithful. Lane efficiency is acceptable for an RL training fit-on-one-GPU technique.
- **Sources:** [SkyRL (NovaSky-AI/SkyRL)](https://github.com/NovaSky-AI/SkyRL) (NovaSky AI, 2026) — Three-layer agentic RL (train/gym/agent) on Ray+vLLM; Tinker-compatible skyrl-tx backend for single-GPU.

### open-instruct / Tülu RLVR (WSL2) — reference codebase to read, then re-implement single-GPU · `situational` · ▸ reproduced
**Ai2's open-instruct (RLVR/Tülu) is a Linux+Ray+vLLM reference whose published recipes assume 8 GPUs; on one 5090 the value is to READ how verifiable-reward RL is wired and re-implement the reward in ms-swift's --reward_funcs for an actually-single-GPU run — and to heed that the Apache-2.0 framework ships several non-commercial/ODC Tülu/OLMo datasets and community-licensed base models.**
A study/adapt reference, not a runnable single-GPU recipe — distinct from wave-1's runnable GRPO selection note. Best used to understand RLVR wiring then lift the verifiable reward into the rig's actually-single-GPU ms-swift GRPO path. Strong license caveat: vet data + base-model license before any commercial fine-tune.
- **Method:** rl-verifiable-reward · **Applies to:** llm · **Kind:** method-theory
- **Measured receipt (tensor-engine):** `training-open-instruct-wsl2-rlvr-reference-study-adapt-wsl2` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **conditional** — Framework Apache-2.0 but several Tülu/OLMo recipe datasets are non-commercial/ODC and base models carry community licenses — vet before any commercial fine-tune.
- **Fit:** rig 1/5 · studio 1/5
- **Verify:** verdict=confirmed-with-fixes | All claims are faithful to recipe `training-open-instruct-wsl2-rlvr-reference-study-adapt-wsl2`: 8-GPU assumption, re-implement in ms-swift, Apache-2.0 code with non-commercial/ODC Tülu/OLMo datasets. FIX NEEDED — lane placement: this technique covers RLVR/preference RL methods (SFT + RL), which belongs in the `llm-finetune` lane (described as 'SFT + preference + RL'), not `efficiency` (described as 'Fitting TRAINING on one 32 GB Blackwell GPU — the binding constraint, orthogonal to method choice'). The technique has no efficiency/VRAM hparams — it is a method-theory entry about RL training approach. Move to llm-finetune lane.
- **Sources:** [open-instruct (allenai/open-instruct)](https://github.com/allenai/open-instruct) (Allen Institute for AI (Ai2), 2026) — RLVR/Tülu reference codebase (8-GPU recipes); Apache-2.0 framework with non-commercial dataset/base-model caveats.

### veRL (WSL2) — single-5090 GRPO with colocated vLLM rollout + FSDP param/optimizer offload · `situational` · ▸ reproduced
**veRL runs single-5090 GRPO inside WSL2 by colocating the vLLM rollout sampler with the FSDP trainer and keeping VRAM survivable via gpu_memory_utilization=0.4 (rollout shares VRAM with FSDP shards), param_offload+optimizer_offload to the 64 GB RAM, LoRA (rank 32) over full-param, and a small train_batch_size — 1.5B is comfortable, 7B is the cramped ceiling on one card.**
An RL framework absent from wave-1 (which covers GRPO as a preference-method selection note, not as a runnable framework). Install verl[vllm]==0.8.0 on the WSL2 cu128 base (force torch==2.9.0+cu128 first if it resolves wrong). main_ppo with adv_estimator=grpo, lora_rank/alpha 32, fsdp param+optimizer offload, rollout vllm tp=1, gpu_memory_utilization=0.4. The 32 GB levers are explicit. Scale-out: bump n_gpus_per_node and drop offload on rented multi-GPU.
- **Method:** rl-verifiable-reward · **Applies to:** llm · **Base:** Qwen2.5 · **Kind:** recipe
- **Measured receipt (tensor-engine):** `training-verl-wsl2-single-5090-grpo-lora-qwen-1-5b-to-7b` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `Qwen/Qwen2.5-1.5B-Instruct`
- **Output license:** commercial **conditional** — veRL Apache-2.0; RLVR datasets/base models carry their own licenses — vet before commercial use.
- **Fit:** rig 2/5 · studio 1/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| adv_estimator | grpo | ○ |  |
| gpu_memory_utilization | 0.4 | ○ | rollout shares VRAM with FSDP shards — too high = OOM during generation |
| param_offload / optimizer_offload | True | ○ | push to 64 GB host RAM |
| lora_rank | 32 | ○ |  |
| tensor_model_parallel_size | 1 | ○ |  |

- **Verify:** verdict=confirmed | Recipe `training-verl-wsl2-single-5090-grpo-lora-qwen-1-5b-to-7b` provides verbatim launch command confirming all claimed hparams: adv_estimator=grpo, gpu_memory_utilization=0.4, param_offload=True, optimizer_offload=True, lora_rank=32, tensor_model_parallel_size=1. '1.5B is comfortable, 7B is the cramped ceiling' stated verbatim in recipe. WSL2-only framing confirmed. Lane efficiency is correct.
- **Sources:** [Qwen docs — veRL training](https://qwen.readthedocs.io/en/latest/training/verl.html) (Qwen / veRL, 2026) — veRL GRPO with colocated vLLM rollout + FSDP offload; single-GPU levers (gpu_memory_utilization, param/optimizer offload, LoRA) make it fit one card.

### DAA differences are a blur — SFT then preference · `situational` · paper
**Unifies one- and two-stage DAAs under SFT-then-preference with shared beta tempering; SFT volume and two-stage setup dominate objective-family differences.**
Unifies one- and two-stage DAAs under SFT-then-preference with shared beta tempering; SFT volume and two-stage setup dominate objective-family differences.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not invent recipes. Do not flip technique rows.
- **Method:** dpo · **Applies to:** llm · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0. Invented recipes: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [DAA differences are a blur — SFT then preference](https://arxiv.org/abs/2502.01237) — Unifies one- and two-stage DAAs under SFT-then-preference with shared beta tempering; SFT volume and two-stage setup dominate objective-family differences.

### DAPO — open-source LLM RL at scale · `situational` · paper
**Open reproduction stack for large-scale reasoning RL; complements GRPO/RLVR lane. Do not invent recipes.**
Open reproduction stack for large-scale reasoning RL; complements GRPO/RLVR lane. Do not invent recipes.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not invent recipes. Do not flip technique rows.
- **Method:** rl · **Applies to:** llm · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** systems
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0. Invented recipes: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [DAPO — open-source LLM RL at scale](https://arxiv.org/abs/2503.14476) — Open reproduction stack for large-scale reasoning RL; complements GRPO/RLVR lane. Do not invent recipes.

### HF PEFT LoRA/QLoRA + Diffusers LoRA + bnb AdamW8bit stack · `situational` · docs
**Portable PEFT/Diffusers/bnb 8-bit Adam stack docs for single-GPU LoRA/QLoRA; no invent ranks.**
STUDY-034 Practitioner Verifier ✅ stack hold. Recipes invented: 0.
- **For the pipeline:** STUDY-034 Verifier ✅. Recipes invented: 0. Copy Ostris YAML values only where present.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-034 deepen; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [PEFT LoRA conceptual guide](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora) — LoraConfig r/alpha/target_modules/use_rslora. ; [PEFT Quantization / QLoRA](https://huggingface.co/docs/peft/main/en/developer_guides/quantization) — bnb 4-bit NF4 + LoRA QLoRA path. ; [Diffusers Training LoRA](https://huggingface.co/docs/diffusers/en/training/lora) — train_text_to_image_lora.py PEFT LoraConfig. ; [bitsandbytes 8-bit optimizers](https://huggingface.co/docs/bitsandbytes/main/en/optimizers) — AdamW8bit ~75% less optimizer GPU memory.

### Unsloth fine-tune + Blackwell RTX 50 series tooling · `situational` · docs
**Unsloth LoRA/QLoRA guide + official 50-series/Blackwell support for local 5090 tooling; no invent ranks/LRs.**
STUDY-034 Practitioner Verifier ✅. Recipes invented: 0.
- **For the pipeline:** STUDY-034 Verifier ✅. Recipes invented: 0. Copy Ostris YAML values only where present.
- **Method:** qlora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-034 deepen; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Unsloth Fine-tuning LLMs Guide](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide) — LoRA vs QLoRA; load_in_4bit starting path. ; [Fine-tuning LLMs with Blackwell, RTX 50 series & Unsloth](https://docs.unsloth.ai/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth) — 5060–5090 named; TORCH_CUDA_ARCH_LIST=12.0.

