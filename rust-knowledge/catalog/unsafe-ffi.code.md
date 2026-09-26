# Unsafe Rust, UB & FFI — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](unsafe-ffi.md) · [catalog index](README.md)

## Choose extern "C" (a panic aborts, 1.81+) or extern "C-unwind" (a panic unwinds) for every boundary fn
**Since 1.81 a panic that reaches an extern "C" function aborts the process instead of unwinding into the caller; extern "C-unwind" (added in 1.71) lets it unwind; under panic=abort nothing unwinds anywhere; a foreign exception entering Rust through a "C" frame is UB.**

*Check 1: A panic escaping extern "C" aborts; catch_unwind never returns (Windows exit 0xC0000409)* · `runs` · edition 2024 · host · bin · exit code 3221226505 · **✔ oracle pass**
```rust
extern "C" fn law(x: u32) -> u32 {
    if x == 0 {
        panic!("zero");
    }
    x
}

fn main() {
    println!("before");
    let r = std::panic::catch_unwind(|| law(0));
    println!("after {}", r.is_err());
}
```
Expected output: `before`

*Check 2: A panic escaping extern "C-unwind" unwinds and catch_unwind catches it* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
extern "C-unwind" fn law(x: u32) -> u32 {
    if x == 0 {
        panic!("zero");
    }
    x
}

fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let r = std::panic::catch_unwind(|| law(0));
    println!("caught {}", r.is_err());
}
```
Expected output: `caught true`

*Check 3: Under -C panic=abort even C-unwind plus catch_unwind aborts (Windows exit 0xC0000409)* · `runs` · edition 2024 · host · bin · exit code 3221226505 · **✔ oracle pass**
```rust
extern "C-unwind" fn law(x: u32) -> u32 {
    if x == 0 {
        panic!("zero");
    }
    x
}

fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let r = std::panic::catch_unwind(|| law(0));
    println!("caught {}", r.is_err());
}
```

*Check 4: wasm32-unknown-unknown builds with cfg(panic = "abort") by default on 1.98.1* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · exports panic_strategy · node calls panic_strategy() · **✔ oracle pass**
```rust
#[cfg(panic = "abort")]
#[unsafe(no_mangle)]
pub extern "C" fn panic_strategy() -> u32 {
    1
}

#[cfg(panic = "unwind")]
#[unsafe(no_mangle)]
pub extern "C" fn panic_strategy() -> u32 {
    2
}
```
Expected output: `1`

## Cross the C ABI only with repr(C) types, scalars and raw pointers; pass strings as &CStr, c"" or CString
**Give C only types with a C-compatible layout (#[repr(C)] or #[repr(transparent)] structs, primitive numbers, raw pointers, Option of a non-null pointer or fn); improper_ctypes_definitions warns when an extern "C" fn takes Vec, &[T], &str or a default-repr struct; c"..." literals (1.77, edition 2021+) are &'static CStr with the NUL added, and CString owns one.**

*Check 1: improper_ctypes_definitions flags Vec<f64>, &[f64], &str and a default-repr struct* · `compiles` · edition 2024 · host · lib · lints: improper_ctypes_definitions · stderr has “`Vec<f64>`, which is not FFI-safe” · stderr has “`[f64]`, which is not FFI-safe” · stderr has “`str`, which is not FFI-safe” · stderr has “`Pose`, which is not FFI-safe” · stderr has “consider adding a `#[repr(C)]` or `#[repr(transparent)]` attribute” · **✔ oracle pass**
```rust
pub struct Pose {
    pub x: f64,
    pub y: f64,
}

#[unsafe(no_mangle)]
pub extern "C" fn load(v: Vec<f64>) -> u32 {
    v.len() as u32
}

#[unsafe(no_mangle)]
pub extern "C" fn sum(v: &[f64]) -> f64 {
    v.iter().sum()
}

#[unsafe(no_mangle)]
pub extern "C" fn name() -> &'static str {
    "law"
}

#[unsafe(no_mangle)]
pub extern "C" fn pose_x(p: Pose) -> f64 {
    p.x
}
```

*Check 2: A repr(C) struct, scalars and a (ptr, len) pair pass the lint cleanly* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
#[repr(C)]
pub struct Pose {
    pub x: f64,
    pub y: f64,
}

#[unsafe(no_mangle)]
pub extern "C" fn pose_x(p: Pose) -> f64 {
    p.x
}

/// # Safety
/// `ptr` must be valid for reads of `len` initialized, aligned f64.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn sum(ptr: *const f64, len: usize) -> f64 {
    // SAFETY: the caller guarantees ptr/len describe live, initialized f64s.
    let v = unsafe { core::slice::from_raw_parts(ptr, len) };
    v.iter().sum()
}
```

*Check 3: c"law" is a &'static CStr with a NUL; CString::new rejects an interior NUL* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::ffi::{CStr, CString};

fn main() {
    let lit: &'static CStr = c"law";
    println!("{} {:?}", lit.to_bytes_with_nul().len(), lit.to_str());
    println!("{}", CString::new("a\0b").is_err());
    let owned = CString::new("law").unwrap();
    println!("{}", owned.as_c_str() == lit);
}
```
Expected output: `4 Ok("law") true true`

