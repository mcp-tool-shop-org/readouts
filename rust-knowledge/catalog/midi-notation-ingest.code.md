# Score ingest inside a wasm law: SMF, MusicXML, ABC — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](midi-notation-ingest.md) · [catalog index](README.md)

## Configure midly for wasm32-unknown-unknown
**Using midly with `default-features = false, features = ["alloc"]` enables `Smf::parse` while avoiding `std` and `rayon` (parallel) dependencies.**

*Check 1: midly compiles with alloc and no default features* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam dependency set · **✔ oracle pass**
```rust
use midly::Smf;
#[unsafe(no_mangle)]
pub extern "C" fn check_midly() {
    let _ = Smf::parse(b"MThd\0\0\0\x06\0\0\0\x01\0\x60MTrk\0\0\0\x04\0\xff\x2f\0");
}
```

## Map MusicXML divisions to fixed PPQ
**MusicXML's `<divisions>` element specifies ticks per quarter note. This must be mapped to the law's fixed PPQ using integer arithmetic.**

*Check 1: Integer math for PPQ conversion* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · node calls convert_duration(3, 2, 96) · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn convert_duration(duration: u32, divisions: u32, fixed_ppq: u32) -> i32 {
    if (duration * fixed_ppq) % divisions != 0 {
        -1
    } else {
        ((duration * fixed_ppq) / divisions) as i32
    }
}
```
Expected output: `144`

## Parse SMF formats and timing
**midly parses SMF formats 0, 1, and 2, exposing timing as either `Metrical` (ticks per beat) or `Timecode` (SMPTE frames).**

*Check 1: Extract metrical timing from SMF header* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam dependency set · node calls get_ppq() · **✔ oracle pass**
```rust
use midly::{Smf, Timing};
#[unsafe(no_mangle)]
pub extern "C" fn get_ppq() -> i32 {
    let smf = Smf::parse(b"MThd\0\0\0\x06\0\0\0\x01\0\x60MTrk\0\0\0\x04\0\xff\x2f\0").unwrap();
    match smf.header.timing {
        Timing::Metrical(ticks) => ticks.as_int() as i32,
        _ => -1,
    }
}
```
Expected output: `96`

## Process MusicXML backup and forward elements
**MusicXML uses `<backup>` and `<forward>` elements to move the time cursor backward and forward, coordinating multiple voices.**

*Check 1: Extract backup duration* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: musicxml · jam dependency set · **✔ oracle pass**
```rust
use musicxml::elements::Backup;
#[unsafe(no_mangle)]
pub extern "C" fn get_backup_dur(backup: &Backup) -> u32 {
    backup.content.duration.content.0
}
```

## Reject out-of-range MidiChannel meta-event under midly strict
**midly 0.5.3 strict rejects a MidiChannel meta-event (type 0x20) whose data byte exceeds 0x0F, while alloc-only masks it to a valid u4.**

*Check 1: alloc-only accepts MidiChannel 0xFF meta-event* · `runs` · edition 2024 · host · bin · deps: midly · jam dependency set · **✔ oracle pass**
```rust
fn main() {
    let bytes: [u8; 27] = [
        0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x60,
        0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x05,
        0x00, 0xFF, 0x20, 0x01, 0xFF,
    ];
    let res = midly::Smf::parse(&bytes);
    assert!(res.is_ok(), "expected ok, got {:?}", res);
    println!("ok");
}
```
Expected output: `ok`

*Check 2: strict rejects MidiChannel 0xFF as Malformed* · `runs` · edition 2024 · host · bin · deps: midly · jam-strict dependency set · output has “malformed event” · **✔ oracle pass**
```rust
fn main() {
    let bytes: [u8; 27] = [
        0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x60,
        0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x05,
        0x00, 0xFF, 0x20, 0x01, 0xFF,
    ];
    let res = midly::Smf::parse(&bytes);
    assert!(res.is_err(), "expected err");
    let kind = res.unwrap_err().kind();
    assert!(matches!(kind, midly::ErrorKind::Malformed(_)), "expected Malformed, got {}", kind);
    println!("{}", kind);
}
```

## Reject track-count mismatch under midly strict
**midly 0.5.3 strict rejects an SMF whose header track-count hint does not match the number of MTrk chunks, while alloc-only accepts it.**

*Check 1: alloc-only accepts track-count mismatch* · `runs` · edition 2024 · host · bin · deps: midly · jam dependency set · **✔ oracle pass**
```rust
fn main() {
    let bytes: [u8; 26] = [
        0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06,
        0x00, 0x01, 0x00, 0x02, 0x00, 0x60,
        0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x04,
        0x00, 0xFF, 0x2F, 0x00,
    ];
    let res = midly::Smf::parse(&bytes);
    assert!(res.is_ok(), "expected ok, got {:?}", res);
    println!("ok");
}
```
Expected output: `ok`

*Check 2: strict rejects track-count mismatch* · `runs` · edition 2024 · host · bin · deps: midly · jam-strict dependency set · output has “file has a different amount of tracks than declared” · **✔ oracle pass**
```rust
fn main() {
    let bytes: [u8; 26] = [
        0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06,
        0x00, 0x01, 0x00, 0x02, 0x00, 0x60,
        0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x04,
        0x00, 0xFF, 0x2F, 0x00,
    ];
    let res = midly::Smf::parse(&bytes);
    assert!(res.is_err(), "expected err");
    let kind = res.unwrap_err().kind();
    assert!(matches!(kind, midly::ErrorKind::Malformed(_)), "expected Malformed, got {}", kind);
    println!("{}", kind);
}
```

## Reject truncated MTrk chunk under midly strict
**midly 0.5.3 strict rejects an SMF whose MTrk chunk length exceeds the remaining file bytes, while alloc-only silently uses the remainder.**

*Check 1: alloc-only accepts truncated MTrk chunk* · `runs` · edition 2024 · host · bin · deps: midly · jam dependency set · **✔ oracle pass**
```rust
fn main() {
    let bytes: [u8; 24] = [
        0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x60,
        0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x10,
        0x00, 0xFF,
    ];
    let res = midly::Smf::parse(&bytes);
    assert!(res.is_ok(), "expected ok, got {:?}", res);
    println!("ok");
}
```
Expected output: `ok`

*Check 2: strict rejects truncated MTrk chunk* · `runs` · edition 2024 · host · bin · deps: midly · jam-strict dependency set · output has “invalid chunk” · **✔ oracle pass**
```rust
fn main() {
    let bytes: [u8; 24] = [
        0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x60,
        0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x10,
        0x00, 0xFF,
    ];
    let res = midly::Smf::parse(&bytes);
    assert!(res.is_err(), "expected err");
    let kind = res.unwrap_err().kind();
    assert!(matches!(kind, midly::ErrorKind::Malformed(_)), "expected Malformed, got {}", kind);
    println!("{}", kind);
}
```

## Export SMPTE refusal and error-kind mapping from wasm32 strict cdylib
**midly 0.5.3 strict compiles and runs in a wasm32-unknown-unknown cdylib; a raw extern "C" export reads SMF bytes and returns 0 for Ok, 1 for Invalid, 2 for Malformed, and 3 for SMPTE Timecode timing, without panicking.**

*Check 1: wasm strict export returns 1 for Invalid* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam-strict dependency set · node calls ingest() · **✔ oracle pass**
```rust
#![no_std]
extern crate alloc;
use core::alloc::{GlobalAlloc, Layout};
use core::cell::UnsafeCell;
use core::sync::atomic::{AtomicUsize, Ordering};
const HEAP_SIZE: usize = 65536;
struct SyncUnsafeCell<T>(UnsafeCell<T>);
unsafe impl<T> Sync for SyncUnsafeCell<T> {}
static HEAP: SyncUnsafeCell<[u8; HEAP_SIZE]> = SyncUnsafeCell(UnsafeCell::new([0; HEAP_SIZE]));
static NEXT: AtomicUsize = AtomicUsize::new(0);
struct BumpAlloc;
unsafe impl GlobalAlloc for BumpAlloc {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        let align = layout.align();
        let size = (layout.size() + align - 1) & !(align - 1);
        let start = NEXT.fetch_add(size, Ordering::SeqCst);
        if start + size > HEAP_SIZE { core::ptr::null_mut() } else { unsafe { (HEAP.0.get() as *mut u8).add(start) } }
    }
    unsafe fn dealloc(&self, _ptr: *mut u8, _layout: Layout) {}
}
#[global_allocator]
static ALLOC: BumpAlloc = BumpAlloc;
#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! { loop {} }
static SMF: [u8; 4] = [0x00, 0x00, 0x00, 0x00];
#[unsafe(no_mangle)]
pub extern "C" fn ingest() -> u64 {
    match midly::Smf::parse(&SMF) {
        Ok(_) => 0,
        Err(e) => match e.kind() {
            midly::ErrorKind::Invalid(_) => 1,
            midly::ErrorKind::Malformed(_) => 2,
        },
    }
}
```
Expected output: `1`

*Check 2: wasm strict export returns 2 for Malformed* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam-strict dependency set · node calls ingest() · **✔ oracle pass**
```rust
#![no_std]
extern crate alloc;
use core::alloc::{GlobalAlloc, Layout};
use core::cell::UnsafeCell;
use core::sync::atomic::{AtomicUsize, Ordering};
const HEAP_SIZE: usize = 65536;
struct SyncUnsafeCell<T>(UnsafeCell<T>);
unsafe impl<T> Sync for SyncUnsafeCell<T> {}
static HEAP: SyncUnsafeCell<[u8; HEAP_SIZE]> = SyncUnsafeCell(UnsafeCell::new([0; HEAP_SIZE]));
static NEXT: AtomicUsize = AtomicUsize::new(0);
struct BumpAlloc;
unsafe impl GlobalAlloc for BumpAlloc {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        let align = layout.align();
        let size = (layout.size() + align - 1) & !(align - 1);
        let start = NEXT.fetch_add(size, Ordering::SeqCst);
        if start + size > HEAP_SIZE { core::ptr::null_mut() } else { unsafe { (HEAP.0.get() as *mut u8).add(start) } }
    }
    unsafe fn dealloc(&self, _ptr: *mut u8, _layout: Layout) {}
}
#[global_allocator]
static ALLOC: BumpAlloc = BumpAlloc;
#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! { loop {} }
static SMF: [u8; 27] = [
    0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06,
    0x00, 0x00, 0x00, 0x01, 0x00, 0x60,
    0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x05,
    0x00, 0xFF, 0x20, 0x01, 0xFF,
];
#[unsafe(no_mangle)]
pub extern "C" fn ingest() -> u64 {
    match midly::Smf::parse(&SMF) {
        Ok(_) => 0,
        Err(e) => match e.kind() {
            midly::ErrorKind::Invalid(_) => 1,
            midly::ErrorKind::Malformed(_) => 2,
        },
    }
}
```
Expected output: `2`

*Check 3: wasm strict export returns 3 for SMPTE timing* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam-strict dependency set · node calls ingest() · **✔ oracle pass**
```rust
#![no_std]
extern crate alloc;
use core::alloc::{GlobalAlloc, Layout};
use core::cell::UnsafeCell;
use core::sync::atomic::{AtomicUsize, Ordering};
const HEAP_SIZE: usize = 65536;
struct SyncUnsafeCell<T>(UnsafeCell<T>);
unsafe impl<T> Sync for SyncUnsafeCell<T> {}
static HEAP: SyncUnsafeCell<[u8; HEAP_SIZE]> = SyncUnsafeCell(UnsafeCell::new([0; HEAP_SIZE]));
static NEXT: AtomicUsize = AtomicUsize::new(0);
struct BumpAlloc;
unsafe impl GlobalAlloc for BumpAlloc {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        let align = layout.align();
        let size = (layout.size() + align - 1) & !(align - 1);
        let start = NEXT.fetch_add(size, Ordering::SeqCst);
        if start + size > HEAP_SIZE { core::ptr::null_mut() } else { unsafe { (HEAP.0.get() as *mut u8).add(start) } }
    }
    unsafe fn dealloc(&self, _ptr: *mut u8, _layout: Layout) {}
}
#[global_allocator]
static ALLOC: BumpAlloc = BumpAlloc;
#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! { loop {} }
static SMF: [u8; 26] = [
    0x4D, 0x54, 0x68, 0x64, 0x00, 0x00, 0x00, 0x06,
    0x00, 0x00, 0x00, 0x01, 0xE8, 0x00,
    0x4D, 0x54, 0x72, 0x6B, 0x00, 0x00, 0x00, 0x04,
    0x00, 0xFF, 0x2F, 0x00,
];
#[unsafe(no_mangle)]
pub extern "C" fn ingest() -> u64 {
    match midly::Smf::parse(&SMF) {
        Ok(smf) => if matches!(smf.header.timing, midly::Timing::Timecode(_, _)) { 3 } else { 0 },
        Err(e) => match e.kind() {
            midly::ErrorKind::Invalid(_) => 1,
            midly::ErrorKind::Malformed(_) => 2,
        },
    }
}
```
Expected output: `3`

## Handle midly parsing errors and strict mode
**midly categorizes errors into `ErrorKind::Invalid` (fatal) and `ErrorKind::Malformed` (non-fatal unless the `strict` feature is enabled).**

*Check 1: midly returns Invalid for bad headers* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam dependency set · node calls is_invalid() · **✔ oracle pass**
```rust
use midly::{Smf, ErrorKind};
#[unsafe(no_mangle)]
pub extern "C" fn is_invalid() -> i32 {
    let res = Smf::parse(b"BADHEADER");
    match res {
        Err(e) => match e.kind() {
            ErrorKind::Invalid(_) => 1,
            _ => 0,
        },
        Ok(_) => 0,
    }
}
```
Expected output: `1`

## Select a MusicXML parsing crate
**quick-xml 0.42 provides a `no_std` pull parser, roxmltree 0.21 provides a read-only DOM (requires alloc/std), and musicxml 1.1.2 provides a typed SDK (supports `no_std`).**

*Check 1: musicxml parses data partwise* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: musicxml · jam dependency set · **✔ oracle pass**
```rust
use musicxml::read_score_data_partwise;
#[unsafe(no_mangle)]
pub extern "C" fn parse_mxml(ptr: *const u8, len: usize) -> i32 {
    let data = unsafe { std::slice::from_raw_parts(ptr, len) }.to_vec();
    match read_score_data_partwise(data) {
        Ok(_) => 1,
        Err(_) => 0,
    }
}
```

## Parse ABC notation with abc-parser
**The `abc-parser` 0.4.0 crate parses ABC text into a `TuneBook` AST using PEG, supporting notes, tuplets, and repeats, but lacks chord symbols and macros.**

*Check 1: Parse ABC tune book* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: abc_parser · jam dependency set · node calls parse_abc() · **✔ oracle pass**
```rust
use abc_parser::abc;
#[unsafe(no_mangle)]
pub extern "C" fn parse_abc() -> i32 {
    let parsed = abc::tune_book("X:1\nT:Example\nK:D\n");
    if parsed.is_ok() { 1 } else { 0 }
}
```
Expected output: `1`

