# Wave 20 — promoted from rnd: judges, juries and planted pairs

**KB** `training-knowledge` · **dispatched** 2026-10-20 · **0** research agents (a promotion) · lanes `evaluation`,
`llm-finetune` · trigger: the readouts promotion queue. It covers two of the R&D bench's 2026-10-08 design entries on
critics and judges: *three follow-up studies for critic recipes* and *dataset recipes for critic jury roles*. Only
their verified claims load.

**Consumer:** aspire-si, the planted-defect programme, and every second-rater or jury design in the studio.

**Headline:**
- A judge's last misses on planted pairs can be real errors it's right about. The studio's planted-pair pipeline
  never checks that a plant is an error.
- On natural errors, gemma4:31b catches almost every flawed answer, and a second judge from another family recovers
  the error sentences it misses.
- The literature agrees on four design rules:
  - personas don't help a judge;
  - train a judge on both answer orders;
  - strong models make correlated errors;
  - a small, diverse panel is a strong default.

---

## Research grounding

**From the studio's rigs (measured-on-rig):**
1. **The hardest planted pairs are real errors.**
   - The Kev-4B judge fine-tune misses 2–3 of aspire-si's 149 confirmation pairs per seed averaged over both orders
     (2 shared by all seeds), and 10–12 pairs as a single choice (9 shared).
   - The hardest are genuine errors, such as "must be" changed to "is usually" known at compile time.
   - aspire-si's filters check truncation, no edit, similarity, length change and self-flag markers. None checks that
     the plant is an error.
   - **Implication:** verify plants before reading a judge's misses as judge error.
2. **Natural errors and local screen judges.**
   - On 95 labelled llama3.1:8b answers, a three-judge local screen flagged all 59 flawed answers but only 70% of the
     error sentences.
   - gemma4:31b alone: recall 0.97, precision 0.72.
   - muse-glimmer: 0.86 and 0.86, and 81% of sentences. The two together cover 93%.
   - The labels are model-made: one Opus pass and four blind Sonnet passes, Opus adjudicating the disagreements
     (Opus and Sonnet agree at kappa 0.63). There's no human gold.
   - **Implication:** use gemma4:31b as the high-recall first pass, and pair it with a judge from another family.

**From the literature (paper; checked at the source):**
3. **Judges miss natural errors.** On REALMistake, GPT-4 and Claude 3 detect natural LLM errors at low recall, and
   majority voting doesn't help (Kamoi et al. 2024).
4. **Personas don't make a judge.** Across 162 personas and 4 families, a persona didn't improve factual accuracy
   (Zheng et al. 2023).
5. **How to train a judge:**
   - Self-Taught Evaluators: Llama-3-70B goes from 75.4 to 88.3 on RewardBench, and modified-instruction negatives beat
     prompted bad answers, 83.8 against 80.7.
   - Prometheus 2: train pointwise and pairwise separately, then merge weights (0.670 Pearson against 0.595).
   - JudgeLM: swap augmentation raises order consistency from 73.45% to 78.89%.
6. **Juries:**
   - Models that both err pick the same wrong answer about 60% of the time on HELM, more so for larger models (Kim et
     al. 2025).
   - Judges favour similar models (Goel et al. 2025).
   - A panel (PoLL) leads single judges on two of three QA sets and trails Haiku on HotpotQA (Verga et al. 2024).
7. **Hard versus easy data:**
   - JTT closes 75% of the worst-group gap by upweighting a first model's errors (Liu et al. 2021).
   - Easy training data often matches hard (Hase et al. 2024).

## What the promotion changed

- **Three figures corrected on the way in:**
  - the fine-tune's single-choice misses are 10–12 pairs, not 9–12;
  - PoLL's best single judge on TriviaQA is CMD-R at 0.902, and PoLL trails Haiku on HotpotQA;
  - Kim et al.'s 60% is for one leaderboard dataset (HELM).
- **FELM's licence is CC BY-NC-SA 4.0:** internal evaluation only.
- **Not loaded:**
  - the entries' unverified claims, which cite literature from memory or search snippets;
  - the role-os specialists claim, which is internal tooling.

## The honest limit

- The rig rows rest on one judge fine-tune and 95 natural answers with model-made labels.
- The literature rows are the papers' own results, read from abstracts and tables, not reproduced.

## Provenance

Promoted from rnd entries
[`2026-10-08-three-follow-up-studies-for-critic-recipes-hard-pairs-two-pl`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-08-three-follow-up-studies-for-critic-recipes-hard-pairs-two-pl.md)
and
[`2026-10-08-dataset-recipes-for-critic-jury-roles-designing-roles-by-dat`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-08-dataset-recipes-for-critic-jury-roles-designing-roles-by-dat.md).
See [`verification.md`](verification.md).
