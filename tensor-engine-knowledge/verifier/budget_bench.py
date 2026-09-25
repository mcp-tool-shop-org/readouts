#!/usr/bin/env python3
"""Wave-5: token-budget-ADHERENCE baseline. Can a small local model compress text to <= N tokens
WITHOUT a hard cap (i.e. self-regulate)? llama-server reports completion_tokens (the model's own
tokenizer) so we score adherence directly. This decides whether a budget-adherence LoRA (Unsloth #155)
is worth training, or whether prompting alone suffices. Usage: budget_bench.py [base]"""
import json, time, urllib.request, sys, os
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:9090"
MODELS = ["qwen3-0.6b", "qwen3-1.7b", "qwen3-4b", "qwen3-14b"]
BUDGETS = [60, 120]
SOURCES = {
 "recipe": ("The official prebuilt Windows x64 CUDA-12 build of llama.cpp b9484 is Blackwell-correct and "
   "needs no CUDA toolkit, cmake, or Visual Studio. Extract the binary zip and the matching cudart pack into "
   "the same folder. Pick the CUDA-12 build, never CUDA-13, because 13.x crashes the sm_120 MMQ kernel and "
   "silently falls back to cuBLAS which runs about five times slower. Verify MMQ is engaged with llama-bench: "
   "a 30B-A3B MoE should report prefill in the thousands of tokens per second; if it reports around one "
   "thousand it fell back to cuBLAS and you should build from source with CUDA 12.8 instead."),
 "log": ("Loading the Ollama qwen3.6 blob into stock llama.cpp failed with the error: key "
   "qwen35moe.rope.dimension_sections has wrong array length, expected 4 got 3. The gemma4 blob also failed "
   "to load. Ollama runs its own inference engine now and its GGUF conversion diverges from upstream "
   "llama.cpp for the newest model architectures, so its blob store is not a drop-in source of GGUF files."),
 "design": ("Saint's Mile is a frontier JRPG rendered as a Rust terminal interface using ratatui and "
   "crossterm. The combat is a standoff system where positioning and initiative matter more than raw stats. "
   "The convoy and relay mechanics let the party move supplies between settlements while bandits and weather "
   "threaten the route. Galen Rook leads a cast that includes Eli Winter, Ada Mercer, and Rosa Varela across "
   "sixteen chapters from Cedar Wake to the Bitter Cut."),
}
def chat(model, text, budget):
    body = {"model": model, "temperature": 0, "max_tokens": 400,
            "messages": [
              {"role": "system", "content": f"You compress text. Rewrite the user's text as a summary of AT MOST {budget} tokens. Preserve the key facts. Output ONLY the summary, nothing else. /no_think"},
              {"role": "user", "content": text}]}
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read())
    ct = d["choices"][0]["message"]["content"]
    if "</think>" in ct: ct = ct.split("</think>")[-1]
    return d.get("usage", {}).get("completion_tokens", 0), ct.strip()
def main():
    res = {"runs": []}
    print(f"{'model':14}{'budget':>7}{'src':>9}{'got_tok':>9}{'overshoot':>11}  fit?")
    agg = {}
    for m in MODELS:
        for b in BUDGETS:
            fits = 0; ratios = []
            for sname, text in SOURCES.items():
                try:
                    got, out = chat(m, text, b)
                except Exception as e:
                    print(f"{m:14}{b:>7}{sname:>9}  ERROR {str(e)[:40]}"); continue
                ratio = got / b; ratios.append(ratio); fit = got <= b * 1.1
                fits += fit
                print(f"{m:14}{b:>7}{sname:>9}{got:>9}{ratio:>10.2f}x  {'YES' if fit else 'no'}")
                res["runs"].append({"model": m, "budget": b, "src": sname, "got": got, "ratio": round(ratio,2), "out": out})
            agg[(m,b)] = (fits, sum(ratios)/len(ratios) if ratios else 0)
    print(f"\n=== ADHERENCE SUMMARY (fit = got <= 1.1x budget; ratio = mean got/budget) ===")
    print(f"{'model':14}{'budget':>7}{'fit/3':>7}{'mean_overshoot':>16}")
    for (m,b),(fits,mr) in agg.items():
        print(f"{m:14}{b:>7}{str(fits)+'/3':>7}{mr:>15.2f}x")
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"budget-results.json"),"w"), indent=2)
    print("wrote budget-results.json")
if __name__ == "__main__": main()
