# Wave 1 — Sung vocals for AI Jam Sessions (study-swarm)

**KB** `vocology-knowledge` · **dispatched** 2026-09-04 · **5** parallel web-grounded lanes (Grok 4.6 research agents) · protocol: research-grounded advisor ("study-swarm").

**Trigger:** Director asked to add vocals to `ai-jam-sessions`, starting with a study-swarm into prosody, vocology, etc., inform this repo, then decide the route. No product code in this wave.

**Consumer measured 2026-09-04:** `E:\AI\ai-jam-sessions` HEAD `72dbb83`. Existing "vocals" are *instruments*: looped "aah" carriers (`vocal-engine.ts`), Pink Trombone LF + 1D waveguide SATB (`vocal-tract-engine.ts`), additive Kokoro-formant synth via `vocal-synth-adapter.ts`. Sing-along is **text** (solfege / note-names / contour / syllables), not sung lyrics. `vocal-synth-engine` already has `VocalScore` (MIDI notes + optional lyrics + ARPAbet `PhonemeEvent`s + dynamics/breathiness/timbre lanes) and CMU-dict G2P — the jam adapter currently ignores lyrics and does `noteOn`/`noteOff`. ROADMAP Tier 3 still lists Spoken Teaching TTS (speech, not singing).

Verification: pass 2 **escalate (advisory, 0 fabricated)** — prism `prism-01m1ndcs5e3zmbptcj3dfre1tb`. Pass 1 refused a misattributed Titze DOI (corrected once). Receipts: [`verification.md`](verification.md) · [`citation-receipt.json`](citation-receipt.json). Raw lane output: [`research-raw.json`](research-raw.json).

---

## The decision this grounds

Three product-shaped questions, not one:

1. **Singing instrument** — operator supplies MIDI + lyrics; engine sings *those notes* under the existing accompaniment.
2. **Song generator** — text in, mixed track out (ACE-Step / DiffRhythm / YuE). Already catalogued in model-knowledge audio.
3. **Coach / tutor** — spoken teaching, or a vocal model the human matches.

Evidence that would change the architecture: whether speech-TTS prosody can be reused; whether Pink Trombone / additive engines can become singers by adding G2P; whether a local neural SVS can hard-lock MIDI; whether a high-MOS lead vocal even helps a learner.

## The spine (every lane serves this)

```
deterministic score floor (MIDI + vowel-on-beat phoneme timeline)
        ↓
model writes residuals (vibrato, time-lag, dynamics, formant tracking) inside that floor
        ↓
verifier admits (score-relative F0 cents + lyrics MOS + hidden-ref panel — not speech MOS)
```

This is the studio's standing shape (deterministic floor + AI ceiling + admission gate). The research below is what makes each layer load-bearing for *voice*, not just another synth preset.

---

## Research grounding (the empirical floor)

Findings are retrieval-sourced by five parallel lanes. Load-bearing claims are then re-verified by a family-different, reasoning-stripped citation gate (`roleos verify-citations` → prism). Each finding: **claim** — source — implication. Numbered globally. Architectural connections in the next section cite these numbers.

### Lane A — vocology / source–filter floor

1. **The radiated voice is source × tract filter; independence is only a first approximation.** Fant 1960 (*Acoustic Theory of Speech Production*, DOI:10.1515/9783110873429). Implication: a formant-shaped oscillator that never generates a glottal flow and then filters it is not a voice.

