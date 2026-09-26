# Floating point & cross-platform determinism — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](float-determinism.md) · [catalog index](README.md)

## Build hashed math from f64 + - * / and sqrt: the same bits on IEEE CPUs, wasm engines and in const eval
**The IEEE 754 basic operations (+, -, *, /, sqrt) are correctly rounded (round to nearest, ties to even) in Rust and in WebAssembly, neither flushes subnormals, and rustc's const evaluator computes them in a host-independent soft-float, so a computation built only from them has one bit pattern natively, in every wasm engine and at compile time; only NaN bit patterns may differ.**

*Check 1: 100k-step +-*/sqrt chain with subnormals: digest on x86-64 at -O0* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
fn chain(n: u32, a0: f64, b0: f64) -> (u64, u32) {
    let (mut a, mut b) = (a0, b0);
    let mut h: u64 = 0xcbf29ce484222325;
    let mut subnormal_steps = 0u32;
    let tiny = f64::MIN_POSITIVE / 1024.0;
    let mut i = 0u32;
    while i < n {
        // Only + - * / and sqrt (abs is a bit operation).
        a = (a * 1.000_000_1 + b / 3.0).abs().sqrt() - 0.25;
        b = b * 0.999_9 - a / 7.0;
        let s = a * 1.0e-310 / 3.0 + tiny * (i % 5) as f64; // lands in the subnormal range
        if s.is_subnormal() {
            subnormal_steps += 1;
        }
        h = (h ^ a.to_bits()).wrapping_mul(0x100000001b3);
        h = (h ^ b.to_bits()).wrapping_mul(0x100000001b3);
        h = (h ^ s.to_bits()).wrapping_mul(0x100000001b3);
        i += 1;
    }
    (h, subnormal_steps)
}

fn main() {
    use std::hint::black_box;
    let (h, s) = chain(black_box(100_000), black_box(2.0), black_box(0.25));
    println!("{} subnormal_steps={}", h as i64, s);
}
```
Expected output: `7853152472807335572 subnormal_steps=100000`

*Check 2: the same chain at -O: optimisation does not change a single bit* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
fn chain(n: u32, a0: f64, b0: f64) -> (u64, u32) {
    let (mut a, mut b) = (a0, b0);
    let mut h: u64 = 0xcbf29ce484222325;
    let mut subnormal_steps = 0u32;
    let tiny = f64::MIN_POSITIVE / 1024.0;
    let mut i = 0u32;
    while i < n {
        // Only + - * / and sqrt (abs is a bit operation).
        a = (a * 1.000_000_1 + b / 3.0).abs().sqrt() - 0.25;
        b = b * 0.999_9 - a / 7.0;
        let s = a * 1.0e-310 / 3.0 + tiny * (i % 5) as f64; // lands in the subnormal range
        if s.is_subnormal() {
            subnormal_steps += 1;
        }
        h = (h ^ a.to_bits()).wrapping_mul(0x100000001b3);
        h = (h ^ b.to_bits()).wrapping_mul(0x100000001b3);
        h = (h ^ s.to_bits()).wrapping_mul(0x100000001b3);
        i += 1;
    }
    (h, subnormal_steps)
}

fn main() {
    use std::hint::black_box;
    let (h, s) = chain(black_box(100_000), black_box(2.0), black_box(0.25));
    println!("{} subnormal_steps={}", h as i64, s);
}
```
Expected output: `7853152472807335572 subnormal_steps=100000`

*Check 3: the same chain computed in wasm32 under node's V8 returns the same digest* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, chain_bits · imports nothing · node calls chain_bits(100000, 2.0, 0.25) · **✔ oracle pass**
```rust
fn chain(n: u32, a0: f64, b0: f64) -> (u64, u32) {
    let (mut a, mut b) = (a0, b0);
    let mut h: u64 = 0xcbf29ce484222325;
    let mut subnormal_steps = 0u32;
    let tiny = f64::MIN_POSITIVE / 1024.0;
    let mut i = 0u32;
    while i < n {
        // Only + - * / and sqrt (abs is a bit operation).
        a = (a * 1.000_000_1 + b / 3.0).abs().sqrt() - 0.25;
        b = b * 0.999_9 - a / 7.0;
        let s = a * 1.0e-310 / 3.0 + tiny * (i % 5) as f64; // lands in the subnormal range
        if s.is_subnormal() {
            subnormal_steps += 1;
        }
        h = (h ^ a.to_bits()).wrapping_mul(0x100000001b3);
        h = (h ^ b.to_bits()).wrapping_mul(0x100000001b3);
        h = (h ^ s.to_bits()).wrapping_mul(0x100000001b3);
        i += 1;
    }
    (h, subnormal_steps)
}

#[no_mangle]
pub extern "C" fn chain_bits(n: u32, a0: f64, b0: f64) -> i64 {
    chain(n, a0, b0).0 as i64
}
```
Expected output: `7853152472807335572`

*Check 4: f64::MIN_POSITIVE / 2 stays subnormal and doubles back exactly (no flush-to-zero)* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;
fn main() {
    let m = black_box(f64::MIN_POSITIVE);
    let h = m / 2.0;
    println!("{:016x} subnormal={} x2 {:016x} back={}", h.to_bits(), h.is_subnormal(), (h * 2.0).to_bits(), h * 2.0 == m);
}
```
Expected output: `0008000000000000 subnormal=true x2 0010000000000000 back=true`

*Check 5: wasm keeps the subnormal: MIN_POSITIVE / 2 = 1.1125369292536007e-308, not 0* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, half · node calls half(2.2250738585072014e-308) · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn half(x: f64) -> f64 {
    x / 2.0
}
```
Expected output: `1.1125369292536007e-308`

*Check 6: const-evaluated SLIDE_ANGLE and mul_add equal their run-time bits; deg(45) == FRAC_PI_4* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::f64::consts::{FRAC_PI_4, PI};
use std::hint::black_box;

// The two angles of si-rpg-engine solver/src/rapier_law.rs, evaluated by rustc.
const CLIMB_ANGLE: f64 = FRAC_PI_4;
const SLIDE_ANGLE: f64 = 50.0 * PI / 180.0;
// mul_add is const-stable since 1.94: rustc's evaluator rounds it once too.
const FMA: f64 = (1.0 + f64::EPSILON).mul_add(1.0 - f64::EPSILON, -1.0);
const fn deg(x: f64) -> f64 {
    x * PI / 180.0
}
const DEG45: f64 = deg(45.0);

