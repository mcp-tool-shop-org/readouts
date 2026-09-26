# Testing, lints & dev tooling — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](testing-tooling.md) · [catalog index](README.md)

## Add what rustc cannot check: Miri on native tests (nightly only), cargo-deny and cargo-audit on dependencies
**Miri interprets cargo miri test and reports out-of-bounds access, use-after-free, uninitialised reads, misalignment, invalid values and data races, but it is a nightly component (1.98.1 offers none) with no FFI; cargo-deny lints the dependency graph (advisories, bans, licenses, sources) from deny.toml, and cargo-audit checks dependencies against the RustSec Advisory Database.**

*Check 1: #[cfg_attr(miri, ignore)] is inert outside Miri: the test runs and cfg!(miri) is false* · `runs` · edition 2021 · host · test · output has “test result: ok. 1 passed; 0 failed; 0 ignored” · exit code 0 · **✔ oracle pass**
```rust
#[test]
#[cfg_attr(miri, ignore = "too slow under the interpreter")]
fn heavy_world_step() {
    assert!(!cfg!(miri));
}
```

## Give lint groups priority = -1 in Cargo's [lints] table; add clippy and rustfmt to the pinned toolchain file
**Cargo turns [lints] into --allow/--warn/--deny flags ordered by priority, not by position in the file; at equal priority a group can come last and override a member lint (measured), which clippy::lint_groups_priority flags. The pinned 1.98.1 minimal toolchain has neither cargo clippy nor cargo fmt.**

*Check 1: group flag last wins: -A unused_variables then -D unused denies the unused variable* · `compile_fail` · edition 2021 · host · lib · stderr has “unused variable: `scratch`” · stderr has “implied by `-D unused`” · **✔ oracle pass**
```rust
pub fn step(dt: f64) -> f64 {
    let scratch = dt * 2.0;
    dt
}
```

*Check 2: member flag last wins: -D unused then -A unused_variables compiles with no warning* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
pub fn step(dt: f64) -> f64 {
    let scratch = dt * 2.0;
    dt
}
```

## Keep wasm evidence in the JS harness: wasm32-unknown-unknown libtest prints nothing and skips should_panic
**Cargo has no runner for wasm32-unknown-unknown: it builds the libtest harness as a .wasm and fails to execute it. Given CARGO_TARGET_<TRIPLE>_RUNNER the harness runs, but println! does nothing, a failure is only an unreachable trap, and libtest marks every #[should_panic] test ignored on non-emscripten wasm.**

*Check 1: wasm32 libtest harness: a should_panic test that cannot pass is skipped, main returns 0* · `runs` · edition 2021 · wasm32-unknown-unknown · test · exports main · imports nothing · node calls main(0, 0) · **✔ oracle pass**
```rust
#[test]
#[should_panic(expected = "NaN")]
fn claims_to_panic_but_never_does() {}
```
Expected output: `0`

*Check 2: same test on the host harness: it runs and fails* · `runs` · edition 2021 · host · test · output has “did not panic as expected” · output has “test result: FAILED. 0 passed; 1 failed” · exit code 101 · **✔ oracle pass**
```rust
#[test]
#[should_panic(expected = "NaN")]
fn claims_to_panic_but_never_does() {}
```

## Property-test the solver's float helpers with proptest over prop::num::f64::ANY, not only hand-picked values
**A proptest over f64::ANY on a verbatim copy of canon_quat failed in 6 of 6 runs: an infinite component returns Some((NaN, 0.0, 0.0, 0.0)), and a finite one whose square overflows (sqrt(f64::MAX) = 1.3407807929942596e154; measured at 1.4e154 and 1e200) returns Some((0.0, 0.0, 0.0, 0.0)), though its doc comment says unit quaternion. proptest shrinks each failure and replays saved seeds.**

*Check 1: canon_quat property holds on bounded inputs incl. +-0: None iff all zero, else unit, w >= +0, no -0* · `runs` · edition 2021 · host · test · deps: proptest · output has “test result: ok. 1 passed; 0 failed” · exit code 0 · **✔ oracle pass**
```rust
use proptest::prelude::*;

fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

