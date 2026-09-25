# Rigging & skeletons
_Blender armatures + 2.5D proxy/mesh rigs as the deterministic motion source: bone hierarchies, hand->weapon_grip->weapon_tip rigid-attach chains (the fix for per-view weapon drift), auto-riggers (UniRig/Rigify/AccuRIG/Auto-Rig Pro/Mixamo)._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

43 recipes · 25 recommended · 5 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 1 | High-fidelity TRELLIS decimate with sliver cleanup (the fix for ribbon/shard armor artifacts) | blender | rigging | ▣ measured | ✅ yes | 5 | 5 | · |
| 1 | Pose rigid plate armor on a learned auto-rig: ROM cap + DQS bake + skin rigidify | blender | rigging | ▣ measured | ✅ yes | 5 | 5 | · |
| 1 | Rigid weapon on a hand→weapon_grip→weapon_tip bone chain | blender | rigging | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | TRELLIS.2-4B mesh → Blender rig → 8-dir sprite render pipeline | blender | rigging | ▣ measured | ✅ yes | 5 | 5 | · |
| 1 | UniRig auto-rig (skeleton + learned skin) on RTX 5090 sm_120 via WSL2 — MEASURED | huggingface | rigging | ▣ measured | ✅ yes | 5 | 5 | · |
| 2 | Auto-rigger license landscape: UniRig MIT vs Rigify GPL vs AccuRIG EULA vs Auto-Rig Pro paid vs Mixamo NC-redistribute | n/a | rigging | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Rigify — Blender's bundled modular auto-rigger | blender | rigging | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 2 | UniRig Hugging Face checkpoints: what is actually downloadable vs. coming soon | huggingface | rigging | ▸ reproduced | ✅ yes | 4 | 4 | ✓ |
| 2 | UniRig SIGGRAPH 2025 / ACM TOG paper: arXiv:2504.12451, DOI 10.1145/3730930 | custom | rigging | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | UniRig commercial license: MIT on code AND released HuggingFace checkpoints | n/a | rigging | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | UniRig community adoption and real-pipeline usage evidence (2025-2026) | python | rigging | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | UniRig in the studio flow: TRELLIS.2 mesh → UniRig rig → weapon_grip chain → Blender 8-dir render | blender | rigging | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | UniRig input mesh requirements and output format spec | huggingface | rigging | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | UniRig redistribution, sublicensing, and commercial derivative works under MIT | n/a | rigging | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | UniRig skeleton tree tokenization: DFS ordering + 256-bin coordinate discretization | huggingface | rigging | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | UniRig stage 1: OPT-125M autoregressive skeleton GPT over 3DShape2Vecset geometry encoding | huggingface | rigging | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | UniRig stage 2: bone-point cross-attention skinning with geodesic distance refinement | huggingface | rigging | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 4 | UniRig inference speed: 1-5 second end-to-end rigging claim vs. commercial baselines | huggingface | rigging | · single-run | ✅ yes | 5 | 5 | ✓ |
| 4 | UniRig — VAST-AI/Tsinghua autoregressive skeleton predictor (SIGGRAPH 2025, MIT) | huggingface | rigging | · single-run | ⚠ cond | 4 | 4 | ✓ |
| 6 | Auto-Rig Pro — paid Blender add-on for rigging + mocap retargeting | blender | rigging | · community | ✅ yes | 5 | 5 | ✓ |
| 6 | Blender NLA strip + orthographic multi-camera sprite-sheet render | blender | rigging | · community | ✅ yes | 5 | 5 | ✓ |
| 6 | Blender humanoid armature bone hierarchy for 2.5D sprite motion | blender | rigging | · community | ✅ yes | 5 | 5 | ✓ |
| 6 | ComfyUI-UniRig — ComfyUI wrapper nodes for UniRig rigging inside ComfyUI | comfyui | rigging | ▸ reproduced | ✅ yes | 4 | 3 | ✓ |
| 6 | Godot 4 Skeleton2D / Bone2D runtime cutout puppet (Blender = authoring) | custom | rigging | ▸ reproduced | ✅ yes | 3 | 3 | ✓ |
| 6 | Mixamo auto-rigger + animation library (Adobe, royalty-free commercial) | custom | rigging | ▸ reproduced | ✅ yes | 3 | 3 | ✓ |
| 6 | UniRig Blender VRM addon — VRM import/export for rigged mesh handoff | blender | rigging | ▸ reproduced | ✅ yes | 2 | 1 | ✓ |
| 6 | UniRig on non-humanoid / exotic meshes — decisive advantage, honest quality ceiling | blender | rigging | · community | ✅ yes | 5 | 4 | ✓ |
| 6 | UniRig paper benchmarks — what the numbers mean and what they do not cover | blender | rigging | ▸ reproduced | ? unk | 4 | 4 | ✓ |
| 6 | UniRig skeleton cleanup workflow — the manual pass every non-humanoid needs | blender | rigging | · community | ✅ yes | 4 | 4 | ✓ |
| 6 | UniRig skeleton → mocap retarget: non-standard bone-name remap via ARP Remap or Blender Retarget addon | blender | rigging | · community | ✅ yes | 4 | 4 | ✓ |
| 6 | UniRig training data (Articulation-XL2.0 / Objaverse-XL): license propagation analysis | n/a | rigging | ▸ reproduced | ⚠ cond | 4 | 4 | ✓ |
| 8 | AccuRIG 2 — Reallusion free auto-rigger with ActorCore motion library | custom | rigging | · community | ✅ yes | 4 | 3 | ✓ |
| 9 | DQS/LBS + Unity Avatar auto-rig limits hold | docs | all-motion | docs | check | 4 | 4 | · |
| 9 | HumanRig learned automatic humanoid rigging (Chu et al. 2024) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | Neural Blend Shapes skeletal articulations (Li et al. 2021) | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | Spiritus — mesh-skeleton binding + MDM | comfy | all-motion | paper | check | 4 | 4 | · |
| 9 | UniRig + Blender cleanup/armature parent peers | blender | all-motion | docs | check | 4 | 4 | · |
| 10 | UniRig license watch: MIT is not guaranteed for future weight releases | n/a | rigging | · community | ✅ yes | 4 | 5 | ✓ |
| 10 | UniRig vs Rigify vs AccuRIG vs Auto-Rig Pro vs Mixamo vs Blender automatic weights — head-to-head | blender | rigging | · community | ⚠ cond | 5 | 5 | ✓ |
| 13 | SkinTokens — VAST-AI UniRig successor (arXiv Feb 2026, MIT) | python | rigging | · single-run | ⚠ cond | 5 | 4 | · |
| 13 | SkinTokens: unified autoregressive successor to UniRig (arXiv:2602.04805, 2026, MIT) | huggingface | rigging | · single-run | ⚠ cond | 4 | 3 | · |
| 15 | Mesh preparation for UniRig: decimating TRELLIS.2 dense meshes before auto-rigging | blender | rigging | · community | ✅ yes | 4 | 5 | · |
| 15 | UniRig successor landscape — Auto-Connect, SkinTokens, and when to upgrade | blender | rigging | · community | ⚠ cond | 5 | 3 | · |

## Detail

### High-fidelity TRELLIS decimate with sliver cleanup (the fix for ribbon/shard armor artifacts) · `recommended` · ▣ measured
**Collapse-decimating a dense TRELLIS mesh leaves THIN SLIVER triangles on thin plate armor (greaves, sabatons, pauldrons) that render as 'ribbon strips' and 'triangular shards' and fail the vision jury; a post-collapse cleanup pass (merge-by-distance + DISSOLVE DEGENERATE + delete-loose) removes them. The fix is the cleanup, not a higher triangle count.**
MEASURED ON RIG (2026-06-25, blackguard): the original collapse-decimate to ~224k tris still showed sliver artifacts on lower-leg/foot armor that the cross-family jury flagged. Re-decimating the 992k-tri TRELLIS mesh to 150k tris with a cleanup pass removed 97,341 sliver/loose elements (~40% of post-collapse verts), yielding a clean 149k-tri, 148k-vert game mesh with solid greaves and sabatons (verified full-res). The cleanup (bpy: remove_doubles 0.00015 -> dissolve_degenerate 0.0002 -> delete_loose -> normals_make_consistent) is the load-bearing step; it did NOT punch holes (full-res confirmed). A ~1:1 vert:tri ratio after cleanup is normal here because the tattered cape/cloth are open sheets, not damage. Decimate-then-rig so UniRig computes skin for the final game-weight geometry.
- **For the pipeline:** Add the sliver-cleanup pass to the decimate step for EVERY armored character in the 68-char roster (the artifact recurs on all plate armor). 150k tris is a fine high-fidelity target for a sprite source; tri count is not the lever, the degenerate-dissolve is. Render the decimated mesh full-res before spending UniRig time on it.
- **Engine:** blender · **Applies to:** rigging · **Kind:** technique
- **VRAM:** n/a
- **Validated under:** RTX 5090 / Blender 5.0.1; blackguard.glb 817k verts/992k tris -> 150k-tri collapse -> cleanup -> 148k verts/149k tris (97,341 removed); UniRig WSL2 re-rig (28-bone skeleton + learned skin).
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: GPL (Blender); MIT (UniRig)) — Blender GPL covers the tool; decimated mesh + rigged GLB are studio IP.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Lower-leg/foot/pauldron armor renders as flat ribbon strips or triangular shards | Collapse decimation produces near-zero-area sliver triangles on thin plate geometry | After modifier_apply: remove_doubles -> dissolve_degenerate (threshold ~0.0002) -> delete_loose -> recalc normals; re-rig the cleaned mesh | summary |

- **Best for:** mesh-prep (-, fit -) ; trellis-pipeline (-, fit -) ; game-asset (-, fit -) ; decimation (-, fit -)
- **Verify:** no external verdict — not checked
- **Sources:** [Blender Manual — Mesh Cleanup (Merge by Distance, Degenerate Dissolve)](https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html) (Blender Foundation, 2025) — Degenerate Dissolve removes edges/faces with zero area or length; Merge by Distance welds coincident verts — the standard cleanup for decimation slivers. ; [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig](https://arxiv.org/abs/2504.12451) (Zhang et al. (VAST AI Research), 2025) — UniRig samples a point cloud from the mesh surface; clean manifold geometry before auto-rig gives better skeleton + skin.

### Pose rigid plate armor on a learned auto-rig: ROM cap + DQS bake + skin rigidify · `recommended` · ▣ measured
**UniRig emits STANDARD linear-blend-skinning weights, so a posed character inherits LBS's candy-wrapper collapse at bent joints regardless of weight accuracy — worst on rigid plate armor. Three stacked fixes make it pose cleanly: (1) cap authored joint flexion <= ~85deg; (2) bake with dual-quaternion skinning (Armature use_deform_preserve_volume); (3) RIGIDIFY the limb-armor skin so plates crease instead of melt.**
MEASURED ON RIG (2026-06-25, blackguard guard pose): the auto-rig skin is cleanly smooth, not noisy (<=4 influences, no stray weights) but ~49-51% of elbow-band verts blend across the joint = the candy-wrapper zone. A 100deg elbow flex melted the armor (jury FAIL 0/3 front). The fix stack: (a) cap the elbow to ~70deg (inside the clean-LBS <=85deg zone); (b) DQS bake (preserve-volume) avoids the volume collapse; (c) RIGIDIFY (per limb-armor vert, push weight toward the dominant bone by ~0.75 and shrink the rest) so the plate rotates rigidly and creases at the joint instead of melting — this approximates the shipped-practice 'rigid-bind each plate to one bone, segment at the joint' rule on a single auto-mesh we cannot physically segment. RESULT: posed FRONT jury moved 0/3 -> 2/3 PASS (matching the clean-rest baseline). Cloth (cape/loincloth, dominated by torso bones) is EXCLUDED from rigidify so it stays soft. HONEST CEILING: a single continuous auto-rig armor shell cannot fold perfectly at a sharp joint (melt vs crack); the true fix is upstream segmented overlapping plates (hand-modeled), and since 2.5D bakes a posed render to a sprite, painterly repaint-in-post is a valid final option.
- **For the pipeline:** In the pose bridge: cap ROM, enable DQS on the Armature modifier before baking, and run a rigidify weight pass on limb-armor verts (exclude cloth). For the roster, rigidify is scriptable and reusable. When creasing is insufficient, add pose-space corrective shapes (the learned corrective branch UniRig lacks). Reserve repaint-in-post for the residual.
- **Engine:** blender · **Applies to:** rigging · **Kind:** technique
- **VRAM:** n/a
- **Validated under:** RTX 5090 / Blender 5.0.1; blackguard hifi rig (28 bones); elbow cap 70deg, DQS preserve_volume, rigidify 0.75 on limb-armor verts; cross-family jury front 0/3 -> 2/3.
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: GPL (Blender); MIT (UniRig)) — Tooling is Blender/UniRig; output is studio IP.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Melted / torn / stretched armor at the bent elbow or shoulder when posed | Linear blend skinning averages transforms not rotations -> volume collapse; UniRig outputs standard LBS weights; rigid plate cannot fold like skin | Cap flexion <=85deg + DQS bake + rigidify limb-armor verts toward the dominant bone; correctives or repaint for the residual | summary |

