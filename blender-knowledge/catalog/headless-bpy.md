# Headless rendering & bpy scripting
_blender --background --python, the bpy API (ops/data/context), CLI render flags, reproducible scene setup, installing python modules, 3.x->4.x API changes — how the studio's turnaround rig actually runs._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

79 recipes · 21 solid.

| Recipe | Blender | Currency | ✓ | What |
|--------|-------|----------|---|------|
| A Scalable Pipeline Combining Procedural 3D Graphics and Guided Diffusion… | 4.5 LTS | ✅ solid | · | Blender remains the geometry/render backend in hybrid farms. |
| Blendify — Python rendering framework for Blender | 4.5 LTS | ✅ solid | · | Lightweight Python high-level API over Blender for scene creation and ray-traced |
| Detect Blender version in script with bpy.app.version | 4.x | ✅ solid | ✓ | Branch script behavior by Blender version to handle 3.x vs 4.x API differences s |
| Enable GPU rendering for Cycles in a headless script | 4.x | ✅ solid | ✓ | Configure Cycles to use NVIDIA OptiX (or CUDA) GPU from inside a background Pyth |
| Import a GLB/glTF mesh in a headless script | 4.x | ✅ solid | ✓ | Load a TRELLIS-generated GLB file into Blender's scene from a Python script runn |
| Kubric — scalable Blender/Cycles dataset generator | 4.5 LTS | ✅ solid | · | Parallel Blender/Cycles dataset farm; cites bpy install/version variation pain. |
| MAPS — Blender on-demand camera/lighting farm | 4.5 LTS | ✅ solid | · | Blender-based rendering under continuous camera/lighting/background factors. |
| Perret-Gentil EEVEE Docker GPU / EGL notes | 4.5 LTS | ✅ solid | · | EEVEE headless needs EGL/ICD; bare Docker fails. |
| Render and save a frame from a Python script | 4.x | ✅ solid | ✓ | Trigger a single-frame render and write the output image to disk from inside a h |
| RenderSettings.engine / film_transparent (API 4.5) | 4.5 LTS | ✅ solid | · | Default engine BLENDER_EEVEE_NEXT; film_transparent for alpha sheets. |
| Run a Python script headlessly via CLI | 4.x | ✅ solid | ✓ | Launch Blender with no GUI, execute a Python script, and pass custom arguments a |
| ScratchSim — BlenderProc synthetic scratch pipeline | 4.5 LTS | ✅ solid | · | Large-scale annotated synthetic data via BlenderProc with camera modes + domain  |
| Set EEVEE Next as render engine in Blender 4.2+ | 4.2+ | ✅ solid | ✓ | Select the correct render engine identifier string for EEVEE in Blender 4.2+; th |
| SpatialEdit — Blender camera-trajectory batch render | 4.5 LTS | ✅ solid | · | Controllable Blender pipeline with systematic camera trajectories for SpatialEdi |
| Start from an empty scene with wm.read_factory_settings | 4.x | ✅ solid | ✓ | Reset the bpy context to a truly empty scene inside a headless script, discardin |
| SynSacc: A Blender-to-V2E Pipeline for Synthetic Neuromorphic Eye-Movement Data | 4.5 LTS | ✅ solid | · | shows Blender as the first stage of multi-stage offline farm pipelines. |
| T85546 — Grease Pencil headless abort | 4.5 LTS | ✅ solid | · | GP stroke objects requiring OpenGL/display abort blender -b. |
| Tips and Tricks — no UI / background python (API 4.5) | 4.5 LTS | ✅ solid | · | Documented farm pattern blender --background --python. |
| Visual Deformation Detection Using Soft Material Simulation for Pre-training… | 4.5 LTS | ✅ solid | · | scripted bpy batch viewpoints without GUI. |
| bpy.data vs bpy.ops vs bpy.context access patterns | 4.x | ✅ solid | ✓ | Know when to use each bpy namespace: direct datablock access (bpy.data), operato |
| bpy.ops.render — write_still (API 4.5) | 4.5 LTS | ✅ solid | · | render() with write_still saves to scene render filepath. |
| Command-line render (Manual latest) — claim holds | 4.5 LTS | ▸ plausible | · | -b background render without graphical display. |
| Install Python packages into Blender's bundled Python | 4.2+ | ▸ plausible | ✓ | Add third-party pip packages (e.g. numpy, trimesh) to Blender's internal Python  |
| 3DCodeBench: Benchmarking Agentic Procedural 3D Modeling Via Code | 4.x pin (not silent 5.0) | ⚠ shaky | · | Instantiates the operator on **Blender 5.0**; failures mostly from API mismatche |
| APOLLO Blender: A Robotics Library for Visualization and Animation in Blender | 4.x pin (still-current) | ⚠ shaky | · | APOLLO Blender robotics viz/animation library — UNVERIFIED claim mismatch on sti |
| Bioinspired123D: Generative 3D Modeling System for Bioinspired Structures | 4.x pin (not silent 5.0) | ⚠ shaky | · | Dataset/validation runs **Blender 4.2 LTS** with bpy; render engine **Eevee Next |
| Blender 4.5 CLI arguments | 4.x pin (still-current) | ⚠ shaky | · | CLI -b/-P/--python-expr on 4.5 — headless knobs for pinned farm; silent 4→5: 0. |
| Blender 4.5 CLI render | 4.x pin (still-current) | ⚠ shaky | · | CLI render order on 4.5 — left-to-right; -f/-a last; dated currency for pin-4.x. |
| Blender 4.5 LTS product | 4.x pin (not silent 5.0) | ⚠ shaky | · | 4.5 LTS: ~2 years updates (to Jul 2027 per dev notes), full Vulkan support. Posi |
| Blender 4.5 LTS product (analog) | 4.x pin (still-current) | ⚠ shaky | · | Analog 4.5-product LTS pin; Hold dated still-current 4.x. Limit: product page no |
| Blender 4.5 LTS product page | 4.x pin (still-current) | ⚠ shaky | · | 4.5 LTS product notes — long-support pin; contrast 5.2 current stable naming. |
| Blender 4.5 Manual | 4.x pin (still-current) | ⚠ shaky | · | Manual 4.5 — dated docs currency for pinned 4.x farm; 5.2 named current stable e |
| Blender 4.5 Release Notes (dev) | 4.x pin (still-current) | ⚠ shaky | · | 4.5 LTS release notes — dated 4.5 currency; not a silent jump to 5.x. |
| Blender 5.0 Core | 4.x pin (not silent 5.0) | ⚠ shaky | · | Unified logger; background render progress format changed. Replacements on page: |
| Blender 5.0 EEVEE & Viewport | 4.x pin (not silent 5.0) | ⚠ shaky | · | Breaking: Light Probe Volume backface meaning fix; View Layer Overrides change o |
| Blender 5.0 Release Notes | 4.x pin (not silent 5.0) | ⚠ shaky | · | Analog (currency): major 5.0 with Compatibility section / listed breaks. Holds:  |
| Blender 5.0 Release Notes (breaks) | 4.x pin (still-current) | ⚠ shaky | · | Analog 5.0 listed Compatibility breaks; Hold treat as major migrate not patch. L |
| Blender 5.0 Release Notes (dev) | 4.x pin (not silent 5.0) | ⚠ shaky | · | Major release with listed Compatibility breaks (name length 255, big-endian gone |
| Blender 5.0 product notes | 4.x pin (not silent 5.0) | ⚠ shaky | · | Recaps color-management/HDR/wide-gamut overhaul (ACES views, Working Color Space |
| Blender LTS downloads | 4.x pin (still-current) | ⚠ shaky | · | LTS download page — production pin target; 4.5 LTS line for still-current farms. |
| Blender Python API 4.5 | 4.x pin (still-current) | ⚠ shaky | · | bpy API 4.5 — headless script surface for pin-4.x; do not float to 5.x silently. |
| Blender Release Notes index | 4.x pin (still-current) | ⚠ shaky | · | Dev release-notes index — dated currency surface for major/minor lines; pin 4.x  |
| BlenderRAG: High-Fidelity 3D Object Generation via Retrieval-Augmented Code Synthesis | 4.x pin (still-current) | ⚠ shaky | · | BlenderRAG RAG over curated Blender code examples raises compile success — code- |
| Blendify -- Python rendering framework for Blender | 4.x pin (still-current) | ⚠ shaky | · | Blendify: lightweight Python framework over Blender bpy for scene creation/rende |
| CLI-Anything: Towards Agent-Native Computer Use | 4.x pin (not silent 5.0) | ⚠ shaky | · | Headless Blender binary runs generated bpy render scripts; EEVEE path is version |
| Calendar Versioning (CalVer) | 4.x pin (still-current) | ⚠ shaky | · | Analog CalVer date-stamped currency; Hold still-current-as-of labels. Limit: sta |
| Command Line Arguments | 4.x pin (not silent 5.0) | ⚠ shaky | · | Headless knobs on page: `-b`/`--background`, `-P`/`--python`, `--python-expr`, ` |
| Command Line Arguments | 4.x pin (not silent 5.0) | ⚠ shaky | · | Same stay: `-b`, `-P`, `--python-expr`, `--factory-startup`, `--`, `--cycles-dev |
| Dockerfile `FROM` image@digest | 4.x pin (not silent 5.0) | ⚠ shaky | · | Analog: pin by digest (immutable) rather than a floating tag. Holds for farm ima |
| EZBlender: Efficient 3D Editing with Plan-and-ReAct Agent | 4.x pin (still-current) | ⚠ shaky | · | EZBlender Plan-and-ReAct Blender editing agent — agentic bpy deepen; pin 4.x; si |
| From Idea to Co-Creation: A Planner–Actor–Critic Framework for Agent Augmented 3D Modeling | 4.x pin (not silent 5.0) | ⚠ shaky | · | Agents emit executable Blender Python (`import bpy` / `bpy.ops`) via Blender-MCP |
| How to port Python 2 Code to Python 3 | 4.x pin (not silent 5.0) | ⚠ shaky | · | Analog: Python 2 EOL → deliberate port, not a quiet upgrade. Holds for treating  |
| MeshCoder: LLM-Powered Structured Mesh Code Generation from Point Clouds | 4.x pin (still-current) | ⚠ shaky | · | MeshCoder reconstructs point clouds into editable Blender Python scripts — mesh- |
| Nimbus: A Unified Embodied Synthetic Data Generation Framework | 4.x pin (not silent 5.0) | ⚠ shaky | · | Blender backend uses OptiX RT/Tensor cores and **multi-process workers** to bypa |
| Node.js Releases (Current → Active LTS) | 4.x pin (not silent 5.0) | ⚠ shaky | · | Analog: production pins Active LTS; Current is for library prep. Holds for pinni |
| Node.js previous releases (LTS) | 4.x pin (still-current) | ⚠ shaky | · | Analog Active LTS vs Current; Hold pin Blender 4.x LTS for production farms. Lim |
| Nova3D: Code-Native Generation of Programmable 3D Assets | 4.x pin (not silent 5.0) | ⚠ shaky | · | Asset = executable Blender Python; compiled via **headless Blender** determinist |
| ProcFunc: Function-Oriented Abstractions for Procedural 3D Generation in Python | 4.x pin (not silent 5.0) | ⚠ shaky | · | Blender-based procedural library with atomic bpy primitives plus an **EEVEE** re |
| Rendering From The Command Line | 4.x pin (not silent 5.0) | ⚠ shaky | · | Args left-to-right; always put `-f` or `-a` last; wrong order silently ignores o |
| SceneCode: Executable World Programs for Editable Indoor Scenes with Articulated Objects | 4.x pin (still-current) | ⚠ shaky | · | SceneCode emits part-wise Blender Python for articulated indoor scenes — executa |
| SceneCraft: An LLM Agent for Synthesizing 3D Scene as Blender Code | 4.x pin (still-current) | ⚠ shaky | · | SceneCraft LLM agent emits Blender-executable Python for complex scenes — bpy co |
| ScratchSim: A Procedural Synthetic Data Pipeline for Surface Scratch Detection | 4.x pin (still-current) | ⚠ shaky | · | ScratchSim BlenderProc procedural synthetic scratch data — farm/proc deepen; pin |
| Semantic Versioning 2.0.0 | 4.x pin (not silent 5.0) | ⚠ shaky | · | Analog: MAJOR = incompatible API changes; PATCH ≠ that. Holds: Blender 5.0 is a  |
| Semantic Versioning 2.0.0 | 4.x pin (still-current) | ⚠ shaky | · | Analog SemVer MAJOR=incompatible; Hold pin+cite; silent 4→5 retarget fails. Limi |
| SimpleProc: Fully Procedural Synthetic Data from Simple Rules for Multi-View Stereo | 4.x pin (not silent 5.0) | ⚠ shaky | · | Blender data-generation pipeline renders with the **EEVEE** engine for multi-vie |
| Unity LTS (Long Term Support) | 4.x pin (not silent 5.0) | ⚠ shaky | · | Analog: production locks an LTS line for stability. Holds for blender-knowledge  |
| Upgrading from Godot 3 to Godot 4 | 4.x pin (not silent 5.0) | ⚠ shaky | · | Analog: major engine jump needs converter + breaking renames; formats not silent |
| Upgrading from Godot 3 to Godot 4 | 4.x pin (still-current) | ⚠ shaky | · | Analog major engine migrate needs deliberate port; Hold for Blender 4→5. Limit:  |
| kajiyama blender-eevee-gpu-headless — 404 | 4.5 LTS | ✗ wrong | · | Cited EEVEE GPU headless repo. |
| Arnold kick — headless CLI analog | 4.x |  | · | Analog: headless CLI renderer (kick -dw -i … -o …). Holds for blender --backgrou |
| Bioinspired123D — Blender 4.2 LTS + EEVEE Next headless | 4.2 LTS |  | · | Dataset/validation runs Blender 4.2 LTS headless with EEVEE Next, fixed TRACK_TO |
| Blender 4.5 LTS CLI arguments — -b/-P | 4.5 LTS |  | · | Documents -b/--background, -P/--python, --python-expr, --factory-startup, and -- |
| Blender 4.5 LTS CLI render order | 4.5 LTS |  | · | Args execute left-to-right; put -o/-F before -f/-a (always last) — wrong order s |
| Blender 5.0 CLI arguments — -b/-P remain (compat note) | 4.x |  | · | Same headless knobs (-b, -P, --) remain; logging options rewritten — farm parser |
| CLI-Anything — headless bpy EEVEE_NEXT tolerance | 4.x |  | · | Headless Blender via bpy + blender --background; EEVEE path is version-tolerant  |
| Maya CLI render — DCC batch analog | 4.x |  | · | Analog: DCC batch override flags from shell. Holds for reproducible headless spr |
| Nimbus — OptiX multi-process Blender batch | 4.x |  | · | Blender backend: OptiX RT/Tensor cores + multi-process workers to bypass the Pyt |
| Nova3D — code-native Blender Python → GLB headless | 4.x |  | · | Asset = executable Blender Python; GLB is the compiled artifact via headless Ble |
| ProcFunc — bpy primitives + EEVEE interface (Cycles half omitted) | 4.x |  | · | Atomic bpy primitives + EEVEE render interface for procedural rooms/datasets — s |

## Detail

### A Scalable Pipeline Combining Procedural 3D Graphics and Guided Diffusion… · `✅ solid` · Blender 4.5 LTS
**Blender remains the geometry/render backend in hybrid farms.**
- **How:** Pin 4.x camera/farm craft; no 5.x invent.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [A Scalable Pipeline Combining Procedural 3D Graphics and Guided Diffusion…](https://arxiv.org/abs/2512.08747) — A Scalable Pipeline Combining Procedural 3D Graphics and Guided Diffusion…

### Blendify — Python rendering framework for Blender · `✅ solid` · Blender 4.5 LTS
**Lightweight Python high-level API over Blender for scene creation and ray-traced rendering.**
- **How:** Reduces bpy friction for automated CV/CG batch renders.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Blendify — Python rendering framework for Blender](https://arxiv.org/abs/2410.17858) — Blendify headless API

### Detect Blender version in script with bpy.app.version · `✅ solid` · Blender 4.x
**Branch script behavior by Blender version to handle 3.x vs 4.x API differences safely.**
- **How:** import bpy
# bpy.app.version is a tuple of ints: (major, minor, patch)
blender_ver = bpy.app.version # e.g. (4, 2, 0)
if blender_ver >= (4, 2, 0): bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
else: bpy.context.scene.render.engine = 'BLENDER_EEVEE' # bpy.app.version_string is a human-readable string: '4.2.0'
print(f'Running Blender {bpy.app.version_string}') # DEPRECATED and REMOVED in 4.3: bpy.app.version_char
# Do NOT use bpy.app.version_char — it no longer exists in 4.3+
- **Gotchas:** bpy.app.version_char was deprecated in Blender 4.0 and fully removed in 4.3.2. Any script using it will throw AttributeError on Blender 4.3+. bpy.data.version differs from bpy.app.version — it returns the version the currently open.blend file was saved with, not the running Blender version. Always use bpy.app.version for runtime version gating.
- **For Studio:** Guard BLENDER_EEVEE_NEXT vs BLENDER_EEVEE string, material API differences, and any other 3.x→4.x branches in shared pipeline scripts.
- **Verify (solid):** bpy.app.version as int-tuple confirmed via blenderartists.org discussion on bpy.data.version confusion (fetched via search). version_char removal in 4.3 confirmed via Adobe community/Mixamo forum reports (search result). | cross-family (deepseek-v3.1): confirmed — Accurate version detection using bpy.app.version tuple and warning about deprecated version_char. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [How to get current Blender version number through the Python API (b3d.interplanety.org)](https://b3d.interplanety.org/en/how-to-get-current-blender-version-number-through-the-python-api/) — bpy.app.version returns a tuple (major, minor, patch); bpy.app.version_string returns human-readable string ; [Blender Plugin — version_char deprecated (Adobe/Mixamo community)](https://community.adobe.com/t5/mixamo-discussions/blender-plugin-not-working-due-to-deprecated-bpy-app-version-char-attribute-in-blender-api/td-p/15196754) — bpy.app.version_char is deprecated since 4.0 and removed in 4.3.2; scripts must migrate to bpy.app.version tuple

### Enable GPU rendering for Cycles in a headless script · `✅ solid` · Blender 4.x
**Configure Cycles to use NVIDIA OptiX (or CUDA) GPU from inside a background Python script — not from the UI.**
- **How:** import bpy
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'GPU' cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
cycles_prefs.get_devices() # must call first to populate device list
cycles_prefs.compute_device_type = 'OPTIX' # or 'CUDA', 'HIP', 'METAL' for device in cycles_prefs.devices: device.use = (device.type == 'OPTIX') # enable only OptiX, disable CPU # Alternative: pass --cycles-device on the CLI instead of scripting prefs:
# blender -b scene.blend -E CYCLES -P script.py -- --cycles-device OPTIX
# The CLI flag sets the device without needing the prefs block above.
- **Gotchas:** get_devices() MUST be called before accessing cycles_prefs.devices — the list is empty without it. In a fresh headless session the Cycles preferences may not persist from the user's prefs (use --factory-startup to ensure clean state). If running on a machine without an NVIDIA GPU, setting OPTIX will silently fall back to CPU — check device.type after get_devices(). The CLI --cycles-device flag (e.g. -- --cycles-device OPTIX) is cleaner for CI/render farm use as it avoids preferences state. For EEVEE Next GPU rendering no equivalent scripted GPU selection is needed — it uses the system GPU automatically.
- **For Studio:** If the turnaround pipeline switches to Cycles for PBR-accurate sprites, this enables the RTX 5090 via OptiX in headless mode. EEVEE Next (the default) doesn't need this block.
- **Verify (solid):** Pattern confirmed via MotionGPT/HuggingFace scene.py (fetched): exact prefs path and get_devices() call. Devtalk.blender.org thread on single-GPU OPTIX confirmed the same API. CLI --cycles-device OPTIX confirmed in renderday.com guide (fetched). | cross-family (deepseek-v3.1): confirmed — Correct device configuration through preferences.addons['cycles'] and CLI flag alternative. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [MotionGPT Blender scene.py — GPU Cycles setup](https://huggingface.co/spaces/fjibj/MotionGPT/blob/b625c801edd539dec9915d7fb48d54565ea566dc/mGPT/render/blender/scene.py) — bpy.context.preferences.addons['cycles'].preferences.get_devices() + compute_device_type + device.use pattern for headless GPU Cycles ; [Mastering the Blender CLI (renderday.com, Blender 4.4)](https://renderday.com/blog/mastering-the-blender-cli) — blender -b scene.blend -E CYCLES -- --cycles-device OPTIX as a clean CLI-level GPU selector

### Import a GLB/glTF mesh in a headless script · `✅ solid` · Blender 4.x
**Load a TRELLIS-generated GLB file into Blender's scene from a Python script running headlessly.**
- **How:** import bpy
# Clear default scene first
bpy.ops.wm.read_factory_settings(use_empty=True)
# Import GLB
bpy.ops.import_scene.gltf( filepath='/abs/path/to/model.glb', merge_vertices=False # optional; default False
)
# Imported objects are now selected; get them:
imported_objects = [o for o in bpy.context.selected_objects]
# Center geometry (optional)
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
# The operator name is import_scene.gltf in Blender 4.x (unchanged from 3.x)
- **Gotchas:** import_scene.gltf requires Blender's built-in glTF add-on, which is enabled by default in standard Blender installs. In Docker/minimal installs it may need enabling: bpy.ops.preferences.addon_enable(module='io_scene_gltf2'). After import, all imported objects are selected — iterate bpy.context.selected_objects to get the mesh roots. Filepath must be absolute in headless mode.
- **For Studio:** First step of the turnaround pipeline: import TRELLIS GLB output, orient and center the mesh, then set up camera orbit for 8-direction sprite renders.
- **Verify (solid):** Operator name confirmed via docs.blender.org/api/current/bpy.ops.import_scene.html (attempted fetch; 403 blocked, but operator name consistent across search results citing 'bpy.ops.import_scene.gltf' in Blender 4.x context including --python-expr example in search result). Confirmed stable since 2.8 with no rename in 4.x notes. | cross-family (deepseek-v3.1): confirmed — Correct bpy.ops.import_scene.gltf operator usage for Blender 4.x headless GLB import. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Import Scene Operators — Blender Python API (current)](https://docs.blender.org/api/current/bpy.ops.import_scene.html) — bpy.ops.import_scene.gltf is the operator name in current Blender API ; [Blender CLI/Python-expr GLB import example](https://renderday.com/blog/mastering-the-blender-cli) — bpy.ops.import_scene.gltf(filepath='...') used in Blender 4.x headless context

### Kubric — scalable Blender/Cycles dataset generator · `✅ solid` · Blender 4.5 LTS
**Parallel Blender/Cycles dataset farm; cites bpy install/version variation pain.**
- **How:** API-stability / farm-packaging pole for headless bpy.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Kubric — scalable Blender/Cycles dataset generator](https://arxiv.org/abs/2203.03570) — Kubric farm packaging

### MAPS — Blender on-demand camera/lighting farm · `✅ solid` · Blender 4.5 LTS
**Blender-based rendering under continuous camera/lighting/background factors.**
- **How:** Parametric camera farm adjacent to multi-azimuth turnaround.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [MAPS — Blender on-demand camera/lighting farm](https://arxiv.org/abs/2605.20549) — MAPS camera farm

### Perret-Gentil EEVEE Docker GPU / EGL notes · `✅ solid` · Blender 4.5 LTS
**EEVEE headless needs EGL/ICD; bare Docker fails.**
- **How:** ICD required for EEVEE headless.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Perret-Gentil EEVEE Docker GPU / EGL notes](https://c.pgdm.ch/notes/eevee-docker-gpu/) — EEVEE+EGL ICD

### Render and save a frame from a Python script · `✅ solid` · Blender 4.x
**Trigger a single-frame render and write the output image to disk from inside a headless bpy script.**
- **How:** import bpy
scene = bpy.context.scene
# Set output path and format
scene.render.filepath = '/abs/path/to/output/frame_####'
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA' # for transparency
scene.render.resolution_x = 128
scene.render.resolution_y = 128
scene.render.resolution_percentage = 100
# Render current frame and write to disk:
bpy.ops.render.render(write_still=True)
# write_still=True writes the file; without it the render result is in memory only.
# For animation, use animation=True instead:
# bpy.ops.render.render(animation=True)
- **Gotchas:** write_still=True is required to actually write the file; omitting it renders to the Blender internal render buffer only (no file written). filepath must be absolute or use // (relative to blend file location). The #### padding is replaced with the frame number. For the sprite pipeline, prefer absolute paths to avoid ambiguity in headless/no-blend-file mode. If running without a blend file loaded, set scene.frame_current explicitly before calling render.
- **For Studio:** Core output step: each of the 8 rotation angles renders one frame, write_still=True writes the PNG sprite sheet cell.
- **Verify (solid):** Pattern confirmed across multiple headless render examples (HPC Arizona docs fetched, renderday.com guide fetched, MotionGPT scene.py fetched). bpy.ops.render.render(write_still=True) is the canonical call; consistent across 3.x and 4.x. | cross-family (deepseek-v3.1): confirmed — Correct bpy.ops.render.render(write_still=True) pattern for headless rendering in Blender 4.x. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Mastering the Blender CLI (renderday.com, Blender 4.4)](https://renderday.com/blog/mastering-the-blender-cli) — bpy.ops.render.render(write_still=True) confirmed as the standard in-script render-and-save call ; [HPC Arizona — Scaling Up Blender Rendering](https://hpcdocs.hpc.arizona.edu/running_jobs/visualization/blender/scaling_up_blender_rendering/) — Headless single-frame render with -b and -f flags, output path with # padding

### RenderSettings.engine / film_transparent (API 4.5) · `✅ solid` · Blender 4.5 LTS
**Default engine BLENDER_EEVEE_NEXT; film_transparent for alpha sheets.**
- **How:** Alpha sprite sheets need film_transparent on.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [RenderSettings.engine / film_transparent (API 4.5)](https://docs.blender.org/api/4.5/bpy.types.RenderSettings.html) — EEVEE_NEXT + film_transparent

### Run a Python script headlessly via CLI · `✅ solid` · Blender 4.x
**Launch Blender with no GUI, execute a Python script, and pass custom arguments after the -- separator.**
- **How:** blender --background [optional.blend] --python script.py -- --my-arg value
Inside the script, extract custom args: import sys, argparse argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [] parser = argparse.ArgumentParser() parser.add_argument('--my-arg') args = parser.parse_known_args(argv)[0]
Argument ORDER is critical: Blender executes flags left-to-right. Set -o (output path) BEFORE -f (render frame), not after. --python can be given multiple times to chain scripts.
- **Gotchas:** Order matters: blender -b scene.blend -f 1 -o /tmp renders to the blend's baked output path, not /tmp. Correct: blender -b -o /tmp scene.blend -f 1. Arguments after -- are NOT processed by Blender — they land verbatim in sys.argv for the Python script. --python-expr accepts inline Python but is length-limited by shell; prefer --python for anything nontrivial.
- **For Studio:** Entry point for the turnaround pipeline: blender --background --python render_turnaround.py -- --glb model.glb --out sprites/ --angles 8
- **Verify (solid):** Confirmed via renderday.com Blender 4.4 CLI guide (fetched) and b3d.interplanety.org argparse pattern (fetched). Argument-order rule verified in renderday source. | cross-family (deepseek-v3.1): confirmed — Correct CLI syntax with -- separator and argparse pattern for Blender 4.x headless execution. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Mastering the Blender CLI (renderday.com, Blender 4.4)](https://renderday.com/blog/mastering-the-blender-cli) — Exact --background, --python, -f, -o, -- separator syntax with Blender 4.4 examples; argument ordering is critical ; [How to pass command line arguments to a Blender Python script (b3d.interplanety.org)](https://b3d.interplanety.org/en/how-to-pass-command-line-arguments-to-a-blender-python-script-or-add-on/) — sys.argv[sys.argv.index('--') + 1:] pattern with argparse.parse_known_args() for isolating script args from Blender args

### ScratchSim — BlenderProc synthetic scratch pipeline · `✅ solid` · Blender 4.5 LTS
**Large-scale annotated synthetic data via BlenderProc with camera modes + domain randomization.**
- **How:** BlenderProc as modular batch-render pipeline layer.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [ScratchSim — BlenderProc synthetic scratch pipeline](https://arxiv.org/abs/2607.27065) — BlenderProc batch layer

### Set EEVEE Next as render engine in Blender 4.2+ · `✅ solid` · Blender 4.2+
**Select the correct render engine identifier string for EEVEE in Blender 4.2+; the legacy 'BLENDER_EEVEE' string was replaced.**
- **How:** import bpy
# Blender 4.2+ — EEVEE is now EEVEE Next; identifier is BLENDER_EEVEE_NEXT
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
# Verify at runtime:
if bpy.app.version >= (4, 2, 0): bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
else: bpy.context.scene.render.engine = 'BLENDER_EEVEE' # 3.x and below # Confirm available engines (useful for debugging):
import bpy
print([e.bl_idname for e in bpy.types.RenderEngine.__subclasses__()])
# Or simply: blender --background --python-expr "import bpy; print(bpy.context.scene.render.bl_rna.properties['engine'].enum_items.keys())"
- **Gotchas:** CRITICAL: 'BLENDER_EEVEE' is no longer a valid enum in Blender 4.2+. Setting it raises 'enum BLENDER_EEVEE not found in (BLENDER_EEVEE_NEXT, CYCLES, BLENDER_WORKBENCH)'. Old scripts, tutorials, and addons that hardcode 'BLENDER_EEVEE' will fail silently or error. Also in 4.2: bpy.types.Material.blend_method renamed to surface_render_method; show_transparent_back renamed to use_transparency_overlap; use_screen_refraction renamed to use_raytrace_refraction. In 4.3 all EEVEE Legacy compat Python API calls were removed.
- **For Studio:** Turnaround renders use EEVEE Next for speed; the engine-id fix is required when scripts were ported from 3.x or from tutorials written before 4.2.
- **Verify (solid):** Confirmed via Sketchfab blender-plugin issue #176 (fetched): error message explicitly states 'BLENDER_EEVEE not found in (BLENDER_EEVEE_NEXT, CYCLES, BLENDER_WORKBENCH)' in Blender 4.2. Issue #141 (fetched) shows same fix. Blender 4.2 Python API release notes list material property renames. | cross-family (deepseek-v3.1): confirmed — Accurate engine identifier 'BLENDER_EEVEE_NEXT' for Blender 4.2+ with proper version checking. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Sketchfab blender-plugin issue #176 — BLENDER_EEVEE not found](https://github.com/sketchfab/blender-plugin/issues/176) — Error message in Blender 4.2 explicitly states enum 'BLENDER_EEVEE' not found in ('BLENDER_EEVEE_NEXT', 'WORKBENCH', 'CYCLES') ; [Sketchfab blender-plugin issue #141 — FIX FOR BLENDER 4.2](https://github.com/sketchfab/blender-plugin/issues/141) — Changing BLENDER_EEVEE to BLENDER_EEVEE_NEXT fixes compatibility with Blender 4.2 ; [Blender 4.2 LTS: Python API release notes](https://developer.blender.org/docs/release_notes/4.2/python_api/) — Material blend_method → surface_render_method, show_transparent_back → use_transparency_overlap, use_screen_refraction → use_raytrace_refraction

### SpatialEdit — Blender camera-trajectory batch render · `✅ solid` · Blender 4.5 LTS
**Controllable Blender pipeline with systematic camera trajectories for SpatialEdit-500k.**
- **How:** Camera-path batching for viewpoint grids.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [SpatialEdit — Blender camera-trajectory batch render](https://arxiv.org/abs/2604.04911) — SpatialEdit camera trajectories

### Start from an empty scene with wm.read_factory_settings · `✅ solid` · Blender 4.x
**Reset the bpy context to a truly empty scene inside a headless script, discarding the default cube/camera/light and any user startup preferences.**
- **How:** import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
# Scene is now empty — no objects, no world, no camera.
# Proceed to build scene programmatically:
bpy.ops.object.camera_add(location=(0, -5, 2))
cam = bpy.context.object
bpy.context.scene.camera = cam
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
When loading a.blend file explicitly (blender --background myfile.blend --python script.py), the blend loading already provides a scene, so read_factory_settings is only needed when running blender --background --python script.py with no blend file (the default startup.blend would otherwise load).
- **Gotchas:** Without use_empty=True, bpy loads the user's startup.blend (or factory startup), which always includes a default cube, camera, and light. When using the bpy Python module (import bpy in a standalone Python process), the module always initializes with the default startup scene — use_empty=True is mandatory there. Do NOT call bpy.ops.wm.read_homefile() in scripts — it reads the user's personal startup.blend and behavior is unpredictable across machines.
- **For Studio:** Guarantees a reproducible blank canvas for each turnaround render invocation regardless of the Blender install's personal settings on a render farm or CI node.
- **Verify (solid):** Pattern confirmed in bpy module docs (info_advanced_blender_as_bpy, fetched via search result summary) and multiple pipeline examples. use_empty=True documented in Blender developer tracker T47418. | cross-family (deepseek-v3.1): confirmed — Correct use of bpy.ops.wm.read_factory_settings(use_empty=True) for clean slate in headless Blender 4.x. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Blender as a Python Module — bpy advanced docs](https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html) — bpy module loads default startup scene on import; use_empty=True is the correct way to get a blank scene ; [Blender Automation with Python (CodePal/community)](https://codepal.ai/code-fixer/query/6lzZTHGY/blender-automation-python) — wm.read_factory_settings(use_empty=True) as the canonical clean-slate call in headless scripting

### SynSacc: A Blender-to-V2E Pipeline for Synthetic Neuromorphic Eye-Movement Data · `✅ solid` · Blender 4.5 LTS
**shows Blender as the first stage of multi-stage offline farm pipelines.**
- **How:** Pin 4.x camera/farm craft; no 5.x invent.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [SynSacc: A Blender-to-V2E Pipeline for Synthetic Neuromorphic Eye-Movement Data](https://arxiv.org/abs/2602.08726) — SynSacc: A Blender-to-V2E Pipeline for Synthetic Neuromorphic Eye-Movement Data

### T85546 — Grease Pencil headless abort · `✅ solid` · Blender 4.5 LTS
**GP stroke objects requiring OpenGL/display abort blender -b.**
- **How:** Live GP fails headless without bake/pack first.
- **Gotchas:** Pin 4.x. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [T85546 — Grease Pencil headless abort](https://archive.blender.org/developer/maniphest/0085/0085546/index.html) — Live GP headless needs bake

### Tips and Tricks — no UI / background python (API 4.5) · `✅ solid` · Blender 4.5 LTS
**Documented farm pattern blender --background --python.**
- **How:** Matches 8-dir turnaround scripts.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Tips and Tricks — no UI / background python (API 4.5)](https://docs.blender.org/api/4.5/info_tips_and_tricks.html) — background --python

### Visual Deformation Detection Using Soft Material Simulation for Pre-training… · `✅ solid` · Blender 4.5 LTS
**scripted bpy batch viewpoints without GUI.**
- **How:** Pin 4.x camera/farm craft; no 5.x invent.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Visual Deformation Detection Using Soft Material Simulation for Pre-training…](https://arxiv.org/abs/2405.14877) — Visual Deformation Detection Using Soft Material Simulation for Pre-training…

### bpy.data vs bpy.ops vs bpy.context access patterns · `✅ solid` · Blender 4.x
**Know when to use each bpy namespace: direct datablock access (bpy.data), operator invocations (bpy.ops), and active context queries (bpy.context).**
- **How:** import bpy # bpy.data — direct datablock access, no context dependency, always reliable in headless
mesh_obj = bpy.data.objects['MyMesh'] # get by name
for scene in bpy.data.scenes: scene.render.engine = 'BLENDER_EEVEE_NEXT' # set on all scenes # bpy.context — active scene/object; depends on selection state
active_obj = bpy.context.active_object # may be None if nothing selected
scene = bpy.context.scene # current scene # bpy.ops — runs operator (like clicking UI buttons); needs correct context
bpy.ops.object.camera_add(location=(0, -5, 2))
bpy.ops.render.render(write_still=True) # Prefer bpy.data over bpy.ops for data mutations in headless scripts:
# GOOD: bpy.data.objects['Cube'].location = (1, 0, 0)
# AVOID in headless: bpy.ops.transform.translate(...) — needs selection context # For operations that have no bpy.data equivalent (import, render), bpy.ops is required.
- **Gotchas:** bpy.ops operators require a valid context (active object, correct mode, etc.). In headless scripts with no UI, some operators fail with 'context is incorrect'. For pure data manipulation (moving objects, setting properties), always prefer bpy.data direct access — it bypasses context checks. bpy.ops.render.render() is an exception and works reliably headless. In 4.x, bpy.context is read-only for most scene-level properties; use bpy.context.scene.X = Y for scene props but use bpy.data for datablocks.
- **For Studio:** Pipeline scripts that set camera positions, material properties, or scene settings should use bpy.data wherever possible to avoid context-dependency failures in CI/headless renders.
- **Verify (solid):** bpy.ops vs bpy.data distinction confirmed via CGWire blog (fetched) and MotionGPT scene.py patterns (fetched). Context-invalidity gotcha for bpy.ops in headless is well-documented across blenderartists.org and devtalk.blender.org search results. | cross-family (deepseek-v3.1): confirmed — Accurate explanation of bpy namespace usage patterns for headless scripting in Blender 4.x. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Blender Scripting for Animation Pipelines (CGWire blog, 2026)](https://blog.cg-wire.com/blender-scripting-animation/) — bpy.ops exposes UI-mirroring operators; bpy.data gives direct datablock access; prefer bpy.data for headless data mutations ; [MotionGPT Blender scene.py](https://huggingface.co/spaces/fjibj/MotionGPT/blob/b625c801edd539dec9915d7fb48d54565ea566dc/mGPT/render/blender/scene.py) — Production headless script uses bpy.data.scenes[0].render.engine and bpy.context.preferences.addons in combination — showing both namespaces in practice

### bpy.ops.render — write_still (API 4.5) · `✅ solid` · Blender 4.5 LTS
**render() with write_still saves to scene render filepath.**
- **How:** Script-side still dump per camera angle.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [bpy.ops.render — write_still (API 4.5)](https://docs.blender.org/api/4.5/bpy.ops.render.html) — bpy.ops.render.write_still

### Command-line render (Manual latest) — claim holds · `▸ plausible` · Blender 4.5 LTS
**-b background render without graphical display.**
- **How:** CLI contract; x as KB target from latest URL.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (plausible):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Command-line render (Manual latest) — claim holds](https://docs.blender.org/manual/en/latest/advanced/command_line/render.html) — -b background render

### Install Python packages into Blender's bundled Python · `▸ plausible` · Blender 4.2+
**Add third-party pip packages (e.g. numpy, trimesh) to Blender's internal Python environment so headless scripts can import them.**
- **How:** # Method 1: From OUTSIDE Blender (recommended for CI/build setup)
# Find Blender's Python executable, then:
/path/to/blender/4.x/python/bin/python3.xx -m pip install numpy
# On Windows: C:/Program Files/Blender Foundation/Blender 4.2/4.2/python/bin/python.exe # Method 2: From INSIDE a bpy script (Blender 4.2+, user-writable path)
import bpy, sys, subprocess, site
python_exe = sys.executable # Blender's own python
modules_path = bpy.utils.user_resource('SCRIPTS', path='modules', create=True)
subprocess.check_call([ python_exe, '-m', 'pip', 'install', '--upgrade', '--target', modules_path, 'numpy'
])
sys.path.insert(0, modules_path)
site.addsitedir(modules_path)
import numpy # now importable # Method 3: CLI inline bootstrap before script runs
# blender --background --python-expr "
import subprocess, sys
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])
" --python my_script.py
- **Gotchas:** Must use Blender's own sys.executable, NOT the system Python — packages installed to system Python are NOT visible to Blender. On Windows the path is inside the Blender install folder (not AppData). bpy.utils.user_resource installs to a per-user scripts/modules directory that persists across Blender restarts. In Docker/CI, prefer Method 1 (external pip install to Blender's python) at image build time to avoid install overhead at render time. pip is bundled with Blender 3.1+ so ensurepip workarounds are generally not needed in 4.x.
- **For Studio:** Required if the turnaround script imports trimesh (for mesh centering/bounds), Pillow (sprite compositing), or other pipeline dependencies not bundled with Blender.
- **Verify (plausible):** Method 2 (user_resource + subprocess + sys.executable) confirmed via Medium article for Blender 4.2+ (fetched). Method 1 (external python) is standard practice. pip bundled since 3.1 is from search results but not doc-confirmed for 4.x specifically — hence plausible not solid. | cross-family (deepseek-v3.1): confirmed — Valid methods for installing packages to Blender's Python environment in 4.2+. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Installing Python packages for Blender 4.2+ (Antoine Boucher, Medium)](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81) — sys.executable + pip install --target bpy.utils.user_resource('SCRIPTS', path='modules') is the correct Blender 4.2+ in-script package install pattern ; [Blender Artists — Installing pip packages in Blender (2.8+)](https://blenderartists.org/t/how-to-install-python-packages-with-pip-blender-2-8/1142721) — Blender bundles its own Python; packages must be installed to Blender's Python, not system Python

### 3DCodeBench: Benchmarking Agentic Procedural 3D Modeling Via Code · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Instantiates the operator on **Blender 5.0**; failures mostly from API mismatches; Experience Library catalogs Blender 5.0 syntax changes and migration rules from older versions — explicit 5.0 pin + cross-major break surface (not a silent 4.x patch).**
- **How:** Literature on Blender version pin vs 5.x; no silent upgrade invent.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [3DCodeBench: Benchmarking Agentic Procedural 3D Modeling Via Code](https://arxiv.org/abs/2606.01057) — Instantiates the operator on **Blender 5.0**; failures mostly from API mismatches; Experience Library catalogs Blender 5.0 syntax changes and migration rules from older versions — explicit 5.0 pin + c

### APOLLO Blender: A Robotics Library for Visualization and Animation in Blender · `⚠ shaky` · Blender 4.x pin (still-current)
**APOLLO Blender robotics viz/animation library — UNVERIFIED claim mismatch on still-current pin-4.x; land verified=false.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 APOLLO UNVERIFIED claim mismatch; verified=false; Pin 4.x [no external verdict — not checked]
- **Sources:** [APOLLO Blender: A Robotics Library for Visualization and Animation in Blender](https://arxiv.org/abs/2512.23103) — APOLLO Blender robotics viz/animation library — UNVERIFIED claim mismatch on still-current pin-4.x; land verified=false.

### Bioinspired123D: Generative 3D Modeling System for Bioinspired Structures · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Dataset/validation runs **Blender 4.2 LTS** with bpy; render engine **Eevee Next**; headless Blender subprocess validates scripts — explicit 4.2 LTS + EEVEE Next headless pin (not 5.0).**
- **How:** Literature on Blender version pin vs 5.x; no silent upgrade invent.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Bioinspired123D: Generative 3D Modeling System for Bioinspired Structures](https://arxiv.org/abs/2603.29592) — Dataset/validation runs **Blender 4.2 LTS** with bpy; render engine **Eevee Next**; headless Blender subprocess validates scripts — explicit 4.2 LTS + EEVEE Next headless pin (not 5.0).

### Blender 4.5 CLI arguments · `⚠ shaky` · Blender 4.x pin (still-current)
**CLI -b/-P/--python-expr on 4.5 — headless knobs for pinned farm; silent 4→5: 0.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blender 4.5 CLI arguments](https://docs.blender.org/manual/en/4.5/advanced/command_line/arguments.html) — CLI -b/-P/--python-expr on 4.5 — headless knobs for pinned farm; silent 4→5: 0.

### Blender 4.5 CLI render · `⚠ shaky` · Blender 4.x pin (still-current)
**CLI render order on 4.5 — left-to-right; -f/-a last; dated currency for pin-4.x.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blender 4.5 CLI render](https://docs.blender.org/manual/en/4.5/advanced/command_line/render.html) — CLI render order on 4.5 — left-to-right; -f/-a last; dated currency for pin-4.x.

### Blender 4.5 LTS product · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**4.5 LTS: ~2 years updates (to Jul 2027 per dev notes), full Vulkan support. Positions 4.5 as the long-support companion vs jumping major.**
- **How:** Official 4.5 LTS vs 5.0 docs; -b/-P stay; logging/color/EEVEE id breaks.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Blender 4.5 LTS product](https://www.blender.org/download/releases/4-5/) — 4.5 LTS: ~2 years updates (to Jul 2027 per dev notes), full Vulkan support. Positions 4.5 as the long-support companion vs jumping major.

### Blender 4.5 LTS product (analog) · `⚠ shaky` · Blender 4.x pin (still-current)
**Analog 4.5-product LTS pin; Hold dated still-current 4.x. Limit: product page not silent-upgrade license.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blender 4.5 LTS product (analog)](https://www.blender.org/download/releases/4-5/) — Analog 4.5-product LTS pin; Hold dated still-current 4.x. Limit: product page not silent-upgrade license.

### Blender 4.5 LTS product page · `⚠ shaky` · Blender 4.x pin (still-current)
**4.5 LTS product notes — long-support pin; contrast 5.2 current stable naming.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blender 4.5 LTS product page](https://www.blender.org/download/releases/4-5/) — 4.5 LTS product notes — long-support pin; contrast 5.2 current stable naming.

### Blender 4.5 Manual · `⚠ shaky` · Blender 4.x pin (still-current)
**Manual 4.5 — dated docs currency for pinned 4.x farm; 5.2 named current stable elsewhere.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blender 4.5 Manual](https://docs.blender.org/manual/en/4.5/) — Manual 4.5 — dated docs currency for pinned 4.x farm; 5.2 named current stable elsewhere.

### Blender 4.5 Release Notes (dev) · `⚠ shaky` · Blender 4.x pin (still-current)
**4.5 LTS release notes — dated 4.5 currency; not a silent jump to 5.x.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blender 4.5 Release Notes (dev)](https://developer.blender.org/docs/release_notes/4.5/) — 4.5 LTS release notes — dated 4.5 currency; not a silent jump to 5.x.

### Blender 5.0 Core · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Unified logger; background render progress format changed. Replacements on page: `--debug-cycles` → `--log cycles`; `--debug-ffmpeg` → `--log video`; `--verbose` → `--log-level [info|debug|trace]`. Farm parsers that scrape old progress lines break.**
- **How:** Official 4.5 LTS vs 5.0 docs; -b/-P stay; logging/color/EEVEE id breaks.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Blender 5.0 Core](https://developer.blender.org/docs/release_notes/5.0/core/) — Unified logger; background render progress format changed. Replacements on page: `--debug-cycles` → `--log cycles`; `--debug-ffmpeg` → `--log video`; `--verbose` → `--log-level [info/debug/trace]`. Fa

### Blender 5.0 EEVEE & Viewport · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Breaking: Light Probe Volume backface meaning fix; View Layer Overrides change older renders; engine id `BLENDER_EEVEE_NEXT` → `BLENDER_EEVEE`; curves `resolution` now honored (can 15× geometry vs 4.5). Color/HDR path also backend-dependent.**
- **How:** Official 4.5 LTS vs 5.0 docs; -b/-P stay; logging/color/EEVEE id breaks.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Blender 5.0 EEVEE & Viewport](https://developer.blender.org/docs/release_notes/5.0/eevee/) — Breaking: Light Probe Volume backface meaning fix; View Layer Overrides change older renders; engine id `BLENDER_EEVEE_NEXT` → `BLENDER_EEVEE`; curves `resolution` now honored (can 15× geometry vs 4.5

### Blender 5.0 Release Notes · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Analog (currency): major 5.0 with Compatibility section / listed breaks. Holds: not a silent 4.x patch; pin turnaround on 4.x until a dedicated 5.x wave. Limit: release notes ≠ farm runbook rewrite.**
- **How:** Adjacent SemVer/LTS/migration hold-with-limit; 5.0-as-patch omitted.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Blender 5.0 Release Notes](https://developer.blender.org/docs/release_notes/5.0/) — Analog (currency): major 5.0 with Compatibility section / listed breaks. Holds: not a silent 4.x patch; pin turnaround on 4.x until a dedicated 5.x wave. Limit: release notes ≠ farm runbook rewrite.

### Blender 5.0 Release Notes (breaks) · `⚠ shaky` · Blender 4.x pin (still-current)
**Analog 5.0 listed Compatibility breaks; Hold treat as major migrate not patch. Limit: 5.0 notes not invent silent 4→5.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blender 5.0 Release Notes (breaks)](https://developer.blender.org/docs/release_notes/5.0/) — Analog 5.0 listed Compatibility breaks; Hold treat as major migrate not patch. Limit: 5.0 notes not invent silent 4→5.

### Blender 5.0 Release Notes (dev) · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Major release with listed Compatibility breaks (name length 255, big-endian gone, Intel Mac gone, Collada gone, GPU mins, theme API rewrite, blend compression default). Not framed as a silent 4.x patch.**
- **How:** Official 4.5 LTS vs 5.0 docs; -b/-P stay; logging/color/EEVEE id breaks.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Blender 5.0 Release Notes (dev)](https://developer.blender.org/docs/release_notes/5.0/) — Major release with listed Compatibility breaks (name length 255, big-endian gone, Intel Mac gone, Collada gone, GPU mins, theme API rewrite, blend compression default). Not framed as a silent 4.x patc

### Blender 5.0 product notes · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Recaps color-management/HDR/wide-gamut overhaul (ACES views, Working Color Space, AgX HDR) plus EEVEE/Cycles feature and requirement changes. Pipeline must treat version as explicit pin.**
- **How:** Official 4.5 LTS vs 5.0 docs; -b/-P stay; logging/color/EEVEE id breaks.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Blender 5.0 product notes](https://www.blender.org/download/releases/5-0/) — Recaps color-management/HDR/wide-gamut overhaul (ACES views, Working Color Space, AgX HDR) plus EEVEE/Cycles feature and requirement changes. Pipeline must treat version as explicit pin.

### Blender LTS downloads · `⚠ shaky` · Blender 4.x pin (still-current)
**LTS download page — production pin target; 4.5 LTS line for still-current farms.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blender LTS downloads](https://www.blender.org/download/lts/) — LTS download page — production pin target; 4.5 LTS line for still-current farms.

### Blender Python API 4.5 · `⚠ shaky` · Blender 4.x pin (still-current)
**bpy API 4.5 — headless script surface for pin-4.x; do not float to 5.x silently.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blender Python API 4.5](https://docs.blender.org/api/4.5/) — bpy API 4.5 — headless script surface for pin-4.x; do not float to 5.x silently.

### Blender Release Notes index · `⚠ shaky` · Blender 4.x pin (still-current)
**Dev release-notes index — dated currency surface for major/minor lines; pin 4.x still-current vs 5.x.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blender Release Notes index](https://developer.blender.org/docs/release_notes/) — Dev release-notes index — dated currency surface for major/minor lines; pin 4.x still-current vs 5.x.

### BlenderRAG: High-Fidelity 3D Object Generation via Retrieval-Augmented Code Synthesis · `⚠ shaky` · Blender 4.x pin (still-current)
**BlenderRAG RAG over curated Blender code examples raises compile success — code-synthesis deepen on pinned 4.x; no silent major bump.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [BlenderRAG: High-Fidelity 3D Object Generation via Retrieval-Augmented Code Synthesis](https://arxiv.org/abs/2605.00632) — BlenderRAG RAG over curated Blender code examples raises compile success — code-synthesis deepen on pinned 4.x; no silent major bump.

### Blendify -- Python rendering framework for Blender · `⚠ shaky` · Blender 4.x pin (still-current)
**Blendify: lightweight Python framework over Blender bpy for scene creation/rendering — deepens headless pin-4.x stack; not a silent 4→5 bump.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Blendify -- Python rendering framework for Blender](https://arxiv.org/abs/2410.17858) — Blendify: lightweight Python framework over Blender bpy for scene creation/rendering — deepens headless pin-4.x stack; not a silent 4→5 bump.

### CLI-Anything: Towards Agent-Native Computer Use · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Headless Blender binary runs generated bpy render scripts; EEVEE path is version-tolerant: newer builds select `BLENDER_EEVEE_NEXT`, while **Blender 4.0** still selects `BLENDER_EEVEE` — engine-enum break across the 4.0→EEVEE-Next pin.**
- **How:** Literature on Blender version pin vs 5.x; no silent upgrade invent.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [CLI-Anything: Towards Agent-Native Computer Use](https://arxiv.org/abs/2606.03854) — Headless Blender binary runs generated bpy render scripts; EEVEE path is version-tolerant: newer builds select `BLENDER_EEVEE_NEXT`, while **Blender 4.0** still selects `BLENDER_EEVEE` — engine-enum b

### Calendar Versioning (CalVer) · `⚠ shaky` · Blender 4.x pin (still-current)
**Analog CalVer date-stamped currency; Hold still-current-as-of labels. Limit: stamp not invent-5.x wave.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Calendar Versioning (CalVer)](https://calver.org/) — Analog CalVer date-stamped currency; Hold still-current-as-of labels. Limit: stamp not invent-5.x wave.

### Command Line Arguments · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Headless knobs on page: `-b`/`--background`, `-P`/`--python`, `--python-expr`, `--factory-startup`, `--` pass-through; Cycles `--cycles-device` after `--`; Logging `--log` / `--log-level` (numeric); Debug still lists `--debug-cycles`.**
- **How:** Official 4.5 LTS vs 5.0 docs; -b/-P stay; logging/color/EEVEE id breaks.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Command Line Arguments](https://docs.blender.org/manual/en/4.5/advanced/command_line/arguments.html) — Headless knobs on page: `-b`/`--background`, `-P`/`--python`, `--python-expr`, `--factory-startup`, `--` pass-through; Cycles `--cycles-device` after `--`; Logging `--log` / `--log-level` (numeric); D

### Command Line Arguments · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Same stay: `-b`, `-P`, `--python-expr`, `--factory-startup`, `--`, `--cycles-device`. Logging section rewritten (named `--log-level` fatal|error|warning|info|debug|trace; `--log-list-categories`; `--log-show-memory`/`--log-show-source`). `--debug-cycles` moved under Other Options (compat note elsewhere maps it to `--log cycles`). Format list drops AVI RAW/JPEG vs 4.5 page.**
- **How:** Official 4.5 LTS vs 5.0 docs; -b/-P stay; logging/color/EEVEE id breaks.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Command Line Arguments](https://docs.blender.org/manual/en/5.0/advanced/command_line/arguments.html) — Same stay: `-b`, `-P`, `--python-expr`, `--factory-startup`, `--`, `--cycles-device`. Logging section rewritten (named `--log-level` fatal/error/warning/info/debug/trace; `--log-list-categories`; `--l

### Dockerfile `FROM` image@digest · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Analog: pin by digest (immutable) rather than a floating tag. Holds for farm images/binaries pinned to exact Blender 4.x builds. Limit: container digest ≠ `.blend` forward-compat.**
- **How:** Adjacent SemVer/LTS/migration hold-with-limit; 5.0-as-patch omitted.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Dockerfile `FROM` image@digest](https://docs.docker.com/reference/dockerfile/#from) — Analog: pin by digest (immutable) rather than a floating tag. Holds for farm images/binaries pinned to exact Blender 4.x builds. Limit: container digest ≠ `.blend` forward-compat.

### EZBlender: Efficient 3D Editing with Plan-and-ReAct Agent · `⚠ shaky` · Blender 4.x pin (still-current)
**EZBlender Plan-and-ReAct Blender editing agent — agentic bpy deepen; pin 4.x; silent 4→5: 0.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [EZBlender: Efficient 3D Editing with Plan-and-ReAct Agent](https://arxiv.org/abs/2601.07143) — EZBlender Plan-and-ReAct Blender editing agent — agentic bpy deepen; pin 4.x; silent 4→5: 0.

### From Idea to Co-Creation: A Planner–Actor–Critic Framework for Agent Augmented 3D Modeling · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Agents emit executable Blender Python (`import bpy` / `bpy.ops`) via Blender-MCP without clearing the scene — live bpy automation surface; does not establish a silent 4→5 upgrade.**
- **How:** Literature on Blender version pin vs 5.x; no silent upgrade invent.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [From Idea to Co-Creation: A Planner–Actor–Critic Framework for Agent Augmented 3](https://arxiv.org/abs/2601.05016) — Agents emit executable Blender Python (`import bpy` / `bpy.ops`) via Blender-MCP without clearing the scene — live bpy automation surface; does not establish a silent 4→5 upgrade.

### How to port Python 2 Code to Python 3 · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Analog: Python 2 EOL → deliberate port, not a quiet upgrade. Holds for treating DCC major bumps as migration projects. Limit: language EOL ≠ Blender file/API break list.**
- **How:** Adjacent SemVer/LTS/migration hold-with-limit; 5.0-as-patch omitted.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [How to port Python 2 Code to Python 3](https://docs.python.org/3/howto/pyporting.html) — Analog: Python 2 EOL → deliberate port, not a quiet upgrade. Holds for treating DCC major bumps as migration projects. Limit: language EOL ≠ Blender file/API break list.

### MeshCoder: LLM-Powered Structured Mesh Code Generation from Point Clouds · `⚠ shaky` · Blender 4.x pin (still-current)
**MeshCoder reconstructs point clouds into editable Blender Python scripts — mesh-code deepen; pin 4.x; silent 4→5: 0.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [MeshCoder: LLM-Powered Structured Mesh Code Generation from Point Clouds](https://arxiv.org/abs/2508.14879) — MeshCoder reconstructs point clouds into editable Blender Python scripts — mesh-code deepen; pin 4.x; silent 4→5: 0.

### Nimbus: A Unified Embodied Synthetic Data Generation Framework · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Blender backend uses OptiX RT/Tensor cores and **multi-process workers** to bypass the Python GIL that limits standard Blender to one thread — farm-scale headless Cycles/OptiX craft under in-process GIL pressure.**
- **How:** Literature on Blender version pin vs 5.x; no silent upgrade invent.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Nimbus: A Unified Embodied Synthetic Data Generation Framework](https://arxiv.org/abs/2601.21449) — Blender backend uses OptiX RT/Tensor cores and **multi-process workers** to bypass the Python GIL that limits standard Blender to one thread — farm-scale headless Cycles/OptiX craft under in-process G

### Node.js Releases (Current → Active LTS) · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Analog: production pins Active LTS; Current is for library prep. Holds for pinning Blender 4.x LTS (e.g. 4.5) while 5.0 is a new major. Limit: Node odd/even LTS rules ≠ Blender LTS schedule.**
- **How:** Adjacent SemVer/LTS/migration hold-with-limit; 5.0-as-patch omitted.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Node.js Releases (Current → Active LTS)](https://nodejs.org/en/about/previous-releases) — Analog: production pins Active LTS; Current is for library prep. Holds for pinning Blender 4.x LTS (e.g. 4.5) while 5.0 is a new major. Limit: Node odd/even LTS rules ≠ Blender LTS schedule.

### Node.js previous releases (LTS) · `⚠ shaky` · Blender 4.x pin (still-current)
**Analog Active LTS vs Current; Hold pin Blender 4.x LTS for production farms. Limit: Node LTS not Blender API.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Node.js previous releases (LTS)](https://nodejs.org/en/about/previous-releases) — Analog Active LTS vs Current; Hold pin Blender 4.x LTS for production farms. Limit: Node LTS not Blender API.

### Nova3D: Code-Native Generation of Programmable 3D Assets · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Asset = executable Blender Python; compiled via **headless Blender** deterministic operator to GLB — code-native headless bpy farm without claiming a silent major upgrade.**
- **How:** Literature on Blender version pin vs 5.x; no silent upgrade invent.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Nova3D: Code-Native Generation of Programmable 3D Assets](https://arxiv.org/abs/2607.22738) — Asset = executable Blender Python; compiled via **headless Blender** deterministic operator to GLB — code-native headless bpy farm without claiming a silent major upgrade.

### ProcFunc: Function-Oriented Abstractions for Procedural 3D Generation in Python · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Blender-based procedural library with atomic bpy primitives plus an **EEVEE** render interface for large-scale dataset generation — EEVEE-as-dataset path on Blender procedural stack.**
- **How:** Literature on Blender version pin vs 5.x; no silent upgrade invent.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [ProcFunc: Function-Oriented Abstractions for Procedural 3D Generation in Python](https://arxiv.org/abs/2604.26943) — Blender-based procedural library with atomic bpy primitives plus an **EEVEE** render interface for large-scale dataset generation — EEVEE-as-dataset path on Blender procedural stack

### Rendering From The Command Line · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Args left-to-right; always put `-f` or `-a` last; wrong order silently ignores output path. Same order rule still documented on 5.0 args page.**
- **How:** Official 4.5 LTS vs 5.0 docs; -b/-P stay; logging/color/EEVEE id breaks.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Rendering From The Command Line](https://docs.blender.org/manual/en/4.5/advanced/command_line/render.html) — Args left-to-right; always put `-f` or `-a` last; wrong order silently ignores output path. Same order rule still documented on 5.0 args page.

### SceneCode: Executable World Programs for Editable Indoor Scenes with Articulated Objects · `⚠ shaky` · Blender 4.x pin (still-current)
**SceneCode emits part-wise Blender Python for articulated indoor scenes — executable-world deepen; pin 4.x.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [SceneCode: Executable World Programs for Editable Indoor Scenes with Articulated Objects](https://arxiv.org/abs/2605.19587) — SceneCode emits part-wise Blender Python for articulated indoor scenes — executable-world deepen; pin 4.x.

### SceneCraft: An LLM Agent for Synthesizing 3D Scene as Blender Code · `⚠ shaky` · Blender 4.x pin (still-current)
**SceneCraft LLM agent emits Blender-executable Python for complex scenes — bpy code-gen deepen; pin 4.x; silent 4→5: 0.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [SceneCraft: An LLM Agent for Synthesizing 3D Scene as Blender Code](https://arxiv.org/abs/2403.01248) — SceneCraft LLM agent emits Blender-executable Python for complex scenes — bpy code-gen deepen; pin 4.x; silent 4→5: 0.

### ScratchSim: A Procedural Synthetic Data Pipeline for Surface Scratch Detection · `⚠ shaky` · Blender 4.x pin (still-current)
**ScratchSim BlenderProc procedural synthetic scratch data — farm/proc deepen; pin 4.x; silent 4→5: 0.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [ScratchSim: A Procedural Synthetic Data Pipeline for Surface Scratch Detection](https://arxiv.org/abs/2607.27065) — ScratchSim BlenderProc procedural synthetic scratch data — farm/proc deepen; pin 4.x; silent 4→5: 0.

### Semantic Versioning 2.0.0 · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Analog: MAJOR = incompatible API changes; PATCH ≠ that. Holds: Blender 5.0 is a major line, not a silent 4.x patch for the sprite farm. Limit: SemVer policy ≠ Blender’s own release cadence labels.**
- **How:** Adjacent SemVer/LTS/migration hold-with-limit; 5.0-as-patch omitted.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Semantic Versioning 2.0.0](https://semver.org/) — Analog: MAJOR = incompatible API changes; PATCH ≠ that. Holds: Blender 5.0 is a major line, not a silent 4.x patch for the sprite farm. Limit: SemVer policy ≠ Blender’s own release cadence labels.

### Semantic Versioning 2.0.0 · `⚠ shaky` · Blender 4.x pin (still-current)
**Analog SemVer MAJOR=incompatible; Hold pin+cite; silent 4→5 retarget fails. Limit: SemVer not invent 5.x.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Semantic Versioning 2.0.0](https://semver.org/) — Analog SemVer MAJOR=incompatible; Hold pin+cite; silent 4→5 retarget fails. Limit: SemVer not invent 5.x.

### SimpleProc: Fully Procedural Synthetic Data from Simple Rules for Multi-View Stereo · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Blender data-generation pipeline renders with the **EEVEE** engine for multi-view stereo synthetic data — EEVEE-named farm path adjacent to turnaround sprites (version pin not elevated to 5.0).**
- **How:** Literature on Blender version pin vs 5.x; no silent upgrade invent.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [SimpleProc: Fully Procedural Synthetic Data from Simple Rules for Multi-View Ste](https://arxiv.org/abs/2604.04925) — Blender data-generation pipeline renders with the **EEVEE** engine for multi-view stereo synthetic data — EEVEE-named farm path adjacent to turnaround sprites (version pin not elevated to 5.0).

### Unity LTS (Long Term Support) · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Analog: production locks an LTS line for stability. Holds for blender-knowledge decisive axis Pin 4.x. Limit: Unity commercial LTS packaging ≠ Blender Foundation LTS.**
- **How:** Adjacent SemVer/LTS/migration hold-with-limit; 5.0-as-patch omitted.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Unity LTS (Long Term Support)](https://unity.com/releases/lts) — Analog: production locks an LTS line for stability. Holds for blender-knowledge decisive axis Pin 4.x. Limit: Unity commercial LTS packaging ≠ Blender Foundation LTS.

### Upgrading from Godot 3 to Godot 4 · `⚠ shaky` · Blender 4.x pin (not silent 5.0)
**Analog: major engine jump needs converter + breaking renames; formats not silently compatible. Holds for “open a 5.x wave only as migration,” not float `latest`. Limit: Godot project converter ≠ bpy/farm scripts.**
- **How:** Adjacent SemVer/LTS/migration hold-with-limit; 5.0-as-patch omitted.
- **Gotchas:** STUDY-046. Keep Pin 4.x decisive axis until deliberate 5.x wave.
- **For Studio:** Headless sprite farm pin-4.x currency; no silent upgrade.
- **Verify (shaky):** STUDY-046 deepen; silent 4→5: 0; pin-4.x holds; default unverified [no external verdict — not checked]
- **Sources:** [Upgrading from Godot 3 to Godot 4](https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.html) — Analog: major engine jump needs converter + breaking renames; formats not silently compatible. Holds for “open a 5.x wave only as migration,” not float `latest`. Limit: Godot project converter ≠ bpy/f

### Upgrading from Godot 3 to Godot 4 · `⚠ shaky` · Blender 4.x pin (still-current)
**Analog major engine migrate needs deliberate port; Hold for Blender 4→5. Limit: Godot converter not Blender farm.**
- **How:** STUDY-062 still-current pin-4.x; silent 4→5: 0.
- **Gotchas:** STUDY-062. Pin 4.x. Silent 4→5: 0.
- **For Studio:** Headless bpy pin-4.x still-current; no silent upgrade.
- **Verify (shaky):** STUDY-062 still-current; Pin 4.x; silent 4→5: 0; default unverified [no external verdict — not checked]
- **Sources:** [Upgrading from Godot 3 to Godot 4](https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.html) — Analog major engine migrate needs deliberate port; Hold for Blender 4→5. Limit: Godot converter not Blender farm.

### kajiyama blender-eevee-gpu-headless — 404 · `✗ wrong` · Blender 4.5 LTS
**Cited EEVEE GPU headless repo.**
- **How:** Verifier: HTTP 404 — leave unverified.
- **Gotchas:** Pin 4.x. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (wrong):** STUDY-027 Verifier: unverified/404 — do not land as verified [no external verdict — not checked]
- **Sources:** [kajiyama blender-eevee-gpu-headless — 404](https://github.com/shotaro-kajiyama/blender-eevee-gpu-headless) — 404 unverified

### Arnold kick — headless CLI analog · `?` · Blender 4.x
**Analog: headless CLI renderer (kick -dw -i … -o …). Holds for blender --background --python batch turnaround; limit: Arnold ≠ bpy/EEVEE Next choice.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Arnold kick — headless CLI analog](https://help.autodesk.com/cloudhelp/ENU/AR-Core/files/ac-rendering/arnold_user_guide_ac_rendering_ac_cl_rendering_html.html) — headless CLI analog

### Bioinspired123D — Blender 4.2 LTS + EEVEE Next headless · `?` · Blender 4.2 LTS
**Dataset/validation runs Blender 4.2 LTS headless with EEVEE Next, fixed TRACK_TO camera + area light — academic default still 4.2 LTS, not 5.x.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Bioinspired123D — Blender 4.2 LTS + EEVEE Next headless](https://arxiv.org/abs/2603.29592) — 4.2 LTS + EEVEE Next default

### Blender 4.5 LTS CLI arguments — -b/-P · `?` · Blender 4.5 LTS
**Documents -b/--background, -P/--python, --python-expr, --factory-startup, and -- pass-through as the headless script surface for LTS.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Blender 4.5 LTS CLI arguments — -b/-P](https://docs.blender.org/manual/en/4.5/advanced/command_line/arguments.html) — -b/-P remain on 4.5 LTS

### Blender 4.5 LTS CLI render order · `?` · Blender 4.5 LTS
**Args execute left-to-right; put -o/-F before -f/-a (always last) — wrong order silently ignores output path on still renders.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Blender 4.5 LTS CLI render order](https://docs.blender.org/manual/en/4.5/advanced/command_line/render.html) — CLI render arg order

### Blender 5.0 CLI arguments — -b/-P remain (compat note) · `?` · Blender 4.x
**Same headless knobs (-b, -P, --) remain; logging options rewritten — farm parsers must update. Pin pipeline to named 4.x; treat 5.0 as major-compat + logging-scrape break, not silent KB flip.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** x recipes; pin 4.x.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Blender 5.0 CLI arguments — -b/-P remain (compat note)](https://docs.blender.org/manual/en/5.0/advanced/command_line/arguments.html) — -b/-P remain; logging break; pin 4.x

### CLI-Anything — headless bpy EEVEE_NEXT tolerance · `?` · Blender 4.x
**Headless Blender via bpy + blender --background; EEVEE path is version-tolerant (BLENDER_EEVEE_NEXT on newer builds, BLENDER_EEVEE on 4.0) — harness absorbs 4.x engine rename, not a 5.x rewrite.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [CLI-Anything — headless bpy EEVEE_NEXT tolerance](https://arxiv.org/abs/2606.03854) — EEVEE→EEVEE_NEXT tolerance; not 5.x

### Maya CLI render — DCC batch analog · `?` · Blender 4.x
**Analog: DCC batch override flags from shell. Holds for reproducible headless sprite jobs; limit: Maya license path ≠ Blender GPL headless.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Maya CLI render — DCC batch analog](https://help.autodesk.com/cloudhelp/2023/ENU/Maya-Rendering/files/GUID-EB558BC0-5C2B-439C-9B00-F97BCB9688E4.htm) — DCC batch analog

### Nimbus — OptiX multi-process Blender batch · `?` · Blender 4.x
**Blender backend: OptiX RT/Tensor cores + multi-process workers to bypass the Python GIL for batch render throughput — scales headless craft without replacing --background --python.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Nimbus — OptiX multi-process Blender batch](https://arxiv.org/abs/2601.21449) — OptiX multi-process complement

### Nova3D — code-native Blender Python → GLB headless · `?` · Blender 4.x
**Asset = executable Blender Python; GLB is the compiled artifact via headless Blender — aligns TRELLIS-GLB → bpy render intake.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Nova3D — code-native Blender Python → GLB headless](https://arxiv.org/abs/2607.22738) — bpy→GLB headless

### ProcFunc — bpy primitives + EEVEE interface (Cycles half omitted) · `?` · Blender 4.x
**Atomic bpy primitives + EEVEE render interface for procedural rooms/datasets — still Blender-4-era EEVEE as the fast batch path. EEVEE-vs-Cycles cost claim NOT landed (Verifier partial/unverified).**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Do not land ProcFunc EEVEE-vs-Cycles as verified.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [ProcFunc — bpy primitives + EEVEE interface (Cycles half omitted)](https://arxiv.org/abs/2604.26943) — EEVEE interface only; Cycles half unverified

