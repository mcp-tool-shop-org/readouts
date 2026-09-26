# Concurrency, parallelism & async — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](concurrency-async.md) · [catalog index](README.md)

## Borrow stack data in worker threads with thread::scope (1.63); thread::spawn needs move and 'static
**std::thread::spawn requires F: FnOnce() -> T + Send + 'static, so a closure borrowing a local is E0373, while std::thread::scope (stable 1.63.0) joins every scoped thread before returning, so workers can borrow slices and write disjoint chunks without Arc.**

*Check 1: thread::spawn borrowing a local vector is E0373 (closure may outlive the function)* · `compile_fail` · edition 2024 · host · bin · errors: E0373 · **✔ oracle pass**
```rust
fn main() {
    let v = vec![1.0f64, 2.0, 3.0];
    let h = std::thread::spawn(|| v.iter().sum::<f64>());
    println!("{}", h.join().unwrap());
}
```

*Check 2: thread::scope workers read shared chunks and write disjoint &mut chunks, no Arc* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let input: Vec<f64> = (0..16).map(|i| i as f64).collect();
    let mut out = vec![0.0f64; 16];
    std::thread::scope(|s| {
        for (src, dst) in input.chunks(4).zip(out.chunks_mut(4)) {
            s.spawn(move || {
                for (x, y) in src.iter().zip(dst.iter_mut()) {
                    *y = x * 0.5;
                }
            });
        }
    });
    println!("{:?}", &out[12..]);
    println!("input still usable: {}", input.len());
}
```
Expected output: `[6.0, 6.5, 7.0, 7.5] input still usable: 16`

*Check 3: JoinHandle::join returns Err when the spawned thread panicked; the caller keeps running* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let h = std::thread::spawn(|| -> u32 { panic!("worker failed") });
    let r = h.join();
    println!("join is_err={}", r.is_err());
}
```
Expected output: `join is_err=true`

*Check 4: thread::scope re-panics in the caller when an un-joined scoped thread panicked* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
fn main() {
    println!("before");
    std::thread::scope(|s| {
        s.spawn(|| panic!("worker failed"));
    });
    println!("never printed");
}
```
Expected output: `before`

## Hand results between threads over mpsc or crossbeam channels and sort by a tag: arrival order is scheduling
**std::sync::mpsc offers an unbounded channel() and a bounded sync_channel(n) (n = 0 is a rendezvous); iterating the Receiver ends only after every Sender is dropped; with several producers the arrival order depends on scheduling, so tag each message and sort before the data reaches a hash or a report.**

*Check 1: Four producers, one receiver: drop(tx) ends the loop; sorting by tag gives a stable result* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel::<(usize, f64)>();
    for id in 0..4 {
        let tx = tx.clone();
        thread::spawn(move || {
            let partial: f64 = (0..1000).map(|i| (id * 1000 + i) as f64 * 0.1).sum();
            tx.send((id, partial)).unwrap();
        });
    }
    drop(tx); // otherwise the receiver below waits forever
    let mut got: Vec<(usize, f64)> = rx.iter().collect();
    got.sort_by_key(|&(id, _)| id); // arrival order is scheduling; the tag is not
    let ids: Vec<usize> = got.iter().map(|&(id, _)| id).collect();
    let total = got.iter().fold(0.0f64, |acc, &(_, p)| acc + p);
    println!("{ids:?} total bits {:016x}", total.to_bits());
}
```
Expected output: `[0, 1, 2, 3] total bits 4128687000000000`

*Check 2: sync_channel is bounded: try_send reports Full, a 0 bound needs a waiting receiver* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::mpsc::{sync_channel, TrySendError};

fn main() {
    let (tx, rx) = sync_channel::<u32>(1);
    println!("first: {:?}", tx.try_send(1).is_ok());
    println!("second full: {}", matches!(tx.try_send(2), Err(TrySendError::Full(2))));
    let (tx0, _rx0) = sync_channel::<u32>(0);
    println!("rendezvous, nobody receiving: {}", matches!(tx0.try_send(3), Err(TrySendError::Full(3))));
    drop(rx);
    println!("after receiver dropped: {}", matches!(tx.try_send(4), Err(TrySendError::Disconnected(4))));
}
```
Expected output: `first: true second full: true rendezvous, nobody receiving: true after receiver dropped: true`

*Check 3: std::sync::mpmc is unstable on 1.98.1 (E0658, mpmc_channel)* · `compile_fail` · edition 2024 · host · bin · errors: E0658 · stderr has “use of unstable library feature `mpmc_channel`” · **✔ oracle pass**
```rust
use std::sync::mpmc;

