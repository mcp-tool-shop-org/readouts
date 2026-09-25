# Rigid-weapon compositing
_The §D Lane B: segment the mesh rigid weapon per view, align it to the painterly view, composite + harmonize (ControlNet-depth / inpaint / tile) — keep the weapon RIGID through the repaint._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

8 recipes · 8 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | Alpha-composite the aligned weapon crop onto the painterly view (rigid, no diffusion) | python | weapon-composite | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Depth-aware occlusion: weapon in front of / behind body and limbs per view angle | blender | weapon-composite | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Extract weapon mask from Blender mesh via Cryptomatte / Object-Index pass | blender | weapon-composite | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Grip-point alignment: anchor weapon to painterly hand via MediaPipe/OpenPose wrist landmark | python | weapon-composite | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | SAM2 prompt-based weapon segmentation (fallback for baked PNG renders) | python | weapon-composite | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 4 | ControlNet-tile + low-denoise inpaint over weapon region only to adopt house brushwork | comfyui | weapon-composite | · single-run | ✅ yes | 5 | 5 | ✓ |
| 4 | Poisson-seamless-clone + diffusion seam inpaint at hand–weapon contact zone | comfyui | weapon-composite | · single-run | ✅ yes | 5 | 4 | ✓ |
| 4 | Weapon-subsystem routing gate: body-attached vs. externally-projected weapons | n/a | weapon-composite | · single-run | ✅ yes | 5 | 5 | ✓ |

## Detail

