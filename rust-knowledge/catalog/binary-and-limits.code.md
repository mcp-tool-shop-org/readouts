# Binary lint, CCD and controller limits (T3/T4) — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](binary-and-limits.md) · [catalog index](README.md)

## Allow ~1,200 quanta for a walker started 0.1 inside the floor: Rapier depenetrates only on a zero desired move
**move_shape runs its depenetration pass only for a zero desired translation, and the engine always passes gravity, so a walker started 0.1 inside the floor rises only by the 1e-4 normal nudge per quantum and stands after about 1,200 quanta.**

*Check 1: A walker 0.1 inside the floor rises 1e-4 per quantum and stands by quantum 1280* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// The engine's walker loop (solver/src/rapier_law.rs integrate()) for one box
// walker, natively: controller constants, gravity, grounded -> vy = 0,
// set_next_kinematic_translation, world.step(). Prints course outcomes.
use rapier3d_f64::control::{CharacterAutostep, CharacterLength, KinematicCharacterController};
use rapier3d_f64::pipeline::CollisionPipeline;
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;
const G: f64 = -8.0;
const H: f64 = 0.25;

fn controller() -> KinematicCharacterController {
    KinematicCharacterController {
        up: Vector::new(0.0, 1.0, 0.0),
        offset: CharacterLength::Absolute(0.01),
        slide: true,
        autostep: Some(CharacterAutostep {
            max_height: CharacterLength::Absolute(0.3),
            min_width: CharacterLength::Absolute(0.2),
            include_dynamic_bodies: false,
        }),
        max_slope_climb_angle: core::f64::consts::FRAC_PI_4,
        min_slope_slide_angle: 50.0 * core::f64::consts::PI / 180.0,
        snap_to_ground: Some(CharacterLength::Absolute(0.2)),
        normal_nudge_factor: 1.0e-4,
    }
}

// (min, max, quaternion xyzw) boxes -> fixed cuboids, like build_world.
fn world_with(boxes: &[([f64; 3], [f64; 3], [f64; 4])], start: Vector) -> (PhysicsWorld, RigidBodyHandle) {
    let mut world = PhysicsWorld::new();
    world.gravity = Vector::new(0.0, G, 0.0);
    world.integration_parameters.dt = DT;
    world.integration_parameters.contact_clustering = false;
    world.integration_parameters.warmstart_coefficient = 1.0;
    for (min, max, q) in boxes {
        let c = Vector::new((min[0] + max[0]) * 0.5, (min[1] + max[1]) * 0.5, (min[2] + max[2]) * 0.5);
        let mut body = RigidBodyBuilder::fixed().translation(c).build();
        body.set_rotation(Rotation::from_xyzw(q[0], q[1], q[2], q[3]), false);
        let co = ColliderBuilder::cuboid((max[0] - min[0]) * 0.5, (max[1] - min[1]) * 0.5, (max[2] - min[2]) * 0.5)
            .restitution(0.0).friction(0.8).build();
        world.insert(body, co);
    }
    let walker = RigidBodyBuilder::kinematic_position_based().translation(start).lock_rotations()
        .additional_mass(1.0).can_sleep(false).ccd_enabled(false).build();
    let (h, _) = world.insert(walker, ColliderBuilder::cuboid(H, H, H).restitution(0.0).friction(0.8).build());
    // warm_broadphase
    let prediction = world.integration_parameters.prediction_distance();
    let mut pipeline = CollisionPipeline::new();
    pipeline.step(prediction, &mut world.islands, &mut world.broad_phase, &mut world.narrow_phase,
        &mut world.bodies, &mut world.colliders, &(), &());
    for (_, body) in world.bodies.iter_mut() {
        if !body.is_fixed() {
            body.wake_up(true);
        }
    }
    (world, h)
}

// One quantum: returns (new vy, grounded).
fn quantum(world: &mut PhysicsWorld, h: RigidBodyHandle, vx: f64, vy: f64) -> (f64, bool) {
    let mut vy = vy + G * DT;
    let desired = Vector::new(vx, vy, 0.0) * DT;
    let shape = SharedShape::cuboid(H, H, H);
    let pos = *world.bodies[h].position();
    let movement = {
        let q = world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(), &world.bodies,
            &world.colliders, QueryFilter::new().exclude_rigid_body(h));
        controller().move_shape(DT, &q, &*shape, &pos, desired, |_| {})
    };
    if movement.grounded {
        vy = 0.0;
    }
    let t = pos.translation + movement.translation;
    world.bodies[h].set_next_kinematic_translation(t);
    world.step();
    (vy, movement.grounded)
}

const FLOOR: ([f64; 3], [f64; 3], [f64; 4]) = ([0.0, -1.0, -3.0], [40.0, 0.0, 3.0], [0.0, 0.0, 0.0, 1.0]);

