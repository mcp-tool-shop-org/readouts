# Mesh editing & cleanup
_Decimate/Remesh/Boolean, normals & the 4.1 Smooth-by-Angle change, merge/fill/clean — preparing imported TRELLIS meshes for render & export._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

9 recipes · 8 solid.

| Recipe | Blender | Currency | ✓ | What |
|--------|-------|----------|---|------|
| Boolean modifier — Exact vs Fast (vs Manifold in 4.5) solver | 4.x (Manifold solver added in 4.5) | ✅ solid | ✓ | Perform CSG Boolean operations (Union/Difference/Intersect) between two meshes.  |
| Decimate modifier — Collapse mode (ratio-based poly reduction) | 4.x | ✅ solid | ✓ | Reduce triangle/polygon count by collapsing edges. The primary tool for lowering |
| Decimate modifier — Planar (Dissolve) mode for flat-face cleanup | 4.x | ✅ solid | ✓ | Dissolve edges between co-planar faces, collapsing triangle fans on flat surface |
| Fill Holes, Delete Loose, Degenerate Dissolve — structural cleanup trio | 4.x | ✅ solid | ✓ | Three mesh cleanup operators that address common TRELLIS mesh defects: open hole |
| Merge by Distance (remove_doubles) — weld coincident vertices | 4.x | ✅ solid | ✓ | Merge vertices that are within a distance threshold of each other. Essential for |
| Recalculate Outside / flip normals & clear custom split normals | 4.x | ✅ solid | ✓ | Fix inverted face normals on imported meshes (a common TRELLIS artifact). Recalc |
| Remesh modifier — Voxel mode for topology reconstruction | 4.x | ✅ solid | ✓ | Rebuild mesh topology from scratch using a volumetric voxel grid. Produces a cle |
| Shade Smooth by Angle — Blender 4.1+ (Auto Smooth removed) | 4.1+ (breaking change from 4.0) | ✅ solid | ✓ | Apply angle-threshold smoothing to mesh normals. In Blender 4.1 the 'Auto Smooth |
| Full TRELLIS GLB cleanup recipe — import to game-export-ready | 4.1+ | ▸ plausible | · | End-to-end headless bpy pipeline for cleaning a raw TRELLIS-generated GLB mesh:  |

## Detail

