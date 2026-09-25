# Wave 4 — Per-expert adaptive calibration: the implementation layer

**KB:** docker-knowledge · **lane:** moe-placement · **date:** 2026-06-04 · backs `gpu-container` (the flagship's deep half)

Wave-1 (feasibility) established that MoE tiered offload *works* in adjacent tools (Fiddler, KTransformers, llama.cpp `--n-cpu-moe`) and that the load-bearing techniques exist: request-level skew, staleness eviction, router-lookahead, cold-NVMe gating. This wave goes one level deeper — **how do we actually realize per-expert hot/warm/cold tiering on a stock-GGUF llama.cpp stack?** Four load-bearing questions, one research agent each (web-grounded), then a 3-lens reasoning-stripped verification (retrieval oracle + `mistral-small:24b` + `granite4.1:30b`).

> **The headline (and the pivot):** stock llama.cpp **cannot** statically place an individual expert. A layer's experts are one fused tensor; `-ot` is per-layer. Per-expert tiering is therefore a **runtime cache**, not a launch flag — and there is an active upstream feature request (`#20757`) for exactly that cache, with a PoC at 12–14 tok/s. This reframes the per-expert lane from "emit a clever `-ot` plan" to "build (or ride) the runtime expert-slot cache."

## Research grounding (the empirical floor)

Each finding is `name — source(s) — design implication`. Full sources + verifier notes in `research-raw.json`; per-citation adjudication in `verification.md`.

**Placement granularity (the gate)**
1. **A layer's experts are one fused tensor; `-ot` is per-layer, never per-expert.** slaren, *llama.cpp #11397* (2025) + GLM-4.6 dump `ffn_gate_exps {5120,1536,160}`. → The planner's static schema emits tensor-name globs, not expert indices.
2. **Per-expert tiering must be a runtime cache at the `#20757` hook point.** *llama.cpp #20757* (2026): byte-offset sub-row copy, *"no slot remapping, no persistence… hook point for the cache,"* proposes `--moe-expert-cache-size N` + `expert_id→slot` map + pluggable eviction, PoC **12–14 tok/s vs 0.5–1**. → This is the Phase-2 build target and gpu-container's novel contribution.
3. **`-ot` *does* pin shared/attention to VRAM and route experts to CPU/RAM.** *llama.cpp #13154* (2025). → The hot-VRAM tier (shared/attn/router) ships today as one flag; only the routed-expert sub-split is deferred.
4. **`--n-cpu-moe` is per-layer and CPU-*computes* offloaded experts.** Doctor-Shotgun guide (2025, non-primary) + tensor-engine-knowledge. → Two-regime cost model: CPU-compute at decode, PCIe-stream at prefill (batch ≥ `GGML_OP_OFFLOAD_MIN_BATCH` 32).

**Activation-trace extraction (the input)**
5. **No built-in trace; capture via `eval-callback` on the top-k/argsort routing tensor → L×E histogram.** *llama.cpp #20757 / examples/eval-callback* + MoE-Infinity EAM (Leyang Xue et al. 2024, arXiv:2401.14361, <1% overhead). → Ship a `cb_eval` calibration harness emitting an L×E integer matrix (KBs), not per-token logs.
6. **Turnkey alternatives: SGLang `ExpertDistributionRecorder` + vLLM `--enable-eplb`.** *sglang #4957* (2026) + *vLLM EPLB docs* (`window_size=1000`). → A cross-engine calibration path; secondary to the in-llama.cpp callback (we're llama.cpp-first).

**Eviction + prefetch mechanism (the policy), and the stock-model line**
7. **Least-Stale = stale/current-queue partition, evict stale first; key `(stale-flag, layer-index)`.** SpecMD, Hoang/Jaiswal/Samragh/Cho (Apple) 2026, arXiv:2602.03921. **2.6–8.6× fewer collision misses (up to 85× best-case), >88% hit at ~5% cache.** → The runtime cache uses Least-Stale, not LRU/ARC, for expert slots.
8. **Cross-layer-gate prefetch works on STOCK models** (run layer *i+1*'s existing router on layer *i*'s state; adjacent layers >83% similar). Fate, Fang 2025 (arXiv:2502.12224) **~99% hit, no retrain**; AdapMoE, Zhong 2024 (arXiv:2408.10284) **1.35×, unmodified**. → Warm-tier prefetch is realizable on stock GGUFs; make tiering **depth-aware** (pin shallow layers 0–3 hot).
9. **Scope line: Pre-gated needs a fine-tuned model (OUT); MoE-Beyond needs a trained predictor (DEFERRED).** Pre-gated, Hwang 2023 (arXiv:2308.12066, body: *"change the MoE model architecture"* + *"incrementally trained during the fine-tuning stage"*); MoE-Beyond, Gavhane 2025 (arXiv:2508.17137, **17%→72%** but a trained predictor). → v1 = cross-layer gate (free); exclude Pre-gated; defer MoE-Beyond.

**Recalibration cadence (closing the loop)**
10. **Recalibrate on DRIFT, not a timer.** MoE-Infinity (request-level skew → static histogram is trace-only valid) + ADWIN (Bifet & Gavaldà 2007, δ=0.002) / DDM (Gama 2004, 2σ/3σ). → Re-trace fires on a confirmed drift step-change: warm-tier miss-rate detector **+** JS/χ² histogram divergence.
11. **Between re-traces, self-tune the split for free** (EWMA/hyperbolic heat scores; ARC ghost lists — Megiddo & Modha 2003; LeCaR — Vietri 2018, best when cache ≪ working set). → Continuous cheap update absorbs gradual drift; a rising ghost-hit rate is itself a drift signal.
12. **The cadence mirrors tiered JIT** (HotSpot: cheap always-on counters, expensive recompile on threshold, anti-thrash guard — Red Hat 2021). → Two-level structure + an explicit "re-trace within N tokens" thrash guard.

## Recommendations for gpu-container (→ reconciled into `docs/moe-lane-architecture.md`)

- **Reframe milestone-5-routing:** the per-expert routing half is NOT `-ot` + traces — it is a **runtime expert-slot cache** (the `#20757` layer) with Least-Stale eviction + cross-layer-gate prefetch. `-ot` delivers only the per-layer split + the shared/attention-in-VRAM hot tier.
- **Ship the cheap wins now:** the hot tier (shared/attn/router in VRAM, routed experts per-layer to CPU/RAM) is expressible as `-ot` today (finding 3).
- **Calibration input = `cb_eval` L×E histogram** (finding 5), <1% overhead; the receipt stores the matrix.
- **Prefetch = cross-layer gate on stock GGUFs** (finding 8); EXCLUDE Pre-gated, DEFER MoE-Beyond (finding 9).
- **Cadence = drift-gated** (findings 10–12): miss-rate detector + histogram divergence trips the re-trace; EWMA/ghost-list self-tuning between; anti-thrash guard.
- **Cost model** distinguishes CPU-compute (decode) from PCIe-stream (prefill) (finding 4).

## Verification summary

3-lens, reasoning-stripped, **0 fabrications**. Both ollama families confirmed UP before the pass (ANDON gate passed, not skipped). Corrections: MoE-Infinity author Xie→**Xue** (oracle); Pre-gated year 2024→**2023**; SpecMD "85×" → **"2.6–8.6× typical, up to 85× best-case"** (both LLM lenses flagged + oracle "up to" framing). Dropped as CANNOT_CONFIRM (non-load-bearing): vLLM `EXPERT_MAP_RECORD` (absent from docs), arXiv:2511.05814's "routing-mass" framing (paper proposes LFU). Detail: `verification.md`.

## Standards compliance (the six workflow standards)

| Standard | Score | Evidence |
|---|---|---|
| PIN_PER_STEP | **2** | Each research question → one agent with a fixed prompt + fixed output schema; verifier models pinned by id (`mistral-small:24b`, `granite4.1:30b`) with captured `run_id`s; `research-raw.json` is the replayable load artifact. Not byte-replayable (agent prompts not hashed) → not 3. |
| ANDON_AUTHORITY | **3** | Verifier-availability gate enforced (both models confirmed UP via `ollama list` before the pass); FABRICATED→drop, MISATTRIBUTED→correct (Xue/Xie, year), CANNOT_CONFIRM→drop-from-load-bearing (2 sub-claims) all applied this run. |
| NAMED_COMPENSATORS | **2** | The only world-touching act is writing this wave + loading the DB — both reversible (`git revert`; `load_db.py` is idempotent-per-wave, re-run replaces wave-4's rows). No irreversible external call. Commit gated on the director. |
| DECOMPOSE_BY_SECRETS | **2** | Stable module = the loader schema + lane taxonomy + sourcing standard; volatile = the 4 questions + the 12 findings. One agent per question hides each search strategy behind a boundary. |
| UNCERTAINTY_GATED_HUMANS | **2** | The architectural pivot (per-expert → runtime cache) + the dropped sub-claims are surfaced to the director with a contrastive frame ("the design assumed `-ot` per-expert; it can't — here's why"), gating the design-doc direction on review. |
| EXTERNAL_VERIFIER | **3** | Citation verification is a different model family from the synthesizer (Claude), reasoning-stripped, with a retrieval-oracle existence floor; the two ollama families ran on bare claims only; 0 fabrications, real corrections made. First docker-knowledge wave to use the family-different upgrade CONVENTIONS.md names. |

**Total: 14 / 18.** No score below 2; no remediation owed. (Compensators: no skip — reversible writes + director-gated commit.)

## Artifacts
`research-raw.json` (the load source) · `verification.md` (the 3-lens receipt) · this `dispatch.md`. Loaded via `scripts/load_db.py waves/wave-04-per-expert/research-raw.json` → `gen_catalog.py` → `gen_loadout.py`.
