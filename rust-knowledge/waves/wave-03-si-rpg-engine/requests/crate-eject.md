# Crate eject: the bench room's drop at the step's edge

Issue #114. si-rpg-engine `main` at `19cf8c89a04c8d972168e91a5a8c82e3ba8e2a23` (`19cf8c8`). rapier3d-f64 0.35.3 with `enhanced-determinism`, parry3d-f64 0.30.2, rustc 1.98.1, `wasm32-unknown-unknown`, relaxed SIMD off. `dt` is 1/64. Dynamic bodies are built with `ccd_enabled(false)`. `max_ccd_substeps` stays at its inherited 1. Measured 2026-09-26.

**Host and tools.** Windows 11 Pro 10.0.26340, x86_64. rustc 1.98.1 (48a229cea 2026-09-01), node v22.22.3.

**Engine state.** The engine was cloned from the local repository into scratch and checked out detached at `19cf8c8`. Nothing in `E:/AI/si-rpg-engine` was read, built, run, or changed. That checkout stays on `dispatch-t7c` at `b9cf38f`. This host's wasm was not written to `fixtures/solver.sha256`. The uninstrumented build's digest here is `9ff6d183d8c76ead2a3b37ab59df3bf1f7336f654d854d6bf186e47e98b46f3e`.

**Scratch.** `<scratchpad>/crate-eject`. `probe.mjs` runs `considerWorld` on `fixtures/bench/room.json`. `replay-analyze.mjs` replays the finding's witness. `trace-release.mjs` reads a scratch instrumentation of `integrate`: the crate's velocity before the character-impulse pass, after it, and after `world.step()`. On the release quantum that instrumentation matches the uninstrumented replay bit for bit. `controls.mjs` repeats the release from the saved pre-release state.

## Re-aim: the 0.25 step-up

The overseer's replay agrees with the placement above: the drop puts the crate inside the walker, at the point the walker has just reached, and `release` does not check again. Same pins. The question is how that step-up reaches a dynamic box, and whether F5's guard counts it.

**Through contacts.** The push copy does not carry the step.

`handle_stairs` adds the rise to the movement and takes it off the remaining translation after the hit has already been recorded (`kcc.rs:847-857`, `result.translation += step + horizontal_nudge`, and `*translation_remaining -= step`). The `CharacterCollision` was emitted at `kcc.rs:357-363`, so its `translation_remaining` is the remaining slide from before the stair. The law then sets the whole movement, rise included, as the kinematic body's next pose (`rapier_law.rs:841`).

The push copy transfers that recorded remainder, not the pose (`impulses.rs:176-177` and `:240`): `normal * remaining.dot(normal) / dt`. On the room's release quantum the pass hits the crate **0** times and leaves its velocity at **0**. `world.step()` then writes **(2.037523572148399, 15.937582192666424, −0.009280713810592341)**. Rapier's own `solve_character_collision_impulses` in place of the copy does the same. The rise is `interpolate_kinematic_velocities` (`physics_pipeline/substep.rs:242-263`) calling `interpolate_velocity` (`rigid_body_components.rs:147-152`), `linvel = pose_err.linear * inv_dt`, and the contact solver writes it onto the box. The walker's centre rose **0.2501000017434255** in that quantum, **16.006400111579232** m/s at `dt = 1/64`. [MEASURED][SOURCE]

A box that only meets the head, and one that overlaps the body, do the same on a 0.25 step at horizontal speed 1. The push sees the box (9 hits) and writes **vy 0.006668924763429998**. The step then writes **vy 16.494756913014285** for the box on the head (speed 16.5136537099776) and **vy 16.55225921744732** for the overlapping box (speed 16.58449750396707). The 0.0067 is not the rise. [MEASURED]

A body the walker **carries** is not in the solver (`Mode::Carried` inserts no body). After the step, `pinCarried` (`world.js:142-162`) sets its centre to the walker's plus both vertical half-extents and zeroes its velocity. On the same step the walker climbs **0.2501** and the carried box ends at the walker's new head, speed **0**, with no Rapier handle and **0** hits. The rise reaches it as that copy, not through contacts and not through the push. [MEASURED][SOURCE]

