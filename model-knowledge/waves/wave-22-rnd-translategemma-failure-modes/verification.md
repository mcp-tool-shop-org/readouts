# Wave 22 — verification

**Dispatch:** [`dispatch.md`](dispatch.md)

**Runner:** a Sonnet subagent made the first pass on 2026-10-20. The R&D seat then re-read:
- ai-jam-sessions commit 5f8d1e2: the README.zh.md diff and the message, "two Chinese cells and Hindi's transliterated
  'Kimi-K3' corrected by hand";
- commit e4cd2fb's message ("Hindi's transliterated 'Kimi-K3' restored to the name");
- the `.polyglot-cache.json` at those commits;
- TranslateGemma's licence fields through the Hugging Face Hub API.

**Verifier maturity, stated plainly:** retrieval against committed history and the Hub API only. No second model
family.

## Result

| fact | verdict | checked against |
|---|---|---|
| Chinese reversed count | confirmed | 5f8d1e2 README.zh.md diff: `218 首中的 224 首` → `218/224` |
| Chinese ordinal | confirmed | the cache at 5f8d1e2 holds `414个中的第285个`; main's cache holds none; 5f8d1e2's message records the hand fix |
| Hindi transliteration, and its return | confirmed | the cache at e4cd2fb holds `किमी-के3`; e4cd2fb's message records the first hand fix; 5f8d1e2's message records the second |
| licence | confirmed | Hub API for google/translategemma-27b-it: `license: gemma`, `gated: manual` |

## Reasons for leaving claims out, checked

- **"The pattern generalises":** there's no receipt beyond this README, so it stays unverified on the bench.

**Net:** 1 row, confirmed; 0 fabricated.
