# Zed speech — Kokoro neural TTS

The agent now speaks through **Kokoro-82M**, a high-quality open-weight neural text-to-speech model. It runs locally on your machine, requires no API keys, and sounds dramatically better than the built-in Windows SAPI5 voices.

## What's changed

- **Default voice** is now `af_heart` — a natural American female neural voice.
- **Legacy voices** still work: set `ZED_SPEAK_VOICE` to a Microsoft voice name (e.g. `Microsoft Zira Desktop`) and the script falls back to `System.Speech.Synthesis`.
- **Stop shortcut** still works exactly as before (`Ctrl+Shift+Alt+.`).

## Shortcuts

| Shortcut | What it does |
| --- | --- |
| `Ctrl+Shift+Alt+V` | Read the selection, or the clipboard if nothing is selected |
| `Ctrl+Shift+Alt+.` | Stop |

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `ZED_SPEAK_VOICE` | `af_heart` | Kokoro voice name (see list below) or legacy `Microsoft*` name |
| `ZED_SPEAK_RATE` | `0` | Speaking rate. `-10` to `10`. Maps to Kokoro speed `0.5`–`1.5` |

## Available Kokoro voices (American English)

**Female**
- `af_heart` — default, warm and clear
- `af_alloy`
- `af_aoede`
- `af_bella`
- `af_jessica`
- `af_kore`
- `af_nicole`
- `af_nova`
- `af_river`
- `af_sarah`
- `af_sky`

**Male**
- `am_adam`
- `am_echo`
- `am_eric`
- `am_fenrir`
- `am_liam`
- `am_michael`
- `am_onyx`
- `am_puck`
- `am_santa`

Other languages (British, Spanish, French, Hindi, Italian, Portuguese, Japanese, Mandarin) have their own prefixes: `bf_`, `bm_`, `ef_`, `em_`, `ff_`, `hf_`, `hm_`, `if_`, `im_`, `jf_`, `jm_`, `pf_`, `pm_`, `zf_`, `zm_`.

Full list: https://huggingface.co/hexgrad/Kokoro-82M/tree/main/voices

## Requirements (already installed)

- Python 3.10+
- `pip install kokoro soundfile torch`
- `espeak-ng` (Windows MSI from https://github.com/espeak-ng/espeak-ng/releases)

## Files

- `speak.ps1` — main speaker script (Kokoro + fallback)
- `stop.ps1` — unchanged
- `speak.ps1.backup` — original SAPI5-only script
