# Wave 1 — Verification receipt

> Adversarial retrieval-verifier per lane (Sonnet tier), currency + boundary + citation lenses · 2026-06-06.

**Researched:** 32 techniques · **loaded:** 31 · **excluded (refuted core claim):** 1.

## Verdict distribution

| Verdict | Count |
|---|--:|
| confirmed | 13 |
| confirmed-with-fixes | 18 |
| refuted | 1 |

## Evidence-strength distribution (loaded techniques)

| Tier | Count |
|---|--:|
| measured-on-rig | 6 |
| reproduced-from-source | 23 |
| community-claim | 2 |


**Sources:** 134 cited · 132 retrieval-verified (resolve + support the claim).

## Excluded by the verifier (ANDON — refuted, not loaded)

- **flux2-klein-4b-style-lora** (diffusion-flux-lora) — CORE CLAIM FAILURE: The technique asserts 'Mistral-3 single encoder' for FLUX.2 [klein] 4B and cites deepwiki:black-forest-labs/flux2/3.1 to support it. That DeepWiki section describes FLUX.2 dev, not klein. FLUX.2-klein-4B uses a Qwen3-4B text encoder, not Mistral-Small-3.2-24B. FLUX.2-klein-9B uses Qwen3-8B. The Mistral encoder is exclusive to FLUX.2 dev. This is confirmed by DeepWiki section 3.2 (text-encoders), the flux2 GitHub repo, musubi-tuner docs, and multiple HF community repos. The cited source (section 3.1) appears to be mis-scoped — it documents the dev model encoder. The technique name, slug, and claim all embed the wrong encoder family for this model variant. Requires correction: replace Mistral encoder claim with Qwen3-4B; update the citation to deepwiki:black-forest-labs/flux2/3.2-text-encoders or the official flux2 GitHub architecture docs.

_Excluded techniques remain in `research-raw.json` for provenance; they are not rows in `training.db`._

