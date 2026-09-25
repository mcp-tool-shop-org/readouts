# Rapier 0.35: pipeline, determinism & upgrades — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](rapier-core.md) · [catalog index](README.md)

## Call PhysicsPipeline::step at 0.35.3 with its 12 arguments and read contacts as start-of-step state
**One 0.35.3 step applies queued user changes, runs broad and narrow phase once, solves and integrates per CCD substep, then only refreshes broad-phase AABBs; a non-finite body is quarantined, not reported as an error.**

*Check 1: the 0.35.3 step coerces to a 12-parameter fn pointer; &() serves as hooks and events* · `compiles` · edition 2021 · host · lib · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// The 0.35.3 step as a function pointer: gravity by value, the concrete BroadPhaseBvh,
// hooks and events as trait objects, and no SoftBodySet.
pub type Step = fn(
    &mut PhysicsPipeline,
    Vector,
    &IntegrationParameters,
    &mut IslandManager,
    &mut BroadPhaseBvh,
    &mut NarrowPhase,
    &mut RigidBodySet,
    &mut ColliderSet,
    &mut ImpulseJointSet,
    &mut MultibodyJointSet,
    &mut CCDSolver,
    &dyn PhysicsHooks,
    &dyn EventHandler,
);

pub const STEP: Step = PhysicsPipeline::step;

// `&()` satisfies both trait-object parameters (what PhysicsWorld::step passes).
pub fn no_hooks_no_events() -> (&'static dyn PhysicsHooks, &'static dyn EventHandler) {
    (&(), &())
}
```

*Check 2: the rapier.rs (Rust 0.36) guide's 13-argument step call does not compile against 0.35.3* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0433, E0061 · stderr has “this method takes 12 arguments but 13 arguments were supplied” · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// The step call as printed by the rapier.rs user guide, which documents Rust 0.36.
pub fn step_like_the_guide() {
    let gravity = Vector::new(0.0, -9.81, 0.0);
    let integration_parameters = IntegrationParameters::default();
    let mut physics_pipeline = PhysicsPipeline::new();
    let mut island_manager = IslandManager::new();
    let mut broad_phase = DefaultBroadPhase::new();
    let mut narrow_phase = NarrowPhase::new();
    let mut rigid_body_set = RigidBodySet::new();
    let mut collider_set = ColliderSet::new();
    let mut impulse_joint_set = ImpulseJointSet::new();
    let mut multibody_joint_set = MultibodyJointSet::new();
    let mut soft_body_set = SoftBodySet::new();
    let mut ccd_solver = CCDSolver::new();
    let physics_hooks = ();
    let event_handler = ();
    physics_pipeline.step(
        gravity,
        &integration_parameters,
        &mut island_manager,
        &mut broad_phase,
        &mut narrow_phase,
        &mut rigid_body_set,
        &mut collider_set,
        &mut impulse_joint_set,
        &mut multibody_joint_set,
        &mut soft_body_set,
        &mut ccd_solver,
        &physics_hooks,
        &event_handler,
    );
}
```

*Check 3: contacts after a step are start-of-step; the query BVH already has end-of-step poses* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

fn main() {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::ZERO;
    w.integration_parameters.dt = 1.0 / 64.0;
    let (_, wall) = w.insert(RigidBodyBuilder::fixed(), ColliderBuilder::cuboid(0.1, 1.0, 1.0));
    // Box face flush with the wall face, leaving at 20 units per second.
    let (h, bx) = w.insert(
        RigidBodyBuilder::dynamic()
            .translation(Vector::new(0.35, 0.0, 0.0))
            .linvel(Vector::new(20.0, 0.0, 0.0)),
        ColliderBuilder::cuboid(0.25, 0.25, 0.25),
    );
    for step in 1..=2 {
        w.step();
        let gap = w.bodies[h].translation().x - 0.25 - 0.1;
        let contact = w
            .narrow_phase
            .contact_pair(wall, bx)
            .is_some_and(|p| p.has_any_active_contact());
        // A ray from x = 2 back towards the wall meets the box's +x face.
        let ray = Ray::new(Vector::new(2.0, 0.0, 0.0), Vector::new(-1.0, 0.0, 0.0));
        let toi = w.query_pipeline().cast_ray(&ray, 10.0, false).map(|(_, t)| t).unwrap_or(-1.0);
        println!("after step {step}: gap={gap:.4} contact_active={contact} ray_toi={toi:.4}");
    }
}
```
Expected output: `after step 1: gap=0.3125 contact_active=true ray_toi=1.0875 after step 2: gap=0.6250 contact_active=false ray_toi=0.7750`

*Check 4: an infinite velocity is quarantined: body disabled, state finite, report gone next step* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

fn main() {
    let mut w = PhysicsWorld::new();
    w.integration_parameters.dt = 1.0 / 64.0;
    // An infinite velocity passes an `is_nan()` guard.
    let v = Vector::new(f64::INFINITY, 0.0, 0.0);
    println!("is_nan guard passes: {}", !v.x.is_nan());
    let (h, _) = w.insert(
        RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 2.0, 0.0)).linvel(v),
        ColliderBuilder::ball(0.5),
    );
    w.step();
    let b = &w.bodies[h];
    let (p, u) = (b.translation(), b.linvel());
    let finite = [p.x, p.y, p.z, u.x, u.y, u.z].iter().all(|x| x.is_finite());
    println!(
        "quarantined={} enabled={} state_finite={} y={} vx={}",
        w.quarantine().bodies().len(),
        b.is_enabled(),
        finite,
        p.y,
        u.x
    );
    w.step();
    println!("next step: reports={} y={}", w.quarantine().bodies().len(), w.bodies[h].translation().y);
}
```
Expected output: `is_nan guard passes: true quarantined=1 enabled=false state_finite=true y=2 vx=0 next step: reports=0 y=2`

