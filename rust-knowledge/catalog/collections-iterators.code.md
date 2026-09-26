# Collections, iterators & closures — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](collections-iterators.md) · [catalog index](README.md)

## Assert equal lengths before zip, handle chunks_exact remainders, and collect into the target you mean
**`zip` ends when either input ends, without error; `windows(k)` yields len-k+1 overlapping slices; `chunks_exact(k)` omits the last len % k elements into `remainder()`; `collect` builds any `FromIterator` target: `Result<Vec<_>, E>` stops at the first Err, and a `BTreeMap` sorts by key and keeps one value per key.**

*Check 1: zip truncates, chunks_exact hides the tail, as_chunks/array_windows, Result collect stops at Err* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::collections::BTreeMap;
fn main() {
    let pos = [0.0f64, 1.0, 2.0, 3.0];
    let vel = [10.0f64, 20.0, 30.0];
    println!("zip pairs {} (pos {}, vel {})", pos.iter().zip(vel.iter()).count(), pos.len(), vel.len());
    let e: Vec<(usize, char)> = "abc".chars().enumerate().collect();
    let c: Vec<i32> = [1, 2].into_iter().chain([3]).collect();
    println!("enumerate {:?} chain {:?}", e, c);
    let d = [1, 2, 3, 4, 5, 6, 7];
    println!("windows(2) count {}", d.windows(2).count());
    let ce = d.chunks_exact(3);
    println!("chunks_exact remainder {:?}", ce.remainder());
    println!("chunks_exact sums {:?}", ce.map(|ch| ch.iter().sum::<i32>()).collect::<Vec<_>>());
    println!("chunks lens {:?}", d.chunks(3).map(|ch| ch.len()).collect::<Vec<_>>());
    let (rows, tail) = d.as_chunks::<3>();
    println!("as_chunks {:?} tail {:?}", rows, tail);
    println!("array_windows diffs {:?}", d.array_windows::<2>().map(|[a, b]| b - a).collect::<Vec<_>>());
    let s: String = ['r', 'u', 's', 't'].iter().collect();
    let m: BTreeMap<&str, usize> = ["b", "a", "c"].iter().enumerate().map(|(i, k)| (*k, i)).collect();
    let dup: BTreeMap<u32, char> = [(1, 'a'), (1, 'b')].into_iter().collect();
    println!("string {s}, btreemap {:?}, duplicate keys -> {} entry", m, dup.len());
    let mut seen = Vec::new();
    let r: Result<Vec<i32>, String> = ["1", "x", "3"]
        .iter()
        .map(|t| {
            seen.push(*t);
            t.parse::<i32>().map_err(|e| format!("{t}: {e}"))
        })
        .collect();
    println!("result {:?} after seeing {:?}", r, seen);
}
```
Expected output: `zip pairs 3 (pos 4, vel 3) enumerate [(0, 'a'), (1, 'b'), (2, 'c')] chain [1, 2, 3] windows(2) count 6 chunks_exact remainder [7] chunks_exact sums [6, 15] chunks lens [3, 3, 1] as_chunks [[1, 2, 3], `

## Choose iter, iter_mut or into_iter by ownership, and consume every adapter chain you build
**`for x in &v` iterates `&T` (iter), `for x in &mut v` iterates `&mut T` (iter_mut), `for x in v` consumes v and yields `T` (into_iter); adapters such as `map` are lazy and run nothing until consumed; from edition 2021, `array.into_iter()` yields values, while 2015/2018 resolve it to `(&array).into_iter()`.**

*Check 1: a bare map is lazy (unused_must_use, map_unit_fn) and prints nothing; iter_mut/into_iter work* · `runs` · edition 2024 · host · bin · lints: unused_must_use, map_unit_fn · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![1, 2, 3];
    v.iter().map(|x| println!("lazy {x}"));
    for x in &mut v {
        *x *= 10;
    }
    let total: i32 = v.iter().sum();
    let owned: Vec<String> = v.into_iter().map(|x| x.to_string()).collect();
    println!("total {total}, owned {:?}", owned);
}
```
Expected output: `total 60, owned ["10", "20", "30"]`

*Check 2: for x in v moves v; using v afterwards is E0382* · `compile_fail` · edition 2024 · host · bin · errors: E0382 · **✔ oracle pass**
```rust
fn main() {
    let v = vec![String::from("a"), String::from("b")];
    for s in v {
        println!("{s}");
    }
    println!("{}", v.len());
}
```

*Check 3: edition 2018: array.into_iter() yields &i32, so collecting Vec<i32> is E0277* · `compile_fail` · edition 2018 · host · bin · errors: E0277 · **✔ oracle pass**
```rust
fn main() {
    let a = [1, 2, 3];
    let v: Vec<i32> = a.into_iter().collect();
    println!("{:?}", v);
}
```

*Check 4: edition 2021: the same array.into_iter() yields i32 values* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let a = [1, 2, 3];
    let v: Vec<i32> = a.into_iter().collect();
    println!("{:?}", v);
}
```
Expected output: `[1, 2, 3]`

*Check 5: edition 2018: array.into_iter() in a for loop compiles by reference and warns array_into_iter* · `runs` · edition 2018 · host · bin · lints: array_into_iter · **✔ oracle pass**
```rust
fn main() {
    let a = [1, 2, 3];
    for x in a.into_iter() {
        let y: &i32 = x;
        println!("{}", y);
    }
}
```
Expected output: `1 2 3`

## Delete from a hashed Vec with remove/retain/drain, not swap_remove; pre-size it with with_capacity/reserve
**A Vec's order is its index order: remove, retain and drain keep it, swap_remove moves the last element into the hole, and capacity is only a lower bound whose growth the docs leave unspecified.**

*Check 1: with_capacity/reserve are lower bounds; swap_remove reorders, remove/retain/drain keep order* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let mut v: Vec<u32> = Vec::with_capacity(10);
    println!("len={} cap>=10:{}", v.len(), v.capacity() >= 10);
    v.extend([1, 2, 3]);
    v.reserve(100);
    println!("cap>=len+100:{}", v.capacity() >= v.len() + 100);
    let mut a = vec!['a', 'b', 'c', 'd'];
    a.swap_remove(1);
    let mut b = vec!['a', 'b', 'c', 'd'];
    b.remove(1);
    println!("swap_remove:{:?} remove:{:?}", a, b);
    let mut r = vec![1, 2, 3, 4, 5, 6];
    r.retain(|x| x % 2 == 0);
    let mut d = vec![1, 2, 3, 4, 5];
    let gone: Vec<i32> = d.drain(1..3).collect();
    println!("retain:{:?} drained:{:?} left:{:?}", r, gone, d);
    let mut e = vec![0u8; 64];
    let cap = e.capacity();
    e.clear();
    println!("clear keeps capacity:{}", e.capacity() == cap);
}
```
Expected output: `len=0 cap>=10:true cap>=len+100:true swap_remove:['a', 'd', 'c'] remove:['a', 'c', 'd'] retain:[2, 4, 6] drained:[2, 3] left:[1, 4, 5] clear keeps capacity:true`

