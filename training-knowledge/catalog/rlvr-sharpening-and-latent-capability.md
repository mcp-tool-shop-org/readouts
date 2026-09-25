# Rlvr Sharpening And Latent Capability
_auto-created from wave lane_ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

3 techniques · 3 recommended · 0 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 5 | An RLVR pass-rate lift is not licensed to be called new capability | rl | text | paper | ✅ yes | 4 | 5 | ✓ |
| 5 | Plain GRPO sharpens the output prior rather than flattening it | grpo | text | paper+measured | ✅ yes | 5 | 5 | ✓ |
| 5 | Verbalized Sampling as a $0 probe for capability the policy has but never samples | prompting | text | paper+measured | ✅ yes | 5 | 5 | ✓ |

## Detail

### An RLVR pass-rate lift is not licensed to be called new capability · `recommended` · paper
**RLVR improves pass@1 while losing to the base model at large k; the sampled reasoning paths already exist in the base distribution. The debate is live and both sides must be represented.**
The skeptic result is Yue et al. 2025. The strongest rebuttal is Yuan et al. 2026, which argues high-k pass@k is structurally biased against RLVR because it declines from overtraining on already-solved problems, and shows that restricting updates to problems with no observed success can lift Pass@256 above base. ProRL reports boundary expansion at >2000 steps with the largest gains where the base model is weakest.
- **For the pipeline:** Write the lift as a lift. To claim capability you need a discriminating test — the base-Pass@k=0 subset, or atomic-to-composite transfer — not a bigger pass@1. A local Verbalized-Sampling probe is cheap direct evidence about how much re-weightable material the base already has.
- **Method:** rl · **Applies to:** text · **Base:** general · **Kind:** methodology
- **Output license:** commercial **yes** — Methodology.
- **Fit:** rig 4/5 · studio 5/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Retrieval oracle (arXiv+Semantic Scholar+Crossref, deterministic, no LLM) resolved every citation; groundedness rated SUPPORTED by two lenses from families outside the synthesiser's (qwen3:14b, mistral-small:24b), reasoning stripped. Lens saw abstracts only. Both sides of a live disagreement are carried.
- **Sources:** [Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?](https://arxiv.org/abs/2504.13837) — RLVR beats base at k=1 but loses at large k; sampled paths already exist in the base model. ; [Understanding Diversity Collapse in RLVR via the Lens of Overtraining](https://arxiv.org/abs/2606.15455) — High-k pass@k is structurally biased against RLVR; restricting updates to unsolved problems can lift Pass@256 above baseline. ; [ProRL: Prolonged Reinforcement Learning Expands Reasoning Boundaries in Large Language Models](https://arxiv.org/abs/2505.24864) — Prolonged RL over thousands of steps expands the boundary, with the largest gains where the base model is weakest. ; [Spurious Rewards: Rethinking Training Signals in RLVR](https://arxiv.org/abs/2506.10947) — Random rewards produced large gains on Qwen math models but did not transfer to other model families, so a flat random-reward control is family-dependent evidence rather than a universal null.

### Plain GRPO sharpens the output prior rather than flattening it · `recommended` · paper+measured
**Across three independent runs, item-wise concentration on the model's modal output moved +2.44pp [+0.07, +4.82] — excluding zero, positive. Training made the policy MORE mode-locked while improving its pass rate.**
This is the predicted behaviour of a KL-regularised objective at low beta, not a failed run. A single earlier run showing a -9.00pp flattening was an outlier that three replications refused.
- **For the pipeline:** Do not expect an RLVR pass-rate gain to broaden outputs; expect the opposite. If output diversity is the goal, the objective's family has to change (entropy term, divergence choice, or reward), not the sampling scaffold.
- **Method:** grpo · **Applies to:** text · **Base:** general · **Kind:** mechanism
- **Output license:** commercial **yes** — Methodology.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Retrieval oracle (arXiv+Semantic Scholar+Crossref, deterministic, no LLM) resolved every citation; groundedness rated SUPPORTED by two lenses from families outside the synthesiser's (qwen3:14b, mistral-small:24b), reasoning stripped. Lens saw abstracts only. Measured half is three replicated runs.
- **Sources:** [KL-Regularized Reinforcement Learning is Designed to Mode Collapse](https://arxiv.org/abs/2510.20817) — Under standard settings such as a low KL coefficient, the optimal policy is by construction non-diverse. ; [ai-jam-sessions p4/GATE-RESULTS.md](https://github.com/mcp-tool-shop-org/ai-jam-sessions) — Three runs: +2.92 / +3.27 / +1.15pp item-wise concentration, across-run +2.44pp excluding zero.

### Verbalized Sampling as a $0 probe for capability the policy has but never samples · `recommended` · paper+measured
**Asking the model to list K candidates with probabilities revealed that it can produce structurally varied, EQUALLY ADMISSIBLE outputs it otherwise never samples — 2.96 distinct of 5, pass rate 0.1045 against standard sampling's 0.1117.**
Critically, the decomposition matters: the model's FIRST-listed candidate was MORE concentrated than ordinary sampling (0.9790 vs 0.9333), and it assigned a flat 1/K probability to every candidate. So VS does not move the prior — it enumerates a tail beneath an unchanged head. Taken as a pooled number it looked like a 41pp diversity gain and would have redirected a research programme.
- **For the pipeline:** Run this before pricing any expensive diversity intervention. It separates 'the model cannot do X' from 'the model will not sample X', which are different problems with different fixes. Always decompose within-completion vs across-completion before believing the headline.
- **Method:** prompting · **Applies to:** text · **Base:** general · **Kind:** method
- **Output license:** commercial **yes** — Prompting technique; no licence constraint.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Retrieval oracle (arXiv+Semantic Scholar+Crossref, deterministic, no LLM) resolved every citation; groundedness rated SUPPORTED by two lenses from families outside the synthesiser's (qwen3:14b, mistral-small:24b), reasoning stripped. Lens saw abstracts only. Measured half is a 75-item run.
- **Sources:** [Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity](https://arxiv.org/abs/2510.01171) — Mode collapse traces to typicality bias and can be substantially mitigated at inference time by prompting alone, without training. ; [ai-jam-sessions p4/scripts/score-vs.mts, vs-within-vs-across.mts](https://github.com/mcp-tool-shop-org/ai-jam-sessions) — 75-item measurement: within-completion 2.96 distinct of 5; first-candidate concentration 0.9790 vs standard 0.9333; pass 0.1045 vs 0.1117.

