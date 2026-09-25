# Driven switch: does main's Rapier world rebuild at verb boundaries, and can the switch happen in place?

An answer to si-rpg-engine's coordinator, measured 2026-09-25.

**Pins.**
- Engine: GitHub `main` at `76a8eef`. Every engine citation below is `@ 76a8eef`.
  - At `5ec07f0` the logic is the same. `rapier_law.rs` differs only by the since-removed `solver_clear_warmstart`, so from `ensure()` on its lines are 15 higher there.
- Rapier: rapier3d-f64 0.35.3 (`enhanced-determinism`) and parry3d-f64 0.30.2, read in the local cargo registry.
- Toolchain: rustc and cargo 1.98.1 (48a229cea), node v22.22.3, on Windows 11 x86_64.

**Scratch.** `$S` = `<scratchpad>/driven-switch/`, a session scratch directory that is not kept in this repo.
- `$S/engine` is a clone of GitHub main with two scratch branches:
  - `probe-rebuilds` (`4355775`): a rebuild counter;
  - `inplace-switch` (`7dae856`): a prototype of the in-place switch.
- Builds used the repo's own `node solver/build.mjs` with `CARGO="cargo +1.98.1"`.
- Nothing was written, built or run inside `E:/AI/si-rpg-engine`.

**Evidence levels.**
- [MEASURED] means I ran it; the command is given.
- [SOURCE] means a file:line read at the pin above.
- [REASONED] means an inference; its basis is named.

## Answer

