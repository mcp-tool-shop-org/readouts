# traits-generics: Traits & generics, the working set

10 recipes, 48 checks, all passing on rustc 1.98.1.

**What does each standard trait promise, and which derives are wrong for f64 fields?** Copy is an implicit bitwise copy needing Clone and all-Copy fields; derived Debug output is unstable; Display is hand-written; the comparison traits and Hash must agree; From is lossless and yields Into; Borrow, unlike AsRef, promises identical Eq/Ord/Hash. On f64 fields only PartialEq and PartialOrd derive; Eq, Hash and Ord fail with E0277.

**When is a generic (static dispatch) better than dyn Trait, and what does it cost?** Generics are the default: monomorphized, no dispatch cost, inlinable, paid for in compile time and binary size. Use dyn for mixed-type collections or smaller code, at the price of a vtable call that blocks inlining.

1. **A hand-written `impl Eq` on an f64 struct compiles and lies: a HashSet then holds NaN twice and finds neither.** Rust Project 2026 (std::cmp::Eq, https://doc.rust-lang.org/stable/std/cmp/trait.Eq.html). Implication: derive only PartialEq/PartialOrd on float records, and compare T2-restored state with `to_bits()`, because derived `==` treats ±0 as equal.

2. **`total_cmp` compares sign-adjusted bits as i64, so it returns Equal exactly when `to_bits` match (oracle: 1,000,196 pairs, 0 disagreements).** Rust Project 2026 (core::num::f64 source, https://doc.rust-lang.org/stable/src/core/num/f64.rs.html). Implication: key floats with Eq and Hash from `to_bits` and Ord from `total_cmp`, never with `partial_cmp().unwrap()`, which panics on NaN.

3. **`push_f64` canonicalises before writing, but `signature` mixes raw collider and height bits into `geom`, and `same_sig` compares `geom`.** mcp-tool-shop-org 2026 (si-rpg-engine rapier_law.rs, https://raw.githubusercontent.com/mcp-tool-shop-org/si-rpg-engine/main/solver/src/rapier_law.rs). Implication: add a test that a -0.0 collider coordinate does not force a world reload. `Signature` stores `cell` as bits, so `derive(PartialEq, Eq, Hash)` could replace the hand-written `same_sig`.

4. **Rapier 0.35.3's `Vector` is glam `DVec3`: every vector operator, plus PartialEq, but no Eq, Hash or PartialOrd.** glam 2026 (docs.rs DVec3 0.33.10, https://docs.rs/glam/0.33.10/glam/f64/struct.DVec3.html). Implication: do vector math on Rapier's type; a local newtype is only for bit-exact keys, because `impl Hash for Vector` is E0117.

5. **Dynamic dispatch looks the method up at run time and prevents inlining; a generic parameter stands for one concrete type at a time.** Rust Project 2026 (The Book 18.2, https://doc.rust-lang.org/stable/book/ch18-02-trait-objects.html). Implication: the flat 64-body buffer needs no dyn, so keep per-quantum loops monomorphic.

6. **`-> impl Trait` hides exactly one concrete type, and callers cannot turbofish an impl-Trait parameter (E0107).** Rust Project 2026 (Reference: Impl trait type, https://doc.rust-lang.org/stable/reference/types/impl-trait.html). Implication: return `Box<dyn>` or an enum when two types are possible; switching a public parameter between the two forms can break callers.

7. **Deref forwards method calls but not trait impls: a Deref wrapper fails a `T: Solid` bound with E0277.** Rust Design Patterns 2026 (Deref polymorphism anti-pattern, https://rust-unofficial.github.io/patterns/anti_patterns/deref.html). Implication: satisfy the orphan rule with a newtype plus delegation, and keep Deref for smart pointers (API guideline C-DEREF).

8. **Derived Debug formats are not a stable output.** Rust Project 2026 (std::fmt::Debug, https://doc.rust-lang.org/stable/std/fmt/trait.Debug.html). Implication: keep snapshot bytes as explicit `to_le_bytes`, and never hash or golden-test `{:?}` output.

9. **Implementing From provides Into, so a hand-written Into beside it is E0119; TryFrom carries an Error type.** Rust Project 2026 (std::convert::From, https://doc.rust-lang.org/stable/std/convert/trait.From.html). Implication: express boundary refusals (NaN, non-positive half-extents) as TryFrom newtypes.

10. **Implementing Iterator needs only `next`; `size_hint` defaults to (0, None), and a plain iterator may resume after None.** Rust Project 2026 (std::iter::Iterator, https://doc.rust-lang.org/stable/std/iter/trait.Iterator.html). Implication: use `chunks_exact` for stride-17 rows; a custom row iterator should yield copies, not references into `static mut BODIES`.

**Thin evidence.** Monomorphization's size cost is sourced, not measured on the solver's wasm; finding 3 is a code reading, not a reproduced failure; OrderedFloat's opposite ±0/NaN policy is from docs.rs `latest` (5.5.0).