- **Best for:** skinning (-, fit -) ; posing (-, fit -) ; rigid-armor (-, fit -) ; deform-safe (-, fit -)
- **Verify:** no external verdict — not checked
- **Sources:** [Geometric Skinning with Approximate Dual Quaternion Blending](https://users.cs.utah.edu/~ladislav/kavan08geometric/kavan08geometric.html) (Ladislav Kavan, Steven Collins, Jiri Zara, Carol O'Sullivan, 2008) — LBS collapses volume at bent/twisted joints (candy-wrapper, severe near 180deg); DQS blends rigid transforms to remove the collapse, at the cost of mild joint bulging. ; [Pose Space Deformation: A Unified Approach to Shape Interpolation and Skeleton-Driven Deformation](https://scribblethink.org/Work/PSD/index.html) (J.P. Lewis, Matt Cordner, Nickson Fong, 2000) — Artist-sculpted corrective shapes interpolated over the skinning envelope repair collapsed elbows/shoulders (the basis of corrective shape keys / pose drivers). ; [Learning Skeletal Articulations with Neural Blend Shapes](https://arxiv.org/abs/2105.02451) (Peizhuo Li, Kfir Aberman et al., 2021) — Adds a learned corrective pose-dependent shape branch to fix the joint-region artifacts of standard rigging/skinning — the corrective branch UniRig does not implement. ; [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig](https://arxiv.org/abs/2504.12451) (Zhang et al. (VAST AI Research), 2025) — UniRig predicts a per-vertex skinning-weight matrix applied through standard LBS, so posed UniRig characters inherit LBS deformation artifacts.

### Rigid weapon on a hand→weapon_grip→weapon_tip bone chain · `recommended` · ▣ measured
**Parenting the weapon as a rigid object to a dedicated weapon_grip bone is the studio-proven fix for the per-view weapon drift that no diffusion method (image-NVS or video/orbit) can solve.**
In the Blender armature, add weapon_grip (child of hand.R) and weapon_tip bones. Make the sword/axe/polearm a separate rigid mesh parented or constrained (Child-Of constraint) to weapon_grip with Set Inverse applied. The body mesh deforms via skinning; the weapon stays rigid — constant length, constant angle — because it is not a deformable mesh at all. Animate the action, render N directions: grip position and tip position are stable every frame. Weapon-tip velocity can be sampled per frame in Python for hit-box data.
- **For the pipeline:** This is the deterministic spine for any externally-projected weapon (cutlass, harpoon, polearm, staff). It makes weapon length and tip continuity automatically verifiable in the motion-verify step, and rules out the weapon-drift failure mode that was measured on the RTX 5090 production rig with TRELLIS.2-4B mesh → 8-view Blender render.
- **Engine:** blender · **Applies to:** rigging · **Kind:** technique
- **VRAM:** 2-8
- **Output license:** commercial **yes** (license: GPL (Blender app); rendered output unrestricted) — Blender GPL covers the application only. Weapon mesh geometry you model is your IP; rendered frames are unrestricted.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| If weapon_grip is accidentally made a deform bone with skinning weights, the weapon will bend with the hand mesh — mark it non-deform. |  |  |  |
| Child-Of constraint requires Set Inverse to neutralize accumulated parent transforms; skipping it offsets the weapon in world space. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed (measured-on-rig — rig is authoritative) [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Armatures — Blender Manual](https://docs.blender.org/manual/en/latest/animation/armatures/index.html) (Blender Foundation, 2025) — An armature is a skeleton of bones; objects parented/constrained to bones move rigidly with them — enabling a weapon mesh to track a grip bone with no deformation. ; [Child Of Constraint — Blender Manual](https://docs.blender.org/manual/en/latest/animation/constraints/relationship/child_of.html) (Blender Foundation, 2025) — The Child Of constraint lets an object follow a bone's transform; Set Inverse removes the cumulative parent-space offset so the object sits at its authored position.

### TRELLIS.2-4B mesh → Blender rig → 8-dir sprite render pipeline · `recommended` · ▣ measured
**Generating a character mesh with TRELLIS.2-4B (MIT) then rigging it in Blender with weapon_grip chain is the studio-proven path that keeps the weapon rigid and the face intact across all N render angles.**
Generate character mesh + PBR textures using TRELLIS.2-4B (MIT license; 4B-parameter image-to-3D). Import the GLB into Blender. Retopologize if needed (or use UniRig for auto-skinning). Build or retarget the canonical humanoid armature, append the weapon_grip→weapon_tip chain off hand.R bone. Parent the weapon prop mesh (rigid, separate object) to weapon_grip via Child-Of constraint with Set Inverse. Author walk/attack/idle/hurt/death actions in NLA strips. Configure 8 orthographic cameras at the correct 2.5D angles. Render all directions × all actions to sprite sheets. The mesh path was directly measured on the studio RTX 5090 rig — weapon length and angle stay constant across all 8 views.
- **For the pipeline:** This is THE captain path — it is the proven end-to-end solution to the weapon-drift problem. The open gap is style: TRELLIS.2-4B output is photorealistic/3D, not painterly. The repaint step (Qwen-Image-Edit-2511 or InstantX Qwen-ControlNet-Union, both Apache) is the downstream lane that converts renders to painterly sprites. Verified VRAM: TRELLIS.2-4B inference peaks around 16-24 GB; Blender rendering is CPU/GPU compositing.
- **Engine:** blender · **Applies to:** rigging · **Base:** TRELLIS · **Kind:** pipeline
- **VRAM:** 16-24
- **Base model (model-knowledge):** `microsoft/TRELLIS.2-4B`
- **Output license:** commercial **yes** (license: MIT (TRELLIS.2-4B); GPL (Blender app); rendered output unrestricted) — TRELLIS.2-4B is MIT, confirmed via Hugging Face model card and GitHub repo. Blender GPL covers the app only. Rendered sprite frames and the game build are fully the studio's IP.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| camera_angle_2.5D | 30-45 degrees elevation from character center | ○ | Typical JRPG 2.5D top-down perspective |
| camera_type | Orthographic | ○ | Required for consistent sprite sizing across directions |
| render_directions | 8 | ○ | N, NE, E, SE, S, SW, W, NW; 4 is minimum viable |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| TRELLIS.2-4B mesh topology can be dense/irregular — decimation or retopology may be needed before clean skinning. |  |  |  |
| Stylized proportions (hero with exaggerated features) may require mesh editing post-generation before rigging. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=unverified] -> confirmed (measured-on-rig — rig is authoritative); not-found x1 [only 1 of 3 juror(s) confirmed [confirmed, unverified]]
- **Sources:** [microsoft/TRELLIS.2 — GitHub](https://github.com/microsoft/TRELLIS.2) (Microsoft Research, 2025) — TRELLIS.2-4B generates high-fidelity 3D meshes with PBR materials from images; released under MIT license with model weights on Hugging Face. ; [Render 4 or 8 Direction Animated Sprites from Blender — Foozle](https://foozlecc.itch.io/render-4-or-8-direction-sprites-from-blender) (Foozle, 2024) — Community-documented workflow for rendering multi-directional 2D/2.5D animated sprites from Blender armature animations using orthographic cameras. ; [microsoft/TRELLIS.2-4B — Hugging Face](https://huggingface.co/microsoft/TRELLIS.2-4B) (Microsoft Research, 2025) — TRELLIS.2-4B model weights are released under MIT license, permitting commercial use; model produces static meshes with PBR materials requiring separate rigging.

### UniRig auto-rig (skeleton + learned skin) on RTX 5090 sm_120 via WSL2 — MEASURED · `recommended` · ▣ measured
**UniRig's full two-stage pipeline (autoregressive skeleton prediction + cross-attention learned skinning) runs end-to-end on a Blackwell RTX 5090 (sm_120) inside WSL2, producing a deforming rigged GLB from a TRELLIS.2 mesh — measured on the studio rig 2026-06-25.**
Native Windows is blocked (no cu13x torch_scatter/torch_cluster Windows wheels; flash_attn sm_120 source builds crash on backward kernels). WSL2 Ubuntu solves it with prebuilt Linux wheels and GPU passthrough. VERIFIED combo: Python 3.11 + torch 2.9.0+cu128; torch_scatter 2.1.2 / torch_cluster 1.6.3 (+pt29cu128 from data.pyg.org); spconv-cu126 2.3.8 (SparseConv3d runs on sm_120 via PTX forward-compat — the traveller59 issue #746 gemm error did NOT occur with the prebuilt wheel); flash_attn 2.8.1+cu128torch2.9 PREBUILT wheel from github.com/mjun0812/flash-attention-prebuild-wheels release v0.4.22 (cp311 linux) — its forward kernel runs on sm_120 in BOTH self- and cross-attention (gate-verified before use). UniRig requirements.txt installs clean on py3.11 (open3d 0.19 caps at cp312 + bpy 4.2 at cp311 -> py3.13 FAILS). bpy 4.2 needs X11 system libs even headless (apt install libsm6 libxext6 libxrender1 libxxf86vm1 libxfixes3... as WSL root). torch>=2.6 needs torch.load(weights_only=False) forced via a sitecustomize.py (UniRig checkpoints pickle box.box.Box; lightning passes weights_only=True explicitly). Run order: generate_skeleton.sh (works flash-free with _attn_implementation:sdpa in the AR config) -> generate_skin.sh (needs REAL flash_attn) -> merge.sh -> rigged GLB. Merge throws a harmless Draco-missing warning + a cosmetic bpy-teardown segfault AFTER writing the GLB. Proven on an armored humanoid (TRELLIS.2 mesh, 822k verts): 28 predicted bones + 28 vertex-group learned skin; Blender pose-test confirms the mesh deforms.
- **For the pipeline:** This is the studio's auto-rig backbone for the 68-character MESH game-asset line (fantasy-villains/goblins/pirates-mesh). UniRig auto-rigs ANY mesh including the 15 exotic pirate species (tortle/kenku/minotaur/sahuagin) that humanoid-template auto-riggers (Rigify/Mixamo/AccuRIG) cannot — and unlike Mixamo (EULA: no standalone redistribution) its MIT output is redistributable. Append the weapon_grip rigid bone-chain (see weapon-grip-rigid-bone-chain) after rigging. Blender automatic-weights is the no-flash_attn fallback for odd/exotic meshes. KEY OPERATIONAL LESSON: match the torch version to an AVAILABLE prebuilt flash_attn wheel (mjun0812 covers torch 2.9-2.12, NOT 2.8) rather than building from source for sm_120; decimate the dense TRELLIS mesh to ~30-50k tris for a game-weight asset.
- **Engine:** huggingface · **Applies to:** rigging · **Base:** autoregressive transformer · **Kind:** pipeline
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: UniRig MIT; flash_attn BSD-3; spconv/cumm Apache-2.0; torch_scatter/torch_cluster MIT; bpy GPL (output unrestricted). All commercial-safe.) — All deps permissive; the rigged GLB output is the studio's IP. Mixamo deliberately avoided for redistribution reasons.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| py3.13 FAILS — open3d (cp312 max) + bpy 4.2 (cp311) have no cp313 wheel; use py3.11. |  |  |  |
| torch 2.8 has no mjun0812 flash_attn wheel — use torch 2.9 (or 2.10); match the wheel to the torch. |  |  |  |
| An SDPA flash_attn stub unblocks the skeleton IMPORT but FAILS skin (skin uses cross-attn Wq/Wkv; a packed-Wqkv stub -> state_dict mismatch). Real flash_attn required for the skin stage. |  |  |  |
| Repeated wsl.exe cold-starts respin the VM + snapd/unattended-upgrades (CPU spike) — keep one WSL session warm. |  |  |  |
| TRELLIS.2 mesh is dense (~800k verts) — decimate before shipping the rigged GLB. |  |  |  |

- **Verify:** measured-on-rig (studio mesh-line, sprite-mesh-line-kickoff.md 2026-06-25) — rig is authoritative; not cloud-jury adjudicated (a web juror cannot verify an on-rig run). [no external verdict — not checked]
- **Sources:** [Studio RTX 5090 / WSL2 Ubuntu 26.04 — UniRig skeleton+skin end-to-end on the blackguard mesh](https://github.com/VAST-AI-Research/UniRig) (mcp-tool-shop studio, 2026) — Full UniRig pipeline (skeleton + learned skin + merge) produced a deforming rigged GLB on a Blackwell RTX 5090 via WSL2; flash_attn 2.8.1 forward kernel verified on sm_120. ; [mjun0812/flash-attention-prebuild-wheels (release v0.4.22)](https://github.com/mjun0812/flash-attention-prebuild-wheels) (mjun0812, 2026) — Prebuilt flash_attn Linux wheels for torch 2.9-2.12 / cu126-cu130 / cp311+ — the cu128torch2.9 cp311 wheel runs its forward kernel on sm_120 Blackwell.

### Auto-rigger license landscape: UniRig MIT vs Rigify GPL vs AccuRIG EULA vs Auto-Rig Pro paid vs Mixamo NC-redistribute · `recommended` · ▸ reproduced
**Among the major auto-rigging tools available in 2025-2026, UniRig (MIT weights + MIT code) is the only SIGGRAPH-class AI auto-rigger with a fully permissive commercial license on both code and model weights. The alternatives each carry specific restrictions that affect commercial game shipping: Rigify (GPL app, output clean), AccuRIG (freeware app, content EULA restricts redistribution of rigged assets via Reallusion content), Auto-Rig Pro (paid per-license, output unrestricted), Mixamo (royalty-free commercial use OK but no standalone asset redistribution).**
Rigify is GPL-licensed as a Blender addon; the Blender Foundation's position and community consensus is that the GPL covers the software tool, not the artist's output data — rigged meshes exported to FBX/GLTF are the studio's own IP, commercial use is fine. AccuRIG is free to download and the application itself has no commercial restriction, but assets accessed through the ActorCore platform carry EULA terms that restrict redistribution; rigging your own mesh with AccuRIG is generally unrestricted. Auto-Rig Pro is a paid Blender Market addon ($40 one-time); it is actively used in commercial games (Manor Lords, Fabledom) with no known output restriction. Mixamo (Adobe) is royalty-free for commercial games but prohibits redistributing raw animation/character files as standalone assets — shipping the game is fine, selling the extracted FBX is not. Research-only auto-riggers (RigNet, BoneGeo, older PIFU-HD rigs) are explicitly NC. UniRig is the only option in this tier that is AI-powered, high-quality on exotic meshes, and fully MIT on both the code and the distributed weights.
- **For the pipeline:** The studio's tool stack should use UniRig as the primary AI auto-rigger for novel and exotic-species meshes where manual rigging is slow. Rigify remains useful for standard humanoid base rigs in Blender. Auto-Rig Pro is a viable paid alternative. Mixamo retargeting is usable for motion but the studio should not redistribute extracted raw animations. Avoid any research-only auto-rigger (RigNet public checkpoints, any HF model with CC-BY-NC on weights) for the commercial pipeline.
- **Engine:** n/a · **Applies to:** rigging · **Kind:** reference
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: varies by tool — see commercial_notes) — UniRig: MIT code + MIT weights — fully commercial. Rigify: GPL app, output unrestricted — commercial OK. AccuRIG app: freeware commercial OK; Reallusion ActorCore content: EULA restricts redistribution of Reallusion-supplied assets. Auto-Rig Pro: paid license, output unrestricted — commercial OK. Mixamo: royalty-free for shipping commercial games; no redistribution of raw asset files. Research-only auto-riggers: NC weights — not usable commercially.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [VAST-AI-Research/UniRig — LICENSE](https://github.com/VAST-AI-Research/UniRig/blob/main/LICENSE) (VAST-AI-Research, 2025) — UniRig code is MIT. VAST-AI/UniRig HF card is also MIT on weights. ; [Rigify — Blender 5.1 Manual](https://docs.blender.org/manual/en/latest/addons/rigging/rigify/index.html) (Blender Foundation, 2025) — Rigify is a GPL Blender addon. Community and Blender Foundation consensus: GPL covers the tool, not the output mesh/armature data exported by the artist. ; [Mixamo FAQ — Licensing, Royalties, Ownership, EULA and TOS](https://community.adobe.com/t5/mixamo-discussions/mixamo-faq-licensing-royalties-ownership-eula-and-tos/td-p/13234775) (Adobe / Mixamo, 2025) — Mixamo is royalty-free for commercial games. Raw asset file redistribution (selling extracted FBX/character files) and bulk ML downloads are prohibited. ; [Auto-Rig Pro — Superhive (Blender Market)](https://superhivemarket.com/products/auto-rig-pro) (Artell, 2025) — Auto-Rig Pro is a paid ($40 approx) one-time purchase. Extended Commercial License available. Used commercially in shipped titles (Manor Lords, Fabledom). No known output restriction on rigged meshes. ; [Free Auto Rig for any 3D Character / AccuRIG — ActorCore](https://actorcore.reallusion.com/auto-rig/accurig) (Reallusion, 2025) — AccuRIG application is freeware for personal and commercial use. Reallusion-supplied ActorCore content carries separate EULA restricting redistribution. Rigging your own mesh assets with AccuRIG is not clearly restricted by content EULA.

### Rigify — Blender's bundled modular auto-rigger · `recommended` · ▸ reproduced
**Rigify generates a production-quality, game-exportable control rig from a positioned metarig in one click, with built-in face, hand, and spine components.**
Enable the Rigify add-on (bundled with Blender, no install required). Place a humanoid metarig and position bones to the character mesh. Press Generate Rig — Rigify outputs a layered control rig with FK/IK switching, squash-and-stretch controls, and a clean deform-bone subset. For sprite workflows, bake the FK deform bones to a simple action, then render. Rigify rigs export cleanly to FBX for Godot/UE5 because the deform bones have standard naming. Authors: Nathan Vegdahl, Lucio Rossi, Ivan Cappiello, Alexander Gavrilov.
- **For the pipeline:** Using Rigify as the authoring rig gives the studio a canonical deform-bone set that Auto-Rig Pro can retarget mocap onto and that Godot's Skeleton3D importer recognizes. Append the weapon_grip chain to the generated rig's hand.R deform bone after generation.
- **Engine:** blender · **Applies to:** rigging · **Base:** n/a · **Kind:** model
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: GPL (Blender add-on included in distribution)) — Rigify is GPL. Your character rigs and rendered output are not GPL-encumbered — GPL covers the Python add-on code, not artist output produced with it.
- **Fit:** rig 5/5 · studio 4/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Rigify — Blender 5.1 Manual](https://docs.blender.org/manual/en/latest/addons/rigging/rigify/index.html) (Blender Foundation / Vegdahl, Rossi, Cappiello, Gavrilov, 2025) — Rigify is a modular auto-rigging system bundled with Blender; it generates a full control rig with FK/IK switching from a positioned metarig template.

### UniRig Hugging Face checkpoints: what is actually downloadable vs. coming soon · `recommended` · ▸ reproduced
**The VAST-AI/UniRig Hugging Face repo (11.5 GB total) contains separate skeleton/ and skin/ checkpoint directories; only the skeleton + skin model trained on Articulation-XL2.0 is currently downloadable — the Rig-XL and VRoid-trained variants described in the paper are listed as 'Coming Soon'. License is MIT.**
The VAST-AI/UniRig HF repo has two checkpoint directories: skeleton/ (skeleton prediction checkpoint) and skin/ (articulation model checkpoint, model.ckpt). Total repo size is ~11.5 GB. The currently downloadable model was trained on the Articulation-XL2.0 dataset — which is a subset of the full Rig-XL (14,611 models) described in the paper. The paper's full results were obtained using Rig-XL + VRoid training data (14,611 + 2,061 models); these checkpoints are not yet released. The model card explicitly states that 'Model checkpoints trained on Rig-XL and VRoid datasets are coming soon.' The weights download automatically via the UniRig inference scripts using the Hugging Face Hub API. No parameter count is disclosed in the model card. The license field on the HF card is MIT, matching the GitHub repo LICENSE file.
- **For the pipeline:** The Articulation-XL2.0-trained checkpoint is the one measured on the studio rig (unirig-blackwell-wsl2-skeleton-skin-measured). The not-yet-released Rig-XL + VRoid checkpoints will likely produce better results for diverse non-humanoid topologies (Rig-XL covers 8 categories including quadrupeds, insects, water creatures) — watch the VAST-AI/UniRig HF repo for the update. The current checkpoint already handles exotic humanoid-adjacent species well enough for the 68-character mesh line, as measured. Do not hand-edit the downloaded checkpoints; the scripts manage weight loading via HF Hub.
- **Engine:** huggingface · **Applies to:** rigging · **Kind:** model
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT) — HF model card license field: MIT. GitHub LICENSE file: MIT. Both confirmed by direct inspection. Applies to currently downloadable weights.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| repo_size_gb | 11.5 | ○ | Total HF repo size including skeleton/ and skin/ checkpoints |
| training_dataset_available | Articulation-XL2.0 | ○ | Subset of Rig-XL; the 14,611-model Rig-XL + 2,061-model VRoid checkpoints are Coming Soon |
| checkpoint_dirs | skeleton/, skin/ | ○ | Separate directories for each stage; model.ckpt in skin/ |
| download_method | automatic via HF Hub in inference scripts | ○ | No manual download required; scripts handle authentication-free public repo access |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=unverified] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, unverified]]
- **Sources:** [VAST-AI/UniRig — Hugging Face model card](https://huggingface.co/VAST-AI/UniRig) (VAST AI Research, 2025) — Model card states: skeleton prediction model trained on Articulation-XL2.0 is available; Rig-XL and VRoid variants are 'Coming Soon'; license field is MIT; minimum VRAM is >8GB CUDA GPU. ; [VAST-AI/UniRig — HF file tree (main branch)](https://huggingface.co/VAST-AI/UniRig/tree/main) (VAST AI Research, 2025) — File tree shows separate skeleton/ and skin/ checkpoint directories; total repo ~11.5 GB; 13 commits from 3 contributors.

### UniRig SIGGRAPH 2025 / ACM TOG paper: arXiv:2504.12451, DOI 10.1145/3730930 · `recommended` · ▸ reproduced
**The canonical citation for UniRig is: Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu. 'One Model to Rig Them All: Diverse Skeleton Rigging with UniRig.' ACM Transactions on Graphics (Proc. SIGGRAPH 2025). DOI: 10.1145/3730930. arXiv preprint: arXiv:2504.12451.**
The paper introduces UniRig at SIGGRAPH 2025 (published in ACM Transactions on Graphics). Five authors: Jia-Peng Zhang (first author, Tsinghua University), Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu. Tsinghua University and VAST AI Research joint affiliation. The arXiv preprint (2504.12451) was posted April 2025; the ACM DOI (10.1145/3730930) is the peer-reviewed TOG publication. Key contributions: (1) Skeleton Tree Tokenization for autoregressive skeleton generation; (2) Rig-XL dataset (14,611 rigged models, 8 categories); (3) bone-point cross-attention skinning with geodesic distance; (4) 215% improvement in rigging accuracy and 194% improvement in motion accuracy over prior state-of-art on held-out test sets. Note: the existing wave-01 recipe (unirig-ai-auto-rigger-mit) cites 'Wang, Lingteng et al.' as authors — this appears to be a different paper confusion; the correct first author of UniRig is Jia-Peng Zhang per the arXiv abstract and HTML full text.
- **For the pipeline:** Correct author attribution matters when citing UniRig in studio knowledge base and any external communications. The Zhang et al. / Tsinghua + VAST affiliation is the verified ground truth. The ACM DOI provides a stable, citable identifier. The SkinTokens follow-on (arXiv:2602.04805, 2026) unifies the two stages into a single Qwen3-0.6B token stream — monitor for release as a potential UniRig upgrade path.
- **Engine:** custom · **Applies to:** rigging · **Kind:** technique
- **VRAM:** n/a
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT (code + weights)) — License note for the paper itself: ACM copyright; code and weights MIT as noted in repo.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig](https://arxiv.org/abs/2504.12451) (Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu, 2025) — arXiv abstract page confirms full author list (Zhang, Pu, Guo, Cao, Hu), Tsinghua + VAST affiliation, SIGGRAPH 2025 / ACM TOG venue. ; [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig — ACM Digital Library](https://dl.acm.org/doi/10.1145/3730930) (Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu, 2025) — ACM Digital Library entry for the peer-reviewed TOG publication; DOI 10.1145/3730930 confirmed via search result (403 on direct fetch, but DOI is confirmed from search result metadata).

### UniRig commercial license: MIT on code AND released HuggingFace checkpoints · `recommended` · ▸ reproduced
**UniRig is MIT-licensed on both the GitHub source code (VAST-AI-Research/UniRig, Copyright 2025 VAST-AI-Research and contributors) and the published HuggingFace checkpoints (VAST-AI/UniRig, license field: MIT) — a rare fully-permissive release for a SIGGRAPH 2025 class auto-rigger. The studio can ship UniRig-rigged game assets commercially without license drag on the tool itself.**
The GitHub LICENSE file is unambiguously MIT: 'Copyright (c) 2025 VAST-AI-Research and contributors. Permission is hereby granted, free of charge, to any person obtaining a copy of this software...' The HuggingFace model card for VAST-AI/UniRig declares the license field as 'mit' with no non-commercial clause or usage restriction visible on the card. MIT grants the right to 'use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies' — the only obligation is retaining the copyright notice. This combination (MIT code + MIT weights) is uncommon for SIGGRAPH-class research artifacts; most comparable models ship research-only or CC-BY-NC weights.
- **For the pipeline:** UniRig is the commercial-clean default auto-rigger for the studio's exotic-species and humanoid lines. Rigged GLBs exported from UniRig are the studio's own IP. No per-seat fee, no royalty clause, no NC restriction blocks a Steam commercial release. Monitor future checkpoint releases: MIT on the current checkpoint does not bind VAST-AI for future weight drops — always verify the HF card license field before integrating a new checkpoint into the pipeline.
- **Engine:** n/a · **Applies to:** rigging · **Kind:** reference
- **VRAM:** n/a
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT (code + released weights)) — MIT on the GitHub repo and the HuggingFace VAST-AI/UniRig model card. No non-commercial clause, no revenue cap, no attribution requirement beyond preserving the copyright notice in redistributed code. Rigged mesh outputs (GLB/FBX) are not derivative works of the model weights under copyright law — they are the studio's own 3D data processed through the tool. Training-data terms (see unirig-training-data-objaverse-terms recipe) do not automatically propagate to rig outputs.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [VAST-AI-Research/UniRig — LICENSE](https://github.com/VAST-AI-Research/UniRig/blob/main/LICENSE) (VAST-AI-Research, 2025) — Repository LICENSE file is MIT, copyright 2025 VAST-AI-Research and contributors. Full permissive grant with no non-commercial restriction. ; [VAST-AI/UniRig — Hugging Face model card](https://huggingface.co/VAST-AI/UniRig) (VAST-AI, 2025) — Model card license field is 'mit'. No non-commercial clause, no usage restrictions noted on the card.

