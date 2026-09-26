# Structs, enums & pattern matching — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](types-patterns.md) · [catalog index](README.md)

## At the raw extern "C" edge, bounds-check counts and TryFrom each mode number into an enum; refuse the rest
**Keep the flat f64/u32 ABI, but turn each raw number into a checked Rust value at the top of the export — counts compared with capacity before they become indices, mode numbers decoded through TryFrom into an enum — and return the export's failure code for anything else.**

*Check 1: wasm32: decoding slot value 1.5 through the round-trip + TryFrom edge is refused (255)* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, mode_code · imports nothing · node calls mode_code(1.5) · **✔ oracle pass**
```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum SolverMode { Dynamic = 0, Kinematic = 1, Lifted = 2, Carried = 3 }

impl TryFrom<u32> for SolverMode {
    type Error = u32;
    fn try_from(v: u32) -> Result<Self, u32> {
        match v {
            0 => Ok(SolverMode::Dynamic),
            1 => Ok(SolverMode::Kinematic),
            2 => Ok(SolverMode::Lifted),
            3 => Ok(SolverMode::Carried),
            other => Err(other),
        }
    }
}

fn mode_from_slot(x: f64) -> Option<SolverMode> {
    let n = x as u32; // truncates and saturates; the round trip below refuses anything it changed
    if f64::from(n) != x {
        return None;
    }
    SolverMode::try_from(n).ok()
}

#[no_mangle]
pub extern "C" fn mode_code(x: f64) -> u32 {
    match mode_from_slot(x) {
        Some(m) => m as u32,
        None => 255,
    }
}
```
Expected output: `255`

*Check 2: wasm32: slot value 2 decodes to Lifted and leaves as its discriminant 2* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, mode_code · imports nothing · node calls mode_code(2) · **✔ oracle pass**
```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum SolverMode { Dynamic = 0, Kinematic = 1, Lifted = 2, Carried = 3 }

impl TryFrom<u32> for SolverMode {
    type Error = u32;
    fn try_from(v: u32) -> Result<Self, u32> {
        match v {
            0 => Ok(SolverMode::Dynamic),
            1 => Ok(SolverMode::Kinematic),
            2 => Ok(SolverMode::Lifted),
            3 => Ok(SolverMode::Carried),
            other => Err(other),
        }
    }
}

fn mode_from_slot(x: f64) -> Option<SolverMode> {
    let n = x as u32;
    if f64::from(n) != x {
        return None;
    }
    SolverMode::try_from(n).ok()
}

#[no_mangle]
pub extern "C" fn mode_code(x: f64) -> u32 {
    match mode_from_slot(x) {
        Some(m) => m as u32,
        None => 255,
    }
}
```
Expected output: `2`

*Check 3: host: naive try_from(x as u32) accepts 1.5, -1, NaN; the round-trip decode refuses them* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[repr(u8)]
enum SolverMode { Dynamic = 0, Kinematic = 1, Lifted = 2, Carried = 3 }

impl TryFrom<u32> for SolverMode {
    type Error = u32;
    fn try_from(v: u32) -> Result<Self, u32> {
        match v {
            0 => Ok(SolverMode::Dynamic),
            1 => Ok(SolverMode::Kinematic),
            2 => Ok(SolverMode::Lifted),
            3 => Ok(SolverMode::Carried),
            other => Err(other),
        }
    }
}

fn mode_from_slot(x: f64) -> Option<SolverMode> {
    let n = x as u32;
    if f64::from(n) != x {
        return None;
    }
    SolverMode::try_from(n).ok()
}

fn main() {
    for x in [0.0, 1.0, 2.0, 3.0, 4.0, 1.5, -1.0, f64::NAN, -0.0, 1e10] {
        println!("{x}: naive={:?} checked={:?}", SolverMode::try_from(x as u32), mode_from_slot(x));
    }
}
```
Expected output: `0: naive=Ok(Dynamic) checked=Some(Dynamic) 1: naive=Ok(Kinematic) checked=Some(Kinematic) 2: naive=Ok(Lifted) checked=Some(Lifted) 3: naive=Ok(Carried) checked=Some(Carried) 4: naive=Err(4) checked=No`

*Check 4: the capacity check is what stops body 64 from indexing past the 1,088-slot buffer (panic, 101)* · `runs` · edition 2021 · host · bin · exit code 101 · **✔ oracle pass**
```rust
const MAX_BODIES: usize = 64;
const BODY_STRIDE: usize = 17;
static BODIES: [f64; MAX_BODIES * BODY_STRIDE] = [0.0; MAX_BODIES * BODY_STRIDE];

