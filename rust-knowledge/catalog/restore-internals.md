# Rapier state for restore (T2)
_Warm-start impulses, activation and islands, broad-phase order, serde canonicality — what solver_restore must carry._ · tier **si-rpg-engine** · wave 5 · 2026-09-25 · [‹ catalog index](README.md)

10 recipes · 10 verified · 10 compiler-checked.

| Recipe | Rust | Currency | ✓ | Code | What |
|--------|------|----------|---|------|------|
| Copy RigidBodyActivation whole or not at all: its pub(crate) sleep_prev_pose restarts the sleep timer | rapier3d-f64 0.35.0+ (per-step displacement sleep test) | ✅ solid | ✓ | ✔ | RigidBodyActivation has five pub fields plus pub(crate) sleep_prev_pose (the pose at the p |
| Count more than warm-start impulses as solver state: frozen arms, parry points, recycle state, colours | rapier3d-f64 0.35.3 / parry3d-f64 0.30.2 | ✅ solid | ✓ | ✔ | Besides warmstart_impulse, warmstart_tangent_world and warmstart_twist_impulse, the 0.35.3 |
| Do not rebuild Rapier's broad phase every step: a fresh BroadPhaseBvh never deletes a narrow-phase pair | rapier3d-f64 0.35.3 | ✅ solid | ✓ | ✔ | A fresh BroadPhaseBvh has no record of the pairs the narrow phase holds, so it never emits |
| Expect a rebuilt BroadPhaseBvh to report fewer pairs: new parry leaves are tight, moved leaves are fat | rapier3d-f64 0.35.3 / parry3d-f64 0.30.2 | ✅ solid | ✓ | ✔ | parry stores a new leaf with its raw AABB and adds the 0.04 x length_unit margin only when |
| Never write through a ptr::from_ref pointer to a ContactPair: parking it in a Vec only hides the UB | any (ptr::from_ref since 1.76) | ✅ solid | ✓ | ✔ | A pointer made by ptr::from_ref from &ContactPair may never be written through; doing so m |
| Read enhanced-determinism as history-deterministic iteration order, not state-canonical order | rapier3d-f64 0.35.3 with enhanced-determinism | ✅ solid | ✓ | ✔ | enhanced-determinism makes parry's HashMap/HashSet an IndexMap/IndexSet with a pointer-siz |
| Read warmstart_coefficient as a per-substep switch, not as clearing the cached warm start | rapier3d-f64 0.35.3 | ✅ solid | ✓ | ✔ | warmstart_coefficient is read every step inside each substep's constraint update; 0.0 also |
| Restore Rapier through serde-serialize or by replay: world bytes are stable and continue bit-exactly | rapier3d-f64 0.35.3 (blobs do not load in 0.36.0) | ✅ solid | ✓ | ✔ | With serde-serialize, PhysicsWorld (physics_pipeline and ccd_solver skipped as workspace)  |
| Treat rapier3d-f64 0.35.3 contact pairs as read-only: no public or hook path writes a manifold point | rapier3d-f64 0.35.3 | ✅ solid | ✓ | ✔ | NarrowPhase hands out only &ContactPair; InteractionGraph's *_mut needs &mut InteractionGr |
| Write restored sleep state after the load pass, never through wake_up=true setters | rapier3d-f64 0.35.3 | ✅ solid | ✓ | ✔ | set_linvel/set_angvel/set_translation/set_rotation/set_position(_, true) and wake_up(true) |

## Detail

### Copy RigidBodyActivation whole or not at all: its pub(crate) sleep_prev_pose restarts the sleep timer
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust rapier3d-f64 0.35.0+ (per-step displacement sleep test)

**RigidBodyActivation has five pub fields plus pub(crate) sleep_prev_pose (the pose at the previous energy update); rebuilding it from the pub fields resets time_since_can_sleep to 0 on the next step for any body not at the origin.**

- **How:** Within a process, copy the whole struct (it is Copy): *rb.activation_mut() = saved. Across bytes, only serde-serialize carries sleep_prev_pose; the snapshot's time_since_can_sleep and sleeping are not enough to continue the timer.
- **Gotchas:** At save time sleep_prev_pose holds the pose one quantum before the save (the energy update runs before the solve), so storing the current pose does not help. Measured: whole copy [20, 6, 6] quanta, pub fields rebuilt [0, 0, 0].
- **In si-rpg-engine:** rapier_law.rs rebuild_snapshot writes time_since_can_sleep/DT and sleeping only; si-rpg-engine T2 (docs/dispatch-t2-restore.md) pin 1 ('sleep state from the bytes'); the T2 branch replaced Rapier's sleep with the law's own for this reason.
- **Code checks** ([source](restore-internals.code.md#copy-rigidbodyactivation-whole-or-not-at-all-its-pubcrate-sleep_prev_pose-restarts-the-sleep-timer)):
  - *Check 1: Rebuilding RigidBodyActivation from its pub fields resets the sleep timer* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**

- **Verifier (solid):** Reproduced exactly: "whole activation kept: [20,6,6]", "pub fields rebuilt: [0,0,0]". sleep_prev_pose pub(crate) at rigid_body_components.rs:1325 exact; update_energy zeroes time_since_can_sleep on drift, confirmed by reading its body. · [operator 2026-09-25: CITATION ANCHOR: pin numbers cite si-rpg-engine docs/dispatch-t2-restore.md at ee2e50a, the head of PR #43 (closed unmerged). main rewrote that dispatch on route (d) at 9c47d40 and renumbered its pins; PR #53 builds the rewrite.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [RigidBodyActivation (rapier3d-f64 0.35.3 API docs)](https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/dynamics/struct.RigidBodyActivation.html) (2026) — Five public fields (thresholds, time_until_sleep, time_since_can_sleep, sleeping); wake_up(strong) and sleep() are the public state changes.
  - ✓ [rapier3d-f64 0.35.3 source: dynamics/rigid_body_components.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/rigid_body_components.rs) (2026) — RigidBodyActivation has a pub(crate) sleep_prev_pose; update_energy replaces it and resets time_since_can_sleep when the drift from it is too large.
  - ✓ [rapier CHANGELOG at tag v0.35.3](https://raw.githubusercontent.com/dimforge/rapier/v0.35.3/CHANGELOG.md) (2026) — v0.35.0: sleep eligibility is judged on the actual per-step pose displacement; contact impulses are stored with canonicalized signed zeros.

### Count more than warm-start impulses as solver state: frozen arms, parry points, recycle state, colours
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust rapier3d-f64 0.35.3 / parry3d-f64 0.30.2

**Besides warmstart_impulse, warmstart_tangent_world and warmstart_twist_impulse, the 0.35.3 solver reads solver_dp1/solver_dp2 (lever arms frozen at the last full update) and history-kept contact points; the pair's pub(crate) recycle_state and solver_color decide recycling and solve order.**

- **How:** A world rebuilt from bit-equal poses and velocities computes fresh contact points; the running world keeps recycled or try_update'd ones. So writing the four warm-start fields back cannot make the next step match: restore all of the narrow phase (serde) or do not restore it (replay).
- **Gotchas:** 3D reads warmstart_tangent_world, not warmstart_tangent_impulse (written back only). contact_recycling defaults to true and turning it off does not help: parry's cuboid-cuboid path still keeps old points through try_update_contacts. Measured with warm starts written soundly: first-quantum divergence up to 3.4e-5 m.
- **In si-rpg-engine:** rapier_law.rs rebuild_snapshot/push_contact hash 7 floats per point but not solver_dp1/solver_dp2, recycle_state or colours; si-rpg-engine T2 (docs/dispatch-t2-restore.md) pin 1 and pin 5.
- **Code checks** ([source](restore-internals.code.md#count-more-than-warm-start-impulses-as-solver-state-frozen-arms-parry-points-recycle-state-colours)):
  - *Check 1: A world rebuilt at bit-equal poses reads different contact geometry* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**

- **Verifier (solid):** Check reproduced exactly ("points 12 vs 11 ... differ: 11"). solver_dp1/dp2 read + "frozen at last full update" comment confirmed. recycle_state/solver_color pub(crate) at contact_pair.rs:237/243/255. try_update_contacts confirmed. · [operator 2026-09-25: CITATION ANCHOR: pin numbers cite si-rpg-engine docs/dispatch-t2-restore.md at ee2e50a, the head of PR #43 (closed unmerged). main rewrote that dispatch on route (d) at 9c47d40 and renumbered its pins; PR #53 builds the rewrite.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [rapier3d-f64 0.35.3 source: contact_with_twist_friction.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/solver/contact_constraint/contact_with_twist_friction.rs) (2026) — generate() reads warmstart_impulse, warmstart_tangent_world, warmstart_twist_impulse, impulse and solver_dp1/solver_dp2 from the manifold points; writeback_impulses() writes them back.
  - ✓ [ContactData (rapier3d-f64 0.35.3 API docs)](https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/geometry/struct.ContactData.html) (2026) — solver_dp1/solver_dp2 are lever arms frozen at the pair's last full narrow-phase update; warmstart_tangent_world is the world-space friction warm start 3D reads.
  - ✓ [rapier3d-f64 0.35.3 source: geometry/narrow_phase/pair_update.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/narrow_phase/pair_update.rs) (2026) — A pair within the recycle drift keeps its points and frozen arms; recycle_state is stored only when recycling is on; pairs with active hooks are never recycled.
  - ✓ [rapier3d-f64 0.35.3 source: geometry/contact_pair.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/contact_pair.rs) (2026) — ContactPair's recycle_state, solver_color and solver_color_bodies are pub(crate); solver_dp1 is frozen at the last full update.
  - ✓ [parry3d-f64 0.30.2 source: contact_manifolds_cuboid_cuboid.rs](https://docs.rs/crate/parry3d-f64/0.30.2/source/src/query/contact_manifolds/contact_manifolds_cuboid_cuboid.rs) (2026) — The cuboid-cuboid manifold returns early through try_update_contacts, keeping the previous contact points, and transfers impulses with match_contacts.

### Do not rebuild Rapier's broad phase every step: a fresh BroadPhaseBvh never deletes a narrow-phase pair
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust rapier3d-f64 0.35.3

**A fresh BroadPhaseBvh has no record of the pairs the narrow phase holds, so it never emits DeletePair; NarrowPhase removes contact pairs only on DeletePair, collider removal or a sensor change, so separated pairs stay forever.**

- **How:** Keep the one BroadPhaseBvh the world was built with. If broad-phase history must be reproduced, serialize it (it is Serialize) rather than rebuilding it with new() + set_aabb.
- **Gotchas:** A rebuilt broad phase still answers queries correctly and physics may look fine; the leak shows in the contact-pair list and the snapshot bytes. It also does not remove the history dependence: a restore with the per-step rebuild in both worlds still diverged on quantum 0.
- **In si-rpg-engine:** si-rpg-engine T2 (docs/dispatch-t2-restore.md) pin 6's fallback ('the law rebuilds the broad phase from the colliders at every step'); rapier_law.rs rebuild_snapshot would carry the leaked pairs.
- **Code checks** ([source](restore-internals.code.md#do-not-rebuild-rapiers-broad-phase-every-step-a-fresh-broadphasebvh-never-deletes-a-narrow-phase-pair)):
  - *Check 1: Pin 6's per-step rebuild never deletes a narrow-phase pair* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**

- **Verifier (solid):** Check reproduced exactly ("box-pillar pair present: kept false, rebuilt every step true"). Engine_note quote "the law rebuilds the broad phase...at every step" is verbatim from dispatch-t2-restore.md pin 6 at ref ee2e50a. · [operator 2026-09-25: CITATION ANCHOR: pin numbers cite si-rpg-engine docs/dispatch-t2-restore.md at ee2e50a, the head of PR #43 (closed unmerged). main rewrote that dispatch on route (d) at 9c47d40 and renumbered its pins; PR #53 builds the rewrite.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [rapier3d-f64 0.35.3 source: geometry/broad_phase_bvh/update.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/broad_phase_bvh/update.rs) (2026) — New pairs are added in traversal order; stale pairs are found only among pairs adjacent to updated or removed colliders, then DeletePair is emitted.
  - ✓ [rapier3d-f64 0.35.3 source: geometry/narrow_phase/pair_management.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/narrow_phase/pair_management.rs) (2026) — AddPair adds a contact-graph edge only if none exists; contact pairs leave the graph on DeletePair (or collider removal / sensor change).
  - ✓ [BroadPhaseBvh (rapier3d-f64 0.35.3 API docs)](https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/geometry/struct.BroadPhaseBvh.html) (2026) — new(), update(...) and set_aabb(...) are public; BroadPhaseBvh is Clone and Serialize/Deserialize.

### Expect a rebuilt BroadPhaseBvh to report fewer pairs: new parry leaves are tight, moved leaves are fat
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust rapier3d-f64 0.35.3 / parry3d-f64 0.30.2

**parry stores a new leaf with its raw AABB and adds the 0.04 x length_unit margin only when a moved collider leaves its leaf, so a running world holds fat leaves where a world rebuilt from bodies holds tight ones, and reports a different pair set.**

- **How:** Do not validate a restore by comparing contact-pair counts against a world rebuilt from bodies: it refuses valid snapshots. Restore the broad phase with everything else (serde) or reach the state by replay.
- **Gotchas:** The engine's snapshot lists every contact pair, including broad-phase pairs with zero points, so the pair list itself is history-dependent. Measured in the product-like scene: 5 vs 2 pairs after 5 quanta.
- **In si-rpg-engine:** rapier_law.rs warm_broadphase and rebuild_snapshot (pair list sorted by collider handles); si-rpg-engine T2 (docs/dispatch-t2-restore.md) pin 1's refusal on pair or point counts.
- **Code checks** ([source](restore-internals.code.md#expect-a-rebuilt-broadphasebvh-to-report-fewer-pairs-new-parry-leaves-are-tight-moved-leaves-are-fat)):
  - *Check 1: A rebuilt broad phase reports a different pair set (tight vs fat leaves)* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**

- **Verifier (solid):** Check reproduced exactly ("pairs at load 0; after 3 quanta: running 1, rebuilt 0"). CHANGE_DETECTION_FACTOR = 4.0e-2 exact; new leaves store raw aabb, existing leaves grow by margin only when moved out, confirmed. · [operator 2026-09-25: CITATION ANCHOR: pin numbers cite si-rpg-engine docs/dispatch-t2-restore.md at ee2e50a, the head of PR #43 (closed unmerged). main rewrote that dispatch on route (d) at 9c47d40 and renumbered its pins; PR #53 builds the rewrite.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [parry3d-f64 0.30.2 source: partitioning/bvh/bvh_insert.rs](https://docs.rs/crate/parry3d-f64/0.30.2/source/src/partitioning/bvh/bvh_insert.rs) (2026) — A new leaf stores the raw AABB; an existing leaf is replaced by the AABB grown by the change-detection margin only when it no longer contains the new one.
  - ✓ [rapier3d-f64 0.35.3 source: geometry/broad_phase_bvh/mod.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/broad_phase_bvh/mod.rs) (2026) — BroadPhaseBvh keeps the tree, the pair map, pending_set_aabb and prev_updated_leaves (serialized 'for determinism after snapshot restore'); the margin is 0.04 x length_unit.
  - ✓ [rapier3d-f64 0.35.3 source: geometry/broad_phase_bvh/update.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/broad_phase_bvh/update.rs) (2026) — New pairs are added in traversal order; stale pairs are found only among pairs adjacent to updated or removed colliders, then DeletePair is emitted.

### Never write through a ptr::from_ref pointer to a ContactPair: parking it in a Vec only hides the UB
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust any (ptr::from_ref since 1.76)

**A pointer made by ptr::from_ref from &ContactPair may never be written through; doing so mutates bytes behind a shared reference, which the Reference lists as UB.**

- **How:** Delete such writes rather than wrapping them: there is no UnsafeCell inside ContactPair to make them sound. rustc's deny-by-default invalid_reference_casting rejects `&mut *(ptr::from_ref(p) as *mut T)` in one expression, but the same cast collected into a Vec<*mut T> and dereferenced later compiles silently.
- **Gotchas:** Single-threaded ownership of the world does not make it sound: the rule is about the provenance of the pointer (derived from &T), not about races. A clean compile is not evidence: the lint is pattern-based.
- **In si-rpg-engine:** rapier_law.rs solver_clear_warmstart on main; on the T2 branch (ee2e50a) pairs_mut (~868), carry_warmstart (~880) and solver_restore (~1193) use the same Vec-of-pointers shape.
- **Code checks** ([source](restore-internals.code.md#never-write-through-a-ptrfrom_ref-pointer-to-a-contactpair-parking-it-in-a-vec-only-hides-the-ub)):
  - *Check 1: One-expression &T to &mut T cast is rejected by invalid_reference_casting* · `compile_fail` · edition 2021 · host · lib · lints: invalid_reference_casting · **✔ oracle pass**
  - *Check 2: The engine's shape (pointers parked in a Vec) compiles with no diagnostic* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**

- **Verifier (solid):** Both checks reproduced: one-expr cast rejected (invalid_reference_casting, live-confirmed); Vec-of-pointers shape compiles clean. Engine main:758 and T2@ee2e50a pairs_mut:869-872 use exactly this shape.
- **Compiler:** 2/2 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [std::ptr::from_ref](https://doc.rust-lang.org/stable/std/ptr/fn.from_ref.html) (2026) — The memory behind a from_ref pointer must never be written through it or any pointer derived from it (except inside an UnsafeCell).
  - ✓ [The Rust Reference: Behavior considered undefined](https://doc.rust-lang.org/stable/reference/behavior-considered-undefined.html) (2026) — Mutating immutable bytes is UB, and the bytes pointed to by a shared reference are immutable.
  - ✓ [rustc lint listing: deny-by-default (invalid_reference_casting)](https://doc.rust-lang.org/rustc/lints/listing/deny-by-default.html) (2026) — invalid_reference_casting (deny by default) rejects casting &T to &mut T without interior mutability.

### Read enhanced-determinism as history-deterministic iteration order, not state-canonical order
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust rapier3d-f64 0.35.3 with enhanced-determinism

**enhanced-determinism makes parry's HashMap/HashSet an IndexMap/IndexSet with a pointer-size-independent FxHasher32, forces libm and canonical signed zeros: orders become a deterministic function of the operation history on every IEEE 754 target, not of the current state.**

- **How:** Expect the same bits only from the same history (same insertion order, same steps). Contact-graph edge order, solver colours (which set the Gauss-Seidel order), island ids and map orders all depend on history, so sort by stable keys before hashing, and never expect a world rebuilt from state to iterate like the running one.
- **Gotchas:** IndexMap's swap_remove moves the last entry into the hole, so removal order changes iteration order. serde_json::Value without preserve_order re-sorts map keys, so a Value round trip changes serialized bytes.
- **In si-rpg-engine:** solver/FLAGS.md (enhanced-determinism); rapier_law.rs rebuild_snapshot sorts pairs by collider handles, which hashes a set, not Rapier's solve order; T3's insertion-order test.
- **Code checks** ([source](restore-internals.code.md#read-enhanced-determinism-as-history-deterministic-iteration-order-not-state-canonical-order)):
  - *Check 1: Under enhanced-determinism parry's HashMap is an IndexMap* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**

- **Verifier (solid):** Check reproduced exactly ("[30,10,20,5] -> [5,10,20]"). parry hashmap.rs: HashMap = IndexMap<_,_,FxHasher32> gated on enhanced-determinism, confirmed. Determinism guide and features page live-fetched, both match claims verbatim.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [parry3d-f64 0.30.2 source: utils/hashmap.rs](https://docs.rs/crate/parry3d-f64/0.30.2/source/src/utils/hashmap.rs) (2026) — Under enhanced-determinism HashMap is indexmap::IndexMap with BuildHasherDefault<FxHasher32>; FxHasher32 does not depend on pointer size.
  - ✓ [Rapier user guide: Determinism](https://rapier.rs/docs/user_guides/templates/determinism/) (2026) — Cross-platform determinism needs enhanced-determinism, IEEE 754 targets and the same initial conditions, with bodies, colliders and joints added in the same order.
  - ✓ [rapier3d-f64 0.35.3 feature flags](https://docs.rs/crate/rapier3d-f64/0.35.3/features) (2026) — enhanced-determinism enables parry3d-f64/enhanced-determinism and simba/libm_force; serde-serialize is a separate, optional feature.
  - ✓ [rapier3d-f64 0.35.3 source: staged_island_solver/mod.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/solver/staged_island_solver/mod.rs) (2026) — 'Deterministic: results depend only on the coloring'; moving a colour's solve changes the Gauss-Seidel order and therefore the results.

### Read warmstart_coefficient as a per-substep switch, not as clearing the cached warm start
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust rapier3d-f64 0.35.3

**warmstart_coefficient is read every step inside each substep's constraint update; 0.0 also removes warm starting between the substeps of every quantum, so it is not the same act as zeroing the cached manifold-point values.**

- **How:** Use it to choose a solver behaviour, not to test the cache. A pair of runs at 1.0 vs 0.0 parts on the first loaded quantum even when the cache is empty; a sound zero-then-step (serde or a vendored accessor) and coefficient 0 for one quantum give different results.
- **Gotchas:** Setting 0.0 to avoid carrying warm starts costs stacking quality at the engine's parameters: a 4-box stack sleeps at quantum 50 instead of 33 and the top box sinks 35.7 mm instead of 2.7 mm.
- **In si-rpg-engine:** rapier_law.rs build_world sets warmstart_coefficient = 1.0; T2 route (a) and the replacement for solver_clear_warmstart's test in si-rpg-engine T2 (docs/dispatch-t2-restore.md).
- **Code checks** ([source](restore-internals.code.md#read-warmstart_coefficient-as-a-per-substep-switch-not-as-clearing-the-cached-warm-start)):
  - *Check 1: warmstart_coefficient is read from the first quantum* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
  - *Check 2: Stack at engine parameters: warm start on vs off* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**

- **Verifier (solid):** Both checks reproduced exactly, incl. the 512-quantum stack run (quantum 33 vs 50, sink 2.71e-3 vs 3.57e-2 m). worker.rs:296/438 gate on warmstart_coefficient != 0.0; "banks the previous substep's impulse" comment confirmed near line 500. · [operator 2026-09-25: CITATION ANCHOR: route (a) is in answer 1 of si-rpg-engine docs/rust-kb-answers.md. The test that replaces solver_clear_warmstart's is pin 6 of PR #53 (head bb462c6), and its pin 1 removes solver_clear_warmstart.]
- **Compiler:** 2/2 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [rapier3d-f64 0.35.3 source: staged_island_solver/worker.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/solver/staged_island_solver/worker.rs) (2026) — Inside the per-substep loop, warmstart_coefficient != 0.0 gates the fused contact update and the whole colour-by-colour warm-start stage.
  - ✓ [rapier3d-f64 0.35.3 source: contact_with_twist_friction.rs (update)](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/solver/contact_constraint/contact_with_twist_friction.rs) (2026) — update() reads params.warmstart_coefficient and banks the previous substep's impulse before scaling it by that coefficient.
  - ✓ [IntegrationParameters (rapier3d-f64 0.35.3 API docs)](https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/dynamics/struct.IntegrationParameters.html) (2026) — contact_recycling defaults to true with a 0.05 recycle drift, and contact_clustering defaults to true.

### Restore Rapier through serde-serialize or by replay: world bytes are stable and continue bit-exactly
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust rapier3d-f64 0.35.3 (blobs do not load in 0.36.0)

**With serde-serialize, PhysicsWorld (physics_pipeline and ccd_solver skipped as workspace) round-trips byte-identically, the bytes match across processes and between x86_64 native and wasm32, and a deserialized world continues bit-exactly; the engine's build does not enable the feature.**

- **How:** Serialize the whole PhysicsWorld on save (bincode; serde_json only for shapes without composite-vs-composite pairs), deserialize on restore, and do not run the load pass or any wake_up afterwards. Keep the compact snapshot as the hashed record: rebuild_snapshot of the deserialized world reproduces it.
- **Gotchas:** The bytes are stable, not canonical: they encode history (arena free lists, edge order, colours, IndexMap insertion order). The feature added 686 KB (+47%) to a test wasm module. Running CollisionPipeline + wake_up(true) after deserializing broke the continuation on quantum 0.
- **In si-rpg-engine:** solver/Cargo.toml features (enhanced-determinism only today); T2 route (c): saveSolver/restoreSolver as a serde blob plus the compact snapshot; pin 9 (digest moves once, goldens unchanged).
- **Code checks** ([source](restore-internals.code.md#restore-rapier-through-serde-serialize-or-by-replay-world-bytes-are-stable-and-continue-bit-exactly)):
  - *Check 1: The oracle links rapier3d-f64 as the engine does: PhysicsWorld is not Serialize* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64, serde_json · errors: E0277 · **✔ oracle pass**
  - *Check 2: Cloning every set into a twin with a fresh pipeline and CCD solver continues bit-identically* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**

- **Verifier (solid):** Both checks reproduced exactly: PhysicsWorld not Serialize without serde-serialize (E0277); fresh-pipeline twin continues bit-identically over 120 steps ("first difference: None"). physics_pipeline/ccd_solver confirmed serde(skip). · [operator 2026-09-25: CITATION ANCHOR: pin 9 cites si-rpg-engine docs/dispatch-t2-restore.md at ee2e50a, the head of PR #43 (closed unmerged). main rewrote that dispatch on route (d) at 9c47d40, where serde of the world is held in reserve (answer 4), not built.]
- **Compiler:** 2/2 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [Rapier user guide: Serialization](https://rapier.rs/docs/user_guides/rust/serialization/) (2026) — With serde-serialize the world serializes as a whole; PhysicsPipeline/CollisionPipeline hold no useful state; with enhanced-determinism the same simulation gives the same bytes.
  - ✓ [PhysicsWorld (rapier3d-f64 0.35.3 API docs)](https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/pipeline/struct.PhysicsWorld.html) (2026) — PhysicsWorld implements Serialize/Deserialize under the feature; ccd_solver is 'Workspace only: not part of a snapshot'.
  - ✓ [rapier3d-f64 0.35.3 source: pipeline/physics_world.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/pipeline/physics_world.rs) (2026) — physics_pipeline and ccd_solver are serde(skip); every other set is serialized.
  - ✓ [rapier CHANGELOG (master): v0.36.0](https://raw.githubusercontent.com/dimforge/rapier/master/CHANGELOG.md) (2026) — v0.36.0 (2026-09-24): snapshots serialized with previous versions can't be loaded anymore; ContactPair::manifolds moves to ContactPair::contacts.

### Treat rapier3d-f64 0.35.3 contact pairs as read-only: no public or hook path writes a manifold point
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust rapier3d-f64 0.35.3

**NarrowPhase hands out only &ContactPair; InteractionGraph's *_mut needs &mut InteractionGraph, which is a private field; a MODIFY_SOLVER_CONTACTS hook gets &ContactManifold and SolverContacts with no warm-start fields.**

- **How:** Do not look for a mutable accessor: at 0.35.3 (and 0.36.0) contact_pairs/contact_pair/contact_graph are all &self. If warm-start values must be written, the sound routes are the serde-serialize round trip or a vendored crate with a ContactData-only accessor (contact_data_mut over contact_graph.graph.edges.iter_mut(), same order as contact_pairs()); otherwise keep one persistent world and let Rapier carry its own warm start.
- **Gotchas:** The hook route looks promising because solver_contacts is &mut, but the solver reads warm starts from manifold.points[..].data (contact_with_twist_friction.rs:192-219), which the hook sees by &; hooked pairs are also never recycled, so enabling a hook changes the simulation. EventHandler callbacks get &ContactPair too.
- **In si-rpg-engine:** rapier_law.rs solver_clear_warmstart (main) and, on the T2 branch at ee2e50a, pairs_mut, carry_warmstart and solver_restore all write manifold points through pointers cast from &ContactPair; si-rpg-engine T2 (docs/dispatch-t2-restore.md) pin 1's warm-start write-back has no sound public path.
- **Code checks** ([source](restore-internals.code.md#treat-rapier3d-f64-0353-contact-pairs-as-read-only-no-public-or-hook-path-writes-a-manifold-point)):
  - *Check 1: NarrowPhase has no contact_pairs_mut* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0599 · **✔ oracle pass**
  - *Check 2: contact_graph() is shared: interaction_pair_mut needs &mut* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0596 · **✔ oracle pass**
  - *Check 3: NarrowPhase::contact_graph field is private* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0616 · **✔ oracle pass**
  - *Check 4: A hook cannot write warm start: SolverContact has no warmstart_impulse* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0609 · **✔ oracle pass**
  - *Check 5: A hook cannot write the manifold: ctx.manifold is behind &* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0596 · **✔ oracle pass**

- **Verifier (solid):** 5/5 checks reproduced (E0599/E0596/E0616/E0609/E0596). queries.rs all &self; 0.36.0 (live, today) unchanged. Engine main:758 + T2@ee2e50a 869/880/1193 confirmed casting ptr::from_ref. · [operator 2026-09-25: CITATION ANCHOR: pin numbers cite si-rpg-engine docs/dispatch-t2-restore.md at ee2e50a, the head of PR #43 (closed unmerged). main rewrote that dispatch on route (d) at 9c47d40 and renumbered its pins; PR #53 builds the rewrite.]
- **Compiler:** 5/5 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [NarrowPhase (rapier3d-f64 0.35.3 API docs)](https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/geometry/struct.NarrowPhase.html) (2026) — Every NarrowPhase accessor takes &self and returns shared references; none returns a mutable pair or graph.
  - ✓ [rapier3d-f64 0.35.3 source: geometry/narrow_phase/queries.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/narrow_phase/queries.rs) (2026) — The accessors (contact_graph, contact_pairs, contact_pair, ...) are all &self; no fn returns &mut ContactPair or &mut InteractionGraph.
  - ✓ [NarrowPhase (rapier3d-f64 0.36.0 API docs)](https://docs.rs/rapier3d-f64/0.36.0/rapier3d_f64/geometry/struct.NarrowPhase.html) (2026) — 0.36.0 (2026-09-25) still exposes only &self contact accessors, so a version bump adds no mutable path.
  - ✓ [rapier3d-f64 0.35.3 source: contact_with_twist_friction.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/solver/contact_constraint/contact_with_twist_friction.rs) (2026) — generate() reads warmstart_impulse, warmstart_tangent_world, warmstart_twist_impulse, impulse and solver_dp1/solver_dp2 from the manifold points; writeback_impulses() writes them back.

### Write restored sleep state after the load pass, never through wake_up=true setters
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust rapier3d-f64 0.35.3

**set_linvel/set_angvel/set_translation/set_rotation/set_position(_, true) and wake_up(true) zero time_since_can_sleep; sleep() zeroes velocities; the IslandManager's persistent islands are pub(crate) history that no public call reads or writes.**

- **How:** Set velocities and poses with wake_up = false (or through the builder). Write activation after CollisionPipeline::step and after any wake_up loop: a begin-touch transition in the pass wakes sleeping bodies and the engine's wake_up(true) loop zeroes every timer. Expect island membership, split cooldowns and epochs to come back only through serde.
- **Gotchas:** In a debug build of Rapier, CollisionPipeline::step with a body touching geometry at load panics at manager.rs:140 (the pass reports transitions to an IslandManager that never registered the bodies); release builds compile the assert out.
- **In si-rpg-engine:** rapier_law.rs warm_broadphase (CollisionPipeline pass + wake_up(true) on every non-fixed body) runs before any restored sleep state could be written; si-rpg-engine T2 (docs/dispatch-t2-restore.md) pin 1 orders sleep state before the pass.
- **Code checks** ([source](restore-internals.code.md#write-restored-sleep-state-after-the-load-pass-never-through-wake_uptrue-setters)):
  - *Check 1: Which public setters zero time_since_can_sleep* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
  - *Check 2: IslandManager's persistent islands are not public* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0616 · **✔ oracle pass**
  - *Check 3: The load pass panics in a debug build of Rapier when a body touches at load* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 101 · **✔ oracle pass**

- **Verifier (solid):** All 3 checks reproduced, incl. the debug panic: stdout "before the pass", exit 101, panic at "manager.rs:140:17" matching the cited assert verbatim. IslandManager fields pub(crate); cooldown constant is 16. · [operator 2026-09-25: CITATION ANCHOR: pin numbers cite si-rpg-engine docs/dispatch-t2-restore.md at ee2e50a, the head of PR #43 (closed unmerged). main rewrote that dispatch on route (d) at 9c47d40 and renumbered its pins; PR #53 builds the rewrite.]
- **Compiler:** 3/3 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [rapier3d-f64 0.35.3 source: dynamics/rigid_body.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/rigid_body.rs) (2026) — activation_mut sets the SLEEP change flag; set_linvel/set_translation with wake_up=true call wake_up(true); sleep() zeroes the velocities.
  - ✓ [rapier3d-f64 0.35.3 source: dynamics/island_manager/manager.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/island_manager/manager.rs) (2026) — IslandManager's fields are pub(crate); interaction_changed debug-asserts that non-fixed endpoints are in the active set; rigid_body_updated bumps the epoch.
  - ✓ [rapier3d-f64 0.35.3 source: dynamics/island_manager/persistent.rs](https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/dynamics/island_manager/persistent.rs) (2026) — Persistent islands keep constraint_remove_count (blocks sleep for multi-body islands), a 16-step split cooldown and eager merges with deferred splits.
  - ✓ [RigidBodyActivation (rapier3d-f64 0.35.3 API docs)](https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/dynamics/struct.RigidBodyActivation.html) (2026) — Five public fields (thresholds, time_until_sleep, time_since_can_sleep, sleeping); wake_up(strong) and sleep() are the public state changes.

