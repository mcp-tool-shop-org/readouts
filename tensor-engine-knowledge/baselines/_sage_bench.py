#!/usr/bin/env python3
"""Focused re-bench after the triton/Python.h fix: SageAttention (auto) + torch.compile on Z-Image-Turbo."""
import json, time, urllib.request, os
HOST = "http://127.0.0.1:8188"; CID = "sagebench"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sage-results.json")
PROMPT = ("2.5D JRPG key art: a lone frontier traveler in a worn duster coat stands at a "
          "windswept mesa overlook at golden hour, distant canyon town below, painterly "
          "stylized, warm cinematic rim light, crisp detail, original concept")

def post(p, payload):
    req = urllib.request.Request(HOST + p, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r: return json.loads(r.read())
def get(p):
    with urllib.request.urlopen(HOST + p, timeout=120) as r: return json.loads(r.read())

def graph(unet, mode, prefix, seed, w=1024, h=1024, batch=1, steps=8):
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
    if mode == "sage":
        g["20"] = {"class_type": "PathchSageAttentionKJ", "inputs": {"model": ["10", 0], "sage_attention": "auto", "allow_compile": False}}
        g["16"]["inputs"]["model"] = ["20", 0]
    elif mode == "compile":
        g["21"] = {"class_type": "TorchCompileModel", "inputs": {"model": ["16", 0], "backend": "inductor"}}
        g["17"]["inputs"]["model"] = ["21", 0]
    return g

def run(g):
    t0 = time.time()
    r = post("/prompt", {"prompt": g, "client_id": CID})
    if r.get("node_errors"): raise RuntimeError("node_errors: " + json.dumps(r["node_errors"]))
    pid = r["prompt_id"]
    while True:
        h = get("/history/" + pid)
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") != "success": raise RuntimeError("exec: " + json.dumps(st)[:400])
            return time.time() - t0
        time.sleep(0.1)

def bench(label, unet, mode, prefix, iters, seed0=42):
    print(f"\n>>> {label}")
    times = []
    win_start = time.time()
    for i in range(iters):
        try:
            dt = run(graph(unet, mode, prefix, seed0 + i))
            times.append(dt); print(f"    iter{i}: {dt:.3f}s ({steps_note(dt)})")
        except Exception as e:
            print(f"    iter{i} FAILED: {type(e).__name__}: {str(e)[:200]}")
            return {"label": label, "error": str(e)[:300], "times": times, "win_start": win_start, "win_end": time.time()}
    win_end = time.time()
    return {"label": label, "unet": unet, "mode": mode, "times": times, "win_start": win_start, "win_end": win_end}

def steps_note(dt): return f"{dt:.3f}s/img, {8/dt:.2f} it/s"

def main():
    res = {"started": time.time(), "runs": []}
    print(">>> WARM-UP bf16"); print(f"    {run(graph('z_image_turbo_bf16.safetensors', None, 'warm', 7)):.2f}s")
    res["runs"].append(bench("bf16 / SAGE-auto (triton)", "z_image_turbo_bf16.safetensors", "sage", "zimg_sage", 3))
    res["runs"].append(bench("nvfp4 / SAGE-auto (triton)", "z_image_turbo_nvfp4.safetensors", "sage", "zimg_sage_fp4", 3))
    res["runs"].append(bench("bf16 / torch.compile inductor (iter0=compile)", "z_image_turbo_bf16.safetensors", "compile", "zimg_compile", 4))
    res["ended"] = time.time()
    json.dump(res, open(OUT, "w"), indent=2)
    print("\n=== SAGE/COMPILE SUMMARY (vs cuDNN-SDPA floor: bf16 2.86s, nvfp4 1.74s) ===")
    for r in res["runs"]:
        if r.get("error"): print(f"  {r['label']:46} ERROR: {r['error'][:90]}")
        elif r["times"]:
            warm = r["times"][1:] if "compile" in r["label"] and len(r["times"]) > 1 else r["times"]
            print(f"  {r['label']:46} min {min(warm):.3f}s/img (all: {[round(t,2) for t in r['times']]})")
    print(f"wrote {OUT}")

if __name__ == "__main__": main()
