Route costs for T2 (restore): (a) `warmstart_coefficient = 0`, (c) a serde round trip of Rapier's state. rapier3d-f64 0.35.3 with `enhanced-determinism`, rustc 1.98.1. Measured 2026-09-25.

**Host.** Windows 11 Pro 10.0.26340, x86_64: Intel Core Ultra 9 285K, 24 logical CPUs, 63.4 GB. The machine is a shared desktop with other processes running.

**Toolchain.** `rustc +1.98.1` (48a229cea 2026-09-01, LLVM 22.1.8, host `x86_64-pc-windows-msvc`), node v22.22.3 (V8).

**Dependencies.**
- The harness lock started from `solver/Cargo.lock`. Every package the solver pins resolved to the same version: rapier3d-f64 0.35.3, parry3d-f64 0.30.2.
- Route (c) adds serde, bincode 1.3.3 and serde_json 1.0.151 (`float_roundtrip`, `arbitrary_precision`).

**Engine state.**
- `main` is GitHub `d5b735b`. The local `solver/` is byte-identical to it apart from CRLF.
- T2 is `slice-t2-restore` at `ee2e50a`.
- Nothing was written, built or executed inside `E:/AI/si-rpg-engine`. The only commands run there were read-only `git branch -a` and `git log`; branch files came through `gh api`.

**Scratch.** Everything lives under `<scratchpad>/route-costs/`, a session scratch directory that is not kept in this repo, called `$S` below. It holds the harness, the solver copies, the node drivers and the raw outputs in `$S/out/`.

## Cost summary

