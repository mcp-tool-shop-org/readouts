# Integer musical time: ticks, tempo maps, samples — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](integer-time.md) · [catalog index](README.md)

## Bound the largest tick whose product with 16777215 and 48000 still fits in u128
**tick.checked_mul(16777215).and_then(|p| p.checked_mul(48000)) is Some for every tick through 422550225262032543670307476 and None at the next tick; at PPQ 3360 that bound is a floor of 24419973467535932409 days.**

*Check 1: checked_mul fits the max tick times 16777215 times 48000 and refuses the next tick* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
fn main() {
    let tempo = (1u128 << 24) - 1;
    assert_eq!(tempo, 0x00FF_FFFF);
    let factor = tempo.checked_mul(48_000).unwrap();
    let tick = u128::MAX.checked_div(factor).unwrap();
    assert!(tick.checked_mul(factor).is_some());
    assert!(tick.checked_add(1).unwrap().checked_mul(factor).is_none());
    let u64_fits = (u64::MAX as u128).checked_mul(factor).is_some();
    let us = tick.checked_mul(tempo).unwrap().checked_div(3360).unwrap();
    let days = us.checked_div(1_000_000).unwrap().checked_div(86_400).unwrap();
    println!("factor {factor}");
    println!("max_tick {tick}");
    println!("next_overflows 1");
    println!("u64_max_fits {}", u64_fits as u8);
    println!("ppq3360_days {days}");
}
```
Expected output: `factor 805306320000 max_tick 422550225262032543670307476 next_overflows 1 u64_max_fits 1 ppq3360_days 24419973467535932409`

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

## Export the u128 tick-to-sample floor from a wasm32 cdylib that takes and returns u64
**wasm32-unknown-unknown can export tick_to_sample(tick: u64, tempo_us_per_quarter: u64, ppq: u64) -> u64, which floors tick * tempo * 48000 / (ppq * 10^6) in u128 and returns 48000 for one quarter at 1000000 microseconds and PPQ 3360; tick_to_sample_status returns 1 when checked_div refuses a zero PPQ.**

*Check 1: wasm32 tick_to_sample(3360, 1000000, 3360) returns 48000* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · exports tick_to_sample, tick_to_sample_status · imports nothing · node calls tick_to_sample(3360n, 1000000n, 3360n) · **✔ oracle pass**
```rust
#![no_std]

#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}

fn floor_sample(tick: u64, tempo_us_per_quarter: u64, ppq: u64) -> Option<u64> {
    let numer = (tick as u128)
        .checked_mul(tempo_us_per_quarter as u128)?
        .checked_mul(48_000)?;
    let denom = (ppq as u128).checked_mul(1_000_000)?;
    u64::try_from(numer.checked_div(denom)?).ok()
}

#[unsafe(no_mangle)]
pub extern "C" fn tick_to_sample(tick: u64, tempo_us_per_quarter: u64, ppq: u64) -> u64 {
    floor_sample(tick, tempo_us_per_quarter, ppq).unwrap_or(u64::MAX)
}

#[unsafe(no_mangle)]
pub extern "C" fn tick_to_sample_status(tick: u64, tempo_us_per_quarter: u64, ppq: u64) -> u64 {
    match floor_sample(tick, tempo_us_per_quarter, ppq) {
        Some(_) => 0,
        None => 1,
    }
}
```
Expected output: `48000`

*Check 2: wasm32 tick_to_sample_status returns 1 when PPQ is 0* · `runs` · edition 2024 · wasm32-unknown-unknown · cdylib · jam dependency set · exports tick_to_sample_status · node calls tick_to_sample_status(3360n, 1000000n, 0n) · **✔ oracle pass**
```rust
#![no_std]

#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    loop {}
}

fn floor_sample(tick: u64, tempo_us_per_quarter: u64, ppq: u64) -> Option<u64> {
    let numer = (tick as u128)
        .checked_mul(tempo_us_per_quarter as u128)?
        .checked_mul(48_000)?;
    let denom = (ppq as u128).checked_mul(1_000_000)?;
    u64::try_from(numer.checked_div(denom)?).ok()
}

#[unsafe(no_mangle)]
pub extern "C" fn tick_to_sample(tick: u64, tempo_us_per_quarter: u64, ppq: u64) -> u64 {
    floor_sample(tick, tempo_us_per_quarter, ppq).unwrap_or(u64::MAX)
}

