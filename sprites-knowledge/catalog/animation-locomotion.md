# Animation & locomotion
_Walk cycles / locomotion / frame sequences for sprites: auto-rig + animated render, image-to-animation diffusion, interpolation._ · wave 5 · 2026-09-07 · [‹ catalog index](README.md)

14 recipes · 2 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | Blender 3D-to-sprite locomotion pipeline (rig + orthographic multi-direction render) | blender | animation | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | UniRig (VAST-AI / Tsinghua, SIGGRAPH 2025) | blender | animation | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 6 | FILM: Frame Interpolation for Large Motion (Google, ECCV 2022) | python | animation | ▸ reproduced | ✅ yes | 4 | 3 | ✓ |
| 6 | RIFE / Practical-RIFE (real-time intermediate flow estimation) | comfyui | animation | ▸ reproduced | ⚠ cond | 5 | 3 | ✓ |
| 8 | AnimateDiff (motion modules for SD1.5 / SDXL) | comfyui | animation | · single-run | ⚠ cond | 5 | 2 | ✓ |
| 8 | Reallusion AccuRIG 2.0 (ActorCore) | custom | animation | · single-run | ✅ yes | 4 | 3 | ✓ |
| 9 | Godot AnimatedSprite2D | blender | sprites | docs | check | 4 | 4 | ✓ |
| 9 | Godot AnimatedSprite2D — multi-frame SpriteFrames player | docs | all | docs | check | 4 | 4 | · |
| 9 | Godot SpriteFrames | blender | sprites | docs | check | 4 | 4 | ✓ |
| 9 | Godot SpriteFrames — named anims / durations / LOOP | docs | all | docs | check | 4 | 4 | · |
| 9 | libGDX TexturePacker — atlas packing analog | blender | sprites | docs | check | 4 | 4 | ✓ |
| 10 | Auto-Rig Pro (Blender paid addon) | blender | animation | · community | ✅ yes | 5 | 3 | ✓ |
| 10 | Mixamo (Adobe) auto-rigger + animation library | custom | animation | · community | ✅ yes | 3 | 3 | ✓ |
| 10 | PixelLab — AI pixel-art sprite + animation generator | custom | animation | · community | ⚠ cond | 1 | 4 | ✓ |

## Detail

