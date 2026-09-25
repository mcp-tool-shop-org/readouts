# vocology-knowledge

**Status:** Waves through 13 (register classification measured, 2026-09-14). Catalog **317 · 214/317 · 13 waves**. Flips beyond ACCEPT: 0. Nodes invented: 0.

- **Wave 13 (register classification measured)** — [dispatch](waves/wave-13-register-classification-measured/dispatch.md) · [research-raw](waves/wave-13-register-classification-measured/research-raw.json) · [verification](waves/wave-13-register-classification-measured/verification.md) — 2 findings, both confirmed on full text; retrieval-oracle only, no second model family; corrects the claim that audio-only register classification is unreliable.

- **Wave 12 (expansion: conversion, expression, articulation, datasets, assessment)** — [research-raw](waves/wave-12-expansion/research-raw.json) — 70 findings, 68 verified; 5 new domains. Renumbered from 8 on the 2026-09-14 merge; main already held a different study at that ordinal.

- **Wave 11 (the spectrogram surface)** — [dispatch](waves/wave-11-spectrogram-surface/dispatch.md) · [research-raw](waves/wave-11-spectrogram-surface/research-raw.json) · [verification](waves/wave-11-spectrogram-surface/verification.md) — 48 findings, all verified; prism-verified, 26/26 exist, 0 fabricated. Renumbered from 7 on the 2026-09-14 merge.

- **Wave 10 (STUDY-064 catalog vs README)** — [dispatch](waves/wave-10-study-064-catalog-readme/dispatch.md) · [research-raw](waves/wave-10-study-064-catalog-readme/research-raw.json) — 22 findings verified=0; Analogist #7–#8 pack-only; Flips beyond ACCEPT: 0; Nodes invented: 0.

- **Wave 9 (STUDY-043 Comfy a2a deepen)** — [dispatch](waves/wave-09-study-043-comfy-a2a/dispatch.md) · [research-raw](waves/wave-09-study-043-comfy-a2a/research-raw.json) — 22 findings verified=0; nodes invented: 0; Cover/Repaint not live Comfy nodes.

- **Wave 8 (STUDY-042 eval deepen)** — [dispatch](waves/wave-08-study-042-eval-deepen/dispatch.md) · [research-raw](waves/wave-08-study-042-eval-deepen/research-raw.json) — 21 findings verified=0; VocalRender invert + Green not verified this land; knobs invented: 0.

- **Wave 7 (STUDY-041 score-lock deepen)** — [dispatch](waves/wave-07-study-041-score-lock-deepen/dispatch.md) · [research-raw](waves/wave-07-study-041-score-lock-deepen/research-raw.json) — 21 findings verified=0; flips beyond ACCEPT: 0; knobs invented: 0.

A knowledge base of **sung-voice craft**: vocology (source–filter, registers, singer's formant), musical vs speech prosody, lyric-to-note alignment, score-controllable singing-voice synthesis vs lyrics-to-song generators, and admission/teaching evaluation.

This is **not** a models table. ACE-Step / DiffRhythm / Kokoro already live in [`model-knowledge/catalog/audio.md`](../model-knowledge/catalog/audio.md). This KB answers: *how does a singing engine have to behave to be a voice, and which local routes can honor an existing MIDI line?*

**Consumer:** `E:\AI\ai-jam-sessions` (MIDI practice companion). Adjacent engine: `E:\AI\vocal-synth-engine` (deterministic additive + G2P + `VocalScore`).

## Verification sweep (2026-09-09)

Six parallel adversarial retrieval lanes over the **147 findings no verifier had ever
reached**. `verified` previously came from nine citation IDs hardcoded in `load_db.py`,
so the KB read 12/159 — an absence of checking, not a quality signal.

**106 confirmed · 38 corrected · 1 refuted · 2 unfindable · 0 fabrications.** Every
citation resolved to a real artifact, including every forward-dated identifier. The
corrections were overwhelmingly *scope-stripping* (a real number quoted without the
dataset or config that gives it meaning) and *compound claims* where a verified half
carried an unchecked half across an "and" — not invention.

Verdicts are a durable ledger at [`verification/verdicts.json`](verification/verdicts.json),
read by `load_db.py`, so a rebuild reproduces the verified state. Full receipt and the
per-lane evidence: [`verification/sweep-2026-09-09/`](verification/sweep-2026-09-09/).

## Wave 11 (2026-09-07) — the spectrogram surface

Five parallel research lanes on how a spectrogram of rendered audio can let the model *see what it hears*. Two surfaces, not one: a constant-Q picture (60 bins/octave) for orientation and localisation, DSP numbers (SuperFlux onsets, SwiftF0/pYIN cents) for the gates. Mel is the secondary "what the model hears" panel — it is what audio models are trained on, but a Slaney mel step is 66.7 Hz below 1 kHz, so it cannot show a 50-cent error at C4. Vision models read spectrograms only coarsely (59% on 10-class sound ID, chance on fine speech content); no gate ever routes through the image. essentia.js is AGPL → own DSP on `fft.js`.

Consumer: ai-jam-sessions `view_spectrogram` + `compare_audio` (proposed lock, Director-gated, with a P0 in-repo render A/B before the default is frozen). Provenance: [`waves/wave-11-spectrogram-surface/dispatch.md`](waves/wave-11-spectrogram-surface/dispatch.md) · [`research-raw.json`](waves/wave-11-spectrogram-surface/research-raw.json) · [`verification.md`](waves/wave-11-spectrogram-surface/verification.md)

## Wave 2 (2026-09-04)

Music as Python seconds + Comfy Cloud timbre. Local per-note TTS/WSOLA is identity death. Clock = jam-sessions `startSec` → Seed Audio `[start:end]`. Transform the one Kokoro lock with ElevenLabs STS (`LoadAudio`), not ACE-Step.

Provenance: [`waves/wave-02-music-language/dispatch.md`](waves/wave-02-music-language/dispatch.md)

### Wave 3 — STUDY-001 reopen
Provenance: [`waves/wave-03-score-lock-registers-alignment/research-raw.json`](waves/wave-03-score-lock-registers-alignment/research-raw.json) · study packs under `/workspace/studio/research/STUDY-011/`

## Wave 1

| | |
|---|---|
| Trigger | Director: add vocals to ai-jam-sessions; start with study-swarm into prosody, vocology; inform readouts; then decide the route |
| Protocol | `research-grounded-advisor-protocol` (study-swarm) |
| Lanes | 5 parallel web-grounded agents |
| Provenance | [`waves/wave-01-foundation/dispatch.md`](waves/wave-01-foundation/dispatch.md) · [`research-raw.json`](waves/wave-01-foundation/research-raw.json) · [`verification.md`](waves/wave-01-foundation/verification.md) |

Decisive axis (when the DB is wired): **score-lock** — can this method honor MIDI notes + lyrics as a hard constraint (singing *instrument*) vs generate a mixed song (generator). Secondary axis: commercial-safe weights for a public npm tool.

Do not hand-edit a future `catalog/`. Waves append.
