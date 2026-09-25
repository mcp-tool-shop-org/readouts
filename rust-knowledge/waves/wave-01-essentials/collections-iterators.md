# collections-iterators (wave 1, essentials)

**Q1. Which standard collections are safe to iterate when order reaches a hash or an output?**
Vec, slices and arrays (index order), VecDeque (front to back) and BTreeMap/BTreeSet (key order). HashMap/HashSet (arbitrary order, randomly seeded per map and per run) and `BinaryHeap::iter`/`into_vec` (arbitrary order) are safe only after you sort what they yield.

**Q2. How do iterators, closures and sorting behave, precisely enough to reason about determinism?**
Adapters are lazy and follow the source's order. Float `sum` is a left fold that starts from -0.0. Stable sorts keep ties in input order; unstable sorts may reorder them and no longer document determinism. `binary_search`'s pick among equal elements changed in 1.82. A closure's Fn trait follows what its body does with its captures.

1. **HashMap and HashSet iterate in arbitrary order under a randomly seeded hasher. Two identical maps in one process iterated and Debug-printed differently (measured).** Rust project 2026 (HashMap in std::collections, https://doc.rust-lang.org/stable/std/collections/struct.HashMap.html). Implication: keep maps off the snapshot path, or emit sorted keys. solver/src has none today.

2. **Only `sort`, `sort_by` and `sort_by_key` promise an order for ties. `sort_unstable` "may reorder equal elements", and the 1.80 docs' "fixed seed ... deterministic behavior" sentence disappeared when ipnsort arrived in 1.81.** Rust project 2026 (Primitive type slice, https://doc.rust-lang.org/stable/std/primitive.slice.html). Implication: give every hashed sort a unique key. On 1.98.1, unstable ties stayed in input order at 20 elements and broke at 21 (measured), so small tests hide the problem.

3. **Under Rapier 0.35.3 the snapshot's contact-pair key cannot tie: Rapier adds a contact edge only when an undirected `find_edge` finds none.** Dimforge 2026 (rapier3d-f64 0.35.3 pair_management.rs, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/geometry/narrow_phase/pair_management.rs). Implication: `rebuild_snapshot`'s stable `sort_by` and an unstable sort would hash the same bytes today. Keep any future key unique.

4. **Rapier's graph removes edges with `swap_remove`, so the order of `contact_pairs()` changes whenever a contact ends.** Dimforge 2026 (rapier3d-f64 0.35.3 graph.rs, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/data/graph.rs). Implication: sort a dependency's iteration order before hashing it. `swap_remove` in engine Vecs has the same effect.

5. **How std handles ties can change between releases: 1.82's `binary_search` "may select a different value among the equal ones".** Rust project 2026 (RELEASES.md at tag 1.98.1, https://github.com/rust-lang/rust/blob/1.98.1/RELEASES.md). Implication: find the first match with `partition_point`, and rerun the goldens whenever the 1.98.1 pin moves.

6. **Since 1.81, sorts may panic when the comparator is not a total order. A NaN-as-Equal comparator panicked on one input and silently mis-sorted another (measured).** Rust project 2024 (Announcing Rust 1.81.0, https://blog.rust-lang.org/2024/09/05/Rust-1.81.0/). Implication: sort floats with `total_cmp` plus an id tiebreak, after `canon()`.

7. **Float `sum` is `fold(-0.0, |a, b| a + b)`, and an empty float sum has been -0.0 since 1.82 (rust-lang/rust#129321).** Rust project 2026 (core accum.rs at tag 1.98.1, https://github.com/rust-lang/rust/blob/1.98.1/library/core/src/iter/traits/accum.rs). Implication: sum in body-index order and canonicalise zero before `to_bits`. The snapshot does this; `mix_f64` in `signature()` does not.

8. **`array.into_iter()` yields values only from edition 2021 on.** Rust project 2026 (Edition Guide: IntoIterator for arrays, https://doc.rust-lang.org/edition-guide/rust-2021/IntoIterator-for-arrays.html). Implication: the solver is edition 2021, so code pasted from 2018 changes its item type.

9. **Unicode-aware `str` and `char` methods follow `char::UNICODE_VERSION`. It changes between releases, which "is not considered to be a breaking change". 1.98.1 reports (17, 0, 0).** Rust project 2026 (Primitive type char, https://doc.rust-lang.org/stable/std/primitive.char.html). Implication: key hashed names by bytes or ASCII case folding.

Thin evidence: the 20/21 tie boundary and the inputs that panic are measurements of 1.98.1's implementation, not documented behaviour. The claim that HashMap order differs between runs rests on the docs' "randomly seeded" and two observed runs. The claim that Rapier's key cannot tie comes from reading its 0.35.3 source; no Rapier document states it.
