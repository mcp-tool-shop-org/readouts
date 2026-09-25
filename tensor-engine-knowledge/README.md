# tensor-engine-knowledge

**Status:** Waves through 17 (STUDY-060 MLC-LLM / bytefit honesty 2026-09-07). Catalog **193 · 134/193 · 17 waves**. Flips 12/143: 0. Invented tok/s: 0.

- **Wave 17 (STUDY-060 MLC-LLM / bytefit honesty)** — [dispatch](waves/wave-17-study-060-mlc-bytefit-honesty/dispatch.md) · [research-raw](waves/wave-17-study-060-mlc-bytefit-honesty/research-raw.json) — 22 engines verified=0; flips 12/143: 0; invented tok/s: 0.
- **Wave 16 (STUDY-039 MLC-LLM + bytefit deepen)** — [dispatch](waves/wave-16-study-039-mlc-bytefit-deepen/dispatch.md) · [research-raw](waves/wave-16-study-039-mlc-bytefit-deepen/research-raw.json) — 22 engines verified=0; flips 12/143: 0; invented tok/s: 0.
A long-lived, **wave-appended** knowledge base of the **tensor / inference / training
engines** — the *software* that runs and trains AI models locally: LLM inference runtimes,
serving layers, quantization frameworks, attention/GPU kernels, fine-tuning engines,
diffusion accelerators, and the foundational runtimes underneath. For each engine: what it
is, what it's best at, the model formats it runs, whether it's **Blackwell/Windows-ready**,
how it's **licensed**, how well it fits this rig — and the **source backing every claim**.

> This is KB #2 of the [readouts](../README.md) monorepo. Its sibling
> [model-knowledge](../model-knowledge/) catalogs the **models**; this one catalogs the
> **engines that run them**. Build models with `model-knowledge`; choose and tune the
> engine to run/train them with this KB.

Built for the **Robot rig** — HP OMEN 45L · RTX 5090 · Blackwell sm_120 · **32 GB VRAM** ·
Core Ultra 9 · **64 GB system RAM** · Windows 11. The only machine. Every recommendation is
filtered for "runs well **on Windows** on a Blackwell 5090," with **`rig_fit`** (this exact
rig) and **`studio_fit`** (local single-user studio workload vs datacenter-only tooling)
scored on every engine. Windows-native support is treated as load-bearing — many engines are
Linux-first or need WSL2, and the catalog says so honestly.

## Waves loaded

Counts are generated, never typed — see the status line above and [`catalog/README.md`](catalog/README.md), which the DB regenerates. Currently **171 engines · 133/171 verified · 16 waves**.

