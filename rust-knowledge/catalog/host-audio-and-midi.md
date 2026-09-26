# Native audio and MIDI host
_cpal output on WASAPI, lock-free event delivery to the audio callback, midir input timestamps mapped onto the law clock._ · tier **si-jam-sessions** · wave 5 · 2026-09-25 · [‹ catalog index](README.md)

14 recipes · 14 verified · 14 compiler-checked.

| Recipe | Rust | Currency | ✓ | Code | What |
|--------|------|----------|---|------|------|
| Anchor midir microseconds to cpal StreamInstant and re-anchor for drift | midir 0.11.0, cpal 0.18.2 | ✅ solid | ✓ | ✔ | Because midir timestamps and cpal StreamInstant come from independent clocks, the host mus |
| Build cpal output stream in f32 for highest real-time priority | cpal 0.18.2 | ✅ solid | ✓ | ✔ | cpal ranks F32 highest in its default-format heuristic because it is the universal real-ti |
| Count allocations across a simulated audio callback popping rtrb into an f32 buffer | 1.98.1, edition 2024, rtrb 0.4.0 | ✅ solid | ✓ | ✔ | A counting #[global_allocator] records zero new allocations during a simulated callback th |
| Create rtrb RingBuffer before the stream because only RingBuffer::new allocates | 1.98.1, edition 2024, rtrb 0.4.0 | ✅ solid | ✓ | ✔ | rtrb 0.4.0 allocates its backing buffer in RingBuffer::new, not during push or pop, so the |
| Interpret midir WinMM input timestamps as microseconds since start | midir 0.11.0 | ✅ solid | ✓ | ✔ | midir’s WinMM backend delivers input callback timestamps in microseconds, converted from t |
| Negative control: Vec push inside callback body increments allocator counter | 1.98.1, edition 2024 | ✅ solid | ✓ | ✔ | A Vec::push inside the same simulated callback body increments the counting allocator, con |
| Register assert_no_alloc AllocDisabler around the callback body to catch debug allocations | 1.98.1, edition 2024, rtrb 0.4.0, assert_no_alloc 1.1.2 | ✅ solid | ✓ | ✔ | With AllocDisabler registered as #[global_allocator], assert_no_alloc aborts in debug if t |
| Render oscillator voices from SPSC queue into cpal silence buffer | cpal 0.18.2, rtrb 0.4.0 | ✅ solid | ✓ | ✔ | The cpal output callback buffer is pre-filled with silence, and the callback can pop commi |
| Request cpal BufferSize::Fixed on WASAPI shared-mode output | cpal 0.18.2 | ✅ solid | ✓ | ✔ | cpal’s WASAPI backend always creates shared-mode streams, and BufferSize::Fixed only reque |
| Use OutputCallbackInfo playback timestamp for latency alignment | cpal 0.18.2 | ✅ solid | ✓ | ✔ | cpal output callbacks receive an OutputCallbackInfo whose timestamp contains a callback in |
| Enumerate midir WinMM input ports by interface ID | midir 0.11.0 | ▸ plausible | ✓ | ✔ | MidiInput::ports returns a vector of MidiInputPort values on Windows via the WinMM midiInG |
| Handle cpal WASAPI xruns and device changes in error callback | cpal 0.18.2 | ✗ wrong | ✓ | ✔ | The cpal WASAPI backend forwards discontinuities as ErrorKind::Xrun and device removals as |
| Send events to audio callback via lock-free rtrb or ringbuf queue | rtrb 0.4.0, ringbuf 0.5.2 | ▸ plausible | ✓ | ✔ | Both rtrb and ringbuf provide single-producer single-consumer queues that are lock-free an |
| Wrap oscillator callback in assert_no_alloc with cpal equilibrium buffer | assert_no_alloc 1.1.2, cpal 0.18.2 | ▸ plausible | ✓ | ✔ | assert_no_alloc aborts or warns if the audio callback allocates, and cpal pre-fills the ou |

## Detail

### Anchor midir microseconds to cpal StreamInstant and re-anchor for drift
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust midir 0.11.0, cpal 0.18.2

**Because midir timestamps and cpal StreamInstant come from independent clocks, the host must establish an anchor and re-anchor periodically to keep the law’s sample clock aligned.**