/// Verbatim copy of si-rpg-engine solver/src/rapier_law.rs canon_quat (e5fbcb9).
fn canon_quat(x: f64, y: f64, z: f64, w: f64) -> Option<(f64, f64, f64, f64)> {
    if x.is_nan() || y.is_nan() || z.is_nan() || w.is_nan() {
        return None;
    }
    let n = (x * x + y * y + z * z + w * w).sqrt();
    if !(n > 0.0) {
        return None;
    }
    let mut x = canon(x / n);
    let mut y = canon(y / n);
    let mut z = canon(z / n);
    let mut w = canon(w / n);
    if w.is_sign_negative() {
        x = canon(-x);
        y = canon(-y);
        z = canon(-z);
        w = canon(-w);
    }
    Some((x, y, z, w))
}

fn component() -> impl Strategy<Value = f64> {
    prop_oneof![Just(0.0), Just(-0.0), -1.0e6..1.0e6f64]
}

proptest! {
    #![proptest_config(ProptestConfig { failure_persistence: None, ..ProptestConfig::default() })]

    #[test]
    fn unit_non_negative_w_no_negative_zero(x in component(), y in component(),
                                            z in component(), w in component()) {
        match canon_quat(x, y, z, w) {
            None => prop_assert!(x == 0.0 && y == 0.0 && z == 0.0 && w == 0.0),
            Some((a, b, c, d)) => {
                let n2 = a * a + b * b + c * c + d * d;
                prop_assert!((n2 - 1.0).abs() <= 1e-12, "n2 = {}", n2);
                prop_assert!(!d.is_sign_negative());
                for v in [a, b, c, d] {
                    prop_assert_ne!(v.to_bits(), (-0.0f64).to_bits());
                }
            }
        }
    }
}
```

*Check 2: proptest shrinks a failing u32 from 0..1000 to the boundary: minimal failing input n = 65* · `runs` · edition 2021 · host · test · deps: proptest · output has “minimal failing input: n = 65” · exit code 101 · **✔ oracle pass**
```rust
use proptest::prelude::*;

const MAX_BODIES: u32 = 64;

fn admit(n_bodies: u32) -> bool {
    n_bodies <= MAX_BODIES
}

proptest! {
    // Persistence off: inside the oracle's temp dir there is no crate layout to write beside.
    #![proptest_config(ProptestConfig { failure_persistence: None, ..ProptestConfig::default() })]

    #[test]
    fn every_count_is_admitted(n in 0u32..1000) {
        prop_assert!(admit(n), "refused n = {}", n);
    }
}
```

*Check 3: over f64::ANY (fixed seed) the 'Some means unit' property fails for canon_quat and is shrunk* · `runs` · edition 2021 · host · test · deps: proptest · output has “not unit: n2 = NaN” · output has “minimal failing input: x = 0.0, y = 0.0, z = -inf, w = 0.0” · exit code 101 · **✔ oracle pass**
```rust
use proptest::prelude::*;
use proptest::test_runner::RngSeed;

fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

/// Verbatim copy of si-rpg-engine solver/src/rapier_law.rs canon_quat (e5fbcb9).
fn canon_quat(x: f64, y: f64, z: f64, w: f64) -> Option<(f64, f64, f64, f64)> {
    if x.is_nan() || y.is_nan() || z.is_nan() || w.is_nan() {
        return None;
    }
    let n = (x * x + y * y + z * z + w * w).sqrt();
    if !(n > 0.0) {
        return None;
    }
    let mut x = canon(x / n);
    let mut y = canon(y / n);
    let mut z = canon(z / n);
    let mut w = canon(w / n);
    if w.is_sign_negative() {
        x = canon(-x);
        y = canon(-y);
        z = canon(-z);
        w = canon(-w);
    }
    Some((x, y, z, w))
}

