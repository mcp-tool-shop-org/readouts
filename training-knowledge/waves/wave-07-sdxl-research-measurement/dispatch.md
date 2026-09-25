# Wave 7 — SDXL research-method measurement (noise levers · checkpoint cadence · multi-concept balancing)

> Measurement dispatch · 2026-06-07 · training-knowledge KB · Batch B of the kickoff (the SDXL research half).

**Goal:** turn the remaining reproduced-from-source `diffusion-sdxl-lora` research methods into measured-on-rig receipts on
the RTX 5090 — noise-schedule levers, checkpoint-selection/save-cadence, and multi-concept repeat-balancing. Native
`networks.lora` + `sdxl_gen_img.py` + the wave-5 CLIP-sim/CMMD harness (the SDXL path is wave-4/5-proven). **Oracle = the
rig + looked-at grids + the eval harness**, not the study-swarm adversarial verifier. The **overwatch watchdog**
(`_watchdog.ps1`, aborts on RAM/VRAM/temp ceilings) guarded every run; campaign stayed clean (no trips, peak ~58 °C).

## B1 — noise-schedule levers (MEASURED, significant)

Matched baseline (AdamW fp32, cosine+warmup, 600 steps, stdstyl 16-img) vs three levers, eval n=20 (10 held-out × 2 seeds):

| config | CLIP-sim ↑ | SEM | CMMD ↓ |
|---|---|---|---|
| **noise_offset 0.1** | **0.7748** | 0.015 | 0.1373 |
| **min_snr_gamma 5** | **0.7747** | 0.018 | 0.1348 |
| baseline | 0.7257 | 0.015 | 0.1782 |
| zero_terminal_snr | 0.7176 | 0.020 | 0.1878 |

**noise_offset 0.1 and min_snr_gamma 5 each lift fidelity ~+0.049 over baseline — ≈2.3 SEM, SIGNIFICANT** (+ better CMMD).
**The headline:** noise_offset **substantially breaks the SDXL #165 blue-ceiling** — the baseline ship renders near-grayscale
(the ceiling that held across waves 4/5, which had no noise_offset), while noise_offset renders a deep Prussian-blue
cyanotype (looked-at, decisive). So the saturated cyanotype palette IS reachable on SDXL base 1.0 with noise_offset — a
cheaper path (109 MB, SDXL ecosystem) than the Chroma base-swap (wave 6). **ztsnr is neutral-to-worse** on eps-pred SDXL
(kohya warns "zero_terminal_snr enabled but v_parameterization is not"). Corrects the wave-3 "situational" framing for a
high-contrast palette. Supersedes `noise-schedule-levers-noiseoffset-ztsnr-sdxl-lora` + `min-snr-gamma-loss-weighting-sdxl`.

## B2 — checkpoint selection / save cadence (MEASURED)

One run, noise_offset 0.1, 900 steps, save every 150; eval each checkpoint (n=20):

| step | 150 | 300 | 450 | **600** | 750 | 900 |
|---|---|---|---|---|---|---|
| CLIP-sim | 0.7727 | 0.7595 | 0.7817 | **0.7865** | 0.7842 | 0.7818 |

**Best checkpoint = step 600, NOT the last (900).** Fidelity rises to a peak by ~450–600 then **plateaus / marginally
declines** (450–900 all ~0.78, within noise) → training past ~600 wastes compute on a 16-img set, and the final ≠ the best.
Style binds fast (150 already 0.77) but **undertrains visibly at 150** — the trigger leaks as literal "STDSYL" text (looked-at).
Validates save-every-N + pick-by-eval. Supersedes `checkpoint-selection-eval-grid-sdxl-lora`.

## B3 — multi-concept repeat-balancing (study-swarm grounded)

The kickoff's Q3 answer: rather than improvise a 2nd concept, a **study-swarm** (`_concept_b_studyswarm.json`,
research-grounded-advisor-protocol) grounded the design and specified **concept B = warm impasto oil painting** (trigger
`oilpst`), chosen to MAXIMIZE CLIP separation from cyanotype (warm/saturated + heavy texture + painterly, vs cool monochrome
linework) per B-LoRA (Frenkel et al. 2024) + the CLIP texture/color bias. 16 commercial-clean images generated on SDXL base
1.0 (OpenRAIL++-M inherits), looked-at + validated (consistent impasto, cleanly distinct from cyanotype). One joint LoRA per
repeat-ratio config (num_repeats = effective-exposure ratio, equal image counts), noise_offset 0.1 added so concept A's
palette renders (B1 finding — else A is #165-handicapped and the competition is unfair; fixed across configs, so it doesn't
confound the repeat lever). NO reg images (isolate the num_repeats signal, per Custom Diffusion).

| config | A:B repeats | A:B effective exposure |
|---|---|---|
| mc_balanced | 10:10 | 16:16 (1:1) |
| mc_adom | 30:10 | 48:16 (3:1, A-dominant) |
| mc_bdom | 10:30 | 16:48 (1:3, B-dominant) |

Eval: dual-trigger grids (stdstyl + oilpst over held-out subjects) → A-fidelity (cos to cyanotype centroid), B-fidelity (cos
to oilpst centroid), + cross-bleed (A-gens vs oilpst centroid, B-gens vs cyanotype centroid). Hypotheses H1–H5 from the
study-swarm. [RESULTS → verification.md, pending.]

## Citation verification (study-swarm spec)

Stage-1 retrieval oracle (WebFetch) on the high-risk citations: all real, 2 attribution fixes (`_citation_verify_stage1.md`).
Stage-2 family-different groundedness (ollama-intern) runs in a GPU-free window before the wave is finalized.

## Supersedes / new

Supersedes 3 wave-3 research techniques (noise-schedule, min-snr-gamma, checkpoint-selection) + `multi-concept-folder-repeat-balancing-sdxl`. The new concept-B dataset is a first-class `datasets` entry (Datasheets fields).
