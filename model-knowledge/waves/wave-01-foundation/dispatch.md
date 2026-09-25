# Wave 1 — Foundation: best local generative-AI models for a 32 GB RTX 5090

**Study-swarm wave 1** · dispatched 2026-06-02 · 7 lanes · 14 agents (one research + one adversarial verifier per lane) · **52 models, 179 sources, 21 custom nodes, 12 workflow links**. Run `wf_554d20e0-735`.

## Context

- **Rig:** HP Omen 45L · RTX 5090 · **32 GB VRAM** · Win 11. A reformat wiped the local model library, so this is a **re-download priority guide** — what to grab now that the card is much bigger than the 12 GB it was last configured for.
- **Dual use, weighted equally:** game-asset production (needs commercial-safe licensing, LoRA-trainability, style consistency) **and** general creative/marketing (text rendering, photoreal, speed). Every model is tagged for both (`game_asset_fit`, `marketing_fit`).
- **Method:** one web-grounded research agent per domain; each output handed to a **reasoning-stripped adversarial verifier** that used live web retrieval as an existence/license/spec oracle *before* the data was trusted. Full receipt → [verification.md](verification.md).
- **Currency:** everything here was confirmed live on 2026-06-02. The assistant's training cutoff predates the FLUX.2 / Z-Image / Qwen-Image-2512 / Wan 2.2 / LTX-2.3 / TRELLIS.2 / Gemma 4 / Qwen3.6 wave — none of that is from memory.

## The finding that reorganizes the whole catalog: licensing has bifurcated

For your dual use, **license is the decisive axis, not quality** — most top models are good enough; the question is whether you can *sell* what you make with them. The field has split into three buckets, and the split is counter-intuitive:

- **Clean (Apache-2.0 / MIT)** — sell freely, worldwide, no caps: Qwen-Image-2512, Z-Image-Turbo, Chroma1-HD, FLUX.2-klein, HiDream-I1 (image); Qwen-Image ControlNets, xinsir SDXL Union, Real-ESRGAN, ai-toolkit, kohya_ss (control); Wan 2.2, TRELLIS.2 (video/3D); ACE-Step 1.5, Chatterbox, Kokoro, YuE (audio); Qwen3.6, Gemma 4, Qwen3-VL, CapRL (LLM).
- **Conditional (revenue or regional caps — read before shipping)** — SD3.5 + its ControlNets and Stable Audio (free under $1M revenue); LTX-2.3 (free under $10M); **Hunyuan3D / HunyuanVideo-Foley (Tencent community license — territory EXCLUDES the EU, UK, South Korea; MAU caps)**.
- **Non-commercial (great for comps, poison for paid game assets)** — the entire **FLUX.1-dev / FLUX.2-dev** conditioning family, **SUPIR**, **4x-UltraSharp / 4x-Remacri**, **CodeFormer**, **MMAudio**, **F5-TTS**, **MusicGen**, **Pony V7**, **NoobAI**.

The trap is that the *most visible, most-recommended-in-tutorials* models — FLUX-dev, SUPIR, 4x-UltraSharp, Pony — are exactly the non-commercial ones. They're fine for marketing/personal comps; they must not enter a paid game-asset pipeline.

**LoRA license-inheritance rule (load-bearing for your game work):** a trained LoRA inherits the **base model's** license, *not the trainer's*. ai-toolkit (MIT) or kohya_ss (Apache) producing a LoRA on FLUX.1-dev → that LoRA is still non-commercial. So **train character/style LoRAs on SDXL, Qwen-Image, or Chroma** for commercial-safe assets. (image-control lane.)

## The re-download plan (grab in this order)

### Tier 0 — runtime first
**ComfyUI** stock Windows portable (`ComfyUI_windows_portable_nvidia.7z`) or the Desktop installer. The old Blackwell/5090 pain is **resolved** as of mid-2026: PyTorch 2.7.0+ ships stable `sm_120`/CUDA 12.8 wheels and the portable bundles CUDA 13 + Python 3.13 — **skip every blog telling you to hand-install torch nightly**, it's stale advice. One rule still holds: **never `pip install xformers`** into the embedded python (it clobbers the working CUDA torch) — use SageAttention + triton-windows + `torch.compile` (exposed by KJNodes). Install **ComfyUI-Manager** by hand first, then install/update all other nodes through its UI. (comfy lane.)

### Tier 1 — the commercial-safe core (this is your shortlist; all Apache/MIT/BSD unless noted)

| Job | Grab | Why |
|---|---|---|
| Image daily-driver | **Z-Image-Turbo** (6B, 8-step, ~13 GB) | #1 open-weights on Artificial Analysis Arena, sub-second, keep it resident. |
| Image quality + text | **Qwen-Image-2512** (20B) | Best-licensed frontier all-rounder; unbeatable text-in-image for marketing. |
| Game-asset base + LoRA target | **Chroma1-HD** (FLUX-quality, Apache) and **Illustrious XL v2.0** (anime/illustration, deepest LoRA ecosystem; *conditional* license) | Purpose-built finetune targets; train your style/character LoRAs here. |
| Control / refine | **Qwen-Image ControlNet-Union (InstantX)** + **xinsir SDXL Union ProMax** + **Real-ESRGAN** | Commercial-safe conditioning + upscaling stack (the popular Flux Union / SUPIR / 4x-UltraSharp are all non-commercial). |
| Trainer | **ai-toolkit** (MIT) — web UI at `localhost:8675`, trains FLUX.1/FLUX.2/SDXL/Qwen/Z-Image; kohya_ss as the SDXL workhorse. |
| Video | **Wan 2.2** (quality anchor, fp8/GGUF) + **LTX-2.3** (≈5.7× faster, for marketing turnaround) | Both have native/day-1 ComfyUI nodes; add a Lightning/LightX2V step-LoRA on Wan to cut render time. |
| 3D | **TRELLIS.2-4B** (MIT, SOTA generalist topology) + **Hunyuan3D-2.1** (PBR-texture workhorse; *Tencent territory caveat*) | Complementary; 32 GB runs both full pipelines (~24 GB / ~29 GB peak). |
| Audio | **ACE-Step 1.5** (music) + **Chatterbox** (VO) + **Kokoro-82M** (UI/narration) + **Stable Audio 3.0** (SFX, *<$1M*) | VRAM is not the constraint here at 32 GB — license + quality are. |
| LLM / captioning | **Qwen3.6-27B** (text/code/prompt) + **Gemma 4** (do-everything multimodal) + **CapRL-InternVL3.5-8B** (dataset captioning — beats Qwen2.5-VL-72B at caption quality) | All Apache-2.0; fit 32 GB at Q6–Q8. |

