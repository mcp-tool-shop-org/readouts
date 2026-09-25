Walker stall: why the T4 product walker loses a quantum's travel. si-rpg-engine PR #56 head `48890ef9b3742bd1a7bc7ffbe40628fc477a5cbe`, rapier3d-f64 0.35.3 with `enhanced-determinism`, parry3d-f64 0.30.2, glam 0.33.10 (all from `solver/Cargo.lock` at that commit). Measured 2026-09-25.

**Host and tools.** Windows 11 Pro 10.0.26340, x86_64 (the route-costs host). rustc and cargo 1.98.1 (48a229cea 2026-09-01), node v22.22.3.

**Engine state.**
- `48890ef` was cloned from GitHub into scratch and re-checked-out with LF line endings, so `solver/src/rapier_law.rs` hashes the same as GitHub's raw file (`53fcc1a5…`).
- Nothing was built or run inside `E:/AI/si-rpg-engine`, and no tracked file changed. The only commands there were `git log`, `git status`, `git branch --show-current` and `git cat-file`; that clone does not contain `48890ef` and stays on `main` at `2c2631f`.

**Scratch.** `$S = <scratchpad>/walker-stall`, a session scratch directory that is not kept in this repo. Raw outputs are in `$S/out/`.

## Answer

1. **Where the travel goes.** On a stalled quantum, the floor hit's `normal1` is exactly `(0, 0x3fefffffffffffff, 0)`: vertical in direction, with y = 1 − 2⁻⁵³.
   - Because the normal is parallel to `up`, `decompose_hit` finds no horizontal-tangent direction. `n × up = 0` and `try_normalize` returns zero (character_controller.rs:698-704), so the whole tangent is filed as "vertical tangent".
   - Its y is the leftover from removing the normal component: −2⁻⁶¹ = −4.34e-19. `handle_slopes` reads that as "slipping without intent on a non-slip slope" and keeps `horizontal_tangent + normal_part` = 0 (:649-651).
   - Only the 1e-4 nudge survives. The quantum keeps 5.1% of its travel (GJK path) or 0% (contact-fallback path). [SOURCE][MEASURED]
2. **Why about one quantum in 30.** GJK returns its normal as −proj·fl(1/|proj|).
   - On 23% of quanta at the origin and 37% at 1e6, the final projection has x and z exactly 0.
   - For about 14% of doubles d, d·fl(1/d) rounds to 1 − 2⁻⁵³.
   - The product is about 3.3%: 332 stalls in 10,000 quanta at the origin, 323 at 1e6.
   - One ulp of the walker's x or y switches a stall on or off. There is no threshold. [MEASURED]
3. **Offset-moved, not offset-caused.**
   - The untranslated scene stalls as often: 23 stalls in the first 640 quanta, the first at q98.
   - At 1e6, every world-x add loses 2.33e-11 to the 2⁻³³ grid. GJK therefore sees different input bits from q2, and the stalls land on other quanta; the first is q3.
   - The cause is not a wall hit, not autostep, not snap and not the nudge. [MEASURED]
4. **The fix.**
   - **Settings-level (works inside a window).** `up = (0, 1, 1e-12)` removes every stall (0 and 0). The course, the step in 4 directions from 20 approach phases each, and the step limit all stay green or unchanged. It only works inside a measured window: at 1e-17 the +z stalls return, and from 1e-8 up the +z step is refused.
   - **Usage-level (fixes the degeneracy itself).** The engine keeps its own copy of `move_shape`, which needs only rapier's public API and, unpatched, reproduces rapier's own call bit for bit. One branch is added to `decompose_hit`. Measured: 0 stalls at both offsets, course green, thresholds unchanged, no window.
   - **What remains.** Under either fix the walker's y still disagrees by 1e-4 between offsets on about 40% of quanta. That is a separate bit-level flip in the hover phase. The split-call variants that remove it turn course 5.9 red.

## 1. Reproduction

### Scene

