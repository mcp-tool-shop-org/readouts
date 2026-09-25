# PEFT methods & adapter theory
_Cross-cutting parameter-efficient fine-tuning theory both domains share — LoRA/QLoRA/DoRA/LoRA+/rsLoRA, diffusion LyCORIS (LoKr/LoHa/LoCon), LLM PiSSA/GaLore + merging. Rank vs alpha as a coupled scaling pair. Weights->model-knowledge; library-as-software->tensor-engine._ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

37 techniques · 4 recommended · 0 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 2 | LoRA: rank and alpha as a coupled scaling pair (alpha/rank = effective-LR multiplier) | lora | both | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | LyCORIS: the diffusion adapter family (LoCon conv, LoKr Kronecker, LoHa Hadamard) | lokr | diffusion | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 2 | QLoRA: LoRA over a 4-bit NF4 frozen base (NF4 + double-quant + paged optimizers) | qlora | llm | ▸ reproduced | ⚠ cond | 5 | 4 | ✓ |
| 4 | DoRA: weight-decomposed LoRA (magnitude + direction, LoRA on direction only) | dora | both | ▸ reproduced | ✅ yes | 4 | 3 | ✓ |
| 5 | Ostris train_lora_qwen_image_24gb.yaml (sourced 24GB path) | lora | both | docs | check | 4 | 4 | · |
| 6 | Adapter/model merging: TIES (trim+elect-sign+merge) and DARE (drop+rescale) | lora | llm | ▸ reproduced | ⚠ cond | 3 | 2 | ✓ |
| 9 | A Rank Stabilization Scaling Factor for Fine-Tuning with LoRA | lora | both | paper | check | 3 | 3 | · |
| 9 | A Unified Study of LoRA Variants: Taxonomy, Review, Codebase, and Empirical Evaluation | lora | both | paper | check | 3 | 3 | · |
| 9 | AdaLoRA adaptive rank budget (Zhang et al. 2023) | lora | both | paper | check | 4 | 4 | ✓ |
| 9 | Kustomize kustomization overlays | lora | both | paper | check | 3 | 3 | · |
| 9 | Learning Rate Matters — LoRA LR retuning | lora | both | paper | check | 4 | 4 | · |
| 9 | Learning Rate Matters: Vanilla LoRA May Suffice for LLM Fine-tuning | lora | both | paper | check | 3 | 3 | · |
| 9 | LoFT — LoRA that behaves like full fine-tuning | lora | both | paper | check | 4 | 4 | · |
| 9 | LoFT: Low-Rank Adaptation That Behaves Like Full Fine-Tuning | lora | both | paper | check | 3 | 3 | · |
| 9 | LoRA Dropout as a Sparsity Regularizer for Overfitting Control | lora | both | paper | check | 3 | 3 | · |
| 9 | LoRA learns less and forgets less (Biderman et al. 2024) | lora | both | paper | check | 4 | 4 | · |
| 9 | LoRA+ asymmetric learning rates (Hayou et al. 2024) | lora | both | paper | check | 4 | 4 | · |
| 9 | LoRA-GA: Low-Rank Adaptation with Gradient Approximation | lora | both | paper | check | 3 | 3 | · |
| 9 | LoRA-Pro: Are Low-Rank Adapters Properly Optimized? | lora | both | paper | check | 3 | 3 | · |
| 9 | PEFT LoRA conceptual guide (`LoraConfig` r / `lora_alpha`) | lora | both | paper | check | 3 | 3 | · |
| 9 | PEFT LoraConfig package ref | lora | both | paper | check | 3 | 3 | · |
| 9 | PiSSA principal-subspace adapter init (Meng et al. 2024) | lora | both | paper | check | 4 | 4 | · |
| 9 | Semantic Versioning 2.0.0 | lora | both | paper | check | 3 | 3 | · |
| 9 | TsqLoRA — sensitivity and quality LoRA | lora | both | paper | check | 4 | 4 | · |
| 9 | TsqLoRA: Towards Sensitivity and Quality Low-Rank Adaptation for Efficient Fine-Tuning | lora | both | paper | check | 3 | 3 | · |
| 9 | Twelve-Factor App III. Config | lora | both | paper | check | 3 | 3 | · |
| 9 | Unified Study of LoRA Variants — taxonomy | lora | both | paper | check | 4 | 4 | · |
| 9 | Unsloth LoRA Hyperparameters Guide | lora | both | paper | check | 3 | 3 | · |
| 9 | VeRA vector-based random matrix adaptation (Kopiczko et al. 2023) | lora | both | paper | check | 4 | 4 | · |
| 9 | What Happens to the License When You Fine‑Tune a Model | lora | both | paper | check | 3 | 3 | · |
| 9 | `train_lora_qwen_image_24gb.yaml` | lora | both | paper | check | 3 | 3 | · |
| 9 | kohya train_network.md | lora | both | paper | check | 3 | 3 | · |
| 9 | train_lora_chroma_24gb.yaml | lora | both | paper | check | 3 | 3 | · |
| 9 | train_lora_flex_24gb.yaml | lora | both | paper | check | 3 | 3 | · |
| 9 | train_lora_flux_24gb.yaml | lora | both | paper | check | 3 | 3 | · |
| 9 | train_lora_qwen_image_edit_32gb.yaml | lora | both | paper | check | 3 | 3 | · |
| 9 | train_lora_wan22_14b_24gb.yaml | lora | both | paper | check | 3 | 3 | · |

## Detail

