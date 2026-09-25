# Singing eval and teaching HCI
_MUSHRA/MOS for singing, vocal-model identity, teaching / practice HCI_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

49 findings · 15 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| AI singing coach metacognition RCT | Li, Cui, Manoharan, Dai, Liu & Huang · 2025 | Quasi-RCT (random assignment, pre/post, two-way repeated-measures ANOVA), N=80 Chinese pre-service teachers aged 18-21 in Guizhou Province, predominantly female, over 6 weeks of weekly 1-hour vocal training. The three-part intervention was a self-recording audio-comparison tool, dialogic feedback from Tencent's Yuanbao LLM chatbot, and reflective journalling - no synthetic singer and no teacher-demonstration arm. Metacognition showed a significant group-by-time interaction (F(1,78)=5.10, p=.03); singing performance improved in both groups with no significant interaction (F(1,78)=2.38, p=.13), and metacognition did not correlate with singing performance (t=0.23, p=.82). Single-site student sample - not a general result. | ✓ |
| Classifier-free guidance (CFG) as soft conditioning | Ho & Salimans · 2022 | Ho & Salimans define classifier-free guidance as a trade-off between sample fidelity and diversity, obtained by mixing conditional and unconditional score estimates from a jointly trained model. The paper states no guarantee that the conditioning is satisfied at any guidance scale - so it cannot be cited as evidence that raising the scale enforces a MIDI+lyric lock, but it does not assert the negative either. | ✓ |
| Constraint-based jazz improvisation pedagogy | Alton Xian Rong Wong (West Virginia University, DMA thesis) · 2026 | Rhythmic/harmonic constraints as generative soft rails — partial hold after hard pitch/lyric lock. | ✓ |
| EMP Soft Constraints | GAMS · 2024 | Soft = penalty in objective; hard = feasibility — names CFG/style as soft vs note/lyric lock as hard. | ✓ |
| ITU-R BS.1534-3 MUSHRA | ITU · 2015 | The hidden reference is the listener post-screening tool: disqualify assessors who rate the hidden reference below 90 MUSHRA points on more than 15% of test items. The mandatory mid-range anchor (typically a 3.5 kHz low-pass version, alongside a 7 kHz anchor) calibrates the scale so minor artefacts are not over-penalised and results pool across labs - it is not part of the exclusion criterion. | ✓ |
| Improvisation and Teaching (adjacent pedagogy) | R. Keith Sawyer (Washington University) · 2007 | Improvisation pedagogy adjacent to score-based learning — soft rails after hard lock. | ✓ |
| Liquid Haskell Tutorial 01 Introduction | Ranjit Jhala, Eric Seidel & Niki Vazou (hosted by UCSD Progsys) · 2024 | Refinement-type intro: rejected programs fail contracts — maps to score-lock as Spec input. | ✓ |
| Liquid Haskell refinement types tutorial | Ricardo Peña (Universidad Complutense de Madrid) · 2017 | Contracts must hold or the program is rejected; soft wishes are not types — analog for MIDI+lyric hard Spec. | ✓ |
| Mix voice / muscular antagonism lexicon | Voice Science (voicescience.org) - not VoiceScienceWorks · 2026 | Per voicescience.org: chest voice is TA-led and maps to laryngeal mechanism M1, head voice is CT-led and maps to M2, and mix is an intermediate TA/CT coordination on a spectrum - explicitly a training target, not a distinct mechanism or register. This is a non-peer-reviewed pedagogy site and the framing is contested: VoiceScienceWorks.org, the organisation this entry credits, argues the opposite, citing Hull that 'there is not a moment when one muscle takes over from the other' and that most chest register and all falsetto were produced under CT dominance. | ✓ |
| Muscular antagonism lexicon | Voice Science (voicescience.org) - not VoiceScienceWorks · 2026 | TA/CT antagonism framing for mix — register as glottal coordination language. | ✓ |
| Score-based / Werktreue pedagogy (ch7) | Mariam Kharatyan (in Teaching Music Performance in Higher Education, Open Book Publishers) · 2024 | Execute the written map vs invent within style — practice-companion as score-instrument. | ✓ |
| Singing with yourself | Pfordresher & Mantell · 2014 | Across three experiments, both accurate and poor-pitch singers imitated their own recorded voice more accurately than another singer's; the self-advantage is enhanced - not exclusive - in poor-pitch singers, and persists when self-recognition, vocal timbre and absolute pitch are controlled (transposed recordings). Targets were other human singers, not a synthetic voice; per-experiment N is not stated in the abstract. | ✓ |
| Sinsy | Hono et al. · 2021 | Without pitch-normalization to the score, F0-RMSE jumps from ~74 to 264 cents. | ✓ |
| VocalRender | Chen, Wang, Mu, Yang & Chng · 2026 | Objective RPA/IOU can invert subjective score-following; VocalRender won MS-MOS 2.96 while SoulX-Singer won RPA. | ✓ |
| XiaoiceSing | Lu et al. · 2020 | Canonical SVS tests split pronunciation MOS from quality; F0 RMSE 10.45 Hz, Dur RMSE 20.55, F0 CORR 0.99. | ✓ |
| AI-assisted feedback and reflection in vocal music training: effects on metacognition and singing performance | Li, Cui, Manoharan, Dai · 2025 | AI singing-coach RCT raised metacognition, not singing scores — teaching-outcome metric split (metacognition vs performance). | · |
| Addressing Documentation Debt in Machine Learning Research: A Retrospective Datasheet for BookCorpus | Bandy, Vincent · 2021 | Documents sparsely described but widely used BookCorpus to pay down documentation debt — README/catalog honesty for legacy rows that stay verified=0 until retrieval-checked. | · |
| Croissant: A Metadata Format for ML-Ready Datasets | Akhtar, Benjelloun, Conforti, Foschini, Giner-Miguelez et al. · 2024 | Shared machine-readable dataset metadata across tools/platforms — structured documentation surface that keeps discoverable counts tied to declared fields (not silent verified invent). | · |
| Datasheets for Datasets | Gebru, Morgenstern, Vecchione, Vaughan, Wallach et al. · 2018 | Argues ML lacked a standard dataset documentation process and proposes datasheets so composition, motivation, and limits are stated explicitly — count/claim honesty over silent promotion of undated rows. | · |
| DiffSinger ConfigurationSchemas | openvpi · live | `num_valid_plots` and `val_with_vocoder` control validation audio plots during training. Developer validation knobs — not human listening-test or coaching feedback surfaces. | · |
| DiffSinger Getting Started | openvpi · live | Training eval surface is TensorBoard (`tensorboard --logdir checkpoints/`); inference is DS-file CLI. No listening-test harness, no MOS/MUSHRA UI documented. | · |
| ExpressiveSinger: Multilingual and Multi-Style Score-based Singing Voice Synthesis with Expressive Performance Control | Zhang, Huang, Li et al. · 2024 | High MOS still lacks musicality without explicit performance control of onset deviations / F0 curves — quality MOS ≠ expressive score-following outcome. | · |
| GLSL Opaque Type | Khronos OpenGL Wiki · 2024 | Opaque types cannot live in uniform blocks — analog for opaque spectral streams. Verifier: 403/timeout — leave unverified. | · |
| GLSL Uniform (named params) | Khronos OpenGL Wiki · 2024 | Named uniforms vs opaque handles analog for formant/register knobs vs opaque mgc/BAP. Verifier: Cloudflare 403 / fetch timeout — leave unverified. | · |
| ITU-R BS.1534-3 | Method for the subjective assessment of intermediate quality level of audio systems (MUSHRA) · 2015 | Hidden reference and mid-range anchors screen listeners; mis-raters of anchors are excluded — formal MUSHRA protocol for intermediate-quality audio listening tests. | · |
| ITU-R BS.1534-3 MUSHRA | ITU-R · 2015-10 | · PDF R-REC-BS.1534-3 — Method is multi-stimulus with hidden reference and anchors (mandatory low-pass anchors 3.5 kHz / mid 7 kHz). Post-screening excludes assessors who rate the hidden reference <90 on >15% of items, or the mid-range anchor >90 on >15% of items. Listening-test class surface — not an SVS product UI. | · |
| ITU-R BS.1534-3 MUSHRA | ITU · 2015 | · PDF — Analog: multi-stimulus with hidden reference + mid-range anchors; post-screen listeners who mis-rate hidden ref/mid-anchor on >15% of items. Holds for outside-SVS listening-test design. Limit: intermediate codec quality scale ≠ SingMOS lyrics/melody split alone. | · |
| Impact of Latency on Perceptual Judgments… in VR | Waltemate et al. · 2016 | · https://cg.cs.tu-dortmund.de/publications/2016-latency.pdf — Analog: motor/simultaneity degrade above ~75 ms; agency later (~125 ms). Holds for practice-companion lyric/score feedback latency. Limit: VR full-body visual delay ≠ phoneme-boundary / MFA error. | · |
| Model Cards for Model Reporting | Mitchell, Wu, Zaldivar, Barnes, Vasserman et al. · 2018 | Recommends model cards that clarify intended uses and discourage use outside well-suited contexts — supports refusing invented verified=1 flips beyond ACCEPT 23/30/50. | · |
| Navigating Dataset Documentations in AI: A Large-Scale Analysis of Dataset Cards on Hugging Face | Yang, Liang, Zou · 2024 | Empirical audit of Hugging Face dataset cards for completeness/transparency gaps — catalog counts must match what cards actually document, not aspirational verified totals. | · |
| OpenUtau README | stakira · live | Practice/editor surface: MIDI editor, vibrato editor, pre-rendering playback, DiffSinger/ENUNU support, expressions replace UTAU flags. Absent on page: MUSHRA/MOS scoring UI, SingMOS integration, teaching metacognition feedback. | · |
| OpenUtau `USTx.cs` default expressions | stakira · live | Editor exposes gender/breathiness/tension/voicing curves for tuning. Tuning knobs present; eval-harness / coaching-score knobs absent. | · |
| Progressive Disclosure | Nielsen / NN/g · 2006 | Analog: defer advanced/rarely used controls to a secondary surface; primary shows only frequent, non-confusing options. Holds for SVS teaching UIs — expose register/formant only when the engine has them; hide false enums. Limit: print-dialog HCI ≠ singing pedagogy content. | · |
| Progressive disclosure of named cockpit controls | LogRocket / enterprise UX · 2024 | Expose register/formant when the engine has them; hide false enums — HCI analog for not inventing register menus on DiffSinger/OpenUtau/WORLD. | · |
| SingMOS README | South-Twilight · live (v1.1.2) | `torch.hub` loaders `singmos_pro` / `singmos_v1` predict singing MOS from 16 kHz waveforms; example returns Pred MOS (batch tensor). Automatic SQA tooling — no MUSHRA panel, no coaching feedback UI, no register/formant knobs on the page. | · |
| SingMOS-Pro | Tang et al. · 2026 | Lyrics MOS, Melody MOS, and overall are separately rated; UTMOS/DNSMOS correlate poorly with singing. | · |
| SingMOS-Pro dataset card | TangRain / HF · 2025-10 | 7,981 clips; `score.json` system/utterance MOS + judges; `metadata.csv` documents `judge_score` and optional `judge_lyrics_score` / `judge_melody_score` columns (may be empty). Annotation/eval dataset surface, not a practice app. | · |
| SingMOS-Pro: An Comprehensive Benchmark for Singing Quality Assessment | Tang, Liu, Feng et al. · 2025 | Multilingual SQA benchmark with separate Lyrics MOS (pronunciation/intelligibility), Melody MOS, and Overall MOS — explicit MOS-dimension split for quality vs lyric clarity. | · |
| SingMOS: An extensive Open-Source Singing Voice Dataset for MOS Prediction | Tang, Shi, Wu et al. · 2024 | First open singing MOS dataset (SVS/SVC/resynthesis clips) for automatic singing-quality prediction — SingMOS-class evaluator literature (not a flip). | · |
| Singing with yourself | Pfordresher & Mantell · 2014 | · http://www.acsu.buffalo.edu/~pqp/pdfs/Pfordresher&Mantell_2014_CogPsy.pdf — Analog: poor-pitch singers match self recordings far better than other voices. Holds for self-vs-other pitch-matching pedagogy (perfect other/synth is the hard tutor). Limit: imitation psychology ≠ SVS MOS admission harness. | · |
| The Data Provenance Initiative: A Large Scale Audit of Dataset Licensing & Attribution in AI | Longpre, Mahari, Chen, Obeng-Marnu, Sileo et al. · 2023 | Multi-disciplinary audit of licensing/attribution under inconsistent documentation — provenance honesty for catalog sources without inventing nodes or flips. | · |
| The Open-Box Fallacy: Why AI Deployment Needs a Calibrated Verification Regime | Konrad, Adam, Merrild, Terrenzi, De Rosa et al. · 2026 | Argues deployment needs a calibrated verification regime rather than overclaiming openness/explainability as proof — analog for default-unverified rows and flips only on ACCEPT 23/30/50. | · |
| The State of Documentation Practices of Third-party Machine Learning Models and Datasets | Lang Oreamuno, Khan, Bangash, Stinson, Adams · 2023 | Finds model/dataset stores often lack the detailed specs model/dataset cards imply — supports keeping README 175 · 12/175 honest rather than inventing verified mass-flips. | · |
| The VoiceMOS Challenge 2023: Zero-shot Subjective Speech Quality Prediction for Multiple Domains | Cooper, Huang, Tsao et al. · 2023 | Challenge framing for automatic prediction of subjective MOS across domains — parent eval class later extended by singing-track MOS datasets (SingMOS lineage). | · |
| The effect of vocal modeling on pitch-matching accuracy of elementary schoolchildren | Green · 1990 | Vocal-model identity changes pitch-matching accuracy: child > adult female > adult male. | · |
| UTMOS: UTokyo-SaruLab System for VoiceMOS Challenge 2022 | Saeki, Xin, Nakata et al. · 2022 | Strong automatic MOS predictor (UTMOS) widely reused as speech/singing SQA baseline — automatic MOS-prediction engine class vs human MOS panels. | · |
| Vocal Registers? (TA/CT antagonism lexicon) | Voice Science Works · live | Analog: chest/head/mix as muscular coordination language, not a simple F0 switch. Holds-with-limit for pedagogy register wording (STUDY-022 item 9). Limit: does not license inventing chest/mix/head menus on DiffSinger/OpenUtau/WORLD. | · |
| VocalRender: Score-Native Singing Voice Synthesis for Real-World Composition | Chen, Wang, Mu et al. · 2026 | VocalRender wins MS-MOS (~2.96) on reported subjective score-following panel — MS-MOS figure only this land; RPA/IOU objective/subjective invert clause stays unverified. | · |
| vocal-synth-engine README | mcp-tool-shop-org · live | Cockpit SPA: piano roll, live keyboard, XY pad (timbre×breathiness), latency presets, render bank + telemetry (peak/RTF/jitter). Practice/instrument UI documented; no MUSHRA, no SingMOS, no named singing-coach score panel. | · |