| route | soundness | fidelity to Rapier's own warm start | per-quantum cost | restore cost |
|---|---|---|---|---|
| **(a) coefficient 0** | Sound. Nothing is written. At 0, the stored impulses change no bits (two checks, 10,000 quanta, 3 scenes). | None. 0 also switches off the warm start between Rapier's 4 substeps (see [Why 0 costs more](#why-0-costs-more-than-dropping-the-carry)). The 5-stack stops 3.7–3.8e-2 interpenetrated, 5.5–5.6e-2 low and leaning 5.8–7.9e-2. At 1.0 these are ≤2.3e-3, ≤5.1e-3 and ≤1.5e-3. Kept awake, it falls over (q759 in T2's regime, q4991 in main's). | An awake 5-stack step costs 6–9% less: 6.8–7.3 µs against 7.5–7.8 µs, native, because the warm-start stage is skipped. | A rebuild, with nothing to carry. The snapshot drops 7 floats per contact point. |
| **(c) serde** | Sound. Safe Rust only: derived `Serialize`/`Deserialize`, plus assignment of the public field `PhysicsWorld::narrow_phase`. | Exact. See [below](#fidelity-of-route-c). | Under V8: +3–6 µs on the 5-stack and +0.22–0.26 ms on 64 boxes (484 pairs). Wasm grows by 82,579 B (+5.4%). | Under V8, T2's restore gets 9 µs slower on 5 boxes and 0.28 ms slower on 64. As Rapier's own snapshot instead: the 768 KB NarrowPhase loads in 0.12–0.14 ms native and 0.15–0.17 ms under V8 (+84 KB wasm). The whole 874 KB world loads in 0.17–0.19 ms native and 0.20 ms under V8 (+640 KB wasm). |

<a id="fidelity-of-route-c"></a>**Fidelity of route (c).**
- **As the per-quantum carry.** The streamed rewrite matches T2's pointer carry at every quantum for 10,000 quanta: 3 scenes, native and in wasm, with sleep on and off. T2's own restore-then-rerun test passes with it.
- **As a snapshot.** NarrowPhase and whole-world round trips are bit-exact and rerun bit-identically.

What decides between them:
- **Route (a) is sound but visible.** It costs every 3- and 5-box stack a visible sink and lean. The loss is larger than dropping the carry, because the coefficient also governs the warm start between substeps.
- **A third option came up on the way: coefficient 1 with no carry.** T2's fresh world starts every point at zero, so nothing needs writing and it is sound. It is still visibly worse than the carry: kept awake, the 5-stack collapses from q3453 and the 3-stack walks 0.57 in 10,000 quanta.
- **Route (c) delivers T2's current behaviour exactly, with no `unsafe` write.** It rebuilds the whole NarrowPhase each quantum, so its cost scales with every pair and point, not with the points that changed.
- **Unrelated to either route:** T2's `restore` refuses valid snapshots. See [Incidental: T2's restore refuses its own snapshot](#incidental-t2s-restore-refuses-its-own-snapshot).

## Method

**Scenes.** One static slab: an engine collider record with x, z in [−5, 5] and y in [−0.5, 0], so its top face is y = 0. Unit cuboids (half-extent 0.5) sit at x = z = 0 with identity rotation, dropped from rest with every interface open by 0.01. Box k starts at y = 0.51 + 1.01·k. The scenes are 1 box, 3 boxes and 5 boxes, run for 10,000 quanta. Lengths are world units, and one box is 1 unit wide.

**Parameters.** These are the engine's own:
- dt = 1/64 and gravity (0, −8, 0).
- `contact_clustering = false`, and `warmstart_coefficient` is 1.0 or 0.0.
- Every other `IntegrationParameters` field is its default, including `num_solver_iterations = 4`, 1 PGS iteration and 1 stabilization iteration (`integration_parameters.rs:386-389`), and the `Simplified` friction model (`FrictionModel`'s `#[default]`, `integration_parameters.rs:24-25`).
- Colliders use friction 0.8 and restitution 0.
- Dynamic bodies use `ccd_enabled(false)` and `can_sleep(true)`, with `time_until_sleep = 32·dt`.
- The load runs `warm_broadphase` as written.

**Two regimes.** The harness (`$S/harness`) ports both the relevant code paths:
- **main:** one persistent world with Rapier's own sleep timer. This is `solver/src/rapier_law.rs` on `main`.
- **T2:** every quantum builds a fresh world from the state the last one ended in. Rapier's thresholds are set to −1, and the law's `settle` counts quiet quanta and puts islands to sleep. The warm-start impulses are carried by pair, subshape and fid1/fid2. This is `rapier_law.rs` at `ee2e50a`: `build_world`, `warm_broadphase`, `settle`, `carry_warmstart`, restricted to dynamic cuboids on cuboid statics.

**The ports are the engine.** Each regime's port was compared with the engine's own wasm under node. The comparison is a canonical record hash over x, y, z, v, q, w for every body, taken every quantum. The binaries were built from scratch copies with their unmodified `build.mjs`, so RUSTFLAGS were `-C target-feature=-relaxed-simd` plus the three `--remap-path-prefix` flags. All pairs were identical at every quantum:

| port | binary | coefficient | scenes and quanta |
|---|---|---|---|
| main | `v0` (main) | 1.0 | n = 1, 3, 5: 2,000 quanta; n = 5: 10,000 quanta |
| main | `v0c0` (main with `= 0.0`) | 0.0 | n = 1, 3, 5: 10,000 quanta |
| T2 | `t2` (the branch) | 1.0 | n = 1, 3, 5: 10,000 quanta |
| T2 | `t2c0` (branch with `= 0.0`) | 0.0 | n = 1, 3, 5: 10,000 quanta |

So the native numbers below are also what the engine computes under V8.

**Independent check (compile oracle).**
- **Why the check moved scenes.** `compile_oracle.py` links rapier built in debug. On the 0.01 scene, rapier aborts in the load pass at `debug_assert!` `dynamics/island_manager/manager.rs:140`, because a pair starts touching inside the 0.02 prediction distance before the body is in the active set. rapier-core finding 6 already records this, and release builds are unaffected.
- **Result.** The same program with 0.03 gaps (`$S/oracle_route_a.rs`) returned `"ok": true`. Its stdout matched the harness's 0.03-gap run exactly:
  - the quantum the stack falls asleep: q123 at 1.0, q79 at 0.0;
  - maximum penetration: 2.831613e-2 and 4.822694e-2;
  - top-box sag at q300: 4.760196e-3 and 5.581378e-2;
  - record hash at q300: `fbda45e92b2b8f5f` and `1965d29ad76a2450`;
  - with sleep off, the top box sinks more than 0.25 from q3418 at 0.0, and stays within 0.25 through q5200 at 1.0.

**Metrics.**
- **Asleep:** the first quantum after which a body reports sleeping. In T2's regime that is the law's flag.
- **Penetration:** measured after every quantum from the poses, with parry `query::contact(…, 0.0)` over every pair among slab and boxes. The deepest value is kept.
- **Drift:** the top box's distance from its starting (x, z) = (0, 0).
- **Sag:** (n − 0.5) − y_top, the rest height minus the actual height. Positive means below rest.
- **Tilt:** 2·acos|q_w|.
- **Speed:** |linvel| of the top box.
- **Collapse:** the first quantum the top box is more than 0.25 below its rest height.

## Route (a): `warmstart_coefficient = 0`

**Main's law** (one running world, Rapier's sleep). Drift, sag and tilt are the same at q300, q1000 and q10000 in every row: every box is asleep by q69 and nothing wakes. The top box's final speed is 0 in every row.

| scene | coeff | asleep from (every box) | max penetration (quantum, pair) | top drift | top sag | top tilt | top peak speed (quantum) |
|---|---|---|---|---|---|---|---|
| 1 box | 1.0 | q36 | 5.63e-5 (q35, slab–box0) | 3.43e-4 | 5.63e-5 | 0° | 0.250 (q2) |
| 1 box | 0.0 | q36 | 5.01e-4 (q34, slab–box0) | 1.88e-4 | 2.55e-4 | 0.028° | 0.250 (q2) |
| 3 boxes | 1.0 | q39 | 8.25e-4 (q38, box0–box1) | 5.44e-4 | 1.42e-3 | 0.0006° | 0.625 (q5) |
| 3 boxes | 0.0 | q41 | 1.75e-2 (q40, box0–box1) | 9.71e-3 | 1.74e-2 | 0.41° | 0.625 (q5) |
| 5 boxes | 1.0 | q42 | 1.66e-3 (q41, box0–box1) | 1.60e-5 | 4.49e-3 | 0.002° | 0.750 (q6) |
| 5 boxes | 0.0 | q69 | **3.72e-2** (q68, box0–box1) | **5.82e-2** | **5.54e-2** | **1.35°** | 0.875 (q7) |

**T2's law** (a fresh world every quantum, the law's sleep). "1.0 + carry" is the branch. "1.0, no carry" is the third option. As above, drift, sag and tilt are the same at q300, q1000 and q10000, and final speed is 0.

