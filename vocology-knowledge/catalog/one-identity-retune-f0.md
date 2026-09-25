# One identity, retune F0 — never 14 people
_auto-created from wave lane_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

1 findings · 1 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| XiaoiceSing | Lu et al. · 2020 | XiaoiceSing residual F0 and DiffSinger MIDI-B condition one model on lyrics+MIDI. | ✓ |

## Detail

### XiaoiceSing · `load-bearing`
**XiaoiceSing residual F0 and DiffSinger MIDI-B condition one model on lyrics+MIDI.**
- **Implication:** score F0 is a residual around one singer, not a new TTS per note.
- **Identifier:** `arXiv:2006.06261`
- **Verify:** arXiv:2006.06261 abstract: 'we add a residual connection in F0 prediction' plus score note pitch/length inputs. DiffSinger MIDI-B confirmed in the official repo changelog (Mar.2 2022) and its Lyric+MIDI->Mel recipe.
- **Sources:** [XiaoiceSing](https://arxiv.org/abs/2006.06261)

