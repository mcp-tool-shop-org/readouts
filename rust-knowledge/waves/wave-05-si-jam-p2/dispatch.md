# Wave 5 — si-jam-sessions: the signed lock's arithmetic, parser and callback, checked (P2)

**Date:** 2026-09-25 · **KB:** `rust-knowledge` · **Tier:** si-jam-sessions · **Lanes:** 3 (the P2 asks) · **Seats:** generators outside the Claude family (Kimi k2.6 and Grok 4.7), a Claude Sonnet verifier, and the compiler

## Why this wave exists

After wave 4, si-jam-sessions signed its design lock (`docs/PHASE-0.md` @ `e3cc85e`) and took 32 of this KB's recipes as pins. Each of those recipes now carries a `consumed-pin` operator note. The lock pins, among other things:

- PPQ 3360, and a u128 tick-to-sample floor with the remainder carried across tempo segments;
- `checked_*` arithmetic, with `overflow-checks = true` in release;
- midly 0.5.3 with `alloc` + `strict`, and SMPTE-timed files refused;
- an edition-2024 `wasm32-unknown-unknown` cdylib whose exports return status codes: a panic never crosses the boundary, and no argument or return is wider than 64 bits;
- a cpal 0.18.2 WASAPI shared-mode host that moves events through an rtrb ring buffer, with no allocation in the callback.

The session then ranked three questions for this wave:

- **A. Integer time at PPQ 3360:** the tuplet table down to the 128th, the u128 overflow bound at tempo 0xFFFFFF, and the remainder carry compared with 480, 960 and 3840.
- **B. midly `strict`, compiled:** what strict refuses that the alloc-only build accepts.
- **C. The callback's no-allocation rule, checked:** a measurement the host can run, rather than a promise.

Each became one lane. The wave has its own briefs, `briefs/GENERATOR-BRIEF-W5.md` and `briefs/VERIFIER-BRIEF-W5.md`, which quote the signed lock items. Each recipe's `engine_note` names the pin it serves.

## Seats

- **Generators.** midi-notation-ingest and host-audio-and-midi were written by Kimi k2.6 (`kimi-k2.6:cloud` on Ollama Cloud, digest `a90cd0d1…`) at temperature 0, through `scripts/openrouter_lane.py`. OpenRouter itself was not used in this wave. integer-time was written by **Grok 4.7 in a Cursor chat seat**. Kimi's first round on that lane returned no JSON, so the chat seat was opened in parallel. Kimi's second round also returned no JSON, while the seat's lane came back clean. The operator adopted the seat's lane and stopped Kimi in its third round.
- **A chat seat under the harness's contract.** `scripts/seat_lane.py` gives a chat model exactly what the harness gives Kimi, and applies the same gates to what comes back:
  - `prompt` writes the byte-identical system and user prompts, plus a receipt with their SHA-256s, the pack manifest, the URLs the seat may tag as opened, and a cap of three revision rounds;
  - `check` runs the harness's own normalisation, source admission, vacuous-check refusal, lane lint and compiler on a reply, and prints the harness's own review;
  - `final` applies the harness's final admission, which drops any check that never passed and any recipe the contract cannot admit, then writes the lane, packet and receipt.

  The seat writes only inside `seats/grok-cursor/`. Its handoff is `briefs/KICKOFF-W5-integer-time-grok-cursor.md`. It was clean at round 0: 5 recipes, 6 checks, nothing dropped. Before adoption the lane was re-checked independently of the seat's report. The receipt's hashes match, a fresh compiler run passed 6 of 6, and every opened URL is in the pack.
