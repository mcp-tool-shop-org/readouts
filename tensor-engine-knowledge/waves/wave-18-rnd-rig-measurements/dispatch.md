# Wave 18 — promoted from rnd: rig measurements and engine recipes

**Promotion wave** · 2026-10-13 · **not a research swarm.** Every row is promoted from the studio's public research
bench, [rnd](https://github.com/mcp-tool-shop-org/rnd), where each topic's load-bearing claims were already checked
against a primary record. The measurements are interlock's pre-registered experiments, whose receipts are committed in
[interlock](https://github.com/mcp-tool-shop-org/interlock). The recipes come from defects the harnesses met on the rig.

## Why now

readouts is updated daily when there is something to publish (2026-10-13). Nothing from rnd had reached a knowledge
base before this wave. These six topics were the first whose claims were all verified, and they all belong to this
KB's subject: the engines and runtimes that run models on the studio rig.

## What it adds (12 rows in `config_recipes`)

| Lane | Kind | Row |
|---|---|---|
| profiling-bench | baseline | E5's method: the largest context window that stays on the RTX 5090, and how it is measured |
| profiling-bench | baseline | one row per model: llama3.1:8b 131,072 · gemma4:31b 86,016 · granite4.1:30b 43,008 · qwen3:14b 40,960 · qwen3:8b 40,960 · mistral-small:24b 32,768 |
| profiling-bench | baseline | E4b: the 5090 keeps its decode speed beside the Intel NPU or iGPU, and they keep theirs beside it (all four pairs within ±10%) |
| llm-inference | recipe | Ollama: `num_predict` 0, null or missing means no completion limit |
| llm-inference | recipe | Counting a long prompt's tokens through Ollama: estimate, then bisect the tail |
| runtime-foundations | baseline | The rig's CUDA stack (driver, nvcc, the two torch builds, sm_120) |
| runtime-foundations | recipe | Checking a rented GPU host's driver and download speed before paying |

E5's per-model rows extend wave 4's baselines. Wave 4 measured speed, power and heat at each model's default context.
E5 measures how much context each model can hold on the same card, three Ollama releases later.

## Method

- **Selection:** rnd entries whose claims were all `[verified]`, each `via:` a named receipt, run log or on-rig call,
  and whose subject is an engine or runtime on the rig.
- **Rows:** the figures are copied from the rnd entry's verified claims and key points, in new words. Each row links its
  rnd entry, which links the receipts.
- **No new measurement was taken for this wave.**

See [verification.md](verification.md) for how each row's figures were checked.
