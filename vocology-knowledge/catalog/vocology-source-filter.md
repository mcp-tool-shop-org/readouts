# Vocology / source-filter floor
_Source–filter theory, singer formant, registers, vibrato, breathiness cues_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

39 findings · 20 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| A four-parameter model of glottal flow | Fant, Liljencrants & Lin · 1985 | The LF source is the derivative of glottal flow (Ee closing discontinuity + Ta return phase), not a harmonic oscillator. | ✓ |
| ACE-Step 1.5 Inference API | ACE-Step · 2026 | GenerationParams metadata is caption/lyrics + bpm / keyscale / timesignature / duration — no note MIDI, no register, no formant; song-generator surface opposite the SVS craft axis. | ✓ |
| Acoustic Theory of Speech Production | Fant · 1971 | The radiated voice is source × tract filter; independence is only a first approximation. | ✓ |
| Bi-stable vocal fold adduction | Titze · 2014 | Registers are glottal adduction shapes rather than F0 labels, for modal vs falsetto and mixed registration; the paper explicitly excludes fry/pulse register, calling it not mechanistically or spectrally unique. | ✓ |
| Cantor Digitalis (Web Audio) README | edwardbrowncross · 2026 | Perceptual API exposes isFalsetto (M1/M2), tenseness, breathiness, vocalTractSize, and synth-level F1–F6 formant centers — register is an explicit boolean, not an F0 label. | ✓ |
| Cantor Digitalis tech notes | Feugère / d’Alessandro / Doval / Perrotin (port) · 2017 | Docs state the singing formant is produced by grouping F3–F5, with hypo-pharynx anti-resonance ~2.5–3.5 kHz — formant cluster is a tract setting, not painted EQ. | ✓ |
| Chest/mix/head classification from mel texture around passaggio | Kim & Botha · 2025 | Classifies chest/mix/head-mix/head from mel-spectrogram texture around male passaggio; mixed voice is TA–CT balance, not a single F0 label. | ✓ |
| Controllable Singing Voice Synthesis using Phoneme-Level Energy Sequence | Ryu, Shin & Kim · 2025 | Phoneme-level energy/dynamics control without register or singer-formant dimensions. | ✓ |
| DiffSinger Best Practices | openvpi · 2026 | Acoustic inputs are fixed to phoneme seq + phoneme duration + F0; narrow variance knobs are energy, breathiness, voicing, tension — no named register or singer-formant control. | ✓ |
| Flexible Singing Voice Synthesis Through Decomposed Framework with Inferrable Features | Violeta & Akama · 2024 | Decomposed score-to-waveform feature streams; flexibility ≠ pedagogy register enums. | ✓ |
| LAPS-Diff: Diffusion-Based SVS With Language Aware Prosody-Style Guided Learning | Dhar, Gupta & Rao · 2025 | Prosody/style guidance ≠ mixed-voice/passaggio registration or singer-formant tract settings. | ✓ |
| Machine Learning Approaches to Vocal Register Classification in Contemporary Male Pop Music | Kim, Botha · 2025 | Full text (v2): 1008 three-second lead-vocal clips, stem-split from pop songs in Logic Pro, were rendered to mel-spectrograms producing 7221 initial images before splitting and augmentation — v1 states 4221 images for the same clip count. Four classes are indexed 0 chest / 1 mix / 2 head mix / 3 head. Augmentation was a horizontal flip plus two brightness variants; the split was 80/20. The SVM reached 0.94 overall accuracy on the test set with per-class metrics spanning 0.91–0.99; the CNN trained for six epochs (68.0% validation accuracy after epoch one). Register labels were assigned by ear from vocal-technique texts (Peckham 2010), not by EGG or laryngoscopy. The authors ship a tool, AVRA (Automatic Vocal Register Analysis). CC BY 4.0. | ✓ |
| Machine Learning with Evolutionary Parameter Tuning for Singing Registers Classification | Boratto, Costa, Meireles, Alves, Saporetti, Bodini, Cury, Goliatt · 2025 | On a purpose-built dataset of 350 audio files spanning chest, mixed and head registers, 14 temporal features extracted with the TSFEL Python library fed three ML models whose hyperparameters were tuned by a Differential Evolution algorithm; the DE-optimised Extreme Gradient Boosting model reached an average classification accuracy of 97.60%. Signals 6(1) article 9, published 21 February 2025, open access under CC BY 4.0. | ✓ |
| Modeling source-filter interaction in belting and high-pitched operatic male singing | Titze & Worley · 2009 | Source–filter interaction in belt vs classical; 2F0/F1–F2 inertance and register flip risk — pedagogy/physics floor under mix/passaggio. | ✓ |
| OpenUtau default expressions (USTx.cs) | stakira/OpenUtau · 2026 | Editor surface maps gender/g (−100…100, formant shift), breath/B, breathiness curve, tension curve, voicing curve — production path for DiffSinger/resampler timbre, still not a register enum. | ✓ |
| SiFiSinger: A High-Fidelity End-to-End Singing Voice Synthesizer based on Source-filter Model | Cui, Gu, Weng, Zhang, Chen et al. · 2024 | Neural source–filter SVS with F0-driven harmonics and mcep envelope; control is F0+envelope, not isFalsetto/singer-formant params. | ✓ |
| Vocal Music under Phoneme-Conditional Analysis | Kim & Lee · 2026 | Isolates phoneme-conditional F1–F3, spectral tilt, H1–H2/HNR; analysis dimensions, not controllable register knobs. | ✓ |
| WORLD README | mmorise · 2025 | Public API is F0 + spectral envelope (CheapTrick) + aperiodicity (D4C) → synthesize; no register or singer-formant parameter names — envelope is opaque. | ✓ |
| nnsvs.gen class reference | nnsvs / r9y9 · 2022 | Score-locked path predicts/post-processes mgc, lf0, vuv, bap; relative_f0 ties LF0 to MIDI score pitch; vibrato_scale and phone V/UV flags exist — source-filter streams, not named formant/register knobs. | ✓ |
| vocal-synth-engine README | mcp-tool-shop-org · 2026 | Additive + spectral envelope + noise; cockpit/API exposes per-note breathiness, timbre, vibrato, portamento and XY timbre×breathiness — no documented singer-formant or falsetto/register field on VocalScore. | ✓ |
| ACE-Step 1.5 Inference API | ace-step · live | `GenerationParams` metadata is caption/lyrics + `bpm` / `keyscale` / `timesignature` / `duration` (+ CFG/seed). No note MIDI, no register, no formant fields — song-generator surface. | · |
| Analysis, synthesis, and perception of voice quality variations among female and male talkers | Klatt & Klatt · 1990 | A voice source is mixed periodic + glottal aspiration; aspiration noise cues breathiness more than H1 amplitude. | · |
| Articulatory interpretation of the singing formant | Sundberg · 1974 | The singer's formant is a ~2.8 kHz cluster from larynx-tube mismatch, not painted EQ. | · |
| Cantor Digitalis README | edwardbrowncross · live | Peer parametric SVS: perceptual API exposes `isFalsetto` (M1/M2), `tenseness`, `breathiness`, `vocalTractSize`, and synth-level F1–F6 formant centers. Explicit register boolean + formant tract — contrast class to DiffSinger/NNSVS/ACE-Step. | · |
| Coverage.py excluding code | coverage.py | Hold for catalog vs README count honesty. Limit: line coverage ≠ claim verification. | · |
| DiffSinger Best Practices | openvpi · live | Acoustic inputs fixed to phoneme seq + phoneme duration + F0; narrowly defined variance knobs are energy, breathiness, voicing, tension. Page does not name a register enum or singer-formant control. | · |
| DiffSinger ConfigurationSchemas | openvpi · live | Documents `predict_breathiness` / `predict_energy` / `predict_tension` / `predict_voicing`, `use_*_embed`, and inference `gender` scaled via `augmentation_args.random_pitch_shifting.range` + `use_key_shift_embed` (key-shift / timbre embed). No `isFalsetto` or F1–Fn formant keys. | · |
| DiffSinger README | openvpi · live | Fork markets variance models for pitch, energy, breathiness controllability and OpenUtau/DiffScope production; Apache-2.0. Still score-driven SVS, not pedagogy register enums. | · |
| Keep a Changelog 1.1.0 | keepachangelog · 1.1.0 | Hold for README Status matching catalog/DB. Limit: human changelog ≠ generated catalog/. | · |
| Measurements of the vibrato rate of ten singers | Prame · 1994 | Vibrato is not a 5-7 Hz law; mean 6.0 Hz but rate rises ~15% at endings; single cycles 4.6-8.7 Hz. | · |
| Nonlinear source-filter coupling in phonation: Theory | Titze · 2008 | At singing pitches source and filter are not independent; F0-F1 crossovers destabilize the folds. | · |
| OpenUtau default expressions (`USTx.cs`) | stakira · live | Editor registers `gender`/`gen` (−100…100, flag `g`), `gender (curve)`, `breath`/`bre`, `breathiness (curve)`, `tension (curve)`, `voicing (curve)`. Gender is the formant-shift surface; no chest/mix/head or falsetto enum. | · |
| SPDX Package verification code / NOASSERTION | SPDX · 2.3 | Hold for default verified=0 / do-not-assert until ACCEPT. Limit: package SBOM ≠ vocology finding gate. | · |
| SPEC Fair Use Rules | SPEC | Hold for README 12/175 verified-ratio honesty. Limit: SPEC public metrics ≠ KB SQLite verified bit. | · |
| Semantic Versioning 2.0.0 | semver.org | Hold for ACCEPT-gate: do not silent-mutate landed verified flags outside the gate. Limit: package release ≠ finding row. | · |
| Vocal tract resonances in singing: the soprano voice | Joliveau, Smith & Wolfe · 2004 | When F0 exceeds speech F1, a singer raises R1 to track F0; a fixed tract dumps the remaining harmonic into a dead zone and vowels collapse. | · |
| WORLD README | mmorise · live | Public analysis/synthesis surface is F0 + spectral envelope (CheapTrick) + aperiodicity (D4C). No register or singer-formant parameter names. | · |
| nnsvs.gen class reference | nnsvs · live | Score-locked path predicts/post-processes `mgc`, `lf0`, `vuv`, `bap`; `relative_f0` ties LF0 to MIDI; `vibrato_scale` and phone V/UV flags exist. Opaque WORLD streams — not named formant/register knobs. | · |
| pytest skip and xfail | pytest | Hold for ACCEPT-gate — unverified stays unverified. Limit: test outcomes ≠ prism ACCEPT ids. | · |