*Check 2: swap_remove vs remove: same elements, different hash until both are sorted* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn fnv_fold(xs: &[u32]) -> u64 {
    xs.iter().fold(0xcbf2_9ce4_8422_2325u64, |h, &x| (h ^ x as u64).wrapping_mul(0x0000_0100_0000_01b3))
}
fn main() {
    let ids = vec![10u32, 11, 12, 13, 14];
    let mut a = ids.clone();
    a.swap_remove(1);
    let mut b = ids.clone();
    b.remove(1);
    let (mut sa, mut sb) = (a.clone(), b.clone());
    sa.sort_unstable();
    sb.sort_unstable();
    println!("same elements: {}", sa == sb);
    println!("same hash before sort: {}", fnv_fold(&a) == fnv_fold(&b));
    a.sort_unstable();
    b.sort_unstable();
    println!("same hash after sort: {}", fnv_fold(&a) == fnv_fold(&b));
}
```
Expected output: `same elements: true same hash before sort: false same hash after sort: true`

## Give every hashed sort a unique total key; if keys can tie, use stable sort_by, not sort_unstable_by
**`sort`, `sort_by` and `sort_by_key` preserve the initial order of equal elements; `sort_unstable*` 'may reorder equal elements', and since the 1.81 switch to ipnsort its docs no longer carry the pdqsort-era promise of 'a fixed seed to always provide deterministic behavior'. With a unique key, both produce identical output.**

*Check 1: stable keeps tie order; unstable keeps it at n=20, not at 21/100; unique key => identical* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn ties_in_input_order(v: &[(u32, u32)]) -> bool {
    v.windows(2).all(|w| w[0].0 != w[1].0 || w[0].1 < w[1].1)
}
fn main() {
    for n in [20u32, 21, 100] {
        let input: Vec<(u32, u32)> = (0..n).map(|i| ((i * 7) % 3, i)).collect();
        let mut s = input.clone();
        s.sort_by_key(|p| p.0);
        let mut u = input.clone();
        u.sort_unstable_by_key(|p| p.0);
        println!(
            "n={n}: stable keeps ties {} | unstable keeps ties {}",
            ties_in_input_order(&s),
            ties_in_input_order(&u)
        );
    }
    let input: Vec<(u32, u32)> = (0..1000u32).map(|i| ((i * 7919) % 97, i)).collect();
    let mut s = input.clone();
    s.sort_by(|a, b| a.0.cmp(&b.0).then(a.1.cmp(&b.1)));
    let mut u = input.clone();
    u.sort_unstable_by(|a, b| a.0.cmp(&b.0).then(a.1.cmp(&b.1)));
    println!("unique key (key, id): sort == sort_unstable: {}", s == u);
}
```
Expected output: `n=20: stable keeps ties true / unstable keeps ties true n=21: stable keeps ties true / unstable keeps ties false n=100: stable keeps ties true / unstable keeps ties false unique key (key, id): sort ==`

