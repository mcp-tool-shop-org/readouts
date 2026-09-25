# Wave 2 — verification record

**Date:** 2026-09-25 · **Wave:** `wave-02-advanced` · 7 lanes · 70 recipes · 426 warrant-source rows · 396 code checks.

Tallies come from `scripts/wave_tallies.py --wave-dir wave-02-advanced --date 2026-09-25`.

## Who generated, who verified

The seats are the same as wave 1: one Claude Opus research seat per lane and one reasoning-stripped Claude Sonnet verifier per lane, with inputs limited to citations and checks. The non-model witness is `rustc 1.98.1 (48a229cea 2026-09-01)` through `scripts/compile_oracle.py run`. `verified = 1` comes from the ledger only, which requires a confirming verdict and no failing check.

## Gate 1 — retrieval verifier

| Lane | Confirmed | Corrected | Refuted | Unfindable | Solid / plausible | Sources ✓ / ✗ |
|---|---|---|---|---|---|---|
| traits-advanced | 10 | 0 | 0 | 0 | 10 / 0 | 49 / 0 |
| memory-layout | 8 | 2 | 0 | 0 | 10 / 0 | 68 / 0 |
| unsafe-ffi | 10 | 0 | 0 | 0 | 9 / 1 | 64 / 0 |
| concurrency-async | 9 | 1 | 0 | 0 | 9 / 1 | 67 / 1 |
| macros-const | 9 | 1 | 0 | 0 | 9 / 1 | 52 / 0 |
| performance | 10 | 0 | 0 | 0 | 10 / 0 | 68 / 0 |
| rust-currency | 10 | 0 | 0 | 0 | 10 / 0 | 57 / 0 |
| **total** | **66** | **4** | **0** | **0** | 67 / 3 | 425 / 1 |

**Corrected (4):**

- **memory-layout ×2: void, the staging defect.** These are the same defect as wave 1's cargo-modules pair. The lane file carried the `no_warnings` gate, but the verifier input dropped it. Both entries are annotated in `verification/operator-notes.json`.
- **concurrency-async ×1: citation precision.** The rustc `wasm32-wasip1-threads` page does not mention `--shared-memory` or `thread-spawn`. Both details are true of wasi-threads, but that page is not the source for them. The recipe's central claim, that Rapier's `parallel` plus `enhanced-determinism` is bitwise identical, was confirmed word for word against the CHANGELOG at the pinned tag.
- **macros-const ×1: a stale count in an engine note.** The note said `build.mjs` writes `view[at + 13..16]` "eight times". The write block occurs twice. The `i * 17` (four) and `j * 10` (two) counts are correct.

**Systemic weaknesses the verifiers named:**

- **traits-advanced:** some secondary gotchas are demonstrated only by a sibling recipe's check.
- **performance:** its timings are single-host measurements that no verifier can reproduce. They are honestly scoped.
- **rust-currency:** precise numbers in gotchas are not exercised by any check, specifically the relaxed-madd −8.67e-19 and the 22-byte delta.
- **unsafe-ffi:** the Tree Borrows and Stacked Borrows papers could not be text-extracted, so the deepest framing rests on the abstract and a co-author's post. The practical claim was reproduced directly.

## Gate 2 — the compiler

`rustc 1.98.1` ran **396 checks: 396 pass, 0 fail**. By lane: traits-advanced 77, memory-layout 29, unsafe-ffi 71, concurrency-async 57, macros-const 63, performance 41, rust-currency 58.

68 of the 70 recipes carry checks. The other two are in performance (profilers, which are documentation-only) and rust-currency (Cargo behaviour, measured with `cargo +1.98.1`).

The run was repeated after the concurrency-async tightening described below. Results are in `verification/compile-2026-09-25/wave-02-advanced.json`.

## Pipeline notes shared with wave 1

**Staging defect.** The same staging defect and fix apply as in wave 1's record.

**UTF-8 decoding and lint regex.** The oracle's UTF-8 decoding fix and its lint regex fix also apply.

**Label-vs-gate lint.** The lint found one wave-2 check (concurrency-async #7, "thread_local! … silently …"), which was tightened with `no_warnings` and still passes.

**Verifiers resisted mid-run instructions.** Five verifiers treated the mid-run notice about regenerated inputs as unverified: performance, rust-currency, unsafe-ffi, macros-const and rapier-core (wave 3). Each one diffed its input file itself before trusting it. Next time, fix staged inputs before launch.

## Post-ingest

`load_db.py` ingested 70 recipes, 396 checks and 415 source rows. All 70 are verified, with 68 carrying compiler checks. `meta.latest_wave` is 2. The repository floor, `python verify.py`, runs on the publishing branch before push.

- **Re-assembled with wave 3's two pipeline fixes (2026-09-25).** The published checks now carry every gate the oracle enforced, and the operator notes reach the database whole. See wave 3's verification record. No verdict or compiler result changed.

## What may lock architecture

**Load-bearing:** all 70 recipes.

**Advisory:**

- the three `plausible` recipes;
- every single-host measurement, as each recipe states it;
- Rapier's own claim that `parallel` with `enhanced-determinism` is bitwise identical, which is unmeasured here.
