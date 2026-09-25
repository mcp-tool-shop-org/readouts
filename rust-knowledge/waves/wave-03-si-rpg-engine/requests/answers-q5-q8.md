Answers 5–8 — rapier3d-f64 0.35.3 (enhanced-determinism), rustc 1.98.1, wasm32-unknown-unknown, checked 2026-09-25.

Engine state checked: GitHub `main` at 4782a8a (after PR #42, the T4 amendment); `solver/` there is byte-identical to the local checkout apart from CRLF. Every binary number below comes from a scratch copy of `solver/` built on this rig with `build.mjs`'s exact `RUSTFLAGS` (`-C target-feature=-relaxed-simd` plus the three `--remap-path-prefix` flags). That copy reproduces both goldens (`fd2f6c03fb982d77`, `0d38671370d12d1e`) and passes all 73 tests. It is a Windows build, so its bytes differ from the pinned Linux artifact only in path strings. Scripts and binaries are in the lane's scratch directory (`…/scratchpad/q5-q8/`). Decoding used a scratch `wasmparser` 0.259 tool (`wscan`), and module execution used node 22.22.3 (V8). Rapier and parry line numbers are from the pinned registry sources, `rapier3d-f64-0.35.3/…` and `parry3d-f64-0.30.2/…`, which is the source docs.rs serves. Compile oracle on this lane: `python scripts/compile_oracle.py check waves/wave-03-si-rpg-engine/lanes/binary-and-limits.json` gives `19 checks over 10 recipes — 19 pass, 0 fail`.

## 5. T3 lint — memory

**Answer.** There are two stable linker arguments. Pass either through `-C link-arg=` to `rust-lld` (LLD 22.1.8):

- `--no-growable-memory` sets the maximum equal to the initial size that wasm-ld computes.
- `--initial-memory=N --max-memory=N` does the same with an explicit size. N must be a multiple of 65,536 and at least the static footprint wasm-ld reports. For the solver that footprint is 1,117,808 bytes: a 1 MiB stack placed first, about 53 KB of data, and the 15,872 bytes of `BODIES`/`COLLIDERS`/`HEIGHTS` statics. That makes the minimum 18 pages.

No `-Z` flag is needed. Neither argument removes the `memory.grow` instruction. std's wasm32 `System` allocator is dlmalloc 0.2.13, and its `alloc` calls `memory_grow`. The solver binary contains exactly one `memory.grow`, inside `<dlmalloc::sys::System as dlmalloc::Allocator>::alloc`, under every linker setting I tried. No other crate in the solver's graph calls `memory_grow`. When the maximum equals the initial size, that instruction returns −1 for any growth of one page or more, because growth past the maximum must fail. dlmalloc never asks for less. Running out of memory then becomes the same trap on every host. T3's lint as pinned still refuses the binary, though.

The fix for the instruction is a `#[global_allocator]` that never calls `memory_grow` and serves a fixed static arena. The smallest change keeps std's own algorithm: the public `dlmalloc` 0.2.13 crate's `Dlmalloc::new_with_allocator`, with an `Allocator` that hands out one static arena. I built and measured it: zero `memory.grow`, memory 532/532 pages with `--no-growable-memory`, both goldens and 73/73 tests unchanged.

Size of the heap:

- **Today's content** needs 21 pages in total: the product harness over 10,000 quanta. Each test file of the suite stays at 18–20.
- **Worlds at the buffer caps** need far more. Their need scales with contact manifolds, not with body count:
  - 49 pages: a settling pile of 64 boxes on a full heightfield.
  - 147 pages: 64 heavily overlapping boxes.
  - 3,320 pages: everything overlapping everything, including all 450 heightfield triangles.

So N is a policy bound, not a derived constant. Exceeding it traps the same way on every host.

**What I checked.**
- Sources:
  - LLD WebAssembly docs, https://lld.llvm.org/WebAssembly.html: `--initial-memory` defaults to the sum of stack, static data and heap; `--max-memory` defaults to unlimited; `--no-growable-memory` sets the maximum to the initial size.
  - rustc book codegen options, https://doc.rust-lang.org/stable/rustc/codegen-options/index.html: `-C link-arg` appends one argument to the linker invocation.
  - Cargo book build scripts, https://doc.rust-lang.org/cargo/reference/build-scripts.html: `cargo::rustc-link-arg-cdylib` passes `-C link-arg` for cdylib targets only.
  - std at the 1.98.1 tag, https://github.com/rust-lang/rust/blob/1.98.1/library/std/src/sys/alloc/wasm.rs: lines 11–17 name dlmalloc, 23–27 hold the `DLMALLOC` static, and 29–60 implement `GlobalAlloc for System`. `library/Cargo.lock` at 1.98.1 pins dlmalloc 0.2.13.
  - dlmalloc 0.2.13 `src/wasm.rs` (https://github.com/alexcrichton/dlmalloc-rs/blob/0.2.13/src/wasm.rs; also opened on docs.rs):
    - Lines 17–48 donate the linker's `[__heap_base, __heap_end)` once. The flag flips on the first request even when that request does not fit.
    - Lines 50–56 call `wasm::memory_grow(0, pages)` and return null on `usize::MAX`.
    - Lines 87–99 are `alloc`.
    - Lines 101–115: `remap`, `free_part` and `free` never release memory.
  - dlmalloc 0.2.13 API, https://docs.rs/dlmalloc/0.2.13/dlmalloc/struct.Dlmalloc.html and `trait.Allocator.html`: `Dlmalloc<A = System>`, `pub const fn new_with_allocator(sys_allocator: A)`, and `unsafe trait Allocator`.
  - `core::arch::wasm32::memory_grow`, https://doc.rust-lang.org/stable/core/arch/wasm32/fn.memory_grow.html: returns `usize::MAX` on failure.
  - WebAssembly 3.0 spec, Growing memories (https://webassembly.github.io/spec/core/exec/modules.html): growth fails when it would exceed the maximum. The profiles appendix (https://webassembly.github.io/spec/core/appendix/profiles.html) says `memory.grow` stays technically non-deterministic even in the deterministic profile.
  - Wasmtime deterministic execution, https://docs.wasmtime.dev/examples-deterministic-wasm-execution.html: growth may succeed or fail non-deterministically. It recommends a validator that rejects growth instructions or memories that are not fixed-size.
  - `std::alloc` `#[global_allocator]`, https://doc.rust-lang.org/stable/std/alloc/index.html.
- Measured on the copy:
  - **Baseline** (`cargo +1.98.1 build --release --target wasm32-unknown-unknown` with build.mjs's RUSTFLAGS, then `wscan si_solver.wasm`):
    ```
    memory: initial=18 pages (1179648 bytes) maximum=None
    memory.grow instructions: 1
      memory.grow in func 1123 …: _RNvXs_NtCsi6WBrLFLuLB_8dlmalloc3sysNtB4_6SystemNtB6_9Allocator5alloc
    ```
    `cargo rustc … -- --print link-args` shows `-z stack-size=1048576 --stack-first … libdlmalloc.rlib … --gc-sections -O3` and no memory limit.
  - **Link variants** (`cargo +1.98.1 rustc --release --target wasm32-unknown-unknown -- -C link-arg=…`):
    - `--no-growable-memory` → 18/18 pages, `memory.grow` still 1.
    - `--initial-memory=4194304 --max-memory=4194304` → 64/64, still 1.
    - `--initial-memory=10485760 --no-growable-memory` → 160/160, still 1.
    - Errors, verbatim:
      - `rust-lld: error: initial memory must be aligned to the page size (65536 bytes)`
      - `rust-lld: error: initial memory too small, 1117808 bytes needed`
      - `rust-lld: error: maximum memory too small, 4194304 bytes needed`
  - **Runtime** (`node drive.mjs <wasm> <scene> 600` loads through `solver_load`, steps through `solver_step`, and reads `memory.buffer.byteLength`):

    | scene | pages after load | peak pages | snapshot bytes |
    |---|---|---|---|
    | pile | 25 | 49 | 49,848 |
    | dense | 61 | 147 | 213,560 |
    | crush | 1,129 | 3,320 | 6,480,000 |

    The product harness goes from 18 to 21 pages, with a 1,840-byte snapshot.
  - **Fixed memory with std's allocator**:
    - `--no-growable-memory` alone (18 fixed pages): both scenes trap with `RuntimeError: unreachable`, `harness/sim.mjs` prints `NAN`, and 32 of 73 tests fail.
    - 64 fixed pages: the goldens match and all 73 tests pass. The pile scene's every-quantum snapshot hash `33dde869dc037425` equals the growable build's. The dense scene traps.
  - **Allocator swap** (`var/dlarena`: dlmalloc 0.2.13 over a 32 MiB static arena, plus `--no-growable-memory`):
    - 532/532 pages, `memory.grow instructions: 0`.
    - `node harness/check.js` prints both goldens and `node --test …` passes 73/73.
    - pile and dense snapshot hashes are identical to the growable build (`33dde869dc037425`, `854795be09b370f3`), and crush traps.
    - It adds only `dlmalloc 0.2.13` and `cfg-if 1.0.5` to the wasm32 graph.
    - A hand-written size-class arena gave the same results (530/530 pages, 0 grows); the whole suite used at most 288,768 bytes of that arena.
  - **Link args from `build.rs`**: a `build.rs` printing `cargo::rustc-link-arg-cdylib=--no-growable-memory`, built with `RUSTFLAGS` set, still produced 18/18. So a build-script link arg survives `build.mjs`'s `RUSTFLAGS` override.
  - **Graph grep** over the cached sources of every crate in `cargo tree --target wasm32-unknown-unknown -e normal`: no `memory_grow` anywhere.
- Oracle (lane `binary-and-limits`, all PASS):
  - `grow()` returns 16 without a flag, −1 under `--no-growable-memory`, and 64 pages / −1 under equal initial and max of 4,194,304.
  - A misaligned `--initial-memory=4000000` fails with the page-size error.
  - std's allocator grows 65 pages for a 4 MiB `Vec` and keeps its pages after `drop`.
  - A fixed-arena `#[global_allocator]` grows 0.

**Consequence for T3.**
- **Make growth impossible and remove the instruction.**
  - Add a `#[global_allocator]` in `solver/src/lib.rs`: `dlmalloc::Dlmalloc::new_with_allocator(FixedArena)`, where `FixedArena::alloc` hands out one `static` zero-initialised arena once and returns `(null, 0, 0)` after that. Add `dlmalloc = "=0.2.13"` to `solver/Cargo.toml`.
  - Link with `--no-growable-memory`. wasm-ld then sets initial = maximum = stack + data + arena, rounded to pages.
  - Put the link argument in a `solver/build.rs` as `cargo::rustc-link-arg-cdylib=--no-growable-memory`, where `build.mjs`'s `RUSTFLAGS` cannot drop it. The alternative is to repeat `-C link-arg=--no-growable-memory` in both `.cargo/config.toml` and `build.mjs`, as the relaxed-SIMD pin already does.
- **Size the arena.** Under today's law, a 32 MiB arena (532 pages) passes the goldens, the suite and both 64-body scenes. The dense scene's dlmalloc heap peaked at about 8.5 MB there. Under PR #44's per-quantum rebuild, the same scene needs 245 pages in total (see the audit below). So fix the memory at 512 pages (32 MiB) and record N in `FLAGS.md`. The digest moves once and the goldens do not (measured).
- **Lint the memory section.** The lint reads the limits of the defined memory and of any imported memory. Flags 0x00 and 0x04 (no maximum) are refused. For 0x01 and 0x05 it compares max with min.
- **Measuring N later.** For any new world, the high-water mark is `memory.buffer.byteLength` after the run: dlmalloc never releases memory and wasm memory never shrinks.

**Audit of PR #44 (head b99a636), claims 1 and 2.** I rebuilt the PR's `solver/` with its own flags, `-C target-feature=-relaxed-simd -C link-arg=--initial-memory=16777216 -C link-arg=--max-memory=16777216`, and decoded the output.

- **Claim 1: agree.** The old binary declares `initial=18 pages, maximum=None`, and std's allocator contributes exactly one `memory.grow`. The PR's own `lint.mjs`, run on my baseline, reports that instruction at byte 1,248,211 in function body 1123. My decoder found it at the same place (`0x130bd3`).
- **Claim 2, the instruction: agree.** Memory is 256/256 pages and the module has **no** `memory.grow` instruction: wasmparser reports `memory.grow instructions: 0`, plus one `memory.size`, which `Arena::alloc` uses to find the end of memory. The PR's lint prints `lint clean: memory 256/256 pages, 1228 function bodies, 598036 instructions, 0 SIMD, no relaxed SIMD, no memory.grow`. The instruction is gone, not merely failing at run time, for three reasons:
  - the `#[global_allocator]` replaces std's `System`, so `--gc-sections` drops std's dlmalloc;
  - the crate's `Dlmalloc<Arena>` never instantiates its own grow-backed `System`;
  - this matches my own dlmalloc-arena build.
- **Claim 2, the headroom: disagree.** 256 pages is not enough headroom at peak under the PR's law. The PR's `build.mjs` says the old growable build "peaked at 71 pages" at capacity with a resting pile. But a limit on bodies is not a limit on contacts. The PR's law also rebuilds the Rapier world every quantum, which raised every peak I measured. I built the same law growable (the PR's `solver/` with its `mod arena` removed) and ran my scenes:

  | scene | old law, peak pages | PR's law, peak pages | fixed 256-page build |
  |---|---|---|---|
  | static footprint | 18 | 22 (the 256 KiB `RESTORE` buffer) | — |
  | pile | 49 | 53 | runs 2,000 quanta |
  | dense | 147 | 245 | runs 2,000 quanta, 11 pages under the limit (about 4%) |
  | crush | 3,320 | 3,973 | traps with `RuntimeError: unreachable` |

  Snapshots under the PR's law reach 37,952 bytes on pile and 211,880 on dense, which is 81% of the PR's 262,144-byte `RESTORE_CAP`. Crush reaches 6,480,000 bytes, so `solver_restore` would refuse it.
- **Recommendation.**
  - Use 512 pages (32 MiB), about 2× the dense peak.
  - Add a test that runs a contact-dense scene at the caps and asserts it completes. A law change that raises the peak then fails in CI instead of trapping in the field.
  - State in `FLAGS.md` that a world denser than the bound traps, the same way on every host. No fixed size covers every world the caps admit.
- **Pin 8.** In my builds the allocator swap and fixed memory alone keep the golden at `fd2f6c03fb982d77`. The PR's new golden `7f7040de58e74e86` therefore comes from its other law changes. This is an inference: I did not run the PR's harness.

**Contradicts a pin?** Yes, pin 2. It says the build fixes the memory "with the linker's initial and maximum memory arguments". Those arguments fix the limits, but std's allocator still contains a `memory.grow`, and pin 2's own lint refuses any `memory.grow`. So pin 2 needs the allocator swap, or a narrower lint that refuses only growable memories. The narrower lint is also deterministic: with max = initial, every growth by one page or more must fail. Pin 8 holds: the goldens did not move under either fixed-memory build.

Pin check: contradicts pin 2 of dispatch-t3-platforms.md because the linker's initial/maximum arguments leave std's allocator's memory.grow in the binary (one instance, measured) and the lint refuses the instruction, dlmalloc-0.2.13/src/wasm.rs:50-56.

## 6. T3 lint — opcodes

**Answer.**

- **Relaxed SIMD.** Each instruction is the `0xFD` prefix followed by its opcode as a u32 LEB128. The opcodes run from 256 to 275: 0x100 is `i8x16.relaxed_swizzle` and 0x113 is `i32x4.relaxed_dot_i8x16_i7x16_add_s`; 0x114–0x12F are reserved. The canonical encodings are the three bytes `fd 80 02` through `fd 93 02`.
- **memory.grow** is `0x40` followed by a memidx, which is also a u32 LEB128. The canonical encoding is `40 00`.
- **A byte scan is unsafe in both directions.**
  - False positives: 0x40 is also the empty block type, and both bytes appear inside LEB128 immediates.
    - The pinned binary's code section has 16,558 bytes equal to 0x40 against one `memory.grow` and 14,916 blocks with the empty type.
    - It has 277 bytes equal to 0xFD against zero SIMD instructions.
    - `i32.const 32893` encodes as `41 fd 80 02`.
  - False negatives: the spec allows padded LEB128. `fd 80 82 80 80 00` is a valid relaxed swizzle that both V8 and wasmparser accept, and a `fd 80 02` pattern misses it. Likewise `40 80 00` is a valid `memory.grow`.
- **The minimal sound lint is an instruction-length decoder.**
  1. Walk the sections by id and u32 size.
  2. Decode the memory section and the limits of imported memories.
  3. In the code section, skip each body's locals, then decode every instruction together with its immediates. Read 0xFC and 0xFD sub-opcodes as u32 LEB128 with any padding.
  4. Refuse ("fail closed") on any opcode the table does not know.
- **`-C target-feature=-relaxed-simd` alone does not guarantee none.**
  - Under that flag, a function-level `#[target_feature(enable = "relaxed-simd")]` still emits `f32x4.relaxed_madd`, and so does a plain call to the `core::arch::wasm32` intrinsic, which carries the attribute itself (measured). On Wasm neither needs `unsafe`.
  - The flag also cannot reach the precompiled std.
  - For the solver today, two crates in the graph carry relaxed-SIMD code: matrixmultiply 0.3.11 (`f32x4_relaxed_madd`) and wide 1.7.1 (`u8x16_relaxed_swizzle`). Both sit only under `#[cfg(target_feature = "relaxed-simd")]`, which the crate-level flag keeps false. Nothing uses a function-level enable or an ungated relaxed call, and the binary has zero 0xFD instructions. So the flag holds today, and it is what keeps those gated paths out. The lint is what guarantees it.

**What I checked.**
- Sources:
  - WebAssembly 3.0 (2026-09-21), binary instructions (https://webassembly.github.io/spec/core/binary/instructions.html):
    - `memory.grow` is `0x40 x:memidx` and `memory.size` is `0x3F x:memidx`.
    - Block type byte `0x40` is the empty type.
    - Vector instructions are `0xFD` plus a u32 opcode.
    - `memarg` bit 6 carries a memidx.
  - WebAssembly 3.0 values (https://webassembly.github.io/spec/core/binary/values.html): a uN takes at most ceil(N/7) bytes and trailing zeros are allowed. The spec's example: `0x03` and `0x83 0x00` both encode 3.
  - WebAssembly 3.0 types (https://webassembly.github.io/spec/core/binary/types.html): limits flags are 0x00 (min), 0x01 (min, max), 0x04 and 0x05 (the same pair for i64 address type).
  - Relaxed-SIMD overview (https://github.com/WebAssembly/relaxed-simd/blob/main/proposals/relaxed-simd/Overview.md): the table from 0x100 to 0x113, with 0x114–0x12F reserved. `relaxed_madd` may round once or twice, host-dependently. The instruction index of the spec itself was cut off at SIMD when I fetched it, so the proposal is the source for the number list.
  - rustc book, wasm32-unknown-unknown (https://doc.rust-lang.org/stable/rustc/platform-support/wasm32-unknown-unknown.html): the default features, and the precompiled std is built with them. Once a function enables SIMD with `#[target_feature(enable = …)]`, there is "no compiler flag to disable emission of SIMD instructions".
  - Rust Reference, codegen attributes (https://doc.rust-lang.org/stable/reference/attributes/codegen.html): safe `#[target_feature]` functions "may always be used in safe contexts on Wasm platforms", and `relaxed-simd` implicitly enables `simd128`.
  - `core::arch::wasm32::f32x4_relaxed_madd` (https://doc.rust-lang.org/stable/core/arch/wasm32/fn.f32x4_relaxed_madd.html): stable since 1.82.0.
  - wasmparser 0.259.0 `OperatorsReader` (https://docs.rs/wasmparser/0.259.0/wasmparser/struct.OperatorsReader.html).
  - WebAssembly design, Nondeterminism.md (https://github.com/WebAssembly/design/blob/main/Nondeterminism.md): relaxed SIMD results are nondeterministic.
- Measured, pinned-binary copy (`wscan`): 1,204 functions and 583,702 decoded operators:
  ```
  SIMD (0xfd-prefixed) instructions: 0
  block/loop/if with empty blocktype …: 14916
  naive scan of code section: bytes==0x40: 16558, bytes==0xfd: 277
  ```
  Its `target_features` section lists only `+bulk-memory +bulk-memory-opt +call-indirect-overlong +multivalue +mutable-globals +nontrapping-fptoint +reference-types +sign-ext`.
- Measured, hand-assembled modules (`node mods.mjs`, which runs `WebAssembly.validate` and executes each module, then `wscan` on each):
  - `i32.const 32893` (`41 fd 80 02`), `i32.const -64` (`41 40`), an empty block (`02 40`) and data bytes all validate. The decoder reports 0 `memory.grow` and 0 relaxed instructions for each.
  - `fd 80 82 80 80 00`: V8 validates it and runs it (`f()=1`); wasmparser decodes it as `I8x16RelaxedSwizzle`.
  - `40 80 00`: V8 validates it; wasmparser decodes it as `MemoryGrow { mem: 0 }`.
  - `fd 94 02`: V8 reports `validate=false`; wasmparser reports `unknown 0xfd subopcode: 0x114`.
- Measured, the `-relaxed-simd` flag (`rustc +1.98.1 --crate-type cdylib --target wasm32-unknown-unknown -C opt-level=3 -C target-feature=-relaxed-simd`):
  - A `#[target_feature(enable = "relaxed-simd")] fn` compiled under the flag, and so did a direct `f32x4_relaxed_madd` call from a plain function.
  - Each binary: `relaxed-SIMD instructions: {"F32x4RelaxedMadd": 1}`, bytes `fd 85 02`, and a `target_features` section with `+relaxed-simd +simd128`. node returns `madd(2,3,1)=7`.
- Graph grep over the wasm32 dependency tree:
  - `#[target_feature(enable=…)]` appears only in matrixmultiply 0.3.11, for `avx`/`avx2`/`avx512f`/`fma`/`neon` kernels (x86 and aarch64).
  - Every wasm SIMD path is under `#[cfg(target_feature = "simd128")]`: glam 0.33.10 `lib.rs:347-350`, wide 1.7.1 `f64x2_.rs:14`, and matrixmultiply `sgemm_kernel.rs:38,72,260`.
  - Relaxed intrinsics appear in exactly two places, both behind `#[cfg(target_feature = "relaxed-simd")]`:
    - matrixmultiply 0.3.11 `src/sgemm_kernel.rs:701-713`: `muladd` becomes `f32x4_relaxed_madd`, otherwise `f32x4_add(f32x4_mul(..))`.
    - wide 1.7.1 `src/u8x16_.rs:707-712`: `shuffle` becomes `u8x16_relaxed_swizzle`.
    Every other "relaxed" hit is `Ordering::Relaxed`, a deprecated `swizzle_relaxed` that forwards to `shuffle`, or documentation. My first grep was cut off by `head -20` and missed wide; the full grep is the one reported here.
- Oracle (PASS):
  - A body with `02 40`, `41 40` and `41 fd 80 02` byte-matches `0x40 x2 | fd 80 02 x1`, but decodes to `memory.grow x0 | relaxed x0`.
  - Eight encodings decode as stated: `40 00`, `40 80 00`, `fd 80 02`, `fd 80 82 80 80 00`, `fd 85 02`, `fd 87 02`, `fd 93 02`, and `fd 94 02` (an error). 0x100..=0x113 decode as relaxed 20/20.
  - Both relaxed builds compile under `-C target-feature=-relaxed-simd` without a warning and return `7`.

**Consequence for T3.**
- **Decoder.** `solver/lint.mjs` needs a small decoder with a complete opcode-immediate table; it does not need a validator. Walk the sections, skip locals, and decode each instruction.
  - Flag `0x40` only at an opcode position, then read a u32 LEB128 memidx.
  - Flag `0xFD` at an opcode position when the u32 LEB128 that follows is between 256 and 275 inclusive. It may be padded up to 5 bytes.
  - Exit 1 on any opcode the table lacks, so a gap in the table can only cause a false refusal.
- **Memory limits.** Refuse when the maximum is absent, or when max ≠ min, in the memory section and in any imported memory.
- **`lint.test.js` (pin 3).** Beyond the three bad modules and the clean one, add these:
  - Accepted, to prove it decodes rather than byte-scans: `i32.const 32893`, `i32.const -64`, an empty `block`, and data bytes `40 fd 80 02`.
  - Refused, to prove it reads LEB128: the padded `fd 80 82 80 80 00` and `40 80 00`.
- **Flags.** Keep `-relaxed-simd` in both flag locations. It is what keeps matrixmultiply's and wide's cfg-gated relaxed paths out if `simd128`, or a CPU level that implies relaxed SIMD, is ever enabled.
- **Signal.** The `target_features` custom section (`+relaxed-simd` / `+simd128`) is a cheap extra signal, but not the check, because custom sections are optional.

**Audit of PR #44 (head b99a636), claim 3: agree.** The PR's `solver/lint.mjs` really decodes:

- It walks the sections and skips each body's locals.
- It decodes every instruction. It reads the memidx after `0x40`, and the `0xFD` and `0xFC` sub-opcodes, as u32 LEB128 of up to 5 bytes.
- It refuses unknown single-byte opcodes and `0xFD` sub-opcodes above 0x113.
- It checks the limits of both defined and imported memories, and refuses any limits flag other than 0x00 or 0x01.

I ran it (`lintWasm`) on my hand-assembled modules:

- Accepted, with no opcode reason: the empty block, `i32.const -64`, `i32.const 32893` and the data bytes.
- Refused, each with the right opcode: canonical relaxed (0x100), padded relaxed (`fd 80 82 80 80 00`), 0x113, `40 00` and `40 80 00`. 0x114 is refused as undecodable. Both rustc-built relaxed modules are refused (`0xfd 0x105`).
- Passed: my two arena builds.

Three gaps, none of which affects rustc output:

1. A `0xFD` sub-opcode below 0x100 that its table does not list is treated as having no immediates instead of being refused. This contradicts its header ("an opcode this decoder does not know is itself a refusal").
2. `table.grow` (`0xFC 15`) is not refused. The profiles appendix and Wasmtime name it alongside `memory.grow` as non-deterministic.
3. `select t*` and reference block types assume one-byte value types.

Its `lint.test.js` already covers the empty-block and `i32.const -64` case and all twenty relaxed opcodes. Add three more cases: `i32.const 32893` (`41 fd 80 02`), the padded `fd 80 82 80 80 00`, and `40 80 00`.

**Contradicts a pin?** No. Pin 2's range, `0xfd` with 0x100 through 0x113, matches the proposal's table, and pin 2 already says the lint "parses" the binary. The byte-scan shortcut from the question is what fails, not a pin.

Pin check: consistent with the pin(s) — 2, 3 of dispatch-t3-platforms.md.

## 7. T4 outcome tests — CCD

**Answer.** CCD is deterministic in every measurement I could make, and it adds no state. But T4's premise is wrong.

**Automatic CCD.** At 0.35.3, CCD is not opt-in. A dynamic body is "fast" when its farthest point moves more than half its thinnest half-extent in one quantum. For T4's 0.05 box at dt = 1/64, that means any speed above 1.6 u/s. Every fast body is swept against fixed colliders, and its end pose is clamped to the first time of impact.

- `ccd_enabled(true)` only widens the targets to kinematic and dynamic bodies: the body becomes a "bullet", and bullets never sweep other bullets.
- `IntegrationParameters::max_ccd_substeps = 0` is the only off switch.

So the law as it stands already keeps T4's box on the near side: 14 of 14 start phases on the engine binary, falling and horizontal. With CCD switched off world-wide, 10 of 14 tunnel. `ccd_enabled(true)` changes nothing against a static slab.

**Determinism.** With `parallel` off, the CCD pass is serial. It walks bodies and targets in arena/BVH order and takes a strict minimum.

- I built a scene of 24 fast, spinning boxes; CCD is active in 2,076 body-quanta, or 2,019 with half of them bullets. It hashes identically on x86-64 release, on x86-64 debug (the oracle), and on wasm32 under V8, and across reruns.
- ARM64 is not determined. T3's ARM lane decides it.

**State.** At the default `max_ccd_substeps = 1`, nothing specific to CCD crosses a quantum.

- The per-body flags and velocities are rewritten after the solve, before they are read.
- The `CCDSolver` holds only a rebuildable cache of fixed targets, which is not serialized.
- The clamp writes the next pose, and the snapshot already records it.
- Swapping in a fresh `CCDSolver` mid-run leaves the hash identical.
- With `max_ccd_substeps > 1`, the pre-solve pass would read the previous quantum's crate-private `ccd_vels`, which a restore cannot set.

**Guarantee.** Rapier states no numeric bound. Measured at dt = 1/64 with 8 phases per cell, nothing tunnelled at speeds from 1 to 1,000 u/s against fixed slabs of half-thickness 0.02 down to 0.0001, with or without `ccd_enabled`. Rapier caps speed at 400 u/s per substep. The source sets four limits:

- a body that already overlaps a target is not clamped;
- non-bullets ignore moving bodies;
- bullets ignore bullets;
- heightfield targets are one-sided.

**What I checked.**
- Sources, rapier3d-f64 0.35.3 (https://docs.rs/crate/rapier3d-f64/0.35.3/source/…):
  - `src/dynamics/ccd/ccd_solver.rs`:
    - 17–25: the doc. Fast dynamic bodies sweep **fixed** colliders; `ccd_enabled` makes a bullet; `max_ccd_substeps = 0` disables CCD.
    - 26–34: `fixed_targets_cache`, under `serde(skip)`.
    - 61–63: "`ccd_enabled` no longer gates *activation*".
    - 328–340: the clamp moves the pose only, and velocities are preserved.
  - `src/dynamics/ccd/sweeps.rs`:
    - 28–42: `is_bullet` and `tier_allows`.
    - 282–283 and 417–419: solid pairs stop only at fractions strictly above 0.
    - 377–384: heightfields are one-sided in 3D.
    - 682–688: the serial map when `parallel` is off.
  - `src/dynamics/rigid_body_components.rs`:
    - 1050–1071: `RigidBodyCcd`. `ccd_active` is set "regardless of `self.ccd_enabled`".
    - 1102–1125: `is_moving_fast` and `FAST_BODY_SAFETY_FACTOR = 0.5`.
  - `src/dynamics/integration_parameters.rs`: 267–271 and 397, `max_ccd_substeps` defaults to 1 and 0 disables all CCD; 390, 395 and 396 give 0.005, 0.02 and 400.
  - `src/pipeline/physics_pipeline/substep.rs`:
    - 339: `ccd_scene_changed`.
    - 405–427: the pre-solve pass runs only when `remaining_substeps > 1`.
    - 496: the post-solve flags.
  - `src/dynamics/solver/staged_island_solver/worker.rs` 844–862: `ccd_vels` and `ccd_active` are written after the solve.
  - `src/pipeline/physics_world.rs` 85–87: `ccd_solver` is "Workspace only: not part of a snapshot".
  - `src/dynamics/rigid_body.rs` 1900–1904: the `ccd_enabled` builder doc.
  - parry3d-f64 0.30.2 `src/shape/shape.rs` 764–766: a cuboid's `ccd_thickness` is `half_extents.min_element()`.
- Other sources:
  - Rapier CHANGELOG at v0.35.3 (https://github.com/dimforge/rapier/blob/v0.35.3/CHANGELOG.md): "Fast dynamic bodies now always run CCD against fixed colliders; `ccd_enabled` upgrades a body to a 'bullet'…" (0.35.0), and "Set `IntegrationParameters::max_ccd_substeps` to `0` to disable CCD entirely."
  - Rapier determinism guide (https://rapier.rs/docs/user_guides/rust/determinism): cross-platform determinism requires IEEE 754-2008 platforms.
- Measured with the engine's own exports (`node drive_fast.mjs <wasm>`). A 0.05 box at 20 u/s against a 0.02 slab, 64 quanta, 7 start phases per direction:

  | build | falling | horizontal |
  |---|---|---|
  | base | all near, rests at y 0.0699 | all near |
  | `ccdoff` (adds `max_ccd_substeps = 0` in `build_world`) | FAR 5/7, e.g. 1.05 → −22.97 | FAR 5/7 |
  | `ccdon` (dynamic bodies `ccd_enabled(true)`) | identical to base | identical to base |

- Envelope (`ccd_matrix.rs` through the oracle, 96 quanta):
  - Engine settings: FAR 0/8 for v ∈ {1, 1.6, 2, 5, 20, 100, 400, 1000} and half-thickness ∈ {0.02, 0.005, 0.001, 0.0001}.
  - CCD off world-wide: FAR 1/8 from 5 u/s on thin slabs, 6/8 at 20, 7/8 at 100 and above.
  - Starting 0.01 inside the slab at 20 u/s: ends at 0.0699, near side.
- Cross-build hash (`ccdprobe`, 240 quanta), printed by the release host binary, by `node` on the wasm32 build, and by the oracle's debug build:
  ```
  bullets=false hash=3eb23b3feb5785fc ccd-active body-quanta=2076 fresh CCDSolver at q100 -> identical
  bullets=true hash=bfe836cfd760e133 ccd-active body-quanta=2019 fresh CCDSolver at q100 -> identical
  ```
- Oracle (PASS):
  ```
  CCD off world-wide (max_ccd_substeps 0): near FAR FAR FAR FAR FAR near
  engine today (ccd_enabled false, substeps 1): near near near near near near near
  T4 pin 2 (ccd_enabled true, substeps 1): near near near near near near near
  ```
  The two hash lines above also pass as an oracle check.

**Consequence for T4.**
- **Fast-body test.** It passes on today's binary. It can go red only with CCD off: `integration_parameters.max_ccd_substeps = 0` in a test-only build or a law flag. For the "shown failing" evidence, use that build: 5 of 7 phases tunnel.
- **Where `ccd_enabled(true)` matters.** Against the kinematic walker, which non-bullets ignore. Since every dynamic body becomes a bullet and bullets skip bullets, dynamic–dynamic sweeps are still not added.
- **Goldens.** They move only if some fast dynamic body meets the walker.
- **Settings.** Keep `max_ccd_substeps = 1` and set it explicitly in `build_world`. If it is ever raised, T2's restore would need the crate-private `ccd_vels`.
- **What the snapshot must carry.** Nothing new. On restore, set `ccd_enabled` from the law, as the builder already does.
- **PR #44's per-quantum rebuild.** PR #44 builds a fresh Rapier world from the snapshot every quantum. That loses no CCD state: a fresh `CCDSolver` mid-run left the hash identical, and at `max_ccd_substeps = 1` the per-body CCD fields are rewritten before they are read.

**Contradicts a pin?** Yes, pin 2 of T4 and the acceptance line. The pin says "At 1/64 s that body moves 0.31 per quantum, so the law as it stands passes through". It does not: automatic CCD against fixed colliders is on at 0.35.3. So "the fast-body test is shown failing on the binary before pin 2" cannot be produced from that binary.

Pin check: contradicts pin 2 of dispatch-t4-outcome-tests.md because rapier3d-f64 0.35.3 already sweeps every fast dynamic body against fixed colliders with ccd_enabled(false), so today's law keeps the box on the near side (14/14 engine runs), rapier3d-f64-0.35.3/src/dynamics/ccd/ccd_solver.rs:17-25.

## 8. T4 outcome tests — the character controller

**Answer.** The exact comparisons at 0.35.3 are grouped below, with what the engine binary does at each limit. All measurements use the product walker, a 0.25 box.

**Autostep.**

- It runs only when the hit is a "wall": the angle between the surface normal and up is at least `max_slope_climb_angle`, an inclusive `>=`.
- With `include_dynamic_bodies = false`, it never steps onto a collider whose parent body is dynamic. Dynamic bodies are also excluded from the step's own casts.
- Its limits are `max_height + offset` and `min_width + offset`: 0.31 and 0.21 for the engine. Shape casts that stop at `offset` check them:
  1. the character must fit when raised by `max_height + offset`;
  2. it must then fit moved forward by `min_width + offset`;
  3. the landing must not be steeper than the climb angle, a strict `>`.

Measured, steps up to 0.31010 are climbed at both 0.4 and 2 u/s. 0.31 is climbed and 0.311 is not. The feet always rest 0.0100–0.0101 above the surface, never on it.

**Slopes.**

- `is_wall` uses `>=`.
- `is_nonslip_slope` compares against `min_slope_slide_angle` with an inclusive `<=`.
- 44° and 44.9° are climbed; 45.1° through 52° are refused.
- Exactly 45° creeps upward: 0.17 in 160 quanta. Do not test at the limit.
- A refused 46° slope still gains height from the 1e-4 normal nudge: about 6e-5 per quantum at 2 u/s, 0.038 by 640 quanta and 0.077 by 1,280.

**Snap.**

- It applies only when the walker was grounded at the start of the move, meaning it had a contact within `offset + 0.05` whose normal·up ≥ 1e-3.
- The resulting translation must not be upward: `translation·up <= 0`.
- It then casts down by `snap`, with `offset` as the target distance.
- At a ledge, at 0.4 and 2 u/s, the walker is ungrounded for one quantum and a 0.19 drop lands on the lower floor two quanta after clearing the edge. At 1 u/s the 0.18 and 0.19 drops show no ungrounded quantum, and 0.19 lands one quantum after the edge.
- The fall threshold depends on speed: 0.2105 at 0.4 u/s, 0.2097 at 1 u/s, 0.2058 at 2 u/s. So a 0.21 drop is snapped at the product walker's 0.4 u/s.

**Start inside geometry.** A walker started 0.1 inside the floor rises only by the nudge, 1e-4 per quantum; its feet reach the floor after about 1,200 quanta. Rapier depenetrates only when the desired movement is zero, and the engine always passes gravity.

**What I checked.**
- Sources, `rapier3d-f64-0.35.3/src/control/character_controller.rs` (https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/control/character_controller.rs):

  | lines | what they hold |
  |---|---|
  | 176–221 | fields and `Default` |
  | 313–324 | depenetrate "only when there is no desired movement" |
  | 328–336 and 442–451 | snap runs only if grounded at the start |
  | 466 | `result.translation.dot(self.up) <= 0.0` |
  | 469–479 | down cast with `max_time_of_impact: snap_distance` and `target_distance: offset` |
  | 491–493 | `predict_ground` = offset + 0.05 |
  | 612 | `normal.dot(self.up) >= 1.0e-3` |
  | 646–658 | slope handling, nudge added along the hit normal |
  | 673 | `is_wall = angle_with_floor >= self.max_slope_climb_angle && !is_ceiling` |
  | 674 | `is_nonslip_slope = angle_with_floor <= self.min_slope_slide_angle` |
  | 736–739 | autostep only on walls |
  | 742–743 | `min_width = … + offset`, `max_height = … + offset` |
  | 745–759 | `include_dynamic_bodies` |
  | 772–806 | up and forward casts |
  | 836 | `climbing && angle_with_floor > self.max_slope_climb_angle` |
  | 842–859 | step height |

- Other sources:
  - docs.rs `KinematicCharacterController` (https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/control/struct.KinematicCharacterController.html): `offset` is "a small gap to preserve", and `normal_nudge_factor` is "a small distance applied to the movement toward the contact normals".
  - docs.rs `CharacterAutostep` (https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/control/struct.CharacterAutostep.html).
  - Rapier CHANGELOG at v0.35.3: snap-to-ground "now triggers on any movement that isn't upwards".
- Measured, through the engine's own exports. The walker has `DRIVEN` = 1 and shape 0 and starts at y 0.26 on a floor whose top is 0.
  - **Steps** (`node drive_course.mjs <wasm> step`): the bisection prints `climbed at 0.3100989` at 0.4 u/s and `0.3100939` at 2 u/s. The stopped walker ends at x 10.7399, with its face 0.0101 short of the riser.
  - **Slopes** (`node drive_course.mjs <wasm> slope` and `node creep.mjs <wasm>`): the ramp is a 1.4-half-length rotated cuboid whose top face starts at floor level.
    - 44°: gain 1.945 at 2 u/s, reaching the top.
    - 45°: 0.169 after 160 quanta.
    - 46° at 2 u/s: q320 0.018, q640 0.038, q1280 0.077, q10000 0.611. At 0.4 u/s: q1280 0.042, q2560 0.088.
  - **Drops** (`node trace_drop.mjs`, `node drop2.mjs`): at 0.4 and 2 u/s, the quantum that clears the edge shows feet 0.0101 and vy −0.125 for every drop. Longest ungrounded runs:

    | drop | 0.4 u/s | 1 u/s | 2 u/s |
    |---|---|---|---|
    | 0.18 | 1 | 0 | 1 |
    | 0.19 | 1 | 0 | 1 |
    | 0.21 | 1 | 11 | 12 |
    | 0.22 | 12 | 12 | 12 |
    | 0.23 | 12 | 12 | 12 |

    Bisected thresholds: 0.210538, 0.209666 and 0.205759.
  - **Start inside by 0.1**: feet −0.0936 at q64, −0.0360 at q640, +0.0101 at q1280. The minimum is −0.0999, never below the start.
  - **Mechanism** (the `nudge0` build, with `normal_nudge_factor` set to 0): the creep is 0 at 45.1°, 46° and 50°, and the start-inside walker stays at −0.1000. With the nudge at 0, the walker also sticks: it climbs nothing. So the nudge is the cause, and it is needed.
- Oracle (PASS). A native copy of `integrate()` for one walker, run on the oracle's Rapier, reproduces the wasm numbers:
  ```
  step 0.31 at 2 u/s: climbed, feet 0.0100 above the step top
  step 0.311 at 2 u/s: stopped, feet 0.0100 above the floor
  44 deg … max gain 1.954 | 45 deg … 0.341 | 46 deg, 320 quanta … 0.018 | 46 deg, 1280 quanta … 0.077
  drop 0.21 at 0.4 u/s: longest ungrounded run 1 quanta | drop 0.21 at 2 u/s: … 12 quanta | drop 0.22 at 0.4 u/s: … 12 quanta
  start 0.1 inside, vx 0.4: feet q64 -0.0936, q640 -0.0360, q1280 0.0101
  ```

**Consequence for T4 (`harness/course.test.js`).** In every case, feet = `y − hy − SKIN`.

- **Step.** Use 0.29 and 0.33, or 0.30 and 0.32, around the real limit of `max_height + offset` = 0.3101.
  - Assert the feet at the step top, or at the floor, within 1e-3.
  - The stopped walker's face stays at least `SKIN` short of the riser.
- **Slope.** Use 44° and 46°, with the speed and quantum count written into the test.
  - At 2 u/s over at most 640 quanta, 46° gains less than 0.05 while 44° gains more than 1.
  - Measure the maximum height reached, or put a landing at the ramp's top. Past the top the walker walks off, and its end height falls back to the floor.
  - At 0.4 u/s, allow at most 1,280 quanta for the 46° case.
  - Never test exactly 45°.
- **Drop.** Use 0.19 and 0.22.
  - 0.19: the longest ungrounded run is at most 1, and the feet reach the lower floor within 2 quanta of clearing the edge.
  - 0.22: the longest ungrounded run is at least 2. It was 12 at 0.4, 1 and 2 u/s.
  - "Grounded on the next quantum" depends on speed: true at 1 u/s, false at 0.4 and 2 u/s.
- **Start inside.** Give it at least 1,300 quanta and assert the feet never go below their start. Alternatively, assert the recovery rate.
- **Record the speed.** Thresholds move with speed; 0.4 u/s is the product walker's speed.
- **Constants.** None of this changes the controller's constants, which T4 forbids.

**Contradicts a pin?** Yes, pin 5 of T4 (numbered the same on `main` after the amendment), in five places:

- The 0.31 step is climbed, not stopped.
- "Feet … within 1e-3" of the step top fails by the 0.01 skin.
- At 0.4 and 2 u/s the 0.19 walker is not grounded on the quantum after the edge. At 1 u/s it is.
- At the product walker's 0.4 u/s, the 0.21 drop is snapped, not a fall. Both 0.19 and 0.21 show exactly one ungrounded quantum.
- The 46° gain stays below 0.05 only for a bounded run. The start-inside walker needs about 1,200 quanta to stand.

The 44°/46° pair itself is on the right side of both slope comparisons.

Pin check: contradicts pin 5 of dispatch-t4-outcome-tests.md because autostep's limit is max_height + offset (a 0.31 step is climbed; measured limit 0.3101), feet rest one offset above surfaces, and a 0.21 drop is snapped at 0.4 u/s, rapier3d-f64-0.35.3/src/control/character_controller.rs:742-743.
