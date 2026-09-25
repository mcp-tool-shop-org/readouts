# Catalog — local generative-AI models

Generated from `models.db` · wave 18 · 2026-09-07. Narrative + re-download plan: [wave-01 dispatch](../waves/wave-01-foundation/dispatch.md). Verification receipt: [verification.md](../waves/wave-01-foundation/verification.md).

## Fastest commercial-safe re-download shortlist

Top `recommended`, commercial-`yes` picks per domain, priority order. `✓` = retrieval-verified this wave.

| Domain | ↓ | Model | License | VRAM | Game | Mkt | ✓ |
|---|---|---|---|---|---|---|---|
| Image — base models | 1 | [FLUX.2 [klein] base 4B](image-base.md) | Apache 2.0 | 13.0 | 5 | 4 | ✓ |
| Image — base models | 1 | [Qwen-Image-2512 (and base Qwen-Image)](image-base.md) | Apache 2.0 | 16.0 | 4 | 5 | ✓ |
| Image — base models | 1 | [Z-Image-Turbo (Z-Image family)](image-base.md) | Apache 2.0 | 16.0 | 4 | 4 | ✓ |
| Image — editing | 1 | [Qwen-Image-Edit-2511](image-edit.md) | Apache 2.0 | 6.0 | 5 | 5 | ✓ |
| Image — editing | 2 | [FireRed-Image-Edit-1.1](image-edit.md) | Apache-2.0 | 24.0 | 9 | 8 | ✓ |
| Image — control & utility | 1 | [Qwen-Image-ControlNet-Union (InstantX)](image-control.md) | Apache-2.0 (both ControlNet and Qwen-Image base) | 16.0 | 9 | 8 | ✓ |
| Image — control & utility | 1 | [ai-toolkit (Ostris) — LoRA trainer](image-control.md) | MIT | 10.0 | 9 | 7 | ✓ |
| Image — control & utility | 2 | [ControlNet Union SDXL 1.0 ProMax (xinsir)](image-control.md) | Apache-2.0 | 8.0 | 9 | 8 | ✓ |
| Video generation | 1 | [LightX2V Wan2.2 4-step Distill (LoRAs + merged models)](video.md) | Apache-2.0 | 16.0 | 5 | 5 | ✓ |
| Video generation | 1 | [Wan 2.2 (TI2V-5B + T2V/I2V-A14B)](video.md) | Apache-2.0 | 8.0 | 5 | 5 | ✓ |
| Video generation | 1 | [Wan2.2-Animate-14B](video.md) | Apache-2.0 | 16.0 | 5 | 4 | ✓ |
| 3D asset generation | 1 | [Hi3DGen (Stable3DGen)](3d.md) | MIT | 8.0 | 5 | 3 | ✓ |
| 3D asset generation | 1 | [TRELLIS.2-4B](3d.md) | MIT (model + code). Note: optional nvdiffrast/nvdiffrec deps are non-commercial NVIDIA license. | 24.0 | 5 | 4 | ✓ |
| 3D asset generation | 1 | [TripoSG](3d.md) | MIT | 8.0 | 5 | 3 | ✓ |
| Audio generation | 1 | [ACE-Step 1.5](audio.md) | MIT (code AND weights) | 6.0 | 5 | 5 | ✓ |
| Audio generation | 1 | [Chatterbox / Chatterbox Multilingual (Resemble AI)](audio.md) | MIT | 5.0 | 5 | 5 | ✓ |
| Audio generation | 1 | [DiffRhythm 2](audio.md) | Apache-2.0 | 8.0 | 5 | 5 | ✓ |
| Local LLM + vision | 1 | [CapRL-InternVL3.5-8B](llm.md) | Apache 2.0 | 16.0 | 5 | 2 | ✓ |
| Local LLM + vision | 1 | [Qwen3-VL (8B / 32B)](llm.md) | Apache 2.0 | 8.0 | 5 | 4 | ✓ |
| Local LLM + vision | 1 | [Qwen3.6-27B](llm.md) | Apache 2.0 | 18.0 | 5 | 5 | ✓ |
| Captioning & tagging | 1 | [JoyCaption Beta One](caption.md) | Apache-2.0 | 8.0 | 5 | 4 | ✓ |
| Captioning & tagging | 1 | [WD EVA02-Large Tagger v3](caption.md) | Apache-2.0 | 2.0 | 5 | 2 | ✓ |
| Captioning & tagging | 2 | [CapRL-InternVL3.5-8B](caption.md) | Apache-2.0 | 18.0 | 4 | 5 | ✓ |
| ComfyUI + workflows | 1 | [ComfyUI](comfy.md) | GPL-3.0 | 4.0 | 5 | 5 | ✓ |

## Domains

- [Image — base models](image-base.md) — Text-to-image base checkpoints (24 models)
- [Image — editing](image-edit.md) — Instruction / in-context image editing (10 models)
- [Image — control & utility](image-control.md) — ControlNet/IP-Adapter, inpaint, upscalers, detailers, LoRA training (11 models)
- [Video generation](video.md) — Text/image-to-video models (22 models)
- [3D asset generation](3d.md) — Image/text-to-3D mesh + texture (14 models)
- [Audio generation](audio.md) — Music, SFX/foley, TTS/voice (27 models)
- [Local LLM + vision](llm.md) — Ollama text/code/reasoning + vision/captioning (9 models)
- [Captioning & tagging](caption.md) — VLM captioners + booru taggers for dataset building (11 models)
- [ComfyUI + workflows](comfy.md) — ComfyUI runtime, custom nodes, workflow sources (1 models)

## Legend

- **↓** download priority (lower = grab first; derived from status + quality tier).
- **Cloud** (detail pages): Comfy Cloud feasibility — yes / partial / local / unknown (wave-6 axis; wave-7 entries are measured on-account).
- **Comm** commercial use: ✅ yes / ⚠ conditional (revenue or regional caps — read notes) / ⛔ no (non-commercial weights) / ? unknown.
- **Game / Mkt** fit 0–5 for game-asset production vs marketing/creative.
- **✓** retrieval-verified this wave (existence + license + specs). Blank/· = unverified lead.
- **VRAM** practical minimum in GB (quantized where noted); all picks target a 32 GB RTX 5090.
