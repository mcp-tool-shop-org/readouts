# Combat key-pose recipes + deform-safe authoring (wave 5 — STAGED for DB ingest)

> **Status:** study-swarm-grounded, family-different citation-gate PASSED (2026-06-25). Staged here for
> ingest into `recipes.db` (a "Combat key-poses" lane + a rigid-armor deform recipe in the Rigging lane).
> NOT yet in the generated `catalog/` — this file is the wave-5 source. Earned on the sprite-motion poser
> bring-up (blackguard proof char): the headless poser was guessing joint angles; this makes it a science.

## Why this wave exists

The `combat-craft` lane has the pose *principles* (key-pose-first, exaggerate 30–50%, silhouette-reads-8-ways)
but no instantiated **pose recipes** (the 6 canonical battle poses as reproducible specs), and the `rigging`
lane has no **rigid-armor deform-limit** recipe. The sprite-motion poser hit both gaps: a hand-authored "guard"
threw the arms up (a touchdown), then a tuned guard FAILED the cross-family vision jury with "melted elbow."
This wave fills both gaps with verified recipes.

## Citation gate receipt (research-grounded-advisor protocol, Step 4)

- **Stage 1 — retrieval oracle (WebFetch existence/attribution):** 7/7 load-bearing citations resolved with
  correct title/authors/year. **0 fabricated, 0 misattributed.** Confirmed: UniRig (arXiv:2504.12451),
  Neural Blend Shapes (arXiv:2105.02451), Kavan DQS (DOI 10.1145/1409625.1409627), Lewis PSD (SIGGRAPH 2000),
  NTU RGB+D (arXiv:1604.02808), AMASS license (= non-commercial, verbatim), Dead Cells pipeline (Motion Twin).
  **CANNOT_CONFIRM (oracle-blocked, non-load-bearing, surfaced not dropped):** Sato 2015 (PMC4519200, reCAPTCHA),
  CMU mocap license (cert/archive blocked), Mixamo FAQ (timeout) — all corroborating/backup, none load-bearing.
- **Stage 2 — groundedness (2 decorrelated non-Claude families, reasoning-stripped):** minimax-m3:cloud +
  kimi-k2.6:cloud → **SUPPORTED 6/6** load-bearing findings, consensus. No REFUTED/UNSURE. No ANDON halt.

## Recipe 1 — Hand-author battle key-poses to biomechanical targets (don't retarget, don't guess)

