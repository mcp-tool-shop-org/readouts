# Wave 6 — ComfyUI beyond image-gen, scored for Comfy Cloud (2026-06-30)

**A full study-swarm sweep** (15 agents: 7 research lanes → per-lane reasoning-stripped adversarial source-verifier → completeness critic; ~835k subagent tokens). Verbal trigger `study-swarm`, run under the [[research-grounded-advisor-protocol]]. The question: **now that the studio has Comfy Cloud (the managed RTX-6000-Pro service, driven headlessly via the official `X-API-Key` API), what can ComfyUI do BEYOND image generation — and which of those uses actually run on the managed cloud vs. the local RTX 5090?**

Verifier = the same WebFetch-as-retrieval-oracle pattern as wave-05: each lane's GO/NO-GO claims (every `cloud_feasible: yes` and every license claim) were independently re-fetched by a reasoning-stripped verifier. Receipts: [verification.md](verification.md).

> This wave does NOT add a domain of new models. It adds a **cross-cutting `cloud_feasible` axis** to existing models (video/audio/3d/caption/control) + one new model (Qwen3-TTS) + the Comfy-Cloud platform facts. The axis now lives in `models.db` (`models.cloud_feasible` / `models.cloud_note`) and renders in `catalog/comfy.md` (the "Comfy Cloud (managed service) — feasibility" section) and each model's Detail.

## The gate (the one fact that governs everything)

Comfy Cloud is **not general compute** — it is a **managed, allowlisted, sandboxed render service**. Three confirmed constraints set the whole envelope:

