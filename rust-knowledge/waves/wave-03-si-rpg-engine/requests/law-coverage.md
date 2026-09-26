Law coverage (for T7b): how to measure which lines of the law's Rust a WASM run under node reaches. si-rpg-engine main `93a2d1e`, rustc and cargo 1.98.1 pinned, `wasm32-unknown-unknown`, rapier3d-f64 0.35.3 with `enhanced-determinism`, parry3d-f64 0.30.2; llvm-tools 1.98.1 (LLVM 22.1.8-rust-1.98.1-stable). Measured 2026-09-26.

**Host and tools.**
- Windows 11 Pro, x86_64, node v22.22.3.
- `llvm-cov` and `llvm-profdata` are the `llvm-tools` component of the pinned toolchain, installed for this question. Nothing else was installed: no nightly, no clang, no minicov.

**Engine state.**
- A scratch worktree (`<scratchpad>/law-coverage/engine-cov`) at `93a2d1e`, cloned from GitHub. `E:/AI/si-rpg-engine` was not touched.
- Its `solver/src/lib.rs` gained a three-line shim, gated on a cfg only the coverage build sets (section 2). The product build of that source still has digest `d1c29dd9…` on this host, the same as without the shim.

**Scratch.** `<scratchpad>/law-coverage`:
- `splice_glue.mjs` writes a `solver.mjs` that is `build.mjs`'s generated glue with only its bytes array replaced.
- `dumpcounters.mjs` is a node preload that zeroes the counters before a script and writes them out at exit.
- `covtools.mjs` finds the profile regions, adds the names section, and writes a text profile from dumped counters.
- `timeloop.mjs` times the product scene.

## Answer

1. **Which ways work.**
   - `-C instrument-coverage` on the pinned **stable** compiler is refused for this target: `E0463: can't find crate for profiler_builtins`. The wasm32 standard library ships no profiler runtime.
   - **What works:** the same pinned rustc 1.98.1 with `RUSTC_BOOTSTRAP=1`. That enables `-Z no-profiler-runtime`, which drops the runtime. A three-line shim defines the one symbol the instrumented code still references, `__llvm_profile_runtime`.
   - **What it covers:** everything compiled into the module. That is the engine's `lib.rs`, `rapier_law.rs`, `kcc.rs` and `arena.rs`, and all of Rapier, Parry, nalgebra, glam and std: 736 files, 97,046 lines, 154,222 regions.
   - **No runtime is needed.** The counters are u64s at a fixed address in linear memory. Node reads and zeroes them, and a script writes them as an `llvm-profdata` text profile.
   - **The alternatives:**
     - a separate pinned nightly would do the same with a different compiler binary than the product's, and costs a second toolchain;
     - minicov's runtime is C, and needs a wasm32 clang, which is not installed here;
     - probes placed in the engine's own files would cover `solver/src` only.

     None is needed. [MEASURED]
2. **The recipe** (section 2), with the measured costs:

   | What | Product build | Coverage build |
   |---|---|---|
   | Time per quantum on the product scene | 17.5 µs | 24.5 µs (+40%) |
   | Instantiate | 3 ms | 10 ms |
   | Full build, all dependencies instrumented | n/a | 40 s |
   | Rebuild after a one-line change | 3.15 s | 3.2 s |
   | Mapping one candidate's counters to lines | n/a | about 1.1 s |

   - Counters reset by zeroing their memory range in the same instance. No fresh instance is needed, but zero again after any image restore, because the image carries the counters.
   - Counters map to file and line ranges through `llvm-cov export` against the instrumented module. That works once the function names are added as a custom section `llvm-cov` can read, and the module is linked with `--no-gc-sections` so that no function's name is dropped.
3. **Yes, the instrumented build computes exactly what the product build computes.** [MEASURED]
   - **Product scene:** frame hash `6e0d351693b18c93` on both, three runs each.
   - **A mutant:** `44a8f226fed31771` on both.
   - **Full suite:** 240 of 243 pass on the coverage build. Every fixture replay, the course, the outcome tests and the golden trace agree. The three that fail test the binary's shape, not its results:
     - the memory image's non-zero page count (71 and 72);
     - "one global: the i32 stack pointer" (the shim exports one more).
   - **Why the arithmetic cannot differ.** The counters are integer increments in memory; there is no fast-math and no FMA on this target. So the floating-point operations the law executes are the product's, in the product's order. [REASONED, consistent with every measurement]