## Collect Rapier 0.35.3 collision events with a Sync EventHandler and ActiveEvents set on a collider
**Collision and contact-force events are opt-in per collider (ActiveEvents, empty by default) and are delivered during the step to an EventHandler, which must be Sync unless the unsync-callbacks feature is on.**

*Check 1: a Cell-based EventHandler is rejected: EventHandler requires MaybeSync (= Sync) at 0.35.3* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0277 · stderr has “MaybeSync” · **✔ oracle pass**
```rust
use rapier3d_f64::geometry::ContactPair;
use rapier3d_f64::prelude::*;
use std::cell::Cell;

struct Counter {
    started: Cell<u32>,
}

impl EventHandler for Counter {
    fn handle_collision_event(&self, _b: &RigidBodySet, _c: &ColliderSet, event: CollisionEvent, _p: Option<&ContactPair>) {
        if event.started() {
            self.started.set(self.started.get() + 1);
        }
    }
    fn handle_contact_force_event(&self, _dt: Real, _b: &RigidBodySet, _c: &ColliderSet, _p: &ContactPair, _f: Real) {}
}
```

*Check 2: one Started and one Stopped with COLLISION_EVENTS, via atomics or the channel; none without* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::geometry::ContactPair;
use rapier3d_f64::prelude::*;
use std::sync::atomic::{AtomicU32, Ordering};
use std::sync::mpsc::channel;

// EventHandler requires Sync (MaybeSync without `unsync-callbacks`): count with atomics.
#[derive(Default)]
struct Counter {
    started: AtomicU32,
    stopped: AtomicU32,
}

impl EventHandler for Counter {
    fn handle_collision_event(&self, _b: &RigidBodySet, _c: &ColliderSet, event: CollisionEvent, _p: Option<&ContactPair>) {
        let n = if event.started() { &self.started } else { &self.stopped };
        n.fetch_add(1, Ordering::Relaxed);
    }
    fn handle_contact_force_event(&self, _dt: Real, _b: &RigidBodySet, _c: &ColliderSet, _p: &ContactPair, _f: Real) {}
}

// Drop a box on a floor, let it rest, then lift it clear: one touch starts and one stops.
fn run(events: ActiveEvents, handler: &dyn EventHandler) {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    w.insert(RigidBodyBuilder::fixed(), ColliderBuilder::cuboid(5.0, 0.1, 5.0));
    let (h, _) = w.insert(
        RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 1.0, 0.0)),
        ColliderBuilder::cuboid(0.25, 0.25, 0.25).active_events(events),
    );
    for _ in 0..64 {
        w.step_with_events(&(), handler);
    }
    w.bodies[h].set_translation(Vector::new(0.0, 3.0, 0.0), true);
    w.step_with_events(&(), handler);
}

