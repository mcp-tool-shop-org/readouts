# How to draw it so a vision model can read it
_auto-created from wave lane_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

9 findings · 9 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| Acoustic spectral feedback in vocal learning: a systematic review of psychological mechanisms and skill outcomes | Zhang · 2026 | Spectrogram displays for vocal learning are thinly evidenced next to simple pitch-trajectory displays; recommended as auxiliary observation, not standalone instruction. | ✓ |
| Images and vision - API guide | OpenAI · 2026 | High-detail pipeline scales the short edge down to 768 px before tiling at 512 px. | ✓ |
| Sonic Visualiser: A Brief Reference (4.5) - layers | Cannam · 2020 | Layers stack like a graphics application: spectrogram at the back, notes and onsets in front. | ✓ |
| Sonic Visualiser: A Brief Reference (4.5) - log-frequency spectrogram axis | Cannam · 2020 | The log-frequency spectrogram replaces the numeric y-axis with a stylised piano keyboard, every octave's C shaded. | ✓ |
| Vision - developer documentation | Anthropic · 2026 | Claude reads images as 28x28-px patches, caps standard models at 1568 px long edge, and warns resizing can make text less legible. | ✓ |
| Vision language models are blind | Rahmanzadehgervi, Bolton, Taesiri & Nguyen · 2024 | Four SOTA VLMs average 58% on overlapping primitives but reach near-100% when marks are separated by space. | ✓ |
| librosa.amplitude_to_db (0.11) | librosa developers · 2025 | amplitude_to_db defaults to ref=1.0, top_db=80, thresholding 80 dB below the peak. | ✓ |
| librosa.display.cmap / specshow (0.11) | librosa developers · 2025 | librosa's canonical sequential colormap for dB-scaled data is magma. | ✓ |
| riffusion spectrogram_params.py | Forsgren & Martiros · 2023 | Riffusion encodes 512 HTK-mel bins to 10 kHz, 10 ms hop, power exponent 0.25, and stores render parameters in PNG EXIF. | ✓ |

## Detail

