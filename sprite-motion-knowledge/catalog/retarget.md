# Retargeting onto stylized rigs
_Getting external mocap onto the studio stylized / non-humanoid 2.5D rigs: Blender Rokoko / Auto-Rig-Pro remap, UE5 IK Retargeter, proportion mismatch (the JRPG / exotic-species silhouette problem), foot-IK cleanup._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

8 recipes · 5 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | Auto-Rig Pro — Remap (retargeting) module | blender | retarget | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Bake to Action → 8-camera ortho render handoff | blender | retarget | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Rokoko Blender plugin — retargeting module | blender | retarget | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 6 | Blender built-in bone-constraint manual retargeting (no addon) | blender | retarget | ▸ reproduced | ✅ yes | 4 | 3 | ✓ |
| 6 | Cascadeur — physics-based animation cleanup after retarget | custom | retarget | ▸ reproduced | ⚠ cond | 3 | 3 | ✓ |
| 6 | Foot IK lock + bake — eliminating foot-slide post-retarget | blender | foot-ik | · community | ✅ yes | 4 | 4 | ✓ |
| 6 | Non-humanoid retarget strategy — additive layers + hand-authoring | blender | non-humanoid | · community | ✅ yes | 3 | 5 | ✓ |
| 6 | Unreal Engine 5 IK Rig + IK Retargeter | custom | retarget | ▸ reproduced | ⚠ cond | 3 | 2 | ✓ |

## Detail

### Auto-Rig Pro — Remap (retargeting) module · `recommended` · ▸ reproduced
**Auto-Rig Pro's Remap tab is the most feature-complete humanoid retargeting solution inside Blender: ships with Mixamo, Rokoko, and XSens presets, supports IK feet/hands for foot-slide reduction, and can batch-retarget multiple actions — but non-humanoid targets (tails, wings, digitigrade) still require manual bone-mapping with no preset support.**
ARP Remap imports a source FBX or BVH, maps source bones to target bones (auto-matched by name for supported presets), enables IK mode for limb ends to reduce foot-slide, and bakes the result frame-by-frame onto the target armature. The interactive offset tool compensates for proportion differences. A Multiple Source Anim button handles batch retargeting in one pass. The 'any armature' claim in docs holds for the remap mechanism, but embedded presets only cover humanoid skeletons — exotic species need manual bone mapping and significant post-cleanup.
- **For the pipeline:** Preferred Blender retarget tool for human-proportioned characters; pairs naturally with ARP-rigged studio characters from the rigging lane. For the exotic roster, use ARP Remap as a skeleton-agnostic manual mapper but budget significant per-species setup time. Batch mode is a multiplier when retargeting a clip library across a full cast.
- **Engine:** blender · **Applies to:** retarget · **Kind:** tool
- **VRAM:** n/a
- **Builds on (stage 1):** Rokoko Blender plugin — retargeting module
- **Output license:** commercial **yes** (license: Paid commercial addon; Extended Commercial License available (unlimited projects, no sales cap)) — Available via Superhive (Blender Market) and Gumroad. Extended Commercial License covers unlimited commercial projects. Actively used in shipped indie games (Manor Lords, Fabledom, Paralives). Does not launder source clip license.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| No built-in presets for non-humanoid targets | Embedded presets cover Mixamo/Rokoko/XSens → ARP humanoid only; exotic species require full manual bone mapping | Build and save a custom preset per exotic species type; reuse across characters of same skeleton family | applicable_to |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Remap — AutoRigPro Documentation](https://www.lucky3d.fr/auto-rig-pro/doc/remap_doc.html) (Artell, 2023) — Official ARP Remap docs: preset list includes Mixamo, Rokoko, XSens; IK feet/hands mode available; multiple-source-anim batch retargeting; target armature 'can be any type' but presets are ARP-humanoid-only. ; [Refining Mocap with Mixamo and Blender AutoRig PRO — Garage Farm](https://garagefarm.net/blog/refining-motion-capture-with-mixamo-and-blender-auto-rig-pro) (Garage Farm, 2024) — Community walkthrough confirming ARP Remap Mixamo preset workflow and post-bake cleanup steps in a production context.

### Bake to Action → 8-camera ortho render handoff · `recommended` · ▸ reproduced
**The final step of every retarget lane — baking the corrected, IK-locked animation to a clean FK Action, then passing it to the 8-camera orthographic render rig — is a discrete pipeline stage with specific settings that prevent constraint drift and ensure render-clean keyframe output.**
After all retarget and IK-lock work is done in Pose mode, select all bones and run Pose → Animation → Bake Action with: Only Selected Bones checked, Visual Keying checked, Clear Constraints checked, Overwrite Current Action checked. This bakes the visual pose (after constraints resolve) to keyframes on the target armature and removes all retarget constraints, leaving a self-contained Action. This Action is then consumed by the 8-camera ortho render rig (cameras fixed at 8 directions around the character, orthographic projection, one render pass per direction per animation clip). Post-render, sprite-sheet assemblers (Blender-Spritesheet-Renderer or custom Python scripts) composite frames into the engine-ready sprite atlas. The bake is the hard boundary between the motion authoring domain and the rendering domain.
- **For the pipeline:** Never hand the ortho render rig a constraint-dependent pose — constraints are evaluated at render time but can produce inconsistent results if the source armature is not present. Always bake to a clean Action first. Store the constraint-laden.blend as the 'edit master' and the baked Action as the 'render master' in separate files or as separate actions in the same file.
- **Engine:** blender · **Applies to:** retarget · **Kind:** workflow
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: Blender native (GPL); output unrestricted) — Standard Blender pipeline; rendered output and baked action data are unrestricted for commercial use.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Baked action has constraint drift or 'jumpy' frames | Visual Keying not enabled — Blender baked the driver value rather than the resolved visual pose | Re-run Bake Action with Visual Keying checked; also ensure scene frame rate matches animation clip frame rate | summary |

