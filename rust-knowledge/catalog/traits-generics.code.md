# Traits & generics — the working set — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](traits-generics.md) · [catalog index](README.md)

## Define traits with required and default methods; state generic bounds inline or in a where clause
**A trait's body-less methods are required and its methods with bodies are defaults an implementor may override; generic code can call only what its bounds name.**

*Check 1: a default method built on a required one; an override; a where-clause generic* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::fmt::Debug;

trait Solid {
    fn half_extents(&self) -> [f64; 3]; // required: no body
    fn volume(&self) -> f64 {           // default: built on the required method
        let [x, y, z] = self.half_extents();
        8.0 * x * y * z
    }
}

#[derive(Debug)]
struct Cube(f64);
#[derive(Debug)]
struct Trigger { half: [f64; 3] }

impl Solid for Cube {
    fn half_extents(&self) -> [f64; 3] { [self.0; 3] }
}
impl Solid for Trigger {
    fn half_extents(&self) -> [f64; 3] { self.half }
    fn volume(&self) -> f64 { 0.0 } // overrides the default
}

fn total_volume<T>(items: &[T]) -> f64
where
    T: Solid + Debug,
{
    items.iter().map(|s| s.volume()).sum()
}

fn main() {
    let t = Trigger { half: [1.0; 3] };
    println!("{} {} {}", Cube(0.5).volume(), t.volume(), total_volume(&[Cube(0.5), Cube(1.0)]));
}
```
Expected output: `1 0 9`

*Check 2: an impl that omits a required method is E0046, even when it overrides the default* · `compile_fail` · edition 2024 · host · lib · errors: E0046 · stderr has “missing: `half_extents`” · **✔ oracle pass**
```rust
pub trait Solid {
    fn half_extents(&self) -> [f64; 3];
    fn volume(&self) -> f64 {
        let [x, y, z] = self.half_extents();
        8.0 * x * y * z
    }
}
pub struct Cube(pub f64);
impl Solid for Cube {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.0 * self.0 }
}
```

*Check 3: a generic body cannot call a trait method its bounds do not name (E0599)* · `compile_fail` · edition 2024 · host · lib · errors: E0599 · stderr has “items from traits can only be used if the type parameter is bounded by the trait” · **✔ oracle pass**
```rust
pub trait Solid {
    fn volume(&self) -> f64;
}
pub fn total<T>(items: &[T]) -> f64 {
    items.iter().map(|s| s.volume()).sum()
}
```

*Check 4: a caller whose type lacks the impl fails the bound with E0277* · `compile_fail` · edition 2024 · host · errors: E0277 · stderr has “the trait bound `f64: Solid` is not satisfied” · **✔ oracle pass**
```rust
trait Solid {
    fn volume(&self) -> f64;
}
fn total<T: Solid>(items: &[T]) -> f64 {
    items.iter().map(|s| s.volume()).sum()
}
fn main() {
    println!("{}", total(&[1.0_f64, 2.0]));
}
```

## Derive Debug, Clone, Copy, PartialEq and Default on plain data; implement Display by hand
**A derive is legal only when every field implements the trait, and each carries a contract: Copy is an implicit bitwise copy that requires Clone, derived Default uses each field's default, derived Debug output is not stable across Rust versions, and Display cannot be derived.**

*Check 1: derived Debug/Copy/PartialEq/Default on f64 fields; enum #[default]; hand-written Display* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Default)]
struct Vec3 {
    x: f64,
    y: f64,
    z: f64,
}

impl fmt::Display for Vec3 {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({}, {}, {})", self.x, self.y, self.z)
    }
}

#[allow(dead_code)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
enum Mode {
    #[default]
    Dynamic,
    Kinematic,
    Fixed,
}

fn main() {
    let a = Vec3 { x: 1.0, ..Default::default() };
    let b = a; // Copy: `a` stays usable
    println!("{:?}", a);
    println!("{} {}", b, b.to_string() == format!("{b}"));
    println!("{:?} {}", Mode::default(), a == b.clone());
}
```
Expected output: `Vec3 { x: 1.0, y: 0.0, z: 0.0 } (1, 0, 0) true Dynamic true`

*Check 2: Copy on a struct with a Vec field is E0204* · `compile_fail` · edition 2024 · host · lib · errors: E0204 · stderr has “the trait `Copy` cannot be implemented for this type” · **✔ oracle pass**
```rust
#[derive(Clone, Copy)]
pub struct Body {
    pub pos: [f64; 3],
    pub contacts: Vec<u32>,
}
```

*Check 3: Display has no derive* · `compile_fail` · edition 2024 · host · lib · stderr has “cannot find derive macro `Display` in this scope” · **✔ oracle pass**
```rust
#[derive(Debug, Display)]
pub struct Pose {
    pub x: f64,
}
```

