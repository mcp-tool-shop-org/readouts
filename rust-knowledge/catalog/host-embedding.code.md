# Embedding the law in hosts — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](host-embedding.md) · [catalog index](README.md)

## Accept a new host only when its T1 trace equals node's in 16-hex-digit IEEE bits, never in decimals
**solver/build.mjs under node is the reference binding: a Godot or Unreal host proves it runs the same law by printing the T1 trace for the same seed and log and passing harness/first-difference.js against node's trace, which writes every body field as its IEEE bit pattern.**

*Check 1: Six-decimal output hides a 1-ulp and a signed-zero difference that the 16-hex-digit tokens keep* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
// The T1 trace token: sixteen lowercase hex digits of the IEEE bits, high word first.
fn token(x: f64) -> String {
    format!("{:016x}", x.to_bits())
}

fn main() {
    let a = std::hint::black_box(0.1) + std::hint::black_box(0.2);
    let b = 0.3;
    println!("{:.6} {:.6}", a, b);
    println!("{} {}", token(a), token(b));
    println!("{} {}", token(0.0), token(-0.0));
    let back = f64::from_bits(u64::from_str_radix("3fd3333333333334", 16).unwrap());
    println!("parsed token equals a: {}", back.to_bits() == a.to_bits());
}
```
Expected output: `0.300000 0.300000 3fd3333333333334 3fd3333333333333 0000000000000000 8000000000000000 parsed token equals a: true`

## Bind the law natively in Godot with gdext 0.5.5: a cdylib entry point, api-4-N no newer than the running Godot
**Option B in Godot compiles the law into a GDExtension with godot-rust (crate godot 0.5.5, 2026-08-09, Rust 1.94+, MPL-2.0): a cdylib per platform that any Godot at or above the API version it was built against (4.2 or later) can load.**

*Check 1: An f64 pose narrowed to an f32 real and widened back is not the committed value* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
// A pose the law committed, and what an f32 `real` (Godot's default) keeps of it.
fn main() {
    let committed: f64 = std::hint::black_box(0.1) + std::hint::black_box(0.2);
    let shown: f32 = committed as f32;
    let widened: f64 = shown as f64;
    println!("committed {:016x}", committed.to_bits());
    println!("widened   {:016x}", widened.to_bits());
    println!("round trip exact: {}", committed == widened);
}
```
Expected output: `committed 3fd3333333333334 widened   3fd3333340000000 round trip exact: false`

## Choose the runtime per platform by tier: Cranelift needs executable pages at run time, interpreters do not
**Four runtimes can execute the law's core module natively, at different maturity: Wasmtime 49.0.1 (Cranelift or Winch compilers, Pulley interpreter), Wasmer 7.4.2, WAMR 2.4.5 and wasm3 0.9.0. Because the law uses no SIMD, even the SIMD-less wasm3 can load it.**

*Check 1: Under the 1.98.1 wasm32 defaults a no-SIMD guard compiles, runs and the module imports nothing* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · imports nothing · node calls scale(1.5, 2.0) · **✔ oracle pass**
```rust
// Fails the build if the target would let the compiler emit v128 or relaxed-SIMD instructions,
// which a SIMD-less runtime (wasm3 lists fixed-width SIMD as N/A) cannot load.
#[cfg(target_feature = "simd128")]
compile_error!("simd128 is enabled: the module may contain v128 instructions");
#[cfg(target_feature = "relaxed-simd")]
compile_error!("relaxed-simd is enabled");

#[unsafe(no_mangle)]
pub extern "C" fn scale(x: f64, k: f64) -> f64 {
    x * k
}
```
Expected output: `3`

*Check 2: The same guard refuses a build with simd128 switched on* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “simd128 is enabled” · **✔ oracle pass**
```rust
// Fails the build if the target would let the compiler emit v128 or relaxed-SIMD instructions,
// which a SIMD-less runtime (wasm3 lists fixed-width SIMD as N/A) cannot load.
#[cfg(target_feature = "simd128")]
compile_error!("simd128 is enabled: the module may contain v128 instructions");
#[cfg(target_feature = "relaxed-simd")]
compile_error!("relaxed-simd is enabled");

#[unsafe(no_mangle)]
pub extern "C" fn scale(x: f64, k: f64) -> f64 {
    x * k
}
```

