# What changed in Rust 1.80 → 1.98 — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](rust-currency.md) · [catalog index](README.md)

## Expect 1.86-1.98 lint escalations to break old unsafe and macro code on a toolchain bump
**Lints tightened in the period, in every edition: dangerous_implicit_autorefs (added 1.88, deny 1.89), missing_fragment_specifier (hard error 1.89), semicolon_in_expressions_from_macros (deny 1.91), never_type_fallback_flowing_into_unsafe and dependency_on_unit_never_type_fallback (deny 1.92), deref_nullptr (deny 1.93), invalid_runtime_symbol_definitions (new, deny 1.98); new warn-by-default lints include missing_abi (1.86), mismatched_lifetime_syntaxes (1.89), dangling_pointers_from_locals (1.91) and linker_messages (1.97, outside the `warnings` group).**

*Check 1: deref_nullptr is deny-by-default (1.93)* · `compile_fail` · edition 2024 · host · lib · lints: deref_nullptr · **✔ oracle pass**
```rust
pub fn read_null() -> f64 {
    unsafe { *std::ptr::null::<f64>() }
}
```

*Check 2: indexing through (*ptr) is a deny-level implicit autoref (1.89)* · `compile_fail` · edition 2024 · host · lib · lints: dangerous_implicit_autorefs · **✔ oracle pass**
```rust
pub unsafe fn first_record(ptr: *mut [f64]) -> *mut [f64] {
    unsafe { &raw mut (*ptr)[..17] }
}
```

*Check 3: an explicit &mut *ptr reborrow compiles cleanly* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub unsafe fn first_record(ptr: *mut [f64]) -> *mut [f64] {
    unsafe { &raw mut (&mut *ptr)[..17] }
}
```

*Check 4: relying on () never-type fallback fails even in edition 2021 (1.92)* · `compile_fail` · edition 2021 · host · bin · lints: dependency_on_unit_never_type_fallback · **✔ oracle pass**
```rust
fn outer<T>(x: T) -> Result<T, ()> {
    fn f<T: Default>() -> Result<T, ()> {
        Ok(T::default())
    }
    f()?;
    Ok(x)
}

fn main() {
    println!("{:?}", outer(3));
}
```

*Check 5: a trailing semicolon in an expression macro is deny (1.91)* · `compile_fail` · edition 2024 · host · lib · lints: semicolon_in_expressions_from_macros · **✔ oracle pass**
```rust
macro_rules! half {
    ($e:expr) => {
        $e * 0.5;
    };
}

pub fn f(x: f64) -> f64 {
    half!(x)
}
```

*Check 6: a memset symbol with the wrong signature is deny (1.98)* · `compile_fail` · edition 2024 · host · lib · lints: invalid_runtime_symbol_definitions · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn memset(dst: *mut u8) -> *mut u8 {
    dst
}
```

*Check 7: extern without an ABI string warns (1.86)* · `compiles` · edition 2024 · host · lib · lints: missing_abi · **✔ oracle pass**
```rust
pub extern fn tick() -> u32 {
    1
}
```

*Check 8: returning a pointer to a local warns (1.91)* · `compiles` · edition 2024 · host · lib · lints: dangling_pointers_from_locals · **✔ oracle pass**
```rust
pub fn dangling() -> *const f64 {
    let x = 1.5f64;
    &x
}
```

*Check 9: a hidden elided lifetime in the return type warns (1.89)* · `compiles` · edition 2024 · host · lib · lints: mismatched_lifetime_syntaxes · **✔ oracle pass**
```rust
pub fn items(scores: &[u8]) -> std::slice::Iter<u8> {
    scores.iter()
}
```

## Expect edition 2024 to drop if-let scrutinee and tail-expression temporaries earlier
**Edition 2024 drops the temporaries of an `if let` scrutinee before the `else` branch runs and drops a block's tail-expression temporaries before its local variables; both reorder `Drop` side effects (checked), and the first is why let chains (stable 1.88) are 2024-only.**

