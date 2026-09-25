#!/usr/bin/env python3
"""Wave-3 family-different verification pass (Step 4, reasoning-stripped).

Two decorrelated NON-Claude families (mistral-small:24b / Mistral, granite4.1:30b / IBM
Granite) judge each finding's CLAIM against its cited source — WITHOUT the research agent's
reasoning (no `detail`, no `design_implication`). The retrieval oracle (run in-workflow) is
the existence + groundedness authority; these families are decorrelating corroboration that
catches overstatement / internal inconsistency.

Lesson folded in from the wave-2 founding receipt: sources here are 2024-2026 NVIDIA docs /
GitHub issues that postdate model training — models MUST mark those `cant_confirm`, never
`refuted` purely for non-recall (the oracle already confirmed existence).

Reads workflow-output.json, writes family-verdicts.json. Local + free + read-only.
"""
import json
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_IN = os.path.join(HERE, "workflow-output.json")
OUT = os.path.join(HERE, "family-verdicts.json")

MODELS = ["mistral-small:24b", "granite4.1:30b"]

SYSTEM = (
    "You are an INDEPENDENT verifier from a different model family than the author. You are given "
    "research claims about NVIDIA's WSL2 / Docker pinned-host-memory (cudaHostAlloc / pin_memory) "
    "limits, each with its cited source. You do NOT see the author's reasoning. For each claim, judge "
    "ONLY whether the claim is plausibly supported by a source of that type and is internally "
    "consistent / not overstated.\n"
    "Verdicts: 'confirmed' = plausible and consistent with the cited source; 'refuted' = contradicts "
    "well-established facts or the cited source category cannot support it; 'cant_confirm' = you cannot "
    "assess it.\n"
    "CRITICAL: many sources are 2024-2026 NVIDIA docs / GitHub issues / forum posts that may POSTDATE "
    "your training. If you simply don't recall a source, output 'cant_confirm' — do NOT output 'refuted' "
    "merely because it is recent or unfamiliar. Reserve 'refuted' for a claim that contradicts a fact "
    "you are confident about.\n"
    'Return ONLY JSON: {"verdicts":[{"id":"<id>","verdict":"confirmed|refuted|cant_confirm","why":"<<=20 words>"}]}'
)


def build_user(findings):
    lines = ["Judge each claim below. Return one verdict per id.\n"]
    for f in findings:
        srcs = "; ".join(
            f"{s.get('title','?')} ({s.get('authors','?')} {s.get('year','?')}) — source states: {s.get('finding','')}"
            for s in (f.get("sources") or [])
        )
        lines.append(f"--- id: {f['id']}\nCLAIM: {f['claim']}\nCITED SOURCE(S): {srcs}\n")
    return "\n".join(lines)


def chat(model, system, user, timeout=420):
    payload = {
        "model": model, "stream": False, "format": "json",
        "options": {"temperature": 0, "num_ctx": 16384},
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
    }
    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.loads(r.read().decode("utf-8"))
    return resp["message"]["content"]


def main():
    d = json.load(open(OUT_IN, encoding="utf-8"))
    findings = d["findings"]
    user = build_user(findings)
    results = {}
    for m in MODELS:
        try:
            raw = chat(m, SYSTEM, user)
            parsed = json.loads(raw)
            verdicts = {v["id"]: v for v in parsed.get("verdicts", []) if v.get("id")}
            results[m] = {"ok": True, "verdicts": verdicts, "n": len(verdicts)}
            print(f"{m}: {len(verdicts)} verdicts")
        except Exception as e:
            results[m] = {"ok": False, "error": str(e)}
            print(f"{m}: ERROR {e}")

    json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # compact cross-family summary
    print("\nid                                  mistral        granite")
    for f in findings:
        a = results.get("mistral-small:24b", {}).get("verdicts", {}).get(f["id"], {}).get("verdict", "-")
        b = results.get("granite4.1:30b", {}).get("verdicts", {}).get(f["id"], {}).get("verdict", "-")
        flag = "" if (a in ("confirmed", "cant_confirm") and b in ("confirmed", "cant_confirm")) else "  <-- REFUTED"
        print(f"{f['id']:34s}  {a:13s}  {b:13s}{flag}")
    print("\nwrote", OUT)


if __name__ == "__main__":
    main()