This is `harness/product-scene.mjs` `productInit()` as `harness/outcome.test.js` `translatedRun()` drives it (48890ef).
- **Walker:** a box with half-extent 0.25, starting at (10, 0.26, 0) with vx = 0.4 and mode 1 every quantum. Its feet start exactly `SKIN` = 0.01 above the floor.
- **Floor:** x 4 to 80, y −1 to 0, z −2 to 6.
- **The rest of the scene:** six other bodies, three more colliders and the 2×3 heightfield. The climber is lifted at steps 200-259 and the parcel is carried from step 400, so the world rebuilds at 200, 260 and 400.
- **Offset:** the translated run adds (1e6, 0, 1e6) to every body and collider, as the test does.
- **The law's walker path** (`rapier_law.rs` at 48890ef) [SOURCE]:
  - `vy = b[4] + G*DT` (:519) and `desired = (b[3], vy, b[5]) * DT` (:523), which is (0.00625, −0.001953125, 0) on a grounded quantum;
  - the filter excludes the walker's own body (:528), then `move_shape` runs (:537);
  - `vy = 0` when the move reports grounded (:539);
  - the new translation is `pos + movement.translation` (:542), applied through `set_next_kinematic_translation` (:550), then `world.step()` (:568).
- **Controller** (`controller()`, :282-297, with the constants at :29-34): as the question lists; I read it at 48890ef rather than relying on the list.

### Programs

- **`$S/harness/`** is a native crate using the solver's `Cargo.lock` unchanged (`--locked`).
  - `src/lib.rs` and `src/rapier_law.rs` are the engine's files. The only differences are two hooks, which are no-ops by default:
    - `controller()` returns `crate::probe::adjust(c)`;
    - `integrate()` calls `probe::after_move` after rapier's `move_shape`, and calls `probe::alt_move` only when a usage variant is selected.
  - `src/main.rs` replays `world.js` `step()` (`solverModes`, then `build.mjs` `writeInputs`, `solver_step`, `readBodies`, then `pinCarried`) and `applyProductAct()`. Its subcommands are `run`, `outcome4`, `course`, `dirs`, `stepscan` and `limits`.
  - `src/kcc.rs` is a verbatim copy of rapier 0.35.3's `move_shape` and every private helper it calls, with trace points added. `probe::traced` runs it beside rapier's own call on every quantum and exits unless the translation, `grounded`, `is_sliding_down_slope` and every `CharacterCollision` agree bit for bit. It never exited: 20,000 product quanta, plus the course.
  - `src/bin/probe_state.rs` builds a floor-only world the way `build_world` builds the product floor, and replays single quanta from pose bits.
- **Per-quantum records** are `$S/out/origin.tsv` and `$S/out/far.tsv`. Each row holds:
  - the walker's x, y, z bits, dx, dy, and an FNV hash over all 7 bodies × 13 record fields;
  - `grounded`, `is_sliding_down_slope` and the loop iteration count;
  - for every loop iteration: the cast origin, direction and distance, the hit (collider, TOI, normal1, normal2, witness1, witness2, status), `is_wall`, `is_nonslip`, angle, stairs, the slope decomposition and the branch taken;
  - the snap result.

### The port is the engine [MEASURED]

- **Build.** The engine's wasm was built from the scratch clone with the unmodified `node solver/build.mjs`. The lint was clean; this host's digest is `b9724fba…`, and the pinned `c311d3aa…` is the Linux build, as `build.mjs` expects.
- **Driver.** `$S/node/drive_product.mjs` imports the clone's own `packages/tick/world.js`, `harness/product-scene.mjs` and `harness/behaviour.mjs`, and runs `translatedRun` verbatim.
- **Per quantum, 10,000 quanta, both offsets:** the walker's x, y, z bits and the all-body hash are identical at every quantum, 0 differing. Sleep quanta are identical too, including slider 189 against 233.
- **The engine's own tests**, run under node on the clone:
  - `course.test.js` prints the same diagnostics as the native course replica, all 10 cases;
  - `outcome.test.js` outcome 4 prints the same 13 diagnostics as the native replica.
- **The test comment's numbers are reproduced:**
  - 23 stalls in the first 640 quanta at the origin, the first at q3 at 1e6;
  - the walker's final x off by 3.83e-2;
  - lower off by 5.68e-5, upper by 1.16e-3 and the slider by 4.74e-1.
- **The stall depends on nothing else.** Every quantum of both runs was replayed through the floor-only probe, with the pose taken from the previous row. All 9,999 translations came out bit-identical, with all 332 and all 323 stalls. The stall is therefore a pure function of the walker's pose bits, the floor pose and the controller settings: no other body, no rebuild and no physics step is involved.
- **Debug agrees with release.**
  - The floor-only replay built in debug gives the same 9,999 of 9,999.
  - The debug product run stops at q196 on rapier's island-manager `debug_assert` (`dynamics/island_manager/manager.rs:140`), in the physics step and not the controller. The 195 quanta before that match release bit for bit at both offsets, including the origin's 7 stalls and the 1e6 run's 10 in that span.

## 2. The mechanism

### 2.1 The branch that eats the travel [SOURCE]

