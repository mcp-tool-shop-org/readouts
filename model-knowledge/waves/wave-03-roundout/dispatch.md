# Wave 3 — Rounding pass: separation, taggers, Wan S2V/VACE, HiDream-E1, formal FLUX.2 rows

**Study-swarm wave 3** · 2026-06-02 · 6 lanes · 12 agents · **21 models, 52 sources, 10 custom nodes**. Run `wf_b38c3518-b22`. Clears the wave 1–2 verifier queue and deepens existing categories (no new ones). KB total: **108 models**.

## Headline findings (each tied to a pick)

- **Post-Demucs separation is the RoFormer family — and the commercial-safe route is specific.** **Mel-Band RoFormer** (lucidrains code MIT) with the **KimberleyJSN vocal checkpoint (MIT)** is the recommended commercial-safe stem path (game VO extraction, remix stems, dataset prep). BS-RoFormer code is MIT too, but the popular **viperx checkpoints are license-unverified** → conditional; verify each checkpoint *file* before shipping. (Sony's new **Woosh** SFX foundation model is **non-commercial weights** — prototyping only.)
- **Editing rounding — a license nuance to watch: HiDream-E1.1** has MIT transformer weights but ships a **Llama-3.1 text encoder under the Llama Community License** → *conditional*, not clean Apache. The genuinely-new **FireRed-Image-Edit-1.1 is Apache** (commercial-safe). Qwen-Image-Edit-2509 added as the documented predecessor (superseded by 2511).
- **The FLUX.2 "klein is open" trap:** klein shipped **two sizes under two licenses — klein 4B = Apache (commercial-safe), klein 9B = FLUX Non-Commercial.** FLUX.2-dev is also non-commercial. Original **Qwen-Image (20B) = Apache**. Many blogs omit the 9B caveat — don't.
- **Wan family completed:** **Wan2.2-S2V-14B** (Apache, speech/audio→video for character cutscenes; Q8 GGUF ~19.6 GB fits 32 GB) + **Wan2.2-VACE-Fun-A14B** (Apache, Canny/Depth/Pose/trajectory control + reference-subject; Q8 ~15.4 GB). The Phr00t Rapid all-in-one merge works but is community/deprecated.
- **LoRA-dataset tagging completed:** **WD SwinV2 Tagger v3** (Apache), **Camie-Tagger v2** (GPL-3.0, ~70k-tag vocab vs WD's ~10k), and **CapRL-InternVL3.5-8B** (Apache, the caption-quality specialist — its CC-BY-NC *training data* does **not** bind the released weights or the captions you make). Plus the **ComfyUI-WD14-Tagger** node + LoRA-caption save nodes + audio-separation nodes.

## Re-download additions (wave 3)

| Domain | Add | License |
|---|---|---|
| Audio (separation) | **Mel-Band RoFormer** + KimberleyJSN vocal ckpt | MIT (clean) |
| Image — editing | **FireRed-Image-Edit-1.1** · HiDream-E1.1 (Llama-encoder caveat) | Apache / conditional |
| Image — base | **FLUX.2 klein 4B** · original **Qwen-Image** (both Apache); FLUX.2-dev + klein-9B = non-commercial | Apache / NC |
| Video | **Wan2.2-S2V-14B** · **Wan2.2-VACE-Fun-A14B** (GGUF Q8 fits 32 GB) | Apache |
| Captioning | **WD SwinV2 v3** · **CapRL-InternVL3.5-8B** · Camie-Tagger v2 | Apache / GPL |
| Comfy nodes | **ComfyUI-WD14-Tagger** + LoRA-caption + audio-separation nodes | MIT |

Catalog: [audio](../../catalog/audio.md) · [image-edit](../../catalog/image-edit.md) · [image-base](../../catalog/image-base.md) · [video](../../catalog/video.md) · [caption](../../catalog/caption.md) · [comfy](../../catalog/comfy.md).

## Method + what's deferred

- 21/21 models resolved; 15 confirmed, 6 corrected, 0 refuted. Catches in [verification.md](verification.md).
- **The verifier-flagged queue is now largely drained.** Remaining narrow wave-4 candidates: SCNet multi-stem separation, MVSep/UVR5 separation front-end, Wan2.2-Fun-Control-Camera, FLUX.2 klein official fp8/nvfp4 quant repos. (Most other "missing" items were already cataloged in earlier waves — the verifiers lack cross-wave visibility.)
- Same verifier-maturity caveat as prior waves (same-family + retrieval oracle; family-different `prism`/`roleos` path still the planned upgrade).
