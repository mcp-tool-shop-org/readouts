# Deterministic simulation architecture — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](sim-architecture.md) · [catalog index](README.md)

## Encode snapshots canonically: to_le_bytes in a fixed field order, sorted pairs, no padding, a version tag
**A snapshot is a byte string the law defines — explicit little-endian numbers in a declared order, collections sorted by a total key, and a header with a magic, a law version and counts — never a struct's memory image, whose field order and padding belong to the compiler.**

*Check 1: Versioned little-endian snapshot: pair order cannot change bytes; old version, truncation refused* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// A canonical snapshot: magic, law version, counts, then fields in one fixed
// order, every number written with to_le_bytes, pairs sorted by their ids.
const MAGIC: [u8; 4] = *b"SIRS";
const LAW_VERSION: u32 = 3;

struct Body { pos: [f64; 3], vel: [f64; 3] }
#[derive(Clone, Copy)]
struct Pair { a: (u32, u32), b: (u32, u32), impulse: f64 }

fn encode(bodies: &[Body], pairs: &[Pair]) -> Vec<u8> {
    let mut out = Vec::new();
    out.extend_from_slice(&MAGIC);
    out.extend_from_slice(&LAW_VERSION.to_le_bytes());
    out.extend_from_slice(&(bodies.len() as u32).to_le_bytes());
    out.extend_from_slice(&(pairs.len() as u32).to_le_bytes());
    for b in bodies {
        for x in b.pos.iter().chain(&b.vel) {
            out.extend_from_slice(&x.to_le_bytes());
        }
    }
    let mut sorted = pairs.to_vec();
    sorted.sort_by_key(|p| (p.a, p.b));
    for p in sorted {
        for w in [p.a.0, p.a.1, p.b.0, p.b.1] {
            out.extend_from_slice(&w.to_le_bytes());
        }
        out.extend_from_slice(&p.impulse.to_le_bytes());
    }
    out
}

// Refuses a foreign magic, another law version, or a length that is not the layout.
fn check(bytes: &[u8]) -> Result<(u32, u32), String> {
    if bytes.len() < 16 || bytes[0..4] != MAGIC {
        return Err("not a snapshot".to_string());
    }
    let word = |at: usize| u32::from_le_bytes(bytes[at..at + 4].try_into().unwrap());
    if word(4) != LAW_VERSION {
        return Err(format!("law version {} is not {}", word(4), LAW_VERSION));
    }
    let (n_bodies, n_pairs) = (word(8), word(12));
    let expected = 16 + n_bodies as usize * 48 + n_pairs as usize * 24;
    if bytes.len() != expected {
        return Err(format!("{} bytes where the layout needs {}", bytes.len(), expected));
    }
    Ok((n_bodies, n_pairs))
}

