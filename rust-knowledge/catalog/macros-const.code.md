# Macros, const evaluation & build scripts — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](macros-const.md) · [catalog index](README.md)

## Compute tables in const fn with while, match and &mut; expect E0015 on for-loops, trait calls and formatting
**On 1.98.1 const code runs loop/while/if/match, takes &mut (1.83), does float arithmetic (1.82) and panics with literal messages (1.57); for-loops, iterator methods, trait operators on your own types, PartialEq on str, heap allocation and formatted panic messages are refused.**

*Check 1: const fn with while, &mut, match, if and loop-break builds tables at compile time* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
const fn fill(buf: &mut [f64; 4], v: f64) {
    let mut i = 0;
    while i < buf.len() { buf[i] = v * i as f64; i += 1; }
}
const TABLE: [f64; 4] = { let mut t = [0.0; 4]; fill(&mut t, 0.25); t };
const fn classify(n: i32) -> &'static str {
    match n { i32::MIN..=-1 => "neg", 0 => "zero", _ => if n > 100 { "big" } else { "pos" } }
}
const LOOPED: u32 = { let mut n = 0u32; loop { n += 3; if n > 10 { break n; } } };
fn main() { println!("{:?} {} {} {}", TABLE, classify(0), classify(500), LOOPED); }
```
Expected output: `[0.0, 0.25, 0.5, 0.75] zero big 12`

*Check 2: a `for` loop in a const fn is refused (E0015)* · `compile_fail` · edition 2024 · host · errors: E0015 · stderr has “cannot use `for` loop” · **✔ oracle pass**
```rust
const fn sum(n: u32) -> u32 { let mut s = 0; for i in 0..n { s += i; } s }
fn main() { println!("{}", sum(4)); }
```

*Check 3: iterator methods are trait calls: a.iter().sum() in a const is refused (E0015)* · `compile_fail` · edition 2024 · host · errors: E0015 · stderr has “is not yet stable as a const fn” · **✔ oracle pass**
```rust
const S: f64 = { let a = [1.0f64, 2.0]; a.iter().sum() };
fn main() { println!("{S}"); }
```

*Check 4: an operator from a user impl of Add is not callable in a const fn (E0015)* · `compile_fail` · edition 2024 · host · errors: E0015 · stderr has “cannot call non-const operator in constant functions” · **✔ oracle pass**
```rust
#[derive(Clone, Copy)] struct V(f64);
impl core::ops::Add for V { type Output = V; fn add(self, o: V) -> V { V(self.0 + o.0) } }
const fn twice(a: V) -> V { a + a }
fn main() { println!("{}", twice(V(1.0)).0); }
```

*Check 5: str == str in a const fn: PartialEq is not a stable const trait (E0658)* · `compile_fail` · edition 2024 · host · errors: E0658 · stderr has “`PartialEq` is not yet stable as a const trait” · **✔ oracle pass**
```rust
const fn same(a: &str, b: &str) -> bool { a == b }
fn main() { println!("{}", same("a", "a")); }
```

*Check 6: heap allocation in a const fn: Vec::push is refused (E0658, E0493)* · `compile_fail` · edition 2024 · host · errors: E0658, E0493 · **✔ oracle pass**
```rust
const fn make() -> usize { let mut v: Vec<u8> = Vec::new(); v.push(1); v.len() }
fn main() { println!("{}", make()); }
```

*Check 7: a const assert! may not format an integer (E0015)* · `compile_fail` · edition 2024 · host · errors: E0015 · stderr has “cannot call non-const formatting macro” · **✔ oracle pass**
```rust
const STRIDE: usize = 17;
const _: () = assert!(STRIDE == 17, "stride is {}", STRIDE);
fn main() {}
```

*Check 8: a literal panic in a const fn called from a const is compile error E0080* · `compile_fail` · edition 2024 · host · errors: E0080 · stderr has “BODY_STRIDE changed: update build.mjs” · **✔ oracle pass**
```rust
const fn check(stride: usize) { if stride != 17 { panic!("BODY_STRIDE changed: update build.mjs"); } }
const _: () = check(18);
fn main() {}
```

## Embed build inputs with include_bytes!, include_str!, env! and concat!, and know which of them fail the build
**include_bytes!/include_str! embed a file located relative to the current source file, env! bakes in a compile-time variable and fails the build when it is unset (option_env! returns None), concat! joins literals into a &'static str, stringify! returns tokens as text, and compile_error! stops the build with your message.**

*Check 1: concat!, stringify!, include_str!/include_bytes! of this file, option_env! of an unset var* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
const TAG: &str = concat!("si-solver/", 17, "/", 2.5, "/", true, "/", 'x');
const SRC: &str = stringify!(BODY_STRIDE * 8 + HX);
const ME: &[u8] = include_bytes!(file!());
const ME_STR: &str = include_str!(file!());
const MISSING: Option<&str> = option_env!("SI_RK_ORACLE_UNSET_9F3A");
fn main() {
    println!("{TAG}");
    println!("{SRC}");
    println!("{} {}", ME.len() == ME_STR.len(), ME_STR.lines().next().unwrap().starts_with("const TAG"));
    println!("{:?}", MISSING);
}
```
Expected output: `si-solver/17/2.5/true/x BODY_STRIDE * 8 + HX true true None`

