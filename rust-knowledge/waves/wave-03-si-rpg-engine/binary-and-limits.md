# binary-and-limits: binary lint, CCD and controller limits (wave 3, si-rpg-engine)

**Q5. Memory.** Fix it with `-C link-arg=--no-growable-memory`, or equal page-aligned `--initial-memory`/`--max-memory`. Link args alone leave std's single `memory.grow` in the binary; a fixed-arena `#[global_allocator]` removes it. Today's content needs 21 pages; dense worlds at the caps need up to 245. Use 512.

**Q6. Opcodes.** Relaxed SIMD is `0xFD` plus a u32 LEB128 opcode from 256 to 275. `memory.grow` is `0x40` plus a memidx. Both can be padded, and both bytes also occur inside immediates, so the lint must decode instructions. `-relaxed-simd` does not guarantee absence.

**Q7. CCD.** Hashes match on x86-64 and wasm32. At `max_ccd_substeps = 1` CCD carries no state. It already sweeps fast bodies against fixed colliders, so T4's thin slab holds today.

**Q8. Controller.** Autostep's limit is `max_height + offset` (0.3101). Walls start at `>=` the climb angle and landings fail at `>` it. Snap requires a grounded start and a move that is not upward; its threshold moves with speed.

## Findings

1. **Link limits keep the instruction.** Rust Project 2026 (std sys/alloc/wasm.rs at 1.98.1, https://github.com/rust-lang/rust/blob/1.98.1/library/std/src/sys/alloc/wasm.rs). Every fixed-memory build kept one `memory.grow`, in dlmalloc's `System::alloc`. Implication: give dlmalloc a fixed arena through `Dlmalloc::new_with_allocator`. That build had zero grows and unchanged goldens.
2. **Fixing memory makes an overflow trap identically on every host, but the size must follow contacts.** Wasmtime 2026 (Deterministic Wasm Execution, https://docs.wasmtime.dev/examples-deterministic-wasm-execution.html). Measured peak pages, today's law then PR #44's: pile 49 then 53, dense 147 then 245, all-overlapping 3,320 then 3,973. Implication: PR #44's 256 pages leaves 4% on the dense scene. Use 512 and add a dense-scene test.
3. **Byte scans misfire both ways.** WebAssembly CG 2026 (Binary Format: Values, https://webassembly.github.io/spec/core/binary/values.html). The binary contains 16,558 `0x40` bytes but one `memory.grow`, and the padded `fd 80 82 80 80 00` is a valid relaxed instruction. Implication: decode with a table that refuses unknown opcodes, as PR #44's lint does, and add padded cases to its tests.
4. **The feature flag is not a guarantee.** Rust Project 2026 (rustc book, wasm32-unknown-unknown, https://doc.rust-lang.org/stable/rustc/platform-support/wasm32-unknown-unknown.html). Under the flag, both a `#[target_feature]` fn and a plain intrinsic call emitted `fd 85 02`. Implication: keep the flag, which gates matrixmultiply's and wide's relaxed `cfg` paths, and trust the lint.
5. **CCD is on by default for fast bodies.** dimforge 2026 (CHANGELOG v0.35.3, https://github.com/dimforge/rapier/blob/v0.35.3/CHANGELOG.md). The engine's current law kept 14/14 runs on the near side. With `max_ccd_substeps = 0`, 10/14 tunnelled. Implication: T4 pin 2's red run needs `max_ccd_substeps = 0`; `ccd_enabled(true)` only adds moving targets.
6. **One CCD substep carries no state.** dimforge 2026 (physics_world.rs source, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/pipeline/physics_world.rs). Swapping in a fresh `CCDSolver` mid-run left the hash unchanged. Implication: pin `max_ccd_substeps = 1`. Restore needs nothing new, and PR #44's per-quantum rebuild loses nothing.
7. **A 0.31 step is climbed.** dimforge 2026 (character_controller.rs source, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/control/character_controller.rs). `handle_stairs` adds the offset to both limits, and feet rest 0.01 above surfaces. Implication: use course steps of 0.29 and 0.33, with feet = y − hy − skin.
8. **Snap and slope limits move with speed and time.** dimforge 2026 (the same source). At 0.4 u/s a 0.21 drop snaps; at 2 u/s it falls. A walker blocked by a 46° slope creeps up 6e-5 per quantum. A walker started 0.1 inside the floor needs about 1,200 quanta to stand. Implication: use drops of 0.19 and 0.22, bound the slope runs, never test at exactly 45°, and state the speed.

Thin evidence: ARM64 is unmeasured. No fixed size covers every world the 64/64/256 caps admit. Where PR #44's golden move comes from is inferred.