fn main() {
    let rt = black_box(50.0) * black_box(PI) / black_box(180.0);
    println!("SLIDE_ANGLE const {:016x} = {} runtime {:016x}", SLIDE_ANGLE.to_bits(), SLIDE_ANGLE.to_bits() as i64, rt.to_bits());
    let f = black_box(1.0 + f64::EPSILON).mul_add(black_box(1.0 - f64::EPSILON), black_box(-1.0));
    println!("mul_add const {:e} runtime {:e}", FMA, f);
    println!("deg(45) {:016x} FRAC_PI_4 {:016x}", DEG45.to_bits(), CLIMB_ANGLE.to_bits());
}
```
Expected output: `SLIDE_ANGLE const 3febecde5da115a9 = 4606035483714196905 runtime 3febecde5da115a9 mul_add const -4.930380657631324e-32 runtime -4.930380657631324e-32 deg(45) 3fe921fb54442d18 FRAC_PI_4 3fe921fb54442d1`

*Check 7: 50 * PI / 180 computed at run time in wasm has the const's bits (4606035483714196905)* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, slide_runtime_bits · node calls slide_runtime_bits(50, 3.141592653589793, 180) · **✔ oracle pass**
```rust
// Computed by the wasm engine at call time, from arguments rustc cannot fold.
#[no_mangle]
pub extern "C" fn slide_runtime_bits(deg: f64, pi: f64, half_turn: f64) -> i64 {
    (deg * pi / half_turn).to_bits() as i64
}
```
Expected output: `4606035483714196905`

*Check 8: a transcendental in a const item is E0015: cos is not a const fn on 1.98.1* · `compile_fail` · edition 2021 · host · lib · errors: E0015 · **✔ oracle pass**
```rust
// Transcendentals are not const fn on 1.98.1.
pub const COS_CLIMB: f64 = (std::f64::consts::FRAC_PI_4).cos();
```

*Check 9: no_std on wasm32v1-none: f64::sqrt is not available on stable (E0599)* · `compile_fail` · edition 2021 · wasm32v1-none · lib · errors: E0599 · **✔ oracle pass**
```rust
#![no_std]
// On a no_std target f64's float-math methods are not available on stable.
pub fn speed(v2: f64) -> f64 {
    v2.sqrt()
}
```

## Canonicalize -0.0 to +0.0 before to_bits() feeds a hash: equal values, different bits
**`0.0 == -0.0` is true but their bits differ (0x0000000000000000 vs 0x8000000000000000), so a hash over `to_bits()` splits equal states; the sign survives the wasm-to-JS boundary, `total_cmp` orders -0.0 before +0.0, and min/max may return either zero on a tie.**

*Check 1: 0.0 == -0.0 yet bits differ; raw mix_f64 splits them, canon or +0.0 merges them* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;

// canon and mix_f64 as written in si-rpg-engine solver/src/rapier_law.rs.
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}
fn mix_f64(h: u64, x: f64) -> u64 {
    h.wrapping_mul(0x100000001b3).wrapping_add(x.to_bits())
}

fn main() {
    let (p, n) = (black_box(0.0f64), black_box(-0.0f64));
    println!("0.0 == -0.0: {}; bits {:016x} vs {:016x}", p == n, p.to_bits(), n.to_bits());
    let seed = 0xcbf29ce484222325u64;
    println!("raw mix differs: {}", mix_f64(seed, p) != mix_f64(seed, n));
    println!("canon(-0.0) {:016x}; -0.0 + 0.0 {:016x}", canon(n).to_bits(), (n + black_box(0.0)).to_bits());
    println!("canonical mix differs: {}", mix_f64(seed, canon(p)) != mix_f64(seed, canon(n)));
    println!("canon leaves NaN alone: {}", canon(f64::NAN).is_nan());
}
```
Expected output: `0.0 == -0.0: true; bits 0000000000000000 vs 8000000000000000 raw mix differs: true canon(-0.0) 0000000000000000; -0.0 + 0.0 0000000000000000 canonical mix differs: false canon leaves NaN alone: true`

*Check 2: the engine's canon_zero(-0.0) returns +0 to JS* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, canon_zero · node calls canon_zero(-0.0) · **✔ oracle pass**
```rust
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}
// As exported by si-rpg-engine solver/src/rapier_law.rs.
#[no_mangle]
pub extern "C" fn canon_zero(x: f64) -> f64 {
    if x.is_nan() { x } else { canon(x) }
}
#[no_mangle]
pub extern "C" fn ident(x: f64) -> f64 {
    x
}
```
Expected output: `0`

*Check 3: an identity export returns -0 to JS: the sign crosses the boundary* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, ident · node calls ident(-0.0) · **✔ oracle pass**
```rust
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}
// As exported by si-rpg-engine solver/src/rapier_law.rs.
#[no_mangle]
pub extern "C" fn canon_zero(x: f64) -> f64 {
    if x.is_nan() { x } else { canon(x) }
}
#[no_mangle]
pub extern "C" fn ident(x: f64) -> f64 {
    x
}
```
Expected output: `-0`

## Expect a*b+c to stay unfused: rustc never contracts, mul_add always rounds once, wasm has no scalar fma
**rustc never turns `a * b + c` into a fused multiply-add, not at -O and not with `-C target-feature=+fma`; `f64::mul_add` always rounds once, and on wasm32 it is a software fma compiled into the module (no import); wasm 3.0 has no scalar fma instruction, so hardware-chosen fusion can only enter through relaxed SIMD's relaxed_madd; the stable opt-in to contraction since 1.98.0 is the `algebraic_*` family.**

*Check 1: a*b+c prints 0 and mul_add prints -4.93e-32 at -O0 on x86-64* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;
fn main() {
    let a = black_box(1.0 + f64::EPSILON);
    let b = black_box(1.0 - f64::EPSILON);
    let c = black_box(-1.0);
    println!("unfused {:e} fused {:e}", a * b + c, a.mul_add(b, c));
}
```
Expected output: `unfused 0e0 fused -4.930380657631324e-32`

*Check 2: with -O and -C target-feature=+fma rustc still does not fuse a*b+c* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;
fn main() {
    let a = black_box(1.0 + f64::EPSILON);
    let b = black_box(1.0 - f64::EPSILON);
    let c = black_box(-1.0);
    println!("unfused {:e} fused {:e}", a * b + c, a.mul_add(b, c));
}
```
Expected output: `unfused 0e0 fused -4.930380657631324e-32`

