Answers 1–4 — rapier3d-f64 0.35.3 (enhanced-determinism), rustc 1.98.1, checked 2026-09-25.

Engine state read: `main` (`solver/src/rapier_law.rs`, `solver/src/lib.rs`, `solver/FLAGS.md`) and the T2 branch `solver/src/rapier_law.rs` at `ee2e50a` (PR #43). Rapier and parry line numbers are from the pinned registry sources `rapier3d-f64-0.35.3/…` and `parry3d-f64-0.30.2/…`, which is the source docs.rs serves (`https://docs.rs/crate/rapier3d-f64/0.35.3/source/…`). Two kinds of evidence:

- **Oracle checks.** These ran under the compile oracle (`scripts/compile_oracle.py`, rustc 1.98.1, rapier3d-f64 0.35.3 + enhanced-determinism, debug profile). Their labels match the lane file `lanes/restore-internals.json`, whose oracle run reads "19 checks over 10 recipes — 19 pass, 0 fail".
- **Experiments.** These ran in scratch cargo projects under `…/scratchpad/q1-q4/` with the solver's release profile (`opt-level 3, lto false, codegen-units 1, panic abort, overflow-checks false`), `cargo +1.98.1 build --release`. The wasm builds used `RUSTFLAGS="-C target-feature=-relaxed-simd"` and ran in node 22.22.3 (V8).

The experiment scene follows `build_world`: dt 1/64, gravity −8, clustering off, warm start 1.0, sleep after 32 quanta, friction 0.8, restitution 0, and fixed colliders on fixed bodies inserted first. It contains a floor, a tilted slab, a 6×6 heightfield, six dynamic boxes (a 3-stack, one on the slab, one on the heightfield, one falling) and one kinematic box walking +x. Routes (a) and (c) in §1 are being **measured separately** by another seat. The numbers I give for them are a second, independent measurement.

## 1. T2 restore — warm-start impulses

**Answer.** No, for two reasons.

**(1) No sound write path.** rapier3d-f64 0.35.3 has no sound public path that writes any field of a `ContactPair` or `ContactManifold`:

- Every contact accessor on `NarrowPhase` and `PhysicsWorld` takes `&self` and returns shared references.
- `InteractionGraph`'s `*_mut` methods need a `&mut InteractionGraph`, which `NarrowPhase` never hands out.
- A `MODIFY_SOLVER_CONTACTS` hook receives the manifold by `&`, and `SolverContact` has no warm-start fields.

The engine's `solver_clear_warmstart` on `main` gets its pointers from `core::ptr::from_ref(pair) as *mut ContactPair` and writes through them. So do the T2 branch's `pairs_mut`, `carry_warmstart` and `solver_restore`. That is undefined behaviour. rustc's deny-by-default `invalid_reference_casting` rejects the same cast written as one expression; parking the pointers in a `Vec` only hides it from the lint.

**(2) A sound write would still not be enough.** Suppose the write were sound, for example through serde. The next step still would not warm-start as the uninterrupted run did, because the solver reads more per-contact state than the four warm-start fields:

- `solver_dp1`/`solver_dp2`, the frozen lever arms, on each point.
- The point geometry, which parry keeps across steps through `try_update_contacts`.
- The solver-contact anchors.
- The pair's crate-private `recycle_state` and `solver_color`.
- The narrow phase's private per-body colour masks, which set the Gauss–Seidel order.

I measured this. A world rebuilt as pin 1 prescribes has every body bit-equal and every warm-start field written from the saved values, yet it parts from the uninterrupted world on the first quantum. At 0.35.3 the only complete and sound restore of Rapier state is `serde-serialize`. Route (d), replay, avoids restoring Rapier state at all.

Fields the solver reads for warm start, per point, in the 3D default friction model (`FrictionModel::Simplified` → `ContactWithTwistFriction`):

- `warmstart_impulse`.
- `warmstart_tangent_world`. In 3D the solver reads this world vector, projected onto the current tangent basis. It does not read `warmstart_tangent_impulse`, which is only written back.
- `warmstart_twist_impulse`.
- `impulse`, as `is_new = impulse == 0.0`. At restitution 0 that only feeds `is_bouncy`, which returns 0 either way.
- `solver_dp1`, `solver_dp2`.
- Per manifold: `solver_contacts` (anchors, `contact_id`, `tangent_velocity`), `normal`, `friction`, `restitution`, `relative_dominance`, and the crate-private `solver_body_ids`.

The solver writes the four warm-start fields and `impulse` back to the manifold points after solving.

**What I checked.**

- **Public surface.**
  - `rapier3d-f64-0.35.3/src/geometry/narrow_phase/queries.rs:21-182`: every `pub fn` takes `&self`, and none returns `&mut`. https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/narrow_phase/queries.rs; API page https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/geometry/struct.NarrowPhase.html.
  - `PhysicsWorld`'s mirrors take `&self` (`src/pipeline/physics_world.rs:629-650`).
  - `InteractionGraph::interaction_pair_mut` and `interactions_with_mut` take `&mut self` (`src/geometry/interaction_graph.rs:148-195`). The graph sits in the private field `NarrowPhase::contact_graph` (`src/geometry/narrow_phase/mod.rs:332`).
  - A sweep of the crate for any `pub fn` that returns or yields `&mut ContactPair`, `&mut ContactManifold` or `&mut InteractionGraph` finds none. `EventHandler` gets `Option<&ContactPair>` and `&ContactPair`.
  - 0.36.0, published 2026-09-25, is the same: https://docs.rs/rapier3d-f64/0.36.0/rapier3d_f64/geometry/struct.NarrowPhase.html lists only `&self` accessors. Its changelog moves `ContactPair::manifolds`/`solver_clusters` to `ContactPair::contacts` (https://raw.githubusercontent.com/dimforge/rapier/master/CHANGELOG.md). A bump opens no route.
  - Oracle, compile_fail:
    - `NarrowPhase has no contact_pairs_mut` → E0599.
    - `contact_graph() is shared: interaction_pair_mut needs &mut` → E0596.
    - `NarrowPhase::contact_graph field is private` → E0616.
- **The hook route (confirms the claim).**
  - `ContactModificationContext` has `manifold: &'a ContactManifold` and `solver_contacts: &'a mut SolverContacts` (`src/pipeline/physics_hooks.rs:29-65`).
  - `SolverContactGeneric` has `anchor1`, `anchor2`, `dist`, `tangent_velocity`, `contact_id` and `padding`. Its own comment says "warm-starts on the manifold points" (`src/geometry/contact_pair.rs:617-653`).
  - The hook runs in the narrow phase (`src/geometry/narrow_phase/pair_update.rs:500-531`).
  - The constraint builder reads the warm start "straight off the manifold points (not duplicated on the solver contacts)":
    - `src/dynamics/solver/contact_constraint/contact_with_twist_friction.rs:192-235`.
    - `contact_with_coulomb_friction.rs:166-171`.
    - Writeback: `contact_with_twist_friction.rs:783-825`.
  - Pairs with hooks are never recycled (`pair_update.rs:116-121`), so a hook would also change the simulation.
  - Oracle, compile_fail:
    - `A hook cannot write warm start: SolverContact has no warmstart_impulse` → E0609 ("no field `warmstart_impulse` on type `&mut SolverContactGeneric<f64, 1>`").
    - `A hook cannot write the manifold: ctx.manifold is behind &` → E0596 ("cannot borrow `ctx.manifold.points` as mutable, as it is behind a `&` reference").
- **The cast is UB.**
  - std `ptr::from_ref`: the memory the pointer points to must be "never written to (except inside an UnsafeCell) using this pointer or any pointer derived from it" (https://doc.rust-lang.org/stable/std/ptr/fn.from_ref.html).
  - The Reference lists "Mutating immutable bytes… the bytes pointed to by a shared reference… are immutable" as UB (https://doc.rust-lang.org/stable/reference/behavior-considered-undefined.html).
  - The lint listing: https://doc.rust-lang.org/rustc/lints/listing/deny-by-default.html (`invalid_reference_casting`).
  - Oracle:
    - `One-expression &T to &mut T cast is rejected by invalid_reference_casting` → compile_fail with the lint ("casting `&T` to `&mut T` is undefined behavior, even if the reference is unused, consider instead using an `UnsafeCell`").
    - `The engine's shape (pointers parked in a Vec) compiles with no diagnostic` → compiles.
- **Per-contact state beyond the warm start.**
  - Frozen arms and body-local anchors are written at the last full update (`pair_update.rs:533-577`).
  - Recycling skips the update while drift ≤ 0.05 (`pair_update.rs:108-171`). It is on by default (`src/dynamics/integration_parameters.rs:279-289, 399`), and the engine does not turn it off.
  - `recycle_state`, `solver_color` and `solver_color_bodies` are `pub(crate)` (`contact_pair.rs:233-255`). docs.rs source: https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/contact_pair.rs.
  - Colours are assigned greedily at begin-touch and released at end-touch (`narrow_phase/mod.rs:87-172`; `narrow_phase/contacts.rs:300-385`). "Deterministic: results depend only on the coloring" (`src/dynamics/solver/staged_island_solver/mod.rs:1-4, 45-51`).
  - parry's cuboid–cuboid manifold returns early through `try_update_contacts`, which keeps the old points (`parry3d-f64-0.30.2/src/query/contact_manifolds/contact_manifolds_cuboid_cuboid.rs:28-30`; `contact_manifold.rs:712-748`).
  - Oracle, runs: `A world rebuilt at bit-equal poses reads different contact geometry` → "points 12 vs 11; of the pairs compared, points whose anchors, lever arms or dist differ: 11".
- **Experiment E2 (pin 1 emulated without UB).** Rebuild from the saved records, run the load pass, copy the whole `RigidBodyActivation` after the pass (better than pin 1 can do), write the seven warm-start floats per point in sorted pair order through a `serde_json::Value` patch, step both worlds (`lab2`, `pin1.exe`):
  - At 5, 12 and 20 quanta, pin 1's count check refuses the snapshot: 5 against 2 pairs, 40 against 71 points, 71 against 55 points.
  - At 1, 33, 50, 75 and 90 quanta it is accepted and diverges on quantum 0.
  - At 33 quanta, before the step, every body is bit-equal (pose, velocity, whole activation) and every warm-start field equal. All 71 of 71 points differ in `local_p1/local_p2/solver_dp1/solver_dp2/dist`. One quantum later the touching bodies differ by up to 3.43e-5 m and 2.25e-3 m/s. The free-falling body is identical.
  - With `contact_recycling = false` in both worlds: refused at 5 and 12, diverging on quantum 0.
- **Colours are result-bearing.** Swapping the colours of the two stack pairs (0↔1), with masks kept consistent and the control given the same `Value` round trip and graph rebuild, parts on quantum 0. The top box ends at 2.498742471332 against 2.498740164194 (`lab2`, `colors.exe`). In a history where the upper pair touched first, the running world has (box0, box1) at colour 1, and the load pass gives it 0 (`colorcmp.exe`).
- **Not result-bearing, measured.** Reversing the awake-island body order (with `active_set_id` rewritten) and forcing a solver-graph rebuild each gave no difference over 300 quanta (`order.exe`, `rebuild.exe`). The `serde_json::Value` round trip, which re-sorts the heightfield workspace's map keys, also gave none over 300 quanta (`labp`, `recheck.exe`).

**Sound routes and their costs.**

- **(a) `warmstart_coefficient = 0`**, in T2's rebuild-every-quantum law, so there is nothing to carry.
  - Sound.
  - The coefficient is read on every step: `contact_with_twist_friction.rs:451` (`update`, called once per substep inside the substep loop at `src/dynamics/solver/staged_island_solver/worker.rs:227`); `worker.rs:296` gates the fused update; `worker.rs:438` skips the whole warm-start stage when it is 0. A world uses a new value from its first quantum.
  - Coefficient 0 also drops the warm start between the substeps of every quantum (`update` "banks the previous substep's impulse before the warm-start scaling", `contact_with_twist_friction.rs:500-518`). So it is weaker than an empty cache.
  - Measured separately. My numbers, a 4-box stack at the engine's parameters: all asleep at quantum 33 with 1.0 and 50 with 0.0; the top box sinks 2.71e-3 m and 3.57e-2 m (oracle `Stack at engine parameters: warm start on vs off`).
- **(b) A vendored rapier3d-f64 0.35.3 with one accessor**, through `[patch.crates-io] rapier3d-f64 = { path = "…" }`, where the vendored `Cargo.toml` stays at version `0.35.3`. The minimal sound diff is 16 lines in `src/geometry/narrow_phase/queries.rs`, after `contact_pairs`:

  ```rust
  /// The contact data of every point of every solver manifold, mutably, with the pair's
  /// collider handles: pairs in the order of [`Self::contact_pairs`], then manifolds, then
  /// points. Only [`ContactData`] is reachable, so the manifold and point counts that the
  /// persistent solver graph indexes cannot change through it.
  pub fn contact_data_mut(
      &mut self,
  ) -> impl Iterator<Item = (ColliderHandle, ColliderHandle, &mut ContactData)> {
      self.contact_graph.graph.edges.iter_mut().flat_map(|edge| {
          let pair = &mut edge.weight;
          let (c1, c2) = (pair.collider1, pair.collider2);
          pair.solver_manifolds_mut()
              .iter_mut()
              .flat_map(move |m| m.points.iter_mut().map(move |pt| (c1, c2, &mut pt.data)))
      })
  }
  ```

  - Its order matches `contact_pairs()`. That method is `self.contact_graph.interactions()` = `graph.raw_edges().iter()` (`interaction_graph.rs:98-100`), the same `Vec` (`src/data/graph.rs:138`) in the same order. Measured: "pairs with points, in contact_pairs() order == contact_data_mut() order: true".
  - It leaves physics bit-identical: snapshot FNV `57339140c4e9049a` at 90 quanta and `40cda3005d1a708c` at 300, equal to the unpatched crate (native at 90; wasm at 90 and 300).
  - Zeroing through it and stepping gives the same hashed state as zeroing through serde and stepping (`labp`, `vendored.exe`).
  - The internal `InteractionsWithMut` iterator (`interaction_graph.rs:254-284`) walks one node's edges through an `unsafe` transmute. `edges.iter_mut()` needs no `unsafe`.
  - A one-line `contact_pairs_mut() -> impl Iterator<Item = &mut ContactPair>` would also compile. It lets callers resize `manifolds`, which the persistent solver graph indexes by ordinal. The manifold store turns a stale ordinal into an always-on panic (`src/dynamics/solver/manifold_store.rs:56-91`), but I did not audit every narrow-phase path, so prefer the data-only accessor.
  - Cost: a patch carried across every bump (0.36.0 already renames the field the body reads), plus Apache-2.0 §4 obligations for a modified copy. This route only makes T2's *carry* sound. By itself it does not make a restore of a running world exact (E2).
- **(c) serde (`serde-serialize`)**: serialize the `PhysicsWorld` on save, deserialize on restore, and never run the load pass afterwards.
  - Sound. Exact continuation (§4). Manifold point order is preserved: `Vec` order is serialized, the round trip is byte-identical, and the continuation is exact.
  - Measured separately. My numbers:
    - The same test module is 1,457,799 bytes without serde and 2,143,817 bytes with it (+686,018, +47%).
    - The 10-body scene's bincode blob is 29–40 KB (JSON 90–121 KB).
    - Native serialize takes about 7–17 µs and deserialize 17–20 µs.
    - Nothing is paid per quantum unless you serialize every quantum.
  - Version-locked: 0.36.0's changelog says "Snapshots serialized with previous versions can't be loaded anymore".
- **(d) Persistent law (main) plus restore by replay** from the seed and the log to the save tick, proven by the T1 trace.
  - Sound: the law writes nothing inside Rapier. The three branch casts and `carry_warmstart` disappear.
  - Full fidelity: Rapier keeps its own warm start.
  - Per quantum: 744 ms / 10,000 quanta on node (coordinator's measurement), against 962 ms for T2's rebuild.
  - Restore: t × ≈74.4 µs for a save tick t, which is 0.744 s at t = 10,000.
  - T6 arithmetic: a sweep of R restores to settled cells at ticks t_i costs 74.4 µs × Σt_i. With R = 100 at a mean tick of 5,000 that is ≈37 s; with R = 1,000 it is ≈6.2 min.
  - Native cross-check (Rapier step only):
    - 119.9 µs/quantum for 64 awake boxes over their first 256 quanta.
    - 9.9 µs/quantum averaged over 10,000 quanta (60 of 64 asleep by the end).
    - 1.0 µs/quantum for the 10-body scene.
  - Checkpointing by replay-to-tick needs a checkpoint the law never writes. **(e)**, which I found in addition, is one:
    - Copy the module's whole linear memory in JS at the tick, and write it into a fresh instance to restore.
    - Measured on a 64-body law-shaped module: 3,538,944-byte image, 1.32 ms out and 0.93 ms in. At tick 260 the continued instance, the restored image and an uninterrupted run all hash `7a4c4d3296f61093` (`memimg/run.js`).
    - With (e), a sweep costs one replay (≤0.744 s) plus about 2 ms per restore, and image memory is paid per checkpoint kept.
    - The image is tied to the exact binary and happens entirely outside Rust (no Rust code runs during the copy). I found no Rust document on host writes to linear memory, so treat that as outside Rust's model: wasm-defined, and exact in the test.
  - What (d) gives up: T2's claim that the snapshot is the whole state. The hash fingerprints a history-determined state.
- **`solver_clear_warmstart` has no sound form under (d)** either, without (b) or serde.
  - **Replacement, part (i): pure-bytes sensitivity.** On a resting stack, check that the warm-start fields in the snapshot bytes are non-zero, flip them in a copy of the bytes, and require the hash to change.
  - **Replacement, part (ii): structural.** `rebuild_snapshot` must emit all seven floats of every point of every `solver_manifolds()` entry, in sorted pair order.
  - (i) and (ii) prove what the old test proved about the hash: the live warm-start cache is emitted and the hash covers it.
  - Neither proves that the cache steers the next quantum.
  - The candidate "same history, coefficient 1.0 against 0.0" does not prove it either:
    - Oracle `warmstart_coefficient is read from the first quantum` → "first quantum a contact carries an impulse: Some(1); first quantum 1.0 and 0.0 differ: Some(1)". The runs part on quantum 1, when the cache is still empty. So they show the coefficient steering the substep loop, not the cached values steering the next quantum.
    - A sound zero-then-step and coefficient 0 for one quantum both differ from control, and they also differ from each other ("zeroed == coefficient 0: false" at 20 and 40 quanta, `labp`, `recheck.exe`).
  - The steering claim needs a sound write in a test-only build: serde, or the (b) accessor in a native test crate, never the product binary.

**Recommendation.**

| Route | Soundness | Fidelity to Rapier's warm start | Per-quantum cost | Restore cost |
|---|---|---|---|---|
| (a) coefficient 0, rebuild each quantum | sound | none: no warm start across quanta or across substeps; the stack sinks 13× deeper and sleeps 17 quanta later | ≈ T2's rebuild (962 ms/10k on node), minus the carry | one rebuild from bytes |
| (b) vendored `contact_data_mut`, rebuild each quantum | sound (data-only accessor, tested) | approximate: carried by pair, subshape and fid, but recycling, parry's point persistence, frozen arms, colours, islands and Rapier's sleep timer reset each quantum | ≈ 962 ms/10k (node) | one rebuild from bytes; the patch carried across bumps |
| (c) serde blob, persistent law | sound | full (exact continuation, tested) | 0 per quantum; +686 KB wasm (+47% in my module) | deserialize (µs natively); blob locked to 0.35.3 |
| (d) persistent law, replay | sound (writes nothing) | full | 744 ms/10k (node, fastest) | t × 74.4 µs (≤0.74 s); ~2 ms with (e) images |

Take **(d)**. Drop every cast (main's `solver_clear_warmstart`, and the branch's `pairs_mut`, `carry_warmstart` and `solver_restore`), and replace the clear test with (i) + (ii). Add (e) images if T6's replay time matters, and keep (c) as the upgrade if restore from bytes becomes a requirement. Neither (a) nor (b) is recommended: (a) costs stacking quality, and (b) keeps a Rapier fork and still diverges from Rapier's own continuous run.

**Consequence for T2.**

1. Pin 1's write-back cannot be implemented soundly. A sound variant (serde) still reruns differently (E2), so pin 5's test would fail on every scene with contacts.
2. If the rebuild-each-quantum design (branch) is kept, its carry must go through (b) or be dropped with (a). Its restore is then exact by construction, but the golden is T2's, not Rapier's continuous run.
3. With (d), T2 becomes: save = tick index plus the T5 log; restore = replay; proof = T1 trace `identical`. Pins 4 and 7 become tests on replay and on the bytes checks above.

**Contradicts a pin?** Yes, pin 1: the write-back of warm-start impulses in sorted pair order, and the refusal on pair/point counts, which also rejects valid snapshots (see §3). Pins 4 and 7 are not contradicted. Under (d) they are carried by replay (the T1 trace) and by the bytes checks above instead of by `solver_restore`.

Pin check: contradicts pin 1 of dispatch-t2-restore.md because no sound public path writes a manifold point at 0.35.3 (NarrowPhase hands out only shared references; the engine's from_ref cast is UB), and a sound write still does not reproduce the next step, since solver_dp1/solver_dp2, the point geometry, recycle_state and solver_color are also read, rapier3d-f64-0.35.3/src/geometry/narrow_phase/queries.rs:21-182.

## 2. T2 restore — sleep state

**Answer.** `RigidBodyActivation` at 0.35.3 has six fields:

- `normalized_linear_threshold`, `angular_threshold`, `time_until_sleep`, `time_since_can_sleep` and `sleeping`, all `pub`.
- `sleep_prev_pose: Pose`, which is `pub(crate)`.

`sleep_prev_pose` is the body's pose at the previous energy update. The update runs before the solve and gets the pose at the start of the step, so at save time the field holds the pose from one quantum before the save, and the snapshot has no copy of it. It came with 0.35.0: "Sleep eligibility is now judged on the actual per-step pose displacement". `update_energy` compares it with the current pose, and a drift above the threshold resets the timer.

It has no public setter. `active()`, `inactive()` and `cannot_sleep()` set it to identity. Only a whole-struct copy carries it, in-process (the type is `Copy`), or serde. Rebuilding the activation from the five public fields therefore resets `time_since_can_sleep` to 0 on the next step for any body not at the origin: measured `[20, 6, 6]` against `[0, 0, 0]` quanta.

The public ways to set the fields, and their side effects:

- **`RigidBody::activation_mut()`** writes all five public fields. It sets the body's `SLEEP` change flag and, when reached through `RigidBodySet` indexing, puts the body in the modified set. It makes no immediate call into the island manager. At the next step, `handle_user_changes_to_rigid_bodies` calls `IslandManager::rigid_body_updated`. That always bumps `active_set_epoch`, admits a body not yet seen, and wakes the body's island when `SLEEP` is set and `sleeping` is false. It then restores the body's own activation value, but not the values of other island members it woke.
- **`set_linvel`, `set_angvel`, `set_translation`, `set_rotation`, `set_position`** with `wake_up = true` call `wake_up(true)`, which zeroes the timer. With `false` they leave it alone.
- **`RigidBody::wake_up(true)`** zeroes the timer; `wake_up(false)` does not.
- **`RigidBody::sleep()`** sets `sleeping`, sets the timer to `time_until_sleep`, and zeroes both velocities.
- **`IslandManager::wake_up`** and **`PhysicsWorld::wake_up`** wake the whole persistent island and strong-reset every member.

`IslandManager` holds state that survives a step and is not derivable from the bodies:

- `active_set_epoch`.
- The island containers: the awake island's body order (`active_set_id`), the sleeping chunks and the free lists.
- `PersistentIslands`:
  - island membership, with eager merges and deferred splits;
  - `constraint_remove_count`, which blocks sleep for a multi-body island;
  - `split_denied_until`, a 16-step cooldown;
  - `split_island`, `removal_journal`, `sleep_scan_stamp`;
  - `contact_link_locs`, keyed by contact-graph edge id;
  - `bootstrapped`.

A rebuilt world bootstraps fresh islands from the current touching pairs. Measured:

- The awake-body order is not result-bearing.
- Island membership gates only when an island sleeps. I did not reproduce a divergence from it in a small scene, because the local split settles most removals at once. So its effect is **not determined** empirically; a scene that forces a global split would settle it. Serde carries it either way.

**What I checked.**

- **Fields.**
  - `rapier3d-f64-0.35.3/src/dynamics/rigid_body_components.rs:1295-1326`.
  - `update_energy`: `:1417-1470`, with `prev_pose = replace(&mut self.sleep_prev_pose, *pose)` and `drift * 0.5 < linear_threshold * dt`.
  - https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/rigid_body_components.rs. The API page https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/dynamics/struct.RigidBodyActivation.html shows five fields; `sleep_prev_pose` is not public.
  - Changelog at the tag: https://raw.githubusercontent.com/dimforge/rapier/v0.35.3/CHANGELOG.md (v0.35.0 entry).
  - The energy update runs in the pre-solve traversal with `rb.pos.position` (`src/pipeline/physics_pipeline/solve.rs:234-250`; `src/dynamics/island_manager/manager.rs:320-333`).
- **Setters.**
  - `src/dynamics/rigid_body.rs:184-187` (`activation_mut`), `:804-807` (`sleep`), `:816-822` (`wake_up`), `:905-917` (`set_linvel`), `:988-1004` (`set_translation`); https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/rigid_body.rs.
  - `src/pipeline/user_changes.rs:76-89, 188` (activation saved, then restored).
  - `manager.rs:257-316` (`rigid_body_updated`).
  - `src/dynamics/island_manager/sleep.rs:31-76` (whole-island wake).
- **Load-pass side effects.** Begin-touch transitions in `CollisionPipeline::step` call `strong_wake_sleeping_side` and `interaction_changed(…, true)`, which runs `activation.wake_up` (`src/geometry/narrow_phase/contacts.rs:312-351`; `manager.rs:118-145`). `warm_broadphase` then calls `wake_up(true)` on every non-fixed body (`rapier_law.rs` `warm_broadphase` on main).
- **Island state.**
  - `manager.rs:28-51`.
  - `src/dynamics/island_manager/persistent.rs:31, 71-90, 127-168`.
  - `finish_sleep_scan`: `:498-516`.
  - `bootstrap`: `:600-666`.
  - https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/island_manager/persistent.rs. That page's summary tool claimed several of these fields were `serde(skip)`; the source says otherwise. So did the serialized JSON, which contains `bootstrapped`, `removal_journal`, `sleep_scan_stamp` and `split_island`.
- **Oracle, runs.**
  - `Rebuilding RigidBodyActivation from its pub fields resets the sleep timer` → "saved at step 20: quanta [19.0, 5.0, 5.0] / next step, whole activation kept: [20.0, 6.0, 6.0] / next step, pub fields rebuilt: [0.0, 0.0, 0.0]".
  - `Which public setters zero time_since_can_sleep` → "set_linvel(_, false) 0.25 | set_linvel(_, true) 0 | set_translation(_, false) 0.25 | set_translation(_, true) 0 | wake_up(false) 0.25 | wake_up(true) 0" and "sleep(): sleeping true timer 0.5 linvel [0.0, 0.0, 0.0]".
- **Experiments.** Awake order reversed with `active_set_id` rewritten, against a control with the same epoch bump: no difference over 300 quanta at 12, 20 and 33 (`order.exe`).
- **Debug builds.** The engine's load pass trips Rapier's `debug_assert!` at `manager.rs:137-144` ("assertion failed: rb.is_fixed() || !rb.is_enabled() || rb.ids.active_island_id != u32::MAX", exit 101) when any body touches geometry at load. `CollisionPipeline` never registers bodies with the island manager (`src/pipeline/collision_pipeline.rs:177-185`) but reports transitions to it. Oracle `The load pass panics in a debug build of Rapier when a body touches at load` → exit 101 after "before the pass". The release wasm compiles the check out.

**Consequence for T2.**

1. Under (c) or (d), sleep comes back with everything else. Do not run the load pass or any `wake_up` after deserializing: that measured a divergence at quantum 0 (`serde_pass.exe`).
2. Under any public-API rebuild, write the sleep state after the load pass, never before it, and never through a `wake_up = true` setter. Even then the first step resets the timers (`sleep_prev_pose`), so pin 5 fails for resting bodies. The branch knew this and replaced Rapier's sleep with the law's own; that is part of why its golden differs from main's.
3. Native debug-profile tests of any load or restore path will panic whenever bodies touch at load.

**Contradicts a pin?** Yes, pin 1, twice:

- Sleep state set before "the same collision pass load runs" is erased by the pass: the wake on begin-touch plus `warm_broadphase`'s `wake_up(true)`.
- The public fields cannot restore the timer's continuation.

Pin check: contradicts pin 1 of dispatch-t2-restore.md because the sleep state it writes before the load pass is erased by that pass, and the timer's continuation depends on the pub(crate) sleep_prev_pose (pose one quantum before the save) that no public call sets, rapier3d-f64-0.35.3/src/dynamics/rigid_body_components.rs:1295-1326.

## 3. T2 restore — broad phase

**Answer.** Yes. `BroadPhaseBvh` keeps state across steps that changes *which* pairs exist, not only their order. The state:

- The BVH itself: topology, optimizer state and `free_wide_nodes`.
- Each leaf's stored AABB.
- The pair map (an `IndexMap` under enhanced-determinism) and `pair_adjacency`.
- `pending_set_aabb`, filled at the end of every step by the pipeline's `set_aabb`.
- `prev_updated_leaves` ("needs to be serialized for determinism after snapshot restore").
- `changes_since_optimize`, `reinsert_leaf_updates` and `frame_index`.

The leaf AABB decides it. parry stores a new leaf **tight**. It adds the change-detection margin (0.04 × length_unit) only when a moving collider first leaves its leaf, and from then on only when it leaves the fat box. So a world that has run holds fat leaves around each moving collider's pose at its last refresh, while a world rebuilt from bodies holds tight leaves. Its first `CollisionPipeline` pass reports fewer pairs. Measured: bit-equal poses after 3 quanta give 1 pair running and 0 rebuilt. In the product-like scene, pin 1's count check refuses the rebuilt world at 5, 12 and 20 quanta.

New pairs are added in BVH traversal order, which becomes the contact-graph edge order. Only pairs next to changed leaves are ever tested for staleness.

There is a public full rebuild: `BroadPhaseBvh::new()` plus `set_aabb` for every collider. It is unsound as a law, though. A fresh broad phase has no record of the pairs the narrow phase holds, so it never emits `DeletePair`, and `NarrowPhase` removes contact pairs only on `DeletePair`, collider removal or a sensor change. Measured: a box 4.01 m from a pillar is still paired to it when the broad phase is rebuilt every step.

What `enhanced-determinism` guarantees:

- parry's `HashMap`/`HashSet` become `IndexMap`/`IndexSet` with `BuildHasherDefault<FxHasher32>`, a hash that does not depend on pointer size.
- simba and glamx use libm.
- Stored contact impulses get canonical signed zeros.
- Joint wake and join sets drain in insertion order, and `swap_remove` is explicit.
- `simd8` cannot be combined with it.

That makes every iteration order a deterministic function of the sequence of operations on every IEEE 754 platform, given the same initial conditions and insertion order. It does not make an order a function of the current state. Contact-graph edge order, solver colours (which set the Gauss–Seidel order), composite manifold ordinals, island ids and the pair map's order all depend on history.

**What I checked.**

- **Broad phase.**
  - `rapier3d-f64-0.35.3/src/geometry/broad_phase_bvh/mod.rs:21-103` (fields, `prev_updated_leaves` comment at `:58-62`), `:171-201` (margin `CHANGE_DETECTION_FACTOR = 4.0e-2`), `:235-263` (`set_aabb` pushes to `pending_set_aabb`).
  - `update.rs:64-72` (pending drain), `:398-427` (new pairs in traversal order and `AddPair`), `:441-601` (stale scan only over the adjacency of updated or removed colliders, then canonical sort and `DeletePair`).
  - https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/broad_phase_bvh/update.rs and https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/broad_phase_bvh/mod.rs; API page https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/geometry/struct.BroadPhaseBvh.html.
  - The end of each step feeds moved AABBs through `set_aabb` (`src/pipeline/physics_pipeline/substep.rs:229-240, 555-565`).
- **parry leaves.**
  - `parry3d-f64-0.30.2/src/partitioning/bvh/bvh_insert.rs:152-216`: an existing leaf is replaced by the AABB grown by the margin only if it no longer contains the new one; otherwise `Unchanged`.
  - `:358-380`: `insert_new_unchecked` stores `BvhNode::leaf(aabb, …)` with the raw AABB.
  - https://docs.rs/crate/parry3d-f64/0.30.2/source/src/partitioning/bvh/bvh_insert.rs. The API doc at https://docs.rs/parry3d-f64/0.30.2/parry3d_f64/partitioning/struct.Bvh.html words this ambiguously; the code and the measurement agree.
- **Narrow-phase pair removal.** `src/geometry/narrow_phase/pair_management.rs:571-663` (`add_pair` adds only if `find_edge` is none) and `:665-690` (`register_pairs`); https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/narrow_phase/pair_management.rs.
- **enhanced-determinism.**
  - `parry3d-f64-0.30.2/src/utils/hashmap.rs:1-63` (https://docs.rs/crate/parry3d-f64/0.30.2/source/src/utils/hashmap.rs) and `fx_hasher.rs:1-10`.
  - `rapier3d-f64-0.35.3/src/utils/mod.rs:80-102` (`canonicalize_zero`), `:165-183` (`hashmap_remove` → `swap_remove`).
  - `src/pipeline/physics_pipeline/substep.rs:286-300, 343-356` (ordered drains).
  - `src/lib.rs:19-22`.
  - Features page https://docs.rs/crate/rapier3d-f64/0.35.3/features. Determinism guide https://rapier.rs/docs/user_guides/templates/determinism/ (conditions include the same initial conditions and the same insertion order).
  - Colour order: `staged_island_solver/mod.rs:1-4, 45-51`.
- **Oracle, runs.**
  - `A rebuilt broad phase reports a different pair set (tight vs fat leaves)` → "poses equal: true; fell 0.0095 m; pairs at load 0; after 3 quanta: running 1, rebuilt 0".
  - `Pin 6's per-step rebuild never deletes a narrow-phase pair` → "gap to pillar 4.01 m / 4.01 m; box-pillar pair present: kept false, rebuilt every step true".
  - `Under enhanced-determinism parry's HashMap is an IndexMap` → "[30, 10, 20, 5] -> [5, 10, 20]".
- **Experiments.**
  - E2 as in §1: refused at 5 quanta (uninterrupted pairs (2,7), (3,4), (4,5) are fat-leaf pairs absent from the rebuild; `pairs5.exe`).
  - With pin 6's per-step rebuild in both worlds (E4): refused at 12 quanta (26 against 71 points) and diverging on quantum 0 at 33 and 50 (`pin6.exe`).
  - Serde restore of everything except the broad phase, which is rebuilt once through `set_aabb`: exact for 300 quanta in the settling scene, but under churn it keeps a dead pair, 2 against 1 pairs for 64 quanta (`bponly.exe`, `bpchurn.exe`).

**Consequence for T2.**

1. Do not rebuild the broad phase, either at restore or every step. Restore it with everything else (serde), or avoid restoring it (replay).
2. Pin 1's refusal on pair and point counts will refuse valid snapshots whenever a body has moved since load.
3. The snapshot's sorted pair list is fine for hashing, but the solver's order is the colour order, which the list does not record.

**Contradicts a pin?** Yes:

- Pin 6's fallback (rebuild the broad phase from the colliders every step) leaks narrow-phase pairs and does not remove the history dependence.
- Pin 1's count check (§1).

Pin check: contradicts pin 6 of dispatch-t2-restore.md because a broad phase rebuilt from the colliders never emits DeletePair for pairs the narrow phase already holds (measured: a pair kept at 4.01 m) and starts from tight leaves where the running world has fat ones, rapier3d-f64-0.35.3/src/geometry/broad_phase_bvh/update.rs:441-601.

## 4. T2 restore — serde

**Answer.** With `serde-serialize` at 0.35.3, serialization of `PhysicsWorld` is byte-stable across runs and across the two targets tested. So is serialization of `RigidBodySet`, `ColliderSet`, `NarrowPhase`, `IslandManager` and `BroadPhaseBvh` separately. Measured:

- Two separate processes gave identical bytes for every part, in `serde_json` with `float_roundtrip` and in `bincode` 1.
- x86_64-pc-windows-msvc native and wasm32-unknown-unknown under node 22 (V8) gave identical bytes at 0, 20, 50 and 90 quanta.
- Deserialize then serialize gives identical bytes.
- A world deserialized mid-run continued bit-identically for 200–250 quanta at every save point tested (0 to 90 quanta), through landing, sleep transitions and CCD on a 40 m/s body.

The bytes include no allocator- or address-dependent data:

- Every hash map under enhanced-determinism is an `IndexMap`/`IndexSet` with `FxHasher32`, which has no random state.
- `BroadPhaseBvh::pairs` and `PersistentIslands::joint_link_locs` are serialized sorted by key, so they are canonical.
- `ImpulseJointSet`/`MultibodyJointSet` `to_wake_up`/`to_join` and parry's heightfield and composite workspaces (`sub_detectors`) are serialized in insertion order: deterministic, but history-dependent.
- parry's capacity-only serializers exist but are unused.
- `Vec` capacities, pointers and `Arc` identities are not serialized.

The bytes are **not canonical** in the strong sense. They encode the whole internal history (arena free lists, island ids, edge order, colours, `IndexMap` insertion order), so two worlds with the same physical state and different histories serialize differently. Stable, not canonical.

Limits:

- Version-locked: 0.36.0 cannot load 0.35.x snapshots.
- `serde_json` cannot encode composite-vs-composite workspaces, whose `(u32, u32)` map keys fail with "key must be a string"; bincode can. The engine's current shapes use `u32` keys.
- `serde_json::Value` without `preserve_order` re-sorts `IndexMap` keys. That was not result-bearing in a test, but it changes bytes.
- `NarrowPhase` holds `u128` colour masks that `Value` cannot hold without `arbitrary_precision`.
- `physics_pipeline` and `ccd_solver` are `serde(skip)`, and are workspace (measured).
- Not tested on ARM64 or Linux here; that is T3's lane.

**What I checked.**

- **Serialized types and skips.**
  - `src/pipeline/physics_world.rs:60-88` (https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/pipeline/physics_world.rs).
  - `src/pipeline/physics_pipeline/mod.rs:44-86` ("only workspace data").
  - `broad_phase_bvh/mod.rs:21-103, 156-168`.
  - `narrow_phase/mod.rs:324-405`.
  - `contact_pair.rs:208-256` (`solver_clusters_prev` skipped; used only with clustering, which the engine turns off).
  - `persistent.rs:127-168`, `manager.rs:28-51`.
  - `src/data/arena.rs:1-40` (arena serialized with its free list).
  - `src/utils/mod.rs:347-381` (sorted serializer).
  - `parry3d-f64-0.30.2/src/query/contact_manifolds/contact_manifolds_heightfield_shape.rs:16-32`.
  - Shapes are written by value through their typed form, so shared `Arc`s come back as separate copies; custom shapes cannot be deserialized (`parry3d-f64-0.30.2/src/shape/shared_shape.rs:695-713`).
  - Feature gate: oracle `The oracle links rapier3d-f64 as the engine does: PhysicsWorld is not Serialize` → compile_fail E0277.
- **Docs.**
  - https://rapier.rs/docs/user_guides/rust/serialization/: serialize the physics world as a whole; `PhysicsPipeline` and `CollisionPipeline` "don't hold any useful state"; with enhanced-determinism, "the exact same byte vectors" after the same number of timesteps. The page now documents 0.36.
  - https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/pipeline/struct.PhysicsWorld.html (Serialize/Deserialize; `ccd_solver`: "Workspace only: not part of a snapshot").
  - 0.36.0 changelog: https://raw.githubusercontent.com/dimforge/rapier/master/CHANGELOG.md.
- **Workspace control.** Oracle `Cloning every set into a twin with a fresh pipeline and CCD solver continues bit-identically` → "twin first difference: None; dynamic bodies asleep at the end: 3".
- **Experiments** (`lab`, `labwasm`, `lab3`, `sz0`, `sz1`, `memimg`):
  - `q4.exe 90 200`, run twice: PhysicsWorld 120,690 bytes, FNV `f9e6a2eb42c880bb`, identical across runs. Round trip identical. "restored world vs uninterrupted over 200 more quanta: first difference None".
  - Save points 0, 1, 3, 7, 12, 20, 33, 50 and 75: none differ. With CCD on and a 40 m/s body (`CCD=1 FAST=1`): none differ at 0, 1, 2, 3, 5, 12 and 40 quanta; CCD was active for 4 quanta and no tunnelling occurred.
  - Native against wasm, per part, at 0/20/50/90 quanta: identical FNVs (for example n=90: world `f9e6a2eb42c880bb`, bodies `5ce6d122d7d53a13`, colliders `ac9e82da1913a8de`, narrow phase `4845b5c4bb7d98bb`, islands `04bbe79020d6962c`, broad phase `b19c12ec22216f1c`, engine-layout snapshot `57339140c4e9049a`). The wasm module imports nothing. The wasm restore also continues exactly.
  - bincode: identical bytes across two processes and between native and wasm (FNV>>1 `32cf8c62f5759a7a`, `8bc1c9b3b52cdc`, `27018d05887bab46` at 12/50/90).
  - Enabling the feature does not change results: the no-serde and serde wasm builds give identical snapshot hashes at 0/20/50/90/300 quanta.

**Consequence for T2.**

1. If restore from bytes is wanted (route (c)), serialize the whole `PhysicsWorld` in bincode on save. Keep the compact snapshot as the hashed record: after deserializing, `rebuild_snapshot` reproduces it, which makes a strong refusal check.
2. Do not re-run the load pass after deserializing.
3. Treat the blob as bound to rapier3d-f64 0.35.3 and to the law's insertion order. A Rapier bump invalidates stored T5 bundles.
4. Adding the feature moves the binary digest once but not the goldens.

**Contradicts a pin?** No, for pins 4 and 9: a serde restore meets pin 4's byte-exact round trip, and the feature changes the digest once without moving either golden. It does replace pin 1's input format; that is recorded in §1.

Pin check: consistent with the pin(s) — 4, 9.