All references are to `rapier3d-f64-0.35.3/src/control/character_controller.rs`.
- **The loop, :343-428.** Each iteration casts the shape along the remaining translation, with `target_distance = offset` and `stop_at_penetration = false` (:354-364). A hit calls `handle_stairs` (:382), which returns at :737 unless `is_wall`, and then `handle_slopes` (:393).
- **`compute_hit_info`, :667-681.** `angle = up.angle_between(normal1)`; `is_wall = angle >= max_slope_climb_angle`; `is_nonslip_slope = angle <= min_slope_slide_angle`. For the stall normal the angle is 0: a non-slip slope, not a wall.
- **`decompose_hit`, :683-711.**
  - `tangent = t − normal_part − penetration_part` (:696).
  - `horizontal_tangent_dir = normal1.cross(up).try_normalize().unwrap_or_default()` (:698, :702). For `normal1 ∥ up` the cross product is zero; glam's `try_normalize` returns None when `1/length` is not finite (glam 0.33.10 `dvec3.rs:654-661`), so the direction is zero.
  - Hence `horizontal_tangent = 0` and `vertical_tangent = tangent` (:703-704).
- **`handle_slopes`, :623-659.**
  - `slipping_intent` is judged on the horizontal input (:637), and `slipping = up·vertical_tangent < 0` on the translation still to go (:639).
  - `hit.is_nonslip_slope && slipping && !slipping_intent` returns `horizontal_tangent + normal_part` (:649-651). Here that is 0 + 0, since `normal_part` is 0 for a translation going into the surface.
  - Then `+ normal1 * normal_nudge_factor` (:658).
- **The discriminating value.** `vertical_tangent.y = rem.y − (rem.y·n.y)·n.y`, which is 0 for n.y = 1 but −2⁻⁶¹ for n.y = 1 − 2⁻⁵³ with rem.y near −2⁻⁹.

### 2.2 A stalled quantum and its neighbours [MEASURED]

Taken from `out/origin.tsv` and `out/far.tsv`. The desired translation is (6.25e-3, −1.953125e-3, 0) on every row.

| quantum | first hit: TOI (path) | `normal1` | horizontal-tangent direction | tangent y | branch | travel kept |
|---|---|---|---|---|---|---|
| origin q96 | 3.3526109e-4 (GJK) | (−8.88e-12, 1, −3.24e-10) | (0.9996, 0, −0.0274) | 5.27e-14 | slide (:652) | 6.2499999999819e-3 |
| origin q97 | 5.7716e-10 (fallback) | (−8.88e-14, 1, 2.22e-14) | (−0.243, 0, −0.970) | 5.55e-16 | slide | 6.249999999999645e-3 |
| **origin q98** | 3.352605505755515e-4 (GJK) | **(0, `3fefffffffffffff`, 0)** | **zero** | **−4.336808689942018e-19** | **non-slip (:649)** | **3.1999948e-4 (5.1%)** |
| origin q99 | 3.35258910847048e-4 (GJK) | (0, 1, −3.197e-10) | (1, −0, 0) | 0 | slide | 6.249999999999645e-3 |
| 1e6 q2 | 3.3525146e-4 (GJK) | (−0, `3fefffffffffffff`, −3.2196e-10) | defined | — | — | full |
| **1e6 q3** | 3.3526330489300996e-4 (GJK) | **(0, `3fefffffffffffff`, 0)** | **zero** | **−4.34e-19** | **non-slip** | **3.2000209e-4** |
| origin q3 | 3.352611446947345e-4 (GJK) | (0, `3fefffffffffffff`, −3.197e-10) | defined | −4.34e-19 | non-slip | 6.25e-3 (full: the x travel is the horizontal tangent) |
| origin q125 | 0 (fallback, `PenetratingOrWithinTargetDist`) | **(0, `3fefffffffffffff`, 0)** | zero | −4.34e-19 | non-slip | **0** |

**What the rows show.**
- y < 1 alone is harmless (1e6 q2, origin q3). An exactly vertical normal with y = 1 exactly is harmless too: 1,948 quanta at the origin and 3,379 at 1e6, where the tangent y comes out exactly 0.
- The stall needs both conditions at once.
- After the discarding branch the second iteration casts straight up, 1e-4, with no hit. The loop runs exactly 2 iterations on all 655 stalls.

**Across both runs:**
- every quantum is either full (at least 0.999 of the desired travel) or a stall (at most 5.12%);
- every stall has this normal and branch;
- every hit with this normal stalls.

