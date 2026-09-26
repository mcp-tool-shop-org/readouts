# Ownership, moves & borrowing — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](ownership-borrowing.md) · [catalog index](README.md)

## Keep one &mut xor any number of & live at once, and end each borrow at its last use (E0499, E0502, E0506)
**A value may have one live mutable reference or any number of live shared ones; since Rust 1.63 NLL is the borrow checker on every edition and a borrow lasts only until its last use, so most conflicts are fixed by reordering rather than by blocks, clones or RefCell.**

*Check 1: Holding &v[0] across v.push(..) and using it afterwards is E0502* · `compile_fail` · edition 2024 · host · bin · errors: E0502 · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![1.0_f64, 2.0];
    let first = &v[0];
    v.push(3.0);
    println!("{first}");
}
```

*Check 2: The same code with the last use above the push compiles (NLL)* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![1.0_f64, 2.0];
    let first = &v[0];
    println!("{first}");
    v.push(3.0);
    println!("{}", v.len());
}
```
Expected output: `1 3`

*Check 3: Two live &mut to one Vec is E0499* · `compile_fail` · edition 2024 · host · bin · errors: E0499 · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![1.0_f64];
    let a = &mut v;
    let b = &mut v;
    a.push(2.0);
    b.push(3.0);
}
```

*Check 4: Assigning to a variable while a reference to it is live is E0506* · `compile_fail` · edition 2024 · host · bin · errors: E0506 · **✔ oracle pass**
```rust
fn main() {
    let mut x = 1.0_f64;
    let r = &x;
    x = 2.0;
    println!("{r} {x}");
}
```

*Check 5: Reading a variable while a &mut to it is live is E0503, not E0499* · `compile_fail` · edition 2024 · host · bin · errors: E0503 · **✔ oracle pass**
```rust
fn main() {
    let mut x = 1.0_f64;
    let r = &mut x;
    let y = x + 1.0;
    *r += y;
}
```

*Check 6: Pushing to a Vec inside `for x in &v` is E0502* · `compile_fail` · edition 2024 · host · bin · errors: E0502 · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![1, 2, 3];
    for x in &v {
        if *x == 2 {
            v.push(4);
        }
    }
}
```

*Check 7: Collect first, apply after the loop* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let extra: Vec<i32> = v.iter().filter(|x| **x == 2).map(|_| 4).collect();
    v.extend(extra);
    println!("{:?}", v);
}
```
Expected output: `[1, 2, 3, 4]`

*Check 8: NLL problem case #3 (return a borrow on one path, mutate on the other) is E0502 on 1.98.1* · `compile_fail` · edition 2024 · host · lib · errors: E0502 · **✔ oracle pass**
```rust
pub fn last_or_push<'a>(vec: &'a mut Vec<String>) -> &'a String {
    if let Some(s) = vec.last() {
        return s;
    }
    vec.push(String::new());
    vec.last().unwrap()
}
```

*Check 9: The Polonius post's get_mut_or_default is E0499 on stable 1.98.1* · `compile_fail` · edition 2024 · host · lib · errors: E0499 · **✔ oracle pass**
```rust
use std::collections::HashMap;
use std::hash::Hash;

pub fn get_mut_or_default<'r, K: Hash + Eq + Copy, V: Default>(
    map: &'r mut HashMap<K, V>,
    key: K,
) -> &'r mut V {
    match map.get_mut(&key) {
        Some(value) => value,
        None => {
            map.insert(key, V::default());
            map.get_mut(&key).unwrap()
        }
    }
}
```

*Check 10: Shapes 1.98.1 accepts: test without holding the borrow; the entry API for maps* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::collections::HashMap;

fn last_or_push(vec: &mut Vec<String>) -> &String {
    if vec.is_empty() {
        vec.push(String::new());
    }
    vec.last().unwrap()
}

fn get_mut_or_default(map: &mut HashMap<u32, f64>, key: u32) -> &mut f64 {
    map.entry(key).or_default()
}

fn main() {
    let mut v = vec![String::from("x")];
    let mut m = HashMap::new();
    *get_mut_or_default(&mut m, 7) += 1.5;
    *get_mut_or_default(&mut m, 7) += 1.5;
    println!("{} {}", last_or_push(&mut v), m[&7]);
}
```
Expected output: `x 3`

## Keep the owner alive past its last borrow: fix E0597, E0716 and E0515 by binding it or returning owned data
**A reference must not outlive what it points to: a named local dropped at the end of its block gives E0597, a temporary dropped at the end of its statement gives E0716, and returning a reference to a local gives E0515; the fix is to bind the owner in the outer scope or to return owned data.**

*Check 1: A reference to a block-local used after the block is E0597* · `compile_fail` · edition 2024 · host · bin · errors: E0597 · **✔ oracle pass**
```rust
fn main() {
    let r;
    {
        let x = 5.0_f64;
        r = &x;
    }
    println!("{r}");
}
```

