"""Wave-5 #160 — Chroma1-HD baseline; completes the 3-model diffusion set. Idempotent."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()
wave5 = c.execute("SELECT id FROM waves WHERE wave_number=5").fetchone()[0]
body = (
"Chroma1-HD (fp8mixed) DIFFUSION BASELINE — MEASURED 2026-06-03, ComfyUI 0.23.0, RTX 5090. The studio's PHOTOREALISM model (vs Z-Image painterly #147, Qwen-Image text-in-image #159). "
"Graph (hand-built API, headless /prompt): UNETLoader(Chroma1-HD-fp8mixed, 9.2GB) + CLIPLoader(t5xxl_fp8_e4m3fn, type=chroma) + VAELoader(ae.safetensors) + ModelSamplingAuraFlow(shift 1) + the SamplerCustomAdvanced chain "
"(RandomNoise -> CFGGuider(cfg 4, pos+neg) -> SamplerCustomAdvanced, with BasicScheduler(simple, 26 steps) sigmas + KSamplerSelect(euler)). 1024^2. Graph worked first try.\n\n"
"FLOOR (cuDNN-SDPA): 12.66 s/img. Peak VRAM 16.3 GB — LIGHT, lots of headroom for higher-res / batch / SA (unlike Qwen-Image's 31.7 GB ceiling). 578 W. "
"Photorealism VERIFIED (looked at the output per the rule: a red-fox close-up — detailed fur, sharp amber eyes, soft natural light, shallow DoF — genuinely photographic).\n\n"
"SA 2.2 fp8_cuda: 11.31 s/img (-11%) — a bit more than Qwen-Image's 7% / Z-Image's 8% at 1024^2 (26 steps + T5 cross-attention give attention a larger share). fp8_cuda confirmed the SAFE working backend on a THIRD model: Z-Image + Qwen-Image + Chroma ALL work with fp8_cuda; fp16_cuda crashes UNIVERSALLY (#159).\n\n"
"DIFFUSION DAILY-DRIVER ROUTING — the 3-model studio set, all Apache-2.0, all now baselined on the 5090: "
"Z-Image-Turbo (nvfp4, 8-step, ~1.7 s, #147) = FAST painterly; Chroma1-HD (fp8mixed, 26-step, ~12.7 s, light 16 GB) = PHOTOREALISM; Qwen-Image-2512 (fp8, 20-step, ~18 s, heavy 31.7 GB) = TEXT-IN-IMAGE / max quality. "
"All three accept SA fp8_cuda (KJNodes patch node) for a small free speedup at 1024^2; the win grows with resolution on the light models. Harness: baselines/_chroma_bench.py; raw chroma-results.json + dmon."
)
c.execute("DELETE FROM config_recipes WHERE id=160")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (160,?,?,?,?,?,?,?,?)""", (
  "diffusion-chroma1-hd-fp8mixed-baseline-measured-5090",
  "Chroma1-HD (fp8mixed) baseline MEASURED: 12.66s/img 1024^2, light 16.3GB, SA fp8_cuda -11%, photorealism verified; completes the 3-model diffusion set",
  6, 56, "baseline",
  "https://comfyanonymous.github.io/ComfyUI_examples/",
  body, wave5))
db.commit()
print("inserted #160; recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id",(wave5,)):
    print(" ", r[0], r[1], "|", r[2][:54])
db.close()