### Avoid for paid assets unless you clear licensing
FLUX.2-dev (non-commercial weights), Pony V7 (Pony License blocks inference-service / >$1M / pro-video), NoobAI, SUPIR, 4x-UltraSharp/Remacri, MMAudio, F5-TTS, MusicGen, Llama 4 (700M-MAU cap + EU vision restriction). Keep them for personal/marketing comps if you like — just tag the output.

## Per-domain grounding (findings → recommendations)

- **Image — base.** The 2026 shift is the FLUX.2 family plus a wave of fast Apache Chinese bases. *Because* license is decisive, the picks invert the usual tutorial advice: Z-Image/Qwen-Image/Chroma over FLUX.2-dev. SDXL-lineage (Illustrious, Juggernaut) + Chroma remain the cheapest, most LoRA-mature trainables → your game-asset consistency lane. See [catalog/image-base.md](../../catalog/image-base.md).
- **Image — control & utility.** The whole popular Flux conditioning stack (Union Pro 2.0, Fill, Depth, Canny, Redux, Kontext) is non-commercial; the commercial-safe stack is Qwen-Image + InstantX ControlNets and xinsir SDXL Union. For reliable character consistency, **train a LoRA, don't lean on IP-Adapter** (InstantX's own card says it's image-reference, not fine-grained character transfer). [catalog/image-control.md](../../catalog/image-control.md).
- **Video.** Wan 2.2 is the verified, downloadable anchor today; **"Wan 2.7" is largely SEO** — the official Wan-AI HF org hosts only 2.1/2.2 (verifier confirmed). LTX-2.3 is the speed play but carries a **custom community license with a $10M revenue threshold**, not Apache (verifier corrected this). [catalog/video.md](../../catalog/video.md).
- **3D.** Download both TRELLIS.2-4B (MIT, clean) and Hunyuan3D-2.1 (best PBR textures). The Hunyuan license **excludes the EU/UK/South Korea** and caps at 1M MAU — if you sell there, prefer the MIT models or get a regional license. Watch the TRELLIS nvdiffrast/nvdiffrec optional deps (NVIDIA non-commercial source license). [catalog/3d.md](../../catalog/3d.md).
- **Audio.** At 32 GB nothing is VRAM-constrained, so license + quality decide. Commercial-safe core: ACE-Step 1.5 (MIT), Chatterbox (MIT), Kokoro (Apache), YuE (Apache). **Separate legal flag:** an MIT/Apache license on a voice-cloning model does **not** grant rights to a *person's voice* — only clone voices you own or have licensed. [catalog/audio.md](../../catalog/audio.md).
- **Local LLM + vision.** Two Apache families dominate: Qwen3.6 (text/code/prompt) and Qwen3-VL (vision), with Gemma 4 as the strongest single do-everything model. For your dataset-captioning pipeline, CapRL-InternVL3.5-8B is the standout value. Llama 4 and JoyCaption carry license caveats (flagged). [catalog/llm.md](../../catalog/llm.md).

## Method, confidence, and what's deferred

- **Verification:** 52/52 models resolved to real pages; 39 confirmed outright, 13 corrected (mostly license precision + currency). The verifier caught material commercial-safety fixes (SkyReels-V2 is *not* Apache; CogVideoX-5B weights aren't fully Apache; DeepSeek-R1-Distill is MIT). Details in [verification.md](verification.md).
- **Caveats (re-verify before shipping commercially):** a few official blogs/cards are JS-rendered and didn't return body text to the fetcher (some Qwen/Gemma specifics) — those were corroborated across multiple secondary sources with the official URLs cited; open the HF **LICENSE file** on each repo before you ship paid assets. Pony V7 community reception is mixed — check current community checkpoints.
- **Verifier maturity:** this wave used a same-model-family verifier with a retrieval oracle. The **family-different** upgrade (route citations through `prism verify` / `roleos verify-citations`, ideally with a *local* non-Claude model on this 32 GB rig per `hardware-omen-45l.md`) is planned for a later wave — consistent with the protocol's own P1 backlog.
- **21 verifier-proposed additions → wave 2** (e.g. FLUX.1-Kontext, Qwen-Image-Edit, Hi3DGen, DiffRhythm 2, VibeVoice, InternVL3.5 base, the IPAdapter/VideoHelperSuite/Frame-Interpolation nodes). Listed in [verification.md](verification.md).

## Querying this wave

```powershell
# the shortlist
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'model-knowledge/models.db').execute('SELECT category,dl,name,license,commercial_use,vram FROM v_recommended')]"
# only commercial-safe, by purpose
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'model-knowledge/models.db').execute(\"SELECT purpose,model,use_tag FROM v_best_for WHERE commercial_use='yes'\")]"
```
