#!/usr/bin/env python3
"""Wave-5: show SA-2.2.0's win SCALES with attention share. Z-Image-Turbo nvfp4, floor vs SA-fp8_cuda,
across resolution (token count ~ (res/16)^2; attention is O(n^2) so its share grows with resolution).
At 1024^2/8-step attention is a small slice -> ~10% win. Higher res -> attention dominates -> bigger win."""
import json, time, urllib.request, os
HOST="http://127.0.0.1:8188"; CID="sa2res"
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"sage2-res-results.json")
PROMPT="2.5D JRPG key art: a lone frontier traveler at a windswept mesa overlook at golden hour, painterly, original"
def post(p,payload):
    req=urllib.request.Request(HOST+p,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=900) as r: return json.loads(r.read())
def get(p):
    with urllib.request.urlopen(HOST+p,timeout=120) as r: return json.loads(r.read())
def graph(backend,prefix,seed,w,h):
    g={"10":{"class_type":"UNETLoader","inputs":{"unet_name":"z_image_turbo_nvfp4.safetensors","weight_dtype":"default"}},
       "11":{"class_type":"CLIPLoader","inputs":{"clip_name":"qwen_3_4b.safetensors","type":"lumina2","device":"default"}},
       "12":{"class_type":"VAELoader","inputs":{"vae_name":"ae.safetensors"}},
       "13":{"class_type":"CLIPTextEncode","inputs":{"clip":["11",0],"text":PROMPT}},
       "14":{"class_type":"ConditioningZeroOut","inputs":{"conditioning":["13",0]}},
       "15":{"class_type":"EmptySD3LatentImage","inputs":{"width":w,"height":h,"batch_size":1}},
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
    if r.get("node_errors"): raise RuntimeError("node_errors: "+json.dumps(r["node_errors"])[:200])
    pid=r["prompt_id"]
    while True:
        h=get("/history/"+pid)
        if pid in h:
            if h[pid].get("status",{}).get("status_str")!="success": raise RuntimeError("exec fail")
            return time.time()-t0
        time.sleep(0.05)
def measure(backend,prefix,w,h,iters=3):
    ts=[]
    for i in range(iters):
        try: ts.append(run(graph(backend,prefix,1000+i,w,h)))
        except Exception as e: print(f"    {prefix} iter{i} FAIL {str(e)[:80]}"); return None
    return min(ts[1:]) if len(ts)>1 else min(ts)  # drop first (compile/alloc)
def main():
    res={"runs":[]}
    print(">>> warmup"); run(graph(None,"w",7,1024,1024))
    for (w,h) in [(1024,1024),(1536,1536),(2048,2048)]:
        fl=measure(None,f"r{w}_floor",w,h)
        sa=measure("sageattn_qk_int8_pv_fp8_cuda",f"r{w}_sa",w,h)
        if fl and sa:
            win=100*(fl-sa)/fl
            print(f"  {w}x{h}: floor {fl:.3f}s  SA-fp8 {sa:.3f}s  ->  {win:.1f}% faster")
            res["runs"].append({"res":w,"floor":round(fl,3),"sa_fp8":round(sa,3),"win_pct":round(win,1)})
        else:
            print(f"  {w}x{h}: incomplete (floor={fl}, sa={sa})")
            res["runs"].append({"res":w,"floor":fl,"sa_fp8":sa})
    json.dump(res,open(OUT,"w"),indent=2); print("wrote",OUT)
if __name__=="__main__": main()
