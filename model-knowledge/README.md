# model-knowledge

**Status:** Waves through 18 (STUDY-053 caption deepen 2026-09-07). Catalog **129 · 126/129 · 19 waves**. TTS invent: 0. JoyCaption Apache invent: 0. Pocket 127 stays.

- **Wave 18 (STUDY-053 caption deepen)** — [dispatch](waves/wave-18-study-053-caption-deepen/dispatch.md) · [research-raw](waves/wave-18-study-053-caption-deepen/research-raw.json) — extras-only; TTS invent: 0; JoyCaption Apache invent: 0; Pocket stays.

- **Wave 17 (STUDY-052 3D deepen)** — [dispatch](waves/wave-17-study-052-3d-deepen/dispatch.md) · [research-raw](waves/wave-17-study-052-3d-deepen/research-raw.json) — extras-only; Hunyuan flip: 0; Pocket stays; no Hunyuan Apache invent.

- **Wave 16 (STUDY-051 VIDEO VRAM)** — [dispatch](waves/wave-16-study-051-video-vram/dispatch.md) · [research-raw](waves/wave-16-study-051-video-vram/research-raw.json) — extras-only; A14B-32GB invent: 0; Pocket stays; GGUF unverified.

- **Wave 15 (STUDY-050 IMAGE deepen)** — [dispatch](waves/wave-15-study-050-image-deepen/dispatch.md) · [research-raw](waves/wave-15-study-050-image-deepen/research-raw.json) — extras-only; Pocket 127 stays; models invented: 0.

- **Wave 11 (STUDY-030 IMAGE deepen)** — [dispatch](waves/wave-11-study-030-image-deepen/dispatch.md) · [research-raw](waves/wave-11-study-030-image-deepen/research-raw.json) — 16 deepen sources; 0 new models; Pocket 127 untouched.
- **Wave 12 (STUDY-031 VIDEO deepen)** — [dispatch](waves/wave-12-study-031-video-deepen/dispatch.md) · [research-raw](waves/wave-12-study-031-video-deepen/research-raw.json) — 22 deepen sources; 0 new models; A14B-32GB invent: 0; Pocket 127 untouched.
- **Wave 13 (STUDY-032 3D deepen)** — [dispatch](waves/wave-13-study-032-3d-deepen/dispatch.md) · [research-raw](waves/wave-13-study-032-3d-deepen/research-raw.json) — 22 deepen sources; 0 new models; Hunyuan flip: 0; Pocket 127 untouched.
- **Wave 14 (STUDY-033 LLM/VLM/caption deepen)** — [dispatch](waves/wave-14-study-033-llm-caption-deepen/dispatch.md) · [research-raw](waves/wave-14-study-033-llm-caption-deepen/research-raw.json) — 21 deepen sources; 0 new models; TTS invent: 0; JoyCaption Apache invent: 0; Pocket 127 untouched.
A long-lived, **wave-appended** knowledge base of the best local generative-AI models
for this rig — what to run, what it's best for, what it costs in VRAM, whether it's
commercially licensable, and the **source backing every claim**. Plus a `workflows/`
folder for ComfyUI graphs.

Built for the **Robot rig** (HP Omen 45L · RTX 5090 · **32 GB VRAM** · Win 11). Every
recommendation is filtered for "runs well on 32 GB." Tuned for **both** game-asset
production (style consistency, LoRA-trainability, commercial-safe licensing) **and**
general creative / marketing — each model is tagged for both.

> Context: the local model library was wiped in a reformat. Wave 1 is therefore a
> **re-download priority guide** (`download_priority`, lower = grab first), not an
> inventory of what's on disk.

## Waves loaded

Counts are generated, never typed — see the status line above and [`catalog/README.md`](catalog/README.md), which the DB regenerates. Currently **129 models · 126/129 verified · 14 waves**.