#[unsafe(no_mangle)]
pub extern "C" fn tick_to_sample_status(tick: u64, tempo_us_per_quarter: u64, ppq: u64) -> u64 {
    match floor_sample(tick, tempo_us_per_quarter, ppq) {
        Some(_) => 0,
        None => 1,
    }
}
```
Expected output: `1`

## Match one floor of a multi-segment span by carrying the remainder while independent floors drift
**Flooring each tempo segment with the remainder of tick * tempo_us * 48000 divided by PPQ * 10^6 carried forward equals one floor of the summed numerators, and summing the separate floors is one sample lower for two one-tick segments at tempo 16777215 on PPQ 3360, 480, 960 and 3840.**

*Check 1: Carried remainder matches one floor at four PPQs; separate floors are one sample low* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
fn advance(ticks: u128, tempo: u128, ppq: u128, rem: u128) -> (u128, u128) {
    let denom = ppq.checked_mul(1_000_000).unwrap();
    let numer = ticks
        .checked_mul(tempo)
        .unwrap()
        .checked_mul(48_000)
        .unwrap()
        .checked_add(rem)
        .unwrap();
    (
        numer.checked_div(denom).unwrap(),
        numer.checked_rem(denom).unwrap(),
    )
}

fn main() {
    let tempo = (1u128 << 24) - 1;
    for ppq in [3360u128, 480, 960, 3840] {
        let denom = ppq.checked_mul(1_000_000).unwrap();
        let n1 = tempo.checked_mul(48_000).unwrap();
        let n2 = n1;
        let independent = n1.checked_div(denom).unwrap() + n2.checked_div(denom).unwrap();
        let whole = n1.checked_add(n2).unwrap().checked_div(denom).unwrap();
        let (q1, r1) = advance(1, tempo, ppq, 0);
        let (q2, r2) = advance(1, tempo, ppq, r1);
        let carried = q1 + q2;
        assert_eq!(carried, whole);
        assert!(independent < carried);
        assert!(r2 < denom);
        println!("{ppq} independent {independent} carried {carried}");
    }
}
```
Expected output: `3360 independent 478 carried 479 480 independent 3354 carried 3355 960 independent 1676 carried 1677 3840 independent 418 carried 419`

## Print whole-tick 3:2, 5:4 and 7:4 durations from a whole note through a 128th at PPQ 3360
**At PPQ 3360 every 3:2, 5:4 and 7:4 tuplet of a whole, half, quarter, eighth, sixteenth, thirty-second, sixty-fourth and hundred-twenty-eighth note is a whole number of ticks.**

*Check 1: PPQ 3360 divides every 3:2, 5:4 and 7:4 from a whole note through a 128th* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
fn main() {
    const PPQ: u128 = 3360;
    assert_eq!(32 * 3 * 5 * 7, PPQ);
    println!("factors 32 3 5 7");
    let notes = [
        "whole",
        "half",
        "quarter",
        "eighth",
        "sixteenth",
        "thirtysecond",
        "sixtyfourth",
        "onetwentyeighth",
    ];
    let mut exact = 0u32;
    for (shift, name) in notes.iter().enumerate() {
        let note = PPQ * 4 / (1u128 << shift);
        let q3 = note * 2;
        let q5 = note * 4;
        let q7 = note * 4;
        assert_eq!(q3.checked_rem(3).unwrap(), 0);
        assert_eq!(q5.checked_rem(5).unwrap(), 0);
        assert_eq!(q7.checked_rem(7).unwrap(), 0);
        let q3 = q3.checked_div(3).unwrap();
        let q5 = q5.checked_div(5).unwrap();
        let q7 = q7.checked_div(7).unwrap();
        exact += 3;
        println!("{name} {note} {q3} {q5} {q7}");
    }
    println!("exact {exact}");
}
```
Expected output: `factors 32 3 5 7 whole 13440 8960 10752 7680 half 6720 4480 5376 3840 quarter 3360 2240 2688 1920 eighth 1680 1120 1344 960 sixteenth 840 560 672 480 thirtysecond 420 280 336 240 sixtyfourth 210 140 1`

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

## Show every 7:4 tuplet from a whole note through a 128th is not a whole tick at PPQ 480, 960 and 3840
**At PPQ 480, 960 and 3840 the 3:2 and 5:4 tuplets of those eight note values are whole ticks, and every 7:4 tuplet of them is not.**

*Check 1: PPQ 480, 960 and 3840 have eight exact 3:2 and 5:4 tuplets and no exact 7:4* · `runs` · edition 2024 · host · bin · jam dependency set · **✔ oracle pass**
```rust
fn main() {
    let notes = [
        "whole",
        "half",
        "quarter",
        "eighth",
        "sixteenth",
        "thirtysecond",
        "sixtyfourth",
        "onetwentyeighth",
    ];
    let mask = (1u32 << 15) - 1;
    println!("u15_max {mask}");
    for ppq in [480u32, 960, 3840, 3360] {
        assert!(ppq <= mask);
    }
    for ppq in [480u128, 960, 3840] {
        let mut c3 = 0u32;
        let mut c5 = 0u32;
        let mut c7 = 0u32;
        for shift in 0..8 {
            let note = ppq * 4 / (1u128 << shift);
            if note.checked_mul(2).unwrap().checked_rem(3).unwrap() == 0 {
                c3 += 1;
            }
            if note.checked_mul(4).unwrap().checked_rem(5).unwrap() == 0 {
                c5 += 1;
            }
            if note.checked_mul(4).unwrap().checked_rem(7).unwrap() == 0 {
                c7 += 1;
            }
        }
        println!("{ppq} t3 {c3} t5 {c5} t7 {c7}");
        assert_eq!(c3, 8);
        assert_eq!(c5, 8);
        assert_eq!(c7, 0);
        for (shift, name) in notes.iter().enumerate() {
            let note = ppq * 4 / (1u128 << shift);
            if note.checked_mul(4).unwrap().checked_rem(7).unwrap() != 0 {
                println!("fail {ppq} t7 {name}");
            }
        }
    }
}
```
Expected output: `u15_max 32767 480 t3 8 t5 8 t7 0 fail 480 t7 whole fail 480 t7 half fail 480 t7 quarter fail 480 t7 eighth fail 480 t7 sixteenth fail 480 t7 thirtysecond fail 480 t7 sixtyfourth fail 480 t7 onetwentye`

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

