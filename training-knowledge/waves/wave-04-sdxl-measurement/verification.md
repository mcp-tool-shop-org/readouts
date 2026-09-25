# Wave 4 — Verification receipt (measurement)

> The oracle is the rig + looked-at sample grids (not the study-swarm adversarial verifier) · 2026-06-06.

## Measured A/B table (SDXL, stdstyl, dim16/alpha16, 600 steps)

| config | it/s | s/it | peak VRAM | adapter |
|---|---|---|---|---|
| AdamW fp32 (#166 v2 ref) | 1.46 | 0.685 | 19.4 GB | 109 MB |
| AdamW8bit + cosine | 1.52 | 0.66 | 19.7 GB | 109 MB |
| Prodigy (lr=1.0) | 0.69 | 1.44 | 20.6 GB | 109 MB |
| LoRA (lycoris, +grad-ckpt) | 0.94 | 1.06 | 14.2 GB | 121.8 MB |
| DoRA (lycoris, +grad-ckpt) | 0.62 | 1.61 | 14.3 GB | 125.6 MB |
| LoKr (lycoris, +grad-ckpt) | 0.87 | 1.15 | 13.5 GB | **6.1 MB** |

_Note: lycoris runs are gradient-checkpointed (lower VRAM, slower it/s) so they are comparable to each other, not directly to the non-checkpointed AdamW/Prodigy rows._

## Quality (looked-at, 600 steps)

All configs bound the style on the subject-prior gradient ship > locomotive > portrait (the #165 base-bounds-the-style interaction). DoRA's ship was the crispest; LoKr matched LoRA quality at 1/20th the size. No saturated blue on any (SDXL base 1.0 ceiling).

## Provenance

5 rig runs on the RTX 5090, 2026-06-06. Every measured technique carries evidence_strength=measured-on-rig + the receipt + the looked-at sample grids in E:/AI/training/output/sample/. 3 wave-3 research techniques superseded.

