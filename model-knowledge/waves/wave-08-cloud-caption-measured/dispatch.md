# Wave 8 — Cloud caption, measured (2026-08-19)

**The second empirical wave** (wave 7 established the class). Provenance: facts measured on this
account and this rig during the 3-round **captioner dialog** with the Comfy Cloud in-app agent
(2026-08-19, closed both sides), with every load-bearing claim re-verified at ingest — the
billing feed re-pulled live, the graph matched widget-for-widget against the ordered spec, the
editor form passed a mechanical link↔node cross-reference, the HF license tag re-fetched, the
local engine pin grepped from source. Full receipts:
`dialogs/comfy-agent/` (private) (captioner rounds 01–03) and
[`workflows/caption/`](../../workflows/caption/README.md).

**Why this wave exists:** the captioner thread caught our own KB asserting something false —
waves 1/3 marked cloud Florence-2 **"credit-FREE on the cloud GPU."** Measurement killed it. The
wave also lands the local native-transformers pin discovered the same day on `plain-sight`
(microsoft/* checkpoints no longer load natively), so both Florence-2 rows now carry the
corrected cloud economics AND the corrected local runtime path.

## The measured facts (the wave's core payload)

### The correction — cloud Florence-2 is NOT credit-free

| Job | GPU-sec (billed) | ≈ credits @0.266 | What it bought |
|---|---|---|---|
| `caption-florence2-v1` confirmation (beach.jpg) | **6.73** (`26a78ccd…`, rtx_pro_6000, 2026-08-20T02:00Z) | **~1.8** | one `more_detailed_caption` + paired .txt sidecar |

- OSS-node captioning bills **active GPU seconds** exactly like the audio jobs — there is no
  free class of cloud jobs. The waves-1/3 "credit-free" notes are superseded on both Florence-2
  rows.
- **Verifier catch at ingest:** the intake's derived "~1.3 credits/caption" does not reproduce —
  6.73 × 0.266 ≈ **1.8**. The wave records ~1.8 (derived, advisory); `gpu_seconds` is the
  authoritative per-job figure (per-job dollar cost is not exposed).
- Cheap enough for the **metadata-rider lane** (caption outputs where they're born, in-cloud);
  ruinous economics never claimed for bulk — which is one-image-per-job anyway (below).

### The local pin — microsoft/* no longer loads natively

Native transformers (≥4.51, verified on 5.15.1) dies loading `microsoft/Florence-2-*`
(`RobertaTokenizer has no attribute image_token`; pre-native configs) unless
`trust_remote_code=True`. **Pin `florence-community/Florence-2-large`** — the official
native-transformers conversions, same weights, HF license tag **mit** (re-pulled live at
ingest; 441k downloads/mo). Measured on the 5090 (`plain-sight` v0.1.0, commit `fdd49b3`,
which pins it as `DEFAULT_MODEL_ID`): fp16 ≈ **1.5 GB VRAM**, ≈ **1.0 s** per
`more_detailed_caption`, deterministic repeat confirmed (`do_sample=False`, `num_beams=3`).
The cloud kijai loader is unaffected (it uses trust_remote_code) — the pin is for local
bulk-captioning runtimes.

### Determinism — cloud captions are stochastic by default

`Florence2Run` ships `do_sample=BOOLEAN default TRUE` — the pinned-seed convention applies:
production graphs set `do_sample=false` + fixed `seed` (the archived graph does), making
re-caption runs reproducible and cache-priced.

### The split — cloud rider vs local bulk

- **One image per job** headlessly: no API-valid directory iterator in the catalog (the "batch"
  nodes operate on in-memory IMAGE batches, no per-file filenames). Bulk dataset captioning
  stays on the local 5090; the cloud tool captions outputs where they're born. (Agent-reported;
  advisory.)
- **Florence-2 family is the OSS in-cloud captioning ceiling** — no JoyCaption / InternVL /
  MiniCPM-V / Qwen-VL packs on the shelf; the KB's 8B-class deep-caption lane stays local.
  Gemini subgraph = partner-ToS, unclear-until-read. (Agent-reported; advisory.)
- **`prompt_gen_*` stays off the commercial menu**: those tasks belong to MiaoshouAI PromptGen
  fine-tunes (license unverified our side); MIT covers `microsoft/Florence-2-*` originals only,
  and the base checkpoints don't carry the PromptGen task tokens — pin and task menu move
  together.

### The trap ledger (headless law, three new entries)

1. **WAS `Text Concatenate` `text_a–d` are link-only inputs** — feed with `PrimitiveString`
   nodes, never widget values (first delivery batch was rejected clean on this).
2. **`delimiter` defaults to `", "`** — explicitly zero it for bare prefix+caption+suffix.
3. **Content-addressed storage:** an `/api/view` hash filename is NOT a pairing failure — the
   logical name rides the download's `content-disposition` (judge pairing there). SaveText
   appends `_00001`; strict sidecars take a counter-strip rename at download.

## Catalog deltas (3 `model_updates`)

| Model | Cloud axis | The wave-8 fact |
|---|---|---|
| Florence-2 large (caption row, `florence-2-large-2`) | yes (**measured** — supersedes wave-3 "credit-FREE") | 6.73 GPU-sec ≈ ~1.8 cr/caption; measured graph + pairing recipe; stochastic-by-default warning; one-image-per-job; OSS ceiling; PromptGen posture; local pin `florence-community` |
| Florence-2 (large) (llm row, `florence-2-large`) | yes (**measured** — supersedes wave-1 "credit-free") | same correction, condensed; cross-references the caption row |
| Qwen3-VL (llm row, `qwen3-vl`) | partial (billing phrasing corrected) | ingest audit caught the same wave-1-era "runs credit-free" falsehood on this row — superseded by the measured billing model (no free class of cloud jobs); pack presence still unexercised/advisory |

Platform facts recorded as comfy-lane entries: `Florence2Run`/loader schema (verified live),
`LoadImageWithFilename_EditUtils` in-graph pairing (measured), WAS Text Concatenate traps
(measured), content-addressed storage (measured), one-image-per-job (agent-reported), and the
no-credit-free-job-class billing measurement.

## The production workflow (archived, validated, run)

| Graph | Cloud record | Confirmation run | Archive |
|---|---|---|---|
| LoadImageWithFilename → Florence-2-large `more_detailed_caption` → prefix/suffix concat → SaveText txt (paired filename) | `b26cb8b5-0153-4279-9c3a-593857fbff6b` | `26a78ccd…` 6.73 GPU-sec | [`workflows/caption/caption-florence2-v1.json`](../../workflows/caption/caption-florence2-v1.json) (+ `.api.json`, server-emitted) |

Archived editor JSON passed the mechanical link↔node cross-reference (7 nodes / 7 links); the
api form matched the ordered spec widget-for-widget. Confirmation artifact:
[`workflows/caption/beach_00001.txt`](../../workflows/caption/beach_00001.txt) (454 B, five
sentences, tier as advertised). Model manifest + trap ledger:
[`workflows/caption/README.md`](../../workflows/caption/README.md).

## Standards note

The shipped workflow performs **no irreversible operations** — runs write new output files to
cloud storage and spend metered credits (measured above); re-runs on the pinned seed are
cache-priced. No compensators table required (nothing to undo); the andon lever in the ingest
pipeline remains the loader's hard-fail on unmatched `model_updates` slugs. PIN_PER_STEP is
satisfied by the archived graph (exact class/values/model per node) + cloud `workflow_id` + job
id. EXTERNAL_VERIFIER: ground truth for every Class A fact is the platform's own
billing/storage/API and the HF API — no LLM in the verification loop (see verification.md).

## Re-ingest ordering (loader contract)

`model_updates` waves (6, 7, 8) modify rows owned by earlier waves. Re-ingesting an older wave
**replaces its model rows and discards later waves' updates to them** — after re-ingesting wave
N, re-run every wave > N that carries `model_updates` (5 → 6 → 7 → 8 to rebuild from scratch).
The loader hard-fails (nothing committed) if an update slug matches no row.

## Provenance

- Method: 3-round Comfy-Agent captioner dialog (rounds 01–03 archived verbatim with replies and
  pull receipts in `dialogs/comfy-agent/`), advisor-side verification over the official API/MCP,
  plus the same-day local `plain-sight` build receipts (E:/AI/plain-sight, v0.1.0 `fdd49b3`).
- Verification receipt for this wave: [verification.md](verification.md) — measured vs
  agent-reported split, the live re-pulls performed at ingest, and the two corrections to our
  own KB (credit-free claim; ~1.3 → ~1.8 arithmetic).
- Supersession: waves 1/3 Florence-2 "credit-free" cloud notes are superseded here — the second
  proof (after wave 7's Chatterbox flip) that the freshness rule earns its keep.