proptest! {
    #![proptest_config(ProptestConfig {
        failure_persistence: None,
        rng_seed: RngSeed::Fixed(20260925),
        ..ProptestConfig::default()
    })]

    #[test]
    fn some_means_unit(x in prop::num::f64::ANY, y in prop::num::f64::ANY,
                       z in prop::num::f64::ANY, w in prop::num::f64::ANY) {
        if let Some((a, b, c, d)) = canon_quat(x, y, z, w) {
            let n2 = a * a + b * b + c * c + d * d;
            prop_assert!((n2 - 1.0).abs() <= 1e-12, "not unit: n2 = {}", n2);
        }
    }
}
```

*Check 4: canon_quat edges: +inf gives a NaN component; 1e200 and 1.4e154 give a zero quaternion* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

/// Verbatim copy of si-rpg-engine solver/src/rapier_law.rs canon_quat (e5fbcb9).
fn canon_quat(x: f64, y: f64, z: f64, w: f64) -> Option<(f64, f64, f64, f64)> {
    if x.is_nan() || y.is_nan() || z.is_nan() || w.is_nan() {
        return None;
    }
    let n = (x * x + y * y + z * z + w * w).sqrt();
    if !(n > 0.0) {
        return None;
    }
    let mut x = canon(x / n);
    let mut y = canon(y / n);
    let mut z = canon(z / n);
    let mut w = canon(w / n);
    if w.is_sign_negative() {
        x = canon(-x);
        y = canon(-y);
        z = canon(-z);
        w = canon(-w);
    }
    Some((x, y, z, w))
}

fn main() {
    println!("{:?}", canon_quat(f64::INFINITY, 0.0, 0.0, 1.0));
    println!("{:?}", canon_quat(1e200, 0.0, 0.0, 1.0));
    println!("{:?}", canon_quat(1.4e154, 0.0, 0.0, 1.0));
    println!("{:e}", f64::MAX.sqrt());
}
```
Expected output: `Some((NaN, 0.0, 0.0, 0.0)) Some((0.0, 0.0, 0.0, 0.0)) Some((0.0, 0.0, 0.0, 0.0)) 1.3407807929942596e154`

*Check 5: wasm32 build: canon_quat(1e200, 0, 0, 1) has squared norm 0, not 1* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls norm2_after_huge() · **✔ oracle pass**
```rust
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

/// Verbatim copy of si-rpg-engine solver/src/rapier_law.rs canon_quat (e5fbcb9).
fn canon_quat(x: f64, y: f64, z: f64, w: f64) -> Option<(f64, f64, f64, f64)> {
    if x.is_nan() || y.is_nan() || z.is_nan() || w.is_nan() {
        return None;
    }
    let n = (x * x + y * y + z * z + w * w).sqrt();
    if !(n > 0.0) {
        return None;
    }
    let mut x = canon(x / n);
    let mut y = canon(y / n);
    let mut z = canon(z / n);
    let mut w = canon(w / n);
    if w.is_sign_negative() {
        x = canon(-x);
        y = canon(-y);
        z = canon(-z);
        w = canon(-w);
    }
    Some((x, y, z, w))
}

/// Squared norm of canon_quat(1e200, 0, 0, 1) in the wasm build: 1.0 if unit.
#[no_mangle]
pub extern "C" fn norm2_after_huge() -> f64 {
    match canon_quat(1e200, 0.0, 0.0, 1.0) {
        Some((a, b, c, d)) => a * a + b * b + c * c + d * d,
        None => -1.0,
    }
}
```
Expected output: `0`

*Check 6: wasm32 build: canon_quat(+inf, 0, 0, 1) returns Some with a NaN x component* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls x_after_inf() · **✔ oracle pass**
```rust
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

/// Verbatim copy of si-rpg-engine solver/src/rapier_law.rs canon_quat (e5fbcb9).
fn canon_quat(x: f64, y: f64, z: f64, w: f64) -> Option<(f64, f64, f64, f64)> {
    if x.is_nan() || y.is_nan() || z.is_nan() || w.is_nan() {
        return None;
    }
    let n = (x * x + y * y + z * z + w * w).sqrt();
    if !(n > 0.0) {
        return None;
    }
    let mut x = canon(x / n);
    let mut y = canon(y / n);
    let mut z = canon(z / n);
    let mut w = canon(w / n);
    if w.is_sign_negative() {
        x = canon(-x);
        y = canon(-y);
        z = canon(-z);
        w = canon(-w);
    }
    Some((x, y, z, w))
}

/// x component of canon_quat(+inf, 0, 0, 1) in the wasm build; -1.0 means None.
#[no_mangle]
pub extern "C" fn x_after_inf() -> f64 {
    match canon_quat(f64::INFINITY, 0.0, 0.0, 1.0) {
        Some((x, _, _, _)) => x,
        None => -1.0,
    }
}
```
Expected output: `NaN`

*Check 7: js_min is not NaN-symmetric: js_min(1, NaN) = 1, js_min(NaN, 1) = NaN* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
/// Verbatim copy of si-rpg-engine solver/src/lib.rs js_min (e5fbcb9).
fn js_min(a: f64, b: f64) -> f64 {
    if b < a || (a == 0.0 && b == 0.0 && b.is_sign_negative() && !a.is_sign_negative()) {
        b
    } else {
        a
    }
}