fn main() {
    let (_tx, _rx) = mpmc::channel::<u32>();
}
```

## Let the compiler infer Send and Sync: they turn data races into E0277/E0499, not race conditions or deadlocks
**Send and Sync are unsafe auto traits derived from a type's fields. An Rc or raw-pointer field stops a value moving to another thread and a Cell field stops it being shared (both E0277), and two threads writing one variable fail with E0499. A check-then-act on atomics still loses updates.**

*Check 1: Rc moved into thread::spawn is E0277 (not Send)* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “cannot be sent between threads safely” · **✔ oracle pass**
```rust
use std::rc::Rc;
use std::thread;

fn main() {
    let shared = Rc::new(5);
    let h = thread::spawn(move || println!("{shared}"));
    h.join().unwrap();
}
```

*Check 2: Cell<u32> is Send but &Cell<u32> is not, because Cell is not Sync* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “`&Cell<u32>` cannot be sent between threads safely” · stderr has “the trait `Sync` is not implemented for `Cell<u32>`” · **✔ oracle pass**
```rust
use std::cell::Cell;

fn assert_send<T: Send>() {}

fn main() {
    assert_send::<Cell<u32>>(); // fine: Cell<u32> is Send
    assert_send::<&Cell<u32>>(); // E0277: &T is Send only when T is Sync
}
```

*Check 3: A struct with a *mut f64 field is not Send once the closure captures all of it* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “`*mut f64` cannot be sent between threads safely” · **✔ oracle pass**
```rust
struct View {
    ptr: *mut f64,
    len: usize,
}

fn main() {
    let mut buf = vec![0.0f64; 4];
    let v = View { ptr: buf.as_mut_ptr(), len: buf.len() };
    let h = std::thread::spawn(move || {
        let v = v; // capture the whole struct, pointer included
        v.len
    });
    println!("{}", h.join().unwrap());
}
```

*Check 4: Edition 2021 captures only v.len, so the same struct crosses threads while the pointer is unused* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
struct View {
    ptr: *mut f64,
    len: usize,
}

fn main() {
    let mut buf = vec![0.0f64; 4];
    let v = View { ptr: buf.as_mut_ptr(), len: buf.len() };
    let h = std::thread::spawn(move || v.len); // disjoint capture: only the usize moves
    println!("{}", h.join().unwrap());
    let _still_here = v.ptr;
}
```
Expected output: `4`

*Check 5: Two scoped threads writing one f64 is rejected at compile time (E0499): no data race* · `compile_fail` · edition 2024 · host · bin · errors: E0499 · **✔ oracle pass**
```rust
fn main() {
    let mut total = 0.0f64;
    std::thread::scope(|s| {
        s.spawn(|| total += 1.0);
        s.spawn(|| total += 2.0);
    });
    println!("{total}");
}
```

*Check 6: Safe code still has race conditions: load-then-store loses an update, fetch_add does not* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::Barrier;
use std::sync::atomic::{AtomicU32, Ordering};

fn main() {
    let hits = AtomicU32::new(0);
    let both_loaded = Barrier::new(2);
    std::thread::scope(|s| {
        for _ in 0..2 {
            s.spawn(|| {
                let seen = hits.load(Ordering::SeqCst);
                both_loaded.wait(); // force both loads before either store
                hits.store(seen + 1, Ordering::SeqCst);
            });
        }
    });
    println!("load-then-store: {}", hits.load(Ordering::SeqCst));

    let hits = AtomicU32::new(0);
    std::thread::scope(|s| {
        for _ in 0..2 {
            s.spawn(|| hits.fetch_add(1, Ordering::SeqCst));
        }
    });
    println!("fetch_add: {}", hits.load(Ordering::SeqCst));
}
```
Expected output: `load-then-store: 1 fetch_add: 2`

## Make parallel float reductions bit-reproducible: fixed chunks, per-chunk partials, combined in index order
**Float addition is not associative, so a parallel sum's bits depend on where the input is split and how the partials are combined. rayon's sum, reduce and fold leave that order unspecified (fold's docs call its break points nondeterministic), so results can change between runs and thread counts. A chunk size fixed in the code, with partials folded sequentially in chunk order, gives the same bits for any thread count.**

*Check 1: Ten 0.1s summed in 1, 2, 3, 5 chunks: the bits depend on the split* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn chunked_sum(xs: &[f64], parts: usize) -> f64 {
    let size = xs.len().div_ceil(parts);
    let partials: Vec<f64> = std::thread::scope(|s| {
        let hs: Vec<_> = xs.chunks(size).map(|c| s.spawn(move || c.iter().sum::<f64>())).collect();
        hs.into_iter().map(|h| h.join().unwrap()).collect()
    });
    partials.iter().sum()
}

fn main() {
    let xs = vec![0.1f64; 10];
    for parts in [1, 2, 3, 5] {
        let s = chunked_sum(&xs, parts);
        println!("{parts} threads: {s:?} bits {:016x}", s.to_bits());
    }
}
```
Expected output: `1 threads: 0.9999999999999999 bits 3fefffffffffffff 2 threads: 1.0 bits 3ff0000000000000 3 threads: 1.0 bits 3ff0000000000000 5 threads: 1.0 bits 3ff0000000000000`

