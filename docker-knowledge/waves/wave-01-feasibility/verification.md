# Wave 1 — Verification receipt

The study-swarm **EXTERNAL_VERIFIER** stage, applied to this wave's own citations before any row was trusted.

## Method

Three decorrelated lenses, **reasoning-stripped** (each verifier saw only the bare citation claims — title / authors / year / one-sentence finding — never the synthesis reasoning):

1. **Retrieval oracle** — `WebFetch` against arXiv / DOI / official docs: existence + attribution + content-groundedness. **The authority on existence.**
2. **mistral-small:24b** (Mistral) — family-different groundedness lens.
3. **granite4.1:30b** (IBM Granite) — family-different groundedness lens.

This is the **family-different** verification (retrieval oracle + two *local non-Claude* models on this rig) that the sibling KBs — `tensor-engine-knowledge`, `model-knowledge` — list as their deferred **P1 upgrade**. So wave-01 here lands at the maturity those KBs are still working toward. Source swarm: `wf_965f110f-e24`; ollama run-ids in the gpu-container feasibility receipt.

## Verdict distribution

**35 unique sources · 0 fabricated.** Every citation resolved to a real source. Both LLM families false-flagged genuine 2025–26 papers as "nonexistent" (the no-retrieval blind spot) — discarded for existence; the oracle governs that axis. Granite correctly marked recent papers `UNSURE`; mistral was an over-skeptic (flagged oracle-confirmed facts as implausible, even hallucinated a wrong-year objection) — its `NO`s on confirmed sources were discarded. The **union** caught what neither caught alone.

## Material actions (none changed a verdict)

- **DROPPED — misattribution:** "Auxiliary-Loss-Free Load Balancing" (arXiv:2408.15664) is a real, correctly-attributed paper, but the *inference-skew* claim is **not in it** (it is training-only). The skew premise survives on MoE-Infinity + MoE-Beyond + SpecMD.
- **DROPPED — unsupported numbers:** a `localllm.in` page that was actually about different models (Qwen3.5 / GLM), not the 70B figures attributed to it.
- **CORRECTED (~8 sub-figures):** KTransformers single-socket decode 10.3 → ~8.7 tok/s (live drift); ExpertFlow "95% accuracy" unsupported (number dropped); FlexGen "9 LP variables" → 11; a Pre-gated SQuAD F1 misread; NVIDIA oversubscription-blog authors → Garg & Sakharnykh; SSD-hierarchy outlet → Tom's Hardware; MoE-Beyond year 2024 → 2025.
- **FLAGGED:** SpecMoEOff is speculative *decoding* (more tokens verified per transfer), not predictive *prefetch* — not carried as prefetch evidence.

## Deferred

Wave 2 (`container-runtime` + `hw-measurement`) will run through the same 3-lens, family-different path.