*Check 4: as_ptr on a temporary CString dangles: dangling_pointers_from_temporaries warns* · `compiles` · edition 2024 · host · lib · lints: dangling_pointers_from_temporaries · stderr has “temporary `CString` is dropped at end of statement” · **✔ oracle pass**
```rust
use std::ffi::{c_char, CString};

pub fn name() -> *const c_char {
    CString::new("law").unwrap().as_ptr()
}
```

*Check 5: c"" literals do not parse in edition 2018* · `compile_fail` · edition 2018 · host · bin · stderr has “c-string literals require Rust 2021 or later” · **✔ oracle pass**
```rust
fn main() {
    let lit = c"law";
    println!("{}", lit.count_bytes());
}
```

## Make raw pointers with &raw const / &raw mut, move bytes with std::ptr, and change addresses with map_addr
**&raw const / &raw mut (1.82) point at a place without the intermediate reference that makes `&packed.field` or a reference to uninitialized memory UB; std::ptr's read, write and copy_nonoverlapping carry stated preconditions that debug builds partly assert (1.78); the strict-provenance APIs (1.84) change an address without an integer round trip.**

*Check 1: A reference to a packed struct's f64 field is E0793; *p through a raw pointer must be aligned* · `compile_fail` · edition 2024 · host · lib · errors: E0793 · stderr has “creating a misaligned reference is undefined behavior” · stderr has “must be properly aligned even when using raw pointers” · **✔ oracle pass**
```rust
#[repr(C, packed)]
pub struct Rec {
    pub tag: u8,
    pub x: f64,
}

pub fn x_ref(r: &Rec) -> &f64 {
    &r.x
}
```

*Check 2: &raw const equals addr_of! and read_unaligned reads the packed field* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
#[repr(C, packed)]
struct Rec {
    tag: u8,
    x: f64,
}

fn main() {
    let r = Rec { tag: 1, x: 2.5 };
    let p: *const f64 = &raw const r.x;
    let q: *const f64 = core::ptr::addr_of!(r.x);
    // SAFETY: p points at an initialized f64 inside r; read_unaligned tolerates the packing.
    let x = unsafe { p.read_unaligned() };
    let tag = r.tag;
    println!("{} {} {}", p == q, x, tag);
}
```
Expected output: `true 2.5 1`

*Check 3: copy_nonoverlapping, read_unaligned and write move f64 bits exactly* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::ptr;

fn main() {
    let src = [1.0f64, -0.0, 3.25];
    let mut dst = [0.0f64; 3];
    // SAFETY: two distinct live arrays of 3 f64, both 8-aligned, so the ranges cannot overlap.
    unsafe { ptr::copy_nonoverlapping(src.as_ptr(), dst.as_mut_ptr(), 3) };
    let bytes: [u8; 9] = [0xAA, 0, 0, 0, 0, 0, 0, 0xF0, 0x3F];
    // SAFETY: 8 initialized bytes start at offset 1; read_unaligned accepts any alignment.
    let one = unsafe { ptr::read_unaligned(bytes.as_ptr().add(1).cast::<f64>()) };
    let mut slot = 0.0f64;
    // SAFETY: slot is a valid, aligned, writable f64 with no destructor.
    unsafe { ptr::write(&raw mut slot, 7.5) };
    println!("{:?} {} {}", dst, one, slot);
}
```
Expected output: `[1.0, -0.0, 3.25] 1 7.5`

*Check 4: Debug assertions abort an overlapping copy_nonoverlapping before it runs (Windows 0xC0000409)* · `runs` · edition 2024 · host · bin · exit code 3221226505 · **✔ oracle pass**
```rust
fn main() {
    let mut buf = [1.0f64, 2.0, 3.0, 4.0, 5.0];
    let p = buf.as_mut_ptr();
    println!("before");
    // Violates the precondition: [0..3) and [1..4) overlap. The debug check aborts first.
    unsafe { std::ptr::copy_nonoverlapping(p, p.add(1), 3) };
    println!("after {:?}", buf);
}
```
Expected output: `before`

*Check 5: map_addr tags and untags a pointer without losing provenance* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
fn main() {
    let v: [f64; 2] = [1.5, 2.5];
    let p: *const f64 = v.as_ptr();
    // f64 is 8-aligned, so the low address bits are free for a tag.
    let tagged = p.map_addr(|a| a | 1);
    let flag = tagged.addr() & 1;
    let untagged = tagged.map_addr(|a| a & !1);
    // SAFETY: untagged has p's provenance and address; index 1 is in bounds.
    let x = unsafe { *untagged.add(1) };
    let sentinel = std::ptr::without_provenance::<f64>(8); // an address only, never dereferenced
    println!("{} {} {} {}", flag, x, untagged == p, sentinel.addr());
}
```
Expected output: `1 2.5 true 8`

*Check 6: (*p).len() on a raw slice pointer is denied by dangerous_implicit_autorefs* · `compile_fail` · edition 2024 · host · lib · lints: dangerous_implicit_autorefs · **✔ oracle pass**
```rust
pub fn count(p: *const [f64]) -> usize {
    unsafe { (*p).len() }
}
```

*Check 7: p.len() on the raw slice pointer needs no reference and no unsafe* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub fn count(p: *const [f64]) -> usize {
    p.len()
}
```

