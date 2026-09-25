# Rapier state for restore (T2) — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](restore-internals.md) · [catalog index](README.md)

## Copy RigidBodyActivation whole or not at all: its pub(crate) sleep_prev_pose restarts the sleep timer
**RigidBodyActivation has five pub fields plus pub(crate) sleep_prev_pose (the pose at the previous energy update); rebuilding it from the pub fields resets time_since_can_sleep to 0 on the next step for any body not at the origin.**

*Check 1: Rebuilding RigidBodyActivation from its pub fields resets the sleep timer* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
// E1: rebuild every dynamic body's RigidBodyActivation through the public API
// (all five pub fields copied) in a twin; touch the original with an identical
// whole-struct write so both take the same activation_mut path. Step both once.
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;

fn world() -> PhysicsWorld {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = DT;
    w.integration_parameters.contact_clustering = false;
    let floor = RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)).build();
    w.insert(floor, ColliderBuilder::cuboid(5.0, 0.5, 5.0).friction(0.8).restitution(0.0).build());
    for i in 0..3 {
        let mut b = RigidBodyBuilder::dynamic()
            .translation(Vector::new(0.05 * i as f64, 0.5 + 1.05 * i as f64, 0.0))
            .can_sleep(true)
            .build();
        b.activation_mut().time_until_sleep = 32.0 * DT;
        w.insert(b, ColliderBuilder::cuboid(0.5, 0.5, 0.5).friction(0.8).restitution(0.0).build());
    }
    w
}

fn twin(w: &PhysicsWorld) -> PhysicsWorld {
    PhysicsWorld {
        gravity: w.gravity,
        integration_parameters: w.integration_parameters,
        physics_pipeline: PhysicsPipeline::new(),
        islands: w.islands.clone(),
        broad_phase: w.broad_phase.clone(),
        narrow_phase: w.narrow_phase.clone(),
        bodies: w.bodies.clone(),
        colliders: w.colliders.clone(),
        impulse_joints: w.impulse_joints.clone(),
        multibody_joints: w.multibody_joints.clone(),
        ccd_solver: CCDSolver::new(),
    }
}

