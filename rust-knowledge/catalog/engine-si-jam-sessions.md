# si-jam-sessions notes — si-jam-sessions — Rust for a deterministic music law (P1)
Generated from `rust.db`. NEVER hand-edited. [‹ engine notes index](engine.md) · [catalog index](README.md)

## [Score ingest inside a wasm law: SMF, MusicXML, ABC](midi-notation-ingest.md)

- ✓ **Configure midly for wasm32-unknown-unknown** — Crucial for the wasm law, which has no threads (rayon would fail to compile or run) and operates in a `no_std` or restricted `std` environment.
- ✓ **Export SMPTE refusal and error-kind mapping from wasm32 strict cdylib** — Signed lock (si-jam-sessions docs/PHASE-0.md @ e3cc85e): the wasm32 cdylib export must parse SMF bytes with midly strict and return a u64 status code. SMPTE-timed files are refused with status 3. ErrorKind::Invalid maps to 1 and ErrorKind::Malformed maps to 2.
- ✓ **Handle midly parsing errors and strict mode** — The law must reject ambiguous or corrupted inputs to ensure deterministic replay. Enabling the `strict` feature (or treating all `Result::Err` as fatal) is required.
- ✓ **Map MusicXML divisions to fixed PPQ** — The law strictly uses one fixed PPQ. Any MusicXML file with tuplets or durations that do not align with this PPQ must be rejected to maintain deterministic integer state.
- · **Parse ABC notation with abc-parser** — Because ABC lengths are floats in this crate, the law must strictly verify that `(length * base_ticks).round() == (length * base_ticks)` to prevent floating-point non-determinism from leaking into the state.
- ✓ **Parse SMF formats and timing** — The law requires integer ticks at one fixed PPQ. If the SMF's metrical timing does not divide evenly into the law's PPQ, the file must be rejected to maintain deterministic integer math.
- ✓ **Process MusicXML backup and forward elements** — The law flattens all voices into a single integer timeline of onsets. Backup/forward are essential for resolving polyphony into this flat timeline.
- ✓ **Reject out-of-range MidiChannel meta-event under midly strict** — Signed lock (si-jam-sessions docs/PHASE-0.md @ e3cc85e): midly 0.5.3 strict must reject out-of-range integers. Map the resulting Malformed error to a refusal status code in the wasm export.
- ✓ **Reject track-count mismatch under midly strict** — Signed lock (si-jam-sessions docs/PHASE-0.md @ e3cc85e): midly 0.5.3 is built with default-features = false, features = ["alloc", "strict"]. Use Smf::parse in the ingest path; any Malformed error from strict mode must be mapped to a refusal code and returned across the wasm boundary, never panicked.
- ✓ **Reject truncated MTrk chunk under midly strict** — Signed lock (si-jam-sessions docs/PHASE-0.md @ e3cc85e): midly 0.5.3 strict must reject truncated chunks. Map the resulting Malformed error to a refusal status code in the wasm export.
- ✓ **Select a MusicXML parsing crate** — The law has no files, so it must ingest MusicXML from a byte slice in linear memory. `musicxml::read_score_data_partwise` fits this perfectly.

## [Integer musical time: ticks, tempo maps, samples](integer-time.md)

