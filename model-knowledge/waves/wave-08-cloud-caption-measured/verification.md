# Wave 8 — verification receipt

Second empirical wave; same verification model as wave 7: the decorrelating element is not a
live web page but **artifacts on disk and API responses from this account/rig** — with one
upgrade: the load-bearing measurements were **re-pulled live at ingest time** (2026-08-19
local / 2026-08-20 UTC) by the ingesting session, not just carried forward from the dialog
archive. Everything in `dialogs/` was treated as unverified intake per CONVENTIONS.md; the
checks below are what promoted each claim.

## Class A — MEASURED (artifact-backed or re-pulled live at ingest; treat as verified)

| Fact | Receipt / re-check performed at ingest |
|---|---|
| Caption job billed **6.732932 gpu_seconds** on rtx_pro_6000 | billing activity feed **re-pulled live via MCP at ingest**: event `cloud_workflow_26a78ccd-06c3-4618-8822-08a547c7e8e9`, created 2026-08-20T02:00:33Z — matches the closeout's 6.73 exactly |
| Graph wiring matches the ordered spec (pin, fp16/sdpa, `more_detailed_caption`, `max_new_tokens=1024`, `num_beams=3`, `do_sample=false`, `seed=1`, PrimitiveString feeders, `delimiter=""`, `clean_whitespace="true"` exact enum string, SaveText `format=txt`, `filename_prefix` LINKED to loader output 2) | archived `caption-florence2-v1.api.json` read field-by-field at ingest — all values confirmed; server-emitted, not client-converted |
| Editor-form graph is structurally sound | mechanical link↔node cross-reference run at ingest: 7 nodes / 7 links, every link id present on both its source node's outputs and destination node's inputs — PASS |
| In-graph filename pairing works end-to-end (`beach.jpg → beach_00001.txt`) | confirmation artifact on disk: `workflows/caption/beach_00001.txt` — **454 bytes** (byte-counted at ingest), five sentences, `more_detailed_caption` tier as advertised; logical name carried by the download's `content-disposition` per the closeout pull receipt |
| `florence-community/Florence-2-large` is MIT | HF model API **re-pulled live at ingest**: `license:mit` tag, 441,456 downloads/mo, lastModified 2025-09-11 |
| microsoft/* fails native loading; community pin is the fix; 5090 numbers (fp16 ≈1.5 GB VRAM, ≈1.0 s/caption, deterministic) | `E:/AI/plain-sight` at commit `fdd49b3` ("feat: plain-sight v0.1.0 — Florence-2 image describer"): `engine.py` greps confirm `DEFAULT_MODEL_ID = "florence-community/Florence-2-large"` and the deterministic `do_sample=False` + `num_beams=3` defaults; perf numbers are the build session's measurements recorded in [[florence2-native-needs-community-checkpoints]] (studio-measured 2026-08-19) |
| `Florence2Run` schema: 3-tier task ladder, `max_new_tokens` 1024/4096, `prompt_gen_*` present, `seed` + `do_sample` default **true** | pulled live via `get_node` during round 1 (recorded in `-01-reply.md`) — our-side API pull, not agent relay |
| WAS Text Concatenate traps (link-only `text_a–d`; delimiter default `", "`) | manifested in the delivered graph itself (PrimitiveString feeders present, delimiter zeroed) + the agent's self-reported rejected first batch, corroborated by the billing feed showing no landed job for it |

## Class B — AGENT-REPORTED (single-source: the in-app agent's live-catalog browsing; advisory until re-measured)

| Claim | Why it stays Class B |
|---|---|
| One image per job headless — no API-valid directory/folder iterator (batch nodes are in-memory IMAGE only) | absence claim from the agent's node browse; not independently exercised |
| No JoyCaption / InternVL / MiniCPM-V / Qwen-VL packs on the cloud shelf → Florence-2 family is the OSS in-cloud ceiling | absence claim from the agent's node search + STRING×IMAGE producer browse |
| `LoadImageWithFilename_EditUtils` image input is a COMBO of server-side files (not free-text) | editor-widget observation by the agent; the node's *behavior* (IMAGE/MASK/STRING outputs, pairing) is Class A via the measured run |

Class B claims are dated **2026-08-19** in their notes; constitution freshness rule applies
(>30 days = advisory until re-measured).

## Corrections landed by this wave (both directions)

| # | Correction | Direction | Receipt |
|---|---|---|---|
| 1 | Waves 1/3 cloud notes claimed Florence-2 "runs credit-FREE on the cloud GPU" — **FALSE**: bills active GPU-sec like any OSS job | measurement → **our KB** | job `26a78ccd…` 6.73 gpu-sec, re-pulled live at ingest; `model_updates` supersede both rows |
| 2 | Intake's derived "**~1.3 credits/caption**" does not reproduce: 6.73 × ~0.266 (wave-6 verified Creator rate) ≈ **1.8** | ingest verifier → intake (closeout + round-3 ack carried the slip) | arithmetic against wave-6's rate receipt; the wave records ~1.8 derived, `gpu_seconds` authoritative |
| 3 | "Florence-2 is MIT" (agent, round 1) narrowed: MIT covers `microsoft/*` originals only — `prompt_gen_*` requires MiaoshouAI PromptGen fine-tunes, license unverified → off the commercial menu | KB → agent | round-1 reply; agent complied (pinned microsoft, left `prompt_gen_*` off the menu) |
| 4 | Agent's round-2 caveat that the `/api/view` hash filename might be a pairing problem — resolved: content-addressing, logical name rides `content-disposition` | measurement → agent | closeout pull receipt; agent owned it in the round-3 ack |
| 5 | Ingest audit swept the DB for the same falsehood class: `qwen3-vl` (wave 1) also claimed "runs credit-free on the cloud GPU" — superseded by the measured billing model (pack presence itself stays advisory/unexercised) | ingest verifier → **our KB** | DB grep at ingest; third `model_updates` entry |
| — | Bookkeeping: "credit-free" was never the agent's claim — it was our KB's (waves 1/3); the agent correctly noted this in its terminal ack | — | `-03-closeout.md` |

## What was NOT verified (honest gaps)

- The **~1.8 credits/caption is derived**, not billed — Comfy Cloud exposes no per-job credit or
  dollar figure; the conversion uses wave-6's ~0.266 cr/GPU-sec Creator rate. `gpu_seconds` is
  the only per-job ground truth.
- The local 5090 perf numbers (≈1.5 GB VRAM, ≈1.0 s/caption) are the plain-sight build session's
  measurements, recorded same-day in memory — accepted as studio-measured, not re-run at ingest.
- `LoadImageWithFilename_EditUtils` was exercised with **one** image; multi-extension and
  unicode-filename behavior untested.
- The one-image-per-job and no-8B-VLM-pack absence claims were not independently swept from this
  rig (`search_nodes` recon happened only for the MIDI thread, not this one) — hence Class B.
- MiaoshouAI PromptGen license terms remain **unread** — deliberately routed around (off the
  commercial menu) rather than resolved; a future thread may clear it.

## Verifier-maturity note

Per CONVENTIONS.md the planned upgrade is family-different verification. Class A here already
exceeds that bar: ground truth = the platform's billing/storage API, the HF API, local git +
source greps, and a mechanical (non-LLM) graph validator — no LLM in the loop. Class B remains
single-model-family (the in-app agent) and is labeled in every note it touches. Correction #2
is the pattern working as designed: a derived number in our own intake failed re-derivation at
ingest and was fixed before it entered the DB.
