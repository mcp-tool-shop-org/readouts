---
title: Getting a small local model to tell the truth
description: A text survival game lets a small local model write the prose and a rule checker keep it honest. Five measured sessions took rejected lines from 61.5% to 8.1%, then a truth check, then a comparison with larger local models and four Claude models.
date: 2026-11-13
---

Every figure on this page is taken from the receipts filed in the public rnd repository under
[`experiments/etv-narrator/`](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/etv-narrator)
(sessions 1 to 5 and the Claude API comparison). Claims are as measured by the harness. Nothing has had a second check
except where a line says so.

## The problem

Escape the Valley is a text survival game. The engine decides what happens on each turn, and a small language model
running on the player's own machine writes the prose. It writes two lines per turn, a scene and an outcome, in one of
three voices (Chronicler, Fireside, Uncanny Bearer) and at one of three lengths (Brief, Standard, Rich).

A narrator that invents facts is worse than no narrator. So every line passes a rule checker:

- no invented numbers or supplies;
- no deaths that didn't happen;
- no copying the event text;
- length caps.

A line that fails is replaced by the game's own plain line.

Each measurement asks the model for every slot of a fixed, hash-pinned set of 360 turns: 3 voices × 3 lengths × 2
lines, or 6,480 lines per arm. The model is `qwen3:4b-instruct-2507` (q4_K_M) on one RTX 5090.

Receipts: [experiment folder](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/etv-narrator).

## What it took (one day, five sessions)

| Session | What changed | Result |
|---|---|---|
| 1 | The first honest measurement | 61.5% of lines rejected. Most rejections were the rules and the prompt contradicting each other, not the model. |
| 2 | First fixes (word caps, unit words, apostrophes) | 55.5% rejected. Rich improved a lot; Standard got worse because the model read the word cap as a target. |
| 3 | Seven arms, paired by turn | The best combination cut rejections to **8.1%**: a prompt stating the rulings, up to 3 candidates, deterministic trimming and the model card's sampling. That is +47.4 points of accepted lines (95% interval +45.1 to +49.7). The unquantised model was *worse* (66.8%), and so was positive wording. |
| 3 (reading) | 29 accepted lines, read by hand | **Accepted is not good.** 7 of 29 contradicted the facts, for example "No water" on a turn where water was found. No victory line said the journey had ended. |
| 4 | "Says what happened": truth rules, the outcome line leads with the main fact, no repeated openings | 82.9% of all lines now pass every rule *and* say what happened. Endings, deaths and arrivals are carried on 90.5%, 85.3% and 71.8% of the lines asked for. No false "supply gone" lines. |
| 5 | Four larger or newer local models on the same shape | None beats the 4B. 8B is level; the 14B and Qwen 3.5 models are worse. |

Receipts: sessions
[1](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/etv-narrator/results/s1),
[2](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/etv-narrator/results/s2-recheck),
[3](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/etv-narrator/results/s3-arms),
[4](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/etv-narrator/results/s4-says-what-happened),
[5](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/etv-narrator/s5-larger-local).

Two lessons came out of this:

- **Measure the checker, not just the model.** Most early "model failures" were our own rules colliding.
- **Read the lines.** Session 3's 8.1% looked done; reading 29 of its lines showed the remaining work.

## Local against cloud

These rates are re-scored under the same two checker corrections: choice parroting now counts only when verbatim, and a
repeated opening means the same first three words. The paired differences are against the local 4B on the same turns.

| Narrator | Good lines | Paired vs local | Time per turn (p50) | Cost per line |
|---|---|---|---|---|
| Local qwen3:4b (ship) | 85.7% (all 6,480) | n/a | 0.36 s | free, on the player's machine |
| Claude Haiku 5.5 | 85.4% | −0.3 (−2.3 to +1.6) | 4.3 s | about $0.0002 |
| Claude Sonnet 5.5 (Fireside Brief, 720 lines) | 89.3% vs local 85.1% | +4.2 (+0.9 to +7.4) | 5.5 s | about $0.003 |
| Claude Opus 5.5 (Standard, 2,160 lines) | 89.3% vs local 86.1% | +3.2 (+0.9 to +5.5) | 7.6 s | about $0.011 |
| Claude Fable 5.2 (Standard, 2,160 lines) | 91.5% vs local 86.1% | +5.4 (+3.3 to +7.5) | 3.5 s | about $0.018 |

