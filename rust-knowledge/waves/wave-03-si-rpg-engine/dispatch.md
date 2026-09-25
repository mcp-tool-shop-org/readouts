# Wave 3 — si-rpg-engine: how Rust is and will be used in the engine

**Date:** 2026-09-25 · **KB:** `rust-knowledge` · **Tier:** si-rpg-engine · **Lanes:** 9 (7 planned, 2 answering the engine coordinator) · **Recipes:** 90

## Why this wave exists

si-rpg-engine's law is Rust compiled to one `wasm32-unknown-unknown` binary. It runs `rapier3d-f64` 0.35.3 with `enhanced-determinism` under rustc 1.98.1. The binary exports raw `extern "C"` functions over `static mut` f64 buffers, and its Linux digest is pinned in `fixtures/solver.sha256`. Three JavaScript engines print the same golden from it. Phase 2, "the suite", turns on Rust questions:

- T2: restoring the solver from a snapshot;
- T3: a binary lint and fixed memory;
- T4: CCD and a character-controller course at its limits.

After Phase 2 come collision from meshes and host bindings for Godot and Unreal. This wave answers those questions against the pinned sources, with the compiler as witness.

Two lanes, `restore-internals` and `binary-and-limits`, were added mid-wave. The engine's coordinator (a separate session) had filed eight blocking questions in `docs/rust-kb-requests.md`, and these lanes answer them. The full answers are in `requests/answers-q1-q4.md` and `requests/answers-q5-q8.md`. The combined file `requests/rust-kb-answers.md` is on the engine's `main` verbatim as `docs/rust-kb-answers.md` (PR #50).

## One-line answers per lane

| Lane | The answer |
|---|---|
| wasm-raw-abi | The module imports nothing and exports `memory` plus its `#[unsafe(no_mangle)]` functions. A panic is an `unreachable` trap that leaves half-written state. dlmalloc grows memory on its first allocation. JS views detach on growth. `wasm32v1-none` cannot build this dependency graph. |
| float-determinism | The five basic ops are correctly rounded and never contracted, identically on every IEEE host and wasm engine. Not identical across hosts: NaN bits, std transcendentals, min/max zero ties, relaxed SIMD and HashMap order. `enhanced-determinism` does **not** turn SIMD off. Method-call transcendentals in dependencies escape libm, so the toolchain pin is part of the law. |
| rapier-core | `step` takes 12 arguments at 0.35.3. Rapier promises identity only for the same build, inputs and insertion order. Non-finite state is quarantined, not refused. Fast bodies get CCD even with `ccd_enabled(false)`. 0.36.0 (published 2026-09-25) breaks this engine's code, so stay on `=0.35.3`. |
| restore-internals | No sound public path writes a contact point. Even a sound write diverges on quantum 0, because the solver also reads lever arms, persisted point geometry, recycle state and colours. Sleep and broad-phase state cannot be rebuilt. Serde restores exactly but is not canonical. **Route (d): persistent world plus replay.** |
| rapier-shapes-kcc | TriMesh and HeightField are for fixed ground only. Meshes are canonicalised and validated offline, because parry swallows topology errors, accepts NaN and welds ±0 by hash layout. The controller casts, never moves. `is_sliding_down_slope` is true on flat ground. |
| binary-and-limits | Link args leave std's `memory.grow`, so a fixed-arena allocator is needed. The lint must decode instructions, since padded LEB128 and immediates defeat byte scans. CCD is automatic and stateless at one substep. The step limit is `max_height + offset` (0.3101). |
| sim-architecture | Integer ticks; state as explicit little-endian bytes behind one save/load pair; proof by restore-and-rerun at many points. Hash named functions over explicit bytes. The solver's `mix_u64` collides, and the two-lane hasher's u32-only digests carry 32 bits. |
| host-embedding | A: one pinned wasm in an embedded runtime. B: native builds. C: WIT components. None of them carries the JS tick and frame hash, so where the hash comes from is the host phase's first decision. godot-wasm runs Wasmtime on non-deterministic defaults. |
| ci-reproducible-builds | Byte-reproducible on one host OS/CPU with the cargo-home remap. Across hosts, both path separators and Cargo's host-triple metadata change the bytes, so re-pin only from x86_64 Linux. Only the cargo-home remap does work today. |

## What the wave changed in the engine (the loop with the coordinator)

Every finding went to the coordinator session as it landed, marked with its evidence level and a "consistent with / contradicts pin N" line. What resulted on the engine's `main`:

1. **T2 was rebuilt on route (d) + (e).** Main's persistent world stays the law. The revised dispatch merged at `9c47d40`, and PR #53 (open, head `bb462c6`) builds it.
   - Restore is replay to the save tick, plus a linear-memory image that carries the binary digest and an FNV digest of its bytes. `__stack_pointer` is exported so that a save is refused unless the stack pointer is at its base.
   - Restores are tested at many points chosen from each run: first new contact, first sleep, first wake, and a third and two thirds of the way.
   - `solver_clear_warmstart` and its cast leave `main`. PR #43, the rebuild-per-quantum design built on the same cast, was closed unmerged.
   - The bytes-sensitivity and structural tests replace the clear test. Steering is stated as unproven in this slice.
2. **T3:** 512 pages, a contact-dense test at the caps, `--no-growable-memory` from `build.rs`, the three lint gaps closed and three lint tests added (including padded LEB128). It names matrixmultiply 0.3.11 and wide 1.7.1 as the gated relaxed-SIMD sites.
3. **T4 pin 2:**
   - its "passes through today" premise was corrected: the box stays near;
   - `max_ccd_substeps = 1` is set explicitly;
   - the red evidence now comes from a test-only native build at 0.
4. **T4 pin 5** now uses the measured course: steps 0.29/0.33, drops 0.19/0.22 at 0.4 u/s, slopes 44°/46° with the speed and a bounded run, and about 1,300 quanta for a start inside geometry.
5. **S1 soundness** (`docs/dispatch-s1-soundness.md`, 13+ pins):
   - a source test for the whole cast family;
   - the mode-slot decoder;
   - the `MAX_BODIES ≤ 64` assert;
   - signed zero in `signature()`;
   - `Result<(), Refusal>` plus `#![deny(unused_must_use)]`;
   - `sort_by` kept;
   - `--locked` with `CARGO_ENCODED_RUSTFLAGS`;
   - `#[unsafe(no_mangle)]` and the `&raw mut` rewrite under edition 2021;
   - the removal case in the insertion-order test;
   - `bad()` → `!is_finite()`;
   - `canon_quat` refusing non-finite input and scaling by its largest component;
   - the `warm_broadphase` comment;
   - the u32 two-lane hash split.
6. **S2 "one surface"** (`docs/dispatch-s2-one-surface.md`): the tick's `heightfieldSupport` moves from bilinear to parry's two-triangle split. Pin 1's diagonal and pin 3's values were checked against `build_world` and `triangles_at` (see below).
7. **Three S1 pins from later lanes**, all merged:
   - pin 14 (PR #48): the toolchain is part of the law;
   - pin 15 (PR #51): the signature compares canonical geometry directly, because `mix_u64` collides;
   - pin 7 (PR #52): the host triple, not only path separators, is why only the Linux build is pinned.

   The per-function relaxed-SIMD enable is recorded in T3's `FLAGS.md` wording (PR #44).
8. **T2's route costs.** A measurement seat priced routes (a) and (c) in `requests/route-costs-a-c.md`. The coordinator recorded the numbers as the reason (d)+(e) stands, with (c) as the priced fallback.
   - Route (a), `warmstart_coefficient = 0`, is sound but visibly wrong for stacks, because 0 also switches the warm start off between Rapier's 4 substeps. A 5-box stack rests 3.7–3.8e-2 interpenetrated and 5.5e-2 low, and it collapses if something keeps it awake.
   - Route (c), serde, is exact: it matched T2's pointer carry at every quantum for 10,000 quanta. Under V8 it costs 0.22–0.26 ms per quantum at 64 boxes, and the wasm grows by 82,579 B.
9. **S1 pin 11, `canon_quat` (PR #55).** The route-costs seat found that the closed T2 branch refused its own snapshots, because its restore ran `canon_quat` twice and compared the bits. The coordinating session confirmed through the oracle that the function is not idempotent (see below). Pin 11 now states that contract:
   - canonicalize once, at output;
   - never compare re-canonicalized bits;
   - never restore by reloading records.

   No golden moves.
10. **Raised with the coordinator, not yet decided.** T3's pin 10 fixes memory at 512 pages, and a T2 image is the whole memory. Once T3 rebases onto PR #53, each image grows from 21 pages to 512: 24.4× the bytes, and by linear scaling about 24–32 ms to copy out. The suggestion is that T3 prints the image cost, and that T5's save stores the image sparsely with its digest over the full image.
11. **Answered: `requests/driven-switch.md`.**
    - **Main does rebuild the world at every verb boundary.** Each driven-mask change (an actor starting or stopping a drive) and each carried-mask change (a pick-up or drop) triggers `ensure()` → `build_world`. A counter measured 3 rebuilds in the product scene's 10,000 quanta (ticks 201, 261 and 401) and 11 in 12,242 quanta across the fixtures. Each product rebuild drops 18–20 warm-start impulses and wakes 5 sleeping bodies.
    - **The switch can be done in place** with public 0.35.3 calls: `set_body_type` first, then the other setters. A carried body uses `set_enabled`, which keeps its handle, or `remove_body` + `insert`, which gives it a new handle generation.
    - **Prototype results.** The in-place prototype moved the product digest once, and it replays and image-restores bit for bit. But Rapier's hidden state then crosses verb boundaries: a no-op type round trip moved later positions by 9.5e-5.
    - **Status.** It is a later-slice fidelity item. T4's builder hit the same rebuild at the climber's lift (tick 261).
12. **Answered: `requests/walker-stall.md`.** In T4's translated scene the walker lost most of a quantum's travel about once in 30 quanta, and the offset only moved which quanta. The origin stalls too: 332 times in 10,000 quanta, against 323 at 1e6.
    - **Cause:** a bug in Rapier's character controller.
      - When the floor hit's normal is parallel to `up` but its y is one ulp below 1, `decompose_hit` has no horizontal direction, since `normal × up` is zero.
      - The travel is filed as a vertical tangent with a −4.3e-19 up-component, and the non-slip branch keeps only the nudge.
      - The code is unchanged at rapier 0.36.0.
      - Reported upstream as https://github.com/dimforge/rapier/issues/1019. The report carries a minimal repro checked through the compile oracle, the cause, and the 3D `decompose_hit` fix.
    - **Fixes measured** at both offsets and on the course:
      - `up = (0, 1, 1e-12)`: one line, 0 stalls, but only inside a measured window from 1e-16 to 1e-10;
      - an engine-owned `move_shape` copy with one extra `decompose_hit` branch: 0 stalls, no window, about 500 lines to own.
    - **The KB's own drop threshold is narrowed.** The binary-and-limits recipe's 0.2105 holds only for its own geometry, and the 0.200–0.2105 band is bit-sensitive. Both the stall and the threshold are recorded as `later-measurement` operator notes on the two recipes.

## Advisor measurements (the coordinating session, recorded here, not in a lane)

These are the checks the coordinating session ran itself: the verification of a peer's pin or of a seat's answer. Each is reproducible from the command given.

- **The answers' citations.** Before release I re-read the load-bearing citations of `rust-kb-answers.md` in the pinned registry sources, and every one matched:
  - `physics_hooks.rs:43/52`;
  - `contact_pair.rs:620` and `:237/243/255`;
  - `contact_with_coulomb_friction.rs:166-171`;
  - `rigid_body_components.rs:1325`;
  - `ccd_solver.rs:17-25`;
  - `character_controller.rs:673/674/742-743/836`;
  - parry `bvh_insert.rs:161-168/367`;
  - dlmalloc `wasm.rs:50-56`.
- **No mutable contact-pair path upstream.** crates.io's `rapier3d-f64` max version is 0.36.0, published 2026-09-25. GitHub master's `narrow_phase/queries.rs` still has only `&self` accessors, and a code search for `contact_pairs_mut` in dimforge/rapier returns 0. In 0.35.3, `interaction_graph.rs:14` has a `pub(crate) graph` and `:264` a `&'a mut E` iterator, so the vendored route (b) was small.
- **S2 pin 1 is correct.**
  - `build_world` (`rapier_law.rs:366-378` on `main`) writes the row-major `HEIGHTS[row*cols+col]` into parry's column-major `data[row+col*rows]`, with scale `((cols-1)·cell, 1, (rows-1)·cell)`.
  - parry `heightfield3.rs:338-401` gives `p10 = (x0, y[i+1,j], z1)` and `p01 = (x1, y[i,j+1], z0)`.
  - The pin's two planes meet every corner and agree on the diagonal `tx + tz = 1`. Cell-centre values are 0 (off-diagonal corner raised), 0.5 (on-diagonal corner) and 0.25 (bilinear).
- **The S1 pin 5 gate, through the oracle (rustc 1.98.1, edition 2021).**
  - A dropped call to an unattributed `bool` refusal: no warning.
  - `#[must_use]` on the function: a warning.
  - Adding `#![deny(unused_must_use)]`: an error.
  - `Result<(), Refusal>`: a warning by type.
  - And `bad(±inf)` is false.
- **Mutable wasm state, for T2 pin 3.** A `wasmparser` 0.259 program run through the oracle scanned main's persistent-law build, PR #44's arena build and a dlmalloc-arena build.
  - Each has exactly one global: global 0, `i32`, mutable, initialised to 1048576. That is `__stack_pointer`, not exported, written at 1,134–1,148 `global.set` sites.
  - The table is fixed at 496/496, with zero `table.set` and `table.grow`.
  - So a linear-memory image is complete when it is taken between calls that returned. A trapped instance is dead, because a trap leaves the stack pointer lowered. The image must be sized to the fresh instance's memory.
- **Segment state, for PR #53's pin 3.** A second `wasmparser` program covered the same three builds.
  - Each has 0 imports, no start section and no DataCount section.
  - Each has 2 active data segments and 1 active element segment, with no passive or declared segments.
  - Each has zero `memory.init`, `data.drop`, `table.init`, `elem.drop`, `table.copy` and `table.fill`. The only bulk instructions are the stateless `memory.copy` (593–602 sites) and `memory.fill` (202–206).
  - So no segment carries a "dropped" bit that an image could miss. Memory plus the stack pointer at its base is the whole state.
  - The suggested guard: the globals test also asserts no passive segments and no start section. A move to shared memory would add both.
  - Both programs are in `probes/`, and the header of each names the three builds it reads. Rerun them with `SI_BUILDS=<dir> python scripts/compile_oracle.py file waves/wave-03-si-rpg-engine/probes/segments_probe.rs --expect runs --edition 2021 --deps wasmparser`, or the same command with `globals_probe.rs`.
- **`canon_quat` is not idempotent, for S1 pin 11.** `probes/canon_idem.rs` copies `canon` and `canon_quat` verbatim from `rapier_law.rs` (lines 68–70 and 138–157 at `5ec07f0`, identical in PR #53). It feeds them 200,000 deterministic inputs.
  - 62,573 canonical quaternions (31%) move under a second application.
  - 4,623 move again under a third, so iterating does not settle.
  - First case: `(-6.490756403187095e-5, 1.8017933394002647e-5, 2.095605450308155e-5, 0.999999997511603)` becomes `(…097e-5, …265e-5, …553e-5, 0.9999999975116031)`.
  - Rerun it with `python scripts/compile_oracle.py file waves/wave-03-si-rpg-engine/probes/canon_idem.rs --expect runs --edition 2021`.
  - On main, body quaternions pass through `canon_quat` in `build_world` (on a rebuild) and in `rebuild_snapshot` (for output).
    - An image restore never applies it twice.
    - A persistent run applies it once between verb boundaries, but twice at each boundary: a changed driven or carried mask rebuilds the world from records that were already canonical.
    - `requests/driven-switch.md` measured 11 such rebuilds in 12,242 quanta. The minds fixture's rebuild at tick 42 moved two quaternions' bits.
    - An earlier version of this note, and delta #18, said a persistent run never canonicalizes twice. That was wrong.

## Where the evidence is thin

- ARM64 is unmeasured everywhere; T3's lane decides it.
- The claim that the toolchain's `log2`, `acos` and `cos` sit on the hot path rests on one scratch build's call graph.
- The route costs for (a) and (c) come from one measurement seat on one Windows x86_64 desktop, with unit cubes on a flat slab only. The report carries no verifier verdict.
- Consoles appear on no retrieved page.
- Where the tick and hash run in a host is undecided, and that is the next architectural question.

## What locks, what stays advisory

`verification.md` sets this, from the joined verifier verdicts and the compiler run.
- **Load-bearing:** the 85 solid recipes, above all the two answer lanes the engine built on.
- **Advisory:**
  - the five plausible recipes;
  - every engine note until it is re-checked against main (the citation anchors name the commit each was checked at);
  - every single-seat measurement.
