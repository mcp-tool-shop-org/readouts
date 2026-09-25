# Concurrency, parallelism & async (wave 2, advanced)

**Q1. What do Send and Sync guarantee, and which primitive fits which job?** They are compiler-inferred auto traits that turn data races into compile errors (E0277, E0499), but race conditions and deadlocks stay your problem. Use Mutex for exclusive state, RwLock for read-mostly state, `Condvar::wait_while` to wait on a predicate, channels to hand results over, atomics for flags and counters, and LazyLock / OnceLock for one-time globals.

**Q2. Where does parallelism break bit-exact determinism, and where is async appropriate at all?** Parallelism breaks it wherever float association or result order follows scheduling: parallel reductions, channel arrival order, thread count. Async fits I/O-bound host and tool code, never the CPU-bound law.

1. **Safe Rust rejects data races, not race conditions or deadlocks.** Rust project 2026 (The Rustonomicon: Data Races and Race Conditions, https://doc.rust-lang.org/nomicon/races.html). Implication: make every check-then-act one atomic read-modify-write or one locked section; the oracle loses an update with safe atomics.

2. **A `static` must be Sync; a `static mut` is exempt.** Rust project 2026 (The Rust Reference: Static items, https://doc.rust-lang.org/reference/items/static-items.html). Implication: the solver's `static mut` BODIES, COLLIDERS, HEIGHTS and SOLVER were never thread-checked. A native Godot or Unreal build puts them in `static LAW: Mutex<Option<Loaded>>` and each export returns 0 when `try_lock` fails. That compiles because rapier3d-f64 0.35.3's PhysicsWorld is Send + Sync (oracle).

3. **Parallel float sums are not reproducible under rayon.** rayon maintainers 2026 (rayon 1.12.0 ParallelIterator, https://docs.rs/rayon/1.12.0/rayon/iter/trait.ParallelIterator.html). Implication: tools that aggregate floats across runs (T5, T6) fix a chunk size and fold the partials in index order. The oracle gets identical bits for 1 to 6 threads, but not the plain sequential sum's bits.

4. **Rapier 0.35 says `parallel` plus `enhanced-determinism` is bitwise identical for any thread-pool size.** Dimforge 2026 (rapier CHANGELOG, v0.35.0-beta.0 entry, https://github.com/dimforge/rapier/blob/v0.35.3/CHANGELOG.md). Implication: the old "incompatible" advice is stale, but the claim is the vendor's and nobody here has measured it. Keep `parallel` off in the wasm law, and re-measure the golden hash at several pool sizes before any native host turns it on.

5. **wasm32-unknown-unknown has no threads on stable.** Rust project 2026 (rustc book: wasm32-unknown-unknown, https://doc.rust-lang.org/rustc/platform-support/wasm32-unknown-unknown.html). Implication: `thread::spawn` panics there, and the oracle shows `+atomics` with `--shared-memory` failing to link against the shipped std and core. Threads would need nightly build-std, for no gain.

6. **Rapier's PhysicsHooks and EventHandler must be Sync even with `parallel` off.** Dimforge 2026 (rapier CHANGELOG at v0.35.3, https://github.com/dimforge/rapier/blob/v0.35.3/CHANGELOG.md). Implication: a hook that holds state uses atomics, not Cell (E0277 in the oracle). Turning on `unsync-callbacks` is a feature change, and so a new artifact.

7. **With several producers, channel messages arrive in scheduling order.** Rust project 2026 (The Book ch. 16.2, https://doc.rust-lang.org/book/ch16-02-message-passing.html). Implication: sweep tools send `(run_index, hash)` and sort before writing the report.

8. **Release/Acquire publishes data, and x86 hides orderings that are too weak.** Rust project 2026 (The Rustonomicon: Atomics, https://doc.rust-lang.org/nomicon/atomics.html). Implication: run host and tool concurrency tests on the T3 ARM64 lane.

9. **Futures are inert state machines, and the "future cannot be sent between threads safely" error has no error code.** Rust project 2026 (std::future::Future, https://doc.rust-lang.org/stable/std/future/trait.Future.html). Implication: the law stays synchronous; a tokio host calls it through `spawn_blocking` and scopes any std MutexGuard before `.await`, since on 1.98.1 `drop(g)` fails once the guard was used (oracle).

10. **Dropping a tokio JoinHandle detaches the task, and spawn_blocking work cannot be aborted.** Tokio project 2026 (tokio 1.53.1 JoinHandle, https://docs.rs/tokio/1.53.1/tokio/task/struct.JoinHandle.html). Implication: cancel with `abort()`; a blocking law call never stops early.

Thin evidence: Rapier's bitwise `parallel` claim is unmeasured here, and the ARM64 ordering risk comes from the Rustonomicon, not a test.
