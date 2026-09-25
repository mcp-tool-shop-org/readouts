# Memory, smart pointers & layout — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](memory-layout.md) · [catalog index](README.md)

## Budget pointer widths: Box<T> is one word, Box<[T]> and &dyn Trait carry metadata, ZSTs take no space
**Box<T> for sized T is guaranteed to be one pointer, ABI-compatible with C's T*; pointers to dynamically sized types ([T], str, dyn Trait) also carry a length or a vtable pointer and are two words today; zero-sized types occupy no memory, and a Vec of a ZST never allocates and reports capacity usize::MAX.**

*Check 1: Box<T> 1 word; Box<[T]>, &[T], &str, &dyn 2; Vec 3; ZSTs 0; Vec<ZST> capacity usize::MAX* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::fmt::Debug;
use std::marker::PhantomData;
use std::mem::size_of;

struct Marker; // a zero-sized type

fn main() {
    let w = size_of::<usize>();
    // thin: one word
    println!("Box<f64> {} Box<[f64; 4]> {} &f64 {}", size_of::<Box<f64>>() / w, size_of::<Box<[f64; 4]>>() / w, size_of::<&f64>() / w);
    // wide: pointer + metadata (length or vtable)
    println!("Box<[f64]> {} &[f64] {} &str {} &dyn Debug {}", size_of::<Box<[f64]>>() / w, size_of::<&[f64]>() / w, size_of::<&str>() / w, size_of::<&dyn Debug>() / w);
    // Vec is (pointer, capacity, length)
    println!("Vec<f64> {}", size_of::<Vec<f64>>() / w);
    // zero-sized types
    println!("() {} Marker {} PhantomData<f64> {} [f64; 0] {}", size_of::<()>(), size_of::<Marker>(), size_of::<PhantomData<f64>>(), size_of::<[f64; 0]>());
    let units: Vec<Marker> = Vec::with_capacity(10);
    println!("Vec<Marker> capacity is usize::MAX: {}", units.capacity() == usize::MAX);
    // into_boxed_slice drops the excess capacity: a fixed-length heap buffer
    let mut v: Vec<f64> = Vec::with_capacity(10);
    v.extend([1.0, 2.0, 3.0]);
    let fixed: Box<[f64]> = v.into_boxed_slice();
    println!("boxed len {} back to vec capacity {}", fixed.len(), fixed.into_vec().capacity());
}
```
Expected output: `Box<f64> 1 Box<[f64; 4]> 1 &f64 1 Box<[f64]> 2 &[f64] 2 &str 2 &dyn Debug 2 Vec<f64> 3 () 0 Marker 0 PhantomData<f64> 0 [f64; 0] 0 Vec<Marker> capacity is usize::MAX: true boxed len 3 back to vec capa`

## Count on Option's niche only for std-listed types; give boundary enums #[repr(u8)] and explicit values
**Option<T> has exactly the size, alignment and call ABI of T when T is &U, &mut U, Box<U>, a fn pointer, a NonZero integer, NonNull<U>, or a #[repr(transparent)] wrapper of one of these; types in which every bit pattern is valid (u32, f64) have no niche, so Option<u32> is 8 bytes and Option<f64> is 16.**

*Check 1: Guaranteed niches keep Option the size of T; u32 and f64 have none; repr(u8) blocks the niche* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::mem::size_of;
use std::num::NonZeroU32;
use std::ptr::NonNull;

#[allow(dead_code)]
#[repr(u8)]
#[derive(Clone, Copy)]
enum Mode { Free = 0, Driven = 1, Lifted = 2, Carried = 3 }

#[allow(dead_code)]
enum Plain<'a> { Nothing, Some(&'a u16) }

#[allow(dead_code)]
#[repr(u8)]
enum Tagged<'a> { Nothing, Some(&'a u16) }

fn main() {
    // guaranteed by std::option "Representation"
    println!("&f64 {} Option<&f64> {}", size_of::<&f64>(), size_of::<Option<&f64>>());
    println!("Box<f64> {} Option<Box<f64>> {}", size_of::<Box<f64>>(), size_of::<Option<Box<f64>>>());
    println!("NonZeroU32 {} Option<NonZeroU32> {}", size_of::<NonZeroU32>(), size_of::<Option<NonZeroU32>>());
    println!("NonNull<f64> {} Option<NonNull<f64>> {}", size_of::<NonNull<f64>>(), size_of::<Option<NonNull<f64>>>());
    // no niche: every bit pattern of u32 and f64 is valid
    println!("u32 {} Option<u32> {}", size_of::<u32>(), size_of::<Option<u32>>());
    println!("f64 {} Option<f64> {}", size_of::<f64>(), size_of::<Option<f64>>());
    // repr(u8) fieldless enum: exactly one byte, discriminants fixed
    println!("Mode {} as u8 {}", size_of::<Mode>(), Mode::Carried as u8);
    // explicit repr on an enum with fields turns niche filling off
    println!("Plain {} Tagged {}", size_of::<Plain>(), size_of::<Tagged>());
}
```
Expected output: `&f64 8 Option<&f64> 8 Box<f64> 8 Option<Box<f64>> 8 NonZeroU32 4 Option<NonZeroU32> 4 NonNull<f64> 8 Option<NonNull<f64>> 8 u32 4 Option<u32> 8 f64 8 Option<f64> 16 Mode 1 as u8 3 Plain 8 Tagged 16`

