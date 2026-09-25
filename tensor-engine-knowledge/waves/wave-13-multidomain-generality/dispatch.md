# Wave 13 — generality test (physical sciences) + a disagreement-gated consensus

**Date:** 2026-06-03 · **Mode:** hands-on + measured on the live RTX 5090 / llama-swap :9090 · **Recipe:** #176

## Goal

Two wave-12 NEXTs:
1. **Generality.** The orthogonal NLI seat aced AI/ML citation traps (waves 10–11, 100%). But those abstracts
   are all one domain. Does the seat hold on a *different* domain with alien vocabulary and dense numerics?
2. **The #26 residual.** The monotone-safe floor can only downgrade a `supported`, so it can't fix a case
   where the LLM panel confidently *refutes* a true claim but the NLI seat is right. A **consensus gate**
   escalates instead: `supported` only if both mechanisms agree; a disagreement on the supported axis →
   `insufficient` (review) — the UNCERTAINTY_GATED_HUMANS standard made concrete.

## Hypotheses (to be measured)

- **H1:** the NLI seat generalizes (stays high-accuracy / 0-fc) on a non-AI/ML domain.
- **H2:** the consensus gate fixes #26 and preserves 0 false-confirms.

## Plan

1. Fetch 5 real physical-sciences abstracts into a **separate** cache (`abstracts-cache-multidomain.json`):
   LIGO GW150914, ATLAS + CMS Higgs, Planck 2015 cosmology, EHT M87 — gravitational waves / particle physics
   / cosmology / black-hole imaging, all numeric-heavy. (`_wave13_fetch.py`, Semantic Scholar, sha-pinned.)
2. Author 17 gold-verified cases against the **real** fetched text (`citations-multidomain.json`): numeric
   (36+29→"~65 M☉"), inversion, scope/added-entity, **unit** (42 µas vs the trap "42 mas"), paraphrase.
3. Measure (`citation_panel_eval_multidomain.py`): NLI doc-level, the LLM panel **live** on offload's
   *promoted* wave-12 default, the floor, and the consensus gate. Regression the consensus on the 39 AI/ML
   cases (incl. #26).
4. Record as wave 13 (`scripts/_wave13_multidomain.py`, recipe #176) + regen. Report **honestly** — if the
   generality test breaks the seat, that is the finding.

## Verifier

Gold hand-verified against the real sha-pinned abstracts; the LLM panel and the NLI seat cross-check each
other; false-confirms are the safety metric. A generality test that *found nothing* would be the suspicious
outcome. See `verification.md`.
