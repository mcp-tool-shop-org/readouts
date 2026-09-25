# Wave 4 — si-jam-sessions: Rust for a deterministic music law (P1)

**Date:** 2026-09-25 · **KB:** `rust-knowledge` · **Tier:** si-jam-sessions · **Lanes:** 4 (the P1 set) · **Seats:** generators outside the Claude family, a Claude Sonnet verifier, and the compiler

## Why this wave exists

A second Claude session is designing **si-jam-sessions**: a deterministic music "law" in Rust, built the way si-rpg-engine was. Its design lock is not signed yet. Its provisional shape:

- a Rust edition-2024 `wasm32-unknown-unknown` cdylib with a raw C ABI, and no files, clocks or threads;
- integer ticks at one fixed PPQ, with pitch, onset, duration, velocity and voice all integers;
- replay as seed plus the admitted-action log, with audio outside the hash;
- a native host that plays committed events through an oscillator.

That session asked for a KB wave in three priority tiers. The operator approved **P1** (four lanes) now, and the rest after the lock signs. The approved seat roster is models outside the Claude family as generators, and Claude as checker. Each lane states the lock item it assumes, and every finding went to the designing session as it landed, with a pin-check line against the lock.

## Seats, and how a non-tool-using generator was admitted

- **Generators.** `midi-notation-ingest` was written by Gemini 3.1 Pro (`google/gemini-3.1-pro-preview-20260219`, through OpenRouter). The other three lanes were written by Kimi k2.6 (`kimi-k2.6:cloud`, through the local Ollama daemon, digest `a90cd0d1…`). Both ran at temperature 0 with JSON mode.
- **Harness.** A generator cannot browse or run code, so `scripts/openrouter_lane.py` does both for it:
  - it grounds the model in source excerpts from the local cargo registry at the pinned versions;
  - on Ollama it adds reference pages that the harness fetches and hashes (Rust std and reference docs, Microsoft Learn, the cargo-deny docs, SPDX, the MPL FAQ);
  - it admits a source as a warrant only if the conversation shows it was opened;
  - it runs every check through the compiler, returns failures for bounded revision rounds, and removes what never passes.
- **Receipts.** `waves/wave-04-si-jam-sessions/receipts/` holds, per lane: every call's model, tokens and cost, the prompt hashes, the pack manifest with a SHA-256 per excerpt, and the harness's own hash.
- **Compiler.** The oracle gained a second dependency set, `oracle-jam/`, built for the host and for wasm32:
  - on both: `midly` 0.5.3 (alloc only), `quick-xml` 0.42.0, `roxmltree` 0.21.1, `musicxml` 1.1.2, `abc-parser` 0.4.0;
  - host only: `cpal` 0.18.2, `midir` 0.11.0, `rtrb` 0.4.0, `ringbuf` 0.5.2, `assert_no_alloc` 1.1.2.

  A check selects the set with `"oracle_set": "jam"`. The engine's set is untouched, and a regression run of all 237 wave-3 checks through the changed oracle gave identical pass/fail results.
- **Verifier.** Claude Sonnet, reasoning-stripped, sees only citations and checks. For this wave that is also a different model family from every generator.

## One-line answers per lane

| Lane | The answer |
|---|---|
| midi-notation-ingest | midly 0.5.3 with `default-features = false, features = ["alloc"]` parses SMF inside a wasm32 export (formats 0/1/2; Metrical or Timecode timing). Malformed input only errors under midly's `strict` feature. MusicXML `<divisions>` maps to one PPQ by integer math with a divisibility test. quick-xml is not no_std. abc-parser stores note lengths as `f32`, which a no-float law cannot take as given. |
| integer-time | Evaluate tick × tempo ÷ PPQ, and tick × tempo × rate ÷ (PPQ × 10⁶), as exact rationals in u128, floored once per tempo segment with the remainder carried across segments. 480, 960 and 3840 PPQ give exact triplets and quintuplets, but no septuplets. Release builds wrap on overflow by default, so set `overflow-checks` and use checked operations. u128 is fine inside the law but never in an `extern "C"` export: its wasm export takes three parameters. |
| host-audio-and-midi | cpal's WASAPI backend is shared-mode only. Callback timestamps come from QueryPerformanceCounter, with playback predicted from buffered frames and latency. midir's WinMM input timestamps have 1 ms resolution, from zero at `midiInStart`. The two clocks need an anchor and re-anchoring. cpal fills silence before the callback. assert_no_alloc aborts on an allocation only with `AllocDisabler` registered, and only in debug by default. |
| crate-licences | What ships is MIT, Apache-2.0, Unlicense and BSD-1-Clause. Every OR expression resolves to MIT or Apache, and Unicode-3.0 is build-time only. cpal is Apache-2.0-only and ships no NOTICE. BSD-1-Clause conditions source redistribution only. midly ships no licence file. cargo-deny keys exceptions by `name` and nests `license-files` under `clarify`. |

## What the wave told the designing session (pin checks against the unsigned lock)

1. **SMPTE-timed SMF has no ticks per quarter.** "One fixed PPQ" needs a stated refusal or conversion rule for it.
2. **ABC through abc-parser 0.4.0 arrives as `f32` durations** in a private field. ABC ingest needs its own exact rational parse, or a refusal, before anything reaches the law.
3. **To refuse malformed scores, the law must build midly with `strict`.** Treating `Err` as fatal is not a substitute, because without `strict` malformed input never errors.
4. **Live MIDI input on Windows through midir/WinMM has a 1 ms floor**, which is 48 samples at 48 kHz, when placed on a sample timeline.
5. **cpal cannot open WASAPI exclusive mode.** If the lock wants exclusive mode for latency, it needs direct WASAPI or another crate.
6. **The shipped licence set is small and permissive.** cpal's Apache-2.0 attribution lands in the native host only.
7. **A sample timeline reached through a tempo map needs a remainder-carry rule in the lock.** The floor is not associative across segments: floor(a/c) + floor(b/c) can be less than floor((a+b)/c).
8. **No export argument or return may be 128 bits.** An `extern "C" fn(u128) -> u128` compiles with no lint, yet its wasm export takes three parameters.

## Pipeline lessons (recorded in full in `verification.md`)

- The OpenRouter web plugin's default engine did nothing for Gemini: 27 prompt tokens and no citations. The `exa` engine works for both Gemini and Grok.
- Generators padded lanes with checks that assert nothing, and replaced unbacked citations with pages that do not state the claim. The harness now refuses empty checks, requires two different warrant URLs, and tells the model to drop a recipe rather than pad it.
- A generator put an expected stdout on a `compiles` check, which the oracle never compared. The oracle now refuses stdout or an exit code on a check that does not run.
- Two Grok 4.7 calls cost $2.25 and $1.76. Each returned two JSON objects, so neither produced a lane. The OpenRouter account then had $3.50 of credit left, and the operator moved generation to Kimi on Ollama Cloud.

## What locks, what stays advisory

`verification.md` sets this, from the joined verifier verdicts and the compiler run. Every recipe in this tier is advisory until the si-jam-sessions lock is signed, because each one names an unsigned lock item.
