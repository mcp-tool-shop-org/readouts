# Musical vs speech prosody
_Duration, F0, and prosody differences that break speech-TTS copied onto lyrics_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

8 findings · 7 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| ExpressiveSinger | Dai, Liu, Valle & Gururani · 2024 | High MOS still lacks musicality without explicit performance control of onset deviations, F0 curves, and amplitude envelopes from score+style. | ✓ |
| NHSS: A Speech and Singing Parallel Database | Sharma, Gao, Vijayan, Tian & Li · 2021 | Sung English vowels average 830.5 ms vs 148.0 ms spoken (~5.6×); sung F0 histograms show discrete note peaks speech lacks. | ✓ |
| NNSVS | Yamamoto, Yoneyama & Toda · 2022 | Joint DNNs overweight spectrum vs F0; DiffSinger retrain produced discontinuous F0 and unstable vibrato. | ✓ |
| Sinsy | Hono, Hashimoto, Oura, Nankaku & Tokuda · 2021 | Time-lag model: consonants start before notated onset; vowel onset tracks the beat; without pitch-norm F0-RMSE jumps ~74 to 264 cents. | ✓ |
| TechSinger | Guo et al. · 2025 | L1/FFT F0 cannot capture technique-dependent contours; a pitch predictor conditioned on notes+lyrics+technique beats DiffSinger/VISinger 2 on FFE. | ✓ |
| UniVoice | Zheng, Xue, Ren, Ding, Liu & Chen · 2026 | Naïve shared melody conditioning causes gradient conflict (speech PER 12.31%/singing 23.45% vs 5.26%/16.22% with factorization). | ✓ |
| XiaoiceSing | Lu, Wu, Luan, Tan & Zhou · 2020 | Residual log-F0 around MIDI notes won 97.3% A/B vs independent LSTM F0 (RMSE 10.45 vs 13.74 Hz). | ✓ |
| VISinger | Zhang, Cong, Xue, Xie, Zhu & Bi · 2022 | Oracle VITS with speech-style duration is off-key and unintelligible on singing; VISinger uses frame-level prior + phoneme-to-note duration ratio. | · |

## Detail

### ExpressiveSinger · `load-bearing`
**High MOS still lacks musicality without explicit performance control of onset deviations, F0 curves, and amplitude envelopes from score+style.**
- **Implication:** MIDI is the skeleton; performance is predicted around it.
- **Identifier:** `DOI:10.1145/3664647.3681642`
- **Verify:** Crossref on 10.1145/3664647.3681642: Dai, Liu, Valle, Gururani; ACM MM 2024, pp.3229-3238. Paper generates performance control signals - phoneme timing, F0 curves, amplitude envelopes - against a stated musicality gap at high audio quality.
- **Sources:** [ExpressiveSinger](https://doi.org/10.1145/3664647.3681642)

### NHSS: A Speech and Singing Parallel Database · `load-bearing`
**Sung English vowels average 830.5 ms vs 148.0 ms spoken (~5.6×); sung F0 histograms show discrete note peaks speech lacks.**
- **Implication:** Speech-TTS duration/F0 cannot be copied onto lyrics.
- **Identifier:** `arXiv:2012.00337`
- **Verify:** ar5iv arXiv:2012.00337 Table 10: sung vowels 830.5 ms vs spoken 148.0 ms. Sung F0 histograms show prominent peaks where speech is relatively flat. arXiv v1 is Dec 2020; 2021 is the Speech Communication version, so the year stands.
- **Sources:** [NHSS: A Speech and Singing Parallel Database](https://arxiv.org/abs/2012.00337)

### NNSVS · `load-bearing`
**Joint DNNs overweight spectrum vs F0; DiffSinger retrain produced discontinuous F0 and unstable vibrato.**
- **Implication:** Keep F0 as its own residual stream.
- **Identifier:** `arXiv:2210.15987`
- **Verify:** ar5iv arXiv:2210.15987 Sec 3.3.2: a DNN tends to prioritize higher dimensional spectral features over F0. Sec 4.3, on the retrained DiffSinger: discontinuous F0 and unstable vibrato. Verbatim match to the claim.
- **Sources:** [NNSVS](https://arxiv.org/abs/2210.15987)

### Sinsy · `load-bearing`
**Time-lag model: consonants start before notated onset; vowel onset tracks the beat; without pitch-norm F0-RMSE jumps ~74 to 264 cents.**
- **Implication:** Anticipatory coarticulation is a time-lag around the score, not ToBI.
- **Identifier:** `arXiv:2108.02776`
- **Verify:** ar5iv arXiv:2108.02776 Table II: F0-RMSE 74.00 cents vs 264.07 without pitch normalisation. Text: humans begin consonants earlier than the note onset, and vowel onset timing is closest to the note timing in the score.
- **Sources:** [Sinsy](https://arxiv.org/abs/2108.02776)

### TechSinger · `load-bearing`
**L1/FFT F0 cannot capture technique-dependent contours; a pitch predictor conditioned on notes+lyrics+technique beats DiffSinger/VISinger 2 on FFE.**
- **Implication:** Speech variance-adaptor F0 is the wrong family.
- **Identifier:** `arXiv:2502.12572`
- **Verify:** arXiv:2502.12572 HTML: L1-only F0 makes the technique-to-F0 mapping hard; FFE 0.245 beats DiffSinger 0.255 and VISinger2 0.296; FMPP conditions on score+technique+phoneme. Note the contrast is L1 vs flow matching, not FFT.
- **Sources:** [TechSinger](https://arxiv.org/abs/2502.12572)

### UniVoice · `load-bearing`
**Naïve shared melody conditioning causes gradient conflict (speech PER 12.31%/singing 23.45% vs 5.26%/16.22% with factorization).**
- **Implication:** Do not reuse speech-TTS prosody as singing melody.
- **Identifier:** `arXiv:2606.05852`
- **Verify:** arXiv:2606.05852 resolves (Zheng, Xue, Ren, Ding, Liu, Chen; 4 Jun 2026). Table 2 ablation without factorized conditioning: speech PER 12.31%, singing 23.45%, against 5.26%/16.22% for the full model; negative gradient correlation argued.
- **Sources:** [UniVoice](https://arxiv.org/abs/2606.05852)

### XiaoiceSing · `load-bearing`
**Residual log-F0 around MIDI notes won 97.3% A/B vs independent LSTM F0 (RMSE 10.45 vs 13.74 Hz).**
- **Implication:** F0 is a residual around the score, not a text-predicted contour.
- **Identifier:** `arXiv:2006.06261`
- **Verify:** ar5iv full text of arXiv:2006.06261: Table 2 gives F0 RMSE 10.45 vs baseline 13.74 Hz; abstract gives the 97.3% A/B rate, and the baseline is named as a separate LSTM-based F0 model. Authors and year exact.
- **Sources:** [XiaoiceSing](https://arxiv.org/abs/2006.06261)

### VISinger · `directional`
**Oracle VITS with speech-style duration is off-key and unintelligible on singing; VISinger uses frame-level prior + phoneme-to-note duration ratio.**
- **Implication:** Speech-TTS free duration fails because rhythm is score-locked.
- **Identifier:** `arXiv:2110.08813`
- **Verify:** no external verdict — not yet swept
- **Sources:** [VISinger](https://arxiv.org/abs/2110.08813)

