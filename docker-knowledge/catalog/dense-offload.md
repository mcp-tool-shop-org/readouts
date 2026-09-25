# Dense-model offload envelope
_Partial RAM/NVMe offload throughput, the latency-vs-throughput tension, the sub-1-tok/s refusal cliff_ · wave 9 · 2026-09-07 · [‹ catalog index](README.md)

1 findings · 1 load-bearing · 1 verified.

| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |
|------|---------|-------|--------|------------|------|---|
| benchmark | Dense offload tiers off a cliff; NVMe spill is sub-1 tok/s | Single-stream dense decode falls roughly linearly with RAM offload and collapses below 1 tok/s once weights stream from NVMe. | 150 tok/s VRAM -> 3-6 tok/s 70B RAM-offload -> sub-1 tok/s NVMe | dense; nvme | ●●● | ✓ |

## Detail

### Dense offload tiers off a cliff; NVMe spill is sub-1 tok/s · `load-bearing` · benchmark
**Single-stream dense decode falls roughly linearly with RAM offload and collapses below 1 tok/s once weights stream from NVMe.**
~150 tok/s fully in VRAM (8B int4) -> ~60-70% at 20/32 layers on GPU -> ~3-6 tok/s for 70B on DDR5 partial offload -> sub-1 tok/s once dense weights stream from NVMe (AirLLM: 0.7 tok/s down to ~1 token/hour). The seminal offload wins are throughput-at-large-batch, explicitly 'not suitable for latency sensitive' (FlexGen 1 tok/s on OPT-175B at batch 144; ZeRO-Inference OPT-30B 43 tok/s CPU vs 30 tok/s NVMe, aggregate).
- **Applies to:** dense; nvme · **Metric:** 150 tok/s VRAM -> 3-6 tok/s 70B RAM-offload -> sub-1 tok/s NVMe · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Calibration #3: RAM-offload partial is the serviceable dense envelope; reserve NVMe for cold MoE experts, NOT dense weights (dense has no sparsity to exploit).
- **Verify:** verdict=confirmed-with-fixes | FlexGen/ZeRO-Inference verbatim; AirLLM tok/s figures community-sourced not repo (PARTIAL); localllm.in DROPPED (page was about different models); bmdpat 60-70%@20/32 verbatim.
- **Sources:** [AirLLM (70B inference on a 4GB GPU via layer-by-layer disk streaming)](https://github.com/lyogavin/airllm) — lyogavin 2024; sub-1 tok/s; PARTIAL ; [ZeRO-Inference: Democratizing massive model inference (DeepSpeed)](https://www.deepspeed.ai/2022/09/09/zero-inference.html) — Microsoft DeepSpeed 2022; 43/30 tok/s aggregate; SUPPORTED ; [FlexGen (single-stream vs aggregate tension)](https://arxiv.org/abs/2303.06865) — Sheng et al. 2023; 1 tok/s @ batch 144; SUPPORTED