*Check 3: wasm32 mul_add is fused in software inside the module: -4.93e-32 and no imports* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, fused · imports nothing · node calls fused(1.0000000000000002, 0.9999999999999998, -1) · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn fused(a: f64, b: f64, c: f64) -> f64 {
    a.mul_add(b, c)
}
#[no_mangle]
pub extern "C" fn unfused(a: f64, b: f64, c: f64) -> f64 {
    a * b + c
}
```
Expected output: `-4.930380657631324e-32`

*Check 4: wasm32 a*b+c stays two roundings: 0* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, unfused · node calls unfused(1.0000000000000002, 0.9999999999999998, -1) · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn fused(a: f64, b: f64, c: f64) -> f64 {
    a.mul_add(b, c)
}
#[no_mangle]
pub extern "C" fn unfused(a: f64, b: f64, c: f64) -> f64 {
    a * b + c
}
```
Expected output: `0`

*Check 5: algebraic_mul/algebraic_add compile on stable 1.98.1 with no feature gate and no warning* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
// Stable since 1.98.0, no feature gate: the compiler may reassociate and contract these.
pub fn dot3(a: [f64; 3], b: [f64; 3]) -> f64 {
    a[0].algebraic_mul(b[0])
        .algebraic_add(a[1].algebraic_mul(b[1]))
        .algebraic_add(a[2].algebraic_mul(b[2]))
}
```

## Gate toolchain and Cargo.lock bumps on goldens plus a libm canary; keep fixed-point for integer-exact parts
**Results move on a bump through three mechanisms, each measured here: a libm version changes an algorithm (rustc 1.98.1's in-tree hypot returns 0x4018842a6ab3fa86 where libm 0.2.16 returns ...85 for the same input), a dependency reorders a sum (floating-point addition is not associative), and codegen changes tie choices such as min/max of zeros. Fixed-point arithmetic removes the float-specific classes (reassociation, NaN, signed zero, platform libm) but not the need for a gate.**

*Check 1: reassociation moves bits; a reversed sum differs; Q32.32 integer sums do not* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;
fn main() {
    let (a, b, c) = (black_box(0.1f64), black_box(0.2f64), black_box(0.3f64));
    println!("(a+b)+c {:016x} a+(b+c) {:016x}", ((a + b) + c).to_bits(), (a + (b + c)).to_bits());
    let v: Vec<f64> = (1..=1000).map(|i| 1.0 / black_box(i as f64)).collect();
    let fwd: f64 = v.iter().sum();
    let rev: f64 = v.iter().rev().sum();
    println!("harmonic(1000) forward {:016x} reversed {:016x}", fwd.to_bits(), rev.to_bits());
    // Q32.32 in an i64: the representation behind fixed's I32F32 (FixedI64<U32>).
    let q: Vec<i64> = v.iter().map(|x| (x * 4294967296.0) as i64).collect();
    let qf: i64 = q.iter().sum();
    let qr: i64 = q.iter().rev().sum();
    println!("Q32.32 forward == reversed: {}", qf == qr);
}
```
Expected output: `(a+b)+c 3fe3333333333334 a+(b+c) 3fe3333333333333 harmonic(1000) forward 401df11f45f4e618 reversed 401df11f45f4e615 Q32.32 forward == reversed: true`

*Check 2: libm 0.2.16 hypot(5.854078790883641, 1.8152787006269886) bits* · `runs` · edition 2021 · host · bin · deps: libm · **✔ oracle pass**
```rust
fn main() {
    let h = libm::hypot(5.854078790883641, 1.8152787006269886);
    println!("libm 0.2.16 hypot {:016x} = {}", h.to_bits(), h.to_bits() as i64);
}
```
Expected output: `libm 0.2.16 hypot 4018842a6ab3fa85 = 4618586735582116485`

*Check 3: the toolchain's hypot on wasm32 returns the next double up for the same input* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, hypot_bits · node calls hypot_bits(5.854078790883641, 1.8152787006269886) · **✔ oracle pass**
```rust
// std's f64::hypot on wasm32-unknown-unknown comes from the toolchain's own libm copy.
#[no_mangle]
pub extern "C" fn hypot_bits(x: f64, y: f64) -> i64 {
    x.hypot(y).to_bits() as i64
}
```
Expected output: `4618586735582116486`

*Check 4: a libm canary test passes at the pinned version and would fail by name after a change* · `runs` · edition 2021 · host · test · deps: libm · output has “test libm_bits_are_pinned ... ok” · output has “test result: ok. 1 passed” · **✔ oracle pass**
```rust
// A canary: bits of the pinned libm (0.2.16) for inputs the law cares about. A Cargo.lock
// bump that changes an algorithm fails this test by name before any golden hash moves.
#[test]
fn libm_bits_are_pinned() {
    assert_eq!(libm::sin(0.5).to_bits(), 0x3fdeaee8744b05f0);
    assert_eq!(libm::hypot(5.854078790883641, 1.8152787006269886).to_bits(), 0x4018842a6ab3fa85);
}
```

## Hash only IndexMap, BTreeMap or sorted order: a fixed hasher does not fix HashMap order across targets
**std's HashMap is randomly seeded (SipHash 1-3 today) and iterates in arbitrary order; hashbrown 0.17.1's default is foldhash's randomly initialised RandomState; a fixed hasher fixes the seed, not the iteration order across targets: the same 1000 inserts into a std HashMap with a fixed FNV hasher iterate differently on x86-64 and in wasm32, while a BTreeMap iterates identically (and foldhash does not even promise equal hash values across platforms).**

*Check 1: two std RandomStates disagree; IndexMap keeps insert/remove order; BTreeMap keeps key order* · `runs` · edition 2021 · host · bin · deps: indexmap, xxhash_rust · **✔ oracle pass**
```rust
use indexmap::IndexMap;
use std::collections::BTreeMap;
use std::hash::{BuildHasher, RandomState};
use xxhash_rust::xxh3::Xxh3Builder;

fn main() {
    // std's default: every RandomState gets fresh random keys.
    let a = RandomState::new().hash_one(42u64);
    let b = RandomState::new().hash_one(42u64);
    println!("two RandomState hashes of 42 agree: {}", a == b);
    // IndexMap: order is the insert/remove sequence, whatever the hasher.
    let mut im: IndexMap<u32, &str, Xxh3Builder> = IndexMap::with_hasher(Xxh3Builder::new());
    for (k, v) in [(5, "e"), (1, "a"), (3, "c"), (4, "d")] {
        im.insert(k, v);
    }
    im.shift_remove(&1);
    let shifted: Vec<u32> = im.keys().copied().collect();
    im.swap_remove(&5);
    let swapped: Vec<u32> = im.keys().copied().collect();
    println!("IndexMap after shift_remove(1) {:?} after swap_remove(5) {:?}", shifted, swapped);
    // BTreeMap: order is key order.
    let bt: BTreeMap<u32, &str> = [(5, "e"), (1, "a"), (3, "c"), (4, "d")].into_iter().collect();
    println!("BTreeMap {:?}", bt.keys().collect::<Vec<_>>());
}
```
Expected output: `two RandomState hashes of 42 agree: false IndexMap after shift_remove(1) [5, 3, 4] after swap_remove(5) [4, 3] BTreeMap [1, 3, 4, 5]`

