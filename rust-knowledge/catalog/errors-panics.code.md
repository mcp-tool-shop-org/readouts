# Errors, panics & arithmetic safety — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](errors-panics.md) · [catalog index](README.md)

## Derive library error enums with thiserror 2; use anyhow or `Box<dyn Error + Send + Sync>` only in binaries
**thiserror generates the `Display`, `Error::source` and `From` impls you would write by hand and stays out of your public API; anyhow gives application code one opaque error type with `.context()` layers and a cause-chain printer.**

*Check 1: thiserror derive: #[error] Display, #[from] gives From + source, ok_or refusal* · `runs` · edition 2024 · host · bin · deps: thiserror, serde_json · **✔ oracle pass**
```rust
use std::error::Error as _;

#[derive(Debug, thiserror::Error)]
enum SceneError {
    #[error("world has {n} bodies, the solver holds {max}")]
    TooManyBodies { n: u64, max: u64 },
    #[error("scene has no integer `bodies` field")]
    MissingCount,
    #[error("scene file is not valid JSON")]
    Json(#[from] serde_json::Error),
}

fn load(text: &str) -> Result<u64, SceneError> {
    let v: serde_json::Value = serde_json::from_str(text)?;
    let n = v["bodies"].as_u64().ok_or(SceneError::MissingCount)?;
    if n > 64 {
        return Err(SceneError::TooManyBodies { n, max: 64 });
    }
    Ok(n)
}

fn main() {
    println!("{:?}", load(r#"{"bodies": 3}"#).ok());
    let e = load(r#"{"bodies": 65}"#).unwrap_err();
    println!("{e} | source: {:?}", e.source().map(|s| s.to_string()));
    let e = load("{}").unwrap_err();
    println!("{e} | source: {:?}", e.source().map(|s| s.to_string()));
    let e = load("{").unwrap_err();
    println!("{e} | has source: {}", e.source().is_some());
}
```
Expected output: `Some(3) world has 65 bodies, the solver holds 64 / source: None scene has no integer `bodies` field / source: None scene file is not valid JSON / has source: true`

*Check 2: anyhow: {} prints the context, {:#} joins causes with ': ', downcast finds the cause* · `runs` · edition 2024 · host · bin · deps: anyhow · **✔ oracle pass**
```rust
use anyhow::{ensure, Context, Result};

fn body_count(s: &str) -> Result<u32> {
    let n: u32 = s.parse().context("body count is not an integer")?;
    ensure!(n <= 64, "world has {n} bodies, the solver holds 64");
    Ok(n)
}

fn main() {
    let e = body_count("x7").unwrap_err();
    println!("{e}");
    println!("{e:#}");
    println!("{}", e.downcast_ref::<std::num::ParseIntError>().is_some());
    println!("{:#}", body_count("65").unwrap_err());
}
```
Expected output: `body count is not an integer body count is not an integer: invalid digit found in string true world has 65 bodies, the solver holds 64`

*Check 3: Box<dyn Error> without Send cannot come back from thread::spawn (E0277)* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “`dyn std::error::Error` cannot be sent between threads safely” · **✔ oracle pass**
```rust
use std::error::Error;

fn work() -> Result<u32, Box<dyn Error>> {
    Err("no world loaded".into())
}

fn main() {
    let h = std::thread::spawn(|| work());
    println!("{}", h.join().unwrap().is_err());
}
```

*Check 4: Box<dyn Error + Send + Sync> takes ParseIntError via ? and a String via into, across threads* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::error::Error;

type BoxError = Box<dyn Error + Send + Sync + 'static>;

fn body_count(s: &str) -> Result<u32, BoxError> {
    let n: u32 = s.parse()?; // ParseIntError: Error + Send + Sync
    if n > 64 {
        return Err(format!("world has {n} bodies, the solver holds 64").into());
    }
    Ok(n)
}

fn main() {
    let h = std::thread::spawn(|| body_count("65"));
    println!("{}", h.join().unwrap().unwrap_err());
    println!("{}", body_count("x7").unwrap_err());
}
```
Expected output: `world has 65 bodies, the solver holds 64 invalid digit found in string`

## Give a library one error enum per failure mode and let `?` convert wrapped causes through `From`
**`?` on `Err(e)` returns `Err(From::from(e))` from the enclosing function, so an error enum plus one `From` impl per wrapped cause turns each fallible call into a single `?`; since 1.81 the `Error` trait is also in `core::error`, so the same impl serves `#![no_std]` code.**

*Check 1: `?` converts ParseIntError via From; source() chain walks; core impl serves dyn std Error* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::error::Error;
use std::fmt;
use std::num::ParseIntError;

#[derive(Debug)]
enum LoadError {
    Parse(ParseIntError),
    TooManyBodies { n: u32, max: u32 },
}

impl fmt::Display for LoadError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LoadError::Parse(_) => write!(f, "body count is not an integer"),
            LoadError::TooManyBodies { n, max } => {
                write!(f, "world has {n} bodies, the solver holds {max}")
            }
        }
    }
}