*Check 2: Fixed 4-element chunks combined in index order: identical bits for 1..=6 threads* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
const CHUNK: usize = 4; // part of the computation, never derived from the thread count

fn fixed_chunk_sum(xs: &[f64], threads: usize) -> f64 {
    let n_chunks = xs.len().div_ceil(CHUNK);
    let mut partials = vec![0.0f64; n_chunks];
    std::thread::scope(|s| {
        let per = n_chunks.div_ceil(threads);
        for (t, out) in partials.chunks_mut(per).enumerate() {
            s.spawn(move || {
                for (k, slot) in out.iter_mut().enumerate() {
                    let c = t * per + k;
                    let end = ((c + 1) * CHUNK).min(xs.len());
                    *slot = xs[c * CHUNK..end].iter().sum();
                }
            });
        }
    });
    partials.iter().sum() // one sequential fold, in chunk order
}

fn main() {
    let xs: Vec<f64> = (0..37).map(|i| 0.1 * i as f64 + 1e-3 / (i as f64 + 1.0)).collect();
    let bits: Vec<u64> = (1..=6).map(|t| fixed_chunk_sum(&xs, t).to_bits()).collect();
    println!("identical for 1..=6 threads: {}", bits.iter().all(|&b| b == bits[0]));
    let seq: f64 = xs.iter().sum();
    println!("equals plain sequential sum: {}", seq.to_bits() == bits[0]);
}
```
Expected output: `identical for 1..=6 threads: true equals plain sequential sum: false`

## Pick Mutex, RwLock or Condvar by job, and decide what a poisoned lock means before a panic decides for you
**Mutex<T> hands one thread &mut T at a time; RwLock<T> allows many readers or one writer under an OS-dependent priority policy; Condvar::wait_while sleeps until a predicate over the guarded state holds; a panic while holding a Mutex (or an RwLock in write mode) poisons it, and poisoning is only advisory.**

*Check 1: A panic while holding the guard poisons the Mutex; into_inner recovers, clear_poison resets* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let m = Arc::new(Mutex::new(7u32));
    let m2 = Arc::clone(&m);
    let r = thread::spawn(move || {
        let _g = m2.lock().unwrap();
        panic!("invariant broken while locked");
    })
    .join();
    println!("thread failed: {}", r.is_err());
    println!("poisoned: {}", m.is_poisoned());
    let v = match m.lock() {
        Ok(g) => *g,
        Err(poisoned) => *poisoned.into_inner(),
    };
    println!("recovered: {v}");
    m.clear_poison();
    println!("lock ok after clear_poison: {}", m.lock().is_ok());
}
```
Expected output: `thread failed: true poisoned: true recovered: 7 lock ok after clear_poison: true`

*Check 2: try_lock on a mutex this thread already holds reports WouldBlock instead of deadlocking* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::{Mutex, TryLockError};

fn main() {
    let m = Mutex::new(0u32);
    let _held = m.lock().unwrap();
    match m.try_lock() {
        Err(TryLockError::WouldBlock) => println!("WouldBlock"),
        Err(TryLockError::Poisoned(_)) => println!("Poisoned"),
        Ok(_) => println!("acquired twice"),
    }
}
```
Expected output: `WouldBlock`

*Check 3: A reader's panic leaves an RwLock unpoisoned; a writer's panic poisons it* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::{Arc, RwLock};
use std::thread;

fn main() {
    let l = Arc::new(RwLock::new(1u32));
    let a = Arc::clone(&l);
    let _ = thread::spawn(move || {
        let _r = a.read().unwrap();
        panic!("reader");
    })
    .join();
    println!("after reader panic: {}", l.is_poisoned());
    let b = Arc::clone(&l);
    let _ = thread::spawn(move || {
        let _w = b.write().unwrap();
        panic!("writer");
    })
    .join();
    println!("after writer panic: {}", l.is_poisoned());
}
```
Expected output: `after reader panic: false after writer panic: true`

*Check 4: Condvar::wait_while sleeps until the guarded predicate holds* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::{Arc, Condvar, Mutex};
use std::thread;

