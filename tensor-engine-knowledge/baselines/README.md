# baselines/

Raw GPU telemetry from **wave 4** — the measured RTX 5090 baseline. Captured with `nvidia-smi dmon` (@1 s) while driving sustained generations through Ollama 0.24.0. See the full report + interpretation in [waves/wave-04-baseline/dispatch.md](../waves/wave-04-baseline/dispatch.md); the numbers are also in the DB as `config_recipes` rows with `kind='baseline'` (query: `SELECT name, body FROM config_recipes WHERE kind='baseline'`).

| File | What |
|---|---|
| `idle.dmon.txt` | 24 samples at idle (16 W · 28°C · P8) |
| `load_qwen3_6_27b.dmon.txt` | qwen3.6:27b under sustained load |
| `load_qwen3_6_35b-a3b.dmon.txt` | qwen3.6:35b-a3b (MoE) under load |
| `load_gemma4_31b.dmon.txt` | gemma4:31b under load |
| `load_translategemma_12b.dmon.txt` | translategemma:12b under load |

`dmon` columns: `gpu pwr(W) gtemp(C) mtemp sm(%) mem(%) enc dec jpg ofa mclk(MHz) pclk(MHz)`. To re-measure, re-run the wave-4 harness and diff against these.

The ComfyUI server logs (`comfy-server*.log`) are captured as-is except for one edit: on 2026-09-25, before publication, home-directory paths inside them were replaced with `<tmp>` (the temp directory) and `~` (the home directory). Nothing else was changed.