- ✓ **Bound the largest tick whose product with 16777215 and 48000 still fits in u128** — Signed lock: tick to sample is computed in u128 with checked_* and a refusal on None, and the release profile sets overflow-checks = true. Keep the product tick * tempo_us_per_quarter * 48000 on checked_mul; a musical take ends long before tick 422550225262032543670307476.
- ✓ **Calculate bar and beat from tick under SMF time signatures** — Bears on the integer tick timeline: the law must locate events in bars and beats for display and looping without floating point.
- ✓ **Carry division remainders across tempo segments** — Bears on the integer tempo map: crossing a tempo boundary must not lose fractional ticks between the score and the sample timeline.
- ✓ **Choose PPQ divisible by 3 and 5 for exact tuplets** — Bears on the fixed PPQ lock item: the chosen PPQ must be high enough and factorable so that common tuplets are exact integers.
- ✓ **Compute tick-to-microseconds with u128 intermediate and floor** — Bears on the likely second integer timeline in samples: the wasm cdylib must convert ticks to exact microseconds without floating point.
- ✓ **Compute tick-to-samples through tempo map with u128** — Bears on the likely separately pinned renderer: sample positions must be exact integers computed from the tempo map inside the wasm law.
- ✓ **Enable overflow-checks in release or rely on checked ops** — Bears on the deterministic replay and hash: silent wrap in release would desynchronise the score from the action log.
- ✓ **Exclude f64 seconds from the law time path** — Bears on the no-floating-point rule: the law’s state and time path must contain no f64 values.
- ✓ **Export the u128 tick-to-sample floor from a wasm32 cdylib that takes and returns u64** — Signed lock: edition 2024 cdylib for wasm32-unknown-unknown, raw extern "C" with #[unsafe(no_mangle)], every export argument and return at most 64 bits, status codes across the boundary and no panic. Compute the floor in u128 inside the export and return status 1 on None.
- ✓ **Match one floor of a multi-segment span by carrying the remainder while independent floors drift** — Signed lock: tick to sample = floor(tick * tempo_us_per_quarter * 48000 / (PPQ * 10^6)) in u128, with the remainder carried across tempo segments, checked_* and a refusal on None. Carry this unreduced remainder; do not add independent per-segment floors.
- ✓ **Print whole-tick 3:2, 5:4 and 7:4 durations from a whole note through a 128th at PPQ 3360** — Signed lock: the score is integer ticks at PPQ 3360 (2^5 * 3 * 5 * 7), with no floating point in the time path. Store that PPQ in Timing::Metrical and use these whole-tick 3:2, 5:4 and 7:4 lengths for onset and duration.
- ✓ **Refuse on overflow with checked arithmetic** — Bears on deterministic replay: an overflow must produce a defined refusal in the action log, not a wrap or trap.
- ✓ **Reserve Wrapping arithmetic for hash state only** — Bears on the state hash: the law hashes its state with wrapping arithmetic, but the musical timeline must never wrap.
- ✓ **Show every 7:4 tuplet from a whole note through a 128th is not a whole tick at PPQ 480, 960 and 3840** — Signed lock: integer ticks at PPQ 3360 and no f64 in the time path. Do not adopt PPQ 480, 960 or 3840 for the law; every 7:4 from a whole through a 128th is a fractional tick there. Refuse a metrical header whose PPQ is not 3360.
- ✓ **Use u128 intermediates on wasm32-unknown-unknown** — Bears on the wasm32-unknown-unknown cdylib target: u128 is available in core for exact integer time math.

## [Native audio and MIDI host](host-audio-and-midi.md)

