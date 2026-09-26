# Advanced traits & the type system — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](traits-advanced.md) · [catalog index](README.md)

## Apply the whole orphan rule: a local type before any uncovered type parameter, and no overlapping impls
**For `impl<P1..=Pn> Trait<T1..=Tn> for T0` with a foreign trait, one of T0..=Tn must be local and no uncovered type parameter may appear before the first local one (RFC 2451); `&`, `&mut`, `Box` and `Pin` are fundamental, so `&Local` and `Box<Local>` count as local; overlapping impls are E0119, including overlap that only a future upstream impl could create.**

*Check 1: Foreign trait for a foreign type: Display for Vec<f64> is E0117* · `compile_fail` · edition 2024 · host · lib · errors: E0117 · **✔ oracle pass**
```rust
use std::fmt;
impl fmt::Display for Vec<f64> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result { write!(f, "{}", self.len()) }
}
```

*Check 2: RFC 2451 shapes pass: From<Local> for Vec<T>, Display for Box<Local>* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
pub struct Snapshot(pub Vec<u8>);
// Foreign trait, foreign type, but the first local type (Snapshot) comes before
// any uncovered type parameter: allowed since RFC 2451.
impl<T> From<Snapshot> for Vec<T> {
    fn from(_: Snapshot) -> Vec<T> { Vec::new() }
}
// A fundamental wrapper around a local type counts as local.
impl std::fmt::Display for Box<Snapshot> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { write!(f, "{} bytes", self.0.len()) }
}
fn main() {
    let v: Vec<u32> = Snapshot(vec![1, 2]).into();
    println!("{} {}", v.len(), Box::new(Snapshot(vec![0; 3])));
}
```
Expected output: `0 3 bytes`

*Check 3: An uncovered T before the first local type is E0210* · `compile_fail` · edition 2024 · host · lib · errors: E0210 · **✔ oracle pass**
```rust
pub struct Snapshot(pub Vec<u8>);
impl<T> From<Snapshot> for T {
    fn from(_: Snapshot) -> T { unimplemented!() }
}
```

*Check 4: Blanket impl plus a foreign type is E0119 because upstream may add Display* · `compile_fail` · edition 2024 · host · lib · errors: E0119 · stderr has “upstream crates may add a new impl of trait `std::fmt::Display` for type `std::vec::Vec<u8>`” · **✔ oracle pass**
```rust
use std::fmt::Display;
trait Describe { fn describe(&self) -> String; }
impl<T: Display> Describe for T { fn describe(&self) -> String { format!("{self}") } }
impl Describe for Vec<u8> { fn describe(&self) -> String { format!("{} bytes", self.len()) } }
```

*Check 5: Blanket impl plus a local non-Display type compiles* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::fmt::Display;
trait Describe { fn describe(&self) -> String; }
impl<T: Display> Describe for T { fn describe(&self) -> String { format!("{self}") } }
struct Snapshot(Vec<u8>);   // local, and not Display: this crate alone decides that
impl Describe for Snapshot { fn describe(&self) -> String { format!("{} bytes", self.0.len()) } }
fn main() { println!("{} {}", 2.5f64.describe(), Snapshot(vec![0; 4]).describe()); }
```
Expected output: `2.5 4 bytes`

*Check 6: Blanket impl plus u32 (which is Display) overlaps: E0119* · `compile_fail` · edition 2024 · host · lib · errors: E0119 · **✔ oracle pass**
```rust
use std::fmt::Display;
trait Describe { fn describe(&self) -> String; }
impl<T: Display> Describe for T { fn describe(&self) -> String { format!("{self}") } }
impl Describe for u32 { fn describe(&self) -> String { String::from("u32") } }
```

*Check 7: From<[f64; 17]> for Rapier's Vector is foreign-for-foreign: E0117* · `compile_fail` · edition 2024 · host · lib · deps: rapier3d_f64 · errors: E0117 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::Vector;
// Foreign trait (From), foreign types ([f64; 17] and Rapier's Vector): refused.
impl From<[f64; 17]> for Vector {
    fn from(b: [f64; 17]) -> Vector { Vector::new(b[0], b[1], b[2]) }
}
```

*Check 8: From<&BodyRecord> for Vector is legal: &Local counts as local* · `runs` · edition 2024 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::Vector;
// A local record type makes the conversion legal.
pub struct BodyRecord(pub [f64; 17]);
impl From<&BodyRecord> for Vector {
    fn from(b: &BodyRecord) -> Vector { Vector::new(b.0[0], b.0[1], b.0[2]) }
}
fn main() {
    let mut raw = [0.0; 17];
    raw[1] = 1.5;
    let v: Vector = (&BodyRecord(raw)).into();
    println!("{} {} {}", v.x, v.y, v.z);
}
```
Expected output: `0 1.5 0`

## Choose associated types for one-impl-per-type outputs; enforce associated consts and GATs at compile time
**An associated type fixes one output per implementing type (a second impl is E0119) while a generic parameter allows many impls; an associated const is evaluated only when an instantiated path references it; generic associated types (stable since 1.65) let an associated type borrow from self.**

*Check 1: A second impl of a trait with an associated type conflicts (E0119)* · `compile_fail` · edition 2024 · host · lib · errors: E0119 · **✔ oracle pass**
```rust
trait Law {
    type Input;
    fn step(&mut self, input: Self::Input) -> u32;
}
struct BoxLaw;
impl Law for BoxLaw {
    type Input = (u32, u32);
    fn step(&mut self, input: (u32, u32)) -> u32 { input.0 + input.1 }
}
impl Law for BoxLaw {
    type Input = f64;
    fn step(&mut self, _input: f64) -> u32 { 0 }
}
fn main() {}
```

*Check 2: A generic-parameter trait allows Integrate<f32> and Integrate<f64> on one type* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
trait Integrate<T> {
    fn integrate(&self, x: T, v: T) -> T;
}
struct Euler;
impl Integrate<f32> for Euler {
    fn integrate(&self, x: f32, v: f32) -> f32 { x + v / 64.0 }
}
impl Integrate<f64> for Euler {
    fn integrate(&self, x: f64, v: f64) -> f64 { x + v / 64.0 }
}
fn main() {
    let e = Euler;
    let a: f32 = e.integrate(1.0f32, 2.0f32);
    let b = <Euler as Integrate<f64>>::integrate(&e, 1.0, 2.0);
    println!("{a} {b}");
}
```
Expected output: `1.03125 1.03125`

*Check 3: A zero-stride impl compiles while nothing instantiates the assert that forbids it* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
trait Law {
    const STRIDE: usize;
    const STRIDE_OK: () = assert!(Self::STRIDE > 0, "a law needs a non-zero stride");
    fn stride() -> usize {
        let () = Self::STRIDE_OK;
        Self::STRIDE
    }
}
struct BoxLaw;
impl Law for BoxLaw { const STRIDE: usize = 17; }
struct Broken;
impl Law for Broken { const STRIDE: usize = 0; }
fn main() {
    println!("{}", BoxLaw::stride());
}
```
Expected output: `17`

