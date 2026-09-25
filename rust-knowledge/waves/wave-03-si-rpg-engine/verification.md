# Wave 3 — verification record

**Date:** 2026-09-25 · **Wave:** `wave-03-si-rpg-engine` · 9 lanes · 90 recipes · 526 warrant-source rows · 237 code checks.

Tallies come from `scripts/wave_tallies.py --wave-dir wave-03-si-rpg-engine --date 2026-09-25`.

## Who generated, who verified

The seats are the same as in waves 1 and 2:

- one Claude Opus research seat per lane;
- one reasoning-stripped Claude Sonnet verifier per lane, whose inputs are limited to citations and checks;
- the non-model witness, `rustc 1.98.1 (48a229cea 2026-09-01)`, run through `scripts/compile_oracle.py run`.

`verified = 1` comes from the ledger only. It requires a confirming verdict and no failing check.

Two of the nine lanes, restore-internals and binary-and-limits, were answer seats for the eight questions the engine's coordinator filed. A third seat measured the costs of T2's routes (a) and (c) and wrote `requests/route-costs-a-c.md`. That report is a request answer, not a lane, so it carries no verifier verdict.

The coordinating session's own measurements are in `dispatch.md` under "Advisor measurements". Each names its program in `probes/` and the command that reruns it.

## Gate 1 — retrieval verifier

| Lane | Confirmed | Corrected | Refuted | Unfindable | Solid / plausible | Sources ✓ / ✗ |
|---|---|---|---|---|---|---|
| wasm-raw-abi | 7 | 3 | 0 | 0 | 10 / 0 | 47 / 0 |
| float-determinism | 10 | 0 | 0 | 0 | 9 / 1 | 66 / 0 |
| rapier-core | 7 | 3 | 0 | 0 | 10 / 0 | 48 / 0 |
| restore-internals | 10 | 0 | 0 | 0 | 10 / 0 | 36 / 0 |
| rapier-shapes-kcc | 9 | 1 | 0 | 0 | 8 / 2 | 54 / 2 |
| binary-and-limits | 10 | 0 | 0 | 0 | 10 / 0 | 47 / 0 |
| sim-architecture | 9 | 1 | 0 | 0 | 9 / 1 | 87 / 1 |
| host-embedding | 10 | 0 | 0 | 0 | 10 / 0 | 74 / 0 |
| ci-reproducible-builds | 8 | 2 | 0 | 0 | 9 / 1 | 63 / 1 |
| **total** | **80** | **10** | **0** | **0** | 85 / 5 | 522 / 4 |

**Corrected (10):**

- **wasm-raw-abi ×3: true claims that no check asserted.** The verifier confirmed each claim with its own counter-example:
  - a `pub` function without `no_mangle` is absent from the exports;
  - `#[link(wasm_import_module = "host")]` yields the import `host.host_log`;
  - an out-of-range index panics into a `RuntimeError: unreachable` trap, and a write made before the panic survives it;
  - `__heap_base` and `__data_end` export as globals.

  After the verdict, `scripts/tighten_checks.py` gave the first three claims gates the oracle gained during this wave: `wasm_absent_exports`, an exact `wasm_imports`, and a new check that must trap. Each gate was dry-run beside a planted wrong value, and each planted value failed.

  Three things stay unasserted: that the write survives the trap (a check makes one call), the trap text on engines other than V8, and the export kind (the oracle has no gate for it).
- **rapier-core ×3.** Two engine notes had gone stale the same day:
  - T4 pin 2, amended on main, no longer assumes the fast box tunnels;
  - T3 pin 6 already says "no new hash" for event order.

  The third correction is one compressed step order: joins drain after quarantine and user changes, not alongside wake-ups.
- **rapier-shapes-kcc ×1.** An engine note said the law builds only cuboid colliders. `rapier_law.rs:425-431` on main builds `ColliderBuilder::capsule_y` for driven bodies with shape 1.
- **sim-architecture ×1.** "f64 cannot represent every Duration" is on the docs of `Duration::mul_f64`, not those of `from_secs_f64`.
- **ci-reproducible-builds ×2.**
  - The disable syntax `-Ctarget-feature=-foo` is documented on rustc's codegen-options page, not on the `wasm32-unknown-unknown` page.
  - `canon_zero` is in `solver/src/rapier_law.rs`, not `lib.rs`. No engine document on main mentions it.

**Unsupported source rows (4):**

- Two of these, in rapier-shapes-kcc, are rows where the recipe's claim was established from source or from a rerun, and the cited page does not state it.
  - One of them is rapier's own `ColliderBuilder` doc, which is wrong: it calls a heightfield's scale the "size of each grid cell".
- The Duration page, in sim-architecture.
- The wasm32 platform page, in ci-reproducible-builds.

**Plausible (5):**

- float-determinism: the call chain from `solver_step` into parry's BVH optimizer rests on one scratch-build measurement.
- rapier-shapes-kcc: the capsule engine note above, and the row-0 `FIX_INTERNAL_EDGES` numbers, which were not re-executed.
- sim-architecture: the Duration recipe.
- ci-reproducible-builds: the flags recipe.

**Systemic weaknesses the verifiers named:**