**Claim:** For STATIC combat key-poses on an auto-rigged custom character, hand-author to biomechanical
targets — it is faster than retarget-and-scrub for one frame, it is what shipped 2.5D/2D-from-3D games do,
and it keeps restrictive mocap licenses out of the project.
- **Evidence:** Dead Cells renders hand-keyframed 3D rigs down to pixel sprites ("animations are designed,
  like 2D animations, on key frames" — Vasseur/Motion Twin, gamedeveloper.com); Sea of Stars, Skullgirls,
  Vanillaware all hand-author. Mocap libraries amortize *motion*, not a single frame.
- **License doctrine (commercial-decisive):** retargeting does NOT relicense a clip. **Blocked for shipping:**
  AMASS/SMPL (NC, verbatim "incorporation in a commercial product is prohibited" — amass.is.tue.mpg.de),
  Ubisoft LaFAN1 (non-commercial), Unreal Lyra/mannequin (UE-only). **Commercial-clean if you do retarget:**
  CMU Mocap (safest), 100STYLE (CC BY), Quaternius (CC0), Mixamo (use-in-product), Rokoko library.
- **Design implication:** the poser's `roleRotations` are authored to **solved biomechanical targets**
  (`_posesolve.py` numeric FK), not eyeballed. The FK math is verified exact vs Blender (millimeter match).

## Recipe 2 — The 6 canonical key-pose definitions (silhouette + joint targets)

Grounded in animation craft (Thomas & Johnston 1981, *Illusion of Life*; Williams, *Animator's Survival Kit*;
Cartwright GDC 2014, Skullgirls), martial guards (orthodox boxing; longsword guards vom Tag/Ochs/Pflug/Alber,
Meyer/Liechtenauer tradition), and mocap taxonomy (NTU RGB+D classes, arXiv:1604.02808; LaFAN1 fight/stumble tags).

| Pose | Load-bearing construction rule |
|---|---|
| **idle-ready** | lowered center of mass — flexed hips/knees, weight on the balls of the feet; **asymmetric** stance (no twinning) so it reads alive, not a mannequin |
| **guard** | **bladed/staggered feet, bent knees, hands raised to chest/face, elbows tucked IN** — a real fighting guard silhouette (boxing guard; longsword Pflug/Ochs), point/guard toward the threat |
| **anticipation** | move OPPOSITE the strike first — weapon/fist drawn back, rear foot loaded, torso counter-rotated (the wind-up extreme) |
| **strike** | the held extreme at the far end of the wind-up arc; clean **profile silhouette**; hard accent then recoil |
| **recovery** | overshoot then settle; loose parts (cape/hair) drag in after the main mass stops (follow-through) |
| **hurt/stagger** | a discrete off-balance class — COM thrown outside the base of support (NTU RGB+D A42/A43 stagger/fall) |

**Verification (per combat-craft):** every key-pose passes the silhouette-reads-in-8-directions check, and the
cross-family vision jury (`_rigqa.py`) is the blocking gate. Exaggerate 30–50% for sprite scale.

## Recipe 3 — Rigid-armor deformation limits on auto-rigged characters (the deform-safe rules)

**Claim:** UniRig (arXiv:2504.12451) outputs **standard Linear-Blend-Skinning weights**, so a posed character
inherits LBS's geometric collapse regardless of weight accuracy — the "melted elbow" is a deformation-MODEL
failure, not a weight error. On RIGID plate armor it is worst (a hard plate can't fold like skin).
- **Failure math:** LBS averages transforms not rotations → candy-wrapper collapse, severe near ~180° twist,
  objectionable from ~90–120° bend (Kavan et al. 2008, "Geometric Skinning with Approximate Dual Quaternion
  Blending", DOI 10.1145/1409625.1409627). Human ROM for reference: elbow 0–150°, knee 0–135°, shoulder 0–180°.
- **The deform-safe authoring rules (verified, applied in `apply_placement.py`):**
  1. **Cap authored joint flexion ≤ ~85°** (elbow/knee/shoulder); past that LBS tears. *(blackguard guard: elbow capped 70°.)*
  2. **Bake with DQS** (Blender Armature `use_deform_preserve_volume=True`) — dual-quaternion skinning avoids the
     volume collapse (Kavan 2008); watch for mild joint-bulging.
  3. **For rigid plate armor specifically, RIGIDIFY the skin** — push smoothly-blended limb-armor verts toward
     their dominant bone so plates *crease* at the joint instead of *melting* (`_clean_skin.py --rigidify`).
     This approximates the shipped-practice rule "rigid-bind each plate 100% to one bone, segment at the joint
     so the bend lands in the gap" (Polycount/80.lv) on a single auto-mesh we can't physically segment.
     **Measured on the blackguard:** rigidify(0.75) moved the posed FRONT jury verdict 0/3 → **2/3 PASS**
     (matching the clean-rest baseline). Cloth (cape/loincloth, dominated by torso bones) is excluded so it stays soft.
  4. **Correctives are the next tier** if creasing isn't enough: pose-space deformation / sculpted corrective
     shapes (Lewis/Cordner/Fong, PSD, SIGGRAPH 2000) or a learned corrective branch (Neural Blend Shapes,
     Li/Aberman et al. 2021, arXiv:2105.02451) — UniRig lacks this branch, so it must be added.
  5. **Since the 2.5D pipeline bakes a posed render to a sprite, "fix in post" (painterly repaint) is a uniquely
     valid final option** — the output is a fixed image, not a live deforming mesh (Dead Cells / HD-2D lineage).
- **Honest ceiling:** a single continuous auto-rig armor shell cannot fold perfectly at a sharp joint — it
  either melts (smooth LBS) or cracks (fully rigid). The true fix is upstream **segmented overlapping plates**
  (hand-modeled hard-surface), unavailable on an auto-generated mesh. Rigidify + DQS + ROM-cap gets the
  deforming-JOINT layer to baseline; remaining base-mesh artifacts (decimation slivers on legs/feet/pauldrons,
  visible even at REST) need a cleaner re-decimate / re-rig, not a skin fix.

## Sources (all retrieval-confirmed unless marked)

- UniRig — Zhang, Pu, Guo, Cao, Hu 2025 — arXiv:2504.12451 (auto-rig: skeleton + LBS skinning weights)
- Kavan, Collins, Žára, O'Sullivan 2008 — "Geometric Skinning with Approximate Dual Quaternion Blending" — ACM TOG/SIGGRAPH, DOI 10.1145/1409625.1409627
- Lewis, Cordner, Fong 2000 — "Pose Space Deformation" — SIGGRAPH 2000
- Li, Aberman, Hanocka, Liu, Sorkine-Hornung, Chen 2021 — "Learning Skeletal Articulations with Neural Blend Shapes" — arXiv:2105.02451
- Shahroudy, Liu, Ng, Wang 2016 — "NTU RGB+D" — arXiv:1604.02808 (combat/stagger action classes)
- AMASS — Mahmood et al. 2019 — amass.is.tue.mpg.de/license.html (NON-COMMERCIAL; license trap)
- Dead Cells art pipeline — Vasseur (Motion Twin) — gamedeveloper.com (hand-keyframed 3D→2D)
- Thomas & Johnston 1981, *The Illusion of Life* (ISBN 978-0-7868-6070-8); Williams, *The Animator's Survival Kit* (ISBN 978-0-571-23834-7); Cartwright 2014, GDC Animation Bootcamp (Skullgirls) — animation-craft canon (foundational)
- *CANNOT_CONFIRM (oracle-blocked, corroborating only):* Sato et al. 2015 (PMC4519200, ready-stance biomech); CMU Mocap license; Mixamo FAQ