*Check 2: A struct holding &data that outlives data is E0597* · `compile_fail` · edition 2024 · host · bin · errors: E0597 · **✔ oracle pass**
```rust
struct View<'a> {
    xs: &'a [f64],
}

fn main() {
    let view;
    {
        let data = vec![1.0, 2.0];
        view = View { xs: &data };
    }
    println!("{}", view.xs.len());
}
```

*Check 3: A method call on a temporary kept in a let (String::from(..).as_str()) is E0716* · `compile_fail` · edition 2024 · host · bin · errors: E0716 · stderr has “temporary value dropped while borrowed” · **✔ oracle pass**
```rust
fn main() {
    let s = String::from("hello").as_str();
    println!("{s}");
}
```

*Check 4: A temporary passed as a function argument is not extended: identity(&temp()) is E0716* · `compile_fail` · edition 2024 · host · bin · errors: E0716 · **✔ oracle pass**
```rust
fn temp() -> Vec<f64> {
    vec![1.0]
}

fn main() {
    let x = core::convert::identity(&temp());
    println!("{:?}", x);
}
```

*Check 5: Extended temporaries and a bound owner compile: `&String::from(..)`, `Some(&temp())`* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn temp() -> Vec<f64> {
    vec![1.0]
}

fn main() {
    let s = &String::from("hello"); // operand of a borrow in the initializer: extended
    let x = Some(&temp()); // tuple-variant constructor argument: extended
    let owner = String::from("world");
    let t = owner.as_str(); // owner bound first
    println!("{s} {:?} {t}", x);
}
```
Expected output: `hello Some([1.0]) world`

*Check 6: Returning a reference to a local Vec is E0515* · `compile_fail` · edition 2024 · host · lib · errors: E0515 · **✔ oracle pass**
```rust
pub fn make() -> &'static [f64] {
    let v = vec![1.0, 2.0];
    &v
}
```

*Check 7: Returning the owned Vec is the fix* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn make() -> Vec<f64> {
    let v = vec![1.0, 2.0];
    v
}

fn main() {
    println!("{:?}", make());
}
```
Expected output: `[1.0, 2.0]`

*Check 8: Edition 2021: a RefCell guard in a block's tail expression is E0597* · `compile_fail` · edition 2021 · host · bin · errors: E0597 · **✔ oracle pass**
```rust
use std::cell::RefCell;

fn len() -> usize {
    let c = RefCell::new(vec![1.0_f64, 2.0]);
    c.borrow().len()
}

fn main() {
    println!("{}", len());
}
```

*Check 9: Edition 2024 drops tail temporaries first and accepts the same function* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::cell::RefCell;

fn len() -> usize {
    let c = RefCell::new(vec![1.0_f64, 2.0]);
    c.borrow().len()
}

fn main() {
    println!("{}", len());
}
```
Expected output: `2`

*Check 10: Edition 2021 fix: bind the result to a local, then return it* · `runs` · edition 2021 · host · no warnings · **✔ oracle pass**
```rust
use std::cell::RefCell;

fn len() -> usize {
    let c = RefCell::new(vec![1.0_f64, 2.0]);
    let n = c.borrow().len();
    n
}

fn main() {
    println!("{}", len());
}
```
Expected output: `2`

## Move a value out from behind &mut with mem::take, mem::replace or mem::swap instead of fighting E0507
**A non-Copy value cannot be moved out of a place behind `&mut` or out of an index (E0507), because the place would be left empty; `std::mem::take`, `std::mem::replace`, `std::mem::swap` and `Option::take`/`replace` move it out while leaving a valid value behind.**

*Check 1: Moving a Vec field out of &mut self is E0507* · `compile_fail` · edition 2024 · host · lib · errors: E0507 · stderr has “which is behind a mutable reference” · **✔ oracle pass**
```rust
pub struct Log {
    lines: Vec<String>,
}

impl Log {
    pub fn drain_all(&mut self) -> Vec<String> {
        let out = self.lines;
        self.lines = Vec::new();
        out
    }
}
```

*Check 2: Moving a String out of a Vec by index is E0507* · `compile_fail` · edition 2024 · host · bin · errors: E0507 · stderr has “cannot move out of index of `Vec<String>`” · **✔ oracle pass**
```rust
fn main() {
    let v = vec![String::from("a")];
    let s = v[0];
    println!("{s}");
}
```

*Check 3: The field()-style accessor over a non-Copy payload is E0507* · `compile_fail` · edition 2024 · host · bin · errors: E0507 · **✔ oracle pass**
```rust
fn slot(xs: &mut [String], k: usize) -> &mut String {
    &mut xs[k]
}

