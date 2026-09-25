# Building it in TypeScript, license-safe
_auto-created from wave lane_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

11 findings · 11 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| MIT JS building blocks for mel and CQT | npm registry (meljs, cqt-web, wavedraw) · 2026 | meljs 1.0.2 (NeMo-calibrated mel), cqt-web 1.0.4 (librosa-compatible CQT, WASM), wavedraw 2.7.0 (Node WAV + mel render) are all MIT. | ✓ |
| MelSpectrogram inconsistency with librosa melspectrogram (pytorch/audio #1058) | SolomidHero · 2020 | The librosa/torchaudio mel mismatch is a filed real-world bug class. | ✓ |
| Meyda audio features / npm 5.6.3 | Meyda project · 2024 | Meyda 5.6.3 is MIT with offline extraction, MFCC, chroma AND a first-class melBands feature (26 bands by default, present in the public MeydaAudioFeature type); last release 2024-04-21. | ✓ |
| OffscreenCanvas.convertToBlob(); pngjs 7.0.0; sharp 0.35.4 | MDN / npm · 2026 | convertToBlob produces PNG in every browser and in Workers; pngjs is pure-JS MIT; sharp is a native binary. | ✓ |
| TensorFlow.js API signal namespace; fft.js npm | Google / fft.js · 2024 | tfjs ships stft/frame/hannWindow but no mel filterbank op; fft.js is a MIT radix-4 FFT. | ✓ |
| Web Audio API 1.1 s1.8.5-1.8.6 AnalyserNode | W3C · 2024 | AnalyserNode mandates a Blackman window, 0.8 default smoothing, and reads only the most recent fftSize frames (max 32768). | ✓ |
| audio-analysis-mcp | zachswift615 · 2025 | An existing audio-analysis MCP server (librosa + matplotlib) saves visual outputs to disk and returns paths. | ✓ |
| essentia.js - npm registry metadata | MTG/UPF · 2021 | essentia.js is AGPL-3.0 and last published 2021-06-24. | ✓ |
| librosa.filters.mel vs torchaudio.transforms.MelSpectrogram defaults | librosa / PyTorch · 2025 | librosa's mel default is htk=False, norm='slaney'; torchaudio's is mel_scale='htk', norm=None. | ✓ |
| librosa.power_to_db (0.11) | librosa developers · 2025 | power_to_db defaults ref=1.0, amin=1e-10, top_db=80. | ✓ |
| whisper/audio.py log_mel_spectrogram | OpenAI · 2024 | Whisper's log-mel uses Hann/n_fft 400/hop 160, power, log10, a peak-relative clamp at max-8, then (x+4)/4. | ✓ |

## Detail

### MIT JS building blocks for mel and CQT · `load-bearing`
**meljs 1.0.2 (NeMo-calibrated mel), cqt-web 1.0.4 (librosa-compatible CQT, WASM), wavedraw 2.7.0 (Node WAV + mel render) are all MIT.**
- **Implication:** Read as reference implementations; meljs's NeMo constants would break librosa parity if vendored unchecked.
- **Identifier:** `npm cqt-web 1.0.4`
- **Verify:** npm and repo licences all MIT: meljs@1.0.2 "NeMo-compatible" (2026-02-06), cqt-web@1.0.4 "librosa-compatible CQT ... in WebAssembly" (2025-12-07), wavedraw@2.7.0 "Mel spectrogram rendering for Node.js". Solo repos: 1/1/7 stars.
- **Sources:** [MIT JS building blocks for mel and CQT](https://registry.npmjs.org/cqt-web)

### MelSpectrogram inconsistency with librosa melspectrogram (pytorch/audio #1058) · `load-bearing`
**The librosa/torchaudio mel mismatch is a filed real-world bug class.**
- **Implication:** Pick one reference (pinned librosa) and generate goldens from it.
- **Identifier:** `pytorch/audio issue 1058`
- **Verify:** GitHub API: pytorch/audio issue #1058 "MelSpectrogram inconsistency with librosa melspectrogram", opened by SolomidHero 2020-11-26, state closed. Body documents MelScale-vs-librosa value and scale divergence with plots.
- **Sources:** [MelSpectrogram inconsistency with librosa melspectrogram (pytorch/audio #1058)](https://github.com/pytorch/audio/issues/1058)

### Meyda audio features / npm 5.6.3 · `load-bearing`
**Meyda 5.6.3 is MIT with offline extraction, MFCC, chroma AND a first-class melBands feature (26 bands by default, present in the public MeydaAudioFeature type); last release 2024-04-21.**
- **Implication:** Usable for spectral scalars; the mel filterbank is still ours to write.
- **Identifier:** `npm meyda 5.6.3`
- **Verify:** MIT, 5.6.3 and 2024-04-21 all confirmed. REFUTED on mel: the published 5.6.3 tarball's main.d.ts MeydaAudioFeature union ends in "melBands", dist ships extractors/melBands.js, config default melBands: 26.
- **Sources:** [Meyda audio features / npm 5.6.3](https://meyda.js.org/audio-features)

### OffscreenCanvas.convertToBlob(); pngjs 7.0.0; sharp 0.35.4 · `load-bearing`
**convertToBlob produces PNG in every browser and in Workers; pngjs is pure-JS MIT; sharp is a native binary.**
- **Implication:** Raster PNG is the render target; a 30 s clip at 10 ms hop is 384,000 cells, so rect-per-cell SVG is out.
- **Identifier:** `MDN OffscreenCanvas.convertToBlob`
- **Verify:** MDN: default type image/png, "Browsers are required to support image/png", available in Web Workers, Baseline since March 2023. npm pngjs@7.0.0 MIT "pure JS"; sharp@0.35.4 Apache-2.0 with prebuilt libvips platform binaries.
- **Sources:** [OffscreenCanvas.convertToBlob(); pngjs 7.0.0; sharp 0.35.4](https://developer.mozilla.org/en-US/docs/Web/API/OffscreenCanvas/convertToBlob)

### TensorFlow.js API signal namespace; fft.js npm · `load-bearing`
**tfjs ships stft/frame/hannWindow but no mel filterbank op; fft.js is a MIT radix-4 FFT.**
- **Implication:** Skip the tensor runtime; take the FFT from fft.js and write ~200 lines of DSP.
- **Identifier:** `tfjs 4.22.0 / fft.js 4.0.4`
- **Verify:** tfjs-core/src/ops/signal contains exactly frame, hamming_window, hann_window, stft - no mel op (tfjs@4.22.0 latest, Apache-2.0). fft.js@4.0.4 MIT, README "Implementation of Radix-4 FFT". fft.js unpublished since 2021-01-11.
- **Sources:** [TensorFlow.js API signal namespace; fft.js npm](https://js.tensorflow.org/api/latest/)

### Web Audio API 1.1 s1.8.5-1.8.6 AnalyserNode · `load-bearing`
**AnalyserNode mandates a Blackman window, 0.8 default smoothing, and reads only the most recent fftSize frames (max 32768).**
- **Implication:** AnalyserNode is excluded from the analysis path; compute the STFT over the rendered AudioBuffer.
- **Identifier:** `W3C webaudio-1.1`
- **Verify:** All four points verbatim in s1.8.5/s1.8.6: "Apply a Blackman window", fftSize "MUST be a power of two in the range 32 to 32768", smoothingTimeConstant "default value is 0.8", "most recent fftSize sample-frames". MDN agrees.
- **Sources:** [Web Audio API 1.1 s1.8.5-1.8.6 AnalyserNode](https://www.w3.org/TR/webaudio-1.1/)

### audio-analysis-mcp · `load-bearing`
**An existing audio-analysis MCP server (librosa + matplotlib) saves visual outputs to disk and returns paths.**
- **Implication:** Precedent for path + numbers; match this repo's view_scored_piano_roll shape (path + inline image + summary).
- **Identifier:** `github audio-analysis-mcp`
- **Verify:** zachswift615/audio-analysis-mcp exists (created 2025-12-10, Python). pyproject deps librosa>=0.10.0 + matplotlib>=3.7.0; README shows spectrogram/waveform/waterfall/pitch returning {output_path}. Caveat: NO licence file.
- **Sources:** [audio-analysis-mcp](https://github.com/zachswift615/audio-analysis-mcp)

### essentia.js - npm registry metadata · `load-bearing`
**essentia.js is AGPL-3.0 and last published 2021-06-24.**
- **Implication:** Excluded: AGPL in the tree of an MIT npm package.
- **Identifier:** `npm essentia.js 0.1.3`
- **Verify:** npm: essentia.js@0.1.3 is latest, license AGPL-3.0, published 2021-06-24T22:43:38Z. MTG/essentia.js repo licence also AGPL-3.0. No release in 5 years. AGPL is disqualifying for shipped MIT code - the exclusion stands.
- **Sources:** [essentia.js - npm registry metadata](https://registry.npmjs.org/essentia.js)

### librosa.filters.mel vs torchaudio.transforms.MelSpectrogram defaults · `load-bearing`
**librosa's mel default is htk=False, norm='slaney'; torchaudio's is mel_scale='htk', norm=None.**
- **Implication:** Expose melScale and norm explicitly in the tool schema and pin them.
- **Identifier:** `librosa 0.11 filters.mel`
- **Verify:** librosa 0.11.0 filters.py L128: htk: bool = False, norm = "slaney". torchaudio main _transforms.py MelSpectrogram.__init__: norm: Optional[str] = None, mel_scale: str = "htk". Exact match on all four defaults.
- **Sources:** [librosa.filters.mel vs torchaudio.transforms.MelSpectrogram defaults](https://librosa.org/doc/0.11.0/generated/librosa.filters.mel.html)

### librosa.power_to_db (0.11) · `load-bearing`
**power_to_db defaults ref=1.0, amin=1e-10, top_db=80.**
- **Implication:** Tests use ref=1.0, top_db=null; peak-relative dB is display-only.
- **Identifier:** `librosa 0.11 power_to_db`
- **Verify:** librosa 0.11.0 core/spectrum.py, real implementation under @cache(level=30): def power_to_db(S, *, ref=1.0, amin=1e-10, top_db=80.0). All three defaults exact. Preceding @overload stubs use Ellipsis, not values.
- **Sources:** [librosa.power_to_db (0.11)](https://librosa.org/doc/0.11.0/generated/librosa.power_to_db.html)

### whisper/audio.py log_mel_spectrogram · `load-bearing`
**Whisper's log-mel uses Hann/n_fft 400/hop 160, power, log10, a peak-relative clamp at max-8, then (x+4)/4.**
- **Implication:** Peak-relative dB changes every value when a clip is trimmed; record ref explicitly.
- **Identifier:** `openai/whisper audio.py`
- **Verify:** whisper/audio.py at main, verbatim: N_FFT=400, HOP_LENGTH=160, torch.hann_window, abs()**2, clamp(min=1e-10).log10(), maximum(log_spec, log_spec.max()-8.0), (log_spec+4.0)/4.0. All five steps hold; file last edited 2024-11-26.
- **Sources:** [whisper/audio.py log_mel_spectrogram](https://github.com/openai/whisper/blob/main/whisper/audio.py)

