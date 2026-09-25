# Honest refusal & receipts
_The >1 tok/s floor, contrastive refusal framing, the measured-receipt -> recalibration loop_ · wave 9 · 2026-09-07 · [‹ catalog index](README.md)

2 findings · 1 load-bearing · 1 verified.

| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |
|------|---------|-------|--------|------------|------|---|
| analog | DGX Spark UMA∉memcg — fail isolation honesty | UMA memory not accounted like discrete memcg — fail isolation honesty; do not claim cgroup OOM equals CUDA OOM. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| policy | The >1 tok/s floor is correct and will refuse dense+NVMe often | A >1 tok/s decode floor is well-justified; for dense models spilling to NVMe it will (correctly) refuse frequently. | floor = >1 tok/s decode | dense; nvme; all | ●●● | ✓ |

## Detail

### DGX Spark UMA∉memcg — fail isolation honesty · `directional` · analog
**UMA memory not accounted like discrete memcg — fail isolation honesty; do not claim cgroup OOM equals CUDA OOM.**
UMA memory not accounted like discrete memcg — fail isolation honesty; do not claim cgroup OOM equals CUDA OOM.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Fail isolation honesty
- **Verify:** verdict=fail-transfer | STUDY-028 fail-transfer / leave unverified
- **Sources:** [DGX Spark UMA∉memcg — fail isolation honesty](https://forums.developer.nvidia.com/t/dgx-spark-becomes-unresponsive-zombie-instead-of-throwing-cuda-oom/353752/18)

### The >1 tok/s floor is correct and will refuse dense+NVMe often · `load-bearing` · policy
**A >1 tok/s decode floor is well-justified; for dense models spilling to NVMe it will (correctly) refuse frequently.**
Because sub-1 tok/s single-stream is the documented norm once dense weights hit NVMe, the refusal floor fires correctly there. The product must frame dense+NVMe refusal as honesty, not failure, and surface it with a contrastive frame ('you expected model X to run; it won't clear 1 tok/s because... — options: smaller quant / more RAM / different model').
- **Applies to:** dense; nvme; all · **Metric:** floor = >1 tok/s decode · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Position NVMe as the cold-MoE-expert lane, not a dense-weight-streaming lane; the measured receipt is the external verifier of the planner's own prediction (different mechanism, never self-grading).
- **Verify:** verdict=confirmed | DeepSpeed-Inference throughput-orientation confirmed; floor justification follows from the dense-offload + memory-wall findings.
- **Sources:** [DeepSpeed-Inference: Enabling Efficient Inference at Unprecedented Scale](https://arxiv.org/abs/2207.00032) — Aminabadi et al. (Microsoft) 2022; throughput-oriented; SUPPORTED

