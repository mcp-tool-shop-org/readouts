#!/usr/bin/env python3
"""Goal 3 (part 2, done right): EXTERNAL-VERIFY recipe_kind with a FAMILY-DIFFERENT PANEL.

Three families (Mistral / IBM Granite / Google Gemma — the wave-9..14 verifier doctrine) each
audit whether a recipe's body supports its assigned recipe_kind, judging by END STATE. Then,
conservative majority (>=2 of 3):
  * majority == current kind  -> verified=1 (confirmed)
  * majority == a DIFFERENT kind -> AUTO-CORRECT to it (+ axis, + backend), verified=1, provenance noted
  * no majority -> verified=0, flagged for review (panel split)
A single seat can false-flag; the panel is the safety. Seat-OUTER loop = 3 model loads, not 480 swaps.
All local, zero Claude tokens. Generator = my regex/heuristics; verifier = different family AND mechanism.

Usage:  $env:PYTHONUTF8='1'; python recipes/_verify_panel.py [--limit N]
"""
import os, sys, re, json, sqlite3, urllib.request
from collections import Counter

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")
OLLAMA = "http://localhost:11434/api/generate"
SEATS = ["mistral-small:24b", "granite4.1:30b", "gemma4:31b"]
VALID = {"launchable-server", "batch-producer", "modifier", "router-fleet"}
AXIS = {"launchable-server": "tok_s", "batch-producer": "build_wall_clock", "modifier": "delta_pct", "router-fleet": "none"}

DEFS = (
    "Decide by the recipe's END STATE, NOT by whether it compiles/builds/installs anything "
    "(a build/install step is just SETUP, it does not decide the kind). "
    "launchable-server = ends with a long-lived server/engine running on a port (incl. building a "
    "llama.cpp/vLLM/exllama/etc. binary you then SERVE with — the binary IS the engine); "
    "batch-producer = the DELIVERABLE is a written DATA artifact consumed elsewhere (quantized model, "
    "LoRA adapter, .engine file, or a benchmark/measurement receipt) and nothing keeps running; "
    "modifier = only changes ANOTHER recipe's build/runtime (kernel/attention overlay/toolchain), "
    "produces nothing runnable or no artifact of its own; "
    "router-fleet = a front that routes to other engine recipes (proxy / model-swap)")
PROMPT = ("Four recipe kinds. " + DEFS + ".\n"
          "A setup recipe was auto-classified as '{kind}'. Decide the BEST of the four by END STATE.\n"
          'Respond ONLY JSON: {{"correct": true/false, "kind": "<best kind>", "note": "<=10 words"}}.\n\n'
          "Recipe: {name}\nBody:\n{body}")

def classify_backend(kind, t):
    if kind == "modifier": return None
    if any(k in t for k in ["wsl2", "wsl ", "docker", "vllm", "sglang", "lmdeploy", "aphrodite"]): return "wsl2-docker"
    if any(k in t for k in ["portable", "run_nvidia_gpu", "python_embeded", "embedded python"]): return "portable-bundle"
    if any(k in t for k in ["onnx", "tensorrt", ".engine", "trtexec"]): return "onnx-compile"
    if kind == "router-fleet" or "litellm" in t or " proxy" in t: return "python-proxy"
    if any(k in t for k in ["uv venv", "uv pip", "venv", "pip install", "conda "]): return "venv"
    if any(k in t for k in ["cmake", "-dggml", "from source", "msvc", "cargo", "prebuilt", ".whl", "wheel", "cu128", "cu130", "cuda 12.8"]): return "native-win-compile"
    return None

def ask(model, name, kind, body):
    payload = {"model": model, "prompt": PROMPT.format(kind=kind, name=name, body=(body or "")[:1800]),
               "stream": False, "think": False, "format": "json", "options": {"temperature": 0.1, "num_predict": 70}}
    req = urllib.request.Request(OLLAMA, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.loads(r.read())["response"]
    try:
        j = json.loads(out)
    except Exception:
        m = re.search(r"\{.*\}", out, re.S); j = json.loads(m.group(0)) if m else {}
    return bool(j.get("correct")), (j.get("kind") or "")

def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    con = sqlite3.connect(DB); cur = con.cursor()
    q = "select id, name, recipe_kind, backend_kind, body from recipes order by id"
    if limit: q += f" limit {limit}"
    recs = cur.execute(q).fetchall()
    votes = {rid: [] for rid, *_ in recs}    # rid -> [effective_kind per seat]
    for seat in SEATS:
        print(f"--- seat: {seat} ({len(recs)} recipes) ---")
        for i, (rid, name, kind, backend, body) in enumerate(recs, 1):
            try:
                correct, sug = ask(seat, name, kind, body)
            except Exception as e:
                print(f"  [{rid}] {seat} ERROR {e}"); continue
            eff = kind if correct else (sug if sug in VALID else None)
            votes[rid].append(eff)
            if i % 40 == 0: print(f"  {seat}: {i}/{len(recs)}")

    confirmed = corrected = flagged = 0
    corr_list = []
    for rid, name, kind, backend, body in recs:
        tally = Counter([v for v in votes[rid] if v])
        if not tally:
            flagged += 1; continue
        winner, wc = tally.most_common(1)[0]
        seats_str = "+".join(f"{v}" for v in votes[rid] if v)
        if wc >= 2 and winner == kind:
            cur.execute("update recipes set verified=1, verify_note=NULL where id=?", (rid,)); confirmed += 1
        elif wc >= 2 and winner != kind:
            t = (name + " " + (body or "")).lower()
            nb = None if winner == "modifier" else (backend or classify_backend(winner, t))
            note = f"panel-corrected {kind}->{winner} ({wc}/3)"
            cur.execute("update recipes set recipe_kind=?, measured_axis=?, backend_kind=?, verified=1, verify_note=? where id=?",
                        (winner, AXIS[winner], nb, note, rid))
            corrected += 1; corr_list.append((kind, winner, wc, name[:44]))
        else:
            cur.execute("update recipes set verified=0, verify_note=? where id=?",
                        (f"panel-split: {dict(tally)}", rid)); flagged += 1
        if (confirmed + corrected + flagged) % 40 == 0: con.commit()
    con.commit()
    print(f"\nPANEL RESULT: {confirmed} confirmed, {corrected} auto-corrected, {flagged} flagged (split)")
    print("\nauto-corrections (>=2/3 agree on a different kind):")
    for old, new, wc, name in corr_list:
        print(f"  {old:16s} -> {new:18s} ({wc}/3)  {name}")
    print("\nrecipe_kind distribution AFTER panel:")
    for k, n in cur.execute("select recipe_kind,count(*) from recipes group by recipe_kind order by 2 desc"):
        print(f"  {k:18s} {n}")
    print("verified=1:", cur.execute("select count(*) from recipes where verified=1").fetchone()[0], "/ 160")
    con.close()

if __name__ == "__main__":
    main()
