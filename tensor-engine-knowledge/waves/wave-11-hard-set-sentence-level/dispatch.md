# Wave 11 — stress the orthogonal NLI seat + sentence-level evidence selection

**Date:** 2026-06-03 · **Mode:** hands-on + measured on the live RTX 5090 / llama-swap :9090 · **Recipe:** #174

## Goal (the wave-10 NEXT)

Wave-10 stood up the mechanistically-orthogonal NLI floor and it scored 100% on the 24-case set — but those
traps were **NLI-canonical** (inversions→contradiction, unstated→neutral), the model's home turf. Two follow-
ups: (1) **sentence-level FEVER-style evidence selection** for the floor, and (2) a **harder set** that stresses
the seat beyond canonical traps, to find its real limits and demonstrate (rather than assert) where the
**combination** (LLM panel + NLI floor) wins.

## Hypotheses (to be measured, not assumed)

- **H1:** a hard set built around NUMERIC/arithmetic, MULTI-HOP, SCOPE, and subtle PARAPHRASE will trip the
  encoder NLI seat (NLI models are documented to be weak at numeric and multi-step inference) — so the LLM
  panel earns its seat on the cases NLI can't do.
- **H2:** sentence-level selection (NLI claim-vs-each-sentence, max-aggregate) helps when the entailing
  evidence is one sentence buried in a long abstract; may hurt multi-hop claims that no single sentence
  entails. Net effect unknown.

## Grounding

- **Thorne et al. 2018 FEVER** (arXiv:1803.05355) — the sentence-selection + aggregation paradigm (find the
  evidence sentence(s), then classify SUPPORTS/REFUTES/NOT-ENOUGH-INFO). Sentence-level is the FEVER default;
  document-level trades sentence precision for cross-sentence context.
- NLI numeric/quantifier weakness is well-documented (e.g., NLI models struggle with counting, comparatives,
  and arithmetic entailment) — the motivation for H1.

## Plan

1. Author `citations-hard.json` — 15 cases grounded in the SAME 8 sha-pinned abstracts (no new fetches;
   reproducible), every gold label verified against the abstract text. Span: numeric (23/36 → "fewer than
   two-thirds" / "more than half"; N=199 → "roughly two hundred"), multi-hop, scope/added-entity, paraphrase-
   supported, harder inversions.
2. Add `verify_one_sentencewise()` to `nli_verify.py` (split → NLI per sentence → max-entailment /
   max-contradiction aggregate, asymmetric safety). Keep document-level (`verify_one`) the default.
3. Measure (`citation_panel_eval_hard.py`): NLI doc vs sentence; the LLM panel **live** on the hard set; and
   the combined floor (two veto rules — veto-on-not-supported vs veto-on-contradiction-only) to expose the
   safety (false-confirm) vs recall (over-escalation) trade. 24-case regression for sentence-level.
4. Record as wave 11 (`scripts/_wave11_sentence_hard.py`, recipe #174) + regen (catalog + readouts + front
   door). Report the result **honestly**, including whatever the hypotheses get wrong.

## Verifier

The gold standard is hand-verified against the sha-pinned abstracts; the LLM panel is an independent (and
different-mechanism) cross-check of the NLI verdicts; every method's false-confirm rate is the safety metric.
See `verification.md` for results + the six-standards scorecard.