*Check 2: 1.98.1: a cyclic (non-total) comparator makes stable sort_by panic on this 50-element input* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
use std::cmp::Ordering;
fn main() {
    let n = 50u32;
    let mut v: Vec<u32> = (0..n).map(|i| (i * 7919) % n).collect();
    // rock-paper-scissors on residues mod 3: not transitive, so not a total order
    v.sort_by(|a, b| match (a % 3 + 3 - b % 3) % 3 {
        0 => Ordering::Equal,
        1 => Ordering::Greater,
        _ => Ordering::Less,
    });
    println!("returned");
}
```

## Let only Vec, VecDeque or BTreeMap/BTreeSet order reach an output; HashMap/HashSet order is random per map
**std defines iteration order for sequences (index 0 upward), VecDeque (front to back) and B-trees (key order); HashMap/HashSet iterate in 'arbitrary order' under a randomly seeded hasher that differs per map and per run, and BinaryHeap::iter/into_vec are arbitrary too.**

*Check 1: identical HashMaps iterate and Debug-print differently; BTree, VecDeque, sorted heap are ordered* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::collections::{BTreeMap, BTreeSet, BinaryHeap, HashMap, VecDeque};
fn main() {
    let mut a: HashMap<u32, u32> = HashMap::new();
    let mut b: HashMap<u32, u32> = HashMap::new();
    for k in 0..1000u32 {
        a.insert(k, k);
        b.insert(k, k);
    }
    println!("maps equal: {}", a == b);
    println!("same iteration order: {}", a.keys().eq(b.keys()));
    println!("same Debug text: {}", format!("{:?}", a) == format!("{:?}", b));
    let mut ks: Vec<u32> = a.keys().copied().collect();
    ks.sort_unstable();
    println!("sorted keys start: {:?}", &ks[..3]);
    let t: BTreeMap<u32, &str> = [(30, "c"), (10, "a"), (20, "b")].into_iter().collect();
    println!("btreemap: {:?}", t.keys().collect::<Vec<_>>());
    let s: BTreeSet<i32> = [3, -1, 2].into_iter().collect();
    println!("btreeset: {:?}", s);
    let mut q = VecDeque::new();
    q.push_back(2);
    q.push_back(3);
    q.push_front(1);
    println!("vecdeque: {:?}", q.iter().collect::<Vec<_>>());
    let h: BinaryHeap<i32> = [1, 5, 2, 4, 3].into_iter().collect();
    println!("heap iter: {:?}", h.iter().collect::<Vec<_>>());
    println!("heap into_sorted_vec: {:?}", h.into_sorted_vec());
}
```
Expected output: `maps equal: true same iteration order: false same Debug text: false sorted keys start: [0, 1, 2] btreemap: [10, 20, 30] btreeset: {-1, 2, 3} vecdeque: [1, 2, 3] heap iter: [5, 4, 2, 1, 3] heap into_so`