fn main() {
    let mut xs = [String::from("a"), String::from("b")];
    let a = *slot(&mut xs, 0);
    println!("{a}");
}
```

*Check 4: mem::take, mem::replace, mem::swap and Option::take/replace move values out safely* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::mem;

#[derive(Debug)]
enum Phase {
    Running(u32),
    Done,
}

struct Log {
    lines: Vec<String>,
    phase: Phase,
    pending: Option<u32>,
}

impl Log {
    fn drain_all(&mut self) -> Vec<String> {
        mem::take(&mut self.lines) // leaves Vec::default()
    }
    fn finish(&mut self) -> Phase {
        mem::replace(&mut self.phase, Phase::Done) // leaves the value passed in
    }
}

fn main() {
    let mut log = Log { lines: vec!["a".into(), "b".into()], phase: Phase::Running(7), pending: Some(5) };
    let got = log.drain_all();
    let old = log.finish();
    let step = if let Phase::Running(n) = old { n } else { 0 };
    let taken = log.pending.take(); // leaves None
    let prev = log.pending.replace(9); // leaves Some(9)
    let mut a = vec![1];
    let mut b = vec![2, 3];
    mem::swap(&mut a, &mut b);
    let mut names = vec![String::from("x"), String::from("y")];
    let first = mem::take(&mut names[0]);
    println!("{:?} {} {} {:?} {:?} {:?} {:?} {:?} {:?} {:?}", got, log.lines.len(), step, log.phase, taken, prev, log.pending, a, b, (first, names));
}
```
Expected output: `["a", "b"] 0 7 Done Some(5) None Some(9) [2, 3] [1] ("x", ["", "y"])`

## Name lifetimes only where the three elision rules fail: two reference inputs, none, or a struct field (E0106)
**Elision gives each elided input its own lifetime, assigns a sole input lifetime to every elided output, and with `&self`/`&mut self` assigns self's lifetime; a returned reference with two candidate inputs and no self, with no reference input, or any reference stored in a struct or enum needs a named lifetime (E0106).**

*Check 1: One reference input: the output borrows from it (rule 2), as in the solver's field()* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub fn first_word(s: &str) -> &str {
    s.split(' ').next().unwrap_or("")
}

pub fn field(bodies: &mut [f64], i: usize, slot: usize) -> &mut f64 {
    &mut bodies[i * 17 + slot]
}
```

*Check 2: Two reference inputs and no self: returning &str is E0106* · `compile_fail` · edition 2024 · host · lib · errors: E0106 · stderr has “missing lifetime specifier” · **✔ oracle pass**
```rust
pub fn longest(x: &str, y: &str) -> &str {
    if x.len() > y.len() { x } else { y }
}
```

*Check 3: Naming one lifetime for both inputs and the output fixes it* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

*Check 4: No reference input: `fn get_str() -> &str` is E0106* · `compile_fail` · edition 2024 · host · lib · errors: E0106 · **✔ oracle pass**
```rust
pub fn get_str() -> &str {
    "x"
}
```

*Check 5: &self rule: returning the other argument fails with 'lifetime may not live long enough'* · `compile_fail` · edition 2024 · host · lib · stderr has “lifetime may not live long enough” · **✔ oracle pass**
```rust
pub struct Table {
    names: Vec<String>,
}

impl Table {
    pub fn pick(&self, fallback: &str) -> &str {
        if self.names.is_empty() { fallback } else { &self.names[0] }
    }
}
```

*Check 6: Naming 'a on self and the argument fixes the method* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub struct Table {
    names: Vec<String>,
}

impl Table {
    pub fn pick<'a>(&'a self, fallback: &'a str) -> &'a str {
        if self.names.is_empty() { fallback } else { &self.names[0] }
    }
}
```

*Check 7: A struct field holding &[f64] without a lifetime parameter is E0106* · `compile_fail` · edition 2024 · host · lib · errors: E0106 · **✔ oracle pass**
```rust
pub struct View {
    pub xs: &[f64],
}
```

*Check 8: `&'a mut self` on Cursor<'a> keeps it borrowed: the second call is E0499* · `compile_fail` · edition 2024 · host · bin · errors: E0499 · **✔ oracle pass**
```rust
struct Cursor<'a> {
    xs: &'a [f64],
    at: usize,
}

impl<'a> Cursor<'a> {
    fn next(&'a mut self) -> &'a f64 {
        self.at += 1;
        &self.xs[self.at - 1]
    }
}

fn main() {
    let data = [1.0, 2.0];
    let mut c = Cursor { xs: &data, at: 0 };
    let a = c.next();
    let b = c.next();
    println!("{a} {b}");
}
```

*Check 9: `&mut self` returning `&'a f64` lets the cursor be called repeatedly* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
struct Cursor<'a> {
    xs: &'a [f64],
    at: usize,
}

impl<'a> Cursor<'a> {
    fn next(&mut self) -> &'a f64 {
        self.at += 1;
        &self.xs[self.at - 1]
    }
}

