# Integer musical time: ticks, tempo maps, samples — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 4 · 2026-09-25 · [‹ lane page](integer-time.md) · [catalog index](README.md)

## Calculate bar and beat from tick under SMF time signatures
**SMF FF 58 stores numerator and a power-of-two denominator; bar/beat arithmetic uses ticks_per_beat = PPQ × 4 ÷ 2^denom and ticks_per_bar = ticks_per_beat × num.**

*Check 1: bar beat from tick under 4-4 time* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
fn bar_beat(tick: u64, ppq: u32, num: u8, denom_exp: u8) -> (u64, u64, u64) {
    let beat_unit = 1u32 << denom_exp;
    let ticks_per_beat = (ppq as u64 * 4) / beat_unit as u64;
    let ticks_per_bar = ticks_per_beat * num as u64;
    let bar = tick / ticks_per_bar;
    let rem = tick % ticks_per_bar;
    let beat = rem / ticks_per_beat;
    let tick_in_beat = rem % ticks_per_beat;
    (bar, beat, tick_in_beat)
}
fn main() {
    let (b, be, t) = bar_beat(1920, 480, 4, 2);
    println!("{} {} {}", b, be, t);
}
```
Expected output: `1 0 0`

## Refuse on overflow with checked arithmetic
**The law uses checked_mul and checked_add so that any overflow in time calculations returns a refusal instead of wrapping or panicking.**

*Check 1: checked_mul returns None on overflow* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
fn main() {
    match u64::MAX.checked_mul(2) {
        Some(_) => println!("unexpected"),
        None => println!("refused"),
    }
}
```
Expected output: `refused`

## Carry division remainders across tempo segments
**Floor division is not associative across segment sums: floor(a/c)+floor(b/c) can be less than floor((a+b)/c); the law carries remainders to keep cumulative time exact.**

*Check 1: floor division remainder carry fixes drift* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
fn main() {
    let a = 5u64;
    let b = 5u64;
    let c = 3u64;
    println!("{} {}", (a + b) / c, a / c + b / c);
    let carried = a / c + b / c + (a % c + b % c) / c;
    println!("{}", carried);
}
```
Expected output: `3 2 3`

## Choose PPQ divisible by 3 and 5 for exact tuplets
**PPQ values 480, 960 and 3840 are divisible by 3 and 5, yielding exact integer tick deltas for triplets and quintuplets, but not for septuplets.**

*Check 1: PPQ divisibility for tuplets* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
fn main() {
    for ppq in [480u64, 960, 3840] {
        println!("{} {} {} {}", ppq, ppq % 3, ppq % 5, ppq % 7);
    }
}
```
Expected output: `480 0 0 4 960 0 0 1 3840 0 0 4`

## Compute tick-to-microseconds with u128 intermediate and floor
**SMF stores tempo as u24 microseconds-per-quarter and tick deltas as u28; the law evaluates the exact rational tick×tempo÷PPQ in u128 and floors once per segment.**

*Check 1: tick to microseconds via u128 on wasm* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · exports tick_to_us · node calls tick_to_us() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn tick_to_us() -> u64 {
    let tick: u64 = 480;
    let tempo: u64 = 500000;
    let ppq: u64 = 480;
    let t = tick as u128 * tempo as u128;
    (t / ppq as u128) as u64
}
```
Expected output: `500000`

## Compute tick-to-samples through tempo map with u128
**Samples are derived from ticks by the exact rational tick×tempo×sample_rate÷(PPQ×1_000_000), computed in u128 and floored once.**

*Check 1: tick to samples via u128 on wasm* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · exports tick_to_samples · node calls tick_to_samples() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn tick_to_samples() -> u64 {
    let tick: u64 = 480;
    let tempo: u64 = 500000;
    let ppq: u64 = 480;
    let sample_rate: u64 = 48000;
    let num = tick as u128 * tempo as u128 * sample_rate as u128;
    let den = ppq as u128 * 1_000_000u128;
    (num / den) as u64
}
```
Expected output: `24000`

## Exclude f64 seconds from the law time path
**f64 cannot represent every u64 value exactly, so microseconds and samples are kept as integers; midly’s second_f32 exists only for SMPTE display.**

*Check 1: f64 loses precision for large u64* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
fn main() {
    let us: u64 = 9_007_199_254_740_993u64;
    let f = us as f64;
    let back = f as u64;
    println!("{} {}", us, back);
}
```
Expected output: `9007199254740993 9007199254740992`

## Reserve Wrapping arithmetic for hash state only
**Wrapping<u64> provides modular arithmetic for hashing and checksums, but must never be used for tick or sample counts because it silently wraps on underflow.**

*Check 1: Wrapping sub wraps around* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
use std::num::Wrapping;
fn main() {
    let z = Wrapping(0u32);
    let o = Wrapping(1u32);
    println!("{}", (z - o).0);
}
```
Expected output: `4294967295`

## Use u128 intermediates on wasm32-unknown-unknown
**u128 compiles and runs on wasm32-unknown-unknown via compiler-builtins, so the law can safely use u128 for tempo-map intermediates.**

*Check 1: u128 math compiles and runs on wasm32* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · exports u128_demo · node calls u128_demo() · **✔ oracle pass**
```rust
#[unsafe(no_mangle)]
pub extern "C" fn u128_demo() -> u64 {
    let prod = u64::MAX as u128 * 2u128;
    (prod >> 64) as u64
}
```
Expected output: `1`