*Check 2: env! of an unset variable fails the build* · `compile_fail` · edition 2024 · host · stderr has “environment variable `SI_RK_ORACLE_UNSET_9F3A` not defined at compile time” · **✔ oracle pass**
```rust
const V: &str = env!("SI_RK_ORACLE_UNSET_9F3A");
fn main() { println!("{V}"); }
```

*Check 3: env!'s second argument replaces the error text* · `compile_fail` · edition 2024 · host · stderr has “set SI_RK_ORACLE_UNSET_9F3A to the law version” · **✔ oracle pass**
```rust
const V: &str = env!("SI_RK_ORACLE_UNSET_9F3A", "set SI_RK_ORACLE_UNSET_9F3A to the law version");
fn main() { println!("{V}"); }
```

*Check 4: include_bytes! of a missing file fails the build* · `compile_fail` · edition 2024 · host · stderr has “couldn't read” · **✔ oracle pass**
```rust
const B: &[u8] = include_bytes!("pinned/si_solver.wasm");
fn main() { println!("{}", B.len()); }
```

*Check 5: a const fn hash over include_bytes! is computed at compile time and matches run time* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
const BYTES: &[u8] = include_bytes!(file!());
const fn fnv1a(b: &[u8]) -> u64 {
    let mut h = 0xcbf29ce484222325u64;
    let mut i = 0;
    while i < b.len() { h ^= b[i] as u64; h = h.wrapping_mul(0x100000001b3); i += 1; }
    h
}
const DIGEST: u64 = fnv1a(BYTES);
fn main() { println!("{}", DIGEST == fnv1a(std::hint::black_box(BYTES))); }
```
Expected output: `true`

*Check 6: compile_error! in a fallback arm names the valid inputs* · `compile_fail` · edition 2024 · host · stderr has “law! accepts `box` or `rapier`” · **✔ oracle pass**
```rust
macro_rules! law {
    (box) => { 1u32 };
    (rapier) => { 2u32 };
    ($other:ident) => { compile_error!("law! accepts `box` or `rapier`") };
}
fn main() { println!("{}", law!(rapier) + law!(havok)); }
```

## Emit cargo:: lines from build.rs, pair rustc-cfg with rustc-check-cfg, and read the target from CARGO_CFG_*
**A build script is a host program Cargo compiles and runs before the crate; since Cargo 1.77 it speaks `cargo::KEY=VALUE`, it must learn the target from CARGO_CFG_* (cfg! there describes the host), write only into OUT_DIR, and declare every cfg it sets.**

*Check 1: `cargo::rustc-cfg=si_abi_generated` reaches rustc as --cfg: the gated item exists* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
#[cfg(si_abi_generated)]
const GENERATED: bool = true;
#[cfg(not(si_abi_generated))]
const GENERATED: bool = false;
fn main() { println!("{}", GENERATED); }
```
Expected output: `true`

*Check 2: without the build script's --cfg the other branch is compiled* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
#[cfg(si_abi_generated)]
const GENERATED: bool = true;
#[cfg(not(si_abi_generated))]
const GENERATED: bool = false;
fn main() { println!("{}", GENERATED); }
```
Expected output: `false`

*Check 3: `cargo::rustc-cfg=abi="v2"` is a key-value cfg: #[cfg(abi = "v2")] selects* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
#[cfg(abi = "v2")]
const ABI: &str = "v2";
#[cfg(not(abi = "v2"))]
const ABI: &str = "v1";
fn main() { println!("{}", ABI); }
```
Expected output: `v2`

*Check 4: OUT_DIR exists only in a Cargo build with a build script; plain rustc refuses the include* · `compile_fail` · edition 2024 · host · stderr has “environment variable `OUT_DIR` not defined at compile time” · **✔ oracle pass**
```rust
include!(concat!(env!("OUT_DIR"), "/abi.rs"));
fn main() {}
```

## Gate wasm code on target_family = "wasm" and turn a forbidden target feature into compile_error!
**#[cfg] removes items before type checking, cfg! only yields a bool, and cfg_attr adds attributes conditionally; on 1.98.1 wasm32-unknown-unknown sets target_family = "wasm", target_arch = "wasm32", target_os = "unknown" and panic = "abort", so `#[cfg(target_feature = "relaxed-simd")] compile_error!(...)` turns a flag slip into a failed build.**

