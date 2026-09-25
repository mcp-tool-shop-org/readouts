# Rl Measurement Methodology
_auto-created from wave lane_ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

4 techniques · 4 recommended · 3 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 1 | Generations per item, not items, is usually the cheap lever on eval power | eval | both | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Pooled eval statistics measure the item mix as well as the behaviour | eval | both | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Run-to-run variance can exceed the effect being measured | rl | text | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 5 | Aggregate an interval over runs; do not require each run to clear significance | rl | both | paper+measured | ✅ yes | 5 | 5 | ✓ |

## Detail

### Generations per item, not items, is usually the cheap lever on eval power · `recommended` · ▣ measured
**At G=16 completions per item, 80% of the per-item paired-lift variance was binomial sampling noise rather than genuine item heterogeneity — and sampling noise is purchasable with generation.**
Measured decomposition: total paired sd 7.42pp = 6.64pp measurement + 3.31pp heterogeneity floor. Raising G 16 -> 64 took the decision rule's power from 42% to 98.4%. Base is the highest-leverage seat because one base eval is shared by every arm, so its noise never averages away across arms or seeds — and base generates faster than an adapter arm.
- **For the pipeline:** Decompose eval variance before adding items. Spend generation on the shared baseline first. Note the heterogeneity floor is what no amount of generation removes.
- **Method:** eval · **Applies to:** both · **Base:** general · **Kind:** methodology
- **Output license:** commercial **yes** — Methodology.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Measured on rig, not literature: verified against committed receipts in mcp-tool-shop-org/ai-jam-sessions experiments/rollout-arc/p4 (run logs, run.json receipts, and scripts that reproduce the published figures as a method check).
- **Sources:** [ai-jam-sessions p4/scripts/gate-variance.mts, gate-allocation.mts, base-g16-vs-g64.mts](https://github.com/mcp-tool-shop-org/ai-jam-sessions) — Variance decomposition and the measured G=16 vs G=64 comparison on one model and pool. ; [Maximizing the Coefficient of Generalizability in Multi-Facet Decision Studies](https://doi.org/10.1007/BF02291112) — Optimal allocation of conditions per facet under a fixed number of observations per subject — the items x generations problem, solved in 1973.

### Pooled eval statistics measure the item mix as well as the behaviour · `recommended` · ▣ measured
**A metric averaged over every completion in a pool moves when an intervention changes WHICH items contribute, without any per-item behaviour changing. Simpson's paradox in an eval metric.**
It pointed the wrong way three times in one day on one arc: a pooled concentration figure of 0.735 was 0.933 item-wise; a headline 9pp effect halved item-wise and its passing-only variant vanished (survivorship confound on top); and a prompting intervention's apparent 43pp diversity gain decomposed into an UNCHANGED first choice plus enumeration in list positions 2-5.
- **For the pipeline:** Compute the item-wise form (per item, then mean over items, equal weight each) and report both. Compare at MATCHED n — modal-share statistics are biased upward at small sample size (measured: 0.17pp at concentration ~0.93, 0.7pp at ~0.5), and the bias always flatters the new thing. Before any comparison, name the two sets and check membership mechanically.
- **Method:** eval · **Applies to:** both · **Base:** general · **Kind:** methodology
- **Output license:** commercial **yes** — Methodology.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Measured on rig, not literature: verified against committed receipts in mcp-tool-shop-org/ai-jam-sessions experiments/rollout-arc/p4 (run logs, run.json receipts, and scripts that reproduce the published figures as a method check).
- **Sources:** [ai-jam-sessions p4/scripts/opening-per-item.mts, opening-2x2.mts, vs-fileorder-check.mts](https://github.com/mcp-tool-shop-org/ai-jam-sessions) — Pooled vs item-wise decomposition reversed three readings; scripts reproduce the published pooled figures as a method check. ; [Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations](https://arxiv.org/abs/2411.00640) — Eval variance decomposes into immutable between-item variance and within-item sampling variance; conduct inference on question-level paired differences.

### Run-to-run variance can exceed the effect being measured · `recommended` · ▣ measured
**On one deterministic-verifier substrate, three runs of an IDENTICAL configuration differing only in seed produced held-out lifts of +0.60pp, +10.08pp and +3.44pp, and opening-concentration changes spanning 12.3pp.**
Same cell, same 200 steps, same data, differing only in a seed that does not even control adapter initialisation. Effective gradient updates ranged 48-77 of 200 because 62-76% of groups had zero within-group reward variance. Training accuracy did NOT reliably predict held-out lift: the run with the MOST effective updates landed mid-pack.
- **For the pipeline:** Never publish a single-run RL result. Use n>=3 runs and an across-run estimator; a two-point trend is not a trend (a clean-looking correlation over two runs was broken by the third).
- **Method:** rl · **Applies to:** text · **Base:** general · **Kind:** methodology
- **Output license:** commercial **yes** — Methodology.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Measured on rig, not literature: verified against committed receipts in mcp-tool-shop-org/ai-jam-sessions experiments/rollout-arc/p4 (run logs, run.json receipts, and scripts that reproduce the published figures as a method check).
- **Sources:** [ai-jam-sessions experiments/rollout-arc/p4/GATE-RESULTS.md](https://github.com/mcp-tool-shop-org/ai-jam-sessions) — Three seeds, identical config: +0.60 / +10.08 / +3.44pp held-out lift. ; [A Sober Look at Progress in Language Model Reasoning: Pitfalls and Paths to Reproducibility](https://arxiv.org/abs/2504.07086) — Pass@1 standard deviation across seeds is large enough that many reported RL gains sit inside the base model's seed-variance band.

### Aggregate an interval over runs; do not require each run to clear significance · `recommended` · paper+measured
**A decision rule of the form 'every seed's interval must exclude zero' is the Gelman & Stern error — it compares significance across conditions instead of estimating the quantity. It is also badly underpowered.**
A live preregistration used that conjunction rule; computed against its own point estimate it had 42% power, i.e. it would vote DOES-NOT-REPLICATE on a real effect more often than confirm it. Replaced by an across-run mean with a bootstrap resampling BOTH runs and items. At K=2 the two bootstraps disagreed in verdict (items-only excluded zero, runs-and-items did not); the wider one was preregistered and is the honest reading.
- **For the pipeline:** Report a stratified-bootstrap interval aggregated over the run dimension. Always print the items-only and runs-and-items intervals side by side — when they disagree, the narrow one is the trap.
- **Method:** rl · **Applies to:** both · **Base:** general · **Kind:** methodology
- **Output license:** commercial **yes** — Methodology.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Retrieval oracle (arXiv+Semantic Scholar+Crossref, deterministic, no LLM) resolved every citation; groundedness rated SUPPORTED by two lenses from families outside the synthesiser's (qwen3:14b, mistral-small:24b), reasoning stripped. Lens saw abstracts only. Power figure computed from measured per-item variance.
- **Sources:** [The Difference Between 'Significant' and 'Not Significant' is not Itself Statistically Significant](https://doi.org/10.1198/000313006X152649) — Comparing significance across conditions is not the same as estimating the difference. ; [Deep Reinforcement Learning at the Edge of the Statistical Precipice](https://arxiv.org/abs/2108.13264) — In the few-run regime report stratified-bootstrap interval estimates aggregated over runs and robust aggregates, not per-run point estimates or thresholds.

