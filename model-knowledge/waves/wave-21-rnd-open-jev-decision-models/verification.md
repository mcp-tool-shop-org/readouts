# Wave 21 — verification

**Dispatch:** [`dispatch.md`](dispatch.md)

**Runner:** a Sonnet subagent made the first pass, read-only, on 2026-10-20. The R&D seat spot-checked its three
corrections against the sources (the Laya README, the Nimble README, and the token counts in `kev4b.jsonl`).

**Verifier maturity, stated plainly:**
- This check reads receipts and the projects' own pages. No second model family reviewed the wave.
- Rig results with committed receipts, and vendor statements read at the source, call for a receipt check under the
  studio's proportional-verification rule.

## Result

| row | verdict | checked against |
|---|---|---|
| Kev family | confirmed | Kev README lines 10, 13, 32–35, 45–46, 52 and 322; `kev/train.py` line 13 at 5e42a7a (re-fetched) |
| Kev on sense-si | confirmed | rnd `experiments/openjev-vs-jev/results/compare-all.json`: n, base-rate Brier 0.2421, Kev-4B 0.2399, Kev-9B 0.2416, Jev 0.2518, AUCs and CIs, `kev9b-knowledge.auc` 0.4185 [0.317, 0.5227], latency medians 0.428 and 0.511; the determinism files; `kev4b.jsonl` input tokens |
| Kev-4B as a judge | confirmed | aspire-si `docs/runs/2026-10-08-kev-confirmation.md` at b8ab54d, lines 30–34 and 40–41; the 0.75 bar in `judge_kev.py` line 150 |
| the judge fine-tune | confirmed | rnd `experiments/kev-judge-finetune/results/summary.json`, the two `*-second.json` files, README lines 41–53 and 85–123; peak in `env/README.md` |
| Laya | confirmed with a fix | Laya README lines 89, 353–359, 657, 1496, 1501–1546 and 1801; card line 2. The MPS rows are an AMD Radeon Pro Vega II. 0.766 is the authors' own figure for the fine-tuned checkpoint (line 89); line 1546 says that row has no committed result file yet, while the base rows match committed files. |
| Bespoke-Nimble-9B | confirmed with a fix | Nimble README lines 24 and 476–486; card line 28. 90.12% is agreement with reference labels; Jev scores 93.21%. |

## Bench claims and what happened to them

- **Loaded:** the rig claims, plus Kev's, Laya's and Nimble's own statements, read at the source.
- **Settled on the way in:** Kev-4B's 124 of 127, unverified on the bench, is a committed figure in aspire-si's report
  (lines 40–41). It loads; the raw probabilities live outside the repo.
- **Not loaded:**
  - the four OpenJev projects and TypeSafe's terms, which have no committed receipt;
  - Kev-9B's memory figures (prose only);
  - Laya's comparison with Jev: the Jev figures are third-party, never measured by the authors (line 1496).
  - the `--init_from` anecdote.
- **Corrections:** Laya's MPS hardware, Nimble's metric, and Kev's token range. The bench entry is corrected in a
  follow-up rnd change.

**Fixed on review:** the first draft listed Laya's 0.766 as "unmeasured by its authors". That misread the README: "never measured here" (line 1496) is about Jev's figures. The Publisher caught it, and 0.766 now loads as Laya's own statement, with the missing result file stated.

**Net:** 6 rows, 4 confirmed and 2 confirmed with a fix; 3 corrections; 0 fabricated.
