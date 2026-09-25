# Wave 7 — Cloud audio, measured (2026-08-19)

**The first empirical wave.** Waves 1–6 were web-retrieval swarms verified by re-fetching pages;
wave 7's provenance is a different class: **facts measured on this account** during a 5-round
dialog with the Comfy Cloud in-app agent (2026-08-18 → 19), with every load-bearing claim
re-verified from this rig over the official API — jobs re-billed from the account feed, graphs
re-pulled by `workflow_id`, outputs re-downloaded and header-decoded byte-for-byte, LUFS
manifests read. Full receipts: `dialogs/comfy-agent/` (private)
(rounds 01–05). The wave exists to make those facts **queryable next to the other 122 models**
and to hand [[motif]] a locked, receipt-backed generation layer.

**Why a dialog instead of a swarm:** the in-app agent sees the *live cloud catalog* (node
classes, template IDs, availability) that web scraping lags on; our KB holds
*adversarially-verified license ground truth*. Each round cross-checked one against the other —
and both directions produced corrections (see verification.md). The dialog protocol, naming, and
provenance rules are documented in the dialogs README and are reusable for the next domain
(video, 3D) verbatim.

## The measured facts (the wave's core payload)

### Costs — the budget question is retired

| Job | GPU-sec (billed) | ≈ credits @0.266 | What it bought |
|---|---|---|---|
| ACE-Step 120 s track + 4-stem split + LUFS | 29.7–31.9 | **~8** | full Motif music unit |
| SA3 Medium ~10 s SFX, uncached | 9.8–10.0 | **~2.6** | one SFX candidate |
| Identical-graph re-run (cache hit) | 1.1–1.2 | **~0.3** | free re-verification |

- **Billing counts active GPU seconds, not wall-clock** — the 170 s music job billed 31.9 s;
  queue and model-load time cost nothing. (Empirically confirms wave 6's pricing facts.)
- The Creator pool (7,400 credits/mo) buys ≈ **870 track+stem units/month**. The entire
  four-round dialog — every build, test, and confirmation — cost **≈ 44 credits (0.6%)**.
- Per-job dollar cost is not exposed anywhere; `gpu_seconds` from the billing activity feed is
  the authoritative per-job figure (the in-app agent cannot see it; our MCP/API side can).

### Determinism — cue families are safe

Identical graph + fixed seed re-ran as a **whole-graph cache hit** (1.16 GPU-sec, 1.65 s wall).
Generation is bit-stable on pinned seeds → any Motif cue can be regenerated exactly, and
re-verifying an already-run graph is nearly free. Corollary for graph design: **one shared seed
primitive feeds every stochastic node** (both archived workflows do this).

### Sample rates — the mismatch nobody advertised

| Output | Rate | Receipt |
|---|---|---|
| ACE-Step 1.5 mix decode | **48,000 Hz** 16-bit, honors duration exactly (5,760,000 samples = 120.000 s) | FLAC header decode |
| Demucs (`AudioSeparation`) stems | **44,100 Hz** — Demucs native, regardless of input rate | header decode, all 4 stems |
| SA3 Medium decode | **44,100 Hz**; duration snaps to the latent grid (3.0 s → 2^17 samples = 2.972 s; 10 s → 10.031 s) | header decode |

The music graph's own outputs are internally rate-mismatched **by design** (48 k mix, 44.1 k
stems). Locked decision: **Motif's runtime standard is 48 kHz; stems and SFX are resampled at
ingest** (we own the resampler); tooling always reads *actual* duration from the file, never the
requested figure — the Comfy Agent has logged grid-snapping as expected behavior it will not
silently "correct."

### LUFS — loudness is in the manifest now

`AudioLoudnessMeter.loudness_info` (STRING) reaches the headless output manifest only via
`SaveText`. Both production graphs wire it; the manifest line is a parseable one-liner —
`Integrated Loudness: -12.32 LUFS` (music confirmation run) / `-21.94 LUFS` (SFX pin).
**Integrated** LUFS confirmed. Motif normalizes at ingest (−12.32 is hot against a −16…−14
music-bed target); the meter-to-file wiring ships by default on all future music builds.

### The trap ledger (headless law)

1. **UI-only nodes never reach `/api/prompt`** — the template `CustomCombo` and the
   `PrimitiveNode` "Song Duration" both validate in the editor and silently vanish headlessly.
   Use `PrimitiveFloat` / `PrimitiveInt`. Both archived graphs are validated headless-clean.
2. **`SaveAudioMP3` is deprecated** in core — and MP3 encoder padding breaks loop points and
   stem/mix sample alignment. Masters are `SaveAudioAdvanced` FLAC (or WAV).
3. **STRING outputs need `SaveText`** to exist in the output manifest.
4. **Standing rule:** the consumer is `POST /api/prompt` — static-validation-green is a hard
   requirement; editor-only validity does not count.

## Catalog deltas (13 `model_updates` — see research-raw.json for full notes)