- **Engine citations are perishable.** Four lanes said so in different words:
  - restore-internals and binary-and-limits cite pins and pull requests that moved the same day;
  - rapier-core found two notes already stale;
  - rapier-shapes-kcc noted that an uncited claim about the engine's current source is the one place prose can drift unnoticed.

  The response is 14 `citation-anchor` operator notes that pin each citation to the commit the verifier checked (see below). Every engine note stays advisory until it is re-checked against main.
- **sim-architecture:** six crates the lane cites are outside the oracle's dependency set: bevy_time, ggrs, backroll, blake3, bevy_ecs and hecs. Claims about them rest on retrieved documentation. None of them is an engine dependency.
- **host-embedding:** shelf life. Wasmtime ships monthly majors; 49.0.1 and 48.0.3 shipped a fuel-spend security fix the day before the sweep. The engine had moved 17 commits past the commit the lane pinned.
- **float-determinism:** no check re-verifies the reachability claim above, so a dependency bump could break it silently.
- **ci-reproducible-builds:** citation drift at the margins. A claim occasionally borrows the authority of a page that supports an adjacent fact.
- **binary-and-limits:** the dense-scene page counts were not re-derived.

## Gate 2 — the compiler

`rustc 1.98.1` ran **237 checks: 237 pass, 0 fail**. By lane:

| Lane | Checks |
|---|---|
| wasm-raw-abi | 41 |
| float-determinism | 47 |
| rapier-core | 23 |
| restore-internals | 19 |
| rapier-shapes-kcc | 25 |
| binary-and-limits | 19 |
| sim-architecture | 35 |
| host-embedding | 17 |
| ci-reproducible-builds | 11 |

81 of the 90 recipes carry checks. The other nine are host-embedding (3) and ci-reproducible-builds (6): runtime configuration, CI workflow and Cargo behaviour, measured with `cargo +1.98.1` where they could be.

The run was repeated after the wasm-raw-abi tightening. Results are in `verification/compile-2026-09-25/wave-03-si-rpg-engine.json`.

## Pipeline notes

**Assembly dropped the gates from the published record, in every wave.** `assemble_lanes.py --final` copied a fixed list of check fields into `research-raw.json`:

- `label` … `stdout`, then `source`.

It left out every other gate the oracle had enforced:

- `no_warnings`, `stderr_contains`, `stdout_contains` and `exit_code`;
- every `wasm_*` gate.

So the database and the code pages under-reported what 566 of the 943 checks assert. This is the same shape as the staging defect in wave 1's record: a hand-written field list beside `CHECK_FIELDS`. The fix has four parts:

- one helper, `check_view()`, now serves both staging and the final pass;
- `checks.gates` holds the rest as JSON, and `load_db.py` migrates an older database;
- each code-page caption says what its check asserts;
- waves 1 and 2 were re-assembled with the fix.

The compiler's verdicts were never affected, because the oracle reads the lane files.

**Operator notes were cut mid-sentence.** `build_ledger.py` cut the verifier's note plus the operator's note at 500 characters from the end. The closing sentence of each of the four void-correction notes never reached the database. The fix:

- `append_note()` now trims the verifier's text, never the note;
- the cap is 600, because `merge_verdicts` caps the verifier's own note at 240;
- the void-correction wording now cites the oracle run instead of asserting the verdict.

**Citation anchors.** Fourteen operator notes of kind `citation-anchor` pin the engine citations:

- restore-internals ×8: "pin N" means `docs/dispatch-t2-restore.md` at `ee2e50a`, the head of PR #43, which closed unmerged. Main rewrote that dispatch at `9c47d40`.
- binary-and-limits ×6: "PR #44" means its head `b99a636`, built on #43's rebuild-per-quantum law.

Operator notes never change a verdict.

**Verifiers and mid-run messages.** The wasm-raw-abi verifier also treated the mid-run notice about regenerated inputs as a claim to check. It re-read its live input and found the notice only partly true: 7 checks across 6 recipes had gained fields, and none of its three gaps had been touched. This matches wave 2's record: fix inputs before launch.

**Oracle gates added mid-wave.** `wasm_absent_exports`, exact `wasm_imports` and `wasm_trap` were each self-tested with planted failures. The wasm-raw-abi tightening is their first use in a lane.

## Post-ingest

`load_db.py` ingested 90 recipes, 237 checks and 526 source rows. All 90 are verified, and 81 carry compiler checks. `meta.latest_wave` is 3. The knowledge base now holds:

- 230 recipes, all verified;
- 943 checks, all passing.

The repository floor, `python verify.py`, runs on the publishing branch before push.

## What may lock architecture

**Load-bearing:**

- the 85 solid recipes;
- above all restore-internals and binary-and-limits (answers 1–8), which the engine has already built on: T2 revised to route (d)+(e), T3 pins 10–11, and T4 pins 2 and 5.

**Advisory:**

- the five plausible recipes;
- every engine note until it is re-checked against main. The citation anchors say which commit each one was verified against.
- single-seat measurements:
  - the route costs for (a) and (c), from one Windows x86_64 desktop with unit cubes only;
  - the dense-scene page counts;
  - the toolchain call-graph reachability;
- ARM64, which is unmeasured everywhere;
- consoles, which appear on no retrieved page;
- host-embedding's runtime recipes, to re-check when the host phase pins a runtime.
