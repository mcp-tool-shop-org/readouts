# Wave 9 — local TTS append from DR-001 (2026-08-30)

JOB-R-001. One append wave on `model-knowledge` audio only. Facts from the Researcher JOB-R-001 pack (DR-001 citations). Did not install a TTS stack. Did not clone generated-audio. Did not touch other KBs. Did not hand-edit `catalog/`.

## Already covered (do not duplicate)

- Chatterbox / Chatterbox Multilingual — wave-8 commercial-safe shortlist and README audio headline (`chatterbox-tts`).
- Qwen3-TTS — already a model row (`qwen3-tts`, wave 7).
- Kokoro-82M — already a model row (`kokoro-82m`, wave 1).
- ACE-Step 1.5 and DiffRhythm 2 — already on the audio shortlist; DR-001 did not treat them as TTS.

A later wave may append Turbo/watermark/Podonos sources to the existing Chatterbox row. That is not a new model.

## New rows this wave (verified=0)

| Model | License | commercial_use | Why new |
|---|---|---|---|
| Fun-CosyVoice 3.0 0.5B | Apache-2.0 | yes | Not in audio table; smaller Apache clone vs Qwen3-TTS |
| IndexTTS-2.5 | Bilibili Model Use License | unknown | Not in audio table; commercial via email, not Apache |
| F5-TTS (official ckpt) | code MIT, weights CC-BY-NC | no | Not in audio table; official weights are not commercial-safe |
| piper1-gpl | GPL-3.0 engine; voices per-file | conditional | Not in audio table; copyleft + voice provenance |
| Pocket TTS ~100M | code MIT; weight SPDX unconfirmed | unknown | Not in audio table; CPU clone claimed |

Not a models row: saghul/local-tts is packaging (ElevenLabs-shaped local API). Recorded as a resource extra.

## Verification

No retrieval verifier ran on this VM. `verification.md` is all unverified. Do not fake `verified`.
