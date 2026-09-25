# Score ingest inside a wasm law: SMF, MusicXML, ABC — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](midi-notation-ingest.md) · [catalog index](README.md)

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

