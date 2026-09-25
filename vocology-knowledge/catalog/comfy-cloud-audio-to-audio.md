# Comfy Cloud audio-to-audio (what actually takes a wav)
_auto-created from wave lane_ · wave 13 · 2026-09-14 · [‹ catalog index](README.md)

9 findings · 1 verified (abstract-supported accept).

| Finding | Authors · year | Claim | ✓ |
|---------|----------------|-------|---|
| ElevenLabsSpeechToSpeech | Comfy-Org · 2026 | ElevenLabsSpeechToSpeech keeps words and emotion; knobs are speed/stability, not pitch_rate. | ✓ |
| ACE-Step 1.5 Cloud templates | same page · documents “Run on Comfy Cloud” for AIO/split **text-to-music** templates (tags/lyrics → song). That is generation from text metadata, not a documented wav-preserving STS path. | documents “Run on Comfy Cloud” for AIO/split **text-to-music** templates (tags/lyrics → song). That is generation from text metadata, not a documented wav-preserving STS path. | · |
| ACE-Step 1.5 guide | Coming Soon · Comfy-Org | Cover and Repaint available in ACE-Step 1.5 but not yet supported in ComfyUI. Explicitly lists **Cover** and **Repaint** as “available in ACE-Step 1.5 but not yet supported in ComfyUI.” Cloud note: “Cloud will update after ComfyUI stable release.” Do not treat Cover/Repaint as live Comfy nodes. | · |
| ACE-Step v1 audio-to-audio tutorial | Comfy-Org · live | Workflow: `LoadAudio` → ACE-Step + `KSampler` `denoise`; “setting it to `1.00` is approximately equivalent to having no audio input.” Source wav can be ignored when denoise=1 — regenerate path, not word-preserving STS. | · |
| ByteDanceSeedAudio | Comfy-Org docs · live | Generates new AUDIO from `text_prompt` (+ optional reference clips/image/preset). Multilingual model documents per-line absolute timing stamps e.g. `[5.5s:8.0s]` controlling when/how long a quoted line is spoken. Has `pitch_rate` ±12 st. Not STS that keeps the source wav’s words — clone-then-speak / prompt synthesis. | · |
| Comfy SDKs | Comfy-Org · live | `client.assets.from_file(...)` lazy content-addressed handles; re-run with same bytes skips re-upload. Default Cloud base `https://cloud.comfy.org`; paid Cloud API key required. Outputs carry producing `job_id` (uploads have none). | · |
| ElevenLabsSpeechToSpeech | Comfy-Org docs · live | Takes `audio` (AUDIO) + target `voice`; “convert speech while preserving the original content and emotional tone.” Knobs on page: `stability`, `speed` (0.7–1.3), `similarity_boost`, `style`, `remove_background_noise`, `output_format`, `seed`. No `pitch_rate`. | · |
| LoadAudio | Comfy-Org docs · live | Loads from ComfyUI **input directory** only (“file must exist and be accessible”); outputs AUDIO (waveform + sample rate). Page does not document a public HTTPS URL input. | · |
| Upload an asset (API v2 multipart) | Comfy-Org · live | Cloud/self-host `POST /api/v2/assets`: multipart `file` + `content_type` + `file_path`; server-computed blake3 (`expected_hash` verified, never trusted); UUID asset + short-lived `url`. Provenance path for feeding bytes into workflows — content-addressed, not partner medias[]. | · |

## Detail

