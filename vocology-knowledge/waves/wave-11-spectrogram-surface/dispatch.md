# Wave 11 — The spectrogram surface: how an AI can see what it hears (study-swarm)

**KB** `vocology-knowledge` · **dispatched** 2026-09-07 · **5** Opus lanes · trigger: Director — study-swarm into mel spectrograms and how they can help AI visualize sound, for inclusion in AI Jam Sessions.

**Consumer:** `E:/AI/ai-jam-sessions` (v2.3.0). Today the model *sees* music only as the SVG piano roll rendered from MIDI, and *hears* it only through the humans in the room. The six engines already render real audio offline; the vocal route already gates SoulX-Singer takes on timing (40 ms) and pitch (50 cents). This wave asks what a spectrogram of that rendered audio can honestly give the model, which transform, how to draw it, what it can measure, and how to build it license-safe in TypeScript.

**Headline.** The five lanes converge from different directions: a spectrogram image is a real but *coarse* channel for a vision model (orientation, localisation, gross defects), mel is the representation audio models are trained on but is arithmetically blind to a 50-cent error below 1 kHz, every number must come from a DSP tracker, and the only batteries-included JS library is AGPL. So the surface is **two things, not one**: a constant-Q picture the model looks at, and DSP numbers it reasons with — with mel as the secondary "what the model hears" panel rather than the primary surface the Director named. **(Priority revised same day — see the supersession note above the lock: the picture is tier 3, the numbers and transcription lead.)**

---

## Research grounding

### A. What a vision model can actually read off a spectrogram

1. **A frontier VLM given a labelled spectrogram image beat a commercial audio-native model on the same clips and matched trained human readers on 10-class sound ID — at ~59% absolute.** Dixit, Heller & Donahue 2024, "Vision Language Models Are Few-Shot Audio Spectrogram Classifiers" (arXiv:2411.12058). https://arxiv.org/abs/2411.12058. Implication: the image is a real channel, at coarse-category resolution; never a gate.

2. **In the same paper's ablation (default render = viridis, log frequency, log amplitude, axis labels on, colorbar off → 27.5% zero-shot), a linear frequency axis scored best (35.0%) and linear amplitude 30.0%, while magma (25.0%), mel (25.0%), showing a colorbar (23.75%), removing the labels (26.25%), low resolution (20.0%) and MFCCs (13.75%) all scored below the default; few-shot exemplars lifted GPT-4o to 70–76%.** Dixit, Heller & Donahue 2024 (arXiv:2411.12058). https://arxiv.org/html/2411.12058v1. Implication: keep axis labels, no colorbar, expose the frequency scale and colormap as parameters, and ship labelled exemplar plates; neither the MIR-default log render nor magma is automatically what a VLM reads best.

3. **On fine-grained speech content every open VLM tested read spectrograms at chance (25%); a phonetician scored 75%, an ASR system 87.6%; adding a waveform did not help.** Loakman, James & Lin 2025, "Seeing isn't Hearing: Benchmarking Vision Language Models at Interpreting Spectrograms" (arXiv:2511.13225). https://arxiv.org/abs/2511.13225. Implication: the 50-cent and 40-ms gates never route through the image.

4. **On real clinical mel spectrograms GPT-4o scored 32.0% zero-shot and 36.3% few-shot against 25% chance.** Dietrich, McShannon & Rzepka 2026, "Evaluating few-shot prompting for spectrogram-based lung sound classification using a multimodal language model" (DOI:10.1371/journal.pdig.0001179). https://pmc.ncbi.nlm.nih.gov/articles/PMC12779135/. Implication: budget the surface as orientation, not measurement.

5. **Across nine current vision and omni models on mel-spectrogram question answering the best scored 51.2%.** Rajgarhia et al. 2026, "CaReCoS: A Spectrogram based Visual Benchmark for Cardiac, Respiratory and Cough Sounds" (arXiv:2607.03356). https://arxiv.org/pdf/2607.03356. Implication: pair the image with a text block of extracted features; domain knowledge is supplied, not assumed.

