# Rendering & 2.5D sprites
_2D rendering of painterly sprites, Y-sort/depth, 2D lighting (CanvasModulate/Light2D/normal maps/glow), AnimatedSprite2D vs AnimationPlayer, atlases, the renderer choice._ · wave 7 · 2026-09-07 · [‹ catalog index](README.md)

33 recipes · 6 solid.

| Recipe | Godot | Currency | ✓ | What |
|--------|-------|----------|---|------|
| 2D normal maps via CanvasTexture so painterly sprites catch light like reliefs | 4.x (CanvasTexture is the 4.x mechanism; replaces 3.x's per-Sprite normal slot workflow) | ✅ solid | ✓ | Flat sprites lit by Light2D look flat (uniform brightening). A normal map per sp |
| 2D shadows + LightOccluder2D, scoped with light/cull masks for legibility | 4.x (LightOccluder2D/OccluderPolygon2D + Light Mask/Item Cull Mask current in 4.x; SDF-based shadows available) | ✅ solid | ✓ | Hard 2D shadows are produced by giving a PointLight2D/DirectionalLight2D Shadow  |
| Ambient darkness with CanvasModulate as the mood floor | 4.x (CanvasModulate unchanged in concept from 3.x; still single global node) | ✅ solid | ✓ | CanvasModulate is a single node that multiplies the whole 2D canvas by one color |
| Import settings for HIGH-FIDELITY painterly sprites (linear filter + mipmaps, lossless) — NOT pixel-art nearest | 4.x (Import dock Filter/Mipmaps/Compress unchanged in concept; 'Detect 3D' auto-switch is 3D-only) | ✅ solid | ✓ | Godot's per-texture Import dock controls Filter, Mipmaps, and Compression. Pixel |
| PointLight2D / DirectionalLight2D — the split Light2D and how to drive it | 4.x (PointLight2D + DirectionalLight2D replace 3.x Light2D) | ✅ solid | ✓ | Godot 3's single Light2D was SPLIT in Godot 4 into PointLight2D (omni/spot light |
| Y-sort the modern way: y_sort_enabled property, NOT the removed YSort node | 4.x (TileMapLayer node since 4.3; y_sort_enabled property since 4.0) | ✅ solid | ✓ | Correct front/back ordering of overlapping sprites on a 2.5D field. In Godot 4 t |
| Glow / bloom via WorldEnvironment (Canvas background) with a controlled HDR threshold | 4.x (HDR 2D since 4.2; pre-tonemap glow on all renderers 4.4+; verify threshold UI per point release after 4.6 changes) | ▸ plausible | ✓ | Glow/bloom is a post-process on the 2D canvas, enabled by a WorldEnvironment nod |
| Pick the renderer deliberately: Forward+ for HDR-2D glow on a desktop painterly game | 4.x (4.4+ for pre-tonemap glow on all renderers; HDR 2D since 4.2) | ▸ plausible | ✓ | Godot 4 ships three rendering methods, set in Project Settings > Rendering > Ren |
| 2D lights and shadows | 4.x | ⚠ shaky | · | Setup: CanvasModulate + **PointLight2D** + **DirectionalLight2D** + LightOcclude |
| A Space-Optimal Hidden Surface Removal Algorithm for Iso-Oriented Rectangles | 4.x | ⚠ shaky | · | Efficient visible-surface reporting for iso-oriented rectangles — axis-aligned / |
| Absences (on these official pages) | 4.x | ⚠ shaky | · | Absences: no YSort node; no bare Light2D placeable; TileMap deprecated for TileM |
| Analysis and Compilation of Normal Map Generation Techniques for Pixel Art | 4.x | ⚠ shaky | · | Compiles normal-map generation for game sprites so dynamic lighting can shade ea |
| CSS stacking contexts | 4.x | ⚠ shaky | · | Analog: nested contexts are atomic; child z only ranks inside the parent. Holds  |
| CanvasItem | 4.x | ⚠ shaky | · | Exposes `y_sort_enabled` (higher Y in front; sorts only vs same `z_index`), `z_i |
| CanvasModulate class | 4.x | ⚠ shaky | · | Single property `color` tint for a canvas; “Only one can be used to tint a canva |
| DeepMind Lab2D | 4.x | ⚠ shaky | · | Grid worlds as one or more 2D layers with position `(x,y,layer)` and user-contro |
| Fast Sprite Decomposition from Animated Graphics | 4.x | ⚠ shaky | · | Decomposes animated graphics into sprites as basic elements/layers with static t |
| Godot 4 Using TileMaps | 4.x | ⚠ shaky | · | Analog (engine-adjacent currency): TileMap → per-layer TileMapLayer migration is |
| Lights tutorial intro | 4.x | ⚠ shaky | · | Without CanvasModulate, 2D lights only brighten already-unshaded look. Backgroun |
| Narrative-to-Scene Generation: An LLM-Driven Pipeline for 2D Game Environments | 4.x | ⚠ shaky | · | Scenes as multi-layer tile matrices (terrain/environment/objects/items/character |
| Painter's algorithm (depth-sort) | 4.x | ⚠ shaky | · | Analog: draw farthest→nearest by a depth key (polygon-by-polygon). Holds for God |
| Same lights tutorial | 4.x | ⚠ shaky | · | CanvasTexture slots: Diffuse / Normal Map / Specular (+ Color/Shininess). After  |
| Six Ways to Draw Vangers with WebGPU: Real-Time Rendering of Editable Multi-Layer Height Fields | 4.x | ⚠ shaky | · | Compares six interactive methods for hand-authored multi-layer game height field |
| Sketch2Scene: Automatic Generation of Interactive 3D Game Scenes from User’s Casual Sketches | 4.x | ⚠ shaky | · | Pipeline starts from an isometric 2D depiction and recovers isometric depth / la |
| TileMapLayer class | 4.x | ⚠ shaky | · | **TileMap deprecated**; TileMapLayer = one layer. Knobs: `y_sort_origin`, `x_dra |
| Two Dimensional Hidden Surface Removal with Frame-to-frame Coherence | 4.x | ⚠ shaky | · | HSR for two-dimensional layered scenes with a front-to-back rendering model that |
| URP 2D Lights | 4.x | ⚠ shaky | · | Analog: 2D lights use sprite normals with a virtual light-to-sprite distance. Ho |
| Unity 2D sorting + Transparency Sort Mode Custom Axis | 4.x | ⚠ shaky | · | Analog: Sorting Layer / Order in Layer plus vertical custom axis (0,1,0) for top |
| Unity Tilemap layers / multi-layer render order | 4.x | ⚠ shaky | · | Analog: separate tile layers as depth bands + Order in Layer. Holds for one `Til |
| Using TileMaps | 4.x | ⚠ shaky | · | Advises **TileMapLayer** nodes (paint/optimize/collision/occlusion/nav). Exposes |
| AnimatedSprite2D vs AnimationPlayer (+ AnimationTree) — pick per need, drive combat with multi-track sync | 4.x (AnimatedSprite2D + SpriteFrames, AnimationPlayer, AnimationTree all current; note `await` replaces 3.x `yield` in any animation-driven coroutine) |  | ✓ | Two native paths. AnimatedSprite2D uses a SpriteFrames resource (named clips of  |
| Bevy ECS system order — multi-track sync analog | 4.x |  | · | Analog: incompatible systems need explicit.before/.after/.chain. Holds for multi |
| Unity Mecanim FAQ — dual animation paths analog | 4.x |  | ✓ | Analog: dual animation paths (Animator/Mecanim vs legacy Animation). Holds for r |

## Detail

### 2D normal maps via CanvasTexture so painterly sprites catch light like reliefs · `✅ solid` · Godot 4.x (CanvasTexture is the 4.x mechanism; replaces 3.x's per-Sprite normal slot workflow)
**Flat sprites lit by Light2D look flat (uniform brightening). A normal map per sprite tells Godot which way each pixel 'faces' so lights produce directional shading — the rim of a shoulder pauldron catches the lamp, the recess stays dark. In Godot 4 the clean way to attach diffuse+normal(+specular) is the CanvasTexture resource, not a bare Normal Map slot.**
- **How:** Create a CanvasTexture resource and assign it as the Sprite2D's Texture. On it set Diffuse > Texture (the painted color sprite), Normal Map > Texture (the normal map image), and optionally Specular > Texture/Color/Shininess for wet/metal highlights. IMPORTANT: after adding normals, raise the Height property on your PointLight2D / DirectionalLight2D — with Height at 0 the light is in-plane and normals barely register; a positive Height makes the directional shading read. Normal maps only affect surfaces actually reached by a Light2D (they do nothing in pure CanvasModulate ambient).
- **Gotchas:** Wrong-handedness or Y-flipped normal maps make light come from the wrong side — verify against the diffusion pipeline's normal convention. Normals do nothing without a Light2D AND a nonzero light Height — the classic 'I added a normal map and see no change'. The normal-map texture itself should import as a raw (non-sRGB) texture so its vectors aren't color-corrected.
- **Verify (solid):** CORRECTED: Normal maps are not imported as a 'raw (non-sRGB)' texture - Godot 4 has no such import option. Use Compress > Normal Map (Detect/Enable, which forces RGTC); DirectX-style maps are fixed with Process > Normal Map Invert Y. · Godot 4.7 docs: CanvasTexture diffuse/normal/specular, the 'increase the Height property' advice and X+Y+Z+ handedness are all verbatim. But no raw/non-sRGB import option exists. [research note: Verified: CanvasTexture is the 4.x mechanism (Diffuse/Normal Map/Specular slots) and the light Height property drives how normals read ('light's virtual height with regards to normal mapping'). 'No effect without a Light2D + nonzero Height' and raw/non-sRGB import are correct.]
- **Sources:** [2D lights and shadows — Godot Engine stable docs (CanvasTexture diffuse/normal/specular + Height)](https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html) ; [Lighting with 2D normal maps — GDQuest](https://www.gdquest.com/tutorial/godot/2d/lighting-with-normal-maps/)

### 2D shadows + LightOccluder2D, scoped with light/cull masks for legibility · `✅ solid` · Godot 4.x (LightOccluder2D/OccluderPolygon2D + Light Mask/Item Cull Mask current in 4.x; SDF-based shadows available)
**Hard 2D shadows are produced by giving a PointLight2D/DirectionalLight2D Shadow > Enabled and placing LightOccluder2D nodes (with an OccluderPolygon2D) on shadow-casting geometry. The pair of MASK systems controls exactly which sprites a light touches and which cast shadows — critical so combat reads cleanly instead of every prop self-shadowing into mush.**
- **How:** Per light: Shadow > Enabled = true, set Shadow Color, and Filter = None / PCF5 / PCF13 (PCF softens edges at a cost). Per occluder: add LightOccluder2D with an OccluderPolygon2D tracing the blocker's footprint. Two mask layers do the scoping: an object's Visibility > Light Mask = which light layers touch it; a light's Range > Item Cull Mask = which object layers it brightens (counterintuitively named — a layer enabled here GETS lit). The light's Shadow > Item Cull Mask selects which occluders cast for that light and which layers receive shadow. Use these to, e.g., let a light illuminate units but not re-shadow the floor tiles they stand on.
- **Gotchas:** Item Cull Mask vs Light Mask is the single most-confused pair in Godot 2D — remember: Light Mask = layers the light touches; Range Item Cull Mask = which object layers the light lights. There are known engine reports where DirectionalLight2D item cull masks don't restrict coverage as expected (godot#101714) — test, and prefer PointLight2D scoping when you need precise exclusion. Tiles self-occluding their own light is a notorious pain (two-tilemap / mask workarounds exist).
- **Verify (solid):** CORRECTED: DirectionalLight2D does not support light cull masks at all - this is documented behaviour, not a flaky bug: 'It will always light up 2D nodes, regardless of the 2D node's CanvasItem.light_mask.' godot#101714 was closed the same day as a duplicate of #48757, which is an OPEN enhancement (i.e. never implemented), so cite #48757 instead. Separately, shadow_item_cull_mask only selects which occluders CAST for that light (matched against LightOccluder2D.occluder_light_mask); it does not select which layers receive shadow. · Godot 4.7: shadow_enabled/shadow_color, filter None|PCF5|PCF13, LightOccluder2D + OccluderPolygon2D, light_mask and range_item_cull_mask all confirmed. Two mask claims are wrong. [research note: Verified: LightOccluder2D + OccluderPolygon2D, Shadow Enabled/Filter (PCF), and the Light Mask vs Item Cull Mask pair are current 4.x. The cited DirectionalLight2D cull-mask bug (#101714, v4.3) is real and correctly flagged; the 'prefer PointLight2D for precise exclusion' workaround is sound.]
- **Sources:** [2D lights and shadows — Godot Engine stable docs (LightOccluder2D, shadow filters, masks)](https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html) ; [Understanding Light2D Masks in Godot (Imaginary Robots)](https://www.imaginaryrobots.net/posts/2022-02-03-understanding-light2d-masks-godot/) ; [DirectionalLight2D item cull mask does not affect light coverage — godot#101714](https://github.com/godotengine/godot/issues/101714)

### Ambient darkness with CanvasModulate as the mood floor · `✅ solid` · Godot 4.x (CanvasModulate unchanged in concept from 3.x; still single global node)
**CanvasModulate is a single node that multiplies the whole 2D canvas by one color, acting as the global ambient/base tint — it is the color the scene reads as in areas no Light2D reaches. It is the cheapest, most impactful tool for a grimy mood: set it to a dark desaturated value and the world goes from 'flat daylight sprites' to 'underlit ruin', and every PointLight2D you add then carves brightness back out of that darkness.**
- **How:** Add one CanvasModulate node per scene (only the last one in tree order is active). Set its Color to a dark, slightly tinted gray-blue or rust tone (e.g. RGB around 0.12–0.22, cool or warm to taste) rather than pure black so unlit areas keep a readable silhouette. Because it MULTIPLIES, sprite art should be authored close to neutral/bright so the modulate can darken it — don't pre-darken the textures or you lose dynamic range. Pair it with Light2D nodes (next recipes) whose Blend Mode = Add to punch light back in.
- **Gotchas:** Multiple CanvasModulate nodes don't blend — only one wins, which surprises people layering scenes. Pure black (0,0,0) ambient makes unlit tactical units invisible — bad for legibility; keep a small floor value. Under hdr_2d, CanvasModulate still works but combine it thoughtfully with glow threshold so darkening doesn't accidentally kill the bloom you wanted.
- **Verify (solid):** CORRECTED: The unit is the CANVAS, not the scene: 'Only one can be used to tint a canvas, but CanvasLayers can be used to render things independently' - so one per CanvasLayer is legitimate. The 'only the last one in tree order is active' tie-break is not documented anywhere; do not rely on it. The docs describe the node as applying a tint / base ambient colour and never state the multiply operation the recipe builds its authoring advice on. · Godot 4.7: 'the final lighting color in areas that are not reached by any 2D light' is near-verbatim, and only one CanvasModulate can tint a canvas. The scope and the tie-break rule are wrong. [research note: Verified against stable 2D-lighting docs: CanvasModulate multiplies the whole canvas as base ambient ('darken the scene by specifying a color that acts as base ambient'), only the last one in tree wins, pairs with additive Light2D. Multiply-so-author-bright guidance is correct.]
- **Sources:** [2D lights and shadows — Godot Engine stable docs](https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html) ; [Godot: Mastering 2D Lighting (Merxon22, Medium) — CanvasModulate as ambient](https://medium.com/@merxon22/godot-mastering-2d-lighting-a949320e1f68)

### Import settings for HIGH-FIDELITY painterly sprites (linear filter + mipmaps, lossless) — NOT pixel-art nearest · `✅ solid` · Godot 4.x (Import dock Filter/Mipmaps/Compress unchanged in concept; 'Detect 3D' auto-switch is 3D-only)
**Godot's per-texture Import dock controls Filter, Mipmaps, and Compression. Pixel-art guides say 'Nearest, no mipmaps' — that is WRONG here. Painterly diffusion sprites are smooth high-resolution art that gets scaled by camera/parallax, so they want Linear filtering and Mipmaps for clean minification, with Lossless compression to preserve the painted detail.**
- **How:** For painterly sprites: in the texture's Import tab set Compress > Mode = Lossless (stores the PNG faithfully; avoid VRAM Compressed which adds artifacts to gradients), Mipmaps > Generate = ON (clean downscaling when the tactical camera zooms or sprites sit at varied scale; costs ~33% more VRAM per texture — acceptable for the visual tier), and leave Filter at the linear default (sharp 'Nearest' would make smooth art look harsh). Set the global default once in Project Settings > Rendering > Textures > Canvas Textures > Default Texture Filter = Linear (or Linear Mipmap). Click Reimport after any change. Atlas related sprites into a TextureAtlas/sprite sheet to cut draw calls, but keep generous padding so mipmaps don't bleed neighbors.
- **Gotchas:** Don't copy pixel-art tutorials wholesale — Nearest + no-mipmaps is correct for 16-bit, wrong here. VRAM Compressed (S3TC/BPTC) introduces gradient banding ugly on painterly art — stay Lossless. Mipmaps without atlas padding cause edge bleed between packed sprites. You MUST Reimport for changes to take effect; per-file settings override the project default.
- **Verify (solid):** CORRECTED: GODOT-3-STALE: the Import dock has no Filter option in Godot 4. 'Since Godot 4.0, texture filter and repeat modes are set in the CanvasItem properties in 2D (with a project setting acting as a default).' Set CanvasItem.texture_filter per node, or rendering/textures/canvas_textures/default_texture_filter (default 1 = Linear) globally - not the Import tab. Also 'TextureAtlas' is not a Godot 4 class; the class is AtlasTexture. · Godot 4.7: Lossless is the documented 2D default, VRAM Compressed 'should be avoided for 2D', mipmaps cost 'roughly 33%' (verbatim), Reimport is required, project-setting path exact. The Filter claim is stale. [research note: Verified against Importing-images docs: Filter/Mipmaps/Compress are per-texture; Lossless avoids VRAM-compressed gradient banding; Linear + Mipmaps is correct for scaled painterly art (vs Nearest/no-mip for pixel art); global default at Rendering > Textures > Canvas Textures > Default Texture Filter; Reimport required. Atlas-padding-vs-mip-bleed caveat is accurate.]
- **Sources:** [Importing images — Godot Engine stable docs (Filter, Mipmaps, Compress modes)](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html) ; [Fix Blurry 2D Graphics and Fonts in Godot — texture scaling, mipmaps, filtering (Dre Dyson)](https://dredyson.com/fix-blurry-2d-graphics-and-fonts-in-godot-a-beginners-step-by-step-guide-to-understanding-texture-scaling-mipmaps-and-resolution-settings-that-actually-work/) ; [Working With Sprites in Godot 4: Nuances, Pitfalls, and Best Practices](https://ilovesprites.com/blog/godot-sprite-nuances-best-practices)

### PointLight2D / DirectionalLight2D — the split Light2D and how to drive it · `✅ solid` · Godot 4.x (PointLight2D + DirectionalLight2D replace 3.x Light2D)
**Godot 3's single Light2D was SPLIT in Godot 4 into PointLight2D (omni/spot light from a light Texture — torches, optics, muzzle flashes) and DirectionalLight2D (parallel rays — sun/moon). Both inherit the Light2D base (Enabled, Color, Energy, Blend Mode, Range/Z-Min-Max). Any code or tutorial referencing a bare `Light2D` node to place in the scene is Godot-3-stale; instantiate the concrete subclass.**
- **How:** PointLight2D needs a Texture that defines its falloff/shape — a soft radial gradient PNG is the standard 'lamp' look; Texture Scale multiplies its reach without re-authoring the texture, and Offset moves the light glow without moving its shadow origin. Set Energy for intensity and Blend Mode = Add (default) so lights accumulate additively over the CanvasModulate darkness; Subtract makes a negative/shadow light, Mix replaces. DirectionalLight2D gives a uniform wash with a direction; its Height property tilts how normal-mapped sprites catch it. For glow integration, push light Color/Energy so lit hotspots exceed 1.0 under hdr_2d and bloom.
- **Gotchas:** Forgetting the Texture on a PointLight2D = no visible light. Lights stack additively, so several mid-energy lights blow out to white fast under HDR — budget energies per scene. Blend Mode Mix is rarely what you want over a dark ambient (it replaces rather than adds). Light Range Z-Min/Z-Max can silently exclude sprites on certain z layers from being lit.
- **Verify (solid):** Confirmed: Godot 4 splits 3.x Light2D into PointLight2D (needs a falloff Texture) + DirectionalLight2D; both inherit the Light2D base (abstract — you instantiate the subclass, not a bare Light2D). Energy/Blend Mode/Texture Scale/Offset and additive-stacking gotchas match docs. [Godot 4.7: the migration table lists Light2D -> PointLight2D and Light2D is now an abstract base. texture/texture_scale/offset, 'changing the offset does not cause shadows to move', Add/Sub/Mix, height and range_z all verbatim.]
- **Sources:** [2D lights and shadows — Godot Engine stable docs (PointLight2D / DirectionalLight2D properties)](https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html) ; [How to Use 2D Lights in Godot 4 — beginner tutorial (YouTube)](https://www.youtube.com/watch?v=AAPqEebFV-E)

### Y-sort the modern way: y_sort_enabled property, NOT the removed YSort node · `✅ solid` · Godot 4.x (TileMapLayer node since 4.3; y_sort_enabled property since 4.0)
**Correct front/back ordering of overlapping sprites on a 2.5D field. In Godot 4 the dedicated YSort node from Godot 3 is GONE — sorting is now a boolean property, Y Sort Enabled (y_sort_enabled), available on any CanvasItem (Node2D, TileMapLayer). When enabled on a parent, its direct children are drawn ordered by their global Y: lower-on-screen (higher Y) draws in front. Any tutorial telling you to 'add a YSort node' is Godot-3-stale.**
- **How:** On the container node (e.g. a Node2D named World or the unit layer) set y_sort_enabled = true. Each sortable actor (a CharacterBody2D/Node2D for a squad unit) must be a DIRECT child of that container — a grandchild won't sort against its peers. Sorting uses the node's ORIGIN, so position each unit's Sprite2D so the sprite's visual feet sit at the parent node's origin (push the texture up via the Sprite2D Offset, or set centered=false and offset accordingly). Keep z_index = 0 on the sprites and disable 'Z as Relative' where it would otherwise override the Y order. For tiles use TileMapLayer (the 4.3+ replacement for TileMap's internal layers) with Y Sort Enabled on the layer and a correct Y Sort Origin per tile in the TileSet so tall props (walls, machinery) sort by their base, not their center.
- **Gotchas:** z_index hard-overrides y-sort — a stray nonzero z_index (or 'Z as Relative' on a child) silently breaks ordering; this is the #1 'y-sort not working' cause. Godot does NOT auto-sort BETWEEN separate sibling layers/TileMapLayers — cross-layer ordering must be managed by layer order or a shared sorting container. For multi-tile-tall objects the TileSet tile's Y Sort Origin must be moved to the visual base or it pops in front of/behind units incorrectly.
- **Verify (solid):** Confirmed: class_ysort.html is 404 on stable (no YSort node in Godot 4); y_sort_enabled is a real CanvasItem property; TileMapLayer is the 4.3+ replacement and TileMap is deprecated. z_index/Z-as-Relative override and origin-based sorting are accurate. (Ignore a stray web claim that 4.4 'reintroduced' a YSort node — unsupported; docs still 404.) [Godot 4.7: migration guide reads 'YSort | Node2D or Control | CanvasItem has a new Y Sort Enabled property in 4.0'; class_ysort 404s on /stable, 200s on /3.6. z_index gotcha verbatim: nodes sort only if on the same z_index.]
- **Sources:** [Using Y-Sort :: Godot 4 Recipes (kidscancode, 4.x)](https://kidscancode.org/godot_recipes/4.x/2d/using_ysort/index.html) ; [How to make y-sort for TileMapLayer in Godot 4.3? — Godot Forum](https://forum.godotengine.org/t/how-to-make-y-sort-for-tilemaplayer-in-godot-4-3/87689) ; [Using YSort for Correct 2D Depth Sorting (StudyRaid)](https://app.studyraid.com/en/read/32761/1441873/using-ysort-for-correct-2d-depth-sorting)

### Glow / bloom via WorldEnvironment (Canvas background) with a controlled HDR threshold · `▸ plausible` · Godot 4.x (HDR 2D since 4.2; pre-tonemap glow on all renderers 4.4+; verify threshold UI per point release after 4.6 changes)
**Glow/bloom is a post-process on the 2D canvas, enabled by a WorldEnvironment node whose Environment has Background.Mode = Canvas and Glow.Enabled = true. Done right it makes neon and emissive marks blossom; done wrong (no real threshold) it fogs the entire frame. The threshold-correct path requires HDR 2D so 'bright' is a meaningful, isolable value.**
- **How:** Add ONE WorldEnvironment to the main scene; on its Environment set Background.Mode = Canvas, Glow.Enabled = true, choose Glow Blend Mode (Additive/Screen/Softlight), and set the per-level Glow intensity/strength/bloom. Turn ON Project Settings > Rendering > Viewport > HDR 2D and tune Glow HDR Threshold so only pixels above the threshold bloom. Make things glow by pushing their modulate/Color or shader output above 1.0 (set via the inspector RAW tab, or `modulate = Color(2.0, 1.6, 0.4)` in code, or an emissive canvas_item shader). On 4.4+ glow blends before tonemapping for a clean, hue-stable bloom.
- **Gotchas:** Without a working threshold (i.e. without hdr_2d) the whole screen glows — the recurring 4.2 complaint (godot#86098). To exclude a CanvasLayer (e.g. crisp UI text) from glow, isolate it on its own viewport/CanvasLayer outside the glowing canvas. Modulate >1.0 only blooms when hdr_2d is on; in non-HDR it clips at 1.0 (godot#75153). The 4.6 line shuffled the 2D glow threshold control — re-verify after upgrades.
- **Verify (plausible):** CORRECTED: Glow-before-tonemapping landed in 4.6 (PR #110671), not 4.4, and not uniformly: 'Mobile and Forward+ now apply glow before the tonemap function, just like the Compatibility renderer, for all blend modes except for soft light' - Compatibility already did it. 4.6 also changed the default blend mode to Screen (glow_blend_mode now defaults to 1). godot#86098 is read backwards: the reporter had HDR 2D ON and the root cause is the Mobile renderer's limited dynamic range; the issue is closed. The 4.6 threshold control was not removed or shuffled - a dev3-only default change (1.0 -> 0.0) was reverted before 4.6-stable. Missing requirement: the docs state glow_hdr_threshold 'needs to be decreased below 1.0 when using glow in 2D, as 2D rendering is performed in SDR'. Glow itself is supported on all three renderers. · Godot 4.7: WorldEnvironment one-per-scene, BG_CANVAS=3, glow_enabled, glow_hdr_threshold, glow_intensity/strength/bloom all confirmed. The version and issue attributions are wrong. [research note: Workflow is correct for current 4.x (WorldEnvironment + Background=Canvas + Glow.Enabled, hdr_2d for a real threshold, push modulate >1.0 via RAW tab; #86098 and #75153 are real). Same version error as recipe #1: 'on 4.4+ glow blends before tonemapping' is actually a 4.6 change. Recipe already hedges the 4.6 threshold-UI churn, which is appropriate given engine is now at 4.7.]
- **Sources:** [4.2 World Environment Glow Effect makes everything glow — godot#86098](https://github.com/godotengine/godot/issues/86098) ; [Finally glowing! (Godot 4.4) — HDR 2D + WorldEnvironment glow workflow](https://initdotdev.itch.io/puzzle-crossing/devlog/903593/finally-glowing-with-godot-44) ; [CanvasItem Modulate values above 1.0 are clipped (HDR threshold) — godot#75153](https://github.com/godotengine/godot/issues/75153)

### Pick the renderer deliberately: Forward+ for HDR-2D glow on a desktop painterly game · `▸ plausible` · Godot 4.x (4.4+ for pre-tonemap glow on all renderers; HDR 2D since 4.2)
**Godot 4 ships three rendering methods, set in Project Settings > Rendering > Rendering Method (rendering/renderer/rendering_method): forward_plus, mobile, and gl_compatibility. The choice is a one-line project setting but it gates which 2D features exist. For a high-fidelity painterly-sprite game (sprites + controlled neon glow + grimy mood, PC-only) the decisive features are HDR 2D and MSAA 2D, which exist ONLY on Forward+ and Mobile — Compatibility (the GLES3/WebGL path) supports neither. The common 'Compatibility is good enough for 2D' advice is true for flat-lit games, but breaks for a bloom-driven look that needs a real brightness threshold.**
- **How:** Set forward_plus (the desktop default). Then enable Project Settings > Rendering > Viewport > HDR 2D (rendering/viewport/hdr_2d = true) so the 2D canvas renders in linear/HDR and pixels brighter than 1.0 actually drive glow. Add a WorldEnvironment node with an Environment resource: Background.Mode = Canvas, Glow.Enabled = true, tune Glow HDR Threshold so only the bright neon/emissive pixels bloom (not the whole grimy frame). As of Godot 4.4 glow blends BEFORE tonemapping on all three renderers (avoids the old hue-shift/hard-edge artifacts), but the HDR threshold workflow itself still needs hdr_2d, hence Forward+. Note the renderer can be set per-platform in the export-style override dropdown, but a desktop-only title can just commit to forward_plus.
- **Gotchas:** Compatibility is the ONLY web-export path — choosing Forward+ forfeits web export (fine for a PC tactical RPG, but document it). With hdr_2d ON, any custom canvas_item shader sampling a color texture MUST mark the sampler uniform `source_color` (hint_color) or it renders washed-out, because the 2D pass is now linear. To set modulate/Color values above 1.0 in the inspector you must use the RAW tab (RGB/HSV tab clamps at 1.0). 4.6 briefly removed/changed the 2D glow threshold UI — pin your exact 4.x point release and re-verify the glow knobs after any engine upgrade.
- **Verify (plausible):** CORRECTED: Glow-before-tonemapping is 4.6 (PR #110671), not 4.4, and it did not change all three renderers: Compatibility already applied glow before tonemapping, and the PR moved Mobile and Forward+ to match it, excluding soft light. 4.6 did not remove the 2D glow threshold UI - a dev-only default change was reverted before stable. 'hint_color' is the Godot 3 name and does not exist in Godot 4; only source_color does. Everything else checks out exactly, including rendering/renderer/rendering_method = 'forward_plus' with values forward_plus / mobile / gl_compatibility, and the source_color rule: 'required in the Forward+ and Mobile renderers, and in canvas_item shaders when HDR 2D is enabled... the texture will appear washed out.' · Godot 4.7 feature table confirms the core claim: 2D HDR Viewport and MSAA 2D are Mobile+Forward+ only and Compatibility supports neither; web is Compatibility-only. Version claims are wrong. [research note: Core claims VERIFIED on stable docs (HDR 2D + MSAA 2D = Forward+/Mobile only; Compatibility unsupported; web export forces Compatibility). One version error: 'as of Godot 4.4 glow blends BEFORE tonemapping on all three renderers' is WRONG — that change landed in 4.6 (the 4.6 release page states the new curves 'don't break compatibility with 4.4 and 4.5', i.e. the pre-tonemap behavior is new in 4.6). hdr_2d-since-4.2 is correct. source_color requirement (#84989) and RAW-tab >1.0 are real.]
- **Sources:** [Overview of renderers — Godot Engine stable docs](https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html) ; [Dev snapshot: Godot 4.6 dev 2 (glow now blends before tonemapping on all renderers)](https://godotengine.org/article/dev-snapshot-godot-4-6-dev-2/) ; [Using vec4/color in canvas_item shaders washed out when 2D HDR active (source_color requirement) — godot#84989](https://github.com/godotengine/godot/issues/84989)

### 2D lights and shadows · `⚠ shaky` · Godot 4.x
**Setup: CanvasModulate + **PointLight2D** + **DirectionalLight2D** + LightOccluder2D; receivers include Sprite2D/TileMapLayer. PointLight2D: Texture, Offset, Texture Scale, **Height** (normals). DirectionalLight2D: Height, Max Distance. Common Light2D base: Energy, Blend Mode, Range Z Min/Max, Item Cull Mask. Shadows: Enabled, Filter None/PCF5/PCF13, Item Cull Mask.**
- **How:** Official Godot 4.x docs; TileMapLayer + y_sort_enabled + Point/Directional lights.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [2D lights and shadows](https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html) — Setup: CanvasModulate + **PointLight2D** + **DirectionalLight2D** + LightOccluder2D; receivers include Sprite2D/TileMapLayer. PointLight2D: Texture, Offset, Texture Scale, **Height** (normals). Direct

### A Space-Optimal Hidden Surface Removal Algorithm for Iso-Oriented Rectangles · `⚠ shaky` · Godot 4.x
**Efficient visible-surface reporting for iso-oriented rectangles — axis-aligned / iso-oriented occlusion frame adjacent to isometric tile depth sorting (no API invent).**
- **How:** Literature deepen for 2.5D depth/lighting/tiles; no Godot API invent.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [A Space-Optimal Hidden Surface Removal Algorithm for Iso-Oriented Rectangles](https://arxiv.org/abs/1109.0389) — Efficient visible-surface reporting for iso-oriented rectangles — axis-aligned / iso-oriented occlusion frame adjacent to isometric tile depth sorting (no API invent).

### Absences (on these official pages) · `⚠ shaky` · Godot 4.x
**Absences: no YSort node; no bare Light2D placeable; TileMap deprecated for TileMapLayer. No Godot-3 bare `Light2D` placeable node (split subclasses). No YSort node. No claim that DirectionalHeight shortens shadows (docs: directional shadows always infinitely long).**
- **How:** Official Godot 4.x docs; TileMapLayer + y_sort_enabled + Point/Directional lights.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]

### Analysis and Compilation of Normal Map Generation Techniques for Pixel Art · `⚠ shaky` · Godot 4.x
**Compiles normal-map generation for game sprites so dynamic lighting can shade each pixel by surface direction — sprite normal-map lighting craft for CanvasTexture/Light2D notes (no API invent).**
- **How:** Literature deepen for 2.5D depth/lighting/tiles; no Godot API invent.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Analysis and Compilation of Normal Map Generation Techniques for Pixel Art](https://arxiv.org/abs/2212.09692) — Compiles normal-map generation for game sprites so dynamic lighting can shade each pixel by surface direction — sprite normal-map lighting craft for CanvasTexture/Light2D notes (no API invent).

### CSS stacking contexts · `⚠ shaky` · Godot 4.x
**Analog: nested contexts are atomic; child z only ranks inside the parent. Holds for “stray `z_index` / Z-as-Relative breaks Y-sort” gotcha. Limit: CSS paint order ≠ Godot canvas item tree.**
- **How:** Adjacent analog hold-with-limit; fail-transfers omitted.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [CSS stacking contexts](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_positioned_layout/Understanding_z-index/Stacking_context) — Analog: nested contexts are atomic; child z only ranks inside the parent. Holds for “stray `z_index` / Z-as-Relative breaks Y-sort” gotcha. Limit: CSS paint order ≠ Godot canvas item tree.

### CanvasItem · `⚠ shaky` · Godot 4.x
**Exposes `y_sort_enabled` (higher Y in front; sorts only vs same `z_index`), `z_index`, `z_as_relative`, `light_mask`, `visibility_layer`, modulate/self_modulate. **Absent:** dedicated YSort node (sorting is a property).**
- **How:** Official Godot 4.x docs; TileMapLayer + y_sort_enabled + Point/Directional lights.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [CanvasItem](https://docs.godotengine.org/en/stable/classes/class_canvasitem.html) — Exposes `y_sort_enabled` (higher Y in front; sorts only vs same `z_index`), `z_index`, `z_as_relative`, `light_mask`, `visibility_layer`, modulate/self_modulate. **Absent:** dedicated YSort node (sort

### CanvasModulate class · `⚠ shaky` · Godot 4.x
**Single property `color` tint for a canvas; “Only one can be used to tint a canvas” (CanvasLayers independent). Ambient/mood floor knob = that color.**
- **How:** Official Godot 4.x docs; TileMapLayer + y_sort_enabled + Point/Directional lights.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [CanvasModulate class](https://docs.godotengine.org/en/stable/classes/class_canvasmodulate.html) — Single property `color` tint for a canvas; “Only one can be used to tint a canvas” (CanvasLayers independent). Ambient/mood floor knob = that color.

### DeepMind Lab2D · `⚠ shaky` · Godot 4.x
**Grid worlds as one or more 2D layers with position `(x,y,layer)` and user-controlled layer rendering order — multi-layer tile substrate / draw-order craft for TileMapLayer banding (no API invent).**
- **How:** Literature deepen for 2.5D depth/lighting/tiles; no Godot API invent.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [DeepMind Lab2D](https://arxiv.org/abs/2011.07027) — Grid worlds as one or more 2D layers with position `(x,y,layer)` and user-controlled layer rendering order — multi-layer tile substrate / draw-order craft for TileMapLayer banding (no API invent).

### Fast Sprite Decomposition from Animated Graphics · `⚠ shaky` · Godot 4.x
**Decomposes animated graphics into sprites as basic elements/layers with static textures — sprite-as-layer representation adjacent to multi-band 2.5D sprite stacks (no API invent).**
- **How:** Literature deepen for 2.5D depth/lighting/tiles; no Godot API invent.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Fast Sprite Decomposition from Animated Graphics](https://arxiv.org/abs/2408.03923) — Decomposes animated graphics into sprites as basic elements/layers with static textures — sprite-as-layer representation adjacent to multi-band 2.5D sprite stacks (no API invent).

### Godot 4 Using TileMaps · `⚠ shaky` · Godot 4.x
**Analog (engine-adjacent currency): TileMap → per-layer TileMapLayer migration is the current substrate. Holds for 2.5D tile practice on 4.3+. Limit: docs are same-engine; still not a flip of unverified leftover recipes.**
- **How:** Adjacent analog hold-with-limit; fail-transfers omitted.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Godot 4 Using TileMaps](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html) — Analog (engine-adjacent currency): TileMap → per-layer TileMapLayer migration is the current substrate. Holds for 2.5D tile practice on 4.3+. Limit: docs are same-engine; still not a flip of unverifie

### Lights tutorial intro · `⚠ shaky` · Godot 4.x
**Without CanvasModulate, 2D lights only brighten already-unshaded look. Background color itself receives no lighting (needs a Sprite2D/visual).**
- **How:** Official Godot 4.x docs; TileMapLayer + y_sort_enabled + Point/Directional lights.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]

### Narrative-to-Scene Generation: An LLM-Driven Pipeline for 2D Game Environments · `⚠ shaky` · Godot 4.x
**Scenes as multi-layer tile matrices (terrain/environment/objects/items/characters) composited in semantic order to preserve depth — layered tile depth composite craft (no API invent).**
- **How:** Literature deepen for 2.5D depth/lighting/tiles; no Godot API invent.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Narrative-to-Scene Generation: An LLM-Driven Pipeline for 2D Game Environments](https://arxiv.org/abs/2509.04481) — Scenes as multi-layer tile matrices (terrain/environment/objects/items/characters) composited in semantic order to preserve depth — layered tile depth composite craft (no API invent).

### Painter's algorithm (depth-sort) · `⚠ shaky` · Godot 4.x
**Analog: draw farthest→nearest by a depth key (polygon-by-polygon). Holds for Godot `y_sort_enabled` (higher screen-Y draws in front). Limit: 3D polygon sort ≠ CanvasItem origin/Y Sort Origin.**
- **How:** Adjacent analog hold-with-limit; fail-transfers omitted.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Painter's algorithm (depth-sort)](https://en.wikipedia.org/wiki/Painter%27s_algorithm) — Analog: draw farthest→nearest by a depth key (polygon-by-polygon). Holds for Godot `y_sort_enabled` (higher screen-Y draws in front). Limit: 3D polygon sort ≠ CanvasItem origin/Y Sort Origin.

### Same lights tutorial · `⚠ shaky` · Godot 4.x
**CanvasTexture slots: Diffuse / Normal Map / Specular (+ Color/Shininess). After normals, raise light **Height** (and often Energy). Additive Sprite2D alternative noted (no shadows/normals).**
- **How:** Official Godot 4.x docs; TileMapLayer + y_sort_enabled + Point/Directional lights.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]

### Six Ways to Draw Vangers with WebGPU: Real-Time Rendering of Editable Multi-Layer Height Fields · `⚠ shaky` · Godot 4.x
**Compares six interactive methods for hand-authored multi-layer game height fields (two solid intervals per sample) — multi-layer terrain depth beyond single-valued DEM (no API invent).**
- **How:** Literature deepen for 2.5D depth/lighting/tiles; no Godot API invent.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Six Ways to Draw Vangers with WebGPU: Real-Time Rendering of Editable Multi-Laye](https://arxiv.org/abs/2608.17390) — Compares six interactive methods for hand-authored multi-layer game height fields (two solid intervals per sample) — multi-layer terrain depth beyond single-valued DEM (no API invent).

### Sketch2Scene: Automatic Generation of Interactive 3D Game Scenes from User’s Casual Sketches · `⚠ shaky` · Godot 4.x
**Pipeline starts from an isometric 2D depiction and recovers isometric depth / layout before engine playable scenes — isometric depth as a first-class 2.5D authoring signal (no API invent).**
- **How:** Literature deepen for 2.5D depth/lighting/tiles; no Godot API invent.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Sketch2Scene: Automatic Generation of Interactive 3D Game Scenes from User’s Cas](https://arxiv.org/abs/2408.04567) — Pipeline starts from an isometric 2D depiction and recovers isometric depth / layout before engine playable scenes — isometric depth as a first-class 2.5D authoring signal (no API invent).

### TileMapLayer class · `⚠ shaky` · Godot 4.x
****TileMap deprecated**; TileMapLayer = one layer. Knobs: `y_sort_origin`, `x_draw_order_reversed`, `rendering_quadrant_size` (ignored when Y-sorted), `occlusion_enabled`, `collision_enabled`, `navigation_enabled`, `local_to_map`/`map_to_local`. Absent on page: old multi-layer TileMap API as current.**
- **How:** Official Godot 4.x docs; TileMapLayer + y_sort_enabled + Point/Directional lights.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [TileMapLayer class](https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html) — **TileMap deprecated**; TileMapLayer = one layer. Knobs: `y_sort_origin`, `x_draw_order_reversed`, `rendering_quadrant_size` (ignored when Y-sorted), `occlusion_enabled`, `collision_enabled`, `navigat

### Two Dimensional Hidden Surface Removal with Frame-to-frame Coherence · `⚠ shaky` · Godot 4.x
**HSR for two-dimensional layered scenes with a front-to-back rendering model that cuts unnecessary rasterization — painter-style layered depth order craft for 2.5D Y-sort notes (no Godot API invent).**
- **How:** Literature deepen for 2.5D depth/lighting/tiles; no Godot API invent.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Two Dimensional Hidden Surface Removal with Frame-to-frame Coherence](https://arxiv.org/abs/2411.00131) — HSR for two-dimensional layered scenes with a front-to-back rendering model that cuts unnecessary rasterization — painter-style layered depth order craft for 2.5D Y-sort notes (no Godot API invent).

### URP 2D Lights · `⚠ shaky` · Godot 4.x
**Analog: 2D lights use sprite normals with a virtual light-to-sprite distance. Holds for CanvasTexture normals + Light2D Height. Limit: URP package knobs ≠ Godot CanvasTexture slots.**
- **How:** Adjacent analog hold-with-limit; fail-transfers omitted.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [URP 2D Lights](https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@14.0/manual/2DLightProperties.html) — Analog: 2D lights use sprite normals with a virtual light-to-sprite distance. Holds for CanvasTexture normals + Light2D Height. Limit: URP package knobs ≠ Godot CanvasTexture slots.

### Unity 2D sorting + Transparency Sort Mode Custom Axis · `⚠ shaky` · Godot 4.x
**Analog: Sorting Layer / Order in Layer plus vertical custom axis (0,1,0) for top-down depth. Holds for TileMapLayer/layer order + Y-sort peers. Limit: Unity Transparency Sort ≠ Godot `y_sort_enabled` property.**
- **How:** Adjacent analog hold-with-limit; fail-transfers omitted.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Unity 2D sorting + Transparency Sort Mode Custom Axis](https://docs.unity3d.com/Manual/2DSorting.html) — Analog: Sorting Layer / Order in Layer plus vertical custom axis (0,1,0) for top-down depth. Holds for TileMapLayer/layer order + Y-sort peers. Limit: Unity Transparency Sort ≠ Godot `y_sort_enabled`

### Unity Tilemap layers / multi-layer render order · `⚠ shaky` · Godot 4.x
**Analog: separate tile layers as depth bands + Order in Layer. Holds for one `TileMapLayer` per logical band (ground/cover/overlays). Limit: Unity Tilemap API ≠ Godot 4.3+ TileMapLayer methods.**
- **How:** Adjacent analog hold-with-limit; fail-transfers omitted.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Unity Tilemap layers / multi-layer render order](https://docs.unity3d.com/Manual/sprites-sort.html) — Analog: separate tile layers as depth bands + Order in Layer. Holds for one `TileMapLayer` per logical band (ground/cover/overlays). Limit: Unity Tilemap API ≠ Godot 4.3+ TileMapLayer methods.

### Using TileMaps · `⚠ shaky` · Godot 4.x
**Advises **TileMapLayer** nodes (paint/optimize/collision/occlusion/nav). Exposes per-layer: Enabled, TileSet; Rendering **Y Sort Origin**, **X Draw Order Reversed** (need CanvasItem Y Sort Enabled), Rendering Quadrant Size; Physics Collision Enabled / Use Kinematic Bodies; Navigation Enabled. Multiple layers by multiple nodes.**
- **How:** Official Godot 4.x docs; TileMapLayer + y_sort_enabled + Point/Directional lights.
- **Gotchas:** STUDY-045.
- **Verify (shaky):** STUDY-045 deepen [no external verdict — not checked]
- **Sources:** [Using TileMaps](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html) — Advises **TileMapLayer** nodes (paint/optimize/collision/occlusion/nav). Exposes per-layer: Enabled, TileSet; Rendering **Y Sort Origin**, **X Draw Order Reversed** (need CanvasItem Y Sort Enabled), R

### AnimatedSprite2D vs AnimationPlayer (+ AnimationTree) — pick per need, drive combat with multi-track sync · `?` · Godot 4.x (AnimatedSprite2D + SpriteFrames, AnimationPlayer, AnimationTree all current; note `await` replaces 3.x `yield` in any animation-driven coroutine)
**Two native paths. AnimatedSprite2D uses a SpriteFrames resource (named clips of frames) and is purpose-built, low-overhead frame playback — ideal for simple state loops (idle/walk). AnimationPlayer is general-purpose: it keyframes ANY property on ANY node over a timeline — a Sprite2D's frame, plus modulate, position, a hitbox's disabled flag, an audio trigger, a particle emit — all synced. For a tactical RPG's discrete, event-precise actions, AnimationPlayer (optionally fed by an AnimationTree state machine) is the stronger backbone.**
- **How:** Simple ambient/loop motion -> AnimatedSprite2D: build a SpriteFrames (add frames from a sprite sheet via the editor, set FPS/loop per clip), then play("walk")/stop() in code. Event-coupled combat -> AnimationPlayer: drive a Sprite2D's frame via either AnimatedSprite2D's clip OR a Sprite2D with hframes/vframes and keyframe the Frame property; on the same timeline keyframe Call Method tracks (apply damage on the exact contact frame), enable/disable a hit Area2D, fire VFX/audio. Wrap multiple AnimationPlayer clips in an AnimationTree (AnimationNodeStateMachine) for clean idle->aim->fire->recoil->hit transitions. Trigger one-shot logic with the animation_finished signal.
- **Gotchas:** Don't reach for AnimationPlayer when AnimatedSprite2D suffices — it's more setup for no gain on a pure loop. Mixing both on one actor (AnimatedSprite2D playing AND AnimationPlayer keying its frame) causes fighting over the frame property. Any old tutorial using `yield(...)` to wait on animation is Godot-3-stale — use `await player.animation_finished`. AnimationTree must have.active = true and a configured state-machine playback or nothing plays.
- **Verify ():** CORRECTED: 'AnimationTree must have .active = true or nothing plays' is Godot-3 residue: active is inherited from AnimationMixer and DEFAULTS TO TRUE in Godot 4 (it defaulted to false in Godot 3), so nothing needs setting. Also set_method_call_mode / get_method_call_mode - the 'Call Method' track API the recipe leans on - are deprecated in favour of AnimationMixer.callback_mode_method. · Godot 4.7: SpriteFrames, Animation.TYPE_METHOD (=5) 'Method tracks call functions with given arguments per key', Sprite2D hframes/vframes/frame, AnimationNodeStateMachine + parameters/playback all confirmed.
- **Sources:** [2D sprite animation — Godot Engine stable docs (AnimatedSprite2D/SpriteFrames vs AnimationPlayer + Sprite2D hframes/vframes)](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html) ; [AnimatedSprite2D vs AnimationPlayer: When to Use Each (UhiyamaLab)](https://uhiyama-lab.com/en/notes/godot/animatedsprite2d-vs-animationplayer-comparison/) ; [Godot Spritesheet Animation: AnimatedSprite2D vs AnimationPlayer Explained (Spritesheets.ai)](https://www.spritesheets.ai/blog/godot-spritesheet-animation-guide)

### Bevy ECS system order — multi-track sync analog · `?` · Godot 4.x
**Analog: incompatible systems need explicit.before/.after/.chain. Holds for multi-track AnimationPlayer / turn-state sync (recipe 37 combat backbone); limit: ECS schedule ≠ SpriteFrames vs AnimationPlayer product choice.**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 [No Godot engine claim, and the record's own source is absent: 'how' reads 'See source URL' with no URL present, and STUDY-002 is not locatable. Bevy's .before/.after/.chain do exist (checked Bevy 0.19.1).]
- **Sources:** [Bevy ECS system order — multi-track sync analog](https://docs.rs/bevy/latest/bevy/ecs/system/index.html) — multi-track sync analog

### Unity Mecanim FAQ — dual animation paths analog · `?` · Godot 4.x
**Analog: dual animation paths (Animator/Mecanim vs legacy Animation). Holds for recipe 37 (AnimatedSprite2D vs AnimationPlayer): pick path by need; limit: Unity deprecates legacy — Godot keeps both current.**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Verify ():** CORRECTED: Unity does not deprecate the legacy Animation component. Its docs call it 'Legacy', 'available for backwards compatibility with old Unity projects', and 'still available because it is easier to use and provides better performance for simpler animations.' The honest contrast is legacy-but-retained, not deprecated - which makes the recipe's 'Godot keeps both current' distinction weaker than stated. · Checked against current Unity docs (no Godot claim here, and no source URL in the record). The dual-path premise holds; the stated limit does not. [research note: STUDY-012 from STUDY-002 Verifier ✅; default verified=0]
- **Sources:** [Unity Mecanim FAQ — dual animation paths analog](https://docs.unity3d.com/2021.2/Documentation/Manual/MecanimFAQ.html) — dual paths