*Check 1: wasm32-unknown-unknown: family wasm, arch wasm32, os unknown, panic abort, no simd128 (=23)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · exports cfg_word · imports nothing · node calls cfg_word() · **✔ oracle pass**
```rust
#[cfg(target_feature = "relaxed-simd")]
compile_error!("si-solver refuses relaxed-simd: it admits fused multiply-add and non-deterministic lanes");

#[unsafe(no_mangle)]
pub extern "C" fn cfg_word() -> u32 {
    (cfg!(target_family = "wasm") as u32)
        | (cfg!(target_arch = "wasm32") as u32) << 1
        | (cfg!(target_os = "unknown") as u32) << 2
        | (cfg!(target_feature = "simd128") as u32) << 3
        | (cfg!(panic = "abort") as u32) << 4
}
```
Expected output: `23`

*Check 2: -C target-feature=+simd128 flips only the simd128 bit (=31)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls cfg_word() · **✔ oracle pass**
```rust
#[cfg(target_feature = "relaxed-simd")]
compile_error!("si-solver refuses relaxed-simd: it admits fused multiply-add and non-deterministic lanes");

#[unsafe(no_mangle)]
pub extern "C" fn cfg_word() -> u32 {
    (cfg!(target_family = "wasm") as u32)
        | (cfg!(target_arch = "wasm32") as u32) << 1
        | (cfg!(target_os = "unknown") as u32) << 2
        | (cfg!(target_feature = "simd128") as u32) << 3
        | (cfg!(panic = "abort") as u32) << 4
}
```
Expected output: `31`

*Check 3: the cfg + compile_error! guard fails a build that enables relaxed-simd* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “si-solver refuses relaxed-simd” · **✔ oracle pass**
```rust
#[cfg(target_feature = "relaxed-simd")]
compile_error!("si-solver refuses relaxed-simd: it admits fused multiply-add and non-deterministic lanes");

#[unsafe(no_mangle)]
pub extern "C" fn cfg_word() -> u32 {
    (cfg!(target_family = "wasm") as u32)
        | (cfg!(target_arch = "wasm32") as u32) << 1
        | (cfg!(target_os = "unknown") as u32) << 2
        | (cfg!(target_feature = "simd128") as u32) << 3
        | (cfg!(panic = "abort") as u32) << 4
}
```

*Check 4: wasm32v1-none: same family and arch, target_os = "none" (=19)* · `runs` · edition 2024 · wasm32v1-none · cdylib · node calls cfg_word() · **✔ oracle pass**
```rust
#![no_std]
#[panic_handler]
fn on_panic(_: &core::panic::PanicInfo) -> ! { loop {} }
#[cfg(target_feature = "relaxed-simd")]
compile_error!("si-solver refuses relaxed-simd: it admits fused multiply-add and non-deterministic lanes");

#[unsafe(no_mangle)]
pub extern "C" fn cfg_word() -> u32 {
    (cfg!(target_family = "wasm") as u32)
        | (cfg!(target_arch = "wasm32") as u32) << 1
        | (cfg!(target_os = "unknown") as u32) << 2
        | (cfg!(target_feature = "simd128") as u32) << 3
        | (cfg!(panic = "abort") as u32) << 4
}
```
Expected output: `19`

*Check 5: cfg! only yields a bool: the dead branch must still resolve (E0425 on the host)* · `compile_fail` · edition 2024 · host · errors: E0425 · **✔ oracle pass**
```rust
#[cfg(target_family = "wasm")]
fn wasm_only() -> &'static str { "wasm" }
fn main() {
    let s = if cfg!(target_family = "wasm") { wasm_only() } else { "host" };
    println!("{s}");
}
```

*Check 6: #[cfg] removes the item, so the host build compiles without it* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
#[cfg(target_family = "wasm")]
fn which() -> &'static str { "wasm" }
#[cfg(not(target_family = "wasm"))]
fn which() -> &'static str { "host" }
fn main() { println!("{}", which()); }
```
Expected output: `host`

*Check 7: cfg_attr expands to several attributes: an export named only on wasm* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · exports law_version · node calls law_version() · **✔ oracle pass**
```rust
#[cfg_attr(target_family = "wasm", unsafe(no_mangle), inline(never))]
pub extern "C" fn law_version() -> u32 { 2 }
```
Expected output: `2`

## Keep const generics to standalone integer, bool and char params; size nested arrays, never N * STRIDE
**Stable const generics (since 1.51) take integer, bool and char parameters used standalone in types; arithmetic on a parameter inside a type, f64 or &str parameters, and #![feature(generic_const_exprs)] are all refused on 1.98.1.**

*Check 1: stable const generics: usize/bool/char params, nested arrays, assoc const, braced arg* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
struct Pool<const N: usize, const STRIDE: usize> { data: [[f64; STRIDE]; N] }
impl<const N: usize, const STRIDE: usize> Pool<N, STRIDE> {
    const WORDS: usize = N * STRIDE;
    fn new() -> Self { Pool { data: [[0.0; STRIDE]; N] } }
    fn words(&self) -> usize { Self::WORDS }
}
fn sum<const N: usize>(xs: [f64; N]) -> f64 { let mut s = 0.0; let mut i = 0; while i < N { s += xs[i]; i += 1; } s }
struct Flag<const ON: bool>;
struct Axis<const C: char>;
fn main() {
    let p: Pool<64, 17> = Pool::new();
    println!("{} {} {}", p.words(), p.data.len(), sum([0.5, 0.25, 0.125]));
    let _ = (Flag::<true>, Axis::<'y'>);
    const K: usize = 3;
    println!("{}", sum::<{ K + 1 }>([1.0; 4]));
}
```
Expected output: `1088 64 0.875 4`

