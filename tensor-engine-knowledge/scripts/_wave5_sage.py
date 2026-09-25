"""Wave-5 #154 — SageAttention 2.2.0 measured on Z-Image. Idempotent on id 154."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()
wave5 = c.execute("SELECT id FROM waves WHERE wave_number=5").fetchone()[0]

body = (
"SageAttention 2.2.0 STOOD UP + MEASURED on native-Win ComfyUI (2026-06-03; RTX 5090 sm_120; ComfyUI 0.23.0 portable, py3.13.12, torch 2.12.0+cu130). "
"Replaces SA 1.0.6 (triton-only, +9-24%). NO source build / NO nvcc needed.\n\n"
"INSTALL (Path A, the KB's 'cp311/torch2.11/cu128 wont load' note is now STALE): woct0rdho/SageAttention release v2.2.0-windows.post4 ships "
"ABI3 wheels -- 'sageattention-2.2.0+cu130torch2.9.0andhigher.post4-cp39-abi3-win_amd64.whl'. cp39-ABI3 = the stable Python ABI => loads on ANY Python >=3.9 incl. cp313; "
"'cu130torch2.9.0andhigher' covers torch 2.12.0+cu130. gh release download v2.2.0-windows.post4 --repo woct0rdho/SageAttention --pattern '*cu130torch2.9.0andhigher*cp39-abi3*.whl'; "
"then .\\python_embeded\\python.exe -m pip uninstall -y sageattention; pip install <whl>. Functional CUDA-kernel test passes on sm_120 (sageattn + sageattn_qk_int8_pv_fp16_cuda both run, finite out). License Apache-2.0.\n\n"
"WIRING: ComfyUI-KJNodes 'PathchSageAttentionKJ' node (model->node->ModelSamplingAuraFlow). With 2.2.0 the node exposes backends: "
"[disabled, auto, sageattn_qk_int8_pv_fp16_cuda, sageattn_qk_int8_pv_fp16_triton, sageattn_qk_int8_pv_fp8_cuda, sageattn_qk_int8_pv_fp8_cuda++, sageattn3, sageattn3_per_block_mean]. "
"Do NOT use the global --use-sage-attention flag (triton path = black output on Qwen/Wan).\n\n"
"CRASH GOTCHA (earned, high-value): backend 'sageattn_qk_int8_pv_fp16_cuda' HARD-CRASHES ComfyUI on Z-Image-Turbo (a Lumina2/NextDiT DiT; CLIP type 'lumina2'; attention.qkv.weight [11520,3840]) -- native access-violation that kills the whole python process (not a catchable error). The int8 fp16-PV CUDA kernel doesn't handle this model's attention head config. SAFE + FAST alternative: 'sageattn_qk_int8_pv_fp8_cuda' works perfectly AND is the fastest; 'sageattn_qk_int8_pv_fp16_triton' also works. => for Z-Image use fp8_cuda.\n\n"
"MEASURED (Z-Image-Turbo nvfp4, 8-step 1024-base, fp8_cuda vs the cuDNN-SDPA floor; min of warm iters):\n"
"  1024x1024: floor 1.35s -> SA 1.24s = 8.3% faster (best nvfp4 1.238; bf16 2.50 vs floor 2.64). vs #148 SA-1.0.6 (nvfp4 1.32) SA-2.2 is ~6% better.\n"
"  1536x1536: floor 3.77s -> SA 2.99s = 20.8% faster\n"
"  2048x2048: floor 8.76s -> SA 6.19s = 29.3% faster\n"
"=> THE WIN SCALES WITH ATTENTION SHARE (attention is O(n^2) in tokens). The KB's '~30-35%' is REAL but only at attention-dominated settings (high-res / high-step / video, e.g. 29% @2048^2); on the 8-step 1024^2 TURBO daily driver attention is a small slice so the win is only ~8-10%. "
"ACTIONABLE: leave SA-2.2 fp8_cuda engaged via the KJNodes node -- it's ~free at 1024^2 and a large win for high-res/high-step/video/batch. Peak 580 W / 57 C during the sweep, zero throttle. "
"Raw: baselines/sage2-zimage-results.json, sage2-res-results.json. Bench harness: baselines/_sage2_zimage.py, _sage2_res.py."
)
c.execute("DELETE FROM config_recipes WHERE id=154")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (154,?,?,?,?,?,?,?,?)""", (
  "attention-sageattention-2.2.0-comfyui-zimage-measured-fp8cuda-5090",
  "SageAttention 2.2.0 on ComfyUI (MEASURED): cu130 abi3 wheel, fp8_cuda best, fp16_cuda crashes Lumina2, win scales with res",
  4, None, "recipe",
  "https://github.com/woct0rdho/SageAttention/releases/tag/v2.2.0-windows.post4",
  body, wave5))
db.commit()
print("inserted #154; recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
db.close()