| scene | variant | asleep from | max penetration (quantum) | top drift | top sag | top tilt | top peak speed (quantum) |
|---|---|---|---|---|---|---|---|
| 1 box | 1.0 + carry | q35 | 5.63e-5 (q35) | 3.40e-4 | 5.63e-5 | 0° | 0.250 (q2) |
| 1 box | 1.0, no carry | q35 | 1.56e-4 (q35) | 1.70e-4 | 1.06e-4 | 0.006° | 0.250 (q2) |
| 1 box | 0.0 | q35 | 5.01e-4 (q35) | 1.86e-4 | 2.51e-4 | 0.029° | 0.250 (q2) |
| 3 boxes | 1.0 + carry | q38 | 9.82e-4 (q25) | 5.27e-4 | 1.47e-3 | 0.009° | 0.625 (q5) |
| 3 boxes | 1.0, no carry | q38 | 6.38e-3 (q38) | 4.72e-3 | 6.64e-3 | 0.14° | 0.625 (q5) |
| 3 boxes | 0.0 | q40 | 1.76e-2 (q40) | 9.86e-3 | 1.76e-2 | 0.39° | 0.625 (q5) |
| 5 boxes | 1.0 + carry | q41 | 2.33e-3 (q8) | 1.47e-3 | 5.09e-3 | 0.016° | 0.750 (q6) |
| 5 boxes | 1.0, no carry | q42 | 1.41e-2 (q42) | 2.40e-2 | 2.22e-2 | 0.51° | 0.874 (q7) |
| 5 boxes | 0.0 | q77 | **3.85e-2** (q77) | **7.86e-2** | **5.57e-2** | **1.55°** | 0.875 (q7) |

**Sleep off.** This is not the law. It stands for a stack whose island something else keeps awake, such as a walker leaning on it. Cells give the top box's drift / sag / |v|. "Rest" means |v| ≤ 1e-9.

| regime | scene | variant | max penetration | q300 | q1000 | q10000 | collapse |
|---|---|---|---|---|---|---|---|
| main | 1 box | 1.0 | 5.63e-5 | 3.43e-4 / 5.63e-5 / rest | same | same | never |
| main | 1 box | 0.0 | 5.01e-4 | 1.93e-4 / 2.79e-4 / rest | same | same | never |
| main | 3 boxes | 1.0 | 9.01e-4 | 5.61e-4 / 1.52e-3 / rest | same | same | never |
| main | 3 boxes | 0.0 | 1.81e-2 | 9.30e-3 / 1.85e-2 / rest | same | same | never |
| main | 5 boxes | 1.0 | 1.80e-3 | 9.73e-5 / 4.78e-3 / rest | same | same | never |
| main | 5 boxes | 0.0 | 6.29e-2 | 5.63e-2 / 5.61e-2 / 9.3e-4 | 6.84e-2 / 5.61e-2 / 1.1e-3 | fallen off the slab, falling at the 400 cap | **q4991** |
| T2 | 1 box | 1.0 + carry | 5.63e-5 | 3.40e-4 / 5.63e-5 / rest | same | same | never |
| T2 | 1 box | 1.0, no carry | 1.56e-4 | 2.56e-4 / 1.06e-4 / 4.2e-5 | 4.81e-4 / 1.06e-4 / 4.2e-5 | 3.39e-3 / 1.06e-4 / 4.2e-5 | never (slides) |
| T2 | 1 box | 0.0 | 5.01e-4 | 1.91e-4 / 2.79e-4 / rest | same | same | never |
| T2 | 3 boxes | 1.0 + carry | 9.82e-4 | 4.10e-4 / 1.52e-3 / rest | same | same | never |
| T2 | 3 boxes | 1.0, no carry | 9.31e-3 | 1.33e-2 / 7.13e-3 / 1.5e-2 | 3.67e-2 / 7.10e-3 / 1.5e-2 | 0.566 / 1.05e-2 / 1.5e-2 | never (walks) |
| T2 | 3 boxes | 0.0 | 4.09e-2 | 1.97e-2 / 1.84e-2 / 2.4e-3 | 5.02e-2 / 1.83e-2 / 2.8e-3 | 2.30 / 2.00 / rest (fallen) | **q6353** |
| T2 | 5 boxes | 1.0 + carry | 2.49e-3 | 1.73e-4 / 4.78e-3 / rest | same | same | never |
| T2 | 5 boxes | 1.0, no carry | 5.23e-2 | 5.20e-2 / 2.35e-2 / 1.7e-2 | 0.139 / 2.36e-2 / 1.8e-2 | fallen, 400 cap | **q3453** |
| T2 | 5 boxes | 0.0 | 5.60e-2 | 0.229 / 5.75e-2 / 5.5e-2 | 10.2 / 27.5 / 19.6 | fallen, 400 cap | **q759** |