### UniRig community adoption and real-pipeline usage evidence (2025-2026) · `recommended` · ▸ reproduced
**UniRig has measurable community adoption beyond academic use: a maintained ComfyUI wrapper (420+ commits, ComfyUI Manager installable), a Hugging Face Spaces demo (jkorstad/Mesh_Rigger), community tutorial articles, and confirmed end-to-end studio use on exotic non-humanoid meshes (studio RTX 5090 measured run) — evidence that it is a real production-path tool, not vaporware.**
Adoption evidence: (1) ComfyUI-UniRig wrapper by PozzettiAndrea (GPL-3.0, 420+ commits, installable via ComfyUI Manager) is actively maintained and integrates UniRig + Make-It-Animatable in one node graph. (2) Hugging Face Space jkorstad/Mesh_Rigger hosts a public demo using UniRig's README directly. (3) Community tutorial articles (Apatero, ComfyUI Wiki) document real installation and workflow steps. (4) Studio measured run on RTX 5090 / WSL2 confirmed end-to-end pipeline on an armored humanoid mesh (28 predicted bones, learned skinning, Blender pose-test). UniRig's SIGGRAPH 2025 / ACM TOG publication and 215%/194% accuracy improvements over prior art (Rignet, TripoSG-rigging) make it academically credible. The successor (SkinTokens, arXiv Feb 2026) validates the research lineage. No evidence of false-start or abandoned status.
- **For the pipeline:** UniRig is a safe bet for the studio's mesh-asset line: real code, real weights, real community adoption, real SIGGRAPH paper, real successor in development. The ComfyUI-UniRig wrapper gives a visual-graph alternative to shell scripts for operators uncomfortable with WSL2. The jkorstad Mesh_Rigger HF Space gives a zero-setup sanity-check demo for testing new mesh types before committing to the full WSL2 install.
- **Engine:** python · **Applies to:** rigging · **Kind:** technique
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT (UniRig); GPL-3.0 (ComfyUI wrapper); output unrestricted) — All adoption paths commercial-clean on the output. GPL-3.0 wrapper does not affect produced 3D assets.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, unverified]]
- **Sources:** [PozzettiAndrea/ComfyUI-UniRig — GitHub (adoption evidence)](https://github.com/PozzettiAndrea/ComfyUI-UniRig) (PozzettiAndrea, 2025) — 420+ commits; ComfyUI Manager installable; active maintenance; community usage via tutorial documentation — concrete adoption signal beyond the research paper. ; [jkorstad/Mesh_Rigger — Hugging Face Space (UniRig demo)](https://huggingface.co/spaces/jkorstad/Mesh_Rigger/blob/main/UniRig/README.md) (jkorstad, 2025) — Public HF Space demo using UniRig's pipeline directly; confirms the model weights and inference scripts are functional in a zero-setup environment — useful for testing new mesh types before WSL2 install. ; [Studio RTX 5090 / WSL2 Ubuntu — UniRig measured run 2026-06-25](https://github.com/VAST-AI-Research/UniRig) (mcp-tool-shop studio, 2026) — End-to-end UniRig (skeleton + skin + merge) confirmed on Blackwell RTX 5090 / WSL2 Ubuntu; 28 predicted bones + learned skin; Blender pose-test confirms deformation — production-path validation.

### UniRig in the studio flow: TRELLIS.2 mesh → UniRig rig → weapon_grip chain → Blender 8-dir render · `recommended` · ▸ reproduced
**UniRig is the rig stage between the TRELLIS.2 mesh and the Blender 8-direction sprite render: auto-rig the mesh with two shell scripts, append the rigid weapon_grip→weapon_tip bone chain, animate NLA actions, then render — turning a static mesh into an animatable game asset in one open-source pipeline.**
Import the TRELLIS.2 GLB (decimated to 30-50k tris), run generate_skeleton.sh (outputs FBX skeleton), run generate_skin.sh (outputs FBX with skinning weights), run merge.sh to produce the final rigged GLB. The rigged GLB drops straight into Blender for armature inspection and weapon_grip chain append (see weapon-grip-rigid-bone-chain recipe). After appending weapon bones, build NLA actions (walk, attack, idle, hurt, death) and render 8 orthographic directions. UniRig's FBX/GLB output is the rig that wave-2 mocap retargets onto — it is the skeleton anchor for the whole motion line.
- **For the pipeline:** This is the rig backbone for the 68-character mesh game-asset line. It connects the TRELLIS.2 mesh path (sprites-knowledge) directly to wave-1 motion render and wave-2 retarget content. Because UniRig is MIT and its output is the studio's IP, the full line is commercial-clean with no redistribution restrictions.
- **Engine:** blender · **Applies to:** rigging · **Kind:** pipeline
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Builds on (stage 1):** UniRig auto-rig (skeleton + learned skin) on RTX 5090 sm_120 via WSL2 — MEASURED
- **Output license:** commercial **yes** (license: MIT (UniRig); Blender output unrestricted) — All stages commercial-clean. UniRig MIT license confirmed via GitHub LICENSE file. Rigged GLB output is studio IP.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [VAST-AI-Research/UniRig — README pipeline commands](https://github.com/VAST-AI-Research/UniRig) (VAST AI Research, 2025) — Documents the three-command pipeline: generate_skeleton.sh (GLB in → FBX skeleton), generate_skin.sh (FBX skeleton → FBX with weights), merge.sh (FBX + original GLB → rigged GLB). Supports batch mode via --input_dir / --output_dir.

### UniRig input mesh requirements and output format spec · `recommended` · ▸ reproduced
**UniRig accepts OBJ, FBX, GLB, and VRM input meshes, converts them to Y-up world space internally, requires no explicit watertight constraint, and outputs rigged FBX (skeleton stage) + FBX with per-vertex skin weights (skin stage) that can be merged to a final rigged GLB or FBX.**
Supported input:.obj,.fbx,.glb,.vrm. No explicit vertex count limit is documented, but internally the pipeline samples exactly 65,536 surface points for shape encoding — meaning the actual mesh polygon count is decoupled from the encoder input (a 3M-tri mesh and a 10k-tri mesh both feed 65,536 sampled points into the shape encoder). The internal coordinate system is Y-up world space (the README states models are 'converted into world space... aligned to Y-up axis, consistent with Blender'). No watertight mesh requirement is stated. Minimum GPU: CUDA-capable with >8GB VRAM. Inference sequence: (1) generate_skeleton.sh --input <mesh> --output <skeleton.fbx>; (2) generate_skin.sh --input <skeleton.fbx> --output <skinned.fbx>; (3) merge.sh --source <skinned.fbx> --target <original_mesh> --output <rigged.glb>. Intermediate outputs support NPZ, OBJ, FBX. Final merged output is GLB (or FBX). The merge step produces a Draco-missing warning and a cosmetic bpy segfault after GLB write — both are harmless (measured on studio rig 2026-06-25, cross-reference unirig-blackwell-wsl2-skeleton-skin-measured).
- **For the pipeline:** GLB-in → GLB-out is the studio's native path (TRELLIS.2 outputs GLB). The 65,536-point sampling means a dense TRELLIS mesh (~800k verts) does not need to be decimated for the UniRig encoder — but should still be decimated before shipping in-engine to ~30-50k tris for game performance. Y-up matches Blender's default, so no coordinate-system fix is needed on import. VRM support is a bonus for any anime-adjacent character assets (excluded from studio canon but noted for completeness).
- **Engine:** huggingface · **Applies to:** rigging · **Kind:** technique
- **VRAM:** 8
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT) — MIT license covers code, inference pipeline, and output weights. Output rigged meshes are the studio's IP.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| input_formats | obj, fbx, glb, vrm | ○ | All four confirmed in README |
| internal_coord_system | Y-up world space | ○ | Models converted to world space aligned to Y-up axis, consistent with Blender |
| shape_encoder_points | 65536 | ○ | Fixed point-cloud sample size regardless of input mesh polygon count |
| output_formats | fbx (skeleton), fbx (skinned), glb or fbx (merged) | ○ | NPZ and OBJ also available as intermediate formats |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [VAST-AI-Research/UniRig — README.md](https://github.com/VAST-AI-Research/UniRig/blob/main/README.md) (VAST AI Research, 2025) — README lists supported input formats (obj, fbx, glb, vrm), minimum GPU requirement (>8GB VRAM), Y-up world space alignment, and inference shell command syntax including merge to GLB output. ; [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig (HTML full text)](https://arxiv.org/html/2504.12451v1) (Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu, 2025) — Paper states 65,536 surface points sampled from the mesh for shape encoding, with normals included; coordinate normalization to [-1,1]^3 for skeleton token generation.

### UniRig redistribution, sublicensing, and commercial derivative works under MIT · `recommended` · ▸ reproduced
**Under MIT, the studio can redistribute UniRig code, sublicense it, incorporate it into proprietary pipeline tooling, and sell products that were processed using it — with the sole obligation to include the copyright notice when redistributing the source code itself. The rigged mesh output is not a reproduction of the model and carries no license obligation whatsoever.**
MIT is the most permissive OSI-approved license: it grants 'without restriction' the right to 'use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.' The only condition is that the MIT copyright notice is included in all copies or substantial portions of the Software code. Rigged 3D mesh outputs (GLB, FBX, USD) are not 'copies of the Software' — they are the studio's original asset data transformed by the tool. There is no share-alike, no copyleft, no patent grant requirement, and no attribution requirement on the game product itself. The studio could in principle also fine-tune or retrain on UniRig's architecture under MIT, subject only to the training-data considerations in the companion recipe.
- **For the pipeline:** The studio can embed UniRig inference into a proprietary CI/CD pipeline, sell that pipeline as a service, or ship a game that uses it without any license disclosure in the game product itself. If redistributing UniRig's code (e.g. in a public tool), include the MIT copyright notice. No royalty, no CLA, no attribution in credits required — though crediting VAST-AI in any public-facing tooling docs is good community practice.
- **Engine:** n/a · **Applies to:** rigging · **Kind:** reference
- **VRAM:** n/a
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT) — Full MIT grant covers redistribution, sublicensing, and sale of code. Output mesh assets have no license obligation at all — they are the studio's own IP. Copyright notice required only when distributing UniRig source code itself.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [VAST-AI-Research/UniRig — LICENSE (full MIT text)](https://raw.githubusercontent.com/VAST-AI-Research/UniRig/main/LICENSE) (VAST-AI-Research, 2025) — Full MIT license text: 'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files... to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.' Only obligation: include copyright notice in copies of the software.

### UniRig skeleton tree tokenization: DFS ordering + 256-bin coordinate discretization · `recommended` · ▸ reproduced
**UniRig encodes a skeleton hierarchy as a linear token sequence using depth-first search traversal with bones sorted by (z,y,x) tail coordinates, discretizing each bone's 3D position into three tokens from a 256-bin vocabulary — enabling a standard next-token-prediction transformer to autoregressively generate topologically valid skeleton trees.**
Bone coordinates are first normalized to [-1,1] then mapped to 256 discrete bins via M(x) = floor((x+1)/2 × 256). Each bone contributes three coordinate tokens (dx, dy, dz). The sequence begins with <bos> and a dataset class token (e.g. <VRoid>, <Mixamo>), then optional template type tokens (<mixamo:body>, <mixamo:hand>, <spring_bone>) for known skeleton templates, then coordinate triples in DFS order with <branch_token> prefixes marking each new branch. The optimized scheme omits parent coordinates for template bones (structure is inferrable from the template name), reducing token count by ~27-30% compared to the naive per-joint encoding. A <eos> token terminates the sequence. This scheme guarantees topological validity: the transformer cannot produce an orphan joint because parent-child relationships are implicit in the DFS prefix structure.
- **For the pipeline:** The tokenization is the architectural reason UniRig can handle exotic non-humanoid species without template constraints — the <cls> token switches the prior, and the DFS token stream encodes any tree topology. For the studio's 15 exotic species (tortle, kenku, sahuagin, minotaur, etc.) no template token is used; the model generates free-form bone trees. Post-rig, the predicted bone names are generic (not Mixamo-compatible); an Auto-Rig Pro Remap step is needed to bind mocap onto the canonical studio hierarchy.
- **Engine:** huggingface · **Applies to:** rigging · **Kind:** technique
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT (code + weights, VAST-AI-Research/UniRig GitHub LICENSE file)) — MIT license confirmed from GitHub repo LICENSE file and Hugging Face model card license field. No usage restrictions.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| vocab_bins | 256 | ○ | Coordinate discretization bins per axis; M(x)=floor((x+1)/2×256) where x in [-1,1] |
| traversal_order | DFS | ○ | Children sorted by tail (z,y,x); branch_token prefix inserted at each branch point |
| token_reduction | ~27-30% | ○ | Measured on VRoid (~27.47%) and Rig-XL (~29.72%) vs naive per-joint encoding |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig](https://arxiv.org/abs/2504.12451) (Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu (Tsinghua University / VAST AI Research), 2025) — Section 3.1 of the paper defines the Skeleton Tree Tokenization: DFS traversal, 256-bin coordinate discretization, type/template/branch tokens, and measured ~27-30% token-count reduction over naive encoding. ; [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig (HTML full text)](https://arxiv.org/html/2504.12451v1) (Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu, 2025) — Full paper HTML confirms token vocabulary structure (<bos>, <eos>, <cls>, type identifiers, coordinate tokens) and the DFS ordering with branch_token prefixes.

### UniRig stage 1: OPT-125M autoregressive skeleton GPT over 3DShape2Vecset geometry encoding · `recommended` · ▸ reproduced
**UniRig's skeleton prediction stage uses a randomly-initialized 3DShape2Vecset encoder to compress a 65,536-point surface sample into a geometric embedding, then prepends that embedding to the token sequence and autoregressively generates skeleton tokens with an OPT-125M (125M parameter) decoder — training with standard next-token prediction loss.**
The input mesh is sampled to N=65,536 surface points with normals, fed through a 3DShape2Vecset shape encoder (parameters randomly initialized, not pretrained from a foundation model) producing a geometric embedding F_G ∈ R^(V×F). F_G is prepended to the skeleton token sequence. The OPT-125M decoder (Meta's Open Pre-trained Transformer, 125M parameters) then autoregressively generates skeleton tokens conditioned on both the geometric prefix and all prior tokens, using next-token-prediction loss: -sum(log P(s_t | s_1...s_{t-1}, F_G)). During training, 16,384 points are used for the skinning stage (reduced for memory efficiency). OPT-125M is a documented, publicly-available model variant — not a novel architecture — which means the skeleton generation stage is an application of standard decoder-only autoregression, not a proprietary transformer design.
- **For the pipeline:** OPT-125M is small by modern standards (125M parameters), which contributes to the sub-5-second inference claim on GPU — the shape encoder is the compute bottleneck, not the transformer itself. The randomly-initialized shape encoder means the model learns geometry grounding entirely from the Rig-XL supervision signal, not from a pretrained 3D foundation model. This limits generalization at the extremes (very unusual topologies) but keeps the weight footprint small. VRAM for the skeleton stage alone is well under the 8GB minimum floor stated by VAST-AI.
- **Engine:** huggingface · **Applies to:** rigging · **Kind:** model
- **VRAM:** 8
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT (UniRig code + weights); OPT-125M base architecture is Meta's OPT, but UniRig trained its own weights — license is MIT per repo.) — MIT license on UniRig repo and Hugging Face model card. OPT-125M architecture is open (Meta OPT paper); UniRig weights are new training, not fine-tuned OPT weights — MIT applies.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| point_cloud_size_inference | 65536 | ○ | Surface points + normals sampled from mesh for shape encoder at inference time |
| point_cloud_size_skin_training | 16384 | ○ | Reduced point count during skinning stage training for memory efficiency |
| transformer_variant | OPT-125M | ○ | Meta OPT-125M decoder architecture, 125M parameters, confirmed in paper |
| shape_encoder | 3DShape2Vecset | ○ | Randomly initialized (non-pretrained); learns geometry grounding from Rig-XL supervision |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig (HTML full text)](https://arxiv.org/html/2504.12451v1) (Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu, 2025) — Paper specifies OPT-125M as the autoregressive decoder variant, 65,536-point surface sampling with normals for shape encoding via 3DShape2Vecset (randomly initialized), and next-token-prediction training objective. ; [VAST-AI/UniRig — Hugging Face model card](https://huggingface.co/VAST-AI/UniRig) (VAST AI Research, 2025) — Model card confirms MIT license, describes the skeleton prediction model as the first stage of the UniRig pipeline (skeleton + skinning), trained on Articulation-XL2.0; minimum GPU VRAM stated as >8GB.

### UniRig stage 2: bone-point cross-attention skinning with geodesic distance refinement · `recommended` · ▸ reproduced
**UniRig's skinning stage encodes predicted bone positions via an MLP bone encoder and mesh points via a pretrained Point Transformer V3 (from SAMPart3D), then computes bone-point cross-attention weights, concatenates them with voxelized geodesic distances, and passes the result through a skinning MLP + softmax to produce per-vertex skin weights.**
Inputs to stage 2 are: (a) the predicted skeleton — head/tail coordinates (J_P, J) ∈ R^(J×6) for J bones, and (b) the original mesh as a point cloud. The Bone Encoder (E_B) is an MLP with positional encoding producing bone features F_B ∈ R^(J×F). The Point Encoder (E_P) is a pretrained Point Transformer V3 (sourced from SAMPart3D) producing per-point features F_P ∈ R^(N×F). Cross-attention is then computed with mesh points as queries and bone features as keys/values: attention weights = softmax(Q_W × K_W^T / sqrt(F)). These attention weights are concatenated with the voxelized geodesic distance D ∈ R^(N×J) (which encodes surface-distance proximity, preventing skin weight bleed across concavities). The combined [attention | geodesic] tensor is passed through the skinning weight MLP (E_W) and a final softmax normalization to produce valid skin weights summing to 1 per vertex. Bone-specific attributes (gravity, stiffness coefficients for spring bones) are predicted via reverse cross-attention (bones as queries, points as keys/values) through a separate MLP. This design means skinning quality is tightly coupled to skeleton quality — poor skeleton prediction propagates directly into bad skin weights.
- **For the pipeline:** The geodesic distance term is the key architectural move that makes skinning correct across concave meshes (inside of an armpit, between fingers) where Euclidean-distance skinning fails. For the studio's exotic species with anatomical concavities (crab claws, wing membranes, scaled bodies) this is load-bearing. If the skeleton stage mis-predicts (missing a tail bone, wrong wing topology), skinning degrades significantly — the paper and README both call this out explicitly as the primary failure mode. The mitigation is manual skeleton refinement in Blender before running the skin stage.
- **Engine:** huggingface · **Applies to:** rigging · **Kind:** technique
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **conditional** (license: MIT (UniRig code + weights); Point Transformer V3 sourced from SAMPart3D — verify its license before redistribution.) — UniRig MIT applies to the full pipeline including the skinning stage. SAMPart3D/Point Transformer V3 is used as a pretrained component; its license (Apache-2.0 per SAMPart3D repo) is compatible with commercial use. Verify independently before redistribution.
- **License correction (verifier):** Point Transformer V3 / SAMPart3D license is not MIT and must be verified independently; the recipe itself flags this but still claims commercial_use=yes which is premature.; commercial_use is conditional; verify SAMPart3D license for Point Transformer V3 before commercial use.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Skinning quality degrades significantly if the skeleton stage produced an inaccurate topology (missing tail bones, wrong wing bone count) — manual skeleton QA before running the skin stage is mandatory for exotic meshes. |  |  |  |
| Geodesic distance computation requires a watertight-ish mesh for correct surface-distance measurement; severely non-manifold geometry may produce incorrect distance fields and therefore incorrect skin weight bleed. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [license -> commercial_use=conditional] [confirmed by 3 of 3 juror(s) [confirmed-with-fixes]]
- **Sources:** [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig (HTML full text)](https://arxiv.org/html/2504.12451v1) (Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu, 2025) — Sections 3.2-3.3 describe bone encoder (MLP with positional encoding), point encoder (pretrained Point Transformer V3 from SAMPart3D), cross-attention weight computation, voxel geodesic distance concatenation, and skinning MLP + softmax normalization. ; [VAST-AI-Research/UniRig — README (inference limitations)](https://github.com/VAST-AI-Research/UniRig) (VAST AI Research, 2025) — README states: 'The results may degrade significantly if the skeleton is inaccurate — for example, if tail bones or wing bones are missing' — confirming the skeleton→skinning error propagation path.

### UniRig inference speed: 1-5 second end-to-end rigging claim vs. commercial baselines · `recommended` · · single-run
**The UniRig paper reports 1-5 second total rigging time (skeleton + skinning + merge), compared to RigNet (1 second to 20 minutes depending on bone count), Tripo commercial (2 minutes), Anything World (5 minutes), and Meshy (1-2 minutes) — but no hardware specification is given for the 1-5 second figure.**
Table 1 of the paper lists inference speed as '1~5 s' for UniRig versus the commercial baselines. The hardware used for this measurement is not stated in the paper. The OPT-125M transformer is computationally lightweight (125M parameters); the shape encoder (3DShape2Vecset on 65,536 points) is the likely bottleneck, not the autoregressive generation itself. The skinning stage runs Point Transformer V3 inference on the point cloud plus cross-attention, which at 16,384 points in training mode adds meaningful compute. On the studio RTX 5090, each stage completes in wall-clock time consistent with the 1-5s claim (not independently timed; measured total is consistent with the claim per studio run 2026-06-25, cross-reference unirig-blackwell-wsl2-skeleton-skin-measured). The 1-5 second figure is a single-reported number from the paper authors — not independently benchmarked on a third-party rig.
- **For the pipeline:** Even at the 5-second ceiling, UniRig is 24× faster than Tripo commercial (2 min) and 240× faster than RigNet's worst case. For a 68-character mesh line, batching all meshes through UniRig in a WSL2 script is practical (~5 min total for the full roster at 5s/mesh). The speed also makes iterating on mesh quality (re-generate in TRELLIS, re-rig in UniRig) low-cost compared to any manual or cloud-service path.
- **Engine:** huggingface · **Applies to:** rigging · **Kind:** technique
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT) — License does not affect this recipe — it documents a performance claim, not a new deployment step.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| reported_inference_time | 1-5 seconds | ○ | Full pipeline (skeleton + skin + merge); hardware unspecified in paper |
| comparison_rigneg | 1s-20min | ○ | RigNet speed varies with bone count |
| comparison_tripo | ~2 min | ○ | Commercial cloud service |
| comparison_meshy | 1-2 min | ○ | Commercial cloud service |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig (HTML full text)](https://arxiv.org/html/2504.12451v1) (Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu, 2025) — Table 1 reports UniRig inference time as '1~5 s' versus RigNet (1s-20min), Tripo (~2 min), Anything World (~5 min), Meshy (1-2 min). No GPU specification for the UniRig figure is given in the table or surrounding text.

### UniRig — VAST-AI/Tsinghua autoregressive skeleton predictor (SIGGRAPH 2025, MIT) · `recommended` · · single-run
**UniRig predicts a topologically valid skeleton hierarchy and per-vertex skinning weights for any 3D mesh input — humans, animals, objects — without hand-placing bones, under MIT license.**
UniRig (SIGGRAPH 2025 / ACM TOG) uses a Skeleton Tree Tokenization scheme to encode hierarchical bone relationships into linear sequences, then autoregressively generates skeleton joints and their coordinates. A second stage predicts per-vertex skinning weights. Trained on Rig-XL (14,000+ rigged models), it outperforms academic and commercial baselines by 215% on rigging accuracy and 194% on motion accuracy on held-out test sets. Model weights are MIT-licensed on Hugging Face (VAST-AI/UniRig). A Blender integration script is available in the repo. Output must be verified and the weapon_grip chain appended manually before the full studio pipeline.
- **For the pipeline:** UniRig is the best open, commercially-safe auto-rigger for novel character meshes (TRELLIS.2-4B → UniRig → Blender weapon_grip → NLA animate → 8-dir render). It eliminates bone placement for hero characters. However, its humanoid skeleton may not match the studio's exact bone naming; a remap step to the canonical hierarchy is needed before mocap retargeting.
- **Engine:** huggingface · **Applies to:** rigging · **Base:** autoregressive transformer · **Kind:** model
- **VRAM:** 8-24
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **conditional** (license: MIT (code + weights)) — MIT license confirmed by reading the LICENSE file in the VAST-AI-Research/UniRig GitHub repository. Weights on Hugging Face tagged MIT. No usage-based or non-commercial restrictions.
- **License correction (verifier):** Verify the actual license file on github.com/VAST-AI-Research/UniRig and the model card on HuggingFace (VAST-AI/UniRig) before claiming weights are MIT; research repos often release code as MIT but ship weights under a research-only or custom license — default commercial_use should be 'conditional' until the HF model card is confirmed.
- **Fit:** rig 4/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Skeleton topology for stylized 2.5D proportions (large head, short legs) may require bone-count trimming or re-parenting after prediction. |  |  |  |
| Weapon_grip chain must be appended manually — UniRig has no concept of held-prop bones. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [license -> commercial_use=conditional] | citation corrected (was wrong authors): arXiv:2504.12451, Zhang/Pu/Guo/Cao/Hu — wave-4 UniRig deep-dive + retrieval-confirmed. [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig](https://arxiv.org/abs/2504.12451) (Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu, 2025) — UniRig autoregressively predicts valid skeleton hierarchy and skinning weights for diverse 3D meshes; outperforms state-of-art by 215% rigging accuracy on held-out test sets. ; [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig](https://github.com/VAST-AI-Research/UniRig) (Jia-Peng Zhang, Cheng-Feng Pu, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu, 2025) — Model code and Blender integration released under MIT license; model weights hosted on Hugging Face under VAST-AI/UniRig, also MIT.

### Auto-Rig Pro — paid Blender add-on for rigging + mocap retargeting · `recommended` · · community
**Auto-Rig Pro (~$40 Blender Market) is the production standard for retargeting purchased BVH/FBX mocap onto a stylized rig, with built-in Mixamo, BVH, and custom skeleton presets.**
Auto-Rig Pro (artell, Superhive/Gumroad) provides a full auto-rigger plus a Remap (retargeting) tool that maps any source skeleton's bones to any target rig by name or manual pairing. Built-in presets cover Mixamo, traditional BVH mocap, and several commercial mocap skeletons. The Remap bakes retargeted keyframes onto the target rig's actions, which can then be pushed into the NLA Editor as strips. For the studio, the use case is: purchase a commercial mocap pack (BVH), retarget it through ARP Remap onto the studio canonical rig, clean up in the NLA, then render the 8-direction sprite sheets.
- **For the pipeline:** The missing link between purchased commercial mocap (BVH/FBX packs from sites like MoCap Online) and the studio's canonical bone hierarchy. Without ARP Remap, retargeting BVH to a custom rig is manual bone-by-bone work. The ~$40 one-time cost is a clear purchase for any mocap-heavy character. Does not conflict with Rigify — ARP can retarget onto a Rigify-generated rig.
- **Engine:** blender · **Applies to:** rigging · **Kind:** model
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: Commercial (one-time purchase, ~$40); royalty-free for use in shipped games) — ARP is a paid Blender add-on; the purchase includes a commercial-use license for shipped projects. The rendered output and retargeted animations are the buyer's IP. Do not distribute the add-on itself.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Remap (Retargeting) — AutoRigPro Documentation](https://www.lucky3d.fr/auto-rig-pro/doc/remap_doc.html) (artell, 2025) — ARP Remap retargets any armature action to another with different bone names/orientations; includes preset mappings for Mixamo, BVH, and other common mocap skeletons. ; [Refining Mocap with Mixamo and Blender AutoRig PRO — GarageFarm](https://garagefarm.net/blog/refining-motion-capture-with-mixamo-and-blender-auto-rig-pro) (GarageFarm, 2024) — Community-documented workflow showing ARP Remap as the standard path for transferring Mixamo/BVH animations to custom Blender rigs.

### Blender NLA strip + orthographic multi-camera sprite-sheet render · `recommended` · · community
**Organising all animation clips as NLA strips and rotating 8 named orthographic cameras around the rig gives a fully automated, per-action, per-direction sprite-sheet batch render from one Blender file.**
Push each action (walk, attack, idle, hurt, death) into the NLA Editor as a strip. Create 8 orthographic cameras at the 2.5D elevation angle (30-45°) rotated every 45° around the character. Use the Sprite Sheet Generator add-on (MIT, Blender Extensions) or the BlenderSpriteGenerator (MIT, GitHub) to iterate cameras × NLA strips automatically. The render script outputs PNG sequences per action per direction, ready for packing into sprite atlases. The rig's weapon_grip bones appear in every render frame — their pixel positions can be extracted for hitbox metadata.
- **For the pipeline:** This workflow makes the multi-direction render deterministic and scriptable. Once the rig and NLA library are set up, adding a new character reuses the same camera rig and render script. Integrate into the studio pipeline between the Blender rig step and the repaint/polish step.
- **Engine:** blender · **Applies to:** rigging · **Kind:** workflow
- **VRAM:** 2-8
- **Output license:** commercial **yes** (license: GPL (Blender); MIT (BlenderSpriteGenerator add-on); output unrestricted) — All components free for commercial output. Sprite sheets and atlases are the studio's own work.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Nonlinear Animation — Blender 5.1 Manual](https://docs.blender.org/manual/en/latest/editors/nla/index.html) (Blender Foundation, 2025) — The NLA Editor lets artists organize multiple animation actions as non-destructive strips, enabling batch export of all clips in a single scene file. ; [BlenderSpriteGenerator — GitHub (RubielGames)](https://github.com/RubielGames/BlenderSpriteGenerator) (RubielGames, 2025) — MIT-licensed Blender add-on that renders 3D models from multiple angles into 2D/2.5D game sprites with animation support and orthographic camera automation.

### Blender humanoid armature bone hierarchy for 2.5D sprite motion · `recommended` · · community
**A canonical root→pelvis→spine→chest→neck→head hierarchy with IK legs and FK/IK arms gives deterministic, retargetable motion for multi-angle orthographic sprite rendering.**
Build the armature from a single root bone (world-space anchor, never animated directly), then pelvis→spine (2–3 segments)→chest→neck→head. Arms branch from the chest: shoulder→upper_arm→forearm→hand. Legs: pelvis→thigh→shin→foot→toe. Add IK targets for feet (foot.IK.L/R) and optional pole targets for knees/elbows. All deform bones carry consistent naming (Blender convention:.L/.R suffix) so skinning and retargeting tools can resolve them automatically. The hierarchy ensures forward kinematics propagate top-down for global transforms while IK solvers handle contact points.
- **For the pipeline:** This bone layout is the prerequisite for every downstream step: UniRig output must be mapped to it, Mixamo/AccuRIG retargeted onto it, and the weapon_grip chain hangs off hand.R. Keeping the hierarchy stable across all character assets lets the sprite-sheet render script iterate actions without per-character camera adjustments.
- **Engine:** blender · **Applies to:** rigging · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: GPL (Blender app); rendered output unrestricted) — Blender GPL covers the application, not the artist's output. Rendered frames and exported FBX/GLTF are fully owned by the studio.
- **Fit:** rig 5/5 · studio 5/5
- **Best for:** motion-truth (-, fit -) ; retargeting-anchor (-, fit -) ; sprite-render (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Bone Positioning Guide — Blender Manual (Rigify)](https://docs.blender.org/manual/en/latest/addons/rigging/rigify/bone_positioning.html) (Blender Foundation, 2025) — Rigify metarig bone positioning guide documents the canonical humanoid hierarchy (spine, arm, leg, face) with.L/.R naming used by Blender's bundled auto-rigger. ; [Armatures — Blender Manual](https://docs.blender.org/manual/en/latest/animation/armatures/index.html) (Blender Foundation, 2025) — An armature is a skeleton of bones arranged in parent-child hierarchy; objects or mesh vertices parented/constrained to bones follow their transforms.

### ComfyUI-UniRig — ComfyUI wrapper nodes for UniRig rigging inside ComfyUI · `situational` · ▸ reproduced
**ComfyUI-UniRig (PozzettiAndrea, GPL-3.0) is a verified ComfyUI custom-node package that wraps UniRig's rigging pipeline in 16 graph nodes — including UniRig:Load Model, UniRig:Auto Rig, UniRig:Apply Animation, UniRig:Export Posed FBX, and UniRig:Save Mesh — installable via ComfyUI Manager.**
The package provides 16 nodes covering the full UniRig pipeline inside ComfyUI: load a 3D mesh, load the UniRig model, extract skeleton, apply ML skinning, apply animation, export posed FBX, preview the rigged mesh, and save the result. A parallel MIA (Make-It-Animatable, CVPR 2025) node set is also included. Installation is via ComfyUI Manager (search 'UniRig') or manual git clone. Hardware overhead is modest — 8 GB GPU handles UniRig alongside other ComfyUI workflows. The package is active (420+ commits as of research date). Output format includes FBX (UniRig:Export Posed FBX node confirmed); GLB output via UniRig:Save Mesh.
- **For the pipeline:** ComfyUI-UniRig enables a fully node-graph rigging pipeline — paste the TRELLIS.2 GLB into a ComfyUI workflow that auto-rigs via UniRig, applies a BVH animation clip, and exports a posed FBX in one shot, without leaving ComfyUI. The GPL-3.0 license on the wrapper does NOT affect the rigged output files — it covers the Python node wrapper code, not the 3D assets produced. Evaluate as an alternative to the shell-script WSL2 path for operators more comfortable in ComfyUI's visual graph.
- **Engine:** comfyui · **Applies to:** rigging · **Kind:** workflow
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: GPL-3.0 (ComfyUI wrapper nodes); MIT (UniRig model itself)) — GPL-3.0 covers the Python wrapper code, not rigged 3D asset output. Produced GLB/FBX assets are the studio's IP. Confirm GPL interpretation before redistributing the node package itself.
- **Fit:** rig 4/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| ComfyUI-UniRig still requires UniRig's Python environment (flash_attn, spconv, torch_scatter) installed in the ComfyUI Python — the Blackwell WSL2 setup complexity from the measured recipe still applies. |  |  |  |
| Output format details (FBX vs GLB per node) require per-node verification — not all nodes document their output format in the registry listing. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed] -> confirmed; not-found x1 [confirmed by 2 of 3 juror(s) [confirmed, unverified]]
- **Sources:** [PozzettiAndrea/ComfyUI-UniRig — GitHub](https://github.com/PozzettiAndrea/ComfyUI-UniRig) (PozzettiAndrea, 2025) — GPL-3.0 licensed ComfyUI custom node package; installable via ComfyUI Manager; 420+ commits, active; provides 16 nodes including UniRig:Auto Rig, UniRig:Apply Animation, UniRig:Export Posed FBX. ; [ComfyUI-UniRig node listing — runcomfy.com](https://www.runcomfy.com/comfyui-nodes/ComfyUI-UniRig) (runcomfy.com, 2025) — Lists all 16 ComfyUI-UniRig nodes by name including UniRig:Load Model, UniRig:Auto Rig, UniRig:Apply Animation, UniRig:Export Posed FBX, UniRig:Save Mesh, UniRig:Preview Rigged Mesh, and MIA:Auto Rig. ; [ComfyUI UniRig Automatic Rigging Guide 2025 — Apatero](https://www.apatero.com/blog/comfyui-unirig-automatic-skeleton-rigging-guide-2025) (Apatero, 2025) — Community guide confirms 8 GB GPU handles UniRig in ComfyUI alongside other workflows; ComfyUI Manager install path verified.

### Godot 4 Skeleton2D / Bone2D runtime cutout puppet (Blender = authoring) · `situational` · ▸ reproduced
**Godot 4's Skeleton2D / Bone2D system enables runtime deformation of 2D sprite pieces — a lighter alternative to full pre-rendered sprite sheets — with Blender used only for motion authoring, not final render.**
In Godot 4, create a Skeleton2D node with Bone2D children forming the character hierarchy (hip→spine→chest→head, arms, legs). Assign Polygon2D nodes to each sprite piece and weight-paint their vertices to the nearest bones. Animate only the Skeleton2D bones in Godot's AnimationPlayer — the polygon deforms automatically. This approach avoids storing hundreds of pre-rendered PNGs and supports smooth interpolation at runtime. Best for supporting cast or enemies where per-pixel painterly quality is not required. Hero characters should still use the full Blender→repaint→sprite-sheet path for maximum visual fidelity.
- **For the pipeline:** Use Skeleton2D for quantity (large enemy rosters, background characters) and the Blender sprite-sheet path for hero-tier characters. The two approaches can coexist in the same Godot project. Godot MIT license — no commercial restrictions on shipped games.
- **Engine:** custom · **Applies to:** rigging · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: MIT (Godot Engine)) — Godot Engine is MIT-licensed. Shipped games have no royalties or restrictions. Sprite artwork assets are the studio's own IP.
- **Fit:** rig 3/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Skeleton2D / polygon deformation does not achieve painterly per-pixel detail — acceptable for supporting cast, not for hero 2.5D quality. |  |  |  |
| Weapon parenting in Skeleton2D is possible (Bone2D child node) but rigid-prop consistency must be enforced by code, not physics. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [2D skeletons — Godot Engine (stable) documentation](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html) (Godot Foundation, 2025) — Skeleton2D and Bone2D enable skeletal deformation of 2D polygon sprites in Godot 4; animating the bones (not the polygons) produces mesh deformation for cutout-style characters. ; [Skeleton2D class — Godot Engine API (stable)](https://docs.godotengine.org/en/stable/classes/class_skeleton2d.html) (Godot Foundation, 2025) — Skeleton2D is the Godot 4 node that manages a hierarchy of Bone2D nodes, providing 2D skeletal deformation for sprite-based characters.

### Mixamo auto-rigger + animation library (Adobe, royalty-free commercial) · `situational` · ▸ reproduced
**Mixamo auto-rigs humanoid meshes in the cloud and provides a royalty-free library of 3,000+ FBX animations usable in commercial games without attribution.**
Upload a humanoid mesh to mixamo.com; the AutoRigger (ML-based) detects limb positions and inserts a humanoid skeleton with skinning weights. Download as FBX with any or all animations. Animations and rigged meshes are royalty-free for personal and commercial projects including shipping games. Key restriction: raw Mixamo files cannot be redistributed as standalone assets — they must be embedded in a project or game. No attribution required. Blender Mixamo add-on (Adobe) imports FBX with retargeted actions. Bipedal humanoids only — no quadrupeds, no weapons auto-rigged.
- **For the pipeline:** Fastest path to a rigged humanoid for early motion tests. The Mixamo skeleton is not identical to the studio's canonical hierarchy, so retargeting via Auto-Rig Pro Remap is needed before final sprite renders. Weapon bones must be added post-import in Blender. Do not redistribute Mixamo FBX files as open source.
- **Engine:** custom · **Applies to:** rigging · **Kind:** service
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: Proprietary (Adobe Creative Cloud); royalty-free for incorporated use) — Adobe FAQ explicitly states characters and animations are royalty-free for commercial projects including video games. Raw file redistribution (as standalone assets) is prohibited by EULA.
- **Fit:** rig 3/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Bipedal humanoids only — no custom or non-human body plans. |  |  |  |
| Weapon / prop bones must be added manually in Blender after import. |  |  |  |
| Raw FBX redistribution prohibited — embed into the game build only. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Mixamo FAQ — Creative Cloud](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) (Adobe, 2025) — Mixamo characters and animations are royalty-free for personal and commercial use including video games; raw redistribution of Mixamo files as standalone assets is prohibited.

