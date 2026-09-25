# Wave 12 — verification (measured)

**Receipt:** `verifier/citation-panel-prompt-v2-receipt.json` · **Harness:** `verifier/citation_panel_eval_prompt_v2.py`
**Refined prompt:** `verifier/verify_sys_numeric.txt` (sha256 `593a06d9…`) · **Hardened:** sha256 `c7ea81d5…`

## Result — a clean win, 0 false-confirms everywhere

| Set | hardened | refined | refined + NLI floor |
|---|--:|--:|--:|
| 24-case (canonical traps) | 87.5% / 0fc | **95.8% / 0fc** | 95.8% / 0fc |
| hard-15 (numeric paraphrases) | 73.3% / 0fc | **86.7% / 0fc** | 86.7% / 0fc |
| combined-39 | 82.1% / 0fc | **92.3% / 0fc** | 92.3% / 0fc |

- **Numeric paraphrases fixed:** #25 ("fewer than two-thirds" of 23/36) and #27 ("roughly 200" of N=199)
  flipped insufficient → **supported**.
- **Bonus on the canonical set:** the contradictory-number clause fixed #8 ("over 100,000" vs 1.4K) and #20
  ("all 36" vs 23/36) — insufficient → **refuted** (the correct verdict), lifting the 24-case 87.5 → 95.8%.
- **Trap regression — all held:** #8/#20 refuted, #21/#22/#23 still caught, #39 still insufficient. **0 new
  false-confirms anywhere.**

## Honest residual

**#26** ("more than half" of 23/36) went insufficient → **refuted** — still a miss (gold = supported), but
still *safe*: it escalates, never a false-confirm. NLI doc-level gets #26 right (P(ent)=0.77), so the LLM+NLI
combination covers it upstream. The fix recovered 2 of the 3 numeric paraphrases and is a strict net win.

## Adoption + scope

Usable today via `OFFLOAD_VERIFY_SYS_FILE=verifier/verify_sys_numeric.txt` (the wave-9 override mechanism).
Promoting it to offload's inline **default** — which role-os `--local-panel` inherits — is a shared-infra
change **deferred to Mike** (the auto-mode guardrail flagged a unilateral default change to the shared
verifier, correctly). `offload.py` was **not** edited.

## Honest caveats

Small sets (24 + 15), single domain (AI/ML abstracts), one deterministic run (temperature 0). The refinement
is targeted at numeric paraphrases; it does not address non-numeric reasoning gaps.

## Standards compliance (`.claude/rules/workflow-standards.md`), 0–3

- **PIN_PER_STEP — 3.** Refined-prompt sha256 + hardened sha256 + the live refined votes + the numeric-fix and
  trap-regression case lists are all pinned in the receipt; reproducible.
- **EXTERNAL_VERIFIER — 3.** The labeled sets + the independent different-mechanism NLI seat verify the prompt
  change; the decisive metric (false-confirms) is checked on every case of both sets.
- **ANDON_AUTHORITY — 3.** The win condition halts on any new false-confirm or trap regression; a prompt that
  recovered numerics but broke a trap would be rejected (none did).
- **NAMED_COMPENSATORS — N/A.** Read-only over the DB + models; the refined prompt is loaded via an env-var
  override (no shared-tool mutation); the DB-recording step is idempotent.
- **DECOMPOSE_BY_SECRETS — 3.** The prompt lives in its own artifact (`verify_sys_numeric.txt`), swapped via
  the override, separate from offload's code and from the NLI seat.
- **UNCERTAINTY_GATED_HUMANS — 3.** The shared-default promotion (the irreversible-ish, role-os-affecting step)
  is explicitly gated to Mike; the refinement itself is a private, override-scoped artifact.

**Score: 17/18** (N/A is correct). The wave closes the wave-11 gap with a measured, regression-checked,
guardrail-respecting prompt fix.