**At the stall, nothing else fired.**
- `is_wall` was false on all 655 stalls, so autostep never ran.
- Snap ran on 183 and 144 of them and moves only y.
- 572 stalls came through the GJK path (TOI 3.35e-4, with the walker starting 1e-4 above its skin) and 83 through the contact fallback (TOI below 1e-4).

**Independent check (compile oracle).**
- **Program.** `$S/oracle_walker_stall.rs` is self-contained and links only `rapier3d_f64`. It builds the floor as `build_world` does, places the kinematic walker, and makes the `move_shape` call as `integrate()` does. It replays origin q98, origin q99, 1e6 q3 and origin q3 from their pose bits, then prints d·fl(1/d) for the q98 projection.
- **Result.** It returned `"ok": true` with the exact stdout (`$S/out/oracle-expected.txt`): the two stalls at `(0, 3fefffffffffffff, 0)` with "hdir none", tangent y −4.336808689942018e-19 and travel 3.2e-4; the two full quanta at 6.25e-3; `d * (1/d) = 3fefffffffffffff`.
- **What this confirms.** The oracle links a rapier built in debug, so this also confirms debug against release on the decisive quanta.

### 2.3 Where the exactly vertical normal comes from [MEASURED][SOURCE]

- **The two normalization sites.** Both paths normalize with glam's `normalize_and_length`, which returns `v * (1/length)` (glam 0.33.10 `dvec3.rs:698-706`):
  - the GJK ray cast normalizes `−proj` at parry3d-f64 0.30.2 `query/gjk/gjk.rs:743`, keeps it as the last lower-bound direction `ldir` (:789), and returns that `ldir` (:748 converged, :774 last chance; q98 and 1e6 q3 return at :774);
  - the small-TOI fallback (`shape_cast_support_map_support_map.rs:34-62`, used when TOI < 1e-4) takes its normal from `contact_support_map_support_map` → `gjk::closest_points` (`gjk.rs:397`).
- **Why y can drop.** For proj = (0, −d, 0), `|proj|` is exactly d, so y = d·fl(1/d). That is 1 or 1 − 2⁻⁵³, and never above 1: 0 of 6,000,000 random doubles went above, while 13.9-14.3% went below.
- **The trace at origin q98.** A diagnostic build with a vendored parry that adds read-only trace points reproduces both runs bit for bit (`$S/harness-gjk`, `$S/vendor/parry3d-f64-0.30.2`). It shows:
  - iteration 5: proj = (0, −1.0000250559923354e-4, 3.1974e-14) gives a z-tilted direction;
  - iteration 6: the projection onto the near-horizontal support triangle comes out exactly `(0, −8.9147424992747573e-10, 0)`, with d = `3e0ea17d8cc5b6f3` and fl(1/d) = `41d0b716abf55138`; the normalized direction is `(−0, 3fefffffffffffff, −0)`, which becomes the returned normal;
  - at q99, the last lower bound is iteration 5's z-tilted direction.
- **The same at 1e6 q3.** Iteration 6 gives exactly `(0, −8.9237859511313351e-10, 0)`. At origin q3 the cast ends after iteration 5.
- **What makes an exact zero.** The projection's x and z are sums like `a + ab·v + ac·w` over support points about 7 to 70 units out. Their rounding residue lands on exact 0 often: first-hit normals were exactly vertical on 2,280 of 9,997 quanta at the origin and 3,702 of 9,996 at 1e6.

### 2.4 Why about 1 in 30, and why it moves with the offset [MEASURED]

- **The rate.** P(exactly vertical) × P(y < 1 | vertical) = 0.228 × 0.146 at the origin and 0.370 × 0.087 at 1e6, about 3.3% in both. The mean gap is 30.1 and 31.0 quanta.
- **Random poses in the hover band.** On 20,000 random poses (feet 0 to 1.2e-4 above the skin), walking +x, −x, +z and −z:
  - origin: 662, 553, 664 and 642 stalls;
  - 1e6: 870, 799, 862 and 881 stalls.
  - The stall does not depend on direction.
- **One ulp switches it.** Perturbing the q98 pose by −40 to +40 ulps stalls 9 of 81 in x and 9 of 81 in y, in scattered clusters. q99's pose gives 0 and 6; 1e6 q3's gives 6 and 30. There is no height threshold, so "accumulated y drift crossing a target-distance comparison" is ruled out.
- **Why the stalled quanta differ between offsets.** At 1e6 each quantum's world-x add rounds to the 2⁻³³ grid:
  - 0.00625 is 53,687,091.2 units of 2⁻³³, so 2.33e-11 is lost per quantum (far dx = 6.249999976716936e-3);
  - the composed cast poses also round (character_controller.rs:355);
  - the walker's z stays exactly 1e6 at the offset, while it drifts to −7.1e-9 at the origin.