6. **Audio-native models are also unreliable at pitch (8–48% across 28 experiments, chords under 20%) and their answers shift with notation — scientific pitch notation good, Hz bad.** Liessens Dujardin et al. 2026, "PitchBench: Measuring Pitch Hearing in Audio-Language Models" (arXiv:2605.26176). https://arxiv.org/abs/2605.26176. Implication: pitch belongs to DSP; when the model must state pitch, hand it note names, never Hz.

7. **Rendering a numeric series as a picture instead of dumping the numbers improved LLM reasoning ~140% and cut tokens ~99%.** Liu, Liu & Prakash 2025, "A Picture is Worth A Thousand Numbers: Enabling LLMs Reason about Time Series via Visualization" (arXiv:2411.06018). https://arxiv.org/abs/2411.06018. Implication: return image + compact numbers, never the raw frame matrix.

8. **Audio multimodal models' predictions are driven mainly by their text input even when the acoustics contradict it.** Xiong et al. 2026, "DEAF: A Benchmark for Diagnostic Evaluation of Acoustic Faithfulness in Audio Language Models" (arXiv:2603.18048). https://arxiv.org/abs/2603.18048. Implication: blind the critic — the model must describe the render before it sees the intended notes.

9. **On realistic charts GPT-4o reads 47.1% vs humans 80.5%.** Wang et al. 2024, "CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs" (arXiv:2406.18521). https://charxiv.github.io/. Implication: reading precise values off any plotted axis has a general ceiling.

10. **Large audio-language models have a "physical perception bottleneck": strong on semantics, unreliable on pitch, timing, loudness and duration.** Sun et al. 2026, "SonicBench: Dissecting the Physical Perception Bottleneck in Large Audio Language Models" (arXiv:2601.11039). https://arxiv.org/pdf/2601.11039. Implication: the picture localises ("bar 3 is smeared"); it never measures.

### B. Which transform

11. **The harmonic CQT behind modern multi-f0 salience uses 60 bins per octave (20 cents), an 11 ms hop, fmin C1 = 32.7 Hz, 6 octaves, harmonics {0.5,1,2,3,4,5} stacked so harmonic energy is locally adjacent.** Bittner, McFee, Salamon, Li & Bello 2017, "Deep Salience Representations for F0 Estimation in Polyphonic Music" (ISMIR 2017). https://archives.ismir.net/ismir2017/paper/000085.pdf. Implication: at 20 cents per bin a 50-cent error spans 2.5 bins and is visible without any overlay.

12. **Basic Pitch transcribes on a CQT at 3 bins per semitone, ~11 ms hop, 7 harmonics + 1 sub-harmonic, scored under the MIREX quarter-tone / 50 ms rules.** Bittner, Bosch, Rubinstein, Meseguer-Brocal & Ewert 2022, "A Lightweight Instrument-Agnostic Model for Polyphonic Note Transcription and Multipitch Estimation" (arXiv:2203.09893). https://arxiv.org/abs/2203.09893. Implication: 36 bins per octave is the proven floor for note-level work; 60 is the pitch-gate resolution.

13. **Whisper's input is an 80-channel log-mel spectrogram at 16 kHz, 25 ms window, 10 ms stride.** Radford et al. 2022, "Robust Speech Recognition via Large-Scale Weak Supervision" (arXiv:2212.04356). https://arxiv.org/abs/2212.04356. Implication: log-mel at ~10 ms hop is what LLM-adjacent audio models are literally trained on — the right legibility surface even where it is the wrong measurement surface.

14. **AST reaches 0.485 mAP on AudioSet from 128-bin log-mel, 25 ms Hamming window, 10 ms shift — the same recipe.** Gong, Chung & Glass 2021, "AST: Audio Spectrogram Transformer" (arXiv:2104.01778). https://arxiv.org/abs/2104.01778. Implication: 25 ms / 10 ms / 80–128 mel is the de facto standard for "what the model hears".

