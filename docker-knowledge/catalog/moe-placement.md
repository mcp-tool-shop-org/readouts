# MoE expert placement & prefetch
_Hot/warm/cold expert tiering, router-lookahead prefetch, staleness eviction, workload-representative calibration_ · wave 9 · 2026-09-07 · [‹ catalog index](README.md)

28 findings · 14 load-bearing · 24 verified.

| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |
|------|---------|-------|--------|------------|------|---|
| craft | Flex-MIG — NVIDIA_VISIBLE_DEVICES UUIDs | K8s pods set NVIDIA_VISIBLE_DEVICES to MIG UUIDs; place craft is UUID visibility + MIG leaves, not ad-hoc --gpus all. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | GKE NVIDIA MPS — sharing fails honest refusal | MPS time-slice/share exists; does not transfer into honest single-GPU refusal axis. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | GPU-Virt-Bench — MIG incl. B200 | MIG on A100/H100/H200/B200 and RTX PRO; software vGPU vs ideal MIG for container multi-tenancy. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | GPUnion — campus GPU sharing via NVIDIA Container Toolkit | Campus GPU sharing runs workloads in Docker with NVIDIA Container Toolkit passthrough and NVIDIA_VISIBLE_DEVICES — package surface stays toolkit inject. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | Global Simulation-Guided Dynamic Operator Scheduling | Container-granularity scheduling leaves idle slices; operator-level SliceScheduler under SLA. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | Hierarchical Resource Partitioning — RL on modern GPUs | RL-based hierarchical partitioning when a single program no longer fills modern GPUs. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | ParvaGPU — spatial GPU sharing for cloud DNN inference | Spatial GPU sharing for cloud DNN inference under SLO latency while minimizing GPU consumption. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | Performance Isolation — MPS vs MIG vs Green Contexts | Compares MPS, MIG, and Green Contexts for temporal isolation on A100 and Jetson Orin. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | Predictable LLM Serving — MIG/MPS/cgroup placement | Host controller combines dynamic MIG reconfiguration, PCIe-aware placement, MPS quotas, and cgroup I/O; tenants in Docker with MIG UUID. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | Scheduler-Driven Job Atomization on MIG clusters | MIG clusters waste capacity when jobs are rigid peak-memory blocks; atomizes jobs for scheduler-driven placement. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | Villarrubia — MPS vs MIG on Blackwell | MIG isolates; MPS shares memory (contention) on Ampere/Hopper/Blackwell B200 — profile before choosing. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| constraint | --n-cpu-moe is per-layer and CPU-COMPUTES offloaded experts (cost model = CPU-compute at decode, PCIe at prefill) | --n-cpu-moe N places experts at per-layer granularity; CPU-assigned experts are COMPUTED on CPU during decode (KTransformers-style), so the offload cost at decode is CPU-compute-bound, while GPU experts stream over PCIe only at batch >= GGML_OP_OFFLOAD_MIN_BATCH (~32) during prompt processing. | GGML_OP_OFFLOAD_MIN_BATCH default 32 tokens; decode = CPU-compute bound, prefill = PCIe bound | llama.cpp; moe; pcie | ●●· | ✓ |
| technique | -ot DOES cleanly pin shared/attention to VRAM and route experts to CPU/RAM (the hot tier is expressible today) | Although intra-routed-expert split is impossible, -ot CAN cheaply pin shared experts + attention + router/norms to VRAM and place routed _exps tensors on CPU/RAM per layer — so the 'shared/attention always hot in VRAM' tier is expressible with a one-line flag today. | regex 'blk\.\d+\.ffn_.*_exps\.=CPU' keeps routed experts on CPU; _shexp/attn stay GPU | llama.cpp; moe | ●●● | ✓ |
| constraint | Cold-NVMe expert streaming is the danger zone | Streaming cold experts from NVMe during decode is feasible only with accurate prefetch + sparsity; otherwise it thrashes. | ~12x per-token energy vs HBM; 9.96 tok/s at 50% FFN on flash (sparsified) | moe; nvme | ●●● | ✓ |
| technique | Cross-layer-gate prefetch works on STOCK models (run layer i+1's existing router on layer i's state early) | The dominant stock-model prefetch is the cross-layer gate (Fate): run the NEXT layer's EXISTING router on the current layer's hidden state one step early (adjacent layers >83% cosine-similar) to predict its experts — ~99% hit rate, zero new parameters, no retraining. AdapMoE independently corroborates (~90% accuracy, 1.35x speedup, unmodified model). | Fate 99.08% hit / 97.15% prefetch accuracy; AdapMoE 1.35x speedup; >83% adjacent-layer cosine similarity | moe | ●●● | ✓ |
| constraint | Expert eviction must be staleness-aware, not LRU | MoE expert access is deterministic-sequential, not recency-based, so LRU/LFU evicts the wrong experts. | 85x fewer collision misses vs LRU; >88% hit at 5% VRAM | moe | ●●● | ✓ |
| gotcha | Expert skew is real but request-level (calibration must be adaptive) | MoE activation is skewed within a request (<5% of experts) but aggregates toward uniform across diverse prompts. | <5% experts active per request; 3.1-16.7x per-token latency improvement | moe | ●●● | ✓ |
| policy | Least-Stale eviction: stale/current queue partition, evict stale first (key = stale-flag + layer-index) | SpecMD's Least-Stale partitions the expert cache into 'stale' (touched in a prior forward pass) vs 'current' (this pass) and evicts stale first, exploiting the deterministic front-to-back layer order so soon-needed experts are protected; the key is (stale-flag, layer-index) updated per forward-pass (not per token), and it needs no model changes (forward hooks on a stock MoE). | 2.6-8.6x fewer collision misses typical; up to 85x best-case (abstract); >88% hit at ~5% cache; up to 34.7% TTFT reduction | moe | ●●● | ✓ |
| method | No built-in per-expert trace — capture via eval-callback on the top-k/argsort routing tensor -> L×E histogram | llama.cpp has no built-in per-expert activation-trace export; the routing decision is an internal top-k/argsort `ids` tensor (global expert IDs). The lowest-friction capture is the eval-callback (ggml_backend_sched_set_eval_callback / cb_eval), filtering on the routing node and returning false on all other nodes (to avoid forcing host copies), accumulating a per-layer x per-expert (L×E) count matrix — a small offline harness, no fork. | trace = L×E integer matrix (KBs); MoE-Infinity EAM <1% overhead budget | llama.cpp; moe | ●●● | ✓ |
| technique | Per-expert tiering must be a RUNTIME cache at llama.cpp's #20757 hook point | The only per-expert behavior in stock llama.cpp is a runtime copy of the ACTIVE experts' sub-rows by byte offset (expert_offset = first_id * expert_size) CPU->GPU, with NO slot remapping or cross-pass persistence — so per-expert hot/warm/cold tiering must be built as a persistent GPU-slot cache ABOVE this copy. | #20757 PoC: 12-14 tok/s steady-state vs 0.5-1 tok/s CPU-only offload | llama.cpp; moe | ●●● | ✓ |
| policy | Recalibrate on DRIFT, not a timer: streaming change-detector tripwire + divergence confirmation | Because expert skew is request-level and aggregates to uniform, a static histogram is valid only for its trace; recalibration should be DRIFT-gated: a cheap always-on streaming change detector on the warm-tier miss-rate (ADWIN, parameter-free, significance delta=0.002; or DDM, 2-sigma warning / 3-sigma alarm) as the tripwire, confirmed by a distribution signal (JS divergence / chi-square between the calibrated vs EWMA-decayed live expert histogram). | ADWIN delta=0.002 (parameter-free); DDM 2-sigma warning / 3-sigma alarm | moe | ●●● | ✓ |
| technique | Router lookahead hides the RAM->VRAM transfer | A router can predict next-layer experts during the current layer, overlapping the warm-tier transfer with compute. | within 19% of GPU-only (Pre-gated); ~99% hit (Fate); 17%->72% hit at 10% resident (MoE-Beyond) | moe | ●●● | ✓ |
| constraint | SCOPE EXCLUSION: Pre-gated needs a fine-tuned model (out); MoE-Beyond needs a trained predictor (deferred) | Not all prefetch methods work on stock GGUFs: Pre-gated MoE REQUIRES changing the architecture and fine-tuning the pre-gates ('incrementally trained during the fine-tuning stage') -> OUT OF SCOPE for stock-GGUF gpu-container; MoE-Beyond keeps the base model stock but needs a separately TRAINED transformer predictor (66M traces) -> a build-and-own deliverable, only if cross-layer-gate (free) proves insufficient. | Pre-gated 81% of GPU-only (needs fine-tune); MoE-Beyond 17%->72% hit at 10% budget (needs trained predictor) | moe | ●●● | ✓ |
| benchmark | Warm-tier MoE offload is production-proven | Hot-VRAM + warm-RAM expert placement (or CPU expert compute) clears the >1 tok/s floor on a single consumer GPU today. | >3 tok/s (Fiddler 24GB), ~8.7-10 tok/s (KTransformers 671B), ~12-14 tok/s (llama.cpp) | moe; llama.cpp; ktransformers | ●●● | ✓ |
| constraint | llama.cpp fuses a layer's experts into ONE tensor — -ot is per-layer, never per-expert | In stock llama.cpp, all experts of a MoE layer's FFN projection are stored in a single fused 3D tensor (blk.N.ffn_{gate,up,down}_exps.weight, shape {n_embd, n_ff, n_expert}); --override-tensor/-ot regex-matches WHOLE tensor names to buffer types, so its finest static-placement grain is per-layer-per-projection — an individual expert cannot be statically placed. | GLM-4.6 ffn_gate_exps {5120,1536,160} = 160 experts in 1 tensor; -ot matches whole tensor names | llama.cpp; moe | ●●● | ✓ |
| technique | Between re-traces, continuously self-tune the warm/cold split (EWMA/hyperbolic heat; ARC ghost lists; LeCaR) | Between expensive re-traces, keep tiers tracking gradual drift for free: maintain each expert's tier priority as an EWMA/time-decayed ('hyperbolic') heat score updated per-iteration, and self-tune the warm/cold boundary with ARC-style ghost lists (a burst of ghost-hits on just-demoted experts = mis-sized split) or LeCaR regret-minimization (best when cache << working set — our exact case). | ARC 0.75% overhead, 10-20% over LRU; Hyperbolic 10-20% lower miss; LeCaR up to 18x on small caches | moe | ●●● | ✓ |
| technique | Cadence mirrors tiered JIT: cheap always-on counters, expensive recompile on threshold, anti-thrash guard | The 'when to recompute an adaptive policy' problem is solved in tiered JIT compilers (HotSpot): cheap always-on hotness counters, expensive recompilation triggered only at a threshold, with a deopt-counter guard against recompile thrashing — mapping directly to per-iteration hit-rate/divergence counters (cheap) -> re-trace on threshold (expensive) -> a 're-trace within N tokens' guard against recalibration thrashing. | HotSpot Tier4CompileThreshold; deopt rate-limit (anti-thrash) | moe | ●●● | ✓ |
| technique | Turnkey trace alternatives: SGLang ExpertDistributionRecorder + vLLM --enable-eplb | If llama.cpp instrumentation is too costly, SGLang ships an ExpertDistributionRecorder (per-layer physical-expert selection counts for EPLB) and vLLM's --enable-eplb records expert load over a rolling window (default 1000 engine steps) — both produce the L×E table directly. | vLLM eplb window_size default 1000 steps; SGLang recorder 'without overhead' (PR claim) | vllm; moe | ●●· | ✓ |

