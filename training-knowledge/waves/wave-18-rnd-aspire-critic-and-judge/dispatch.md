# Wave 18 — promoted from rnd: the ASPIRE critic's seed variance, and scoring a judge in both orders

**KB** `training-knowledge` · **dispatched** 2026-10-20 · **0** research agents (a promotion) · lanes
`rl-measurement-methodology`, `evaluation` · trigger: the readouts promotion queue. The Director approved promoting these
two topics from the studio's research bench, [rnd](https://github.com/mcp-tool-shop-org/rnd), on 2026-10-20.

**Consumer:** any studio work that trains a learned critic or uses an LLM as a judge: aspire-si, the planted-defect
programme, and every second-rater design.

**Headline.** Two measurements from aspire-si's 2026-10-07 and 2026-10-08 runs, both with committed run reports.
- A learned critic's accuracy at 32 training prompts swings more between seeds than between treatments.
- An LLM judge read as a single A/B choice has total position bias in one order. Read from its option
  probabilities, averaged over both orders, the same judge separates strong from flawed answers well.

---

## Research grounding

1. **SFT before ASPIRE had no reliable effect on the critic.**
   - Seed 42 alone suggested SFT made the critic much worse: 0.866 against 0.646, on 127 planted-error pairs.
   - Under the pre-registered three-seed rule, the mean drop was 0.06 (composite teacher) and 0.008 (local teacher).
     Both are under the 0.10 bar.
   - The composite control critic ranged from 0.425 to 0.866 across seeds. Training loss didn't predict accuracy.
   - What did replicate is the drift: ASPIRE pulls representations in a fixed direction, opposite to SFT on teacher
     answers, in every seed and with both teachers.
   - **Implication:** three seeds per arm and a pre-registered rule before any critic comparison. Never select a critic
     by its loss.
2. **Score an LLM judge in both orders.**
   - Qwen2.5-32B-Instruct, as a single text choice, picked A on all 127 pairs when the strong answer was A, and the
     strong answer only 49 of 127 times when it was B.
   - Whole-number 0–10 scores tied 89 of 127 pairs.
   - Averaging the A/B option probabilities over both orders lifted the same model (Q4) to 0.886 on 149 fresh pairs and
     0.898 on the 127, from 0.685 and 0.701 on single choices.
   - **Implication:** every studio judge scores both orders and averages. Forced choice beats absolute scores. Plant
     controlled defects by a structured edit that code applies, never by asking a model to rewrite.

## What the promotion corrected

The rnd entries were the bench copies. Re-reading them against aspire-si's run reports changed one figure:
- **The single-choice baseline on the 127 judge-set pairs is 0.701, not 0.685.** 0.685 is the baseline on the 149
  fresh pairs. The rnd entry used 0.685 for both.

The SFT entry's id still says "weakens", because ids are kept so links resolve. This KB takes its corrected claim: no
reliable effect.

## The honest limit

- One student size (1.5B), 32 training prompts, and three seeds.
- A later aspire-si run at 128 prompts lifted every critic by 0.10–0.13 and left the spread between seeds unchanged.
- One judge model, measured on planted single-sentence errors.

## Provenance

Promoted from rnd entries
[`2026-10-07-sft-before-aspire-weakens-critic`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-07-sft-before-aspire-weakens-critic.md)
and
[`2026-10-07-qwen32b-judge-position-bias`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-07-qwen32b-judge-position-bias.md).
They were re-read against aspire-si's run reports at commit b8ab54d on 2026-10-20. The full receipt is in
[`verification.md`](verification.md).
