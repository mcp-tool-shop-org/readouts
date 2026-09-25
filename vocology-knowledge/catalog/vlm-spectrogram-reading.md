# What a vision model can read off a spectrogram
_auto-created from wave lane_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

10 findings · 10 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| A Picture is Worth A Thousand Numbers: Enabling LLMs Reason about Time Series via Visualization | Liu, Liu & Prakash · 2025 | Rendering a numeric series as an image instead of dumping numbers improved LLM reasoning ~140% and cut tokens ~99%. | ✓ |
| CaReCoS: A Spectrogram based Visual Benchmark for Cardiac, Respiratory and Cough Sounds | Rajgarhia et al. · 2026 | Best of nine current vision/omni models scored 51.2% on mel-spectrogram QA; none combined visual pattern recognition with domain knowledge reliably. | ✓ |
| CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs | Wang et al. · 2024 | GPT-4o reads realistic charts at 47.1% vs humans 80.5%. | ✓ |
| DEAF: A Benchmark for Diagnostic Evaluation of Acoustic Faithfulness in Audio Language Models | Xiong et al. · 2026 | Audio multimodal model predictions are driven mainly by text input even when acoustics contradict it. | ✓ |
| Evaluating few-shot prompting for spectrogram-based lung sound classification using a multimodal language model | Dietrich, McShannon & Rzepka · 2026 | GPT-4o on real clinical mel spectrograms: 32.0% zero-shot, 36.3% few-shot vs 25% chance. | ✓ |
| PitchBench: Measuring Pitch Hearing in Audio-Language Models | Liessens Dujardin et al. · 2026 | Audio-language models score 8-48% on pitch across 28 experiments, chords under 20%, and shift with notation (SPN good, Hz bad). | ✓ |
| Seeing isn't Hearing: Benchmarking Vision Language Models at Interpreting Spectrograms | Loakman, James & Lin · 2025 | Open VLMs read fine-grained speech content off spectrograms at chance (25%); phonetician 75%, ASR 87.6%; adding a waveform did not help. | ✓ |
| SonicBench: Dissecting the Physical Perception Bottleneck in Large Audio Language Models | Sun et al. · 2026 | Large audio-language models are strong on semantics but unreliable on pitch, timing, loudness and duration. | ✓ |
| Vision Language Models Are Few-Shot Audio Spectrogram Classifiers | Dixit, Heller & Donahue · 2024 | GPT-4o on labelled spectrogram images scored 59.0% on ESC-10 vs Gemini-1.5 native audio 49.6%, matching human spectrogram readers (73.75 vs 72.5 on fold 1). | ✓ |
| Vision Language Models Are Few-Shot Audio Spectrogram Classifiers (ablation) | Dixit, Heller & Donahue · 2024 | Ablation (default render = viridis, log frequency, log amplitude, axis labels on, colorbar off -> 27.5% zero-shot): linear frequency axis best (35.0%), linear amplitude 30.0%; magma (25.0%), mel (25.0%), showing a colorbar (23.75%), removing labels (26.25%), low resolution (20.0%) and MFCCs (13.75%) all below the default; few-shot exemplars lifted GPT-4o to 70-76%. | ✓ |

## Detail

