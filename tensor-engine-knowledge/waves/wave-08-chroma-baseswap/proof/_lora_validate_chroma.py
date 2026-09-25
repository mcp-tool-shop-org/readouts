#!/usr/bin/env python3
"""Trigger-fires A/B for the CHROMA LoRA (Flux-family, T5-only). Same 3 held-out subjects + 3 cells as the SDXL runs,
so Chroma-vs-SDXL is apples-to-apples. Chroma inference graph per the official starter workflow:
UNETLoader -> [LoraLoaderModelOnly] -> ModelSamplingAuraFlow(shift1.0) -> CFGGuider -> SamplerCustomAdvanced (euler/beta/26).
CLIPLoader type 'chroma' (T5XXL only, no CLIP-L). LoRA is DiT-only (LoraLoaderModelOnly)."""
import json, time, urllib.request
HOST = "http://127.0.0.1:8188"; CID = "loraval_chroma"
UNET = "Chroma1-HD-fp8mixed.safetensors"
T5   = "t5xxl_fp8_e4m3fn.safetensors"
AE   = "ae.safetensors"
LORA = "stdstyl_chroma_lora.safetensors"
TRIGGER = "stdstyl"
NEG = "low quality, blurry, watermark, jpeg artifacts"
SEED = 7; STEPS = 26; CFG = 4.0
HELDOUT = ["a tall sailing ship", "a steam locomotive", "a portrait of a bearded man"]

def post(p, payload):
    req = urllib.request.Request(HOST + p, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r: return json.loads(r.read())
def get(p):
    with urllib.request.urlopen(HOST + p, timeout=120) as r: return json.loads(r.read())

def _common(model_src, prompt, prefix):
    # model_src = node ref producing MODEL (post-LoRA or raw UNET)
    return {
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": T5, "type": "chroma", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": AE}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": NEG}},
        "8": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": model_src, "shift": 1.0}},
        "9": {"class_type": "CFGGuider", "inputs": {"model": ["8", 0], "positive": ["6", 0], "negative": ["7", 0], "cfg": CFG}},
        "10": {"class_type": "RandomNoise", "inputs": {"noise_seed": SEED}},
        "11": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler"}},
        "12": {"class_type": "BasicScheduler", "inputs": {"model": ["8", 0], "scheduler": "beta", "steps": STEPS, "denoise": 1.0}},
        "13": {"class_type": "EmptySD3LatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "14": {"class_type": "SamplerCustomAdvanced", "inputs": {"noise": ["10", 0], "guider": ["9", 0], "sampler": ["11", 0], "sigmas": ["12", 0], "latent_image": ["13", 0]}},
        "15": {"class_type": "VAEDecode", "inputs": {"samples": ["14", 0], "vae": ["3", 0]}},
        "16": {"class_type": "SaveImage", "inputs": {"images": ["15", 0], "filename_prefix": prefix}},
    }

def base_graph(prompt, prefix):
    g = {"1": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}}}
    g.update(_common(["1", 0], prompt, prefix))   # raw UNET, no LoRA
    return g

def lora_graph(prompt, prefix):
    g = {"1": {"class_type": "UNETLoader", "inputs": {"unet_name": UNET, "weight_dtype": "default"}},
         "4": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": LORA, "strength_model": 1.0}}}
    g.update(_common(["4", 0], prompt, prefix))   # model from LoRA
    return g

def run(g):
    r = post("/prompt", {"prompt": g, "client_id": CID})
    if r.get("node_errors"): raise RuntimeError("node_errors: " + json.dumps(r["node_errors"]))
    pid = r["prompt_id"]
    while True:
        h = get("/history/" + pid)
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") != "success": raise RuntimeError("exec: " + json.dumps(st)[:400])
            return h[pid]["outputs"]["16"]["images"][0]["filename"]
        time.sleep(0.2)

def main():
    for i, subj in enumerate(HELDOUT):
        a = run(base_graph(f"{TRIGGER}, {subj}", f"CH_A_{i}")); print(f"[{i}] A base+trigger (no LoRA): {a}")
        b = run(lora_graph(subj, f"CH_B_{i}"));                 print(f"[{i}] B LoRA, no trigger      : {b}")
        c = run(lora_graph(f"{TRIGGER}, {subj}", f"CH_C_{i}")); print(f"[{i}] C LoRA + trigger        : {c}")
    print("\nDone. B (no trigger) vs C (trigger): style in C; and does the cyanotype BLUE survive on Chroma?")

if __name__ == "__main__":
    main()
