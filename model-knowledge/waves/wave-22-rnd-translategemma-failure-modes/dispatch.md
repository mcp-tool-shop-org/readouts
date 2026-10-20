# Wave 22 — promoted from rnd: TranslateGemma's failure modes on README tables

**KB** `model-knowledge` · **dispatched** 2026-10-20 · **0** research agents (a promotion) · lane `llm` · trigger:
the readouts promotion queue. The studio translates every release README locally with TranslateGemma 27B, so its slips
reach public pages.

**Headline:** TranslateGemma 27B is reliable on README prose. It slips on two things readers rely on, and the
translation cache can bring a slip back after a hand fix:
- counts written as "N of M";
- product and model names.

## What it adds (1 row in `sources`, lane llm)

| Fact | Evidence |
|---|---|
| Chinese: "218 of 224" came back reversed as "224 of 218" (218 首中的 224 首), and "285 of 414" as an ordinal, "the 285th of 414"; both were fixed by hand | ai-jam-sessions commit 5f8d1e2: the README.zh.md diff, its message, and the cache at that commit |
| Hindi: "Kimi-K3" was transliterated into Devanagari; restored by hand, it came back from the cache on the next run and was fixed again | commits e4cd2fb and 5f8d1e2 |
| The check: compare verbatim English lines before and after, read every "N of M" cell, and clear a hand-fixed entry from the cache | the entry's method |
| Licence: Gemma licence, gated on Hugging Face with manual approval | Hugging Face Hub API, 2026-10-20 |

## What the promotion changed

- **Not loaded:** whether the pattern holds beyond this one README. It's untested and stays unverified on the bench.
- **The licence line:** the model card is gated, so the licence is read from the Hub API. The row links the Gemma Terms of
  Use without interpreting them.

## The honest limit

One README, two languages, two runs. It's a pattern to check for, not a measured error rate.

## Provenance

Promoted from rnd entry
[`2026-10-08-translategemma-failure-modes-on-readme-tables`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-08-translategemma-failure-modes-on-readme-tables.md).
See [`verification.md`](verification.md).