fn step_case(height: f64, vx: f64) -> (f64, f64) {
    let riser = ([11.0, 0.0, -3.0], [14.0, height, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let (mut w, h) = world_with(&[FLOOR, riser], Vector::new(10.0, H + 0.01, 0.0));
    let mut vy = 0.0;
    for _ in 0..((2.5 / vx) * 64.0) as usize {
        vy = quantum(&mut w, h, vx, vy).0;
    }
    let p = w.bodies[h].translation();
    (p.y - H, p.x)
}

fn slope_case(deg: f64, vx: f64, quanta: usize) -> f64 {
    let th = deg.to_radians();
    let (l, t) = (1.4, 0.35);
    let n = [-th.sin(), th.cos()];
    let cx = 11.0 + l * th.cos() - t * n[0];
    let cy = l * th.sin() - t * n[1];
    let ramp = ([cx - l, cy - t, -0.5], [cx + l, cy + t, 0.5], [0.0, 0.0, (th / 2.0).sin(), (th / 2.0).cos()]);
    let (mut w, h) = world_with(&[FLOOR, ramp], Vector::new(10.0, H + 0.01, 0.0));
    let mut vy = 0.0;
    let mut max_gain: f64 = 0.0;
    for _ in 0..quanta {
        vy = quantum(&mut w, h, vx, vy).0;
        max_gain = max_gain.max(w.bodies[h].translation().y - (H + 0.01));
    }
    max_gain
}

// Returns the longest run of consecutive ungrounded quanta after the edge.
fn drop_case(d: f64, vx: f64) -> u32 {
    let upper = ([0.0, -1.0, -3.0], [11.0, 0.0, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let lower = ([11.0, -1.0 - d, -3.0], [40.0, -d, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let (mut w, h) = world_with(&[upper, lower], Vector::new(10.5, H + 0.01, 0.0));
    let (mut vy, mut run, mut longest) = (0.0, 0u32, 0u32);
    for _ in 0..((1.5 / vx) * 64.0) as usize {
        let (nvy, grounded) = quantum(&mut w, h, vx, vy);
        vy = nvy;
        if grounded { run = 0 } else { run += 1; longest = longest.max(run) }
    }
    longest
}

fn main() {
    // Centre 0.1 lower than resting height: the box starts 0.1 inside the floor.
    for vx in [0.0, 0.4] {
        let (mut w, h) = world_with(&[FLOOR], Vector::new(10.0, H - 0.1, 0.0));
        let mut vy = 0.0;
        let mut feet = Vec::new();
        for q in 1..=1280 {
            vy = quantum(&mut w, h, vx, vy).0;
            if q == 64 || q == 640 || q == 1280 {
                feet.push(format!("q{} {:.4}", q, w.bodies[h].translation().y - H));
            }
        }
        println!("start 0.1 inside, vx {}: feet {}", vx, feet.join(", "));
    }
}
```
Expected output: `start 0.1 inside, vx 0: feet q64 -0.0936, q640 -0.0360, q1280 0.0101 start 0.1 inside, vx 0.4: feet q64 -0.0936, q640 -0.0360, q1280 0.0101`

## Don't rely on -C target-feature=-relaxed-simd: a #[target_feature] fn or a relaxed intrinsic still emits
**Under -C target-feature=-relaxed-simd a #[target_feature(enable = "relaxed-simd")] function and a plain call to core::arch::wasm32::f32x4_relaxed_madd both compile without unsafe and emit f32x4.relaxed_madd (fd 85 02).**

*Check 1: A plain call to f32x4_relaxed_madd compiles under -relaxed-simd and runs: 2*3+1* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · no warnings · exports memory, madd · imports nothing · node calls madd(2, 3, 1) · **✔ oracle pass**
```rust
// Built with -C target-feature=-relaxed-simd. The intrinsic carries its own
// #[target_feature(enable = "relaxed-simd")], so the crate flag does not stop it.
use core::arch::wasm32::*;

#[no_mangle]
pub extern "C" fn madd(a: f32, b: f32, c: f32) -> f32 {
    let v = f32x4_relaxed_madd(f32x4_splat(a), f32x4_splat(b), f32x4_splat(c));
    f32x4_extract_lane::<0>(v)
}
```
Expected output: `7`

*Check 2: A #[target_feature(enable=relaxed-simd)] fn compiles under -relaxed-simd, called without unsafe* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · no warnings · exports memory, madd · imports nothing · node calls madd(2, 3, 1) · **✔ oracle pass**
```rust
// Built with -C target-feature=-relaxed-simd. A function-level enable wins,
// and on Wasm a safe #[target_feature] fn is callable from safe code.
use core::arch::wasm32::*;

#[target_feature(enable = "relaxed-simd")]
fn inner(a: f32, b: f32, c: f32) -> f32 {
    let v = f32x4_relaxed_madd(f32x4_splat(a), f32x4_splat(b), f32x4_splat(c));
    f32x4_extract_lane::<0>(v)
}

#[no_mangle]
pub extern "C" fn madd(a: f32, b: f32, c: f32) -> f32 {
    inner(a, b, c)
}
```
Expected output: `7`

## Expect Rapier 0.35.3 to stop T4's fast box at a fixed slab with ccd_enabled(false); max_ccd_substeps 0 tunnels
**In rapier3d-f64 0.35.3 every dynamic body moving more than half its thinnest half-extent per step is swept against fixed colliders even with ccd_enabled(false); ccd_enabled(true) only adds kinematic and dynamic targets.**

*Check 1: A 0.05 box at 20 u/s vs a 0.02 fixed slab, 7 start phases, three CCD settings* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// T4 pin 2 as the engine builds it: dt 1/64, g -8, clustering off, warm-start 1,
// a dynamic box of half-extent 0.05 launched at 20 u/s at a fixed slab of
// half-thickness 0.02 (restitution 0, friction 0.8, sleep after 32 quanta).
use rapier3d_f64::prelude::*;

fn run(y0: f64, ccd_enabled: bool, max_ccd_substeps: usize) -> (f64, f64) {
    let mut world = PhysicsWorld::new();
    world.gravity = Vector::new(0.0, -8.0, 0.0);
    world.integration_parameters.dt = 1.0 / 64.0;
    world.integration_parameters.contact_clustering = false;
    world.integration_parameters.warmstart_coefficient = 1.0;
    world.integration_parameters.max_ccd_substeps = max_ccd_substeps;
    let slab = RigidBodyBuilder::fixed().translation(Vector::new(0.0, 0.0, 0.0)).build();
    let slab_co = ColliderBuilder::cuboid(2.0, 0.02, 2.0).restitution(0.0).friction(0.8).build();
    world.insert(slab, slab_co);
    let mut body = RigidBodyBuilder::dynamic()
        .translation(Vector::new(0.0, y0, 0.0))
        .linvel(Vector::new(0.0, -20.0, 0.0))
        .can_sleep(true)
        .ccd_enabled(ccd_enabled)
        .build();
    body.activation_mut().time_until_sleep = 32.0 / 64.0;
    let co = ColliderBuilder::cuboid(0.05, 0.05, 0.05).restitution(0.0).friction(0.8).build();
    let (h, _) = world.insert(body, co);
    let mut min_y = f64::MAX;
    for _ in 0..64 {
        world.step();
        min_y = min_y.min(world.bodies[h].translation().y);
    }
    (world.bodies[h].translation().y, min_y)
}

fn main() {
    let starts = [1.0, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3];
    let side = |(y, _): (f64, f64)| if y > 0.0 { "near" } else { "FAR" };
    let row = |ccd: bool, sub: usize| starts.iter().map(|&y0| side(run(y0, ccd, sub))).collect::<Vec<_>>().join(" ");
    println!("CCD off world-wide (max_ccd_substeps 0): {}", row(false, 0));
    println!("engine today (ccd_enabled false, substeps 1): {}", row(false, 1));
    println!("T4 pin 2 (ccd_enabled true, substeps 1): {}", row(true, 1));
}
```
Expected output: `CCD off world-wide (max_ccd_substeps 0): near FAR FAR FAR FAR FAR near engine today (ccd_enabled false, substeps 1): near near near near near near near T4 pin 2 (ccd_enabled true, substeps 1): near ne`

## Fix wasm32 memory with -C link-arg=--no-growable-memory or equal, page-aligned --initial-memory/--max-memory
**On rustc 1.98.1 (rust-lld, LLD 22.1.8) two stable link args make a wasm32 module's maximum equal its initial size; memory.grow of one page then returns -1 on every host.**

*Check 1: Without a maximum, memory.grow(1) succeeds and returns the old size, 16 pages* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, grow · imports nothing · node calls grow() · **✔ oracle pass**
```rust
// One page asked of a memory whose maximum equals its initial size.
#[no_mangle]
pub extern "C" fn grow() -> i32 {
    core::arch::wasm32::memory_grow(0, 1) as i32
}

#[no_mangle]
pub extern "C" fn pages() -> i32 {
    core::arch::wasm32::memory_size(0) as i32
}
```
Expected output: `16`

*Check 2: --no-growable-memory: memory.grow(1) returns -1* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, grow · imports nothing · node calls grow() · **✔ oracle pass**
```rust
// One page asked of a memory whose maximum equals its initial size.
#[no_mangle]
pub extern "C" fn grow() -> i32 {
    core::arch::wasm32::memory_grow(0, 1) as i32
}

#[no_mangle]
pub extern "C" fn pages() -> i32 {
    core::arch::wasm32::memory_size(0) as i32
}
```
Expected output: `-1`

*Check 3: Equal --initial-memory/--max-memory of 4194304 bytes give 64 pages* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, pages · imports nothing · node calls pages() · **✔ oracle pass**
```rust
// One page asked of a memory whose maximum equals its initial size.
#[no_mangle]
pub extern "C" fn grow() -> i32 {
    core::arch::wasm32::memory_grow(0, 1) as i32
}

#[no_mangle]
pub extern "C" fn pages() -> i32 {
    core::arch::wasm32::memory_size(0) as i32
}
```
Expected output: `64`

*Check 4: Equal --initial-memory/--max-memory: memory.grow(1) returns -1* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, grow · imports nothing · node calls grow() · **✔ oracle pass**
```rust
// One page asked of a memory whose maximum equals its initial size.
#[no_mangle]
pub extern "C" fn grow() -> i32 {
    core::arch::wasm32::memory_grow(0, 1) as i32
}

#[no_mangle]
pub extern "C" fn pages() -> i32 {
    core::arch::wasm32::memory_size(0) as i32
}
```
Expected output: `-1`

*Check 5: An initial memory that is not a multiple of 65536 fails to link* · `compile_fail` · edition 2021 · wasm32-unknown-unknown · cdylib · stderr has “initial memory must be aligned to the page size (65536 bytes)” · **✔ oracle pass**
```rust
// One page asked of a memory whose maximum equals its initial size.
#[no_mangle]
pub extern "C" fn grow() -> i32 {
    core::arch::wasm32::memory_grow(0, 1) as i32
}

#[no_mangle]
pub extern "C" fn pages() -> i32 {
    core::arch::wasm32::memory_size(0) as i32
}
```

*Check 6: An initial memory below the static footprint fails to link* · `compile_fail` · edition 2021 · wasm32-unknown-unknown · cdylib · stderr has “initial memory too small” · **✔ oracle pass**
```rust
// One page asked of a memory whose maximum equals its initial size.
#[no_mangle]
pub extern "C" fn grow() -> i32 {
    core::arch::wasm32::memory_grow(0, 1) as i32
}

#[no_mangle]
pub extern "C" fn pages() -> i32 {
    core::arch::wasm32::memory_size(0) as i32
}
```

## Keep T4 slope and ledge cases off the controller's comparisons: >= at 45 degrees, nudge creep, speed-set snap
**is_wall is angle >= max_slope_climb_angle and is_nonslip_slope is angle <= min_slope_slide_angle; snap needs a grounded start and translation.up <= 0; the 1e-4 normal nudge lifts a walker blocked on a 46 degree slope by about 6e-5 per quantum; the snap-or-fall threshold moves with speed (0.2105, 0.2097, 0.2058 at 0.4, 1, 2 u/s).**

*Check 1: 44 deg climbs, 45 creeps, 46 is refused but gains 0.018 then 0.077 over 320 and 1280 quanta* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// The engine's walker loop (solver/src/rapier_law.rs integrate()) for one box
// walker, natively: controller constants, gravity, grounded -> vy = 0,
// set_next_kinematic_translation, world.step(). Prints course outcomes.
use rapier3d_f64::control::{CharacterAutostep, CharacterLength, KinematicCharacterController};
use rapier3d_f64::pipeline::CollisionPipeline;
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;
const G: f64 = -8.0;
const H: f64 = 0.25;

fn controller() -> KinematicCharacterController {
    KinematicCharacterController {
        up: Vector::new(0.0, 1.0, 0.0),
        offset: CharacterLength::Absolute(0.01),
        slide: true,
        autostep: Some(CharacterAutostep {
            max_height: CharacterLength::Absolute(0.3),
            min_width: CharacterLength::Absolute(0.2),
            include_dynamic_bodies: false,
        }),
        max_slope_climb_angle: core::f64::consts::FRAC_PI_4,
        min_slope_slide_angle: 50.0 * core::f64::consts::PI / 180.0,
        snap_to_ground: Some(CharacterLength::Absolute(0.2)),
        normal_nudge_factor: 1.0e-4,
    }
}

// (min, max, quaternion xyzw) boxes -> fixed cuboids, like build_world.
fn world_with(boxes: &[([f64; 3], [f64; 3], [f64; 4])], start: Vector) -> (PhysicsWorld, RigidBodyHandle) {
    let mut world = PhysicsWorld::new();
    world.gravity = Vector::new(0.0, G, 0.0);
    world.integration_parameters.dt = DT;
    world.integration_parameters.contact_clustering = false;
    world.integration_parameters.warmstart_coefficient = 1.0;
    for (min, max, q) in boxes {
        let c = Vector::new((min[0] + max[0]) * 0.5, (min[1] + max[1]) * 0.5, (min[2] + max[2]) * 0.5);
        let mut body = RigidBodyBuilder::fixed().translation(c).build();
        body.set_rotation(Rotation::from_xyzw(q[0], q[1], q[2], q[3]), false);
        let co = ColliderBuilder::cuboid((max[0] - min[0]) * 0.5, (max[1] - min[1]) * 0.5, (max[2] - min[2]) * 0.5)
            .restitution(0.0).friction(0.8).build();
        world.insert(body, co);
    }
    let walker = RigidBodyBuilder::kinematic_position_based().translation(start).lock_rotations()
        .additional_mass(1.0).can_sleep(false).ccd_enabled(false).build();
    let (h, _) = world.insert(walker, ColliderBuilder::cuboid(H, H, H).restitution(0.0).friction(0.8).build());
    // warm_broadphase
    let prediction = world.integration_parameters.prediction_distance();
    let mut pipeline = CollisionPipeline::new();
    pipeline.step(prediction, &mut world.islands, &mut world.broad_phase, &mut world.narrow_phase,
        &mut world.bodies, &mut world.colliders, &(), &());
    for (_, body) in world.bodies.iter_mut() {
        if !body.is_fixed() {
            body.wake_up(true);
        }
    }
    (world, h)
}

// One quantum: returns (new vy, grounded).
fn quantum(world: &mut PhysicsWorld, h: RigidBodyHandle, vx: f64, vy: f64) -> (f64, bool) {
    let mut vy = vy + G * DT;
    let desired = Vector::new(vx, vy, 0.0) * DT;
    let shape = SharedShape::cuboid(H, H, H);
    let pos = *world.bodies[h].position();
    let movement = {
        let q = world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(), &world.bodies,
            &world.colliders, QueryFilter::new().exclude_rigid_body(h));
        controller().move_shape(DT, &q, &*shape, &pos, desired, |_| {})
    };
    if movement.grounded {
        vy = 0.0;
    }
    let t = pos.translation + movement.translation;
    world.bodies[h].set_next_kinematic_translation(t);
    world.step();
    (vy, movement.grounded)
}

const FLOOR: ([f64; 3], [f64; 3], [f64; 4]) = ([0.0, -1.0, -3.0], [40.0, 0.0, 3.0], [0.0, 0.0, 0.0, 1.0]);

fn step_case(height: f64, vx: f64) -> (f64, f64) {
    let riser = ([11.0, 0.0, -3.0], [14.0, height, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let (mut w, h) = world_with(&[FLOOR, riser], Vector::new(10.0, H + 0.01, 0.0));
    let mut vy = 0.0;
    for _ in 0..((2.5 / vx) * 64.0) as usize {
        vy = quantum(&mut w, h, vx, vy).0;
    }
    let p = w.bodies[h].translation();
    (p.y - H, p.x)
}

fn slope_case(deg: f64, vx: f64, quanta: usize) -> f64 {
    let th = deg.to_radians();
    let (l, t) = (1.4, 0.35);
    let n = [-th.sin(), th.cos()];
    let cx = 11.0 + l * th.cos() - t * n[0];
    let cy = l * th.sin() - t * n[1];
    let ramp = ([cx - l, cy - t, -0.5], [cx + l, cy + t, 0.5], [0.0, 0.0, (th / 2.0).sin(), (th / 2.0).cos()]);
    let (mut w, h) = world_with(&[FLOOR, ramp], Vector::new(10.0, H + 0.01, 0.0));
    let mut vy = 0.0;
    let mut max_gain: f64 = 0.0;
    for _ in 0..quanta {
        vy = quantum(&mut w, h, vx, vy).0;
        max_gain = max_gain.max(w.bodies[h].translation().y - (H + 0.01));
    }
    max_gain
}

// Returns the longest run of consecutive ungrounded quanta after the edge.
fn drop_case(d: f64, vx: f64) -> u32 {
    let upper = ([0.0, -1.0, -3.0], [11.0, 0.0, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let lower = ([11.0, -1.0 - d, -3.0], [40.0, -d, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let (mut w, h) = world_with(&[upper, lower], Vector::new(10.5, H + 0.01, 0.0));
    let (mut vy, mut run, mut longest) = (0.0, 0u32, 0u32);
    for _ in 0..((1.5 / vx) * 64.0) as usize {
        let (nvy, grounded) = quantum(&mut w, h, vx, vy);
        vy = nvy;
        if grounded { run = 0 } else { run += 1; longest = longest.max(run) }
    }
    longest
}

fn main() {
    println!("44 deg, 320 quanta at 2 u/s: max gain {:.3}", slope_case(44.0, 2.0, 320));
    println!("45 deg, 320 quanta at 2 u/s: max gain {:.3}", slope_case(45.0, 2.0, 320));
    println!("46 deg, 320 quanta at 2 u/s: max gain {:.3}", slope_case(46.0, 2.0, 320));
    println!("46 deg, 1280 quanta at 2 u/s: max gain {:.3}", slope_case(46.0, 2.0, 1280));
}
```
Expected output: `44 deg, 320 quanta at 2 u/s: max gain 1.954 45 deg, 320 quanta at 2 u/s: max gain 0.341 46 deg, 320 quanta at 2 u/s: max gain 0.018 46 deg, 1280 quanta at 2 u/s: max gain 0.077`

*Check 2: Ledge drops: 0.21 snaps at 0.4 u/s but falls 12 quanta at 2 u/s; 0.22 falls at both* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// The engine's walker loop (solver/src/rapier_law.rs integrate()) for one box
// walker, natively: controller constants, gravity, grounded -> vy = 0,
// set_next_kinematic_translation, world.step(). Prints course outcomes.
use rapier3d_f64::control::{CharacterAutostep, CharacterLength, KinematicCharacterController};
use rapier3d_f64::pipeline::CollisionPipeline;
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;
const G: f64 = -8.0;
const H: f64 = 0.25;

fn controller() -> KinematicCharacterController {
    KinematicCharacterController {
        up: Vector::new(0.0, 1.0, 0.0),
        offset: CharacterLength::Absolute(0.01),
        slide: true,
        autostep: Some(CharacterAutostep {
            max_height: CharacterLength::Absolute(0.3),
            min_width: CharacterLength::Absolute(0.2),
            include_dynamic_bodies: false,
        }),
        max_slope_climb_angle: core::f64::consts::FRAC_PI_4,
        min_slope_slide_angle: 50.0 * core::f64::consts::PI / 180.0,
        snap_to_ground: Some(CharacterLength::Absolute(0.2)),
        normal_nudge_factor: 1.0e-4,
    }
}

// (min, max, quaternion xyzw) boxes -> fixed cuboids, like build_world.
fn world_with(boxes: &[([f64; 3], [f64; 3], [f64; 4])], start: Vector) -> (PhysicsWorld, RigidBodyHandle) {
    let mut world = PhysicsWorld::new();
    world.gravity = Vector::new(0.0, G, 0.0);
    world.integration_parameters.dt = DT;
    world.integration_parameters.contact_clustering = false;
    world.integration_parameters.warmstart_coefficient = 1.0;
    for (min, max, q) in boxes {
        let c = Vector::new((min[0] + max[0]) * 0.5, (min[1] + max[1]) * 0.5, (min[2] + max[2]) * 0.5);
        let mut body = RigidBodyBuilder::fixed().translation(c).build();
        body.set_rotation(Rotation::from_xyzw(q[0], q[1], q[2], q[3]), false);
        let co = ColliderBuilder::cuboid((max[0] - min[0]) * 0.5, (max[1] - min[1]) * 0.5, (max[2] - min[2]) * 0.5)
            .restitution(0.0).friction(0.8).build();
        world.insert(body, co);
    }
    let walker = RigidBodyBuilder::kinematic_position_based().translation(start).lock_rotations()
        .additional_mass(1.0).can_sleep(false).ccd_enabled(false).build();
    let (h, _) = world.insert(walker, ColliderBuilder::cuboid(H, H, H).restitution(0.0).friction(0.8).build());
    // warm_broadphase
    let prediction = world.integration_parameters.prediction_distance();
    let mut pipeline = CollisionPipeline::new();
    pipeline.step(prediction, &mut world.islands, &mut world.broad_phase, &mut world.narrow_phase,
        &mut world.bodies, &mut world.colliders, &(), &());
    for (_, body) in world.bodies.iter_mut() {
        if !body.is_fixed() {
            body.wake_up(true);
        }
    }
    (world, h)
}

// One quantum: returns (new vy, grounded).
fn quantum(world: &mut PhysicsWorld, h: RigidBodyHandle, vx: f64, vy: f64) -> (f64, bool) {
    let mut vy = vy + G * DT;
    let desired = Vector::new(vx, vy, 0.0) * DT;
    let shape = SharedShape::cuboid(H, H, H);
    let pos = *world.bodies[h].position();
    let movement = {
        let q = world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(), &world.bodies,
            &world.colliders, QueryFilter::new().exclude_rigid_body(h));
        controller().move_shape(DT, &q, &*shape, &pos, desired, |_| {})
    };
    if movement.grounded {
        vy = 0.0;
    }
    let t = pos.translation + movement.translation;
    world.bodies[h].set_next_kinematic_translation(t);
    world.step();
    (vy, movement.grounded)
}

const FLOOR: ([f64; 3], [f64; 3], [f64; 4]) = ([0.0, -1.0, -3.0], [40.0, 0.0, 3.0], [0.0, 0.0, 0.0, 1.0]);

fn step_case(height: f64, vx: f64) -> (f64, f64) {
    let riser = ([11.0, 0.0, -3.0], [14.0, height, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let (mut w, h) = world_with(&[FLOOR, riser], Vector::new(10.0, H + 0.01, 0.0));
    let mut vy = 0.0;
    for _ in 0..((2.5 / vx) * 64.0) as usize {
        vy = quantum(&mut w, h, vx, vy).0;
    }
    let p = w.bodies[h].translation();
    (p.y - H, p.x)
}

fn slope_case(deg: f64, vx: f64, quanta: usize) -> f64 {
    let th = deg.to_radians();
    let (l, t) = (1.4, 0.35);
    let n = [-th.sin(), th.cos()];
    let cx = 11.0 + l * th.cos() - t * n[0];
    let cy = l * th.sin() - t * n[1];
    let ramp = ([cx - l, cy - t, -0.5], [cx + l, cy + t, 0.5], [0.0, 0.0, (th / 2.0).sin(), (th / 2.0).cos()]);
    let (mut w, h) = world_with(&[FLOOR, ramp], Vector::new(10.0, H + 0.01, 0.0));
    let mut vy = 0.0;
    let mut max_gain: f64 = 0.0;
    for _ in 0..quanta {
        vy = quantum(&mut w, h, vx, vy).0;
        max_gain = max_gain.max(w.bodies[h].translation().y - (H + 0.01));
    }
    max_gain
}

// Returns the longest run of consecutive ungrounded quanta after the edge.
fn drop_case(d: f64, vx: f64) -> u32 {
    let upper = ([0.0, -1.0, -3.0], [11.0, 0.0, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let lower = ([11.0, -1.0 - d, -3.0], [40.0, -d, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let (mut w, h) = world_with(&[upper, lower], Vector::new(10.5, H + 0.01, 0.0));
    let (mut vy, mut run, mut longest) = (0.0, 0u32, 0u32);
    for _ in 0..((1.5 / vx) * 64.0) as usize {
        let (nvy, grounded) = quantum(&mut w, h, vx, vy);
        vy = nvy;
        if grounded { run = 0 } else { run += 1; longest = longest.max(run) }
    }
    longest
}

fn main() {
    for &(d, vx) in &[(0.19, 0.4), (0.21, 0.4), (0.22, 0.4), (0.19, 2.0), (0.21, 2.0), (0.22, 2.0)] {
        println!("drop {} at {} u/s: longest ungrounded run {} quanta", d, vx, drop_case(d, vx));
    }
}
```
Expected output: `drop 0.19 at 0.4 u/s: longest ungrounded run 1 quanta drop 0.21 at 0.4 u/s: longest ungrounded run 1 quanta drop 0.22 at 0.4 u/s: longest ungrounded run 12 quanta drop 0.19 at 2 u/s: longest ungrounde`

## Keep max_ccd_substeps = 1 so Rapier CCD carries no state between quanta; it hashed alike on x86-64 and wasm32
**At max_ccd_substeps = 1 the CCD pass reads only values written in the same step and the CCDSolver holds a rebuildable cache; a 24-body CCD-heavy scene hashes identically on x86-64 release and debug and on wasm32 under V8, with a fresh CCDSolver swapped in mid-run.**

*Check 1: CCD-heavy scene: fixed hash, identical after a fresh CCDSolver at quantum 100* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// A CCD-heavy scene hashed bit-for-bit; a fresh CCDSolver swapped in mid-run.
use rapier3d_f64::prelude::*;

fn fnv(h: u64, x: u64) -> u64 {
    (h ^ x).wrapping_mul(0x100000001b3)
}

/// Returns (hash of every body's pose and velocity bits after 240 quanta,
/// number of body-quanta with CCD active, number of bullets).
pub fn probe(bullets: bool, reset_ccd_solver_at: u32) -> (u64, u32, u32) {
    let mut world = PhysicsWorld::new();
    world.gravity = Vector::new(0.0, -8.0, 0.0);
    world.integration_parameters.dt = 1.0 / 64.0;
    world.integration_parameters.contact_clustering = false;
    world.integration_parameters.warmstart_coefficient = 1.0;
    // Floor, two thin walls, a thin tilted fin.
    let fixed = [
        ((0.0, -0.5, 0.0), (6.0, 0.5, 6.0), (0.0, 0.0, 0.0, 1.0)),
        ((3.0, 1.0, 0.0), (0.01, 1.0, 3.0), (0.0, 0.0, 0.0, 1.0)),
        ((-3.0, 1.0, 0.0), (0.01, 1.0, 3.0), (0.0, 0.0, 0.0, 1.0)),
        ((0.0, 1.0, 2.0), (2.0, 1.0, 0.005), (0.0, 0.3826834323650898, 0.0, 0.9238795325112867)),
    ];
    for (t, h, q) in fixed {
        let mut rb = RigidBodyBuilder::fixed().translation(Vector::new(t.0, t.1, t.2)).build();
        rb.set_rotation(Rotation::from_xyzw(q.0, q.1, q.2, q.3), false);
        world.insert(rb, ColliderBuilder::cuboid(h.0, h.1, h.2).restitution(0.0).friction(0.8).build());
    }
    // A kinematic slab moving back and forth (a bullet target).
    let kin = world.insert(
        RigidBodyBuilder::kinematic_position_based().translation(Vector::new(0.0, 1.0, -2.0)).build(),
        ColliderBuilder::cuboid(1.5, 0.8, 0.01).build(),
    ).0;
    let mut handles = Vec::new();
    for i in 0..24u32 {
        let fi = i as f64;
        let x = -2.0 + (i % 6) as f64 * 0.8;
        let z = -1.0 + (i / 6) as f64 * 0.7;
        let v = Vector::new(
            if i % 2 == 0 { 25.0 + fi } else { -25.0 - fi },
            -10.0 - 2.0 * fi,
            if i % 3 == 0 { 30.0 } else { -12.0 + fi },
        );
        let rb = RigidBodyBuilder::dynamic()
            .translation(Vector::new(x, 1.0 + 0.1 * fi, z))
            .linvel(v)
            .angvel(Vector::new(0.3 * fi, -2.0, 1.0 + 0.1 * fi))
            .ccd_enabled(bullets && i % 2 == 0)
            .build();
        let (h, _) = world.insert(rb, ColliderBuilder::cuboid(0.05, 0.08 + 0.002 * fi, 0.06).restitution(0.0).friction(0.8).build());
        handles.push(h);
    }
    let mut active = 0u32;
    for q in 0..240u32 {
        if q == reset_ccd_solver_at {
            world.ccd_solver = CCDSolver::new();
        }
        let t = q as f64 / 64.0;
        let x = if (q / 32) % 2 == 0 { -1.0 + t % 0.5 } else { 1.0 - t % 0.5 };
        world.bodies[kin].set_next_kinematic_translation(Vector::new(x, 1.0, -2.0));
        world.step();
        for h in &handles {
            if world.bodies[*h].is_ccd_active() {
                active += 1;
            }
        }
    }
    let mut hash = 0xcbf29ce484222325u64;
    for h in &handles {
        let b = &world.bodies[*h];
        let p = b.translation();
        let r = b.rotation();
        let v = b.linvel();
        let w = b.angvel();
        for x in [p.x, p.y, p.z, r.x, r.y, r.z, r.w, v.x, v.y, v.z, w.x, w.y, w.z] {
            hash = fnv(hash, x.to_bits());
        }
    }
    (hash, active, handles.len() as u32)
}

fn main() {
    for bullets in [false, true] {
        let (h, active, _) = probe(bullets, u32::MAX);
        let (h2, _, _) = probe(bullets, 100);
        println!("bullets={} hash={:016x} ccd-active body-quanta={} fresh CCDSolver at q100 -> {}",
            bullets, h, active, if h == h2 { "identical" } else { "DIFFERENT" });
    }
}
```
Expected output: `bullets=false hash=3eb23b3feb5785fc ccd-active body-quanta=2076 fresh CCDSolver at q100 -> identical bullets=true hash=bfe836cfd760e133 ccd-active body-quanta=2019 fresh CCDSolver at q100 -> identical`

## Lint wasm by decoding every instruction: 0x40 and 0xFD bytes recur in block types, immediates and data
**The solver binary's code section holds 16,558 bytes equal to 0x40 against one memory.grow (14,916 of them empty block types) and 277 bytes equal to 0xFD against zero SIMD instructions; i32.const 32893 encodes as 41 fd 80 02.**

*Check 1: A body with 0x40 twice and fd 80 02 once decodes to no memory.grow and no relaxed op* · `runs` · edition 2021 · host · bin · deps: wasmparser · exit code 0 · **✔ oracle pass**
```rust
// A function body with no memory.grow and no relaxed SIMD whose bytes still
// contain 0x40 twice and the sequence fd 80 02 once.
use wasmparser::{BinaryReader, FunctionBody};

fn decode(body: &[u8]) -> Vec<String> {
    let mut ops = FunctionBody::new(BinaryReader::new(body, 0)).get_operators_reader().unwrap();
    let mut out = Vec::new();
    while !ops.eof() {
        out.push(format!("{:?}", ops.read().unwrap()));
    }
    out
}

fn main() {
    // no locals; block (empty) end; i32.const -64; drop; i32.const 32893; drop; end
    let body = [0x00, 0x02, 0x40, 0x0b, 0x41, 0x40, 0x1a, 0x41, 0xfd, 0x80, 0x02, 0x1a, 0x0b];
    let naive_40 = body.iter().filter(|&&b| b == 0x40).count();
    let naive_relaxed = body.windows(3).filter(|w| *w == [0xfd, 0x80, 0x02]).count();
    let ops = decode(&body);
    let grows = ops.iter().filter(|o| o.starts_with("MemoryGrow")).count();
    let relaxed = ops.iter().filter(|o| o.contains("Relaxed")).count();
    println!("byte scan: 0x40 x{} | fd 80 02 x{}", naive_40, naive_relaxed);
    println!("decoded: memory.grow x{} | relaxed x{}", grows, relaxed);
    println!("{}", ops.join(" | "));
}
```
Expected output: `byte scan: 0x40 x2 / fd 80 02 x1 decoded: memory.grow x0 / relaxed x0 Block { blockty: Empty } / End / I32Const { value: -64 } / Drop / I32Const { value: 32893 } / Drop / End`

## Match relaxed SIMD as 0xFD then u32 LEB128 256..=275 and memory.grow as 0x40 then a memidx, padding allowed
**Relaxed SIMD is 0xFD followed by the opcode 0x100..=0x113 as a u32 LEB128 (canonically fd 80 02 to fd 93 02; 0x114-0x12F reserved) and memory.grow is 0x40 followed by a memidx; V8 and wasmparser accept padded encodings such as fd 80 82 80 80 00 and 40 80 00.**

*Check 1: wasmparser decodes padded relaxed and memory.grow encodings; 0x100..=0x113 are relaxed* · `runs` · edition 2021 · host · bin · deps: wasmparser · exit code 0 · **✔ oracle pass**
```rust
// How wasmparser 0.259 decodes memory.grow and the relaxed-SIMD opcodes.
use wasmparser::{BinaryReader, FunctionBody};

fn first_op(code: &[u8]) -> String {
    let mut body = vec![0x00];
    body.extend_from_slice(code);
    body.push(0x0b);
    let mut ops = FunctionBody::new(BinaryReader::new(&body, 0)).get_operators_reader().unwrap();
    match ops.read() {
        Ok(op) => format!("{:?}", op),
        Err(e) => format!("error: {}", e.message()),
    }
}

fn uleb(mut n: u32) -> Vec<u8> {
    let mut out = Vec::new();
    loop {
        let mut b = (n & 0x7f) as u8;
        n >>= 7;
        if n != 0 {
            b |= 0x80;
        }
        out.push(b);
        if n == 0 {
            return out;
        }
    }
}

fn main() {
    for code in [
        &[0x40, 0x00][..],
        &[0x40, 0x80, 0x00][..],
        &[0xfd, 0x80, 0x02][..],
        &[0xfd, 0x80, 0x82, 0x80, 0x80, 0x00][..],
        &[0xfd, 0x85, 0x02][..],
        &[0xfd, 0x87, 0x02][..],
        &[0xfd, 0x93, 0x02][..],
        &[0xfd, 0x94, 0x02][..],
    ] {
        let hex: Vec<String> = code.iter().map(|b| format!("{:02x}", b)).collect();
        println!("{} -> {}", hex.join(" "), first_op(code));
    }
    let named = (0x100u32..=0x113)
        .filter(|&sub| {
            let mut code = vec![0xfd];
            code.extend(uleb(sub));
            first_op(&code).contains("Relaxed")
        })
        .count();
    println!("0xfd subopcodes 0x100..=0x113 decoding as relaxed: {}/20", named);
}
```
Expected output: `40 00 -> MemoryGrow { mem: 0 } 40 80 00 -> MemoryGrow { mem: 0 } fd 80 02 -> I8x16RelaxedSwizzle fd 80 82 80 80 00 -> I8x16RelaxedSwizzle fd 85 02 -> F32x4RelaxedMadd fd 87 02 -> F64x2RelaxedMadd fd 9`

## Remove memory.grow from the law's binary with a fixed-arena #[global_allocator]: dlmalloc 0.2.13 over one span
**std 1.98.1's wasm32 System allocator is dlmalloc 0.2.13 and calls memory.grow; a #[global_allocator] that hands dlmalloc one fixed span removes the instruction and left the solver's results bit-identical.**

*Check 1: std's allocator grows the memory 65 pages to hold a 4 MiB Vec* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, grew · imports nothing · node calls grew() · **✔ oracle pass**
```rust
// std's allocator on wasm32-unknown-unknown: allocate 4 MiB and report how
// many pages the memory grew by while doing it.
#[no_mangle]
pub extern "C" fn grew() -> i32 {
    let before = core::arch::wasm32::memory_size(0);
    let v: Vec<u64> = (0..524_288u64).collect();
    let sum: u64 = v.iter().sum();
    let after = core::arch::wasm32::memory_size(0);
    if sum != 524_288 * 524_287 / 2 {
        return -1;
    }
    (after - before) as i32
}
```
Expected output: `65`

*Check 2: Freed memory is reused and never returned: 65 pages grown, then 0 for 1 MiB* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, high_water · imports nothing · node calls high_water() · **✔ oracle pass**
```rust
// std's allocator: grow for 4 MiB, drop it, then allocate 1 MiB. Returns
// pages grown in phase one * 1000 + pages grown in phase two.
#[no_mangle]
pub extern "C" fn high_water() -> i32 {
    let p0 = core::arch::wasm32::memory_size(0);
    {
        let v: Vec<u64> = (0..524_288u64).collect();
        core::hint::black_box(&v);
    }
    let p1 = core::arch::wasm32::memory_size(0);
    let w: Vec<u64> = (0..131_072u64).collect();
    core::hint::black_box(&w);
    let p2 = core::arch::wasm32::memory_size(0);
    ((p1 - p0) * 1000 + (p2 - p1)) as i32
}
```
Expected output: `65000`

*Check 3: A fixed-arena #[global_allocator] under --no-growable-memory grows 0 pages* · `runs` · edition 2021 · wasm32-unknown-unknown · cdylib · exports memory, grew · imports nothing · node calls grew() · **✔ oracle pass**
```rust
// A #[global_allocator] over a fixed static arena: power-of-two size classes,
// a free list per class, bump allocation from the arena. It never calls
// memory.grow; exhaustion returns null and Rust aborts.
use std::alloc::{GlobalAlloc, Layout};
use std::cell::UnsafeCell;

const ARENA_BYTES: usize = 8 << 20;
const CLASSES: usize = 32;

#[repr(C, align(4096))]
struct Arena(UnsafeCell<[u8; ARENA_BYTES]>);
unsafe impl Sync for Arena {}
static ARENA: Arena = Arena(UnsafeCell::new([0; ARENA_BYTES]));

struct State {
    next: usize,
    free: [usize; CLASSES],
}
struct Holder(UnsafeCell<State>);
unsafe impl Sync for Holder {}
static STATE: Holder = Holder(UnsafeCell::new(State { next: 0, free: [0; CLASSES] }));

struct FixedArena;

fn class_of(layout: Layout) -> usize {
    let need = layout.size().max(layout.align()).max(16);
    (usize::BITS - (need - 1).leading_zeros()) as usize
}

unsafe impl GlobalAlloc for FixedArena {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        let c = class_of(layout);
        if c >= CLASSES {
            return std::ptr::null_mut();
        }
        let st = unsafe { &mut *STATE.0.get() };
        let head = st.free[c];
        if head != 0 {
            st.free[c] = unsafe { *(head as *const usize) };
            return head as *mut u8;
        }
        let size = 1usize << c;
        let align = size.min(4096);
        let base = ARENA.0.get() as usize;
        let start = (base + st.next + align - 1) & !(align - 1);
        if start + size > base + ARENA_BYTES {
            return std::ptr::null_mut();
        }
        st.next = start + size - base;
        start as *mut u8
    }

    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        let c = class_of(layout);
        let st = unsafe { &mut *STATE.0.get() };
        unsafe { *(ptr as *mut usize) = st.free[c] };
        st.free[c] = ptr as usize;
    }
}

#[global_allocator]
static GLOBAL: FixedArena = FixedArena;

#[no_mangle]
pub extern "C" fn grew() -> i32 {
    let before = core::arch::wasm32::memory_size(0);
    let v: Vec<u64> = (0..524_288u64).collect();
    let sum: u64 = v.iter().sum();
    let after = core::arch::wasm32::memory_size(0);
    if sum != 524_288 * 524_287 / 2 {
        return -1;
    }
    (after - before) as i32
}
```
Expected output: `0`

## Set T4's step heights around max_height + offset: KinematicCharacterController climbs 0.31 at max_height 0.3
**handle_stairs evaluates max_height + offset and min_width + offset, so with max_height 0.3 and offset 0.01 the engine's box walker climbs steps up to 0.3101, and its feet rest one offset above every surface.**

*Check 1: The engine's walker loop: 0.29-0.31 climbed, 0.311 and 0.32 stopped, feet one offset up* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// The engine's walker loop (solver/src/rapier_law.rs integrate()) for one box
// walker, natively: controller constants, gravity, grounded -> vy = 0,
// set_next_kinematic_translation, world.step(). Prints course outcomes.
use rapier3d_f64::control::{CharacterAutostep, CharacterLength, KinematicCharacterController};
use rapier3d_f64::pipeline::CollisionPipeline;
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;
const G: f64 = -8.0;
const H: f64 = 0.25;

fn controller() -> KinematicCharacterController {
    KinematicCharacterController {
        up: Vector::new(0.0, 1.0, 0.0),
        offset: CharacterLength::Absolute(0.01),
        slide: true,
        autostep: Some(CharacterAutostep {
            max_height: CharacterLength::Absolute(0.3),
            min_width: CharacterLength::Absolute(0.2),
            include_dynamic_bodies: false,
        }),
        max_slope_climb_angle: core::f64::consts::FRAC_PI_4,
        min_slope_slide_angle: 50.0 * core::f64::consts::PI / 180.0,
        snap_to_ground: Some(CharacterLength::Absolute(0.2)),
        normal_nudge_factor: 1.0e-4,
    }
}

// (min, max, quaternion xyzw) boxes -> fixed cuboids, like build_world.
fn world_with(boxes: &[([f64; 3], [f64; 3], [f64; 4])], start: Vector) -> (PhysicsWorld, RigidBodyHandle) {
    let mut world = PhysicsWorld::new();
    world.gravity = Vector::new(0.0, G, 0.0);
    world.integration_parameters.dt = DT;
    world.integration_parameters.contact_clustering = false;
    world.integration_parameters.warmstart_coefficient = 1.0;
    for (min, max, q) in boxes {
        let c = Vector::new((min[0] + max[0]) * 0.5, (min[1] + max[1]) * 0.5, (min[2] + max[2]) * 0.5);
        let mut body = RigidBodyBuilder::fixed().translation(c).build();
        body.set_rotation(Rotation::from_xyzw(q[0], q[1], q[2], q[3]), false);
        let co = ColliderBuilder::cuboid((max[0] - min[0]) * 0.5, (max[1] - min[1]) * 0.5, (max[2] - min[2]) * 0.5)
            .restitution(0.0).friction(0.8).build();
        world.insert(body, co);
    }
    let walker = RigidBodyBuilder::kinematic_position_based().translation(start).lock_rotations()
        .additional_mass(1.0).can_sleep(false).ccd_enabled(false).build();
    let (h, _) = world.insert(walker, ColliderBuilder::cuboid(H, H, H).restitution(0.0).friction(0.8).build());
    // warm_broadphase
    let prediction = world.integration_parameters.prediction_distance();
    let mut pipeline = CollisionPipeline::new();
    pipeline.step(prediction, &mut world.islands, &mut world.broad_phase, &mut world.narrow_phase,
        &mut world.bodies, &mut world.colliders, &(), &());
    for (_, body) in world.bodies.iter_mut() {
        if !body.is_fixed() {
            body.wake_up(true);
        }
    }
    (world, h)
}

// One quantum: returns (new vy, grounded).
fn quantum(world: &mut PhysicsWorld, h: RigidBodyHandle, vx: f64, vy: f64) -> (f64, bool) {
    let mut vy = vy + G * DT;
    let desired = Vector::new(vx, vy, 0.0) * DT;
    let shape = SharedShape::cuboid(H, H, H);
    let pos = *world.bodies[h].position();
    let movement = {
        let q = world.broad_phase.as_query_pipeline(world.narrow_phase.query_dispatcher(), &world.bodies,
            &world.colliders, QueryFilter::new().exclude_rigid_body(h));
        controller().move_shape(DT, &q, &*shape, &pos, desired, |_| {})
    };
    if movement.grounded {
        vy = 0.0;
    }
    let t = pos.translation + movement.translation;
    world.bodies[h].set_next_kinematic_translation(t);
    world.step();
    (vy, movement.grounded)
}

const FLOOR: ([f64; 3], [f64; 3], [f64; 4]) = ([0.0, -1.0, -3.0], [40.0, 0.0, 3.0], [0.0, 0.0, 0.0, 1.0]);

fn step_case(height: f64, vx: f64) -> (f64, f64) {
    let riser = ([11.0, 0.0, -3.0], [14.0, height, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let (mut w, h) = world_with(&[FLOOR, riser], Vector::new(10.0, H + 0.01, 0.0));
    let mut vy = 0.0;
    for _ in 0..((2.5 / vx) * 64.0) as usize {
        vy = quantum(&mut w, h, vx, vy).0;
    }
    let p = w.bodies[h].translation();
    (p.y - H, p.x)
}

fn slope_case(deg: f64, vx: f64, quanta: usize) -> f64 {
    let th = deg.to_radians();
    let (l, t) = (1.4, 0.35);
    let n = [-th.sin(), th.cos()];
    let cx = 11.0 + l * th.cos() - t * n[0];
    let cy = l * th.sin() - t * n[1];
    let ramp = ([cx - l, cy - t, -0.5], [cx + l, cy + t, 0.5], [0.0, 0.0, (th / 2.0).sin(), (th / 2.0).cos()]);
    let (mut w, h) = world_with(&[FLOOR, ramp], Vector::new(10.0, H + 0.01, 0.0));
    let mut vy = 0.0;
    let mut max_gain: f64 = 0.0;
    for _ in 0..quanta {
        vy = quantum(&mut w, h, vx, vy).0;
        max_gain = max_gain.max(w.bodies[h].translation().y - (H + 0.01));
    }
    max_gain
}

// Returns the longest run of consecutive ungrounded quanta after the edge.
fn drop_case(d: f64, vx: f64) -> u32 {
    let upper = ([0.0, -1.0, -3.0], [11.0, 0.0, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let lower = ([11.0, -1.0 - d, -3.0], [40.0, -d, 3.0], [0.0, 0.0, 0.0, 1.0]);
    let (mut w, h) = world_with(&[upper, lower], Vector::new(10.5, H + 0.01, 0.0));
    let (mut vy, mut run, mut longest) = (0.0, 0u32, 0u32);
    for _ in 0..((1.5 / vx) * 64.0) as usize {
        let (nvy, grounded) = quantum(&mut w, h, vx, vy);
        vy = nvy;
        if grounded { run = 0 } else { run += 1; longest = longest.max(run) }
    }
    longest
}

fn main() {
    for &(hgt, vx) in &[(0.29, 2.0), (0.30, 2.0), (0.31, 2.0), (0.311, 2.0), (0.32, 2.0), (0.31, 0.4), (0.311, 0.4)] {
        let (feet, x) = step_case(hgt, vx);
        let climbed = feet > hgt && x - H > 11.0;
        println!("step {} at {} u/s: {}, feet {:.4} above {}", hgt, vx, if climbed { "climbed" } else { "stopped" },
            if climbed { feet - hgt } else { feet }, if climbed { "the step top" } else { "the floor" });
    }
}
```
Expected output: `step 0.29 at 2 u/s: climbed, feet 0.0100 above the step top step 0.3 at 2 u/s: climbed, feet 0.0101 above the step top step 0.31 at 2 u/s: climbed, feet 0.0100 above the step top step 0.311 at 2 u/s: `