*Check 2: Option<RigidBodyHandle> is 12 bytes (no niche); Option<slotmap DefaultKey> is 8 on 1.98.1* · `runs` · edition 2024 · host · bin · deps: rapier3d_f64, slotmap · **✔ oracle pass**
```rust
use std::mem::size_of;
use rapier3d_f64::prelude::RigidBodyHandle;
use slotmap::DefaultKey;

fn main() {
    println!("RigidBodyHandle {} Option<RigidBodyHandle> {}", size_of::<RigidBodyHandle>(), size_of::<Option<RigidBodyHandle>>());
    println!("DefaultKey {} Option<DefaultKey> {}", size_of::<DefaultKey>(), size_of::<Option<DefaultKey>>());
}
```
Expected output: `RigidBodyHandle 8 Option<RigidBodyHandle> 12 DefaultKey 8 Option<DefaultKey> 8`

*Check 3: A #[repr(u8)] discriminant of 300 is rejected by the overflowing_literals lint* · `compile_fail` · edition 2024 · host · lib · lints: overflowing_literals · stderr has “literal out of range for `u8`” · **✔ oracle pass**
```rust
#[repr(u8)]
pub enum Mode { Free = 0, Driven = 1, Wide = 300 }
```

*Check 4: A TryFrom<f64> decoder maps 3.0 to a variant and rejects 7.0* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
#[derive(Debug, Clone, Copy, PartialEq)]
#[repr(u8)]
enum Mode { Free = 0, Driven = 1, Lifted = 2, Carried = 3 }

impl TryFrom<f64> for Mode {
    type Error = f64;
    fn try_from(x: f64) -> Result<Self, f64> {
        match x {
            0.0 => Ok(Mode::Free),
            1.0 => Ok(Mode::Driven),
            2.0 => Ok(Mode::Lifted),
            3.0 => Ok(Mode::Carried),
            other => Err(other),
        }
    }
}

fn main() {
    println!("{:?} {:?} {}", Mode::try_from(3.0), Mode::try_from(7.0), Mode::Lifted as u8);
}
```
Expected output: `Ok(Carried) Err(7.0) 2`

## Keep entities in a generational arena keyed by (index, generation); insertion order hands out the ids
**A generational arena (slotmap, Rapier's RigidBodySet and ColliderSet) stores values in a Vec and returns a Copy key of slot index plus version, so a removed key stays invalid even after its slot is reused; which index a value gets is decided by insertion order and the free list, and in Rapier the generation is one counter for the whole arena.**

*Check 1: slotmap: a removed key stays invalid after its slot is reused* · `runs` · edition 2024 · host · bin · deps: slotmap · **✔ oracle pass**
```rust
use slotmap::{new_key_type, SlotMap};

new_key_type! { struct BodyKey; }