fn read_all(n_bodies: u32) -> f64 {
    let mut sum = 0.0;
    for i in 0..n_bodies as usize {
        for k in 0..BODY_STRIDE {
            sum += BODIES[i * BODY_STRIDE + k];
        }
    }
    sum
}

fn step_checked(n_bodies: u32) -> u32 {
    if n_bodies as usize > MAX_BODIES {
        return 0;
    }
    let _ = read_all(n_bodies);
    1
}

fn main() {
    println!("checked 65 -> {}", step_checked(65));
    println!("checked 64 -> {}", step_checked(64));
    let _ = read_all(std::hint::black_box(65)); // unchecked: index 1088 is out of bounds
    println!("not reached");
}
```
Expected output: `checked 65 -> 0 checked 64 -> 1`

*Check 5: host, overflow-checks off + opt-level 3 (solver release): 1u64 << 64 is 1, masks alias* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;
fn main() {
    let last: u32 = black_box(63);
    let past: u32 = black_box(64);
    println!("{} {}", 1u64 << last, 1u64 << past);
}
```
Expected output: `9223372036854775808 1`

*Check 6: wasm32, same flags: an exported 1u64 << i returns 1 for i = 64* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls bit(64) · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn bit(i: u32) -> u64 {
    1u64 << i
}
```
Expected output: `1`

*Check 7: wasm32: usize is 32 bits, so `n_bodies as usize` from u32 cannot truncate there* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls usize_bits() · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn usize_bits() -> u32 {
    usize::BITS
}
```
Expected output: `32`

## Chain Option and Result with map, and_then, filter, ok_or_else and ?; convert between them explicitly
**Option<T> and Result<T, E> are plain enums whose combinators and `?` replace nested matches; `?` works on Option only in a function returning Option and on Result only in one returning Result, so crossing needs ok_or / ok_or_else / .ok().**

*Check 1: map / filter / and_then / ok_or_else / ? on Option and Result; is_some_and, is_none_or* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn half_even(s: &str) -> Option<u32> {
    let n: u32 = s.parse().ok()?; // Result -> Option, then ? on Option
    Some(n).filter(|n| n % 2 == 0).map(|n| n / 2)
}
fn first_field(s: &str) -> Result<u32, String> {
    let first = s.split(',').next().filter(|t| !t.is_empty()).ok_or_else(|| "empty".to_string())?;
    first.trim().parse::<u32>().map_err(|e| e.to_string())
}
fn main() {
    println!("{:?} {:?} {:?}", half_even("42"), half_even("7"), half_even("x"));
    println!("{:?} {:?}", first_field("5,6"), first_field(""));
    println!("{} {}", Some(3).is_some_and(|x| x > 2), None::<u32>.is_none_or(|x| x > 2));
    println!("{:?}", Some(2).and_then(|x| if x > 1 { Some(x * 10) } else { None }));
    println!("{:?}", Ok::<Result<u8, String>, String>(Ok(7)).flatten());
    println!("{}", u32::from(true));
}
```
Expected output: `Some(21) None None Ok(5) Err("empty") true true Some(20) Ok(7) 1`

*Check 2: ok_or evaluates its argument on the Some path; ok_or_else does not* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::cell::Cell;
fn main() {
    let v: Option<u32> = Some(1);
    let calls = Cell::new(0u32);
    let make_err = || { calls.set(calls.get() + 1); "missing" };
    let _ = v.ok_or(make_err());
    println!("after ok_or: {}", calls.get());
    let _ = v.ok_or_else(make_err);
    println!("after ok_or_else: {}", calls.get());
}
```
Expected output: `after ok_or: 1 after ok_or_else: 1`

*Check 3: ? on an Option inside a fn returning Result is E0277* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “the `?` operator can only be used on `Result`s, not `Option`s” · stderr has “use `.ok_or(...)?`” · **✔ oracle pass**
```rust
fn first_upper(s: &str) -> Result<char, String> {
    let c = s.chars().next()?;
    Ok(c.to_ascii_uppercase())
}
fn main() { println!("{:?}", first_upper("abc")); }
```

## Flatten refutable matches with let-else (1.65+); let chains need edition 2024; if-let guards work since 1.95
**let-else (1.65, every edition) binds on match and makes the else block diverge; let chains (`if let .. && let ..`, 1.88) are edition-2024 only; if-let guards on match arms (1.95) work in every edition but never count toward exhaustiveness.**

