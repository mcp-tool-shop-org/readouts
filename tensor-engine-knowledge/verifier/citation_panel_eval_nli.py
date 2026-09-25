#!/usr/bin/env python3
"""Wave-10: measure the MECHANISTICALLY-ORTHOGONAL NLI seat (nli_verify.py) against the wave-9
correlated-failure ceiling, and the combined LLM-panel + NLI-floor.

Wave-9 proved family diversity can't fix CORRELATED error: the 3-family LLM panel (all decoder-only
instruct models) false-confirmed #21/#22/#23 under the legacy prompt (#22 fooled all three families).
Prompt-hardening recovered them, but that's a patch on the same mechanism. The durable fix is a member
that fails DIFFERENTLY. This wave adds an encoder NLI cross-encoder (DeBERTa-v3-large MNLI+FEVER+ANLI+
LingNLI+WANLI, MIT) and measures whether mechanistic orthogonality breaks the ceiling.

The LLM votes are REUSED (sha-pinned) from verifier/prompt-hardening-receipt.json — the LLMs ran in
wave-9 against the SAME sha-pinned abstracts, so reusing them is reproducible and needs no llama-swap.
Only the NLI seat runs here. Run with an env that has torch+transformers (the rig's unsloth-env):

  set HF_HOME=E:\\AI-Models\\hf-cache
  E:\\AI\\training\\unsloth-env\\Scripts\\python.exe citation_panel_eval_nli.py

Reports, on the full 24-case set + the original-16 subset + the 8 hard traps:
  - NLI seat SOLO (accuracy + false-confirms; is it itself safe?)
  - the correlated-fc catches (#21/#22/#23): does the orthogonal seat catch what every family slipped?
  - combined FLOOR panels (LLM panel + NLI veto-on-supported), for BOTH legacy and hardened LLM votes
  - NLI as a 4th conservative-majority SEAT (comparison)
  - a TAU_SUPPORT calibration sweep (the abstention threshold that holds 0 false-confirms at min cost)
  - the honest cost: over-escalation (genuinely-supported cases the floor downgrades to review)
"""
import json, os, hashlib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-06-03"
CORRELATED = [21, 22, 23]  # the wave-9 correlated false-confirms (legacy per-family panel)

spec = importlib.util.spec_from_file_location("nli_verify", os.path.join(HERE, "nli_verify.py"))
nli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nli)

CASES = json.load(open(os.path.join(HERE, "citations-real.json"), encoding="utf-8"))
BASE_IDS = {c["id"] for c in CASES}
ext_path = os.path.join(HERE, "citations-real-ext.json")
if os.path.exists(ext_path):
    CASES = CASES + json.load(open(ext_path, encoding="utf-8"))
SRC = json.load(open(os.path.join(HERE, "abstracts-cache.json"), encoding="utf-8"))
GOLD = {c["id"]: c["gold"] for c in CASES}
IDS = [c["id"] for c in CASES]
TRAP_IDS = [i for i in IDS if i not in BASE_IDS]

# wave-9 LLM panel votes (per-seat + panel verdict), legacy AND hardened — reused, sha-pinned.
HARD = json.load(open(os.path.join(HERE, "prompt-hardening-receipt.json"), encoding="utf-8"))
LLM_SEATS = HARD["seats"]
llm_panel = {p: {row["id"]: row["panel"] for row in HARD["panel"][p]["rows"]} for p in ("default", "hardened")}
llm_votes = {p: {row["id"]: row["votes"] for row in HARD["panel"][p]["rows"]} for p in ("default", "hardened")}


def evidence_for(case):
    s = SRC[case["arxiv_id"]]
    return f"{s['title']}. {s['abstract']}"


def metrics(pred, ids):
    corr = sum(1 for i in ids if pred[i] == GOLD[i])
    fc = sorted(i for i in ids if pred[i] == "supported" and GOLD[i] != "supported")
    over = sorted(i for i in ids if GOLD[i] == "supported" and pred[i] != "supported")  # escalated a true claim
    return {"n": len(ids), "correct": corr, "accuracy": round(100 * corr / len(ids), 1),
            "false_confirms": fc, "n_false_confirms": len(fc), "over_escalation": over}


def verdict_at(scores, tau):
    """Recompute the NLI verdict from cached scores at a given abstention threshold (cheap, no re-infer)."""
    top = max(scores, key=scores.get)
    if top == "entailment":
        return "supported" if scores["entailment"] >= tau else "insufficient"
    return "refuted" if top == "contradiction" else "insufficient"


def floor(llm_v, nli_v):
    """NLI as a conservative veto on 'supported': downgrade only; never upgrade. Cannot add a false-confirm."""
    if llm_v == "supported" and nli_v != "supported":
        return nli_v
    return llm_v


