# blender-knowledge

**Status:** Waves through 8 (STUDY-062 still-current pin-4.x 2026-09-07). Catalog **219 · 130/219 · 8 waves**. Pin 4.x. Silent 4→5: 0.

- **Wave 8 (STUDY-062 still-current pin-4.x)** — [dispatch](waves/wave-08-study-062-still-current/dispatch.md) · [research-raw](waves/wave-08-study-062-still-current/research-raw.json) — 22 recipes verified=0; Pin 4.x; silent 4→5: 0; APOLLO unverified; Analogist #7–#8 omitted.

- **Wave 7 (STUDY-047 GLB-first)** — [dispatch](waves/wave-07-study-047-glb-first/dispatch.md) · [research-raw](waves/wave-07-study-047-glb-first/research-raw.json) — 22 recipes verified=0; Pin 4.x; silent 4→5: 0; meshopt unverified.

- **Wave 6 (STUDY-046 pin-4.x vs 5.0)** — [dispatch](waves/wave-06-study-046-pin4x-vs-5/dispatch.md) · [research-raw](waves/wave-06-study-046-pin4x-vs-5/research-raw.json) — 23 recipes verified=0; silent 4→5: 0; pin-4.x holds.
Readouts KB: current, web-grounded **Blender 4.x** practice for the studio's **headless sprite-turnaround
render pipeline** (import a TRELLIS-generated GLB → render 8-direction sprites via `blender --background
--python` → composite into a 2.5D game) plus general game-asset prep. Part of the `readouts` monorepo
(study-swarm-built, ai-loadout-routed SQLite KBs). KB #8.

- **Primary entity:** a RECIPE — an actionable, current Blender-4.x practice / API / pattern.
- **Decisive axis:** `currency` — the Blender-4.x verdict (`solid` / `plausible` / `shaky` / `blender3_stale`
  / `wrong`). Blender moves fast — EEVEE Next replaced legacy EEVEE in **4.2**, AgX became the default view
  transform in **4.0**, Auto Smooth became the Smooth-by-Angle modifier in **4.1**, bone layers became Bone
  Collections in **4.0**, the Extensions platform arrived in **4.2** — so most online tutorials are 2.8/2.9/3.x
  and stale. Each recipe targets current 4.x and flags 3.x-isms. A code/practice KB, so license / VRAM /
  rig-fit (the sprites & model axes) do **not** apply.
- **10 lanes, 5 waves.** Counts are generated, never typed — see the status line above and [`catalog/README.md`](catalog/README.md).
  - *wave 1 — pipeline-core:* headless-bpy · render-engines · color-management · import-export · lighting-camera
  - *wave 2 — asset-creation:* mesh-ops · materials-baking · geometry-nodes · rigging-animation · addons-pipeline

## Layout
- `blender.db` — SQLite (waves → recipes → sources; categories; FTS). Defined by `schema.sql`.
- `catalog/` — per-lane markdown, generated from the DB (never hand-edited). Start at `catalog/README.md`.
- `waves/wave-NN-*/` — per-wave provenance: `lanes/*.json` (per-lane research) + `research-raw.json` (the assembled load source).
- `scripts/` — `load_db.py` (idempotent wave ingester) · `gen_catalog.py` · `gen_loadout.py` ·
  `_assemble_lanes.py` (lanes/*.json → research-raw.json) · `refresh_meta.py` · `regen.py` (one-command rebuild).
- `.claude/loadout/index.json` — the KB's progressive-disclosure router.

## Verification maturity (honest)
The 10 lanes were researched by parallel **web-grounded agents** that FETCHED current Blender docs
(docs.blender.org manual + the bpy API + 4.x release notes) — the **live-docs retrieval oracle**, which for a
fast-moving tool is the authoritative *currency* signal (an LLM's parametric Blender knowledge is itself
cutoff-limited). Every recipe carries ≥1 fetched `source` with a specific claim; currency was assessed by the
researcher against those fetched docs. This matches the godot-knowledge wave-1 standard.

**Cross-family hardening (done, 2026-06-20):** the wave-1 and wave-2 recipes (86 of the KB's 152) were re-adjudicated by `deepseek-v3.1:671b-cloud`
(a different model family from the Sonnet researchers), reasoning-stripped + refute-by-default, via
`scripts/verify_cloud.py`. Result: **77 confirmed · 6 confirmed-with-fixes · 3 unverified · 0 refuted** → 75
solid / 11 plausible / 0 flagged. The 9 fixed/unconfirmable recipes were down-weighted solid→plausible with
cross-family notes appended; none were refuted. Per-wave receipts in `waves/*/verification.md`; the juror's
verdicts + provenance live in each wave's `research-raw.json` under `cloud_verify`. The `verified` flag now
means "currency confirmed against current Blender docs **and** survived cross-family adjudication."

## Rebuild
```
$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'
python scripts/regen.py        # loads every wave, rebuilds catalog + loadout + the monorepo root routers
```

## Query
```
sqlite3 blender.db "SELECT * FROM v_recommended"   -- current, verified Blender-4.x practice
sqlite3 blender.db "SELECT * FROM v_flagged"       -- needs care (stale / shaky / wrong)
sqlite3 blender.db "SELECT * FROM v_by_lane"       -- per-lane currency rollup
sqlite3 blender.db "SELECT name FROM recipes_fts WHERE recipes_fts MATCH 'agx'"
```

Built 2026-06-20 to ground the studio's Blender turnaround pipeline (the headless TRELLIS-GLB → 8-direction
sprite render path). The **color-management** lane directly captures the AgX-washes-stylized-art fix earned in
production (use the `Standard` view transform for saturated stylized sprite art; AgX desaturates it).