The main-regime 0.0 collapse, traced every 250 quanta (`trace 10000 5 0.0 250 0`):
- **From q250 to q2250:** the top box leans in −x at a steady 1.12e-3/s. It moves from x −0.055 to −0.090 while y holds at 4.444.
- **From q2500:** the creep speeds up.
- **The fall:** tilt is 3.1° at q4750 and 23.9° at q5000. By q5250 the top box has left the slab at x −9.2.

**Timing.** Native, 5-box stack, µs per quantum, median of 9 runs × 10,000 quanta. Two sessions are shown as "a / b". The sleep-off rows time the first 4,000 quanta, before any collapse.

| regime | variant | mean over 10,000 | awake quanta | asleep quanta |
|---|---|---|---|---|
| main (`world.step()`) | 1.0 | 0.131 / 0.132 | 7.76 / 7.77 (42 quanta) | 0.098 / 0.099 |
| main (`world.step()`) | 0.0 | 0.147 / 0.147 | 7.29 / 7.06 (69 quanta) | 0.097 / 0.099 |
| main, sleep off | 1.0 | 7.71 / 7.50 | all | n/a |
| main, sleep off | 0.0 | 7.01 / 6.82 | all | n/a |
| T2 (whole quantum) | 1.0 + carry | 10.30 / 10.43 | 22.2 / 23.2 (41) | 10.25 / 10.36 |
| T2 (whole quantum) | 1.0, no carry | 10.22 / 10.24 | 21.1 / 21.6 (42) | 10.17 / 10.19 |
| T2 (whole quantum) | 0.0 | 9.92 / 10.21 | 19.9 / 21.1 (77) | 9.84 / 10.11 |

<a id="why-0-costs-more-than-dropping-the-carry"></a>**Why 0 costs more than dropping the carry.**
- **The 4 iterations are substeps.** `num_solver_iterations = 4` (`integration_parameters.rs:389`) runs as 4 substeps of dt/4 (`dynamics/solver/staged_island_solver/init.rs:95-101`, loop at `worker.rs:227`).
- **Every substep scales the carried impulse by the coefficient.** 3D contacts take the twist-friction path, because the default friction model is `Simplified` (`init.rs:419`). Each substep's `update` scales the impulse the constraint carries by the coefficient before reusing it: `contact_with_twist_friction.rs:451` (splat), `:502` (normal), `:516` (tangent), `:518` (twist).
- **At 0 the warm-start stage is skipped.** It applies those impulses to the bodies only when the coefficient is non-zero (`worker.rs:438`; the fused update, `worker.rs:296`).
- **So 0 cuts two warm starts.** It removes the warm start from substep k to k+1 inside every quantum, as well as the one carried across quanta.
- **Why "1.0, no carry" sits between.** A fresh T2 world starts each quantum's points at zero, since the first substep reads the manifold points (`contact_with_twist_friction.rs:197-217`), but it keeps the substep warm start.

**At 0 there is nothing to carry.** Two checks:
- **Zero-check** (`zero 10000`). Under main's law, every warm-start field of every manifold point was set to 0 after every quantum, through the sound serde rewrite of route (c). At 0.0 the run stays bit-identical to the untouched one for 10,000 quanta on 1, 3 and 5 boxes (40,000, 200,000 and 320,220 point zeroings). At 1.0 the same zeroing changes the state from q4, so the check can see a difference when one exists.
- **The branch at 0.0.** `t2c0`, the branch built with coefficient 0.0, still runs its carry. Its record equals the no-carry port at every quantum for 10,000 quanta, 3 scenes.

At 0.0, T2 can therefore delete `carry_warmstart`, `pairs_mut` and the 7 floats per point.

**What a player would see at these iteration counts.** Yes, 0.0 changes what a player sees, for 3- and 5-box stacks.
- **At rest.** The 5-stack comes to rest visibly sunk into itself and leaning:
  - main's law: box0 and box1 overlap by 3.7e-2, and the top box is 5.5e-2 low, 5.8e-2 off centre and tilted 1.35°;
  - T2's law: 3.8e-2, 5.6e-2, 7.9e-2 and 1.55°;
  - 1.0 in both regimes: ≤2.3e-3, ≤5.1e-3, ≤1.5e-3 and ≤0.016°.
  
  The 3-stack at 0.0 rests 1.8e-2 interpenetrated and 1.0e-2 off centre. A single box shows nothing a player would notice (≤5e-4).
- **It is a creep, not a jitter.** No oscillation appeared. The stack still sleeps, later (q69 against q42; T2 q77 against q41), because its creep speed (about 1e-3/s) sits under both sleep tests: Rapier's 0.05/s (`rigid_body_components.rs:1338-1340`) and the law's quiet test. Sleep then freezes the lean.
- **Kept awake, it falls.** Any stack kept awake keeps creeping and falls over:
  - the 5-stack, from q4991 (78 s) under main's law and from q759 (12 s) under T2's;
  - the 3-stack, from q6353 under T2's law.
  
  At 1.0 with T2's carry, nothing falls in 10,000 quanta, and velocities decay to ~1e-13.

## Route (c): serde

