# Geometry Nodes (procedural)
_The GN modifier/editor, scattering/instancing, named attributes, the Repeat/Simulation zones (4.x), procedural props & asset variation for the game world._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

24 recipes · 24 solid.

| Recipe | Blender | Currency | ✓ | What |
|--------|-------|----------|---|------|
| BlenderAlchemy — VLM editing of Blender node graphs | 4.5 LTS | ✅ solid | · | VLM-guided editing including material-node connection sequences. |
| BlenderGym — foundational model graphics editing bench | 4.5 LTS | ✅ solid | · | Code-based 3D reconstruction/editing benchmark in Blender. |
| GN Modifier + Node Group Inputs/Outputs | 4.0+ | ✅ solid | ✓ | Add a Geometry Nodes modifier to any object, wire up Group Input → Group Output  |
| Geometry Nodes Introduction (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | GN modifies geometry via modifier + node group; Group Input prior stack. |
| Geometry Nodes Modifier (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | Modifier binds GN group; bake Packed/Disk; mesh/curve/text/volume. |
| Grease Pencil Fill Tool (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | Draw Mode Fill auto-fills closed stroke areas. |
| Grease Pencil Introduction (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | GP is 3D-space stroke object; Draw/Edit/Sculpt + materials/modifiers. |
| Grease Pencil Material Stroke+Fill (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | Independent Stroke and Fill; Fill Solid/Gradient/Texture. |
| Grease Pencil to Curves Node (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | GN converts each GP layer into curve instances. |
| Greebles / Procedural Surface Detailing | 4.0+ (4.2 for Align Rotation to Vector; 4.3 for Hash Value node) | ✅ solid | ✓ | Add sci-fi or industrial micro-detail to a flat or low-poly surface by scatterin |
| Import/Export SVG as Grease Pencil (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | SVG import/export path for Grease Pencil strokes. |
| Infinigen Indoors — Blender procedural indoor assets | 4.5 LTS | ✅ solid | · | Blender-based procedural generator of indoor assets + constraint arrangement. |
| Infinigen-Articulated — simulation-ready procedural assets | 4.5 LTS | ✅ solid | · | Procedural generators + Blender utilities for articulated assets with physics ex |
| LL3M — LLMs write Blender Python for editable 3D | 4.5 LTS | ✅ solid | · | Multi-agent LLMs write interpretable bpy to generate editable assets. |
| Line Art Modifier (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | Contours from Scene/Collection/Object into GP; needs active camera; Bake Line Ar |
| Named Attributes — Store / Capture / Retrieve | 4.0+; Capture Attribute multi-capture added 4.2 | ✅ solid | ✓ | Three complementary nodes for reading and writing per-element data (position, co |
| Procedural Asset Variation via Menu Switch + Seed | 4.1+ (Menu Switch added 4.1; 'extend' socket added 4.2; Hash Value 4.3+) | ✅ solid | ✓ | A single GN node group that produces multiple visually distinct outputs — differ |
| Process expertise → Blender material node graphs | 4.5 LTS | ✅ solid | · | Compiles expert process traces into executable Blender material node graphs. |
| PyTorchGeoNodes — differentiable GN shape programs | 4.5 LTS | ✅ solid | · | Parses Blender Geometry Nodes into differentiable PyTorch graphs for reconstruct |
| Realize Instances + Apply Modifier for Game Engine Export | 4.0+ (Realize Instances existed earlier but glTF limitation and Store Named Attribute UV pattern are 4.x-confirmed practice) | ✅ solid | ✓ | GN instances are virtual — they share geometry data and are invisible to FBX/glT |
| Repeat Zone (4.0) — Single-Frame Iteration | 4.0+ (new in 4.0) | ✅ solid | ✓ | A pair of boundary nodes (Repeat Input + Repeat Output) enclosing a sub-graph th |
| Scatter/Instancing — Distribute Points on Faces → Instance on Points | 4.0+ | ✅ solid | ✓ | The canonical GN scatter pattern: place a cloud of points on a mesh surface, the |
| Simulation Zone (3.6/4.x) — Frame-Persistent State | 3.6 (introduced); 4.0+ (stable); 4.1 Bake Node; 4.2 bake overlay | ✅ solid | ✓ | A pair of boundary nodes (Simulation Input + Simulation Output) whose body execu |
| Wei & Bousseau — Grease Pencil sketch→3D add-on | 4.5 LTS | ✅ solid | · | Bridges GP 2D vector strokes to symmetry-driven 3D lift. |

## Detail

### BlenderAlchemy — VLM editing of Blender node graphs · `✅ solid` · Blender 4.5 LTS
**VLM-guided editing including material-node connection sequences.**
- **How:** Node-graph editing as graphics automation surface.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [BlenderAlchemy — VLM editing of Blender node graphs](https://arxiv.org/abs/2404.17672) — VLM node-graph editing

### BlenderGym — foundational model graphics editing bench · `✅ solid` · Blender 4.5 LTS
**Code-based 3D reconstruction/editing benchmark in Blender.**
- **How:** Evaluates systems against real Blender craft complexity.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [BlenderGym — foundational model graphics editing bench](https://arxiv.org/abs/2504.01786) — Blender graphics editing bench

### GN Modifier + Node Group Inputs/Outputs · `✅ solid` · Blender 4.0+
**Add a Geometry Nodes modifier to any object, wire up Group Input → Group Output as the data pipe, and expose socket values to the modifier panel so artists can art-direct procedural params without opening the node editor.**
- **How:** 1. Select object → Properties → Modifier tab (blue wrench) → Add Modifier → Geometry Nodes (or press New in GN editor header). 2. The default tree is Group Input → Group Output — this is the identity passthrough. 3. To expose a parameter: add any node (e.g. Set Position with an Offset input), drag the Offset socket to Group Input, then that socket appears in the modifier panel as a named field. 4. In Blender 4.0+ you can mark the whole node group as an asset and enable 'Is Modifier' — the group then appears directly in the Add Modifier menu by catalog path, and the node-group-selector is hidden by default for a cleaner interface. 5. Use the Menu Switch node (added 4.1) to create a dropdown enum in the modifier panel — connect different geometry branches to one Menu Switch whose items become a UI dropdown. 6. Node inputs can be flagged 'Single Value' (4.0+) to suppress the attribute toggle, keeping the modifier panel uncluttered.
- **Gotchas:** Pre-4.0 node group assets could not be marked 'Is Modifier' — that's 4.0-only. Menu Switch node is 4.1+. In 3.x the N-panel > Group tab was the only way to add inputs; 4.x still supports it but exposing sockets by dragging is faster. Single-value flag only available 4.0+.
- **For Studio:** Core pattern for every procedural prop in the 2.5D pipeline: expose Seed, Density, Detail Level as modifier inputs so art-direction happens in the properties panel without touching nodes. Reusable node group assets let the same 'rock scatter' or 'pipe cluster' GN group appear in the Add Modifier menu and get dropped onto any prop.
- **Verify (solid):** Confirmed via Blender 4.0 release notes (developer.blender.org/docs/release_notes/4.0/geometry_nodes/) and community sources (cgcookie, artisticrender). Is Modifier + asset catalog integration is 4.0-specific and confirmed. | cross-family (deepseek-v3.1): confirmed — Correct description of GN modifier workflow with parameter exposure and 4.0+ asset modifier features. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Everything New in Blender 4.0 — CG Cookie](https://cgcookie.com/posts/everything-new-in-blender-4-0) — Node groups marked as assets with 'Is Modifier' appear in the modifier menu; node group selector hidden by default; inputs can be forced single-value. ; [Blender Geometry Nodes Fundamentals Guide — Artisticrender](https://artisticrender.com/blender-geometry-nodes-fundamentals-guide/) — Group Input/Output structure, exposing parameters to modifier panel via socket drag or N-panel Group tab, field vs non-field socket shapes. ; [Menu Switch Node — Blender 4.1 Manual](https://docs.blender.org/manual/en/4.1/modeling/geometry_nodes/utilities/menu_switch.html) — Menu Switch outputs one of its inputs based on a dropdown; menu items defined in editor sidebar; 4.1 added 'extend' socket in 4.2.

### Geometry Nodes Introduction (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**GN modifies geometry via modifier + node group; Group Input prior stack.**
- **How:** Procedural craft on modifier stack.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Geometry Nodes Introduction (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/introduction.html) — GN introduction 4.5

### Geometry Nodes Modifier (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**Modifier binds GN group; bake Packed/Disk; mesh/curve/text/volume.**
- **How:** Procedural variation entry for sprite-adjacent props.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Geometry Nodes Modifier (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/modeling/modifiers/generate/geometry_nodes.html) — GN modifier 4.5

### Grease Pencil Fill Tool (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**Draw Mode Fill auto-fills closed stroke areas.**
- **How:** Filled silhouette regions for 2.5D sprites.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Grease Pencil Fill Tool (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/grease_pencil/modes/draw/tools/fill.html) — GP Fill tool 4.5

### Grease Pencil Introduction (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**GP is 3D-space stroke object; Draw/Edit/Sculpt + materials/modifiers.**
- **How:** 2.5D drawing surface for turnaround line craft.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Grease Pencil Introduction (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/grease_pencil/introduction.html) — GP introduction 4.5

### Grease Pencil Material Stroke+Fill (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**Independent Stroke and Fill; Fill Solid/Gradient/Texture.**
- **How:** Line+fill via material slots.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Grease Pencil Material Stroke+Fill (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/grease_pencil/materials/properties.html) — GP materials 4.5

### Grease Pencil to Curves Node (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**GN converts each GP layer into curve instances.**
- **How:** Bridge Line Art/GP into curve/mesh GN pipelines.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Grease Pencil to Curves Node (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/grease_pencil/operations/grease_pencil_to_curves.html) — GP→Curves GN

### Greebles / Procedural Surface Detailing · `✅ solid` · Blender 4.0+ (4.2 for Align Rotation to Vector; 4.3 for Hash Value node)
**Add sci-fi or industrial micro-detail to a flat or low-poly surface by scattering pre-made greeble meshes (panels, bolts, vents, pipes) procedurally. Combine Distribute Points on Faces, Instance on Points, and Repeat Zone to build layered geometry variation without duplicating topology manually.**
- **How:** Pattern A — Scatter greebles on a surface: Build a small library Collection of detail meshes (panel_A, bolt_ring, vent_slot). Use Collection Info (Separate Children = true, Reset Children = true) → Instance on Points. Drive Instance on Points 'Pick Instance' socket with a Hash Value node (4.3+) or a Random Value (Integer) node seeded per-point — each point gets a different greeble. Add Align Rotation to Vector node (4.2+, replaces deprecated Align Euler to Vector) to orient each instance to the surface normal (Surface Normal field from Distribute Points on Faces Normal output). Expose Density, Seed, Scale Min/Max to Group Input. Pattern B — Repeat Zone for layered paneling: start with a flat mesh → Repeat Zone (body: Extrude Mesh individual faces, then Scale Elements to shrink slightly per iteration, Iterations = 3) → produces stepped panel rings. Combine via Join Geometry (scatter result + base mesh). Pattern C — Noise-driven height variation: Named Attribute (position) → Noise Texture → Map Range → Set Position Offset to push surface geometry up/down for organic micro-bumps without a displacement modifier.
- **Gotchas:** Align Euler to Vector is deprecated as of 4.2 — use Align Rotation to Vector instead (faster, cleaner socket types). Hash Value node for stable per-element randomness is 4.3+; for 4.0–4.2 use Random Value (Integer) seeded with an Index node. High-density greeble scatter is expensive — realize and bake for hero props, keep instance count under ~5K for interactive viewport.
- **For Studio:** Core tool for the 2.5D RPG city tileset: industrial building facades, underground corridor walls, and tech-prop surfaces all get a GN greeble pass before texture bake. One GN group per surface type (metal_panel, concrete_worn, pipe_cluster) stored as modifier assets in the project library.
- **Verify (solid):** Align Rotation to Vector replacing Align Euler to Vector confirmed in 4.2 release notes summary. Hash Value node confirmed as 4.3 addition via 80.lv fetch. Scatter pattern confirmed solid from multiple sources. Noise-driven Set Position is a well-established 3.x/4.x pattern. | cross-family (deepseek-v3.1): confirmed — Valid greeble workflow using proper 4.x nodes including Align Rotation to Vector (4.2) and Hash Value (4.3). [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Sci-Fi Greebles with Blender Geometry Nodes — YouTube (Dec 2024)](https://www.youtube.com/watch?v=Gj4sJp4FLX0) — Procedural sci-fi greeble system using GN scatter + instancing pattern; released December 2024 confirming 4.x currency. ; [Geometry Nodes 4.2 LTS Release Notes — Blender Developer Docs](https://developer.blender.org/docs/release_notes/4.2/geometry_nodes/) — Align Rotation to Vector replaces deprecated Align Euler to Vector; Scale Elements 4-10x faster. ; [Check Out New Geometry Nodes Coming To Blender 4.3 — 80.lv](https://80.lv/articles/blender-4-3-s-for-each-element-node-zone-upgrade) — Hash Value node added in 4.3 for stable per-element randomness.

### Import/Export SVG as Grease Pencil (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**SVG import/export path for Grease Pencil strokes.**
- **How:** Vector authoring → raster sheet still farm contract.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Import/Export SVG as Grease Pencil (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/files/import_export/grease_pencil_svg.html) — GP SVG IO 4.5

### Infinigen Indoors — Blender procedural indoor assets · `✅ solid` · Blender 4.5 LTS
**Blender-based procedural generator of indoor assets + constraint arrangement.**
- **How:** Procedural asset library still Blender-native; 4.x craft not 5.x.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Infinigen Indoors — Blender procedural indoor assets](https://arxiv.org/abs/2406.11824) — Procedural indoor generators

### Infinigen-Articulated — simulation-ready procedural assets · `✅ solid` · Blender 4.5 LTS
**Procedural generators + Blender utilities for articulated assets with physics export.**
- **How:** Procedural mesh/joint craft for sim-ready props.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Infinigen-Articulated — simulation-ready procedural assets](https://arxiv.org/abs/2505.10755) — Articulated procedural assets

### LL3M — LLMs write Blender Python for editable 3D · `✅ solid` · Blender 4.5 LTS
**Multi-agent LLMs write interpretable bpy to generate editable assets.**
- **How:** Code-native procedural path aligned with bpy/GN.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [LL3M — LLMs write Blender Python for editable 3D](https://arxiv.org/abs/2508.08228) — LLM bpy procedural modelers

### Line Art Modifier (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**Contours from Scene/Collection/Object into GP; needs active camera; Bake Line Art.**
- **How:** Mesh→stroke for multi-angle sprite outlines; bake for headless.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Line Art Modifier (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/grease_pencil/modifiers/generate/line_art.html) — Line Art 4.5

### Named Attributes — Store / Capture / Retrieve · `✅ solid` · Blender 4.0+; Capture Attribute multi-capture added 4.2
**Three complementary nodes for reading and writing per-element data (position, color, float, vector, int) tagged by string name. Essential for passing data across node boundaries, freezing a value before geometry changes, and wiring GN-generated UV maps for export.**
- **How:** Three roles: (1) Named Attribute node — READ an existing attribute by name (string input). Domain is inferred. Use to read built-in attributes like 'position', 'normal', or custom ones you stored earlier. Output is a Field. (2) Store Named Attribute node — WRITE a field to a named attribute slot at the current domain (Point, Edge, Face, Face Corner). Example: to bake UVs for export, pipe a Texture Coordinate UV field into Store Named Attribute, set Domain = Face Corner, Data Type = 2D Vector, Name = 'UVMap'. The resulting attribute survives Realize Instances and is recognized by FBX/glTF exporters. (3) Capture Attribute node — FREEZE a field's value at a specific moment in the graph, producing an anonymous attribute you can re-use downstream after the geometry has moved. Classic use: capture Position before a Set Position moves verts, then compare old vs new position downstream. Pattern for Set Position: Group Input Geometry → Capture Attribute (Position field) → Set Position (Offset = some noise/vector math) → Named Attribute reads back the captured original position for blend math → Group Output.
- **Gotchas:** Store Named Attribute writes on evaluation every frame — if used inside a Simulation Zone, be aware of frame-order effects. Capture Attribute in 4.2+ can capture multiple attributes at once (4.1 and earlier: one per node). Store Named Attribute can write 8-bit integer attributes as of 4.2. Named Attribute reads are domain-sensitive — querying 'position' on the Face domain returns face-center positions, not vertex positions.
- **For Studio:** Required for game-engine export: always Store Named Attribute (Face Corner, 2D Vector, 'UVMap') on any procedurally generated mesh that needs textures. Also used to tag prop variants (e.g. store 'variant_id' as a per-instance integer for shader-side variation in Godot).
- **Verify (solid):** Confirmed from Blender 4.2 release notes summary (Capture Attribute multi-capture, 8-bit int store), artisticrender fundamentals guide, and surf-visualization course fetch. | cross-family (deepseek-v3.1): confirmed — Correct explanation of attribute workflow with proper 4.x features including multi-capture in 4.2. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Attributes Reference — Blender Manual (latest)](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attributes_reference.html) — Named vs anonymous attributes, domain types, built-in attribute names (position, normal, etc.). ; [Geometry Nodes 4.2 LTS Release Notes — Blender Developer Docs](https://developer.blender.org/docs/release_notes/4.2/geometry_nodes/) — Capture Attribute now supports multiple attributes at once; Store Named Attribute can write 8-bit integer attributes. ; [Blender Geometry Nodes to UE5 — James Roha on Medium](https://medium.com/@Jamesroha/blender-geometry-nodes-to-unreal-engine-5-the-procedural-environment-art-guide-05cf8d8b4701) — Store Named Attribute on Face Corner domain (2D Vector, name 'UVMap') is required for GN-generated UVs to survive export.

### Procedural Asset Variation via Menu Switch + Seed · `✅ solid` · Blender 4.1+ (Menu Switch added 4.1; 'extend' socket added 4.2; Hash Value 4.3+)
**A single GN node group that produces multiple visually distinct outputs — different prop configurations, damage states, or style variants — controlled by a dropdown enum in the modifier panel. Eliminates maintaining separate meshes for each variant; one GN group, N variants, art-direction via modifier UI.**
- **How:** 1. Build each variant as a sub-graph branch (e.g. 'intact_crate', 'dented_crate', 'broken_crate') each producing a Geometry output. 2. Connect all branches into a Menu Switch node (Shift+A → Utilities → Menu Switch). Add menu items named per variant in the sidebar. 3. Expose the Menu Switch 'Menu' socket to Group Input — this becomes a dropdown in the modifier panel. 4. Additionally expose a Seed integer input wired to any Random Value nodes inside each branch — a different seed produces geometric variation within the same variant. 5. For scale/rotation variation: Random Value (Vector, seeded by Seed + Index) → Combine XYZ → Set Position Offset or Instance on Points Scale. 6. Result: one modifier, dropdown selects crate state, Seed slider shuffles geometry within that state. Mark the node group as an asset ('Is Modifier') for library reuse. Optional: use Hash Value (4.3+) instead of Random Value for stable per-element randomness that doesn't shift when other nodes change.
- **Gotchas:** Menu Switch is only available from 4.1 — pre-4.1 you must use an Index Switch node or Math Compare chain instead. Menu Socket items are defined per node group and are not data-driven at runtime (you can't procedurally populate them from attributes). Hash Value for stable randomness is 4.3+; use seeded Random Value + Index for 4.1–4.2.
- **For Studio:** Prop library workflow for a 2.5D RPG: each prop category (crate, barrel, console, column) gets one GN group with 3–5 Menu Switch variants + Seed. Level designers drop the modifier on any mesh, pick the state, and randomize — no extra meshes in the scene file. Combined with Realize Instances + export, each resolved variant bakes to a clean static mesh.
- **Verify (solid):** Menu Switch node introduction at 4.1 confirmed from release notes summary and manual URL. 'extend' socket in 4.2 confirmed. Hash Value 4.3 confirmed. Dropdown in modifier panel from Menu Switch confirmed by search result extract. | cross-family (deepseek-v3.1): confirmed — Accurate Menu Switch workflow with proper 4.1+ features and variant control pattern. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Menu Switch Node — Blender 4.1 Manual](https://docs.blender.org/manual/en/4.1/modeling/geometry_nodes/utilities/menu_switch.html) — Menu Switch outputs one of N inputs by dropdown; items defined in sidebar; only the active branch is computed. ; [Geometry Nodes 4.2 LTS Release Notes — Blender Developer Docs](https://developer.blender.org/docs/release_notes/4.2/geometry_nodes/) — Menu Switch 'extend' socket added; sockets in Repeat and Simulation zones now aligned; Scale Elements rewritten 4-10x faster. ; [Everything New in Blender 4.0 — CG Cookie](https://cgcookie.com/posts/everything-new-in-blender-4-0) — GN node groups marked as modifier assets appear in Add Modifier menu; inputs forced to single values clean up the modifier panel.

### Process expertise → Blender material node graphs · `✅ solid` · Blender 4.5 LTS
**Compiles expert process traces into executable Blender material node graphs.**
- **How:** Procedural node-graph craft beyond static dump.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Process expertise → Blender material node graphs](https://arxiv.org/abs/2607.13318) — Material node-graph generation

### PyTorchGeoNodes — differentiable GN shape programs · `✅ solid` · Blender 4.5 LTS
**Parses Blender Geometry Nodes into differentiable PyTorch graphs for reconstruction/editing.**
- **How:** GN node graphs as first-class procedural mesh craft.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [PyTorchGeoNodes — differentiable GN shape programs](https://arxiv.org/abs/2404.10620) — Differentiable GeoNodes-adjacent shape programs

### Realize Instances + Apply Modifier for Game Engine Export · `✅ solid` · Blender 4.0+ (Realize Instances existed earlier but glTF limitation and Store Named Attribute UV pattern are 4.x-confirmed practice)
**GN instances are virtual — they share geometry data and are invisible to FBX/glTF exporters. Before exporting to Godot or any game engine you must collapse instances to real mesh data, then apply the modifier. Two methods: in-graph (Realize Instances node) or operator-based (Ctrl+A → Apply).**
- **How:** Method 1 — In-graph (preferred for pipelines): at the end of your GN tree, before Group Output, insert Realize Instances node. Its Geometry input comes from your last Instance on Points or Join Geometry; its output goes to Group Output. The modifier now evaluates to a real mesh. Then: in Object Mode, Ctrl+A → Apply → Geometry Nodes Modifier — mesh is baked to object data. Now export as FBX or glTF normally. Method 2 — Operator only (no node change): skip Realize Instances in-graph; instead use Object → Apply → Make Instances Real, then Object → Apply → Visual Geometry to Mesh (merges everything). Method 3 — UV prep: before Realize Instances, insert Store Named Attribute (Domain = Face Corner, Data Type = 2D Vector, Name = 'UVMap') to ensure procedurally-generated UVs survive. glTF exporter note: glTF has a known limitation — GN instances are not exported by the glTF exporter at all; Realize Instances in-graph is mandatory for glTF. FBX handles instances better but still benefits from Realize for clean import. Apply scale (Ctrl+A → Scale) before export since Blender uses meters and Godot/UE5 use different unit bases.
- **Gotchas:** Realizing instances on a dense scatter (100K+ instances) can produce a very large mesh — budget poly count before realizing for game assets. The glTF exporter limitation (no unrealized GN instances) is a hard stop. Apply modifier is irreversible — always work on a copy or from a linked asset. Applying scale before export is essential — missing this causes scale=100 issues in Godot when Blender units ≠ engine units.
- **For Studio:** Required final step for every GN-generated prop in the 2.5D RPG pipeline before handoff to Godot. Realize → Apply → Export FBX → Godot import. UVMap attribute store ensures baked textures align. Named attribute 'variant_id' can be carried through Realize Instances as a vertex color for shader-side variation.
- **Verify (solid):** glTF 'no unrealized instances' limitation confirmed via James Roha Medium article and Blender Artists community thread. Store Named Attribute for UV export confirmed via same Medium source and search results. Apply scale guidance is widely confirmed. | cross-family (deepseek-v3.1): confirmed — Correct export pipeline with proper UV attribute storage and realization methods for game engines. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Blender Geometry Nodes to UE5 — James Roha on Medium](https://medium.com/@Jamesroha/blender-geometry-nodes-to-unreal-engine-5-the-procedural-environment-art-guide-05cf8d8b4701) — Full export pipeline: Realize Instances → Apply modifier (Ctrl+A) → Store Named Attribute for UVs → FBX export; glTF cannot export unrealized GN instances. ; [How to Export Geometry Nodes Instances in a Game — Blender Artists](https://blenderartists.org/t/how-to-export-geometry-nodes-instances-in-a-game/1419992) — Community-confirmed: Make Instances Real + Visual Geometry to Mesh as operator-based alternative to in-graph Realize Instances. ; [Geometry Nodes 4.0 Release Notes — Blender Developer Docs](https://developer.blender.org/docs/release_notes/4.0/geometry_nodes/) — Node group tool assets introduced — apply-immediately pattern (add modifier + apply) for GN tool assets.

### Repeat Zone (4.0) — Single-Frame Iteration · `✅ solid` · Blender 4.0+ (new in 4.0)
**A pair of boundary nodes (Repeat Input + Repeat Output) enclosing a sub-graph that executes N times within a single frame. Unlike Simulation Zone (which steps once per timeline frame), Repeat Zone runs its body an arbitrary number of times at every evaluation. Use it for recursive subdivision, L-system growth, iterative displacement, or building up geometry in layers.**
- **How:** Add via Shift+A → Utilities → Repeat Zone — two nodes appear as a pair (Repeat Input on left, Repeat Output on right). 1. Connect incoming data (geometry, float, vector, etc.) into the Repeat Input's body sockets — these become iteration variables. 2. Inside the zone, modify the data however you want (Extrude Mesh, Scale Elements, Set Position, etc.). 3. Connect the zone's internal outputs to Repeat Output — they flow back to Repeat Input for the next iteration. 4. Set the Iterations integer on Repeat Input. 5. Repeat Output's sockets emit the final-iteration result downstream. Accumulator pattern: each socket on Repeat Input/Output carries a value forward — the geometry from iteration N is the input to iteration N+1. You can also feed external (non-iterated) values into interior nodes from outside the zone as constants. Example — growing a pipe rack: Repeat Input (Geometry) → Extrude Mesh → Scale Elements → Repeat Output (Geometry), Iterations = 6: produces 6 progressively extruded rings.
- **Gotchas:** High iteration counts are fully evaluated every frame — computationally expensive; bake with the Bake Node (4.1+) if static. Repeat Zone cannot carry simulation state across frames — that is Simulation Zone's role. In 4.3+, a For Each Element zone was added for per-element iteration without manually wiring counts; it coexists with Repeat Zone (Repeat = N times; For Each = once per element).
- **For Studio:** Procedural prop detailing: iterative extrusion for tech-corridor panels, recursive subdivision of a base shape for organic rocks, stacking elements to build a multi-floor ruin wall section. Art-direct iteration count as a modifier input for LOD-lite control.
- **Verify (solid):** Confirmed new in 4.0 from multiple release note summaries. Accumulator pattern and socket mechanics confirmed via mipmap.substack.com fetch and b3d.interplanety.org source. For Each zone as 4.3 addition confirmed via 80.lv article fetch. | cross-family (deepseek-v3.1): confirmed — Accurate description of Repeat Zone introduced in 4.0 with proper accumulator pattern explanation. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Using Loops & Logic In Geometry Nodes — Mipmap Substack](https://mipmap.substack.com/p/using-loops-and-logic-in-geometry) — Repeat Zone mechanics: accumulator pattern, reconnecting output to input for iteration, simultaneous output (not frame-by-frame), comparison to Simulation Zone. ; [Repeat Zone — Blender Manual 4.0](https://docs.blender.org/manual/en/4.0/modeling/geometry_nodes/utilities/repeat_zone.html) — Official node reference: Repeat Input/Output pair, Iterations input, body socket data flow. ; [Check Out New Geometry Nodes Coming To Blender 4.3 — 80.lv](https://80.lv/articles/blender-4-3-s-for-each-element-node-zone-upgrade) — For Each Element zone arrives in 4.3; Integer Math and Hash Value nodes added alongside it.

### Scatter/Instancing — Distribute Points on Faces → Instance on Points · `✅ solid` · Blender 4.0+
**The canonical GN scatter pattern: place a cloud of points on a mesh surface, then instance a collection or object at every point. Controls density, seed, minimum spacing (Poisson Disk), per-instance random rotation/scale. Foundation for environment set-dressing, ground-cover, debris, prop clusters.**
- **How:** Node chain: Group Input (Mesh) → Distribute Points on Faces → Instance on Points → [optional Realize Instances] → Group Output. Key socket wiring: (A) Distribute Points on Faces: Mesh ← Group Input Geometry; set Distribution Method to 'Random' (uniform) or 'Poisson Disk' (prevents overlap, adds Distance Min input); Density controls point count per unit area; Seed randomises placement. (B) Instance on Points: Points ← Distribute Points on Faces Points; Instance ← Object Info (Geometry output) of your prop object; add Random Value (Vector type) → Instance on Points Rotation for random Y-axis spin; add Random Value (Float, range 0.8–1.2) → Instance on Points Scale for size variety. (C) To scatter from a Collection: Collection Info node (Separate Children = true, Reset Children = true) → Instance on Points Instance socket — GN picks a random child per point. (D) Expose Density and Seed to Group Input so the modifier panel lets artists paint-sculpt coverage without touching the node tree. (E) If you need vertex-group masking: connect a Named Attribute node (name = your vertex group string, type Float) → Distribute Points on Faces Density Factor — points only land where weight > 0.
- **Gotchas:** Poisson Disk Distance Min is in Blender units — scale your scene correctly first. Collection Info 'Separate Children' + 'Reset Children' flags behave differently between 3.x and 4.x — always test. Instance on Points Scale expects a vector; connecting a Float directly works (uniform scale) but explicit Combine XYZ gives per-axis control. Instances are NOT real geometry until Realize Instances runs — the FBX/glTF exporter will not export unrealized instances.
- **For Studio:** Primary tool for environment set-dressing in the 2.5D RPG: scatter rocks, roots, moss patches, broken pipes, crates on any surface with art-directible density via vertex weights painted in weight-paint mode. One GN group serves every biome by swapping the Collection Info source.
- **Verify (solid):** Core workflow confirmed via multiple 4.x sources (artisticrender, poliigon, Blender manual excerpt). Node names and socket names verified via fetched content. | cross-family (deepseek-v3.1): confirmed — Accurate description of canonical scatter pattern with proper 4.x node usage and parameter controls. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [How to Scatter Objects With Geometry Nodes in Blender — Artisticrender](https://artisticrender.com/how-to-scatter-objects-with-geometry-nodes-in-blender/) — Full scatter chain including Distribute Points on Faces (Random/Poisson Disk), Instance on Points, Object Info, vertex-group density masking. ; [Easy Scattering — The Blend (Beehiiv)](https://blend.beehiiv.com/p/scattering) — Collection Info separate-children pattern for multi-prop scatter; expose density/seed to modifier panel. ; [Distribute Points on Faces — Blender Manual (latest)](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/point/distribute_points_on_faces.html) — Canonical node reference: Distribution Method (Random/Poisson Disk), Density, Seed, Distance Min, Density Factor inputs; Points output.

### Simulation Zone (3.6/4.x) — Frame-Persistent State · `✅ solid` · Blender 3.6 (introduced); 4.0+ (stable); 4.1 Bake Node; 4.2 bake overlay
**A pair of boundary nodes (Simulation Input + Simulation Output) whose body executes once per timeline frame, with the previous frame's output fed back as this frame's input. Enables true particle systems, growth animations, erosion, and any effect where state accumulates over time. Requires stepping through frames in order (no random access).**
- **How:** Add via Shift+A → Simulation → Simulation Zone. Structure: Simulation Input ← previous frame state sockets ← Simulation Output body. 1. Connect your initial geometry into Simulation Input. 2. Inside the zone: apply per-frame operations (move points by velocity field, increment an 'age' attribute via Math node + Named Attribute, delete old points with Delete Geometry). 3. Connect results to Simulation Output. 4. On frame 1 the Input reads the initial state; on frame 2+ it reads Simulation Output's result from the prior frame. 5. In Blender 4.1+, add a Bake Node immediately after Simulation Output to cache the simulation to disk — press Bake in the modifier panel to write frames, then the simulation plays back without re-evaluation. 6. In 4.2+, a bake overlay appears in the node editor showing which frames are cached. Combining with Repeat Zone: use Repeat Zone inside Simulation Zone for sub-frame physics steps (physics timestep << 1/24s).
- **Gotchas:** Simulation Zones require sequential frame evaluation — scrubbing backwards forces re-evaluation from frame 1 unless baked. Heavy simulations must be baked (Bake Node, 4.1+) before they are usable in production. Unlike Repeat Zone, Simulation Zone cannot be evaluated multiple times per frame without nesting inside Repeat Zone. The Simulation Zone stores state per-frame in memory; very long simulations with many attributes exhaust RAM.
- **For Studio:** Environmental storytelling props: dripping water that accumulates, smoke that lingers in a ventilation shaft, particles that settle on a surface frame-by-frame. Mostly useful for pre-baked FX elements that get exported as vertex-animated meshes or rendered to a flipbook sheet for the Godot 2.5D pipeline. Not suited for real-time in-engine — bake and export.
- **Verify (solid):** Introduction in 3.6 confirmed by multiple sources. Bake Node 4.1 and overlay 4.2 confirmed via 4.2 release notes summary. Sub-frame step pattern (Repeat inside Simulation) confirmed via digitalproduction.com article and search result summary. | cross-family (deepseek-v3.1): confirmed — Correct simulation zone workflow with proper 4.x bake features and frame-by-frame evaluation. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Simulation Zone — Blender Manual (4.5 LTS)](https://docs.blender.org/manual/en/4.5/modeling/geometry_nodes/simulation/simulation_zone.html) — Canonical node reference; frame-by-frame evaluation, state persistence, bake workflow. ; [Your Own Particle System With Simulation Nodes — Digital Production](https://digitalproduction.com/2023/08/10/your-own-particle-system-with-simulation-nodes/) — Particle emitter setup inside Simulation Zone, 'age' attribute increment per frame, combining Repeat Zone for sub-frame steps. ; [Everything New in Blender 4.0 — CG Cookie](https://cgcookie.com/posts/everything-new-in-blender-4-0) — Simulation Zone (3.6) vs Repeat Zone (4.0) distinction; Repeat runs any number of times per frame, Simulation steps once per timeline frame.

### Wei & Bousseau — Grease Pencil sketch→3D add-on · `✅ solid` · Blender 4.5 LTS
**Bridges GP 2D vector strokes to symmetry-driven 3D lift.**
- **How:** Pair with Line Art/SVG; not live headless GP.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Wei & Bousseau — Grease Pencil sketch→3D add-on](https://doi.org/10.2312/exw.20251065) — GP sketch→3D

