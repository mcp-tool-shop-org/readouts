# Wave 7 — Verification receipt (SDXL research-method measurement)

> Oracle = the rig + looked-at grids + the CLIP-sim/CMMD harness — NOT the study-swarm adversarial verifier. The **overwatch
> watchdog** (`_watchdog.ps1`, auto-abort on RAM/VRAM/temp ceilings) guarded every run; zero trips, peak ~58 °C all of Batch B.

## B1 — noise levers (n=20, cyanotype centroid)

| config | CLIP-sim ↑ | SEM | CMMD ↓ |
|---|---|---|---|
| noise_offset 0.1 | 0.7748 | 0.015 | 0.1373 |
| min_snr_gamma 5 | 0.7747 | 0.018 | 0.1348 |
| baseline | 0.7257 | 0.015 | 0.1782 |
| zero_terminal_snr | 0.7176 | 0.020 | 0.1878 |

noise_offset + min_snr each **~2.3 SEM over baseline** (significant). **Looked-at:** baseline ship near-**grayscale** (the #165
blue-ceiling), noise_offset ship deep **Prussian-blue** cyanotype — noise_offset breaks the ceiling. ztsnr neutral-worse
(eps-pred SDXL, kohya warns no v_parameterization).

## B2 — checkpoint curve (n=20 per checkpoint, noise_offset 0.1, 900 steps)

| step | 150 | 300 | 450 | **600** | 750 | 900 |
|---|---|---|---|---|---|---|
| CLIP-sim | 0.7727 | 0.7595 | 0.7817 | **0.7865** | 0.7842 | 0.7818 |

**Best = step 600, not the last (900).** Plateau 450–900 (within noise). **Looked-at:** step 150 shows a literal "STDSYL"
trigger-text artifact (undertraining); step 600 clean; step 900 ≈ 600 (no gain).

## B3 — multi-concept repeat-balancing (dual-trigger n=20 each + cross-bleed)

| config | A_fid (cyanotype) ↑ | B_fid (oilpst) ↑ | A→B bleed | B→A bleed |
|---|---|---|---|---|
| balanced 10:10 (1:1) | 0.7738 | 0.7710 | 0.6489 | 0.6984 |
| A-dom 30:10 (3:1) | 0.7793 | 0.7787 | 0.6541 | 0.7000 |
| B-dom 10:30 (1:3) | 0.7937 | 0.7843 | 0.6783 | 0.6751 |

**Both concepts keep high own-fidelity across all ratios (spreads ~1 SEM) — no collapse at 3:1.** Dominance shows as
**cross-bleed**: B-dominant → highest A→B bleed (0.678, cyanotype tinted painterly) + lowest B→A bleed (0.675, oilpst purest);
A-dominant the reverse. Own (0.77–0.79) >> cross (0.65–0.70) → concepts genuinely separated. **Looked-at confirms:** the
dominated concept keeps identity but takes a subtle tint of the dominant style (B-dom cyanotype ship softer/painterly;
A-dom oilpst ship cooler/muted). H3 + H4 supported; the naive H1 trade-off weaker than predicted — distinct triggers +
adequate capacity + 1600 steps co-train robustly through moderate imbalance.

## Concept B (study-swarm grounded + empirically validated)

Warm impasto-oil (`oilpst`), 16 synthetic SDXL-base images (OpenRAIL++-M, commercial-clean), chosen to maximize CLIP
separation from cyanotype. **Looked-at + validated** before training: consistent impasto, cleanly distinct from cyanotype.
First-class `datasets` entry (`oilpst-impasto-oil-concept-b`, Datasheets fields).

## Citation verification (study-swarm spec; `_citation_verify_stage1.md` + `_citation_verify_stage2.md`)

- **Stage-1 (retrieval oracle, WebFetch):** high-risk citations all real; 2 attribution fixes (SCAdapter authors; the
  texture-bias paper's first author is Hernández-Cámara, not "Jiang").
- **Stage-2 (family-different groundedness, mistral-small:24b + granite4.1:30b):** the load-bearing design citations —
  B-LoRA (separation), kohya num_repeats (the lever), SDXL license (commercial-clean) — **SUPPORTED**. The panel **REFUTED /
  could-not-confirm finding #2 (CLIP texture/color bias, 2508.09814)** — the paper is about texture-shape bias *dynamics*,
  not "color+texture-driven at high resolution" — so it was **dropped** as a load-bearing citation (the concept-B choice rests
  on B-LoRA + the empirical separation, not on #2). The two-stage gate caught a real source-mischaracterization that survived
  Stage-1. **The wave's measured findings do not depend on any citation** (oracle = rig + eyes + harness).

## Not in scope (recorded)

Lower-priority research-by-nature lanes were skipped per the kickoff (peft-methods theory, dataset-caption craft, debugging
failure-modes — hard to measure cleanly). All *tractable* `diffusion-sdxl-lora` research methods are now measured.

## Provenance

7 SDXL rig runs (4 B1 + 1 B2 + 3 B3 multiconcept... = 8 runs incl. concept-B generation) + 6 eval-grid passes on the RTX 5090,
2026-06-07. Every measured technique: `evidence_strength=measured-on-rig` + `engine_recipe_ref=training-kohya-sdxl-lora-proven-blackwell-5090`
+ the receipt + looked-at grids (`eval_grid_sdxlnoise/`, `eval_grid_ckpt/`, `eval_grid_mc/`). Eval JSON `_eval_sdxl_noise.json`,
`_eval_ckpt.json`, `_eval_multiconcept.json`. 4 wave-3 research techniques superseded.