15. **State-of-the-art piano transcription ran on 229 log-mel bins (16 kHz, n_fft 2048, hop 512) and scored note F1 82.3 at 50 ms onset tolerance.** Hawthorne et al. 2018, "Onsets and Frames: Dual-Objective Piano Transcription" (arXiv:1710.11153). https://arxiv.org/abs/1710.11153. Implication: mel with many bins is sufficient for onsets and note identity on piano — use 229, not the speech default.

16. **The best onset detector of its generation stacked three log-mels (23/46/93 ms windows, 10 ms hop, 80 bands) and hit F = 88.5–89.9% at a strict 25 ms tolerance.** Schlüter & Böck 2014, "Improved Musical Onset Detection with Convolutional Neural Networks" (ICASSP 2014). http://ofai.at/~jan.schlueter/pubs/2014_icassp.pdf. Implication: a 10 ms hop clears the 40 ms gate with 4× margin; a short-window channel sharpens onsets.

17. **Slaney-style mel (librosa default) is linear below 1 kHz at 200/3 ≈ 66.7 Hz per step, so at C4 a 50-cent error (7.7 Hz) is about one-ninth of a filter spacing.** Slaney 1998, "Auditory Toolbox" as implemented in librosa 0.11 `mel_frequencies`. https://librosa.org/doc/0.11.0/generated/librosa.mel_frequencies.html. Implication: mel alone cannot show the product's 50-cent gate in the vocal and guitar fundamental range — the decisive argument for a CQT primary.

18. **A dedicated tracker, not the transform, supplies sub-bin precision: CREPE reaches raw pitch accuracy 0.967 at 50 cents and 0.909 at 10 cents vs pYIN 0.919 / 0.826.** Kim, Salamon, Li & Bello 2018, "CREPE: A Convolutional Representation for Pitch Estimation" (arXiv:1802.06182). https://arxiv.org/abs/1802.06182. Implication: overlay a tracker's f0 in cents-vs-target on the CQT; the picture shows why, the tracker supplies the number.

19. **MERT adds a CQT "musical teacher" beside its codec acoustic teacher precisely to model pitched structure.** Li, Yuan, Zhang et al. 2023, "MERT: Acoustic Music Understanding Model with Large-Scale Self-supervised Training" (arXiv:2306.00107). https://arxiv.org/abs/2306.00107. Implication: even mel/codec music models bolt a CQT back on for pitch — corroborates a two-surface design.

### C. How to draw it so a vision model can read it

20. **librosa's canonical sequential colormap for dB-scaled data is `magma`.** librosa 0.11 `display.cmap` / `specshow`. https://librosa.org/doc/0.11.0/generated/librosa.display.cmap.html. Implication: magma is the MIR convention, but the one VLM measurement (2) scored it below viridis — so viridis is the default, magma the alternate, both exposed.

21. **`amplitude_to_db` defaults to `ref=1.0, top_db=80`, thresholding 80 dB below the peak.** librosa 0.11 `amplitude_to_db`. https://librosa.org/doc/0.11.0/generated/librosa.amplitude_to_db.html. Implication: clip 80 dB below peak and normalise per image so the colormap is spent on musical content.

22. **Sonic Visualiser's log-frequency spectrogram replaces the numeric y-axis with a stylised piano keyboard, every octave's C shaded.** Cannam et al., "Sonic Visualiser: A Brief Reference" 4.5. https://www.sonicvisualiser.org/doc/reference/4.5/en/. Implication: draw a keyboard strip with C shading instead of Hz ticks; semitone position becomes readable without arithmetic.

23. **The same reference stacks layers "like a graphics application": spectrogram at the back, notes and onsets in layers in front.** Cannam et al., Sonic Visualiser reference 4.5. https://www.sonicvisualiser.org/doc/reference/4.5/en/. Implication: overlaying the piano roll and beat grid on the spectrogram is the established MIR idiom.