// Implemented through core::error; used below as &dyn std::error::Error: one trait.
impl core::error::Error for LoadError {
    fn source(&self) -> Option<&(dyn core::error::Error + 'static)> {
        match self {
            LoadError::Parse(e) => Some(e),
            LoadError::TooManyBodies { .. } => None,
        }
    }
}

impl From<ParseIntError> for LoadError {
    fn from(e: ParseIntError) -> Self {
        LoadError::Parse(e)
    }
}

const MAX_BODIES: u32 = 64;

fn body_count(s: &str) -> Result<u32, LoadError> {
    let n = s.parse::<u32>()?; // Err(e) leaves as Err(LoadError::from(e))
    if n > MAX_BODIES {
        return Err(LoadError::TooManyBodies { n, max: MAX_BODIES });
    }
    Ok(n)
}

fn report(e: &dyn Error) -> String {
    let mut out = e.to_string();
    let mut cur = e.source();
    while let Some(cause) = cur {
        out.push_str(" <- ");
        out.push_str(&cause.to_string());
        cur = cause.source();
    }
    out
}

fn main() {
    println!("{:?}", body_count("7").ok());
    println!("{}", report(&body_count("65").unwrap_err()));
    println!("{}", report(&body_count("x7").unwrap_err()));
}
```
Expected output: `Some(7) world has 65 bodies, the solver holds 64 body count is not an integer <- invalid digit found in string`

*Check 2: without a From impl, `?` stops with E0277 "couldn't convert the error"* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “`?` couldn't convert the error to `LoadError`” · **✔ oracle pass**
```rust
use std::num::ParseIntError;

#[derive(Debug)]
enum LoadError {
    Parse(ParseIntError),
}

fn body_count(s: &str) -> Result<u32, LoadError> {
    let n = s.parse::<u32>()?; // no From<ParseIntError> for LoadError
    Ok(n)
}

fn main() {
    let _ = body_count("7");
}
```

*Check 3: ok_or turns a missing Option value into a named refusal that carries its data* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
#[derive(Debug)]
enum Refusal {
    Carried { body: usize },
}

fn handle_of(handles: &[Option<u32>], i: usize) -> Result<u32, Refusal> {
    let h = handles[i].ok_or(Refusal::Carried { body: i })?;
    Ok(h)
}

fn main() {
    println!("{:?}", handle_of(&[Some(3), None], 0));
    println!("{:?}", handle_of(&[Some(3), None], 1));
}
```
Expected output: `Ok(3) Err(Carried { body: 1 })`

*Check 4: core::error::Error with source() works in a no_std wasm32v1-none module* · `runs` · edition 2024 · wasm32v1-none · cdylib · imports nothing · node calls chain_depth() · **✔ oracle pass**
```rust
#![no_std]
use core::fmt;

#[derive(Debug)]
struct ZeroQuaternion;

impl fmt::Display for ZeroQuaternion {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("quaternion has zero length")
    }
}

#[derive(Debug)]
struct BodyRefused(ZeroQuaternion);

impl fmt::Display for BodyRefused {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("body refused")
    }
}

impl core::error::Error for ZeroQuaternion {}

impl core::error::Error for BodyRefused {
    fn source(&self) -> Option<&(dyn core::error::Error + 'static)> {
        Some(&self.0)
    }
}

fn depth(e: &dyn core::error::Error) -> u32 {
    let mut n = 1;
    let mut cur = e.source();
    while let Some(c) = cur {
        n += 1;
        cur = c.source();
    }
    n
}

#[unsafe(no_mangle)]
pub extern "C" fn chain_depth() -> u32 {
    depth(&BodyRefused(ZeroQuaternion))
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
```
Expected output: `2`

