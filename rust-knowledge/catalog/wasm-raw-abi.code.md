# Rust → WebAssembly without bindgen — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](wasm-raw-abi.md) · [catalog index](README.md)

## Choose wasm32v1-none only for an all-no_std crate graph: MVP features, own panic handler and allocator
**wasm32v1-none ships core and alloc built for WebAssembly 1.0 (MVP plus mutable-globals) on stable; the crate must be #![no_std] with a #[panic_handler] and needs a #[global_allocator] to use alloc - and the pinned solver graph cannot build for it.**

*Check 1: a std crate cannot build for wasm32v1-none (E0463)* · `compile_fail` · edition 2024 · wasm32v1-none · cdylib · errors: E0463 · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn add(a: f64, b: f64) -> f64 {
    a + b
}
```

*Check 2: a no_std cdylib must define #[panic_handler]* · `compile_fail` · edition 2024 · wasm32v1-none · cdylib · stderr has “`#[panic_handler]` function required, but not found” · **✔ oracle pass**
```rust
#![no_std]
#[unsafe(no_mangle)]
pub extern "C" fn add(a: f64, b: f64) -> f64 {
    a + b
}
```

*Check 3: using alloc on wasm32v1-none requires a #[global_allocator]* · `compile_fail` · edition 2024 · wasm32v1-none · cdylib · stderr has “no global memory allocator found but one is required” · **✔ oracle pass**
```rust
#![no_std]
extern crate alloc;
use alloc::vec::Vec;
#[panic_handler]
fn on_panic(_: &core::panic::PanicInfo) -> ! {
    core::arch::wasm32::unreachable()
}
#[unsafe(no_mangle)]
pub extern "C" fn sum(n: u32) -> f64 {
    let v: Vec<f64> = (0..n).map(|i| i as f64).collect();
    v.iter().sum()
}
```

*Check 4: a minimal no_std module builds with only mutable-globals, imports nothing and runs* · `runs` · edition 2024 · wasm32v1-none · cdylib · no warnings · exports memory, add · imports nothing · node calls add(1.5, 2.25) · **✔ oracle pass**
```rust
#![no_std]
#[cfg(any(target_feature = "bulk-memory", target_feature = "sign-ext", target_feature = "nontrapping-fptoint",
          target_feature = "multivalue", target_feature = "reference-types"))]
compile_error!("a post-1.0 feature is enabled");
#[cfg(not(target_feature = "mutable-globals"))]
compile_error!("mutable-globals is off");
#[panic_handler]
fn on_panic(_: &core::panic::PanicInfo) -> ! {
    core::arch::wasm32::unreachable()
}
#[unsafe(no_mangle)]
pub extern "C" fn add(a: f64, b: f64) -> f64 {
    a + b
}
```
Expected output: `3.75`

## Export the law with #[unsafe(no_mangle)] extern "C" fns and read each signature as JS sees it
**In a wasm cdylib the no_mangle / export_name attribute (not pub, not extern "C") decides what is exported, an undeclared extern is a link error since Rust 1.96, and every argument and result crosses JS as an i32, i64 (BigInt), f32 or f64.**

*Check 1: edition 2024 rejects a bare #[no_mangle] (unsafe attribute used without unsafe)* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “unsafe attribute used without unsafe” · **✔ oracle pass**
```rust
#[no_mangle]
pub extern "C" fn add(a: f64, b: f64) -> f64 {
    a + b
}
```

*Check 2: no_mangle/export_name decide exports: a private no_mangle fn is exported, a pub fn is not needed* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · exports memory, private_but_exported, law_step · does not export public_but_not_exported, step_impl · imports nothing · node calls law_step() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
extern "C" fn private_but_exported() -> u32 {
    1
}
pub extern "C" fn public_but_not_exported() -> u32 {
    2
}
#[unsafe(export_name = "law_step")]
pub extern "C" fn step_impl() -> u32 {
    3
}
```
Expected output: `3`

*Check 3: a u32 result of u32::MAX reaches JS as the signed number -1* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls u32_max() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn u32_max() -> u32 {
    u32::MAX
}
```
Expected output: `-1`

