# Wave 12 — numeric-paraphrase prompt fix (a QUANTITY EXCEPTION)

**Date:** 2026-06-03 · **Mode:** hands-on + measured on the live RTX 5090 / llama-swap :9090 · **Recipe:** #175

## The lever (from wave 11)

Wave-11 found the hardened verify prompt's **added-specific-check** is too aggressive on numeric paraphrases:
it treats any number not *literally* in the evidence as an "added specific" → `insufficient`. So it stamped
"fewer than two-thirds" (of 23/36), "more than half", and "roughly 200" (of N=199) as insufficient, where the
NLI doc-level seat correctly said `supported`. On all four wave-11 NLI-vs-LLM disagreements, NLI was right —
and the gap was a **prompt** issue, not a floor issue.

## The fix

A surgical **QUANTITY EXCEPTION** added to rule 2 (`verifier/verify_sys_numeric.txt`): a number that is a
faithful restatement, rounding, or one-step arithmetic consequence of a quantity *explicitly in the evidence*
is **not** "added" — evaluate it under the contradiction/support rules instead. Guardrails kept intact:
- a number that **contradicts** the evidence's quantity ("all 36" when it says 23/36; "over 100,000" when it
  says 1.4K) → `refuted`;
- a number with **no quantity in the evidence to derive from** ("70% accuracy" the abstract never reports) →
  `insufficient`.

## Plan

1. Author the refined prompt; load it via the existing `OFFLOAD_VERIFY_SYS_FILE` override (no edit to the
   shared `offload.py` — its default stays the hardened prompt until promotion is approved).
2. Run the LLM panel **live** on all 39 cases (24 canonical + 15 hard) under the refined prompt; compare to
   the pinned hardened + NLI-doc verdicts.
3. **Win condition:** fix the numeric paraphrases (#25/#26/#27) **and** introduce **0 new false-confirms**,
   **0 trap regressions** (#8/#20 refuted, #21/#22/#23 caught, #39 insufficient).
4. Record as wave 12 (`scripts/_wave12_numeric_prompt.py`, recipe #175) + regen.

## Verifier (EXTERNAL_VERIFIER)

The labeled 24+15 sets (hand-verified gold, sha-pinned abstracts) **and** the independent, different-mechanism
NLI doc seat cross-check the refined panel. The decisive metric is false-confirms (must stay 0); accuracy +
over-escalation are reported per set. A prompt that recovered the numerics but reintroduced any trap false-
confirm would be rejected. See `verification.md`.

## Scope note

Promoting the refined prompt to offload's inline **default** (which role-os `--local-panel` inherits) is a
shared-infrastructure change and is **deferred to Mike** — the auto-mode guardrail flagged a unilateral
default change to the shared verifier, correctly. The refinement is fully usable now via the override.
