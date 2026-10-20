# Wave 15 — a voice gate for sung vocals, and undating aligner misdates (promoted from rnd)

**KB** `vocology-knowledge` · **dispatched** 2026-10-20 · **0** research agents (a promotion) · lanes
`singing-assessment`, `lyric-to-note-alignment` · trigger: the readouts promotion queue. It covers two R&D bench entries
from ai-jam-sessions' sung-vocal work of 2026-10-08.

**Headline:**
- A voice gate built on pyannote segmentation checks that a placed vocal sings its notes and stays quiet in rests. Its
  flags are precise, but it catches few short honks: 3 of 20 the Director marked.
- One syllable an aligner dated 0.7 s late was nearly silent in a published vocal. The fix rejects a date far from its
  neighbours and picks that syllable from another take.

## Research grounding

1. **The voice gate** (`scripts/voice_gate.py`, pyannote/segmentation-3.0):
   - It flags voice in a rest, an overlong release, two voices, and silent notes.
   - On the published Battle Hymn vocal, the voice level is 0.984 in sung notes and 0.09 in rests.
   - Scored against the Director's marks on nine takes, it caught 3 of 20 marked honks. All 3 of its voice-in-rest
     flags fell on honk marks, and four takes with no marked noise drew none.
   - **Implication:** a cheap, precise check beside listening, not instead of it.
2. **Aligner misdates:**
   - The onset detector left "jah" at 0:52 undated, and the aligner dated it 0.7 s late on its own fading tail.
     Placement cut the tail, and the syllable came out at −42 dB.
   - `undate_outliers()` now rejects a date more than 0.3 s from the median offset of up to 4 neighbours on each side,
     before and after the aligner fill.
   - Results:
     - Battle Hymn: 3 of 40 phrases re-picked, and "jah" now at −22 dB;
     - America: 2 of 20 phrases re-picked;
     - Amazing Grace: unchanged.
   - **Implication:** a single syllable far from its neighbours is a misdate; a whole take running late is the take.

## What the promotion changed

- **Corrected:** the voice levels are cited from the published Battle Hymn receipt (0.984 and 0.09). The bench's 0.98
  and 0.08 came from an earlier mix that isn't committed.
- **Corrected:** the tempo range the thresholds were set on is 72–92 bpm, not 72–95.
- **Not loaded:**
  - "17 honks missed in short phrase gaps": the per-frame data isn't committed;
  - the gate's running time: no timing receipt;
  - the claim that pitch evidence separates short-gap honks: still unverified;
  - a listening reaction recorded in a commit message.
- **Stated as such:** the misdate's 0.7 s, −42 dB and re-pick counts rest on the fix's commit record, because the
  before-and-after plans aren't committed.

## The honest limit

- Three hymns, one singer voice, one session of marks.
- The gate's recall on short honks is low.
- The aligner thresholds have no tuning receipt.

## Provenance

Promoted from rnd entries
[`2026-10-08-voice-gate-pyannote-segmentation-on-sung-vocals`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-08-voice-gate-pyannote-segmentation-on-sung-vocals.md)
and
[`2026-10-08-aligner-misdates-cause-sung-dropouts`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-08-aligner-misdates-cause-sung-dropouts.md).
See [`verification.md`](verification.md).
