# Wave 6 — STUDY-045 2.5D lighting / Y-sort / TileMapLayer

**Tip:** `8f23082`
**Constraints:** Flips 37/42/49: 0. Godot APIs invented: 0 — no YSort node / bare Light2D / Godot-3 TileMap.

## Findings → recommendations
- Layered HSR / (x,y,layer) / tile matrices / sprite normals deepen 2.5D notes.
- TileMapLayer + y_sort_enabled + Point/Directional Height + CanvasTexture + CanvasModulate.
- Hold painter/Unity/CSS/URP; omit z-buffer-as-Y-sort + Godot-3 YSort fail-transfers.

## Evidence
`/workspace/studio/research/STUDY-045/` five packs + research-raw.json
