# Wave 20 — verification

**Dispatch:** [`dispatch.md`](dispatch.md)

**Runner:** the R&D seat, 2026-10-20.

**Verifier maturity, stated plainly:**
- The R&D seat ran these measurements and re-read their committed outputs. No second model family reviewed the wave.
- They are rig measurements with committed scripts and outputs, so under the studio's proportional-verification rule
  a receipt check is the right depth.

## Result

| row | verdict | checked against |
|---|---|---|
| six libraries pass at compute capability 12.0 | confirmed | rnd `experiments/cuda-python-5090-rung/results/run2-numpy-2.4.6.jsonl` (six passing rows) and `data/env-freeze.txt` (the pins and the 13.4.92 runtime wheels) |
| numba-cuda fails on NumPy 2.5 | confirmed | `results/run1-numpy-2.5.4.jsonl`: numba-cuda's row fails on `row_stack`; run 2 passes on 2.4.6 |
| CuPy's built-in 13.2 runtime | confirmed | `results/cupy-runtime-2026-10-20.txt`, from `scripts/cupy_runtime_check.py`, run under the Publisher's grant; merged in rnd 1.1.23.1.5 (#189) |

## Bench claims and what happened to them

- **Loaded:** all three of the entry's claims. The CuPy claim was unverified on the bench until the 2026-10-20
  follow-up. It is verified in rnd 1.1.23.1.5, before this wave.
- **Run 1's cuda.compute failure** was the test's own error (`reduce_into` takes keyword arguments only). It isn't a
  library finding, so it isn't loaded.

**Net:** 3 rows, 3 confirmed, 0 fabricated.