### UniRig Blender VRM addon — VRM import/export for rigged mesh handoff · `situational` · ▸ reproduced
**UniRig ships a modified VRM-Addon-for-Blender (add-on-vrm-v2.20.77_modified.zip) that installs into Blender via one Python command and enables.vrm import/export — useful only for VRM-format input meshes; the primary studio path (TRELLIS.2 GLB in, rigged GLB out) does not require the addon.**
The addon is installed with: `python -c "import bpy, os; bpy.ops.preferences.addon_install(filepath=os.path.abspath('blender/add-on-vrm-v2.20.77_modified.zip'))"`. It is a fork of the open-source VRM-Addon-for-Blender and adds.vrm import/export capability to Blender for use with UniRig's VRM input path. UniRig accepts.obj,.fbx,.glb, and.vrm — so the addon is only required when the source mesh is a VRM file (e.g. a VRoid character). For the studio's TRELLIS.2 GLB input pipeline, the addon is not needed: generate_skeleton.sh and merge.sh consume and produce GLB/FBX natively via UniRig's own Python environment.
- **For the pipeline:** Skip the Blender addon for the standard TRELLIS.2 → rigged GLB path. Reserve it for any VRoid or VRM-sourced character mesh. Do not conflate 'Blender addon' with 'Blender integration' — UniRig's Blender interaction is primarily through importing the rigged GLB output into Blender manually, not through a live Blender addon interface.
- **Engine:** blender · **Applies to:** rigging · **Kind:** technique
- **VRAM:** n/a
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT (UniRig repo, which includes the addon); original VRM-Addon-for-Blender is MIT) — MIT license; addon covers VRM file handling only, output is unrestricted.
- **Fit:** rig 2/5 · studio 1/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| The addon enables VRM I/O only — it does not expose a UniRig 'rig this mesh' button inside Blender. UniRig rigging still runs as Python shell commands outside Blender. |  |  |  |
| VRM is a humanoid-avatar format (VRChat, VRoid). TRELLIS.2 outputs GLB, not VRM — the addon adds no value for the standard studio path. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, unverified]]
- **Sources:** [VAST-AI-Research/UniRig — Blender addon install command](https://github.com/VAST-AI-Research/UniRig) (VAST AI Research, 2025) — README documents the Python install command for add-on-vrm-v2.20.77_modified.zip; identifies it as modified from VRM-Addon-for-Blender; input formats listed as.obj,.fbx,.glb,.vrm.

### UniRig on non-humanoid / exotic meshes — decisive advantage, honest quality ceiling · `recommended` · · community
**UniRig is the only MIT-licensed auto-rigger that can produce a skeleton and skinning for arbitrary/non-humanoid topology (tortle, kenku, sahuagin, minotaur) without hand-placing bones — but the output is an 80-90% draft requiring cleanup on tails, wings, digitigrade legs, and joint skin weights.**
UniRig's Skeleton Tree Tokenization predicts bone placement from geometry rather than a fixed template, giving it a decisive advantage on the studio's 15 exotic species. The Rig-XL training set covers 8 non-humanoid categories (Quadruped, Bird & Flyer, Insect & Arachnid, Water Creature) but human-related categories are overrepresented in source data, so sampling probability adjustments were applied during training — meaning non-humanoid results are good but not as reliable as humanoid results. Community reports confirm missing or mis-placed bones on tails (squirrel/dragon tails), turtle limbs, and misaligned joints on hands. The paper's own supplemental notes that skin weights 'degrade significantly if the skeleton is inaccurate' and recommends skeleton refinement before running the skin stage. Treat UniRig output as a strong first-pass draft, not a hands-off production rig.
- **For the pipeline:** For the studio's exotic-species roster, UniRig is still the correct tool — no template-based alternative can handle a tortle, kenku, or sahuagin at all. Build a skeleton-cleanup pass into every non-humanoid character budget: fix tail and wing bone chains, verify digitigrade leg alignment, then re-run the skin stage with the corrected skeleton before hand-editing weights. Hero characters with unusual proportions may need more cleanup time than biped supporting cast.
- **Engine:** blender · **Applies to:** rigging · **Kind:** technique
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT) — MIT; cleanup is artist time only, no license constraint.
- **Fit:** rig 5/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Missing bone chains on tails and wings | Autoregressive skeleton predictor prematurely emits the termination token, cutting chain short — documented failure mode in Auto-Connect (CVPR 2026) paper analyzing UniRig's architecture | After skeleton generation, open the predicted skeleton in Blender, manually extend the tail/wing bone chain to the tip, then re-run generate_skin.sh with the corrected skeleton JSON | summary |
| Spatial gap / discontinuity between bone chains | UniRig uses heuristic distance-threshold rules to merge chain endpoints — non-end-to-end design produces compounding error when chains are far apart (e.g., wings far from spine root) | Manually connect disconnected chains in Blender Pose Mode before skinning; the merge gap is typically visible as a floating chain with no parent | summary |
| Mis-placed bones on turtle limbs and quadruped extremities | Explicitly documented in UniRig supplemental and confirmed in Auto-Connect paper: 'missing bones on turtle limbs and squirrel tail and misaligned skeletons on human hands' | Skeleton edit pass in Blender; move individual bone heads/tails to correct anatomical positions before skin stage | summary |
| Skinning artifacts (stretching / tearing at deforming joints) | Skin quality is downstream of skeleton accuracy; any skeleton error compounds into bad weight assignments. Overlapping geometry (wings over body, tails between legs) produces phantom bone targets. | Weight paint touch-up in Blender after skin stage; focus on hips/shoulder junction, joint interiors, and any overlapping mesh region | summary |
| Incomplete skeletons on heavily stylized / chibi proportions | Training distribution skewed toward realistic proportions; extreme stylization departs from learned geometry-to-bone mapping | Use Blender automatic weights as a fallback for extreme stylized meshes; or manually place bones and use UniRig only for skinning stage | summary |