## Drive one law instance per world from one thread; collect Rapier events in a Sync buffer the host drains
**The law holds one Rapier world in static mut SOLVER and silently rebuilds it when the call signature changes, so a host needs one module instance per world, called from one thread; host callbacks cannot go into Rapier (its EventHandler must be Sync), so events belong in a law-owned Sync buffer drained after each step; and the buffer traffic is small, 22,528 bytes per quantum at the engine's maxima.**

*Check 1: A host sink holding Rc<RefCell<..>> cannot be Rapier's EventHandler: E0277 via MaybeSync* · `compile_fail` · edition 2024 · host · lib · deps: rapier3d_f64 · errors: E0277 · stderr has “cannot be shared between threads safely” · stderr has “MaybeSync” · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;
use std::cell::RefCell;
use std::rc::Rc;

// A host-side sink shaped like a single-threaded engine object handle.
pub struct HostSink {
    pub started: Rc<RefCell<Vec<bool>>>,
}

impl EventHandler for HostSink {
    fn handle_collision_event(&self, _b: &RigidBodySet, _c: &ColliderSet, e: CollisionEvent, _p: Option<&ContactPair>) {
        self.started.borrow_mut().push(e.started());
    }
    fn handle_contact_force_event(&self, _dt: f64, _b: &RigidBodySet, _c: &ColliderSet, _p: &ContactPair, _m: f64) {}
}
```

*Check 2: A law-owned Mutex<Vec> handler, drained after each step, yields the Started event at quantum 20* · `runs` · edition 2024 · host · bin · deps: rapier3d_f64 · no warnings · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;
use std::sync::Mutex;

// The law owns a Sync buffer; Rapier writes into it during the step, the host drains it after.
struct LawEvents {
    started: Mutex<Vec<bool>>,
}

impl EventHandler for LawEvents {
    fn handle_collision_event(&self, _b: &RigidBodySet, _c: &ColliderSet, e: CollisionEvent, _p: Option<&ContactPair>) {
        self.started.lock().unwrap().push(e.started());
    }
    fn handle_contact_force_event(&self, _dt: f64, _b: &RigidBodySet, _c: &ColliderSet, _p: &ContactPair, _m: f64) {}
}

fn main() {
    let mut world = PhysicsWorld::new();
    world.integration_parameters.dt = 1.0 / 64.0;
    world.insert(RigidBodyBuilder::fixed(), ColliderBuilder::cuboid(5.0, 0.5, 5.0));
    world.insert(
        RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 1.5, 0.0)),
        ColliderBuilder::ball(0.5).active_events(ActiveEvents::COLLISION_EVENTS),
    );
    let events = LawEvents { started: Mutex::new(Vec::new()) };
    let mut drained: Vec<(u32, bool)> = Vec::new();
    for q in 0..64u32 {
        world.step_with_events(&(), &events);
        // Host side, between quanta: take what the step produced.
        for s in events.started.lock().unwrap().drain(..) {
            drained.push((q, s));
        }
    }
    println!("drained (quantum, started): {:?}", drained);
}
```
Expected output: `drained (quantum, started): [(20, true)]`

*Check 3: Buffer traffic at the engine's maxima: 22,528 bytes per quantum, 1,441,792 bytes/s at 64 Hz* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::mem::size_of;

const MAX_BODIES: usize = 64;
const BODY_STRIDE: usize = 17;
const MAX_COLLIDERS: usize = 64;
const COLLIDER_STRIDE: usize = 10;
const MAX_HEIGHTS: usize = 256;
const READ_BACK_FIELDS: usize = 13; // x y z vx vy vz qx qy qz qw wx wy wz