## Probe UB with const evaluation, which rejects invalid values and bad accesses with E0080; runtime is unchecked
**The Reference lists the UB classes (data races, dangling or misaligned access, aliasing violations, mutating immutable bytes, wrong call ABI or unwinding through a non-unwind frame, invalid values) and std adds library UB such as reaching unreachable_unchecked; rustc's const evaluator rejects the invalid-value, uninitialized, null, misaligned, dangling and unreachable cases it executes with E0080, while the same operations in runtime code compile silently.**

*Check 1: Const eval rejects an undeclared enum tag (5 in a 3-variant repr(u8) enum)* · `compile_fail` · edition 2024 · host · lib · errors: E0080 · stderr has “expected a valid enum tag” · **✔ oracle pass**
```rust
#[derive(Clone, Copy)]
#[repr(u8)]
pub enum Axis {
    X = 0,
    Y = 1,
    Z = 2,
}

pub const BAD: Axis = unsafe { core::mem::transmute::<u8, Axis>(5) };
```

*Check 2: Const eval rejects a surrogate char (0xD800)* · `compile_fail` · edition 2024 · host · lib · errors: E0080 · stderr has “expected a valid unicode scalar value” · **✔ oracle pass**
```rust
pub const C: char = unsafe { char::from_u32_unchecked(0xD800) };
```

*Check 3: Const eval rejects reading an uninitialized u8* · `compile_fail` · edition 2024 · host · lib · errors: E0080 · stderr has “memory is uninitialized” · **✔ oracle pass**
```rust
use core::mem::MaybeUninit;

pub const U: u8 = unsafe { MaybeUninit::<u8>::uninit().assume_init() };
```

*Check 4: Reaching unreachable_unchecked during const eval is E0080* · `compile_fail` · edition 2024 · host · lib · errors: E0080 · stderr has “entering unreachable code” · **✔ oracle pass**
```rust
pub const X: () = unsafe { core::hint::unreachable_unchecked() };
```

*Check 5: Const eval rejects a null reference* · `compile_fail` · edition 2024 · host · lib · errors: E0080 · stderr has “encountered a null reference” · **✔ oracle pass**
```rust
pub const R: &u32 = unsafe { &*core::ptr::null::<u32>() };
```

*Check 6: Const eval rejects a misaligned u16 load* · `compile_fail` · edition 2024 · host · lib · errors: E0080 · stderr has “alignment 2 is required” · **✔ oracle pass**
```rust
static BYTES: [u8; 4] = [1, 2, 3, 4];

pub const P: u16 = unsafe { *(BYTES.as_ptr().add(1) as *const u16) };
```

*Check 7: Const eval rejects a read through a pointer to a dead local* · `compile_fail` · edition 2024 · host · lib · errors: E0080 · stderr has “this pointer is dangling” · **✔ oracle pass**
```rust
const fn dangling() -> *const u32 {
    let x = 5u32;
    &x as *const u32
}

pub const D: u32 = unsafe { *dangling() };
```

*Check 8: The same invalid-bool transmute in a runtime fn compiles with no diagnostic* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
// UB if ever called; rustc says nothing. Only Miri would report it at run time.
pub fn flag() -> bool {
    unsafe { core::mem::transmute::<u8, bool>(2) }
}
```

*Check 9: invalid_value only warns on mem::zeroed for a reference type* · `compiles` · edition 2024 · host · lib · lints: invalid_value · stderr has “does not permit zero-initialization” · **✔ oracle pass**
```rust
pub fn null_ref() -> &'static i32 {
    unsafe { core::mem::zeroed() }
}
```

## Put each unsafe operation in its own unsafe block under a // SAFETY: line, even inside an unsafe fn
**Edition 2024 turns unsafe_op_in_unsafe_fn to warn, so an unsafe fn's body is no longer one implicit unsafe block: each unsafe operation gets an explicit block and a // SAFETY: comment, and clippy's restriction lints can enforce both.**

*Check 1: Edition 2024: a raw deref directly in an unsafe fn body warns unsafe_op_in_unsafe_fn* · `compiles` · edition 2024 · host · lib · lints: unsafe_op_in_unsafe_fn · stderr has “warning[E0133]” · **✔ oracle pass**
```rust
/// # Safety
/// `p` must be valid for reads of one aligned, initialized f64.
pub unsafe fn read_one(p: *const f64) -> f64 {
    *p
}
```

*Check 2: Edition 2021: the same unsafe fn compiles with no warning (lint allow-by-default)* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
/// # Safety
/// `p` must be valid for reads of one aligned, initialized f64.
pub unsafe fn read_one(p: *const f64) -> f64 {
    *p
}
```

*Check 3: An explicit unsafe block under a SAFETY comment is warning-free in 2024* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
/// # Safety
/// `p` must be valid for reads of one aligned, initialized f64.
pub unsafe fn read_one(p: *const f64) -> f64 {
    // SAFETY: the caller guarantees `p` is valid, aligned and initialized.
    unsafe { *p }
}
```

*Check 4: #![deny(unsafe_code)] rejects any unsafe block in the crate* · `compile_fail` · edition 2024 · host · lib · stderr has “usage of an `unsafe` block” · **✔ oracle pass**
```rust
#![deny(unsafe_code)]

