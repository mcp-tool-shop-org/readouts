# Wave 2 — Deep pass: editing, video control, game-ready 3D, captioning, comfy nodes

**Study-swarm wave 2** · 2026-06-02 · 7 lanes · 14 agents · **35 models, 96 sources, 34 custom nodes**. Run `wf_8d160bb6-4e5`. Clears the wave-1 verifier-flagged gaps and deepens each domain. Adds two new DB categories: **Image — editing** and **Captioning & tagging**. KB total: **87 models**.

## What wave 2 adds

- A whole new capability lane — **instruction image editing** (iterate an asset without a full regen): the core of fast game-asset work.
- **Captioning & tagging** as its own category — directly feeds the LoRA-training pipeline (style-dataset-lab).
- Deeper **video** (control + acceleration), **3D** (geometry tier + mesh→game-asset gap), **audio** (full pipeline), and the job-specific **ComfyUI node** ecosystem.

## Headline findings (each tied to a pick)

- **Editing has one decisive winner: Qwen-Image-Edit-2511 (Apache-2.0).** The only *frontier-class* editor that's also unconditionally commercial → the default for both lanes. FLUX.1-Kontext-dev is frontier too but **non-commercial** (paid BFL license) → personal/prototyping only. Step1X-Edit-v1p2 (Apache) is the reasoning-heavy specialist; OmniGen2 the low-VRAM multi-reference option. **ICEdit is double-non-commercial** (its own license *and* its FLUX-Fill base) — avoid for paid work.
- **The anime-base licensing trap is now escapable: Illustrious XL v2.0 was relicensed FAIPL → OpenRAIL-M** — the *only* clean commercial anime/illustration base (NoobAI and Pony remain non-commercial). Plus Lumina-Image 2.0 (Apache) and Juggernaut XL Ragnarok / RealVisXL V5 (OpenRAIL++) for realism. HunyuanImage 3.0 = conditional (Tencent: excludes EU/UK/South Korea, 100M-MAU gate).
- **The "newer Wan" everyone links is not open weights.** Checked `huggingface.co/Wan-AI` directly: there is **no Wan 2.5/2.6/2.7/3.0** weight repo — newest open is **Wan2.2-Animate-14B** (Sep 2025). The `wan25-*` repos are unofficial re-uploads; Wan 2.6 is a hosted API. So the local play stays **Wan 2.2 + a LightX2V 4-step distill LoRA** (Apache, big speedup) + **Wan2.2-Animate-14B** (character motion) + Fun-Control. All Apache.
- **The 3D geometry tier is uniformly MIT — a clean game-asset spine.** Hi3DGen, TripoSG, PartCrafter, UniRig (auto-rigging), ComfyUI-3D-Pack — all MIT, commercial-safe, finetune-friendly. Stable Fast 3D = SAI community (<$1M). Note: the wave-1 PBR pick **Hunyuan3D-2.1 is materially *worse* licensed** (Tencent EU/UK/SK exclusion) — don't assume "open = MIT". **Sparc3D is deprecated (do-not-use)** — verifier-confirmed.
- **Audio: DiffRhythm 2 (Apache, full-song) is the cleanest-licensed music model**, plus a withdrawn-model caveat: **VibeVoice (MIT) had its official Microsoft repo disabled** — mirror-only, treat as at-risk; Chatterbox/Kokoro stay the maintained TTS picks. Demucs is deprecated for separation → **BS-RoFormer / Mel-Band RoFormer** are current SOTA.
- **Captioning's load-bearing rule: match caption style to the base model's text encoder.**
  - **SDXL / Illustrious / Pony / NoobAI** (CLIP, booru-trained) → **TAG** with WD v3 taggers (EVA02-Large for precision, ConvNeXt for recall) — crisp composable trigger tokens.
  - **Flux / SD3.5 / HiDream / Qwen-Image** (T5/LLM, prose-trained) → **CAPTION** with a prose VLM: JoyCaption Beta One (best default, Apache, uncensored), MiniCPM-V 4.5 / InternVL3.5-8B (richer), CapRL when caption quality is the sole priority. Mismatching style to encoder is the common LoRA mistake.
- **Comfy nodes split into three license tiers.** *Use freely:* VideoHelperSuite, Frame-Interpolation (RIFE/FILM), Florence2, rembg/InSPyReNet, SAM2, UltimateSDUpscale + RealESRGAN, seamless-tiling. *GPL node code but unrestricted output (safe for assets):* IPAdapter_plus, RMBG. ***Non-commercial — flagged:*** SUPIR weights.

## Updated re-download shortlist (wave-2 additions, all commercial-safe unless noted)

| Domain | Add | License |
|---|---|---|
| Image — editing | **Qwen-Image-Edit-2511** (default) · Step1X-Edit-v1p2 · OmniGen2 | Apache |
| Image — base | **Illustrious XL v2.0** (anime, clean) · Lumina-Image 2.0 · Juggernaut XL Ragnarok · RealVisXL V5 | OpenRAIL / Apache |
| Video | **Wan2.2 + LightX2V 4-step** · Wan2.2-Animate-14B · Wan2.2-TI2V-5B · Fun-Control | Apache |
| 3D | **Hi3DGen · TripoSG · PartCrafter** · UniRig (rigging) | MIT |
| Audio | **DiffRhythm 2** (full song) · VibeVoice (mirror-only) · htdemucs→prefer RoFormer | Apache / MIT |
| Captioning | **JoyCaption Beta One** (prose) · **WD EVA02-Large v3** (tags) · MiniCPM-V 4.5 · InternVL3.5-8B | Apache |
| Comfy nodes | IPAdapter_plus · VideoHelperSuite · Frame-Interpolation · Ultimate SD Upscale · rembg/SAM2 | mixed (output free) |

Catalog: [image-edit](../../catalog/image-edit.md) · [caption](../../catalog/caption.md) · [video](../../catalog/video.md) · [3d](../../catalog/3d.md) · [audio](../../catalog/audio.md) · [comfy](../../catalog/comfy.md) · [image-base](../../catalog/image-base.md).

## Method + what's deferred

- 35/35 models resolved; 23 confirmed, 12 corrected; 0 refuted. Verifier catches in [verification.md](verification.md).
- Same verifier maturity caveat as wave 1 (same-family + retrieval oracle; family-different `prism`/`roleos` path still the planned upgrade).
- 16 official starter workflows fetched into `workflows/` (incl. Qwen-Image-Edit, Wan i2v, Hunyuan3D, FILM interpolation).
- **Wave-3 candidates** (verifier "missing", genuinely new): HiDream-E1 editor · FLUX.2-dev (formal catalog row) · Wan2.2-VACE-Fun + Wan2.2-S2V · Phr00t WAN2.2 Rapid all-in-one · BS-RoFormer / Mel-Band RoFormer · WD SwinV2 tagger · ComfyUI-WD14-Tagger node. See [verification.md](verification.md).