fn main() {
    let bodies = size_of::<[f64; MAX_BODIES * BODY_STRIDE]>();
    let colliders = size_of::<[f64; MAX_COLLIDERS * COLLIDER_STRIDE]>();
    let heights = size_of::<[f64; MAX_HEIGHTS]>();
    let read_back = size_of::<[f64; MAX_BODIES * READ_BACK_FIELDS]>();
    let per_quantum = bodies + colliders + heights + read_back;
    println!("in: bodies {bodies} colliders {colliders} heights {heights}; out: {read_back}");
    println!("per quantum {per_quantum} B; at 64 quanta/s {} B/s", per_quantum * 64);
}
```
Expected output: `in: bodies 8704 colliders 5120 heights 2048; out: 6656 per quantum 22528 B; at 64 quanta/s 1441792 B/s`

*Check 4: A #[repr(C)] Pod record of 17 f64 casts to 136 bytes per body with slots in stride order* · `runs` · edition 2024 · host · bin · deps: bytemuck · no warnings · **✔ oracle pass**
```rust
use bytemuck::{Pod, Zeroable};
use std::mem::{align_of, offset_of, size_of};

// One body record exactly as the law's buffer holds it: 17 f64, stride 17.
#[repr(C)]
#[derive(Clone, Copy, Pod, Zeroable)]
struct BodyIn {
    pos: [f64; 3],
    vel: [f64; 3],
    quat: [f64; 4],
    ang: [f64; 3],
    half: [f64; 3],
    mode: f64,
}

const _: () = assert!(size_of::<BodyIn>() == 17 * 8);

fn main() {
    let mut bodies = [BodyIn::zeroed(); 2];
    bodies[1].pos = [1.0, 2.0, 3.0];
    bodies[1].mode = 1.0;
    // The byte slice a wasmtime Memory::write takes.
    let bytes: &[u8] = bytemuck::cast_slice(&bodies);
    println!("size {} align {} half@{} mode@{}", size_of::<BodyIn>(), align_of::<BodyIn>(), offset_of!(BodyIn, half), offset_of!(BodyIn, mode));
    println!("bytes for 2 bodies {}", bytes.len());
    let back: &[f64] = bytemuck::cast_slice(bytes);
    println!("body 1 slot 0 = {}, slot 16 = {}", back[17], back[17 + 16]);
}
```
Expected output: `size 136 align 8 half@104 mode@128 bytes for 2 bodies 272 body 1 slot 0 = 1, slot 16 = 1`

*Check 5: derive(Pod) refuses a record with tail padding (E0080)* · `compile_fail` · edition 2024 · host · lib · deps: bytemuck · errors: E0080 · stderr has “derive(Pod) was applied to a type with padding” · **✔ oracle pass**
```rust
use bytemuck::{Pod, Zeroable};

// A u32 flag after the 16 floats leaves 4 bytes of tail padding.
#[repr(C)]
#[derive(Clone, Copy, Pod, Zeroable)]
pub struct BodyIn {
    pub fields: [f64; 16],
    pub mode: u32,
}
```

## Host the law as the one pinned .wasm in an embedded runtime; it imports nothing, so no WASI is linked
**Option A ships the Linux-built si_solver.wasm itself to every host and runs it in an embedded runtime: one artifact and one digest, and because the module imports nothing the host supplies no WASI and no host functions, only an executor for core wasm.**

*Check 1: A law-shaped cdylib (static f64 buffers, Vec snapshot, release flags) imports nothing, exports memory* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · exports memory, bodies_ptr, solver_step, snapshot_ptr, snapshot_len · imports nothing · node calls solver_step(3) · **✔ oracle pass**
```rust
// The law's shape: static f64 buffers, a heap-allocated snapshot, raw extern "C" exports.
const MAX_BODIES: usize = 64;
const BODY_STRIDE: usize = 17;
const DT: f64 = 1.0 / 64.0;

static mut BODIES: [f64; MAX_BODIES * BODY_STRIDE] = [0.0; MAX_BODIES * BODY_STRIDE];
static mut SNAPSHOT: Vec<u8> = Vec::new();

#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    (&raw mut BODIES).cast::<f64>()
}

#[unsafe(no_mangle)]
pub extern "C" fn solver_step(n_bodies: u32) -> u32 {
    let n = n_bodies as usize;
    if n > MAX_BODIES {
        return 0;
    }
    let bodies = unsafe { &mut *(&raw mut BODIES) };
    let snap = unsafe { &mut *(&raw mut SNAPSHOT) };
    snap.clear();
    for i in 0..n {
        let at = i * BODY_STRIDE;
        bodies[at + 4] = bodies[at + 4] + -8.0 * DT;
        bodies[at + 1] = bodies[at + 1] + bodies[at + 4] * DT;
        snap.extend_from_slice(&bodies[at + 1].to_bits().to_le_bytes());
    }
    1
}

