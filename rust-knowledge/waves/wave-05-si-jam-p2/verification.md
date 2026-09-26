# Wave 5 — verification record

**Date:** 2026-09-25 · **Wave:** `wave-05-si-jam-p2` · 3 lanes · 13 recipes · 29 warrant-source rows · 19 code checks.

Tallies come from `scripts/wave_tallies.py --wave-dir wave-05-si-jam-p2 --date 2026-09-25 --sweep sweep-2026-09-25-w5`. The verdicts sit in their own sweep folder, `verification/sweep-2026-09-25-w5/`, because this wave's lane slugs repeat wave 4's on the same date.

## Who generated, who verified

| Lane | Generator | Calls | Tokens in / out | Cost | Rounds |
|---|---|---|---|---|---|
| midi-notation-ingest | Kimi k2.6, `kimi-k2.6:cloud` (Ollama Cloud, digest `a90cd0d1…`) | 3 | 100,181 / 58,910 | none (plan) | Round 0 hit the 32,000-token output cap inside its JSON, so there was no lane. Round 1 had 3 of 9 checks failing. Round 2 was clean. |
| host-audio-and-midi | Kimi k2.6 | 1 | 24,670 / 22,794 | none (plan) | clean at round 0 |
| integer-time | Grok 4.7 in a Cursor chat seat, through `scripts/seat_lane.py` | 1 reply | not visible to the harness | the chat seat's subscription; no per-call record | clean at round 0 |

The seat's receipt (`receipts/integer-time.json`, a copy of `seats/grok-cursor/integer-time.receipt.json`) records:

- the SHA-256 of the brief, the scope, the user prompt and the adapter;
- the pack manifest and the URLs the seat could tag as opened;
- the reply's SHA-256 and the model name the chat reported.

The prompt files themselves quote pinned crate source without its licence notice. They are kept out of git, as the harness does for Kimi's prompts, and their hashes stand in for them.

**The attempt that did not produce a lane.** Kimi k2.6 also ran integer-time:

- Round 0 (11:39 to about 12:34) returned no JSON object holding recipes, and so did round 1 (to 13:23).
- The operator stopped round 2 at 13:32, after the Grok seat's lane had come back clean and been adopted. The harness writes its lane, packet and receipt on exit, so a finished run would have overwritten the adopted lane.
- The in-memory receipt was lost with the process. `receipts/integer-time.kimi.json` is reconstructed from the harness log.

The verifier is Claude Sonnet, reasoning-stripped, reading only citations and checks under `briefs/VERIFIER-BRIEF-W5.md`, which quotes the signed lock items. Its bucket is `<lane>@wave-5`, and it is a different model family from both generators. The non-model witness is `rustc 1.98.1` through `scripts/compile_oracle.py`, with the `jam` and the new `jam-strict` dependency sets.

## Gate 1 — retrieval verifier

| Lane | Confirmed | Corrected | Refuted | Unfindable | Solid / plausible / shaky-or-worse | Sources ✓ / ✗ |
|---|---|---|---|---|---|---|
| integer-time | 5 | 0 | 0 | 0 | 5 / 0 / 0 | 12 / 0 |
| midi-notation-ingest | 1 | 3 | 0 | 0 | 3 / 0 / 1 | 9 / 0 |
| host-audio-and-midi | 3 | 1 | 0 | 0 | 4 / 0 / 0 | 8 / 0 |
| **total** | **9** | **4** | **0** | **0** | 12 / 0 / 1 | 29 / 0 |

**Corrected (4):**

- **midi-notation-ingest ×3:**
  - **Two of the three strict pairs.** The alloc-only check in each pair asserts only `is_ok()`, not the permissive outcome its prose states: an empty track after truncation, and 0xFF masked to 0x0F. The verifier confirmed both outcomes with its own runs (`tracks[0].len() == 0`; `channel.as_int() == 15`), so the claims stand, but the checks would not catch a regression.
  - **The SMPTE-refusal export.** It was re-adjudicated from confirmed to corrected, with currency wrong, after a later measurement (below).
    - As written, it claims "without panicking". But a division word starting 0x80 panics inside `Smf::parse` in strict and alloc-only builds alike, and the recipe's own export hangs.
    - Its correction: read bit 15 of the division word, and refuse before calling midly.
    - It lands verified but marked **avoid**: the loader maps currency wrong to avoid, so it is never listed as recommended.
- **host-audio-and-midi ×1.** The assert_no_alloc recipe's check exercises only the path that does not allocate. The abort half is real, and the verifier's own counter-example aborted, but no check in this recipe shows it.

**Systemic weaknesses the verifiers named:**

- **integer-time: every check is self-referential.** The same Rust program derives its numbers and asserts them, so a shared conceptual error would compile and pass. The verifier re-derived every number independently, in Python big integers, for all four PPQs. It also ran one counter-example of its own (tick = tempo = 10¹⁵, PPQ 1), which shows the export's u64-quotient refusal is a real path separate from the tested zero-PPQ one. Four of the five recipes lean on one page, the std `u128` docs, for their API warrant.
- **midi-notation-ingest:** on the alloc-only side, the checks assert `is_ok()` where the prose claims a specific value. This is the source of both pair corrections.
- **host-audio-and-midi:** the zero-allocation claims are backed by a negative control that proves the counter works. The assert_no_alloc abort claim has no such check.

## Gate 2 — the compiler

`rustc 1.98.1` ran **19 checks: 19 pass, 0 fail.** By lane:

| Lane | Checks | Recipes with checks | Dependency sets |
|---|---|---|---|
| midi-notation-ingest | 9 | 4 | `jam` for the alloc-only side, `jam-strict` for the strict side and the wasm32 export |
| integer-time | 6 | 5 | `jam`, host, plus wasm32 for the export |
| host-audio-and-midi | 4 | 4 | `jam`, host |