*Check 2: N * 17 in a type is generic_const_exprs territory: refused on stable* · `compile_fail` · edition 2024 · host · stderr has “generic parameters may not be used in const operations” · **✔ oracle pass**
```rust
fn flat<const N: usize>() -> [f64; N * 17] { [0.0; N * 17] }
fn main() { println!("{}", flat::<2>().len()); }
```

*Check 3: an associated const derived from params still cannot size a type* · `compile_fail` · edition 2024 · host · stderr has “generic `Self` types are currently not permitted in anonymous constants” · **✔ oracle pass**
```rust
struct Pool<const N: usize, const STRIDE: usize>;
impl<const N: usize, const STRIDE: usize> Pool<N, STRIDE> {
    const WORDS: usize = N * STRIDE;
    fn flat(&self) -> [f64; Self::WORDS] { [0.0; Self::WORDS] }
}
fn main() {}
```

*Check 4: f64 is not an allowed const parameter type* · `compile_fail` · edition 2024 · host · stderr has “`f64` is forbidden as the type of a const generic parameter” · **✔ oracle pass**
```rust
struct Angle<const RAD: f64>;
fn main() {}
```

*Check 5: #![feature(generic_const_exprs)] is refused on the stable channel (E0554)* · `compile_fail` · edition 2024 · host · errors: E0554 · **✔ oracle pass**
```rust
#![feature(generic_const_exprs)]
fn main() {}
```

*Check 6: the stable workaround: [[f64; 17]; 2] flattens to 34 contiguous f64* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
fn main() {
    let nested: [[f64; 17]; 2] = [[1.0; 17]; 2];
    let flat: &[f64] = nested.as_flattened();
    println!("{} {}", flat.len(), core::mem::size_of::<[[f64; 17]; 2]>());
}
```
Expected output: `34 272`

## Trust const f64 bits for + - * /, but keep d * PI / 180.0: to_radians() differs on 93 of 361 integer degrees
**rustc evaluates const float arithmetic in the soft-float rustc_apfloat, so finite + - * / results are the IEEE bits an IEEE-conforming target computes at run time, whatever the build host (only NaN sign and payload may differ); sqrt, powi, exp, sin and cos are not const on 1.98.1; and to_radians() multiplies by a pre-rounded PI / 180, a different rounding from d * PI / 180.0.**

*Check 1: SLIDE_ANGLE/CLIMB_ANGLE: const bits equal run-time bits and to_radians for 50 and 45* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use core::f64::consts::{FRAC_PI_4, PI};
use std::hint::black_box;
const SLIDE_ANGLE: f64 = 50.0 * PI / 180.0;
const SLIDE_TO_RAD: f64 = 50.0f64.to_radians();
const CLIMB_ANGLE: f64 = FRAC_PI_4;
const CLIMB_EXPR: f64 = 45.0 * PI / 180.0;
fn main() {
    let rt = black_box(50.0f64) * black_box(PI) / black_box(180.0f64);
    println!("{:016x} {:016x} {:016x}", SLIDE_ANGLE.to_bits(), rt.to_bits(), SLIDE_TO_RAD.to_bits());
    println!("{:016x} {:016x}", CLIMB_ANGLE.to_bits(), CLIMB_EXPR.to_bits());
}
```
Expected output: `3febecde5da115a9 3febecde5da115a9 3febecde5da115a9 3fe921fb54442d18 3fe921fb54442d18`