fn main() {
    let data = [1.0, 2.0];
    let mut c = Cursor { xs: &data, at: 0 };
    let a = c.next();
    let b = c.next();
    println!("{a} {b}");
}
```
Expected output: `1 2`

*Check 10: A lifetime hidden in `-> std::slice::Iter<f64>` warns mismatched_lifetime_syntaxes* · `compiles` · edition 2024 · host · lib · lints: mismatched_lifetime_syntaxes · stderr has “hiding a lifetime that's elided elsewhere is confusing” · **✔ oracle pass**
```rust
pub struct Track {
    xs: Vec<f64>,
}

impl Track {
    pub fn iter(&self) -> std::slice::Iter<f64> {
        self.xs.iter()
    }
}
```

*Check 11: `-> std::slice::Iter<'_, f64>` compiles with no warning* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
pub struct Track {
    xs: Vec<f64>,
}

impl Track {
    pub fn iter(&self) -> std::slice::Iter<'_, f64> {
        self.xs.iter()
    }
}
```

## Pass a held &mut to generic parameters as &mut *r: concrete &mut parameters reborrow, generic T moves (E0382)
**A held `r: &mut T` passed where the parameter's type is known to be `&mut T` is implicitly reborrowed (`&mut *r`) and stays usable; passed to a generic `T` or `impl Trait` parameter, the reference itself is moved and the next use is E0382.**

*Check 1: A &mut passed to a concrete &mut parameter is reborrowed; an annotated let reborrows too* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn bump(x: &mut f64) {
    *x += 1.0;
}

fn main() {
    let mut n = 0.0_f64;
    let r = &mut n;
    bump(r); // implicit reborrow: &mut *r
    bump(r); // r is still usable
    let r2: &mut f64 = r; // let with an explicit type: reborrow, not move
    *r2 += 1.0;
    *r += 1.0; // allowed after r2's last use
    println!("{n}");
}
```
Expected output: `4`

*Check 2: Passing the same &mut to a generic T twice is E0382; rustc suggests a fresh reborrow* · `compile_fail` · edition 2024 · host · bin · errors: E0382 · stderr has “consider creating a fresh reborrow of `r` here” · **✔ oracle pass**
```rust
fn consume<T>(_t: T) {}

fn main() {
    let mut n = 0.0_f64;
    let r = &mut n;
    consume(r); // T = &mut f64: the reference itself is moved
    consume(r);
}
```

*Check 3: &mut *r, or a turbofish naming &mut f64, keeps r usable across generic calls* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn consume<T>(_t: T) {}

fn main() {
    let mut n = 0.0_f64;
    let r = &mut n;
    consume(&mut *r);
    consume(&mut *r);
    consume::<&mut f64>(r);
    consume::<&mut f64>(r);
    *r += 1.0;
    println!("{n}");
}
```
Expected output: `1`

*Check 4: `let r2 = r;` without a type moves the &mut: using r afterwards is E0382* · `compile_fail` · edition 2024 · host · bin · errors: E0382 · **✔ oracle pass**
```rust
fn main() {
    let mut n = 0.0_f64;
    let r = &mut n;
    let r2 = r;
    *r2 += 1.0;
    *r += 1.0;
}
```

*Check 5: While a reborrow is live the original is frozen: borrowing it again is E0499* · `compile_fail` · edition 2024 · host · bin · errors: E0499 · **✔ oracle pass**
```rust
fn bump(x: &mut f64) {
    *x += 1.0;
}

fn main() {
    let mut n = 0.0_f64;
    let r = &mut n;
    let r2: &mut f64 = r;
    bump(r);
    *r2 += 1.0;
}
```

*Check 6: step()'s shape: one &mut [f64; N] passed twice to a &mut [f64] parameter stays usable* · `runs` · edition 2021 · host · no warnings · **✔ oracle pass**
```rust
fn sum(xs: &mut [f64]) -> f64 {
    xs[0] += 1.0;
    xs.iter().sum()
}

fn main() {
    let mut buf = [0.0_f64; 4 * 17];
    let bodies = &mut buf; // &mut [f64; 68], as step() holds &mut BODIES
    let a = sum(bodies); // reborrow + unsize coercion to &mut [f64]
    let b = sum(bodies); // bodies is still usable
    println!("{a} {b}");
}
```
Expected output: `1 2`

*Check 7: A generic AsMut<[f64]> helper would move step()'s &mut buffer: the second call is E0382* · `compile_fail` · edition 2021 · host · bin · errors: E0382 · stderr has “consider creating a fresh reborrow of `bodies` here” · **✔ oracle pass**
```rust
fn sum<B: AsMut<[f64]>>(mut xs: B) -> f64 {
    xs.as_mut().iter().sum()
}

fn main() {
    let mut buf = [0.0_f64; 4 * 17];
    let bodies = &mut buf;
    let a = sum(bodies);
    let b = sum(bodies);
    println!("{a} {b}");
}
```

*Check 8: Handle::from(r) with impl From<&mut Body> moves r: the next use is E0382 (#108532)* · `compile_fail` · edition 2024 · host · bin · errors: E0382 · **✔ oracle pass**
```rust
struct Body {
    x: f64,
}

