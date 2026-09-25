# Catalog — sprite-motion recipes (architecture · rigging · AI-motion · inbetween · cloud · combat · verify)

Generated from `recipes.db` · wave 8 · 2026-09-07. NEVER hand-edited — regenerated from the DB.

The portable **animate-the-sprite** craft for this rig (RTX 5090 · Blackwell · 32 GB · Win 11 / WSL2) — the motion layer atop [sprites-knowledge](../../sprites-knowledge/catalog/README.md) (static 2.5D sprite generation). The spine is **motion truth (rig/mesh/proxy) -> AI polish -> sprite-sheet export -> verify**. Sibling KBs own the layers this one points at: [model-knowledge](../../model-knowledge/catalog/README.md) (the *weights*) · [tensor-engine-knowledge](../../tensor-engine-knowledge/catalog/README.md) (the *software* + rig-measured receipts) · [blender-knowledge](../../blender-knowledge/catalog/README.md) (Blender 4.x recipes) — linked via `engine_recipe_ref` / `base_model_slug`, never restated.

## Proven on-rig

Recipes whose `evidence_strength` is ▣ **measured-on-rig** — validated on this exact machine.

| Lane | Recipe | Engine | Applies | Comm | Validated under | ✓ |
|---|---|---|---|---|---|---|
| Rigging & skeletons | High-fidelity TRELLIS decimate with sliver cleanup (the fix for ribbon/shard armor artifacts) | blender | rigging | ✅ yes | RTX 5090 / Blender 5.0.1; blackguard.glb 817k verts/992k tris -> 150k-tri collapse -> cleanup -> 148k verts/149k tris (97,341 removed); UniRig WSL2 re-rig (28-bone skeleton + learned skin). | · |
| Rigging & skeletons | Pose rigid plate armor on a learned auto-rig: ROM cap + DQS bake + skin rigidify | blender | rigging | ✅ yes | RTX 5090 / Blender 5.0.1; blackguard hifi rig (28 bones); elbow cap 70deg, DQS preserve_volume, rigidify 0.75 on limb-armor verts; cross-family jury front 0/3 -> 2/3. | · |
| Rigging & skeletons | Rigid weapon on a hand→weapon_grip→weapon_tip bone chain | blender | rigging | ✅ yes |  | ✓ |
| Rigging & skeletons | TRELLIS.2-4B mesh → Blender rig → 8-dir sprite render pipeline | blender | rigging | ✅ yes |  | · |
| Rigging & skeletons | UniRig auto-rig (skeleton + learned skin) on RTX 5090 sm_120 via WSL2 — MEASURED | huggingface | rigging | ✅ yes |  | · |
| Motion verification & QA | Anchor the cross-family vision jury with a bug-free reference image (kill false positives on dark/ornate characters) | n/a | all-motion | ✅ yes | ollama-cloud jury (minimax-m3 / kimi-k2.6 / gemini-3-flash canary), refute-by-default 2-of-3; blackguard clean hifi rig fails rest+guard on hallucinated defects contradicted by full-res inspection. | · |

## Recommended shortlist

Top `recommended` / `runner-up` picks per lane, by try-first order. `Evidence` ▣ measured-on-rig is the strongest tier.