fn main() {
    println!("{} {}", js_min(1.0, f64::NAN), js_min(f64::NAN, 1.0));
}
```
Expected output: `1 NaN`

## Prove each Rust harness can go red: cargo-mutants on unit tests, insta goldens that CI cannot auto-accept
**cargo-mutants copies the tree, runs cargo test per mutant, replaces an f64 body with 0.0, 1.0 or -1.0 and swaps == with !=; a mutant no test kills is 'missed' (exit 2). For the solver's canon, assert_eq!(canon(-0.0), 0.0) misses the ==-to-!= mutant because -0.0 == 0.0, and a to_bits assertion catches it. An insta golden fails on a mismatch by default; cargo insta test and INSTA_FORCE_PASS=1 force it to pass.**

*Check 1: original canon: the to_bits test and the nonzero test both pass* · `runs` · edition 2021 · host · test · output has “test result: ok. 2 passed; 0 failed” · exit code 0 · **✔ oracle pass**
```rust
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

#[test]
fn canon_maps_negative_zero_to_positive_zero() {
    assert_eq!(canon(-0.0).to_bits(), 0.0f64.to_bits());
}

#[test]
fn canon_keeps_nonzero() {
    assert_eq!(canon(1.5).to_bits(), 1.5f64.to_bits());
}
```

*Check 2: mutant == to !=: the natural == test still passes, so the mutant is missed* · `runs` · edition 2021 · host · test · output has “test result: ok. 1 passed; 0 failed” · exit code 0 · **✔ oracle pass**
```rust
fn canon(x: f64) -> f64 {
    if x != 0.0 { 0.0 } else { x } // mutant: == replaced with !=
}

#[test]
fn canon_zero_compares_equal() {
    assert_eq!(canon(-0.0), 0.0);
}
```

*Check 3: mutant == to !=: the to_bits test fails, so the mutant is caught* · `runs` · edition 2021 · host · test · output has “test result: FAILED. 0 passed; 1 failed” · exit code 101 · **✔ oracle pass**
```rust
fn canon(x: f64) -> f64 {
    if x != 0.0 { 0.0 } else { x } // mutant: == replaced with !=
}

#[test]
fn canon_maps_negative_zero_to_positive_zero() {
    assert_eq!(canon(-0.0).to_bits(), 0.0f64.to_bits());
}
```

*Check 4: mutant body -> 0.0: the -0.0 bit test passes, only the nonzero test catches it* · `runs` · edition 2021 · host · test · output has “test result: FAILED. 1 passed; 1 failed” · exit code 101 · **✔ oracle pass**
```rust
fn canon(_x: f64) -> f64 {
    0.0 // mutant: body replaced with 0.0
}

#[test]
fn canon_maps_negative_zero_to_positive_zero() {
    assert_eq!(canon(-0.0).to_bits(), 0.0f64.to_bits());
}

#[test]
fn canon_keeps_nonzero() {
    assert_eq!(canon(1.5).to_bits(), 1.5f64.to_bits());
}
```

## Rely on rustc for constant overflow and NaN ==, and on Clippy's pedantic float_cmp and cast lints for the rest
**rustc denies overflow it can evaluate at compile time (arithmetic_overflow, overflowing_literals, unconditional_panic) and warns on == f64::NAN; it accepts `1088 as u8` and `0.1 + 0.2 == 0.3` without a word, even under #![deny(clippy::...)]. Clippy's float_cmp and cast_possible_truncation are the lints written for those, and they run only under cargo clippy.**

*Check 1: deny-by-default: constant overflow, out-of-bounds constant index, out-of-range literal all fail* · `compile_fail` · edition 2021 · host · bin · lints: arithmetic_overflow, unconditional_panic, overflowing_literals · **✔ oracle pass**
```rust
const MAX_BODIES: usize = 64;
const BODY_STRIDE: usize = 17;

fn main() {
    let bytes: u8 = 255 + 1;
    let slot = [0.0f64; MAX_BODIES * BODY_STRIDE][MAX_BODIES * BODY_STRIDE];
    let lit: u8 = 1088;
    println!("{bytes} {slot} {lit}");
}
```

*Check 2: rustc accepts deny(clippy::...) yet enforces nothing: 1088 as u8 and 0.1 + 0.2 == 0.3 run silently* · `runs` · edition 2021 · host · bin · no warnings · **✔ oracle pass**
```rust
#![deny(clippy::float_cmp, clippy::cast_possible_truncation)]

const MAX_BODIES: usize = 64;
const BODY_STRIDE: usize = 17;