*Check 1: let-else and while let in edition 2021* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
fn double(s: &str) -> Option<u32> {
    let Ok(n) = s.parse::<u32>() else {
        return None;
    };
    Some(n * 2)
}
fn main() {
    println!("{:?} {:?}", double("21"), double("x"));
    let mut stack = vec![1, 2, 3];
    let mut order = Vec::new();
    while let Some(top) = stack.pop() {
        order.push(top);
    }
    println!("{order:?}");
}
```
Expected output: `Some(42) None [3, 2, 1]`

*Check 2: a let-else whose else block does not diverge is E0308* · `compile_fail` · edition 2021 · host · bin · errors: E0308 · stderr has “`else` clause of `let...else` does not diverge” · **✔ oracle pass**
```rust
fn parse(s: &str) -> u32 {
    let Ok(n) = s.parse::<u32>() else {
        0
    };
    n
}
fn main() { println!("{}", parse("7")); }
```

*Check 3: let chains in edition 2021 are rejected* · `compile_fail` · edition 2021 · host · bin · stderr has “let chains are only allowed in Rust 2024 or later” · **✔ oracle pass**
```rust
fn main() {
    let outer = Some(Some(1i32));
    if let Some(inner) = outer
        && let Some(n) = inner
        && n == 1
    {
        println!("chained {n}");
    }
}
```

*Check 4: let chains run in edition 2024* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let outer = Some(Some(1i32));
    if let Some(inner) = outer
        && let Some(n) = inner
        && n == 1
    {
        println!("chained {n}");
    }
}
```
Expected output: `chained 1`

*Check 5: `//` directly in a let chain is rejected* · `compile_fail` · edition 2024 · host · bin · stderr has “`||` operators are not supported in let chain conditions” · **✔ oracle pass**
```rust
fn main() {
    let a: Option<u8> = Some(1);
    let flag = true;
    if let Some(x) = a || flag {
        println!("{x:?}");
    }
}
```

*Check 6: if-let guard (with a && chain) compiles and runs in edition 2021 on 1.98.1* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
fn classify(s: Option<&str>) -> &'static str {
    match s {
        Some(t) if let Ok(n) = t.parse::<i32>() && n > 0 => "positive number",
        Some(_) => "other text",
        None => "nothing",
    }
}
fn main() {
    println!("{} / {} / {}", classify(Some("5")), classify(Some("x")), classify(None));
}
```
Expected output: `positive number / other text / nothing`

*Check 7: an if-let guard does not count toward exhaustiveness* · `compile_fail` · edition 2021 · host · bin · errors: E0004 · stderr has “match arms with guards don't count towards exhaustivity” · **✔ oracle pass**
```rust
fn f(o: Option<&str>) -> i32 {
    match o {
        Some(t) if let Ok(n) = t.parse::<i32>() => n,
        None => 0,
    }
}
fn main() { println!("{}", f(Some("3"))); }
```

## Keep patterns edition-2024 clean: no `mut`, `ref` or `&` inside an implicitly borrowing pattern
**Matching a reference with a non-reference pattern switches the default binding mode to ref / ref mut; Rust 2024 makes `mut`, `ref`, `ref mut`, `&` and `&mut` under that implicit mode hard errors, where Rust 2021 accepted them and a `mut` silently reset the binding to a by-value copy.**

*Check 1: 2021: `mut` under an implicitly borrowing pattern silently copies* · `runs` · edition 2021 · host · bin · no warnings · **✔ oracle pass**
```rust
fn main() {
    let pair = &(1u8, 2u8);
    let (mut a, b) = pair; // a: u8 (copied), b: &u8
    a += 10;
    let b: &u8 = b;
    println!("a={a} b={b} pair={:?}", pair);
}
```
Expected output: `a=11 b=2 pair=(1, 2)`

*Check 2: 2024: the same `mut` is an error* · `compile_fail` · edition 2024 · host · bin · stderr has “cannot mutably bind by value within an implicitly-borrowing pattern” · **✔ oracle pass**
```rust
fn main() {
    let pair = &(1u8, 2u8);
    let (mut a, b) = pair;
    a += 10;
    let b: &u8 = b;
    println!("a={a} b={b} pair={:?}", pair);
}
```

*Check 3: 2024: a redundant `ref` under implicit borrowing is an error* · `compile_fail` · edition 2024 · host · bin · stderr has “cannot explicitly borrow within an implicitly-borrowing pattern” · **✔ oracle pass**
```rust
fn main() {
    let [ref x] = &[()];
    let _: &() = x;
}
```

*Check 4: 2024: a `&` pattern under implicit borrowing is an error* · `compile_fail` · edition 2024 · host · bin · stderr has “cannot explicitly dereference within an implicitly-borrowing pattern” · **✔ oracle pass**
```rust
fn main() {
    let [&x, y] = &[&(), &()];
    let _: () = x;
    let _: &&() = y;
}
```

*Check 5: 2021: rust_2024_incompatible_pat reports the site before the edition move* · `runs` · edition 2021 · host · bin · lints: rust_2024_incompatible_pat · stderr has “this changes meaning in Rust 2024” · **✔ oracle pass**
```rust
#[warn(rust_2024_incompatible_pat)]
fn main() {
    let [x, mut y] = &[(), ()];
    let _: &() = x;
    y = ();
    let _: () = y;
    println!("2021 accepts it");
}
```
Expected output: `2021 accepts it`

*Check 6: 2024: fully explicit prefixes and pure ergonomics both compile* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let &[ref x, mut y] = &[1u8, 2u8];
    y += 1;
    let &[&a, ref b] = &[&3u8, &4u8];
    let (c, d) = &(5u8, 6u8); // ergonomics: c: &u8, d: &u8
    let _: (&u8, u8, u8, &&u8, &u8, &u8) = (x, y, a, b, c, d);
    println!("{x} {y} {a} {b} {c} {d}");
}
```
Expected output: `1 3 3 4 5 6`