fn main() {
    let counter = Counter::default();
    run(ActiveEvents::COLLISION_EVENTS, &counter);
    println!(
        "counter: started={} stopped={}",
        counter.started.load(Ordering::Relaxed),
        counter.stopped.load(Ordering::Relaxed)
    );

    let (tx, rx) = channel();
    let (ftx, _frx) = channel();
    run(ActiveEvents::COLLISION_EVENTS, &ChannelEventCollector::new(tx, ftx));
    let kinds: Vec<&str> = rx.try_iter().map(|e| if e.started() { "Started" } else { "Stopped" }).collect();
    println!("channel: {:?}", kinds);

    let quiet = Counter::default();
    run(ActiveEvents::empty(), &quiet);
    println!(
        "no ActiveEvents: started={} stopped={}",
        quiet.started.load(Ordering::Relaxed),
        quiet.stopped.load(Ordering::Relaxed)
    );
}
```
Expected output: `counter: started=1 stopped=1 channel: ["Started", "Stopped"] no ActiveEvents: started=0 stopped=0`

## Count Rapier 0.35.3 sleep in quanta: time_until_sleep = 32·dt sleeps after quantum 32, 33 off the origin
**Sleep is judged on displacement: each step a dynamic body whose half per-step drift is below normalized_linear_threshold·length_unit·dt adds dt to time_since_can_sleep (any other step resets it), and its island sleeps once time_since_can_sleep ≥ time_until_sleep.**

*Check 1: sleep quanta at dt = 1/64: 32 at the origin, 33 elsewhere, drift and angular thresholds* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// The quantum after which the body is asleep (None: still awake after 200), its x velocity
// and time_since_can_sleep at that point.
fn sleep_quantum(start: Vector, linvel: Vector, angvel: Vector, angular_threshold: f64, collider: bool) -> (Option<u32>, f64, f64) {
    let dt = 1.0 / 64.0;
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::ZERO;
    w.integration_parameters.dt = dt;
    let mut rb = RigidBodyBuilder::dynamic().translation(start).linvel(linvel).angvel(angvel).build();
    rb.activation_mut().time_until_sleep = 32.0 * dt; // SLEEP_QUANTA * DT in rapier_law.rs
    rb.activation_mut().angular_threshold = angular_threshold;
    let h = if collider {
        w.insert(rb, ColliderBuilder::cuboid(0.5, 0.5, 0.5)).0
    } else {
        w.insert_body(rb)
    };
    for q in 1..=200u32 {
        w.step();
        let b = &w.bodies[h];
        if b.is_sleeping() {
            return (Some(q), b.linvel().x, b.activation().time_since_can_sleep);
        }
    }
    let b = &w.bodies[h];
    (None, b.linvel().x, b.activation().time_since_can_sleep)
}

fn main() {
    let z = Vector::ZERO;
    let spin = Vector::new(0.0, 0.05, 0.0);
    println!("at rest at the origin: {:?}", sleep_quantum(z, z, z, 0.5, true));
    println!("at rest at (3, 1, 0): {:?}", sleep_quantum(Vector::new(3.0, 1.0, 0.0), z, z, 0.5, true));
    println!("drifting 0.08 u/s: {:?}", sleep_quantum(z, Vector::new(0.08, 0.0, 0.0), z, 0.5, true));
    println!("drifting 0.12 u/s: {:?}", sleep_quantum(z, Vector::new(0.12, 0.0, 0.0), z, 0.5, true));
    println!("spinning 0.05 rad/s, angular_threshold 0.01, collider: {:?}", sleep_quantum(z, z, spin, 0.01, true));
    println!("spinning 0.05 rad/s, angular_threshold 0.01, no collider: {:?}", sleep_quantum(z, z, spin, 0.01, false));
}
```
Expected output: `at rest at the origin: (Some(32), 0.0, 0.5) at rest at (3, 1, 0): (Some(33), 0.0, 0.5) drifting 0.08 u/s: (Some(32), 0.0, 0.5) drifting 0.12 u/s: (None, 0.12, 0.0) spinning 0.05 rad/s, angular_thresho`

## Expect Rapier 0.35.3 body types to gate contacts: kinematic-fixed off, kinematic pushes dynamic one way
**By default only pairs involving a dynamic body get contacts; kinematic bodies follow their next pose (position-based) or their velocity (velocity-based) and push dynamic bodies without being pushed; fixed bodies never move.**

*Check 1: kinematic-fixed contacts need KINEMATIC_FIXED; both kinematic kinds move; kinematic is not pushed* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

fn kinematic_vs_fixed(types: ActiveCollisionTypes) -> bool {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::ZERO;
    w.integration_parameters.dt = 1.0 / 64.0;
    let (_, wall) = w.insert(
        RigidBodyBuilder::fixed().translation(Vector::new(0.9, 0.0, 0.0)),
        ColliderBuilder::cuboid(0.5, 0.5, 0.5),
    );
    // Overlapping the wall by 0.1.
    let (_, kc) = w.insert(
        RigidBodyBuilder::kinematic_position_based(),
        ColliderBuilder::cuboid(0.5, 0.5, 0.5).active_collision_types(types),
    );
    for _ in 0..2 {
        w.step();
    }
    w.narrow_phase.contact_pair(wall, kc).is_some_and(|p| p.has_any_active_contact())
}