fn main() {
    let slots = (MAX_BODIES * BODY_STRIDE) as u8;
    let x = 0.1f64 + 0.2;
    println!("{} {}", slots, x == 0.3);
}
```
Expected output: `64 false`

*Check 3: comparing with f64::NAN is a warn-by-default rustc lint and is always false* · `runs` · edition 2021 · host · bin · lints: invalid_nan_comparisons · **✔ oracle pass**
```rust
fn main() {
    let y = std::hint::black_box(f64::NAN);
    println!("{}", y == f64::NAN);
}
```
Expected output: `false`

## Run cargo test and cargo test --release: the release run wraps integer overflow that the debug run panics on
**cargo test uses the test profile (inherits dev, overflow checks on); --release is --profile=release, so a crate whose release profile sets overflow-checks = false runs its tests with wrapping arithmetic, the shipped behaviour. panic = "abort" is ignored for test builds, and rustc itself refuses --test with -C panic=abort.**

*Check 1: default rustc --test (opt-level 0): u32 overflow panics, so the should_panic test passes* · `runs` · edition 2021 · host · test · output has “test result: ok. 1 passed; 0 failed” · exit code 0 · **✔ oracle pass**
```rust
const BODY_STRIDE: u32 = 17;

fn slot(i: u32) -> u32 {
    i * BODY_STRIDE
}

#[test]
#[should_panic(expected = "overflow")]
fn slot_overflow_is_caught() {
    let i = std::hint::black_box(u32::MAX);
    let _ = slot(i);
}
```

*Check 2: overflow-checks=off (the solver's release profile): the same test fails, the product wrapped* · `runs` · edition 2021 · host · test · output has “did not panic as expected” · output has “test result: FAILED” · exit code 101 · **✔ oracle pass**
```rust
const BODY_STRIDE: u32 = 17;

fn slot(i: u32) -> u32 {
    i * BODY_STRIDE
}

#[test]
#[should_panic(expected = "overflow")]
fn slot_overflow_is_caught() {
    let i = std::hint::black_box(u32::MAX);
    let _ = slot(i);
}
```

*Check 3: -O alone disables overflow checks: debug-assertions default off above opt-level 0* · `runs` · edition 2021 · host · test · output has “did not panic as expected” · exit code 101 · **✔ oracle pass**
```rust
const BODY_STRIDE: u32 = 17;

fn slot(i: u32) -> u32 {
    i * BODY_STRIDE
}

#[test]
#[should_panic(expected = "overflow")]
fn slot_overflow_is_caught() {
    let i = std::hint::black_box(u32::MAX);
    let _ = slot(i);
}
```

*Check 4: rustc refuses a test harness built with -C panic=abort on stable* · `compile_fail` · edition 2021 · host · test · stderr has “building tests with panic=abort is not supported without `-Zpanic_abort_tests`” · **✔ oracle pass**
```rust
#[test]
#[should_panic(expected = "NaN")]
fn nan_is_refused() {
    panic!("NaN input");
}
```

## Suppress lints with #[expect(lint, reason = "...")] (1.81+) instead of #[allow], so a stale suppression warns
**#[expect] silences a lint and emits unfulfilled_lint_expectations once the lint stops firing, while #[allow] goes stale silently. rustc never checks an #[expect(clippy::...)] (only a Clippy run does), and an expectation that holds on the host can be unfulfilled on wasm32.**

*Check 1: fulfilled #[expect] suppresses the lint and prints nothing* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
#[expect(unused_variables, reason = "kept until the restore path reads it")]
pub fn step(dt: f64) -> f64 {
    let scratch = dt * 2.0;
    dt
}
```

*Check 2: unfulfilled #[expect] warns unfulfilled_lint_expectations and shows the reason* · `compiles` · edition 2021 · host · lib · lints: unfulfilled_lint_expectations · stderr has “this lint expectation is unfulfilled” · stderr has “kept until the restore path reads it” · **✔ oracle pass**
```rust
#[expect(unused_variables, reason = "kept until the restore path reads it")]
pub fn step(dt: f64) -> f64 {
    let scratch = dt * 2.0;
    scratch
}
```

*Check 3: under -D warnings an unfulfilled expectation fails the build* · `compile_fail` · edition 2021 · host · lib · stderr has “this lint expectation is unfulfilled” · **✔ oracle pass**
```rust
#[expect(unused_variables, reason = "kept until the restore path reads it")]
pub fn step(dt: f64) -> f64 {
    let scratch = dt * 2.0;
    scratch
}
```

