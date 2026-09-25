#!/usr/bin/env python3
"""Path A proof: does the TRIGGER FIRE through the trained text encoder?

3 cells per held-out subject (subjects NOT in the training set -> also tests generalization):
  A base        : SDXL base, no LoRA, prompt WITH trigger  -> trigger is meaningless to base (control)
  B lora_notrig : base + LoRA @1.0,   prompt WITHOUT trigger -> does style leak without the token?
  C lora_trig   : base + LoRA @1.0,   prompt WITH trigger    -> style should appear

Decisive comparison: B vs C (LoRA loaded for both, only the trigger token toggled).
If style appears in C but not B, the text encoder learned the token -> the trigger fires.
Same seed across all cells. Every image is LOOKED AT (look-at-images rule).
"""
import json, time, urllib.request
HOST = "http://127.0.0.1:8188"; CID = "loraval_stdstyl"
LORA = "stdstyl_te_lora_v3.safetensors"
TRIGGER = "stdstyl"
NEG = "blurry, low quality, watermark"
SEED = 7
# Held-out subjects: none were in the training set; portrait is a deliberate far-from-training stress test.
HELDOUT = ["a tall sailing ship", "a steam locomotive", "a portrait of a bearded man"]

def post(p, payload):
    req = urllib.request.Request(HOST + p, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r: return json.loads(r.read())
def get(p):
    with urllib.request.urlopen(HOST + p, timeout=120) as r: return json.loads(r.read())

def base_graph(prompt, prefix):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": prompt}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": NEG}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "6": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["3", 0], "negative": ["4", 0],
              "latent_image": ["5", 0], "seed": SEED, "steps": 25, "cfg": 7.0,
              "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0}},
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": prefix}},
    }

def lora_graph(prompt, prefix):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "2": {"class_type": "LoraLoader", "inputs": {"model": ["1", 0], "clip": ["1", 1],
              "lora_name": LORA, "strength_model": 1.0, "strength_clip": 1.0}},
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
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") != "success": raise RuntimeError("exec: " + json.dumps(st)[:300])
            return h[pid]["outputs"]["8"]["images"][0]["filename"]
        time.sleep(0.1)

def main():
    for i, subj in enumerate(HELDOUT):
        a = run(base_graph(f"{TRIGGER}, {subj}", f"A3_base_{i}"))
        print(f"[{i}] A base        (trigger, no LoRA) : {a}")
        b = run(lora_graph(subj, f"B3_lora_notrig_{i}"))
        print(f"[{i}] B lora_notrig (no trigger)      : {b}")
        c = run(lora_graph(f"{TRIGGER}, {subj}", f"C3_lora_trig_{i}"))
        print(f"[{i}] C lora_trig   (trigger)         : {c}")
    print("\nDone. Compare B (no trigger) vs C (trigger): style in C only => trigger fires.")

if __name__ == "__main__":
    main()