fn main() {
    let mut a = world();
    // Run until every dynamic body has started its sleep timer but none sleeps.
    let mut n = 0;
    loop {
        a.step();
        n += 1;
        let ok = a.bodies.iter().filter(|(_, b)| b.is_dynamic()).all(|(_, b)| {
            let act = b.activation();
            act.time_since_can_sleep > 4.0 * DT && !act.sleeping
        });
        if ok || n > 400 { break; }
    }
    let mut b = twin(&a);
    let handles: Vec<RigidBodyHandle> =
        a.bodies.iter().filter(|(_, b)| b.is_dynamic()).map(|(h, _)| h).collect();
    for &h in &handles {
        let same = *a.bodies[h].activation();
        *a.bodies[h].activation_mut() = same; // identical write, same change flags
        let old = *b.bodies[h].activation();
        let mut act = RigidBodyActivation::active();
        act.normalized_linear_threshold = old.normalized_linear_threshold;
        act.angular_threshold = old.angular_threshold;
        act.time_until_sleep = old.time_until_sleep;
        act.time_since_can_sleep = old.time_since_can_sleep;
        act.sleeping = old.sleeping;
        *b.bodies[h].activation_mut() = act;
    }
    let before: Vec<f64> =
        handles.iter().map(|h| a.bodies[*h].activation().time_since_can_sleep / DT).collect();
    a.step();
    b.step();
    let qa: Vec<f64> = handles.iter().map(|h| a.bodies[*h].activation().time_since_can_sleep / DT).collect();
    let qb: Vec<f64> = handles.iter().map(|h| b.bodies[*h].activation().time_since_can_sleep / DT).collect();
    println!("saved at step {n}: quanta {before:?}");
    println!("next step, whole activation kept: {qa:?}");
    println!("next step, pub fields rebuilt:    {qb:?}");
}
```
Expected output: `saved at step 20: quanta [19.0, 5.0, 5.0] next step, whole activation kept: [20.0, 6.0, 6.0] next step, pub fields rebuilt:    [0.0, 0.0, 0.0]`

## Count more than warm-start impulses as solver state: frozen arms, parry points, recycle state, colours
**Besides warmstart_impulse, warmstart_tangent_world and warmstart_twist_impulse, the 0.35.3 solver reads solver_dp1/solver_dp2 (lever arms frozen at the last full update) and history-kept contact points; the pair's pub(crate) recycle_state and solver_color decide recycling and solve order.**

*Check 1: A world rebuilt at bit-equal poses reads different contact geometry* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
// Three stacked boxes settle for 20 quanta. A second world is built with the same
// bodies at bit-equal poses and velocities (whole activation copied). Both take one
// step; compare what the solver read for each contact point in that step.
use rapier3d_f64::prelude::*;

fn world(state: Option<&[(Pose, Vector, Vector, RigidBodyActivation)]>) -> (PhysicsWorld, Vec<RigidBodyHandle>) {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    w.integration_parameters.contact_clustering = false;
    let floor = RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)).build();
    w.insert(floor, ColliderBuilder::cuboid(5.0, 0.5, 5.0).friction(0.8).build());
    let mut hs = Vec::new();
    for i in 0..3 {
        let mut b = RigidBodyBuilder::dynamic()
            .translation(Vector::new(0.05 * i as f64, 0.5 + 1.05 * i as f64, 0.0)).build();
        if let Some(s) = state {
            b.set_position(s[i].0, false);
            b.set_linvel(s[i].1, false);
            b.set_angvel(s[i].2, false);
            *b.activation_mut() = s[i].3;
        }
        hs.push(w.insert(b, ColliderBuilder::cuboid(0.5, 0.5, 0.5).friction(0.8).build()).0);
    }
    (w, hs)
}

fn read_by_solver(w: &PhysicsWorld) -> Vec<[u64; 13]> {
    let mut pairs: Vec<_> = w.narrow_phase.contact_pairs().collect();
    pairs.sort_by_key(|p| (p.collider1.into_raw_parts(), p.collider2.into_raw_parts()));
    let mut out = Vec::new();
    for p in pairs {
        for m in p.solver_manifolds() {
            for pt in &m.points {
                let (a, b, d1, d2) = (pt.local_p1, pt.local_p2, pt.data.solver_dp1, pt.data.solver_dp2);
                out.push([a.x, a.y, a.z, b.x, b.y, b.z, d1.x, d1.y, d1.z, d2.x, d2.y, d2.z, pt.dist].map(f64::to_bits));
            }
        }
    }
    out
}

fn main() {
    let (mut a, hs) = world(None);
    for _ in 0..20 { a.step(); }
    let saved: Vec<_> = hs.iter().map(|h| {
        let b = &a.bodies[*h];
        (*b.position(), b.linvel(), b.angvel(), *b.activation())
    }).collect();
    let (mut r, _) = world(Some(&saved));
    a.step();
    r.step();
    let (ga, gr) = (read_by_solver(&a), read_by_solver(&r));
    let differ = ga.iter().zip(&gr).filter(|(x, y)| x != y).count();
    println!("points {} vs {}; of the pairs compared, points whose anchors, lever arms or dist differ: {}",
             ga.len(), gr.len(), differ);
}
```
Expected output: `points 12 vs 11; of the pairs compared, points whose anchors, lever arms or dist differ: 11`

## Do not rebuild Rapier's broad phase every step: a fresh BroadPhaseBvh never deletes a narrow-phase pair
**A fresh BroadPhaseBvh has no record of the pairs the narrow phase holds, so it never emits DeletePair; NarrowPhase removes contact pairs only on DeletePair, collider removal or a sensor change, so separated pairs stay forever.**

*Check 1: Pin 6's per-step rebuild never deletes a narrow-phase pair* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
// Pin 6's fallback: a fresh BroadPhaseBvh, filled with set_aabb for every collider,
// before every step. A box slides away from a pillar it started beside.
use rapier3d_f64::prelude::*;

fn world() -> (PhysicsWorld, ColliderHandle, ColliderHandle) {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    let floor = RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)).build();
    w.insert(floor, ColliderBuilder::cuboid(20.0, 0.5, 20.0).friction(0.0).build());
    let pillar = RigidBodyBuilder::fixed().translation(Vector::new(0.0, 1.0, 0.0)).build();
    let (_, pc) = w.insert(pillar, ColliderBuilder::cuboid(0.5, 1.0, 0.5).friction(0.0).build());
    let bx = RigidBodyBuilder::dynamic().translation(Vector::new(1.0, 0.5, 0.0)).linvel(Vector::new(4.0, 0.0, 0.0)).build();
    let (_, bc) = w.insert(bx, ColliderBuilder::cuboid(0.49, 0.5, 0.49).friction(0.0).build());
    (w, pc, bc)
}