fn main() {
    println!("kinematic-fixed default: {}", kinematic_vs_fixed(ActiveCollisionTypes::default()));
    println!(
        "kinematic-fixed with KINEMATIC_FIXED: {}",
        kinematic_vs_fixed(ActiveCollisionTypes::default() | ActiveCollisionTypes::KINEMATIC_FIXED)
    );

    // Position-based: velocity derived from the next pose. Velocity-based: pose from velocity.
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::ZERO;
    w.integration_parameters.dt = 1.0 / 64.0;
    let (kp, _) = w.insert(RigidBodyBuilder::kinematic_position_based(), ColliderBuilder::cuboid(0.5, 0.5, 0.5));
    let (kv, _) = w.insert(
        RigidBodyBuilder::kinematic_velocity_based()
            .translation(Vector::new(0.0, 5.0, 0.0))
            .linvel(Vector::new(6.4, 0.0, 0.0)),
        ColliderBuilder::cuboid(0.5, 0.5, 0.5),
    );
    w.bodies[kp].set_next_kinematic_translation(Vector::new(0.1, 0.0, 0.0));
    w.step();
    println!("position-based: x={} vx={}", w.bodies[kp].translation().x, w.bodies[kp].linvel().x);
    println!("velocity-based: x={} vx={}", w.bodies[kv].translation().x, w.bodies[kv].linvel().x);

    // A kinematic body pushes a dynamic box and is not pushed back.
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::ZERO;
    w.integration_parameters.dt = 1.0 / 64.0;
    let (k, _) = w.insert(
        RigidBodyBuilder::kinematic_velocity_based().linvel(Vector::new(2.0, 0.0, 0.0)),
        ColliderBuilder::cuboid(0.5, 0.5, 0.5),
    );
    let (d, _) = w.insert(
        RigidBodyBuilder::dynamic().translation(Vector::new(1.2, 0.0, 0.0)),
        ColliderBuilder::cuboid(0.5, 0.5, 0.5),
    );
    for _ in 0..64 {
        w.step();
    }
    let kx = w.bodies[k].translation().x;
    println!(
        "kinematic after 64 steps: x={} vx={}; box pushed ahead by more than 0.99: {}",
        kx,
        w.bodies[k].linvel().x,
        w.bodies[d].translation().x > kx + 0.99
    );
}
```
Expected output: `kinematic-fixed default: false kinematic-fixed with KINEMATIC_FIXED: true position-based: x=0.1 vx=6.4 velocity-based: x=0.1 vx=6.4 kinematic after 64 steps: x=2 vx=2; box pushed ahead by more than 0.`

## Filter Rapier pairs with collision_groups (no contact) or solver_groups (contact, no force); flag the hooks
**collision_groups stop a pair before the narrow phase (no contacts, no events); solver_groups keep contacts and events but drop the forces; PhysicsHooks run only for pairs where a collider carries the matching ActiveHooks flag.**

*Check 1: collision_groups remove contact and events; solver_groups keep both and remove only forces* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;
use std::sync::mpsc::channel;

fn run(label: &str, collision: InteractionGroups, solver: InteractionGroups) {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    let floor_groups = InteractionGroups::new(Group::GROUP_1, Group::ALL, InteractionTestMode::And);
    let (_, floor) = w.insert(
        RigidBodyBuilder::fixed(),
        ColliderBuilder::cuboid(5.0, 0.1, 5.0).collision_groups(floor_groups).solver_groups(floor_groups),
    );
    let (h, bx) = w.insert(
        RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 1.0, 0.0)),
        ColliderBuilder::cuboid(0.25, 0.25, 0.25)
            .collision_groups(collision)
            .solver_groups(solver)
            .active_events(ActiveEvents::COLLISION_EVENTS),
    );
    let (tx, rx) = channel();
    let (ftx, _frx) = channel();
    let events = ChannelEventCollector::new(tx, ftx);
    let mut contact = false;
    for _ in 0..64 {
        w.step_with_events(&(), &events);
        contact |= w.narrow_phase.contact_pair(floor, bx).is_some_and(|p| p.has_any_active_contact());
    }
    let started = rx.try_iter().filter(|e| e.started()).count();
    println!("{label}: y={:.3} contact={} started={}", w.bodies[h].translation().y, contact, started);
}

fn main() {
    let all = InteractionGroups::all();
    // Member of group 2, interacts only with group 3: the floor (group 1) fails the And test.
    let not_floor = InteractionGroups::new(Group::GROUP_2, Group::GROUP_3, InteractionTestMode::And);
    run("default", all, all);
    run("collision_groups", not_floor, all);
    run("solver_groups", all, not_floor);
}
```
Expected output: `default: y=0.350 contact=true started=1 collision_groups: y=-3.016 contact=false started=0 solver_groups: y=-3.016 contact=true started=1`

*Check 2: a refusing filter_contact_pair hook acts only on colliders flagged FILTER_CONTACT_PAIRS* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// A hook that refuses every contact pair it is asked about.
struct Ghost;
impl PhysicsHooks for Ghost {
    fn filter_contact_pair(&self, _ctx: &PairFilterContext) -> Option<SolverFlags> {
        None
    }
}

fn drop_box(hooks: ActiveHooks) -> f64 {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    w.insert(RigidBodyBuilder::fixed(), ColliderBuilder::cuboid(5.0, 0.1, 5.0));
    let (h, _) = w.insert(
        RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 1.0, 0.0)),
        ColliderBuilder::cuboid(0.25, 0.25, 0.25).active_hooks(hooks),
    );
    for _ in 0..64 {
        w.step_with_events(&Ghost, &());
    }
    w.bodies[h].translation().y
}

