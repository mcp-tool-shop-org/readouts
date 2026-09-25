# Wave 7 — verification receipt

Wave 7 is the KB's first **empirical wave**, so its verification model differs from the
reasoning-stripped WebFetch oracle of waves 1–6: the decorrelating element here is not a live
web page but **artifacts on disk and API responses from this account** — things neither the
Comfy Agent nor this advisor could have hallucinated into existence. Every claim in the wave
carries one of two provenance labels, written into its `cloud_note`/extra text:

## Class A — MEASURED (artifact-backed; treat as verified)

| Fact | Artifact / receipt |
|---|---|
| Per-job billing: 31.9 / 29.7 GPU-sec (music), 9.8–10.0 (SFX uncached), 1.1–1.2 (cache hit); active-GPU-sec billing | billing activity feed rows with job ids `6c99f797…`, `b81c6dbf…`, `495b2f2c…`, `7b966963…` (03-run-receipts.md, 04-run-receipts.md) |
| Mix decode 48 kHz / 16-bit / 5,760,000 samples = 120.000 s | FLAC STREAMINFO hexdump `0B B8 02 F0 00 57 E4 00` (03-run-receipts.md); file sha256 `FB655B1E…` |
| All 4 stems 44.1 kHz / 5,292,000 samples = 120.000 s (Demucs resamples) | header decodes of the downloaded stems (03-run-receipts.md) |
| SA3 grid-snap: 3.0 s → 131,072 samples (2^17) = 2.972 s; 10 s → 10.031 s | header decodes (03/04-run-receipts.md) |
| Whole-graph memoization / bit-determinism | cache-hit runs billed 1.16/1.14 GPU-sec vs ~9.8 uncached |
| LUFS-to-file works headlessly; integrated LUFS; parseable one-liner | downloaded manifests: `Integrated Loudness: -12.32 LUFS` / `-21.94 LUFS` |
| Both graphs' full wiring (nodes, values, model files, seed fan-out) | graphs pulled by `workflow_id` (`78a76ecd…`, `2c46c9ed…`) and archived after link↔node cross-reference validation |
| Duration-input regression in SFX v2, fixed in v3 | pulled v2 record showed empty `primitive_settings`; v3 record shows `PrimitiveFloat` → both seconds fields; 3 s pin decoded 2.972 s |
| SaveAudioMP3 deprecated; SaveAudioAdvanced/FLAC in final graphs | `_meta` titles in pulled graphs; output manifests' `class_type` |
| T5Gemma encoder in the SA3 stack (Gemma-ToU rider is concrete) | `t5gemma_b_b_ul2.safetensors` in the pulled graph's loader |

## Class B — AGENT-REPORTED (single-source: the in-app agent's live-catalog browsing; advisory until re-measured)

| Claim | Why it stays Class B |
|---|---|
| FL_Chatterbox* pack present on cloud (5 classes); FB_Qwen3TTS* class inventory | catalog listing seen only by the agent; not independently fetched from this rig |
| `audio_prompt` optional / `target_voice` required; **no AUDIO upload path** into graphs | schema inspection by the agent; consistent with our failed expectations but not exercised end-to-end |
| DiffRhythm 2 + Kokoro absent; partner/audio/* = Sonilo ×2, ByteDance, ElevenLabs, HeyGen | absence claims from the agent's node search — absence is inherently weaker than presence |
| No audio-LoRA loader on the allowlist (lora category image/video only) | agent's category browse |
| MelBandRoFormer node present (checkpoint unidentified); SCNet absent | agent's catalog browse |
| No SA3 inpaint/continuation node on cloud | agent searched, did not find — absence claim |

Class B claims are dated **2026-08-19** in their notes and are subject to the constitution's
freshness rule: >30 days = advisory until re-measured. The Chatterbox case is the proof this
matters — wave 6 (June) correctly recorded it absent; by August the catalog had changed.

## Cross-corrections performed during the dialog (both directions)

| # | Correction | Direction | Receipt |
|---|---|---|---|
| 1 | ACE-Step license: agent's "Apache-2.0" vs KB's verified **MIT** (Comfy's own blog verbatim + HF tag) | KB → agent | wave-6 verification + round-1 reply |
| 2 | "MelBandRoFormer is Apache-family" → per-checkpoint; top vocal checkpoint has **no license file** (all-rights-reserved) | KB → agent | wave-4 verify note; round-1 reply |
| 3 | "ACE-Step decode → 48 kHz" true for the mix only — **stems decode 44.1 kHz** | measurement → agent | stem header decodes |
| 4 | SFX v2 silently lost its duration input (30 s → 10 s default) | measurement → agent | pulled v2 record; fixed + proven in v3 |
| — | plus: round-4 lineage id mix-up corrected on intake; wave-6 `chatterbox: unknown` superseded by the August catalog | bookkeeping | 04-brief intake note; this wave |

## What was NOT verified (honest gaps)

- The FL_Chatterbox and FB_Qwen3TTS nodes were **not run** — presence and schema are Class B;
  a future VO thread should run one default-voice line end-to-end before Motif's VO lane relies
  on it.
- `estimate_credits` (pre-run quoting) was never exercised — costs above are post-hoc measured.
- The MelBandRoFormer cloud node's checkpoint identity remains unknown — deliberately routed
  around rather than resolved.
- Audio outputs were verified structurally (rates, durations, stem separation audible on the
  drums stem) but no quality bar was asserted — prompt quality is Motif-production's problem,
  not this wave's.

## Verifier-maturity note

Per CONVENTIONS.md the planned upgrade path is family-different verification. This wave's Class
A facts already exceed that bar (ground truth = the platform's own billing/storage/API, no LLM
in the loop); Class B remains single-model-family (the in-app agent) and is labeled accordingly
in every note it touches.