| Model | Cloud axis | The wave-7 fact |
|---|---|---|
| ACE-Step 1.5 | yes (**measured**) | full node schema incl. authored bpm/keyscale/timesig; 48 kHz; ~8 cr/unit; deterministic |
| Stable Audio 3.0 | yes (**measured**) | lcm/8/cfg1 flat recipe; 44.1 kHz; grid-snap; no inpaint on cloud; Gemma-rider encoder on disk |
| Hybrid Demucs | yes (**measured**) | IS core `AudioSeparation`; 44.1 kHz out; the commercial-clean cloud stem path |
| Chatterbox | **yes — supersedes wave-6 "unknown"** | FL_* pack live; default-voice TTS cloud-OK; cloning local (no audio upload path) |
| Qwen3-TTS | yes (refresh) | FB_* class inventory; designed/preset voices cloud, clone-reference local |
| Kokoro-82M | local (**new fact**) | absent from allowlist 2026-08-19 |
| DiffRhythm 2 | local (re-confirmed) | absent 2026-08-19 |
| SCNet large/XL | local | not separately allowlisted; cloud stems = Demucs |
| Mel-Band RoFormer | partial | node exists, checkpoint license unverified → avoid for shipping |
| SA Open 1.0 / SA3 Small-SFX | yes(example) / unknown | superseded by SA3 Medium; small-sfx not surfaced on cloud |
| UVR5 | partial (refresh) | cloud prep = Demucs; zoo stays local |

Platform binds recorded as comfy-lane resources: **no AUDIO upload path** into cloud graphs
(all reference-audio work is local), **no audio-LoRA loader** on the allowlist (the ACE-Step
house-style OST LoRA trains *and* infers on the 5090; cloud is stock-model fan-out), plus the
billing/memoization/grid-snap measurements above.

## The two production workflows (archived, validated, run)

| Graph | Cloud record | Confirmation run | Archive |
|---|---|---|---|
| ACE-Step 1.5 XL instrumental → Demucs 4-stem → FLAC×5 + LUFS txt | `Motif builds v2` · `78a76ecd-7ae2-452a-afea-ad55a8d290f8` | `b81c6dbf…` 29.7 GPU-sec | [`workflows/audio/ace15-track-to-stems.json`](../../workflows/audio/ace15-track-to-stems.json) |
| SA3 Medium flat SFX → FLAC + LUFS txt | `Motif SFX batch v3` · `2c46c9ed-a0ac-43a7-a594-9616c384f4ca` | `7b966963…` 1.1 GPU-sec | [`workflows/audio/sa3-sfx-batch.json`](../../workflows/audio/sa3-sfx-batch.json) |

Archived JSONs passed a mechanical link↔node cross-reference (every link id present on both its
source node's outputs and destination node's inputs). Model manifests + trap ledger:
[`workflows/audio/README.md`](../../workflows/audio/README.md). The exact cloud model files
(HF `Comfy-Org/ace_step_1.5_ComfyUI_files` split_files) mirror bit-for-bit to the local 5090.

## Motif handoff — the locked generation layer (Advisor → Executor)

Roles from here: **this KB session line = Advisor; Grok Build = Executor.** The executor builds
Motif against these locked, receipt-backed decisions — anything below changes only with a new
measured receipt, not on impulse:

1. **Runtime standard 48 kHz**; resample 44.1 k inputs (stems, SFX) at ingest. Read actual
   durations from files (grid-snap). Normalize loudness at ingest from the manifest LUFS line.
2. **Music unit** = `ace15-track-to-stems.json`: authored **bpm + keyscale + timesignature at
   generation time** — cue families generated at a shared BPM/key are loop- and
   transition-compatible *by construction*; stems give vertical layering (drop drums for
   stealth); pinned seed makes every cue exactly regenerable. ~8 credits/unit.
3. **SFX unit** = `sa3-sfx-batch.json`: prompt + duration + seed are the only knobs; ~2.6
   credits/10 s. Loop seams via AudioConcat/Crop/fades or local tooling — there is no SA3
   inpaint on cloud.
4. **VO**: cloud = non-cloned batching only (FL_ChatterboxTTS default voice, Qwen3-TTS
   preset/designed voices). Consented-voice **cloning is local** (no audio upload path), as is
   Kokoro (consent-free presets) and the future ACE-Step **house-style OST LoRA** (no audio-LoRA
   loader on cloud; the cloud also cannot train). Partner API nodes are prototyping-only —
   shipped assets stay on open weights.
5. **Key detection does not exist on the allowlist** (tempo does) — key/chroma analysis, where
   needed beyond the authored keyscale, happens in Motif's ingest, not in the graph.
6. **Driving the graphs headlessly**: `POST /api/prompt` with the archived api-format wiring
   (or `run_saved_workflow` by `workflow_id`); per-job cost from the billing feed's
   `gpu_seconds`; outputs via `/api/view` / `get_output`. 3 concurrent jobs on Creator.

## Standards note

The two shipped workflow graphs perform **no irreversible operations** — every run only writes
new output files to cloud storage and spends metered credits (measured above); re-runs are
cache-priced. No compensators table required (nothing to undo); the andon lever in the pipeline
is the loader's hard-fail on unmatched `model_updates` slugs, added with this wave's tooling.
PIN_PER_STEP is satisfied by the archived graphs (exact class/values/model-files per node) +
cloud `workflow_id`s + job ids in the receipts.

## Re-ingest ordering (loader contract, new with this wave)

`model_updates` waves (6, 7) modify rows owned by earlier waves. Re-ingesting an older wave
**replaces its model rows and discards later waves' updates to them** — after re-ingesting wave
N, re-run every wave > N that carries `model_updates` (i.e. `load_db.py` waves 5 → 6 → 7 to
rebuild from scratch). The loader hard-fails (nothing committed) if an update slug matches no
row, which catches out-of-order ingestion immediately.

## Provenance

- Method: 5-round Comfy-Agent dialog (rounds 01–05 archived verbatim with replies and pull
  receipts in `dialogs/comfy-agent/`), advisor-side verification over the official API/MCP.
- Verification receipt for this wave: [verification.md](verification.md) — including the
  measured-vs-agent-reported split and the four cross-corrections.
- Supersession: wave-6's `chatterbox-tts: unknown` is superseded here (catalog changed between
  June and August — the reason the freshness rule exists).