## List every variant in a match: a `_` arm silently absorbs variants added later
**match must be exhaustive (E0004 names the missing pattern), which turns 'a variant was added' into a compile error at every match that has to decide about it; a `_` arm switches that off and hands the new variant the default.**

*Check 1: a match missing one variant is E0004 naming it* · `compile_fail` · edition 2024 · host · bin · errors: E0004 · stderr has “`Mode::Carried` not covered” · **✔ oracle pass**
```rust
#[derive(Clone, Copy)]
enum Mode { Dynamic, Kinematic, Lifted, Carried }
fn applies_gravity(m: Mode) -> bool {
    match m {
        Mode::Dynamic => true,
        Mode::Kinematic => true,
        Mode::Lifted => false,
    }
}
fn main() { let _ = applies_gravity(Mode::Carried); }
```

*Check 2: with `_`, a variant added later silently takes the default* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
#[derive(Clone, Copy, Debug)]
enum Mode { Dynamic, Kinematic, Lifted, Carried } // Carried was added last
// Written before Carried existed: "only a lifted body skips gravity".
fn applies_gravity(m: Mode) -> bool {
    match m {
        Mode::Lifted => false,
        _ => true,
    }
}
fn main() {
    for m in [Mode::Dynamic, Mode::Kinematic, Mode::Lifted, Mode::Carried] {
        print!("{:?}:{} ", m, applies_gravity(m));
    }
    println!();
}
```
Expected output: `Dynamic:true Kinematic:true Lifted:false Carried:true`

*Check 3: std's #[non_exhaustive] IntErrorKind needs `_` even with all five variants listed* · `compile_fail` · edition 2024 · host · bin · errors: E0004 · stderr has “marked as non-exhaustive, so a wildcard `_` is necessary” · **✔ oracle pass**
```rust
use std::num::IntErrorKind;
fn describe(k: &IntErrorKind) -> &'static str {
    match k {
        IntErrorKind::Empty => "empty",
        IntErrorKind::InvalidDigit => "digit",
        IntErrorKind::PosOverflow => "too big",
        IntErrorKind::NegOverflow => "too small",
        IntErrorKind::Zero => "zero",
    }
}
fn main() { println!("{}", describe("x".parse::<u8>().unwrap_err().kind())); }
```

*Check 4: non_exhaustive_omitted_patterns is not a stable lint on 1.98.1* · `compiles` · edition 2024 · host · bin · lints: unknown_lints · stderr has “the `non_exhaustive_omitted_patterns` lint is unstable” · **✔ oracle pass**
```rust
#![warn(non_exhaustive_omitted_patterns)]
fn main() {}
```

*Check 5: arms after a catch-all are unreachable and warned* · `runs` · edition 2024 · host · bin · lints: unreachable_patterns · **✔ oracle pass**
```rust
fn f(x: u8) -> u8 {
    match x {
        _ => 0,
        3 => 1,
    }
}
fn main() { println!("{}", f(3)); }
```
Expected output: `0`

*Check 6: guarded arms do not count toward exhaustiveness* · `compile_fail` · edition 2024 · host · bin · errors: E0004 · stderr has “match arms with guards don't count towards exhaustivity” · **✔ oracle pass**
```rust
fn sign(o: Option<i32>) -> i32 {
    match o {
        Some(x) if x >= 0 => 1,
        Some(x) if x < 0 => -1,
        None => 0,
    }
}
fn main() { println!("{}", sign(Some(3))); }
```

*Check 7: rapier3d-f64 0.35.3 RigidBodyType matches exhaustively with no `_` arm* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · no warnings · **✔ oracle pass**
```rust
use rapier3d_f64::dynamics::RigidBodyType;
fn solver_mode(t: RigidBodyType) -> u32 {
    match t {
        RigidBodyType::Dynamic => 0,
        RigidBodyType::KinematicPositionBased => 1,
        RigidBodyType::KinematicVelocityBased => 1,
        RigidBodyType::Fixed => 4,
    }
}
fn main() { println!("{}", solver_mode(RigidBodyType::KinematicPositionBased)); }
```
Expected output: `1`

## Model a closed set of body states as an enum with per-variant data, not a flag number or parallel vectors
**An enum value is exactly one variant and carries only that variant's data, so the states a flag number or parallel Vec<bool> / Vec<Option<_>> admit but nobody means (mode 4.0, mode 1.5, NaN, kinematic with no handle) cannot be constructed.**

*Check 1: the two slot-16 readers (lib.rs step, rapier_law.rs signature) disagree on 4.0, 1.5 and NaN* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
// Comparisons copied from si-rpg-engine e5fbcb9.
fn box_step_driven(slot: f64) -> bool { slot != 0.0 } // lib.rs step()
fn rapier_law_class(slot: f64) -> &'static str { // rapier_law.rs signature()
    if slot == 1.0 || slot == 2.0 { "driven" } else if slot == 3.0 { "carried" } else { "dynamic" }
}
fn main() {
    for x in [0.0, 1.0, 2.0, 3.0, 4.0, 1.5, f64::NAN] {
        println!("{x}: box step driven={} | rapier law {}", box_step_driven(x), rapier_law_class(x));
    }
}
```
Expected output: `0: box step driven=false / rapier law dynamic 1: box step driven=true / rapier law driven 2: box step driven=true / rapier law driven 3: box step driven=true / rapier law carried 4: box step driven=tr`

