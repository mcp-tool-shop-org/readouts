# Rust CI, reproducible binaries & supply chain — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](ci-reproducible-builds.md) · [catalog index](README.md)

## Gate the solver in ci.yml with fmt --check, clippy -D warnings for wasm32 and host cargo test --lib
**Rust gates need no new push-triggered workflow file. rustfmt --check, clippy with -D warnings for the wasm32 target and host unit tests of pure functions all fit in ci.yml, and `cargo test --lib` works on a cdylib-only crate. But today's solver fails -D warnings on seven static_mut_refs warnings, and integration tests or doctests would need "rlib", which moves the digest.**

*Check 1: -D warnings rejects the solver's BODIES.as_mut_ptr() (static_mut_refs)* · `compile_fail` · edition 2021 · wasm32-unknown-unknown · cdylib · stderr has “creating a mutable reference to mutable static” · stderr has “implied by `-D warnings`” · **✔ oracle pass**
```rust
// The solver's own export shape (solver/src/lib.rs, edition 2021).
static mut BODIES: [f64; 64 * 17] = [0.0; 64 * 17];

#[no_mangle]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    unsafe { BODIES.as_mut_ptr() }
}
```

*Check 2: the &raw mut form passes -D warnings with no warning at all* · `compiles` · edition 2021 · wasm32-unknown-unknown · cdylib · no warnings · exports bodies_ptr · **✔ oracle pass**
```rust
static mut BODIES: [f64; 64 * 17] = [0.0; 64 * 17];

// A raw pointer to the static, with no reference in between: nothing for static_mut_refs to flag.
#[no_mangle]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    (&raw mut BODIES).cast::<f64>()
}
```

*Check 3: a pure function's unit test runs natively on the host* · `runs` · edition 2021 · host · test · output has “negative_zero_becomes_positive_zero ... ok” · output has “1 passed” · **✔ oracle pass**
```rust
/// +0 for both signed zeros; NaN stays NaN (the shape of the solver's canon_zero).
fn canon_zero(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

#[test]
fn negative_zero_becomes_positive_zero() {
    assert_eq!(canon_zero(-0.0).to_bits(), 0u64);
    assert_eq!(canon_zero(1.5), 1.5);
    assert!(canon_zero(f64::NAN).is_nan());
}
```

*Check 4: the test harness refuses -C panic=abort, so host tests unwind* · `compile_fail` · edition 2021 · host · test · stderr has “building tests with panic=abort is not supported” · **✔ oracle pass**
```rust
/// +0 for both signed zeros; NaN stays NaN (the shape of the solver's canon_zero).
fn canon_zero(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

#[test]
fn negative_zero_becomes_positive_zero() {
    assert_eq!(canon_zero(-0.0).to_bits(), 0u64);
    assert_eq!(canon_zero(1.5), 1.5);
    assert!(canon_zero(f64::NAN).is_nan());
}
```

## Remap CARGO_HOME to make the solver digest path-independent, then scan the wasm for any leaked build path
**Dependency source paths reach the wasm as panic-location strings. Remapping the cargo home alone made the 1.98.1 solver build byte-identical across four checkout directories, one of them containing a space. Cargo passes the workspace member's own source to rustc as a relative path (`src\lib.rs`), so build.mjs's solver and repo remaps change no bytes today.**

*Check 1: a panic's Location names the absolute source path rustc was given* · `runs` · edition 2021 · host · bin · output has “rk-oracle-” · output has “main.rs” · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    // Print only where the panic happened, then let it end the process (exit 101).
    std::panic::set_hook(Box::new(|info| {
        if let Some(loc) = info.location() {
            println!("{}", loc.file());
        }
    }));
    let missing: Option<u32> = None;
    missing.unwrap();
}
```

*Check 2: in a wasm32 cdylib the Location data still names the build directory* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls location_names_build_dir() · **✔ oracle pass**
```rust
#[track_caller]
fn here() -> &'static std::panic::Location<'static> {
    std::panic::Location::caller()
}