### Acoustic spectral feedback in vocal learning: a systematic review of psychological mechanisms and skill outcomes · `load-bearing`
**Spectrogram displays for vocal learning are thinly evidenced next to simple pitch-trajectory displays; recommended as auxiliary observation, not standalone instruction.**
- **Implication:** Always pair the spectrogram with a pitch-contour-vs-target line.
- **Identifier:** `DOI:10.3389/fpsyg.2026.1920074`
- **Verify:** DOI resolves: Front. Psychol. 2026, sole author Yuze Zhang, PRISMA review of 36 studies. Verbatim: evidence 'extremely limited'; position such tools 'as auxiliary means of observation rather than as standalone instructional interventions'.
- **Sources:** [Acoustic spectral feedback in vocal learning: a systematic review of psychological mechanisms and skill outcomes](https://pmc.ncbi.nlm.nih.gov/articles/PMC13537971/)

### Images and vision - API guide · `load-bearing`
**High-detail pipeline scales the short edge down to 768 px before tiling at 512 px.**
- **Implication:** Budget legibility against a 768-px-high render; keep the aspect wide-and-short.
- **Identifier:** `OpenAI images-vision guide`
- **Verify:** Live guide verbatim: fit within 2048x2048, then 'If the shortest side exceeds 768px, scale it down to 768px', then 'Count the 512px squares'. Applies to gpt-4o/4.1/4o-mini/gpt-5.1; newer GPT-5 variants are patch-based.
- **Sources:** [Images and vision - API guide](https://developers.openai.com/api/docs/guides/images-vision)

### Sonic Visualiser: A Brief Reference (4.5) - layers · `load-bearing`
**Layers stack like a graphics application: spectrogram at the back, notes and onsets in front.**
- **Implication:** Overlaying the piano roll and beat grid on the spectrogram is the established MIR idiom.
- **Identifier:** `Sonic Visualiser reference 4.5`
- **Verify:** Reference sect 1.1 verbatim: layers 'stacked on top of one another like layers in a graphics application', 'a spectrogram layer at the back', notes/onsets 'in front'. Sole author Chris Cannam; doc (c) 2006-2020, not 2024.
- **Sources:** [Sonic Visualiser: A Brief Reference (4.5) - layers](https://www.sonicvisualiser.org/doc/reference/4.5/en/)

### Sonic Visualiser: A Brief Reference (4.5) - log-frequency spectrogram axis · `load-bearing`
**The log-frequency spectrogram replaces the numeric y-axis with a stylised piano keyboard, every octave's C shaded.**
- **Implication:** Draw a keyboard strip with C shading instead of Hz ticks.
- **Identifier:** `Sonic Visualiser reference 4.5`
- **Verify:** Reference v4.5 sect 6.3 verbatim: 'a stylised piano keyboard as its vertical scale, with the C in each octave shaded in grey.' Claim exact. But the sole author is Chris Cannam and the doc is (c) 2006-2020, not 2024.
- **Sources:** [Sonic Visualiser: A Brief Reference (4.5) - log-frequency spectrogram axis](https://www.sonicvisualiser.org/doc/reference/4.5/en/)

### Vision - developer documentation · `load-bearing`
**Claude reads images as 28x28-px patches, caps standard models at 1568 px long edge, and warns resizing can make text less legible.**
- **Implication:** Render at exactly 1568 px wide; give a semitone whole patch rows.
- **Identifier:** `Anthropic vision docs`
- **Verify:** Live docs verbatim: 'Each patch is a 28x28-pixel block'; table gives Standard tier (all pre-4.7 models) max long edge 1568 px; resizing 'might, for example, make text less legible'. NB Claude 4.7+ tier is 2576 px.
- **Sources:** [Vision - developer documentation](https://platform.claude.com/docs/en/build-with-claude/vision)

### Vision language models are blind · `load-bearing`
**Four SOTA VLMs average 58% on overlapping primitives but reach near-100% when marks are separated by space.**
- **Implication:** The score overlay must be hollow, offset, never superimposed on the harmonic band.
- **Identifier:** `arXiv:2407.06581`
- **Verify:** arXiv:2407.06581, Rahmanzadehgervi/Bolton/Taesiri/Nguyen 2024. '58.07% accurate on average' is the 7-task BlindTest mean, not solely overlap tasks; 'near-100% accuracy when much more space is added to separate shapes'.
- **Sources:** [Vision language models are blind](https://arxiv.org/abs/2407.06581)

### librosa.amplitude_to_db (0.11) · `load-bearing`
**amplitude_to_db defaults to ref=1.0, top_db=80, thresholding 80 dB below the peak.**
- **Implication:** Clip 80 dB below peak and normalise per image.
- **Identifier:** `librosa 0.11 amplitude_to_db`
- **Verify:** librosa 0.11.0 docs: amplitude_to_db(S, *, ref=1.0, amin=1e-05, top_db=80.0); top_db is 'threshold the output at top_db below the peak: max(20 * log10(S/ref)) - top_db'. Exact on all three. Licence ISC.
- **Sources:** [librosa.amplitude_to_db (0.11)](https://librosa.org/doc/0.11.0/generated/librosa.amplitude_to_db.html)

### librosa.display.cmap / specshow (0.11) · `load-bearing`
**librosa's canonical sequential colormap for dB-scaled data is magma.**
- **Implication:** Magma is the MIR convention, but the one VLM measurement (finding 2) scored it below viridis: viridis default, magma alternate, both exposed.
- **Identifier:** `librosa 0.11 display.cmap`
- **Verify:** librosa 0.11.0 docs: cmap(data, *, robust=True, cmap_seq='magma', cmap_bool='gray_r', cmap_div='coolwarm'); unipolar data -> cmap_seq. dB data is unipolar, so magma. Licence ISC (permissive, not AGPL).
- **Sources:** [librosa.display.cmap / specshow (0.11)](https://librosa.org/doc/0.11.0/generated/librosa.display.cmap.html)

### riffusion spectrogram_params.py · `load-bearing`
**Riffusion encodes 512 HTK-mel bins to 10 kHz, 10 ms hop, power exponent 0.25, and stores render parameters in PNG EXIF.**
- **Implication:** Emit render parameters as a sidecar; a ^0.25 map is a proven alternative to dB clipping.
- **Identifier:** `riffusion-hobby spectrogram_params`
- **Verify:** Source: num_frequencies=512, max_frequency=10000, mel_scale_type='htk', step_size_ms=10, power_for_image=0.25, plus an ExifTags enum with to_exif/from_exif. All five exact. MIT licence, (c) 2022 Martiros & Forsgren.
- **Sources:** [riffusion spectrogram_params.py](https://github.com/riffusion/riffusion-hobby/blob/main/riffusion/spectrogram_params.py)