4. **Mutants: yes, the same way.**
   - One operator changed at `rapier_law.rs:779` (`b[4] + G * DT` to `b[4] - G * DT`) rebuilds in 3.15 s as a product build and 3.2 s as a coverage build. Only the law crate recompiles; the instrumented dependencies stay cached.
   - Both builds give the mutant's frame hash `44a8f226fed31771`, and coverage shows line 779 executed 10.0k times in the product scene.
   - The cheapest loop per mutant is: edit, incremental coverage build (3.2 s), run, map (1.1 s).

## 1. What was tried [MEASURED]

| Route | Result |
|---|---|
| stable 1.98.1, `-C instrument-coverage` | refused: `error[E0463]: can't find crate for profiler_builtins` ("the compiler may have been built without the profiler runtime"), in every dependency |
| + `RUSTC_BOOTSTRAP=1`, `-Z no-profiler-runtime` | compiles; the link fails: `rust-lld: error: … undefined symbol: __llvm_profile_runtime` |
| + the shim (`#[cfg(law_coverage)] #[unsafe(no_mangle)] pub static __llvm_profile_runtime: i32 = 0;`) and `--cfg law_coverage` | links. 10.6 MB against the product's 1.7 MB. The product's 13 exports plus the shim, no imports. Custom sections `__llvm_covmap` and `__llvm_covfun`. |
| `llvm-cov export --empty-profile` on that module | reads it, then fails: "malformed instrumentation profile data: function name is empty". The names are in a data segment, which `llvm-cov` does not read. |
| + a custom section `__llvm_prf_names` holding the names (`covtools.mjs names-section`) | still fails: 224 of 25,049 function records name functions whose names the linker's `--gc-sections` dropped |
| + `-C link-arg=--no-gc-sections` | every record is named. `llvm-cov` loads the module: 736 files, 97,046 lines, 154,222 regions. |

## 2. The recipe

**Build** (from `solver/`, into its own target directory, so the product build and its digest are untouched):

```
RUSTC_BOOTSTRAP=1 CARGO_TARGET_DIR=<cov-target> \
CARGO_ENCODED_RUSTFLAGS="-C␟target-feature=-relaxed-simd␟-C␟link-arg=--export=__stack_pointer␟-C␟instrument-coverage␟-Z␟no-profiler-runtime␟--cfg␟law_coverage␟-C␟link-arg=--no-gc-sections" \
cargo +1.98.1 build --release --locked --target wasm32-unknown-unknown
```

The ␟ is the 0x1f separator, as in `build.mjs`. Add `build.mjs`'s three `--remap-path-prefix` flags to make the mapping's paths host-independent; `llvm-cov -path-equivalence` then maps them back.

`build.rs` still gives 512 fixed pages. The counters, data records and names take about 4.3 MB of them, and the module stays inside the fixed memory.

**The shim** in `solver/src/lib.rs`. The product never sets the cfg; measured, the product digest is unchanged with the shim present:

```rust
#[cfg(law_coverage)]
#[unsafe(no_mangle)]
pub static __llvm_profile_runtime: i32 = 0;
```

**Load.** The coverage module replaces only the bytes in `build.mjs`'s generated glue (`splice_glue.mjs`), so `packages/tick/world.js` runs it unchanged.

Loading 10.6 MB through the glue's JavaScript array literal takes most of a run's startup (1.37 s against 0.75 s for `harness/sim.mjs`). A coverage glue that reads the `.wasm` from disk would avoid it.

**The counters.**
- `llvm-objdump -t <module>` names the three regions, because the module's name section keeps the data-segment names. In this build:

  | Region | Address | Size |
  |---|---|---|
  | `__llvm_prf_cnts` | 0x124108 | 210,576 bytes, u64 counters |
  | `__llvm_prf_data` | 0x157798 | 48-byte records, one per function |
  | `__llvm_prf_names` | 0x1f6ca8 | 3.49 MB of names |

- **Reset:** `new Uint8Array(memory.buffer, cntsAddr, cntsSize).fill(0)` in the running instance, before each candidate.
- **Restores:** the counters are ordinary memory, so T6's sparse image and restore carry them. Zero them after a restore. Never compare images across the product and coverage builds; the suite's "a stored image from another binary is not used" test refuses that already.
- **Read:** copy the same range after the run.

**Map to lines** (`covtools.mjs`):
1. Once per build, `names-section`: copy the names blob out of memory into a custom section `__llvm_prf_names` appended to a copy of the module. That is where `llvm-cov` looks for names. 0.12 s.
2. Per candidate, `proftext`:
   - Walk the data records: `NameRef` (MD5 of the name), `FuncHash`, the relative counter pointer and `NumCounters`, in wasm32's 48-byte layout. Name them from the blob.
   - Write `llvm-profdata`'s text format for frontend profiles: name, `# Func Hash:`, `# Num Counters:`, `# Counter Values:`.
   - 0.18 s.