- **The first divergence.** Relative x differs from q1. At q3, GJK's input `pos12` is (−31.987500000046566, 0.76010000064457661, −2) at 1e6 against (−31.987500000000001, 0.76010000065564021, −2.000000000000032) at the origin. Only the 1e6 run takes the sixth iteration that yields the exact vertical.
- **Local-frame translation.** Rapier's own change of frame is exact here: `part_pose1.inv_mul(pose12)`, shape_cast_composite_shape_shape.rs:46, subtracts two numbers already on the same grid. The bits are lost in the world-space adds.

### 2.5 The named candidates

- **A spurious wall hit from the floor's top face at the offset.** Partly right: the hit is the floor's top face at the skin. But it is never a wall (angle 0), and it is not a TOI-0 effect as such, since 572 of the 655 stalls hit at TOI 3.35e-4. What decides is the last bit of the normal's y together with its exact-zero x and z. [MEASURED]
- **Snap-to-ground or autostep.** No. Autostep never runs, because `handle_stairs` returns at :737 on a non-wall. Snap runs on some stalls and not others, and it only moves y (:457-489). [MEASURED][SOURCE]
- **The normal nudge.** Not the cause; it is all that survives a stall.
  - It keeps the walker hovering 1e-4 above its skin, so most quanta start with a 3.35e-4 hit.
  - At 0 the loop hits TOI 0 twenty times and exhausts `max_iters` (:338, :346): 9,976 stalls, and the walker moves 0.15 in 10,000 quanta. [MEASURED]
- **Bits lost in the collider's frame at 1e6.** Not the cause, since the origin stalls at the same rate. It is why the stalled quanta differ. With the stalls removed it leaves 2.33e-7 of x difference after 10,000 quanta, within outcome 4's 1e-6. [MEASURED]

**A second, smaller bit-level effect.**
- The walker ends each quantum either at its skin (y 0.26) or 1e-4 above it. It ends above on 7,238 of 10,000 quanta at the origin and 7,249 at 1e6.
- Which one depends on bit-level outcomes at the skin boundary. At origin q96, for example, snap's `translation·up <= 0` test (:466) saw −1.22e-13.
- The two offsets disagree by 1e-4 in y on 4,063 quanta today, and on 3,996 to 4,556 under the single-call fixes below.
- A 1e-9 snap tolerance does not remove it (variant U7, 4,556 quanta). Only splitting the call does: 0 quanta differ by more than 1e-6.
- This is not lost travel, but it decides whether any stall fix makes outcome 4's walker agree at quantum 10000. [MEASURED]

## 3. Fixes tried

**How to read the table.**
- "Origin ≡ 1e6" is the walker's final relative difference at q10000 as outcome 4 measures it (tolerance 1e-6). The per-quantum y disagreement count is given where measured.
- "Course" is the native replica of `course.test.js`, which matches the node test exactly on the unmodified law.
- "4-dir step" is a 0.29 step approached in +x, −x, +z and −z, from 20 start offsets each (`stepscan`); the stall counts are for a 2000-quantum flat walk.
- What moves in the engine, for every row that changes code: the wasm digest (`fixtures/solver.sha256`); the product golden (`fixtures/golden.txt`); in `fixtures/golden-behaviour.json`, the walker and parcel finals (70.5255 becomes about 72.5 when stalls are gone) and `snapshotDigest.last`.
- The five untouched bodies stay bit-identical at every quantum under the engine, S12, S13, S15, U2, U3 and U4, at both offsets (hash over their per-quantum records), so their finals and every sleep quantum stay.
- Outcome 4 is red or green as written at 48890ef.

