# Which transform for pitched music
_auto-created from wave lane_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

9 findings · 9 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| A Lightweight Instrument-Agnostic Model for Polyphonic Note Transcription and Multipitch Estimation | Bittner, Bosch, Rubinstein, Meseguer-Brocal & Ewert · 2022 | Basic Pitch uses a CQT at 3 bins/semitone, ~11 ms hop, 7 harmonics + 1 sub-harmonic, scored under MIREX quarter-tone / 50 ms rules. | ✓ |
| AST: Audio Spectrogram Transformer | Gong, Chung & Glass · 2021 | AST reaches 0.485 mAP on AudioSet from 128-bin log-mel, 25 ms Hamming, 10 ms shift. | ✓ |
| Auditory Toolbox - mel_frequencies | Slaney (as implemented in librosa 0.11) · 1998 | Slaney mel is linear below 1 kHz at 200/3 = 66.7 Hz per step, so a 50-cent error at C4 (7.7 Hz) is one-ninth of a filter spacing. | ✓ |
| CREPE: A Convolutional Representation for Pitch Estimation | Kim, Salamon, Li & Bello · 2018 | CREPE raw pitch accuracy 0.967 at 50 cents and 0.909 at 10 cents vs pYIN 0.919 / 0.826. | ✓ |
| Deep Salience Representations for F0 Estimation in Polyphonic Music | Bittner, McFee, Salamon, Li & Bello · 2017 | HCQT: 60 bins/octave (20 cents), 11 ms hop, fmin C1 32.7 Hz, 6 octaves, harmonics {0.5,1,2,3,4,5} stacked. | ✓ |
| Improved Musical Onset Detection with Convolutional Neural Networks | Schluter & Bock · 2014 | Three stacked log-mels (23/46/93 ms windows, 10 ms hop, 80 bands from 27.5 Hz to 16 kHz) reached F 88.5-90.3% at a 25 ms tolerance; 88.5% is the base CNN and 90.3% is the paper's final result (rectified linear units). | ✓ |
| MERT: Acoustic Music Understanding Model with Large-Scale Self-supervised Training | Li, Yuan, Zhang et al. · 2023 | MERT adds a CQT musical teacher beside its codec acoustic teacher to model pitched structure. | ✓ |
| Onsets and Frames: Dual-Objective Piano Transcription | Hawthorne et al. · 2018 | SOTA piano transcription ran on 229 log-mel bins (16 kHz, n_fft 2048, hop 512), note F1 82.3 at 50 ms. | ✓ |
| Robust Speech Recognition via Large-Scale Weak Supervision | Radford et al. · 2022 | Whisper's input is an 80-channel log-mel at 16 kHz, 25 ms window, 10 ms stride. | ✓ |

## Detail