*Check 4: Calling stride() on the zero-stride impl evaluates the assert: E0080 at build time* · `compile_fail` · edition 2024 · host · bin · errors: E0080 · stderr has “a law needs a non-zero stride” · **✔ oracle pass**
```rust
trait Law {
    const STRIDE: usize;
    const STRIDE_OK: () = assert!(Self::STRIDE > 0, "a law needs a non-zero stride");
    fn stride() -> usize {
        let () = Self::STRIDE_OK;
        Self::STRIDE
    }
}
struct BoxLaw;
impl Law for BoxLaw { const STRIDE: usize = 17; }
struct Broken;
impl Law for Broken { const STRIDE: usize = 0; }
fn main() {
    println!("{}", BoxLaw::stride());
    println!("{}", Broken::stride());
}
```

*Check 5: In a library, a private dead helper does not trigger the assert* · `compiles` · edition 2024 · host · lib · **✔ oracle pass**
```rust
pub trait Law {
    const STRIDE: usize;
    const STRIDE_OK: () = assert!(Self::STRIDE > 0, "a law needs a non-zero stride");
    fn stride() -> usize {
        let () = Self::STRIDE_OK;
        Self::STRIDE
    }
}
pub struct Broken;
impl Law for Broken { const STRIDE: usize = 0; }
// A private, unused path: nothing instantiates Broken::stride, so no error.
#[allow(dead_code)]
fn never_called() -> usize { Broken::stride() }
```

*Check 6: In a library, a pub fn reaching the zero-stride impl fails with E0080* · `compile_fail` · edition 2024 · host · lib · errors: E0080 · **✔ oracle pass**
```rust
pub trait Law {
    const STRIDE: usize;
    const STRIDE_OK: () = assert!(Self::STRIDE > 0, "a law needs a non-zero stride");
    fn stride() -> usize {
        let () = Self::STRIDE_OK;
        Self::STRIDE
    }
}
pub struct Broken;
impl Law for Broken { const STRIDE: usize = 0; }
// An exported path instantiates it, so the library build fails.
pub fn exported() -> usize { Broken::stride() }
```

*Check 7: A generic associated const cannot size an array on stable Rust* · `compile_fail` · edition 2024 · host · lib · stderr has “generic parameters may not be used in const operations” · **✔ oracle pass**
```rust
trait Law { const STRIDE: usize; }
fn zeroed<L: Law>() -> [f64; L::STRIDE] { [0.0; L::STRIDE] }
```

*Check 8: A concrete <BoxLaw as Law>::STRIDE does size a static buffer* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
trait Law { const STRIDE: usize; }
struct BoxLaw;
impl Law for BoxLaw { const STRIDE: usize = 17; }
static BODIES: [f64; 64 * <BoxLaw as Law>::STRIDE] = [0.0; 64 * <BoxLaw as Law>::STRIDE];
fn main() { println!("{}", BODIES.len()); }
```
Expected output: `1088`

*Check 9: A GAT lending iterator hands out &mut body slices one at a time* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
// A lending iterator: each item borrows the iterator mutably, so two items
// can never be alive at once. std's Iterator cannot express this.
trait LendingIterator {
    type Item<'a> where Self: 'a;
    fn next<'a>(&'a mut self) -> Option<Self::Item<'a>>;
}
struct BodiesMut<'s> { buf: &'s mut [f64], stride: usize, at: usize }
impl<'s> LendingIterator for BodiesMut<'s> {
    type Item<'a> = &'a mut [f64] where Self: 'a;
    fn next<'a>(&'a mut self) -> Option<&'a mut [f64]> {
        let start = self.at * self.stride;
        if start + self.stride > self.buf.len() { return None; }
        self.at += 1;
        Some(&mut self.buf[start..start + self.stride])
    }
}
fn main() {
    let mut buf = [0.0f64; 6];
    let mut it = BodiesMut { buf: &mut buf, stride: 3, at: 0 };
    let mut k = 0.0;
    while let Some(body) = it.next() {
        body[1] = k; // y of each body
        k += 1.0;
    }
    println!("{:?}", buf);
}
```
Expected output: `[0.0, 0.0, 0.0, 0.0, 1.0, 0.0]`

*Check 10: Omitting `where Self: 'a` on the GAT is a hard error without a code* · `compile_fail` · edition 2024 · host · lib · stderr has “missing required bound on `Item`” · **✔ oracle pass**
```rust
trait LendingIterator {
    type Item<'a>;
    fn next<'a>(&'a mut self) -> Option<Self::Item<'a>>;
}
fn main() {}
```

## Choose variance on purpose: &'a T, Box and Vec are covariant; &mut T and Cell invariant; fn(T) contravariant
**Rust subtyping is over lifetimes (`&'static str` is a subtype of `&'a str`); covariant constructors pass it through (`&'a T`, `*const T`, `[T]`, `fn() -> T`, `PhantomData<T>`, Box, Vec), `fn(T)` flips it, and `&'a mut T` (in T), `*mut T`, `UnsafeCell<T>`/`Cell<T>` and `dyn Trait<T>` (in T) forbid it; a struct takes the combination of its fields, and a parameter used both ways becomes invariant.**

*Check 1: &mut T is invariant: assign(&mut &'static str, &local) is E0597* · `compile_fail` · edition 2024 · host · bin · errors: E0597 · **✔ oracle pass**
```rust
fn assign<T>(input: &mut T, val: T) { *input = val; }
fn main() {
    let mut hello: &'static str = "hello";
    {
        let world = String::from("world");
        assign(&mut hello, &world);   // &mut T is invariant in T: T must be &'static str
    }
    println!("{hello}");
}
```

*Check 2: &'a T, Box<T> and Vec<T> are covariant: 'static shortens to 'a* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
// Covariance: a longer-lived reference is usable where a shorter one is expected,
// through &'a T, Box<T> and Vec<T> alike.
fn shorten<'a>(x: &'static str, b: Box<&'static str>, v: Vec<&'static str>) -> (&'a str, Box<&'a str>, Vec<&'a str>) {
    (x, b, v)
}
fn main() {
    let (a, b, v) = shorten("x", Box::new("y"), vec!["z"]);
    println!("{a}{b}{}", v[0]);
}
```
Expected output: `xyz`

*Check 3: fn(&'a str) is accepted where fn(&'static str) is expected (contravariance)* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
// Contravariance: fn(&'a str) is a subtype of fn(&'static str), because
// &'static str is a subtype of &'a str and fn(T) flips the direction.
fn wants_static_sink(f: fn(&'static str)) { f("quantum") }
fn pass<'a>(f: fn(&'a str)) { wants_static_sink(f) }
fn print_it(s: &str) { println!("{s}"); }
fn main() { pass(print_it); }
```
Expected output: `quantum`

