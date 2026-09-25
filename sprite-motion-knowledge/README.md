# sprite-motion-knowledge

**Status:** Waves through 8 (STUDY-058 leftover minus prism 2026-09-07). Catalog **246 · 178/246 · 8 waves**. Flips 33/117/486: 0. Recipes invented: 0.
- **Wave 8 (STUDY-058 leftover minus prism)** — [dispatch](waves/wave-08-study-058-leftover-minus-prism/dispatch.md) · [research-raw](waves/wave-08-study-058-leftover-minus-prism/research-raw.json) — 22 recipes verified=0; flips 33/117/486: 0; recipes invented: 0; Analogist #7–#8 fail-transfer omitted.
- **Wave 7 (STUDY-037 leftover craft)** — [dispatch](waves/wave-07-study-037-leftover-craft/dispatch.md) · [research-raw](waves/wave-07-study-037-leftover-craft/research-raw.json) — 17 recipes verified=0; flips 33/117/486: 0.
> The portable **animate-the-sprite** craft for this rig
> (OMEN 45L · RTX 5090 · Blackwell sm_120 · 32 GB VRAM · Windows 11 / WSL2 — the only machine).

KB #9 of the [readouts](../README.md) monorepo. The primary entity is a **recipe**: a sprite-*motion*
procedure or model/tool choice plus its *proof*. Each recipe answers "how do I make an approved 2.5D JRPG
sprite walk, swing, idle, and die — without melting the character or detaching the weapon — and how well does
this exact approach hold up?"

This is the **animation layer atop [sprites-knowledge](../sprites-knowledge/catalog/README.md)** (KB #5, which
owns *static* concept-art → 2.5D sprite generation). The spine is one idea:

```
motion truth (rig / mesh / proxy)  ->  AI polish / inbetween / repaint  ->  sprite-sheet export  ->  local verify
   ▣ deterministic                        ◐ generative ceiling                                       ✓ admission gate
```

That is the **same insight the studio proved for rigid weapons** (the §D weapon-drift fix: no diffusion method
rotates a rigid held prop, so the prop must be rigid in 3D — a mesh/proxy — then repainted to the painterly
house style), extended from a static turnaround to walk / attack / hurt / death motion. It is *not*
"AI video → sprite sheet" — that drifts, mutates faces, and makes combat mushy.

Sibling KBs own the layers this one points at, never restates:
- [sprites-knowledge](../sprites-knowledge/catalog/README.md) — the *static sprite* the motion animates.
- [model-knowledge](../model-knowledge/catalog/README.md) — the *weights* (base/motion/recon models); linked via `base_model_slug`.
- [tensor-engine-knowledge](../tensor-engine-knowledge/catalog/README.md) — the *software* + rig-measured it/s & VRAM peaks; linked via `engine_recipe_ref`.
- [blender-knowledge](../blender-knowledge/catalog/README.md) — Blender 4.x recipes (rigging, headless render).

## The 7 lanes

The animation pipeline, partitioned into the seven domains a wave dispatches against (`categories`, seeded by
`schema.sql`):

| Lane (`slug`) | What it owns |
|---|---|
| **Motion architecture & contracts** (`motion-arch`) | The rig-truth-first doctrine; per-character animation contracts/manifests (views, frame counts, loop flags, anchors, layers); the 3-lane production model; one shared motion cage rendered per-direction, NOT 80 independent images. |
| **Rigging & skeletons** (`rigging`) | Blender armatures + 2.5D proxy/mesh rigs as the deterministic motion source: bone hierarchies, `hand → weapon_grip → weapon_tip` rigid-attach chains, auto-riggers (UniRig/Rigify/AccuRIG/Auto-Rig Pro/Mixamo). |
| **AI motion models** (`ai-motion`) | Models that propose or drive motion: video-diffusion + pose-conditioned generation, AnimateDiff, image-to-animation DiTs. **License-decisive** (research/academic-only weights are the trap). |
| **Inbetweening & interpolation** (`inbetween`) | Keyframe → tween generation: FILM, RIFE/Practical-RIFE, optical-flow interpolation; multiply sparse keyposes into a smooth cycle. |
| **Cloud GPU workers** (`cloud-workers`) | Run bigger-than-VRAM models as a pipeline worker: RunPod / Modal / fal.ai / Replicate / HF Endpoints; ComfyUI-as-serverless, cold starts, caching, cost. Source-of-truth stays in the repo. |
| **Combat animation craft** (`combat-craft`) | The designed-not-generated principles: anticipation → active/hit frame → follow-through → recovery; smears, hit-stop, readable silhouettes, attack timing. |
| **Motion verification & QA** (`motion-verify`) | The local verifier gate: root/anchor stability, foot-contact (no slide), hand-to-weapon attachment + weapon length/tip continuity, no frame-to-frame face mutation, silhouette readability, canvas consistency. |

