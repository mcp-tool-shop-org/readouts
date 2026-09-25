# Score ingest inside a wasm law: SMF, MusicXML, ABC
_Parsing score bytes with no files or clocks: midly, quick-xml, roxmltree, musicxml, abc-parser; one PPQ; canonical re-encoding._ · tier **si-jam-sessions** · wave 4 · 2026-09-25 · [‹ catalog index](README.md)

7 recipes · 6 verified · 7 compiler-checked.

| Recipe | Rust | Currency | ✓ | Code | What |
|--------|------|----------|---|------|------|
| Configure midly for wasm32-unknown-unknown | 1.98.1 | ✅ solid | ✓ | ✔ | Using midly with `default-features = false, features = ["alloc"]` enables `Smf::parse` whi |
| Map MusicXML divisions to fixed PPQ | 1.98.1 | ✅ solid | ✓ | ✔ | MusicXML's `<divisions>` element specifies ticks per quarter note. This must be mapped to  |
| Parse SMF formats and timing | 1.98.1 | ✅ solid | ✓ | ✔ | midly parses SMF formats 0, 1, and 2, exposing timing as either `Metrical` (ticks per beat |
| Process MusicXML backup and forward elements | 1.98.1 | ✅ solid | ✓ | ✔ | MusicXML uses `<backup>` and `<forward>` elements to move the time cursor backward and for |
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

- **Verifier (solid):** midly-0.5.3 Cargo.toml: default=[alloc,std,parallel]; parallel needs rayon. lib.rs: Smf unavailable w/o alloc. oracle-jam pins midly exactly as recipe recommends (default-features=false, features=[alloc]).
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

- **Verifier (solid):** divisions.rs doc matches claim verbatim; backup.rs confirms duration must not cross mid-measure divisions changes. Hand-verified check: (3*96)%2=0, (3*96)/2=144, matching expected stdout.
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

- **Verifier (solid):** primitive.rs: Format{SingleTrack=0,Parallel=1,Sequential=2}, Timing{Metrical(u15),Timecode(Fps,u8)}; smf.rs Header{format,timing}. Hand-traced check bytes: header timing=0x0060 gives Metrical(96), matching stdout.
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

### Handle midly parsing errors and strict mode
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1

**midly categorizes errors into `ErrorKind::Invalid` (fatal) and `ErrorKind::Malformed` (non-fatal unless the `strict` feature is enabled).**

- **How:** Check the `Error::kind()` returned by `Smf::parse`. Without the `strict` feature, midly silently drops malformed tracks or events. For a deterministic law, you must either enable `strict` or manually validate track counts.
- **Gotchas:** If `strict` is disabled, a corrupted file might parse successfully but yield missing data, which could lead to non-deterministic behavior if the corruption is interpreted differently by other tools.
- **In si-jam-sessions:** The law must reject ambiguous or corrupted inputs to ensure deterministic replay. Enabling the `strict` feature (or treating all `Result::Err` as fatal) is required.
- **Code checks** ([source](midi-notation-ingest.code.md#handle-midly-parsing-errors-and-strict-mode)):
  - *Check 1: midly returns Invalid for bad headers* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · deps: midly · jam dependency set · node calls is_invalid() · **✔ oracle pass**

- **Verifier (plausible):** error.rs confirms Invalid/Malformed split, Malformed only emitted under strict. engine_note wrongly treats 'Err-as-fatal' as a substitute for strict -- without it, Malformed never raises Err at all.
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

- **Verifier (plausible):** musicxml lib.rs confirms no_std path + read_score_data_partwise (ungated). But 'what' falsely calls quick-xml 0.42 no_std (no such feature exists); oracle-jam pins musicxml w/ default std-on features, not default-features=false.
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

- **Verifier (wrong):** README/datatypes confirm parsing + Length(f32). engine_note's '(length*base_ticks).round()==...' is impossible: Length has no Mul impl (E0369) and a private field (E0616) -- confirmed via compile-oracle counter-example.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [abc-parser 0.4.0 README.md](https://docs.rs/crate/abc-parser/0.4.0/source/README.md) (2026) — abc-parser parses ABC text into Rust data structures using PEG, but lacks support for Chord Symbols and Macros.
  - ✓ [abc-parser 0.4.0 src/datatypes/mod.rs](https://docs.rs/crate/abc-parser/0.4.0/source/src/datatypes/mod.rs) (2026) — Lengths are expressed as a newtype wrapper for f32 `Length(f32)`.

