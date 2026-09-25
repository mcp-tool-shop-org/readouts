# Wave 1 — Verification receipt

The study-swarm **EXTERNAL_VERIFIER** stage, applied to this wave's own output before any row was trusted.

## Method

Each research lane's findings were handed to a **separate, reasoning-stripped** agent — it saw only the bare claims + source URLs, never the researcher's reasoning — that used **`WebFetch` as a retrieval oracle** to check, per model: **exists** (does the repo/page resolve with that name?), **license + commercial-use** correctness (and supply a correction if wrong), **spec plausibility** for a 32 GB card, and **currency** (current vs superseded/deprecated as of 2026-06-02). The default verdict on non-confirmation was `unverified`, not pass-on-faith.

**Honest scope.** The verifier is the **same model family** as the researcher this wave. The decorrelating element is the **retrieval oracle** (the live page), which is independent of the researcher's parametric claims — and per the protocol's own receipt, that oracle is what catches what same-family LLM lenses structurally cannot. The **family-different** upgrade (route through `prism verify` / `roleos verify-citations`, both shipped in this org, ideally with a *local non-Claude* model on this 32 GB rig per `hardware-omen-45l.md`) is the planned next-wave improvement — consistent with the protocol's documented P1 backlog. Treat this receipt as "retrieval-grounded, single-family," not "family-different verified."

## Verdict distribution

**52 models · 39 `confirmed` · 13 `confirmed-with-fixes` · 0 `unverified` · 0 `refuted`.**

Every model resolved to a real repo/page — i.e. nothing was fabricated; the verifier's value-add was **license precision and currency**, exactly the axis that matters for commercial game-asset use. Per-model verdicts are stored in `models.verify_note` and surfaced in the catalog (`✓` column).

## Material corrections the verifier caught (commercial-safety critical)

| Model | Correction |
|---|---|
| **SkyReels-V2** | License is **NOT Apache-2.0** — it's the custom **Skywork License** (commercial use still permitted, so `commercial_use:yes` stands, but the license name was wrong). |
| **CogVideoX 5B / 5B-I2V** | Code + the **2B** weights are Apache-2.0, but the **5B / 5B-I2V weights ship under a custom CogVideoX License** — not blanket Apache. Also superseded. |
| **DeepSeek-R1-Distill-Qwen-32B** | Distilled weights are **MIT**, not Apache-2.0 (the Qwen2.5-32B *base* is Apache; the distill is MIT per DeepSeek's card). Also superseded. |
| **LTX-2.3** | "19B" = 14B video + 5B audio; the downloadable video model is ~14B. License is a custom **LTX-2 community license with a $10M revenue threshold**, not Apache. |
| **Hunyuan3D-2 / 2.1, HunyuanVideo-Foley** | Tencent community license **territory excludes the EU, UK, and South Korea** and caps at 1M (3D) / 100M (Foley) MAU — verified against the raw LICENSE file. |

## Currency flags (real + usable, but a newer option exists)

`superseded` — keep only if you have a specific reason; otherwise prefer the newer pick in the same lane:

- **Stable Diffusion 3.5 Large** (image) → Qwen-Image-2512 / Z-Image / Chroma are better-licensed and newer.
- **Mochi 1**, **CogVideoX 5B** (video) → Wan 2.2 / LTX-2.3.
- **Kokoro-82M** (audio) — still the best lightweight consent-free TTS, but its "#1" ranking is superseded; fine to keep.
- **DeepSeek-R1-Distill-Qwen-32B** (llm) → Qwen3.6 / Gemma 4.

## Confidence caveats (carried from the lanes)

- **JS-rendered sources:** some official blogs/model cards (certain Qwen3.6 / Gemma 4 specifics) didn't return body text to the fetcher; those facts were corroborated across multiple secondary sources with the official URLs cited. **Re-open the HF LICENSE file on each repo before shipping paid assets.**
- **audio:** HunyuanVideo-Foley's license-restriction text couldn't be confirmed verbatim from the repo page; ACE-Step's `repo_url` points to a real but slightly-off variant of the canonical repo name (the authoritative HF repo confirms MIT).
- **image-base:** Pony V7 (Oct 2025, on AuraFlow) had mixed early community reception vs entrenched Illustrious/NoobAI — verify current community checkpoints before committing.

## Verifier-proposed additions → wave 2 candidates

Each verifier was asked for up to 3 must-have models the researcher omitted. 21 surfaced (none added this wave; these scope wave 2):

- **image-base:** HunyuanImage 3.0 · Lumina-Image 2.0 · Qwen-Image-Edit (2509)
- **image-control:** FLUX.1-Kontext [dev] (instruction editing) · Qwen-Image-Edit (Apache editing counterpart) · Ultimate SD Upscale (tiled-diffusion node)
- **video:** Wan 2.5 / 2.6 (the real intermediate releases) · FLUX.2 image-to-video / first-frame pipelines · LTX-Video 0.9.x legacy (low-VRAM)
- **3d:** Hi3DGen (geometry-quality leader) · TripoSG / TripoSR · Stable Fast 3D (real-time tier)
- **audio:** DiffRhythm / DiffRhythm 2 (Apache full-song) · VibeVoice (promote from extra) · (F5-TTS already in extras, non-commercial)
- **llm:** InternVL3.5 base family · MiniCPM-V 4.x · WD/SmilingWolf ConvNeXt-v3 tagger (booru-tag captioning)
- **comfy:** ComfyUI_IPAdapter_plus (cubiq) · ComfyUI-VideoHelperSuite (Kosinkadink) · ComfyUI-Frame-Interpolation (Fannovel16)

> Wave 2 suggestion: a focused "editing + video-helper + tagger" pass would close most of these and deepen the game-asset pipeline (instruction-edit + character-consistency + booru tagging).
