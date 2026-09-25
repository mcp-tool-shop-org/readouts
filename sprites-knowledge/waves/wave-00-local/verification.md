# Wave 0 — Verification receipt

**Verifier note:** This wave's evidence is **measured-on-rig by direct execution + look-at-output**, not citation. The decorrelating element is the rig itself (the run either produced the GLB/sprites at the stated VRAM/time or it didn't) plus the look-at-images discipline (every GLB and sprite set was opened and judged from 8 angles, not described from numbers).

## What backs each `verified = 1`
| Recipe | Receipt |
|---|---|
| trellis2-4b-rtx5090-image-to-glb | 512 + 1024_cascade runs; GLBs (35.9 / 38.3 MB) rendered + looked-at from 8 angles |
| trellis2-1024-cascade-vs-512-thin-features | side-by-side 512 vs 1024 renders, looked-at |
| trellis2-skip-v1-cleanup-ovoxel-is-clean | watchdog `_watchdog_KILL.log` RAM 99% during cleanup; `--no-cleanup` re-run completed 159.5s |
| sprite-pipeline-trellis-v3-end-to-end | `pipeline.py --backend trellis_v3` produced 8 sprites + contact sheet |
| blender-headless-8dir-camera-parented-rig | bpy API probe on Blender 5.0.1 (engine/AgX/glTF all valid); 8 views rendered |
| tonemap-per-character-value | 4-variant (AgX±/Standard/Filmic) render compared + looked-at |
| studio-hdri-ambient-fill | rendered with + without the HDRI, looked-at |
| lanczos-512-to-64-foot-anchored | 8× 64px sprites + contact sheet, looked-at |

## External sources
arXiv:2512.14692, github.com/microsoft/TRELLIS.2, huggingface.co/microsoft/TRELLIS.2-4B, huggingface.co/ZhengPeng7/BiRefNet, polyhaven.com/a/studio_kontrast_04, docs.blender.org, pillow.readthedocs.io — all real, public, resolving as of 2026-06-07.

## Caveat
These numbers are this rig (RTX 5090, Win11, the exact env in `measured_conditions`). VRAM/time will differ on other hardware. Allocator-peak (3.4–3.5 GB) is the PyTorch delta, not total process VRAM (~15–16 GB with weights).