fn main() {
    let pair = Arc::new((Mutex::new(0u32), Condvar::new()));
    let p2 = Arc::clone(&pair);
    let producer = thread::spawn(move || {
        for _ in 0..3 {
            let (lock, cv) = &*p2;
            *lock.lock().unwrap() += 1;
            cv.notify_all();
        }
    });
    let (lock, cv) = &*pair;
    let g = cv.wait_while(lock.lock().unwrap(), |n| *n < 3).unwrap();
    println!("ready {}", *g);
    drop(g);
    producer.join().unwrap();
}
```
Expected output: `ready 3`

## Publish data across threads with a Release store and an Acquire load; keep Relaxed for counters
**Rust atomics follow the C++20 model: a Release store paired with an Acquire load of the same atomic makes every earlier write visible after the load, Relaxed only makes each operation atomic, SeqCst adds one total order, and an ordering an operation cannot take is a deny-by-default lint (or a run-time panic when it arrives in a variable).**

*Check 1: Release store + Acquire load publishes the payload written before the flag* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::thread;

static DATA: AtomicU64 = AtomicU64::new(0);
static READY: AtomicBool = AtomicBool::new(false);

fn main() {
    let reader = thread::spawn(|| {
        while !READY.load(Ordering::Acquire) {
            std::hint::spin_loop();
        }
        f64::from_bits(DATA.load(Ordering::Relaxed))
    });
    DATA.store(1.25f64.to_bits(), Ordering::Relaxed);
    READY.store(true, Ordering::Release);
    println!("{}", reader.join().unwrap());
}
```
Expected output: `1.25`

*Check 2: An Acquire store is rejected by the deny-by-default invalid_atomic_ordering lint* · `compile_fail` · edition 2024 · host · bin · lints: invalid_atomic_ordering · stderr has “atomic stores cannot have `Acquire` or `AcqRel` ordering” · **✔ oracle pass**
```rust
use std::sync::atomic::{AtomicBool, Ordering};

static READY: AtomicBool = AtomicBool::new(false);

fn main() {
    READY.store(true, Ordering::Acquire);
}
```

*Check 3: The same invalid ordering passed through a variable compiles and panics at run time* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
use std::sync::atomic::{AtomicBool, Ordering};

static READY: AtomicBool = AtomicBool::new(false);

fn publish(order: Ordering) {
    READY.store(true, order);
}

fn main() {
    println!("storing");
    publish(std::hint::black_box(Ordering::Acquire));
    println!("unreachable");
}
```
Expected output: `storing`

*Check 4: Relaxed fetch_add from 8 threads never loses an increment* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::atomic::{AtomicUsize, Ordering};

static HITS: AtomicUsize = AtomicUsize::new(0);

fn main() {
    std::thread::scope(|s| {
        for _ in 0..8 {
            s.spawn(|| {
                for _ in 0..1000 {
                    HITS.fetch_add(1, Ordering::Relaxed);
                }
            });
        }
    });
    println!("{}", HITS.load(Ordering::Relaxed));
}
```
Expected output: `8000`

*Check 5: std has no AtomicF64 on 1.98.1 (E0432): store f64 bits in an AtomicU64* · `compile_fail` · edition 2024 · host · bin · errors: E0432 · **✔ oracle pass**
```rust
use std::sync::atomic::AtomicF64;

fn main() {
    let _ = AtomicF64::new(0.0);
}
```

*Check 6: A compare_exchange busy flag refuses a second entry; builds for wasm32 without +atomics* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · imports nothing · node calls demo() · **✔ oracle pass**
```rust
use std::sync::atomic::{AtomicBool, Ordering};

static BUSY: AtomicBool = AtomicBool::new(false);

fn enter() -> bool {
    BUSY.compare_exchange(false, true, Ordering::Acquire, Ordering::Relaxed).is_ok()
}

fn leave() {
    BUSY.store(false, Ordering::Release);
}

#[unsafe(no_mangle)]
pub extern "C" fn demo() -> u32 {
    let a = enter() as u32; // 1: entered
    let b = enter() as u32; // 0: refused while busy
    leave();
    let c = enter() as u32; // 1: entered again
    a * 100 + b * 10 + c
}
```
Expected output: `101`

## Serialize native calls into the law: static needs Sync, static mut skips the check, a Mutex restores it
**A plain static must be Sync (E0277 'shared static variables must have a type that implements `Sync`') but a static mut is exempt, so a static-mut world compiles with no thread-safety check at all. A native host must own the law on one thread or put it behind a static Mutex, which compiles because rapier3d-f64 0.35.3's PhysicsWorld and KinematicCharacterController are Send. LazyLock (1.80) and OnceLock (1.70) cover read-only globals.**

*Check 1: A non-mut static of a non-Sync type is E0277* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “shared static variables must have a type that implements `Sync`” · **✔ oracle pass**
```rust
use std::cell::RefCell;

static SNAPSHOT: RefCell<Vec<u8>> = RefCell::new(Vec::new());

fn main() {
    SNAPSHOT.borrow_mut().push(1);
}
```

*Check 2: A static mut of the same non-Sync type compiles: the Sync check is skipped* · `compiles` · edition 2021 · host · lib · **✔ oracle pass**
```rust
use std::cell::RefCell;

pub static mut SNAPSHOT: RefCell<Vec<u8>> = RefCell::new(Vec::new());

pub fn push(b: u8) {
    // SAFETY: only sound if every caller is on one thread; nothing checks that.
    unsafe { (*core::ptr::addr_of_mut!(SNAPSHOT)).borrow_mut().push(b) }
}
```

