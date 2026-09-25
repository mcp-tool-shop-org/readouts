# Wave 4 — Verification receipt

Same method as prior waves (reasoning-stripped adversarial verifier + `WebFetch` retrieval oracle; same-family, family-different path still the planned upgrade).

## Verdict distribution

**11 models · 8 `confirmed` · 3 `confirmed-with-fixes` · 0 `unverified` · 0 `refuted`.** Commercial: **9 yes / 1 conditional / 1 no**.

## Material catches

| Item | Catch |
|---|---|
| **SCNet-large / XL** | Confirmed MIT (starrytong repo + ZFTurbo MSST framework); SDR claims verified against the MSST table; VRAM minimums are inference-floor estimates, not the A6000-class *training* figure. |
| **Wan2.2-Fun-Control / Control-Camera** | Confirmed **Apache-2.0** on the alibaba-pai cards — the Fun fine-tunes do **not** inherit more-restrictive base-Wan terms; QuantStack GGUFs inherit Apache. |
| **FLUX.2 klein rows** | Confirmed: **4B base / FP8 / NVFP4 = Apache** (commercial-safe); **9B base = FLUX Non-Commercial**. Two distinct axes (distilled-vs-base, 4B-vs-9B) — repos verified to exist on HF. |
| **UVR5** | GUI app is MIT, but it's a *front-end* — commercial use of separated audio depends on the specific model checkpoint run through it (`commercial_use: conditional`). |

## Queue status

**Drained.** Every verifier-flagged candidate from waves 1–3 is now cataloged or consciously declined. Future waves are optional and topic-driven (e.g. a new domain, or a refresh when a major model ships).
