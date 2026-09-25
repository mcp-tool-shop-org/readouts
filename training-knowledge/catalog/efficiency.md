# Single-GPU efficiency & training-VRAM technique
_Fitting TRAINING on one 32 GB Blackwell GPU — the binding constraint, orthogonal to method choice. The training-VRAM arithmetic (optimizer-state + gradient + activation sizing) and the decision heuristics; paged/8-bit optimizers, gradient checkpointing/accumulation, FSDP2 CPU-offload, NF4 vs fp8 training. Measured peaks->tensor-engine; inference placement->docker-knowledge._ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

12 techniques · 4 recommended · 2 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 1 | gradient_checkpointing is mandatory for lycoris.kohya LoRA on 32 GB (MEASURED 27.7 -> 14.5 GB) | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 2 | 8-bit / paged AdamW (bitsandbytes) — cut and spill the optimizer-state addend | qlora | both | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 2 | Gradient-checkpointing + bf16 + grad-accum — the activation-addend trio | lora | both | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Training-VRAM arithmetic: the optimizer + gradient + activation budget on one 32 GB GPU | lora | both | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 5 | FSDP2 CPUOffload full-finetune — spill params + optimizer state into 64 GB host RAM | sft | both | ▣ measured | ✅ yes | 2 | 2 | ✓ |
| 9 | Axolotl docs — LoRA/QLoRA/DPO/GRPO surface | axolotl | llm | docs | check | 4 | 4 | · |
| 9 | Diffusers Training LoRA — train_text_to_image_lora | lora | both | docs | check | 4 | 4 | · |
| 9 | GoF Adapter pattern hold-with-limit (≠ ΔW) | lora | both | docs | check | 4 | 4 | · |
| 9 | HF Trainer — TrainingArguments surface | trainer | both | docs | check | 4 | 4 | · |
| 9 | PEFT library index — live mid-2026 surface | peft | both | docs | check | 4 | 4 | · |
| 9 | Unsloth docs — local run+train surface | unsloth | both | docs | check | 4 | 4 | · |
| 9 | WCR PEFT fine-tune license flow-down | lora | both | docs | check | 4 | 4 | · |

## Detail

