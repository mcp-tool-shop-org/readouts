# Rl Measurement Methodology
_auto-created from wave lane_ · wave 18 · 2026-10-20 · [‹ catalog index](README.md)

5 techniques · 5 recommended · 4 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 1 | A learned critic's accuracy is a distribution: SFT before ASPIRE showed no reliable effect over three seeds | evaluation | text | ▣ measured |  | 4 | 4 | ✓ |
| 1 | Generations per item, not items, is usually the cheap lever on eval power | eval | both | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Pooled eval statistics measure the item mix as well as the behaviour | eval | both | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 1 | Run-to-run variance can exceed the effect being measured | rl | text | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 5 | Aggregate an interval over runs; do not require each run to clear significance | rl | both | paper+measured | ✅ yes | 5 | 5 | ✓ |

## Detail

### A learned critic's accuracy is a distribution: SFT before ASPIRE showed no reliable effect over three seeds · `recommended` · ▣ measured
**With 32 training prompts, ASPIRE's learned critic varied more between seeds than between treatments: SFT on teacher answers before ASPIRE gave no reliable change in critic accuracy (mean drops 0.06 composite, 0.008 local, under the pre-registered 0.10), while one control critic ranged from 0.425 to 0.866.**
aspire-si, 2026-10-07. Qwen2.5-1.5B student, LoRA r16, critic head on the last hidden layer; teachers Qwen2.5-32B (local) or Qwen + Gemma-4-31B (composite); 32 training prompts; judged on 127 pairs of a strong answer and the same answer with one planted error (pairwise accuracy, ties as half). Seed 42 alone showed control 0.866 [0.787, 0.929] against SFT-then-ASPIRE 0.646 [0.559, 0.732]. Over seeds 42/43/44 the means were 0.698 vs 0.638 (composite) and 0.635 vs 0.627 (local), so under the pre-registered three-seed rule there is no reliable difference. Critic training loss did not predict accuracy: seed 44's best critic (0.764) had loss rising from 0.91 to 1.10. The drift result did replicate: the fine-tune's representation drift points the same way on every seed (cosine 0.98, size 20.2 to 22.8), and ASPIRE's drift opposes it in all six SFT-then-ASPIRE runs (cosine -0.49 to -0.77) and in control ASPIRE too (-0.57 to -0.75), aligning with ASPIRE-after-SFT (+0.67 to +0.81). The SFT itself improved held-out answers by +0.109 [+0.016, +0.203], under its pre-registered 0.2 bar.
- **For the pipeline:** Budget at least three seeds per arm for any learned critic at this scale and pre-register the decision rule; never pick a critic by its training loss; don't avoid SFT-then-preference training on the strength of one run. The drift opposition is the durable lead.
- **Method:** evaluation · **Applies to:** text · **Base:** Qwen · **Kind:** finding
- **Seed:** 42, 43, 44 · **Runs:** 12
- **Variance:** Composite control critic 0.425 to 0.866 across seeds; local control 0.543 to 0.724. A later aspire-si test showed critic initialisation alone can invert a critic, so the 0.425 draw may be an inverted one.
- **Validated under:** aspire-si runs on 2026-10-07; 32 training prompts; 127 planted-error judge pairs on 64 held-out questions.
- **Output license:** commercial **?**
- **Fit:** rig 4/5 · studio 4/5

**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| pairwise-planted-error | pairwise accuracy, mean of 3 seeds | composite control 0.698 vs SFT-then-ASPIRE 0.638; local 0.635 vs 0.627 | mean drop >= 0.10 | — |  |
| held-out-answer-quality | paired gain over 64 questions | +0.109 [+0.016, +0.203] | +0.2 | — |  |

- **Verify:** verdict=confirmed | currency=2026-10-20 | Re-read by the R&D seat on 2026-10-20 against aspire-si's committed run reports at b8ab54d (line numbers in each eval). Receipt check only; no second model family.
- **Sources:** [aspire-si run 1: seeds 42-44](https://github.com/mcp-tool-shop-org/aspire-si/blob/b8ab54d/docs/runs/2026-10-07-run-1-seeds.md) — Per-seed critic accuracies, mean drops 0.06 and 0.008, the seed ranges, the rising loss, and the drift table. ; [aspire-si runs 2-3](https://github.com/mcp-tool-shop-org/aspire-si/blob/b8ab54d/docs/runs/2026-10-07-runs-2-3.md) — The SFT's held-out gain, +0.109 [+0.016, +0.203], under the 0.2 bar. ; [aspire-si: SFT then ASPIRE (seed 42, with its correction note)](https://github.com/mcp-tool-shop-org/aspire-si/blob/b8ab54d/docs/runs/2026-10-07-sft-then-aspire.md) — Seed 42: 0.866 [0.787, 0.929] against 0.646 [0.559, 0.732], one run each; corrected by run 1. ; [rnd: SFT before ASPIRE has no reliable effect on the critic](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-07-sft-before-aspire-weakens-critic.md) — The bench entry this row is promoted from.

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