**1. What implements Serialize/Deserialize at 0.35.3.** With the feature on, every part of the world does except `PhysicsPipeline`. Paths below are in `rapier3d-f64-0.35.3/src/` unless noted.

**The feature.** `serde-serialize = ["arrayvec/serde", "nalgebra/serde-serialize", "parry3d-f64/serde-serialize", "dep:serde", "std"]` (`rapier3d-f64-0.35.3/Cargo.toml:85-91`).

**Contact state.**
- **`NarrowPhase`:** `geometry/narrow_phase/mod.rs:324`.
  - Skipped: `query_dispatcher` (327-331, rebuilt through `default_persistent_query_dispatcher`), `update_candidates` (337), `body_qualify_info` (347), `awake_body_mask` (352), `solver_graph_dirty` (377), `solver_color_todo` (398) and `retired_pairs` (403).
  - Serialized: the contact and intersection graphs, `graph_indices`, `pair_solver_hints`, `solver_contact_graph`, the solver-graph epochs and the force-event lists.
- **`ContactPair`:** `geometry/contact_pair.rs:178`. `solver_clusters_prev` is skipped (231; empty with clustering off). `recycle_state` is serialized (252-255: "Part of the snapshot").
- **`ContactData`:** `contact_pair.rs:52`. All the warm-start fields are included (62-76), and so are `solver_dp1`/`solver_dp2` (82-86).
- **`ContactManifoldData`:** 520. `solver_contacts` are serialized (553-569).
- **`SolverContactGeneric`:** 602-614.
- **parry** (`parry3d-f64-0.30.2/src/query/contact_manifolds/contact_manifold.rs`): `TrackedContact` derives at 7 (`fid1`/`fid2` at 133/139), and `ContactManifold` at 228 (struct at 474).

**The world.**
- **`PhysicsWorld`:** `pipeline/physics_world.rs:60`. It skips `physics_pipeline` (67) and `ccd_solver` (86, "Workspace only: not part of a snapshot").
- **`PhysicsPipeline`** has no derive: "this contains only workspace data" (`pipeline/physics_pipeline/mod.rs:44`).
- **The sets:**
  - `IntegrationParameters`: `dynamics/integration_parameters.rs:180`.
  - `RigidBodySet`: `dynamics/rigid_body_set.rs:43`.
  - `ColliderSet`: `geometry/collider_set.rs:24`.
  - `RigidBody`: `dynamics/rigid_body.rs:21`.
  - `Collider`: `geometry/collider.rs:21`.
  - `IslandManager`: `dynamics/island_manager/manager.rs:28`; skips 43 and 46.
  - `ImpulseJointSet`: `dynamics/joint/impulse_joint/impulse_joint_set.rs:16`.
  - `MultibodyJointSet`: `multibody_joint_set.rs:54`.
  - `CCDSolver`: `dynamics/ccd/ccd_solver.rs:27`.
- **`BroadPhaseBvh`:** `geometry/broad_phase_bvh/mod.rs:22`. Its pair `HashMap` is written sorted (28-34 and 159-168 into `utils/mod.rs:349-364`).
- **`RigidBodyActivation`:** `dynamics/rigid_body_components.rs:1296`. It serializes the `pub(crate)` `sleep_prev_pose` (1325).
- **Ordering.** Under `enhanced-determinism`, parry's `HashSet` is an insertion-ordered `IndexSet` (`parry3d-f64-0.30.2/src/utils/hashset.rs:1-7`), so `ImpulseJointSet::to_join` serializes in a fixed order.

**No `&mut` path.** `geometry/narrow_phase/*.rs` has no `pub fn …_mut`, and `contact_pairs()` returns `&ContactPair` (`queries.rs:180`).

**The feature is inert.** Enabling it changes no simulation bit: all 15 route-(a) run hashes are identical between the plain build and the serde build.

**2. The round trip.** Main's law, 5-box stack. The NarrowPhase is serialized with bincode 1.3.3 and deserialized. The comparison is field by field, through the public API, in order:
- every pair's handles and manifold count;
- every manifold's subshapes, normals, bodies, flags, friction, restitution and solver contacts;
- every point, in order: fid1, fid2, local points, dist, and `impulse`, `tangent_impulse`, the four warm-start fields, `solver_dp1` and `solver_dp2`.

The deserialized value was also re-serialized and compared byte for byte.

- **At q200, as specified.** 5 pairs, 5 manifolds and 36 points, 20 of them with a non-zero `warmstart_impulse`.
  - bincode: 12,054 B. Re-serialized bytes identical. 0 field mismatches.
  - serde_json with `float_roundtrip`: 25,215 B, 0 mismatches.
  - The whole world: 19,744 B, re-serialized identically.
  - **This checkpoint cannot test continuation.** All 5 bodies have been asleep since q42, so every candidate below stays identical for 200 quanta, including the control with nothing carried.
