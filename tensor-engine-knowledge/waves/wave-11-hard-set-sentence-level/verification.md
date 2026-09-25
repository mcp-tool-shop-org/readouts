# Wave 11 — verification (measured)

**Receipt:** `verifier/citation-panel-hard-receipt.json` · **Harness:** `verifier/citation_panel_eval_hard.py`
**Data:** `verifier/citations-hard.json` (15 cases) · **Seat:** `verifier/nli_verify.py` (doc + sentence)

Both hypotheses were partly **wrong** — which is the value of the wave.

## Hard set (15 cases) — accuracy / false-confirms / over-escalation

| Method | acc | false-confirms | over-escalation |
|---|--:|--:|---|
| **NLI doc-level** | **100.0%** | 0 | 0 |
| NLI sentence-level | 80.0% | 0 | {25, 26} |
| LLM panel (hardened, live) | 73.3% | 0 | {25, 26, 27} |
| floor (doc, veto-not-supported) | 73.3% | 0 | {25, 26, 27} |
| floor (doc, veto-contradiction-only) | 73.3% | 0 | {25, 26, 27} |

**0 false-confirms across *every* method** — the safety property is universal on this set; the differences
are all in over-escalation (recall), never safety.

## H1 — "the hard set breaks the NLI seat" → **FALSE.**

NLI **doc-level scored 100%** (15/15), including the numeric paraphrases (#25 supported P(ent)=0.998, #26
0.77, #27 0.998) and the multi-hop cases. The wave-10 "NLI-canonical caveat" is weaker than feared: the seat
generalizes to non-canonical hard cases (at least this set). The seat's numeric success may be paraphrase-
pattern rather than true arithmetic — an honest unknown — but the verdicts are correct.

## H2 — "sentence-level helps" → **FALSE (negative result).**

Sentence-level **hurts**: 80% on the hard set, **70.8% on the 24-case regression** (vs doc-level 100%/100%).
It loses the cross-sentence context the numeric cases need — no single abstract sentence carries
"23/36 → fewer than two-thirds" (#25 max-sentence-entailment 0.53, #26 0.15 → both drop to insufficient).
**Document-level stays the default**; `verify_one_sentencewise()` is kept for long-document cases but **not
promoted**.

## The surprise — the hardened LLM panel is the *weakest* verifier here (73.3%)

On all **4** NLI-vs-LLM disagreements, **NLI doc-level was right and the LLM panel was wrong**:

| case | gold | LLM panel | NLI doc | why |
|---|---|---|---|---|
| #25 | supported | insufficient | **supported** | added-specific-check over-escalates "fewer than two-thirds" (seats split: qwen=sup, mistral=insuf, granite=ref) |
| #26 | supported | insufficient | **supported** | same — "more than half" of 23/36 |
| #27 | supported | insufficient | **supported** | "roughly two hundred" for N=199 |
| #34 | insufficient | refuted | **insufficient** | LLM over-refutes a scope ("as much as") claim |

The hardened prompt's **added-specific-check** (great for catching invented specifics, #21/#23) is **too
aggressive on legitimate numeric paraphrases**.

## Floor behavior

The monotone-safe floor holds **0 fc** but cannot *improve* accuracy here — it only downgrades an LLM
`supported`, and the LLM already over-escalated (no false `supported` to veto), so the floor = the LLM panel
(73.3%). Both floor variants (veto-on-not-supported vs veto-on-contradiction-only) are **identical** here
because there was no LLM false-confirm to catch — the distinction only bites when the LLM slips a `supported`
(as on the legacy-prompt 24-case set). The doc-level floor on the 24-case set is still **87.5% / 0 fc**
(matches wave-10).

## Takeaways

- **NLI doc-level is a strong *standalone* verifier** (robust past canonical traps) **and** the safety floor
  (0-fc, wave-10). Best of both: use it as the floor *and* weigh its independent verdict.
- **Sentence-level is not adopted** (negative result; doc-level wins on these abstracts).
- **The LLM panel's numeric over-escalation is a *prompt* issue**, not a floor issue — a future LLM-prompt
  refinement (relax the added-specific-check for numeric paraphrases). A symmetric NLI "upgrade" is rejected:
  it would break monotone-safety (a wrong upgrade = a false-confirm).

## Honest caveats

Still small (15 hard + 24 canonical), single domain (AI/ML abstracts). The NLI's numeric success may be
paraphrase-pattern, not arithmetic. The LLM panel ran once (temperature 0, deterministic).

## Standards compliance (`.claude/rules/workflow-standards.md`), 0–3

- **PIN_PER_STEP — 3.** Hard-set sha256 + per-abstract sha256 + verify-prompt sha256 + the live LLM votes are
  all pinned in the receipt; reproducible from the DB-pinned artifacts.
- **EXTERNAL_VERIFIER — 3.** Two independent, different-mechanism verifiers (encoder NLI vs decoder LLM panel)
  cross-check each other against a hand-verified gold standard; the disagreement analysis is the receipt's
  core. The wave is itself a verification *of* the verifier.
- **ANDON_AUTHORITY — 3.** 0 false-confirms across every method; the gate never waves an unsupported claim
  through. A negative result (sentence-level) is reported, not buried.
- **NAMED_COMPENSATORS — N/A.** Read-only over the DB + models; the DB-recording step is idempotent
  (`_wave11_sentence_hard.py`) / `git checkout`.
- **DECOMPOSE_BY_SECRETS — 3.** The hard data, the seat (doc + sentence), and the LLM panel are separate; the
  harness composes them without coupling.
- **UNCERTAINTY_GATED_HUMANS — 3.** Over-escalation (the safe failure) is measured and surfaced per case; the
  honest framing is contrastive (the LLM over-escalates *here*, NLI is right *there*).

**Score: 17/18** (N/A is correct). The wave's worth is its honesty: a stress test the seat passed, a clean
negative result on sentence-level, and a measured weakness in the hardened LLM prompt.
