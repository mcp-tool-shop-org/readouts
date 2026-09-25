#!/usr/bin/env python3
"""Wave-9: the 24-case set surfaced a CORRELATED failure the conservative-majority panel cannot
catch — #21/#22/#23 (a direction-inversion + two plausible-but-unstated additions) fool a MAJORITY
of seats across ALL families, so every panel composition false-confirms them (3 fc). Family
diversity kills UNCORRELATED slips, not correlated ones.

This probe tests whether PROMPT HARDENING (a different lever than more seats) recovers those
correlated false-confirms, by re-running the per-family panel (qwen3-14b + mistral-nemo-12b +
granite-3.3-8b) under two system prompts on the full 24-case set:
  default   = offload._V_SYS_DEFAULT (the shipped wave-5/6 prompt)
  hardened  = verify_sys_hardened.txt (explicit direction-check + added-specific-check rules)

Measures per-seat + panel false-confirms and accuracy under each prompt, and which cases flip. The
shipped offload default is NOT changed (the hardened prompt is opt-in via OFFLOAD_VERIFY_SYS_FILE);
this records whether it is worth adopting. llama-swap must be up (:9090).

  python prompt_hardening_probe.py
"""
import json, os, hashlib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-06-03"
OFFLOAD = os.environ.get("OFFLOAD_SCRIPT", "E:/AI-Models/studio-local/offload.py")
SEATS = ["qwen3-14b", "mistral-nemo-12b", "granite-3.3-8b"]   # the wave-9 per-family panel

_spec = importlib.util.spec_from_file_location("offload", OFFLOAD)
offload = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(offload)

CASES = json.load(open(os.path.join(HERE, "citations-real.json"), encoding="utf-8"))
ext = os.path.join(HERE, "citations-real-ext.json")
if os.path.exists(ext):
    CASES += json.load(open(ext, encoding="utf-8"))
SRC = json.load(open(os.path.join(HERE, "abstracts-cache.json"), encoding="utf-8"))
GOLD = {c["id"]: c["gold"] for c in CASES}
IDS = [c["id"] for c in CASES]

DEFAULT_SYS = offload._V_SYS_DEFAULT
HARDENED_SYS = open(os.path.join(HERE, "verify_sys_hardened.txt"), encoding="utf-8").read().strip()
PROMPTS = {"default": DEFAULT_SYS, "hardened": HARDENED_SYS}


def evidence_for(c):
    s = SRC[c["arxiv_id"]]
    return f"Title: {s['title']}\n\nAbstract: {s['abstract']}"


def verify(model, claim, evidence, sysprompt):
    d = offload._post("/v1/chat/completions", {
        "model": model, "temperature": 0, "max_tokens": 700,
        "messages": [{"role": "system", "content": sysprompt},
                     {"role": "user", "content": f"CLAIM:\n{claim}\n\nEVIDENCE:\n{evidence}"}],
        "response_format": {"type": "json_schema",
                            "json_schema": {"name": "verdict", "strict": True, "schema": offload._V_SCHEMA}}})
    v = offload._extract_json(d["choices"][0]["message"]["content"]) or {}
    return v.get("verdict", "error")


def panel_verdict(votes):
    sup = votes.count("supported")
    if sup > len(votes) / 2:
        return "supported"
    return "refuted" if votes.count("refuted") > votes.count("insufficient") else "insufficient"


def fc_cases(pred_by_id):
    return [i for i in IDS if pred_by_id[i] == "supported" and GOLD[i] != "supported"]


def run():
    # preds[promptname][model][id]
    preds = {p: {m: {} for m in SEATS} for p in PROMPTS}
    for m in SEATS:                       # load each model once; run both prompts while warm
        print(f"\n=== seat: {m} ===")
        for pname, sysp in PROMPTS.items():
            for c in CASES:
                preds[pname][m][c["id"]] = verify(m, c["claim"], evidence_for(c), sysp)
            fc = fc_cases(preds[pname][m])
            corr = sum(1 for i in IDS if preds[pname][m][i] == GOLD[i])
            print(f"  [{pname:8}] acc={100*corr/len(IDS):4.1f}%  fc={len(fc)} {fc}")

    out = {"schema": "tensor-engine-knowledge/prompt-hardening-receipt/v1", "wave": 9, "date": DATE,
           "n_cases": len(IDS), "seats": SEATS, "panel_rule": "conservative-majority",
           "prompts": {p: {"sha256": hashlib.sha256(PROMPTS[p].encode()).hexdigest()} for p in PROMPTS},
           "per_seat": {}, "panel": {}}
    print("\n=== per-seat false-confirms (full 24) ===")
    for pname in PROMPTS:
        out["per_seat"][pname] = {}
        for m in SEATS:
            fc = fc_cases(preds[pname][m])
            corr = sum(1 for i in IDS if preds[pname][m][i] == GOLD[i])
            out["per_seat"][pname][m] = {"accuracy": round(100 * corr / len(IDS), 1), "false_confirms": fc}
            print(f"  {pname:8} {m:18} acc={100*corr/len(IDS):4.1f}%  fc={len(fc)} {fc}")

    print("\n=== PANEL (per-family) under each prompt ===")
    for pname in PROMPTS:
        panel = {i: panel_verdict([preds[pname][m][i] for m in SEATS]) for i in IDS}
        fc = fc_cases(panel)
        corr = sum(1 for i in IDS if panel[i] == GOLD[i])
        out["panel"][pname] = {"accuracy": round(100 * corr / len(IDS), 1), "false_confirms": fc,
                               "rows": [{"id": i, "gold": GOLD[i], "panel": panel[i],
                                         "votes": {m: preds[pname][m][i] for m in SEATS}} for i in IDS]}
        print(f"  {pname:8} panel  acc={100*corr/len(IDS):4.1f}%  false-confirms={len(fc)} {fc}")

    df, hd = out["panel"]["default"]["false_confirms"], out["panel"]["hardened"]["false_confirms"]
    out["recovered"] = sorted(set(df) - set(hd))
    out["newly_broken"] = sorted(set(hd) - set(df))
    print(f"\n  recovered by hardening (was fc, now caught): {out['recovered']}")
    print(f"  newly broken by hardening (regressions):      {out['newly_broken']}")
    path = os.path.join(HERE, "prompt-hardening-receipt.json")
    json.dump(out, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\nreceipt -> {path}")


if __name__ == "__main__":
    run()
