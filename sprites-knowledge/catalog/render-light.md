# Render & lighting
_Blender headless render: camera-parented rig, color-management/tonemap per character value, render passes, outline/toon._ · wave 5 · 2026-09-07 · [‹ catalog index](README.md)

9 recipes · 7 recommended · 3 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 1 | Blender 5.0.1 headless 8-direction camera-parented light rig | blender | game-sprite | ▣ measured | ✅ yes | 5 | 5 | · |
| 1 | Studio HDRI ambient fill (Studio Kontrast 04, CC0) | blender | game-sprite | ▣ measured | ✅ yes | 5 | 4 | · |
| 1 | Tonemap per character value: AgX for dark, Standard for bright | blender | game-sprite | ▣ measured | ✅ yes | 5 | 5 | · |
| 2 | Blender headless multi-direction render rig (--background + --python) | blender | game-sprite | ▸ reproduced | ✅ yes | 5 | 5 | · |
| 2 | Color-management discipline: Standard/Raw (not AgX) for sprite albedo | blender | both | ▸ reproduced | ✅ yes | 5 | 5 | · |
| 2 | Inverse-hull (backface solidify) outline for toon sprites | blender | both | ▸ reproduced | ✅ yes | 5 | 5 | · |
| 2 | Normal / depth / AO passes for in-engine sprite re-lighting | blender | both | ▸ reproduced | ✅ yes | 5 | 5 | · |
| 9 | Diffusers ControlNet overview | blender | sprites | docs | check | 4 | 4 | · |
| 10 | Freestyle / Grease-Pencil Line Art outline pass | blender | both | · community | ✅ yes | 4 | 4 | · |

## Detail

### Blender 5.0.1 headless 8-direction camera-parented light rig · `recommended` · ▣ measured
**A camera-parented 3-point + shadowless lens-fill rig orbiting with an ortho camera gives 8 identically-lit directional renders; runs unmodified on Blender 5.0.1.**
render_views.py imports the GLB, builds an ORTHO camera at pitch 30 parented to an orbit pivot, and parents Key/Fill/Rim Area lights + a shadowless camera-coincident LensFill to the camera so every yaw step is lit identically. Energies auto-scale with size^2. EEVEE, film_transparent, 8 yaws (front..front_left). Verified the bpy API on Blender 5.0.1: engine enum 'BLENDER_EEVEE' is valid in 5.0 (EEVEE-Next reclaimed that id; 'BLENDER_EEVEE_NEXT' is gone), AgX/gamma/exposure/glTF-import/Area-light-shadow all present.
- **For the pipeline:** Blender 5.0.1 is the studio's sprite renderer (installed at E:/AI-Models/blender-5.0.1-windows-x64). The camera-parented rig is the fix for dark back/side views. Render in Blender (commercial-clean) — never nvdiffrast.
- **Engine:** blender · **Applies to:** game-sprite · **Base:** n/a · **Kind:** technique
- **Validated under:** Blender 5.0.1 headless on RTX 5090; 8 views ~7s; API probed 2026-06-07.
- **Output license:** commercial **yes** (license: Blender is GPL; rendered output is yours (commercial-clean))
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| pitch | 30 deg | ○ | camera elevation for 2.5D JRPG read |
| ortho_scale | size*1.3 | ○ | frames the normalized TRELLIS mesh |
| lights | Key/Fill/Rim + shadowless LensFill | ○ | energies auto-scale size^2; LensFill prevents black silhouettes in EEVEE (no GI) |

