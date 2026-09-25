# Lyric-to-note alignment
_Vowel-on-beat, phoneme×MIDI×duration, melisma and onset timing_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

27 findings · 20 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| A Real-Time Lyrics Alignment System Using Chroma And Phonetic Features For Classical Vocal Performance | Park, Yong, Kwon & Nam · 2024 | Live classical lyrics alignment combining chromagram with phonetic posteriorgrams under low-latency constraint. | ✓ |
| Adapting pretrained speech model for Mandarin lyrics transcription and alignment | Wang, Leong, Lin, Su & Jang · 2023 | Whisper adapted to Mandarin singing yields lyrics alignment MAE 0.071 s on polyphonic pop. | ✓ |
| Contrastive Learning-Based Audio to Lyrics Alignment for Multiple Languages | Durand, Stoller & Ewert · 2023 | Contrastive cross-modal embeddings reach <0.2 s average absolute error on Jamendo — alignment-tailored alternative to CTC transcription loss. | ✓ |
| Impact of Latency on Perceptual Judgments… in VR | Waltemate et al. · 2016 | Analog: HCI simultaneity / agency thresholds; delays above ~75 ms worsen felt sync. Holds for practice-companion UX of lyric lock; limit: perceptual threshold ≠ phoneme-boundary / MFA error. | ✓ |
| MFA Troubleshooting — singing atypical style | Montreal Forced Aligner · 2024 | Official caveat: MFA is not intended to align single files that are long, noisy, or a different style such as singing — on-page only; further singing failure modes stay ·. | ✓ |
| MakeDiffSinger README — MFA for acoustic training | openvpi / MakeDiffSinger · 2024 | Dataset pipeline names acoustic-forced-alignment make dataset from scratch with MFA for acoustic model training — MFA upstream labeling, not runtime score-lock. | ✓ |
| Montreal Forced Aligner user guide | McAuliffe et al. · 2026 | Analog: speech forced alignment. MFA is documented as a CLI for forced alignment of SPEECH datasets using Kaldi, driven by a pronunciation dictionary plus a pretrained acoustic model; the validator trains 'a simple monophone model' within Kaldi. The specific 'GMM/HMM' wording appears nowhere in the current docs - it is an inference from Kaldi monophone/triphone training, so cite it as Kaldi-based rather than as documented GMM/HMM. It does not transfer cleanly to singing: see the MFA troubleshooting caveat and the NHSS 25.30 vs 103.90 ms word-boundary measurement. | ✓ |
| NHSS | Sharma et al. · 2021 | MFA word-boundary error is 25 ms on speech vs 104 ms on singing. | ✓ |
| OpenUtau DiffSingerRhythmizerPhonemizer | stakira / OpenUtau · 2024 | Lyric→phonemes; ONNX rhythmizer inputs tokens/midi/midi_dur/is_slur → ph_dur; vowels stretched so note onsets align — note grid drives phone timing. | ✓ |
| OpenUtau DiffSingerVariance predict_dur | stakira / OpenUtau · 2024 | DiffSingerVariance runs a dual linguistic-encode path. When predict_dur is true it uses word encode mode: word_div is built from the indices of vowel phones (g2p.IsVowel) and word_dur is the SUM of the phone durations inside each vowel-anchored group. When predict_dur is false it uses phoneme encode mode and feeds ph_dur directly. Correction: word_dur is derived from ph_dur, NOT from note spans - both branches start from the same PaddedPhoneDurations, so the split is word-level vs phone-level granularity for the linguistic encoder, not predicted vs editor-fixed phone timing. | ✓ |
| RFC 5905 NTPv4 | Mills et al. / IETF · 2010 | Analog: two clocks share a reference; undisciplined skew accumulates. Holds for jam startSec vs Seed Audio [start:end] as dual timelines. | ✓ |
| RMSSinger | He et al. · 2023 | Fine-grained SVS corpora force MFA then manual phoneme/note edits because one vowel may span multiple notes. | ✓ |
| RMSSinger: Realistic-Music-Score based Singing Voice Synthesis | He, Liu, Ye, Huang, Cui, Liu et al. · 2023 | Fine-grained SVS pipelines run MFA then manual phoneme/note edits because one vowel may span multiple notes; switches to word-level modeling. | ✓ |
| Segment Duration and Proportion in Mandarin Singing | Zhang & Wang · 2020 | Measured on 20 songs from the MIREX singing corpus (Mandarin). Mandarin SPEECH vowel proportion is 51.6-74.6%; duplicating that ratio in synthesis would force 2.5-5 s consonants on a 10 s sung syllable, 'which is physically unachievable'. In the sung data the extra length goes to the rime: the nucleus lengthens the most, codas follow, and onset duration rises only slightly while its proportion falls. Onset ceilings are category-specific: affricate/fricative consonant onsets max 0.28 s (max syllable 2.11 s, N=284), while approximant onsets max 0.40 s (N=793) - so '~0.28 s' is not a global onset ceiling. Also note the coda is not frozen: the paper reports the nasal coda's proportion always RISES as the syllable or rime lengthens. | ✓ |
| SongTrans | Wu et al. · 2024 | MFA labels melisma as silence, which then collides with true rests. | ✓ |
| Source Level Debugging with LLVM | LLVM Project · 2024 | Analog: source AST objects map onto instruction ranges via debug metadata. Holds for discrete lyric/score tokens ↔ audio-frame spans under score-lock; limit: no continuous-time melisma or expressive lag. | ✓ |
| Specifying Systems (TLA) | Lamport · 2002 | Analog: verification — Spec = Init ∧ □[Next]; stuttering steps are unobservable. Partial hold: expressive microtiming as stuttering around a score Spec; limit: discrete state machines, no continuous F0. | ✓ |
| Towards Context-Aware Neural Performance-Score Synchronisation | Agrawal · 2022 | Analog: Needleman–Wunsch Time Warping / DTW map performance ↔ score with warps and jumps. Holds for monotonic lyric↔timeline alignment; limit: classic NW/DTW assume structural agreement. | ✓ |
| When Does a Sung Tone Start? | Sundberg & Bauer-Huppmann · 2007 | Sung tone onset is the vowel: accompanists most commonly synchronised their piano attacks with the singers' vowel onsets. Measured on commercial CD recordings of art songs performed by international vocal artists with piano. Lead and lag do occur, apparently for expressive purposes, and vary greatly by song - smallest at fast tempo, longest at slow tempo. UNVERIFIED: the specific '-100 to +300 ms' consonant-to-beat range is not in the abstract and the full text could not be retrieved (paywalled); do not quote that number without the paper in hand. | ✓ |
| When are initial consonants articulated in choral performance? | Hauck · 2020 | Analog: music pedagogy - initial consonants are nearly always anticipated (articulated ahead of the beat to which they are assigned), with the amount of anticipation shaped by the consonant's 'lengthenability' and by its surroundings; exceptions noted for the plosive [kh] and occasionally the second consonant of a cluster. Measured on six recordings of Bach BWV 227/5 and four of Schubert's An die Sonne (German choral repertoire). The paper does not measure vowel-on-beat placement - that finding belongs to Sundberg & Bauer-Huppmann 2007, not to Hauck. | ✓ |
| CTC forced alignment API tutorial | Zhang & Hira / torchaudio · docs | Analog: modern CTC FA from frame emissions → token/word spans via `forced_align` + merge; blank treatment for duration is ambiguous/peaky. Holds as CTC-FA sibling to Stoller. Limit: speech FA on Wav2Vec2 emissions; not score-conditioned MIDI lock. | · |
| Connectionist Temporal Classification | Graves, Fernández, Gomez & Schmidhuber · 2006 | Analog: CTC labels unsegmented sequences by summing blank/repeat paths (many-to-one, U≤T); no pre-segmentation. Holds for naming the CTC lyrics-to-audio family (Stoller ACCEPT). Limit: CTC transcript paths ≠ lyrics-to-MIDI note grid / vowel-on-beat score-lock. | · |
| End-to-end Lyrics Alignment | Stoller, Durand & Ewert · 2019 | CTC lyrics-to-audio alignment (~0.35 s mean word error) is not lyrics-to-MIDI. | · |
| How Does This Thing Work? (aeneas TTS+DTW) | Pettarin / readbeyond · docs | Analog: FA via TTS synth + Sakoe-Chiba DTW on MFCC → text↔audio sync map. Holds when structures match (monotonic sync). Limit: ebook/caption speech FA; no MIDI note hard constraint; melisma/repeats break clean transfer. | · |
| Kaldi: HMM topology and alignments | Kaldi Project · docs | Analog: Viterbi forced path yields per-frame transition-ids given transcript (MFA substrate). Holds for naming HMM-FA mechanism under MFA/Gentle. Limit: speech GMM/HMM phone paths; sung duration/melisma not in the topology. | · |
| Sequence Modeling with CTC | Hannun / Distill · 2017 | Analog: CTC alignments are monotonic many-to-one; blank merges; output cannot exceed input length. Holds for why CTC FA recovers audio spans, not MIDI note onsets. Limit: speech/handwriting framing; peaky blanks ≠ vowel-nucleus contract. | · |
| Synchronising speech segments with musical beats in Mandarin and English singing | Zhang & Zhu · 2021 | English vowel beats sit near mid-vowel; sonorant onsets take earlier beats than stops/fricatives. | · |

