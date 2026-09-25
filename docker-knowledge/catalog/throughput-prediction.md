# Throughput & memory prediction
_KV/weight memory math (closed-form), roofline + measured calibration, prediction error bands, the receipt_ · wave 9 · 2026-09-07 · [‹ catalog index](README.md)

3 findings · 1 load-bearing · 1 verified.

| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |
|------|---------|-------|--------|------------|------|---|
| craft | Jarmusch — Blackwell CUDA 12.8 / PTX 8.7 | CUDA 12.8 / PTX 8.7 unlock Blackwell 5th-gen tensor ops — toolkit currency gates compute. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | Yadav — sm_100 ≠ sm_120 | B200/sm_100 and RTX PRO 6000/sm_120 stacks use CUDA 12.8+; sm_120 ≠ sm_100. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| method | Memory is exact; throughput prediction splits by offload regime | KV/weight memory is closed-form; throughput is predictable to ~10% in-VRAM but only ~1.5-2x under heavy NVMe offload. | 3.33% P95 in-VRAM (Vidur); 80% target-hit (LLM-Pilot); roofline insufficient w/o calibration | all; nvme | ●●● | ✓ |

## Detail

### Jarmusch — Blackwell CUDA 12.8 / PTX 8.7 · `directional` · craft
**CUDA 12.8 / PTX 8.7 unlock Blackwell 5th-gen tensor ops — toolkit currency gates compute.**
CUDA 12.8 / PTX 8.7 unlock Blackwell 5th-gen tensor ops — toolkit currency gates compute.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Blackwell needs CUDA≥12.8.
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [Jarmusch — Blackwell CUDA 12.8 / PTX 8.7](https://arxiv.org/abs/2507.10789) — Jarmusch et al. 2025; SUPPORTED

### Yadav — sm_100 ≠ sm_120 · `directional` · craft
**B200/sm_100 and RTX PRO 6000/sm_120 stacks use CUDA 12.8+; sm_120 ≠ sm_100.**
B200/sm_100 and RTX PRO 6000/sm_120 stacks use CUDA 12.8+; sm_120 ≠ sm_100.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [Yadav — sm_100 ≠ sm_120](https://arxiv.org/abs/2604.23466) — Yadav et al. 2026; SUPPORTED

### Memory is exact; throughput prediction splits by offload regime · `load-bearing` · method
**KV/weight memory is closed-form; throughput is predictable to ~10% in-VRAM but only ~1.5-2x under heavy NVMe offload.**
KV-cache is closed-form/linear in context (NVIDIA). In-VRAM, Vidur predicts P95 latency within 3.33%. Under heavy offload, static analytical prediction is documented insufficient: roofline over-predicts and needs measured calibration (Imai 2024); FlexGen's own LP 'can run out of memory' and is 'beaten by tuning manually'; LLM-Pilot (a learned predictor) meets its target only 80% of the time; NVMe random QD1-4 is far below sequential, so a sequential assumption over-predicts decode by multiples.
- **Applies to:** all; nvme · **Metric:** 3.33% P95 in-VRAM (Vidur); 80% target-hit (LLM-Pilot); roofline insufficient w/o calibration · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Calibration #2: guarantee the +/-10% receipt only for in-VRAM/light-offload; label heavy-NVMe plans 'estimated, receipt-confirmed'; make refusal conservative; the receipt->recalibration loop is load-bearing.
- **Verify:** verdict=confirmed-with-fixes | Vidur/FlexGen/LLM-Pilot/NVIDIA confirmed verbatim; FlexGen 'LP variables' count corrected 9->11; Imai exact quote treated as paraphrase.
- **Sources:** [Vidur: A Large-Scale Simulation Framework for LLM Inference](https://arxiv.org/abs/2405.05465) — Agrawal et al. 2024; P95 within 3.33%; SUPPORTED ; [FlexGen: High-Throughput Generative Inference with a Single GPU](https://arxiv.org/abs/2303.06865) — Sheng et al. 2023; LP is guidance, not guarantee; SUPPORTED ; [LLM-Pilot: Characterize and Optimize Performance of your LLM Inference Services](https://arxiv.org/abs/2410.02425) — Lazuka et al. (IBM) 2024; 80% target-hit; SUPPORTED ; [Mastering LLM Techniques: Inference Optimization (NVIDIA)](https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/) — NVIDIA 2023; closed-form, linear; SUPPORTED

