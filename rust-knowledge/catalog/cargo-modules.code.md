# Cargo, crates, modules & editions — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](cargo-modules.md) · [catalog index](README.md)

## Assume a Cargo feature enabled by any dependent is on for all; audit with `cargo tree -e features -i <crate>`
**Cargo compiles a dependency with the union of the features that every package selected for the build asks for (resolver 2 keeps build-dependencies, proc-macros and dev-dependencies apart), each passed to rustc as `--cfg feature="name"`, so `default-features = false` in one manifest does not keep defaults off when another dependent enables them.**

*Check 1: with --cfg feature="parallel" (an enabled feature) the one build takes the parallel path* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// One compilation of a crate sees one feature set. Cargo passes every enabled
// feature as `--cfg feature="..."`, and every dependent links that one build.
fn mode() -> &'static str {
    if cfg!(feature = "parallel") { "parallel" } else { "serial" }
}

fn main() {
    println!("{}", mode());
}
```
Expected output: `parallel`

*Check 2: without that cfg the same source takes the serial path* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// One compilation of a crate sees one feature set. Cargo passes every enabled
// feature as `--cfg feature="..."`, and every dependent links that one build.
fn mode() -> &'static str {
    if cfg!(feature = "parallel") { "parallel" } else { "serial" }
}

fn main() {
    println!("{}", mode());
}
```
Expected output: `serial`

## Choose [lib] crate-type by who loads it: cdylib for the wasm module, rlib for Rust callers, staticlib for C
**crate-type belongs to the library target (default "lib", the compiler-recommended Rust library); cdylib produces a system dynamic library for another language to load, which on wasm32-unknown-unknown is the .wasm module, while library dependencies are still compiled as Rust libraries whatever the root chooses.**

*Check 1: a wasm32 cdylib exports memory + the no_mangle fn, imports nothing, and the export runs* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, step · imports nothing · node calls step(3, 5) · **✔ oracle pass**
```rust
// The export shape of an engine call: a C-ABI function under an unmangled name.
#[no_mangle]
pub extern "C" fn step(n_bodies: u32, n_colliders: u32) -> u32 {
    (n_bodies <= 64 && n_colliders <= 64) as u32
}
```
Expected output: `1`

*Check 2: the same source builds as a native cdylib for the host* · `compiles` · edition 2021 · host · cdylib · no warnings · **✔ oracle pass**
```rust
// The export shape of an engine call: a C-ABI function under an unmangled name.
#[no_mangle]
pub extern "C" fn step(n_bodies: u32, n_colliders: u32) -> u32 {
    (n_bodies <= 64 && n_colliders <= 64) as u32
}
```

*Check 3: the same source builds as a staticlib for a C/C++ linker* · `compiles` · edition 2021 · host · staticlib · no warnings · **✔ oracle pass**
```rust
// The export shape of an engine call: a C-ABI function under an unmangled name.
#[no_mangle]
pub extern "C" fn step(n_bodies: u32, n_colliders: u32) -> u32 {
    (n_bodies <= 64 && n_colliders <= 64) as u32
}
```

## Migrate a crate's edition with `cargo fix --edition`, then edit `edition` yourself, then rebuild and test
**The edition is chosen per package (absent means 2015), crates of every edition link into one binary, and `cargo fix --edition` rewrites code toward the next edition but never changes the edition field and cannot fix everything.**

*Check 1: edition 2024 rejects a bare #[no_mangle]: unsafe attribute used without unsafe* · `compile_fail` · edition 2024 · host · lib · stderr has “unsafe attribute used without unsafe” · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn snapshot_len() -> u32 {
    0
}
```

*Check 2: edition 2021 accepts the solver's bare #[no_mangle] export (wasm cdylib, callable)* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, snapshot_len · node calls snapshot_len() · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn snapshot_len() -> u32 {
    0
}
```
Expected output: `0`

*Check 3: #[unsafe(no_mangle)] already compiles under edition 2021 (migrate attributes first)* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, snapshot_len · node calls snapshot_len() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn snapshot_len() -> u32 {
    0
}
```
Expected output: `0`

*Check 4: edition 2024 exports the same symbol with #[unsafe(no_mangle)]* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · exports memory, snapshot_len · node calls snapshot_len() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn snapshot_len() -> u32 {
    0
}
```
Expected output: `0`

## Set [profile.*] only in the root manifest, and remember config files and CARGO_PROFILE_* env vars override it
**Cargo reads profiles only from the workspace root's Cargo.toml and applies them to every crate in the graph (per-package overrides aside), emits a rustc -C flag only where a setting differs from rustc's own default, and lets a [profile] table in .cargo/config.toml or a CARGO_PROFILE_<NAME>_<KEY> variable override the manifest.**

*Check 1: opt-level=3 alone (the release profile's flags): overflow wraps and debug_assertions is off* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let x: u8 = std::hint::black_box(255);
    let y = x + 1;
    println!("{} debug_assertions={}", y, cfg!(debug_assertions));
}
```
Expected output: `0 debug_assertions=false`

*Check 2: opt-level=3 plus overflow-checks=on (what the env or config override adds) panics, exit 101* · `runs` · edition 2021 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    let x: u8 = std::hint::black_box(255);
    let y = x + 1;
    println!("{} debug_assertions={}", y, cfg!(debug_assertions));
}
```