*Check 4: a u64 crosses as a signed BigInt: u64::MAX comes back as -1n* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls add_u64(18446744073709551615n, 0n) · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn add_u64(a: u64, b: u64) -> u64 {
    a.wrapping_add(b)
}
```
Expected output: `-1`

*Check 5: an undeclared extern fn is a link error on 1.98.1 (no --allow-undefined)* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “undefined symbol: host_log” · **✔ oracle pass**
```rust
// An extern the host was supposed to provide, declared without #[link(wasm_import_module)].
unsafe extern "C" {
    fn host_log(x: f64);
}
#[unsafe(no_mangle)]
pub extern "C" fn add(a: f64, b: f64) -> f64 {
    unsafe { host_log(a) };
    a + b
}
```

*Check 6: #[link(wasm_import_module)] turns the same extern into a module import and links* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · exports memory, add · imports exactly host.host_log · **✔ oracle pass**
```rust
#[link(wasm_import_module = "host")]
unsafe extern "C" {
    fn host_log(x: f64);
}
#[unsafe(no_mangle)]
pub extern "C" fn add(a: f64, b: f64) -> f64 {
    unsafe { host_log(a) };
    a + b
}
```

*Check 7: a tuple parameter in an extern "C" export draws improper_ctypes_definitions* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · lints: improper_ctypes_definitions · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn pair(p: (f64, f64)) -> f64 {
    p.0 + p.1
}
```

## Hand JS pointers to 8-aligned static f64 buffers made with &raw mut, and index Float64Array only by ptr / 8
**A static [f64; N] is 8-aligned on wasm32 so ptr / 8 is an exact index; a byte buffer is 1-aligned unless raised with repr(align(8)); and a misaligned whole-buffer index is silently ignored by JS.**

*Check 1: edition 2021: the engine's BODIES.as_mut_ptr() shape compiles with a static_mut_refs warning* · `compiles` · edition 2021 · wasm32-unknown-unknown · cdylib · lints: static_mut_refs · **✔ oracle pass**
```rust
static mut BODIES: [f64; 64 * 17] = [0.0; 64 * 17];
#[no_mangle]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    unsafe { BODIES.as_mut_ptr() }
}
```

*Check 2: edition 2024: the same shape is denied by static_mut_refs* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · lints: static_mut_refs · **✔ oracle pass**
```rust
static mut BODIES: [f64; 64 * 17] = [0.0; 64 * 17];
#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    unsafe { BODIES.as_mut_ptr() }
}
```

*Check 3: &raw mut pointers to a static f64 array and a repr(align(8)) byte buffer are both 8-aligned* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · node calls misaligned() · **✔ oracle pass**
```rust
static mut BODIES: [f64; 64 * 17] = [0.0; 64 * 17];
#[repr(C, align(8))]
struct Bytes([u8; 4096]);
static mut RESTORE: Bytes = Bytes([0; 4096]);
const _: () = assert!(core::mem::align_of::<f64>() == 8);
#[unsafe(no_mangle)]
pub extern "C" fn bodies_ptr() -> *mut f64 {
    (&raw mut BODIES).cast::<f64>()
}
#[unsafe(no_mangle)]
pub extern "C" fn restore_ptr() -> *mut u8 {
    (&raw mut RESTORE).cast::<u8>()
}
#[unsafe(no_mangle)]
pub extern "C" fn misaligned() -> u32 {
    (bodies_ptr() as usize % 8 + restore_ptr() as usize % 8) as u32
}
```
Expected output: `0`

*Check 4: an empty Vec<u8> static hands out the dangling pointer 1 (as snapshot_ptr does before a load)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls snapshot_ptr() · **✔ oracle pass**
```rust
static mut SNAPSHOT: Vec<u8> = Vec::new();
#[unsafe(no_mangle)]
pub extern "C" fn snapshot_ptr() -> u32 {
    unsafe { (*(&raw const SNAPSHOT)).as_ptr() as u32 }
}
```
Expected output: `1`

*Check 5: from_le_bytes decodes f64 words from a byte buffer at an odd offset, no alignment needed* · `runs` · edition 2024 · host · bin · **✔ oracle pass**
```rust
fn main() {
    let mut record = Vec::new();
    for x in [1.5f64, -0.0, 1e300] {
        record.extend_from_slice(&x.to_le_bytes());
    }
    // Place the record at offset 1 so no f64 in it is 8-aligned.
    let mut buffer = vec![0u8; 1];
    buffer.extend_from_slice(&record);
    let words: Vec<f64> = buffer[1..]
        .chunks_exact(8)
        .map(|c| f64::from_le_bytes(c.try_into().unwrap()))
        .collect();
    println!("{:?}", words);
}
```
Expected output: `[1.5, -0.0, 1e300]`