*Check 2: x86-64: iteration-order digests of HashMap(fixed FNV) and BTreeMap for 1000 inserts* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::collections::{BTreeMap, HashMap};
use std::hash::{BuildHasherDefault, Hasher};

// A fixed, seedless FNV-1a hasher: the hash of a u64 key is the same on every target.
#[derive(Default)]
struct Fnv(u64);
impl Hasher for Fnv {
    fn finish(&self) -> u64 {
        self.0
    }
    fn write(&mut self, bytes: &[u8]) {
        let mut h = if self.0 == 0 { 0xcbf29ce484222325 } else { self.0 };
        for b in bytes {
            h = (h ^ *b as u64).wrapping_mul(0x100000001b3);
        }
        self.0 = h;
    }
}

// Digest of the order in which a map yields the same 1000 inserts.
fn digest(values: impl Iterator<Item = u64>) -> i64 {
    let mut d: u64 = 0xcbf29ce484222325;
    for v in values {
        d = (d ^ v).wrapping_mul(0x100000001b3);
    }
    d as i64
}
fn hashmap_order(n: u64) -> i64 {
    let mut m: HashMap<u64, u64, BuildHasherDefault<Fnv>> = HashMap::default();
    for k in 0..n {
        m.insert(k.wrapping_mul(0x9e3779b97f4a7c15), k);
    }
    digest(m.values().copied())
}
fn btreemap_order(n: u64) -> i64 {
    let mut m: BTreeMap<u64, u64> = BTreeMap::new();
    for k in 0..n {
        m.insert(k.wrapping_mul(0x9e3779b97f4a7c15), k);
    }
    digest(m.values().copied())
}

fn main() {
    println!("HashMap<u64, u64, fixed FNV> order {}", hashmap_order(1000));
    println!("BTreeMap order {}", btreemap_order(1000));
}
```
Expected output: `HashMap<u64, u64, fixed FNV> order 7883764408781778729 BTreeMap order 4523094667136758445`

*Check 3: wasm32: the same HashMap(fixed FNV) iterates in a different order* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, hashmap_digest · node calls hashmap_digest(1000) · **✔ oracle pass**
```rust
use std::collections::{BTreeMap, HashMap};
use std::hash::{BuildHasherDefault, Hasher};

// A fixed, seedless FNV-1a hasher: the hash of a u64 key is the same on every target.
#[derive(Default)]
struct Fnv(u64);
impl Hasher for Fnv {
    fn finish(&self) -> u64 {
        self.0
    }
    fn write(&mut self, bytes: &[u8]) {
        let mut h = if self.0 == 0 { 0xcbf29ce484222325 } else { self.0 };
        for b in bytes {
            h = (h ^ *b as u64).wrapping_mul(0x100000001b3);
        }
        self.0 = h;
    }
}

// Digest of the order in which a map yields the same 1000 inserts.
fn digest(values: impl Iterator<Item = u64>) -> i64 {
    let mut d: u64 = 0xcbf29ce484222325;
    for v in values {
        d = (d ^ v).wrapping_mul(0x100000001b3);
    }
    d as i64
}
fn hashmap_order(n: u64) -> i64 {
    let mut m: HashMap<u64, u64, BuildHasherDefault<Fnv>> = HashMap::default();
    for k in 0..n {
        m.insert(k.wrapping_mul(0x9e3779b97f4a7c15), k);
    }
    digest(m.values().copied())
}
fn btreemap_order(n: u64) -> i64 {
    let mut m: BTreeMap<u64, u64> = BTreeMap::new();
    for k in 0..n {
        m.insert(k.wrapping_mul(0x9e3779b97f4a7c15), k);
    }
    digest(m.values().copied())
}

#[no_mangle]
pub extern "C" fn hashmap_digest(n: u32) -> i64 {
    hashmap_order(n as u64)
}
#[no_mangle]
pub extern "C" fn btreemap_digest(n: u32) -> i64 {
    btreemap_order(n as u64)
}
```
Expected output: `415840167048917935`

*Check 4: wasm32: the BTreeMap iterates in the same order as on x86-64* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, btreemap_digest · node calls btreemap_digest(1000) · **✔ oracle pass**
```rust
use std::collections::{BTreeMap, HashMap};
use std::hash::{BuildHasherDefault, Hasher};

// A fixed, seedless FNV-1a hasher: the hash of a u64 key is the same on every target.
#[derive(Default)]
struct Fnv(u64);
impl Hasher for Fnv {
    fn finish(&self) -> u64 {
        self.0
    }
    fn write(&mut self, bytes: &[u8]) {
        let mut h = if self.0 == 0 { 0xcbf29ce484222325 } else { self.0 };
        for b in bytes {
            h = (h ^ *b as u64).wrapping_mul(0x100000001b3);
        }
        self.0 = h;
    }
}

// Digest of the order in which a map yields the same 1000 inserts.
fn digest(values: impl Iterator<Item = u64>) -> i64 {
    let mut d: u64 = 0xcbf29ce484222325;
    for v in values {
        d = (d ^ v).wrapping_mul(0x100000001b3);
    }
    d as i64
}
fn hashmap_order(n: u64) -> i64 {
    let mut m: HashMap<u64, u64, BuildHasherDefault<Fnv>> = HashMap::default();
    for k in 0..n {
        m.insert(k.wrapping_mul(0x9e3779b97f4a7c15), k);
    }
    digest(m.values().copied())
}
fn btreemap_order(n: u64) -> i64 {
    let mut m: BTreeMap<u64, u64> = BTreeMap::new();
    for k in 0..n {
        m.insert(k.wrapping_mul(0x9e3779b97f4a7c15), k);
    }
    digest(m.values().copied())
}

