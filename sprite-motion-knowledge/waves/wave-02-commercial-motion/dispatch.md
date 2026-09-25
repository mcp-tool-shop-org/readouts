# Wave 02 — Commercial motion sources & data

**KB #9 `sprite-motion-knowledge` · dispatched 2026-06-24 · 6 parallel lane agents (Sonnet), web-grounded + license-verified.**
Verification receipt (cross-family PoLL jury): [`verification.md`](verification.md). Raw verified output: [`research-raw.json`](research-raw.json).

Wave 1 catalogued the animation **tools**. Wave 2 catalogues the **content/data** those tools consume — *where shippable
character motion comes from, what its licence permits for a commercial Steam game, and how to get it onto the studio's
rigs.* This is a **licence-decisive** wave: the single load-bearing field per recipe is an accurate `commercial_use`,
and the cross-family jury's licence check is the point.

## The one rule that governs the wave

> **Trace the data, not the code.** An MIT/Apache *code* licence never makes the *weights* or *dataset* commercial.
> Academic mocap is non-commercial, and any model trained on it (or emitting SMPL parameters) inherits the
> restriction. The `motion-licensing` lane is the doctrine; every other lane is an application of it.

## The 6 lanes — findings → recommendation

**1. `mocap-libraries` — commercial ready-made packs.** Commercial-clean for in-game use: **Mixamo** (royalty-free, no
raw redistribution, no ML-training, humanoid-only), **Reallusion ActorCore**, **Fab/Epic** marketplace clips, on-demand
mocap studios. Conditional: **Rokoko** (subscription-lock unclear), **MoCap Online** (explicitly forbids AI processing —
so wave-1 AI tools can't legally touch those clips), **Cascadeur Indie** (revenue cap; but zero humanoid-mis-fit since
the artist authors the rig), **Truebones** (provenance controversy — greybox only without chain-of-title). → Mixamo +
ActorCore + Fab for the human cast; Cascadeur for clean authored polish.

**2. `mocap-datasets` — open datasets + the licence cascade.** Only two commercial-clean wins: **100STYLE (CC BY 4.0)**
= best free human-locomotion source, and **Truebones Zoo (~$99, royalty-free, 75+ animals)** = the creature source for
the non-humanoid roster. Everything else is research-only — **AMASS is the root poison; HumanML3D inherits it directly,
Motion-X adds a viral share-alike, LAFAN1 a NoDerivatives block, BANDAI-Namco is the "sounds permissive, actually NC"
trap, Human3.6M is access-gated.** → Buy Truebones Zoo for creatures; 100STYLE for human locomotion; avoid the rest for
shipping.

**3. `motion-gen` — text-to-motion (blocked).** All 7 verified models (MDM, MoMask, T2M-GPT, MLD, MotionGPT,
OmniControl, FlowMDM) are commercial-blocked: they train on AMASS-derived HumanML3D and emit SMPL — both non-commercial
— so MIT code is irrelevant. An 8th "clean-data NVIDIA" candidate the research agent presented as the lone shippable
exception was **fabricated (fake arXiv id, repo, datasets, authors) and REFUTED by the cross-family jury (2/3
`not-found`) — dropped** (see [`verification.md`](verification.md)). → There is **no verified commercially-clean
generated-motion path**; use generated motion for prototyping/blocking ONLY, never shipping.

**4. `driving-video` — driving/reference video for pose-transfer.** The clean default is **own footage** (phone/webcam +
the studio's own actor) → extract a pose signal with **DWPose / MediaPipe (Apache-2.0)** → drive a wave-1 pose model.
Rotoscoping own footage is the oldest clean technique. Avoid: stock video (Shutterstock/Getty prohibit AI use),
OpenPose (CMU's $25k/yr commercial fee), Mixamo-as-driving (Adobe bans AI driving use). → Shoot your own; it sidesteps
the derivative-work question entirely.

**5. `retarget` — onto the stylized / non-humanoid rigs.** **Auto-Rig Pro Remap** is the recommended paid Blender path
(Mixamo/Rokoko presets + IK feet); **Rokoko's addon (LGPL-3.0, free)** and Blender's **native bone-constraint** retarget
(the zero-assumption fallback) cover the rest; **UE5 IK Retargeter** is the engine-side path (EULA royalty). The honest
finding for the **15-exotic-species** roster: retarget saves time proportional to how humanoid the target is — for
tortle/kenku/sahuagin it gives rough blocking at best. The policy answer is the **non-humanoid additive-layer strategy**:
retarget the shared humanoid bones, hand-author tails / wings / fins as additive NLA on top. Always finish with a
**foot-IK lock** before the 8-camera ortho render. → Auto-Rig Pro for humans; additive-layer + hand-author for exotics.

**6. `motion-licensing` — the governing doctrine.** Eight reusable rules: data-licence-governs-not-code; royalty-free ≠
do-anything (Mixamo); academic = non-commercial; the **AMASS downstream-poison** rule; the **SMPL/SMPL-X body-model
poison** (research-only from Max Planck — a hidden trap even when the motion data is clean, unless you hold a Meshcapade
commercial licence); CC variants (CC0/CC-BY shippable, NC/ND blocked); engine-marketplace grants (Fab/Unity allow
in-game, exclude raw redistribution + ML-training); and the **safe-harbour recipe** — CMU + CC0/own-capture + no SMPL
intermediate + a chain-of-title registry. → This lane is the checklist every motion asset passes before it ships.

## The commercial-clean motion stack (the wave's synthesis)

```
own-mocap / own-footage  +  100STYLE (CC-BY, human locomotion)  +  Truebones Zoo (paid, creatures)  +  Mixamo (in-game-only, human)
        ↓ retarget (Auto-Rig Pro / native; additive-layer + hand-author for exotic species)  ↓ foot-IK lock
        → bake to action → 8-camera ortho render → (wave-1) repaint → sprite sheet → verify
AVOID for shipping: generated motion (AMASS/SMPL poison), all academic datasets, stock-video-as-driving.
```

## Cross-KB seams

Complements wave 1 (the animation tools/models that consume this data) and points at `blender-knowledge` (the retarget
+ render mechanics), `model-knowledge` (any model weights), never restated. Verification: cross-family PoLL jury
(`deepseek-v4-pro` + `glm-5.2` + `minimax-m3`) — see [`verification.md`](verification.md) for the per-lane tally, the
refuted/flagged list, and licence corrections.