## Guard invariants the shipped build keeps with `assert!`; `debug_assert!` vanishes without debug-assertions
**`assert!` is checked in every build and cannot be disabled; `debug_assert!` runs only when `cfg(debug_assertions)` is on, which by default means opt-level 0, and Cargo's release profile turns it off.**

*Check 1: -O: debug_assertions is off and a failing debug_assert! is skipped* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    println!("debug_assertions: {}", cfg!(debug_assertions));
    let quat_len: f64 = std::hint::black_box(0.0);
    debug_assert!(quat_len > 0.0, "quaternion should be non-zero");
    println!("kept running");
}
```
Expected output: `debug_assertions: false kept running`

*Check 2: opt-level 0 (rustc default): the same debug_assert! panics* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    println!("debug_assertions: {}", cfg!(debug_assertions));
    let quat_len: f64 = std::hint::black_box(0.0);
    debug_assert!(quat_len > 0.0, "quaternion should be non-zero");
    println!("kept running");
}
```
Expected output: `debug_assertions: true`

*Check 3: -O -C debug-assertions=on: debug_assert! fires in an optimized build* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    println!("debug_assertions: {}", cfg!(debug_assertions));
    let quat_len: f64 = std::hint::black_box(0.0);
    debug_assert!(quat_len > 0.0, "quaternion should be non-zero");
    println!("kept running");
}
```
Expected output: `debug_assertions: true`

*Check 4: -O: assert! still fires with debug-assertions off* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    println!("debug_assertions: {}", cfg!(debug_assertions));
    let quat_len: f64 = std::hint::black_box(0.0);
    assert!(quat_len > 0.0, "quaternion should be non-zero");
    println!("kept running");
}
```
Expected output: `debug_assertions: false`

## Keep panics out of `extern "C"` exports: refuse through an internal `Result` chain mapped to a `u32` status
**Since 1.81 a panic that unwinds out of an `extern "C"` function aborts the process, and `catch_unwind` in the caller cannot stop it; so an export never panics: the code behind it returns `Result<(), Refusal>` through `?`, and one `match` at the boundary produces the status code.**

*Check 1: Windows host: a panic escaping extern "C" aborts (0xC0000409) even inside catch_unwind* · `runs` · edition 2024 · host · bin · exit code 3221226505 · **✔ oracle pass**
```rust
struct Guard;

impl Drop for Guard {
    fn drop(&mut self) {
        println!("caller's drop ran");
    }
}

extern "C" fn load(n_bodies: u32) -> u32 {
    if n_bodies > 64 {
        panic!("too many bodies");
    }
    1
}

fn main() {
    let _g = Guard;
    let r = std::panic::catch_unwind(|| load(std::hint::black_box(65)));
    println!("caught: {}", r.is_err());
}
```

*Check 2: contrast: the same fn as extern "C-unwind" lets catch_unwind catch it* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
struct Guard;

impl Drop for Guard {
    fn drop(&mut self) {
        println!("caller's drop ran");
    }
}

extern "C-unwind" fn load(n_bodies: u32) -> u32 {
    if n_bodies > 64 {
        panic!("too many bodies");
    }
    1
}

fn main() {
    let _g = Guard;
    let r = std::panic::catch_unwind(|| load(std::hint::black_box(65)));
    println!("caught: {}", r.is_err());
}
```
Expected output: `caught: true caller's drop ran`