fn fresh_broad_phase(w: &mut PhysicsWorld) {
    let params = w.integration_parameters;
    let mut bp = BroadPhaseBvh::new();
    for (h, co) in w.colliders.iter() {
        bp.set_aabb(&params, h, co.compute_broad_phase_aabb(&params, &w.bodies));
    }
    w.broad_phase = bp;
}

fn main() {
    let (mut kept, pc, bc) = world();
    let (mut rebuilt, _, _) = world();
    for _ in 0..64 {
        kept.step();
        fresh_broad_phase(&mut rebuilt);
        rebuilt.step();
    }
    let gap = |w: &PhysicsWorld| w.colliders[bc].position().translation.x - 0.49 - 0.5;
    println!("gap to pillar {:.2} m / {:.2} m; box-pillar pair present: kept {}, rebuilt every step {}",
             gap(&kept), gap(&rebuilt),
             kept.narrow_phase.contact_pair(pc, bc).is_some(), rebuilt.narrow_phase.contact_pair(pc, bc).is_some());
}
```
Expected output: `gap to pillar 4.01 m / 4.01 m; box-pillar pair present: kept false, rebuilt every step true`

## Expect a rebuilt BroadPhaseBvh to report fewer pairs: new parry leaves are tight, moved leaves are fat
**parry stores a new leaf with its raw AABB and adds the 0.04 x length_unit margin only when a moved collider leaves its leaf, so a running world holds fat leaves where a world rebuilt from bodies holds tight ones, and reports a different pair set.**

*Check 1: A rebuilt broad phase reports a different pair set (tight vs fat leaves)* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
// Two boxes fall side by side, 0.05 apart, touching nothing. Compare the pair set
// of the running world with a world rebuilt from the same poses and velocities
// plus one CollisionPipeline pass (the engine's load pass).
use rapier3d_f64::pipeline::CollisionPipeline;
use rapier3d_f64::prelude::*;

fn world(xs: [(f64, f64); 2]) -> PhysicsWorld {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    for (x, vy) in xs {
        let b = RigidBodyBuilder::dynamic().translation(Vector::new(x, 10.0, 0.0)).linvel(Vector::new(0.0, vy, 0.0)).build();
        w.insert(b, ColliderBuilder::cuboid(0.5, 0.5, 0.5).build());
    }
    w
}

fn load_pass(w: &mut PhysicsWorld) {
    let p = w.integration_parameters.prediction_distance();
    CollisionPipeline::new().step(p, &mut w.islands, &mut w.broad_phase, &mut w.narrow_phase,
                                  &mut w.bodies, &mut w.colliders, &(), &());
    // As warm_broadphase: re-admit every body to the next step's active set.
    for (_, b) in w.bodies.iter_mut() {
        if !b.is_fixed() { b.wake_up(true); }
    }
}

fn main() {
    let mut running = world([(0.0, 0.0), (1.05, 0.0)]);
    load_pass(&mut running);
    let at_load = running.narrow_phase.contact_pairs().count();
    for _ in 0..3 { running.step(); }
    let hs: Vec<RigidBodyHandle> = running.bodies.iter().map(|(h, _)| h).collect();
    let mut rebuilt = world([(0.0, 0.0), (1.05, 0.0)]);
    for h in &hs {
        let (p, v) = (*running.bodies[*h].position(), running.bodies[*h].linvel());
        rebuilt.bodies[*h].set_position(p, false);
        rebuilt.bodies[*h].set_linvel(v, false);
    }
    load_pass(&mut rebuilt);
    let same = hs.iter().all(|h| running.bodies[*h].position() == rebuilt.bodies[*h].position());
    println!("poses equal: {same}; fell {:.4} m; pairs at load {at_load}; after 3 quanta: running {}, rebuilt {}", 10.0 - running.bodies[hs[0]].translation().y,
             running.narrow_phase.contact_pairs().count(), rebuilt.narrow_phase.contact_pairs().count());
}
```
Expected output: `poses equal: true; fell 0.0095 m; pairs at load 0; after 3 quanta: running 1, rebuilt 0`

## Never write through a ptr::from_ref pointer to a ContactPair: parking it in a Vec only hides the UB
**A pointer made by ptr::from_ref from &ContactPair may never be written through; doing so mutates bytes behind a shared reference, which the Reference lists as UB.**