**F5's guard does not count the step-up as the character's speed.** The bound is the record's horizontal speed at the start of the quantum (`rapier_law.rs:3472`):

`(b[3] * b[3] + b[5] * b[5]).sqrt()`

Slot 4, the vertical velocity, is not in it. The room walker's record at the release quantum is (0.7005004858589507, 0, 0.7136519244781548). The horizontal speed is **1**, and the guard's multiple is **1.5**. The rise is not in that record: the plan's vertical velocity is 0 once the controller reports grounded (`rapier_law.rs:830-831`). The guard then scores only a body whose velocity the push changed (`rapier_law.rs` `Guarded::push`, the bit compare before `self.pushed.push`). The room crate's bits do not change in the push, so its **16.067299542446676** after the step is not scored. A box the push does touch is scored after the step at its full `linvel`, still against the horizontal 1: the box on the head would be **16.51** times its bound. [MEASURED][SOURCE]

## Answer

The numbers match the second case. `admitRelease` admits a pose that overlaps no static collider and no body. The physics then ejects the crate. The fix the numbers support is a checker rule.

1. **The released volume overlaps no static collider.** The drop is admitted at tick 454 and places the crate at the start of the quantum that advances to tick 544. `supportAt(1.25, 1.75, actor.y + 8)` returns **0.25, the step's top**, at both ticks. The floor's surface is 0. `consider` keeps the greater one (`world.js:751`, `y > best`).
   - The query point is the step's west face. In the step's local frame the ray origin's x is **−0.375, equal to the face** (`min` x is −0.375). The parallel-axis test is `origin[a] < min[a] || origin[a] > max[a]` (`world.js:798`). Equality is not a miss. `t0` is 8.009999998256575, not 0, so the `t0 === 0` branch (`world.js:820-822`), which returns `fromY`, does not run. The return is `fromY - t0` (`world.js:827`) = **0.25**.
   - Placement is `support + hy + 0.05` (`predicates.js:280`, `world.js:961`). The centre is **(1.25, 0.55, 1.75)**. The crate spans y **0.30 to 0.80**. The step spans y **0 to 0.25**. The y intervals miss by **0.050 m** (the crate is above the step). On x they would overlap by **0.250 m**, and on z by **0.500 m**. `overlaps` uses `<=` and `>=` (`world.js:461`), so a face that only touches is not an overlap. Every static collider misses. `overlaps` returns null for the statics.
   - At tick 454 the walker is at (0.2684200367636458, 0.2499437119189832, 0.7499915147326947), still carrying the crate. Distance to (1.25, 1.75) is 1.401255221161974. At speed 1 that is **90 quanta**. `volumeClear` finds no body. `overlaps` returns null. `admitRelease` accepts the pose.
   - At the release quantum the walker is at (0.989899999665149, 0.25999999825657394, 1.739899999997309), velocity (0.7005004858589507, 0, 0.7136519244781548). The same placed volume overlaps the **walker**, by **0.239900 m on x, 0.210000 m on y, and 0.489900 m on z**. `overlaps` returns `walker`. `volumeClear` would return `walker` and `admitRelease` would refuse with `standing volume is blocked`. `release` (`world.js:949`) does not call it. [MEASURED][SOURCE]

