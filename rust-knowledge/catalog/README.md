# Catalog — Rust for building si-rpg-engine

Generated from `rust.db` · wave 5 · 2026-09-25. NEVER hand-edited — regenerated from the DB.

280 recipes · 279 verified · 989 code checks, 989 passing under the pinned compiler (rustc 1.98.1). Two independent verdicts per recipe: **currency** from an adversarial retrieval verifier (a different model than the author, reasoning-stripped) and **compile** from the compiler itself. `verified` needs both. The engine-facing index is [engine.md](engine.md).

## Essentials — the Rust a builder must never get wrong

| Lane | Recipes | Solid | Verified | Code ✔ | Code ✘ |
|---|---|---|---|---|---|
| [Ownership, moves & borrowing](ownership-borrowing.md) | 10 | 7 | 10 | 10 | 0 |
| [Structs, enums & pattern matching](types-patterns.md) | 10 | 10 | 10 | 10 | 0 |
| [Traits & generics — the working set](traits-generics.md) | 10 | 10 | 10 | 10 | 0 |
| [Errors, panics & arithmetic safety](errors-panics.md) | 10 | 9 | 10 | 10 | 0 |
| [Collections, iterators & closures](collections-iterators.md) | 10 | 10 | 10 | 10 | 0 |
| [Cargo, crates, modules & editions](cargo-modules.md) | 10 | 10 | 10 | 7 | 0 |
| [Testing, lints & dev tooling](testing-tooling.md) | 10 | 9 | 10 | 9 | 0 |

## Advanced — the parts of the language that decide design

| Lane | Recipes | Solid | Verified | Code ✔ | Code ✘ |
|---|---|---|---|---|---|
| [Advanced traits & the type system](traits-advanced.md) | 10 | 10 | 10 | 10 | 0 |
| [Memory, smart pointers & layout](memory-layout.md) | 10 | 10 | 10 | 10 | 0 |
| [Unsafe Rust, UB & FFI](unsafe-ffi.md) | 10 | 9 | 10 | 10 | 0 |
| [Concurrency, parallelism & async](concurrency-async.md) | 10 | 9 | 10 | 10 | 0 |
| [Macros, const evaluation & build scripts](macros-const.md) | 10 | 9 | 10 | 10 | 0 |
| [Performance & profiling](performance.md) | 10 | 10 | 10 | 9 | 0 |
| [What changed in Rust 1.80 → 1.98](rust-currency.md) | 10 | 10 | 10 | 9 | 0 |

## si-rpg-engine — how Rust is and will be used in the engine

| Lane | Recipes | Solid | Verified | Code ✔ | Code ✘ |
|---|---|---|---|---|---|
| [Rust → WebAssembly without bindgen](wasm-raw-abi.md) | 10 | 10 | 10 | 10 | 0 |
| [Floating point & cross-platform determinism](float-determinism.md) | 10 | 9 | 10 | 10 | 0 |
| [Rapier 0.35: pipeline, determinism & upgrades](rapier-core.md) | 10 | 10 | 10 | 10 | 0 |
| [Rapier state for restore (T2)](restore-internals.md) | 10 | 10 | 10 | 10 | 0 |
| [Rapier shapes, meshes & the character controller](rapier-shapes-kcc.md) | 10 | 8 | 10 | 10 | 0 |
| [Binary lint, CCD and controller limits (T3/T4)](binary-and-limits.md) | 10 | 10 | 10 | 10 | 0 |
| [Deterministic simulation architecture](sim-architecture.md) | 10 | 9 | 10 | 10 | 0 |
| [Embedding the law in hosts](host-embedding.md) | 10 | 10 | 10 | 7 | 0 |
| [Rust CI, reproducible binaries & supply chain](ci-reproducible-builds.md) | 10 | 9 | 10 | 4 | 0 |

## si-jam-sessions — Rust for a deterministic music law (P1)

| Lane | Recipes | Solid | Verified | Code ✔ | Code ✘ |
|---|---|---|---|---|---|
| [Score ingest inside a wasm law: SMF, MusicXML, ABC](midi-notation-ingest.md) | 11 | 7 | 10 | 11 | 0 |
| [Integer musical time: ticks, tempo maps, samples](integer-time.md) | 15 | 8 | 15 | 14 | 0 |
| [Native audio and MIDI host](host-audio-and-midi.md) | 14 | 10 | 14 | 14 | 0 |
| [Crate licences for a shipped MIT/Apache product](crate-licences.md) | 10 | 6 | 10 | 0 | 0 |

## Flagged — needs care (never silently trusted)

| Tier | Lane | Recipe | Currency | Code | Status | Note |
|---|---|---|---|---|---|---|
| si-jam-sessions | Score ingest inside a wasm law: SMF, MusicXML, ABC | Export SMPTE refusal and error-kind mapping from wasm32 strict cdylib | ✗ wrong | pass | avoid | CORRECTED: FALSE AS WRITTEN: division high byte 0x80 makes Timing::read negate i8::MIN, panicking (primitive.r |
| si-jam-sessions | Score ingest inside a wasm law: SMF, MusicXML, ABC | Parse ABC notation with abc-parser | ✗ wrong | pass | avoid | README/datatypes confirm parsing + Length(f32). engine_note's '(length*base_ticks).round()==...' is impossible |
| si-jam-sessions | Native audio and MIDI host | Handle cpal WASAPI xruns and device changes in error callback | ✗ wrong | pass | avoid | CORRECTED: 'StreamInvalidated when the default device changes' is wrong. MS Learn: AUDCLNT_E_RESOURCES_INVALID |
| si-jam-sessions | Crate licences for a shipped MIT/Apache product | Add per-crate licence exceptions in cargo-deny | ⚠ shaky | none | situational | CORRECTED: how's example used `crate = "assert_no_alloc"`; the real PackageSpec key is `name` (docs' own liter |
| si-jam-sessions | Crate licences for a shipped MIT/Apache product | Clarify ambiguous crate licences with hashed file assertions | ⚠ shaky | none | situational | CORRECTED: how omits the required `name` key (target crate) and lists path/hash as flat keys. Real schema: `na |

## Legend

- **Currency** (retrieval verifier, against Rust 1.98.1 stable / edition 2024 / the pinned crates): ✅ solid > ▸ plausible > ⚠ shaky > ⛔ stale > ✗ wrong.
- **Code**: ✔ every check the recipe carries did what the recipe says under rustc 1.98.1 · ✘ at least one did not · · the claim is not one code can show.
- **✓ verified**: the ledger (`verification/verdicts.json`) holds a confirming external verdict AND no failing code check. Never the author's own flag.
- Pinned: rustc 1.98.1 (48a229cea 2026-09-01), rapier3d-f64 0.35.3 + enhanced-determinism, parry3d-f64 0.30.2. The oracle is `scripts/compile_oracle.py`.
