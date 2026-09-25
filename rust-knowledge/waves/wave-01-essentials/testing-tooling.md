# testing-tooling — wave 1 (essentials)

**How does a cdylib-only crate get native Rust tests, and how do those tests run for wasm?** Append `#[cfg(test)]` modules; `cargo test --lib` runs them natively, crate-type unchanged. tests/ and doc tests need an `rlib`, which moved the solver's wasm bytes. On wasm32, libtest prints nothing and skips `#[should_panic]`, so leave the wasm to the JS harness.

**Which lints and tools catch real defects in numeric, unsafe code?** rustc catches only compile-time-evaluable overflow and `== NAN`. Clippy's float_cmp, cast and undocumented_unsafe_blocks lints work once installed and named. proptest found a canon_quat edge, cargo-mutants proves tests fail, and Miri (nightly) checks native tests.

1. **A solver/ copy at e5fbcb9 ran 5 appended unit tests natively; its release wasm stayed byte-identical (c8782b06…). Moving the module to the top of rapier_law.rs changed the digest: 21 data-section line numbers shifted by 24.** Rust Project 2026 (The Rust Programming Language 11.3, https://doc.rust-lang.org/book/ch11-03-test-organization.html). Implication: append tests, and treat solver/src line layout as part of the pin.

2. **Adding `rlib` changed the solver's wasm SHA-256 (→ 8191738e…; code +28 bytes). Without it, `cargo test` skips doc tests silently and tests/ fails with E0433.** Rust Project 2026 (The Cargo Book: cargo test, https://doc.rust-lang.org/cargo/commands/cargo-test.html). Implication: keep `["cdylib"]`; the private helpers fail doc tests with E0603 anyway. Measured on Windows only; mechanism not isolated.

3. **`cargo test --release` uses the release profile: with `overflow-checks = false` an overflow test that passes in debug fails. `panic = "abort"` is ignored for tests.** Rust Project 2026 (The Cargo Book: Profiles, https://doc.rust-lang.org/cargo/reference/profiles.html). Implication: run both; the release run tests the shipped wrapping.

4. **libtest at tag 1.98.1 marks `#[should_panic]` tests ignored on non-emscripten wasm. A wasm32-unknown-unknown runner sees only `main`'s return or an `unreachable` trap.** Rust Project 2026 (library/test/src/lib.rs, https://github.com/rust-lang/rust/blob/1.98.1/library/test/src/lib.rs). Implication: Rust tests stay native, wasm evidence stays in the three-engine JS harness. WASI route unmeasured.

5. **A proptest over `f64::ANY` broke a verbatim copy of canon_quat in 6 of 6 runs: ±inf gives a NaN component, and an overflowing square (≈1.34e154 and up) gives `Some((0,0,0,0))`. The wasm build agrees.** proptest-rs 2026 (proptest 1.11.0 num::f64, https://docs.rs/proptest/1.11.0/proptest/num/f64/index.html). Implication: add the property and commit proptest-regressions/; T3's non-finite refusal misses 1e200.

6. **`assert_eq!(canon(-0.0), 0.0)` misses the `==`→`!=` mutant, and `to_bits` catches it. A `0.0` body passes the -0.0 bit test but fails `canon(1.5)`.** cargo-mutants 2026 (Generated mutants, https://mutants.rs/mutants.html). Implication: PHASE-2's go-red rule means `cargo mutants` with nothing missed; assert on bits. Mutants were hand-applied.

7. **rustc enforces nothing from `#![deny(clippy::…)]`: `1088 as u8` and `0.1 + 0.2 == 0.3` compile silently. float_cmp exempts zero, so it never flags canon's `x == 0.0`.** Rust Project 2026 (Reference: Diagnostic attributes, https://doc.rust-lang.org/reference/attributes/diagnostics.html). Implication: add clippy and rustfmt to rust-toolchain.toml components, and enable the lints by name.

8. **At equal priority Cargo passed `--allow=unused_variables --deny=unused`, so the group won. Setting `priority = -1` fixes it.** Rust Project 2026 (The Cargo Book: [lints], https://doc.rust-lang.org/cargo/reference/manifest.html). Implication: put groups at -1. A warnings gate first hits 7 static_mut_refs warnings.

9. **An `#[expect]` over code gated by `cfg(target_arch)` is fulfilled on the host and unfulfilled on wasm32.** Rust Project 2024 (Announcing Rust 1.81.0, https://blog.rust-lang.org/2024/09/05/Rust-1.81.0/). Implication: scope it with `cfg_attr`.

10. **Tests in one binary share its statics, and nextest runs one process per test. Miri is nightly-only; 1.98.1 reports the component unavailable.** nextest-rs 2026 (How nextest works, https://nexte.st/docs/design/how-it-works/). Implication: isolate tests that call step or solver_load; Miri (nightly) can check their static mut accesses at run time.

Measured on 1.98.1. Thin evidence: Clippy, nextest, cargo-mutants, insta, cargo-deny, cargo-audit and Miri are not installed here; their behaviour comes from documentation.
