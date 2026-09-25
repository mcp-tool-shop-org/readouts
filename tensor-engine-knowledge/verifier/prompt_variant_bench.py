#!/usr/bin/env python3
"""Wave-5: before training a budget-adherence LoRA, can PROMPTING alone close the gap? Models often hit
WORD/SENTENCE targets better than TOKEN targets. Hard case = compress dense text to ~60 tokens.
Variants: token-budget vs word-budget vs sentence-budget. If a variant reliably lands <=66 tok, no LoRA needed."""
import json, time, urllib.request, sys, os
BASE = "http://127.0.0.1:9090"
MODELS = ["qwen3-1.7b", "qwen3-4b"]
TARGET = 60  # tokens; fit = got <= 66
SOURCES = {
 "recipe": ("The official prebuilt Windows x64 CUDA-12 build of llama.cpp b9484 is Blackwell-correct and "
   "needs no CUDA toolkit, cmake, or Visual Studio. Extract the binary zip and the matching cudart pack into "
   "the same folder. Pick the CUDA-12 build, never CUDA-13, because 13.x crashes the sm_120 MMQ kernel and "
   "silently falls back to cuBLAS which runs about five times slower."),
 "design": ("Saint's Mile is a frontier JRPG rendered as a Rust terminal interface using ratatui and "
   "crossterm. Combat is a standoff system where positioning and initiative matter more than raw stats. "
   "Convoy and relay mechanics move supplies between settlements while bandits and weather threaten the route."),
}
VARIANTS = {
 "token(<=60)":    "Rewrite the user's text as a summary of AT MOST 60 tokens. Preserve key facts. Output ONLY the summary. /no_think",
 "word(<=45)":     "Rewrite the user's text as a summary of AT MOST 45 words. Preserve key facts. Output ONLY the summary. /no_think",
 "sentence(<=2)":  "Rewrite the user's text as AT MOST 2 short sentences. Preserve key facts. Output ONLY the summary. /no_think",
}
def chat(model, sysmsg, text):
    body = {"model": model, "temperature": 0, "max_tokens": 300,
            "messages": [{"role":"system","content":sysmsg},{"role":"user","content":text}]}
    req = urllib.request.Request(BASE+"/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=300) as r: d=json.loads(r.read())
    ct=d["choices"][0]["message"]["content"]
    if "</think>" in ct: ct=ct.split("</think>")[-1]
    return d.get("usage",{}).get("completion_tokens",0), ct.strip()
def main():
    print(f"{'model':12}{'variant':16}{'src':>9}{'got':>6}  fit(<=66)?")
    agg={}
    for m in MODELS:
        for vname,vsys in VARIANTS.items():
            fits=0
            for sname,text in SOURCES.items():
                got,out=chat(m,vsys,text)
                fit=got<=66; fits+=fit
                print(f"{m:12}{vname:16}{sname:>9}{got:>6}  {'YES' if fit else 'no'}")
            agg[(m,vname)]=fits
    print(f"\n=== fit rate (got <= 66 tok) per (model, variant) ===")
    for (m,v),f in agg.items(): print(f"  {m:12}{v:16}{f}/2")
    json.dump(agg.__repr__(), open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"variant-results.json"),"w"))
if __name__=="__main__": main()