*Check 2: to_radians multiplies by a pre-rounded PI/180: 46 and 3 degrees differ by one ulp* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use core::f64::consts::PI;
const D46: f64 = 46.0 * PI / 180.0;
const D46_TO_RAD: f64 = 46.0f64.to_radians();
const D3: f64 = 3.0 * PI / 180.0;
const D3_TO_RAD: f64 = 3.0f64.to_radians();
fn main() {
    println!("{:016x} {:016x}", D46.to_bits(), D46_TO_RAD.to_bits());
    println!("{:016x} {:016x}", D3.to_bits(), D3_TO_RAD.to_bits());
}
```
Expected output: `3fe9b0f58956c201 3fe9b0f58956c202 3faacee9f37bebd5 3faacee9f37bebd6`

*Check 3: in wasm (node), run-time d*PI/180 matches the compiler's consts; 46 still != to_radians (=15)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls angle_word(50, 45, 46) · **✔ oracle pass**
```rust
use core::f64::consts::{FRAC_PI_4, PI};
const SLIDE_ANGLE: f64 = 50.0 * PI / 180.0;
const D46: f64 = 46.0 * PI / 180.0;
#[unsafe(no_mangle)]
pub extern "C" fn angle_word(d50: f64, d45: f64, d46: f64) -> u32 {
    let slide = d50 * PI / 180.0;
    let climb = d45 * PI / 180.0;
    let a46 = d46 * PI / 180.0;
    ((slide.to_bits() == SLIDE_ANGLE.to_bits()) as u32)
        | ((climb.to_bits() == FRAC_PI_4.to_bits()) as u32) << 1
        | ((a46.to_bits() == D46.to_bits()) as u32) << 2
        | ((a46.to_bits() != d46.to_radians().to_bits()) as u32) << 3
}
```
Expected output: `15`

*Check 4: f64::sin is not const on 1.98.1 (E0015)* · `compile_fail` · edition 2024 · host · errors: E0015 · stderr has “cannot call non-const method `f64::<impl f64>::sin`” · **✔ oracle pass**
```rust
const S: f64 = (0.5f64).sin();
fn main() { println!("{}", S); }
```

*Check 5: f64::sqrt is not const on 1.98.1 (E0015)* · `compile_fail` · edition 2024 · host · errors: E0015 · stderr has “cannot call non-const method `f64::<impl f64>::sqrt`” · **✔ oracle pass**
```rust
const S: f64 = (2.0f64).sqrt();
fn main() { println!("{}", S); }
```

*Check 6: x86_64 host: 0.0/0.0 is +NaN in const, -NaN at run time (the 1.82 post's example)* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;
const CT: f64 = 0.0 / 0.0;
const CT_POSITIVE: bool = (0.0f64 / 0.0).is_sign_positive();
fn main() {
    let rt = black_box(0.0f64) / black_box(0.0f64);
    println!("const {:016x} {}", CT.to_bits(), CT_POSITIVE);
    println!("rt    {:016x} {}", rt.to_bits(), rt.is_sign_positive());
}
```
Expected output: `const 7ff8000000000000 true rt    fff8000000000000 false`

## Use a derive proc macro only when code must read a type's definition; count its syn builds in build time
**Proc macros (derive, attribute, function-like) live in separate proc-macro crates that rustc runs during expansion, usually on syn, quote and proc-macro2; they can generate code and compile-time checks from a struct's definition, and they cost host-side dependency builds plus unoptimized expansion (uncached, per the 2025 survey post).**

*Check 1: derive(Pod) rejects a padded repr(C) struct at compile time (E0080)* · `compile_fail` · edition 2024 · host · deps: bytemuck · errors: E0080 · stderr has “derive(Pod) was applied to a type with padding” · **✔ oracle pass**
```rust
use bytemuck::{Pod, Zeroable};
#[derive(Clone, Copy, Pod, Zeroable)]
#[repr(C)]
struct Padded { flag: u8, x: f64 }
fn main() {}
```

*Check 2: derive(Pod) rejects a struct without repr(C) / repr(transparent)* · `compile_fail` · edition 2024 · host · deps: bytemuck · stderr has “Pod requires the type to be #[repr(C)] or #[repr(transparent)]” · **✔ oracle pass**
```rust
use bytemuck::{Pod, Zeroable};
#[derive(Clone, Copy, Pod, Zeroable)]
struct NoRepr { x: f64, y: f64 }
fn main() {}
```

*Check 3: a 17-f64 repr(C) body passes derive(Pod) and casts to a flat f64 slice* · `runs` · edition 2024 · host · deps: bytemuck · **✔ oracle pass**
```rust
use bytemuck::{Pod, Zeroable};
#[derive(Clone, Copy, Pod, Zeroable)]
#[repr(C)]
struct Body { pos: [f64; 3], vel: [f64; 3], rot: [f64; 4], ang: [f64; 3], half: [f64; 3], driven: f64 }
fn main() {
    let b = Body { pos: [1.0, 2.0, 3.0], vel: [0.0; 3], rot: [0.0, 0.0, 0.0, 1.0], ang: [0.0; 3], half: [0.5, 0.25, 0.125], driven: 1.0 };
    let bodies = [b; 2];
    let flat: &[f64] = bytemuck::cast_slice(&bodies);
    println!("{} {} {} {}", flat.len(), core::mem::size_of::<Body>(), flat[17 + 13], flat[17 + 16]);
}
```
Expected output: `34 136 0.5 1`

## Use const for values, static for one address, const { } for non-Copy repeats and generic compile-time asserts
**A const is inlined as a fresh value at every use, so interior mutability on it does nothing (rustc warns), while a static has one address and must be Sync unless mut; inline `const { }` blocks (1.79) run at compile time inside functions, may use generics, and fail per instantiation.**

