# Wave 3 — Verification receipt

3-lens, reasoning-stripped, applied to all 22 raw findings before any row was trusted or any wave-2 finding was reconciled.

## Method
1. **Retrieval oracle** (`WebFetch`, in-workflow) — existence + attribution + content-groundedness, one oracle agent per finding. The authority on existence and (sources are NVIDIA docs / GitHub issues / forum threads, not papers) the load-bearing groundedness lens.
2. **mistral-small:24b** (Mistral) — family-different groundedness, reasoning-stripped (claim + cited source only; no research-agent `detail`/`design_implication`).
3. **granite4.1:30b** (IBM Granite) — family-different groundedness, reasoning-stripped.

**ANDON note:** both ollama families were confirmed UP (`/api/version` → 0.24.0; both models present in `ollama list`) BEFORE the family pass began — the verifier-availability gate PASSED, so the wave proceeded. Had either been unreachable, doctrine is HALT-and-restore, never skip (wave-2 precedent).

## Verdict distribution
**22 raw findings checked.**
- **Retrieval oracle:** 17 `confirmed`, 5 `partial`, **0 `not_supported`, 0 `fabricated`/unreachable.** The 5 partials are scope-narrowings (a sub-claim qualified), not refutations.
- **granite4.1:30b:** **22/22 confirmed**, 0 refutations.
- **mistral-small:24b:** 14 `confirmed`, **8 `cant_confirm`**, **0 refuted.** Every `cant_confirm` fell on an absence-of-evidence claim ("no release note found …") or a 2026-dated NVIDIA-doc/GitHub-issue source that postdates the model's training — exactly the recency pattern the prompt instructed it to mark `cant_confirm` rather than false-`refute`.

## Family-different outcome
- **Union: 0 genuine refutations across all three lenses; 0 fabrications.** No finding was dropped or HALTed.
- **mistral's 8 `cant_confirm`** are priors-not-knowledge on oracle-confirmed facts (the oracle fetched the live v13.3 guide, #14078, the CUDA-13.2 blog). Filtered by the oracle — the same decorrelation wave-2 documented (mistral over-skeptic on post-training sources; the oracle reads the page).
- **granite** corroborated the concrete mechanism claims (container/memlock artifact, Windows-managed limit, VM-RAM tracking) without flagging any as unsupported.
- The instruction "mark recent sources `cant_confirm`, never `refuted`" worked: unlike the wave-2 founding receipt (where families false-flagged 2026 papers as fabricated), mistral here correctly abstained instead of refuting.

## Material actions
- **Consolidation:** 22 raw findings → **8 distinct KB findings** (the 4 lanes independently re-surfaced the same load-bearing facts — "still documented", "Windows-managed", "container artifact" each appeared 2–4×; cross-lane convergence is signal, but the KB stores distinct findings). Sources pulled verbatim from the workflow output and deduped by URL; none retyped.
- **5 `confirmed-with-fixes`** findings carry an oracle `PARTIAL` on ≥1 source (scope-narrowed sub-claim); retained with the partial recorded.
- **Reconciliation of 4 wave-2 findings** (separate UPDATE, FTS-safe — only `status`/`verify_note` touched):
  - `wsl2-collapses-…-300-mb` → **load-bearing → watch** (superseded on current rigs; held for ≤572.83 / constrained containers).
  - `wsl2-pinned-memory-cap`, `native-windows-pins-50%…` → kept, nuance note (this rig exceeded 50%; ceiling tracks VM RAM; the "lower under WSL2" is a container gate).
  - `cuda-on-wsl-guide-…-limited` → kept + **REAFFIRMED** (wording persists verbatim in v13.3; still numberless).

## Artifacts
`workflow-output.json` (raw research + oracle), `family-verdicts.json` (mistral + granite, reasoning-stripped), `_family_verify.py` (the family pass), `_build_raw.py` (consolidation → loader shape), `research-raw.json` (loaded by `scripts/load_db.py`). Run `wf_280fb07f-a91`.