// The static Location data a panic message reads. Does it name the directory rustc compiled in?
#[no_mangle]
pub extern "C" fn location_names_build_dir() -> i32 {
    here().file().contains("rk-oracle-") as i32
}
```
Expected output: `1`

*Check 3: -C strip=symbols keeps that path: it is data, not a symbol* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls location_names_build_dir() · **✔ oracle pass**
```rust
#[track_caller]
fn here() -> &'static std::panic::Location<'static> {
    std::panic::Location::caller()
}

// The static Location data a panic message reads. Does it name the directory rustc compiled in?
#[no_mangle]
pub extern "C" fn location_names_build_dir() -> i32 {
    here().file().contains("rk-oracle-") as i32
}
```
Expected output: `1`

## Run Miri, cargo-fuzz and cargo-mutants on a date-pinned nightly job that never builds the pinned digest
**Miri is a nightly component and cargo-fuzz needs -Z sanitizer flags; stable 1.98.1 refuses both `#![feature]` (E0554) and -Z options. So these tools run in their own jobs on a date-pinned nightly against host unit tests. rustc compiles raw-pointer reads past a static buffer without a warning, and the lint for &T-to-&mut casts misses the solver's Vec-parked form. Both are defects only a run-time checker such as Miri reports.**

*Check 1: stable rustc compiles an out-of-bounds read through a static buffer's raw pointer, no warning* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
static mut BODIES: [f64; 4] = [0.0; 4];

pub fn read_body(i: usize) -> f64 {
    // Nothing checks i < 4: an index past the end is an out-of-bounds read.
    unsafe { *(&raw const BODIES).cast::<f64>().add(i) }
}

pub fn past_the_end() -> f64 {
    read_body(4)
}
```

*Check 2: the pinned stable compiler refuses #![feature] (E0554)* · `compile_fail` · edition 2021 · host · lib · errors: E0554 · **✔ oracle pass**
```rust
#![feature(test)]
pub fn f() {}
```

## Pass build.mjs's flags via CARGO_ENCODED_RUSTFLAGS and refuse relaxed-simd in code: the bytes hide the pin
**Cargo uses only the first rustflags source it finds: CARGO_ENCODED_RUSTFLAGS, then RUSTFLAGS, then target rustflags, then build rustflags. RUSTFLAGS is split on whitespace. An inherited CARGO_ENCODED_RUSTFLAGS, even an empty one, drops every flag build.mjs sets. And on 1.98.1, losing `-C target-feature=-relaxed-simd` changes no byte, so only a compile-time guard notices a lost pin.**

*Check 1: default flags: the guard compiles, and cfg is false even inside a target_feature(enable) fn* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · no warnings · node calls guard_blind_spot() · **✔ oracle pass**
```rust
#[cfg(target_feature = "relaxed-simd")]
compile_error!("relaxed-simd reached rustc: the -C target-feature=-relaxed-simd pin was lost or overridden");

// A per-function enable does not set the crate-level cfg the guard reads.
#[target_feature(enable = "relaxed-simd")]
fn per_function_relaxed() -> i32 {
    cfg!(target_feature = "relaxed-simd") as i32 + 40
}

#[no_mangle]
pub extern "C" fn guard_blind_spot() -> i32 {
    per_function_relaxed() + cfg!(target_feature = "relaxed-simd") as i32
}
```
Expected output: `40`

*Check 2: +relaxed-simd reaching rustc turns the guard into a compile error* · `compile_fail` · edition 2021 · wasm32-unknown-unknown · cdylib · stderr has “relaxed-simd reached rustc” · **✔ oracle pass**
```rust
#[cfg(target_feature = "relaxed-simd")]
compile_error!("relaxed-simd reached rustc: the -C target-feature=-relaxed-simd pin was lost or overridden");

#[no_mangle]
pub extern "C" fn relaxed_simd_on() -> i32 {
    cfg!(target_feature = "relaxed-simd") as i32
}
```