| Lane | ↓ | Recipe | Engine | Applies | Evidence | Comm | ✓ |
|---|---|---|---|---|---|---|---|
| Motion architecture & contracts | 2 | [Godot 4 consumption pattern (AnimatedSprite2D + Skeleton2D / Spine runtime)](motion-arch.md) | n/a | godot4-integration | ▸ reproduced | ✅ yes | ✓ |
| Motion architecture & contracts | 2 | [Motion cage rendered per direction (8-view orthographic batch)](motion-arch.md) | blender | rig-proxy-lane | ▸ reproduced | ✅ yes | ✓ |
| Motion architecture & contracts | 2 | [Per-character animation contract (manifest)](motion-arch.md) | n/a | all-motion | ▸ reproduced | ✅ yes | ✓ |
| Motion architecture & contracts | 2 | [Sprite-sheet packing and atlas layout (JSON-hash / row-per-animation)](motion-arch.md) | n/a | all-motion | ▸ reproduced | ✅ yes | ✓ |
| Motion architecture & contracts | 2 | [UE5 Paper2D consumption pattern (Sprites + Flipbooks)](motion-arch.md) | n/a | ue5-integration | ▸ reproduced | ⚠ cond | ✓ |
| Motion architecture & contracts | 6 | [3-lane production model (rig-proxy / AI-polish / manual-keyframe)](motion-arch.md) | n/a | all-motion | · community | ✅ yes | ✓ |
| Motion architecture & contracts | 6 | [8-direction consistency strategy (5 unique + 3 mirrored)](motion-arch.md) | n/a | all-motion | · community | ✅ yes | ✓ |
| Motion architecture & contracts | 6 | [JRPG frame budget table (idle/walk/attack/hurt/death)](motion-arch.md) | n/a | all-motion | · community | ✅ yes | ✓ |
| Motion architecture & contracts | 6 | [Layer separation strategy (body / weapon / shadow / fx)](motion-arch.md) | n/a | all-motion | · community | ✅ yes | ✓ |
| Rigging & skeletons | 1 | [High-fidelity TRELLIS decimate with sliver cleanup (the fix for ribbon/shard armor artifacts)](rigging.md) | blender | rigging | ▣ measured | ✅ yes |  |
| Rigging & skeletons | 1 | [Pose rigid plate armor on a learned auto-rig: ROM cap + DQS bake + skin rigidify](rigging.md) | blender | rigging | ▣ measured | ✅ yes |  |
| Rigging & skeletons | 1 | [Rigid weapon on a hand→weapon_grip→weapon_tip bone chain](rigging.md) | blender | rigging | ▣ measured | ✅ yes | ✓ |
| Rigging & skeletons | 1 | [TRELLIS.2-4B mesh → Blender rig → 8-dir sprite render pipeline](rigging.md) | blender | rigging | ▣ measured | ✅ yes |  |
| Rigging & skeletons | 1 | [UniRig auto-rig (skeleton + learned skin) on RTX 5090 sm_120 via WSL2 — MEASURED](rigging.md) | huggingface | rigging | ▣ measured | ✅ yes |  |
| Rigging & skeletons | 2 | [Auto-rigger license landscape: UniRig MIT vs Rigify GPL vs AccuRIG EULA vs Auto-Rig Pro paid vs Mixamo NC-redistribute](rigging.md) | n/a | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [Rigify — Blender's bundled modular auto-rigger](rigging.md) | blender | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [UniRig Hugging Face checkpoints: what is actually downloadable vs. coming soon](rigging.md) | huggingface | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [UniRig SIGGRAPH 2025 / ACM TOG paper: arXiv:2504.12451, DOI 10.1145/3730930](rigging.md) | custom | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [UniRig commercial license: MIT on code AND released HuggingFace checkpoints](rigging.md) | n/a | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [UniRig community adoption and real-pipeline usage evidence (2025-2026)](rigging.md) | python | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [UniRig in the studio flow: TRELLIS.2 mesh → UniRig rig → weapon_grip chain → Blender 8-dir render](rigging.md) | blender | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [UniRig input mesh requirements and output format spec](rigging.md) | huggingface | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [UniRig redistribution, sublicensing, and commercial derivative works under MIT](rigging.md) | n/a | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [UniRig skeleton tree tokenization: DFS ordering + 256-bin coordinate discretization](rigging.md) | huggingface | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [UniRig stage 1: OPT-125M autoregressive skeleton GPT over 3DShape2Vecset geometry encoding](rigging.md) | huggingface | rigging | ▸ reproduced | ✅ yes | ✓ |
| Rigging & skeletons | 2 | [UniRig stage 2: bone-point cross-attention skinning with geodesic distance refinement](rigging.md) | huggingface | rigging | ▸ reproduced | ⚠ cond | ✓ |
| Rigging & skeletons | 4 | [UniRig inference speed: 1-5 second end-to-end rigging claim vs. commercial baselines](rigging.md) | huggingface | rigging | · single-run | ✅ yes | ✓ |
| Rigging & skeletons | 4 | [UniRig — VAST-AI/Tsinghua autoregressive skeleton predictor (SIGGRAPH 2025, MIT)](rigging.md) | huggingface | rigging | · single-run | ⚠ cond | ✓ |
| Rigging & skeletons | 6 | [Auto-Rig Pro — paid Blender add-on for rigging + mocap retargeting](rigging.md) | blender | rigging | · community | ✅ yes | ✓ |
| Rigging & skeletons | 6 | [Blender NLA strip + orthographic multi-camera sprite-sheet render](rigging.md) | blender | rigging | · community | ✅ yes | ✓ |
| Rigging & skeletons | 6 | [Blender humanoid armature bone hierarchy for 2.5D sprite motion](rigging.md) | blender | rigging | · community | ✅ yes | ✓ |
| Rigging & skeletons | 6 | [UniRig on non-humanoid / exotic meshes — decisive advantage, honest quality ceiling](rigging.md) | blender | rigging | · community | ✅ yes | ✓ |
| Rigging & skeletons | 6 | [UniRig skeleton cleanup workflow — the manual pass every non-humanoid needs](rigging.md) | blender | rigging | · community | ✅ yes | ✓ |
| Rigging & skeletons | 6 | [UniRig skeleton → mocap retarget: non-standard bone-name remap via ARP Remap or Blender Retarget addon](rigging.md) | blender | rigging | · community | ✅ yes | ✓ |
| Rigging & skeletons | 8 | [AccuRIG 2 — Reallusion free auto-rigger with ActorCore motion library](rigging.md) | custom | rigging | · community | ✅ yes | ✓ |
| AI motion models | 2 | [ControlNet OpenPose / DWPose — pose-driven repaint pass](ai-motion.md) | comfyui | walk, idle, attack, hurt, death — POSE REPAINT only; rigid props still require separate rig layer | ▸ reproduced | ⚠ cond | ✓ |
| AI motion models | 4 | [Qwen-Image-Edit-2511 — painterly style repaint / face-preserve pass](ai-motion.md) | python | style recovery, face-preserve repaint, idle/walk frame polish — all animation stages after proxy render | · single-run | ✅ yes | ✓ |
| Inbetweening & interpolation | 2 | [ComfyUI-Frame-Interpolation (Fannovel16) — production integration node](inbetween.md) | comfyui | walk-cycle, attack-swing, any-sprite-animation, comfyui-pipeline | ▸ reproduced | ⚠ cond | ✓ |
| Inbetweening & interpolation | 2 | [FILM: Frame Interpolation for Large Motion (Google, ECCV 2022)](inbetween.md) | python | attack-swing, dodge-burst, sparse-2-key-poses, large-displacement | ▸ reproduced | ✅ yes | ✓ |
| Inbetweening & interpolation | 4 | [Large-displacement vs smooth-displacement: FILM vs RIFE decision principle](inbetween.md) | n/a | attack-swing, walk-cycle, any-sprite-animation | · single-run | ✅ yes | ✓ |
| Inbetweening & interpolation | 4 | [Thin-limb and contact-pose artifact cleanup (post-interpolation)](inbetween.md) | n/a | attack-swing, walk-cycle, any-thin-limb-sprite | · single-run | ✅ yes |  |
| Inbetweening & interpolation | 6 | [4-6 Keypose → Inbetween → Palette Cleanup workflow](inbetween.md) | comfyui | walk-cycle, attack-swing, any-sprite-animation | · community | ✅ yes |  |
| Cloud GPU workers | 2 | [ComfyUI-as-serverless pattern (platform-agnostic)](cloud-workers.md) | custom | cloud-compute/pipeline | ▸ reproduced | ✅ yes | ✓ |
| Cloud GPU workers | 2 | [Modal custom Python pipeline on H100/H200/B200](cloud-workers.md) | modal | cloud-compute/pipeline | ▸ reproduced | ✅ yes | ✓ |
| Cloud GPU workers | 2 | [RunPod serverless ComfyUI worker](cloud-workers.md) | runpod | cloud-compute/pipeline | ▸ reproduced | ✅ yes | ✓ |
| Cloud GPU workers | 2 | [fal.ai serverless media API and custom deployment](cloud-workers.md) | fal | cloud-compute/pipeline | ▸ reproduced | ✅ yes | ✓ |
| Cloud GPU workers | 4 | [Replicate Cog custom model deployment](cloud-workers.md) | replicate | cloud-compute/pipeline | ▸ reproduced | ✅ yes | ✓ |
| Cloud GPU workers | 6 | [Cloud worker pipeline architecture (input/output contract)](cloud-workers.md) | custom | cloud-compute/pipeline | · community | ✅ yes | ✓ |
| Combat animation craft | 2 | [Attack structure: anticipation → active/hit frame → follow-through → recovery](combat-craft.md) | n/a | attack | ▸ reproduced | ✅ yes | ✓ |
| Combat animation craft | 2 | [Author the 6 battle key-poses to biomechanical targets (hand-author, don't retarget, don't guess)](combat-craft.md) | blender | all-motion | ▸ reproduced | ✅ yes |  |
| Combat animation craft | 2 | [Exaggeration for small sprites: push poses 30–50% beyond naturalistic to survive the pixel grid](combat-craft.md) | n/a | attack | ▸ reproduced | ✅ yes | ✓ |
| Combat animation craft | 2 | [Follow-through and overlapping action: capes, hair, cloth settle after the primary motion ends](combat-craft.md) | n/a | all-motion | ▸ reproduced | ✅ yes | ✓ |
| Combat animation craft | 2 | [Hit-stop / freeze frame: the moment of impact is held to deliver game feel](combat-craft.md) | n/a | attack | ▸ reproduced | ✅ yes | ✓ |
| Combat animation craft | 2 | [Idle loop discipline: seamless loop, breathing breath, foot-contact discipline](combat-craft.md) | n/a | idle | ▸ reproduced | ✅ yes | ✓ |
| Combat animation craft | 2 | [Key-pose-first authoring: extremes before breakdowns before inbetweens](combat-craft.md) | n/a | attack | ▸ reproduced | ✅ yes | ✓ |
| Combat animation craft | 2 | [Readable silhouette: every key pose reads at thumbnail size in all 8 directions](combat-craft.md) | n/a | attack | ▸ reproduced | ✅ yes | ✓ |
| Combat animation craft | 2 | [Slow-in / slow-out (ease in/out): spacing that makes attacks feel weighted, not mechanical](combat-craft.md) | n/a | attack | ▸ reproduced | ✅ yes | ✓ |
| Combat animation craft | 2 | [Smear / multi-position blur frame: one frame captures the full arc of a fast swing](combat-craft.md) | n/a | attack | ▸ reproduced | ✅ yes | ✓ |
| Motion verification & QA | 1 | [Anchor the cross-family vision jury with a bug-free reference image (kill false positives on dark/ornate characters)](motion-verify.md) | n/a | all-motion | ▣ measured | ✅ yes |  |
| Motion verification & QA | 2 | [Frame-to-frame face identity / no-mutation detector](motion-verify.md) | python | verify | ▸ reproduced | ⚠ cond | ✓ |
| Motion verification & QA | 2 | [Frame-to-frame temporal LPIPS / SSIM consistency](motion-verify.md) | python | verify | ▸ reproduced | ✅ yes | ✓ |
| Motion verification & QA | 6 | [Foot-contact / no-slide detector](motion-verify.md) | python | verify | · community | ⚠ cond | ✓ |
| Motion verification & QA | 6 | [Root / foot-anchor canvas stability check](motion-verify.md) | python | verify | · community | ✅ yes | ✓ |
| Motion verification & QA | 6 | [SigLIP2 / CLIP identity-to-reference across animation frames](motion-verify.md) | python | verify | · community | ✅ yes | ✓ |
| Motion verification & QA | 6 | [Silhouette readability check (thumbnail-scale alpha legibility)](motion-verify.md) | python | verify | · community | ✅ yes | ✓ |
| Motion verification & QA | 6 | [Weapon length/tip continuity detector](motion-verify.md) | python | verify | · community | ✅ yes | ✓ |
| Commercial mocap & animation libraries | 2 | [Cascadeur (Nekki) — AI-assisted keyframe animation tool with commercial output](mocap-libraries.md) | custom | locomotion, combat, physics-driven action, creature (any skeleton the artist builds) | ▸ reproduced | ⚠ cond | ✓ |
| Commercial mocap & animation libraries | 2 | [Fab (Epic) marketplace — mocap animation packs (Standard License)](mocap-libraries.md) | unreal | locomotion, combat, idle, death (humanoid; creature packs available per-seller) | ▸ reproduced | ✅ yes | ✓ |
| Commercial mocap & animation libraries | 2 | [MoCap Online — Unity/Unreal game-ready mocap packs](mocap-libraries.md) | custom | locomotion, combat, shooter, athletic, death (humanoid) | ▸ reproduced | ⚠ cond | ✓ |
| Commercial mocap & animation libraries | 2 | [Reallusion ActorCore — per-clip commercial mocap library](mocap-libraries.md) | custom | locomotion, combat, social, death (humanoid; some creature packs available) | ▸ reproduced | ✅ yes | ✓ |
| Commercial mocap & animation libraries | 6 | [Move.ai — video-to-mocap cloud service (markerless, commercial output)](mocap-libraries.md) | custom | locomotion, combat, performance capture (humanoid performers only) | · single-run | ⚠ cond | ✓ |
| Open mocap datasets & license traps | 2 | [100STYLE — Edinburgh Locomotion Style Dataset](mocap-datasets.md) | n/a | locomotion/stylized-motion | ▸ reproduced | ✅ yes | ✓ |
| Open mocap datasets & license traps | 5 | [Truebones — Commercial Creature & Human Mocap Library](mocap-datasets.md) | n/a | creature/locomotion/combat | partial | ✅ yes | ✓ |
| Driving & reference video sources | 2 | [DWPose pose extraction from own footage (Apache-2.0, commercial-clean)](driving-video.md) | python | pose-extract | ▸ reproduced | ✅ yes | ✓ |
| Driving & reference video sources | 2 | [Rotoscoping from own reference footage (oldest clean technique — no derivative risk)](driving-video.md) | custom | driving-video | ▸ reproduced | ✅ yes | ✓ |
| Driving & reference video sources | 2 | [Shoot-your-own reference video (the always-clean driving source)](driving-video.md) | custom | driving-video | ▸ reproduced | ✅ yes | ✓ |
| Driving & reference video sources | 4 | [MediaPipe Pose extraction from own footage (Apache-2.0, commercial-clean)](driving-video.md) | python | pose-extract | ▸ reproduced | ✅ yes | ✓ |
| Driving & reference video sources | 4 | [Public-domain / CC0 video (Internet Archive, Prelinger) as driving reference](driving-video.md) | n/a | driving-video | ▸ reproduced | ⚠ cond | ✓ |
| Retargeting onto stylized rigs | 2 | [Auto-Rig Pro — Remap (retargeting) module](retarget.md) | blender | retarget | ▸ reproduced | ✅ yes | ✓ |
| Retargeting onto stylized rigs | 2 | [Bake to Action → 8-camera ortho render handoff](retarget.md) | blender | retarget | ▸ reproduced | ✅ yes | ✓ |
| Retargeting onto stylized rigs | 2 | [Rokoko Blender plugin — retargeting module](retarget.md) | blender | retarget | ▸ reproduced | ✅ yes | ✓ |
| Retargeting onto stylized rigs | 6 | [Foot IK lock + bake — eliminating foot-slide post-retarget](retarget.md) | blender | foot-ik | · community | ✅ yes | ✓ |
| Retargeting onto stylized rigs | 6 | [Non-humanoid retarget strategy — additive layers + hand-authoring](retarget.md) | blender | non-humanoid | · community | ✅ yes | ✓ |
| Motion data licensing doctrine | 2 | ["Royalty-free" ≠ "do anything" — the Mixamo case](motion-licensing.md) | n/a | licensing | ▸ reproduced | ⚠ cond | ✓ |
| Motion data licensing doctrine | 2 | [Academic mocap datasets are non-commercial — AMASS, Human3.6M, HumanAct12](motion-licensing.md) | n/a | licensing | ▸ reproduced | ⛔ no | ✓ |
| Motion data licensing doctrine | 2 | [Creative Commons license variants — which are shippable in a commercial game](motion-licensing.md) | n/a | licensing | ▸ reproduced | ⚠ cond | ✓ |
| Motion data licensing doctrine | 2 | [Engine marketplace motion grants — incorporated-use only, no raw redistribution](motion-licensing.md) | n/a | licensing | ▸ reproduced | ⚠ cond | ✓ |
| Motion data licensing doctrine | 2 | [The SMPL / SMPL-X body-model poison — research-only even with clean motion data](motion-licensing.md) | n/a | licensing | ▸ reproduced | ⛔ no | ✓ |
| Motion data licensing doctrine | 2 | [The non-commercial training-data poison rule (AMASS / HumanML3D)](motion-licensing.md) | n/a | licensing | ▸ reproduced | ⛔ no | ✓ |
| Motion data licensing doctrine | 2 | [The safe-harbor recipe for shippable motion](motion-licensing.md) | n/a | all-motion | ▸ reproduced | ✅ yes | ✓ |
| Motion data licensing doctrine | 6 | [Data license governs — not the code license](motion-licensing.md) | n/a | licensing | · community | ⚠ cond | ✓ |
| Structure-preserving repaint (ControlNet) | 4 | [Depth-from-mesh + Qwen-Image-Edit-2511 + InstantX ControlNet-Union repaint](repaint-controlnet.md) | comfyui | repaint | · single-run | ✅ yes |  |
| Structure-preserving repaint (ControlNet) | 6 | [Depth + Lineart/AnyLine ControlNet stack for 3D-render-to-painterly repaint](repaint-controlnet.md) | comfyui | repaint | · community | ⚠ cond | ✓ |
| Structure-preserving repaint (ControlNet) | 6 | [Render depth + normal passes directly from the TRELLIS.2 mesh (Blender Cycles) for ControlNet input](repaint-controlnet.md) | custom | repaint | · community | ✅ yes | ✓ |
| Structure-preserving repaint (ControlNet) | 6 | [Structure-from-ControlNet, style-from-LoRA decomposition principle](repaint-controlnet.md) | n/a | repaint | · community | ✅ yes | ✓ |
| Structure-preserving repaint (ControlNet) | 6 | [Tile ControlNet + Ultimate SD Upscale for painterly detail recovery after repaint](repaint-controlnet.md) | comfyui | repaint | · community | ⚠ cond | ✓ |
| Structure-preserving repaint (ControlNet) | 6 | [xinsir controlnet-union-sdxl-1.0 ProMax multi-condition repaint (SDXL base)](repaint-controlnet.md) | comfyui | repaint | · single-run | ✅ yes | ✓ |
| House-style injection | 2 | [B-LoRA: content/style-separated LoRA training (SDXL blocks 4 + 5)](style-injection.md) | comfyui | LoRA training and inference — separate style injection from content fidelity on SDXL | ▸ reproduced | ⚠ cond | ✓ |
| House-style injection | 2 | [House-palette color-grade transfer — post-repaint color lock](style-injection.md) | comfyui | post-repaint pass — runs after the LoRA/IP-Adapter repaint to lock output to the approved house palette | ▸ reproduced | ✅ yes | ✓ |
| House-style injection | 2 | [IP-Adapter Plus — style-transfer mode from a reference sprite](style-injection.md) | comfyui | repaint — inject painterly style from an approved reference sprite; complements ControlNet structure | ▸ reproduced | ⚠ cond | ✓ |
| House-style injection | 2 | [Studio house-style LoRA injected during the repaint pass](style-injection.md) | comfyui | repaint — any frame: idle, walk, attack, death; works alongside ControlNet-depth | ▸ reproduced | ✅ yes | ✓ |
| House-style injection | 2 | [img2img denoise strength — style/fidelity tradeoff window](style-injection.md) | comfyui | any img2img repaint pass; tuning the balance between injected style and preserved mesh layout | ▸ reproduced | ✅ yes | ✓ |
| House-style injection | 6 | [Avoiding style-bleed and over-stylization — selective block targeting for LoRAs](style-injection.md) | comfyui | LoRA inference — prevent house LoRA from over-stylizing face or weapon regions | · community | ✅ yes | ✓ |
| Identity & face preservation | 2 | [IP-Adapter (base, ViT-bigG) reference-image identity conditioning](identity-preserve.md) | comfyui | identity | ▸ reproduced | ✅ yes | ✓ |
| Identity & face preservation | 2 | [Masked-face differential-denoise repaint (preserve the approved face)](identity-preserve.md) | comfyui | identity | ▸ reproduced | ✅ yes | ✓ |
| Identity & face preservation | 5 | [Cross-frame face region anchor — locking identity across animation frames](identity-preserve.md) | comfyui | identity | community-confirmed-primary-source | ✅ yes |  |
| Rigid-weapon compositing | 2 | [Alpha-composite the aligned weapon crop onto the painterly view (rigid, no diffusion)](weapon-composite.md) | python | weapon-composite | ▸ reproduced | ✅ yes | ✓ |
| Rigid-weapon compositing | 2 | [Depth-aware occlusion: weapon in front of / behind body and limbs per view angle](weapon-composite.md) | blender | weapon-composite | ▸ reproduced | ✅ yes | ✓ |
| Rigid-weapon compositing | 2 | [Extract weapon mask from Blender mesh via Cryptomatte / Object-Index pass](weapon-composite.md) | blender | weapon-composite | ▸ reproduced | ✅ yes | ✓ |
| Rigid-weapon compositing | 2 | [Grip-point alignment: anchor weapon to painterly hand via MediaPipe/OpenPose wrist landmark](weapon-composite.md) | python | weapon-composite | ▸ reproduced | ✅ yes | ✓ |
| Rigid-weapon compositing | 2 | [SAM2 prompt-based weapon segmentation (fallback for baked PNG renders)](weapon-composite.md) | python | weapon-composite | ▸ reproduced | ✅ yes | ✓ |
| Rigid-weapon compositing | 4 | [ControlNet-tile + low-denoise inpaint over weapon region only to adopt house brushwork](weapon-composite.md) | comfyui | weapon-composite | · single-run | ✅ yes | ✓ |
| Rigid-weapon compositing | 4 | [Poisson-seamless-clone + diffusion seam inpaint at hand–weapon contact zone](weapon-composite.md) | comfyui | weapon-composite | · single-run | ✅ yes | ✓ |
| Rigid-weapon compositing | 4 | [Weapon-subsystem routing gate: body-attached vs. externally-projected weapons](weapon-composite.md) | n/a | weapon-composite | · single-run | ✅ yes | ✓ |
| Cross-frame & cross-direction coherence | 2 | [AnimateDiff temporal module for vid2vid repaint (not generation)](temporal-coherence.md) | comfyui | temporal-coherence | ▸ reproduced | ⚠ cond | ✓ |
| Cross-frame & cross-direction coherence | 2 | [Reference-frame style propagation via IP-Adapter](temporal-coherence.md) | comfyui | temporal-coherence | ▸ reproduced | ✅ yes | ✓ |
| Cross-frame & cross-direction coherence | 5 | [Batch-consistent conditioning across frames + directions](temporal-coherence.md) | comfyui | temporal-coherence | community-reproduced | ✅ yes | ✓ |
| Cross-frame & cross-direction coherence | 5 | [Cross-direction identity coherence — honest limits](temporal-coherence.md) | comfyui | temporal-coherence | field-consensus | ✅ yes | ✓ |
| Cross-frame & cross-direction coherence | 5 | [Wan2.1 VACE video-to-video repaint for temporally coherent animation restyling](temporal-coherence.md) | comfyui | temporal-coherence | vendor-documented | ✅ yes | ✓ |
| Repaint QA gate | 2 | [Identity-preserved check (CLIP/DINOv2 face-crop distance, repaint-vs-approved)](repaint-eval.md) | python | verify | ▸ reproduced | ⚠ cond | ✓ |
| Repaint QA gate | 2 | [Over-smoothing / detail-loss detection (Laplacian-variance + GLCM energy before-vs-after)](repaint-eval.md) | python | verify | ▸ reproduced | ✅ yes | ✓ |
| Repaint QA gate | 2 | [Palette adherence (Earth Mover's Distance on color histograms vs. approved palette)](repaint-eval.md) | python | verify | ▸ reproduced | ✅ yes | ✓ |
| Repaint QA gate | 2 | [Style-match score (SigLIP2/CLIP cosine) to the approved house baseline](repaint-eval.md) | python | verify | ▸ reproduced | ✅ yes | ✓ |
| Repaint QA gate | 2 | [Temporal-flicker metric for repainted cycle (LPIPS frame-delta + optical-flow warping error)](repaint-eval.md) | python | verify | ▸ reproduced | ⚠ cond | ✓ |
| Repaint QA gate | 6 | [Cross-family vision-LLM jury for repaint style + painterly + not-anime verdict](repaint-eval.md) | custom | verify | · community | ✅ yes |  |
| Repaint QA gate | 6 | [Repaint accept/reject gate: assembling all sub-metrics into a single admission decision](repaint-eval.md) | python | verify | · community | ✅ yes |  |
| Repaint QA gate | 6 | [Weapon-continuity check post-repaint (length + tip position, reuse wave-1 detector)](repaint-eval.md) | python | verify | · community | ✅ yes |  |

## Lanes

- [Motion architecture & contracts](motion-arch.md) — The rig-truth-first doctrine: motion truth -> AI polish -> sprite-sheet export; per-character animation contracts/manifests (views, frame counts, loop flags, anchors, layers); the 3-lane production model; one shared motion cage rendered per-direction, NOT 80 independent images. (9 recipes)
- [Rigging & skeletons](rigging.md) — Blender armatures + 2.5D proxy/mesh rigs as the deterministic motion source: bone hierarchies, hand->weapon_grip->weapon_tip rigid-attach chains (the fix for per-view weapon drift), auto-riggers (UniRig/Rigify/AccuRIG/Auto-Rig Pro/Mixamo). (43 recipes)
- [AI motion models](ai-motion.md) — Character-animation models that propose or drive motion: video-diffusion + pose-conditioned generation, AnimateDiff, image-to-animation DiTs. LICENSE-DECISIVE (research/academic-only weights are the trap; base-model license is inherited). (20 recipes)
- [Inbetweening & interpolation](inbetween.md) — Keyframe -> tween frame generation: FILM, RIFE/Practical-RIFE, optical-flow interpolation; multiply sparse keyposes into a smooth cycle; large-displacement vs smooth-motion tradeoffs. (14 recipes)
- [Cloud GPU workers](cloud-workers.md) — Run bigger-than-VRAM animation/edit models as a pipeline worker, not a website: RunPod / Modal / fal.ai / Replicate / HF Inference Endpoints; ComfyUI-as-serverless, cold starts, model caching, cost. Source-of-truth stays in the repo. (7 recipes)
- [Combat animation craft](combat-craft.md) — The designed-not-generated principles: anticipation -> active/hit frame -> follow-through -> recovery; smears, hit-stop, readable silhouettes, attack timing -- the animation principles that make combat game-readable. (19 recipes)
- [Motion verification & QA](motion-verify.md) — The local verifier gate for motion: root/anchor stability, foot-contact (no slide), hand-to-weapon attachment + weapon length/tip continuity, no frame-to-frame face mutation, silhouette readability, canvas/size consistency; automatable temporal-consistency metrics. (23 recipes)
- [Commercial mocap & animation libraries](mocap-libraries.md) — Ready-made mocap/animation packs licensed for commercial games: Mixamo, Reallusion ActorCore, Rokoko, marketplace/asset-store packs — coverage, license terms for shipping, FBX/BVH formats, humanoid-skeleton fit. (9 recipes)
- [Open mocap datasets & license traps](mocap-datasets.md) — Open/research motion-capture datasets and their licenses: CMU, AMASS, LAFAN1, Motion-X, 100STYLE, HumanML3D — which are commercial-safe vs RESEARCH-ONLY (the NC trap that poisons every downstream model trained on them). (9 recipes)
- [Text-to-motion & motion synthesis](motion-gen.md) — Generative motion models (text->motion / motion synthesis): MDM, MoMask, MotionGPT, T2M-GPT, OmniControl — existence + license-decisive (many TRAIN on AMASS and inherit its non-commercial terms in the output). (10 recipes)
- [Driving & reference video sources](driving-video.md) — Sourcing commercial-safe driving/reference video for pose-transfer animation, the license implications, and the shoot-your-own-reference recipe (always license-clean). (8 recipes)
- [Retargeting onto stylized rigs](retarget.md) — Getting external mocap onto the studio stylized / non-humanoid 2.5D rigs: Blender Rokoko / Auto-Rig-Pro remap, UE5 IK Retargeter, proportion mismatch (the JRPG / exotic-species silhouette problem), foot-IK cleanup. (8 recipes)
- [Motion data licensing doctrine](motion-licensing.md) — How motion-capture DATA licensing actually works for shipping a commercial game: royalty-free vs no-raw-redistribution vs research-only; whether you may train a model on it; Mixamo must-incorporate; the AMASS-NC downstream-poison trap. (8 recipes)
- [Structure-preserving repaint (ControlNet)](repaint-controlnet.md) — Repaint a 3D mesh/proxy render to the painterly house style while HOLDING structure: ControlNet depth/lineart/canny/tile/softedge stacks on Qwen-Image-Edit-2511; denoise + control-strength schedules. The mesh-render -> painterly-skin core that closes the §D style gap. (14 recipes)
- [House-style injection](style-injection.md) — Applying the painterly house style during repaint: the studio sfhd_style LoRA, IP-Adapter style-reference, img2img denoise ranges, content/style separation, palette/color-grade matching to the approved look. (8 recipes)
- [Identity & face preservation](identity-preserve.md) — Keeping the APPROVED face/character through repaint + across frames: face-preserve (de-lit), IP-Adapter-FaceID, inpaint-only / low-denoise face regions, ArcFace-guided locks. License-aware (InsightFace weights are NC). (13 recipes)
- [Rigid-weapon compositing](weapon-composite.md) — The §D Lane B: segment the mesh rigid weapon per view, align it to the painterly view, composite + harmonize (ControlNet-depth / inpaint / tile) — keep the weapon RIGID through the repaint. (8 recipes)
- [Cross-frame & cross-direction coherence](temporal-coherence.md) — The motion-specific hard part: style + identity stable across 8 directions AND animation frames — batch-consistent seeds, reference-frame propagation, AnimateDiff / video temporal modules for repaint, flicker/shimmer reduction, optical-flow-guided consistency. (8 recipes)
- [Repaint QA gate](repaint-eval.md) — QA specific to repaint: identity preserved (face-distance), weapon continuity, style-match to the house reference (SigLIP/CLIP), no over-smoothing / detail-loss, palette adherence. Extends motion-verify to the repaint stage. (8 recipes)

## Legend

- **↓** try-first order (lower = try first; derived from status + evidence strength).
- **Evidence** ▣ measured-on-rig > ▸ reproduced-from-source > · single-run / community / untested. The ordinal disciplines a single-reported claim from wearing the authority of an on-rig measurement. Proven (▣ measured-on-rig) vs research (everything else) is the spine of this KB.
- **Comm** commercial use of the OUTPUT: ✅ yes / ⚠ conditional / ⛔ no / ? unknown. A sprite inherits its base model's + recon model's license — the decisive axis (Zero123-lineage NVS is non-commercial).
- **Rig** fit 0–5 for this exact rig (RTX 5090 · 32 GB · Win 11 / WSL2). **Studio** fit 0–5 for commercial 2.5D JRPG sprite production.
- **✓** retrieval-verified this wave (existence + attribution + currency). Blank/· = unverified lead.
- **Boundary:** rig-measured it/s & VRAM peaks live in tensor-engine-knowledge (linked via `engine_recipe_ref`); base weights live in model-knowledge (linked via `base_model_slug`); never restated here.