- **At q20, all bodies awake.** Same counts. bincode 12,094 B, JSON 25,264 B, world 19,792 B, 0 mismatches. Stepping each candidate 200 more quanta against the uninterrupted world:
  - **Fresh world plus the deserialized NarrowPhase:** bit-identical throughout. The fresh world is built the way T2 builds a quantum's world from the bodies' public state, with the whole `RigidBodyActivation` struct copied.
  - **The same, without copying the activation:** first differs at +22 (sleep timing), max |Δp| 1.6e-4 at +200.
  - **Fresh world, its own NarrowPhase (control):** differs from +1, max |Δp| 2.1e-2.
  - **The deserialized whole `PhysicsWorld`:** bit-identical throughout.
- **64 boxes at q20.** A 4×4 grid of columns 4 high, all 0.01 apart. 484 pairs, 2,224 points, 256 of them carrying load.
  - The NarrowPhase is 768,174 B in bincode and 1,673,736 B in JSON, with 0 mismatches. The world is 873,968 B.
  - Over 300 more quanta: NarrowPhase plus activation bit-identical; without the activation, differs from +20; control differs from +1; whole world bit-identical.
  - At q100 everything is asleep, so the check is vacuous there.
- **Inside T2's regime.** The running world at quantum q is fresh(state) plus the carry. The restore is fresh(state) plus the deserialized NarrowPhase (8,686 B).
  - From q20: bit-identical for 200 quanta. The no-carry control differs from +1.
  - From q200: asleep, so vacuous.
- **Bytes across builds.** For the 64-box world at q20, native x86_64 and wasm32 under V8 serialize identical bytes: NarrowPhase SHA-256 `bb0f1303…e951`, whole world `cba7fc35…cb91`.

**3. Binary size.** Built with `node build.mjs` in scratch copies. The RUSTFLAGS are build.mjs's own; these are Windows builds, not the pinned Linux artifact.

| build | bytes | Δ against its base |
|---|---|---|
| `v0`, main as is | 1,524,412 | n/a |
| `v1`, + `serde-serialize` feature, no code | 1,524,415 | +3 |
| `v2`, + bincode 1.3.3 and exported `solver_save_np`/`solver_load_np` (bincode NarrowPhase into a static buffer, deserialize, assign) | 1,608,447 | +84,035 (+5.5%) |
| `v3`, `v2` + exported `solver_save_world`/`solver_load_world` (whole `PhysicsWorld`) | 2,164,270 | +639,858 (+42%) |
| `t2`, the branch | 1,536,474 | n/a |
| `t2s`, the branch with its three pointer writes (`carry_warmstart`, `solver_clear_warmstart`, `restore`) replaced by the streamed serde rewrite | 1,619,053 | +82,579 (+5.4%) |

The whole world costs far more because it pulls in serde for every shape type.

**4. Time.** The world is 64 boxes at q20, awake: 484 pairs, 2,224 points.

Native, median over 5 × 400 operations per run, five runs. One run's NarrowPhase serialize read 260 µs while the others read 71–73 µs; it is shown separately.

| operation | bincode | serde_json (2 runs) |
|---|---|---|
| NarrowPhase serialize | 71.2–72.8 µs (outlier 260) | 2,097–2,125 µs |
| NarrowPhase deserialize | 118.9–136.6 µs | 1,875–1,904 µs |
| PhysicsWorld serialize | 95.7–103.7 µs | 2,520–2,531 µs |
| PhysicsWorld deserialize | 172.1–190.6 µs | 2,893–3,161 µs |
| for scale: one `world.step()` of this world | 275–418 µs (median 282) | n/a |

**In wasm under node** (`v2`/`v3`, median of 5 × 200 calls):
- NarrowPhase: save 91.1–91.2 µs, load 153–169 µs.
- PhysicsWorld: save 122.7 µs, load 201.1 µs.
- For scale, `stepSolver` on this world costs 737–797 µs per quantum.
- An in-place round trip at q20, followed by 200 quanta, reruns identically, both for the NarrowPhase and for the whole world.

**As T2's per-quantum carry.** Native, T2's regime with sleep off (every body awake). The 64-box JSON row is over 100 quanta, the others over 1,000. Two runs are shown as "a / b".

| carry | 5 boxes: carry µs | 5 boxes: quantum µs | 64 boxes: carry µs | 64 boxes: quantum µs |
|---|---|---|---|---|
| none | 0 | 21.6 / 22.2 | 0.1 | 775 / 783 |
| pointer write (the branch; undefined behaviour) | 0.5 / 0.7 | 19.5 / 19.0 | 63.3 / 62.0 | 860 / 875 |
| streamed bincode rewrite (sound) | 6.7 / 4.4 | 26.2 / 23.3 | 499 / 528 | 1,332 / 1,372 |
| serde_json tree patch (sound) | 154 / 169 | 180 / 196 | 14,322 / 12,408 | 15,580 / 13,580 |

**In wasm under node** (`t2` against `t2s`, µs per quantum). The module was warmed first, and each figure is the median of 9 runs, over two rounds.

| scene | phase | t2 | t2s |
|---|---|---|---|
| 5 boxes | awake | 39.3 / 42.1 | 44.4 / 45.4 |
| 5 boxes | at rest | 15.4 / 16.1 | 19.9 / 21.6 |
| 64 boxes | awake | 1,715 / 1,646 | 1,939 / 1,903 |
| 64 boxes | at rest | 696 / 687 | 947 / 920 |

