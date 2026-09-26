# Integer musical time: ticks, tempo maps, samples
_Tick to microsecond and sample through an SMF tempo map with u64/u128 math, exact rounding, PPQ choice, bars under meter changes._ · tier **si-jam-sessions** · wave 5 · 2026-09-25 · [‹ catalog index](README.md)

15 recipes · 15 verified · 14 compiler-checked.

| Recipe | Rust | Currency | ✓ | Code | What |
|--------|------|----------|---|------|------|
| Bound the largest tick whose product with 16777215 and 48000 still fits in u128 | 1.98.1, edition 2024 | ✅ solid | ✓ | ✔ | tick.checked_mul(16777215).and_then(/p/ p.checked_mul(48000)) is Some for every tick throu |
| Calculate bar and beat from tick under SMF time signatures | 1.98.1, edition 2024 | ✅ solid | ✓ | ✔ | SMF FF 58 stores numerator and a power-of-two denominator; bar/beat arithmetic uses ticks_ |
| Enable overflow-checks in release or rely on checked ops | 1.98.1, edition 2024 | ✅ solid | ✓ | · | Inference: The release profile disables overflow-checks by default, so unchecked operators |
| Export the u128 tick-to-sample floor from a wasm32 cdylib that takes and returns u64 | 1.98.1, edition 2024, target wasm32-unknown-unknown | ✅ solid | ✓ | ✔ | wasm32-unknown-unknown can export tick_to_sample(tick: u64, tempo_us_per_quarter: u64, ppq |
| Match one floor of a multi-segment span by carrying the remainder while independent floors drift | 1.98.1, edition 2024 | ✅ solid | ✓ | ✔ | Flooring each tempo segment with the remainder of tick * tempo_us * 48000 divided by PPQ * |
| Print whole-tick 3:2, 5:4 and 7:4 durations from a whole note through a 128th at PPQ 3360 | 1.98.1, edition 2024; SMF ticks/beat is midly 0.5.3 u15 | ✅ solid | ✓ | ✔ | At PPQ 3360 every 3:2, 5:4 and 7:4 tuplet of a whole, half, quarter, eighth, sixteenth, th |
| Refuse on overflow with checked arithmetic | 1.98.1, edition 2024 | ✅ solid | ✓ | ✔ | The law uses checked_mul and checked_add so that any overflow in time calculations returns |
| Show every 7:4 tuplet from a whole note through a 128th is not a whole tick at PPQ 480, 960 and 3840 | 1.98.1, edition 2024; SMF ticks/beat is midly 0.5.3 u15 | ✅ solid | ✓ | ✔ | At PPQ 480, 960 and 3840 the 3:2 and 5:4 tuplets of those eight note values are whole tick |
| Carry division remainders across tempo segments | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | Floor division is not associative across segment sums: floor(a/c)+floor(b/c) can be less t |
| Choose PPQ divisible by 3 and 5 for exact tuplets | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | PPQ values 480, 960 and 3840 are divisible by 3 and 5, yielding exact integer tick deltas  |
| Compute tick-to-microseconds with u128 intermediate and floor | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | SMF stores tempo as u24 microseconds-per-quarter and tick deltas as u28; the law evaluates |
| Compute tick-to-samples through tempo map with u128 | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | Samples are derived from ticks by the exact rational tick×tempo×sample_rate÷(PPQ×1_000_000 |
| Exclude f64 seconds from the law time path | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | f64 cannot represent every u64 value exactly, so microseconds and samples are kept as inte |
| Reserve Wrapping arithmetic for hash state only | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | Wrapping<u64> provides modular arithmetic for hashing and checksums, but must never be use |
| Use u128 intermediates on wasm32-unknown-unknown | 1.98.1, edition 2024 | ▸ plausible | ✓ | ✔ | u128 compiles and runs on wasm32-unknown-unknown via compiler-builtins, so the law can saf |

## Detail

### Bound the largest tick whose product with 16777215 and 48000 still fits in u128
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**tick.checked_mul(16777215).and_then(|p| p.checked_mul(48000)) is Some for every tick through 422550225262032543670307476 and None at the next tick; at PPQ 3360 that bound is a floor of 24419973467535932409 days.**

- **How:** Tempo is (1 << 24) - 1, which equals 0xFFFFFF. factor = tempo.checked_mul(48000). max_tick = u128::MAX.checked_div(factor). Require max_tick.checked_mul(factor) to be Some and (max_tick + 1).checked_mul(factor) to be None. Floor days are max_tick * tempo / 3360 / 1_000_000 / 86_400. The same factor times u64::MAX is still Some.
- **Gotchas:** A bare * panics on overflow only when overflow-checks is enabled, and wraps when it is disabled. checked_mul returns None in either build. u64::MAX cannot reach this bound, but the sample quotient of a huge tick can still exceed u64, so the export must refuse when the quotient does not fit in the 64-bit return.
- **In si-jam-sessions:** Signed lock: tick to sample is computed in u128 with checked_* and a refusal on None, and the release profile sets overflow-checks = true. Keep the product tick * tempo_us_per_quarter * 48000 on checked_mul; a musical take ends long before tick 422550225262032543670307476.
- **Code checks** ([source](integer-time.code.md#bound-the-largest-tick-whose-product-with-16777215-and-48000-still-fits-in-u128)):
  - *Check 1: checked_mul fits the max tick times 16777215 times 48000 and refuses the next tick* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** Independent Python bigint recompute: factor=805306320000, max_tick=422550225262032543670307476, overflows at +1, u64::MAX*factor fits, days=24419973467535932409 -- all exact. WebFetch confirmed checked_mul + overflow-checks docs.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [u128 checked_mul](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128::checked_mul computes self * rhs and returns None if overflow occurred.
  - ✓ [midly 0.5.3 primitive.rs u24](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — u24 wraps a u32 and keeps the low 24 bits; its mask is (1 << 24) - 1.
  - ✓ [Cargo profile overflow-checks](https://doc.rust-lang.org/stable/cargo/reference/profiles.html) (2026) — The overflow-checks profile setting controls -C overflow-checks, and when overflow-checks are enabled a panic occurs on overflow.

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

- **Verifier (solid):** No check was given, so I wrote one: -C overflow-checks=on panicked on an opaque u64::MAX+1 at opt-level 3; =off and the un-set default at opt-level 3 both wrapped to 0, matching the Cargo doc's stated release default. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 2 (integer-time): PPQ 3360; tick to sample in u128, floored with the remainder carried; checked_* with a refusal; overflow-checks on; no f64. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [Profiles](https://doc.rust-lang.org/stable/cargo/reference/profiles.html) (2026) — The overflow-checks setting controls the -C overflow-checks flag, and when overflow-checks are enabled, a panic will occur on overflow.
  - ✓ [Operator expressions](https://doc.rust-lang.org/stable/reference/expressions/operator-expr.html) (2026) — Integer operators will panic when they overflow when compiled in debug mode, and the -C overflow-checks compiler flag can be used to control this more directly.

### Export the u128 tick-to-sample floor from a wasm32 cdylib that takes and returns u64
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024, target wasm32-unknown-unknown

**wasm32-unknown-unknown can export tick_to_sample(tick: u64, tempo_us_per_quarter: u64, ppq: u64) -> u64, which floors tick * tempo * 48000 / (ppq * 10^6) in u128 and returns 48000 for one quarter at 1000000 microseconds and PPQ 3360; tick_to_sample_status returns 1 when checked_div refuses a zero PPQ.**

- **How:** Build an edition 2024 cdylib with #[unsafe(no_mangle)] extern "C" functions. Widen each u64 to u128, then checked_mul by the tempo, checked_mul by 48000, checked_div by ppq.checked_mul(1_000_000), and u64::try_from the quotient. tick_to_sample returns the quotient or u64::MAX on None; tick_to_sample_status returns 0 or 1. Call them from node with BigInt arguments.
- **Gotchas:** println! does nothing on wasm32-unknown-unknown, so the sample has to be the export's return value. A JS number is not an i64 argument; node must pass a BigInt. u64::MAX as the refusal sentinel collides with a genuine quotient of 2^64-1, which is why the status export is the refusal signal.
- **In si-jam-sessions:** Signed lock: edition 2024 cdylib for wasm32-unknown-unknown, raw extern "C" with #[unsafe(no_mangle)], every export argument and return at most 64 bits, status codes across the boundary and no panic. Compute the floor in u128 inside the export and return status 1 on None.
- **Code checks** ([source](integer-time.code.md#export-the-u128-tick-to-sample-floor-from-a-wasm32-cdylib-that-takes-and-returns-u64)):
  - *Check 1: wasm32 tick_to_sample(3360, 1000000, 3360) returns 48000* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · exports tick_to_sample, tick_to_sample_status · imports nothing · node calls tick_to_sample(3360n, 1000000n, 3360n) · **✔ oracle pass**
  - *Check 2: wasm32 tick_to_sample_status returns 1 when PPQ is 0* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · exports tick_to_sample_status · node calls tick_to_sample_status(3360n, 1000000n, 0n) · **✔ oracle pass**

- **Verifier (solid):** Both wasm_call checks PASS (compiler-executed, BigInt args). Hand-verified 3360*1e6*48000/(3360*1e6)=48000. Own counter-example (tick=tempo=1e15,ppq=1) proves the u64-quotient-overflow refusal is real and distinct from ppq=0, no panic.
- **Compiler:** 2/2 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [wasm32-unknown-unknown](https://doc.rust-lang.org/stable/rustc/platform-support/wasm32-unknown-unknown.html) (2026) — wasm32-unknown-unknown is compiled with rustc --target wasm32-unknown-unknown, fully supports core and alloc, imports no host functions for the standard library, and println! does nothing.
  - ✓ [u128 checked_mul and checked_div](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128::checked_mul returns None if self * rhs overflows, and u128::checked_div returns None if rhs is 0.

### Match one floor of a multi-segment span by carrying the remainder while independent floors drift
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**Flooring each tempo segment with the remainder of tick * tempo_us * 48000 divided by PPQ * 10^6 carried forward equals one floor of the summed numerators, and summing the separate floors is one sample lower for two one-tick segments at tempo 16777215 on PPQ 3360, 480, 960 and 3840.**

- **How:** denom = ppq.checked_mul(1_000_000). numer = ticks.checked_mul(tempo).checked_mul(48000).checked_add(rem). The segment returns (numer.checked_div(denom), numer.checked_rem(denom)) and the next segment adds that remainder before dividing. For ticks = 1 and tempo = (1 << 24) - 1 the carried totals are 479, 3355, 1677 and 419; the independent sums are 478, 3354, 1676 and 418.
- **Gotchas:** Cancelling 48000/10^6 down to 6/125 before the carry changes the modulus, so a remainder from the reduced fraction is not the remainder the next segment must add. Summing floor(segment) drops a sample whenever successive remainders add up to at least one denominator.
- **In si-jam-sessions:** Signed lock: tick to sample = floor(tick * tempo_us_per_quarter * 48000 / (PPQ * 10^6)) in u128, with the remainder carried across tempo segments, checked_* and a refusal on None. Carry this unreduced remainder; do not add independent per-segment floors.
- **Code checks** ([source](integer-time.code.md#match-one-floor-of-a-multi-segment-span-by-carrying-the-remainder-while-independent-floors-drift)):
  - *Check 1: Carried remainder matches one floor at four PPQs; separate floors are one sample low* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** Independent Python bigint recompute at PPQ 3360/480/960/3840: carried 479/3355/1677/419 vs independent 478/3354/1676/418, carried==floor(sum) every time -- exact match to prose+stdout. Own scenario also confirms r2<denom.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [u128 checked_div and checked_rem](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128::checked_div computes self / rhs and returns None if rhs is 0, and u128::checked_rem computes self % rhs and returns None if rhs is 0.
  - ✓ [midly 0.5.3 primitive.rs Tempo and Timing::Metrical](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — Timing::Metrical specifies ticks/beat as a 15-bit integer, and the beat length is not standard, so a MetaMessage::Tempo event is required to describe the length of a tick.
  - ✓ [Integer operator overflow](https://doc.rust-lang.org/stable/reference/expressions/operator-expr.html) (2026) — Integer * overflows when it creates a value greater than the maximum that the type can store, and integer operators panic on overflow in debug mode, controlled by -C overflow-checks.

### Print whole-tick 3:2, 5:4 and 7:4 durations from a whole note through a 128th at PPQ 3360
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024; SMF ticks/beat is midly 0.5.3 u15

**At PPQ 3360 every 3:2, 5:4 and 7:4 tuplet of a whole, half, quarter, eighth, sixteenth, thirty-second, sixty-fourth and hundred-twenty-eighth note is a whole number of ticks.**

- **How:** PPQ 3360 = 32*3*5*7. Note ticks for level k in 0..=7 are 3360*4/2^k (whole down to a 128th). One tuplet note is note*2/3, note*4/5 or note*4/7. Require checked_rem of that numerator to be 0 and keep the checked_div quotient: the 128th is 70, 84 and 60.
- **Gotchas:** A 7:8 septuplet is a different ratio and is not what this grid was factored for. PPQ 960 and 3840 still have no factor of 7, so switching the written ratio to another power of two does not make those 7-tuplets whole ticks. Do not round an f64 tuplet back onto this grid.
- **In si-jam-sessions:** Signed lock: the score is integer ticks at PPQ 3360 (2^5 * 3 * 5 * 7), with no floating point in the time path. Store that PPQ in Timing::Metrical and use these whole-tick 3:2, 5:4 and 7:4 lengths for onset and duration.
- **Code checks** ([source](integer-time.code.md#print-whole-tick-32-54-and-74-durations-from-a-whole-note-through-a-128th-at-ppq-3360)):
  - *Check 1: PPQ 3360 divides every 3:2, 5:4 and 7:4 from a whole note through a 128th* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** Recomputed all 8 note-levels x3 ratios in Python at PPQ 3360=2^5*3*5*7: exact match to stdout/how (128th=70/84/60). midly src confirms Timing::Metrical(u15). Oracle PASS. Lock@e3cc85e cites this exact rationale.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 primitive.rs Timing::Metrical](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — Timing::Metrical specifies ticks/beat as a 15-bit integer (u15), and u15's mask is (1 << 15) - 1.
  - ✓ [u128 checked_rem](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128::checked_rem computes self % rhs and returns None if rhs is 0.

### Refuse on overflow with checked arithmetic
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**The law uses checked_mul and checked_add so that any overflow in time calculations returns a refusal instead of wrapping or panicking.**

- **How:** Chain `tick.checked_mul(tempo)?.checked_add(carry)?` and propagate None as a refusal event to the host.
- **Gotchas:** Unchecked `*` panics in debug and wraps in release by default; strict_mul always panics, which is unsuitable for a law that must refuse gracefully.
- **In si-jam-sessions:** Bears on deterministic replay: an overflow must produce a defined refusal in the action log, not a wrap or trap.
- **Code checks** ([source](integer-time.code.md#refuse-on-overflow-with-checked-arithmetic)):
  - *Check 1: checked_mul returns None on overflow* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** Ran the check verbatim: stdout 'refused' (u64::MAX.checked_mul(2) -> None). Both sources match doc.rust-lang.org wording verbatim. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 2 (integer-time): PPQ 3360; tick to sample in u128, floored with the remainder carried; checked_* with a refusal; overflow-checks on; no f64. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [Primitive Type u64](https://doc.rust-lang.org/stable/std/primitive.u64.html) (2026) — u64::checked_mul computes self * rhs, returning None if overflow occurred.
  - ✓ [Operator expressions](https://doc.rust-lang.org/stable/reference/expressions/operator-expr.html) (2026) — Integer operators will panic when they overflow when compiled in debug mode.

### Show every 7:4 tuplet from a whole note through a 128th is not a whole tick at PPQ 480, 960 and 3840
`✅ solid` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024; SMF ticks/beat is midly 0.5.3 u15

**At PPQ 480, 960 and 3840 the 3:2 and 5:4 tuplets of those eight note values are whole ticks, and every 7:4 tuplet of them is not.**

- **How:** Use the same note ticks PPQ*4/2^k and the same ratios 2/3, 4/5 and 4/7. Count checked_rem == 0. Each of 480, 960 and 3840 yields 8, 8 and 0. All three PPQs, and 3360, are <= the u15 mask (1 << 15) - 1.
- **Gotchas:** 480, 960 and 3840 are common MIDI divisions and they do represent straight 128ths, because each is divisible by 32. They fail only the factor of 7. Fitting in the 15-bit header field is not the same as representing a septuplet.
- **In si-jam-sessions:** Signed lock: integer ticks at PPQ 3360 and no f64 in the time path. Do not adopt PPQ 480, 960 or 3840 for the law; every 7:4 from a whole through a 128th is a fractional tick there. Refuse a metrical header whose PPQ is not 3360.
- **Code checks** ([source](integer-time.code.md#show-every-74-tuplet-from-a-whole-note-through-a-128th-is-not-a-whole-tick-at-ppq-480-960-and-3840)):
  - *Check 1: PPQ 480, 960 and 3840 have eight exact 3:2 and 5:4 tuplets and no exact 7:4* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (solid):** Recomputed t3/t5/t7 counts for PPQ 480/960/3840 in Python: (8,8,0) each, all eight 7:4 fail -- exact match to stdout. u15 mask 32767 >= all 4 PPQs (checked). Oracle PASS. Engine_note matches locks single fixed PPQ 3360.
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 primitive.rs u15](https://docs.rs/crate/midly/0.5.3/source/src/primitive.rs) (2026) — u15 wraps a u16, keeps the low 15 bits, and Timing::Metrical stores ticks/beat as that u15.
  - ✓ [u128 checked_rem](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128::checked_rem computes self % rhs and returns None if rhs is 0, so a remainder of Some(0) is an exact division.

### Carry division remainders across tempo segments
`▸ plausible` · ✓ verified · ✔ compiles as claimed · Rust 1.98.1, edition 2024

**Floor division is not associative across segment sums: floor(a/c)+floor(b/c) can be less than floor((a+b)/c); the law carries remainders to keep cumulative time exact.**

- **How:** For each segment compute `quot = tick * tempo / PPQ` and `rem = (tick * tempo) % PPQ`; add `rem` to the next segment’s numerator before division.
- **Gotchas:** Flooring each segment independently drops fractional ticks that accumulate into audible micro-timing drift across tempo changes.
- **In si-jam-sessions:** Bears on the integer tempo map: crossing a tempo boundary must not lose fractional ticks between the score and the sample timeline.
- **Code checks** ([source](integer-time.code.md#carry-division-remainders-across-tempo-segments)):
  - *Check 1: floor division remainder carry fixes drift* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**

- **Verifier (plausible):** Ran the check verbatim: stdout '3 2' then '3' -- confirms floor((a+b)/c) != a/c+b/c, and the remainder-carry sum recovers the exact total. Both cited sources are true but unused; the check only uses plain u64 %,/. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 2 (integer-time): PPQ 3360; tick to sample in u128, floored with the remainder carried; checked_* with a refusal; overflow-checks on; no f64. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
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

- **Verifier (plausible):** Ran the check verbatim: stdout matched exactly for 480/960/3840 mod 3,5,7. Timing::Metrical(u15) confirmed in primitive.rs. checked_rem source is accurate but the check itself only ever uses plain %. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 2 (integer-time): PPQ 3360; tick to sample in u128, floored with the remainder carried; checked_* with a refusal; overflow-checks on; no f64. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
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

- **Verifier (plausible):** CORRECTED: Source cites src/primitive.rs for 'tempo=u24, delta=u28'; that tie is made in src/event.rs (MetaMessage::Tempo(u24); TrackEvent.delta: u28). primitive.rs only defines the generic bit-width wrapper types, not their use. · Host port of the wasm check ran: stdout 500000, exact. Wasm build with #[unsafe(no_mangle)] compiles on 1.98.1/ed2024. Gotcha confirmed: u64.checked_mul at max tick x u24::MAX tempo overflows; the u128 product does not.
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

- **Verifier (plausible):** CORRECTED: Source cites src/primitive.rs for 'tempo=u24, delta=u28'; that tie is in src/event.rs (MetaMessage::Tempo(u24); TrackEvent.delta: u28), not primitive.rs, which only defines the bit-width types generically. · Host port of the wasm check ran: stdout 24000, exact. Same primitive.rs mis-citation as the tick-to-us recipe; the u24 tempo / u28 delta tie is defined in event.rs, not primitive.rs. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 2 (integer-time): PPQ 3360; tick to sample in u128, floored with the remainder carried; checked_* with a refusal; overflow-checks on; no f64. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
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

- **Verifier (plausible):** Ran the check verbatim: stdout '9007199254740993 9007199254740992' exact -- 2^53+1 round-trips through f64 losing 1. midly's second_f32 confirmed on SmpteTime. Second source (u128) is true but unrelated filler. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 2 (integer-time): PPQ 3360; tick to sample in u128, floored with the remainder carried; checked_* with a refusal; overflow-checks on; no f64. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
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

- **Verifier (plausible):** CORRECTED: Neither cited source discusses the C ABI or FFI. The real warrant is doc.rust-lang.org's i128 page: i128/u128 ABI matches C's __int128 only where that type exists; wasm32-unknown-unknown has no C/C++ toolchain at all. · Wasm build compiles; host port gave stdout 1. Neither source discusses FFI/ABI. Counter-example: extern "C" fn(u128)->u128 compiles with NO lint, but its wasm export has JS arity 3, not 1 -- confirms the gotcha by a different route. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 1 (wasm-raw-abi): extern "C" + #[unsafe(no_mangle)], status codes not panics, every export argument and return at most 64 bits. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** 1/1 checks pass under rustc 1.98.1 (48a229cea 2026-09-01)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [Primitive Type u128](https://doc.rust-lang.org/stable/std/primitive.u128.html) (2026) — u128 is a 128-bit unsigned integer type.
  - ✓ [wasm32-unknown-unknown](https://doc.rust-lang.org/stable/rustc/platform-support/wasm32-unknown-unknown.html) (2026) — The wasm32-unknown-unknown target has full support for the core and alloc crates.

