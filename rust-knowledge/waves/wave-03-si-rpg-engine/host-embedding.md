# host-embedding — Embedding the Rust law in hosts (JS, Godot, Unreal)

Wave 3, tier si-rpg-engine, retrieved 2026-09-25. 17 compile checks pass under rustc 1.98.1.

**Q1 — Ways to run the law in Godot 4 and Unreal 5.**
- **A: run the pinned .wasm in an embedded runtime.** Keeps one artifact and one digest.
- **B: compile the law natively** (gdext cdylib; Unreal staticlib + cbindgen). Adds a second artifact per target, which matches the wasm on basic ops but not on every dependency math call.
- **C: build a WIT component.** A new target, a new pin and a copying ABI.

None of the three carries the JavaScript tick and frame hash along.

**Q2 — Runtimes and determinism settings.** Wasmtime 49.0.1 (LTS 48.0.3), Wasmer 7.4.2, WAMR 2.4.5 and wasm3 0.9.0 can load an import-free module that uses no SIMD. Set these explicitly, because defaults and fuel accounting change between releases:
- NaN canonicalization on
- relaxed SIMD off
- threads off
- deterministic memory growth
- fuel, not epochs, for any watchdog

1. **The law imports nothing.** W3C 2026 (WebAssembly JavaScript Interface, https://webassembly.github.io/spec/js-api/). Instantiating a module that has imports without an import object throws TypeError, so build.mjs succeeding proves the law has none. Implication: verify fixtures/solver.sha256, then call `Instance::new(&mut store, &module, &[])`, and re-derive memory offsets after every call.
2. **Wasmtime's defaults are not deterministic.** Bytecode Alliance 2026 (Config, https://docs.rs/wasmtime/49.0.1/wasmtime/struct.Config.html). NaN canonicalization is off by default, and 49.0.0 and 49.0.1 both changed fuel accounting. Implication: set the knobs in code, pin LTS 48.0.x, and keep fuel out of the hash.
3. **Cranelift needs run-time executable pages; Pulley does not.** Bytecode Alliance 2026 (Platform Support, https://docs.wasmtime.dev/stability-platform-support.html). Implication: choose the runtime per platform, and prove aarch64 hosts on T3's ARM64 lane.
4. **godot-wasm runs Wasmtime on `wasm_engine_new()` defaults.** ashtonmeuser 2026 (godot-wasm, https://github.com/ashtonmeuser/godot-wasm). Implication: own the Config in a gdext extension, or use JavaScriptBridge in Web exports.
5. **gdext 0.5.5 loads in any Godot at or above its API version (4.2+).** godot-rust 2026 (Compatibility, https://godot-rust.github.io/book/toolchain/compatibility.html). Implication: ship one cdylib per platform. Godot's `real` is f32, so never write Godot poses back into the law.
6. **enhanced-determinism does not reroute inherent std math in dependencies.** Dimforge 2026 (glamx eigen3.rs, https://docs.rs/crate/glamx/0.3.1/source/src/eigen3.rs). Inertia that is not diagonal goes through `acos`/`cos`, which compound bodies and convex hulls will reach. Implication: gate each native build with T1. Basic ops matched: identical bits natively and in wasm.
7. **Two Rust staticlibs in one binary are likely to conflict.** Rust Project 2026 (Reference: Linkage, https://doc.rust-lang.org/stable/reference/linkage.html). Implication: for Unreal, build one staticlib that embeds wasmtime and exposes a 136-byte `#[repr(C)]` record.
8. **Components cannot share memory; values cross by copy.** Bytecode Alliance 2026 (Why the Component Model?, https://component-model.bytecodealliance.org/design/why-component-model.html). Implication: option C restarts the pin and the T1 baseline.
9. **Rapier handlers must be Sync, and the law holds one world per instance.** Dimforge 2026 (MaybeSync, https://docs.rs/rapier3d-f64/0.35.3/rapier3d_f64/utils/trait.MaybeSync.html). Implication: run one instance per world on one thread, and drain events from a Mutex buffer. Traffic is 22,528 B per quantum.
10. **Hosts are accepted by trace equality.** si-rpg-engine 2026 (trace-line.mjs, https://github.com/mcp-tool-shop-org/si-rpg-engine/blob/f84c98b35c6707a10c8ddcb99caf505efc02e6af/harness/trace-line.mjs). Implication: compare `{:016x}` bits, never decimals.

**Thin evidence.**
- **Consoles:** no retrieved page shows a runtime or a Rust binding on a console SDK.
- **gdext with wasmtime:** combining them in one extension is an inference.
- **wasm3:** its README says it is in minimal maintenance.
- **The tick and hash:** where they run in a host is still undecided.