fn main() {
    let mut bodies: SlotMap<BodyKey, &str> = SlotMap::with_key();
    let crate_a = bodies.insert("crate a");
    let crate_b = bodies.insert("crate b");
    bodies.remove(crate_b);
    let barrel = bodies.insert("barrel"); // may reuse crate_b's slot
    println!("stale key get: {:?}", bodies.get(crate_b));
    println!("stale key contains: {}", bodies.contains_key(crate_b));
    println!("stale == new: {}", crate_b == barrel);
    println!("live: {} {} len {}", bodies[crate_a], bodies[barrel], bodies.len());
}
```
Expected output: `stale key get: None stale key contains: false stale == new: false live: crate a barrel len 2`

*Check 2: Rapier handles follow insertion order; a removal reuses the index under an arena-wide generation* · `runs` · edition 2024 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

fn fixed_box(x: f64) -> (RigidBody, Collider) {
    (RigidBodyBuilder::fixed().translation(Vector::new(x, 0.0, 0.0)).build(),
     ColliderBuilder::cuboid(1.0, 0.1, 1.0).build())
}
fn dynamic_box() -> (RigidBody, Collider) {
    (RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 2.0, 0.0)).build(),
     ColliderBuilder::cuboid(0.5, 0.5, 0.5).build())
}

fn main() {
    // The engine's order: static geometry first, then the moving bodies.
    let mut w1 = PhysicsWorld::new();
    for x in [0.0, 5.0] {
        let (b, c) = fixed_box(x);
        w1.insert(b, c);
    }
    let (b, c) = dynamic_box();
    let (h1, c1) = w1.insert(b, c);
    println!("statics first: body {:?} collider {:?}", h1.into_raw_parts(), c1.into_raw_parts());

    // Same content, other order: the moving body gets index 0.
    let mut w2 = PhysicsWorld::new();
    let (b, c) = dynamic_box();
    let (h2, c2) = w2.insert(b, c);
    for x in [0.0, 5.0] {
        let (b, c) = fixed_box(x);
        w2.insert(b, c);
    }
    println!("body first: body {:?} collider {:?}", h2.into_raw_parts(), c2.into_raw_parts());

    // Removal frees the index; the next insertion reuses it under a new generation.
    w1.remove_body(h1);
    let (b, c) = dynamic_box();
    let (h3, _) = w1.insert(b, c);
    println!("reinserted: body {:?}", h3.into_raw_parts());
    println!("stale handle resolves: {}", w1.bodies.get(h1).is_some());
    // The generation counter is arena-wide: a never-used index now starts at 1.
    let (b, c) = dynamic_box();
    let (h4, _) = w1.insert(b, c);
    println!("fresh index after a removal: body {:?}", h4.into_raw_parts());
}
```
Expected output: `statics first: body (2, 0) collider (2, 0) body first: body (0, 0) collider (0, 0) reinserted: body (2, 1) stale handle resolves: false fresh index after a removal: body (3, 1)`

## Mutate through & only via UnsafeCell-based types; a &T-to-&mut T cast is UB even where the lint is silent
**UnsafeCell<T> is the only allowed way to mutate data behind a shared reference, and Cell, RefCell, OnceCell, LazyCell and the thread-safe cells and atomics are built on it; mutating through a &T any other way, including a &T -> *mut T -> &mut T cast, is undefined behaviour.**

*Check 1: The engine's &ContactPair-to-&mut cast, written inline, is denied by invalid_reference_casting* · `compile_fail` · edition 2024 · host · lib · lints: invalid_reference_casting · stderr has “casting `&T` to `&mut T` is undefined behavior, even if the reference is unused” · **✔ oracle pass**
```rust
pub struct Pair {
    pub manifolds: Vec<f64>,
}

/// The engine's cast written in one expression: &Pair -> *mut Pair -> &mut Pair.
pub fn clear(pairs: &[Pair]) {
    for pair in pairs {
        let p = unsafe { &mut *(core::ptr::from_ref(pair) as *mut Pair) };
        for m in p.manifolds.iter_mut() {
            *m = 0.0;
        }
    }
}
```

*Check 2: The same cast with the pointers parked in a Vec compiles with no diagnostic at all* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub struct Pair {
    pub manifolds: Vec<f64>,
}

/// The same cast, shaped like solver_clear_warmstart: pointers parked in a Vec first.
pub fn clear(pairs: &[Pair]) -> u32 {
    let mut ptrs: Vec<*mut Pair> = Vec::new();
    for pair in pairs {
        ptrs.push(core::ptr::from_ref(pair) as *mut Pair);
    }
    let mut n = 0;
    for ptr in ptrs {
        let p = unsafe { &mut *ptr };
        for m in p.manifolds.iter_mut() {
            *m = 0.0;
            n += 1;
        }
    }
    n
}
```

*Check 3: Cell mutates through &; RefCell's try_borrow_mut errs and a second borrow_mut panics (exit 101)* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
use std::cell::{Cell, RefCell};

fn main() {
    let steps = Cell::new(0u32);
    let shared = &steps;
    shared.set(shared.get() + 1); // mutation through a shared reference, no borrow to track
    println!("cell {}", steps.get());

    let cache = RefCell::new(vec![1.0f64, 2.0]);
    let first = cache.borrow_mut();
    println!("try_borrow_mut while borrowed is_err: {}", cache.try_borrow_mut().is_err());
    let second = cache.borrow_mut(); // a second exclusive borrow: panics at run time
    println!("not reached {} {}", first.len(), second.len());
}
```
Expected output: `cell 1 try_borrow_mut while borrowed is_err: true`

