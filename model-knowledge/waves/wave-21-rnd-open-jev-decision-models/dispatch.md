# Wave 21 — promoted from rnd: open Jev-style decision models, and the studio's Kev runs

**KB** `model-knowledge` · **dispatched** 2026-10-20 · **0** research agents (a promotion) · lane `llm` · trigger:
the readouts promotion queue. It comes from the rnd entry with the most verified claims in the 2026-10-20 queue.

**Headline:**
- Kev is an open, Apache-2.0 family of Jev-style decision models. As a forecaster on sense-si, the studio measured it no
  better than the base rate.
- As a judge of planted errors, Kev-4B is badly position-biased as a single choice. Averaged over both orders it scores
  0.973 on 149 fresh pairs, ahead of Qwen2.5-32B's 0.886.
- A 22-minute fine-tune removes the position bias on three of three seeds, and it carries over to a different planter.

## What it adds (6 rows in `sources`, lane llm)

| Row | Evidence | Kind |
|---|---|---|
| Kev: sizes, bases, Apache-2.0, no Jev outputs used; self-reported 0.851 / 0.889 against Jev's 0.857; the trainer fails on native Windows | Kev README and source, read 2026-10-20 | project's own statement |
| Kev-4B and Kev-9B on sense-si: Brier 0.240 / 0.242 against a 0.242 base rate; AUC 0.54 / 0.52; a knowledge prompt didn't help | rnd `experiments/openjev-vs-jev` result files | rig measurement |
| Kev-4B as a judge: 0.547 as a single choice (A 95%), 0.973 averaged over both orders on 149 fresh pairs | aspire-si `kev-confirmation` report | rig measurement |
| The Kev-4B judge fine-tune: three of three seeds pass; 0.989 on gemma4:31b's plants | rnd `experiments/kev-judge-finetune` result files | rig measurement |
| Laya: 421M, Apache-2.0, about 33–40 ms a question; its fine-tuned checkpoint scores 0.766 on its authors' typed-decisions benchmark, against 0.362 base (no committed result file yet, by the README) | Laya README and card | project's own statement |
| Bespoke-Nimble-9B: 90.12% agreement with reference labels, against Jev's 93.21% | Nimble README and card | project's own statement |

## What the promotion corrected

The re-read changed three things against the bench copy:
- **Laya's "Apple MPS" timing** is PyTorch MPS on an AMD Radeon Pro Vega II in an Intel Mac Pro, not Apple Silicon.
- **Nimble's "about 90% of Jev's answers"** is agreement with synthetic reference labels, on which Jev itself scores
  93.21%.
- **Kev's "3–5k-token requests"** are 1,562 to 4,721 tokens, median 3,045.

**Not loaded:**
- claims with no committed receipt: the four unrelated "OpenJev" projects, and TypeSafe's terms;
- Kev-9B's memory figures, which are prose with no log;
- Laya's comparison with Jev, whose figures the authors took from third parties and never measured;
- the `--init_from` anecdote, one user's report in Kev's README.

## The honest limit

- The sense-si result is 124 records; the judge results are single planted errors in long answers.
- The vendor figures are the projects' own.
- The fine-tune's adapters are private and aren't part of this wave.

## Provenance

Promoted from rnd entry
[`2026-10-07-open-jev-style-decision-models`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-07-open-jev-style-decision-models.md).
See [`verification.md`](verification.md).
