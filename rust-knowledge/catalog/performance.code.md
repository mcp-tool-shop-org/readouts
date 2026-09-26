# Performance & profiling — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](performance.md) · [catalog index](README.md)

## Benchmark before tuning: criterion or divan with harness = false, black_box on every input and output
**Stable Rust has no built-in bench harness (#[bench] is nightly-only), so time work with criterion 0.8 or divan 0.1 under [[bench]] harness = false and route inputs and results through std::hint::black_box so the optimizer cannot fold the measured work away.**

*Check 1: black_box on input and output: the bench loop compiles at -O and computes the same value* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;

// One unit of work on a 17-slot row: the thing a benchmark should time.
fn quantum(row: &mut [f64; 17]) {
    for x in row.iter_mut() {
        *x = *x * 0.5 + 1.0;
    }
}

fn main() {
    let mut row = [0.0f64; 17];
    for _ in 0..64 {
        // Input through black_box: the optimizer may not assume what `row` holds.
        quantum(black_box(&mut row));
    }
    // Output through black_box: the work may not be deleted as unused.
    let out = black_box(row[16]);
    println!("{out}");
}
```
Expected output: `2`

*Check 2: black_box is usable in a const item on 1.98.1 (const-stable since 1.86)* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub const K: u32 = std::hint::black_box(7);
```

*Check 3: the libtest #[bench] harness needs #![feature(test)], which stable rejects with E0554* · `compile_fail` · edition 2024 · host · lib · errors: E0554 · **✔ oracle pass**
```rust
#![feature(test)]
extern crate test;

#[bench]
fn bench_step(b: &mut test::Bencher) {
    b.iter(|| 1 + 1);
}
```

## Choose release-profile knobs by measurement: opt-level sets speed; lto, codegen-units, strip, debug move bytes
**Measured on a scratch copy of the solver (wasm32, V8): only opt-level changed speed materially (s 1.69x, z 2.73x, 0 30x slower); lto, codegen-units, debug, strip and panic moved size between -12% and +634% within run-to-run noise on speed. Cargo's lto = false is thin-local LTO, a no-op at codegen-units = 1, and release strips debuginfo by default.**

*Check 1: the host target defaults to unwinding* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
fn main() {
    println!("{}", if cfg!(panic = "abort") { "abort" } else { "unwind" });
}
```
Expected output: `unwind`

*Check 2: -C panic=abort switches the strategy the code is compiled for* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
fn main() {
    println!("{}", if cfg!(panic = "abort") { "abort" } else { "unwind" });
}
```
Expected output: `abort`

*Check 3: wasm32-unknown-unknown already compiles with panic=abort, no flag given* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls panic_is_abort() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn panic_is_abort() -> u32 {
    cfg!(panic = "abort") as u32
}
```
Expected output: `1`

*Check 4: rustc -C opt-level=0 turns on cfg(debug_assertions)* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
fn main() {
    println!("{}", cfg!(debug_assertions));
}
```
Expected output: `true`

*Check 5: rustc -C opt-level=3 leaves cfg(debug_assertions) off* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
fn main() {
    println!("{}", cfg!(debug_assertions));
}
```
Expected output: `false`

## Get SIMD on stable from auto-vectorization, std::arch and #[target_feature]; std::simd is still nightly-only
**Once a SIMD feature is enabled, LLVM vectorizes elementwise loops and integer reductions but keeps float reductions in order; std::arch intrinsics are safe #[target_feature] functions that need `unsafe` unless the caller itself enables the feature (on wasm they are always safe to call); std::simd (portable_simd) needs nightly.**

*Check 1: std::simd needs #![feature(portable_simd)]: E0554 on stable* · `compile_fail` · edition 2024 · host · lib · errors: E0554 · **✔ oracle pass**
```rust
#![feature(portable_simd)]
use std::simd::f64x2;

pub fn double(a: f64x2) -> f64x2 {
    a + a
}
```

*Check 2: a safe #[target_feature] fn called from a plain fn needs unsafe: E0133* · `compile_fail` · edition 2024 · host · lib · errors: E0133 · **✔ oracle pass**
```rust
#[target_feature(enable = "avx2")]
pub fn needs_avx2() -> u32 {
    2
}

pub fn caller() -> u32 {
    needs_avx2()
}
```

*Check 3: runtime detection + unsafe call is the portable x86 pattern* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
#[target_feature(enable = "avx2")]
fn sum4(xs: &[f64; 4]) -> f64 {
    xs.iter().sum()
}

fn sum4_dispatch(xs: &[f64; 4]) -> f64 {
    if is_x86_feature_detected!("avx2") {
        // SAFETY: the running CPU was just checked for AVX2.
        unsafe { sum4(xs) }
    } else {
        xs.iter().sum()
    }
}

fn main() {
    println!("{}", sum4_dispatch(&[1.0, 2.0, 3.0, 4.0]));
}
```
Expected output: `10`

*Check 4: an SSE2 intrinsic from a plain fn is E0133 even though sse2 is a default feature* · `compile_fail` · edition 2024 · host · lib · errors: E0133 · **✔ oracle pass**
```rust
use std::arch::x86_64::*;

pub fn add2(a: __m128d, b: __m128d) -> __m128d {
    _mm_add_pd(a, b)
}
```

*Check 5: the same intrinsic compiles without unsafe inside #[target_feature(enable = "sse2")]* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
use std::arch::x86_64::*;

#[target_feature(enable = "sse2")]
pub fn add2(a: __m128d, b: __m128d) -> __m128d {
    _mm_add_pd(a, b)
}
```

*Check 6: on wasm a safe simd128 #[target_feature] fn is callable from a plain fn* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls call_simd_fn_safely() · **✔ oracle pass**
```rust
#[target_feature(enable = "simd128")]
fn lanes() -> u32 {
    2
}

#[unsafe(no_mangle)]
pub extern "C" fn call_simd_fn_safely() -> u32 {
    lanes()
}

#[unsafe(no_mangle)]
pub extern "C" fn simd128_on() -> u32 {
    cfg!(target_feature = "simd128") as u32
}
```
Expected output: `2`

*Check 7: simd128 is off by default on wasm32-unknown-unknown (1.98.1)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls simd128_on() · **✔ oracle pass**
```rust
#[target_feature(enable = "simd128")]
fn lanes() -> u32 {
    2
}

#[unsafe(no_mangle)]
pub extern "C" fn call_simd_fn_safely() -> u32 {
    lanes()
}

#[unsafe(no_mangle)]
pub extern "C" fn simd128_on() -> u32 {
    cfg!(target_feature = "simd128") as u32
}
```
Expected output: `0`

*Check 8: -C target-feature=+simd128 turns it on for the whole crate* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls simd128_on() · **✔ oracle pass**
```rust
#[target_feature(enable = "simd128")]
fn lanes() -> u32 {
    2
}

#[unsafe(no_mangle)]
pub extern "C" fn call_simd_fn_safely() -> u32 {
    lanes()
}

#[unsafe(no_mangle)]
pub extern "C" fn simd128_on() -> u32 {
    cfg!(target_feature = "simd128") as u32
}
```
Expected output: `1`

## Keep target-cpu=native, PGO and BOLT out of the pinned artifact: they tie codegen to a machine or a profile
**target-cpu=native targets 'the processor of the host machine' and turns on its features (38 instead of 5 on this rig), which flips any cfg(target_feature) path such as wide 1.7.1's fused mul_add; for wasm32, rustc 1.98.1 ignores it with warnings. PGO bytes depend on a training run and cannot even be instrumented for wasm32-unknown-unknown (E0463 profiler_builtins); BOLT rewrites only x86-64 and AArch64 ELF.**

*Check 1: default host features: the cfg(fma) branch takes the unfused path and prints 0* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;

// The pattern SIMD libraries use: a fused path only when the target feature is on.
#[inline]
fn madd(a: f64, b: f64, c: f64) -> f64 {
    if cfg!(target_feature = "fma") { a.mul_add(b, c) } else { a * b + c }
}

fn main() {
    let a = black_box(f64::from_bits(0x3FF0_0000_0200_0000)); // 1 + 2^-27
    let c = black_box(f64::from_bits(0xBFF0_0000_0400_0000)); // -(1 + 2^-26)
    println!("fma={} madd={:e} plain={:e}", cfg!(target_feature = "fma"), madd(a, a, c), a * a + c);
}
```
Expected output: `fma=false madd=0e0 plain=0e0`

*Check 2: +fma flips the same source to the fused path (2^-54); plain a*b+c still prints 0* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;

// The pattern SIMD libraries use: a fused path only when the target feature is on.
#[inline]
fn madd(a: f64, b: f64, c: f64) -> f64 {
    if cfg!(target_feature = "fma") { a.mul_add(b, c) } else { a * b + c }
}

fn main() {
    let a = black_box(f64::from_bits(0x3FF0_0000_0200_0000)); // 1 + 2^-27
    let c = black_box(f64::from_bits(0xBFF0_0000_0400_0000)); // -(1 + 2^-26)
    println!("fma={} madd={:e} plain={:e}", cfg!(target_feature = "fma"), madd(a, a, c), a * a + c);
}
```
Expected output: `fma=true madd=5.551115123125783e-17 plain=0e0`

## Lay out hot data by access: struct-of-arrays when loops read few fields, rows sized against cache lines
**Struct-of-arrays lets a loop load only the fields it reads; array-of-structs keeps one element's fields together; either way the sizes come from size_of / align_of and #[repr(align(N))], and cache-line sizes are per-architecture guesses (crossbeam assumes 128 bytes on x86_64 and aarch64, 64 on most others).**

*Check 1: a 17-slot f64 row is 136 bytes, the body buffer 8,704; repr(align(64)) makes a 64-byte line* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::mem::{align_of, size_of};

#[repr(align(64))]
struct Line([f64; 8]);

fn main() {
    println!("{} {} {} {} {}", size_of::<[f64; 17]>(), align_of::<[f64; 17]>(), size_of::<[f64; 64 * 17]>(), size_of::<Line>(), align_of::<Line>());
}
```
Expected output: `136 8 8704 64 64`

*Check 2: repr(align) must be a power of two: E0589* · `compile_fail` · edition 2024 · host · lib · errors: E0589 · **✔ oracle pass**
```rust
#[repr(align(3))]
pub struct Row(u8);
```

*Check 3: packed and align cannot be combined: E0587* · `compile_fail` · edition 2024 · host · lib · errors: E0587 · **✔ oracle pass**
```rust
#[repr(packed, align(8))]
pub struct Row(u8);
```

## Leave inlining to rustc: #[inline] for cross-crate calls, #[cold] on refusal paths, static dispatch when hot
**Every #[inline] form is a hint the compiler may ignore; since 1.75 rustc makes small leaf functions cross-crate-inlinable by itself; #[cold] marks unlikely paths; generics are monomorphized into static calls while dyn Trait calls go through a vtable that blocks inlining.**

*Check 1: #[inline] belongs on functions: on a struct 1.98.1 rejects it with a message and no error code* · `compile_fail` · edition 2024 · host · lib · stderr has “`#[inline]` attribute cannot be used on structs” · **✔ oracle pass**
```rust
#[inline]
pub struct Body;
```

*Check 2: generic, dyn and enum dispatch compute the same total; &dyn is a two-word fat pointer* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::mem::size_of;

trait Shape {
    fn volume(&self) -> f64;
}

struct Cuboid {
    hx: f64,
    hy: f64,
    hz: f64,
}

impl Shape for Cuboid {
    fn volume(&self) -> f64 {
        8.0 * self.hx * self.hy * self.hz
    }
}

enum Kind {
    Cuboid(Cuboid),
}

// Static dispatch: monomorphized per S, the call can inline.
fn total_static<S: Shape>(xs: &[S]) -> f64 {
    xs.iter().map(|s| s.volume()).sum()
}

// Dynamic dispatch: each call goes through the vtable in the fat pointer.
fn total_dyn(xs: &[Box<dyn Shape>]) -> f64 {
    xs.iter().map(|s| s.volume()).sum()
}

// A closed set: enum + match is static dispatch without generics.
fn total_enum(xs: &[Kind]) -> f64 {
    xs.iter().map(|k| match k { Kind::Cuboid(c) => c.volume() }).sum()
}

fn main() {
    let c = || Cuboid { hx: 0.5, hy: 0.5, hz: 0.5 };
    let a = [c(), c(), c()];
    let b: Vec<Box<dyn Shape>> = vec![Box::new(c()), Box::new(c()), Box::new(c())];
    let e = [Kind::Cuboid(c()), Kind::Cuboid(c()), Kind::Cuboid(c())];
    println!("{} {} {} {} {}", total_static(&a), total_dyn(&b), total_enum(&e), size_of::<&dyn Shape>(), size_of::<&Cuboid>());
}
```
Expected output: `3 3 3 16 8`

*Check 3: hot path #[inline] + #[cold] #[inline(never)] refusal path compiles cleanly* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
/// Hot path: small, inlined into callers.
#[inline]
pub fn admit(n: u32, max: u32) -> Result<u32, u32> {
    if n <= max { Ok(n) } else { refuse(n) }
}

/// Cold path: rarely taken, kept out of line so the hot path stays small.
#[cold]
#[inline(never)]
fn refuse(n: u32) -> Result<u32, u32> {
    Err(n)
}
```

## Prove indices once: an entry guard, chunks_exact_mut or as_chunks_mut removes per-iteration bounds checks
**Measured in LLVM IR at opt-level 3: LLVM already hoists the check out of a loop without stores, but a read-modify-write loop keeps one check per iteration; chunks_exact_mut and as_chunks_mut (1.88) leave none, and in the solver the early `n_bodies > MAX_BODIES` return is what removes all 30 checks from the box law's step.**

*Check 1: as_chunks gives 64 rows of 17 and no remainder; chunks_exact leaves a tail; get() returns None* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
fn main() {
    let buf = vec![0.0f64; 64 * 17];
    let (rows, rest) = buf.as_chunks::<17>();
    let short = [1.0f64; 40];
    let it = short.chunks_exact(17);
    println!("{} {} {} {} {:?}", rows.len(), rest.len(), it.len(), it.remainder().len(), short.get(40));
}
```
Expected output: `64 0 2 6 None`

*Check 2: the solver's shape: guard first, then fixed rows via as_chunks_mut; 65 bodies is refused* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
const MAX_BODIES: usize = 64;
const STRIDE: usize = 17;
const DT: f64 = 1.0 / 64.0;

// Guard first, then index a fixed-length buffer through [f64; STRIDE] rows.
fn step(bodies: &mut [f64; MAX_BODIES * STRIDE], n_bodies: u32) -> u32 {
    if n_bodies as usize > MAX_BODIES {
        return 0;
    }
    let n = n_bodies as usize;
    let (rows, _) = bodies.as_chunks_mut::<STRIDE>();
    for row in rows.iter_mut().take(n) {
        row[4] = row[4] - 8.0 * DT;
        row[1] = row[1] + row[4] * DT;
    }
    1
}

fn main() {
    let mut bodies = [0.0f64; MAX_BODIES * STRIDE];
    let ok = step(&mut bodies, 64);
    let refused = step(&mut bodies, 65);
    println!("{} {} {} {}", ok, refused, bodies[4], bodies[63 * STRIDE + 1]);
}
```
Expected output: `1 0 -0.125 -0.001953125`

*Check 3: an index the compiler cannot prove in range is still checked at run time: exit 101* · `runs` · edition 2024 · host · exit code 101 · **✔ oracle pass**
```rust
use std::hint::black_box;

fn main() {
    let v = vec![0.0f64; 17];
    let i = black_box(17usize);
    println!("{}", v[i]);
}
```

## Reuse per-quantum buffers: clear() keeps capacity, with_capacity sizes once, SmallVec/ArrayVec for small lists
**Vec never shrinks on its own, and refilling a cleared Vec to the same length 'should incur no calls to the allocator', so a buffer cleared each quantum stops allocating once it reaches its peak; SmallVec keeps up to N items inline and spills to the heap; ArrayVec has a hard capacity and never allocates.**

*Check 1: clear() keeps capacity and the buffer address across 100 refills below capacity* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
fn main() {
    let mut snapshot: Vec<u8> = Vec::with_capacity(4096);
    let (cap0, ptr0) = (snapshot.capacity(), snapshot.as_ptr());
    let mut peak = 0;
    for quantum in 0..100u32 {
        snapshot.clear(); // len = 0, capacity kept
        for k in 0..(quantum % 64) {
            snapshot.extend_from_slice(&(k as f64).to_le_bytes());
        }
        peak = peak.max(snapshot.len());
    }
    println!("{} {} {} {}", cap0 >= 4096, snapshot.capacity() == cap0, snapshot.as_ptr() == ptr0, peak);
}
```
Expected output: `true true true 504`

*Check 2: SmallVec spills on item N+1 and keeps its heap buffer after clear(); ArrayVec refuses past CAP* · `runs` · edition 2024 · host · deps: smallvec, arrayvec · **✔ oracle pass**
```rust
use arrayvec::ArrayVec;
use smallvec::SmallVec;

fn main() {
    let mut v: SmallVec<[u32; 4]> = SmallVec::new();
    for i in 0..4 {
        v.push(i);
    }
    let inline4 = !v.spilled();
    v.push(4);
    let spilled5 = v.spilled();
    let cap = v.capacity();
    v.clear();
    println!("{} {} {} {} {}", inline4, spilled5, v.spilled(), v.capacity() == cap, v.inline_size());
    let mut a: ArrayVec<u32, 4> = ArrayVec::new();
    for i in 0..4 {
        a.push(i);
    }
    let r = a.try_push(9);
    println!("{} {} {}", a.is_full(), r.is_err(), std::mem::size_of::<ArrayVec<u32, 4>>());
}
```
Expected output: `true true true true 4 true true 20`

*Check 3: with_capacity(1088) reports exactly 1088; one push past it grows the buffer* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
fn main() {
    let mut v: Vec<f64> = Vec::with_capacity(1088);
    let c0 = v.capacity();
    v.resize(1088, 0.0);
    let c1 = v.capacity();
    v.push(1.0);
    println!("{} {} {}", c0, c1, v.capacity() > 1088);
}
```
Expected output: `1088 1088 true`

## Split profile knobs into digest-only and result-changing before editing the solver's pinned release profile
**On a scratch copy of solver/, 15 profile variants all changed the wasm digest and even the code section, yet all gave byte-identical results over 400 quanta of both laws; knobs change results only through semantics: overflow-checks, debug-assertions, cfg(target_feature) paths, NaN bit patterns and std transcendentals.**

*Check 1: IEEE kernel at -C opt-level=0 prints these bits* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;

// Add, sub, mul, div and sqrt only: IEEE-exact at every optimization level.
fn main() {
    let dt = black_box(1.0f64 / 64.0);
    let (mut y, mut vy) = (black_box(3.0f64), black_box(0.0f64));
    let mut acc = 0.0f64;
    for i in 0..640 {
        vy = vy - 8.0 * dt;
        y = y + vy * dt;
        if y < 0.5 {
            y = 0.5 + (0.5 - y);
            vy = 0.0 - vy * 0.8;
        }
        acc = acc + (y * y + vy * vy).sqrt() / (i as f64 + 1.0);
    }
    println!("{:016x} {:016x} {:016x} {}", y.to_bits(), vy.to_bits(), acc.to_bits(), acc);
}
```
Expected output: `3fe01580a0938479 bfb32acb97a48626 4034df7d77a90ec0 20.873008230947335`

*Check 2: same kernel at -C opt-level=3, one codegen unit: identical bits* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;

// Add, sub, mul, div and sqrt only: IEEE-exact at every optimization level.
fn main() {
    let dt = black_box(1.0f64 / 64.0);
    let (mut y, mut vy) = (black_box(3.0f64), black_box(0.0f64));
    let mut acc = 0.0f64;
    for i in 0..640 {
        vy = vy - 8.0 * dt;
        y = y + vy * dt;
        if y < 0.5 {
            y = 0.5 + (0.5 - y);
            vy = 0.0 - vy * 0.8;
        }
        acc = acc + (y * y + vy * vy).sqrt() / (i as f64 + 1.0);
    }
    println!("{:016x} {:016x} {:016x} {}", y.to_bits(), vy.to_bits(), acc.to_bits(), acc);
}
```
Expected output: `3fe01580a0938479 bfb32acb97a48626 4034df7d77a90ec0 20.873008230947335`

*Check 3: same kernel at -C opt-level=z with fat LTO: identical bits* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;

// Add, sub, mul, div and sqrt only: IEEE-exact at every optimization level.
fn main() {
    let dt = black_box(1.0f64 / 64.0);
    let (mut y, mut vy) = (black_box(3.0f64), black_box(0.0f64));
    let mut acc = 0.0f64;
    for i in 0..640 {
        vy = vy - 8.0 * dt;
        y = y + vy * dt;
        if y < 0.5 {
            y = 0.5 + (0.5 - y);
            vy = 0.0 - vy * 0.8;
        }
        acc = acc + (y * y + vy * vy).sqrt() / (i as f64 + 1.0);
    }
    println!("{:016x} {:016x} {:016x} {}", y.to_bits(), vy.to_bits(), acc.to_bits(), acc);
}
```
Expected output: `3fe01580a0938479 bfb32acb97a48626 4034df7d77a90ec0 20.873008230947335`

*Check 4: same kernel at -C opt-level=s with 16 codegen units: identical bits* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;

// Add, sub, mul, div and sqrt only: IEEE-exact at every optimization level.
fn main() {
    let dt = black_box(1.0f64 / 64.0);
    let (mut y, mut vy) = (black_box(3.0f64), black_box(0.0f64));
    let mut acc = 0.0f64;
    for i in 0..640 {
        vy = vy - 8.0 * dt;
        y = y + vy * dt;
        if y < 0.5 {
            y = 0.5 + (0.5 - y);
            vy = 0.0 - vy * 0.8;
        }
        acc = acc + (y * y + vy * vy).sqrt() / (i as f64 + 1.0);
    }
    println!("{:016x} {:016x} {:016x} {}", y.to_bits(), vy.to_bits(), acc.to_bits(), acc);
}
```
Expected output: `3fe01580a0938479 bfb32acb97a48626 4034df7d77a90ec0 20.873008230947335`

*Check 5: the kernel compiled to wasm32 at opt-level 0 returns the host's value* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls kernel_acc() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn kernel_acc() -> f64 {
    let dt = core::hint::black_box(1.0f64 / 64.0);
    let (mut y, mut vy) = (core::hint::black_box(3.0f64), core::hint::black_box(0.0f64));
    let mut acc = 0.0f64;
    for i in 0..640 {
        vy = vy - 8.0 * dt;
        y = y + vy * dt;
        if y < 0.5 {
            y = 0.5 + (0.5 - y);
            vy = 0.0 - vy * 0.8;
        }
        acc = acc + (y * y + vy * vy).sqrt() / (i as f64 + 1.0);
    }
    acc
}
```
Expected output: `20.873008230947335`

*Check 6: the kernel compiled to wasm32 at opt-level 3 returns the same value* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls kernel_acc() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn kernel_acc() -> f64 {
    let dt = core::hint::black_box(1.0f64 / 64.0);
    let (mut y, mut vy) = (core::hint::black_box(3.0f64), core::hint::black_box(0.0f64));
    let mut acc = 0.0f64;
    for i in 0..640 {
        vy = vy - 8.0 * dt;
        y = y + vy * dt;
        if y < 0.5 {
            y = 0.5 + (0.5 - y);
            vy = 0.0 - vy * 0.8;
        }
        acc = acc + (y * y + vy * vy).sqrt() / (i as f64 + 1.0);
    }
    acc
}
```
Expected output: `20.873008230947335`

