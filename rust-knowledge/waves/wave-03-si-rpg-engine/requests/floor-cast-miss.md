Floor-cast miss: why the character's first downward cast sometimes finds no floor. si-rpg-engine main `93a2d1e` (F2's law), rapier3d-f64 0.35.3 with `enhanced-determinism`, parry3d-f64 0.30.2. This is the second question of the squeeze-launch request (`squeeze-launch.md`). Measured 2026-09-26.

**Host and tools.** As `squeeze-launch.md`: Windows 11 Pro, x86_64; rustc and cargo 1.98.1; node v22.22.3. The engine is cloned from GitHub into scratch; nothing in `E:/AI/si-rpg-engine` was touched.

**Scratch.** `$S = <scratchpad>/squeeze-launch`.
- `flatwalk.mjs` is outcome 4b's flat walk as `harness/outcome.test.js` builds it at `93a2d1e`: the product walker alone on the product floor, driven at 0.4 units/s for 10,000 quanta, at the origin or at (1e6, 0, 1e6). It records the law's calls with `recorder.mjs`.
- `harness-f2g/` is the native replay harness built from `93a2d1e`'s `solver/src`, with parry 0.30.2 patched to a scratch copy. That copy is the walker-stall answer's vendored parry, whose `minkowski_ray_cast` pushes trace lines when asked. `trace_gjk_exits.py` added a trace line and a counter at each of its untraced exits. With tracing off the copy computes what parry computes: every replay below matches the wasm bit for bit.
- `hook_first_cast.py` wraps `move_shape`'s first cast in `kcc.rs`. It records which `minkowski_ray_cast` exit that cast took, and on traced quanta prints the cast's inputs as bits and parry's GJK iterations.
- `patch_kcc_retry.py` puts the candidate fix of section 4 into a scratch checkout's `kcc.rs`.

## Answer

1. **Why the cast misses.** It is neither a time-of-impact tolerance nor the skin distance as such. Parry's GJK ray cast loses its search direction to rounding when the cast starts on the skin boundary.
   - The first cast asks for the character's box, dilated by the 0.01 skin (`target_distance`), cast along the quantum's move. That move is (0.00625, −0.001953125, 0).
   - On all 15 missed quanta the walker starts with its dilated bottom on the floor's top face to within rounding: y is between 0.26 − 2.44e-15 and 0.26 exactly. So the ray starts on the surface of the shapes' Minkowski difference.
   - GJK's projected distance falls to the rounding floor of that difference, about 2.5e-15. That is just above its absolute tolerance, `eps_tol` = 10·ε = 2.2e-15. The floor is 76 units long, so the difference has support coordinates near 56.
   - Past that point the normalised projection is rounding noise. Parry takes it as the search direction. When it points along the cast (dot 0.014 to 0.732 on the 15 misses), the half-space clip declares a miss. The cast returns nothing, and the character takes its whole move, gravity step included. [MEASURED][SOURCE]
2. **Rapier's own controller does the same.** The first cast is identical in `kcc.rs` and in rapier's `move_shape`, since F2 changes only `decompose_hit`. The code that misses is parry's. parry 0.31.1, which a bump to rapier 0.36.0 would bring, has a byte-identical `gjk.rs`. [SOURCE]
3. **Benign, with limits.** A miss sinks the walker one gravity step, 1.953125e-3, into its 0.01 skin. It keeps its full stride and stays grounded (outcome 4b is green), and climbs back at the 1e-4 nudge over 20 quanta.
   - A miss cannot repeat during that climb: the next casts start 1.9e-3 inside the skin and take GJK's "inside" exit.
   - It happens 8 times in 10,000 quanta at the origin and 7 at 1e6. The product scene has the same 8, on the same quanta.
   - It has been measured only on flat cuboid floors. [MEASURED]
4. **A sound fix in the copy exists, and it costs the product golden.**
   - The fix: when the first cast finds nothing while the character was grounded at the start, cast once more with the skin 1e-9 larger. The start is then clearly inside the dilated shape, and parry's contact fallback answers.
   - Measured in F2's wasm law: 0 sunk quanta and 0 short strides at both offsets.
   - The suite passes 238 of 244. The course, the outcome tests and every fixture replay stay green.
   - It moves the product golden from `6e0d351693b18c93` to `69a671f962665563`. It also moves the product scene's recorded behaviour and snapshot digests (6 tests), all of which need recapturing.
   - The retry runs only on a first cast that found nothing while grounded. In a motion that moves away from the ground, parry's own fallback still returns nothing. [MEASURED]