2. **The launch is Rapier's contact response to the walker's step-up, inside `world.step()`.** On the release quantum the crate's velocity is 0 before the character-impulse pass and 0 after it. `move_shape` records 4 collisions and **0 against the crate**. After `world.step()` (`rapier_law.rs:859`) the velocity is **(2.037523572148399, 15.937582192666424, −0.009280713810592341)**, speed **16.067299542446676**.
   - The walker's centre goes from y 0.25999999825657394 to y 0.5100999999999994 in that quantum: **+0.2501000017434255 m**, which is 16.006400111579232 m/s at `dt = 1/64`. Its feet start a skin above the floor and end a skin above the step. The law sets that translation with `set_next_kinematic_translation` (`rapier_law.rs:841`) before the step.
   - Rapier turns the pose change into a velocity in `interpolate_kinematic_velocities` (`physics_pipeline/substep.rs:242-263`, called at `:477`), which calls `RigidBodyPosition::interpolate_velocity` (`rigid_body_components.rs:147-152`): `linvel = pose_err.linear * inv_dt`. The contact solver then runs that velocity through the manifold. The bias term is `contact_with_twist_friction.rs:488-489`. Setting `normalized_max_corrective_velocity` to 0 on this quantum leaves vy at **15.931192766673794**. The corrective cap is not the source.
   - Skipping `pusher.push` (`rapier_law.rs:856`, `solver/src/impulses.rs`) leaves the same velocity bit for bit. Calling Rapier's own `solve_character_collision_impulses` instead of the engine's copy does too. The product law and stock Rapier 0.35.3 do not differ on this quantum. [MEASURED][SOURCE]
   - The greatest speed afterwards is **16.935883603199272** at tick 806, velocity (2.0374635761633666, −16.81287597083518, −0.009858307888372103). The horizontal component is the release quantum's. The vertical component is that launch under gravity. The centre is then y **−1.0352618235859863** at (x, z) **(9.62282217918251, 1.7095560991381176)**. The frame hash is `38172e72e9a2ebee`, the sweep's hash.

3. **The centre goes over the wall.** The first quantum with x greater than 4 is tick **630**, centre **(4.01979734473329, 14.993115846210793, 1.736666445831082)**, speed **5.572935555375275**, velocity y **+5.187124029164821**. The east wall occupies x 3 to 4 and y 0 to 3. The centre is above the wall. [MEASURED]

4. **A target whose volume misses the step still launches, and stays inside the room.** At x = 1.0 the crate's east face equals the step's west face, so `overlaps` does not meet the step. The downward ray misses it (`origin` x −0.625 is less than `min` x −0.375), and `supportAt` returns the **floor, 0**. The centre is placed at y 0.30. That volume still overlaps the walker. The release quantum's velocity is (0.034849599859587514, 16.987723377461087, −0.018473560814907704), speed **16.987769168322174**. Over the next 270 quanta, x stays below 4 and y stays above −1. At quantum 270 the centre is (1.1464671671126103, 1.1439624760033653, 1.5325064863148488), still at speed 16.664009058072303.
   - The same release with the target at x = 1.49, the first centre whose volume also misses the walker (`overlaps` returns null, `volumeClear` would accept it), has release-quantum speed **1.7252827784610951** and is at rest at (1.6929064544785544, 0.4999437941586928, 1.7438135952010365) inside the 270 quanta. The original leaves at quantum 262 of this same continuation, at the sweep's y −1.0352618235859863. [MEASURED]

**What the dispatch can take.** A checker rule. At the release quantum, `volumeClear` finds the walker, which is the overlap the step ejects. The same quantum with a target `volumeClear` accepts stays in the room and comes to rest. The 16 m/s is stock Rapier's response to a 0.250 m kinematic step in one quantum of 1/64 s, and the engine's `impulses.rs` does not write it.

## Reproduction

`considerWorld` on `fixtures/bench/room.json` refuses. The reason is the issue's sentence, and the bundle replays to the same hash:

`crate leaves the world after drop (1.25, 1.75) by walker: its centre is at y -1.0352618235859863, below the lowest collider minimum -1, at tick 806 at (x, z) (9.623, 1.710), past the edge of every collider`

The sweep ran 109,593 quanta in 7.9 s. The witness log is pick-up at 36, move to (1.75, 0.75) at 184, drop at (0.25, 0.75) at 255, pick-up at 420, drop at (1.25, 1.75) at 454. The earlier drop ends at speed 0.308 and the crate is still there to be picked up at 420. The cell the second drop is taken from is `walker 0,0,1 carries crate`.
