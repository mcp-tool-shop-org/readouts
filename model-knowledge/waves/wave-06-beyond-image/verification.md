# Wave 6 — verification receipts

Each research lane's GO/NO-GO claims (every `cloud_feasible: yes` and every license claim) were independently re-fetched by a **reasoning-stripped adversarial verifier** (a second agent given the bare claim + URL only, told to retrieve and judge CONFIRMED / REFUTED / CANNOT_CONFIRM, never to confirm from prior knowledge). Retrieval oracle = `WebFetch` (live page), same posture as waves 1–5. Run `wf_92f13b67-f91`, 2026-06-30.

## Gate lane (Comfy Cloud platform) — all 4 CONFIRMED

| Claim | Verdict | Note |
|---|---|---|
| Curated allowlist; cannot install arbitrary nodes ("~90% of local workflows") | **CONFIRMED** | Substance confirmed; the specific "70+" pack count is **not on the page** (unverified number, true substance). |
| Official `X-API-Key` API: `POST /api/prompt` → poll → `/api/view`; Creator = 3 concurrent | **CONFIRMED** | Queue=100 + 30-min cap confirmed on the pricing page (not the docs page originally cited). |
| Creator = $35/mo **metered** (7,400 credits, ~0.266/GPU-sec) — not flat | **CONFIRMED** | 0.266 rate verbatim on blog.comfy.org; pricing page confirms 7,400 + active-GPU-time billing. |
| BYO models = **LoRAs** (CivitAI now, HF soon), Creator+ — not arbitrary checkpoints | **CONFIRMED** | Exactly as stated; full-checkpoint import not documented. |

## 3D lane

| Claim | Verdict | Note |
|---|---|---|
| Hunyuan3D-2 native runs on Comfy Cloud ("Run on Comfy Cloud") — **shape only, no PBR** | **CONFIRMED** | Page: "natively supports Hunyuan3D-2mv, but does not yet support texture and material generation." |
| Hunyuan3D-2.1 commercial < 1M MAU but **excludes EU/UK/South Korea** | **CONFIRMED** | License text quoted verbatim (MAU threshold + territory exclusion). |
| Heavy 3D stack (3D-Pack/TRELLIS2) is local-only (no arbitrary node install) | **CANNOT_CONFIRM** | True operationally, but the *cited* get-started page only markets "pre-installed nodes" — it doesn't state the prohibition. Substantiated by the gate lane's registry/allowlist sources instead. |
| TRELLIS.2-4B is MIT + needs Linux/24GB → local-only | **CANNOT_CONFIRM** | MIT + Linux/24GB **confirmed**; the "non-supported wrapper / local-only" half isn't on the cited wiki page (a third-party ComfyUI-TRELLIS2 wrapper does exist). |

## Audio lane

| Claim | Verdict | Note |
|---|---|---|
| ACE-Step 1.5 XL is MIT (commercial) AND on Comfy Cloud | **CONFIRMED** | "Commercially Licensed — MIT" + "Try on Comfy Cloud" links, both on the blog. |
| Qwen3-TTS Apache-2.0 + preinstalled audio pack on cloud | **CANNOT_CONFIRM** | Cloud-availability **confirmed** (ComfyUI-Qwen-TTS in the index); the Apache license is **not** on that page → verified separately against the Qwen3-TTS LICENSE file. |
| VibeVoice + MMAudio NOT in the index, with commercial restrictions | **REFUTED (as written)** | VibeVoice absence correct; but **MMAudio-named nodes ARE in the index** (nested in WanVideoWrapper/Ovi). License-restriction sub-claims weren't on the cited page. Net: foley-on-cloud is murkier; the real blocker is MMAudio's non-commercial CLIP, verified separately. |
| Wan2.2-S2V native-core + Apache-2.0; blog doesn't confirm cloud | **CANNOT_CONFIRM** | Native/template + "no cloud mention" **confirmed**; Apache license not on the blog → verified at the repo. |

## Video lane

