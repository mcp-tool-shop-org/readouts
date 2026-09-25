# Wave 10 — verification (measured)

**Receipt:** `verifier/citation-panel-nli-receipt.json` · **Harness:** `verifier/citation_panel_eval_nli.py`
**Seat:** `verifier/nli_verify.py` · **Companion:** `studio-local/nli_floor.py`

## The orthogonal seat

`MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` — DeBERTa-v3-large base (**MIT**), 435M params,
loaded on CUDA (sm_120 fine). `id2label` confirmed at load `{0:entailment, 1:neutral, 2:contradiction}`
(read from the model, not hard-coded). Mapping: entailment→`supported`, contradiction→`refuted`,
neutral→`insufficient`. Asymmetric abstention: `supported` only if argmax==entailment **and**
P(ent) ≥ `TAU_SUPPORT` (0.55); `refuted`/`insufficient` are not thresholded.

## Results (24-case adversarial set; LLM votes reused sha-pinned from `prompt-hardening-receipt.json`)

**NLI seat SOLO:** **100% (24/24), 0 false-confirms**, **8/8 traps**.
Catches all three correlated false-confirms the LLM panel slipped:

| Case | Trap | gold | legacy LLM panel | NLI seat | caught |
|---|---|---|---|---|---|
| #21 | unstated entity ("Claude" not in abstract) | insufficient | **supported (slip)** | insufficient (P(neu)=0.95) | ✅ |
| #22 | inversion (stricter↔looser) — fooled all 3 families | refuted | **supported (slip)** | refuted (P(con)=0.999) | ✅ |
| #23 | unstated ranking | insufficient | **supported (slip)** | insufficient | ✅ |

**Combined LLM panel + NLI FLOOR** (NLI vetoes `supported` only — downgrade-only, so it *cannot* add a
false-confirm):

| LLM prompt | panel alone | + NLI floor |
|---|---|---|
| legacy (default-at-wave-9) | 79.2% · **3 fc** {21,22,23} | 91.7% · **0 fc** · 0 over-escalation |
| hardened (current default) | 87.5% · 0 fc | 87.5% · **0 fc** · 0 over-escalation |

→ Orthogonality breaks the ceiling **without** the prompt patch, and **composes** with it (no regression).

**Floor beats 4th-seat majority:** a 4-seat majority (3 LLM + NLI) still false-confirms **#22** — the
correlated LLM bloc out-votes the orthogonal seat 3–1. The asymmetric **veto** is the correct integration,
not naive voting.

**TAU sweep:** 0 false-confirms across 0.50–0.90 on this set (robust; 0.55 default is safe, 0 over-escalation).

**Live e2e** (`nli_floor.py --demo`, llama-swap UP): with the hardened default, the LLM panel **and** the NLI
seat both `refuted` #22 — belt-and-suspenders; the floor is the independent backstop.

## Honest caveats

- **n = 24 is small**, and the traps are **NLI-canonical** (inversions→contradiction, unstated→neutral) —
  the model's home turf. 100% here is *not* a general accuracy claim.
- **Durable value = the combination, not NLI-alone.** The LLM panel handles reasoning the NLI lacks
  (multi-hop, numeric, world knowledge); the NLI floor vetoes the LLM's credulity slips. Because the floor is
  **monotone-safe** (downgrade-only), NLI errors on other distributions degrade to over-escalation (safe),
  never a false-confirm.
- **Document-level NLI** (claim vs whole title+abstract). Sentence-level FEVER-style evidence selection is the
  next refinement.

## Standards compliance (`.claude/rules/workflow-standards.md`), 0–3

- **PIN_PER_STEP — 3.** Model + license + `TAU` + mapping + the reused LLM-vote receipt sha256 + per-source
  abstract sha256 are all pinned in the receipt; the property reproduces from the DB-pinned artifacts.
- **EXTERNAL_VERIFIER — 3.** The whole wave *is* this standard, taken to its strongest form: a verifier of a
  **different family AND a different mechanism** (encoder NLI vs decoder LLM), reasoning-stripped, judged on a
  fixed labeled set against sha-pinned evidence. Measured, not asserted.
- **ANDON_AUTHORITY — 3.** The floor halts a `supported` the moment the orthogonal seat disagrees; a bad
  (false-confirming) verdict cannot propagate downstream — and the floor can only *downgrade*, so it never
  introduces one.
- **NAMED_COMPENSATORS — N/A.** Read-only over the DB + models; no irreversible/outward-facing calls.
  (The DB-recording step's undo: re-run the idempotent `_wave10_nli_verifier.py`, or `git checkout`.)
- **DECOMPOSE_BY_SECRETS — 3.** The seat (`nli_verify.py`, torch/transformers) is separate from the stdlib
  `offload.py`; the companion (`nli_floor.py`) composes them without editing either. Each part changes for its
  own reason.
- **UNCERTAINTY_GATED_HUMANS — 3.** Calibrated *asymmetric* abstention: the seat escalates (declines to
  confirm) under uncertainty rather than guessing, and the gate's only hard rule is "never wave through an
  unsupported claim." Frames the trade contrastively (over-escalation is the safe failure).

**Score: 17/18** (the one N/A is correct — nothing irreversible here). Up from wave-9's 16/18: the
mechanistically-orthogonal seat is the durable complement to wave-9's prompt patch.