fn main() {
    println!("hook flag off: y={:.3}", drop_box(ActiveHooks::empty()));
    println!("FILTER_CONTACT_PAIRS on: y={:.3}", drop_box(ActiveHooks::FILTER_CONTACT_PAIRS));
}
```
Expected output: `hook flag off: y=0.350 FILTER_CONTACT_PAIRS on: y=-3.016`

*Check 3: the guide's FILTER_CONTACT_PAIR and the doc example's 2-argument groups do not compile* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0599, E0061 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// The user guide's prose spells this flag in the singular.
pub fn flags() -> ActiveHooks {
    ActiveHooks::FILTER_CONTACT_PAIR | ActiveHooks::MODIFY_SOLVER_CONTACTS
}

// The two-argument form printed in the ColliderBuilder::collision_groups doc example.
pub fn groups() -> InteractionGroups {
    InteractionGroups::new(Group::GROUP_1, Group::GROUP_2)
}
```

## Govern a rapier3d-f64 bump: pin =0.35.3, read every CHANGELOG entry to the target, rerun course and goldens
**Most Rapier releases from 0.30 to 0.36.0 changed simulation behaviour, patch releases included (0.30.1, 0.35.2, 0.35.3), and 0.36.0 (on crates.io since 2026-09-25) breaks the API this engine calls, so a bump is a law change gated by the outcome course and the goldens.**

*Check 1: tripwire: the 0.35.3 surface rapier_law.rs uses that 0.36.0 changes compiles today* · `compiles` · edition 2021 · host · lib · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::geometry::{ContactManifold, ContactPair};
use rapier3d_f64::prelude::*;
use std::sync::mpsc::Sender;

// rebuild_snapshot and solver_clear_warmstart read and write these pub fields;
// 0.36.0 moves `manifolds` and `solver_clusters` into ContactPair::contacts.
pub fn warmstart_sources(pair: &mut ContactPair) -> (usize, &mut Vec<ContactManifold>) {
    let n = pair.solver_clusters.len() + pair.solver_manifolds().len();
    (n, &mut pair.manifolds)
}

// A handler with exactly the two 0.35.3 methods; 0.36.0 adds a required third.
pub struct Quiet;
impl EventHandler for Quiet {
    fn handle_collision_event(&self, _: &RigidBodySet, _: &ColliderSet, _: CollisionEvent, _: Option<&ContactPair>) {}
    fn handle_contact_force_event(&self, _: Real, _: &RigidBodySet, _: &ColliderSet, _: &ContactPair, _: Real) {}
}

// Two senders at 0.35.3; 0.36.0 takes a third for soft-body tear events.
pub fn collector(c: Sender<CollisionEvent>, f: Sender<ContactForceEvent>) -> ChannelEventCollector {
    ChannelEventCollector::new(c, f)
}

// The 12-argument step (0.36.0 inserts a SoftBodySet).
pub fn step(w: &mut PhysicsWorld) {
    w.physics_pipeline.step(
        w.gravity,
        &w.integration_parameters,
        &mut w.islands,
        &mut w.broad_phase,
        &mut w.narrow_phase,
        &mut w.bodies,
        &mut w.colliders,
        &mut w.impulse_joints,
        &mut w.multibody_joints,
        &mut w.ccd_solver,
        &(),
        &(),
    );
}
```

## Hold Rapier to its stated determinism terms: same build and inputs, enhanced-determinism, same insertion order
**Rapier promises identical reruns on one machine with the same Rapier and Rust versions and the same initial conditions, and cross-platform identity only with enhanced-determinism, IEEE 754-2008 targets and identical insertion order; nothing is promised across Rapier versions.**

*Check 1: same insertion order: bit-identical after 200 steps; reversed insertion order: different* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// FNV-1a over the final bits of four boxes, read in scene order (not handle order).
fn pile(order: &[usize]) -> u64 {
    let starts = [
        Vector::new(0.00, 0.40, 0.00),
        Vector::new(0.13, 0.95, 0.07),
        Vector::new(-0.11, 1.50, 0.05),
        Vector::new(0.05, 2.05, -0.12),
    ];
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    w.insert(RigidBodyBuilder::fixed(), ColliderBuilder::cuboid(5.0, 0.1, 5.0));
    let mut handles = [RigidBodyHandle::invalid(); 4];
    for &i in order {
        let (h, _) = w.insert(RigidBodyBuilder::dynamic().translation(starts[i]), ColliderBuilder::cuboid(0.25, 0.25, 0.25));
        handles[i] = h;
    }
    for _ in 0..200 {
        w.step();
    }
    let mut h = 0xcbf29ce484222325u64;
    for hd in handles {
        let b = &w.bodies[hd];
        let (p, q) = (b.translation(), b.rotation());
        for x in [p.x, p.y, p.z, q.x, q.y, q.z, q.w] {
            for byte in x.to_bits().to_le_bytes() {
                h = (h ^ byte as u64).wrapping_mul(0x100000001b3);
            }
        }
    }
    h
}

fn main() {
    let a = pile(&[0, 1, 2, 3]);
    println!("same order twice identical: {}", a == pile(&[0, 1, 2, 3]));
    println!("reversed insertion order identical: {}", a == pile(&[3, 2, 1, 0]));
}
```
Expected output: `same order twice identical: true reversed insertion order identical: false`

