# Wave 1 — verification record

**Date:** 2026-09-25 · **Wave:** `wave-01-essentials` · 7 lanes · 70 recipes · 369 warrant-source rows · 310 code checks.
Tallies come from `scripts/wave_tallies.py --wave-dir wave-01-essentials --date 2026-09-25`.

## Who generated, who verified

| Seat | Model / tool | Saw | Wrote |
|---|---|---|---|
| Research (7 lanes) | Claude Opus, one seat per lane | `briefs/LANE-BRIEF.md`, its lane object in `briefs/lanes.json`, the web, the pinned sources, the compile oracle for self-checks | `lanes/<lane>.json`, `<lane>.md` |
| Retrieval verifier (7 lanes) | Claude Sonnet, one reasoning-stripped seat per lane | `briefs/VERIFIER-BRIEF.md` + `verification/sweep-2026-09-25/lanes/<lane>.input.json` (recipes, checks and citations only) | `verification/sweep-2026-09-25/lanes/<lane>.json` |
| Compiler (not a model) | `rustc 1.98.1 (48a229cea 2026-09-01)` via `scripts/compile_oracle.py run` | every check in every lane | `verification/compile-2026-09-25/wave-01-essentials.json` |

`verified = 1` comes only from the ledger (`verification/verdicts.json`, built by `scripts/build_ledger.py`). That requires a confirming verdict and no failing check. The research seats' own `currency` field was left null and ignored.

## Gate 1 — retrieval verifier

| Lane | confirmed | corrected | refuted | unfindable | solid / plausible | sources ✓ / ✗ |
|---|---|---|---|---|---|---|
| ownership-borrowing | 7 | 3 | 0 | 0 | 7 / 3 | 47 / 1 |
| types-patterns | 10 | 0 | 0 | 0 | 10 / 0 | 58 / 0 |
| traits-generics | 10 | 0 | 0 | 0 | 10 / 0 | 66 / 0 |
| errors-panics | 10 | 0 | 0 | 0 | 9 / 1 | 50 / 0 |
| collections-iterators | 10 | 0 | 0 | 0 | 10 / 0 | 48 / 0 |
| cargo-modules | 8 | 2 | 0 | 0 | 10 / 0 | 35 / 0 |
| testing-tooling | 10 | 0 | 0 | 0 | 9 / 1 | 64 / 0 |
| **total** | **65** | **5** | **0** | **0** | 65 / 5 | 368 / 1 |

**Corrected (5).**

- *ownership-borrowing ×3.*
  - One citation named the ICSE 2022 paper's "Finding 6" for an array-vs-tuple result. The verifier extracted the PDF text, and it is Finding 5. That source is marked unsupported.
  - Two recipes rested their edge case (indexing activates a two-phase borrow; indexing is "impure" for closure capture) on 2017 RFCs alone. The verifier wrote counter-examples, ran them on 1.98.1, and confirmed both behaviours still hold. The confirmation is recorded in the corrections.
- *cargo-modules ×2.* **Void; see the staging defect below.** Both say a check lacks a `wasm_no_imports` or `no_warnings` gate. The lane file had both gates; the verifier's input did not. Each is annotated through `verification/operator-notes.json`, and neither verdict was changed.

**Systemic weaknesses the verifiers named.**

- The sharpest claims rest on checks rather than a second web source (types-patterns). That is by design: the compiler is the witness.
- Secondary gotchas sometimes lean on a sibling recipe's check, not their own (collections-iterators).
- Engine citations by line number drift as `main` moves; cite by function (errors-panics).
- The ICSE finding-number miscite (ownership-borrowing).

## Gate 2 — the compiler

`rustc 1.98.1` ran **310 checks: 310 pass, 0 fail**:

| Lane | checks |
|---|---|
| ownership-borrowing | 74 |
| types-patterns | 56 |
| traits-generics | 48 |
| errors-panics | 46 |
| collections-iterators | 30 |
| cargo-modules | 23 |
| testing-tooling | 33 |

66 of the 70 recipes carry checks. The 4 without are claims about Cargo and rustup behaviour: 3 in cargo-modules, 1 in testing-tooling. Their evidence is real `cargo +1.98.1` runs recorded in the recipe text. The run file is `verification/compile-2026-09-25/wave-01-essentials.json`. It was re-run after the tightenings below, so it reflects the final lane files.

**Host-specific checks.** Two errors-panics checks assert Windows' abort status, 0xC0000409; on Unix it is SIGABRT. Their recipes say so.

## Defects found in this KB's own pipeline, and fixed

1. **Staging dropped two check fields (`no_warnings`, `wasm_no_imports`) from the verifier inputs.** Two verifiers, cargo-modules and memory-layout (wave 2), correctly reported gates "missing" that the lane files had.
   - Fix: `assemble_lanes.py` now stages every field the oracle reads (`CHECK_FIELDS`), and every input was regenerated.
   - The four void corrections are annotated in `verification/operator-notes.json`, which `build_ledger.py` applies without changing a verdict.
2. **The oracle decoded program output with the Windows code page** when Python was not in UTF-8 mode, and a non-ASCII check failed. A research seat reported it. Every subprocess now decodes UTF-8, and the self-test is unchanged.
3. **The oracle's lint detector missed crate-level `#![deny(..)]` notes.** It was found while checking S1 pin 5, and broadened to `#!?[..]`.
4. **Labels that promise more than their checks assert.** A new lint in `assemble_lanes.py` flags a label that promises silence or an import-free module without the gate. It found three types-patterns checks in this wave. They were tightened with `no_warnings` (`scripts/tighten_checks.py`) and still pass.

**A lesson recorded for the next wave.** Several verifiers treated the mid-run notice about regenerated inputs as a possible injection and verified the files themselves. That is the right instinct for this role. Fix staged inputs before launch, never while verifiers run.

## Post-ingest

- `scripts/build_ledger.py`: 4 operator notes applied, and the compile gate set 0 recipes unverified.
- `load_db.py`: 70 recipes, 310 checks and 365 source rows were ingested, all 70 verified.
- **Re-assembled with wave 3's two pipeline fixes (2026-09-25).** The published checks now carry every gate the oracle enforced, and the operator notes reach the database whole. See wave 3's verification record. No verdict or compiler result changed.
- `meta.latest_wave` was refreshed.
- **One example path edited before publication (2026-09-25).** The rustflags recipe ("Treat Cargo's rustflags sources as exclusive") shows RUSTFLAGS splitting a `--remap-path-prefix` argument at a space. Its made-up folder `A B` sat inside the Windows user-profile folder, which trips every home-path gate the public export runs. The path now reads `C:\A B\.cargo`, in the lane and in the verifier's staged input. The verifier saw the original. The claim is about the space, and neither the verdict nor any check changed.

The repository floor, `python verify.py`, is run on the branch that carries this KB before it is pushed. Its result is recorded in the commit.

## What may lock architecture

**Load-bearing:** all 70 recipes.

**Advisory:**

- the 5 `plausible` recipes;
- every claim its recipe marks as measured on this host;
- the one source marked unsupported (the ICSE finding number), whose recipe stands on its other warrants.
