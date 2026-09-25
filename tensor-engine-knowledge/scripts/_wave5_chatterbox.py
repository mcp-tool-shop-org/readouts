"""Wave-5 #161 — Chatterbox TTS engine row (144) + Blackwell run-recipe. Idempotent."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()
wave5 = c.execute("SELECT id FROM waves WHERE wave_number=5").fetchone()[0]

# --- engine row 144: Chatterbox TTS ---
c.execute("DELETE FROM engines WHERE id=144")
c.execute("""INSERT INTO engines (id,slug,name,category_id,engine_type,developer,language,latest_version,release_date,
  license,commercial_use,commercial_notes,maturity_tier,platforms,accelerators,model_formats,blackwell_ready,
  optimization_for,multi_gpu,speed_note,repo_url,status,rig_fit,studio_fit,download_priority,summary,verified,verify_note,wave_id,created_date)
  VALUES (144,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
  "chatterbox-tts","Chatterbox TTS (Resemble AI)",9,"runtime (PyTorch TTS)","Resemble AI","Python (PyTorch)",
  "pip chatterbox-tts (2026-06)","2026-06-03","MIT (engine + weights)","yes",
  "MIT on code AND weights - commercial-safe, the cleanest license among top-quality voice-clone TTS. Every output carries Resemble's imperceptible 'Perth' watermark (provenance feature, not a restriction). MIT does NOT waive voice-cloning CONSENT - clone only voices you have rights to (use own/licensed/synthetic refs for game VO).",
  "production","Windows (native, validated), Linux, macOS","NVIDIA CUDA (PyTorch)","HuggingFace auto-download (~2-3GB)",1,
  "Most realistic commercial-safe voice: zero-shot voice cloning + emotion-exaggeration control. Offline character VO.",
  "Single-GPU (light ~6GB, runs alongside other engines)","RTF ~1.1 on the 5090 (near real-time; offline batch VO, not live). Light 6.2GB VRAM.",
  "https://github.com/resemble-ai/chatterbox","recommended",5,5,1,
  "The most realistic commercial-safe voice for this rig and the studio's character-VO default. MIT-licensed (code+weights), frontier blind-test quality (Chatterbox-Turbo ~65% vs ElevenLabs ~25%), zero-shot voice cloning from a reference wav + emotion control. STOOD UP + MEASURED on the 5090 (wave-5 #161): runs on torch 2.12 cu130 sm_120 despite its torch==2.6.0 pin (override it), RTF 1.10, ~6.2GB VRAM, non-silent audio confirmed. Fills the speech-lane gap - Kokoro #109/Piper #108 were the only TTS run-recipes and both are plainer/no-clone. Pair with Kokoro for no-consent-risk bulk VO; VibeVoice-Large 7B (MIT, not yet stood up) for long-form multi-speaker.",
  1,"Stood up + measured live on the RTX 5090 (sm_120, torch 2.12.0+cu130) 2026-06-03: import OK, generated 4.88s audio @24kHz in 5.37s (RTF 1.10), peak 6.2GB VRAM, RMS 0.117 (non-silent). torch==2.6.0 pin overridden to 2.12 cu130. torchaudio.save->torchcodec gotcha worked around with stdlib wave write.",
  wave5,"2026-06-03"))

# --- recipe #161 ---
body = (
"Chatterbox TTS (Resemble AI, MIT) STOOD UP + VALIDATED on the RTX 5090 / sm_120 — the MOST REALISTIC commercial-safe voice (frontier blind-test quality, zero-shot voice cloning + emotion control; beat ElevenLabs ~65/25 in side-by-sides). "
"Fills the speech-engines gap: the lane had Blackwell run-recipes only for the plainer Kokoro (#109) + Piper (#108); none for a realistic voice-clone model.\n\n"
"ENV: fresh uv venv (py3.11) at E:\\AI\\training\\chatterbox-env; torch 2.12.0+cu130 + torchaudio 2.11.0+cu130 + chatterbox-tts (pip).\n\n"
"BLACKWELL GOTCHAS (earned, both real):\n"
"1) chatterbox-tts HARD-PINS torch==2.6.0 -> pip installs the CPU build AND torch 2.6.0 predates sm_120 entirely (Blackwell needs >=2.7/cu128). The pin is OVER-CONSERVATIVE. FIX: after `pip install chatterbox-tts`, reinstall `torch==2.12.0 torchaudio --index-url https://download.pytorch.org/whl/cu130`. Chatterbox imports + runs fine on torch 2.12 (note: cu130 pairs torch 2.12 with torchaudio 2.11, not 2.12).\n"
"2) torchaudio 2.11 routes `torchaudio.save` through torchcodec (not installed) -> ModuleNotFoundError. FIX: write the WAV via stdlib `wave` + numpy int16 PCM (no extra dep), or `pip install torchcodec`/`soundfile`.\n\n"
"MEASURED (default settings, 105-char line): audio 4.88 s @ 24000 Hz, gen 5.37 s -> RTF 1.10 (near real-time — fine for OFFLINE batch VO, not live streaming), peak ~6.2 GB process VRAM (3.37 GB torch-alloc) = LIGHT (runs alongside ComfyUI / llama-swap), 141 W. Audio VERIFIED non-silent (RMS 0.117); wav saved to E:\\AI\\training\\chatterbox_sample.wav for the USER to LISTEN (subjective realism is theirs to judge — the engine baseline + that it runs/produces real audio is what's proven here).\n\n"
"USAGE: `from chatterbox.tts import ChatterboxTTS; m=ChatterboxTTS.from_pretrained(device='cuda'); wav=m.generate(text)`. VOICE CLONE: `m.generate(text, audio_prompt_path='ref.wav')`. Emotion via the exaggeration param. Perth watermark embedded in every output.\n\n"
"RECOMMENDATION (studio voice routing): Chatterbox = the realistic CHARACTER-VOICE default (clone a reference per character; ties to Motif VO + game dialogue). Kokoro (#109) = no-consent-risk bulk/UI VO (fixed voices, much faster). VibeVoice-Large 7B (Microsoft, MIT) = long-form multi-speaker dialogue — ALSO a gap (not yet stood up; next speech target). Test: E:\\AI\\training\\chatterbox_test.py; result chatterbox_result.json; telem baselines/chatterbox-dmon.log."
)
c.execute("DELETE FROM config_recipes WHERE id=161")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (161,?,?,?,?,?,?,?,?)""", (
  "speech-chatterbox-tts-blackwell-5090-most-realistic-commercial-voice",
  "Chatterbox TTS on the 5090 (VALIDATED): the most realistic commercial-safe voice — torch-pin override + torchcodec gotcha, RTF 1.10, 6.2GB",
  9, 144, "recipe",
  "https://github.com/resemble-ai/chatterbox",
  body, wave5))
db.commit()
print("inserted engine 144 + recipe #161")
print("engines:", c.execute("SELECT count(*) FROM engines").fetchone()[0], "| recipes:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
db.close()