*Check 4: LazyLock and OnceLock work as statics; LazyCell and OnceCell initialise once in a local* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::cell::{LazyCell, OnceCell};
use std::sync::{LazyLock, OnceLock};

// Thread-safe: allowed in a static. The closure runs once, on first access.
static SLOPE_TABLE: LazyLock<Vec<f64>> = LazyLock::new(|| {
    println!("building table");
    (0..=4).map(|d| d as f64 * 22.5).collect()
});

// OnceLock: set once from a value computed elsewhere.
static SEED: OnceLock<u64> = OnceLock::new();

fn main() {
    println!("before first access");
    println!("table[2] = {}", SLOPE_TABLE[2]);
    println!("table len = {}", SLOPE_TABLE.len()); // no second "building table"

    println!("first set ok: {}", SEED.set(42).is_ok());
    println!("second set ok: {}", SEED.set(7).is_ok());
    println!("seed = {}", SEED.get().unwrap());

    // Single-threaded twins: no Sync, so not for statics, fine for locals.
    let lazy = LazyCell::new(|| {
        println!("computing local");
        2.0f64.sqrt()
    });
    let once: OnceCell<&str> = OnceCell::new();
    println!("local ready");
    println!("{:.3} {:.3}", *lazy, *lazy);
    println!("{}", once.get_or_init(|| "init once"));
    println!("{}", once.get_or_init(|| "ignored"));
}
```
Expected output: `before first access building table table[2] = 45 table len = 5 first set ok: true second set ok: false seed = 42 local ready computing local 1.414 1.414 init once init once`

*Check 5: RefCell, LazyCell and UnsafeCell statics are refused as not Sync (E0277)* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “`RefCell<u32>` cannot be shared between threads safely” · stderr has “`UnsafeCell<cell::lazy::State<f64” · stderr has “`UnsafeCell<u32>` cannot be shared between threads safely” · **✔ oracle pass**
```rust
use std::cell::{LazyCell, RefCell, UnsafeCell};

pub static COUNTER: RefCell<u32> = RefCell::new(0);
pub static TABLE: LazyCell<f64> = LazyCell::new(|| 2.0f64.sqrt());
pub static RAW: UnsafeCell<u32> = UnsafeCell::new(0);
```

## Point Rc/Arc edges one way (strong down, Weak back) or a strong cycle leaks and its destructors never run
**Rc and Arc drop their value when the last strong handle goes, so a cycle of strong handles never reaches zero: no destructor runs and nothing warns, because leaks are memory-safe in Rust. Weak (Rc::downgrade / Arc::downgrade) does not own, and upgrade() returns None once the value is gone.**

*Check 1: A strong Rc cycle outlives its handles; a Weak back-edge lets the parent drop* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Node {
    name: &'static str,
    next: RefCell<Option<Rc<Node>>>,   // strong edge
    parent: RefCell<Weak<Node>>,       // weak back-edge
}
impl Drop for Node {
    fn drop(&mut self) {
        println!("drop {}", self.name);
    }
}
fn node(name: &'static str) -> Rc<Node> {
    Rc::new(Node { name, next: RefCell::new(None), parent: RefCell::new(Weak::new()) })
}