*Check 2: an enum with per-variant data, read by an exhaustive match; fieldless enum casts to u32* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
#[derive(Clone, Copy)]
enum Slot {
    Carried,
    Dynamic { handle: u32 },
    Kinematic { handle: u32, lifted: bool },
}
#[derive(Clone, Copy)]
enum Mode { Dynamic, Kinematic, Lifted, Carried }
fn describe(s: Slot) -> String {
    match s {
        Slot::Carried => "carried: not in the solver".to_string(),
        Slot::Dynamic { handle } => format!("dynamic #{handle}"),
        Slot::Kinematic { handle, lifted: true } => format!("lifted kinematic #{handle}"),
        Slot::Kinematic { handle, lifted: false } => format!("kinematic #{handle}"),
    }
}
fn main() {
    for s in [Slot::Carried, Slot::Dynamic { handle: 3 }, Slot::Kinematic { handle: 4, lifted: true }] {
        println!("{}", describe(s));
    }
    let modes = [Mode::Dynamic, Mode::Kinematic, Mode::Lifted, Mode::Carried];
    println!("{:?}", modes.map(|m| m as u32));
}
```
Expected output: `carried: not in the solver dynamic #3 lifted kinematic #4 [0, 1, 2, 3]`

*Check 3: a kinematic slot without its handle cannot be built: E0063* · `compile_fail` · edition 2024 · host · bin · errors: E0063 · stderr has “missing field `handle`” · **✔ oracle pass**
```rust
enum Slot {
    Carried,
    Dynamic { handle: u32 },
    Kinematic { handle: u32, lifted: bool },
}
fn main() {
    let _s = Slot::Kinematic { lifted: true };
}
```

*Check 4: there is no integer-to-enum cast: `1u32 as Mode` is E0605* · `compile_fail` · edition 2024 · host · bin · errors: E0605 · stderr has “non-primitive cast: `u32` as `Mode`” · **✔ oracle pass**
```rust
#[derive(Debug)]
enum Mode { Dynamic, Kinematic }
fn main() {
    let m = 1u32 as Mode;
    println!("{:?} {:?}", m, Mode::Dynamic);
}
```

## Pick named-field, tuple or unit structs by meaning; hang constructors and constants on impl blocks
**Rust has three struct kinds (named-field, tuple, unit-like); every fn in an impl block is an associated function, only those taking self are methods, and an associated const is evaluated only when something references it.**

*Check 1: named, tuple and unit structs with associated consts and fns called through the type* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
#[derive(Debug, Clone, Copy)]
struct Vec3 { x: f64, y: f64, z: f64 } // named fields
#[derive(Debug, Clone, Copy)]
struct Quanta(u32); // tuple struct
#[derive(Debug)]
struct Warm; // unit-like struct