## 1. Reproduction [MEASURED]

`flatwalk.mjs` under F2 (`93a2d1e`) reproduces PHASE-2.md's list exactly:
- at the origin, the walker sinks more than 1e-3 at 2242, 4385, 4890, 5276, 5820, 6709, 6887 and 7197;
- at (1e6, 0, 1e6), at 1532, 2252, 4653, 5272, 5350, 6392 and 7445.

Each event puts y at 0.258046875 (0.26 − 1.953125e-3), then 0.2581468…, climbing 1e-4 a quantum. Short strides: 0 at both offsets.

Replayed natively with the traced parry, both walks match the wasm bit for bit. On exactly those 15 quanta, `move_shape`'s first cast returns `None`.

## 2. The mechanism

### 2.1 The path [SOURCE]

1. `kcc.rs:268` (`93a2d1e`) makes the first cast: `queries.cast_shape(pos, translation_dir, character_shape, ShapeCastOptions { target_distance: offset /* 0.01 */, stop_at_penetration: false, max_time_of_impact: translation_dist, compute_impact_geometry_on_penetration: true })`.
2. For two cuboids that reaches parry's `cast_shapes_support_map_support_map` (`query/shape_cast/shape_cast_support_map_support_map.rs:21-29`). That wraps the character in a `RoundShapeRef` of radius `target_distance`, then calls `gjk::directional_distance`.
3. The time-of-impact fallback there (`:34-50`) handles an impact below 1e-4: it re-derives the normal from a contact query and drops the hit if the motion leaves the contact. It needs a time of impact, and on these quanta GJK never returns one.
4. `gjk::directional_distance` (`query/gjk/gjk.rs:673`) is a ray cast from the origin along the motion, `minkowski_ray_cast` (`:701`), on the Minkowski difference of the dilated character and the floor.

### 2.2 Inside `minkowski_ray_cast` at quantum 2242 [MEASURED]

The walker starts at y = 0.25999999999999940, bits `3fd0a3d70a3d7099`. The cast direction is (0.954479978035029708, −0.298274993135946798, 0) over 6.548e-3. The GJK iterations:

| Iteration | Projected distance | Search direction (normalised −projection) |
|---|---|---|
| 0 to 6 | 20.4 → 2.5e-9 | converging on the floor normal |
| 7 | 2.5e-9 | (−7.0e-7, 1.0, −8.8e-8): the floor normal |
| 8 | 2.52e-15 | (0.705, 0.687, 0.176): noise |
| 9 | 2.71e-15 | (0.755, 0.639, 0.144): noise |

The ray origin never moves: no lower bound was ever found, because the ray starts on the surface. At iteration 9, `ray_toi_with_halfspace(support, dir, ray)` (`:785`) finds no crossing. `dir · ray_dir` is 0.530, above `eps_tol`, so the loop takes the miss branch (`:807-809`) and returns `None`.

**Why the distance stops at about 2.5e-15.**
- The difference's support points carry coordinates such as −20.26 and 56.25, set by the floor's 76 × 1 × 8 extent. A double near 56 has an ulp of 7.1e-15, so projections of such points are good to about 1e-14.
- `eps_tol()` (`:141`) is an absolute 10·ε = 2.2e-15. So the convergence test `dist > _eps_tol` (`:744`) can be passed or missed by rounding alone.
- Parry scales the tolerance for its dimension-3 inside test (`:842`, `_eps_tol * scale.max(1.0)`), but not for the convergence test or the half-space miss test. [SOURCE][REASONED]
- The same holds at 1e6. The cast works in the character's frame (pos12), so the magnitudes are the floor's size relative to the walker, not the world offset. That fits the near-equal rates of 8 and 7.

### 2.3 All 15 misses [MEASURED]