#[unsafe(no_mangle)]
pub extern "C" fn snapshot_ptr() -> *const u8 {
    unsafe { (*(&raw const SNAPSHOT)).as_ptr() }
}

#[unsafe(no_mangle)]
pub extern "C" fn snapshot_len() -> u32 {
    unsafe { (*(&raw const SNAPSHOT)).len() as u32 }
}
```
Expected output: `1`

## Link the law into Unreal 5 as one Rust staticlib or cdylib behind a cbindgen header in an External module
**Unreal Engine 5.8 documents third-party code as a module with Type = ModuleType.External that adds include paths and a static or dynamic library; a Rust crate meets it with crate-type staticlib (one .lib/.a carrying the crate, its dependencies and std) or cdylib, extern "C" functions over #[repr(C)] records, and a header generated by cbindgen 0.29.4.**

*Check 1: A pointer-plus-count C API over a #[repr(C)] record builds as a staticlib with no warnings* · `compiles` · edition 2024 · host · staticlib · no warnings · **✔ oracle pass**
```rust
// A C ABI for a native host (Unreal's External module links the .lib/.a or loads the .dll).
use core::ptr::{addr_of, addr_of_mut, copy_nonoverlapping};

pub const MAX_BODIES: u32 = 64;

/// One body record, laid out exactly like the law's stride-17 f64 buffer.
#[repr(C)]
#[derive(Clone, Copy)]
pub struct BodyIn {
    pub pos: [f64; 3],
    pub vel: [f64; 3],
    pub quat: [f64; 4],
    pub ang: [f64; 3],
    pub half: [f64; 3],
    pub mode: f64,
}

const ZERO: BodyIn = BodyIn { pos: [0.0; 3], vel: [0.0; 3], quat: [0.0; 4], ang: [0.0; 3], half: [0.0; 3], mode: 0.0 };
static mut BODIES: [BodyIn; MAX_BODIES as usize] = [ZERO; MAX_BODIES as usize];

/// Copies `n` records in; returns 0 when `n` is out of range or `src` is null.
///
/// # Safety
/// `src` must point to `n` readable, initialized `BodyIn` records.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn law_write_bodies(src: *const BodyIn, n: u32) -> u32 {
    if n > MAX_BODIES || src.is_null() {
        return 0;
    }
    // SAFETY: the caller guarantees `n` records at `src`; BODIES holds MAX_BODIES.
    unsafe { copy_nonoverlapping(src, addr_of_mut!(BODIES).cast::<BodyIn>(), n as usize) };
    1
}

/// Copies `n` records out; returns 0 when `n` is out of range or `dst` is null.
///
/// # Safety
/// `dst` must point to room for `n` `BodyIn` records.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn law_read_bodies(dst: *mut BodyIn, n: u32) -> u32 {
    if n > MAX_BODIES || dst.is_null() {
        return 0;
    }
    // SAFETY: as above, in the other direction.
    unsafe { copy_nonoverlapping(addr_of!(BODIES).cast::<BodyIn>(), dst, n as usize) };
    1
}
```

*Check 2: The same source builds as a cdylib with no warnings* · `compiles` · edition 2024 · host · cdylib · no warnings · **✔ oracle pass**
```rust
// A C ABI for a native host (Unreal's External module links the .lib/.a or loads the .dll).
use core::ptr::{addr_of, addr_of_mut, copy_nonoverlapping};

pub const MAX_BODIES: u32 = 64;

/// One body record, laid out exactly like the law's stride-17 f64 buffer.
#[repr(C)]
#[derive(Clone, Copy)]
pub struct BodyIn {
    pub pos: [f64; 3],
    pub vel: [f64; 3],
    pub quat: [f64; 4],
    pub ang: [f64; 3],
    pub half: [f64; 3],
    pub mode: f64,
}

const ZERO: BodyIn = BodyIn { pos: [0.0; 3], vel: [0.0; 3], quat: [0.0; 4], ang: [0.0; 3], half: [0.0; 3], mode: 0.0 };
static mut BODIES: [BodyIn; MAX_BODIES as usize] = [ZERO; MAX_BODIES as usize];