struct Handle;

impl From<&mut Body> for Handle {
    fn from(_: &mut Body) -> Self {
        Handle
    }
}

fn main() {
    let r = &mut Body { x: 1.0 };
    let _h = Handle::from(r); // generic From::from: r is moved, not reborrowed
    r.x = 2.0;
}
```

## Take &[T], &mut [T] and &str parameters instead of &Vec<T>, &String or &[T; N]
**A slice parameter accepts a Vec, an array, any sub-range and a String through deref and unsize coercions; a `&Vec<T>` or `&String` parameter rejects arrays and sub-slices (E0308) and gains nothing unless the callee must grow the collection.**

*Check 1: Slice parameters accept a Vec, an array, a sub-range, a String and a literal* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn sum(xs: &[f64]) -> f64 {
    xs.iter().sum()
}

fn zero(xs: &mut [f64]) {
    for x in xs.iter_mut() {
        *x = 0.0;
    }
}

fn name_len(s: &str) -> usize {
    s.len()
}

fn main() {
    let v = vec![1.0, 2.0, 3.0];
    let a = [4.0, 5.0];
    let mut buf = [1.0_f64; 4];
    zero(&mut buf[1..3]);
    let owned = String::from("abc");
    println!("{} {} {} {:?} {} {}", sum(&v), sum(&a), sum(&v[1..]), buf, name_len(&owned), name_len("de"));
}
```
Expected output: `6 9 5 [1.0, 0.0, 0.0, 1.0] 3 2`

*Check 2: A &Vec<f64> parameter rejects an array argument (E0308)* · `compile_fail` · edition 2024 · host · bin · errors: E0308 · **✔ oracle pass**
```rust
fn sum(xs: &Vec<f64>) -> f64 {
    xs.iter().sum()
}

fn main() {
    let a = [4.0, 5.0];
    println!("{}", sum(&a));
}
```

*Check 3: A slice cannot grow: push on &mut [f64] is E0599* · `compile_fail` · edition 2024 · host · lib · errors: E0599 · **✔ oracle pass**
```rust
pub fn add(xs: &mut [f64]) {
    xs.push(1.0);
}
```

## Treat every by-value use as a move: derive Copy only for plain data, clone on purpose (E0382, E0505, E0204)
**Assigning, passing or returning a non-Copy value moves it and kills the source (E0382 on reuse, E0505 if a borrow of it is still live); Copy types are bit-copied implicitly; Clone is an explicit and possibly expensive call.**

*Check 1: Using a String after `let s2 = s1;` is E0382 (borrow of moved value)* · `compile_fail` · edition 2024 · host · bin · errors: E0382 · stderr has “borrow of moved value: `s1`” · **✔ oracle pass**
```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;
    println!("{s1}, {s2}");
}
```

*Check 2: Moving a Vec inside a loop is E0382 with the 'previous iteration of loop' label* · `compile_fail` · edition 2024 · host · bin · errors: E0382 · stderr has “value moved here, in previous iteration of loop” · **✔ oracle pass**
```rust
fn consume(_v: Vec<f64>) {}

fn main() {
    let v = vec![1.0];
    for _ in 0..2 {
        consume(v);
    }
}
```

*Check 3: derive(Clone, Copy) on a struct with a Vec field is E0204* · `compile_fail` · edition 2024 · host · lib · errors: E0204 · **✔ oracle pass**
```rust
#[derive(Clone, Copy)]
pub struct PointList {
    pub points: Vec<f64>,
}
```

*Check 4: Moving a Vec while a reference into it is still used is E0505* · `compile_fail` · edition 2024 · host · bin · errors: E0505 · **✔ oracle pass**
```rust
fn eat(_v: Vec<f64>) {}

fn main() {
    let v = vec![1.0, 2.0];
    let first = &v[0];
    eat(v);
    println!("{first}");
}
```

*Check 5: Finishing with the reference before the move fixes E0505 (NLL)* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn eat(v: Vec<f64>) -> usize {
    v.len()
}

fn main() {
    let v = vec![1.0, 2.0];
    let first = &v[0];
    println!("{first}");
    println!("{}", eat(v));
}
```
Expected output: `1 2`

*Check 6: A Copy struct of f64 arrays is duplicated by `let b = a;`; a String needs .clone()* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
#[derive(Clone, Copy)]
struct Pose {
    p: [f64; 3],
    v: [f64; 3],
}

fn main() {
    let a = Pose { p: [1.0, 2.0, 3.0], v: [0.5; 3] };
    let mut b = a; // bitwise copy: `a` stays usable
    b.p[0] = 9.0;
    let s = String::from("id");
    let t = s.clone(); // explicit deep copy
    println!("{} {} {} {} {}", a.p[0], b.p[0], a.v[2], s, t);
}
```
Expected output: `1 9 0.5 id id`