## Pin rapier3d-f64 0.35.3 features explicitly: block-solver is a default and docs.rs documents other builds
**rapier3d-f64 0.35.3 has 15 features; the defaults are dim3, f64, std (which enables alloc) and block-solver; it has no simd-stable, simd-nightly or simd8 feature, and docs.rs documents a parallel + serde-serialize + debug-render build.**

*Check 1: the linked crate reports rapier3d_f64::VERSION = 0.35.3* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
fn main() {
    println!("{}", rapier3d_f64::VERSION);
}
```
Expected output: `0.35.3`

*Check 2: docs.rs shows configure_thread_pool (parallel build); the pinned build lacks it: E0599* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0599 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// Documented on docs.rs, which builds rapier3d-f64 with `parallel`; absent without it.
pub fn pool(p: &mut PhysicsPipeline) {
    let _ = p.configure_thread_pool(2);
}
```

*Check 3: without serde-serialize IntegrationParameters is not Serialize: E0277* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64, serde_json · errors: E0277 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// IntegrationParameters derives Serialize only under `serde-serialize`.
pub fn save(p: &IntegrationParameters) -> String {
    serde_json::to_string(p).unwrap()
}
```

## Read rapier3d-f64 0.35.3 IntegrationParameters defaults from code: prediction 0.02, slop 0.005, CCD on
**The 0.35.3 defaults that decide results are prediction 0.02, allowed error 0.005, 4 solver iterations, 30 Hz / ζ 10 contacts (60 Hz against fixed bodies), CCD and contact recycling on, and two doc comments still state the pre-0.35 values.**

*Check 1: IntegrationParameters::default() at 0.35.3: prediction 0.02, allowed error 0.005, CCD 1* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

fn main() {
    let p = IntegrationParameters::default();
    println!("dt={} min_ccd_dt={}", p.dt, p.min_ccd_dt);
    println!(
        "num_solver_iterations={} num_internal_pgs_iterations={} num_internal_stabilization_iterations={}",
        p.num_solver_iterations, p.num_internal_pgs_iterations, p.num_internal_stabilization_iterations
    );
    println!(
        "warmstart_coefficient={} warmstart_joints={} length_unit={}",
        p.warmstart_coefficient, p.warmstart_joints, p.length_unit
    );
    println!(
        "contact_softness={}Hz/{} static_contact_softness={}Hz/{}",
        p.contact_softness.natural_frequency,
        p.contact_softness.damping_ratio,
        p.static_contact_softness.natural_frequency,
        p.static_contact_softness.damping_ratio
    );
    println!(
        "normalized_allowed_linear_error={} allowed_linear_error()={}",
        p.normalized_allowed_linear_error,
        p.allowed_linear_error()
    );
    println!(
        "normalized_prediction_distance={} prediction_distance()={}",
        p.normalized_prediction_distance,
        p.prediction_distance()
    );
    println!(
        "normalized_max_corrective_velocity={} normalized_max_linear_velocity={}",
        p.normalized_max_corrective_velocity, p.normalized_max_linear_velocity
    );
    println!(
        "max_ccd_substeps={} contact_clustering={} contact_recycling={} normalized_contact_recycle_distance={}",
        p.max_ccd_substeps, p.contact_clustering, p.contact_recycling, p.normalized_contact_recycle_distance
    );
    println!("friction_in_bias_pass={} friction_model={:?}", p.friction_in_bias_pass, p.friction_model);
}
```
Expected output: `dt=0.016666666666666666 min_ccd_dt=0.00016666666666666666 num_solver_iterations=4 num_internal_pgs_iterations=1 num_internal_stabilization_iterations=1 warmstart_coefficient=1 warmstart_joints=false l`