- **Rebuild at verb boundaries: yes.** Every quantum where an actor enters or leaves the driving set, and every pick-up and drop, changes the driven or carried mask, and `ensure()` rebuilds the whole Rapier world. [SOURCE] A counter in a scratch build that still prints the golden `fd2f6c03fb982d77` finds 3 rebuilds in the product scene's 10,000 quanta (0.30 per 1,000, at ticks 201, 261, 401), 5.9 and 15.8 per 1,000 in the verb fixture's climb and carry cases, 6.0 in the minds fixture, and 0 in the constant-mask solver fixtures. Each product-scene rebuild drops 18–20 warm-start impulses and wakes 5 sleeping bodies. [MEASURED]
- **In place: yes, with public 0.35.3 calls.** The driven switch takes `set_body_type`, `lock_rotations`, `set_additional_mass`/`set_additional_mass_properties` and the `activation_mut()` thresholds, then `set_rotation`/`set_linvel`/`set_angvel` with the type set first, plus `Collider::set_shape` in shape-1 worlds. A carried body takes `remove_body` + `insert` (a new handle generation) or `set_enabled` (the same handle). Contact pairs survive the switch, and bodies it does not touch keep sleeping. [SOURCE+MEASURED]
- **Cost to determinism:** the goldens move once (the prototype's product digest is `c302031a6302814f`, first different at tick 201), and the in-place law replays and image-restores bit for bit; but Rapier's hidden state then crosses verb boundaries, so even a no-op type round trip moves later bits, by 9.5e-5 here. [MEASURED]

## 1. Main rebuilds the world at every verb boundary

### The path [SOURCE]

1. **The tick builds the driving set.** Each quantum, `advance()` builds `driving` from the actions whose effect is drive, climb, carry or release (`tick.js:148-150`, `197-203`) and steps the world with it (`204`).
   - An action leaves the map after its last quantum (`213-226`), so the next quantum's set lacks the actor.
   - `use` (effect `episode`) never drives.
   - The carry and release actions call `world.carry`/`world.release` on their last quantum (`tick.js:166-172`).
2. **The world sets each body's mode.** `world.step` calls `solverModes(driving)` (`world.js:162`, `112-125`): 3 if carried, 2 if driving and lifted, 1 if driving, else 0. `carry` and `release` edit `carriedBy` (`world.js:832-839`, `848-875`).
3. **The binding writes the mode into slot 16.** `writeInputs` writes `solverMode` there (`build.mjs:181`; at load, when no mode is set yet, it falls back to `driven.has(id)`). `stepSolver` then calls `solver_step` (`build.mjs:253-259`).
4. **The solver compares signatures and rebuilds.**
   - `signature()` folds modes 1 and 2 into `driven`, and mode 3 into `carried` (`rapier_law.rs:186-205`).
   - `same_sig` compares both masks (`266-267`), and `ensure()` rebuilds when they differ (`680-688`).
   - `build_world` builds a new `PhysicsWorld`: statics first, then bodies in record order. A carried body gets `None` (`397-402`); a driven body the kinematic builder, with identity rotation (`403-412`); a dynamic body its record pose, through `canon_quat` (`393`, `413-424`).
   - It then runs the load pass `warm_broadphase` (`442`, `305-325`), which wakes every non-fixed body (`320-324`).

Modes 1 and 2 are both in the driven mask. So a climb's rise turning into its walk (2 → 1) does not rebuild; every other mode change does. [SOURCE]

### Measured [MEASURED: `node harness/probe-rebuilds.mjs` on `probe-rebuilds`]

The probe replays the product scene, the verb and minds fixtures, and the solver fixtures. Every fixture frame matched its fixture, so the counter changes no behaviour.

| run | quanta | rebuilds after load | per 1,000 | frame tick: cause |
|---|---|---|---|---|
| product scene (golden run) | 10,000 | 3 | 0.30 | 201 climber starts (0→2); 261 climber ends (2→0); 401 parcel picked up (0→3) |
| verbs: climb | 171 | 1 | 5.85 | 1 walker starts (0→2). The rise→walk toggle (2→1) does not rebuild. |
| verbs: carry | 253 | 4 | 15.81 | 42 walker starts; 104 crate picked up; 251 crate dropped; 252 walker ends |
| verbs: refusals | 0 | 0 | – | – |
| minds | 498 | 3 | 6.02 | 42 walker starts; 76 crate picked up; 493 walker ends |
| solver fixtures, 18 cases (constant masks) | 1,320 | 0 | 0 | – |
| **total** | 12,242 | 11 | 0.90 | |

**Back-to-back driving verbs rebuild once at each end, not per verb.** In the carry case, pick-up, move and drop run back to back, so the walker stays in the driven set from tick 42 to 251.

**What each rebuild discarded**, read from the old world just before it was dropped:
- **Product scene, each of the three:**
  - 5 contact pairs holding points, and 18–20 nonzero `warmstart_impulse`s;
  - 5 sleeping bodies woken: lower, upper, tip, slider, parcel;
  - one dynamic body's quaternion bits replaced by the re-canonicalized record: renormalized at 201 and 401, sign-flipped at 261.
- **Carry case:**
  - tick 42: 2 pairs, 8 impulses, 2 sleepers;
  - tick 104: nothing, because the crate was airborne (the walker's approach had lifted it to y 0.31–0.32 at ticks 100–103);
  - tick 251: nothing, because the crate was carried and the walker, being kinematic, has no pair with the slab;
  - tick 252: 1 pair, with impulses still 0.
- **Minds fixture:**
  - tick 42: 4 pairs, 16 impulses, 4 sleepers, and 2 bodies whose record did not survive `canon_quat` bit for bit (the known non-idempotence, here on a record that was already canonical);
  - tick 76: 5 pairs, 11 impulses, 2 sleepers;
  - tick 493: 2 pairs, 8 impulses, 2 sleepers.

### The T4 builder's report, checked [MEASURED: `node harness/probe-product-snap.mjs 199-203 259-263 399-403`]

**Where and why.** The rebuild the T4 builder traced at quantum 260 happens in the quantum stepped with `applyProductAct(world, 260)`, which is frame tick and T1 trace line 261: the same event, numbered from the step index in one case and from the trace in the other. Its cause is the driven mask: the climber leaves the driven set when its lift window, `step >= 200 && step < 260` (`product-scene.mjs:36`), closes.

**What the snapshot shows.**
- At tick 260, lower, upper, tip, slider and parcel are asleep. At tick 261 none is.
- The stack is re-solved from zero warm start:
  - lower/upper held 4 points summing 3.906166e-3 at rest;
  - after the rebuilt world's first step it has 3 points summing 5.014306e-3, then 3.682153e-3 and 3.943487e-3;
  - floor/lower goes 7.812409e-3 → 8.984330e-3 → 7.570251e-3.

**The other two boundaries do the same.**
- Index 200 (tick 201): lower/upper goes 3.906509e-3 → 4.592406e-3.
- Index 400 (tick 401): the parcel is picked up.

### A correction to this wave's own notes

`dispatch.md` records, under the `canon_quat` advisor measurement, that a persistent run never applies `canon_quat` twice. That holds only between verb boundaries:
- every verb-boundary rebuild runs the already-canonical record through `canon_quat` again (`rapier_law.rs:393` → `159-162`);
- the minds run shows it moving bits at tick 42.

[MEASURED]

## 2. The switch can be done in place, through public 0.35.3 calls

### Property by property [SOURCE: rapier3d-f64 0.35.3]

| `build_world` sets | in-place call on the running body | flag raised / note |
|---|---|---|
| type: `kinematic_position_based` or `dynamic` | `RigidBody::set_body_type(t, wake)`, `rigid_body.rs:252-269` | Raises `TYPE` (254). Zeroes velocities only for `Fixed` (257-259). Refreshes world mass properties (263). |
| `lock_rotations()` | `lock_rotations(bool, wake)`, `327-338` | No flag; the flags and world mass properties update at once. |
| `additional_mass(1.0)`, or none | `set_additional_mass(1.0, _)`, `591-596`. To go back: `set_additional_mass_properties(MassProperties::default(), _)`, `615-620`. | Raises `LOCAL_MASS_PROPERTIES` (630). The recompute treats `MassProps(default)` exactly as no additional mass (`rigid_body_components.rs:428-432, 450-453`). |
| `can_sleep(false)` / `(true)` | No setter. The builder writes the two thresholds (`rigid_body.rs:2003-2006`); `activation_mut()` (`184-187`) exposes them as pub fields (`rigid_body_components.rs:1297-1321`). | Raises `SLEEP`. |
| `time_until_sleep = 32·dt` | `activation_mut().time_until_sleep` | Raises `SLEEP`. |
| rotation: identity (driven) or the record's `canon_quat` (dynamic) | `set_rotation(q, _)`, `rigid_body.rs:1016-1030`; sets `position` and `next_position` | Raises `POSITION`. |
| velocities: zero (kinematic) or the record's (dynamic) | `set_linvel` / `set_angvel`, `905-917` and `943-955` | Both are **ignored on a position-based kinematic** (914, 952). Going dynamic, set the type first; going kinematic, zero the velocities first. |
| `ccd_enabled(false)` | `enable_ccd(false)`, `501` | Already off. |
| collider: `capsule_y` for a driven body in a shape-1 world, else `cuboid` | `Collider::set_shape(SharedShape)`, `collider.rs:530-533` | Raises the collider's `SHAPE`. |
| cannot be set | `RigidBodyActivation::sleep_prev_pose` is `pub(crate)` (`rigid_body_components.rs:1325`) | A rebuilt body starts from `Pose::IDENTITY` (`1356-1365`); an in-place body keeps its last dynamic pose. |

### What the next `PhysicsPipeline::step` does with those flags [SOURCE]

- **Order.** `step_inner` takes the modified sets (`substep.rs:306-315`) and runs both user-change handlers (`309-324`) before collision detection (`380-394`).
- **The body.** `rigid_body_updated` runs (`user_changes.rs:81-87` → `manager.rs:257-316`).
  - The body keeps its active-set slot and its persistent island. Every enabled non-fixed body is a member, kinematic or dynamic (`persistent.rs:1`).
  - A `TYPE` or `SLEEP` flag wakes it (`manager.rs:308-315`).
  - `TYPE` marks each of its colliders `PARENT_EFFECTIVE_DOMINANCE` (`user_changes.rs:108-119`). `LOCAL_MASS_PROPERTIES` recomputes its mass from its colliders (`177-186`).
- **The narrow phase.** A collider with such a change (`needs_narrow_phase_update`, `collider_components.rs:55-62`) is handled like this:
  - it wakes its parent and every contact partner (`pair_management.rs:235-258`);
  - it re-colours its pairs and unlinks and relinks their persistent-island links (`263-316`);
  - **no pair is removed** (only a sensor change moves pairs, `322-352`), so pairs and their manifold points keep their warm-start fields through the switch.
- **The contact update.**
  - A changed collider is never recycled (`pair_update.rs:116-121`).
  - Pairs are filtered by body type (`237-244`) under the default `DYNAMIC_DYNAMIC | DYNAMIC_KINEMATIC | DYNAMIC_FIXED` (`collider_components.rs:339-345`). So a new kinematic body's pairs with static geometry are emptied (`narrow_phase/mod.rs:177-184` → `contact_pair.rs:392-398`).
  - Its pairs with dynamic bodies are recomputed from their old manifolds. Parry moves warm-start data to the new points by feature id (`contact_manifolds_cuboid_cuboid.rs:79-99`, `contact_manifold.rs:821-830`).
  - A `SHAPE` change drops the pair's workspace (`pair_update.rs:283-288`).
- **The broad phase.**
  - The collider's BVH leaf is removed and re-inserted as new, forcing a full refit (`broad_phase_bvh/update.rs:74-94, 270, 288-294`).
  - Its pairs stay in the pair map until their AABBs separate (`441-601`).
  - A fresh build never creates a kinematic–fixed pair (`361-385`). In place, that emptied pair stays in the graph, and in the law's snapshot as a zero-point pair (`rapier_law.rs:636-661`).
- **Sleep.**
  - In place, only the switched body and its contact partners wake, with their whole persistent islands (`sleep.rs:42-70`).
  - The rebuild wakes every body and zeroes every timer (`rapier_law.rs:320-324`; `rigid_body_components.rs:1396-1402`).

**In the experiment below [MEASURED]:**
- The in-place switch leaves all 5 pairs and their warm-start sums untouched.
- After the next step, ground–s is empty, s–t continues (3 → 6 points, 3.9064e-3 → 4.1214e-3), and the stack is untouched and asleep: 3 of 5 bodies asleep, against 0 of 5 after a rebuild.
- s's rotation reset rebuilt the s–t manifold, so that one pair ends within 1e-4 relative of the cold rebuild (4.1215e-3).

### Carried bodies [SOURCE; handles MEASURED]

- **Removal.** `PhysicsWorld::remove_body` (`physics_world.rs:216-225` → `rigid_body_set.rs:201-238`) takes the body out of the active set by `swap_remove` (`manager.rs:64-114`) and removes its collider (`collider_set.rs:335-367`).
  - The next step removes the collider's graph node, wakes its contact partners, and swap-removes its edges (`pair_management.rs:39-66, 78-200`). That renumbers another pair's edge and invalidates the solver graph (`162-166`).
  - The BVH drops the leaf and its pairs without events (`update.rs:55-57, 450-459`).
- **Insertion.** `PhysicsWorld::insert` (`physics_world.rs:184-194`). On the next step the body is appended to the active set (`manager.rs:275-299`) and gets a new BVH leaf.
- **Handles.** An `Arena` has one `generation` counter (`arena.rs:30`), raised on every removal (`366`).
  - An insert takes the current generation (`210`, `269`) and the most recently freed slot (a LIFO free list: `265`, `367`).
  - Measured: after remove + insert, the body and the collider go from (5, 0) to (5, 1); a fresh build gives (5, 0).
  - The law's snapshot writes both halves of every pair key (`rapier_law.rs:644-649`), so the generation reaches the hash. The engine prototype's snapshot shows it: pair key `2.0-3.1` after the carry case's drop.
- **The alternative, `set_enabled(false/true)`, keeps both handles** (measured: (5, 0) throughout).
  - A disabled body leaves the islands (`user_changes.rs:168-171, 192-201`).
  - Its collider is treated as removed (`substep.rs:326-334`).
  - Re-enabling it raises every change flag (`rigid_body.rs:195-209`).

### Two traps for any in-place design [SOURCE]

1. **Query timing.** `integrate()` runs the character controller's queries (`rapier_law.rs:513-550`) before `world.step()` (`552`), and the query resolves BVH leaves through `get_unknown_gen` (`query_pipeline.rs:109, 298, 386, 428, 552`). So in the quantum of a switch:
   - a removed collider disappears from the query at once;
   - an inserted one is invisible until that step's broad-phase update;
   - a just-disabled one is still hit at its old pose, because `QueryFilter::test` does not check `is_enabled()` (`684-694`).
   - This is why `build_world` needs its load pass (`rapier_law.rs:299-304`).
2. **The load pass must not be reused on a running world.**
   - `CollisionPipeline::step` handles body changes with `islands: None`, then clears their flags (`collision_pipeline.rs:168-185, 210`). A type change consumed there never reaches `rigid_body_updated`, and the persistent-island relink is skipped (`pair_management.rs:299`).
   - It also runs a dt = 0 contact update over every awake pair, and the law's version wakes every body (`rapier_law.rs:320-324`).
   - In a debug build the load pass trips `debug_assert!` at `dynamics/island_manager/manager.rs:140` (via `contacts.rs:351`) whenever the rebuilt world has a touching pair, because its bodies are not yet in the active set. The oracle measures this on the law's own rebuild, below. Every verb-boundary rebuild with resting bodies is therefore release-only code, as T2 pin 8 already assumes for native tests.

## 3. Cost to determinism

### The goldens move once [MEASURED on `inplace-switch`]

**The prototype.**
- `ensure()` reloads only on world id, counts, grid, geometry or shape.
- A mask change calls `switch_in_place` in record order, using the calls in section 2.
- A carried body is removed with `remove_body` and dropped back with an `insert` built as in `build_world`. There is no load pass.

**What moved.**
- **Product digest:** `fd2f6c03fb982d77` → `c302031a6302814f` (`node harness/sim.mjs`, twice).
- **`node harness/first-difference.js trace-rebuild.txt trace-inplace.txt`:** first difference at tick 201, body `lower`, field `x`: `5.99950738061522` on main against `5.999512067457441` in place.
  - That is the first verb boundary, in a body the verb never touches: main's rebuild woke and re-solved it, the prototype left it asleep.
- **Product behaviour numbers** (`node harness/probe-golden-behaviour.mjs`, against `fixtures/golden-behaviour.json`): 11 move.
  - The final x, y and z of lower and upper, by up to 6.4e-5.
  - The x and y of tip and slider, by at most 4e-8.
  - The last snapshot, 1840 → 1784 bytes.
  - Sleep quanta, the walker's zone, and the walker, climber and parcel finals do not move.
- **Verb fixture** (`node harness/probe-behaviour.mjs`):
  - climb: identical frame for frame (its one switch comes before any contact or sleep exists);
  - refusals: identical;
  - carry: first differs at frame 42 and runs 255 frames instead of 254. The crate ends at (3.270706, 0.242848, 0.007373) instead of (3.143616, 0.241764, 0.231861).
  - Every verb is still admitted with the same episodes, and the carry assertions in `verbs.test.js` still hold.
- **Minds fixture:** first differs at frame 42. Its episodes and beliefs change, so its recorded log no longer replays.
- **Solver fixtures:** they have no mask change, so they take main's path (0 switches measured).
- **`node --test` over package.json's test list:** 117 of 124 pass. The 7 failures are all golden or fixture comparisons:
  - `check.test.js` ×3;
  - the golden trace test;
  - the verb and minds fixture replays;
  - `restore.test.js`'s minds case, which replays the fixture's recorded log and is refused at entry 1 as a stale frame.

### Deterministic under replay [MEASURED]

- **The prototype's product trace, run twice:** `first-difference` reports `identical` over 10,001 lines.
- **`restore.test.js` on the prototype** (`node --test harness/restore.test.js`): replay and image restores rerun identically at every chosen point, for the product scene and 22 fixture cases (21 on the product law, 1 on the reference law), the carry case included. The chosen points include a third and two thirds of each run, so they fall after the carry case's first two switches and after all three product switches. Only the minds case fails, for the recorded-log reason above.
- **The oracle program:** the in-place run twice in one process gives state hash `a756eee8721a4e1a` both times, and the debug and release rapier builds agree bit for bit on every in-place line.

So the same call sequence gives the same bits. The tick's log fixes the call sequence: which bodies switch in a quantum is a function of the masks and record order. [REASONED from `switch_in_place` walking the records in order]

### History the snapshot does not see

- **What the snapshot captures:** handle generations (in the pair keys), emptied kinematic–fixed pairs (as zero-point pairs), and the sleep flag and timer (`rapier_law.rs:630-632`). [SOURCE]
- **What it does not capture:** [SOURCE, sites in section 2]
  - the BVH shape (a forced re-insertion on every type switch);
  - contact-graph edge order (swap-removed on each removal);
  - solver colours and persistent-island links;
  - active-set order (a swap_remove on removal, an append on insert or wake);
  - `sleep_prev_pose`, the recycle state, and the retired-pair pool.
- **The measured effect:** a type round trip at q96 (`set_body_type(Dynamic)` then `(KinematicPositionBased)`, before the step) changes no body field. Yet it moves positions from q96 on, by 9.526e-5 at q192. [MEASURED]
- **Today and in place.** Two worlds with equal records are not interchangeable after a switch.
  - Today that holds only between two verb boundaries, because each rebuild resets all of this to a fresh build.
  - In place, it accumulates over the whole run.

### What replay would not reproduce

Nothing, given the same binary, the same log and the same starting world (measured above). The risks:

1. **A mid-run reload from records.** Examples are a restore through `build_world`, or a tool that rebuilds a world from a frame. Such a reload diverges from the continuous run from the first switch on; the oracle shows A ≠ B from q65. S1 pin 11 already forbids restoring by reload. In place, the verb-boundary reloads that main performs today disappear.
2. **Switch order within a quantum.** It must be record order, never a map's iteration order. The Rapier paths the switch touches order their work by sort: stale pairs (`update.rs:568-576`), touch transitions (`contacts.rs:308`) and colouring (`371-374`). [SOURCE]
3. **The shared wasm instance.** Every world in one JS process shares it (`build.mjs` `instantiate`), so a world's heap layout depends on the worlds before it. Nothing here showed a dependence on addresses: the in-process runs twice were identical, and the restore tests pass in one process. That is evidence, not proof.
4. **Carry history reaches the hash.** Handle generations now depend on the carry history (S1 pin 9): two runs that reach the same records through different pick-up and drop sequences hash differently.

## 4. The experiment

**Program.** `$S/driven_switch.rs`: 378 lines, SHA-256 `56a0e5bf7cb1a31233c15c3d2f57e5e50ab10b0e8e989293db8245d349327b6f`.
- It copies `canon_quat`, `warm_broadphase`, the two builders and `write_body`'s record rule from `rapier_law.rs`, with the law's integration parameters.
- **Scene:**
  - a fixed slab with its top at y = 0;
  - a 3-box stack a0–a2 at x = 0;
  - a switcher s at x = 1.5, with a rider t on it;
  - half-extents 0.25; load gaps 0.03, wider than the 0.02 prediction distance (`integration_parameters.rs:395`), so the load pass itself does not trip the debug assert.
- **Schedule:** s is dynamic for q1–64, driven at +0.5 u/s along x for q65–128, and dynamic again to q192.
- **A** rebuilds from records at each switch, as the law does. **B** switches in place (section 2).
- **Checks:**
  - B's pairs and warm-start sums around the switch, and B run twice;
  - A against B;
  - B plus `wake_up_all`, to split waking from the warm-start loss;
  - a no-op round trip;
  - a carried cycle both ways.

**Command.**

```
cd E:/AI/readouts/rust-knowledge && python scripts/compile_oracle.py file $S/driven_switch.rs --expect runs --edition 2021 --deps rapier3d_f64 --stdout "<the 18 lines below>"
```

Result: `"ok": true`, `"note": "ran as expected"`, exit 0, rustc 1.98.1, oracle rapier in debug.

**Exact stdout:**

```
B (in place) twice: state hash a756eee8721a4e1a / a756eee8721a4e1a, identical true
B q64 before switch: asleep 5/5, pairs ground-a0:4pt/1.1716e-2 ground-s:4pt/7.8127e-3 a0-a1:3pt/7.8095e-3 a1-a2:4pt/3.9048e-3 s-t:3pt/3.9064e-3
B q64 after switch, before step: pairs ground-a0:4pt/1.1716e-2 ground-s:4pt/7.8127e-3 a0-a1:3pt/7.8095e-3 a1-a2:4pt/3.9048e-3 s-t:3pt/3.9064e-3
B q65 after step: asleep 3/5, pairs ground-a0:4pt/1.1716e-2 ground-s:0pt/0.0000e0 a0-a1:3pt/7.8095e-3 a1-a2:4pt/3.9048e-3 s-t:6pt/4.1214e-3
A (rebuild as the law: build_world + warm_broadphase) aborted at rapier dynamics/island_manager/manager.rs:140 on the rebuild before q65; A below rebuilds without the load pass; twice identical true
A q64 before switch: asleep 5/5, pairs ground-a0:4pt/1.1716e-2 ground-s:4pt/7.8127e-3 a0-a1:3pt/7.8095e-3 a1-a2:4pt/3.9048e-3 s-t:3pt/3.9064e-3
A q64 after switch, before step: pairs
A q65 after step: asleep 0/5, pairs ground-a0:4pt/1.4775e-2 a0-a1:5pt/1.0814e-2 a1-a2:4pt/5.3750e-3 s-t:6pt/4.1215e-3
A vs B: first differing quantum q65 (through q64 identical)
q65: max |A-B| position: all 2.798e-4, stack 2.798e-4, s+t 1.242e-8
q72: max |A-B| position: all 1.244e-2, stack 1.244e-2, s+t 1.833e-6
q96: max |A-B| position: all 2.120e-2, stack 2.120e-2, s+t 2.940e-6
q129: max |A-B| position: all 2.121e-2, stack 2.121e-2, s+t 2.942e-6
q192: max |A-B| position: all 2.142e-2, stack 2.142e-2, s+t 2.891e-6
B + wake_up_all at each switch: stack vs B at q192 2.087e-3, stack vs A at q192 1.935e-2
B + no-op set_body_type round trip at q96: first differing quantum q96, max |diff| at q192 9.526e-5
remove_body + insert: t body (5, 0) -> (5, 1), collider (5, 0) -> (5, 1) (fresh build: (5, 0), (5, 0)); bodies woken by the removal 1; pair keys (0, 0)-(1, 0) (0, 0)-(4, 0) (0, 0)-(5, 1) (1, 0)-(2, 0) (2, 0)-(3, 0)
set_enabled(false/true): t body stays (5, 0), collider (5, 0); bodies woken by the disable 1; t ends at x 3.010497, y 0.249944
```

**The law's rebuild in release [MEASURED].** The same file was built natively in release: `$S/native`, with `Cargo.lock` copied from `solver/`, run with `cargo +1.98.1 build --release --offline --locked`.
- Only the two A lines change:
  - `A (rebuild as the law: build_world + warm_broadphase) completed; twice identical true; same run without the load pass differs first at q65`
  - `A q64 after switch, before step: pairs ground-a0:4pt/0.0000e0 a0-a1:5pt/0.0000e0 a1-a2:4pt/0.0000e0 s-t:6pt/0.0000e0`
- Every other line is identical. So the load pass changes bits but none of the printed digits, and the debug run's A stands in for the law's.

**What it shows:**
- **In place keeps the pairs and their warm-start fields through the switch.** Only the kinematic–fixed pair empties.
- **In place leaves an untouched sleeping stack asleep; the rebuild wakes it and starts it cold.**
  - The stack had settled leaning, its top box 2.1e-2 off-axis in x and z.
  - Woken by the rebuild, it straightens (top box within 5e-4 of the axis by q192); in place it stays asleep, leaning. [MEASURED with a one-off diagnostic print of the same program]
  - Waking alone moves it 2.1e-3. Most of A's 2.1e-2 is the cold start.
- **The switched pair itself differs little.** s and t differ by at most 2.9e-6 between A and B.
- **Deterministic, but history-bound.** The in-place path is bit-reproducible, yet it carries history that the records do not show.

## 5. What a later slice would change

### The smallest in-place design that keeps replay deterministic

This is what `inplace-switch` does, in about 110 lines of `rapier_law.rs`.

1. **Split the reload test.** `ensure()` reloads only when the world id, counts, rows/cols/cell, geometry or shape differ; S1 pin 15's geometry bytes stay in that test. The two masks stay in `Signature` as the last state applied.
2. **When only the masks differ, switch in record order.** Walk the bodies in record order, apply each transition, store the new masks, and rebuild the snapshot:
   - **to driven:** `set_linvel(0)`, `set_angvel(0)` (while still dynamic), then `set_body_type(KinematicPositionBased)`, `lock_rotations(true)`, `set_additional_mass(1.0)`, `set_rotation(identity)`, thresholds −1, `wake_up(true)`. In a shape-1 world, add `set_shape(capsule)`.
   - **to dynamic:** `set_body_type(Dynamic)` first, then `lock_rotations(false)`, `set_additional_mass_properties(MassProperties::default())`, `set_rotation(canon_quat(record))`, the record's `set_linvel`/`set_angvel`, the default thresholds, `time_until_sleep = 32·dt`, and `wake_up(true)`. In a shape-1 world, add `set_shape(cuboid)`.
   - **pick-up:** `remove_body`.
   - **drop:** `insert`, with `build_world`'s builder applied to the record.
3. **No load pass for a switch.** Pin the consequence instead: a dropped body is invisible to that quantum's character queries (section 2, trap 1).
4. **Keep `build_world`** for the first load and for geometry changes.

### What would move (measured on the prototype)

- the product golden;
- `golden-behaviour.json` (11 numbers);
- the carry case of `behavior-verbs.json`;
- `behavior-minds.json`: frames, episodes, beliefs and log hashes;
- the Linux binary digest.

The climb case, the refusals, the solver fixtures and the arithmetic golden stay.

### Tests that should go red on main and green in place

1. **Untouched sleepers stay asleep.** In the product scene, lower, upper, tip, slider and parcel stay asleep through ticks 199–202 and 259–262, and all but the carried parcel through 399–402. Main wakes all five at 201, 261 and 401.
2. **Untouched warm starts survive.** Every untouched resting pair keeps its warm-start fields through each switch quantum; on main, lower/upper goes 3.906509e-3 → 4.592406e-3 at 201.
3. **No rebuild after load**, in the product scene and in every fixture.

Items 1 and 2 are already green on the prototype: `node harness/probe-product-snap.mjs 199-202 259-262 399-402` on `inplace-switch` shows the five asleep throughout, and lower/upper at 3.906509e-3 and floor/lower at 7.812789e-3 at every printed tick. [MEASURED]

### Tests that hold the in-place contract

1. **Restores straddle every switch.** Replay and image restores at points on both sides of each switch: 200/201, 260/261 and 400/401 in the product scene; 42, 104, 251 and 252 in the carry case.
2. **Velocities survive the return to dynamic.** A body switched back to dynamic keeps its record velocity; calling `set_linvel` before `set_body_type` silently drops it.
3. **Generations reach the hash.** S1 pin 9's removal case now runs through carry: after a drop, a pair key carries generation 1.
4. **Shape-1 worlds.** A switch in a shape-1 (capsule) world; no fixture has one.

## 6. Caveats and what was not measured

- **One host.** Every wasm was built on Windows. The unmodified build reproduces the pinned golden, so `c302031a6302814f` is what I expect a Linux build of the prototype to print, but no Linux build was made. The digests pinned from Linux were not re-pinned.
- **The prototype is a scratch design** that no one has reviewed. Its numbers are what this prototype printed, not a reviewed law.
- **The oracle scene is simplified.** It uses boxes only and a prescribed kinematic motion, not the character controller.
- **Not measured:**
  - the runtime cost of a rebuild against an in-place switch;
  - the capsule (`set_shape`) path, since no run changes a mask in a shape-1 world;
  - the hazard suite;
  - ARM64.
- **Scenarios that pre-set `carrying` before the load should rebuild on quantum 1.** The load fills slot 16 from `driven.has(id)`, because no mode is set yet (`world.js:517-521`, `build.mjs:181`). [REASONED, not run]
- **The per-1,000 rates come from scripted runs.** A play session's rate is its own verb-boundary rate: one rebuild when a driving run of verbs starts, one when it ends, and one per pick-up or drop.

Pin check: consistent with E4 pin 4 (`dispatch-e4-verbs.md:14`: the carried mask rebuilds the world and resets the warm start, by design and in the hash) and with T2 pin 8 (`dispatch-t2-restore.md:22`: native tests in release, because the rebuild path trips the debug assert); bears on T2 pin 1 (`dispatch-t2-restore.md:15`: one Rapier world across quanta holds only between verb boundaries, measured 11 rebuilds in 12,242 quanta), on S1 pin 9 (removal changes handles, measured (5, 0) → (5, 1)), pin 11 (every verb-boundary rebuild is a mid-run reload that applies `canon_quat` to a canonical record again), pin 12 (the load pass must not be reused for an in-place switch) and pin 15 (an in-place slice takes the masks out of the reload test), all in `docs/dispatch-s1-soundness.md`; no Phase 2 pin requires the change, so it stays a later-slice fidelity item.