*Check 7: rapier3d-f64 0.35.3 KinematicCharacterController is Copy, so integrate() may copy it out of &mut* · `runs` · edition 2021 · host · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::control::KinematicCharacterController;

struct Loaded {
    controller: KinematicCharacterController,
    halves: Vec<f64>,
}

fn is_copy<T: Copy>(_: &T) -> bool {
    true
}

// integrate() in rapier_law.rs copies the controller out of &mut Loaded, then keeps
// mutating `loaded`. That line compiles only because the type is Copy.
fn integrate(loaded: &mut Loaded) -> (bool, bool, usize) {
    let controller = loaded.controller;
    loaded.halves.push(0.5);
    (is_copy(&controller), controller.slide, loaded.halves.len())
}

fn main() {
    let mut l = Loaded { controller: KinematicCharacterController::default(), halves: Vec::new() };
    println!("{:?}", integrate(&mut l));
}
```
Expected output: `(true, true, 1)`

## Borrow struct fields directly, not through &mut self getters; edition-2021 closures capture only used fields
**Distinct field paths are distinct places, so `&mut w.pos` and `&w.vel` coexist; a `&mut self` getter borrows all of `self`, so two getters held together are E0499; since edition 2021 a closure captures only the field paths it uses.**

*Check 1: Direct field borrows and a parts() method returning both borrows compile* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
struct World {
    pos: Vec<f64>,
    vel: Vec<f64>,
}

impl World {
    fn parts(&mut self) -> (&mut [f64], &[f64]) {
        (&mut self.pos, &self.vel)
    }
}

fn main() {
    let mut w = World { pos: vec![0.0], vel: vec![1.0] };
    let p = &mut w.pos;
    let v = &w.vel;
    p[0] += v[0];
    let (p2, v2) = w.parts();
    p2[0] += v2[0];
    println!("{:?}", w.pos);
}
```
Expected output: `[2.0]`

*Check 2: Two &mut self getters held at once are E0499: a method borrows all of self* · `compile_fail` · edition 2024 · host · bin · errors: E0499 · **✔ oracle pass**
```rust
struct World {
    pos: Vec<f64>,
    vel: Vec<f64>,
}

impl World {
    fn pos_mut(&mut self) -> &mut Vec<f64> {
        &mut self.pos
    }
    fn vel_mut(&mut self) -> &mut Vec<f64> {
        &mut self.vel
    }
}

fn main() {
    let mut w = World { pos: vec![0.0], vel: vec![1.0] };
    let p = w.pos_mut();
    let v = w.vel_mut();
    p[0] += v[0];
}
```

*Check 3: Edition 2018: a closure using s.log captures all of s, so &s.count is E0502* · `compile_fail` · edition 2018 · host · bin · errors: E0502 · **✔ oracle pass**
```rust
struct S {
    log: Vec<i32>,
    count: i32,
}

fn main() {
    let mut s = S { log: vec![], count: 0 };
    let mut record = |x: i32| s.log.push(x);
    let c = &s.count;
    record(*c);
    println!("{:?}", s.log);
}
```

*Check 4: Edition 2021: the same closure captures only s.log and the code compiles* · `runs` · edition 2021 · host · no warnings · **✔ oracle pass**
```rust
struct S {
    log: Vec<i32>,
    count: i32,
}

fn main() {
    let mut s = S { log: vec![], count: 0 };
    let mut record = |x: i32| s.log.push(x);
    let c = &s.count;
    record(*c);
    println!("{:?}", s.log);
}
```
Expected output: `[0]`

*Check 5: Indexing in a closure captures the whole Vec field: &s.rows[1] is E0502 (edition 2021)* · `compile_fail` · edition 2021 · host · bin · errors: E0502 · **✔ oracle pass**
```rust
struct S {
    rows: Vec<f64>,
    other: f64,
}

fn main() {
    let mut s = S { rows: vec![1.0, 2.0], other: 5.0 };
    let mut bump = || s.rows[0] += 1.0;
    let o = &s.other; // a different field: fine
    let r1 = &s.rows[1]; // same field the closure captured: E0502
    bump();
    println!("{o} {r1}");
}
```

*Check 6: integrate()'s shape: destructure &mut PhysicsWorld into four field borrows for one call* · `runs` · edition 2021 · host · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

// integrate() in rapier_law.rs lends four disjoint fields of one &mut PhysicsWorld
// to a single call.
fn query_once(world: &mut PhysicsWorld) -> usize {
    let PhysicsWorld { broad_phase, narrow_phase, bodies, colliders, .. } = world;
    let _query = broad_phase.as_query_pipeline_mut(
        narrow_phase.query_dispatcher(),
        bodies,
        colliders,
        QueryFilter::new(),
    );
    world.bodies.len()
}

