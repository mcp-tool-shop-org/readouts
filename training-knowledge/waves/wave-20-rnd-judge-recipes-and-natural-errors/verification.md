# Wave 20 — verification

**Dispatch:** [`dispatch.md`](dispatch.md)

**Runner:**
- A Sonnet subagent made the first pass, read-only, on 2026-10-20. It recomputed the rig figures from rnd's committed
  JSON and checked each paper's figures in its abstract or tables.
- The R&D seat then rechecked every correction itself:
  - it recounted the fine-tune's misses from the three `*-confirm.json` files;
  - it re-fetched PoLL's Table 1 and Kim et al.'s abstract;
  - it confirmed all ten paper titles and first authors against the arXiv API;
  - it read the natural-errors README for muse-glimmer and the licences.

**Verifier maturity, stated plainly:**
- This check reads receipts and primary sources. No second model family reviewed the wave.
- The literature rows are the papers' own results, read at the source and not reproduced.

## Result

| row | verdict | checked against |
|---|---|---|
| planted-pair-filters-never-check-the-error | confirmed with a fix | `judge-4b-full-s{0,1,2}-confirm.json`: order-averaged misses 3/2/3 (2 shared); single choice 11/13/12 presentations, 10/12/11 pairs (9 shared). aspire-si `confirm_set.json` edit spans. `clean_dataset.py` `pair_problems`, `build_dataset.py`, `fresh_pairs.py` |
| natural-errors-local-screen-judges | confirmed | natural-errors `gold.json` against `screen.json` and `screen_extra.json`: 59/59, 59/84 (0.702), gemma 57/59 (0.966) and precision 0.722, muse 0.86/0.86 and 68/84, union 78/84; label kappa 0.633; README lines 13–16, 44–57, 83–86 and 149–169 |
| realmistake-llm-error-detection-recall | confirmed | arXiv 2404.03602 abstract and Appendix A.2; the HF dataset card gives cc-by-sa-4.0 |
| felm-factuality-segment-benchmark | confirmed | hkust-nlp/felm README lines 35–38 and 110–119 (CC BY-NC-SA 4.0; code MIT) |
| personas-do-not-improve-factual-accuracy | confirmed | arXiv 2311.10054 abstract |
| self-taught-evaluators | confirmed | arXiv 2408.02666 abstract; section 6.2 |
| prometheus-2-weight-merged-judges | confirmed | arXiv 2405.01535 Table 5 (averaged columns) |
| judgelm-swap-augmentation-and-scale | confirmed | arXiv 2310.17631 Table 5 and the scaling table |
| llm-errors-are-correlated | confirmed with a fix | arXiv 2506.07962 abstract. The 60% is "on one leaderboard dataset" (HELM). |
| judges-favour-similar-models-capa | confirmed | arXiv 2502.04313 abstract |
| poll-panel-of-judges | confirmed with a fix | arXiv 2404.18796 Table 1: the best single judge on TriviaQA is CMD-R 0.902, not Haiku 0.894; on HotpotQA, Haiku 0.873 beats PoLL 0.867 |
| jtt-upweight-errors-worst-group | confirmed | arXiv 2107.09044 abstract |
| easy-to-hard-generalization | confirmed | arXiv 2401.06751 abstract |

## Bench claims and what happened to them

- **Loaded:** 17 verified claims from the two entries, as 13 rows.
- **Not loaded:**
  - the seven unverified claims (literature from memory or search snippets, and two judgement calls);
  - the role-os specialists claim (internal tooling).
- **Corrections:** the single-choice miss range, PoLL's best single judge and its HotpotQA result, and the scope of
  Kim et al.'s 60%. The bench entries are corrected in a follow-up rnd change.
- **Licences and labels:**
  - FELM is CC BY-NC-SA 4.0, internal evaluation only.
  - The natural-errors answers are Llama 3.1 8B outputs (Llama 3.1 Community License), and its questions Mistral
    Small 24B (Apache-2.0).
  - Its labels are Claude-made and serve as an evaluation yardstick, not training targets.

**Fixed after merge (2026-10-20):** the natural-errors row's `measured_conditions` said "labels by two Claude passes". The labelling was one Opus pass and four blind Sonnet passes, with Opus adjudicating. The Publisher caught it after #61 merged.

**Net:** 13 rows, 10 confirmed and 3 confirmed with a fix; 1 title corrected against arXiv; 0 fabricated.
