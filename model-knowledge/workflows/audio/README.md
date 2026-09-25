# workflows/audio/

Reusable audio graphs, harvested from the Comfy-Agent dialog (2026-08-18/19) and verified by
confirmation runs on Comfy Cloud. Provenance, run receipts, and LUFS values:
the private `dialogs/comfy-agent/` record (rounds 01–05). Both graphs are **headless-clean** (validate
green, no UI-only nodes, every runtime knob is a connectable primitive) and run unmodified on
Comfy Cloud or a local ComfyUI with the models below.

## ace15-track-to-stems.json

ACE-Step 1.5 XL instrumental track → core `AudioSeparation` (Demucs htdemucs) 4-stem split →
FLAC mix + 4 FLAC stems + integrated-LUFS text manifest. The Motif front-end: authored BPM /
key / time-signature at generation time, deterministic re-runs via one shared seed primitive.

- Cloud record: `Motif builds v2` (workflow_id `78a76ecd-7ae2-452a-afea-ad55a8d290f8`);
  confirmation run `b81c6dbf…` — 29.7 GPU-sec ≈ 7.9 credits; mix −12.32 LUFS.
- Exposed primitives: duration `PrimitiveFloat` (120 s), seed `PrimitiveInt` (0, fixed).
  Style tags / lyrics / bpm / keyscale / timesignature are widgets on
  `TextEncodeAceStepAudio1.5` (defaults: 72 bpm, E minor, 4/4, `[inst]`).
- Sampler: euler / simple / 50 steps / cfg 6 / `ModelSamplingAuraFlow` shift 3.
- ⚠ Output rates differ by design: mix decodes at **48 kHz**, Demucs stems at **44.1 kHz**
  (Demucs native). Motif ingest resamples to the 48 kHz runtime standard.
- Models (all in `Comfy-Org/ace_step_1.5_ComfyUI_files` on HF, `split_files/`):
  | File | Directory |
  |---|---|
  | `acestep_v1.5_xl_base_bf16.safetensors` | `models/diffusion_models/` |
  | `ace_1.5_vae.safetensors` | `models/vae/` |
  | `qwen_0.6b_ace15.safetensors` + `qwen_4b_ace15.safetensors` | `models/text_encoders/` |
- License: ACE-Step 1.5 MIT (code+weights, KB-verified); Demucs MIT — commercial-clean end to end.

## sa3-sfx-batch.json

Stable Audio 3.0 Medium text→SFX, flat headless graph (no template subgraph, no reprompter) →
FLAC one-shot + integrated-LUFS text manifest.

- Cloud record: `Motif SFX batch v3` (workflow_id `2c46c9ed-a0ac-43a7-a594-9616c384f4ca`);
  confirmation run `7b966963…` — 1.1 GPU-sec (partial cache); 3 s pin → 2.972 s @ −21.94 LUFS.
- Exposed primitives: prompt `PrimitiveStringMultiline` (bracketed placeholder), duration
  `PrimitiveFloat` (10 s default — one float drives BOTH `EmptyLatentAudio.seconds` and
  `ConditioningStableAudio.seconds_total`), seed on the KSampler.
- Sampler: **lcm / simple / 8 steps / cfg 1** — SA3 Medium's distilled fast path (~1 GPU-sec/s
  of audio). Output **44.1 kHz**; duration snaps to the latent grid (3.0 s ask → 131,072
  samples = 2.972 s exactly 2^17).
- Models: `stable_audio_3_medium.safetensors` (`models/checkpoints/`),
  `t5gemma_b_b_ul2.safetensors` (`models/text_encoders/`; CLIPLoader type `stable_audio`).
- License: Stability AI Community License (< $1M revenue free-commercial; tracked upgrade
  trigger) **plus a Gemma-ToU rider on the T5Gemma text encoder** — KB-verified, see the
  audio catalog entry.

## API-format companions (`*.api.json`) — the REST payloads

The `.json` graphs above are **editor/save format** (`nodes` + `links`) — loadable in ComfyUI,
runnable on cloud via MCP `run_saved_workflow({ workflow_id })`, but **rejected by REST
`POST /api/prompt`**, which takes API-format only (node-id keys → `{class_type, inputs}`).
The `*.api.json` companions are the REST payloads for the same graphs, derived from the cloud
records on 2026-08-19 and shape/reference-validated. Provenance note: derived via the MCP's
graph→api conversion of records `78a76ecd…` / `2c46c9ed…`; generation is deterministic on
pinned seeds, so the cheap correctness check for any consumer is one submission compared
against the confirmation-run receipts (a cache-priced re-run if byte-identical). Wire runtime
knobs through the primitive nodes (`PrimitiveFloat` duration, `PrimitiveInt` seed, the prompt
primitives) — same ids as the tables above.

