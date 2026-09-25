# Wave 5 — Qwen multi-ControlNet addendum (2026-06-26)

**Not a full study-swarm sweep — a targeted 2-model addendum** surfaced by the `cloud-quality-levers` research workflow
(run `wf_7dd729e6-761`) while scoping the move of the 3D pre-render RESTYLIZE step onto an 80GB cloud GPU.

## Why these two
The restylize lever research (Lever B — ControlNet) found two **commercial-safe (Apache-2.0) Qwen-Image ControlNet unions**
that post-date wave-4 and were not yet in the KB. Both were WebFetch-confirmed by the workflow's adversarial source
verifier (the same pass that caught a fabricated `qwen_image_fp8_scaled` model file and the misattributed BideDPO claim,
and established the load-bearing correction below).

| Model | Status | Note |
|---|---|---|
| `alibaba-pai/Qwen-Image-2512-Fun-Controlnet-Union` | recommended | Multi-condition union for Qwen-Image-2512; the practical canny+depth path for the mesh-AOV restylize. Repo slug casing: `Fun-Controlnet-Union` (lowercase n). |
| DiffSynth In-Context-Control-Union (modelscope/DiffSynth-Studio) | situational | Second commercial-safe Qwen multi-control option; not yet measured on-rig, less turnkey in ComfyUI. |

## Load-bearing correction recorded with this wave
There is **NO commercial-safe NORMAL ControlNet on the Qwen stack** — the InstantX / alibaba-pai / DiffSynth unions support
canny / soft-edge / depth / pose, but **not normal**. A "canny+depth+normal from the real mesh" restylize is therefore
**canny+depth only** on Qwen; a normal leg would require switching families to the SDXL xinsir Union ProMax (id 11).

## Provenance
- Verifier: the cloud-quality-levers workflow's per-lever adversarial source-checker (WebFetch as retrieval oracle), 2026-06-26.
- VRAM figures are base-family-inferred (same 20B Qwen base as InstantX Union id 10), not separately on-rig measured — flagged in each `verify_note`.
- Full research synthesis lives in memory: `cloud-restylize-quality-levers.md`.
