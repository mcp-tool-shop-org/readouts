# Wave 2 — Music as code; Comfy owns timbre (study-swarm)

**KB** `vocology-knowledge` · **dispatched** 2026-09-04 · **5** lanes · trigger: Director — stop local DSP singing; use Comfy Cloud via comfy-mcp; plug the one Kokoro lock into an audio-to-audio transform; prompting + timing from jam-sessions + fx-dub; first research “music as a language you understand (Python).”

Wave 1 locked vocology. Wave 2 locks **representation + Cloud transform**. Local per-note TTS chunks and formant-moving pitch-shift are empirically identity destruction (finding 11).

---

## Research grounding

### Music is a seconds grid, not a prompt

1. **SMF times a sung line as integer ticks × microseconds-per-quarter, not BPM.** MMA 1996 (SMF 1.1). https://midimusic.github.io/tech/midispec.html. Implication: `startSec` is the integral of that map; a duration sentence in a prompt is not a clock.

2. **pretty_midi exists because MIDI ticks are unusable in Python; notes are pitch + start + end in seconds.** Raffel & Ellis 2014 (ISMIR). https://colinraffel.com/publications/ismir2014intuitive.pdf. Implication: jam-sessions `ScoreNote.startSec` is already the lingua franca.

3. **MusicXML/MEI/ABC bind each syllable to a timed note (melisma is a field).** W3C MusicXML 4.0; MEI v4; Walshaw 2011 ABC 2.1 §5. Implication: lyrics are children of notes, not a paragraph under a staff.

4. **music21 is the Python object graph of a score.** Cuthbert & Ariza 2010 (ISMIR). http://ismir2010.ismir.net/proceedings/ismir2010-108.pdf. Implication: Python Streams, not SuperCollider or MIDI hex, are what an LLM emits correctly.

5. **librosa analyzes audio; it does not specify a score.** McFee et al. 2015 (SciPy). https://proceedings.scipy.org/articles/Majora-7b98e3ed-003.pdf. Implication: DSP features recover a performance; they cannot author New Britain.

6. **LLMs emit more valid music as Python/ABC than as MIDI-like tokens; free audio prompts fail the grid.** Yuan et al. 2024 ChatMusician (arXiv:2402.16153); Zhang et al. 2024 (arXiv:2409.00856); Melechovsky et al. 2024 Mustango (arXiv:2311.08355). Implication: Python emits chords/beats/seconds; the model fills timbre.

7. **Without a beat-bar grid, sequence models drift; singing models consume phoneme × MIDI × duration.** Huang & Yang 2020 REMI (arXiv:2002.00212); Chen et al. 2020 HiFiSinger (arXiv:2009.01776). Implication: “sing in 35 seconds” has nothing to scale.

### One identity, retune F0 — never 14 people

8. **WORLD / STRAIGHT / TD-PSOLA retune F0 of one utterance; timbre lives in the envelope.** Morise et al. 2016 WORLD; Saitou et al. 2007 STS; Moulines & Charpentier 1990 TD-PSOLA. Implication: CAST one Kokoro take; replace F0/timing only.

9. **Formant-moving WSOLA destroys speaker ID (EER 0.9% → 38%); TD-PSOLA does not.** Looney & Gaubitch 2025 EUSIPCO. Implication: the landing-page DSP pitch-shift was measured identity death.

10. **XiaoiceSing residual F0 and DiffSinger MIDI-B condition one model on lyrics+MIDI.** Lu et al. 2020 (arXiv:2006.06261); Liu et al. 2022 (arXiv:2105.02446). Implication: score F0 is a residual around one singer, not a new TTS per note.

11. **RVC/so-vits-svc: content + F0 from the same source take; `auto_predict_f0` is forbidden for singing.** Qian et al. 2022 ContentVec; RVC README. Implication: independent syllable TTS samples a new embedding each time — the nightmare fuel.

### Timing is a contract; Comfy fills the window

12. **DAWs pin audio to the meter with warp markers, not prompts.** Ableton Live 12 §9. Implication: fx-dub `place(at_seconds)` / `place_exact` is the production move.