fn main() {
    // A cycle of strong edges: a -> b -> a.
    let a = node("cycle a");
    let b = node("cycle b");
    *a.next.borrow_mut() = Some(Rc::clone(&b));
    *b.next.borrow_mut() = Some(Rc::clone(&a));
    let probe = Rc::downgrade(&a);
    drop(a);
    drop(b);
    println!("after dropping the cycle: strong {} alive {}", probe.strong_count(), probe.upgrade().is_some());

    // A tree: parent owns child strongly, child points back weakly.
    let parent = node("tree parent");
    let child = node("tree child");
    *parent.next.borrow_mut() = Some(Rc::clone(&child));
    *child.parent.borrow_mut() = Rc::downgrade(&parent);
    println!("child sees parent: {}", child.parent.borrow().upgrade().is_some());
    drop(parent);
    println!("child sees parent after drop: {}", child.parent.borrow().upgrade().is_some());
}
```
Expected output: `after dropping the cycle: strong 1 alive true child sees parent: true drop tree parent child sees parent after drop: false drop tree child`

*Check 2: Moving an Rc into thread::spawn is refused: Rc is not Send (E0277)* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “cannot be sent between threads safely” · **✔ oracle pass**
```rust
use std::rc::Rc;
use std::thread;

pub fn share() {
    let state = Rc::new(vec![0.0f64; 4]);
    let handle = thread::spawn(move || state.len());
    handle.join().unwrap();
}
```

*Check 3: parry SharedShape: clone bumps the Arc count, rebuilding allocates anew; it is two words wide* · `runs` · edition 2024 · host · bin · deps: parry3d_f64 · **✔ oracle pass**
```rust
use parry3d_f64::shape::SharedShape;
use std::sync::Arc;

fn main() {
    let a = SharedShape::cuboid(0.5, 1.0, 0.5);
    let b = a.clone(); // bumps the count; the shape data is shared
    println!("strong count after clone: {}", Arc::strong_count(&a.0));
    println!("clone shares the allocation: {}", Arc::ptr_eq(&a.0, &b.0));
    let c = SharedShape::cuboid(0.5, 1.0, 0.5); // same numbers, a new heap allocation
    println!("rebuilt shape shares it: {}", Arc::ptr_eq(&a.0, &c.0));
    println!("SharedShape width in words: {}", std::mem::size_of::<SharedShape>() / std::mem::size_of::<usize>());
}
```
Expected output: `strong count after clone: 2 clone shares the allocation: true rebuilt shape shares it: false SharedShape width in words: 2`

## Predict destructors: fields drop in declaration order, locals in reverse, statics and forgotten values never
**A struct's fields drop in declaration order and a scope's locals in reverse order of declaration; an assignment drops the old value before the new one moves in; statics are never dropped; mem::forget and ManuallyDrop skip a destructor safely, because Rust does not promise that destructors run; memory that is not yet initialised must be held as MaybeUninit<T>.**

*Check 1: Assignment drops the old value; fields in order; locals reversed; static/forget/ManuallyDrop never* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
#![allow(dead_code, unused_assignments)]
use std::mem::{self, ManuallyDrop};

struct Loud(&'static str);
impl Drop for Loud {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

struct World {
    first: Loud,
    second: Loud,
}

static FOREVER: Loud = Loud("static");

fn main() {
    let _a = Loud("local a");
    let _b = Loud("local b");
    let _w = World { first: Loud("field first"), second: Loud("field second") };
    mem::forget(Loud("forgotten"));
    let _m = ManuallyDrop::new(Loud("manual"));
    let mut slot = Loud("old value");
    slot = Loud("new value"); // assignment drops the old value first
    println!("static at {}", FOREVER.0);
    println!("end of main");
    let _ = &slot;
}
```
Expected output: `drop old value static at static end of main drop new value drop field first drop field second drop local b drop local a`

*Check 2: assume_init on an uninitialised bool compiles, flagged only by the invalid_value warning* · `compiles` · edition 2024 · host · lib · lints: invalid_value · stderr has “does not permit being left uninitialized” · **✔ oracle pass**
```rust
use std::mem::MaybeUninit;

pub fn make_flag() -> bool {
    unsafe { MaybeUninit::uninit().assume_init() }
}
```

*Check 3: The MaybeUninit array idiom: write each slot once, then transmute to [T; N]* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::mem::{self, MaybeUninit};