*Check 2: fields older tutorials set (min_island_size, contact_natural_frequency) are gone: E0609* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0609 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// Two fields older tutorials set. Neither exists at 0.35.3.
pub fn tune(p: &mut IntegrationParameters) {
    p.min_island_size = 128; // removed in 0.35.0-beta.0 (single active set)
    p.contact_natural_frequency = 30.0; // grouped into contact_softness in 0.31
}
```

*Check 3: ccd_enabled(false) is still swept against a fixed slab; max_ccd_substeps = 0 turns CCD off* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// A 0.05-half box at 20 units/s (0.3125 per 1/64 s step) toward a fixed slab of
// half-thickness 0.02 at x = 1. From x = -0.1 its positions jump the slab between steps.
fn shoot(max_ccd_substeps: usize, ccd_enabled: bool) -> f64 {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::ZERO;
    w.integration_parameters.dt = 1.0 / 64.0;
    w.integration_parameters.max_ccd_substeps = max_ccd_substeps;
    w.insert(
        RigidBodyBuilder::fixed().translation(Vector::new(1.0, 0.0, 0.0)),
        ColliderBuilder::cuboid(0.02, 2.0, 2.0),
    );
    let (h, _) = w.insert(
        RigidBodyBuilder::dynamic()
            .translation(Vector::new(-0.1, 0.0, 0.0))
            .linvel(Vector::new(20.0, 0.0, 0.0))
            .ccd_enabled(ccd_enabled),
        ColliderBuilder::cuboid(0.05, 0.05, 0.05),
    );
    for _ in 0..16 {
        w.step();
    }
    w.bodies[h].translation().x
}

fn main() {
    for (substeps, ccd) in [(1, false), (0, false), (0, true), (1, true)] {
        println!("max_ccd_substeps={} ccd_enabled={}: x={:.3}", substeps, ccd, shoot(substeps, ccd));
    }
}
```
Expected output: `max_ccd_substeps=1 ccd_enabled=false: x=0.921 max_ccd_substeps=0 ccd_enabled=false: x=4.900 max_ccd_substeps=0 ccd_enabled=true: x=4.900 max_ccd_substeps=1 ccd_enabled=true: x=0.921`

*Check 4: contact_recycling changes result bits on a box pile; contact_clustering does not there* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// FNV-1a over the bit patterns of four boxes after 200 steps of a small pile.
fn pile(recycling: bool, clustering: bool) -> u64 {
    let starts = [
        Vector::new(0.00, 0.40, 0.00),
        Vector::new(0.13, 0.95, 0.07),
        Vector::new(-0.11, 1.50, 0.05),
        Vector::new(0.05, 2.05, -0.12),
    ];
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    w.integration_parameters.contact_recycling = recycling;
    w.integration_parameters.contact_clustering = clustering;
    w.insert(RigidBodyBuilder::fixed(), ColliderBuilder::cuboid(5.0, 0.1, 5.0));
    let hs: Vec<RigidBodyHandle> = starts
        .iter()
        .map(|s| {
            w.insert(RigidBodyBuilder::dynamic().translation(*s), ColliderBuilder::cuboid(0.25, 0.25, 0.25)).0
        })
        .collect();
    for _ in 0..200 {
        w.step();
    }
    let mut h = 0xcbf29ce484222325u64;
    for hd in &hs {
        let b = &w.bodies[*hd];
        let (p, q) = (b.translation(), b.rotation());
        for x in [p.x, p.y, p.z, q.x, q.y, q.z, q.w] {
            for byte in x.to_bits().to_le_bytes() {
                h = (h ^ byte as u64).wrapping_mul(0x100000001b3);
            }
        }
    }
    h
}

fn main() {
    let base = pile(true, false);
    println!("recycling on vs off identical: {}", base == pile(false, false));
    println!("clustering on vs off identical: {}", base == pile(true, true));
}
```
Expected output: `recycling on vs off identical: false clustering on vs off identical: true`

## Warm Rapier's broad phase with one CollisionPipeline::step at load, then re-mark bodies with iter_mut
**A hand-run BroadPhaseBvh::update whose pair events are dropped loses those pairs for good; CollisionPipeline::step registers them, but at 0.35.3 it leaves every body outside the IslandManager, so bodies must be re-marked modified before the first PhysicsPipeline step.**

*Check 1: E3: a hand-updated broad phase with dropped events lets a box fall through a rotated slab* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::pipeline::CollisionPipeline;
use rapier3d_f64::prelude::*;

// A box above the centre of a slab rotated 0.3 rad about z: their AABBs overlap at load.
fn world() -> (PhysicsWorld, RigidBodyHandle, Vec<ColliderHandle>) {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    let slab = RigidBodyBuilder::fixed().rotation(Vector::new(0.0, 0.0, 0.3)).build();
    let (_, c1) = w.insert(slab, ColliderBuilder::cuboid(3.0, 0.1, 1.0));
    let (h, c2) = w.insert(
        RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 0.6, 0.0)),
        ColliderBuilder::cuboid(0.25, 0.25, 0.25),
    );
    (w, h, vec![c1, c2])
}

fn main() {
    // The pre-E3 load: update the broad phase by hand and drop its pair events.
    let (mut w, h, cols) = world();
    let mut events = Vec::new();
    let params = w.integration_parameters;
    w.broad_phase.update(&params, &w.colliders, &w.bodies, &cols, &[], &mut events);
    let discarded = events.len();
    for _ in 0..128 {
        w.step();
    }
    println!(
        "hand_update: discarded={} y={:.3} pairs={}",
        discarded,
        w.bodies[h].translation().y,
        w.narrow_phase.contact_pairs().count()
    );

    // The E3 fix: one CollisionPipeline pass, then re-mark the bodies.
    let (mut w, h, _) = world();
    let prediction = w.integration_parameters.prediction_distance();
    CollisionPipeline::new().step(
        prediction,
        &mut w.islands,
        &mut w.broad_phase,
        &mut w.narrow_phase,
        &mut w.bodies,
        &mut w.colliders,
        &(),
        &(),
    );
    for (_, b) in w.bodies.iter_mut() {
        if !b.is_fixed() {
            b.wake_up(true);
        }
    }
    for _ in 0..128 {
        w.step();
    }
    println!(
        "pipeline_pass: y={:.3} pairs={}",
        w.bodies[h].translation().y,
        w.narrow_phase.contact_pairs().count()
    );
}
```
Expected output: `hand_update: discarded=1 y=-15.431 pairs=0 pipeline_pass: y=0.309 pairs=1`

