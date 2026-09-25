# Concept-B study-swarm — Step-4 citation verification (Stage 2: family-different groundedness)

Stage-2 = two decorrelated non-Claude families (the founding-receipt pair) via ollama-intern, reasoning-stripped, NLI-style
groundedness against the Stage-1-retrieved abstracts. Run 2026-06-07 (GPU free after the multiconcept training).
Models: **mistral-small:24b** (Mistral, run `run_2026-06-07T12-31-16_747d41`) + **granite4.1:30b** (IBM Granite,
`run_2026-06-07T12-32-33_f0cf10`).

| # | citation | mistral-24b | granite-30b | synthesis |
|---|---|---|---|---|
| 1 | B-LoRA 2403.14572 (concept-choice justification) | SUPPORTED | PARTIAL | **SUPPORTED** — block-separation holds; the specific blocks 4/5 live in the paper body, not the abstract |
| 2 | CLIP texture/color bias 2508.09814 | **REFUTED** | **CANNOT_CONFIRM** | **NOT GROUNDED** — paper is about texture-shape bias *dynamics over training*, NOT "CLIP is color+texture-driven at high resolution." **Dropped** as a load-bearing citation. |
| 3 | Custom Diffusion 2212.04488 (distinct tokens) | CANNOT_CONFIRM | PARTIAL | real (Stage-1); claim is textbook, abstract not in-context |
| 4 | kohya num_repeats (effective exposure) | SUPPORTED | SUPPORTED | **SUPPORTED** |
| 5 | CMMD 2401.09603 | PARTIAL | PARTIAL | **PARTIAL** — core small-n claim ok; the "n=15 thin" caveat is ours, not the paper's |
| 6 | Carlini 2301.13188 (diversity vs memorization) | CANNOT_CONFIRM | SUPPORTED | real; well-known |
| 7 | StyleDrop 2306.00983 | PARTIAL | PARTIAL | **PARTIAL** — "<1% params, few images" supported; "16 is ample" is our extrapolation |
| 8 | SDXL OpenRAIL++-M license | SUPPORTED | SUPPORTED | **SUPPORTED** |

## Outcome (ANDON applied)
- **#2 (2508.09814) is REFUTED/not-grounded by the panel → removed from the load-bearing citation set.** The concept-B =
  warm-impasto-oil choice does NOT hinge on it: it rests on **#1 B-LoRA (SUPPORTED)** + the **empirical** separation actually
  measured (the two concepts ARE cleanly separated — looked-at + CLIP own-vs-cross centroid gap). The wave stands.
- The load-bearing design citations — **#4 num_repeats (the lever), #8 license (commercial-clean), #1 B-LoRA (separation)** —
  are SUPPORTED by the panel.
- #5/#7 downgraded to PARTIAL (claim slightly broader than the source) — kept with corrected, narrower phrasing.
- #3/#6 CANNOT_CONFIRM are abstract-availability artifacts (Stage-1 retrieval already confirmed existence + topic); textbook
  claims, low risk.

The protocol's value showed: a real source-mischaracterization (#2) survived Stage-1 (the paper exists + is on the topic of
CLIP texture bias) but was caught by the different-family groundedness lens in Stage-2 — exactly the failure mode the
two-stage gate exists for. **Note:** wave-07's MEASURED findings (noise levers, checkpoint, repeat-balancing) are rig-measured;
their oracle is the rig + eyes + harness, NOT these citations — the citations only ground the concept-B *design*.
