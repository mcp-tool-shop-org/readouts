# Wave 4 — SDXL measurement (optimizer + network-type receipts)

> Measurement dispatch · 2026-06-06 · training-knowledge KB · the GPU pass.

**Goal:** turn the wave-3 reproduced-from-source SDXL claims into measured-on-rig receipts by actually running them on the RTX 5090.

**Method:** 5 real kohya/sd-scripts training runs on the stdstyl benchmark set (16-img cyanotype, dim16/alpha16, TE on, 600 steps unless noted), each capturing steady-state it/s + a 1 Hz peak-VRAM sample + a held-out 3-subject sample grid (ship/locomotive/portrait) that was LOOKED AT. The 'verifier' here is the rig itself + direct image inspection — not the study-swarm adversarial panel.

**Runs:** Prodigy @400 (Run 1), Prodigy @600 matched (Run 1b), AdamW8bit+cosine @600 (Run 2), and a gradient-checkpointed 3-way LoRA/DoRA/LoKr (Run 3, after a first attempt spilled VRAM without checkpointing).

## Four wave-3 claims corrected/confirmed by measurement

| claim (wave-3) | measured |
|---|---|
| Prodigy 'slightly higher state' | **~1.8-2.2x/step + ~1.2 GB** — convenience optimizer; breakeven S>=1 |
| AdamW8bit 'halves VRAM -> more headroom' | **no LoRA saving** (19.7 vs 19.4 GB); ~4% faster; win is full-FT-only |
| DoRA 'near-free quality upgrade' | **+52% train time** (1.61 vs 1.06 s/it), marginal quality — situational |
| LoKr 'capacity/efficiency' | **confirmed: 6.1 MB adapter (~20x smaller), comparable quality** |

**Superseded** (provenance kept via superseded_by): prodigy-adaptive-lr-sdxl-style-lora, adamw8bit-cosine-warmup-sdxl-lora, network-type-choice-locon-lokr-dora-sdxl-style.

**Env facts earned:** lycoris.kohya needs --gradient_checkpointing on 32 GB (27.7 -> 14.5 GB; DoRA spilled to 33 s/it without it, a ~2-hour detour); this sd-scripts has no native DoRA (routes via lycoris-lora 3.4.0, uv-installed --no-deps to protect torch cu130). SDXL base blue-ceiling (#165) held across all runs.

