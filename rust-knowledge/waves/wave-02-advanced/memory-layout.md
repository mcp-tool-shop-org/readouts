# memory-layout: Memory, smart pointers & layout (wave 2, advanced)

**Which layout guarantees does Rust make, and which does it not?** Guaranteed: array offsets, repr(C) and repr(transparent) layouts, one-byte repr(u8) enums, Box<T> as one C pointer, Option's niche for the std-listed types, Vec as a (ptr, cap, len) triplet. Not guaranteed: repr(Rust) order or size, other niches, DST-pointer width, Vec's growth strategy.

**Which ownership shapes fit simulation state?** One owner per collection with Copy indices into it: flat arrays at the ABI, a generational arena for entities, Box<[T]> for fixed heap buffers, Rc/Arc only for immutable shared leaves, no self-references.

1. **Arrays and #[repr(C)] are the only layouts a foreign reader may assume; repr(Rust) promises only aligned, non-overlapping fields.** The Rust Reference 2026 (Type layout, https://doc.rust-lang.org/stable/reference/type-layout.html). Implication: keep BODIES and COLLIDERS as flat [f64; N]. The oracle measures f64 as 8-aligned on wasm32, so `bodies_ptr() / 8` is sound. The one unchecked coupling is the 17/10 strides hard-coded in build.mjs.

2. **Option's niche is guaranteed only for the std-listed types.** Rust std docs 2026 (std::option, Representation, https://doc.rust-lang.org/stable/std/option/index.html). Implication: Option<RigidBodyHandle> costs 12 bytes because Index has no niche. Use NonZeroU32 for ids you design, and decode the DRIVEN mode with match or TryFrom, never transmute.

3. **UnsafeCell is the only legal source of shared mutation, and the deny-by-default invalid_reference_casting lint only catches casts written inline.** The Rust Reference 2026 (Interior mutability, https://doc.rust-lang.org/stable/reference/interior-mutability.html); rustc book 2026 (Deny-by-default lints, https://doc.rust-lang.org/stable/rustc/lints/listing/deny-by-default.html). Implication: solver_clear_warmstart turns &ContactPair into &mut through a Vec of pointers; rustc denies the same cast inline. rapier3d-f64 0.35.3 has no &mut path to contact pairs, so T2's warm-start writes need a sound route: rebuild the world, or patch in an accessor.

4. **After a successful realloc the old pointer is dead, even if the block stayed where it was.** Rust std docs 2026 (GlobalAlloc::realloc, https://doc.rust-lang.org/stable/std/alloc/trait.GlobalAlloc.html#method.realloc). Implication: snapshot_ptr() is valid until the next solver_* call. build.mjs already reads it fresh each time. T2's restore_ptr() must be read after the buffer is sized.

5. **Rapier's arena hands out indices in insertion order and bumps one arena-wide generation on every removal.** Dimforge 2026 (rapier3d-f64 0.35.3 src/data/arena.rs, https://docs.rs/crate/rapier3d-f64/0.35.3/source/src/data/arena.rs). Implication: the snapshot hashes (index, generation) pairs. Build in a fixed order and never remove; otherwise T2 must replay the same removals.

6. **A strong Rc/Arc cycle leaks without warning; Weak breaks it.** The Rust Book 2026 (Reference Cycles Can Leak Memory, https://doc.rust-lang.org/stable/book/ch15-06-reference-cycles.html). Implication: keep state in arenas with indices. Cache each body's parry SharedShape instead of allocating one or two new Arcs per driven body every quantum.

7. **LazyCell and LazyLock have been stable since 1.80, OnceCell and OnceLock since 1.70, and a static must be Sync.** Rust Release Team 2024 (Announcing Rust 1.80.0, https://blog.rust-lang.org/2024/07/25/Rust-1.80.0/). Implication: computed statics use LazyLock or OnceLock; SOLVER's const initialiser needs neither.

8. **Statics are never dropped, and an assignment drops the old value first.** The Rust Reference 2026 (Static items, https://doc.rust-lang.org/stable/reference/items/static-items.html). Implication: `solver.loaded = Some(..)` is the only place a world is freed.

9. **Pin fixes the address only of !Unpin values; a self-reference breaks when its struct moves.** Rust std docs 2026 (std::pin, https://doc.rust-lang.org/stable/std/pin/index.html). Implication: keep every cross-reference an index. That is what lets T2 rebuild a world from bytes.

**Where the evidence is thin.** The repr(Rust) size and the slotmap key's niche are rustc 1.98.1 measurements, not promises. The typed-arena and bumpalo claims rest on their docs alone. The UB verdict on solver_clear_warmstart rests on the std docs' and the lint's wording; Miri's view belongs to the unsafe-ffi lane. Whether the wasm allocator moves the snapshot buffer is for wave 3 to measure.