#[no_mangle]
pub extern "C" fn hashmap_digest(n: u32) -> i64 {
    hashmap_order(n as u64)
}
#[no_mangle]
pub extern "C" fn btreemap_digest(n: u32) -> i64 {
    btreemap_order(n as u64)
}
```
Expected output: `4523094667136758445`

## Keep std sin, cos, exp, ln, powf, atan2 and hypot out of hashed math; call the Cargo.lock-pinned libm
**std documents sin, cos, exp, ln, powf, atan2 and hypot as 'Unspecified precision' (varies by platform and Rust version). Natively they are the platform C library's (on this Windows host each of the seven disagrees with the libm crate somewhere in a 100 000-input sweep); on wasm32-unknown-unknown they are compiled into the module from the toolchain's own copy of libm in compiler-builtins, which today matches libm 0.2.16 for sin but not for hypot.**

*Check 1: on x86_64-pc-windows-msvc std's sin/cos/exp/ln/powf/atan2/hypot each differ from libm somewhere* · `runs` · edition 2021 · host · bin · deps: libm · **✔ oracle pass**
```rust
// On this host (x86_64-pc-windows-msvc) std's f64 math comes from the platform C runtime.
fn main() {
    let names = ["sin", "cos", "exp", "ln", "powf", "atan2", "hypot"];
    let mut differs = [false; 7];
    let mut s = 0x9e3779b97f4a7c15u64;
    for _ in 0..100_000 {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let x = std::hint::black_box(((s >> 11) as f64 / (1u64 << 53) as f64) * 16.0 - 8.0);
        let y = std::hint::black_box(((s.rotate_left(17) >> 11) as f64 / (1u64 << 53) as f64) * 16.0 - 8.0);
        let pairs = [
            (x.sin(), libm::sin(x)),
            (x.cos(), libm::cos(x)),
            (x.exp(), libm::exp(x)),
            (x.abs().ln(), libm::log(x.abs())),
            (x.abs().powf(y), libm::pow(x.abs(), y)),
            (y.atan2(x), libm::atan2(y, x)),
            (x.hypot(y), libm::hypot(x, y)),
        ];
        for (k, (a, b)) in pairs.iter().enumerate() {
            differs[k] |= a.to_bits() != b.to_bits();
        }
    }
    for k in 0..7 {
        println!("{} std!=libm: {}", names[k], differs[k]);
    }
}
```
Expected output: `sin std!=libm: true cos std!=libm: true exp std!=libm: true ln std!=libm: true powf std!=libm: true atan2 std!=libm: true hypot std!=libm: true`

*Check 2: libm 0.2.16 digests over the shared 100k sweep: sin and hypot* · `runs` · edition 2021 · host · bin · deps: libm · **✔ oracle pass**
```rust
fn sweep(n: u32, f: &dyn Fn(f64, f64) -> f64) -> i64 {
    let (mut s, mut h) = (0x9e3779b97f4a7c15u64, 0xcbf29ce484222325u64);
    let mut i = 0;
    while i < n {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let x = ((s >> 11) as f64 / (1u64 << 53) as f64) * 16.0 - 8.0;
        let y = ((s.rotate_left(17) >> 11) as f64 / (1u64 << 53) as f64) * 16.0 - 8.0;
        h = (h ^ f(std::hint::black_box(x), std::hint::black_box(y)).to_bits()).wrapping_mul(0x100000001b3);
        i += 1;
    }
    h as i64
}

// Digests of the pinned libm crate (0.2.16) over the same sweep the wasm checks use.
fn main() {
    println!("libm sin {}", sweep(100_000, &|x, _| libm::sin(x)));
    println!("libm hypot {}", sweep(100_000, &|x, y| libm::hypot(x, y)));
}
```
Expected output: `libm sin 1810793848087136966 libm hypot 727198713234182705`

*Check 3: wasm32 std f64::sin equals libm 0.2.16 over the sweep and the module imports nothing* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, std_sin · imports nothing · node calls std_sin(100000) · **✔ oracle pass**
```rust
fn sweep(n: u32, f: &dyn Fn(f64, f64) -> f64) -> i64 {
    let (mut s, mut h) = (0x9e3779b97f4a7c15u64, 0xcbf29ce484222325u64);
    let mut i = 0;
    while i < n {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let x = ((s >> 11) as f64 / (1u64 << 53) as f64) * 16.0 - 8.0;
        let y = ((s.rotate_left(17) >> 11) as f64 / (1u64 << 53) as f64) * 16.0 - 8.0;
        h = (h ^ f(std::hint::black_box(x), std::hint::black_box(y)).to_bits()).wrapping_mul(0x100000001b3);
        i += 1;
    }
    h as i64
}

// std's f64::sin / f64::hypot on wasm32-unknown-unknown.
#[no_mangle]
pub extern "C" fn std_sin(n: u32) -> i64 {
    sweep(n, &|x, _| x.sin())
}
#[no_mangle]
pub extern "C" fn std_hypot(n: u32) -> i64 {
    sweep(n, &|x, y| x.hypot(y))
}
```
Expected output: `1810793848087136966`

*Check 4: wasm32 std f64::hypot differs from libm 0.2.16 over the same sweep (toolchain's CORE-MATH port)* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, std_hypot · node calls std_hypot(100000) · **✔ oracle pass**
```rust
fn sweep(n: u32, f: &dyn Fn(f64, f64) -> f64) -> i64 {
    let (mut s, mut h) = (0x9e3779b97f4a7c15u64, 0xcbf29ce484222325u64);
    let mut i = 0;
    while i < n {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let x = ((s >> 11) as f64 / (1u64 << 53) as f64) * 16.0 - 8.0;
        let y = ((s.rotate_left(17) >> 11) as f64 / (1u64 << 53) as f64) * 16.0 - 8.0;
        h = (h ^ f(std::hint::black_box(x), std::hint::black_box(y)).to_bits()).wrapping_mul(0x100000001b3);
        i += 1;
    }
    h as i64
}

