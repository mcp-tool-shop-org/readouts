# Route D handoff — DSP dry vocal + SVC timbre

**Status:** not started. Director: knock out A/B/C first; leave D as a handoff.
**Date:** 2026-09-04
**Depends on:** Route A (score-locked DSP singer) — landed in `ai-jam-sessions` `src/vocal/`.

## What D is

Take the Route A dry vocal (MIDI + lyrics, vowel-on-beat, residual vibrato) and retimbre it through a singing-voice conversion model so the lead can sound like a chosen singer. F0 and timing stay upstream (the DSP score). SVC must not become the pitch source.

Study-swarm finding 31: so-vits-svc takes F0 from the *source recording*, not MIDI. License **AGPL-3.0**. Real-time forks exist. Failure modes: timbre leakage; needs a pitch-accurate dry vocal.

## Do not

- Put so-vits-svc (AGPL) in the public `@mcptoolshop/ai-jam-sessions` npm tarball.
- Let SVC estimate F0 and replace the score (that undoes C2).
- Ship cloned voices without consent (same rule as Chatterbox in model-knowledge).

## Suggested shape (when picked up)

1. Render Route A to WAV (`renderOfflineSvs` / `--out`).
2. Isolated sidecar (separate package or local-only extra): AGPL converter reads that WAV + a reference clip, writes a retimbred WAV.
3. jam-sessions only shells out if `SVC_CMD` is set; default path stays the DSP lead.
4. Admission: score-relative F0 cents on the *output* must stay within the A gate (SVC must not retune). Lyrics MOS still required.

## Open questions for the Director

- Sidecar repo vs `~/.ai-jam-sessions/svc` extra?
- Acceptable SVC family if not so-vits-svc (MIT/Apache alternatives)?
- Consent / watermark policy for reference clips.

## Pointers

- A implementation: `E:\AI\ai-jam-sessions\src\vocal\`
- Research: [`dispatch.md`](dispatch.md) C5, finding 31
- Model-knowledge audio: Chatterbox is TTS, not SVC
