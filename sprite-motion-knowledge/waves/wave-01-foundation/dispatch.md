# Wave 01 — Foundation: the sprite-motion pipeline

**KB #9 `sprite-motion-knowledge` · dispatched 2026-06-24 · 7 parallel lane agents (Sonnet), web-grounded + sourced.**
Verification receipt (cross-family PoLL jury): [`verification.md`](verification.md). Raw verified output: [`research-raw.json`](research-raw.json).

This is the **animation layer** atop [`sprites-knowledge`](../../../sprites-knowledge/catalog/README.md) (KB #5, static
2.5D sprite generation). It answers: *how do I make an approved painterly 2.5D sprite walk, swing, idle, and die —
without melting the character or detaching the weapon — and how well does each approach hold up?*

## The spine (every lane serves this)

```
motion truth (rig / mesh / proxy)  ->  AI polish / inbetween / repaint  ->  sprite-sheet export  ->  local verify
   ▣ deterministic floor                  ◐ generative ceiling                                       ✓ admission gate
```

This is **not** "AI video → sprite sheet" (it drifts, mutates faces, makes combat mushy). It is the same insight the
studio already proved for rigid weapons — the §D weapon-drift fix (no diffusion method rotates a rigid held prop;
the prop must be rigid in 3D, then repainted) — generalised from a static turnaround to walk / attack / hurt / death.
The deterministic-floor + generative-ceiling + verifier shape matches the studio's workflow standards and the
research-grounded protocol.

## The 7 lanes — findings → recommendation

**1. `motion-arch` — Motion architecture & contracts.** The per-character **animation contract/manifest** (views;
animations + frame counts + loop flags; anchors root/head/hands/weapon_grip/weapon_tip/feet; layers
body/weapon/shadow/fx) is the keystone: it turns "make a cool animation" into a verifiable target every downstream
stage (rig → render → repaint → QA) aims at. Backed by the **3-lane production model** (rig-proxy for combat, AI for
life/idle, manual keyframe for hit frames), the **one-motion-cage-rendered-per-direction** rule (not 80 independent
images), and Godot 4 (`AnimatedSprite2D`/`SpriteFrames`, `Skeleton2D`) / UE5 (Paper2D flipbooks) consumption.
→ Adopt the manifest as the contract that gates the whole pipeline.

**2. `rigging` — Rigging & skeletons.** The rig is the deterministic motion source. The load-bearing recipe is the
**`hand → weapon_grip → weapon_tip` rigid bone chain** — the weapon is a rigid child of the grip bone, so length/angle
stay constant across views/frames (the weapon-drift fix, by construction). The studio-proven **TRELLIS.2-4B mesh →
8-view Blender render** path is the combat backbone (captain prototype: rigid weapon + face survives). Auto-rig
options ranked by license: **UniRig (MIT)** and Rigify (GPL, output-clean) are the open defaults; AccuRIG (free EULA)
and Auto-Rig Pro (paid) are convenience layers; Mixamo (royalty-free, no raw-file redistribution) seeds humanoid
motion. The 2.5D-proxy-rig-then-repaint beats both a full-3D model and a flat-PNG puppet.
→ Rig the motion truth in Blender; keep all extended-weapon work on this lane.

**3. `ai-motion` — AI motion models (the polish/propose ceiling, NOT combat truth).** Strongly license-decisive — most
character-animation research weights are non-commercial. Commercial-safe: **Qwen-Image-Edit-2511 (Apache)** for the
pose-guided **repaint** that recovers painterly style after a proxy/mesh render; MimicMotion / Animate-X (Apache) and
Wan2.1-I2V (Apache, but it *warps* rigid props → situational) for life/idle proposals; AnimateDiff (Apache module,
but inherits the base-checkpoint license → conditional) for idle shimmer. **UniAnimate flagged non-commercial →
`avoid`** (drop-in: MimicMotion/Animate-X). Pose-conditioned ControlNet (OpenPose/DWPose) drives a frozen checkpoint.
→ Use these for life/idle/stylisation and the repaint step; never for rigid-prop combat truth.

