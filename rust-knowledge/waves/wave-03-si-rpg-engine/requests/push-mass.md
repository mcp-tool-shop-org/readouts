Push mass (for F5): the character's push with the angular term its mass ratio leaves out. si-rpg-engine PR #82 head `2f7c7c9` (F3's law), rustc and cargo 1.98.1 pinned, rapier3d-f64 0.35.3 with `enhanced-determinism`, parry3d-f64 0.30.2. Measured 2026-09-26.

**Host and tools.** Windows 11 Pro, x86_64, node v22.22.3.

**Engine state.** The engine was cloned from GitHub into scratch; `E:/AI/si-rpg-engine` was not touched. On this host F3's solver builds to digest `b1edc05c…`; the pin is the Linux build's, `89a7b6be…`. F3's JS suite passes 247 of 247.

**Scratch.** `<scratchpad>/push-mass`:
- `engine-f3/`: PR #82 at `2f7c7c9`, with the change (off in the law), the push-mass native test, and the red world's fixture and law run.
- `engine-f5/`: the same, with the law's push switched on (`Shove` passes `Impulses::<true, true>`) and law runs recorded from its own closed-loop runs.
- `redworld.mjs` builds and runs the red world, and `boxtrace.mjs` traces its box.
- `firstdiff.mjs` finds each fixture run's first differing tick.
- `closedloop.mjs` runs every fixture through a law, re-admitting each logged intent against the current frame, and records the law runs.
- `wasmsections.mjs` and `datadiff.mjs` compare two builds section by section.

The standalone measurements behind dimforge/rapier#1020 are in `<scratchpad>/upstream/rapier-kcc*`.

## The change

In `solver/src/impulses.rs`, a third const parameter beside `SEPARATE`, off by default. The law's `Shove` passes `Impulses::<true, true>`.

```rust
pub(crate) struct Impulses<'c, const SEPARATE: bool, const EFFECTIVE: bool = false>(pub(crate) &'c KinematicCharacterController);

// in solve_single_character_collision_impulse, for each contact point:
let mass_ratio = body_mass * character_mass / (body_mass + character_mass);
let mass_ratio = if EFFECTIVE {
    let mprops = body.mass_properties();
    let rn = (contact_point - mprops.world_com).cross(manifold.data.normal);
    let k = rn.dot(mprops.effective_world_inv_inertia * rn);
    mass_ratio / (1.0 + k * mass_ratio)
} else {
    mass_ratio
};
```

`mass_ratio / (1 + k·mass_ratio)` is `1 / (1/m + 1/M + k)`, the effective mass at the point. With k exactly 0 it is F3's `mass_ratio` bit for bit, because x / 1.0 is exact. The `Deref` and method impls gain the parameter; nothing else changes.

## Answer

1. **The red.** [MEASURED]
   - **The world:** `fixtures/push/push-mass-thin-box.json`, given in full below. It is red room A's 5 × 3 room walled 2.0 high, with the walker at the origin and a box with half-extents 0.06, 0.2, 0.12 (mass 0.01152) standing at x = 0.7578125. The walker pushes it from tick 0, for 200 quanta.
   - **On F3's law** the box leaves the first contact at **40.94123133916884 at tick 29, with frame hash `8f201d064bb90bea`**.
     - That is the first tick over 8×, and over 6×.
     - It flies until the east wall stops it, at 2.004 at tick 33.
     - The frame hash at tick 200 is `47411a650b444068`.
   - **The native guard on its law run:** the box leaves the push at 42.5391 times its pusher's speed and has 40.9412 times after the step, both at quantum 29.
   - **Why x = 0.7578125:** the launch depends on the phase of the walker's stride at first contact.
     - Over 16 starts across one stride, x from 0.75 to 0.7646 in steps of 0.015625/16, F3's law launches the box past 8× on 3 of them: 23.86, 33.16 and 40.94. This start is the worst.
     - The other 13 starts peak between 1.6 and 6.8.
   - **On F5's law** the box leaves the first contact at 0.628.
     - Its peak, 1.5509 at tick 134, is not a push. The box topples: it is tilted 30° at tick 120 and 88° at tick 134, with vy −1.30 as it lands, and then it slides at 0.6.
     - The frame hash at tick 200 is `7534c79b4a74b103`.
     - Over the same 16 starts, F5's peaks are 0.79 to 1.55, all at tick 37 or later. The one traced, this start, is the topple.