1. **Curated node allowlist** — you run only Comfy Cloud's preinstalled packs ("~90% of local workflows"); you **cannot install arbitrary registry nodes or bring your own node code**, and a workflow referencing an unsupported node is rejected. ([supported-nodes](https://comfy.org/cloud/supported-nodes/), [out-of-beta blog](https://blog.comfy.org/p/comfy-cloud-is-out-of-beta-and-its))
2. **Sandbox bans arbitrary code + arbitrary network** — the Comfy Registry prohibits `eval`/`exec` and subprocess installs, and outbound calls to non-allowlisted hosts are blocked. ([registry standards](https://docs.comfy.org/registry/standards)) → no run-python nodes, no scraping, no external DB, no calling an outside LLM/API from inside a graph.
3. **Metered, not flat** — Creator is **$35/mo but with a 7,400-credit/mo pool** (~0.266 credits/GPU-sec ≈ **~7.7 GPU-hours/mo**), **3 concurrent jobs**, **30-min/workflow cap**, BYO-LoRA (CivitAI now, HF soon). ([pricing](https://comfy.org/cloud/pricing/)) Hardware: Blackwell RTX 6000 Pro, **96 GB VRAM / 180 GB RAM** — runs Wan 14B fp8/bf16 without GGUF.

**Decision rule:** a non-image capability is cloud-feasible **iff** it maps to nodes already on the allowlist and needs no arbitrary code, no outbound network, and no persistent DB. Everything else stays on the local RTX 5090 (which also trains LoRAs — the cloud cannot, per [[comfy-cloud-run]] Gotcha #7).

> **Correction recorded with this wave:** the "$35/mo flat — no per-render meter" framing in the `comfy-cloud` skill + the sprite-foundry handoffs was **wrong** and was fixed 2026-06-30. The credit pool is exhaustible; cost heavy batch sweeps before launching. `memory/comfy-cloud-run.md` Gotcha #7 was already correct.

## The five proposed categories, graded

| Category | On Comfy Cloud? | Reality |
|---|---|---|
| **3D modeling & texturing** | 🟠 mostly **local** | Only **Hunyuan3D-2 native** nodes run on cloud ("Run on Comfy Cloud" buttons) — **shape only, no PBR/UV**. 3D-Pack / TRELLIS.2 / Hunyuan-2.1-PBR need compiled CUDA → local. ⚠ Hunyuan3D license **excludes EU/UK/South Korea** — a shipping flag. TRELLIS.2 is MIT-clean but local-only. |
| **LLM / text processing** | 🟡 **split** | First-party **Gemini/GPT API nodes** run on cloud but draw from the **same 7,400-credit pool**. **Open VLM on-GPU** (Florence2/QwenVL) runs **credit-free** — the additive play. **Local-Ollama LLM nodes need `127.0.0.1:11434`** → cloud-impossible, and locally they **duplicate [[ollama-intern]]**. |
| **Audio & voiceover** | 🟢 **cloud (selective)** | **ACE-Step 1.5** music (MIT) + **Qwen3-TTS** character VO (Apache-2.0) + **AudioTools / MelBand-RoFormer** stem-sep are on the allowlist + commercial-safe → feed [[motif]]. **VibeVoice** (research-license-only + off-cloud), **DiffRhythm**, **MMAudio foley** (non-commercial CLIP) → local/prototype only. |
| **Data processing & automation** | 🟡 **split** | GPU batch + no-code dataset-prep (resize/mask/grid via supported nodes) = cloud. Scraping / SQLite / HTTP / DB = **blocked** (non-allowlisted hosts). Right pattern: client-side **ComfyScript / ComfyUI-to-Python** (MIT) POST jobs to the API; DB/manifest writes happen in *your* code. |
| **Code execution (arbitrary Python)** | 🔴 **local only** | Run-python nodes use `exec()` — banned by the registry. Push glue logic into the calling orchestrator, not a node. |

## What's actually worth doing on the cloud (highest value × certainty)

1. **Comfy Cloud as a headless render microservice behind Sprite Foundry / [[style-dataset-lab]]** — the official `X-API-Key` → `POST /api/prompt` → poll → `/api/view` API ([reference](https://docs.comfy.org/development/cloud/api-reference)); 3 concurrent jobs = real fan-out. The studio's `comfy_cloud_bridge.py` already does this. Everything else rides it.
2. **Wan 2.2 Animate (Move mode) + DWPose pose-driven sprite animation** — WanVideoWrapper, DWPose, VideoHelperSuite all on the allowlist; Wan 2.2 is **Apache-2.0** (shippable). The cloud sprite-motion path; maps onto [[sprite-motion-knowledge-kb]]. *(30-min cap: tile/keep ≤640p for long 720p clips.)*
3. **Florence2 + SAM3 auto-caption / auto-mask for sdlab ingest** — credit-free on the cloud GPU; attacks the real bottleneck (dataset prep), not just making more art.
4. **ACE-Step music + Qwen3-TTS VO + stem-separation → Motif** — three commercial-safe audio capabilities feeding a second shipping product's adaptive-stem pipeline.
5. **RIFE/FILM frame interpolation** for sprite in-betweening — cheap, deterministic, within the time cap.

**Video is the biggest "beyond images" category** by node count (WanVideoWrapper, Frame-Interpolation, VideoHelperSuite, **AnimateDiff-Evolved** for lighter looping FX, CogVideoX, LTXVideo all preinstalled). Plus **upscale/restore** (pin **RealESRGAN x4plus / BSD-3** — *not* SUPIR or 4x-UltraSharp, both non-commercial).

## What stays on the local RTX 5090

LoRA **training** (off-allowlist + collides with the 30-min cap — [[comfy-cloud-run]] Gotcha #7), the heavy **3D** stack (3D-Pack / TRELLIS.2 / Hunyuan-PBR), **IC-Light relighting + single-image normal maps** (a strong 2.5D find), dedicated **seamless-texture** + **pixel-art** packs, **VibeVoice / DiffRhythm / MMAudio**, and anything **code / scrape / DB**.

## Completeness critic — what the 7 lanes missed

- **In-graph LoRA training** (FluxTrainer / Realtime-Lora) — the studio's core workflow, but **cloud=no** (off-allowlist + 30-min cap + no persistent dataset FS). Flagged because a "what else can the cloud do" scan would wrongly assume it can train.
- **AnimateDiff-Evolved** — lighter, LoRA-compatible looping FX (idle breathing, flame, water); **cloud=yes** (on the allowlist). Drive a trained canon LoRA without standing up the 14B Wan stack.
- **Official "Sprite Sheet Generator" template** — first-party, has a "Try on Comfy Cloud" button; **cloud=partial** (its image step is a Gemini/Nano-Banana API node drawing credits → swap for a local-checkpoint + BYO-LoRA sampler for canon sprites).
- **Florence2 + SAM3 auto-caption/auto-mask dataset prep** — **cloud=yes**, credit-free; the cleanest sdlab accelerator.

## Honest verification notes (the verifier earned its keep)

- **"70+ packs" is unverified** — the curated-allowlist *substance* is confirmed; the round number isn't on the page.
- **SAM2 is not a standalone cloud pack** — the cloud lists **SAM3** + **SeC** for video segmentation; SAM2 appears only as a model inside RMBG. Use SAM3/SeC.
- **MMAudio is murkier than the audio lane first claimed** — MMAudio-named loaders *do* appear nested under WanVideoWrapper/Ovi; the real blocker is the standalone foley path's non-commercial CLIP.
- A few license claims (Qwen3-TTS / Wan-S2V Apache-2.0) were flagged `CANNOT_CONFIRM` only because the *cited blog* wasn't the LICENSE file — the licenses are real, verified against the repos.

## Provenance

- Swarm: `comfyui-beyond-image-study-swarm` (run `wf_92f13b67-f91`, 2026-06-30), 15 agents, model `claude-opus-4-8`.
- Verifier: per-lane reasoning-stripped WebFetch retrieval-oracle (existence / cloud-support / license). Family-different prism/roleos path deferred (same posture as waves 1–5).
- Full synthesis + the studio-facing readout live in this dispatch; the operational cloud-run procedure is [[comfy-cloud-run]]; the bridge wiring is the `comfy-cloud` skill.