*Check 2: the pass leaves bodies unadmitted: iter_mut re-admits, PhysicsWorld::wake_up does not* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::pipeline::CollisionPipeline;
use rapier3d_f64::prelude::*;

fn world() -> (PhysicsWorld, RigidBodyHandle) {
    let mut w = PhysicsWorld::new();
    w.gravity = Vector::new(0.0, -8.0, 0.0);
    w.integration_parameters.dt = 1.0 / 64.0;
    w.insert(RigidBodyBuilder::fixed(), ColliderBuilder::cuboid(5.0, 0.1, 5.0));
    let (h, _) = w.insert(
        RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 2.0, 0.0)),
        ColliderBuilder::cuboid(0.25, 0.25, 0.25),
    );
    (w, h)
}

fn collision_pass(w: &mut PhysicsWorld) {
    let prediction = w.integration_parameters.prediction_distance();
    CollisionPipeline::new().step(
        prediction,
        &mut w.islands,
        &mut w.broad_phase,
        &mut w.narrow_phase,
        &mut w.bodies,
        &mut w.colliders,
        &(),
        &(),
    );
}

fn ray_hits(w: &PhysicsWorld) -> bool {
    let ray = Ray::new(Vector::new(0.0, 5.0, 0.0), Vector::new(0.0, -1.0, 0.0));
    w.query_pipeline().cast_ray(&ray, 10.0, true).is_some()
}

fn fall(mut w: PhysicsWorld, h: RigidBodyHandle, label: &str) {
    for _ in 0..10 {
        w.step();
    }
    println!("{label}: y={:.4}", w.bodies[h].translation().y);
}

fn main() {
    let (w, h) = world();
    println!("ray before any pass hits: {}", ray_hits(&w));
    fall(w, h, "no pass, plain steps");

    let (mut w, h) = world();
    collision_pass(&mut w);
    println!("ray after the collision pass hits: {}", ray_hits(&w));
    fall(w, h, "pass only");

    let (mut w, h) = world();
    collision_pass(&mut w);
    for (_, _b) in w.bodies.iter_mut() {}
    fall(w, h, "pass + bodies.iter_mut()");

    let (mut w, h) = world();
    collision_pass(&mut w);
    for (_, b) in w.bodies.iter_mut() {
        if !b.is_fixed() {
            b.wake_up(true);
        }
    }
    fall(w, h, "pass + iter_mut + wake_up(true), as warm_broadphase");

    let (mut w, h) = world();
    collision_pass(&mut w);
    w.wake_up(h, true);
    fall(w, h, "pass + PhysicsWorld::wake_up(h, true)");
}
```
Expected output: `ray before any pass hits: false no pass, plain steps: y=1.8999 ray after the collision pass hits: true pass only: y=2.0000 pass + bodies.iter_mut(): y=1.8999 pass + iter_mut + wake_up(true), as warm_b`

*Check 3: the load pass with a body touching the floor panics in a debug-assertion build (exit 101)* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 101 · **✔ oracle pass**
```rust
use rapier3d_f64::pipeline::CollisionPipeline;
use rapier3d_f64::prelude::*;

fn main() {
    let mut w = PhysicsWorld::new();
    w.integration_parameters.dt = 1.0 / 64.0;
    w.insert(RigidBodyBuilder::fixed(), ColliderBuilder::cuboid(5.0, 0.1, 5.0));
    // A box resting on the floor at load: its bottom face on the floor's top face.
    w.insert(
        RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 0.35, 0.0)),
        ColliderBuilder::cuboid(0.25, 0.25, 0.25),
    );
    println!("load pass, one dynamic body resting on the floor");
    let prediction = w.integration_parameters.prediction_distance();
    CollisionPipeline::new().step(
        prediction,
        &mut w.islands,
        &mut w.broad_phase,
        &mut w.narrow_phase,
        &mut w.bodies,
        &mut w.colliders,
        &(),
        &(),
    );
    println!("not reached while rapier is built with debug assertions");
}
```
Expected output: `load pass, one dynamic body resting on the floor`

