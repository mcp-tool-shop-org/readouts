#!/usr/bin/env python3
"""Wave-5: does a multi-seat panel (workflow-standards 'multi-lens >= 3') beat any single verifier,
esp. on the safety metric (false-confirm = stamping a non-supported claim 'supported')?"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = ["qwen3-4b", "qwen3-14b", "qwen3-30b-a3b", "mistral-nemo-12b"]
R = {m: {row["id"]: row for row in json.load(open(os.path.join(HERE, f"results-{m}.json")))["rows"]} for m in MODELS}
GOLD = {row["id"]: row["gold"] for row in json.load(open(os.path.join(HERE, "claims.json")))}
IDS = sorted(GOLD)

def panel(seats, ids):
    """Conservative panel: verdict='supported' ONLY if a strict majority of seats say supported;
    otherwise take the majority among the rest (tie -> 'insufficient'). Safety-first."""
    correct = fc = 0
    for i in ids:
        votes = [R[m][i]["pred"] for m in seats]
        sup = votes.count("supported")
        if sup > len(seats) / 2:
            v = "supported"
        else:
            ref, ins = votes.count("refuted"), votes.count("insufficient")
            v = "refuted" if ref > ins else "insufficient"
        if v == GOLD[i]: correct += 1
        if v == "supported" and GOLD[i] != "supported": fc += 1
    return correct, fc

print("=== single models ===")
for m in MODELS:
    rows = R[m]; corr = sum(1 for i in IDS if rows[i].get("ok"))
    fc = sum(1 for i in IDS if rows[i]["pred"] == "supported" and GOLD[i] != "supported")
    print(f"  {m:18} {corr}/{len(IDS)} = {100*corr/len(IDS):.1f}%   false-confirms={fc}")

print("=== panels (conservative majority) ===")
for name, seats in [
    ("3-seat 2fam (4b+14b+nemo)", ["qwen3-4b", "qwen3-14b", "mistral-nemo-12b"]),
    ("3-seat Qwen (4b+14b+30b)",  ["qwen3-4b", "qwen3-14b", "qwen3-30b-a3b"]),
    ("4-seat all",                MODELS),
]:
    corr, fc = panel(seats, IDS)
    print(f"  {name:28} {corr}/{len(IDS)} = {100*corr/len(IDS):.1f}%   false-confirms={fc}")
# show the case where the panel rescues a single-model false-confirm
print("\n=== case #6 (gold=refuted) per model — the false-confirm Nemo made ===")
for m in MODELS: print(f"  {m:18} -> {R[m][6]['pred']}")
