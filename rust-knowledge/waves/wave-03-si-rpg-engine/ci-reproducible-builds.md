# ci-reproducible-builds — Rust CI, reproducible binaries & supply chain (wave 3)

**Q1: What makes a Rust→wasm build byte-reproducible, and what still differs between hosts?**
On one host OS and CPU, the same rustc 1.98.1, Cargo.lock, rustflags, package version and crate-type, plus a CARGO_HOME remap, give one digest: four checkout paths matched (measured). Between hosts, path separators *and* Cargo's host-unit metadata change the bytes, and nothing on stable 1.98.1 removes the second.

**Q2: Which Rust-side CI jobs should si-rpg-engine add, and how are bumps governed?**
Inside ci.yml:
- an explicit toolchain install and a `--locked` build;
- fmt, clippy `-D warnings`, `cargo test --lib`, a feature guard and cargo deny;
- the ARM lane on the x64 artifact, verified by hash.

In a weekly scheduled file: advisories, an uncached rebuild, Miri and mutants. Every toolchain, lock, version or crate-type bump re-pins from x86_64 Linux CI.

1. **Only the cargo-home remap moves bytes.** The build.mjs, cargo-home-only and reversed-order builds were identical (b21c7f15…); without a remap, 132 strings name the user's cargo home. rust-lang 2026 (rustc book: Remap source paths, https://doc.rust-lang.org/rustc/remap-source-paths.html). Implication: add a post-build scan for leaked paths, and keep rust-src off the pinned toolchain.

2. **Cargo leaks the build host into wasm crates.** Proc-macros and build scripts hash the host line, and a unit mixes in its dependencies' metadata. rust-lang/cargo 2026 (compilation_files.rs at rust-1.98.0, https://github.com/rust-lang/cargo/blob/rust-1.98.0/src/cargo/core/compiler/build_runner/compilation_files.rs). Changing only the host units' profile reordered the code, data and name sections, even in a stripped build; normalising separators did not reproduce the Linux pin (both measured). Implication: re-pin only from x86_64 Linux, and gate build.mjs on `process.arch === 'x64'`.

3. **aarch64 vs x86_64 Linux: different bytes, thinly evidenced.** The evidence is one user report on cargo#8140 (2026-07-31) plus the mechanism; the fix is still a draft. rust-lang/cargo 2025 (PR #15477, Only hash host-independent host-dependency metadata, https://github.com/rust-lang/cargo/pull/15477). Not measured here. Implication: T3's ARM lane runs the x64 artifact and checks sha256(bytes) against fixtures/solver.sha256.

4. **trim-paths is still nightly; `--remap-path-scope` is stable since 1.95.0.** rust-lang 2026 (Cargo Book: Unstable features, https://doc.rust-lang.org/cargo/reference/unstable.html). Implication: no stable profile setting makes Windows bytes match; the Windows digest stays informational.

5. **An inherited CARGO_ENCODED_RUSTFLAGS silently erases build.mjs's flags, and the relaxed-SIMD pin leaves no trace in the bytes.** rust-lang 2026 (Cargo Book: Configuration, https://doc.rust-lang.org/cargo/reference/config.html). Implication: set CARGO_ENCODED_RUSTFLAGS in build.mjs and add a cfg `compile_error!` guard. The guard cannot see `#[target_feature]` functions, so keep T3's lint.

6. **rustup auto-installs a pinned toolchain by default; rustup 1.30 narrows that only for its own subcommands.** rust-lang 2026 (rustup CHANGELOG, https://raw.githubusercontent.com/rust-lang/rustup/main/CHANGELOG.md). Implication: run an explicit `rustup toolchain install --no-self-update` in solver/ and drop the second pin in the dtolnay step.

7. **rust-cache never sees build.mjs's flags and skips the save on a full hit.** Swatinem 2026 (rust-cache src/config.ts, https://github.com/Swatinem/rust-cache/blob/master/src/config.ts); CI run 36121826863 confirms both. Implication: add `--locked`, and hash build.mjs into the key.

8. **`-D warnings` fails on today's solver (seven static_mut_refs warnings).** rust-lang 2026 (Edition Guide: static mut references, https://doc.rust-lang.org/edition-guide/rust-2024/static-mut-references.html). Implication: fix those sites, then gate with fmt, clippy for wasm32 and `cargo test --lib`. Adding "rlib" for integration tests moves the digest.

9. **`solver_clear_warmstart`'s &T→&mut cast evades invalid_reference_casting.** rust-lang 2026 (rustc lints: invalid_reference_casting, https://doc.rust-lang.org/rustc/lints/listing/deny-by-default.html). Implication: run a date-pinned nightly Miri job; the restore-internals lane owns the fix. Miri was not run here (no nightly on the rig).