*Check 3: wasm export over a Result chain: 65 bodies -> status 0* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports solver_step · node calls solver_step(65, 1.0) · **✔ oracle pass**
```rust
#[derive(Debug, Clone, Copy, PartialEq)]
enum Refusal {
    TooManyBodies,
    BadQuaternion,
}

const MAX_BODIES: u32 = 64;

fn canon_quat(x: f64, y: f64, z: f64, w: f64) -> Option<(f64, f64, f64, f64)> {
    if x.is_nan() || y.is_nan() || z.is_nan() || w.is_nan() {
        return None;
    }
    let n = (x * x + y * y + z * z + w * w).sqrt();
    if !(n > 0.0) {
        return None;
    }
    Some((x / n, y / n, z / n, w / n))
}

fn step_inner(n_bodies: u32, qw: f64) -> Result<(), Refusal> {
    if n_bodies > MAX_BODIES {
        return Err(Refusal::TooManyBodies);
    }
    let _q = canon_quat(0.0, 0.0, 0.0, qw).ok_or(Refusal::BadQuaternion)?;
    Ok(())
}

#[no_mangle]
pub extern "C" fn solver_step(n_bodies: u32, qw: f64) -> u32 {
    match step_inner(n_bodies, qw) {
        Ok(()) => 1,
        Err(_) => 0,
    }
}
```
Expected output: `0`

*Check 4: wasm export over a Result chain: zero quaternion -> status 0* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls solver_step(3, 0.0) · **✔ oracle pass**
```rust
#[derive(Debug, Clone, Copy, PartialEq)]
enum Refusal {
    TooManyBodies,
    BadQuaternion,
}

const MAX_BODIES: u32 = 64;

fn canon_quat(x: f64, y: f64, z: f64, w: f64) -> Option<(f64, f64, f64, f64)> {
    if x.is_nan() || y.is_nan() || z.is_nan() || w.is_nan() {
        return None;
    }
    let n = (x * x + y * y + z * z + w * w).sqrt();
    if !(n > 0.0) {
        return None;
    }
    Some((x / n, y / n, z / n, w / n))
}

fn step_inner(n_bodies: u32, qw: f64) -> Result<(), Refusal> {
    if n_bodies > MAX_BODIES {
        return Err(Refusal::TooManyBodies);
    }
    let _q = canon_quat(0.0, 0.0, 0.0, qw).ok_or(Refusal::BadQuaternion)?;
    Ok(())
}

#[no_mangle]
pub extern "C" fn solver_step(n_bodies: u32, qw: f64) -> u32 {
    match step_inner(n_bodies, qw) {
        Ok(()) => 1,
        Err(_) => 0,
    }
}
```
Expected output: `0`

*Check 5: wasm export over a Result chain: valid input -> status 1* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · node calls solver_step(3, 1.0) · **✔ oracle pass**
```rust
#[derive(Debug, Clone, Copy, PartialEq)]
enum Refusal {
    TooManyBodies,
    BadQuaternion,
}

const MAX_BODIES: u32 = 64;

fn canon_quat(x: f64, y: f64, z: f64, w: f64) -> Option<(f64, f64, f64, f64)> {
    if x.is_nan() || y.is_nan() || z.is_nan() || w.is_nan() {
        return None;
    }
    let n = (x * x + y * y + z * z + w * w).sqrt();
    if !(n > 0.0) {
        return None;
    }
    Some((x / n, y / n, z / n, w / n))
}

fn step_inner(n_bodies: u32, qw: f64) -> Result<(), Refusal> {
    if n_bodies > MAX_BODIES {
        return Err(Refusal::TooManyBodies);
    }
    let _q = canon_quat(0.0, 0.0, 0.0, qw).ok_or(Refusal::BadQuaternion)?;
    Ok(())
}

#[no_mangle]
pub extern "C" fn solver_step(n_bodies: u32, qw: f64) -> u32 {
    match step_inner(n_bodies, qw) {
        Ok(()) => 1,
        Err(_) => 0,
    }
}
```
Expected output: `1`

*Check 6: natively the same chain names which refusal fired* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
#[derive(Debug, Clone, Copy, PartialEq)]
enum Refusal {
    TooManyBodies,
    BadQuaternion,
}

const MAX_BODIES: u32 = 64;

fn canon_quat(x: f64, y: f64, z: f64, w: f64) -> Option<(f64, f64, f64, f64)> {
    if x.is_nan() || y.is_nan() || z.is_nan() || w.is_nan() {
        return None;
    }
    let n = (x * x + y * y + z * z + w * w).sqrt();
    if !(n > 0.0) {
        return None;
    }
    Some((x / n, y / n, z / n, w / n))
}