- **[Catalog index](catalog/README.md)** — the commercial-safe re-download shortlist + per-domain tables (9 domains).
- **Wave 1 (foundation)** — [dispatch](waves/wave-01-foundation/dispatch.md) · [verification](waves/wave-01-foundation/verification.md)
- **Wave 2 (deep pass)** — [dispatch](waves/wave-02-deep/dispatch.md) · [verification](waves/wave-02-deep/verification.md)
- **Wave 3 (rounding)** — [dispatch](waves/wave-03-roundout/dispatch.md) · [verification](waves/wave-03-roundout/verification.md)
- **Wave 4 (tail)** — [dispatch](waves/wave-04-tail/dispatch.md) · [verification](waves/wave-04-tail/verification.md)

**Headline:** on this rig, *license* — not quality — is the deciding axis. The most-tutorialed models
(FLUX-dev, SUPIR, 4x-UltraSharp, Pony) are non-commercial; the commercial-safe core is Z-Image-Turbo +
Qwen-Image-2512 + Chroma (image), Wan 2.2 + LTX-2.3 (video), TRELLIS.2 + Hunyuan3D-2.1 (3D),
ACE-Step + Chatterbox (audio), Qwen3.6 + Gemma 4 (LLM). A LoRA inherits its **base model's** license —
train on SDXL/Qwen/Chroma for sellable assets.

## Why a database (not a markdown list)

The old `../MODEL-INDEX.md` was a flat hand-edited table — it went stale (it still
describes the 5080/12 GB era and SD1.5/SDXL as the frontier). This KB is queryable,
de-dupes across waves, links models ↔ purposes ↔ sources ↔ workflows, and keeps
**provenance**: every row knows which study-swarm wave produced it and whether the
external verifier confirmed it. New waves *append*; nothing silently overwrites.

One SQLite file (`models.db`) — not a multi-DB cluster. The "cluster" you want is the
**linked-table graph**, which is exactly what relational tables give you, while staying
portable and matching the repo-knowledge / swarm-control-plane tooling already on this rig.

## Layout

```
model-knowledge/
  README.md            <- you are here
  schema.sql           <- the table graph (idempotent; re-runs safely)
  models.db            <- the SQLite knowledge base
  catalog/             <- generated human-readable digests, one per domain
  workflows/           <- ComfyUI workflow .json files, by domain (see its README)
  waves/
    wave-01-foundation/
      dispatch.md         <- the research-grounding writeup (findings + implications)
      research-raw.json   <- raw verified swarm output (the load source)
      verification.md     <- what the adversarial verifier caught
  scripts/
    load_db.py          <- ingest a wave's research-raw.json into models.db
```

## The schema (linked-table graph)

| Table | Holds |
|---|---|
| `waves` | one row per study-swarm wave (provenance + how it was verified) |
| `categories` | the domains: image-base, image-control, video, 3d, audio, llm, comfy |
| `models` | every model + specs, VRAM, license, fit scores, status, `download_priority` |
| `purposes` + `model_purposes` | the "best model for *what*" matrix (many-to-many, with fitness + use-tag) |
| `sources` | the citation/evidence trail — every claim links to a URL + one-line finding |
| `custom_nodes` | essential ComfyUI custom nodes |
| `workflows` | ready-made workflow files + vetted workflow sources |
| `models_fts` | FTS5 full-text search over models |

Two convenience views: `v_recommended` (download shortlist by category) and
`v_best_for` (purpose → ranked models).

## Querying

```powershell
# the re-download shortlist, by category, priority order
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'model-knowledge/models.db').execute('SELECT category,dl,name,license,commercial_use,vram FROM v_recommended')]"

# best models for a purpose
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'model-knowledge/models.db').execute(\"SELECT * FROM v_best_for WHERE purpose LIKE '%concept%'\")]"

# full-text search
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'model-knowledge/models.db').execute(\"SELECT name FROM models_fts WHERE models_fts MATCH 'anime OR illustration'\")]"
```

## Loadout — pull only the slice you need (`ai-loadout`)