2. **The LF source is the derivative of glottal flow (Ee closing discontinuity + Ta return phase), not a harmonic oscillator.** Fant, Liljencrants & Lin 1985 (*A four-parameter model of glottal flow*, STL-QPSR 26(4); https://www.speech.kth.se/qpsr/1985/1985_26_4_001-013.pdf). Implication: pitch-shifting a looped "aah" or a Kokoro formant preset without open-quotient / return-phase / Ee control cannot produce modal vs breathy vs pressed source spectra.

3. **The singer's formant is a ~2.8 kHz cluster from larynx-tube mismatch, not painted EQ.** Sundberg 1974 (*Articulatory interpretation of the singing formant*, JASA 55:838, DOI:10.1121/1.1914609). Implication: SATB additive presets without a narrowed epilarynx will lack male operatic ring.

4. **When F0 exceeds speech F1, a singer raises R1 to track F0; a fixed tract dumps the remaining harmonic into a dead zone and vowels collapse.** Joliveau, Smith & Wolfe 2004 (*Vocal tract resonances in singing: the soprano voice*, JASA 116:2434, DOI:10.1121/1.1791717). Implication: MIDI `noteOn` that drives F0 above a fixed SATB F1 without jaw/lip modification is the named production error.

5. **At singing pitches source and filter are not independent: F0–F1 crossovers destabilize the folds.** Titze 2008 (*Nonlinear source–filter coupling in phonation: Theory*, JASA 123:2733, DOI:10.1121/1.2832337, PMC2811547). Companion exercises: Titze, Riede & Popolo 2008 (DOI:10.1121/1.2832339, PMC2677316). Implication: holding a Pink-Trombone tract fixed while sweeping MIDI through F1 is a documented instability, not a filter miss. *Gate note: first-pass DOI 10.1121/1.2829014 was a misattribution (Crossref no-record → refuse); corrected once to 10.1121/1.2832337.*

6. **Registers are glottal shapes, not F0 labels.** Titze 2014 (*Bi-stable vocal fold adduction*, JASA 135:2091, PMC4167751). Modal = thick TA-squared glottis; falsetto = thin CT-dominated edge; fry = pulse-like below ~70 Hz. Implication: one LF/waveguide source with only F0 changed cannot be SATB "modal vs falsetto."

7. **Vibrato is not a 5–7 Hz law.** Prame 1994 (*Measurements of the vibrato rate of ten singers*, JASA 96:1979, DOI:10.1121/1.410141). Mean 6.0 Hz, but rate typically rose ~15% at tone ends; single cycles 4.6–8.7 Hz; later work extent ±34 to ±123 cents. Implication: a constant LFO on F0 is a cartoon; rate and extent must move with phrase position.

8. **A voice source is mixed periodic + glottal aspiration; aspiration noise cues breathiness more than H1 amplitude.** Klatt & Klatt 1990 (*Analysis, synthesis, and perception of voice quality variations*, JASA 87:820, DOI:10.1121/1.398894). Implication: additive singing without a glottal noise source cannot do breath, /h/, or phrase-final decay.

### Lane B — musical vs speech prosody

9. **On parallel English pop, sung vowels average 830.5 ms vs 148.0 ms spoken (~5.6×); stops/fricatives stretch far less; sung F0 histograms show discrete note peaks speech lacks.** Sharma, Gao, Vijayan, Tian & Li 2021 (NHSS, arXiv:2012.00337). Implication: speech-TTS duration/F0 cannot be copied onto lyrics; vowels occupy the note, consonants stay short.

10. **XiaoiceSing concatenates MIDI pitch/length with phonemes and predicts *residual* log-F0 around the note; residual F0 won 97.3% A/B vs an independent LSTM F0 model (F0 RMSE 10.45 vs 13.74 Hz).** Lu, Wu, Luan, Tan & Zhou 2020 (XiaoiceSing, arXiv:2006.06261). Implication: F0 is a residual around the score, not a text-predicted contour as in FastSpeech 2's variance adaptor.

11. **Oracle VITS (speech-style duration) is off-key and unintelligible on singing; VISinger replaces it with a frame-level prior, an F0 predictor, and a duration head that predicts phoneme-to-note duration ratio so frames match the score.** Zhang, Cong, Xue, Xie, Zhu & Bi 2022 (VISinger, arXiv:2110.08813). Implication: speech-TTS phoneme-level variance and free duration fail because within-note F0/vibrato vary at frame rate and rhythm is score-locked.

12. **Sinsy models time-lag (consonants start before the notated onset; vowel onset tracks the beat), then renormalizes phone durations to the adjusted note; log F0 = note pitch + residual; without pitch normalization F0-RMSE jumps from ~74 to 264 cents.** Hono, Hashimoto, Oura, Nankaku & Tokuda 2021 (Sinsy, arXiv:2108.02776). Implication: anticipatory coarticulation is a time-lag around the score, not ToBI phrasing.

13. **NNSVS inherits Sinsy's time-lag/duration pipeline; joint DNNs overweight spectrum vs F0, so multi-stream + autoregressive residual log-F0 is required; a DiffSinger retrain produced discontinuous F0 and unstable vibrato.** Yamamoto, Yoneyama & Toda 2022 (NNSVS, arXiv:2210.15987). Implication: FastSpeech 2-style joint pitch/energy/duration prediction under-models singing F0/vibrato.

14. **High MOS still lacks musicality without explicit performance control (onset deviations, F0 curves, amplitude envelopes from score+style); DiffSinger/VISinger 2 often ingest ground-truth performance MIDI and go out of tune with unstable vibrato on long notes.** Dai, Liu, Valle & Gururani 2024 (ExpressiveSinger, DOI:10.1145/3664647.3681642). Implication: MIDI is the skeleton; performance timing, F0 residual, and dynamics are predicted around it — not from text.

15. **L1/FFT F0 (FastSpeech 2-style) cannot capture technique-dependent contours (vibrato, bubble, glissando); a pitch predictor conditioned on notes+lyrics+technique beats DiffSinger/VISinger 2 on FFE.** Guo et al. 2025 (TechSinger, arXiv:2502.12572). Implication: speech variance-adaptor F0 is the wrong family.

16. **~~Naïve shared melody conditioning causes gradient conflict between speech and singing.~~** Zheng, Xue, Ren, Ding, Liu & Chen 2026 (UniVoice, arXiv:2606.05852). *CANNOT_CONFIRM at the citation gate: arXiv export API returned unresolvable (not read as fabrication). Advisor independently retrieved https://arxiv.org/abs/2606.05852 (title/authors/year match). Per protocol this finding is **out of Step 5** until a human override — C8 does not cite it.* Implication (advisory only): do not reuse speech-TTS prosody as singing melody.

### Lane C — lyric-to-note alignment

17. **Sung tone onset is the vowel, not the consonant; accompanists lock piano attacks to the singer's vowel onset; consonant-to-beat lag ranges about −100 to +300 ms and scales with tempo.** Sundberg & Bauer-Huppmann 2007 (*When Does a Sung Tone Start?*, Journal of Voice, DOI:10.1016/j.jvoice.2006.01.003). Implication: put the vowel nucleus on the MIDI beat; park onset consonants in the preceding inter-onset gap.

18. **English vowel beats sit near mid-vowel; sonorant onsets take earlier beats than stops/fricatives.** Zhang & Zhu 2021 (*Synchronising speech segments with musical beats*, arXiv:2106.10045). Implication: English alignment should fire the nucleus slightly after note-on; late-coda nasals are separate.

19. **Copying speech C/V ratios makes consonants eat the vowel: speech vowel share 52–75% would force 2.5–5 s consonants on a 10 s sung syllable; real singing dumps extra length onto the rime (onset consonants max ~0.28 s).** Zhang & Wang 2020 (*Segment Duration and Proportion in Mandarin Singing*, Speech Prosody 2020; https://www.isca-archive.org/speechprosody_2020/zhang20c_speechprosody.pdf). Implication: freeze onset/coda in a short band; leftover note length goes to the nucleus (diphthong off-glide last).

20. **Speech Montreal Forced Aligner word-boundary error is 25 ms on speech vs 104 ms on singing.** Sharma et al. 2021 (NHSS, arXiv:2012.00337) — same paper as finding 9. Implication: if you force-align, adapt on singing; do not trust speech GMM-HMM boundaries for `PhonemeEvent`s.

21. **MFA labels melisma as silence, which then collides with true rests.** Wu, He, Yuan, Wei, Wei, Lin, Xu & Lin 2024 (SongTrans, arXiv:2409.14619). Implication: rest-as-breath vs melisma cannot be inferred from energy; slur/tie flags (or an explicit note-count head) are required.

22. **Fine-grained SVS corpora force MFA then *manual* phoneme/note edits because one vowel may span multiple notes; RMSSinger replaces that with word-level hard-alignment + learned Gaussian upsampling.** He, Liu, Ye, Huang, Cui, Liu & Zhao 2023 (RMSSinger, ACL 2023 Findings; https://aclanthology.org/2023.findings-acl.16/). Implication: prefer syllable/word→note maps (slurs for melisma) over phone-level forced alignment unless you will hand-correct.

23. **Wave-U-Net+CTC lyrics-to-*audio* alignment (~0.35 s mean word error) is not lyrics-to-MIDI.** Stoller, Durand & Ewert 2019 (arXiv:1902.06797). DiffSinger (Liu et al. 2022, arXiv:2105.02446) still uses MFA then a length regulator. Implication: CTC/attention recovers timestamps from recordings; synthesis from MIDI should stay score-constrained.

### Lane D — SVS vs lyrics-to-song (the route table)

24. **DiffSinger is score-conditioned SVS (lyrics+pitch+duration → mel), not a song generator; a MIDI-B path exists in the official repo.** Liu, Li, Ren, Chen & Zhao 2022 (DiffSinger, arXiv:2105.02446). MOS 3.85±0.11; shallow-diffusion RTF 0.191. Code MIT; OpenVPI fork Apache 2.0. Failure (NNSVS re-run): discontinuous F0 / unstable vibrato, MOS 2.90. Implication: this family can take MIDI as an acoustic condition; render is offline.

25. **NNSVS + WORLD: phone durations renormalized to note length (hard score lock); residual log-F0 against MIDI pitch; toolkit MIT; WORLD modified-BSD; authors report RTF low enough for real time; MOS 3.86±0.10 vs recordings 4.39.** Yamamoto et al. 2022 (arXiv:2210.15987) + Morise, Yokomori & Ozawa 2016 (DOI:10.1587/transinf.2015EDP7457). Implication: source-filter SVS remains the only local real-time score-locked path with permissive licenses.

26. **VISinger 2 takes lyrics + musical score; predicted F0 drives a DDSP harmonic oscillator as a hard pitch constraint at inference.** Zhang, Xue, Li, Xie et al. 2022 (arXiv:2211.02903). MOS 3.81±0.14 at 44.1 kHz vs GT 4.32. Official weights not confirmed. Implication: hybrid DSP+neural SVS can keep F0 hard-constrained; lyrics-to-song models do not.

27. **StyleSinger is still notes+lyrics SVS plus a reference clip (MOS 3.90±0.05), trained on M4Singer (CC BY-NC-SA 4.0); authors will impose restrictions on code and models.** Zhang, Huang, Li et al. 2024 (arXiv:2312.10741). Implication: neural SVS can clone style from a clip while keeping notes; published data/weights are not commercial-safe for a public npm tool.

28. **ACE-Step 1.5 is lyrics+caption → mixed song; MIT code and weights; BPM/key/time-sig are metadata, not note MIDI.** Gong, Song, Zhao et al. 2026 (arXiv:2602.00744; https://huggingface.co/ACE-Step/Ace-Step1.5). Cover copies melody from *source audio*; Vocal2BGM adds backing to a vocal. Failure: no MIDI-note hard constraint. Implication: commercially licensed local *song generator*, not a singing instrument.

29. **DiffRhythm 2 states SVS "produces vocals with predefined melodies"; song generation does not.** Jiang, Chen, Ning et al. 2025 (arXiv:2510.22950). Code+weights Apache 2.0; lyrics+style in, mixed track out; RTF 0.213 on RTX 4090. v1 VAE is Stability AI Community License ($1M revenue cap). Implication: v2 weights are Apache; cannot honor MIDI.

30. **YuE is lyrics-to-song (Apache 2.0); dual-track ICL can change lyrics while preserving accompaniment *audio*; MIDI is not an input; BPM control was removed.** Yuan, Lin, Guo et al. 2025 (arXiv:2503.08638). ~30 s audio ≈ 360 s on RTX 4090. Implication: can restyle over an existing mix; cannot sing a supplied MIDI line.

31. **so-vits-svc converts a dry vocal (SoftVC content + F0) into a cloned singer; F0 comes from the source recording, not MIDI; license AGPL-3.0.** innnky / SVC community (https://github.com/innnky/so-vits-svc). Implication: SVC can retimbre a DSP/MIDI-driven dry vocal; MIDI control stays upstream; AGPL is a ship-blocker for the public package unless isolated.

### Lane E — evaluation and teaching HCI

32. **MUSHRA (ITU-R BS.1534-3) is for intermediate impairments; hidden reference and 3.5/7 kHz anchors are listener-screening tools, not optional UI.** ITU 2015 (https://www.itu.int/rec/R-REC-BS.1534). Exclude a listener who scores the hidden reference <90 on >15% of items. Implication: a synth-vocal admission panel that omits hidden-reference screening and loudness alignment will pass loud/smooth systems, not better singers. (Jam-sessions already has this floor for accompaniment voicings — reuse it, do not invent a speech-MOS gate.)

33. **Sung quality is not one MOS: lyrics intelligibility, melody/pitch, and overall are separately rated; speech MOS predictors (UTMOS/DNSMOS) correlate poorly with singing.** Tang, Liu, Feng, Zhao, Han, Yu, Shi & Jin 2026 (SingMOS-Pro, arXiv:2510.01812). Implication: an admission gate must score lyrics and pitch-to-score separately; a speech MOS number is not a vocal-quality ticket.

34. **Canonical SVS listening tests split pronunciation MOS from quality; objective companions are F0 RMSE/CORR, duration RMSE/CORR, MCD, V/UV error.** Lu et al. 2020 (XiaoiceSing, arXiv:2006.06261) — same paper as finding 10. Implication: pitch-to-score and lyric accuracy are admission axes; a single "naturalness" MOS hides off-key or unintelligible singing.

35. **Without pitch-normalization to the score, F0 error explodes (~74 vs ~264 cents) and listeners hear the wrong notes.** Hono et al. 2021 (Sinsy, arXiv:2108.02776) — same paper as finding 12. Implication: score-relative F0 error in *cents*, not absolute Hz, is the pitch admission metric.

36. **ASR WER, raw pitch accuracy (RPA), speaker-embedding SIM, and CMOS are the current SVS battery — and objective pitch/rhythm can invert subjective score-following.** Chen, Wang, Mu, Yang & Chng 2026 (VocalRender, arXiv:2607.27768). SoulX-Singer won objective RPA/IOU; VocalRender won MS-MOS (2.96) and N-CMOS. Implication: do not admit a vocal on RPA/MCD alone; CMOS vs a human hidden reference is the perceptual check.

37. **An LLM singing-coach (dialog + compare-to-human-demo + journals) raised metacognition, not singing scores, vs ordinary lessons; metacognition did not predict performance.** Li, Cui, Manoharan, Dai, Liu & Huang 2025 (*Front. Psychol.* 16:1598867, PMC12400964). The "AI" was a chatbot plus teacher-demo comparison, not a synthetic singer. Implication: coaching-layer evidence does not license a model-as-singer.

38. **Poor-pitch singers match themselves far better than other voices; a "perfect" other singer is the hard case (inverse-model deficit).** Pfordresher & Mantell 2014 (*Cognition and singing*, *Cogn. Psychol.* 70:31–57, DOI:10.1016/j.cogpsych.2013.12.005). Self-advantage survives timbre controls and transposition; larger for poor-pitch singers (criterion ±50 cents). Implication: a high-MOS synth of a different identity is a worse pitch-matching model than the learner's own voice.

39. **Vocal-model identity (register/timbre) changes children's pitch-matching accuracy: child > adult female > adult male.** Green 1990 (*J. Res. Music Educ.* 38:225–231, DOI:10.2307/3345186). Implication: even a high-quality synth singer is the wrong tutor if its register/timbre is far from the learner; accompaniment doubling is not a substitute for a matched vocal model.

---

## Architectural connection (findings → route)

Each load-bearing choice traces to ≥1 finding. This is the advisor recommendation, not a ship order.

**C1. Do not treat ACE-Step / DiffRhythm / YuE as the jam-sessions vocal engine.** They are mixed-song generators; BPM/key are metadata, MIDI notes are not a hard constraint (28, 29, 30). They stay in model-knowledge audio as a *side door* (generate a reference track, then stem) — never as `play --engine vocal` over a library MIDI.

**C2. Keep MIDI + lyrics as a hard score floor; models write residuals only.** Speech-TTS variance adaptors, ToBI, and free duration fail on singing (9–16, 11). F0 = note + residual (10, 12, 13). Duration = time-lag + renormalize phones to the note (12, 19). This is already the `VocalScore` shape in vocal-synth-engine — the missing work is *using* lyrics/phonemes, not inventing a new score format.

**C3. Alignment is deterministic-from-score, not speech-MFA.** Vowel nucleus on the beat, consonants in the inter-onset gap, leftover ticks into the nucleus, diphthongs split on long notes, slurs for melisma, rests ≠ silence-as-melisma (17–23). The existing CMU-dict G2P is necessary and not sufficient (3, 19).

**C4. Vocology constraints bind the DSP engines we already have.** Separate LF-like source from tract filter (1, 2); glottal aspiration noise (8); formant tracking when F0 > speech F1 (4, 5); register as glottal shape, not transpose (6); phrase-moving vibrato, not a constant LFO (7); singer's formant only if we want male ring (3). Today's `noteOn` into a fixed SATB tract is the Joliveau/Titze failure mode.

**C5. Two runtime paths, one contract.** (a) **Real-time instrument** — extend tract + additive engines under C2–C4; NNSVS+WORLD is the cited real-time score-locked family with permissive licenses (25). (b) **Offline neural SVS render** — DiffSinger/OpenVPI (MIT/Apache) or VISinger 2 *if* weights are confirmed commercial-safe (24, 26). StyleSinger / M4Singer are NC — do not ship (27). so-vits-svc is AGPL and F0-from-audio — optional isolated timbre lane, not the public package (31).

**C6. Admission is not speech MOS.** Score-relative F0 cents + lyrics/pronunciation MOS + MUSHRA-style hidden-ref panel already used for the composition panel (32–36). Loudness-match. Do not gate on UTMOS.

**C7. Model-as-singer ≠ model-as-coach.** A high-MOS lead vocal of another identity can *hurt* pitch matching (38, 39). Spoken teaching TTS (ROADMAP) is a separate surface (37). If we ship a practice vocal, default to a register/timbre near the learner — or the learner's own voice — not an operatic SATB demo.

**C8. Spoken TTS and sung vocals do not share a prosody stack** (9–15). Kokoro/Chatterbox (already in model-knowledge) can serve C7's coach lane; they must not drive the singer's F0. (Finding 16 / UniVoice is retrieval-confirmed out of band but **out of this connection** until the arXiv-export CANNOT_CONFIRM is overridden.)

---

## Route options for the Director

| Route | What it is | Honors library MIDI? | Real-time? | License for public npm | First slice | Findings |
|---|---|---|---|---|---|---|
| **A. Score-locked DSP singer** | Wire lyrics → G2P → `PhonemeEvent`s; vowel-on-beat; LF source + formant tracking + residual vibrato on tract/additive | Yes, by construction | Yes | MIT (ours) | 8–16 bars of one English song, aah vs lyric A/B | C2–C4, 1–8, 17–19, 25 |
| **B. Offline neural SVS** | DiffSinger/OpenVPI (or VISinger 2 if weights clear) renders a vocal stem against the MIDI, mix with piano | Yes, if MIDI-B / score path is used | No (RTF ~0.2) | MIT/Apache code; **weights must be re-checked** | Same 8–16 bars, MOS split lyrics vs pitch | 24, 26, 27 |
| **C. Full-song generator** | ACE-Step 1.5 / DiffRhythm 2 / YuE | **No** | Offline | MIT / Apache | Do not use as the play engine | 28–30 |
| **D. DSP dry + SVC timbre** | A or NNSVS dry vocal → so-vits-svc | Yes (upstream) | Maybe | **AGPL** | Isolated experiment only | 31 |
| **E. Coach only (no singer)** | Spoken teaching TTS + solfege text; no sung lyrics | n/a | Yes | MIT TTS (Chatterbox/Kokoro) | ROADMAP spoken teaching | 37–39, 16 |

**Advisor ranking (not a ship):** **A first**, because the score contract already exists and vocology says the current engines fail in *named* ways we can fix without a new model family. **B as an optional render** once a commercial-safe checkpoint is pinned. **C is a different product** (already in model-knowledge). **E stays on the roadmap and must not share F0 code with A.** Do not start A or B inside the closed Phase 9 swarm; this is a new product layer with its own kickoff.

Honest ceiling: we did not retrieve a direct adult RCT of "perfect synth lead vs no lead" on pitch learning (lane E retrieval notes). C7 is grounded in self-vs-other matching (38) and model-identity (39), not that missing RCT.

---

## What this wave does *not* do

- No product code in `ai-jam-sessions` or `vocal-synth-engine`.
- No new model rows in model-knowledge (ACE-Step / DiffRhythm / YuE / Kokoro already live there).
- No SQLite ingest yet — schema/loadout for this KB is a follow-on if the Director keeps vocology as its own KB rather than a model-knowledge audio append.