**First-use verified 2026-08-19:** both payloads submitted as-is/with primitive overrides and
**byte-reproduced their confirmation runs** at memoize pricing (ACE 3.47 gpu-sec ≈ 0.92 cr,
SA3 0.81 ≈ 0.21). Full receipt, including the run1/run3 fixture-provenance correction:
the private `2026-08-19-api-first-use-receipt.md`.

## Trap ledger (why these are shaped this way)

- `SaveAudioMP3` is deprecated in core, and MP3 padding breaks loop points / stem alignment —
  always `SaveAudioAdvanced` + FLAC (or WAV) for masters.
- UI-only nodes (`PrimitiveNode` "Song Duration", template `CustomCombo`) validate in the
  editor but never reach `/api/prompt` — headless graphs use `PrimitiveFloat`/`PrimitiveInt`.
- `AudioLoudnessMeter.loudness_info` is a STRING; it reaches the output manifest only through
  `SaveText` (format: `Integrated Loudness: -12.32 LUFS`).
- Cloud output filenames are content-addresses but **not sha256 of the served bytes** — same
  filename proves same object, but only a local hash of downloaded bytes is a byte receipt.
- A memoized whole-graph replay still bills ~3.5 gpu-sec (ACE) / ~0.8 (SA3) of load/verify
  overhead — cache-priced ≠ free.
- **`keyscale` is a 34-value COMBO** (17 enharmonic roots × major/minor) — modes
  (phrygian/dorian/"chromatic") are `value_not_in_list` rejections at job pickup; modal color
  belongs in the style tags. `timesignature` is COMBO `["2","3","4","6"]` (never "4/4").
  The MCP submit pre-flight does NOT enforce COMBO membership; the server does. Rejected jobs
  bill zero.
- **Editor-valid ≠ API-valid:** a tab can report `valid:true` while `/api/prompt` rejects it —
  COMBO values are TYPE-strict at the API (`timesignature: 4` INT fails; `"4"` string passes).
  Fix saved records via `run_saved_workflow` + `input_overrides` (post-conversion). Failed
  validation bills zero.
- **Node-level caching spans jobs:** byte-identical subgraph nodes (loaders, encodes) serve
  from cache across concurrent/sequential jobs — per-job gpu_seconds drop accordingly.
- **Byte-identity of pinned-seed re-runs is cache-only.** A fresh re-execution of the identical
  graph reproduces loudness/music but NOT bytes (GPU-kernel drift; measured 2026-08-19,
  grounded-wave receipt). Treat downloaded masters as canonical-by-hash; regeneration yields an
  equivalent new artifact unless the cache serves it.
- **`submit_batch` item labels truncate at 40 chars — never map outputs by label.** Measured
  2026-08-21 (Tier-1 wave): `tier1 dark-dungeon: abomination-boss-s3551` and its `-s3552`
  sibling both arrived as the same 40-char string, as did `mythic-aegean: monster-battle-s655`.
  The job UUIDs stay distinct, so nothing is lost — but a collector that parses labels silently
  collides two takes into one folder. **Map `job_id` → cue from the authoring spec** (catalog
  order: seedA then seedB per cue) and treat any label check as loose, tolerating truncation.
- **Batch tokens are client-side base64 of the item list** — `batch_id` = `batch_` +
  base64url(`{"v":1,"items":[{id,label},…]}`). They are therefore re-derivable, but also
  hand-corruptible: a token retyped by hand can differ cosmetically in a label and still decode
  to the correct job-ID set. Collectors must key strictly on `job_id`; the token is a transport
  container, never the source of truth for what a job is.
- **The workspace queue caps at 100 jobs, ACCOUNT-WIDE — serialize batch submission, never
  fan it out.** Measured 2026-08-21 (Tier-2 wave): four submission agents dispatched in
  parallel filled all 100 slots, and every subsequent item came back
  `POST /api/prompt failed: Maximum queued jobs limit reached (100 jobs in this workspace)`.
  60 of 204 jobs were rejected. The Tier-1 wave (210 jobs) never hit this only because its
  batches went out sequentially and the queue drained as it filled — that was luck, not
  design. **Submit one batch at a time and check `get_queue` for `pending + 20 <= 100`
  headroom before the next.** The cap is shared with every other session and agent on the
  account, so a nonzero count is never attributable to your own wave.
- **A rejected batch item is not positionally aligned to your catalog order.** When
  `submit_batch` partially fails, the returned `job_ids` array is *compacted* — only the
  accepted items. Zipping it against catalog order silently mislabels every take after the
  first failure. Record an explicit `{catalog_index: job_id}` map at submission time.
  (Comfy's per-item error also warns the item "may already have been queued and charged";
  in the measured case `get_queue` showed the slots were full and the items were rejected
  outright, consistent with the standing "rejected jobs bill zero" rule — but verify against
  billing before re-submitting rather than assuming.)