**4. `inbetween` — Inbetweening & interpolation.** Multiply sparse keyposes into smooth motion. **FILM (Apache, code +
weights)** is the cleaner-licensed default for large-displacement (attack swings, sparse 2-key); **RIFE/Practical-RIFE
(MIT code, weights-vary → conditional)** for dense smooth walks; EMA-VFI (conditional). **GIMM-VFI flagged S-Lab
non-commercial → blocked**, listed only to prevent accidental adoption. The ComfyUI Frame-Interpolation node set is the
practical integration point; the keypose → interpolate → palette-cleanup workflow is the pattern. Thin-limb /
fast-contact-pose artifacts always need a cleanup pass.
→ FILM for attacks, RIFE for walks; treat interpolation as a post-process assist you only trust when you own the keys.

**5. `cloud-workers` — Cloud GPU workers (run bigger-than-32GB off-box).** Cloud is **just compute** — the source of
truth (approved art, rigs, motion specs, receipts) stays in the repo. **Modal** is the cleanest "run my own Python
pipeline on bigger GPUs" (A100→B200, multi-GPU); **RunPod serverless** is the default for ComfyUI-graph workers (cached
models, cold starts); **fal.ai** for serverless media + deploy-your-own; **Replicate** for the quick API path; **HF
Inference Endpoints** for an already-on-HF model. The worker contract: input (reference frame + 8-view turnaround +
motion spec + proxy/pose + weapon layer) → ComfyUI/animation model → candidate frames + masks + receipts
(seed/config/model/license). The service is commercial; the **output's license is the model's, not the platform's**.
→ Modal or RunPod-serverless for the heavy animation/edit graphs; keep the repo as source-of-truth.

**6. `combat-craft` — Combat animation craft (designed, not generated).** Attacks are authored to four beats —
**anticipation → active/hit frame → follow-through → recovery** — with the hit frame the clearest, most exaggerated
pose (10-frame slash budget). Key-pose-first authoring, readable silhouettes at thumbnail scale in all 8 directions,
hit-stop/freeze frames for impact, smears on fast arcs, slow-in/slow-out spacing, follow-through on secondary geometry,
clean idle loops, and **foot-contact discipline** (a locked contact beats a smooth slide). Grounded in Thomas &
Johnston (1981), Richard Williams (2001), Swink "Game Feel" (2008), and GDC craft talks.
→ Storyboard every roster attack to these beats before any rig/AI work; the hit frame is what motion-verify checks.

**7. `motion-verify` — Motion verification & QA (the admission gate).** Automatable checks: **weapon length/tip
continuity** (the §D drift detector — segment the weapon, bound length/angle variance), root/anchor stability,
foot-contact / no-slide (RAFT flow), **frame-to-frame face-identity drift** (ArcFace embedding distance — but
InsightFace weights are NC → LPIPS face-crop fallback for commercial use), temporal LPIPS/SSIM, optical-flow warping
error, FVD + SigLIP2 identity-to-reference, silhouette readability, and the **cross-family vision-LLM QA jury**
(reasoning-stripped, refute-by-default, 2-of-3 consensus — the studio's `_concept_vision_qa.py` pattern). Thresholds
are to-be-tuned on the captain set.
→ Assemble these into a hard accept/reject gate; a weapon-continuity fail blocks the sprite from shipping.

## Cross-KB seams (this KB points, never restates)

- **[sprites-knowledge](../../../sprites-knowledge/catalog/README.md)** — the static sprite the motion animates (its
  `animation-locomotion` lane's auto-rig/interpolation tools are superseded + deepened here).
- **[model-knowledge](../../../model-knowledge/catalog/README.md)** — model weights/licenses (`base_model_slug`).
- **[tensor-engine-knowledge](../../../tensor-engine-knowledge/catalog/README.md)** — rig-measured it/s + VRAM (`engine_recipe_ref`).
- **[blender-knowledge](../../../blender-knowledge/catalog/README.md)** — Blender 4.x rigging/render recipes.

## Verification

Every recipe was re-adjudicated by a cross-family PoLL jury of the biggest Ollama Cloud thinking flagships
(`deepseek-v4-pro` + `glm-5.2` + `minimax-m3` — disjoint families, reasoning-stripped, refute-by-default).
`verified=1` only where ≥2 jurors confirmed and none refuted; existence-refuted or ≥2-refuted recipes are flagged
`avoid` and kept visible; license over-claims are corrected to the most restrictive juror verdict. See
[`verification.md`](verification.md) for the per-lane tally, the refuted/flagged list, and license corrections.
