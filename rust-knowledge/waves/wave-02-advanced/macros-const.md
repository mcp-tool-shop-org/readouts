# macros-const: macros, const evaluation and build scripts (wave 2, advanced)

**Q1. When does a macro or a build script beat a plain function, and what does each cost?** A macro wins only when the output is items or names (consts, exports, a stringify!'d table), a derive only when code must read a type's definition, a build script only when the input lives outside Rust. macro_rules! costs diagnostics; proc macros cost host-built syn crates and uncached expansion; build scripts cost a host compile and run, plus an unpinned program inside the build.

**Q2. What can be computed and asserted at compile time on stable 1.98, including floats?** loop/while/if/match, &mut (1.83), float + - * / (1.82; soft-float, host-independent except NaN bits), literal-message panics (E0080), size_of/offset_of! proofs. Refused: for-loops, iterator and trait calls, allocation, formatted messages, sqrt/sin/powi, arithmetic on const-generic parameters inside types.

1. **Edition 2024 widens `expr` to `const {}` and `_`; `expr_2021` keeps the old set (stable since 1.83).** Rust project 2026 (Edition Guide: Macro Fragment Specifiers, https://doc.rust-lang.org/edition-guide/rust-2024/macro-fragment-specifiers.html). Implication: one macro printed "second rule" under 2021 and "first rule" under 2024; write ABI macros in the edition-2021 solver with `$v:literal`.

2. **The solver already compiles four proc-macro crates on two syn majors.** si-rpg-engine repository 2026 (solver/Cargo.lock at e5fbcb9, https://raw.githubusercontent.com/mcp-tool-shop-org/si-rpg-engine/e5fbcb9/solver/Cargo.lock). Implication: in a measured cold build (30.6 s) the macro chain finished by about 3.8 s, off the critical path (rapier3d-f64 took 15.3 s); macro cost is not where build time goes.

3. **cfg! inside build.rs describes the host.** Rust project 2026 (Cargo Book: Build Scripts, https://doc.rust-lang.org/cargo/reference/build-scripts.html). Implication: measured `cfg!(target_arch = "wasm32")` = false beside `CARGO_CFG_TARGET_ARCH` = wasm32, and a `cargo::rustc-cfg` without `rustc-check-cfg` warns unexpected_cfgs; prefer a macro table over a build.rs for the ABI.

4. **A cfg-gated compile_error! refuses relaxed-simd at compile time.** Rust project 2026 (Reference: Conditional compilation, https://doc.rust-lang.org/stable/reference/conditional-compilation.html). Implication: `-C target-cpu=bleeding-edge` enables relaxed-simd; two lines appended to lib.rs failed that build and left si_solver.wasm byte-identical.

5. **Const float arithmetic is soft-float and host-independent; only NaN bits may differ from run time.** Rust project 2023 (RFC 3514: Float semantics, https://rust-lang.github.io/rfcs/3514-float-semantics.html). Implication: SLIDE_ANGLE is 0x3febecde5da115a9 at compile time, at run time and in V8's wasm; never compare a const NaN (on x86_64 it is +NaN in const, -NaN at run time).

6. **`to_radians()` is not `d * PI / 180.0`.** Rust project 2026 (core f64 source, https://doc.rust-lang.org/stable/src/core/num/f64.rs.html). Implication: 93 of 361 integer degrees differ by one ulp, 46 among them, while JS matches the expression form 361/361; use the expression on both sides of T4's course.

7. **Free `const _` proofs are always evaluated and add no bytes when appended.** Rust project 2026 (Reference: Constant items, https://doc.rust-lang.org/stable/reference/items/constant-items.html). Implication: a 17-slot proof appended to rapier_law.rs kept the digest; build.mjs's hand-typed `i * 17` (four times) and `j * 10` (twice) drift until the glue reads an exported descriptor.

8. **A const-block assert in a generic fn fires only for codegen'd instantiations.** Rust project 2026 (Reference: Block expressions, https://doc.rust-lang.org/stable/reference/expressions/block-expr.html). Implication: E0080 as a bin, clean as a lib; put layout proofs in free consts.

9. **Stable const generics cannot size `[f64; N * STRIDE]`.** Rust project 2026 (Reference: Generic parameters, https://doc.rust-lang.org/stable/reference/items/generics.html). Implication: keep `MAX_BODIES * BODY_STRIDE` as const items.

**Where the evidence is thin.** Timings are one cold build on one 24-thread Windows machine. Host independence of const floats rests on rustc's source and the rustc_apfloat README; I compiled on one host architecture and ran wasm only under node v22. The derive-caching status comes from a September 2025 post and was not re-checked. The byte comparisons are Windows builds without path remapping; the pinned Linux artifact was not rebuilt.