*Check 4: #[default] only on a unit variant* · `compile_fail` · edition 2024 · host · lib · stderr has “the `#[default]` attribute may only be used on unit enum variants” · **✔ oracle pass**
```rust
#[derive(Debug, Default)]
pub enum Mode {
    #[default]
    Dynamic(f64),
    Fixed,
}
```

## Derive only PartialEq and PartialOrd on structs with f64 fields; derived Eq, Hash and Ord fail with E0277
**f64 implements PartialEq and PartialOrd but not Eq, Ord or Hash, so derives stop at the partial traits, and the derived == inherits float semantics: NaN is unequal to itself and 0.0 equals -0.0.**

*Check 1: derive(Eq) on a struct with an f64 field is E0277 `f64: Eq`* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “the trait bound `f64: Eq` is not satisfied” · **✔ oracle pass**
```rust
#[derive(PartialEq, Eq)]
pub struct Pose {
    pub x: f64,
    pub id: u32,
}
```

*Check 2: derive(Hash) on a struct with an f64 field is E0277 `f64: Hash`* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “the trait bound `f64: Hash` is not satisfied” · **✔ oracle pass**
```rust
#[derive(PartialEq, Hash)]
pub struct Pose {
    pub x: f64,
    pub id: u32,
}
```

*Check 3: derive(Ord) fails on `f64: Ord` even with a hand-written Eq* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “the trait bound `f64: Ord` is not satisfied” · **✔ oracle pass**
```rust
#[derive(PartialEq, PartialOrd, Ord)]
pub struct Pose {
    pub x: f64,
    pub id: u32,
}
impl Eq for Pose {}
```

*Check 4: derived == and partial_cmp: NaN != itself, None ordering, 0.0 == -0.0 with different bits* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
#[derive(Debug, Clone, Copy, PartialEq, PartialOrd)]
struct Pose {
    x: f64,
    y: f64,
}

fn main() {
    let nan = Pose { x: f64::NAN, y: 0.0 };
    let pz = Pose { x: 0.0, y: 1.0 };
    let nz = Pose { x: -0.0, y: 1.0 };
    println!("{}", nan == nan);
    println!("{:?}", nan.partial_cmp(&pz));
    println!("{} {}", pz == nz, pz.x.to_bits() == nz.x.to_bits());
}
```
Expected output: `false None true false`

*Check 5: assert_eq! on a derived-PartialEq value holding NaN panics even against its own copy* · `runs` · edition 2024 · host · no warnings · exit code 101 · **✔ oracle pass**
```rust
#[derive(Debug, Clone, Copy, PartialEq)]
struct Pose {
    x: f64,
}

fn main() {
    let p = Pose { x: f64::NAN };
    let q = p; // the very same bits
    assert_eq!(p, q); // panics: NaN != NaN
    println!("equal");
}
```

*Check 6: a hand-written Eq compiles but lies: a HashSet holds NaN twice and cannot find it* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::collections::HashSet;
use std::hash::{Hash, Hasher};

#[derive(Debug, Clone, Copy, PartialEq)]
struct Pose {
    x: f64,
}
impl Eq for Pose {} // compiles: Eq has no methods and reflexivity is not checked
impl Hash for Pose {
    fn hash<H: Hasher>(&self, h: &mut H) {
        self.x.to_bits().hash(h)
    }
}

fn main() {
    let nan = Pose { x: f64::NAN };
    let mut set = HashSet::new();
    set.insert(nan);
    set.insert(nan);
    println!("{} {} {}", nan == nan, set.len(), set.contains(&nan));
}
```
Expected output: `false 2 false`

## Implement From for lossless conversions and TryFrom for checked ones; never Into; accept AsRef or Borrow
**From is for infallible, lossless conversions and gives Into for free through a blanket impl, so a hand-written Into for the same pair collides (E0119); TryFrom carries an Error type for conversions that can fail; AsRef is a cheap view, and Borrow additionally promises identical Eq, Ord and Hash.**

*Check 1: From gives .into(); TryFrom refuses NaN and range; String: Borrow<str>; AsRef<str>* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq)]
struct Meters(f64);
impl From<f64> for Meters {
    fn from(v: f64) -> Self { Meters(v) }
}

#[derive(Debug, Clone, Copy, PartialEq)]
struct UnitInterval(f64);
impl TryFrom<f64> for UnitInterval {
    type Error = f64;
    fn try_from(v: f64) -> Result<Self, Self::Error> {
        if (0.0..=1.0).contains(&v) { Ok(UnitInterval(v)) } else { Err(v) }
    }
}

fn advance(pos: f64, d: impl Into<Meters>) -> f64 {
    pos + d.into().0
}

fn len_of(s: impl AsRef<str>) -> usize {
    s.as_ref().len()
}