def majority4(votes_dict, nli_v):
    """4-seat conservative majority: 'supported' only on a STRICT majority (offload's rule)."""
    votes = list(votes_dict.values()) + [nli_v]
    sup = votes.count("supported")
    if sup > len(votes) / 2:
        return "supported"
    return "refuted" if votes.count("refuted") > votes.count("insufficient") else "insufficient"


def run():
    # ---- 1. run the NLI seat on every case (the only live inference here) ----
    nli_rows, scores_by_id, nli_pred = [], {}, {}
    print("=== NLI seat (DeBERTa-v3-large NLI) — per case ===")
    for c in CASES:
        r = nli.verify_one(c["claim"], evidence_for(c))
        nli_pred[c["id"]] = r["verdict"]
        scores_by_id[c["id"]] = r["scores"]
        nli_rows.append({"id": c["id"], "gold": GOLD[c["id"]], "verdict": r["verdict"],
                         "p_entailment": r["p_entailment"], "scores": r["scores"]})
        miss = "" if r["verdict"] == GOLD[c["id"]] else "  <-- miss"
        fc = "  *** FALSE-CONFIRM ***" if (r["verdict"] == "supported" and GOLD[c["id"]] != "supported") else ""
        trap = " [TRAP]" if c["id"] in TRAP_IDS else ""
        print(f"  [{c['id']:>2}]{trap:7} gold={GOLD[c['id']]:<12} nli={r['verdict']:<12} "
              f"P(ent)={r['p_entailment']:.3f}{miss}{fc}")

    full, base, traps = IDS, [i for i in IDS if i in BASE_IDS], TRAP_IDS
    nli_metrics = {"full": metrics(nli_pred, full), "base16": metrics(nli_pred, base), "traps": metrics(nli_pred, traps)}

    # ---- 2. the headline: does the orthogonal seat CATCH the correlated false-confirms? ----
    correlated_catch = {i: {"gold": GOLD[i], "llm_legacy_panel": llm_panel["default"][i],
                            "nli_verdict": nli_pred[i], "nli_scores": scores_by_id[i],
                            "caught": (llm_panel["default"][i] == "supported" and nli_pred[i] != "supported")}
                        for i in CORRELATED}

    # ---- 3. combined FLOOR panels (NLI veto-on-supported) for legacy + hardened LLM votes ----
    floor_pred = {p: {i: floor(llm_panel[p][i], nli_pred[i]) for i in IDS} for p in ("default", "hardened")}
    floor_metrics = {p: {"full": metrics(floor_pred[p], full), "base16": metrics(floor_pred[p], base),
                         "traps": metrics(floor_pred[p], traps)} for p in ("default", "hardened")}

    # ---- 4. NLI as a 4th conservative-majority seat (comparison vs the floor) ----
    maj_pred = {p: {i: majority4(llm_votes[p][i], nli_pred[i]) for i in IDS} for p in ("default", "hardened")}
    maj_metrics = {p: {"full": metrics(maj_pred[p], full), "traps": metrics(maj_pred[p], traps)}
                   for p in ("default", "hardened")}

    # ---- 5. TAU calibration sweep (abstention threshold) ----
    taus = [round(0.50 + 0.05 * k, 2) for k in range(9)]  # 0.50 .. 0.90
    sweep = []
    for t in taus:
        pt = {i: verdict_at(scores_by_id[i], t) for i in IDS}
        m = metrics(pt, full)
        # floor at this tau, on the legacy panel (the hard case)
        fl = {i: floor(llm_panel["default"][i], pt[i]) for i in IDS}
        fm = metrics(fl, full)
        sweep.append({"tau": t, "nli_solo": {"accuracy": m["accuracy"], "n_fc": m["n_false_confirms"],
                                             "n_over_escalation": len(m["over_escalation"])},
                      "floor_legacy": {"accuracy": fm["accuracy"], "n_fc": fm["n_false_confirms"],
                                       "n_over_escalation": len(fm["over_escalation"])}})

    # ---- print summary ----
    print("\n=== NLI seat SOLO ===")
    for k, m in nli_metrics.items():
        print(f"  {k:7} {m['correct']}/{m['n']} = {m['accuracy']:>5}%   false-confirms={m['n_false_confirms']} {m['false_confirms']}")
    print("\n=== correlated false-confirms (#21/#22/#23) — does the orthogonal seat catch them? ===")
    for i in CORRELATED:
        cc = correlated_catch[i]
        print(f"  #{i} gold={cc['gold']:<12} legacy-LLM-panel={cc['llm_legacy_panel']:<11} "
              f"NLI={cc['nli_verdict']:<12} caught={cc['caught']}")
    print("\n=== combined LLM panel + NLI FLOOR (veto on 'supported') ===")
    for p in ("default", "hardened"):
        lm = metrics(llm_panel[p], full)
        fm = floor_metrics[p]["full"]
        print(f"  LLM-{p:8} panel: acc={lm['accuracy']:>5}% fc={lm['n_false_confirms']}{lm['false_confirms']}  "
              f"-> +NLI floor: acc={fm['accuracy']:>5}% fc={fm['n_false_confirms']} over-esc={len(fm['over_escalation'])}{fm['over_escalation']}")
    print("\n=== NLI as a 4th majority seat (comparison) ===")
    for p in ("default", "hardened"):
        mm = maj_metrics[p]["full"]
        print(f"  4-seat majority ({p}): acc={mm['accuracy']:>5}% fc={mm['n_false_confirms']}{mm['false_confirms']}")
    print("\n=== TAU_SUPPORT sweep (NLI abstention threshold) ===")
    for s in sweep:
        print(f"  tau={s['tau']:.2f}  NLI-solo acc={s['nli_solo']['accuracy']:>5}% fc={s['nli_solo']['n_fc']} "
              f"over-esc={s['nli_solo']['n_over_escalation']}   |  floor-legacy acc={s['floor_legacy']['accuracy']:>5}% "
              f"fc={s['floor_legacy']['n_fc']} over-esc={s['floor_legacy']['n_over_escalation']}")

    # ---- receipt ----
    receipt = {
        "schema": "tensor-engine-knowledge/citation-panel-nli-receipt/v1",
        "kind": "verifier-orthogonal-nli-seat-eval",
        "wave": 10,
        "date": DATE,
        "thesis": ("family diversity fixes UNCORRELATED error; an encoder NLI cross-encoder (different "
                   "MECHANISM, reasoning-stripped) is mechanistically orthogonal and catches the CORRELATED "
                   "false-confirms a decoder-only LLM panel shares."),
        "dataset": "citations-real.json" + ("+citations-real-ext.json" if os.path.exists(ext_path) else ""),
        "dataset_sha256": hashlib.sha256(json.dumps(CASES, sort_keys=True).encode()).hexdigest(),
        "n_cases": len(IDS), "n_base16": len(base), "n_traps": len(traps),
        "n_not_supported": sum(1 for i in IDS if GOLD[i] != "supported"),
        # PIN_PER_STEP — the orthogonal seat, the reused LLM votes (a DIFFERENT receipt), the threshold.
        "nli_seat": {"model": nli.MODEL, "license": "MIT (DeBERTa-v3-large base; MoritzLaurer NLI head)",
                     "mechanism": "encoder cross-encoder, 3-way NLI classifier (no chain-of-thought, no prompt)",
                     "tau_support": nli.TAU_SUPPORT, "mapping": {"entailment": "supported",
                     "contradiction": "refuted", "neutral": "insufficient"}},
        "llm_votes_source": {"receipt": "prompt-hardening-receipt.json",
                             "sha256": hashlib.sha256(json.dumps(HARD, sort_keys=True).encode()).hexdigest(),
                             "seats": LLM_SEATS},
        "source_pins": [{"arxiv_id": k, "title": v["title"], "abstract_sha256": v["sha256"], "source": v["source"]}
                        for k, v in SRC.items() if any(c["arxiv_id"] == k for c in CASES)],
        "nli_solo": nli_metrics,
        "nli_rows": nli_rows,
        "correlated_catch": correlated_catch,
        "correlated_all_caught": all(correlated_catch[i]["caught"] for i in CORRELATED),
        "floor_panels": {p: {**floor_metrics[p],
                             "rows": [{"id": i, "gold": GOLD[i], "llm_panel": llm_panel[p][i],
                                       "nli": nli_pred[i], "floor": floor_pred[p][i]} for i in IDS]}
                         for p in ("default", "hardened")},
        "fourth_seat_majority": maj_metrics,
        "tau_sweep": sweep,
        "floor_zero_fc_both": all(floor_metrics[p]["full"]["n_false_confirms"] == 0 for p in ("default", "hardened")),
    }
    out = os.path.join(HERE, "citation-panel-nli-receipt.json")
    json.dump(receipt, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("\n=== verdict ===")
    print(f"  orthogonal seat catches ALL correlated false-confirms (#21/#22/#23): {receipt['correlated_all_caught']}")
    print(f"  LLM panel + NLI floor holds 0 false-confirms (legacy AND hardened): {receipt['floor_zero_fc_both']}")
    print(f"  NLI seat solo: {nli_metrics['full']['accuracy']}% acc, {nli_metrics['full']['n_false_confirms']} false-confirms on {len(IDS)} cases")
    print(f"receipt -> {out}")


if __name__ == "__main__":
    run()
