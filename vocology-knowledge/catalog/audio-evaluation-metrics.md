# What a spectrogram can honestly measure
_auto-created from wave lane_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

9 findings · 9 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| A Survey on Evaluation Metrics for Music Generation | Kader & Karmaker · 2025 | FAD is distributional and needs large reference sets; CLAP measures prompt relevance; both align poorly with human preference. | ✓ |
| Chirp Group Delay based Onset Detection in Instruments with Fast Attack | Joysingh, Vijayalakshmi & Nagarajan · 2024 | Onset F1 near 0.88 is an average over guitar and solo-piano datasets (IDMT-SMT-Guitar, GuitarSet, MusicNet); no sung material was evaluated, so the figure does not transfer to a singing route without caveat. SuperFlux and the proposed method are close, but the CNN detector outperforms both on 2 of the 3 sets (GuitarSet 0.930, MusicNet 0.909). | ✓ |
| Correlation of Frechet Audio Distance With Human Perception of Environmental Audio Is Embedding Dependant | Tailleur et al. · 2024 | FAD's human agreement exceeds Spearman 0.5 with PANNs-WGM-LogMel and falls below 0.1 with VGGish. | ✓ |
| Frechet Audio Distance: A Metric for Evaluating Music Enhancement Algorithms | Kilgour, Zuluaga, Roblek & Sharifi · 2018 | Magnitude L2 correlated -0.01 and cosine -0.15 with human ratings; FAD 0.52. | ✓ |
| Maximum Filter Vibrato Suppression for Onset Detection | Bock & Widmer · 2013 | SuperFlux's maximum filter over spectral trajectories cuts onset false positives up to 60% on vibrato-heavy material. | ✓ |
| Pitch-and-Spectrum-Aware Singing Quality Assessment with Bias Correction and Model Fusion | Shi, Ai, Lu, Du & Ling · 2024 | The winning VoiceMOS 2024 track-2 singing submission (T08) reached utterance-level SRCC 0.620 and system-level 0.856; the same team's post-challenge PS-SQA reaches 0.639 utterance-level and 0.888 system-level. Utterance-level prediction is far weaker than system-level in both. | ✓ |
| RMVPE: A Robust Model for Vocal Pitch Estimation in Polyphonic Music | Wei, Cao, Dan & Chen · 2023 | RMVPE extracts vocal pitch from polyphonic mixes without separation, stable across SNR. | ✓ |
| SwiftF0: Fast and Accurate Monophonic Pitch Detection | Nieradzik · 2025 | SwiftF0 operates on the magnitude spectrogram, 91.8% harmonic mean at 10 dB SNR, 95,842 params, ~42x CREPE CPU speed. | ✓ |
| mir_eval: A Transparent Implementation of Common MIR Metrics | Raffel et al. · 2014 | mir_eval defaults encode 50 ms onset and 50 cent pitch tolerance. | ✓ |

## Detail

