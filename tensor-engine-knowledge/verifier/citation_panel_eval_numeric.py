#!/usr/bin/env python3
"""Wave-14: measure the DETERMINISTIC numeric/unit floor (numeric_floor.py) — does the third, non-learned
mechanism catch the wave-13 correlated false-confirms (#48 comparison, #55 unit) that fooled BOTH learned
verifiers, WITHOUT false-refuting any of the 56 labeled cases?

Runs numeric_check on every case across all four sets (AI/ML 1-39 + physics 40-56), checks precision
(every 'refuted' must be gold=refuted), and measures the COMBINED gate on the physics set:
    combined = numeric_floor=='refuted' ? 'refuted' : <learned verdict>
reusing the wave-13 multidomain receipt's per-case LLM panel / NLI / consensus verdicts. stdlib only.

  python citation_panel_eval_numeric.py
"""
import json, os, hashlib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-06-03"
spec = importlib.util.spec_from_file_location("numeric_floor", os.path.join(HERE, "numeric_floor.py"))
nf = importlib.util.module_from_spec(spec); spec.loader.exec_module(nf)


def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


C = load("citations-real.json") + load("citations-real-ext.json") + load("citations-hard.json")
MULTI = load("citations-multidomain.json")
ALL = C + MULTI
SRC = json.load(open(os.path.join(HERE, "abstracts-cache.json"), encoding="utf-8"))
SRCM = json.load(open(os.path.join(HERE, "abstracts-cache-multidomain.json"), encoding="utf-8"))
GOLD = {c["id"]: c["gold"] for c in ALL}
MIDS = [c["id"] for c in MULTI]


def evidence_for(case):
    src = SRCM if case["id"] >= 40 else SRC
    s = src[case["arxiv_id"]]
    return f"{s['title']}. {s['abstract']}"


def run():
    refuted, rows = [], []
    for c in ALL:
        r = nf.numeric_check(c["claim"], evidence_for(c))
        rows.append({"id": c["id"], "gold": GOLD[c["id"]], "verdict": r["verdict"],
                     "rule": r["rule"], "detail": r["detail"]})
        if r["verdict"] == "refuted":
            refuted.append(c["id"])
    false_refutes = [i for i in refuted if GOLD[i] != "refuted"]
    catches = {"#48_comparison": 48 in refuted, "#55_unit": 55 in refuted}

    print("=== deterministic numeric/unit floor — cases it REFUTED (all others: abstain) ===")
    for row in rows:
        if row["verdict"] == "refuted":
            ok = "ok" if row["gold"] == "refuted" else "*** FALSE-REFUTE ***"
            print(f"  #{row['id']:>2} gold={row['gold']:<10} [{row['rule']}] {ok}\n       {row['detail']}")
    print(f"\n  refuted {len(refuted)} of {len(ALL)} cases: {refuted}")
    print(f"  false-refutes (gold != refuted): {false_refutes or 'none'}  -> precision "
          f"{0 if not refuted else round(100*(len(refuted)-len(false_refutes))/len(refuted))}%")
    print(f"  catches the wave-13 correlated misses: {catches}")

    # ---- combined gate on the physics set: numeric floor -> else the learned verdict ----
    MREC = json.load(open(os.path.join(HERE, "citation-panel-multidomain-receipt.json"), encoding="utf-8"))
    R = {r["id"]: r for r in MREC["multidomain_rows"]}
    det = {i: nf.numeric_check(next(c["claim"] for c in MULTI if c["id"] == i),
                               evidence_for(next(c for c in MULTI if c["id"] == i)))["verdict"] for i in MIDS}

    def combine(learned, i):
        return "refuted" if det[i] == "refuted" else learned

    def metrics(pred):
        fc = sorted(i for i in MIDS if pred[i] == "supported" and GOLD[i] != "supported")
        corr = sum(1 for i in MIDS if pred[i] == GOLD[i])
        return {"accuracy": round(100 * corr / len(MIDS), 1), "false_confirms": fc, "n_fc": len(fc)}

    layers = {}
    for name in ("llm_panel", "nli_doc", "floor", "consensus"):
        base = {i: R[i][name] for i in MIDS}
        comb = {i: combine(base[i], i) for i in MIDS}
        layers[name] = {"alone": metrics(base), "plus_numeric_floor": metrics(comb)}

    print("\n=== physics set — each learned layer, with vs without the deterministic floor ===")
    for name, m in layers.items():
        a, b = m["alone"], m["plus_numeric_floor"]
        print(f"  {name:10} alone acc={a['accuracy']:>5}% fc={a['n_fc']}{a['false_confirms']}  "
              f"-> +floor acc={b['accuracy']:>5}% fc={b['n_fc']}{b['false_confirms']}")

    receipt = {
        "schema": "tensor-engine-knowledge/citation-panel-numeric-receipt/v1",
        "kind": "verifier-deterministic-numeric-unit-floor", "wave": 14, "date": DATE,
        "n_cases": len(ALL), "n_refuted": len(refuted), "refuted_ids": refuted,
        "false_refutes": false_refutes, "precision_pct": 0 if not refuted else
        round(100 * (len(refuted) - len(false_refutes)) / len(refuted)),
        "catches_wave13_correlated_misses": catches,
        "rows_nonabstain": [r for r in rows if r["verdict"]],
        "physics_layers_with_without_floor": layers,
        "floor_module": "numeric_floor.py",
        "floor_sha256": hashlib.sha256(open(os.path.join(HERE, "numeric_floor.py"), "rb").read()).hexdigest(),
    }
    out = os.path.join(HERE, "citation-panel-numeric-receipt.json")
    json.dump(receipt, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("\n=== verdict ===")
    print(f"  catches #48 (comparison) and #55 (unit): {catches}")
    print(f"  false-refutes across all {len(ALL)} cases: {false_refutes or 'none'} (precision {receipt['precision_pct']}%)")
    print(f"receipt -> {out}")


if __name__ == "__main__":
    run()