*Check 2: a BTreeMap keyed by f64 is rejected: f64 is not Ord (E0277)* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “the trait bound `f64: Ord` is not satisfied” · **✔ oracle pass**
```rust
use std::collections::BTreeMap;
pub fn index_by_depth(depths: &[f64]) -> BTreeMap<f64, usize> {
    let mut m = BTreeMap::new();
    for (i, d) in depths.iter().enumerate() {
        m.insert(*d, i);
    }
    m
}
```

## Return closures as impl Fn with move, and bound callbacks by the weakest Fn trait the call site needs
**A closure captures each variable in the first mode its body allows (shared borrow, unique borrow, mutable borrow, move) and implements FnOnce always, FnMut if it moves nothing out, Fn if it also mutates nothing; `move` forces by-value capture (a copy for Copy types) without changing which Fn traits apply.**

*Check 1: returning a closure that borrows a parameter is E0373* · `compile_fail` · edition 2024 · host · lib · errors: E0373 · **✔ oracle pass**
```rust
pub fn scaler(k: f64) -> impl Fn(f64) -> f64 {
    |x| x * k
}
```

*Check 2: calling a closure that moves a capture out twice is E0382* · `compile_fail` · edition 2024 · host · lib · errors: E0382 · **✔ oracle pass**
```rust
pub fn twice() {
    let name = String::from("orc");
    let consume = move || name;
    let a = consume();
    let b = consume();
    let _ = (a, b);
}
```

*Check 3: an inline mutating closure passed to an F: Fn() parameter is E0594* · `compile_fail` · edition 2024 · host · lib · errors: E0594 · **✔ oracle pass**
```rust
fn call_twice<F: Fn()>(f: F) {
    f();
    f();
}
pub fn g() {
    let mut n = 0;
    call_twice(|| n += 1);
}
```

*Check 4: an FnOnce closure bound to a variable, then passed to an F: Fn() parameter, is E0525* · `compile_fail` · edition 2024 · host · lib · errors: E0525 · **✔ oracle pass**
```rust
fn call_twice<F: Fn()>(f: F) {
    f();
    f();
}
pub fn g() {
    let s = String::from("x");
    let f = move || drop(s);
    call_twice(f);
}
```

