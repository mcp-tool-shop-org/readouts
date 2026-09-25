# Import/export interchange
_glTF/GLB (the TRELLIS mesh input), FBX, OBJ (rewritten C++ importer), USD; vertex colors/materials, axis/scale conventions, the bpy import operators._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

31 recipes · 7 solid.

| Recipe | Blender | Currency | ✓ | What |
|--------|-------|----------|---|------|
| Check imported mesh bounds and normalize to unit cube | 4.0–4.5 | ✅ solid | ✓ | After importing a TRELLIS GLB, the mesh may arrive at arbitrary scale (TRELLIS o |
| Draco mesh compression — import/export support in 4.x | 4.0–4.5 (export: solid; import: unreliable in 4.0–4.2, improved in 4.3+) | ✅ solid | ✓ | KHR_draco_mesh_compression is a glTF extension that compresses mesh geometry. Bl |
| Export a GLB from Blender 4.x (bpy headless) | 4.0–4.5 | ✅ solid | ✓ | Export the current scene or selected objects as a binary GLB file, controlling f |
| FBX import/export — scale/unit pitfalls and 4.5 C++ importer | 4.0–4.4 (Python importer); 4.5+ (C++ ufbx importer, same operator name) | ✅ solid | ✓ | FBX has a chronic scale mismatch problem between Blender (meters, 1 BU = 1m) and |
| OBJ import — new C++ importer (bpy.ops.wm.obj_import, 3.3+) | 3.3–4.5 (C++ importer); bpy.ops.import_scene.obj removed in 4.0 | ✅ solid | ✓ | The Python OBJ importer/exporter addon was removed in Blender 4.0. The replaceme |
| glTF axis conventions and PBR material mapping on import | 4.0–4.5 | ✅ solid | ✓ | Understand how Blender converts glTF's Y-up coordinate system to Blender's Z-up, |
| glTF vertex colors / color attributes — 4.x behavior and export options | 4.0–4.5 (breaking change at 4.1, partial fix at 4.2) | ✅ solid | ✓ | Blender 4.1 changed when COLOR_0 vertex attributes get exported, breaking workfl |
| Import a textured GLB in a headless bpy script | 4.0–4.5 | ▸ plausible | ✓ | Load a TRELLIS-output GLB (textured mesh, PBR materials) into a blank Blender sc |
| USD import/export in Blender 4.x — scope and limits | 4.0–4.5 | ▸ plausible | ✓ | Blender 4.x includes built-in OpenUSD support (bpy.ops.wm.usd_import / bpy.ops.w |
| Absences on these pages | 4.x pin (GLB-first) | ⚠ shaky | · | **Absent:** TRELLIS product name; unit-cube normalize recipe; farm camera framin |
| Articulate3D: Holistic Understanding of 3D Scenes as Universal Scene Description | 4.x pin (GLB-first) | ⚠ shaky | · | First large-scale non-synthetic indoor dataset **natively in USD**; argues USD b |
| BlendFusion | 4.x pin (GLB-first) | ⚠ shaky | · | BlenderProc places cameras on a discrete orbit with azimuth every **45° (eight v |
| DeepJEB++: Foundation Model-Driven Large-Scale 3D Engineering Dataset via 2D Latent Space Augmentation | 4.x pin (GLB-first) | ⚠ shaky | · | Selects TRELLIS (MIT) for multi-view conditioning and SLAT decode into NeRF / 3D |
| EXT_meshopt_compression / meshopt | 4.x pin (GLB-first) | ⚠ shaky | · | UNVERIFIED meshopt — Analog: GPU-friendly mesh compression for glTF shipping siz |
| FBX (Experimental) | 4.x pin (GLB-first) | ⚠ shaky | · | Analog: proprietary FBX path marked Experimental with chronic unit/scale pitfall |
| From USD Scenes to Knowledge Graphs: Zero-Shot Ontology Grounding with LLMs | 4.x pin (GLB-first) | ⚠ shaky | · | USD encodes rich scene graphs but relies on user-defined identifiers; grounding  |
| Generating Actionable Robot Knowledge Bases by Combining 3D Scene Graphs with Robot Ontologies | 4.x pin (GLB-first) | ⚠ shaky | · | Converts diverse scene graphs into unified **USD** so only one importer/exporter |
| Headless farm path (on-page composition only) | 4.x pin (GLB-first) | ⚠ shaky | · | `-b`/`-P` (STUDY-046) + `bpy.ops.import_scene.gltf(filepath=…)` loads textured G |
| Khronos glTF 2.0 Specification | 4.x pin (GLB-first) | ⚠ shaky | · | Runtime delivery format; +Y up, +Z forward, meters; GLB = JSON+BIN in one file ( |
| MExECON: Multi-view Extended Explicit Clothed humans Optimized via Normal integration | 4.x pin (GLB-first) | ⚠ shaky | · | Blender renders an **8-view** set with cameras uniformly around the subject — sa |
| Modifiers introduction (non-destructive → apply) | 4.x pin (GLB-first) | ⚠ shaky | · | Analog: modifiers are non-destructive until applied; export must bake evaluated  |
| NANO3D: A Training-Free Approach for Efficient 3D Editing Without Masks | 4.x pin (GLB-first) | ⚠ shaky | · | Stores SLAT then uses FlexiCube to convert SLAT into **explicit GLB meshes** for |
| OpenUSD home | 4.x pin (GLB-first) | ⚠ shaky | · | USD as collaborative scene platform / DCC interchange (geometry, shading, lighti |
| Referencing Layers (USD composition) | 4.x pin (GLB-first) | ⚠ shaky | · | Analog: compose scenes by referencing layers/opinions. Holds as VFX composition  |
| Structured 3D Latents for Scalable and Versatile 3D Generation (TRELLIS) | 4.x pin (GLB-first) | ⚠ shaky | · | SLAT decodes to versatile formats (radiance fields, 3D Gaussians, meshes via Fle |
| Universal Scene Description | 4.x pin (GLB-first) | ⚠ shaky | · | Import meshes/materials/cameras/lights/volumes/points; Y-up → Z-up rotation on r |
| Universal Scene Description (Blender 4.5) | 4.x pin (GLB-first) | ⚠ shaky | · | Analog: Blender USD I/O exists but importer “does not yet handle certain USD com |
| bpy.ops.export_scene.gltf | 4.x pin (GLB-first) | ⚠ shaky | · | Headless export knobs: `export_format`, `export_yup`, `export_apply`, `export_dr |
| bpy.ops.import_scene.gltf | 4.x pin (GLB-first) | ⚠ shaky | · | Headless entry: `filepath`, `import_pack_images`, `merge_vertices`, `import_shad |
| glTF | 4.x pin (GLB-first) | ⚠ shaky | · | Analog: royalty-free runtime shipping format (JSON + binary `.glb`). Holds for T |
| glTF 2.0 | 4.x pin (GLB-first) | ⚠ shaky | · | Import/export `.glb`/`.gltf`; PBR Principled map; formats GLB binary / Separate  |

## Detail

### Check imported mesh bounds and normalize to unit cube · `✅ solid` · Blender 4.0–4.5
**After importing a TRELLIS GLB, the mesh may arrive at arbitrary scale (TRELLIS output is not normalized to any consistent real-world size). Read bounds via bpy, compute scale factor, center and fit to unit cube so the 8-direction render camera framing is stable.**
- **How:** ```python
import bpy, math
from mathutils import Vector def scene_bbox(): """Return world-space bounding box min/max of all mesh objects.""" bbox_min = [math.inf] * 3 bbox_max = [-math.inf] * 3 for obj in bpy.context.scene.objects: if obj.type != 'MESH': continue for corner in obj.bound_box: # 8 corners in local space world_pt = obj.matrix_world @ Vector(corner) for i in range(3): bbox_min[i] = min(bbox_min[i], world_pt[i]) bbox_max[i] = max(bbox_max[i], world_pt[i]) return Vector(bbox_min), Vector(bbox_max) def normalize_scene(): bbox_min, bbox_max = scene_bbox() extent = bbox_max - bbox_min scale = 1.0 / max(extent) # fit longest axis to 1 BU center = (bbox_min + bbox_max) / 2.0 for obj in bpy.context.scene.objects: if obj.parent is None and obj.type != 'LIGHT' and obj.type != 'CAMERA': obj.scale *= scale obj.location -= center * scale bpy.context.view_layer.update() # re-evaluate world matrices # Usage after import
normalize_scene()
print("Normalized bounds:", scene_bbox())
```
`obj.bound_box` returns 8 corners in local object space — multiply by `obj.matrix_world` to get world coordinates. `obj.dimensions` is simpler but ignores transforms if applied; `bound_box` + matrix_world is authoritative.
- **Gotchas:** Call bpy.context.view_layer.update() after changing scale/location or bound_box will reflect stale values.; TRELLIS GLBs may import as multiple mesh objects (one per material). The loop must iterate all MESH objects, not just bpy.context.active_object.; If the model has a root Empty parent (some TRELLIS exports wrap in a hierarchy), scaling the Empty scales all children — check for parent-less objects only.; Do not apply scale (bpy.ops.object.transform_apply) before this check — it corrupts animation data and is rarely needed for a pure render pipeline.
- **For Studio:** Run immediately after import_scene.gltf in the sprite-turnaround script to normalize the TRELLIS mesh so the camera rig's fixed radius always frames the subject.
- **Verify (solid):** Pattern extracted from both TRELLIS-3D and cube3d real render pipelines on HuggingFace. bound_box + matrix_world is documented Blender Python idiom across all 4.x versions. | cross-family (deepseek-v3.1): confirmed — Correct approach using bound_box and matrix_world for world-space bounding box calculation in 4.x. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [cube3d renderer blender_script.py — scene_bbox and normalize_scene](https://huggingface.co/spaces/Nymbo/cube3d-interactive/raw/0c10674d822643fd6c4c5536c33fe8dd8cbb3bc1/cube/cube3d/renderer/blender_script.py) — Production AI-model render pipeline uses this exact bound_box + matrix_world pattern for normalization ; [TRELLIS-3D HuggingFace render.py](https://huggingface.co/datasets/argojuni0506/TRELLIS-3D/blob/main/dataset_toolkits/blender_script/render.py) — Uses scene_bbox() -> normalize_scene() before multi-view render

### Draco mesh compression — import/export support in 4.x · `✅ solid` · Blender 4.0–4.5 (export: solid; import: unreliable in 4.0–4.2, improved in 4.3+)
**KHR_draco_mesh_compression is a glTF extension that compresses mesh geometry. Blender bundles Draco for export but import support has been inconsistent. Know when it works and when to pre-decompress.**
- **How:** **Draco EXPORT (4.x — works):**
```python
bpy.ops.export_scene.gltf( filepath="/out/compressed.glb", export_format="GLB", export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6, # 0-10, higher = smaller file export_draco_position_quantization=14, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12,
)
``` **Draco IMPORT (4.x — unreliable):**
- 4.0–4.2: Draco-compressed GLBs may fail silently or raise errors. Blender does NOT natively decompress on import in these versions.
- 4.3: Draco import was re-enabled but had a Windows DLL issue (missing `extern_draco.dll`, issue #130545). Fixed in a 4.3 patch.
- 4.5+: Draco import status improved but not fully stress-tested for all edge cases. **Pre-decompress workaround (safest for 4.0–4.2):**
```bash
# Using gltf-transform (Node.js) to strip Draco before Blender import:
npx @gltf-transform/cli decompress input.glb output_nodracos.glb
```
- **Gotchas:** TRELLIS GLBs are NOT Draco-compressed by default. This recipe is only relevant if receiving GLBs from web-optimization pipelines (three.js, Sketchfab, etc.).; Round-trip: if you export with Draco and then try to import back in the same Blender version, 4.0–4.2 will fail to import what it just exported.; Draco compression is lossy (quantization reduces precision). Not suitable for high-fidelity game asset pipelines.; DCC tools (Blender, Maya, 3dsMax) generally do not support Draco import. Draco is a delivery format for the web, not an interchange format.
- **For Studio:** Relevant only as a warning: if any upstream source delivers Draco-compressed GLBs, pre-decompress before Blender import. TRELLIS outputs are safe.
- **Verify (solid):** Draco export parameters confirmed by search results and community guides. Import unreliability in 4.0–4.2 confirmed by KhronosGroup issue #1333 and Blender issue #130545. The recommendation to use gltf-transform for pre-decompression is standard practice in the glTF community. | cross-family (deepseek-v3.1): confirmed — Accurately describes Draco compression support with export working reliably and import being problematic. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Import draco compressed gltf/glb — KhronosGroup/glTF-Blender-IO Issue #1333](https://github.com/KhronosGroup/glTF-Blender-IO/issues/1333) — Confirms Draco import has been a longstanding gap in Blender's glTF IO; import requires separate decompressor step ; [Blender Issue #130545 — Error importing glTF 4.3 (missing extern_draco.dll)](https://projects.blender.org/blender/blender/issues/130545) — Draco import re-enabled in Blender 4.3 but had a Windows DLL missing error in some builds ; [GLB models with Draco compression don't load in Blender 2.8 — KhronosGroup/glTF-Blender-IO Issue #252](https://github.com/KhronosGroup/glTF-Blender-IO/issues/252) — Original Draco import issue report; pattern has persisted across versions

### Export a GLB from Blender 4.x (bpy headless) · `✅ solid` · Blender 4.0–4.5
**Export the current scene or selected objects as a binary GLB file, controlling format, materials, textures, and compression.**
- **How:** ```python
import bpy # Minimal GLB export — all materials, embedded textures:
bpy.ops.export_scene.gltf( filepath="/out/model.glb", export_format="GLB", # 'GLB' = binary, 'GLTF_SEPARATE' =.gltf +.bin + textures use_selection=False, # export whole scene export_materials="EXPORT", # 'EXPORT' | 'PLACEHOLDER' | 'NONE' export_image_format="AUTO", # 'AUTO' | 'JPEG' | 'WEBP' | 'NONE' export_texcoords=True, export_normals=True, export_tangents=False, export_cameras=False, export_lights=False, # Draco compression (4.x bundled support on export): # export_draco_mesh_compression_enable=True, # export_draco_mesh_compression_level=6,
) # Export only selected objects:
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects["MyMesh"].select_set(True)
bpy.ops.export_scene.gltf( filepath="/out/selected.glb", export_format="GLB", use_selection=True,
)
```
Operator: `bpy.ops.export_scene.gltf` — stable name through 4.x.
Draco export: bundled `extern/draco` in Blender enables `export_draco_mesh_compression_enable`; however Draco-compressed GLBs cannot be re-imported by Blender 4.0–4.2, and import in 4.3 required a fix for a missing DLL (#130545). Keep Draco off for round-trip pipelines.
- **Gotchas:** export_format='GLTF_SEPARATE' is the only format that keeps textures as external files; GLB always embeds textures in the binary buffer.; Draco export works in 4.x but Draco IMPORT was broken in some 4.3 Windows builds (missing extern_draco.dll per issue #130545). For studio pipelines, avoid Draco unless the consumer is confirmed able to read it.; export_image_format='JPEG' compresses and converts all textures to JPEG — lossy. Use 'AUTO' to preserve PNG for RGBA, JPEG for RGB.; The operator runs in the current context; in headless mode, no context override is needed for bpy.ops.export_scene.gltf (unlike bpy.ops.wm.usd_export).; Collection exporters (added 4.2) allow per-collection export settings in the UI but are not yet exposed via a clean bpy.ops path for scripting — use the standard operator above.
- **For Studio:** Round-trip export if annotated meshes need to go back to the game engine after post-processing in Blender (e.g. adding LOD levels, baked normals). Not the primary path — the pipeline is GLB-in → render-out, not GLB-in → GLB-out.
- **Verify (solid):** Operator name and export_format parameter confirmed across multiple sources including KhronosGroup/glTF-Blender-IO issues and community posts. Draco import issue confirmed via issue #130545. | cross-family (deepseek-v3.1): confirmed — Correct export parameters for glTF/GLB export in Blender 4.x. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [KhronosGroup/glTF-Blender-IO GitHub — export operator issues](https://github.com/KhronosGroup/glTF-Blender-IO/issues/1441) — bpy.ops.export_scene.gltf is the current stable export operator with export_format, export_cameras, export_lights params ; [Blender Issue #130545 — Error importing glTF in Blender 4.3 (missing extern_draco.dll)](https://projects.blender.org/blender/blender/issues/130545) — Draco import was broken on Windows in some 4.3 builds due to missing DLL; confirms Draco export is bundled but import has had reliability issues

### FBX import/export — scale/unit pitfalls and 4.5 C++ importer · `✅ solid` · Blender 4.0–4.4 (Python importer); 4.5+ (C++ ufbx importer, same operator name)
**FBX has a chronic scale mismatch problem between Blender (meters, 1 BU = 1m) and game engines (UE5: centimeters, 1 UU = 1cm; Unity: meters but FBX scale metadata). In 4.5, a new C++ importer (ufbx) is faster and fixes many edge cases.**
- **How:** ```python
import bpy # FBX Import (4.5+ uses new C++ importer internally, same operator name):
bpy.ops.import_scene.fbx( filepath="/path/to/model.fbx", use_manual_orientation=False, # auto-detect FBX axis from file header global_scale=1.0, # 1.0 = use FBX file's built-in scale bake_space_transform=False, # True = apply axis conversion to mesh data use_custom_normals=True, use_subsurf=False, use_anim=False, # skip animation for static mesh import
) # FBX Export for Unreal Engine 5:
bpy.ops.export_scene.fbx( filepath="/path/to/out.fbx", apply_scale_options="FBX_SCALE_NONE", # let UE5 apply its own 100x conversion # Alternatives: # "FBX_SCALE_ALL" = bake 100x into mesh data (avoids runtime scale) # "FBX_SCALE_UNITS" = write scale in FBX metadata apply_unit_scale=True, # convert from meters to FBX units axis_forward='-Z', axis_up='Y', use_selection=False, object_types={'MESH'}, use_mesh_modifiers=True, bake_anim=False,
)
```
**Scale matrix for Blender→UE5 via FBX:**
- UE5 uses centimeters; Blender uses meters
- `FBX_SCALE_NONE` + `apply_unit_scale=True`: FBX metadata carries the 100x, UE5 reads it and rescales on import
- `FBX_SCALE_ALL` + `apply_unit_scale=True`: bakes the 100x into vertex data; FBX scale = 1.0 — safer for skeletal meshes where scale metadata can confuse the UE5 skeleton **4.5 C++ importer (ufbx):**
- Operator name unchanged: `bpy.ops.import_scene.fbx`
- 5–20x faster import; handles ASCII FBX, old binary FBX pre-7.1, geometric transforms (common in 3dsMax exports)
- Fixes ~20 open bug reports from the Python importer
- **Gotchas:** FBX_SCALE_NONE with animated skeletal meshes for UE4/UE5 can produce a 100x scale on the armature — use FBX_SCALE_ALL for rigged characters.; The chronic FBX import scale=100 problem (e.g. bpy.data.objects[n].scale = (100,100,100) after import) is caused by FBX files authored in centimeter units. Fix: apply_scale_options='FBX_SCALE_ALL' on re-export, or manually apply scale in Blender (Ctrl+A → Scale).; Blender 4.5 ships the C++ importer via the same bpy.ops.import_scene.fbx operator — no API change needed, but behavior differences exist: geometric transforms are now imported correctly (was a common 3dsMax FBX bug).; FBX is NOT the preferred format for the TRELLIS sprite-turnaround pipeline. GLB is preferred: embedded textures, correct PBR mapping, no scale ambiguity. FBX is only needed if the downstream engine specifically requires it (UE5 Skeletal Mesh, for example).
- **For Studio:** Relevant when re-exporting Blender-processed meshes to UE5 (the studio's 2.5D RPG targets Godot 4, but FBX may appear in other workflows). Not part of the TRELLIS→Blender→sprite-render pipeline.
- **Verify (solid):** apply_scale_options enum values confirmed in Blender API docs. UE5 unit mismatch documented in Medium 'Blender to UE5 complete export pipeline'. 4.5 C++ importer (ufbx) confirmed by Aras Pranckevičius blog post and Blender Projects PR #132406. | cross-family (deepseek-v3.1): confirmed — Accurately describes FBX scale issues and the new ufbx-based C++ importer in 4.5. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Blender FBX importer via ufbx — Aras Pranckevičius](https://aras-p.info/blog/2025/05/08/Blender-FBX-importer-via-ufbx/) — New ufbx C++ FBX importer in Blender 4.5: 5-20x faster, handles ASCII FBX, geometric transforms, ~20 bug fixes ; [Blender to UE5: the complete export pipeline](https://medium.com/@sarah.hyperdense/blender-to-ue5-the-complete-export-pipeline-17807d6f2c26) — Documents 100x scale mismatch between Blender meters and UE5 centimeters; FBX_SCALE_NONE vs FBX_SCALE_ALL strategies ; [Blender Issue #70161 — FBX I/O imports/exports objects with wrong scale transform](https://projects.blender.org/blender/blender-addons/issues/70161) — Long-standing FBX scale bug confirming that apply_scale_options is the correct mitigation

### OBJ import — new C++ importer (bpy.ops.wm.obj_import, 3.3+) · `✅ solid` · Blender 3.3–4.5 (C++ importer); bpy.ops.import_scene.obj removed in 4.0
**The Python OBJ importer/exporter addon was removed in Blender 4.0. The replacement is a C++ native importer accessible via bpy.ops.wm.obj_import (not bpy.ops.import_scene.obj). Scripts targeting 3.3+ must use the new operator.**
- **How:** ```python
import bpy # NEW (3.3+, required in 4.x):
bpy.ops.wm.obj_import( filepath="/path/to/model.obj", forward_axis="NEGATIVE_Z", # matches old Python importer default up_axis="Y", # matches old Python importer default global_scale=1.0, use_split_objects=True, # each 'o' group becomes a Blender object use_split_groups=False, # 'g' groups don't split objects
) # OLD (removed in 4.0 — do NOT use in 4.x scripts):
# bpy.ops.import_scene.obj(filepath=..., axis_forward='-Z', axis_up='Y') # OBJ export (also new C++ operator):
bpy.ops.wm.obj_export( filepath="/path/to/out.obj", forward_axis="NEGATIVE_Z", up_axis="Y", export_selected_objects=False, export_uv=True, export_normals=True, export_materials=True,
)
```
**Key differences from old Python importer:**
- Operator namespace: `bpy.ops.wm.*` not `bpy.ops.import_scene.*`
- Axis parameter names changed: old `axis_forward`/`axis_up` → new `forward_axis`/`up_axis` (order swapped)
- Performance: ~5x faster, ~4x less memory (C++ vs Python)
- Added `global_scale` parameter (was absent in older Python importer)
- MTL material file handling improved; less likely to silently skip textures
- **Gotchas:** bpy.ops.import_scene.obj is GONE in Blender 4.0. Any script using it will throw 'AttributeError: bpy_prop_collection[key]: key "import_scene" not found'. Check for this in inherited scripts.; Axis parameter names are DIFFERENT between old and new: old used `axis_forward='-Z'`, new uses `forward_axis='NEGATIVE_Z'` with enum values ('X','Y','Z','NEGATIVE_X','NEGATIVE_Y','NEGATIVE_Z').; The C++ importer was introduced in 3.2 alpha, matured in 3.3, and is the only OBJ importer in 4.0+. There is no compatibility shim.; OBJ has no embedded textures — MTL file must be co-located or textures will be missing. For the TRELLIS pipeline, GLB is preferred over OBJ precisely because GLB is self-contained.
- **For Studio:** Needed only if receiving OBJ-format meshes from non-TRELLIS sources. For the sprite-turnaround pipeline, GLB is the primary format. OBJ may appear in intermediate steps or from other generators.
- **Verify (solid):** Operator name change confirmed by Blender devtalk discussion (devtalk.blender.org/t/import-obj-from-python-using-new-native-importer/30941). 4.0 removal of bpy.ops.import_scene.obj confirmed by Blender 4.0 release notes stating 'OBJ and PLY I/O addons were removed, now implemented natively'. | cross-family (deepseek-v3.1): confirmed — Correctly identifies the shift from Python to C++ OBJ importer and the new operator name. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Import OBJ from python using new native importer — Blender Developer Forum](https://devtalk.blender.org/t/import-obj-from-python-using-new-native-importer/30941) — Confirms bpy.ops.wm.obj_import is the replacement for bpy.ops.import_scene.obj in Blender 3.2+ and required in 4.x ; [Speeding up Blender .obj import — Aras Pranckevičius](https://aras-p.info/blog/2022/05/12/speeding-up-blender-obj-import/) — Documents the C++ rewrite history: GSoC 2020, landed 3.1 exporter, 3.2 importer; performance gains 5x+ over Python ; [Wm Operators — Blender Python API (current)](https://docs.blender.org/api/current/bpy.ops.wm.html) — Official API location for bpy.ops.wm.obj_import and bpy.ops.wm.obj_export

### glTF axis conventions and PBR material mapping on import · `✅ solid` · Blender 4.0–4.5
**Understand how Blender converts glTF's Y-up coordinate system to Blender's Z-up, and how PBR materials (baseColorTexture, metallicRoughnessTexture, normalTexture) map to Principled BSDF.**
- **How:** **Axis:** glTF spec mandates Y-up, right-handed. Blender's importer silently converts on import: Y→Z, Z→-Y. No axis parameter is needed or available for glTF import (unlike OBJ/FBX). The imported mesh sits in Blender space correctly. On *export*, the exporter converts Blender's Z-up back to glTF Y-up. The `Y Up` toggle in the exporter UI (bpy: `export_yup=True`, default) controls this — leave True for all standards-compliant consumers (game engines, three.js, Godot, UE5). **PBR material mapping (auto on import):**
- `baseColorTexture` → Principled BSDF `Base Color` socket (image texture node)
- `metallicRoughnessTexture` → Metallic (B channel) and Roughness (G channel) sockets via Separate RGB node
- `normalTexture` → Normal Map node → Normal socket
- `occlusionTexture` → AO node or plugged into Base Color (importer approximation)
- `emissiveTexture` → Emission socket TRELLIS GLBs carry a baseColorTexture (diffuse albedo bake) and often metallicRoughness; no vertex colors by default. **Verify materials post-import:**
```python
for mat in bpy.data.materials: if mat.use_nodes: for node in mat.node_tree.nodes: if node.type == 'BSDF_PRINCIPLED': bc = node.inputs['Base Color'] print(mat.name, "Base Color linked:", bc.is_linked)
```
- **Gotchas:** TRELLIS outputs a GLB with Y-up (glTF spec). Blender imports it correctly with Z as up. If a downstream render script places the camera looking at Z=0 as ground, the model arrives in the right orientation without any manual rotation.; The normal map texture uses OpenGL convention (Y-up) in glTF. Blender's importer sets the Normal Map node to 'OpenGL' automatically — do not override to 'DirectX'.; Occlusion texture import is approximate — Blender does not have a dedicated AO socket; the importer may wire it differently across versions. If AO data is critical, bake a new AO map in Blender after import.; export_yup=True is the default and should stay True for Godot/UE5/Unity — all expect Y-up glTF. Setting False produces a non-standard file.
- **For Studio:** The Principled BSDF wiring is what makes TRELLIS albedo textures appear correctly in Blender's Cycles/EEVEE renders for the 8-direction sprite turnaround. Confirm Base Color is linked before rendering.
- **Verify (solid):** glTF Y-up conversion is spec-defined and documented in KhronosGroup/glTF-Blender-IO. PBR mapping to Principled BSDF is the documented behavior of io_scene_gltf2 across all 4.x versions. Confirmed in multiple community guides. | cross-family (deepseek-v3.1): confirmed — Accurate description of Y-up to Z-up conversion and PBR material mapping in glTF importer. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [glTF 2.0 — Blender Manual (latest)](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html) — Documents Y-up axis conversion and PBR material mapping for the bundled io_scene_gltf2 addon ; [KhronosGroup/glTF-Blender-IO GitHub](https://github.com/KhronosGroup/glTF-Blender-IO) — Source of truth for glTF importer/exporter; material mapping is implemented here

### glTF vertex colors / color attributes — 4.x behavior and export options · `✅ solid` · Blender 4.0–4.5 (breaking change at 4.1, partial fix at 4.2)
**Blender 4.1 changed when COLOR_0 vertex attributes get exported, breaking workflows that bake AO or use vertex colors for masking. Understand import vs export behavior and the 4.2 fix.**
- **How:** **Import (4.0–4.5):** glTF COLOR_0 always imports as a Blender Color Attribute (geometry attribute, domain=POINT or CORNER, data_type=FLOAT_COLOR or BYTE_COLOR). Access via `mesh.color_attributes[0]` or `mesh.vertex_colors` (legacy alias). The `colors_type` import parameter controls linear vs sRGB interpretation. **Export — 4.0 behavior:** vertex color exported whenever a Color Attribute exists on the mesh, regardless of material use. **Export — 4.1 BREAKING CHANGE:** vertex color only exported if the Color Attribute is connected in the material node tree (Vertex Color node → Principled BSDF Base Color multiplier, for example). Bare Color Attributes are silently dropped. Issue #120544 / #123925 confirmed this. **Export — 4.2 fix:** new `export_vertex_color` option (UI: "Export Active Vertex Colors" or "Export All Vertex Colors") allows export of Color Attributes without material node tree connection. ```python
# 4.2+ export with vertex colors forced:
bpy.ops.export_scene.gltf( filepath="/out/model.glb", export_format="GLB", export_colors=True # legacy name; in 4.2+ this triggers active-vc export
)
# Or for Blender 4.2+, check the exact param name at runtime:
import inspect
print(inspect.signature(bpy.ops.export_scene.gltf))
``` **Verify vertex colors imported correctly:**
```python
for obj in bpy.data.objects: if obj.type == 'MESH': mesh = obj.data print(obj.name, "color_attributes:", [a.name for a in mesh.color_attributes])
```
- **Gotchas:** 4.1 silently drops vertex colors on export if not in material node tree. Upgrade from 4.0 to 4.1 can silently corrupt baked-AO workflows.; The export parameter name for forcing vertex color export in 4.2+ is export_vertex_color in some builds; run inspect.signature() to get the actual name for your Blender build.; TRELLIS output GLBs typically carry no vertex colors (PBR textures instead). This recipe matters if you add AO bake as a color attribute post-import.; Blender uses 'Color Attributes' (4.0+ term) not 'Vertex Colors' (pre-4.0 term). The old mesh.vertex_colors accessor still works as an alias but iterates CORNER-domain byte attributes only — use mesh.color_attributes for full coverage.
- **For Studio:** Relevant if the studio adds AO bake as a Color Attribute post-import and then re-exports the annotated mesh. For pure render-only pipelines with TRELLIS GLBs (no re-export), import behavior is what matters: COLOR_0 imports cleanly in all 4.x.
- **Verify (solid):** Confirmed by Blender issue tracker #120544 and #123925; BabylonJS community post documents exact 4.1 behavior change. 4.2 fix confirmed by multiple search results referencing the beta option addition. | cross-family (deepseek-v3.1): confirmed — Accurately describes the 4.1 breaking change and 4.2 partial fix for vertex color export behavior. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Blender Issue #120544 — vertex color attributes doesn't export correctly with glb/gltf (4.1.0)](https://projects.blender.org/blender/blender/issues/120544) — Confirmed 4.1 breaking change: vertex colors silently dropped on glTF export unless connected to material node tree ; [Blender Issue #123925 — Blender 4.1 gltf exporter not exporting Vertex Color Attributes with materials but works in 4.0](https://projects.blender.org/blender/blender/issues/123925) — Documents regression from 4.0→4.1 and tracks the 4.2 fix ; [READ THIS if you use vertex colors and plan to update to Blender 4.1 — BabylonJS Forum](https://forum.babylonjs.com/t/read-this-if-you-use-vertex-colors-and-have-plans-to-update-to-blender-4-1/49611) — Community-confirmed 4.1 behavior: glTF exporter drops COLOR_0 if mesh has no material assigned or VC not in node tree

### Import a textured GLB in a headless bpy script · `▸ plausible` · Blender 4.0–4.5
**Load a TRELLIS-output GLB (textured mesh, PBR materials) into a blank Blender scene via bpy. The bundled io_scene_gltf2 addon is always enabled in 4.x — no addon.enable() needed.**
- **How:** ```python
import bpy # Clear default scene objects first
bpy.ops.wm.read_factory_settings(use_empty=True) # Import GLB — textures are embedded in the binary, so pack_images embeds them in.blend
bpy.ops.import_scene.gltf( filepath="/path/to/model.glb", import_pack_images=True, # embed packed textures into.blend merge_vertices=False, # keep TRELLIS topology as-is import_shading="NORMALS" # use mesh normals, not smooth-group auto
) # After import, mesh objects are available in bpy.context.scene.objects
for obj in bpy.context.scene.objects: if obj.type == "MESH": print(obj.name, obj.dimensions)
```
Operator: `bpy.ops.import_scene.gltf` (unchanged since 3.x — this name is stable through 4.5).
glTF is Y-up by default; Blender converts automatically on import to Z-up (Blender native), no axis argument required.
- **Gotchas:** import_pack_images defaults True in most 4.x builds but is worth being explicit — if False and the GLB embeds textures (which TRELLIS GLBs do), textures still load from the binary buffer, but re-saving the .blend without packing may lose them.; merge_vertices=True can silently weld seam vertices on UV islands, breaking texture mapping; leave False for TRELLIS output.; The operator requires a valid WINDOW context — in fully headless mode (blender -b --python script.py) a context override is NOT needed for this particular operator; it runs fine background-mode.; Draco-compressed GLBs (KHR_draco_mesh_compression): Blender 4.3 re-enabled Draco import after a DLL issue (issue #130545). In 4.0–4.2, import of Draco-compressed files may silently fail or error. TRELLIS does NOT use Draco by default — safe to ignore unless your GLB source is web-optimised.
- **For Studio:** Primary entry point for every TRELLIS GLB: import the mesh, verify it loaded, then proceed to normalize and set up 8-direction camera rig. Use import_pack_images=True so the headless script is self-contained.
- **Verify (plausible):** Operator name `import_scene.gltf` confirmed stable in official API docs (docs.blender.org/api/current). TRELLIS render script on HuggingFace (argojuni0506/TRELLIS-3D) uses exactly this call with merge_vertices=True; cube3d renderer confirms same. | cross-family (deepseek-v3.1): confirmed-with-fixes — The glTF importer doesn't have an import_shading parameter - shading is handled automatically based on mesh normals. [fix: Remove 'import_shading="NORMALS"' parameter as it doesn't exist in glTF importer] [confirmed by 1 of 1 juror(s) [confirmed-with-fixes]]
- **Sources:** [Import Scene Operators – Blender Python API (current)](https://docs.blender.org/api/current/bpy.ops.import_scene.html) — bpy.ops.import_scene.gltf is the stable operator for glTF/GLB import across Blender 3.x–4.x ; [TRELLIS-3D HuggingFace render.py](https://huggingface.co/datasets/argojuni0506/TRELLIS-3D/blob/main/dataset_toolkits/blender_script/render.py) — Real-world TRELLIS GLB pipeline uses bpy.ops.import_scene.gltf(filepath=..., merge_vertices=True) ; [cube3d renderer blender_script.py](https://huggingface.co/spaces/Nymbo/cube3d-interactive/raw/0c10674d822643fd6c4c5536c33fe8dd8cbb3bc1/cube/cube3d/renderer/blender_script.py) — Confirms import_scene.gltf with merge_vertices + import_shading='NORMALS' for AI-generated GLBs

### USD import/export in Blender 4.x — scope and limits · `▸ plausible` · Blender 4.0–4.5
**Blender 4.x includes built-in OpenUSD support (bpy.ops.wm.usd_import / bpy.ops.wm.usd_export). Useful for VFX studio pipelines and Omniverse integration, but has specific limits relevant to game-asset workflows.**
- **How:** ```python
import bpy # USD Import — requires active window context in some Blender versions
# For headless (blender -b), use context override:
with bpy.context.temp_override(**bpy.context.copy()): bpy.ops.wm.usd_import( filepath="/path/to/scene.usd", import_materials=True, import_meshes=True, import_cameras=False, import_lights=False, import_subdiv=False, # renamed to import_subdivision in Blender 5.0 attr_import_mode="NONE" # renamed to property_import_mode in Blender 5.0 ) # USD Export:
bpy.ops.wm.usd_export( filepath="/path/to/out.usd", export_materials=True, export_textures=True, export_meshes=True, export_cameras=False, export_lights=False, selected_objects_only=False, # export_textures_mode is available in newer 4.x builds # (supersedes older export_textures boolean)
)
```
**Material support:** Principled BSDF → USD Preview Surface (approximation). MaterialX export added in 4.2+. **Scope primitives:** USD Scope prims (no transform) import as Blender Empties at origin — imperfect but hierarchy-preserving. **Vertex color / attributes:** USD Primvar animation of vertex colors is supported for import/export (confirmed in 4.2 LTS). All four combinations of Vertex|FaceCorner × Color|ByteColor are round-trippable.
- **Gotchas:** bpy.ops.wm.usd_import needs a valid window/scene context. In headless mode, use `with bpy.context.temp_override(**bpy.context.copy()):` wrapper. bpy.ops.import_scene.gltf does NOT need this; USD does.; Blender 5.0 renamed two parameters: `import_subdiv` → `import_subdivision` and `attr_import_mode` → `property_import_mode`. If writing version-agnostic scripts, check bpy version at runtime.; USD Scope prims import as Empties at (0,0,0). In Blender 4.2, users reported meshes attached to Empties couldn't be directly selected in the viewport — a known hierarchy-mapping limitation.; USD texture export in 4.x copies textures to a subdirectory alongside the .usd file. The `export_textures_mode` parameter (4.2+) replaced the old `export_textures` boolean.; For the TRELLIS GLB sprite-turnaround pipeline, USD is not needed. USD is relevant only if integrating with a VFX pipeline (Houdini, Omniverse) or Pixar-based game engine workflow.
- **For Studio:** Not part of the core TRELLIS→sprite pipeline. Potentially useful if UE5's USD import pipeline is adopted for scene composition. Monitor USD support improvements per Blender LTS releases.
- **Verify (plausible):** Operator names confirmed. Context-override requirement for usd_import confirmed by devtalk.blender.org discussion. Parameter renames to 5.0 confirmed by Blender 5.0 Python API release notes. Scope-import-as-Empty confirmed by official USD manual entry. Some details (exact param list) are derived from multiple indirect sources rather than a direct API doc fetch. | cross-family (deepseek-v3.1): confirmed-with-fixes — USD import requires context override but the specific parameter names mentioned don't exist in 4.x. [fix: Remove 'import_subdiv' and 'attr_import_mode' parameters as they don't exist in 4.x USD importer] [confirmed by 1 of 1 juror(s) [confirmed-with-fixes]]
- **Sources:** [Issue with importing USD files via bpy.ops.wm.usd_import — Blender Developer Forum](https://devtalk.blender.org/t/issue-with-importing-usd-files-via-bpy-ops-wm-usd-import-and-python/26152) — Confirms usd_import requires context (unlike gltf import), and demonstrates bpy.context.temp_override usage in Blender 4.x ; [Universal Scene Description — Blender Manual (latest)](https://docs.blender.org/manual/en/latest/files/import_export/usd.html) — Documents USD import/export options including Scope-as-Empty mapping and vertex color attribute support ; [USDs in 4.2 — Blender Artists Community](https://blenderartists.org/t/usds-in-4-2/1546148) — Documents known USD hierarchy issues in 4.2 (Empties on every mesh, selection problems)

### Absences on these pages · `⚠ shaky` · Blender 4.x pin (GLB-first)
****Absent:** TRELLIS product name; unit-cube normalize recipe; farm camera framing; Draco-import reliability matrix by 4.0–4.5 patch. Scale/bounds post-import is post-doc craft, not a documented import knob.**
- **How:** Official 4.5 glTF/USD docs; import/export_scene.gltf; Khronos axes.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]

### Articulate3D: Holistic Understanding of 3D Scenes as Universal Scene Description · `⚠ shaky` · Blender 4.x pin (GLB-first)
**First large-scale non-synthetic indoor dataset **natively in USD**; argues USD beats PLY/JSON for hierarchical semantics, articulation, and simulation-ready interchange.**
- **How:** TRELLIS/GLB/glTF literature; USD adjacent not required; Pin 4.x.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [Articulate3D: Holistic Understanding of 3D Scenes as Universal Scene Description](https://arxiv.org/abs/2412.01398) — First large-scale non-synthetic indoor dataset **natively in USD**; argues USD beats PLY/JSON for hierarchical semantics, articulation, and simulation-ready interchange.

### BlendFusion · `⚠ shaky` · Blender 4.x pin (GLB-first)
**BlenderProc places cameras on a discrete orbit with azimuth every **45° (eight viewpoints)** around the object AABB center — 8-dir turnaround geometry for object-centric renders (no silent 4→5 invent).**
- **How:** TRELLIS/GLB/glTF literature; USD adjacent not required; Pin 4.x.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [BlendFusion](https://arxiv.org/abs/2604.09022) — BlenderProc places cameras on a discrete orbit with azimuth every **45° (eight viewpoints)** around the object AABB center — 8-dir turnaround geometry for object-centric renders (no silent 4→5 invent)

### DeepJEB++: Foundation Model-Driven Large-Scale 3D Engineering Dataset via 2D Latent Space Augmentation · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Selects TRELLIS (MIT) for multi-view conditioning and SLAT decode into NeRF / 3DGS / **triangle meshes** — mesh export + multi-view conditioning limits for engineering assets.**
- **How:** TRELLIS/GLB/glTF literature; USD adjacent not required; Pin 4.x.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [DeepJEB++: Foundation Model-Driven Large-Scale 3D Engineering Dataset via 2D Lat](https://arxiv.org/abs/2606.12994) — Selects TRELLIS (MIT) for multi-view conditioning and SLAT decode into NeRF / 3DGS / **triangle meshes** — mesh export + multi-view conditioning limits for engineering assets.

### EXT_meshopt_compression / meshopt · `⚠ shaky` · Blender 4.x pin (GLB-first)
**UNVERIFIED meshopt — Analog: GPU-friendly mesh compression for glTF shipping size. Holds for optional compressed GLB adjacent to Draco export knobs. Limit: compression ext ≠ cleanup/decimate before 8-dir render.**
- **How:** glTF-first/FBX trap/bake hold-with-limit; USD-required + float-latest omitted.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified; meshopt UNVERIFIED [no external verdict — not checked]
- **Sources:** [EXT_meshopt_compression / meshopt](https://www.khronos.org/blog/meshopt-compression-makes-3d-assets-smaller-and-faster) — UNVERIFIED meshopt — Analog: GPU-friendly mesh compression for glTF shipping size. Holds for optional compressed GLB adjacent to Draco export knobs. Limit: compression ext ≠ cleanup/decimate before 8-

### FBX (Experimental) · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Analog: proprietary FBX path marked Experimental with chronic unit/scale pitfalls (KB lane). Holds as the interchange trap vs GLB for generative meshes. Limit: Autodesk DCC round-trips ≠ TRELLIS GLB contract.**
- **How:** glTF-first/FBX trap/bake hold-with-limit; USD-required + float-latest omitted.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [FBX (Experimental)](https://docs.blender.org/manual/en/4.5/files/import_export/fbx.html) — Analog: proprietary FBX path marked Experimental with chronic unit/scale pitfalls (KB lane). Holds as the interchange trap vs GLB for generative meshes. Limit: Autodesk DCC round-trips ≠ TRELLIS GLB c

### From USD Scenes to Knowledge Graphs: Zero-Shot Ontology Grounding with LLMs · `⚠ shaky` · Blender 4.x pin (GLB-first)
**USD encodes rich scene graphs but relies on user-defined identifiers; grounding maps prims to OWL — interchange limit: USD structure alone is not a shared ontology.**
- **How:** TRELLIS/GLB/glTF literature; USD adjacent not required; Pin 4.x.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [From USD Scenes to Knowledge Graphs: Zero-Shot Ontology Grounding with LLMs](https://arxiv.org/abs/2606.09134) — USD encodes rich scene graphs but relies on user-defined identifiers; grounding maps prims to OWL — interchange limit: USD structure alone is not a shared ontology.

### Generating Actionable Robot Knowledge Bases by Combining 3D Scene Graphs with Robot Ontologies · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Converts diverse scene graphs into unified **USD** so only one importer/exporter to USD is required per format — USD-as-intermediary interchange pattern (and its mapping cost).**
- **How:** TRELLIS/GLB/glTF literature; USD adjacent not required; Pin 4.x.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [Generating Actionable Robot Knowledge Bases by Combining 3D Scene Graphs with Ro](https://arxiv.org/abs/2507.11770) — Converts diverse scene graphs into unified **USD** so only one importer/exporter to USD is required per format — USD-as-intermediary interchange pattern (and its mapping cost).

### Headless farm path (on-page composition only) · `⚠ shaky` · Blender 4.x pin (GLB-first)
**`-b`/`-P` (STUDY-046) + `bpy.ops.import_scene.gltf(filepath=…)` loads textured GLB into a background scene; optional later `export_scene.gltf` / USD export. Pages document operators + axes; they do not invent a silent 5.0 API.**
- **How:** Official 4.5 glTF/USD docs; import/export_scene.gltf; Khronos axes.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]

### Khronos glTF 2.0 Specification · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Runtime delivery format; +Y up, +Z forward, meters; GLB = JSON+BIN in one file (`model/gltf-binary`). Core metallic-roughness PBR. Normative axis/units for why Blender rotates on import.**
- **How:** Official 4.5 glTF/USD docs; import/export_scene.gltf; Khronos axes.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [Khronos glTF 2.0 Specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html) — Runtime delivery format; +Y up, +Z forward, meters; GLB = JSON+BIN in one file (`model/gltf-binary`). Core metallic-roughness PBR. Normative axis/units for why Blender rotates on import.

### MExECON: Multi-view Extended Explicit Clothed humans Optimized via Normal integration · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Blender renders an **8-view** set with cameras uniformly around the subject — same orbit cardinality as the studio 8-dir turnaround (Blender 4.x pin held).**
- **How:** TRELLIS/GLB/glTF literature; USD adjacent not required; Pin 4.x.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [MExECON: Multi-view Extended Explicit Clothed humans Optimized via Normal integr](https://arxiv.org/abs/2508.15500) — Blender renders an **8-view** set with cameras uniformly around the subject — same orbit cardinality as the studio 8-dir turnaround (Blender 4.x pin held).

### Modifiers introduction (non-destructive → apply) · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Analog: modifiers are non-destructive until applied; export must bake evaluated mesh. Holds for `export_apply=True` / bake-before-export in cleanup→GLB. Limit: modifier stack ≠ glTF material mapping.**
- **How:** glTF-first/FBX trap/bake hold-with-limit; USD-required + float-latest omitted.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [Modifiers introduction (non-destructive → apply)](https://docs.blender.org/manual/en/4.5/modeling/modifiers/introduction.html) — Analog: modifiers are non-destructive until applied; export must bake evaluated mesh. Holds for `export_apply=True` / bake-before-export in cleanup→GLB. Limit: modifier stack ≠ glTF material mapping.

### NANO3D: A Training-Free Approach for Efficient 3D Editing Without Masks · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Stores SLAT then uses FlexiCube to convert SLAT into **explicit GLB meshes** for downstream apps — names GLB as the compiled mesh delivery from TRELLIS-class latents.**
- **How:** TRELLIS/GLB/glTF literature; USD adjacent not required; Pin 4.x.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [NANO3D: A Training-Free Approach for Efficient 3D Editing Without Masks](https://arxiv.org/abs/2510.15019) — Stores SLAT then uses FlexiCube to convert SLAT into **explicit GLB meshes** for downstream apps — names GLB as the compiled mesh delivery from TRELLIS-class latents.

### OpenUSD home · `⚠ shaky` · Blender 4.x pin (GLB-first)
**USD as collaborative scene platform / DCC interchange (geometry, shading, lighting). Frames why Blender ships USD I/O; does not define Blender operator knobs.**
- **How:** Official 4.5 glTF/USD docs; import/export_scene.gltf; Khronos axes.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [OpenUSD home](https://openusd.org/release/index.html) — USD as collaborative scene platform / DCC interchange (geometry, shading, lighting). Frames why Blender ships USD I/O; does not define Blender operator knobs.

### Referencing Layers (USD composition) · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Analog: compose scenes by referencing layers/opinions. Holds as VFX composition craft adjacent to multi-asset pipelines. Limit: USD composition ≠ required for a single GLB sprite turnaround.**
- **How:** glTF-first/FBX trap/bake hold-with-limit; USD-required + float-latest omitted.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [Referencing Layers (USD composition)](https://openusd.org/release/tut_referencing_layers.html) — Analog: compose scenes by referencing layers/opinions. Holds as VFX composition craft adjacent to multi-asset pipelines. Limit: USD composition ≠ required for a single GLB sprite turnaround.

### Structured 3D Latents for Scalable and Versatile 3D Generation (TRELLIS) · `⚠ shaky` · Blender 4.x pin (GLB-first)
**SLAT decodes to versatile formats (radiance fields, 3D Gaussians, meshes via FlexiCubes) from dense multiview features — generative mesh artifact pole feeding TRELLIS→import pipelines (not a silent Blender major bump).**
- **How:** TRELLIS/GLB/glTF literature; USD adjacent not required; Pin 4.x.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [Structured 3D Latents for Scalable and Versatile 3D Generation (TRELLIS)](https://arxiv.org/abs/2412.01506) — SLAT decodes to versatile formats (radiance fields, 3D Gaussians, meshes via FlexiCubes) from dense multiview features — generative mesh artifact pole feeding TRELLIS→import pipelines (not a silent Bl

### Universal Scene Description · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Import meshes/materials/cameras/lights/volumes/points; Y-up → Z-up rotation on roots; Import Options: Scale, Apply Unit Conversion Scale, Import USD Preview, textures None/Packed/Copy. Export: meshes/cameras/lights/curves; USDZ via `.usdz`; Convert Orientation; USD Preview Surface / MaterialX networks. Note: layers/variants not fully handled.**
- **How:** Official 4.5 glTF/USD docs; import/export_scene.gltf; Khronos axes.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [Universal Scene Description](https://docs.blender.org/manual/en/4.5/files/import_export/usd.html) — Import meshes/materials/cameras/lights/volumes/points; Y-up → Z-up rotation on roots; Import Options: Scale, Apply Unit Conversion Scale, Import USD Preview, textures None/Packed/Copy. Export: meshes/

### Universal Scene Description (Blender 4.5) · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Analog: Blender USD I/O exists but importer “does not yet handle certain USD composition concepts, such as layers and references.” Holds as scoped USD support; reinforces GLB-first for TRELLIS. Limit: Blender USD gaps ≠ OpenUSD studio full stack.**
- **How:** glTF-first/FBX trap/bake hold-with-limit; USD-required + float-latest omitted.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [Universal Scene Description (Blender 4.5)](https://docs.blender.org/manual/en/4.5/files/import_export/usd.html) — Analog: Blender USD I/O exists but importer “does not yet handle certain USD composition concepts, such as layers and references.” Holds as scoped USD support; reinforces GLB-first for TRELLIS. Limit:

### bpy.ops.export_scene.gltf · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Headless export knobs: `export_format`, `export_yup`, `export_apply`, `export_draco_mesh_compression_enable` (+ quantization), `export_materials`, `export_texcoords`/`export_normals`, `use_selection`/`use_visible`. Default filter `*.glb`.**
- **How:** Official 4.5 glTF/USD docs; import/export_scene.gltf; Khronos axes.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [bpy.ops.export_scene.gltf](https://docs.blender.org/api/4.5/bpy.ops.export_scene.html) — Headless export knobs: `export_format`, `export_yup`, `export_apply`, `export_draco_mesh_compression_enable` (+ quantization), `export_materials`, `export_texcoords`/`export_normals`, `use_selection`/

### bpy.ops.import_scene.gltf · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Headless entry: `filepath`, `import_pack_images`, `merge_vertices`, `import_shading`, `import_webp_texture`, `import_scene_as_collection`, `import_select_created_objects`. Filter `*.glb;*.gltf`. No TRELLIS-specific args on page.**
- **How:** Official 4.5 glTF/USD docs; import/export_scene.gltf; Khronos axes.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [bpy.ops.import_scene.gltf](https://docs.blender.org/api/4.5/bpy.ops.import_scene.html) — Headless entry: `filepath`, `import_pack_images`, `merge_vertices`, `import_shading`, `import_webp_texture`, `import_scene_as_collection`, `import_select_created_objects`. Filter `*.glb;*.gltf`. No TR

### glTF · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Analog: royalty-free runtime shipping format (JSON + binary `.glb`). Holds for TRELLIS→`import_scene.gltf`→8-dir sprites as the decisive interchange, not FBX/USD-first. Limit: runtime delivery spec ≠ headless camera farm knobs.**
- **How:** glTF-first/FBX trap/bake hold-with-limit; USD-required + float-latest omitted.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [glTF](https://www.khronos.org/gltf/) — Analog: royalty-free runtime shipping format (JSON + binary `.glb`). Holds for TRELLIS→`import_scene.gltf`→8-dir sprites as the decisive interchange, not FBX/USD-first. Limit: runtime delivery spec ≠

### glTF 2.0 · `⚠ shaky` · Blender 4.x pin (GLB-first)
**Import/export `.glb`/`.gltf`; PBR Principled map; formats GLB binary / Separate / Embedded. Import knobs: Pack Images, Merge Vertices, Shading, Import Scenes as Collections. Export: Format, Y Up, Apply Modifiers, Draco (`KHR_draco_mesh_compression`), materials/vertex color modes. Enabled by default.**
- **How:** Official 4.5 glTF/USD docs; import/export_scene.gltf; Khronos axes.
- **Gotchas:** STUDY-047. Pin 4.x. Silent 4→5: 0. Do not invent USD-required-for-sprites or float-latest. meshopt blog not verified.
- **For Studio:** TRELLIS→GLB→8-dir turnaround; USD adjacent not required.
- **Verify (shaky):** STUDY-047 deepen; Pin 4.x; silent 4→5: 0; GLB-first; default unverified [no external verdict — not checked]
- **Sources:** [glTF 2.0](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html) — Import/export `.glb`/`.gltf`; PBR Principled map; formats GLB binary / Separate / Embedded. Import knobs: Pack Images, Merge Vertices, Shading, Import Scenes as Collections. Export: Format, Y Up, Appl

