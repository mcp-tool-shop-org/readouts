# Wave 4 — Measured rig baseline (RTX 5090, Ollama)

**Measurement wave** · 2026-06-02 · **not a research swarm — measured live on the actual rig.** The first time the KB's sourced claims meet the metal. Builds on the [profiling-bench lane](../../catalog/profiling-bench.md) (wave 3) — which supplied the method (nvidia-smi dmon).

## Context

- **Rig (confirmed live):** NVIDIA GeForce RTX 5090 · **32607 MiB (32 GB)** · driver **610.47** · CUDA UMD **13.3** · **WDDM** (Windows 11). Idle: **16 W / 575 W cap · 28°C · 2% SM · 405 MHz mem / 476 MHz core · P8**, ~2287 MiB used by desktop apps (the VRAM floor).
- **Engine:** **Ollama 0.24.0** (llama.cpp backend), default quant (~Q4_K_M) + default context. The studio's actual local-LLM stack. No torch/llama.cpp-standalone/ComfyUI present at measurement time.
- **Why:** turn the sourced config recipes into **rig-truth** and establish a thermal/power/throughput baseline the studio can plan against.

## Method

Per model: warm (load into VRAM), then a **sustained ~60–75 s soak** = 2–4 back-to-back 2000-token generations via the Ollama API, while sampling the GPU at 1 s with `nvidia-smi dmon`. Decode tok/s = `eval_count / eval_duration` (API timing); the load-window = dmon samples with SM-util > 30%. Raw logs: [`baselines/`](../../baselines/) (`idle.dmon.txt` + `load_<model>.dmon.txt`).

## The baseline

| Model | Type | Decode tok/s | Prompt tok/s | VRAM (of 32 GB) | Power avg / peak | Temp avg / peak | Core clock | Throttle |
|---|---|---|---|---|---|---|---|---|
| **qwen3.6:35b-a3b** | MoE (3B active) | **138.8** | 999 | 28.4 GB | 256 / **271 W** | 45 / **48°C** | 2881 MHz | none |
| **translategemma:12b** | dense 12B | 126.7 | 3086 | 13.4 GB | 435 / 463 W | 64 / 67°C | 2872 MHz | none |
| **gemma4:31b** | dense 31B | 60.4 | 2364 | 28.2 GB | 480 / **503 W** | 58 / 66°C | 2883 MHz | none |
| **qwen3.6:27b** | dense 27B | 57.5 | 746 | 26.8 GB | 419 / 442 W | 49 / 56°C | 2895 MHz | none |
| *idle* | — | — | — | 2.3 GB | 16 W | 28°C | 405/476 MHz | P8 |

## What it means for the studio

- **The 5090 is not thermally or power constrained for single-stream local LLM.** Peak temp across everything was **67°C** (throttle ~88°C → >20°C headroom); peak power **503 W** (cap 575 W → 72 W headroom); the core held **full ~2880 MHz boost on every model with zero throttle**. You can run the local crew all day without thermal worry.
- **The MoE is the efficiency king.** qwen3.6:35b-a3b hits **138.8 tok/s at only 256 W / 48°C** — because just 3B of its params are active per token (memory-bandwidth-bound, not compute-bound). For sustained crew work where speed + coolness + power matter, this is the pick.
- **Dense 27–31B models** run **57–60 tok/s** and use **~26–28 GB** — they fit with 4–6 GB headroom, but the dense compute pulls **420–503 W** (gemma4:31b is the hungriest). 
- **The 12B** runs **127 tok/s** in **13.4 GB**, leaving room for a co-resident model or a much larger context window.
- **The real limiters are VRAM (for >30B dense) and single-stream decode speed — not heat or power.** That reframes upgrade/scaling decisions: headroom exists for bigger context, a second resident model, or batched/concurrent serving (which waves 1–2 noted needs WSL2 vLLM for true continuous batching).

## Sustained thermal soak — 9.5 min, gemma4:31b (worst case)

The 4-model table is a ~75 s snapshot. For true steady-state, the highest-power model (gemma4:31b) was held under continuous load for **9.5 minutes** (15 generations / 30,000 tokens, sustained **61.3 tok/s**), sampled at 1 s:

