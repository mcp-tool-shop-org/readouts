Squeeze launch: why the product law launches a small box at 162.7 units a second. si-rpg-engine PR #75 head `88379d5` (F1's law), main `93a2d1e` (F2's law), rapier3d-f64 0.35.3 with `enhanced-determinism`, parry3d-f64 0.30.2; the bump measured against rapier3d-f64 0.36.0 with parry3d-f64 0.31.1. Measured 2026-09-26.

**Host and tools.** Windows 11 Pro 10.0.26340, x86_64. rustc 1.98.1 (48a229cea 2026-09-01), cargo 1.98.1 (797e8a9bc 2026-08-05), node v22.22.3.

**Engine state.**
- The engine was cloned from GitHub into scratch with `core.autocrlf=false`, and `pull/75/head` was fetched for `88379d5`. Nothing in `E:/AI/si-rpg-engine` was read, built, run or changed.
- `88379d5` walls the minds fixture's room. The coordinator's scene is `7bbed41`'s open room, so every F1 run below uses `git show 7bbed41:fixtures/behavior-minds.json` as its world, on `88379d5`'s code. The Rust law at `88379d5` is `7bbed41`'s: only `solver/build.mjs` differs under `solver/`.
- F2 runs use `93a2d1e` with T6's rest margin (`6e41ccd`, which touches only `packages/tick/predicates.js` and its test) applied without a commit, unless a row says "plain main".

**Scratch.** `$S = <scratchpad>/squeeze-launch`, a session scratch directory that is not kept in this repo. Programs:
- `probe.mjs` is the coordinator's probe as described: seed 11, the product law, the four intents, advancing to tick 1274. `--retry` resubmits an intent refused as mid-action on each later tick until it is admitted.
- `patch_glue.mjs` and `recorder.mjs` record every `solver_load` and `solver_step` call: its arguments, the body, collider and height buffers the glue wrote, and every step's output. The patch goes into the scratch checkout's generated `solver/dist/solver.mjs` and does nothing unless a recorder is loaded, so the wasm bytes are unchanged. Any script records under `node --import recorder.mjs` with `SOLVER_LOG` set.
- `harness/` (F1), `harness-f2/` (F2) and `harness-bump/` (0.36.0) are native builds of the solver crate's own `lib.rs`, `rapier_law.rs` and `kcc.rs`, made by `make_harness.py` against each commit's `Cargo.lock`. `replay` feeds a recorded call log through the native law and compares every step's output with the wasm's, bit for bit.
  - Trace points and variants are inert unless switched on.
  - `copy-impulses` replaces rapier's `solve_character_collision_impulses` with a copy made through the public API, with trace points. It matches the wasm bit for bit on every run below.
  - `copy-impulses-fixed` is that copy with a Vec of its own per collider. `copy-impulses-1004` is that copy with rapier PR #1004's exact change.
  - `--from-tick T` loads a fresh world from tick T's own input buffers and steps it once, so the same state goes through each law.
- `patch_law.py` patches the scratch law with one candidate fix. `measure.sh` rebuilds the wasm and runs the probe, the product golden (`node harness/sim.mjs`) and the full `npm test` file list.
- `search.mjs` and `red.mjs` build the closed test rooms.

## Answer

1. **Where the 162.7 comes from.** The contact solver does not produce it: `world.step()` damps it. The source is `solve_character_collision_impulses`, which the law calls before the step (`solver/src/rapier_law.rs:817` at `88379d5`, `:825` at `93a2d1e`). It hits a defect in how rapier 0.35.3 collects contact manifolds.
   - At tick 710 that call takes the crate from (0.042, 0.079, −0.174) to (0.042, 0.079, −178.846) units/s, and its spin from 0.41 to 3,117.7 rad/s.
   - The step then leaves (36.690, 61.350, −146.145), |v| 162.690. Two floor contacts take 1.4146 of impulse, and the solver's per-substep angular cap brings the spin down to 50.22 rad/s. [MEASURED]