## Detail

### A four-parameter model of glottal flow · `load-bearing`
**The LF source is the derivative of glottal flow (Ee closing discontinuity + Ta return phase), not a harmonic oscillator.**
- **Implication:** Pitch-shifting a looped aah or Kokoro formant preset without open-quotient/return-phase/Ee cannot produce modal vs breathy vs pressed source spectra.
- **Identifier:** `STL-QPSR 26(4)`
- **Verify:** Primary STL-QPSR scan unreachable (KTH 500, RG 403). Google Books gives Fant/Liljencrants/Lin + exact title; arXiv:2410.04704 ref 17 cites STL-QPSR pp.1-13, 1985, defining Ee at glottal closure and Ta as return phase on the flow derivative.
- **Sources:** [A four-parameter model of glottal flow](https://www.speech.kth.se/qpsr/1985/1985_26_4_001-013.pdf)

### ACE-Step 1.5 Inference API · `load-bearing`
**GenerationParams metadata is caption/lyrics + bpm / keyscale / timesignature / duration — no note MIDI, no register, no formant; song-generator surface opposite the SVS craft axis.**
- **Implication:** Song-gen surface opposite score-lock.
- **Identifier:** `ACE-Step 1.5 INFERENCE`
- **Verify:** ACE-Step-1.5 docs/en/INFERENCE.md GenerationParams: caption, lyrics, instrumental, bpm, keyscale, timesignature, vocal_language, duration, plus sampler/DiT/LM fields. No note-MIDI, register or formant parameter anywhere in the surface.
- **Sources:** [ACE-Step 1.5 Inference API](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INFERENCE.md)

### Acoustic Theory of Speech Production · `load-bearing`
**The radiated voice is source × tract filter; independence is only a first approximation.**
- **Implication:** A formant-shaped oscillator that never generates a glottal flow and then filters it is not a voice.
- **Identifier:** `DOI:10.1515/9783110873429`
- **Verify:** Crossref on 10.1515/9783110873429 returns Fant, DE GRUYTER, issued 1971-12-31, ISBN 9789027916006 - the second edition, not the 1960 Mouton first edition, which carries no DOI. The source-times-filter formulation itself is canonical.
- **Sources:** [Acoustic Theory of Speech Production](https://doi.org/10.1515/9783110873429)

### Bi-stable vocal fold adduction · `load-bearing`
**Registers are glottal adduction shapes rather than F0 labels, for modal vs falsetto and mixed registration; the paper explicitly excludes fry/pulse register, calling it not mechanistically or spectrally unique.**
- **Implication:** One LF/waveguide source with only F0 changed cannot be SATB modal vs falsetto.
- **Identifier:** `PMC4167751`
- **Verify:** PMC4167751 = Titze, JASA 135(4):2091-2101, 2014. Modal/falsetto/mixed as convergent-vs-divergent adduction geometry confirmed, but the paper excludes fry: vocal fry, or pulse register, is not mechanistically or spectrally unique.
- **Sources:** [Bi-stable vocal fold adduction](https://pmc.ncbi.nlm.nih.gov/articles/PMC4167751/)

### Cantor Digitalis (Web Audio) README · `load-bearing`
**Perceptual API exposes isFalsetto (M1/M2), tenseness, breathiness, vocalTractSize, and synth-level F1–F6 formant centers — register is an explicit boolean, not an F0 label.**
- **Implication:** Only parametric surfaces expose isFalsetto + formants.
- **Identifier:** `Cantor Digitalis`
- **Verify:** npm cantor-digitalis README, author Edward Browncross, 0.0.6 published Feb 2026. Perceptual table lists isFalsetto bool described as Laryngeal mechanism (M1/M2), plus tenseness, breathiness, vocalTractSize; synth layer exposes F1-F6.
- **Sources:** [Cantor Digitalis (Web Audio) README](https://github.com/edwardbrowncross/cantor-digitalis)

### Cantor Digitalis tech notes · `load-bearing`
**Docs state the singing formant is produced by grouping F3–F5, with hypo-pharynx anti-resonance ~2.5–3.5 kHz — formant cluster is a tract setting, not painted EQ.**
- **Implication:** Singer formant is tract setting (F3–F5 cluster).
- **Identifier:** `Cantor tech notes`
- **Verify:** cantor_digitalis.md in edwardbrowncross/cantor-digitalis (notes on Feugere/d'Alessandro/Doval/Perrotin 2017): the singing formant can be produced by grouping the third, fourth and fifth formants; hypo-pharynx anti-resonances at 2.5-3.5 kHz.
- **Sources:** [Cantor Digitalis tech notes](https://raw.githubusercontent.com/edwardbrowncross/cantor-digitalis/main/cantor_digitalis.md)

### Chest/mix/head classification from mel texture around passaggio · `load-bearing`
**Classifies chest/mix/head-mix/head from mel-spectrogram texture around male passaggio; mixed voice is TA–CT balance, not a single F0 label.**
- **Implication:** Measurement/pedagogy naming ≠ SVS register enum.
- **Identifier:** `arXiv:2505.11378`
- **Verify:** arXiv:2505.11378v2, Kim & Botha 2025. Four classes chest/mix/head mix/head confirmed; mixed voice = TA and CT coordination; pitch alone does not fix register. Real title: ML Approaches to Vocal Register Classification.
- **Sources:** [Chest/mix/head classification from mel texture around passaggio](https://arxiv.org/abs/2505.11378)

### Controllable Singing Voice Synthesis using Phoneme-Level Energy Sequence · `load-bearing`
**Phoneme-level energy/dynamics control without register or singer-formant dimensions.**
- **Implication:** Energy control ≠ register enum.
- **Identifier:** `arXiv:2509.07038`
- **Verify:** arXiv:2509.07038, Ryu, Shin & Kim, 8 Sep 2025, exact title. Energy sequences from ground-truth spectrograms drive dynamics control, over 50% MAE reduction at phoneme level. No register or singer-formant dimension in the paper.
- **Sources:** [Controllable Singing Voice Synthesis using Phoneme-Level Energy Sequence](https://arxiv.org/abs/2509.07038)

### DiffSinger Best Practices · `load-bearing`
**Acoustic inputs are fixed to phoneme seq + phoneme duration + F0; narrow variance knobs are energy, breathiness, voicing, tension — no named register or singer-formant control.**
- **Identifier:** `DiffSinger BestPractices`
- **Verify:** openvpi/DiffSinger docs/BestPractices.md: three basic and fixed inputs are phoneme sequence, phoneme duration sequence and F0. Variance parameters documented are energy, breathiness, voicing, tension. No register or singer-formant control.
- **Sources:** [DiffSinger Best Practices](https://github.com/openvpi/DiffSinger/blob/main/docs/BestPractices.md)

### Flexible Singing Voice Synthesis Through Decomposed Framework with Inferrable Features · `load-bearing`
**Decomposed score-to-waveform feature streams; flexibility ≠ pedagogy register enums.**
- **Implication:** Feature decomposition; no register enums.
- **Identifier:** `arXiv:2407.09346`
- **Verify:** arXiv:2407.09346, Lester Phillip Violeta & Taketo Akama, 12 Jul 2024. Three-stage decomposition (linguistic, pitch contour, synthesis) over F0, V/UV, singer embedding, loudness. Full title begins A Preliminary Investigation on.
- **Sources:** [Flexible Singing Voice Synthesis Through Decomposed Framework with Inferrable Features](https://arxiv.org/abs/2407.09346)

### LAPS-Diff: Diffusion-Based SVS With Language Aware Prosody-Style Guided Learning · `load-bearing`
**Prosody/style guidance ≠ mixed-voice/passaggio registration or singer-formant tract settings.**
- **Implication:** Style/prosody ≠ register enum.
- **Identifier:** `arXiv:2507.04966`
- **Verify:** arXiv:2507.04966, Dhar, Gupta & Rao, 2025, exact title. Controls are language-aware embeddings plus style and pitch losses for Bollywood Hindi SVS. No mention of mixed voice, passaggio, registration or singer's formant anywhere.
- **Sources:** [LAPS-Diff: Diffusion-Based SVS With Language Aware Prosody-Style Guided Learning](https://arxiv.org/abs/2507.04966)

### Machine Learning Approaches to Vocal Register Classification in Contemporary Male Pop Music · `load-bearing`
**Full text (v2): 1008 three-second lead-vocal clips, stem-split from pop songs in Logic Pro, were rendered to mel-spectrograms producing 7221 initial images before splitting and augmentation — v1 states 4221 images for the same clip count. Four classes are indexed 0 chest / 1 mix / 2 head mix / 3 head. Augmentation was a horizontal flip plus two brightness variants; the split was 80/20. The SVM reached 0.94 overall accuracy on the test set with per-class metrics spanning 0.91–0.99; the CNN trained for six epochs (68.0% validation accuracy after epoch one). Register labels were assigned by ear from vocal-technique texts (Peckham 2010), not by EGG or laryngoscopy. The authors ship a tool, AVRA (Automatic Vocal Register Analysis). CC BY 4.0.**
- **Implication:** Wave 8 recorded this paper's four-class scheme but no performance; the measured floor is SVM 0.94 on held-out male pop. Two limits travel with that number. The ground truth is pedagogical annotation, so the classifier reproduces trained listeners' labels and inherits their disagreements — accuracy here is agreement with annotators, never laryngeal state. And the corpus is one genre, one voice type. Reuse the four-class scheme (splitting mix into mix / head-mix is load-bearing near the passaggio) and treat 0.94 as an in-domain ceiling. The v1/v2 image-count discrepancy means the version must be cited, not just the identifier.
- **Identifier:** `arXiv:2505.11378`
- **Verify:** arXiv:2505.11378v2 full text, section 3.1 verbatim: 'A total of 1008 audio clips were rendered into mel-spectrograms which produced 7221 initial images before splitting and augmentation'; class indices 0 chest / 1 mix / 2 head mix / 3 head;
- **Sources:** [Machine Learning Approaches to Vocal Register Classification in Contemporary Male Pop Music](https://arxiv.org/abs/2505.11378)

### Machine Learning with Evolutionary Parameter Tuning for Singing Registers Classification · `load-bearing`
**On a purpose-built dataset of 350 audio files spanning chest, mixed and head registers, 14 temporal features extracted with the TSFEL Python library fed three ML models whose hyperparameters were tuned by a Differential Evolution algorithm; the DE-optimised Extreme Gradient Boosting model reached an average classification accuracy of 97.60%. Signals 6(1) article 9, published 21 February 2025, open access under CC BY 4.0.**
- **Implication:** Register classification from audio alone is not an open problem to be routed around — it is a published result whose front end is engineered temporal features, not a neural embedding. A practice tool can gate on register from audio without a sensor. The caveats are the corpus (350 files, internally constructed, voice type and genre unstated in the abstract) and the label provenance, not the method.
- **Identifier:** `DOI:10.3390/signals6010009`
- **Verify:** Crossref 10.3390/signals6010009: exact title, Boratto Tales + 7, Signals 6(1) art. 9, 2025-02-21, license CC BY 4.0. Abstract verbatim: 350 audio files, TSFEL, '14 pieces of temporal information', Differential Evolution over three ML models
- **Sources:** [Machine Learning with Evolutionary Parameter Tuning for Singing Registers Classification](https://doi.org/10.3390/signals6010009)

### Modeling source-filter interaction in belting and high-pitched operatic male singing · `load-bearing`
**Source–filter interaction in belt vs classical; 2F0/F1–F2 inertance and register flip risk — pedagogy/physics floor under mix/passaggio.**
- **Implication:** Belt/opera source-filter floor.
- **Identifier:** `PMC2757425`
- **Verify:** PMC2757425 = Titze & Worley, JASA 126(3):1530-1540, 2009. Belt keeps F0 and 2F0 below F1; opera lowers F1 so 2F0 lifts over it. A harmonic crossing a formant destabilises fold vibration: pitch jumps, subharmonics, chaotic vibration.
- **Sources:** [Modeling source-filter interaction in belting and high-pitched operatic male singing](https://pmc.ncbi.nlm.nih.gov/articles/PMC2757425/)

### OpenUtau default expressions (USTx.cs) · `load-bearing`
**Editor surface maps gender/g (−100…100, formant shift), breath/B, breathiness curve, tension curve, voicing curve — production path for DiffSinger/resampler timbre, still not a register enum.**
- **Implication:** Breathiness/tension/gender on hard F0; no register enum.
- **Identifier:** `OpenUtau USTx`
- **Verify:** AddDefaultExpressions lives in OpenUtau.Core/Format/USTx.cs (not Ustx/): gender GEN -100..100 flag g, GENC curve, breath BRE 0..100 flag B, BREC, TENC, VOIC. No register or falsetto expression. Wiki confirms GENC is formant shift.
- **Sources:** [OpenUtau default expressions (USTx.cs)](https://raw.githubusercontent.com/stakira/OpenUtau/master/OpenUtau.Core/Format/USTx.cs)

### SiFiSinger: A High-Fidelity End-to-End Singing Voice Synthesizer based on Source-filter Model · `load-bearing`
**Neural source–filter SVS with F0-driven harmonics and mcep envelope; control is F0+envelope, not isFalsetto/singer-formant params.**
- **Implication:** F0/envelope surface; no register enums.
- **Identifier:** `arXiv:2410.12536`
- **Verify:** arXiv:2410.12536, Cui/Gu/Weng/Zhang/Chen/Dai, 16 Oct 2024, exact title. mcep decouples mel from F0; source excitation signals represent F0 per neural source-filter; differentiable mcep+F0 losses. Surface is F0 + envelope, no register param.
- **Sources:** [SiFiSinger: A High-Fidelity End-to-End Singing Voice Synthesizer based on Source-filter Model](https://arxiv.org/abs/2410.12536)

### Vocal Music under Phoneme-Conditional Analysis · `load-bearing`
**Isolates phoneme-conditional F1–F3, spectral tilt, H1–H2/HNR; analysis dimensions, not controllable register knobs.**
- **Implication:** F1–F3/tilt analysis ≠ register API.
- **Identifier:** `arXiv:2608.30823`
- **Verify:** arXiv:2608.30823 resolves (Hayoon Kim & Kyogu Lee, 31 Aug 2026), exact title. HTML feature section names articulatory impact as F1-F3, spectral tilt, H1-H2, HNR, formant deltas. Analysis features only; no synthesis control surface.
- **Sources:** [Vocal Music under Phoneme-Conditional Analysis](https://arxiv.org/abs/2608.30823)

### WORLD README · `load-bearing`
**Public API is F0 + spectral envelope (CheapTrick) + aperiodicity (D4C) → synthesize; no register or singer-formant parameter names — envelope is opaque.**
- **Implication:** mgc/BAP/LF0 ≠ formant/register APIs.
- **Identifier:** `WORLD`
- **Verify:** mmorise/World README: DIO and Harvest for F0, CheapTrick for spectral envelope, D4C for band aperiodicity, synthesis from those parameters only. No register, falsetto or singer-formant name; latest dated note is 2025/02/21.
- **Sources:** [WORLD README](https://github.com/mmorise/World)

### nnsvs.gen class reference · `load-bearing`
**Score-locked path predicts/post-processes mgc, lf0, vuv, bap; relative_f0 ties LF0 to MIDI score pitch; vibrato_scale and phone V/UV flags exist — source-filter streams, not named formant/register knobs.**
- **Implication:** Opaque streams under score lock.
- **Identifier:** `nnsvs.gen`
- **Verify:** nnsvs/gen.py: relative_f0 and vibrato_scale are real kwargs; under relative_f0, f0 = diff_lf0 + lf0_score from _midi_to_hz(pitch_idx), so LF0 is a residual on score MIDI. Streams mgc/lf0/vuv/bap + correct_vuv_by_phone; no formant name.
- **Sources:** [nnsvs.gen class reference](https://nnsvs.github.io/_modules/nnsvs/gen.html)

### vocal-synth-engine README · `load-bearing`
**Additive + spectral envelope + noise; cockpit/API exposes per-note breathiness, timbre, vibrato, portamento and XY timbre×breathiness — no documented singer-formant or falsetto/register field on VocalScore.**
- **Implication:** Generators/cockpit off register ACCEPT knobs.
- **Identifier:** `vocal-synth-engine`
- **Verify:** E:/AI/vocal-synth-engine clone: VocalNote has velocity/timbre/vibrato/portamentoSec; lanes dynamics/breathiness/timbreMorph; README XY pad = timbre x breathiness. grep falsetto|singer-formant|register over src/types, src/preset: 0 hits.
- **Sources:** [vocal-synth-engine README](https://github.com/mcp-tool-shop-org/vocal-synth-engine)

### ACE-Step 1.5 Inference API · `directional`
**`GenerationParams` metadata is caption/lyrics + `bpm` / `keyscale` / `timesignature` / `duration` (+ CFG/seed). No note MIDI, no register, no formant fields — song-generator surface.**
- **Implication:** STUDY-041 formant/register surface deepen.
- **Identifier:** `https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/docs/en/INFERENCE.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ACE-Step 1.5 Inference API](https://raw.githubusercontent.com/ace-step/ACE-Step-1.5/main/docs/en/INFERENCE.md)

### Analysis, synthesis, and perception of voice quality variations among female and male talkers · `directional`
**A voice source is mixed periodic + glottal aspiration; aspiration noise cues breathiness more than H1 amplitude.**
- **Implication:** Additive singing without a glottal noise source cannot do breath, /h/, or phrase-final decay.
- **Identifier:** `DOI:10.1121/1.398894`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Analysis, synthesis, and perception of voice quality variations among female and male talkers](https://doi.org/10.1121/1.398894)

### Articulatory interpretation of the singing formant · `directional`
**The singer's formant is a ~2.8 kHz cluster from larynx-tube mismatch, not painted EQ.**
- **Implication:** SATB additive presets without a narrowed epilarynx will lack male operatic ring.
- **Identifier:** `DOI:10.1121/1.1914609`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Articulatory interpretation of the singing formant](https://doi.org/10.1121/1.1914609)

### Cantor Digitalis README · `directional`
**Peer parametric SVS: perceptual API exposes `isFalsetto` (M1/M2), `tenseness`, `breathiness`, `vocalTractSize`, and synth-level F1–F6 formant centers. Explicit register boolean + formant tract — contrast class to DiffSinger/NNSVS/ACE-Step.**
- **Implication:** STUDY-041 formant/register surface deepen.
- **Identifier:** `https://raw.githubusercontent.com/edwardbrowncross/cantor-digitalis/main/README.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Cantor Digitalis README](https://raw.githubusercontent.com/edwardbrowncross/cantor-digitalis/main/README.md)

### Coverage.py excluding code · `directional`
**Hold for catalog vs README count honesty. Limit: line coverage ≠ claim verification.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `coverage-excluding`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Coverage.py excluding code](https://coverage.readthedocs.io/en/latest/excluding.html)

### DiffSinger Best Practices · `directional`
**Acoustic inputs fixed to phoneme seq + phoneme duration + F0; narrowly defined variance knobs are energy, breathiness, voicing, tension. Page does not name a register enum or singer-formant control.**
- **Implication:** STUDY-041 formant/register surface deepen.
- **Identifier:** `https://raw.githubusercontent.com/openvpi/DiffSinger/main/docs/BestPractices.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [DiffSinger Best Practices](https://raw.githubusercontent.com/openvpi/DiffSinger/main/docs/BestPractices.md)

### DiffSinger ConfigurationSchemas · `directional`
**Documents `predict_breathiness` / `predict_energy` / `predict_tension` / `predict_voicing`, `use_*_embed`, and inference `gender` scaled via `augmentation_args.random_pitch_shifting.range` + `use_key_shift_embed` (key-shift / timbre embed). No `isFalsetto` or F1–Fn formant keys.**
- **Implication:** STUDY-041 formant/register surface deepen.
- **Identifier:** `https://raw.githubusercontent.com/openvpi/DiffSinger/main/docs/ConfigurationSchemas.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [DiffSinger ConfigurationSchemas](https://raw.githubusercontent.com/openvpi/DiffSinger/main/docs/ConfigurationSchemas.md)

### DiffSinger README · `directional`
**Fork markets variance models for pitch, energy, breathiness controllability and OpenUtau/DiffScope production; Apache-2.0. Still score-driven SVS, not pedagogy register enums.**
- **Implication:** STUDY-041 formant/register surface deepen.
- **Identifier:** `https://github.com/openvpi/DiffSinger`
- **Verify:** no external verdict — not yet swept
- **Sources:** [DiffSinger README](https://github.com/openvpi/DiffSinger)

### Keep a Changelog 1.1.0 · `directional`
**Hold for README Status matching catalog/DB. Limit: human changelog ≠ generated catalog/.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `keepachangelog-1.1.0`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)

### Measurements of the vibrato rate of ten singers · `directional`
**Vibrato is not a 5-7 Hz law; mean 6.0 Hz but rate rises ~15% at endings; single cycles 4.6-8.7 Hz.**
- **Implication:** A constant LFO on F0 is a cartoon; rate and extent must move with phrase position.
- **Identifier:** `DOI:10.1121/1.410141`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Measurements of the vibrato rate of ten singers](https://doi.org/10.1121/1.410141)

### Nonlinear source-filter coupling in phonation: Theory · `directional`
**At singing pitches source and filter are not independent; F0-F1 crossovers destabilize the folds.**
- **Implication:** Holding a Pink-Trombone tract fixed while sweeping MIDI through F1 is a documented instability.
- **Identifier:** `DOI:10.1121/1.2832337`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Nonlinear source-filter coupling in phonation: Theory](https://doi.org/10.1121/1.2832337)

### OpenUtau default expressions (`USTx.cs`) · `directional`
**Editor registers `gender`/`gen` (−100…100, flag `g`), `gender (curve)`, `breath`/`bre`, `breathiness (curve)`, `tension (curve)`, `voicing (curve)`. Gender is the formant-shift surface; no chest/mix/head or falsetto enum.**
- **Implication:** STUDY-041 formant/register surface deepen.
- **Identifier:** `https://raw.githubusercontent.com/stakira/OpenUtau/master/OpenUtau.Core/Format/USTx.cs`
- **Verify:** no external verdict — not yet swept
- **Sources:** [OpenUtau default expressions (`USTx.cs`)](https://raw.githubusercontent.com/stakira/OpenUtau/master/OpenUtau.Core/Format/USTx.cs)

### SPDX Package verification code / NOASSERTION · `directional`
**Hold for default verified=0 / do-not-assert until ACCEPT. Limit: package SBOM ≠ vocology finding gate.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `spdx-noassertion`
- **Verify:** no external verdict — not yet swept
- **Sources:** [SPDX Package verification code / NOASSERTION](https://spdx.github.io/spdx-spec/v2.3/package-information/)

### SPEC Fair Use Rules · `directional`
**Hold for README 12/175 verified-ratio honesty. Limit: SPEC public metrics ≠ KB SQLite verified bit.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `spec-fairuse`
- **Verify:** no external verdict — not yet swept
- **Sources:** [SPEC Fair Use Rules](https://www.spec.org/fairuse.html)

### Semantic Versioning 2.0.0 · `directional`
**Hold for ACCEPT-gate: do not silent-mutate landed verified flags outside the gate. Limit: package release ≠ finding row.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `semver`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Semantic Versioning 2.0.0](https://semver.org/)

### Vocal tract resonances in singing: the soprano voice · `directional`
**When F0 exceeds speech F1, a singer raises R1 to track F0; a fixed tract dumps the remaining harmonic into a dead zone and vowels collapse.**
- **Implication:** MIDI noteOn that drives F0 above a fixed SATB F1 without jaw/lip modification is the named production error.
- **Identifier:** `DOI:10.1121/1.1791717`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Vocal tract resonances in singing: the soprano voice](https://doi.org/10.1121/1.1791717)

### WORLD README · `directional`
**Public analysis/synthesis surface is F0 + spectral envelope (CheapTrick) + aperiodicity (D4C). No register or singer-formant parameter names.**
- **Implication:** STUDY-041 formant/register surface deepen.
- **Identifier:** `https://raw.githubusercontent.com/mmorise/World/master/README.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [WORLD README](https://raw.githubusercontent.com/mmorise/World/master/README.md)

### nnsvs.gen class reference · `directional`
**Score-locked path predicts/post-processes `mgc`, `lf0`, `vuv`, `bap`; `relative_f0` ties LF0 to MIDI; `vibrato_scale` and phone V/UV flags exist. Opaque WORLD streams — not named formant/register knobs.**
- **Implication:** STUDY-041 formant/register surface deepen.
- **Identifier:** `https://nnsvs.github.io/_modules/nnsvs/gen.html`
- **Verify:** no external verdict — not yet swept
- **Sources:** [nnsvs.gen class reference](https://nnsvs.github.io/_modules/nnsvs/gen.html)

### pytest skip and xfail · `directional`
**Hold for ACCEPT-gate — unverified stays unverified. Limit: test outcomes ≠ prism ACCEPT ids.**
- **Implication:** STUDY-064 catalog/README honesty.
- **Identifier:** `pytest-skipping`
- **Verify:** no external verdict — not yet swept
- **Sources:** [pytest skip and xfail](https://docs.pytest.org/en/stable/how-to/skipping.html)