/// Copies `n` records in; returns 0 when `n` is out of range or `src` is null.
///
/// # Safety
/// `src` must point to `n` readable, initialized `BodyIn` records.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn law_write_bodies(src: *const BodyIn, n: u32) -> u32 {
    if n > MAX_BODIES || src.is_null() {
        return 0;
    }
    // SAFETY: the caller guarantees `n` records at `src`; BODIES holds MAX_BODIES.
    unsafe { copy_nonoverlapping(src, addr_of_mut!(BODIES).cast::<BodyIn>(), n as usize) };
    1
}

/// Copies `n` records out; returns 0 when `n` is out of range or `dst` is null.
///
/// # Safety
/// `dst` must point to room for `n` `BodyIn` records.
#[unsafe(no_mangle)]
pub unsafe extern "C" fn law_read_bodies(dst: *mut BodyIn, n: u32) -> u32 {
    if n > MAX_BODIES || dst.is_null() {
        return 0;
    }
    // SAFETY: as above, in the other direction.
    unsafe { copy_nonoverlapping(addr_of!(BODIES).cast::<BodyIn>(), dst, n as usize) };
    1
}
```

*Check 3: On the host the 17-f64 BodyIn is 136 bytes, align 8, mode at 128 (encoded 136008128)* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::mem::{align_of, offset_of, size_of};

#[repr(C)]
pub struct BodyIn {
    pub pos: [f64; 3],
    pub vel: [f64; 3],
    pub quat: [f64; 4],
    pub ang: [f64; 3],
    pub half: [f64; 3],
    pub mode: f64,
}

// size * 1_000_000 + align * 1_000 + offset of `mode`, the same number the wasm build returns.
fn layout_code() -> i64 {
    (size_of::<BodyIn>() * 1_000_000 + align_of::<BodyIn>() * 1_000 + offset_of!(BodyIn, mode)) as i64
}

fn main() {
    println!("{}", layout_code());
}
```
Expected output: `136008128`

*Check 4: In wasm32 the same BodyIn reports the same size, align and offset (136008128)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · node calls layout_code() · **✔ oracle pass**
```rust
use core::mem::{align_of, offset_of, size_of};

#[repr(C)]
pub struct BodyIn {
    pub pos: [f64; 3],
    pub vel: [f64; 3],
    pub quat: [f64; 4],
    pub ang: [f64; 3],
    pub half: [f64; 3],
    pub mode: f64,
}

// size * 1_000_000 + align * 1_000 + offset of `mode`, the same number the host build prints.
#[unsafe(no_mangle)]
pub extern "C" fn layout_code() -> i64 {
    (size_of::<BodyIn>() * 1_000_000 + align_of::<BodyIn>() * 1_000 + offset_of!(BodyIn, mode)) as i64
}
```
Expected output: `136008128`

## Treat a native law build as a second artifact: basic ops match the wasm, std math inside dependencies may not
**Option B recompiles the law for each host target. A step built only from add/sub/mul/div/sqrt, like lib.rs's, gives the wasm build's bits natively, but enhanced-determinism does not reroute inherent std calls inside dependencies: with std on, parry 0.30.2 diagonalizes summed, convex-hull and trimesh inertia through glamx 0.3.1, whose non-diagonal branch calls acos and cos.**

*Check 1: An add/mul/div/sqrt box step natively at opt-level 3: the FNV of its bits over 640 quanta* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
const DT: f64 = 1.0 / 64.0;
const G: f64 = -8.0;
const MAX_SPEED: f64 = 2.0;

// One quantum of a box over a floor: add, sub, mul, div and sqrt only.
fn quantum(s: &mut [f64; 6], hy: f64, floor_top: f64) {
    s[4] = s[4] + G * DT;
    s[0] = s[0] + s[3] * DT;
    s[1] = s[1] + s[4] * DT;
    s[2] = s[2] + s[5] * DT;
    let pen = floor_top - (s[1] - hy);
    if pen > 0.0 {
        s[1] = s[1] + pen;
        s[4] = 0.0 - s[4] * 0.5;
    }
    let speed2 = s[3] * s[3] + s[4] * s[4] + s[5] * s[5];
    if speed2 > MAX_SPEED * MAX_SPEED {
        let scale = MAX_SPEED / speed2.sqrt();
        s[3] = s[3] * scale;
        s[4] = s[4] * scale;
        s[5] = s[5] * scale;
    }
}

