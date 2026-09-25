# Wave 3 — Verification receipt

Same method as waves 1–2 (reasoning-stripped adversarial verifier + `WebFetch` retrieval oracle; same-family this wave, family-different `prism`/`roleos` path still the planned upgrade).

## Verdict distribution

**21 models · 15 `confirmed` · 6 `confirmed-with-fixes` · 0 `unverified` · 0 `refuted`.** Commercial split: **11 yes / 6 conditional / 4 no**.

## Material catches

| Item | Catch |
|---|---|
| **HiDream-E1 / E1.1** | Transformer weights MIT, but it ships a **Llama-3.1 text encoder under the Llama 3.1 Community License** — so commercial use is *conditional*, not clean Apache/MIT. |
| **FLUX.2 klein** | Ships **two sizes under two licenses**: klein **4B = Apache** (commercial-safe), klein **9B = FLUX Non-Commercial**. FLUX.2-dev also non-commercial. Canonical name is "FLUX Non-Commercial License". |
| **Mel-Band / BS-RoFormer** | Code is MIT, but **checkpoint licenses vary** — KimberleyJSN Mel-Band vocal = MIT (use this for commercial); viperx BS-RoFormer checkpoints are license-unverified → conditional. |
| **Woosh (Sony AI SFX)** | Weights **non-commercial**; release date corrected to **March 2026** (not April). |
| **Phr00t/WAN2.2-14B-Rapid-AllInOne** | Real + Apache-tagged, but a **deprecated** community merge — prefer the official Wan2.2 + LightX2V route. |
| **Qwen-Image-Edit-2509** | Apache (clean), but **superseded** by 2511 — kept as a documented fallback. |
| **CapRL-InternVL3.5-8B** | Weights Apache (Qwen3 base, no Qwen-license inheritance); its **CC-BY-NC training dataset does NOT bind** users of the released weights or the captions they generate. |

## Currency flags

`superseded` / `deprecated`: Qwen-Image-Edit-2509 (→ 2511), Phr00t Rapid merge (→ official Wan2.2 + LightX2V), HiDream-E1-Full (→ E1.1).

## Wave-4 candidates (queue largely drained)

The wave 1–2 backlog is essentially cleared. Remaining narrow items:

- **audio:** SCNet / SCNet-large (top multi-stem separator) · MVSep / UVR5 (end-user separation front-end)
- **video:** Wan2.2-Fun-Control / Control-Camera · QuantStack GGUF repos for VACE-Fun
- **image-base:** FLUX.2 klein official fp8 / nvfp4 quant repos · klein 9B non-distilled "base" line
- **comfy:** comfyui_controlnet_aux (Fannovel16) preprocessor pack — *(note: already partly covered as "ControlNet-aux" in wave 1; confirm the exact repo row)*

> Most other verifier "missing" items (Demucs, JoyCaption, Florence-2, FLUX.1-Kontext, Step1X, OmniGen2, Wan-Animate, Impact/Inspire packs) are **already cataloged** in earlier waves — surfaced again only because each wave's verifier sees one lane, not the whole DB. A wave 4 is optional; the catalog is now broad + deep across all 9 domains.