impl Vec3 {
    const ZERO: Vec3 = Vec3 { x: 0.0, y: 0.0, z: 0.0 };
    fn new(x: f64, y: f64, z: f64) -> Self { Self { x, y, z } }
}
impl Vec3 { // a second impl block for the same type
    fn dot(self, o: Vec3) -> f64 { self.x * o.x + self.y * o.y + self.z * o.z }
}
impl Quanta {
    const PER_SECOND: u32 = 64;
    fn seconds(self) -> f64 { f64::from(self.0) / f64::from(Self::PER_SECOND) }
}
fn main() {
    let v = Vec3::new(1.0, 2.0, 3.0);
    println!("{} {}", v.dot(Vec3::ZERO), v.dot(v));
    println!("{}", Quanta(32).seconds());
    println!("{:?}", Warm);
}
```
Expected output: `0 14 0.5 Warm`

*Check 2: calling a self-less associated fn with method syntax is E0599* · `compile_fail` · edition 2024 · host · bin · errors: E0599 · stderr has “this is an associated function, not a method” · **✔ oracle pass**
```rust
struct Vec3 { x: f64, y: f64, z: f64 }
impl Vec3 {
    const ZERO: Vec3 = Vec3 { x: 0.0, y: 0.0, z: 0.0 };
    fn new(x: f64, y: f64, z: f64) -> Self { Self { x, y, z } }
}
fn main() {
    let v = Vec3::ZERO;
    let w = v.new(1.0, 2.0, 3.0);
    let _ = (w.x, w.y, w.z);
}
```

*Check 3: a false assert in an unreferenced associated const compiles (dead_code warning only)* · `runs` · edition 2024 · host · bin · lints: dead_code · stderr has “associated constant `CHECK` is never used” · **✔ oracle pass**
```rust
struct Solver;
impl Solver {
    const MAX_BODIES: usize = 64;
    const CHECK: () = assert!(Self::MAX_BODIES <= 32, "masks are 32-bit");
}
fn main() { println!("{}", Solver::MAX_BODIES); }
```
Expected output: `64`

*Check 4: the same associated const, once referenced, is evaluated and fails with E0080* · `compile_fail` · edition 2024 · host · bin · errors: E0080 · stderr has “masks are 32-bit” · **✔ oracle pass**
```rust
struct Solver;
impl Solver {
    const MAX_BODIES: usize = 64;
    const CHECK: () = assert!(Self::MAX_BODIES <= 32, "masks are 32-bit");
}
fn main() {
    let () = Solver::CHECK;
    println!("{}", Solver::MAX_BODIES);
}
```

## Treat `as` as silent truncation or saturation; convert integers with From or TryFrom so a loss is visible
**`as` never fails: narrowing keeps the low bits, float-to-int rounds toward zero and saturates (NaN -> 0), int-to-float rounds to nearest; std implements From only where no value can be lost and TryFrom returns Err instead of a wrong number.**

*Check 1: `as` truncates integers, and rounds toward zero and saturates float-to-int (NaN -> 0)* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    println!("{} {} {}", 300i32 as u8, -1i32 as u32, 1234u16 as u8);
    println!("{} {} {}", 2.9f64 as i32, -2.9f64 as i32, f64::NAN as i32);
    println!("{} {}", 1e20f64 as i32, -1e20f64 as i32);
    println!("{} {} {}", f64::INFINITY as u8, -1.0f64 as u8, 1.5f64 as u32);
}
```
Expected output: `44 4294967295 210 2 -2 0 2147483647 -2147483648 255 0 1`