## Detail

### AI singing coach metacognition RCT · `load-bearing`
**Quasi-RCT (random assignment, pre/post, two-way repeated-measures ANOVA), N=80 Chinese pre-service teachers aged 18-21 in Guizhou Province, predominantly female, over 6 weeks of weekly 1-hour vocal training. The three-part intervention was a self-recording audio-comparison tool, dialogic feedback from Tencent's Yuanbao LLM chatbot, and reflective journalling - no synthetic singer and no teacher-demonstration arm. Metacognition showed a significant group-by-time interaction (F(1,78)=5.10, p=.03); singing performance improved in both groups with no significant interaction (F(1,78)=2.38, p=.13), and metacognition did not correlate with singing performance (t=0.23, p=.82). Single-site student sample - not a general result.**
- **Implication:** Coaching-layer evidence does not license a model-as-singer.
- **Identifier:** `DOI:10.3389/fpsyg.2025.1598867`
- **Verify:** DOI resolves (Li, Cui, Manoharan, Dai, Liu, Huang; Front Psychol 2025). N=80 (38 exp / 42 ctrl), pre-service teachers aged 18-21, Guizhou China, 6 weeks. Metacognition F(1,78)=5.10 p=.03; singing F(1,78)=2.38 p=.13, not significant.
- **Sources:** [AI singing coach metacognition RCT](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12400964/)