fn main() {
    let m: Meters = 2.5.into(); // Into comes from the From impl
    println!("{:?} {}", m, advance(1.0, 0.5));
    println!("{:?} {:?} {:?}",
        UnitInterval::try_from(0.5), UnitInterval::try_from(f64::NAN), UnitInterval::try_from(2.0));
    println!("{} {}", u8::try_from(300u32).is_err(), 300u32 as u8);
    let mut ids: HashMap<String, u32> = HashMap::new();
    ids.insert("crate".to_string(), 7);
    println!("{:?} {} {}", ids.get("crate"), len_of("abc"), len_of(String::from("abcd")));
}
```
Expected output: `Meters(2.5) 1.5 Ok(UnitInterval(0.5)) Err(NaN) Err(2.0) true 44 Some(7) 3 4`

*Check 2: a hand-written Into next to From conflicts with std's blanket impl (E0119)* · `compile_fail` · edition 2024 · host · lib · errors: E0119 · stderr has “conflicting implementations of trait `Into<Meters>` for type `f64`” · **✔ oracle pass**
```rust
pub struct Meters(pub f64);
impl From<f64> for Meters {
    fn from(v: f64) -> Self { Meters(v) }
}
impl Into<Meters> for f64 {
    fn into(self) -> Meters { Meters(self) }
}
```

## Implement Iterator for your own type with type Item and next(); the adapters and for loops come free
**Iterator has one required method, `next(&mut self) -> Option<Self::Item>`; map, filter, zip, sum, collect and for-loop support all come from its provided methods and std's blanket IntoIterator impl.**

*Check 1: only next() written: size_hint default, map/collect, filter/count, for; chunks_exact agrees* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
const STRIDE: usize = 17;

/// Walks the first `n` rows of a flat, stride-17 body buffer.
struct Rows<'a> {
    buf: &'a [f64],
    next_row: usize,
    n: usize,
}

impl<'a> Iterator for Rows<'a> {
    type Item = &'a [f64];
    fn next(&mut self) -> Option<&'a [f64]> {
        if self.next_row == self.n {
            return None;
        }
        let start = self.next_row * STRIDE;
        self.next_row += 1;
        Some(&self.buf[start..start + STRIDE])
    }
}

fn main() {
    let mut buf = [0.0f64; 4 * STRIDE];
    for i in 0..4 {
        buf[i * STRIDE] = i as f64 * 0.5;        // slot 0: x
        buf[i * STRIDE + 16] = (i % 2) as f64;   // slot 16: driven flag
    }
    let rows = |n| Rows { buf: &buf, next_row: 0, n };
    println!("{:?}", rows(3).size_hint()); // provided default: (0, None)
    let xs: Vec<f64> = rows(3).map(|r| r[0]).collect();
    let driven = rows(3).filter(|r| r[16] == 1.0).count();
    let mut sum = 0.0;
    for r in rows(3) {
        sum += r[0];
    }
    // std already walks fixed-stride rows: chunks_exact yields the same slices
    let via_std: Vec<f64> = buf[..3 * STRIDE].chunks_exact(STRIDE).map(|r| r[0]).collect();
    println!("{:?} {} {} {}", xs, driven, sum, xs == via_std);
}
```
Expected output: `(0, None) [0.0, 0.5, 1.0] 1 1.5 true`

*Check 2: an Iterator impl without next is E0046* · `compile_fail` · edition 2024 · host · lib · errors: E0046 · stderr has “missing: `next`” · **✔ oracle pass**
```rust
pub struct Ticks {
    pub i: u32,
}
impl Iterator for Ticks {
    type Item = f64;
}
```

*Check 3: a plain iterator may resume after None; fuse() keeps it None* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
struct Blink {
    n: u32,
}
impl Iterator for Blink {
    type Item = u32;
    fn next(&mut self) -> Option<u32> {
        self.n += 1;
        if self.n % 2 == 0 { None } else { Some(self.n) }
    }
}

fn main() {
    let mut b = Blink { n: 0 };
    let (x, y, z) = (b.next(), b.next(), b.next());
    println!("{:?} {:?} {:?}", x, y, z);
    let mut f = Blink { n: 0 }.fuse();
    let (x, y, z) = (f.next(), f.next(), f.next());
    println!("{:?} {:?} {:?}", x, y, z);
}
```
Expected output: `Some(1) None Some(3) Some(1) None None`

*Check 4: an unconsumed adapter does nothing and warns unused_must_use* · `compiles` · edition 2024 · host · lib · lints: unused_must_use · stderr has “iterators are lazy and do nothing unless consumed” · **✔ oracle pass**
```rust
pub fn scale(v: &[f64]) {
    v.iter().map(|x| x * 2.0);
}
```

## Key f64 values by their bits: Eq and Hash from to_bits, Ord from total_cmp, never partial_cmp().unwrap()
**`f64::total_cmp` (1.62) orders every bit pattern by IEEE 754 totalOrder and `to_bits` (1.20) exposes the exact pattern; total_cmp compares a sign-adjusted copy of the bits as i64, so it reports Equal exactly when the bits match, and Eq/Hash from to_bits plus Ord from total_cmp form one consistent key.**

*Check 1: sort_by(f64::total_cmp): -NaN, -inf, -0.0, 0.0, 1.5, inf, NaN* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![f64::NAN, 1.5, f64::INFINITY, 0.0, -0.0, f64::NEG_INFINITY, -f64::NAN];
    v.sort_by(f64::total_cmp);
    println!("{:?}", v);
    println!("{}", v[0].is_nan() && v[0].is_sign_negative()); // the negative NaN sorts first
}
```
Expected output: `[NaN, -inf, -0.0, 0.0, 1.5, inf, NaN] true`