pub fn read(p: *const f64) -> f64 {
    unsafe { *p }
}
```

*Check 5: deny(unsafe_code) plus #[allow(unsafe_code)] on one module compiles* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
#![deny(unsafe_code)]

#[allow(unsafe_code)]
pub mod ffi {
    /// # Safety
    /// `p` must be valid for reads of one aligned, initialized f64.
    pub unsafe fn read(p: *const f64) -> f64 {
        // SAFETY: the caller guarantees `p` is valid, aligned and initialized.
        unsafe { *p }
    }
}

pub fn safe_sum(v: &[f64]) -> f64 {
    v.iter().sum()
}
```

*Check 6: forbid(unsafe_code) cannot be relaxed by an inner allow (E0453)* · `compile_fail` · edition 2024 · host · lib · errors: E0453 · **✔ oracle pass**
```rust
#![forbid(unsafe_code)]

#[allow(unsafe_code)]
pub fn read(p: *const f64) -> f64 {
    unsafe { *p }
}
```

## Read unsafe as a short list of unlocked operations, never as a switch that turns the borrow checker off
**An unsafe block unlocks a fixed set of operations and nothing else: every other check keeps running inside it, and the code must still never produce a value that breaks its type's validity invariant.**

*Check 1: Dereferencing a raw pointer outside unsafe is E0133* · `compile_fail` · edition 2024 · host · lib · errors: E0133 · **✔ oracle pass**
```rust
pub fn read(p: *const f64) -> f64 {
    *p
}
```

*Check 2: Calling an unsafe fn outside unsafe is E0133* · `compile_fail` · edition 2024 · host · lib · errors: E0133 · stderr has “call to unsafe function `quantum_unchecked` is unsafe” · **✔ oracle pass**
```rust
/// # Safety
/// Callers must pass a quantum count below 64.
pub unsafe fn quantum_unchecked(n: u32) -> u32 {
    n
}

pub fn quantum() -> u32 {
    quantum_unchecked(3)
}
```

*Check 3: Reading a static mut outside unsafe is E0133* · `compile_fail` · edition 2024 · host · lib · errors: E0133 · stderr has “use of mutable static is unsafe and requires unsafe block” · **✔ oracle pass**
```rust
static mut QUANTA: u32 = 0;

pub fn quanta() -> u32 {
    QUANTA
}
```

*Check 4: Reading a union field outside unsafe is E0133* · `compile_fail` · edition 2024 · host · lib · errors: E0133 · stderr has “access to union field is unsafe” · **✔ oracle pass**
```rust
pub union Bits {
    pub f: f64,
    pub u: u64,
}

pub fn bits(b: Bits) -> u64 {
    b.u
}
```

*Check 5: Assigning to a union field needs no unsafe block* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub union Bits {
    pub f: f64,
    pub u: u64,
}

pub fn one() -> Bits {
    let mut b = Bits { u: 0 };
    b.f = 1.0;
    b
}
```

*Check 6: Implementing an unsafe trait without `unsafe impl` is E0200* · `compile_fail` · edition 2024 · host · lib · errors: E0200 · **✔ oracle pass**
```rust
/// # Safety
/// Implementors must be plain old data.
pub unsafe trait Pod {}

pub struct Pose;

impl Pod for Pose {}
```

*Check 7: Borrowck still runs inside unsafe (E0499); a block with nothing unsafe gets unused_unsafe* · `compile_fail` · edition 2024 · host · lib · errors: E0499 · lints: unused_unsafe · **✔ oracle pass**
```rust
pub fn push_twice(v: &mut Vec<f64>) {
    unsafe {
        let a = &mut *v;
        let b = &mut *v;
        a.push(1.0);
        b.push(2.0);
    }
}
```

*Check 8: Validity invariant: a bool built from 2 is rejected by const eval (E0080)* · `compile_fail` · edition 2024 · host · lib · errors: E0080 · stderr has “constructing invalid value” · stderr has “expected a boolean” · **✔ oracle pass**
```rust
pub const FLAG: bool = unsafe { core::mem::transmute::<u8, bool>(2) };
```

*Check 9: Safety invariant: const eval accepts a non-UTF-8 &str (UTF-8 is a library promise)* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
const fn bytes() -> [u8; 2] {
    [0xFF, 0xFE]
}

const BYTES: [u8; 2] = bytes();

// Compiles: validity of str only requires initialized bytes. Calling str methods on it
// could be UB later, so nothing here does.
pub const NOT_UTF8: &str = unsafe { core::str::from_utf8_unchecked(&BYTES) };
```

*Check 10: An invalid UTF-8 literal given to from_utf8_unchecked is caught by a deny lint instead* · `compile_fail` · edition 2024 · host · lib · lints: invalid_from_utf8_unchecked · **✔ oracle pass**
```rust
pub const NOT_UTF8: &str = unsafe { core::str::from_utf8_unchecked(&[0xFF]) };
```

## Replace every reference to a static mut with &raw mut before edition 2024 turns static_mut_refs into deny
**Taking & or &mut of a static mut, including hidden autorefs such as B.as_mut_ptr(), B.len() or S.field.as_ptr(), warns in edition 2021 and is denied in 2024; cargo fix --edition does not rewrite it; the sound form is a raw pointer from &raw mut (no unsafe needed since 1.82), with at most one short-lived reference made from it per call.**

