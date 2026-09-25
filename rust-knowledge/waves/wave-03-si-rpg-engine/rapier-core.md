# rapier-core: Rapier 0.35 pipeline, determinism & upgrades

**Q1. What does one step do at 0.35.3?** `PhysicsPipeline::step` takes 12 arguments. Gravity is passed by value and hooks and events as `&dyn`; everything else is `&mut` sets and a concrete `BroadPhaseBvh`. The step applies user changes, runs the broad and narrow phase once, solves and integrates per CCD substep, and ends by refreshing only the broad-phase AABBs.

**Q2. What does Rapier promise, and how should a bump be governed?** It promises identical reruns on the same build, compiler and inputs. Cross-platform identity needs `enhanced-determinism`, IEEE 754-2008 targets and the same insertion order. Nothing is promised across versions. Pin `=0.35.3`, read the changelog, and rerun the T4 course before any golden moves.

1. **Contacts lag integration by one step.** dimforge 2026 (substep.rs, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/pipeline/physics_pipeline/substep.rs). Measured: a box 0.3125 clear of a wall still has an active contact. Implication: `rebuild_snapshot` hashes start-of-step contacts. Document this.

2. **Rapier quarantines non-finite state instead of failing.** dimforge 2026 (CHANGELOG v0.36.0, https://github.com/dimforge/rapier/blob/v0.36.0/CHANGELOG.md). Measured: an infinite velocity passes `is_nan()`, and Rapier leaves the body disabled, finite and frozen. Implication: `bad()` must reject non-finite values, and `integrate` should refuse the step when `world.quarantine()` is non-empty.

3. **Two doc comments still give pre-0.35 defaults.** dimforge 2026 (IntegrationParameters, https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/dynamics/struct.IntegrationParameters.html). The code's defaults are prediction 0.02 and allowed error 0.005. `contact_recycling` changes the result bits. Implication: record the law's parameters from the code.

4. **`ccd_enabled(false)` leaves CCD on.** dimforge 2026 (CHANGELOG v0.35.3, https://github.com/dimforge/rapier/blob/v0.35.3/CHANGELOG.md). Measured: T4's thin fast body stops at the slab under the default `max_ccd_substeps = 1`, and passes only at 0. Implication: measure T4 pin 2's premise before moving goldens.

5. **Sleep counts exact quanta, one quantum later off the origin.** dimforge 2026 (rigid_body_components.rs, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/rigid_body_components.rs). Measured with 32·dt: a body at the origin sleeps after quantum 32, one at (3, 1, 0) after 33. A body drifting at 0.08 u/s is stopped. Implication: a body at rest from load sleeps after quantum 33.

6. **The E3 fix works for a reason its comment does not name.** dimforge 2026 (collision_pipeline.rs, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/pipeline/collision_pipeline.rs). Measured:
   - A broad phase updated by hand drops a box through the slab.
   - After the collision pass, `iter_mut()` re-admits the bodies and `PhysicsWorld::wake_up` does not.
   - A body touching geometry at load trips a debug assertion.

   Implication: correct the comment in `warm_broadphase` and test T2 in release builds.

7. **Solver groups keep contacts; collision groups do not.** dimforge 2026 (PhysicsHooks, https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/pipeline/trait.PhysicsHooks.html). Measured: `solver_groups` keep contacts and events, `collision_groups` remove both, and hooks need an `ActiveHooks` flag. Implication: groups belong in the world file and the geometry hash.

8. **Insertion order changes the result bits.** dimforge 2026 (Determinism, https://rapier.rs/docs/user_guides/rust/determinism). Measured on reversed insertion. Implication: T3's insertion-order test should fail, as intended.

9. **0.36.0 (2026-09-25) breaks the engine's code.** dimforge 2026 (CHANGELOG v0.36.0). `step` takes a `SoftBodySet`, the `ContactPair` fields the engine writes have moved, and rapier.rs now documents only 0.36. Implication: pin `=0.35.3` and read docs.rs 0.35.3.

**Where evidence is thin:**
- The order of events from simultaneous contacts was not measured.
- That the release load pass is harmless is inferred from `#[cfg(debug_assertions)]`, not run.
- The restore effects of `sleep_prev_pose` and contact recycling are inferred.
- The CCD numbers belong to binary-and-limits.
