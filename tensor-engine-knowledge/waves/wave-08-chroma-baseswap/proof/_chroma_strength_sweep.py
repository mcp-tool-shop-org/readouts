#!/usr/bin/env python3
"""Is the cyanotype BLUE latent-but-weak in the Chroma LoRA? Sweep LoRA strength on the two clearest cases
(portrait = went monochrome; ship = had some blue), trigger ON. If blue saturates with strength -> latent (inference fix);
if it stays linework -> under-trained (recipe fix)."""
import json, time, urllib.request
HOST="http://127.0.0.1:8188"; CID="chroma_sweep"
UNET="Chroma1-HD-fp8mixed.safetensors"; T5="t5xxl_fp8_e4m3fn.safetensors"; AE="ae.safetensors"
LORA="stdstyl_chroma_lora.safetensors"; TRIGGER="stdstyl"
NEG="low quality, blurry, watermark"; SEED=7; STEPS=26; CFG=4.0
SUBJECTS=["a portrait of a bearded man","a tall sailing ship"]
STRENGTHS=[1.0,1.5,2.0]

def post(p,pl):
    r=urllib.request.Request(HOST+p,data=json.dumps(pl).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(r,timeout=600) as x: return json.loads(x.read())
def get(p):
    with urllib.request.urlopen(HOST+p,timeout=120) as x: return json.loads(x.read())

def graph(prompt,strength,prefix):
    return {
      "1":{"class_type":"UNETLoader","inputs":{"unet_name":UNET,"weight_dtype":"default"}},
      "4":{"class_type":"LoraLoaderModelOnly","inputs":{"model":["1",0],"lora_name":LORA,"strength_model":strength}},
      "2":{"class_type":"CLIPLoader","inputs":{"clip_name":T5,"type":"chroma","device":"default"}},
      "3":{"class_type":"VAELoader","inputs":{"vae_name":AE}},
      "6":{"class_type":"CLIPTextEncode","inputs":{"clip":["2",0],"text":prompt}},
      "7":{"class_type":"CLIPTextEncode","inputs":{"clip":["2",0],"text":NEG}},
      "8":{"class_type":"ModelSamplingAuraFlow","inputs":{"model":["4",0],"shift":1.0}},
      "9":{"class_type":"CFGGuider","inputs":{"model":["8",0],"positive":["6",0],"negative":["7",0],"cfg":CFG}},
      "10":{"class_type":"RandomNoise","inputs":{"noise_seed":SEED}},
      "11":{"class_type":"KSamplerSelect","inputs":{"sampler_name":"euler"}},
      "12":{"class_type":"BasicScheduler","inputs":{"model":["8",0],"scheduler":"beta","steps":STEPS,"denoise":1.0}},
      "13":{"class_type":"EmptySD3LatentImage","inputs":{"width":1024,"height":1024,"batch_size":1}},
      "14":{"class_type":"SamplerCustomAdvanced","inputs":{"noise":["10",0],"guider":["9",0],"sampler":["11",0],"sigmas":["12",0],"latent_image":["13",0]}},
      "15":{"class_type":"VAEDecode","inputs":{"samples":["14",0],"vae":["3",0]}},
      "16":{"class_type":"SaveImage","inputs":{"images":["15",0],"filename_prefix":prefix}},
    }
def run(g):
    r=post("/prompt",{"prompt":g,"client_id":CID})
    if r.get("node_errors"): raise RuntimeError(json.dumps(r["node_errors"]))
    pid=r["prompt_id"]
    while True:
        h=get("/history/"+pid)
        if pid in h: return h[pid]["outputs"]["16"]["images"][0]["filename"]
        time.sleep(0.2)
for si,subj in enumerate(SUBJECTS):
    for st in STRENGTHS:
        fn=run(graph(f"{TRIGGER}, {subj}",st,f"CHSW_{si}_{int(st*10)}"))
        print(f"  {subj[:18]:18s} str {st}: {fn}")
print("done")