### Classifier-free guidance (CFG) as soft conditioning · `load-bearing`
**Ho & Salimans define classifier-free guidance as a trade-off between sample fidelity and diversity, obtained by mixing conditional and unconditional score estimates from a jointly trained model. The paper states no guarantee that the conditioning is satisfied at any guidance scale - so it cannot be cited as evidence that raising the scale enforces a MIDI+lyric lock, but it does not assert the negative either.**
- **Implication:** Flag CFG-as-lock fail-transfer; leave unverified as lock.
- **Identifier:** `arXiv:2207.12598`
- **Verify:** arXiv 2207.12598 'Classifier-Free Diffusion Guidance', Ho & Salimans 2022 - exact match. Paper frames guidance as a fidelity/diversity trade-off and makes no claim about guaranteeing the condition; 'never guarantees' is inference.
- **Sources:** [Classifier-free guidance (CFG) as soft conditioning](https://arxiv.org/abs/2207.12598)

### Constraint-based jazz improvisation pedagogy · `load-bearing`
**Rhythmic/harmonic constraints as generative soft rails — partial hold after hard pitch/lyric lock.**
- **Implication:** Jazz soft-after-hard hold-with-limit.
- **Identifier:** `doi:10.33915/etd.13302`
- **Verify:** doi 10.33915/etd.13302 = 'A Constraint-Based Approach to Developing Melodic Improvisational Skills in Intermediate Jazz Piano Students', Alton Xian Rong Wong, WVU DMA 2026. Constraints-as-generative-tools claim holds. Unrefereed thesis.
- **Sources:** [Constraint-based jazz improvisation pedagogy](https://doi.org/10.33915/etd.13302)

### EMP Soft Constraints · `load-bearing`
**Soft = penalty in objective; hard = feasibility — names CFG/style as soft vs note/lyric lock as hard.**
- **Implication:** Soft vs hard formulation hold-with-limit.
- **Identifier:** `gams:EMP_SoftConstraints`
- **Verify:** GAMS EMP 'Soft Constraints' doc, verbatim: 'constraints that are allowed to be violated are called soft constraints and the constraints that continue to hold are called hard constraints', penalty in objective. Living doc, no fixed year.
- **Sources:** [EMP Soft Constraints](https://www.gams.com/latest/docs/UG_EMP_SoftConstraints.html)

### ITU-R BS.1534-3 MUSHRA · `load-bearing`
**The hidden reference is the listener post-screening tool: disqualify assessors who rate the hidden reference below 90 MUSHRA points on more than 15% of test items. The mandatory mid-range anchor (typically a 3.5 kHz low-pass version, alongside a 7 kHz anchor) calibrates the scale so minor artefacts are not over-penalised and results pool across labs - it is not part of the exclusion criterion.**
- **Implication:** Reuse the composition-panel discrimination floor; do not invent a speech-MOS gate.
- **Identifier:** `ITU-R BS.1534-3`
- **Verify:** BS.1534-3 (2015) title/edition confirmed at ITU; full text paywalled. Exclusion applies to the HIDDEN REFERENCE only - rated below 90 MUSHRA points on >15% of items. Anchors calibrate the scale across labs; not a screening rule.
- **Sources:** [ITU-R BS.1534-3 MUSHRA](https://www.itu.int/rec/R-REC-BS.1534)

### Improvisation and Teaching (adjacent pedagogy) · `load-bearing`
**Improvisation pedagogy adjacent to score-based learning — soft rails after hard lock.**
- **Implication:** Pedagogy adjacent hold-with-limit.
- **Identifier:** `criticalimprov:380`
- **Verify:** criticalimprov.com article 380 = 'Improvisation and Teaching' by Keith Sawyer (Washington University), Critical Studies in Improvisation Vol 3 No 2, 2007 - not 2020, and the journal is not the author. Short 'Notes and Opinions' piece.
- **Sources:** [Improvisation and Teaching (adjacent pedagogy)](https://www.criticalimprov.com/index.php/csieci/article/view/380)

### Liquid Haskell Tutorial 01 Introduction · `load-bearing`
**Refinement-type intro: rejected programs fail contracts — maps to score-lock as Spec input.**
- **Implication:** Hard-contract pedagogy for SVS inputs.
- **Identifier:** `liquidhaskell-tutorial`
- **Verify:** ucsd-progsys.github.io/liquidhaskell-tutorial Ch.1 loads: 'The refinement type system guarantees at compile-time that functions adhere to their contracts.' Authors are Jhala, Seidel & Vazou; UCSD Progsys is the host org, not the author.
- **Sources:** [Liquid Haskell Tutorial 01 Introduction](https://ucsd-progsys.github.io/liquidhaskell-tutorial/Tutorial_01_Introduction.html)

### Liquid Haskell refinement types tutorial · `load-bearing`
**Contracts must hold or the program is rejected; soft wishes are not types — analog for MIDI+lyric hard Spec.**
- **Implication:** Hard refinement analog hold-with-limit.
- **Identifier:** `arXiv:1701.03320`
- **Verify:** arXiv:1701.03320 resolves to 'An Introduction to Liquid Haskell' by Ricardo Peña (Universidad Complutense de Madrid), 2017 - not Vazou et al. / UCSD. It is a genuine Liquid Haskell tutorial, so the contract-or-rejection substance stands.
- **Sources:** [Liquid Haskell refinement types tutorial](https://arxiv.org/abs/1701.03320)

### Mix voice / muscular antagonism lexicon · `load-bearing`
**Per voicescience.org: chest voice is TA-led and maps to laryngeal mechanism M1, head voice is CT-led and maps to M2, and mix is an intermediate TA/CT coordination on a spectrum - explicitly a training target, not a distinct mechanism or register. This is a non-peer-reviewed pedagogy site and the framing is contested: VoiceScienceWorks.org, the organisation this entry credits, argues the opposite, citing Hull that 'there is not a moment when one muscle takes over from the other' and that most chest register and all falsetto were produced under CT dominance.**
- **Implication:** Pedagogy hold-with-limit; not DiffSinger tension scalar.
- **Identifier:** `voicescience:mix-voice`
- **Verify:** Content is on voicescience.org/lexicon/mixed-voice ('chest voice is what happens when TA leads'; mix = intermediate TA/CT, 'not a distinct laryngeal mechanism or register'), mod 2026-03-31. NOT VoiceScienceWorks, which rejects this model.
- **Sources:** [Mix voice / muscular antagonism lexicon](https://www.voicescience.org/articles/mix-voice/)

### Muscular antagonism lexicon · `load-bearing`
**TA/CT antagonism framing for mix — register as glottal coordination language.**
- **Implication:** Pedagogy hold-with-limit.
- **Identifier:** `voicescience:muscular-antagonism`
- **Verify:** voicescience.org/lexicon/muscular-antagonism (mod 2026-05-05): 'high TA relative to CT produces...the M1 / chest-voice configuration'; CT-dominant gives M2/head. Site is Voice Science, not VoiceScienceWorks. Non-peer-reviewed pedagogy page.
- **Sources:** [Muscular antagonism lexicon](https://www.voicescience.org/lexicon/muscular-antagonism/)

### Score-based / Werktreue pedagogy (ch7) · `load-bearing`
**Execute the written map vs invent within style — practice-companion as score-instrument.**
- **Implication:** Werktreue analog hold-with-limit.
- **Identifier:** `obp:0398/ch7`
- **Verify:** obp.0398 ch7 = 'Score-Based Learning and Improvisation in Classical Music Performance', Mariam Kharatyan, in Teaching Music Performance in Higher Education (Open Book Publishers, May 2024). OBP is the publisher, not the author.
- **Sources:** [Score-based / Werktreue pedagogy (ch7)](https://books.openbookpublishers.com/10.11647/obp.0398/ch7.xhtml)

### Singing with yourself · `load-bearing`
**Across three experiments, both accurate and poor-pitch singers imitated their own recorded voice more accurately than another singer's; the self-advantage is enhanced - not exclusive - in poor-pitch singers, and persists when self-recognition, vocal timbre and absolute pitch are controlled (transposed recordings). Targets were other human singers, not a synthetic voice; per-experiment N is not stated in the abstract.**
- **Implication:** A high-MOS synth of a different identity is a worse pitch-matching model than the learner's own voice.
- **Identifier:** `DOI:10.1016/j.cogpsych.2013.12.005`
- **Verify:** Europe PMC: Pfordresher & Mantell, Cognit Psychol 70:31-57, 2014, PMID 24480454. Across 3 experiments BOTH accurate and poor-pitch singers imitated self-recordings better; advantage larger, not exclusive, in poor-pitch. N not in abstract.
- **Sources:** [Singing with yourself](https://doi.org/10.1016/j.cogpsych.2013.12.005)

### Sinsy · `load-bearing`
**Without pitch-normalization to the score, F0-RMSE jumps from ~74 to 264 cents.**
- **Implication:** Score-relative F0 error in cents is the pitch admission metric.
- **Identifier:** `arXiv:2108.02776`
- **Verify:** arXiv 2108.02776 (Hono, Hashimoto, Oura, Nankaku, Tokuda 2021) Table II: F0-RMSE 74.00 cents with pitch normalisation vs 264.07 cents without. Authors conclude normalisation is 'essential in modeling the pitches of singing voices'.
- **Sources:** [Sinsy](https://arxiv.org/abs/2108.02776)

### VocalRender · `load-bearing`
**Objective RPA/IOU can invert subjective score-following; VocalRender won MS-MOS 2.96 while SoulX-Singer won RPA.**
- **Implication:** Do not admit a vocal on RPA/MCD alone; CMOS vs a human hidden reference is the perceptual check.
- **Identifier:** `arXiv:2607.27768`
- **Verify:** arXiv:2607.27768 (30 Jul 2026) resolves and authors match exactly. Table 2 MS-MOS: VocalRender 2.96 (top), SoulX-Singer 2.84. Table 1: SoulX wins RPA 0.77/0.70 vs 0.72/0.63, and IoU too. Unrefereed preprint; MS-MOS = music-score MOS.
- **Sources:** [VocalRender](https://arxiv.org/abs/2607.27768)

### XiaoiceSing · `load-bearing`
**Canonical SVS tests split pronunciation MOS from quality; F0 RMSE 10.45 Hz, Dur RMSE 20.55, F0 CORR 0.99.**
- **Implication:** A single naturalness MOS hides off-key or unintelligible singing.
- **Identifier:** `arXiv:2006.06261`
- **Verify:** arXiv 2006.06261 (Lu, Wu, Luan, Tan, Zhou 2020) Table 2: F0 RMSE 10.45 Hz, Dur RMSE 20.55, F0 CORR 0.99 vs baseline 13.74 / 24.39 / 0.91. Abstract splits MOS into sound quality, pronunciation accuracy and naturalness, as claimed.
- **Sources:** [XiaoiceSing](https://arxiv.org/abs/2006.06261)

### AI-assisted feedback and reflection in vocal music training: effects on metacognition and singing performance · `directional`
**AI singing-coach RCT raised metacognition, not singing scores — teaching-outcome metric split (metacognition vs performance).**
- **Implication:** STUDY-042 eval deepen. Flips beyond ACCEPT 23/30/50: 0.
- **Identifier:** `DOI:10.3389/fpsyg.2025.1598867`
- **Verify:** no external verdict — not yet swept
- **Sources:** [AI-assisted feedback and reflection in vocal music training: effects on metacognition and singing performance](https://doi.org/10.3389/fpsyg.2025.1598867)

### Addressing Documentation Debt in Machine Learning Research: A Retrospective Datasheet for BookCorpus · `directional`
**Documents sparsely described but widely used BookCorpus to pay down documentation debt — README/catalog honesty for legacy rows that stay verified=0 until retrieval-checked.**
- **Implication:** STUDY-064 catalog/README honesty. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2105.05241`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Addressing Documentation Debt in Machine Learning Research: A Retrospective Datasheet for BookCorpus](https://arxiv.org/abs/2105.05241)

### Croissant: A Metadata Format for ML-Ready Datasets · `directional`
**Shared machine-readable dataset metadata across tools/platforms — structured documentation surface that keeps discoverable counts tied to declared fields (not silent verified invent).**
- **Implication:** STUDY-064 catalog/README honesty. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2403.19546`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Croissant: A Metadata Format for ML-Ready Datasets](https://arxiv.org/abs/2403.19546)

### Datasheets for Datasets · `directional`
**Argues ML lacked a standard dataset documentation process and proposes datasheets so composition, motivation, and limits are stated explicitly — count/claim honesty over silent promotion of undated rows.**
- **Implication:** STUDY-064 catalog/README honesty. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:1803.09010`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Datasheets for Datasets](https://arxiv.org/abs/1803.09010)

### DiffSinger ConfigurationSchemas · `directional`
**`num_valid_plots` and `val_with_vocoder` control validation audio plots during training. Developer validation knobs — not human listening-test or coaching feedback surfaces.**
- **Implication:** STUDY-042 practice/eval surfaces. Knobs invented: 0. Flips beyond ACCEPT: 0.
- **Identifier:** `https://raw.githubusercontent.com/openvpi/DiffSinger/main/docs/ConfigurationSchemas.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [DiffSinger ConfigurationSchemas](https://raw.githubusercontent.com/openvpi/DiffSinger/main/docs/ConfigurationSchemas.md)

### DiffSinger Getting Started · `directional`
**Training eval surface is TensorBoard (`tensorboard --logdir checkpoints/`); inference is DS-file CLI. No listening-test harness, no MOS/MUSHRA UI documented.**
- **Implication:** STUDY-042 practice/eval surfaces. Knobs invented: 0. Flips beyond ACCEPT: 0.
- **Identifier:** `https://raw.githubusercontent.com/openvpi/DiffSinger/main/docs/GettingStarted.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [DiffSinger Getting Started](https://raw.githubusercontent.com/openvpi/DiffSinger/main/docs/GettingStarted.md)

### ExpressiveSinger: Multilingual and Multi-Style Score-based Singing Voice Synthesis with Expressive Performance Control · `directional`
**High MOS still lacks musicality without explicit performance control of onset deviations / F0 curves — quality MOS ≠ expressive score-following outcome.**
- **Implication:** STUDY-042 eval deepen. Flips beyond ACCEPT 23/30/50: 0.
- **Identifier:** `DOI:10.1145/3664647.3681642`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ExpressiveSinger: Multilingual and Multi-Style Score-based Singing Voice Synthesis with Expressive Performance Control](https://doi.org/10.1145/3664647.3681642)

### GLSL Opaque Type · `directional`
**Opaque types cannot live in uniform blocks — analog for opaque spectral streams. Verifier: 403/timeout — leave unverified.**
- **Implication:** Flag GLSL 403 unverified.
- **Identifier:** `khronos:opaque-type`
- **Verify:** khronos.org/opengl/wiki/Opaque_Type 301s to wikis.khronos.org - 403. GLSL 4.60 spec HTML and PDF at registry.khronos.org also 403; archive.org blocked. The uniform-block restriction is unverified against any Khronos source.
- **Sources:** [GLSL Opaque Type](https://www.khronos.org/opengl/wiki/Opaque_Type)

### GLSL Uniform (named params) · `directional`
**Named uniforms vs opaque handles analog for formant/register knobs vs opaque mgc/BAP. Verifier: Cloudflare 403 / fetch timeout — leave unverified.**
- **Implication:** Flag GLSL 403 unverified; do not land as verified.
- **Identifier:** `khronos:glsl-uniform`
- **Verify:** khronos.org/opengl/wiki/Uniform_(GLSL) 301s to wikis.khronos.org, which 403s; registry.khronos.org GLSL 4.60 spec and docs.gl also 403; archive.org blocked to this tool. Could not retrieve - entry's own 403 note reproduced.
- **Sources:** [GLSL Uniform (named params)](https://www.khronos.org/opengl/wiki/Uniform_(GLSL))

### ITU-R BS.1534-3 · `directional`
**Hidden reference and mid-range anchors screen listeners; mis-raters of anchors are excluded — formal MUSHRA protocol for intermediate-quality audio listening tests.**
- **Implication:** STUDY-042 eval deepen. Flips beyond ACCEPT 23/30/50: 0.
- **Identifier:** `R-REC-BS.1534-3`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ITU-R BS.1534-3](https://www.itu.int/rec/R-REC-BS.1534)

### ITU-R BS.1534-3 MUSHRA · `directional`
**· PDF R-REC-BS.1534-3 — Method is multi-stimulus with hidden reference and anchors (mandatory low-pass anchors 3.5 kHz / mid 7 kHz). Post-screening excludes assessors who rate the hidden reference <90 on >15% of items, or the mid-range anchor >90 on >15% of items. Listening-test class surface — not an SVS product UI.**
- **Implication:** STUDY-042 practice/eval surfaces. Knobs invented: 0. Flips beyond ACCEPT: 0.
- **Identifier:** `https://www.itu.int/rec/R-REC-BS.1534`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ITU-R BS.1534-3 MUSHRA](https://www.itu.int/rec/R-REC-BS.1534)

### ITU-R BS.1534-3 MUSHRA · `directional`
**· PDF — Analog: multi-stimulus with hidden reference + mid-range anchors; post-screen listeners who mis-rate hidden ref/mid-anchor on >15% of items. Holds for outside-SVS listening-test design. Limit: intermediate codec quality scale ≠ SingMOS lyrics/melody split alone.**
- **Implication:** STUDY-042 HCI/pedagogy analog hold-with-limit. Green 1990 + fail-transfers omitted. Flips beyond ACCEPT: 0.
- **Identifier:** `https://www.itu.int/rec/R-REC-BS.1534-3-201510-I`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ITU-R BS.1534-3 MUSHRA](https://www.itu.int/rec/R-REC-BS.1534-3-201510-I)

### Impact of Latency on Perceptual Judgments… in VR · `directional`
**· https://cg.cs.tu-dortmund.de/publications/2016-latency.pdf — Analog: motor/simultaneity degrade above ~75 ms; agency later (~125 ms). Holds for practice-companion lyric/score feedback latency. Limit: VR full-body visual delay ≠ phoneme-boundary / MFA error.**
- **Implication:** STUDY-042 HCI/pedagogy analog hold-with-limit. Green 1990 + fail-transfers omitted. Flips beyond ACCEPT: 0.
- **Identifier:** `https://doi.org/10.1145/2993369.2993381`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Impact of Latency on Perceptual Judgments… in VR](https://doi.org/10.1145/2993369.2993381)

### Model Cards for Model Reporting · `directional`
**Recommends model cards that clarify intended uses and discourage use outside well-suited contexts — supports refusing invented verified=1 flips beyond ACCEPT 23/30/50.**
- **Implication:** STUDY-064 catalog/README honesty. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:1810.03993`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993)

### Navigating Dataset Documentations in AI: A Large-Scale Analysis of Dataset Cards on Hugging Face · `directional`
**Empirical audit of Hugging Face dataset cards for completeness/transparency gaps — catalog counts must match what cards actually document, not aspirational verified totals.**
- **Implication:** STUDY-064 catalog/README honesty. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2401.13822`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Navigating Dataset Documentations in AI: A Large-Scale Analysis of Dataset Cards on Hugging Face](https://arxiv.org/abs/2401.13822)

### OpenUtau README · `directional`
**Practice/editor surface: MIDI editor, vibrato editor, pre-rendering playback, DiffSinger/ENUNU support, expressions replace UTAU flags. Absent on page: MUSHRA/MOS scoring UI, SingMOS integration, teaching metacognition feedback.**
- **Implication:** STUDY-042 practice/eval surfaces. Knobs invented: 0. Flips beyond ACCEPT: 0.
- **Identifier:** `https://raw.githubusercontent.com/stakira/OpenUtau/master/README.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [OpenUtau README](https://raw.githubusercontent.com/stakira/OpenUtau/master/README.md)

### OpenUtau `USTx.cs` default expressions · `directional`
**Editor exposes gender/breathiness/tension/voicing curves for tuning. Tuning knobs present; eval-harness / coaching-score knobs absent.**
- **Implication:** STUDY-042 practice/eval surfaces. Knobs invented: 0. Flips beyond ACCEPT: 0.
- **Identifier:** `https://raw.githubusercontent.com/stakira/OpenUtau/master/OpenUtau.Core/Format/USTx.cs`
- **Verify:** no external verdict — not yet swept
- **Sources:** [OpenUtau `USTx.cs` default expressions](https://raw.githubusercontent.com/stakira/OpenUtau/master/OpenUtau.Core/Format/USTx.cs)

### Progressive Disclosure · `directional`
**Analog: defer advanced/rarely used controls to a secondary surface; primary shows only frequent, non-confusing options. Holds for SVS teaching UIs — expose register/formant only when the engine has them; hide false enums. Limit: print-dialog HCI ≠ singing pedagogy content.**
- **Implication:** STUDY-042 HCI/pedagogy analog hold-with-limit. Green 1990 + fail-transfers omitted. Flips beyond ACCEPT: 0.
- **Identifier:** `https://www.nngroup.com/articles/progressive-disclosure/`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)

### Progressive disclosure of named cockpit controls · `avoid`
**Expose register/formant when the engine has them; hide false enums — HCI analog for not inventing register menus on DiffSinger/OpenUtau/WORLD.**
- **Implication:** HCI hold-with-limit.
- **Identifier:** `logrocket:progressive-disclosure`
- **Verify:** Cited slug 404s. The real LogRocket piece (Eric Chung, upd. Chinwe Uzegbu, 21 Mar 2025) defines progressive disclosure purely as staging complexity to cut cognitive load; it says nothing about not exposing controls the system lacks.
- **Sources:** [Progressive disclosure of named cockpit controls](https://blog.logrocket.com/ux-design/progressive-disclosure-ux-types-use-cases/)

### SingMOS README · `directional`
**`torch.hub` loaders `singmos_pro` / `singmos_v1` predict singing MOS from 16 kHz waveforms; example returns Pred MOS (batch tensor). Automatic SQA tooling — no MUSHRA panel, no coaching feedback UI, no register/formant knobs on the page.**
- **Implication:** STUDY-042 practice/eval surfaces. Knobs invented: 0. Flips beyond ACCEPT: 0.
- **Identifier:** `https://raw.githubusercontent.com/South-Twilight/SingMOS/main/README.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [SingMOS README](https://raw.githubusercontent.com/South-Twilight/SingMOS/main/README.md)

### SingMOS-Pro · `directional`
**Lyrics MOS, Melody MOS, and overall are separately rated; UTMOS/DNSMOS correlate poorly with singing.**
- **Implication:** Admission must score lyrics and pitch-to-score separately.
- **Identifier:** `arXiv:2510.01812`
- **Verify:** no external verdict — not yet swept
- **Sources:** [SingMOS-Pro](https://arxiv.org/abs/2510.01812)

### SingMOS-Pro dataset card · `directional`
**7,981 clips; `score.json` system/utterance MOS + judges; `metadata.csv` documents `judge_score` and optional `judge_lyrics_score` / `judge_melody_score` columns (may be empty). Annotation/eval dataset surface, not a practice app.**
- **Implication:** STUDY-042 practice/eval surfaces. Knobs invented: 0. Flips beyond ACCEPT: 0.
- **Identifier:** `https://huggingface.co/datasets/TangRain/SingMOS-Pro`
- **Verify:** no external verdict — not yet swept
- **Sources:** [SingMOS-Pro dataset card](https://huggingface.co/datasets/TangRain/SingMOS-Pro)

### SingMOS-Pro: An Comprehensive Benchmark for Singing Quality Assessment · `directional`
**Multilingual SQA benchmark with separate Lyrics MOS (pronunciation/intelligibility), Melody MOS, and Overall MOS — explicit MOS-dimension split for quality vs lyric clarity.**
- **Implication:** STUDY-042 eval deepen. Flips beyond ACCEPT 23/30/50: 0.
- **Identifier:** `SingMOS-Pro STUDY-042 deepen (see url)`
- **Verify:** no external verdict — not yet swept
- **Sources:** [SingMOS-Pro: An Comprehensive Benchmark for Singing Quality Assessment](https://arxiv.org/abs/2510.01812)

### SingMOS: An extensive Open-Source Singing Voice Dataset for MOS Prediction · `directional`
**First open singing MOS dataset (SVS/SVC/resynthesis clips) for automatic singing-quality prediction — SingMOS-class evaluator literature (not a flip).**
- **Implication:** STUDY-042 eval deepen. Flips beyond ACCEPT 23/30/50: 0.
- **Identifier:** `arXiv:2406.10911`
- **Verify:** no external verdict — not yet swept
- **Sources:** [SingMOS: An extensive Open-Source Singing Voice Dataset for MOS Prediction](https://arxiv.org/abs/2406.10911)

### Singing with yourself · `directional`
**· http://www.acsu.buffalo.edu/~pqp/pdfs/Pfordresher&Mantell_2014_CogPsy.pdf — Analog: poor-pitch singers match self recordings far better than other voices. Holds for self-vs-other pitch-matching pedagogy (perfect other/synth is the hard tutor). Limit: imitation psychology ≠ SVS MOS admission harness.**
- **Implication:** STUDY-042 HCI/pedagogy analog hold-with-limit. Green 1990 + fail-transfers omitted. Flips beyond ACCEPT: 0.
- **Identifier:** `https://doi.org/10.1016/j.cogpsych.2013.12.005`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Singing with yourself](https://doi.org/10.1016/j.cogpsych.2013.12.005)

### The Data Provenance Initiative: A Large Scale Audit of Dataset Licensing & Attribution in AI · `directional`
**Multi-disciplinary audit of licensing/attribution under inconsistent documentation — provenance honesty for catalog sources without inventing nodes or flips.**
- **Implication:** STUDY-064 catalog/README honesty. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2310.16787`
- **Verify:** no external verdict — not yet swept
- **Sources:** [The Data Provenance Initiative: A Large Scale Audit of Dataset Licensing & Attribution in AI](https://arxiv.org/abs/2310.16787)

### The Open-Box Fallacy: Why AI Deployment Needs a Calibrated Verification Regime · `directional`
**Argues deployment needs a calibrated verification regime rather than overclaiming openness/explainability as proof — analog for default-unverified rows and flips only on ACCEPT 23/30/50.**
- **Implication:** STUDY-064 catalog/README honesty. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2605.10601`
- **Verify:** no external verdict — not yet swept
- **Sources:** [The Open-Box Fallacy: Why AI Deployment Needs a Calibrated Verification Regime](https://arxiv.org/abs/2605.10601)

### The State of Documentation Practices of Third-party Machine Learning Models and Datasets · `directional`
**Finds model/dataset stores often lack the detailed specs model/dataset cards imply — supports keeping README 175 · 12/175 honest rather than inventing verified mass-flips.**
- **Implication:** STUDY-064 catalog/README honesty. Flips beyond ACCEPT: 0. Nodes invented: 0.
- **Identifier:** `arXiv:2312.15058`
- **Verify:** no external verdict — not yet swept
- **Sources:** [The State of Documentation Practices of Third-party Machine Learning Models and Datasets](https://arxiv.org/abs/2312.15058)

### The VoiceMOS Challenge 2023: Zero-shot Subjective Speech Quality Prediction for Multiple Domains · `directional`
**Challenge framing for automatic prediction of subjective MOS across domains — parent eval class later extended by singing-track MOS datasets (SingMOS lineage).**
- **Implication:** STUDY-042 eval deepen. Flips beyond ACCEPT 23/30/50: 0.
- **Identifier:** `arXiv:2310.02640`
- **Verify:** no external verdict — not yet swept
- **Sources:** [The VoiceMOS Challenge 2023: Zero-shot Subjective Speech Quality Prediction for Multiple Domains](https://arxiv.org/abs/2310.02640)

### The effect of vocal modeling on pitch-matching accuracy of elementary schoolchildren · `directional`
**Vocal-model identity changes pitch-matching accuracy: child > adult female > adult male.**
- **Implication:** A synth singer is the wrong tutor if its register/timbre is far from the learner.
- **Identifier:** `DOI:10.2307/3345186`
- **Verify:** no external verdict — not yet swept
- **Sources:** [The effect of vocal modeling on pitch-matching accuracy of elementary schoolchildren](https://doi.org/10.2307/3345186)

### UTMOS: UTokyo-SaruLab System for VoiceMOS Challenge 2022 · `directional`
**Strong automatic MOS predictor (UTMOS) widely reused as speech/singing SQA baseline — automatic MOS-prediction engine class vs human MOS panels.**
- **Implication:** STUDY-042 eval deepen. Flips beyond ACCEPT 23/30/50: 0.
- **Identifier:** `arXiv:2204.02152`
- **Verify:** no external verdict — not yet swept
- **Sources:** [UTMOS: UTokyo-SaruLab System for VoiceMOS Challenge 2022](https://arxiv.org/abs/2204.02152)

### Vocal Registers? (TA/CT antagonism lexicon) · `directional`
**Analog: chest/head/mix as muscular coordination language, not a simple F0 switch. Holds-with-limit for pedagogy register wording (STUDY-022 item 9). Limit: does not license inventing chest/mix/head menus on DiffSinger/OpenUtau/WORLD.**
- **Implication:** STUDY-042 HCI/pedagogy analog hold-with-limit. Green 1990 + fail-transfers omitted. Flips beyond ACCEPT: 0.
- **Identifier:** `http://www.voicescienceworks.org/vocal-registers.html`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Vocal Registers? (TA/CT antagonism lexicon)](http://www.voicescienceworks.org/vocal-registers.html)

### VocalRender: Score-Native Singing Voice Synthesis for Real-World Composition · `directional`
**VocalRender wins MS-MOS (~2.96) on reported subjective score-following panel — MS-MOS figure only this land; RPA/IOU objective/subjective invert clause stays unverified.**
- **Implication:** STUDY-042 eval deepen. VocalRender RPA/IOU invert UNVERIFIED. Flips beyond ACCEPT: 0.
- **Identifier:** `arXiv:2607.27768`
- **Verify:** no external verdict — not yet swept
- **Sources:** [VocalRender: Score-Native Singing Voice Synthesis for Real-World Composition](https://arxiv.org/abs/2607.27768)

### vocal-synth-engine README · `directional`
**Cockpit SPA: piano roll, live keyboard, XY pad (timbre×breathiness), latency presets, render bank + telemetry (peak/RTF/jitter). Practice/instrument UI documented; no MUSHRA, no SingMOS, no named singing-coach score panel.**
- **Implication:** STUDY-042 practice/eval surfaces. Knobs invented: 0. Flips beyond ACCEPT: 0.
- **Identifier:** `https://raw.githubusercontent.com/mcp-tool-shop-org/vocal-synth-engine/main/README.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [vocal-synth-engine README](https://raw.githubusercontent.com/mcp-tool-shop-org/vocal-synth-engine/main/README.md)

