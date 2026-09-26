Floor-cast retry (for F4): the candidate fix from `floor-cast-miss.md`, re-measured on si-rpg-engine main `29e1c52`, where F3 has merged (#1004's backport, in `solver/src/impulses.rs`). rustc and cargo 1.98.1 pinned, rapier3d-f64 0.35.3 with `enhanced-determinism`, parry3d-f64 0.30.2. Measured 2026-09-26.

**Host and tools.** Windows 11 Pro, x86_64, node v22.22.3.

**Engine state.**
- The engine was cloned from GitHub into scratch; `E:/AI/si-rpg-engine` was not touched.
- `solver/src/kcc.rs` is byte-identical at F2 (`93a2d1e`) and at `29e1c52`, so `floor-cast-miss.md`'s retry patch applies unchanged.
- The host digests: `29e1c52` builds to `b1edc05c…`, the same as F3's head; with the retry it builds to `892cd744…`.
- `29e1c52` passes its JS suite 356 of 356.

**Scratch.** `<scratchpad>/f4`:
- `base/` is `29e1c52` as it is, and `retry/` is `29e1c52` with the retry (`patch_kcc_retry.py`).
- `count/` is the retry plus counters that only read (`patch_count.py`).
  - They count the retries fired and the retries that hit.
  - For a retry that hit, parry's distance query measures the start pose's distance to the collider it hit, against the skin.
  - A scratch-only export, `f4_counts`, reads them.
- `countf5/` is `count/` plus push-mass's effective-mass push (F5).
- The scripts:
  - `f4hooks.mjs`, a preload that records, per test, the quanta on which the retry fires;
  - `f4summary.py`;
  - `f4fixtures.mjs`, which runs every fixture run and push fixture closed loop;
  - `planted.mjs`, `planted2.mjs` and `plantsweep.mjs`;
  - `flatwalk.mjs`, from `floor-cast-miss.md`.

## Answer

1. **The flat walk.** [MEASURED]

   | Build | Origin: sunk quanta (events), short strides | (1e6, 0, 1e6): sunk quanta (events), short strides |
   |---|---|---|
   | `29e1c52` | 80 (8), 0 | 70 (7), 0 |
   | `29e1c52` with the retry | 0, 0 | 0, 0 |

   - F3 did not change the misses. The 8 events at the origin (2242, 4385, 4890, 5276, 5820, 6709, 6887, 7197) and the 7 at 1e6 (1532, 2252, 4653, 5272, 5350, 6392, 7445) are F2's, on the same quanta. The flat walk pushes nothing.
2. **What moves with the retry.** [MEASURED]
   - **The product golden** moves from `6e0d351693b18c93` to `69a671f962665563`, as it did on F2's law. With F5's push on as well, it is still `69a671f962665563`.
   - **The JS suite:** 349 of 356 pass. The 7 that fail are all the product scene's record:
     - 15, "the recorded behaviour passes the check", and 16, 17 and 21, which perturb that record;
     - 19, "the snapshot digests are recorded at load and at the last quantum";
     - 168, "two traces of one run are byte-identical, and the last quantum is the golden";
     - 47, the law-run file check.
   - **Fixture replays:** all 16 fixture runs are identical at every tick. The retry fires in 9 of them but never hits (question 3).
   - **The law runs:** `node harness/law-runs.mjs --check` gives 17 ok and 1 stale, `product-scene`.
   - **The sweep's record:** `node harness/corpus.mjs --record-sweep` writes 25 worlds with 0 moved, on `29e1c52` and with the retry.
     - On both, `fixtures/sweep/verdicts.json` is byte-identical to the committed file, so no verdict moves.
     - The two records took 7.8 and 6.7 minutes.
3. **Where else the retry fires.** [MEASURED] Closed loop, counted around every quantum:

   | Run | Quanta | Retry fired (quanta) | Of them, hit |
   |---|---|---|---|
   | course 5.5, a 0.19 drop | 240 | 1 (122) | 0 |
   | course 5.6, a 0.22 drop | 240 | 3 (122, 123, 136) | 0 |
   | course 5.9, two walkers at 1 u/s | 192 | 2 (77, 103) | 2 |
   | course 5.10, two walkers at 8 u/s | 192 | 1 (110) | 1 |
   | outcome 4, the product scene at the origin and at 1e6 | 20,000 | 8 (origin 2242; 1e6 1532, 2252, 4653, 5272, 5350, 6392, 7445) | 8 |
   | outcome 4b, the flat walks | 20,000 | 8, the same quanta | 8 |
   | outcome 4c, the 0.29 step from 80 starts | 38,400 | 22 | 3 |
   | shape-traversal step-capsule | 80 | 19 | 0 |
   | shape-traversal ledge-capsule | 80 | 11 | 0 |
   | behavior-verbs carry-capsule | 261 | 6 (155 to 160) | 0 |
   | shape-traversal gap-capsule | 80 | 5 | 0 |
   | shape-traversal step-box | 80 | 2 | 0 |
   | rotation-tumble, ledge-box, gap-box, verbs-climb | 90, 80, 80, 171 | 1 each | 0 |

   - **Everywhere else it never fires.** That covers course 5.1 to 5.4, 5.7 and 5.8 (the 0.29 and 0.33 steps, the 44° and 46° slopes, the two sunk starts), outcome 2 (the fast box), outcome 3a and 3b (the heightfield seams: 24 worlds, 3,456 quanta), and the other fixture runs, including red room A and the minds fixture.
   - **It hits 22 times, and every one is a boundary start.** At each hit, the start's distance to the collider it hit equals the skin within 2.4e-15 (within 3.2e-16 in the course). No hit started off the boundary.
   - **The other 71 firings change nothing.** The retry finds nothing either, so it costs one more cast. These are grounded starts whose first cast finds nothing in the path, which is exactly the retry's condition.
   - **The retry changes the origin walk's later misses.** With the retry, the origin walk misses once, at 2242. After that the walker never sinks, so its trajectory differs, and the other seven boundary misses do not come back. At 1e6, all seven come back on the same quanta.
4. **F5.** [SOURCE][MEASURED]
   - **In code, the paths never meet.** In `integrate()` (`rapier_law.rs` at `29e1c52`), the steps run in this order:
     - every driven body's move is planned first, against the world as it stands (`:805`); the first cast and the retry are there, in `kcc.rs`;
     - the next kinematic translations are set (`:817-818`);
     - each plan's push runs (`:833`). That is the only call into `impulses.rs`, and it writes dynamic bodies' velocities and nothing else (`impulses.rs:244-255`);
     - then the world steps (`:836`).
   - **They can meet only through the world:** a body a push moved is where a later quantum's first cast or grounded check looks.
   - **Measured, with F5 on top of the retry, over the 18 fixture runs and push fixtures:**
     - the firings differ in one run only, the capsule carry: 6 at quanta 155 to 160 become 5 at 157 to 161;
     - the retry hits in none of the 18, with or without F5;
     - behavior-verbs-carry runs 262 quanta instead of 253, which is F5's own change.
   - **The product golden with both is `69a671f962665563`.** So F4's measured effect is the same whether F5 lands first or not.
5. **The red test.** [MEASURED]
   - **The smallest case** is one walker, one floor and one quantum:

     ```js
     const world = createWorld({
       bodies: [{ id: 'walker', x: 7.51119, y: 0.25999999999999984, z: 0, vx: 0.4, vy: 0, vz: 0, hx: 0.25, hy: 0.25, hz: 0.25 }],
       colliders: [{ id: 'floor', minX: 4, maxX: 80, minY: -1, maxY: 0, minZ: -2, maxZ: 6 }],
     }, 'product');
     world.step(new Set(['walker']));
     assert.ok(world.body('walker').y > 0.26 - 1e-3);
     ```

     - y is 0.26 less 3 ulps, so the walker's dilated bottom rests on the floor's top face.
     - On `29e1c52` it ends at 0.25804687499999984, sunk one gravity step. With the retry it ends at 0.2601000000000001.
   - **It depends on exact bits.** At 2 or 6 ulps under 0.26 the walker holds on both builds; at 3, 4 or 5 it sinks on `29e1c52`.
     - The flat walk's own start at 2242 is a red case too: x 24.006249999986952, y 0.2599999999999994, z −7.384715719950948e-10. It ends at 0.2580468749999994 on `29e1c52` and at 0.26009999846574744 with the retry. With z = 0 at that x, both builds hold.
   - **Sturdier red tests:**
     - 900 single-quantum starts, x = 5 + k·0.00617 for k = 400 to 419, at 0 to 44 ulps under 0.26, z = 0. On `29e1c52` 3 sink; with the retry 0 sink. It takes 0.1 s.
     - The whole grid, k < 12,000: 540,000 starts in 10 s. 1,323 sink on `29e1c52`, which is exactly parry#452's count of `None` on the same grid, so every sink is one of parry's misses. With the retry, none sink.

## Caveats

- **The retry's classification** uses parry's distance query from the start pose to the collider the retry hit. For a firing that hits nothing, there is no collider to measure against.
- **The fixture runs are closed loop,** with logged intents re-admitted against the current frame, as in `push-mass.md`. The retry needed no re-admission: every fixture replay is unchanged.
- **Only the box and capsule characters of these runs are measured.** The heightfield seams are sleds. Outcome 3 steps its worlds with no driven body (`world.step(new Set())`, `outcome.test.js:183`), so the controller, and the retry with it, never runs there.

## Commands

```
git worktree add --detach f4/base 29e1c52     # likewise f4/retry, f4/count, f4/countf5
python patch_kcc_retry.py f4/retry && python patch_kcc_retry.py f4/count && python patch_count.py f4/count
cd f4/<w> && node solver/build.mjs            # count, countf5: then node patch_glue.mjs solver/dist/solver.mjs
node flatwalk.mjs 0 && node flatwalk.mjs 1000000
node harness/sim.mjs; npm test --ignore-scripts; node harness/law-runs.mjs --check; node firstdiff.mjs
node harness/corpus.mjs --record-sweep && git diff -- fixtures/sweep/
F4_LOG=q3.jsonl node --import f4hooks.mjs harness/course.test.js    # and outcome.test.js; python f4summary.py q3.jsonl
node f4fixtures.mjs                           # in count and in countf5
node planted2.mjs; node plantsweep.mjs 20 400; node plantsweep.mjs 12000
```