*Check 1: a const atomic is a fresh copy per use (warns); the static keeps state and one address* · `runs` · edition 2024 · host · lints: const_item_interior_mutations · **✔ oracle pass**
```rust
use std::sync::atomic::{AtomicU32, Ordering};
const COUNTER_C: AtomicU32 = AtomicU32::new(0);
static COUNTER_S: AtomicU32 = AtomicU32::new(0);
fn main() {
    COUNTER_C.fetch_add(1, Ordering::Relaxed);
    COUNTER_C.fetch_add(1, Ordering::Relaxed);
    COUNTER_S.fetch_add(1, Ordering::Relaxed);
    COUNTER_S.fetch_add(1, Ordering::Relaxed);
    println!("const {} static {}", COUNTER_C.load(Ordering::Relaxed), COUNTER_S.load(Ordering::Relaxed));
    let a = &raw const COUNTER_S;
    let b = &raw const COUNTER_S;
    println!("same address {}", a == b);
}
```
Expected output: `const 0 static 2 same address true`

*Check 2: a non-mut static must be Sync: static Cell is E0277* · `compile_fail` · edition 2024 · host · errors: E0277 · **✔ oracle pass**
```rust
use std::cell::Cell;
static FLAG: Cell<bool> = Cell::new(false);
fn main() { FLAG.set(true); }
```

*Check 3: inline const repeats a non-Copy value: [const { Vec::new() }; 4]* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
fn main() {
    let bufs: [Vec<f64>; 4] = [const { Vec::new() }; 4];
    println!("{}", bufs.iter().map(|b| b.capacity()).sum::<usize>() + bufs.len());
}
```
Expected output: `4`

*Check 4: without const { }, [Vec::new(); 4] needs Copy (E0277)* · `compile_fail` · edition 2024 · host · errors: E0277 · **✔ oracle pass**
```rust
fn main() {
    let bufs: [Vec<f64>; 4] = [Vec::new(); 4];
    println!("{}", bufs.len());
}
```

*Check 5: const { assert! } in a generic fn fails to compile for the bad instantiation (E0080)* · `compile_fail` · edition 2024 · host · bin · errors: E0080 · stderr has “while instantiating `fn stride_of::<0>`” · **✔ oracle pass**
```rust
fn stride_of<const N: usize>() -> usize {
    const { assert!(N > 0, "stride must be positive") };
    N
}
fn main() { println!("{}", stride_of::<17>()); println!("{}", stride_of::<0>()); }
```

*Check 6: the same file as a lib (main unused, nothing instantiates ::<0>) builds cleanly* · `compiles` · edition 2024 · host · lib · **✔ oracle pass**
```rust
fn stride_of<const N: usize>() -> usize {
    const { assert!(N > 0, "stride must be positive") };
    N
}
fn main() { println!("{}", stride_of::<17>()); println!("{}", stride_of::<0>()); }
```

*Check 7: the same assert! outside const { } compiles and panics at run time (exit 101)* · `runs` · edition 2024 · host · exit code 101 · **✔ oracle pass**
```rust
fn stride_of<const N: usize>() -> usize {
    assert!(N > 0, "stride must be positive");
    N
}
fn main() { println!("{}", stride_of::<17>()); println!("{}", stride_of::<0>()); }
```
Expected output: `17`

## Write macro_rules! with fragment follow-sets, $crate paths and edition 2024's wider expr (expr_2021) in mind
**macro_rules! matches token fragments under follow-set rules and mixed-site hygiene, is visible only after its definition unless #[macro_export] moves it to the crate root, and from edition 2024 `expr` also matches `const { }` and `_` while `expr_2021` keeps the 2021 set.**

*Check 1: repetition + stringify!: one invocation declares six consts and a names table* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
macro_rules! abi_table {
    ($( $name:ident = $val:literal ),+ $(,)?) => {
        $( pub const $name: usize = $val; )+
        pub const ABI_NAMES: &[&str] = &[ $( stringify!($name) ),+ ];
        pub const ABI_VALUES: &[usize] = &[ $( $val ),+ ];
    };
}
abi_table! { BODY_STRIDE = 17, HX = 13, HY = 14, HZ = 15, DRIVEN = 16, COLLIDER_STRIDE = 10, }
fn main() {
    for (n, v) in ABI_NAMES.iter().zip(ABI_VALUES) { print!("{n}={v} "); }
    println!("| {}", HX + DRIVEN);
}
```
Expected output: `BODY_STRIDE=17 HX=13 HY=14 HZ=15 DRIVEN=16 COLLIDER_STRIDE=10 / 29`

*Check 2: hygiene: a local declared inside the expansion is invisible to the caller (E0425)* · `compile_fail` · edition 2024 · host · errors: E0425 · stderr has “not accessible due to macro hygiene” · **✔ oracle pass**
```rust
macro_rules! declare { () => { let x = 1; }; }
fn main() { declare!(); println!("{}", x); }
```

*Check 3: textual scope: a macro used above its definition is not found* · `compile_fail` · edition 2024 · host · stderr has “cannot find macro `m` in this scope” · **✔ oracle pass**
```rust
fn main() { m!(); }
macro_rules! m { () => {}; }
```

*Check 4: follow-set: an expr fragment may not be followed by an ident* · `compile_fail` · edition 2024 · host · stderr has “which is not allowed for `expr` fragments” · **✔ oracle pass**
```rust
macro_rules! bad { ($e:expr $i:ident) => {}; }
fn main() {}
```