*Check 1: One-expression &T to &mut T cast is rejected by invalid_reference_casting* · `compile_fail` · edition 2021 · host · lib · lints: invalid_reference_casting · **✔ oracle pass**
```rust
pub struct Pair { pub w: f64 }
pub fn clear(p: &Pair) {
    unsafe {
        let m = &mut *(core::ptr::from_ref(p) as *mut Pair);
        m.w = 0.0;
    }
}
```

*Check 2: The engine's shape (pointers parked in a Vec) compiles with no diagnostic* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
// The engine's shape: pointers collected from shared references, written later.
pub struct Pair { pub w: f64 }
pub fn clear(pairs: &[Pair]) -> usize {
    let mut ptrs: Vec<*mut Pair> = Vec::new();
    for p in pairs {
        ptrs.push(core::ptr::from_ref(p) as *mut Pair);
    }
    let n = ptrs.len();
    for ptr in ptrs {
        unsafe {
            let pair = &mut *ptr;
            pair.w = 0.0;
        }
    }
    n
}
```

## Read enhanced-determinism as history-deterministic iteration order, not state-canonical order
**enhanced-determinism makes parry's HashMap/HashSet an IndexMap/IndexSet with a pointer-size-independent FxHasher32, forces libm and canonical signed zeros: orders become a deterministic function of the operation history on every IEEE 754 target, not of the current state.**

*Check 1: Under enhanced-determinism parry's HashMap is an IndexMap* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
// Under enhanced-determinism parry's HashMap (the map Rapier's broad phase and
// composite workspaces use) is an IndexMap: insertion order, and swap_remove exists.
use rapier3d_f64::parry::utils::hashmap::HashMap;
fn main() {
    let mut m: HashMap<u32, u32> = HashMap::default();
    for k in [30u32, 10, 20, 5] { m.insert(k, k * 2); }
    let before: Vec<u32> = m.keys().copied().collect();
    m.swap_remove(&30);
    let after: Vec<u32> = m.keys().copied().collect();
    println!("{before:?} -> {after:?}");
}
```
Expected output: `[30, 10, 20, 5] -> [5, 10, 20]`

## Read warmstart_coefficient as a per-substep switch, not as clearing the cached warm start
**warmstart_coefficient is read every step inside each substep's constraint update; 0.0 also removes warm starting between the substeps of every quantum, so it is not the same act as zeroing the cached manifold-point values.**

*Check 1: warmstart_coefficient is read from the first quantum* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
// Is IntegrationParameters::warmstart_coefficient read from the first quantum? A box
// resting on a slab, two worlds at 1.0 and 0.0: the first quantum whose pose or
// velocity bits differ, and the first quantum a contact point carries an impulse.
use rapier3d_f64::prelude::*;

fn world(coefficient: f64) -> (PhysicsWorld, RigidBodyHandle) {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    w.integration_parameters.contact_clustering = false;
    w.integration_parameters.warmstart_coefficient = coefficient;
    let slab = RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)).build();
    w.insert(slab, ColliderBuilder::cuboid(5.0, 0.5, 5.0).friction(0.8).build());
    let b = RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 0.5, 0.0)).build();
    let (h, _) = w.insert(b, ColliderBuilder::cuboid(0.5, 0.5, 0.5).friction(0.8).build());
    (w, h)
}

fn bits(w: &PhysicsWorld, h: RigidBodyHandle) -> [u64; 7] {
    let b = &w.bodies[h];
    let (p, v) = (b.translation(), b.linvel());
    [p.x, p.y, p.z, v.x, v.y, v.z, b.rotation().w].map(f64::to_bits)
}