fn main() {
    let mut world = PhysicsWorld::new();
    println!("{}", query_once(&mut world));
}
```
Expected output: `0`

## Know where two-phase borrows apply: v.push(v.len()) compiles, Vec::push(&mut v, v.len()) is E0502
**rustc makes only three implicit mutable borrows two-phase - the autoref of a `&mut self` method call, a mutable reborrow in function arguments, and overloaded compound assignment - and such a borrow acts as a shared borrow until the call activates it; an `&mut` written in source never gets this.**

*Check 1: v.push(v.len()) and Vec::push(r, r.len()) compile (edition 2024)* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn main() {
    let mut v: Vec<usize> = vec![10, 20];
    v.push(v.len());
    let mut w: Vec<usize> = vec![7];
    let r = &mut w;
    Vec::push(r, r.len());
    println!("{:?} {:?}", v, w);
}
```
Expected output: `[10, 20, 2] [7, 1]`

*Check 2: The same two-phase shapes compile under edition 2015* · `runs` · edition 2015 · host · no warnings · **✔ oracle pass**
```rust
fn main() {
    let mut v: Vec<usize> = vec![10, 20];
    v.push(v.len());
    let mut w: Vec<usize> = vec![7];
    let r = &mut w;
    Vec::push(r, r.len());
    println!("{:?} {:?}", v, w);
}
```
Expected output: `[10, 20, 2] [7, 1]`

*Check 3: Vec::push(&mut v, v.len()) is E0502: an explicit &mut is never two-phase* · `compile_fail` · edition 2024 · host · bin · errors: E0502 · **✔ oracle pass**
```rust
fn main() {
    let mut v: Vec<usize> = vec![10, 20];
    Vec::push(&mut v, v.len());
    println!("{:?}", v);
}
```

*Check 4: Mutating in the arguments still conflicts: v.push(v.pop().unwrap()) is E0499* · `compile_fail` · edition 2024 · host · bin · errors: E0499 · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![1, 2];
    v.push(v.pop().unwrap());
    println!("{:?}", v);
}
```

*Check 5: Indexing activates the borrow: v[0].push_str(&format!("{}", v.len())) is E0502* · `compile_fail` · edition 2024 · host · bin · errors: E0502 · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![String::from("a")];
    v[0].push_str(&format!("{}", v.len()));
    println!("{:?}", v);
}
```

*Check 6: Hoisting the argument into a local fixes each case* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn main() {
    let mut v = vec![String::from("a")];
    let n = v.len();
    v[0].push_str(&n.to_string());
    let mut w = vec![1, 2];
    let last = w.pop().unwrap();
    w.push(last);
    println!("{:?} {:?}", v, w);
}
```
Expected output: `["a1"] [1, 2]`

## Split one flat buffer into disjoint &mut with split_at_mut, as_chunks_mut and get_disjoint_mut (1.86+)
**The borrow checker treats every index of a slice or array as the same place, so `&mut v[i]` and `&mut v[j]` together are E0499 even when i != j; `split_at_mut`, `split_first_mut`, `as_chunks_mut`, `chunks_exact_mut` and `get_disjoint_mut` hand out non-overlapping `&mut` safely.**

*Check 1: `&mut v[0]` and `&mut v[2]` together are E0499; rustc points to split_at_mut* · `compile_fail` · edition 2024 · host · bin · errors: E0499 · stderr has “use `.split_at_mut(position)` to obtain two mutable non-overlapping sub-slices” · **✔ oracle pass**
```rust
fn main() {
    let mut v = [1.0_f64, 2.0, 3.0];
    let a = &mut v[0];
    let b = &mut v[2];
    *a += *b;
}
```

*Check 2: split_at_mut hands out two non-overlapping &mut halves* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn main() {
    let mut v = [1.0_f64, 2.0, 3.0];
    let (lo, hi) = v.split_at_mut(2);
    let a = &mut lo[0];
    let b = &mut hi[0];
    *a += *b;
    *b = 0.0;
    println!("{:?}", v);
}
```
Expected output: `[4.0, 2.0, 0.0]`

*Check 3: get_disjoint_mut (1.86+): Ok for distinct indices, Err for equal or out-of-range ones* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
use std::slice::GetDisjointMutError;

fn main() {
    let mut v = [1.0_f64, 2.0, 3.0];
    if let Ok([a, b]) = v.get_disjoint_mut([0, 2]) {
        std::mem::swap(a, b);
    }
    let same = v.get_disjoint_mut([1, 1]).map(|_| ());
    let oob = v.get_disjoint_mut([0, 9]).map(|_| ());
    println!("{:?} {} {}", v, same == Err(GetDisjointMutError::OverlappingIndices), oob == Err(GetDisjointMutError::IndexOutOfBounds));
}
```
Expected output: `[3.0, 2.0, 1.0] true true`

*Check 4: resolve_pair's shape: copy both bodies out through field(), then write (edition 2021)* · `runs` · edition 2021 · host · no warnings · **✔ oracle pass**
```rust
const BODY_STRIDE: usize = 17;