*Check 2: TryFrom reports what `as` hides; From is exact; bool::try_from (1.95); u64 -> f64 rounds* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    println!("{:?} {:?}", u8::try_from(300i32), u8::try_from(200i32));
    println!("{:?}", usize::try_from(7u32));
    println!("{} {}", u32::from(7u8), f64::from(u32::MAX));
    println!("{:?} {:?} {:?}", bool::try_from(0u8), bool::try_from(1u8), bool::try_from(2u8));
    let big: u64 = (1u64 << 53) + 1;
    println!("{}", big as f64 == (1u64 << 53) as f64);
}
```
Expected output: `Err(TryFromIntError(PosOverflow)) Ok(200) Ok(7) 7 4294967295 Ok(false) Ok(true) Err(TryFromIntError(PosOverflow)) true`

*Check 3: there is no From<u32> for usize: E0277* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “the trait bound `usize: From<u32>` is not satisfied” · **✔ oracle pass**
```rust
fn main() {
    let n: u32 = 5;
    let i: usize = usize::from(n);
    println!("{i}");
}
```

*Check 4: there is no From<u64> for f64: E0277* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “the trait bound `f64: From<u64>` is not satisfied” · **✔ oracle pass**
```rust
fn main() {
    let n: u64 = 1 << 53;
    let x = f64::from(n);
    println!("{x}");
}
```

*Check 5: an integer cannot be cast to bool: E0054* · `compile_fail` · edition 2024 · host · bin · errors: E0054 · **✔ oracle pass**
```rust
fn main() {
    let b = 7u8 as bool;
    println!("{b}");
}
```

## Use slice, @, range and array patterns (and matches!) instead of index arithmetic and comparison chains
**Patterns test and bind in one step: `matches!(x, pat if guard)` yields a bool, `[head, tail @ ..]` splits a slice, `d @ 1..=9` binds the value it tested, exclusive `a..b` ranges are stable since 1.80, and an array pattern over `[f64; 17]` must name exactly 17 elements (E0527 otherwise).**

*Check 1: matches!, slice patterns with @ rest, @ bindings on ranges, exclusive ranges, exhaustive u32 bands* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
#[derive(Clone, Copy)]
enum Mode { Dynamic, Kinematic, Lifted, Carried }
fn driven(m: Mode) -> bool { matches!(m, Mode::Kinematic | Mode::Lifted) }
fn ends(s: &[u32]) -> String {
    match s {
        [] => "empty".to_string(),
        [one] => format!("one {one}"),
        [first, .., last] => format!("{first}..{last}"),
    }
}
fn split(s: &[u32]) -> String {
    match s {
        [head, tail @ ..] => format!("head {head} tail {tail:?}"),
        [] => "none".to_string(),
    }
}
fn band(n: u32) -> String {
    match n { // no `_`: the four ranges cover every u32
        0 => "zero".to_string(),
        d @ 1..=9 => format!("digit {d}"),
        10..100 => "tens".to_string(),
        big @ 100.. => format!("big {big}"),
    }
}
fn main() {
    let modes = [Mode::Dynamic, Mode::Kinematic, Mode::Lifted, Mode::Carried];
    println!("{:?}", modes.map(driven));
    println!("{} | {} | {}", ends(&[]), ends(&[7]), ends(&[1, 2, 3]));
    println!("{}", split(&[4, 5, 6]));
    println!("{} | {} | {} | {}", band(0), band(7), band(42), band(640));
    println!("{}", matches!(Some(4), Some(x) if x > 2));
}
```
Expected output: `[false, true, true, false] empty / one 7 / 1..3 head 4 tail [5, 6] zero / digit 7 / tens / big 640 true`

*Check 2: empty range patterns are E0030 (a..=b with a > b) and E0579 (a..b with a >= b)* · `compile_fail` · edition 2024 · host · bin · errors: E0030, E0579 · **✔ oracle pass**
```rust
fn f(x: u8) -> u8 { match x { 10..=0 => 1, _ => 0 } }
fn g(x: u8) -> u8 { match x { 10..10 => 1, _ => 0 } }
fn main() { println!("{} {}", f(1), g(1)); }
```

*Check 3: off-by-one range bands trip the two warn-by-default range lints* · `runs` · edition 2024 · host · bin · lints: non_contiguous_range_endpoints, overlapping_range_endpoints · **✔ oracle pass**
```rust
fn gap(x: u32) -> u8 {
    match x {
        0..10 => 1,
        11..20 => 2, // 10 falls through to `_`
        _ => 0,
    }
}
fn overlap(x: u32) -> u8 {
    match x {
        0..=10 => 1,
        10..=20 => 2, // 10 is claimed twice; the first arm wins
        _ => 0,
    }
}
fn main() { println!("{} {}", gap(10), overlap(10)); }
```
Expected output: `0 1`

*Check 4: an array pattern must name every element: 3 names over [f64; 17] is E0527* · `compile_fail` · edition 2024 · host · bin · errors: E0527 · stderr has “pattern requires 3 elements but array has 17” · **✔ oracle pass**
```rust
fn main() {
    let body = [0.0f64; 17];
    let [x, y, z] = body;
    println!("{x} {y} {z}");
}
```

