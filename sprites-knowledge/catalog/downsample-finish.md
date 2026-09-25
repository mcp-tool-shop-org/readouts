# Downsample & pixel finish
_512px master -> 48/64px game sprite: Lanczos/area downscale, foot-anchor, union bbox, quantization/dithering, palette._ · wave 5 · 2026-09-07 · [‹ catalog index](README.md)

19 recipes · 4 recommended · 1 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 1 | Lanczos 512->64px, foot-anchored, union-bbox | python | game-sprite | ▣ measured | ✅ yes | 5 | 5 | · |
| 2 | Color quantization + dithering + palette discipline at small sizes | python | both | ▸ reproduced | ✅ yes | 5 | 5 | · |
| 2 | Supersample + Lanczos/area downsample (512 -> 48/64px) | python | both | ▸ reproduced | ✅ yes | 5 | 5 | · |
| 6 | Orthographic camera + foot-anchor (bottom-center) registration | blender | both | · community | ✅ yes | 5 | 5 | · |
| 8 | Hiive adaptive pixel-art downscaler (majority-block + edge-preserving) | python | both | · single-run | ? unk | 4 | 3 | · |
| 9 | Aseprite CLI sheet export — packing hold-with-limit | docs | all | analog | check | 4 | 4 | · |
| 9 | Aseprite CLI — sheet export surface | docs | all | docs | check | 4 | 4 | · |
| 9 | BLOCK — pixel-quant character-to-skin | blender | sprites | paper | check | 4 | 4 | · |
| 9 | CSS image-rendering pixelated — display analog | blender | sprites | docs | check | 4 | 4 | · |
| 9 | CSS image-rendering — pixelated / crisp-edges display peer | docs | all | docs | check | 4 | 4 | · |
| 9 | Heckbert median-cut — palette lock analog (paywall unverified) | docs | all | analog | check | 4 | 4 | · |
| 9 | Heckbert median-cut — palette quant analog | blender | sprites | docs | check | 4 | 4 | · |
| 9 | Pillow Concepts — LANCZOS downsample + palette modes | docs | all | docs | check | 4 | 4 | · |
| 9 | Pillow LANCZOS / palette modes — downsample hold-with-limit | docs | all | analog | check | 4 | 4 | · |
| 9 | Pillow resampling — LANCZOS downsample | blender | sprites | docs | check | 4 | 4 | · |
| 9 | SD-piXL — low-res quantized imagery | blender | sprites | paper | check | 4 | 4 | · |
| 9 | SD-πXL — SDS palette tensor quantized pixel art (Binninger & Sorkine-Hornung 2024) | comfy | all | paper | check | 4 | 4 | · |
| 9 | libGDX TexturePacker — atlas pack + .atlas | docs | all | docs | check | 4 | 4 | · |
| 9 | libGDX TexturePacker — sheet packing hold-with-limit | docs | all | analog | check | 4 | 4 | · |

## Detail

### Lanczos 512->64px, foot-anchored, union-bbox · `recommended` · ▣ measured
**Auto-crop -> union-bbox across 8 directions -> foot-anchor -> Lanczos resize -> unsharp gives consistent, readable 64px game sprites.**
downsample_sprites.py (Pillow): crops each direction by its alpha bbox, computes a union bbox across all 8 so every direction shares framing, foot-anchors (feet on a common ground line), Lanczos-resizes to the game size, applies a light unsharp mask, and writes a contact sheet. Pillow Lanczos scales the filter window for downscale (unlike OpenCV INTER_LANCZOS4). Produced 8x 64px in <1s, looked-at.
- **For the pipeline:** Final stage of the sprite pipeline. Foot-anchoring + union-bbox is what makes an 8-direction set read as one character at game size. 64px reads here; 48px and palette-quantization are available knobs (see the research lane).
- **Engine:** python · **Applies to:** game-sprite · **Base:** n/a · **Kind:** post-process
- **Validated under:** Ran on the 8 Blender renders; 64px contact sheet looked-at 2026-06-07.
- **Output license:** commercial **yes** (license: Pillow is HPND (permissive))
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| target_size | 64 px | ○ | 48 also supported; 64 read cleanly for a detailed character |
| foot_anchor | true | ○ | feet on a common baseline across directions |
| resample | Lanczos | ○ | Pillow scales the window on downscale; better than OpenCV INTER_LANCZOS4 |