*Check 2: partial_cmp().unwrap() as a sort comparator panics on NaN (exit 101)* · `runs` · edition 2024 · host · no warnings · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![1.0, f64::NAN, 0.5];
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    println!("{:?}", v);
}
```

*Check 3: a Bits newtype: to_bits Eq/Hash + total_cmp Ord agree in HashSet and BTreeSet* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::cmp::Ordering;
use std::collections::{BTreeSet, HashSet};
use std::hash::{Hash, Hasher};

/// An f64 key whose identity is its bit pattern.
#[derive(Clone, Copy, Debug)]
struct Bits(f64);

impl PartialEq for Bits {
    fn eq(&self, o: &Self) -> bool { self.0.to_bits() == o.0.to_bits() }
}
impl Eq for Bits {}
impl Hash for Bits {
    fn hash<H: Hasher>(&self, h: &mut H) { self.0.to_bits().hash(h) }
}
impl Ord for Bits {
    fn cmp(&self, o: &Self) -> Ordering { self.0.total_cmp(&o.0) }
}
impl PartialOrd for Bits {
    fn partial_cmp(&self, o: &Self) -> Option<Ordering> { Some(self.cmp(o)) }
}

// as in si-rpg-engine solver/src/rapier_law.rs
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

fn main() {
    let raw = [1.0, f64::NAN, 0.0, -0.0, f64::NAN, 1.0];
    let hashed: HashSet<Bits> = raw.iter().map(|&x| Bits(x)).collect();
    let ordered: BTreeSet<Bits> = raw.iter().map(|&x| Bits(x)).collect();
    let canonical: BTreeSet<Bits> = raw.iter().map(|&x| Bits(canon(x))).collect();
    println!("{} {}", hashed.len(), ordered.len());
    println!("{:?}", ordered.iter().map(|b| b.0).collect::<Vec<_>>());
    println!("{}", canonical.len());
    println!("{}", Bits(f64::NAN) == Bits(f64::NAN));
}
```
Expected output: `4 4 [-0.0, 0.0, 1.0, NaN] 3 true`

*Check 4: total_cmp is Equal exactly when to_bits is equal (special values + 1e6 pairs)* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::cmp::Ordering;

fn main() {
    let specials: [u64; 14] = [
        0x0000_0000_0000_0000, 0x8000_0000_0000_0000, // +0, -0
        0x7FF0_0000_0000_0000, 0xFFF0_0000_0000_0000, // +inf, -inf
        0x7FF8_0000_0000_0000, 0xFFF8_0000_0000_0000, // quiet NaN, negative quiet NaN
        0x7FF8_0000_0000_0001, 0x7FF0_0000_0000_0001, // NaN with payload, signaling NaN
        0x0000_0000_0000_0001, 0x8000_0000_0000_0001, // +/- smallest subnormal
        0x3FF0_0000_0000_0000, 0xBFF0_0000_0000_0000, // +1, -1
        0x7FEF_FFFF_FFFF_FFFF, 0xFFEF_FFFF_FFFF_FFFF, // +MAX, -MAX
    ];
    let mut pairs = 0u64;
    let mut bad = 0u64;
    let mut check = |a: u64, b: u64| {
        let (x, y) = (f64::from_bits(a), f64::from_bits(b));
        let ord = x.total_cmp(&y);
        pairs += 1;
        if (ord == Ordering::Equal) != (a == b) {
            bad += 1;
        }
        if ord != y.total_cmp(&x).reverse() {
            bad += 1;
        }
    };
    for &a in &specials {
        for &b in &specials {
            check(a, b);
        }
    }
    let mut s = 0x9E37_79B9_7F4A_7C15u64; // xorshift64: equal pairs and one-bit-apart pairs
    for _ in 0..1_000_000 {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let b = if s & 1 == 0 { s } else { s ^ (1u64 << (s >> 58)) };
        check(s, b);
    }
    println!("{} pairs, {} disagreements", pairs, bad);
}
```
Expected output: `1000196 pairs, 0 disagreements`

*Check 5: the solver's mix_f64: -0.0 and 0.0 hash apart until canon folds them* · `runs` · edition 2021 · host · no warnings · **✔ oracle pass**
```rust
// mix_u64 / mix_f64 / canon as written in si-rpg-engine solver/src/rapier_law.rs
fn mix_u64(h: u64, x: u64) -> u64 {
    h.wrapping_mul(0x100000001b3).wrapping_add(x)
}
fn mix_f64(h: u64, x: f64) -> u64 {
    mix_u64(h, x.to_bits())
}
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}
const SEED: u64 = 0xcbf29ce484222325;

