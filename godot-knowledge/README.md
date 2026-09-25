# godot-knowledge

**Status:** Waves through 7 (STUDY-065 catalog vs README 2026-09-07). Catalog **177 · 88/177 · 7 waves**. Flips 37/42/49: 0. APIs invented: 0.

- **Wave 7 (STUDY-065 catalog vs README)** — [dispatch](waves/wave-07-study-065-catalog-readme/dispatch.md) · [research-raw](waves/wave-07-study-065-catalog-readme/research-raw.json) — 22 recipes verified=0; Analogist #7–#8 pack-only; Flips 37/42/49: 0; APIs invented: 0.

- **Wave 6 (STUDY-045 2.5D lighting)** — [dispatch](waves/wave-06-study-045-25d-lighting/dispatch.md) · [research-raw](waves/wave-06-study-045-25d-lighting/research-raw.json) — 22 recipes verified=0; flips 37/42/49: 0; APIs invented: 0.

- **Wave 5 (STUDY-044 leftover deepen)** — [dispatch](waves/wave-05-study-044-leftover-deepen/dispatch.md) · [research-raw](waves/wave-05-study-044-leftover-deepen/research-raw.json) — 23 recipes verified=0; flips 37/42/49: 0.
Readouts KB: current, adversarially-verified **Godot 4** dev knowledge for building **the target game** (a 2.5D
turn-based tactical RPG). Part of the `readouts` monorepo (study-swarm-built, ai-loadout-routed SQLite KBs).

- **Primary entity:** a RECIPE — an actionable, current Godot-4 practice / API / pattern.
- **Decisive axis:** `currency` — the adversarial Godot-4 verdict (`solid` / `plausible` / `shaky` /
 `godot3_stale` / `wrong`). The verifier web-checks each recipe against current Godot 4.x and flags Godot-3
 staleness (deprecated nodes, renamed APIs). A code/practice KB, so license / VRAM / rig-fit (the sprites &
 model axes) do **not** apply.
- **6 lanes:** architecture · grid-movement · turn-combat · rendering-2.5d · ui-tactical · tooling-test-export.

## Layout
- `godot.db` — SQLite (waves → recipes → sources; categories; FTS). Defined by `schema.sql`.
- `catalog/` — per-lane markdown, generated from the DB (never hand-edited). Start at `catalog/README.md`.
- `waves/wave-NN-*/` — per-wave provenance: `dispatch.md`, `research-raw.json` (the load source), `verification.md`.
- `scripts/` — `load_db.py` (idempotent wave ingester), `gen_catalog.py` (DB→catalog), `gen_loadout.py` (DB→loadout index).
- `.claude/loadout/index.json` — the KB's progressive-disclosure router.

## Rebuild a wave
```
$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'
python scripts/load_db.py waves/wave-01-foundation/research-raw.json
python scripts/gen_catalog.py
python scripts/gen_loadout.py
python../shared/gen_root_loadout.py # refresh the monorepo root router
```

## Query
```
sqlite3 godot.db "SELECT * FROM v_recommended" -- current, verified Godot-4 practice
sqlite3 godot.db "SELECT * FROM v_flagged" -- needs care (stale / shaky / wrong)
sqlite3 godot.db "SELECT * FROM v_by_lane" -- per-lane currency rollup
sqlite3 godot.db "SELECT name FROM recipes_fts WHERE recipes_fts MATCH 'astar'"
```

Wave 1 (2026-06-18) — a 6-lane study swarm, each lane adversarially verified for Godot-4 currency, built to
ground the vertical-slice spine (the part-targeting verb + one deterministic fight) in current Godot 4.x.
