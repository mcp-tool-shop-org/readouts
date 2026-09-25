# sprites-knowledge

**Status:** Waves through 5 (STUDY-059 leftover minus 486 2026-09-07). Catalog **215 · 162/215 · 6 waves**. Flip 486: 0. Recipes invented: 0.
- **Wave 5 (STUDY-059 leftover minus 486)** — [dispatch](waves/wave-05-study-059-leftover-minus-486/dispatch.md) · [research-raw](waves/wave-05-study-059-leftover-minus-486/research-raw.json) — 22 recipes verified=0; flip 486: 0; Analogist #1–#2 paywall unverified; #7–#8 fail-transfer omitted.
- **Wave 4 (STUDY-038 pose-control deepen)** — [dispatch](waves/wave-04-study-038-pose-control-deepen/dispatch.md) · [research-raw](waves/wave-04-study-038-pose-control-deepen/research-raw.json) — 13 recipes verified=0; flip 486: 0.
> The portable **concept-art → game-ready 2.5D JRPG sprite** craft for this rig
> (OMEN 45L · RTX 5090 · Blackwell sm_120 · 32 GB VRAM · Windows 11 / WSL2 — the only machine).

KB #5 of the [readouts](../README.md) monorepo. The primary entity is a **recipe**: a sprite-pipeline
*procedure or model choice* plus its *proof*. Each recipe answers "how do I turn a concept-art frame into a
finished game sprite, and how well does this exact approach work on this exact rig?"

Sibling KBs own the layers this one points at, never restates:
- [model-knowledge](../model-knowledge/catalog/README.md) — the *weights* (base models, recon models); linked via `base_model_slug`.
- [tensor-engine-knowledge](../tensor-engine-knowledge/catalog/README.md) — the *software* + rig-measured it/s & VRAM peaks; linked via `engine_recipe_ref`.
- [training-knowledge](../training-knowledge/catalog/README.md) — the *training craft* (LoRA recipes, hyperparameters).

## The 7 lanes

The sprite pipeline, source-to-screen, partitioned into the seven domains a wave dispatches against
(`categories`, seeded by `schema.sql`):

| Lane (`slug`) | What it owns |
|---|---|
| **Mesh-path 360** (`mesh-360`) | Single image → textured 3D mesh → rendered multi-direction sprites. The recon-model landscape + the proven TRELLIS.2 path. |
| **Render & lighting** (`render-light`) | Blender headless render: camera-parented rig, color-management/tonemap per character value, render passes, outline/toon. |
| **Downsample & pixel finish** (`downsample-finish`) | 512px master → 48/64px game sprite: Lanczos/area downscale, foot-anchor, union bbox, quantization/dithering, palette. |
| **NVS-direct turnaround** (`nvs-direct`) | Image → multiple consistent 2D views via multi-view diffusion / novel-view synthesis. License-decisive (Zero123 lineage is non-commercial). |
| **Diffusion sprite-sheet direct** (`sheet-direct`) | Text/image → sprite sheet or 8-direction set directly via diffusion: charturn + pixel-art LoRAs, ControlNet pose sheets. |
| **Sprite evaluation / QA gate** (`eval-qa`) | Grounded evaluators (SigLIP2/CLIP), turnaround-consistency + perceptual metrics, AI-judge gates for an automatable sprite verifier. |
| **Animation & locomotion** (`animation-locomotion`) | Walk cycles / locomotion / frame sequences: auto-rig + animated render, image-to-animation diffusion, interpolation. |

## Proven vs research — the spine of this KB

Every recipe carries an ordinal `evidence_strength`. It is the load-bearing axis: it stops a single reported
community claim from wearing the authority of an on-rig measurement.

```
measured-on-rig  >  reproduced-from-source  >  single-reported-run  >  community-claim  >  untested
   ▣ PROVEN                          └────────────────── RESEARCH ──────────────────┘
```

- **Proven** = `evidence_strength = 'measured-on-rig'` — validated on *this* machine, with `measured_conditions`
  recording the exact rig/env. This is the half you can build production on today.
- **Research** = everything else — study-swarm sourced, web-grounded, retrieval-verified, but **not yet rig-measured**.
  Trustworthy leads to measure next, not yet production-blessed.

A second decisive axis is **license** (`commercial_use` ∈ yes/conditional/no/unknown): a sprite inherits its base
model's and recon model's license. The Zero123 NVS lineage being non-commercial is the canonical trap this KB flags.

## How to query

Open `recipes.db` (SQLite, WAL). The catalog markdown under [`catalog/`](catalog/README.md) is generated from it —
never hand-edit those. Useful views:

```sql
-- The proven half: recipes measured on this rig.
SELECT * FROM v_proven;

-- The research half: study-swarm leads not yet rig-measured.
SELECT * FROM v_research;

-- Try-first picks per lane (recommended + runner-up, ordered by download_priority).
SELECT * FROM v_recommended;

-- Best recipe per purpose (ranked).
SELECT * FROM v_best_for;

-- Multi-stage pipeline chains (predecessor → stage_order).
SELECT * FROM v_pipeline;

-- Full-text search across slug/name/engine/applies/base/summary/claim/category.
SELECT r.name FROM recipes r JOIN recipes_fts f ON f.rowid = r.id WHERE recipes_fts MATCH 'turnaround';
```

For agents, route via ai-loadout — the root loadout picks this KB, then this KB's own
[`.claude/loadout/index.json`](.claude/loadout/index.json) picks the lane slice (two-level progressive disclosure):

```
ai-loadout resolve --project .
```

## Growing the KB (waves)

A wave is a parallel research dispatch (one agent per lane), web-grounded and sourced, then adversarially
retrieval-verified before it is trusted. The verified output is staged at `waves/wave-NN-name/research-raw.json`
(`{ wave, date, title, domain_scope, agent_count, verifier_note, lanes:[{laneSlug, recipes:[…]}] }`), then ingested.

Ingestion is **idempotent per wave** — re-running a wave file fully replaces that wave's rows and leaves other
waves untouched. Run Python with UTF-8 forced (entries carry em-dashes the default Windows codepage chokes on):

```powershell
$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'

# Ingest one wave (idempotent):
python scripts/load_db.py waves/wave-01-foundation/research-raw.json

# OR rebuild everything from recipes.db — discovers every waves/*/research-raw.json,
# ingests each, regenerates catalog + loadout, refreshes the root routers, validates:
python scripts/regen.py
```

`scripts/`:
- `load_db.py` — idempotent wave ingester (research-raw.json → recipes.db; two-pass predecessor resolution; rebuilds FTS; updates meta currency).
- `gen_catalog.py` — `recipes.db` → `catalog/*.md` (DB-only; never hand-edited).
- `gen_loadout.py` — `recipes.db` → `.claude/loadout/index.json` (progressive-disclosure router).
- `refresh_meta.py` — derives `meta.latest_wave`/`updated` from `MAX(waves.wave_number)` and asserts they agree (no stale currency pointer).
- `regen.py` — one-command rebuild of every derived artifact from `recipes.db`.

## Provenance

Every recipe carries a `wave_id` (waves append; nothing silently overwrites) and a `verified` flag; every claim
links to a `source` with a retrieval-checked `{url, claim}`. Verification is currently a same-family verifier plus a
retrieval oracle (the live page decorrelates what a parametric model can't catch); the planned upgrade is a
family-different local non-Claude verifier on the rig.