fn main() {
    println!("{}", mix_f64(SEED, 0.0) == mix_f64(SEED, -0.0));
    println!("{}", mix_f64(SEED, canon(-0.0)) == mix_f64(SEED, 0.0));
    println!("{}", -0.0 == 0.0); // what canon relies on
}
```
Expected output: `false true true`

*Check 6: a struct keeping its float as to_bits() u64 derives Eq and Hash (Signature mirror)* · `runs` · edition 2021 · host · no warnings · **✔ oracle pass**
```rust
use std::collections::HashSet;

// Field-for-field mirror of `Signature` in si-rpg-engine solver/src/rapier_law.rs:
// every field is an integer because `cell` is stored as `cell.to_bits()`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Signature {
    world_id: u32,
    n_bodies: u32,
    n_colliders: u32,
    rows: u32,
    cols: u32,
    cell: u64,
    driven: u64,
    carried: u64,
    geom: u64,
    shape: u32,
}

fn sig(cell: f64) -> Signature {
    Signature {
        world_id: 1, n_bodies: 2, n_colliders: 1, rows: 2, cols: 2,
        cell: cell.to_bits(), driven: 1, carried: 0, geom: 0xcbf29ce484222325, shape: 0,
    }
}

fn main() {
    let (a, b, c) = (sig(0.5), sig(0.5), sig(0.25));
    let set: HashSet<Signature> = [a, b, c].into_iter().collect();
    println!("{} {} {}", a == b, a == c, set.len());
}
```
Expected output: `true false 2`

*Check 7: rapier3d-f64 0.35.3 ColliderHandle is Eq + Hash but not Ord; (u32, u32) is Ord* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0277 · stderr has “the trait bound `ColliderHandle: Ord` is not satisfied” · **✔ oracle pass**
```rust
use rapier3d_f64::geometry::ColliderHandle;

fn hashable<T: Eq + std::hash::Hash>() {}
fn sortable<T: Ord>() {}

pub fn probe() {
    hashable::<ColliderHandle>(); // fine
    sortable::<(u32, u32)>();     // fine: what into_raw_parts() returns
    sortable::<ColliderHandle>(); // E0277
}
```

## Overload vector math with std::ops on a Copy Vec3, or reuse Rapier's glam DVec3 that already has the ops
**Each operator is a std::ops trait impl with an Output type, and the binary operators take their operands by value, so a vector type must be Copy (or implement the ops for references) to be used again after `a + b`.**

*Check 1: Add, Sub, Neg, Mul<f64>, f64 * Vec3 and += on a Copy Vec3; Neg yields -0.0* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::ops::{Add, AddAssign, Mul, Neg, Sub};

#[derive(Debug, Clone, Copy, PartialEq, Default)]
struct Vec3 {
    x: f64,
    y: f64,
    z: f64,
}

impl Vec3 {
    const fn new(x: f64, y: f64, z: f64) -> Self { Vec3 { x, y, z } }
}
impl Add for Vec3 {
    type Output = Vec3;
    fn add(self, o: Vec3) -> Vec3 { Vec3::new(self.x + o.x, self.y + o.y, self.z + o.z) }
}
impl Sub for Vec3 {
    type Output = Vec3;
    fn sub(self, o: Vec3) -> Vec3 { Vec3::new(self.x - o.x, self.y - o.y, self.z - o.z) }
}
impl Neg for Vec3 {
    type Output = Vec3;
    fn neg(self) -> Vec3 { Vec3::new(-self.x, -self.y, -self.z) }
}
impl Mul<f64> for Vec3 {
    type Output = Vec3;
    fn mul(self, s: f64) -> Vec3 { Vec3::new(self.x * s, self.y * s, self.z * s) }
}
impl Mul<Vec3> for f64 { // allowed: Vec3 is local
    type Output = Vec3;
    fn mul(self, v: Vec3) -> Vec3 { v * self }
}
impl AddAssign for Vec3 {
    fn add_assign(&mut self, o: Vec3) { *self = *self + o; }
}

const DT: f64 = 1.0 / 64.0;

fn main() {
    let mut p = Vec3::new(0.0, 1.0, 0.0);
    let v = Vec3::new(2.0, -8.0, 0.5);
    p += v * DT;           // AddAssign + Mul<f64>
    let back = p - DT * v; // Sub + Mul<Vec3> for f64; `v` reused because Vec3 is Copy
    println!("{:?}", p);
    println!("{:?} {}", -back, back == Vec3::new(0.0, 1.0, 0.0));
}
```
Expected output: `Vec3 { x: 0.03125, y: 0.875, z: 0.0078125 } Vec3 { x: -0.0, y: -1.0, z: -0.0 } true`