// FNV-1a over the IEEE bits of every field after every quantum.
fn law_bits(n: u32) -> i64 {
    let mut s = [0.1, 3.0, -0.2, 0.7, 0.0, 0.3];
    let mut acc: u64 = 0xcbf29ce484222325;
    let mut q = 0;
    while q < n {
        quantum(&mut s, 0.5, 0.0);
        for v in s {
            acc = (acc ^ v.to_bits()).wrapping_mul(0x100000001b3);
        }
        q += 1;
    }
    acc as i64
}

fn main() {
    println!("{}", law_bits(std::hint::black_box(640)));
}
```
Expected output: `4769065195358558711`

*Check 2: The same step as a wasm export (release flags) returns the same FNV of bits through wasm_call* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · imports nothing · node calls law_trace(640) · **✔ oracle pass**
```rust
const DT: f64 = 1.0 / 64.0;
const G: f64 = -8.0;
const MAX_SPEED: f64 = 2.0;

// One quantum of a box over a floor: add, sub, mul, div and sqrt only.
fn quantum(s: &mut [f64; 6], hy: f64, floor_top: f64) {
    s[4] = s[4] + G * DT;
    s[0] = s[0] + s[3] * DT;
    s[1] = s[1] + s[4] * DT;
    s[2] = s[2] + s[5] * DT;
    let pen = floor_top - (s[1] - hy);
    if pen > 0.0 {
        s[1] = s[1] + pen;
        s[4] = 0.0 - s[4] * 0.5;
    }
    let speed2 = s[3] * s[3] + s[4] * s[4] + s[5] * s[5];
    if speed2 > MAX_SPEED * MAX_SPEED {
        let scale = MAX_SPEED / speed2.sqrt();
        s[3] = s[3] * scale;
        s[4] = s[4] * scale;
        s[5] = s[5] * scale;
    }
}

// FNV-1a over the IEEE bits of every field after every quantum.
fn law_bits(n: u32) -> i64 {
    let mut s = [0.1, 3.0, -0.2, 0.7, 0.0, 0.3];
    let mut acc: u64 = 0xcbf29ce484222325;
    let mut q = 0;
    while q < n {
        quantum(&mut s, 0.5, 0.0);
        for v in s {
            acc = (acc ^ v.to_bits()).wrapping_mul(0x100000001b3);
        }
        q += 1;
    }
    acc as i64
}

#[unsafe(no_mangle)]
pub extern "C" fn law_trace(n: u32) -> i64 {
    law_bits(n)
}
```
Expected output: `4769065195358558711`

*Check 3: parry 0.30.2: one box's inertia is diagonal (no eigen trig); two boxes, one turned, are not* · `runs` · edition 2024 · host · bin · deps: parry3d_f64 · no warnings · **✔ oracle pass**
```rust
use parry3d_f64::mass_properties::MassProperties;
use parry3d_f64::math::{Pose, Rotation, Vector};

// p1 of glamx's symmetric 3x3 eigen solver: zero means the diagonal branch (no acos/cos).
fn off_diagonal(mp: &MassProperties) -> f64 {
    let m = mp.reconstruct_inertia_matrix();
    m.y_axis.x * m.y_axis.x + m.z_axis.x * m.z_axis.x + m.z_axis.y * m.z_axis.y
}

fn main() {
    let half = Vector::new(0.5, 0.25, 0.1);
    let one_box = MassProperties::from_cuboid(1.0, half);
    let turned = Pose::from_parts(Vector::new(0.3, 0.0, 0.0), Rotation::from_rotation_z(0.5));
    let two_boxes = one_box + one_box.transform_by(&turned);
    println!("single box off-diagonal is zero: {}", off_diagonal(&one_box) == 0.0);
    println!("two boxes off-diagonal is zero: {}", off_diagonal(&two_boxes) == 0.0);
}
```
Expected output: `single box off-diagonal is zero: true two boxes off-diagonal is zero: false`