### A Survey on Evaluation Metrics for Music Generation · `load-bearing`
**FAD is distributional and needs large reference sets; CLAP measures prompt relevance; both align poorly with human preference.**
- **Implication:** Exclude FAD and CLAP from any single-take tool.
- **Identifier:** `arXiv:2509.00051`
- **Verify:** arXiv 2509.00051 HTML: FAD needs large reference sets (small ones bias it), CLAP is text-audio cosine similarity, and 'CLAP-score, FAD, and KLD often align poorly with human preferences' - cited to Yuan et al. 2025, secondary.
- **Sources:** [A Survey on Evaluation Metrics for Music Generation](https://arxiv.org/abs/2509.00051)

### Chirp Group Delay based Onset Detection in Instruments with Fast Attack · `load-bearing`
**Onset F1 near 0.88 is an average over guitar and solo-piano datasets (IDMT-SMT-Guitar, GuitarSet, MusicNet); no sung material was evaluated, so the figure does not transfer to a singing route without caveat. SuperFlux and the proposed method are close, but the CNN detector outperforms both on 2 of the 3 sets (GuitarSet 0.930, MusicNet 0.909).**
- **Implication:** Audio-derived onset error ships with a detector-confidence caveat and never overrides the MIDI-truth gate.
- **Identifier:** `arXiv:2408.13734`
- **Verify:** arXiv 2408.13734 HTML: eval sets are IDMT-SMT-Guitar, GuitarSet and MusicNet piano - NO vocal material at all. Proposed F1 .889/.912/.856 (avg ~.88); the CNN beats it on GuitarSet .930 and MusicNet .909, so 'comparably' overstates.
- **Sources:** [Chirp Group Delay based Onset Detection in Instruments with Fast Attack](https://arxiv.org/abs/2408.13734)

### Correlation of Frechet Audio Distance With Human Perception of Environmental Audio Is Embedding Dependant · `load-bearing`
**FAD's human agreement exceeds Spearman 0.5 with PANNs-WGM-LogMel and falls below 0.1 with VGGish.**
- **Implication:** If FAD ever ships, pin and name the embedding.
- **Identifier:** `arXiv:2403.17508`
- **Verify:** arXiv 2403.17508 abstract: PANNs-WGM-LogMel Spearman higher than 0.5, VGGish below 0.1, on DCASE 2023 Task 7 environmental sounds. Verbatim match. Domain is environmental audio; disclosed only in the paper title, not the claim.
- **Sources:** [Correlation of Frechet Audio Distance With Human Perception of Environmental Audio Is Embedding Dependant](https://arxiv.org/abs/2403.17508)

### Frechet Audio Distance: A Metric for Evaluating Music Enhancement Algorithms · `load-bearing`
**Magnitude L2 correlated -0.01 and cosine -0.15 with human ratings; FAD 0.52.**
- **Implication:** Never surface log-mel L1/L2 as a quality number; label it a deviation diagnostic.
- **Identifier:** `arXiv:1812.08466`
- **Verify:** arXiv 1812.08466 abstract gives FAD 0.52, SDR 0.39, cosine -0.15, magnitude L2 -0.01 against human ratings - exact match. Validation domain is music ENHANCEMENT, not singing; the claim text does not say so.
- **Sources:** [Frechet Audio Distance: A Metric for Evaluating Music Enhancement Algorithms](https://arxiv.org/abs/1812.08466)

### Maximum Filter Vibrato Suppression for Onset Detection · `load-bearing`
**SuperFlux's maximum filter over spectral trajectories cuts onset false positives up to 60% on vibrato-heavy material.**
- **Implication:** Use SuperFlux, not plain spectral flux, on the singing route.
- **Identifier:** `DAFx-13`
- **Verify:** DAFx archive abstract verbatim: heavy-vibrato music (sung opera, strings) sees false positives 'reduced by up to 60% without missing any additional events'. Böck & Widmer, DAFx-2013; sets include 1,448 operatic solo-voice onsets.
- **Sources:** [Maximum Filter Vibrato Suppression for Onset Detection](https://www.dafx.de/paper-archive/details/0oee-99Z88WL7pSo749gcA)

### Pitch-and-Spectrum-Aware Singing Quality Assessment with Bias Correction and Model Fusion · `load-bearing`
**The winning VoiceMOS 2024 track-2 singing submission (T08) reached utterance-level SRCC 0.620 and system-level 0.856; the same team's post-challenge PS-SQA reaches 0.639 utterance-level and 0.888 system-level. Utterance-level prediction is far weaker than system-level in both.**
- **Implication:** Aggregate across takes before any comparative claim.
- **Identifier:** `arXiv:2411.11123`
- **Verify:** arXiv 2411.11123 HTML Table 3: 0.639 utt / 0.888 sys belong to the paper's post-challenge PS-SQA, NOT the VoiceMOS 2024 track-2 winning submission (T08 = 0.620 utt / 0.856 sys). The utterance-vs-system gap holds either way.
- **Sources:** [Pitch-and-Spectrum-Aware Singing Quality Assessment with Bias Correction and Model Fusion](https://arxiv.org/abs/2411.11123)

### RMVPE: A Robust Model for Vocal Pitch Estimation in Polyphonic Music · `load-bearing`
**RMVPE extracts vocal pitch from polyphonic mixes without separation, stable across SNR.**
- **Implication:** Route pitch through RMVPE when the reference is a produced mix.
- **Identifier:** `arXiv:2306.15412`
- **Verify:** arXiv 2306.15412: title, year and claim all hold (no source separation; 'robust across all signal-to-noise ratio (SNR) levels'). Authors are wrong - the paper is Haojie Wei, Xueke Cao, Tangpeng Dan, Yueguo Chen. No author named Wang.
- **Sources:** [RMVPE: A Robust Model for Vocal Pitch Estimation in Polyphonic Music](https://arxiv.org/abs/2306.15412)

### SwiftF0: Fast and Accurate Monophonic Pitch Detection · `load-bearing`
**SwiftF0 operates on the magnitude spectrogram, 91.8% harmonic mean at 10 dB SNR, 95,842 params, ~42x CREPE CPU speed.**
- **Implication:** A spectrogram-derived pitch is legitimate when a trained model reads it; peak-picking a mel plot is not a substitute.
- **Identifier:** `arXiv:2508.18440`
- **Verify:** arXiv 2508.18440 abs + HTML: 91.80% HM at 10 dB SNR, 95,842 params, ~42x CREPE on CPU; input is STFT magnitude spectrogram 'rather than raw waveform data'. HM averages 3 sets: Bach10 (music), Vocadito (singing), SpeechSynth (speech).
- **Sources:** [SwiftF0: Fast and Accurate Monophonic Pitch Detection](https://arxiv.org/abs/2508.18440)

### mir_eval: A Transparent Implementation of Common MIR Metrics · `load-bearing`
**mir_eval defaults encode 50 ms onset and 50 cent pitch tolerance.**
- **Implication:** The 40 ms gate is stricter than convention; report the 50 ms figure alongside.
- **Identifier:** `ISMIR 2014`
- **Verify:** mir_eval docs: onset.f_measure window 'Default value = .05' (50 ms); melody raw_pitch_accuracy cent_tolerance=50. Paper is Raffel, McFee, Humphrey, Salamon, Nieto, Liang, Ellis, ISMIR 2014 (dblp RaffelMHSNLE14).
- **Sources:** [mir_eval: A Transparent Implementation of Common MIR Metrics](https://www.ee.columbia.edu/~dpwe/pubs/RaffMHS14-mireval.pdf)

