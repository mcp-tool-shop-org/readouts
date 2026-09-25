#!/usr/bin/env python3
"""Wave-9: add a THIRD verifier family (IBM Granite 3.3 8B Instruct, Apache-2.0) to the offload
entailment panel and MEASURE whether 3 families beat 2 on the REAL arXiv citation set.

The decisive metric is FALSE-CONFIRM rate (a refuted/insufficient claim stamped 'supported'), NOT
raw accuracy: a citation GATE must never wave through a fabricated/inverted claim; over-escalation
(a faithful claim sent for human review) is the safe failure. So we report accuracy AND false-confirms
per composition, plus the head-to-head: does adding Granite catch a false-confirm the 2-family panel
slips, and at what accuracy cost.

Panel compositions (offload's own conservative-majority rule: 'supported' only on a STRICT majority):
  P2_baseline          qwen3-4b + qwen3-14b + mistral-nemo-12b       (wave-6: Qwen + Mistral, 2 families)
  P3_4seat             + granite-3.3-8b                               (3 families, 4 seats)
  P3_3seat_perfamily   qwen3-14b + mistral-nemo-12b + granite-3.3-8b  (3 families, strongest seat each)
  P3_3seat_cheap       qwen3-4b + mistral-nemo-12b + granite-3.3-8b   (3 families, cheapest Qwen)

Reuses offload.py's OWN verifier (same prompt + schema the wired roleos seat calls), so the receipt
reflects the shipped tool. Runs model-by-model (4 llama-swap loads total). stdlib + offload only.
llama-swap must be up (:9090) and serving granite-3.3-8b (added to config.yaml in wave-9).

Dataset: citations-real.json (the wave-6 16-case set) + citations-real-ext.json if present (wave-9
extra hard traps against the SAME sha-pinned abstracts). Metrics are reported on the FULL set and on
the original-16 subset (so the wave-6 baseline stays directly comparable).

  python citation_panel_eval_3family.py
"""
import json, os, hashlib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-06-03"
OFFLOAD = os.environ.get("OFFLOAD_SCRIPT", "E:/AI-Models/studio-local/offload.py")
SEATS = ["qwen3-4b", "qwen3-14b", "mistral-nemo-12b", "granite-3.3-8b"]
PANELS = {
    "P2_baseline":        ["qwen3-4b", "qwen3-14b", "mistral-nemo-12b"],
    "P3_4seat":           ["qwen3-4b", "qwen3-14b", "mistral-nemo-12b", "granite-3.3-8b"],
    "P3_3seat_perfamily": ["qwen3-14b", "mistral-nemo-12b", "granite-3.3-8b"],
    "P3_3seat_cheap":     ["qwen3-4b", "mistral-nemo-12b", "granite-3.3-8b"],
}

_spec = importlib.util.spec_from_file_location("offload", OFFLOAD)
offload = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(offload)

CASES = json.load(open(os.path.join(HERE, "citations-real.json"), encoding="utf-8"))
BASE_IDS = {c["id"] for c in CASES}
ext_path = os.path.join(HERE, "citations-real-ext.json")
if os.path.exists(ext_path):
    CASES = CASES + json.load(open(ext_path, encoding="utf-8"))
SRC = json.load(open(os.path.join(HERE, "abstracts-cache.json"), encoding="utf-8"))
GOLD = {c["id"]: c["gold"] for c in CASES}
IDS = [c["id"] for c in CASES]


def evidence_for(case):
    s = SRC[case["arxiv_id"]]
    return f"Title: {s['title']}\n\nAbstract: {s['abstract']}"


def panel_verdict(votes):
    """offload's conservative majority: 'supported' only on a strict majority."""
    sup = votes.count("supported")
    if sup > len(votes) / 2:
        return "supported"
    ref, ins = votes.count("refuted"), votes.count("insufficient")
    return "refuted" if ref > ins else "insufficient"


def metrics(pred_by_id, ids):
    corr = sum(1 for i in ids if pred_by_id[i] == GOLD[i])
    fc = sum(1 for i in ids if pred_by_id[i] == "supported" and GOLD[i] != "supported")
    return {"n": len(ids), "correct": corr, "accuracy": round(100 * corr / len(ids), 1),
            "false_confirms": fc}


