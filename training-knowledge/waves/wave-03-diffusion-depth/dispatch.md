# Wave 3 — Diffusion depth (SDXL + Flux + dataset + eval)

> Study-swarm dispatch · 2026-06-06 · training-knowledge KB · the priority loop.

**Goal:** rebalance the KB toward the studio's #1 workload. After wave 2 deepened `llm-finetune` (15), the SDXL/Flux style-LoRA loop was the thinnest part of the KB — so wave 3 goes DEEP on the four diffusion-loop lanes.

**Method:** 4 deep lane researchers (web-grounded) → one Sonnet adversarial verifier per lane with a **dedup-vs-wave-1 lens** (each agent read the existing lane techniques first and EXTENDED, never restated; the verifier refuted any duplicate). RESEARCH wave — the GPU was busy, so nothing measured; evidence is reproduced-from-source / community-claim, tagged honestly.

**Result:** **27 new techniques** (all verified, 0 refuted, 0 duplicates). Lane depths after: SDXL 12, Flux 10, dataset-caption 10, evaluation 10.

**Coverage added** (the completeness-critic's diffusion gaps): optimizer×LR-schedule matrix + warmup as a first-class axis, multi-concept/multi-folder balancing, checkpoint selection & save cadence, network-type choice (LoRA/LoCon/LoKr/DoRA), noise/schedule levers, adapter merge/resize/extraction, inference-side validation settings; Flux guidance-distilled-base training, timestep/shift schedules, NL-caption depth, fp8/bf16 tradeoffs; dataset balancing/dedup/size-scaling/Datasheets; eval candidate-comparison grid, CMMD vs preference vs perceptual metrics, overfitting/replication detection, ai-eyes A/B wiring.

## Wave-3 evidence-strength distribution

| Tier | Count |
|---|--:|
| reproduced-from-source | 22 |
| community-claim | 5 |
