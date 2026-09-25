# Wave 1 — Feasibility: is gpu-container's explicit-placement planner buildable?

**Study-swarm wave 1** · dispatched 2026-06-04 · 5 questions · 11 agents · seeded from the gpu-container feasibility swarm `wf_965f110f-e24`. **Verdict: PASS, with three required calibrations.** Full synthesis: the product repo at github.com/mcp-tool-shop-org/gpu-container (`docs/feasibility.md`).

## Context
- **Rig:** OMEN 45L · RTX 5090 · Blackwell sm_120 · 32 GB VRAM · 64 GB RAM · Windows 11 / WSL2. GPU-in-container passthrough smoke-tested green.
- **Product:** a model-aware planner that profiles the rig + model, emits an explicit VRAM / pinned-RAM / NVMe placement plan across runtimes, proves it with a measured receipt, and refuses below 1 tok/s. NOT "Docker VRAM overflow."
- **Method:** 5 web-grounded research lanes → a 3-lens, reasoning-stripped verification (retrieval oracle + two local non-Claude families). Receipt → [verification.md](verification.md).

## The verdict, by lane
- **MoE placement (the flagship).** Warm-tier offload is production-proven (Fiddler >3 tok/s Mixtral-8x7B on 24 GB; KTransformers ~8.7–10 tok/s DeepSeek-V3 671B; llama.cpp `--n-cpu-moe` ~12–14 tok/s). Cold-NVMe is gated (SSD ~12x energy; needs prefetch + sparsity). Two design constraints fell out: calibration must be **adaptive** (skew is request-level), eviction must be **staleness-aware** (not LRU).
- **Container-runtime (the moat).** NVIDIA's own docs confirm there is **no UVM oversubscription on Windows/WSL2**, and that UVM is the wrong tool for decode even on Linux. Explicit placement is the only honest route.
- **Throughput prediction.** Memory is exact; throughput is ~10%-predictable in-VRAM (Vidur 3.33% P95) but only ~1.5–2x under heavy NVMe → scope the receipt.
- **Dense offload.** Tiers off a cliff to sub-1 tok/s once weights stream from NVMe; RAM-offload partial is the serviceable envelope.
- **Refusal / receipt.** The >1 tok/s floor is correctly calibrated and will refuse dense+NVMe often — by design.

## The three required calibrations (feed Phase 1)
1. **Adaptive + staleness-aware MoE calibration** — NOT a static histogram + LRU.
2. **Scope the ±10% receipt** to in-VRAM/light-offload; heavy-NVMe = "estimated, receipt-confirmed".
3. **Dense+NVMe ⇒ expected refusal**; NVMe is the cold-MoE-expert lane, not a dense-weight lane.

## Method, confidence, deferred
- 35 unique sources, 0 fabricated. The verifier corrected ~8 sub-figures and dropped 1 misattribution + 1 unsupported source — see [verification.md](verification.md).
- **Deferred to wave 2** — the `container-runtime` + `hw-measurement` gap: how to measure VRAM / PCIe / NVMe (seq + rand QD1) / pinnable-RAM **truthfully from inside a WSL2 GPU container**. This wave seeded the methodology lanes; wave 2 fills the measurement lane the Milestone-1 profiler depends on.
