# Wave 13 — verification (measured)

**Receipt:** `verifier/citation-panel-multidomain-receipt.json` · **Harness:** `verifier/citation_panel_eval_multidomain.py`
**Data:** `verifier/citations-multidomain.json` (17 physics cases) · 5 sha-pinned abstracts (LIGO/ATLAS/CMS/Planck/EHT)

**The generality test broke the verifier — the first false-confirms in the whole arc.** Both hypotheses were
partly wrong, and that is the value.

## Results — multi-domain (17 physics cases)

| Method | acc | false-confirms | over-escalation |
|---|--:|--:|---|
| NLI doc-level | 76.5% | **{48, 55}** | {41} |
| LLM panel (refined default, live) | 82.4% | **{45, 48, 55}** | — |
| floor (NLI veto) | 82.4% | {48, 55} | {41} |
| consensus gate | 76.5% | {48, 55} | {41} |

vs **100% / 0 fc** for NLI doc-level on the AI/ML sets. **H1 (the seat generalizes) → false.**

## What broke, and why it matters

- **#48** (CMS, "observed 5.0σ *exceeded* expected 5.8σ" — gold refuted): the NLI seat said **supported**
  (P=0.99) and the panel slipped too. Subtle quantitative **comparison** missed by both.
- **#55** (EHT, "42 **milli**arcseconds" vs the abstract's "42 **micro**-as" — gold refuted): **all three LLM
  seats + the NLI seat** said supported. A **unit** error fooled everything.
- **#45** (ATLAS, "5.0σ" vs the stated 5.9σ — gold refuted): the NLI floor **caught** the panel's false-
  confirm (NLI refuted P=0.99). The orthogonal seat earning its keep — an *uncorrelated* error.
- **#41** (36+29 = "~65 M☉" — gold supported): the LLM panel did the arithmetic; the NLI **wrong-refuted** it.
  Each mechanism covers *some* of the other's blind spots.

**The correlated-failure ceiling re-emerges across mechanisms.** #48 and #55 are **correlated false-confirms**
— shared by a decoder LLM *and* an encoder NLI. Mechanistic orthogonality *reduces* correlated error (it fixed
the AI/ML #21/#22/#23) but does not *eliminate* it: quantitative-comparison and unit failure modes are common
to both learned verifiers.

## The consensus gate (the #26 residual)

On the 39 AI/ML cases the consensus gate **fixes #26**: panel=refuted + NLI=supported → consensus=`insufficient`
(escalate for review) instead of confidently auto-refuting a true claim, with **0 false-confirms preserved**.
It also escalates uncorrelated disagreements (#41/#45 on physics). But it **inherits** the correlated blind
spot (#48/#55, both-supported → consensus supported) — no two-verifier combination catches a case both fail.

## Honest takeaway (KB integrity)

The verifier's **0-false-confirm property is domain-dependent** — validated for AI/ML citation traps, but
numeric-comparison ("exceeded") and unit (milli/micro) claims on physics abstracts break it across **both**
learned verifiers. The durable fix is a mechanistically-**third**, **deterministic** verifier: a numeric/unit
extractor-comparator (parse quantities + units from claim vs evidence, compare arithmetically) — the quantity
analog of prism's existence floor, which neither an LLM nor an NLI provides. **→ wave-14 candidate.**

## Honest caveats

17 cases, one new domain (physical sciences). The seat may do better/worse on biomedical/economics/etc. The
finding is a *floor* on the verifier's limits (it breaks *at least* here), not a full characterization.

## Standards compliance (`.claude/rules/workflow-standards.md`), 0–3

- **PIN_PER_STEP — 3.** Multi-domain sha256 + per-abstract sha256 + NLI scores + live LLM votes pinned.
- **EXTERNAL_VERIFIER — 3.** Two different-mechanism verifiers cross-checked against hand-verified gold; the
  wave's whole point was to find where the verifier itself fails — and it did, on the record.
- **ANDON_AUTHORITY — 3.** The false-confirms are reported, not buried; the 0-fc claim is explicitly re-scoped
  to AI/ML, halting any overclaim of universal safety.
- **NAMED_COMPENSATORS — N/A.** Read-only (one network fetch to a separate cache; idempotent DB recorder).
- **DECOMPOSE_BY_SECRETS — 3.** New-domain data, the NLI seat, the LLM panel, and the consensus combiner are
  separate; the harness composes them.
- **UNCERTAINTY_GATED_HUMANS — 3.** The consensus gate operationalizes this exactly — inter-verifier
  disagreement (a real uncertainty signal) routes to human review rather than an auto-decision.

**Score: 17/18** (N/A correct). The most valuable wave of the arc: it found the verifier's real limits and
named the precise fix.