## Inspect the pinned .wasm with node, wasmparser or wasm-tools; never wasm-opt it unless that step is pinned too
**The digest pins exactly what cargo emitted; wasm-opt, wasm-pack's default wasm-opt pass and strip settings all rewrite bytes, and wasm-opt's -tnh and -ffm change behaviour, so any post-processing must be pinned in the build and re-pinned in the digest.**

*Check 1: wasmparser 0.259 reads exports, memory limits and a custom section, and rejects a bad export index* · `runs` · edition 2024 · host · bin · deps: wasmparser · **✔ oracle pass**
```rust
use wasmparser::{Parser, Payload, Validator};

// 76 bytes: memory (initial 17 pages, no maximum) exported as "memory",
// law_version() -> i32 { 3 }, and a custom section "si_law" holding "si-law-v1".
const MODULE: &[u8] = &[
    0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 5, 3, 1, 0, 17, 7, 24, 2, 6,
    109, 101, 109, 111, 114, 121, 2, 0, 11, 108, 97, 119, 95, 118, 101, 114, 115, 105, 111, 110,
    0, 0, 10, 6, 1, 4, 0, 65, 3, 11, 0, 16, 6, 115, 105, 95, 108, 97, 119, 115, 105, 45, 108,
    97, 119, 45, 118, 49,
];

fn main() {
    for payload in Parser::new(0).parse_all(MODULE) {
        match payload.expect("parse") {
            Payload::ExportSection(reader) => {
                for export in reader {
                    let export = export.expect("export");
                    println!("export {} {:?} {}", export.name, export.kind, export.index);
                }
            }
            Payload::MemorySection(reader) => {
                for memory in reader {
                    let memory = memory.expect("memory");
                    println!("memory initial={} maximum={:?} shared={}", memory.initial, memory.maximum, memory.shared);
                }
            }
            Payload::CustomSection(section) => {
                println!("custom {} {:?}", section.name(), String::from_utf8_lossy(section.data()));
            }
            _ => {}
        }
    }
    println!("validate: {}", Validator::new().validate_all(MODULE).is_ok());
    // Point the "law_version" export at function 1, which does not exist.
    let mut bad = MODULE.to_vec();
    let code = bad.windows(4).position(|w| w == [10, 6, 1, 4]).expect("code section");
    bad[code - 1] = 1;
    match Validator::new().validate_all(&bad) {
        Ok(_) => println!("corrupt: accepted"),
        Err(e) => println!("corrupt: {} at offset {}", e.message(), e.offset()),
    }
}
```
Expected output: `memory initial=17 maximum=None shared=false export memory Memory 0 export law_version Func 0 custom si_law "si-law-v1" validate: true corrupt: unknown function 1: exported function index out of bounds`

