# Wave 2 — Verification receipt

Same method as wave 1: a **reasoning-stripped adversarial verifier** per lane using **`WebFetch` as a retrieval oracle** (existence / license / specs / currency); default `unverified` on non-confirmation. Same-model-family this wave; the family-different path (`prism verify` / `roleos verify-citations`, ideally a local non-Claude model per `hardware-omen-45l.md`) remains the planned upgrade.

## Verdict distribution

**35 models · 23 `confirmed` · 12 `confirmed-with-fixes` · 0 `unverified` · 0 `refuted`.** Commercial split: **27 yes / 4 conditional / 2 no / 2 unknown** (the comfy lane's 23 node/workflow extras were verified too — 58 verdicts total).

## Material catches

| Item | Catch |
|---|---|
| **VibeVoice (Large 7B + 1.5B)** | Weights are MIT, but **Microsoft disabled the official GitHub repo** (~late 2025) — only HF mirrors remain. Treat as **superseded / at-risk**; prefer Chatterbox or Kokoro for a maintained TTS. |
| **Sparc3D** | **Deprecated / do-not-use** — verifier-confirmed accurate (code/paper only, superseded by the Sparcubes line). Kept in the DB as `legacy/avoid`, not recommended. |
| **Hybrid Demucs (htdemucs)** | Real + MIT, but **deprecated for quality** — **BS-RoFormer / Mel-Band RoFormer** are the current stem-separation SOTA (queued for wave 3). |
| **Illustrious XL v2.0** | License **confirmed relicensed FAIPL → OpenRAIL-M** — i.e. the one *clean commercial* anime base (contrast NoobAI/Pony, which stay non-commercial). |
| **3D geometry tier** | Confirmed **uniformly MIT** (Hi3DGen, TripoSG, PartCrafter, UniRig, ComfyUI-3D-Pack) — clean commercial spine. |
| **SUPIR (comfy lane)** | Confirmed **strictly non-commercial** weights — flagged so it never enters a paid pipeline. |

## Currency flags

`superseded` / `deprecated` — prefer the alternative: **VibeVoice** (repo withdrawn → Chatterbox/Kokoro), **Sparc3D** (do-not-use → TripoSG/Hi3DGen), **Hybrid Demucs** (→ BS-RoFormer).

## Wave-3 candidates (verifier "missing")

Filtered to the genuinely-new (several "missing" items — Qwen-Image base, ACE-Step, Hunyuan3D, Manager, KJNodes — are already in the DB from earlier; the verifier lacked full cross-wave visibility):

- **image-edit:** HiDream-E1 / E1.1 (open commercial instruction editor) · FLUX.1-Kontext [pro]/[max] (commercial API tier, for the licensed path)
- **image-base:** FLUX.2 [dev] (add a formal catalog row — currently only referenced)
- **video:** Wan2.2-VACE-Fun-A14B · Wan2.2-S2V-14B (speech/audio-to-video, character cutscenes) · Phr00t WAN2.2-14B-Rapid-AllInOne (community merged checkpoint)
- **audio:** **BS-RoFormer / Mel-Band RoFormer** (the current separation SOTA that supersedes Demucs)
- **caption:** WD SwinV2 Tagger v3 (third v3 family member) · ensure JoyCaption HF *weights* repo (not just GitHub) is the linked download
- **comfy:** ComfyUI-WD14-Tagger (pythongosssss) — the de-facto booru-tag captioner node for LoRA datasets

> Wave-3 suggestion: a short "separation + tagger + Wan-S2V + formal FLUX.2/HiDream-E1 rows" pass closes these and rounds out the game-audio + LoRA-dataset pipelines.