*Check 4: The reverse, fn(&'static str) for fn(&'a str), is refused (E0521)* · `compile_fail` · edition 2024 · host · lib · errors: E0521 · **✔ oracle pass**
```rust
// The other direction is refused: a sink that only accepts &'static str
// cannot stand in for one that must accept a short-lived borrow.
fn wants_any_sink<'a>(f: fn(&'a str), s: &'a str) { f(s) }
fn pass_static<'a>(f: fn(&'static str), s: &'a str) { wants_any_sink(f, s) }
fn main() {}
```

*Check 5: Cell<T> is invariant: Cell<&'static str> will not become Cell<&'a str>* · `compile_fail` · edition 2024 · host · lib · stderr has “the struct `Cell<T>` is invariant over the parameter `T`” · **✔ oracle pass**
```rust
use std::cell::Cell;
// Cell<T> is invariant in T, like &mut T.
fn shorten_cell<'a>(c: Cell<&'static str>) -> Cell<&'a str> { c }
fn main() {}
```

*Check 6: PhantomData<fn(&'id ()) -> &'id ()> makes a user struct invariant in 'id* · `compile_fail` · edition 2024 · host · lib · stderr has “the struct `Brand<'id>` is invariant over the parameter `'id`” · **✔ oracle pass**
```rust
use std::marker::PhantomData;
// PhantomData<fn(T) -> T> makes the parameter invariant in a user type.
struct Brand<'id>(PhantomData<fn(&'id ()) -> &'id ()>);
fn shrink<'a>(b: Brand<'static>) -> Brand<'a> { b }
fn main() {}
```

## Control what impl Trait captures: RPITIT/async fn in traits (1.75), use<..> (1.82; traits 1.87), 2024 rules
**A free function's `-> impl Trait` captures every in-scope lifetime in edition 2024 but only lifetimes named in its bounds in 2021; `use<..>` (1.82) states the captured set in any edition and, since 1.87, inside trait definitions; `-> impl Trait` and `async fn` in traits (1.75) capture every in-scope lifetime in every edition unless a `use<..>` bound narrows it, and make the trait dyn-incompatible.**

*Check 1: Edition 2021: returning a borrow through a free fn's impl Trait is E0700* · `compile_fail` · edition 2021 · host · lib · errors: E0700 · stderr has “captures lifetime that does not appear in bounds” · **✔ oracle pass**
```rust
// Edition 2021: a free function's impl Trait does not capture the elided
// lifetime of `v`, so returning a borrow of it is refused.
fn ys(v: &[f64]) -> impl Iterator<Item = f64> {
    v.chunks_exact(17).map(|b| b[1])
}
fn main() {}
```

*Check 2: Edition 2024: the same free fn captures the lifetime and compiles* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
// Edition 2024: the same signature captures every in-scope lifetime.
fn ys(v: &[f64]) -> impl Iterator<Item = f64> {
    v.chunks_exact(17).map(|b| b[1])
}
fn main() {
    let mut bodies = vec![0.0; 34];
    bodies[1] = 1.0;
    bodies[18] = 2.0;
    println!("{:?}", ys(&bodies).collect::<Vec<_>>());
}
```
Expected output: `[1.0, 2.0]`

*Check 3: Edition 2021: a non-borrowing result leaves the argument free to mutate* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// Edition 2021: the same function does not capture the elided lifetime,
// so the caller may mutate `v` while the iterator is alive.
fn indices(v: &Vec<f64>) -> impl Iterator<Item = usize> { 0..v.len() }
fn main() {
    let mut v = vec![0.0; 3];
    let it = indices(&v);
    v.push(1.0);
    println!("{} {}", it.count(), v.len());
}
```
Expected output: `3 4`

*Check 4: Edition 2024: the same code overcaptures and is E0502* · `compile_fail` · edition 2024 · host · bin · errors: E0502 · stderr has “Rust 2024 has adjusted the `impl Trait` lifetime capture rules” · **✔ oracle pass**
```rust
// Edition 2024 overcapture: the iterator does not borrow `v`, but its type says it does.
fn indices(v: &Vec<f64>) -> impl Iterator<Item = usize> { 0..v.len() }
fn main() {
    let mut v = vec![0.0; 3];
    let it = indices(&v);
    v.push(1.0);
    println!("{}", it.count());
}
```

*Check 5: Edition 2024: + use<> captures nothing and the mutation is allowed* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
// use<> says: capture nothing. The borrow ends at the call.
fn indices(v: &Vec<f64>) -> impl Iterator<Item = usize> + use<> { 0..v.len() }
fn main() {
    let mut v = vec![0.0; 3];
    let it = indices(&v);
    v.push(1.0);
    println!("{} {}", it.count(), v.len());
}
```
Expected output: `3 4`

*Check 6: impl_trait_overcaptures flags a 2021 signature that 2024 would change* · `compiles` · edition 2021 · host · lib · stderr has “will capture more lifetimes than possibly intended in edition 2024” · **✔ oracle pass**
```rust
// Edition 2021 crate: the migration lint names what 2024 would capture.
pub fn indices(v: &Vec<f64>) -> impl Iterator<Item = usize> { 0..v.len() }
```

*Check 7: Edition 2021 trait method: RPITIT captures &self anyway* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// Edition 2021, but inside a trait: return-position impl Trait captures the
// &self lifetime anyway (traits used the 2024 capture rules from 1.75 on).
trait Bodies {
    fn ys(&self) -> impl Iterator<Item = f64>;
}
struct World { buf: Vec<f64> }
impl Bodies for World {
    fn ys(&self) -> impl Iterator<Item = f64> { self.buf.chunks_exact(17).map(|b| b[1]) }
}
fn main() {
    let mut w = World { buf: vec![0.0; 34] };
    w.buf[18] = 3.0;
    println!("{:?}", w.ys().collect::<Vec<_>>());
}
```
Expected output: `[0.0, 3.0]`

*Check 8: A trait with an RPITIT method cannot be dyn (E0038)* · `compile_fail` · edition 2024 · host · lib · errors: E0038 · stderr has “references an `impl Trait` type in its return type” · **✔ oracle pass**
```rust
trait Bodies {
    fn ys(&self) -> impl Iterator<Item = f64>;
}
pub fn count(b: &dyn Bodies) -> usize { b.ys().count() }
fn main() {}
```

*Check 9: async fn in a pub trait triggers the async_fn_in_trait lint* · `compiles` · edition 2024 · host · lib · lints: async_fn_in_trait · **✔ oracle pass**
```rust
pub trait Loader {
    async fn load(&self, world_id: u32) -> bool;
}
```

*Check 10: The desugared fn -> impl Future + Send compiles without warnings* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub trait Loader {
    fn load(&self, world_id: u32) -> impl std::future::Future<Output = bool> + Send;
}
```

*Check 11: 1.87+: use<Self> in a trait method; the iterator does not borrow the world* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
// 1.87+: use<..> inside a trait. It must list Self; leaving out the &self
// lifetime promises callers the iterator does not borrow the world.
trait Bodies {
    fn ids(&self) -> impl Iterator<Item = u32> + use<Self>;
}
struct World { n: u32 }
impl Bodies for World {
    fn ids(&self) -> impl Iterator<Item = u32> + use<> { 0..self.n }
}
fn main() {
    let mut w = World { n: 2 };
    let it = w.ids();
    w.n = 5;                       // allowed: `it` does not borrow `w`
    println!("{} {}", it.count(), w.n);
}
```
Expected output: `2 5`

*Check 12: use<> in a trait definition must still mention Self* · `compile_fail` · edition 2024 · host · lib · stderr has “must mention the `Self` type of the trait in `use<...>`” · **✔ oracle pass**
```rust
trait Bodies {
    fn ids(&self) -> impl Iterator<Item = u32> + use<>;
}
fn main() {}
```

*Check 13: In the impl, use<Self> is refused: Self is an alias there (E0799)* · `compile_fail` · edition 2024 · host · bin · errors: E0799 · **✔ oracle pass**
```rust
trait Bodies {
    fn ids(&self) -> impl Iterator<Item = u32> + use<Self>;
}
struct World { n: u32 }
impl Bodies for World {
    fn ids(&self) -> impl Iterator<Item = u32> + use<Self> { 0..self.n }
}
fn main() {
    let mut w = World { n: 2 };
    let it = w.ids();
    w.n = 5;
    println!("{} {}", it.count(), w.n);
}
```

## Encode solver states as zero-sized type parameters, seal traits privately, and import extension traits
**A zero-sized state marker (`Solver<Unloaded>`/`Solver<Loaded>` over `PhantomData<S>`) turns an out-of-order call into E0599 at no size cost; a public trait with a supertrait in a private module cannot be implemented outside that module (E0277, E0603); an extension trait adds methods to a foreign type such as f64, callable only where the trait is imported (E0599 otherwise).**

*Check 1: Typestate: step exists on Solver<Loaded>; the ZST marker adds no bytes* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::marker::PhantomData;
use std::mem::size_of;
// Typestate: the state is a zero-sized type parameter, so `step` exists only
// on a loaded solver and the marker costs no bytes.
pub struct Unloaded;
pub struct Loaded;
pub struct Solver<S> { quanta: u64, _state: PhantomData<S> }
impl Solver<Unloaded> {
    pub fn new() -> Self { Solver { quanta: 0, _state: PhantomData } }
    pub fn load(self) -> Solver<Loaded> { Solver { quanta: self.quanta, _state: PhantomData } }
}
impl Solver<Loaded> {
    pub fn step(&mut self) { self.quanta += 1; }
}
fn main() {
    let mut s = Solver::new().load();
    s.step();
    s.step();
    println!("{} {} {}", s.quanta, size_of::<Solver<Loaded>>(), size_of::<u64>());
}
```
Expected output: `2 8 8`

*Check 2: Calling step on Solver<Unloaded> is E0599* · `compile_fail` · edition 2024 · host · bin · errors: E0599 · **✔ oracle pass**
```rust
use std::marker::PhantomData;
pub struct Unloaded;
pub struct Loaded;
pub struct Solver<S> { quanta: u64, _state: PhantomData<S> }
impl Solver<Unloaded> {
    pub fn new() -> Self { Solver { quanta: 0, _state: PhantomData } }
}
impl Solver<Loaded> {
    pub fn step(&mut self) { self.quanta += 1; }
}
fn main() {
    let mut s = Solver::new();
    s.step();   // no `step` on Solver<Unloaded>
}
```

*Check 3: Implementing a sealed trait from outside is E0277; rustc calls it a sealed trait* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “is a "sealed trait"” · **✔ oracle pass**
```rust
mod law {
    mod private { pub trait Sealed {} }
    /// Sealed: only this module can add a law.
    pub trait Law: private::Sealed { fn name(&self) -> &'static str; }
    pub struct BoxLaw;
    impl private::Sealed for BoxLaw {}
    impl Law for BoxLaw { fn name(&self) -> &'static str { "box" } }
}
struct Rogue;
impl law::Law for Rogue { fn name(&self) -> &'static str { "rogue" } }
fn main() {}
```

*Check 4: Naming the private Sealed supertrait from outside is E0603* · `compile_fail` · edition 2024 · host · lib · errors: E0603 · **✔ oracle pass**
```rust
mod law {
    mod private { pub trait Sealed {} }
    pub trait Law: private::Sealed { fn name(&self) -> &'static str; }
}
struct Rogue;
impl law::private::Sealed for Rogue {}
fn main() {}
```

*Check 5: An extension trait on f64 canonicalises -0.0 to +0.0 bits* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
mod canon {
    /// Extension trait: a method added to a foreign type (f64).
    pub trait CanonZero { fn canon_zero(self) -> f64; }
    impl CanonZero for f64 {
        fn canon_zero(self) -> f64 { if self == 0.0 { 0.0 } else { self } }
    }
}
use canon::CanonZero;
fn main() {
    let z = -0.0f64;
    println!("{:#x} {:#x}", z.to_bits(), z.canon_zero().to_bits());
}
```
Expected output: `0x8000000000000000 0x0`

*Check 6: Without the use, the extension method is not found (E0599)* · `compile_fail` · edition 2024 · host · bin · errors: E0599 · stderr has “items from traits can only be used if the trait is in scope” · **✔ oracle pass**
```rust
mod canon {
    pub trait CanonZero { fn canon_zero(self) -> f64; }
    impl CanonZero for f64 {
        fn canon_zero(self) -> f64 { if self == 0.0 { 0.0 } else { self } }
    }
}
fn main() {
    let z = -0.0f64;
    println!("{}", z.canon_zero());   // trait not in scope
}
```

*Check 7: Boundary keeps one Option check; restore swaps in a complete value or changes nothing* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// The export boundary cannot carry a typestate (the host calls exports in any
// order), so it keeps one Option check; everything inside takes &mut Loaded.
struct Loaded { quanta: u64 }
struct Solver { loaded: Option<Loaded> }
fn integrate(l: &mut Loaded) -> bool { l.quanta += 1; true }
fn decode(bytes: &[u8]) -> Option<Loaded> {
    let raw: [u8; 8] = bytes.try_into().ok()?;          // wrong length: refuse
    Some(Loaded { quanta: u64::from_le_bytes(raw) })
}
fn solver_step(s: &mut Solver) -> u32 {
    let Some(l) = s.loaded.as_mut() else { return 0 };  // step before load: refuse
    if integrate(l) { 1 } else { 0 }
}
fn solver_restore(s: &mut Solver, bytes: &[u8]) -> u32 {
    let Some(fresh) = decode(bytes) else { return 0 };  // refusal changes nothing
    s.loaded = Some(fresh);                             // swap in a complete value
    1
}
fn main() {
    let mut s = Solver { loaded: None };
    let before = solver_step(&mut s);
    let ok = solver_restore(&mut s, &41u64.to_le_bytes());
    let stepped = solver_step(&mut s);
    let bad = solver_restore(&mut s, &[1, 2, 3]);
    println!("{before} {ok} {stepped} {bad} {}", s.loaded.as_ref().unwrap().quanta);
}
```
Expected output: `0 1 1 0 42`

## Keep a trait dyn compatible or fence methods with `where Self: Sized`; a &dyn is two words: data + vtable
**A trait can be a `dyn` base only if its supertraits are dyn compatible, `Sized` is not a supertrait, it has no associated consts and no GATs, and each method is dispatchable (no type parameters, `Self` only in the receiver `&self`/`&mut self`/`Box<Self>`/`Rc<Self>`/`Arc<Self>`/`Pin<P>`, no `async fn`, no `-> impl Trait`) or is excluded by `where Self: Sized`; otherwise E0038, which on 1.98.1 reads 'the trait `X` is not dyn compatible' (formerly 'object safety').**

*Check 1: A generic method makes the trait dyn-incompatible (E0038, 'not dyn compatible')* · `compile_fail` · edition 2024 · host · lib · errors: E0038 · stderr has “is not dyn compatible” · stderr has “has generic type parameters” · **✔ oracle pass**
```rust
trait Probe {
    fn sample(&self) -> f64;
    fn visit<V: FnMut(f64)>(&self, v: V);
}
struct Height(f64);
impl Probe for Height {
    fn sample(&self) -> f64 { self.0 }
    fn visit<V: FnMut(f64)>(&self, mut v: V) { v(self.0) }
}
pub fn read(p: &dyn Probe) -> f64 { p.sample() }
fn main() {}
```

*Check 2: `where Self: Sized` on the generic method restores `&dyn Probe`* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
trait Probe {
    fn sample(&self) -> f64;
    fn visit<V: FnMut(f64)>(&self, v: V) where Self: Sized;
}
struct Height(f64);
impl Probe for Height {
    fn sample(&self) -> f64 { self.0 }
    fn visit<V: FnMut(f64)>(&self, mut v: V) { v(self.0) }
}
fn main() {
    let h = Height(2.5);
    let d: &dyn Probe = &h;
    let mut seen = 0.0;
    h.visit(|x| seen = x);      // static dispatch: fine on the concrete type
    println!("{} {}", d.sample(), seen);
}
```
Expected output: `2.5 2.5`

*Check 3: The fenced method cannot be called on the trait object* · `compile_fail` · edition 2024 · host · bin · stderr has “cannot be invoked on a trait object” · **✔ oracle pass**
```rust
trait Probe {
    fn sample(&self) -> f64;
    fn visit<V: FnMut(f64)>(&self, v: V) where Self: Sized;
}
struct Height(f64);
impl Probe for Height {
    fn sample(&self) -> f64 { self.0 }
    fn visit<V: FnMut(f64)>(&self, mut v: V) { v(self.0) }
}
fn main() {
    let d: &dyn Probe = &Height(2.5);
    d.visit(|_| {});            // excluded from the vtable
}
```

*Check 4: An associated const makes the trait dyn-incompatible (E0038)* · `compile_fail` · edition 2024 · host · lib · errors: E0038 · stderr has “contains associated const `STRIDE`” · **✔ oracle pass**
```rust
trait Law {
    const STRIDE: usize;
    fn step(&mut self) -> u32;
}
pub fn run(l: &mut dyn Law) -> u32 { l.step() }
fn main() {}
```

*Check 5: A generic associated type makes the trait dyn-incompatible (E0038)* · `compile_fail` · edition 2024 · host · lib · errors: E0038 · stderr has “contains generic associated type `Item`” · **✔ oracle pass**
```rust
trait LendingIterator {
    type Item<'a> where Self: 'a;
    fn next<'a>(&'a mut self) -> Option<Self::Item<'a>>;
}
fn use_dyn(_: &mut dyn LendingIterator<Item<'static> = &'static mut [f64]>) {}
fn main() {}
```

*Check 6: &dyn, Box<dyn> and &[f64] are two usizes; &f64 is one (host)* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::mem::size_of;
trait Probe { fn sample(&self) -> f64; }
fn main() {
    let w = size_of::<usize>();
    println!("{} {} {} {}",
        size_of::<&f64>() == w,
        size_of::<&[f64]>() == 2 * w,
        size_of::<&dyn Probe>() == 2 * w,
        size_of::<Box<dyn Probe>>() == 2 * w);
}
```
Expected output: `true true true true`

*Check 7: On wasm32 a &dyn pointer is 8 bytes: two 32-bit words* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports dyn_ptr_bytes · node calls dyn_ptr_bytes() · **✔ oracle pass**
```rust
trait Probe { fn sample(&self) -> f64; }
struct Height(f64);
impl Probe for Height { fn sample(&self) -> f64 { self.0 } }
// On wasm32 a pointer is 4 bytes, so &dyn Probe (data + vtable) is 8.
#[no_mangle]
pub extern "C" fn dyn_ptr_bytes() -> u32 {
    let h = Height(1.0);
    let d: &dyn Probe = &h;
    let _ = d.sample();
    core::mem::size_of::<&dyn Probe>() as u32
}
```
Expected output: `8`

*Check 8: An implicit Sized bound rejects T = str (E0277)* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “the size for values of type `str` cannot be known at compilation time” · **✔ oracle pass**
```rust
use std::fmt::Debug;
fn show<T: Debug>(t: &T) -> String { format!("{t:?}") }
fn main() {
    let s: &str = "slab";
    println!("{}", show(s));        // T = str, which is not Sized
}
```

*Check 9: `T: ?Sized` accepts str and [f64] behind a reference* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::fmt::Debug;
fn show<T: Debug + ?Sized>(t: &T) -> String { format!("{t:?}") }
fn main() {
    let s: &str = "slab";
    let heights: &[f64] = &[0.0, 0.5];
    println!("{} {}", show(s), show(heights));
}
```
Expected output: `"slab" [0.0, 0.5]`

*Check 10: Box<dyn Probe> is Box<dyn Probe + 'static>: a borrowing probe is refused* · `compile_fail` · edition 2024 · host · lib · stderr has “lifetime may not live long enough” · stderr has “must outlive `'static`” · **✔ oracle pass**
```rust
trait Probe { fn sample(&self) -> f64; }
struct View<'a>(&'a [f64]);
impl Probe for View<'_> { fn sample(&self) -> f64 { self.0[0] } }
// Box<dyn Probe> means Box<dyn Probe + 'static>: a borrowing probe does not fit.
fn boxed(v: &[f64]) -> Box<dyn Probe> { Box::new(View(v)) }
fn main() {}
```

*Check 11: Box<dyn Probe + '_> carries the borrow* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
trait Probe { fn sample(&self) -> f64; }
struct View<'a>(&'a [f64]);
impl Probe for View<'_> { fn sample(&self) -> f64 { self.0[0] } }
fn boxed(v: &[f64]) -> Box<dyn Probe + '_> { Box::new(View(v)) }
fn main() { let h = [0.75]; println!("{}", boxed(&h).sample()); }
```
Expected output: `0.75`

## Let auto traits follow the fields, steer them with PhantomData, and know a Drop impl drives drop check
**Send, Sync, Unpin, UnwindSafe and RefUnwindSafe are auto traits: a struct gets one when all its fields have it, and stable code cannot write negative impls; `PhantomData<*const ()>` removes Send and Sync, `PhantomData<fn() -> T>` keeps a typed handle Send + Sync whatever T is, and since RFC 1238 a `PhantomData<T>` field is superfluous for drop check when the type has an explicit Drop impl: the Drop impl itself makes drop check strict, while the phantom still sets variance and auto traits.**

*Check 1: An Rc field makes the whole struct !Send (E0277)* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “cannot be sent between threads safely” · **✔ oracle pass**
```rust
use std::rc::Rc;
fn assert_send<T: Send>() {}
struct Cache { shared: Rc<Vec<f64>> }   // Rc makes the whole struct !Send
fn main() { assert_send::<Cache>(); }
```

*Check 2: PhantomData<*const ()> opts a type out of Send and Sync on stable* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · **✔ oracle pass**
```rust
use std::marker::PhantomData;
fn assert_send<T: Send>() {}
fn assert_sync<T: Sync>() {}
// A raw-pointer phantom opts the type out of Send and Sync on stable Rust,
// without a negative impl (those are std-only).
struct WorldToken { id: u32, _not_thread_safe: PhantomData<*const ()> }
fn main() { assert_send::<WorldToken>(); assert_sync::<WorldToken>(); }
```

*Check 3: PhantomData<fn() -> T> handle: 4 bytes, Send + Sync even for T = Rc* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::marker::PhantomData;
use std::mem::size_of;
use std::rc::Rc;
fn assert_send_sync<T: Send + Sync>() {}
// A typed index: PhantomData<fn() -> T> is covariant in T and Send + Sync
// whatever T is, and it costs zero bytes.
struct Handle<T> { index: u32, _for: PhantomData<fn() -> T> }
struct Body; struct Collider;
fn main() {
    assert_send_sync::<Handle<Rc<f64>>>();   // Rc is !Send, the handle still is
    let b: Handle<Body> = Handle { index: 3, _for: PhantomData };
    let c: Handle<Collider> = Handle { index: 3, _for: PhantomData };
    println!("{} {} {}", size_of::<Handle<Body>>(), b.index, c.index);
}
```
Expected output: `4 3 3`

*Check 4: Handle<Collider> where Handle<Body> is wanted is E0308* · `compile_fail` · edition 2024 · host · bin · errors: E0308 · **✔ oracle pass**
```rust
use std::marker::PhantomData;
struct Handle<T> { index: u32, _for: PhantomData<fn() -> T> }
struct Body; struct Collider;
fn wake(_: Handle<Body>) {}
fn main() {
    let c: Handle<Collider> = Handle { index: 3, _for: PhantomData };
    wake(c);
}
```

*Check 5: A Drop impl makes drop check reject the dangling borrow (E0597)* · `compile_fail` · edition 2024 · host · bin · errors: E0597 · stderr has “runs the `Drop` code for type `Inspector`” · **✔ oracle pass**
```rust
struct Inspector<'a>(&'a u8);
impl Drop for Inspector<'_> {
    fn drop(&mut self) { println!("inspecting {}", self.0); }
}
fn main() {
    let (inspector, days);
    days = Box::new(1);
    inspector = Inspector(&days);
    let _ = &inspector;
}
```

*Check 6: Without the Drop impl the same borrow compiles* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
struct Inspector<'a>(&'a u8);   // no Drop impl: drop check has nothing to protect
fn main() {
    let (inspector, days);
    days = Box::new(1);
    inspector = Inspector(&days);
    println!("{}", inspector.0);
}
```
Expected output: `1`

*Check 7: rapier 0.35.3 EventHandler requires Sync via MaybeSync: RefCell log is E0277* · `compile_fail` · edition 2024 · host · lib · deps: rapier3d_f64 · errors: E0277 · stderr has “required for `Log` to implement `MaybeSync`” · **✔ oracle pass**
```rust
use std::cell::RefCell;
use rapier3d_f64::prelude::*;
// EventHandler: MaybeSync, and MaybeSync: Sync unless rapier's
// `unsync-callbacks` feature is on. A RefCell log is not Sync.
struct Log { started: RefCell<u32> }
impl EventHandler for Log {
    fn handle_collision_event(&self, _: &RigidBodySet, _: &ColliderSet, e: CollisionEvent, _: Option<&ContactPair>) {
        if e.started() { *self.started.borrow_mut() += 1; }
    }
    fn handle_contact_force_event(&self, _: f64, _: &RigidBodySet, _: &ColliderSet, _: &ContactPair, _: f64) {}
}
fn main() {}
```

*Check 8: An AtomicU32 log satisfies MaybeSync and counts one started collision* · `runs` · edition 2024 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use std::sync::atomic::{AtomicU32, Ordering};
use rapier3d_f64::prelude::*;
// An atomic counter is Sync, so the handler satisfies the supertrait.
struct Log { started: AtomicU32 }
impl EventHandler for Log {
    fn handle_collision_event(&self, _: &RigidBodySet, _: &ColliderSet, e: CollisionEvent, _: Option<&ContactPair>) {
        if e.started() { self.started.fetch_add(1, Ordering::Relaxed); }
    }
    fn handle_contact_force_event(&self, _: f64, _: &RigidBodySet, _: &ColliderSet, _: &ContactPair, _: f64) {}
}
fn main() {
    let mut world = PhysicsWorld::new();
    world.gravity = Vector::new(0.0, -8.0, 0.0);
    world.integration_parameters.dt = 1.0 / 64.0;
    let ground = RigidBodyBuilder::fixed().build();
    let (_, _) = world.insert(ground, ColliderBuilder::cuboid(5.0, 0.5, 5.0).build());
    let body = RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 1.2, 0.0)).build();
    let (_, _) = world.insert(body, ColliderBuilder::cuboid(0.5, 0.5, 0.5).active_events(ActiveEvents::COLLISION_EVENTS).build());
    let log = Log { started: AtomicU32::new(0) };
    for _ in 0..64 { world.step_with_events(&(), &log); }
    println!("{}", log.started.load(Ordering::Relaxed));
}
```
Expected output: `1`

## Put the box and product laws behind a Law trait only when Rust code drives both; keep every export monomorphic
**Generic code over `L: Law` is monomorphized (static dispatch, no vtable, inlinable) but a `#[no_mangle]` export cannot be generic: rustc warns `no_mangle_generic_items` ('functions generic over types or consts must be mangled'); so each wasm export stays a concrete `extern "C"` shim, and a Law trait only pays off where Rust code runs both laws through one driver.**