T2's `restoreSolver`, median of 21 calls in V8:

| build | 5 boxes (2,040 B snapshot) | 64 boxes (116,424 B snapshot) |
|---|---|---|
| t2 | 30 µs | 887 µs |
| t2s | 39 µs | 1,164 µs |

**5. What (c) can and cannot do for T2's per-quantum carry.**

**Can.**
- **Be the carry, soundly, with no change in behaviour.** Serde cannot mutate a live NarrowPhase, but it can construct one, and `world.narrow_phase` is a public field. The per-quantum carry becomes: build the fresh world, run the collision pass, serialize its NarrowPhase while substituting the carried warm-start fields, deserialize, and assign.
  - **How it works.** A streaming serializer writes bincode 1.3's byte format and substitutes the four `warmstart_*` fields of each `ContactData` as serde visits it (`$S/harness/src/patchser.rs`, about 230 lines).
  - **Byte check.** Without patches, its output is byte-identical to `bincode::serialize` for the NarrowPhase and the whole world, and it visits exactly one `ContactData` per point (36 and 2,224).
  - **Against the branch.** It matches the branch's pointer carry:
    - at every quantum for 10,000 quanta, on 1, 3 and 5 boxes;
    - natively, and in wasm as `t2s` against `t2`;
    - with sleep on, and with sleep off (239,720 points carried on the 5-stack).
  - **Restore.** `t2s` passes T2's own restore-then-rerun: the snapshot after restore is byte-identical, and the state 200 quanta later matches, on 5 and 64 boxes.
  - **What remains.** `t2s` keeps only the engine's existing `unsafe` for its statics; no pointer cast from a shared reference remains.
- **Be the restore instead of the carry.** A fresh world plus a deserialized NarrowPhase reruns bit-identically: in T2's regime as it stands, and in main's regime when the whole `RigidBodyActivation` is copied too. A deserialized whole `PhysicsWorld` reruns bit-identically in main's regime, so a single running world saved and restored with Rapier's own serialization would pass restore-then-rerun without the per-quantum rebuild, in the scenes measured.
  - Its snapshot is 874 KB for 64 boxes, against T2's 116 KB.
  - Its bytes matched between x86_64 and wasm32 here.
  - Hashing it every quantum was not measured.
- **Carry `sleep_prev_pose`.** T2's header says no public call can read or write it. It cannot be reached field by field, but `RigidBodyActivation` is `Copy` and serialized whole. Copying the whole struct through `activation()`/`activation_mut()` is what made the main-regime transplant bit-identical; without it, the runs part at +20/+22.

**Cannot.**
- **Mutate in place.** Each carry rebuilds the whole NarrowPhase: every pair and point, 768 KB in the 64-box world. Its cost therefore scales with contact count, not with how many points carry impulses: +0.22–0.26 ms per quantum under V8 at 484 pairs.
- **Stay cheap with a generic JSON tree.** A patch through a `serde_json::Value` tree costs 12–14 ms per quantum natively for 64 boxes, most of the 15.6 ms quantum, so it is not usable. It also needs `float_roundtrip`, because default serde_json parsing is not exact, and `arbitrary_precision`, because the NarrowPhase holds `Vec<u128>` colour masks.
- **Reach skipped state.** It cannot reach state serde skips:
  - the NarrowPhase's scratch buffers and pair pool (inert here: every rerun above is bit-identical without them);
  - the `PhysicsPipeline` workspace;
  - the `CCDSolver`, which is fine at `max_ccd_substeps = 1` (answer 7).
- **Survive a Rapier bump on its own.** The rewrite keys on the struct name `ContactData`, the four field names, serde's visit order and bincode 1.3.3's layout. A bump that renames or reorders any of them breaks it. The bit-identity test against the pointer-free run is what would catch that.
- **Tolerate changed handles.** The deserialized NarrowPhase must meet the same collider and body handles. That holds in T2 because `build_world` inserts in the same order for a given signature.

## Incidental: T2's restore refuses its own snapshot

Measured on the unmodified branch binary (`t2`, `ee2e50a`). The 5-box stack saved at q13, q23 or q26 is refused by `restoreSolver` with refusal 6, `REFUSE_RECORD`. At q12, q14, q22 and q24 it is taken.

**Cause.** `restore` rebuilds the record's state with `record_state` (`rapier_law.rs:381`), which runs the record's quaternion through `canon_quat` again (388). It then compares that bit for bit with the snapshot's quaternion (1109-1132). `canon_quat` is not idempotent: re-normalizing an already-normalized quaternion can move its last bit.
- Example: q13, body 4. `(-5.682693679169333e-5, …, 0.999999838276571)` becomes `(-5.682693679169334e-5, …, 0.9999998382765711)`.
- Over q1–q100 of the 5-stack, 3 of 500 body-quanta are affected at coefficient 1.0 and 13 of 500 at 0.0.
- It is unrelated to either route: `t2s` refuses at the same quanta, and `t2c0` refused at q20.
- It bears on T2's acceptance line, which requires the restore to pass for every fixture.

## Caveats