*Check 5: an irrefutable 17-name array pattern replaces slot-index constants* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
const BODY_STRIDE: usize = 17;
fn body_at(i: usize) -> [f64; BODY_STRIDE] {
    let mut b = [0.0; BODY_STRIDE];
    b[9] = 1.0; // qw
    b[13] = 0.5; // hx
    b[16] = i as f64; // mode
    b
}
fn main() {
    let [x, y, z, _vx, _vy, _vz, _qx, _qy, _qz, qw, _wx, _wy, _wz, hx, _hy, _hz, mode] = body_at(2);
    println!("pos=({x},{y},{z}) qw={qw} hx={hx} mode={mode}");
}
```
Expected output: `pos=(0,0,0) qw=1 hx=0.5 mode=2`

*Check 6: f64 literal patterns: -0.0 matches the 0.0 arm, NaN only reaches `_`* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn mode(x: f64) -> &'static str {
    match x {
        0.0 => "dynamic",
        1.0 | 2.0 => "driven",
        3.0 => "carried",
        _ => "refuse",
    }
}
fn main() {
    for x in [0.0, -0.0, 1.0, 2.0, 3.0, 1.5, 4.0, f64::NAN] {
        print!("{}={} ", x, mode(x));
    }
    println!();
}
```
Expected output: `0=dynamic -0=dynamic 1=driven 2=driven 3=carried 1.5=refuse 4=refuse NaN=refuse`

*Check 7: a match on f64 without `_` is E0004* · `compile_fail` · edition 2024 · host · bin · errors: E0004 · stderr has “the matched value is of type `f64`” · **✔ oracle pass**
```rust
fn mode(x: f64) -> &'static str {
    match x {
        0.0 => "dynamic",
        1.0 | 2.0 => "driven",
        3.0 => "carried",
    }
}
fn main() { println!("{}", mode(1.0)); }
```

## Wrap units and ids in tuple-struct newtypes; keep type aliases for renames and long names
**A newtype (`struct Quanta(u32)`) is a distinct type the compiler keeps apart (E0308 on a mix-up); a type alias (`type Quanta = u32`) is only another name, so aliased values interconvert with no error.**

*Check 1: newtypes keep units apart: Seconds where Quanta is expected is E0308* · `compile_fail` · edition 2024 · host · bin · errors: E0308 · stderr has “expected `Quanta`, found `Seconds`” · **✔ oracle pass**
```rust
#[derive(Clone, Copy, Debug)]
struct Quanta(u32);
#[derive(Clone, Copy, Debug)]
struct Seconds(f64);
fn sleep_after(q: Quanta) -> Quanta { q }
fn main() {
    let dt = Seconds(1.0 / 64.0);
    let q = sleep_after(dt);
    println!("{:?}", q);
}
```

*Check 2: type aliases interconvert silently: seconds flow into a quanta parameter* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
type Quanta = f64;
type Seconds = f64;
fn sleep_after(q: Quanta) -> Quanta { q * 1.0 }
fn main() {
    let dt: Seconds = 1.0 / 64.0;
    println!("{}", sleep_after(dt));
}
```
Expected output: `0.015625`

*Check 3: rows/cols transposed: plain u32 compiles, newtypes refuse with E0308* · `compile_fail` · edition 2024 · host · bin · errors: E0308 · stderr has “expected `Rows`, found `Cols`” · **✔ oracle pass**
```rust
#[derive(Clone, Copy)]
struct Rows(u32);
#[derive(Clone, Copy)]
struct Cols(u32);
fn cells_raw(rows: u32, cols: u32) -> u32 { rows * cols }
fn cells(rows: Rows, cols: Cols) -> u32 { rows.0 * cols.0 }
fn main() {
    let (r, c) = (4u32, 8u32);
    let _ = cells_raw(c, r); // swapped, accepted
    let _ = cells(Cols(c), Rows(r)); // swapped, refused
}
```

*Check 4: an alias of a tuple struct is not its constructor: E0423* · `compile_fail` · edition 2024 · host · bin · errors: E0423 · **✔ oracle pass**
```rust
struct Quanta(u32);
type Q = Quanta;
fn main() {
    let q = Q(32);
    let _ = q.0;
}
```

*Check 5: a newtype has no inner-type operators until implemented: E0369* · `compile_fail` · edition 2024 · host · bin · errors: E0369 · **✔ oracle pass**
```rust
#[derive(Clone, Copy, Debug)]
struct Quanta(u32);
fn main() {
    let t = Quanta(1) + Quanta(2);
    println!("{:?}", t);
}
```

*Check 6: rapier3d-f64 0.35.3: deprecated alias BodyStatus is the same type as RigidBodyType* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · lints: deprecated · **✔ oracle pass**
```rust
use rapier3d_f64::dynamics::{BodyStatus, RigidBodyType};
fn main() {
    let old: BodyStatus = RigidBodyType::Fixed;
    let new: RigidBodyType = old;
    println!("{}", new == RigidBodyType::Fixed);
}
```
Expected output: `true`

