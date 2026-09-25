# workflows/caption/

Reusable captioning graphs, harvested from the Comfy-Agent captioner dialog (2026-08-19) and
verified by a confirmation run on Comfy Cloud. Provenance and run receipts:
`../../dialogs/comfy-agent/` (captioner rounds 01–03); wave receipt:
`../../waves/wave-08-cloud-caption-measured/`. The graph is **headless-clean** (validates
green, no UI-only nodes) and runs unmodified on Comfy Cloud or a local ComfyUI with the kijai
Florence-2 pack.

## caption-florence2-v1.json (+ .api.json)

One image in → `more_detailed_caption` → templated `.txt` sidecar out, with **in-graph filename
pairing** (`beach.jpg → beach_00001.txt`). The born-in-cloud metadata rider: caption outputs
where they're born; bulk dataset captioning stays local (cloud is one-image-per-job headless).

- Cloud record: workflow_id `b26cb8b5-0153-4279-9c3a-593857fbff6b`; confirmation run
  `26a78ccd-06c3-4618-8822-08a547c7e8e9` — **6.73 GPU-sec** on rtx_pro_6000 ≈ ~1.8 credits
  derived (billing feed; gpu_seconds is authoritative). Confirmation artifact:
  [`beach_00001.txt`](beach_00001.txt) (454 B, five sentences).
- Graph (7 nodes): `LoadImageWithFilename_EditUtils` → `DownloadAndLoadFlorence2Model`
  (`microsoft/Florence-2-large`, fp16, sdpa) → `Florence2Run` (`more_detailed_caption`,
  `max_new_tokens=1024`, `num_beams=3`, **`do_sample=false`, `seed=1`**) → 2×`PrimitiveString`
  (prefix/suffix, empty; prefix reserved for a trigger token) → WAS `Text Concatenate`
  (`delimiter=""`, `clean_whitespace="true"`) → `SaveText` (`format=txt`, `filename_prefix`
  **linked** to the loader's filename STRING).
- Knobs: task tier, `max_new_tokens` (ceiling 4096), prefix, suffix, `filename_prefix`.
- Both forms archived server-emitted (editor `.json` loads in the canvas /
  `run_saved_workflow`; `.api.json` is the `POST /api/prompt` form). Editor form passed the
  mechanical link↔node cross-reference at ingest.
- License: `microsoft/Florence-2-large` MIT (KB-verified). **`prompt_gen_*` tasks are OFF the
  menu** — they belong to MiaoshouAI PromptGen fine-tunes (license unverified our side).

### Trap ledger (earned in this build)

1. **`Florence2Run.do_sample` defaults to `true`** — cloud captions are stochastic out of the
   box. Production graphs pin `do_sample=false` + a fixed `seed`.
2. **WAS `Text Concatenate` `text_a–d` are link-only STRING inputs** — feed with
   `PrimitiveString` nodes, never widget values (first delivery batch rejected clean on this).
3. **`delimiter` defaults to `", "`** — explicitly zero it for bare prefix+caption+suffix.
4. **Content-addressed storage:** an `/api/view` hash filename is NOT a pairing failure — the
   logical name rides the download's `content-disposition`. `SaveText` appends its `_00001`
   counter; strict training sidecars (`img_0042.txt` exact) take a counter-strip rename at
   download.
5. **`LoadImageWithFilename_EditUtils.image` is a COMBO of server-side files** (not free-text)
   — fine for API-driven jobs where the key is set by JSON.

### Local runtime note

For **local** native-transformers runs (transformers ≥4.51), `microsoft/Florence-2-*` no longer
loads without `trust_remote_code` — pin **`florence-community/Florence-2-large`** (same
weights, MIT). Measured on the 5090 (plain-sight v0.1.0): fp16 ≈1.5 GB VRAM, ≈1.0 s per
`more_detailed_caption`, deterministic. The cloud kijai loader is unaffected.