*Check 2: -C strip=symbols keeps the export names (exports are not a custom section)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · exports memory, law_version · node calls law_version() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn law_version() -> u32 {
    3
}
```
Expected output: `3`

## Keep the law's memory exported and know rustc's wasm layout: a 1 MiB stack first, then statics, then heap
**rustc links every wasm32 module with -z stack-size=1048576 and --stack-first, so __stack_pointer starts at 1 MiB and grows toward 0 with statics and the heap above it; --import-memory trades the memory export for an env.memory import.**

*Check 1: default layout: a stack local sits just under 1 MiB and statics start at 1 MiB* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls layout_ok() · **✔ oracle pass**
```rust
static mut FIRST: [f64; 2] = [0.0; 2];
#[unsafe(no_mangle)]
pub extern "C" fn layout_ok() -> u32 {
    let local = 0u8;
    let sp = core::hint::black_box(&local) as *const u8 as usize;
    let data = (&raw const FIRST) as usize;
    (sp < 1_048_576 && sp > 1_048_576 - 4096 && data >= 1_048_576) as u32
}
```
Expected output: `1`

*Check 2: -C link-arg=-zstack-size=65536 moves the stack top and the statics down to 64 KiB* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls layout_ok() · **✔ oracle pass**
```rust
static mut FIRST: [f64; 2] = [0.0; 2];
#[unsafe(no_mangle)]
pub extern "C" fn layout_ok() -> u32 {
    let local = 0u8;
    let sp = core::hint::black_box(&local) as *const u8 as usize;
    let data = (&raw const FIRST) as usize;
    (sp < 65_536 && sp > 65_536 - 4096 && data >= 65_536 && data < 1_048_576) as u32
}
```
Expected output: `1`

*Check 3: rustc passes -z stack-size=1048576 and --stack-first to rust-lld (visible in a failed link)* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “stack-size=1048576” · stderr has “--stack-first” · **✔ oracle pass**
```rust
// An extern the host was supposed to provide, declared without #[link(wasm_import_module)].
unsafe extern "C" {
    fn host_log(x: f64);
}
#[unsafe(no_mangle)]
pub extern "C" fn add(a: f64, b: f64) -> f64 {
    unsafe { host_log(a) };
    a + b
}
```

*Check 4: --export=__heap_base / --export=__data_end expose the linker symbols as exported globals* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · exports memory, add, __heap_base, __data_end · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn add(a: f64, b: f64) -> f64 {
    a + b
}
```

*Check 5: -C link-arg=--import-memory links (the module then imports env.memory; see how)* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · exports add · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn add(a: f64, b: f64) -> f64 {
    a + b
}
```

## Re-create every Float64Array after an export that can allocate: memory.grow detaches the old ArrayBuffer
**When the module's allocator executes memory.grow, the JS API detaches the previous ArrayBuffer: old views read undefined and drop writes without throwing.**

*Check 1: memory grows inside an export call when the allocator needs pages (33 pages for a 2 MiB block)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls grow_by_holding(2) · **✔ oracle pass**
```rust
static mut KEEP: Vec<Vec<u8>> = Vec::new();
#[unsafe(no_mangle)]
pub extern "C" fn grow_by_holding(mib: u32) -> u32 {
    let before = core::arch::wasm32::memory_size::<0>();
    let block = vec![1u8; mib as usize * 1024 * 1024];
    unsafe { (*(&raw mut KEEP)).push(block) };
    (core::arch::wasm32::memory_size::<0>() - before) as u32
}
```
Expected output: `33`

*Check 2: an export that only writes a static buffer does not grow memory* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls step_no_alloc(64) · **✔ oracle pass**
```rust
static mut BODIES: [f64; 64 * 17] = [0.0; 64 * 17];
#[unsafe(no_mangle)]
pub extern "C" fn step_no_alloc(n: u32) -> u32 {
    let before = core::arch::wasm32::memory_size::<0>();
    let bodies = unsafe { &mut *(&raw mut BODIES) };
    for i in 0..(n as usize).min(64) {
        bodies[i * 17 + 1] += -8.0 / 64.0;
    }
    (core::arch::wasm32::memory_size::<0>() - before) as u32
}
```
Expected output: `0`

## Read a wasm target's features with rustc --print cfg and pin them with cfg compile_error! guards
**rustc --print cfg --target wasm32-unknown-unknown shows the enabled features (1.98.1: bulk-memory, multivalue, mutable-globals, nontrapping-fptoint, reference-types, sign-ext); -C target-feature=-x removes one for the crates you compile, and a misspelled name only warns.**

*Check 1: the guard compiles cleanly under the 1.98.1 defaults (cfg names are known, no warnings)* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · **✔ oracle pass**
```rust
// Pins the feature set measured on 1.98.1; drift fails the build.
#[cfg(target_feature = "relaxed-simd")]
compile_error!("relaxed-simd is enabled");
#[cfg(target_feature = "simd128")]
compile_error!("simd128 is enabled");
#[cfg(not(all(target_feature = "bulk-memory", target_feature = "multivalue", target_feature = "mutable-globals",
              target_feature = "nontrapping-fptoint", target_feature = "reference-types", target_feature = "sign-ext")))]
