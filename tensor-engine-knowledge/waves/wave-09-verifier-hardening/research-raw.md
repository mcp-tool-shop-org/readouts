# Wave-9 study-swarm — research grounding for the verifier-hardening finding

Three parallel research agents (research-grounded-advisor protocol) grounding the wave-9 empirical
result: a 3-family local verifier panel (Qwen3-14B + Mistral-Nemo-12B + IBM-Granite-8B, conservative
majority) held 0 false-confirms on easy citations but false-confirmed adversarial traps where a
MAJORITY of seats shared a credulity blind spot. Question: does family diversity fix correlated
errors, and if not, what does? These three outputs are the large sources fed to `offload compress`
(preread token-economy measurement) and whose arXiv citations are re-checked by the wave-9 panel.

---

## Agent A — Ensemble diversity vs correlated error

Does model/family diversity reduce correlated errors in LLM verifier ensembles?

1. **Correlated Errors in Large Language Models** — Kim, Garg, Peng, Garg (2025). arXiv:2506.07962 — https://arxiv.org/abs/2506.07962
   Across 350+ LLMs, models agree ~60% of the time when both are wrong, and larger/more-accurate models have MORE correlated errors even across distinct architectures and providers — capability convergence (not just shared lineage) drives shared blind spots.
2. **Don't Always Pick the Highest-Performing Model: An Information-Theoretic View of LLM Ensemble Selection** — Turkmen, Buyukates, Bastopcu (2026). arXiv:2602.08003 — https://arxiv.org/abs/2602.08003 (ID future-dated; treat as unconfirmed)
   Selecting the strongest models saturates because they share error patterns; selecting by mutual information (diversity) yields a lower-average-accuracy but collectively more-correct panel — supports cross-family over best-of-breed.
3. **Hidden Clones: Exposing and Fixing Family Bias in Vision-Language Model Ensembles** — Bugaud (2026). arXiv:2603.17111 — https://arxiv.org/abs/2603.17111 (ID future-dated; treat as unconfirmed)
   Same-family models violate voting-independence: family-correlated errors collapse a nominally N-member panel to an effective 2.5–3.6 independent voters; family-aware aggregation recovers +18–26 pts on hard cases.
4. **Measures of Diversity in Classifier Ensembles and Their Relationship with the Ensemble Accuracy** — Kuncheva & Whitaker (2003), Machine Learning 51(2):181–207. DOI 10.1023/A:1022859003006 (no arXiv)
   The classic result: majority-vote accuracy is bounded by member correlation; the independence-assumption gains are largely unrealizable because real classifiers' errors are positively correlated (coincident "double-fault" failures dominate).
5. **Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models (PoLL)** — Verga, Hofstätter, Althammer et al. (2024). arXiv:2404.18796 — https://arxiv.org/abs/2404.18796
   A panel of 3 different-family small judges reduces intra-model bias and beats a single large judge — but the mechanism it fixes is self-preference/style bias, NOT shared reasoning errors common to all three.
6. **Self-Preference Bias in LLM-as-a-Judge** — Wataoka, Takahashi, Ri (2024). arXiv:2410.21819 — https://arxiv.org/abs/2410.21819
   Judges over-score text that is familiar / low-perplexity to them; because low-perplexity correlates with fluent-but-wrong phrasings, a subtle inversion that reads naturally fools judges from multiple families the same way.
7. **Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge** — Shi, Ma, Liang, Diao, Ma, Vosoughi (2024). arXiv:2406.07791 — https://arxiv.org/abs/2406.07791
   Position bias is systematic, not random, and varies by judge/task — structured enough that several judges can share it, so it is not guaranteed to cancel under majority vote.

**Design implication:** family/model diversity reduces idiosyncratic biases (position, verbosity, self-preference) but does NOT reliably reduce correlated errors rooted in shared generalization — so a 3rd model family will not close the adversarial false-confirm gap (the trap is the coincident-failure regime where majority vote provably gives no gain). The fix is a different MECHANISM: an asymmetric/contrastive verifier step, a deterministic entailment/NLI or string-grounding floor that does not share the LLMs' fluency bias, and unanimity-with-abstention rather than majority on flagged items.

---

## Agent B — Mechanism diversity (not just model diversity)

1. **SAC3: Reliable Hallucination Detection via Semantic-aware Cross-check Consistency** — Zhang, Li, Das, Malin, Kumar (2023). arXiv:2311.01740 — https://arxiv.org/abs/2311.01740
   Self-consistency (resampling one model) cannot catch question/model-level hallucinations because the model answers consistently wrong; cross-mechanism checks (perturbed variants + a different model) beat same-model self-consistency.
2. **Large Language Models Cannot Self-Correct Reasoning Yet** — Huang et al. (2023). arXiv:2310.01798 — https://arxiv.org/abs/2310.01798
   Without external feedback LLMs fail to self-correct and accuracy frequently degrades after self-revision — a model's own judgment is not an independent verifier of itself.
3. **Position: LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks** — Kambhampati et al. (2024). arXiv:2402.01817 — https://arxiv.org/abs/2402.01817
   Self-verification is itself reasoning LLMs can't do reliably; correctness needs an external, sound (model-based/symbolic) critic — a categorically different mechanism, not another LLM seat.
4. **Debate or Vote: Which Yields Better Decisions in Multi-Agent LLMs?** — Choi, Zhu, Li (2024). arXiv:2508.17536 — https://arxiv.org/abs/2508.17536
   The decisive variable is agent diversity: when agents are correlated/homogeneous, voting degrades from shared error and debate stalls — explains why same-mechanism seats false-confirm traps.