*Check 1: Edition 2021: B.as_mut_ptr() on a static mut compiles with a static_mut_refs warning* · `compiles` · edition 2021 · host · lib · lints: static_mut_refs · stderr has “creating a mutable reference to mutable static” · **✔ oracle pass**
```rust
static mut BODIES: [f64; 4] = [0.0; 4];

#[no_mangle]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    unsafe { BODIES.as_mut_ptr() }
}
```

*Check 2: Edition 2024: as_mut_ptr() and a field's as_ptr() on static muts are denied* · `compile_fail` · edition 2024 · host · lib · lints: static_mut_refs · stderr has “creating a mutable reference to mutable static” · stderr has “creating a shared reference to mutable static” · **✔ oracle pass**
```rust
static mut BODIES: [f64; 4] = [0.0; 4];
struct Solver {
    snapshot: Vec<u8>,
}
static mut SOLVER: Solver = Solver { snapshot: Vec::new() };

#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    unsafe { BODIES.as_mut_ptr() }
}

#[unsafe(no_mangle)]
pub extern "C" fn snapshot_ptr() -> *const u8 {
    unsafe { SOLVER.snapshot.as_ptr() }
}
```

*Check 3: The &raw rewrite of the solver's access shapes is warning-free under edition 2024* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
const N: usize = 4;
static mut BODIES: [f64; N] = [0.0; N];
static mut COLLIDERS: [f64; N] = [0.0; N];
struct Solver {
    snapshot: Vec<u8>,
}
static mut SOLVER: Solver = Solver { snapshot: Vec::new() };

#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    // No unsafe: taking a raw pointer to a static mut creates no reference.
    (&raw mut BODIES).cast::<f64>()
}

#[unsafe(no_mangle)]
pub extern "C" fn snapshot_ptr() -> *const u8 {
    // SAFETY: one thread; no &mut SOLVER is live during this call.
    unsafe { (*(&raw const SOLVER)).snapshot.as_ptr() }
}

#[unsafe(no_mangle)]
pub extern "C" fn snapshot_len() -> u32 {
    // SAFETY: as in snapshot_ptr.
    unsafe { (*(&raw const SOLVER)).snapshot.len() as u32 }
}

#[unsafe(no_mangle)]
pub extern "C" fn step(n: u32) -> u32 {
    if n as usize > N {
        return 0;
    }
    // SAFETY: one thread, no export re-enters another, and JS touches the buffers only
    // between calls, so these are the only references to BODIES and COLLIDERS while step runs.
    let bodies: &mut [f64; N] = unsafe { &mut *(&raw mut BODIES) };
    let colliders: &[f64; N] = unsafe { &*(&raw const COLLIDERS) };
    bodies[0] += colliders[0];
    1
}

#[unsafe(no_mangle)]
pub extern "C" fn solver_clear() -> u32 {
    // The shape ensure / solver_step already use (lint-free): a reference that lives
    // only inside this call.
    // SAFETY: one thread, no re-entry: the only reference to SOLVER while this runs.
    let solver = unsafe { &mut *core::ptr::addr_of_mut!(SOLVER) };
    solver.snapshot.clear();
    1
}
```

*Check 4: The same rewrite is warning-free under edition 2021, so it can land before the bump* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
const N: usize = 4;
static mut BODIES: [f64; N] = [0.0; N];
static mut COLLIDERS: [f64; N] = [0.0; N];
struct Solver {
    snapshot: Vec<u8>,
}
static mut SOLVER: Solver = Solver { snapshot: Vec::new() };

#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    // No unsafe: taking a raw pointer to a static mut creates no reference.
    (&raw mut BODIES).cast::<f64>()
}

#[unsafe(no_mangle)]
pub extern "C" fn snapshot_ptr() -> *const u8 {
    // SAFETY: one thread; no &mut SOLVER is live during this call.
    unsafe { (*(&raw const SOLVER)).snapshot.as_ptr() }
}

#[unsafe(no_mangle)]
pub extern "C" fn snapshot_len() -> u32 {
    // SAFETY: as in snapshot_ptr.
    unsafe { (*(&raw const SOLVER)).snapshot.len() as u32 }
}

#[unsafe(no_mangle)]
pub extern "C" fn step(n: u32) -> u32 {
    if n as usize > N {
        return 0;
    }
    // SAFETY: one thread, no export re-enters another, and JS touches the buffers only
    // between calls, so these are the only references to BODIES and COLLIDERS while step runs.
    let bodies: &mut [f64; N] = unsafe { &mut *(&raw mut BODIES) };
    let colliders: &[f64; N] = unsafe { &*(&raw const COLLIDERS) };
    bodies[0] += colliders[0];
    1
}

#[unsafe(no_mangle)]
pub extern "C" fn solver_clear() -> u32 {
    // The shape ensure / solver_step already use (lint-free): a reference that lives
    // only inside this call.
    // SAFETY: one thread, no re-entry: the only reference to SOLVER while this runs.
    let solver = unsafe { &mut *core::ptr::addr_of_mut!(SOLVER) };
    solver.snapshot.clear();
    1
}
```

*Check 5: Indexing a static mut array directly (BODIES[i]) makes no reference and is not linted* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
static mut BODIES: [f64; 4] = [0.0; 4];