### A Picture is Worth A Thousand Numbers: Enabling LLMs Reason about Time Series via Visualization · `load-bearing`
**Rendering a numeric series as an image instead of dumping numbers improved LLM reasoning ~140% and cut tokens ~99%.**
- **Implication:** Return image + compact numbers, never the raw frame matrix.
- **Identifier:** `arXiv:2411.06018`
- **Verify:** arXiv:2411.06018 v1 is Nov 2024 but the paper is NAACL 2025 pp.7486-7518, so 2025 is the venue year. Abstract: VL-Time gives 'about 140% average performance improvement and 99% average token costs reduction'.
- **Sources:** [A Picture is Worth A Thousand Numbers: Enabling LLMs Reason about Time Series via Visualization](https://arxiv.org/abs/2411.06018)

### CaReCoS: A Spectrogram based Visual Benchmark for Cardiac, Respiratory and Cough Sounds · `load-bearing`
**Best of nine current vision/omni models scored 51.2% on mel-spectrogram QA; none combined visual pattern recognition with domain knowledge reliably.**
- **Implication:** Pair the image with a text block of extracted features; domain knowledge is supplied, not assumed.
- **Identifier:** `arXiv:2607.03356`
- **Verify:** arXiv:2607.03356 exists, Rajgarhia et al., Jul 2026. Nine vision/omni models on mel-spectrogram QA drawn from seven medical audio collections, best 51.2%; paper states they fail to fuse visual patterns with clinical expertise.
- **Sources:** [CaReCoS: A Spectrogram based Visual Benchmark for Cardiac, Respiratory and Cough Sounds](https://arxiv.org/pdf/2607.03356)

### CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs · `load-bearing`
**GPT-4o reads realistic charts at 47.1% vs humans 80.5%.**
- **Implication:** Reading precise values off any plotted axis has a general ceiling.
- **Identifier:** `arXiv:2406.18521`
- **Verify:** arXiv:2406.18521 exists, Wang et al. 2024, 2,323 charts from arXiv papers. GPT-4o 47.1% vs human 80.5% - both are the REASONING-question split specifically, not the descriptive split. Exact.
- **Sources:** [CharXiv: Charting Gaps in Realistic Chart Understanding in Multimodal LLMs](https://charxiv.github.io/)

### DEAF: A Benchmark for Diagnostic Evaluation of Acoustic Faithfulness in Audio Language Models · `load-bearing`
**Audio multimodal model predictions are driven mainly by text input even when acoustics contradict it.**
- **Implication:** Blind the critic: describe the render before seeing the intended notes.
- **Identifier:** `arXiv:2603.18048`
- **Verify:** arXiv:2603.18048 exists, Xiong et al., Mar 2026. 'over 2,700 conflict stimuli' across prosody / background sounds / speaker identity; seven audio MLLMs show 'a consistent pattern of text dominance'. Claim is the headline finding.
- **Sources:** [DEAF: A Benchmark for Diagnostic Evaluation of Acoustic Faithfulness in Audio Language Models](https://arxiv.org/abs/2603.18048)

### Evaluating few-shot prompting for spectrogram-based lung sound classification using a multimodal language model · `load-bearing`
**GPT-4o on real clinical mel spectrograms: 32.0% zero-shot, 36.3% few-shot vs 25% chance.**
- **Implication:** Budget the surface as orientation, not measurement.
- **Identifier:** `DOI:10.1371/journal.pdig.0001179`
- **Verify:** DOI resolves: PLOS Digital Health 5(1):e0001179, Dietrich/McShannon/Rzepka 2026. GPT-4o on ICBHI-2017 clinical mel-spectrograms (128 bands): 0.320 zero-shot, 0.363 few-shot, four-class chance 25%. Exact.
- **Sources:** [Evaluating few-shot prompting for spectrogram-based lung sound classification using a multimodal language model](https://pmc.ncbi.nlm.nih.gov/articles/PMC12779135/)

### PitchBench: Measuring Pitch Hearing in Audio-Language Models · `load-bearing`
**Audio-language models score 8-48% on pitch across 28 experiments, chords under 20%, and shift with notation (SPN good, Hz bad).**
- **Implication:** Pitch belongs to DSP; when the model states pitch, use note names, never Hz.
- **Identifier:** `arXiv:2605.26176`
- **Verify:** arXiv:2605.26176 exists, Liessens Dujardin et al. 2026, 28 experiments. Chord quality 9.9-13.0% (<20%) and SPN best / Hz weakest both confirmed. Range top 47.7% matches; low bound read once as 8.4%, once 15.4% - not pinned.
- **Sources:** [PitchBench: Measuring Pitch Hearing in Audio-Language Models](https://arxiv.org/abs/2605.26176)

### Seeing isn't Hearing: Benchmarking Vision Language Models at Interpreting Spectrograms · `load-bearing`
**Open VLMs read fine-grained speech content off spectrograms at chance (25%); phonetician 75%, ASR 87.6%; adding a waveform did not help.**
- **Implication:** The 50-cent and 40-ms gates never route through the image.
- **Identifier:** `arXiv:2511.13225`
- **Verify:** 4-option MCQ so chance is 25%; zero-shot VLMs 'around chance-level (25%) across all conditions'; phonetician 'accuracy of 75.00%'; 'the ASR model achieves an accuracy of 87.56%'; 'no benefit ... inclusion of the waveform'.
- **Sources:** [Seeing isn't Hearing: Benchmarking Vision Language Models at Interpreting Spectrograms](https://arxiv.org/abs/2511.13225)

### SonicBench: Dissecting the Physical Perception Bottleneck in Large Audio Language Models · `load-bearing`
**Large audio-language models are strong on semantics but unreliable on pitch, timing, loudness and duration.**
- **Implication:** The picture localises; it never measures.
- **Identifier:** `arXiv:2601.11039`
- **Verify:** arXiv:2601.11039 exists, Sun et al., Jan 2026. Five dimensions / twelve attributes incl. pitch, loudness, duration, tempo. 'excel at semantic and paralinguistic tasks' vs 'near random guessing'; best 72% vs human 91%.
- **Sources:** [SonicBench: Dissecting the Physical Perception Bottleneck in Large Audio Language Models](https://arxiv.org/pdf/2601.11039)

### Vision Language Models Are Few-Shot Audio Spectrogram Classifiers · `load-bearing`
**GPT-4o on labelled spectrogram images scored 59.0% on ESC-10 vs Gemini-1.5 native audio 49.6%, matching human spectrogram readers (73.75 vs 72.5 on fold 1).**
- **Implication:** The image is a real channel at coarse-category resolution; never a gate.
- **Identifier:** `arXiv:2411.12058`
- **Verify:** arXiv:2411.12058 HTML: GPT-4o 59.00% cross-validated on ESC-10 spectrograms; 49.62% is Gemini-1.5 PRO on native audio; fold 1 GPT-4o 73.75% vs human expert ensemble 72.50%. All four exact.
- **Sources:** [Vision Language Models Are Few-Shot Audio Spectrogram Classifiers](https://arxiv.org/abs/2411.12058)

### Vision Language Models Are Few-Shot Audio Spectrogram Classifiers (ablation) · `load-bearing`
**Ablation (default render = viridis, log frequency, log amplitude, axis labels on, colorbar off -> 27.5% zero-shot): linear frequency axis best (35.0%), linear amplitude 30.0%; magma (25.0%), mel (25.0%), showing a colorbar (23.75%), removing labels (26.25%), low resolution (20.0%) and MFCCs (13.75%) all below the default; few-shot exemplars lifted GPT-4o to 70-76%.**
- **Implication:** Keep axis labels, no colorbar, expose frequency scale and colormap as parameters, ship labelled exemplar plates; neither the MIR-default log render nor magma is automatically best for a VLM.
- **Identifier:** `arXiv:2411.12058`
- **Verify:** All nine values exact: default 27.50 (viridis/log-freq/log-amp/labels-on/no-colorbar), lin-freq 35.0, lin-amp 30.0, magma 25.0, mel 25.0, colorbar 23.75, no-labels 26.25, low-res 20.0, MFCC 13.75; few-shot 70.00-76.25%.
- **Sources:** [Vision Language Models Are Few-Shot Audio Spectrogram Classifiers (ablation)](https://arxiv.org/html/2411.12058v1)

