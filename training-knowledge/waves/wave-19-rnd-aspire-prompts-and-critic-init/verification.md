# Wave 19 — verification

**Dispatch:** [`dispatch.md`](dispatch.md)

**Runner:** the R&D seat, 2026-10-20. It read aspire-si's committed run reports at b8ab54d (`docs/runs/`).

**Verifier maturity, stated plainly:**
- This check reads receipts. No second model family reviewed the wave.
- These are measurements with committed run reports and readouts committed before each run, so under the studio's
  proportional-verification rule a receipt check is the right depth.

## Result

| row | verdict | checked against |
|---|---|---|
| aspire-critic-more-prompts-level-not-spread | confirmed | `2026-10-08-step-2.md`:<br>• lines 24–28: the six accuracies, intervals, range 0.181 and means 0.745 / 0.635;<br>• 32–33: rule 1 fails, rule 2 passes;<br>• 55–58: $1.86, $2.24 and $8.03;<br>• 70–71: epoch 1 at about 1.67 min per dialogue per seed, epochs 2 and 3 about 5 min. |
| aspire-critic-init-can-invert-critic | confirmed | `2026-10-08-critic-init.md`:<br>• lines 9–19: the inversion, ranges 0.488 and 0.283, and the one-draw caveat (0.803 and 0.787 differ by 0.016);<br>• 31–36: the six accuracies and intervals;<br>• 40–44: noise floor 0.055 and the rule reading;<br>• 51–52: 0 of 32 dialogues identical;<br>• 65–70: the earlier critics, 0.425 [0.333, 0.516];<br>• 92: $3.85. |
| aspire-found-auditor-holds-on-fresh-pairs | confirmed | `2026-10-08-auditor.md`:<br>• lines 8–10: no role reading, because the shuffled-label control failed;<br>• 12–16 and 20–21: 0.678 [0.582, 0.763] on 149 fresh pairs, 0.685 on the judge set;<br>• 22–25: 0.315 identical locally, 123 of 127 decisions, median difference 0.002, mean gap about 0.01, 24% of pairs within the difference, 0.681 with the noise band. |

## Bench claims and what happened to them

- **Loaded, verified on the bench:** the 128- and 32-prompt accuracies, the cost, the critic-init ranges and the
  inversion, the found Auditor's 0.678, and the 0 of 32 dialogues.
- **Loaded, unverified on the bench:** epoch 1 at about 1.67 min per dialogue. The step-2 report states it (lines
  70–71), so it is verified here.
- **Not loaded:** "the spread comes from critic-head initialisation or student sampling". The bench entry marks it
  superseded by the critic-init test.

**Net:** 3 rows, 3 confirmed, 1 bench-unverified claim verified from the receipts, 1 superseded claim left on the
bench, 0 fabricated.