- **Verify:** no external verdict — not checked
- **Sources:** [render_views.py (trellis-sprite-pipeline)](https://github.com/mcp-tool-shop-org/trellis-sprite-pipeline) — The camera-parented 8-direction render rig. ; [Blender 5.0 Python API (color management, EEVEE)](https://docs.blender.org/api/current/) — view_settings.view_transform + EEVEE engine enum.

### Studio HDRI ambient fill (Studio Kontrast 04, CC0) · `recommended` · ▣ measured
**A CC0 studio HDRI gives better directional form than flat-gray ambient; the flat-ambient fallback still works for a first look.**
render_views.py loads an environment HDRI (Studio Kontrast 04, Poly Haven, CC0) at strength 0.8 and rotates it with camera yaw for direction-independent fill; falls back to flat gray (strength 3.0) if absent. The HDRI improves shadow/form modeling but, being a bright neutral studio map, adds little saturation to an already-light subject. Installed at E:/AI-Models/hdri/studio_kontrast_04_4k.exr (path fixed F:->E: in render_views.py).
- **For the pipeline:** Use the HDRI for delivery-quality form; it is commercial-clean (CC0) and input-only. For punch, pair with the Standard tonemap (above), not just brighter light.
- **Engine:** blender · **Applies to:** game-sprite · **Base:** n/a · **Kind:** technique
- **Validated under:** Rendered with + without HDRI, looked-at on the rig 2026-06-07.
- **Output license:** commercial **yes** (license: CC0 (Poly Haven))
- **Fit:** rig 5/5 · studio 4/5
- **Verify:** no external verdict — not checked
- **Sources:** [Poly Haven — Studio Kontrast 04 (CC0 HDRI)](https://polyhaven.com/a/studio_kontrast_04) — CC0-licensed studio HDRI used for ambient fill.

### Tonemap per character value: AgX for dark, Standard for bright · `recommended` · ▣ measured
**AgX + raised exposure washes out bright/light characters; Standard (or Filmic) + exposure 0 restores their saturation. Choose the view transform per character value.**
render_views.py defaulted to AgX view transform + view-exposure 1.5 (chosen to lift dark back textures off black). On a bright silver-armored character that overshoots into a chalky, desaturated look. A 4-way A/B (AgX+1.5 / AgX+0 / Standard+0 / Filmic+0) on the same render showed the colors are fully present in the texture — AgX+exposure was the wash. Standard+0 restored real metallic contrast + warm accents, closest to the SDXL source. Added a --view-transform CLI flag.
- **For the pipeline:** Expose view_transform as a per-character knob: dark-armored villains keep AgX+1.5 (rescues dark backs from black); bright/light characters use Standard or Filmic at exposure 0. A light saturation/levels pass is the final polish (TRELLIS bakes albedo a touch flatter than the input).
- **Engine:** blender · **Applies to:** game-sprite · **Base:** n/a · **Kind:** technique
- **Validated under:** 4-variant render compared + looked-at on the rig 2026-06-07.
- **Output license:** commercial **yes** (license: n/a)
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Sprites look washed-out / chalky / desaturated | AgX view transform + raised exposure desaturates highlights on a bright subject | --view-transform Standard --view-exposure 0 (Filmic for a middle ground) |  |

- **Verify:** no external verdict — not checked
- **Sources:** [Blender AgX / Standard view transforms](https://docs.blender.org/manual/en/latest/render/color_management/index.html) — AgX is a filmic transform that desaturates toward white; Standard is linear-to-sRGB.

### Blender headless multi-direction render rig (--background + --python) · `recommended` · ▸ reproduced
**Blender renders any number of fixed camera directions to PNG with zero GUI, driven entirely by a Python script over the CLI — the load-bearing automation layer of a sprite studio.**
Run `blender -b scene.blend -P rig.py` (or `--background... --python`) on a server/headless box; the Python script rotates the camera (or a parent empty) through N compass directions, sets the orthographic camera and output path per direction, and triggers a still or animation render. Render args (-f frame, -a animation) must be the LAST CLI arguments; -o sets output, -E sets engine, -s/-e set frame start/end. Sprite sheets are assembled afterward (ImageMagick montage) since Blender has no native sheet packer. Tools like yuki-koyama/blender-cli-rendering and oqton/blenderless wrap this pattern for batch multi-view output.
- **Engine:** blender · **Applies to:** game-sprite · **Base:** n/a · **Kind:** workflow
- **VRAM:** 2-8 (geometry/sample dependent; EEVEE Next far lighter than Cycles)
- **Output license:** commercial **yes** (license: Blender GPLv2+ (output unrestricted); wrappers GPLv3 / permissive) — Blender is GPLv2+ software, but rendered IMAGE OUTPUT carries no copyleft obligation — you own your sprites outright and may sell them commercially. No model license inheritance applies here (this is deterministic rendering, not a diffusion model). Wrapper repos: blender-cli-rendering is GPLv3, blenderless is permissive — but again only matters if you redistribute their CODE, not your renders.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| render flag position | -f / -a must be last | ○ | Blender ignores output options set after the render trigger; classic gotcha reported on Blender Artists |
| camera type | orthographic | ○ | kills perspective skew across directions so foot anchor stays stable |
| directions | 8 (or 4/16) | ○ | rotate a parent empty in fixed increments; keep the model still so rigging stays valid |
| engine | EEVEE Next (-E BLENDER_EEVEE_NEXT) or Cycles | ○ | EEVEE Next is realtime-fast for flat sprite albedo; Cycles for AO/GI passes |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Output options ignored, files land in /tmp | -o or format set AFTER -f/-a on the command line | Put all output/scene flags before the render trigger; verify with a 1-frame dry run |  |
| Directions drift / sprite jitters between angles | rotating the mesh instead of the camera, or perspective camera | Parent camera to an empty, rotate the empty; use orthographic; lock the model transform |  |

- **Verify:** Both sources resolve (200). Blender manual confirms verbatim: 'we do not need a graphical display (no need for X server on Linux)', 'render via a remote shell (typically SSH)', and 'Always position -f or -a as the last arguments.' yuki-koyama/blender-cli-rendering exists, is a set of Blender Python CLI-rendering scripts (--background + --python pattern), licensed GPL-3.0 — matches 'GPLv3' claim. Blender output unrestricted is correct. License/commercial_use accurate. [no external verdict — not checked]
- **Sources:** [Rendering From The Command Line — Blender Manual](https://docs.blender.org/manual/en/latest/advanced/command_line/render.html) (Blender Foundation, 2025) — Command-line rendering needs no graphical display and can run over SSH; the -f and -a render arguments must be positioned as the last arguments. ; [yuki-koyama/blender-cli-rendering](https://github.com/yuki-koyama/blender-cli-rendering) (Yuki Koyama, 2021) — Provides Blender Python scripts that render images directly from the CLI, demonstrating the --background + --python automation pattern reusable for multi-direction sprite rigs.

### Color-management discipline: Standard/Raw (not AgX) for sprite albedo · `recommended` · ▸ reproduced
**AgX became Blender's default in 4.0 and tone-maps/desaturates flat graphics — for sprite albedo you must switch the view transform to Standard (or Raw for data passes) or your palette shifts before quantization even starts.**
Blender 4.0 replaced Filmic with AgX as the default view transform. AgX is a sigmoid film-emulation curve that rolls highlights toward white and is great for photoreal renders but actively harmful for flat 2D/graphic/albedo work — it desaturates and skews the exact colors you want to feed a limited palette. For sprite color masters, render with the Standard view transform; for any DATA pass (normals, depth, masks) use Raw so no curve is applied at all. Getting this wrong means every later step (palette extraction, quantization, engine tint) inherits a wrong-color source.
- **Engine:** blender · **Applies to:** both · **Base:** n/a · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: n/a (technique); Blender GPLv2+ output unrestricted) — Configuration choice in GPL Blender; output unrestricted.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| view transform (color master) | Standard | ○ | no film curve; albedo colors stay true for palette work |
| view transform (data passes) | Raw | ○ | no transform at all — required for normals/depth/masks |
| what NOT to use | AgX / Filmic | ○ | sigmoid curves desaturate & skew flat graphics |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Sprite colors look muddy/desaturated vs material preview | AgX default view transform applied on output | Switch Render Properties > Color Management > View Transform to Standard |  |
| Bright hero costume colors clip to neon or white | Standard sRGB blows out very bright values; or AgX rolls them off | Keep emission/values in valid 0-1 range; light flatter for sprite albedo |  |

- **Verify:** Both sources resolve (200). Blender 4.0 release notes confirm verbatim: 'AgX view transform has been added, and replaces Filmic as the [default]... new files; Standard and Filmic remain available.' Blendergrid confirms view transforms only affect display/output, not the linear render. The 'Standard/Raw for albedo' guidance is the entry's own inference; core verifiable claims confirmed. No license concern. [no external verdict — not checked]
- **Sources:** [Color Management — Filmic / AgX (Blender 4.0 release notes)](https://developer.blender.org/docs/release_notes/4.0/color_management/) (Blender Foundation, 2023) — AgX view transform was added and replaces Filmic as the default in new files; Standard and Filmic remain available. ; [Understanding Color Management in Blender](https://blendergrid.com/articles/color-management-in-blender) (Blendergrid, 2024) — View transforms only affect display/output and not the linear render; Standard/Raw are appropriate when you need un-tone-mapped flat or data imagery.

### Inverse-hull (backface solidify) outline for toon sprites · `recommended` · ▸ reproduced
**A Solidify modifier with flipped backface normals and a black emission material gives a controllable, render-cheap outline that survives downscaling better than post-process line filters.**
Duplicate the mesh (or add a Solidify modifier set to render backfaces only), invert normals, assign a flat black emission shader, and push the shell outward along normals. Because the outline is real geometry it is resolution-independent and consistent per direction — ideal for a turnaround where every angle must read identically. Line weight is set by shell thickness; it scales cleanly when the 512px master is downsampled to 48/64px. Compared to Freestyle/Line Art it is faster (no separate line pass) and engine-portable, at the cost of weaker handling of interior detail lines.
- **Engine:** blender · **Applies to:** both · **Base:** n/a · **Kind:** technique
- **VRAM:** negligible over base render
- **Output license:** commercial **yes** (license: n/a (technique); Blender GPLv2+ output unrestricted) — Pure geometry/shader technique inside Blender — rendered sprites are unrestricted for commercial sale. No third-party asset license involved.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| outline source | Solidify modifier, render backfaces | ○ | or duplicate mesh + flip normals |
| material | flat black Emission | ○ | avoids shading on the outline; reads as ink line |
| thickness | tuned for target px | ○ | thin enough that a 512->64px Lanczos pass keeps ~1px line |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Outline vanishes or doubles on thin geometry | shell thickness larger than feature; concave normals | Reduce thickness on small parts; use weighted-normals or per-vertex thickness |  |
| Outline inconsistent between turnaround angles | screen-space line filter used instead of geometry shell | Use the geometry inverse-hull (resolution/angle independent) rather than a compositor edge filter |  |

- **Verify:** Both sources resolve (200). Blender Artists thread confirms inverted-hull/Solidify, Freestyle (post-process), and game-engine context (16 'inverted hull', 36 'freestyle', 15+3 'game engine', 3 'post-process' mentions). Rogo Digital confirms the solidify/backface inverse-hull as geometry-based real-time outline. Technique entry; no license concern (Blender output unrestricted). [no external verdict — not checked]
- **Sources:** [What's the best outline for toon/anime — Freestyle vs inverted hull vs another method](https://blenderartists.org/t/whats-the-best-outline-for-toon-anime-freestyle-vs-inverted-hull-method-vs-another-method-in-2-9/1278907) (Blender Artists community, 2021) — Inverted-hull uses the Solidify modifier to create real-time cartoon outlines and is the method game engines favor, while Freestyle is a post-process render pass. ; [Create a Cartoon Outline for Any Object](https://rogodigital.design/tutorials/create-a-cartoon-outline-for-any-object/) (Rogo Digital, 2023) — Demonstrates the solidify/backface inverse-hull outline as a geometry-based, resolution-independent cartoon line method.

### Normal / depth / AO passes for in-engine sprite re-lighting · `recommended` · ▸ reproduced
**Rendering a flat (unlit) albedo plus a world-space normal pass (and optional depth + AO) lets the game engine dynamically light 2D sprites — the foundation of modern 2.5D look.**
Set an orthographic camera looking straight down/forward, render an unlit color/albedo pass, and a separate normal pass. Critical: the normal pass must be exported with color management OFF (Raw / Standard, not AgX) or the vectors get tone-mapped and break; encode as 16-bit RGBA PNG for precision, and invert the green channel to match Godot/most-engine tangent-space conventions. Normals come out in WORLD space and depend on camera orientation, so the camera angle is part of the contract. Add depth and AO passes from Cycles for parallax/contact shadows. The engine then combines albedo + normal + light positions for real-time shading per sprite.
- **Engine:** blender · **Applies to:** both · **Base:** n/a · **Kind:** technique
- **VRAM:** Cycles AO/normal: 4-10 depending on scene
- **Output license:** commercial **yes** (license: n/a (technique); Blender GPLv2+ output unrestricted) — Native render passes; output unrestricted commercially.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| color management on normal pass | Raw / OFF | ○ | AgX/Filmic tone-maps the vectors and corrupts the map |
| bit depth | 16-bit RGBA PNG | ○ | 8-bit banding shows as lighting steps in-engine |
| green channel | invert for Godot/OpenGL convention | ○ | DirectX-convention engines keep it; pick per target engine |
| normal space | world/global | ○ | camera-above orthographic setup is required for the encoding to be valid |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| In-engine lighting looks inverted/wrong on Y | green-channel convention mismatch (OpenGL vs DirectX) | Flip the green channel to match the target engine |  |
| Normal map looks washed/pastel | AgX/Filmic view transform applied to the normal pass | Set color management to Raw/Standard for the normal output node |  |

- **Verify:** Both sources resolve (200). Kodera Games confirms all specifics: orthographic top-down camera, unlit color pass + world-space normal pass, color management disabled, green-channel inversion for Godot, 16-bit RGBA transparent PNG. EEVEE developer docs confirm NORMAL (PASS_POST_NORMAL), DEPTH, and AO render passes exist. Technique; no license concern. [no external verdict — not checked]
- **Sources:** [Render sprites with normal maps in Blender](https://games.kodera.pl/dev/render-sprites-with-normal-maps-in-blender/) (Kodera Games, 2020) — Use an orthographic top-down camera and export an unlit color pass plus a world-space normal pass with color management disabled and green channel inverted for Godot, as 16-bit RGBA PNG. ; [Render Passes (EEVEE) — Blender Developer Docs](https://developer.blender.org/docs/features/eevee/render_passes/) (Blender Foundation, 2025) — Blender exposes world-space surface normal, depth/Z, and ambient-occlusion as separate render passes usable for downstream re-lighting.

### Diffusers ControlNet overview · `situational` · docs
**ControlNet adds spatial conditioning (pose/edges/depth) to frozen T2I; control image + controlnet_conditioning_scale.**
ControlNet adds spatial conditioning (pose/edges/depth) to frozen T2I; control image + controlnet_conditioning_scale.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Diffusers ControlNet overview](https://huggingface.co/docs/diffusers/en/api/pipelines/controlnet) — ControlNet adds spatial conditioning (pose/edges/depth) to frozen T2I; control image + controlnet_conditioning_scale.

### Freestyle / Grease-Pencil Line Art outline pass · `situational` · · community
**Freestyle (or the newer Grease Pencil Line Art modifier) produces hand-drawn-looking edge lines as a render pass, with crease/silhouette/contour control the inverse-hull cannot give — at higher render cost.**
Enable Freestyle in render settings (or attach a Line Art modifier to a Grease Pencil object pointing at the mesh) to extract silhouette, crease, border, and material edges as vector-quality lines. Line Art is the modern, editable successor — non-destructive, modifier-stackable, and previewable in viewport — whereas Freestyle is an older post-process. Better than inverse-hull for interior detail lines and variable line weight; worse for raw throughput because it adds a pass and can fight 2D plane assets. For a JRPG turnaround it shines on hero close-ups; for tiny 48px walk-cycle frames the inverse-hull is usually enough.
- **Engine:** blender · **Applies to:** both · **Base:** n/a · **Kind:** technique
- **VRAM:** small added pass cost
- **Output license:** commercial **yes** (license: n/a (technique); Blender GPLv2+ output unrestricted) — Native Blender feature; rendered output unrestricted for commercial use.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| method | Grease Pencil Line Art modifier (preferred) or Freestyle | ○ | Line Art is editable + modifier-compatible |
| edge types | silhouette + crease + material border | ○ | tune crease angle to control interior line density |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Lines flicker frame-to-frame in animation | Freestyle re-evaluates per frame with sub-pixel instability | Prefer Line Art (more stable), bake at higher res then downscale, or thicken lines |  |
| Slow renders on dense meshes | Freestyle stroke computation scales with edge count | Use Line Art with edge-type filtering; reserve for hero frames |  |

- **Verify:** Both sources resolve (200). Blender Artists thread confirms Line Art (Grease Pencil) as newer editable/modifier-compatible approach (6 'Line Art' mentions) and Freestyle as post-process render pass. Blender manual passes.html confirms Freestyle render pass exists (3+ Freestyle, plus Normal/Z/Mist/AO passes). Technique; no license concern. [no external verdict — not checked]
- **Sources:** [Outline method comparison thread (Freestyle / inverted hull / Line Art)](https://blenderartists.org/t/whats-the-best-outline-for-toon-anime-freestyle-vs-inverted-hull-method-vs-another-method-in-2-9/1278907) (Blender Artists community, 2021) — Line Art (Grease Pencil) is the newer approach, working like Freestyle but editable and modifier-compatible; Freestyle is a post-process render pass. ; [Passes / Render Layers — Blender Manual](https://docs.blender.org/manual/en/latest/render/layers/passes.html) (Blender Foundation, 2025) — Blender exposes outline/edge and other data as render passes that can be composited or exported separately from the color pass.

