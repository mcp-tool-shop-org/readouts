#!/usr/bin/env python3
"""Wave-5: re-bench Z-Image-Turbo with SageAttention 2.2.0 (CUDA kernels) vs the cuDNN-SDPA floor.
Re-measures the floor in the SAME session for apples-to-apples comparison; tries multiple SA backends.
Compare against #147 floor (bf16 2.86 / nvfp4 1.74) and #148 SA-1.0.6-auto-triton (bf16 2.60 / nvfp4 1.32)."""
import json, time, urllib.request, os
HOST = "http://127.0.0.1:8188"; CID = "sage2bench"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sage2-results.json")
PROMPT = ("2.5D JRPG key art: a lone frontier traveler in a worn duster coat stands at a "
          "windswept mesa overlook at golden hour, distant canyon town below, painterly "
          "stylized, warm cinematic rim light, crisp detail, original concept")

def post(p, payload):
    req = urllib.request.Request(HOST + p, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r: return json.loads(r.read())
def get(p):
    with urllib.request.urlopen(HOST + p, timeout=120) as r: return json.loads(r.read())

def wait_ready(timeout=120):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            get("/object_info/KSampler"); return True
        except Exception: time.sleep(1.0)
    raise RuntimeError("ComfyUI not ready")

def graph(unet, sage_backend, prefix, seed, w=1024, h=1024, batch=1, steps=8):
    g = {
        "10": {"class_type": "UNETLoader", "inputs": {"unet_name": unet, "weight_dtype": "default"}},
        "11": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}},
        "12": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "13": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["11", 0], "text": PROMPT}},
        "14": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["13", 0]}},
        "15": {"class_type": "EmptySD3LatentImage", "inputs": {"width": w, "height": h, "batch_size": batch}},
        "16": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["10", 0], "shift": 3.0}},
        "17": {"class_type": "KSampler", "inputs": {"model": ["16", 0], "positive": ["13", 0], "negative": ["14", 0],
               "latent_image": ["15", 0], "seed": seed, "steps": steps, "cfg": 1.0,
               "sampler_name": "res_multistep", "scheduler": "simple", "denoise": 1.0}},
        "18": {"class_type": "VAEDecode", "inputs": {"samples": ["17", 0], "vae": ["12", 0]}},
        "19": {"class_type": "SaveImage", "inputs": {"images": ["18", 0], "filename_prefix": prefix}},
    }
    if sage_backend:
        g["20"] = {"class_type": "PathchSageAttentionKJ", "inputs": {"model": ["10", 0], "sage_attention": sage_backend, "allow_compile": False}}
        g["16"]["inputs"]["model"] = ["20", 0]
    return g

def run(g):
    t0 = time.time()
    r = post("/prompt", {"prompt": g, "client_id": CID})
    if r.get("node_errors"): raise RuntimeError("node_errors: " + json.dumps(r["node_errors"])[:400])
    pid = r["prompt_id"]
    while True:
        h = get("/history/" + pid)
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") != "success": raise RuntimeError("exec: " + json.dumps(st)[:400])
            return time.time() - t0
        time.sleep(0.05)

def bench(label, unet, sage_backend, prefix, iters=3, seed0=42):
    print(f"\n>>> {label}")
    times = []
    for i in range(iters):
        try:
            dt = run(graph(unet, sage_backend, prefix, seed0 + i))
            times.append(dt); print(f"    iter{i}: {dt:.3f}s/img ({8/dt:.2f} it/s)")
        except Exception as e:
            print(f"    iter{i} FAILED: {type(e).__name__}: {str(e)[:220]}")
            return {"label": label, "error": str(e)[:300], "times": times}
    return {"label": label, "unet": unet, "backend": sage_backend, "times": times, "min": min(times)}

def main():
    wait_ready()
    # discover available SA backends in this install
    try:
        oi = get("/object_info/PathchSageAttentionKJ")
        opts = oi["PathchSageAttentionKJ"]["input"]["required"]["sage_attention"][0]
        print(">>> PatchSageAttentionKJ backends available:", opts)
    except Exception as e:
        print(">>> could not read node backends:", str(e)[:120]); opts = []
    res = {"started": time.time(), "backends_available": opts, "runs": []}
    print(">>> WARM-UP"); print(f"    {run(graph('z_image_turbo_bf16.safetensors', None, 'warm', 7)):.2f}s")
    # floor (re-measured this session)
    res["runs"].append(bench("bf16  / NO-SAGE (cuDNN-SDPA floor)",  "z_image_turbo_bf16.safetensors",  None, "z2_bf16_floor"))
    res["runs"].append(bench("nvfp4 / NO-SAGE (cuDNN-SDPA floor)",  "z_image_turbo_nvfp4.safetensors", None, "z2_fp4_floor"))
    # SA 2.2.0 CUDA backend (recipe #68 target)
    be = "sageattn_qk_int8_pv_fp16_cuda" if (not opts or "sageattn_qk_int8_pv_fp16_cuda" in opts) else "auto"
    res["runs"].append(bench(f"bf16  / SA-2.2 ({be})",  "z_image_turbo_bf16.safetensors",  be, "z2_bf16_sa22"))
    res["runs"].append(bench(f"nvfp4 / SA-2.2 ({be})",  "z_image_turbo_nvfp4.safetensors", be, "z2_fp4_sa22"))
    # auto (let the node pick) for comparison
    res["runs"].append(bench("bf16  / SA-2.2 (auto)",  "z_image_turbo_bf16.safetensors",  "auto", "z2_bf16_auto"))
    res["runs"].append(bench("nvfp4 / SA-2.2 (auto)",  "z_image_turbo_nvfp4.safetensors", "auto", "z2_fp4_auto"))
    res["ended"] = time.time()
    json.dump(res, open(OUT, "w"), indent=2)
    print("\n=== SA-2.2.0 SUMMARY (vs #147 floor bf16 2.86 / nvfp4 1.74 ; #148 SA1.0.6 bf16 2.60 / nvfp4 1.32) ===")
    for r in res["runs"]:
        if r.get("error"): print(f"  {r['label']:42} ERROR: {r['error'][:80]}")
        else: print(f"  {r['label']:42} min {r['min']:.3f}s/img  all={[round(t,2) for t in r['times']]}")
    print(f"wrote {OUT}")

if __name__ == "__main__": main()