The catalog is ~120k tokens whole. You (or an agent) shouldn't read it all. An
[ai-loadout](https://www.npmjs.com/package/@mcptoolshop/ai-loadout) dispatch table at
`.claude/loadout/index.json` routes a task to just the relevant entries: a tiny always-on
orientation entry (the catalog index, ~800 tok) plus the 1–3 domain catalogs the task needs.
Generated from the DB by `scripts/gen_loadout.py`, re-run each wave.

```powershell
ai-loadout validate .claude\loadout\index.json          # structural check
ai-loadout budget   .claude\loadout\index.json           # token breakdown
ai-loadout resolve  --project model-knowledge --json
```

Agents integrate via `planLoad(task)` (from `@mcptoolshop/ai-loadout`) → preload / on-demand /
manual sets within budget. Measured routing: *"install comfyui + nodes"* loads ~4% of the KB;
*"image-to-video for marketing"* ~13%; *"commercial-safe game concept art"* ~20% — never the whole thing.
The raw swarm JSON is a `manual` entry (never auto-loaded).

## Starter workflows

`workflows/` is seeded with 16 official **local-model** starter graphs from
`Comfy-Org/workflow_templates` (fetched by `scripts/fetch_workflows.py`), covering the
commercial-safe core (Z-Image, Qwen-Image/-Edit, Chroma, SDXL, Wan i2v/t2v, LTX, Hunyuan3D,
ACE-Step, Chatterbox, FILM interpolation) plus a couple of non-commercial canonical ones
(Flux Kontext/Fill) clearly labelled. They're registered in the DB (`workflows` table, `wave 0 = local`).

## Where downloads go (storage convention)

Aligned with the established convention (memory: `feedback_models_live_on_f.md`,
F:→E: on this rig). **Set `HF_HOME` before pulling anything**, or it lands on C:.

| Class | Path |
|---|---|
| ComfyUI single-file checkpoints / unets / LoRAs / VAE / controlnet / upscalers | `E:\AI-Models\ComfyUI\models\<class>\` |
| HuggingFace cache (diffusers, gated, tokenizers) | `E:\AI-Models\hf-cache\` → `$env:HF_HOME` |
| Ollama models | `E:\AI-Models\Ollama\` (`OLLAMA_MODELS`) |
| LoRA training outputs | `E:\AI-Models\<project>\loras\` |

Runtime + how generations are driven: see memory `comfyui-setup.md` — ComfyUI at
`E:\AI-Models\ComfyUI-runtime\`, plus the `comfy-headless` Python client (v2.5.2) for
programmatic generation. **Per-game** style profiles live separately under
`style-dataset-lab/projects/<game>/workflows/profiles/` — this KB is the general
model/workflow catalog, not a replacement for those.

## Adding the next wave

This is wave 1 of many. Later waves go deep where wave 1 went broad (e.g. "Wave 2:
SDXL-vs-Flux LoRA training deep-dive", "Wave 3: local video pipeline shootout").

1. Dispatch the research+verify swarm (see `scripts/` and the wave-01 dispatch as the template).
2. Drop its verified output at `waves/wave-NN-name/research-raw.json` with `{ "wave": NN, "date": "YYYY-MM-DD", "lanes": [...] }`.
3. `python scripts/load_db.py waves/wave-NN-name/research-raw.json` — idempotent; re-running replaces that wave's rows. Then `python scripts/gen_catalog.py` and `python scripts/gen_loadout.py` to refresh the catalog + loadout index (`ai-loadout validate .claude/loadout/index.json` to confirm).

## Verification (how much to trust a row)

Each wave's claims pass an adversarial, reasoning-stripped verifier that uses web
retrieval as an existence/license/spec oracle before a row is trusted (`models.verified`,
`sources.verified`). Wave 1 uses a same-model-family verifier with a retrieval oracle;
the **family-different** path (route through `prism verify` / `roleos verify-citations`,
both already shipped in this org, ideally with a *local* non-Claude model on this 32 GB
rig per `hardware-omen-45l.md`) is the planned upgrade for a later wave. Treat
`verified=0` rows as leads to confirm, not gospel.
