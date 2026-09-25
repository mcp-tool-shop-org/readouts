# Wave 4 — Verification receipt

3-lens, reasoning-stripped (study-swarm Step 4), applied to every load-bearing citation before any finding connected to architecture.

## Method
1. **Retrieval oracle** (`WebFetch`/`WebSearch`, in-session) — existence + attribution + content-groundedness. The load-bearing lens (these are arXiv papers + GitHub PRs/issues + vendor docs). Every load-bearing source fetched: 7 arXiv abstracts, the Pre-gated **body**, 6 llama.cpp/SGLang/vLLM pages, ARC.
2. **mistral-small:24b** (Mistral) — family-different groundedness, reasoning-stripped (bare numbered claims only; no agent `detail`/reasoning). `run_2026-06-04T16-13-28_2720b3`.
3. **granite4.1:30b** (IBM Granite) — family-different groundedness, reasoning-stripped. `run_2026-06-04T16-13-54_2f5c63`.

**ANDON note:** both ollama families confirmed UP (`ollama list` → 0.24.0; `mistral-small:24b` 14 GB + `granite4.1:30b` 17 GB present) BEFORE the family pass. Gate passed, not skipped. Had either been unreachable: HALT-and-restore (never read absence as "fine").

## Verdict distribution
**12 consolidated findings; ~30 raw agent findings; ~20 distinct sources checked.**
- **Retrieval oracle:** all 7 arXiv papers EXIST with corrected attributions; all load-bearing llama.cpp/SGLang/vLLM pages resolved; **0 fabricated, 0 not_supported.** Several PARTIALs = abstract-silent-but-body-supports (Fate/AdapMoE/Pre-gated specifics) or scope-narrowed sub-claims.
- **granite4.1:30b:** 13/14 PLAUSIBLE, 1 DOUBTFUL (SpecMD 85×), **0 contradictory.**
- **mistral-small:24b:** 10/14 PLAUSIBLE, 3 DOUBTFUL (incl. SpecMD 85×, claim-2 persistence, claim-14 JIT), 1 CONTRADICTORY (claim-8 "no retraining").

## Family-different outcome
- **0 genuine refutations; 0 fabrications across all three lenses.** No finding HALTed.
- **mistral's lone CONTRADICTORY (claim 8 — cross-layer gate "no retraining"):** overridden — Fate's abstract ("without additional GPU overhead," reuses the native router) and AdapMoE ("no additional finetuning") are two independent primary sources confirming the stock-model claim; the oracle read both. This is the documented LLM blind spot (conflating "predict experts" with "train a predictor"), exactly why the retrieval oracle is the floor.
- **Both families flagged SpecMD "85×" as exaggerated-looking** — a *correlated* doubt that the oracle adjudicated: "up to 85×" IS the abstract's stated maximum, with 2.6–8.6× in the per-config body. Resolution: lead with the conservative range, keep 85× as labelled best-case. (Submodular-coverage in action — the union of oracle + two families produced the honest number neither lens alone would.)

## Material actions (corrections + drops)
- **MISATTRIBUTED → corrected:** MoE-Infinity first author **Xie → Xue** (Leyang Xue et al.) — two research agents carried "Xie"; the oracle (arXiv:2401.14361) fixed it. Agent-4's title variant ("Offloading-Efficient MoE Model Serving") also dropped for the canonical title.
- **Year fixed:** Pre-gated **2024 → 2023** (arXiv 2308; ISCA'24 is the venue).
- **Reframed (number):** SpecMD **"85×" → "2.6–8.6× typical, up to 85× best-case"** + ">88% hit / 34.7% TTFT."
- **DROPPED as CANNOT_CONFIRM (non-load-bearing, surfaced contrastively):**
  - vLLM **`EXPERT_MAP_RECORD` / `expert_map_record_path`** dump path — absent from the current EPLB docs the oracle fetched. The load-bearing `--enable-eplb` recorder stands.
  - arXiv:**2511.05814** "routing count vs routing mass / per-layer scores suffice" — paper EXISTS (Lin 2025) but its abstract proposes *LFU*; the specific framing isn't confirmed. The L×E-histogram conclusion is carried by MoE-Infinity instead.
  - The `mintlify.com/...llama.cpp` URL (an agent's eval-callback source) — not cited; the callback-returns-bool fact stands on `examples/eval-callback` (primary).
- **Honesty flags retained in `research-raw.json`:** the exact MoE routing-node `->name` was not pinned this run (one-grep in `build_moe_ffn`, `src/llama-graph.cpp`); DDM/LeCaR/Hyperbolic/HotSpot are canonical adjacent-domain citations attribution-cited but not individually re-fetched this run (`exists_verified=0`, both LLM lenses PLAUSIBLE) — load-bearing cadence rests on the oracle-verified MoE-Infinity + ADWIN (agent-retrieved) + ARC (oracle-verified).

## Consolidation
~30 raw findings from 4 parallel research agents → **12 distinct KB findings** (the lanes converged on the same load-bearing facts; cross-agent convergence is signal, stored once). Sources pulled from the agent output and deduped by URL.

## Artifacts
`research-raw.json` (loaded by `scripts/load_db.py`) · `dispatch.md` (narrative + Standards) · this receipt. Verifier run-ids: mistral `run_2026-06-04T16-13-28_2720b3`, granite `run_2026-06-04T16-13-54_2f5c63`. Execution: in-session study-swarm (parallel Agent research dispatch + manual oracle/family verification — the protocol's documented fallback path, family-different + reasoning-stripped).
