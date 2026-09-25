# SVS vs lyrics-to-song routes
_Score-conditioned singing synthesis vs mixed-song generators; MIDI-lock and licenses_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

38 findings · 21 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| ACE-Step 1.5 | Gong, Song, Zhao et al. · 2026 | Lyrics+caption → mixed song; MIT; BPM/key are metadata, not note MIDI. | ✓ |
| CoMelSinger: Discrete Token-Based Zero-Shot Singing Synthesis With Structured Melody Control and Guidance | Zhao, Zeng, Lyu & Wang · 2025 | Zero-shot SVS with lyric + pitch tokens under MaskGCT; contrastive anti-prosody-leakage hardens score-lock beyond STUDY-011 MIDI+lyrics. | ✓ |
| DiTSinger: Scaling Singing Voice Synthesis with Diffusion Transformer and Implicit Alignment | Du, Deng, Guo et al. · 2025 | DiT SVS conditioned on pitch, phonemes, word durations, slur; still score-bound (implicit alignment does not drop MIDI). | ✓ |
| DiffRhythm 2 | Jiang, Chen, Ning et al. · 2025 | Paper states SVS produces vocals with predefined melodies; song generation does not; Apache 2.0 v2 weights. | ✓ |
| DiffSinger | Liu, Li, Ren, Chen & Zhao · 2022 | DiffSinger is score-conditioned SVS (lyrics+pitch+duration → mel); MIDI-B path in official repo; code MIT / OpenVPI Apache 2.0; RTF 0.191. | ✓ |
| DiffSinger ConfigurationSchemas | openvpi / DiffSinger · 2024 | Variance pitch defaults predict_pitch + use_melody_encoder; midi_smooth_width smooths MIDI step→base pitch — MIDI is the prior. | ✓ |
| DiffSinger README | openvpi / DiffSinger · 2024 | Fork positioned as SVS production tooling (OpenUtau/DiffScope); variance controllability on score-driven synthesis. | ✓ |
| LeVo: High-Quality Song Generation with Multi-Preference Alignment | Lei, Xu, Lin et al. · 2025 | Lyrics (+ optional text descriptions and optional audio prompts) -> mixed song; song-section structure labels (verse/chorus, auto-extracted with All-In-One) plus open-vocabulary tags, with no note-level MIDI lock (MIDI is never mentioned in the paper). BPM is NOT a stated conditioning label. Availability today: the official repo github.com/tencent-ailab/songgeneration returns 404 and huggingface.co/tencent/SongGeneration returns 401; only unlicensed third-party mirrors remain. | ✓ |
| MPEcho: A Melody and Phoneme-Aware Generative Framework for Controllable Cover Song Generation | Lee, Yeh, Hu, Tan, Tsai & Yang · 2026 | Cover CSG conditioned on melody and phonemes; still ≠ MIDI+lyrics score-lock SVS. | ✓ |
| NNSVS | Yamamoto, Yoneyama & Toda · 2022 | NNSVS+WORLD hard-locks phone durations to note length (post-processing normalises phone durations so their sum equals the note duration); MIT + WORLD modified-BSD; MOS 3.86 vs recordings 4.39. No RTF or real-time figure is reported in arXiv:2210.15987 - drop the real-time claim or source it elsewhere. Repo dormant since 2023-10. | ✓ |
| OpenUtau MidiWriter.cs | openutau / OpenUtau (repo renamed from stakira/OpenUtau; stakira remains lead maintainer) · 2024 | MIDI import builds UNote from NoteNumber/Time/Length and attaches LyricEvent; pitch×time×lyric co-enforced. | ✓ |
| SemBridge: Semantic Token Anchoring for Continuous-Latent Autoregressive Speech Generation | Xie, Lin, Qian, Guo, Jiang, Wang et al. · 2026 | Score-conditioned SVS with lyrics plus score-derived pitch and duration under semantic anchoring. | ✓ |
| SmoothSinger: A Conditional Diffusion Model for Singing Voice Synthesis with Multi-Resolution Architecture | Sui, Xiang & Jin · 2025 | Conditional diffusion SVS from musical scores requiring precise pitch, duration, articulation — score-bound, not mixed-song gen. | ✓ |
| SongEcho: Towards Cover Song Generation via Instance-Adaptive Element-wise Linear Modulation | Li, Li, Wang, Zhang, Wu, Deussen et al. · 2026 | Cover-song generation synthesizes vocals+accompaniment; contrasts with SVS/SVC single-track score-controlled vocals. | ✓ |
| SongGen: A Single Stage Auto-regressive Transformer for Text-to-Song Generation | Liu, Ding, Zhang et al. · 2025 | Single-stage text-to-song (lyrics + descriptions ± voice clip); no MIDI note hard constraint. | ✓ |
| SoulX-Singer: Towards High-Quality Zero-Shot Singing Voice Synthesis | Qian et al. · 2026 | Score-control mode takes MIDI + lyrics only; MIDI timing constraints lower WER vs melody-only F0 mode under lyric rewrite. | ✓ |
| StyleSinger | Zhang, Huang, Li et al. · 2024 | Notes+lyrics SVS plus reference clip; trained on M4Singer under CC BY-NC-SA 4.0. The paper's Ethics Statement promises restrictions on code and models, but that never happened - code and checkpoints were released in 2024.05 under MIT and remain public and ungated. The commercial blocker is the CC-BY-NC-SA-4.0 training data, not an author-imposed restriction. | ✓ |
| TCSinger 2: Customizable Multilingual Zero-shot Singing Voice Synthesis | Zhang, Guo, Pan, Yao, Zhu, Jiang et al. · 2025 | Multilingual zero-shot SVS that still takes lyrics plus music notation extracted from the score - not a lyrics-to-song foundation model. It is NOT dependent on phoneme/note boundary structure: the Blurred Boundary Content encoder is the paper's stated contribution for removing reliance on phoneme and note boundary annotations, predicting duration itself and masking boundaries. Code AaronZ345/TCSinger2 is MIT. | ✓ |
| VISinger 2 | Zhang, Xue, Li, Xie et al. · 2022 | Predicted F0 drives a DDSP harmonic oscillator as a hard pitch constraint (f_k = k*f_0). Official Opencpop pre-trained weights ARE published from the author's own repo, but zhangyongmao/VISinger2 carries no LICENSE file at all - all rights reserved, so the weights are not commercially usable. | ✓ |
| YingMusic-Singer: Zero-shot Singing Voice Synthesis and Editing with Annotation-free Melody Guidance | Zheng, Hao, Ma, Zhang, Chen, Ding et al. · 2025 | Melody-driven SVS without phoneme-level duration/pitch annotation; soft annotation vs hard MIDI — still not free lyrics-to-song. | ✓ |
| so-vits-svc 4.0 | innnky / SVC community · 2023 | Converts a dry vocal into a cloned singer; F0 comes from the source recording, not MIDI; AGPL-3.0. | ✓ |
| A Comparison of Discrete and Soft Speech Units for Improved Voice Conversion | van Niekerk, Carbonneau, Zaïdi, Baas et al. · 2021 | SoftVC: transform source speech into a target voice while keeping content unchanged; soft units retain more linguistic content than discrete units (so-vits-svc SoftVC content-encoder lineage). | · |
| ACE-Step 1.5: Pushing the Boundaries of Open-Source Music Generation | Gong, Song, Zhao, Wang et al. · 2026 | Unified editing toolkit includes cover generation, repainting, vocal-to-BGM; cover re-synthesizes timbre while retaining melodic skeletons via quantized latents — cover/repaint pole, not note-MIDI score-lock. | · |
| ACE-Step: A Step Towards Music Generation Foundation Model | Gong, Zhao, Wang et al. · 2025 | Lyrics+caption → mixed song; BPM/duration size a latent canvas — free-generator pole that breaks note-level MIDI+lyrics hard lock (contrast SVS score-lock; no invent) | · |
| DiffRhythm 2: Efficient and High Fidelity Song Generation via Block Flow Matching | Jiang, Chen, Ning, Yao et al. · 2025 | Explicit pole: unlike singing voice synthesis, which produces vocals with predefined melodies, song generation does not — free song-gen vs score/melody-predefined SVS. | · |
| DiffSVC: A Diffusion Probabilistic Model for Singing Voice Conversion | Liu, Cao, Su, Meng · 2021 | SVC with PPGs as content features plus fundamental-frequency and loudness features as auxiliary inputs to the denoiser — content+F0+loudness taken from the source performance, not a MIDI score. | · |
| DiffSinger: Singing Voice Synthesis via Shallow Diffusion Mechanism | Liu, Li, Ren et al. · 2021 | Diffusion acoustic model conditioned on music score (lyrics+pitch+duration → mel; MIDI-B path) — score-bound SVS pole opposite free lyrics-to-song generators | · |
| FreeSVC: Towards Zero-shot Multilingual Singing Voice Conversion | Ferreira, Gris, da Rosa, de Oliveira et al. · 2025 | Zero-shot multilingual SVC (enhanced VITS + SPIN content + ECAPA2 speaker): disentangles speaker from linguistic content; multilingual content extractor for cross-language conversion — so-vits SoftVC-class SVC, not score-lock SVS. | · |
| FreeVC: Towards High-Quality Text-Free One-Shot Voice Conversion | Li, Tu, Xiao · 2022 | Text-free one-shot VC: extract clean content from WavLM (information bottleneck) without text annotation, then reconstruct waveform with target speaker — STS/wav→wav content path, no new text mint. | · |
| LDM-SVC: Latent Diffusion Model Based Zero-Shot Any-to-Any Singing Voice Conversion with Singer Guidance | Chen, Gu, Zhang, Li · 2024 | Any-to-any SVC pretrained on open-source So-VITS-SVC (VITS); latent diffusion + singer guidance to suppress source timbre leakage while converting — So-VITS-SVC stack, not MIDI-locked SVS. | · |
| NNSVS: A Neural Network-Based Singing Voice Synthesis Toolkit | Yamamoto, Yoneyama, Toda · 2022 | Reports DiffSinger-style retrain yielding discontinuous F0 and unstable vibrato when spectrum is overweighted vs F0 — acoustic-path failure under score-conditioned SVS | · |
| Singing voice synthesis based on frame-level sequence-to-sequence models considering vocal timing deviation | Nishihara, Hono, Hashimoto et al. · 2023 | SVS quality collapses when phoneme-boundary alignments from external aligners err; models vocal timing deviation explicitly — alignment/timing failure mode under score conditioning | · |
| Sinsy: A Deep Neural Network-Based Singing Voice Synthesis System | Hono, Hashimoto, Oura et al. · 2021 | Without pitch-normalization to the score, F0-RMSE jumps ~74→264 cents; time-lag puts consonants before notated onset — classic score-lock failure modes under MIDI+lyrics | · |
| SongEcho: Towards Cover Song Generation via Instance-Adaptive Element-wise Linear Modulation | Li, Li, Wang, Zhang et al. · 2026 | Cover song generation: simultaneously generate new vocals and accompaniment conditioned on the original vocal melody and text prompts — melody from source performance, not score-lock MIDI+lyrics SVS. | · |
| UniVoice: A Unified Model for Speech and Singing Voice Generation | Zheng, Xue, Ren et al. · 2026 | Naïve shared melody conditioning causes gradient conflict (elevated speech/singing PER) vs factorized paths — failure mode when one model blurs speech and score-locked singing | · |
| VISinger 2: High-Fidelity End-to-End Singing Voice Synthesis Enhanced by Digital Signal Processing Techniques | Zhang, Xue, Li et al. · 2022 | Predicted F0 drives a DDSP harmonic oscillator as hard pitch constraint; removing DSP path yields spectral discontinuities / glitches — failure mode when pitch is soft | · |
| XiaoiceSing: A High-Quality and Integrated Singing Voice Synthesis System | Lu, Wu, Luan et al. · 2020 | Residual log-F0 around MIDI note pitch vs independent F0 prediction — documents out-of-tune failure when score pitch is not residual-locked (hard constraint craft; no flip beyond ACCEPT) | · |
| YuE | Yuan, Lin, Guo et al. · 2025 | Lyrics-to-song; dual-track ICL can change lyrics while preserving accompaniment audio; MIDI is not an input. | · |

