# rust-currency: Rust 1.80 → 1.98 and edition 2024

**Q1. What would a model trained on older Rust get wrong?** It would treat edition 2024 as optional, though it changes unsafe attributes, `static mut` references and drop order. It would miss that wasm links fail on undefined symbols (1.96), `extern "C"` on wasm uses the standard C ABI (1.89), the default wasm feature set grew twice (1.82, 1.87), `algebraic_*` float methods are stable (1.98), sorts panic on non-total orders (1.81), and several lints are now deny.

**Q2. What would moving si-solver to 2024 change?** Measured on a copy with 1.98.1: `cargo fix --edition` rewrote only the 10 `#[no_mangle]` attributes. The 7 `static_mut_refs` sites need hand rewrites. With line positions preserved, the wasm stayed byte-identical (sha256 b21c7f15…, Windows host).

## Findings not covered by the ten recipes

1. **v0 symbol mangling became the default in 1.97.** Rust Project 2026 (Announcing Rust 1.97.0, https://blog.rust-lang.org/2026/07/09/Rust-1.97.0/). The solver copy's `name` section holds 1,180 `_R…` symbols and no `_ZN…` symbols. Its `producers` section records `rustc 1.98.1 (48a229cea 2026-09-01)`. Implication: every toolchain bump moves fixtures/solver.sha256 even when the source is unchanged. Gate bumps on the golden hash, and re-pin the digest in the same change.

2. **Point releases in this window fixed miscompilations.** Rust Project 2026 (Announcing Rust 1.97.1, https://blog.rust-lang.org/2026/07/16/Rust-1.97.1/). 1.97.1 fixed an LLVM miscompile present since 1.87. 1.98.1 fixed vtables generated with a null function pointer, and 1.80.1 fixed float comparisons broken by jump threading. Implication: pin the latest point release, as the solver does.

3. **Paths embedded in binaries changed shape.** Rust Project 2026 (Rust release notes, https://doc.rust-lang.org/stable/releases.html). Std panic paths gained a `library/` prefix (1.85). Filename handling now respects the relativeness of `--remap-path-prefix` (1.94), and `--remap-path-scope` is stable (1.95). Implication: re-check build.mjs's remaps on each bump. Whether `--remap-path-scope` fixes the Windows-backslash difference is untested.

4. **LLVM moved four times: 19 (1.82), 20 (1.87), 21 (1.91), 22 (1.95).** Rust Project 2026 (Rust release notes, same URL). Implication: codegen can change at each of these. The three-engine golden run, not the digest, proves the law.

5. **Panic behaviour at `extern "C"` changed.** Rust Project 2024 (Announcing Rust 1.81.0, https://blog.rust-lang.org/2024/09/05/Rust-1.81.0/). An uncaught unwind out of `extern "C"` now aborts; `"C-unwind"` is the ABI for unwinding. Since 1.92, unwind tables are emitted even with panic=abort. Implication: the Godot and Unreal host builds must choose the ABI on purpose. The wasm build already aborts.

6. **The solver's dependencies are already edition 2024.** docs.rs 2026 (rapier3d-f64 0.35.3 Cargo.toml, https://docs.rs/crate/rapier3d-f64/0.35.3/source/Cargo.toml). rapier3d-f64 declares edition 2024 and rust-version 1.86; nalgebra 0.35.0 declares 2024 and 1.89.0. Implication: editions are per crate, so the solver can migrate whenever it chooses. The toolchain floor comes from its dependencies.

7. **JSON target specs have needed nightly since 1.95.** Rust Project 2026 (Announcing Rust 1.95.0, https://blog.rust-lang.org/2026/04/16/Rust-1.95.0/). Implication: a custom "deterministic wasm" target file is not a stable option. Stay on wasm32-unknown-unknown or wasm32v1-none.

8. **Platform tiers moved.** Rust Project 2025 (Announcing Rust 1.91.0, https://blog.rust-lang.org/2025/10/30/Rust-1.91.0/). aarch64-pc-windows-msvc is now Tier 1. In 1.90, x86_64-apple-darwin dropped to Tier 2 and LLD became the default linker on x86_64 Linux. Implication: native Intel-Mac host builds lose Tier 1 testing; the wasm artifact links with rust-lld regardless.

## Where the evidence is thin

- Byte identity was measured on the Windows host only; the Linux pin was not rebuilt.
- The fused `f64x2.relaxed_madd` result comes from one x86 host under node 22.
- The Cargo docs I retrieved do not say what resolver 3 does when `rust-version` is unset.
- WebFetch returned inconsistent text for the std slice and lint-listing pages, so those claims rest on the compiler and release notes.