| Walk | Quantum | y − 0.26 | GJK iterations | dir · ray at the miss |
|---|---|---|---|---|
| origin | 2242 | −6.11e-16 | 10 | 0.530 |
| origin | 4385 | −6.66e-16 | 13 | 0.732 |
| origin | 4890 | 0 | 10 | 0.221 |
| origin | 5276 | −1.67e-16 | 10 | 0.0137 |
| origin | 5820 | −6.11e-16 | 11 | 0.113 |
| origin | 6709 | −3.89e-16 | 10 | 0.238 |
| origin | 6887 | −5.55e-17 | 11 | 0.412 |
| origin | 7197 | −7.77e-16 | 10 | 0.366 |
| 1e6 | 1532 | −5.55e-17 | 10 | 0.211 |
| 1e6 | 2252 | −2.44e-15 | 10 | 0.106 |
| 1e6 | 4653 | 0 | 11 | 0.107 |
| 1e6 | 5272 | −2.78e-16 | 10 | 0.145 |
| 1e6 | 5350 | −6.66e-16 | 11 | 0.228 |
| 1e6 | 6392 | −1.67e-16 | 10 | 0.355 |
| 1e6 | 7445 | −3.33e-16 | 10 | 0.450 |

Every miss starts on the boundary to within 2.5e-15 and leaves by the half-space miss. A boundary start is necessary, not sufficient. At the origin, 1,041 first casts start within 2.5e-15 of y = 0.26: 1,033 hit and 8 miss, 0.77%. At 1e6 it is 1,056 starts and 7 misses, 0.66%. Whether a boundary start misses turns on whether rounding lets the distance reach `eps_tol`, and where the noise direction then points.

### 2.4 How the first cast ends, over whole runs [MEASURED]

These are `minkowski_ray_cast` exits of `move_shape`'s first cast, counted in the native replay.

| Run | Quanta | Converged | Last chance with a lower bound | Inside (dim 3) | Half-space miss | Other exits |
|---|---|---|---|---|---|---|
| flat walk, origin | 10,000 | 806 | 7,666 | 1,520 | **8** | 0 |
| flat walk, 1e6 | 10,000 | 802 | 7,708 | 1,483 | **7** | 0 |
| product scene (`sim.mjs`) | 10,000 | 806 | 7,666 | 1,520 | **8**, the same quanta | 0 |
| `course.test.js` | 9,044 | 393 | 4,741 | 5,226 | **8** | 0 |
| `outcome.test.js` | 82,752 | 11,944 | 57,198 | 9,392 | **33** | 0 |

In the course and outcome runs, `None` first casts outnumber these misses: 18 and 105. The rest are casts with nothing in reach, such as a walker in the air, and those are correct.

## 3. Is it benign? [MEASURED][REASONED]

- **Bounded.** One miss applies one gravity step, 1.953125e-3, into a 0.01 skin, so the feet stay 8.05e-3 above the floor. The next casts start 1.95e-3 inside the skin and leave by "inside", which cannot miss, so the drop does not compound. The walker climbs back by the controller's 1e-4 nudge over 20 quanta.
- **No lost travel, no lost ground.** Outcome 4b checks every quantum at both offsets: short strides 0, airborne 0.
- **Deterministic.** It happens on the same quanta in wasm and native builds, as every replay here shows.
- **Not measured:** slopes, steps, heightfields, the capsule character, other speeds. A miss on a step's edge still applies only one gravity step, and I would expect it to be as harmless there, but I have not measured it.

## 4. Fixes [MEASURED]

| Fix | Flat walk, origin: sunk quanta / short | Flat walk, 1e6 | Product golden | Suite at F2 (244) | Digest on this host |
|---|---|---|---|---|---|
| none (`93a2d1e` + T6 margin) | 80 (8 events) / 0 | 70 (7) / 0 | `6e0d351693b18c93` | 244/244 | `d1c29dd9…` |
| retry with the skin 1e-9 larger when the first cast finds nothing while grounded (`patch_kcc_retry.py`) | 0 / 0 | 0 / 0 | `69a671f962665563` | 238/244 | `d03b81b1…` |

The retry's six failures are the product scene's record, each correctly detecting that the scene moved on the quanta that no longer sink:
- 15, "the recorded behaviour passes the check";
- 16, 17 and 21, checks that perturb that record;
- 19, "the snapshot digests are recorded at load and at the last quantum";
- 113, "two traces of one run are byte-identical, and the last quantum is the golden".

