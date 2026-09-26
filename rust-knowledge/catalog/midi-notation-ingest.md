# Score ingest inside a wasm law: SMF, MusicXML, ABC
_Parsing score bytes with no files or clocks: midly, quick-xml, roxmltree, musicxml, abc-parser; one PPQ; canonical re-encoding._ · tier **si-jam-sessions** · wave 5 · 2026-09-25 · [‹ catalog index](README.md)

11 recipes · 10 verified · 11 compiler-checked.

| Recipe | Rust | Currency | ✓ | Code | What |
|--------|------|----------|---|------|------|
| Configure midly for wasm32-unknown-unknown | 1.98.1 | ✅ solid | ✓ | ✔ | Using midly with `default-features = false, features = ["alloc"]` enables `Smf::parse` whi |
| Map MusicXML divisions to fixed PPQ | 1.98.1 | ✅ solid | ✓ | ✔ | MusicXML's `<divisions>` element specifies ticks per quarter note. This must be mapped to  |
| Parse SMF formats and timing | 1.98.1 | ✅ solid | ✓ | ✔ | midly parses SMF formats 0, 1, and 2, exposing timing as either `Metrical` (ticks per beat |
| Process MusicXML backup and forward elements | 1.98.1 | ✅ solid | ✓ | ✔ | MusicXML uses `<backup>` and `<forward>` elements to move the time cursor backward and for |
| Reject out-of-range MidiChannel meta-event under midly strict | midly 0.5.3 (alloc + strict), edition 2024 | ✅ solid | ✓ | ✔ | midly 0.5.3 strict rejects a MidiChannel meta-event (type 0x20) whose data byte exceeds 0x |
| Reject track-count mismatch under midly strict | midly 0.5.3 (alloc + strict), edition 2024 | ✅ solid | ✓ | ✔ | midly 0.5.3 strict rejects an SMF whose header track-count hint does not match the number  |
| Reject truncated MTrk chunk under midly strict | midly 0.5.3 (alloc + strict), edition 2024 | ✅ solid | ✓ | ✔ | midly 0.5.3 strict rejects an SMF whose MTrk chunk length exceeds the remaining file bytes |
| Export SMPTE refusal and error-kind mapping from wasm32 strict cdylib | midly 0.5.3 (alloc + strict), edition 2024, wasm32-unknown-unknown | ✗ wrong | ✓ | ✔ | midly 0.5.3 strict compiles and runs in a wasm32-unknown-unknown cdylib; a raw extern "C"  |
| Handle midly parsing errors and strict mode | 1.98.1 | ▸ plausible | ✓ | ✔ | midly categorizes errors into `ErrorKind::Invalid` (fatal) and `ErrorKind::Malformed` (non |
| Select a MusicXML parsing crate | 1.98.1 | ▸ plausible | ✓ | ✔ | quick-xml 0.42 provides a `no_std` pull parser, roxmltree 0.21 provides a read-only DOM (r |
| Parse ABC notation with abc-parser | 1.98.1 | ✗ wrong | · | ✔ | The `abc-parser` 0.4.0 crate parses ABC text into a `TuneBook` AST using PEG, supporting n |

## Detail

### Configure midly for wasm32-unknown-unknown
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1

**Using midly with `default-features = false, features = ["alloc"]` enables `Smf::parse` while avoiding `std` and `rayon` (parallel) dependencies.**

- **How:** In `Cargo.toml`, specify `midly = { version = "0.5.3", default-features = false, features = ["alloc"] }`. This provides the `Smf` type and allocation-backed parsing without requiring OS threads or the standard library.
- **Gotchas:** If `alloc` is omitted, `Smf::parse` is unavailable, and you must use the lower-level `parse` function which returns iterators.
- **In si-jam-sessions:** Crucial for the wasm law, which has no threads (rayon would fail to compile or run) and operates in a `no_std` or restricted `std` environment.
- **Code checks** ([source](midi-notation-ingest.code.md#configure-midly-for-wasm32-unknown-unknown)):
  - *Check 1: midly compiles with alloc and no default features* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** midly-0.5.3 Cargo.toml: default=[alloc,std,parallel]; parallel needs rayon. lib.rs: Smf unavailable w/o alloc. oracle-jam pins midly exactly as recipe recommends (default-features=false, features=[alloc]). · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 6 (midi-notation-ingest): midly 0.5.3 alloc + strict; SMPTE-timed files refused; MusicXML divisions to PPQ by integer maths; ABC durations as exact rationals. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 Cargo.toml](https://docs.rs/crate/midly/0.5.3/source/Cargo.toml) (2026) — The default features include `alloc`, `std`, and `parallel` (which depends on `rayon`).
  - ✓ [midly 0.5.3 src/lib.rs](https://docs.rs/crate/midly/0.5.3/source/src/lib.rs) (2026) — Disabling `std` and `alloc` makes the crate fully `no_std`, but `Smf` is unavailable without the `alloc` feature.

### Map MusicXML divisions to fixed PPQ
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1

**MusicXML's `<divisions>` element specifies ticks per quarter note. This must be mapped to the law's fixed PPQ using integer arithmetic.**

- **How:** Calculate `(note_duration * fixed_ppq) / divisions`. If `(note_duration * fixed_ppq) % divisions != 0`, the note's exact timing cannot be represented in the law's fixed PPQ and must be refused.
- **Gotchas:** Divisions can change mid-score in MusicXML. The mapping must use the currently active `<divisions>` value.
- **In si-jam-sessions:** The law strictly uses one fixed PPQ. Any MusicXML file with tuplets or durations that do not align with this PPQ must be rejected to maintain deterministic integer state.
- **Code checks** ([source](midi-notation-ingest.code.md#map-musicxml-divisions-to-fixed-ppq)):
  - *Check 1: Integer math for PPQ conversion* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · node calls convert_duration(3, 2, 96) · **✔ oracle pass**

- **Verifier (solid):** divisions.rs doc matches claim verbatim; backup.rs confirms duration must not cross mid-measure divisions changes. Hand-verified check: (3*96)%2=0, (3*96)/2=144, matching expected stdout. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 6 (midi-notation-ingest): midly 0.5.3 alloc + strict; SMPTE-timed files refused; MusicXML divisions to PPQ by integer maths; ABC durations as exact rationals. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [musicxml 1.1.2 src/elements/divisions.rs](https://docs.rs/crate/musicxml/1.1.2/source/src/elements/divisions.rs) (2026) — The Divisions element indicates how many divisions per quarter note are used to indicate a note's duration.
  - ✓ [musicxml 1.1.2 src/elements/backup.rs](https://docs.rs/crate/musicxml/1.1.2/source/src/elements/backup.rs) (2026) — Duration values should not cross mid-measure changes in the Divisions value.

### Parse SMF formats and timing
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1

**midly parses SMF formats 0, 1, and 2, exposing timing as either `Metrical` (ticks per beat) or `Timecode` (SMPTE frames).**

- **How:** Match on `smf.header.format` (`SingleTrack`, `Parallel`, `Sequential`) and `smf.header.timing`. For the law's fixed PPQ, reject `Timing::Timecode` and extract the `u15` ticks per beat from `Timing::Metrical`.
- **Gotchas:** Format 2 (Sequential) contains multiple independent songs; the law should likely reject it or only process the first track.
- **In si-jam-sessions:** The law requires integer ticks at one fixed PPQ. If the SMF's metrical timing does not divide evenly into the law's PPQ, the file must be rejected to maintain deterministic integer math.
- **Code checks** ([source](midi-notation-ingest.code.md#parse-smf-formats-and-timing)):
  - *Check 1: Extract metrical timing from SMF header* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam dependency set · node calls get_ppq() · **✔ oracle pass**

- **Verifier (solid):** primitive.rs: Format{SingleTrack=0,Parallel=1,Sequential=2}, Timing{Metrical(u15),Timecode(Fps,u8)}; smf.rs Header{format,timing}. Hand-traced check bytes: header timing=0x0060 gives Metrical(96), matching stdout. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 6 (midi-notation-ingest): midly 0.5.3 alloc + strict; SMPTE-timed files refused; MusicXML divisions to PPQ by integer maths; ABC durations as exact rationals. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.] · [operator 2026-09-25: LATER MEASUREMENT: rejecting Timing::Timecode after parsing misses one input. A division word starting 0x80 panics in Smf::parse with overflow checks on (midly 0.5.3 negates the byte as an i8). Refuse a timecode division word (bit 15 set) before calling midly (verification/measurements/2026-09-25-midly-timecode-0x80.json).]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 src/primitive.rs](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — Timing is an enum with `Metrical(u15)` and `Timecode(Fps, u8)` variants.
  - ✓ [midly 0.5.3 src/smf.rs](https://docs.rs/crate/midly/0.5.3/source/src/smf.rs) (2026) — The `Header` struct contains `format` and `timing` fields.

### Process MusicXML backup and forward elements
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1

**MusicXML uses `<backup>` and `<forward>` elements to move the time cursor backward and forward, coordinating multiple voices.**

- **How:** Maintain a running integer time cursor for the current measure. When encountering a `Forward` element, add its `duration.content.0` to the cursor. For a `Backup` element, subtract its duration.
- **Gotchas:** Backup and forward durations are in the current `<divisions>` units, so they must be converted to the law's fixed PPQ before adjusting the global integer timeline.
- **In si-jam-sessions:** The law flattens all voices into a single integer timeline of onsets. Backup/forward are essential for resolving polyphony into this flat timeline.
- **Code checks** ([source](midi-notation-ingest.code.md#process-musicxml-backup-and-forward-elements)):
  - *Check 1: Extract backup duration* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: musicxml · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** backup.rs/forward.rs confirm the coordinate-multiple-voices purpose. Field chain backup.content.duration.content.0 verified valid: Backup.content:BackupContents.duration:Duration.content:PositiveDivisions(pub u32).
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [musicxml 1.1.2 src/elements/backup.rs](https://docs.rs/crate/musicxml/1.1.2/source/src/elements/backup.rs) (2026) — The Backup element specifies the number of divisions to move back, coordinating multiple voices.
  - ✓ [musicxml 1.1.2 src/elements/forward.rs](https://docs.rs/crate/musicxml/1.1.2/source/src/elements/forward.rs) (2026) — The Forward element specifies the duration to move forward, generally used within voices and staves.

### Reject out-of-range MidiChannel meta-event under midly strict
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust midly 0.5.3 (alloc + strict), edition 2024

**midly 0.5.3 strict rejects a MidiChannel meta-event (type 0x20) whose data byte exceeds 0x0F, while alloc-only masks it to a valid u4.**

- **How:** Construct a single-track SMF containing the track event FF 20 01 FF. Under jam, u4::read masks 0xFF to 0x0F and Smf::parse returns Ok. Under jam-strict, u4::try_from fails and Smf::parse returns ErrorKind::Malformed.
- **Gotchas:** Without strict, midly applies a lossy mask to restricted integers. A parse success does not mean the file is standards-compliant.
- **In si-jam-sessions:** Signed lock (si-jam-sessions docs/PHASE-0.md @ e3cc85e): midly 0.5.3 strict must reject out-of-range integers. Map the resulting Malformed error to a refusal status code in the wasm export.
- **Code checks** ([source](midi-notation-ingest.code.md#reject-out-of-range-midichannel-meta-event-under-midly-strict)):
  - *Check 1: alloc-only accepts MidiChannel 0xFF meta-event* · `runs` · edition 2024 · host · bin · deps: midly · jam dependency set · **✔ oracle pass**
  - *Check 2: strict rejects MidiChannel 0xFF as Malformed* · `runs` · edition 2024 · host · bin · deps: midly · jam-strict dependency set · output has “malformed event” · **✔ oracle pass**

- **Verifier (solid):** CORRECTED: Check 0 only asserts res.is_ok(), not the 'how' claim that 0xFF masks to 0x0F. Verified independently: channel.as_int()==15 under jam - claim holds, but the check wouldn't catch a regression that stored a different masked channel value. · event.rs: MidiChannel reads via u4::read, confirmed verbatim. primitive.rs int_feature 'read' arm: strict uses try_from->Malformed. Check 1 confirms 'malformed event' after two context wraps; I confirmed non-strict masks 0xFF->15. · [operator 2026-09-25: LATER MEASUREMENT: cargo unifies features per command. If any workspace member enables midly/strict, --workspace (or no package flag at a virtual root) builds every member with strict; -p <member> keeps its own. Measure non-strict with -p or in its own workspace (verification/measurements/2026-09-25-cargo-feature-unification.json).]
- **Compiler:** 2/2 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 src/event.rs](https://docs.rs/crate/midly/0.5.3/source/src/event.rs) (2026) — MetaMessage::read reads a MidiChannel meta-event using u4::read on the data byte.
  - ✓ [midly 0.5.3 src/primitive.rs](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — The int_feature macro implements IntRead::read for restricted integers so that under strict, try_from is used and returns ErrorKind::Malformed if the raw value exceeds the allowed mask.

### Reject track-count mismatch under midly strict
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust midly 0.5.3 (alloc + strict), edition 2024

**midly 0.5.3 strict rejects an SMF whose header track-count hint does not match the number of MTrk chunks, while alloc-only accepts it.**

- **How:** Build an SMF with header format Parallel, track count 2, but supply only one EndOfTrack track. Parse with Smf::parse. Under jam the result is Ok; under jam-strict validate_smf returns ErrorKind::Malformed("file has a different amount of tracks than declared").
- **Gotchas:** Without strict, midly silently ignores the mismatch and returns the tracks it found. Do not assume header counts are validated unless strict is enabled.
- **In si-jam-sessions:** Signed lock (si-jam-sessions docs/PHASE-0.md @ e3cc85e): midly 0.5.3 is built with default-features = false, features = ["alloc", "strict"]. Use Smf::parse in the ingest path; any Malformed error from strict mode must be mapped to a refusal code and returned across the wasm boundary, never panicked.
- **Code checks** ([source](midi-notation-ingest.code.md#reject-track-count-mismatch-under-midly-strict)):
  - *Check 1: alloc-only accepts track-count mismatch* · `runs` · edition 2024 · host · bin · deps: midly · jam dependency set · **✔ oracle pass**
  - *Check 2: strict rejects track-count mismatch* · `runs` · edition 2024 · host · bin · deps: midly · jam-strict dependency set · output has “file has a different amount of tracks than declared” · **✔ oracle pass**

- **Verifier (solid):** validate_smf's message matches smf.rs verbatim. Oracle ran both checks: jam->Ok, jam-strict->Malformed with the exact quoted string. Confirmed live on docs.rs 0.5.3, byte-identical to the local registry copy. · [operator 2026-09-25: LATER MEASUREMENT: cargo unifies features per command. If any workspace member enables midly/strict, --workspace (or no package flag at a virtual root) builds every member with strict; -p <member> keeps its own. Measure non-strict with -p or in its own workspace (verification/measurements/2026-09-25-cargo-feature-unification.json).]
- **Compiler:** 2/2 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 src/smf.rs](https://docs.rs/crate/midly/0.5.3/source/src/smf.rs) (2026) — validate_smf under strict ensures track_count_hint equals the collected track count, returning err_malformed if they differ.
  - ✓ [midly 0.5.3 src/error.rs](https://docs.rs/crate/midly/0.5.3/source/src/error.rs) (2026) — ErrorKind::Malformed carries a static message describing non-fatal corruption detected when strict is enabled.

### Reject truncated MTrk chunk under midly strict
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust midly 0.5.3 (alloc + strict), edition 2024

**midly 0.5.3 strict rejects an SMF whose MTrk chunk length exceeds the remaining file bytes, while alloc-only silently uses the remainder.**

- **How:** Build a single-track SMF with an MTrk header declaring length 16 but only 2 bytes of data following. Under jam, Chunk::read uses the remainder and Smf::parse returns Ok with an empty track. Under jam-strict, Chunk::read returns err_malformed and Smf::parse fails.
- **Gotchas:** Non-strict silently truncates the chunk and may return an empty track or partial events. This hides file corruption.
- **In si-jam-sessions:** Signed lock (si-jam-sessions docs/PHASE-0.md @ e3cc85e): midly 0.5.3 strict must reject truncated chunks. Map the resulting Malformed error to a refusal status code in the wasm export.
- **Code checks** ([source](midi-notation-ingest.code.md#reject-truncated-mtrk-chunk-under-midly-strict)):
  - *Check 1: alloc-only accepts truncated MTrk chunk* · `runs` · edition 2024 · host · bin · deps: midly · jam dependency set · **✔ oracle pass**
  - *Check 2: strict rejects truncated MTrk chunk* · `runs` · edition 2024 · host · bin · deps: midly · jam-strict dependency set · output has “invalid chunk” · **✔ oracle pass**

- **Verifier (solid):** CORRECTED: Check 0 only asserts res.is_ok(), not the 'how' claim of an empty resulting track. Verified independently: parsing these bytes under jam gives tracks=1, tracks[0].len()=0 - claim holds, but the check wouldn't catch a regression that kept partial events. · Chunk::read (smf.rs) bails 'reached eof before chunk ended' under strict; TrackIter::next() re-wraps it as 'invalid chunk', which check 1 tests. I independently confirmed the non-strict path yields tracks=1, track0 len=0. · [operator 2026-09-25: LATER MEASUREMENT: cargo unifies features per command. If any workspace member enables midly/strict, --workspace (or no package flag at a virtual root) builds every member with strict; -p <member> keeps its own. Measure non-strict with -p or in its own workspace (verification/measurements/2026-09-25-cargo-feature-unification.json).]
- **Compiler:** 2/2 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 src/smf.rs](https://docs.rs/crate/midly/0.5.3/source/src/smf.rs) (2026) — In Chunk::read, when raw.split_checked(len as usize) returns None and the strict feature is enabled, the parser returns err_malformed with message "reached eof before chunk ended".
  - ✓ [midly 0.5.3 src/error.rs](https://docs.rs/crate/midly/0.5.3/source/src/error.rs) (2026) — ErrorKind::Malformed carries a static message describing non-fatal corruption detected by strict mode.

### Export SMPTE refusal and error-kind mapping from wasm32 strict cdylib
`✗ wrong` · ✓ verified · ✔ compiles as claimed · Rust midly 0.5.3 (alloc + strict), edition 2024, wasm32-unknown-unknown

**midly 0.5.3 strict compiles and runs in a wasm32-unknown-unknown cdylib; a raw extern "C" export reads SMF bytes and returns 0 for Ok, 1 for Invalid, 2 for Malformed, and 3 for SMPTE Timecode timing, without panicking.**

- **How:** Write a #![no_std] cdylib with a bump allocator and panic handler. Expose #[unsafe(no_mangle)] pub extern "C" fn ingest() -> u64. Match Smf::parse result: Ok with Timing::Timecode => 3, Ok otherwise => 0, Err with Invalid => 1, Err with Malformed => 2.
- **Gotchas:** wasm32-unknown-unknown has no default allocator; you must supply a #[global_allocator] and a #[panic_handler]. Keep the export panic-free and return only u64.
- **In si-jam-sessions:** Signed lock (si-jam-sessions docs/PHASE-0.md @ e3cc85e): the wasm32 cdylib export must parse SMF bytes with midly strict and return a u64 status code. SMPTE-timed files are refused with status 3. ErrorKind::Invalid maps to 1 and ErrorKind::Malformed maps to 2.
- **Code checks** ([source](midi-notation-ingest.code.md#export-smpte-refusal-and-error-kind-mapping-from-wasm32-strict-cdylib)):
  - *Check 1: wasm strict export returns 1 for Invalid* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam-strict dependency set · node calls ingest() · **✔ oracle pass**
  - *Check 2: wasm strict export returns 2 for Malformed* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam-strict dependency set · node calls ingest() · **✔ oracle pass**
  - *Check 3: wasm strict export returns 3 for SMPTE timing* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam-strict dependency set · node calls ingest() · **✔ oracle pass**

- **Verifier (wrong):** CORRECTED: FALSE AS WRITTEN: division high byte 0x80 makes Timing::read negate i8::MIN, panicking (primitive.rs:495) in strict and non-strict alike; the recipe's own wasm export hangs, not returns 1/2/3. Fix: inspect the raw division word's bit 15 and refuse as status 3 before calling Smf::parse. · Reproduced independently: byte 0x80 in the division field makes Timing::read (primitive.rs:495) negate i8::MIN and panic, in both strict and non-strict. The wasm ingest() export doesn't trap on it either - it hangs (20s timeout, no return). · [operator 2026-09-25: LATER MEASUREMENT: the recipe's `loop {}` panic handler never returns (the verifier's 0x80 run hung). These trap, so the host sees a RuntimeError: a handler calling core::arch::wasm32::unreachable(), or none, linking std unnamed (`extern crate std as _;`, panic=abort) (verification/measurements/2026-09-25-midly-timecode-0x80.json).]
- **Compiler:** 3/3 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 src/primitive.rs](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — Timing::read returns Timing::Timecode when bit 15 of the timing word is set, parsing fps and subframe from the lower bits.
  - ✓ [midly 0.5.3 src/error.rs](https://docs.rs/crate/midly/0.5.3/source/src/error.rs) (2026) — midly defines exactly two error kinds: ErrorKind::Invalid for fatal errors and ErrorKind::Malformed for non-fatal strict-mode errors.
  - ✓ [midly 0.5.3 src/lib.rs](https://docs.rs/crate/midly/0.5.3/source/src/lib.rs) (2026) — The strict feature causes the parser to reject uncompliant data, throwing errors of the kind ErrorKind::Malformed.

### Handle midly parsing errors and strict mode
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1

**midly categorizes errors into `ErrorKind::Invalid` (fatal) and `ErrorKind::Malformed` (non-fatal unless the `strict` feature is enabled).**

- **How:** Check the `Error::kind()` returned by `Smf::parse`. Without the `strict` feature, midly silently drops malformed tracks or events. For a deterministic law, you must either enable `strict` or manually validate track counts.
- **Gotchas:** If `strict` is disabled, a corrupted file might parse successfully but yield missing data, which could lead to non-deterministic behavior if the corruption is interpreted differently by other tools.
- **In si-jam-sessions:** The law must reject ambiguous or corrupted inputs to ensure deterministic replay. Enabling the `strict` feature (or treating all `Result::Err` as fatal) is required.
- **Code checks** ([source](midi-notation-ingest.code.md#handle-midly-parsing-errors-and-strict-mode)):
  - *Check 1: midly returns Invalid for bad headers* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam dependency set · node calls is_invalid() · **✔ oracle pass**

- **Verifier (plausible):** CORRECTED: engine_note equates 'strict' with 'treating all Result::Err as fatal'; not equivalent. Without strict, ErrorKind::Malformed is never emitted (midly silently drops bad tracks/events per lib.rs), so Err-as-fatal alone only catches Invalid, missing what strict guards against. · error.rs confirms Invalid/Malformed split, Malformed only emitted under strict. engine_note wrongly treats 'Err-as-fatal' as a substitute for strict -- without it, Malformed never raises Err at all. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 6 (midi-notation-ingest): midly 0.5.3 alloc + strict; SMPTE-timed files refused; MusicXML divisions to PPQ by integer maths; ABC durations as exact rationals. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 src/error.rs](https://docs.rs/crate/midly/0.5.3/source/src/error.rs) (2026) — ErrorKind has Invalid (fatal) and Malformed (non-fatal unless strict is enabled) variants.
  - ✓ [midly 0.5.3 src/lib.rs](https://docs.rs/crate/midly/0.5.3/source/src/lib.rs) (2026) — By default midly plows through non-standard files, but the strict feature makes it reject uncompliant data.

### Select a MusicXML parsing crate
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1

**quick-xml 0.42 provides a `no_std` pull parser, roxmltree 0.21 provides a read-only DOM (requires alloc/std), and musicxml 1.1.2 provides a typed SDK (supports `no_std`).**

- **How:** For a wasm32 law, `musicxml` with `default-features = false` provides a typed `ScorePartwise` struct directly from bytes via `read_score_data_partwise`. `quick-xml` is smaller but requires manual event handling.
- **Gotchas:** The `musicxml` crate's `read_score_partwise` function requires `std` (for file I/O), but `read_score_data_partwise` works on `Vec<u8>` in `no_std`.
- **In si-jam-sessions:** The law has no files, so it must ingest MusicXML from a byte slice in linear memory. `musicxml::read_score_data_partwise` fits this perfectly.
- **Code checks** ([source](midi-notation-ingest.code.md#select-a-musicxml-parsing-crate)):
  - *Check 1: musicxml parses data partwise* · `compiles` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: musicxml · jam dependency set · **✔ oracle pass**

- **Verifier (plausible):** CORRECTED: 'what' calls quick-xml 0.42 'a no_std pull parser' -- false: its Cargo.toml has no std/no_std/alloc feature (default=[]); lib.rs unconditionally does 'use std::borrow::Cow'. Also the check links musicxml with default (std-on) features, not the recipe's own recommended default-features=false. · musicxml lib.rs confirms no_std path + read_score_data_partwise (ungated). But 'what' falsely calls quick-xml 0.42 no_std (no such feature exists); oracle-jam pins musicxml w/ default std-on features, not default-features=false.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [musicxml 1.1.2 src/lib.rs](https://docs.rs/crate/musicxml/1.1.2/source/src/lib.rs) (2026) — In a no_std environment, you can parse MusicXML data directly by calling read_score_data_partwise with a Vec<u8>.
  - ✓ [quick-xml 0.42.0 src/lib.rs](https://docs.rs/crate/quick-xml/0.42.0/source/src/lib.rs) (2026) — quick-xml is a low level XML pull-reader where buffer allocation/clearing is left to user.

### Parse ABC notation with abc-parser
`✗ wrong` · · not verified · ✔ compiles as claimed · Rust 1.98.1

**The `abc-parser` 0.4.0 crate parses ABC text into a `TuneBook` AST using PEG, supporting notes, tuplets, and repeats, but lacks chord symbols and macros.**

- **How:** Call `abc_parser::abc::tune_book(text)` to get a `TuneBook`. Iterate over `tunes`, then `body.lines`, matching on `TuneLine::Music` to extract `MusicSymbol::Note`.
- **Gotchas:** ABC lengths are expressed as `f32` (e.g., `Length(0.5)`). These floats must be converted to exact integer ticks at the fixed PPQ, rejecting any that lose precision.
- **In si-jam-sessions:** Because ABC lengths are floats in this crate, the law must strictly verify that `(length * base_ticks).round() == (length * base_ticks)` to prevent floating-point non-determinism from leaking into the state.
- **Code checks** ([source](midi-notation-ingest.code.md#parse-abc-notation-with-abc-parser)):
  - *Check 1: Parse ABC tune book* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: abc_parser · jam dependency set · node calls parse_abc() · **✔ oracle pass**

- **Verifier (wrong):** README/datatypes confirm parsing + Length(f32). engine_note's '(length*base_ticks).round()==...' is impossible: Length has no Mul impl (E0369) and a private field (E0616) -- confirmed via compile-oracle counter-example. · [operator 2026-09-25: CONSUMED AS A REFUSAL: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 6 (midi-notation-ingest) takes this recipe's refuted guard as its evidence that abc-parser 0.4.0 keeps durations as f32, and parses ABC durations as exact rationals instead. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [abc-parser 0.4.0 README.md](https://docs.rs/crate/abc-parser/0.4.0/source/README.md) (2026) — abc-parser parses ABC text into Rust data structures using PEG, but lacks support for Chord Symbols and Macros.
  - ✓ [abc-parser 0.4.0 src/datatypes/mod.rs](https://docs.rs/crate/abc-parser/0.4.0/source/src/datatypes/mod.rs) (2026) — Lengths are expressed as a newtype wrapper for f32 `Length(f32)`.