24. **A 2026 systematic review finds spectrogram displays for vocal learning thinly evidenced next to simple pitch-trajectory displays and advises using them as auxiliary observation, not standalone instruction.** Zhang 2026, "Acoustic spectral feedback in vocal learning: a systematic review of psychological mechanisms and skill outcomes", Frontiers in Psychology 17:1920074 (DOI:10.3389/fpsyg.2026.1920074). https://pmc.ncbi.nlm.nih.gov/articles/PMC13537971/. Implication: always pair the spectrogram with a pitch-contour-vs-target line; never let it be the sole error signal.

25. **Claude reads images as 28×28-px patches, caps standard models at 1568 px long edge, and warns that resizing can make text less legible.** Anthropic 2026, "Vision" developer documentation. https://platform.claude.com/docs/en/build-with-claude/vision. Implication: render at exactly 1568 px wide so nothing is resampled; a semitone band should span whole patch rows.

26. **OpenAI's high-detail pipeline scales the short edge down to 768 px before tiling at 512 px.** OpenAI 2026, "Images and vision" API guide. https://developers.openai.com/api/docs/guides/images-vision. Implication: budget legibility against a 768-px-high render and keep the aspect wide-and-short.

27. **Four SOTA VLMs average 58% on fine-grained overlapping primitives but reach near-100% when the marks are separated by space.** Rahmanzadehgervi, Bolton, Taesiri & Nguyen 2024, "Vision language models are blind" (arXiv:2407.06581). https://arxiv.org/abs/2407.06581. Implication: the score overlay must be hollow, offset, and never superimposed on the harmonic band it annotates.

28. **Riffusion's image-as-audio encoding uses 512 HTK-mel bins to 10 kHz, 10 ms hop, a power-law amplitude exponent 0.25, and stores the render parameters in the PNG's EXIF so the image is self-describing.** Forsgren & Martiros, riffusion `spectrogram_params.py`. https://github.com/riffusion/riffusion-hobby/blob/main/riffusion/spectrogram_params.py. Implication: emit render parameters as a sidecar beside the image; a ^0.25 map is a proven alternative to dB clipping.

### D. What it can honestly measure

29. **Raw spectrogram distances are near-useless perceptual proxies: magnitude L2 correlated −0.01 and cosine −0.15 with human ratings; FAD 0.52.** Kilgour, Zuluaga, Roblek & Sharifi 2018, "Fréchet Audio Distance: A Metric for Evaluating Music Enhancement Algorithms" (arXiv:1812.08466). https://arxiv.org/abs/1812.08466. Implication: never surface log-mel L1/L2 as a quality number; label it as a deviation diagnostic only.

30. **FAD's human agreement is embedding-dependent — above Spearman 0.5 with PANNs-WGM-LogMel, below 0.1 with VGGish.** Tailleur et al. 2024, "Correlation of Fréchet Audio Distance With Human Perception of Environmental Audio Is Embedding Dependant" (arXiv:2403.17508). https://arxiv.org/abs/2403.17508. Implication: if FAD ever ships, pin and name the embedding.

31. **FAD is distributional and needs large reference sets; CLAP score measures prompt relevance, not quality; both "often align poorly with human preferences".** Kader & Karmaker 2025, "A Survey on Evaluation Metrics for Music Generation" (arXiv:2509.00051). https://arxiv.org/abs/2509.00051. Implication: exclude FAD and CLAP from any single-take tool.

32. **The MIR convention encoded in mir_eval defaults is 50 ms onset tolerance and 50 cents pitch tolerance.** Raffel et al. 2014, "mir_eval: A Transparent Implementation of Common MIR Metrics" (ISMIR 2014). https://www.ee.columbia.edu/~dpwe/pubs/RaffMHS14-mireval.pdf. Implication: the 40 ms gate is stricter than convention — keep it, report the 50 ms figure alongside for comparability.