fn main() {
    let (mut on, h) = world(1.0);
    let (mut off, _) = world(0.0);
    let (mut loaded, mut differ) = (None, None);
    for q in 1..=8 {
        on.step();
        off.step();
        let carries = on.narrow_phase.contact_pairs()
            .any(|p| p.solver_manifolds().iter().any(|m| m.points.iter().any(|pt| pt.data.impulse != 0.0)));
        if loaded.is_none() && carries { loaded = Some(q); }
        if differ.is_none() && bits(&on, h) != bits(&off, h) { differ = Some(q); }
    }
    println!("first quantum a contact carries an impulse: {loaded:?}; first quantum 1.0 and 0.0 differ: {differ:?}");
}
```
Expected output: `first quantum a contact carries an impulse: Some(1); first quantum 1.0 and 0.0 differ: Some(1)`

*Check 2: Stack at engine parameters: warm start on vs off* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
// Route (a): a 4-box stack at the engine's integration parameters (build_world:
// dt 1/64, g -8, clustering off, friction 0.8, restitution 0, sleep 32 quanta,
// default iterations), warm start on (1.0) vs off (0.0), one persistent world each.
use rapier3d_f64::prelude::*;

fn run(coefficient: f64) -> String {
    let dt = 1.0 / 64.0;
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = dt;
    w.integration_parameters.contact_clustering = false;
    w.integration_parameters.warmstart_coefficient = coefficient;
    let floor = RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)).build();
    w.insert(floor, ColliderBuilder::cuboid(5.0, 0.5, 5.0).restitution(0.0).friction(0.8).build());
    let mut hs = Vec::new();
    for i in 0..4 {
        let mut b = RigidBodyBuilder::dynamic()
            .translation(Vector::new(0.0, 0.5 + 1.0 * i as f64, 0.0))
            .can_sleep(true).ccd_enabled(false).build();
        b.activation_mut().time_until_sleep = 32.0 * dt;
        hs.push(w.insert(b, ColliderBuilder::cuboid(0.5, 0.5, 0.5).restitution(0.0).friction(0.8).build()).0);
    }
    let mut asleep_at = None;
    let mut max_speed_after_64 = 0.0f64;
    for q in 1..=512 {
        w.step();
        if q > 64 {
            for h in &hs { max_speed_after_64 = max_speed_after_64.max(w.bodies[*h].linvel().length()); }
        }
        if asleep_at.is_none() && hs.iter().all(|h| w.bodies[*h].is_sleeping()) { asleep_at = Some(q); }
    }
    // Overlap of each interface from the body poses (floor top at y = 0, half-extent 0.5).
    let mut below = 0.0;
    let mut worst = 0.0f64;
    for h in &hs {
        let y = w.bodies[*h].translation().y;
        worst = worst.max(below - (y - 0.5));
        below = y + 0.5;
    }
    let sink = 3.5 - w.bodies[hs[3]].translation().y;
    format!("coefficient {coefficient}: all asleep at quantum {asleep_at:?}; max speed after quantum 64 {max_speed_after_64:.2e} m/s; top box sank {sink:.2e} m; deepest interface overlap {worst:.2e} m")
}

fn main() {
    println!("{}", run(1.0));
    println!("{}", run(0.0));
}
```
Expected output: `coefficient 1: all asleep at quantum Some(33); max speed after quantum 64 0.00e0 m/s; top box sank 2.71e-3 m; deepest interface overlap 1.23e-3 m coefficient 0: all asleep at quantum Some(50); max spe`

## Restore Rapier through serde-serialize or by replay: world bytes are stable and continue bit-exactly
**With serde-serialize, PhysicsWorld (physics_pipeline and ccd_solver skipped as workspace) round-trips byte-identically, the bytes match across processes and between x86_64 native and wasm32, and a deserialized world continues bit-exactly; the engine's build does not enable the feature.**

*Check 1: The oracle links rapier3d-f64 as the engine does: PhysicsWorld is not Serialize* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64, serde_json · errors: E0277 · **✔ oracle pass**
```rust
// The oracle links rapier3d-f64 exactly as the engine does (no serde-serialize):
// PhysicsWorld is then not Serialize.
use rapier3d_f64::prelude::*;
pub fn save(w: &PhysicsWorld) -> Vec<u8> {
    serde_json::to_vec(w).unwrap()
}
```

*Check 2: Cloning every set into a twin with a fresh pipeline and CCD solver continues bit-identically* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
// E0 control: clone every Rapier set, give the twin a fresh PhysicsPipeline and
// CCDSolver, step both, compare bits. If this is identical, the result-bearing
// state lives in the sets and the pipeline/CCD objects are workspace.
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;

