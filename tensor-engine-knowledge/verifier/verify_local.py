#!/usr/bin/env python3
"""Wave-5: local FAMILY-DIFFERENT verifier on llama-swap. The generator is Claude; the verifier is a
local non-Claude model (Qwen, Apache-2.0) served natively via llama-swap. Grounded entailment:
given CLAIM + EVIDENCE only (the generator's reasoning is HIDDEN), return a constrained-JSON verdict.
This is the EXTERNAL_VERIFIER the workflow-standards + study-swarm protocol want, now standable because
wave-5 stood up llama-swap. Usage: verify_local.py [model] [llama-swap-base]"""
import json, time, urllib.request, sys, os

MODEL = sys.argv[1] if len(sys.argv) > 1 else "qwen3-30b-a3b"
BASE  = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:9090"
THINK = len(sys.argv) > 3 and sys.argv[3] == "think"   # allow the verifier to reason (no grammar, strip <think>)
HERE  = os.path.dirname(os.path.abspath(__file__))
CLAIMS = json.load(open(os.path.join(HERE, "claims.json")))

SYS = ("You are a STRICT fact-checking verifier. You are given a CLAIM and a piece of EVIDENCE. "
       "Decide, using ONLY the evidence, whether the evidence supports the claim. Do NOT use any outside "
       "knowledge and do NOT guess beyond what the evidence states.\n"
       "- 'supported': the evidence clearly entails the claim.\n"
       "- 'refuted': the evidence contradicts the claim.\n"
       "- 'insufficient': the evidence does not address the claim or is not enough to decide.\n"
       "If the claim sounds plausible but the evidence does not actually establish it, you MUST say "
       "'insufficient' or 'refuted'. Treat the claim as 'supported' when the evidence's facts or numbers "
       "logically entail it, even via one obvious step. Answer with the JSON object only.")

def extract_json(s):
    try: return json.loads(s)
    except Exception: pass
    # strip a qwen <think>...</think> block if present, then grab the last {...}
    if "</think>" in s: s = s.split("</think>")[-1]
    i, j = s.find("{"), s.rfind("}")
    if i >= 0 and j > i: return json.loads(s[i:j+1])
    raise ValueError(f"no JSON in: {s[:80]!r}")

SCHEMA = {"type": "object", "properties": {
    "verdict": {"type": "string", "enum": ["supported", "refuted", "insufficient"]},
    "confidence": {"type": "number"},
    "rationale": {"type": "string"}}, "required": ["verdict", "confidence", "rationale"]}

def call(claim, evidence):
    sysmsg = SYS if THINK else SYS + " /no_think"
    body = {"model": MODEL, "temperature": 0, "max_tokens": 2048 if THINK else 700,
            "messages": [{"role": "system", "content": sysmsg},
                         {"role": "user", "content": f"CLAIM:\n{claim}\n\nEVIDENCE:\n{evidence}"}]}
    if not THINK:  # grammar-constrain when not reasoning; when reasoning, let it think then strip <think>
        body["response_format"] = {"type": "json_schema",
                                   "json_schema": {"name": "verdict", "strict": True, "schema": SCHEMA}}
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.loads(r.read())
    dt = time.time() - t0
    content = d["choices"][0]["message"]["content"]
    return extract_json(content), dt, d.get("usage", {})

def main():
    print(f">>> Verifier model: {MODEL} (family-different from the Claude generator) via {BASE}")
    rows, correct, lat = [], 0, []
    for c in CLAIMS:
        try:
            v, dt, usage = call(c["claim"], c["evidence"])
        except Exception as e:
            print(f"  #{c['id']:2} ERROR {type(e).__name__}: {str(e)[:120]}")
            rows.append({**c, "pred": "ERROR", "ok": False}); continue
        if "verdict" not in v:
            print(f"  #{c['id']:2} ERROR no 'verdict' key in {str(v)[:80]}"); rows.append({**c,"pred":"ERROR","ok":False}); continue
        ok = (v["verdict"] == c["gold"]); correct += ok; lat.append(dt)
        mark = "OK " if ok else "XX "
        print(f"  #{c['id']:2} {mark} gold={c['gold']:12} pred={v['verdict']:12} conf={v.get('confidence',0):.2f} {dt:5.2f}s  {v.get('rationale','')[:72]}")
        rows.append({**c, "pred": v["verdict"], "conf": v.get("confidence"), "ok": ok,
                     "rationale": v.get("rationale"), "secs": round(dt, 2)})
    n = len(CLAIMS)
    acc = 100 * correct / n
    avg = sum(lat) / len(lat) if lat else 0
    # per-label recall
    from collections import defaultdict
    by = defaultdict(lambda: [0, 0])
    for r in rows:
        by[r["gold"]][1] += 1
        if r.get("ok"): by[r["gold"]][0] += 1
    print(f"\n=== {MODEL}: {correct}/{n} correct = {acc:.1f}%  | avg {avg:.2f}s/verdict ===")
    for g in ["supported", "refuted", "insufficient"]:
        ok_, tot_ = by[g]; print(f"    {g:12}: {ok_}/{tot_}")
    out = os.path.join(HERE, f"results-{MODEL}.json")
    json.dump({"model": MODEL, "n": n, "correct": correct, "accuracy_pct": round(acc, 1),
               "avg_secs": round(avg, 2), "rows": rows}, open(out, "w"), indent=2)
    print("wrote", out)

if __name__ == "__main__":
    main()