fn main() {
    // An array of MaybeUninit needs no initialisation; each slot is written exactly once.
    let mut slots: [MaybeUninit<f64>; 4] = [const { MaybeUninit::uninit() }; 4];
    for (i, slot) in slots.iter_mut().enumerate() {
        slot.write(i as f64 * 0.5);
    }
    // Every element is initialised: reinterpret as the initialised array.
    let values: [f64; 4] = unsafe { mem::transmute::<[MaybeUninit<f64>; 4], [f64; 4]>(slots) };
    println!("{:?}", values);
    println!("{} {}", mem::size_of::<MaybeUninit<f64>>(), mem::size_of::<Option<MaybeUninit<bool>>>());
}
```
Expected output: `[0.0, 0.5, 1.0, 1.5] 8 2`

## Put ABI buffers in flat arrays or #[repr(C)]: default repr(Rust) promises no field order or size
**Rust fixes the layout of arrays (element n at byte n*size_of::<T>()), of #[repr(C)] types (declaration order, C padding) and of #[repr(transparent)] types (the layout and ABI of their one non-zero-sized field); the default representation promises only aligned, non-overlapping fields, and its order and size may differ between compilations.**

*Check 1: Arrays and repr(C) have fixed offsets; the repr(Rust) size is whatever 1.98.1 chose* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
#![allow(dead_code)]
use std::mem::{align_of, offset_of, size_of};

#[repr(C)]
struct CRec { a: u8, b: u32, c: u16 }

struct RustRec { a: u8, b: u32, c: u16 } // default repr(Rust)

#[repr(transparent)]
struct Meters(f64);

const MAX_BODIES: usize = 64;
const BODY_STRIDE: usize = 17;
// Compile-time layout pins: a wrong number is a build error, not a runtime surprise.
const _: () = assert!(size_of::<[f64; MAX_BODIES * BODY_STRIDE]>() == MAX_BODIES * BODY_STRIDE * 8);
const _: () = assert!(offset_of!(CRec, b) == 4);

fn main() {
    println!("repr(C) size {} align {}", size_of::<CRec>(), align_of::<CRec>());
    println!("repr(C) offsets a={} b={} c={}", offset_of!(CRec, a), offset_of!(CRec, b), offset_of!(CRec, c));
    println!("repr(Rust) size {} (unspecified)", size_of::<RustRec>());
    println!("transparent size {} align {}", size_of::<Meters>(), align_of::<Meters>());
    let arr = [0.0f64; MAX_BODIES * BODY_STRIDE];
    let base = arr.as_ptr() as usize;
    let at = &arr[2 * BODY_STRIDE + 13] as *const f64 as usize; // body 2, slot 13
    println!("element offset {}", at - base);
    println!("array size {} align {}", size_of::<[f64; MAX_BODIES * BODY_STRIDE]>(), align_of::<[f64; MAX_BODIES * BODY_STRIDE]>());
}
```
Expected output: `repr(C) size 12 align 4 repr(C) offsets a=0 b=4 c=8 repr(Rust) size 8 (unspecified) transparent size 8 align 8 element offset 376 array size 8704 align 8`

*Check 2: A reference to a #[repr(packed)] field is refused with E0793* · `compile_fail` · edition 2024 · host · lib · errors: E0793 · stderr has “reference to field of packed struct is unaligned” · stderr has “creating a misaligned reference is undefined behavior” · **✔ oracle pass**
```rust
#[repr(C, packed)]
pub struct Wire { tag: u8, value: f64 }

pub fn value_ref(w: &Wire) -> &f64 {
    &w.value
}
```

*Check 3: Copying a packed field, or &raw const plus read_unaligned, compiles and reads it* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
#[repr(C, packed)]
pub struct Wire { tag: u8, value: f64 }

fn main() {
    let w = Wire { tag: 1, value: 2.5 };
    let copy = w.value;                     // a copy, not a reference
    let raw = &raw const w.value;           // a raw pointer, then an unaligned read
    let read = unsafe { raw.read_unaligned() };
    println!("{} {} {} {}", std::mem::size_of::<Wire>(), { w.tag }, copy, read);
}
```
Expected output: `9 1 2.5 2.5`

*Check 4: On wasm32-unknown-unknown f64 is 8-aligned and a static [f64; N] starts 8-aligned* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · exports memory, bodies_ptr, layout_probe · node calls layout_probe() · **✔ oracle pass**
```rust
const MAX_BODIES: usize = 64;
const BODY_STRIDE: usize = 17;
static mut BODIES: [f64; MAX_BODIES * BODY_STRIDE] = [0.0; MAX_BODIES * BODY_STRIDE];

#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    (&raw mut BODIES).cast::<f64>()
}