fn world() -> PhysicsWorld {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = DT;
    w.integration_parameters.contact_clustering = false;
    w.integration_parameters.warmstart_coefficient = 1.0;
    let floor = RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)).build();
    w.insert(floor, ColliderBuilder::cuboid(5.0, 0.5, 5.0).friction(0.8).restitution(0.0).build());
    for i in 0..3 {
        let mut b = RigidBodyBuilder::dynamic()
            .translation(Vector::new(0.05 * i as f64, 0.5 + 1.05 * i as f64, 0.0))
            .can_sleep(true)
            .ccd_enabled(false)
            .build();
        b.set_rotation(Rotation::from_xyzw(0.0, 0.02 * i as f64, 0.0, 1.0).normalize(), false);
        b.activation_mut().time_until_sleep = 32.0 * DT;
        w.insert(b, ColliderBuilder::cuboid(0.5, 0.5, 0.5).friction(0.8).restitution(0.0).build());
    }
    w
}

fn twin(w: &PhysicsWorld) -> PhysicsWorld {
    PhysicsWorld {
        gravity: w.gravity,
        integration_parameters: w.integration_parameters,
        physics_pipeline: PhysicsPipeline::new(),
        islands: w.islands.clone(),
        broad_phase: w.broad_phase.clone(),
        narrow_phase: w.narrow_phase.clone(),
        bodies: w.bodies.clone(),
        colliders: w.colliders.clone(),
        impulse_joints: w.impulse_joints.clone(),
        multibody_joints: w.multibody_joints.clone(),
        ccd_solver: CCDSolver::new(),
    }
}

fn digest(w: &PhysicsWorld) -> u64 {
    let mut h = 0xcbf29ce484222325u64;
    let mut mix = |x: u64| h = (h ^ x).wrapping_mul(0x100000001b3);
    for (_, b) in w.bodies.iter() {
        let p = b.position();
        for v in [p.translation.x, p.translation.y, p.translation.z, p.rotation.x, p.rotation.y,
                  p.rotation.z, p.rotation.w, b.linvel().x, b.linvel().y, b.linvel().z,
                  b.angvel().x, b.angvel().y, b.angvel().z, b.activation().time_since_can_sleep] {
            mix(v.to_bits());
        }
        mix(b.is_sleeping() as u64);
    }
    for pair in w.narrow_phase.contact_pairs() {
        for m in pair.solver_manifolds() {
            for pt in &m.points {
                for v in [pt.data.warmstart_impulse, pt.data.warmstart_twist_impulse,
                          pt.data.warmstart_tangent_world.x, pt.data.warmstart_tangent_world.y,
                          pt.data.warmstart_tangent_world.z] {
                    mix(v.to_bits());
                }
            }
        }
    }
    h
}

fn main() {
    let mut a = world();
    for _ in 0..40 { a.step(); }
    let mut b = twin(&a);
    let mut first_diff = None;
    for s in 0..120 {
        a.step();
        b.step();
        if first_diff.is_none() && digest(&a) != digest(&b) { first_diff = Some(s); }
    }
    let asleep = a.bodies.iter().filter(|(_, b)| b.is_dynamic() && b.is_sleeping()).count();
    println!("twin first difference: {:?}; dynamic bodies asleep at the end: {}", first_diff, asleep);
}
```
Expected output: `twin first difference: None; dynamic bodies asleep at the end: 3`

## Treat rapier3d-f64 0.35.3 contact pairs as read-only: no public or hook path writes a manifold point
**NarrowPhase hands out only &ContactPair; InteractionGraph's *_mut needs &mut InteractionGraph, which is a private field; a MODIFY_SOLVER_CONTACTS hook gets &ContactManifold and SolverContacts with no warm-start fields.**

*Check 1: NarrowPhase has no contact_pairs_mut* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0599 · **✔ oracle pass**
```rust
// No mutable accessor on NarrowPhase; the graph accessor is shared.
use rapier3d_f64::prelude::*;
pub fn f(w: &mut PhysicsWorld) {
    for pair in w.narrow_phase.contact_pairs_mut() { pair.manifolds.clear(); }
}
```

*Check 2: contact_graph() is shared: interaction_pair_mut needs &mut* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0596 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;
pub fn f(w: &mut PhysicsWorld, a: ColliderGraphIndex, b: ColliderGraphIndex) {
    let _ = w.narrow_phase.contact_graph().interaction_pair_mut(a, b);
}
```