*Check 3: rapier3d-f64 0.35.3 PhysicsWorld and KinematicCharacterController fit a static Mutex* · `compiles` · edition 2024 · host · lib · deps: rapier3d_f64 · **✔ oracle pass**
```rust
use std::sync::Mutex;
use rapier3d_f64::control::KinematicCharacterController;
use rapier3d_f64::prelude::*;

pub struct Law {
    pub world: PhysicsWorld,
    pub controller: KinematicCharacterController,
    pub snapshot: Vec<u8>,
}

pub static LAW: Mutex<Option<Law>> = Mutex::new(None);

fn assert_send<T: Send>() {}
fn assert_sync<T: Sync>() {}

pub fn probe() {
    assert_send::<PhysicsWorld>();
    assert_sync::<PhysicsWorld>();
    assert_send::<KinematicCharacterController>();
}
```

*Check 4: try_lock-based exports refuse (0) while another caller holds the law or after it panicked* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::{Mutex, TryLockError};

struct Law {
    steps: u32,
}

static LAW: Mutex<Law> = Mutex::new(Law { steps: 0 });

fn solver_step() -> u32 {
    match LAW.try_lock() {
        Ok(mut law) => {
            law.steps += 1;
            1
        }
        Err(TryLockError::WouldBlock) => 0,
        Err(TryLockError::Poisoned(_)) => 0,
    }
}

fn main() {
    println!("free: {}", solver_step());
    let held = LAW.lock().unwrap();
    println!("while another caller holds it: {}", solver_step());
    drop(held);
    let r = std::thread::spawn(|| {
        let _g = LAW.lock().unwrap();
        panic!("law panicked mid-step");
    })
    .join();
    println!("thread failed: {}", r.is_err());
    println!("after a panic inside the law: {}", solver_step());
}
```
Expected output: `free: 1 while another caller holds it: 0 thread failed: true after a panic inside the law: 0`

*Check 5: A static LazyLock table initialises exactly once under 8 racing threads* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::LazyLock;
use std::sync::atomic::{AtomicUsize, Ordering};

static INITS: AtomicUsize = AtomicUsize::new(0);
static TABLE: LazyLock<Vec<f64>> = LazyLock::new(|| {
    INITS.fetch_add(1, Ordering::Relaxed);
    (0..256).map(|i| i as f64 / 256.0).collect()
});

fn main() {
    std::thread::scope(|s| {
        for _ in 0..8 {
            s.spawn(|| TABLE[255]);
        }
    });
    println!("len {} inits {}", TABLE.len(), INITS.load(Ordering::Relaxed));
}
```
Expected output: `len 256 inits 1`

*Check 6: A LazyLock whose initializer panicked panics on every later access (unrecoverable)* · `runs` · edition 2024 · host · bin · exit code 101 · **✔ oracle pass**
```rust
use std::sync::LazyLock;

static TABLE: LazyLock<Vec<f64>> = LazyLock::new(|| panic!("table source missing"));

fn main() {
    let first = std::thread::spawn(|| TABLE.len()).join();
    println!("first access failed: {}", first.is_err());
    println!("second access: {}", TABLE.len());
}
```
Expected output: `first access failed: true`

*Check 7: OnceLock::set succeeds once and returns Err(value) afterwards* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::sync::OnceLock;

static LAW_VERSION: OnceLock<u32> = OnceLock::new();

fn main() {
    println!("first set: {:?}", LAW_VERSION.set(3));
    println!("second set: {:?}", LAW_VERSION.set(4));
    println!("value: {}", LAW_VERSION.get_or_init(|| 99));
}
```
Expected output: `first set: Ok(()) second set: Err(4) value: 3`

*Check 8: thread_local! is not a fix: each calling thread silently gets its own state* · `runs` · edition 2024 · host · bin · no warnings · **✔ oracle pass**
```rust
use std::cell::Cell;

thread_local! {
    static STEPS: Cell<u32> = const { Cell::new(0) };
}

fn step() {
    STEPS.with(|s| s.set(s.get() + 1));
}

fn main() {
    step();
    step();
    let other = std::thread::spawn(|| {
        step();
        STEPS.with(|s| s.get())
    })
    .join()
    .unwrap();
    println!("main thread saw {}, other thread saw {}", STEPS.with(|s| s.get()), other);
}
```
Expected output: `main thread saw 2, other thread saw 1`

*Check 9: The same static Mutex compiles and runs on wasm32-unknown-unknown with no imports* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · imports nothing · node calls bump() · **✔ oracle pass**
```rust
use std::sync::Mutex;

static LAW: Mutex<Option<Vec<f64>>> = Mutex::new(None);

