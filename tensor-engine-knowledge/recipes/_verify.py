#!/usr/bin/env python3
"""Goal 3 (part 2): EXTERNAL-VERIFY the deterministic recipe_kind classification.

A different-family local model (mistral-small:24b) audits the generator (my regex/heuristics):
does each recipe's body support the assigned recipe_kind? Sets recipes.verified=1 when the
auditor confirms; on disagreement, leaves verified=0 and records the auditor's suggested kind in
verify_note (a review flag — does NOT auto-reclassify). This is the EXTERNAL_VERIFIER standard:
verifier of a different family than the qwen summarizer and a different mechanism than the regex.

Note: this verifies the EXTRACTION is grounded in the prose. A recipe's real correctness proof is
EXECUTION (engine-room baseline gate); resolvability of its pins is a separate deterministic floor.

Usage:  $env:PYTHONUTF8='1'; python recipes/_verify.py [--limit N]
"""
import os, sys, re, json, sqlite3, urllib.request

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "mistral-small:24b"   # different family than the qwen3.6 summarizer + the Claude generator

DEFS = (
    "Decide by the recipe's END STATE, NOT by whether it compiles/builds/installs anything "
    "(a build or install step is just SETUP, it does not decide the kind). "
    "launchable-server = ends with a long-lived server/engine running on a port (incl. building a "
    "llama.cpp/vLLM/etc. binary you then SERVE with — the binary IS the engine); "
    "batch-producer = the DELIVERABLE is a written DATA artifact consumed elsewhere (quantized model, "
    "LoRA adapter, .engine file, or a benchmark/measurement receipt) and nothing keeps running; "
    "modifier = only changes ANOTHER recipe's build/runtime (a kernel/attention overlay/toolchain), "
    "produces nothing runnable or no artifact of its own; "
    "router-fleet = a front that routes to other engine recipes (proxy / model-swap)")

PROMPT = (
    "Four recipe kinds. " + DEFS + ".\n"
    "A setup recipe was auto-classified as '{kind}'. Read the body and decide the BEST of the four kinds by END STATE.\n"
    'Respond ONLY JSON: {{"correct": true/false, "kind": "<best kind>", "note": "<=12 words why>"}}.\n\n'
    "Recipe: {name}\nBody:\n{body}")

def audit(name, kind, body):
    payload = {
        "model": MODEL,
        "prompt": PROMPT.format(kind=kind, name=name, body=(body or "")[:2000]),
        "stream": False, "think": False, "format": "json",
        "options": {"temperature": 0.1, "num_predict": 80},
    }
    req = urllib.request.Request(OLLAMA, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.loads(r.read())["response"]
    try:
        j = json.loads(out)
    except Exception:
        m = re.search(r"\{.*\}", out, re.S)
        j = json.loads(m.group(0)) if m else {"correct": None, "kind": None, "note": "unparseable"}
    return bool(j.get("correct")), (j.get("kind") or ""), (j.get("note") or "")[:80]

VALID = {"launchable-server", "batch-producer", "modifier", "router-fleet"}

def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    con = sqlite3.connect(DB); cur = con.cursor()
    q = "select id, name, recipe_kind, body, verify_note from recipes order by id"
    if limit: q += f" limit {limit}"
    rows = cur.execute(q).fetchall()
    print(f"external-verifying {len(rows)} kinds on {MODEL} ...")
    ok = flag = done = 0
    flagged = []
    for rid, name, kind, body, note in rows:
        try:
            correct, sug, why = audit(name, kind, body)
        except Exception as e:
            print(f"  [{rid}] ERROR {e}"); continue
        done += 1
        if correct:
            cur.execute("update recipes set verified=1 where id=?", (rid,)); ok += 1
        else:
            sug = sug if sug in VALID else "?"
            nn = (note or "").split(" | verifier:")[0]
            nn = f"{nn} | verifier: suggests {sug} — {why}".strip(" |")
            cur.execute("update recipes set verified=0, verify_note=? where id=?", (nn, rid)); flag += 1
            flagged.append((kind, sug, name[:42], why))
        if done % 20 == 0:
            con.commit(); print(f"  [{done}/{len(rows)}] verified={ok} flagged={flag}")
    con.commit()
    print(f"\ndone: {ok} verified, {flag} flagged for review")
    if flagged:
        print("\nflagged (auditor disagrees with assigned kind):")
        for kind, sug, name, why in flagged[:30]:
            print(f"  {kind:16s} -> {sug:16s} {name:42s} {why}")
    con.close()

if __name__ == "__main__":
    main()