- **Best for:** exotic-species-rig (-, fit -) ; non-humanoid-auto-rig (-, fit -) ; cleanup-guide (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, unverified]]
- **Sources:** [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig](https://arxiv.org/html/2504.12451v1) (Wang, Lingteng et al. (Tsinghua University / VAST AI Research), 2025) — Rig-XL dataset covers 8 non-humanoid categories; human-related categories remain overrepresented in source data requiring sampling probability adjustments; UniRig recommends skeleton refinement before skinning because skin quality degrades significantly with inaccurate skeletons. ; [Auto-Connect: Connectivity-Preserving RigFormer with Direct Preference Optimization](https://arxiv.org/html/2506.11430) (Auto-Connect authors (CVPR 2026 submission), 2026) — Explicitly identifies UniRig failure modes: premature termination token (missing bone chains), spatial discontinuity between chains (initialization barriers), and non-end-to-end heuristic merging causing compounding errors. Documents 'missing bones on turtle limbs and squirrel tail and misaligned skeletons on human hands' as concrete examples. ; [VAST-AI-Research/UniRig — README](https://github.com/VAST-AI-Research/UniRig) (VAST AI Research, 2025) — README states 'results may degrade significantly if the skeleton is inaccurate' and recommends skeleton refinement before skinning; notes training distribution includes Quadruped, Bird & Flyer, Insect & Arachnid, Water Creature categories. ; [ComfyUI UniRig Automatic Rigging Guide 2025 — Apatero](https://www.apatero.com/blog/comfyui-unirig-automatic-skeleton-rigging-guide-2025) (Apatero, 2025) — Community guide documents practical failure modes: 'non-humanoid designs (animals, robots, monsters)' and 'extreme stylization' require significant manual adjustment; overlapping elements create phantom bones.

### UniRig paper benchmarks — what the numbers mean and what they do not cover · `situational` · ▸ reproduced
**UniRig's 215% rigging accuracy / 194% motion accuracy benchmark improvements are real and verified against prior art, but the evaluation datasets (VRoid anime + Rig-XL Objaverse) do not include stylized JRPG creature meshes from image-to-3D generators — studio results will differ from paper numbers.**
The paper evaluates on VRoid (2,061 anime humanoid meshes from VRoidHub, standardized skeleton with spring bones) and Rig-XL (14,611 Objaverse-XL models including Quadruped/Bird/Insect/Water Creature categories). Metrics are Chamfer Distance joint-to-joint, joint-to-bone, bone-to-bone (lower is better) and IoU (higher is better). UniRig outperforms prior methods by large margins on these datasets. However, none of the evaluation meshes are TRELLIS-generated images-to-3D outputs (which have characteristic topology artifacts and dense vertex counts), and VRoid anime meshes differ significantly from painterly JRPG creature designs. The Auto-Connect follow-up (arXiv:2506.11430) shows that even on a new Art-XL2.0 dataset, UniRig CD-J2J degrades to 3.232% vs Auto-Connect's 2.572% — a 20% gap the paper does not mention. Take the 215% headline as valid proof of superiority over prior art, not as a guarantee for arbitrary creature meshes.
- **For the pipeline:** The benchmark gap between VRoid/Rig-XL and TRELLIS creature meshes means studio testing is the only way to know actual quality for a given species. Prioritize measured-on-rig data over paper claims when deciding whether a skeleton needs cleanup. The Auto-Connect paper's Art-XL2.0 results suggest UniRig is 80% as accurate as the best current alternative on out-of-distribution meshes.
- **Engine:** blender · **Applies to:** rigging · **Kind:** reference
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **unknown** (license: MIT) — MIT; benchmark discussion is informational only.
- **License correction (verifier):** The paper is not MIT-licensed; the recipe's license claim is inaccurate. The benchmark information itself is freely available but not under an MIT license.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=unverified minimax-m3=confirmed-with-fixes] -> confirmed [license -> commercial_use=unknown] [confirmed by 2 of 3 juror(s) [confirmed-with-fixes, unverified]]
- **Sources:** [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig](https://arxiv.org/abs/2504.12451) (Wang, Lingteng et al. (Tsinghua University / VAST AI Research), 2025) — Evaluated on VRoid (anime humanoid, 2061 models) and Rig-XL (14611 diverse models, 8 categories); reports 215% rigging accuracy and 194% motion accuracy improvement over prior art. Tokenization reduces token count 27-30% vs naive approaches on both datasets. ; [Auto-Connect: Connectivity-Preserving RigFormer with Direct Preference Optimization](https://arxiv.org/html/2506.11430) (Auto-Connect authors, 2026) — On Art-XL2.0 dataset, UniRig achieves CD-J2J 3.232%, CD-J2B 2.540%, CD-B2B 2.124%, IoU 75.571% vs Auto-Connect's CD-J2J 2.572%, IoU 82.806% — a ~20% gap across all metrics, showing UniRig is strong but not the absolute ceiling.

### UniRig skeleton cleanup workflow — the manual pass every non-humanoid needs · `recommended` · · community
**Every UniRig skeleton for non-humanoid / exotic meshes requires a Blender skeleton-edit pass before the skin stage: extend missing tail/wing chains, re-parent disconnected bones, verify roll axes, then re-run generate_skin.sh with the corrected skeleton JSON.**
After generate_skeleton.sh produces the predicted skeleton, import it into Blender (the merge.sh output or the intermediate JSON) and inspect in Pose Mode. Common fixes for exotic species: (1) tail chains — manually add missing tail bones to the tip, parenting each to the last predicted tail bone; (2) wing chains — connect floating wing chain to the predicted shoulder bone; (3) digitigrade legs (kenku, sahuagin) — verify the hock/ankle joint exists as a distinct bone, not merged with the toe; (4) re-roll all bones so the Y-axis points along the bone and X-axis points toward the character's right (use Recalculate Roll → Global -Z Axis in Blender). Once the skeleton JSON is corrected, pass it to generate_skin.sh explicitly to avoid re-predicting the skeleton. The skin stage produces noticeably better weights on a clean skeleton than on the predicted-only version.
- **For the pipeline:** Budget one Blender cleanup session per exotic species character — approximately 30-60 minutes for a thorough skeleton edit and spot weight-paint fix. This is the irreducible human cost of auto-rigging non-humanoid topology. The studio's 15 exotic species characters should each have a documented cleanup checklist stored with their Blender file so the cleanup is reproducible across character variants.
- **Engine:** blender · **Applies to:** rigging · **Kind:** technique
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: GPL (Blender); MIT (UniRig)) — All cleanup work is in Blender; rigged output is studio IP.
- **Fit:** rig 4/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Re-running generate_skin.sh after skeleton edit still uses old predicted skeleton | generate_skin.sh may cache or re-predict if the skeleton input path is not explicitly overridden | Pass the corrected skeleton JSON path explicitly as an argument; check shell script arguments before running | summary |
| Weight paint seam at tail base / wing root after skin stage | Manually added bones were not present during skinning or have incorrect roll causing weight assignment to wrong bone | Use Blender Weight Paint mode on the problematic region; normalize weights after manual paint | summary |

- **Best for:** exotic-species-rig (-, fit -) ; non-humanoid-cleanup (-, fit -) ; skinning (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, unverified]]
- **Sources:** [VAST-AI-Research/UniRig — README: skeleton refinement recommendation](https://github.com/VAST-AI-Research/UniRig) (VAST AI Research, 2025) — README explicitly recommends skeleton refinement before skinning because results degrade significantly with inaccurate skeletons. ; [Auto-Connect: Connectivity-Preserving RigFormer with Direct Preference Optimization](https://arxiv.org/html/2506.11430) (Auto-Connect authors, 2026) — Documents the specific UniRig gap: heuristic post-hoc chain merging (distance threshold) is the root cause of connectivity errors requiring manual repair. ; [Armatures — Blender Manual (Edit Mode / Roll)](https://docs.blender.org/manual/en/latest/animation/armatures/index.html) (Blender Foundation, 2025) — Blender Pose Mode and Armature Edit Mode provide bone manipulation (parent, roll, head/tail position) for correcting predicted skeletons before skinning.

### UniRig skeleton → mocap retarget: non-standard bone-name remap via ARP Remap or Blender Retarget addon · `recommended` · · community
**UniRig generates skeletons with non-standardized bone names (inherited from training data diversity, not aligned to Mixamo/Blender/UE5 conventions); a manual bone-name remap pass — via Auto-Rig Pro Remap's 'Replace Namespace' feature or the Blender Retarget addon presets — is required before any commercial mocap BVH/FBX can retarget onto a UniRig skeleton.**
UniRig's autoregressive skeleton predictor outputs bone names derived from its Rig-XL training corpus, which contains diverse rigging conventions. These names do not match Mixamo's 'mixamorig:Hips' scheme, Blender's '.L/.R' convention, 100STYLE's BVH names, or CMU Mocap Database joint names. To retarget commercial BVH/FBX mocap onto a UniRig skeleton in Blender, build a custom bone-name mapping JSON (ARP Batch Retargeting workflow: github.com/Shimingyi/ARP-Batch-Retargeting) or use ARP Remap's interactive bone-pair UI with Replace Namespace to handle name prefix differences. The Blender Retarget addon (extensions.blender.org) also provides interactive source-to-target bone pairing. Build and save a per-species preset — reuse across all characters of the same UniRig topology. This remap is a one-time setup cost per species skeleton family.
- **For the pipeline:** The wave-2 mocap retarget lane uses UniRig skeletons as the target rig — but UniRig gives no naming guarantee. Budget one remap-preset authoring session per species family (humanoid, tortle, kenku, sahuagin, etc.) before the mocap retarget wave begins. Store each remap preset as a.blend template. This is the key integration seam between UniRig (wave-4) and the retarget lane (wave-2).
- **Engine:** blender · **Applies to:** rigging · **Kind:** workflow
- **VRAM:** n/a
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: Blender Retarget addon: free (Blender Extensions); ARP Remap: paid (~$40); technique itself: free) — The remap/retarget step does not launder the source mocap clip license — verify commercial-use rights on the mocap clip itself (see mocap-datasets and motion-licensing lanes).
- **Fit:** rig 4/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Skipping the remap step and running ARP Remap with a Mixamo preset on a UniRig skeleton will fail silently — most bones will be unmapped, resulting in a frozen rig with only root motion. |  |  |  |
| UniRig bone count varies by mesh complexity — exotic species may get fewer or more predicted bones than humanoids, making a generic remap preset unusable across species. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Remap — AutoRigPro Documentation (Replace Namespace)](https://www.lucky3d.fr/auto-rig-pro/doc/remap_doc.html) (artell, 2025) — Documents the Replace Namespace function for handling bone-name prefix differences when preset names don't match source names (e.g. 'mixamorig:Hips' vs 'matthew:Hips'); applicable to UniRig's non-standard names. ; [ARP-Batch-Retargeting — GitHub (Shimingyi)](https://github.com/Shimingyi/ARP-Batch-Retargeting) (Shimingyi, 2024) — JSON-based bone mapping pipeline for batch BVH retargeting via ARP; demonstrates 100STYLE_to_Mixamo and SMPL_to_Mixamo mappings — the same JSON approach works for UniRig-to-Mixamo bone name mapping. ; [Retarget — Blender Extensions](https://extensions.blender.org/add-ons/retarget/) (Blender Foundation community, 2025) — Free Blender Extension with presets for Mixamo, Unreal, VRoid, MMD, Daz, Auto Rig Pro — includes interactive source-to-target bone pairing for custom skeletons like UniRig output.

### UniRig training data (Articulation-XL2.0 / Objaverse-XL): license propagation analysis · `situational` · ▸ reproduced
**The current released checkpoint was trained on Articulation-XL2.0 (CC-BY-4.0, Seed3D/HuggingFace), which is itself derived from Objaverse-XL (ODC-By 1.0 for the collection; individual objects carry mixed licenses including some CC-BY-NC). However, training-data licenses do not automatically propagate to model weights or to the rig outputs produced by running the model — outputs are the user's own 3D data, not reproductions of training assets.**
Articulation-XL2.0 is published on HuggingFace under CC-BY-4.0, which permits commercial use with attribution. It is sourced from the GitHub and Sketchfab subsets of Objaverse-XL; those subsets contain some CC-BY-NC objects. The Objaverse-XL collection itself is ODC-By 1.0 (permissive for the database as a whole). The core legal question — whether NC training data infects model weights or outputs — is unsettled law as of 2026, but the prevailing practical position (per AI-law commentary and VAST-AI's own MIT weight license) is that running an inference call does not make the rig output a derivative work of the training asset. VAST-AI publishing the weights under MIT is their implicit commercial-use grant. The studio's actual risk exposure from the training-data layer is low but non-zero and should be noted for due-diligence purposes.
- **For the pipeline:** For a commercial JRPG Steam release, treat the training-data layer as a due-diligence footnote rather than a blocker: the tool license is MIT, the weights are MIT, and rig outputs are the studio's own asset data. If a future legal challenge on NC-training-data propagation ever crystallized, it would affect VAST-AI (as the trainer) rather than studio users running inference. Attribution of Articulation-XL2.0 (Seed3D) is not required for rig outputs — only for redistribution of the dataset itself.
- **Engine:** n/a · **Applies to:** rigging · **Kind:** reference
- **VRAM:** n/a
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **conditional** (license: Articulation-XL2.0: CC-BY-4.0; Objaverse-XL: ODC-By 1.0 (collection); individual objects: mixed) — Dataset licenses apply to redistribution of the training data itself, not to model inference outputs. The conditional rating reflects legal uncertainty about NC-training-data propagation, not a practical blocker. VAST-AI publishing weights under MIT is the operative commercial grant for studio use. No attribution of training data is required when shipping a game that uses UniRig-rigged assets.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=unverified] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, unverified]]
- **Sources:** [Seed3D/Articulation-XL2.0 — Hugging Face dataset card](https://huggingface.co/datasets/Seed3D/Articulation-XL2.0) (Seed3D / VAST-AI, 2025) — Articulation-XL2.0 license field is CC-BY-4.0. Commercial use is permitted; attribution to dataset creators is required when redistributing the dataset itself. ; [allenai/objaverse-xl — Hugging Face dataset card](https://huggingface.co/datasets/allenai/objaverse-xl) (Allen AI, 2023) — Objaverse-XL collection is ODC-By 1.0. Individual objects have heterogeneous licenses including CC-BY, CC-BY-NC, CC-BY-SA, CC0. Some subsets (Polycam) are non-commercial academic-only. ; [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig](https://arxiv.org/abs/2504.12451) (Zhang, Pu, Guo, Cao, Hu (Tsinghua + VAST-AI), 2025) — Paper states training on Rig-XL (14,000+ rigged models from Objaverse-XL) and Articulation-XL2.0. Current released checkpoint is trained on Articulation-XL2.0.

### AccuRIG 2 — Reallusion free auto-rigger with ActorCore motion library · `runner-up` · · community
**AccuRIG 2 is a free standalone auto-rigger that places a production-quality humanoid skeleton, exports FBX/USD, and plugs into Blender, UE5, and Godot with DCC presets.**
AccuRIG 2 (free, requires free ActorCore account) detects body landmarks and generates a humanoid control rig with twist bones, face bones, and finger chains. Export presets for Blender, Cinema 4D, Maya, Unreal Engine, Unity, MotionBuilder, and Godot are built in. Version 2 (released 2025) adds direct access to ActorCore's 4,500+ production-ready animations (free and premium tiers) for preview and apply. AccuRIG itself has no commercial restriction — it is free software. Premium ActorCore animations carry per-animation licensing. Output FBX is your own work.
- **For the pipeline:** Strong alternative to Mixamo for the rig-fast→retarget→append-weapon-grip path. The Blender DCC preset aligns bone orientations for one-click FBX import. More anatomy detail than Mixamo (twist bones help forearm rotation in sprite frames). Still humanoid-only; weapon bones must be appended in Blender.
- **Engine:** custom · **Applies to:** rigging · **Kind:** service
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: Proprietary freeware (AccuRIG software); ActorCore animation assets have per-item licensing) — AccuRIG software is free with no stated commercial restrictions. Output rigs and renders are the studio's IP. Premium ActorCore animation assets require per-asset license review before commercial use.
- **Fit:** rig 4/5 · studio 3/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [AccuRIG 2 vs Mixamo: Smarter Auto-Rigging for 3D Animators — Reallusion Magazine](https://magazine.reallusion.com/2025/07/30/accurig-2-vs-mixamo-smarter-auto-rigging-for-3d-animators/) (Reallusion, 2025) — AccuRIG 2 is free auto-rigging software with no licensing fees; it supports commercial output and exports FBX/USD with DCC-friendly presets for Blender, Unreal Engine, Unity, and Godot. ; [Free Auto Rig for any 3D Character — ActorCore](https://actorcore.reallusion.com/auto-rig) (Reallusion, 2025) — AccuRIG is described as free software requiring only a free ActorCore account, with no extra fees or surprise licensing.

### DQS/LBS + Unity Avatar auto-rig limits hold · `situational` · docs
**LBS candy-wrap vs DQS; Humanoid Avatar auto-map fails without T-pose — hold auto-rig limits**
STUDY-037 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0; flips 33/117/486: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT — do not invent-verify 33/117/486. [no external verdict — not checked]
- **Sources:** [Geometric skinning DQS](https://users.cs.utah.edu/~ladislav/kavan08geometric/kavan08geometric.html) — LBS volume loss; dual-quaternion better. ; [Unity Configuring the Avatar](https://docs.unity3d.com/Manual/ConfiguringtheAvatar.html) — Auto-map needs T-pose / required bones.

### HumanRig learned automatic humanoid rigging (Chu et al. 2024) · `situational` · paper
**Learned automatic humanoid rigging on large dataset — auto-rig deepen**
STUDY-037 Scholar deepen.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0; flips 33/117/486: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT — do not invent-verify 33/117/486. [no external verdict — not checked]
- **Sources:** [HumanRig](https://arxiv.org/abs/2412.02317) — Automatic rigging for humanoid characters.

### Neural Blend Shapes skeletal articulations (Li et al. 2021) · `situational` · paper
**Neural blend shapes beyond naive LBS candy-wrapper — plate-armor rigidity craft**
STUDY-037 Scholar deepen.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** comfy · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0; flips 33/117/486: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT — do not invent-verify 33/117/486. [no external verdict — not checked]
- **Sources:** [Neural Blend Shapes](https://arxiv.org/abs/2105.02451) — Skeletal articulations with neural blend shapes.

### Spiritus — mesh-skeleton binding + MDM · `situational` · paper
**End-to-end 2D character tool: text to layered character, mesh-skeleton binding, BVH mapping, MDM for reusable 2D animation.**
End-to-end 2D character tool: text to layered character, mesh-skeleton binding, BVH mapping, MDM for reusable 2D animation.
- **For the pipeline:** STUDY-006 Verifier-verified. Spine: motion truth → polish → sheet → verify.
- **Engine:** comfy · **Applies to:** all-motion · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-016 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-016 from STUDY-006 Verifier ✅; default verified=0 [no external verdict — not checked]
- **Sources:** [Spiritus — mesh-skeleton binding + MDM](https://arxiv.org/abs/2503.09127) — End-to-end 2D character tool: text to layered character, mesh-skeleton binding, BVH mapping, MDM for reusable 2D animation.

### UniRig + Blender cleanup/armature parent peers · `situational` · docs
**UniRig auto-rig ≥8GB + Blender cleanup/deform parent — mesh-prep peers; auto-rig alone does not invent-verify.**
STUDY-037 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-037 Verifier ✅.
- **Engine:** blender · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-037 leftover craft deepen; verified=0; flips 33/117/486: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-037 deepen; empty ACCEPT — do not invent-verify 33/117/486. [no external verdict — not checked]
- **Sources:** [UniRig README](https://github.com/VAST-AI-Research/UniRig) — Skeleton GPT + bone-point skinning; FBX out. ; [Blender Clean Up](https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/cleanup.html) — Decimate / dissolve / merge cleanup. ; [Armature Deform Parent](https://docs.blender.org/manual/en/latest/animation/armatures/skinning/parenting.html) — Empty Groups / Automatic Weights parenting.

### UniRig license watch: MIT is not guaranteed for future weight releases · `situational` · · community
**The current VAST-AI/UniRig HuggingFace checkpoint is MIT-licensed, but VAST-AI is under no legal obligation to maintain MIT on future checkpoints. The GitHub README explicitly notes that Rig-XL-trained checkpoints (the main-paper results) are 'planned for future release' — those may carry different terms. Studios must verify the HF card license field for every new checkpoint before integrating into a commercial pipeline.**
The current released checkpoint is MIT; the upcoming Rig-XL checkpoint is 'planned for future release' per the README and may carry different terms. MIT is not contractually guaranteed for future releases. Always check huggingface.co/VAST-AI/UniRig license field before pulling a new checkpoint tag into the production pipeline. If a future checkpoint ships under a restricted license, the studio's mitigation is to pin the MIT-licensed checkpoint version hash and continue using it — MIT is irrevocable once granted.
- **For the pipeline:** Pin the current checkpoint by HuggingFace commit hash (not just 'main' or 'latest') in the studio pipeline's requirements/config. When a new checkpoint ships, verify the HF card license before pulling. If VAST-AI ever moves to NC or commercial terms, the pinned MIT checkpoint remains usable indefinitely under its original grant. Add a brief license-check step to the quarterly pipeline maintenance checklist.
- **Engine:** n/a · **Applies to:** rigging · **Kind:** reference
- **VRAM:** n/a
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: MIT (current checkpoint only — future checkpoints unconfirmed)) — MIT grant is irrevocable — once granted for a given artifact, it cannot be retroactively restricted. Pin the checkpoint by hash. Future checkpoints should be assumed unverified until the HF card license field is confirmed. Rig-XL checkpoint (unreleased as of research date) license is unknown.
- **Fit:** rig 4/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| If the studio pulls 'latest' checkpoint without checking the license field and VAST-AI has updated to NC terms, the pipeline would unknowingly ingest a restricted model. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [VAST-AI-Research/UniRig — README (checkpoint status)](https://github.com/VAST-AI-Research/UniRig) (VAST-AI-Research, 2025) — README states: checkpoints trained on Rig-XL/VRoid replicating main paper results are planned for future release. Current released checkpoint is trained on Articulation-XL2.0. ; [VAST-AI/UniRig — Hugging Face model card](https://huggingface.co/VAST-AI/UniRig) (VAST-AI, 2025) — Current checkpoint license field is MIT. Future checkpoint license fields must be verified independently.

### UniRig vs Rigify vs AccuRIG vs Auto-Rig Pro vs Mixamo vs Blender automatic weights — head-to-head · `situational` · · community
**UniRig wins decisively for arbitrary/non-humanoid topology and MIT redistribution; template-based riggers (Rigify, AccuRIG, Mixamo, Auto-Rig Pro) win for humanoid characters when the skeleton must match a specific convention or when cleaner default weights are needed without a cleanup pass.**
Six tools compared on four axes: non-humanoid support, skeleton convention match, output license, and workflow integration. Rigify (Blender-bundled, GPL) generates a production-quality control rig from a positioned metarig — it includes quadruped, bird, wolf, horse, and shark templates, but exotic/novel body plans (tortle, kenku, minotaur, sahuagin) require building a 'Frankenstein' rig from modules, which is expert work. AccuRIG 2 (Reallusion, free) is primarily humanoid but claims beastman / minotaur / bird support via manual joint layout adjustment — non-humanoid results require more manual configuration than UniRig. Auto-Rig Pro (paid, ~$40) has the best non-humanoid Blender support among template riggers: Multi-Ped mode for quadrupeds, IK Spline for long necks, digitigrade leg types for dog/cat/T-Rex — but still requires marker placement and correct template selection, meaning it cannot auto-detect a novel species the way UniRig can. Mixamo (Adobe, free, cloud) is humanoid-only with no exceptions; it cannot rig any of the 15 studio exotic species, and its EULA prohibits standalone file redistribution. Blender automatic weights is not an auto-rigger — it only assigns skin weights given a manually placed armature, and is the fallback when UniRig's skeleton prediction fails (or when flash_attn is unavailable). UniRig wins on: arbitrary body plan, zero manual bone placement, MIT redistribution, and consistent pipeline integration. Template riggers win on: clean default weights for humanoid characters, animator-friendly control rigs (IK/FK switch, stretch), and no cleanup needed for supported body types.
- **For the pipeline:** Studio decision tree: (1) Is the character one of the 15 exotic species (non-humanoid body plan)? → UniRig first pass + cleanup. (2) Is it a biped humanoid hero character that will be hand-animated with an animator-friendly rig? → Rigify or Auto-Rig Pro for cleaner control rig, retarget mocap with ARP Remap. (3) Is it a humanoid supporting cast needing quick mocap retarget only? → AccuRIG or Mixamo for speed. (4) Does the output need to be redistributed as MIT-licensed assets? → Never Mixamo; UniRig or Rigify only.
- **Engine:** blender · **Applies to:** rigging · **Kind:** reference
- **VRAM:** n/a
- **Output license:** commercial **conditional** (license: varies per tool — see commercial_notes) — UniRig: MIT (yes). Rigify: GPL (yes, output unrestricted). AccuRIG: proprietary freeware (yes, no stated commercial restriction). Auto-Rig Pro: commercial license ~$40 (yes, ships in projects). Mixamo: Adobe EULA — commercial use yes but standalone redistribution prohibited. Blender automatic weights: GPL (yes, output unrestricted).
- **Fit:** rig 5/5 · studio 5/5
- **Best for:** exotic-species-rig (-, fit -) ; tool-selection (-, fit -) ; comparison (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [One Model to Rig Them All: Diverse Skeleton Rigging with UniRig](https://arxiv.org/abs/2504.12451) (Wang, Lingteng et al. (Tsinghua University / VAST AI Research), 2025) — UniRig outperforms academic and commercial baselines on diverse mesh categories without template selection; geometry-based prediction handles arbitrary body plans. ; [Rigify Human/Quadruped Meta-Rigs — CGDive Tutorial Series](https://cgdive.com/rig-anything-with-rigify-chapter-3-the-prebuilt-metarigs-human-and-quadruped/) (CGDive, 2025) — Rigify includes prebuilt metarigs for Wolf, Cat, Horse, Bird, Shark — novel creatures (Dragon, Spider, Tortle) require expert 'Frankenstein' rig assembly from individual bone modules. ; [AccuRIG 2 vs Mixamo: Smarter Auto-Rigging — The Morphic Studio](https://www.themorphicstudio.com/accurig-2-vs-mixamo-smarter-auto-rigging/) (The Morphic Studio, 2025) — AccuRIG 2 supports some non-humanoid characters (beastmen, minotaur, bird) with manual configuration; Mixamo is strictly humanoid-only and its limitations for non-standard body types have led professionals to seek alternatives. ; [Auto-Rig Pro — Documentation: Creature / Multi-Ped rigging](https://www.lucky3d.fr/auto-rig-pro/doc/auto_rig.html) (artell, 2025) — Auto-Rig Pro includes Multi-Ped type for quadrupeds, digitigrade 3-bone IK for dog/cat/T-rex, and IK Spline spine for long-neck creatures — best template-based non-humanoid support in Blender. ; [Mixamo FAQ — Creative Cloud](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) (Adobe, 2025) — Mixamo auto-rigger and animation library is for bipedal humanoids only; characters cannot be redistributed as standalone assets. ; [Armature Deform Parent — Blender Manual (Automatic Weights)](https://docs.blender.org/manual/en/latest/animation/armatures/skinning/parenting.html) (Blender Foundation, 2025) — Blender Automatic Weights assigns per-vertex bone influence given an existing armature; it is a skinning tool, not a skeleton predictor — requires manually placed bones as input.

### SkinTokens — VAST-AI UniRig successor (arXiv Feb 2026, MIT) · `avoid` · · single-run
**SkinTokens (VAST-AI, arXiv 2602.04805, February 2026) is the verified MIT-licensed successor to UniRig that unifies skeleton prediction and skinning into a single autoregressive token sequence (SkinTokens), reporting 98-133% skinning accuracy improvement and 17-22% bone prediction improvement over UniRig; code and model weights are available on GitHub as of May 2026.**
Where UniRig runs two sequential stages (skeleton prediction → skin weight prediction), SkinTokens represents both skeleton joints and skinning weights as a single unified discrete token sequence, predicted autoregressively. The SkinTokens representation is the key innovation: learned discrete tokens replace the per-vertex skinning weight matrices of UniRig, enabling the entire rig to be generated in one forward pass. Input is a 3D mesh GLB; output is a rigged GLB. MIT license confirmed in the GitHub repo. The Hugging Face Space demo is live. Code last updated May 12, 2026 per GitHub. No Blender addon is documented for SkinTokens; the workaround for Blender import is to 'remove the glTF_not_exported node when importing results into Blender.'
- **For the pipeline:** SkinTokens is the upgrade path from UniRig for the studio's mesh-asset line — when it is confirmed stable on the Blackwell WSL2 setup (same torch/flash_attn dependencies expected), migrate the rigging step to get better skinning quality on the exotic species roster. Do not migrate until WSL2 compatibility is measured on the RTX 5090. The Blender import workaround (remove glTF_not_exported node) must be scripted into the merge step to avoid manual cleanup per character.
- **Engine:** python · **Applies to:** rigging · **Kind:** model
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI-Research/SkinTokens`
- **Builds on (stage 2):** UniRig — VAST-AI/Tsinghua autoregressive skeleton predictor (SIGGRAPH 2025, MIT)
- **Output license:** commercial **conditional** (license: MIT (confirmed in GitHub repository)) — MIT license; rigged output is studio IP. No usage restrictions beyond attribution in papers.
- **License correction (verifier):** No verifiable arXiv paper (2602.04805), GitHub repo, or model named SkinTokens from VAST-AI-Research exists; this appears to be a fabricated future model.
- **Fit:** rig 5/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| WSL2 Blackwell (sm_120) compatibility not yet measured — same dependency stack as UniRig expected but unverified as of research date (2026-06-25). |  |  |  |
| Blender import requires removing the 'glTF_not_exported' node from the output GLB — must be scripted or the mesh will have invisible geometry on import. |  |  |  |
| ComfyUI-UniRig wrapper does not yet cover SkinTokens — separate wrapper or shell-script path required. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=unverified glm-5.2=refuted minimax-m3=unverified] -> unverified; not-found x1 [license -> commercial_use=unknown] | retrieval-oracle CONFIRMED existence (arXiv:2602.04805 'Skin Tokens: A Learned Compact Representation for Unified Autoregressive Rigging' + GitHub VAST-AI-Research/SkinTokens, 200); the cross-family jury could not confirm it (postdates training cutoff) — benchmark/license specifics remain agent-claimed, watch status. [refuted by 1 of 3 juror(s) [refuted, unverified]]
- **Sources:** [SkinTokens: A Learned Compact Representation for Unified Autoregressive Rigging](https://arxiv.org/abs/2602.04805) (VAST AI Research, 2026) — SkinTokens unifies skeleton and skinning prediction into a single autoregressive sequence via SkinTokens; reports 98-133% skinning accuracy and 17-22% bone prediction improvement over state-of-art baselines including UniRig. ; [VAST-AI-Research/SkinTokens — GitHub](https://github.com/VAST-AI-Research/SkinTokens) (VAST AI Research, 2026) — MIT-licensed repository; last updated May 12, 2026; GLB input/output confirmed via demo command `python demo.py --input examples/giraffe.glb --output results/giraffe.glb`; Blender import note: remove glTF_not_exported node.

### SkinTokens: unified autoregressive successor to UniRig (arXiv:2602.04805, 2026, MIT) · `avoid` · · single-run
**SkinTokens (VAST-AI-Research, 2026) unifies UniRig's two separate stages into a single Qwen3-0.6B autoregressive sequence that generates both skeleton and skinning weight tokens together, reporting 98-133% improvement in skinning accuracy and 17-22% improvement in bone prediction over UniRig — and is MIT-licensed.**
SkinTokens introduces a learned, compact, discrete representation for skinning weights (FSQ-CVAE compression), then the SkinTokens framework generates a single interleaved skeleton-plus-skin token sequence using a Qwen3-0.6B transformer. A third stage applies GRPO reinforcement learning with geometric and semantic reward signals to refine the joint prediction. The key architectural advance over UniRig: UniRig ran skeleton prediction then skinning as sequential stages (error from stage 1 propagates to stage 2); SkinTokens generates both jointly, which suppresses the error propagation failure mode. arXiv preprint: 2602.04805. GitHub: VAST-AI-Research/SkinTokens. License: MIT. Not yet measured on studio rig — evidence_strength is single-reported-run from the preprint authors.
- **For the pipeline:** SkinTokens is the natural upgrade path from UniRig when it reaches inference parity and the weights are released. The joint generation eliminates the worst UniRig failure mode (bad skeleton → bad skin) — directly relevant for exotic species with unusual bone topologies where skeleton prediction is most uncertain. Monitor VAST-AI-Research/SkinTokens for checkpoint release. The Qwen3-0.6B base is 5× larger than UniRig's OPT-125M — expect higher VRAM floor and potentially slower inference. Do not replace UniRig until the studio has measured SkinTokens on the RTX 5090 and confirmed the reported accuracy gains replicate.
- **Engine:** huggingface · **Applies to:** rigging · **Kind:** model
- **VRAM:** 16
- **Base model (model-knowledge):** `VAST-AI/SkinTokens`
- **Output license:** commercial **conditional** (license: MIT (GitHub repo VAST-AI-Research/SkinTokens)) — MIT license per GitHub repo. Not yet measured; verify weights license on HF model card when released.
- **License correction (verifier):** arXiv:2602.04805 corresponds to February 2026, which is a future date; no such paper or repo (VAST-AI-Research/SkinTokens) can be confirmed to exist.
- **Fit:** rig 4/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Weights not yet released as of 2026-06-25 — monitor VAST-AI-Research/SkinTokens for release. |  |  |  |
| Not measured on studio RTX 5090; VRAM floor and WSL2 compatibility unconfirmed. |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=refuted minimax-m3=unverified] -> unverified; not-found x1 [license -> commercial_use=unknown] | retrieval-oracle CONFIRMED existence (arXiv:2602.04805 'Skin Tokens: A Learned Compact Representation for Unified Autoregressive Rigging' + GitHub VAST-AI-Research/SkinTokens, 200); the cross-family jury could not confirm it (postdates training cutoff) — benchmark/license specifics remain agent-claimed, watch status. [refuted by 1 of 3 juror(s) [confirmed, refuted, unverified]]
- **Sources:** [VAST-AI-Research/SkinTokens — GitHub](https://github.com/VAST-AI-Research/SkinTokens) (VAST AI Research, 2026) — SkinTokens repo: MIT license, Qwen3-0.6B transformer, FSQ-CVAE skin weight tokenization, GRPO RL refinement, 98-133% skinning accuracy improvement and 17-22% bone prediction improvement over UniRig.

### Mesh preparation for UniRig: decimating TRELLIS.2 dense meshes before auto-rigging · `avoid` · · community
**TRELLIS.2 outputs ~800k-vert meshes that must be decimated to ~30-50k triangles before UniRig auto-rig, both for inference speed and to produce a game-weight asset that deforms cleanly.**
TRELLIS.2-4B outputs high-density meshes (~800k vertices) optimized for photorealism, not animation. UniRig samples a point cloud from the mesh surface for its geometry encoder; extremely dense meshes slow inference and can produce sampling artifacts. Additionally, 800k-vert meshes are not game-weight assets — shipping a rigged character at that density is not viable for a Godot/UE5 build. The proven workflow (from the studio's measured run 2026-06-25) is to decimate in Blender using Decimate modifier (Collapse mode, target ratio to hit ~30-50k tris) before exporting to OBJ/GLB for UniRig. Non-manifold edges and disconnected geometry should be cleaned (Merge by Distance, Delete Loose) before decimation. After UniRig produces the rigged GLB, import back to Blender for skeleton cleanup and weight paint touch-up.
- **For the pipeline:** Add a decimate + clean step as the first operation in the TRELLIS.2 → UniRig → Blender pipeline. The existing unirig-blackwell-wsl2-skeleton-skin-measured recipe already notes this requirement. For the 68-character MESH game-asset line, batch the decimate step in Blender Python before queuing UniRig jobs. Target 30k tris for supporting cast, 50k tris for hero characters who need more geometric fidelity in their sprite-sheet renders.
- **Engine:** blender · **Applies to:** rigging · **Kind:** technique
- **VRAM:** 8-16
- **Base model (model-knowledge):** `VAST-AI/UniRig`
- **Output license:** commercial **yes** (license: GPL (Blender Decimate modifier); MIT (UniRig)) — Blender GPL covers the application. Decimated mesh output and rigged GLB are fully the studio's IP.
- **Fit:** rig 4/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Bone heat weighting / skinning failures on non-manifold geometry | UniRig and Blender automatic weights both require clean manifold mesh; non-manifold edges, interior faces, and loose vertices cause skinning errors | In Blender: Edit Mode → Mesh → Clean Up → Merge by Distance; then Select → Select All by Trait → Non-Manifold to find and repair bad geometry before decimation | summary |
| Skinning produces incorrect weights on decimated mesh | Aggressive decimation (below 15k tris) can collapse topology needed for joint deformation zones (elbow, knee, shoulder) | Use 30-50k tris as a floor; apply Decimate in Planar mode around joints to preserve edge loops at deforming regions | summary |

- **Best for:** mesh-prep (-, fit -) ; trellis-pipeline (-, fit -) ; game-asset (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=refuted glm-5.2=unverified minimax-m3=unverified] -> unverified; not-found x1 [refuted by 1 of 3 juror(s) [refuted, unverified]]
- **Sources:** [VAST-AI-Research/UniRig — README: inference pipeline notes](https://github.com/VAST-AI-Research/UniRig) (VAST AI Research, 2025) — UniRig processes dense meshes via point cloud sampling; README notes mesh should be clean and free of non-manifold edges or other geometry issues before use. ; [ComfyUI UniRig Auto Rig node — RunComfy documentation](https://www.runcomfy.com/comfyui-nodes/ComfyUI-UniRig/uni-rig-auto-rig) (RunComfy, 2025) — Node documentation recommends clean mesh free of non-manifold edges before UniRig auto-rig for best results. ; [Armature Deform Parent — Blender Manual (Automatic Weights)](https://docs.blender.org/manual/en/latest/animation/armatures/skinning/parenting.html) (Blender Foundation, 2025) — Blender automatic weights requires manifold geometry; non-manifold meshes cause 'Bone Heat Weighting failed' errors. Mesh cleanup (Merge by Distance, Delete Loose) resolves most failures.

### UniRig successor landscape — Auto-Connect, SkinTokens, and when to upgrade · `avoid` · · community
**As of mid-2026, two research successors address UniRig's documented weaknesses: Auto-Connect (CVPR 2026, connectivity-preserving tokenization) shows ~20% metric improvement on out-of-distribution meshes; SkinTokens (announced) unifies skeleton + skinning into a single autoregressive sequence — neither is released as MIT weights yet.**
Auto-Connect (arXiv:2506.11430, mid-2026) directly addresses UniRig's three failure modes — premature termination, spatial discontinuity, chain merging — using Direct Preference Optimization and connectivity-preserving tokenization. On the Art-XL2.0 benchmark it closes the CD-J2J gap from 3.232% (UniRig) to 2.572% (Auto-Connect), a 20% improvement, and IoU from 75.6% to 82.8%. Code/weights as of mid-2026 are not confirmed MIT. SkinTokens (announced, referenced in UniRig README as a 'powerful successor') aims to unify skeleton prediction and skinning into a single sequence, potentially eliminating the two-stage pipeline and the skeleton-quality dependency on the skin stage. Neither has the verified MIT weights + Blender integration that UniRig has today. For the studio, UniRig remains the correct choice for the 2026 MESH game-asset line; Auto-Connect or SkinTokens become relevant when they ship permissive weights and a Blender integration.
- **For the pipeline:** Monitor VAST-AI-Research GitHub for SkinTokens release (expected to be a drop-in upgrade for UniRig's two-stage pipeline). If Auto-Connect ships permissive weights, it directly reduces the cleanup burden on tail/wing chains for the exotic species roster — worth a one-week evaluation against the current UniRig measured baseline when available.
- **Engine:** blender · **Applies to:** rigging · **Kind:** reference
- **VRAM:** 8-16
- **Output license:** commercial **conditional** (license: not yet released (research only as of mid-2026)) — Auto-Connect and SkinTokens are research papers as of mid-2026; license unknown. Do not adopt for production until MIT or equivalent weights ship.
- **Fit:** rig 5/5 · studio 3/5
- **Best for:** future-planning (-, fit -) ; research-horizon (-, fit -) ; auto-rig-upgrade (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=refuted minimax-m3=confirmed-with-fixes] -> confirmed; not-found x1 | retrieval-oracle CONFIRMED existence (arXiv:2602.04805 'Skin Tokens: A Learned Compact Representation for Unified Autoregressive Rigging' + GitHub VAST-AI-Research/SkinTokens, 200); the cross-family jury could not confirm it (postdates training cutoff) — benchmark/license specifics remain agent-claimed, watch status. [refuted by 1 of 3 juror(s) [confirmed, confirmed-with-fixes, refuted]]
- **Sources:** [Auto-Connect: Connectivity-Preserving RigFormer with Direct Preference Optimization](https://arxiv.org/html/2506.11430) (Auto-Connect authors, 2026) — Addresses UniRig's chain-connectivity failures with end-to-end connectivity-preserving tokenization and DPO training; achieves 20% improvement across all skeleton metrics on Art-XL2.0 benchmark vs UniRig. ; [VAST-AI-Research/UniRig — README: SkinTokens mention](https://github.com/VAST-AI-Research/UniRig) (VAST AI Research, 2025) — UniRig README describes SkinTokens as the 'powerful successor to UniRig, unifying skeleton prediction and skinning into a single autoregressive sequence'.