### gradient_checkpointing is mandatory for lycoris.kohya LoRA on 32 GB (MEASURED 27.7 -> 14.5 GB) · `recommended` · ▣ measured
**MEASURED: lycoris.kohya SDXL LoRA (dim16/1024) peaks 27.7 GB WITHOUT gradient_checkpointing (vs native sd-scripts LoRA's 19.4 GB), and DoRA on top SPILLS the 32 GB ceiling -> WDDM pages GPU memory to system RAM -> 33 s/it (~50x slower); adding --gradient_checkpointing drops the peak to 14.5 GB at 1.06 s/it, fitting DoRA + LoKr with ~18 GB headroom.**
Earned the hard way (a ~2-hour spilled DoRA run before catching it). Two env facts for this rig: (1) lycoris.kohya is far heavier than native LoRA without gradient checkpointing; pass --gradient_checkpointing for ANY lycoris training here. (2) This sd-scripts checkout has NO native DoRA ('dora_wd' absent from networks.lora) -> DoRA/LoKr/LoCon route through lycoris-lora 3.4.0, installed via `uv pip install --no-deps` (the venv is uv-managed with no pip; --no-deps protected the torch 2.12.0+cu130 build, the #155 trap).
- **For the pipeline:** Always pass --gradient_checkpointing for lycoris.kohya on the 5090. And verify run-1's VRAM receipt before launching any unattended multi-run training batch — a 27.7 GB run-1 was the visible warning that DoRA would spill.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** failure-fix
- **Runs:** 4
- **Validated under:** RTX 5090 32GB; SDXL base 1.0; stdstyl set; lycoris.kohya dim16; with/without --gradient_checkpointing. 2026-06-06.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-proven-blackwell-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **yes**
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| lycoris_lora_vram_NO_gc | 27.7 GB | ○ |  |
| lycoris_lora_vram_WITH_gc | 14.5 GB | ○ |  |
| native_lora_vram_no_gc | 19.4 GB | ○ | native sd-scripts is lighter than lycoris |
| dora_no_gc | 32 GB spill -> 33 s/it (WDDM paging) | ○ | unusable without gradient_checkpointing |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| lycoris DoRA/LoRA training at ~33 s/it with VRAM pinned near 32 GB | no gradient_checkpointing + lycoris codepath overhead spills the card -> system-RAM paging | --gradient_checkpointing (27.7 -> 14.5 GB measured) | gradient_checkpointing |

- **Best for:** fitting lycoris LoRA/DoRA/LoKr training on 32 GB (single-gpu, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-06 | direct rig measurement (incl. the spill failure)
- **Sources:** [training-knowledge wave-4 measurement (lycoris VRAM, the spill + the fix)](https://github.com/mcp-tool-shop-org/readouts) — rig-measured RTX 5090 2026-06-06

### 8-bit / paged AdamW (bitsandbytes) — cut and spill the optimizer-state addend · `recommended` · ▸ reproduced
**Swapping fp32 AdamW for bitsandbytes 8-bit AdamW cuts optimizer state ~4x (8→2 B/trainable-param) with no measured task-quality loss; the paged variant additionally survives transient OOM spikes by spilling moment pages to host RAM.**
Drop-in optimizer swap that targets the optimizer-state addend specifically. bitsandbytes AdamW8bit block-wise-quantizes Adam's m and v moments to 8-bit (block size 2048, dynamic non-linear quant + stable embedding) — the moments are dequantized per-block on use, so the running state is ~2 B/param instead of fp32's 8 B/param. PagedAdamW8bit goes further: it registers the optimizer buffers as CUDA unified (paged) memory so, when a forward/backward spike would OOM, the optimizer pages are evicted to host RAM and paged back — turning a hard OOM crash into a slowdown. This is the 'paged optimizer' from the QLoRA paper, the standard pairing for QLoRA-NF4 SFT of 24-34B models on the rig. For SDXL/Flux LoRA the optimizer addend is small (adapter-only trainable params), so 8-bit AdamW buys little there — the studio's diffusion default leans on Prodigy/AdamW + checkpointing instead, and this recipe earns its keep mainly on the LLM lane. Wiring: kohya/sd-scripts exposes --optimizer_type AdamW8bit; PEFT/Unsloth/TRL accept optim='paged_adamw_8bit'.
- **For the pipeline:** On the LLM full/QLoRA lane, make paged_adamw_8bit the default optimizer — it is the cheapest lever that attacks the dominant addend and the paged behavior is a free OOM safety net. On the diffusion lane, do NOT reach for it first; the optimizer addend is too small for the swap to matter, and Prodigy's auto-LR is worth more.
- **Method:** qlora · **Applies to:** both · **Base:** Qwen3 · **Kind:** recipe
- **Tuning budget:** No search — drop-in swap; LR/schedule inherited from the underlying AdamW recipe. · **Search:** none
- **Validated under:** Memory/quality parity established in the source paper across LM/GLUE/translation/vision; not separately rig-measured here (the rig receipt for the QLoRA-SFT run that uses it lives in tensor-engine).
- **Base model (model-knowledge):** `qwen3-32b`
- **Output license:** commercial **yes** — bitsandbytes is MIT-licensed; the optimizer imposes no output restriction. Output commercial cleanliness inherits from the base weights + SFT dataset.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| optimizer | paged_adamw_8bit | ● | bitsandbytes PagedAdamW8bit; 8-bit moments + unified-memory paging. Plain adamw_8bit if host-RAM paging is undesirable. |
| precision | bf16 | ● | Compute/weights in bf16; only the optimizer MOMENTS are 8-bit, not the gradients or weights. |
| learning_rate | 1e-4 to 2e-4 lr | ○ | QLoRA-SFT range for 24-34B adapters; 8-bit state does not require LR retuning vs fp32 AdamW. |
| warmup | 3-5 percent-of-steps | ○ | Standard linear warmup; unaffected by optimizer precision. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Training is fine for hundreds of steps then OOM-crashes on a long sequence | fp32 AdamW moment buffers leave no headroom for a transient activation spike on a long batch | Switch to paged_adamw_8bit — the spike pages moments to host RAM instead of crashing | optimizer |
| 8-bit optimizer gave no VRAM relief on an SDXL LoRA run | Optimizer state only taxes TRAINABLE params; a LoRA adapter has few, so the addend it cuts was already tiny | On diffusion, attack the activation/base-precision addends (gradient-checkpointing, fp8 base) instead; reserve 8-bit optimizer for the LLM lane | optimizer |

- **Best for:** QLoRA-SFT of a 24-34B model on one 32 GB GPU (llm, fit 5) ; Survive transient OOM spikes without lowering batch (single-gpu, fit 4)
- **Verify:** verdict=confirmed | currency=Current. bitsandbytes 8-bit and paged AdamW are active 2024-2025 practice for both LLM SFT and Flux/SDXL LoRA training. No successor has displaced them; bitsandbytes docs (fetched) confirm both AdamW8bit and PagedAdamW8bit remain the live API. | All three citations verified. arXiv:2110.02861 and arXiv:2305.14314 are real and support the claims. The bitsandbytes optimizers docs URL (https://huggingface.co/docs/bitsandbytes/main/en/optimizers) resolves and confirms: '75% less GPU memory without losing any accuracy' and paged offload via unified memory. The '8→2 B/param' framing is arithmetically correct (fp32 Adam: 4 bytes × 2 moments = 8 B/param; 8-bit: 1 byte × 2 = 2 B/param). No measured VRAM numbers stored inline; no weight catalog.
- **Sources:** [8-bit Optimizers via Block-wise Quantization](https://arxiv.org/abs/2110.02861) (Tim Dettmers, Mike Lewis, Sam Shleifer, Luke Zettlemoyer, 2021) — Block-wise 8-bit quantization of Adam's optimizer state maintains 32-bit task performance at a fraction of the memory across LM, GLUE, ImageNet and translation. ; [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) (Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, Luke Zettlemoyer, 2023) — Paged optimizers use NVIDIA unified memory to spill optimizer state on memory spikes, preventing the OOM that would otherwise kill long-sequence batches during single-GPU finetuning. ; [bitsandbytes optimizers documentation (8-bit & paged)](https://huggingface.co/docs/bitsandbytes/main/en/optimizers) (bitsandbytes-foundation, 2024) — bitsandbytes exposes AdamW8bit and PagedAdamW8bit as drop-in optimizers; paged variants offload state to CPU RAM via unified memory to avoid OOM.

### Gradient-checkpointing + bf16 + grad-accum — the activation-addend trio · `recommended` · ▸ reproduced
**Gradient-checkpointing trades ~30% recompute for an O(√n) cut to the activation memory addend, and combined with bf16 + grad-accum lets a 1024px SDXL or Flux style-LoRA train at a useful effective batch inside 32 GB.**
The three composable levers that attack the activation addend (the only one that scales with batch/resolution). (1) Gradient (activation) checkpointing: discard intermediate activations on the forward pass and recompute them during backward, dropping activation memory from O(n) to O(√n) for ~30% extra runtime — the single biggest VRAM lever for high-resolution diffusion, where 1024px latents make activations huge. (2) bf16 mixed precision: store weights/activations in bf16 (2 B vs fp32 4 B), halving the activation and weight footprint; bf16's fp32-equivalent exponent range means no loss-scaling fragility (the fp16 failure mode), and Blackwell sm_120 runs it natively. (3) Gradient accumulation: reach a target effective batch with a tiny physical batch, so activation peak stays at the physical-batch level while the gradient signal is averaged over the effective batch. Order of application when OOM: enable bf16 (free), then gradient-checkpointing (cheap, ~30% slower), then drop physical batch to 1-2 and recover effective batch via accumulation. Wiring: kohya/sd-scripts --gradient_checkpointing --mixed_precision bf16 --gradient_accumulation_steps N; PyTorch torch.utils.checkpoint / HF gradient_checkpointing_enable().
- **For the pipeline:** Make --gradient_checkpointing + bf16 the unconditional default for every 1024px SDXL/Flux LoRA on the rig — the recompute cost is worth the headroom it frees for resolution and rank. Use grad-accum, never a larger physical batch, to chase an effective batch — it is the activation-free path to batch size. Do NOT use fp16 in place of bf16 on Blackwell; it reintroduces loss-scaling NaN risk for no memory gain.
- **Method:** lora · **Applies to:** both · **Base:** SDXL · **Kind:** recipe
- **Tuning budget:** No per-run search — these are toggles; effective batch is the only thing tuned, via grad_accum. · **Search:** none
- **Validated under:** The O(√n) activation result and ~30% recompute overhead are from the source paper (48→7 GB on a 1000-layer ResNet); the rig it/s cost of checkpointing on SDXL lives in tensor-engine, not restated here.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — Pure compute technique; no license effect. Output cleanliness inherits from base + dataset.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| precision | bf16 | ● | Native on Blackwell sm_120; no loss-scaling unlike fp16. Halves activation+weight footprint vs fp32. |
| resolution | 1024 px | ● | SDXL native; the resolution that makes the activation addend dominant and checkpointing worthwhile. Flux uses 1024 NL-captioned too. |
| batch_size | 1-2 images | ○ | Keep physical batch low; activation peak scales with it. |
| grad_accum | 4-8 steps | ○ | Recover effective batch (e.g. 1×8=8) without raising the activation peak. |
| network_type | lora | ○ | Frozen base keeps the gradient+optimizer addends tiny; checkpointing then attacks the remaining (activation) addend. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| 1024px SDXL LoRA OOMs at the first backward pass even at batch 1 | Activation addend at 1024px exceeds remaining headroom; gradient-checkpointing not enabled | Add --gradient_checkpointing; if still tight, drop the U-Net text-encoder training or cache latents | gradient_checkpointing |
| Loss goes to NaN early in training | fp16 mixed precision overflow (loss-scaling) — a failure bf16 does not have | Switch --mixed_precision from fp16 to bf16 (free on Blackwell, same memory, fp32 exponent range) | precision |
| Training ~30% slower after enabling checkpointing | Expected — checkpointing recomputes activations on the backward pass (one extra forward) | Accept the recompute cost; it is the price of the O(√n) activation saving. Disable only if VRAM headroom returns. | gradient_checkpointing |

- **Best for:** Fit a 1024px SDXL/Flux style-LoRA in 32 GB (sdxl, fit 5) ; Reach a larger effective batch without more VRAM (single-gpu, fit 5)
- **Verify:** verdict=confirmed | currency=Current. Gradient checkpointing, bf16 mixed precision, and gradient accumulation are the standard 2025-2026 memory-fitting trio for both LLM SFT and diffusion LoRA. Community guides from 2025-2026 confirm kohya sd-scripts still exposes exactly these flags. No superseding approach exists for single-GPU diffusion LoRA. | Citations verified: arXiv:1604.06174 (Chen 2016) is real and supports O(√n) + ~30% overhead claim. HF transformers perf docs are a live reference (appropriately cited as docs, not paper). kohya-ss sd-scripts is real and exposes --gradient_checkpointing, --mixed_precision bf16, and --gradient_accumulation_steps as documented. No measured VRAM scalars stored inline. The bf16 vs fp16 stability note is correct and well-supported.
- **Sources:** [Training Deep Nets with Sublinear Memory Cost](https://arxiv.org/abs/1604.06174) (Tianqi Chen, Bing Xu, Chiyuan Zhang, Carlos Guestrin, 2016) — Gradient checkpointing reduces activation memory to O(√n) for an n-layer net at the cost of one extra forward pass (~30% runtime), demonstrated cutting a 1000-layer ResNet from 48 GB to 7 GB. ; [Performance and Scalability: How to fit a bigger model and train it faster (gradient checkpointing, mixed precision)](https://huggingface.co/docs/transformers/en/perf_train_gpu_one) (Hugging Face, 2024) — Gradient checkpointing, bf16 mixed precision, and gradient accumulation are the standard composable levers for fitting larger training on a single GPU; bf16 avoids fp16 loss-scaling instability. ; [kohya-ss sd-scripts training options (--gradient_checkpointing, --mixed_precision, --gradient_accumulation_steps)](https://github.com/kohya-ss/sd-scripts) (kohya-ss, 2024) — sd-scripts exposes gradient_checkpointing, bf16 mixed precision, and gradient_accumulation_steps as the memory-fitting flags for SDXL/Flux LoRA training.

### Training-VRAM arithmetic: the optimizer + gradient + activation budget on one 32 GB GPU · `recommended` · ▸ reproduced
**Training VRAM is the sum of four addends — model weights + gradients + optimizer state + activations — and only the last two are tunable post-method-choice, so the fitting decision is arithmetic, not guesswork.**
The portable sizing model: (1) weights = P×bytes/param (bf16 = 2 B/param; an NF4-quantized base ≈ 0.5 B/param + small dequant scratch); (2) gradients = one bf16 copy of the *trainable* params only (for LoRA/QLoRA the adapter is tiny, so this addend nearly vanishes — the central reason PEFT fits where full-finetune does not); (3) optimizer state = the dominant addend for full-finetune — Adam keeps two moments, so fp32 Adam = 8 B/param of *trainable* params (4 B m + 4 B v), 8-bit Adam ≈ 2 B/param, paged Adam spills the spikes to host RAM; (4) activations = batch×seq(or HxW latents)×layers, the only addend that scales with batch and the one gradient-checkpointing trades for ~30% recompute. Decision heuristics that fall out of the arithmetic: (a) prefer grad-accum over a larger physical batch once activations dominate — accumulation multiplies the *effective* batch with zero activation cost; (b) reach for an 8-bit/paged optimizer before touching batch size, because optimizer state is a fixed per-trainable-param tax that batch tuning cannot reduce; (c) NF4 (quantize the *base*) attacks addend 1, fp8/bf16 attacks the compute path, gradient-checkpointing attacks addend 4 — they compose, they do not substitute; (d) FSDP2 CPU-offload is the last resort because it converts a memory problem into a PCIe-bandwidth problem. For LoRA on a frozen base the binding addend is usually activations + the (large) frozen base in bf16/fp8, not optimizer state; for full-finetune it is optimizer state — which is why the studio's LoRA-first default holds.
- **For the pipeline:** Make the four-addend table the first artifact of any 'will it fit' question. For SDXL/Flux style-LoRA the frozen base dominates — so the lever order is base-precision (fp8/NF4) → gradient-checkpointing → grad-accum, and the optimizer choice barely matters. For 24-34B full-finetune the optimizer state dominates — lever order flips to QLoRA (kill gradients+optimizer by freezing+quantizing the base) first, FSDP2 CPU-offload only if a true full-finetune is required.
- **Method:** lora · **Applies to:** both · **Base:** SDXL · **Kind:** method-theory
- **Validated under:** Sizing model is arithmetic and base-model-agnostic; the per-addend byte constants (Adam=8 B/param fp32, 8-bit≈2 B/param, bf16 weight=2 B/param, checkpointing≈O(√n) activations at ~30% recompute) are from the cited papers, not rig-measured.
- **Output license:** commercial **yes** — Method theory imposes no license; commercial cleanliness is inherited from the base weights and dataset, tracked on those rows.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| optimizer | adamw-8bit | ○ | fp32 AdamW = 8 B/trainable-param of state; 8-bit ≈ 2 B; paged spills spikes to host RAM. Only taxes TRAINABLE params — negligible for LoRA, dominant for full-finetune. |
| precision | bf16 | ● | bf16 weights = 2 B/param; same exponent range as fp32 so no loss-scaling needed (unlike fp16). Blackwell sm_120 has native bf16. |
| grad_accum | >=1 steps | ○ | Multiplies EFFECTIVE batch at zero activation cost — the preferred lever once activations are the binding addend. effective_batch = batch_size × grad_accum. |
| batch_size | 1-4 images-or-sequences | ○ | The only knob that scales the activation addend; raise effective batch via grad_accum instead of physical batch when activation-bound. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| OOM appears only at the optimizer step, not the forward/backward | Adam allocates m+v moment buffers lazily on first step — the optimizer-state addend is invisible until step 1 | Pre-account 8 B/trainable-param (fp32 Adam) in the budget; switch to 8-bit or paged AdamW to cut/spill that addend | optimizer |
| Raising grad_accum did not reduce peak VRAM | Misconception that accumulation lowers memory — it lowers the *physical* batch needed for a target effective batch, but a given physical batch's activation peak is unchanged | Lower physical batch_size to 1-2, recover effective batch via grad_accum; add gradient-checkpointing to attack the activation addend directly | grad_accum |

- **Best for:** Decide whether a training run fits in 32 GB before launching (single-gpu, fit 5) ; Choose the next VRAM lever when a run OOMs (single-gpu, fit 5)
- **Verify:** verdict=confirmed | currency=Current. The four-addend model (weights + gradients + optimizer state + activations) is the standard 2024-era framing used in HuggingFace docs, bitsandbytes literature, and every major single-GPU training guide. Nothing is superseded. | All three citations confirmed real and correctly attributed. arXiv:2110.02861 (Dettmers 2021) confirms 8-bit optimizer-state compression from 8 B/param to 2 B/param. arXiv:1604.06174 (Chen 2016) confirms O(√n) activation memory with ~30% recompute overhead. arXiv:2305.14314 (Dettmers 2023) confirms PEFT attacks weight+gradient+optimizer addends independently of checkpointing. No measured VRAM numbers are stored inline; no weight catalog present. All finding_supported flags are accurate.
- **Sources:** [8-bit Optimizers via Block-wise Quantization](https://arxiv.org/abs/2110.02861) (Tim Dettmers, Mike Lewis, Sam Shleifer, Luke Zettlemoyer, 2021) — 8-bit optimizers compress Adam's m/v moment state to ~2 B/param (from 8 B/param fp32) while matching 32-bit task performance — the basis for the optimizer-state addend in the arithmetic. ; [Training Deep Nets with Sublinear Memory Cost](https://arxiv.org/abs/1604.06174) (Tianqi Chen, Bing Xu, Chiyuan Zhang, Carlos Guestrin, 2016) — Gradient (activation) checkpointing reduces the activation memory addend to O(√n) for an n-layer net at the cost of one extra forward pass (~30% runtime), shown reducing a 1000-layer ResNet from 48 GB to 7 GB. ; [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) (Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, Luke Zettlemoyer, 2023) — Freezing+4-bit-quantizing the base (NF4) collapses the weight + gradient + optimizer addends so a 65B model finetunes on a single 48 GB GPU — evidence that PEFT attacks different addends than checkpointing.

### FSDP2 CPUOffload full-finetune — spill params + optimizer state into 64 GB host RAM · `situational` · ▣ measured
**When a TRUE full (non-LoRA) finetune of a model just over 32 GB is required, FSDP2 fully_shard with CPUOffloadPolicy pushes params + optimizer state into 64 GB system RAM — combined with activation checkpointing + bf16 it fits, at the cost of being PCIe/CPU-bandwidth-bound.**
The last-resort efficiency path, owned here as the decision heuristic + portable recipe; the measured it/s and VRAM peak live in tensor-engine. Use the FSDP2 fully_shard API (FSDP1 is deprecated) with offload_policy=CPUOffloadPolicy(), MixedPrecisionPolicy(param_dtype=bf16, reduce_dtype=fp32), and activation/gradient checkpointing. On a single GPU FSDP gives no sharding-across-ranks benefit — its value here is purely the CPU-offload mechanism: parameter shards and optimizer state live in host RAM and are streamed to the GPU per layer, so the GPU only ever holds the active layer + activations. This converts a 32 GB memory wall into a PCIe-bandwidth bottleneck (expect it slow). The studio decision rule: this is strictly the path AFTER QLoRA has been ruled out — for almost every studio need a QLoRA-NF4 adapter (Unsloth/PEFT) is the better answer because it sidesteps the bandwidth tax entirely. Reach for DeepSpeed ZeRO-Infinity NVMe-offload only inside WSL2 and only if FSDP2 CPUOffload still OOMs (one more rung down the bandwidth ladder). The rig receipt (exact measured it/s + VRAM peak + WSL2 host-RAM behavior) is in tensor-engine config_recipes; this row stores the portable recipe + the pointer so the number is never duplicated.
- **For the pipeline:** Treat FSDP2 CPU-offload as the studio's documented escape hatch, not a default: it exists so 'the model is 2 GB over the wall and must be a full finetune' has a known answer. Default remains QLoRA-NF4 + paged 8-bit AdamW. If FSDP2 is chosen, budget for a slow, bandwidth-bound run and require 64 GB host RAM; if it still OOMs, step to ZeRO-Infinity NVMe inside WSL2 before declaring the run infeasible.
- **Method:** sft · **Applies to:** both · **Base:** Qwen3 · **Kind:** recipe
- **Seed:** see tensor-engine receipt · **Runs:** 1 · **Tuning budget:** Last-resort path, not tuned for speed — chosen for feasibility, not throughput. · **Search:** manual
- **Variance:** Single measured run on the rig (RTX 5090 / 32 GB / 64 GB host RAM / WSL2); it/s + VRAM peak recorded in the tensor-engine config_recipes row, not restated here. Bandwidth-bound so throughput is sensitive to PCIe + host-RAM speed.
- **Validated under:** RTX 5090, 32 GB VRAM, 64 GB system RAM, Windows 11 / WSL2, Blackwell sm_120; full (non-LoRA) finetune of a model just over the 32 GB wall; FSDP2 fully_shard + CPUOffloadPolicy + activation checkpointing + bf16. Measured throughput/VRAM in tensor-engine.
- **Measured receipt (tensor-engine):** `training-single-gpu-full-finetune-that-won-t-fit-in-32-gb-fsdp2-cpuoffload-into-64-gb-ram` — the rig-measured it/s + VRAM peak live there, not here.
- **Base model (model-knowledge):** `qwen3-32b`
- **Output license:** commercial **yes** — PyTorch FSDP is BSD-licensed; technique imposes no output restriction. Output commercial cleanliness inherits from base weights + dataset.
- **Fit:** rig 2/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | full-finetune | ● | This path exists specifically for FULL finetune; if LoRA/QLoRA suffices, do not use it. |
| precision | bf16 | ● | MixedPrecisionPolicy(param_dtype=torch.bfloat16, reduce_dtype=torch.float32) per the FSDP2 tutorial. |
| optimizer | adamw | ○ | Optimizer state is CPU-offloaded with the param shards into host RAM; 8-bit AdamW can further shrink the host-RAM footprint. |
| batch_size | 1 sequences | ○ | Keep physical batch minimal; the run is bandwidth-bound, not compute-bound, so large batch buys little. |
| grad_accum | >=8 steps | ○ | Recover effective batch since physical batch is pinned at 1. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Full-finetune of a 32-GB-class model OOMs immediately even at batch 1 | Weights + gradients + fp32 optimizer state exceed 32 GB; no offload configured | Wrap with FSDP2 fully_shard + offload_policy=CPUOffloadPolicy() to spill params+optimizer state to 64 GB host RAM; add activation checkpointing | network_type |
| FSDP2 run fits but is extremely slow | Expected — CPU-offload makes the run PCIe/CPU-bandwidth-bound; per-layer param streaming dominates | Accept it as last-resort, or switch to QLoRA-NF4 which avoids offload entirely; this is why QLoRA is the studio default | network_type |
| FSDP2 CPUOffload still OOMs (host RAM exhausted) | 64 GB host RAM insufficient for params + optimizer state of the chosen model | Step down to DeepSpeed ZeRO-Infinity NVMe-offload inside WSL2 (one more bandwidth rung), or reduce model size / fall back to QLoRA | network_type |
| AttributeError / deprecation on FSDP API | Using deprecated FSDP1 (FullyShardedDataParallel wrapper) instead of FSDP2 | Use the FSDP2 fully_shard API (torch.distributed.fsdp.fully_shard); FSDP1 is deprecated | network_type |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| rig-receipt | it/s + VRAM-peak |  |  | ✓ |  |

- **Best for:** Full (non-LoRA) finetune of a model just over the 32 GB wall (single-gpu, fit 3) ; Documented escape hatch when QLoRA is insufficient (llm, fit 3)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. FSDP1 is deprecated as of PyTorch 2.11.0+ (confirmed by PyTorch tutorial). The fully_shard + CPUOffloadPolicy() API is the live canonical form. ZeRO-Infinity is correctly cited as a contextual next-rung alternative, not a replacement. | Two fixes needed. (1) evidence_strength mismatch: the entry is tagged 'measured-on-rig' but the cited papers do not prove single-GPU CPU-offload full finetune — that is a community-reproduced inference from the FSDP API; the rig measurement lives in engine_recipe_ref per boundary rules. The evidence_strength for the citation layer of this entry should be 'reproduced-from-source'. The 'measured-on-rig' tag is acceptable only because it defers entirely to the engine_recipe_ref, but auditors will find it ambiguous without that clarification in a note. (2) engine_recipe_ref slug 'training-single-gpu-full-finetune-that-won-t-fit-in-32-gb-fsdp2-cpuoffload-into-64-gb-ram' reads as an auto-derived display name rather than a canonical recipe slug — verify it matches an actual key in the tensor-engine config_recipes index or the cross-reference will not resolve. The FSDP paper (arXiv:2304.11277) finding_supported='PARTIAL' is correctly flagged: the paper focuses on multi-GPU scaling and only mentions CPU offloading as a supported feature, not a studied contribution. The PyTorch FSDP2 tutorial URL is confirmed live with CPUOffloadPolicy mapping documented. Single-GPU use of FSDP with CPU offload is confirmed functional (PyTorch docs and community reports, including torchtune issue #1412 closed/fixed).
- **Sources:** [PyTorch FSDP: Experiences on Scaling Fully Sharded Data Parallel](https://arxiv.org/abs/2304.11277) (Yanli Zhao, Andrew Gu, Rohan Varma, Liang Luo, Chien-Chin Huang, Min Xu, Less Wright, Hamid Shojanazeri, Myle Ott, Sam Shleifer, Alban Desmaison, Can Balioglu, Pritam Damania, Bernard Nguyen, Geeta Chauhan, Yuchen Hao, Ajit Mathews, Shen Li, 2023) — FSDP shards parameters, gradients and optimizer state and supports CPU offloading, enabling training of significantly larger models than fit in device memory. ; [Getting Started with Fully Sharded Data Parallel (FSDP2)](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html) (Wei Feng, Will Constable, Yifan Mao (PyTorch), 2024) — The FSDP2 fully_shard API supports offload_policy=CPUOffloadPolicy() (maps to FSDP1 CPUOffload.offload_params=True) and MixedPrecisionPolicy(param_dtype=torch.bfloat16, reduce_dtype=torch.float32); FSDP1 is deprecated. ; [DeepSpeed ZeRO-Infinity: NVMe offloading for training beyond GPU+CPU memory](https://www.deepspeed.ai/2021/03/07/zero3-offload.html) (DeepSpeed / Microsoft, 2021) — ZeRO-Infinity offloads parameters and optimizer state to NVMe, the next rung below CPU-offload when host RAM is exhausted.

### Axolotl docs — LoRA/QLoRA/DPO/GRPO surface · `situational` · docs
**Free/open LLM post-training; methods list LoRA, QLoRA, DPO/ORPO/KTO, GRPO; Apache-2.0.**
Free/open LLM post-training; methods list LoRA, QLoRA, DPO/ORPO/KTO, GRPO; Apache-2.0.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not flip technique rows.
- **Method:** axolotl · **Applies to:** llm · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** tooling
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Axolotl docs — LoRA/QLoRA/DPO/GRPO surface](https://docs.axolotl.ai/) — Free/open LLM post-training; methods list LoRA, QLoRA, DPO/ORPO/KTO, GRPO; Apache-2.0.

### Diffusers Training LoRA — train_text_to_image_lora · `situational` · docs
**Official train_text_to_image_lora.py; peft.LoraConfig on UNet (+ text encoder for SDXL).**
Official train_text_to_image_lora.py; peft.LoraConfig on UNet (+ text encoder for SDXL).
- **For the pipeline:** STUDY-009 Verifier-verified. Do not flip technique rows.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** tooling
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Diffusers Training LoRA — train_text_to_image_lora](https://huggingface.co/docs/diffusers/en/training/lora) — Official train_text_to_image_lora.py; peft.LoraConfig on UNet (+ text encoder for SDXL).

### GoF Adapter pattern hold-with-limit (≠ ΔW) · `situational` · docs
**Frozen host + swappable module analogy holds for many LoRAs on one base; limit: software adapters ≠ weight-space ΔW.**
STUDY-034 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-034 Verifier ✅. Copy Ostris YAML values only where present.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-034 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Adapter design pattern](https://refactoring.guru/design-patterns/adapter) — Swappable module on frozen host; ≠ ΔW.

### HF Trainer — TrainingArguments surface · `situational` · docs
**Feature-complete PyTorch train loop with TrainingArguments (bf16/fp16, gradient_checkpointing, adamw_8bit, FSDP/DeepSpeed).**
Feature-complete PyTorch train loop with TrainingArguments (bf16/fp16, gradient_checkpointing, adamw_8bit, FSDP/DeepSpeed).
- **For the pipeline:** STUDY-009 Verifier-verified. Do not flip technique rows.
- **Method:** trainer · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** tooling
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [HF Trainer — TrainingArguments surface](https://huggingface.co/docs/transformers/en/main_classes/trainer) — Feature-complete PyTorch train loop with TrainingArguments (bf16/fp16, gradient_checkpointing, adamw_8bit, FSDP/DeepSpeed).

### PEFT library index — live mid-2026 surface · `situational` · docs
**PEFT adapts large models by training few parameters; integrated with Transformers, Diffusers, Accelerate. Currency of library docs; no technique flip.**
PEFT adapts large models by training few parameters; integrated with Transformers, Diffusers, Accelerate. Currency of library docs; no technique flip.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not flip technique rows.
- **Method:** peft · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** tooling
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [PEFT library index — live mid-2026 surface](https://huggingface.co/docs/peft/en/index) — PEFT adapts large models by training few parameters; integrated with Transformers, Diffusers, Accelerate. Currency of library docs; no technique flip.

### Unsloth docs — local run+train surface · `situational` · docs
**Local run+train; states LoRA, QLoRA, full FT, DPO, GRPO, FP8 support.**
Local run+train; states LoRA, QLoRA, full FT, DPO, GRPO, FP8 support.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not flip technique rows.
- **Method:** unsloth · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** tooling
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Unsloth docs — local run+train surface](https://docs.unsloth.ai/) — Local run+train; states LoRA, QLoRA, full FT, DPO, GRPO, FP8 support.

### WCR PEFT fine-tune license flow-down · `situational` · docs
**LoRA adapter distribution inherits base-model license — commercial-clean PEFT needs commercial-clean base.**
STUDY-034 Analogist Verifier ✅ hold.
- **For the pipeline:** STUDY-034 Verifier ✅. Copy Ostris YAML values only where present.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-034 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [WCR fine-tuned model license](https://wcr.legal/fine-tuned-model-license/) — Fine-tune/LoRA inherits base license.