- **Queue warm-up costs ~6% on batch waves.** The first item of each batch runs 16–25 gpu-sec
  against a ~12.8 gpu-sec steady state (measured across 10 Tier-1 batches: 715 cr estimated,
  758.6 cr actual). Budget batch waves at steady-state × 1.06, not steady-state flat.
- **TEMPO predicts loudness collapse; prose wording does not.** Measured across 410 takes
  (Tier 1 + Tier 2, 2026-08-21). Takes at **bpm ≤ 70 hit the +6 dB boost cap 21.2% of the time
  (28/132); above 70 bpm, 1.4% (4/278)** — z = +7.0, roughly a 15× difference, and above
  85 bpm collapse is essentially absent (1/94). **Plan for it: a slow cue loses about one take
  in five no matter how it is written, so slow cues need MORE TAKES (C/D as standard, not as
  an exception) — not better adjectives.**
- **⚠ The "quiet-cue prose rule" was FALSIFIED — do not re-derive it.** The plausible theory
  was that quiet cues collapse because their prose uses absence language ("faint", "distant",
  "empty") instead of naming a continuously-sounding anchor. Tier 2 was authored under that
  rule with a validator enforcing it. Result in the targeted population (bpm ≤ 70):
  Tier 1 (no rule) 9/48 = 18.8%, Tier 2 (rule enforced) 19/84 = 22.6% — difference +3.9pp
  against a pooled SE of 7.4pp, **z = +0.52, no detectable effect.** The headline rates
  (5.7% → 10.0%) differ only because Tier 2 deliberately holds far more slow cues; that is
  composition, not regression. Four Tier-2 cues still lost BOTH takes
  (`hidden-tomb`, `withered-grove`, `glass-plain`, `fireflies`) — every one bpm ≤ 70 and every
  one fully rule-compliant. An earlier n=4 controlled re-roll appeared to show +8.97 dB; with
  hindsight that was regression to the mean, since all four v1 takes were extreme outliers
  (−21 to −34 LUFS). **Lesson beyond audio: a 4-sample controlled test on outlier-selected
  cases is not evidence — it is exactly the setup that manufactures a false positive.**
- **A cloud FLAC can declare more samples than it contains — and the collection manifest will
  not catch it.** Measured 2026-08-21 (library close): `ambient-drones/snow-bed-s13554`'s
  vocals stem has STREAMINFO `totalSamples = 2 646 000` but decodes to 2 644 992 — short by
  1008 samples (0.023 s). Its bytes match `sha256-manifest.json` exactly, so the download was
  complete and the served artifact itself is malformed; a fresh decoder per file reproduces it,
  so it is not a decoder-reuse artifact. **A sha256 manifest proves you received what the
  server sent, never that what the server sent is well-formed.** Rate: 1 stem in 2 420 across
  the 484-take library. The ingest's `RESAMPLE_COUNT` andon is what caught it — keep that check.
- **Scope an andon to the item, not the run, when the defect is in an immutable upstream
  artifact.** One malformed stem halted a 62-take ingest at take ~30 and discarded every
  take after it. Halting the line is right when the defect is fixable in place; here the other
  483 takes were independent and unaffected. `run-ingest-library.js --skip-defective` narrows
  it: the bad take is still refused and never folded, the rest finish, every failure is listed,
  and the process exits non-zero so a run that dropped something cannot read as clean. Default
  stays strict.
- **⚠ "Per-file WASM decoder instantiation is the ingest bottleneck" was FALSIFIED.** The
  plausible theory: `decodeFlacPcm` built a new `FLACDecoder` (compile + start a WASM module)
  for all five files of every take, ~2 420 instantiations across the library. Holding one
  decoder for the process and `reset()`-ing between files measured **417.4 s forced vs 414.0 s
  baseline for ten takes — no effect.** The ~41 s/take fresh cost is decode/resample/encode/
  write, not setup. The reuse was kept (it is strictly less work) but it is **not** a
  throughput fix, and the real fresh-ingest cost is still unprofiled. Lesson: profile before
  optimizing even when the wasteful thing is real and obvious — "obviously wasteful" and
  "actually costly" are different claims.
- **Content-address what you already hash.** Ingest computed a sha256 of every input FLAC,
  wrote it into the persisted record, and then threw it away and re-did ~86 MB of decode and
  writes on the next run. Reusing a prior ingest when the input hashes, loudness target and
  generation identity all match takes a finished pack from ~14 minutes to **1.0 s**, and lets
  an interrupted run resume instead of restarting — 13 already-finished takes survived the run
  that was stopped mid-pack. The safety rule that makes it sound: derive the assets/stems/
  scene/cue in ONE function both the fresh and cached paths call, so the cache cannot drift
  into a lookalike. Proven by re-running a pack ingested by the older code and getting its
  manifest entries back byte-for-byte.