#[unsafe(no_mangle)]
pub extern "C" fn bump() -> u32 {
    let mut g = LAW.lock().unwrap();
    g.get_or_insert_with(Vec::new).push(1.0);
    drop(g);
    let mut g = LAW.lock().unwrap();
    let v = g.as_mut().unwrap();
    v.push(2.0);
    v.len() as u32
}
```
Expected output: `2`

## Spawn only Send + 'static futures: no std MutexGuard or Rc across .await, CPU-bound work to spawn_blocking
**tokio::spawn (1.53.1) requires F: Future + Send + 'static because a task can move between worker threads. A std MutexGuard or Rc alive across an .await makes the future !Send; on 1.98.1 the error 'future cannot be sent between threads safely' carries no error code. Blocking or long CPU work belongs on spawn_blocking or rayon. Async closures (1.85) are for callbacks awaited in place.**

*Check 1: std MutexGuard held across .await: the future is !Send and a Send-bounded spawn rejects it* · `compile_fail` · edition 2024 · host · bin · stderr has “future cannot be sent between threads safely” · stderr has “has type `std::sync::MutexGuard<'_, u32>` which is not `Send`” · **✔ oracle pass**
```rust
use std::future::Future;
use std::sync::Mutex;

static STATE: Mutex<u32> = Mutex::new(0);

// Same bounds as tokio::spawn.
fn spawn<F: Future + Send + 'static>(_f: F) {}

async fn io() {}

fn main() {
    spawn(async {
        let mut g = STATE.lock().unwrap();
        *g += 1;
        io().await;
        *g += 1;
    });
}
```

*Check 2: Not using the guard after the await is not enough: it still drops at scope end* · `compile_fail` · edition 2024 · host · bin · stderr has “future cannot be sent between threads safely” · stderr has “await occurs here” · **✔ oracle pass**
```rust
use std::future::Future;
use std::sync::Mutex;

static STATE: Mutex<u32> = Mutex::new(0);

fn spawn<F: Future + Send + 'static>(_f: F) {}

async fn io() {}

fn main() {
    spawn(async {
        let mut g = STATE.lock().unwrap();
        *g += 1;
        io().await; // g is still alive here
    });
}
```

*Check 3: Confining the guard to an inner block before the await makes the future Send* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
use std::future::Future;
use std::sync::Mutex;

static STATE: Mutex<u32> = Mutex::new(0);

fn spawn<F: Future + Send + 'static>(_f: F) {}

async fn io() {}

pub fn go() {
    spawn(async {
        {
            let mut g = STATE.lock().unwrap();
            *g += 1;
        } // guard dropped before the await
        io().await;
    });
}
```

*Check 4: drop(g) after using the guard still leaves the future !Send on 1.98.1* · `compile_fail` · edition 2024 · host · lib · stderr has “future cannot be sent between threads safely” · stderr has “maybe used later” · **✔ oracle pass**
```rust
use std::future::Future;
use std::sync::Mutex;

static STATE: Mutex<u32> = Mutex::new(0);

fn spawn<F: Future + Send + 'static>(_f: F) {}

async fn io() {}

pub fn go() {
    spawn(async {
        let mut g = STATE.lock().unwrap();
        *g += 1;
        drop(g); // moved out, yet the borrowed local still counts as live
        io().await;
    });
}
```

*Check 5: Even a read through the guard before drop(g) keeps the future !Send* · `compile_fail` · edition 2024 · host · lib · stderr has “future cannot be sent between threads safely” · stderr has “maybe used later” · **✔ oracle pass**
```rust
use std::future::Future;
use std::sync::Mutex;

static STATE: Mutex<u32> = Mutex::new(0);

fn spawn<F: Future + Send + 'static>(_f: F) {}

async fn io() {}

pub fn go() {
    spawn(async {
        let g = STATE.lock().unwrap();
        let seen = *g;
        drop(g);
        io().await;
        let _ = seen;
    });
}
```

*Check 6: A guard that lives only inside one statement is dropped before the await: Send* · `compiles` · edition 2024 · host · lib · no warnings · **✔ oracle pass**
```rust
use std::future::Future;
use std::sync::Mutex;

static STATE: Mutex<u32> = Mutex::new(0);

fn spawn<F: Future + Send + 'static>(_f: F) {}

async fn io() {}

pub fn go() {
    spawn(async {
        *STATE.lock().unwrap() += 1; // temporary guard dropped at the semicolon
        io().await;
    });
}
```

*Check 7: Async closure (1.85) into an AsyncFnMut bound borrows its captures; prelude, edition 2021* · `runs` · edition 2021 · host · bin · **✔ oracle pass**
```rust
use std::future::Future;
use std::pin::pin;
use std::task::{Context, Poll, Waker};

// A test-only executor: busy-polls with a waker that discards wake-ups.
fn block_on<F: Future>(fut: F) -> F::Output {
    let mut fut = pin!(fut);
    let mut cx = Context::from_waker(Waker::noop());
    loop {
        if let Poll::Ready(v) = fut.as_mut().poll(&mut cx) {
            return v;
        }
    }
}

async fn feed(mut sink: impl AsyncFnMut(u32)) {
    sink(1).await;
    sink(2).await;
}