- **Verify:** no external verdict — not checked
- **Sources:** [downsample_sprites.py (trellis-sprite-pipeline)](https://github.com/mcp-tool-shop-org/trellis-sprite-pipeline) — Auto-crop/union-bbox/foot-anchor/Lanczos/unsharp downsampler. ; [Pillow Image.resize (Lanczos)](https://pillow.readthedocs.io/en/stable/handbook/concepts.html#filters) — Lanczos properly scales the filter window for downsampling.

### Color quantization + dithering + palette discipline at small sizes · `recommended` · ▸ reproduced
**At 48-64px a modified median-cut (with k-means refinement) palette plus selective Floyd-Steinberg or Bayer dithering controls banding while a locked house palette keeps every sprite/tile coherent.**
Reduce the downsampled sprite to a constrained palette with modified median-cut (Heckbert 1979) refined by k-means and perceptual weighting — the approach libvips/pngquant use. Combine with dithering only where needed: Floyd-Steinberg error-diffusion hides gradient banding but adds noise that can shimmer in animation; ordered/Bayer dithering is deterministic (no frame-to-frame crawl) and thus safer for animated sprites. Palette discipline is the studio-level rule: extract or author a fixed house palette (e.g. 16-32 colors), quantize ALL sprites/tiles to it, so characters, props, and tiles share a coherent look and engine tinting stays predictable.
- **Engine:** python · **Applies to:** both · **Base:** n/a · **Kind:** post-process
- **VRAM:** 0 (CPU)
- **Output license:** commercial **yes** (license: algorithms public; pngquant/libimagequant GPLv3-or-commercial; Pillow HPND) — Algorithms are public-domain math; common impls (Pillow, libimagequant/pngquant) — note pngquant/libimagequant is GPLv3 OR a paid commercial license, so for a closed-source pipeline use Pillow's median-cut or a clean implementation, or buy the libimagequant commercial license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| quantizer | median-cut + k-means refine | ○ | perceptual weighting like libvips/pngquant; better than plain median-cut |
| palette size | 16-32 house palette | ○ | lock once, quantize everything to it for coherence |
| dither (animated) | ordered/Bayer | ○ | deterministic; avoids frame-to-frame shimmer |
| dither (static) | Floyd-Steinberg, sparingly | ○ | best banding suppression but adds noise |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Dither pattern crawls/shimmers across animation frames | error-diffusion (Floyd-Steinberg) recomputed per frame | Use ordered/Bayer dithering, or quantize to a fixed palette without diffusion for animated sprites |  |
| Sprites look color-incoherent across the cast | per-sprite palettes instead of a shared house palette | Author one locked palette; quantize all assets to it |  |

- **Verify:** Both sources resolve. Wikipedia Color quantization confirms verbatim: 'most popular algorithm... invented by Paul Heckbert in 1979, is the median cut algorithm' and 'frequently combined with dithering, which can eliminate... banding.' ubitux (Clement Beffa) blog confirms modified median-cut + K-means refinement + perceptual (OkLab) color weighting + dithering. Minor: blog dated Dec 2022, cited as 2021. License claim accurate (pngquant/libimagequant GPLv3-or-commercial; Pillow HPND; algorithms public). [no external verdict — not checked]
- **Sources:** [Improving color quantization heuristics](http://blog.pkh.me/p/39-improving-color-quantization-heuristics.html) (Clement Beffa (ubitux), 2021) — Modified median-cut with k-means refinement and perceptual color weighting (as in libvips/pngquant) yields better palettes than plain median-cut, and quantization is paired with dithering to break up banding. ; [Color quantization — Wikipedia](https://en.wikipedia.org/wiki/Color_quantization) (Wikipedia contributors, 2025) — Median cut (Heckbert 1979) is the most popular quantization algorithm; it is frequently combined with dithering to eliminate banding artifacts when reducing smooth gradients to a limited palette.

### Supersample + Lanczos/area downsample (512 -> 48/64px) · `recommended` · ▸ reproduced
**Render at 8-10x target (512px for a 48-64px sprite), then box/area-filter or Lanczos downscale: area minimizes aliasing on flat fills, Lanczos keeps edges crisp — the baseline before any pixel-art-specific pass.**
Rendering at the target 48/64px directly aliases hard; instead render a 512px master and downsample. Area/box filtering widens the kernel proportionally to the scale factor, acting as a low-pass anti-alias filter — clean on large flat color regions. Lanczos (windowed-sinc) preserves sharp edges and detail but can ring (halos) on high-contrast borders. For sprites the common move is a hybrid: area/box for the body, then a sharpening or edge-preserving pass for the silhouette. This is the deterministic floor every other finishing technique builds on.
- **Engine:** python · **Applies to:** both · **Base:** n/a · **Kind:** post-process
- **VRAM:** 0 (CPU)
- **Output license:** commercial **yes** (license: algorithm public; common impls permissive (Pillow HPND, OpenCV Apache-2.0)) — Standard resampling math (Pillow/ImageMagick/OpenCV); no asset license. Pillow is HPND/permissive, ImageMagick Apache-2.0-ish, OpenCV Apache-2.0 — all commercial-safe.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| render scale | 8-10x target (512px for 48-64) | ○ | gives the filter enough samples to anti-alias |
| flat fills | area/box filter | ○ | best aliasing suppression on solid color regions |
| edges/silhouette | Lanczos | ○ | sharpest; watch for ringing halos on high contrast |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Halos/ringing around the outline after downscale | Lanczos overshoot on high-contrast edges | Use area filter or reduce Lanczos lobe count; clamp; or switch to edge-preserving downscaler |  |
| Sprite looks blurry/soft at 64px | bilinear default in editor instead of Lanczos/area | Force Lanczos or area resampling explicitly in the script |  |

- **Verify:** Both URLs resolve (200). Wikipedia Image scaling strongly confirms box sampling (area averaging, all input pixels contribute) and Lanczos as a windowed-sinc approximation sharper than bilinear/bicubic; ringing is mentioned (tied more to Fourier methods than Lanczos directly — minor). License claim accurate (algorithm public; Pillow HPND, OpenCV Apache-2.0). WEAK SOURCE: pixelera.art resolves but emphasizes Nearest Neighbor and does NOT mention box/area filtering, kernel widening, low-pass, or halo — the specific claim attributed to it is only loosely supported. Entry stands on the Wikipedia source plus universally-known technique. [no external verdict — not checked]
- **Sources:** [How to Scale Down Pixel Art: A Technical Deep Dive](https://pixelera.art/blog/how-to-scale-down-pixel-art) (Pixelera, 2024) — Box/area filtering merges adjacent pixels with a kernel widened by the scale factor to low-pass against aliasing, while Lanczos sharpens at the cost of halo artifacts. ; [Image scaling — Wikipedia](https://en.wikipedia.org/wiki/Image_scaling) (Wikipedia contributors, 2025) — Lanczos resampling uses a windowed sinc function giving sharper results than bilinear/bicubic but can introduce ringing; box filtering provides anti-aliased area averaging when downscaling.

### Orthographic camera + foot-anchor (bottom-center) registration · `recommended` · · community
**A fixed orthographic camera plus a known ground reference lets every direction and animation frame share a bottom-center pivot, so the engine's Y-sort and ground contact stay rock-solid across the turnaround.**
Place the model's feet on a fixed world origin and render with a locked orthographic camera per direction; because the camera and ground plane never move, the foot point lands at a predictable pixel each frame. Export with a consistent frame size (don't auto-crop to content, or uneven sprites shift the pivot) and set the engine pivot to bottom-center — the standard registration for Y-sorted 2.5D where the sort key is the sprite's feet. Godot/Unity/Bevy all support a bottom-center anchor or a per-frame draw-offset script; the render-side discipline (fixed frame, fixed ground, ortho camera) is what makes the engine side trivial.
- **Engine:** blender · **Applies to:** both · **Base:** n/a · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: n/a (technique)) — Render/engine technique; no asset license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| camera | orthographic, locked per direction | ○ | no perspective foot drift |
| frame export | fixed canvas, NOT auto-cropped | ○ | auto-crop to content moves the pivot between frames |
| engine pivot | bottom-center | ○ | matches Y-sort contact point |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Character bobs/shifts vertically between animation frames | per-frame auto-crop to content changes the foot pixel | Render to a fixed canvas size; keep feet on world origin |  |
| Wrong draw order around props (sprite in front/behind incorrectly) | pivot at center, not feet, so Y-sort uses the wrong contact point | Set pivot to bottom-center so the sort key is the ground contact |  |

- **Verify:** Both sources resolve. Godot forum thread exists; discusses uneven/auto-cropped spritesheets needing per-frame Sprite2D.offset/region fixes for consistent ground registration (bottom-pivot Y-sort context). Bevy PR #3463 exists and was merged 2022-04-04, adding a sprite anchor enum (common presets incl. edges + custom point, defaulting to center) — matches claim exactly. Technique; no license concern. [no external verdict — not checked]
- **Sources:** [Set sprite pivot to bottom instead of center on uneven spritesheets](https://forum.godotengine.org/t/set-sprites-pivot-to-bottom-instead-of-center-on-uneven-spritesheets/43612) (Godot community, 2024) — For Y-sorted 2D games the bottom-center pivot is desired as the sort point, and uneven (auto-cropped) spritesheets require a script to fix the per-frame draw offset. ; [Add an anchor for a sprite (Bevy PR #3463)](https://github.com/bevyengine/bevy/pull/3463) (mockersf / Bevy contributors, 2022) — Engines add an explicit sprite anchor enum (center plus custom/edge anchors) so registration can be set to bottom-center rather than the default center.

### Hiive adaptive pixel-art downscaler (majority-block + edge-preserving) · `situational` · · single-run
**An adaptive downscaler that blends a Lanczos base with majority-color block sampling and edge-detected masking preserves silhouette, shading, and transparency at 2-3x better than naive resize — but ships with NO license.**
The Hiive method (2025) creates a naive Lanczos/bilinear downscale, then runs majority-color block sampling (pick the most frequent color per NxN block, and make a block fully transparent if its majority is transparent) plus an edge-preserving pass (edge-detect the grayscale, use edges as a mask to retain critical detail), then merges via conditional replacement. The author reports it retains edges/shading/transparency far better than nearest-neighbor or bilinear, with 2x best for character sprites and 3x as small as you can go while keeping detail. The Python/Streamlit reference is at hiive/pixel_scale.
- **Engine:** python · **Applies to:** both · **Base:** n/a · **Kind:** post-process
- **VRAM:** 0 (CPU)
- **Output license:** commercial **unknown** (license: no license stated (all-rights-reserved by default); algorithm reimplementable) — DECISIVE CAVEAT: the hiive/pixel_scale repo has NO LICENSE FILE — by default that means all rights reserved, so you may NOT legally vendor or redistribute its code in a commercial pipeline without permission. The ALGORITHM (majority-block + edge mask) is described in the blog and is independently reimplementable; a clean-room reimplementation you write yourself is commercially safe. Do not copy their source.
- **Fit:** rig 4/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| base downscale | Lanczos / bilinear / bicubic | ○ | the smooth layer that gets selectively overwritten |
| block rule | majority color per block; transparent if majority transparent | ○ | preserves alpha cleanly |
| best scale | 2x (3x = practical floor) | ○ | author's reported sweet spot for character sprites |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Detail still lost at 4x | block size too large for the feature density | Stay at 2-3x; author notes 4x loses too much |  |
| Legal exposure shipping the tool | no license on the repo | Reimplement the described algorithm clean-room; do not redistribute hiive source |  |

- **Verify:** Both sources resolve (200). Hiive Labs blog confirms the adaptive downscaler: Lanczos/bilinear base + majority-color block sampling + edge-preserving mask, with 2x retaining most features for character sprites. GitHub hiive/pixel_scale exists (Python pix.py + Streamlit streamlit_main.py) and has NO LICENSE file — so 'no license stated, all-rights-reserved by default, commercial_use: unknown' is ACCURATE. License/commercial_use claim confirmed correct. [no external verdict — not checked]
- **Sources:** [Adaptive Downscaling of Pixel Art](https://hiivelabs.com/blog/gamedev/graphics/2025/01/19/adaptive-downscaling-pixel-art/) (Hiive Labs, 2025) — Combines a naive Lanczos/bilinear downscale with majority-color block sampling and edge-preserving masking to retain edges, shading, and transparency better than nearest-neighbor or bilinear; 2x works best for character sprites, 3x is the practical floor. ; [hiive/pixel_scale](https://github.com/hiive/pixel_scale) (hiive, 2025) — Python/Streamlit reference implementation of the adaptive downscaler; repository contains no LICENSE file, so reuse rights are unspecified (default all-rights-reserved).

### Aseprite CLI sheet export — packing hold-with-limit · `situational` · analog
**`-b` batch `--sheet` + sheet-type + JSON data — hold for deterministic sheet packing export; limit ≠ invent-verify 486.**
STUDY-059 Analogist #5 Verifier ✅ hold-with-limit. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [Aseprite CLI sheet export](https://www.aseprite.org/docs/cli/) — `-b` batch `--sheet` + sheet-type (rows/columns/packed) + JSON data.

### Aseprite CLI — sheet export surface · `situational` · docs
**`-b` `--sheet`/`--data`; sheet-type horizontal/vertical/rows/columns/packed — sheet-export surface; flip 486: 0.**
STUDY-059 Practitioner deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [Aseprite CLI](https://www.aseprite.org/docs/cli/) — `-b` `--sheet`/`--data`; sheet-type horizontal/vertical/rows/columns/packed.

### BLOCK — pixel-quant character-to-skin · `situational` · paper
**MLLM dual-panel preview to FLUX.2 atlas to nearest-neighbor 64x64 UV skin; EvolveLoRA curriculum — pixel-grid + integer-upsample lock.**
MLLM dual-panel preview to FLUX.2 atlas to nearest-neighbor 64x64 UV skin; EvolveLoRA curriculum — pixel-grid + integer-upsample lock.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [BLOCK — pixel-quant character-to-skin](https://arxiv.org/abs/2603.03964) — MLLM dual-panel preview to FLUX.2 atlas to nearest-neighbor 64x64 UV skin; EvolveLoRA curriculum — pixel-grid + integer-upsample lock.

### CSS image-rendering pixelated — display analog · `situational` · docs
**Nearest-neighbor upscale preserves hard pixel edges. Holds for display of finished pixel sprites.**
Nearest-neighbor upscale preserves hard pixel edges. Holds for display of finished pixel sprites.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [CSS image-rendering pixelated — display analog](https://developer.mozilla.org/en-US/docs/Web/CSS/image-rendering) — Nearest-neighbor upscale preserves hard pixel edges. Holds for display of finished pixel sprites.

### CSS image-rendering — pixelated / crisp-edges display peer · `situational` · docs
**`pixelated`/`crisp-edges` nearest-neighbor-class — display peer; flip 486: 0.**
STUDY-059 Practitioner deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [CSS image-rendering](https://developer.mozilla.org/en-US/docs/Web/CSS/image-rendering) — `pixelated`/`crisp-edges` nearest-neighbor-class.

### Heckbert median-cut — palette lock analog (paywall unverified) · `situational` · analog
**Choose one shared colormap; remap all pixels — hold for palette lock at 48–64px finish; limit ≠ inventing a named studio palette recipe.**
STUDY-059 Analogist #2 paywall unverified. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 Verifier: Analogist #1/#2 paywall unverified — do not land as verified. Flip 486: 0. [no external verdict — not checked]
- **Sources:** [Color image quantization for frame buffer display (median-cut)](https://dl.acm.org/doi/10.1145/800064.801294) — Median-cut shared colormap; remap all pixels to that table.

### Heckbert median-cut — palette quant analog · `situational` · docs
**Median-cut chooses a shared colormap; remap all pixels to that table. Holds for palette lock at 48-64px.**
Median-cut chooses a shared colormap; remap all pixels to that table. Holds for palette lock at 48-64px.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Heckbert median-cut — palette quant analog](https://dl.acm.org/doi/10.1145/800064.801294) — Median-cut chooses a shared colormap; remap all pixels to that table. Holds for palette lock at 48-64px.

### Pillow Concepts — LANCZOS downsample + palette modes · `situational` · docs
**`Resampling.LANCZOS` tops downscale table; mode `P` palette — downsample peer; flip 486: 0.**
STUDY-059 Practitioner deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [Pillow Concepts](https://pillow.readthedocs.io/en/stable/handbook/concepts.html) — `Resampling.LANCZOS` tops downscale table; mode `P` palette.

### Pillow LANCZOS / palette modes — downsample hold-with-limit · `situational` · analog
**High-quality Lanczos downsample + palette-indexed modes — hold for 512→48/64 + palette finish; limit ≠ verified flip of any avoid-row.**
STUDY-059 Analogist #3 Verifier ✅ hold-with-limit. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [Pillow Concepts — Resampling.LANCZOS / palette modes](https://pillow.readthedocs.io/en/stable/handbook/concepts.html) — Lanczos downsample; palette-indexed pixel modes.

### Pillow resampling — LANCZOS downsample · `situational` · docs
**Resampling.LANCZOS ranked highest downscale quality among listed filters; P mode = palette pixels.**
Resampling.LANCZOS ranked highest downscale quality among listed filters; P mode = palette pixels.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Pillow resampling — LANCZOS downsample](https://pillow.readthedocs.io/en/stable/handbook/concepts.html) — Resampling.LANCZOS ranked highest downscale quality among listed filters; P mode = palette pixels.

### SD-piXL — low-res quantized imagery · `situational` · paper
**SDS + Gumbel-softmax palette tensor for crisp HxW x n quantized pixel art from prompt/image.**
SDS + Gumbel-softmax palette tensor for crisp HxW x n quantized pixel art from prompt/image.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [SD-piXL — low-res quantized imagery](https://arxiv.org/abs/2410.06236) — SDS + Gumbel-softmax palette tensor for crisp HxW x n quantized pixel art from prompt/image.

### SD-πXL — SDS palette tensor quantized pixel art (Binninger & Sorkine-Hornung 2024) · `situational` · paper
**SDS palette tensor quantized pixel art — downsample-finish deepen; flip 486: 0.**
STUDY-059 Scholar deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** comfy · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [SD-πXL](https://arxiv.org/abs/2410.06236) — SDS palette tensor quantized pixel art.

### libGDX TexturePacker — atlas pack + .atlas · `situational` · docs
**Atlas pack + `.atlas`; padding/bleed — packing analog peer; flip 486: 0.**
STUDY-059 Practitioner deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [libGDX TexturePacker](https://libgdx.com/wiki/tools/texture-packer) — Atlas pack + `.atlas`; padding/bleed.

### libGDX TexturePacker — sheet packing hold-with-limit · `situational` · analog
**Pack many rects into one atlas; bind once, draw many — hold for sprite-sheet packing / row-per-anim metadata; limit ≠ diffusion invent.**
STUDY-059 Analogist #4 Verifier ✅ hold-with-limit. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [libGDX TexturePacker](https://libgdx.com/wiki/tools/texture-packer) — Pack many rects into one atlas; bind once, draw many.