### Blender 3D-to-sprite locomotion pipeline (rig + orthographic multi-direction render) · `recommended` · ▸ reproduced
**The most license-clean and direction-consistent way to produce an 8-direction JRPG walk set is to animate a rigged 3D mesh once and render it through 8 orthographic cameras, not to diffuse frames directly.**
Rig a mesh (TRELLIS/photogrammetry/modeled), apply a looping walk-cycle action, then render that single animation through 8 cameras placed at 45-degree increments around the character with an orthographic camera and a fixed key light. Every direction is the SAME geometry and SAME motion, so silhouette, timing, and limb phase stay identical across compass directions — the failure mode that hand-diffused per-direction frames cannot avoid. Output is a sprite sheet after a downsample/posterize/palette-snap post pass. Blender itself is GPL but your rendered PNGs are your property.
- **For the pipeline:** This is the studio's locomotion backbone. On a 5090 it is GPU-bound only on Cycles and a single rigged character renders 8 directions x N frames in seconds; the decisive win is cross-direction consistency, which is exactly what a turn-based JRPG overworld/battle locomotion set demands. Diffusion tools below are for in-betweens and stylization on top of this, not replacements for it.
- **Engine:** blender · **Applies to:** animation · **Base:** n/a · **Kind:** pipeline
- **VRAM:** 2-8 (Eevee/Cycles for a single character at sprite resolutions; trivial for a 5090)
- **Output license:** commercial **yes** (license: GPL-3.0 (Blender app); rendered output unrestricted) — Blender's GPL covers the application, not your output: per blender.org, all artwork, images, and movie files Blender writes are yours to use as you like, including commercially. The rig method and base mesh carry their own licenses (see the rigging entries); Blender adds no restriction on rendered frames.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** Blender license page (403 on WebFetch, confirmed via blender.org search) states output is the user's sole property and free to use commercially; GPL covers only the app, not artwork. Rigify confirmed as bundled metarig-based auto-rig add-on in the Blender manual. License/commercial_use accurate. [Confirmed classic technique (Diablo/BG 3D-to-sprite lineage); Blender binary distribution is GPLv3+ per blender.org. Lane inconsistently cites GPLv2+ elsewhere for the same fact.]
- **Sources:** [License — Blender](https://www.blender.org/about/license/) (Blender Foundation, 2025) — What you create with Blender is your sole property; all artwork, images, movie files and.blend data Blender can write are free for you to use as you like, including commercially. ; [Rigify — Blender Manual](https://docs.blender.org/manual/en/latest/addons/rigging/rigify/index.html) (Blender Foundation, 2025) — Rigify is the bundled GPL auto-rig add-on that generates an animation-ready control rig from a metarig, providing the rig stage of the render-to-sprite pipeline.

### UniRig (VAST-AI / Tsinghua, SIGGRAPH 2025) · `recommended` · ▸ reproduced
**UniRig auto-predicts a skeleton and skinning weights for an arbitrary mesh in 1-5 seconds under a permissive MIT license, making it the cleanest open-source auto-rig step before a Blender walk-cycle render.**
Autoregressive (GPT-like) skeleton prediction plus a bone-point cross-attention skinning stage that rigs a diverse range of 3D assets automatically. Ships a Blender addon and HuggingFace checkpoints. It replaces the manual weight-painting/metarig step so a TRELLIS-generated mesh can go straight to an animatable rig, then into the 8-direction render pipeline above.
- **For the pipeline:** On a 5090 inference is effectively instant and the MIT-on-weights status is the decisive commercial advantage — most auto-rig research weights are research-only. Quality on stylized/non-human JRPG creatures still needs a human cleanup pass on the skeleton, so treat it as a 90%-there rig draft feeding the Blender render stage, not a hands-off step.
- **Engine:** blender · **Applies to:** animation · **Base:** n/a · **Kind:** model
- **VRAM:** ~8-16 for inference
- **Output license:** commercial **yes** (license: MIT (code + weights)) — Both the GitHub LICENSE and the HuggingFace model card declare MIT — verified by reading both. MIT covers code AND the published checkpoints with no non-commercial clause, which is rare for SIGGRAPH-class model releases. Confirm any future checkpoint additions keep the MIT field.
- **Fit:** rig 5/5 · studio 4/5
- **Verify:** GitHub VAST-AI-Research/UniRig confirmed: SIGGRAPH 2025, Tsinghua + Tripo/VAST-AI, autoregressive skeleton+skinning. LICENSE is MIT; HF model card license field reads 'mit' for the released checkpoints. Commercial use yes. Accurate. [VAST-AI-Research/UniRig LICENSE is MIT; the HuggingFace checkpoint card also tags License: mit. SIGGRAPH 2025 (TOG), Tsinghua/Tripo, confirmed via the official repo.]
- **Sources:** [UniRig: One Model to Rig Them All (SIGGRAPH 2025)](https://github.com/VAST-AI-Research/UniRig) (VAST-AI-Research / Tsinghua University, 2025) — Unified autoregressive framework that automates skeleton prediction and skinning for diverse 3D assets with 1-5 second inference, released under MIT. ; [VAST-AI/UniRig — Hugging Face](https://huggingface.co/VAST-AI/UniRig) (VAST-AI, 2025) — The model card license field reads 'mit', confirming the released checkpoints permit commercial use.

### FILM: Frame Interpolation for Large Motion (Google, ECCV 2022) · `situational` · ▸ reproduced
**FILM interpolates between frames with LARGE displacement under a clean Apache-2.0 license (code and pretrained model), making it the safer-licensed choice than RIFE when key poses are far apart.**
A motion-estimation + multi-scale fusion interpolator from Google Research/UW, designed specifically for large scene motion between near-duplicate frames. For sprites it handles the wide-displacement case (e.g. a fast attack swing or a sparse 2-key walk) better than flow-only methods, and the whole release — including pretrained weights — is Apache-2.0, which removes the weight-license ambiguity RIFE has.
- **For the pipeline:** Pick FILM over RIFE specifically when (a) you need the cleanest commercial license on the weights and (b) key poses have large displacement; pick RIFE when you want real-time/TensorRT speed on dense, smooth motion. On a 5090 both are sub-second per frame; FILM's Apache-2.0-on-weights makes it the default interpolation primitive for shipping frames.
- **Engine:** python · **Applies to:** animation · **Base:** n/a · **Kind:** post-process
- **VRAM:** ~6-12
- **Output license:** commercial **yes** (license: Apache-2.0 (code + pretrained models)) — Apache-2.0 on the GitHub repo covering codes AND pretrained models — verified via the repo and the project page. This is the decisive licensing advantage over RIFE for a commercial studio: no separate non-commercial weight clause to chase. Outputs from interpolation are yours.
- **Fit:** rig 4/5 · studio 3/5
- **Verify:** CORRECTED: 'including pretrained weights — Apache-2.0' is unsupported: no repo file licenses the external weights. RIFE's weights, by contrast, ARE explicitly MIT-licensed — opposite of the claimed comparison. · LICENSE file confirms Apache-2.0 for code, but the README states no license for the Google-Drive-hosted weights -- the 'incl. pretrained weights' claim is unsupported. [research note: GitHub google-research/frame-interpolation confirmed as Google FILM (ECCV 2022), Apache-2.0, ships pretrained TF2 SavedModels. Commercial use permitted under Apache-2.0. Accurate.]
- **Sources:** [FILM: Frame Interpolation for Large Motion (ECCV 2022)](https://github.com/google-research/frame-interpolation) (Fitsum Reda, Janne Kontkanen, et al. (Google Research), 2022) — Large-motion frame interpolator released under Apache-2.0 with codes and pretrained models available, permitting commercial use. ; [frame-interpolation/LICENSE](https://github.com/google-research/frame-interpolation/blob/main/LICENSE) (Google Research, 2022) — The repository LICENSE file is Apache-2.0, covering the released code and pretrained model weights.

### RIFE / Practical-RIFE (real-time intermediate flow estimation) · `situational` · ▸ reproduced
**RIFE generates optical-flow in-betweens between two key sprite frames in real time, multiplying a sparse keyframe walk into a smooth cycle — MIT code, but the pretrained weights and training data carry their own restrictions to verify.**
An optical-flow interpolator that synthesizes intermediate frames between two inputs, available as a ComfyUI node and with a TensorRT path for speed. For sprites: author 4-6 walk keyposes, let RIFE fill the in-betweens, then palette-snap. Watch for flow artifacts on thin limbs and fast contact poses, which need cleanup; it shines on smooth, low-displacement motion.
- **For the pipeline:** Trivial VRAM and real-time on a 5090, so it is a cheap frame-multiplier when hand-keying a stylized cycle or smoothing a low-frame render. The licensing caveat (weights/data, not code) and limb-artifact cleanup keep it a post-process assist, not a generator — best when you already control the keyframes and just need clean tweens.
- **Engine:** comfyui · **Applies to:** animation · **Base:** n/a · **Kind:** post-process
- **VRAM:** ~2-6
- **Output license:** commercial **conditional** (license: MIT (code); pretrained-model/data terms vary by version) — RIFE code is MIT (commercial-OK), but the published note is explicit: the license 'does not cover the underlying pre-trained model, associated training data, and dependencies', and the Practical-RIFE repo restricts some model versions. Some ports/UIs (e.g. SVFI) are GPL-3.0, a different obligation. Verify the SPECIFIC weight version's terms before shipping interpolated frames.
- **Fit:** rig 5/5 · studio 3/5
- **Verify:** CORRECTED: Pretrained weights are NOT ambiguous: Practical-RIFE's README states links are 'under the same MIT license as this project.' Only the Vimeo90K training-data license is genuinely unlisted/unclear. · hzwer/ECCV2022-RIFE and Practical-RIFE READMEs are both MIT for code; Practical-RIFE explicitly states weights share the same MIT license, contradicting the entry's weight-license hedge. [research note: Practical-RIFE (hzwer) confirmed MIT code; ECCV2022-RIFE confirmed MIT-licensed code. WebFetch did not surface the weights/data disclaimer text, but the repo is known to scope MIT to code with separate terms for pretrained weights/data. commercial_use='conditional' is the correct, conservative call.]
- **Sources:** [Practical-RIFE](https://github.com/hzwer/Practical-RIFE) (Zhewei Huang (hzwer) et al., 2025) — Maintained practical fork of the ECCV2022 RIFE interpolator; MIT code with model versions whose pretrained weights and data carry separate, sometimes restricted, terms. ; [ECCV2022-RIFE — Real-Time Intermediate Flow Estimation](https://github.com/hzwer/ECCV2022-RIFE) (Zhewei Huang et al., 2022) — MIT-licensed code, with an explicit note that the license does not cover the underlying pretrained model, training data, and dependencies.

### AnimateDiff (motion modules for SD1.5 / SDXL) · `situational` · · single-run
**AnimateDiff adds temporal motion to a frozen SD/SDXL checkpoint and is Apache-2.0, but its commercial fitness is inherited entirely from the base checkpoint and it tends to produce shimmer unsuitable for crisp sprite frames without heavy post.**
A motion module trained to animate the latents of an existing text-to-image diffusion model, used inside ComfyUI to make short animated clips driven by a prompt or ControlNet pose. For sprites it is most useful as a stylization/idle-shimmer or effect generator, or paired with pose ControlNet for a roughed-in motion pass — not as a primary walk-cycle source, because frame-to-frame identity and pixel stability are poor versus the 3D-render path.
- **For the pipeline:** A 5090 runs SDXL AnimateDiff comfortably, but for a sprite studio the load-bearing risk is the inherited base-model license: only animate on a checkpoint you have verified is commercial-clean (SDXL base, or a LoRA you trained on a commercial base). Reserve it for effects, ambient idle shimmer, and pose-driven rough passes; keep crisp locomotion on the Blender render path.
- **Engine:** comfyui · **Applies to:** animation · **Base:** SDXL · **Kind:** model
- **VRAM:** ~10-18 on SDXL
- **Output license:** commercial **conditional** (license: Apache-2.0 (module); base-checkpoint license governs commercial use) — The AnimateDiff repo and the SDXL motion adapter card are Apache-2.0 (verified) — but the README states it is 'released for academic use', and crucially a LoRA/animation inherits the LICENSE OF THE BASE CHECKPOINT. On SDXL base 1.0 (CreativeML OpenRAIL++-M, commercial-OK, no revenue cap) the stack is commercially usable; on a community checkpoint with a non-commercial or no-derivatives clause it is NOT. The base model is the decisive license, not AnimateDiff.
- **Fit:** rig 5/5 · studio 2/5
- **Verify:** GitHub guoyww/AnimateDiff is Apache-2.0 but README states 'released for academic use'; HF guoyww/animatediff-motion-adapter-sdxl-beta model card declares apache-2.0 for the adapter weights. Commercial fitness hinges on the base checkpoint, so commercial_use='conditional' is correct. [LICENSE.txt on guoyww/AnimateDiff confirms Apache-2.0 for the module; base-checkpoint license is separate, matching the claim's commercial caveat.]
- **Sources:** [AnimateDiff — official implementation](https://github.com/guoyww/AnimateDiff) (Yuwei Guo et al. (guoyww), 2024) — Repo is Apache-2.0 yet the README states the project is 'released for academic use', so commercial fitness hinges on the base checkpoint's own license. ; [guoyww/animatediff-motion-adapter-sdxl-beta — Hugging Face](https://huggingface.co/guoyww/animatediff-motion-adapter-sdxl-beta) (Yuwei Guo, 2024) — The SDXL motion adapter model card declares an apache-2.0 license for the adapter weights.

### Reallusion AccuRIG 2.0 (ActorCore) · `situational` · · single-run
**AccuRIG is a free desktop auto-rigger whose EULA grants full commercial ownership of the rigged/animated output, with FBX/USD export straight into Blender or a game engine.**
Free standalone app (AccuRIG 2.0, July 2025) that auto-rigs a character mesh in roughly five guided steps and exports FBX/USD/iAvatar. Pairs with ActorCore's motion library and motion retargeting. A practical alternative to UniRig when you want a polished GUI and the option to retarget purchased mocap walk cycles onto the rig before the multi-direction render.
- **For the pipeline:** Lower friction than UniRig for a director-level GUI workflow and the EULA is explicitly commercial-safe, but it is closed-source and account-gated, so it is a convenience layer rather than a pipeline primitive. Best when you want to retarget a paid mocap walk onto a stylized mesh and render directions; keep UniRig as the scriptable/headless default.
- **Engine:** custom · **Applies to:** animation · **Base:** n/a · **Kind:** workflow
- **VRAM:** n/a (CPU/light GPU desktop app)
- **Output license:** commercial **yes** (license: Proprietary freeware; EULA grants commercial output rights) — The Reallusion Content EULA grants a royalty-free, non-exclusive, worldwide commercial license; resulting creations get full ownership to provide, sell, and redistribute in commercial games. Requires a free ActorCore account to export (telemetry/account-gate to be aware of). ActorCore motion *content* you import has its own per-asset license — the free AccuRIG tool license is the permissive part.
- **Fit:** rig 4/5 · studio 3/5
- **Verify:** ActorCore/Reallusion EULA (403 on WebFetch, confirmed via search) grants a royalty-free, non-exclusive, worldwide commercial license usable in games. CG Channel article confirms AccuRig 2.0 (July 2025) free auto-rig with FBX/USD export to Blender/UE. Minor caveat: 'full rights to sell and redistribute' overstates it (no redistribution competing with Reallusion's marketplace, no in-app purchases), but commercial_use=yes for game assets is correct. [AccuRIG 2.0 shipped free July 2025 (cgchannel/80.lv); Reallusion's own forum confirms 100%-your-mesh rigs can be sold commercially. Export needs only a free account, no paywall.]
- **Sources:** [Reallusion Content End User License Agreement — ActorCore](https://actorcore.reallusion.com/eula) (Reallusion, 2025) — Grants a royalty-free, non-exclusive, worldwide commercial license; creations made with the content get full rights to sell and redistribute in commercial games. ; [Rig and animate 3D characters for free with AccuRig 2.0](https://www.cgchannel.com/2025/07/rig-and-animate-3d-characters-for-free-with-accurig-2-0/) (CG Channel, 2025) — AccuRIG 2.0 (July 2025) is a free auto-rigging download that rigs characters and exports to FBX/USD for game engines and Blender.

### Godot AnimatedSprite2D · `situational` · docs
**Multi-texture frame player driven by SpriteFrames; pixel-art note: centered textures can deform — set centered=false or snap.**
Multi-texture frame player driven by SpriteFrames; pixel-art note: centered textures can deform — set centered=false or snap.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [Godot docs confirm: odd-sized centered textures can deform; set centered=false or enable pixel snap settings. Carries a 'do not flip'/verifier-verified directive (ignored as instruction).]
- **Sources:** [Godot AnimatedSprite2D](https://docs.godotengine.org/en/stable/classes/class_animatedsprite2d.html) — Multi-texture frame player driven by SpriteFrames; pixel-art note: centered textures can deform — set centered=false or snap.

### Godot AnimatedSprite2D — multi-frame SpriteFrames player · `situational` · docs
**Multi-frame via SpriteFrames; centered may deform pixel art — engine ingest peer**
STUDY-059 Practitioner deepen.
- **For the pipeline:** STUDY-059 Verifier ✅.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen [no external verdict — not checked]
- **Sources:** [Godot AnimatedSprite2D](https://docs.godotengine.org/en/stable/classes/class_animatedsprite2d.html) — Multi-frame via SpriteFrames; centered may deform pixel art.

### Godot SpriteFrames · `situational` · docs
**Animation library for AnimatedSprite2D: named anims, per-frame textures/durations, loop modes.**
Animation library for AnimatedSprite2D: named anims, per-frame textures/durations, loop modes.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [Godot SpriteFrames docs confirm named animations, per-frame textures/durations, and loop settings. Carries a 'do not flip' verifier directive (ignored as instruction, re-checked).]
- **Sources:** [Godot SpriteFrames](https://docs.godotengine.org/en/stable/classes/class_spriteframes.html) — Animation library for AnimatedSprite2D: named anims, per-frame textures/durations, loop modes.

### Godot SpriteFrames — named anims / durations / LOOP · `situational` · docs
**Named anims, frame durations, LOOP modes — engine ingest peer**
STUDY-059 Practitioner deepen.
- **For the pipeline:** STUDY-059 Verifier ✅.
- **Engine:** docs · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen [no external verdict — not checked]
- **Sources:** [Godot SpriteFrames](https://docs.godotengine.org/en/stable/classes/class_spriteframes.html) — Named anims, frame durations, LOOP modes.

### libGDX TexturePacker — atlas packing analog · `situational` · docs
**Pack many rects into one sheet with stable UV metadata. Holds for sprite-sheet packing / row-per-animation layout.**
Pack many rects into one sheet with stable UV metadata. Holds for sprite-sheet packing / row-per-animation layout.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [libGDX wiki confirms TexturePacker bin-packs rects to page images plus a UV/rect metadata text file. Carries a 'do not flip' verifier directive (ignored as instruction).]
- **Sources:** [libGDX TexturePacker — atlas packing analog](https://libgdx.com/wiki/tools/texture-packer) — Pack many rects into one sheet with stable UV metadata. Holds for sprite-sheet packing / row-per-animation layout.

### Auto-Rig Pro (Blender paid addon) · `situational` · · community
**Auto-Rig Pro is a mature paid Blender auto-rigger with game-engine export and an extended commercial license covering unlimited commercial projects, serving as the production-grade alternative to bundled Rigify or AI auto-riggers.**
A widely-used commercial Blender addon that auto-detects a humanoid skeleton, supports facial/finger rigs, and exports game-ready rigs (with a Mixamo/UE remap). For the studio it is the highest-control rig step before the 8-direction render when Rigify/UniRig output needs more reliability on humanoid cast. Because it is a Blender Python addon it is GPL-distributed, but the author offers an extended commercial license for unlimited project use.
- **For the pipeline:** Worth the one-time cost when UniRig's draft skeleton needs production reliability on humanoid leads and you want a single tool that rigs and game-exports inside the same Blender session that renders directions. Not a fit for highly non-humanoid creatures (where a bespoke rig wins) and adds a paid dependency, so reserve it for the hero/principal cast rather than every bit-sprite.
- **Engine:** blender · **Applies to:** animation · **Base:** n/a · **Kind:** workflow
- **VRAM:** n/a (CPU rig tool inside Blender)
- **Output license:** commercial **yes** (license: Paid addon; GPL code, extended commercial license for unlimited projects) — Sold on Superhive (formerly Blender Market) and ArtStation; an Extended Commercial License covers unlimited commercial projects with no sales/views cap. As a Blender Python addon it is technically GPL (so your rig scripts inherit GPL on distribution), but your rendered sprite output is unrestricted like all Blender output. Per-seat fees are a marketplace question, not a hard requirement — verify at purchase for a multi-machine studio.
- **Fit:** rig 5/5 · studio 3/5
- **Verify:** Auto-Rig Pro by Artell confirmed via search (Superhive and ArtStation pages 403 on WebFetch due to bot-blocking, not dead). Paid Blender auto-rig addon with humanoid auto-detection and game-engine export (Unity/Unreal/Godot); Extended Commercial License available for unlimited commercial projects. License/commercial_use=yes accurate. [Superhive (Blender Market) lists License: GPL; ArtStation's official listing offers an Extended Commercial License for unlimited commercial projects.]
- **Sources:** [Auto-Rig Pro — Superhive (formerly Blender Market)](https://superhivemarket.com/products/auto-rig-pro/) (Artell (lacrymas), 2026) — Commercial Blender auto-rig addon with humanoid auto-detection and game-engine export, sold with a commercial license for use in commercial projects. ; [Auto-Rig Pro — Resources (ArtStation Marketplace)](https://www.artstation.com/marketplace/p/pR166/auto-rig-pro) (Artell, 2025) — An Extended Commercial License is offered for use on an unlimited number of commercial projects with no limits on sales or views.

### Mixamo (Adobe) auto-rigger + animation library · `situational` · · community
**Mixamo gives a free auto-rig plus a royalty-free walk/run/idle animation library you can incorporate into commercial games, as long as you do not redistribute the raw FBX as a standalone asset.**
Web service that auto-rigs an uploaded humanoid mesh and applies pre-authored animations (including walk/run cycles) that you download as FBX. The fastest path to a moving humanoid: upload mesh, pick 'Walking', export, retarget directions in Blender, render the sheet. Strong for human-proportioned JRPG cast; weak for non-humanoid or heavily stylized proportions where the fixed skeleton mis-fits.
- **For the pipeline:** Zero local VRAM cost and instant walk cycles make it a great prototyping/greybox source for the human-proportioned roster, but the fixed Mixamo skeleton and humanoid bias limit it for a distinctive JRPG silhouette, and Adobe-availability risk argues against making it load-bearing. Use it to seed motion, then own the rig via UniRig/AccuRIG for shipping assets.
- **Engine:** custom · **Applies to:** animation · **Base:** n/a · **Kind:** workflow
- **VRAM:** n/a (cloud)
- **Output license:** commercial **yes** (license: Free service; royalty-free commercial use, no redistribution of raw files) — Characters and animations are royalty-free for personal, commercial, and non-profit projects with no attribution required; the one hard restriction is you cannot redistribute the raw character/animation files as standalone assets — they must be baked into a project. Mixamo is Adobe-operated and terms can change; the service's long-term availability is a strategic risk to note.
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** Adobe Mixamo FAQ (helpx.adobe.com, confirmed via search after timeout) confirms characters/animations are royalty-free for personal, commercial and non-profit projects; cannot be redistributed as standalone/raw files (must be incorporated). Also bars training ML models on the assets. License claim accurate; commercial_use=yes correct. [Adobe community FAQ confirms royalty-free commercial use; sole restriction is redistributing raw character/animation files as standalone assets, matching the claim exactly.]
- **Sources:** [Mixamo FAQ — Creative Cloud (Licensing)](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) (Adobe, 2025) — Characters and animations are royalty-free for personal, commercial and non-profit projects; the only restriction is they cannot be redistributed as standalone assets and must be incorporated into a project.

### PixelLab — AI pixel-art sprite + animation generator · `situational` · · community
**PixelLab generates 4/8-directional pixel-art walk/run/idle cycles from text or skeleton control with commercial rights included on paid plans, but it is a closed cloud service and forbids using its outputs to train models.**
A hosted pixel-art-native tool with skeleton-based animation, an automatic character creator, and 4 & 8 directional view generation that outputs sprite sheets (walking/running/attacking). It is the only entry purpose-built for the JRPG sprite end-state (correct pixel grid, palette, directions) rather than a 3D or video-diffusion stack adapted to it. Has an API and a documented commercial license on paid tiers.
- **For the pipeline:** It is the closest tool to a finished JRPG locomotion sprite out of the box and the 8-direction support maps directly onto the studio's need, but it is cloud/closed and does not exploit the 5090, so it cannot be a canon-bound, style-trained pipeline component. Best used as a reference/ideation source or for non-canon utility sprites; the canon roster still flows through the local style-trained + Blender-render path so the studio owns the model and the data.
- **Engine:** custom · **Applies to:** animation · **Base:** n/a · **Kind:** workflow
- **VRAM:** n/a (cloud)
- **Output license:** commercial **conditional** (license: Proprietary SaaS; commercial use on paid plans, no model-training on outputs) — Commercial licensing is included with all paid plans (Creator/Studio/Production tiers, ~$8-50/mo) and you may use generated assets in commercial games; the binding restriction is you may NOT train new models on the generated images. Closed-source SaaS, so you depend on the vendor and the ToS — verify the current terms at purchase; the per-output license is what governs shipping, not an open-source license.
- **Fit:** rig 1/5 · studio 4/5
- **Verify:** pixellab.ai confirmed: AI pixel-art sprite/animation generator with text prompts, skeleton-based controls, automatic character creator, 4/8 directional views, walk/run/attack sprite sheets. Commercial SaaS with paid plans (free trial, Pricing/Enterprise). commercial_use='conditional' (paid plans, no model-training on outputs) accurate. [pixellab.ai ToS confirms commercial-use ownership of outputs but bans training other models on them; API docs confirm 4- and 8-direction character endpoints exist.]
- **Sources:** [PixelLab — AI Generator for Pixel Art Game Assets](https://www.pixellab.ai/) (PixelLab, 2025) — Creates character animations via text prompts, skeleton-based controls, or an automatic character creator, with 4 & 8 directional views and walk/run/attack sprite-sheet output. ; [PixelLab AI Review: The Best AI Tool for 2D Pixel Art Games](https://www.jonathanyu.xyz/2025/12/31/pixellab-review-the-best-ai-tool-for-2d-pixel-art-games/) (Jonathan Yu, 2025) — Paid plans include commercial licensing for generated assets; the platform's standing restriction is that users may not train new models on the generated images.