- **How:** At stream start (or first MIDI event), record both the midir microseconds value and cpal’s StreamInstant (or frames_written). For each subsequent MIDI event, compute delta_us = midi_timestamp - anchor_midi, then convert to samples with delta_us * sample_rate / 1_000_000. Re-sample both clocks every few seconds to correct drift.
- **Gotchas:** Integer division when converting microseconds to samples truncates; accumulate remainders to avoid systematic timing drift. Re-anchor at least every few seconds.
- **In si-jam-sessions:** Bears on the integer sample clock; re-anchor the midir-to-cpal offset regularly because the two device clocks drift independently.
- **Code checks** ([source](host-audio-and-midi.code.md#anchor-midir-microseconds-to-cpal-streaminstant-and-re-anchor-for-drift)):
  - *Check 1: midir timestamp and cpal StreamInstant types can be combined* · `compiles` · edition 2024 · host · bin · deps: cpal, midir · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** handler.rs confirms the ms*1000 conversion; timestamp.rs table confirms WASAPI/QueryPerformanceCounter(). Check's delta_us/sample arithmetic matches 'how' exactly and type-checks (StreamInstant::ZERO exists). · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 7 (host-audio-and-midi): cpal 0.18.2 WASAPI shared mode, input-only xrun reports; rtrb SPSC; no allocation on the callback; WinMM 1 ms, clocks anchored. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midir 0.11.0 src/backend/winmm/handler.rs](https://docs.rs/crate/midir/0.11.0/source/src/backend/winmm/handler.rs) (2026) — WinMM timestamps are in milliseconds beginning at zero when midiInStart was called, and midir multiplies by 1000 to produce microseconds.
  - ✓ [cpal 0.18.2 src/timestamp.rs](https://docs.rs/crate/cpal/0.18.2/source/src/timestamp.rs) (2026) — On WASAPI, StreamInstant uses QueryPerformanceCounter() as its time source.

### Build cpal output stream in f32 for highest real-time priority
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust cpal 0.18.2

**cpal ranks F32 highest in its default-format heuristic because it is the universal real-time audio format, and build_output_stream::<f32> selects compile-time sample processing.**

- **How:** When building the output stream, use build_output_stream::<f32, _, _> so the callback receives &mut [f32]. If the device default is not F32, cpal may insert a converter in shared mode, but F32 is still the preferred real-time choice.
- **Gotchas:** Not all devices support f32 natively; cpal may insert a format converter in shared mode. Query supported_output_configs() if bit-exact output is required.
- **In si-jam-sessions:** Bears on the oscillator output; request f32 format because cpal ranks it highest for real-time streams.
- **Code checks** ([source](host-audio-and-midi.code.md#build-cpal-output-stream-in-f32-for-highest-real-time-priority)):
  - *Check 1: cpal F32 output stream compiles* · `compiles` · edition 2024 · host · bin · deps: cpal · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** lib.rs cmp_default_heuristics doc says 'F32 is ranked highest as the universal realtime audio format' verbatim; format_rank() gives F32=>14, the max. AUDCLNT_STREAMFLAGS_AUTOCONVERTPCM in device.rs backs the converter gotcha.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [cpal 0.18.2 src/lib.rs](https://docs.rs/crate/cpal/0.18.2/source/src/lib.rs) (2026) — In cmp_default_heuristics, SampleFormat::F32 is ranked highest as the universal realtime audio format.
  - ✓ [cpal 0.18.2 src/traits.rs](https://docs.rs/crate/cpal/0.18.2/source/src/traits.rs) (2026) — build_output_stream::<f32> creates an output stream with compile-time sample type f32.

### Count allocations across a simulated audio callback popping rtrb into an f32 buffer
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024, rtrb 0.4.0

**A counting #[global_allocator] records zero new allocations during a simulated callback that pops from an rtrb Consumer into a stack f32 buffer.**

- **How:** Implement GlobalAlloc by forwarding to System and incrementing an AtomicUsize in alloc. Create the RingBuffer and pre-fill events before resetting the counter. In the callback body, pop from the Consumer into a fixed [f32; N] on the stack. Compare the counter before and after; it must be identical.
- **Gotchas:** Do not measure RingBuffer::new itself; it allocates. Do not use Mutex or Vec inside the GlobalAlloc impl or measuring will recurse or allocate. Reset the counter after setup but before the callback body.
- **In si-jam-sessions:** Bears on the signed lock pin: host audio callback must allocate nothing. Use this counting-allocator pattern to verify the callback body that pops committed events from an rtrb Consumer and writes them into the cpal output buffer.
- **Code checks** ([source](host-audio-and-midi.code.md#count-allocations-across-a-simulated-audio-callback-popping-rtrb-into-an-f32-buffer)):
  - *Check 1: Counting allocator shows zero allocs in simulated callback body* · `runs` · edition 2024 · host · bin · deps: rtrb · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** Ran the exact check via compile_oracle (rustc 1.98.1, jam set): printed alloc_count=0 as claimed. rtrb 0.4.0's pop()/push() (src/lib.rs) use only atomics and raw-pointer ops -- no alloc call sites exist.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [GlobalAlloc in std::alloc - Rust](https://doc.rust-lang.org/stable/std/alloc/trait.GlobalAlloc.html) (2026) — A memory allocator can be registered as the standard library’s default through the #[global_allocator] attribute, and the alloc method is called for each heap allocation.
  - ✓ [rtrb 0.4.0 src/lib.rs](https://docs.rs/crate/rtrb/0.4.0/source/src/lib.rs) (2026) — A fixed-capacity buffer is allocated on construction. After that, no more memory is allocated (unless the type T does that internally).

### Create rtrb RingBuffer before the stream because only RingBuffer::new allocates
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024, rtrb 0.4.0

**rtrb 0.4.0 allocates its backing buffer in RingBuffer::new, not during push or pop, so the ring must be created before the stream starts.**

- **How:** Call RingBuffer::new(capacity) during setup, before the cpal stream is built. Pass only the Producer to the non-real-time thread and the Consumer into the callback. Never construct or resize the ring inside the callback.
- **Gotchas:** RingBuffer::new may perform multiple backing allocations; the check only asserts the total is non-zero. Do not call new, grow, or shrink in the callback. The capacity is fixed and must be chosen at setup time.
- **In si-jam-sessions:** Bears on the signed lock pin: host audio callback must allocate nothing. Because rtrb 0.4.0 only allocates in RingBuffer::new, the ring must be created before the cpal stream starts.
- **Code checks** ([source](host-audio-and-midi.code.md#create-rtrb-ringbuffer-before-the-stream-because-only-ringbuffernew-allocates)):
  - *Check 1: RingBuffer::new allocates but push and pop do not* · `runs` · edition 2024 · host · bin · deps: rtrb · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** Ran the exact check: printed 'new_allocates ops_do_not'. Source: RingBuffer::new does Vec::with_capacity + Box::new (2 allocs, confirmed via arc_ring_buffer.rs); push/pop touch only atomics/pointers.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [rtrb 0.4.0 src/lib.rs](https://docs.rs/crate/rtrb/0.4.0/source/src/lib.rs) (2026) — A fixed-capacity buffer is allocated on construction. After that, no more memory is allocated (unless the type T does that internally).
  - ✓ [rtrb 0.4.0 README.md](https://docs.rs/crate/rtrb/0.4.0/source/README.md) (2026) — This crate can be used without the standard library, but the alloc crate is needed nevertheless.

### Interpret midir WinMM input timestamps as microseconds since start
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust midir 0.11.0

**midir’s WinMM backend delivers input callback timestamps in microseconds, converted from the Windows MIDI driver’s millisecond timestamp that starts at zero when midiInStart is called.**

- **How:** In the MidiInput::connect callback, treat the first u64 argument as microseconds elapsed since the connection began. Do not assume it is an absolute clock; it is an arbitrary epoch fixed for the lifetime of the MidiInputConnection.
- **Gotchas:** The timestamp epoch is fixed per MidiInputConnection, but it is not comparable across connections or processes. Do not assume it is Unix time.
- **In si-jam-sessions:** Bears on MIDI input ingestion; treat the u64 microseconds as relative to midiInStart and convert to the law's integer sample timeline.
- **Code checks** ([source](host-audio-and-midi.code.md#interpret-midir-winmm-input-timestamps-as-microseconds-since-start)):
  - *Check 1: midir input callback signature and timestamp type compile* · `compiles` · edition 2024 · host · bin · deps: midir · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** handler.rs: 'timestamp = timestamp as u64 * 1000' verbatim. MS Learn MIM_DATA page independently confirms dwTimestamp is ms 'beginning at zero when the midiInStart function was called'; connect() calls midiInStart once (mod.rs:329). · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 7 (host-audio-and-midi): cpal 0.18.2 WASAPI shared mode, input-only xrun reports; rtrb SPSC; no allocation on the callback; WinMM 1 ms, clocks anchored. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midir 0.11.0 README.md](https://docs.rs/crate/midir/0.11.0/source/README.md) (2026) — midir supports the WinMM backend on Windows.
  - ✓ [midir 0.11.0 src/backend/winmm/handler.rs](https://docs.rs/crate/midir/0.11.0/source/src/backend/winmm/handler.rs) (2026) — The WinMM input handler sets data.message.timestamp = timestamp as u64 * 1000, converting the dwTimestamp (milliseconds since midiInStart) to microseconds.

### Negative control: Vec push inside callback body increments allocator counter
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**A Vec::push inside the same simulated callback body increments the counting allocator, confirming the measurement is sensitive.**

- **How:** Use the same counting allocator. After resetting the counter, call vec.push(1.0) on a Vec::new() inside the simulated callback. Read the counter afterward; it is greater than zero.
- **Gotchas:** A Vec with reserved capacity may not allocate on push, so start with Vec::new(). The counting allocator must not itself allocate (e.g., no format! inside alloc).
- **In si-jam-sessions:** Bears on the signed lock pin: host audio callback must allocate nothing. This negative control demonstrates that the counting-allocator test is sensitive to allocations, ensuring a false negative is unlikely.
- **Code checks** ([source](host-audio-and-midi.code.md#negative-control-vec-push-inside-callback-body-increments-allocator-counter)):
  - *Check 1: Vec push inside callback body increments allocation counter* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** Ran the exact check: Vec::new().push(1.0) printed alloc_count>0 -- the counting allocator is demonstrably sensitive, not a vacuous control. CountingAllocator itself only does an atomic add + System forwarding.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [std::alloc - Rust](https://doc.rust-lang.org/stable/std/alloc/index.html) (2026) — The #[global_allocator] attribute allows configuring the choice of global allocator to route all default allocation requests to a custom object.
  - ✓ [GlobalAlloc in std::alloc - Rust](https://doc.rust-lang.org/stable/std/alloc/trait.GlobalAlloc.html) (2026) — GlobalAlloc's alloc method is called for each heap allocation, enabling a counting wrapper.

### Register assert_no_alloc AllocDisabler around the callback body to catch debug allocations
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024, rtrb 0.4.0, assert_no_alloc 1.1.2

**With AllocDisabler registered as #[global_allocator], assert_no_alloc aborts in debug if the callback body allocates and returns normally when it does not.**

- **How:** Add assert_no_alloc as a dependency, register #[global_allocator] static A: AllocDisabler = AllocDisabler;, and wrap the callback body in assert_no_alloc(move || { ... }). In debug builds, any allocation inside the closure triggers an abort via handle_alloc_error.
- **Gotchas:** Default features disable the guard in release; for debug-only protection this is correct. The closure must not drop heap-allocated types that deallocate inside the forbidden zone unless wrapped in PermitDrop. The oracle has no audio device, so this only proves the callback body, not cpal's backend thread.
- **In si-jam-sessions:** Bears on the signed lock pin: host audio callback must allocate nothing. Use assert_no_alloc as a second, independent guard around the callback body in debug builds.
- **Code checks** ([source](host-audio-and-midi.code.md#register-assert_no_alloc-allocdisabler-around-the-callback-body-to-catch-debug-allocations)):
  - *Check 1: assert_no_alloc returns normally when callback body does not allocate* · `runs` · edition 2024 · host · bin · deps: rtrb, assert_no_alloc · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** CORRECTED: Recipe's own check exercises only the non-allocating path (sum=10). The 'aborts if it allocates' half is real -- confirmed by AllocDisabler::check()'s handle_alloc_error call and by my own compiled counter-example, which aborted -- but no check here exercises it. · The check only proves the no-alloc branch (sum=10). My own counter-example (alloc inside the closure) aborted: exit 0xC0000409, stderr 'memory allocation of 8 bytes failed' -- confirms the untested abort half.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [assert_no_alloc 1.1.2 README.md](https://docs.rs/crate/assert_no_alloc/1.1.2/source/README.md) (2026) — With default features, the program will abort if a (de)allocation is attempted inside assert_no_alloc in debug mode.
  - ✓ [assert_no_alloc 1.1.2 src/lib.rs](https://docs.rs/crate/assert_no_alloc/1.1.2/source/src/lib.rs) (2026) — AllocDisabler::check calls std::alloc::handle_alloc_error when an allocation occurs while forbidden and warn mode is not selected.

### Render oscillator voices from SPSC queue into cpal silence buffer
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust cpal 0.18.2, rtrb 0.4.0

**The cpal output callback buffer is pre-filled with silence, and the callback can pop committed events from an rtrb Consumer without blocking or allocating.**

- **How:** In the callback, call consumer.pop() or consumer.pop_partial_slice() for each voice event. Write the rendered samples into the &mut [f32] buffer. If the queue is empty, do nothing; the buffer remains silent because cpal pre-filled it with equilibrium.
- **Gotchas:** The callback must not block waiting for the queue; always use try_pop and render silence if the queue is empty. Pre-silencing by cpal means missing a write leaves silence, not garbage.
- **In si-jam-sessions:** Bears on the oscillator renderer; read committed events from the SPSC queue and write samples into cpal's pre-silenced buffer.
- **Code checks** ([source](host-audio-and-midi.code.md#render-oscillator-voices-from-spsc-queue-into-cpal-silence-buffer)):
  - *Check 1: SPSC event queue feeds non-allocating audio callback simulation* · `runs` · edition 2024 · host · bin · deps: rtrb · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** wasapi/stream.rs: fill_equilibrium(buffer_slice,...) runs before data_callback(...) (line 886 vs 894), confirmed exact. rtrb lib.rs confirms non-blocking push/pop. Check's runs simulation reproduces pop-or-silence correctly.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [cpal 0.18.2 src/host/wasapi/stream.rs](https://docs.rs/crate/cpal/0.18.2/source/src/host/wasapi/stream.rs) (2026) — The output data callback receives &mut Data that has been pre-filled with equilibrium silence.
  - ✓ [rtrb 0.4.0 src/lib.rs](https://docs.rs/crate/rtrb/0.4.0/source/src/lib.rs) (2026) — Producer::push and Consumer::pop are non-blocking; attempts on a full or empty buffer return an error immediately.

### Request cpal BufferSize::Fixed on WASAPI shared-mode output
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust cpal 0.18.2

**cpal’s WASAPI backend always creates shared-mode streams, and BufferSize::Fixed only requests a callback size that the host may round.**

- **How:** Set StreamConfig.buffer_size to BufferSize::Fixed(frames) before calling build_output_stream. Query SupportedBufferSize::Range on the device to pick a valid value. Expect shared mode; cpal does not expose exclusive mode.
- **Gotchas:** Requesting BufferSize::Fixed does not guarantee that exact size; WASAPI may round. Cpal does not expose exclusive mode; shared mode is always used.
- **In si-jam-sessions:** Bears on the host audio output path; use BufferSize::Fixed to control latency when playing committed events through the oscillator.
- **Code checks** ([source](host-audio-and-midi.code.md#request-cpal-buffersizefixed-on-wasapi-shared-mode-output)):
  - *Check 1: cpal BufferSize::Fixed and shared mode compile* · `compiles` · edition 2024 · host · bin · deps: cpal · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** lib.rs BufferSize doc: host may round, no size guaranteed (verbatim). wasapi/device.rs: 'always create voices in shared mode'. No AUDCLNT_SHAREMODE_EXCLUSIVE anywhere in cpal src/. Check's SampleRate/FrameCount are u32 aliases; compiles. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 7 (host-audio-and-midi): cpal 0.18.2 WASAPI shared mode, input-only xrun reports; rtrb SPSC; no allocation on the callback; WinMM 1 ms, clocks anchored. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [cpal 0.18.2 src/lib.rs](https://docs.rs/crate/cpal/0.18.2/source/src/lib.rs) (2026) — When BufferSize::Fixed(x) is specified, the host may round to hardware-supported values and no guarantees can be made about the actual callback size.
  - ✓ [cpal 0.18.2 src/host/wasapi/device.rs](https://docs.rs/crate/cpal/0.18.2/source/src/host/wasapi/device.rs) (2026) — The WASAPI device implementation comments state that cpal always creates voices in shared mode, therefore all samples go through an audio processor to mix them together.

### Use OutputCallbackInfo playback timestamp for latency alignment
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust cpal 0.18.2

**cpal output callbacks receive an OutputCallbackInfo whose timestamp contains a callback instant and a predicted playback instant derived from the device clock and buffered frames.**

- **How:** In the output callback, read info.timestamp().playback as a StreamInstant. On WASAPI this is computed from IAudioClock::GetPosition, frames_written, and stream_latency. Use playback minus callback to estimate latency.
- **Gotchas:** playback is a prediction, not a hardware interrupt timestamp; subtracting callback from playback gives latency but not sample-accurate device time.
- **In si-jam-sessions:** Bears on the host sample clock; use the playback instant to align the law's integer sample timeline with the audio device.
- **Code checks** ([source](host-audio-and-midi.code.md#use-outputcallbackinfo-playback-timestamp-for-latency-alignment)):
  - *Check 1: OutputCallbackInfo timestamp fields accessible* · `compiles` · edition 2024 · host · bin · deps: cpal · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** timestamp.rs host table lists WASAPI = QueryPerformanceCounter(). wasapi/stream.rs output_timestamp(): playback = callback + buffered + stream_latency; callback comes from clock_position() -> audio_clock.GetPosition.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [cpal 0.18.2 src/timestamp.rs](https://docs.rs/crate/cpal/0.18.2/source/src/timestamp.rs) (2026) — OutputStreamTimestamp contains a callback StreamInstant and a playback StreamInstant, and on WASAPI the time source for StreamInstant is QueryPerformanceCounter().
  - ✓ [cpal 0.18.2 src/host/wasapi/stream.rs](https://docs.rs/crate/cpal/0.18.2/source/src/host/wasapi/stream.rs) (2026) — The output_timestamp function derives playback by adding stream.stream_latency and the duration of buffered frames to the callback instant obtained from IAudioClock::GetPosition.

### Enumerate midir WinMM input ports by interface ID
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust midir 0.11.0

**MidiInput::ports returns a vector of MidiInputPort values on Windows via the WinMM midiInGetNumDevs and midiInGetDevCapsW APIs.**

- **How:** Create a MidiInput, call ports(), then iterate and call port_name() for display and id() for a stable string identifier. Use the id string to reconnect to the same physical device across restarts.
- **Gotchas:** WinMM port indices can change when devices are plugged or unplugged; use port.id() (the interface ID string) for stable identification, not the port index.
- **In si-jam-sessions:** Bears on host setup; enumerate WinMM ports with MidiInput::ports() before opening the input used for admitted actions.
- **Code checks** ([source](host-audio-and-midi.code.md#enumerate-midir-winmm-input-ports-by-interface-id)):
  - *Check 1: midir port enumeration compiles on Windows host* · `compiles` · edition 2024 · host · bin · deps: midir · jam dependency set · **✔ oracle pass**

- **Verifier (plausible):** CORRECTED: Source 2 covers count+display-name enumeration but not id(): MidiInputPort::id() returns interface_id, populated via midiInMessage(DRV_QUERYDEVICEINTERFACESIZE/DRV_QUERYDEVICEINTERFACE) -- a 3rd WinMM call neither source names. midiInGetDevCapsW supplies only port_name()'s string. · common.rs: MidiInputPorts = Vec<MidiInputPort> exact. mod.rs source's claim (midiInGetNumDevs+midiInGetDevCapsW) is true but incomplete for what the recipe actually relies on (id()); see corrections.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midir 0.11.0 src/common.rs](https://docs.rs/crate/midir/0.11.0/source/src/common.rs) (2026) — MidiInput::ports returns a Vec<MidiInputPort> and port_name returns the port name string.
  - ✓ [midir 0.11.0 src/backend/winmm/mod.rs](https://docs.rs/crate/midir/0.11.0/source/src/backend/winmm/mod.rs) (2026) — On Windows, ports_internal enumerates devices by calling midiInGetNumDevs and midiInGetDevCapsW.

### Handle cpal WASAPI xruns and device changes in error callback
`✗ wrong` · ✓ verified · ✔ compiles as claimed · Rust cpal 0.18.2

**The cpal WASAPI backend forwards discontinuities as ErrorKind::Xrun and device removals as DeviceNotAvailable or StreamInvalidated on the error callback.**

- **How:** Provide an error callback to build_output_stream. Match on err.kind(): ErrorKind::Xrun for glitches, ErrorKind::DeviceNotAvailable when the endpoint is unplugged, and ErrorKind::StreamInvalidated when the default device changes.
- **Gotchas:** ErrorKind::Xrun is only emitted on the input path in cpal 0.18.2; output underruns are not explicitly flagged as Xrun in the WASAPI backend.
- **In si-jam-sessions:** Bears on host reliability; route ErrorKind::Xrun and DeviceNotAvailable to the law's error log so replay can remain deterministic.
- **Code checks** ([source](host-audio-and-midi.code.md#handle-cpal-wasapi-xruns-and-device-changes-in-error-callback)):
  - *Check 1: cpal error callback handles ErrorKind* · `compiles` · edition 2024 · host · bin · deps: cpal · jam dependency set · **✔ oracle pass**

- **Verifier (wrong):** CORRECTED: 'StreamInvalidated when the default device changes' is wrong. MS Learn: AUDCLNT_E_RESOURCES_INVALIDATED fires when the stream is suspended, an exclusive/offload stream disconnects, a packaged app is quiesced, or a protected-output stream closes -- not on default-device change. · cpal's error-code mapping is exact, and Xrun-input-only gotcha is confirmed (process_output has zero Xrun logic). But 'StreamInvalidated when the default device changes' is wrong per MS Learn; see corrections. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 7 (host-audio-and-midi): cpal 0.18.2 WASAPI shared mode, input-only xrun reports; rtrb SPSC; no allocation on the callback; WinMM 1 ms, clocks anchored. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [cpal 0.18.2 src/host/wasapi/stream.rs](https://docs.rs/crate/cpal/0.18.2/source/src/host/wasapi/stream.rs) (2026) — In process_input, the WASAPI stream emits ErrorKind::Xrun when the AUDCLNT_BUFFERFLAGS_DATA_DISCONTINUITY flag is set.
  - ✓ [cpal 0.18.2 src/host/wasapi/mod.rs](https://docs.rs/crate/cpal/0.18.2/source/src/host/wasapi/mod.rs) (2026) — Windows error codes AUDCLNT_E_DEVICE_INVALIDATED and AUDCLNT_E_ENDPOINT_CREATE_FAILED map to ErrorKind::DeviceNotAvailable, and AUDCLNT_E_RESOURCES_INVALIDATED maps to ErrorKind::StreamInvalidated.

### Send events to audio callback via lock-free rtrb or ringbuf queue
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust rtrb 0.4.0, ringbuf 0.5.2

**Both rtrb and ringbuf provide single-producer single-consumer queues that are lock-free and allocate only on construction, making them safe for real-time audio callbacks.**

- **How:** Create a RingBuffer::new(capacity) (rtrb) or HeapRb::new(capacity) (ringbuf) on the host thread before starting the stream. Move the Consumer into the cpal callback and the Producer stays on the host thread. Use try_push and try_pop (or pop) so the callback never blocks.
- **Gotchas:** rtrb requires std or alloc by default; ringbuf 0.5 uses edition 2024 and requires the std feature for HeapRb. Neither queue provides blocking pop, so the callback must poll.
- **In si-jam-sessions:** Bears on the host-to-callback event delivery; adopt a wait-free SPSC queue so the audio callback never blocks or allocates.
- **Code checks** ([source](host-audio-and-midi.code.md#send-events-to-audio-callback-via-lock-free-rtrb-or-ringbuf-queue)):
  - *Check 1: rtrb SPSC queue works across threads without blocking* · `runs` · edition 2024 · host · bin · deps: rtrb · jam dependency set · **✔ oracle pass**

- **Verifier (plausible):** CORRECTED: 'requires std feature for HeapRb' is imprecise: alias.rs/macros.rs gate HeapRb::new() on feature="alloc" only; std enables alloc by default but alloc alone suffices. Also 'try_push and try_pop (or pop)' overstates rtrb: rtrb only has push()/pop(); try_push/try_pop is ringbuf-only naming. · Core 'what' fully sourced: rtrb lib.rs says lock-free/wait-free, alloc-once; ringbuf lib.rs literally says 'Lock-free SPSC'; SharedRb uses AtomicUsize+Acquire/Release. Two gotcha-level naming/feature claims need fixing; see corrections. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 7 (host-audio-and-midi): cpal 0.18.2 WASAPI shared mode, input-only xrun reports; rtrb SPSC; no allocation on the callback; WinMM 1 ms, clocks anchored. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [rtrb 0.4.0 src/lib.rs](https://docs.rs/crate/rtrb/0.4.0/source/src/lib.rs) (2026) — Reading from and writing into the ring buffer is lock-free and wait-free; a fixed-capacity buffer is allocated on construction and no more memory is allocated afterwards.
  - ✓ [ringbuf 0.5.2 src/rb/shared.rs](https://docs.rs/crate/ringbuf/0.5.2/source/src/rb/shared.rs) (2026) — SharedRb synchronizes producer and consumer via AtomicUsize indices with Ordering::Acquire and Ordering::Release, providing a lock-free SPSC implementation.

### Wrap oscillator callback in assert_no_alloc with cpal equilibrium buffer
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust assert_no_alloc 1.1.2, cpal 0.18.2

**assert_no_alloc aborts or warns if the audio callback allocates, and cpal pre-fills the output buffer with silence before invoking the callback.**

- **How:** Register the global allocator AllocDisabler in main (debug builds). Inside the cpal output callback, wrap all work in assert_no_alloc(|| { ... }). Because cpal calls fill_equilibrium before the callback, any slot the callback does not overwrite remains silent.
- **Gotchas:** assert_no_alloc only catches allocations made through the global allocator; it does not prevent Vec growth inside the closure unless the global allocator is hooked. In release mode with default features it is a no-op.
- **In si-jam-sessions:** Bears on the real-time guarantee; wrap the oscillator callback in assert_no_alloc to enforce zero allocation on the audio thread.
- **Code checks** ([source](host-audio-and-midi.code.md#wrap-oscillator-callback-in-assert_no_alloc-with-cpal-equilibrium-buffer)):
  - *Check 1: assert_no_alloc wraps cpal callback pattern compiles* · `compiles` · edition 2024 · host · bin · deps: cpal, assert_no_alloc · jam dependency set · **✔ oracle pass**
  - *Check 2: with AllocDisabler as #[global_allocator], an allocation inside assert_no_alloc aborts (debug build); one outside it is allowed* · `runs` · edition 2024 · host · bin · deps: assert_no_alloc · jam dependency set · exit code 3221226505 · **✔ oracle pass**

- **Verifier (plausible):** CORRECTED: Check omits '#[global_allocator] static A: AllocDisabler', which the recipe's own 'how' and README step 2 require. Without it, assert_no_alloc(||...) compiles/runs but checks nothing -- it only proves the closure nests inside a cpal callback, not that allocation is caught. · Both sources exact: README 'abort or print a warning'; wasapi/stream.rs fill_equilibrium() runs before data_callback() (line 886 vs 894). But the check never registers AllocDisabler as #[global_allocator]; see corrections. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 7 (host-audio-and-midi): cpal 0.18.2 WASAPI shared mode, input-only xrun reports; rtrb SPSC; no allocation on the callback; WinMM 1 ms, clocks anchored. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 2/2 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [assert_no_alloc 1.1.2 README.md](https://docs.rs/crate/assert_no_alloc/1.1.2/source/README.md) (2026) — If a (de)allocation is attempted inside the forbidden zone, the program will abort or print a warning.
  - ✓ [cpal 0.18.2 src/host/wasapi/stream.rs](https://docs.rs/crate/cpal/0.18.2/source/src/host/wasapi/stream.rs) (2026) — Before invoking the output data callback, process_output calls fill_equilibrium to pre-fill the buffer with silence.

