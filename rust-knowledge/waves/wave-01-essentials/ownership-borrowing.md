# Ownership, moves & borrowing: wave 1 packet (essentials)

**Q1. Which borrow-checker errors will a builder hit most, and what is the fix?** Frequency data is thin. One 2022 study of 100 Stack Overflow questions traced 77 of 118 violations to lifetime computation and 41 to the move and borrow rules. Fix by code:
- E0382/E0505 (moves): borrow, reorder, or clone on purpose.
- E0499/E0502/E0506/E0503 (aliasing): end the first borrow earlier.
- E0597/E0716/E0515 (the owner dies first): bind the owner outside, or return owned data.
- E0507: `mem::take` or `mem::replace`.

**Q2. When does a signature need explicit lifetimes?** When a returned reference has no single source: two reference inputs without `self`, no reference input at all, or a reference stored in a struct (E0106). Elision covers one reference input, or a `&self`/`&mut self` receiver.

Findings. All 74 checks pass under rustc 1.98.1.

1. **Only implicit borrows are two-phase.** rustc-dev-guide 2026 (Two-phase borrows, https://rustc-dev-guide.rust-lang.org/borrow-check/two-phase-borrows.html). Implication: `v.push(v.len())` compiles, but `Vec::push(&mut v, v.len())` is E0502, and indexing activates the borrow at once. Move such arguments into locals first.

2. **A `&mut` passed to a generic parameter is moved, not reborrowed, and this is still open upstream.** rust-lang 2026 (Passing a mutable reference to a generic function doesn't reborrow, https://github.com/rust-lang/rust/issues/162690). Implication: `step()`'s `let bodies = &mut BODIES` stays usable across calls only because `field` and `resolve_pair` take a concrete `&mut [f64]`. A generic Phase-2 helper needs `&mut *bodies`.

3. **On the pinned compiler, NLL still rejects returning a borrow on one path and mutating on another.** Rust Blog 2026 (Enabling the next iteration of the borrow checker on nightly, https://blog.rust-lang.org/2026/08/04/enabling-polonius-alpha-on-nightly/). Implication: Polonius Alpha is on nightly only, so a nightly snippet can fail on 1.98.1. Check first without holding the borrow, or use `entry()`.

4. **`get_disjoint_mut` has been stable since 1.86 and `as_chunks_mut` since 1.88.** Rust std docs 2026 (primitive slice, https://doc.rust-lang.org/stable/std/primitive.slice.html). Implication: `resolve_pair` copies values out, so it needs no split. A rewrite that holds two rows at once uses `as_chunks_mut::<BODY_STRIDE>()` then `get_disjoint_mut([i, j])`. Two live `field()` results are E0499.

5. **A `&mut self` method borrows all of `self`, and view types are only a 2026 experiment.** Rust Project Goals 2026 (The Borrow Checker Within, https://goals.rust-lang.org/2026/roadmap-borrow-checker-within.html). Implication: `integrate()` destructures `&mut PhysicsWorld` into separate field borrows; keep it that way. `&mut self` getters on a wrapper would be E0499.

6. **In edition 2021, temporaries in a block's tail expression outlive the block's locals.** Rust Edition Guide 2026 (Tail expression temporary scope, https://doc.rust-lang.org/edition-guide/rust-2024/temporary-tail-expr-scope.html). Implication: `solver/` is edition 2021, so a guard created in a tail expression is E0597 there. Bind the result to a local first.

7. **`mismatched_lifetime_syntaxes` warns by default since 1.89.** Rust Blog 2025 (Announcing Rust 1.89.0, https://blog.rust-lang.org/2025/08/07/Rust-1.89.0/). Implication: a helper that returns an iterator writes `Iter<'_, f64>`.

8. **Array elements are borrowed as a whole, while tuple and struct fields split.** Zhu et al. 2022 (Learning and Programming Challenges of Rust, https://songlh.github.io/paper/survey.pdf). Implication: to lend two elements of one array, use `split_first_mut` or `split_at_mut`, not two index expressions.

9. **Moving a value out from behind `&mut` needs `take` or `replace`, but rustc's E0507 help offers only `&` or `.clone()`.** Rust std docs 2026 (std::mem::take, https://doc.rust-lang.org/stable/std/mem/fn.take.html). Implication: the `*field(..)` accessor works only on Copy payloads. Move non-Copy values out with `mem::take`, `mem::replace` or `Option::take`.

Where the evidence is thin: the frequency answer rests on one Stack Overflow study, not on engine code. The Reference barely documents reborrowing, so the compiler checks are the only real evidence there.
