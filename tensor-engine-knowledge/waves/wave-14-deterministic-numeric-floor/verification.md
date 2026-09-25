# Wave 14 — verification (measured)

**Receipt:** `verifier/citation-panel-numeric-receipt.json` · **Harness:** `verifier/citation_panel_eval_numeric.py`
**Floor:** `verifier/numeric_floor.py`

## The deterministic floor catches both correlated failures, false-refutes nothing

On all **56** labeled cases it refuted exactly **2** — both correct:

| case | gold | rule | detail |
|---|---|---|---|
| #48 | refuted | comparison-direction | claim asserts 5 > 5.8 ("exceeded") but evidence has 5 ≤ 5.8 |
| #55 | refuted | unit-scale-mismatch | claim states 42 (10⁻³) arcsec but evidence says 10⁻⁶ arcsec |

**0 false-refutes across all 56 cases → 100% precision.** #55 is the case that fooled **all four** learned
verifiers; #48 fooled both the panel and the NLI seat.

## The full stack restores 0-false-confirm on physics

Combined gate = deterministic floor (refute) → else the learned verdict:

| learned layer | alone | + numeric floor |
|---|--:|--:|
| NLI doc-level | 2 fc {48, 55} | **0 fc** |
| NLI-veto floor | 2 fc {48, 55} | **0 fc** |
| consensus gate | 2 fc {48, 55} | **0 fc** |
| LLM panel | 3 fc {45, 48, 55} | 1 fc {45} |

The LLM panel alone keeps #45 — but the **NLI floor catches #45** (wave-13), so the complete stack
(**deterministic floor → LLM panel → NLI floor**) is **0 false-confirms on both AI/ML and physics**.

## What this validates

**Defense-in-depth with mechanistically-different layers.** The deterministic floor catches the quantitative-
comparison and unit failures that the two *learned* verifiers share and cannot catch — exactly as prism's
existence floor catches fabricated citations an LLM can't. Three layers, three mechanisms (deterministic /
decoder-LLM / encoder-NLI), each covering the others' blind spots.

## Honest residual

The comparison rule is **targeted**: it needs a shared quantity-noun to anchor on plus a discriminating
modifier adjacent to it. It **abstains** safely on claims it can't bind (0 false-refutes on the 56), so harder
comparison structures fall through to the panel + the consensus gate's human-review escalation. This is a
high-precision floor, not a complete numeric reasoner — by design (a floor must never false-refute).

## Standards compliance (`.claude/rules/workflow-standards.md`), 0–3

- **PIN_PER_STEP — 3.** Floor sha256 + per-case rule/detail + the with/without-floor physics metrics pinned.
- **EXTERNAL_VERIFIER — 3.** A *non-learned* verifier, maximally decorrelated from the LLM and NLI seats;
  validated against 56 hand-verified labels; precision is the safety metric.
- **ANDON_AUTHORITY — 3.** Refute-or-abstain: it halts a correlated false-confirm the learned layers would
  pass, and (by abstaining unless it can prove a contradiction) never halts a true claim wrongly.
- **NAMED_COMPENSATORS — N/A.** Pure-function, read-only; idempotent DB recorder.
- **DECOMPOSE_BY_SECRETS — 3.** The deterministic floor is its own module, composed under the learned
  verifiers; its quantitative logic changes independently of the prompts/models.
- **UNCERTAINTY_GATED_HUMANS — 3.** It only acts where it is *certain* (a proof) and abstains otherwise,
  routing the uncertain remainder to the panel + the consensus gate's review.

**Score: 17/18** (N/A correct). The capstone of the verifier arc: deterministic floor (existence +
numeric/unit) → 3-family LLM panel → orthogonal NLI floor, 0-false-confirm across AI/ML and physics.
