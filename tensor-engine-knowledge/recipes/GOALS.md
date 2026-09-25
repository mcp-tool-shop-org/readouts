# Recipe layer — goals (caveats turned into work)

The three "caveats" from the backfill are not defects — they're the honest current state. Each is
a goal with an acceptance test. Status as of this pass.

## Goal 1 — Reproducible pins (vendoring)
**Was:** all 205 `recipe_artifacts` are `store_expect='index'` → the resolvability floor correctly
flags every one as *not reproducible* (a URL+hash against a curated index 404s when the channel
moves; cu128 is the proof).
**Goal:** every pin a recipe actually uses is content-addressed — `store_expect ∈ {local-vendored,
mirror}` with a verified `sha256` — so `resolvable_ok=1` is *earned*, not assumed.
**Acceptance:** provisioned recipes have vendored pins + sha256 + `resolvable_ok=1`; anything still
`index`-only is explicitly surfaced as not-yet-reproducible (never silently "pinned").
**First step / owner:** the engine-room executor vendors a recipe's pins into `_artifact-cache/<sha>`
on first successful provision (PIN_PER_STEP); a proactive pass can pre-vendor the top recipes'
wheels/images. **Status: NOT STARTED** — `index` is the correct honest value until then.

## Goal 2 — Confident classification (no `?`)
**Was:** 21 recipes carry a `?` verify_note (low-confidence `recipe_kind` — profiling-bench,
runtime-foundations).
**Goal:** 0 recipes with a `?`; every `recipe_kind` defensible.
**Acceptance:** no `verify_note LIKE '%?%'`; spot-check correct per kind.
**First step:** deterministic reclassification of the clear ones (TensorRT → onnx-compile producer;
llama.cpp-foundations → launchable-server; profiling tools/receipts → batch-producer). Genuinely
ambiguous cases get a sharpened note, not a forced fit. **Status: IN PROGRESS this pass.**
*Open refinement:* the profiling **baseline** rows (idle / qwen3 / soak / loadout) are measured
*receipts*, better modeled as `recipe_baselines` than as standalone recipes — noted for a later pass.

## Goal 3 — Enriched + verified recipes
**Was:** nuance enrichment pending; `verified=0` on every recipe (the groundedness panel hasn't run
over the recipe layer; `config_recipes` never had a `verified` column).
**Goal:** each recipe carries a one-line `summary` and a `verified` flag set by the family-different
groundedness panel; ambiguous kinds resolved.
**Acceptance:** `summary` populated; `verified` set by the panel; resolvability floor run.
**First step:** the ollama-intern enrichment pass (summaries + ambiguous-kind resolution + groundedness).
**Status: PARTIAL.**
- *Summaries:* ✅ 160/160 on qwen3.6:35b-a3b (local, zero Claude tokens).
- *Verified:* a 3-family panel (Mistral/Granite/Gemma) audited `recipe_kind` by end-state. It
  **confirmed 64** (backfill+panel agree → `verified=1`) but **auto-corrected 89** — a 56% change
  rate that meta-verification (reading corrections vs bodies) showed was **~25% wrong** (a correlated
  TRAINING blind spot: kohya/unsloth *produce* a LoRA = batch-producer, but the panel moved them to
  launchable on vllm/install keywords) **+ ~25% out-of-taxonomy** force-fits. So the 89 were
  **reverted** to baseline (`verified=0`, panel suggestion recorded for review). Doctrine working:
  EXTERNAL_VERIFIER (panel) → meta-check → ANDON (don't propagate) → surface to human.
- *Resolved (3-method consensus):* a deterministic END-STATE classifier (encoding the panel's
  lessons: training→producer, serving→launchable, routers→router-fleet, kernels/toolchain→modifier)
  became the **third** classifier. `verified=1` now = the end-state kind agrees with backfill OR the
  panel (≥2 of 3 mechanistically-different methods): **112/127 executable recipes verified**, **15
  flagged** as genuine 3-way splits (offload-as-launchable-vs-modifier; KTransformers; a few
  profiling tools). Sanity-checked on knowns (vLLM→launchable, kohya→producer, litellm→router,
  sageattention→modifier, tensorrt→producer). **Status: DONE.**

## Goal 4 — Taxonomy carve-out (DONE)
~15–20 `config_recipes` are **not engine recipes** and don't fit the 4 kinds — the panel force-fit
them and so did the backfill: **measurement receipts** (profiling baselines/loadouts/soak/idle/
context-capability → belong as `recipe_baselines`, not standalone recipes) and **tooling/reference**
(the `offload` CLI, the producer→format→consumer decision matrix, the verifier/NLI/offload-wiring
notes → arguably outside the engine-recipe layer's scope).
**Done:** added an `executable` flag (SQLite can't extend the `recipe_kind` CHECK in place). **33
rows carved to `executable=0`** — 13 profiling-bench measurement receipts + 20 tooling/reference
(the `offload` CLI, verifier/NLI wiring, decision matrices, the survival card). engine-room only
provisions `executable=1` (127 rows). Receipts stay queryable; *refinement* (move their measured
numbers into `recipe_baselines` keyed to the engine they measured) is a later, optional pass.
**Status: DONE.** (Carve patterns are precise — bare `offload` was fixed so it no longer eats
RAM/CPU-offload *engine* recipes.)

## Goal 0 — Integration + regen (consolidation)
Fold the recipe DDL into canonical `schema.sql`, extend `load_db.py` + the shared `gen_catalog.py`
to ingest/render the recipe layer, then regenerate the readouts.
**Status: HELD** — runs at the shared regen point *after* the measurement session's wave lands, to
avoid a regen under live edits. Cross-KB `recipe_techniques` re-syncs via `_link_techniques.py` then.