13. **ByteDance Seed Audio `[start:end]` stamps are an absolute output timeline and write leading silence.** Comfy-Org ByteDanceSeedAudio docs 2026. https://docs.comfy.org/built-in-nodes/ByteDanceSeedAudio. Implication: jam-sessions `startSec`/`durationSec` emit those stamps; Python is the clock.

14. **ACE-Step duration/BPM sizes a latent canvas; it is not note MIDI.** Gong et al. 2025–2026 (arXiv:2506.00045, 2602.00744). Implication: ACE-Step cannot honor New Britain onsets.

15. **Sinsy time-lag: vowel onset tracks the score; consonants anticipate.** Hono et al. 2021 (arXiv:2108.02776). Implication: stamps should target vowel windows, not letter onsets.

16. **Autoregressive TTS has no duration unless token count / MFA durations are inputs.** Zhou et al. 2025 IndexTTS2 (arXiv:2506.21619); Ren et al. 2019 FastSpeech. Implication: a prompt cannot be the metronome.

### Comfy Cloud audio-to-audio (what actually takes a wav)

17. **`ByteDanceSeedAudio` + `LoadAudio`: clone-then-speak, `pitch_rate` ±12 st; not STS that keeps the wav’s words.** Comfy-Org 2026. Implication: use timestamps from (13), not as MIDI-accurate F0.

18. **`ElevenLabsSpeechToSpeech` keeps words and emotion; knobs are speed/stability, not pitch_rate.** Comfy-Org 2026. https://docs.comfy.org/built-in-nodes/ElevenLabsSpeechToSpeech. Implication: this is the Cloud node that *transforms the Kokoro file* without minting new text.

19. **ACE-Step 1.5 Cover/Repaint is “Coming Soon” on Cloud; v1 audio-to-audio `denoise` can ignore the source.** Comfy-Org ACE-Step tutorials. Implication: not the MIDI-locked singer.

20. **Chatterbox VC is MIT wav→wav, local; Fill-ChatterBox is not on the retrieved Cloud allowlist. Kokoro is Apache local, not on Cloud.** Resemble 2025; hexgrad 2025. Implication: Cloud transform of the lock file = ElevenLabs STS (paid ToS) or Seed Audio clone-then-speak; local MIT VC = Chatterbox.

21. **LoadAudio uses a storage key after upload, not a public HTTPS URL.** Comfy-Org LoadAudio + Cloud API. Implication: `upload_file` → LoadAudio → STS, never `partner_generate` medias[].

---

## Architectural lock

```
Python / jam-sessions ScoreNote.startSec     (findings 1–7, 12–16)
        ↓ emit [start:end] lyric stamps
one CAST wav (Kokoro lock.wav)                (8–11)
        ↓ Comfy Cloud LoadAudio
ElevenLabsSpeechToSpeech  OR  Seed Audio
   (keep words)                  (timestamped new delivery)
        ↓ fx-dub place / mix_dialogue_anchored
piano bed from jam-sessions
        ↓ fxdub-dialogue + F0-cents vs MIDI
admit or reject
```

**C1.** The language is Python seconds (pretty_midi / jam-sessions), not SuperCollider and not a prose prompt (1, 2, 4, 6, 7).

**C2.** One take. Never 14 TTS syllables (9, 11).

**C3.** Comfy owns timbre. Plug the lock into `ElevenLabsSpeechToSpeech` (18, 21) or Seed Audio with stamps emitted from the score (13, 17). Do not use ACE-Step as the singer (14, 19).

**C4.** Timing = absolute stamps from `startSec` (13, 15), then mix (12). Do not ask the model for 35 seconds (16).

**C5.** Landing-page license: Kokoro Apache CAST is fine; ElevenLabs STS output follows paid ToS (wave 2 finding 8 in lane comfy). Prefer Chatterbox VC locally if the clip must stay MIT.

---

## What this wave does not do

- No more Pink Trombone / additive / WSOLA-per-note as the public singer.
- Comfy MCP was **unauthenticated in the Grok TUI session**; the API key file exists. Submit is a follow-on: upload `tmp/kokoro-lock/lock.wav`, run STS or timestamped Seed Audio, mix with piano.