3. `llvm-profdata merge -o run.profdata run.proftext`: 0.07 s.
4. `llvm-cov export -instr-profile run.profdata <named module> -sources <changed files>`: 0.82 s for `rapier_law.rs`. Or use `llvm-cov show` for a line view.

   The export gives, per file, the segments and each line's execution count. "Did the run execute the changed lines" is then a count above zero on each changed line.

**What it covers.** In the product scene, lines covered:

| File | Lines covered |
|---|---|
| `rapier_law.rs` | 90.7% |
| `kcc.rs` | 60.2% |
| `arena.rs` | 66.7% |
| `lib.rs` (the box law, mostly unused by the product scene) | 6.1% |
| Rapier's own `character_controller.rs` (the engine uses its copy) | 3.5% |

Line counts are per line, including F2's added branch in `kcc.rs:615-617`, which ran 4.56k times.

## 3. Does it compute what the product computes? [MEASURED]

| Run | Product build | Coverage build (gc) | Coverage build (no gc) |
|---|---|---|---|
| `harness/sim.mjs`, product golden | `6e0d351693b18c93` | `6e0d351693b18c93` | `6e0d351693b18c93` |
| the same with the `rapier_law.rs:779` mutant | `44a8f226fed31771` | n/a | `44a8f226fed31771` |
| full suite, 243 tests at plain `93a2d1e` | 243/243 | 240/243 | not run |

The three failures on the coverage build:
- "the sparse image: 512 pages of 64 KiB, the non-zero ones kept": error "71 pages";
- "(b) a stored image from another binary is not used": error "pages 72";
- "linear memory and the stack pointer are the whole mutable state of the binary": error "one global: the i32 stack pointer". The shim's static is exported as a second global.

All three describe the module's layout. Every test that compares frames, hashes, outcomes or goldens passes.

**Why it cannot drift [REASONED].**
- Instrumentation inserts integer adds on u64 counters in memory.
- The law's floating-point operations are unchanged: there is no fast-math, `relaxed-simd` is off, and wasm has no FMA without it. Wasm float semantics are fixed.
- Rapier's `enhanced-determinism` already pins libm for transcendental functions.

Code layout does change, and the counters are extra memory writes. Neither changes a floating-point result.

## 4. Costs and choices

- **Per quantum.** The product scene takes 17.2 to 17.9 µs a quantum on the product build and 23.9 to 25.0 on the coverage build (three runs each). With `--gc-sections` it is the same, 24.5 to 25.0.
- **Instantiate:** 3 ms against 10 ms.
- **Builds.**
  - A cold coverage build, every dependency instrumented, takes 38 to 40 s. It uses a separate target directory, so it never touches the product's cached build.
  - An incremental rebuild of the law crate takes 3.2 s. The product's incremental rebuild takes 3.15 s.
- **Instrumenting only the law's crate.** `cargo rustc` for the last crate, with the flags after `--`, would cover `solver/src` only, which is faster to build and run. Not measured. T7b's "anything the law calls" needs the dependencies instrumented, so the recipe above instruments all of them.
- **`RUSTC_BOOTSTRAP=1` is an escape hatch the Rust project does not support.** It is the cheapest route here because the compiler binary is the pinned product compiler. `-Z no-profiler-runtime` is unstable and must be re-checked whenever the toolchain pin moves. A pinned nightly would carry the same flag at the cost of a second compiler.

## Commands

```
cd <cov-worktree>/solver && RUSTC_BOOTSTRAP=1 CARGO_TARGET_DIR=<cov-target> CARGO_ENCODED_RUSTFLAGS=... cargo +1.98.1 build --release --locked --target wasm32-unknown-unknown
node splice_glue.mjs <product solver.mjs> <cov-target>/wasm32-unknown-unknown/release/si_solver.wasm solver/dist/solver.mjs
node covtools.mjs regions <wasm>                 # {"__llvm_prf_cnts":{"addr":...,"size":...}, ...}
COV_DUMP=run.cnts.bin COV_CNTS=<addr>,<size> node --import dumpcounters.mjs harness/sim.mjs
node covtools.mjs names-section <wasm> named.wasm
node covtools.mjs proftext <wasm> run.cnts.bin run.proftext
llvm-profdata merge -o run.profdata run.proftext
llvm-cov export -instr-profile run.profdata named.wasm -sources solver/src/rapier_law.rs   # or: llvm-cov show ...
node timeloop.mjs                                 # per-quantum timing, product scene
```
