# Wave 14 — deterministic numeric/unit floor (the capstone)

**Date:** 2026-06-03 · **Mode:** hands-on + measured (stdlib, no GPU) · **Recipe:** #177

## The fix wave 13 named

Wave-13's generality test found 2 **correlated** false-confirms on physics abstracts that fooled **both**
learned verifiers (the LLM panel and the orthogonal NLI seat): #48 (a numeric comparison — "observed 5.0σ
*exceeded* expected 5.8σ", false since 5.0 < 5.8) and #55 (a unit error — "42 **milli**arcseconds" vs the
abstract's "42 **micro**-as"). Both learned mechanisms judge surface plausibility, so both miss these. The
named fix: a mechanistically-**third**, **deterministic** verifier — the quantity analog of prism's existence
floor (which deterministically refutes fabricated citations an LLM can't).

## Design — a refute-or-abstain floor

`numeric_floor.py` returns `refuted` **only** when it can *prove* a quantitative contradiction; otherwise it
abstains (falls through to the learned verifiers). It never confirms, and only refutes on a proof — so it
**cannot add a false-confirm**, and a wrong rule would only ever *escalate* a true claim (safe). Two rules:

1. **Unit-scale mismatch** — the claim states the same number as the evidence but a different metric prefix
   on the same base unit (42 milli-arcsec vs 42 micro-arcsec). (Catches #55.)
2. **Comparison-direction falsehood** — the claim asserts A > B / A < B where A and B each bind, via a
   discriminating modifier sitting *adjacent to a shared quantity-noun* (which disambiguates "expected
   background" from "expected significance"), to a distinct explicit number in the evidence, and the asserted
   relation is arithmetically false. (Catches #48.)

## Plan

1. Build `numeric_floor.py` (metric-prefix + arcsecond unit normalization; phrase-anchored numeric binding).
2. Measure on **all 56 labeled cases** (`citation_panel_eval_numeric.py`): it MUST catch #48/#55 and
   **false-refute nothing** (high precision is the whole point of a floor).
3. Measure the **combined gate** on physics (deterministic floor → else the learned verdict): does it restore
   0-false-confirm for the NLI floor / consensus layers?
4. Record as wave 14 (`scripts/_wave14_numeric.py`, recipe #177) + regen.

## Verifier

The 56 hand-verified labeled cases are the test: the floor's precision (every `refuted` must be gold=refuted)
is the safety property, and the with/without-floor false-confirm counts on physics are the efficacy measure.
See `verification.md`.