*Check 1: #[no_mangle] on a generic extern fn triggers no_mangle_generic_items* · `compiles` · edition 2021 · host · lib · lints: no_mangle_generic_items · stderr has “functions generic over types or consts must be mangled” · **✔ oracle pass**
```rust
pub trait Law { fn step(&mut self, y: f64) -> f64; }
pub struct BoxLaw;
impl Law for BoxLaw { fn step(&mut self, y: f64) -> f64 { y - 0.125 } }
// A generic export: one symbol name cannot stand for every monomorphization.
#[no_mangle]
pub extern "C" fn run<L: Law + Default>(y: f64) -> f64 { L::default().step(y) }
```

*Check 2: wasm32: one generic driver, two monomorphic exports, no imports* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, box_run, product_run · imports nothing · node calls product_run(2.0, 4) · **✔ oracle pass**
```rust
// Two laws, one generic driver, two monomorphic exports: the trait lives
// inside the crate; the ABI stays plain extern "C" functions.
trait Law {
    const GRAVITY_SCALE: f64;
    fn step(&mut self, body: &mut [f64; 3]) -> bool;
}
struct BoxLaw;
struct ProductLaw { quanta: u32 }
impl Law for BoxLaw {
    const GRAVITY_SCALE: f64 = 1.0;
    fn step(&mut self, b: &mut [f64; 3]) -> bool { b[1] += -8.0 / 64.0 * Self::GRAVITY_SCALE; !b[1].is_nan() }
}
impl Law for ProductLaw {
    const GRAVITY_SCALE: f64 = 0.5;
    fn step(&mut self, b: &mut [f64; 3]) -> bool { self.quanta += 1; b[1] += -8.0 / 64.0 * Self::GRAVITY_SCALE; !b[1].is_nan() }
}
fn run<L: Law>(law: &mut L, y0: f64, n: u32) -> f64 {
    let mut body = [0.0, y0, 0.0];
    for _ in 0..n {
        if !law.step(&mut body) { return f64::NAN; }
    }
    body[1]
}
#[no_mangle]
pub extern "C" fn box_run(y0: f64, n: u32) -> f64 { run(&mut BoxLaw, y0, n) }
#[no_mangle]
pub extern "C" fn product_run(y0: f64, n: u32) -> f64 { run(&mut ProductLaw { quanta: 0 }, y0, n) }
```
Expected output: `1.75`