*Check 3: debug-assertions=on with overflow-checks unset turns overflow checks on too (exit 101)* · `runs` · edition 2021 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    let x: u8 = std::hint::black_box(255);
    let y = x + 1;
    println!("{} debug_assertions={}", y, cfg!(debug_assertions));
}
```

*Check 4: Cargo's pair for release + debug-assertions = true: assertions on, overflow wraps* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let x: u8 = std::hint::black_box(255);
    let y = x + 1;
    println!("{} debug_assertions={}", y, cfg!(debug_assertions));
}
```
Expected output: `0 debug_assertions=true`

*Check 5: panic = "abort" arrives as -C panic=abort, visible as cfg(panic = "abort")* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
fn main() {
    println!("panic=abort: {}", cfg!(panic = "abort"));
}
```
Expected output: `panic=abort: true`

## Share lock, target dir and lints across crates with [workspace.dependencies] and [workspace.lints]
**Workspace members share one Cargo.lock and one target/ at the root, [profile], [patch] and [replace] count only in the root manifest, [workspace.dependencies] and [workspace.lints] are inherited with `workspace = true`, and a virtual workspace must name its resolver or it falls back to resolver 1.**

*Check 1: -F unsafe_code (what [workspace.lints] forbid passes) rejects an unsafe block* · `compile_fail` · edition 2021 · host · lib · stderr has “usage of an `unsafe` block” · stderr has “requested on the command line with `-F unsafe-code`” · **✔ oracle pass**
```rust
// `[workspace.lints.rust] unsafe_code = "forbid"` reaches each member as
// `--forbid=unsafe_code`; `-F unsafe_code` is the same flag.
pub fn first(p: *const f64) -> f64 {
    unsafe { *p }
}
```

*Check 2: under forbid, #[allow(unsafe_code)] is itself an error, E0453* · `compile_fail` · edition 2021 · host · lib · errors: E0453 · stderr has “incompatible with previous forbid” · **✔ oracle pass**
```rust
#[allow(unsafe_code)]
pub fn first(p: *const f64) -> f64 {
    unsafe { *p }
}
```

*Check 3: under deny, #[allow(unsafe_code)] on the item is accepted without a warning* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
#[allow(unsafe_code)]
pub fn first(p: *const f64) -> f64 {
    unsafe { *p }
}
```

## Split a crate into file modules with `mod name;` and share internals via pub(crate) / pub(super), not pub
**A package holds at most one library crate plus any number of binaries; each crate is a module tree in which `mod name;` loads name.rs (or name/mod.rs, never both), and privacy is per module, so pub(crate) and pub(super) say exactly who may use an item.**

*Check 1: pub(super) is callable from the parent module and pub(crate) from anywhere in the crate* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
mod outer {
    pub mod inner {
        pub(super) fn only_outer() -> u32 {
            1
        }
        pub(crate) fn whole_crate() -> u32 {
            2
        }
    }
    pub fn via_outer() -> u32 {
        inner::only_outer()
    }
}

fn main() {
    println!("{} {}", outer::via_outer(), outer::inner::whole_crate());
}
```
Expected output: `1 2`

*Check 2: a pub(super) item named from the crate root is E0603 (private)* · `compile_fail` · edition 2021 · host · bin · errors: E0603 · stderr has “function `only_outer` is private” · **✔ oracle pass**
```rust
mod outer {
    pub mod inner {
        pub(super) fn only_outer() -> u32 {
            1
        }
    }
    pub fn via_outer() -> u32 {
        inner::only_outer()
    }
}

fn main() {
    let _ = outer::via_outer();
    // pub(super) reaches `outer`, not the crate root.
    let _ = outer::inner::only_outer();
}
```

*Check 3: `mod rapier_law;` with no rapier_law.rs is E0583 (file not found for module)* · `compile_fail` · edition 2021 · host · bin · errors: E0583 · stderr has “file not found for module `rapier_law`” · **✔ oracle pass**
```rust
// `mod name;` without a body loads name.rs (or name/mod.rs) next to this file.
mod rapier_law;

fn main() {}
```

## Treat Cargo's rustflags sources as exclusive: any RUSTFLAGS, even empty, drops .cargo/config.toml rustflags
**Cargo uses only the first of CARGO_ENCODED_RUSTFLAGS, RUSTFLAGS, all matching [target.<triple>] / [target.<cfg>] rustflags (joined), or [build] rustflags, so exporting RUSTFLAGS to add one flag silently discards a pin kept in .cargo/config.toml.**

*Check 1: on 1.98.1 wasm32-unknown-unknown compiles with relaxed-simd off by default* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls relaxed_simd_enabled() · **✔ oracle pass**
```rust
// Reports whether this compilation had the relaxed-simd target feature on.
#[no_mangle]
pub extern "C" fn relaxed_simd_enabled() -> u32 {
    cfg!(target_feature = "relaxed-simd") as u32
}
```
Expected output: `0`

*Check 2: -C target-feature=-relaxed-simd (the solver's config pin) keeps it off* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls relaxed_simd_enabled() · **✔ oracle pass**
```rust
// Reports whether this compilation had the relaxed-simd target feature on.
#[no_mangle]
pub extern "C" fn relaxed_simd_enabled() -> u32 {
    cfg!(target_feature = "relaxed-simd") as u32
}
```
Expected output: `0`

*Check 3: -C target-feature=+relaxed-simd turns it on: the rustflags that reach rustc decide* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls relaxed_simd_enabled() · **✔ oracle pass**
```rust
// Reports whether this compilation had the relaxed-simd target feature on.
#[no_mangle]
pub extern "C" fn relaxed_simd_enabled() -> u32 {
    cfg!(target_feature = "relaxed-simd") as u32
}
```
Expected output: `1`