fn step_inner(n_bodies: u32, qw: f64) -> Result<(), Refusal> {
    if n_bodies > MAX_BODIES {
        return Err(Refusal::TooManyBodies);
    }
    let _q = canon_quat(0.0, 0.0, 0.0, qw).ok_or(Refusal::BadQuaternion)?;
    Ok(())
}

fn main() {
    println!("{:?}", step_inner(65, 1.0));
    println!("{:?}", step_inner(3, 0.0));
    println!("{:?}", step_inner(3, 1.0));
}
```
Expected output: `Err(TooManyBodies) Err(BadQuaternion) Ok(())`

## Make refusals impossible to drop silently: `Result` is `#[must_use]`, `Option<()>` and `bool` are not
**Discarding a `Result` in an expression statement fires `unused_must_use`, but a refusal returned as `Option<()>`, `bool` or a bare integer compiles with no warning unless the function itself is `#[must_use]`.**

*Check 1: a dropped Result fires unused_must_use (warn by default)* · `compiles` · edition 2024 · host · bin · lints: unused_must_use · stderr has “unused `Result` that must be used” · **✔ oracle pass**
```rust
#[derive(Debug)]
enum Refusal {
    BadQuaternion,
}

fn rebuild_snapshot(ok: bool) -> Result<(), Refusal> {
    if ok { Ok(()) } else { Err(Refusal::BadQuaternion) }
}

fn main() {
    rebuild_snapshot(false);
}
```

*Check 2: a dropped Option<()>, bool, u32 or Result<(), Infallible> compiles with no warning at all* · `compiles` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
fn canon_quat_ok(n: f64) -> Option<()> {
    if n > 0.0 { Some(()) } else { None }
}

fn write_body(x: f64) -> bool {
    !x.is_nan()
}

fn solver_load(ok: bool) -> u32 {
    ok as u32
}

fn never_fails() -> Result<(), std::convert::Infallible> {
    Ok(())
}

fn main() {
    canon_quat_ok(0.0);   // a refusal as Option<()>, dropped: no warning
    write_body(f64::NAN); // a refusal as bool, dropped: no warning
    solver_load(false);   // a 0 status as u32, dropped: no warning
    never_fails();        // uninhabited error type: exempt from the lint
}
```

*Check 3: #[must_use = "..."] on a bool-returning fn makes the dropped status warn with the message* · `compiles` · edition 2024 · host · bin · lints: unused_must_use · stderr has “unused return value of `rebuild_snapshot` that must be used” · stderr has “a false return is a refusal and must reach the export” · **✔ oracle pass**
```rust
#[must_use = "a false return is a refusal and must reach the export"]
fn rebuild_snapshot(ok: bool) -> bool {
    ok
}

fn main() {
    rebuild_snapshot(false);
}
```

*Check 4: -D unused_must_use turns a dropped Result into a build error* · `compile_fail` · edition 2024 · host · bin · stderr has “unused `Result` that must be used” · **✔ oracle pass**
```rust
#[derive(Debug)]
struct Refusal;

fn integrate(ok: bool) -> Result<(), Refusal> {
    if ok { Ok(()) } else { Err(Refusal) }
}

fn main() {
    integrate(false);
}
```

## Return `Result<(), E: Debug>` from `main`: an `Err` is printed as `Error: {err:?}` and the process exits 1
**`main` may return any `Termination` type; for `Result<T, E>` with `E: Debug`, `Err(e)` is Debug-printed to stderr as `Error: ...` and reported as `ExitCode::FAILURE` (status 1 on this host), and `ExitCode::from(n)` sets an exact status.**

*Check 1: main returning Err: stdout keeps what was printed, the process exits with status 1* · `runs` · edition 2024 · host · bin · exit code 1 · **✔ oracle pass**
```rust
#[derive(Debug)]
enum SceneError {
    TooManyBodies { n: u32, max: u32 },
}