*Check 1: edition 2021: an if-let scrutinee temporary drops after the else branch* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
struct Guard(&'static str);

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

impl Guard {
    fn body(&self) -> Option<u32> {
        None
    }
}

fn main() {
    if let Some(n) = Guard("scrutinee").body() {
        println!("then {n}");
    } else {
        println!("else");
    }
    println!("after");
}
```
Expected output: `else drop scrutinee after`

*Check 2: edition 2024: the same temporary drops before the else branch runs* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
struct Guard(&'static str);

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

impl Guard {
    fn body(&self) -> Option<u32> {
        None
    }
}

fn main() {
    if let Some(n) = Guard("scrutinee").body() {
        println!("then {n}");
    } else {
        println!("else");
    }
    println!("after");
}
```
Expected output: `drop scrutinee else after`

*Check 3: edition 2021: a tail-expression borrow of a block's local is E0597* · `compile_fail` · edition 2021 · host · lib · errors: E0597 · **✔ oracle pass**
```rust
use std::cell::RefCell;

pub fn f() -> usize {
    let c = RefCell::new("..");
    c.borrow().len()
}
```

*Check 4: edition 2024: the same tail expression compiles* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
use std::cell::RefCell;

pub fn f() -> usize {
    let c = RefCell::new("..");
    c.borrow().len()
}
```

*Check 5: edition 2021: the tail temporary drops after the block's local* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
struct Guard(&'static str);

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn len_of(g: &Guard) -> usize {
    g.0.len()
}

fn tail() -> usize {
    let _local = Guard("local");
    len_of(&Guard("temporary"))
}

fn main() {
    let n = tail();
    println!("{n}");
}
```
Expected output: `drop local drop temporary 9`

*Check 6: edition 2024: the tail temporary drops before the block's local* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
struct Guard(&'static str);

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn len_of(g: &Guard) -> usize {
    g.0.len()
}

fn tail() -> usize {
    let _local = Guard("local");
    len_of(&Guard("temporary"))
}

fn main() {
    let n = tail();
    println!("{n}");
}
```
Expected output: `drop temporary drop local 9`

*Check 7: edition 2021 rejects a let chain* · `compile_fail` · edition 2021 · host · lib · stderr has “let chains are only allowed in Rust 2024 or later” · **✔ oracle pass**
```rust
fn first_positive(v: &[f64]) -> Option<f64> {
    if let Some(&x) = v.first() && x > 0.0 {
        Some(x)
    } else {
        None
    }
}

fn main() {
    println!("{:?}", first_positive(&[1.5, -2.0]));
}
```

*Check 8: edition 2024 runs the same let chain* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
fn first_positive(v: &[f64]) -> Option<f64> {
    if let Some(&x) = v.first() && x > 0.0 {
        Some(x)
    } else {
        None
    }
}

fn main() {
    println!("{:?}", first_positive(&[1.5, -2.0]));
}
```
Expected output: `Some(1.5)`

*Check 9: edition 2024: an if-let guard in a match arm (stable 1.95)* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
fn parse(s: &str) -> Option<f64> {
    s.parse().ok()
}

fn main() {
    let v = Some("2.5");
    match v {
        Some(s) if let Some(x) = parse(s) => println!("{x}"),
        _ => println!("none"),
    }
}
```
Expected output: `2.5`

*Check 10: edition 2021: the same if-let guard compiles and runs too* · `runs` · edition 2021 · host · bin · no warnings · **✔ oracle pass**
```rust
fn parse(s: &str) -> Option<f64> {
    s.parse().ok()
}

fn main() {
    let v = Some("2.5");
    match v {
        Some(s) if let Some(x) = parse(s) => println!("{x}"),
        _ => println!("none"),
    }
}
```
Expected output: `2.5`

## Expect wasm32 undefined symbols to fail the link since 1.96 and the standard C ABI since 1.89
**Since 1.96 rustc no longer passes --allow-undefined to wasm-ld, so an extern function with no definition is a link error ('undefined symbol') instead of a silent `env` import; since 1.89 `extern "C"` on wasm32-unknown-unknown follows the standard tool-conventions C ABI, which changed how aggregates are passed and left scalars alone; 1.84 removed the wasm32-wasi target name (now wasm32-wasip1) and added wasm32v1-none at Tier 2.**

*Check 1: 1.96+: an undefined extern fn is a wasm link error, not an env import* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “undefined symbol: host_gravity” · **✔ oracle pass**
```rust
unsafe extern "C" {
    fn host_gravity() -> f64;
}

#[unsafe(no_mangle)]
pub extern "C" fn fall(vy: f64) -> f64 {
    vy + unsafe { host_gravity() } / 64.0
}
```

*Check 2: #[link(wasm_import_module = "env")] makes the import explicit and links* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · exports fall · **✔ oracle pass**
```rust
#[link(wasm_import_module = "env")]
unsafe extern "C" {
    fn host_gravity() -> f64;
}

#[unsafe(no_mangle)]
pub extern "C" fn fall(vy: f64) -> f64 {
    vy + unsafe { host_gravity() } / 64.0
}
```

*Check 3: -C link-arg=--allow-undefined restores the pre-1.96 behaviour* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · exports fall · **✔ oracle pass**
```rust
unsafe extern "C" {
    fn host_gravity() -> f64;
}

#[unsafe(no_mangle)]
pub extern "C" fn fall(vy: f64) -> f64 {
    vy + unsafe { host_gravity() } / 64.0
}
```

*Check 4: scalar-only exports pass u32 and f64 directly* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · imports nothing · node calls mix(3, 1.5) · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn mix(n_bodies: u32, dt: f64) -> f64 {
    n_bodies as f64 * dt
}
```
Expected output: `4.5`

## Keep 1.98's f64::algebraic_* methods out of the law: the std docs allow different results per run
**1.98 stabilized `algebraic_add`, `_sub`, `_mul`, `_div` and `_rem` on f32 and f64, which let the compiler combine and reorder operations, swap division for reciprocal multiplication and ignore the sign of zero; the core docs say the same inputs may produce different results even within one program run. They compile on stable with no feature gate and no warning (checked).**

*Check 1: algebraic_add is stable on 1.98.1: no feature gate, no warning* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub fn sum4(a: f64, b: f64, c: f64, d: f64) -> f64 {
    a.algebraic_add(b).algebraic_add(c).algebraic_add(d)
}
```

*Check 2: algebraic_add also compiles for wasm32-unknown-unknown* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · exports sum4 · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn sum4(a: f64, b: f64, c: f64, d: f64) -> f64 {
    a.algebraic_add(b).algebraic_add(c).algebraic_add(d)
}
```

*Check 3: f64::NAN has the quiet bit set (guaranteed since 1.88)* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
fn main() {
    // bit 51 is the quiet bit of an f64 NaN
    println!("{}", f64::NAN.to_bits() & (1u64 << 51) != 0);
}
```
Expected output: `true`

*Check 4: a const fn float constant matches the runtime bits (50 deg to rad)* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::f64::consts::PI;
use std::hint::black_box;

const fn radians(deg: f64) -> f64 {
    deg * PI / 180.0
}

const SLIDE_ANGLE: f64 = radians(50.0);

fn main() {
    println!("{}", SLIDE_ANGLE.to_bits() == radians(black_box(50.0)).to_bits());
}
```
Expected output: `true`

## Know which edition-2024 changes cargo fix --edition migrates and which stay manual
**Of the Edition Guide's 2024 list, `cargo fix --edition` rewrites unsafe attributes, unsafe extern blocks, unsafe_op_in_unsafe_fn, if-let (into match), RPIT over-capture (inserts `use<..>`), `expr` -> `expr_2021`, `gen` -> `r#gen`, `Box<[T]>::into_iter`, prelude collisions, reserved `#".."#` syntax, match-ergonomics patterns, `env::set_var` calls and Cargo.toml key names; it does not migrate static_mut_refs, tail-expression drop order, never-type fallback, missing macro fragment specifiers, combined doctests or the resolver change.**

*Check 1: edition 2021: a const { .. } argument skips the $e:expr arm* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
macro_rules! which {
    ($e:expr) => {
        "expr"
    };
    (const $b:block) => {
        "const block"
    };
}

fn main() {
    println!("{}", which!(const { 1.0f64 + 0.5 }));
}
```
Expected output: `const block`

*Check 2: edition 2024: the $e:expr arm now matches const { .. }* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
macro_rules! which {
    ($e:expr) => {
        "expr"
    };
    (const $b:block) => {
        "const block"
    };
}

fn main() {
    println!("{}", which!(const { 1.0f64 + 0.5 }));
}
```
Expected output: `expr`

*Check 3: edition 2021: RPIT does not capture the argument lifetime (E0700)* · `compile_fail` · edition 2021 · host · lib · errors: E0700 · **✔ oracle pass**
```rust
pub fn doubled(v: &Vec<f64>) -> impl Iterator<Item = f64> {
    v.iter().map(|x| x * 2.0)
}
```

*Check 4: edition 2024: the same RPIT captures it and compiles* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub fn doubled(v: &Vec<f64>) -> impl Iterator<Item = f64> {
    v.iter().map(|x| x * 2.0)
}
```

*Check 5: edition 2021: Box<[f64]>::into_iter yields &f64, so collecting Vec<f64> is E0277* · `compile_fail` · edition 2021 · host · lib · errors: E0277 · **✔ oracle pass**
```rust
pub fn owned(heights: Box<[f64]>) -> Vec<f64> {
    heights.into_iter().collect()
}
```

*Check 6: edition 2024: Box<[f64]>::into_iter yields f64 and the collect compiles* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub fn owned(heights: Box<[f64]>) -> Vec<f64> {
    heights.into_iter().collect()
}
```

*Check 7: edition 2024: gen is a reserved keyword* · `compile_fail` · edition 2024 · host · lib · stderr has “reserved keyword `gen`” · **✔ oracle pass**
```rust
pub fn gen(seed: u64) -> u64 {
    seed.wrapping_mul(6364136223846793005)
}
```

*Check 8: edition 2024: a plain extern block is rejected* · `compile_fail` · edition 2024 · host · lib · stderr has “extern blocks must be unsafe” · **✔ oracle pass**
```rust
extern "C" {
    fn host_sqrt(x: f64) -> f64;
}

pub fn call(x: f64) -> f64 {
    unsafe { host_sqrt(x) }
}
```

*Check 9: edition 2024: an unsafe op in an unsafe fn body warns* · `compiles` · edition 2024 · host · lib · lints: unsafe_op_in_unsafe_fn · **✔ oracle pass**
```rust
pub unsafe fn read(p: *const f64) -> f64 {
    *p
}
```

*Check 10: edition 2024: std::env::set_var needs an unsafe block (E0133)* · `compile_fail` · edition 2024 · host · bin · errors: E0133 · **✔ oracle pass**
```rust
fn main() {
    std::env::set_var("SI_SEED", "1");
}
```

*Check 11: edition 2024: code relying on () never-type fallback is a type error (E0277)* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · **✔ oracle pass**
```rust
fn outer<T>(x: T) -> Result<T, ()> {
    fn f<T: Default>() -> Result<T, ()> {
        Ok(T::default())
    }
    f()?;
    Ok(x)
}

fn main() {
    println!("{:?}", outer(3));
}
```

## Move si-solver to edition 2024: cargo fix rewrites 10 #[no_mangle], hand-fix 7 static_mut_refs
**On 1.98.1, `cargo fix --edition` on a copy of solver/ changed only the 10 `#[no_mangle]` exports to `#[unsafe(no_mangle)]`, left `edition = "2021"` in Cargo.toml, and left 7 `static_mut_refs` sites that fail the build once the edition is 2024; neither rewrite changed a byte of the wasm (measured).**

*Check 1: edition 2024 rejects a bare #[no_mangle] on an extern "C" export* · `compile_fail` · edition 2024 · host · lib · stderr has “unsafe attribute used without unsafe” · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn bodies_ptr() -> u32 {
    1
}
```

*Check 2: #[unsafe(no_mangle)] already compiles warning-free under edition 2021* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> u32 {
    1
}
```

*Check 3: edition 2021: the solver's static mut shapes build with static_mut_refs warnings* · `compiles` · edition 2021 · host · lib · lints: static_mut_refs · **✔ oracle pass**
```rust
static mut BODIES: [f64; 68] = [0.0; 68];
static mut COLLIDERS: [f64; 40] = [0.0; 40];

pub fn bodies_ptr() -> *mut f64 {
    unsafe { BODIES.as_mut_ptr() }
}

pub fn step() -> f64 {
    unsafe {
        let bodies = &mut BODIES;
        let colliders = &COLLIDERS;
        bodies[1] += colliders[0];
        bodies[1]
    }
}
```

*Check 4: edition 2024: the same shapes are deny-level static_mut_refs errors* · `compile_fail` · edition 2024 · host · lib · lints: static_mut_refs · **✔ oracle pass**
```rust
static mut BODIES: [f64; 68] = [0.0; 68];
static mut COLLIDERS: [f64; 40] = [0.0; 40];

pub fn bodies_ptr() -> *mut f64 {
    unsafe { BODIES.as_mut_ptr() }
}

pub fn step() -> f64 {
    unsafe {
        let bodies = &mut BODIES;
        let colliders = &COLLIDERS;
        bodies[1] += colliders[0];
        bodies[1]
    }
}
```

*Check 5: edition 2024: #![allow(static_mut_refs)] makes them build, so it is a lint* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
#![allow(static_mut_refs)]
static mut BODIES: [f64; 68] = [0.0; 68];
static mut COLLIDERS: [f64; 40] = [0.0; 40];

pub fn bodies_ptr() -> *mut f64 {
    unsafe { BODIES.as_mut_ptr() }
}

pub fn step() -> f64 {
    unsafe {
        let bodies = &mut BODIES;
        let colliders = &COLLIDERS;
        bodies[1] += colliders[0];
        bodies[1]
    }
}
```

*Check 6: edition 2024: by-value indexing of a static mut array is not flagged* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
static mut HEIGHTS: [f64; 4] = [0.0; 4];

fn main() {
    let h = unsafe {
        HEIGHTS[2] = 1.5;
        HEIGHTS[2]
    };
    println!("{h}");
}
```
Expected output: `1.5`

*Check 7: edition 2024 wasm: the &raw rewrites build warning-free and keep the ABI* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · exports memory, bodies_ptr, step, snapshot_ptr, snapshot_len · imports nothing · node calls probe() · **✔ oracle pass**
```rust
const BODY_STRIDE: usize = 17;
const MAX_BODIES: usize = 4;

static mut BODIES: [f64; MAX_BODIES * BODY_STRIDE] = [0.0; MAX_BODIES * BODY_STRIDE];

struct Solver {
    snapshot: Vec<u8>,
}

static mut SOLVER: Solver = Solver { snapshot: Vec::new() };

#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    (&raw mut BODIES).cast::<f64>()
}

#[unsafe(no_mangle)]
pub extern "C" fn step(n: u32) -> u32 {
    let bodies = unsafe { &mut *(&raw mut BODIES) };
    let n = (n as usize).min(MAX_BODIES);
    for i in 0..n {
        bodies[i * BODY_STRIDE + 4] += -8.0 / 64.0;
    }
    let solver = unsafe { &mut *(&raw mut SOLVER) };
    solver.snapshot.clear();
    for v in bodies.iter() {
        solver.snapshot.extend_from_slice(&v.to_le_bytes());
    }
    1
}

#[unsafe(no_mangle)]
pub extern "C" fn snapshot_ptr() -> *const u8 {
    unsafe { (*(&raw const SOLVER)).snapshot.as_ptr() }
}

#[unsafe(no_mangle)]
pub extern "C" fn snapshot_len() -> u32 {
    unsafe { (*(&raw const SOLVER)).snapshot.len() as u32 }
}

#[unsafe(no_mangle)]
pub extern "C" fn probe() -> u32 {
    step(2);
    snapshot_len()
}
```
Expected output: `544`

## Replace flat-buffer index math with 1.86-1.93 std APIs: as_chunks_mut, get_disjoint_mut, as_array
**Stable std now covers what the solver does by hand: `<[T]>::as_chunks_mut::<N>()` (1.88) views a flat f64 buffer as `[[f64; N]]`, `get_disjoint_mut([i, j])` (1.86) hands out two records mutably and reports overlap as an `Err`, `<[T]>::as_array::<N>()` (1.93) turns a sub-slice into `&[T; N]`, `strict_add` and the other `strict_*` methods (1.91) panic on overflow even with overflow-checks off, `f64::midpoint` (1.85) and `next_up` / `next_down` (1.86) avoid overflow and epsilon tricks, `cfg_select!` (1.95) replaces cfg-if, and `floor` / `round` / `trunc` (const since 1.90) and `mul_add` (const since 1.94) work in constants.**

*Check 1: as_chunks_mut, get_disjoint_mut, as_array, midpoint and next_up on stable* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
const BODY_STRIDE: usize = 17;
const MAX_BODIES: usize = 4;

fn main() {
    let mut bodies = [0.0f64; MAX_BODIES * BODY_STRIDE];
    // 1.88: view the flat ABI buffer as fixed-size records, no index arithmetic
    let (records, rest) = bodies.as_chunks_mut::<BODY_STRIDE>();
    assert!(rest.is_empty());
    records[2][1] = 3.5;
    // 1.86: two records mutably at once; overlapping indices are an Err, not a panic
    let [a, b] = records.get_disjoint_mut([0, 2]).unwrap();
    a[1] = b[1] - 1.0;
    let overlap = records.get_disjoint_mut([1, 1]).is_err();
    let out_of_bounds = records.get_disjoint_mut([0, 9]).is_err();
    println!("{} {} {} {}", records.len(), records[0][1], overlap, out_of_bounds);
    // 1.93: a fixed-size view of a sub-slice (the quaternion slots 6..10)
    let q: &[f64; 4] = bodies[6..10].as_array().unwrap();
    println!("{}", q.len());
    // 1.85 / 1.86: midpoint without overflow, next representable value
    println!("{:e} {:e}", f64::MAX.midpoint(f64::MAX), (f64::MAX + f64::MAX) / 2.0);
    println!("{}", 1.0f64.next_up() == 1.0 + f64::EPSILON);
}
```
Expected output: `4 2.5 true true 4 1.7976931348623157e308 inf true`

*Check 2: strict_add panics on overflow even with overflow checks off* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
use std::hint::black_box;

fn main() {
    let n: u32 = black_box(u32::MAX);
    println!("{}", n.wrapping_add(1));
    println!("{}", n.strict_add(1));
}
```
Expected output: `0`

*Check 3: f64 floor and mul_add evaluate in const items* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
// 1.90: floor/round/trunc are const; 1.94: mul_add is const
const CELL_FLOOR: f64 = 2.75f64.floor();
const FMA: f64 = 2.0f64.mul_add(3.0, 0.5);

fn main() {
    println!("{CELL_FLOOR} {FMA}");
}
```
Expected output: `2 6.5`

*Check 4: cfg_select! picks the first matching arm on stable* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
cfg_select! {
    target_family = "wasm" => { const HOST: &str = "wasm"; }
    _ => { const HOST: &str = "native"; }
}

fn main() {
    println!("{HOST}");
}
```
Expected output: `native`

## Stop sorting floats with partial_cmp().unwrap_or(Equal): 1.81+ sorts panic on a non-total order
**1.81 replaced the slice sorts with driftsort (stable) and ipnsort (unstable), which may panic when the comparison is not a total order; the old 'NaN-tolerant' idiom `sort_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal))` panics on 1.98.1 with 'user-provided comparison function does not correctly implement a total order' once a NaN is in a 64-element slice (checked), where older sorts silently returned some order.**

*Check 1: partial_cmp().unwrap_or(Equal) with a NaN panics in the 1.81+ sort* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
use std::cmp::Ordering;

fn main() {
    let mut v: Vec<f64> = (0..64).map(|i| ((i * 37) % 11) as f64).collect();
    v[10] = f64::NAN;
    v.sort_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal));
    println!("{:?}", &v[..12]);
}
```

*Check 2: total_cmp sorts the same kind of data without panicking* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![2.0f64, -0.0, f64::NAN, 0.0, -1.5];
    v.sort_by(|a, b| a.total_cmp(b));
    println!("{:?}", v);
}
```
Expected output: `[-1.5, -0.0, 0.0, 2.0, NaN]`