def run():
    preds = {m: {} for m in SEATS}
    for m in SEATS:
        print(f"\n=== seat: {m} ===")
        for c in CASES:
            r = offload._verify_one(m, c["claim"], evidence_for(c))
            preds[m][c["id"]] = r["verdict"]
            flag = "" if r["verdict"] == GOLD[c["id"]] else "  <-- miss"
            fc = "  *** FALSE-CONFIRM ***" if (r["verdict"] == "supported" and GOLD[c["id"]] != "supported") else ""
            print(f"  [{c['id']:>2}] gold={GOLD[c['id']]:<12} pred={r['verdict']:<12}{flag}{fc}")
        rows = [{"id": i, "gold": GOLD[i], "pred": preds[m][i], "ok": preds[m][i] == GOLD[i]} for i in IDS]
        json.dump({"model": m, "rows": rows},
                  open(os.path.join(HERE, f"results-real-{m}.json"), "w", encoding="utf-8"), indent=2)

    full_ids = IDS
    base_ids = [i for i in IDS if i in BASE_IDS]

    # Per single seat (full set + original-16 subset).
    per_model = {}
    print("\n=== single seats (full set) ===")
    for m in SEATS:
        per_model[m] = {"full": metrics(preds[m], full_ids), "base16": metrics(preds[m], base_ids)}
        f = per_model[m]["full"]
        print(f"  {m:18} {f['correct']}/{f['n']} = {f['accuracy']}%   false-confirms={f['false_confirms']}")

    # Per panel composition.
    panel_pred = {}
    panel_metrics = {}
    print("\n=== panel compositions (full set) ===")
    for name, seats in PANELS.items():
        pp = {i: panel_verdict([preds[m][i] for m in seats]) for i in IDS}
        panel_pred[name] = pp
        panel_metrics[name] = {"seats": seats, "n_families": len({s.split('-')[0].split('3')[0] or s for s in seats}),
                               "full": metrics(pp, full_ids), "base16": metrics(pp, base_ids)}
        f = panel_metrics[name]["full"]
        print(f"  {name:20} {','.join(seats):55} {f['correct']}/{f['n']} = {f['accuracy']}%   fc={f['false_confirms']}")

    # Head-to-head: cases the 2-family baseline FALSE-CONFIRMS that a 3-family panel CATCHES.
    base = panel_pred["P2_baseline"]
    print("\n=== 3-family CATCHES that the 2-family baseline SLIPS (false-confirm rescued) ===")
    catches = {}
    for name in PANELS:
        if name == "P2_baseline":
            continue
        rescued = []
        for i in IDS:
            if GOLD[i] != "supported" and base[i] == "supported" and panel_pred[name][i] != "supported":
                rescued.append({"id": i, "arxiv_id": next(c["arxiv_id"] for c in CASES if c["id"] == i),
                                "gold": GOLD[i], "baseline": base[i], "panel_verdict": panel_pred[name][i],
                                "seat_votes": {m: preds[m][i] for m in PANELS[name]}})
        catches[name] = rescued
        if rescued:
            for r in rescued:
                print(f"  {name}: case #{r['id']} ({r['arxiv_id']}) gold={r['gold']} | baseline=SUPPORTED(slip) -> panel={r['panel_verdict']}")
        else:
            print(f"  {name}: (no case where the 2-family baseline false-confirmed but this panel caught it)")

    # Per-seat slip catches (any single seat false-confirmed; panel held) — the wave-6-style rescue.
    print("\n=== single-seat slips the panel HELD (per panel) ===")
    seat_slip = {}
    for name, seats in PANELS.items():
        rescues = []
        for i in IDS:
            if GOLD[i] == "supported":
                continue
            slips = [m for m in seats if preds[m][i] == "supported"]
            if slips and panel_pred[name][i] != "supported":
                rescues.append({"id": i, "gold": GOLD[i], "panel_verdict": panel_pred[name][i], "slipping_seats": slips})
        seat_slip[name] = rescues
        print(f"  {name:20} held {len(rescues)} single-seat slip(s): " +
              ", ".join(f"#{r['id']}({'+'.join(r['slipping_seats'])})" for r in rescues) if rescues else f"  {name:20} (none)")

    receipt = {
        "schema": "tensor-engine-knowledge/citation-panel-3family-receipt/v1",
        "kind": "verifier-panel-eval-3family",
        "wave": 9,
        "date": DATE,
        "dataset": "citations-real.json" + ("+citations-real-ext.json" if os.path.exists(ext_path) else ""),
        "dataset_sha256": hashlib.sha256(json.dumps(CASES, sort_keys=True).encode()).hexdigest(),
        "n_cases": len(IDS),
        "n_base16": len(base_ids),
        "n_not_supported": sum(1 for i in IDS if GOLD[i] != "supported"),
        # PIN_PER_STEP: the exact seats (incl. the new family), the offload prompt, llama-swap base.
        "seats": SEATS,
        "third_family": {"name": "granite-3.3-8b", "model": "IBM Granite 3.3 8B Instruct",
                         "license": "Apache-2.0", "gguf": "granite-3.3-8b-instruct-Q4_K_M.gguf",
                         "hf_repo": "ibm-granite/granite-3.3-8b-instruct-GGUF"},
        "offload_script": OFFLOAD,
        "llamaswap_base": offload.BASE,
        "verify_prompt_sha256": hashlib.sha256(offload._V_SYS.encode()).hexdigest(),
        "source_pins": [{"arxiv_id": k, "title": v["title"], "abstract_sha256": v["sha256"], "source": v["source"]}
                        for k, v in SRC.items() if any(c["arxiv_id"] == k for c in CASES)],
        "per_model": per_model,
        "panels": {name: {**panel_metrics[name],
                          "rows": [{"id": i, "gold": GOLD[i], "panel_verdict": panel_pred[name][i],
                                    "seat_votes": {m: preds[m][i] for m in panel_metrics[name]["seats"]}} for i in IDS]}
                   for name in PANELS},
        "third_family_catches_vs_baseline": catches,
        "single_seat_slips_held": seat_slip,
        "property_holds_all_panels": all(panel_metrics[n]["full"]["false_confirms"] == 0 for n in PANELS),
    }
    out = os.path.join(HERE, "citation-panel-3family-receipt.json")
    json.dump(receipt, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("\n=== verdict ===")
    for name in PANELS:
        f = panel_metrics[name]["full"]
        print(f"  {name:20} acc={f['accuracy']:>5}%  false-confirms={f['false_confirms']}")
    print(f"\n0-false-confirm holds across ALL panels: {receipt['property_holds_all_panels']}")
    print(f"receipt -> {out}")


if __name__ == "__main__":
    run()