*Check 5: FnMut accumulator, move copies a Copy capture, a move closure stays Fn, boxed dyn Fn* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn scaler(k: f64) -> impl Fn(f64) -> f64 {
    move |x| x * k
}
fn call_each<F: FnMut(u32)>(mut f: F) {
    for i in 1..=3 {
        f(i);
    }
}
fn main() {
    let mut total = 0;
    call_each(|i| total += i);
    println!("FnMut total {total}");
    let k = 3;
    let add_k = move |x: i32| x + k;
    println!("move copies Copy captures: {} and k is still {}", add_k(1), k);
    let names = vec![String::from("a"), String::from("b")];
    let count = move || names.len();
    println!("move closure is still Fn: {} {}", count(), count());
    let fs: Vec<Box<dyn Fn(f64) -> f64>> = vec![Box::new(scaler(2.0)), Box::new(|x| x + 1.0)];
    println!("boxed {:?}", fs.iter().map(|f| f(1.5)).collect::<Vec<_>>());
}
```
Expected output: `FnMut total 6 move copies Copy captures: 4 and k is still 3 move closure is still Fn: 2 2 boxed [3.0, 2.5]`

## Sort f64 with sort_by(f64::total_cmp), find first matches with partition_point, and dedup floats by bits
**f64 is not Ord, so `sort()`, `sort_by_key(|p| p.x)` and `BTreeMap<f64, _>` fail with E0277; `total_cmp` is IEEE 754 totalOrder (-NaN < -inf < ... < -0.0 < +0.0 < ... < +inf < +NaN); on a sorted slice `binary_search` may return any of several equal matches, and `dedup` removes only consecutive PartialEq-equal runs.**

*Check 1: sorting a Vec<f64> with sort() is rejected: f64 is not Ord (E0277)* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “the trait bound `f64: Ord` is not satisfied” · **✔ oracle pass**
```rust
pub fn order(v: &mut Vec<f64>) {
    v.sort();
}
```

*Check 2: sort_by_key with an f64 key is rejected the same way (E0277): the key must be Ord* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “the trait bound `f64: Ord` is not satisfied” · **✔ oracle pass**
```rust
pub fn by_depth(v: &mut Vec<(f64, u32)>) {
    v.sort_by_key(|p| p.0);
}
```

*Check 3: total_cmp order, cached-key call count, binary_search tie index, dedup vs dedup-by-bits* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::cell::Cell;
fn main() {
    let mut w = vec![1.0, f64::NAN, -0.0, 0.0, f64::NEG_INFINITY, -f64::NAN, -1.5];
    w.sort_by(f64::total_cmp);
    println!("{:?}", w);
    println!(
        "first is -NaN: {}, -0.0 before +0.0: {}",
        w[0].is_nan() && w[0].is_sign_negative(),
        w[3].is_sign_negative() && !w[4].is_sign_negative()
    );
    let data: Vec<u32> = (0..100u32).map(|i| (i * 37) % 100).collect();
    let calls = Cell::new(0u32);
    let mut a = data.clone();
    a.sort_by_key(|&x| {
        calls.set(calls.get() + 1);
        x
    });
    let by_key = calls.replace(0);
    let mut b = data.clone();
    b.sort_by_cached_key(|&x| {
        calls.set(calls.get() + 1);
        x.to_string()
    });
    println!("key calls: sort_by_key {} (>100: {}), sort_by_cached_key {}", by_key, by_key > 100, calls.get());
    let s = [1, 2, 2, 2, 3];
    println!(
        "binary_search(2) {:?}, partition_point {}, binary_search(4) {:?}",
        s.binary_search(&2),
        s.partition_point(|&x| x < 2),
        s.binary_search(&4)
    );
    let mut d = vec![1, 2, 2, 3, 2, 1];
    d.dedup();
    let mut e = vec![1, 2, 2, 3, 2, 1];
    e.sort();
    e.dedup();
    println!("dedup {:?}, sort+dedup {:?}", d, e);
    let mut f = vec![1.0f64, 1.0, -0.0, 0.0, f64::NAN, f64::NAN];
    f.dedup();
    let mut g = vec![1.0f64, 1.0, -0.0, 0.0, f64::NAN, f64::NAN];
    g.dedup_by(|a, b| a.to_bits() == b.to_bits());
    println!("f64 dedup {:?}, dedup by bits {:?}", f, g);
}
```
Expected output: `[NaN, -inf, -1.5, -0.0, 0.0, 1.0, NaN] first is -NaN: true, -0.0 before +0.0: true key calls: sort_by_key 1406 (>100: true), sort_by_cached_key 100 binary_search(2) Ok(3), partition_point 1, binary_se`

*Check 4: partial_cmp().unwrap() as a comparator panics as soon as a NaN is compared* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![2.0, f64::NAN, 1.0];
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    println!("unreachable: {:?}", v);
}
```

*Check 5: 1.98.1: NaN-as-Equal comparator makes sort_unstable_by panic on this 100-element input* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
use std::cmp::Ordering;
fn main() {
    let mut v: Vec<f64> = (0..100usize)
        .map(|i| if i % 5 == 0 { f64::NAN } else { ((i * 7919) % 1000) as f64 })
        .collect();
    v.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal));
    println!("returned");
}
```

