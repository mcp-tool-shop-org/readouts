# Render engines: EEVEE Next & Cycles
_EEVEE Next (4.2+, replaced legacy EEVEE) vs Cycles, GPU backends, samples/denoising, film_transparent alpha output, fast sprite-render settings._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

15 recipes · 9 solid.

| Recipe | Blender | Currency | ✓ | What |
|--------|-------|----------|---|------|
| Cycles GPU rendering: OptiX/CUDA via bpy in headless mode | 4.0+ | ✅ solid | ✓ | Cycles is the path-traced renderer. In headless mode it defaults to CPU unless y |
| Cycles Introduction (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | Cycles path-tracing engine docs for 4.5 LTS. |
| Cycles adaptive sampling for sprite renders: fast convergence with quality floor | 4.0+ (adaptive sampling stable since Cycles X, ~3.0) | ✅ solid | ✓ | Cycles adaptive sampling automatically stops tracing pixels that have converged  |
| EEVEE Introduction (Manual 4.5 LTS) | 4.5 LTS | ✅ solid | · | EEVEE realtime engine docs for 4.5 LTS line. |
| EEVEE Next in Blender 4.2+: what replaced legacy EEVEE | 4.2+ | ✅ solid | ✓ | Blender 4.2 LTS (July 2024) removed EEVEE Legacy entirely and shipped EEVEE Next |
| EEVEE Next material transparency: Render Method replaces Blend Mode (4.2+) | 4.2+ | ✅ solid | ✓ | In Blender 4.2+, the per-material Blend Mode dropdown (Alpha Clip / Alpha Blend  |
| EEVEE Next vs Cycles for batch sprite/turnaround renders: choosing the right engine | 4.2+ | ✅ solid | ✓ | For a headless 8-direction sprite turnaround pipeline (import GLB → rotate camer |
| Render engine ID: BLENDER_EEVEE_NEXT vs BLENDER_EEVEE across versions | 4.2–5.0 | ✅ solid | ✓ | The Python string used to select EEVEE via `scene.render.engine` changed between |
| Transparent background alpha PNG output for sprite rendering | 4.2+ | ✅ solid | ✓ | Rendering sprites as RGBA PNG with transparent background requires two independe |
| Cycles denoising: OptiX denoiser vs OpenImageDenoise (OIDN) | 4.2+ | ▸ plausible | ✓ | Cycles produces noisy output at low sample counts; denoising is essential for fa |
| EEVEE Next: key render settings via bpy for headless batch renders | 4.2–4.4 | ▸ plausible | ✓ | The Python-accessible settings on `scene.eevee` (a `SceneEEVEE` struct) that con |
| Freestyle NPR introduction — hold-with-limit | 4.5 LTS | ▸ plausible | · | Edge/line-based NPR silhouette/crease → Line Style. |
| Blender 5.0 core logging rewrite | 4.x |  | · | Background render progress uses unified logger; --debug-cycles → --log cycles; f |
| Blender 5.0 product notes — pin version | 4.x |  | · | Recaps 5.0 color-management/HDR overhaul and EEVEE/Cycles changes; pipeline must |
| Blender 5.0 release notes — major compat (pin 4.x) | 4.x |  | · | Major 5.0 shipped Nov 18 2025 with listed compatibility breaks; not a silent 4.x |

## Detail

### Cycles GPU rendering: OptiX/CUDA via bpy in headless mode · `✅ solid` · Blender 4.0+
**Cycles is the path-traced renderer. In headless mode it defaults to CPU unless you explicitly configure the GPU device via the preferences API. OptiX (NVIDIA RTX) is the fastest backend for denoised production renders; CUDA is the fallback for older NVIDIA cards. For the studio RTX 5090, OptiX is the correct choice.**
- **How:** ```python
import bpy scene = bpy.context.scene
scene.render.engine = 'CYCLES' # ── GPU device configuration (must do in headless; prefs are not saved in.blend) ──
prefs = bpy.context.preferences
cycles_prefs = prefs.addons['cycles'].preferences # Priority list: try OptiX first, fall back to CUDA, then CPU
for device_type in ['OPTIX', 'CUDA', 'HIP', 'CPU']: cycles_prefs.compute_device_type = device_type cycles_prefs.refresh_devices() devices = [d for d in cycles_prefs.devices if d.type == device_type] if devices: for d in devices: d.use = True if device_type != 'CPU': scene.cycles.device = 'GPU' break # ── Sampling ──
scene.cycles.samples = 128 # max samples per pixel
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01 # stop when noise < this (0.01 = good balance)
scene.cycles.adaptive_min_samples = 32 # never stop below this count # ── Denoising ──
scene.cycles.use_denoising = True
# Options: 'OPTIX' (GPU, NVIDIA only), 'OPENIMAGEDENOISE' (CPU/GPU, universal)
scene.cycles.denoiser = 'OPTIX' # fastest on RTX; fall back to 'OPENIMAGEDENOISE' if unavailable
``` CLI equivalent for single frames:
```bash
blender -b scene.blend -E CYCLES -f 1 -- --cycles-device OPTIX
```
- **Gotchas:** GPU device preferences are NOT stored in .blend files — they must be set in every headless script that targets GPU rendering. Forgetting this means headless scripts render on CPU even when a GPU is present.; `cycles_prefs.refresh_devices()` must be called after setting `compute_device_type` or the device list may be stale/empty.; OptiX denoiser requires the compute device to also be set to OptiX — if you set CUDA compute but request OptiX denoiser, Blender falls back to OpenImageDenoise (OIDN) on CPU silently.; On multi-GPU setups, OptiX from the Python API may only use a single GPU by default; CUDA can use multiple. See devtalk issue on single-GPU OptiX limitation.; `--cycles-device OPTIX` CLI flag sets the device for that session but does NOT set it in the Python prefs; combine with a `-P script.py` that also sets `compute_device_type` for robustness.; HIP is the AMD equivalent of OptiX; Metal is for Apple Silicon.
- **For Studio:** Use Cycles + OptiX on the RTX 5090 when sprite fidelity matters more than speed (final-pass or reference renders). For batch 8-direction turnarounds where throughput dominates, EEVEE Next is usually faster — use Cycles selectively.
- **Verify (solid):** bpy code confirmed via danthemango gist (tested as of Blender 4.0, stable API) and renderday CLI guide for 4.4. OptiX fallback behavior confirmed via Blender 4.2 issue #125392. | cross-family (deepseek-v3.1): confirmed — Accurate description of GPU device configuration in headless mode with proper fallback logic. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [enable optix GPU rendering in blender python — GitHub Gist (danthemango)](https://gist.github.com/danthemango/1aaab8264c75be9c165dc8610357e3f3) — Complete working Python script for OptiX/CUDA/CPU fallback device selection; tested Blender 4.0. ; [Mastering the Blender CLI — renderday.com](https://renderday.com/blog/mastering-the-blender-cli) — --cycles-device OPTIX confirmed as Blender 4.4 CLI flag; OPTIX, CUDA, HIP, ONEAPI, METAL all valid values. ; [GPU Rendering — Blender 5.1 Manual](https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html) — OptiX requires NVIDIA GPU with OptiX support and driver >= 535; compute capability 5.0+.

### Cycles Introduction (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**Cycles path-tracing engine docs for 4.5 LTS.**
- **How:** Cycles-first farms remain the easier headless path.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Cycles Introduction (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/render/cycles/introduction.html) — Cycles 4.5

### Cycles adaptive sampling for sprite renders: fast convergence with quality floor · `✅ solid` · Blender 4.0+ (adaptive sampling stable since Cycles X, ~3.0)
**Cycles adaptive sampling automatically stops tracing pixels that have converged below a noise threshold, allowing noisy regions (complex lighting) to get more samples while simple regions finish early. For sprite renders this means clean flat surfaces converge fast; complex hair/metal/subsurface areas get more samples automatically.**
- **How:** ```python
scene = bpy.context.scene
scene.render.engine = 'CYCLES' # ── Adaptive sampling ──
scene.cycles.samples = 256 # hard ceiling — never more than this
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.01 # stop when pixel noise < 0.01 (good default)
scene.cycles.adaptive_min_samples = 32 # never stop before 32 samples # Practical sprite render target:
# Simple stylized characters: threshold 0.02, min 16 → very fast
# Complex metallic/glass: threshold 0.005, ceiling 512 → slower but clean # ── Denoising (pair with adaptive sampling) ──
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPTIX' # RTX 5090: use OptiX
``` Typical sprite convergence:
- Opaque stylized character: 64–128 samples with threshold 0.01 + OptiX denoise → clean
- Metallic armor / glass visor: 128–256 samples + denoiser
- Background elements: may converge at 16–32 samples automatically
- **Gotchas:** Adaptive threshold 0.0 means Blender picks automatically based on sample count — useful default but less predictable for batch pipelines. Set an explicit value.; Min samples below 16 can cause visible gradient artifacts in areas with subtle color shifts (gradients in sky, subsurface skin). Keep min ≥ 32 for characters.; Adaptive sampling + denoiser is the recommended combo; without denoising, even converged images may show low-frequency noise at small sprite resolutions.; Render time with adaptive sampling enabled is non-deterministic; for scheduling pipeline slots, benchmark a representative character and use the P95 time as budget.
- **For Studio:** Pair adaptive sampling with OptiX denoiser for Cycles hero-render passes. At 128 ceiling + 0.01 threshold + OptiX denoise, a 512×512 sprite typically completes in under 60 seconds on RTX 5090 — acceptable for infrequent reference renders.
- **Verify (solid):** Adaptive sampling properties (cycles.samples, use_adaptive_sampling, adaptive_threshold, adaptive_min_samples) are stable Cycles API since 3.0; confirmed still active in 4.x via multiple render guides and official sampling docs. | cross-family (deepseek-v3.1): confirmed — Accurate description of adaptive sampling workflow with appropriate threshold values for sprite rendering. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Render Smarter in Blender, with Adaptive Samples — Blendergrid](https://blendergrid.com/articles/render-smarter-in-blender-with-adaptive-samples) — Adaptive sampling automatically reduces samples in converged areas; min samples below 16 risks gradient artifacts; threshold 0.01 is a good production default. ; [Sampling — Blender 5.1 Manual](https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html) — Noise Threshold 0.1–0.001 range; adaptive_min_samples default 0 (auto); cycles.samples is the hard ceiling. ; [Blender Render Settings: Cycles & Eevee Guide (2026) — SuperRenders](https://superrendersfarm.com/article/blender-render-settings-optimization-guide) — Recommended: 256–512 samples, adaptive threshold 0.01, OIDN/OptiX denoiser for production scenes.

### EEVEE Introduction (Manual 4.5 LTS) · `✅ solid` · Blender 4.5 LTS
**EEVEE realtime engine docs for 4.5 LTS line.**
- **How:** Pin 4.5 EEVEE Next for headless sprite craft.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [EEVEE Introduction (Manual 4.5 LTS)](https://docs.blender.org/manual/en/4.5/render/eevee/introduction.html) — EEVEE 4.5

### EEVEE Next in Blender 4.2+: what replaced legacy EEVEE · `✅ solid` · Blender 4.2+
**Blender 4.2 LTS (July 2024) removed EEVEE Legacy entirely and shipped EEVEE Next as the only EEVEE variant. It is a ground-up rewrite that adds screen-space ray tracing for all BSDFs, Virtual Shadow Maps (VSM), unlimited lights (up to 4096 visible simultaneously), light visibility through refractive surfaces, and dynamic sphere light probes. Features that no longer exist: Contact Shadows (removed; VSM handles it), the old irradiance-volume bake workflow (replaced by per-object Volume Light Probe baking), and the legacy Ambient Occlusion distance/quality knob. Screen Space Reflections (SSR) was replaced by proper ray-traced reflections governed by `use_raytracing`. GI is now screen-space ray traced and configurable via `gi_diffuse_bounces`. Volumetric rendering capability expanded.**
- **How:** Open any.blend in 4.2+: EEVEE Legacy is gone from the engine list. The engine ID in Python changed (see recipe `eevee-next-engine-id`). Migration docs at developer.blender.org cover the automatic scene-compat pass Blender runs on open; review the migration guide if a scene looks different after upgrade. Light probe workflow: add a 'Volume' probe (renamed from Irradiance Grid), set it up, Bake Irradiance (Object > Bake Irradiance). Shadow system: use Virtual Shadow Maps by default; tune `shadow_pool_size` if VRAM is tight, `shadow_resolution_scale` for quality vs. memory. Ray tracing toggle: `scene.eevee.use_raytracing = True` enables the new ray-traced reflections/GI at the cost of render time.
- **Gotchas:** Scenes from 4.1 and earlier may look different on first open; Blender auto-migrates but some lighting setups (especially heavy Contact Shadow reliance) need manual tweaks.; The old SSR panel is gone; enabling `use_raytracing` enables full reflection ray tracing — it is slower than the old SSR approximation.; Irradiance Volume baking is now per-object, not scene-global — old mass-bake workflows need updating.; Contact Shadows setting that existed in old .blend files is silently dropped on migration.; Performance with raytracing ON approaches Cycles territory — for sprite turnarounds where GI/reflections are not critical, leave `use_raytracing = False` for maximum speed.
- **For Studio:** Understand the migration landscape before building the turnaround pipeline; importing TRELLIS GLBs into 4.2+ means EEVEE Next is the only EEVEE available. Keep raytracing OFF for batch sprite renders where pure speed matters.
- **Verify (solid):** Confirmed via Blender 4.2 release notes (developer.blender.org/docs/release_notes/4.2/eevee/) and EEVEE migration doc. EEVEE Legacy removal is a hard fact in 4.2 LTS. | cross-family (deepseek-v3.1): confirmed — Accurately describes EEVEE Next as the replacement for legacy EEVEE in 4.2+ with correct feature changes and removals. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Blender 4.2 LTS: EEVEE — Blender Developer Documentation](https://developer.blender.org/docs/release_notes/4.2/eevee/) — EEVEE was rewritten as EEVEE Next in 4.2 LTS; unlimited lights (up to 4096 visible), VSM shadows, screen-space GI, light linking all introduced. ; [EEVEE migration from older versions to Blender 4.2 LTS](https://developer.blender.org/docs/release_notes/4.2/eevee_migration/) — Contact Shadows removed; irradiance baking workflow changed to per-object; most scenes auto-migrate but some manual fixes needed. ; [Eevee Next finally arrives in Blender — CG Channel](https://www.cgchannel.com/2024/07/eevee-next-finally-arrives-in-blender/) — EEVEE Next shipped in 4.2 LTS July 2024 with screen-space GI, VSM, motion blur, and unlimited shader support.

### EEVEE Next material transparency: Render Method replaces Blend Mode (4.2+) · `✅ solid` · Blender 4.2+
**In Blender 4.2+, the per-material Blend Mode dropdown (Alpha Clip / Alpha Blend / Alpha Hashed) was removed and replaced by a new Render Method system. The default method is Dithered (approximates old Alpha Hashed) and Blended replicates old Alpha Blend. This affects sprite materials that use partial transparency or cutout alpha, not the world background transparency (which is `film_transparent`).**
- **How:** The Render Method is a material property, settable via bpy:
```python
# Set render method on a material
mat = bpy.data.materials['CharacterSkin']
mat.surface_render_method = 'DITHERED' # default; approximates Alpha Hashed
# OR:
mat.surface_render_method = 'BLENDED' # approximates Alpha Blend; prone to sort issues
``` For sprite cutout (sharp alpha clip — e.g., hair cards, leaf cards):
- No direct 'CLIP' method exists in EEVEE Next
- Workaround: in the material shader, use a Math node (Greater Than, threshold 0.5) on the Alpha before connecting to BSDF Alpha input, then set Render Method to 'DITHERED' For transparent world background (scene-level):
- This is `scene.render.film_transparent = True` (unchanged, see recipe `film-transparent-rgba-sprite-output`)
- **Gotchas:** Dithered transparency produces a noisy/stippled look at low sample counts. Raise `eevee.taa_render_samples` to 128 or higher to suppress dither noise on sprite edges.; Old .blend files auto-migrate: Alpha Hashed → Dithered, Alpha Blend → Blended. Alpha Clip has no direct equivalent — migrated files may need manual shader adjustment.; Blended (equivalent to old Alpha Blend) has Z-sorting issues for overlapping transparent geometry — avoid for complex multi-layered character sprites.; The property name `surface_render_method` should be verified at runtime — it may vary between Blender sub-versions; check `mat.bl_rna.properties.keys()` if scripts fail.; Cycles is unaffected by this change; Cycles always does full ray-traced transparency regardless of material Render Method setting.
- **For Studio:** Relevant when TRELLIS GLBs contain partially transparent materials (e.g., hair, cloth edges, visor glass). Set Render Method explicitly in the pipeline script after GLB import to avoid inheriting stale-migration defaults. Use Dithered + high samples (128) for clean sprite edges.
- **Verify (solid):** Confirmed via katsbits.com EEVEE transparency deep-dive (specifically covers 4.2+ Render Method) and Blender Artists community threads #1539602 and #1537320. | cross-family (deepseek-v3.1): confirmed — Correctly describes the Render Method system replacing Blend Mode in 4.2+ with proper property names. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Eevee, Transparency & Blender 4.2+ — KatsBits Codex](https://www.katsbits.com/codex/eevee-transparency-dithered/) — Blend Mode replaced by Render Method in 4.2; Dithered = default/Alpha Hashed approx; Blended = Alpha Blend; Alpha Clip has no direct equivalent, workaround documented. ; [Blender 4.2 Eevee (Next) transparency — Blender Artists #1539602](https://blenderartists.org/t/blender-4-2-eevee-next-transparency/1539602) — Community confirms Render Method as the 4.2+ replacement; dithered noise reduced by increasing samples.

### EEVEE Next vs Cycles for batch sprite/turnaround renders: choosing the right engine · `✅ solid` · Blender 4.2+
**For a headless 8-direction sprite turnaround pipeline (import GLB → rotate camera or object → render 8 frames → export PNGs), the choice between EEVEE Next and Cycles is a speed-vs-fidelity tradeoff. EEVEE Next renders in seconds per frame (rasterisation-based); Cycles takes minutes per frame (path tracing). For stylized 2.5D game sprites at 256–512px, EEVEE Next quality is typically sufficient and the throughput advantage is decisive.**
- **How:** Decision matrix: | Criterion | EEVEE Next | Cycles |
|-----------|-----------|--------|
| Speed (256px sprite) | ~0.5–3 seconds/frame | ~30–120 seconds/frame |
| Global illumination | Screen-space approx | True path tracing |
| Stylized/toon look | Excellent | Good |
| Physically accurate lighting | Approximate | Accurate |
| Raytraced reflections | Optional (use_raytracing) | Always |
| Transparency quality | Dithered (default) / Blended | Full ray traced |
| Headless GPU support | Yes (via display/software emulation) | Yes (compute, no display needed) |
| Best for | Batch production sprites | Hero/reference renders | Recommended pipeline:
- Default engine: EEVEE Next with `use_raytracing=False`, `taa_render_samples=64`
- Override to Cycles for final-pass reference sheets or hero character close-ups where lighting accuracy matters
- Never use Workbench for production sprites (no material shading)
- **Gotchas:** Older forum posts and tutorials say 'EEVEE can't do headless' — this is stale. EEVEE Next runs in `blender --background` on Linux/Windows without a display (uses software GL on headless servers, or real GPU on workstations).; On a headless Linux server without display, EEVEE Next may need the `--no-window-focus` flag or OSMesa/EGL support compiled in. On a Windows workstation (the studio Robot rig), this is not an issue.; EEVEE Next with `use_raytracing=True` closes some of the speed gap against Cycles but still rasterises the base shading; it is not full path tracing.; Dithered transparency in EEVEE Next at low samples shows grain on character silhouettes — raise `taa_render_samples` to 128 or use Cycles if clean alpha edges are critical at small sizes.
- **For Studio:** Use EEVEE Next as the default engine for all turnaround batch renders. Speed advantage over Cycles is 10–60x at sprite resolutions; stylized JRPG art does not need physically accurate GI. Reserve Cycles for curated reference renders.
- **Verify (solid):** Speed comparison grounded in irendering.net 4.2 EEVEE vs Cycles comparison. Headless EEVEE capability confirmed via multiple community reports and renderday CLI guide covering 4.4. | cross-family (deepseek-v3.1): confirmed — Accurate comparison of speed vs fidelity tradeoffs for sprite rendering workflows. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Blender 4.2's Eevee Next and Cycles Comparison — iRender Farm](https://irendering.net/blender-4-2s-eevee-next-and-cycles-comparison/) — EEVEE Next produces frames in seconds vs Cycles minutes; EEVEE Next recommended for tasks requiring quick feedback or animations. ; [Eevee vs Cycles: When Each Wins on a Cloud Farm (2026) — SuperRenders](https://superrendersfarm.com/article/eevee-vs-cycles-cloud-render-farm-comparison-2026) — EEVEE consistently renders significantly faster across various scene complexities; Cycles preferred for projects demanding top-notch photorealistic visuals. ; [Mastering the Blender CLI — renderday.com](https://renderday.com/blog/mastering-the-blender-cli) — Headless EEVEE rendering confirmed working in Blender 4.4 via -b flag; no special display requirement noted for workstation use.

### Render engine ID: BLENDER_EEVEE_NEXT vs BLENDER_EEVEE across versions · `✅ solid` · Blender 4.2–5.0
**The Python string used to select EEVEE via `scene.render.engine` changed between major Blender versions. This is the #1 stale-code trap in headless scripts sourced from pre-4.2 tutorials.**
- **How:** Version matrix:
- Blender ≤ 4.1 (Legacy EEVEE): `'BLENDER_EEVEE'`
- Blender 4.2 – 4.4 (EEVEE Next): `'BLENDER_EEVEE_NEXT'`
- Blender 5.0+ (EEVEE Next, renamed back): `'BLENDER_EEVEE'` Version-safe helper:
```python
import bpy def set_eevee(scene): ver = bpy.app.version # (major, minor, patch) tuple if ver >= (5, 0, 0): scene.render.engine = 'BLENDER_EEVEE' elif ver >= (4, 2, 0): scene.render.engine = 'BLENDER_EEVEE_NEXT' else: scene.render.engine = 'BLENDER_EEVEE'
```
Alternatively probe the engine enum at runtime: `bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items.keys()` returns available IDs.
- **Gotchas:** Any script that sets `'BLENDER_EEVEE'` and targets Blender 4.2–4.4 will silently fall back to Cycles (or raise an error) — there is NO legacy EEVEE in 4.2+.; Blender 5.0 reverts the ID back to `'BLENDER_EEVEE'`, so a script pinned to `'BLENDER_EEVEE_NEXT'` will break on 5.0.; The `-E EEVEE` CLI flag behavior may differ from the Python string; always test with explicit bpy assignment in headless scripts.; GitHub CI scripts and tutorial code from 2022-2023 almost universally use `'BLENDER_EEVEE'` — all stale for 4.2–4.4.
- **For Studio:** Load-bearing in the headless turnaround pipeline. The render script that rotates the TRELLIS GLB and fires `bpy.ops.render.render()` for each of 8 directions must use the correct engine ID or silently fall through to a wrong engine. Pin the ID check to `bpy.app.version` at script top.
- **Verify (solid):** Confirmed via Blender 4.2 Python API release notes (developer.blender.org) and Sketchfab plugin GitHub issues #141 and #161 which document the 4.2 and 5.0 identifier changes respectively. | cross-family (deepseek-v3.1): confirmed — Correctly documents the engine ID changes between versions, including the 5.0 reversion to BLENDER_EEVEE. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Blender 4.2 LTS: Python API — Blender Developer Documentation](https://developer.blender.org/docs/release_notes/4.2/python_api/) — Engine identifier changed to BLENDER_EEVEE_NEXT in 4.2 when EEVEE Legacy was removed. ; [FIX FOR BLENDER 4.2 — sketchfab/blender-plugin Issue #141](https://github.com/sketchfab/blender-plugin/issues/141) — Real-world breakage: plugin broke in 4.2 because BLENDER_EEVEE no longer existed; fix was switching to BLENDER_EEVEE_NEXT. ; [Blender 5.0: Python API — Blender Developer Documentation](https://developer.blender.org/docs/release_notes/5.0/python_api/) — Identifier changed back to BLENDER_EEVEE in 5.0 — BLENDER_EEVEE_NEXT is gone in 5.0+.

### Transparent background alpha PNG output for sprite rendering · `✅ solid` · Blender 4.2+
**Rendering sprites as RGBA PNG with transparent background requires two independent settings that must both be set: `film_transparent` on the render settings (makes the world background transparent) and `color_mode = 'RGBA'` on the image output settings (tells the file encoder to write the alpha channel). Missing either produces opaque output or a PNG with no alpha.**
- **How:** ```python
import bpy scene = bpy.context.scene # Engine (choose one)
scene.render.engine = 'BLENDER_EEVEE_NEXT' # or 'CYCLES' # ── Transparent background ──
scene.render.film_transparent = True # ── RGBA PNG output ──
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.image_settings.compression = 15 # 0–100; 15 = fast, reasonable size # ── Output path (use absolute path for headless safety) ──
scene.render.filepath = 'E:/sprites/frame_####' # ── Render ──
bpy.ops.render.render(write_still=True)
``` For animation/multi-frame (8-direction turnaround):
```python
# Set camera angle, then render single frame to named file
scene.render.filepath = f'E:/sprites/char_dir{direction:02d}_'
bpy.ops.render.render(write_still=True)
```
- **Gotchas:** `film_transparent = True` only makes the world/background transparent. If the mesh itself has opaque materials, those still render solid — expected.; EEVEE Next + transparent materials (alpha in shader): the old Blend Mode → Alpha Blend/Hashed is replaced by the new Render Method (Dithered = default, approximates Alpha Hashed). Dithered transparency at low sample counts has visible dither noise on sprite edges. Fix: raise `taa_render_samples` to 128+.; PNG color mode must be `'RGBA'` not `'RGB'` — 'RGB' writes a fully opaque file even with film_transparent ON.; EXR (OPEN_EXR_MULTILAYER) preserves more quality but compositing pipelines typically expect PNG sprites; stick with PNG + RGBA for game pipelines.; In headless mode, `render.filepath` must be an absolute path — relative paths using `//` work in interactive Blender but can resolve unpredictably in background mode depending on blend file location.
- **For Studio:** This is the core output configuration for every TRELLIS GLB → sprite frame. Set once in the pipeline script header. Use `####` in filepath for frame numbering if rendering animation frames per direction.
- **Verify (solid):** Confirmed via gachoki.com transparent PNG guide (tested in 4.x) and iRender 2026 transparent background article. film_transparent + RGBA PNG is a stable API unchanged since Blender 2.8. | cross-family (deepseek-v3.1): confirmed — Correctly identifies both film_transparent and RGBA color_mode as required for transparent PNG output. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Make Transparent PNGs In Blender: Quick Guide For Cycles & Eevee — Gachoki Studios](https://gachoki.com/how-to-render-transparent-png-images-in-blenders-cycles-and-eevee-render-engines/) — film_transparent + RGBA color_mode both required; code example confirmed working in 4.x. ; [How to Render With a Transparent Background in Blender (2026) — iRender Farm](https://medium.com/@irenderofficial/how-to-render-with-a-transparent-background-in-blender-stills-animation-and-glass-2026-5d112865b4e9) — Both settings confirmed still apply in 4.x; EEVEE Next and Cycles both support film_transparent.

### Cycles denoising: OptiX denoiser vs OpenImageDenoise (OIDN) · `▸ plausible` · Blender 4.2+
**Cycles produces noisy output at low sample counts; denoising is essential for fast sprite renders. Two main denoisers: OptiX (NVIDIA GPU, fastest on RTX hardware) and OpenImageDenoise/OIDN (Intel AI denoiser, CPU or GPU, more universally available). Choosing wrong means either slow CPU denoising or missing the GPU acceleration entirely.**
- **How:** ```python
scene = bpy.context.scene
scene.cycles.use_denoising = True # OptiX denoiser — fastest on NVIDIA RTX, requires OptiX compute device
scene.cycles.denoiser = 'OPTIX' # OR: OIDN — works on any GPU/CPU, enable GPU acceleration:
scene.cycles.denoiser = 'OPENIMAGEDENOISE'
# To run OIDN on GPU (4.x feature, much faster than CPU OIDN):
scene.cycles.denoising_use_gpu = True # property may vary; check bpy.types.CyclesRenderSettings
``` For RTX 5090 (OptiX supported):
- Use `denoiser = 'OPTIX'` + `compute_device_type = 'OPTIX'` together
- At 64–128 samples + OptiX denoise: high-quality sprite frames in seconds per frame For a safe universal fallback:
- `denoiser = 'OPENIMAGEDENOISE'` works on any hardware
- Enable GPU mode in OIDN if available in the Blender version
- **Gotchas:** If compute_device_type is set to CUDA but denoiser is set to OPTIX, Blender silently falls back to CPU OIDN — render stats will show CPU denoising, not GPU.; OIDN on CPU is dramatically slower than OIDN on GPU; always check that GPU OIDN is enabled if not using OptiX.; OptiX denoiser can produce slightly different (sometimes over-smoothed) results compared to OIDN; for pixel-art style sprites this can erase fine texture detail at small resolutions.; Blender 4.2 issue #125392 documents CUDA device type printing OPTIX denoising kernel reload messages multiple times per frame — known log noise, not a correctness bug.
- **For Studio:** For 256×256 or 512×512 sprite renders: use 64–128 samples + OptiX denoiser on the RTX 5090. This is the fastest Cycles path for clean output. If sprites look over-smoothed, lower denoiser strength or raise samples instead.
- **Verify (plausible):** Denoiser fallback behavior confirmed via Blender 4.2 issue tracker and SuperRenders guide. OIDN GPU mode documented in multiple 4.x guides. | cross-family (deepseek-v3.1): confirmed-with-fixes — Correct denoiser types but incorrect property for GPU acceleration - OIDN uses GPU automatically when available. [fix: denoising_use_gpu property doesn't exist; OIDN GPU acceleration is automatic when using GPU compute device] [confirmed by 1 of 1 juror(s) [confirmed-with-fixes]]
- **Sources:** [Blender Render Settings: Cycles & Eevee Guide (2026) — SuperRenders](https://superrendersfarm.com/article/blender-render-settings-optimization-guide) — OptiX denoiser requires OptiX compute device; CUDA compute + OptiX denoiser silently falls back to CPU OIDN. ; [How to Make Blender Cycles Render Faster — iRender Farm / Medium](https://medium.com/@irenderofficial/how-to-make-blender-cycles-render-faster-without-losing-quality-10-techniques-i-actually-use-b723d2681a91) — Enable GPU in OIDN subpanel — no reason to let CPU handle denoising while GPU sits idle. ; [#125392 — EEVEE Next 4.2.2: CUDA + OptiX denoising kernel reload messages](https://projects.blender.org/blender/blender/issues/125392) — Confirms CUDA + OptiX interaction in 4.2; known log spam, documented interaction between compute backend and denoiser selection.

### EEVEE Next: key render settings via bpy for headless batch renders · `▸ plausible` · Blender 4.2–4.4
**The Python-accessible settings on `scene.eevee` (a `SceneEEVEE` struct) that control quality and performance in EEVEE Next headless renders. Targets Blender 4.2–4.4.**
- **How:** ```python
import bpy scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' eevee = scene.eevee # --- Sampling (TAA) ---
# Final render sample count; higher = less aliasing/noise, linear time cost
# 64 is default; for stylized sprite work 32–64 often sufficient
eevee.taa_render_samples = 64 # --- Shadows ---
eevee.use_shadows = True
eevee.shadow_pool_size = '1024' # MB; increase if shadows drop out in heavy scenes
eevee.shadow_resolution_scale = 1.0 # 1.0 = full; 0.5 = half-res for speed
eevee.shadow_ray_count = 1 # 1–4; higher = softer contact shadows # --- GI / Ray tracing ---
# For fast sprite renders: disable raytracing for maximum throughput
eevee.use_raytracing = False
# When ON: controls indirect diffuse bounces
eevee.gi_diffuse_bounces = 3 # --- Ambient Occlusion ---
# Built-in GTAO; cheap and good for game-art look
eevee.use_gtao = True # --- Resolution ---
scene.render.resolution_x = 256
scene.render.resolution_y = 256
scene.render.resolution_percentage = 100
```
- **Gotchas:** `taa_render_samples` controls aliasing but not ray-traced noise (that is controlled by raytracing settings when `use_raytracing=True`). For opaque sprites 32 samples is typically clean enough.; `shadow_pool_size` is a string enum in the bpy API (values like '16', '32', '64', '128', '256', '512', '1024' in MB) — not an integer. Setting the wrong type causes a silent no-op.; In EEVEE Next the viewport sample count (`taa_samples`) and the render sample count (`taa_render_samples`) are separate; headless renders always use `taa_render_samples`.; Temporal reprojection (`use_taa_reprojection`) is a viewport-only feature and does nothing in background renders.
- **For Studio:** Set these at the top of the turnaround render script after opening the GLB/blend. `use_raytracing=False` + `taa_render_samples=64` gives clean fast frames for 256×256 sprite sheets. Raise samples if dithered transparency noise is visible on character edges.
- **Verify (plausible):** Property names confirmed against UPBGE SceneEEVEE API (mirrors upstream Blender API docs) and cross-checked with SuperRenders guide. | cross-family (deepseek-v3.1): confirmed-with-fixes — Most properties are correct but shadow_ray_count was renamed to shadow_ray_count_per_step in EEVEE Next. [fix: shadow_ray_count should be shadow_ray_count_per_step (actual property name in 4.2+)] [confirmed by 1 of 1 juror(s) [confirmed-with-fixes]]
- **Sources:** [SceneEEVEE(bpy_struct) — UPBGE/Blender Python API](https://upbge.org/docs/latest/api/bpy.types.SceneEEVEE.html) — taa_render_samples default 64, shadow_pool_size, shadow_resolution_scale, use_raytracing, gi_diffuse_bounces all confirmed as valid SceneEEVEE properties. ; [Blender Render Settings: Cycles & Eevee Guide (2026) — SuperRenders](https://superrendersfarm.com/article/blender-render-settings-optimization-guide) — taa_render_samples and Cycles equivalents documented with recommended values for production renders.

### Freestyle NPR introduction — hold-with-limit · `▸ plausible` · Blender 4.5 LTS
**Edge/line-based NPR silhouette/crease → Line Style.**
- **How:** Classic vector-line NPR; not GP strokes; keep 4.x pin (do not invent 5.x from latest URL).
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (plausible):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Freestyle NPR introduction — hold-with-limit](https://docs.blender.org/manual/en/latest/render/freestyle/introduction.html) — Freestyle NPR

### Blender 5.0 core logging rewrite · `?` · Blender 4.x
**Background render progress uses unified logger; --debug-cycles → --log cycles; farm parsers that scrape old stdout must update.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Blender 5.0 core logging rewrite](https://developer.blender.org/docs/release_notes/5.0/core/) — logging scrape break

### Blender 5.0 product notes — pin version · `?` · Blender 4.x
**Recaps 5.0 color-management/HDR overhaul and EEVEE/Cycles changes; pipeline must pin a version explicitly.**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Pin 4.x; x recipes or silent KB flip.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Blender 5.0 product notes — pin version](https://www.blender.org/download/releases/5-0/) — pin version; no silent flip

### Blender 5.0 release notes — major compat (pin 4.x) · `?` · Blender 4.x
**Major 5.0 shipped Nov 18 2025 with listed compatibility breaks; not a silent 4.x patch. Pin turnaround to named 4.x (4.2+/4.5 LTS).**
- **How:** See source URL; STUDY-003 Verifier-verified finding.
- **Gotchas:** Invented 5.x recipes: 0.
- **For Studio:** Headless turnaround / batch craft currency for Blender 4.x.
- **Verify ():** STUDY-013 from STUDY-003 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Blender 5.0 release notes — major compat (pin 4.x)](https://developer.blender.org/docs/release_notes/5.0/) — 5.0 = major break; pin 4.x