fn main() {
    let mut seen = Vec::new();
    block_on(feed(async |x| seen.push(x)));
    println!("{seen:?}");
}
```
Expected output: `[1, 2]`

*Check 8: The pre-1.85 FnMut -> Future callback cannot let its future borrow the captures* · `compile_fail` · edition 2021 · host · bin · errors: E0373 · stderr has “captured variable cannot escape `FnMut` closure body” · **✔ oracle pass**
```rust
use std::future::Future;

async fn feed<F, Fut>(mut sink: F)
where
    F: FnMut(u32) -> Fut,
    Fut: Future<Output = ()>,
{
    sink(1).await;
    sink(2).await;
}

fn main() {
    let mut seen: Vec<u32> = Vec::new();
    let _ = feed(|x| async { seen.push(x) });
}
```

*Check 9: Adding async move to the old callback only turns it into E0507* · `compile_fail` · edition 2021 · host · bin · errors: E0507 · stderr has “cannot move out of `seen`, a captured variable in an `FnMut` closure” · **✔ oracle pass**
```rust
use std::future::Future;

async fn feed<F, Fut>(mut sink: F)
where
    F: FnMut(u32) -> Fut,
    Fut: Future<Output = ()>,
{
    sink(1).await;
    sink(2).await;
}

fn main() {
    let mut seen: Vec<u32> = Vec::new();
    let _ = feed(|x| async move { seen.push(x) });
}
```

*Check 10: An async closure's future borrows the closure, so it cannot meet spawn's 'static (E0597)* · `compile_fail` · edition 2024 · host · bin · errors: E0597 · stderr has “argument requires that `push` is borrowed for `'static`” · **✔ oracle pass**
```rust
use std::future::Future;

// Same bounds as tokio::spawn.
fn spawn<F: Future + Send + 'static>(_f: F) {}

fn main() {
    let mut seen: Vec<u32> = Vec::new();
    let mut push = async |x: u32| seen.push(x);
    spawn(push(1));
}
```

## Treat a future as an inert, pinned state machine: nothing runs until polled, and dropping it cancels it
**Calling an async fn only builds a future, a compiler-generated state machine that stores every local alive across an .await. Nothing runs until an executor polls it through Pin<&mut Self>; async-block futures are !Unpin and must be pinned (pin!, 1.68, or Box::pin). Dropping a pending future runs its destructors, and the code after its current .await never executes.**

*Check 1: An un-awaited future is an unused_must_use warning and its body never runs* · `runs` · edition 2024 · host · bin · lints: unused_must_use · stderr has “futures do nothing unless you `.await` or poll them” · **✔ oracle pass**
```rust
async fn step() -> u32 {
    println!("step body ran");
    1
}

fn main() {
    step(); // builds the state machine, runs nothing
    println!("main done");
}
```
Expected output: `main done`

*Check 2: The body runs only when block_on polls it (pin! + Waker::noop executor)* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::future::Future;
use std::pin::pin;
use std::task::{Context, Poll, Waker};

// A test-only executor: busy-polls with a waker that discards wake-ups.
fn block_on<F: Future>(fut: F) -> F::Output {
    let mut fut = pin!(fut);
    let mut cx = Context::from_waker(Waker::noop());
    loop {
        if let Poll::Ready(v) = fut.as_mut().poll(&mut cx) {
            return v;
        }
    }
}

async fn law_step(x: u32) -> u32 {
    println!("body runs");
    x * 2
}

fn main() {
    let fut = law_step(21);
    println!("future created");
    let v = block_on(fut);
    println!("result {v}");
}
```
Expected output: `future created body runs result 42`

*Check 3: Pin::new on an async block is E0277: the future is !Unpin (use pin! or Box::pin)* · `compile_fail` · edition 2024 · host · bin · errors: E0277 · stderr has “cannot be unpinned” · stderr has “consider using the `pin!` macro” · **✔ oracle pass**
```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Waker};

fn main() {
    let mut fut = async { 1u32 };
    let mut cx = Context::from_waker(Waker::noop());
    let _ = Pin::new(&mut fut).poll(&mut cx);
}
```

*Check 4: Dropping a pending future runs its Drop guards; code after the await never runs* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
use std::future::Future;
use std::pin::{pin, Pin};
use std::task::{Context, Poll, Waker};

struct YieldOnce(bool);

impl Future for YieldOnce {
    type Output = ();
    fn poll(mut self: Pin<&mut Self>, _cx: &mut Context<'_>) -> Poll<()> {
        if self.0 {
            Poll::Ready(())
        } else {
            self.0 = true;
            Poll::Pending
        }
    }
}

struct Guard;

impl Drop for Guard {
    fn drop(&mut self) {
        println!("guard dropped");
    }
}

async fn task() {
    let _g = Guard;
    println!("before await");
    YieldOnce(false).await;
    println!("after await");
}

fn main() {
    let mut cx = Context::from_waker(Waker::noop());
    {
        let mut fut = pin!(task());
        let first = fut.as_mut().poll(&mut cx);
        println!("first poll pending: {}", first.is_pending());
    } // the future is dropped here, mid-flight
    println!("future dropped");
}
```
Expected output: `before await first poll pending: true guard dropped future dropped`

