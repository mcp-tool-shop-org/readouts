#!/usr/bin/env python3
"""Wave-6: prove the offload entailment PANEL holds the 0-false-confirm property on a REAL arXiv
citation set (the papers role-os's verify-citations gate actually checks), and capture the
planted false-confirm a single seat slips that the panel catches.

Reuses offload.py's OWN verifier (same prompt + schema the wired roleos seat calls), so the receipt
reflects the shipped tool, not a re-implementation. Runs model-by-model (3 llama-swap loads total,
not 3-per-case). stdlib + offload only. llama-swap must be up (:9090).

  python citation_panel_eval.py            # run all seats, write receipt
"""
import json, os, hashlib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-06-03"
OFFLOAD = os.environ.get("OFFLOAD_SCRIPT", "E:/AI-Models/studio-local/offload.py")
SEATS = ["qwen3-4b", "qwen3-14b", "mistral-nemo-12b"]  # offload.PANEL_SEATS — >=2 families

# import offload.py as a module (it's a single-file stdlib CLI)
_spec = importlib.util.spec_from_file_location("offload", OFFLOAD)
offload = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(offload)

CASES = json.load(open(os.path.join(HERE, "citations-real.json"), encoding="utf-8"))
SRC = json.load(open(os.path.join(HERE, "abstracts-cache.json"), encoding="utf-8"))
GOLD = {c["id"]: c["gold"] for c in CASES}
IDS = [c["id"] for c in CASES]


def evidence_for(case):
    s = SRC[case["arxiv_id"]]
    return f"Title: {s['title']}\n\nAbstract: {s['abstract']}"


def panel_verdict(votes):
    """offload's conservative majority: 'supported' only if a strict majority say so."""
    sup = votes.count("supported")
    if sup > len(votes) / 2:
        return "supported"
    ref, ins = votes.count("refuted"), votes.count("insufficient")
    return "refuted" if ref > ins else "insufficient"


def run():
    # Per-seat predictions (model-by-model keeps each model warm — 3 swaps total).
    preds = {m: {} for m in SEATS}
    for m in SEATS:
        print(f"\n=== seat: {m} ===")
        for c in CASES:
            r = offload._verify_one(m, c["claim"], evidence_for(c))
            preds[m][c["id"]] = r["verdict"]
            flag = "" if r["verdict"] == GOLD[c["id"]] else "  <-- miss"
            fc = "  *** FALSE-CONFIRM ***" if (r["verdict"] == "supported" and GOLD[c["id"]] != "supported") else ""
            print(f"  [{c['id']:>2}] gold={GOLD[c['id']]:<12} pred={r['verdict']:<12}{flag}{fc}")
        # per-model results file (parity with wave-5 #156 results-<model>.json)
        rows = [{"id": i, "gold": GOLD[i], "pred": preds[m][i], "ok": preds[m][i] == GOLD[i]} for i in IDS]
        json.dump({"model": m, "rows": rows},
                  open(os.path.join(HERE, f"results-real-{m}.json"), "w", encoding="utf-8"), indent=2)

    # Metrics
    def acc_fc(pred_by_id):
        corr = sum(1 for i in IDS if pred_by_id[i] == GOLD[i])
        fc = sum(1 for i in IDS if pred_by_id[i] == "supported" and GOLD[i] != "supported")
        return corr, fc

    per_model = {}
    print("\n=== single seats ===")
    for m in SEATS:
        corr, fc = acc_fc(preds[m])
        per_model[m] = {"accuracy": round(100 * corr / len(IDS), 1), "false_confirms": fc}
        print(f"  {m:18} {corr}/{len(IDS)} = {100*corr/len(IDS):.1f}%   false-confirms={fc}")

    panel = {i: panel_verdict([preds[m][i] for m in SEATS]) for i in IDS}
    pcorr, pfc = acc_fc(panel)
    print("\n=== 3-seat conservative-majority panel (Qwen 4b+14b + Mistral-Nemo) ===")
    print(f"  panel               {pcorr}/{len(IDS)} = {100*pcorr/len(IDS):.1f}%   false-confirms={pfc}")

    # Rescues: not-supported gold where >=1 seat false-confirmed but the panel did NOT.
    rescues = []
    for i in IDS:
        if GOLD[i] == "supported":
            continue
        slips = [m for m in SEATS if preds[m][i] == "supported"]
        if slips and panel[i] != "supported":
            rescues.append({"id": i, "arxiv_id": next(c["arxiv_id"] for c in CASES if c["id"] == i),
                            "gold": GOLD[i], "panel_verdict": panel[i], "slipping_seats": slips})
    print("\n=== planted false-confirms the PANEL caught (single seat slipped, panel held) ===")
    if rescues:
        for r in rescues:
            print(f"  case #{r['id']} ({r['arxiv_id']}, gold={r['gold']}): seat(s) {r['slipping_seats']} said 'supported'; panel said '{r['panel_verdict']}'")
    else:
        print("  (no single-seat slip this run — all seats already held; panel still 0 false-confirms)")

    receipt = {
        "schema": "tensor-engine-knowledge/citation-panel-receipt/v1",
        "kind": "verifier-panel-eval",
        "date": DATE,
        "dataset": "citations-real.json",
        "dataset_sha256": hashlib.sha256(json.dumps(CASES, sort_keys=True).encode()).hexdigest(),
        "n_cases": len(IDS),
        "n_not_supported": sum(1 for i in IDS if GOLD[i] != "supported"),
        # PIN_PER_STEP: the exact seats, the offload prompt, llama-swap base.
        "seats": SEATS,
        "offload_script": OFFLOAD,
        "llamaswap_base": offload.BASE,
        "verify_prompt_sha256": hashlib.sha256(offload._V_SYS.encode()).hexdigest(),
        # Source pins (replay/drift): the abstract each claim was judged against.
        "source_pins": [{"arxiv_id": k, "title": v["title"], "abstract_sha256": v["sha256"], "source": v["source"]}
                        for k, v in SRC.items()],
        "per_model": per_model,
        "panel": {"seats": SEATS, "accuracy": round(100 * pcorr / len(IDS), 1), "false_confirms": pfc,
                  "rows": [{"id": i, "gold": GOLD[i], "panel_verdict": panel[i],
                            "seat_votes": {m: preds[m][i] for m in SEATS}} for i in IDS]},
        "rescued_false_confirms": rescues,
        "property_holds": pfc == 0,
    }
    out = os.path.join(HERE, "citation-panel-receipt.json")
    json.dump(receipt, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\n0-false-confirm property holds: {pfc == 0}")
    print(f"receipt -> {out}")


if __name__ == "__main__":
    run()
