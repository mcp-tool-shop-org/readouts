# types-patterns: structs, enums & pattern matching (wave 1, essentials)

**Q1. How do enums and exhaustive matching make illegal states unrepresentable?** Each variant carries only its own data and `match` must name every variant (E0004). So mode 4.0, mode 1.5, NaN or "kinematic without a handle" cannot be built, and a new variant breaks every match that must decide about it. A `_` arm switches that protection off.

**Q2. Which pattern features changed recently?** In release order:

- let-else: 1.65, every edition.
- Exclusive range patterns: 1.80.
- Let chains: 1.88, edition 2024 only.
- Edition 2024: `mut`/`ref`/`&` inside an implicitly borrowing pattern became hard errors.
- if-let guards: 1.95, every edition, not counted toward exhaustiveness.

1. **Body slot 16 is read two ways, and neither reader refuses an unknown value.** si-rpg-engine 2026 (solver/src/lib.rs and rapier_law.rs at e5fbcb9, https://github.com/mcp-tool-shop-org/si-rpg-engine/blob/e5fbcb9/solver/src/rapier_law.rs). `step()` treats any non-zero value, NaN included, as driven. `signature()` treats 4.0, 1.5 and NaN as dynamic. Implication: decode the slot once, at the export edge, into `enum SolverMode` through `TryFrom<u32>`. Before that, require an exact round trip, `f64::from(x as u32) == x`. Return 0 for anything else.

2. **`as` truncates and saturates without saying so; From and TryFrom do not.** Rust Reference 2026 (Operator expressions, https://doc.rust-lang.org/stable/reference/expressions/operator-expr.html). Implication: `SolverMode::try_from(x as u32)` accepts 1.5 as Kinematic and NaN as Dynamic (compiler-checked). std has no `From<u32> for usize` and no `From<u64> for f64`.

3. **A `_` arm quietly gives every later variant the default.** Rust Book 2026 (6.2 match, https://doc.rust-lang.org/stable/book/ch06-02-match.html). Implication: write no `_` on the solver's own enums. rapier3d-f64 0.35.3 does not mark RigidBodyType `#[non_exhaustive]`, so a `_`-free match over it turns a Rapier bump that adds a variant into a compile error.

4. **Edition 2024 rejects `mut`, `ref` and `&` inside implicitly borrowing patterns.** Rust Edition Guide 2026 (Match ergonomics reservations, https://doc.rust-lang.org/edition-guide/rust-2024/match-ergonomics.html). Implication: the edition-2021 solver shows no `rust_2024_incompatible_pat` sites (measured on a scratch copy), so its patterns will not block an edition move.

5. **Let chains need edition 2024; if-let guards do not.** Rust Blog 2025 (Announcing Rust 1.88.0, https://blog.rust-lang.org/2025/06/26/Rust-1.88.0/); Rust Blog 2026 (Announcing Rust 1.95.0, https://blog.rust-lang.org/2026/04/16/Rust-1.95.0/). Implication: on the pinned 1.98.1 the edition-2021 solver can use let-else (already its refusal idiom) and if-let guards, but not let chains.

6. **The capacity check before `n_bodies as usize` protects the indices and the u64 masks.** si-rpg-engine 2026 (lib.rs, https://github.com/mcp-tool-shop-org/si-rpg-engine/blob/e5fbcb9/solver/src/lib.rs). Implication:
   - `u32 as usize` cannot truncate on wasm32.
   - Without the check, body 64 indexes past the 1,088-slot buffer.
   - With overflow checks off, `1u64 << 64` is 1, measured on the host and on wasm32. Keep MAX_BODIES at 64 or below, or widen the masks.
   - T2's `solver_restore(.., len)` needs the same bounds on `len` and on the counts stored in the snapshot as f64.

7. **Newtypes catch transposed u32 parameters; type aliases do not.** Rust Book 2026 (20.3 Advanced Types, https://doc.rust-lang.org/stable/book/ch20-03-advanced-types.html). Implication: wrap `rows`, `cols` and the counts right after entry to `solver_load`/`solver_step`, and keep the wasm signature plain.

8. **Associated consts are evaluated only when something references them.** Rust Reference 2026 (Associated items, https://doc.rust-lang.org/stable/reference/items/associated-items.html). Implication: an ABI assertion in an associated const that nothing references never fires. Unreferenced, it produces only a dead_code warning.

**Where the evidence is thin.** Three points rest on measurement alone:

- Float literal patterns match -0.0 with a `0.0` arm, and `1u64 << 64` is 1 with overflow checks off. No retrieved page states either; only the compiler shows them.
- The zero-site edition result came from a scratch compile outside the oracle, so the lane file cannot rerun it.