*Check 5: A local held across an await lives in the future: 4 KiB buffer >= 4096 bytes* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
async fn noop() {}

async fn holds_buffer() -> u8 {
    let buf = [7u8; 4096];
    noop().await;
    buf[4095]
}

async fn drops_buffer() -> u8 {
    let last = {
        let buf = [7u8; 4096];
        buf[4095]
    };
    noop().await;
    last
}

fn main() {
    let a = std::mem::size_of_val(&holds_buffer());
    let b = std::mem::size_of_val(&drops_buffer());
    println!("holds >= 4096: {}, drops < 64: {}", a >= 4096, b < 64);
}
```
Expected output: `holds >= 4096: true, drops < 64: true`

## Keep the wasm law single-threaded: no threads on wasm32-unknown-unknown, rapier3d-f64's parallel left off
**On wasm32-unknown-unknown, std::thread::spawn panics (Builder::spawn returns Err) and available_parallelism errs. Shared-memory threads need the unstable `atomics` target feature plus a core and std rebuilt with it (nightly -Zbuild-std): stable 1.98.1's shipped core and std refuse --shared-memory at link time. Rapier 0.35.3 declares no conflict between `parallel` and `enhanced-determinism`, and its changelog says they 'can now be combined' with bitwise-identical results for any pool size.**

*Check 1: wasm32-unknown-unknown: thread::Builder::spawn returns Err* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · imports nothing · node calls spawn_fails() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn spawn_fails() -> u32 {
    std::thread::Builder::new().spawn(|| ()).is_err() as u32
}
```
Expected output: `1`

*Check 2: wasm32-unknown-unknown: available_parallelism returns Err* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls parallelism_unknown() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn parallelism_unknown() -> u32 {
    std::thread::available_parallelism().is_err() as u32
}
```
Expected output: `1`

*Check 3: wasm32-unknown-unknown on 1.98.1: the atomics target feature is off by default* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls atomics_on() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn atomics_on() -> u32 {
    cfg!(target_feature = "atomics") as u32
}
```
Expected output: `0`

*Check 4: +atomics with --shared-memory fails to link against the shipped std (not built with atomics)* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “unstable feature specified for `-Ctarget-feature`: `atomics`” · stderr has “--shared-memory is disallowed by std-” · stderr has “because it was not compiled with 'atomics' or 'bulk-memory' features” · **✔ oracle pass**
```rust
use std::sync::atomic::{AtomicU32, Ordering};

static COUNT: AtomicU32 = AtomicU32::new(0);

#[unsafe(no_mangle)]
pub extern "C" fn bump() -> u32 {
    COUNT.fetch_add(1, Ordering::Relaxed) + 1
}
```

*Check 5: Even #![no_std] fails: the shipped core was not compiled with atomics either* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “--shared-memory is disallowed by core-” · stderr has “because it was not compiled with 'atomics' or 'bulk-memory' features” · **✔ oracle pass**
```rust
#![no_std]
use core::sync::atomic::{AtomicU32, Ordering};

static COUNT: AtomicU32 = AtomicU32::new(0);

#[unsafe(no_mangle)]
pub extern "C" fn bump() -> u32 {
    COUNT.fetch_add(1, Ordering::Relaxed) + 1
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
```

*Check 6: The solver's rapier build (enhanced-determinism, no parallel) has no rapier3d_f64::rayon* · `compile_fail` · edition 2024 · host · lib · deps: rapier3d_f64 · errors: E0432 · stderr has “the item is gated behind the `parallel` feature” · **✔ oracle pass**
```rust
pub use rapier3d_f64::rayon;
```

*Check 7: Without parallel the thread-pool API is compiled out (E0599 configure_thread_pool)* · `compile_fail` · edition 2024 · host · lib · deps: rapier3d_f64 · errors: E0599 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

pub fn try_pool() {
    let mut pipeline = PhysicsPipeline::new();
    let _ = pipeline.configure_thread_pool(2);
}
```

*Check 8: PhysicsHooks must be Sync even with parallel off: a Cell counter in a hook is E0277* · `compile_fail` · edition 2024 · host · lib · deps: rapier3d_f64 · errors: E0277 · stderr has “`Cell<u32>` cannot be shared between threads safely” · stderr has “required for `CountingHooks` to implement `MaybeSync`” · **✔ oracle pass**
```rust
use std::cell::Cell;
use rapier3d_f64::prelude::*;

pub struct CountingHooks {
    pub calls: Cell<u32>,
}

impl PhysicsHooks for CountingHooks {}
```