## Treat wasm32-unknown-unknown's six default features as byte changes, and -relaxed-simd as no ban
**On 1.98.1 wasm32-unknown-unknown enables sign-ext and mutable-globals (in codegen since 1.70), multivalue and reference-types (default since 1.82, LLVM 19) and bulk-memory and nontrapping-fptoint (since 1.87, LLVM 20); simd128 and relaxed-simd are off. None of the six is float arithmetic: `f64 as i32` saturates the same with nontrapping-fptoint and bulk-memory switched off (checked), while every change to the default set changes module bytes. `-C target-feature=-relaxed-simd` leaves the default set as it is and does not stop a function that enables relaxed-simd itself.**

*Check 1: 1.98.1 wasm32-unknown-unknown: six defaults on, simd128 and relaxed-simd off (63)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · imports nothing · node calls default_features() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn default_features() -> u32 {
    (cfg!(target_feature = "sign-ext") as u32)
        | (cfg!(target_feature = "mutable-globals") as u32) << 1
        | (cfg!(target_feature = "multivalue") as u32) << 2
        | (cfg!(target_feature = "reference-types") as u32) << 3
        | (cfg!(target_feature = "bulk-memory") as u32) << 4
        | (cfg!(target_feature = "nontrapping-fptoint") as u32) << 5
        | (cfg!(target_feature = "simd128") as u32) << 6
        | (cfg!(target_feature = "relaxed-simd") as u32) << 7
}
```
Expected output: `63`

*Check 2: -C target-feature=-relaxed-simd leaves the default set unchanged* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls default_features() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn default_features() -> u32 {
    (cfg!(target_feature = "sign-ext") as u32)
        | (cfg!(target_feature = "mutable-globals") as u32) << 1
        | (cfg!(target_feature = "multivalue") as u32) << 2
        | (cfg!(target_feature = "reference-types") as u32) << 3
        | (cfg!(target_feature = "bulk-memory") as u32) << 4
        | (cfg!(target_feature = "nontrapping-fptoint") as u32) << 5
        | (cfg!(target_feature = "simd128") as u32) << 6
        | (cfg!(target_feature = "relaxed-simd") as u32) << 7
}
```
Expected output: `63`

