# Wave 20 — promoted from rnd: EmbeddingGemma 2 and its studio benchmark

**KB** `model-knowledge` · **dispatched** 2026-10-20 · **0** research agents (a promotion) · lane `llm` · trigger:
the readouts promotion queue. The R&D seat chose this topic from the 2026-10-20 queue because studio tools use it:
offrig adopts it, and dataset-desk ships an `eg2` backend.

**Headline:**
- EmbeddingGemma 2 is Google DeepMind's open embedder. It maps text, code, images, video and audio into one
  768-dimension space, Apache 2.0 and not gated. The card asks deployments to follow the Gemma Prohibited Use Policy.
- On the studio's own pre-registered benchmark it beat offrig's embedder, nomic-embed-text, by +0.112 dense nDCG@10,
  with a one-sided 95% lower bound of +0.065.
- Never run it in float16. The model card says its activations overflow, and it returns NaN or silently degraded
  vectors.

## What it adds (1 row in `models`, lane llm)

| Fact | Source | Status |
|---|---|---|
| Sizes: 740M in full, text-only 270M, text+image 440M, text+audio 570M; one 1.49 GB safetensors file | model card; the bench's sha check | verified |
| Matryoshka cuts to 512, 256 and 128 dimensions; task prefixes | model card | verified |
| MTEB multilingual v2 61.36, English v2 68.46, code v1 78.68 at 768d; 67.78 and 76.18 at 256d; EmbeddingGemma 1 61.15 and 68.76 | model card, rev 914f7f89 | verified here (unverified on the bench) |
| bfloat16 or float32 only: float16 overflows | model card | verified here (unverified on the bench) |
| +0.112 dense nDCG@10 over nomic-embed-text [+0.065], code +0.174, prose +0.041, on 93 queries | rnd benchmark, results.md | verified |
| The 256d cut loses 0.043 [−0.062] and fails its bar | rnd benchmark | verified |
| 2.6 chunks a second on the rig's CPU in float32, against nomic's 5.6 on CPU Ollama | rnd benchmark | verified |
| Ollama 0.40.4 on Windows refuses every library tag (MLX tensor builds) | the bench, 2026-10-15 | verified |

**The lane.** model-knowledge has no embeddings lane. The row goes in `llm` (Local LLM + vision), the closest fit.

## The honest limit

- The benchmark is the studio's: 93 queries over offrig's corpus, scored after offrig's int8 quantization, on one
  rig's CPU. It decides for offrig; it isn't a general ranking.
- The MTEB figures are Google's own, as stated on the card.
- Multimodal use wasn't measured here.

## Provenance

Promoted from rnd entry
[`embeddinggemma-2`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/embeddinggemma-2.md), with the
benchmark in
[`experiments/embeddinggemma-2/results.md`](https://github.com/mcp-tool-shop-org/rnd/blob/main/experiments/embeddinggemma-2/results.md).
See [`verification.md`](verification.md).