*Check 5: #[macro_export] puts the macro at the crate root; $crate finds items with no import* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
pub mod abi {
    pub const BODY_STRIDE: usize = 17;
    pub fn at(i: usize, slot: usize) -> usize { i * BODY_STRIDE + slot }
    #[macro_export]
    macro_rules! slot {
        ($i:expr, $s:expr) => { $crate::abi::at($i, $s) };
    }
}
mod elsewhere {
    pub fn probe() -> usize { crate::slot!(2, 13) }
}
fn main() { println!("{}", elsewhere::probe()); }
```
Expected output: `47`

*Check 6: edition 2021: `expr` does not match a const block, so the `const` arm wins* · `runs` · edition 2021 · host · **✔ oracle pass**
```rust
macro_rules! example {
    ($e:expr) => { println!("first rule"); };
    (const $e:expr) => { println!("second rule"); };
}
fn main() { example!(const { 1 + 1 }); }
```
Expected output: `second rule`

*Check 7: edition 2024: the same macro now matches `expr` first* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
macro_rules! example {
    ($e:expr) => { println!("first rule"); };
    (const $e:expr) => { println!("second rule"); };
}
fn main() { example!(const { 1 + 1 }); }
```
Expected output: `first rule`

*Check 8: edition 2024: expr_2021 keeps the 2021 matching* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
macro_rules! example {
    ($e:expr_2021) => { println!("first rule"); };
    (const $e:expr_2021) => { println!("second rule"); };
}
fn main() { example!(const { 1 + 1 }); }
```
Expected output: `second rule`

*Check 9: edition 2021: `_` is not an expr fragment (falls to tt)* · `runs` · edition 2021 · host · **✔ oracle pass**
```rust
macro_rules! m {
    ($e:expr) => { "expr" };
    ($t:tt) => { "tt" };
}
fn main() { println!("{}", m!(_)); }
```
Expected output: `tt`

*Check 10: edition 2024: `_` matches expr* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
macro_rules! m {
    ($e:expr) => { "expr" };
    ($t:tt) => { "tt" };
}
fn main() { println!("{}", m!(_)); }
```
Expected output: `expr`

*Check 11: the migration lint edition_2024_expr_fragment_specifier flags `expr` in a 2021 crate* · `runs` · edition 2021 · host · lints: edition_2024_expr_fragment_specifier · stderr has “use the `expr_2021` fragment specifier” · **✔ oracle pass**
```rust
#[warn(edition_2024_expr_fragment_specifier)]
macro_rules! m {
    ($e:expr) => { "expr" };
    ($t:tt) => { "tt" };
}
fn main() { println!("{}", m!(_)); }
```
Expected output: `tt`

## Pin the solver ABI with const _ assertions and generate the JS strides from one Rust table, not by hand
**`const _: () = { ... }` blocks, offset_of! (1.77) and size_of turn layout and slot invariants into E0080 build failures that add no bytes when appended; a macro_rules! table can emit the consts, the proof and one exported descriptor so JS never retypes 17 or 10.**

