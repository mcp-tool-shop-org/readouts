# Training evaluation & validation methodology
_How to attest a trained adapter with receipts. Diffusion STYLE eval (CMMD/HPSv2/PickScore/LPIPS + ai-eyes A/B, not DreamBooth subject metrics); LLM eval via pinned lm-eval-harness + a bias-controlled DIFFERENT-FAMILY judge. Never a bare FID/CLIP scalar. Eval tool-as-software->tensor-engine._ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

44 techniques · 10 recommended · 1 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 1 | Diffusion style-fidelity eval panel — MEASURED (CLIP-sim + CMMD, n=20) on the wave-4 SDXL LoRAs | lora | diffusion | ▣ measured | ✅ yes | 5 | 5 | ✓ |
| 2 | Acceptance threshold calibration + bare-scalar ban (delta-vs-base, pre-declared, held-out) | diffusion-acceptance-gating | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Bias-controlled different-family LLM judge (order-swap + length-match) | dpo | llm | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 2 | Diffusion style-LoRA eval panel (CMMD + HPSv2 + PickScore + LPIPS-vs-exemplar + ai-eyes A/B) | lora | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Eval acceptance gate: threshold + accepted, never a bare scalar | lora | both | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Metric routing: distribution (CMMD) vs per-image preference (HPSv2/PickScore/ImageReward) vs perceptual-to-exemplar (LPIPS/DreamSim) | diffusion-eval-metric-selection | diffusion | ▸ reproduced | ⚠ cond | 4 | 5 | ✓ |
| 2 | Overfitting & memorization detection (SSCD copy-detection + train-vs-novel-prompt divergence) | diffusion-overfit-detection | diffusion | ▸ reproduced | ✅ yes | 4 | 5 | ✓ |
| 2 | Pinned lm-eval-harness LLM evaluation (task_version / prompt / n_shot / precision / seed) | qlora | llm | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 2 | XY-grid candidate selection (frozen prompt+seed across epochs/ranks/weights) | diffusion-lora-checkpoint-selection | diffusion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 6 | Style-fidelity vs prompt-adherence tradeoff (the LoRA-weight frontier curve) | diffusion-tradeoff-measurement | diffusion | · community | ⚠ cond | 5 | 5 | ✓ |
| 6 | ai-eyes A/B rubric as the bias-controlled visual arbiter (order-swap + criterion-split) | diffusion-human-model-arbiter | diffusion | · community | ✅ yes | 4 | 5 | ✓ |
| 9 | AlpacaEval | evaluation | both | paper | check | 3 | 3 | · |
| 9 | AlpacaEval annotator protocol (same repo §Evaluators) | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Amulet: Putting Complex Multi-Turn Conversations on the Stand with LLM Juries | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Bradley–Terry model | evaluation | both | paper | check | 3 | 3 | · |
| 9 | CLIP+MLP Aesthetic Predictor | evaluation | both | paper | check | 3 | 3 | · |
| 9 | CMMD README CLI eval stack (google-research) | eval | both | paper | check | 4 | 4 | · |
| 9 | Clean First, Align Later: Benchmarking Preference Data Cleaning for Reliable LLM Alignment | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Cohen's kappa | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Diffusers adapter scale 0–1 checkpoint grid | eval | both | docs | check | 4 | 4 | · |
| 9 | DreamSim | evaluation | both | paper | check | 3 | 3 | · |
| 9 | EleutherAI lm-evaluation-harness pinned LLM eval | eval | both | docs | check | 4 | 4 | · |
| 9 | FastChat LLM Judge / MT-Bench | evaluation | both | paper | check | 3 | 3 | · |
| 9 | G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment | evaluation | both | paper | check | 3 | 3 | · |
| 9 | HPSv2 human preference scorer (Wu et al. 2023) | eval | both | paper | check | 4 | 4 | · |
| 9 | HPSv3 | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Human Preference Score v2 | evaluation | both | paper | check | 3 | 3 | · |
| 9 | ImageReward learned T2I preference reward (Xu et al. 2023) | eval | both | paper | check | 4 | 4 | · |
| 9 | Inter-rater reliability | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Judging LLM-as-a-Judge (MT-Bench / Arena) | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges | evaluation | both | paper | check | 3 | 3 | · |
| 9 | LPIPS / PerceptualSimilarity | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Pick-a-Pic open user preference pairs (Kirstain et al. 2023) | eval | both | paper | check | 4 | 4 | · |
| 9 | Pre-SPEC pre-specified eval endpoints | eval | both | paper | check | 4 | 4 | · |
| 9 | Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Prometheus: Inducing Fine-grained Evaluation Capability in Language Models | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Rating Scales in UX (Likert biases) | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Reliability without Validity — LLM-as-judge audit | eval | both | paper | check | 4 | 4 | · |
| 9 | Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias | evaluation | both | paper | check | 3 | 3 | · |
| 9 | SSCD copy-detection | evaluation | both | paper | check | 3 | 3 | · |
| 9 | Spaced repetition / sequenced curriculum hold-with-limit | dataset | both | docs | check | 4 | 4 | · |
| 9 | sklearn common pitfalls — train/test leakage | eval | both | docs | check | 4 | 4 | · |
| 9 | sklearn train/test leakage + learning-curve overfit checks | eval | both | docs | check | 4 | 4 | · |

## Detail

### Diffusion style-fidelity eval panel — MEASURED (CLIP-sim + CMMD, n=20) on the wave-4 SDXL LoRAs · `recommended` · ▣ measured
**A CLIP-image-similarity + CMMD harness scored the 6 wave-4 SDXL LoRAs against the training-style set (n=20/config, 10 held-out subjects x 2 seeds). It quantifies style fidelity and CORRECTED two looked-at reads: DoRA gives NO measurable fidelity gain over LoRA (within noise — not the n=3 'crispest' eyeball), and LoKr is measurably LOWER fidelity (0.673 vs 0.734, ~3.5 SEM) — a real size-vs-fidelity tradeoff, not 'comparable.'**
Method: CLIP ViT-B/32 image embeddings; reference = the 16-image stdstyl cyanotype set; style fidelity = mean cosine of each generation to the reference style centroid; CMMD = CLIP-MMD (median-heuristic bandwidth sigma=0.541) between each config's gen set and the reference set. Grid = 10 held-out subjects x 2 seeds per LoRA (native configs via sdxl_gen_img.py; lycoris configs via the training-sampler --network_weights+--sample_at_first path, since the gen script's lycoris create-from-weights is broken on this 3.4.0/sd-scripts combo). RESULT (CLIP-sim / CMMD, n=20): DoRA 0.7388/0.1613, LoRA 0.7339/0.1610, AdamW8bit 0.7332/0.1740, Prodigy600 0.7215/0.1795, Prodigy400 0.6972/0.1981, LoKr 0.6734/0.2198. FINDINGS: (1) the top four cluster within the noise floor (SEM~0.017 vs inter-config gaps ~0.005) -> optimizer/network choice is ~fidelity-neutral for SDXL style-LoRA; the real differentiators are perf + size (wave 4). (2) LoKr alone is measurably lower (~3.5 SEM) -> 6MB/20x-smaller costs real style fidelity. (3) Prodigy 400<600 (~1 SEM) -> undertraining direction holds. METHODOLOGY LESSON: n=3 mis-ranked DoRA (sampling artifact); ~n>=15 needed to separate close configs.
- **For the pipeline:** Score every candidate style-LoRA with this harness before claiming quality (it caught a looked-at over-claim on first use). Use n>=15; CLIP-sim to the style centroid ~>=0.70 reads as in-style for this set (illustrative, calibrate per style). Gate retrains on it. The harness lives at E:/AI/training/_eval_panel3.py.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** eval-method
- **Seed:** 42 · **Runs:** 20 · **Search:** n=20 per config, 10 held-out subjects x 2 seeds
- **Validated under:** RTX 5090; CLIP ViT-B/32; ref=16-img stdstyl cyanotype set; CLIP-sim-to-style-centroid + CMMD (sigma=0.541); 6 wave-4 SDXL LoRAs. 2026-06-07.
- **Measured receipt (tensor-engine):** `training-kohya-sdxl-lora-proven-blackwell-5090` — the rig-measured it/s + VRAM peak live there, not here.
- **Output license:** commercial **yes** — metric models (CLIP) Apache/MIT; measures only.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| clip_model | openai/clip-vit-base-patch32 | ● |  |
| reference_set | 16-img stdstyl cyanotype | ● | style centroid |
| cmmd_sigma | 0.541 | ○ | median-heuristic bandwidth over the ref set |
| n_per_config | 20 imgs | ○ | 10 held-out subjects x 2 seeds |
| result_DoRA | CLIP-sim 0.7388 / CMMD 0.1613 | ○ |  |
| result_LoRA | CLIP-sim 0.7339 / CMMD 0.1610 | ○ |  |
| result_AdamW8bit | CLIP-sim 0.7332 / CMMD 0.1740 | ○ |  |
| result_Prodigy600 | CLIP-sim 0.7215 / CMMD 0.1795 | ○ |  |
| result_Prodigy400 | CLIP-sim 0.6972 / CMMD 0.1981 | ○ |  |
| result_LoKr | CLIP-sim 0.6734 / CMMD 0.2198 | ○ | lowest fidelity, worst CMMD — the 6MB tradeoff |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| close configs ranked confidently from a few samples | subject variance (sigma~0.076) swamps inter-config gaps (~0.005) at small n | use n>=15 (SEM~0.017); only trust gaps > ~2 SEM | sample-size |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | CLIP-sim-to-style-centroid | 0.7339 | >=0.70 | ✓ | clip-vit-b32 |
| diffusion-style | CLIP-sim-to-style-centroid | 0.6734 | >=0.70 | ✗ | clip-vit-b32 |
| diffusion-style | CLIP-sim-to-style-centroid | 0.6972 | >=0.70 | ✗ | clip-vit-b32 |