## Detail

### Flex-MIG — NVIDIA_VISIBLE_DEVICES UUIDs · `directional` · craft
**K8s pods set NVIDIA_VISIBLE_DEVICES to MIG UUIDs; place craft is UUID visibility + MIG leaves, not ad-hoc --gpus all.**
K8s pods set NVIDIA_VISIBLE_DEVICES to MIG UUIDs; place craft is UUID visibility + MIG leaves, not ad-hoc --gpus all.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [Flex-MIG — NVIDIA_VISIBLE_DEVICES UUIDs](https://arxiv.org/abs/2511.09143) — Kim et al. 2025; SUPPORTED

### GKE NVIDIA MPS — sharing fails honest refusal · `directional` · craft
**MPS time-slice/share exists; does not transfer into honest single-GPU refusal axis.**
MPS time-slice/share exists; does not transfer into honest single-GPU refusal axis.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Sharing fails honest single-GPU refusal.
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [GKE NVIDIA MPS — sharing fails honest refusal](https://cloud.google.com/kubernetes-engine/docs/how-to/nvidia-mps-gpus) — 2026; SUPPORTED

### GPU-Virt-Bench — MIG incl. B200 · `directional` · craft
**MIG on A100/H100/H200/B200 and RTX PRO; software vGPU vs ideal MIG for container multi-tenancy.**
MIG on A100/H100/H200/B200 and RTX PRO; software vGPU vs ideal MIG for container multi-tenancy.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** B200 in MIG scope
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [GPU-Virt-Bench — MIG incl. B200](https://arxiv.org/abs/2512.22125) — Jithin/Ditto 2025; SUPPORTED

### GPUnion — campus GPU sharing via NVIDIA Container Toolkit · `directional` · craft
**Campus GPU sharing runs workloads in Docker with NVIDIA Container Toolkit passthrough and NVIDIA_VISIBLE_DEVICES — package surface stays toolkit inject.**
Campus GPU sharing runs workloads in Docker with NVIDIA Container Toolkit passthrough and NVIDIA_VISIBLE_DEVICES — package surface stays toolkit inject.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Toolkit inject under multi-lab scheduling
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [GPUnion — campus GPU sharing via NVIDIA Container Toolkit](https://arxiv.org/abs/2507.18928) — Li et al. 2025; SUPPORTED

### Global Simulation-Guided Dynamic Operator Scheduling · `directional` · craft
**Container-granularity scheduling leaves idle slices; operator-level SliceScheduler under SLA.**
Container-granularity scheduling leaves idle slices; operator-level SliceScheduler under SLA.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Finer schedule grain than Docker start/stop
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [Global Simulation-Guided Dynamic Operator Scheduling](https://arxiv.org/abs/2608.15762) — Liu et al. 2026; SUPPORTED

### Hierarchical Resource Partitioning — RL on modern GPUs · `directional` · craft
**RL-based hierarchical partitioning when a single program no longer fills modern GPUs.**
RL-based hierarchical partitioning when a single program no longer fills modern GPUs.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Deepens package/place
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [Hierarchical Resource Partitioning — RL on modern GPUs](https://arxiv.org/abs/2405.08754) — Saroliya et al. 2024; SUPPORTED

### ParvaGPU — spatial GPU sharing for cloud DNN inference · `directional` · craft
**Spatial GPU sharing for cloud DNN inference under SLO latency while minimizing GPU consumption.**
Spatial GPU sharing for cloud DNN inference under SLO latency while minimizing GPU consumption.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Deepens package/place
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [ParvaGPU — spatial GPU sharing for cloud DNN inference](https://arxiv.org/abs/2409.14447) — Lee et al. 2024; SUPPORTED

### Performance Isolation — MPS vs MIG vs Green Contexts · `directional` · craft
**Compares MPS, MIG, and Green Contexts for temporal isolation on A100 and Jetson Orin.**
Compares MPS, MIG, and Green Contexts for temporal isolation on A100 and Jetson Orin.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Isolation mechanism choice deepens place axis
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [Performance Isolation — MPS vs MIG vs Green Contexts](https://arxiv.org/abs/2601.07600) — Martín et al. 2026; SUPPORTED

### Predictable LLM Serving — MIG/MPS/cgroup placement · `directional` · craft
**Host controller combines dynamic MIG reconfiguration, PCIe-aware placement, MPS quotas, and cgroup I/O; tenants in Docker with MIG UUID.**
Host controller combines dynamic MIG reconfiguration, PCIe-aware placement, MPS quotas, and cgroup I/O; tenants in Docker with MIG UUID.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Multi-GPU place/schedule craft
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [Predictable LLM Serving — MIG/MPS/cgroup placement](https://arxiv.org/abs/2508.20274) — Darzi et al. 2025; SUPPORTED

### Scheduler-Driven Job Atomization on MIG clusters · `directional` · craft
**MIG clusters waste capacity when jobs are rigid peak-memory blocks; atomizes jobs for scheduler-driven placement.**
MIG clusters waste capacity when jobs are rigid peak-memory blocks; atomizes jobs for scheduler-driven placement.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Deepens package/place
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [Scheduler-Driven Job Atomization on MIG clusters](https://arxiv.org/abs/2509.19086) — Konopa et al. 2025; SUPPORTED

### Villarrubia — MPS vs MIG on Blackwell · `directional` · craft
**MIG isolates; MPS shares memory (contention) on Ampere/Hopper/Blackwell B200 — profile before choosing.**
MIG isolates; MPS shares memory (contention) on Ampere/Hopper/Blackwell B200 — profile before choosing.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [Villarrubia — MPS vs MIG on Blackwell](https://arxiv.org/abs/2604.22430) — Villarrubia et al. 2026; SUPPORTED

### --n-cpu-moe is per-layer and CPU-COMPUTES offloaded experts (cost model = CPU-compute at decode, PCIe at prefill) · `load-bearing` · constraint
**--n-cpu-moe N places experts at per-layer granularity; CPU-assigned experts are COMPUTED on CPU during decode (KTransformers-style), so the offload cost at decode is CPU-compute-bound, while GPU experts stream over PCIe only at batch >= GGML_OP_OFFLOAD_MIN_BATCH (~32) during prompt processing.**
The decode-time bottleneck for offloaded experts is CPU matmul throughput + RAM bandwidth, NOT PCIe; PCIe streaming only kicks in for large batches (prompt processing) above the offload-min-batch threshold (mainline default 32 tokens; ik_llama scales it as 32 * total_experts / active_experts). This is the two-regime cost model the planner must encode.
- **Applies to:** llama.cpp; moe; pcie · **Metric:** GGML_OP_OFFLOAD_MIN_BATCH default 32 tokens; decode = CPU-compute bound, prefill = PCIe bound · **Confidence:** medium · **Rig relevance:** 5/5
- **Design implication:** The planner's per-tier cost model must distinguish CPU-compute (decode, offloaded experts -> uses the measured cpu_bw probe) from PCIe-stream (prefill, batch>=32). Conflating them mis-predicts decode tok/s. (Partly already in the Milestone-2/3 cpu_bw input.)
- **Verify:** verdict=confirmed-with-fixes | primary source is a marked non-primary blog; the compute-on-CPU + min-batch-32 facts are corroborated by tensor-engine-knowledge (verified) + #20757; both LLM lenses PLAUSIBLE.
- **Sources:** [Performant local MoE CPU inference with GPU acceleration in llama.cpp (MoE offload guide)](https://huggingface.co/blog/Doctor-Shotgun/llamacpp-moe-offload-guide) — Doctor-Shotgun (HF blog — non-primary, marked) 2025; GGML_OP_OFFLOAD_MIN_BATCH = 32 (mainline default); PARTIAL

### -ot DOES cleanly pin shared/attention to VRAM and route experts to CPU/RAM (the hot tier is expressible today) · `load-bearing` · technique
**Although intra-routed-expert split is impossible, -ot CAN cheaply pin shared experts + attention + router/norms to VRAM and place routed _exps tensors on CPU/RAM per layer — so the 'shared/attention always hot in VRAM' tier is expressible with a one-line flag today.**
A regex like 'blk\.\d+\.ffn_.*_exps\.=CPU' routes the routed-expert tensors to CPU while shared experts (_shexp), attention (attn_*), and norms stay on the default GPU device. This validates the hot-VRAM tier of the architecture (shared/attention/router) without any custom code; only the routed-expert SUB-tiering needs the runtime cache.
- **Applies to:** llama.cpp; moe · **Metric:** regex 'blk\.\d+\.ffn_.*_exps\.=CPU' keeps routed experts on CPU; _shexp/attn stay GPU · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** The planner emits the shared/attention-in-VRAM tier directly as -ot today (low-risk, shipping). Only the routed-expert hot/warm/cold split is deferred to the runtime cache (#20757 layer).
- **Verify:** verdict=confirmed | oracle: #13154 confirms shared(_shexp)/routed(_exps) split via tensor names; this is the solid part of #13154.
- **Sources:** [Insufficient documentation for -ot and --override-tensor flag (Discussion #13154)](https://github.com/ggml-org/llama.cpp/discussions/13154) — ggml-org/llama.cpp community 2025; SUPPORTED

### Cold-NVMe expert streaming is the danger zone · `load-bearing` · constraint
**Streaming cold experts from NVMe during decode is feasible only with accurate prefetch + sparsity; otherwise it thrashes.**
SSD expert offload raises per-token-generation energy ~12x vs an HBM baseline, and prefetching hides latency but NOT the energy/bandwidth penalty. PowerInfer-2 reaches 9.96 tok/s with 50% of FFN on flash by overlapping I/O with compute — but only with a custom SPARSIFIED model with predictable activation.
- **Applies to:** moe; nvme · **Metric:** ~12x per-token energy vs HBM; 9.96 tok/s at 50% FFN on flash (sparsified) · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Gate the cold-NVMe tier: admit only if predicted prefetch hit-rate keeps decode above the floor; default it off for experts otherwise.
- **Verify:** verdict=confirmed | SSD-harmful + PowerInfer-2 confirmed verbatim by oracle; both families plausibility-concurred.
- **Sources:** [SSD Offloading for LLM MoE Weights Considered Harmful in Energy Efficiency](https://arxiv.org/abs/2508.06978) — Kyung, Yun & Ahn 2025; ~12x energy; SUPPORTED ; [PowerInfer-2: Fast LLM Inference on a Smartphone](https://arxiv.org/abs/2406.06282) — Xue et al. 2024; 9.96 tok/s @ 50% FFN on flash; SUPPORTED

### Cross-layer-gate prefetch works on STOCK models (run layer i+1's existing router on layer i's state early) · `load-bearing` · technique
**The dominant stock-model prefetch is the cross-layer gate (Fate): run the NEXT layer's EXISTING router on the current layer's hidden state one step early (adjacent layers >83% cosine-similar) to predict its experts — ~99% hit rate, zero new parameters, no retraining. AdapMoE independently corroborates (~90% accuracy, 1.35x speedup, unmodified model).**
Fate clones layer i's gate input to predict layer i+1's experts via the native router (no added params, no training), tested on Qwen1.5-MoE / DeepSeekMoE; it pins shallow layers (0-3) fully because they predict worst, spreading the rest of the VRAM budget across deep layers (depth-aware tiering). AdapMoE applies layer i+1's gate to layer i's activations for ~90% accuracy with no finetuning (only an OPTIONAL first-layer predictor needs training).
- **Applies to:** moe · **Metric:** Fate 99.08% hit / 97.15% prefetch accuracy; AdapMoE 1.35x speedup; >83% adjacent-layer cosine similarity · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Warm-tier prefetch is realizable on stock GGUFs by invoking layer i+1's router on layer i's residual — no model surgery. Make the hot/warm tiering DEPTH-AWARE: pin the first ~3-4 MoE layers hot, prefetch deep layers via the cross-layer gate.
- **Verify:** verdict=confirmed | oracle: Fate (Fang 2025) abstract = cross-layer gate + ~99% hit + no extra training; AdapMoE (Zhong 2024) 1.35x + unmodified. mistral's lone CONTRADICTORY (needs retraining) overridden by 2 primary sources + oracle (known LLM blind spot).
- **Sources:** [Fate: Fast Edge Inference of Mixture-of-Experts Models via Cross-Layer Gate](https://arxiv.org/abs/2502.12224) — Zhiyuan Fang et al. 2025; 99.08% hit / 97.15% accuracy; >83% cosine; shallow pin L=3; SUPPORTED ; [AdapMoE: Adaptive Sensitivity-based Expert Gating and Management for Efficient MoE Inference](https://arxiv.org/abs/2408.10284) — Shuzhang Zhong et al. 2024; 1.35x speedup; ~90% prefetch accuracy; PARTIAL

### Expert eviction must be staleness-aware, not LRU · `load-bearing` · constraint
**MoE expert access is deterministic-sequential, not recency-based, so LRU/LFU evicts the wrong experts.**
SpecMD finds expert access is deterministic-sequential rather than temporal-locality-based; a Least-Stale eviction policy cuts collision misses up to 85x vs LRU and reaches >88% hit at only 5% (0.6GB) VRAM cache.
- **Applies to:** moe · **Metric:** 85x fewer collision misses vs LRU; >88% hit at 5% VRAM · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Calibration #1: use a staleness/sequence-aware eviction policy for experts. (LRU/ARC remains correct for KV-cache spill — it is wrong for experts.)
- **Verify:** verdict=confirmed-with-fixes | Core eviction/hit figures verbatim; 'deterministic-sequential by layer' is paper framing, abstract says 'predictable, not-recency' (PARTIAL).
- **Sources:** [SpecMD: A Comprehensive Study on Speculative Expert Prefetching](https://arxiv.org/abs/2602.03921) — Hoang, Jaiswal, Samragh & Cho (Apple) 2026; 85x vs LRU; >88% hit @ 5% VRAM; PARTIAL

### Expert skew is real but request-level (calibration must be adaptive) · `load-bearing` · gotcha
**MoE activation is skewed within a request (<5% of experts) but aggregates toward uniform across diverse prompts.**
MoE-Infinity measures <5% of experts repeatedly activated per request, but is explicit that the skew is request-level and flattens to uniform when aggregated across many diverse prompts. A one-time global frequency histogram therefore mis-tiers out-of-distribution workloads and thrashes the warm tier.
- **Applies to:** moe · **Metric:** <5% experts active per request; 3.1-16.7x per-token latency improvement · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Calibration #1: calibrate on workload-representative traces and refine online from the receipt's measured routing — NOT a single generic-corpus snapshot.
- **Verify:** verdict=confirmed-with-fixes | Core <5%/request + 3.1-16.7x confirmed; the '4x less GPU' sub-claim unverified (PARTIAL on source).
- **Sources:** [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](https://arxiv.org/abs/2401.14361) — Xue et al. 2024; <5% experts/request; 3.1-16.7x; PARTIAL

### Least-Stale eviction: stale/current queue partition, evict stale first (key = stale-flag + layer-index) · `load-bearing` · policy
**SpecMD's Least-Stale partitions the expert cache into 'stale' (touched in a prior forward pass) vs 'current' (this pass) and evicts stale first, exploiting the deterministic front-to-back layer order so soon-needed experts are protected; the key is (stale-flag, layer-index) updated per forward-pass (not per token), and it needs no model changes (forward hooks on a stock MoE).**
Staleness is a binary flag flipped per forward pass, backed by FIFO/priority structures ordered by layer position (O(log N) insert / O(1) evict), purely retrospective (no future-selection oracle). It beats LRU because MoE expert access follows layer order, not temporal recency — LRU keeps a just-finished early-layer expert while evicting an upcoming one.
- **Applies to:** moe · **Metric:** 2.6-8.6x fewer collision misses typical; up to 85x best-case (abstract); >88% hit at ~5% cache; up to 34.7% TTFT reduction · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** The runtime expert cache (per-expert-cache-is-the-runtime-hook) uses Least-Stale, NOT LRU/ARC, for the expert slots; key on (stale-flag, layer-index). (LRU/ARC remain correct for KV-cache spill — wrong for experts.)
- **Verify:** verdict=confirmed-with-fixes | oracle: SpecMD EXISTS (Apple, 2026), abstract states 'up to 85x' + '>88% hit' + '34.7% TTFT' verbatim; both LLM lenses flagged 85x as headline -> reframed to lead with 2.6-8.6x typical, 85x best-case.
- **Sources:** [SpecMD: A Comprehensive Study On Speculative Expert Prefetching](https://arxiv.org/abs/2602.03921) — Duc Hoang, Ajay Jaiswal, Mohammad Samragh, Minsik Cho (Apple) 2026; up to 85x (abstract); 2.6-8.6x per-config; >88% hit at ~5% cache; 34.7% TTFT reduction; SUPPORTED

### No built-in per-expert trace — capture via eval-callback on the top-k/argsort routing tensor -> L×E histogram · `load-bearing` · method
**llama.cpp has no built-in per-expert activation-trace export; the routing decision is an internal top-k/argsort `ids` tensor (global expert IDs). The lowest-friction capture is the eval-callback (ggml_backend_sched_set_eval_callback / cb_eval), filtering on the routing node and returning false on all other nodes (to avoid forcing host copies), accumulating a per-layer x per-expert (L×E) count matrix — a small offline harness, no fork.**
Expert selection is built from ggml_top_k (internally ggml_argsort) producing the per-token top-n_expert_used id tensor with GLOBAL expert IDs (so the histogram maps directly to physical tiers, no remapping). The eval-callback fires per graph node with name+data during llama_decode; returning false on non-routing nodes keeps it a sub-1% probe (MoE-Infinity's EAM overhead budget). The exact routing-node ->name is a one-grep task in build_moe_ffn (src/llama-graph.cpp).
- **Applies to:** llama.cpp; moe · **Metric:** trace = L×E integer matrix (KBs); MoE-Infinity EAM <1% overhead budget · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** gpu-container ships a calibration harness using cb_eval to emit the L×E activation matrix; budget <1% overhead; store the L×E integer matrix (KBs) in the receipt — NOT per-token logs. This is the concrete INPUT that makes 'adaptive calibration' real on llama.cpp.
- **Verify:** verdict=confirmed-with-fixes | oracle: #20757 ids tensor + MoE-Infinity EAM/<1% confirmed; the exact routing-node ->name not pinned this run (one-grep in build_moe_ffn) — flagged, not load-bearing to method validity.
- **Sources:** [Two-tier GPU+RAM expert cache for MoE offload (Issue #20757) — the routing ids tensor](https://github.com/ggml-org/llama.cpp/issues/20757) — ggml-org/llama.cpp 2026; SUPPORTED ; [llama.cpp examples/eval-callback (ggml_backend_sched_set_eval_callback / cb_eval)](https://github.com/ggml-org/llama.cpp/tree/master/examples/eval-callback) — ggml-org/llama.cpp 2026; PARTIAL ; [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](https://arxiv.org/abs/2401.14361) — Leyang Xue, Yao Fu, Zhan Lu, Luo Mai, Mahesh Marina 2024; <1% overhead (EAM); PARTIAL

### Per-expert tiering must be a RUNTIME cache at llama.cpp's #20757 hook point · `load-bearing` · technique
**The only per-expert behavior in stock llama.cpp is a runtime copy of the ACTIVE experts' sub-rows by byte offset (expert_offset = first_id * expert_size) CPU->GPU, with NO slot remapping or cross-pass persistence — so per-expert hot/warm/cold tiering must be built as a persistent GPU-slot cache ABOVE this copy.**
Issue #20757 quotes the exact hook: 'it copies by byte offset into a GPU tensor that mirrors the full CPU tensor layout (expert_offset = first_id * expert_size, line 1529)' and 'no slot remapping, no persistence across passes. This is the hook point for the cache.' The issue PROPOSES exactly what gpu-container's per-expert lane needs: a GPU buffer of N slots (--moe-expert-cache-size N, N << n_expert), a persistent expert_id->slot_idx map carried across passes, and pluggable eviction (LRU/SLRU/LFU/FIFO). Its PoC reports 12-14 tok/s steady-state vs 0.5-1 tok/s CPU-only offload.
- **Applies to:** llama.cpp; moe · **Metric:** #20757 PoC: 12-14 tok/s steady-state vs 0.5-1 tok/s CPU-only offload · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** gpu-container's per-expert tiering is NOVEL vs all stock engines. Phase-2 build target: either implement the runtime expert-slot cache (the #20757 layer, with Least-Stale eviction) or contribute to/ride that upstream effort. The cache — not -ot — is where hot/warm/cold per-expert placement lives.
- **Verify:** verdict=confirmed | oracle: #20757 quotes byte-offset addressing + 'no slot remapping, no persistence... hook point for the cache' + --moe-expert-cache-size proposal + 12-14 vs 0.5-1 tok/s PoC, VERBATIM.
- **Sources:** [Feature Request: Two-tier GPU+RAM expert cache for MoE offload (pluggable eviction policy) (Issue #20757)](https://github.com/ggml-org/llama.cpp/issues/20757) — ggml-org/llama.cpp (community + code refs ~L1529) 2026; 12-14 tok/s vs 0.5-1 tok/s; expert_offset = first_id * expert_size (line 1529); SUPPORTED ; [Loads of interesting ideas in the 'ktransformers' report (Discussion #8721)](https://github.com/ggml-org/llama.cpp/discussions/8721) — ggml-org/llama.cpp; ikawrakow/ik_llama.cpp 2024; PARTIAL

### Recalibrate on DRIFT, not a timer: streaming change-detector tripwire + divergence confirmation · `load-bearing` · policy
**Because expert skew is request-level and aggregates to uniform, a static histogram is valid only for its trace; recalibration should be DRIFT-gated: a cheap always-on streaming change detector on the warm-tier miss-rate (ADWIN, parameter-free, significance delta=0.002; or DDM, 2-sigma warning / 3-sigma alarm) as the tripwire, confirmed by a distribution signal (JS divergence / chi-square between the calibrated vs EWMA-decayed live expert histogram).**
ADWIN keeps a variable-length window, splits it, and declares drift when sub-window means differ beyond a bound at delta=0.002, then drops the stale half (the kept window IS the fresh calibration sample). DDM treats each warm-tier miss as Bernoulli and uses 2-sigma/3-sigma control limits to separate transient load spikes (warning -> start buffering a candidate trace) from real drift (alarm -> commit the re-trace). A JS/chi-square divergence between calibrated and live expert distributions confirms the CAUSE is routing shift, not transient load.
- **Applies to:** moe · **Metric:** ADWIN delta=0.002 (parameter-free); DDM 2-sigma warning / 3-sigma alarm · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** The routing half of gpu-container's recalibration loop fires a re-trace only on a CONFIRMED drift step-change (miss-rate detector + histogram divergence), never per-request or on a fixed timer. This closes the per-expert loop without constant re-tracing cost.
- **Verify:** verdict=confirmed-with-fixes | MoE-Infinity oracle-verified (Xue, request-level skew); ADWIN canonical (Bifet & Gavalda 2007, river-docs agent-retrieved); DDM canonical (Gama 2004, attribution-cited, not re-fetched); both LLM lenses PLAUSIBLE.
- **Sources:** [MoE-Infinity: Efficient MoE Inference on Personal Machines with Sparsity-Aware Expert Cache](https://arxiv.org/abs/2401.14361) — Leyang Xue et al. 2024; 3.1-16.7x per-token latency improvement; SUPPORTED ; [Learning from Time-Changing Data with Adaptive Windowing (ADWIN)](https://riverml.xyz/dev/api/drift/ADWIN/) — Albert Bifet & Ricard Gavalda 2007; delta=0.002 default; SUPPORTED ; [Learning with Drift Detection (DDM)](https://link.springer.com/chapter/10.1007/978-3-540-28645-5_29) — Joao Gama et al. 2004; 2-sigma warning / 3-sigma alarm; PARTIAL

### Router lookahead hides the RAM->VRAM transfer · `load-bearing` · technique
**A router can predict next-layer experts during the current layer, overlapping the warm-tier transfer with compute.**
Pre-gated MoE selects the next layer's experts during the current layer, landing within 19% of GPU-only latency at 4.2x memory reduction with quality preserved; Fate reaches ~99% expert hit-rate (4.1x decode speedup); MoE-Beyond lifts cache hit from 17% to 72% with only 10% of experts resident.
- **Applies to:** moe · **Metric:** within 19% of GPU-only (Pre-gated); ~99% hit (Fate); 17%->72% hit at 10% resident (MoE-Beyond) · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** A small VRAM hot tier + router-lookahead prefetch is sufficient — the warm tier need not be large.
- **Verify:** verdict=confirmed-with-fixes | Pre-gated/Fate/MoE-Beyond confirmed; a Pre-gated SQuAD figure was a misread (corrected); MoE-Beyond year 2024->2025.
- **Sources:** [Pre-gated MoE: Algorithm-System Co-Design for Fast & Scalable MoE Inference](https://arxiv.org/abs/2308.12066) — Hwang et al. 2024; within 19% of GPU-only; 4.2x mem; SUPPORTED ; [Fate: Fast Edge Inference of MoE Models via Cross-Layer Gate](https://arxiv.org/abs/2502.12224) — Fang et al. 2025; ~99% hit; 4.1x decode; SUPPORTED ; [MoE-Beyond: Learning-Based Expert Activation Prediction on Edge Devices](https://arxiv.org/abs/2508.17137) — Gavhane et al. 2025; 17%->72% hit @ 10% resident; SUPPORTED

### SCOPE EXCLUSION: Pre-gated needs a fine-tuned model (out); MoE-Beyond needs a trained predictor (deferred) · `load-bearing` · constraint
**Not all prefetch methods work on stock GGUFs: Pre-gated MoE REQUIRES changing the architecture and fine-tuning the pre-gates ('incrementally trained during the fine-tuning stage') -> OUT OF SCOPE for stock-GGUF gpu-container; MoE-Beyond keeps the base model stock but needs a separately TRAINED transformer predictor (66M traces) -> a build-and-own deliverable, only if cross-layer-gate (free) proves insufficient.**
Pre-gated's body states verbatim 'change the MoE model architecture to properly accommodate... our pre-gate function' and 'our pre-gate functions are incrementally trained during the fine-tuning stage' — so a stock Mixtral/Qwen GGUF cannot use it as-is. MoE-Beyond trains a lightweight transformer predictor (multi-label sequence prediction, 97.5% acc / 86.6% F1) on activation traces; the MoE is unmodified but the predictor is a per-model offline training step.
- **Applies to:** moe · **Metric:** Pre-gated 81% of GPU-only (needs fine-tune); MoE-Beyond 17%->72% hit at 10% budget (needs trained predictor) · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** v1 uses cross-layer-gate prefetch (stock, free). EXCLUDE Pre-gated (we cannot ship a fine-tuned model). MoE-Beyond is a DEFERRED option (own a trained predictor) gated on Fate-style prefetch proving insufficient on target GGUFs.
- **Verify:** verdict=confirmed | oracle (body): Pre-gated VERBATIM 'change the MoE model architecture' + 'incrementally trained during the fine-tuning stage' (year fixed ->2023); MoE-Beyond (Gavhane 2025) abstract fully supports trained-predictor + 17%->72%.
- **Sources:** [Pre-gated MoE: An Algorithm-System Co-Design for Fast and Scalable Mixture-of-Expert Inference](https://arxiv.org/abs/2308.12066) — Ranggi Hwang et al. 2023; 81% of GPU-only throughput; SUPPORTED ; [MoE-Beyond: Learning-Based Expert Activation Prediction on Edge Devices](https://arxiv.org/abs/2508.17137) — Nishant Gavhane et al. 2025; 17%->72% hit at 10% budget; 97.5% acc / 86.6% F1; SUPPORTED

### Warm-tier MoE offload is production-proven · `load-bearing` · benchmark
**Hot-VRAM + warm-RAM expert placement (or CPU expert compute) clears the >1 tok/s floor on a single consumer GPU today.**
Fiddler runs uncompressed Mixtral-8x7B (90GB+) at >3 tok/s on one 24GB GPU by computing cold experts on CPU instead of moving weights over PCIe; KTransformers runs DeepSeek-V3 671B at ~8.7-10 tok/s decode on a 4090D + 382GB RAM; llama.cpp --n-cpu-moe field-reports ~12-14 tok/s on huge MoEs; Mixtral-offloading hits 2-3 tok/s on consumer/Colab and is PCIe host-to-device bound.
- **Applies to:** moe; llama.cpp; ktransformers · **Metric:** >3 tok/s (Fiddler 24GB), ~8.7-10 tok/s (KTransformers 671B), ~12-14 tok/s (llama.cpp) · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** The hot/warm tier is a safe throughput claim; llama.cpp --n-cpu-moe is the first integration target.
- **Verify:** verdict=confirmed | Fiddler/Mixtral-offloading/llama.cpp verbatim; KTransformers single-socket figure drifted to ~8.73 tok/s (qualitative holds).
- **Sources:** [Fiddler: CPU-GPU Orchestration for Fast Inference of MoE Models](https://arxiv.org/abs/2402.07033) — Kamahori et al. 2024; >3 tok/s, single 24GB GPU; SUPPORTED ; [Fast Inference of MoE Language Models with Offloading](https://arxiv.org/abs/2312.17238) — Eliseev & Mazur 2023; 2-3 tok/s; SUPPORTED ; [KTransformers DeepSeek-V3/R1 tutorial](https://github.com/kvcache-ai/ktransformers) — kvcache-ai 2025; ~8.7-10 tok/s decode; PARTIAL ; [llama.cpp MoE offload guide (--n-cpu-moe / -ot exps=CPU)](https://huggingface.co/blog/Doctor-Shotgun/llamacpp-moe-offload-guide) — Doctor-Shotgun 2025; ~12-14 tok/s; SUPPORTED

### llama.cpp fuses a layer's experts into ONE tensor — -ot is per-layer, never per-expert · `load-bearing` · constraint
**In stock llama.cpp, all experts of a MoE layer's FFN projection are stored in a single fused 3D tensor (blk.N.ffn_{gate,up,down}_exps.weight, shape {n_embd, n_ff, n_expert}); --override-tensor/-ot regex-matches WHOLE tensor names to buffer types, so its finest static-placement grain is per-layer-per-projection — an individual expert cannot be statically placed.**
GLM-4.6 converts to blk.91.ffn_gate_exps.weight of shape {5120, 1536, 160} — all 160 experts stacked in one tensor. PR #11397 (slaren) implements -ot as a std::regex over the full tensor name (e.g. '[2-9][0-9]\.ffn_.*_exps\.=CPU' keeps layers 20-99's experts on CPU) mapping matches to a buffer type (CPU/CUDA0). It operates on entire named tensors, not sub-tensor/per-expert slices. This is the single most load-bearing finding for the per-expert lane: it kills static per-expert placement on this engine.
- **Applies to:** llama.cpp; moe · **Metric:** GLM-4.6 ffn_gate_exps {5120,1536,160} = 160 experts in 1 tensor; -ot matches whole tensor names · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** The planner's STATIC placement schema must emit tensor-name globs (per-layer-per-projection), NOT expert indices. True per-expert tiering is impossible as an -ot plan; it must be a RUNTIME cache (see per-expert-cache-is-the-runtime-hook).
- **Verify:** verdict=confirmed | oracle: PR#11397 'entire named tensors' + GLM {5120,1536,160} dump; both LLM lenses PLAUSIBLE. Gating finding for the per-expert lane.
- **Sources:** [llama : add option to override model tensor buffers (PR #11397)](https://github.com/ggml-org/llama.cpp/pull/11397) — slaren (ggml-org/llama.cpp) 2025; SUPPORTED ; [Insufficient documentation for -ot and --override-tensor flag (Discussion #13154)](https://github.com/ggml-org/llama.cpp/discussions/13154) — ggml-org/llama.cpp community (steampunque et al.) 2025; PARTIAL ; [convert_hf_to_gguf.py — GGUF MoE expert tensor layout](https://github.com/ggml-org/llama.cpp/blob/master/convert_hf_to_gguf.py) — ggml-org/llama.cpp 2026; GLM-4.6: {5120, 1536, 160}; SUPPORTED

### Between re-traces, continuously self-tune the warm/cold split (EWMA/hyperbolic heat; ARC ghost lists; LeCaR) · `supporting` · technique
**Between expensive re-traces, keep tiers tracking gradual drift for free: maintain each expert's tier priority as an EWMA/time-decayed ('hyperbolic') heat score updated per-iteration, and self-tune the warm/cold boundary with ARC-style ghost lists (a burst of ghost-hits on just-demoted experts = mis-sized split) or LeCaR regret-minimization (best when cache << working set — our exact case).**
Hyperbolic caching gives O(1) frequency-with-aging (priority = access-count / age) that self-adjusts to shifting popularity. ARC keeps ghost lists of recently-evicted keys and shifts the recency/frequency target by ghost hits (0.75% overhead, 10-20% over LRU). LeCaR models eviction as online learning over {recency, frequency} via regret on wrongful evictions, winning most when the cache is far smaller than the working set — which is exactly the VRAM-warm-tier-vs-full-expert-set situation.
- **Applies to:** moe · **Metric:** ARC 0.75% overhead, 10-20% over LRU; Hyperbolic 10-20% lower miss; LeCaR up to 18x on small caches · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Continuous cheap update (EWMA heat + ghost-list split-tuning) absorbs GRADUAL drift, so the costly re-trace only fires on a confirmed STEP-change (drift-gated-recalibration-cadence). A rising ghost-hit / wrongful-eviction rate is itself a cheap drift signal.
- **Verify:** verdict=confirmed-with-fixes | ARC oracle-verified (Megiddo & Modha 2003, ghost lists, 0.75%/10-20%); LeCaR (Vietri 2018) + Hyperbolic (Blankstein 2017) canonical, attribution-cited, not individually re-fetched; both LLM lenses PLAUSIBLE.
- **Sources:** [ARC: A Self-Tuning, Low Overhead Replacement Cache](https://www.usenix.org/conference/fast-03/arc-self-tuning-low-overhead-replacement-cache) — Nimrod Megiddo & Dharmendra S. Modha (IBM) 2003; 0.75% overhead; 10-20% over LRU; SUPPORTED ; [Driving Cache Replacement with ML-based LeCaR](https://www.usenix.org/system/files/conference/hotstorage18/hotstorage18-paper-vietri.pdf) — Giuseppe Vietri et al. 2018; up to 18x on small caches; PARTIAL ; [Hyperbolic Caching: Flexible Caching for Web Applications](https://www.usenix.org/system/files/conference/atc17/atc17-blankstein.pdf) — Aaron Blankstein et al. 2017; 10-20% lower miss rate; PARTIAL

### Cadence mirrors tiered JIT: cheap always-on counters, expensive recompile on threshold, anti-thrash guard · `supporting` · technique
**The 'when to recompute an adaptive policy' problem is solved in tiered JIT compilers (HotSpot): cheap always-on hotness counters, expensive recompilation triggered only at a threshold, with a deopt-counter guard against recompile thrashing — mapping directly to per-iteration hit-rate/divergence counters (cheap) -> re-trace on threshold (expensive) -> a 're-trace within N tokens' guard against recalibration thrashing.**
HotSpot increments invocation/back-edge counters in low tiers; crossing Tier3/Tier4 thresholds triggers C1/C2 recompilation, and deopt+recompile is rate-limited so pathological code doesn't recompile forever. The structural lesson (two-level: always-on cheap profiling + threshold-gated expensive recompute + anti-thrash guard) is domain-general.
- **Applies to:** moe · **Metric:** HotSpot Tier4CompileThreshold; deopt rate-limit (anti-thrash) · **Confidence:** high · **Rig relevance:** 3/5
- **Design implication:** Adopt the two-level structure with an EXPLICIT anti-thrash guard so an oscillating workload doesn't re-trace forever; the cheap tier is the per-iteration miss-rate/divergence counters, the expensive tier is the trace+recalibrate.
- **Verify:** verdict=confirmed-with-fixes | cross-domain analogy (HotSpot tiered compilation); canonical, attribution-cited, not re-fetched; both LLM lenses PLAUSIBLE. Provides the anti-thrash design pattern.
- **Sources:** [Runtime profiling in OpenJDK's HotSpot JVM](https://developers.redhat.com/articles/2021/11/18/runtime-profiling-openjdks-hotspot-jvm) — Red Hat Developer (OpenJDK HotSpot) 2021; Tier4CompileThreshold; rate-limited deopt; PARTIAL

### Turnkey trace alternatives: SGLang ExpertDistributionRecorder + vLLM --enable-eplb · `supporting` · technique
**If llama.cpp instrumentation is too costly, SGLang ships an ExpertDistributionRecorder (per-layer physical-expert selection counts for EPLB) and vLLM's --enable-eplb records expert load over a rolling window (default 1000 engine steps) — both produce the L×E table directly.**
SGLang PR #4957 ('Expert distribution recording without overhead for EPLB', author fzyzcjy) adds the recorder; Agent-sourced docs give the '--expert-distribution-recorder-mode stat' aggregate mode. vLLM's --enable-eplb (--eplb-config window_size=1000, step_interval=3000, log_balancedness) collects per-forward-pass load. The trace engine need not be the serving engine.
- **Applies to:** vllm; moe · **Metric:** vLLM eplb window_size default 1000 steps; SGLang recorder 'without overhead' (PR claim) · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** A cross-engine calibration path: run a representative trace through SGLang/vLLM to get the L×E table, then apply the per-layer/per-expert plan to a llama.cpp serve. Secondary to the in-llama.cpp eval-callback path (we are llama.cpp-first).
- **Verify:** verdict=confirmed-with-fixes | oracle: SGLang recorder EXISTS (#4957 'without overhead') + vLLM --enable-eplb/window_size=1000 CONFIRMED; DROPPED vLLM EXPERT_MAP_RECORD (absent from docs); exact SGLang flag string is docs-sourced, not PR-confirmed.
- **Sources:** [Expert distribution recording without overhead for EPLB (SGLang PR #4957)](https://github.com/sgl-project/sglang/pull/4957) — fzyzcjy (sgl-project/sglang) 2026; PARTIAL ; [Expert Parallel Deployment (EPLB) — vLLM documentation](https://docs.vllm.ai/en/latest/serving/expert_parallel_deployment/) — vllm-project/vllm 2026; window_size=1000, step_interval=3000 (defaults); SUPPORTED

