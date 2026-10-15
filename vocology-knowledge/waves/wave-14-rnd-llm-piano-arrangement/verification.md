# Wave 14 — verification

**Dispatch:** [`dispatch.md`](dispatch.md)
**Runner:** the R&D seat, 2026-10-13, reading the committed receipts in `ai-jam-sessions` (`src/vocal/arrangements/source/<id>/meta.json` for both arrangements, and PR 109) and re-reading the Kimi K3 License at source.
**Verifier maturity, stated plainly:** this check reads receipts and licence text. No second model family reviewed the wave. Under the studio's proportional-verification rule a receipt check is the right depth for measured facts. The one specialised claim, the licence terms in finding 5, was read at source twice: by ai-jam-sessions and R&D on 2026-10-08, and again by R&D on 2026-10-13.

## Result

| finding | verdict | checked against |
|---|---|---|
| 1. arrangements accepted by machine gates | confirmed | PR 109 (merged 2026-10-08); both meta.json files: temperature 0, reasoning high, finish_reason stop |
| 2. a generated brief | confirmed, restated | Amazing Grace meta.json `brief_note`: hand-written, `\partial 4`, import offset 768 ticks; America the Beautiful's `fixes` is empty |
| 3. cost | confirmed, restated | both `usage` blocks: tokens, reasoning tokens, cost, wall time; the input rate from `cost_details` |
| 4. one-line fixes | confirmed | Amazing Grace `fixes`; America `fixes` empty; the Battle Hymn fix as checked by rnd on 2026-10-08 |
| 5. rights | confirmed | Kimi K3 License (re-read 2026-10-13); OpenRouter Terms and the hymn editions (read 2026-10-08) |

## Corrections made to the bench copy

- **Finding 2.** The rnd entry said the briefs were generated from the score. One was: America the Beautiful's. Amazing Grace's brief was written by hand before `arrange-hymn.ts` existed, and its meta.json says so. This finding states the pair as it is.
- **Finding 3.** The rnd entry gave $0.72 per million input tokens. The receipts bill 1,728 prompt tokens at $0.005184 and 1,956 at $0.005868: $3.00 per million, from the provider Modal. The output rate ($15 per million), the per-arrangement costs and the $3.00 worst case stand.

The rnd entry is corrected in the same change on the bench.

**Net:** 5 findings, 5 confirmed, 2 restated against the receipts, 0 fabricated.