*Check 2: without Copy, the operand moved into `+` cannot be used again (E0382)* · `compile_fail` · edition 2024 · host · errors: E0382 · stderr has “use of moved value: `a`” · **✔ oracle pass**
```rust
use std::ops::Add;

#[derive(Debug, Clone, PartialEq)] // no Copy
struct Vec3 {
    x: f64,
    y: f64,
    z: f64,
}
impl Add for Vec3 {
    type Output = Vec3;
    fn add(self, o: Vec3) -> Vec3 { Vec3 { x: self.x + o.x, y: self.y + o.y, z: self.z + o.z } }
}

fn main() {
    let a = Vec3 { x: 1.0, y: 0.0, z: 0.0 };
    let b = Vec3 { x: 0.0, y: 1.0, z: 0.0 };
    let c = a + b;
    let d = a + c; // `a` was moved by the first `+`
    println!("{:?}", d);
}
```

*Check 3: an operator with no impl is E0369* · `compile_fail` · edition 2024 · host · errors: E0369 · stderr has “cannot multiply `Vec3` by `{float}`” · **✔ oracle pass**
```rust
use std::ops::Add;

#[derive(Debug, Clone, Copy, PartialEq)]
struct Vec3 {
    x: f64,
    y: f64,
    z: f64,
}
impl Add for Vec3 {
    type Output = Vec3;
    fn add(self, o: Vec3) -> Vec3 { Vec3 { x: self.x + o.x, y: self.y + o.y, z: self.z + o.z } }
}

fn main() {
    let a = Vec3 { x: 1.0, y: 0.0, z: 0.0 };
    println!("{:?}", a * 2.0); // no Mul<f64> impl
}
```

*Check 4: Rapier's Vector (glam DVec3) already supports +, -, unary -, * f64, f64 *, +=* · `compiles` · edition 2021 · host · lib · deps: rapier3d_f64 · no warnings · **✔ oracle pass**
```rust
use rapier3d_f64::math::Vector;

pub fn integrate(p: Vector, v: Vector, dt: f64) -> Vector {
    let mut q = p;
    q += v * dt;      // AddAssign, Mul<f64>
    let r = -(q - p); // Sub, Neg
    q + 2.0 * r       // Add, Mul<Vector> for f64
}
```

*Check 5: Rapier's Vector is neither Eq nor Hash, so it cannot key a map directly (E0277)* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0277 · stderr has “the trait bound `DVec3: Eq` is not satisfied” · stderr has “the trait bound `DVec3: Hash` is not satisfied” · **✔ oracle pass**
```rust
use rapier3d_f64::math::Vector;

fn key<T: Eq + std::hash::Hash>(_: T) {}

pub fn probe() {
    key(Vector::ZERO);
}
```

## Prefer monomorphized generics; use Box<dyn Trait> for mixed-type collections or to cut code size
**Generic code is compiled once per concrete type (static dispatch, inlinable, no run-time dispatch cost, paid for in compile time and binary size); a dyn Trait call goes through a vtable (one copy of the code, a run-time lookup, no inlining) and is what lets one container hold different types.**

*Check 1: a generic T is one concrete type: mixing Cube and Slab in one slice is E0308* · `compile_fail` · edition 2024 · host · errors: E0308 · stderr has “expected `Cube`, found `Slab`” · **✔ oracle pass**
```rust
trait Solid {
    fn volume(&self) -> f64;
}
struct Cube(f64);
struct Slab(f64, f64, f64);
impl Solid for Cube {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.0 * self.0 }
}
impl Solid for Slab {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.1 * self.2 }
}
fn total<T: Solid>(items: &[T]) -> f64 {
    items.iter().map(|s| s.volume()).sum()
}
fn main() {
    println!("{}", total(&[Cube(0.5), Slab(2.0, 0.25, 2.0)]));
}
```

*Check 2: Box<dyn Solid> holds both types; &dyn is two words, &T one* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
trait Solid {
    fn volume(&self) -> f64;
}
struct Cube(f64);
struct Slab(f64, f64, f64);
impl Solid for Cube {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.0 * self.0 }
}
impl Solid for Slab {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.1 * self.2 }
}
use std::mem::size_of;

fn total<T: Solid>(items: &[T]) -> f64 { // monomorphized: one copy per T
    items.iter().map(|s| s.volume()).sum()
}
fn total_dyn(items: &[Box<dyn Solid>]) -> f64 { // one copy, vtable calls
    items.iter().map(|s| s.volume()).sum()
}

