#!/usr/bin/env python3
"""Path A engine proof: generate a NEUTRAL, non-canon style dataset (cyanotype blueprint) via ComfyUI Z-Image-Turbo.

Style LoRA discipline (vs #151's subject LoRA):
  - Consistent STYLE (cyanotype blueprint), VARIED subjects -> the LoRA learns the style, not a subject.
  - Caption = "<TRIGGER>, <subject>"  (trigger carries the style; NO style words in the caption)
    so the style binds to the semantically-empty trigger token, not to any real word.
  - Folder class_token is NEUTRAL ("neutralset"), so if captions are read the trigger comes ONLY
    from captions; if captions were (wrongly) ignored, the A/B with the trigger would fail loudly.
Reuses the EXACT proven #151 Z-Image graph (UNETLoader nvfp4 + lumina2 CLIP + ae VAE).
"""
import json, time, urllib.request, os, shutil
HOST = "http://127.0.0.1:8188"; CID = "datagen_stdstyl"
DST = r"E:\AI\training\dataset_stdstyl\10_neutralset"
COMFY_OUT = r"E:\AI-Models\ComfyUI_windows_portable\ComfyUI\output"
os.makedirs(DST, exist_ok=True)
TRIGGER = "stdstyl"
# 16 varied, non-canon subjects with distinct silhouettes (NOT held-out: ship/locomotive/portrait are reserved for A/B).
SUBJECTS = [
    "a teapot", "a sitting fox", "a bicycle", "a potted cactus",
    "an owl on a branch", "a vintage camera", "a mushroom", "a lighthouse",
    "a hot air balloon", "an acoustic guitar", "a wristwatch", "a small songbird",
    "a maple leaf", "a coffee mug", "a pair of boots", "a desk lamp",
]
# Style words live ONLY in the generation prompt, never in the kohya caption.
STYLE = "cyanotype blueprint, white ink line drawing on deep prussian blue paper, monochrome cyan-blue, vintage technical blueprint, flat, centered"

def post(p, payload):
    req = urllib.request.Request(HOST + p, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r: return json.loads(r.read())
def get(p):
    with urllib.request.urlopen(HOST + p, timeout=120) as r: return json.loads(r.read())

def graph(subject, seed, prefix):
    return {
        "10": {"class_type": "UNETLoader", "inputs": {"unet_name": "z_image_turbo_nvfp4.safetensors", "weight_dtype": "default"}},
        "11": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen_3_4b.safetensors", "type": "lumina2", "device": "default"}},
        "12": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
        "13": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["11", 0], "text": f"{subject}, {STYLE}"}},
        "14": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["13", 0]}},
        "15": {"class_type": "EmptySD3LatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "16": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["10", 0], "shift": 3.0}},
        "17": {"class_type": "KSampler", "inputs": {"model": ["16", 0], "positive": ["13", 0], "negative": ["14", 0],
               "latent_image": ["15", 0], "seed": seed, "steps": 8, "cfg": 1.0,
               "sampler_name": "res_multistep", "scheduler": "simple", "denoise": 1.0}},
        "18": {"class_type": "VAEDecode", "inputs": {"samples": ["17", 0], "vae": ["12", 0]}},
        "19": {"class_type": "SaveImage", "inputs": {"images": ["18", 0], "filename_prefix": prefix}},
    }

def run(g):
    r = post("/prompt", {"prompt": g, "client_id": CID})
    if r.get("node_errors"): raise RuntimeError("node_errors: " + json.dumps(r["node_errors"]))
    pid = r["prompt_id"]
    while True:
        h = get("/history/" + pid)
        if pid in h:
            return h[pid]["outputs"]["19"]["images"][0]["filename"]
        time.sleep(0.1)

def main():
    for i, subject in enumerate(SUBJECTS):
        fn = run(graph(subject, 2000 + i, f"stdstyl_{i:02d}"))
        shutil.copyfile(os.path.join(COMFY_OUT, fn), os.path.join(DST, f"img_{i:02d}.png"))
        with open(os.path.join(DST, f"img_{i:02d}.txt"), "w") as f:
            f.write(f"{TRIGGER}, {subject}")
        print(f"  [{i:02d}] {fn} -> img_{i:02d}.png  caption='{TRIGGER}, {subject}'")
    print(f"\n{len(SUBJECTS)} images + .txt captions -> {DST}")

if __name__ == "__main__":
    main()