pub fn get(i: usize) -> f64 {
    // SAFETY: one thread; no reference to BODIES is live.
    unsafe { BODIES[i] }
}

pub fn set(i: usize, x: f64) {
    // SAFETY: as in get.
    unsafe { BODIES[i] = x };
}
```

*Check 6: wasm32 build of the rewrite exports its names, imports nothing, and step mutates* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · exports memory, bodies_ptr, step, probe · imports nothing · node calls probe() · **✔ oracle pass**
```rust
const N: usize = 4;
static mut BODIES: [f64; N] = [0.0; N];

#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    (&raw mut BODIES).cast::<f64>()
}

#[unsafe(no_mangle)]
pub extern "C" fn step(n: u32) -> u32 {
    if n as usize > N {
        return 0;
    }
    // SAFETY: one thread, no re-entry: the only reference to BODIES while step runs.
    let bodies: &mut [f64; N] = unsafe { &mut *(&raw mut BODIES) };
    bodies[0] += 1.5;
    1
}

#[unsafe(no_mangle)]
pub extern "C" fn probe() -> f64 {
    step(1);
    step(1);
    // SAFETY: the &mut taken inside step ended when step returned.
    unsafe { *bodies_ptr() }
}
```
Expected output: `3`

*Check 7: A plain static UnsafeCell is E0277: UnsafeCell is not Sync* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “cannot be shared between threads safely” · **✔ oracle pass**
```rust
use std::cell::UnsafeCell;

static BODIES: UnsafeCell<[f64; 4]> = UnsafeCell::new([0.0; 4]);

pub fn bodies_ptr() -> *mut f64 {
    BODIES.get().cast::<f64>()
}
```

*Check 8: std's SyncUnsafeCell is still unstable on 1.98.1 (E0658)* · `compile_fail` · edition 2024 · host · lib · errors: E0658 · stderr has “sync_unsafe_cell” · **✔ oracle pass**
```rust
use std::cell::SyncUnsafeCell;

static BODIES: SyncUnsafeCell<[f64; 4]> = SyncUnsafeCell::new([0.0; 4]);

pub fn bodies_ptr() -> *mut f64 {
    BODIES.get().cast::<f64>()
}
```

*Check 9: An UnsafeCell wrapper with unsafe impl Sync works as a static buffer* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::cell::UnsafeCell;

#[repr(transparent)]
pub struct Buf<const N: usize>(UnsafeCell<[f64; N]>);

// SAFETY: only one thread ever calls into this module, and no call re-enters another,
// so no two accesses to a Buf overlap. A native host must keep that promise.
unsafe impl<const N: usize> Sync for Buf<N> {}

impl<const N: usize> Buf<N> {
    pub const fn new() -> Self {
        Buf(UnsafeCell::new([0.0; N]))
    }
    pub fn ptr(&self) -> *mut f64 {
        self.0.get().cast::<f64>()
    }
}

pub static BODIES: Buf<{ 64 * 17 }> = Buf::new();

#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    BODIES.ptr()
}

fn step() -> f64 {
    // SAFETY: no other reference into BODIES is live while step runs.
    let b: &mut [f64; 64 * 17] = unsafe { &mut *BODIES.0.get() };
    b[0] += 1.0;
    b[0]
}

fn main() {
    step();
    // SAFETY: slot 1 is in bounds and no reference into BODIES is live.
    unsafe { *bodies_ptr().add(1) = 2.5 };
    let second = step();
    // SAFETY: as above.
    let slot1 = unsafe { *bodies_ptr().add(1) };
    println!("{} {}", second, slot1);
}
```
Expected output: `2 2.5`

*Check 10: An atomic replaces a scalar static mut with no unsafe at all* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::sync::atomic::{AtomicU32, Ordering};

static LOADS: AtomicU32 = AtomicU32::new(0);

fn load() -> u32 {
    LOADS.fetch_add(1, Ordering::Relaxed) + 1
}

fn main() {
    load();
    println!("{}", load());
}
```
Expected output: `2`

*Check 11: #![allow(static_mut_refs)] silences the 2024 deny: a lint, not a soundness check* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
#![allow(static_mut_refs)]

static mut BODIES: [f64; 4] = [0.0; 4];

#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    unsafe { BODIES.as_mut_ptr() }
}
```

## Run Miri on the law natively: Stacked Borrows is its default aliasing model, Tree Borrows is opt-in
**Miri (a nightly component) interprets a test suite and reports the UB it executes: out-of-bounds and use-after-free, uninitialized reads, misalignment, invalid values, data races and, experimentally, aliasing violations under Stacked Borrows (default) or Tree Borrows (-Zmiri-tree-borrows); it supports tier-1 hosts, has almost no FFI, and checks only what the tests run.**

*Check 1: cfg!(miri) is false when rustc itself compiles the crate* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
fn main() {
    // Set only when `cargo miri` builds the crate for interpretation.
    println!("{}", cfg!(miri));
}
```
Expected output: `false`

*Check 2: A pure law-helper test plus a cfg_attr(miri, ignore) test both run under rustc --test* · `runs` · edition 2021 · host · test · no warnings · output has “2 passed” · **✔ oracle pass**
```rust
// Same rule as lib.rs js_min: JavaScript Math.min semantics for signed zero.
fn js_min(a: f64, b: f64) -> f64 {
    if b < a || (a == 0.0 && b == 0.0 && b.is_sign_negative() && !a.is_sign_negative()) {
        b
    } else {
        a
    }
}