33. **SuperFlux adds a maximum filter over spectral trajectories and cuts onset false positives by up to 60% on vibrato-heavy material.** Böck & Widmer 2013, "Maximum Filter Vibrato Suppression for Onset Detection" (DAFx-13). https://www.dafx.de/paper-archive/details/0oee-99Z88WL7pSo749gcA. Implication: use SuperFlux, not plain spectral flux, on the singing route.

34. **State-of-the-art onset detection sits near F1 0.88 across datasets; SuperFlux and CNN detectors perform comparably.** Joysingh, Vijayalakshmi & Nagarajan 2024, "Chirp Group Delay based Onset Detection in Instruments with Fast Attack" (arXiv:2408.13734). https://arxiv.org/abs/2408.13734. Implication: audio-derived onset error ships with a detector-confidence caveat and never silently overrides the MIDI-truth gate.

35. **SwiftF0 operates directly on the magnitude spectrogram, reaches 91.8% harmonic mean at 10 dB SNR (+12 points over CREPE) with 95,842 parameters at ~42× CREPE's CPU speed.** Nieradzik 2025, "SwiftF0: Fast and Accurate Monophonic Pitch Detection" (arXiv:2508.18440). https://arxiv.org/abs/2508.18440. Implication: a spectrogram-derived pitch is legitimate when a trained model reads the spectrogram; peak-picking a mel plot is not a substitute.

36. **RMVPE extracts vocal pitch directly from polyphonic mixes without separation, stable across SNR levels.** Wang et al. 2023, "RMVPE: A Robust Model for Vocal Pitch Estimation in Polyphonic Music" (arXiv:2306.15412). https://arxiv.org/abs/2306.15412. Implication: when the reference is a produced recording rather than a dry stem, route pitch through RMVPE.

37. **The singing-MOS benchmark states that existing objective metrics capture only limited perceptual aspects of singing quality (7,981 clips, 41 models).** Tang et al. 2025, "SingMOS-Pro: A Comprehensive Benchmark for Singing Quality Assessment" (arXiv:2510.01812). https://arxiv.org/abs/2510.01812. Implication: hard-code the caveat — passing the gates means "not obviously broken", never "sounds good".

38. **Even the winning VoiceMOS 2024 singing-quality predictor reaches only utterance-level SRCC 0.639 (system-level 0.888).** Shi, Ai, Lu, Du & Ling 2024, "Pitch-and-Spectrum-Aware Singing Quality Assessment with Bias Correction and Model Fusion" (arXiv:2411.11123). https://arxiv.org/abs/2411.11123. Implication: aggregate across takes before any comparative claim.

### E. Building it in TypeScript, license-safe

39. **essentia.js is AGPL-3.0 and last published 2021-06-24 (0.1.3).** MTG/UPF, essentia.js repository and npm registry metadata. https://registry.npmjs.org/essentia.js. Implication: excluded — AGPL in the tree of an MIT npm package.

40. **Meyda is MIT, supports offline extraction, exposes MFCC and chroma but no raw mel bands; last release 2024-04-21 (5.6.3).** Meyda project, npm registry and feature docs. https://meyda.js.org/audio-features. Implication: usable for spectral scalars; the mel filterbank is still ours to write.

41. **TensorFlow.js ships `stft`, `frame`, `hannWindow` but no mel filterbank op; `fft.js` is a MIT radix-4 FFT (4.0.4).** Google, TensorFlow.js API signal namespace; fft.js npm registry. https://js.tensorflow.org/api/latest/. Implication: skip the tensor runtime; take the FFT from fft.js and write ~200 lines of DSP.

42. **The Web Audio spec mandates a Blackman window and a default 0.8 smoothing time constant on `AnalyserNode`, which reads only the most recent fftSize frames (max 32768).** W3C, "Web Audio API 1.1" §1.8.5–1.8.6. https://www.w3.org/TR/webaudio-1.1/. Implication: AnalyserNode is excluded from the analysis path; compute the STFT over the rendered AudioBuffer.

