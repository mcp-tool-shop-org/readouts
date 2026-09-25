# Wave 1 — verification receipt

**Verifier:** a reasoning-stripped adversarial Godot-4 reviewer per lane, web-grounded against the CURRENT Godot 4.x
official docs + the named open-source repos. Decisive axis = **currency** (solid / plausible / shaky / godot3_stale /
wrong) — catches Godot-3-isms (deprecated nodes, renamed APIs), version-wrong API names, and unverified framework
claims. Default unverified on non-confirmation.

**Result: 55 recipes · 52 verified (solid/plausible) · 2 flagged (shaky) · 0 godot3_stale · 0 wrong.**
Per lane: architecture 10/10 solid · grid-movement 7 solid (9 verified) · turn-combat 8 solid (9) · rendering-2.5d
6 solid (8) · ui-tactical 8 solid (8) · tooling 8 solid (8).

The verifier was rigorous — it confirmed load-bearing API claims against the docs (`move_and_slide` no-args,
`change_scene_to_file/packed`, `instantiate`, `create_tween`, Resource `changed` not auto-emitted, AStarGrid2D
`region` vs deprecated `size`, TileMapLayer `set_cell` with no layer arg) and even caught that a cited bug
(godot#45350, local-to-scene on duplication) is now FIXED on the 4.6 milestone, and that the engine is at 4.7.

## The 2 flagged (shaky) — corrections, not rejections (both how-tos work; a note is wrong)
1. **ui-tactical — `_make_custom_tooltip()` override:** the how-to is correct, but the recipe's *version note* is
   INVERTED — `_make_custom_tooltip(for_text) -> Object` still returns Object (the returned node must be
   Control-derived), not "returns Control, formerly Object." Use the recipe; ignore the note.
2. **tooling — GUT headless CI:** the headline command uses `-gexit_on_complete`, which does NOT exist in GUT 9.5/9.6
   docs (it propagated from a blog, not the GUT docs). Use **`-gexit`** (returns exit 1 on any failure — the exact CI
   behavior wanted). Everything else (setup-godot, `--headless --import` warm-up, actions/cache@v4) is solid.

## Verifier maturity
Same-model-family verifier + a live-docs retrieval oracle (the official Godot 4.x page is the decorrelating element).
Cross-family cloud verification (`verify_cloud.py` via a non-Claude cloud model) is the planned hardening pass per the
readouts convention — wave 1 is research-grade, currency-checked, with the 2 flagged items carrying explicit corrections.
