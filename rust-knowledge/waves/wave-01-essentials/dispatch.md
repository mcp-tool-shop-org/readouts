# Wave 1 — Essentials: the Rust a builder must never get wrong

**Date:** 2026-09-25 · **KB:** `rust-knowledge` · **Tier:** essentials · **Lanes:** 7 · **Recipes:** 70 · **Code checks:** 310 (every one passing under rustc 1.98.1)

## Why this wave exists

si-rpg-engine's physics law is Rust. The crate is `solver/`: `rapier3d-f64` 0.35.3 with `enhanced-determinism`, built with edition 2021 and toolchain 1.98.1, and shipped as one pinned `wasm32-unknown-unknown` binary. Everyone who touches the law needs the core language right: coordinators, builders and reviewers from any model family. This wave is that core. Each lane is written for an engineer who knows another language well.

One constraint shaped every answer: the law is hashed. A fact that is harmless in ordinary Rust, such as HashMap iteration order, a tie in `sort_unstable`, the sign of an empty float sum, or `1u64 << 64`, becomes a question about whether two machines agree. Each lane was asked where its topic touches the engine, and to name the file and function.

## How it was built

- **Research.** One Claude Opus seat per lane, briefed by `briefs/LANE-BRIEF.md` and its lane object in `briefs/lanes.json`. Each seat had to open every source it cites, and to ground every code claim in a check that the pinned compiler runs.
- **Retrieval verification.** A reasoning-stripped Claude Sonnet verifier per lane (`briefs/VERIFIER-BRIEF.md`). It saw only the citations and checks, never the research packet.
- **The compiler.** `scripts/compile_oracle.py` runs every check under `rustc 1.98.1`, linking the engine's own `rapier3d-f64` build where a check needs it. It is not a model.
- **What `verified` means.** A recipe is verified only when the verifier confirms it and none of its checks fails. Receipts are in `verification.md`.

## One-line answers per lane

| Lane | The answer a builder needs |
|---|---|
| Ownership & borrowing | Most borrow errors are lifetime computation, not moves. Fix aliasing by ending the first borrow earlier, never by cloning by reflex. Only *implicit* borrows are two-phase: `Vec::push(&mut v, v.len())` is E0502. |
| Types & patterns | Decode ABI numbers once, at the export edge, into exhaustive enums. `as` truncates and saturates silently, and `SolverMode::try_from(x as u32)` accepts 1.5 and NaN. Require an exact round trip first. |
| Traits & generics | On f64 fields only PartialEq and PartialOrd derive. A hand-written `Eq` on floats compiles and lies. Key floats with `to_bits` and order them with `total_cmp`; the two agree on every bit pattern (1,000,196 pairs checked). |
| Errors & panics | `Result` is `#[must_use]`; `bool`, `Option<()>` and `u32` are not, and dropping them compiles silently. Under `panic = "abort"` a panic is a wasm trap, and the instance stays callable with half-written statics. Re-instantiate after any trap. |
| Collections & iterators | Only `sort`, `sort_by` and `sort_by_key` promise an order for ties. `sort_unstable` lost its "deterministic" wording in 1.81, and on 1.98.1 it reorders ties from 21 elements up. An empty float `sum()` is −0.0. |
| Cargo & editions | Any `RUSTFLAGS`, even an empty one, replaces `.cargo/config.toml`'s rustflags. `rust-toolchain.toml` and the config are found from the working directory. `"0.35.3"` is a caret range, and only `--locked` holds it. |
| Testing & tooling | A cdylib-only crate runs in-crate `#[cfg(test)]` modules natively. Tests appended at the end of a file leave the wasm byte-identical; tests at the top move the digest. libtest skips `#[should_panic]` on wasm. |

## Findings that bear on the engine (cross-lane)

1. **Body slot 16 (the mode) is read two ways, and neither reader refuses an unknown value.** `lib.rs` `step()` tests `!= 0.0`, so NaN counts as driven. `rapier_law.rs` `signature()` tests `== 1.0 || == 2.0` and then `== 3.0`, so 1.5, 4.0 and NaN count as dynamic. The fix is to decode once, at the export edge, and refuse. *(types-patterns)*
2. **`MAX_BODIES = 64` is coupled to the u64 masks.** With `overflow-checks = false`, `1u64 << 64 == 1` on host and wasm, so a 65th body would alias bit 0. The fix is `const _: () = assert!(MAX_BODIES <= 64);`. *(types-patterns, errors-panics: two lanes, measured independently)*
3. **Refusals can be dropped silently.** `ensure`, `integrate`, `write_body` and `rebuild_snapshot` return bare `bool`s. Return `Result<(), Refusal>` or add `#[must_use]`, and add `#![deny(unused_must_use)]` so a dropped refusal fails the build. The advisor measured the last point with the oracle. *(errors-panics)*
4. **`rebuild_snapshot`'s "continue on a failed `canon_quat`" was already fixed at `6a33297`.** The brief's recollection was stale. One `.unwrap()` remains, in `integrate`. *(errors-panics)*
5. **`signature()` hashes raw collider bits while the snapshot canonicalises −0.0.** A −0.0 coordinate would make an identical world look different. This comes from code reading; the test that settles it is S1 pin 4. *(traits-generics, collections-iterators)*
6. **Build hygiene in `build.mjs`:**
   - add `--locked`;
   - pass flags as `CARGO_ENCODED_RUSTFLAGS`, which gives the same digest, survives paths with spaces, and cannot be overridden by an inherited value;
   - never run cargo from outside `solver/`, which silently switches to the stable toolchain and drops the relaxed-SIMD config pin;
   - adding `rlib` to the crate-type changes the wasm bytes (+28 bytes, measured by two lanes independently). *(cargo-modules, testing-tooling)*
7. **`canon_quat` fails a property test over the full f64 range.** An infinite component returns `Some` holding a NaN. A component from about 1.34e154 up, where the square overflows, returns `Some((0,0,0,0))`. *(testing-tooling; now S1 pin 11)*
8. **The edition-2024 move is cheap.** `cargo fix --edition` touches only the attributes, and no `rust_2024_incompatible_pat` sites exist. Patterns will not block it. *(types-patterns, cargo-modules)*

Every finding above went to the si-rpg-engine coordinator as it landed. Items 1–7 are pins in `docs/dispatch-s1-soundness.md` on the engine's `main` (PRs #45 and #46).

## Where the evidence is thin

- The frequency of borrow errors rests on one 2022 Stack Overflow study.
- Several behaviours are implementation measurements of 1.98.1, not documented guarantees, and each recipe says so: the 20/21 tie boundary, `1u64 << 64 == 1`, float-literal patterns matching −0.0.
- Two errors-panics checks assert this Windows host's abort status, 0xC0000409; on Unix it would be SIGABRT.
- Clippy, rustfmt, nextest, cargo-mutants, insta, cargo-deny and Miri are not installed on this rig. Claims about them rest on their documentation.

## What locks, what stays advisory

**Load-bearing:** every recipe in this wave. All 70 carry a confirming verdict (65 confirmed, 5 corrected), and none has a failing check.

**Advisory:** the five `plausible` recipes, whose limits are named in their verifier notes, and any claim marked as measured on one host.