*Check 3: Host: run::<BoxLaw> and run::<ProductLaw>; the stateless law is zero bytes* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::mem::size_of;
trait Law {
    const GRAVITY_SCALE: f64;
    fn step(&mut self, body: &mut [f64; 3]) -> bool;
}
struct BoxLaw;
struct ProductLaw { quanta: u32 }
impl Law for BoxLaw {
    const GRAVITY_SCALE: f64 = 1.0;
    fn step(&mut self, b: &mut [f64; 3]) -> bool { b[1] += -8.0 / 64.0 * Self::GRAVITY_SCALE; !b[1].is_nan() }
}
impl Law for ProductLaw {
    const GRAVITY_SCALE: f64 = 0.5;
    fn step(&mut self, b: &mut [f64; 3]) -> bool { self.quanta += 1; b[1] += -8.0 / 64.0 * Self::GRAVITY_SCALE; !b[1].is_nan() }
}
fn run<L: Law>(law: &mut L, y0: f64, n: u32) -> f64 {
    let mut body = [0.0, y0, 0.0];
    for _ in 0..n {
        if !law.step(&mut body) { return f64::NAN; }
    }
    body[1]
}
fn main() {
    let mut p = ProductLaw { quanta: 0 };
    let a = run(&mut BoxLaw, 2.0, 4);
    let b = run(&mut p, 2.0, 4);
    println!("{a} {b} {} {}", p.quanta, size_of::<BoxLaw>());
}
```
Expected output: `1.5 1.75 4 0`

*Check 4: The associated const that suits static dispatch rules out dyn Law (E0038)* · `compile_fail` · edition 2021 · host · lib · errors: E0038 · **✔ oracle pass**
```rust
trait Law {
    const GRAVITY_SCALE: f64;
    fn step(&mut self, body: &mut [f64; 3]) -> bool;
}
// The associated const that suits static dispatch rules out a trait object.
fn pick(which: u32, a: &mut dyn Law, b: &mut dyn Law) -> bool {
    let mut body = [0.0; 3];
    if which == 0 { a.step(&mut body) } else { b.step(&mut body) }
}
```

## Upcast trait objects to a supertrait (1.86+) and downcast through dyn Any instead of an as_any method
**Since Rust 1.86 a pointer to `dyn Sub` coerces to a pointer to `dyn Super` for any supertrait, so with `trait Law: Any` a `&dyn Law` becomes `&dyn Any` and `downcast_ref::<ProductLaw>()` works with no `as_any` boilerplate; `Any` requires `'static`, and `Box<dyn Any>::downcast` recovers ownership.**

