# Music is a seconds grid, not a prompt
_auto-created from wave lane_ · wave 15 · 2026-10-20 · [‹ catalog index](README.md)

11 findings · 11 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| A brief generated from the hymn data rather than written by hand | ai-jam-sessions (mcp-tool-shop-org) · 2026 | scripts/arrange-hymn.ts builds the brief from the hymn's own data: the melody bar by bar in LilyPond absolute pitches with chords per beat, every stanza, the form (introduction, one pass per stanza, coda), a texture plan, and the checkable rules. America the Beautiful's brief was generated this way, and its answer compiled as returned. Amazing Grace's brief was written by hand before the script existed: it asked for a \partial 4 at the start, so its MIDI import needed an offset of 768 ticks, and its answer needed the one hand fix. The comparison is one generated brief against one hand-written brief. | ✓ |
| ChatMusician | Yuan et al. · 2024 | ChatMusician continually pre-trains LLaMA2 on ABC notation and argues for ABC over MIDI tokens on compression rate and because MIDI tokenization introduces quantization errors and unstable rhythms. The paper never mentions Python, never measures representation validity head-to-head, and makes no claim about free audio prompts. | ✓ |
| Intuitive Analysis of Song Structure | Raffel & Ellis · 2014 | pretty_midi exists because MIDI ticks are unusable in Python; notes are pitch + start + end in seconds. | ✓ |
| Piano arrangements written in LilyPond by a reasoning model and accepted by machine gates | ai-jam-sessions (mcp-tool-shop-org) · 2026 | Kimi-K3 (moonshotai/kimi-k3 on OpenRouter, temperature 0, reasoning effort high) wrote complete solo-piano arrangements of Amazing Grace and America the Beautiful in LilyPond: an introduction, one pass per stanza with a texture that builds from verse to verse, and a coda. Three machine gates decided acceptance: LilyPond 2.24 compiles the file with no error or warning; a MIDI import finds every verse's melody in the piano at its written time; and the score clock refuses any sung note with no piano note under it. Both arrangements passed all three (one after a recorded one-line fix), and the Director approved both recordings by ear on 2026-10-08. | ✓ |
| REMI | Huang & Yang · 2020 | REMI (Pop Music Transformer, Huang & Yang 2020) imposes a beat-bar metrical structure on the token stream and reports better rhythmic structure than grid-free Transformer baselines. The paper says nothing about singing-voice models or phoneme x MIDI x duration inputs. | ✓ |
| Rights: model and provider terms that leave a hymn arrangement free to dedicate CC0 | ai-jam-sessions (mcp-tool-shop-org) · 2026 | The Kimi K3 License grants and conditions the Software (the weights, code and documentation) and asserts no ownership of the model's outputs; its display requirement (section 3) applies only to large commercial products built on the model. OpenRouter's Terms take only a non-exclusive licence in content passed through the service (sections 5.8, 6.1 and 6.2). The hymns' tunes and texts are in the public domain: every edition followed dates from 1919 or earlier, every author died before 1930, and each brief carries the hymn's own melody and chords, not a modern harmonisation. The studio dedicated both arrangements CC0. | ✓ |
| Small syntax slips: two of three model-written arrangements needed a one-line fix | ai-jam-sessions (mcp-tool-shop-org) · 2026 | Of the three hymn arrangements the studio has had a model write, two needed a one-line fix before LilyPond 2.24 would compile them. Amazing Grace wrote \key g major without the backslash before the mode, twice. The Battle Hymn (arranged on 2026-09-26 by an earlier route, before arrange-hymn.ts) left out \language "english". America the Beautiful compiled as returned. Each fix is written into the arrangement's record. | ✓ |
| Standard MIDI Files 1.1 | International MIDI Association (original text distribution), updated by David Back, (c)1999 - not the MMA · 1996 | SMF times a sung line as integer ticks × microseconds-per-quarter, not BPM. | ✓ |
| What an arrangement costs: output tokens, most of them reasoning | ai-jam-sessions (mcp-tool-shop-org) · 2026 | Amazing Grace: 1,728 prompt tokens and 19,510 completion tokens, 13,023 of them reasoning; $0.298; 196 s. America the Beautiful: 1,956 prompt tokens and 67,147 completion tokens, 36,692 of them reasoning; $1.013; 528 s. Both calls were served by the provider Modal and billed at $3.00 per million input tokens and $15 per million output tokens. Completion tokens were over 98% of each bill, and reasoning was 55-67% of the completion. With max_tokens at 200,000 the worst case is about $3.00; the script prints that estimate and spends only when run with --yes. | ✓ |
| librosa: Audio and Music Signal Analysis in Python | McFee et al. · 2015 | librosa analyzes audio; it does not specify a score. | ✓ |
| music21: A Toolkit for Computer-Aided Musicology | Cuthbert & Ariza · 2010 | music21 is the Python object graph of a score. | ✓ |