compile_error!("the default feature set changed");
#[unsafe(no_mangle)]
pub extern "C" fn ok() -> u32 {
    1
}
```

*Check 2: the guard fails the build when relaxed-simd is switched on* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “relaxed-simd is enabled” · **✔ oracle pass**
```rust
// Pins the feature set measured on 1.98.1; drift fails the build.
#[cfg(target_feature = "relaxed-simd")]
compile_error!("relaxed-simd is enabled");
#[cfg(target_feature = "simd128")]
compile_error!("simd128 is enabled");
#[cfg(not(all(target_feature = "bulk-memory", target_feature = "multivalue", target_feature = "mutable-globals",
              target_feature = "nontrapping-fptoint", target_feature = "reference-types", target_feature = "sign-ext")))]
compile_error!("the default feature set changed");
#[unsafe(no_mangle)]
pub extern "C" fn ok() -> u32 {
    1
}
```

*Check 3: the guard fails the build when a default feature (bulk-memory) is switched off* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “the default feature set changed” · **✔ oracle pass**
```rust
// Pins the feature set measured on 1.98.1; drift fails the build.
#[cfg(target_feature = "relaxed-simd")]
compile_error!("relaxed-simd is enabled");
#[cfg(target_feature = "simd128")]
compile_error!("simd128 is enabled");
#[cfg(not(all(target_feature = "bulk-memory", target_feature = "multivalue", target_feature = "mutable-globals",
              target_feature = "nontrapping-fptoint", target_feature = "reference-types", target_feature = "sign-ext")))]
compile_error!("the default feature set changed");
#[unsafe(no_mangle)]
pub extern "C" fn ok() -> u32 {
    1
}
```

*Check 4: a misspelled feature (-relaxed_simd) only warns and the build succeeds* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “unknown and unstable feature specified for `-Ctarget-feature`: `relaxed_simd`” · stderr has “is not a recognized feature for this target (ignoring feature)” · **✔ oracle pass**
```rust
// Pins the feature set measured on 1.98.1; drift fails the build.
#[cfg(target_feature = "relaxed-simd")]
compile_error!("relaxed-simd is enabled");
#[cfg(target_feature = "simd128")]
compile_error!("simd128 is enabled");
#[cfg(not(all(target_feature = "bulk-memory", target_feature = "multivalue", target_feature = "mutable-globals",
              target_feature = "nontrapping-fptoint", target_feature = "reference-types", target_feature = "sign-ext")))]
compile_error!("the default feature set changed");
#[unsafe(no_mangle)]
pub extern "C" fn ok() -> u32 {
    1
}
```

## Return a status code from every export; under the wasm abort default a panic is an unreachable trap
**wasm32 targets default to panic=abort and unwinding cannot be built on stable, so a panic compiles to the unreachable trap, reaches JS as a WebAssembly.RuntimeError without the Rust message, and leaves linear memory as the panic found it.**

*Check 1: with no -C panic flag the wasm32-unknown-unknown cfg is panic = "abort"* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · **✔ oracle pass**
```rust
#[cfg(not(panic = "abort"))]
compile_error!("panic strategy is not abort");
#[unsafe(no_mangle)]
pub extern "C" fn f() -> u32 {
    1
}
```

*Check 2: -C panic=unwind cannot link on stable: the shipped panic_unwind is built for abort* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “does not have the panic strategy `unwind`” · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn f() -> u32 {
    1
}
```

*Check 3: a checked export refuses an out-of-range slot with status 0 instead of trapping* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls write_slot(9, 1.5) · **✔ oracle pass**
```rust
static mut SLOTS: [f64; 4] = [0.0; 4];
/// 1 = written, 0 = refused (slot out of range or NaN). Never panics.
#[unsafe(no_mangle)]
pub extern "C" fn write_slot(i: u32, v: f64) -> u32 {
    if i >= 4 || v.is_nan() {
        return 0;
    }
    let slots = unsafe { &mut *(&raw mut SLOTS) };
    slots[i as usize] = v;
    1
}
```
Expected output: `0`

*Check 4: the same export accepts an in-range slot with status 1* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls write_slot(2, 1.5) · **✔ oracle pass**
```rust
static mut SLOTS: [f64; 4] = [0.0; 4];
#[unsafe(no_mangle)]
pub extern "C" fn write_slot(i: u32, v: f64) -> u32 {
    if i >= 4 || v.is_nan() {
        return 0;
    }
    let slots = unsafe { &mut *(&raw mut SLOTS) };
    slots[i as usize] = v;
    1
}
```
Expected output: `1`

