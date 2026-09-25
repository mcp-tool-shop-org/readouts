# Music is a seconds grid, not a prompt
_auto-created from wave lane_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

6 findings · 6 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| ChatMusician | Yuan et al. · 2024 | ChatMusician continually pre-trains LLaMA2 on ABC notation and argues for ABC over MIDI tokens on compression rate and because MIDI tokenization introduces quantization errors and unstable rhythms. The paper never mentions Python, never measures representation validity head-to-head, and makes no claim about free audio prompts. | ✓ |
| Intuitive Analysis of Song Structure | Raffel & Ellis · 2014 | pretty_midi exists because MIDI ticks are unusable in Python; notes are pitch + start + end in seconds. | ✓ |
| REMI | Huang & Yang · 2020 | REMI (Pop Music Transformer, Huang & Yang 2020) imposes a beat-bar metrical structure on the token stream and reports better rhythmic structure than grid-free Transformer baselines. The paper says nothing about singing-voice models or phoneme x MIDI x duration inputs. | ✓ |
| Standard MIDI Files 1.1 | International MIDI Association (original text distribution), updated by David Back, (c)1999 - not the MMA · 1996 | SMF times a sung line as integer ticks × microseconds-per-quarter, not BPM. | ✓ |
| librosa: Audio and Music Signal Analysis in Python | McFee et al. · 2015 | librosa analyzes audio; it does not specify a score. | ✓ |
| music21: A Toolkit for Computer-Aided Musicology | Cuthbert & Ariza · 2010 | music21 is the Python object graph of a score. | ✓ |

## Detail

### ChatMusician · `load-bearing`
**ChatMusician continually pre-trains LLaMA2 on ABC notation and argues for ABC over MIDI tokens on compression rate and because MIDI tokenization introduces quantization errors and unstable rhythms. The paper never mentions Python, never measures representation validity head-to-head, and makes no claim about free audio prompts.**
- **Implication:** Python emits chords/beats/seconds; the model fills timbre.
- **Identifier:** `arXiv:2402.16153`
- **Verify:** arXiv:2402.16153, Yuan et al. 2024, real. ABC-over-MIDI rationale is in s2.2 ("quantization errors and unstable rhythms when being tokenized"). But "Python" occurs 0 times in the full text, and no audio-prompt claim appears.
- **Sources:** [ChatMusician](https://arxiv.org/abs/2402.16153)

### Intuitive Analysis of Song Structure · `load-bearing`
**pretty_midi exists because MIDI ticks are unusable in Python; notes are pitch + start + end in seconds.**
- **Implication:** jam-sessions ScoreNote.startSec is already the lingua franca.
- **Identifier:** `Raffel & Ellis, 'Intuitive Analysis, Creation and Manipulation of MIDI Data With pretty_midi', 15th ISMIR 2014, Late-Breaking/Demo LBD29`
- **Verify:** Title is mangled - the real paper is about MIDI data, not song structure. The claim itself holds: ticks make "interpretation in terms of absolute time (in seconds) difficult"; docs confirm Note(velocity, pitch, start, end) in seconds.
- **Sources:** [Intuitive Analysis of Song Structure](https://colinraffel.com/publications/ismir2014intuitive.pdf)

### REMI · `load-bearing`
**REMI (Pop Music Transformer, Huang & Yang 2020) imposes a beat-bar metrical structure on the token stream and reports better rhythmic structure than grid-free Transformer baselines. The paper says nothing about singing-voice models or phoneme x MIDI x duration inputs.**
- **Implication:** sing in 35 seconds has nothing to scale.
- **Identifier:** `arXiv:2002.00212`
- **Verify:** arXiv:2002.00212 is "Pop Music Transformer" (Huang & Yang, ACM MM 2020); REMI is the representation it introduces and the beat-bar-grid rationale checks out. The singing-model phoneme x MIDI x duration half is absent.
- **Sources:** [REMI](https://arxiv.org/abs/2002.00212)

### Standard MIDI Files 1.1 · `load-bearing`
**SMF times a sung line as integer ticks × microseconds-per-quarter, not BPM.**
- **Implication:** startSec is the integral of that map; a duration sentence in a prompt is not a clock.
- **Identifier:** `MMA RP-001 v1.0 'Standard MIDI Files 1.0' (96-1-4) is the normative spec; 'Standard MIDI-File Format Spec. 1.1, updated' is an unofficial IMA/David Back reformatting`
- **Verify:** Timing claim holds verbatim: "FF 51 03 tttttt Set Tempo (in microseconds per MIDI quarter-note)"; division bits 14-0 are ticks per quarter-note. But the MMA publishes RP-001 v1.0 "Standard MIDI Files 1.0" - no MMA 1.1 exists.
- **Sources:** [Standard MIDI Files 1.1](https://midimusic.github.io/tech/midispec.html)

### librosa: Audio and Music Signal Analysis in Python · `load-bearing`
**librosa analyzes audio; it does not specify a score.**
- **Implication:** DSP features recover a performance; they cannot author New Britain.
- **Identifier:** `SciPy 2015`
- **Verify:** SciPy 2015 proceedings PDF (14th Python in Science Conf): McFee, Raffel, Liang, Ellis, McVicar, Battenberg, Nieto. Abstract scopes it as "a Python package for audio and music signal processing" / MIR functions - no score layer.
- **Sources:** [librosa: Audio and Music Signal Analysis in Python](https://proceedings.scipy.org/articles/Majora-7b98e3ed-003.pdf)

### music21: A Toolkit for Computer-Aided Musicology · `load-bearing`
**music21 is the Python object graph of a score.**
- **Implication:** Python Streams, not SuperCollider or MIDI hex, are what an LLM emits correctly.
- **Identifier:** `ISMIR 2010`
- **Verify:** ISMIR 2010 proceedings PDF: Cuthbert & Ariza (MIT); full title adds "and Symbolic Music Data". Abstract: "an object-oriented toolkit for analyzing, searching, and transforming music in symbolic (score-based) forms" - claim supported.
- **Sources:** [music21: A Toolkit for Computer-Aided Musicology](http://ismir2010.ismir.net/proceedings/ismir2010-108.pdf)

