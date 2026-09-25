# Wave 8 — STUDY-049 hw-measurement honesty

**Tip:** `1bdd509`
**Constraints:** Axis invented: 0. Numbers invented: 0. Do not invent GB/s, tok/s, VRAM, or equate sm_100↔sm_120.

## Findings → recommendations
- sm_100≠sm_120 · Pro 6000 Gen5 · theoretical≠effective · 5090 sm_120 named.
- CC 10.0≠12.0 · bandwidthTest/nvbandwidth · NVML · WSL pin limited.
- Hold SPEC/fio/CUDA/nvbandwidth; omit invent tok/s + equate-sm fail-transfers.

## Evidence
`/workspace/studio/research/STUDY-049/` five packs + research-raw.json