| Elapsed | Temp avg / max | Power avg | Core clock |
|---|---|---|---|
| 0–95 s | 55 / 65°C | 481 W | 2881 MHz |
| 95–190 s | 69 / 71°C | 503 W | 2837 MHz |
| 190–285 s | 71 / 71°C | 513 W | 2872 MHz |
| 285–475 s | 71 / 72°C | 512 W | 2852 MHz |
| 475–570 s | 69 / **74°C** | 511 W | 2871 MHz |

**It plateaus at ~71°C by the 3-minute mark and holds it** (peak 74°C) for the rest of the soak — it does **not** keep climbing. Power 506 W avg / 547 W peak (cap 575 W); core clock held ~2861 MHz full boost; **zero thermal throttle** (steady 71°C is 14°C under the ~88°C limit). **The rig sustains worst-case LLM inference indefinitely at ~71°C with full performance.**

## bytefit — loadout planning (getting the most out of 32 GB)

[bytefit](https://github.com/mcp-tool-shop-org/bytefit) (in-org, MIT — now an engine row in this lane, run live) probed the rig (**1792 GB/s** GDDR7 bandwidth) and planned every Ollama model. Headroom finding: the **qwen3.6 family runs full 128 K context entirely in VRAM** (qwen3.6:27b ~60 t/s with KV just 4 GiB; the MoE ~117 t/s, KV 1.3 GiB — heavy GQA), while **gemma4 / granite / aya degrade to 5–29 t/s at 128 K** (KV spills to RAM; bytefit refuses it) → for long-context crew work use Qwen3.6; gemma4 is short-context here. Optimal emitted loadout, e.g. `llama-server -m qwen3.6:27b.gguf -c 131072 -ngl 64 -ctk q8_0 -ctv q8_0 -fa on`. **Calibration vs the measured table:** bytefit matched the MoE (132 vs 138.8) and gemma4 (60 vs 60.4) but over-predicted dense models ~25–29% (qwen3.6:27b 74 vs 57.5) — its bandwidth roofline omits attention/KV/WDDM overhead, so discount dense estimates ~20–25%.

## Cooling — the OMEN Cryo Chamber + safe fan headroom

The 45L's patented **Cryo Chamber** is the top compartment housing the **240 mm CPU AIO radiator**, isolated from the main case so it pulls fresh ambient air (HP claims ~6°C lower CPU temps) — it cools the **CPU, not the GPU** (the 5090 is air-cooled in the main chamber by its own VBIOS-curve fans + case airflow). **GPU power limit is already maxed** (575 W default = max; min 400 W → can only be lowered). GPU fan is VBIOS-auto (nvidia-smi can't set it on consumer/WDDM). The **safe fan lever is OMEN Gaming Hub** (installed): Performance Mode / Max-Fan Mode / Thermal-Control→Manual slider. Given the soak plateaued at 71°C, more cooling isn't needed for LLM work — it's headroom for heavier future loads.

## Reproduce / extend

The exact harness (warm → 60 s soak loop via `/api/generate` → `nvidia-smi dmon -c N` in a background job → parse SM>30% window) is in this session's wave-4 PowerShell. To extend the baseline:
- ✓ **Longer thermal soak — done** (see the soak section above): plateaus ~71°C, no throttle. A multi-hour soak would only test dust/fan drift over time.
- **Concurrency / batched** throughput (WSL2 vLLM, per the serving lane) — the single-stream numbers here are the floor, not the throughput ceiling.
- **Prompt-length sweep** (prefill scaling) and **KV-cache-quant** comparisons (the wave-2 recipes: `-fa --cache-type-k q8_0`).
- **Diffusion baseline** once ComfyUI is installed (the diffusion-engines lane) — SDXL/Flux it/s + VRAM + thermals.

## Provenance note

This wave records **measured** data, so the EXTERNAL_VERIFIER stage is replaced by **reproducibility**: the method + raw `dmon` logs are committed so any later run can re-measure and compare. The numbers are tagged in the DB as `config_recipes` rows with `kind='baseline'` under the `profiling-bench` lane (queryable: `SELECT name, body FROM config_recipes WHERE kind='baseline'`).
