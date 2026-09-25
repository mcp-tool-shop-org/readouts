# Integer musical time: ticks, tempo maps, samples
_Tick to microsecond and sample through an SMF tempo map with u64/u128 math, exact rounding, PPQ choice, bars under meter changes._ · tier **si-jam-sessions** · wave 4 · 2026-09-25 · [‹ catalog index](README.md)

10 recipes · 10 verified · 9 compiler-checked.

| Recipe | Rust | Currency | ✓ | Code | What |
|--------|------|----------|---|------|------|
| Calculate bar and beat from tick under SMF time signatures | 1.98.1, edition 2024 | ✅ solid | ✓ | ✔ | SMF FF 58 stores numerator and a power-of-two denominator; bar/beat arithmetic uses ticks_ |
| Enable overflow-checks in release or rely on checked ops | 1.98.1, edition 2024 | ✅ solid | ✓ | · | Inference: The release profile disables overflow-checks by default, so unchecked operators |
| Refuse on overflow with checked arithmetic | 1.98.1, edition 2024 | ✅ solid | ✓ | ✔ | The law uses checked_mul and checked_add so that any overflow in time calculations returns |
| Carry division remainders across tempo segments | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | Floor division is not associative across segment sums: floor(a/c)+floor(b/c) can be less t |
| Choose PPQ divisible by 3 and 5 for exact tuplets | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | PPQ values 480, 960 and 3840 are divisible by 3 and 5, yielding exact integer tick deltas  |
| Compute tick-to-microseconds with u128 intermediate and floor | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | SMF stores tempo as u24 microseconds-per-quarter and tick deltas as u28; the law evaluates |
| Compute tick-to-samples through tempo map with u128 | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | Samples are derived from ticks by the exact rational tick×tempo×sample_rate÷(PPQ×1_000_000 |
| Exclude f64 seconds from the law time path | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | f64 cannot represent every u64 value exactly, so microseconds and samples are kept as inte |
| Reserve Wrapping arithmetic for hash state only | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | Wrapping<u64> provides modular arithmetic for hashing and checksums, but must never be use |
| Use u128 intermediates on wasm32-unknown-unknown | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | u128 compiles and runs on wasm32-unknown-unknown via compiler-builtins, so the law can saf |

## Detail

### Calculate bar and beat from tick under SMF time signatures
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**SMF FF 58 stores numerator and a power-of-two denominator; bar/beat arithmetic uses ticks_per_beat = PPQ × 4 ÷ 2^denom and ticks_per_bar = ticks_per_beat × num.**

- **How:** Parse the four TimeSignature bytes; compute `beat_unit = 1u32 << denom_exp; ticks_per_beat = (ppq * 4) / beat_unit;` then derive bar, beat and tick-in-beat with `/` and `%`.
- **Gotchas:** The denominator byte is the exponent, not the written denominator; e.g., 4/4 uses denom_exp = 2.
- **In si-jam-sessions:** Bears on the integer tick timeline: the law must locate events in bars and beats for display and looping without floating point.
- **Code checks** ([source](integer-time.code.md#calculate-bar-and-beat-from-tick-under-smf-time-signatures)):
  - *Check 1: bar beat from tick under 4-4 time* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** Ran the check verbatim (stdout '1 0 0') plus my own non-boundary case tick=2500: got '1 1 100', matching hand derivation. SMF spec (retrieved separately) confirms the denominator byte is the power-of-2 exponent.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 src/event.rs](https://docs.rs/crate/midly/0.5.3/source/src/event.rs) (2026) — MetaMessage::TimeSignature stores four u8 values: numerator, denominator power of two, MIDI clocks per click, and 32nd notes per quarter.
  - ✓ [midly 0.5.3 src/primitive.rs](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — Timing::Metrical(u15) stores the number of ticks per beat (PPQ) as a 15-bit integer.

### Enable overflow-checks in release or rely on checked ops
`✅ solid` · ✓ verified · · no code check · Rust 1.98.1, edition 2024

**Inference: The release profile disables overflow-checks by default, so unchecked operators wrap; the law should either set overflow-checks = true or use exclusively checked methods.**

- **How:** Add `overflow-checks = true` under `[profile.release]` in Cargo.toml, or prefer `checked_` methods explicitly.
- **Gotchas:** Relying on the default release profile makes `+` and `*` silently wrap, corrupting musical position.
- **In si-jam-sessions:** Bears on the deterministic replay and hash: silent wrap in release would desynchronise the score from the action log.

- **Verifier (solid):** No check was given, so I wrote one: -C overflow-checks=on panicked on an opaque u64::MAX+1 at opt-level 3; =off and the un-set default at opt-level 3 both wrapped to 0, matching the Cargo doc's stated release default.
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [Profiles](https://doc.rust-lang.org/stable/cargo/reference/profiles.html) (2026) — The overflow-checks setting controls the -C overflow-checks flag, and when overflow-checks are enabled, a panic will occur on overflow.
  - ✓ [Operator expressions](https://doc.rust-lang.org/stable/reference/expressions/operator-expr.html) (2026) — Integer operators will panic when they overflow when compiled in debug mode, and the -C overflow-checks compiler flag can be used to control this more directly.

### Refuse on overflow with checked arithmetic
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**The law uses checked_mul and checked_add so that any overflow in time calculations returns a refusal instead of wrapping or panicking.**

- **How:** Chain `tick.checked_mul(tempo)?.checked_add(carry)?` and propagate None as a refusal event to the host.
- **Gotchas:** Unchecked `*` panics in debug and wraps in release by default; strict_mul always panics, which is unsuitable for a law that must refuse gracefully.
- **In si-jam-sessions:** Bears on deterministic replay: an overflow must produce a defined refusal in the action log, not a wrap or trap.
- **Code checks** ([source](integer-time.code.md#refuse-on-overflow-with-checked-arithmetic)):
  - *Check 1: checked_mul returns None on overflow* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** Ran the check verbatim: stdout 'refused' (u64::MAX.checked_mul(2) -> None). Both sources match doc.rust-lang.org wording verbatim.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [Primitive Type u64](https://doc.rust-lang.org/stable/std/primitive.u64.html) (2026) — u64::checked_mul computes self * rhs, returning None if overflow occurred.
  - ✓ [Operator expressions](https://doc.rust-lang.org/stable/reference/expressions/operator-expr.html) (2026) — Integer operators will panic when they overflow when compiled in debug mode.

### Carry division remainders across tempo segments
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**Floor division is not associative across segment sums: floor(a/c)+floor(b/c) can be less than floor((a+b)/c); the law carries remainders to keep cumulative time exact.**

- **How:** For each segment compute `quot = tick * tempo / PPQ` and `rem = (tick * tempo) % PPQ`; add `rem` to the next segment’s numerator before division.
- **Gotchas:** Flooring each segment independently drops fractional ticks that accumulate into audible micro-timing drift across tempo changes.
- **In si-jam-sessions:** Bears on the integer tempo map: crossing a tempo boundary must not lose fractional ticks between the score and the sample timeline.
- **Code checks** ([source](integer-time.code.md#carry-division-remainders-across-tempo-segments)):
  - *Check 1: floor division remainder carry fixes drift* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (plausible):** Ran the check verbatim: stdout '3 2' then '3' -- confirms floor((a+b)/c) != a/c+b/c, and the remainder-carry sum recovers the exact total. Both cited sources are true but unused; the check only uses plain u64 %,/.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [Primitive Type u64](https://doc.rust-lang.org/stable/std/primitive.u64.html) (2026) — u64::checked_rem computes self % rhs, returning None if rhs is zero.
  - ✓ [Primitive Type u128](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128 is a 128-bit unsigned integer type.

### Choose PPQ divisible by 3 and 5 for exact tuplets
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**PPQ values 480, 960 and 3840 are divisible by 3 and 5, yielding exact integer tick deltas for triplets and quintuplets, but not for septuplets.**

- **How:** Select a PPQ that is a multiple of the desired tuplet ratio; verify exactness with `ppq % ratio == 0`.
- **Gotchas:** 3840 is not divisible by 7, so a septuplet grid must be approximated or handled by a higher-level tuplet track.
- **In si-jam-sessions:** Bears on the fixed PPQ lock item: the chosen PPQ must be high enough and factorable so that common tuplets are exact integers.
- **Code checks** ([source](integer-time.code.md#choose-ppq-divisible-by-3-and-5-for-exact-tuplets)):
  - *Check 1: PPQ divisibility for tuplets* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (plausible):** Ran the check verbatim: stdout matched exactly for 480/960/3840 mod 3,5,7. Timing::Metrical(u15) confirmed in primitive.rs. checked_rem source is accurate but the check itself only ever uses plain %.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 src/primitive.rs](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — Timing::Metrical stores ticks per beat (PPQ) as a u15 restricted integer.
  - ✓ [Primitive Type u64](https://doc.rust-lang.org/stable/std/primitive.u64.html) (2026) — u64::checked_rem computes self % rhs, returning None only when rhs is zero.

### Compute tick-to-microseconds with u128 intermediate and floor
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**SMF stores tempo as u24 microseconds-per-quarter and tick deltas as u28; the law evaluates the exact rational tick×tempo÷PPQ in u128 and floors once per segment.**

- **How:** Inside an extern "C" function, write `let us = ((tick as u128 * tempo as u128) / ppq as u128) as u64;`. The single integer division is the floor.
- **Gotchas:** Dividing before multiplying truncates early and loses tempo resolution; u64 intermediates overflow at max tick × max tempo.
- **In si-jam-sessions:** Bears on the likely second integer timeline in samples: the wasm cdylib must convert ticks to exact microseconds without floating point.
- **Code checks** ([source](integer-time.code.md#compute-tick-to-microseconds-with-u128-intermediate-and-floor)):
  - *Check 1: tick to microseconds via u128 on wasm* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · exports tick_to_us · node calls tick_to_us() · **✔ oracle pass**

- **Verifier (plausible):** Host port of the wasm check ran: stdout 500000, exact. Wasm build with #[unsafe(no_mangle)] compiles on 1.98.1/ed2024. Gotcha confirmed: u64.checked_mul at max tick x u24::MAX tempo overflows; the u128 product does not.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✗ [midly 0.5.3 src/primitive.rs](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — SMF tempo is stored as a u24 microseconds per quarter, and tick deltas are stored as a u28.
  - ✓ [Primitive Type u128](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128 is a 128-bit unsigned integer type with a maximum value of 2^128 − 1, sufficient to hold the product of a u64 tick count and a u24 tempo without overflow.

### Compute tick-to-samples through tempo map with u128
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**Samples are derived from ticks by the exact rational tick×tempo×sample_rate÷(PPQ×1_000_000), computed in u128 and floored once.**

- **How:** Compute `let num = tick as u128 * tempo as u128 * sample_rate as u128; let den = ppq as u128 * 1_000_000u128; let samples = (num / den) as u64;` inside the exported function.
- **Gotchas:** Reordering to divide early introduces rounding errors; the full numerator must stay in u128 until the final division.
- **In si-jam-sessions:** Bears on the likely separately pinned renderer: sample positions must be exact integers computed from the tempo map inside the wasm law.
- **Code checks** ([source](integer-time.code.md#compute-tick-to-samples-through-tempo-map-with-u128)):
  - *Check 1: tick to samples via u128 on wasm* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · exports tick_to_samples · node calls tick_to_samples() · **✔ oracle pass**

- **Verifier (plausible):** Host port of the wasm check ran: stdout 24000, exact. Same primitive.rs mis-citation as the tick-to-us recipe; the u24 tempo / u28 delta tie is defined in event.rs, not primitive.rs.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✗ [midly 0.5.3 src/primitive.rs](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — SMF tempo is stored as a u24 microseconds per quarter, and tick deltas are stored as a u28.
  - ✓ [Primitive Type u128](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128 is a 128-bit unsigned integer type with a maximum value of 2^128 − 1, sufficient to hold the product of a u64 tick count, a u24 tempo, and a u32 sample rate without overflow.

### Exclude f64 seconds from the law time path
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**f64 cannot represent every u64 value exactly, so microseconds and samples are kept as integers; midly’s second_f32 exists only for SMPTE display.**

- **How:** Store tempo as u24 microseconds-per-quarter and onsets as u64 ticks or samples; never convert through `as f64`.
- **Gotchas:** A single `tick as f64 * tempo as f64 / ppq as f64` introduces rounding that shifts note onsets by whole samples.
- **In si-jam-sessions:** Bears on the no-floating-point rule: the law’s state and time path must contain no f64 values.
- **Code checks** ([source](integer-time.code.md#exclude-f64-seconds-from-the-law-time-path)):
  - *Check 1: f64 loses precision for large u64* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (plausible):** Ran the check verbatim: stdout '9007199254740993 9007199254740992' exact -- 2^53+1 round-trips through f64 losing 1. midly's second_f32 confirmed on SmpteTime. Second source (u128) is true but unrelated filler.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 src/primitive.rs](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — SmpteTime provides a second_f32 method that returns an f32 representation of seconds.
  - ✓ [Primitive Type u128](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128 is a 128-bit unsigned integer type.

### Reserve Wrapping arithmetic for hash state only
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**Wrapping<u64> provides modular arithmetic for hashing and checksums, but must never be used for tick or sample counts because it silently wraps on underflow.**

- **How:** Use `Wrapping(hash)` for the state hash; use `checked_add` or exact integer ops for the timeline.
- **Gotchas:** Accidentally using Wrapping for deltas makes `zero - one` jump to u32::MAX, destroying bar/beat alignment.
- **In si-jam-sessions:** Bears on the state hash: the law hashes its state with wrapping arithmetic, but the musical timeline must never wrap.
- **Code checks** ([source](integer-time.code.md#reserve-wrapping-arithmetic-for-hash-state-only)):
  - *Check 1: Wrapping sub wraps around* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (plausible):** Ran the check verbatim: stdout 4294967295 (Wrapping(0u32)-Wrapping(1u32) underflows). engine_note states the hash specifically uses Wrapping, a detail the given lock doesn't itself lock (only 'audio outside the hash').
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [Struct std::num::Wrapping](https://doc.rust-lang.org/stable/std/num/struct.Wrapping.html) (2026) — Wrapping<T> provides intentionally-wrapped arithmetic on T.
  - ✓ [Operator expressions](https://doc.rust-lang.org/stable/reference/expressions/operator-expr.html) (2026) — Integer operators will panic when they overflow when compiled in debug mode.

### Use u128 intermediates on wasm32-unknown-unknown
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**u128 compiles and runs on wasm32-unknown-unknown via compiler-builtins, so the law can safely use u128 for tempo-map intermediates.**

- **How:** Cast operands to u128 inside the wasm-exported function; the compiler lowers the math to wasm i64/i32 operations.
- **Gotchas:** u128 is not in the wasm C ABI, so extern "C" functions must not pass or return u128 directly; use u64 and reconstruct internally.
- **In si-jam-sessions:** Bears on the wasm32-unknown-unknown cdylib target: u128 is available in core for exact integer time math.
- **Code checks** ([source](integer-time.code.md#use-u128-intermediates-on-wasm32-unknown-unknown)):
  - *Check 1: u128 math compiles and runs on wasm32* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · exports u128_demo · node calls u128_demo() · **✔ oracle pass**

- **Verifier (plausible):** Wasm build compiles; host port gave stdout 1. Neither source discusses FFI/ABI. Counter-example: extern "C" fn(u128)->u128 compiles with NO lint, but its wasm export has JS arity 3, not 1 -- confirms the gotcha by a different route.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [Primitive Type u128](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128 is a 128-bit unsigned integer type.
  - ✓ [wasm32-unknown-unknown](https://doc.rust-lang.org/stable/rustc/platform-support/wasm32-unknown-unknown.html) (2026) — The wasm32-unknown-unknown target has full support for the core and alloc crates.

