#!/usr/bin/env python3
"""Path A v3: generate REGULARIZATION images to teach the trigger to GATE the style.

Prior-preservation contrast:
  train: "stdstyl, a teapot"  -> cyanotype (style present, trigger present)
  reg:   "a teapot"           -> normal full color (style ABSENT, trigger ABSENT)
The ONLY difference between the two captions is the trigger token, so the model
attributes the entire style delta to `stdstyl` -> style fires ONLY with the trigger.
Same 16 subjects as the train set; clearly NON-cyanotype (full color), no paper border.
"""
import json, time, urllib.request, os, shutil
HOST = "http://127.0.0.1:8188"; CID = "reggen_stdstyl"
DST = r"E:\AI\training\reg_stdstyl\10_object"
COMFY_OUT = r"E:\AI-Models\ComfyUI_windows_portable\ComfyUI\output"
os.makedirs(DST, exist_ok=True)
SUBJECTS = [
    "a teapot", "a sitting fox", "a bicycle", "a potted cactus",
    "an owl on a branch", "a vintage camera", "a mushroom", "a lighthouse",
    "a hot air balloon", "an acoustic guitar", "a wristwatch", "a small songbird",
    "a maple leaf", "a coffee mug", "a pair of boots", "a desk lamp",
]
NORMAL = "full color illustration, natural colors, soft studio lighting, plain white background, centered"

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
        "13": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["11", 0], "text": f"{subject}, {NORMAL}"}},
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
        fn = run(graph(subject, 3000 + i, f"reg_{i:02d}"))
        shutil.copyfile(os.path.join(COMFY_OUT, fn), os.path.join(DST, f"img_{i:02d}.png"))
        with open(os.path.join(DST, f"img_{i:02d}.txt"), "w") as f:
            f.write(subject)  # NO trigger -> this is the contrast
        print(f"  [{i:02d}] {fn} -> img_{i:02d}.png  caption='{subject}' (no trigger)")
    print(f"\n{len(SUBJECTS)} reg images + .txt captions -> {DST}")

if __name__ == "__main__":
    main()