2. **The control.** [MEASURED]
   - **Off:** the law built with the change off has F3's code section byte for byte (1,457,531 bytes).
     - In the whole module, two bytes of the data section differ. They are the line numbers of the two panic locations in `impulses.rs` below the new doc comment: the `unwrap` of `rigid_body2` (243 → 246) and the index `queries.bodies[body_handle]` (244 → 247).
     - So the digest moves on this host, from `b1edc05c…` to `ab34ea53…`. A slice that adds no lines above those two sites keeps it.
   - **On:** every push of a dynamic body changes, and nothing else.
     - Per law run, F3's push moves the world, and the effective push is given the same world before every push.

     | Run | Quanta on which F3's push changed velocities | Of them, changed by the effective push |
     |---|---|---|
     | behavior-minds | 10 | 10 |
     | behavior-rotation-tumble | 4 | 4 |
     | behavior-verbs-carry-capsule | 11 | 11 |
     | behavior-verbs-carry | 2 | 2 |
     | push-mass-thin-box | 24 | 24 |
     | red-room-a | 81 | 81 |
     | the other 12 runs, the product scene included | 0 | 0 |

     - No push is left bit for bit: k is never exactly 0 at a real contact.
3. **What moves.** [MEASURED]
   - **The product golden:** `6e0d351693b18c93` under both laws, as `fixtures/golden.txt` holds. The product scene never pushes a body.
   - **Fixture runs:** the first tick at which F5's law parts from the recorded hashes. F3's law matches all 16 runs at every tick.
     - behavior-rotation-tumble parts at 14 of 90.
     - behavior-verbs-carry parts at 85 of 253.
     - behavior-verbs-carry-capsule parts at 88 of 261.
     - behavior-minds parts at 60 of 496.
     - The other 12 match throughout.
     - The push fixtures part at red room A's quantum 24 and the red world's 29.
     - Each of these is the run's first push; the native control finds the same six quanta.
   - **The JS suite** on F5, with F3's fixtures: 236 of 248 pass. The 12 that fail are:
     - the four fixture checks: rotation and verbs frame for frame, minds frame for frame, and the law-run file check;
     - the two push fixtures' final hashes;
     - six tests that replay the minds fixture. All six stop at one refusal: the fixture's log entry 1 names the frame `348ee04ec5ad2837`, and F5's run is at `9879101e6a81bab2` there. Re-admitted against F5's frames, all 4 of the minds log's later intents are admitted.
   - **Recaptured under F5** (closed loop, intents re-admitted), the six moved runs end at:

     | Run | F3 | F5 |
     |---|---|---|
     | behavior-rotation-tumble | `45d86b1294896295` | `5f080f6d98073dca` |
     | behavior-verbs-carry | `aeb33a80402e5ef2` after 253 quanta | `41d781c318a6322c` after 262 |
     | behavior-verbs-carry-capsule | `c3647339074627de` | `3a25657f4ce8d002` |
     | behavior-minds | `5e6e1ac2ed3b9ff4` | `2883688e26109ec5` |
     | red-room-a | `f436e7596fd4d6ea` | `69cc8d12a240069f` |
     | push-mass-thin-box | `47411a650b444068` | `7534c79b4a74b103` |

   - **Native,** on F5's own law runs: 26 of 29 pass, the guard included. The three that fail pin F3's claim that the law's push is Rapier's wherever #1004 does not apply, which F5 changes on purpose:
     - `the_change_parts_from_rapiers_routine_in_red_room_a_only_where_two_dynamic_colliders_are_near`: the law parts from Rapier's routine at 24, the first push, instead of 45.
     - `the_copy_with_its_branch_off_moves_the_character_as_rapiers_controller_does_bit_for_bit`: the capsule carry, replayed with the law's push, ends elsewhere than F3's fixture run. Body 0 ends at x 3.049 instead of 3.135.
     - `the_copy_with_its_change_off_pushes_as_rapiers_routine_does_bit_for_bit`: in behavior-minds, main's run (`aff6b0206f69191d`) is no longer the product binary's (`19a58dc84e8658c4`).