*Check 4: rustc does not check #[expect(clippy::float_cmp)]: no float == and still no warning* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
#[expect(clippy::float_cmp, reason = "exact compare is the point")]
pub fn is_tiny(x: f64) -> bool {
    x.abs() < 1e-12
}
```

*Check 5: host build: scratch is unused, so the expectation is fulfilled* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
#[expect(unused_variables, reason = "only the wasm32 build reads it")]
pub fn step(dt: f64) -> f64 {
    let scratch = dt * 2.0;
    #[cfg(target_arch = "wasm32")]
    let dt = scratch;
    dt
}
```

*Check 6: wasm32 build of the same source: scratch is used, so the expectation is unfulfilled* · `compiles` · edition 2021 · wasm32-unknown-unknown · cdylib · lints: unfulfilled_lint_expectations · **✔ oracle pass**
```rust
#[expect(unused_variables, reason = "only the wasm32 build reads it")]
pub fn step(dt: f64) -> f64 {
    let scratch = dt * 2.0;
    #[cfg(target_arch = "wasm32")]
    let dt = scratch;
    dt
}
```

*Check 7: cfg_attr scopes the expectation to non-wasm targets: the wasm32 build is clean* · `compiles` · edition 2021 · wasm32-unknown-unknown · cdylib · no warnings · **✔ oracle pass**
```rust
#[cfg_attr(not(target_arch = "wasm32"), expect(unused_variables, reason = "only the wasm32 build reads it"))]
pub fn step(dt: f64) -> f64 {
    let scratch = dt * 2.0;
    #[cfg(target_arch = "wasm32")]
    let dt = scratch;
    dt
}
```

## Unit-test the cdylib in #[cfg(test)] modules at the end of each file so the wasm bytes stay put
**cargo test --lib builds a cdylib-only crate's #[cfg(test)] modules into a native libtest binary without any crate-type change; the test code never reaches the wasm, but its position can, because line numbers of shipped code are stored in the binary.**

*Check 1: libtest harness: plain, should_panic(expected) and ignore(reason) tests; ignored test not run* · `runs` · edition 2021 · host · test · output has “test result: ok. 2 passed; 0 failed; 1 ignored” · output has “ignored, needs the full world” · exit code 0 · **✔ oracle pass**
```rust
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

fn refuse_nan(x: f64) -> f64 {
    if x.is_nan() {
        panic!("NaN input refused");
    }
    x
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn negative_zero_becomes_positive_zero() {
        assert_eq!(canon(-0.0).to_bits(), 0.0f64.to_bits());
    }

    #[test]
    #[should_panic(expected = "NaN input")]
    fn nan_is_refused() {
        refuse_nan(f64::NAN);
    }

    #[test]
    #[ignore = "needs the full world"]
    fn full_world_replay() {}
}
```

*Check 2: #[cfg(test)] code never enters the cdylib: its compile_error! does not fire; wasm export returns +0* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports canon_zero · imports nothing · node calls canon_zero() · **✔ oracle pass**
```rust
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

#[no_mangle]
pub extern "C" fn canon_zero() -> f64 {
    canon(-0.0)
}

#[cfg(test)]
mod tests {
    compile_error!("test code reached the shipped cdylib");
}
```
Expected output: `0`

*Check 3: tests in one binary share one copy of a static: the second test sees the first test's write* · `runs` · edition 2021 · host · test · output has “state leaked from another test” · output has “test result: FAILED. 1 passed; 1 failed” · exit code 101 · **✔ oracle pass**
```rust
use std::sync::atomic::{AtomicBool, AtomicU32, Ordering};
use std::time::{Duration, Instant};

// One copy per process, like the solver's `static mut` world.
static STEPS: AtomicU32 = AtomicU32::new(0);
static A_DONE: AtomicBool = AtomicBool::new(false);

#[test]
fn a_steps_the_world() {
    STEPS.fetch_add(1, Ordering::SeqCst);
    A_DONE.store(true, Ordering::SeqCst);
}

#[test]
fn b_expects_a_fresh_world() {
    // Wait for test a whether the harness runs the tests in parallel or one by one.
    let t0 = Instant::now();
    while !A_DONE.load(Ordering::SeqCst) && t0.elapsed() < Duration::from_secs(5) {
        std::thread::yield_now();
    }
    assert_eq!(STEPS.load(Ordering::SeqCst), 0, "state leaked from another test");
}
```