### Alpha-composite the aligned weapon crop onto the painterly view (rigid, no diffusion) · `recommended` · ▸ reproduced
**After grip alignment, a straight alpha-over composite of the weapon crop (from the mesh render, feathered mask) onto the painterly NVS view places the rigid weapon without any diffusion — preserving exact blade length and angle — before the harmonization pass adjusts color and brushwork.**
Use OpenCV (Apache-2.0 since v4.5.0) or Pillow to alpha-composite the weapon PNG crop onto the matched painterly view at the corrected position. The weapon layer sits above the body layer; the feathered mask (1-2 px) at the blade edge softens the composite boundary. This step is deterministic and reversible — it is the anchor from which the harmonization pass is measured. No model runs here; no geometry is changed. Save both the pre-harmonize and post-harmonize composites as checkpoints so a failed harmonize can be rolled back to the clean composite.
- **For the pipeline:** Separating the hard composite step from the harmonization step enforces the ANDON principle: if harmonization re-imagines the blade, the checkpoint lets you roll back and retry with tighter denoise settings without re-running segmentation or alignment.
- **Engine:** python · **Applies to:** weapon-composite · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: OpenCV Apache-2.0 (v4.5.0+); Pillow HPND (permissive)) — Both OpenCV 4.5+ and Pillow are commercially permissive. Outputs are the studio's.
- **Fit:** rig 5/5 · studio 5/5
- **Best for:** compositing (-, fit -) ; rigid-placement (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [OpenCV Seamless Cloning / Photo Clone API](https://docs.opencv.org/4.x/df/da0/group__photo__clone.html) (OpenCV Contributors, 2024) — OpenCV (Apache-2.0 since 4.5.0) provides seamlessClone() for gradient-domain compositing and standard alpha-blending primitives via cv2.copyTo with mask. ; [Poisson Image Editing](https://dl.acm.org/doi/10.1145/882262.882269) (P. Pérez, M. Gangnet, A. Blake, 2003) — The foundational SIGGRAPH 2003 paper underlying seamless cloning: solving Poisson equations in the gradient domain removes color-mismatch seams when pasting a source region into a destination image.

### Depth-aware occlusion: weapon in front of / behind body and limbs per view angle · `recommended` · ▸ reproduced
**The mesh render already encodes per-pixel depth in the EXR Z-pass; comparing weapon depth vs. body depth per pixel determines per-view occlusion (e.g. a held cutlass behind the near arm at 45° front view) without any ML inference.**
Export the Z-depth pass alongside the Cryptomatte EXR from the mesh render. For each of the 8 views, generate a per-pixel weapon-vs-body depth comparison mask: pixels where weapon_Z > body_Z are occluded by the body (weapon is behind); pixels where weapon_Z < body_Z are in front. Apply this occlusion mask as an additional alpha multiply on the weapon composite layer before the harmonization pass — the weapon is hidden behind the arm where the mesh says it should be, and shows in front elsewhere. For the NVS painterly view, use the matching mesh depth as a proxy since NVS does not produce a reliable depth map.
- **For the pipeline:** Skipping depth-aware occlusion produces a weapon that floats in front of the arm at every angle, breaking 2.5D believability. The mesh Z-pass is zero cost to export and makes this deterministic — no per-frame manual masking.
- **Engine:** blender · **Applies to:** weapon-composite · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: Blender GPL (output renders unrestricted for commercial use)) — Blender is GPL; depth pass EXR outputs are the studio's property with no restriction.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Occlusion mask has aliased stairstepping at arm silhouette edge | Z-pass is integer-quantized at 8-bit; edge pixels have ambiguous depth | Export Z-pass as 32-bit float EXR; feather the occlusion boundary 1-2 px before applying | summary |

- **Best for:** depth-occlusion (-, fit -) ; z-ordering (-, fit -) ; per-view-compositing (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Cryptomatte Node + Render Passes (Z-depth) — Blender Manual](https://docs.blender.org/manual/en/latest/compositing/types/mask/cryptomatte.html) (Blender Foundation, 2024) — Blender Cryptomatte and Z-depth render passes together provide per-object matte and per-pixel depth at render time; together they fully encode occlusion relationships for 2.5D compositing without post-hoc inference.

### Extract weapon mask from Blender mesh via Cryptomatte / Object-Index pass · `recommended` · ▸ reproduced
**Because the studio controls the captain mesh, the weapon is its own named object with a dedicated Pass Index; Cryptomatte (Blender 2.8+) emits a per-object alpha matte that is pixel-exact, anti-aliased, and available for all 8 render angles with zero segmentation inference cost.**
Enable Cryptomatte (Object mode) in the Render Layers panel; the weapon object gets a unique Pass Index. Each rendered frame carries an EXR with the weapon's clean matte at full resolution, anti-aliased, with motion-blur and transparency support. This is the cleanest weapon-isolation path because you own the mesh geometry — no ML segmentation needed, no edge leakage, deterministic across all 8 views. Export each angle's matte alongside its RGB render for use in the compositing steps downstream.
- **For the pipeline:** Always prefer the mesh-owned matte over SAM2 for the weapon: it is zero-cost at render time, perfectly consistent across frames, and requires no prompt engineering. SAM2 is the fallback when the source render is a baked PNG without passes.
- **Engine:** blender · **Applies to:** weapon-composite · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: Blender Apache-2.0 (GPL for the Blender binary, but the render output and compositor are unrestricted for commercial use)) — Blender is GPL; rendered output and compositing pipelines built with it are unrestricted. No output license restriction on commercial assets.
- **License correction (verifier):** Blender is GPL-2.0/3.0, not Apache-2.0. The output/render exemption (Blender's longstanding policy that rendered output is not bound by the GPL) does make commercial use of the renders legal, so the commercial_use='yes' conclusion is correct, but the license label 'Apache-2.0' is wrong and should read 'GPL (output exempt)'.; Blender is licensed under GPL, not Apache-2.0; the render output and compositor are not restricted by Blender's license, so commercial use is allowed.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Matte has aliased or missing pixels at blade edge | Cryptomatte node not connected, or render samples too low for transparent edges | Use Cryptomatte node (not ID Mask) and increase sample count; export as 16-bit EXR to preserve sub-pixel alpha | summary |

- **Best for:** weapon-segmentation (-, fit -) ; mask-extraction (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [license -> commercial_use=yes] [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Cryptomatte Node — Blender Manual](https://docs.blender.org/manual/en/latest/compositing/types/mask/cryptomatte.html) (Blender Foundation, 2024) — Cryptomatte (Blender 2.8+) generates per-object/material mattes that are anti-aliased and support depth-of-field and motion blur, superseding the older ID Mask node.

### Grip-point alignment: anchor weapon to painterly hand via MediaPipe/OpenPose wrist landmark · `recommended` · ▸ reproduced
**The mesh render and the NVS painterly view share the same 8-angle framing with a common foot anchor, so wrist/grip keypoints from either image are a stable alignment target; translating the segmented weapon mask to match the painterly hand's keypoint 0 (wrist) or keypoint 9 (index MCP) places the weapon grip within 2-4 px for all views before any fine correction.**
Run MediaPipe Hand Landmarker on both the mesh render and the painterly NVS view for the matching angle to extract the wrist keypoint (landmark 0) or index-finger MCP (landmark 5). Compute the translation delta between the two grip points and apply it to the weapon mask and its RGB crop before compositing. Because foot-anchor framing keeps scale and rotation consistent across views, a pure translation is usually sufficient; rotation correction is only needed if the painterly view has body lean divergence from the mesh. This step runs in CPU-only mode on the studio's Python pipeline — no GPU needed.
- **For the pipeline:** Do not rely solely on pixel-position alignment from the shared framing; even with identical camera angles, the NVS pass may have minor body-lean variation. A 2-keypoint alignment step costs <50 ms and removes the main source of grip-seam misregistration.
- **Engine:** python · **Applies to:** weapon-composite · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: Apache-2.0) — MediaPipe is Apache-2.0; output alignment data is the studio's. No restriction.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| landmark_target | 0 (wrist) or 5 (index MCP) | ○ | use whichever is visible and unoccluded for the view angle |
| alignment_mode | translation-only | ○ | add rotation only if body-lean divergence > 3 degrees |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| MediaPipe fails to detect hand in the mesh render (clean background confuses detector) | Hand landmarker trained on photographic data; mesh renders may lack skin texture | Fall back to manually placing grip-point anchor per view in a one-time calibration pass; or use the mesh's known grip bone world-space coordinate directly | summary |

- **Best for:** alignment (-, fit -) ; keypoint-registration (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Hand landmarks detection guide — MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) (Google AI Edge, 2024) — MediaPipe Hand Landmarker (Apache-2.0) detects 21 3D hand-knuckle coordinates from a single image frame; code samples licensed Apache-2.0.

### SAM2 prompt-based weapon segmentation (fallback for baked PNG renders) · `recommended` · ▸ reproduced
**SAM2 (Apache-2.0) can isolate a weapon from a baked PNG mesh render with a single bounding-box or point prompt per view; because the mesh render is clean and uncluttered, SAM2 achieves near-matte quality without needing the Cryptomatte pass.**
When only a flat RGB render is available (no EXR passes), run SAM2 with a bounding-box prompt around the weapon region for each of the 8 angles. The mesh render is low-noise and high-contrast, making SAM2's segmentation highly reliable here compared to a cluttered photo. Output masks as 8-bit PNGs per angle for downstream compositing. Use SAM2's image mode (not video mode) since the 8 views are discrete frames, not a continuous sequence. Feather mask edges 1-2 px before compositing.
- **For the pipeline:** SAM2 is the correct fallback when the mesh EXR passes are lost or unavailable. For initial pipeline bring-up, both paths should be exercised and the Cryptomatte path locked in as canonical once proven.
- **Engine:** python · **Applies to:** weapon-composite · **Base:** SAM2 · **Kind:** technique
- **VRAM:** 4-8
- **Builds on (stage 2):** Extract weapon mask from Blender mesh via Cryptomatte / Object-Index pass
- **Output license:** commercial **yes** (license: Apache-2.0) — SAM2 is Apache-2.0; all outputs are the studio's. No restriction on commercial sprite production.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| prompt_type | bounding_box | ○ | box prompt is more stable than single point for elongated weapons |
| mask_feather_px | 1-2 | ○ | feather before compositing to avoid hard-edge artifacts |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Mask leaks into body at grip area | Weapon and hand overlap region confuses the segmentation boundary | Use a tighter bounding box that excludes the grip overlap; the seam-inpaint step (later recipe) handles the contact zone anyway | summary |

- **Best for:** weapon-segmentation (-, fit -) ; mask-extraction (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [facebookresearch/segment-anything-2](https://github.com/facebookresearch/sam2) (Meta AI, 2024) — SAM2 (Apache-2.0) is a promptable segmentation foundation model for images and video; SAM2.1 (Sep 2024) improves tracking and mask quality over the original July 2024 release.

### ControlNet-tile + low-denoise inpaint over weapon region only to adopt house brushwork · `recommended` · · single-run
**Running ControlNet-tile (or depth-ControlNet) with denoise ≤ 0.3 on the weapon-only mask causes the diffusion pass to re-texture the blade surface with the painterly house style without changing blade length, angle, or width — the low denoise and tile constraint prevent geometry re-imagination.**
In ComfyUI: load the SDXL ControlNet-Union (xinsir, Apache-2.0) with tile+depth modes active; input the composite image as both the latent source and the ControlNet condition image; apply the weapon mask via SetNoiseMask so only the weapon region is noised; set denoise=0.20-0.28 and CFG=5-6. The tile conditioning locks high-frequency structure (blade geometry) while the low denoise pass adds painterly brushwork texture matching the body. Do NOT apply to the full image — mask strictly to the weapon crop plus a 4-8 px feather into the seam zone. Qwen-Image-Edit-2511 (Apache-2.0) can be substituted for instruction-guided harmonization ('make the blade look painted in oil, same shape').
- **For the pipeline:** Denoise ceiling of 0.30 is the hard blocker threshold: above it the model begins re-imagining blade geometry. If the brushwork match is insufficient at ≤0.30, increase CFG (up to 7) or use IP-Adapter style injection at low weight rather than raising denoise.
- **Engine:** comfyui · **Applies to:** weapon-composite · **Base:** SDXL · **Kind:** workflow
- **VRAM:** 12-24
- **Output license:** commercial **yes** (license: ControlNet-Union SDXL Apache-2.0; Qwen-Image-Edit-2511 Apache-2.0) — Both base models are Apache-2.0. ComfyUI itself is GPL-3 (runtime), but generated outputs are the studio's.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| denoise | 0.20-0.28 | ○ | hard ceiling 0.30 to prevent geometry re-imagination |
| cfg | 5-6 | ○ | raise to 7 before raising denoise if brushwork match is weak |
| controlnet_mode | tile+depth | ○ | tile locks structure; depth provides z-ordering reference |
| controlnet_strength | 0.8-1.0 | ○ | per xinsir recommendation for tile/depth modes |
| mask_feather_px | 4-8 | ○ | feather into seam zone but not onto body |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Harmonize pass re-imagines the blade (wrong length, curved, redesigned) | Denoise too high (>0.35) or mask too large, including body region | Reduce denoise to ≤0.25; tighten mask to weapon only; increase ControlNet strength to 1.0 | hparams |
| Blade looks plasticky / unmatched to painterly body | Denoise too low (< 0.15) — not enough noise to generate brushwork | Raise denoise to 0.22-0.28 band; add IP-Adapter at 0.3 weight with style reference crop from body | hparams |

- **Best for:** harmonization (-, fit -) ; style-injection (-, fit -) ; weapon-texturing (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [xinsir/controlnet-union-sdxl-1.0](https://huggingface.co/xinsir/controlnet-union-sdxl-1.0) (xinsir, 2024) — ControlNet-Union SDXL (Apache-2.0) supports 10+ control types including tile and depth in a single model; multi-condition fusion is learned during training with no single-condition performance drop. ; [Qwen-Image-Edit (Qwen-Image-Edit-2511)](https://github.com/QwenLM/Qwen-Image) (Alibaba Qwen Team, 2025) — Qwen-Image-Edit (Apache-2.0, released August 2025) enables instruction-guided region editing with identity and semantic preservation; supports material-replacement and viewpoint-consistent edits.

### Poisson-seamless-clone + diffusion seam inpaint at hand–weapon contact zone · `recommended` · · single-run
**The grip contact zone (3-6 px where hand and weapon meet) is the hardest compositing seam; Poisson seamless cloning (OpenCV, Apache-2.0) removes color-gradient discontinuity at the boundary, then a 12-16 px inpaint with denoise=0.35-0.45 regenerates the grip wrap and finger details to match the painterly body style.**
Step 1: apply OpenCV seamlessClone (NORMAL_CLONE) with a tight mask around the weapon grip edge to blend color gradients across the seam — this is a pure mathematical operation with no model inference. Step 2: dilate the contact mask 12-16 px to cover the grip overlap zone and run a ComfyUI inpaint pass (denoise 0.35-0.45) with a prompt targeting the grip material ('leather-wrapped hilt, painterly strokes'). This two-pass approach keeps the weapon geometry locked from Step 1 while regenerating only the organic hand-wrap contact that bridges the two assets. The Pixel-Equivalent Latent Compositing (PELC / DecFormer, arXiv:2512.05198) technique can replace the standard latent interpolation if seam artifacts persist at the mask boundary.
- **For the pipeline:** The contact zone is the only place in the weapon-composite pipeline where denoise should exceed 0.30 — because hand-wrap geometry is not rigid and must conform to both assets. Keep the mask tight (12-16 px from the actual contact line) to prevent drift into the validated weapon blade or painterly arm.
- **Engine:** comfyui · **Applies to:** weapon-composite · **Kind:** workflow
- **VRAM:** 8-16
- **Output license:** commercial **yes** (license: OpenCV Apache-2.0; ComfyUI GPL-3 (outputs unrestricted)) — OpenCV 4.5+ is Apache-2.0. ComfyUI runtime is GPL-3 but generated images are not GPL-encumbered.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| clone_mode | NORMAL_CLONE | ○ | use MIXED_CLONE if preserving weapon texture gradient is less important than matching body color |
| contact_mask_dilation_px | 12-16 | ○ | covers grip overlap without bleeding into blade or arm |
| denoise_contact | 0.35-0.45 | ○ | higher than blade harmonize — hand wrap is organic, not rigid |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Poisson clone introduces color bleed from weapon metal onto the hand skin | Mask too loose; NORMAL_CLONE mixes gradient from both sides equally | Tighten mask to only the weapon-side seam edge; or switch to MIXED_CLONE to weight destination gradient | hparams |

- **Best for:** seam-inpaint (-, fit -) ; hand-weapon-contact (-, fit -) ; blending (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=unverified] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, confirmed-with-fixes, unverified]]
- **Sources:** [Poisson Image Editing](https://dl.acm.org/doi/10.1145/882262.882269) (P. Pérez, M. Gangnet, A. Blake, 2003) — Gradient-domain compositing solves the Poisson equation to eliminate color-mismatch seams; implemented in OpenCV as cv2.seamlessClone. ; [Your Latent Mask is Wrong: Pixel-Equivalent Latent Compositing for Diffusion Models](https://arxiv.org/abs/2512.05198) (Rowan Bradbury, Dazhi Zhong, 2025) — Standard linear latent blending under a downsampled mask produces boundary seams and global color shifts; DecFormer (7.7M params) predicts pixel-equivalent blend weights and residual corrections, reducing edge error up to 53% over standard mask interpolation on FLUX.1.

### Weapon-subsystem routing gate: body-attached vs. externally-projected weapons · `recommended` · · single-run
**Not all weapons need the composite lane: weapons that are body-attached (sheathed sword, holstered pistol, back-mounted shield) or share deformation with the body (cloak, tail, necklace) are already correctly painted by the NVS repaint and should stay in that lane; only externally-projected rigid props (held cutlass, extended harpoon, pole weapon) that diffusion re-imagines between views need to be routed through the weapon-composite lane.**
At pipeline intake, classify each character's weapons: (A) body-attached/sheathed — stays in NVS lane, no composite needed; (B) held-rigid/externally-projected — routed to this weapon-composite lane per §D. The classification gate prevents unnecessary composite passes on weapons that are already validated. For the pirate pack: the captain's cutlass (held, extended) is Class B; the belt dagger (sheathed) is Class A. For the goblin pack: thrown javelins are Class B at release frame; at-rest they are Class A. This routing decision should be recorded in the roster JSON per character so it is persistent and version-controlled.
- **For the pipeline:** Routing ALL weapons through composite adds 3-5 min per character-view with no quality gain for body-attached weapons. The gate is the first step in the per-character weapon pipeline — run it before any segmentation or alignment work.
- **Engine:** n/a · **Applies to:** weapon-composite · **Kind:** workflow
- **VRAM:** 0
- **Output license:** commercial **yes** (license: n/a) — Organizational routing logic; no model or tool license applies.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| class_A_criteria | body-attached, sheathed, or shares deformation with body | ○ | stays in NVS lane |
| class_B_criteria | held-rigid, externally-projected, or drifts across NVS views | ○ | routes to weapon-composite lane |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Composite applied to a sheathed weapon that was already clean in NVS | Missing routing gate; all weapons sent to composite | Add weapon_class field to roster JSON; gate composite step on class=B | summary |

- **Best for:** routing (-, fit -) ; pipeline-gate (-, fit -) ; classification (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, unverified]]
- **Sources:** [facebookresearch/segment-anything-2](https://github.com/facebookresearch/sam2) (Meta AI, 2024) — SAM2 can segment held props from video sequences, but the studio's §D finding establishes that no diffusion method rotates a held rigid prop consistently across views — making mesh-composite the correct fix rather than better segmentation of the NVS output.

