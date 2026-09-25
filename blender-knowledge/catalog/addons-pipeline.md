# Add-ons & ecosystem
_The 4.2 Extensions platform, bundled pipeline add-ons, the bpy add-on API, enabling add-ons headlessly, and the GPL licensing caveat for shipped add-ons._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

17 recipes · 15 solid.

| Recipe | Blender | Currency | ✓ | What |
|--------|-------|----------|---|------|
| Autodesk Bifrost — build/modify graphs | 4.5 LTS | ✅ solid | · | Left-to-right typed procedural graph for geometry compounds. |
| Blender 4.2 Extensions platform — what changed | 4.2+ (extensions platform GA); 4.1 and earlier use the old Add-ons panel | ✅ solid | ✓ | Blender 4.2 LTS (July 2024) replaced the old Add-ons section in Preferences with |
| Bundled pipeline add-ons in Blender 4.2 — what moved where | 4.2+ for the split; Node Wrangler on extensions.blender.org requires 4.2.0 minimum | ✅ solid | ✓ | Several workflow-critical add-ons changed status in Blender 4.2. glTF 2.0 and OB |
| Enabling add-ons headlessly in --background --python scripts | addon_utils.enable() works in 4.x (same API as 3.x). blender --command extension install-file is 4.2+ only. | ✅ solid | ✓ | When Blender runs in headless mode (blender --background --python script.py), ad |
| Flamenco job types / manager blenderArgs -b | 4.5 LTS | ✅ solid | · | Studio render manager compiles Blend jobs with -b. |
| Flamenco manager configuration | 4.5 LTS | ✅ solid | · | Manager config for Flamenco workers/jobs. |
| GPL licensing caveat — what it means for a studio using or shipping add-ons | All Blender versions — GPL has applied since Blender went open-source | ✅ solid | ✓ | Any Python file that imports bpy is legally a derivative work of Blender (GPL-2. |
| GenioPlus — 8-dir turntable sprite analog | 4.5 LTS | ✅ solid | · | 8-direction sprite sheets; camera orbits. |
| Houdini SOP networks — procedural graph analog | 4.5 LTS | ✅ solid | · | Wired procedural geometry graph generate→modify→display. |
| Pixar Tractor tractor-spool -c | 4.5 LTS | ✅ solid | · | Spool a single CLI command to farm blades. |
| Substance 3D Designer — graph view | 4.5 LTS | ✅ solid | · | Node graph + exposed params → reusable SBSAR. |
| Thinkbox Deadline — SubmitCommandLineJob | 4.5 LTS | ✅ solid | · | Farm wraps headless executable + frame range into tasks. |
| Vector vs raster in game art — Sunstrike | 4.5 LTS | ✅ solid | · | Author vector, export bitmaps/sprite sheets/SDF. |
| blender_manifest.toml — the extension manifest format | 4.2+ only — blender_manifest.toml is not read by Blender 4.1 or earlier | ✅ solid | ✓ | Extensions in Blender 4.2+ are described by a blender_manifest.toml file in the  |
| bpy add-on API: register/unregister and the minimal operator pattern | 4.x (pattern unchanged from 3.x; bl_info optional when manifest present in 4.2+) | ✅ solid | ✓ | Blender add-ons and extensions both use the same bpy Python API internally. An _ |
| Studio distribution: local extension repository + portable Blender build | Local repository support: Blender 4.2+. Portable builds + BLENDER_USER_RESOURCES: all Blender 3.x/4.x | ▸ plausible | ✓ | Blender 4.2 introduces support for custom (local) extension repositories — a dir |
| Useful current extensions for a game-asset batch pipeline | All listed target Blender 4.2+; ACT also supports 3.x | ▸ plausible | · | As of 2025-2026, extensions.blender.org hosts several verified game-pipeline add |

## Detail

### Autodesk Bifrost — build/modify graphs · `✅ solid` · Blender 4.5 LTS
**Left-to-right typed procedural graph for geometry compounds.**
- **How:** Adjacent DCC graph craft; ≠ Realize Instances→glTF sprite bake.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Autodesk Bifrost — build/modify graphs](https://help.autodesk.com/cloudhelp/2026/ENU/Bifrost-Common/files/Bifrost_Common_build_a_graph_html.html) — Bifrost graph analog

### Blender 4.2 Extensions platform — what changed · `✅ solid` · Blender 4.2+ (extensions platform GA); 4.1 and earlier use the old Add-ons panel
**Blender 4.2 LTS (July 2024) replaced the old Add-ons section in Preferences with an Extensions section and launched extensions.blender.org as the official distribution hub. Extensions use a blender_manifest.toml file instead of (or alongside) the old bl_info dict. The old bundled add-ons were split: functionality promoted to Blender core (e.g., some Cycles nodes), popular ones migrated to extensions.blender.org as individual installs, and the rest shipped as a downloadable 'Legacy Add-ons Bundle'. Any pre-4.2 install guide that says 'drop a.py or.zip into the add-ons folder via Preferences > Add-ons > Install' is now stale — the UI path is Preferences > Extensions > Install from Disk.**
- **How:** Interactive install from extensions.blender.org: open Preferences > Extensions, allow online access, browse or search, click Get. Drag-and-drop from the website into Blender also works in 4.2+. Install from disk (local.zip extension): Preferences > Extensions > dropdown arrow (⌄) > Install from Disk. Legacy add-ons bundle (for offline/airgapped studios): download the separate legacy.zip from blender.org downloads, then Preferences > Extensions > ⌄ > Install Legacy Add-on.
- **Gotchas:** Pre-4.2 guides reference 'Preferences > Add-ons > Install' — that UI is gone in 4.2+.; Online access must be explicitly granted the first time; airgapped machines need the legacy bundle or local repo.; The 'Legacy Add-ons Bundle' is a separate download, not bundled in the main 4.2 installer.; Extensions require blender_manifest.toml; legacy add-ons still use bl_info — mixing them in the same file is possible but the manifest takes precedence on 4.2+.
- **For Studio:** For a headless pipeline, pre-install extensions into a portable Blender build before shipping; avoid relying on online access at render-time. Use a local directory repository (custom repo in Extensions prefs) to distribute studio extensions to all workstations without internet dependency.
- **Verify (solid):** Confirmed via extensions.blender.org/about/, code.blender.org blog (May 2024 beta release), and devtalk.blender.org bundling thread. | cross-family (deepseek-v3.1): confirmed — Correctly describes the 4.2 Extensions platform replacement of the old Add-ons panel and the new installation workflows. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Extensions Platform Beta Release — Blender Developers Blog](https://code.blender.org/2024/05/extensions-platform-beta-release/) — Extensions platform went GA in Blender 4.2 LTS; describes install flow and bundling changes ; [Changes to Add-on and Themes Bundling (4.2 onwards) — Developer Forum](https://devtalk.blender.org/t/changes-to-add-on-and-themes-bundling-4-2-onwards/34593) — Official thread detailing which add-ons were removed from core, how the legacy bundle works ; [Get Extensions — Blender 5.1 Manual](https://docs.blender.org/manual/en/latest/editors/preferences/extensions.html) — Current install flow, online access requirement, Install from Disk path

### Bundled pipeline add-ons in Blender 4.2 — what moved where · `✅ solid` · Blender 4.2+ for the split; Node Wrangler on extensions.blender.org requires 4.2.0 minimum
**Several workflow-critical add-ons changed status in Blender 4.2. glTF 2.0 and OBJ importers are now native (compiled C) — no enable needed, always available. FBX import/export remains a Python add-on bundled with Blender core, enabled by default. Node Wrangler moved from bundled to extensions.blender.org (install separately in 4.2+). 'Import Images as Planes' similarly moved to extensions.blender.org. The 'legacy add-ons bundle' (separate download from blender.org) contains most of the other previously-bundled add-ons for users who need them.**
- **How:** glTF 2.0 (native in 4.2+): always available, no enable required. Access via File > Import/Export > glTF 2.0 (.glb/.gltf). Headless: bpy.ops.export_scene.gltf() directly. FBX: bundled, enabled by default. Headless: bpy.ops.export_scene.fbx(). Node Wrangler (4.2+): must be installed from extensions.blender.org or the legacy bundle. After install: addon_utils.enable('node_wrangler', persistent=True) in headless scripts. Node Wrangler adds Ctrl+Shift+Click (viewer node) and Ctrl+T (texture setup) shortcuts — not relevant headlessly, but its batch texture-setup can be scripted. Import Images as Planes (4.2+): now on extensions.blender.org. Headless use: enable via addon_utils then bpy.ops.import_image.to_plane(). Useful for sprite-sheet plane setup in batch.
- **Gotchas:** Node Wrangler is NOT included in the standard Blender 4.2 install — users upgrading from 4.1 lose it unless they install the legacy bundle or grab it from extensions.blender.org.; The glTF exporter changed from Python to native C in 4.x; bpy.ops.export_scene.gltf() still works but some bl_info-based detection scripts checking for the old module name 'io_scene_gltf2' may behave differently.; The legacy add-ons bundle is a point-in-time snapshot; it will NOT receive updates — extensions.blender.org versions will be maintained going forward.; Some add-ons from the legacy bundle conflict with their extensions.blender.org counterpart if both are installed; uninstall the legacy version first.
- **For Studio:** For a game-asset headless pipeline: glTF and FBX work out of the box. Node Wrangler is primarily interactive (keyboard shortcuts) — skip enabling it headlessly unless scripting its batch PBR setup. Import Images as Planes is useful for sprite/billboard batch setup.
- **Verify (solid):** Node Wrangler extensions.blender.org status confirmed (extensions.blender.org/add-ons/node-wrangler/versions/). glTF native status confirmed via multiple 4.2 release notes references. | cross-family (deepseek-v3.1): confirmed — Correct description of the 4.2 add-on restructuring with glTF becoming native and Node Wrangler moving to extensions. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Node Wrangler Version History — Blender Extensions](https://extensions.blender.org/add-ons/node-wrangler/versions/) — Node Wrangler on extensions.blender.org, requires Blender 4.2+, GPL-2.0-or-later ; [Import Images as planes — Extension? — Blender Artists](https://blenderartists.org/t/import-images-as-planes-extension/1616331) — Community confirmation that Import Images as Planes moved to extensions.blender.org in 4.2 ; [Changes to Add-on and Themes Bundling (4.2 onwards) — Developer Forum](https://devtalk.blender.org/t/changes-to-add-on-and-themes-bundling-4-2-onwards/34593) — Official list of what moved where in the 4.2 bundling restructure

### Enabling add-ons headlessly in --background --python scripts · `✅ solid` · Blender addon_utils.enable() works in 4.x (same API as 3.x). blender --command extension install-file is 4.2+ only.
**When Blender runs in headless mode (blender --background --python script.py), add-ons and extensions are NOT auto-enabled from user preferences unless prefs were saved with them enabled. For pipeline scripts that need an add-on's operators/functions, you must enable it programmatically in the script itself. Two approaches: addon_utils.enable() (session-only, does not modify saved prefs) or bpy.ops.preferences.addon_enable() + bpy.ops.wm.save_userpref() (persistent). For pre-installed extensions (4.2+), the same addon_utils API works.**
- **How:** Session-only enable (preferred for headless — no prefs mutation):
```python
import addon_utils
# Enable by module name (for legacy add-ons: the module filename without.py)
addon_utils.enable("io_scene_gltf2", default_set=False, persistent=True)
# persistent=True keeps it enabled across bpy.ops.wm.open_mainfile() calls in the same session
``` Persistent enable (write to prefs — use for initial setup, not per-render):
```python
bpy.ops.preferences.addon_enable(module="io_scene_gltf2")
bpy.ops.wm.save_userpref()
``` Install + enable a.zip add-on headlessly (legacy method, still works in 4.2):
```python
bpy.ops.preferences.addon_install(filepath="/path/to/addon.zip")
bpy.ops.preferences.addon_enable(module="addon_module_name")
bpy.ops.wm.save_userpref()
# Run as: blender --background --python install_addon.py -- /path/to/addon.zip
``` For Blender 4.2 extensions installed from disk, install with:
```
blender --command extension install-file -r user_default --enable studio_batch_exporter-1.0.0.zip
```
The `-r user_default` specifies the local repository (use `blender --command extension repo-list` to see available repos).
- **Gotchas:** addon_utils.enable() without persistent=True will disable the add-on when bpy.ops.wm.open_mainfile() is called — always pass persistent=True for pipeline scripts that open .blend files.; bpy.ops.preferences.addon_enable() requires an operator context; in a headless script at module level this is usually fine, but if called inside a modal or from a non-context thread it fails.; The module name for addon_utils is the Python module name (directory or .py filename), NOT the display name. For extensions in 4.2+, it is the extension id from blender_manifest.toml.; bpy.context.preferences.addons[module_name] raises KeyError if the add-on was enabled with addon_utils (session-only) but not written to prefs.; blender --background without --factory-startup loads saved user prefs; if prefs have the add-on enabled, it loads automatically without any Python call needed.
- **For Studio:** The recommended headless pattern: pre-configure a studio Blender build with all extensions pre-enabled and prefs saved; pipeline scripts then run without any addon_enable() boilerplate. For dynamic per-script add-on loading, use addon_utils.enable(module, persistent=True) at the top of the script before any other bpy calls.
- **Verify (solid):** Pattern confirmed by Blender developer tracker (T66924), Preferences Operators API docs (bpy.ops.preferences), and a real headless install script from HuggingFace StdGEN space. | cross-family (deepseek-v3.1): confirmed — Accurate headless enable patterns using addon_utils.enable() and the persistent enable methods. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [bpy.ops.preferences — Blender Python API](https://docs.blender.org/api/current/bpy.ops.preferences.html) — addon_enable() and addon_install() operator signatures ; [Headless addon install script (StdGEN / HuggingFace)](https://huggingface.co/spaces/hyz317/StdGEN/blame/6f8045fd0df8fbc08cf155b13232481af379c9e4/blender/install_addon.py) — Working headless install pattern: addon_install + addon_enable + save_userpref via --background --python ; [Extensions Command Line Arguments — Blender Manual](https://docs.blender.org/manual/en/latest/advanced/command_line/extension_arguments.html) — blender --command extension install-file syntax for 4.2+

### Flamenco job types / manager blenderArgs -b · `✅ solid` · Blender 4.5 LTS
**Studio render manager compiles Blend jobs with -b.**
- **How:** Offline batch of turnaround blends; limit: shared-storage≠orbit logic.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Flamenco job types / manager blenderArgs -b](https://flamenco.blender.org/usage/job-types/) — Flamenco -b jobs

### Flamenco manager configuration · `✅ solid` · Blender 4.5 LTS
**Manager config for Flamenco workers/jobs.**
- **How:** Companion to job-types; pin 4.x blends.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Flamenco manager configuration](https://flamenco.blender.org/usage/manager-configuration/) — Flamenco manager

### GPL licensing caveat — what it means for a studio using or shipping add-ons · `✅ solid` · Blender All Blender versions — GPL has applied since Blender went open-source
**Any Python file that imports bpy is legally a derivative work of Blender (GPL-2.0-or-later). This means all add-on CODE must be GPL-compatible. However, the ASSETS created with Blender or its add-ons are not affected — rendered frames, exported meshes, textures, and game assets belong to the studio under whatever license they choose. The GPL only governs the add-on source code itself.**
- **How:** Three scenarios for a studio: 1. Using third-party GPL add-ons (e.g., from extensions.blender.org): no restrictions on using them commercially. The GPL covers the add-on code, not your output. You can use unlimited seats — GPL prohibits seat-licensing restrictions. 2. Writing in-house add-ons that stay inside the studio: internal tools that are never distributed outside the organization are NOT subject to GPL disclosure. The GPL copyleft only triggers on *distribution*. You can keep a proprietary internal extension as long as you never ship it outside the studio. 3. Distributing add-ons to customers or other studios: the GPL requires you to provide source code to anyone you distribute the add-on to. You can charge for it (you're 'charging for the service of delivering the software'), but you cannot prevent redistribution or modification by the recipient. Bottom line: the studio's rendered output, game assets,.blend scenes, and exported meshes are YOURS, fully proprietary. Only the.py files that import bpy fall under GPL when distributed.
- **Gotchas:** Including a bpy-importing script in a commercial software product distributed externally triggers GPL disclosure on that script — this is a real risk if you bundle pipeline scripts with a shipped game's asset tools.; The blender_manifest.toml requires an SPDX license field; submitting to extensions.blender.org requires GPL-compatible license. You cannot submit a proprietary add-on to the official platform.; GPL-2.0-or-later vs GPL-3.0: Blender itself is GPL-2.0-or-later; using GPL-3.0 for an extension is technically incompatible by strict reading, though in practice the community and Blender Foundation accept either for extensions.; The 'output is yours' principle is well-established but not a written Blender Foundation statement — it follows from general GPL interpretation of tool vs. work produced by the tool.
- **For Studio:** For in-house pipeline add-ons: keep them internal (never distribute) and GPL does not require disclosure. Document internal tools as 'GPL-2.0-or-later (not distributed)' to make the intent explicit. For tools you might open-source later, author them GPL from day one and host on extensions.blender.org.
- **Verify (solid):** GPL derivative-work principle confirmed by multiple sources: cgmarket.net add-on license post, Blender Foundation FAQ, devtalk.blender.org GPL thread. 'Internal use doesn't trigger disclosure' is standard GPL interpretation per FSF guidance. | cross-family (deepseek-v3.1): confirmed — Accurate explanation of GPL implications for add-ons, including internal use vs distribution scenarios. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [What License Should You Use for Blender Add-ons? — CGMarket Blog](https://blog.cgmarket.net/blender-addon-license/) — Importing bpy makes code GPL derivative; output assets are not covered; commercial use of add-ons is unrestricted ; [License — Blender Foundation](https://www.blender.org/about/license/) — Blender is GPL-2.0-or-later; the license page clarifies add-on status ; [How to Make Your Blender Add-on GPL Compliant — Superhive Docs](https://support.superhivemarket.com/article/294-how-to-make-your-blender-addon-gpl-compliant) — Practical compliance guide for commercial add-on developers

### GenioPlus — 8-dir turntable sprite analog · `✅ solid` · Blender 4.5 LTS
**8-direction sprite sheets; camera orbits.**
- **How:** 8-dir turntable analog for sprite orbit craft.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [GenioPlus — 8-dir turntable sprite analog](https://genioplus.com/en/workspace/3d-to-sprite) — 8-dir turntable

### Houdini SOP networks — procedural graph analog · `✅ solid` · Blender 4.5 LTS
**Wired procedural geometry graph generate→modify→display.**
- **How:** Holds for GN with DCC limits; not bpy 8-dir farm substitute.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Houdini SOP networks — procedural graph analog](https://www.sidefx.com/docs/houdini/nodes/sop/) — Houdini SOP analog

### Pixar Tractor tractor-spool -c · `✅ solid` · Blender 4.5 LTS
**Spool a single CLI command to farm blades.**
- **How:** Adjacent farm CLI batch; limit: prman≠EEVEE/Cycles choice.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Pixar Tractor tractor-spool -c](https://renderman.atlassian.net/wiki/spaces/TRA/pages/22184276/tractor-spool) — Tractor spool

### Substance 3D Designer — graph view · `✅ solid` · Blender 4.5 LTS
**Node graph + exposed params → reusable SBSAR.**
- **How:** Procedural graph mindset; texture≠mesh GN sprite bake.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Substance 3D Designer — graph view](https://experienceleague.adobe.com/en/docs/substance-3d-designer/using/workspace/graph-view/the-graph-view) — Substance graph analog

### Thinkbox Deadline — SubmitCommandLineJob · `✅ solid` · Blender 4.5 LTS
**Farm wraps headless executable + frame range into tasks.**
- **How:** Holds for queueing blender -b -P; limit: pools≠orbit script.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. ProcFunc (176) stays verified=0. Live GP headless needs bake (T85546).
- **For Studio:** Headless blender -b -P farm; EEVEE_NEXT needs EGL/ICD; bake GP first.
- **Verify (solid):** STUDY-027 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Thinkbox Deadline — SubmitCommandLineJob](https://docs.thinkboxsoftware.com/products/deadline/10.4/1_User%20Manual/manual/command-line-arguments-jobs.html) — Deadline CLI jobs

### Vector vs raster in game art — Sunstrike · `✅ solid` · Blender 4.5 LTS
**Author vector, export bitmaps/sprite sheets/SDF.**
- **How:** GP/Freestyle authoring-time vector; output raster PNG atlas.
- **Gotchas:** Pin 4.x. Invented 5.x: 0. Live GP headless needs bake (T85546).
- **For Studio:** 4.x GN/GP/Line Art craft for 2.5D sprite/NPR; bake GP before blender -b.
- **Verify (solid):** STUDY-026 Verifier ✅; pin 4.x [no external verdict — not checked]
- **Sources:** [Vector vs raster in game art — Sunstrike](https://sunstrikestudios.com/en/blog/vector_vs_raster_in_game_art/) — Vector→raster game practice

### blender_manifest.toml — the extension manifest format · `✅ solid` · Blender 4.2+ only — blender_manifest.toml is not read by Blender 4.1 or earlier
**Extensions in Blender 4.2+ are described by a blender_manifest.toml file in the root of the extension.zip. It replaces the old bl_info dict for extensions distributed via extensions.blender.org or local repos. Legacy add-ons (still using bl_info) are also supported in 4.2+ via the legacy install path but will not appear in extensions.blender.org.**
- **How:** Minimum required fields: schema_version, id, version, name, tagline, maintainer, type, blender_version_min, license (SPDX string). Example: ```toml
schema_version = "1.0.0"
id = "studio_batch_exporter"
version = "1.0.0"
name = "Studio Batch Exporter"
tagline = "Headless multi-format export for game assets"
maintainer = "Studio Name <studio@example.com>"
type = "add-on"
blender_version_min = "4.2.0"
license = ["SPDX:GPL-2.0-or-later"] # Optional:
# tags = ["Import-Export", "Game Engine"]
# blender_version_max = "5.0.0"
# platforms = ["windows-x64", "linux-x64"]
# wheels = ["./wheels/my_lib-1.0-py3-none-any.whl"]
# [permissions]
# files = "Reads/writes asset directories"
``` The id must be globally unique on extensions.blender.org; convention is author_extensionname (underscores). type must be 'add-on' or 'theme'.
- **Gotchas:** id uses underscores (not hyphens); mismatches cause install failures.; license must be an SPDX identifier array: e.g., ["SPDX:GPL-2.0-or-later"]. Plain strings like 'GPL' are rejected.; blender_version_min must be '4.2.0' or higher to use the extensions platform; setting it to '3.x' is valid but the extension won't appear on extensions.blender.org.; wheels (bundled Python packages) are a key feature over legacy add-ons — include third-party .whl files in the zip, no pip install needed at runtime.; If you include both blender_manifest.toml and bl_info in the same __init__.py, Blender 4.2+ prefers the manifest.
- **For Studio:** For studio-internal extensions, host a local repository directory and point all workstations to it via Preferences > Extensions > Repositories. Use wheels to bundle numpy, Pillow, or other deps so headless render nodes need no internet or pip.
- **Verify (solid):** Required fields confirmed by fetching github.com/BlenderDefender/blender_manifest_schema (cross-referenced against Pallaidium and MedBlend real extension manifests on GitHub). | cross-family (deepseek-v3.1): confirmed — Accurate description of the blender_manifest.toml format and its required fields for Blender 4.2+ extensions. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [blender_manifest_schema — example TOML (GitHub)](https://github.com/BlenderDefender/blender_manifest_schema/blob/main/blender_manifest_v1.example.toml) — Community-maintained JSON Schema for the manifest; shows all required and optional fields ; [How to Create Extensions — Blender 5.1 Manual](https://docs.blender.org/manual/en/latest/advanced/extensions/getting_started.html) — Official manifest field documentation ; [How to Convert Your Blender Add-on to an Extension — Superhive](https://superhivemarket.com/posts/how-to-convert-your-blender-add-on-to-an-extension) — Step-by-step bl_info → blender_manifest.toml migration guide

### bpy add-on API: register/unregister and the minimal operator pattern · `✅ solid` · Blender 4.x (pattern unchanged from 3.x; bl_info optional when manifest present in 4.2+)
**Blender add-ons and extensions both use the same bpy Python API internally. An __init__.py must define register() and unregister() functions. Classes (operators, panels, menus) are registered with bpy.utils.register_class() and unregistered with bpy.utils.unregister_class(). For extensions, bl_info is no longer required (the manifest supplies metadata), but is still valid as a fallback and for backward compatibility.**
- **How:** Minimal extension __init__.py: ```python
import bpy # bl_info retained for Blender < 4.2 compatibility (ignored by 4.2+ if manifest present)
bl_info = { "name": "My Operator", "author": "Studio", "version": (1, 0, 0), "blender": (4, 2, 0), "category": "Import-Export",
} class STUDIO_OT_BatchExport(bpy.types.Operator): bl_idname = "studio.batch_export" bl_label = "Batch Export Assets" bl_description = "Export selected objects to FBX/glTF" def execute(self, context): # pipeline logic here self.report({'INFO'}, "Export complete") return {'FINISHED'} classes = [STUDIO_OT_BatchExport] def register(): for cls in classes: bpy.utils.register_class(cls) def unregister(): for cls in reversed(classes): bpy.utils.unregister_class(cls)
``` Naming convention: operators use CATEGORY_OT_name, panels use CATEGORY_PT_name, menus CATEGORY_MT_name. bl_idname uses dot notation: 'category.action'.
- **Gotchas:** Unregister must iterate classes in reverse order to avoid dependency errors.; bl_idname must be globally unique; clashes with another registered operator will silently shadow one.; For 4.2+ extensions, bl_info is IGNORED if blender_manifest.toml is present — do not put version metadata only in bl_info for extensions.; Operators called headlessly need 'EXEC_DEFAULT' execution context: bpy.ops.studio.batch_export('EXEC_DEFAULT') — the default 'INVOKE_DEFAULT' requires a window.
- **For Studio:** Write studio pipeline operators as extensions with blender_manifest.toml for 4.2+ deploy. Keep bl_info as a fallback comment for any artist who still runs 4.1. Call operators with 'EXEC_DEFAULT' in headless scripts to avoid window context errors.
- **Verify (solid):** register/unregister pattern is stable across all Blender 4.x versions; confirmed via Blender addon tutorial docs and multiple GitHub extension examples. | cross-family (deepseek-v3.1): confirmed — Correct description of the unchanged register/unregister pattern and bl_info becoming optional with manifests in 4.2+. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Add-on Tutorial — Blender Manual](https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html) — Official register/unregister pattern, bl_info structure, operator basics ; [Addons — Blender Developer Documentation (2.80 Python API changes)](https://developer.blender.org/docs/release_notes/2.80/python_api/addons/) — Describes the register/unregister API that remains the basis in 4.x

### Studio distribution: local extension repository + portable Blender build · `▸ plausible` · Blender Local repository support: Blender 4.2+. Portable builds + BLENDER_USER_RESOURCES: all Blender 3.x/4.x
**Blender 4.2 introduces support for custom (local) extension repositories — a directory on disk or network share that Blender treats exactly like extensions.blender.org. This is the correct pattern for a studio that wants to distribute in-house extensions to multiple machines without internet access or publishing to the public platform. Combined with a portable Blender install (extracted, not system-installed), this produces a fully self-contained pipeline build.**
- **How:** Setup a local repo:
1. Create a directory: /studio/blender-extensions/
2. Copy extension.zip files into it
3. In Blender: Preferences > Extensions > Repositories > + (Add) > Local Repository > path to directory
4. Blender will scan and list extensions from that directory in the Extensions panel For headless batch nodes:
- Ship a portable Blender.zip extracted to /studio/blender/
- Pre-configure user prefs (userpref.blend) with all extensions enabled and the local repo registered
- Store the userpref.blend in version control alongside the portable build
- On each render node, copy the portable build — prefs (including enabled extensions) travel with it Portable Blender user data: set BLENDER_USER_RESOURCES env var to a directory inside the portable build so all prefs/extensions are self-contained and don't pollute the OS user profile:
```
BLENDER_USER_RESOURCES=/studio/blender/portable blender --background --python pipeline.py
```
- **Gotchas:** BLENDER_USER_RESOURCES is the correct env var for 4.2+; older docs may reference BLENDER_USER_CONFIG, BLENDER_USER_SCRIPTS, BLENDER_USER_DATAFILES — these still work individually but BLENDER_USER_RESOURCES overrides all of them at once.; Local repo extensions must be valid .zip archives with a blender_manifest.toml at the root — Blender does NOT accept legacy add-on .zips in a local repo (use Install Legacy Add-on for those instead).; The local repo directory must not require write permission from the render node user if extensions are pre-installed; make it read-only on nodes.; extensions.blender.org rate limits or network restrictions won't affect a local-repo build — fully offline.
- **For Studio:** Canonical headless pipeline pattern: one portable Blender build in version control, BLENDER_USER_RESOURCES pointed into it, all studio extensions pre-enabled in committed userpref.blend. New render nodes need only a directory copy. No per-node setup, no internet dependency.
- **Verify (plausible):** Local repository feature confirmed by the extensions platform beta blog and community coverage. BLENDER_USER_RESOURCES env var confirmed in Blender 4.2 release notes discussion; verify exact name against current docs.blender.org/manual (was blocked by 403 during this research session). | cross-family (deepseek-v3.1): confirmed — Correct description of local repository support in 4.2+ and portable build configuration using BLENDER_USER_RESOURCES. [confirmed by 1 of 1 juror(s) [confirmed]]
- **Sources:** [Extensions Platform Beta Release — Blender Developers Blog](https://code.blender.org/2024/05/extensions-platform-beta-release/) — Mentions portable installation and custom bundling of extensions as pipeline features of 4.2 ; [4.2 LTS — Blender (release page)](https://www.blender.org/download/releases/4-2/) — Pipeline integration improvements including portable install and environment variable support

### Useful current extensions for a game-asset batch pipeline · `▸ plausible` · Blender All listed target Blender 4.2+; ACT also supports 3.x
**As of 2025-2026, extensions.blender.org hosts several verified game-pipeline add-ons worth knowing. These are extensions (not legacy add-ons), compatible with Blender 4.2+, available for headless batch use via their operators.**
- **How:** Picks with practical notes: **1. ACT — Asset Creation Toolset** (mrven / MIT/GPL): Batch FBX/glTF export for Unity/UE/Godot, origin alignment, UV tools, renaming. Has a long release history (github.com/mrven/Blender-Asset-Creation-Toolset). Headless: bpy.ops.act.batch_export() pattern. Supports Blender 3.0–5.0+. **2. Game Asset Optimizer**: One-click LOD generation, mesh decimation, dual UV unwrapping, batch optimization presets (CAD Import, Game Asset, VR Optimized, Custom). Good for preparing hi-poly sculpts for engine import. **3. BatchForge / EasyMesh Batch Exporter**: Batch export with per-object origin control, game-engine naming conventions (LOD0/LOD1 suffixes), texture resizing per LOD. Both on extensions.blender.org. **4. Super Duper Batch Exporter**: Auto LOD on export via decimate modifier; Unreal/Unity auto-detect LOD on import. Streamlined single-operator batch export. Install any of these via Preferences > Extensions (online) or blender --command extension install-file for offline. Enable headlessly with addon_utils.enable('act', persistent=True) (module name varies — check the extension id in its blender_manifest.toml).
- **Gotchas:** License: most game pipeline extensions on extensions.blender.org are GPL-2.0-or-later (required by the platform). Some (ACT) carry dual MIT/GPL notice. Check each extension's manifest.; Module names for addon_utils.enable() must match the 'id' field in blender_manifest.toml, NOT the display name — verify by inspecting the installed extension's toml.; Batch exporters that use bpy.ops internally need 'EXEC_DEFAULT' context in headless scripts, or they will error with 'context is incorrect'.; Extensions on extensions.blender.org are reviewed but not audited for security — treat unfamiliar extensions the same as any open-source code before integrating into an automated pipeline.
- **For Studio:** ACT or BatchForge cover the core game-asset-to-engine export loop (FBX/glTF, origin alignment, LOD naming). Pre-bake these into a portable Blender studio build. For Godot-targeted pipeline, glTF via native exporter is sufficient without any add-on; ACT adds per-object batch control on top.
- **Verify (plausible):** Extensions confirmed on extensions.blender.org search results (June 2025 search). ACT confirmed at github.com/mrven/Blender-Asset-Creation-Toolset with 2025.x releases. Full headless operator names not independently verified — confirm by inspecting each extension's source. | cross-family (deepseek-v3.1): unverified — Cannot verify the current status and availability of these specific extensions on extensions.blender.org as of 2025-2026. [only 0 of 1 juror(s) confirmed [unverified]]
- **Sources:** [Game Asset Optimizer — Blender Extensions](https://extensions.blender.org/add-ons/asset-optimizer/) — LOD generation, batch optimization presets, available on extensions.blender.org ; [ACT: Game Asset Creation Toolset releases — GitHub](https://github.com/mrven/Blender-Asset-Creation-Toolset/releases) — Actively maintained batch FBX/glTF exporter for Unity/UE/Godot; 2025.x releases confirm 4.x support ; [EasyMesh Batch Exporter — Blender Extensions](https://extensions.blender.org/add-ons/easymesh-batch-exporter/) — LOD hierarchy export, automatic texture resizing, game-engine naming conventions