fn main() -> Result<(), SceneError> {
    println!("loading");
    Err(SceneError::TooManyBodies { n: 65, max: 64 })
}
```
Expected output: `loading`

*Check 2: main returning ExitCode::from(2) exits with exactly 2* · `runs` · edition 2024 · host · bin · exit code 2 · **✔ oracle pass**
```rust
use std::process::ExitCode;

fn main() -> ExitCode {
    let refused = true;
    if refused {
        println!("input refused");
        return ExitCode::from(2);
    }
    ExitCode::SUCCESS
}
```
Expected output: `input refused`

*Check 3: an error type without Debug cannot be returned from main (E0277)* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “doesn't implement `Debug`” · **✔ oracle pass**
```rust
struct Opaque;

fn main() -> Result<(), Opaque> {
    Ok(())
}
```

## Say the overflow intent in the call: `checked_`, `wrapping_`, `saturating_`, `overflowing_`, `strict_` (1.91+)
**The method families behave the same under every profile: `checked_*` returns `None`, `wrapping_*` wraps, `saturating_*` clamps, `overflowing_*` returns `(value, overflowed)`, and `strict_*` (stable since 1.91.0) always panics on overflow, whether or not overflow checks are enabled.**

*Check 1: checked/wrapping/saturating/overflowing at the edge, shl by 64, Wrapping<u8>* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::num::Wrapping;

fn main() {
    let x: u8 = 250;
    println!("{:?} {} {} {:?}", x.checked_add(10), x.wrapping_add(10), x.saturating_add(10), x.overflowing_add(10));
    println!("{:?} {} {}", 1u64.checked_shl(64), 1u64.wrapping_shl(64), i32::MIN.wrapping_abs());
    println!("{:?} {} {}", i32::MIN.checked_div(-1), 7u32.saturating_sub(9), (Wrapping(x) + Wrapping(10)).0);
}
```
Expected output: `None 4 255 (4, true) None 1 -2147483648 None 0 4`

*Check 2: strict_add panics even with -C overflow-checks=off (stable 1.91)* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
use std::hint::black_box;

fn main() {
    let n: u32 = black_box(u32::MAX);
    println!("before");
    let total = n.strict_add(1);
    println!("{total}");
}
```
Expected output: `before`

*Check 3: an FNV-style mix written with wrapping_ ops: this value with overflow checks on* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;

fn mix_u64(h: u64, x: u64) -> u64 {
    h.wrapping_mul(0x100000001b3).wrapping_add(x)
}

fn main() {
    let mut h = black_box(0xcbf29ce484222325u64);
    for v in [1.5f64, -0.0, 64.0] {
        h = mix_u64(h, v.to_bits());
    }
    println!("{h:016x}");
}
```
Expected output: `c05512186c0f2fb7`

*Check 4: the same wrapping_ mix gives the identical value with overflow checks off* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;

fn mix_u64(h: u64, x: u64) -> u64 {
    h.wrapping_mul(0x100000001b3).wrapping_add(x)
}

fn main() {
    let mut h = black_box(0xcbf29ce484222325u64);
    for v in [1.5f64, -0.0, 64.0] {
        h = mix_u64(h, v.to_bits());
    }
    println!("{h:016x}");
}
```
Expected output: `c05512186c0f2fb7`

*Check 5: the mix written with plain * and + panics with overflow checks on* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
use std::hint::black_box;

fn mix_u64(h: u64, x: u64) -> u64 {
    h * 0x100000001b3 + x
}

fn main() {
    let h = mix_u64(black_box(0xcbf29ce484222325u64), 1.5f64.to_bits());
    println!("{h:016x}");
}
```

## Under `overflow-checks = false`, `+ - *`, negation, `abs` and shifts wrap; `/ %` and indexing still panic
**With overflow checks off (Cargo's release default and the solver's profile) arithmetic overflow wraps in two's complement and an oversized shift amount is masked, but division by zero, `MIN / -1`, `MIN % -1` and out-of-bounds indexing panic in every build.**

*Check 1: -C overflow-checks=off: u8 add, shift by 64, i32::MIN.abs() and -MIN all wrap* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;