fn body_at(i: usize) -> usize {
    i * BODY_STRIDE
}

fn field(bodies: &mut [f64], i: usize, slot: usize) -> &mut f64 {
    &mut bodies[body_at(i) + slot]
}

// Copy both bodies out, then write: no two &mut into the buffer coexist.
fn separate_x(bodies: &mut [f64], i: usize, j: usize) {
    let ax = *field(bodies, i, 0);
    let bx = *field(bodies, j, 0);
    let half = (ax + 1.0 - bx) / 2.0;
    *field(bodies, i, 0) = ax - half;
    *field(bodies, j, 0) = bx + half;
}

fn main() {
    let mut buf = [0.0_f64; 2 * BODY_STRIDE];
    buf[body_at(1)] = 0.5;
    separate_x(&mut buf, 0, 1);
    println!("{} {}", buf[body_at(0)], buf[body_at(1)]);
}
```
Expected output: `-0.25 0.75`

*Check 5: Holding two field() results at once is E0499 (edition 2021)* · `compile_fail` · edition 2021 · host · lib · errors: E0499 · **✔ oracle pass**
```rust
const BODY_STRIDE: usize = 17;

fn field(bodies: &mut [f64], i: usize, slot: usize) -> &mut f64 {
    &mut bodies[i * BODY_STRIDE + slot]
}

pub fn separate_x(bodies: &mut [f64], i: usize, j: usize) {
    let a = field(bodies, i, 0);
    let b = field(bodies, j, 0);
    let half = (*a + 1.0 - *b) / 2.0;
    *a -= half;
    *b += half;
}
```

*Check 6: as_chunks_mut::<17>() then get_disjoint_mut([i, j]) gives two &mut body rows (edition 2021)* · `runs` · edition 2021 · host · no warnings · **✔ oracle pass**
```rust
const BODY_STRIDE: usize = 17;

fn separate_x(bodies: &mut [f64], i: usize, j: usize) -> bool {
    let (rows, _rest) = bodies.as_chunks_mut::<BODY_STRIDE>();
    match rows.get_disjoint_mut([i, j]) {
        Ok([a, b]) => {
            let half = (a[0] + 1.0 - b[0]) / 2.0;
            a[0] -= half;
            b[0] += half;
            true
        }
        Err(_) => false,
    }
}

fn main() {
    let mut buf = [0.0_f64; 2 * BODY_STRIDE];
    buf[BODY_STRIDE] = 0.5;
    let ok = separate_x(&mut buf, 0, 1);
    let same = separate_x(&mut buf, 1, 1);
    println!("{} {} {} {}", buf[0], buf[BODY_STRIDE], ok, same);
}
```
Expected output: `-0.25 0.75 true false`

*Check 7: split_at_mut(j * STRIDE) with i < j gives the same two rows (edition 2021)* · `runs` · edition 2021 · host · no warnings · **✔ oracle pass**
```rust
const BODY_STRIDE: usize = 17;

fn separate_x(bodies: &mut [f64], i: usize, j: usize) {
    assert!(i < j);
    let (lo, hi) = bodies.split_at_mut(j * BODY_STRIDE);
    let a = &mut lo[i * BODY_STRIDE..(i + 1) * BODY_STRIDE];
    let b = &mut hi[..BODY_STRIDE];
    let half = (a[0] + 1.0 - b[0]) / 2.0;
    a[0] -= half;
    b[0] += half;
}

fn main() {
    let mut buf = [0.0_f64; 2 * BODY_STRIDE];
    buf[BODY_STRIDE] = 0.5;
    separate_x(&mut buf, 0, 1);
    println!("{} {}", buf[0], buf[BODY_STRIDE]);
}
```
Expected output: `-0.25 0.75`

*Check 8: An array field's elements borrow as a whole (E0502) while tuple fields split* · `compile_fail` · edition 2024 · host · bin · errors: E0502 · **✔ oracle pass**
```rust
struct Pair {
    a: [f64; 2],
    t: (f64, f64),
}

fn add(x: &mut f64, y: &f64) {
    *x += *y;
}

fn main() {
    let mut p = Pair { a: [1.0, 2.0], t: (1.0, 2.0) };
    add(&mut p.t.0, &p.t.1); // tuple fields: disjoint
    add(&mut p.a[0], &p.a[1]); // array elements: E0502
    println!("{:?} {:?}", p.a, p.t);
}
```

*Check 9: split_first_mut splits the array so both elements can be lent* · `runs` · edition 2024 · host · no warnings · **✔ oracle pass**
```rust
fn add(x: &mut f64, y: &f64) {
    *x += *y;
}

fn main() {
    let mut a = [1.0_f64, 2.0];
    let (first, rest) = a.split_first_mut().unwrap();
    add(first, &rest[0]);
    println!("{:?}", a);
}
```
Expected output: `[3.0, 2.0]`