Recapturing `fixtures/golden.txt` and `fixtures/golden-behaviour.json` clears them. The course, the outcome tests, the fixture replays and the restore tests stay green.

**Why 1e-9.** It is about 1e5 times the rounding floor, so the retry starts clearly inside the dilated shape. It is also far below anything the controller resolves: the nudge is 1e-4 and the skin 1e-2.

Parry's own fallback (`shape_cast_support_map_support_map.rs:34-50`) then derives the normal from a contact query and returns the hit only if the motion approaches. So the retry cannot invent a hit for a character that is moving off the ground.

**What the retry leaves alone.**
- It runs only on the first cast, only when it found nothing, and only when grounded at the start. In the native replay of the two walks it ran on 8 quanta, and found the floor every time.
- Later casts in the same `move_shape` loop could in principle start on a boundary too. None of those missed in any run counted here.

**Other routes.**
- Accept it as benign, as PHASE-2.md records it now.
- Fix it upstream by scaling parry's tolerances, as the dimension-3 test already does. It was reported on 2026-09-26 as dimforge/parry#452.
  - The report carries a standalone repro on parry3d-f64 0.31.1.
  - It also carries a floor-size sweep. The rate is not monotonic in size: 0 at half-extents 0.5, 2, 38 and 200; 0.023% at 8; 30.5% at 1000.
  - Every miss leaves through the half-space exit.
  - The proposed fix scales the convergence test at `:744` only. The half-space test at `:807` compares a cosine, so scaling it by a length would mean nothing.
- The bump to rapier 0.36.0 does not change it: `gjk.rs` is identical in parry 0.31.1, and the bumped law keeps the golden, misses included.

## 5. Caveats

- The magnitude explanation (section 2.2) is reasoned from the ulp of the support coordinates and the absolute tolerance. I did not vary the floor's size in the walk, because the walk needs a floor longer than 62.5 units.
  - Later (2026-09-26) a standalone repro varied it (parry3d-f64 0.31.1, 180,000 boundary starts per slab). The rate is not monotonic in size: 0 misses at half-extents 0.5, 2, 38 and 200; 0.023% at 8; 30.5% at 1000.
  - So the support magnitude sets how coarse the rounding floor is. Whether the distance stalls just above `eps_tol`, with the noise pointing forward, also depends on the geometry.
  - Every miss in those sweeps (55,551) leaves through the half-space exit.
- Only the box character on flat cuboid floors, at 0.4 units/s.
- The retry was measured in F2's law only, not on top of F3.
- This is the glitch `walker-stall.md` §4 recorded as "not investigated". At `48890ef` it came at 2182, 7058 and 8233 at the origin.

## Commands

```
cd $S/engine-f2s    # 93a2d1e + `git cherry-pick -n 6e41ccd`, patch_glue.mjs applied
SOLVER_LOG=$S/out/flat0.calls.bin node --import file:///$S/recorder.mjs $S/flatwalk.mjs 0
SOLVER_LOG=$S/out/flat1e6.calls.bin node --import file:///$S/recorder.mjs $S/flatwalk.mjs 1000000
python $S/trace_gjk_exits.py $S/vendor/parry3d-f64-0.30.2/src/query/gjk/gjk.rs
python $S/make_harness.py $S/engine-f2s/solver $S/harness-f2g   # then add [patch.crates-io] parry3d-f64 = { path = "../vendor/parry3d-f64-0.30.2" }
python $S/hook_first_cast.py $S/harness-f2g/src/kcc.rs && cd $S/harness-f2g && cargo +1.98.1 build --release
./target/release/replay.exe $S/out/flat0.calls.bin [--trace 2242,2242] [--sunk] [--variant retry-inflated --no-check]
python $S/patch_kcc_retry.py <engine-dir> && node solver/build.mjs && node $S/flatwalk.mjs 0 && node harness/sim.mjs && npm test
diff <parry3d-f64-0.30.2>/src/query/gjk/gjk.rs <parry3d-f64-0.31.1>/src/query/gjk/gjk.rs    # identical
```
