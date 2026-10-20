# Wave 19 — promoted from rnd: more prompts, the critic's initial weights, and a found Auditor

**KB** `training-knowledge` · **dispatched** 2026-10-20 · **0** research agents (a promotion) · lanes
`rl-measurement-methodology`, `evaluation` · trigger: the readouts promotion queue. The R&D seat chose this topic from
the 2026-10-20 queue. It continues wave 18's critic results with aspire-si's runs of 2026-10-08.

**Consumer:** any studio work that trains a learned critic: aspire-si, the planted-defect programme, and every
second-rater design.

**Headline.** Three measurements from aspire-si's 2026-10-08 runs, each with a committed run report and a readout
committed before it ran.
- Four times the training prompts lifts every critic's accuracy, but not the spread between seeds.
- A critic's initial weights can invert it, and the run seed also moves it.
- The inverted critic still prefers the flawed answer on fresh pairs, so it reads as an auditor.

---

## Research grounding

1. **More prompts raise the level, not the spread.**
   - At 128 training prompts instead of 32, every seed rose by 0.10 to 0.13. The mean went from 0.635 to 0.745 on 127
     planted-error pairs.
   - The range between seeds stayed 0.181 at both prompt counts, so the pre-registered spread rule failed.
   - Epoch 1, where ASPIRE generates its dialogues, set the run time: about 1.67 min per dialogue per seed with three
     seeds side by side. Epochs 2 and 3 took about 5 min.
   - **Implication:** more prompts are worth having, but one seed still can't be trusted. Plan rented-GPU time from
     epoch 1.
2. **Both seeds carry the spread, and one critic init inverted the critic.**
   - Critic seed 43 scored 0.315, with its whole interval below 0.5: it learned to prefer the flawed answer.
   - Critic init alone spanned 0.488, and the run seed alone 0.283, against a noise floor of 0.055 from one identical
     repeat.
   - The 0.488 is one draw: without the 0.315 run, the other two critic seeds differ by 0.016.
   - Generation isn't reproducible on the pod GPU: 0 of 32 dialogues matched between identical-seed runs.
   - **Implication:** never ship a single critic unchecked. Train several inits, select on a held-out validation set
     (never the judge set), and reject any critic below 0.5.
3. **The inverted critic holds on fresh pairs.**
   - On 149 confirmation pairs it was never read on, it prefers the flawed answer on 0.678 [0.582, 0.763], against
     0.685 where it was found.
   - Re-scored on the local card, it matches the pod: 123 of 127 decisions, median score difference 0.002.
   - Its margins are tiny, about 0.01 on average.
   - **Implication:** 0.678 on validation is the bar a trained Auditor has to beat, with a paired interval.

## What the promotion changed

- **One claim unverified on the bench loads here:** the epoch-1 rate of about 1.67 min per dialogue is in the step-2
  report's timing table.
- **Not loaded:** the entry's early hypothesis that the spread comes from the critic head's init or student sampling.
  The critic-init test superseded it.
- **Added from the receipts:** the critic-init range of 0.488 rests on a single draw. Also, the Auditor plan's
  trained-head readings were all stopped, because the shuffled-label control failed; only the found Auditor's reading
  stands.

## The honest limit

- One student size (1.5B) and three seeds per arm. The noise floor rests on one repeat, so the ranges are rough.
- The run-seed arm bundles adapter init, data order and sampling with generation noise, and this test can't separate
  them.
- One found Auditor, with margins small enough that about a quarter of judge pairs fall within the local–pod
  difference.

## Provenance

Promoted from rnd entry
[`2026-10-08-more-prompts-raise-the-aspire-critic-s-accuracy-but-not-its-`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-08-more-prompts-raise-the-aspire-critic-s-accuracy-but-not-its-.md).
It was re-read against aspire-si's run reports at commit b8ab54d on 2026-10-20. The full receipt is in
[`verification.md`](verification.md).