fn main() {
    let mixed: Vec<Box<dyn Solid>> = vec![Box::new(Cube(0.5)), Box::new(Slab(2.0, 0.25, 2.0))];
    println!("{} {}", total(&[Cube(0.5), Cube(1.0)]), total_dyn(&mixed));
    println!("{} {}",
        size_of::<&dyn Solid>() == 2 * size_of::<usize>(),
        size_of::<&Cube>() == size_of::<usize>());
}
```
Expected output: `9 9 true true`

*Check 3: edition 2021: a trait object without dyn is error E0782* · `compile_fail` · edition 2021 · host · lib · errors: E0782 · stderr has “expected a type, found a trait” · **✔ oracle pass**
```rust
pub trait Solid {
    fn volume(&self) -> f64;
}
pub fn total(items: &[Box<Solid>]) -> f64 {
    items.iter().map(|s| s.volume()).sum()
}
```

*Check 4: edition 2015: the same code only warns (bare_trait_objects)* · `compiles` · edition 2015 · host · lib · lints: bare_trait_objects · **✔ oracle pass**
```rust
pub trait Solid {
    fn volume(&self) -> f64;
}
pub fn total(items: &[Box<Solid>]) -> f64 {
    items.iter().map(|s| s.volume()).sum()
}
```

*Check 5: edition 2018: the same code only warns (bare_trait_objects)* · `compiles` · edition 2018 · host · lib · lints: bare_trait_objects · **✔ oracle pass**
```rust
pub trait Solid {
    fn volume(&self) -> f64;
}
pub fn total(items: &[Box<Solid>]) -> f64 {
    items.iter().map(|s| s.volume()).sum()
}
```

## Satisfy the orphan rule with a local newtype and forward its methods; Deref does not confer trait impls
**You may implement a trait only when the trait or the type is local to your crate (E0117 otherwise); a one-field wrapper struct makes the type local at no run-time cost, but Deref on that wrapper only forwards method calls and does not make the wrapper implement the inner type's traits.**

*Check 1: a foreign trait on a foreign type is E0117 (Display for Vec<f64>)* · `compile_fail` · edition 2024 · host · lib · errors: E0117 · stderr has “define and implement a trait or new type instead” · **✔ oracle pass**
```rust
use std::fmt;

impl fmt::Display for Vec<f64> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{} samples", self.len())
    }
}
```

*Check 2: std Hash on Rapier's Vector is E0117 too* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0117 · stderr has “only traits defined in the current crate can be implemented for types defined outside of the crate” · **✔ oracle pass**
```rust
use rapier3d_f64::math::Vector;
use std::hash::{Hash, Hasher};

impl Hash for Vector {
    fn hash<H: Hasher>(&self, h: &mut H) {
        self.x.to_bits().hash(h)
    }
}
```

*Check 3: a local newtype over Rapier's Vector may implement Eq and Hash by bits* · `compiles` · edition 2021 · host · lib · deps: rapier3d_f64 · no warnings · **✔ oracle pass**
```rust
use rapier3d_f64::math::Vector;
use std::hash::{Hash, Hasher};

/// A position key: identity is the bit pattern of each component.
#[derive(Clone, Copy, Debug)]
pub struct Key3(pub Vector);

impl PartialEq for Key3 {
    fn eq(&self, o: &Self) -> bool {
        self.0.x.to_bits() == o.0.x.to_bits()
            && self.0.y.to_bits() == o.0.y.to_bits()
            && self.0.z.to_bits() == o.0.z.to_bits()
    }
}
impl Eq for Key3 {}
impl Hash for Key3 {
    fn hash<H: Hasher>(&self, h: &mut H) {
        self.0.x.to_bits().hash(h);
        self.0.y.to_bits().hash(h);
        self.0.z.to_bits().hash(h);
    }
}
```

*Check 4: the newtype Samples(Vec<f64>) implements Display and delegates len()* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::fmt;

struct Samples(Vec<f64>);

impl Samples {
    fn len(&self) -> usize { self.0.len() } // delegate what you need
}
impl fmt::Display for Samples {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let parts: Vec<String> = self.0.iter().map(|v| v.to_string()).collect();
        write!(f, "[{}]", parts.join(", "))
    }
}

fn main() {
    let s = Samples(vec![0.5, 1.0, 2.0]);
    println!("{} {}", s, s.len());
}
```
Expected output: `[0.5, 1, 2] 3`

*Check 5: Deref forwards method calls: tagged.volume() resolves to Cube's* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::ops::Deref;

trait Solid {
    fn volume(&self) -> f64;
}
struct Cube(f64);
impl Solid for Cube {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.0 * self.0 }
}

/// A cube plus a tag, "inheriting" from Cube through Deref.
struct Tagged {
    inner: Cube,
    tag: u32,
}
impl Deref for Tagged {
    type Target = Cube;
    fn deref(&self) -> &Cube { &self.inner }
}

fn total<T: Solid>(items: &[T]) -> f64 {
    items.iter().map(|s| s.volume()).sum()
}

fn main() {
    let t = Tagged { inner: Cube(0.5), tag: 7 };
    println!("{} {}", t.volume(), t.tag); // auto-deref to Cube
    let _ = total(&[Cube(1.0)]);
}
```
Expected output: `1 7`

*Check 6: but Deref does not make Tagged implement Solid (E0277)* · `compile_fail` · edition 2024 · host · errors: E0277 · stderr has “the trait bound `Tagged: Solid` is not satisfied” · **✔ oracle pass**
```rust
use std::ops::Deref;