*Check 1: a const proof that slots 0..16 are each used once, plus repr(C) size and offset_of! checks* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
pub const BODY_STRIDE: usize = 17;
pub const QX: usize = 6;
pub const QY: usize = 7;
pub const QZ: usize = 8;
pub const QW: usize = 9;
pub const WX: usize = 10;
pub const WY: usize = 11;
pub const WZ: usize = 12;
pub const HX: usize = 13;
pub const HY: usize = 14;
pub const HZ: usize = 15;
pub const DRIVEN: usize = 16;
// Every slot of the 17-f64 body record, named or literal, exactly once.
const SLOTS: [usize; BODY_STRIDE] = [0, 1, 2, 3, 4, 5, QX, QY, QZ, QW, WX, WY, WZ, HX, HY, HZ, DRIVEN];
const _: () = {
    let mut i = 0;
    while i < SLOTS.len() {
        assert!(SLOTS[i] < BODY_STRIDE, "ABI slot outside the body stride");
        let mut j = i + 1;
        while j < SLOTS.len() {
            assert!(SLOTS[i] != SLOTS[j], "two ABI slots share an index");
            j += 1;
        }
        i += 1;
    }
};
#[repr(C)]
pub struct Body { pos: [f64; 3], vel: [f64; 3], rot: [f64; 4], ang: [f64; 3], half: [f64; 3], driven: f64 }
const _: () = assert!(core::mem::size_of::<Body>() == BODY_STRIDE * core::mem::size_of::<f64>());
const _: () = assert!(core::mem::offset_of!(Body, rot) == QX * 8);
const _: () = assert!(core::mem::offset_of!(Body, half) == HX * 8);
const _: () = assert!(core::mem::offset_of!(Body, driven) == DRIVEN * 8);
fn main() { println!("ok {} {}", core::mem::size_of::<Body>(), SLOTS.len()); }
```
Expected output: `ok 136 17`

*Check 2: two slots on one index (DRIVEN = HZ) stop the build with E0080* · `compile_fail` · edition 2024 · host · errors: E0080 · stderr has “two ABI slots share an index” · **✔ oracle pass**
```rust
pub const BODY_STRIDE: usize = 17;
pub const QX: usize = 6;
pub const QY: usize = 7;
pub const QZ: usize = 8;
pub const QW: usize = 9;
pub const WX: usize = 10;
pub const WY: usize = 11;
pub const WZ: usize = 12;
pub const HX: usize = 13;
pub const HY: usize = 14;
pub const HZ: usize = 15;
pub const DRIVEN: usize = 15;
// Every slot of the 17-f64 body record, named or literal, exactly once.
const SLOTS: [usize; BODY_STRIDE] = [0, 1, 2, 3, 4, 5, QX, QY, QZ, QW, WX, WY, WZ, HX, HY, HZ, DRIVEN];
const _: () = {
    let mut i = 0;
    while i < SLOTS.len() {
        assert!(SLOTS[i] < BODY_STRIDE, "ABI slot outside the body stride");
        let mut j = i + 1;
        while j < SLOTS.len() {
            assert!(SLOTS[i] != SLOTS[j], "two ABI slots share an index");
            j += 1;
        }
        i += 1;
    }
};
#[repr(C)]
pub struct Body { pos: [f64; 3], vel: [f64; 3], rot: [f64; 4], ang: [f64; 3], half: [f64; 3], driven: f64 }
const _: () = assert!(core::mem::size_of::<Body>() == BODY_STRIDE * core::mem::size_of::<f64>());
const _: () = assert!(core::mem::offset_of!(Body, rot) == QX * 8);
const _: () = assert!(core::mem::offset_of!(Body, half) == HX * 8);
const _: () = assert!(core::mem::offset_of!(Body, driven) == DRIVEN * 8);
fn main() { println!("ok {} {}", core::mem::size_of::<Body>(), SLOTS.len()); }
```

*Check 3: one macro table emits consts, the proof and an exported descriptor (wasm: word 0 = 17)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · exports abi_word, bodies_ptr, memory · node calls abi_word(0) · **✔ oracle pass**
```rust
macro_rules! abi_layout {
    ($stride:ident = $n:literal; $( $name:ident = $slot:literal ),+ $(,)?) => {
        pub const $stride: usize = $n;
        $( pub const $name: usize = $slot; )+
        const _: () = {
            let slots = [$( $slot ),+];
            let mut i = 0;
            while i < slots.len() {
                assert!(slots[i] < $n, "slot outside the stride");
                let mut j = i + 1;
                while j < slots.len() { assert!(slots[i] != slots[j], "two slots share an index"); j += 1; }
                i += 1;
            }
        };
        /// [stride, slots...] in declaration order, for the JS glue to read instead of typing 17.
        static ABI_WORDS: &[u32] = &[$n, $( $slot ),+];
        #[unsafe(no_mangle)]
        pub extern "C" fn abi_word(i: u32) -> u32 {
            match ABI_WORDS.get(i as usize) { Some(w) => *w, None => u32::MAX }
        }
    };
}
abi_layout! { BODY_STRIDE = 17; HX = 13, HY = 14, HZ = 15, DRIVEN = 16 }
static mut BODIES: [f64; 64 * BODY_STRIDE] = [0.0; 64 * BODY_STRIDE];
#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 { (&raw mut BODIES).cast() }
```
Expected output: `17`

*Check 4: the same table with a slot equal to the stride fails in the macro's proof (E0080)* · `compile_fail` · edition 2024 · host · lib · errors: E0080 · stderr has “slot outside the stride” · **✔ oracle pass**
```rust
macro_rules! abi_layout {
    ($stride:ident = $n:literal; $( $name:ident = $slot:literal ),+ $(,)?) => {
        pub const $stride: usize = $n;
        $( pub const $name: usize = $slot; )+
        const _: () = {
            let slots = [$( $slot ),+];
            let mut i = 0;
            while i < slots.len() {
                assert!(slots[i] < $n, "slot outside the stride");
                let mut j = i + 1;
                while j < slots.len() { assert!(slots[i] != slots[j], "two slots share an index"); j += 1; }
                i += 1;
            }
        };
        /// [stride, slots...] in declaration order, for the JS glue to read instead of typing 17.
        static ABI_WORDS: &[u32] = &[$n, $( $slot ),+];
        #[unsafe(no_mangle)]
        pub extern "C" fn abi_word(i: u32) -> u32 {
            match ABI_WORDS.get(i as usize) { Some(w) => *w, None => u32::MAX }
        }
    };
}
abi_layout! { BODY_STRIDE = 17; HX = 13, HY = 14, HZ = 17, DRIVEN = 16 }
```

*Check 5: a free const _ is evaluated even inside an unused generic function (E0080)* · `compile_fail` · edition 2024 · host · errors: E0080 · **✔ oracle pass**
```rust
#[allow(dead_code)]
fn unused_generic_function<T>() {
    const _: () = assert!(usize::BITS == 0);
}
fn main() {}
```