## Detail

### A brief generated from the hymn data rather than written by hand · `load-bearing`
**scripts/arrange-hymn.ts builds the brief from the hymn's own data: the melody bar by bar in LilyPond absolute pitches with chords per beat, every stanza, the form (introduction, one pass per stanza, coda), a texture plan, and the checkable rules. America the Beautiful's brief was generated this way, and its answer compiled as returned. Amazing Grace's brief was written by hand before the script existed: it asked for a \partial 4 at the start, so its MIDI import needed an offset of 768 ticks, and its answer needed the one hand fix. The comparison is one generated brief against one hand-written brief.**
- **Implication:** Generate the brief from the same data the score clock reads, so the model is told exactly what the gates will check. With one arrangement each way, treat 'a generated brief compiles cleaner' as directional until more hymns go through the script.
- **Identifier:** `ai-jam-sessions scripts/arrange-hymn.ts`
- **Verify:** Amazing Grace meta.json brief_note (2026-10-13): written by hand before arrange-hymn.ts, \partial 4, import offset 768 ticks. America the Beautiful meta.json: fixes empty.
- **Sources:** [A brief generated from the hymn data rather than written by hand](https://github.com/mcp-tool-shop-org/ai-jam-sessions/blob/main/scripts/arrange-hymn.ts)

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

### Piano arrangements written in LilyPond by a reasoning model and accepted by machine gates · `load-bearing`
**Kimi-K3 (moonshotai/kimi-k3 on OpenRouter, temperature 0, reasoning effort high) wrote complete solo-piano arrangements of Amazing Grace and America the Beautiful in LilyPond: an introduction, one pass per stanza with a texture that builds from verse to verse, and a coda. Three machine gates decided acceptance: LilyPond 2.24 compiles the file with no error or warning; a MIDI import finds every verse's melody in the piano at its written time; and the score clock refuses any sung note with no piano note under it. Both arrangements passed all three (one after a recorded one-line fix), and the Director approved both recordings by ear on 2026-10-08.**
- **Implication:** A model can write the accompaniment as code, but the gates accept it, not the model. Put rules in the brief that a machine can check (the melody as the top voice at its written time in every pass; no \partial after the start; no pedal marks, repeats, tuplets or \ottava), so a failure is a measured miss rather than a matter of taste. Keep the brief, the system prompt, the raw answer, the compiled .ly and a meta.json (sha256 of each, generation id, usage, cost, any hand fix) per arrangement.
- **Identifier:** `ai-jam-sessions PR 109`
- **Verify:** PR 109 merged 2026-10-08; both meta.json files read 2026-10-13: temperature 0, reasoning high, finish_reason stop. Director's approval by ear is recorded on the PR and in rnd.
- **Sources:** [Piano arrangements written in LilyPond by a reasoning model and accepted by machine gates](https://github.com/mcp-tool-shop-org/ai-jam-sessions/pull/109)

### REMI · `load-bearing`
**REMI (Pop Music Transformer, Huang & Yang 2020) imposes a beat-bar metrical structure on the token stream and reports better rhythmic structure than grid-free Transformer baselines. The paper says nothing about singing-voice models or phoneme x MIDI x duration inputs.**
- **Implication:** sing in 35 seconds has nothing to scale.
- **Identifier:** `arXiv:2002.00212`
- **Verify:** arXiv:2002.00212 is "Pop Music Transformer" (Huang & Yang, ACM MM 2020); REMI is the representation it introduces and the beat-bar-grid rationale checks out. The singing-model phoneme x MIDI x duration half is absent.
- **Sources:** [REMI](https://arxiv.org/abs/2002.00212)

### Rights: model and provider terms that leave a hymn arrangement free to dedicate CC0 · `load-bearing`
**The Kimi K3 License grants and conditions the Software (the weights, code and documentation) and asserts no ownership of the model's outputs; its display requirement (section 3) applies only to large commercial products built on the model. OpenRouter's Terms take only a non-exclusive licence in content passed through the service (sections 5.8, 6.1 and 6.2). The hymns' tunes and texts are in the public domain: every edition followed dates from 1919 or earlier, every author died before 1930, and each brief carries the hymn's own melody and chords, not a modern harmonisation. The studio dedicated both arrangements CC0.**
- **Implication:** A model-written arrangement of a public-domain hymn can ship CC0 when the model licence claims no rights in outputs, the provider's licence in content is non-exclusive, and the brief carries only public-domain material. Check all three for each model and each hymn, because terms change. This records what the terms say; it is not legal advice.
- **Identifier:** `Kimi K3 License; OpenRouter Terms`
- **Verify:** Kimi K3 LICENSE re-read at source 2026-10-13: no output ownership clause; section 3 display duty is for large commercial products. OpenRouter Terms and editions checked at source 2026-10-08.
- **Sources:** [Rights: model and provider terms that leave a hymn arrangement free to dedicate CC0](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE)

### Small syntax slips: two of three model-written arrangements needed a one-line fix · `load-bearing`
**Of the three hymn arrangements the studio has had a model write, two needed a one-line fix before LilyPond 2.24 would compile them. Amazing Grace wrote \key g major without the backslash before the mode, twice. The Battle Hymn (arranged on 2026-09-26 by an earlier route, before arrange-hymn.ts) left out \language "english". America the Beautiful compiled as returned. Each fix is written into the arrangement's record.**
- **Implication:** Expect small syntax slips even when the music is right. The compile gate catches them, and a recorded one-line fix is cheaper than a second call. Keep the fix in meta.json, so the published file and the model's answer differ only by what is written down.
- **Identifier:** `ai-jam-sessions arrangement meta.json; rnd 2026-10-08`
- **Verify:** Amazing Grace meta.json fixes: the \key mode backslash, twice; America fixes empty (2026-10-13). Battle Hymn fix per rnd, checked on 2026-10-08 against the published file.
- **Sources:** [Small syntax slips: two of three model-written arrangements needed a one-line fix](https://github.com/mcp-tool-shop-org/ai-jam-sessions/blob/main/src/vocal/arrangements/source/amazing-grace-kimi-k3/meta.json)

### Standard MIDI Files 1.1 · `load-bearing`
**SMF times a sung line as integer ticks × microseconds-per-quarter, not BPM.**
- **Implication:** startSec is the integral of that map; a duration sentence in a prompt is not a clock.
- **Identifier:** `MMA RP-001 v1.0 'Standard MIDI Files 1.0' (96-1-4) is the normative spec; 'Standard MIDI-File Format Spec. 1.1, updated' is an unofficial IMA/David Back reformatting`
- **Verify:** Timing claim holds verbatim: "FF 51 03 tttttt Set Tempo (in microseconds per MIDI quarter-note)"; division bits 14-0 are ticks per quarter-note. But the MMA publishes RP-001 v1.0 "Standard MIDI Files 1.0" - no MMA 1.1 exists.
- **Sources:** [Standard MIDI Files 1.1](https://midimusic.github.io/tech/midispec.html)

### What an arrangement costs: output tokens, most of them reasoning · `load-bearing`
**Amazing Grace: 1,728 prompt tokens and 19,510 completion tokens, 13,023 of them reasoning; $0.298; 196 s. America the Beautiful: 1,956 prompt tokens and 67,147 completion tokens, 36,692 of them reasoning; $1.013; 528 s. Both calls were served by the provider Modal and billed at $3.00 per million input tokens and $15 per million output tokens. Completion tokens were over 98% of each bill, and reasoning was 55-67% of the completion. With max_tokens at 200,000 the worst case is about $3.00; the script prints that estimate and spends only when run with --yes.**
- **Implication:** Budget an arrangement as max_tokens times the output price; the brief costs under a cent. A longer hymn costs more in reasoning, not in input. Record the usage block from the provider in meta.json, because the per-token price depends on which provider serves the call.
- **Identifier:** `ai-jam-sessions arrangement meta.json`
- **Verify:** meta.json usage, both arrangements, read 2026-10-13. Input rate derived from cost_details: 0.005184/1728 and 0.005868/1956 = $3.00 per million. rnd's $0.72 input figure did not apply.
- **Sources:** [What an arrangement costs: output tokens, most of them reasoning](https://github.com/mcp-tool-shop-org/ai-jam-sessions/blob/main/src/vocal/arrangements/source/america-the-beautiful-kimi-k3/meta.json)

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

