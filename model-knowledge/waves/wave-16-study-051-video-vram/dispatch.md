# Wave 16 — STUDY-051 VIDEO VRAM honesty

**Tip:** `bd38488`
**Constraints:** A14B-32GB invent: 0. Pocket 127 stays verified=0. Do not land GGUF Q4/Q6/Q8 GB labels as verified.

## Findings → recommendations
- Wan tiers + Alice distill + MobileWan 80GB honesty + KV ceilings.
- A14B I2V/S2V ≥80GB refuse · TI2V-5B ≥24GB · Hunyuan1.5 ≥14GB offload · LightX2V quant · LTX no GB.
- Hold refuse/offload≠fit/inherit; omit A14B-32GB invent + Pocket invent fail-transfers.

## Evidence
`/workspace/studio/research/STUDY-051/` five packs + research-raw.json
