# PPQ 3360 and the u128 tick-to-sample rule, checked — generator packet

Written by the `grok-cursor` seat (`Grok 4.7`) through `scripts/seat_lane.py`; unverified until the wave's verification record says otherwise.

PPQ 3360 is a whole-tick grid for a 3:2, a 5:4, and a 7:4 tuplet of every note from a whole through a 128th; PPQ 480, 960 and 3840 keep the 3:2 and 5:4 tuplets whole and miss every 7:4 tuplet of those notes. tick times 16777215 times 48000 still fits in u128 at tick 422550225262032543670307476 and overflows on the next tick, a floor of 24419973467535932409 days at PPQ 3360, and a carried remainder matches one floor of the span while independent floors drop a sample.

1. 3360 = 32 times 3 times 5 times 7. Note length k from 0 (whole) to 7 (128th) is 3360 times 4 divided by 2^k ticks. One 3:2, 5:4 or 7:4 note is that length times 2/3, 4/5 or 4/7. All 24 quotients are integers; the 128th is 70, 84 and 60 ticks.
2. 480 = 32 times 3 times 5, 960 = 64 times 3 times 5 and 3840 = 256 times 3 times 5. Across the same eight note lengths each of those PPQs has 8 exact 3:2 values, 8 exact 5:4 values and 0 exact 7:4 values. All four PPQs fit in midly's 15-bit Timing::Metrical field, whose mask is 32767.
3. The lane's slowest SMF tempo is 0xFFFFFF microseconds per quarter, and midly u24's mask (1 << 24) - 1 is that same integer. The factor is 16777215 times 48000 = 805306320000. The largest fitting tick is u128::MAX divided by that factor. u64::MAX times the factor still fits, so a 64-bit tick argument cannot overflow the product.
4. Two successive one-tick segments at tempo 16777215, with the remainder carried, produce 479, 3355, 1677 and 419 samples at PPQ 3360, 480, 960 and 3840. Summing each segment's own floor is one sample lower on every one of those grids.
5. The same floor, compiled as a wasm32-unknown-unknown cdylib, exports tick_to_sample(u64, u64, u64) -> u64. One quarter at 1000000 microseconds per quarter and PPQ 3360 returns 48000. A zero PPQ makes checked_div return None, and tick_to_sample_status returns 1 instead of panicking.