// std's f64::sin / f64::hypot on wasm32-unknown-unknown.
#[no_mangle]
pub extern "C" fn std_sin(n: u32) -> i64 {
    sweep(n, &|x, _| x.sin())
}
#[no_mangle]
pub extern "C" fn std_hypot(n: u32) -> i64 {
    sweep(n, &|x, y| x.hypot(y))
}
```
Expected output: `-4090065345391819473`

## Know what rapier3d-f64 0.35.3's enhanced-determinism switches: libm, IndexMap, canonical zeros, not SIMD
**`enhanced-determinism` = simba's `libm_force` (an optional dependency on the libm crate, so simba's ComplexField/RealField math on f64 calls libm) plus parry's flag (indexmap, glamx/libm, glamx/scalar-math). In code it makes parry's HashMap/HashSet an IndexMap/IndexSet with a pointer-width-independent FxHasher32, drains joint wake-up/join sets in order, canonicalises -0.0 in the warm-start impulses it stores, and refuses `simd8` with compile_error!. It does not switch off parry's 4-lane `wide` types.**

*Check 1: parry HashMap is an IndexMap (insertion order, swap_remove); SIMD is 4-lane WideF64x4* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::math::{SimdReal, SIMD_WIDTH};
use rapier3d_f64::parry::utils::hashmap::HashMap;
use std::hash::BuildHasher;

fn main() {
    // Under enhanced-determinism parry's HashMap is an IndexMap: insertion-order iteration
    // and swap_remove exist only on that type.
    let mut m: HashMap<u32, u32> = HashMap::default();
    for k in [5u32, 1, 3] {
        m.insert(k, k * 10);
    }
    let before: Vec<u32> = m.keys().copied().collect();
    m.swap_remove(&5);
    let after: Vec<u32> = m.keys().copied().collect();
    println!("{:?} {:?} fx32(7)={}", before, after, m.hasher().hash_one(7u64));
    // The 4-lane wide type is still the solver's SIMD scalar.
    println!("lanes={} {}", SIMD_WIDTH, std::any::type_name::<SimdReal>());
}
```
Expected output: `[5, 1, 3] [3, 1] fx32(7)=549813274 lanes=4 simba::simd::wide_simd_impl::WideF64x4`

*Check 2: simba ComplexField::sin and glam DQuat use libm bit for bit; std f64::sin does not* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64, libm · **✔ oracle pass**
```rust
use rapier3d_f64::math::Rotation;
use rapier3d_f64::parry::simba::scalar::ComplexField;

// Under enhanced-determinism simba (libm_force) and glam (glamx/libm) send f64
// transcendentals to the libm crate, not to the platform's C runtime.
fn main() {
    let (mut simba_eq_libm, mut glam_eq_libm, mut std_eq_libm) = (true, true, true);
    let mut s = 0x9e3779b97f4a7c15u64;
    for _ in 0..100_000 {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let a = std::hint::black_box(((s >> 11) as f64 / (1u64 << 53) as f64) * 16.0 - 8.0);
        let l = libm::sin(a);
        simba_eq_libm &= <f64 as ComplexField>::sin(a).to_bits() == l.to_bits();
        std_eq_libm &= a.sin().to_bits() == l.to_bits();
        // glam's DQuat::from_rotation_y stores sin(angle / 2) in y.
        glam_eq_libm &= Rotation::from_rotation_y(2.0 * a).y.to_bits() == l.to_bits();
    }
    println!("simba sin == libm: {simba_eq_libm}; glam quat == libm: {glam_eq_libm}; std sin == libm: {std_eq_libm}");
}
```
Expected output: `simba sin == libm: true; glam quat == libm: true; std sin == libm: false`

## Refuse NaN or map it to one bit pattern before hashing: its sign and payload are the engine's choice
**NaN != NaN, and the bits of a NaN produced by arithmetic are nondeterministic in both Rust and wasm (the sign always; the payload within the options each spec lists), may differ between const eval and run time, and V8 on this x86-64 host returns 0xfff8000000000000 (sign set) for 0/0 while `f64::NAN` is 0x7ff8000000000000; `total_cmp` still gives a total order (-NaN < -inf < ... < -0 < +0 < ... < +inf < +NaN) where `partial_cmp` returns None.**

*Check 1: x86-64: runtime 0/0 is fff8000000000000, NAN is 7ff8...; total_cmp orders it; one-pattern map* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;
fn main() {
    let n = black_box(0.0f64) / black_box(0.0f64); // computed at run time on this x86-64 host
    println!("n == n: {}; 0/0 bits {:016x}; f64::NAN bits {:016x}", n == n, n.to_bits(), f64::NAN.to_bits());
    let mut v = vec![1.0, n, -0.0, f64::NAN, 0.0, -1.0, f64::NEG_INFINITY];
    v.sort_by(|a, b| a.total_cmp(b));
    let s: Vec<String> = v.iter().map(|x| format!("{:016x}", x.to_bits())).collect();
    println!("total_cmp order: {}", s.join(" "));
    let canonical = |x: f64| if x.is_nan() { f64::from_bits(0x7ff8000000000000) } else { x };
    println!("canonical NaN bits {:016x}", canonical(n).to_bits());
}
```
Expected output: `n == n: false; 0/0 bits fff8000000000000; f64::NAN bits 7ff8000000000000 total_cmp order: fff8000000000000 fff0000000000000 bff0000000000000 8000000000000000 0000000000000000 3ff0000000000000 7ff80000`

*Check 2: sort_by(partial_cmp().unwrap()) panics on a NaN: exit 101* · `runs` · edition 2021 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![2.0, f64::NAN, 1.0];
    // partial_cmp returns None for NaN; the unwrap panics.
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    println!("{:?}", v);
}
```

*Check 3: V8 on this x86-64 host computes 0/0 as 0xfff8000000000000 (sign set)* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, nan_bits · node calls nan_bits(0, 0) · **✔ oracle pass**
```rust
// The division runs in the wasm engine at call time: the NaN's sign is the host's choice.
#[no_mangle]
pub extern "C" fn nan_bits(a: f64, b: f64) -> i64 {
    (a / b).to_bits() as i64
}
#[no_mangle]
pub extern "C" fn canonical_nan_bits(a: f64, b: f64) -> i64 {
    let x = a / b;
    let x = if x.is_nan() { f64::from_bits(0x7ff8000000000000) } else { x };
    x.to_bits() as i64
}
```
Expected output: `-2251799813685248`

*Check 4: mapping NaN to 0x7ff8000000000000 before to_bits gives one pattern in wasm* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, canonical_nan_bits · node calls canonical_nan_bits(0, 0) · **✔ oracle pass**
```rust
// The division runs in the wasm engine at call time: the NaN's sign is the host's choice.
#[no_mangle]
pub extern "C" fn nan_bits(a: f64, b: f64) -> i64 {
    (a / b).to_bits() as i64
}
#[no_mangle]
pub extern "C" fn canonical_nan_bits(a: f64, b: f64) -> i64 {
    let x = a / b;
    let x = if x.is_nan() { f64::from_bits(0x7ff8000000000000) } else { x };
    x.to_bits() as i64
}
```
Expected output: `9221120237041090560`

