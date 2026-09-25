# Wave 10 — Mechanistically-orthogonal NLI verifier seat

**Date:** 2026-06-03 · **Mode:** hands-on + measured on the live RTX 5090 (no research swarm) · **Recipe:** #173

## The problem (carried from wave-9 #171)

Wave-9 stood up a 3-family LLM citation panel (qwen3-14b + mistral-nemo-12b + IBM granite-3.3-8b) and
discovered a ceiling: on a 24-case adversarial set the panel **false-confirmed #21/#22/#23**, and #22 (a
stricter/looser inversion of arXiv:2408.02442) **fooled all three families**. The seats are family-different
but **same-mechanism** — all decoder-only instruct LLMs doing generative grounded-entailment — so they share
a **correlated** credulity blind spot. Conservative majority and a 3rd family fix *uncorrelated* error only;
they cannot catch a correlated slip. The hardened prompt (#171) recovered the three, but a prompt is a patch
on the *same* mechanism; wave-9 named the durable fix as its NEXT: **a mechanistically-orthogonal verifier +
calibrated abstention.**

## Hypothesis

An **encoder NLI cross-encoder** fails *differently* from a decoder-only LLM: bidirectional encoder,
discriminative 3-way classifier (entailment / neutral / contradiction), trained on NLI/fact-verification
data, **no chain-of-thought, no prompt**. Its errors should decorrelate from the LLM bloc, so adding it as a
member breaks the correlated ceiling. The trap types map onto its native classes: inversions → contradiction
→ `refuted`; plausible-but-unstated → neutral → `insufficient`.

## Literature grounding

- **Kuncheva & Whitaker 2003** — *Measures of Diversity in Classifier Ensembles…*, Machine Learning 51:181.
  Majority-vote accuracy is bounded by member **correlation**, not member count → the fix must lower
  correlation, i.e. change the *mechanism*, not add another same-mechanism seat.
- **Kim et al. 2025** (arXiv:2506.07962) and **Verga et al. 2024 PoLL** (arXiv:2404.18796), per wave-9's
  grounding — capability convergence drives correlated error; diverse LLM panels fix idiosyncratic bias, not
  shared reasoning error. **Li et al. 2022** (arXiv:2210.04695) — LMs are poor at *directional* inference
  (exactly the #22 failure).
- **He et al. 2021 DeBERTaV3** (arXiv:2111.09543) — the encoder backbone. **Thorne et al. 2018 FEVER**
  (arXiv:1803.05355) + **Nie et al. 2020 ANLI** (arXiv:1910.14599) — the fact-verification / adversarial-NLI
  training mix; FEVER is claim-vs-evidence, the exact shape of a citation check.
- **Geifman & El-Yaniv 2017** (arXiv:1705.08500) — selective classification / abstention: a calibrated
  confidence threshold lets the model decline rather than guess, which we make **asymmetric** (gate only the
  `supported` decision; over-escalation is the safe failure).

## Plan

1. Pick a **commercial-safe** NLI cross-encoder (commercial-license-first): `MoritzLaurer/DeBERTa-v3-large-
   mnli-fever-anli-ling-wanli` — DeBERTa-v3-large base (**MIT**), ~435M, MNLI+FEVER+ANLI+LingNLI+WANLI.
2. Stand it up on the rig (unsloth-env: torch 2.12 cu130 sm_120). Map NLI → verdict; add asymmetric
   calibrated abstention (`TAU_SUPPORT`, default 0.55). → `verifier/nli_verify.py`.
3. **Measure** on the 24-case set + the original-16 subset + the 8 traps: does the orthogonal seat catch the
   correlated false-confirms? Reuse the wave-9 sha-pinned LLM panel votes (legacy + hardened) and measure the
   **combined LLM-panel + NLI floor** (veto on `supported`, downgrade-only → cannot add a false-confirm).
   Compare against a 4th-seat majority. Sweep `TAU`. → `verifier/citation_panel_eval_nli.py`.
4. **Wire it in** without touching frozen tools: `studio-local/nli_floor.py` composes `offload`'s LLM panel +
   the NLI floor (the wave-6 #164 companion pattern). role-os's citation gate can call it.
5. **Record** as wave 10 (`scripts/_wave10_nli_verifier.py`: wave row + recipe #173; mark #171's NEXT done)
   and `regen.py` (rebuilds catalog + readouts + the monorepo front door from the DB).

## Verifier (EXTERNAL_VERIFIER)

The generator is Claude; the result is checked by signals independent of the generator: (a) the NLI seat is a
**different family AND a different mechanism**, reasoning-stripped; (b) the labeled 24-case set with a fixed
gold standard and sha-pinned abstracts; (c) the measured property is reproducible from the DB-pinned receipt.
See `verification.md` for results + the six-standards scorecard.
