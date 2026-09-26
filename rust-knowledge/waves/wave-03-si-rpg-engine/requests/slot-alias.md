Slot alias (si-rpg-engine issue #71): can a collider inserted in the quantum another is removed take its broad-phase slot, so that a shape query that quantum resolves the old leaf to the new collider? rapier3d-f64 0.35.3 with `enhanced-determinism`, parry3d-f64 0.30.2; the law at main `93a2d1e`. Measured 2026-09-26.

**Host and tools.** As `squeeze-launch.md`. The demonstration is a scratch crate, `<scratchpad>/slot-alias`, that links rapier3d-f64 0.35.3 and parry3d-f64 0.30.2 through the `PhysicsWorld` API the law uses. The law measurements use the same scratch F2 worktree as `squeeze-launch.md`.

## Answer

1. **Yes, the slot is reused, and the stale leaf resolves to the new collider, not to nothing. But the alias cannot produce a hit at the removed body's old place.** Every query re-reads the collider's current shape and pose, so a cast through the old place is tested against the new collider where it really is. [SOURCE][MEASURED]
   - **What the alias does.** Until the next step, the newly dropped body is visible to exactly those queries whose region overlaps the removed body's old footprint. It is found there only where its real geometry meets the query.
   - **The other order.** A drop that does not reuse a freed slot is invisible to every query until the step.
   - **What decides it.** The law applies a quantum's switches in record-index order. So whether a dropped body can be found in its drop quantum depends on whether a body with a lower index was picked up in the same quantum.
   - **Determinism.** It is deterministic either way.
2. **A scene that shows the alias** (section 2; the failing test in #71's sense does not exist). A floor and a box J are stepped once. Then J is removed and a box K inserted 3 units away; K takes J's slot. Until the next step:
   - an AABB query over J's old place returns K;
   - a cast through J's old place alone misses (no phantom);
   - a cast through K's place alone misses (K has no leaf yet);
   - a cast that crosses both finds K, at K's real face.

   With the insertion before the removal, K gets a fresh slot and every query misses it until the step.
3. **Fixes.** None is needed for correctness: there is no phantom hit, and the next step removes the stale leaf before it adds the new one.
   - If the engine wants a dropped body's first-quantum visibility not to depend on index order, the cheapest deterministic change is to apply drops before pick-ups in `switch_in_place`. That is a one-line stable sort. A drop can then never take a slot a pick-up freed in the same quantum.
   - Measured on F2: it moves nothing. Product golden `6e0d351693b18c93`, 244 of 244 tests, the switch tests included.
   - Of #71's candidates, "reorder so every removal completes before any insertion" is the order that produces the alias. Removal-first is exactly when the insertion takes the freed slot.

## 1. The source [SOURCE]

**The law** (`solver/src/rapier_law.rs`, `switch_in_place`, `93a2d1e`):
- It plans every body's transition, then applies them in record-index order.
- A pick-up calls `loaded.world.remove_body(handle)`, and a drop calls `loaded.world.insert(body, co)`.
- Neither touches the broad phase. The broad phase sees both at the next `PhysicsWorld::step`, and `integrate` runs the characters' queries before that.

**The collider arena** (rapier `data/arena.rs`):
- `remove` (`:353-372`) frees the slot, pushes it on the head of the free list, and bumps the arena generation.
- `insert` takes `try_alloc_next_index` (`:259-274`), which pops that head. So the next insertion reuses the most recently freed slot, with the new generation.
- `ColliderSet::remove` (`geometry/collider_set.rs:335-364`) records the removed handle in `removed_colliders`. `ColliderSet::insert` (`:167-177`) records the new one in `modified_colliders`.

**The broad phase** (`geometry/broad_phase_bvh/update.rs`) keys its BVH leaves by collider slot index. At the next step, `update` (`:35`) removes leaves for `removed_colliders` first (`:53-57`), with the comment: "Removals must be handled first, in case another collider in `modified_colliders` shares the same index." Then it inserts or updates the modified colliders. So the step itself handles a shared index correctly. Between the switch and that step, the removed collider's leaf, with its old AABB, is still in the tree under the reused index.

**The queries** (`pipeline/query_pipeline.rs`) turn a leaf into a collider by slot alone, `self.colliders.get_unknown_gen(leaf)`, which ignores the generation (arena `:757-768`), and then test that collider's current `co.position()` and `co.shape()`:

| Query | Lines |
|---|---|
| composite-shape part access for shape casts | `:101-127` |
| rays | `:298-302` |
| points | `:386-388` |
| `intersect_aabb_conservative` | `:420-432` |
| shape intersection | `:552-555` |
| `id_to_handle` | `:170-171` |

The stale AABB only decides which leaves are visited. It is never used as geometry.

**Rapier 0.36.0** keeps all of this:
- `arena.rs` is unchanged.
- The broad phase's changes are renames.
- The query pipeline still resolves leaves with `get_unknown_gen`, now inside `handle_of`.
- `ColliderSet::remove` is refactored into `remove_internal`, which takes the soft-body set.

## 2. The demonstration [MEASURED]

`slot-alias` builds a floor, and a dynamic box J (half 0.25) at x = 0, then steps once so J has a leaf. Then it either removes J and inserts box K at x = 3, or inserts K and then removes J. Queries use a pipeline built exactly as the law builds it (`broad_phase.as_query_pipeline`), excluding fixed bodies; each cast is a 0.1-half probe box moving along +x at y = 0.25.

| Query | Remove J, then insert K: before the step | After the step | Insert K, then remove J: before the step | After the step |
|---|---|---|---|---|
| K's handle | slot 1, generation 1 (J's slot) | same | slot 2, generation 0 | same |
| AABB over J's old place | **K** | nothing | nothing | nothing |
| AABB over K's real place | nothing | K | nothing | K |
| cast through J's old place only (x −1 to 1) | no hit | no hit | no hit | no hit |
| cast through K's place only (x 2 to 4) | no hit | hit K at x 2.65 | no hit | hit K at x 2.65 |
| cast through both (x −1 to 4) | **hit K at x 2.65** | hit K at x 2.65 | no hit | hit K at x 2.65 |

The only difference the alias makes is in the two bold cells. Before the step, K is reachable through J's old footprint, and only at K's own geometry.

## 3. What it can and cannot do in the law [REASONED from section 1, measured in section 2]

- **It cannot** give a character a hit, a contact or a ground contact where the removed body used to be. `move_shape`'s casts, its grounded check (`intersect_aabb_conservative`, then real contact manifolds) and `solve_character_collision_impulses` all test real geometry.
- **It can** let a character's cast, in the quantum of a same-quantum pick-up and drop, find the dropped body one quantum early. That needs the cast's swept region to overlap the picked-up body's old footprint and the dropped body's real shape to lie on the cast. With the opposite index order, the same cast passes through the dropped body's space for that one quantum, as any freshly dropped body does today.
- **It is deterministic.** It depends only on the record indices, which the law fixes.

## 4. Fix candidates

| Candidate | Effect | Cost measured on F2 |
|---|---|---|
| none | alias as in section 3; no phantom | none: golden `6e0d351693b18c93`, 244/244 |
| apply drops before pick-ups (`plan.sort_by_key(\|(_, t)\| matches!(t, Transition::PickUp(_)))` before the apply loop) | a dropped body never takes a slot freed that quantum, so it is uniformly invisible until the step | nothing moves: golden `6e0d351693b18c93`, 244/244, probe hash unchanged |
| remove the leaf at pick-up | not possible through rapier's public API: `update` and `set_aabb` are the only public methods of `BroadPhaseBvh` that change its tree | n/a |
| `broad_phase.set_aabb(params, dropped_collider, aabb)` right after a drop | the dropped body is visible at its real place at once, whatever the order | not measured. At the next step, `update` removes the reused index's leaf before reinserting the modified collider, so correctness rests on that ordering. |
| run a broad-phase update when a removal and an insertion share a quantum | the same, through rapier's own update | not measured. Driving `update` outside the pipeline consumes the removed and modified lists that the narrow phase also needs, so it would need the collision pipeline's own step, as `warm_broadphase` does at load, and that also touches contacts. |

With no phantom, #71 can close as "reuse confirmed, no wrong hit". Drops-first is the cheapest way to make first-quantum visibility independent of index order.

## Commands

```
cd <scratchpad>/slot-alias && cargo +1.98.1 build --release --offline && ./target/release/slot-alias.exe
python <scratchpad>/squeeze-launch/patch_law.py <engine-f2> u4-drops-first && bash <scratchpad>/squeeze-launch/measure.sh <engine-f2> u4-drops-first <minds-7bbed41.json> f2
```
