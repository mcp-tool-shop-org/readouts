# Wave 08 — Qwen-Image LoRA measurement (rig wave, 2026-06-09)

A measurement wave (same class as waves 04/06), not a study-swarm: the source of truth is
the rig, not retrieved literature. Opens the **`diffusion-qwen-lora` lane** — the KB's first
Qwen-Image-as-training-base rows (wave-7's qwen mentions were klein's Qwen3 *encoder*).

## What was measured

The studio's Phase-1 style-LoRA run (`tallow_fen_style_v1`) end-to-end on the RTX 5090:

1. **The 32GB recipe** — AI-Toolkit uint3+ARA + qfloat8-TE + low_vram on the 20B DiT:
   3.6–4.7 s/it, ~18GB peak, ~2h10m / 2000 steps; native ComfyUI `LoraLoaderModelOnly` load;
   inference strength 1.5; **best checkpoint at 62% of the run**, caught by CMMD + embedding-cloud
   geometry where raw CLIP-sim alone would have shipped the overfit final checkpoint.
2. **Descriptor-noun literalization** — a 3-wave A/B/B′ (86 looked-at images): a style-descriptor
   noun ("lantern light") materialized as a prop in 58/58 neutral images, negatives powerless;
   naming the light by material ("tallow light") fixed it 0/28.
3. **Dataset-mode dominance** (recorded as a failure row on #1) — 2 off-canon exemplars in an
   8-image class beat 6 on-canon ones + prompt negatives at inference; per-creature canon needs
   dataset-level enforcement. The v2 re-curation + retrain is in flight; its outcome amends this wave.

## Provenance

Run config `E:/AI/training/tallow_fen_style_v1.yaml`; dataset packages `tp-20260609-201716-4744`
(v1) / `tp-20260610-030434-413e` (v2); A/B + probes + strength sweep under `E:/AI/training/ab_tallow/`;
trajectory baseline in `vector-caliper/baselines/qwen-lora-tallow-fen-v1.json`. PRs:
style-dataset-lab #25 (merged), studio kickoff `KICKOFF-qwen-style-lora.md` Phase 1.

## Verification

Verifier = the rig + the eval harness + a full human looked-at pass (every generated image was
opened). Gate families differ from the generator (SigLIP2 probes, CLIP ViT-B/32 metrics). No
study-swarm citation panel was run — `evidence_strength: measured-on-rig` throughout, with
receipts as sources.
