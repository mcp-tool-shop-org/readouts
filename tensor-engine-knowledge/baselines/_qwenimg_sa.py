#!/usr/bin/env python3
"""Wave-5: SA-2.2 on Qwen-Image-2512 — the WORKING backends (fp8_cuda, fp16_triton) vs the 18.08s floor.
fp16_cuda crashes (kernel bug, proven on Z-Image too). Crash-resilient; saves images."""
import json, time, urllib.request, os
HOST="http://127.0.0.1:8188"; CID="qwensa"
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"qwenimg-sa-results.json")
POS=('A weathered wooden tavern signboard hanging from an iron bracket, carved relief letters reading '
     '"STUDIO TEST 2512" painted in gold leaf, warm lantern light, painterly fantasy illustration, '
     'crisp detail, original concept art')
NEG="blurry, low quality, distorted, watermark, text errors, deformed"
def post(p,payload):
    req=urllib.request.Request(HOST+p,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=600) as r: return json.loads(r.read())
def get(p):
    with urllib.request.urlopen(HOST+p,timeout=120) as r: return json.loads(r.read())
def wait_ready(t=120):
    t0=time.time()
    while time.time()-t0<t:
        try: get("/object_info/KSampler"); return
        except Exception: time.sleep(1.0)
    raise RuntimeError("not ready")
def graph(backend,prefix,seed,steps=20):
    g={"1":{"class_type":"UNETLoader","inputs":{"unet_name":"qwen_image_2512_fp8_e4m3fn.safetensors","weight_dtype":"default"}},
       "2":{"class_type":"CLIPLoader","inputs":{"clip_name":"qwen_2.5_vl_7b.safetensors","type":"qwen_image","device":"default"}},
       "3":{"class_type":"VAELoader","inputs":{"vae_name":"qwen_image_vae.safetensors"}},
       "4":{"class_type":"CLIPTextEncode","inputs":{"clip":["2",0],"text":POS}},
       "5":{"class_type":"CLIPTextEncode","inputs":{"clip":["2",0],"text":NEG}},
       "6":{"class_type":"EmptySD3LatentImage","inputs":{"width":1024,"height":1024,"batch_size":1}},
       "7":{"class_type":"ModelSamplingAuraFlow","inputs":{"model":["1",0],"shift":3.0}},
       "8":{"class_type":"KSampler","inputs":{"model":["7",0],"positive":["4",0],"negative":["5",0],
            "latent_image":["6",0],"seed":seed,"steps":steps,"cfg":2.5,"sampler_name":"euler","scheduler":"simple","denoise":1.0}},
       "9":{"class_type":"VAEDecode","inputs":{"samples":["8",0],"vae":["3",0]}},
       "10":{"class_type":"SaveImage","inputs":{"images":["9",0],"filename_prefix":prefix}}}
    if backend:
        g["11"]={"class_type":"PathchSageAttentionKJ","inputs":{"model":["1",0],"sage_attention":backend,"allow_compile":False}}
        g["7"]["inputs"]["model"]=["11",0]
    return g
def run(g):
    t0=time.time(); r=post("/prompt",{"prompt":g,"client_id":CID})
    if r.get("node_errors"): raise RuntimeError("node_errors: "+json.dumps(r["node_errors"])[:400])
    pid=r["prompt_id"]
    while True:
        h=get("/history/"+pid)
        if pid in h:
            st=h[pid].get("status",{})
            if st.get("status_str")!="success": raise RuntimeError("exec: "+json.dumps(st)[:400])
            fn=None
            for n in h[pid].get("outputs",{}).values():
                for im in n.get("images",[]): fn=im.get("filename")
            return time.time()-t0,fn
        time.sleep(0.1)
def bench(label,backend,prefix,res,iters=2,seed0=42):
    print(f"\n>>> {label}"); times=[]; img=None
    for i in range(iters):
        try:
            dt,fn=run(graph(backend,prefix,seed0+i)); times.append(dt); img=fn; print(f"    iter{i}: {dt:.2f}s/img -> {fn}")
        except Exception as e:
            print(f"    iter{i} FAILED {type(e).__name__}: {str(e)[:180]}")
            res["runs"].append({"label":label,"error":str(e)[:200],"times":times}); json.dump(res,open(OUT,"w"),indent=2); return False
    res["runs"].append({"label":label,"times":times,"min":min(times),"img":img}); json.dump(res,open(OUT,"w"),indent=2); return True
def main():
    wait_ready()
    res={"floor_sec":18.08,"runs":[]}
    print(">>> warmup (load 20GB model)"); dt,_=run(graph(None,"qwsa_warm",7)); print(f"   {dt:.1f}s")
    if bench("SA-2.2 fp8_cuda","sageattn_qk_int8_pv_fp8_cuda","qwsa_fp8",res):
        bench("SA-2.2 fp16_triton","sageattn_qk_int8_pv_fp16_triton","qwsa_triton",res)
    json.dump(res,open(OUT,"w"),indent=2)
    print("\n=== QWEN-IMAGE SA vs floor 18.08s ===")
    for r in res["runs"]:
        if r.get("error"): print(f"  {r['label']:22} ERROR {r['error'][:50]}")
        else: print(f"  {r['label']:22} min {r['min']:.2f}s ({100*(1-r['min']/18.08):.0f}% vs floor) img={r.get('img')}")
    print("wrote",OUT)
if __name__=="__main__": main()