- **Best for:** pipeline-handoff (-, fit -) ; render-prep (-, fit -) ; sprite-sheet (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Render 4 or 8 Direction Animated Sprites from Blender — Foozle](https://foozlecc.itch.io/render-4-or-8-direction-sprites-from-blender) (Foozle, 2023) — Documents the 8-direction ortho render workflow in Blender: orthographic camera rig, action-per-direction rendering, and sprite sheet compositing — confirms baked Actions are the input. ; [Blender Spritesheet Renderer — GitHub](https://github.com/chrishayesmu/Blender-Spritesheet-Renderer) (chrishayesmu, 2023) — Open-source Blender addon that automates the per-direction, per-action render loop and sprite atlas assembly — confirms the bake-to-action → assign-to-camera-rig handoff pattern.

### Rokoko Blender plugin — retargeting module · `recommended` · ▸ reproduced
**The free, open-source Rokoko Blender addon (LGPL-3.0) retargets a source mocap armature onto a target rig inside Blender using a bone-list mapping and optional Auto Scale — well-proven for humanoid→humanoid but requires heavy manual cleanup on the studio's exotic species.**
The plugin's retargeting tab lets you select a source armature (e.g. a Rokoko/Mixamo export) and a target armature, auto-builds a bone correspondence list, optionally scales for size differences, and bakes the result into an Action. Humanoid→humanoid transfers are reliable. For the studio's non-humanoid roster (tails, wings, digitigrade legs, fins) the proportion and topology mismatch produces foot-slide, broken contacts, and disconnected extremity chains that fall outside the mapping model. Does NOT launder source-clip license: a non-commercial mocap clip stays non-commercial after retarget.
- **For the pipeline:** Use as the default humanoid retarget path inside Blender for human-proportioned characters. For exotic species, treat retarget output as a rough blocking pass and budget a full cleanup session, or bypass retarget and hand-author from scratch.
- **Engine:** blender · **Applies to:** retarget · **Kind:** tool
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: LGPL-3.0 (addon open source); Blender output is unrestricted) — Addon and Blender output are commercial-clean. The retarget step does NOT launder the source clip's license — a non-commercial clip remains non-commercial after retarget regardless of tool used.
- **Fit:** rig 5/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| foot-slide and broken contacts on non-humanoid targets | Bone-list mapping assumes roughly humanoid topology; proportion mismatch (digitigrade legs, tails, fins, wings) produces incorrect rotation propagation | Apply foot-IK lock post-retarget, or hand-author for heavily non-human species | applicable_to |
| Source-clip license not transferred | The tool remaps rotation data; it cannot change the intellectual-property terms of the motion data itself | Verify source clip license before retargeting; check the mocap-datasets lane for commercial-clean sources | commercial_notes |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Retarget an animation in Blender — Rokoko Support](https://support.rokoko.com/hc/en-us/articles/4410463481489-Retarget-an-animation-in-Blender) (Rokoko, 2024) — Official step-by-step guide: select source armature → Build Bone List → Auto Scale → bake. Confirms the tool works on any custom armature but tutorials only demonstrate humanoid setups. ; [rokoko-studio-live-blender — GitHub](https://github.com/Rokoko/rokoko-studio-live-blender) (Rokoko, 2024) — Plugin is LGPL-3.0 open source; free to use commercially without restriction on the tool itself.

### Blender built-in bone-constraint manual retargeting (no addon) · `situational` · ▸ reproduced
**Blender's native Copy Rotation / Copy Location constraints can retarget any source skeleton onto any target rig without addons — fully free, fully commercial-clean, and the only path that can handle arbitrary non-humanoid bone structures without an addon's humanoid assumptions.**
Attach Copy Rotation (and optionally Copy Location or IK) constraints to each target bone, referencing the corresponding source bone. The constraint-based live preview lets you validate the mapping, then Pose → Animation → Bake Action bakes it to keyframes on the target with Visual Keying and Clear Constraints checked. Tedious for full-body rigs but uniquely flexible: you can map, skip, or invert any individual bone chain, making it the only zero-assumption path for the studio's exotic species. Result is a clean Action ready for the 8-camera ortho render pipeline.
- **For the pipeline:** Fallback for any species where addon presets fail. For the exotic roster (tortle shell, sahuagin fins, kenku wings), start constraint-retarget on the shared humanoid bones (spine, arms, head), skip fins/tail/shell entirely, and hand-author the species-specific chains as additive layers. More setup time than ARP Remap but no per-species preset debt.
- **Engine:** blender · **Applies to:** retarget · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: Blender is GPL; output animations are unrestricted (Blender Foundation confirmed output license)) — Blender GPL does not infect output content. Commercial use of rendered animations and baked action data is unrestricted.
- **Fit:** rig 4/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Very high setup time per character | Every bone pair must be manually constrained; no batch mapping | Build a reusable constraint-template .blend file per species skeleton family; use ARP Remap for humanoid characters instead | studio_fit |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Copy Rotation Constraint — Blender 5.1 Manual](https://docs.blender.org/manual/en/latest/animation/constraints/transform/copy_rotation.html) (Blender Foundation, 2025) — Official manual: Copy Rotation forces an object or bone to match a target's rotation; forms the basis for manual bone-constraint retargeting in Blender without addons. ; [Nonlinear Animation — Blender 4.5 LTS Manual (Bake Action)](https://docs.blender.org/manual/en/latest/editors/nla/editing.html) (Blender Foundation, 2024) — Documents Bake Action workflow (Visual Keying + Clear Constraints) used to convert constraint-based retarget to independent keyframes on the target armature.

### Cascadeur — physics-based animation cleanup after retarget · `situational` · ▸ reproduced
**Cascadeur (Pro, $25/mo billed annually) applies physics-based AutoPhysics and sliding-correction passes to retargeted animation, turning a rough retarget into physically plausible motion — but retargeting itself requires characters to have a generated Autoposing rig, which fails for highly exotic anatomies.**
After retargeting in Blender or UE5, import the baked FBX into Cascadeur. AutoPhysics analyzes the animation and suggests physically accurate weight/momentum corrections; the Polishing tools remove jitter, fix foot-slide via Bezier-clamped interpolation or Fixed interpolation, and correct rotational distortions. Cascadeur's own retarget feature (copy/paste transfer, added 2024.1) requires a Cascadeur Autoposing rig on both source and target — this rig can be generated for bipeds but may not generate for the studio's most exotic species. Use Cascadeur as a cleanup stage post-Blender-retarget rather than as the primary retarget tool.
- **For the pipeline:** Best used as a secondary polish pass on already-retargeted humanoid animations before the bake-to-ortho-render step. For exotic species, Cascadeur's own retarget is blocked by rig-generation limits — use its physics tools only, not its retarget feature.
- **Engine:** custom · **Applies to:** retarget · **Kind:** tool
- **VRAM:** n/a
- **Output license:** commercial **conditional** (license: Proprietary; Free (non-commercial only), Indie ($6/mo, <$100k revenue), Pro ($25/mo, unlimited commercial)) — Free tier is non-commercial only. Indie tier covers studios under $100k annual gross revenue. Pro tier is required for unlimited commercial use. Retargeting feature is Indie+ (not available in Free). Annual subscriptions convert to perpetual licenses after 12 months.
- **Fit:** rig 3/5 · studio 3/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Cascadeur retarget blocked for exotic species | Cascadeur's internal retarget requires a generated Autoposing rig; exotic anatomies (multiple appendages, radically non-humanoid) may not generate a valid rig | Use Cascadeur only for physics cleanup pass, not as primary retarget; retarget in Blender first | applicable_to |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Cascadeur Pricing Plans](https://cascadeur.com/plans) (Cascadeur, 2025) — Retargeting is Indie+ feature; Free tier non-commercial only; Pro = unlimited commercial use; annual subscriptions convert to perpetual licenses. ; [Cascadeur FAQ](https://cascadeur.com/help/faq) (Cascadeur, 2025) — States: 'If your characters can't have an Autoposing rig generated, the retargeting has to be done in another software.' Confirms physics tools (AutoPhysics) require decent source animation as input. ; [Polishing — Cascadeur Help](https://cascadeur.com/help/animation_pipeline/polishing) (Cascadeur, 2025) — Documents sliding correction via Bezier clamped / Fixed interpolation, jitter removal, and trajectory editing — the physics cleanup tools used post-retarget.

### Foot IK lock + bake — eliminating foot-slide post-retarget · `recommended` · · community
**Adding a temporary IK constraint to each foot with a ground-locked Empty as target, then baking the corrected pose back to FK keyframes, is the primary technique for eliminating foot-slide artifacts that appear on nearly every retargeted clip — especially critical for the studio's non-humanoid characters where proportion mismatch amplifies slide.**
After retargeting, push the mocap action into an NLA strip to protect the original data. For each foot bone, create a ground-plane Empty and add an IK constraint on the foot chain targeting the Empty. Keyframe the Empty to match ground contact frames (foot contacts the ground = Empty locked at floor height). Then Bake Action in Pose mode with Visual Keying + Clear Constraints to bake the corrected positions to FK keyframes. Verify in the Graph Editor and smooth residual noise. For non-humanoid legs (digitigrade, triple-jointed, fin-as-foot) the same technique applies but the IK chain length and pole target angle must be set species-specifically. This is the most reproducible foot-slide fix that does not require a paid addon.
- **For the pipeline:** Make this a required pipeline step for every retargeted clip before the 8-camera ortho render. Budget 15-30 min per clip for a human character; 45-90 min for an exotic species with non-standard foot topology. Auto-Rig Pro's IK mode reduces this overhead significantly for ARP-rigged characters.
- **Engine:** blender · **Applies to:** foot-ik · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: Blender native technique — no addon required) — Pure Blender technique; output is unrestricted for commercial use.
- **Fit:** rig 4/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Foot still slides if Connected bone flag is set | Blender 'Connected' bone property prevents location override by IK; the foot bone stays chained to parent | In Bone Properties → Relations, uncheck 'Connected' on the foot/toe bone before applying the IK constraint | summary |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Fixing animated hand and foot sliding — BlenderNation](https://www.blendernation.com/2023/09/04/fixing-animated-hand-and-foot-sliding/) (BlenderNation editorial, 2023) — Documents the NLA strip → IK constraint → Empty lock → Bake Action workflow for eliminating foot-slide from retargeted mocap in Blender. ; [The Complete Guide to Retargeting Mocap to Custom Character Rigs — MocapWork](https://mocapwork.com/blog/retargeting-mocap-custom-rigs/) (MocapWork, 2024) — Identifies foot sliding as a primary retarget failure mode; attributes root cause to height mismatch and missing IK; recommends foot IK enable and scale animation as remediation.

### Non-humanoid retarget strategy — additive layers + hand-authoring · `recommended` · · community
**For the studio's exotic species roster (digitigrade kenku, finned sahuagin, shelled tortle, animal-headed humanoids), retarget the shared humanoid skeleton (spine/arms/head) as a base layer, then hand-author species-specific chains (tails, wings, fins, shell offsets) as additive NLA strips on top — because standard retarget tools have no concept of appendages that have no mocap counterpart.**
Divide the exotic character's rig into humanoid-adjacent bones (pelvis, spine, arms, head) and species-specific bones (tail, wing, fin, shell, extra limbs). Retarget the humanoid subset using ARP Remap or Rokoko addon, accepting that species bones will be ignored. Then hand-keyframe the species chains using shape-reference poses and action constraints in a separate NLA strip set to additive blend. This mirrors how AAA creature animation studios use a 'blocking from mocap + creature-specific keyframe on top' workflow. For bipedal exotic characters (kenku, tortle who walk upright) the humanoid retarget covers 70-80% of the motion; tails and wings are the hand-authored additive portion. For radically non-humanoid targets (sahuagin, crab-folk), retarget may cover only spine and head; most motion is bespoke.
- **For the pipeline:** Budget per-character: bipedal exotic = 1 day (retarget humanoid base + half-day additive); radically non-humanoid = 2-3 days full hand-author. The retarget tools save time proportional to how humanoid the target is. This technique is a studio-specific policy decision, not a tool — communicate it clearly in the sprint plan so exotic species don't get underestimated as 'just a retarget job'.
- **Engine:** blender · **Applies to:** non-humanoid · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: Pure technique; uses Blender NLA (GPL, output unrestricted)) — Technique using Blender native NLA; output is commercial-clean.
- **Fit:** rig 3/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Additive NLA strip introduces root-motion double-counting | If both the base retarget layer and the additive layer include root bone keyframes, hip/root position is doubled | Zero out root-bone keyframes in the additive strip; let the base retarget layer drive the root | summary |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Creature Animation for Games — MoCap Online blog](https://mocaponline.com/blogs/mocap-news/creature-animation-games-guide) (MoCap Online, 2024) — Describes the industry approach: 'retargeted animation as a blocking layer and keyframe-polish over it to reshape creature-specific details (claw angle, neck curve, tail counterbalance)' — the source for the additive-layer hybrid technique. ; [Animating Non-Human Characters: Challenges and Techniques — RMCAD](https://www.rmcad.edu/blog/animating-non-human-characters-challenges-and-techniques/) (Rocky Mountain College of Art + Design, 2024) — Surveys non-humanoid animation challenges and confirms that appendages without motion-capture counterparts (tails, wings, multiple legs) must be hand-authored or driven by procedural rigs, not retargeted from human mocap.

### Unreal Engine 5 IK Rig + IK Retargeter · `situational` · ▸ reproduced
**UE5's IK Rig + IK Retargeter system is the modern engine-side retarget path: supports explicit limb-chain mapping (arms, legs, spine, tail, tentacles per documentation), proportional compensation across size differences, and foot-IK contact preservation — but auto-chain generation is biped-only and exotic species require manual IK Rig setup.**
Create an IK Rig asset for both source and target skeletons defining bone chains (spine, limb pairs, optionally tail/jaw/etc.). An IK Retargeter asset maps chains between the two rigs, aligns reference poses, and compensates proportions frame-by-frame. Auto Retargeting can auto-generate chains for standard biped skeletons (UE Mannequin, MetaHuman) but explicitly requires manual chain authoring for non-humanoid topologies. Retargeted animations can be batch-exported as Animation Sequences. The studio's primary engine is Blender-to-ortho-render, so UE5 retarget is secondary — useful if the studio later moves to a real-time engine or wants runtime retarget at play time.
- **For the pipeline:** Not the primary studio path (pipeline is Blender → ortho render → sprite sheet), but relevant if the studio adopts a real-time UE5 presentation layer or needs runtime retarget for in-engine cutscenes. Non-humanoid species need fully manual IK Rig authoring — the auto-biped chain generator will not handle tails, wings, or digitigrade legs.
- **Engine:** custom · **Applies to:** retarget · **Kind:** tool
- **VRAM:** n/a
- **Output license:** commercial **conditional** (license: Unreal Engine EULA — royalty-free for commercial games below $1M gross revenue; standard royalty above) — UE5 EULA: 5% royalty on gross product revenue above $1,000,000 per product. Below that threshold is royalty-free for commercial games. IK Retargeter output (baked Animation Sequences) is commercial-clean under the EULA.
- **Fit:** rig 3/5 · studio 2/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Auto Retarget Chains fails on exotic skeletons | Tool matches against biped templates (UE Mannequin skeleton naming); non-standard bone hierarchies produce no or wrong chain auto-mapping | Manually define IK chains for each exotic species skeleton; use the IK Rig editor to name and configure each chain | applicable_to |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [IK Rig Animation Retargeting in Unreal Engine — Epic Developer Community](https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-animation-retargeting-in-unreal-engine) (Epic Games, 2025) — Official UE5.8 docs: confirms tail, tentacle, jaw as named chain types; describes proportional compensation and reference pose alignment; IK Retargeter supports 'characters of any size'. ; [Auto Retargeting in Unreal Engine — Epic Developer Community](https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-retargeting-in-unreal-engine) (Epic Games, 2025) — Confirms Auto Retarget Chains targets 'common biped skeletons' (Mannequin, MetaHuman, Stack O Bot) and relies on skeleton naming conventions — non-humanoid skeletons are not covered.