#[cfg(test)]
mod tests {
    use super::js_min;

    #[test]
    fn min_keeps_negative_zero() {
        assert!(js_min(0.0, -0.0).is_sign_negative());
        assert!(js_min(-0.0, 0.0).is_sign_negative());
        assert_eq!(js_min(1.0, 2.0), 1.0);
    }

    #[test]
    #[cfg_attr(miri, ignore)] // stands in for a full-world test too slow to interpret
    fn many_quanta() {
        let mut m = f64::INFINITY;
        for i in 0..100_000 {
            m = js_min(m, (i % 977) as f64);
        }
        assert_eq!(m, 0.0);
    }
}
```

*Check 3: The pinned stable compiler refuses nightly features: #![feature] is E0554* · `compile_fail` · edition 2024 · host · bin · errors: E0554 · **✔ oracle pass**
```rust
#![feature(cfg_sanitize)]

fn main() {}
```

## Write #[unsafe(no_mangle)], #[unsafe(export_name)], #[unsafe(link_section)] and unsafe extern blocks now
**Edition 2024 makes the bare no_mangle / export_name / link_section attributes and unmarked extern blocks hard errors; the unsafe(...) attribute form and `unsafe extern` blocks with per-item `safe fn` / `unsafe fn` are accepted by every edition since 1.82, so the rewrite can land before the edition bump.**

*Check 1: Edition 2024: a bare #[no_mangle] is a hard error with no error code* · `compile_fail` · edition 2024 · host · lib · stderr has “unsafe attribute used without unsafe” · stderr has “#[unsafe(no_mangle)]” · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn step(n: u32) -> u32 {
    n
}
```

*Check 2: Edition 2024: bare export_name and link_section fail the same way* · `compile_fail` · edition 2024 · host · lib · stderr has “unsafe attribute used without unsafe” · stderr has “#[unsafe(export_name = "law_version")]” · stderr has “#[unsafe(link_section = ".law")]” · **✔ oracle pass**
```rust
#[export_name = "law_version"]
pub extern "C" fn version() -> u32 {
    2
}

#[link_section = ".law"]
#[used]
pub static LAW: [u8; 2] = [1, 0];
```

*Check 3: Edition 2021 accepts all three unsafe(...) attribute forms with no warning* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn step(n: u32) -> u32 {
    n
}

#[unsafe(export_name = "law_version")]
pub extern "C" fn version() -> u32 {
    2
}

#[unsafe(link_section = ".law")]
#[used]
pub static LAW: [u8; 2] = [1, 0];
```

*Check 4: Migration lints under 2021 say both forms are hard errors in Rust 2024* · `compiles` · edition 2021 · host · lib · stderr has “is a hard error in Rust 2024” · stderr has “extern blocks should be unsafe” · stderr has “unsafe attribute used without unsafe” · **✔ oracle pass**
```rust
#![warn(unsafe_attr_outside_unsafe, missing_unsafe_on_extern)]

#[no_mangle]
pub extern "C" fn step() -> u32 {
    1
}

extern "C" {
    pub fn abs(x: i32) -> i32;
}
```

*Check 5: Edition 2024: an extern block without unsafe is an error* · `compile_fail` · edition 2024 · host · lib · stderr has “extern blocks must be unsafe” · **✔ oracle pass**
```rust
extern "C" {
    pub fn abs(x: i32) -> i32;
}
```

*Check 6: A `safe fn` in an unsafe extern block is callable without unsafe* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
unsafe extern "C" {
    // abs from the C runtime accepts any i32 except i32::MIN, which we never pass.
    safe fn abs(x: i32) -> i32;
}

fn main() {
    println!("{}", abs(-3));
}
```
Expected output: `3`

*Check 7: An extern item with no qualifier defaults to unsafe: calling it bare is E0133* · `compile_fail` · edition 2024 · host · bin · errors: E0133 · **✔ oracle pass**
```rust
unsafe extern "C" {
    fn abs(x: i32) -> i32;
}

fn main() {
    println!("{}", abs(-3));
}
```

*Check 8: safe / unsafe item qualifiers are refused in an extern block not marked unsafe* · `compile_fail` · edition 2021 · host · lib · stderr has “cannot have safety qualifiers” · **✔ oracle pass**
```rust
extern "C" {
    pub safe fn abs(x: i32) -> i32;
}
```

*Check 9: wasm32: #[unsafe(no_mangle)] and #[unsafe(export_name)] export the expected names* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · exports memory, step, law_version · imports nothing · node calls law_version() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn step(n: u32) -> u32 {
    n
}

#[unsafe(export_name = "law_version")]
pub extern "C" fn version() -> u32 {
    2
}
```
Expected output: `2`

## Never write through a pointer cast from &T: the solver's warm-start clear does, and rustc's lint misses it
**solver_clear_warmstart turns each &ContactPair from NarrowPhase::contact_pairs() into *mut and reborrows it as &mut to zero warm-start impulses; a pointer derived from a shared reference never carries write permission, whoever holds the owner, rustc documents the &T-to-&mut T cast as UB, and its lint catches only the one-expression forms, not this Vec hop.**

*Check 1: rustc rejects &mut *(from_ref(p) as *mut T): 'UB, even if the reference is unused'* · `compile_fail` · edition 2021 · host · lib · lints: invalid_reference_casting · stderr has “casting `&T` to `&mut T` is undefined behavior, even if the reference is unused” · **✔ oracle pass**
```rust
pub struct ContactPair {
    pub manifolds: Vec<f64>,
}

