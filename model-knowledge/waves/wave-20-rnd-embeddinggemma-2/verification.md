# Wave 20 — verification

**Dispatch:** [`dispatch.md`](dispatch.md)

**Runner:** the R&D seat, 2026-10-20.

**Verifier maturity, stated plainly:**
- This check reads receipts and the primary source. No second model family reviewed the wave.
- The figures are a vendor's model card and the studio's own pre-registered benchmark, so under the studio's
  proportional-verification rule a receipt check is the right depth.

## Result

| fact | verdict | checked against |
|---|---|---|
| MTEB at 768d: multilingual v2 61.36, English v2 68.46, code v1 78.68; EmbeddingGemma 1 61.15 and 68.76 | confirmed | the Hugging Face model card at rev 914f7f89 (last modified 2026-10-06), fetched 2026-10-20: lines 80–81 (the 768d table, both models) and 96 (the truncation table's 768d row) |
| MTEB at 256d: English v2 67.78, code 76.18 | confirmed | the card, line 98 |
| float16 overflows: NaN or silently degraded vectors | confirmed | the card, lines 189–191 |
| Apache 2.0, not gated | confirmed | the card's licence (line 2, and the License link at line 32), and the Hub API's `gated: false`, 2026-10-20 |
| a term of use: deployments follow the Gemma Prohibited Use Policy | confirmed | the card, line 282 (added on the Publisher's review) |
| +0.112 dense nDCG@10 [+0.065]; prose +0.041, code +0.174; 93 of 100 queries scored | confirmed | rnd `experiments/embeddinggemma-2/results.md` lines 11 and 26–29 |
| 256d: −0.043, lower bound −0.062, fails | confirmed | results.md lines 39–40 |
| 2.6 chunks a second, against 5.6 | confirmed | results.md line 66: 11,525 chunks in 4,425 s, against 2,046 s for nomic-embed-text |
| sizes, the 1.49 GB file, the Ollama refusal, the CPU smoke run | confirmed | the bench's verified claims of 2026-10-15 (R&D smoke run, sha256 check, `ollama pull`) |

## Bench claims and what happened to them

- **Loaded, verified on the bench:** the CPU smoke run, the file's sha, the Ollama refusal, the benchmark result, the
  256d failure and the rates.
- **Loaded, unverified on the bench:** the three model-card claims. All three are on the card as stated, so they're
  verified here. The bench entry is updated in a follow-up change.

**Net:** 1 row, confirmed; 3 bench-unverified claims verified against the primary source; 0 fabricated.