fn main() {
    let bodies = [Body { pos: [0.0, 0.5, 0.0], vel: [0.0, -0.125, 0.0] }, Body { pos: [1.0, 0.5, 0.0], vel: [0.0; 3] }];
    let p = Pair { a: (1, 0), b: (2, 0), impulse: 0.25 };
    let q = Pair { a: (0, 0), b: (2, 0), impulse: 0.5 };
    let one = encode(&bodies, &[p, q]);
    let two = encode(&bodies, &[q, p]);
    println!("{} bytes, header {:02x?}, same bytes for either pair order: {}", one.len(), &one[..16], one == two);
    println!("check: {:?}", check(&one));
    let mut old = one.clone();
    old[4..8].copy_from_slice(&2u32.to_le_bytes());
    println!("older law: {:?}", check(&old));
    println!("truncated: {:?}", check(&one[..one.len() - 8]));
    println!("0.5 to_le_bytes {:02x?}, to_be_bytes {:02x?}", 0.5f64.to_le_bytes(), 0.5f64.to_be_bytes());
}
```
Expected output: `160 bytes, header [53, 49, 52, 53, 03, 00, 00, 00, 02, 00, 00, 00, 02, 00, 00, 00], same bytes for either pair order: true check: Ok((2, 2)) older law: Err("law version 2 is not 3") truncated: Err("15`

*Check 2: repr(C) pads { u8, f64, u8 } to 24 bytes; the default representation packs it into 16* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::mem::{offset_of, size_of};

#[repr(C)]
struct CContact { flag: u8, impulse: f64, kind: u8 }

struct RustContact { flag: u8, impulse: f64, kind: u8 }

fn main() {
    println!(
        "repr(C): size {} offsets {} {} {}; repr(Rust): size {}",
        size_of::<CContact>(),
        offset_of!(CContact, flag),
        offset_of!(CContact, impulse),
        offset_of!(CContact, kind),
        size_of::<RustContact>()
    );
    let r = RustContact { flag: 1, impulse: 0.5, kind: 2 };
    let c = CContact { flag: 1, impulse: 0.5, kind: 2 };
    let _ = (r.flag, r.impulse, r.kind, c.flag, c.impulse, c.kind);
}
```
Expected output: `repr(C): size 24 offsets 0 8 16; repr(Rust): size 16`

*Check 3: bytemuck derive(Pod) refuses a struct with padding: E0080 at compile time* · `compile_fail` · edition 2021 · host · lib · deps: bytemuck · errors: E0080 · stderr has “derive(Pod) was applied to a type with padding” · **✔ oracle pass**
```rust
use bytemuck::{Pod, Zeroable};

// 4 bytes of padding sit between `pair` and `impulse`.
#[derive(Clone, Copy, Pod, Zeroable)]
#[repr(C)]
pub struct ContactRecord {
    pub pair: u32,
    pub impulse: f64,
}
```

*Check 4: Padding spelled as a zeroed field makes the record Pod, and its 16 bytes are explicit* · `runs` · edition 2021 · host · bin · deps: bytemuck · **✔ oracle pass**
```rust
use bytemuck::{Pod, Zeroable};

// The padding is a named, zeroed field, so the struct has no uninit bytes.
#[derive(Clone, Copy, Pod, Zeroable)]
#[repr(C)]
pub struct ContactRecord {
    pub pair: u32,
    pub _pad: u32,
    pub impulse: f64,
}

fn main() {
    let r = ContactRecord { pair: 7, _pad: 0, impulse: 0.5 };
    let bytes: &[u8] = bytemuck::bytes_of(&r);
    let hex: Vec<String> = bytes.iter().map(|b| format!("{b:02x}")).collect();
    println!("{} {}", std::mem::size_of::<ContactRecord>(), hex.join(""));
}
```
Expected output: `16 0700000000000000000000000000e03f`

## Keep the law out of an ECS: archetype tables swap-remove rows and query iteration order is not guaranteed
**bevy_ecs 0.19.1 and hecs 0.11.1 keep entities in archetype tables that swap-remove rows, bevy documents query iteration order as not guaranteed and runs non-conflicting systems in parallel, and Entity bits are not stable across releases; for a 64-record law an ECS buys composition it does not need and costs an explicit sort, a pinned executor and ambiguity checks to win determinism back.**

*Check 1: Swap-remove storage model: one despawn and one archetype move reorder iteration; sort restores* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// A model of archetype storage: each table is a Vec of entity ids. Despawn is a
// swap-remove (hecs 0.11.1 Archetype::remove, bevy_ecs 0.19.1
// Table::swap_remove_unchecked); gaining a component appends the entity to another
// archetype and swap-removes it from the old one (hecs 0.11.1 World::insert).
fn iterate(tables: &[Vec<u32>]) -> Vec<u32> { tables.iter().flatten().copied().collect() }

fn main() {
    let mut boxes: Vec<u32> = vec![1, 2, 3, 4, 5];
    let mut carried: Vec<u32> = vec![];
    println!("spawned:        {:?}", iterate(&[boxes.clone(), carried.clone()]));
    let at = boxes.iter().position(|&e| e == 2).unwrap();
    boxes.swap_remove(at); // despawn 2: the last row moves into its place
    println!("despawn 2:      {:?}", iterate(&[boxes.clone(), carried.clone()]));
    let at = boxes.iter().position(|&e| e == 1).unwrap();
    let moved = boxes.swap_remove(at); // add a Carried component to 1
    carried.push(moved);
    println!("1 gains a part: {:?}", iterate(&[boxes.clone(), carried.clone()]));
    let mut sorted = iterate(&[boxes, carried]);
    sorted.sort_unstable();
    println!("sorted by id:   {:?}", sorted);
}
```
Expected output: `spawned:        [1, 2, 3, 4, 5] despawn 2:      [1, 5, 3, 4] 1 gains a part: [4, 5, 3, 1] sorted by id:   [1, 3, 4, 5]`

## Key records by stable ids, keep insertion and removal history in the record, and sort by a total id key
**Generational handles encode history — Rapier's generation is one counter per set, raised on every removal, and slotmap reuses slots under new versions — so persisted ids are the world file's own, handles are reproduced only by replaying the same inserts and removals, and every order-sensitive step iterates in sorted full-key order, never container order.**

*Check 1: Rapier handles follow insertion order, and each removal raises the generation of later handles* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// The same three colliders inserted in two orders: which (index, generation) each gets.
fn build(order: &[&str]) -> Vec<(String, (u32, u32))> {
    let mut colliders = ColliderSet::new();
    let mut out = Vec::new();
    for name in order {
        let half = match *name { "slab" => 4.0, "crate" => 0.5, _ => 1.0 };
        let h = colliders.insert(ColliderBuilder::cuboid(half, 0.25, half).build());
        out.push((name.to_string(), h.into_raw_parts()));
    }
    out.sort();
    out
}

fn main() {
    println!("file order  {:?}", build(&["slab", "crate", "wall"]));
    println!("other order {:?}", build(&["wall", "crate", "slab"]));
    // Removal history: every handle inserted after a removal carries the new generation,
    // in a reused slot or a fresh one.
    let mut islands = IslandManager::new();
    let mut bodies = RigidBodySet::new();
    let mut colliders = ColliderSet::new();
    let ball = || ColliderBuilder::ball(0.5).build();
    let a = colliders.insert(ball());
    let b = colliders.insert(ball());
    colliders.remove(a, &mut islands, &mut bodies, false);
    let c = colliders.insert(ball());
    let d = colliders.insert(ball());
    colliders.remove(b, &mut islands, &mut bodies, false);
    let e = colliders.insert(ball());
    let f = colliders.insert(ball());
    let parts: Vec<String> = [("a", a), ("b", b), ("c", c), ("d", d), ("e", e), ("f", f)]
        .iter()
        .map(|(n, h)| format!("{n}{:?}", h.into_raw_parts()))
        .collect();
    println!("{}", parts.join(" "));
}
```
Expected output: `file order  [("crate", (1, 0)), ("slab", (0, 0)), ("wall", (2, 0))] other order [("crate", (1, 0)), ("slab", (2, 0)), ("wall", (0, 0))] a(0, 0) b(1, 0) c(0, 1) d(2, 1) e(1, 2) f(3, 2)`

*Check 2: ColliderHandle has no Ord at 0.35.3: sorting handle pairs directly is E0277* · `compile_fail` · edition 2021 · host · lib · deps: rapier3d_f64 · errors: E0277 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

pub fn canonical(mut pairs: Vec<(ColliderHandle, ColliderHandle)>) -> Vec<(ColliderHandle, ColliderHandle)> {
    pairs.sort();
    pairs
}
```

*Check 3: Sorting contact pairs by their into_raw_parts() tuples compiles* · `compiles` · edition 2021 · host · lib · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

pub fn canonical(mut pairs: Vec<(ColliderHandle, ColliderHandle)>) -> Vec<(ColliderHandle, ColliderHandle)> {
    pairs.sort_by_key(|(a, b)| (a.into_raw_parts(), b.into_raw_parts()));
    pairs
}
```

*Check 4: slotmap reuses a freed slot under a new version; a map rebuilt from live values has other keys* · `runs` · edition 2021 · host · bin · deps: slotmap · **✔ oracle pass**
```rust
use slotmap::{DefaultKey, SlotMap};

fn order(m: &SlotMap<DefaultKey, &'static str>) -> String {
    m.values().copied().collect::<Vec<_>>().join(",")
}

fn main() {
    let mut m: SlotMap<DefaultKey, &'static str> = SlotMap::new();
    let a = m.insert("a");
    let b = m.insert("b");
    let _c = m.insert("c");
    m.remove(b);
    let d = m.insert("d");
    // d reuses b's slot with a new version; the old key for b is dead.
    println!("iteration after remove+insert: {}", order(&m));
    println!("old key b finds: {:?}", m.get(b));
    println!("b={:?} d={:?} a={:?}", b, d, a);
    // Rebuilding from the live values in insertion order does not give back the same keys.
    let mut rebuilt: SlotMap<DefaultKey, &'static str> = SlotMap::new();
    let mut keys = Vec::new();
    for v in ["a", "c", "d"] {
        keys.push(rebuilt.insert(v));
    }
    println!("rebuilt keys {:?}; original d key still valid in rebuilt: {}", keys, rebuilt.get(d).is_some());
}
```
Expected output: `iteration after remove+insert: a,d,c old key b finds: None b=DefaultKey(2v1) d=DefaultKey(2v3) a=DefaultKey(1v1) rebuilt keys [DefaultKey(1v1), DefaultKey(2v1), DefaultKey(3v1)]; original d key still `

*Check 5: IndexMap: swap_remove perturbs order, shift_remove keeps it, sort_keys restores key order* · `runs` · edition 2021 · host · bin · deps: indexmap · **✔ oracle pass**
```rust
use indexmap::IndexMap;

fn keys(m: &IndexMap<u32, f64>) -> String {
    m.keys().map(|k| k.to_string()).collect::<Vec<_>>().join(",")
}

fn main() {
    let mut a: IndexMap<u32, f64> = IndexMap::new();
    for id in [30, 10, 20, 40] {
        a.insert(id, id as f64);
    }
    let mut b = a.clone();
    println!("insertion order: {}", keys(&a));
    a.swap_remove(&10);
    b.shift_remove(&10);
    println!("swap_remove(10): {}", keys(&a));
    println!("shift_remove(10): {}", keys(&b));
    a.sort_keys();
    println!("after sort_keys: {}", keys(&a));
}
```
Expected output: `insertion order: 30,10,20,40 swap_remove(10): 30,40,20 shift_remove(10): 30,20,40 after sort_keys: 20,30,40`

*Check 6: Sums depend on order, HashMap orders differ per map, a stable sort on a tying key leaks order* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::collections::{BTreeMap, HashMap};

fn main() {
    // An order-sensitive reduction: the f64 sum of the same four impulses.
    let impulses: [(u32, f64); 4] = [(3, 1e16), (1, 1.0), (4, -1e16), (2, 1.0)];
    let mut container_order = impulses.to_vec();
    let a: f64 = container_order.iter().map(|p| p.1).sum();
    container_order.reverse();
    let b: f64 = container_order.iter().map(|p| p.1).sum();
    container_order.sort_by_key(|p| p.0);
    let sorted: f64 = container_order.iter().map(|p| p.1).sum();
    println!("sum in one order {a:?}, reversed {b:?}, sorted by id {sorted:?}");

    // Two HashMaps with fresh RandomState keys, same 64 entries: compare iteration orders.
    let h1: HashMap<u32, f64> = (0..64).map(|i| (i, i as f64)).collect();
    let h2: HashMap<u32, f64> = (0..64).map(|i| (i, i as f64)).collect();
    let o1: Vec<u32> = h1.keys().copied().collect();
    let o2: Vec<u32> = h2.keys().copied().collect();
    let b1: BTreeMap<u32, f64> = h1.clone().into_iter().collect();
    let b2: BTreeMap<u32, f64> = h2.clone().into_iter().collect();
    let k1: Vec<u32> = b1.keys().copied().collect();
    let k2: Vec<u32> = b2.keys().copied().collect();
    println!("HashMap orders equal: {}; BTreeMap orders equal: {}", o1 == o2, k1 == k2);

    // A stable sort on a key that is not unique keeps the incoming order of ties.
    let contacts_a = vec![(5u32, 9u32), (2, 7), (5, 1)];
    let contacts_b = vec![(5u32, 1u32), (2, 7), (5, 9)];
    let by_body = |mut v: Vec<(u32, u32)>| { v.sort_by_key(|c| c.0); v };
    let by_pair = |mut v: Vec<(u32, u32)>| { v.sort_by_key(|c| (c.0, c.1)); v };
    println!("sorted by body only equal: {}", by_body(contacts_a.clone()) == by_body(contacts_b.clone()));
    println!("sorted by full pair equal: {}", by_pair(contacts_a) == by_pair(contacts_b));
}
```
Expected output: `sum in one order 1.0, reversed 0.0, sorted by id 2.0 HashMap orders equal: false; BTreeMap orders equal: true sorted by body only equal: false sorted by full pair equal: true`

## Parse host-written body slots into a typed record at the boundary, with named refusals for the mode slot
**Every f64 the host writes into the law's buffers is untrusted: decode each record once into a typed value — finite floats, positive half-extents, a unit quaternion, and a mode that is exactly 0, 1, 2 or 3 — and refuse anything else with a reason naming the body, the slot and the raw bits, so every law reads the same decoded value.**

*Check 1: Slot 16 read two ways: 3.0, 0.5, 4.0, NaN, inf disagree; the decoder refuses with body and bits* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// Slot 16 of a body record is its solver mode. Today two readers disagree:
//   lib.rs step():          driven = slot16 != 0.0
//   rapier_law.rs signature(): driven = slot16 == 1.0 || slot16 == 2.0; carried = slot16 == 3.0
// and neither refuses an unknown value or NaN.
fn box_reading(x: f64) -> &'static str { if x != 0.0 { "driven" } else { "free" } }
fn product_reading(x: f64) -> &'static str {
    if x == 1.0 || x == 2.0 { "driven" } else if x == 3.0 { "carried" } else { "dynamic" }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Mode { Dynamic, Kinematic, Lifted, Carried }

#[derive(Debug, PartialEq)]
enum Refusal { UnknownMode { body: u32, bits: u64 } }

// One decoder, called by every law: accepts exactly 0, 1, 2, 3 (signed zero is
// canonicalised first, as the law does everywhere) and refuses everything else,
// NaN included, naming the body and the raw bit pattern.
fn decode_mode(body: u32, x: f64) -> Result<Mode, Refusal> {
    let x = if x == 0.0 { 0.0 } else { x };
    match x.to_bits() {
        0x0000_0000_0000_0000 => Ok(Mode::Dynamic),
        0x3ff0_0000_0000_0000 => Ok(Mode::Kinematic),
        0x4000_0000_0000_0000 => Ok(Mode::Lifted),
        0x4008_0000_0000_0000 => Ok(Mode::Carried),
        bits => Err(Refusal::UnknownMode { body, bits }),
    }
}

fn main() {
    for x in [0.0, -0.0, 1.0, 2.0, 3.0, 0.5, 4.0, -1.0, f64::NAN, f64::INFINITY] {
        let decoded = match decode_mode(5, x) {
            Ok(m) => format!("{m:?}"),
            Err(Refusal::UnknownMode { body, bits }) => format!("refused body {body} slot 16 bits {bits:016x}"),
        };
        println!("{:>5}: box law {:<6} product law {:<7} decoder {}", format!("{x:?}"), box_reading(x), product_reading(x), decoded);
    }
}
```
Expected output: `0.0: box law free   product law dynamic decoder Dynamic  -0.0: box law free   product law dynamic decoder Dynamic   1.0: box law driven product law driven  decoder Kinematic   2.0: box law driven prod`

*Check 2: TryFrom<&[f64; 17]> refuses inf, NaN, a zero half-extent, a non-unit quaternion, mode 0.5* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// Parse, don't just check: a raw stride-17 body record becomes a typed record or a named refusal.
#[derive(Debug, Clone, Copy)]
enum Mode { Dynamic, Kinematic, Lifted, Carried }

enum Refusal {
    NotFinite { slot: usize, bits: u64 },
    NotPositive { slot: usize },
    NotUnit { norm: f64 },
    UnknownMode { bits: u64 },
}

impl std::fmt::Display for Refusal {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Refusal::NotFinite { slot, bits } => write!(f, "slot {slot} is not finite (bits {bits:016x})"),
            Refusal::NotPositive { slot } => write!(f, "slot {slot} is not a positive half-extent"),
            Refusal::NotUnit { norm } => write!(f, "quaternion norm {norm:?} is not 1 within 1e-9"),
            Refusal::UnknownMode { bits } => write!(f, "slot 16 holds no mode (bits {bits:016x})"),
        }
    }
}

struct Body { mode: Mode }

const UNIT_TOLERANCE: f64 = 1e-9;

impl TryFrom<&[f64; 17]> for Body {
    type Error = Refusal;
    fn try_from(r: &[f64; 17]) -> Result<Body, Refusal> {
        for (slot, x) in r.iter().enumerate() {
            if !x.is_finite() {
                return Err(Refusal::NotFinite { slot, bits: x.to_bits() });
            }
        }
        for slot in 13..16 {
            if !(r[slot] > 0.0) {
                return Err(Refusal::NotPositive { slot });
            }
        }
        let norm = (r[6] * r[6] + r[7] * r[7] + r[8] * r[8] + r[9] * r[9]).sqrt();
        if !((norm - 1.0).abs() <= UNIT_TOLERANCE) {
            return Err(Refusal::NotUnit { norm });
        }
        let m = if r[16] == 0.0 { 0.0 } else { r[16] };
        let mode = match m.to_bits() {
            0x0000_0000_0000_0000 => Mode::Dynamic,
            0x3ff0_0000_0000_0000 => Mode::Kinematic,
            0x4000_0000_0000_0000 => Mode::Lifted,
            0x4008_0000_0000_0000 => Mode::Carried,
            bits => return Err(Refusal::UnknownMode { bits }),
        };
        Ok(Body { mode })
    }
}

fn main() {
    let ok = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 1.0];
    let mut cases: Vec<(&str, [f64; 17])> = vec![("well-formed", ok)];
    let mut r = ok; r[0] = f64::INFINITY; cases.push(("x = inf", r));
    let mut r = ok; r[4] = f64::NAN; cases.push(("vy = NaN", r));
    let mut r = ok; r[14] = 0.0; cases.push(("hy = 0", r));
    let mut r = ok; r[9] = 2.0; cases.push(("q = (0,0,0,2)", r));
    let mut r = ok; r[16] = 3.0; cases.push(("mode = 3", r));
    let mut r = ok; r[16] = 0.5; cases.push(("mode = 0.5", r));
    for (name, rec) in &cases {
        match Body::try_from(rec) {
            Ok(b) => println!("{name}: accepted as {:?}", b.mode),
            Err(e) => println!("{name}: refused, {e}"),
        }
    }
    let _ = [Mode::Dynamic, Mode::Kinematic, Mode::Lifted, Mode::Carried];
    // A NaN-only guard, as bad() is today, lets infinity through.
    println!("a NaN-only guard passes inf: {}", !f64::INFINITY.is_nan());
}
```
Expected output: `well-formed: accepted as Kinematic x = inf: refused, slot 0 is not finite (bits 7ff0000000000000) vy = NaN: refused, slot 4 is not finite (bits 7ff8000000000000) hy = 0: refused, slot 14 is not a posi`

*Check 3: Float literal patterns compile clean: -0.0 takes the 0.0 arm and NaN takes no literal arm* · `runs` · edition 2021 · host · bin · no warnings · **✔ oracle pass**
```rust
fn mode(x: f64) -> &'static str {
    match x {
        0.0 => "dynamic",
        1.0 => "kinematic",
        2.0 => "lifted",
        3.0 => "carried",
        _ => "no literal matched",
    }
}

fn main() {
    for x in [-0.0, 3.0, f64::NAN] {
        println!("{x:?}: {}", mode(x));
    }
}
```
Expected output: `-0.0: dynamic 3.0: carried NaN: no literal matched`

*Check 4: A law whose match on Mode forgets Carried fails to build: E0004* · `compile_fail` · edition 2021 · host · lib · errors: E0004 · stderr has “`Mode::Carried` not covered” · **✔ oracle pass**
```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Mode { Dynamic, Kinematic, Lifted, Carried }

// A law that forgot one mode does not build.
pub fn box_law_driven(mode: Mode) -> bool {
    match mode {
        Mode::Dynamic => false,
        Mode::Kinematic | Mode::Lifted => true,
    }
}
```

*Check 5: The exhaustive match over Mode compiles clean* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Mode { Dynamic, Kinematic, Lifted, Carried }

// Each law states what every mode means; a new mode fails the build until it does.
pub fn box_law_driven(mode: Mode) -> bool {
    match mode {
        Mode::Dynamic | Mode::Carried => false,
        Mode::Kinematic | Mode::Lifted => true,
    }
}
```

## Persist hashes of explicit little-endian bytes, never #[derive(Hash)] streams or DefaultHasher output
**What `Hash` feeds a hasher is not portable (usize length prefixes, native endianness) and `DefaultHasher`'s algorithm is unspecified across releases, so any hash that is stored, compared across hosts or pinned in a golden is a named function (FNV-1a, xxh3, BLAKE3) over bytes the law encoded itself.**

*Check 1: #[derive(Hash)] feeds 18 bytes on x86_64: a u32, str bytes plus 0xff, an 8-byte Vec length* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::hash::{Hash, Hasher};

// Records every byte that Hash feeds to a Hasher.
struct Recorder(Vec<u8>);
impl Hasher for Recorder {
    fn write(&mut self, bytes: &[u8]) { self.0.extend_from_slice(bytes); }
    fn finish(&self) -> u64 { 0 }
}

#[derive(Hash)]
struct Body { id: u32, name: String, cells: Vec<u8> }

fn main() {
    let b = Body { id: 7, name: "ab".to_string(), cells: vec![1, 2, 3] };
    let mut r = Recorder(Vec::new());
    b.hash(&mut r);
    let hex: Vec<String> = r.0.iter().map(|x| format!("{x:02x}")).collect();
    println!("{} bytes: {}", r.0.len(), hex.join(" "));
    println!("usize is {} bytes here", std::mem::size_of::<usize>());
}
```
Expected output: `18 bytes: 07 00 00 00 61 62 ff 03 00 00 00 00 00 00 00 01 02 03 usize is 8 bytes here`

*Check 2: The same #[derive(Hash)] value feeds 14 bytes on wasm32: the usize prefix is 4 bytes* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls fed_bytes() · **✔ oracle pass**
```rust
use std::hash::{Hash, Hasher};

struct Recorder(Vec<u8>);
impl Hasher for Recorder {
    fn write(&mut self, bytes: &[u8]) { self.0.extend_from_slice(bytes); }
    fn finish(&self) -> u64 { 0 }
}

#[derive(Hash)]
struct Body { id: u32, name: String, cells: Vec<u8> }

/// How many bytes #[derive(Hash)] feeds for the same value on this target.
#[unsafe(no_mangle)]
pub extern "C" fn fed_bytes() -> u32 {
    let b = Body { id: 7, name: "ab".to_string(), cells: vec![1, 2, 3] };
    let mut r = Recorder(Vec::new());
    b.hash(&mut r);
    r.0.len() as u32
}
```
Expected output: `14`

*Check 3: FNV-1a 64 over 35 explicit little-endian bytes returns 845153761026826623 on x86_64* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
// FNV-1a 64 (RFC 9923) over an explicit little-endian encoding of one body record.
fn fnv1a64(bytes: &[u8]) -> u64 {
    let mut h: u64 = 0xcbf29ce484222325;
    for &b in bytes {
        h = (h ^ b as u64).wrapping_mul(0x100000001b3);
    }
    h
}

fn encode(id: u32, pos: [f64; 3], cells: &[u8]) -> Vec<u8> {
    let mut out = Vec::new();
    out.extend_from_slice(&id.to_le_bytes());
    for x in pos {
        out.extend_from_slice(&x.to_le_bytes());
    }
    out.extend_from_slice(&(cells.len() as u32).to_le_bytes()); // a fixed-width length, not usize
    out.extend_from_slice(cells);
    out
}

fn main() {
    let bytes = encode(7, [0.5, -8.0, 1.0 / 64.0], &[1, 2, 3]);
    println!("{} bytes, fnv1a64 {}", bytes.len(), fnv1a64(&bytes));
}
```
Expected output: `35 bytes, fnv1a64 845153761026826623`

*Check 4: The same FNV-1a 64 over the same bytes returns the same value on wasm32* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls record_hash() · **✔ oracle pass**
```rust
fn fnv1a64(bytes: &[u8]) -> u64 {
    let mut h: u64 = 0xcbf29ce484222325;
    for &b in bytes {
        h = (h ^ b as u64).wrapping_mul(0x100000001b3);
    }
    h
}

fn encode(id: u32, pos: [f64; 3], cells: &[u8]) -> Vec<u8> {
    let mut out = Vec::new();
    out.extend_from_slice(&id.to_le_bytes());
    for x in pos {
        out.extend_from_slice(&x.to_le_bytes());
    }
    out.extend_from_slice(&(cells.len() as u32).to_le_bytes());
    out.extend_from_slice(cells);
    out
}

#[unsafe(no_mangle)]
pub extern "C" fn record_hash() -> u64 {
    fnv1a64(&encode(7, [0.5, -8.0, 1.0 / 64.0], &[1, 2, 3]))
}
```
Expected output: `845153761026826623`

*Check 5: The signature's word mixer collides on two half-extent pairs; FNV-1a 64 and xxh3 do not* · `runs` · edition 2021 · host · bin · deps: xxhash_rust · **✔ oracle pass**
```rust
use xxhash_rust::xxh3::xxh3_64;

const P: u64 = 0x100000001b3;
const BASIS: u64 = 0xcbf29ce484222325;

// The solver's signature mixer (solver/src/rapier_law.rs): multiply, then add a whole word.
fn mix_u64(h: u64, x: u64) -> u64 { h.wrapping_mul(P).wrapping_add(x) }

// FNV-1a 64 as RFC 9923 defines it: XOR one octet, then multiply.
fn fnv1a64(bytes: &[u8]) -> u64 {
    let mut h = BASIS;
    for &b in bytes {
        h = (h ^ b as u64).wrapping_mul(P);
    }
    h
}

fn le(xs: &[f64]) -> Vec<u8> { xs.iter().flat_map(|x| x.to_le_bytes()).collect() }

fn main() {
    let (hx, hy) = (0.5f64, 0.5f64);
    // Next float above hx, and hy's bit pattern minus the prime.
    let hx2 = f64::from_bits(hx.to_bits() + 1);
    let hy2 = f64::from_bits(hy.to_bits().wrapping_sub(P));
    let a = mix_u64(mix_u64(BASIS, hx.to_bits()), hy.to_bits());
    let b = mix_u64(mix_u64(BASIS, hx2.to_bits()), hy2.to_bits());
    println!("half-extents ({hx:?}, {hy:?}) vs ({hx2:?}, {hy2:?})");
    println!("word mixer:  {:016x} {:016x} equal={}", a, b, a == b);
    let (fa, fb) = (fnv1a64(&le(&[hx, hy])), fnv1a64(&le(&[hx2, hy2])));
    println!("FNV-1a 64:   {:016x} {:016x} equal={}", fa, fb, fa == fb);
    let (xa, xb) = (xxh3_64(&le(&[hx, hy])), xxh3_64(&le(&[hx2, hy2])));
    println!("xxh3_64:     {:016x} {:016x} equal={}", xa, xb, xa == xb);
}
```
Expected output: `half-extents (0.5, 0.5) vs (0.5000000000000001, 0.49993896484372585) word mixer:  d1b28807b4eb6fed d1b28807b4eb6fed equal=true FNV-1a 64:   271be7d4e51a6a45 4ed1ef0e2cfee083 equal=false xxh3_64:     f`

*Check 6: xxh3 streamed in five chunkings equals the one-shot xxh3_64 of the same 1840 bytes* · `runs` · edition 2021 · host · bin · deps: xxhash_rust · **✔ oracle pass**
```rust
use xxhash_rust::xxh3::{xxh3_64, Xxh3};

fn main() {
    // A 1840-byte stand-in for a snapshot: 230 little-endian f64 words.
    let snap: Vec<u8> = (0..230).flat_map(|i| (i as f64 * 0.125 - 7.0).to_le_bytes()).collect();
    let one_shot = xxh3_64(&snap);
    let mut all_same = true;
    for chunk in [1usize, 7, 8, 64, 1000] {
        let mut h = Xxh3::new();
        for piece in snap.chunks(chunk) {
            h.update(piece);
        }
        all_same &= h.digest() == one_shot;
    }
    println!("{} bytes, xxh3_64 {:016x}, streamed in 5 chunkings equal: {}", snap.len(), one_shot, all_same);
}
```
Expected output: `1840 bytes, xxh3_64 bd87493de0eb502a, streamed in 5 chunkings equal: true`

## Prove the record complete twice: replay seed plus stamped inputs, and save-restore-rerun every quantum
**Replay from the seed and the tick-stamped admitted inputs proves the inputs are the whole cause; saving, restoring into a fresh world and resimulating proves the snapshot is the whole state, and only an every-quantum sync test (GGRS's SyncTestSession, check distance of at least 2) cannot pass vacuously.**

*Check 1: Replay from seed plus tick-stamped inputs matches; an input one quantum late diverges at 40* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// The record is the seed plus the admitted inputs, each stamped with the quantum
// it applies to. Replay reruns the law from that record and compares the hash chain.
#[derive(Clone, Copy)]
struct Input { tick: u64, body: usize, dvy: f64 }

fn fnv(h: u64, bytes: &[u8]) -> u64 {
    let mut h = h;
    for &b in bytes { h = (h ^ b as u64).wrapping_mul(0x100000001b3); }
    h
}

fn run(seed: u64, log: &[Input], ticks: u64) -> Vec<u64> {
    // The seed fixes the initial heights through a fixed integer generator.
    let mut s = seed;
    let mut y = [0.0f64; 4];
    for yi in y.iter_mut() {
        s ^= s << 13; s ^= s >> 7; s ^= s << 17;
        *yi = (s % 1024) as f64 / 256.0; // 0 .. 4 m in steps of 1/256
    }
    let mut vy = [0.0f64; 4];
    let mut chain = Vec::new();
    let mut h: u64 = 0xcbf29ce484222325;
    for tick in 0..ticks {
        for inp in log.iter().filter(|i| i.tick == tick) {
            vy[inp.body] += inp.dvy;
        }
        for i in 0..4 {
            vy[i] += -8.0 / 64.0;
            y[i] += vy[i] / 64.0;
            if y[i] < 0.0 { y[i] = 0.0; vy[i] = 0.0; }
            h = fnv(h, &y[i].to_le_bytes());
            h = fnv(h, &vy[i].to_le_bytes());
        }
        chain.push(h);
    }
    chain
}

fn first_difference(a: &[u64], b: &[u64]) -> Option<usize> {
    a.iter().zip(b).position(|(x, y)| x != y)
}

fn main() {
    let seed = 0x5eed;
    let log = [Input { tick: 40, body: 2, dvy: 3.0 }, Input { tick: 90, body: 0, dvy: 2.5 }];
    let played = run(seed, &log, 256);
    let replayed = run(seed, &log, 256);
    println!("replay: {:?}", first_difference(&played, &replayed));
    let shifted = [Input { tick: 41, body: 2, dvy: 3.0 }, log[1]];
    println!("input stamped one quantum late: first difference at tick {:?}", first_difference(&played, &run(seed, &shifted, 256)));
    println!("other seed: first difference at tick {:?}", first_difference(&played, &run(seed + 1, &log, 256)));
}
```
Expected output: `replay: None input stamped one quantum late: first difference at tick Some(40) other seed: first difference at tick Some(0)`

*Check 2: A snapshot missing a rest counter passes a restore at 20, fails at 40; the sync test finds 53* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// Save / restore / rerun as a completeness test. The law keeps a per-body
// rest counter (like a solver's time-since-can-sleep): a body at rest for 32
// quanta falls asleep, and the trace records the sleep flag.
const SLEEP_QUANTA: u32 = 32;

#[derive(Clone, PartialEq, Debug)]
struct World { y: Vec<f64>, vy: Vec<f64>, rest: Vec<u32>, asleep: Vec<bool> }

impl World {
    fn new(heights: &[f64]) -> World {
        let n = heights.len();
        World { y: heights.to_vec(), vy: vec![0.0; n], rest: vec![0; n], asleep: vec![false; n] }
    }
    fn step(&mut self) {
        for i in 0..self.y.len() {
            if self.asleep[i] { continue; }
            self.vy[i] += -8.0 / 64.0;
            self.y[i] += self.vy[i] / 64.0;
            if self.y[i] <= 0.0 { self.y[i] = 0.0; self.vy[i] = 0.0; }
            if self.y[i] == 0.0 && self.vy[i] == 0.0 { self.rest[i] += 1 } else { self.rest[i] = 0 }
            if self.rest[i] >= SLEEP_QUANTA { self.asleep[i] = true; }
        }
    }
    // What the trace hashes each quantum: pose, velocity, sleep flag.
    fn trace_hash(&self) -> u64 {
        let mut h: u64 = 0xcbf29ce484222325;
        let mut put = |bytes: &[u8]| for &b in bytes { h = (h ^ b as u64).wrapping_mul(0x100000001b3) };
        for i in 0..self.y.len() {
            put(&self.y[i].to_le_bytes());
            put(&self.vy[i].to_le_bytes());
            put(&[self.asleep[i] as u8]);
        }
        h
    }
    // A snapshot as little-endian bytes. `with_rest` decides whether the counter is saved.
    fn save(&self, with_rest: bool) -> Vec<u8> {
        let mut out = Vec::new();
        for i in 0..self.y.len() {
            out.extend_from_slice(&self.y[i].to_le_bytes());
            out.extend_from_slice(&self.vy[i].to_le_bytes());
            out.push(self.asleep[i] as u8);
            if with_rest { out.extend_from_slice(&self.rest[i].to_le_bytes()); }
        }
        out
    }
    fn restore(n: usize, bytes: &[u8], with_rest: bool) -> World {
        let mut w = World::new(&vec![0.0; n]);
        let mut at = 0;
        let mut take = |len: usize| { let s = &bytes[at..at + len]; at += len; s };
        for i in 0..n {
            w.y[i] = f64::from_le_bytes(take(8).try_into().unwrap());
            w.vy[i] = f64::from_le_bytes(take(8).try_into().unwrap());
            w.asleep[i] = take(1)[0] == 1;
            if with_rest { w.rest[i] = u32::from_le_bytes(take(4).try_into().unwrap()); }
        }
        w
    }
}

// Run to `total`, save at `at`, restore into a fresh world, rerun, name the first differing quantum.
fn restore_rerun(with_rest: bool, at: usize, total: usize) -> Option<usize> {
    let heights = [0.5, 1.0, 2.0];
    let mut w = World::new(&heights);
    let mut trace = Vec::new();
    let mut snap = Vec::new();
    for q in 0..total {
        if q == at { snap = w.save(with_rest); }
        w.step();
        trace.push(w.trace_hash());
    }
    let mut r = World::restore(heights.len(), &snap, with_rest);
    (at..total).find(|&q| { r.step(); r.trace_hash() != trace[q] })
}

// GGRS-style: every quantum, save, step, then roll back `distance` quanta and resimulate.
fn sync_test(with_rest: bool, distance: usize, total: usize) -> Option<usize> {
    let heights = [0.5, 1.0, 2.0];
    let mut w = World::new(&heights);
    let mut saves: Vec<Vec<u8>> = Vec::new();
    let mut hashes: Vec<u64> = Vec::new();
    for q in 0..total {
        saves.push(w.save(with_rest));
        w.step();
        hashes.push(w.trace_hash());
        if q + 1 >= distance {
            let from = q + 1 - distance;
            let mut r = World::restore(heights.len(), &saves[from], with_rest);
            for k in from..=q {
                r.step();
                if r.trace_hash() != hashes[k] { return Some(k); }
            }
        }
    }
    None
}

fn main() {
    println!("restore at 20, rest counter left out: {:?}", restore_rerun(false, 20, 200));
    println!("restore at 40, rest counter left out: {:?}", restore_rerun(false, 40, 200));
    println!("restore at 40, complete snapshot: {:?}", restore_rerun(true, 40, 200));
    println!("sync test distance 2, rest counter left out: {:?}", sync_test(false, 2, 200));
    println!("sync test distance 2, complete snapshot: {:?}", sync_test(true, 2, 200));
}
```
Expected output: `restore at 20, rest counter left out: None restore at 40, rest counter left out: Some(53) restore at 40, complete snapshot: None sync test distance 2, rest counter left out: Some(53) sync test distanc`

## Read world files with serde_json's float_roundtrip, refuse unknown fields, and hash parsed bits, not text
**With `float_roundtrip`, serde_json 1.0.151 turns f64 into JSON and back bit-exactly (200,000 arbitrary finite values, none changed) and parses as std's correctly rounded `str::parse` does; its text is not a stable artefact (1.0.147 swapped Ryū for Żmij and exponents gained a '+'), and NaN or infinity serialise as null, so validate before writing and hash parsed values.**

*Check 1: 200,000 arbitrary finite f64 survive to_string then from_str bit-exactly and match str::parse* · `runs` · edition 2021 · host · bin · deps: serde_json · **✔ oracle pass**
```rust
// f64 -> JSON text -> f64 through serde_json built with `float_roundtrip`.
fn main() {
    let mut s: u64 = 0x9E37_79B9_7F4A_7C15;
    let mut tested = 0u32;
    let mut mismatched = 0u32;
    let mut disagree_with_std = 0u32;
    while tested < 200_000 {
        // xorshift64: a fixed sequence of arbitrary bit patterns
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        let x = f64::from_bits(s);
        if !x.is_finite() {
            continue;
        }
        tested += 1;
        let text = serde_json::to_string(&x).unwrap();
        let back: f64 = serde_json::from_str(&text).unwrap();
        if back.to_bits() != x.to_bits() {
            mismatched += 1;
        }
        let by_std: f64 = text.parse().unwrap();
        if by_std.to_bits() != back.to_bits() {
            disagree_with_std += 1;
        }
    }
    // Long decimals: serde_json's parse must equal std's correctly rounded parse.
    let long = [
        "0.1000000000000000055511151231257827021181583404541015625",
        "2.2250738585072011e-308",
        "4.9406564584124654e-324",
        "1.00000000000000011102230246251565404236316680908203125",
        "9007199254740993.0",
    ];
    let mut long_ok = 0;
    for t in long {
        let a: f64 = serde_json::from_str(t).unwrap();
        let b: f64 = t.parse().unwrap();
        if a.to_bits() == b.to_bits() {
            long_ok += 1;
        }
    }
    println!("{tested} finite values, {mismatched} changed bits, {disagree_with_std} differ from str::parse, long decimals {long_ok}/5");
}
```
Expected output: `200000 finite values, 0 changed bits, 0 differ from str::parse, long decimals 5/5`

*Check 2: serde_json 1.0.151 float text: 1e+21, 0.000025, -0.0; NaN and inf become null; 1e400 refused* · `runs` · edition 2021 · host · bin · deps: serde_json · **✔ oracle pass**
```rust
fn main() {
    let xs: [f64; 12] = [0.1, 1.0, -0.0, 1e21, 1e-7, 5e-324, 1.0 / 3.0, 123456789.0, 1e15, 1e16, 2.5e-5, f64::MAX];
    for x in xs {
        println!("{}", serde_json::to_string(&x).unwrap());
    }
    println!("{}", serde_json::to_string(&vec![f64::NAN, f64::INFINITY]).unwrap());
    let back: Result<Vec<f64>, _> = serde_json::from_str("[null]");
    println!("{}", back.unwrap_err());
    let big: Result<f64, _> = serde_json::from_str("1e400");
    println!("{}", big.unwrap_err());
    let js_style: f64 = serde_json::from_str("1e+21").unwrap();
    println!("{}", js_style.to_bits() == 1e21f64.to_bits());
}
```
Expected output: `0.1 1.0 -0.0 1e+21 1e-7 5e-324 0.3333333333333333 123456789.0 1000000000000000.0 1e+16 0.000025 1.7976931348623157e+308 [null,null] invalid type: null, expected f64 at line 1 column 5 number out of ra`

*Check 3: deny_unknown_fields refuses an extra key; duplicate keys and bare NaN are refused; -0.0 survives* · `runs` · edition 2021 · host · bin · deps: serde, serde_json · **✔ oracle pass**
```rust
use serde::Deserialize;

#[derive(Debug, Deserialize)]
#[serde(deny_unknown_fields)]
struct Body { id: String, x: f64, y: f64, z: f64 }

fn main() {
    let ok: Result<Body, _> = serde_json::from_str(r#"{"id":"crate","x":2,"y":0.5,"z":-0.0}"#);
    let b = ok.unwrap();
    println!("x {:?} y {:?} z {:?} (z bits {:016x}) id {}", b.x, b.y, b.z, b.z.to_bits(), b.id);
    let unknown: Result<Body, _> = serde_json::from_str(r#"{"id":"crate","x":2,"y":0.5,"z":0,"mass":3}"#);
    println!("{}", unknown.unwrap_err());
    let dup: Result<Body, _> = serde_json::from_str(r#"{"id":"crate","x":2,"x":3,"y":0.5,"z":0}"#);
    println!("{}", dup.unwrap_err());
    let nan: Result<Body, _> = serde_json::from_str(r#"{"id":"crate","x":NaN,"y":0.5,"z":0}"#);
    println!("{}", nan.unwrap_err());
}
```
Expected output: `x 2.0 y 0.5 z -0.0 (z bits 8000000000000000) id crate unknown field `mass`, expected one of `id`, `x`, `y`, `z` at line 1 column 40 duplicate field `x` at line 1 column 23 expected value at line 1 col`

## Stop feeding u32-only streams to both FNV-1a lanes: such a digest repeats one 32-bit half
**packages/frame/hash.js mixes every u32 into both lanes from the same basis, so a digest built only from u32 input — the T1 trace's snapshot digest and the snapshot digests T3 adds to the behaviour file — has identical halves and carries 32 bits; frame hashes keep the lanes apart because each double's low and high words go to different lanes.**

*Check 1: A Rust port of the two-lane FNV-1a prints the digest hash.js prints for the same input* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// A Rust port of the engine's frame hash (packages/frame/hash.js): two FNV-1a
// 32-bit lanes; a double's low little-endian word feeds lane 0, its high word
// lane 1; words and text feed both lanes; NaN is refused.
struct FrameHash { h0: u32, h1: u32 }

impl FrameHash {
    const BASIS: u32 = 0x811c_9dc5;
    const PRIME: u32 = 0x0100_0193;
    fn new() -> Self { FrameHash { h0: Self::BASIS, h1: Self::BASIS } }
    fn mix(mut h: u32, word: u32) -> u32 {
        for b in word.to_le_bytes() {
            h = (h ^ b as u32).wrapping_mul(Self::PRIME);
        }
        h
    }
    fn u32(&mut self, w: u32) {
        self.h0 = Self::mix(self.h0, w);
        self.h1 = Self::mix(self.h1, w);
    }
    fn float(&mut self, x: f64) -> bool {
        if x.is_nan() {
            return false;
        }
        let bits = x.to_bits();
        self.h0 = Self::mix(self.h0, bits as u32);
        self.h1 = Self::mix(self.h1, (bits >> 32) as u32);
        true
    }
    fn text(&mut self, s: &str) {
        let units: Vec<u16> = s.encode_utf16().collect();
        self.u32(units.len() as u32);
        for u in units {
            self.u32(u as u32);
        }
    }
    fn digest(&self) -> String { format!("{:08x}{:08x}", self.h0, self.h1) }
}

fn main() {
    let mut h = FrameHash::new();
    h.u32(7);
    for x in [0.5, -8.0, 1.0 / 64.0, 1e-300, 3.141592653589793, -0.0] {
        assert!(h.float(x));
    }
    h.text("box");
    println!("{}", h.digest());
    println!("{}", FrameHash::new().digest());
    println!("{}", FrameHash::new().float(f64::NAN));
}
```
Expected output: `81b14261d3a75682 811c9dc5811c9dc5 false`

*Check 2: u32-only input repeats a half, a double splits them, fixes A-C differ, and 32 bits collide* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::collections::HashMap;

// The engine's frame hasher (packages/frame/hash.js), ported: two FNV-1a 32-bit
// lanes; u32 words go to BOTH lanes; a double's low word goes to lane 0, its high word to lane 1.
#[derive(Clone, Copy)]
struct Lanes { h0: u32, h1: u32 }
const BASIS: u32 = 0x811c_9dc5;
const PRIME: u32 = 0x0100_0193;
fn mix(mut h: u32, word: u32) -> u32 {
    for b in word.to_le_bytes() { h = (h ^ b as u32).wrapping_mul(PRIME); }
    h
}
impl Lanes {
    fn new() -> Self { Lanes { h0: BASIS, h1: BASIS } }
    fn u32(&mut self, w: u32) { self.h0 = mix(self.h0, w); self.h1 = mix(self.h1, w); }
    fn float(&mut self, x: f64) { let b = x.to_bits(); self.h0 = mix(self.h0, b as u32); self.h1 = mix(self.h1, (b >> 32) as u32); }
    fn digest(&self) -> u64 { ((self.h0 as u64) << 32) | self.h1 as u64 }
}

// Today's snapshot digest (harness/trace-line.mjs snapshotField): length, then every byte as a u32.
fn digest_today(snap: &[u8]) -> u64 {
    let mut h = Lanes::new();
    h.u32(snap.len() as u32);
    for &b in snap { h.u32(b as u32); }
    h.digest()
}
// Fix A: split the stream across the lanes the way a double is split (low 4 bytes lane 0, high 4 lane 1).
fn digest_split(snap: &[u8]) -> u64 {
    let mut h = Lanes::new();
    h.u32(snap.len() as u32);
    for w in snap.chunks(8) {
        let mut word = [0u8; 8];
        word[..w.len()].copy_from_slice(w);
        h.h0 = mix(h.h0, u32::from_le_bytes(word[0..4].try_into().unwrap()));
        h.h1 = mix(h.h1, u32::from_le_bytes(word[4..8].try_into().unwrap()));
    }
    h.digest()
}
// Fix B: give each lane a different image of a u32 (lane 1 sees it bit-reversed).
fn digest_distinct(snap: &[u8]) -> u64 {
    let mut h = Lanes::new();
    let mut put = |w: u32| { h.h0 = mix(h.h0, w); h.h1 = mix(h.h1, w.reverse_bits()); };
    put(snap.len() as u32);
    for &b in snap { put(b as u32); }
    h.digest()
}
// Fix C: FNV-1a 64 (RFC 9923) over the length and the bytes.
fn digest_fnv64(snap: &[u8]) -> u64 {
    let mut h: u64 = 0xcbf2_9ce4_8422_2325;
    for b in (snap.len() as u32).to_le_bytes().iter().chain(snap) { h = (h ^ *b as u64).wrapping_mul(0x0000_0100_0000_01b3); }
    h
}

fn main() {
    let snap: Vec<u8> = [0.25f64, -8.0, 1.0 / 64.0].iter().flat_map(|x| x.to_le_bytes()).collect();
    println!("u32-only input:   {:016x}", digest_today(&snap));
    let mut frame = Lanes::new();
    frame.u32(1);
    frame.float(0.25);
    println!("with a double:    {:016x}", frame.digest());
    println!("fix A split:      {:016x}", digest_split(&snap));
    println!("fix B distinct:   {:016x}", digest_distinct(&snap));
    println!("fix C FNV-1a 64:  {:016x}", digest_fnv64(&snap));
    // 32 bits of state: search one-word snapshots (arbitrary bit patterns from a
    // fixed xorshift sequence) for two that share today's digest.
    let mut seen: HashMap<u64, [u8; 8]> = HashMap::new();
    let mut x: u64 = 0x9e37_79b9_7f4a_7c15;
    for n in 1u32..=1_000_000 {
        x ^= x << 13; x ^= x >> 7; x ^= x << 17;
        let s = x.to_le_bytes();
        let d = digest_today(&s);
        if let Some(t) = seen.get(&d) {
            println!("collision after {n} snapshots: {:016x} and {:016x} both digest to {d:016x}", u64::from_le_bytes(*t), x);
            println!("  still equal under fix A {}, fix B {}, fix C {}", digest_split(&s) == digest_split(t), digest_distinct(&s) == digest_distinct(t), digest_fnv64(&s) == digest_fnv64(t));
            break;
        }
        seen.insert(d, s);
    }
}
```
Expected output: `u32-only input:   d990006dd990006d with a double:    3e80124425092999 fix A split:      51fd4f1de54696bd fix B distinct:   d990006d08bb077e fix C FNV-1a 64:  05d863786a65fcad collision after 125346 sn`

## Version the law with golden hashes plus behaviour numbers, so each golden move names what moved
**A golden hash says only that something changed; behaviour numbers recorded beside it — each body's sleep quantum, final positions, snapshot length and digest — checked by the same test and rewritten by the same command turn a move into a named, reviewable change, as Box2D's CI does with its step count to sleep and a hash of the resting transforms.**

*Check 1: Golden hash and behaviour numbers as #[test]s: both pass for the pinned law* · `runs` · edition 2021 · host · test · output has “test result: ok. 2 passed” · **✔ oracle pass**
```rust
// A law's golden hash and the behaviour numbers recorded beside it, as tests.
// `--cfg law_bump` models a law change: a restitution rule is added.
const DT: f64 = 1.0 / 64.0;
const SLEEP_QUANTA: u32 = 32;
#[cfg(not(law_bump))]
const BOUNCE: f64 = 0.0;
#[cfg(law_bump)]
const BOUNCE: f64 = 0.25;

pub struct Outcome { pub hash: u64, pub sleep_quantum: Option<u32>, pub rest_height: f64 }

pub fn run() -> Outcome {
    let (mut y, mut vy, mut rest) = (2.0f64, 0.0f64, 0u32);
    let mut h: u64 = 0xcbf29ce484222325;
    let mut sleep_quantum = None;
    for q in 1..=400u32 {
        vy += -8.0 * DT;
        y += vy * DT;
        if y <= 0.0 {
            y = 0.0;
            vy = -vy * BOUNCE;
            if vy < 0.05 { vy = 0.0; }
        }
        rest = if y == 0.0 && vy == 0.0 { rest + 1 } else { 0 };
        for b in y.to_le_bytes().into_iter().chain(vy.to_le_bytes()) {
            h = (h ^ b as u64).wrapping_mul(0x100000001b3);
        }
        if rest >= SLEEP_QUANTA { sleep_quantum = Some(q); break; }
    }
    Outcome { hash: h, sleep_quantum, rest_height: y }
}

// Written together by one `write-golden` step; a rewrite states which number moved.
const GOLDEN_HASH: u64 = 0x16182f0f3e959493;
const GOLDEN_SLEEP_QUANTUM: Option<u32> = Some(76);
const GOLDEN_REST_HEIGHT: f64 = 0.0;

#[test]
fn golden_hash() {
    assert_eq!(run().hash, GOLDEN_HASH, "golden moved");
}

#[test]
fn behaviour_numbers() {
    let o = run();
    assert_eq!(o.sleep_quantum, GOLDEN_SLEEP_QUANTUM, "behaviour moved: sleep quantum");
    assert_eq!(o.rest_height.to_bits(), GOLDEN_REST_HEIGHT.to_bits(), "behaviour moved: rest height");
}
```

*Check 2: A bumped law fails both tests; only the behaviour test says what moved (sleep 76 -> 104)* · `runs` · edition 2021 · host · test · output has “golden moved” · output has “behaviour moved: sleep quantum” · output has “left: Some(104)” · output has “right: Some(76)” · output has “test result: FAILED. 0 passed; 2 failed” · exit code 101 · **✔ oracle pass**
```rust
// A law's golden hash and the behaviour numbers recorded beside it, as tests.
// `--cfg law_bump` models a law change: a restitution rule is added.
const DT: f64 = 1.0 / 64.0;
const SLEEP_QUANTA: u32 = 32;
#[cfg(not(law_bump))]
const BOUNCE: f64 = 0.0;
#[cfg(law_bump)]
const BOUNCE: f64 = 0.25;

pub struct Outcome { pub hash: u64, pub sleep_quantum: Option<u32>, pub rest_height: f64 }

pub fn run() -> Outcome {
    let (mut y, mut vy, mut rest) = (2.0f64, 0.0f64, 0u32);
    let mut h: u64 = 0xcbf29ce484222325;
    let mut sleep_quantum = None;
    for q in 1..=400u32 {
        vy += -8.0 * DT;
        y += vy * DT;
        if y <= 0.0 {
            y = 0.0;
            vy = -vy * BOUNCE;
            if vy < 0.05 { vy = 0.0; }
        }
        rest = if y == 0.0 && vy == 0.0 { rest + 1 } else { 0 };
        for b in y.to_le_bytes().into_iter().chain(vy.to_le_bytes()) {
            h = (h ^ b as u64).wrapping_mul(0x100000001b3);
        }
        if rest >= SLEEP_QUANTA { sleep_quantum = Some(q); break; }
    }
    Outcome { hash: h, sleep_quantum, rest_height: y }
}

// Written together by one `write-golden` step; a rewrite states which number moved.
const GOLDEN_HASH: u64 = 0x16182f0f3e959493;
const GOLDEN_SLEEP_QUANTUM: Option<u32> = Some(76);
const GOLDEN_REST_HEIGHT: f64 = 0.0;

#[test]
fn golden_hash() {
    assert_eq!(run().hash, GOLDEN_HASH, "golden moved");
}

#[test]
fn behaviour_numbers() {
    let o = run();
    assert_eq!(o.sleep_quantum, GOLDEN_SLEEP_QUANTUM, "behaviour moved: sleep quantum");
    assert_eq!(o.rest_height.to_bits(), GOLDEN_REST_HEIGHT.to_bits(), "behaviour moved: rest height");
}
```

## Run the law on integer quanta from a host-owned accumulator; keep render interpolation out of the state
**A 1/64 s quantum is exact in binary, so the law counts time as an integer tick; the host's accumulator, kept in integer nanoseconds, decides how many quanta a frame runs and the render alpha, and neither the alpha nor any clock value reaches the hashed state.**

*Check 1: 64 steps of 1/64 sum to exactly 1.0; 60 of 1/60 do not, and an hour of 1/60 drifts* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let q64: f64 = 1.0 / 64.0;
    let q60: f64 = 1.0 / 60.0;
    let mut t64 = 0.0f64;
    let mut t60 = 0.0f64;
    for _ in 0..64 { t64 += q64; }
    for _ in 0..60 { t60 += q60; }
    println!("64 x 1/64 = {:?} exact={}", t64, t64 == 1.0);
    println!("60 x 1/60 = {:?} exact={}", t60, t60 == 1.0);
    // drift after one hour of quanta, accumulated vs tick * dt
    let mut acc = 0.0f64;
    let n: u64 = 60 * 60 * 60;
    for _ in 0..n { acc += q60; }
    println!("1h of 1/60: accumulated {:?} vs ticks*dt {:?}", acc, n as f64 * q60);
    let mut acc64 = 0.0f64;
    let n64: u64 = 64 * 60 * 60;
    for _ in 0..n64 { acc64 += q64; }
    println!("1h of 1/64: accumulated {:?} vs ticks*dt {:?} same={}", acc64, n64 as f64 * q64, acc64 == n64 as f64 * q64);
    // Duration: 1/64 s is 15_625_000 ns exactly
    let d = std::time::Duration::from_nanos(15_625_000);
    println!("64 x 15625000ns = {:?}", d * 64);
    println!("1/60 s as Duration = {:?}", std::time::Duration::from_secs_f64(q60));
}
```
Expected output: `64 x 1/64 = 1.0 exact=true 60 x 1/60 = 1.0000000000000013 exact=false 1h of 1/60: accumulated 3600.0000000182276 vs ticks*dt 3600.0 1h of 1/64: accumulated 3600.0 vs ticks*dt 3600.0 same=true 64 x 156`

*Check 2: Integer-ns accumulator runs 64 quanta at 60-240 Hz; an f64 one runs 63 at 60, 120 and 144 Hz* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
// The host owns the clock: an integer nanosecond accumulator turns frame deltas
// into whole quanta of 1/64 s. The law sees only the quantum count.
const QUANTUM_NS: u64 = 15_625_000; // 1/64 s, exact

fn law_hash(quanta: u64) -> u64 {
    let (mut y, mut vy) = (2.0f64, 0.0f64);
    for _ in 0..quanta {
        vy += -8.0 / 64.0;
        y += vy / 64.0;
        if y < 0.0 { y = 0.0; vy = 0.0; }
    }
    let mut h: u64 = 0xcbf29ce484222325;
    for b in y.to_le_bytes().into_iter().chain(vy.to_le_bytes()) {
        h = (h ^ b as u64).wrapping_mul(0x100000001b3);
    }
    h
}

fn quanta_int(frame_ns: u64, frames: u64) -> u64 {
    let (mut acc, mut n) = (0u64, 0u64);
    for _ in 0..frames {
        acc += frame_ns;
        while acc >= QUANTUM_NS { acc -= QUANTUM_NS; n += 1; }
    }
    n
}

fn quanta_f64(frame_s: f64, frames: u64) -> u64 {
    let (mut acc, mut n) = (0.0f64, 0u64);
    let dt = 1.0 / 64.0;
    for _ in 0..frames {
        acc += frame_s;
        while acc >= dt { acc -= dt; n += 1; }
    }
    n
}

fn main() {
    // One second of wall time at 60, 120, 144 and 240 Hz, with frame times in whole ns.
    for (hz, frame_ns) in [(60u64, 16_666_667u64), (120, 8_333_334), (144, 6_944_445), (240, 4_166_667)] {
        let n = quanta_int(frame_ns, hz);
        println!("int ns {hz:>3} Hz: {n} quanta, law hash {:016x}", law_hash(n));
    }
    for hz in [60u64, 120, 144, 240] {
        let n = quanta_f64(1.0 / hz as f64, hz);
        println!("f64 s  {hz:>3} Hz: {n} quanta");
    }
}
```
Expected output: `int ns  60 Hz: 64 quanta, law hash 88201fb960ff6465 int ns 120 Hz: 64 quanta, law hash 88201fb960ff6465 int ns 144 Hz: 64 quanta, law hash 88201fb960ff6465 int ns 240 Hz: 64 quanta, law hash 88201fb96`

*Check 3: Presentation writing a smoothed pose back through &State is E0594* · `compile_fail` · edition 2021 · host · lib · errors: E0594 · stderr has “which is behind a `&` reference” · **✔ oracle pass**
```rust
pub struct State { pub y: f64, pub vy: f64 }

// Presentation reads the law's state through a shared reference.
pub fn draw(state: &State, alpha: f64) -> f64 {
    state.y = state.y + state.vy * alpha / 64.0; // tries to write the smoothed pose back
    state.y
}
```

*Check 4: Interpolating between two committed states through shared references compiles clean* · `compiles` · edition 2021 · host · lib · no warnings · **✔ oracle pass**
```rust
pub struct State { pub y: f64, pub vy: f64 }

// Presentation blends the last two committed states by the host's alpha.
// It reads the law's state and returns a pose; nothing flows back.
pub fn draw(prev: &State, cur: &State, alpha: f64) -> f64 {
    prev.y + (cur.y - prev.y) * alpha
}
```

