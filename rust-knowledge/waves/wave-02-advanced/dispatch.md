# Wave 2 — Advanced: the parts of the language that decide design

**Date:** 2026-09-25 · **KB:** `rust-knowledge` · **Tier:** advanced · **Lanes:** 7 · **Recipes:** 70 · **Code checks:** 396 (every one passing under rustc 1.98.1)

## Why this wave exists

Wave 1 covered what any Rust code needs. This wave covers what decides design: the type system, layout and ownership shapes, unsafe code and the C ABI, concurrency, compile-time computation, performance, and what changed between Rust 1.80 and 1.98.

The last topic has its own lane because it is where a model's memory is least trustworthy. Stable on this date is 1.98.1, the exact compiler the engine pins, so every claim here is checked against the release the law actually builds with.

## How it was built

It was built the same way as wave 1:

- one Claude Opus research seat per lane;
- one reasoning-stripped Claude Sonnet verifier per lane;
- `rustc 1.98.1` through `scripts/compile_oracle.py` as the non-model witness for every code claim.

Receipts are in `verification.md`.

## One-line answers per lane

| Lane | The answer a builder needs |
|---|---|
| Advanced traits | Dyn compatibility means no generic methods, associated consts, GATs, `async fn` or RPIT unless fenced by `where Self: Sized`. Upcasting has been stable since 1.86. Zero-sized typestate costs 0 bytes but cannot cross `extern "C"`, so the exports keep their `Option<Loaded>` checks. |
| Memory & layout | Only arrays and `#[repr(C)]` layouts may be assumed by a foreign reader, so keep the flat `[f64; N]` ABI. Option's niche is promised only for std-listed types. A successful realloc kills the old pointer even when the block did not move. |
| Unsafe & FFI | Never create a reference to a `static mut`; export `(&raw mut X).cast()` instead. `#[unsafe(no_mangle)]` compiles in edition 2021 today. `invalid_reference_casting` misses field-write and Vec-of-pointers casts, which is how `solver_clear_warmstart`'s UB compiled silently. |
| Concurrency & async | A `static` must be `Sync`; a `static mut` is exempt, so the solver's statics were never thread-checked. A native host wraps the law in a `Mutex`: Rapier's `PhysicsWorld` is Send + Sync. Rapier now says `parallel` with `enhanced-determinism` is bitwise identical at any pool size. That is the vendor's claim, unmeasured here. |
| Macros & const | Const float arithmetic is soft-float and host-independent, except NaN bits: on x86_64 `0.0/0.0` is +NaN as a const and −NaN at run time. `to_radians()` is not `d*PI/180` for 93 of 361 integer degrees, 46° among them. Free `const _` proofs add no bytes. |
| Performance | Every profile knob moves the pinned bytes, and only `opt-level` moved V8 speed. About 22% of wasm solver time is libm's software `sqrt`, which comes with `enhanced-determinism`. One early bounds guard removes all 30 bounds checks from `step`. |
| Rust currency | Edition 2024, the static-mut deny, and unsafe attributes. Undefined wasm symbols are a link error since 1.96. Wasm feature defaults changed in 1.82 and 1.87. v0 mangling is the default since 1.97, so every toolchain bump moves the digest. Point releases fixed real miscompiles, so pin the latest point release. |

## Findings that bear on the engine (cross-lane)

1. **`solver_clear_warmstart` is undefined behaviour, and the compiler cannot see it.** It writes through pointers cast from `&ContactPair`, laundered through a `Vec` past the deny-by-default lint.
   - Two lanes found this independently (memory-layout, unsafe-ffi), as did wave 1's ownership lane.
   - rapier3d-f64 0.35.3 exposes no `&mut` path: `contact_pairs_mut` fails E0599 and the `contact_graph` field fails E0616.
   - The engine's T2 route decision followed: replay, no writes. See the wave 3 restore-internals lane and `docs/rust-kb-answers.md` on the engine's `main`.
2. **Edition-2024 forms can land under 2021 now.**
   - All ten exports can take `#[unsafe(no_mangle)]` today.
   - The seven `static mut` reference sites have an exact short-lived `&raw mut` rewrite that compiles clean in both editions and gave byte-identical wasm. `cargo fix --edition` changes only the attributes; the static-mut sites need hand edits.
   - (unsafe-ffi, rust-currency; now S1 pin 8)
3. **A native Godot or Unreal build must serialise every call.** The solver's `static mut` statics were never checked for `Sync`. Wrap the law in `static LAW: Mutex<Option<Loaded>>`, and return 0 when `try_lock` fails. (concurrency-async)
4. **Rapier's event handler and hooks must be `Sync` even with `parallel` off.** A `RefCell` counter fails E0277, so hold state in atomics. Rapier's `Vector` is glam's `DVec3`, a foreign type, so `From<[f64; 17]> for Vector` fails E0117; convert through a local `BodyRecord`. (traits-advanced)
5. **Removal history changes Rapier handles as well as insertion order.** Rapier's arena bumps one generation counter per set on every removal. (memory-layout; now S1 pin 9)
6. **Digest sensitivity:**
   - any profile edit moves it, even an inert one;
   - a line shift in `rapier_law.rs` moves it, through panic locations, by 22 bytes measured;
   - v0 mangling means every toolchain bump moves it.

   The golden, not the digest, proves the law, so re-pin the digest in the same change. (performance, macros-const, rust-currency)
7. **Slope angles for T4.** Build slopes as `d*PI/180.0` on both sides; JS matches it on all 361 degrees, while `to_radians()` differs at 46°. (macros-const; now in T4)
8. **The layout constants in `build.mjs` drift silently.** It hand-codes the strides: `i * 17` four times and `j * 10` twice. A free `const _` ABI proof in Rust adds no bytes; the JS side should read an exported descriptor. (macros-const, memory-layout)

Every finding above went to the si-rpg-engine coordinator as it landed.

## Where the evidence is thin

- Rapier's bitwise `parallel` claim is the vendor's word.
- The Stacked Borrows vs Tree Borrows reading of the solver's heap-only writes is analysis; Miri is not installed here.
- The timings come from one machine and one scene, with about ±10% noise.
- The byte comparisons are Windows builds without the Linux remaps.
- The relaxed-madd fused result (−8.67e-19) is a one-host node measurement, not a check.

## What locks, what stays advisory

**Load-bearing:** all 70 recipes. They carry 66 confirmed and 4 corrected verdicts, and no check fails.

**Advisory:**

- the 3 `plausible` recipes;
- the performance numbers, which are scoped to one host and one scene;
- the vendor's `parallel` claim.