/// 100 * align_of::<f64>() + (address of BODIES mod 8): 800 means 8-byte aligned f64 and an aligned buffer.
#[unsafe(no_mangle)]
pub extern "C" fn layout_probe() -> u32 {
    let addr = bodies_ptr() as usize;
    (100 * core::mem::align_of::<f64>() + addr % 8) as u32
}
```
Expected output: `800`

## Re-read a Vec's pointer after any call that can grow it: growth reallocates and kills raw pointers into it
**A Vec (re)allocates when a push finds len == capacity, and after a successful realloc any access through the old pointer is undefined behaviour even if the block stayed in place; within capacity push never reallocates, clear() keeps the buffer, and Vec::new() allocates nothing until the first push.**

*Check 1: Counting allocator: none for Vec::new or within capacity; growth calls it and moves the buffer* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering::Relaxed};

/// Counts every allocator call. `realloc` does what GlobalAlloc's provided default
/// does (allocate a new block, copy, free the old one), so a grown buffer always moves.
struct Counting;
static CALLS: AtomicUsize = AtomicUsize::new(0);

unsafe impl GlobalAlloc for Counting {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        CALLS.fetch_add(1, Relaxed);
        unsafe { System.alloc(layout) }
    }
    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        CALLS.fetch_add(1, Relaxed);
        unsafe { System.dealloc(ptr, layout) }
    }
    unsafe fn realloc(&self, ptr: *mut u8, layout: Layout, new_size: usize) -> *mut u8 {
        CALLS.fetch_add(1, Relaxed);
        let new_layout = unsafe { Layout::from_size_align_unchecked(new_size, layout.align()) };
        let new_ptr = unsafe { System.alloc(new_layout) };
        if !new_ptr.is_null() {
            unsafe {
                std::ptr::copy_nonoverlapping(ptr, new_ptr, layout.size().min(new_size));
                System.dealloc(ptr, layout);
            }
        }
        new_ptr
    }
}

#[global_allocator]
static GLOBAL: Counting = Counting;

fn calls() -> usize {
    CALLS.load(Relaxed)
}

fn main() {
    let c0 = calls();
    let mut snapshot: Vec<u8> = Vec::new();
    let c1 = calls();

    snapshot.push(0);
    let p0 = snapshot.as_ptr();
    let c2 = calls();
    while snapshot.len() < snapshot.capacity() {
        snapshot.push(1);
    }
    let c3 = calls();
    let p1 = snapshot.as_ptr();

    snapshot.push(2); // len == capacity: this push must (re)allocate
    let c4 = calls();
    let p2 = snapshot.as_ptr();

    let (len, cap) = (snapshot.len(), snapshot.capacity());
    snapshot.clear(); // len 0, same buffer
    while snapshot.len() < len {
        snapshot.push(3);
    }
    let c5 = calls();
    let p3 = snapshot.as_ptr();

    println!("Vec::new called the allocator: {}", c1 != c0);
    println!("push within capacity called the allocator: {}", c3 != c2);
    println!("pointer stable within capacity: {}", p0 == p1);
    println!("push at capacity called the allocator: {}", c4 != c3);
    println!("growth moved the buffer: {}", p2 != p1);
    println!("clear + refill called the allocator: {}", c5 != c4);
    println!("clear kept the buffer: {}", p3 == p2 && snapshot.capacity() == cap);
}
```
Expected output: `Vec::new called the allocator: false push within capacity called the allocator: false pointer stable within capacity: true push at capacity called the allocator: true growth moved the buffer: true cle`

*Check 2: Holding &v[0] across v.push is refused by the borrow checker (E0502)* · `compile_fail` · edition 2024 · host · lib · errors: E0502 · **✔ oracle pass**
```rust
pub fn first_after_growth(snapshot: &mut Vec<u8>) -> u8 {
    let first = &snapshot[0];
    snapshot.push(9); // may reallocate: the borrow checker refuses while `first` lives
    *first
}
```