*Check 7: overflow-checks on: 255u8 + 1 panics (exit 101) after printing 'before'* · `runs` · edition 2024 · host · exit code 101 · **✔ oracle pass**
```rust
use std::hint::black_box;

fn main() {
    let x: u8 = black_box(255);
    println!("before");
    let y = x + 1;
    println!("{y}");
}
```
Expected output: `before`

*Check 8: overflow-checks off: the same program wraps to 0 and continues* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;

fn main() {
    let x: u8 = black_box(255);
    println!("before");
    let y = x + 1;
    println!("{y}");
}
```
Expected output: `before 0`

*Check 9: wrapping_mul/wrapping_add (the law's mix_u64) are unaffected by overflow-checks=on* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;

fn mix_u64(h: u64, x: u64) -> u64 {
    h.wrapping_mul(0x100000001b3).wrapping_add(x)
}

fn main() {
    let h = black_box(0xcbf29ce484222325u64);
    println!("{:016x}", mix_u64(h, black_box(u64::MAX)));
}
```
Expected output: `af63bd4c8601b7de`

*Check 10: debug-assertions on: a failing debug_assert! panics (exit 101)* · `runs` · edition 2024 · host · exit code 101 · **✔ oracle pass**
```rust
use std::hint::black_box;

fn main() {
    println!("start");
    debug_assert!(black_box(1) == 2, "a debug-only invariant");
    println!("ran");
}
```
Expected output: `start`

*Check 11: debug-assertions off: the same program runs past the assertion* · `runs` · edition 2024 · host · **✔ oracle pass**
```rust
use std::hint::black_box;

fn main() {
    println!("start");
    debug_assert!(black_box(1) == 2, "a debug-only invariant");
    println!("ran");
}
```
Expected output: `start ran`