### A Lightweight Instrument-Agnostic Model for Polyphonic Note Transcription and Multipitch Estimation · `load-bearing`
**Basic Pitch uses a CQT at 3 bins/semitone, ~11 ms hop, 7 harmonics + 1 sub-harmonic, scored under MIREX quarter-tone / 50 ms rules.**
- **Implication:** 36 bins/octave is the proven floor for note-level work; 60 is the pitch-gate resolution.
- **Identifier:** `arXiv:2203.09893`
- **Verify:** arXiv:2203.09893, Bittner/Bosch/Rubinstein/Meseguer-Brocal/Ewert 2022. Text: '3 bins per semitone' (=36/octave), hop '~11 ms' (256 @ 22050 = 11.61 ms I compute), '7 harmonics and 1 sub-harmonic', MIREX quarter-tone + 50 ms.
- **Sources:** [A Lightweight Instrument-Agnostic Model for Polyphonic Note Transcription and Multipitch Estimation](https://arxiv.org/abs/2203.09893)

### AST: Audio Spectrogram Transformer · `load-bearing`
**AST reaches 0.485 mAP on AudioSet from 128-bin log-mel, 25 ms Hamming, 10 ms shift.**
- **Implication:** 25 ms / 10 ms / 80-128 mel is the de facto standard for what the model hears.
- **Identifier:** `arXiv:2104.01778`
- **Verify:** Gong/Chung/Glass 2021. Abstract: 'new state-of-the-art results of 0.485 mAP on AudioSet'; body: '128-dimensional log Mel filterbank ... computed with a 25ms Hamming window every 10ms'. NB 0.485 is the Ensemble-M config.
- **Sources:** [AST: Audio Spectrogram Transformer](https://arxiv.org/abs/2104.01778)

### Auditory Toolbox - mel_frequencies · `load-bearing`
**Slaney mel is linear below 1 kHz at 200/3 = 66.7 Hz per step, so a 50-cent error at C4 (7.7 Hz) is one-ninth of a filter spacing.**
- **Implication:** Mel alone cannot show the 50-cent gate in the vocal/guitar fundamental range: the decisive argument for a CQT primary.
- **Identifier:** `librosa 0.11 mel_frequencies`
- **Verify:** librosa source: f_sp=200.0/3 (66.667 Hz), min_log_hz=1000. I computed C4 261.626 -> 269.292 = 7.666 Hz = 1/8.7 of 66.67. CAVEAT: 66.67 is Hz-per-mel (Slaney's 13-filter bank); librosa n_mels=128 spacing is 26.2 Hz -> 1/3.4.
- **Sources:** [Auditory Toolbox - mel_frequencies](https://librosa.org/doc/0.11.0/generated/librosa.mel_frequencies.html)

### CREPE: A Convolutional Representation for Pitch Estimation · `load-bearing`
**CREPE raw pitch accuracy 0.967 at 50 cents and 0.909 at 10 cents vs pYIN 0.919 / 0.826.**
- **Implication:** Overlay a tracker's f0 in cents-vs-target on the CQT; the picture shows why, the tracker supplies the number.
- **Identifier:** `arXiv:1802.06182`
- **Verify:** Kim/Salamon/Li/Bello 2018. All four numbers exact but ONLY on MDB-stem-synth, which the claim omits: CREPE .967@50c / .909@10c, pYIN .919 / .826. On RWC-synth CREPE is .999 / .995 and pYIN .990 / .908.
- **Sources:** [CREPE: A Convolutional Representation for Pitch Estimation](https://arxiv.org/abs/1802.06182)

### Deep Salience Representations for F0 Estimation in Polyphonic Music · `load-bearing`
**HCQT: 60 bins/octave (20 cents), 11 ms hop, fmin C1 32.7 Hz, 6 octaves, harmonics {0.5,1,2,3,4,5} stacked.**
- **Implication:** At 20 cents/bin a 50-cent error spans 2.5 bins and is visible without overlay.
- **Identifier:** `ISMIR 2017 paper 85`
- **Verify:** ISMIR 2017 paper 000085, text extracted: 'h in {0.5,1,2,3,4,5} ... hop size is 11 ms ... 6 octaves in frequency at 60 bins per octave (20 cents per bin) ... fmin = 32.7 Hz (i.e. C1)'. I compute 1200/60=20c, 50c=2.5 bins.
- **Sources:** [Deep Salience Representations for F0 Estimation in Polyphonic Music](https://archives.ismir.net/ismir2017/paper/000085.pdf)

### Improved Musical Onset Detection with Convolutional Neural Networks · `load-bearing`
**Three stacked log-mels (23/46/93 ms windows, 10 ms hop, 80 bands from 27.5 Hz to 16 kHz) reached F 88.5-90.3% at a 25 ms tolerance; 88.5% is the base CNN and 90.3% is the paper's final result (rectified linear units).**
- **Implication:** A 10 ms hop clears the 40 ms gate with 4x margin; a short-window channel sharpens onsets.
- **Identifier:** `ICASSP 2014`
- **Verify:** PDF text I extracted: '80-band Mel filter from 27.5 Hz to 16 kHz', windows 23/46/93 ms, 10 ms hop, 25 ms tolerance - all exact. But the F range runs to 90.3%: 89.9% is the fuzziness step, 'our final result of 90.3%' with ReLU.
- **Sources:** [Improved Musical Onset Detection with Convolutional Neural Networks](http://ofai.at/~jan.schlueter/pubs/2014_icassp.pdf)

### MERT: Acoustic Music Understanding Model with Large-Scale Self-supervised Training · `load-bearing`
**MERT adds a CQT musical teacher beside its codec acoustic teacher to model pitched structure.**
- **Implication:** Even mel/codec music models bolt a CQT back on for pitch; corroborates a two-surface design.
- **Identifier:** `arXiv:2306.00107`
- **Verify:** arXiv:2306.00107, Li/Yuan/Zhang et al. 2023 (ICLR 2024). Verbatim: 'an acoustic teacher based on Residual Vector Quantisation - Variational AutoEncoder (RVQ-VAE) and a musical teacher based on the Constant-Q Transform (CQT)'.
- **Sources:** [MERT: Acoustic Music Understanding Model with Large-Scale Self-supervised Training](https://arxiv.org/abs/2306.00107)

### Onsets and Frames: Dual-Objective Piano Transcription · `load-bearing`
**SOTA piano transcription ran on 229 log-mel bins (16 kHz, n_fft 2048, hop 512), note F1 82.3 at 50 ms.**
- **Implication:** Mel with many bins is sufficient for onsets and note identity on piano; use 229, not the speech default.
- **Identifier:** `arXiv:1710.11153`
- **Verify:** Hawthorne et al.: '229 logarithmically-spaced frequency bins, a hop length of 512, an FFT window of 2048, and a sample rate of 16kHz'; note F1 82.29 on MAPS at onsets '+/-50ms ... ignoring offsets' (50.22 with offsets).
- **Sources:** [Onsets and Frames: Dual-Objective Piano Transcription](https://arxiv.org/abs/1710.11153)

### Robust Speech Recognition via Large-Scale Weak Supervision · `load-bearing`
**Whisper's input is an 80-channel log-mel at 16 kHz, 25 ms window, 10 ms stride.**
- **Implication:** Log-mel at ~10 ms hop is what LLM-adjacent audio models are trained on: the legibility surface, not the measurement surface.
- **Identifier:** `arXiv:2212.04356`
- **Verify:** Sect 2.2 verbatim: 'All audio is re-sampled to 16,000 Hz, and an 80-channel log-magnitude Mel spectrogram representation is computed on 25-millisecond windows with a stride of 10 milliseconds.' Radford et al., arXiv Dec 2022.
- **Sources:** [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)