- **[Catalog index](catalog/README.md)** — the fastest-install shortlist + per-lane tables (10 lanes).
- **Wave 1 (foundation)** — best engine per lane — [dispatch](waves/wave-01-foundation/dispatch.md) · [verification](waves/wave-01-foundation/verification.md)
- **Wave 2 (deep)** — +18 engines + 56 version-pinned config recipes (the "configure properly" layer) — [dispatch](waves/wave-02-deep/dispatch.md) · [verification](waves/wave-02-deep/verification.md)
- **Wave 3 (expansion)** — +3 lanes (structured-output · speech-engines · profiling-bench) +39 engines — [dispatch](waves/wave-03-expansion/dispatch.md) · [verification](waves/wave-03-expansion/verification.md)
- **Wave 4 (measured baseline)** — real RTX 5090 thermals/power/throughput on Ollama + a 9.5-min soak (plateau **~71°C**, no throttle) + **bytefit** loadout planning (qwen3.6 holds **128K context in VRAM**) + the Cryo-Chamber/fan story — [report](waves/wave-04-baseline/dispatch.md) · raw logs in [baselines/](baselines/)
- **Wave 5 (recipe-proving II)** — three engines proven hands-on, all native-Windows: **llama.cpp (prebuilt CUDA-12 b9484) → llama-swap** (MMQ confirmed pp512 **7251** t/s; name-routed serving + TTL VRAM reclaim) · **SageAttention 2.2.0** (cu130 abi3 wheel; win scales **8→29%** with resolution; fp8_cuda best, fp16_cuda crashes Lumina2) · **Unsloth LLM-QLoRA** (Qwen3-4B, ~6 GB VRAM, completes the training pair) — recipes #152–155 · raw in [baselines/](baselines/)
- **Wave 6 (wiring)** — `offload` wired into the real workflows so it cuts Claude tokens in use, not on disk: a family-different **local verifier panel** (Qwen3-4B + Qwen3-14B + Mistral-Nemo-12B) added as a second seat in **`roleos verify-citations --local-panel`** (0 false-confirms re-proven on a real 16-case arXiv set — the panel caught a single model's false-confirm); **pre-read `compress`** measured **92.1%** Claude-token reduction on real wave artifacts; an **ollama-intern companion** verifier — recipes #162–164 · receipts in [verifier/](verifier/)

Ten lanes: `llm-inference` · `llm-serving` · `structured-output` · `quantization` · `attention-kernels` ·
`training` · `speech-engines` · `diffusion-engines` · `runtime-foundations` · `profiling-bench`.

**Headline:** on this rig the deciding axis is *native-Windows Blackwell survivability*, not throughput. The
datacenter throughput kings (vLLM, SGLang, TensorRT-LLM, Triton) are Linux-first → WSL2; the native-Windows
studio core is **llama.cpp / Ollama / ExLlamaV3** (inference), **llama-swap** (serving), **GGUF + EXL3** (quant),
**cuDNN-SDPA + SageAttention** (kernels), **TRL + PEFT / kohya_ss** (training), **ComfyUI + Nunchaku** (diffusion),
**PyTorch-cu130 + ggml** (foundations). Four load-bearing Blackwell gotchas — CUDA **12.8** for llama.cpp but
**cu130** for PyTorch; sm_120 **can't run FA3/FA4**; **never `pip install xformers`**; **64 GB RAM** unlocks
MoE/offload — are in the [dispatch](waves/wave-01-foundation/dispatch.md).

## Why a database (not a markdown list)

The engine landscape moves fast and the decision is multi-axis — *license* (GPL vs Apache vs
custom), *Blackwell/Windows readiness*, *which model formats it loads*, *what it optimizes for*
(throughput vs latency vs memory), and *fit for one powerful workstation vs a datacenter*. A
flat list goes stale and can't answer "best engine to run a 32B GGUF on Windows with the most
throughput." This KB is queryable, de-dupes across waves, links engines ↔ purposes ↔ sources
↔ config-recipes, and keeps **provenance**: every row knows which research wave produced it
and whether the external verifier confirmed it. New waves *append*; nothing silently overwrites.

One SQLite file (`engines.db`) — the "cluster" is the **linked-table graph**, matching the
`model-knowledge` / repo-knowledge tooling already on this rig.

## Layout

```
tensor-engine-knowledge/
  README.md            <- you are here
  schema.sql           <- the table graph (idempotent; re-runs safely)
  engines.db           <- the SQLite knowledge base
  catalog/             <- generated human-readable digests, one per lane (never hand-edited)
  recipes/             <- optional companion files (config snippets, benchmark dumps)
  waves/
    wave-01-foundation/
      dispatch.md         <- the research-grounding writeup (findings + install plan)
      research-raw.json   <- raw verified swarm output (the load source)
      verification.md     <- what the adversarial verifier caught
  scripts/
    load_db.py          <- ingest a wave's research-raw.json into engines.db (idempotent)
    gen_catalog.py      <- DB -> catalog/*.md
    gen_readout.py      <- DB -> readout/readout-<domain>.html (branded, JSON-driven; all domains by default)
    gen_index.py        <- DB -> readout/index.{html,md,json} (the agent-first home)
    gen_loadout.py      <- DB -> .claude/loadout/index.json (ai-loadout progressive disclosure)
    regen.py            <- one command: catalog + readouts + index + loadout + root + validate
  readout/              <- the OUTPUT pillar: standalone catalog readouts + index (human AND agent)
  .claude/loadout/index.json
```

## The schema (linked-table graph)

| Table | Holds |
|---|---|
| `waves` | one row per research wave (provenance + how it was verified) |
| `categories` | the lanes: llm-inference, llm-serving, quantization, attention-kernels, training, diffusion-engines, runtime-foundations |
| `engines` | every engine + type, language, version, platforms, accelerators, model_formats, `blackwell_ready`, license, `rig_fit`/`studio_fit`, status, `download_priority` |
| `purposes` + `engine_purposes` | the "best engine for *what*" matrix (many-to-many, with fitness + use-tag) |
| `sources` | the citation/evidence trail — every claim links to a URL + one-line finding |
| `config_recipes` | the **how-to-configure/optimize-properly** layer — named, sourced recipes + tools per lane |
| `engines_fts` | FTS5 full-text search over engines |

Two convenience views: `v_recommended` (install shortlist by lane) and
`v_best_for` (purpose → ranked engines).

## Querying

```powershell
# the install shortlist, by lane, priority order
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'tensor-engine-knowledge/engines.db').execute('SELECT category,dl,name,license,bw,rig,studio FROM v_recommended')]"

# best engines for a purpose
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'tensor-engine-knowledge/engines.db').execute(\"SELECT * FROM v_best_for WHERE purpose LIKE '%throughput%'\")]"

# full-text search (e.g. everything that loads GGUF)
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'tensor-engine-knowledge/engines.db').execute(\"SELECT name FROM engines_fts WHERE engines_fts MATCH 'gguf OR llamacpp'\")]"
```

## Loadout — pull only the slice you need (`ai-loadout`)

The catalog is large whole. An [ai-loadout](https://www.npmjs.com/package/@mcptoolshop/ai-loadout)
dispatch table at `.claude/loadout/index.json` routes a task to just the relevant lanes: a tiny
always-on orientation entry (the catalog index) plus the 1–3 lane catalogs the task needs.
Generated from the DB by `scripts/gen_loadout.py`, re-run each wave.

```powershell
ai-loadout validate .claude\loadout\index.json
ai-loadout resolve  --project tensor-engine-knowledge --json
```

## Readouts — the output pillar (`gen_readout.py` + `gen_index.py`)

The DB also renders to **standalone, brand-correct readouts** — the product face of the KB, in `readout/`:

- `readout-<domain>.html` — one self-contained file per lane: a filter/sort table of every engine with
  license / blackwell / rig-fit chips, click-to-expand detail and the full source + verify trail. It's
  JSON-driven (a `<script type="application/json">` data island), so a human reads it in a browser and an
  agent parses the same file. ~70–115 KB, zero dependencies, dark default + light toggle.
- `index.{html,md,json}` — the home, designed **agent-first**: `index.md` is the clean text map an agent
  reads in one shot; `index.json` is the programmatic map; `index.html` is the branded landing whose content
  lives in semantic markup + a JSON island (so `get_page_text` still yields the full map). Every domain links
  to its readout; an explicit "For agents" callout points at `index.md` and the `engines.db` views.

Regenerated from `engines.db` each wave by `regen.py` (or `python scripts/gen_readout.py <domain>` for one).

## Adding the next wave

This is wave 1 of many — broad foundation now; later waves go deep where this went wide
(e.g. "Wave 2: vLLM vs SGLang vs TensorRT-LLM throughput shootout + exact Blackwell configs",
"Wave 3: the Windows quantization-format compatibility matrix", "Wave 4: single-GPU QLoRA tuning").

1. Dispatch the research+verify swarm (template: `scripts/wave-swarm.workflow.js` — one
   web-grounded researcher + one reasoning-stripped retrieval-verifier per lane).
2. Extract the workflow payload (it lands under `result` in the harness envelope) to
   `waves/wave-NN-name/research-raw.json` as `{ "wave": NN, "date": "YYYY-MM-DD", "lanes": [...] }`.
3. `python scripts/load_db.py waves/wave-NN-name/research-raw.json` — ingest the wave (idempotent;
   re-running replaces that wave's rows).
4. `python scripts/regen.py` — rebuilds **every** derived artifact from the DB (catalog + readouts +
   index + both loadouts) and validates the indexes. One command, idempotent; it forces UTF-8 for the
   sub-steps (entries carry em-dashes). Run one domain with `python scripts/gen_readout.py <domain>`.

## Verification (how much to trust a row)

Each wave's claims pass an adversarial, **reasoning-stripped** verifier that uses live web
retrieval as an existence/license/spec/currency oracle before a row is trusted
(`engines.verified`, `sources.verified`). Wave 1 uses a *different-tier* verifier (Sonnet)
plus the retrieval oracle (the live page is the decorrelating element). The **family-different**
path landed in **wave 6**: a *local* non-Claude entailment **panel** (Qwen3-4B + Qwen3-14B +
Mistral-Nemo-12B on llama-swap, via the `offload` CLI) is wired into
**`roleos verify-citations --local-panel`** as a decorrelated second seat — measured **0
false-confirms** (it never stamps a false claim "supported"), re-proven on a real 16-case arXiv
set where it caught a single model's false-confirm
([verifier/citation-panel-receipt.json](verifier/citation-panel-receipt.json)). Treat `verified=0`
rows as leads to confirm, not gospel.