*Check 5: an unchecked export that indexes out of range panics, and under panic=abort the panic is a WebAssembly trap (RuntimeError: unreachable)* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · the trap message has “unreachable” · node calls write_slot_unchecked(9, 1.5), which must trap · **✔ oracle pass**
```rust
static mut SLOTS: [f64; 4] = [0.0; 4];
/// No range check: an index of 4 or more panics.
#[unsafe(no_mangle)]
pub extern "C" fn write_slot_unchecked(i: u32, v: f64) -> u32 {
    let slots = unsafe { &mut *(&raw mut SLOTS) };
    slots[i as usize] = v;
    1
}
```

## Stamp the law version into the module: an exported law_version() and a #[unsafe(link_section)] custom section
**An exported law_version() -> u32 lets the host ask a live instance, and a byte-array static under #[unsafe(link_section = "si_law")] becomes a custom section the host can read with WebAssembly.Module.customSections before instantiating.**

*Check 1: a link_section byte-array static builds cleanly and law_version() answers 3* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · no warnings · imports nothing · node calls law_version() · **✔ oracle pass**
```rust
pub const LAW_VERSION: u32 = 3;
#[unsafe(link_section = "si_law")]
#[used]
static LAW_TAG: [u8; 9] = *b"si-law-v1";
#[unsafe(no_mangle)]
pub extern "C" fn law_version() -> u32 {
    LAW_VERSION
}
```
Expected output: `3`

*Check 2: on wasm a link_section static holding a reference is rejected* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “must be a simple list of bytes on the wasm target” · **✔ oracle pass**
```rust
#[unsafe(link_section = "si_law")]
#[used]
static LAW_TAG: &[u8] = b"si-law-v1";
#[unsafe(no_mangle)]
pub extern "C" fn law_version() -> u32 {
    3
}
```

*Check 3: edition 2024 rejects a bare #[link_section]* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “unsafe attribute used without unsafe” · **✔ oracle pass**
```rust
#[link_section = "si_law"]
#[used]
static LAW_TAG: [u8; 9] = *b"si-law-v1";
#[unsafe(no_mangle)]
pub extern "C" fn law_version() -> u32 {
    3
}
```

## Treat std on wasm32-unknown-unknown as stubs: files and threads return Unsupported, clocks trap
**On 1.98.1 a std cdylib imports nothing because every OS service is a stub that errors, does nothing, or panics (a trap), and the global allocator is dlmalloc built on memory.size / memory.grow.**

*Check 1: std::fs::read returns ErrorKind::Unsupported and the std module imports nothing* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · exports memory, fs_read_is_unsupported · imports nothing · node calls fs_read_is_unsupported() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn fs_read_is_unsupported() -> u32 {
    match std::fs::read("world.json") {
        Ok(_) => 0,
        Err(e) => (e.kind() == std::io::ErrorKind::Unsupported) as u32,
    }
}
```
Expected output: `1`

*Check 2: thread::Builder::spawn returns ErrorKind::Unsupported on this target* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls spawn_is_unsupported() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn spawn_is_unsupported() -> u32 {
    match std::thread::Builder::new().spawn(|| ()) {
        Ok(_) => 0,
        Err(e) => (e.kind() == std::io::ErrorKind::Unsupported) as u32,
    }
}
```
Expected output: `1`

*Check 3: the first 1-byte heap allocation grows linear memory by one page* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · node calls pages_grown_by_first_alloc() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn pages_grown_by_first_alloc() -> u32 {
    let before = core::arch::wasm32::memory_size::<0>();
    let b = Box::new(core::hint::black_box(1u8));
    core::hint::black_box(&b);
    (core::arch::wasm32::memory_size::<0>() - before) as u32
}
```
Expected output: `1`

*Check 4: std's link set on this target includes dlmalloc (shown in the linker line of a failed link)* · `compile_fail` · edition 2024 · wasm32-unknown-unknown · cdylib · stderr has “libdlmalloc” · **✔ oracle pass**
```rust
// An extern the host was supposed to provide, declared without #[link(wasm_import_module)].
unsafe extern "C" {
    fn host_log(x: f64);
}
#[unsafe(no_mangle)]
pub extern "C" fn add(a: f64, b: f64) -> f64 {
    unsafe { host_log(a) };
    a + b
}
```

