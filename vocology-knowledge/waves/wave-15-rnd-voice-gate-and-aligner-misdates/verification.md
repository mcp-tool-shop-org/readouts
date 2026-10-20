# Wave 15 — verification

**Dispatch:** [`dispatch.md`](dispatch.md)

**Runner:**
- A Sonnet subagent re-read each claim against ai-jam-sessions' committed receipts and code on 2026-10-20.
- The R&D seat then re-read the load-bearing items itself:
  - `voice-gate-eval-2026-10-08/score.txt`;
  - the published Battle Hymn `voice-gate.json`;
  - `vocal_clock.py` lines 645–670;
  - commit 66faa82's message.

It also checked the subagent's reasons for leaving claims out.

**Verifier maturity, stated plainly:** this check reads receipts and code. No second model family reviewed the wave.

## Result

| finding | verdict | checked against |
|---|---|---|
| the voice gate | confirmed with a fix | `scripts/voice_gate.py` lines 36–45; `scores/receipts/battle-hymn-of-the-republic/sung-2026-10-08/voice-gate.json`: voice_mean_sung 0.984, voice_mean_rest 0.09, frame_s 0.01698; `scores/receipts/voice-gate-eval-2026-10-08/score.txt`: 20 noise marks, 3 caught, 6 flags, 3 near a mark (all voice-in-rest, within 1.5 s); ag-pad16, am-pad16, ag-kimi and am-kimi at 0 flags. The bench's 0.98 / 0.08 isn't tied to a committed mix (eval.log line 13 reads 0.981 / 0.078 for an unlabelled run), so the published receipt is cited instead. |
| undating aligner misdates | confirmed with a fix | commit 66faa82's message: 0.7 s late, −42 dB, 3 of 40 phrases (22 of 414 syllables), −22 dB after; `scripts/vocal_clock.py` lines 645–670: DATE_OUTLIER_S 0.3, DATE_NEIGHBOURS 4; commit 5f8d1e2: America 2 of 20, Amazing Grace unaffected; the Battle Hymn receipt dates "jah" at 52.11 s by onset rise. The tempo range is 72–92 bpm, from the score clocks (76, 92, 72). |

## Reasons for leaving claims out, checked

- **17 honks in short gaps:** the explanation is in the docs, but the per-frame `.npz` isn't committed, so where the
  misses fell can't be checked.
- **The gate's running time:** there is no timing receipt.
- **The Director's listening verdict** on the re-picked syllable is left out. What it decided is already on record:
  the fixed vocals were re-published.

**Net:** 2 findings, both confirmed with a fix; 0 fabricated.

**Licences:** pyannote/segmentation-3.0 is MIT and gated (it asks for company or university and website, and may lead
to emails about pyannote's paid services). pyannote-audio is MIT. The aligner work is studio code.
