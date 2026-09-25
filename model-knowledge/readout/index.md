# readouts — model-knowledge

> Verified knowledge base of the best local generative-AI MODELS per purpose (image / edit / control / video / 3D / audio / LLM / caption) for the RTX 5090 rig — commercial-license-first.
>
> **129 models · 126 verified · 553 sources · 19 waves · generated 2026-09-14.**  
> Decisive axis: commercial license (a LoRA/asset inherits its base model's license) + fits 32 GB VRAM.

## Domains

| Domain | Models | Verified | Top pick | License | Readout |
|---|--:|--:|---|---|---|
| Image — base models | 24 | 23/24 | FLUX.2 [klein] base 4B | commercial | [`readout-image-base.html`](readout-image-base.html) |
| Image — editing | 10 | 10/10 | Qwen-Image-Edit-2511 | commercial | [`readout-image-edit.html`](readout-image-edit.html) |
| Image — control & utility | 11 | 11/11 | ai-toolkit (Ostris) — LoRA trainer | commercial | [`readout-image-control.html`](readout-image-control.html) |
| Video generation | 22 | 21/22 | LightX2V Wan2.2 4-step Distill (LoRAs + merged models) | commercial | [`readout-video.html`](readout-video.html) |
| 3D asset generation | 14 | 14/14 | Hi3DGen (Stable3DGen) | commercial | [`readout-3d.html`](readout-3d.html) |
| Audio generation | 27 | 26/27 | ACE-Step 1.5 | commercial | [`readout-audio.html`](readout-audio.html) |
| Local LLM + vision | 9 | 9/9 | CapRL-InternVL3.5-8B | commercial | [`readout-llm.html`](readout-llm.html) |
| Captioning & tagging | 11 | 11/11 | JoyCaption Beta One | commercial | [`readout-caption.html`](readout-caption.html) |
| ComfyUI + workflows | 1 | 1/1 | ComfyUI | commercial | [`readout-comfy.html`](readout-comfy.html) |

## Install-first shortlist (recommended, by KB download priority)

1. **ACE-Step 1.5** (Audio generation) — commercial
2. **ai-toolkit (Ostris) — LoRA trainer** (Image — control & utility) — commercial
3. **BS-RoFormer (Band-Split RoFormer)** (Audio generation) — conditional
4. **CapRL-InternVL3.5-8B** (Local LLM + vision) — commercial
5. **Chatterbox / Chatterbox Multilingual (Resemble AI)** (Audio generation) — commercial
6. **ComfyUI** (ComfyUI + workflows) — commercial
7. **DiffRhythm 2** (Audio generation) — commercial
8. **FLUX.2 [klein] base 4B** (Image — base models) — commercial
9. **Hi3DGen (Stable3DGen)** (3D asset generation) — commercial
10. **Hunyuan3D-2.1** (3D asset generation) — conditional
11. **JoyCaption Beta One** (Captioning & tagging) — commercial
12. **LightX2V Wan2.2 4-step Distill (LoRAs + merged models)** (Video generation) — commercial
13. **LTX-2.3 (LTX-2 family, 19B)** (Video generation) — conditional
14. **Mel-Band RoFormer (separation architecture + KimberleyJSN vocal checkpoint)** (Audio generation) — commercial
15. **Qwen-Image-2512 (and base Qwen-Image)** (Image — base models) — commercial
16. **Qwen-Image-ControlNet-Union (InstantX)** (Image — control & utility) — commercial
17. **Qwen-Image-Edit-2511** (Image — editing) — commercial
18. **Qwen3-VL (8B / 32B)** (Local LLM + vision) — commercial

## Go deeper

- **Per-domain readout:** `readout-<slug>.html` — filterable table + sources + verify trail
- **Wave dispatches** (research log): `waves.md` / `waves.html`
- **Verification receipt** (trust trail): `verification.md` / `verification.html`
- **Query the DB:** `models.db (views v_recommended, v_best_for; FTS models_fts)`
- **Resolve via loadout:** `ai-loadout resolve --project ./model-knowledge`
- **Programmatic map:** `index.json`

## Provenance

Every fact carries a **wave id** and a **verified** flag; sources are retrieval-checked by a different-family verifier. 19 waves; 126/129 models verified.