43. **librosa's mel default is `htk=False, norm='slaney'`; torchaudio's is `mel_scale='htk', norm=None`.** librosa 0.11 `filters.mel`; PyTorch torchaudio `MelSpectrogram` docs. https://librosa.org/doc/0.11.0/generated/librosa.filters.mel.html. Implication: expose `melScale` and `norm` explicitly in the tool schema and pin them; "mel" is never left undefined.

44. **The librosa/torchaudio mel mismatch is a filed, real-world bug class.** SolomidHero 2020, "MelSpectrogram inconsistency with librosa melspectrogram", pytorch/audio issue #1058. https://github.com/pytorch/audio/issues/1058. Implication: pick one reference (pinned librosa) and generate goldens from it; never cross-check two libraries.

45. **Whisper's reference log-mel uses Hann / n_fft 400 / hop 160, power, log10, then a peak-relative clamp at max − 8 and an affine (x+4)/4.** OpenAI, `whisper/audio.py`. https://github.com/openai/whisper/blob/main/whisper/audio.py. Implication: peak-relative dB changes every value when a clip is trimmed — record `ref` explicitly.

46. **librosa `power_to_db` defaults `ref=1.0, amin=1e-10, top_db=80`.** librosa 0.11 `power_to_db`. https://librosa.org/doc/0.11.0/generated/librosa.power_to_db.html. Implication: tests use `ref=1.0, top_db=null`; peak-relative dB is a display-only option.

47. **MIT zero-dependency JS building blocks exist for both mel and CQT: `meljs` 1.0.2 (NeMo-calibrated, 2026-02), `cqt-web` 1.0.4 (librosa-compatible CQT, WASM, 2025-12), `wavedraw` 2.7.0 (Node WAV parse + mel render, 2026-06).** npm registry metadata. https://registry.npmjs.org/cqt-web. Implication: read them as reference implementations; meljs's NeMo constants would silently break librosa parity if vendored unchecked.

48. **An existing audio-analysis MCP server (Python, librosa + matplotlib) saves visual outputs to disk and returns paths.** zachswift615, "audio-analysis-mcp". https://github.com/zachswift615/audio-analysis-mcp. Implication: precedent for path + numbers; this repo's own convention (`view_scored_piano_roll`) is path + inline image + summary, which is the shape to match.

49. **`OffscreenCanvas.convertToBlob()` produces PNG in every browser and in Workers (Baseline 2023); `pngjs` 7.0.0 is pure-JS MIT; `sharp` is a native binary.** MDN, "OffscreenCanvas.convertToBlob()"; npm registry. https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas/convertToBlob. Implication: raster PNG is the render target — a 30 s clip at 10 ms hop is 384,000 cells, so rect-per-cell SVG (~15 MB) is out; SVG is reserved for axes and overlay.

---

> **SUPERSEDED IN PART, 2026-09-07 (same day).** The Director approved a reframing after this
> lock was written. The findings below are unchanged and still govern; what changed is the
> PRIORITY of the two surfaces. The picture is now tier 3, not the headline. The surface is an
> audio inspector mirroring this repo's consumer's existing MIDI inspector tools: deterministic
> numbers first (the gates), transcription second (audio enters the EXISTING `scorePerformance`
> and `renderScoredPianoRoll` stack as `MidiNoteEvent[]`), image last and optional. The revised
> lock lives with the consumer, at
> `E:/AI/ai-jam-sessions/docs/spectrogram-surface-study-2026-09.md`. Read L1–L8 below as the
> research-derived constraints they are; read the tiering there.

## Architectural lock (proposed — the Director gates it)