## Detail

### A Real-Time Lyrics Alignment System Using Chroma And Phonetic Features For Classical Vocal Performance · `load-bearing`
**Live classical lyrics alignment combining chromagram with phonetic posteriorgrams under low-latency constraint.**
- **Implication:** Chroma+phonetic singing align.
- **Identifier:** `arXiv:2401.09200`
- **Verify:** arXiv abstract verbatim: 'an optimal combination of chromagram and phonetic posteriorgram (PPG)' for real-time alignment in live singing. Park/Yong/Kwon/Nam, Jan 2024. Evaluated on the Schubert Winterreise Dataset.
- **Sources:** [A Real-Time Lyrics Alignment System Using Chroma And Phonetic Features For Classical Vocal Performance](https://arxiv.org/abs/2401.09200)

### Adapting pretrained speech model for Mandarin lyrics transcription and alignment · `load-bearing`
**Whisper adapted to Mandarin singing yields lyrics alignment MAE 0.071 s on polyphonic pop.**
- **Implication:** Pretrained-speech transfer to sung lyric timing.
- **Identifier:** `arXiv:2311.12488`
- **Verify:** arXiv abstract verbatim: 'a mean absolute error of 0.071 seconds for lyrics alignment' (CER <18%) on a Mandarin POLYPHONIC pop dataset. Whisper fine-tuned on monophonic Mandarin singing. Sung data, not speech.
- **Sources:** [Adapting pretrained speech model for Mandarin lyrics transcription and alignment](https://arxiv.org/abs/2311.12488)

### Contrastive Learning-Based Audio to Lyrics Alignment for Multiple Languages · `load-bearing`
**Contrastive cross-modal embeddings reach <0.2 s average absolute error on Jamendo — alignment-tailored alternative to CTC transcription loss.**
- **Implication:** Contrastive lyrics alignment deepen.
- **Identifier:** `arXiv:2306.07744`
- **Verify:** arXiv abstract verbatim: 'average absolute error below 0.2 seconds on the standard Jamendo dataset'; framed as an alternative to speech-recognition/CTC toolkits. ICASSP 2023. Jamendo is sung music, not speech.
- **Sources:** [Contrastive Learning-Based Audio to Lyrics Alignment for Multiple Languages](https://arxiv.org/abs/2306.07744)

### Impact of Latency on Perceptual Judgments… in VR · `load-bearing`
**Analog: HCI simultaneity / agency thresholds; delays above ~75 ms worsen felt sync. Holds for practice-companion UX of lyric lock; limit: perceptual threshold ≠ phoneme-boundary / MFA error.**
- **Implication:** ~75 ms UX threshold for lyric lock feel.
- **Identifier:** `Waltemate 2016`
- **Verify:** OpenAlex abstract verbatim (DOI 10.1145/2993369.2993381): 'motor performance and simultaneity perception are affected by latencies above 75 ms'. Waltemate+6, VRST 2016. Dataset: CAVE full-body visual mirror, 45-350 ms.
- **Sources:** [Impact of Latency on Perceptual Judgments… in VR](https://ls7-gv.cs.tu-dortmund.de/publications/2016-latency.pdf)

### MFA Troubleshooting — singing atypical style · `load-bearing`
**Official caveat: MFA is not intended to align single files that are long, noisy, or a different style such as singing — on-page only; further singing failure modes stay ·.**
- **Implication:** MFA singing caveat on-page; extras stay unverified.
- **Identifier:** `mfa:troubleshooting`
- **Verify:** Live MFA docs (v3.4; release v3.4.2, 2026-08-20) carry it verbatim: 'MFA is not intended to align single files, particularly if they are long, have noise in the background, a different style such a singing etc.'
- **Sources:** [MFA Troubleshooting — singing atypical style](https://montreal-forced-aligner.readthedocs.io/en/stable/user_guide/troubleshooting.html)

### MakeDiffSinger README — MFA for acoustic training · `load-bearing`
**Dataset pipeline names acoustic-forced-alignment make dataset from scratch with MFA for acoustic model training — MFA upstream labeling, not runtime score-lock.**
- **Implication:** MFA as DiffSinger dataset labeling only.
- **Identifier:** `github:MakeDiffSinger`
- **Verify:** MakeDiffSinger README line verbatim: 'acoustic-forced-alignment: make dataset from scratch with MFA for acoustic model training', under the recommended standard dataset-making pipelines. Upstream labeling, not runtime.
- **Sources:** [MakeDiffSinger README — MFA for acoustic training](https://github.com/openvpi/MakeDiffSinger)

### Montreal Forced Aligner user guide · `load-bearing`
**Analog: speech forced alignment. MFA is documented as a CLI for forced alignment of SPEECH datasets using Kaldi, driven by a pronunciation dictionary plus a pretrained acoustic model; the validator trains 'a simple monophone model' within Kaldi. The specific 'GMM/HMM' wording appears nowhere in the current docs - it is an inference from Kaldi monophone/triphone training, so cite it as Kaldi-based rather than as documented GMM/HMM. It does not transfer cleanly to singing: see the MFA troubleshooting caveat and the NHSS 25.30 vs 103.90 ms word-boundary measurement.**
- **Implication:** Leave MFA speech→singing caveats unverified as transfer.
- **Identifier:** `McAuliffe, Gunter, Wagner & Sonderegger, Interspeech 2026 (MFA v3.4.2 docs); original McAuliffe, Socolof, Mihuc, Wagner & Sonderegger, Interspeech 2017`
- **Verify:** README verbatim: MFA is 'a command line utility for performing forced alignment of speech datasets using Kaldi'. Release v3.4.2 (2026-08-20); cite is McAuliffe et al., Interspeech 2026 (orig. 2017), not 2024.
- **Sources:** [Montreal Forced Aligner user guide](https://montreal-forced-aligner.readthedocs.io/en/stable/user_guide/index.html)

### NHSS · `load-bearing`
**MFA word-boundary error is 25 ms on speech vs 104 ms on singing.**
- **Implication:** Do not trust speech MFA boundaries for PhonemeEvents.
- **Identifier:** `arXiv:2012.00337`
- **Verify:** NHSS Table 5, auto vs manual annotation: speech word-boundary deviation 25.30 ms, singing 103.90 ms. Decisive: the singing run used the DAMP speaker-ADAPTED model, not raw LibriSpeech - 4x is the post-adaptation floor.
- **Sources:** [NHSS](https://arxiv.org/abs/2012.00337)

### OpenUtau DiffSingerRhythmizerPhonemizer · `load-bearing`
**Lyric→phonemes; ONNX rhythmizer inputs tokens/midi/midi_dur/is_slur → ph_dur; vowels stretched so note onsets align — note grid drives phone timing.**
- **Implication:** Score-grid phoneme×note in OpenUtau.
- **Identifier:** `github:DiffSingerRhythmizerPhonemizer`
- **Verify:** Source read: ONNX inputs tokens/midi/midi_dur/is_slur -> ph_dur, exactly as claimed. Comments verbatim: 'Align the starting time of vowels to the position of each note'; 'Starting consonants are not scaled'.
- **Sources:** [OpenUtau DiffSingerRhythmizerPhonemizer](https://raw.githubusercontent.com/stakira/OpenUtau/master/OpenUtau.Core/DiffSinger/Phonemizers/DiffSingerRhythmizerPhonemizer.cs)

### OpenUtau DiffSingerVariance predict_dur · `load-bearing`
**DiffSingerVariance runs a dual linguistic-encode path. When predict_dur is true it uses word encode mode: word_div is built from the indices of vowel phones (g2p.IsVowel) and word_dur is the SUM of the phone durations inside each vowel-anchored group. When predict_dur is false it uses phoneme encode mode and feeds ph_dur directly. Correction: word_dur is derived from ph_dur, NOT from note spans - both branches start from the same PaddedPhoneDurations, so the split is word-level vs phone-level granularity for the linguistic encoder, not predicted vs editor-fixed phone timing.**
- **Implication:** Predicted vs fixed phone timing paths.
- **Identifier:** `github:DiffSingerVariance`
- **Verify:** Source read: 'if predict_dur is true, use word encode mode' -> PaddedWordDivAndDur(phrase, ph_dur, g2p.IsVowel); else 'phoneme encode mode' -> ph_dur. Vowel grouping confirmed, but word_dur SUMS ph_dur, not note spans.
- **Sources:** [OpenUtau DiffSingerVariance predict_dur](https://github.com/stakira/OpenUtau/blob/master/OpenUtau.Core/DiffSinger/DiffSingerVariance.cs)

### RFC 5905 NTPv4 · `load-bearing`
**Analog: two clocks share a reference; undisciplined skew accumulates. Holds for jam startSec vs Seed Audio [start:end] as dual timelines.**
- **Implication:** Dual clocks: jam startSec vs seed [start:end].
- **Identifier:** `RFC 5905`
- **Verify:** RFC 5905 'NTPv4: Protocol and Algorithms Specification', Mills, Martin (Ed.), Burbank, Kasch, June 2010. Defines clock offset relative to a reference and the Clock Discipline Algorithm (Sec 11.3) correcting frequency/skew.
- **Sources:** [RFC 5905 NTPv4](https://datatracker.ietf.org/doc/html/rfc5905)

### RMSSinger · `load-bearing`
**Fine-grained SVS corpora force MFA then manual phoneme/note edits because one vowel may span multiple notes.**
- **Implication:** Prefer syllable/word→note maps (slurs for melisma) over phone-level forced alignment.
- **Identifier:** `ACL 2023 Findings`
- **Verify:** ACL Anthology resolves: 2023.findings-acl.16, pp236-248. Verbatim: phoneme duration 'first extracted from singing through Montreal Forced Aligner and then further manually annotated'; 'one vowel phoneme may correspond to multiple notes'.
- **Sources:** [RMSSinger](https://aclanthology.org/2023.findings-acl.16/)

### RMSSinger: Realistic-Music-Score based Singing Voice Synthesis · `load-bearing`
**Fine-grained SVS pipelines run MFA then manual phoneme/note edits because one vowel may span multiple notes; switches to word-level modeling.**
- **Implication:** MFA+manual; word-level vs phoneme-duration hard align.
- **Identifier:** `arXiv:2305.10686`
- **Verify:** arXiv:2305.10686, He/Liu/Ye/Huang/Cui/Liu/Zhao, May 2023. Text confirms MFA-then-manual annotation, 'one vowel phoneme may correspond to multiple notes', and word-level modeling to avoid phoneme-level mel-note alignment.
- **Sources:** [RMSSinger: Realistic-Music-Score based Singing Voice Synthesis](https://arxiv.org/abs/2305.10686)

### Segment Duration and Proportion in Mandarin Singing · `load-bearing`
**Measured on 20 songs from the MIREX singing corpus (Mandarin). Mandarin SPEECH vowel proportion is 51.6-74.6%; duplicating that ratio in synthesis would force 2.5-5 s consonants on a 10 s sung syllable, 'which is physically unachievable'. In the sung data the extra length goes to the rime: the nucleus lengthens the most, codas follow, and onset duration rises only slightly while its proportion falls. Onset ceilings are category-specific: affricate/fricative consonant onsets max 0.28 s (max syllable 2.11 s, N=284), while approximant onsets max 0.40 s (N=793) - so '~0.28 s' is not a global onset ceiling. Also note the coda is not frozen: the paper reports the nasal coda's proportion always RISES as the syllable or rime lengthens.**
- **Implication:** Freeze onset/coda in a short band; leftover note length goes to the nucleus.
- **Identifier:** `SpeechProsody 2020`
- **Verify:** Zhang & Wang, Speech Prosody 2020, verbatim: 'consonants need to be lengthened to 2.5s - 5s in a 10-second syllable'; 'the longest consonant only reaches 0.28s'. But 0.28 s is RQ1 consonants only; approximants reach 0.40 s. 20 MIREX songs.
- **Sources:** [Segment Duration and Proportion in Mandarin Singing](https://www.isca-archive.org/speechprosody_2020/zhang20c_speechprosody.pdf)

### SongTrans · `load-bearing`
**MFA labels melisma as silence, which then collides with true rests.**
- **Implication:** Slur/tie flags (or an explicit note-count head) are required.
- **Identifier:** `arXiv:2409.14619`
- **Verify:** SongTrans full text verbatim: 'MFA tends to recognize melisma as silence' and 'the mistakenly recognized melisma portion will be confused with the existing silence in the audio and cannot be identified'. Wu et al., Sep 2024.
- **Sources:** [SongTrans](https://arxiv.org/abs/2409.14619)

### Source Level Debugging with LLVM · `load-bearing`
**Analog: source AST objects map onto instruction ranges via debug metadata. Holds for discrete lyric/score tokens ↔ audio-frame spans under score-lock; limit: no continuous-time melisma or expressive lag.**
- **Implication:** Discrete lyric/score spans under score-lock.
- **Identifier:** `LLVM SourceLevelDebugging`
- **Verify:** LLVM doc verbatim: 'how the important pieces of the source-language's Abstract Syntax Tree map onto LLVM code', plus 'a mapping from each variable to their machine locations over ranges of instructions'. Discrete only.
- **Sources:** [Source Level Debugging with LLVM](https://llvm.org/docs/SourceLevelDebugging.html)

### Specifying Systems (TLA) · `load-bearing`
**Analog: verification — Spec = Init ∧ □[Next]; stuttering steps are unobservable. Partial hold: expressive microtiming as stuttering around a score Spec; limit: discrete state machines, no continuous F0.**
- **Implication:** Partial: stuttering ≠ continuous F0 continuum.
- **Identifier:** `TLA Specifying Systems`
- **Verify:** Lamport's own book page: 'Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers', Addison-Wesley, (c) 2002. Spec == Init /\ [][Next]_vars; [A]_x is A \/ UNCHANGED x, so stuttering is always allowed.
- **Sources:** [Specifying Systems (TLA)](https://lamport.azurewebsites.net/tla/book-01-11-10.pdf)

### Towards Context-Aware Neural Performance-Score Synchronisation · `load-bearing`
**Analog: Needleman–Wunsch Time Warping / DTW map performance ↔ score with warps and jumps. Holds for monotonic lyric↔timeline alignment; limit: classic NW/DTW assume structural agreement.**
- **Implication:** NW/DTW only under structural agreement.
- **Identifier:** `arXiv:2206.00454`
- **Verify:** QMUL PhD thesis, Ruchit Agrawal, 31 May 2022. Full text names NWTW (Grachten 2013) and JumpDTW for jumps, and states traditional methods 'normally assume complete structural agreement between the performances and the scores'.
- **Sources:** [Towards Context-Aware Neural Performance-Score Synchronisation](https://arxiv.org/abs/2206.00454)

### When Does a Sung Tone Start? · `load-bearing`
**Sung tone onset is the vowel: accompanists most commonly synchronised their piano attacks with the singers' vowel onsets. Measured on commercial CD recordings of art songs performed by international vocal artists with piano. Lead and lag do occur, apparently for expressive purposes, and vary greatly by song - smallest at fast tempo, longest at slow tempo. UNVERIFIED: the specific '-100 to +300 ms' consonant-to-beat range is not in the abstract and the full text could not be retrieved (paywalled); do not quote that number without the paper in hand.**
- **Implication:** Put the vowel nucleus on the MIDI beat; park onset consonants in the preceding gap.
- **Identifier:** `DOI:10.1016/j.jvoice.2006.01.003`
- **Verify:** Crossref resolves the DOI exactly: Sundberg & Bauer-Huppmann, J Voice 21:285-293, May 2007. Abstract confirms accompanists sync to the singer's VOWEL onset. Paywalled - the '-100/+300 ms' range is unverifiable.
- **Sources:** [When Does a Sung Tone Start?](https://doi.org/10.1016/j.jvoice.2006.01.003)

### When are initial consonants articulated in choral performance? · `load-bearing`
**Analog: music pedagogy - initial consonants are nearly always anticipated (articulated ahead of the beat to which they are assigned), with the amount of anticipation shaped by the consonant's 'lengthenability' and by its surroundings; exceptions noted for the plosive [kh] and occasionally the second consonant of a cluster. Measured on six recordings of Bach BWV 227/5 and four of Schubert's An die Sonne (German choral repertoire). The paper does not measure vowel-on-beat placement - that finding belongs to Sundberg & Bauer-Huppmann 2007, not to Hauck.**
- **Implication:** Vowel-on-beat; consonants anticipate.
- **Identifier:** `Hauck 2020`
- **Verify:** Hauck, Music Performance Research v10, 2020. Verbatim: consonants 'nearly always anticipated...ahead of the beat to which they are assigned', with lengthenability/surroundings effects. Vowel-on-beat is NOT measured here.
- **Sources:** [When are initial consonants articulated in choral performance?](https://musicperformanceresearch.org/wp-content/uploads/2020/12/MPR-0145-Hauck-copyedited_FINAL.pdf)

### CTC forced alignment API tutorial · `directional`
**Analog: modern CTC FA from frame emissions → token/word spans via `forced_align` + merge; blank treatment for duration is ambiguous/peaky. Holds as CTC-FA sibling to Stoller. Limit: speech FA on Wav2Vec2 emissions; not score-conditioned MIDI lock.**
- **Implication:** STUDY-041 FA/CTC analog hold-with-limit. Fail-transfers 6–8 omitted. Flips beyond ACCEPT: 0.
- **Identifier:** `https://docs.pytorch.org/audio/stable/tutorials/ctc_forced_alignment_api_tutorial.html`
- **Verify:** no external verdict — not yet swept
- **Sources:** [CTC forced alignment API tutorial](https://docs.pytorch.org/audio/stable/tutorials/ctc_forced_alignment_api_tutorial.html)

### Connectionist Temporal Classification · `directional`
**Analog: CTC labels unsegmented sequences by summing blank/repeat paths (many-to-one, U≤T); no pre-segmentation. Holds for naming the CTC lyrics-to-audio family (Stoller ACCEPT). Limit: CTC transcript paths ≠ lyrics-to-MIDI note grid / vowel-on-beat score-lock.**
- **Implication:** STUDY-041 FA/CTC analog hold-with-limit. Fail-transfers 6–8 omitted. Flips beyond ACCEPT: 0.
- **Identifier:** `http://www.cs.toronto.edu/~graves/icml_2006.pdf`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Connectionist Temporal Classification](http://www.cs.toronto.edu/~graves/icml_2006.pdf)

### End-to-end Lyrics Alignment · `directional`
**CTC lyrics-to-audio alignment (~0.35 s mean word error) is not lyrics-to-MIDI.**
- **Implication:** Synthesis from MIDI should stay score-constrained, not unconstrained-aligner-driven.
- **Identifier:** `arXiv:1902.06797`
- **Verify:** no external verdict — not yet swept
- **Sources:** [End-to-end Lyrics Alignment](https://arxiv.org/abs/1902.06797)

### How Does This Thing Work? (aeneas TTS+DTW) · `directional`
**Analog: FA via TTS synth + Sakoe-Chiba DTW on MFCC → text↔audio sync map. Holds when structures match (monotonic sync). Limit: ebook/caption speech FA; no MIDI note hard constraint; melisma/repeats break clean transfer.**
- **Implication:** STUDY-041 FA/CTC analog hold-with-limit. Fail-transfers 6–8 omitted. Flips beyond ACCEPT: 0.
- **Identifier:** `https://raw.githubusercontent.com/readbeyond/aeneas/master/wiki/HOWITWORKS.md`
- **Verify:** no external verdict — not yet swept
- **Sources:** [How Does This Thing Work? (aeneas TTS+DTW)](https://raw.githubusercontent.com/readbeyond/aeneas/master/wiki/HOWITWORKS.md)

### Kaldi: HMM topology and alignments · `directional`
**Analog: Viterbi forced path yields per-frame transition-ids given transcript (MFA substrate). Holds for naming HMM-FA mechanism under MFA/Gentle. Limit: speech GMM/HMM phone paths; sung duration/melisma not in the topology.**
- **Implication:** STUDY-041 FA/CTC analog hold-with-limit. Fail-transfers 6–8 omitted. Flips beyond ACCEPT: 0.
- **Identifier:** `https://www.kaldi-asr.org/doc/hmm.html`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Kaldi: HMM topology and alignments](https://www.kaldi-asr.org/doc/hmm.html)

### Sequence Modeling with CTC · `directional`
**Analog: CTC alignments are monotonic many-to-one; blank merges; output cannot exceed input length. Holds for why CTC FA recovers audio spans, not MIDI note onsets. Limit: speech/handwriting framing; peaky blanks ≠ vowel-nucleus contract.**
- **Implication:** STUDY-041 FA/CTC analog hold-with-limit. Fail-transfers 6–8 omitted. Flips beyond ACCEPT: 0.
- **Identifier:** `https://distill.pub/2017/ctc`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Sequence Modeling with CTC](https://distill.pub/2017/ctc)

### Synchronising speech segments with musical beats in Mandarin and English singing · `directional`
**English vowel beats sit near mid-vowel; sonorant onsets take earlier beats than stops/fricatives.**
- **Implication:** Fire the English nucleus slightly after note-on.
- **Identifier:** `arXiv:2106.10045`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Synchronising speech segments with musical beats in Mandarin and English singing](https://arxiv.org/abs/2106.10045)