2. **What drives it.** It is not a squeeze.
   - On ticks 700 to 710 the crate touches only the floor (never deeper than 1e-4) and the walker (never closer than 0.0150, solver impulse 0). There is no wall contact, and its pair with the shade has no contact points.
   - The driver is the character-impulse pass. rapier 0.35.3 gathers every nearby dynamic collider's manifolds into one Vec and assumes parry appends to it. For a convex pair parry writes into `manifolds[0]` instead.
   - With the crate and the shade both near the walker, the shade's call overwrites the crate's manifold. The crate is then pushed at the shade's contact points, placed through the crate's pose, along the crate's normal.
   - The impulse's mass ratio uses linear mass only and re-reads the point velocity after every impulse. Every one of the walker's five hits re-runs the pass. So the error grows to 178.8 units/s in one quantum.
   - The character mass of 1.0 enters only through that mass ratio. The kinematic walker's infinite mass does not enter at all. [SOURCE][MEASURED]
3. **Fixes, measured.** Everything was measured under both laws; the table is in section 3.
   - **Backport #1004:** the engine's own copy of `solve_character_collision_impulses` with rapier PR #1004's change (a Vec per collider). It removes every launch and moves nothing: F1 286 of 286 tests with golden `b5e62d2cc42d9ad8`; F2 244 of 244 with golden `6e0d351693b18c93`.
   - **Bump to rapier3d-f64 0.36.0**, which carries #1004. It builds the law unchanged and moves nothing either. On the red worlds its call logs are byte-identical to the backport's.
   - **Settings-level:** `normalized_max_linear_velocity` (rapier's per-substep speed cap, 400 by default) at 10 bounds the ejection to 10 units/s and keeps all 244 tests and the golden. It does not fix the cause: the box still takes the wrong impulses and crosses the room.
   - **Other usage-level changes** keep the golden but move 12 to 14 fixture and restore tests: only the hit body pushed, no character impulses, or a character mass of 0.1.
4. **Under F2.** With the four intents as given there is no launch, because the scene never forms.
   - F2's walker keeps its full stride, so the move from tick 497 still has 19 quanta to run at 570, and the push is refused as mid-action. Resubmitted at 589, it is admitted, and the crate and the shade are never both near the walker (0 overwrites in 1,274 quanta).
   - From F1's exact state at tick 710, F2's law launches the crate identically, to |v| 162.698. F2 still calls rapier's own impulse function (`rapier_law.rs:825`). [MEASURED]

**For F3 (test first).**
- **The red.** The closed room in section 4.1 (three bodies; walls 2.0 high on every side, above the controller's 1.5 maximum rise), under F2's law on plain `93a2d1e`. The walker pushes the shade at tick 0.
  - The crate first exceeds 10 units/s at tick 53, at 26.0642 units/s. The frame hash there is `375c78856a5a4b15`, and at tick 200 it is `8936cf832bc642ab`.
  - The overwrite fires 19 times, and quanta 42 to 53 have two dynamic colliders near the walker. T6's margin changes nothing here: same hashes.
- **The control.** The copy with the fix off matches the wasm bit for bit on every run recorded:
  - the minds scene, 1,274 quanta;
  - the product scene, 10,000;
  - the course tests, 9,044;
  - the outcome tests, 82,752;
  - both red rooms, 200 each.

  With the fix on it is identical wherever no quantum has two dynamic colliders near the walker. The product scene, the course and the outcome runs never have even one. On the red rooms it first differs on a quantum that has two: tick 45 of 42 to 53, tick 63 of 57 to 74, and tick 72 of 72 to 124.
- **The cost.** About 70 lines copied from rapier (a NOTICE entry), and one Vec per dynamic collider per pass. It moves no golden, behaviour number, course or outcome test.
  - The product scene never has a dynamic collider near the walker: 0 of 10,000 quanta. So the golden cannot move under either route.

**Bump versus backport.** Everything the engine measures is identical between the two routes. The bump also carries more: parry 0.31.1, rapier's solver, CCD and island changes, soft bodies, and `ContactPair::manifolds` as a method. The suite covers some of that; section 4.3 lists what it does not.
- #1012 touches the broad phase only by renaming its scratch buffers.
- The query pipeline still resolves broad-phase leaves without their generation (`handle_of` calls `get_unknown_gen`). So the slot-alias path is the same in both versions.

## 1. Reproduction

### Scene

This is the coordinator's scene and probe, exactly: `7bbed41`'s `behavior-minds.json` world (no outer walls), `createWorld(world, 'product')`, `createMemory()`, `createTick({ seed: 11, world, rules: loadIntentRules().rules, memory })`. The walker's intents cite the newest frame hash:

| Tick | Intent | Under F1 (88379d5) |
|---|---|---|
| 41 | push crate | admitted |
| 269 | push shade | admitted |
| 497 | move to (0.75, 3.75) | admitted |
| 570 | push shade | admitted |

- **Tick 709:** crate |v| 0.196.
- **Tick 710:** crate v = (36.690183, 61.349555, −146.144584), |v| 162.690; w = (21.074995, −9.129084, −44.662425).
- **Tick 1274:** crate at (39.019, 16.345, 133.433), |v| 36.798, |w| 48.454. The frame hash is `35f70795965dd5f4`, as the coordinator measured.

The wasm built on this host has digest `218932242846db166e2e319a6a706f84b869eeebb5f269dd5326f5496d87a0f1`. The pinned digest is the Linux build's.

### The native replay is the law [MEASURED]

The recorded log has 1 load and 1,274 steps. Replayed through the native build of the same `lib.rs` and `rapier_law.rs`, every step's 17 slots for every body match the wasm bit for bit, and the final crate state matches. The same holds with rapier's impulse function replaced by the `copy-impulses` copy.

## 2. The mechanism

### 2.1 Where the speed appears [MEASURED]

The law's quantum, from `integrate` at `88379d5` (`rapier_law.rs:744-843`):
1. `move_shape` plans the kinematic walker (`:789`).
2. `set_next_kinematic_translation` sets its next translation (`:802`).
3. `solve_character_collision_impulses(DT, &mut query, &*shape, 1.0, &plan.collisions)` runs (`:817`).
4. `world.step()` steps the world (`:820`).

The crate at each stage of tick 710:

| Stage | Crate v | Crate \|w\| |
|---|---|---|
| Before the impulses | (0.042403, 0.079006, −0.174382) | 0.4141 |
| After the impulses | (0.042403, 0.079006, −178.845727) | 3,117.7414 |
| After the step | (36.690183, 61.349555, −146.144584) | 50.2218 |

The step does not add the speed; it removes some of it.
- The two floor points it solves take 0.1714 and 1.2432 of impulse.
- The solver caps each body's angular speed at `MAX_ROTATION × inv_dt` per substep. At dt = 1/64 that is 50.27 rad/s, which matches the post-step |w| of 50.22 (rapier `dynamics/solver/staged_island_solver/worker.rs:569-600`).
- It also caps linear speed at `normalized_max_linear_velocity`, 400 units/s by default (`dynamics/integration_parameters.rs:250-255, 396`). Red room B in section 4.1 reaches exactly 400.0000 because of that cap.

### 2.2 The overwrite [SOURCE]

**parry3d-f64 0.30.2, `query/default_query_dispatcher.rs:740-752`.** For a convex–convex pair (every box here), `contact_manifolds` pushes a manifold only if the Vec is empty, then computes into `&mut manifolds[0]`. This is the dispatcher's contract, one persistent Vec per pair. Rapier's narrow phase honours it with `&mut pair.manifolds` (rapier `geometry/narrow_phase/pair_update.rs:323-330`).

**rapier3d-f64 0.35.3, `control/character_controller.rs`,** in `solve_single_character_collision_impulse`:
- One `manifolds` Vec is shared by every dynamic collider in the character's loosened AABB (`:921`).
- Each call records `prev_manifolds_len` (`:934`) and passes the shared Vec to the dispatcher (`:935-942`).
- It then tags only `manifolds[prev_manifolds_len..]` with `rigid_body2` and `normal` (`:944-947`), and pads the poses with `resize` (`:948`).

With a second convex dynamic collider in range, the second call overwrites `manifolds[0]` and adds nothing:
- the slice `[1..]` is empty, so the second body gets no manifold;
- `manifolds[0]` keeps the first body's `rigid_body2` and `normal`, because parry rewrites only `points`, `local_n1` and `local_n2` (`contact_manifolds_cuboid_cuboid.rs:81-99`, and `ContactManifold::clear`, `contact_manifold.rs:853-855`, clears points only);
- `resize` leaves the first body's collider pose in place.

Then, for each point:
- the impulse goes to the first body at `collider_pos * pt.local_p2` (`:963`), which is the second body's local contact point placed through the first body's pose;
- the direction is the first body's normal (`:966`);
- the gate is `pt.dist <= prediction` (`:961`), which uses the second body's distances, with prediction = skin + 0.05 = 0.06 (`predict_ground`, `:491`).

The same file's grounded check does it correctly: it clears its Vec for each collider (`:519`).

### 2.3 Tick 710, point by point [MEASURED]

The walker's plan at tick 710 holds five hits: floor, shade, crate, floor, shade. Each hit runs the pass once. In every pass the crate is gathered first and the shade second, so the crate's manifold is overwritten every time.

The replay of the copied function shows the effect:
- The crate's manifold is right when computed. `local_p1` is on the walker's −z face, `local_p2` is on the crate, and `|pos12·lp2 − (lp1 + n1·dist)|` is about 1e-16.
- The shade's call then replaces it. `local_p1` moves to the walker's +x face, and `local_p2` has |lp2| 0.39 to 0.43, which is shade-sized: the shade's half-extent is 0.25.
- So the impulses reach the crate at lever arms of 0.39 to 0.43. No point on the crate is further than 0.26 from its centre (half-extents 0.12 × 0.2 × 0.12).

Each point's impulse is `normal · max(0, (v_transfer − v_point)·normal) · m·M/(m+M)`. Here m = 0.02304 is the crate's mass and M = 1.0 is the character's. The mass ratio counts linear mass only.
- The point's normal velocity changed by 4.862 times the intended correction at point 0, and by 12.820 times at point 1. Above 2 the sequential update diverges.
- The effective-mass form of the ratio is (1 + m·k)/(1 + m/M), with k = (r×n)ᵀ I⁻¹ (r×n). It matches both measured values: m·k is 3.97 and 12.1. [REASONED]

The corrections applied, in order:

| Pass (hit) | Point 0 | Point 1 |
|---|---|---|
| #0 (floor) | nothing | nothing |
| #1 (shade) | nothing | nothing |
| #2 (crate) | 0.1105 | 0.8442 |
| #3 (floor) | 3.8811 | 11.0383 |
| #4 (shade) | 45.7392 | 121.1746 |

In passes #0 and #1 every delta was negative. The impulses in passes #3 and #4 are 0.087 to 2.73. Their `velocity_to_transfer` is about 0, so the pass is chasing the spin it made itself. After pass #4 the crate is at −178.846 units/s.

**Same state, each law.** F1's exact state at tick 710 was loaded fresh and stepped once:

| Law | Impulse function | Crate after the step |
|---|---|---|
| F1 | Rapier's | \|v\| 162.698 |
| F2 | Rapier's | \|v\| 162.698, bit-identical to F1 |
| F1 or F2 | the fixed copy | \|v\| 0.311, \|w\| 1.315 |

### 2.4 Ticks 700 to 710 [MEASURED]

These are traced through the native replay of the coordinator's run. A pair listed with "(no points)" overlaps in the broad phase with no contact inside the prediction distance. A depth is the smallest point distance, where negative means penetration.

| Tick | Hits | Crate \|v\| before impulses | After impulses | \|w\| after impulses | After step | \|w\| after step | Crate contacts after the step: min depth / summed impulse |
|---|---|---|---|---|---|---|---|
| 700 | 5 | 0.2311 | 0.2682 | 1.800 | 0.1950 | 0.316 | shade (no points); walker +0.0150 / 0; floor +0.0010 / 0.0017 |
| 701 | 4 | 0.1950 | 0.3044 | 2.432 | 0.2514 | 1.292 | shade (no points); walker +0.0150 / 0; floor +0.0000 / 0.0014 |
| 702 | 5 | 0.2514 | 0.2514 | 1.292 | 0.1965 | 0.441 | shade (no points); walker +0.0150 / 0; floor +0.0000 / 0.0019 |
| 703 | 5 | 0.1965 | 0.3688 | 3.217 | 0.2313 | 0.687 | shade (no points); walker +0.0150 / 0; floor −0.0000 / 0.0039 |
| 704 | 5 | 0.2313 | 0.2598 | 0.302 | 0.2528 | 0.767 | shade (no points); walker +0.0150 / 0; floor +0.0005 / 0.0008 |
| 705 | 5 | 0.2528 | 0.2943 | 0.383 | 0.2673 | 1.396 | shade (no points); walker +0.0150 / 0; floor −0.0000 / 0.0018 |
| 706 | 5 | 0.2673 | 0.3848 | 1.912 | 0.2004 | 0.784 | shade (no points); walker +0.0150 / 0; floor −0.0000 / 0.0050 |
| 707 | 3 | 0.2004 | 0.2004 | 0.784 | 0.0500 | 0.118 | shade (no points); walker +0.0150 / 0; floor +0.0000 / 0.0053 |
| 708 | 5 | 0.0500 | 0.3531 | 6.561 | 0.2342 | 0.957 | shade (no points); walker +0.0150 / 0; floor −0.0001 / 0.0055 |
| 709 | 5 | 0.2342 | 0.2674 | 1.522 | 0.1961 | 0.414 | shade (no points); walker +0.0150 / 0; floor +0.0015 / 0.0011 |
| 710 | 5 | 0.1961 | 178.8457 | 3117.741 | 162.6904 | 50.222 | shade (no points); walker +0.0150 / 0; floor +0.0000 / 1.4146 |

- The pass adds speed and spin on almost every quantum, and the step takes most of it back, until 710 compounds.
- The overwrite first fires at tick 609, after the tick-570 push. It fires 284 times in the run, on 103 quanta, the last at 711.
- The crate is tipped: at tick 710 its quaternion is (−0.591, 0.397, −0.379, −0.591). Over 700 to 710 its centre sits 0.120 to 0.126 above the floor. The narrow phase never reports it deeper than 1e-4. I did not find how the sweep's "0.036 into the floor" was measured.

### 2.5 The amplifier on its own [MEASURED][REASONED]

The linear-mass ratio is a second defect, independent of the overwrite. It is still in rapier 0.36.0.
- With correct contact points the lever arms stop at 0.26, so the overshoot is smaller, but it can still exceed 2 on a light box.
- Nothing measured here diverged with the fix in place:
  - the same state at tick 710 ends at 0.311 units/s;
  - the highest crate speed in any fixed run is 2.57 units/s, in the F1 minds scene;
  - the red rooms under the fix stay under 1.36.
- That is not a proof of a bound. A light body with several points far from its centre, and several hits in one plan, is the case to watch. Section 5 suggests a guard.

### 2.6 The panic path the same defect opens [SOURCE]

For a composite shape (compound, trimesh, heightfield), parry replaces the Vec rather than writing slot 0 (`contact_manifolds_composite_shape_shape.rs:84` and `contact_manifolds_heightfield_shape.rs:119` `mem::take`; `contact_manifolds_trimesh_shape.rs:120-125` swap). In rapier's loop, a composite dynamic collider processed after any other dynamic collider then does one of two things:
- it makes the slice start `[prev_len..]` out of range;
- or it leaves `rigid_body2` as `None` for the later `.unwrap()` (`:957`).

Either is a panic, and in the wasm law a panic is a trap. Every body the law builds is a cuboid, or a capsule for a driven body, so the engine cannot reach this today. #1004's own regression test is for this case. [REASONED from source; not run]

### 2.7 The named candidates

| Candidate | Finding |
|---|---|
| The kinematic walker pressing through with infinite mass | No. The walker's contact with the crate stays at +0.0150 with zero solver impulse on 700 to 710, and its translation at 709 to 710 is 0.0016. |
| The impulses from `solve_character_collision_impulses` at character mass 1.0 | Yes, but through the overwritten manifold. The mass enters only as m·M/(m+M) ≈ 0.0225 ≈ m. Lowering it to 0.1 shrinks the impulses about threefold and moves 12 fixture tests. |
| The constraint solver alone | No. It removes speed at 710 (178.8 → 162.7) and caps the spin. |
| Position correction and its cap | No contact penetrates more than 1e-4, so there is nothing to correct. |
| Soft-contact parameters | Not involved on these quanta. |

## 3. Fixes measured

The F1 rows are `88379d5` with `7bbed41`'s open-room world; the full suite there is 286 tests. The F2 rows are `93a2d1e` with T6's margin; the suite there is 244 tests. "Probe" is the coordinator's four intents. "Suite" is the full `npm test` file list. Red rooms A and B are in section 4.1.

| # | Fix | Law | Probe: crate peak | Suite | Product golden | Red A (tick 0) | Red B | Digest on this host |
|---|---|---|---|---|---|---|---|---|
| 0 | none | F1 | 162.690 at 710 | 286/286 | `b5e62d2cc42d9ad8` | n/a | n/a | `21893224…` |
| 0 | none | F2 | 2.50 (the scene never forms) | 244/244 | `6e0d351693b18c93` | 26.06 at 53 | 400.00 at 124 | `d1c29dd9…` |
| U1 | backport #1004 (engine copy) | F1 | 2.57 | 286/286 | unchanged | n/a | n/a | `7b4cff04…` |
| U1 | backport #1004 (engine copy) | F2 | 2.50 | 244/244 | unchanged | 1.36; tick-200 hash `f436e7596fd4d6ea` | 0.98 | `cd79da03…` |
| B | rapier3d-f64 0.36.0 + parry3d-f64 0.31.1 | F2 | 2.50 | 244/244 | unchanged | 1.36; `f436e7596fd4d6ea` | 0.98 | `643af323…` |
| U2 | rapier's call once per hit, filtered to the hit collider's body (public API) | F1 | 2.50 | 272/286 | unchanged | n/a | n/a | n/a |
| U3 | no character impulses | F1 | 0.88 | 274/286 | unchanged | n/a | n/a | n/a |
| S1 | character mass 0.1 | F1 | 2.10 | 274/286 | unchanged | n/a | n/a | n/a |
| S2 | `normalized_max_linear_velocity = 10` | F2 | 2.50 | 244/244 | unchanged | 5.11 | 10.00 (capped) | `34a7fb05…` |

- **U2, U3 and S1** fail the same 12 tests: the minds, rotation and verb fixtures' frame-for-frame replays, F1 pins 5 and 6, and the restore and bundle tests built on those fixtures. U2 also fails two source-lint tests, because my version reborrows with `&mut *`. They move every push, including in scenes that never have two bodies near the walker.
  - Under U3 the probe's push at 269 is refused ("path crosses collider wall").
- **S2** bounds the speed but not the cause. In red room B the crate still reaches the cap and ends on the far side of the room.
- **Backport and bump** agree on the red rooms at every byte of every quantum's inputs and outputs (260,048 bytes of call log each). So do my change and #1004's exact change.
- **The digests** are of the wasm built on this host. The pinned artifact is the Linux build, so every row that changes code also changes `fixtures/solver.sha256` when rebuilt on Linux.

## 4. F2, F3 and the bump

### 4.1 The red rooms

Both are under F2's law, and both launch the crate. The world is also in `$S/out/squeeze-launch-red-A.json`.

**Red room A, walker pushes at tick 0.** Measured on plain `93a2d1e` and again with T6's margin, with identical hashes.
- The crate first exceeds 10 units/s at tick 53, at 26.0642 units/s. Frame hash `375c78856a5a4b15`.
- The frame hash at tick 200 is `8936cf832bc642ab`.
- The overwrite fires 19 times, first at tick 42. Quanta 42 to 53 have two dynamic colliders near the walker.

```json
{"seed":11,"world":{"name":"squeeze-launch-red","bodies":[
 {"id":"walker","x":0,"y":0.26,"z":0,"vx":0,"vy":0,"vz":0,"hx":0.25,"hy":0.25,"hz":0.25},
 {"id":"crate","x":0.75,"y":0.201,"z":0.37,"vx":0,"vy":0,"vz":0,"hx":0.12,"hy":0.2,"hz":0.12,"qx":0,"qy":0,"qz":0,"qw":1},
 {"id":"shade","x":1.2,"y":0.26,"z":0,"vx":0,"vy":0,"vz":0,"hx":0.25,"hy":0.25,"hz":0.25}],
 "colliders":[
 {"id":"floor","minX":-1.5,"maxX":3.5,"minY":-1,"maxY":0,"minZ":-1.5,"maxZ":1.5},
 {"id":"wall-west","minX":-1.5,"maxX":-1.3,"minY":0,"maxY":2,"minZ":-1.5,"maxZ":1.5},
 {"id":"wall-east","minX":3.3,"maxX":3.5,"minY":0,"maxY":2,"minZ":-1.5,"maxZ":1.5},
 {"id":"wall-south","minX":-1.5,"maxX":3.5,"minY":0,"maxY":2,"minZ":-1.5,"maxZ":-1.3},
 {"id":"wall-north","minX":-1.5,"maxX":3.5,"minY":0,"maxY":2,"minZ":1.3,"maxZ":1.5}],
 "zones":[],"minds":[]},
 "script":[{"tick":0,"kind":"intent","verb":"push","actor":"walker","target":{"body":"shade"}}]}
```

The same room with the push at tick 16, after the walker settles, needs T6's margin. On plain main that push from rest is refused ("path crosses collider floor"). With the margin, the crate first exceeds 10 units/s at tick 74, at 27.2165, frame hash `9556ff2a11272d74`.

**Red room B.** The same room with the crate at (0.6, 0.201, 0.4), the shade at (1.45, 0.26, 0.15), and the push at tick 16; it needs the margin.
- The crate first exceeds 10 units/s at tick 124, at exactly 400.0000, rapier's speed cap. Frame hash `848a52bb08a4939b`.
- The overwrite fires 170 times, on quanta 72 to 124.

**How they were found.** A grid of 540 closed rooms: the crate upright or tipped about x or z, five positions along the walker's path, either side, three gaps, and two shade distances with three offsets. All 540 pushes were admitted; 11 launched above 10 units/s under F2. "Smallest" here means three bodies in a 5 × 3 room. I did not search for anything smaller.

### 4.2 The control, and what the fix moves

| Run | Quanta | Passes with a dynamic collider near the walker | Quanta with two or more | Fix off vs wasm | Fix on vs wasm |
|---|---|---|---|---|---|
| minds scene (F1) | 1,274 | 770 | 103 (609-711) | bit for bit | first differs at 617 |
| product scene, `harness/sim.mjs` (F2) | 10,000 | 0 | 0 | bit for bit | bit for bit |
| `harness/course.test.js`, 10 tests (F2) | 9,044 | 0 | 0 | bit for bit | bit for bit |
| `harness/outcome.test.js`, 6 tests (F2) | 82,752 | 0 | 0 | bit for bit | bit for bit |
| red A, tick 0, plain main (F2) | 200 | 208 | 12 (42-53) | bit for bit | first differs at 45 |
| red A, tick 16 (F2) | 200 | 263 | 23 (57-74, 117-121) | bit for bit | first differs at 63 |
| red B (F2) | 200 | 252 | 53 (72-124) | bit for bit | first differs at 72 |

On the red rooms the first difference always falls on a quantum with two dynamic colliders near the walker. Some of those quanta change nothing, when the overwritten points fall outside the prediction distance. The product scene never brings a dynamic collider near the walker, so no route can move its golden.

### 4.3 Bump or backport

**What 0.36.0 changes, as a source diff of `rapier3d-f64-0.35.3/src` against `0.36.0/src`, and `parry3d-f64-0.30.2` against `0.31.1`.**
- `control/character_controller.rs` changes by #1004 only, plus soft-body test plumbing. `move_shape` is unchanged, so `kcc.rs` needs no re-sync.
  - Its outcome still rests on parry, which moves to 0.31.1 (55 source files differ). The suite, the golden and the red rooms say parry's move did not reach anything the engine measures.
- The solver, CCD, island manager, narrow phase and collider set all change. Soft bodies are added.
  - `ContactPair::manifolds` becomes a method; only code that reads pairs directly notices.
  - The law compiles against 0.36.0 with no source change, and its wasm passes `solver/lint.mjs`.
- `ContactData` has the same public fields in both versions, so the snapshot's layout (`rebuild_snapshot` / `push_contact`) is the same. The golden, the restore tests and T2's image round-trips pass.
- Determinism: on this host the bumped native build replays the bumped wasm bit for bit on both red rooms. A Linux build was not made.
- #1003 (CCD fixed-target cache invalidation) and #1012 are in the range.
  - #1012's broad-phase changes are renames (`update_scratch` becomes `update_workspace`, and similar).
  - `query_pipeline.rs` still resolves a BVH leaf through `colliders.get_unknown_gen(id)`, now inside `handle_of`.
  - `ColliderSet::remove` is refactored into `remove_internal` and now takes the soft-body set.
  - None of these changes the leaf-to-collider path that slot-alias asks about. That question is answered separately.

**How the two routes compare.**
- **The backport** is surgical: one function, a NOTICE entry, and a control test shaped like F2's.
- **The bump** carries more upstream fixes, and more unmeasured surface: CCD, islands and the solver outside what the suite exercises.
- Every engine measurement taken is identical between them, including every byte of the red rooms.

## 5. Caveats and what was not measured

- **The amplifier** (section 2.5) is not fixed by either route. A cheap guard is a law test that fails when a pushed body leaves a push faster than a stated multiple of the pusher's speed.
  - Later (2026-09-26): rapier master (`b716d375`) keeps the same mass ratio; its `character_controller.rs` is identical to 0.36.0's.
  - The amplifier alone launches thin light bodies. On 0.36.0, one frame launches a box with half-extents 0.06, 0.2, 0.12 at 44 times the character's speed.
  - `push-mass.md` measures the effective-mass fix on F3's law.
- **Platforms.** Only x86_64 native and wasm32 under node on Windows. The frame hashes are platform-identical by design, and Linux was not run.
- **Search coverage.** Red rooms come from one 540-candidate grid, box walker (shape 0) only. The capsule character, heightfields and more than two dynamic bodies were not tried.
- **"0.036 into the floor."** The narrow phase does not show it on 700 to 710 (section 2.4). I did not trace the sweep's own measure.
- **Upstream.** Rapier fixed the overwrite in #1004 (`bd7a2f2e`, released in 0.36.0). Later, on 2026-09-26:
  - the amplifier was reported as dimforge/rapier#1020, with a standalone repro;
  - a comment on dimforge/rapier#1009 shows that issue's two panics, at `:944` and `:957`, are #1004's bug. Both reproduce with a compound on 0.35.3, and both are gone on 0.36.0.
- **The second question** (the first downward cast missing the floor) is not in this file. Its answer follows separately.

## Commands

`S` as above. All builds use `cargo +1.98.1`; all node runs use v22.22.3.

```
git clone -q -c core.autocrlf=false https://github.com/mcp-tool-shop-org/si-rpg-engine.git $S/engine
cd $S/engine && git fetch origin pull/75/head:pr75 && git checkout 88379d5
git show 7bbed41:fixtures/behavior-minds.json > $S/minds-7bbed41.json
node solver/build.mjs && node $S/patch_glue.mjs solver/dist/solver.mjs
node $S/probe.mjs $S/minds-7bbed41.json 1274 --trace 700,712 --record $S/out/f1.calls.bin     # 162.690 at 710; 35f70795965dd5f4
python $S/make_harness.py $S/engine/solver $S/harness && cd $S/harness && cargo +1.98.1 build --release --locked
./target/release/replay.exe $S/out/f1.calls.bin [--variant copy-impulses|copy-impulses-fixed|copy-impulses-1004] [--trace A,B] [--from-tick T] [--list-flagged] [--dump F]
# F2 worktrees: 93a2d1e + `git cherry-pick -n 6e41ccd`; the bump: rapier3d-f64 "0.36.0" in solver/Cargo.toml, then
cargo +1.98.1 update -p rapier3d-f64 --precise 0.36.0
bash $S/measure.sh <engine-dir> base|u1-fixed-copy|u2-hit-body-only|u3-no-impulses|s1-mass-0.1|s2-maxlin-10 $S/minds-7bbed41.json <tag>
node $S/search.mjs $S/out/search1-f2.json                                                      # 540 rooms, 11 above 10 u/s
PUSH_TICK=0 SOLVER_LOG=$S/out/red-A0-main.calls.bin node --import file:///$S/recorder.mjs $S/red.mjs '{"orient":"upright","cx":0.75,"cz":0.37,"sx":1.2,"sz":0}' 200 --world $S/out/squeeze-launch-red-A.json
SOLVER_LOG=$S/out/f2-product.calls.bin node --import file:///$S/recorder.mjs harness/sim.mjs  # and harness/course.test.js, harness/outcome.test.js
gh api repos/dimforge/rapier/commits/bd7a2f2e -H "Accept: application/vnd.github.v3.diff"; gh api repos/dimforge/rapier/compare/v0.35.3...v0.36.0
```