4. **The guard afterwards.** [MEASURED]
   - **Pushed bodies (the native guard),** as the push leaves the body and after the step, as a multiple of the pusher's speed:

     | Run | F3 | F5, on its own law runs |
     |---|---|---|
     | push-mass-thin-box | 42.5391 and 40.9412 (quantum 29) | 1.2745 and 1.3155 (quantum 131, while it topples) |
     | behavior-verbs-carry | 3.7008 and 2.8785 (quantum 88) | 0.7678 and 0.7200 |
     | behavior-minds | 3.0233 and 2.5023 | 0.8463 and 0.8328 |
     | behavior-rotation-tumble | 2.2192 and 2.1663 | 0.7314 and 0.7248 |
     | red-room-a | 2.0905 and 2.0535 | 0.6517 and 0.5990 |
     | behavior-verbs-carry-capsule | 1.3063 and 1.0156 | 0.9792 and 0.8510 |

     Through Rapier's own routine, red room A still leaves a push at 25.2731 and has 26.0642 after the step, so the guard's red does not move.
   - **Every body (the JS bound on the push fixtures):** F5's highest is the red world's topple, 1.5509 at tick 134. In red room A the fastest body is the walker itself, at 1.0.
   - **So:**
     - At the push, 1.5× holds under F5 with 0.18 to spare. The highest, 1.3155, comes during a topple; without the red world the highest is 0.98.
     - The every-body bound cannot drop to 1.5×: a box pushed until it tips over falls at 1.55 times its pusher's speed. Either keep that bound near 2×, or measure it on pushed bodies, as the native guard does.
     - Under the linear ratio (F3), a 1.5× guard fails five of the six runs that push. The exception is the capsule carry, whose highest is 1.31.
5. **Rotation through Rapier's public API at 0.35.3.** [SOURCE][MEASURED]
   - **The fields:** `RigidBody::mass_properties()` returns `&RigidBodyMassProps`, whose fields `world_com`, `effective_inv_mass` and `effective_world_inv_inertia` are public.
   - **What uses them:** `apply_impulse_at_point` (`dynamics/rigid_body.rs`).
     - The torque is `(point − world_com) × impulse`.
     - `apply_impulse` adds `impulse ⊙ effective_inv_mass` to the linear velocity.
     - `apply_torque_impulse` adds `effective_world_inv_inertia * torque` to the angular velocity.
   - **So** `effective_world_inv_inertia` is the world inverse inertia itself.
     - Its doc comment calls it the square root (`rigid_body_components.rs:317`). That is stale: the field is set from `local_mprops.world_inv_inertia(&rotation)` (`:531`).
   - **Measured:** 480 probes, covering every dynamic body of every law run at 8 points and 4 normals.
     - Each probe compares `n·(effective_inv_mass ⊙ n) + (r×n)·(effective_world_inv_inertia·(r×n))` with the change in normal velocity that `apply_impulse_at_point` gives a unit impulse.
     - The worst relative difference is 2.8e-16.
   - **The change** uses the angular term only, k, and scales F3's own `mass_ratio`. The linear part stays F3's `body.mass()` and `character_mass`.

## The red world