- **Compiler.** A third dependency set, `oracle-jam-strict/`, holds midly 0.5.3 with `alloc` + `strict` (the law's own configuration), built for the host and for wasm32. A check selects it with `"oracle_set": "jam-strict"`. It is a separate crate because cargo unifies features over the packages that one command builds. Adding `strict` to the jam set would have changed what every wave-4 midly check measured.
- **Verifier.** Claude Sonnet, reasoning-stripped, seeing only citations and checks. It is a different model family from both generators.

## One-line answers per lane

| Lane | The answer |
|---|---|
| integer-time (ask A) | At PPQ 3360, every 3:2, 5:4 and 7:4 tuplet of the eight note values from a whole note to a 128th is a whole number of ticks: 24 of 24. At 480, 960 and 3840, the 3:2 and 5:4 tuplets are, and no 7:4 tuplet is. With tempo at most 0xFFFFFF µs per quarter and 48 kHz, tick × tempo × 48000 fits in u128 for every tick through 422,550,225,262,032,543,670,307,476. So every u64 tick is safe, and only the conversion back to u64 can refuse. Carrying each segment's remainder equals one floor of the whole span, while summing separate floors comes out one sample low: two one-tick segments at tempo 0xFFFFFF, at each of 3360, 480, 960 and 3840. The floor exports from a wasm32 cdylib as u64 in and u64 out, with the u128 inside, and a status export reports the refusal. |
| midi-notation-ingest (ask B) | Three byte-level pairs where strict refuses what alloc-only accepts. The first is a header track count that does not match the MTrk chunks. The second is an MTrk length that runs past the end of the file, where alloc-only keeps an empty track. The third is a MidiChannel meta-event above 0x0F, where alloc-only masks it to 0x0F. The SMPTE-refusal export is marked avoid. midly 0.5.3 panics on a division word starting 0x80, strict or not, so the refusal has to read bit 15 before calling midly. |
| host-audio-and-midi (ask C) | A counting `#[global_allocator]` records zero allocations across a simulated callback that pops rtrb into a stack buffer. A planted `Vec::push` in the same body is counted, which is the negative control. rtrb 0.4.0 allocates only in `RingBuffer::new`, so the ring is built before the stream starts. assert_no_alloc's `AllocDisabler` returns normally on the clean path. Its abort path is real, but no check in the lane exercises it. |

## What the wave told the designing session (pin checks against the signed lock)

Each lane went to the si-jam-sessions session once it was verified, with an evidence level and a pin-check line.

1. **Host (ask C): consistent with the host pin.**
   - Items 1 and 2 became the host slice's callback test; item 3 is its construction order; item 4 is a debug-only guard.
   - The session carries its own abort test, and does not cite the abort half as verified here.
2. **Ingest (ask B): consistent with the ingest and export pins.**
   - The three byte pairs, with their alloc-only and strict outcomes, went to the session's ingest agent as test input, with the advice to assert the specific refusal rather than `is_err()`.
   - The 0/1/2/3 status numbering was flagged as the generator's suggestion, not a verified pin.
3. **Integer time (ask A): consistent with the time pins.**
   - The session's law core already computes the product in u128 and refuses only at the u64 conversions.
   - It added the tuplet table and a carry pair (479 against 478 at PPQ 3360) as cross-check tests that cite this lane.
   - Two suggestions went beyond the lock and were flagged as such:
     - refuse files whose PPQ does not rescale exactly to 3360 (96, 120, 240 and 480 do; 192, 384, 960 and 1920 do not);
     - do not treat the export recipe's `u64::MAX` return as a refusal, because it collides with a genuine quotient.
   - The session's ingest applies a finer rule: it refuses only events whose tick × 3360 is not a multiple of the file's PPQ. Its exports return status codes.
4. **midly and a division word starting 0x80.**
   - The lead came from the session's ingest agent and was reproduced here under the compiler and in midly's source.
   - Recipe 4 went back to its verifier and came back corrected, currency wrong, marked avoid.
   - Notes were added to recipe 4 and to wave 4's `parse-smf-formats-and-timing`.
   - No upstream midly issue has been filed. That is the operator's call.
5. **Panic handlers in a wasm law.** Measured here, on recipe 4's export with that input:
   - a `loop {}` handler hangs the host's call;
   - a handler that calls `core::arch::wasm32::unreachable()` traps;
   - a `#![no_std]` crate with no handler that links std unnamed (`extern crate std as _;`, panic abort), as the session's law crate does, also traps, and its module imports nothing.

## Pipeline lessons (recorded in full in `verification.md`)

- A chat model can write a lane under the harness's contract, through `scripts/seat_lane.py`, with the same gates and a receipt.
- A generator still running can overwrite a lane that has already been adopted, because the harness writes its lane on exit. Stop it before it finishes.
- `assemble_lanes.finalize` credited every wave to "Claude Opus", which published wave 4 with the wrong generators. It now reads each wave's `seats` line, and wave 4's record is corrected.
- `wave_tallies.py` would have printed wave 4's verdicts as wave 5's, because the two waves share lane slugs and a date. It now takes `--sweep`.

## What locks, what stays advisory

`verification.md` sets this, from the joined verifier verdicts, the compiler run and the later measurements.