pub fn clear(pair: &ContactPair) {
    let p = unsafe { &mut *(core::ptr::from_ref(pair) as *mut ContactPair) };
    p.manifolds.clear();
}
```

*Check 2: rustc rejects a whole-value write through the cast: 'assigning to `&T` is UB'* · `compile_fail` · edition 2021 · host · lib · lints: invalid_reference_casting · stderr has “assigning to `&T` is undefined behavior” · **✔ oracle pass**
```rust
pub struct Manifold {
    pub warmstart_impulse: f64,
}

pub fn clear(m: &Manifold) {
    unsafe { *(core::ptr::from_ref(m) as *mut Manifold) = Manifold { warmstart_impulse: 0.0 } };
}
```

*Check 3: Lint blind spot 1: a field write through the same cast, in one expression, compiles silently* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
pub struct Manifold {
    pub warmstart_impulse: f64,
}

// UB exactly like the rejected forms; rustc says nothing.
pub fn clear(m: &Manifold) {
    unsafe { (*(core::ptr::from_ref(m) as *mut Manifold)).warmstart_impulse = 0.0 };
}
```

*Check 4: Lint blind spot 2: the solver's Vec-of-pointers form compiles with no diagnostic* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
pub struct Manifold {
    pub warmstart_impulse: f64,
}

pub struct ContactPair {
    pub manifolds: Vec<Manifold>,
}

pub struct NarrowPhase {
    pairs: Vec<ContactPair>,
}

impl NarrowPhase {
    pub fn contact_pairs(&self) -> impl Iterator<Item = &ContactPair> {
        self.pairs.iter()
    }
}

fn zero_manifolds(manifolds: &mut [Manifold]) -> u32 {
    let mut n = 0;
    for m in manifolds {
        m.warmstart_impulse = 0.0;
        n += 1;
    }
    n
}

// The shape of solver_clear_warmstart: UB, and rustc says nothing.
pub fn clear_warmstart(narrow: &mut NarrowPhase) -> u32 {
    let mut ptrs: Vec<*mut ContactPair> = Vec::new();
    for pair in narrow.contact_pairs() {
        ptrs.push(core::ptr::from_ref(pair) as *mut ContactPair);
    }
    let mut n = 0u32;
    for ptr in ptrs {
        unsafe {
            let pair = &mut *ptr;
            n += zero_manifolds(&mut pair.manifolds);
        }
    }
    n
}
```

*Check 5: The sound shape: a &mut accessor that starts at the owner makes the clear safe code* · `runs` · edition 2021 · host · bin · no warnings · **✔ oracle pass**
```rust
pub struct Manifold {
    pub warmstart_impulse: f64,
}

pub struct ContactPair {
    pub manifolds: Vec<Manifold>,
}

pub struct NarrowPhase {
    pairs: Vec<ContactPair>,
}

impl NarrowPhase {
    // What a pinned patch would add: &mut self in, &mut pairs out. No cast anywhere.
    pub fn contact_pairs_mut(&mut self) -> impl Iterator<Item = &mut ContactPair> {
        self.pairs.iter_mut()
    }
}

fn zero_manifolds(manifolds: &mut [Manifold]) -> u32 {
    let mut n = 0;
    for m in manifolds {
        m.warmstart_impulse = 0.0;
        n += 1;
    }
    n
}

fn main() {
    let mut narrow = NarrowPhase {
        pairs: vec![
            ContactPair { manifolds: vec![Manifold { warmstart_impulse: 0.5 }] },
            ContactPair { manifolds: vec![Manifold { warmstart_impulse: -1.0 }] },
        ],
    };
    let mut n = 0;
    for pair in narrow.contact_pairs_mut() {
        n += zero_manifolds(&mut pair.manifolds);
    }
    let left: f64 = narrow
        .pairs
        .iter()
        .flat_map(|p| p.manifolds.iter())
        .map(|m| m.warmstart_impulse.abs())
        .sum();
    println!("{} {}", n, left);
}
```
Expected output: `2 0`

*Check 6: rapier3d-f64 0.35.3 has no NarrowPhase::contact_pairs_mut (E0599)* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0599 · stderr has “no method named `contact_pairs_mut`” · **✔ oracle pass**
```rust
use rapier3d_f64::geometry::NarrowPhase;

pub fn clear(n: &mut NarrowPhase) -> usize {
    let mut k = 0;
    for pair in n.contact_pairs_mut() {
        for m in &mut pair.manifolds {
            k += m.points.len();
        }
    }
    k
}
```

*Check 7: NarrowPhase's contact_graph field is private in 0.35.3 (E0616)* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0616 · **✔ oracle pass**
```rust
use rapier3d_f64::geometry::NarrowPhase;

pub fn edges(n: &mut NarrowPhase) -> usize {
    n.contact_graph.raw_graph().raw_edges().len()
}
```