*Check 3: NarrowPhase::contact_graph field is private* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0616 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;
pub fn f(w: &mut PhysicsWorld) -> usize {
    w.narrow_phase.contact_graph.raw_graph().raw_edges().len()
}
```

*Check 4: A hook cannot write warm start: SolverContact has no warmstart_impulse* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0609 · **✔ oracle pass**
```rust
// A MODIFY_SOLVER_CONTACTS hook cannot carry warm-starts: SolverContact has no such field.
use rapier3d_f64::prelude::*;
struct Warm;
impl PhysicsHooks for Warm {
    fn modify_solver_contacts(&self, ctx: &mut ContactModificationContext) {
        for sc in ctx.solver_contacts.iter_mut() {
            sc.warmstart_impulse = 1.0;
        }
    }
}
pub fn hooks() -> impl PhysicsHooks { Warm }
```

*Check 5: A hook cannot write the manifold: ctx.manifold is behind &* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0596 · **✔ oracle pass**
```rust
// ...and the manifold (where the solver reads warm-starts) arrives as a shared reference.
use rapier3d_f64::prelude::*;
struct Warm;
impl PhysicsHooks for Warm {
    fn modify_solver_contacts(&self, ctx: &mut ContactModificationContext) {
        ctx.manifold.points[0].data.warmstart_impulse = 1.0;
    }
}
pub fn hooks() -> impl PhysicsHooks { Warm }
```

## Write restored sleep state after the load pass, never through wake_up=true setters
**set_linvel/set_angvel/set_translation/set_rotation/set_position(_, true) and wake_up(true) zero time_since_can_sleep; sleep() zeroes velocities; the IslandManager's persistent islands are pub(crate) history that no public call reads or writes.**

*Check 1: Which public setters zero time_since_can_sleep* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
// Which public setters touch the sleep timer (time_since_can_sleep)?
use rapier3d_f64::prelude::*;
fn body() -> RigidBody {
    let mut b = RigidBodyBuilder::dynamic().build();
    b.activation_mut().time_since_can_sleep = 0.25;
    b
}
fn main() {
    let v = Vector::new(1.0, 0.0, 0.0);
    let mut a = body(); a.set_linvel(v, false);
    let mut b = body(); b.set_linvel(v, true);
    let mut c = body(); c.set_translation(v, false);
    let mut d = body(); d.set_translation(v, true);
    let mut e = body(); e.wake_up(false);
    let mut f = body(); f.wake_up(true);
    let mut g = body(); g.set_linvel(v, false); g.sleep();
    println!("set_linvel(_, false) {} | set_linvel(_, true) {} | set_translation(_, false) {} | set_translation(_, true) {} | wake_up(false) {} | wake_up(true) {}",
        a.activation().time_since_can_sleep, b.activation().time_since_can_sleep, c.activation().time_since_can_sleep,
        d.activation().time_since_can_sleep, e.activation().time_since_can_sleep, f.activation().time_since_can_sleep);
    println!("sleep(): sleeping {} timer {} linvel {:?}", g.activation().sleeping, g.activation().time_since_can_sleep, g.linvel().to_array());
}
```
Expected output: `set_linvel(_, false) 0.25 / set_linvel(_, true) 0 / set_translation(_, false) 0.25 / set_translation(_, true) 0 / wake_up(false) 0.25 / wake_up(true) 0 sleep(): sleeping true timer 0.5 linvel [0.0, 0.`

*Check 2: IslandManager's persistent islands are not public* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0616 · **✔ oracle pass**
```rust
// The persistent islands (membership, split cooldowns, removal journal) are not public.
use rapier3d_f64::prelude::*;
pub fn peek(w: &PhysicsWorld) -> usize {
    w.islands.persistent.islands.len()
}
```

*Check 3: The load pass panics in a debug build of Rapier when a body touches at load* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 101 · **✔ oracle pass**
```rust
// The engine's load pass in a debug build of Rapier, with a box resting on the floor.
use rapier3d_f64::pipeline::CollisionPipeline;
use rapier3d_f64::prelude::*;
fn main() {
    let mut w = PhysicsWorld::new();
    let floor = RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)).build();
    w.insert(floor, ColliderBuilder::cuboid(5.0, 0.5, 5.0).build());
    w.insert(RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 0.5, 0.0)).build(),
             ColliderBuilder::cuboid(0.5, 0.5, 0.5).build());
    println!("before the pass");
    let p = w.integration_parameters.prediction_distance();
    CollisionPipeline::new().step(p, &mut w.islands, &mut w.broad_phase, &mut w.narrow_phase,
                                  &mut w.bodies, &mut w.colliders, &(), &());
    println!("after the pass");
}
```
Expected output: `before the pass`