```
rendered take (AudioBuffer, 44.1/48 kHz)           ← existing engines / SoulX-Singer take
        ├─ own STFT (fft.js) → true CQT 60 bins/oct   (11, 12, 17)   → the PICTURE
        │        └─ log-mel 229 bins, 10 ms hop        (13–16)        → secondary panel
        │        └─ PNG 1568×784, viridis, keyboard strip, hollow score overlay (20–28)
        └─ DSP numbers                                  (29–38)        → the NUMBERS
                 SuperFlux onsets vs 40 ms (+50 ms mir_eval) · SwiftF0/pYIN cents vs target
                 RMVPE when the reference is a mix · log-mel L1 labelled "deviation, not quality"
view_spectrogram → temp path + inline PNG + summary block   (7, 48)
compare_audio    → numbers + hard-coded SingMOS-Pro caveat   (37, 38)
```

**L1. Two surfaces, not one.** The picture orients and localises ("measure 3, the D is smeared"); the numbers gate. No gate ever routes through the image (1–10). The mel spectrogram the Director named is the *secondary* panel: it is what audio models are trained on (13, 14) and is fine for onsets (15, 16), but a Slaney mel step is 66.7 Hz below 1 kHz and a 50-cent error at C4 is 7.7 Hz (17).

**L2. Primary transform = true constant-Q**, fmin C1 32.7 Hz, 60 bins per octave (20 cents), 6–7 octaves, hop 512 @ 44.1 kHz / 480 @ 48 kHz (11, 12), dB with `top_db` 80 and per-image peak normalisation (21). True per-bin kernels, not a pseudo-CQT over a long STFT: at C3 a 20-cent bin is 1.5 Hz, which no practical FFT bin resolves. Secondary panel = log-mel, n_fft 2048, hop 512, n_mels 229, fmin 30 Hz, fmax 11,025 Hz, power → dB, Slaney (15, 43). No chromagram.

**L3. Render spec.** PNG 1568 × 784 (25, 26); paged by measure range like `view_piano_roll`, about 6 s of audio per image (≈260 px/s, ≈4 px per 40-ms event); log-frequency y-axis spanning the notes in view (default C2–C7 ≈ 11–12 px per semitone); stylised keyboard strip with every C shaded and named (22); beat rules at low alpha, measure rules full-height with numbers (23); `viridis` default with `magma` as the alternate, both exposed via `colormap`, plus `frequencyScale` (2, 20); colorbar off, axis labels on (2); score overlay as hollow 2-px outlined rectangles at half semitone height, offset just above the fundamental band, blue right hand / coral left hand (27); render parameters emitted as sidecar JSON (28).

**L4. Blind-then-overlay.** The default call renders without the overlay and the tool text asks the model to describe what it sees before comparing; a second call with `overlay: true` adds the intended notes (8, 27). Pitch in the summary block is scientific pitch notation with cents, never Hz (6).

**L5. `compare_audio` numbers.** SuperFlux onsets (33) against the 40 ms gate with the 50 ms mir_eval figure alongside (32) and a detector-confidence caveat since SOTA F1 ≈ 0.88 (34); pitch through the existing SwiftF0 / pYIN gate (35, 18) in cents vs target, RMVPE when the reference is a produced mix (36); log-mel L1 exposed only as "timbre deviation" (29); no FAD, no CLAP (30, 31); the SingMOS-Pro caveat string is part of the output, not the docs (37, 38).

**L6. Stack.** `audio-decode` (MIT) → own STFT on `fft.js` (MIT) → own mel matrix with `melScale: 'slaney'|'htk'` and `norm` pinned in the zod schema (43, 44) → own CQT kernels with `cqt-web` as the browser reference (47) → `pngjs` in Node, `OffscreenCanvas.convertToBlob()` in the cockpit (49). Goldens generated once from pinned librosa 0.11 at relative tolerance ~1e-4 with `ref=1.0, top_db=null` (45, 46). `AnalyserNode` excluded (42); essentia.js excluded (39); tfjs and sharp not adopted (41, 49).

**L7. Return shape** matches `view_scored_piano_roll`: temp file path, inline image block, and a short text summary of the DSP numbers — never the raw matrix (7, 48).