*Check 6: 1.98.1: NaN-as-Equal sort_by over 1000 elements returns, but the numbers are left unsorted* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::cmp::Ordering;
fn main() {
    let mut v: Vec<f64> = (0..1000usize)
        .map(|i| if i % 5 == 0 { f64::NAN } else { ((i * 7919) % 1000) as f64 })
        .collect();
    v.sort_by(|a, b| a.partial_cmp(b).unwrap_or(Ordering::Equal));
    let nums: Vec<f64> = v.iter().copied().filter(|x| !x.is_nan()).collect();
    println!("returned; non-NaN values ascending: {}", nums.windows(2).all(|w| w[0] <= w[1]));
}
```
Expected output: `returned; non-NaN values ascending: false`

## Sum floats in one canonical order: iter().sum() is a left fold from -0.0 and reordering changes the bits
**For f16/f32/f64/f128, `Iterator::sum` is `iter.fold(-0.0, |a, b| a + b)` in iteration order (core at tag 1.98.1); float addition is not associative, so reversing or regrouping the same values changes the result, and an empty float sum is -0.0 since 1.82 (rust-lang/rust#129321).**

*Check 1: sum is fold(-0.0): order changes bits; empty sum is -0.0; canon() maps it to +0.0* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let xs = [0.1f64, 0.2, 0.3];
    let fwd: f64 = xs.iter().sum();
    let rev: f64 = xs.iter().rev().sum();
    println!("forward {:?} reverse {:?} same bits {}", fwd, rev, fwd.to_bits() == rev.to_bits());
    let folded = xs.iter().fold(-0.0, |a, &b| a + b);
    println!("sum == fold(-0.0) bitwise {}", folded.to_bits() == fwd.to_bits());
    let a: f64 = [1e16f64, 1.0, -1e16].iter().sum();
    let b: f64 = [1e16f64, -1e16, 1.0].iter().sum();
    println!("absorption {:?} vs {:?}", a, b);
    let empty: f64 = std::iter::empty::<f64>().sum();
    let empty_fold = std::iter::empty::<f64>().fold(0.0, |a, b| a + b);
    println!("empty sum {:?} (sign bit {}), empty fold(0.0) {:?}", empty, empty.is_sign_negative(), empty_fold);
    let canon = |x: f64| if x == 0.0 { 0.0 } else { x };
    println!("canon(empty) has +0.0 bits: {}", canon(empty).to_bits() == 0.0f64.to_bits());
}
```
Expected output: `forward 0.6000000000000001 reverse 0.6 same bits false sum == fold(-0.0) bitwise true absorption 0.0 vs 1.0 empty sum -0.0 (sign bit true), empty fold(0.0) 0.0 canon(empty) has +0.0 bits: true`

*Check 2: the same order effects survive -O: the optimiser does not regroup the additions* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let xs = [0.1f64, 0.2, 0.3];
    let fwd: f64 = xs.iter().sum();
    let rev: f64 = xs.iter().rev().sum();
    println!("forward {:?} reverse {:?} same bits {}", fwd, rev, fwd.to_bits() == rev.to_bits());
    let folded = xs.iter().fold(-0.0, |a, &b| a + b);
    println!("sum == fold(-0.0) bitwise {}", folded.to_bits() == fwd.to_bits());
    let a: f64 = [1e16f64, 1.0, -1e16].iter().sum();
    let b: f64 = [1e16f64, -1e16, 1.0].iter().sum();
    println!("absorption {:?} vs {:?}", a, b);
    let empty: f64 = std::iter::empty::<f64>().sum();
    let empty_fold = std::iter::empty::<f64>().fold(0.0, |a, b| a + b);
    println!("empty sum {:?} (sign bit {}), empty fold(0.0) {:?}", empty, empty.is_sign_negative(), empty_fold);
    let canon = |x: f64| if x == 0.0 { 0.0 } else { x };
    println!("canon(empty) has +0.0 bits: {}", canon(empty).to_bits() == 0.0f64.to_bits());
}
```
Expected output: `forward 0.6000000000000001 reverse 0.6 same bits false sum == fold(-0.0) bitwise true absorption 0.0 vs 1.0 empty sum -0.0 (sign bit true), empty fold(0.0) 0.0 canon(empty) has +0.0 bits: true`

## Treat str lengths as bytes, slice only on char boundaries, and keep Unicode case mapping out of hashed keys
**String and &str are always valid UTF-8: `len()` counts bytes, `s[i]` does not compile (E0277), `&s[a..b]` panics off a char boundary while `s.get(a..b)` returns None, and Unicode-aware methods follow `char::UNICODE_VERSION`, which the docs say changes over time without that being a breaking change.**

*Check 1: bytes vs chars, boundaries, get, from_utf8, UNICODE_VERSION, case mapping, format! (ASCII out)* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    // Non-ASCII results are printed with escape_default so stdout is plain ASCII on any console.
    let s = "héllo";
    println!("len {} chars {} first bytes {:?}", s.len(), s.chars().count(), s.bytes().take(3).collect::<Vec<u8>>());
    println!(
        "boundary(2) {} get(0..2) is None: {}, get(0..3) = {}",
        s.is_char_boundary(2),
        s.get(0..2).is_none(),
        s.get(0..3).unwrap_or("none").escape_default()
    );
    println!("char starts {:?}", s.char_indices().map(|(i, _)| i).collect::<Vec<_>>());
    let bad = [0x66u8, 0x6f, 0xff];
    println!(
        "from_utf8 invalid is_err {}, lossy replaced {}",
        String::from_utf8(bad.to_vec()).is_err(),
        String::from_utf8_lossy(&bad) == "fo\u{FFFD}"
    );
    println!("unicode {:?}", char::UNICODE_VERSION);
    println!(
        "{} {} {}",
        "Straße".to_uppercase(),
        "ÉLAN".to_ascii_lowercase().escape_default(),
        "orc".eq_ignore_ascii_case("ORC")
    );
    println!("[{:>8.3}] [{:<4}] [{:05}] [{:e}] [{}]", 3.14159f64, "hp", 42, 1500.0f64, 1e21f64);
}
```
Expected output: `len 6 chars 5 first bytes [104, 195, 169] boundary(2) false get(0..2) is None: true, get(0..3) = h\u{e9} char starts [0, 1, 3, 4, 5] from_utf8 invalid is_err true, lossy replaced true unicode (17, 0, `

