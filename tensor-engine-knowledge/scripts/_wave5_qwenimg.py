"""Wave-5 #159 — Qwen-Image-2512 baseline + corrects #154's Lumina2-head_dim speculation. Idempotent."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()
wave5 = c.execute("SELECT id FROM waves WHERE wave_number=5").fetchone()[0]

# correct #154 (the fp16_cuda crash is NOT Lumina2-specific)
row = c.execute("SELECT body FROM config_recipes WHERE id=154").fetchone()
if row and "CORRECTION 2026-06-03" not in row[0]:
    corr = ("\n\nCORRECTION 2026-06-03 (#159): the fp16_cuda crash is NOT a Lumina2/head_dim issue as speculated above — "
            "sageattn_qk_int8_pv_fp16_cuda ALSO crashes ComfyUI on Qwen-Image-2512 (a different DiT). It is a GENERAL "
            "instability of that backend in ComfyUI+SA-2.2 across these DiT models. Use fp8_cuda (or fp16_triton); never fp16_cuda.")
    c.execute("UPDATE config_recipes SET body=? WHERE id=154", (row[0]+corr,))
    print("corrected #154")

body = (
"Qwen-Image-2512 (fp8) DIFFUSION BASELINE — MEASURED 2026-06-03, ComfyUI 0.23.0, RTX 5090. The studio's QUALITY / text-in-image model (vs the Z-Image-Turbo daily driver #147). "
"Graph (hand-built API, headless /prompt): UNETLoader(qwen_image_2512_fp8_e4m3fn, 20GB) + CLIPLoader(qwen_2.5_vl_7b, type=qwen_image) + VAELoader(qwen_image_vae) + ModelSamplingAuraFlow(shift 3) + KSampler(20-step euler, cfg 2.5) + EmptySD3LatentImage. 1024^2.\n\n"
"FLOOR (cuDNN-SDPA): 18.08 s/img. Peak VRAM 31.7 GB — NEAR THE 32GB CEILING: Qwen-Image fp8 at 1024^2 leaves NO room for 2048^2 or batch (this is the practical max res on a 5090). 575 W. "
"Text-in-image VERIFIED EXCELLENT (looked at the output per the look-at-images rule: a tavern signboard reading 'STUDIO TEST 2512' rendered perfectly in carved gold-leaf letters — Qwen-Image's signature strength, confirmed).\n\n"
"SA 2.2 (KJNodes patch node): fp8_cuda 16.89 s (-7%), fp16_triton 16.79 s (-7%) — MODEST, same reason as Z-Image at 1024^2 (attention is a small slice of a 20-step gen on a 20B model; the win grows with resolution but Qwen-Image is VRAM-capped at 1024^2 so you can't chase it). SA fp8_cuda output VERIFIED valid (non-garbage, text intact).\n\n"
"KEY FINDING / HYPOTHESIS REFUTED: sageattn_qk_int8_pv_fp16_cuda CRASHES ComfyUI on Qwen-Image-2512 TOO (not just Z-Image/Lumina2). => the fp16_cuda crash is NOT a Lumina2 head_dim issue — it's a GENERAL instability of that backend in ComfyUI+SA-2.2 on these DiTs (corrects #154's speculation). USE fp8_cuda or fp16_triton (both work, ~7%); NEVER fp16_cuda.\n\n"
"PER-MODEL RECOMMENDATION (diffusion daily-driver routing): Z-Image-Turbo (nvfp4, 8-step, ~1.4-1.7 s, #147) for FAST gens; Qwen-Image-2512 (fp8, ~18 s, VRAM-heavy) when TEXT-IN-IMAGE or max quality is needed (text rendering unmatched). Harness: baselines/_qwenimg_bench.py + _qwenimg_sa.py; raw qwenimg-results.json + qwenimg-sa-results.json + dmon logs."
)
c.execute("DELETE FROM config_recipes WHERE id=159")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (159,?,?,?,?,?,?,?,?)""", (
  "diffusion-qwen-image-2512-fp8-baseline-and-sa-measured-5090",
  "Qwen-Image-2512 (fp8) baseline MEASURED: 18.08s/img 1024^2, 31.7GB (VRAM ceiling), SA ~7%, fp16_cuda crashes (not Lumina2-specific), text-in-image verified",
  6, 56, "baseline",
  "https://comfyanonymous.github.io/ComfyUI_examples/",
  body, wave5))
db.commit()
print("inserted #159; recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
db.close()