fn main() {
    let a: u8 = black_box(255);
    let shift: u32 = black_box(64);
    let m: i32 = black_box(i32::MIN);
    println!("{} {} {} {}", a + 1, 1u64 << shift, m.abs(), -m);
}
```
Expected output: `0 1 -2147483648 -2147483648`

*Check 2: -O alone (debug-assertions off, so overflow checks off) wraps the same way* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;

fn main() {
    let a: u8 = black_box(255);
    let shift: u32 = black_box(64);
    let m: i32 = black_box(i32::MIN);
    println!("{} {} {} {}", a + 1, 1u64 << shift, m.abs(), -m);
}
```
Expected output: `0 1 -2147483648 -2147483648`

*Check 3: -C overflow-checks=on: the same add, shift by 64, abs(MIN) and -MIN each panic* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;
use std::panic::catch_unwind;

fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let a: u8 = black_box(255);
    let shift: u32 = black_box(64);
    let m: i32 = black_box(i32::MIN);
    println!(
        "{} {} {} {}",
        catch_unwind(|| a + 1).is_err(),
        catch_unwind(|| 1u64 << shift).is_err(),
        catch_unwind(|| m.abs()).is_err(),
        catch_unwind(|| -m).is_err()
    );
}
```
Expected output: `true true true true`

*Check 4: checks off + -O: MIN / -1, MIN % -1, / 0 and a bad index still panic while u8 add wraps* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::hint::black_box;
use std::panic::catch_unwind;

fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let m: i32 = black_box(i32::MIN);
    let neg1: i32 = black_box(-1);
    let zero: u32 = black_box(0);
    let bodies = [0.0f64; 4];
    let i: usize = black_box(4);
    println!("MIN / -1 panics: {}", catch_unwind(|| m / neg1).is_err());
    println!("MIN % -1 panics: {}", catch_unwind(|| m % neg1).is_err());
    println!("7 / 0 panics: {}", catch_unwind(|| black_box(7u32) / zero).is_err());
    println!("bodies[4] of 4 panics: {}", catch_unwind(|| bodies[i]).is_err());
    println!("255u8 + 1 = {}", black_box(255u8) + 1);
}
```
Expected output: `MIN / -1 panics: true MIN % -1 panics: true 7 / 0 panics: true bodies[4] of 4 panics: true 255u8 + 1 = 0`

*Check 5: constant overflow is a deny-by-default arithmetic_overflow error even with checks off* · `compile_fail` · edition 2024 · host · bin · lints: arithmetic_overflow · stderr has “this arithmetic operation will overflow” · **✔ oracle pass**
```rust
fn main() {
    let x: u8 = 255 + 1;
    let bit = 1u64 << 64;
    println!("{x} {bit}");
}
```

*Check 6: constant MIN / -1 and a constant bad index are deny-by-default unconditional_panic errors* · `compile_fail` · edition 2024 · host · bin · lints: unconditional_panic · stderr has “this operation will panic at runtime” · **✔ oracle pass**
```rust
fn main() {
    let q = i32::MIN / -1;
    let bodies = [0.0f64; 4];
    let x = bodies[4];
    println!("{q} {x}");
}
```

*Check 7: a const assertion refuses MAX_BODIES = 65 at compile time (E0080)* · `compile_fail` · edition 2021 · host · bin · errors: E0080 · stderr has “body masks are u64: one bit per body” · **✔ oracle pass**
```rust
const MAX_BODIES: usize = 65;

// `driven` and `carried` are u64 masks with one bit per body.
const _: () = assert!(MAX_BODIES <= 64, "body masks are u64: one bit per body");

fn main() {}
```

## Use `expect` with a 'should' message only for invariants the compiler can't see; return `Result` for input
**A panic is for a broken invariant or contract (a bug) and a `Result` for an anticipated failure; `expect("... should ...")` records why a value is guaranteed, while bare `unwrap()` panics with no reason attached.**