### LoRA: rank and alpha as a coupled scaling pair (alpha/rank = effective-LR multiplier) · `recommended` · ▸ reproduced
**LoRA injects a frozen-base low-rank update BA scaled by alpha/r, so rank and alpha are NOT independent knobs — alpha/rank is a single effective-learning-rate multiplier on the adapter, and the rsLoRA fix shows the canonical alpha/r collapses learning at high rank.**
LoRA (Hu et al. 2021) freezes pretrained weights W0 and learns a rank-r decomposition delta-W = B*A (B in R^{d×r}, A in R^{r×k}), with the update added as W0 + (alpha/r)*B*A. The alpha/r factor is the load-bearing coupling: doubling alpha while holding rank fixed doubles the adapter's effective contribution exactly like raising its learning rate, which is why kohya/diffusion practice sets alpha=rank (scale 1.0) or alpha=rank/2 (scale 0.5) rather than treating alpha as a free dimension. Two refinements sharpen the coupling: rsLoRA (Kalajdzievski 2023) proves the canonical alpha/r divisor slows/stunts learning at higher ranks and that dividing by alpha/sqrt(r) instead stabilizes gradients and unlocks high-rank capacity; LoRA+ (Hayou et al. 2024) shows A and B should NOT share a learning rate — raising B's LR above A's by a fixed ratio gives ~1-2% quality and up to ~2x speedup at the same cost. Original LoRA is typically applied to attention query/value projections; diffusion practice extends it to more modules (see LyCORIS LoCon).
- **For the pipeline:** Tune rank and alpha together, never in isolation: pick rank for capacity, then set alpha to fix the scale (alpha=rank for 1.0, or use rsLoRA's sqrt-scaling when pushing rank>32 on SDXL style work). For 24-34B LLM QLoRA, LoRA+ (higher B-LR) and rsLoRA are cheap wins. A LoRA whose effective scale is mis-set reads at inference like an over/under-strength adapter regardless of how long it trained.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen3|Llama · **Kind:** method-theory
- **Tuning budget:** Coupling is theory-derived; no rig grid run this wave (lane has no rig-measured recipe yet). · **Search:** none
- **Variance:** alpha/r scaling and the rsLoRA sqrt(r) result are analytic (derived + proven in-source), not single-run artifacts; LoRA+ 1-2%/2x figures are the paper's reported measurements, not rig-measured here.
- **Validated under:** Cross-domain theory: validated in-source on LLMs (RoBERTa/DeBERTa/GPT-2/GPT-3, Hu 2021) and on LLaMA-family (rsLoRA, LoRA+); the alpha/rank=scale identity is architecture-agnostic and applies unchanged to SDXL/Flux adapters.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — LoRA is a method, not weights — output commercial-cleanliness inherits entirely from the chosen base model and dataset, not from LoRA itself. The method imposes no license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | lora | ● | linear low-rank adapter (LoRA / kohya 'networks.lora'). |
| rank | capacity knob (set first) dim | ● | r in B(d×r)·A(r×k); higher r = more capacity + more params. Couple with alpha. |
| alpha | set to fix scale (alpha/rank) | ● | Effective scale = alpha/rank. alpha=rank -> scale 1.0; alpha=rank/2 -> 0.5. NOT an independent capacity knob. |
| network_type | lora (rsLoRA scaling) | ○ | rsLoRA: replace alpha/r divisor with alpha/sqrt(r) to stabilize high-rank training (Kalajdzievski 2023). |
| learning_rate | split A vs B (LoRA+) | ○ | LoRA+ : lr_B > lr_A by fixed ratio lambda; ~1-2% quality, up to ~2x speedup (Hayou 2024). |
| target_modules | attn q,v (LLM) / + conv (diffusion) | ○ | Original LoRA targets query/value attention; diffusion extends to conv (LoCon). |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Adapter trained correctly but inference looks over-baked or washed-out at weight 1.0 | alpha set far from rank so the effective scale (alpha/rank) is too high/low — read as wrong adapter strength. | Set alpha=rank for scale 1.0 (or compensate at inference by lowering/raising LoRA weight); do not raise alpha to 'add capacity'. | alpha |
| High-rank LoRA (r>=64) learns slower / plateaus worse than a low-rank run | canonical alpha/r divisor shrinks the high-rank update, the stunted-learning effect rsLoRA identifies. | Switch to rsLoRA sqrt-rank scaling (alpha/sqrt(r)) to unlock high-rank capacity. | rank |

- **Best for:** Parameter-efficient style/task adaptation on one GPU (single-gpu, fit 5) ; Correctly sizing SDXL style-LoRA scale (sdxl, fit 5)
- **Verify:** verdict=confirmed | currency=Current. rsLoRA (arXiv:2312.03732) and LoRA+ (arXiv:2402.12354) are both actively integrated in kohya sd-scripts and related tooling as of 2025/2026. The alpha/rank scaling framing remains the canonical operational model. | All three papers are real, correctly cited, and support the stated claims. The kohya community source is accurate: network_alpha/network_dim is the live operational knob, and network_alpha == network_dim yields adapter scale 1.0. The claim that alpha/rank is a single effective-LR multiplier is a useful simplification but slightly incomplete — LoRA+ demonstrates that A and B matrix LRs interact asymmetrically even at fixed alpha/rank, so the multiplier framing is the floor, not the ceiling. Acceptable abstraction for a how-to-train KB; no fix required.
- **Sources:** [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) (Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, 2021) — Freezes pretrained weights and injects trainable rank-decomposition matrices scaled by alpha/r; reduces trainable params ~10,000x and GPU memory ~3x vs full GPT-3 175B fine-tuning, on-par or better quality. ; [A Rank Stabilization Scaling Factor for Fine-Tuning with LoRA (rsLoRA)](https://arxiv.org/abs/2312.03732) (Damjan Kalajdzievski, 2023) — Proves the canonical divide-by-rank scaling slows learning and stunts high-rank performance, and that dividing by sqrt(rank) instead stabilizes learning and unlocks a compute/performance trade-off at larger ranks. ; [LoRA+: Efficient Low Rank Adaptation of Large Models](https://arxiv.org/abs/2402.12354) (Soufiane Hayou, Nikhil Ghosh, Bin Yu, 2024) — Using the same learning rate for A and B is suboptimal; setting a higher learning rate for B by a fixed ratio gives 1-2% quality improvement and up to ~2x speedup at the same compute cost. ; [kohya-ss/sd-scripts — LoRA training (network_dim / network_alpha)](https://github.com/kohya-ss/sd-scripts) (kohya-ss, 2024) — In the dominant SDXL LoRA trainer, network_alpha relative to network_dim sets the adapter scale (alpha=dim -> scale 1.0); the operational alpha-vs-dim convention used by the studio. (Operational/community detail; the underlying alpha/r identity is the LoRA paper's.)

### LyCORIS: the diffusion adapter family (LoCon conv, LoKr Kronecker, LoHa Hadamard) · `recommended` · ▸ reproduced
**Stable-Diffusion adaptation needs more than attention-only LoRA: LoCon extends the adapter to convolution layers, while LoKr (Kronecker product) and LoHa (Hadamard/low-rank-product) re-parameterize the update for higher expressive capacity at comparable or smaller file size — the canonical diffusion-side PEFT family for style work.**
LyCORIS (Yeh et al. 2023, 'Navigating Text-To-Image Customization: From LyCORIS Fine-Tuning to Model Evaluation') is the library/method family that generalizes LoRA for Stable Diffusion. LoCon applies the low-rank adapter to convolution layers (not just attention), capturing texture/spatial style that attention-only LoRA misses — important because SDXL's U-Net style signal lives heavily in conv blocks. LoKr factorizes the weight update as a Kronecker product, and LoHa as a Hadamard product of two low-rank factors; both increase the expressive capacity reachable per stored parameter relative to a plain rank-r LoRA, trading a different capacity/size curve. For the studio's #1 workload (SDXL/Flux style-LoRA), these are first-class alternatives to vanilla LoRA: LoCon when conv-level style matters, LoKr for compact high-capacity style captures. The same rank/alpha effective-scale coupling (peft theory above) governs them. This is the diffusion counterpart to the LLM-side LoRA/DoRA entries — a genuinely separate adapter space, which is why this lane is MECE across modalities.
- **For the pipeline:** For SDXL/Flux style LoRAs, do not default to attention-only LoRA: evaluate LoCon (conv coverage) and LoKr (compact capacity) as the style-binding adapter. Concrete recipe values (which rank, which alpha, which factor dims) belong in the diffusion-sdxl-lora / diffusion-flux-lora recipe lanes; this entry establishes the method-theory and the module-coverage rationale.
- **Method:** lokr · **Applies to:** diffusion · **Base:** SDXL|Flux · **Kind:** method-theory
- **Tuning budget:** No rig recipe in this lane yet; recipe sweeps live in the diffusion recipe lanes. · **Search:** none
- **Variance:** Method existence, module coverage, and the Kronecker/Hadamard re-parameterizations are source-defined; relative quality vs plain LoRA is workload-dependent and not rig-measured this wave.
- **Validated under:** Diffusion-only (Stable Diffusion family, incl. SDXL). Not an LLM method — the LLM-side analogues are LoRA/DoRA above.
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **conditional** — LyCORIS is Apache-2.0-licensed tooling (permissive); the trained adapter's commercial-cleanliness inherits from the base diffusion model (SDXL-1.0 = clean; FLUX.1-dev = NON-commercial, do not use as a training base — use FLUX.2-klein/Chroma1-HD) and the image dataset. Verify the base before any commercial style LoRA.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | locon / lokr / loha | ● | LoCon = LoRA on conv; LoKr = Kronecker-product update; LoHa = Hadamard/low-rank-product update. |
| rank | per-method capacity knob dim | ● | Same rank/alpha effective-scale coupling as LoRA; LoKr/LoHa reach more capacity per stored param. |
| alpha | set to fix scale | ○ | Effective scale alpha/rank applies to LyCORIS variants too. |
| target_modules | U-Net attention + conv (LoCon) | ○ | LoCon's extension to conv layers is the key delta over attention-only LoRA for style. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Attention-only LoRA fails to capture a style's texture/brushwork | style signal lives in U-Net convolution layers the adapter does not touch. | Use LoCon to extend the adapter to conv layers. | target_modules |
| Need higher style capacity but LoRA file is already large | plain rank-r LoRA's capacity-per-parameter curve is limiting. | Switch to LoKr (Kronecker) for more expressive capacity at comparable/smaller size. | network_type |

- **Best for:** SDXL/Flux style adapter with conv coverage (sdxl, fit 5) ; Compact high-capacity style capture (flux, fit 4)
- **Verify:** verdict=confirmed | currency=Current. LyCORIS is actively maintained (GitHub KohakuBlueleaf/LyCORIS), LoCon/LoKr/LoHa are all available and used with SDXL in 2026. AUTOMATIC1111 v1.5+ has built-in LyCORIS support. | arXiv:2309.14859 confirmed (ICLR 2024). The specific method names LoCon, LoKr, LoHa do not appear in the abstract but are confirmed via the GitHub repo and community sources. The entry correctly identifies this as the canonical diffusion-side PEFT family. No boundary violations — no weight catalog entries, no rig-measured numbers. The claim that LyCORIS covers 'more than attention-only LoRA' via convolution layers is accurate and well-supported.
- **Sources:** [Navigating Text-To-Image Customization: From LyCORIS Fine-Tuning to Model Evaluation](https://arxiv.org/abs/2309.14859) (Shih-Ying Yeh, Yu-Guan Hsieh, Zhidong Gao, Bernard B W Yang, Giyeong Oh, Yanmin Gong, 2023) — LyCORIS (Lora beYond Conventional methods) provides LoCon (LoRA on convolution), LoKr (Kronecker product), and LoHa (Hadamard product) fine-tuning methods for Stable Diffusion, with an accompanying evaluation framework. ; [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) (Edward J. Hu et al., 2021) — The base low-rank-adapter formulation LyCORIS generalizes to convolution and to Kronecker/Hadamard re-parameterizations for diffusion.

### QLoRA: LoRA over a 4-bit NF4 frozen base (NF4 + double-quant + paged optimizers) · `recommended` · ▸ reproduced
**Quantizing the frozen base to 4-bit NormalFloat and backpropagating LoRA adapters through it preserves full 16-bit fine-tuning task performance while collapsing the memory footprint enough to fine-tune a 65B model on a single 48GB GPU.**
QLoRA (Dettmers et al. 2023) is the method that makes the studio's #2 workload — light 24-34B local LLM fine-tuning on one 32GB Blackwell GPU — feasible. Three innovations: (1) 4-bit NormalFloat (NF4), a data type information-theoretically optimal for the normally-distributed pretrained weights, used to store the frozen base; (2) double quantization, which quantizes the quantization constants themselves to shave more memory; (3) paged optimizers, which use NVIDIA unified memory to absorb gradient-checkpointing memory spikes without OOM. The trainable LoRA adapters (BF16) are backpropagated through the frozen 4-bit base. The headline result: 65B fine-tuned on a single 48GB GPU with no loss vs 16-bit, and the resulting Guanaco hitting 99.3% of ChatGPT-level on their eval after 24h on one GPU. As a PEFT-theory entry, the load-bearing point is that adapter training does not require a full-precision base — the base only needs to be a faithful frozen reference, so it can live in 4 bits.
- **For the pipeline:** For 24-34B local fine-tuning on the 5090's 32GB, QLoRA-NF4 is the baseline method; it is what makes the second workload single-GPU-feasible at all. Pair with LoRA+ / rsLoRA (peft theory above) for cheap quality. Inference can then merge or load the adapter against a 4-bit or higher base. Measured it/s and VRAM peaks for the studio's QLoRA runs belong in tensor-engine-knowledge, not here.
- **Method:** qlora · **Applies to:** llm · **Base:** Qwen3|Llama · **Kind:** method-theory
- **Tuning budget:** Source ran extensive scale sweeps (up to 65B); no rig sweep this wave. · **Search:** none
- **Variance:** NF4-matches-16-bit and the 65B/48GB result are the paper's reported measurements across multiple model scales; not re-measured on the studio rig this wave.
- **Validated under:** LLM-only, validated on LLaMA-family up to 65B at 48GB; the 32GB 5090 comfortably covers the studio's 24-34B target band. Diffusion bases are not QLoRA-NF4 targets (different memory regime — fp8 base is the diffusion analogue, owned by the efficiency lane).
- **Base model (model-knowledge):** `qwen3-32b`
- **Output license:** commercial **conditional** — Method imposes no license; commercial-cleanliness of the fine-tuned model inherits from the base weights' license (e.g. Qwen3 Apache-2.0 = clean; check per base) and the SFT dataset. QLoRA itself adds no restriction.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | qlora (LoRA over NF4 base) | ● | BF16 LoRA adapters backpropagated through a 4-bit NF4 frozen base. |
| precision | NF4 base + bf16 adapter | ● | 4-bit NormalFloat for frozen weights; compute/adapters in bf16. + double quantization on the quant constants. |
| optimizer | paged (8-bit) optimizer | ● | Paged optimizer uses unified memory to survive gradient-checkpointing spikes without OOM. |
| target_modules | all linear layers | ○ | QLoRA paper applies LoRA to all linear layers (broader than original q,v) to recover full-FT quality at 4-bit. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| OOM spikes mid-training despite fitting at steady state | gradient-checkpointing memory peaks exceed VRAM at long sequence lengths. | Use a paged optimizer (QLoRA's third innovation) so spikes page to host memory instead of crashing. | optimizer |
| 4-bit fine-tune underperforms 16-bit baseline on task metrics | LoRA applied to too few modules and/or non-NF4 (e.g. fp4/int4) quantization of the base. | Use NF4 (not fp4/int4) for the frozen base and apply LoRA to all linear layers, per the paper's recovery recipe. | target_modules |

- **Best for:** Fine-tune 24-34B LLM on a single 32GB GPU (single-gpu, fit 5) ; First stage of a QLoRA-SFT -> DPO chain (llm, fit 4)
- **Verify:** verdict=confirmed | currency=Current. QLoRA remains the standard single-GPU LLM fine-tuning method. NF4 + double-quant + paged optimizers are still the reference stack. The 65B/48GB benchmark framing is a demonstration of the method ceiling; the technique applies at 24-34B scales on a 32GB RTX 5090 without modification. | arXiv:2305.14314 confirmed: all three innovations (NF4, double quantization, paged optimizers) are present, the 65B/48GB/24h/99.3% Guanaco claim is in the abstract. Evidence strength reproduced-from-source is accurate. No boundary violations — no measured rig numbers stored here, no weight catalog entry.
- **Sources:** [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314) (Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, Luke Zettlemoyer, 2023) — 4-bit NormalFloat + double quantization + paged optimizers let LoRA adapters backprop through a frozen 4-bit base, fine-tuning 65B on a single 48GB GPU while preserving full 16-bit task performance (Guanaco: 99.3% of ChatGPT level, 24h on one GPU). ; [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) (Edward J. Hu et al., 2021) — The frozen-base + trainable low-rank adapter formulation QLoRA quantizes; QLoRA's contribution is making that frozen base 4-bit.

### DoRA: weight-decomposed LoRA (magnitude + direction, LoRA on direction only) · `runner-up` · ▸ reproduced
**Decomposing each pretrained weight into a separately-trained magnitude scalar and a LoRA-adapted direction recovers a learning pattern closer to full fine-tuning, beating plain LoRA on downstream tasks with no added inference cost.**
DoRA (Liu et al. 2024, ICML Oral) refines LoRA by first decomposing the pretrained weight matrix into a magnitude component (a trainable per-column scalar vector) and a directional component (the unit-norm direction). LoRA is then applied only to the directional update, while the magnitude is trained independently. The motivation is an analysis showing full fine-tuning and LoRA exhibit different magnitude/direction update patterns; DoRA's decomposition lets the adapter mimic full-FT behavior more closely, improving both learning capacity and training stability. It consistently outperforms LoRA on LLaMA, LLaVA, and VL-BART across commonsense reasoning, visual-instruction tuning, and image/video-text understanding — and crucially the decomposition folds back into the weights at merge time, so there is no additional inference overhead. Because it is a drop-in directional refinement of LoRA, it applies to diffusion adapters too, though the published validation is LLM/VLM-centric.
- **For the pipeline:** DoRA is a low-cost upgrade path from LoRA when a plain-LoRA run underfits or trains unstably — same inference cost, modestly more train-time params. For the studio: a candidate for both 24-34B LLM tuning and SDXL/Flux style work, but its diffusion benefit is an UNTESTED cross-domain import here (the paper measured LLM/VLM); treat the diffusion claim as community-grade until rig-measured.
- **Method:** dora · **Applies to:** both · **Base:** Llama|SDXL|Flux · **Kind:** method-theory
- **Tuning budget:** Source benchmarked across several model/task families; no rig sweep this wave. · **Search:** none
- **Variance:** Consistent-outperformance-of-LoRA is the paper's multi-benchmark reported result on LLM/VLM; the diffusion applicability is inference, not measured.
- **Validated under:** Validated on LLaMA / LLaVA / VL-BART (LLM + vision-language). Applying DoRA to SDXL/Flux style-LoRA is a cross-domain extrapolation — flagged, not source-measured for diffusion.
- **Base model (model-knowledge):** `qwen3-32b`
- **Output license:** commercial **yes** — Method imposes no license; cleanliness inherits from base + dataset. No inference overhead means no runtime licensing surface either.
- **Fit:** rig 4/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | dora | ● | LoRA on the directional component + a separately-trained magnitude vector. |
| rank | as LoRA dim | ● | Directional adapter is a standard low-rank LoRA; same rank/alpha coupling applies. |
| alpha | as LoRA | ○ | Effective scale alpha/rank carries over to the directional update. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Plain LoRA underfits or trains unstably on a hard task | LoRA's coupled magnitude+direction update diverges from the full-FT learning pattern. | Switch to DoRA so magnitude trains separately from the LoRA-adapted direction; recovers full-FT-like behavior at no inference cost. | network_type |

- **Best for:** Higher-capacity PEFT when LoRA underfits (llm, fit 4) ; Inference-overhead-free adapter for deployment (single-gpu, fit 4)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. DoRA (arXiv:2402.09353, ICML 2024 Oral) is actively being integrated into diffusion training tooling. A version-mismatch bug in stable-diffusion-webui-forge for DoRA + LoCon is a compatibility issue, not a method problem. | Paper confirmed, authors confirmed, ICML 2024 Oral confirmed. The 'no additional inference overhead' claim requires a small qualification: DoRA adds a per-layer magnitude-normalization step relative to plain LoRA, which has a marginal runtime cost. The paper characterizes this as negligible and frames it as equivalent to LoRA inference cost, which is defensible. Recommended fix: add a parenthetical noting the normalization step is present but characterized as negligible in the paper, to avoid overclaiming. The evidence_strength reproduced-from-source is accurate.
- **Sources:** [DoRA: Weight-Decomposed Low-Rank Adaptation](https://arxiv.org/abs/2402.09353) (Shih-Yang Liu, Chien-Yi Wang, Hongxu Yin, Pavlo Molchanov, Yu-Chiang Frank Wang, Kwang-Ting Cheng, Min-Hung Chen, 2024) — Decomposes pretrained weights into magnitude and direction, applies LoRA to the directional update; consistently outperforms LoRA on LLaMA/LLaVA/VL-BART across commonsense reasoning + visual instruction tuning with no additional inference overhead (ICML 2024 Oral). ; [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) (Edward J. Hu et al., 2021) — The base low-rank-adapter method DoRA decomposes and refines.

### Ostris train_lora_qwen_image_24gb.yaml (sourced 24GB path) · `recommended` · docs
**Sourced Ostris 24GB-class Qwen-Image LoRA YAML: linear/alpha 16, adamw8bit, lr 1e-4, qtype uint3, low_vram — copy values only.**
STUDY-034 Practitioner Verifier ✅. Recipes invented: 0. Do not invent other ranks/LRs.
- **For the pipeline:** STUDY-034 Verifier ✅. Recipes invented: 0. Copy Ostris YAML values only where present.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** recipe
- **Output license:** commercial **check** — STUDY-034 deepen; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| linear | 16 | ● | Ostris YAML sourced — do not invent other ranks |
| linear_alpha | 16 | ● | Ostris YAML sourced |
| optimizer | adamw8bit | ● | Ostris YAML sourced |
| lr | 1e-4 | ● | Ostris YAML sourced — do not invent other LRs |
| qtype | uint3 | ● | Ostris YAML sourced |
| low_vram | true | ● | Ostris YAML sourced |
| cache_text_embeddings | true | ○ | Ostris YAML sourced (required for 24GB on page) |
| gradient_checkpointing | true | ○ | Ostris YAML sourced |

- **Sources:** [Ostris AI Toolkit README](https://github.com/ostris/ai-toolkit) — Consumer-GPU diffusion LoRA suite; YAML train path. ; [train_lora_qwen_image_24gb.yaml](https://github.com/ostris/ai-toolkit/blob/main/config/examples/train_lora_qwen_image_24gb.yaml) — linear/linear_alpha 16; adamw8bit; lr 1e-4; qtype uint3; low_vram true.

### Adapter/model merging: TIES (trim+elect-sign+merge) and DARE (drop+rescale) · `situational` · ▸ reproduced
**Multiple task/style adapters or fine-tunes of the same base can be combined into one model without retraining by first resolving delta-parameter interference — TIES trims small deltas and elects a consensus sign; DARE shows 90-99% of deltas can be dropped and the rest rescaled by 1/(1-p) with no performance loss.**
Merging is the PEFT-adjacent operation for combining homologous fine-tunes (same base) into one model. Naive weight averaging suffers interference: TIES-Merging (Yadav et al. 2023, NeurIPS) attributes this to (a) redundant parameter values and (b) sign disagreement across models, and fixes it in three steps — Trim (reset deltas that barely changed during fine-tuning), Elect Sign (pick the dominant sign per parameter across models), and Disjoint Merge (average only the deltas agreeing with the elected sign). DARE (Yu et al. 2023, 'Language Models are Super Mario', ICML 2024) is complementary: it shows fine-tuned delta parameters are extremely redundant (values typically within 0.002) and that randomly dropping a fraction p (90% or even 99%) of deltas and rescaling survivors by 1/(1-p) preserves performance and preserves the parameter distribution — so DARE is a sparsification pre-step that feeds TIES or task-arithmetic merging, sometimes yielding a merge that surpasses every source model. Both operate on delta parameters, so they apply directly to merged LoRA adapters and full fine-tunes of a shared base.
- **For the pipeline:** For the studio's LLM side, merging lets one base host several capability/persona fine-tunes without serving N adapters: DARE-sparsify each delta, then TIES-merge. Diffusion LoRA merging exists in practice (kohya merge tools) but DARE/TIES were validated on LLMs — treat diffusion adapter merging as a separate, lighter-evidence path. Requires homologous bases (same pretrained weights); cross-base merges are out of scope.
- **Method:** lora · **Applies to:** llm · **Base:** Llama|Qwen3 · **Kind:** method-theory
- **Tuning budget:** Drop rate p and trim threshold are the tunable knobs; sources swept them, no rig sweep this wave. · **Search:** none
- **Variance:** The 90-99%-droppable and sign-interference results are the papers' reported multi-model findings; not rig-measured here. 'Surpasses sources' is conditional, not guaranteed.
- **Validated under:** Validated on LLM fine-tunes of a shared base (homologous models required). LoRA-adapter merging is a direct corollary (deltas are low-rank). Diffusion-adapter merging is a community-grade extrapolation, flagged.
- **Base model (model-knowledge):** `qwen3-32b`
- **Output license:** commercial **conditional** — Merging is a method; the merged model's license is the (shared) base's license plus every contributing dataset's terms — a merge can only be as clean as its dirtiest input. Verify all sources, not just the base.
- **Fit:** rig 3/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| loss_type | ties (trim+elect-sign+disjoint-merge) | ○ | TIES merge operator; resolves redundancy + sign interference. |
| loss_type | dare (drop p + rescale 1/(1-p)) | ○ | DARE sparsification pre-step; p typically 0.9-0.99. |
| loss_type | dare_ties (DARE then TIES) | ○ | Common composition: DARE-sparsify each delta, then TIES-merge. |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Merged model is worse than any single source model | naive averaging lets redundant deltas and opposing signs cancel useful updates. | Use TIES: trim small deltas, elect a consensus sign, merge only sign-agreeing deltas. | loss_type |
| Too many overlapping deltas make a multi-model merge mushy | delta parameters are extremely redundant, so summed deltas over-interfere. | DARE-sparsify each delta (drop 90-99%, rescale by 1/(1-p)) before merging. | loss_type |

- **Best for:** Combine multiple LLM fine-tunes into one served model (llm, fit 4)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. TIES (NeurIPS 2023) and DARE (ICML 2024) are both integrated into HuggingFace PEFT and Diffusers, with documented support for SDXL LoRA adapter merging as of 2025. | Both papers confirmed: TIES arXiv:2306.01708 at NeurIPS 2023, DARE arXiv:2311.03099 at ICML 2024. All author lists and venue claims check out. One missing flag: both TIES and DARE were developed and evaluated on LLM weight deltas. Their application to diffusion LoRA adapters is a cross-domain transfer that should be flagged per the boundary discipline rules ('cross-domain imports must be flagged in the note and tagged no higher than community-claim unless separately sourced'). The HuggingFace Diffusers integration and ComfyUI-DareMerge existence confirm the transfer works in practice, but the evidence_strength should be downgraded from reproduced-from-source to community-claim for the diffusion-specific application, or a note should explicitly flag 'LLM-origin method, diffusion transfer confirmed via HuggingFace Diffusers integration.' Recommended fix: add a cross-domain flag in the note for the diffusion application path.
- **Sources:** [TIES-Merging: Resolving Interference When Merging Models](https://arxiv.org/abs/2306.01708) (Prateek Yadav, Derek Tam, Leshem Choshen, Colin Raffel, Mohit Bansal, 2023) — Merges task-specific models in three steps — reset small-magnitude deltas, resolve sign conflicts by electing a consensus sign, and merge only sign-aligned parameters — addressing interference from redundant values and sign disagreement (NeurIPS 2023). ; [Language Models are Super Mario: Absorbing Abilities from Homologous Models as a Free Lunch (DARE)](https://arxiv.org/abs/2311.03099) (Le Yu, Bowen Yu, Haiyang Yu, Fei Huang, Yongbin Li, 2023) — Delta parameters are extremely redundant (values within ~0.002); DARE drops 90-99% of them and rescales survivors by 1/(1-p) with no performance loss, enabling merges of homologous models that can surpass any source (ICML 2024).

### A Rank Stabilization Scaling Factor for Fine-Tuning with LoRA · `situational` · paper
****rsLoRA**: scale by α/√r (vs α/r) so higher ranks remain trainable — rank-scaling honesty for single-GPU PEFT (no invent concrete r).**
STUDY-054 deepen — **rsLoRA**: scale by α/√r (vs α/r) so higher ranks remain trainable — rank-scaling honesty for single-GPU PEFT (no invent concrete r). Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [A Rank Stabilization Scaling Factor for Fine-Tuning with LoRA](https://arxiv.org/abs/2312.03732) — **rsLoRA**: scale by α/√r (vs α/r) so higher ranks remain trainable — rank-scaling honesty for single-GPU PEFT (no invent concrete r).

### A Unified Study of LoRA Variants: Taxonomy, Review, Codebase, and Empirical Evaluation · `situational` · paper
**Taxonomy along rank / optimization / init / MoE axes + LoRAFactory codebase — map of PEFT variants beyond STUDY-034’s eight without inventing fixed-r schedules.**
STUDY-054 deepen — Taxonomy along rank / optimization / init / MoE axes + LoRAFactory codebase — map of PEFT variants beyond STUDY-034’s eight without inventing fixed-r schedules. Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [A Unified Study of LoRA Variants: Taxonomy, Review, Codebase, and Empirical Eval](https://arxiv.org/abs/2601.22708) — Taxonomy along rank / optimization / init / MoE axes + LoRAFactory codebase — map of PEFT variants beyond STUDY-034’s eight without inventing fixed-r schedules.

### AdaLoRA adaptive rank budget (Zhang et al. 2023) · `situational` · paper
**Dynamic singular-value importance pruning reallocates rank budget — not a fixed-r recipe invent.**
STUDY-034 Scholar deepen — AdaLoRA (2303.10512). Recipes invented: 0.
- **For the pipeline:** STUDY-034 Verifier ✅. Recipes invented: 0. Copy Ostris YAML values only where present.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-034 deepen; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** OPERATOR PRISM ACCEPT PRISM-ACCEPT-P2 (arXiv 2303.10512 AdaLoRA)
- **Sources:** [AdaLoRA](https://arxiv.org/abs/2303.10512) — Adaptive budget allocation for PEFT.

### Kustomize kustomization overlays · `situational` · paper
**Analog: declare diffs over a base; don’t silently rewrite. Holds for documenting 32GB deltas only when sourced — else keep 24GB path labeled. Limit: K8s overlays ≠ Ostris job schema.**
STUDY-054 deepen — Analog: declare diffs over a base; don’t silently rewrite. Holds for documenting 32GB deltas only when sourced — else keep 24GB path labeled. Limit: K8s overlay Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [Kustomize kustomization overlays](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/) — Analog: declare diffs over a base; don’t silently rewrite. Holds for documenting 32GB deltas only when sourced — else keep 24GB path labeled. Limit: K8s overlays ≠ Ostris job schema.

### Learning Rate Matters — LoRA LR retuning · `situational` · paper
**Across LoRA variants and ranks, accuracy gaps collapse under LR sweeps; advanced variants need different LR bands than vanilla LoRA — rank claims without LR retuning are not load-bearing.**
Across LoRA variants and ranks, accuracy gaps collapse under LR sweeps; advanced variants need different LR bands than vanilla LoRA — rank claims without LR retuning are not load-bearing.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not invent recipes. Do not flip technique rows.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0. Invented recipes: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Learning Rate Matters — LoRA LR retuning](https://arxiv.org/abs/2602.04998) — Across LoRA variants and ranks, accuracy gaps collapse under LR sweeps; advanced variants need different LR bands than vanilla LoRA — rank claims without LR retuning are not load-bearing.

### Learning Rate Matters: Vanilla LoRA May Suffice for LLM Fine-tuning · `situational` · paper
**Across LoRA variants, accuracy gaps collapse under proper LR sweeps; advanced variants need different LR ranges — LR-first honesty vs crowning a new rank recipe (no invent studio LR).**
STUDY-054 deepen — Across LoRA variants, accuracy gaps collapse under proper LR sweeps; advanced variants need different LR ranges — LR-first honesty vs crowning a new rank recipe Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [Learning Rate Matters: Vanilla LoRA May Suffice for LLM Fine-tuning](https://arxiv.org/abs/2602.04998) — Across LoRA variants, accuracy gaps collapse under proper LR sweeps; advanced variants need different LR ranges — LR-first honesty vs crowning a new rank recipe (no invent studio LR).

### LoFT — LoRA that behaves like full fine-tuning · `situational` · paper
**Aligns optimizer internal moments so low-rank updates behave closer to full fine-tuning; evaluated vs LoRA/DoRA. Do not invent recipes.**
Aligns optimizer internal moments so low-rank updates behave closer to full fine-tuning; evaluated vs LoRA/DoRA. Do not invent recipes.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not invent recipes. Do not flip technique rows.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0. Invented recipes: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [LoFT — LoRA that behaves like full fine-tuning](https://arxiv.org/abs/2505.21289) — Aligns optimizer internal moments so low-rank updates behave closer to full fine-tuning; evaluated vs LoRA/DoRA. Do not invent recipes.

### LoFT: Low-Rank Adaptation That Behaves Like Full Fine-Tuning · `situational` · paper
**Aligns optimizer internal moments so low-rank updates behave closer to full FT — PEFT–FT gap craft without inventing studio hyperparameters.**
STUDY-054 deepen — Aligns optimizer internal moments so low-rank updates behave closer to full FT — PEFT–FT gap craft without inventing studio hyperparameters. Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [LoFT: Low-Rank Adaptation That Behaves Like Full Fine-Tuning](https://arxiv.org/abs/2505.21289) — Aligns optimizer internal moments so low-rank updates behave closer to full FT — PEFT–FT gap craft without inventing studio hyperparameters.

### LoRA Dropout as a Sparsity Regularizer for Overfitting Control · `situational` · paper
**Dropout noise on low-rank matrices as sparsity regularizer; also applies with AdaLoRA — overfitting-control PEFT craft for small single-GPU sets (no invent dropout rates as studio recipe).**
STUDY-054 deepen — Dropout noise on low-rank matrices as sparsity regularizer; also applies with AdaLoRA — overfitting-control PEFT craft for small single-GPU sets (no invent drop Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [LoRA Dropout as a Sparsity Regularizer for Overfitting Control](https://arxiv.org/abs/2404.09610) — Dropout noise on low-rank matrices as sparsity regularizer; also applies with AdaLoRA — overfitting-control PEFT craft for small single-GPU sets (no invent dropout rates as studio recipe).

### LoRA learns less and forgets less (Biderman et al. 2024) · `situational` · paper
**LoRA underfits vs full FT but forgets less — plasticity/stability trade; no recipe invent.**
STUDY-034 Scholar deepen — 2405.09673. Recipes invented: 0.
- **For the pipeline:** STUDY-034 Verifier ✅. Recipes invented: 0. Copy Ostris YAML values only where present.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-034 deepen; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [LoRA Learns Less and Forgets Less](https://arxiv.org/abs/2405.09673) — LoRA underfits and forgets less vs full FT.

### LoRA+ asymmetric learning rates (Hayou et al. 2024) · `situational` · paper
**Asymmetric LRs for A vs B stabilize/accelerate LoRA — LR-as-first-class PEFT knob; no studio schedule invent.**
STUDY-034 Scholar deepen — LoRA+ (2402.12354). Recipes invented: 0.
- **For the pipeline:** STUDY-034 Verifier ✅. Recipes invented: 0. Copy Ostris YAML values only where present.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-034 deepen; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [LoRA+](https://arxiv.org/abs/2402.12354) — Asymmetric LR for LoRA A/B matrices.

### LoRA-GA: Low-Rank Adaptation with Gradient Approximation · `situational` · paper
**SVD-on-gradient initialization aligning BA gradients with full-weight gradients — init-axis PEFT peer to PiSSA without inventing ranks.**
STUDY-054 deepen — SVD-on-gradient initialization aligning BA gradients with full-weight gradients — init-axis PEFT peer to PiSSA without inventing ranks. Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [LoRA-GA: Low-Rank Adaptation with Gradient Approximation](https://arxiv.org/abs/2407.05000) — SVD-on-gradient initialization aligning BA gradients with full-weight gradients — init-axis PEFT peer to PiSSA without inventing ranks.

### LoRA-Pro: Are Low-Rank Adapters Properly Optimized? · `situational` · paper
**Adjusts LoRA matrix gradients so the implied low-rank update better approximates full-FT gradients — optimization-process PEFT deepen beyond LoRA+.**
STUDY-054 deepen — Adjusts LoRA matrix gradients so the implied low-rank update better approximates full-FT gradients — optimization-process PEFT deepen beyond LoRA+. Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [LoRA-Pro: Are Low-Rank Adapters Properly Optimized?](https://arxiv.org/abs/2407.18242) — Adjusts LoRA matrix gradients so the implied low-rank update better approximates full-FT gradients — optimization-process PEFT deepen beyond LoRA+.

### PEFT LoRA conceptual guide (`LoraConfig` r / `lora_alpha`) · `situational` · paper
**Analog: rank/alpha are coupled scaling knobs (`alpha/r` or RSLoRA). Holds for **PEFT inheritance limits** — change only with measured/docs source. Limit: HF PEFT ≠ Ostris YAML keys.**
STUDY-054 deepen — Analog: rank/alpha are coupled scaling knobs (`alpha/r` or RSLoRA). Holds for **PEFT inheritance limits** — change only with measured/docs source. Limit: HF PEF Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [PEFT LoRA conceptual guide (`LoraConfig` r / `lora_alpha`)](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora) — Analog: rank/alpha are coupled scaling knobs (`alpha/r` or RSLoRA). Holds for **PEFT inheritance limits** — change only with measured/docs source. Limit: HF PEFT ≠ Ostris YAML keys.

### PEFT LoraConfig package ref · `situational` · paper
**Usage example `r=16`, `lora_alpha=16`; API defaults `r: int = 8`, `lora_alpha: int = 8`; LoRA-FA sample `r=128`, `lora_alpha=32`, `lr=7e-5`.**
STUDY-054 deepen — Usage example `r=16`, `lora_alpha=16`; API defaults `r: int = 8`, `lora_alpha: int = 8`; LoRA-FA sample `r=128`, `lora_alpha=32`, `lr=7e-5`. Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [PEFT LoraConfig package ref](https://huggingface.co/docs/peft/main/en/package_reference/lora) — Usage example `r=16`, `lora_alpha=16`; API defaults `r: int = 8`, `lora_alpha: int = 8`; LoRA-FA sample `r=128`, `lora_alpha=32`, `lr=7e-5`.

### PiSSA principal-subspace adapter init (Meng et al. 2024) · `situational` · paper
**SVD principal-subspace init of adapters vs random LoRA init — initialization axis; no fixed-r invent.**
STUDY-034 Scholar deepen — PiSSA (2404.02948). Recipes invented: 0.
- **For the pipeline:** STUDY-034 Verifier ✅. Recipes invented: 0. Copy Ostris YAML values only where present.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-034 deepen; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [PiSSA](https://arxiv.org/abs/2404.02948) — Principal singular subspace adapter init.

### Semantic Versioning 2.0.0 · `situational` · paper
**Analog: MAJOR/incompatible change must be explicit. Holds: retargeting a **24GB** YAML to **32GB** without a sourced overlay is a silent incompatible claim. Limit: SemVer ≠ trainer CLI flags.**
STUDY-054 deepen — Analog: MAJOR/incompatible change must be explicit. Holds: retargeting a **24GB** YAML to **32GB** without a sourced overlay is a silent incompatible claim. Lim Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [Semantic Versioning 2.0.0](https://semver.org/) — Analog: MAJOR/incompatible change must be explicit. Holds: retargeting a **24GB** YAML to **32GB** without a sourced overlay is a silent incompatible claim. Limit: SemVer ≠ trainer CLI flags.

### TsqLoRA — sensitivity and quality LoRA · `situational` · paper
**Couples quality-aware data sampling with sensitivity-guided dynamic rank allocation; PEFT that ignores data informativeness underperforms at low rank/low data.**
Couples quality-aware data sampling with sensitivity-guided dynamic rank allocation; PEFT that ignores data informativeness underperforms at low rank/low data.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not invent recipes. Do not flip technique rows.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0. Invented recipes: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [TsqLoRA — sensitivity and quality LoRA](https://arxiv.org/abs/2509.18585) — Couples quality-aware data sampling with sensitivity-guided dynamic rank allocation; PEFT that ignores data informativeness underperforms at low rank/low data.

### TsqLoRA: Towards Sensitivity and Quality Low-Rank Adaptation for Efficient Fine-Tuning · `situational` · paper
**Quality-aware data sampling + **sensitivity-guided dynamic rank** per layer — adaptive-rank PEFT craft (not a fixed 5090 r invent).**
STUDY-054 deepen — Quality-aware data sampling + **sensitivity-guided dynamic rank** per layer — adaptive-rank PEFT craft (not a fixed 5090 r invent). Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [TsqLoRA: Towards Sensitivity and Quality Low-Rank Adaptation for Efficient Fine-](https://arxiv.org/abs/2509.18585) — Quality-aware data sampling + **sensitivity-guided dynamic rank** per layer — adaptive-rank PEFT craft (not a fixed 5090 r invent).

### Twelve-Factor App III. Config · `situational` · paper
**Analog: config is source of truth, separated from code/folklore. Holds for Ostris YAML-as-SoT over chat “try rank 64” advice. Limit: 12factor env config ≠ diffusion LoRA graph.**
STUDY-054 deepen — Analog: config is source of truth, separated from code/folklore. Holds for Ostris YAML-as-SoT over chat “try rank 64” advice. Limit: 12factor env config ≠ diffu Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 Analogist #1 UNVERIFIED — do not land as verified; recipes invented: 0
- **Sources:** [Twelve-Factor App III. Config](https://12factor.net/config) — Analog: config is source of truth, separated from code/folklore. Holds for Ostris YAML-as-SoT over chat “try rank 64” advice. Limit: 12factor env config ≠ diffusion LoRA graph.

### Unified Study of LoRA Variants — taxonomy · `situational` · paper
**Unified taxonomy (rank-adjust / optimization-adjust / init-adjust / MoE-integration) plus shared codebase consolidating AdaLoRA, LoRA+, PiSSA, LoRA-GA peers. No new technique invent beyond catalog.**
Unified taxonomy (rank-adjust / optimization-adjust / init-adjust / MoE-integration) plus shared codebase consolidating AdaLoRA, LoRA+, PiSSA, LoRA-GA peers. No new technique invent beyond catalog.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not invent recipes. Do not flip technique rows.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0. Invented recipes: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Unified Study of LoRA Variants — taxonomy](https://arxiv.org/abs/2601.22708) — Unified taxonomy (rank-adjust / optimization-adjust / init-adjust / MoE-integration) plus shared codebase consolidating AdaLoRA, LoRA+, PiSSA, LoRA-GA peers. No new technique invent beyond catalog.

### Unsloth LoRA Hyperparameters Guide · `situational` · paper
**Table: LoRA Rank **8, 16, 32, 64, 128** (“Choose 16 or 32”); normal LoRA/QLoRA LR start **`2e-4`**; alpha = `r` or `r*2`.**
STUDY-054 deepen — Table: LoRA Rank **8, 16, 32, 64, 128** (“Choose 16 or 32”); normal LoRA/QLoRA LR start **`2e-4`**; alpha = `r` or `r*2`. Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [Unsloth LoRA Hyperparameters Guide](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide) — Table: LoRA Rank **8, 16, 32, 64, 128** (“Choose 16 or 32”); normal LoRA/QLoRA LR start **`2e-4`**; alpha = `r` or `r*2`.

### VeRA vector-based random matrix adaptation (Kopiczko et al. 2023) · `situational` · paper
**Frozen shared random matrices + tiny trainable vectors; extreme PEFT memory lane; no rank invent.**
STUDY-034 Scholar deepen — VeRA (2310.11454). Recipes invented: 0.
- **For the pipeline:** STUDY-034 Verifier ✅. Recipes invented: 0. Copy Ostris YAML values only where present.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-034 deepen; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [VeRA](https://arxiv.org/abs/2310.11454) — Vector-based random matrix adaptation.

### What Happens to the License When You Fine‑Tune a Model · `situational` · paper
**Analog: LoRA adapters inherit base license. Holds for PEFT inheritance audit on commercial bases. Limit: commentary ≠ inventing hparams.**
STUDY-054 deepen — Analog: LoRA adapters inherit base license. Holds for PEFT inheritance audit on commercial bases. Limit: commentary ≠ inventing hparams. Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [What Happens to the License When You Fine‑Tune a Model](https://wcr.legal/fine-tuned-model-license/) — Analog: LoRA adapters inherit base license. Holds for PEFT inheritance audit on commercial bases. Limit: commentary ≠ inventing hparams.

### `train_lora_qwen_image_24gb.yaml` · `situational` · paper
**Analog: named 24GB example pins `linear`/`linear_alpha` 16, `adamw8bit`, `uint3`, `low_vram`, cache TE. Holds: cite this file only; **do not invent 5090 ranks**. Limit: filename is 24GB-class — not a silent 32GB recipe.**
STUDY-054 deepen — Analog: named 24GB example pins `linear`/`linear_alpha` 16, `adamw8bit`, `uint3`, `low_vram`, cache TE. Holds: cite this file only; **do not invent 5090 ranks** Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [`train_lora_qwen_image_24gb.yaml`](https://github.com/ostris/ai-toolkit/blob/main/config/examples/train_lora_qwen_image_24gb.yaml) — Analog: named 24GB example pins `linear`/`linear_alpha` 16, `adamw8bit`, `uint3`, `low_vram`, cache TE. Holds: cite this file only; **do not invent 5090 ranks**. Limit: filename is 24GB-class — not a

### kohya train_network.md · `situational` · paper
**Example `--network_dim=16`, `--network_alpha=1`, `--learning_rate=1e-4`, `--optimizer_type="AdamW8bit"`; dim commonly 4–128 (page range, not a recipe invent).**
STUDY-054 deepen — Example `--network_dim=16`, `--network_alpha=1`, `--learning_rate=1e-4`, `--optimizer_type="AdamW8bit"`; dim commonly 4–128 (page range, not a recipe invent). Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [kohya train_network.md](https://github.com/kohya-ss/sd-scripts/blob/main/docs/train_network.md) — Example `--network_dim=16`, `--network_alpha=1`, `--learning_rate=1e-4`, `--optimizer_type="AdamW8bit"`; dim commonly 4–128 (page range, not a recipe invent).

### train_lora_chroma_24gb.yaml · `situational` · paper
**`linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `arch: chroma`, `quantize: true`.**
STUDY-054 deepen — `linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `arch: chroma`, `quantize: true`. Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [train_lora_chroma_24gb.yaml](https://github.com/ostris/ai-toolkit/blob/main/config/examples/train_lora_chroma_24gb.yaml) — `linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `arch: chroma`, `quantize: true`.

### train_lora_flex_24gb.yaml · `situational` · paper
**`linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `bypass_guidance_embedding: true`.**
STUDY-054 deepen — `linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `bypass_guidance_embedding: true`. Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [train_lora_flex_24gb.yaml](https://github.com/ostris/ai-toolkit/blob/main/config/examples/train_lora_flex_24gb.yaml) — `linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `bypass_guidance_embedding: true`.

### train_lora_flux_24gb.yaml · `situational` · paper
**`linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `adamw8bit`, `quantize: true` (8bit MP).**
STUDY-054 deepen — `linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `adamw8bit`, `quantize: true` (8bit MP). Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [train_lora_flux_24gb.yaml](https://github.com/ostris/ai-toolkit/blob/main/config/examples/train_lora_flux_24gb.yaml) — `linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `adamw8bit`, `quantize: true` (8bit MP).

### train_lora_qwen_image_edit_32gb.yaml · `situational` · paper
**`linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `adamw8bit`; comments: **caching text embeddings required for 32GB**, **3bit (`uint3|…`) required for 32GB**, `low_vram: true`.**
STUDY-054 deepen — `linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `adamw8bit`; comments: **caching text embeddings required for 32GB**, **3bit (`uint3|…`) required for 32GB**, `low Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [train_lora_qwen_image_edit_32gb.yaml](https://github.com/ostris/ai-toolkit/blob/main/config/examples/train_lora_qwen_image_edit_32gb.yaml) — `linear: 16`, `linear_alpha: 16`, `lr: 1e-4`, `adamw8bit`; comments: **caching text embeddings required for 32GB**, **3bit (`uint3/…`) required for 32GB**, `low_vram: true`.

### train_lora_wan22_14b_24gb.yaml · `situational` · paper
**`linear: 32`, `linear_alpha: 32`, `lr: 1e-4`, `weight_decay: 1e-4`; `cache_text_embeddings: true` + `low_vram` / `uint4|…ARA` for 24GB-class path.**
STUDY-054 deepen — `linear: 32`, `linear_alpha: 32`, `lr: 1e-4`, `weight_decay: 1e-4`; `cache_text_embeddings: true` + `low_vram` / `uint4|…ARA` for 24GB-class path. Recipes invented: 0.
- **For the pipeline:** STUDY-054. Recipes invented: 0. Cite Ostris YAML / PEFT on-page ranks only. Do not invent 5090 ranks.
- **Method:** lora · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-054 deepen; recipes invented: 0.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-054 deepen; recipes invented: 0; Analogist #1 unverified if present
- **Sources:** [train_lora_wan22_14b_24gb.yaml](https://github.com/ostris/ai-toolkit/blob/main/config/examples/train_lora_wan22_14b_24gb.yaml) — `linear: 32`, `linear_alpha: 32`, `lr: 1e-4`, `weight_decay: 1e-4`; `cache_text_embeddings: true` + `low_vram` / `uint4/…ARA` for 24GB-class path.