- **Scene coverage.** Only unit cubes, exactly aligned, on a flat cuboid slab: no heightfield (whose contact workspaces serde would carry), no rotated statics, no kinematic walker, no joints. There is one drop gap, 0.01, plus the 0.03 sensitivity run. At 0.03 the 5-stack at 0.0 still rests with 3.75e-2 penetration and 5.58e-2 sag, and collapses from q3418 with sleep off; at 1.0 it does not collapse.
- **Sleep off is a stand-in.** It is not the engine's law; it stands for an island that something else holds awake.
- **Timing noise.** Timings come from a shared desktop, and repeated sessions are shown side by side. V8 timings were taken after a warm-up; the first unwarmed pass read 115 µs for the 5-stack.
- **The pointer carry is undefined behaviour.** The harness's pointer carry is the branch's undefined behaviour, reproduced only as a reference. Its agreement with the branch binary is an observation about this compiler, not a soundness argument. The sound carries were checked against the branch's wasm directly.
- **Byte stability is narrow.** It was seen for x86_64 native against wasm32 under V8, on one scene. ARM was not tested.

## Commands

`S=<scratchpad>/route-costs`; `export PATH=~/.cargo/bin:$PATH`. Raw outputs are in `$S/out/`.

```
cargo +1.98.1 --version; rustc +1.98.1 --version --verbose; node --version
# engine sources, read through the API (main d5b735b; T2 ee2e50a)
gh api -H "Accept: application/vnd.github.raw" "repos/mcp-tool-shop-org/si-rpg-engine/contents/solver/<file>?ref=<main|ee2e50a179917d57c52eef9e2a326bf199f2d34e>"
# harness (Cargo.lock copied from solver/Cargo.lock)
cd $S/harness
cargo +1.98.1 build --release --target-dir target-plain
cargo +1.98.1 build --release --features serde --target-dir target-serde
./target-plain/release/route-costs.exe a 10000              # route (a), main's law     -> out/a.txt
./target-plain/release/route-costs.exe a-t2 10000           # route (a), T2's law       -> out/a-t2.txt
./target-plain/release/route-costs.exe a-nosleep 10000      #                           -> out/a-nosleep.txt
./target-plain/release/route-costs.exe a-t2-nosleep 10000   #                           -> out/a-t2-nosleep.txt
./target-plain/release/route-costs.exe trace 10000 5 0.0 250 0
./target-plain/release/route-costs.exe time 10000 9         # twice: out/time.txt, out/time-run2.txt
ROUTE_GAP=0.03 ./target-plain/release/route-costs.exe a 10000; ROUTE_GAP=0.03 ./target-plain/release/route-costs.exe a-nosleep 10000
./target-serde/release/route-costs.exe a 10000; ./target-serde/release/route-costs.exe a-t2 10000   # hashes == plain build
./target-serde/release/route-costs.exe zero 10000
./target-serde/release/route-costs.exe a-t2-serde 10000; ./target-serde/release/route-costs.exe a-t2-nosleep-serde 10000; ./target-serde/release/route-costs.exe a-t2-bincode 10000
./target-serde/release/route-costs.exe patchser
./target-serde/release/route-costs.exe c2 200; ./target-serde/release/route-costs.exe c2 20
./target-serde/release/route-costs.exe c2-grid 20 300; ./target-serde/release/route-costs.exe c2-grid 100 300
./target-serde/release/route-costs.exe c2-t2 200; ./target-serde/release/route-costs.exe c2-t2 20
./target-serde/release/route-costs.exe c4 20 400            # five runs
./target-serde/release/route-costs.exe c5 1000              # two runs
./target-serde/release/route-costs.exe dump-bytes 20; sha256sum $S/out/native-grid64-*.bin
# engine binaries: scratch copies, unmodified build.mjs (v1-v3, v0c0, t2c0, t2s as described above; t2s by python $S/make_t2s.py)
cd $S/<v0|v1|v2|v3|v0c0|t2|t2c0|t2s>/solver && node build.mjs
# port == engine, per quantum
./target-plain/release/route-costs.exe rec-hash <Q> <main|t2> <n> <1.0|0.0> <ptr|none>   # serde build also: serde, bincode
node $S/node/drive_stack.mjs $S/<build>/solver/dist/solver.mjs <n> <Q>                  # then diff the two
# wasm timing and checks
node $S/node/drive_serde.mjs $S/v2/solver/dist/solver.mjs 200; node $S/node/drive_serde.mjs $S/v3/solver/dist/solver.mjs 200
node $S/node/dump_bytes.mjs $S/v3/solver/dist/solver.mjs
node $S/node/drive_t2.mjs $S/<t2|t2s>/solver/dist/solver.mjs      # two rounds
node $S/node/time_restore.mjs $S/<t2|t2s>/solver/dist/solver.mjs
node $S/node/why_refused.mjs $S/<t2|t2s|t2c0>/solver/dist/solver.mjs 12,13,14,22,23,24,26; node $S/node/why3.mjs $S/<t2|t2c0>/solver/dist/solver.mjs
# oracle (run from E:/AI/readouts/rust-knowledge)
python scripts/compile_oracle.py file $S/oracle_route_a.rs --expect runs --deps rapier3d_f64 --stdout "<the four lines quoted in Method>"
```