*Check 3: The same pattern through v.as_ptr() compiles silently: the raw pointer is on you* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub fn first_after_growth(snapshot: &mut Vec<u8>) -> *const u8 {
    let first = snapshot.as_ptr();
    snapshot.push(9); // may reallocate: nothing stops the raw pointer from dangling
    first
}
```

## Return Cow when a function usually passes its input through and only sometimes rewrites it
**Cow (clone-on-write) holds either borrowed data or its owned form; to_mut() clones only on the first write, so the common no-change path allocates nothing, which is the pattern std itself uses in String::from_utf8_lossy.**

*Check 1: A signed-zero canonicaliser borrows clean input and clones only dirty input; from_utf8_lossy too* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::borrow::Cow;

/// +0.0 for both signed zeros. Borrows when nothing needs changing.
fn canon_zeros(xs: &[f64]) -> Cow<'_, [f64]> {
    let mut out = Cow::Borrowed(xs);
    for i in 0..xs.len() {
        if xs[i] == 0.0 && xs[i].is_sign_negative() {
            out.to_mut()[i] = 0.0; // first write clones the whole slice, later writes reuse it
        }
    }
    out
}

fn kind<T: ?Sized + ToOwned>(c: &Cow<'_, T>) -> &'static str {
    match c {
        Cow::Borrowed(_) => "borrowed",
        Cow::Owned(_) => "owned",
    }
}

fn main() {
    let clean = [1.0, 0.0, 2.5];
    let dirty = [1.0, -0.0, -0.0];
    let a = canon_zeros(&clean);
    let b = canon_zeros(&dirty);
    println!("{} {:?}", kind(&a), a);
    println!("{} {:?}", kind(&b), b);
    println!("{}", b.iter().all(|x| !x.is_sign_negative()));
    // std returns Cow too: lossy UTF-8 only allocates when it must replace bytes.
    println!("{} {}", kind(&String::from_utf8_lossy(b"quantum")), kind(&String::from_utf8_lossy(b"q\xFFm")));
}
```
Expected output: `borrowed [1.0, 0.0, 2.5] owned [1.0, 0.0, 0.0] true borrowed owned`

## Store indices or offsets instead of self-references; use Pin only where an API such as Future::poll needs it
**A struct cannot safely hold a reference into its own fields, because moving it would leave the pointer at the old address, and the borrow checker refuses to build one (E0505, E0515). Pin guarantees that a !Unpin value stays at one address until it is dropped; most types are Unpin, and for them Pin adds nothing.**

*Check 1: A struct holding a reference into its own Vec cannot be built (E0505, E0515)* · `compile_fail` · edition 2024 · host · lib · errors: E0505, E0515 · **✔ oracle pass**
```rust
pub struct Track<'a> {
    samples: Vec<f64>,
    last: &'a f64, // meant to point into `samples`
}

pub fn build<'a>() -> Track<'a> {
    let samples = vec![1.0, 2.0, 3.0];
    let last = &samples[2];
    Track { samples, last }
}
```

*Check 2: Pin::new refuses a !Unpin (PhantomPinned) value with E0277* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “`PhantomPinned` cannot be unpinned” · stderr has “consider using the `pin!` macro” · **✔ oracle pass**
```rust
use std::marker::PhantomPinned;
use std::pin::Pin;

pub struct AddressSensitive {
    pub data: [f64; 4],
    _pin: PhantomPinned,
}

pub fn pin_it(x: &mut AddressSensitive) -> Pin<&mut AddressSensitive> {
    Pin::new(x)
}
```

*Check 3: pin! pins a !Unpin value on the stack; an index into an owned Vec survives moves* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::marker::PhantomPinned;
use std::pin::{pin, Pin};

struct AddressSensitive {
    data: [f64; 4],
    _pin: PhantomPinned,
}

// The index-based alternative: a "reference" to its own element that survives moves.
struct Track {
    samples: Vec<f64>,
    last: usize, // an index into `samples`, not a pointer
}

fn main() {
    // Unpin types: Pin::new is safe and adds no restriction.
    let mut plain = [1.0f64, 2.0];
    let p: Pin<&mut [f64; 2]> = Pin::new(&mut plain);
    println!("unpin via Pin::new: {}", p[1]);

    // A !Unpin value can still be pinned on the stack with pin!.
    let pinned: Pin<&mut AddressSensitive> = pin!(AddressSensitive { data: [0.5; 4], _pin: PhantomPinned });
    println!("stack-pinned via pin!: {}", pinned.data[3]);

    // The index survives every move of the struct, including into a Vec that later grows.
    let t = Track { samples: vec![1.0, 2.0, 3.0], last: 2 };
    let mut tracks = Vec::with_capacity(1);
    tracks.push(t);
    tracks.push(Track { samples: vec![9.0], last: 0 }); // may reallocate `tracks`
    let first = &tracks[0];
    println!("index after moves: {}", first.samples[first.last]);
}
```
Expected output: `unpin via Pin::new: 2 stack-pinned via pin!: 0.5 index after moves: 3`