### ElevenLabsSpeechToSpeech · `load-bearing`
**ElevenLabsSpeechToSpeech keeps words and emotion; knobs are speed/stability, not pitch_rate.**
- **Implication:** this is the Cloud node that transforms the Kokoro file without minting new text.
- **Identifier:** `Comfy ElevenLabsSpeechToSpeech`
- **Verify:** Live Comfy Cloud catalog (get_node): desc 'preserving the original content and emotion'; full input spec is stability, model.speed, similarity_boost, style, seed, output_format, noise-removal. No pitch field. AUDIO in/out.
- **Sources:** [ElevenLabsSpeechToSpeech](https://docs.comfy.org/built-in-nodes/ElevenLabsSpeechToSpeech)

### ACE-Step 1.5 Cloud templates · `directional`
**documents “Run on Comfy Cloud” for AIO/split **text-to-music** templates (tags/lyrics → song). That is generation from text metadata, not a documented wav-preserving STS path.**
- **Implication:** STUDY-043 Comfy Cloud a2a docs. Cover/Repaint not live Comfy nodes.
- **Verify:** no external verdict — not yet swept

### ACE-Step 1.5 guide · `directional`
**Cover and Repaint available in ACE-Step 1.5 but not yet supported in ComfyUI. Explicitly lists **Cover** and **Repaint** as “available in ACE-Step 1.5 but not yet supported in ComfyUI.” Cloud note: “Cloud will update after ComfyUI stable release.” Do not treat Cover/Repaint as live Comfy nodes.**
- **Implication:** STUDY-043 Comfy Cloud a2a docs. Cover/Repaint not live Comfy nodes.
- **Identifier:** `https://docs.comfy.org/tutorials/audio/ace-step/ace-step-v1-5`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ACE-Step 1.5 guide](https://docs.comfy.org/tutorials/audio/ace-step/ace-step-v1-5)

### ACE-Step v1 audio-to-audio tutorial · `directional`
**Workflow: `LoadAudio` → ACE-Step + `KSampler` `denoise`; “setting it to `1.00` is approximately equivalent to having no audio input.” Source wav can be ignored when denoise=1 — regenerate path, not word-preserving STS.**
- **Implication:** STUDY-043 Comfy Cloud a2a docs. Cover/Repaint not live Comfy nodes.
- **Identifier:** `https://docs.comfy.org/tutorials/audio/ace-step/ace-step-v1`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ACE-Step v1 audio-to-audio tutorial](https://docs.comfy.org/tutorials/audio/ace-step/ace-step-v1)

### ByteDanceSeedAudio · `directional`
**Generates new AUDIO from `text_prompt` (+ optional reference clips/image/preset). Multilingual model documents per-line absolute timing stamps e.g. `[5.5s:8.0s]` controlling when/how long a quoted line is spoken. Has `pitch_rate` ±12 st. Not STS that keeps the source wav’s words — clone-then-speak / prompt synthesis.**
- **Implication:** STUDY-043 Comfy Cloud a2a docs. Cover/Repaint not live Comfy nodes.
- **Identifier:** `https://docs.comfy.org/built-in-nodes/ByteDanceSeedAudio`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ByteDanceSeedAudio](https://docs.comfy.org/built-in-nodes/ByteDanceSeedAudio)

### Comfy SDKs · `directional`
**`client.assets.from_file(...)` lazy content-addressed handles; re-run with same bytes skips re-upload. Default Cloud base `https://cloud.comfy.org`; paid Cloud API key required. Outputs carry producing `job_id` (uploads have none).**
- **Implication:** STUDY-043 Comfy Cloud a2a docs. Cover/Repaint not live Comfy nodes.
- **Identifier:** `https://docs.comfy.org/development/api-development/sdks`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Comfy SDKs](https://docs.comfy.org/development/api-development/sdks)

### ElevenLabsSpeechToSpeech · `directional`
**Takes `audio` (AUDIO) + target `voice`; “convert speech while preserving the original content and emotional tone.” Knobs on page: `stability`, `speed` (0.7–1.3), `similarity_boost`, `style`, `remove_background_noise`, `output_format`, `seed`. No `pitch_rate`.**
- **Implication:** STUDY-043 Comfy Cloud a2a docs. Cover/Repaint not live Comfy nodes.
- **Identifier:** `https://docs.comfy.org/built-in-nodes/ElevenLabsSpeechToSpeech`
- **Verify:** no external verdict — not yet swept
- **Sources:** [ElevenLabsSpeechToSpeech](https://docs.comfy.org/built-in-nodes/ElevenLabsSpeechToSpeech)

### LoadAudio · `directional`
**Loads from ComfyUI **input directory** only (“file must exist and be accessible”); outputs AUDIO (waveform + sample rate). Page does not document a public HTTPS URL input.**
- **Implication:** STUDY-043 Comfy Cloud a2a docs. Cover/Repaint not live Comfy nodes.
- **Identifier:** `https://docs.comfy.org/built-in-nodes/LoadAudio`
- **Verify:** no external verdict — not yet swept
- **Sources:** [LoadAudio](https://docs.comfy.org/built-in-nodes/LoadAudio)

### Upload an asset (API v2 multipart) · `directional`
**Cloud/self-host `POST /api/v2/assets`: multipart `file` + `content_type` + `file_path`; server-computed blake3 (`expected_hash` verified, never trusted); UUID asset + short-lived `url`. Provenance path for feeding bytes into workflows — content-addressed, not partner medias[].**
- **Implication:** STUDY-043 Comfy Cloud a2a docs. Cover/Repaint not live Comfy nodes.
- **Identifier:** `https://docs.comfy.org/api-reference/v2/assets/upload-an-asset-single-call-multipart`
- **Verify:** no external verdict — not yet swept
- **Sources:** [Upload an asset (API v2 multipart)](https://docs.comfy.org/api-reference/v2/assets/upload-an-asset-single-call-multipart)

