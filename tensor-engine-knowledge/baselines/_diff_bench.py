#!/usr/bin/env python3
"""Headless ComfyUI diffusion baseline bench for the Robot rig (RTX 5090, sm_120).
Z-Image-Turbo, 1024^2, A/B pytorch-attn vs SageAttention (KJNodes patch node), + batch.
Stdlib only (urllib). Writes baselines/diff-results.json with per-run epoch windows for dmon slicing."""
import json, time, urllib.request, urllib.error, sys, os

HOST = "http://127.0.0.1:8188"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diff-results.json")
CID = "diffbench"

PROMPT = ("2.5D JRPG key art: a lone frontier traveler in a worn duster coat stands at a "
          "windswept mesa overlook at golden hour, distant canyon town below, painterly "
          "stylized, warm cinematic rim light, crisp detail, original concept")

def post(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(HOST + path, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())

def get(path):
    with urllib.request.urlopen(HOST + path, timeout=60) as r:
        return json.loads(r.read())

def build_graph(unet, sage_backend, width, height, batch, steps, seed):
    """Z-Image-Turbo API graph. sage_backend=None -> pytorch attention (no patch node)."""
    g = {
        "10": {"class_type": "UNETLoader", "inputs": {"unet_name": unet, "weight_dtype": "default"}},
        "11": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}},
        "12": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "13": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["11", 0], "text": PROMPT}},
        "14": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["13", 0]}},
        "15": {"class_type": "EmptySD3LatentImage", "inputs": {"width": width, "height": height, "batch_size": batch}},
        "16": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["10", 0], "shift": 3.0}},
        "17": {"class_type": "KSampler", "inputs": {
            "model": ["16", 0], "positive": ["13", 0], "negative": ["14", 0], "latent_image": ["15", 0],
            "seed": seed, "steps": steps, "cfg": 1.0, "sampler_name": "res_multistep", "scheduler": "simple", "denoise": 1.0}},
        "18": {"class_type": "VAEDecode", "inputs": {"samples": ["17", 0], "vae": ["12", 0]}},
        "19": {"class_type": "SaveImage", "inputs": {"images": ["18", 0], "filename_prefix": "zimg_baseline"}},
    }
    if sage_backend:
        # insert KJNodes Patch Sage Attention between UNETLoader and ModelSamplingAuraFlow
        g["20"] = {"class_type": "PathchSageAttentionKJ", "inputs": {"model": ["10", 0], "sage_attention": sage_backend, "allow_compile": False}}
        g["16"]["inputs"]["model"] = ["20", 0]
    return g

def run_once(graph):
    t0 = time.time()
    resp = post("/prompt", {"prompt": graph, "client_id": CID})
    if resp.get("node_errors"):
        raise RuntimeError("node_errors: " + json.dumps(resp["node_errors"]))
    pid = resp["prompt_id"]
    while True:
        h = get("/history/" + pid)
        if pid in h:
            st = h[pid].get("status", {})
            t1 = time.time()
            if st.get("status_str") == "error" or (st.get("status_str") and st.get("status_str") != "success"):
                raise RuntimeError("exec status: " + json.dumps(st))
            return t0, t1, h[pid]
        time.sleep(0.1)

def timed(label, unet, sage_backend, width, height, batch, steps, iters=3, seed=42):
    print(f"\n>>> {label}: unet={unet} sage={sage_backend} {width}x{height} batch={batch} steps={steps} iters={iters}")
    times = []
    win_start = time.time()
    for i in range(iters):
        g = build_graph(unet, sage_backend, width, height, batch, steps, seed + i)
        t0, t1, hist = run_once(g)
        dt = t1 - t0
        times.append(dt)
        print(f"    iter{i}: {dt:.3f}s  ({batch} img -> {dt/batch:.3f}s/img, {steps/dt:.2f} it/s)")
    win_end = time.time()
    times.sort()
    res = {
        "label": label, "unet": unet, "sage": sage_backend, "width": width, "height": height,
        "batch": batch, "steps": steps, "iters": iters,
        "t_min": times[0], "t_median": times[len(times)//2], "t_mean": sum(times)/len(times),
        "s_per_img_min": times[0]/batch, "it_s_max": steps/times[0],
        "win_start": win_start, "win_end": win_end, "all_times": times,
    }
    return res

def main():
    results = {"started": time.time(), "host": HOST, "runs": []}
    Z_BF16 = "z_image_turbo_bf16.safetensors"
    Z_FP4 = "z_image_turbo_nvfp4.safetensors"
    SAGE = "auto"  # SA 1.0.6 only exports top-level sageattn; KJNodes "auto" -> that dispatcher

    # warm-up (loads bf16 model + qwen_3_4b encoder; excluded from baselines)
    print(">>> WARM-UP (model load, excluded)")
    t0, t1, _ = run_once(build_graph(Z_BF16, None, 1024, 1024, 1, 8, 7))
    print(f"    warm-up wall: {t1-t0:.2f}s (includes weight load)")
    results["warmup_s"] = t1 - t0

    matrix = [
        ("bf16 / cuDNN-SDPA / 1024 / b1", Z_BF16, None, 1024, 1024, 1, 8, 3),
        ("bf16 / sage-auto / 1024 / b1",  Z_BF16, SAGE, 1024, 1024, 1, 8, 3),
        ("bf16 / cuDNN-SDPA / 1024 / b4", Z_BF16, None, 1024, 1024, 4, 8, 2),
        ("nvfp4 / cuDNN-SDPA / 1024 / b1", Z_FP4, None, 1024, 1024, 1, 8, 3),
        ("nvfp4 / sage-auto / 1024 / b1",  Z_FP4, SAGE, 1024, 1024, 1, 8, 3),
    ]
    for (label, unet, sage, w, h, b, st, it) in matrix:
        try:
            results["runs"].append(timed(label, unet, sage, w, h, b, st, iters=it))
        except Exception as e:
            print(f"    !! {label} FAILED: {type(e).__name__}: {str(e)[:300]}")
            results["runs"].append({"label": label, "error": f"{type(e).__name__}: {str(e)[:500]}"})

    results["ended"] = time.time()
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    print("\n=== SUMMARY ===")
    print(f"warm-up (load): {results['warmup_s']:.2f}s")
    for r in results["runs"]:
        if "error" in r:
            print(f"  {r['label']:38} ERROR: {r['error'][:120]}")
        else:
            print(f"  {r['label']:38} min {r['t_min']:.3f}s  {r['s_per_img_min']:.3f}s/img  {r['it_s_max']:.2f} it/s")
    print(f"\nwrote {OUT}")

if __name__ == "__main__":
    main()