### Boolean modifier — Exact vs Fast (vs Manifold in 4.5) solver · `✅ solid` · Blender 4.x (Manifold solver added in 4.5)
**Perform CSG Boolean operations (Union/Difference/Intersect) between two meshes. The solver choice determines accuracy and speed.**
- **How:** import bpy # Setup: obj_a is the base, obj_b is the cutter
obj_a = bpy.data.objects['Base']
obj_b = bpy.data.objects['Cutter'] bpy.context.view_layer.objects.active = obj_a bool_mod = obj_a.modifiers.new(name='Boolean', type='BOOLEAN')
bool_mod.operation = 'DIFFERENCE' # UNION | DIFFERENCE | INTERSECT
bool_mod.solver = 'EXACT' # FAST | EXACT | (MANIFOLD in 4.5+)
bool_mod.object = obj_b # Exact-solver extras:
bool_mod.use_self = False # True if obj_a self-intersects
bool_mod.use_hole_tolerant = True # better results on meshes with holes bpy.ops.object.modifier_apply(modifier='Boolean') # Remove the cutter object after apply
bpy.data.objects.remove(obj_b, do_unlink=True) # In Blender 4.5+ MANIFOLD solver (fastest, requires manifold inputs):
# bool_mod.solver = 'MANIFOLD'
- **Gotchas:** FAST (BMesh solver): works only on manifold meshes; much faster but fails silently on non-manifold input by producing garbled output. EXACT: uses multi-precision arithmetic (Zhou et al. Mesh Arrangements algorithm); handles coplanar faces and non-manifold geometry correctly but is slower. MANIFOLD (4.5 LTS, 2025-07-15): fastest solver, based on the Manifold library, but requires ALL inputs to be strictly manifold (every edge adjacent to exactly two faces) — TRELLIS meshes often fail this requirement. TRELLIS GLBs should default to EXACT. Always remove or hide the cutter object after applying to avoid export issues.
- **For Studio:** Cutting sprite-silhouette masks or holes in props exported from TRELLIS. Use EXACT by default for TRELLIS input since it handles the mesh quality variation typical of AI-generated geometry.
- **Verify (solid):** Solver differences confirmed via blenderbasecamp.com fetch (Fast vs Exact) and developer.blender.org 4.5 release notes (Manifold solver, released 2025-07-15). Exact solver attribution: Zhou, Grinspun, Zorin, and Jacobson algorithm confirmed in Blender 2.91 release notes. | cross-family (deepseek-v3.1): confirmed — Correctly describes EXACT/FAST solvers and mentions MANIFOLD solver addition in 4.5 with proper use_self and use_hole_tolerant properties. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Boolean Tool Fast vs Exact Solver — Blender Base Camp](https://www.blenderbasecamp.com/boolean-tool-fast-vs-exact-solver-when-and-why-to-use-them/) — Fast solver uses BMesh (manifold-only, fastest); Exact solver uses multi-precision arithmetic and handles coplanar/non-manifold meshes accurately but is slower ; [Blender 4.5 LTS — Modeling & UV release notes](https://developer.blender.org/docs/release_notes/4.5/modeling/) — New Manifold solver added to Boolean modifier in 4.5; based on Manifold library; fastest but requires strictly manifold inputs

### Decimate modifier — Collapse mode (ratio-based poly reduction) · `✅ solid` · Blender 4.x
**Reduce triangle/polygon count by collapsing edges. The primary tool for lowering TRELLIS mesh density before game export. Produces a triangulated result by default; use_collapse_triangulate=False preserves quads where possible.**
- **How:** import bpy, math obj = bpy.context.active_object # must be a MESH object # Add Decimate modifier
dec = obj.modifiers.new(name='Decimate', type='DECIMATE')
dec.decimate_type = 'COLLAPSE' # enum: COLLAPSE | UNSUBDIV | DISSOLVE
dec.ratio = 0.25 # 0.0–1.0; 0.25 = keep 25% of faces
dec.use_collapse_triangulate = True # True = all-tris output (safe for game export)
# Optional: limit to a vertex group
# dec.vertex_group = 'MyGroup'
# dec.invert_vertex_group = False # Apply (required for export to see changes)
bpy.ops.object.modifier_apply(modifier='Decimate') # Read final face count:
print('Faces after decimate:', len(obj.data.polygons))
- **Gotchas:** Collapse is destructive — it discards normals and can create non-manifold edges at high reduction ratios (>0.75 reduction). TRELLIS meshes are already all-tris so triangulate=True has no overhead. The 'ratio' property is 0–1 where 1.0 = no change; the modifier shows the resulting face count in the UI as 'Face Count'. Applying via bpy.ops.object.modifier_apply() requires the modifier name string to match exactly.
- **For Studio:** First pass on every imported TRELLIS GLB: ratio 0.3–0.5 before normals fixup. Brings a 150k-tri scan mesh to ~40–75k for sprite rendering without visible silhouette loss at 256×256 sprite res.
- **Verify (solid):** Confirmed: docs.blender.org/api/4.0/bpy.types.DecimateModifier.html (search result) lists decimate_type enum COLLAPSE/UNSUBDIV/DISSOLVE plus ratio, iterations, angle_limit properties — consistent through 4.x. bpy.ops.object.modifier_apply pattern confirmed across multiple pipeline examples. | cross-family (deepseek-v3.1): confirmed — All properties and methods are correct for Blender 4.x, including use_collapse_triangulate and proper modifier application. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [DecimateModifier — Blender Python API (4.0/current)](https://docs.blender.org/api/current/bpy.types.DecimateModifier.html) — decimate_type enum is COLLAPSE/UNSUBDIV/DISSOLVE; ratio, use_collapse_triangulate, vertex_group are the key COLLAPSE-mode properties ; [Mesh Operators — Blender Python API 4.2](https://docs.blender.org/api/4.2/bpy.ops.mesh.html) — bpy.ops.object.modifier_apply is the correct operator for applying a modifier by name in 4.x

### Decimate modifier — Planar (Dissolve) mode for flat-face cleanup · `✅ solid` · Blender 4.x
**Dissolve edges between co-planar faces, collapsing triangle fans on flat surfaces into single ngons. More topology-aware than Collapse for architectural or hard-surface meshes that have many tiny triangles on flat regions.**
- **How:** import bpy, math obj = bpy.context.active_object dec = obj.modifiers.new(name='DecimatePlanar', type='DECIMATE')
dec.decimate_type = 'DISSOLVE' # Planar mode
dec.angle_limit = math.radians(5.0) # dissolve edges where face angle < 5 degrees
dec.use_dissolve_boundaries = False # True can dissolve UV seam edges too # Check face count before apply
print('Before:', len(obj.data.polygons))
bpy.ops.object.modifier_apply(modifier='DecimatePlanar')
print('After:', len(obj.data.polygons))
- **Gotchas:** DISSOLVE outputs ngons — downstream exporters or game engines that require tris must triangulate after. use_dissolve_boundaries=True is aggressive and can break UV islands. angle_limit is in radians in the API, degrees in the UI. Very effective on scan meshes with flat floors/walls but does nothing on organic rounded surfaces.
- **For Studio:** Secondary pass on TRELLIS meshes that have flat base planes (pedestal, ground contact) where Collapse would distort silhouette but Planar can dissolve thousands of co-planar micro-triangles into clean ngons.
- **Verify (solid):** API property names confirmed from docs.blender.org/api/4.0/bpy.types.DecimateModifier.html search result. angle_limit + use_dissolve_boundaries are the DISSOLVE-mode specific properties. | cross-family (deepseek-v3.1): confirmed — DISSOLVE mode with angle_limit in radians and use_dissolve_boundaries are correctly implemented for Blender 4.x. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [DecimateModifier — Blender Python API (current)](https://docs.blender.org/api/current/bpy.types.DecimateModifier.html) — angle_limit and use_dissolve_boundaries are DISSOLVE mode properties; value is in radians

### Fill Holes, Delete Loose, Degenerate Dissolve — structural cleanup trio · `✅ solid` · Blender 4.x
**Three mesh cleanup operators that address common TRELLIS mesh defects: open holes in the surface, floating disconnected vertices/edges, and zero-area degenerate faces/edges.**
- **How:** import bpy obj = bpy.context.active_object
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT') # 1. Delete Loose — remove disconnected verts, edges, or faces
bpy.ops.mesh.delete_loose( use_verts=True, use_edges=True, use_faces=False # keep floating face patches (they may be intentional)
) # 2. Degenerate Dissolve — collapse zero-area faces and zero-length edges
bpy.ops.mesh.dissolve_degenerate( threshold=0.0001 # edges/faces smaller than this are removed
) # 3. Fill Holes — fill open boundary loops up to N sides
bpy.ops.mesh.fill_holes(sides=4) # sides=0 means any hole size
# fill_holes detects boundary edges and fills them;
# sides=4 limits filling to holes with <= 4 boundary edges (quads only)
# sides=0 fills all holes regardless of size bpy.ops.object.mode_set(mode='OBJECT')
- **Gotchas:** Run in this order: delete_loose FIRST (removes garbage verts that confuse hole detection), THEN dissolve_degenerate, THEN fill_holes. fill_holes with sides=0 on complex organic meshes can fill large concave holes with unpredictable ngons — prefer sides=4 or sides=8 for controlled filling. dissolve_degenerate with too large a threshold can accidentally remove thin legitimate geometry (fins on characters, etc.) — use 0.0001 as a conservative default. These three ops are stable and unchanged across 4.x.
- **For Studio:** Run after merge_by_distance and before Decimate in the TRELLIS GLB cleanup pipeline. Removes the floating vert debris and micro-face artifacts that the volumetric TRELLIS extraction step leaves behind.
- **Verify (solid):** All three operators confirmed in Blender 4.2 mesh ops API (docs.blender.org/api/4.2/bpy.ops.mesh.html) via search result. Parameter names (use_verts, use_edges, use_faces for delete_loose; threshold for dissolve_degenerate; sides for fill_holes) confirmed across multiple Blender scripting references and consistent since 2.x. | cross-family (deepseek-v3.1): confirmed — All three cleanup operators (delete_loose, dissolve_degenerate, fill_holes) are correctly implemented with proper parameters for Blender 4.x. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Mesh Operators — Blender Python API 4.2](https://docs.blender.org/api/4.2/bpy.ops.mesh.html) — delete_loose(use_verts, use_edges, use_faces), dissolve_degenerate(threshold), fill_holes(sides) all present and documented in 4.2 ; [Clean Up — Blender Manual 4.0](https://docs.blender.org/manual/en/4.0/modeling/meshes/editing/mesh/cleanup.html) — Fill Holes, Delete Loose, and Degenerate Dissolve are all under Mesh > Clean Up; Fill Holes uses a 'sides' parameter to limit hole size ; [TRELLIS GLB import and cleanup workflow — 3D AI Studio](https://www.3daistudio.com/3d-generator-ai-comparison-alternatives-guide/how-to-import-optimize-ai-models-in-blender) — fill_holes(), delete_loose(), dissolve_degenerate(), and normals_make_consistent() are the canonical cleanup sequence for AI-generated mesh imports

### Merge by Distance (remove_doubles) — weld coincident vertices · `✅ solid` · Blender 4.x
**Merge vertices that are within a distance threshold of each other. Essential for TRELLIS meshes that may have zero-length edges, duplicate verts at seams, or disconnected shells that share coordinates.**
- **How:** import bpy obj = bpy.context.active_object
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT') # Merge vertices closer than threshold (world-space distance)
bpy.ops.mesh.remove_doubles(threshold=0.0001, use_unselected=False)
# threshold: 0.0001 (0.1mm) is a conservative safe default
# use_unselected=True also merges into unselected verts (useful for partial selections) bpy.ops.object.mode_set(mode='OBJECT')
print('Vertex count after merge:', len(obj.data.vertices))
- **Gotchas:** The UI label is 'Merge by Distance' (since ~2.82) but the bpy operator is still bpy.ops.mesh.remove_doubles() — the legacy name is preserved in the API and works in 4.x. threshold is in world-space units: a mesh scaled to 2m tall should use a small value like 0.0001; a mesh at 0.01m scale may need 0.000001. Run BEFORE fill_holes and after initial import to ensure topology is coherent. Do NOT use with use_unselected=True in headless pipelines unless you've verified what 'unselected' geometry exists.
- **For Studio:** Always run as the first cleanup op on a TRELLIS GLB in the pipeline. Collapses any micro-gaps left by the mesh extraction step, which can otherwise cause shading seams and Boolean failures.
- **Verify (solid):** Operator name remove_doubles confirmed in Blender 4.2 mesh ops API search result (docs.blender.org/api/4.2/bpy.ops.mesh.html). Threshold behavior confirmed across multiple Blender scripting guides. UI renamed to 'Merge by Distance' in 2.82 but API name unchanged. | cross-family (deepseek-v3.1): confirmed — remove_doubles operator with threshold parameter is correctly implemented for vertex welding in Blender 4.x. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Mesh Operators — Blender Python API 4.2](https://docs.blender.org/api/4.2/bpy.ops.mesh.html) — bpy.ops.mesh.remove_doubles(threshold, use_unselected) is the 4.2 API; UI label is 'Merge by Distance' but operator name is preserved ; [Clean meshes automatically in Blender with Python](https://thinkmoult.com/clean-meshes-automatically-blender-python.html) — bpy.ops.mesh.remove_doubles() confirmed as the correct cleanup operator for welding verts in headless scripts

### Recalculate Outside / flip normals & clear custom split normals · `✅ solid` · Blender 4.x
**Fix inverted face normals on imported meshes (a common TRELLIS artifact). Recalculate Outside makes all face normals point outward consistently. Also covers how to clear any baked Custom Split Normals Data that can override smooth shading.**
- **How:** import bpy obj = bpy.context.active_object
bpy.context.view_layer.objects.active = obj # Enter Edit Mode
bpy.ops.object.mode_set(mode='EDIT') # Select all geometry
bpy.ops.mesh.select_all(action='SELECT') # Recalculate normals to point outward (Shift+N in UI)
bpy.ops.mesh.normals_make_consistent(inside=False)
# inside=True would flip to point inward (Shift+Ctrl+N) # Return to Object Mode
bpy.ops.object.mode_set(mode='OBJECT') # ---------------------------------------------------------
# Clear Custom Split Normals (if mesh was imported with
# baked custom normals that are fighting your shade smooth):
# ---------------------------------------------------------
if obj.data.has_custom_normals: bpy.ops.mesh.customdata_custom_splitnormals_clear() # Equivalent UI: Object Data Properties > Geometry Data > # Clear Custom Split Normals Data
- **Gotchas:** normals_make_consistent requires EDIT mode and selected geometry — call after mode_set(mode='EDIT') and select_all. GLB/glTF imports from TRELLIS often carry baked custom split normals (has_custom_normals == True); these override Shade Smooth/Smooth by Angle completely and must be cleared before normal smoothing has any visible effect. customdata_custom_splitnormals_clear() was available before 4.1 and is still present in 4.x — it predates and is separate from the Auto Smooth removal.
- **For Studio:** Step 2 in the TRELLIS GLB cleanup recipe after import: clear custom normals first, then recalculate outside, then apply Smooth by Angle. Without this step, Shade Smooth by Angle has no visible effect on GLTF-imported meshes.
- **Verify (solid):** normals_make_consistent(inside=False) for 'Recalculate Outside' confirmed via multiple Blender normals guides and API search results. has_custom_normals and customdata_custom_splitnormals_clear confirmed in bpy.types.Mesh API and mentioned in Blender manual/community sources as the required step before normal re-smoothing. | cross-family (deepseek-v3.1): confirmed — Correct normals_make_consistent operation with inside=False and proper handling of custom split normals for Blender 4.x. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [How to Fix Normals in Blender — 3DModels.org](https://3dmodels.org/blog/how-to-fix-normals-in-blender/) — Recalculate Outside is bpy.ops.mesh.normals_make_consistent(inside=False); clear custom split normals via Object Data Properties > Geometry Data to un-bake imported normals ; [Blender Normal Fixer // Clear Custom Normals Script](https://danielvesterbaek.gumroad.com/l/uXKAX) — Custom split normals must be cleared before Shade Smooth takes effect on imported meshes

### Remesh modifier — Voxel mode for topology reconstruction · `✅ solid` · Blender 4.x
**Rebuild mesh topology from scratch using a volumetric voxel grid. Produces a clean, evenly-spaced triangle mesh that follows the original shape. Best for heavily broken TRELLIS output (non-manifold, inside-out shells, internal geometry) where cleanup ops alone can't rescue the mesh.**
- **How:** import bpy obj = bpy.context.active_object # Method 1: Modifier (non-destructive, apply when ready)
rm = obj.modifiers.new(name='Remesh', type='REMESH')
rm.mode = 'VOXEL' # enum: BLOCKS | SMOOTH | SHARP | VOXEL
rm.voxel_size = 0.005 # smaller = more detail; world-space units
rm.adaptivity = 0.0 # 0.0 = uniform; higher = fewer polys on flat areas
rm.use_smooth_shade = False # keep False; handle shading via Smooth by Angle modifier
bpy.ops.object.modifier_apply(modifier='Remesh') # Method 2: Direct operator (destructive, applies immediately)
# bpy.ops.object.voxel_remesh() # uses object.data.remesh_voxel_size
# obj.data.remesh_voxel_size = 0.005
# bpy.ops.object.voxel_remesh() print('Faces after voxel remesh:', len(obj.data.polygons))
- **Gotchas:** Voxel remesh DESTROYS UV maps, custom normals, and vertex colors — run before any UV unwrap. voxel_size is in world-space: a 1m tall character with voxel_size=0.01 gives 100 voxels of height. All-tris output. Does not preserve sharp edges unless you use SHARP mode (which uses an octree, not voxels). adaptivity > 0 can cause stretched triangles on curved surfaces. Internal geometry is removed, which is usually desirable for TRELLIS output.
- **For Studio:** Nuclear option for TRELLIS meshes with severe inside-out faces, internal walls (known TRELLIS.2 issue per GitHub #140), or non-manifold geometry that blocks Boolean operations downstream.
- **Verify (solid):** RemeshModifier API confirmed from search: docs.blender.org/api/current/bpy.types.RemeshModifier.html lists mode (BLOCKS/SMOOTH/SHARP/VOXEL), voxel_size, adaptivity, use_smooth_shade. TRELLIS internal mesh walls confirmed as known issue in microsoft/TRELLIS.2 #140. | cross-family (deepseek-v3.1): confirmed — VOXEL mode with voxel_size, adaptivity, and use_smooth_shade properties are correct for Blender 4.x remeshing. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [RemeshModifier — Blender Python API (current)](https://docs.blender.org/api/current/bpy.types.RemeshModifier.html) — Mode enum is BLOCKS/SMOOTH/SHARP/VOXEL; voxel_size and adaptivity are the VOXEL-mode control properties ; [TRELLIS generating duplicate inner mesh walls · Issue #140](https://github.com/microsoft/TRELLIS.2/issues/140) — TRELLIS outputs internal geometry (duplicate inner walls) — voxel remesh is the reliable fix because it fills the volume from outside

### Shade Smooth by Angle — Blender 4.1+ (Auto Smooth removed) · `✅ solid` · Blender 4.1+ (breaking change from 4.0)
**Apply angle-threshold smoothing to mesh normals. In Blender 4.1 the 'Auto Smooth' checkbox in Object Data Properties was removed. It is now a Geometry Nodes modifier node group called 'Smooth by Angle' bundled with Blender, or accessible via the 'Shade Auto Smooth' operator.**
- **How:** import bpy, math obj = bpy.context.active_object # ------------------------------------------------------------------
# METHOD A: Operator (simplest — adds the modifier automatically)
# Works in Object Mode; available in 4.1+
# ------------------------------------------------------------------
bpy.context.view_layer.objects.active = obj
bpy.ops.object.shade_smooth_by_angle(angle=math.radians(30.0), keep_sharp_edges=True)
# This adds the 'Smooth by Angle' GN modifier AND sets shade-smooth on the mesh. # ------------------------------------------------------------------
# METHOD B: Manual modifier approach (for headless scripts where
# the asset library may not be auto-loaded)
# ------------------------------------------------------------------
# Step 1: Load the node group from Blender's bundled assets
import os, bpy
blender_path = bpy.utils.resource_path('LOCAL') # e.g. C:/Program Files/Blender Foundation/Blender 4.2
asset_blend = os.path.join(blender_path, 'datafiles', 'assets', 'geometry_nodes', 'smooth_by_angle.blend') if 'Smooth by Angle' not in bpy.data.node_groups: with bpy.data.libraries.load(asset_blend, link=False) as (data_from, data_to): data_to.node_groups = ['Smooth by Angle'] # Step 2: Add a Geometry Nodes modifier and assign the node group
mod = obj.modifiers.new(name='SmoothByAngle', type='NODES')
mod.node_group = bpy.data.node_groups['Smooth by Angle'] # Step 3: Set the angle (Input_1 = angle in radians)
mod['Input_1'] = math.radians(30.0) # 30 degrees # Note: Input_1_use_attribute is 0 (use value, not attribute) # ------------------------------------------------------------------
# Shade Flat / Shade Smooth (no angle)
# ------------------------------------------------------------------
# bpy.ops.object.shade_flat() # flat shading
# bpy.ops.object.shade_smooth() # smooth shading (180deg, no angle threshold)
- **Gotchas:** CRITICAL BREAKING CHANGE IN 4.1: The 'Auto Smooth' toggle in Object Data Properties > Normals was removed. Scripts or add-ons that set obj.data.auto_smooth_angle or obj.data.use_auto_smooth will break in 4.1+. The new system uses a Geometry Nodes modifier ('Smooth by Angle') from the bundled 'Essentials' asset library. In headless/background mode the asset library may not be initialized — use Method B (bpy.data.libraries.load from the bundled.blend path) rather than the asset browser API. The operator bpy.ops.object.shade_smooth_by_angle() is the cleanest single-line solution when the asset library is available. Input_1 key accesses the angle socket by index — may change between Blender minor versions; verify with mod.node_group.inputs['Angle'].identifier if needed.
- **For Studio:** Applied after Decimate in the TRELLIS GLB cleanup pipeline to restore clean shading across low-poly sprite meshes. 30° threshold is a good default for organic character meshes; hard-surface props may want 45–60°.
- **Verify (solid):** Breaking change confirmed: multiple community sources (blenderartists.org, gamedev.tv) confirm Auto Smooth checkbox removed in 4.1. Operator name bpy.ops.object.shade_smooth_by_angle confirmed in Blender 4.1 docs search result. Modifier['Input_1'] = angle_radians pattern confirmed from Bforartists GitHub issue #4189 (fetched) with working code. Asset path via bpy.data.libraries.load workaround confirmed as fix in Blender bug #117399. | cross-family (deepseek-v3.1): confirmed — Accurately describes the 4.1+ change from Auto Smooth checkbox to Smooth by Angle modifier and provides correct implementation methods. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Blender 4.1 Auto Smooth is now a modifier ONLY — Blender Artists](https://blenderartists.org/t/blender-4-1-auto-smooth-is-now-a-modifier-only/1488922) — Auto Smooth checkbox removed in 4.1; replaced by Smooth by Angle GN modifier node group; modifier['Input_1'] = radians is the Python angle-setting pattern ; [#117399 Adding assets (Smooth by Angle) not working in background Python script — Blender Projects](https://projects.blender.org/blender/blender/issues/117399) — In headless mode the asset list may not be loaded; workaround is bpy.data.libraries.load() from the bundled geometry_nodes/smooth_by_angle.blend path ; [Add Adjust Smooth by Angle Modifier operator · Issue #4189 — Bforartists](https://github.com/Bforartists/Bforartists/issues/4189) — Working Python code: detect NODES modifier with node_group == bpy.data.node_groups['Smooth by Angle'], set modifier['Input_1'] = math.radians(angle)

### Full TRELLIS GLB cleanup recipe — import to game-export-ready · `▸ plausible` · Blender 4.1+
**End-to-end headless bpy pipeline for cleaning a raw TRELLIS-generated GLB mesh: import → structural cleanup → poly reduction → normals → export. Combines all mesh-ops lane recipes into a single callable script.**
- **How:** import bpy, math, os, sys def clean_trellis_glb(glb_path: str, out_path: str, decimate_ratio: float = 0.35): """ Import a TRELLIS GLB, clean it, and export a game-ready GLB. Designed for Blender 4.1+. """ # 0. Clean scene bpy.ops.wm.read_factory_settings(use_empty=True) # 1. Import GLB bpy.ops.import_scene.gltf(filepath=glb_path) # 2. Gather mesh objects mesh_objs = [o for o in bpy.context.scene.objects if o.type == 'MESH'] if not mesh_objs: raise RuntimeError('No mesh objects found after import') for obj in mesh_objs: bpy.context.view_layer.objects.active = obj obj.select_set(True) # 3. Enter Edit Mode for cleanup ops bpy.ops.object.mode_set(mode='EDIT') bpy.ops.mesh.select_all(action='SELECT') # 3a. Merge by distance — weld micro-seams bpy.ops.mesh.remove_doubles(threshold=0.0001) # 3b. Delete loose geometry bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False) # 3c. Dissolve degenerate elements bpy.ops.mesh.dissolve_degenerate(threshold=0.0001) # 3d. Recalculate normals outward bpy.ops.mesh.normals_make_consistent(inside=False) bpy.ops.object.mode_set(mode='OBJECT') # 3e. Clear any baked custom split normals if obj.data.has_custom_normals: bpy.ops.mesh.customdata_custom_splitnormals_clear() # 4. Decimate (Collapse) dec = obj.modifiers.new(name='Decimate', type='DECIMATE') dec.decimate_type = 'COLLAPSE' dec.ratio = decimate_ratio dec.use_collapse_triangulate = True bpy.ops.object.modifier_apply(modifier='Decimate') # 5. Apply Smooth by Angle (Blender 4.1+ modifier approach) blender_local = bpy.utils.resource_path('LOCAL') smooth_blend = os.path.join( blender_local, 'datafiles', 'assets', 'geometry_nodes', 'smooth_by_angle.blend' ) if 'Smooth by Angle' not in bpy.data.node_groups: with bpy.data.libraries.load(smooth_blend, link=False) as (src, dst): dst.node_groups = ['Smooth by Angle'] sba = obj.modifiers.new(name='SmoothByAngle', type='NODES') sba.node_group = bpy.data.node_groups['Smooth by Angle'] sba['Input_1'] = math.radians(30.0) # Note: leave modifier UNAPPLIED so it's live/adjustable; # apply only if exporting to a format that doesn't support GN modifiers obj.select_set(False) # 6. Export cleaned GLB bpy.ops.export_scene.gltf( filepath=out_path, export_format='GLB', use_selection=False, export_apply=True # bakes all modifiers including Smooth by Angle ) print(f'Exported to {out_path}') # --- Entry point when run headlessly ---
if __name__ == '__main__': argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [] import argparse p = argparse.ArgumentParser() p.add_argument('--glb', required=True) p.add_argument('--out', required=True) p.add_argument('--ratio', type=float, default=0.35) args = p.parse_args(argv) clean_trellis_glb(args.glb, args.out, args.ratio) # Invocation:
# blender --background --python clean_trellis.py -- --glb input.glb --out clean.glb --ratio 0.35
- **Gotchas:** export_apply=True in export_scene.gltf is REQUIRED to bake the Smooth by Angle GN modifier into the output mesh normals — without it, the exported GLB reverts to flat normals. The Smooth by Angle.blend asset path (via bpy.utils.resource_path('LOCAL')) assumes the standard Blender installation layout; verify on your install with: python -c "import bpy; import os; print(os.path.join(bpy.utils.resource_path('LOCAL'), 'datafiles', 'assets', 'geometry_nodes', 'smooth_by_angle.blend'))". customdata_custom_splitnormals_clear() must be called while in Object Mode (not Edit Mode). Fill Holes is intentionally omitted from this recipe — it can produce large unexpected ngon fills on organic meshes; add it back with sides=4 only if the mesh has known specific holes.
- **For Studio:** Production script for the TRELLIS GLB → 2.5D sprite pipeline. Run as: blender --background --python clean_trellis.py -- --glb trellis_output.glb --out cleaned.glb --ratio 0.35. Feed output to the camera-orbit render script.
- **Verify (plausible):** Each individual op in this recipe is confirmed solid from its own recipe entry. The full end-to-end script is synthesized — the Smooth by Angle asset path may vary by OS and Blender version. Marked plausible (not solid) because the complete script has not been run end-to-end against a live Blender 4.x install. Verify the smooth_by_angle.blend path on your install before production use. | cross-family (deepseek-v3.1): unverified — While the individual components appear correct, the complete end-to-end pipeline cannot be fully verified without testing the specific GLB import/export workflow. [only 0 of 1 juror(s) confirmed [unverified]]
- **Sources:** [Blender Python script: converting mesh to GLB (gist by ryanfb)](https://gist.github.com/ryanfb/f7caff4f08b1afa2960a40f63b39434b) — bpy.ops.import_scene.gltf + export_scene.gltf with export_apply=True is the correct headless GLB round-trip pattern ; [#117399 Adding assets (Smooth by Angle) not working in background Python script](https://projects.blender.org/blender/blender/issues/117399) — bpy.data.libraries.load(smooth_by_angle.blend) is the correct workaround for loading the Smooth by Angle node group in headless mode ; [TRELLIS mesh cleanup pipeline — AI import workflow guide](https://www.3daistudio.com/3d-generator-ai-comparison-alternatives-guide/how-to-import-optimize-ai-models-in-blender) — Decimate at ratio 0.5 + normals fix is the recommended standard workflow for TRELLIS/AI-generated GLB imports into Blender