## Detail

### ACE-Step 1.5 · `load-bearing`
**Lyrics+caption → mixed song; MIT; BPM/key are metadata, not note MIDI.**
- **Implication:** Commercially licensed local song generator, not a singing instrument.
- **Identifier:** `arXiv:2602.00744`
- **Verify:** arXiv:2602.00744v3 sec 3.4: the LM emits CoT metadata 'including BPM, key, duration, and structure' in YAML; 'MIDI' appears zero times in the paper. Licence MIT on ACE-Step/Ace-Step1.5 and acestep-v15-xl-base/turbo.
- **Sources:** [ACE-Step 1.5](https://arxiv.org/abs/2602.00744)

### CoMelSinger: Discrete Token-Based Zero-Shot Singing Synthesis With Structured Melody Control and Guidance · `load-bearing`
**Zero-shot SVS with lyric + pitch tokens under MaskGCT; contrastive anti-prosody-leakage hardens score-lock beyond STUDY-011 MIDI+lyrics.**
- **Implication:** Deepen score-lock axis; structured melody control.
- **Identifier:** `arXiv:2509.19883`
- **Verify:** arXiv:2509.19883v2 abstract: MaskGCT backbone, text replaced by lyric+pitch tokens, coarse-to-fine contrastive learning regularizing pitch leakage from the timbre prompt. Authors/year exact. Danny-NUS/CoMelSinger has NO licence.
- **Sources:** [CoMelSinger: Discrete Token-Based Zero-Shot Singing Synthesis With Structured Melody Control and Guidance](https://arxiv.org/abs/2509.19883)

### DiTSinger: Scaling Singing Voice Synthesis with Diffusion Transformer and Implicit Alignment · `load-bearing`
**DiT SVS conditioned on pitch, phonemes, word durations, slur; still score-bound (implicit alignment does not drop MIDI).**
- **Implication:** Implicit alignment stays score-bound; not a free song generator.
- **Identifier:** `arXiv:2510.09016`
- **Verify:** arXiv:2510.09016v2 sec 2.3 verbatim: 'Fine-grained inputs - pitch p, phonemes ph, word durations w, and slur indicators sl'. Implicit alignment drops only phoneme-level duration labels; pitch conditioning stays.
- **Sources:** [DiTSinger: Scaling Singing Voice Synthesis with Diffusion Transformer and Implicit Alignment](https://arxiv.org/abs/2510.09016)

### DiffRhythm 2 · `load-bearing`
**Paper states SVS produces vocals with predefined melodies; song generation does not; Apache 2.0 v2 weights.**
- **Implication:** Cannot honor MIDI; v1 VAE is NC-capped.
- **Identifier:** `arXiv:2510.22950`
- **Verify:** Paper intro verbatim: 'Unlike singing voice synthesis, which produces vocals with predefined melodies...'. ASLP-lab/DiffRhythm2 weights Apache-2.0. v1 DiffRhythm-vae = Stability AI Community Licence, commercial only under $1M revenue.
- **Sources:** [DiffRhythm 2](https://arxiv.org/abs/2510.22950)

### DiffSinger · `load-bearing`
**DiffSinger is score-conditioned SVS (lyrics+pitch+duration → mel); MIDI-B path in official repo; code MIT / OpenVPI Apache 2.0; RTF 0.191.**
- **Implication:** This family can take MIDI as an acoustic condition; render is offline.
- **Identifier:** `arXiv:2105.02446`
- **Verify:** All four parts hold: score-conditioned mel (abstract); MIDI-B in the official repo changelog; MoonInTheRiver MIT + openvpi Apache-2.0 via GitHub API; paper text 'RTF 0.191 vs. 0.348' verbatim.
- **Sources:** [DiffSinger](https://arxiv.org/abs/2105.02446)

### DiffSinger ConfigurationSchemas · `load-bearing`
**Variance pitch defaults predict_pitch + use_melody_encoder; midi_smooth_width smooths MIDI step→base pitch — MIDI is the prior.**
- **Implication:** MIDI sequence as hard pitch prior.
- **Identifier:** `github:DiffSinger.ConfigurationSchemas`
- **Verify:** Doc plus shipped configs/variance.yaml: predict_pitch true, use_melody_encoder true, midi_smooth_width 0.06. Doc text: smoothing kernel 'on the step function representing MIDI sequence for base pitch calculation'.
- **Sources:** [DiffSinger ConfigurationSchemas](https://github.com/openvpi/DiffSinger/blob/main/docs/ConfigurationSchemas.md)

### DiffSinger README · `load-bearing`
**Fork positioned as SVS production tooling (OpenUtau/DiffScope); variance controllability on score-driven synthesis.**
- **Implication:** Community editor lock, not free song gen.
- **Identifier:** `github:openvpi/DiffSinger`
- **Verify:** openvpi/DiffSinger README read live 2026-09: 'Deployment & production: OpenUTAU, DiffScope (under development)'; 'variance models and parameters for prediction and control of pitch, energy, breathiness'. Apache-2.0.
- **Sources:** [DiffSinger README](https://github.com/openvpi/DiffSinger)

### LeVo: High-Quality Song Generation with Multi-Preference Alignment · `load-bearing`
**Lyrics (+ optional text descriptions and optional audio prompts) -> mixed song; song-section structure labels (verse/chorus, auto-extracted with All-In-One) plus open-vocabulary tags, with no note-level MIDI lock (MIDI is never mentioned in the paper). BPM is NOT a stated conditioning label. Availability today: the official repo github.com/tencent-ailab/songgeneration returns 404 and huggingface.co/tencent/SongGeneration returns 401; only unlicensed third-party mirrors remain.**
- **Implication:** Generator off score-lock ACCEPT lane.
- **Identifier:** `arXiv:2506.07520`
- **Verify:** Verbatim 'based on lyrics, optional text descriptions, and optional audio prompts'; verse/chorus structure via All-In-One; MIDI zero mentions. But BPM appears ZERO times, and tencent-ailab/songgeneration is 404 today.
- **Sources:** [LeVo: High-Quality Song Generation with Multi-Preference Alignment](https://arxiv.org/abs/2506.07520)

### MPEcho: A Melody and Phoneme-Aware Generative Framework for Controllable Cover Song Generation · `load-bearing`
**Cover CSG conditioned on melody and phonemes; still ≠ MIDI+lyrics score-lock SVS.**
- **Implication:** Melody/phoneme cover pole off ACCEPT score-lock lane.
- **Identifier:** `arXiv:2607.26698`
- **Verify:** arXiv:2607.26698 abstract: SongEcho conditions on F0 + V/UV tags; MPEcho adds a phoneme encoder and length regulator. Melody+phoneme, not MIDI+lyrics score. Lee, Yeh, Hu, Tan, Tsai & Yang 2026 exact.
- **Sources:** [MPEcho: A Melody and Phoneme-Aware Generative Framework for Controllable Cover Song Generation](https://arxiv.org/abs/2607.26698)

### NNSVS · `load-bearing`
**NNSVS+WORLD hard-locks phone durations to note length (post-processing normalises phone durations so their sum equals the note duration); MIT + WORLD modified-BSD; MOS 3.86 vs recordings 4.39. No RTF or real-time figure is reported in arXiv:2210.15987 - drop the real-time claim or source it elsewhere. Repo dormant since 2023-10.**
- **Implication:** Source-filter SVS is the only local real-time score-locked path with permissive licenses.
- **Identifier:** `arXiv:2210.15987`
- **Verify:** Confirmed: 'sum of the predicted durations equals to the note durations'; MOS 3.86 vs recordings 4.39; NNSVS MIT + WORLD 'modified-BSD'. But 'RTF'/'real-time factor' appears ZERO times in the paper or the README.
- **Sources:** [NNSVS](https://arxiv.org/abs/2210.15987)

### OpenUtau MidiWriter.cs · `load-bearing`
**MIDI import builds UNote from NoteNumber/Time/Length and attaches LyricEvent; pitch×time×lyric co-enforced.**
- **Implication:** Hard MIDI+lyric project objects.
- **Identifier:** `github:openutau/OpenUtau - OpenUtau.Core/Format/MidiWriter.cs`
- **Verify:** Code read: OpenUtau.Core/Format/MidiWriter.cs calls CreateNote(midiNote.NoteNumber, Time, Length) then sets note.lyric from LyricEvent. Repo has MOVED to openutau/OpenUtau (MIT); stakira/OpenUtau redirects.
- **Sources:** [OpenUtau MidiWriter.cs](https://raw.githubusercontent.com/stakira/OpenUtau/master/OpenUtau.Core/Format/MidiWriter.cs)

### SemBridge: Semantic Token Anchoring for Continuous-Latent Autoregressive Speech Generation · `load-bearing`
**Score-conditioned SVS with lyrics plus score-derived pitch and duration under semantic anchoring.**
- **Implication:** Semantic anchoring under explicit musical constraints.
- **Identifier:** `arXiv:2608.07462`
- **Verify:** arXiv:2608.07462 verbatim: 'score-conditioned SVS additionally incorporates lyrics and score-derived pitch and duration', evaluated 'under explicit musical constraints'. Six-author prefix matches exactly.
- **Sources:** [SemBridge: Semantic Token Anchoring for Continuous-Latent Autoregressive Speech Generation](https://arxiv.org/abs/2608.07462)

### SmoothSinger: A Conditional Diffusion Model for Singing Voice Synthesis with Multi-Resolution Architecture · `load-bearing`
**Conditional diffusion SVS from musical scores requiring precise pitch, duration, articulation — score-bound, not mixed-song gen.**
- **Implication:** Score-conditioned diffusion on lock pole.
- **Identifier:** `arXiv:2506.21478`
- **Verify:** arXiv:2506.21478 abstract is near-verbatim: SVS 'aims to generate expressive and high-quality vocals from musical scores, requiring precise modeling of pitch, duration, and articulation'. Sui, Xiang & Jin 2025 exact.
- **Sources:** [SmoothSinger: A Conditional Diffusion Model for Singing Voice Synthesis with Multi-Resolution Architecture](https://arxiv.org/abs/2506.21478)

### SongEcho: Towards Cover Song Generation via Instance-Adaptive Element-wise Linear Modulation · `load-bearing`
**Cover-song generation synthesizes vocals+accompaniment; contrasts with SVS/SVC single-track score-controlled vocals.**
- **Implication:** Cover pole ≠ MIDI+lyric instrument.
- **Identifier:** `arXiv:2602.19976`
- **Verify:** arXiv:2602.19976 abstract: 'simultaneously generates new vocals and accompaniment conditioned on the original vocal melody and text prompts'. Authors Li, Li, Wang, Zhang, Wu, Deussen exact; 2026.
- **Sources:** [SongEcho: Towards Cover Song Generation via Instance-Adaptive Element-wise Linear Modulation](https://arxiv.org/abs/2602.19976)

### SongGen: A Single Stage Auto-regressive Transformer for Text-to-Song Generation · `load-bearing`
**Single-stage text-to-song (lyrics + descriptions ± voice clip); no MIDI note hard constraint.**
- **Implication:** Generator without note MIDI lock.
- **Identifier:** `arXiv:2502.13128`
- **Verify:** arXiv:2502.13128v2 abstract: lyrics + text descriptions of instrumentation/genre/mood/timbre + optional 3s reference clip for voice cloning; mixed and dual-track modes. No MIDI. Repo LiuZH-19/SongGen Apache-2.0.
- **Sources:** [SongGen: A Single Stage Auto-regressive Transformer for Text-to-Song Generation](https://arxiv.org/abs/2502.13128)

### SoulX-Singer: Towards High-Quality Zero-Shot Singing Voice Synthesis · `load-bearing`
**Score-control mode takes MIDI + lyrics only; MIDI timing constraints lower WER vs melody-only F0 mode under lyric rewrite.**
- **Implication:** Score-native MIDI+lyrics path; deepen wave-03 score-lock axis.
- **Identifier:** `arXiv:2602.07803`
- **Verify:** arXiv:2602.07803v2 sec 3.3.1: 'driven by discrete MIDI notes (score-control mode), SoulX-Singer attains the lowest WER... MIDI-based timing constraints help stabilize pronunciation'; editing = rewritten lyrics. Weights Apache-2.0.
- **Sources:** [SoulX-Singer: Towards High-Quality Zero-Shot Singing Voice Synthesis](https://arxiv.org/abs/2602.07803)

### StyleSinger · `load-bearing`
**Notes+lyrics SVS plus reference clip; trained on M4Singer under CC BY-NC-SA 4.0. The paper's Ethics Statement promises restrictions on code and models, but that never happened - code and checkpoints were released in 2024.05 under MIT and remain public and ungated. The commercial blocker is the CC-BY-NC-SA-4.0 training data, not an author-imposed restriction.**
- **Implication:** Published neural-SVS data/weights are not commercial-safe for a public npm tool.
- **Identifier:** `arXiv:2312.10741`
- **Verify:** Paper verbatim: M4Singer 'used under license CC BY-NC-SA 4.0' and Ethics 'we will impose restrictions on our code and models'. But today code+ckpts are public and MIT (HF AaronZ345/StyleSinger, ungated). The NC risk is the data.
- **Sources:** [StyleSinger](https://arxiv.org/abs/2312.10741)

### TCSinger 2: Customizable Multilingual Zero-shot Singing Voice Synthesis · `load-bearing`
**Multilingual zero-shot SVS that still takes lyrics plus music notation extracted from the score - not a lyrics-to-song foundation model. It is NOT dependent on phoneme/note boundary structure: the Blurred Boundary Content encoder is the paper's stated contribution for removing reliance on phoneme and note boundary annotations, predicting duration itself and masking boundaries. Code AaronZ345/TCSinger2 is MIT.**
- **Implication:** Phoneme/note SVS lane; not generator.
- **Identifier:** `arXiv:2505.14910`
- **Verify:** Paper: 'C includes the lyrics l and music notation n extracted from the music scores' - so 'not a lyrics-to-song model' is right. But the BBC Encoder exists precisely to REMOVE dependence on phoneme/note boundary annotations.
- **Sources:** [TCSinger 2: Customizable Multilingual Zero-shot Singing Voice Synthesis](https://arxiv.org/abs/2505.14910)

### VISinger 2 · `load-bearing`
**Predicted F0 drives a DDSP harmonic oscillator as a hard pitch constraint (f_k = k*f_0). Official Opencpop pre-trained weights ARE published from the author's own repo, but zhangyongmao/VISinger2 carries no LICENSE file at all - all rights reserved, so the weights are not commercially usable.**
- **Implication:** Hybrid DSP+neural SVS can keep F0 hard-constrained.
- **Identifier:** `arXiv:2211.02903`
- **Verify:** F0 lock holds: f_k(n)=k*f_0(n) feeds the DDSP harmonic oscillator. But official weights DO exist - the author's own repo links an Opencpop pre-trained model. Decisive instead: zhangyongmao/VISinger2 has NO licence file.
- **Sources:** [VISinger 2](https://arxiv.org/abs/2211.02903)

### YingMusic-Singer: Zero-shot Singing Voice Synthesis and Editing with Annotation-free Melody Guidance · `load-bearing`
**Melody-driven SVS without phoneme-level duration/pitch annotation; soft annotation vs hard MIDI — still not free lyrics-to-song.**
- **Implication:** Soft vs hard melody conditioning on score-lock axis.
- **Identifier:** `arXiv:2512.04779`
- **Verify:** arXiv:2512.04779 abstract: melody extracted from reference AUDIO, no phoneme-level alignment, arbitrary lyrics over any reference melody. LICENCE BLOCKER: official weights GiantAILab/YingMusic-Singer are CC-BY-NC-4.0.
- **Sources:** [YingMusic-Singer: Zero-shot Singing Voice Synthesis and Editing with Annotation-free Melody Guidance](https://arxiv.org/abs/2512.04779)

### so-vits-svc 4.0 · `load-bearing`
**Converts a dry vocal into a cloned singer; F0 comes from the source recording, not MIDI; AGPL-3.0.**
- **Implication:** SVC can retimbre a DSP/MIDI-driven dry vocal; MIDI control stays upstream; AGPL is a ship-blocker for the public package.
- **Identifier:** `AGPL-3.0`
- **Verify:** README: 'the pitch and intonations of the original audio are preserved'; F0 predictors (crepe/dio/harvest/rmvpe/fcpe) all estimate from the input audio, no MIDI path. LICENCE BLOCKER AGPL-3.0; both repos now archived.
- **Sources:** [so-vits-svc 4.0](https://github.com/innnky/so-vits-svc)

### A Comparison of Discrete and Soft Speech Units for Improved Voice Conversion · `directional`
**SoftVC: transform source speech into a target voice while keeping content unchanged; soft units retain more linguistic content than discrete units (so-vits-svc SoftVC content-encoder lineage).**
- **Implication:** STUDY-043 A2A/SVC/cover deepen. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2111.02392`
- **Verify:** no external verdict — not yet swept
- **Sources:** [A Comparison of Discrete and Soft Speech Units for Improved Voice Conversion](https://arxiv.org/abs/2111.02392)

### ACE-Step 1.5: Pushing the Boundaries of Open-Source Music Generation · `directional`
**Unified editing toolkit includes cover generation, repainting, vocal-to-BGM; cover re-synthesizes timbre while retaining melodic skeletons via quantized latents — cover/repaint pole, not note-MIDI score-lock.**
- **Implication:** STUDY-043 A2A/SVC/cover deepen. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2602.00744`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ACE-Step 1.5: Pushing the Boundaries of Open-Source Music Generation](https://arxiv.org/abs/2602.00744)

### ACE-Step: A Step Towards Music Generation Foundation Model · `directional`
**Lyrics+caption → mixed song; BPM/duration size a latent canvas — free-generator pole that breaks note-level MIDI+lyrics hard lock (contrast SVS score-lock; no invent)**
- **Implication:** STUDY-041 score-lock failure deepen. Flips beyond ACCEPT: 0.
- **Identifier:** `arXiv:2506.00045`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ACE-Step: A Step Towards Music Generation Foundation Model](https://arxiv.org/abs/2506.00045)

### DiffRhythm 2: Efficient and High Fidelity Song Generation via Block Flow Matching · `directional`
**Explicit pole: unlike singing voice synthesis, which produces vocals with predefined melodies, song generation does not — free song-gen vs score/melody-predefined SVS.**
- **Implication:** STUDY-043 A2A/SVC/cover deepen. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2510.22950`
- **Verify:** no external verdict — not yet swept
- **Sources:** [DiffRhythm 2: Efficient and High Fidelity Song Generation via Block Flow Matching](https://arxiv.org/abs/2510.22950)

### DiffSVC: A Diffusion Probabilistic Model for Singing Voice Conversion · `directional`
**SVC with PPGs as content features plus fundamental-frequency and loudness features as auxiliary inputs to the denoiser — content+F0+loudness taken from the source performance, not a MIDI score.**
- **Implication:** STUDY-043 A2A/SVC/cover deepen. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2105.13871`
- **Verify:** no external verdict — not yet swept
- **Sources:** [DiffSVC: A Diffusion Probabilistic Model for Singing Voice Conversion](https://arxiv.org/abs/2105.13871)

### DiffSinger: Singing Voice Synthesis via Shallow Diffusion Mechanism · `directional`
**Diffusion acoustic model conditioned on music score (lyrics+pitch+duration → mel; MIDI-B path) — score-bound SVS pole opposite free lyrics-to-song generators**
- **Implication:** STUDY-041 score-lock failure deepen. Flips beyond ACCEPT: 0.
- **Identifier:** `arXiv:2105.02446`
- **Verify:** no external verdict — not yet swept
- **Sources:** [DiffSinger: Singing Voice Synthesis via Shallow Diffusion Mechanism](https://arxiv.org/abs/2105.02446)

### FreeSVC: Towards Zero-shot Multilingual Singing Voice Conversion · `directional`
**Zero-shot multilingual SVC (enhanced VITS + SPIN content + ECAPA2 speaker): disentangles speaker from linguistic content; multilingual content extractor for cross-language conversion — so-vits SoftVC-class SVC, not score-lock SVS.**
- **Implication:** STUDY-043 A2A/SVC/cover deepen. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2501.05586`
- **Verify:** no external verdict — not yet swept
- **Sources:** [FreeSVC: Towards Zero-shot Multilingual Singing Voice Conversion](https://arxiv.org/abs/2501.05586)

### FreeVC: Towards High-Quality Text-Free One-Shot Voice Conversion · `directional`
**Text-free one-shot VC: extract clean content from WavLM (information bottleneck) without text annotation, then reconstruct waveform with target speaker — STS/wav→wav content path, no new text mint.**
- **Implication:** STUDY-043 A2A/SVC/cover deepen. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2210.15418`
- **Verify:** no external verdict — not yet swept
- **Sources:** [FreeVC: Towards High-Quality Text-Free One-Shot Voice Conversion](https://arxiv.org/abs/2210.15418)

### LDM-SVC: Latent Diffusion Model Based Zero-Shot Any-to-Any Singing Voice Conversion with Singer Guidance · `directional`
**Any-to-any SVC pretrained on open-source So-VITS-SVC (VITS); latent diffusion + singer guidance to suppress source timbre leakage while converting — So-VITS-SVC stack, not MIDI-locked SVS.**
- **Implication:** STUDY-043 A2A/SVC/cover deepen. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2406.05325`
- **Verify:** no external verdict — not yet swept
- **Sources:** [LDM-SVC: Latent Diffusion Model Based Zero-Shot Any-to-Any Singing Voice Conversion with Singer Guidance](https://arxiv.org/abs/2406.05325)

### NNSVS: A Neural Network-Based Singing Voice Synthesis Toolkit · `directional`
**Reports DiffSinger-style retrain yielding discontinuous F0 and unstable vibrato when spectrum is overweighted vs F0 — acoustic-path failure under score-conditioned SVS**
- **Implication:** STUDY-041 score-lock failure deepen. Flips beyond ACCEPT: 0.
- **Identifier:** `arXiv:2210.15987`
- **Verify:** no external verdict — not yet swept
- **Sources:** [NNSVS: A Neural Network-Based Singing Voice Synthesis Toolkit](https://arxiv.org/abs/2210.15987)

### Singing voice synthesis based on frame-level sequence-to-sequence models considering vocal timing deviation · `directional`
**SVS quality collapses when phoneme-boundary alignments from external aligners err; models vocal timing deviation explicitly — alignment/timing failure mode under score conditioning**
- **Implication:** STUDY-041 score-lock failure deepen. Flips beyond ACCEPT: 0.
- **Identifier:** `arXiv:2301.02262`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Singing voice synthesis based on frame-level sequence-to-sequence models considering vocal timing deviation](https://arxiv.org/abs/2301.02262)

### Sinsy: A Deep Neural Network-Based Singing Voice Synthesis System · `directional`
**Without pitch-normalization to the score, F0-RMSE jumps ~74→264 cents; time-lag puts consonants before notated onset — classic score-lock failure modes under MIDI+lyrics**
- **Implication:** STUDY-041 score-lock failure deepen. Flips beyond ACCEPT: 0.
- **Identifier:** `arXiv:2108.02776`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Sinsy: A Deep Neural Network-Based Singing Voice Synthesis System](https://arxiv.org/abs/2108.02776)

### SongEcho: Towards Cover Song Generation via Instance-Adaptive Element-wise Linear Modulation · `directional`
**Cover song generation: simultaneously generate new vocals and accompaniment conditioned on the original vocal melody and text prompts — melody from source performance, not score-lock MIDI+lyrics SVS.**
- **Implication:** STUDY-043 A2A/SVC/cover deepen. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2602.19976`
- **Verify:** no external verdict — not yet swept
- **Sources:** [SongEcho: Towards Cover Song Generation via Instance-Adaptive Element-wise Linear Modulation](https://arxiv.org/abs/2602.19976)

### UniVoice: A Unified Model for Speech and Singing Voice Generation · `directional`
**Naïve shared melody conditioning causes gradient conflict (elevated speech/singing PER) vs factorized paths — failure mode when one model blurs speech and score-locked singing**
- **Implication:** STUDY-041 score-lock failure deepen. Flips beyond ACCEPT: 0.
- **Identifier:** `arXiv:2606.05852`
- **Verify:** no external verdict — not yet swept
- **Sources:** [UniVoice: A Unified Model for Speech and Singing Voice Generation](https://arxiv.org/abs/2606.05852)

### VISinger 2: High-Fidelity End-to-End Singing Voice Synthesis Enhanced by Digital Signal Processing Techniques · `directional`
**Predicted F0 drives a DDSP harmonic oscillator as hard pitch constraint; removing DSP path yields spectral discontinuities / glitches — failure mode when pitch is soft**
- **Implication:** STUDY-041 score-lock failure deepen. Flips beyond ACCEPT: 0.
- **Identifier:** `arXiv:2211.02903`
- **Verify:** no external verdict — not yet swept
- **Sources:** [VISinger 2: High-Fidelity End-to-End Singing Voice Synthesis Enhanced by Digital Signal Processing Techniques](https://arxiv.org/abs/2211.02903)

### XiaoiceSing: A High-Quality and Integrated Singing Voice Synthesis System · `directional`
**Residual log-F0 around MIDI note pitch vs independent F0 prediction — documents out-of-tune failure when score pitch is not residual-locked (hard constraint craft; no flip beyond ACCEPT)**
- **Implication:** STUDY-041 score-lock failure deepen. Flips beyond ACCEPT: 0.
- **Identifier:** `arXiv:2006.06261`
- **Verify:** no external verdict — not yet swept
- **Sources:** [XiaoiceSing: A High-Quality and Integrated Singing Voice Synthesis System](https://arxiv.org/abs/2006.06261)

### YuE · `directional`
**Lyrics-to-song; dual-track ICL can change lyrics while preserving accompaniment audio; MIDI is not an input.**
- **Implication:** Can restyle over an existing mix; cannot sing a supplied MIDI line.
- **Identifier:** `arXiv:2503.08638`
- **Verify:** no external verdict — not yet swept
- **Sources:** [YuE](https://arxiv.org/abs/2503.08638)