## Write the min/max tie rule yourself: f64::max(-0.0, 0.0) changes with context, minimum/maximum are nightly
**f64::min/max ignore a single NaN (IEEE 754-2019 minimumNumber/maximumNumber) but may return either zero on a -0.0/+0.0 tie; f64::minimum/maximum (NaN-propagating, -0 < +0) are still unstable on 1.98.1 (E0658, feature float_minimum_maximum, #91079); wasm's fmin/fmax propagate NaN and order the zeros; JS Math.min/max return NaN for any NaN argument and treat -0 as smaller than +0 (Math.min(0, -0) is -0, Math.max(-0, 0) is 0).**

*Check 1: f64::minimum is unstable on 1.98.1: E0658 (float_minimum_maximum)* · `compile_fail` · edition 2021 · host · lib · errors: E0658 · **✔ oracle pass**
```rust
pub fn ieee_min(a: f64, b: f64) -> f64 {
    a.minimum(b)
}
```

*Check 2: native -O0: n.max(p) gives 0.0 in both contexts* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;

// The same expression, n.max(p) with n = -0.0 and p = +0.0, in two contexts.
#[inline(never)]
fn alone(n: f64, p: f64) -> f64 {
    n.max(p)
}
#[inline(never)]
fn beside(n: f64, p: f64) -> (f64, f64) {
    (p.max(n), n.max(p))
}

fn main() {
    let (n, p) = (black_box(-0.0f64), black_box(0.0f64));
    let (_, b) = beside(n, p);
    println!("alone {:?} beside {:?}", alone(n, p), b);
}
```
Expected output: `alone 0.0 beside 0.0`

*Check 3: native -O: the same n.max(p) gives 0.0 alone and -0.0 beside p.max(n)* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;

// The same expression, n.max(p) with n = -0.0 and p = +0.0, in two contexts.
#[inline(never)]
fn alone(n: f64, p: f64) -> f64 {
    n.max(p)
}
#[inline(never)]
fn beside(n: f64, p: f64) -> (f64, f64) {
    (p.max(n), n.max(p))
}

fn main() {
    let (n, p) = (black_box(-0.0f64), black_box(0.0f64));
    let (_, b) = beside(n, p);
    println!("alone {:?} beside {:?}", alone(n, p), b);
}
```
Expected output: `alone 0.0 beside -0.0`

*Check 4: wasm -O: max(-0.0, 0.0) alone returns +0* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, alone · node calls alone(-0.0, 0.0) · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn alone(n: f64, p: f64) -> f64 {
    n.max(p)
}
#[no_mangle]
pub extern "C" fn beside(n: f64, p: f64) -> f64 {
    let first = p.max(n);
    let second = n.max(p);
    if first.to_bits() == 1 { first } else { second }
}
```
Expected output: `0`

*Check 5: wasm -O: the same max(-0.0, 0.0) beside max(0.0, -0.0) returns -0* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, beside · node calls beside(-0.0, 0.0) · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn alone(n: f64, p: f64) -> f64 {
    n.max(p)
}
#[no_mangle]
pub extern "C" fn beside(n: f64, p: f64) -> f64 {
    let first = p.max(n);
    let second = n.max(p);
    if first.to_bits() == 1 { first } else { second }
}
```
Expected output: `-0`

*Check 6: lib.rs js_min/js_max: JS zero order, asymmetric NaN; clamp keeps -0.0* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// js_min / js_max as written in si-rpg-engine solver/src/lib.rs.
fn js_min(a: f64, b: f64) -> f64 {
    if b < a || (a == 0.0 && b == 0.0 && b.is_sign_negative() && !a.is_sign_negative()) { b } else { a }
}
fn js_max(a: f64, b: f64) -> f64 {
    if a < b || (a == 0.0 && b == 0.0 && a.is_sign_negative() && !b.is_sign_negative()) { b } else { a }
}
fn main() {
    let nan = f64::NAN;
    println!("zeros: js_min(0,-0)={:?} js_min(-0,0)={:?} js_max(0,-0)={:?} js_max(-0,0)={:?}",
        js_min(0.0, -0.0), js_min(-0.0, 0.0), js_max(0.0, -0.0), js_max(-0.0, 0.0));
    println!("NaN: js_min(1,NaN)={:?} js_min(NaN,1)={:?} f64::min(1,NaN)={:?} f64::min(NaN,1)={:?}",
        js_min(1.0, nan), js_min(nan, 1.0), 1.0f64.min(nan), nan.min(1.0));
    println!("clamp: (-0.0).clamp(0.0, 1.0)={:?}", std::hint::black_box(-0.0f64).clamp(0.0, 1.0));
}
```
Expected output: `zeros: js_min(0,-0)=-0.0 js_min(-0,0)=-0.0 js_max(0,-0)=0.0 js_max(-0,0)=0.0 NaN: js_min(1,NaN)=1.0 js_min(NaN,1)=NaN f64::min(1,NaN)=1.0 f64::min(NaN,1)=1.0 clamp: (-0.0).clamp(0.0, 1.0)=-0.0`

## Treat rust-toolchain.toml as part of the law: the solver links the toolchain's own log2, acos, cos and sin
**Inherent calls such as `x.log2()` or `x.acos()` on an f64 resolve to std's method (inherent methods are searched before trait methods, and a `#![no_std]` crate that links std sees them), so libm_force cannot reroute them; in parry 0.30.2's bvh_optimize.rs and glamx 0.3.1's eigen3.rs the ComplexField import is compiled only without std. On wasm32 those std methods are compiler-builtins' copy of libm, pinned by the toolchain, not by Cargo.lock.**

*Check 1: with ComplexField in scope a.sin() is std's (import reported unused); the trait path is libm's* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64, libm · lints: unused_imports · **✔ oracle pass**
```rust
// With simba's ComplexField in scope, method syntax on an f64 still picks the inherent
// std method; only trait-path calls (and generic code over ComplexField) reach libm.
use rapier3d_f64::parry::simba::scalar::ComplexField as _;

fn main() {
    let (mut method_is_std, mut trait_path_is_libm, mut std_eq_libm) = (true, true, true);
    let mut s = 0x9e3779b97f4a7c15u64;
    for _ in 0..100_000 {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let a = std::hint::black_box(((s >> 11) as f64 / (1u64 << 53) as f64) * 16.0 - 8.0);
        let by_method = a.sin();
        method_is_std &= by_method.to_bits() == f64::sin(a).to_bits();
        trait_path_is_libm &= <f64 as rapier3d_f64::parry::simba::scalar::ComplexField>::sin(a).to_bits() == libm::sin(a).to_bits();
        std_eq_libm &= f64::sin(a).to_bits() == libm::sin(a).to_bits();
    }
    println!("a.sin() is std's: {method_is_std}; ComplexField::sin is libm's: {trait_path_is_libm}; std == libm: {std_eq_libm}");
}
```
Expected output: `a.sin() is std's: true; ComplexField::sin is libm's: true; std == libm: false`

*Check 2: a #![no_std] crate that links std compiles root.log2() as parry's BVH optimizer does* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
#![no_std]
// The pattern parry and glamx use: no_std, plus std when their `std` feature is on.
extern crate std;

// With std linked, the inherent (std) method resolves even in a no_std crate.
pub fn refinement_cost(root: f64, subtree: f64) -> f64 {
    root * root.log2() / (subtree * subtree.log2())
}
```

*Check 3: libm 0.2.16 and this host's std digests for acos, log2 and cos over 100k inputs* · `runs` · edition 2021 · host · bin · deps: libm · **✔ oracle pass**
```rust
// acos over [-1, 1); log2 over [2^-20, 2^20) with random mantissas; cos over [-8, 8).
fn sweep(n: u32, k: u32, f: &dyn Fn(u32, f64) -> f64) -> i64 {
    let (mut s, mut h) = (0x9e3779b97f4a7c15u64, 0xcbf29ce484222325u64);
    let mut i = 0;
    while i < n {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let u = (s >> 11) as f64 / (1u64 << 53) as f64;
        let x = match k {
            0 => u * 2.0 - 1.0,
            1 => f64::from_bits((s & 0x000f_ffff_ffff_ffff) | (((1023 - 20 + (s >> 58) as i64 % 40) as u64) << 52)),
            _ => u * 16.0 - 8.0,
        };
        h = (h ^ f(k, std::hint::black_box(x)).to_bits()).wrapping_mul(0x100000001b3);
        i += 1;
    }
    h as i64
}

fn main() {
    let lib = |k: u32, x: f64| match k { 0 => libm::acos(x), 1 => libm::log2(x), _ => libm::cos(x) };
    let st = |k: u32, x: f64| match k { 0 => x.acos(), 1 => x.log2(), _ => x.cos() };
    for (k, name) in [(0, "acos"), (1, "log2"), (2, "cos")] {
        println!("{name}: libm {} host-std {}", sweep(100_000, k, &lib), sweep(100_000, k, &st));
    }
}
```
Expected output: `acos: libm -6587451203984369641 host-std -7754005744722629736 log2: libm -746673324466636529 host-std -5254763021945254724 cos: libm 2919292257806185509 host-std -404969107991927780`

*Check 4: wasm32 std acos (compiler-builtins) equals libm 0.2.16 over the sweep today* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, std_digest · imports nothing · node calls std_digest(100000, 0) · **✔ oracle pass**
```rust
// acos over [-1, 1); log2 over [2^-20, 2^20) with random mantissas; cos over [-8, 8).
fn sweep(n: u32, k: u32, f: &dyn Fn(u32, f64) -> f64) -> i64 {
    let (mut s, mut h) = (0x9e3779b97f4a7c15u64, 0xcbf29ce484222325u64);
    let mut i = 0;
    while i < n {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let u = (s >> 11) as f64 / (1u64 << 53) as f64;
        let x = match k {
            0 => u * 2.0 - 1.0,
            1 => f64::from_bits((s & 0x000f_ffff_ffff_ffff) | (((1023 - 20 + (s >> 58) as i64 % 40) as u64) << 52)),
            _ => u * 16.0 - 8.0,
        };
        h = (h ^ f(k, std::hint::black_box(x)).to_bits()).wrapping_mul(0x100000001b3);
        i += 1;
    }
    h as i64
}

// std's inherent acos / log2 / cos on wasm32-unknown-unknown: compiler-builtins' copy of libm.
#[no_mangle]
pub extern "C" fn std_digest(n: u32, k: u32) -> i64 {
    sweep(n, k, &|k, x| match k { 0 => x.acos(), 1 => x.log2(), _ => x.cos() })
}
```
Expected output: `-6587451203984369641`

*Check 5: wasm32 std log2 (compiler-builtins) equals libm 0.2.16 over the sweep today* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, std_digest · node calls std_digest(100000, 1) · **✔ oracle pass**
```rust
// acos over [-1, 1); log2 over [2^-20, 2^20) with random mantissas; cos over [-8, 8).
fn sweep(n: u32, k: u32, f: &dyn Fn(u32, f64) -> f64) -> i64 {
    let (mut s, mut h) = (0x9e3779b97f4a7c15u64, 0xcbf29ce484222325u64);
    let mut i = 0;
    while i < n {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let u = (s >> 11) as f64 / (1u64 << 53) as f64;
        let x = match k {
            0 => u * 2.0 - 1.0,
            1 => f64::from_bits((s & 0x000f_ffff_ffff_ffff) | (((1023 - 20 + (s >> 58) as i64 % 40) as u64) << 52)),
            _ => u * 16.0 - 8.0,
        };
        h = (h ^ f(k, std::hint::black_box(x)).to_bits()).wrapping_mul(0x100000001b3);
        i += 1;
    }
    h as i64
}

// std's inherent acos / log2 / cos on wasm32-unknown-unknown: compiler-builtins' copy of libm.
#[no_mangle]
pub extern "C" fn std_digest(n: u32, k: u32) -> i64 {
    sweep(n, k, &|k, x| match k { 0 => x.acos(), 1 => x.log2(), _ => x.cos() })
}
```
Expected output: `-746673324466636529`

*Check 6: wasm32 std cos (compiler-builtins) equals libm 0.2.16 over the sweep today* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, std_digest · node calls std_digest(100000, 2) · **✔ oracle pass**
```rust
// acos over [-1, 1); log2 over [2^-20, 2^20) with random mantissas; cos over [-8, 8).
fn sweep(n: u32, k: u32, f: &dyn Fn(u32, f64) -> f64) -> i64 {
    let (mut s, mut h) = (0x9e3779b97f4a7c15u64, 0xcbf29ce484222325u64);
    let mut i = 0;
    while i < n {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let u = (s >> 11) as f64 / (1u64 << 53) as f64;
        let x = match k {
            0 => u * 2.0 - 1.0,
            1 => f64::from_bits((s & 0x000f_ffff_ffff_ffff) | (((1023 - 20 + (s >> 58) as i64 % 40) as u64) << 52)),
            _ => u * 16.0 - 8.0,
        };
        h = (h ^ f(k, std::hint::black_box(x)).to_bits()).wrapping_mul(0x100000001b3);
        i += 1;
    }
    h as i64
}

// std's inherent acos / log2 / cos on wasm32-unknown-unknown: compiler-builtins' copy of libm.
#[no_mangle]
pub extern "C" fn std_digest(n: u32, k: u32) -> i64 {
    sweep(n, k, &|k, x| match k { 0 => x.acos(), 1 => x.log2(), _ => x.cos() })
}
```
Expected output: `2919292257806185509`

