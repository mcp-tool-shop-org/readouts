# Wave 18 — verification

**Proportional verification:** these are measurements with committed receipts and on-rig calls, not claims about
outside sources. Each was checked against its primary record when it was filed in rnd, and the figures here were
re-read against those rnd entries when this wave was written (R&D, 2026-10-13). No model verifier ran, and none was
needed: the primary record is the measurement itself.

| Row | Checked against | By, when |
|---|---|---|
| E5 method and the six per-model rows | interlock `receipts/e5-2026-10-13b.jsonl` (at 6e8cab6) and `receipts/e5-2026-10-13c.jsonl` (at cc91aed). rnd collects both with `rnd collect e5 --check`, which reproduces the trimmed records byte for byte. Also the harness `src/interlock/harness/e5.py` at 0db35c8 | R&D, 2026-10-13 |
| E4b | interlock `receipts/e4b-block-2.jsonl` and `receipts/e4b-block-3.jsonl`. R&D recomputed the estimates and intervals from the receipts' per-triplet values | R&D, 2026-10-12 |
| Ollama `num_predict` | the Publisher's direct calls on the rig (2026-10-12) and switchyard #71's recorded fixtures | R&D, 2026-10-12 |
| Prompt-count cost | the Publisher's direct prefill call and E5 run report (2026-10-12) | R&D, 2026-10-12 |
| CUDA stack | commands run on the rig (2026-10-07). The driver update to 617.42 is from E5's preflight record (2026-10-13) | R&D, 2026-10-07 and 2026-10-13 |
| Rented-host checks | aspire-si's pod runs (seeds 43 and 44) and host_check output, as reported to rnd (2026-10-07) | R&D, 2026-10-07 |

**Corrections made while writing:** none.

**Known limits, stated in the rows:**
- E5's edges depend on run-to-run memory readings (about ±250 MiB).
- granite4.1:30b's next window was forecast over, not measured.
- Every figure holds for the Ollama release, driver and settings named in the row.
