# restore-internals — Rapier state for restore (T2)

rapier3d-f64 0.35.3 with enhanced-determinism, rustc 1.98.1. Full evidence: `requests/answers-q1-q4.md`. Oracle: 19 checks over 10 recipes, 19 pass.

**Answers**

1. **Warm start.** No sound public path writes a manifold point: every accessor is `&self`, and hooks see `&ContactManifold`. A sound write would still not reproduce the next step, because the solver also reads frozen lever arms, contact points parry keeps across steps, recycle state and colours.
2. **Sleep.** `RigidBodyActivation` has six fields. `sleep_prev_pose` is `pub(crate)`, so the public fields cannot continue the timer. `IslandManager` keeps history the bodies do not: persistent islands, split cooldowns and epochs.
3. **Broad phase.** Yes. Tight versus fat leaves change the pair set, not only its order. Rebuilding the broad phase never deletes narrow-phase pairs. Enhanced-determinism makes iteration order a deterministic function of history; it does not make it a function of state.
4. **Serde.** Bytes are stable across runs and between x86_64 and wasm32, and the continuation is exact. The bytes are not canonical (they encode history), and they are locked to 0.35.3.

**Findings**

1. **NarrowPhase is read-only from outside, and the engine's cast is UB.** Rust project 2026 (std::ptr::from_ref, https://doc.rust-lang.org/stable/std/ptr/fn.from_ref.html). Implication: delete `solver_clear_warmstart`'s cast and the T2 branch's three. The oracle shows E0599, E0596, E0616 and E0609 for every public route.
2. **The solver reads more than the warm-start impulses.** Dimforge 2026 (ContactData, https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/geometry/struct.ContactData.html). Implication: a pin-1 restore with every warm-start field written soundly diverged on quantum 0, by up to 3.4e-5 m. Do not build restore on write-back.
3. **Colours set the Gauss–Seidel order, and colours follow history.** Dimforge 2026 (staged island solver, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/solver/staged_island_solver/mod.rs). Implication: swapping two pairs' colours changed quantum 0, and the load pass coloured a pair 0 where the running world had 1.
4. **`sleep_prev_pose` is crate-private.** Dimforge 2026 (rigid_body_components.rs, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/rigid_body_components.rs). Implication: rebuilding the activation from its public fields resets the timer ([20,6,6] became [0,0,0]). The load pass also wakes bodies, so never write sleep state before it.
5. **parry stores new BVH leaves tight.** Dimforge 2026 (bvh_insert.rs, https://docs.rs/crate/parry3d-f64/0.30.2/source/src/partitioning/bvh/bvh_insert.rs). Implication: a rebuilt world reports fewer pairs (1 against 0), so pin 1's count check refuses valid snapshots. Pin 6's per-step rebuild keeps a pair at 4.01 m.
6. **`warmstart_coefficient` acts inside every substep.** Dimforge 2026 (worker.rs, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/solver/staged_island_solver/worker.rs). Implication: runs at 1.0 and 0.0 part on quantum 1 with an empty cache, so they cannot replace the clear-then-step test. Coefficient 0 made a stack sink 13× deeper.
7. **Serde restores exactly.** Dimforge 2026 (Serialization guide, https://rapier.rs/docs/user_guides/rust/serialization/). Implication: a whole-world bincode blob gives the same bytes native and in wasm, and continues exactly through sleep and CCD. It adds 686 KB to the wasm. Never run the load pass after it; 0.36.0 cannot load it.
8. **Replay needs no writes.** Dimforge 2026 (Determinism guide, https://rapier.rs/docs/user_guides/templates/determinism/). Implication: keep one persistent world (route d) and restore by replay at t × ~74 µs. For T6, checkpoint by copying linear memory: 3.5 MB, about 2 ms, exact.

Recommendation: (d), plus a bytes-sensitivity test and a structural test in place of the clear test. Keep (c) in reserve.