| Claim | Verdict | Note |
|---|---|---|
| ComfyUI-WanVideoWrapper (Kijai) preinstalled on Comfy Cloud | **CONFIRMED** | Listed on the cloud supported-nodes directory (Kijai, v1.4.7); the "51 nodes" count is not stated. |
| Blackwell RTX 6000 Pro, 96GB VRAM + 180GB RAM | **CONFIRMED** | Verbatim on the out-of-beta blog. |
| Wan 2.2 (Animate/VACE/S2V) Apache-2.0, commercial | **CONFIRMED** | "The models in this repository are licensed under the Apache 2.0 License." |
| RIFE/FILM **and SAM2** preinstalled on cloud | **REFUTED (as written)** | RIFE/FILM **confirmed**; **no standalone SAM2 pack** on the cloud directory — it lists **SAM3** + **SeC**; SAM2 only as a model inside RMBG. |

## LLM / agents lane

| Claim | Verdict | Note |
|---|---|---|
| First-party API Nodes (Gemini/GPT) provide in-graph LLM/VLM, proxy-routed, on cloud | **CANNOT_CONFIRM (on cited URL)** | The Wave-2 blog confirms the nodes + model list + capabilities, but does **not** state the proxy/no-egress routing or mention Comfy Cloud — that's supported by *other* Comfy docs (cloud overview / DeepWiki), not the cited blog. |
| API/Partner nodes are prepaid-credit, no free tier, Comfy-proxied | **CONFIRMED** | "API nodes always consume credits (prepaid)… no free tier." |
| comfyui-ollama needs local `127.0.0.1:11434` → local-only | **CONFIRMED** | README requires a reachable local Ollama server. |
| Comfy Cloud server API (`/api/prompt`, `/ws`, `/api/view`) is real | **CONFIRMED** | Documented in the cloud API reference. |

## Data / code lane

| Claim | Verdict | Note |
|---|---|---|
| Registry bans `eval`/`exec` + subprocess installs → arbitrary-code/scrape/DB infeasible on cloud | **CONFIRMED** | "The use of eval and exec functions is prohibited… Runtime package installation through subprocess calls is not permitted." |
| Official server-side API, Standard/Creator/Pro, Creator=3 concurrent | **CONFIRMED** | All specifics match the cloud overview. |
| "70+ packs… lists no SQLite/HTTP/scrape" | **REFUTED (as written)** | No "70+" count on the page; SQLite/scrape absence holds but **WAS Node Suite ships an "Image Send HTTP" node** → the blanket "no HTTP" is false. |
| ComfyScript + ComfyUI-to-Python are MIT, client-side, API-only | **CANNOT_CONFIRM** | **MIT confirmed** for both; the "only submit JSON to the API" mechanism is imprecise (both also have in-process runtimes). |

## Divergent lane

| Claim | Verdict | Note |
|---|---|---|
| Official server-to-server API, Creator=3 / Pro=5, not Free | **CONFIRMED** | Standard tier (1 concurrent) ALSO has API access — claim omits it but every asserted fact is correct. |
| DepthAnythingV2 / Advanced-ControlNet / RMBG / UltimateSDUpscale / WAS / video stack ON the allowlist; controlnet_aux + efficiency-nodes XY-Plot NOT | **CONFIRMED** | Each listed (or absent) exactly as claimed on the supported-nodes directory. |
| Upscaler license: RealESRGAN x4plus BSD-3 (clean); UltraSharp / SUPIR / RMBG-2.0 non-commercial | **CANNOT_CONFIRM** | The cited URL substantiates **only** UltraSharp (CC BY-NC-SA); RealESRGAN/SUPIR/RMBG-2.0 need their own model-card sources. |

## Net

The gate-lane GO/NO-GO facts (allowlist, sandbox, metered API, hardware) are **all CONFIRMED** — they hold the whole readout. The `REFUTED`/`CANNOT_CONFIRM` verdicts are mostly *citation-precision* catches (wrong URL for a true fact, an overstated round number, a compound claim where one half failed) rather than fabrications — exactly the value a reasoning-stripped retrieval verifier adds. Corrections folded into the dispatch: SAM2→SAM3/SeC, MMAudio nesting, the "70+"/"no HTTP" overstatements, and license claims re-sourced to their LICENSE files.