Results are in `verification/compile-2026-09-25/wave-05-si-jam-p2.json`.

## Later measurements (after the verdicts)

1. **midly 0.5.3 panics on a division word starting 0x80.**
   - The lead came from the si-jam-sessions ingest agent, which had measured it. It was reproduced here under the compiler and in midly's source. `Timing::read` computes `-(bit_range!(raw, 8..16) as i8)`, and negating -128 overflows.
   - With overflow checks on, as in the lock's release profile, `Smf::parse` panics, strict or not. 0x81 returns an error, and 0xE8, 0xE7, 0xE3 and 0xE2 parse as 24, 25, 29 and 30 fps.
   - Even with strict, midly unwraps RIFF RMID files and skips unknown chunks.
   - Evidence: `verification/measurements/2026-09-25-midly-timecode-0x80.json`, checks 1 to 5.
   - It changed recipe 4's verdict (above), and it adds a note to wave 4's `parse-smf-formats-and-timing`: refuse bit 15 before calling midly.
2. **What a wasm32 export does on that panic depends on its panic handler.** All on recipe 4's export with that input:
   - A `#![no_std]` `loop {}` handler never returns; the verifier's run hung.
   - A handler that calls `core::arch::wasm32::unreachable()` traps, so the host sees a RuntimeError.
   - A crate with no handler of its own that links std unnamed (`extern crate std as _;`, panic abort) also traps, under both dev and release flags, and its module imports nothing. A 96-PPQ control returns 0, so std's allocator works there.
   - In that crate a std path does not resolve (E0433). One `extern crate std;` line in any module binds the name again and compiles, so the `_` binding is a review boundary, not a wall.
   - The last setup is the si-jam-sessions law crate's root, which that session had reasoned about but not measured. Evidence: the same file, checks 6 to 11. It is recorded in recipe 4's note.
3. **Cargo unifies features per command.** The test is a two-member workspace in which one member enables midly/strict.
   - `cargo tree -p` on the other member shows midly with `alloc` only.
   - `--workspace`, and a bare command at the virtual root, show `alloc` + `strict`.
   - So a workspace that has a strict member measures alloc-only behaviour only with `-p`, or in a workspace of its own.
   - Evidence: `verification/measurements/2026-09-25-cargo-feature-unification.json`. It is recorded as a note on each of the three strict pair recipes.

Operator notes annotate a verdict and never change it. The one verdict that changed, recipe 4's, was changed by its verifier.

## Pipeline notes

**A chat seat can write a lane under the harness's contract.** `scripts/seat_lane.py` gives a model in a chat the harness's own prompts and the same gates: source admission, the vacuous-check refusal, the lane lint, the compiler and the final admission. This is the first lane written that way. Two limits:

- The harness cannot see the chat's token use.
- A chat can run anything its host allows. The handoff therefore limits the seat to one folder and to `cargo +1.98.1` with nothing installed. The lane was re-checked from its files, not from the seat's report.

**A running generator can overwrite an adopted lane.** The harness writes its lane, packet and receipt when it exits, so a round that finishes after adoption would replace the adopted lane. Kimi was stopped by pid for that reason.

**`assemble_lanes.finalize` credited every wave to Claude Opus.** Its opening sentence was a constant written when waves 1 to 3 were the only ones. Wave 4 shipped under it, although Kimi and Gemini wrote that wave. The fix:

- The sentence now comes from each wave's `seats` line in `briefs/lanes.json`.
- Wave 4's `research-raw.json` is corrected.
- The same sentence named the shared verifier brief for every wave; it now names a wave's own brief when one exists.

**`wave_tallies.py` would have printed wave 4's verdicts as wave 5's.** It read `sweep-<date>`, and wave 5's lane slugs and date match wave 4's. It now takes `--sweep`, as `assemble_lanes.py` does. Without it, midi-notation-ingest would have shown 4 confirmed, 2 corrected and 1 refuted, which are wave 4's figures.

**Kimi's midi round 0 filled its 32,000-token output budget inside the JSON.** The harness recorded the parse error and asked again. Round 1 fitted in 19,149 tokens.

## Post-ingest

`load_db.py` ingested 13 recipes, 19 checks and 29 source rows. All 13 are verified, including the export marked avoid. `meta.latest_wave` is 5. The knowledge base now holds:

- 280 recipes, 279 of them verified (the one that is not is wave 4's refuted ABC recipe);
- 989 checks, all passing.

The same rebuild applied two earlier changes that had been committed without a rebuild:

- The loader's corrections-first notes: 30 older recipes now open with their correction.
- The 32 consumed-pin notes: all 56 recipes that carry an operator note now show it, against 20 before. The other 4 are this wave's.

A snapshot diff of `rust.db` before and after shows these two changes, the 13 new recipes with their notes, and wave 4's corrected seats line. It shows no other change.

## What may lock architecture

The lock is signed, so this wave answers it rather than waiting for it.

- **Load-bearing (all solid):**
  - the integer-time lane: the 24-of-24 tuplet table, the overflow bound, the remainder carry, and the u64-in, u64-out export with its status export;
  - the three strict pairs, as ingest test input;
  - the host lane's allocation count, with its negative control and its construction order.
- **Avoid as written:** the SMPTE-refusal export. Its correction and notes say what to do instead.
- **Advisory:**
  - assert_no_alloc's abort half, which has no check in this wave;
  - the 0/1/2/3 status numbering, a generator's suggestion;
  - any claim about device behaviour, which the oracle cannot run without a device.