*Check 3: wasm32v1-none enables only mutable-globals (2)* · `runs` · edition 2024 · wasm32v1-none · cdylib · no warnings · imports nothing · node calls default_features() · **✔ oracle pass**
```rust
#![no_std]

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}

#[unsafe(no_mangle)]
pub extern "C" fn default_features() -> u32 {
    (cfg!(target_feature = "sign-ext") as u32)
        | (cfg!(target_feature = "mutable-globals") as u32) << 1
        | (cfg!(target_feature = "multivalue") as u32) << 2
        | (cfg!(target_feature = "reference-types") as u32) << 3
        | (cfg!(target_feature = "bulk-memory") as u32) << 4
        | (cfg!(target_feature = "nontrapping-fptoint") as u32) << 5
        | (cfg!(target_feature = "simd128") as u32) << 6
        | (cfg!(target_feature = "relaxed-simd") as u32) << 7
}
```
Expected output: `2`

*Check 4: f64 as i32 saturates with the default features* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls to_i32(10000000000.0) · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn to_i32(x: f64) -> i32 {
    x as i32
}

#[unsafe(no_mangle)]
pub extern "C" fn nan_to_i32() -> i32 {
    let z = core::hint::black_box(0.0f64);
    (z / z) as i32
}
```
Expected output: `2147483647`

*Check 5: ... and identically with nontrapping-fptoint and bulk-memory off* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls to_i32(10000000000.0) · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn to_i32(x: f64) -> i32 {
    x as i32
}

#[unsafe(no_mangle)]
pub extern "C" fn nan_to_i32() -> i32 {
    let z = core::hint::black_box(0.0f64);
    (z / z) as i32
}
```
Expected output: `2147483647`

*Check 6: NaN as i32 is 0 without nontrapping-fptoint too* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls nan_to_i32() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn to_i32(x: f64) -> i32 {
    x as i32
}

#[unsafe(no_mangle)]
pub extern "C" fn nan_to_i32() -> i32 {
    let z = core::hint::black_box(0.0f64);
    (z / z) as i32
}
```
Expected output: `0`

*Check 7: a #[target_feature(enable = relaxed-simd)] fn still compiles under -relaxed-simd* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · exports fused · **✔ oracle pass**
```rust
use core::arch::wasm32::{f64x2_extract_lane, f64x2_relaxed_madd, f64x2_splat};

#[target_feature(enable = "simd128,relaxed-simd")]
fn madd(a: f64, b: f64, c: f64) -> f64 {
    f64x2_extract_lane::<0>(f64x2_relaxed_madd(f64x2_splat(a), f64x2_splat(b), f64x2_splat(c)))
}

#[unsafe(no_mangle)]
pub extern "C" fn fused(a: f64, b: f64, c: f64) -> f64 {
    madd(a, b, c)
}
```