## Proven vs research — the spine of this KB

Every recipe carries an ordinal `evidence_strength`. It stops a single community claim from wearing the
authority of an on-rig measurement.

```
measured-on-rig  >  reproduced-from-source  >  single-reported-run  >  community-claim  >  untested
   ▣ PROVEN                          └────────────────── RESEARCH ──────────────────┘
```

- **Proven** = `evidence_strength = 'measured-on-rig'` — validated on *this* machine (`measured_conditions`
  records the exact rig/env). Build production on this today. (The mesh-as-rigid-weapon captain prototype is
  the seed of this half.)
- **Research** = everything else — study-swarm sourced, web-grounded, **cross-family-jury verified**, but not
  yet rig-measured. Trustworthy leads to measure next, not yet production-blessed.

A second decisive axis is **license** (`commercial_use` ∈ yes/conditional/no/unknown): a motion clip inherits
its driving model's *and* base checkpoint's license. Research-only motion weights (and FLUX-Kontext-NC,
Hunyuan3D-restricted, Era3D-AGPL turnaround paths) are the canonical traps this KB flags.

## How to query

Open `recipes.db` (SQLite, WAL). The catalog markdown under [`catalog/`](catalog/README.md) is generated from
it — never hand-edit those. Useful views:

```sql
SELECT * FROM v_proven;       -- the proven half: motion recipes measured on this rig
SELECT * FROM v_research;     -- the research half: study-swarm leads not yet rig-measured
SELECT * FROM v_recommended;  -- try-first picks per lane (recommended + runner-up)
SELECT * FROM v_best_for;     -- best recipe per purpose (ranked)
SELECT * FROM v_pipeline;     -- multi-stage chains (predecessor -> stage_order)
SELECT r.name FROM recipes r JOIN recipes_fts f ON f.rowid = r.id WHERE recipes_fts MATCH 'weapon';
```

For agents, route via ai-loadout — the root loadout picks this KB, then this KB's own
[`.claude/loadout/index.json`](.claude/loadout/index.json) picks the lane slice (two-level progressive
disclosure): `ai-loadout resolve --project .`.

## Growing the KB (waves)

A wave is a parallel research dispatch (one agent per lane), web-grounded and sourced, then **cross-family
adversarially verified** before it is trusted. Each lane agent writes `waves/wave-NN-name/lanes/<slug>.json`;
`_assemble_lanes.py` wraps them into `research-raw.json`; `verify_cloud.py` re-adjudicates every recipe with a
PoLL jury of the biggest Ollama Cloud thinking flagships and sets the `verified` flag; then it is ingested.

Run Python with UTF-8 forced (entries carry em-dashes the default Windows codepage chokes on):

```powershell
$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'

# Per-lane research files -> research-raw.json:
python scripts/_assemble_lanes.py waves/wave-01-foundation --wave 1 --date 2026-06-24 --title "Foundation"

# Cross-family jury sets the verified flag (off-box; needs the Ollama Cloud daemon up):
python scripts/verify_cloud.py waves/wave-01-foundation/research-raw.json

# Rebuild everything from recipes.db — ingest every wave, regen catalog + loadout, refresh root, validate:
python scripts/regen.py
```

`scripts/`:
- `_assemble_lanes.py` — gather `waves/<wave>/lanes/*.json` → the wave's `research-raw.json`.
- `verify_cloud.py` — **the authoritative cross-family verifier**: a PoLL jury (deepseek-v4-pro / glm-5.2 / minimax-m3, disjoint families) sets `verified` refute-by-default (existence / license / claim-support / currency).
- `load_db.py` — idempotent wave ingester (`research-raw.json` → `recipes.db`; two-pass predecessor resolution; rebuilds FTS; updates meta currency).
- `gen_catalog.py` — `recipes.db` → `catalog/*.md` (DB-only; never hand-edited).
- `gen_loadout.py` — `recipes.db` → `.claude/loadout/index.json` (progressive-disclosure router).
- `refresh_meta.py` — derives `meta.latest_wave`/`updated` from `MAX(waves.wave_number)` and asserts they agree.
- `regen.py` — one-command rebuild of every derived artifact from `recipes.db`.

## Provenance

Every recipe carries a `wave_id` (waves append; nothing silently overwrites) and a `verified` flag; every claim
links to a `source` with a retrieval-checked `{url, claim}`. The `verified` flag is set by a **family-different
PoLL jury of the largest Ollama Cloud thinking reasoners** (Claude does the research; a disjoint-family jury
adjudicates — same-family judges over-rate via mechanistic self-preference). `verified=1` only when ≥2 jurors
confirm and none refute; refuted recipes are flagged `avoid` and kept visible, never silently dropped.