- **Best for:** quantify style-LoRA fidelity + gate retrains (eval, fit 5)
- **Verify:** verdict=confirmed | currency=measured 2026-06-07 | direct rig run; the harness corrected a wave-4 looked-at claim on first use (the oracle is the measurement)
- **Sources:** [training-knowledge wave-5 eval panel (n=20, 6 LoRAs)](https://github.com/mcp-tool-shop-org/readouts) — rig-run 2026-06-07; _eval_panel3.py + _eval_panel3.json ; [Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) (Jayasumana et al., 2024) — CLIP-MMD is a more reliable distribution metric than FID ; [Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020) (Radford et al., 2021) — CLIP image embeddings; the basis for the similarity + CMMD metrics

### Acceptance threshold calibration + bare-scalar ban (delta-vs-base, pre-declared, held-out) · `recommended` · ▸ reproduced
**Every diffusion-LoRA acceptance threshold is CALIBRATED once from a base-vs-known-good run, expressed as a DELTA vs the base under identical conditions, pre-declared before the candidate is scored, and pinned — and no eval may emit a verdict carrying a bare scalar without (threshold, accepted, held-out-and-overlap-checked, delta-vs-base).**
Wave-1 established the bare-scalar ban as a principle; this technique is the CALIBRATION METHOD that makes the thresholds defensible and non-circular, and extends the ban to the new wave-3 metrics (DreamSim, SSCD, frontier-knee, swap-agreement). The problem with absolute thresholds: CMMD/HPSv2/PickScore/DreamSim absolutes are not portable across styles, resolutions, or scorer versions, so 'CMMD < 0.4' means nothing on its own. The discipline: (1) CALIBRATE PER STYLE from a reference run — take the base model and a KNOWN-GOOD adapter (or a held-out batch of canon exemplars) under the exact eval conditions, measure each metric, and set the threshold as the DELTA the candidate must beat (e.g. 'CMMD-to-style must drop by >= X vs base', 'ImageReward must not fall below base by more than Y', 'max SSCD-to-training < Z', 'frontier knee exists with style-gate and adherence-gate both met'); (2) PRE-DECLARE — thresholds are written down BEFORE the candidate is scored, never back-fit to make a given run pass (the cardinal calibration sin); (3) DELTA-VS-BASE under identical conditions — same prompt panel, seed, sampler, resolution, scorer version — because only the delta is portable; re-run the base locally, never copy a published base number; (4) HELD-OUT + OVERLAP-CHECKED — the eval panel must be contamination-checked against the training corpus (train_eval_overlap_checked on the dataset row), or the scores report memorization not capability; (5) BARE-SCALAR BAN — the readout layer REFUSES to render a green/pass for any axis lacking the full tuple, and an adapter shows green only when every HARD axis (the SSCD memorization gate and the frontier-knee existence are hard; preference axes can be soft/advisory) has accepted=1. This is the ANDON gate the whole lane funnels into: accepted=0 on any hard axis halts the ship and bad output never propagates downstream. Thresholds live with the eval, version-stamped to the scorer version (a scorer upgrade invalidates old absolute thresholds — re-calibrate).
- **For the pipeline:** sdlab's eval pack stores a per-style threshold MANIFEST (metric -> calibrated delta, scorer version, calibration-run id) that is loaded before scoring and cannot be edited by the scoring run. The readout renders green only when every hard-axis tuple is complete and accepted=1; a bare number renders as 'uncalibrated — no verdict', never as a pass. SSCD-to-training and frontier-knee-exists are the hard ANDON axes (memorization and unusable-tradeoff are ship-blockers); CMMD/preference deltas are the soft quality axes. A scorer-version bump flags all absolute thresholds stale and forces re-calibration.
- **Method:** diffusion-acceptance-gating · **Applies to:** diffusion · **Base:** SDXL / Flux · **Kind:** eval-method
- **Validated under:** All diffusion-LoRA eval axes (CMMD, HPSv2, PickScore, ImageReward, DreamSim, LPIPS, SSCD, frontier-knee, ai-eyes swap-agreement). Thresholds calibrated per style from a base-vs-known-good reference run under pinned conditions; deltas, not absolutes; held-out panel with train_eval_overlap_checked=1; scorer-version-stamped. Non-portability of absolute generative-eval scores is reproduced from Jayasumana 2024 (FID/CMMD) and the broader eval-setup-sensitivity literature.
- **Base model (model-knowledge):** `sdxl-base / flux-dev`
- **Output license:** commercial **yes** — Pure process discipline over the cited instruments; no redistribution or licensing concern. The calibration manifest is internal studio data.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| precision | calibrate and evaluate at the precision the adapter ships at | ● | scoring at a different precision than ship measures a different model |
| resolution | calibration and candidate eval at identical resolution px | ● | absolute metric values shift with resolution; thresholds are resolution-specific |
| seed | calibration run and candidate run share the frozen seed set | ● | delta-vs-base requires identical sampling |

- **Datasets:** Frozen eval prompt+seed panel (style-LoRA acceptance) (eval, license studio-internal (curated prompts; no third-party image redistribution)) ; Threshold calibration reference (base + known-good run) (reference, license studio-internal)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| threshold set after seeing the score so the run 'passes' | back-fitting thresholds to the candidate (circular gating) | pre-declare thresholds from a separate calibration run before scoring the candidate; store them in a manifest the scoring run can't edit | acceptance_gate |
| absolute threshold from one style fails wildly on another | absolute generative-eval scores are not portable across styles/resolutions/scorer versions | express thresholds as delta-vs-base under identical conditions, re-calibrated per style and per scorer version | acceptance_gate |
| adapter passes the gate but had seen eval prompts/images in training | eval panel not contamination-checked against the training corpus | set train_eval_overlap_checked=1 on the eval dataset before any threshold means anything | train_eval_overlap_checked |
| readout shows a green pass next to a single CMMD number | bare scalar rendered as a verdict | render green only with the full (threshold, accepted, held-out-overlap-checked, delta-vs-base) tuple; bare number = 'no verdict' | readout_render |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| acceptance-gate | per-axis (threshold, accepted, delta-vs-base) tuple completeness; hard-axis accepted=1 | green only when every hard axis accepted=1 with full tuple | SSCD-to-training under replication limit AND frontier-knee exists are HARD (must pass); CMMD/preference deltas above pre-declared margins are soft/advisory | ✓ | n/a (gating logic over instrument outputs) |

- **Best for:** make every eval number a binding gate instead of a vibe (acceptance-gate, fit 5) ; keep thresholds honest across styles and scorer upgrades (calibration, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=current | CMMD paper (arXiv:2401.09603) and cmmd-pytorch repo (github:sayakpaul/cmmd-pytorch) confirmed real. Datasheets for Datasets (arXiv:1803.09010) confirmed real; PARTIAL citation rating is correct (it supports the train/eval overlap precondition by analogy, not directly). Near-dedup with wave-1 'Eval acceptance gate: threshold + accepted, never a bare scalar': the core ban on bare scalars is restated. However, the extensions — calibration-from-base-vs-known-good, delta-vs-base expression, pre-declaration, scorer-version pinning as invalidation trigger — are genuine new depth not in wave-1. Fix: restructure the claim to lead with the calibration methodology (delta-vs-base, pre-declaration, version-pinning) and explicitly frame the bare-scalar ban as a prerequisite already in wave-1, not the new contribution.
- **Sources:** [Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) (Sadeep Jayasumana et al., 2024) — absolute generative-eval scores (FID) are biased and non-portable across sample sizes/setups — the reason thresholds must be deltas vs base under identical conditions ; [cmmd-pytorch — reference implementation (scorer-version-stamped CMMD)](https://github.com/sayakpaul/cmmd-pytorch) (Sayak Paul, 2024) — CMMD is computed from a specific CLIP backbone + kernel; the scorer version is part of the number, so a backbone change invalidates old absolute thresholds — re-calibrate ; [Datasheets for Datasets — provenance + intended-use disclosure (train/eval overlap)](https://arxiv.org/abs/1803.09010) (Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan, Hanna Wallach, Hal Daumé III, Kate Crawford, 2021) — documenting dataset provenance and intended use (incl. train/eval separation) is required for a score to mean capability rather than contamination — basis for the train_eval_overlap_checked precondition

### Bias-controlled different-family LLM judge (order-swap + length-match) · `recommended` · ▸ reproduced
**When an LLM judges fine-tune quality, the judge MUST be a different model family from the model-under-test, with position swapped and length matched — or the verdict is biased.**
The pairwise/preference acceptance gate for an LLM fine-tune (especially after DPO/ORPO/KTO/SimPO preference training, where task-accuracy harnesses don't capture the win). Zheng 2023 (MT-Bench / Chatbot Arena) documents three judge biases that must be controlled: POSITION bias (judges favor the first-presented answer), VERBOSITY bias (judges favor longer answers regardless of quality), and SELF-ENHANCEMENT bias (judges favor outputs from their own family). Wataoka 2024 refines the third: the mechanism is FAMILIARITY (judges over-reward low-perplexity / in-distribution text), so a same-family judge systematically inflates a same-family model-under-test. Controls: (1) DIFFERENT-FAMILY judge — never let a model (or its sibling) judge itself; this is the EXTERNAL_VERIFIER standard for the LLM lane; (2) ORDER-SWAP — present each A/B pair in both orders and only count agreement (a verdict that flips on swap is a position artifact, discarded); (3) LENGTH-MATCH — constrain or normalize for response length so verbosity isn't rewarded. Report win-rate with the swap-agreement rate and the length distribution, plus a threshold. The judge is CITED as an instrument; it is run at inference and is not the model being shipped. Pairs with the workflow-standards EXTERNAL_VERIFIER rule (no model verifies its own output; verifier is a different family).
- **For the pipeline:** The studio's LLM eval pack runs a local NON-generator-family judge (e.g. if the fine-tune is Qwen-family, judge with a Mistral/Llama/Granite-family local model on the rig), always order-swapped and length-controlled, and reports swap-agreement alongside win-rate. A win that only holds in one presentation order, or only because answers are longer, is not a win.
- **Method:** dpo · **Applies to:** llm · **Base:** Qwen3 · **Kind:** eval-method
- **Tuning budget:** none — protocol; the choices are which different-family judge to seat and the length-control method. · **Search:** none
- **Variance:** Position and verbosity biases make a single-order, length-unmatched judgment unreliable; swap-agreement quantifies the residual position artifact. Self-preference/familiarity bias (Wataoka 2024) means a same-family judge's verdict is confounded and cannot be trusted as the acceptance signal.
- **Validated under:** Pairwise base-vs-trained (or candidate-vs-candidate) comparison of a local LLM fine-tune, judged by a different-family local model, every pair scored in both orders with response length matched/normalized.
- **Base model (model-knowledge):** `qwen3-32b`
- **Output license:** commercial **yes** — The judge model is used only at inference for evaluation and does not enter the fine-tune's weights or license. Choose a commercially-licensed local judge so the eval pipeline itself stays commercial-clean.
- **Fit:** rig 5/5 · studio 4/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Judge declares the fine-tune a clear winner but the verdicts flip when A/B order is swapped | Position bias — judge favored whichever answer was shown first | score both orders, count only swap-consistent verdicts, report swap-agreement | eval_prompt |
| Fine-tune wins but its answers are consistently much longer | Verbosity bias — judge rewards length, not quality | length-match / normalize responses before judging; report length distribution | eval_prompt |
| Same-family judge rates the same-family fine-tune very highly; a different judge disagrees | Self-preference / familiarity bias (low-perplexity preference) | always use a different-family judge as the acceptance signal | judge_model_family |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| llm-judge | pairwise win-rate (trained vs base) | win-rate + swap-agreement rate + length distribution | win-rate > 0.5 vs base AND swap-agreement >= a fixed bar (e.g. 0.8) AND response-length matched (no verbosity confound) | ✓ | different from the model-under-test (e.g. Mistral/Llama/Granite judging a Qwen fine-tune) |

- **Best for:** Attest a preference-trained (DPO/ORPO/KTO/SimPO) LLM fine-tune where task accuracy is not the goal (llm, fit 5) ; Provide the EXTERNAL_VERIFIER seat for LLM fine-tunes (llm, fit 5)
- **Verify:** verdict=confirmed | currency=Current. Both papers (2023, 2024) are active references; the different-family judge design is the consensus mitigation as of 2026. | Both sources verified. Zheng et al. 2023 (arXiv:2306.05685) confirms position, verbosity, and self-enhancement biases in LLM judges and the >80% human agreement finding. Wataoka et al. 2024 (arXiv:2410.21819, accepted NeurIPS 2024 Safe Generative AI Workshop) confirms the familiarity/perplexity mechanism driving self-preference bias. Authors and year are correct. Claims are supported. Boundary clean.
- **Sources:** [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) (Zheng, Chiang, Sheng, Zhuang, Wu, Zhuang, Lin, Li, Li, Xing, Zhang, Gonzalez, Stoica, 2023) — LLM judges exhibit position bias, verbosity bias, and self-enhancement bias; strong judges agree with humans >80% but the biases must be mitigated (e.g. swapping positions) for the verdict to be reliable. ; [Self-Preference Bias in LLM-as-a-Judge](https://arxiv.org/abs/2410.21819) (Wataoka, Takahashi, Ri, 2024) — LLM judges assign higher scores to lower-perplexity (more familiar) outputs regardless of authorship; self-preference bias is driven by familiarity, motivating a different-family judge as the unbiased choice.

### Diffusion style-LoRA eval panel (CMMD + HPSv2 + PickScore + LPIPS-vs-exemplar + ai-eyes A/B) · `superseded` · ▸ reproduced
**Attest a STYLE LoRA with a multi-metric panel (distributional CMMD + preference HPSv2/PickScore + exemplar LPIPS + human A/B), never a bare FID or CLIP scalar.**
The acceptance panel for a trained SDXL/Flux STYLE adapter (style transfer, not DreamBooth subject fidelity). Four complementary axes, each with a threshold: (1) CMMD (Jayasumana 2024) replaces FID as the distributional 'does the output set match the target style distribution' metric — CLIP-MMD embeddings, unbiased, sample-efficient, so it works on the small generated sets a single-GPU studio produces (FID is biased at low N and contradicts human raters); (2) HPSv2 and PickScore are CLIP-based human-preference scorers giving a per-image preference signal that is responsive to algorithmic improvement, scored over a FIXED held-out prompt set; (3) LPIPS (Zhang 2018) computed against a curated style EXEMPLAR plate measures perceptual closeness to the intended look (lower = closer) — read as a band, not minimized, since LPIPS->0 means replication/overfit; (4) the studio ai-eyes A/B rubric is the human/different-model arbiter that breaks ties and vetoes. Run the SAME prompt set + seed at base-vs-LoRA and at candidate checkpoints; report deltas, not absolutes. No single metric is sufficient: CMMD is distributional (blind to per-image quality), preference scorers reward generic aesthetics (can mask off-style drift), LPIPS-to-exemplar can be gamed by near-copying — the panel cross-checks them.
- **For the pipeline:** sdlab's eval pack should emit all four numbers + the ai-eyes verdict for every candidate checkpoint over one frozen prompt list and seed, so checkpoint selection is a receipt, not a vibe. CMMD over FID specifically because the studio generates small eval sets on one GPU where FID is unreliable. LPIPS is reported as an overfit GUARD (a too-low value flags replication) as much as a closeness score.
- **Method:** lora · **Applies to:** diffusion · **Base:** SDXL · **Kind:** eval-method
- **Tuning budget:** none — this is the measurement protocol, not a trained model; the only 'search' is choosing thresholds per style from a base-vs-trained calibration run. · **Search:** none
- **Variance:** CMMD is sample-efficient and an unbiased estimator (Jayasumana 2024) so it is stable at low N where FID is not; HPSv2/PickScore are deterministic given fixed images+prompts; LPIPS varies with the chosen exemplar plate, so the exemplar set must be pinned per style. Re-run on a fixed seed + prompt list to make deltas comparable across checkpoints.
- **Validated under:** SDXL/Flux style LoRAs, small studio-scale generated eval sets, fixed held-out prompt list + pinned seed, scored at base vs trained and across checkpoints. NOT validated for DreamBooth subject-identity eval (use subject metrics there).
- **Base model (model-knowledge):** `sdxl-base-1.0`
- **Output license:** commercial **yes** — All four instruments are research/eval tooling, not training inputs: CMMD (Apache-2.0 ref impl), LPIPS (BSD-2 ref impl), HPSv2 and PickScore weights are evaluation scorers run at inference — they do not touch the LoRA's weights or the LoRA's license. The eval EXEMPLAR plate must itself be commercial-clean (it is canon-bound studio art); license follows the dataset row.
- **Fit:** rig 5/5 · studio 5/5
- **Datasets:** Held-out style eval set (frozen prompt list + pinned style-exemplar plate) (eval, license studio-internal canon art (commercial-clean by construction); the exemplar plate's license follows the canon-bound source it is drawn from)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| All four numbers look fine but outputs are clearly off-style to the director | Preference scorers reward generic aesthetics and can mask style drift; CMMD is distributional and blind to per-image semantics | ai-eyes A/B is the tiebreak/veto — never ship on automated scores alone | eval_panel |
| Exemplar-LPIPS is extremely low and CMMD is excellent | LoRA is replicating training images, not learning transferable style (overfit) | treat low exemplar-LPIPS as a FAILURE band; reduce repeats/steps/rank or broaden the dataset and re-eval | epochs |
| Metrics swing wildly between eval runs of the same checkpoint | Eval prompt set or seed not pinned; small N makes FID-like metrics noisy | pin prompt list + seed; use CMMD (unbiased at low N) instead of FID | seed |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| diffusion-style | CMMD | report as base-vs-trained delta over a fixed prompt set | trained-set CMMD-to-target-style materially below base-set CMMD-to-target-style (per-style calibrated; lower is better) | ✓ | CLIP (distributional, no LLM judge) |
| diffusion-style | HPSv2 | mean HPSv2 over the fixed prompt set, trained vs base | trained mean HPSv2 >= base mean (no preference regression) AND no per-prompt cliff | ✓ | CLIP fine-tuned on HPD v2 preference data |
| diffusion-style | PickScore | PickScore win-rate trained-vs-base over the fixed prompt set | trained win-rate vs base > 0.5 (preferred more often than the base it was trained from) | ✓ | CLIP fine-tuned on Pick-a-Pic preferences |
| diffusion-style | LPIPS | mean LPIPS of trained outputs vs the pinned style-exemplar plate | inside a per-style BAND — low enough to be on-style, but NOT near-zero (near-zero = replication/overfit, a failure) | ✓ | AlexNet/VGG deep features (perceptual, no LLM judge) |
| human-ab | ai-eyes A/B rubric | rubric verdict per A/B pair (base vs trained, and checkpoint vs checkpoint) | ai-eyes A/B prefers the trained adapter AND raises no canon/style-bleed veto | ✓ | vision model + human director (different family from the generator) |

- **Best for:** Attest a trained SDXL/Flux style LoRA with receipts before shipping it into the pipeline (diffusion, fit 5) ; Select the best checkpoint across a training run (sdxl, fit 5) ; Catch style-overfit / training-image replication (diffusion, fit 4)
- **Verify:** verdict=confirmed-with-fixes | currency=Current as of 2026. CMMD (2024) and HPSv2/PickScore (2023) are the active standard; LPIPS (2018) is a durable foundational metric still in wide use. No supersession. | All four papers are real and the claims they are cited for are supported. One citation error: the HPSv2 paper (2306.09341) is attributed to 'Wu, Hao, Sun, Zhang, Li, Wang, Li, Wong, Wang, Li' (10 names) but the actual authors are Wu, Hao, Sun, Chen, Zhu, Zhao, Li (7 names). The names 'Zhang, Wang, Wong, Wang' do not appear on the paper. The paper and its findings are genuine; the author list in the KB is fabricated/inflated and should be corrected to match the actual byline. No boundary violations — eval metrics are correctly framed as evaluation craft, not weight cataloguing or rig-measured numbers.
- **Sources:** [Rethinking FID: Towards a Better Evaluation Metric for Image Generation](https://arxiv.org/abs/2401.09603) (Jayasumana, Ramalingam, Veit, Glasner, Chakrabarti, Kumar, 2024) — CMMD (CLIP embeddings + MMD with Gaussian RBF kernel) is an unbiased, sample-efficient estimator; FID is biased at low sample sizes, contradicts human raters, and fails to reflect gradual improvement of text-to-image models. ; [Human Preference Score v2: A Solid Benchmark for Evaluating Human Preferences of Text-to-Image Synthesis](https://arxiv.org/abs/2306.09341) (Wu, Hao, Sun, Zhang, Li, Wang, Li, Wong, Wang, Li, 2023) — HPSv2 (CLIP fine-tuned on 798K preference choices over 433K image pairs) generalizes better than prior metrics across image distributions and is responsive to algorithmic improvements of text-to-image models. ; [Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation](https://arxiv.org/abs/2305.01569) (Kirstain, Polyak, Singer, Matiana, Penna, Levy, 2023) — PickScore (CLIP-based scorer trained on Pick-a-Pic) predicts human preferences with superhuman performance and correlates with human rankings better than other automatic metrics; recommended for evaluating text-to-image models. ; [The Unreasonable Effectiveness of Deep Features as a Perceptual Metric](https://arxiv.org/abs/1801.03924) (Zhang, Isola, Efros, Shechtman, Wang, 2018) — LPIPS (deep-feature distance) matches human perceptual similarity judgments far better than PSNR/SSIM; provides a perceptual distance usable as a closeness metric or perceptual loss.

### Eval acceptance gate: threshold + accepted, never a bare scalar · `recommended` · ▸ reproduced
**Every training eval carries an explicit acceptance THRESHOLD and a pass/fail bit on a CONTAMINATION-checked held-out set — a score without a bar is not a receipt.**
The cross-cutting discipline that ties every other eval in this lane together (the ANDON/UNCERTAINTY-gate seam). Three rules: (1) every recorded metric MUST be paired with a pre-declared threshold and an accepted (0/1) bit — a bare CMMD/CLIP/HPSv2/lm-eval number is not an attestation, only a threshold makes it a gate that can HALT a ship; (2) eval runs on a HELD-OUT set that has been contamination/train-eval-overlap checked (the Datasheets train_eval_overlap_checked flag on the dataset row) — a model evaluated on data it trained on reports memorization, not capability; (3) report DELTA vs the base under identical conditions, since absolute scores are not portable (FID is biased at low N per Jayasumana 2024; LLM scores are setup-sensitive per Biderman 2024). The gate is binding: if accepted=0 on any hard axis, the adapter does not enter the pipeline — bad output never propagates downstream. Thresholds are calibrated once per style/task from a base-vs-known-good run and then pinned; they are deliberately set, not back-fit to make a given run pass.
- **For the pipeline:** sdlab eval packs and the LLM eval block both refuse to emit a 'pass' without (threshold, accepted, held-out-and-overlap-checked, delta-vs-base). This is the single gate the readout layer surfaces: an adapter shows green only when every hard-axis accepted=1. Thresholds live with the eval, not in someone's head.
- **Method:** lora · **Applies to:** both · **Base:** SDXL · **Kind:** protocol
- **Tuning budget:** threshold-setting only — calibrate per style/task from one base-vs-known-good run; do not re-tune the threshold to pass a failing candidate. · **Search:** manual
- **Variance:** Because absolute scores are setup- and sample-size-sensitive (Jayasumana 2024 for diffusion FID; Biderman 2024 for LLM tasks), thresholds are defined on DELTAS vs a pinned base under identical conditions, which is the stable quantity.
- **Validated under:** Applies to both lanes: diffusion style panel and LLM harness/judge. Requires a held-out eval set with train_eval_overlap_checked=1 and pinned thresholds expressed as deltas vs base.
- **Output license:** commercial **yes** — Pure methodology; no licensing surface of its own. The held-out eval set inherits the dataset row's license (must be commercial-clean if any generated artifacts are retained).
- **Fit:** rig 5/5 · studio 5/5
- **Datasets:** Held-out style eval set (frozen prompt list + pinned style-exemplar plate) (eval, license studio-internal canon art (commercial-clean by construction); the exemplar plate's license follows the canon-bound source it is drawn from)

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| A readout shows a metric value but no one can say if it passed | Score recorded without a pre-declared threshold | every metric row carries (threshold, accepted); no bare scalars | eval_threshold |
| Adapter aces eval then underperforms in real use | Train/eval overlap — evaluated on memorized data | score on a held-out set with train_eval_overlap_checked=1; dedup eval against train | train_eval_overlap_checked |
| Threshold quietly lowered so a weak run 'passes' | Back-fitting the bar to the candidate | calibrate + pin thresholds from a base-vs-known-good run BEFORE evaluating candidates | eval_threshold |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| human-ab | acceptance gate (composite) | per-axis (metric, threshold, accepted) tuple + overall ship/hold | ALL hard-axis accepted=1 on a contamination-checked held-out set, scored as delta vs base | ✓ | different-family judge for the LLM axis; CLIP/perceptual + human for the diffusion axis |

- **Best for:** Turn eval scores into a binding ship/hold receipt (eval, fit 5) ; Prevent eval contamination from faking a pass (eval, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=Current. Threshold-gated acceptance on contamination-checked held-out sets is active best practice as of 2026. | The core claim (explicit acceptance threshold + pass/fail bit on a contamination-checked held-out set) is sound engineering practice. However the 'Datasheets for Datasets' citation (arXiv:1803.09010, Gebru et al. 2021) is tangential and does not directly support it. That paper is about dataset documentation standards (motivation, composition, collection, intended uses) — it does not establish held-out split discipline, contamination-checking, or threshold-based acceptance gates. The citation is being used to launder a reasonable claim through a paper that does not make that argument. The Biderman 2024 and Jayasumana 2024 citations are more relevant but still indirect. Recommended fix: replace or supplement the Datasheets citation with a source that directly argues for contamination-checked evaluation splits and threshold discipline (e.g. the BIG-bench paper, Srivastava et al. 2022, or the HELM paper, Liang et al. 2022, both of which address held-out and contamination protocol directly). The evidence_strength='reproduced-from-source' is acceptable for the Biderman/Jayasumana legs but is weak for the Datasheets leg.
- **Sources:** [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) (Gebru, Morgenstern, Vecchione, Vaughan, Wallach, Daumé III, Crawford, 2021) — A dataset should document its composition, collection, and intended uses (the datasheet), which grounds the train/eval-overlap and held-out discipline the acceptance gate enforces. ; [Lessons from the Trenches on Reproducible Evaluation of Language Models](https://arxiv.org/abs/2405.14782) (Biderman, Schoelkopf, et al. (EleutherAI), 2024) — Reliable LLM evaluation requires reporting setup and comparing under identical conditions; absolute scores are not portable across setups, motivating delta-vs-base thresholds. ; [Rethinking FID: Towards a Better Evaluation Metric for Image Generation](https://arxiv.org/abs/2401.09603) (Jayasumana, Ramalingam, Veit, Glasner, Chakrabarti, Kumar, 2024) — FID is biased at low sample sizes and inconsistent across N, so absolute generation scores are unreliable — acceptance should be framed on stable, sample-efficient deltas (e.g. CMMD vs base).

### Metric routing: distribution (CMMD) vs per-image preference (HPSv2/PickScore/ImageReward) vs perceptual-to-exemplar (LPIPS/DreamSim) · `recommended` · ▸ reproduced
**Each style-LoRA question maps to a specific metric FAMILY — 'did the output SET acquire the style distribution' is CMMD; 'is THIS image preferred / does it follow the prompt' is a learned preference scorer (HPSv2 for aesthetic-aligned, PickScore for user-preference ranking, ImageReward for prompt-faithfulness); 'how close is the look to the intended EXEMPLAR' is a perceptual distance (DreamSim for mid-level layout/semantics, LPIPS for low-level texture) — using the wrong family answers a different question.**
Wave-1 listed the four panel axes; this technique is the DECISION RULE for which to read when, plus DreamSim as a net-new mid-level instrument. (a) DISTRIBUTIONAL — CMMD (Jayasumana 2024) is the only family that answers 'does the generated SET match the target style distribution' and is the FID replacement specifically because it is unbiased and stable at ~1k samples, the regime a single-GPU studio lives in; read it for 'did the adapter move the whole output toward the style', blind to per-image quality by design. (b) PER-IMAGE PREFERENCE — three learned scorers that are NOT interchangeable: PickScore (Kirstain 2023, trained on Pick-a-Pic user A/B choices, ~70% accuracy vs 68% expert humans) is the best at predicting which of two images a user PREFERS — use it to RANK candidates; HPSv2 (Wu 2023, CLIP fine-tuned on 798k preference choices) is aesthetic-and-preference aligned and responsive to algorithmic improvement — use it as the general quality axis over a fixed prompt set; ImageReward (Xu 2023, 137k expert comparisons) is the strongest at PROMPT-FAITHFULNESS and artifact penalties — use it specifically when the worry is 'pretty but ignores the prompt'. Route by the question, don't average three correlated-but-different scorers into mush. (c) PERCEPTUAL-TO-EXEMPLAR — distance against a curated style plate: LPIPS (Zhang 2018) is LOW-level (color/texture) and read as a BAND not minimized (LPIPS->0 = replication); DreamSim (Fu 2023, NeurIPS) is the missing MID-level metric — it captures layout, pose, and semantic arrangement that LPIPS is blind to, by fine-tuning concatenated CLIP+OpenCLIP+DINO embeddings on human triplet judgments, so 'does this MATCH the exemplar's composition/feel' is a DreamSim question, 'does it match the exemplar's brushwork' is an LPIPS question. The routing prevents the wave-1 failure where a single number masks an off-axis regression.
- **For the pipeline:** sdlab's eval pack should label each emitted number with the QUESTION it answers, not just the metric name: CMMD->'style-set match (delta vs base)', PickScore->'candidate ranking', HPSv2->'general preference', ImageReward->'prompt faithfulness', DreamSim->'mid-level exemplar match', LPIPS->'low-level exemplar band + overfit guard'. When two scorers disagree (e.g. HPSv2 up but ImageReward down) the readout must SURFACE the disagreement (style improved at the cost of prompt-adherence) rather than collapse to an average. DreamSim is the new addition vs wave-1 and is the right tool for 'matches the look but composition drifted'.
- **Method:** diffusion-eval-metric-selection · **Applies to:** diffusion · **Base:** SDXL / Flux · **Kind:** eval-method
- **Validated under:** SDXL/Flux style LoRAs, small studio eval sets over a fixed prompt panel; CMMD on the generated set, preference scorers per-image over the panel, perceptual distances against a curated exemplar plate. Scorer accuracy figures (PickScore 70.2% vs 68% expert; HPSv2 798k pairs) are from the source papers' held-out benchmarks, not measured on this rig.
- **Base model (model-knowledge):** `sdxl-base / flux-dev`
- **Output license:** commercial **conditional** — CMMD code (sayakpaul/cmmd-pytorch) and DreamSim/LPIPS are permissively usable as evaluation instruments. PickScore/HPSv2/ImageReward weights derive from research datasets (Pick-a-Pic, HPD v2, ImageRewardDB) with research-leaning terms — fine for INTERNAL acceptance gating (you are scoring, not redistributing the scorer or training on it); confirm each model's license before bundling a scorer into a shipped product. Used here strictly as cited instruments, not catalogued or redistributed.
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| resolution | score at the resolution the adapter ships at px | ● | preference scorers and CMMD both shift with input resolution |
| batch_size | CMMD stable from ~1000 generated samples samples | ○ | below ~1k CMMD variance rises; FID is worse — this is why CMMD is the small-set default |

- **Datasets:** Frozen eval prompt+seed panel (style-LoRA acceptance) (eval, license studio-internal (curated prompts; no third-party image redistribution)) ; Curated style exemplar plate (perceptual-distance reference) (reference, license studio-internal canon assets (owned/licensed source art))

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| three preference scorers reported but they just track each other | treating HPSv2/PickScore/ImageReward as redundant aesthetic numbers instead of routing by question | assign each scorer its question (preference / ranking / prompt-faithfulness) and read disagreements as signal | metric_selection |
| LPIPS-to-exemplar looks fine but the composition is clearly off-style | LPIPS is low-level and blind to mid-level layout/semantics | add DreamSim against the exemplar for the mid-level (layout/pose/semantic) axis | perceptual_metric |
| FID used on a few-hundred-image studio eval set gives noisy, contradictory rankings | FID is biased and unstable at low N and can contradict human raters | use CMMD for the distributional axis on small studio sets | distribution_metric |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| distribution | CMMD (CLIP-MMD, generated-set vs target-style-set) | delta vs base reported | CMMD-to-target decreases vs base by a pre-declared margin | ✓ | CLIP-embedding (instrument) |
| preference | PickScore (candidate ranking) + HPSv2 (general preference) + ImageReward (prompt faithfulness) | per-image scores over the fixed prompt panel | trained >= base on each routed axis; ImageReward not regressed when HPSv2 rises | ✓ | CLIP/BLIP-based reward (instrument) |
| perceptual | DreamSim (mid-level) + LPIPS (low-level band) vs exemplar | distance to exemplar in a target band | DreamSim/LPIPS inside the calibrated band (not minimized — a floor catches replication) | ✓ | perceptual (instrument) |

- **Best for:** decide which metric answers a given style-LoRA question (metric-routing, fit 5) ; detect style-improved-but-prompt-broke regressions (tradeoff-detection, fit 4)
- **Verify:** verdict=confirmed-with-fixes | currency=current | All six papers verified real with correct authors/years. The family-routing framing ('wrong family answers a different question') and the DreamSim/LPIPS mid-level vs low-level distinction are genuine new depth beyond wave-1's 'eval panel' entry. However, the technique names the same metric set as wave-1 and risks being read as a restatement. Fix: explicitly note in the KB entry that this extends wave-1 by adding routing logic and cross-family misuse warnings, not merely by listing the same instruments. No evidence_strength overclaim.
- **Sources:** [Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) (Sadeep Jayasumana et al., 2024) — CMMD ranks text-to-image models in agreement with human raters in 92.5% of cases where FID fails, and is stable at ~1000 samples — the distributional metric for small studio sets ; [Pick-a-Pic: An Open Dataset of User Preferences for Text-to-Image Generation (PickScore)](https://arxiv.org/abs/2305.01569) (Yuval Kirstain, Adam Polyak, Uriel Singer, Shahbuland Matiana, Joe Penna, Omer Levy, 2023) — PickScore predicts human preference at 70.2% vs 68.0% expert humans and correlates with human rankings better than other automatic metrics — use it to RANK candidates ; [Human Preference Score v2: A Solid Benchmark for Evaluating Human Preferences of Text-to-Image Synthesis](https://arxiv.org/abs/2306.09341) (Xiaoshi Wu, Yiming Hao, Keqiang Sun, Yixiong Chen, Feng Zhu, Rui Zhao, Hongsheng Li, 2023) — HPSv2 (CLIP fine-tuned on 798k preference choices over 433k pairs) generalizes across distributions and is responsive to algorithmic improvement — the general preference axis ; [ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977) (Jiazheng Xu, Xiao Liu, Yuchen Wu, Yuxuan Tong, Qinkai Li, Ming Ding, Jie Tang, Yuxiao Dong, 2023) — ImageReward (137k expert comparisons) outperforms CLIP/Aesthetic/BLIP scores at modeling human preference and is strongest on prompt-faithfulness/artifact penalties — the prompt-adherence axis ; [DreamSim: Learning New Dimensions of Human Visual Similarity using Synthetic Data](https://arxiv.org/abs/2306.09344) (Stephanie Fu, Netanel Tamir, Shobhita Sundaram, Lucy Chai, Richard Zhang, Tali Dekel, Phillip Isola, 2023) — DreamSim captures MID-level similarity (layout, pose, semantic content) that low-level metrics like LPIPS miss, by fine-tuning CLIP+OpenCLIP+DINO on human triplet judgments — the mid-level exemplar-match axis ; [The Unreasonable Effectiveness of Deep Features as a Perceptual Metric (LPIPS)](https://arxiv.org/abs/1801.03924) (Richard Zhang, Phillip Isola, Alexei A. Efros, Eli Shechtman, Oliver Wang, 2018) — LPIPS measures low-level perceptual (texture/color) distance via deep features — read as a band against the exemplar, not minimized

### Overfitting & memorization detection (SSCD copy-detection + train-vs-novel-prompt divergence) · `recommended` · ▸ reproduced
**A style LoRA is tested for MEMORIZATION by retrieving each generation's nearest training image under SSCD copy-detection embeddings and flagging any pair above the replication threshold, and for OVERFIT by measuring quality divergence between training-caption prompts and held-out NOVEL prompts — a low-LPIPS hero shot is not proof of style; a high SSCD match to a training image is proof of copying.**
Wave-1's only overfit signal was 'LPIPS->0 flags replication'. This technique is the dedicated memorization/overfit protocol, which is BOTH a quality concern (an overfit style LoRA reproduces training compositions instead of generalizing the style) AND a legal/IP concern for a shipping studio (regurgitating a training image is the replication failure that gets diffusion pipelines into trouble). Two complementary tests. (1) COPY-DETECTION RETRIEVAL — generate over the eval prompt panel, embed every generation AND every training image with SSCD (Pizzi 2022, the strongest open replication detector; Somepalli 2023 used SSCD-derived similarity and found generations above ~0.5 SSCD similarity are partial object-level copies of training images, with 0.5-2% of generations duplicating training samples). For each generation, take the max SSCD similarity to any training image; if any generation exceeds the replication threshold, the adapter is memorizing and is REJECTED (ANDON halt) regardless of how good its preference scores are. SSCD beats raw LPIPS/CLIP here because it is purpose-built to catch crops/recolors/partial copies. (2) TRAIN-VS-NOVEL DIVERGENCE — score the panel split into two prompt sets: prompts close to the TRAINING captions vs deliberately NOVEL prompts the style was never described against. A healthy generalizing style scores similarly on both; a large drop on novel prompts (looks great echoing training captions, falls apart on new ones) is overfit — the model learned the training images, not the style. Report the delta between the two sets as the overfit score. Somepalli's mitigation (prompt-token randomization to break memorized prompt->image links) is the upstream FIX when the test trips; the dedup_method on the dataset row (near-dup removal before training) is the prevention.
- **For the pipeline:** sdlab eval packs gain two hard gates beyond the wave-1 panel: a max-SSCD-to-training-set guard (accepted=0 and ANDON-halt if any generation exceeds the replication threshold) and a train-vs-novel divergence score with a max-allowed gap. The training set must be available to the eval pack to compute SSCD retrieval — so the eval references the exact training corpus snapshot (and its dedup receipt). This is where 'is the style trainable AND safe to ship' is actually decided; preference scores can be high on a memorizing adapter, so this gate is independent and binding.
- **Method:** diffusion-overfit-detection · **Applies to:** diffusion · **Base:** SDXL / Flux · **Kind:** eval-method
- **Validated under:** SDXL/Flux style LoRAs, eval generations retrieved against the full training corpus snapshot via SSCD embeddings; novel-prompt split distinct from training captions. SSCD ~0.5 partial-copy threshold and 0.5-2% duplication rate are Somepalli 2023's findings on diffusion models generally — the studio must calibrate its own replication threshold per style on a base-vs-known-good run, not copy 0.5 blindly.
- **Base model (model-knowledge):** `sdxl-base / flux-dev`
- **Output license:** commercial **yes** — SSCD (facebookresearch/sscd-copy-detection) is open and used purely as a detector instrument. This test is ESPECIALLY relevant commercially: it is the studio's evidence that a shipped style adapter does not regurgitate training images, an IP-safety receipt. Used as a cited instrument, not catalogued.
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| epochs | test at each candidate epoch — memorization rises with over-training checkpoints | ● | later epochs are the memorization-risk zone; run SSCD across the epoch axis |
| repeats | high per-image repeats raise memorization risk — re-check SSCD if repeats are high repeats | ○ | duplicated/over-repeated images are the classic memorization driver |
| min_snr_gamma | n/a to this test | ○ | listed only to note this is a detection method, not a training knob |

- **Datasets:** Frozen eval prompt+seed panel (style-LoRA acceptance) (eval, license studio-internal (curated prompts; no third-party image redistribution)) ; Training corpus snapshot (memorization-retrieval reference) (reference, license studio-internal (the exact training set used for the adapter; canon-owned/licensed))

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| adapter scores great on HPSv2/PickScore but reproduces a recognizable training composition | memorization — preference scorers reward the (memorized) good image, they do not detect copying | run SSCD retrieval against the training set; reject if any generation exceeds the replication threshold | overfit_gate |
| looks perfect on prompts like the training captions, breaks on new prompts | overfit to training images/captions rather than learning a generalizable style | score train-caption vs novel-prompt splits separately; gate on the divergence; reduce epochs/LR/repeats or add dataset diversity | overfit_gate |
| SSCD flags copies but the cause is duplicate training images | near-duplicate or over-repeated training samples drive memorization | re-run dataset dedup (record dedup_method/threshold) and Somepalli prompt-token randomization, then retrain | dedup_method |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| memorization-retrieval | max SSCD similarity of any generation to any training image | max-similarity reported per generation | no generation exceeds the per-style replication threshold (calibrate from base; Somepalli ~0.5 is a starting reference) | ✓ | SSCD descriptor (instrument) |
| overfit-divergence | panel-score gap between train-caption prompts and novel prompts | divergence delta reported | novel-prompt panel score within a max-allowed gap of the train-caption panel | ✓ | preference scorers (instrument) |

- **Best for:** prove a shipped style adapter does not regurgitate training images (ip-safety, fit 5) ; catch over-trained checkpoints the preference panel rates highly (overfit-detection, fit 5)
- **Verify:** verdict=confirmed-with-fixes | currency=current | SSCD paper (arXiv:2202.10261), Somepalli 2023 (arXiv:2305.20086), and Somepalli 2022 (arXiv:2212.03860) all confirmed real. Minor misattribution: the ~0.5 SSCD similarity threshold for partial-object copies is from arXiv:2212.03860 (the original replication paper), not arXiv:2305.20086 (the mitigation paper). Both are same authors; the 0.5-2% duplication rate claim is in 2305.20086. Fix: move the threshold claim citation to arXiv:2212.03860. Not in wave-1. evidence_strength 'reproduced-from-source' is justified.
- **Sources:** [A Self-Supervised Descriptor for Image Copy Detection (SSCD)](https://arxiv.org/abs/2202.10261) (Ed Pizzi, Sreya Dutta Roy, Sugosh Nagavara Ravindra, Priya Goyal, Matthijs Douze, 2022) — SSCD is a purpose-built self-supervised copy-detection descriptor that outperforms classification SSL features by large margins on DISC2021 — the strongest open detector for crops/recolors/partial copies ; [Understanding and Mitigating Copying in Diffusion Models](https://arxiv.org/abs/2305.20086) (Gowthami Somepalli, Vasu Singla, Micah Goldblum, Jonas Geiping, Tom Goldstein, 2023) — Generations above ~0.5 SSCD similarity are partial object-level copies of training images, 0.5-2% of generations duplicate training samples, and prompt-token randomization mitigates the memorized prompt->image link ; [Diffusion Art or Digital Forgery? Investigating Data Replication in Diffusion Models](https://arxiv.org/abs/2212.03860) (Gowthami Somepalli, Vasu Singla, Micah Goldblum, Jonas Geiping, Tom Goldstein, 2023) — Diffusion models replicate training content and replication is detectable by nearest-neighbor retrieval in a copy-detection embedding space — the basis for the SSCD-retrieval memorization test

### Pinned lm-eval-harness LLM evaluation (task_version / prompt / n_shot / precision / seed) · `recommended` · ▸ reproduced
**An LLM fine-tune is only attested if its eval pins task_version, prompt template, n_shot, precision, and seed — otherwise the score is irreproducible and meaningless.**
The reproducibility contract for evaluating a light 24-34B Q-quant fine-tune. EleutherAI's 'Lessons from the Trenches' (Biderman 2024) documents that LLM scores are extremely sensitive to evaluation SETUP — prompt formatting, few-shot count, answer extraction, and library version can swing results enough to flip a comparison — so a bare task name + score is not a result. The discipline: pin and RECORD the harness commit/version, the exact task_version, the prompt_template (a single character of prompt difference can move scores), n_shot, the eval PRECISION (eval the model at the quant you SHIP — a Q4 fine-tune evaluated in bf16 is measuring a different model), and the sampling seed. Always score the FINE-TUNE against its own BASE under byte-identical settings and report the delta; absolute leaderboard numbers are not portable across setups. This is the PIN_PER_STEP standard applied to eval: the run must be byte-for-byte replayable. The harness itself (lm-evaluation-harness) is CITED as the instrument; it is not catalogued as a training-knowledge entry (it lives in tensor-engine-knowledge as software).
- **For the pipeline:** Every LLM fine-tune readout carries an eval block stamping harness-version + task_version + prompt + n_shot + precision + seed + base-vs-trained delta. Eval at the SHIPPING quant (the Q-quant the studio actually serves), not the training precision. Never copy a leaderboard number for the base as the baseline — re-run the base locally under the same pins.
- **Method:** qlora · **Applies to:** llm · **Base:** Qwen3 · **Kind:** eval-method
- **Seed:** pinned per run (recorded, not arbitrary) · **Tuning budget:** none — measurement protocol; the only choice is which tasks map to the fine-tune's intended capability. · **Search:** none
- **Variance:** Biderman 2024: scores are sensitive to prompt format, n_shot, answer extraction, and harness version; without pinning, run-to-run and setup-to-setup variance can exceed the fine-tuning delta you are trying to measure. Quant precision at eval time is a first-class variable — eval the quant you ship.
- **Validated under:** Local 24-34B Q-quant fine-tunes evaluated on a small task suite chosen to match the adapter's purpose, at the shipping quant, base-vs-trained, all eval knobs pinned and recorded.
- **Base model (model-knowledge):** `qwen3-32b`
- **Output license:** commercial **yes** — lm-evaluation-harness is MIT-licensed eval software run at inference; it does not affect the fine-tune's license, which inherits from the base weights + SFT/preference data.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| n_shot | pinned & recorded (e.g. 0 or 5) shots | ● | few-shot count materially changes scores; must be fixed across base and trained |
| precision | the SHIPPING quant (e.g. Q4_K_M / NF4) quant | ● | eval the model you serve, not the bf16 training precision |
| seed | pinned & recorded int | ● | PIN_PER_STEP — byte-for-byte replayable |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Fine-tune 'beats base' but the gain vanishes when someone re-runs it | Eval setup (prompt/n_shot/version/precision) not pinned; the delta was setup noise | pin and record harness-version + task_version + prompt + n_shot + precision + seed; re-run base under identical pins | precision |
| Local eval disagrees sharply with the model card's reported score | Different harness version / prompt format / shots / quant than the card used | match the card's pins where possible, else only compare base-vs-trained measured locally under one setup | task_version |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| llm-task | lm-eval:<task suite matched to adapter purpose> | report trained-minus-base delta under byte-identical pins | trained >= base on target capability AND no regression beyond noise on a held-out general-capability task (forgetting guard) | ✓ | n/a (task accuracy / exact-match, not a judge) |

- **Best for:** Attest a 24-34B Q-quant fine-tune reproducibly (llm, fit 5) ; Detect capability regression / catastrophic forgetting after SFT (llm, fit 4)
- **Verify:** verdict=confirmed | currency=Current. lm-eval-harness is actively maintained as of 2026; the reproducibility paper (2405.14782) is 2024 and the guidance has not been superseded. | Both sources verified real and correctly attributed. Biderman et al. 2024 (arXiv:2405.14782) confirmed to address sensitivity to eval setup including prompt format, few-shot count, and library version. The lm-eval-harness GitHub reference is accurate. The eval harness is cited as an instrument, not catalogued as a training-knowledge entry — boundary correct. evidence_strength='reproduced-from-source' is appropriate.
- **Sources:** [Lessons from the Trenches on Reproducible Evaluation of Language Models](https://arxiv.org/abs/2405.14782) (Biderman, Schoelkopf, et al. (EleutherAI), 2024) — LLM evaluation is highly sensitive to setup (prompt format, few-shot count, answer extraction, library version); reproducibility requires pinning and reporting these, which lm-eval (the Language Model Evaluation Harness) is designed to support. ; [EleutherAI/lm-evaluation-harness (framework for few-shot evaluation of language models)](https://github.com/EleutherAI/lm-evaluation-harness) (EleutherAI, 2024) — The harness emits task versions and supports pinning prompt format, n_shot, and precision for independent, reproducible, extensible LLM evaluation.

### XY-grid candidate selection (frozen prompt+seed across epochs/ranks/weights) · `recommended` · ▸ reproduced
**A LoRA checkpoint is chosen from a fixed-prompt fixed-seed XY grid (axis = epoch/rank/weight, the other axis = a frozen prompt panel) where the only variable is the thing under test, then ranked by the panel metrics — never picked from the lowest training loss or a single hero image.**
The concrete winner-selection workflow that wave-1's eval panel assumed but did not specify. Diffusion training loss is a denoising MSE that is near-flat and NON-monotonic with perceived style quality, so you cannot read 'best epoch' off the loss curve; the winner is found by GENERATION. Protocol: (1) freeze a prompt panel of 6-12 prompts spanning the style's coverage (a few in-distribution scene types, a few out-of-distribution stress prompts, one or two that probe known failure modes) and a SMALL set of fixed seeds (3-5) — total cells small enough that one GPU can sweep them per checkpoint; (2) build an XY plot where one axis is the candidate dimension (saved epochs, OR rank when a rank sweep is in flight, OR LoRA application weight 0.6/0.8/1.0 at inference) and the other axis is the prompt panel, seed held identical down each column; (3) the ONLY thing that varies within a comparison is the candidate dimension — same prompt, same seed, same sampler/steps/CFG/resolution — so any visual difference is attributable to the adapter, not to sampling noise; (4) score every cell-set with the wave-1 panel (CMMD over the generated set, HPSv2/PickScore per-image, LPIPS-band + SSCD overfit guard) and have ai-eyes A/B the top 2-3; (5) the winner is the checkpoint that maximizes the preference axis WITHOUT tripping the overfit guard and WITHOUT collapsing prompt-adherence — i.e. the selection reads down the whole panel, not one number. Kohya/sd-scripts saves checkpoints every N epochs precisely so this sweep is possible after the run; A1111/Forge and ComfyUI both ship native XYZ-plot nodes to mechanize the grid. The grid is the receipt: it is replayable byte-for-byte because prompt+seed+sampler are pinned (PIN_PER_STEP).
- **For the pipeline:** sdlab's eval pack should emit the XY grid as an artifact (the grid image + the per-cell metric table) for every candidate set, with prompt list, seeds, sampler/steps/CFG/resolution stamped in the receipt. Checkpoint selection becomes 'cell (epoch=8, weight=0.8) won the panel' with the grid attached, not 'epoch 10 looked good'. Sweep LoRA application weight at inference on the grid too — the best training checkpoint and the best inference weight are two separate knobs and both belong on the axis.
- **Method:** diffusion-lora-checkpoint-selection · **Applies to:** diffusion · **Base:** SDXL / Flux · **Kind:** eval-method
- **Validated under:** SDXL/Flux style LoRAs, single-GPU studio sweeps over kohya-saved per-epoch checkpoints; frozen 6-12 prompt panel + 3-5 pinned seeds; identical sampler/steps/CFG/resolution within each comparison. Loss-curve non-monotonicity claim is general to diffusion denoising objectives; the winner-by-generation discipline is the portable part.
- **Base model (model-knowledge):** `sdxl-base / flux-dev`
- **Output license:** commercial **yes** — XYZ-plot tooling (A1111/Forge/ComfyUI) is open; the workflow is a process, no licensing constraint. Preference scorers used to rank cells carry their own license notes (see metric-routing technique).
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| steps | frozen across all cells sampler-steps | ● | any per-cell difference in sampler steps confounds the comparison |
| resolution | frozen across all cells (e.g. 1024x1024 SDXL) px | ● | resolution change shifts both quality and CMMD; hold it |
| epochs | save every N (e.g. every 1-2 epochs) so the epoch axis has candidates checkpoints | ● | kohya save_every_n_epochs makes the sweep possible post-run |
| network_type | LoRA/LoCon application weight 0.6/0.8/1.0 as a separate grid axis weight | ○ | best training checkpoint != best inference weight; sweep both |

- **Datasets:** Frozen eval prompt+seed panel (style-LoRA acceptance) (eval, license studio-internal (curated prompts; no third-party image redistribution))

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| winner picked from training-loss minimum looks worse than a higher-loss checkpoint | diffusion denoising loss is near-flat and not monotonic with style quality | select by generation on the XY grid, ignore loss for checkpoint choice | checkpoint_selection |
| two checkpoints look different but the difference vanishes on re-roll | seed not held fixed down the column — the variation was sampling noise, not the adapter | pin the seed per prompt across the candidate axis; only the candidate dimension may vary | seed |
| grid says epoch 12 wins but it has started copying training images | ranking on preference alone without the overfit guard on the same grid | run the SSCD/LPIPS overfit guard on each winning cell before crowning it | acceptance_gate |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| checkpoint-selection-grid | panel-rank of winning cell (CMMD delta + HPSv2 + PickScore + overfit-guard pass) | winning cell identified by panel consensus | winner must lead the preference axis AND pass the overfit guard AND not regress prompt-adherence vs base | ✓ | non-generator (ai-eyes arbiter on top 2-3) |

- **Best for:** pick the ship checkpoint from a style-LoRA training run (checkpoint-selection, fit 5) ; choose the inference LoRA weight to recommend with the adapter (weight-tuning, fit 5)
- **Verify:** verdict=confirmed | currency=current | All three sources verified real and correctly cited. kohya-ss save_every_n_epochs, AUTOMATIC1111 XYZ-plot, and CMMD arXiv:2401.09603 all confirmed. Not in wave-1 (wave-1 names the eval panel metrics but not the XY-grid checkpoint-selection methodology). Evidence_strength 'reproduced-from-source' is justified: the XY grid approach is a mechanization of documented trainer + webui features. No boundary violation, no overclaim.
- **Sources:** [kohya-ss sd-scripts — checkpoint saving (save_every_n_epochs) for post-run epoch selection](https://github.com/kohya-ss/sd-scripts) (kohya-ss, 2024) — trainer saves intermediate LoRA checkpoints per N epochs, enabling a post-run epoch sweep rather than trusting a loss curve ; [AUTOMATIC1111 stable-diffusion-webui — X/Y/Z plot script (fixed seed, vary one axis)](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features) (AUTOMATIC1111 contributors, 2024) — native XYZ-plot generates a grid varying one parameter (e.g. checkpoint/weight) with prompt and seed held fixed, the mechanization of the candidate-comparison grid ; [Rethinking FID: Towards a Better Evaluation Metric for Image Generation (CMMD)](https://arxiv.org/abs/2401.09603) (Sadeep Jayasumana, Srikumar Ramalingam, Andreas Veit, Daniel Glasner, Ayan Chakrabarti, Sanjiv Kumar, 2024) — CMMD is sample-efficient (stable at ~1000 samples) and monotone with quality, so it can rank the small per-cell generated sets a single-GPU grid produces where FID is unreliable

### Style-fidelity vs prompt-adherence tradeoff (the LoRA-weight frontier curve) · `recommended` · · community
**Style fidelity and prompt adherence trade off along LoRA application weight: as weight rises the style locks in (style metric improves) but the base model's prompt-following degrades (CLIP/ImageReward adherence drops), so the adapter is accepted at the KNEE of a measured weight-sweep frontier, not at the single weight that maximizes style.**
A net-new axis vs wave-1. A style LoRA does not have one quality number — it has a CURVE. Sweep the inference LoRA application weight (e.g. 0.4/0.6/0.8/1.0/1.2) over the frozen prompt+seed panel and plot two quantities against it: a STYLE-FIDELITY axis (CMMD-to-target-style and/or DreamSim-to-exemplar — does it look like the style) and a PROMPT-ADHERENCE axis (CLIP text-image similarity and ImageReward — does it still render what the prompt asked). The characteristic shape is a frontier: low weight = faithful to the prompt but weak style; high weight = strong style but the adapter overrides the prompt (subjects deform, requested content drops, palette/composition is forced regardless of prompt). The right ship weight is the KNEE — the highest style the panel will accept before prompt-adherence falls below its threshold. This makes the wave-1 'no single metric is sufficient' concrete and measurable: the two families are PLOTTED AGAINST EACH OTHER, and a checkpoint that has a better knee (more style at equal adherence) is genuinely better than one that only wins at max weight. The same frontier diagnoses training problems: a LoRA whose adherence collapses even at low weight is over-baked (too many epochs / LR too high / rank too high relative to dataset); one that never reaches acceptable style even at weight 1.2 is under-trained. ImageReward is the preferred adherence scorer because it was built to penalize prompt-ignoring and artifacts; CLIP-similarity is the cheap second opinion.
- **For the pipeline:** sdlab's eval pack emits a weight-sweep frontier (style axis vs adherence axis across application weights) for the winning checkpoint, and the recommended ship weight is the measured knee with both thresholds annotated. The readout shows the curve, so 'ship at 0.8' is justified by 'that is the knee where style peaks before adherence drops below gate'. Two checkpoints are compared by their frontiers, not their best single cell. A collapsed frontier (no acceptable knee exists) is itself a reject verdict that points back at training hparams.
- **Method:** diffusion-tradeoff-measurement · **Applies to:** diffusion · **Base:** SDXL / Flux · **Kind:** eval-method
- **Validated under:** SDXL/Flux style LoRAs, inference-weight sweep (0.4-1.2) over the frozen prompt+seed panel; style axis = CMMD/DreamSim, adherence axis = ImageReward/CLIP-sim. The fidelity-vs-adherence tradeoff along LoRA weight is a well-established community/practitioner observation and follows from how scaled adapter deltas override base conditioning; the specific knee is per-style and must be measured on the rig, not assumed.
- **Base model (model-knowledge):** `sdxl-base / flux-dev`
- **Builds on (stage 4):** XY-grid candidate selection (frozen prompt+seed across epochs/ranks/weights)
- **Output license:** commercial **conditional** — Uses the same scorer instruments as the routing technique (CMMD/DreamSim open; ImageReward/CLIP as cited instruments). No additional constraint beyond those scorers' terms for internal gating.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| network_type | LoRA/LoCon application weight swept 0.4/0.6/0.8/1.0/1.2 weight | ● | the x-axis of the frontier; the ship weight is the knee |
| rank | compare frontiers across rank candidates rank | ○ | higher rank often shifts the knee — a better frontier beats a better single cell |
| epochs | an adherence collapse at low weight flags over-training (reduce epochs) checkpoints | ○ | the frontier diagnoses over/under-training |

- **Datasets:** Frozen eval prompt+seed panel (style-LoRA acceptance) (eval, license studio-internal (curated prompts; no third-party image redistribution)) ; Curated style exemplar plate (perceptual-distance reference) (reference, license studio-internal canon assets (owned/licensed source art))

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| at the weight that nails the style, prompts are ignored (wrong subject/content) | scaled adapter delta overrides base text conditioning at high weight | ship at the measured knee (lower weight) where adherence is still above gate, not at max-style weight | ship_weight |
| adherence is poor even at low application weight | over-baked LoRA (too many epochs / LR too high / rank too high for the dataset) | retrain with fewer epochs / lower LR / lower rank; re-measure the frontier | epochs |
| style never reaches acceptable even at weight 1.2 | under-trained or dataset too thin/inconsistent for the style | more epochs/repeats or stronger/cleaner canon dataset; re-measure | steps |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| tradeoff-frontier | style-fidelity (CMMD/DreamSim) vs prompt-adherence (ImageReward/CLIP-sim) across LoRA weight | frontier curve + identified knee weight | a knee exists where style >= style-gate AND adherence >= adherence-gate; ship weight = knee | ✓ | CLIP/reward + CLIP-embedding (instruments) |

- **Best for:** choose the recommended inference weight to ship with the adapter (ship-weight, fit 5) ; compare two checkpoints fairly (checkpoint-comparison, fit 5) ; diagnose over- vs under-training from eval alone (training-diagnosis, fit 4)
- **Verify:** verdict=confirmed | currency=current | evidence_strength 'community-claim' is correct and honest — no single paper directly measures the LoRA-weight tradeoff frontier for style LoRAs. Sources are real: ImageReward (arXiv:2304.05977), LoRA paper (arXiv:2106.09685), diffusers docs all confirmed. PARTIAL ratings on two sources are appropriate (they support the mechanism but don't study the frontier directly). Not in wave-1. The knee-of-frontier acceptance rule is a genuine evaluation craft contribution. No overclaim.
- **Sources:** [ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977) (Jiazheng Xu et al., 2023) — ImageReward is purpose-built to penalize prompt-ignoring and artifacts, making it the adherence axis of the tradeoff frontier ; [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) (Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, 2021) — a LoRA contributes a scaled low-rank delta to the base weights — scaling that delta (application weight) is what trades adapter influence against base behavior, the mechanism behind the fidelity/adherence frontier ; [diffusers — controlling LoRA strength via cross_attention_kwargs scale / set_adapters weights](https://huggingface.co/docs/diffusers/en/using-diffusers/loading_adapters) (Hugging Face, 2024) — LoRA application weight (scale) is a first-class inference knob that adjusts how strongly the adapter is applied — the sweep axis of the frontier

### ai-eyes A/B rubric as the bias-controlled visual arbiter (order-swap + criterion-split) · `recommended` · · community
**The studio ai-eyes A/B arbiter is run as a STRUCTURED pairwise rubric — fixed criteria scored separately (style-fidelity / prompt-adherence / artifact-freedom / canon-consistency), each pair presented in BOTH orders with only swap-agreeing verdicts counted — porting the LLM-judge bias controls (position-swap, different-family verifier) into the visual lane so the arbiter is a verifier, not a vibe.**
Wave-1 named ai-eyes as the human/different-model tie-breaker and veto; this technique specifies the RUBRIC and its bias controls, importing the discipline already proven in wave-1's LLM-judge technique into the diffusion lane (a flagged cross-domain import). ai-eyes (a vision-LLM A/B comparator) is the EXTERNAL_VERIFIER for visual quality: it must be a DIFFERENT model family than anything in the generation pipeline, and it must never see the metric scores or which candidate is the 'new' one (reasoning hidden, per the workflow-standards verifier rule). The rubric: (1) CRITERION-SPLIT — instead of one 'which is better', score fixed independent criteria — style fidelity to the canon, prompt adherence, artifact/anatomy freedom, canon/terminology consistency — so the verdict is decomposable and a style win that costs anatomy is visible, not averaged away; (2) ORDER-SWAP — every A/B pair is shown in both left-right orders and only verdicts that AGREE across the swap count (position bias is the dominant pairwise-judge artifact, per Zheng 2023, and applies to VLM judges too); report the swap-agreement rate as a confidence signal — low agreement means the pair is too close to call and goes to a human; (3) BLIND — the arbiter does not know which image came from the candidate vs the base/incumbent, removing the 'newer must be better' prior. ai-eyes is the TIE-BREAKER and VETO over the numeric panel: when the metric panel is ambiguous (two checkpoints within noise) ai-eyes decides; when the metric panel says pass but ai-eyes flags a hard defect (broken hands, off-canon palette) ai-eyes can VETO (ANDON). It is the UNCERTAINTY_GATED_HUMANS seam too: low swap-agreement is the uncertainty signal that escalates to the human director, framed contrastively ('the metrics preferred candidate B; ai-eyes split 50/50 on style — your call').
- **For the pipeline:** sdlab's rubric/eval pack runs ai-eyes as a structured criterion-split A/B with order-swap and blinding, emitting per-criterion verdicts + swap-agreement, NOT a single 'B wins'. The arbiter model family must differ from the generation stack (cross-domain import of the EXTERNAL_VERIFIER rule from the LLM lane). Wire two gates: ai-eyes breaks ties the numeric panel can't, and ai-eyes can veto a metric-pass on a hard visual defect. Low swap-agreement routes to the human director with a contrastive framing rather than auto-deciding.
- **Method:** diffusion-human-model-arbiter · **Applies to:** diffusion · **Base:** SDXL / Flux · **Kind:** eval-method
- **Validated under:** SDXL/Flux style-LoRA candidate pairs (checkpoint vs checkpoint, or trained vs base) judged by a different-family vision-LLM A/B arbiter over the frozen prompt+seed panel, every pair order-swapped and blinded, scored on the fixed criterion split. Bias-control mechanisms (position-swap, different-family, blinding) are reproduced-from-source for LLM judges; their transfer to VLM visual judging is a reasoned cross-domain import, not separately measured here.
- **Base model (model-knowledge):** `sdxl-base / flux-dev`
- **Output license:** commercial **yes** — ai-eyes is an internal studio instrument; the rubric is a process. No redistribution concern. The arbiter VLM's own license governs that model's use as an instrument.
- **Fit:** rig 4/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| batch_size | every pair scored in both orders (2x presentations) presentations | ● | order-swap doubles presentations; only swap-agreeing verdicts count |
| seed | same prompt+seed pair shown to the arbiter as to the metric panel | ● | arbiter and metrics judge the identical generations |

- **Datasets:** Frozen eval prompt+seed panel (style-LoRA acceptance) (eval, license studio-internal (curated prompts; no third-party image redistribution))

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| ai-eyes verdict flips when the images are swapped left-right | position bias — the dominant pairwise-judge artifact, present in VLM judges too | present every pair in both orders, count only swap-agreeing verdicts, report agreement rate | judge_protocol |
| arbiter consistently prefers the candidate it was told is 'the new one' | newer-is-better prior / lack of blinding | blind the arbiter to which image is candidate vs base and hide the metric scores | judge_protocol |
| the same-family VLM rates the studio's own pipeline outputs too generously | self-enhancement / familiarity bias when the judge shares a family with the stack | use a different-family arbiter than the generation pipeline (EXTERNAL_VERIFIER) | judge_model_family |


**Evaluation**

| Kind | Metric | Result | Threshold | Pass | Judge family |
|---|---|---|---|---|---|
| pairwise-arbiter | criterion-split A/B win-rate (style / adherence / artifact / canon) with swap-agreement | per-criterion verdicts + swap-agreement rate | candidate wins or ties on every hard criterion with swap-agreement above the confidence floor; any hard-defect veto = reject | ✓ | different-family VLM (non-generator) |

- **Best for:** break ties the numeric panel cannot resolve (tie-break, fit 5) ; veto a metric-pass that has a hard visual defect (veto, fit 5) ; decide when to escalate to the human director (uncertainty-gate, fit 4)
- **Verify:** verdict=confirmed-with-fixes | currency=current | MT-Bench paper (arXiv:2306.05685) confirmed real, position bias discussion confirmed. Kambhampati (arXiv:2402.01817) confirmed real. evidence_strength 'community-claim' is correct — the specific port of LLM-judge bias controls to a VLM visual arbiter is a studio design decision, not paper-sourced. Near-dedup warning: wave-1 has 'Bias-controlled different-family LLM judge (order-swap + length-match)' but that covers the TEXT lane; this technique covers the VISUAL lane (ai-eyes VLM). Fix: add an explicit cross-reference distinguishing this as the visual-lane counterpart to the wave-1 text-lane technique. Third source (internal workflow_standards.md) is legitimate grounding for the external-verifier requirement.
- **Sources:** [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) (Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica, 2023) — pairwise judges exhibit position, verbosity, and self-enhancement bias; position-swapping and only counting consistent verdicts controls position bias — the controls ported here to the VLM visual arbiter ; [On Verification and the Role of LLMs (the LLM-Modulo / external-verifier argument)](https://arxiv.org/abs/2402.01817) (Subbarao Kambhampati et al., 2024) — models cannot reliably verify their own outputs; verification must be external — grounds the requirement that the visual arbiter be a different family than the generation stack ; [Workflow Standards — EXTERNAL_VERIFIER and UNCERTAINTY_GATED_HUMANS (mcp-tool-shop)](https://github.com/mcp-tool-shop/mcp-tool-shop) (mcp-tool-shop, 2026) — no model verifies its own output; the verifier is a different family with the generator's reasoning hidden; human checkpoints gate on uncertainty with contrastive framing — the studio standards this rubric implements

### AlpacaEval · `situational` · paper
**Pairwise auto-evaluator vs reference; default **length-controlled win-rates**; annotator **`is_randomize_output_order`** against position bias; win-rate = mean preference foil (not invent thresholds).**
STUDY-055 deepen — Pairwise auto-evaluator vs reference; default **length-controlled win-rates**; annotator **`is_randomize_output_order`** against position bias; win-rate = mean
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [AlpacaEval](https://github.com/tatsu-lab/alpaca_eval) — Pairwise auto-evaluator vs reference; default **length-controlled win-rates**; annotator **`is_randomize_output_order`** against position bias; win-rate = mean preference foil (not invent thresholds).

### AlpacaEval annotator protocol (same repo §Evaluators) · `situational` · paper
**On-page metrics table defines **Human agreement**, **Bias/Variance**, **Proba. prefer longer** for judge foil quality (describes evaluator, not invent studio gates).**
STUDY-055 deepen — On-page metrics table defines **Human agreement**, **Bias/Variance**, **Proba. prefer longer** for judge foil quality (describes evaluator, not invent studio ga
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [AlpacaEval annotator protocol (same repo §Evaluators)](https://github.com/tatsu-lab/alpaca_eval#evaluators) — On-page metrics table defines **Human agreement**, **Bias/Variance**, **Proba. prefer longer** for judge foil quality (describes evaluator, not invent studio gates).

### Amulet: Putting Complex Multi-Turn Conversations on the Stand with LLM Juries · `situational` · paper
**Multi-turn preference judging; runs **R1/R2 then swapped** to mitigate position bias; juries of LLM/RM judges — explicit AB/BA contrastive protocol for bias-controlled arbiter.**
STUDY-055 deepen — Multi-turn preference judging; runs **R1/R2 then swapped** to mitigate position bias; juries of LLM/RM judges — explicit AB/BA contrastive protocol for bias-con
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Amulet: Putting Complex Multi-Turn Conversations on the Stand with LLM Juries](https://arxiv.org/abs/2505.20451) — Multi-turn preference judging; runs **R1/R2 then swapped** to mitigate position bias; juries of LLM/RM judges — explicit AB/BA contrastive protocol for bias-controlled arbiter.

### Bradley–Terry model · `situational` · paper
**Analog: pairwise preference outcomes → latent strengths. Holds for contrastive A/B human foil protocols over absolute scalar invent. Limit: BT math ≠ FID/CLIP lone ship gate.**
STUDY-055 deepen — Analog: pairwise preference outcomes → latent strengths. Holds for contrastive A/B human foil protocols over absolute scalar invent. Limit: BT math ≠ FID/CLIP l
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Bradley–Terry model](https://en.wikipedia.org/wiki/Bradley%E2%80%93Terry_model) — Analog: pairwise preference outcomes → latent strengths. Holds for contrastive A/B human foil protocols over absolute scalar invent. Limit: BT math ≠ FID/CLIP lone ship gate.

### CLIP+MLP Aesthetic Predictor · `situational` · paper
**Average “how much people like” aesthetic foil from CLIP embeds; LAION-bucket viz — **no acceptance threshold on page → flag**.**
STUDY-055 deepen — Average “how much people like” aesthetic foil from CLIP embeds; LAION-bucket viz — **no acceptance threshold on page → flag**.
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [CLIP+MLP Aesthetic Predictor](https://github.com/christophschuhmann/improved-aesthetic-predictor) — Average “how much people like” aesthetic foil from CLIP embeds; LAION-bucket viz — **no acceptance threshold on page → flag**.

### CMMD README CLI eval stack (google-research) · `situational` · paper
**Distributional image-gen metric CLI (CLIP ViT-L/14@336) — portable peer to bare FID**
STUDY-035 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** eval · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Rethinking FID / CMMD](https://arxiv.org/abs/2401.09603) — CMMD vs FID failure modes. ; [CMMD README](https://github.com/google-research/google-research/tree/master/cmmd) — python -m cmmd.main ref_dir eval_dir CLI.

### Clean First, Align Later: Benchmarking Preference Data Cleaning for Reliable LLM Alignment · `situational` · paper
**Benchmarks LLM-as-judge (and RM/heuristic) preference-label cleaning with human foil on noisy feedback — preference-judge data hygiene before DPO-class stages.**
STUDY-055 deepen — Benchmarks LLM-as-judge (and RM/heuristic) preference-label cleaning with human foil on noisy feedback — preference-judge data hygiene before DPO-class stages
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Clean First, Align Later: Benchmarking Preference Data Cleaning for Reliable LLM](https://arxiv.org/abs/2509.23564) — Benchmarks LLM-as-judge (and RM/heuristic) preference-label cleaning with human foil on noisy feedback — preference-judge data hygiene before DPO-class stages.

### Cohen's kappa · `situational` · paper
**Analog: inter-rater agreement **chance-corrected** (κ accounts for expected agreement). Holds for judge↔human foil reporting beyond raw %-agree. Limit: categorical κ ≠ inventing a style CMMD threshold.**
STUDY-055 deepen — Analog: inter-rater agreement **chance-corrected** (κ accounts for expected agreement). Holds for judge↔human foil reporting beyond raw %-agree. Limit: categori
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Cohen's kappa](https://en.wikipedia.org/wiki/Cohen%27s_kappa) — Analog: inter-rater agreement **chance-corrected** (κ accounts for expected agreement). Holds for judge↔human foil reporting beyond raw %-agree. Limit: categorical κ ≠ inventing a style CMMD threshold

### Diffusers adapter scale 0–1 checkpoint grid · `situational` · docs
**cross_attention_kwargs scale / set_adapters for LoRA strength grids — inference eval knob**
STUDY-035 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** eval · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Diffusers Load adapters](https://huggingface.co/docs/diffusers/main/en/using-diffusers/loading_adapters) — scale 0–1 LoRA strength for eval grids.

### DreamSim · `situational` · paper
**Mid/high-level perceptual distance on diffusion **NIGHTS triplets** (human similarity judgments); distance = cosine between embeds; retrieval ranking by distance.**
STUDY-055 deepen — Mid/high-level perceptual distance on diffusion **NIGHTS triplets** (human similarity judgments); distance = cosine between embeds; retrieval ranking by distanc
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [DreamSim](https://github.com/ssundaram21/dreamsim) — Mid/high-level perceptual distance on diffusion **NIGHTS triplets** (human similarity judgments); distance = cosine between embeds; retrieval ranking by distance.

### EleutherAI lm-evaluation-harness pinned LLM eval · `situational` · docs
**Pinned task configs/few-shot/PEFT LoRA model_args — portable LLM eval stack**
STUDY-035 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** eval · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [lm-evaluation-harness README](https://github.com/EleutherAI/lm-evaluation-harness) — Pinned public prompts; peft= in model_args.

### FastChat LLM Judge / MT-Bench · `situational` · paper
**LLM-as-judge: single-answer 1–10 grading; **pairwise-baseline** / **pairwise-all** winrate modes; human↔GPT-4 agreement notebook on MT-bench judgments.**
STUDY-055 deepen — LLM-as-judge: single-answer 1–10 grading; **pairwise-baseline** / **pairwise-all** winrate modes; human↔GPT-4 agreement notebook on MT-bench judgments.
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [FastChat LLM Judge / MT-Bench](https://github.com/lm-sys/FastChat/blob/main/fastchat/llm_judge/README.md) — LLM-as-judge: single-answer 1–10 grading; **pairwise-baseline** / **pairwise-all** winrate modes; human↔GPT-4 agreement notebook on MT-bench judgments.

### G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment · `situational` · paper
**Framework for LLM NLG eval with reported Spearman correlation to humans; notes LLM-evaluator biases — human-alignment gate for automated judges.**
STUDY-055 deepen — Framework for LLM NLG eval with reported Spearman correlation to humans; notes LLM-evaluator biases — human-alignment gate for automated judges.
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment](https://arxiv.org/abs/2303.16634) — Framework for LLM NLG eval with reported Spearman correlation to humans; notes LLM-evaluator biases — human-alignment gate for automated judges.

### HPSv2 human preference scorer (Wu et al. 2023) · `situational` · paper
**HPDv2 pairs + HPSv2 scorer for T2I preference — beyond bare CLIP-sim**
STUDY-035 Scholar deepen — 2306.09341.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** eval · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [HPSv2](https://arxiv.org/abs/2306.09341) — Human preference score v2 for T2I.

### HPSv3 · `situational` · paper
**Beyond HPSv2: VLM preference scorer + **HPDv3** pairwise comparisons (1.17M annotated pairs); `reward(prompts, image_paths)` API (no studio cutoffs invent).**
STUDY-055 deepen — Beyond HPSv2: VLM preference scorer + **HPDv3** pairwise comparisons (1.17M annotated pairs); `reward(prompts, image_paths)` API (no studio cutoffs invent).
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [HPSv3](https://github.com/MizzenAI/HPSv3) — Beyond HPSv2: VLM preference scorer + **HPDv3** pairwise comparisons (1.17M annotated pairs); `reward(prompts, image_paths)` API (no studio cutoffs invent).

### Human Preference Score v2 · `situational` · paper
**Analog: preference scorer grounded in human preference pairs (HPDv2). Holds as contrastive human-foil lane for T2I eval (alongside PickScore/ImageReward). Limit: HPSv2 ≠ inventing studio ship gates.**
STUDY-055 deepen — Analog: preference scorer grounded in human preference pairs (HPDv2). Holds as contrastive human-foil lane for T2I eval (alongside PickScore/ImageReward).
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Human Preference Score v2](https://arxiv.org/abs/2306.09341) — Analog: preference scorer grounded in human preference pairs (HPDv2). Holds as contrastive human-foil lane for T2I eval (alongside PickScore/ImageReward). Limit: HPSv2 ≠ inventing studio ship gates.

### ImageReward learned T2I preference reward (Xu et al. 2023) · `situational` · paper
**Learned reward on human T2I preferences — third preference-eval axis**
STUDY-035 Scholar deepen — 2304.05977.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** eval · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [ImageReward](https://arxiv.org/abs/2304.05977) — Learned human preference reward for T2I.

### Inter-rater reliability · `situational` · paper
**Analog: agreement among raters as a reliability construct (kappa / ICC / α families). Holds: LLM-judge panels need IRR vs human foil, not solo score. Limit: IRR stats ≠ diffusion LoRA recipe invent.**
STUDY-055 deepen — Analog: agreement among raters as a reliability construct (kappa / ICC / α families). Holds: LLM-judge panels need IRR vs human foil, not solo score. Limit: IRR
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Inter-rater reliability](https://en.wikipedia.org/wiki/Inter-rater_reliability) — Analog: agreement among raters as a reliability construct (kappa / ICC / α families). Holds: LLM-judge panels need IRR vs human foil, not solo score. Limit: IRR stats ≠ diffusion LoRA recipe invent.

### Judging LLM-as-a-Judge (MT-Bench / Arena) · `situational` · paper
**Analog: LLM judges show position/verbosity/self-enhancement biases; agreement with humans must be verified. Holds: **judge ≠ automatic human substitute**. Limit: chat MT-Bench ≠ T2I preference panels.**
STUDY-055 deepen — Analog: LLM judges show position/verbosity/self-enhancement biases; agreement with humans must be verified. Holds: **judge ≠ automatic human substitute**.
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Judging LLM-as-a-Judge (MT-Bench / Arena)](https://arxiv.org/abs/2306.05685) — Analog: LLM judges show position/verbosity/self-enhancement biases; agreement with humans must be verified. Holds: **judge ≠ automatic human substitute**. Limit: chat MT-Bench ≠ T2I preference panels.

### Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena · `situational` · paper
**Documents LLM-judge **position/verbosity/self-enhancement** biases; verifies agreement with **human** preferences via MT-Bench + Chatbot Arena — foundational different-family judge foil (order-control craft, not a new scalar invent).**
STUDY-055 deepen — Documents LLM-judge **position/verbosity/self-enhancement** biases; verifies agreement with **human** preferences via MT-Bench + Chatbot Arena — foundational di
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) — Documents LLM-judge **position/verbosity/self-enhancement** biases; verifies agreement with **human** preferences via MT-Bench + Chatbot Arena — foundational different-family judge foil (order-control

### Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges · `situational` · paper
**Only largest judges reasonably align; still differ from humans; urges metrics beyond percent agreement — judge-vs-human honesty without inventing ship gates.**
STUDY-055 deepen — Only largest judges reasonably align; still differ from humans; urges metrics beyond percent agreement — judge-vs-human honesty without inventing ship gates.
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges](https://arxiv.org/abs/2406.12624) — Only largest judges reasonably align; still differ from humans; urges metrics beyond percent agreement — judge-vs-human honesty without inventing ship gates.

### LPIPS / PerceptualSimilarity · `situational` · paper
**Perceptual distance (higher = more different); BAPPS **2AFC** human foil (ref + two distorted; pick closer) + **JND**; CLI `lpips_2imgs` / `lpips_2dirs`.**
STUDY-055 deepen — Perceptual distance (higher = more different); BAPPS **2AFC** human foil (ref + two distorted; pick closer) + **JND**; CLI `lpips_2imgs` / `lpips_2dirs`.
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [LPIPS / PerceptualSimilarity](https://github.com/richzhang/PerceptualSimilarity) — Perceptual distance (higher = more different); BAPPS **2AFC** human foil (ref + two distorted; pick closer) + **JND**; CLI `lpips_2imgs` / `lpips_2dirs`.

### Pick-a-Pic open user preference pairs (Kirstain et al. 2023) · `situational` · paper
**Open user-preference pairs underlying PickScore — pairwise preference eval**
STUDY-035 Scholar deepen — 2305.01569.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** eval · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Pick-a-Pic](https://arxiv.org/abs/2305.01569) — Open T2I user preference dataset.

### Pre-SPEC pre-specified eval endpoints · `situational` · paper
**Declare endpoints before seeing candidate data — acceptance threshold discipline**
STUDY-035 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** eval · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Pre-SPEC clinical-trial stats](https://doi.org/10.1186/s12916-020-01706-7) — Endpoints declared before candidate data.

### Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Language Models · `situational` · paper
**Direct assessment **and** pairwise ranking; highest human/GPT-4 agreement among open judges tested — dual-protocol open judge craft.**
STUDY-055 deepen — Direct assessment **and** pairwise ranking; highest human/GPT-4 agreement among open judges tested — dual-protocol open judge craft.
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Prometheus 2: An Open Source Language Model Specialized in Evaluating Other Lang](https://arxiv.org/abs/2405.01535) — Direct assessment **and** pairwise ranking; highest human/GPT-4 agreement among open judges tested — dual-protocol open judge craft.

### Prometheus: Inducing Fine-grained Evaluation Capability in Language Models · `situational` · paper
**Open evaluator LLM with custom rubrics; high Pearson with human evaluators on Feedback Collection — open judge alternative to proprietary-only scoring.**
STUDY-055 deepen — Open evaluator LLM with custom rubrics; high Pearson with human evaluators on Feedback Collection — open judge alternative to proprietary-only scoring.
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Prometheus: Inducing Fine-grained Evaluation Capability in Language Models](https://arxiv.org/abs/2310.08491) — Open evaluator LLM with custom rubrics; high Pearson with human evaluators on Feedback Collection — open judge alternative to proprietary-only scoring.

### Rating Scales in UX (Likert biases) · `situational` · paper
**Analog: Likert/semantic scales carry acquiescence / social-desirability bias. Holds for HCI preference protocol design (forced choice / foil over soft agree). Limit: UX surveys ≠ Comfy batch eval harness.**
STUDY-055 deepen — Analog: Likert/semantic scales carry acquiescence / social-desirability bias. Holds for HCI preference protocol design (forced choice / foil over soft agree).
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Rating Scales in UX (Likert biases)](https://www.nngroup.com/articles/rating-scales/) — Analog: Likert/semantic scales carry acquiescence / social-desirability bias. Holds for HCI preference protocol design (forced choice / foil over soft agree). Limit: UX surveys ≠ Comfy batch eval harn

### Reliability without Validity — LLM-as-judge audit · `situational` · paper
**Large multi-judge audit: exact-match overstates agreement; need chance-corrected kappa/alpha, AB+BA swaps, retest, contrasting benchmarks.**
Large multi-judge audit: exact-match overstates agreement; need chance-corrected kappa/alpha, AB+BA swaps, retest, contrasting benchmarks.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not flip technique rows.
- **Method:** eval · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** eval-method
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Reliability without Validity — LLM-as-judge audit](https://arxiv.org/abs/2606.19544) — Large multi-judge audit: exact-match overstates agreement; need chance-corrected kappa/alpha, AB+BA swaps, retest, contrasting benchmarks.

### Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias · `situational` · paper
**Exact-match overstates ability; use chance-corrected **Cohen’s κ** / related; multi-protocol audit incl. bias — catalog “Reliability without Validity” deepen.**
STUDY-055 deepen — Exact-match overstates ability; use chance-corrected **Cohen’s κ** / related; multi-protocol audit incl. bias — catalog “Reliability without Validity” deepen
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-J](https://arxiv.org/abs/2606.19544) — Exact-match overstates ability; use chance-corrected **Cohen’s κ** / related; multi-protocol audit incl. bias — catalog “Reliability without Validity” deepen.

### SSCD copy-detection · `situational` · paper
**Self-supervised fingerprint for copy/overfit foil; README states for `sscd_disc_mixup`, DISC pairs with cosine **>0.75** are copies at **90% precision** (vendor claim on-page — not a studio ship gate invent).**
STUDY-055 deepen — Self-supervised fingerprint for copy/overfit foil; README states for `sscd_disc_mixup`, DISC pairs with cosine **>0.75** are copies at **90% precision**
- **For the pipeline:** STUDY-055. Judge ≠ human substitute; no ship-gate invent.
- **Method:** evaluation · **Applies to:** both · **Base:** SDXL|Flux|Qwen|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-055 deepen
- **Fit:** rig 3/5 · studio 3/5
- **Verify:** STUDY-055 deepen
- **Sources:** [SSCD copy-detection](https://github.com/facebookresearch/sscd-copy-detection) — Self-supervised fingerprint for copy/overfit foil; README states for `sscd_disc_mixup`, DISC pairs with cosine **>0.75** are copies at **90% precision** (vendor claim on-page — not a studio ship gate

### Spaced repetition / sequenced curriculum hold-with-limit · `situational` · docs
**Isolate fundamentals before mixing — anti-bleed curriculum analogy; limit ≠ invent caption-tag recipes.**
STUDY-035 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** dataset · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [Spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition) — Sequenced fundamentals before mixing.

### sklearn common pitfalls — train/test leakage · `situational` · docs
**Never fit transforms on the test set; split first. Holds for held-out eval + train_eval_overlap_checked.**
Never fit transforms on the test set; split first. Holds for held-out eval + train_eval_overlap_checked.
- **For the pipeline:** STUDY-009 Verifier-verified. Do not flip technique rows.
- **Method:** eval · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama · **Kind:** eval-method
- **Output license:** commercial **check** — STUDY-019 reopen; verified=0.
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [sklearn common pitfalls — train/test leakage](https://scikit-learn.org/stable/common_pitfalls.html) — Never fit transforms on the test set; split first. Holds for held-out eval + train_eval_overlap_checked.

### sklearn train/test leakage + learning-curve overfit checks · `situational` · docs
**Split before fit; high train/low val ⇒ overfit; checkpoint≠last — hold-with-limit**
STUDY-035 Practitioner/Analogist Verifier ✅.
- **For the pipeline:** STUDY-035 Verifier ✅. WD thresholds only as card-scraped.
- **Method:** eval · **Applies to:** both · **Base:** SDXL|Flux|Qwen|Llama|general · **Kind:** method-theory
- **Output license:** commercial **check** — STUDY-035 deepen
- **Fit:** rig 4/5 · studio 4/5
- **Sources:** [sklearn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) — Split first; never fit on test. ; [sklearn learning curves](https://scikit-learn.org/stable/modules/learning_curve.html) — Train/val gap signals overfitting.