```json
{
  "name": "push-mass-thin-box",
  "note": "push-mass red world: a light box 0.12 by 0.4 by 0.24 (half-extents 0.06, 0.2, 0.12; mass 0.01152) standing in red room A's 5 by 3 room, walled 2.0 high, with the walker pushing it from tick 0. The box starts at x = 0.7578125, the phase of the walker's stride, of 16 across one stride, at which F3's law launches it hardest: 40.94123133916884 at tick 29, frame hash 8f201d064bb90bea. The frame hash at tick 200 below is F3's law's (PR #82 at 2f7c7c9).",
  "seed": 11,
  "quanta": 200,
  "world": {
    "name": "push-mass-thin-box",
    "bodies": [
      { "id": "walker", "x": 0, "y": 0.26, "z": 0, "vx": 0, "vy": 0, "vz": 0, "hx": 0.25, "hy": 0.25, "hz": 0.25 },
      { "id": "box", "x": 0.7578125, "y": 0.201, "z": 0, "vx": 0, "vy": 0, "vz": 0, "hx": 0.06, "hy": 0.2, "hz": 0.12, "qx": 0, "qy": 0, "qz": 0, "qw": 1 }
    ],
    "colliders": [
      { "id": "floor", "minX": -1.5, "maxX": 3.5, "minY": -1, "maxY": 0, "minZ": -1.5, "maxZ": 1.5 },
      { "id": "wall-west", "minX": -1.5, "maxX": -1.3, "minY": 0, "maxY": 2, "minZ": -1.5, "maxZ": 1.5 },
      { "id": "wall-east", "minX": 3.3, "maxX": 3.5, "minY": 0, "maxY": 2, "minZ": -1.5, "maxZ": 1.5 },
      { "id": "wall-south", "minX": -1.5, "maxX": 3.5, "minY": 0, "maxY": 2, "minZ": -1.5, "maxZ": -1.3 },
      { "id": "wall-north", "minX": -1.5, "maxX": 3.5, "minY": 0, "maxY": 2, "minZ": 1.3, "maxZ": 1.5 }
    ],
    "zones": [],
    "minds": []
  },
  "script": [
    { "tick": 0, "kind": "intent", "verb": "push", "actor": "walker", "target": { "body": "box" } }
  ],
  "log": [
    { "tick": 0, "hash": "96ae398296ae3982", "proposal": { "kind": "intent", "verb": "push", "actor": "walker", "target": { "body": "box" }, "frameHash": "96ae398296ae3982" } }
  ],
  "hash": "47411a650b444068"
}
```

Under F5 its `hash` becomes `7534c79b4a74b103`. The tick-0 hash in the log is the world's and does not change.

## Caveats

- **The red world** is one geometry at the worst of 16 stride phases. The topple that sets F5's highest speed is a property of a tall, thin box pushed at its lower half.
- **The closed-loop reruns** re-admit logged intents against the current frame; the minds log needed 4 re-targeted. That is what recapturing the fixtures would do, and the intents themselves are unchanged.
- **Open loop against closed loop:** the native guard gives the same numbers on F3's recorded runs with the effective push as on F5's own runs, to every printed digit. The tick's recorded writes (driven velocities, pins) do not depend on where the pushed bodies go in these runs.
- **Upstream:** the mass ratio is reported as dimforge/rapier#1020, with a standalone repro. On rapier3d-f64 0.36.0, one frame launches a box with half-extents 0.06, 0.2, 0.12 at 44 times the character's speed; the effective-mass impulse gives 0.742.

## Commands

```
git fetch origin pull/82/head:pr-82 && git worktree add engine-f3 pr-82 && git worktree add --detach engine-f5 2f7c7c9
cd engine-f3 && node <scratch>/redworld.mjs <out.json> 200 8 0.7578125      # the red world on F3's law; the 16-phase scan varies the last argument
node solver/build.mjs                                                       # with the change off; then compare against F3's own build:
node <scratch>/wasmsections.mjs <f3.wasm> <off.wasm> && node <scratch>/datadiff.mjs <f3.wasm> <off.wasm>
cd solver && cargo +1.98.1 test --release push_mass_control_guard_and_probe -- --nocapture
cd engine-f5 && node solver/build.mjs && npm test --ignore-scripts && node harness/sim.mjs
node <scratch>/firstdiff.mjs && node <scratch>/closedloop.mjs --write
cd solver && cargo +1.98.1 test --release -- --nocapture --test-threads=1
node <scratch>/boxtrace.mjs <thin-box.f5.json> 120 140
```