| # | fix | stalls origin | stalls 1e6 | origin ≡ 1e6 (walker) | course (pin 5), other checks | outcome 4 |
|---|---|---|---|---|---|---|
| 0 | engine (48890ef) | 332 | 323 | 3.83e-2 in x; y differs on 4,063 quanta | green; 4-dir step 20/20 each; flat walk stalls 77-90 per 2000 | green |
| S1 | offset 0.005 | 294 | 330 | 2.32e-1 | 7 red (5.1, 5.2, 5.5-5.9); the course's feet use SKIN 0.01 | green |
| S2 | offset 0.02 | 313 | 446 | 8.15e-1 | 7 red | green |
| S3 | nudge 0 | 9,976 | 9,969 | 4.37e-2 | 7 red; `max_iters` lock | green |
| S4 | nudge 1e-5 | 9,810 | 9,916 | 6.63e-1 | 5 red | green |
| S5 | nudge 1e-3 | 10 | 63 | 2.52e-1 | 5.4 red (46° gains 0.331) | green |
| S6 | snap off | 374 | 419 | 2.67e-1 | 5.5 red | green |
| S7 | snap 0.1 | 332 | 323 | 3.83e-2 | 5.5 red | green |
| S8 | autostep off | 332 | 323 | 3.83e-2 | 5.1 red | green |
| S9 | slide off | 10,000 | 10,000 | 2.6e-11 (never moves) | 7 red | red |
| S10 | climb angle 40° | 332 | 323 | 3.83e-2 | 5.3 red | green |
| S11 | `min_slope_slide_angle` 0 | 332 | 323 | 3.83e-2 | 5.1 red (0 ≤ 0 is still non-slip) | green |
| S12 | `min_slope_slide_angle` −1° | 0 | 0 | 1.00e-4 in y | 5.1 red; the 0.29 step refused in all 4 directions; non-slip off on every slope | green |
| S13 | `up` = (0, 1, 1e-6) | 0 | 0 | 4.28e-7 | green; +z step 0/20 | red |
| S14 | `up` = normalize(1e-6, 1, 1e-6) | 0 | 0 | 2.36e-7 | 5.1 red; 8 u/s walkers pass through | red |
| **S15** | **`up` = (0, 1, 1e-12)** | **0** | **0** | 2.34e-7; y differs on 3,996 quanta | **green; 4-dir step 20/20 each; flat walk 0 stalls; step limit unchanged; drop outcome moves (below)** | **red** |
| U1 | no gravity in the move while `b[4] == 0` | 0 | 0 | 1.00e-4 in y | 5.4 red (0.064), 5.7 and 5.8 red (never rises) | green |
| U2 | two calls: horizontal, then vertical | 0 | 0 | 2.33e-7; y 0 quanta over 1e-6 | 5.9 red (closest 0.4687); step 20/20 each | red |
| U3 | two calls: vertical, then horizontal | 0 | 0 | 2.33e-7; y 0 quanta over 1e-6 | 5.9 red (0.4650); dirs 4/4 | red |
| **U4** | **engine-owned `move_shape` copy with the `decompose_hit` branch** | **0** | **0** | 2.34e-7 in x, but 1.00e-4 in y at q10000; y differs on 4,142 quanta | **green; step 20/20 each; flat 0; step and drop limits identical to the engine** | green (walker and parcel still listed, now for 1e-4 in y) |
| U5 | walker's y re-anchored to a 2⁻¹⁶ grid | 205 | 197 | 4.74e-2 | green | green |
| U6 | control: the copy unpatched | 332 | 323 | 3.83e-2 (identical) | identical to the engine | green |
| U7 | U4 plus snap when the rise is ≤ 1e-9 | 0 | 0 | 2.33e-7 at q10000, but y differs on 4,556 quanta | green; 20/20 each; drop snaps through 0.211 | red (at q10000 only by luck) |

**Row notes.**
- "7 red" in S1-S4 and S9 lists the failing cases: S2 is 5.1-5.3 and 5.5-5.8; S3 and S9 are 5.1-5.3 and 5.5-5.8; S4 is 5.1-5.3, 5.7 and 5.8.
- S12's failure is on stepping, in every direction (`dirs`). U1's failure at 5.7 and 5.8 is expected: with no vertical input, the fallback's `normal_vel >= 0` test lets a walker inside the floor slide horizontally, and nothing registers the hit that carries the nudge.

**The settings-level fix, S15.** The `up` tilt breaks the exact `normal1 ∥ up` degeneracy.
- The x travel becomes the horizontal tangent. The z travel is judged by `up·v_z·ε`, whose sign `slipping` and `slipping_intent` share.
- The measured window at 0.4 u/s:
  - ε = 1e-17: the residue wins, and +z stalls on 664 of 20,000 poses;
  - 1e-16, 1e-14, 1e-12 and 1e-10: 0 stalls and 20/20 steps in every direction;
  - 1e-8 and 1e-7: the +z step is refused from 20 of 20 phases.
- Why the edges are there [REASONED from the measured edges and :772-788]:
  - The lower edge is where ε·|v_h·DT| no longer dominates the residue, about |v_y·DT|·2⁻⁵². It rises on a landing quantum (larger v_y) and for slow walks.
  - The upper edge is where `handle_stairs`' upward cast, travelling along the tilted `up` for 0.31, closes the small gap the riser hit left. Any riser facing against the tilt would also be refused if a hit ever left the walker inside the target distance, since the fallback then counts `n·up = −ε < 0` as a hit.
