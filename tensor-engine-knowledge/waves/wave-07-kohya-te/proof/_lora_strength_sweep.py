#!/usr/bin/env python3
"""Diagnostic: is the cyanotype BLUE latent-but-weak in a LoRA (strength reveals it) or absent (needs retrain)?
Generate the SAME held-out subject WITH the trigger at increasing LoRA strength. If blue intensifies with
strength, it's in the weights -> inference fix. If it stays grayscale, blue wasn't trained -> recipe fix."""
import json, time, urllib.request, sys
HOST = "http://127.0.0.1:8188"; CID = "sweep"
LORA = sys.argv[1] if len(sys.argv) > 1 else "stdstyl_te_lora_v3.safetensors"
TRIGGER = "stdstyl"; NEG = "blurry, low quality, watermark"; SEED = 7
SUBJECTS = ["a tall sailing ship", "a portrait of a bearded man"]
STRENGTHS = [1.0, 1.4]

def post(p, payload):
    req = urllib.request.Request(HOST + p, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r: return json.loads(r.read())
def get(p):
    with urllib.request.urlopen(HOST + p, timeout=120) as r: return json.loads(r.read())

def graph(prompt, strength, prefix):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "2": {"class_type": "LoraLoader", "inputs": {"model": ["1", 0], "clip": ["1", 1],
              "lora_name": LORA, "strength_model": strength, "strength_clip": strength}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 1], "text": prompt}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 1], "text": NEG}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "6": {"class_type": "KSampler", "inputs": {"model": ["2", 0], "positive": ["3", 0], "negative": ["4", 0],
              "latent_image": ["5", 0], "seed": SEED, "steps": 25, "cfg": 7.0,
              "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0}},
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": prefix}},
    }

def run(g):
    r = post("/prompt", {"prompt": g, "client_id": CID})
    if r.get("node_errors"): raise RuntimeError("node_errors: " + json.dumps(r["node_errors"]))
    pid = r["prompt_id"]
    while True:
        h = get("/history/" + pid)
        if pid in h: return h[pid]["outputs"]["8"]["images"][0]["filename"]
        time.sleep(0.1)

for si, subj in enumerate(SUBJECTS):
    for st in STRENGTHS:
        fn = run(graph(f"{TRIGGER}, {subj}", st, f"SW_{si}_{int(st*10)}"))
        print(f"  {subj[:20]:20s} strength {st}: {fn}")
print("done")
