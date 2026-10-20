# Wave 18 — verification

**Dispatch:** [`dispatch.md`](dispatch.md)

**Runner:** the R&D seat, 2026-10-20. It read aspire-si's committed run reports at b8ab54d (`docs/runs/`).

**Verifier maturity, stated plainly:**
- This check reads receipts. No second model family reviewed the wave.
- These are measurements with committed run reports, so under the studio's proportional-verification rule a receipt
  check is the right depth.

## Result

| row | verdict | checked against |
|---|---|---|
| aspire-critic-seed-variance-sft-null | confirmed | `2026-10-07-run-1-seeds.md`:<br>• lines 51–54: the 12 accuracies and the means;<br>• 60–61: the drops 0.06 and 0.008;<br>• 66–68: the ranges;<br>• 73–74: seed 44's loss rising 0.91 → 1.10;<br>• 90–95: the drift table, size 20.2–22.8, cosines −0.49 to −0.77, −0.57 to −0.75 and +0.67 to +0.81.<br>`2026-10-07-runs-2-3.md` lines 47–51: +0.109 [+0.016, +0.203].<br>`2026-10-07-sft-then-aspire.md` lines 89–92: seed 42's intervals. |
| llm-judge-score-both-orders-qwen25-32b | confirmed with a fix | `2026-10-08-kev-confirmation.md`:<br>• line 34: 0.886 (132/149), single 0.685, A 82%;<br>• line 42: 0.898 (114/127), single **0.701**, A 80%;<br>• the Corrections section, which scopes "A for all 127" to text choices and "ties 89" to whole-number scores.<br>`2026-10-07-sft-then-aspire.md` lines 105–109: ties 89/127, right 31 of 38. |

## Corrections made to the bench copy

- **qwen32b-judge-position-bias:**
  - The rnd entry gave 0.685 as the single-choice baseline for both the 149 fresh pairs and the 127 judge-set pairs.
  - The receipts give 0.685 for the 149 and 0.701 for the 127.
  - The rnd entry is corrected on the bench in a follow-up change.

**Net:** 2 rows, 2 confirmed, 1 figure restated against the receipts, 0 fabricated.
