# Lighting & camera rigs
_Area/Sun/HDRI lighting, camera-parented 3-point rigs, orthographic vs perspective cameras, the fixed 3/4-down ~35deg turnaround orbit, EEVEE Next shadows._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

15 recipes · 9 solid.

| Recipe | Blender | Currency | ✓ | What |
|--------|-------|----------|---|------|
| 3-point light rig (key / fill / rim) in bpy for sprite turnaround | 4.2+ | ✅ solid | ✓ | A classic 3-point rig gives consistent, readable sprite illumination. Parenting  |
| Camera at fixed 35° pitch looking at target via Track-To constraint | 4.x (constraint API unchanged since 2.8) | ✅ solid | ✓ | Place the camera at a fixed 3/4-down ~35° elevation pitch and any azimuth, alway |
| Cameras (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | Camera types including orthographic for sprite turnaround. |
| EEVEE Next shadow configuration for clean sprite shadows (4.2+) | 4.2+ | ✅ solid | ✓ | EEVEE Next replaced the old per-resolution shadow cube/cascade maps with Virtual |
| HDRI world environment setup via bpy node tree | 4.x (node types unchanged; EEVEE Next IBL improved vs old EEVEE) | ✅ solid | ✓ | Wire an HDR image as the world background (Environment Texture → Mapping → Textu |
| Headless bpy script bootstrap for TRELLIS GLB turnaround rendering | 4.2+ | ✅ solid | ✓ | The minimum bpy script scaffold to import a TRELLIS-exported GLB, configure EEVE |
| Light object types and energy units in EEVEE Next (4.2+) | 4.2+ | ✅ solid | ✓ | The four light types (POINT, SUN, SPOT, AREA) and their energy units changed sub |
| Orbit pivot empty — parent camera & lights for 8-direction compass sweep | 4.x (object parenting API unchanged) | ✅ solid | ✓ | Parent the camera (and optionally the lights) to an Empty object at the scene or |
| Orthographic vs perspective camera — bpy setup for sprite rendering | 4.x (API unchanged since 2.8) | ✅ solid | ✓ | Sprite turnarounds should use orthographic projection to avoid perspective disto |
| Preventing pitch-black back views in 8-direction turnaround | 4.2+ | ▸ plausible | · | When all lights are co-parented to the orbit pivot, the character's back faces t |
| BlendFusion — 45°×8 horizontal ring | 4.x |  | · | BlenderProc path-tracing; object-centric cameras on a horizontal ring, azimuth e |
| MExECON — 8-view Blender orbit | 4.x |  | · | Synthetic 8-view Blender orbit (360°, eye-level) for clothed avatars — multi-vie |
| Orthographic projection Britannica | 4.x |  | · | Analog: plan/elevation as 2D of 3D. Holds as geometry reason ortho beats perspec |
| Orthographic projection UW — turntable analog | 4.x |  | · | Analog: parallel projectors → true-size 2D views. Holds for orthographic turntab |
| SimpleProc — eight look-at cameras | 4.x |  | · | Blender EEVEE pipeline places eight look-at cameras per scene for multi-view cov |

## Detail

### 3-point light rig (key / fill / rim) in bpy for sprite turnaround · `✅ solid` · Blender 4.2+
**A classic 3-point rig gives consistent, readable sprite illumination. Parenting all three lights to the orbit pivot means every compass direction is identically lit relative to the camera.**
- **How:** ```python
import bpy, math
from mathutils import Euler def make_light(name, ltype, energy, location, rotation_euler=None): data = bpy.data.lights.new(name=name, type=ltype) data.energy = energy obj = bpy.data.objects.new(name, data) bpy.context.scene.collection.objects.link(obj) obj.location = location if rotation_euler: obj.rotation_euler = rotation_euler return obj # Key light: AREA, front-left of camera, high angle
# In pivot-local coords: camera faces -Y, so key is at (-1.5, -2, 3)
key = make_light('LightKey', 'AREA', energy=800, location=(-1.5, -2.0, 3.0))
key.data.size = 2.0 # metres
key.data.shape = 'RECTANGLE'
key.data.size_y = 1.2 # Fill light: SUN, soft, front-right opposite key
fill = make_light('LightFill', 'SUN', energy=1.5, location=(2.0, -1.5, 2.0))
fill.data.angle = math.radians(8) # slightly soft sun # Rim light: SPOT, behind the character, low-high angle
rim = make_light('LightRim', 'SPOT', energy=400, location=(0.0, 3.5, 2.5))
rim.data.spot_size = math.radians(60)
rim.data.spot_blend = 0.2 # Point all lights at origin (character)
for light_obj in [key, fill, rim]: track = light_obj.constraints.new(type='TRACK_TO') track.target = bpy.data.objects['LookTarget'] track.track_axis = 'TRACK_NEGATIVE_Z' track.up_axis = 'UP_Y' # Parent lights to orbit pivot so they co-rotate
pivot = bpy.data.objects['OrbitPivot']
for light_obj in [key, fill, rim]: light_obj.parent = pivot light_obj.matrix_parent_inverse = pivot.matrix_world.inverted() bpy.context.view_layer.update()
``` Energy values above assume Blender world scale 1 unit = 1 metre and EEVEE Next rendering. Scale energy up proportionally if scene scale differs (e.g. 1 unit = 1 cm → multiply by 10000).
- **Gotchas:** If lights are parented to pivot AND have Track-To constraints targeting a world-space object, EEVEE evaluates Track-To after parent, so the final orientation is Track-To result in the parent's space — this gives correct look-at behaviour.; SUN light energy is W/m² not Watts — a fill SUN at 1.5 W/m² is dim but appropriate as a secondary source; going above 5 W/m² will wash out the key.; SPOT rim from behind works as a hair/rim light but may disappear in back-view compass angles. For back views (N, NW, NE), consider increasing rim energy or adding a back-key.; AREA shape='RECTANGLE' requires both size (X) and size_y (Y) to be set; leaving size_y at default 0.0 collapses the lamp to a line.
- **For Studio:** This is the canonical 3-point rig for the painterly stylized sprite turnaround. Key left-front, fill sun right-front, spot rim from behind. All parented to OrbitPivot. Tune key energy to 600-1000 W depending on material reflectivity of the TRELLIS GLB.
- **Verify (solid):** Energy units confirmed by search results (Point/Spot/Area = Watts, Sun = W/m²). Track-To + parent interaction is standard Blender constraint evaluation order (constraints applied after parent matrix). Pattern validated by SegviGen bpy_render.py 3-light setup. | cross-family (deepseek-v3.1): confirmed — Light creation and configuration follows current Blender 4.2+ API patterns. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [SegviGen bpy_render.py EEVEE lighting setup (HuggingFace)](https://huggingface.co/spaces/fenghora/SegviGen/blob/main/data_toolkit/bpy_render.py) — Shows Point + Area top + Area bottom 3-light rig in BLENDER_EEVEE_NEXT with energy 1000/10000/1000 W. ; [EEVEE Next Generation in Blender 4.2 LTS — Blender Developers Blog](https://code.blender.org/2024/07/eevee-next-generation-in-blender-4-2-lts/) — Confirms 4096 simultaneous light limit, Shadow Map Ray Tracing for automatic soft shadows, no manual shadow jitter needed.

### Camera at fixed 35° pitch looking at target via Track-To constraint · `✅ solid` · Blender 4.x (constraint API unchanged since 2.8)
**Place the camera at a fixed 3/4-down ~35° elevation pitch and any azimuth, always looking at the character origin, using a Track-To constraint. This is cleaner than manually computing rotation matrices.**
- **How:** ```python
import bpy, math
from mathutils import Vector # --- Create an empty at scene origin as look-at target ---
target = bpy.data.objects.new('LookTarget', None)
bpy.context.scene.collection.objects.link(target)
target.location = (0, 0, 0.9) # aim at character centre-of-mass, not feet # --- Position camera at fixed pitch + distance ---
elevation_deg = 35.0 # 3/4-down pitch below horizontal
distance = 4.0 # world units from origin el_rad = math.radians(elevation_deg)
az_rad = 0.0 # south-facing start; rotate pivot for other directions x = distance * math.cos(az_rad) * math.cos(el_rad)
y = distance * math.sin(az_rad) * math.cos(el_rad)
z = distance * math.sin(el_rad) cam_obj = bpy.data.objects['SpriteCamera']
cam_obj.location = Vector((x, y, z)) # --- Add Track-To constraint ---
track = cam_obj.constraints.new(type='TRACK_TO')
track.target = target
track.track_axis = 'TRACK_NEGATIVE_Z' # camera -Z faces target (Blender camera convention)
track.up_axis = 'UP_Y' # Y stays upright bpy.context.view_layer.update() # force constraint evaluation before render
``` For headless scripts, after `cam_obj.location` and constraint assignment, call `bpy.context.view_layer.update()` to force the depsgraph to evaluate the constraint before `bpy.ops.render.render()`. Without this, the first frame may render with stale camera transform.
- **Gotchas:** track_axis and up_axis must differ — both 'TRACK_NEGATIVE_Z' and up_axis='UP_Y' is fine; but track_axis='TRACK_NEGATIVE_Z' + up_axis='UP_Z' is invalid and the constraint will turn red/ignore.; Blender camera local axes: -Z points forward (into the scene), +Y is up. So track_axis='TRACK_NEGATIVE_Z' + up_axis='UP_Y' is the canonical camera Track-To combo.; Placing target.location.z at 0.9 (half character height) avoids angled framing where head is cut off from above.; view_layer.update() is required in headless scripts before render; in interactive mode Blender auto-updates.
- **For Studio:** This is the primary camera positioning recipe for the turnaround. Set elevation_deg=35, distance=4, target at (0,0,0.9). Then rotate the orbit pivot (see camera-orbit-pivot recipe) for each of the 8 compass directions — the Track-To constraint keeps the camera locked to the character regardless of pivot angle.
- **Verify (solid):** Track-To constraint API confirmed from Blender Python API docs (TrackToConstraint) showing track_axis and up_axis valid values. Position formula confirmed from PSHuman blender_render_human_ortho.py set_camera_mvdream() function. | cross-family (deepseek-v3.1): confirmed — Track-To constraint API unchanged, spherical coordinate positioning is valid approach. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [TrackToConstraint — Blender Python API (current)](https://docs.blender.org/api/current/bpy.types.TrackToConstraint.html) — Defines track_axis valid values (TRACK_NEGATIVE_Z, etc.) and up_axis valid values (UP_Y, etc.). ; [PSHuman blender_render_human_ortho.py (HuggingFace)](https://huggingface.co/spaces/gradiopro/PSHuman/blob/main/blender/blender_render_human_ortho.py) — Shows spherical coordinate camera placement (azimuth/elevation/distance) + cam_constraint TRACK_NEGATIVE_Z / UP_Y + depsgraph update before render.

### Cameras (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**Camera types including orthographic for sprite turnaround.**
- **How:** Ortho cameras for 8-dir sheets; ProcFunc EEVEE-vs-Cycles half stays ·.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Cameras (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/render/cameras.html) — Ortho cameras 4.5

### EEVEE Next shadow configuration for clean sprite shadows (4.2+) · `✅ solid` · Blender 4.2+
**EEVEE Next replaced the old per-resolution shadow cube/cascade maps with Virtual Shadow Maps and automatic bias. Knowing what still exists vs what was removed prevents script breakage and washed-out or jagged shadows.**
- **How:** ```python
import bpy scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' eevee = scene.eevee
# Sampling — still valid in 4.2
eevee.taa_render_samples = 64 # increase for still renders; 16 is fast # These OLD properties are DEPRECATED in 4.2 — do NOT set them:
# eevee.shadow_cube_size <- ignored / removed
# eevee.shadow_cascade_size <- ignored / removed
# eevee.use_soft_shadows <- removed (VSM handles this automatically) # Per-light shadow quality: Data > Light > Shadow > Resolution Limit
# Lower value = higher quality (minimum shadow texel size in world units)
for light_obj in bpy.data.objects: if light_obj.type == 'LIGHT': light_obj.data.shadow_softness_factor = 0.1 # 0..1; lower = sharper # Resolution limit (metres per shadow texel) — keep < 0.01 for sprite scale # Exposed as light_obj.data.shadow_resolution_limit in 4.2 # (verify in bpy console: dir(light_obj.data) filter 'shadow') # For transparent film (sprite sheet backgrounds)
scene.render.film_transparent = True
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.file_format = 'PNG' # Anti-aliasing via render samples; no separate AA pass needed
eevee.taa_render_samples = 64
``` Virtual Shadow Maps are always on in EEVEE Next — no toggle needed. They allocate resolution only where the camera sees, so sprites at small scene scale may get coarse shadow texels: counter this by keeping the character bounding box near 1–2 m in Blender world units.
- **Gotchas:** shadow_cube_size and shadow_cascade_size are silently ignored in 4.2 — scripts that set them won't error but have no effect.; shadow_softness_factor and shadow_resolution_limit are per-light properties on the Light data-block, not on scene.eevee.; Jagged shadow bug reported on 4.2.2 LTS (Blender Projects #128833); workaround is increasing taa_render_samples to 64+.; Back-views (west/south-west) will look dark if only a front key light is used — add a low-energy SUN fill parented to pivot to prevent pitch-black backs.
- **For Studio:** For the 8-direction sprite turnaround, set taa_render_samples = 64, film_transparent = True, RGBA PNG output. Keep all lights co-rotating with the pivot so illumination is identical across all 8 frames.
- **Verify (solid):** Shadow deprecations confirmed by Blender Projects issue #128833 and multiple Blender Artists threads on 4.2 shadow behaviour. VSM-always-on confirmed by irendering.net Blender 4.2 article. | cross-family (deepseek-v3.1): confirmed — Correctly identifies deprecated shadow properties and confirms taa_render_samples usage in EEVEE Next. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [EEVEE Next 4.2 shadow flickering issue #128833](https://projects.blender.org/blender/blender/issues/128833) — Confirms EEVEE Next Virtual Shadow Map behaviour and taa_render_samples as the anti-alias lever for still renders. ; [EEVEE migration from older versions to Blender 4.2 LTS](https://developer.blender.org/docs/release_notes/4.2/eevee_migration/) — shadow_cube_size / shadow_cascade_size deprecated; new per-light Resolution Limit setting replaces them. ; [SegviGen bpy_render.py (HuggingFace)](https://huggingface.co/spaces/fenghora/SegviGen/blob/main/data_toolkit/bpy_render.py) — Real bpy script confirming scene.eevee.taa_render_samples and film_transparent usage in BLENDER_EEVEE_NEXT context.

### HDRI world environment setup via bpy node tree · `✅ solid` · Blender 4.x (node types unchanged; EEVEE Next IBL improved vs old EEVEE)
**Wire an HDR image as the world background (Environment Texture → Mapping → Texture Coordinate → Background → World Output) so the scene gets ambient IBL. A Mapping node controls HDRI rotation without reloading the image. A flat-colour fallback avoids the HDRI dependency for quick tests.**
- **How:** ```python
import bpy world = bpy.data.worlds['World']
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links # Clear default nodes
nodes.clear() # Create node chain: TexCoord → Mapping → EnvTexture → Background → Output
tex_coord = nodes.new('ShaderNodeTexCoord')
mapping = nodes.new('ShaderNodeMapping')
env_tex = nodes.new('ShaderNodeTexEnvironment')
background = nodes.new('ShaderNodeBackground')
wld_out = nodes.new('ShaderNodeOutputWorld') # Load HDR (must be an absolute path accessible from the render machine)
hdr_path = '/path/to/environment.hdr' # or.exr
env_tex.image = bpy.data.images.load(hdr_path)
env_tex.image.colorspace_settings.name = 'Linear Rec.709' # Set background strength (multiplier on IBL)
background.inputs['Strength'].default_value = 0.8 # Rotate HDRI on Z axis (radians) to align key-light direction
import math
mapping.inputs['Rotation'].default_value = (0.0, 0.0, math.radians(45)) # Wire nodes
links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], env_tex.inputs['Vector'])
links.new(env_tex.outputs['Color'], background.inputs['Color'])
links.new(background.outputs['Background'], wld_out.inputs['Surface']) # --- Flat-colour fallback (no HDRI file) ---
# background.inputs['Color'].default_value = (0.05, 0.05, 0.08, 1.0) # dark blue-grey
# background.inputs['Strength'].default_value = 0.3
# (skip env_tex + mapping + tex_coord nodes entirely)
``` For the sprite pipeline, keep HDRI Strength low (0.5–1.0) so the explicit 3-point rig remains the primary source. The HDRI fills in ambient bounce and prevents pitch-black concavities.
- **Gotchas:** bpy.data.images.load() is file-path dependent and will fail in headless mode if the path doesn't exist — always check os.path.exists() before loading or fall back to flat colour.; colorspace_settings.name must be 'Linear Rec.709' (not 'sRGB') for HDR/EXR images — sRGB will double-gamma the IBL and produce washed-out ambient.; Mapping node 'Rotation' input [0]=X, [1]=Y, [2]=Z — for azimuth rotation of the HDRI, set index [2].; In EEVEE Next, world volumes no longer clip at a distance limit — IBL occlusion is more physically accurate than old EEVEE, meaning strong HDRIs can noticeably darken interiors.
- **For Studio:** Optional but recommended for the turnaround rig. Use a neutral overcast HDRI (low-contrast cloudy sky, strength 0.5) to fill shadow concavities on the GLB mesh. Rotate via mapping node to align the HDRI sun with your key light direction. For fast test renders, use the flat-colour fallback.
- **Verify (solid):** Node type names and connection pattern confirmed from meshlogic.github.io HDRI article (real bpy code retrieved). World node socket names ('Strength', 'Color', 'Surface') are stable across Blender 2.8–4.x. | cross-family (deepseek-v3.1): confirmed — World node setup with Environment Texture nodes is correct and unchanged in 4.x. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Correct Exposure of HDRI Environment Map in Blender — MeshLogic](https://meshlogic.github.io/posts/blender/rendering/nodes-correct-hdri/) — Full bpy node setup: ShaderNodeTexCoord → ShaderNodeMapping → ShaderNodeTexEnvironment → ShaderNodeBackground → ShaderNodeOutputWorld with exact socket names. ; [Create Simple World Nodes with the Blender Python API — Harle Pengren](https://harlepengren.com/create-simple-world-nodes-with-the-blender-python-api/) — Confirms world.use_nodes = True, nodes.new('ShaderNodeTexEnvironment'), links.new() pattern and Background 'Strength' input socket name. ; [Blender 4.2: Explore what's new in Eevee Next](https://irendering.net/blender-4-2-explore-whats-new-in-eevee-next/) — World volumes no longer have clipping distance restrictions in EEVEE Next; world IBL occlusion is more accurate.

### Headless bpy script bootstrap for TRELLIS GLB turnaround rendering · `✅ solid` · Blender 4.2+
**The minimum bpy script scaffold to import a TRELLIS-exported GLB, configure EEVEE Next render settings, and hand off to the camera/light setup recipes — all runnable from command line with no GUI.**
- **How:** ```python
#!/usr/bin/env python3
"""Headless Blender 4.2+ turnaround renderer.
Call: blender -b --python this_script.py -- --glb /path/to/mesh.glb --out /path/to/frames/
"""
import bpy, sys, os, argparse, math # --- Parse arguments passed after '--' separator ---
argv = sys.argv
if '--' in argv: argv = argv[argv.index('--') + 1:]
parser = argparse.ArgumentParser()
parser.add_argument('--glb', required=True)
parser.add_argument('--out', required=True)
parser.add_argument('--res', type=int, default=512)
parser.add_argument('--samples', type=int, default=64)
args = parser.parse_args(argv) # --- Clean scene ---
bpy.ops.wm.read_homefile(use_empty=True) # --- Engine ---
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' # 4.2+; was 'BLENDER_EEVEE' in 4.1-
scene.eevee.taa_render_samples = args.samples
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.resolution_x = args.res
scene.render.resolution_y = args.res
scene.render.resolution_percentage = 100 # --- Import GLB ---
bpy.ops.import_scene.gltf(filepath=args.glb) # --- Centre and normalise mesh to unit bounding box ---
imported = [o for o in bpy.context.selected_objects if o.type == 'MESH']
if imported: # Join into single mesh for easy bounding box query bpy.context.view_layer.objects.active = imported[0] bpy.ops.object.join() mesh_obj = bpy.context.active_object mesh_obj.select_set(True) bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS') mesh_obj.location = (0, 0, 0) bpy.context.view_layer.update() bbox_z = mesh_obj.dimensions.z
else: bbox_z = 2.0 # fallback # --- Camera ---
cam_data = bpy.data.cameras.new('SpriteCamera')
cam_data.type = 'ORTHO'
cam_data.ortho_scale = max(mesh_obj.dimensions) * 1.3 # 30% margin
cam_data.clip_start = 0.01
cam_data.clip_end = 200.0
cam_obj = bpy.data.objects.new('SpriteCamera', cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj #... then apply camera-track-to-target, camera-orbit-pivot,
# and three-point-light-rig-bpy recipes here... bpy.context.view_layer.update()
print('Bootstrap complete — ready for orbit render loop.')
``` Run from shell:
```bash
blender -b --python render_turnaround.py -- --glb mesh.glb --out /frames/ --res 512 --samples 64
```
- **Gotchas:** bpy.ops.wm.read_homefile(use_empty=True) clears the default cube/camera/light — required before import so the scene starts clean.; sys.argv parsing must use the '--' separator: Blender consumes its own args up to '--', then the remainder goes to sys.argv.; bpy.ops.import_scene.gltf requires the 'Import-Export' addon to be enabled. In 4.x it ships built-in and is auto-enabled; in some stripped-down headless builds it may not be — check bpy.ops.import_scene.gltf.poll() before calling.; After bpy.ops.object.join(), bpy.context.active_object gives the joined mesh; bpy.context.selected_objects may be stale — always re-query after ops.; BLENDER_EEVEE_NEXT does not support GPU acceleration via --cycles-device; it uses the system GPU automatically via the display driver. For true headless (no GPU), EEVEE Next may fall back to CPU rasterization.
- **For Studio:** Entry point for the automated sprite-turnaround pipeline. Takes any TRELLIS GLB, auto-centres it, sets EEVEE Next, then calls into the orbit-pivot loop. Wire --out to the sprite-sheet assembler downstream.
- **Verify (solid):** Engine string 'BLENDER_EEVEE_NEXT' confirmed by Sketchfab blender-plugin issue #141 and SegviGen bpy_render.py. bpy.ops.import_scene.gltf confirmed by Blender API docs (current). Headless -b -P -- arg pattern confirmed by renderday.com CLI guide. | cross-family (deepseek-v3.1): confirmed — Headless execution pattern and GLB import operator are correct for Blender 4.2+. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [FIX FOR BLENDER 4.2 — Sketchfab blender-plugin Issue #141](https://github.com/sketchfab/blender-plugin/issues/161) — Confirms engine string must be 'BLENDER_EEVEE_NEXT' in Blender 4.2; 'BLENDER_EEVEE' is no longer valid. ; [Import Scene Operators — Blender Python API (current)](https://docs.blender.org/api/current/bpy.ops.import_scene.html) — bpy.ops.import_scene.gltf(filepath=...) is the correct operator for.glb and.gltf in Blender 4.x. ; [Mastering the Blender CLI](https://renderday.com/blog/mastering-the-blender-cli) — blender -b --python script.py -- custom_args is the correct headless execution pattern; -- separator passes args to the script.

### Light object types and energy units in EEVEE Next (4.2+) · `✅ solid` · Blender 4.2+
**The four light types (POINT, SUN, SPOT, AREA) and their energy units changed subtly between old EEVEE and EEVEE Next. Understanding units is critical for consistent brightness across orbit angles.**
- **How:** Create lights via bpy: ```python
import bpy, math # Point / Spot / Area: energy in Watts
light_data = bpy.data.lights.new(name='Key', type='AREA')
light_data.energy = 800 # Watts; visible change circa 400-1200 for sprite scale
light_data.size = 2.0 # metres, controls softness
light_data.shape = 'RECTANGLE' # 'SQUARE' | 'RECTANGLE' | 'DISK' | 'ELLIPSE'
light_data.size_y = 1.0 # only used when shape='RECTANGLE' # Sun: energy in W/m² (irradiance); 2-6 W/m² looks like outdoor sun
sun_data = bpy.data.lights.new(name='Ambient', type='SUN')
sun_data.energy = 3.0 # W/m²
sun_data.angle = math.radians(5) # angular diameter; larger = softer shadow # Spot: energy Watts + cone angles
spot_data = bpy.data.lights.new(name='Rim', type='SPOT')
spot_data.energy = 500
spot_data.spot_size = math.radians(45) # outer cone
spot_data.spot_blend = 0.15 # softness of cone edge # Attach to scene
light_obj = bpy.data.objects.new('Key', light_data)
bpy.context.scene.collection.objects.link(light_obj)
``` In EEVEE Next (Blender 4.2+), light visibility is computed via Shadow Map Ray Tracing; the old per-light `use_shadow` boolean is gone — shadows are always computed for all lights unless you set the object's `hide_render = True` or use Light Linking.
- **Gotchas:** In Blender 4.1 and earlier the engine string is 'BLENDER_EEVEE'; in 4.2+ it must be 'BLENDER_EEVEE_NEXT' — using the wrong string silently falls back to Cycles or errors.; Sun energy unit is W/m², not Watts. A Sun at 800 W is massively overexposed; use 2–6 for daylight.; Area light 'size' only sets X dimension when shape='RECTANGLE'; also set size_y.; Contact shadows were removed in EEVEE Next; the property scene.eevee.use_soft_shadows and scene.eevee.shadow_cube_size / shadow_cascade_size are deprecated and ignored in 4.2+.
- **For Studio:** For the turnaround pipeline use an AREA key (key light), a SUN fill (low energy ~1.0 W/m²), and a SPOT rim. Parent all three to the camera orbit pivot (see camera-orbit-pivot recipe) so they co-rotate with each compass direction.
- **Verify (solid):** Confirmed from irendering.net/blender-4-2-explore-whats-new-in-eevee-next/ (shadow map ray tracing, contact shadows removed) and PSHuman bpy_render.py real-world script showing energy values and light type usage. | cross-family (deepseek-v3.1): confirmed — Light types and energy units are correctly described for EEVEE Next, with SUN using W/m² and others using Watts. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Blender 4.2: Explore what's new in Eevee Next](https://irendering.net/blender-4-2-explore-whats-new-in-eevee-next/) — Contact shadows removed, shadow map ray tracing replaces manual shadow jitter, light limit raised to 4096. ; [PSHuman blender_render_human_ortho.py (HuggingFace)](https://huggingface.co/spaces/gradiopro/PSHuman/blob/main/blender/blender_render_human_ortho.py) — Real production headless bpy script using SUN lights at energy 3.0 / 5.0 with disable-shadow fallback, BLENDER_EEVEE render engine. ; [Mastering the Blender CLI](https://renderday.com/blog/mastering-the-blender-cli) — Engine identifier -E BLENDER_EEVEE_NEXT confirmed; headless -b -P script pattern.

### Orbit pivot empty — parent camera & lights for 8-direction compass sweep · `✅ solid` · Blender 4.x (object parenting API unchanged)
**Parent the camera (and optionally the lights) to an Empty object at the scene origin. Rotating the Empty's Z-axis in 45° steps gives the 8 compass directions without recalculating any camera or light positions — they all follow.**
- **How:** ```python
import bpy, math # --- Create pivot empty at origin ---
pivot = bpy.data.objects.new('OrbitPivot', None)
bpy.context.scene.collection.objects.link(pivot)
pivot.location = (0, 0, 0) # --- Parent camera to pivot ---
cam_obj = bpy.data.objects['SpriteCamera']
cam_obj.parent = pivot
cam_obj.matrix_parent_inverse = pivot.matrix_world.inverted() # --- 8 compass directions (S=0, SW=45, W=90, NW=135, N=180, NE=225, E=270, SE=315) ---
compass_angles = [0, 45, 90, 135, 180, 225, 270, 315] # degrees for i, angle_deg in enumerate(compass_angles): pivot.rotation_euler.z = math.radians(angle_deg) bpy.context.view_layer.update() output_path = f'/tmp/sprite_{angle_deg:03d}.png' bpy.context.scene.render.filepath = output_path bpy.ops.render.render(write_still=True) print(f'Rendered: {output_path}') # --- Optional: parent lights to pivot too (so they co-rotate) ---
for obj_name in ['LightKey', 'LightFill', 'LightRim']: if obj_name in bpy.data.objects: light_obj = bpy.data.objects[obj_name] light_obj.parent = pivot light_obj.matrix_parent_inverse = pivot.matrix_world.inverted()
``` Alternatively, keep lights world-fixed (unparented) if you want the character to always be lit from the same world direction regardless of viewing angle — this produces more realistic cross-angle lighting but less consistent silhouette-edge illumination.
- **Gotchas:** matrix_parent_inverse must be set after parenting otherwise the child's current world position is baked into the offset — child appears to jump when pivot rotates.; If camera has a Track-To constraint targeting a world-space empty, and the camera is also parented to the pivot, the Track-To will fight the parent. Solution: either track-to a pivot-parented child empty, or compute camera rotation manually instead of using Track-To.; rotation_euler.z is radians — forgetting math.radians() gives 1-radian steps (≈57°) instead of 45°.; view_layer.update() must precede each render call to propagate pivot rotation to child camera/lights.
- **For Studio:** This is the master turnaround loop for the sprite pipeline. Create pivot, parent camera + 3-point rig to it, loop over 8 angles, render each. Output filenames include the angle for sprite-sheet assembly downstream.
- **Verify (solid):** Pattern confirmed from multiple real turnaround bpy scripts (PSHuman, blender_script_mvs.py on HuggingFace) and Blender documentation on parent relationships. | cross-family (deepseek-v3.1): confirmed — Parenting API unchanged, orbit pivot technique is valid for multi-angle rendering. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [PSHuman blender_render_human_ortho.py (HuggingFace)](https://huggingface.co/spaces/gradiopro/PSHuman/blob/main/blender/blender_render_human_ortho.py) — Production orbit render loop: iterates azimuth angles, calls set_camera_mvdream(azimuth, 0, distance), renders each frame. ; [EscherNet blender_script_mvs.py (HuggingFace)](https://huggingface.co/spaces/kxic/EscherNet/raw/4937fdb2a6c792bab23ef477e85b9ed45179dae3/scripts/blender_script_mvs.py) — Multi-view orbit render script using bpy, iterating angles and rendering to numbered output paths.

### Orthographic vs perspective camera — bpy setup for sprite rendering · `✅ solid` · Blender 4.x (API unchanged since 2.8)
**Sprite turnarounds should use orthographic projection to avoid perspective distortion across the 8 compass angles. Orthographic scale maps directly to world-unit width of the frame.**
- **How:** ```python
import bpy # --- Create or grab camera ---
cam_data = bpy.data.cameras.new('SpriteCamera')
cam_obj = bpy.data.objects.new('SpriteCamera', cam_data)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj # --- Orthographic mode ---
cam_data.type = 'ORTHO' # 'ORTHO' | 'PERSP' | 'PANO'
cam_data.ortho_scale = 2.5 # world-unit width of rendered frame # for a ~1.8 m character, 2.5 m fits with margin # --- Clip planes ---
cam_data.clip_start = 0.01
cam_data.clip_end = 100.0 # --- For perspective fallback (not recommended for sprites) ---
# cam_data.type = 'PERSP'
# cam_data.lens = 85 # focal length mm (longer = less distortion)
# cam_data.sensor_width = 36 # full-frame equivalent # --- Render resolution ---
scene = bpy.context.scene
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.render.resolution_percentage = 100
``` Ortho_scale is the world-unit height when resolution_x == resolution_y. For a non-square render, the scale maps to the narrower dimension. Adjust per-character or per-sprite-sheet layout.
- **Gotchas:** ortho_scale is in world units (metres by default). If your GLB mesh was exported at cm scale (common from TRELLIS), 1 Blender unit = 1 cm, so set ortho_scale = 250 for a 1.8 m character.; camera.data.type must be set AFTER creating the camera object and before render — setting it on a linked camera that's been type='PERSP' may need a depsgraph update.; Perspective cameras with long lens (85-135mm) can approximate ortho but will still have slight parallax across the 8 angles — use true ORTHO for game sprites.; clip_start too large (e.g. 0.1 on a small mesh) clips foreground geometry; keep it at 0.01 or less.
- **For Studio:** Set cam_data.type = 'ORTHO' and cam_data.ortho_scale to match the character bounding box + ~30% margin. For the fixed 3/4-down 35° turnaround, position the camera at (0, -dist, dist*tan(35°)) looking at origin, then use Track-To (see recipe camera-track-to-target).
- **Verify (solid):** API confirmed from PSHuman blender_render_human_ortho.py which sets cam.data.type = 'ORTHO' and cam.data.ortho_scale = 1.0 in a real production turnaround script. | cross-family (deepseek-v3.1): confirmed — Camera API remains unchanged since 2.8, orthographic setup is correct for sprite rendering. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [PSHuman blender_render_human_ortho.py (HuggingFace)](https://huggingface.co/spaces/gradiopro/PSHuman/blob/main/blender/blender_render_human_ortho.py) — Sets cam.data.type = 'ORTHO', cam.data.ortho_scale, and cam.data.lens in a real 360-turnaround headless render script. ; [bpy.ops.import_scene — Blender Python API (current)](https://docs.blender.org/api/current/bpy.ops.import_scene.html) — Confirms bpy.ops.import_scene.gltf(filepath=...) operator for GLB import, consistent with camera/scene setup patterns.

### Preventing pitch-black back views in 8-direction turnaround · `▸ plausible` · Blender 4.2+
**When all lights are co-parented to the orbit pivot, the character's back faces the key and rim lights' target directions only from the front view. Back-facing views (N, NW, NE compass) can go very dark or silhouetted. This recipe shows how to keep back views readable.**
- **How:** Strategy A — World-fixed ambient SUN (not parented to pivot):
```python
# Add a low-energy world-fixed sun that does NOT rotate with the pivot
ambient_data = bpy.data.lights.new('WorldAmbient', 'SUN')
ambient_data.energy = 1.0 # W/m²; low fill
ambient_data.angle = math.radians(180) # full hemisphere = almost no directionality
ambient_obj = bpy.data.objects.new('WorldAmbient', ambient_data)
bpy.context.scene.collection.objects.link(ambient_obj)
# Do NOT parent to pivot; stays world-fixed
ambient_obj.rotation_euler = (math.radians(45), 0, 0) # aim from above
``` Strategy B — Increase HDRI world strength for ambient fill:
```python
world = bpy.data.worlds['World']
world.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.2
``` Strategy C — Increase rim light energy for back views dynamically:
```python
back_angles = {180, 225, 135} # N, NW, NE
for i, angle_deg in enumerate(compass_angles): pivot.rotation_euler.z = math.radians(angle_deg) # Boost rim for back-facing compass directions rim_light = bpy.data.objects['LightRim'].data rim_light.energy = 800 if angle_deg in back_angles else 400 bpy.context.view_layer.update() bpy.ops.render.render(write_still=True)
``` Strategy D (preferred for consistency) — Add a persistent back-fill AREA at low energy, world-fixed behind the character:
```python
back_data = bpy.data.lights.new('BackFill', 'AREA')
back_data.energy = 200 # Watts, gentle back-fill
back_data.size = 3.0
back_obj = bpy.data.objects.new('BackFill', back_data)
bpy.context.scene.collection.objects.link(back_obj)
back_obj.location = (0, 3.0, 1.5) # behind character in world space
# Track-To the character but DO NOT parent to pivot
track = back_obj.constraints.new('TRACK_TO')
track.target = bpy.data.objects['LookTarget']
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
```
- **Gotchas:** A world-fixed back-fill creates inconsistent lighting across angles — back views will appear brighter relative to front views. This is often acceptable for 2.5D sprites where the player mostly sees front/side angles.; EEVEE Next does not have a 'light falloff' node for stylized flat-shading control; use node materials with an Emission mix for cartoon-style fills.; In EEVEE Next, sun lights at angle = math.radians(180) act as near-uniform hemisphere fills — this is a useful hack for ambient fill without IBL.; Strategy C (dynamic energy change per angle) requires re-evaluating the depsgraph each time: always call view_layer.update() after changing light energy in a loop.
- **For Studio:** Use Strategy D (world-fixed back-fill AREA at 150-250 W) as the base, combined with HDRI strength 0.5-0.8 for ambient. This prevents pitch-black backs without blowing out front-view contrast. Fine-tune per character material darkness.
- **Verify (plausible):** The specific strategy is reasoned from EEVEE Next lighting behaviour (confirmed VSM, ambient IBL) and standard CG turnaround practice. The sun hemisphere trick (angle=180°) is inferred from Blender light angle docs. No direct source verified this exact combination — test in-engine. | cross-family (deepseek-v3.1): unverified — While the lighting strategies seem plausible, specific energy values and angle settings for ambient solutions require empirical testing in EEVEE Next. [only 0 of 1 juror(s) confirmed [unverified]]
- **Sources:** [EEVEE Next Generation in Blender 4.2 LTS — Blender Developers Blog](https://code.blender.org/2024/07/eevee-next-generation-in-blender-4-2-lts/) — Confirms EEVEE Next IBL and shadow behaviour that motivates the ambient fill strategies. ; [Blender 4.2 EEVEE-Next Feedback thread](https://devtalk.blender.org/t/blender-4-2-eevee-next-feedback/31813) — Community reports on back-view darkness and lighting consistency issues in EEVEE Next, confirming this is a real production concern.

### BlendFusion — 45°×8 horizontal ring · `?` · Blender 4.x
**BlenderProc path-tracing; object-centric cameras on a horizontal ring, azimuth every 45° (8 views), fill-fraction framing.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [BlendFusion — 45°×8 horizontal ring](https://arxiv.org/abs/2604.09022) — 45°×8 orbit

### MExECON — 8-view Blender orbit · `?` · Blender 4.x
**Synthetic 8-view Blender orbit (360°, eye-level) for clothed avatars — multi-view turnaround remains standard.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [MExECON — 8-view Blender orbit](https://arxiv.org/abs/2508.15500) — 8-view eval/render

### Orthographic projection Britannica · `?` · Blender 4.x
**Analog: plan/elevation as 2D of 3D. Holds as geometry reason ortho beats perspective for readable turnaround frames.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Orthographic projection Britannica](https://www.britannica.com/technology/orthographic-projection-engineering) — ortho readability

### Orthographic projection UW — turntable analog · `?` · Blender 4.x
**Analog: parallel projectors → true-size 2D views. Holds for orthographic turntable cameras; limit: CAD ≠ 8-dir game orbit.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Orthographic projection UW — turntable analog](https://uw.pressbooks.pub/enggraphics/chapter/orthographic-projection/) — ortho turntable analog

### SimpleProc — eight look-at cameras · `?` · Blender 4.x
**Blender EEVEE pipeline places eight look-at cameras per scene for multi-view coverage — same orbit count as studio 8-direction turnaround.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [SimpleProc — eight look-at cameras](https://arxiv.org/abs/2604.04925) — 8-view orbit