- ε = 1e-12 has three to four decades to each measured edge. `Vector::new(0.0, 1.0, 1.0e-12)` is exactly what was measured, because `normalize` leaves it unchanged.

**The usage-level fix, U4.** The engine keeps its own copy of the controller (`$S/harness/src/kcc.rs`, about 500 lines, rapier's public API only). Unpatched (U6), it reproduces the engine to the bit. The one change, in `decompose_hit`:

```rust
let horizontal_tangent_dir = hit.normal1.cross(self.up).try_normalize().unwrap_or_default();
let (horizontal_tangent, vertical_tangent) = if horizontal_tangent_dir == Vector::ZERO {
    // normal1 parallel to up: no slope direction, so every tangential motion is horizontal
    let vt = self.up * self.up.dot(tangent);
    (tangent - vt, vt)
} else {
    let ht = tangent.dot(horizontal_tangent_dir) * horizontal_tangent_dir;
    (ht, tangent - ht)
};
```

What U4 does and does not change [MEASURED]:
- It changes nothing where the direction exists. The walker's path is identical to the engine's through q97 at the origin and q2 at 1e6.
- It removes all stalls with no window.
- The step limit is unchanged (climbs 0.31, stops at 0.3101). So is the drop outcome: 0.200 snaps and falls from 0.205, as today in the course's geometry.
- This is not fixed upstream: `handle_slopes` through `compute_dims` is byte-identical at rapier v0.36.0, which is master `b716d375` as of 2026-09-25 (`gh api`). [MEASURED]
- The cost is ownership: the copy must be re-synced on every rapier bump.

**Neither fix makes the walker agree between offsets at every quantum.** The 1e-4 hover phase still disagrees on about 40% of quanta. The split calls (U2, U3) are the only variants that make y offset-stable, but they change walker-against-walker contact (the platform-velocity transfer at :545-584 runs in both calls), and 5.9 goes below 0.49.

**Soundness.** Every row is a pure function of the record: the pose and `b[3..5]`. None adds history, and all are deterministic under replay. The copy is the same code as rapier's.

## 4. Caveats and what was not measured

- **Scene coverage.** A box walker (shape 0) on flat cuboid floors, at 0.4 u/s. Not covered:
  - diagonal walking;
  - the capsule (shape 1), whose rounded bottom may never produce an exactly vertical normal;
  - walking on the heightfield;
  - riding a T3 platform;
  - speeds other than 0.4 (1 and 8 u/s appear only in 5.9 and 5.10).
- **The exact-zero frequency is measured, not derived.** Its structure (a near-horizontal support triangle whose projection residue lands on 0) is shown at two traced quanta only. The fallback path's normal (gjk.rs:397) was not traced; its values are measured.
- **Tilt window.** The edges are empirical for this speed, gravity step, offset, 0.31 autostep height and the 20-phase approach. The reasons are [REASONED]. Any bump of rapier or parry could move the upper edge.
- **Drop threshold.** Between 0.200 and 0.2105 the outcome is bit-sensitive, like the stall.
  - With the course's geometry (upper floor to x 12, walker from 11.5), today's law falls from 0.205 by 5.5's criterion. With the tilt it snaps through 0.21.
  - The lane recipe's own geometry (upper floor x 0 to 11, walker from 10.5) snaps 0.21, so the recipe's "0.2105" holds for that geometry, not generally.
  - The course pair, 0.19 snapped and 0.22 fallen, holds under every fix measured.
- **A different glitch.** On 3 quanta at the origin (2182, 7058, 8233) and 4 at 1e6, the first diagonal cast misses the floor. The walker keeps full travel but sinks 1.95e-3 into its skin. Not investigated.
- **Walker against walker.** Contact in 5.9 and 5.10 is itself bit-sensitive. The closest approach moves under every change (0.494 to 0.508 at 1 u/s; at 8 u/s, 0.387 today against 0.5 with S15 or U4).
- **Platforms.** Only x86_64 native and wasm32 under V8. ARM was not tested.
- **Timing.** Not measured. U2 and U3 make two controller calls per walker per quantum.
- **Harness state.** The harness globals (`probe::CFG`, `kcc::PATCH`) are module statics, run single-threaded.

## Commands

`S` as above. All builds use `cargo +1.98.1`. Rows marked with a plain `walker.exe` or `probe_state.exe` are run from `$S/harness`.

```
cargo +1.98.1 --version; rustc +1.98.1 --version; node --version
# engine at 48890ef, LF, scratch only
git clone https://github.com/mcp-tool-shop-org/si-rpg-engine.git $S/engine-src && cd $S/engine-src && git fetch origin pull/56/head \
  && git config --local core.autocrlf false && git rm --cached -r -q . && git reset --hard 48890ef9b3742bd1a7bc7ffbe40628fc477a5cbe
cd $S/engine-src/solver && node build.mjs                                   # wasm, digest b9724fba… on this host
# native harness (solver/Cargo.lock)
cd $S/harness && cargo +1.98.1 build --release --locked
./target/release/walker.exe run 0 0 10000 ../out/origin.tsv --trace        # 332 stalls
./target/release/walker.exe run 1e6 1e6 10000 ../out/far.tsv --trace       # 323 stalls
python $S/classify.py $S/out/origin.tsv $S/out/far.tsv; python $S/stallbits.py $S/out/origin.tsv $S/out/far.tsv
# port == engine
node $S/node/drive_product.mjs $S/engine-src 0 0 10000 $S/out/wasm-origin.tsv; node $S/node/drive_product.mjs $S/engine-src 1e6 1e6 10000 $S/out/wasm-far.tsv
#   compare harness TSV cols 1-4 and 7 with wasm TSV cols 1-5: 0 differing quanta
cd $S/engine-src && node --test --test-reporter=tap harness/course.test.js
cd $S/engine-src && node --test --test-reporter=tap --test-name-pattern="outcome 4" harness/outcome.test.js
# floor-only replay, sensitivity, scans (release and target/debug)
./target/release/probe_state.exe replay 0 0 ../out/origin.tsv; ./target/release/probe_state.exe replay 1e6 1e6 ../out/far.tsv
./target/release/probe_state.exe ulps 0 0 4025366666666671 3fd0a57a783cd042 bdc150395781bb4b 40
./target/release/probe_state.exe scan 0 0 20000 7 [--up 0,1,E | --slide-deg -1 | --nudge 1e-3 | --patch]   # and 1e6 1e6
# GJK trace (vendored parry, read-only trace points)
cd $S/harness-gjk && cargo +1.98.1 build --release && GJK_Q=98,99 ./target/release/walker.exe run 0 0 100 ../out/tmp.tsv --trace | python $S/gjkview.py
python -c "import random,math; ..."                                          # d*fl(1/d) rate, 2,000,000 samples per range
# fixes: F = [] | --offset x | --nudge x | --snap none|x | --autostep 0 | --slide 0 | --climb-deg d | --slide-deg d | --up x,y,z | --usage 1..7
./target/release/walker.exe outcome4 10000 F; ./target/release/walker.exe course F; ./target/release/walker.exe dirs F
./target/release/walker.exe stepscan F; ./target/release/walker.exe limits F
OTHERS=1 ./target/release/walker.exe run 0 0 10000 ../out/tmp.tsv F 2> ../out/others.txt   # untouched bodies, per quantum
# upstream
gh api -H "Accept: application/vnd.github.raw" "repos/dimforge/rapier/contents/src/control/character_controller.rs?ref=v0.36.0"   # and ref=master
# oracle (run from E:/AI/readouts/rust-knowledge)
python scripts/compile_oracle.py file $S/oracle_walker_stall.rs --expect runs --edition 2021 --deps rapier3d_f64 --stdout "$(cat $S/out/oracle-expected.txt)"
```

Pin check: consistent with T4 pin 4 of `docs/dispatch-t4-outcome-tests.md` as landed at 48890ef (`harness/outcome.test.js`:255-337). The walker divergence is the lost travel its comment describes (23 stalls in the first 640 quanta at the origin, first at q3 at 1e6, final x off by 3.83e-2). It is offset-moved, not offset-caused.

What each fix would turn red:
- **S15 (tilt), U2, U3 and U7:** walker and parcel leave `FINAL_DIVERGES` (they agree within 2.34e-7), so outcome 4's `deepEqual` fails and `write-golden` refuses until the list changes (pin 6). U2 and U3 also turn course 5.9 red.
- **U4:** outcome 4 stays green at q10000, but only because the 1e-4 hover phase happens to disagree there. The listed cause (0.038 in x) becomes wrong, and the verdict becomes a coin flip under any later change.
- **Every fix:** `fixtures/solver.sha256`, `golden.txt`, and the walker, parcel and `snapshotDigest.last` entries of `golden-behaviour.json` all move.
