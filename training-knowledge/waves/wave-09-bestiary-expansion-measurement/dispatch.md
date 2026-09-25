# Wave 09 — Qwen-Image bestiary-expansion measurement (rig wave, 2026-06-17)

A measurement wave (same class as 04/06/08), not a study-swarm: the source of truth is the rig.
Continues the **`diffusion-qwen-lora`** lane opened in wave-08 with the `tallow_fen_style_v3`
bestiary-expansion run — the studio's first multi-class style-LoRA scale-up and its first
TRELLIS turnaround stress-test on a winged+headed creature.

## What was measured

The studio grew the Tallow Fen bestiary 3 → 8 classes (canon-first), built dataset v3, retrained
the house style LoRA on the **identical pinned recipe** (single lever = dataset only), proved each
class, and ran TRELLIS turnarounds.

1. **Shape-anchored img2img for silhouette-hard classes** — for creatures whose canonical
   silhouette has no limbs/head/face (Rust Boil limbless dome, Peat Dredge headless hump, Mire Maw
   apex cone), Qwen-Image's base silhouette prior **overrides the text prompt even with the trained
   style LoRA loaded**: txt2img grows limbs/snouts/skulls (Boil 0/24, Maw 2/32 on-canon). A crude
   PIL silhouette mock (master-palette colour blocks) → **no-LoRA** Qwen img2img at denoise 0.6–0.75
   imposes the silhouette txt2img can't hold (Boil geometry 8/8). The same 3 classes that needed i2i
   to build the DATASET need i2i (or low strength) to PRODUCE — the LoRA supplies material/surface/
   style, the base prior wins on shape. Their production lane is i2i/turnaround, not bare txt2img.

2. **Clean dataset = no late embedding-cloud collapse — 3rd cross-run confirmation.** Single-lever
   retrain (only the dataset changed) on the pinned recipe. v3 anisotropy peaks 13.27@1500 then
   **recovers** to 11.55@2000, effdim steady ~6.9; the only run that collapsed late (v1, aniso
   8.2→12.5) is the one with off-canon exemplars in a class. Ship-ckpt picked by CMMD +
   embedding-cloud geometry (1750 @1.5), never CLIP-sim alone. vector-caliper baseline #3.

3. **TRELLIS turnaround fragility for winged+headed creatures, and its concept-stage fix.** The Fen
   Pall (thin wings-on-bone-struts + a head) produced a strutty, skull-prone mesh: side/rear views
   erupted into skull/skeleton/gargoyle-face under restylize, and SigLIP2 *preferred* the stylized
   skull (palette match) — eyes were the stricter gate. Reroll at low denoise could not fix it (the
   drift is mesh-level). Fix is upstream at the CONCEPT stage: a fuller **continuous** membrane
   (struts hidden) + a large round featureless head + the drift attractors (skull/face/sockets/
   skeleton/spindly-limbs) in the concept-stage **negative**. A folded/perched pose over-corrects
   and kills the winged identity (a mossy blob). Result after re-mesh: Pall 8/8; Brood 8/8; Rust
   Boil 8/8 (a limbless dome carried clean through mesh → 8-dir → restylize on every angle).

## Provenance

Run config `E:/AI/training/tallow_fen_style_v3.yaml` (identical pinned recipe vs v1/v2); dataset
package `tp-20260617-132101-7bba` (99 records, 8 classes); A/B + SigLIP2 probes + strength sweeps
under `E:/AI/training/ab_tallow/v3_*`; trajectory baseline
`vector-caliper/baselines/qwen-lora-tallow-fen-v3.{json,svg}`; turnarounds under
`E:/AI/training/p2_turnaround_v3/`. PRs: style-dataset-lab #27, studio
`KICKOFF-bestiary-expansion.md` (COMPLETE).

## Verification

Verifier = the rig + the eval harness + a full human looked-at pass (every generated image opened,
including every reroll candidate). Gate families differ from the Qwen generator (SigLIP2-so400m
contrastive canon probes, CLIP ViT-B/32 cloud metrics). `evidence_strength: measured-on-rig`
throughout; receipts as sources. A measured limitation is recorded honestly: SigLIP2 under-penalizes
a face on an otherwise-correct silhouette (it weights global palette/style), so the eyes carry the
canon-veto on focal-feature drift.
