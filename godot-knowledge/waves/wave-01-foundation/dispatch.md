# Wave 1 — Godot-4 dev knowledge (dispatch)

6 web-grounded research lanes (architecture · grid-movement · turn-combat · rendering-2.5d · ui-tactical ·
tooling-test-export), each adversarially verified against current Godot 4.x for CURRENCY. **55 recipes · 52
verified · 2 flagged.** Built to ground the vertical-slice spine (the part-targeting verb + one
deterministic fight) in current Godot 4 — never Godot 3.

## The headline call per lane

- **Architecture** — model ALL game data (units / abilities / parts / loot / status) as custom **Resource (.tres)**
 scripts (`class_name X extends Resource`, typed `@export` arrays). Plain-text, diffable, LLM-authorable without
 opening the editor — the single highest-leverage pattern for this studio. One `Events` autoload (signals-only)
 for decoupled comms; keep autoloads few + self-contained (the official "manage only your own data" rule); a
 node-based FSM for the turn loop; `change_scene_to_packed/file` for swaps; the ResourceLoader security rule
 (untrusted `.tres` can execute code → CACHE_MODE_IGNORE / a safe loader). The STALE-API recipe is a ready Godot-3→4 lint gate.
- **Grid & movement** — **TileMapLayer** (one node per layer; `TileMap` deprecated 4.3); `local_to_map`/`map_to_local`
 for cell conversion; **flood-fill (BFS)** for movement RANGE keyed on `Vector2i`; **AStarGrid2D** (use `region`,
 not the deprecated `size`) for the actual path. Open-source MIT floor: GDQuest tactical-rpg-movement + godot-open-rpg
 give grid/cursor/pathfinding — but they STOP at movement; the combat loop + UI is the real build.
- **Turn-combat** — a turn **state machine**, a **deterministic** damage/effect model (no hidden hit-chance —
 required by the theme), abilities/status as data Resources, called-shot targeting reading the target's
 `parts: Array[PartData]`.
- **Rendering 2.5D** — **Y-sort** for depth; 2D lighting via CanvasModulate / Light2D / 2D normal maps / glow for the
 grimy mood; AnimatedSprite2D vs AnimationPlayer per need; the **forward_plus** renderer for 2D HDR/glow on PC.
- **Tactical UI** — Control nodes + the Theme system; the legibility-critical HUD (shown disable/loot outcomes,
 part panels, a collateral indicator, range/AP) built data-drivenly; custom tooltips for the deterministic breakdowns.
- **Tooling/test/export** — **GUT** to unit-test the deterministic combat (deterministic logic is trivially testable),
 **headless + GitHub-Actions CI** (setup-godot, `--headless --import` warm-up), export templates for Windows/Steam,
 the Godot `.gitignore` (`.godot/`). Target current stable 4.x (4.7 shipped 2026-06-18).

## The through-line
The build leans on the **Resource-as-data spine**: units, abilities, lootable parts, and the part-targeting
verb are all `.tres` the LLM crew authors as text — new enemies/parts ship as a PR, no editor session. Deterministic
combat (the theme's core) is both a design win AND a testing win (GUT-unit-testable). Start the vertical slice on the
open-source grid floor (GDQuest / godot-open-rpg, MIT) and build the turn loop + loot UI on top — that's the part
nothing ships for free.
