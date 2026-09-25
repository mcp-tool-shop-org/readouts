#!/usr/bin/env python3
"""Wave-5 diffusion baseline: Chroma1-HD (fp8mixed) on ComfyUI. SamplerCustomAdvanced chain (RandomNoise
-> CFGGuider -> SamplerCustomAdvanced + BasicScheduler sigmas). Light model (9GB) so SA + higher-res have
headroom. Floor + SA fp8_cuda; saves images. Crash-resilient."""
import json, time, urllib.request, os, sys
HOST="http://127.0.0.1:8188"; CID="chroma"
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"chroma-results.json")
POS=("A nature documentary close-up photograph of a red fox in autumn forest, highly detailed fur, "
     "sharp amber eyes, soft natural light, shallow depth of field, professional wildlife photography")
NEG=("low quality, blurry, greyscale, sketch, chromatic aberration, oversaturated, bloom, flat colors, "
     "bold outlines, cartoon, deformed")
def post(p,payload):
    req=urllib.request.Request(HOST+p,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=600) as r: return json.loads(r.read())
def get(p):
    with urllib.request.urlopen(HOST+p,timeout=120) as r: return json.loads(r.read())
def wait_ready(t=120):
    t0=time.time()
    while time.time()-t0<t:
        try: get("/object_info/SamplerCustomAdvanced"); return
        except Exception: time.sleep(1.0)
    raise RuntimeError("not ready")
def graph(backend,prefix,seed,w=1024,h=1024,steps=26,cfg=4.0):
    g={"1":{"class_type":"UNETLoader","inputs":{"unet_name":"Chroma1-HD-fp8mixed.safetensors","weight_dtype":"default"}},
       "2":{"class_type":"CLIPLoader","inputs":{"clip_name":"t5xxl_fp8_e4m3fn.safetensors","type":"chroma","device":"default"}},
       "3":{"class_type":"VAELoader","inputs":{"vae_name":"ae.safetensors"}},
       "4":{"class_type":"CLIPTextEncode","inputs":{"clip":["2",0],"text":POS}},
       "5":{"class_type":"CLIPTextEncode","inputs":{"clip":["2",0],"text":NEG}},
       "6":{"class_type":"EmptySD3LatentImage","inputs":{"width":w,"height":h,"batch_size":1}},
       "7":{"class_type":"ModelSamplingAuraFlow","inputs":{"model":["1",0],"shift":1.0}},
       "8":{"class_type":"KSamplerSelect","inputs":{"sampler_name":"euler"}},
       "9":{"class_type":"BasicScheduler","inputs":{"model":["7",0],"scheduler":"simple","steps":steps,"denoise":1.0}},
       "10":{"class_type":"RandomNoise","inputs":{"noise_seed":seed}},
       "11":{"class_type":"CFGGuider","inputs":{"model":["7",0],"positive":["4",0],"negative":["5",0],"cfg":cfg}},
       "12":{"class_type":"SamplerCustomAdvanced","inputs":{"noise":["10",0],"guider":["11",0],"sampler":["8",0],"sigmas":["9",0],"latent_image":["6",0]}},
       "13":{"class_type":"VAEDecode","inputs":{"samples":["12",0],"vae":["3",0]}},
       "14":{"class_type":"SaveImage","inputs":{"images":["13",0],"filename_prefix":prefix}}}
    if backend:
        g["15"]={"class_type":"PathchSageAttentionKJ","inputs":{"model":["1",0],"sage_attention":backend,"allow_compile":False}}
        g["7"]["inputs"]["model"]=["15",0]
    return g
def run(g):
    t0=time.time(); r=post("/prompt",{"prompt":g,"client_id":CID})
    if r.get("node_errors"): raise RuntimeError("node_errors: "+json.dumps(r["node_errors"])[:500])
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
def bench(label,backend,prefix,res,iters=2,seed0=42,**kw):
    print(f"\n>>> {label}"); times=[]; img=None
    for i in range(iters):
        try:
            dt,fn=run(graph(backend,prefix,seed0+i,**kw)); times.append(dt); img=fn; print(f"    iter{i}: {dt:.2f}s/img -> {fn}")
        except Exception as e:
            print(f"    iter{i} FAILED {type(e).__name__}: {str(e)[:260]}")
            res["runs"].append({"label":label,"error":str(e)[:300],"times":times}); json.dump(res,open(OUT,"w"),indent=2); return False
    res["runs"].append({"label":label,"times":times,"min":min(times),"img":img}); json.dump(res,open(OUT,"w"),indent=2); return True
def main():
    wait_ready()
    res={"model":"Chroma1-HD-fp8mixed","settings":"1024^2, 26-step euler, cfg4, SamplerCustomAdvanced","runs":[]}
    print(">>> warmup (loads 9GB model)")
    try: dt,fn=run(graph(None,"chroma_warm",7)); print(f"   {dt:.1f}s -> {fn}")
    except Exception as e: print(f"   WARMUP FAILED: {str(e)[:300]}"); json.dump({"warmup_error":str(e)[:400]},open(OUT,"w")); return
    bench("FLOOR (cuDNN-SDPA)",None,"chroma_floor",res)
    bench("SA-2.2 fp8_cuda","sageattn_qk_int8_pv_fp8_cuda","chroma_sa_fp8",res)
    json.dump(res,open(OUT,"w"),indent=2)
    print("\n=== CHROMA1-HD SUMMARY ===")
    fl=next((r['min'] for r in res['runs'] if 'FLOOR' in r['label'] and 'min' in r),None)
    for r in res["runs"]:
        if r.get("error"): print(f"  {r['label']:24} ERROR {r['error'][:60]}")
        else:
            tag=f" ({100*(1-r['min']/fl):.0f}% vs floor)" if fl and 'FLOOR' not in r['label'] else ""
            print(f"  {r['label']:24} min {r['min']:.2f}s/img{tag} img={r.get('img')}")
    print("wrote",OUT)
if __name__=="__main__": main()