*Check 1: &dyn Law upcasts to &dyn Any; downcast_ref finds the product law* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::any::Any;
trait Law: Any {
    fn name(&self) -> &'static str;
}
struct BoxLaw;
struct ProductLaw { quanta: u32 }
impl Law for BoxLaw { fn name(&self) -> &'static str { "box" } }
impl Law for ProductLaw { fn name(&self) -> &'static str { "product" } }
fn main() {
    let laws: Vec<Box<dyn Law>> = vec![Box::new(BoxLaw), Box::new(ProductLaw { quanta: 64 })];
    for law in &laws {
        let any: &dyn Any = &**law;          // trait-object upcasting coercion (1.86+)
        match any.downcast_ref::<ProductLaw>() {
            Some(p) => println!("{} {}", law.name(), p.quanta),
            None => println!("{} -", law.name()),
        }
    }
}
```
Expected output: `box - product 64`

*Check 2: Box<dyn Law> upcasts to Box<dyn Any>; downcast returns Box<ProductLaw>* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::any::Any;
trait Law: Any { fn name(&self) -> &'static str; }
struct ProductLaw { quanta: u32 }
impl Law for ProductLaw { fn name(&self) -> &'static str { "product" } }
fn main() {
    let law: Box<dyn Law> = Box::new(ProductLaw { quanta: 64 });
    let any: Box<dyn Any> = law;                  // Box<dyn Law> -> Box<dyn Any>
    let p: Box<ProductLaw> = any.downcast::<ProductLaw>().ok().unwrap();
    println!("{} {}", p.name(), p.quanta);
}
```
Expected output: `product 64`

*Check 3: Box<dyn Any>.type_id() is the box's TypeId; (&*boxed).type_id() is the value's* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::any::{Any, TypeId};
fn main() {
    let boxed: Box<dyn Any> = Box::new(3_i32);
    let wrong = boxed.type_id() == TypeId::of::<i32>();     // TypeId of the Box itself
    let right = (&*boxed).type_id() == TypeId::of::<i32>(); // TypeId of the value
    println!("{wrong} {right} {}", boxed.is::<i32>());
}
```
Expected output: `false true true`

*Check 4: Any needs 'static: a borrowed &str cannot become &dyn Any (E0597)* · `compile_fail` · edition 2024 · host · bin · errors: E0597 · stderr has “borrowed for `'static`” · **✔ oracle pass**
```rust
use std::any::Any;
fn store(_: &dyn Any) {}
fn main() {
    let name = String::from("slab");
    let r: &str = &name;     // a borrowed, non-'static value
    store(&r);               // Any requires 'static
}
```

*Check 5: A supertrait default method uses Display; &dyn Law upcasts to &dyn Report* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::fmt;
trait Report: fmt::Display {
    fn banner(&self) -> String { format!("[{}]", self.to_string()) }
}
trait Law: Report {}
struct BoxLaw;
impl fmt::Display for BoxLaw { fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result { write!(f, "box") } }
impl Report for BoxLaw {}
impl Law for BoxLaw {}
fn show(l: &dyn Law) -> String { let r: &dyn Report = l; r.banner() }
fn main() { println!("{}", show(&BoxLaw)); }
```
Expected output: `[box]`

*Check 6: Implementing the subtrait without the supertrait is E0277* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · **✔ oracle pass**
```rust
trait Report { fn banner(&self) -> String; }
trait Law: Report {}
struct BoxLaw;
impl Law for BoxLaw {}
fn main() {}
```

## Write for<'a> bounds when a generic must accept a borrow that the function creates itself
**A lifetime parameter on a function is chosen by the caller and outlives the call, so it cannot name a borrow of a local; a higher-ranked bound (`F: for<'a> Fn(&'a f64) -> f64`, or the elided `Fn(&f64) -> f64`, or `where for<'a> &'a C: IntoIterator<Item = &'a f64>`) must hold for every lifetime, including that local one.**

*Check 1: A caller-chosen 'a cannot name a local borrow: E0597* · `compile_fail` · edition 2024 · host · bin · errors: E0597 · **✔ oracle pass**
```rust
// A lifetime chosen by the caller cannot name a borrow of a local.
fn call_on_local<'a, F: Fn(&'a f64) -> f64>(f: F) -> f64 {
    let x = 1.5;
    f(&x)
}
fn main() { println!("{}", call_on_local(|v| *v * 2.0)); }
```

*Check 2: for<'a> Fn(&'a f64) and the elided Fn(&f64) both accept the local borrow* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
// for<'a>: the bound holds for every lifetime, including the local borrow.
fn call_on_local<F>(f: F) -> f64 where F: for<'a> Fn(&'a f64) -> f64 {
    let x = 1.5;
    f(&x)
}
// Elided form: Fn(&f64) -> f64 in a bound is the same higher-ranked bound.
fn call_on_local_elided<F: Fn(&f64) -> f64>(f: F) -> f64 {
    let x = 2.5;
    f(&x)
}
fn main() { println!("{} {}", call_on_local(|v| *v * 2.0), call_on_local_elided(|v| *v * 2.0)); }
```
Expected output: `3 5`

*Check 3: for<'a> &'a C: IntoIterator sums Vec, array and VecDeque by reference* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::collections::VecDeque;
// Iterate any collection by shared reference, whatever its concrete type.
fn sum_all<C>(c: C) -> f64 where for<'a> &'a C: IntoIterator<Item = &'a f64> {
    let mut s = 0.0;
    for x in &c { s += *x; }
    s
}
fn main() {
    let v = vec![1.0, 2.0];
    let a = [0.5; 4];
    let d: VecDeque<f64> = VecDeque::from(vec![0.25, 0.25]);
    println!("{} {} {}", sum_all(v), sum_all(a), sum_all(d));
}
```
Expected output: `3 2 0.5`

*Check 4: The same bound with a function-level 'a is E0597* · `compile_fail` · edition 2024 · host · bin · errors: E0597 · **✔ oracle pass**
```rust
fn sum_all<'a, C: 'a>(c: C) -> f64 where &'a C: IntoIterator<Item = &'a f64> {
    let mut s = 0.0;
    for x in &c { s += *x; }
    s
}
fn main() { println!("{}", sum_all(vec![1.0, 2.0])); }
```