![Dot-and-whisker chart of the paired difference in good lines between each Claude model and the local 4B, with 95% intervals. Haiku is level with zero; Sonnet, Opus and Fable sit to the right of it.](/readouts/results/etv-narrator-local-vs-cloud.svg)

*Chart description.* Four rows, one per Claude model, each showing the paired difference in good lines against the
local model on the same turns. Haiku (all lines) is about level (−0.3, interval −2.3 to +1.6, straddling zero). Sonnet
on Fireside Brief (+4.2), Opus on Standard (+3.2) and Fable on Standard (+5.4) have intervals that stay above zero.
Each row compares a different subset of turns, so the rows are not a ranking of the models against one another.

Reading them side by side, the cloud models write the length Standard asks for, while the local model's Standard lines
are often clipped. The cloud models also invent small details (an extra river, an invented "old rule") without breaking
the game's facts. The Claude test cost $66.31 of a $75 cap.

Before the two checker corrections the order was the other way: on the Standard cells the local model passed 84.1% of
lines against 80.7% (Fable), 78.8% (Opus) and 76.2% (Haiku), mostly because of the choice-parroting rule. The
latency in the table is for the whole turn, including the network.

Receipts: [cloud-claude](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/etv-narrator/cloud-claude)
(run record and tables) and the
[re-score](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/etv-narrator/results/s4-says-what-happened).

## Speed by hardware (the local model, p50 seconds per turn)

Fireside voice, one RTX 5090 with part of the model moved onto the CPU.

| Where the model runs | Brief | Standard | Rich |
|---|---|---|---|
| All on the GPU | 0.17 | 0.43 | 0.76 |
| Half on the GPU | 0.9 | 3.6 | 6.3 |
| A quarter on the GPU | 1.3 | 4.4 | 8.8 |
| CPU only | 3.9 | 8.3 | 13.4 |

![Grouped bar chart of seconds per turn at Brief, Standard and Rich for four placements of the model: all on the GPU, half, a quarter, and CPU only. Time rises steeply as less of the model is on the GPU.](/readouts/results/etv-narrator-speed-by-hardware.svg)

*Chart description.* Four groups of three bars. With the whole model on the GPU a turn takes under a second at every
length. With half the model on the GPU a Standard turn takes 3.6 s, and on the CPU alone it takes 8.3 s at Standard and
13.4 s at Rich. These figures are from this machine's CPU paired with the GPU; a weaker card with the whole model on it
was not measured.

Receipts: [session 4](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/etv-narrator/results/s4-says-what-happened)
(latency with fewer layers on the GPU).

That leads to the design:

- **Small and local by default, at Brief.**
- **Claude as the cloud default** for richer narration, with the player's own key.
- **Other providers easy to pick:** another Ollama model, OpenRouter.
- The wait is hidden by starting early, caching and sound, rather than by cutting what the narrator does.

## Honest caveats

- **Same sampling for every local model in session 5.** It ran 0.7 / 0.8 / 20 for all four, which overrode each
  package's own defaults, including Qwen 3.5's presence penalty. The comparison is fair, but the Qwen 3.5 models didn't
  run at their own card's settings.
- **The rules were tuned on the 4B,** so larger models may lose partly to that tuning. The 8B is to be re-measured after
  the next fixes, at its own card's sampling, as a possible "large local" tier.
- **Hand readings are one reader on 29 lines** each: direction only.
- **Cloud cells are subsets** (Standard for Opus and Fable, Fireside Brief for Sonnet). Haiku covered all 6,480.
- **One local session overlapped a short build** (marked in its record). Latency for those cells isn't comparable.
- **Open from reading session 5:** the larger model leaks the party's taboo ("no river water") into scenery, and once
  shows the party drinking from an invented river. A taboo rule is in the next fixes, as are choices conveyed, the
  pyrrhic-loss word and a Brief line that must add one concrete detail.

## What's next

The fixes PR (behind flags), then one live session that measures:

- the fixes on the 4B;
- the Brief detail cost;
- the 8B at its own sampling.