*Check 2: slicing a String inside a multi-byte char panics at run time* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    let s = String::from("héllo");
    let t = &s[0..2];
    println!("{t}");
}
```

*Check 3: indexing a String with an integer is E0277* · `compile_fail` · edition 2024 · host · lib · errors: E0277 · stderr has “cannot be indexed by `{integer}`” · **✔ oracle pass**
```rust
pub fn first(s: &String) -> char {
    s[0]
}
```

## Use the map entry API for counters and get-or-insert instead of get_mut followed by insert
**`map.entry(k)` searches once and returns an Entry whose `or_insert`, `or_insert_with`, `or_default` and `and_modify` give `&mut V`; the hand-written get_mut / insert / get_mut function that returns the reference is still rejected on 1.98.1 (E0499).**

*Check 1: get_mut, then insert, then get_mut returning the reference is rejected with E0499* · `compile_fail` · edition 2024 · host · lib · errors: E0499 · **✔ oracle pass**
```rust
use std::collections::HashMap;
pub fn slot<'m>(map: &'m mut HashMap<u32, Vec<u32>>, k: u32) -> &'m mut Vec<u32> {
    match map.get_mut(&k) {
        Some(v) => v,
        None => {
            map.insert(k, Vec::new());
            map.get_mut(&k).unwrap()
        }
    }
}
```

*Check 2: entry().or_default() returns &mut V; or_insert_with is lazy, or_insert(make()) is eager* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::collections::{BTreeMap, HashMap};
fn slot(m: &mut HashMap<u32, Vec<u32>>, k: u32) -> &mut Vec<u32> {
    m.entry(k).or_default()
}
fn main() {
    let mut m: HashMap<u32, Vec<u32>> = HashMap::new();
    slot(&mut m, 7).push(1);
    slot(&mut m, 7).push(2);
    println!("slot 7: {:?}", m[&7]);
    let mut counts: BTreeMap<&str, u32> = BTreeMap::new();
    for w in "b a b c b a".split(' ') {
        *counts.entry(w).or_insert(0) += 1;
    }
    println!("counts: {:?}", counts);
    let mut hp: BTreeMap<&str, i32> = BTreeMap::new();
    for _ in 0..2 {
        hp.entry("orc").and_modify(|h| *h -= 5).or_insert(100);
    }
    println!("hp: {:?}", hp);
    let mut built = 0;
    let mut lazy: BTreeMap<u32, u32> = BTreeMap::new();
    for _ in 0..3 {
        lazy.entry(1).or_insert_with(|| {
            built += 1;
            10
        });
    }
    println!("or_insert_with ran {} time(s)", built);
    let mut calls = 0;
    let mut make = || {
        calls += 1;
        10u32
    };
    let mut eager: BTreeMap<u32, u32> = BTreeMap::new();
    for _ in 0..3 {
        eager.entry(1).or_insert(make());
    }
    println!("or_insert(make()) ran {} time(s)", calls);
}
```
Expected output: `slot 7: [1, 2] counts: {"a": 2, "b": 3, "c": 1} hp: {"orc": 95} or_insert_with ran 1 time(s) or_insert(make()) ran 3 time(s)`