5. **Fact or Fiction: Verifying Scientific Claims (SciFact)** — Wadden et al. (2020). arXiv:2004.14974 — https://arxiv.org/abs/2004.14974
   Frames citation checking as explicit SUPPORTS/REFUTES/NOT-ENOUGH-INFO entailment with rationale selection against the cited abstract — a dedicated grounded-entailment formulation.
6. **Measuring Attribution in Natural Language Generation Models (AIS)** — Rashkin et al. (2021). arXiv:2112.12870 — https://arxiv.org/abs/2112.12870
   "Attributable to Identified Sources": every claim must be entailed by an independent provided source — the canonical standard a citation gate should enforce as a separate axis.
7. **FActScore: Fine-grained Atomic Evaluation of Factual Precision** — Min et al. (2023). arXiv:2305.14251 — https://arxiv.org/abs/2305.14251
   Decomposes generations into atomic facts checked against a source via retrieval + validator; the retrieval-grounding step catches per-fact unsupported claims a holistic judge waves through.
8. **Auditing Multi-Agent LLM Reasoning Trees Outperforms Majority Vote and LLM-as-Judge** — (2026). arXiv:2602.09341 (ID UNCONFIRMED — future-dated, could not fetch). Classical grounding: Krogh & Vedelsby, "Neural Network Ensembles, Cross Validation, and Active Learning" (1995, NeurIPS) — variance reduction requires low error-correlation / different inductive biases.

**Design implication:** beyond a 3rd model family, add a mechanistically-orthogonal verifier — a dedicated NLI/entailment check (premise→hypothesis against the retrieved span, SciFact/AIS formulation) gated by a deterministic retrieval-existence/atomic-grounding floor (FActScore-style) that fails closed. That entailment+symbolic floor fails precisely where a homogeneous LLM panel false-confirms, because it does not share the panel's generative blind spot.

---

## Agent C — Prompting / calibration vs plausibility & directional bias

1. **Language Models Don't Always Say What They Think: Unfaithful Explanations in CoT** — Turpin, Michael, Perez, Bowman (2023). arXiv:2305.04388 — https://arxiv.org/abs/2305.04388
   CoT is systematically plausible yet unfaithful — models rationalize a biased/wrong answer (accuracy drops up to 36%); the exact mechanism behind confirming a plausible-but-unstated addition.
2. **Towards Understanding Sycophancy in Language Models** — Sharma, Tong, Korbak, …, Perez (2023). arXiv:2310.13548 — https://arxiv.org/abs/2310.13548
   RLHF models and their preference models prefer responses matching the user's stated view over truthful ones a non-negligible fraction of the time — a verifier inherits a prior toward agreeing with the claim it's handed.
3. **Evaluating LLMs' Assessment of Mixed-Context Hallucination (Summarization lens)** — Qi, Cao, He, Yuan (2025). arXiv:2503.01670 — https://arxiv.org/abs/2503.01670
   Intrinsic world-knowledge biases the judge: a claim true-in-the-world but unstated-in-source gets false-confirmed (failure class b).
4. **Language Models Are Poor Learners of Directional Inference** — Li, Hosseini, Weber, Steedman (2022). arXiv:2210.04695 — https://arxiv.org/abs/2210.04695
   Models look competent on standard NLI but fail at directionality (A→B vs B→A), exploiting artifacts — the structural reason an inverted claim ("looser degrades more" vs "stricter degrades more") slips through (failure class a).
5. **LLMs as Factual Reasoners: Insights from Existing Benchmarks and Beyond** — Laban et al. (2023). arXiv:2305.14540 — https://arxiv.org/abs/2305.14540
   On SummEdits (edit-level consistency) most LLMs score near random and even GPT-4 is 8% below humans; bare "is this supported?" prompting is unreliable for subtle edits like inversions.
6. **Fact in Fragments: Atomic Fact Extraction and Verification** — Zheng et al. (2025). arXiv:2506.07446 — https://arxiv.org/abs/2506.07446
   Decomposing a claim into atomic facts and checking each against the source raises precision and makes the specific unsupported atom visible — the direct mitigation for plausible-but-unstated additions.
7. **Sycophancy under Pressure: Mitigating Sycophantic Bias via Adversarial Dialogues** — Zhang et al. (2025). arXiv:2508.13743 — https://arxiv.org/abs/2508.13743
   Pressure-Tune trains on adversarial dialogues + CoT that reject misinformation, raising sycophancy resistance without hurting accuracy — reasoning that explicitly contests a claim reduces false-confirms.
8. **Overconfidence in LLM-as-a-Judge: Diagnosis and Confidence-Driven Solution** — Tian et al. (2025). arXiv:2508.06225 — https://arxiv.org/abs/2508.06225
   The "Overconfidence Phenomenon": a verifier's CONFIRMED carries inflated confidence; calibration/fusion yields risk-aware judgments — supports an abstain/flag threshold over a binary confirm.

**Design implication:** harden the verifier's system prompt with two explicit decompositional sub-checks — (a) a DIRECTION check (does the claim reverse/weaken/strengthen the source's stated relationship? → not supported) and (b) an UNSUPPORTED-SPECIFICS check (flag any entity/number/ranking not literally in the source, even if plausibly true) — run per atomic claim with an abstain/insufficient option. The literature predicts this measurably reduces both failure classes (4, 6, 7 directly; 1–3 explain why the default fails), BUT prompt-only mitigation is PARTIAL — directional and sycophantic biases are training-baked, so the durable fix pairs the hardened prompt with an external different-family verifier and calibrated abstention.