**L8. Uncertainty gate — a P0 measurement before L2/L3 are ratified.** No study measures a VLM reading a spectrogram on a *music* task (Lane A gap), and finding 2 shows render choice swings accuracy by 7.5 points with the MIR default not the winner. The executor runs an in-repo A/B on a jam-sessions task ("which measure has the wrong note / the late onset?") across three axes — transform {CQT-log, linear-STFT/linear-amplitude, mel}, colormap {viridis, magma}, and {blind, overlay} — scored against MIDI truth, before the render default is frozen. Dixit's ablation was ten classes of environmental sound on one model; nothing says its winner transfers to reading a piano take. Contrastive frame for the Director: *you asked for a mel spectrogram; this lock makes mel the secondary panel and CQT the primary, because mel cannot show the 50-cent gate below 1 kHz (17) — override if the surface is meant for orientation only, in which case mel-only at 229 bins is sufficient (15).*

---

## What this wave does not do

- No code. The lock is a proposal; the executor session builds it after the Director gates L8.
- No claim that the model can *hear* through the picture. Findings 3–6 and 10 bound what the image gives.
- No FAD/CLAP "quality" score, ever, on a single take (29–31).

## Not retrieved (CANNOT_CONFIRM — surfaced, not load-bearing)

- Liu & Heer 2018, "Somewhere Over the Rainbow" (CHI) — the canonical human colormap-accuracy study; PDF and page unreadable. The only colormap number in hand is the VLM one in finding 2 (viridis 27.5 vs magma 25.0 on ESC-10, one model); hence `colormap` stays a parameter under L8, with viridis as the evidence-backed default rather than a locked value.
- The ESC-50 (50-class) accuracy figure for the same paper — the lane reported 14%, the retrieved text confirms the harder subset was run but the number was not found in the grep, so it is not stated here.
- Schörkhuber & Klapuri 2010 CQT toolbox full text; Brown & Puckette 1992 CQT kernels — not retrieved, so the "true CQT" rule in L2 stands on arithmetic and on 11/12, not on those papers.
- Sing&See efficacy studies (403); an MCD-vs-MOS coefficient (−0.28 seen only in a snippet, excluded); SuperFlux's per-dataset table (PDF mirrors unparseable).
- The pytorch/audio #1058 resolution recipe (`norm='slaney'`, `mel_scale='slaney'`, `pad_mode='constant'`) — seen only in search summaries; treat as unverified.

## Standards compliance (this wave)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Five lane prompts recorded in the session; every finding carries authors / year / title / identifier / URL; lanes ran on Opus, coordinator on Fable; dated 2026-09-07. Remediation: pin lane prompts into a `dispatch.lock.json` (owner: next wave). |
| ANDON_AUTHORITY | 3 | Lane A halted the "gate through the image" reading before any design; lane B demoted the Director-named mel from primary to secondary on arithmetic (17); lane E rejected the only batteries-included library on license. |
| NAMED_COMPENSATORS | 2 | No irreversible action taken (no credits, no installs, no commits by lanes). Rollback of the lock = delete this wave folder and `load_db.py` re-run without it; the ai-jam-sessions doc is uncommitted until the operator says go. |
| DECOMPOSE_BY_SECRETS | 3 | One question per lane (VLM reading / transform / rendering / measurement / implementation), no overlap; CREPE and Dixit were the only cross-lane hits and are merged here. |
| UNCERTAINTY_GATED_HUMANS | 3 | L8 is an explicit uncertainty gate with a contrastive frame; the CANNOT_CONFIRM list is surfaced rather than silently kept. |
| EXTERNAL_VERIFIER | 2→3 pending | Run through `roleos verify-citations` → `prism verify --type citations` on a non-Claude Ollama seat with the retrieval oracle; receipt in [`verification.md`](verification.md) / [`citation-receipt.json`](citation-receipt.json). |