*Check 1: expect's precondition message is the panic payload (exit 101 under unwind)* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    std::panic::set_hook(Box::new(|info| {
        println!("hook: {}", info.payload_as_str().unwrap_or("<non-string payload>"));
    }));
    let plan_bodies: Vec<usize> = vec![0, 2];
    let body = 1;
    let plan = plan_bodies
        .iter()
        .position(|&index| index == body)
        .expect("a plan should exist for every kinematic body with a handle");
    println!("plan {plan}");
}
```
Expected output: `hook: a plan should exist for every kinematic body with a handle`

*Check 2: Option::unwrap panics with a generic message that names no reason* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    std::panic::set_hook(Box::new(|info| {
        println!("hook: {}", info.payload_as_str().unwrap_or("<non-string payload>"));
    }));
    let plan_bodies: Vec<usize> = vec![0, 2];
    let plan = plan_bodies.iter().position(|&index| index == 1).unwrap();
    println!("plan {plan}");
}
```
Expected output: `hook: called `Option::unwrap()` on a `None` value`

*Check 3: Result::expect appends the error's Debug to the message* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    std::panic::set_hook(Box::new(|info| {
        println!("hook: {}", info.payload_as_str().unwrap_or("<non-string payload>"));
    }));
    let text = std::hint::black_box("7x");
    let n: u32 = text.parse().expect("the scene's body count should be an integer");
    println!("{n}");
}
```
Expected output: `hook: the scene's body count should be an integer: ParseIntError { kind: InvalidDigit }`

## Know what `panic = "abort"` changes: the hook still runs, then no unwinding, no `Drop`, nothing to catch
**Under the abort strategy a panic calls the panic hook and then ends the process: destructors do not run and `catch_unwind`, which catches only unwinding panics, gets nothing; `wasm32-unknown-unknown` compiles with `-C panic=abort` by default and its abort is a trap.**

*Check 1: unwind (host default): hook runs, Drop runs during unwinding, catch_unwind returns Err* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
struct Guard;

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop ran");
    }
}

fn main() {
    std::panic::set_hook(Box::new(|_| println!("hook ran")));
    let r = std::panic::catch_unwind(|| {
        let _g = Guard;
        panic!("boom");
    });
    println!("caught: {}", r.is_err());
}
```
Expected output: `hook ran drop ran caught: true`

*Check 2: -C panic=abort, Windows host: hook runs, then no Drop, no catch; status 0xC0000409* · `runs` · edition 2024 · host · bin · exit code 3221226505 · **✔ oracle pass**
```rust
struct Guard;

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop ran");
    }
}

fn main() {
    std::panic::set_hook(Box::new(|_| println!("hook ran")));
    let r = std::panic::catch_unwind(|| {
        let _g = Guard;
        panic!("boom");
    });
    println!("caught: {}", r.is_err());
}
```
Expected output: `hook ran`

*Check 3: cfg!(panic = "abort") is true under -C panic=abort* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let strategy = if cfg!(panic = "abort") { "abort" } else { "unwind" };
    println!("{strategy}");
}
```
Expected output: `abort`

*Check 4: wasm32-unknown-unknown is abort with no -C panic flag; the module imports nothing* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, strategy_is_abort, get · imports nothing · node calls strategy_is_abort() · **✔ oracle pass**
```rust
static mut BODIES: [f64; 4] = [0.0; 4];

#[no_mangle]
pub extern "C" fn strategy_is_abort() -> u32 {
    cfg!(panic = "abort") as u32
}

#[no_mangle]
pub extern "C" fn get(i: u32) -> f64 {
    let bodies = unsafe { &*core::ptr::addr_of!(BODIES) };
    bodies[i as usize] // an out-of-range i panics; under abort that is a trap
}
```
Expected output: `1`

*Check 5: catch_unwind requires UnwindSafe: capturing &mut is E0277* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “may not be safely transferred across an unwind boundary” · **✔ oracle pass**
```rust
fn main() {
    let mut steps = 0u32;
    let r = std::panic::catch_unwind(|| {
        steps += 1;
    });
    println!("{} {}", r.is_ok(), steps);
}
```

*Check 6: AssertUnwindSafe is the explicit opt-in that compiles* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::panic::{catch_unwind, AssertUnwindSafe};

fn main() {
    let mut steps = 0u32;
    let r = catch_unwind(AssertUnwindSafe(|| {
        steps += 1;
    }));
    println!("{} {}", r.is_ok(), steps);
}
```
Expected output: `true 1`