trait Solid {
    fn volume(&self) -> f64;
}
struct Cube(f64);
impl Solid for Cube {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.0 * self.0 }
}

/// A cube plus a tag, "inheriting" from Cube through Deref.
struct Tagged {
    inner: Cube,
    tag: u32,
}
impl Deref for Tagged {
    type Target = Cube;
    fn deref(&self) -> &Cube { &self.inner }
}

fn total<T: Solid>(items: &[T]) -> f64 {
    items.iter().map(|s| s.volume()).sum()
}

fn main() {
    let t = Tagged { inner: Cube(0.5), tag: 7 };
    println!("{} {}", t.volume(), t.tag);
    println!("{}", total(&[t])); // the bound sees Tagged, not Cube
}
```

## Use impl Trait to accept any implementor or return one hidden type; return Box<dyn Trait> for two types
**`impl Trait` in argument position is an anonymous generic parameter; in return position the function picks one concrete type the caller cannot name, and every return path must produce that same type.**

*Check 1: two &impl params may differ; -> impl Iterator returns a closure adapter; Box<dyn> for two* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
trait Solid {
    fn volume(&self) -> f64;
}
struct Cube(f64);
struct Slab(f64, f64, f64);
impl Solid for Cube {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.0 * self.0 }
}
impl Solid for Slab {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.1 * self.2 }
}
// argument position: each parameter is its own anonymous type parameter
fn sum_two(a: &impl Solid, b: &impl Solid) -> f64 {
    a.volume() + b.volume()
}

// return position: one concrete, unnameable type chosen here; no Box
fn ticks(n: u32) -> impl Iterator<Item = f64> {
    (0..n).map(|i| i as f64 / 64.0)
}

// two concrete types: box them behind a trait object
fn pick(flat: bool) -> Box<dyn Solid> {
    if flat { Box::new(Slab(2.0, 0.25, 2.0)) } else { Box::new(Cube(0.5)) }
}

fn main() {
    println!("{}", sum_two(&Cube(0.5), &Slab(2.0, 0.25, 2.0)));
    println!("{:?}", ticks(3).collect::<Vec<_>>());
    println!("{} {}", pick(true).volume(), pick(false).volume());
}
```
Expected output: `9 [0.0, 0.015625, 0.03125] 8 1`

*Check 2: -> impl Solid returning two different types is E0308* · `compile_fail` · edition 2024 · host · lib · errors: E0308 · stderr has “`if` and `else` have incompatible types” · **✔ oracle pass**
```rust
pub trait Solid {
    fn volume(&self) -> f64;
}
pub struct Cube(pub f64);
pub struct Slab(pub f64, pub f64, pub f64);
impl Solid for Cube {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.0 * self.0 }
}
impl Solid for Slab {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.1 * self.2 }
}
pub fn pick(flat: bool) -> impl Solid {
    if flat { Slab(2.0, 0.25, 2.0) } else { Cube(0.5) }
}
```

*Check 3: one named T for both params forces the same type (E0308)* · `compile_fail` · edition 2024 · host · errors: E0308 · stderr has “expected `&Cube`, found `&Slab`” · **✔ oracle pass**
```rust
trait Solid {
    fn volume(&self) -> f64;
}
struct Cube(f64);
struct Slab(f64, f64, f64);
impl Solid for Cube {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.0 * self.0 }
}
impl Solid for Slab {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.1 * self.2 }
}
fn sum_same<T: Solid>(a: &T, b: &T) -> f64 {
    a.volume() + b.volume()
}
fn main() {
    println!("{}", sum_same(&Cube(0.5), &Slab(2.0, 0.25, 2.0)));
}
```

*Check 4: callers cannot turbofish an impl-Trait parameter (E0107)* · `compile_fail` · edition 2024 · host · errors: E0107 · stderr has “`impl Trait` cannot be explicitly specified as a generic argument” · **✔ oracle pass**
```rust
trait Solid {
    fn volume(&self) -> f64;
}
struct Cube(f64);
impl Solid for Cube {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.0 * self.0 }
}
fn show(s: impl Solid) -> f64 {
    s.volume()
}
fn main() {
    println!("{}", show::<Cube>(Cube(0.5)));
}
```

*Check 5: impl Trait is not allowed in a let binding (E0562)* · `compile_fail` · edition 2024 · host · errors: E0562 · stderr has “`impl Trait` is not allowed in the type of variable bindings” · **✔ oracle pass**
```rust
trait Solid {
    fn volume(&self) -> f64;
}
struct Cube(f64);
impl Solid for Cube {
    fn volume(&self) -> f64 { 8.0 * self.0 * self.0 * self.0 }
}
fn main() {
    let c: impl Solid = Cube(0.5);
    println!("{}", c.volume());
}
```