- ✓ **Anchor midir microseconds to cpal StreamInstant and re-anchor for drift** — Bears on the integer sample clock; re-anchor the midir-to-cpal offset regularly because the two device clocks drift independently.
- ✓ **Build cpal output stream in f32 for highest real-time priority** — Bears on the oscillator output; request f32 format because cpal ranks it highest for real-time streams.
- ✓ **Count allocations across a simulated audio callback popping rtrb into an f32 buffer** — Bears on the signed lock pin: host audio callback must allocate nothing. Use this counting-allocator pattern to verify the callback body that pops committed events from an rtrb Consumer and writes them into the cpal output buffer.
- ✓ **Create rtrb RingBuffer before the stream because only RingBuffer::new allocates** — Bears on the signed lock pin: host audio callback must allocate nothing. Because rtrb 0.4.0 only allocates in RingBuffer::new, the ring must be created before the cpal stream starts.
- ✓ **Enumerate midir WinMM input ports by interface ID** — Bears on host setup; enumerate WinMM ports with MidiInput::ports() before opening the input used for admitted actions.
- ✓ **Handle cpal WASAPI xruns and device changes in error callback** — Bears on host reliability; route ErrorKind::Xrun and DeviceNotAvailable to the law's error log so replay can remain deterministic.
- ✓ **Interpret midir WinMM input timestamps as microseconds since start** — Bears on MIDI input ingestion; treat the u64 microseconds as relative to midiInStart and convert to the law's integer sample timeline.
- ✓ **Negative control: Vec push inside callback body increments allocator counter** — Bears on the signed lock pin: host audio callback must allocate nothing. This negative control demonstrates that the counting-allocator test is sensitive to allocations, ensuring a false negative is unlikely.
- ✓ **Register assert_no_alloc AllocDisabler around the callback body to catch debug allocations** — Bears on the signed lock pin: host audio callback must allocate nothing. Use assert_no_alloc as a second, independent guard around the callback body in debug builds.
- ✓ **Render oscillator voices from SPSC queue into cpal silence buffer** — Bears on the oscillator renderer; read committed events from the SPSC queue and write samples into cpal's pre-silenced buffer.
- ✓ **Request cpal BufferSize::Fixed on WASAPI shared-mode output** — Bears on the host audio output path; use BufferSize::Fixed to control latency when playing committed events through the oscillator.
- ✓ **Send events to audio callback via lock-free rtrb or ringbuf queue** — Bears on the host-to-callback event delivery; adopt a wait-free SPSC queue so the audio callback never blocks or allocates.
- ✓ **Use OutputCallbackInfo playback timestamp for latency alignment** — Bears on the host sample clock; use the playback instant to align the law's integer sample timeline with the audio device.
- ✓ **Wrap oscillator callback in assert_no_alloc with cpal equilibrium buffer** — Bears on the real-time guarantee; wrap the oscillator callback in assert_no_alloc to enforce zero allocation on the audio thread.

## [Crate licences for a shipped MIT/Apache product](crate-licences.md)

- ✓ **Add per-crate licence exceptions in cargo-deny** — Bears on CI/licence scanning; use exceptions to isolate non-global licences like BSD-1-Clause or Unlicense.
- ✓ **Clarify ambiguous crate licences with hashed file assertions** — Bears on CI/licence scanning; use clarify for crates with missing SPDX metadata.
- ✓ **Configure cargo-deny explicit allowlist for MIT/Apache products** — Bears on CI/licence scanning for both wasm and native targets; configure cargo-deny to enforce the product's MIT/Apache allowlist.
- ✓ **Enumerate native host-only Apache-2.0 and BSD-1-Clause dependencies** — Bears on the shipped native host binary; cpal and assert_no_alloc carry Apache-2.0 and BSD-1-Clause obligations respectively.
- ✓ **List permissive licences linked into the wasm32 law binary** — Bears on the shipped wasm32 law binary; verify that all linked crate licences are permissive and documented.
- ✓ **Plan for MPL-2.0 file-level copyleft if introduced later** — Bears on future dependency additions; an MPL-2.0 crate would trigger file-level copyleft obligations on its own files.
- ✓ **Preserve MIT copyright notices for abc-parser and midir** — Bears on attribution output for shipped binaries; MIT notices must be preserved in binary distributions.
- ✓ **Retain BSD-1-Clause copyright notice for assert_no_alloc source** — Bears on the shipped native host binary; assert_no_alloc is BSD-1-Clause and requires source redistribution to retain copyright.
- ✓ **Ship Apache-2.0 licence copy for cpal and reproduce NOTICE if present** — Bears on the shipped native host binary; cpal is Apache-2.0 and requires licence copy and NOTICE reproduction if present.
- ✓ **Treat midly as public domain under Unlicense** — Bears on the shipped wasm32 law binary; midly is public domain and requires no licence reproduction.

