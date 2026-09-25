#!/usr/bin/env python3
"""Wave-5: SA 2.2.0 backend sweep on Z-Image-Turbo (the #147 daily-driver baseline).
fp16_cuda CRASHED ComfyUI (Lumina2 head_dim unsupported by the int8 CUDA kernel). Test the
safe backends. Saves incrementally so a crash preserves prior results.
Floor this session: bf16 2.64 / nvfp4 1.39 s/img. #148 SA-1.0.6-auto: bf16 2.60 / nvfp4 1.32."""
import json, time, urllib.request, os, sys
HOST="http://127.0.0.1:8188"; CID="sa2z"
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"sage2-zimage-results.json")
PROMPT=("2.5D JRPG key art: a lone frontier traveler in a worn duster coat stands at a "
        "windswept mesa overlook at golden hour, distant canyon town below, painterly "
        "stylized, warm cinematic rim light, crisp detail, original concept")
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
def graph(unet,backend,prefix,seed):
    g={"10":{"class_type":"UNETLoader","inputs":{"unet_name":unet,"weight_dtype":"default"}},
       "11":{"class_type":"CLIPLoader","inputs":{"clip_name":"qwen_3_4b.safetensors","type":"lumina2","device":"default"}},
       "12":{"class_type":"VAELoader","inputs":{"vae_name":"ae.safetensors"}},
       "13":{"class_type":"CLIPTextEncode","inputs":{"clip":["11",0],"text":PROMPT}},
       "14":{"class_type":"ConditioningZeroOut","inputs":{"conditioning":["13",0]}},
       "15":{"class_type":"EmptySD3LatentImage","inputs":{"width":1024,"height":1024,"batch_size":1}},
       "16":{"class_type":"ModelSamplingAuraFlow","inputs":{"model":["10",0],"shift":3.0}},
       "17":{"class_type":"KSampler","inputs":{"model":["16",0],"positive":["13",0],"negative":["14",0],
             "latent_image":["15",0],"seed":seed,"steps":8,"cfg":1.0,"sampler_name":"res_multistep","scheduler":"simple","denoise":1.0}},
       "18":{"class_type":"VAEDecode","inputs":{"samples":["17",0],"vae":["12",0]}},
       "19":{"class_type":"SaveImage","inputs":{"images":["18",0],"filename_prefix":prefix}}}
    if backend:
        g["20"]={"class_type":"PathchSageAttentionKJ","inputs":{"model":["10",0],"sage_attention":backend,"allow_compile":False}}
        g["16"]["inputs"]["model"]=["20",0]
    return g
def run(g):
    t0=time.time(); r=post("/prompt",{"prompt":g,"client_id":CID})
    if r.get("node_errors"): raise RuntimeError("node_errors: "+json.dumps(r["node_errors"])[:300])
    pid=r["prompt_id"]
    while True:
        h=get("/history/"+pid)
        if pid in h:
            st=h[pid].get("status",{})
            if st.get("status_str")!="success": raise RuntimeError("exec: "+json.dumps(st)[:300])
            return time.time()-t0
        time.sleep(0.05)
def bench(label,unet,backend,prefix,res,iters=3,seed0=42):
    print(f"\n>>> {label}"); times=[]
    for i in range(iters):
        try:
            dt=run(graph(unet,backend,prefix,seed0+i)); times.append(dt); print(f"    iter{i}: {dt:.3f}s/img ({8/dt:.2f} it/s)")
        except Exception as e:
            print(f"    iter{i} FAILED: {type(e).__name__}: {str(e)[:160]}")
            res["runs"].append({"label":label,"backend":backend,"error":str(e)[:200],"times":times}); save(res); return False
    res["runs"].append({"label":label,"backend":backend,"times":times,"min":min(times)}); save(res); return True
def save(res): json.dump(res,open(OUT,"w"),indent=2)
def main():
    wait_ready()
    res={"started":time.time(),"floor_this_session":{"bf16":2.64,"nvfp4":1.39},"runs":[]}
    print(">>> WARM-UP"); print(f"    {run(graph('z_image_turbo_bf16.safetensors',None,'warm',7)):.2f}s")
    # backends to sweep (fp16_cuda excluded - it crashes; we know that)
    for be in ["sageattn_qk_int8_pv_fp16_triton","sageattn_qk_int8_pv_fp8_cuda"]:
        ok=bench(f"bf16  / SA-2.2 ({be})","z_image_turbo_bf16.safetensors",be,"z_"+be[-10:]+"_bf16",res)
        if ok: bench(f"nvfp4 / SA-2.2 ({be})","z_image_turbo_nvfp4.safetensors",be,"z_"+be[-10:]+"_fp4",res)
        else: print(f"    (backend {be} crashed/failed; server may be down - stopping sweep)"); break
    res["ended"]=time.time(); save(res)
    print("\n=== Z-IMAGE SA-2.2 SWEEP (floor bf16 2.64 / nvfp4 1.39 ; #148 SA1.0.6 bf16 2.60 / nvfp4 1.32) ===")
    for r in res["runs"]:
        if r.get("error"): print(f"  {r['label']:46} ERROR {r['error'][:60]}")
        else: print(f"  {r['label']:46} min {r['min']:.3f}s/img all={[round(t,2) for t in r['times']]}")
    print("wrote",OUT)
if __name__=="__main__": main()
