#!/usr/bin/env python3
"""Wave-13: test the orthogonal NLI seat's GENERALITY beyond AI/ML (physical-sciences abstracts) + a
DISAGREEMENT-GATED consensus combination (the UNCERTAINTY_GATED_HUMANS standard made concrete).

Two questions:
  1. Generality. The NLI seat aced AI/ML traps (waves 10-11) — does it hold on a DIFFERENT domain
     (gravitational waves / particle physics / cosmology / black-hole imaging; numeric-heavy, alien
     vocabulary)? citations-multidomain.json = 17 cases grounded in 5 real sha-pinned physics abstracts.
  2. The #26 residual. The monotone-safe floor can only DOWNGRADE a 'supported', so it can't fix a case
     where the LLM panel confidently REFUTES a true claim but the NLI seat is right (#26). A CONSENSUS
     gate escalates instead: 'supported' only if BOTH mechanisms agree; a disagreement on the supported
     axis -> 'insufficient' (review). It never auto-confirms on disagreement (0-fc) and never auto-refutes
     a claim the orthogonal seat supports.

The LLM panel runs LIVE on the multi-domain set with offload's DEFAULT prompt — which is now the wave-12
QUANTITY-EXCEPTION prompt (promoted), so this also confirms the shipped verifier on a new domain. The
39-case regression reuses pinned verdicts (refined panel from wave-12; NLI doc from waves 10-11).
Needs torch+transformers (unsloth-env) AND llama-swap up (:9090).

  set HF_HOME=E:\\AI-Models\\hf-cache
  E:\\AI\\training\\unsloth-env\\Scripts\\python.exe citation_panel_eval_multidomain.py
"""
import json, os, hashlib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-06-03"

spec = importlib.util.spec_from_file_location("nli_verify", os.path.join(HERE, "nli_verify.py"))
nli = importlib.util.module_from_spec(spec); spec.loader.exec_module(nli)
os.environ.pop("OFFLOAD_VERIFY_SYS_FILE", None)  # use offload's PROMOTED default (wave-12 refined prompt)
ofspec = importlib.util.spec_from_file_location("offload", os.environ.get("OFFLOAD_SCRIPT", "E:/AI-Models/studio-local/offload.py"))
offload = importlib.util.module_from_spec(ofspec); ofspec.loader.exec_module(offload)

MULTI = json.load(open(os.path.join(HERE, "citations-multidomain.json"), encoding="utf-8"))
SRCM = json.load(open(os.path.join(HERE, "abstracts-cache-multidomain.json"), encoding="utf-8"))
GOLDM = {c["id"]: c["gold"] for c in MULTI}
MIDS = [c["id"] for c in MULTI]


def evidence_for(case, src):
    s = src[case["arxiv_id"]]
    return f"{s['title']}. {s['abstract']}"


def panel_verdict(votes):
    sup = votes.count("supported")
    if sup > len(votes) / 2:
        return "supported"
    return "refuted" if votes.count("refuted") > votes.count("insufficient") else "insufficient"


def metrics(pred, ids, gold):
    corr = sum(1 for i in ids if pred[i] == gold[i])
    fc = sorted(i for i in ids if pred[i] == "supported" and gold[i] != "supported")
    over = sorted(i for i in ids if gold[i] == "supported" and pred[i] != "supported")
    return {"n": len(ids), "accuracy": round(100 * corr / len(ids), 1),
            "false_confirms": fc, "n_fc": len(fc), "over_escalation": over, "n_over": len(over)}


def floor_notsup(llm_v, nli_v):
    return nli_v if (llm_v == "supported" and nli_v != "supported") else llm_v


def consensus(llm_v, nli_v):
    """'supported' only if BOTH agree; disagreement on the supported axis -> escalate ('insufficient')."""
    sup_llm, sup_nli = (llm_v == "supported"), (nli_v == "supported")
    if sup_llm and sup_nli:
        return "supported"
    if sup_llm != sup_nli:
        return "insufficient"   # disagreement -> review (never auto-confirm, never auto-refute)
    return llm_v                # both not-supported -> the panel's specific verdict


def run():
    # ---- multi-domain: NLI doc + LLM panel LIVE ----
    nli_m, scores_m, rows = {}, {}, []
    print("=== multi-domain (physics) — NLI doc per case ===")
    for c in MULTI:
        r = nli.verify_one(c["claim"], evidence_for(c, SRCM))
        nli_m[c["id"]] = r["verdict"]; scores_m[c["id"]] = r["scores"]
        miss = "" if r["verdict"] == GOLDM[c["id"]] else "  <-- doc-MISS"
        print(f"  [{c['id']}] {c['note'].split(':')[0]:<18} gold={GOLDM[c['id']]:<12} nli={r['verdict']:<12}{miss}")
    print("\n=== multi-domain — LLM panel LIVE (offload default = wave-12 refined prompt) ===")
    llm_votes_m = {i: {} for i in MIDS}
    for m in offload.PANEL_SEATS:
        print(f"  seat: {m}")
        for c in MULTI:
            llm_votes_m[c["id"]][m] = offload._verify_one(m, c["claim"], evidence_for(c, SRCM))["verdict"]
    llm_m = {i: panel_verdict(list(llm_votes_m[i].values())) for i in MIDS}
    floor_m = {i: floor_notsup(llm_m[i], nli_m[i]) for i in MIDS}
    cons_m = {i: consensus(llm_m[i], nli_m[i]) for i in MIDS}
    escalated_m = [i for i in MIDS if (llm_m[i] == "supported") != (nli_m[i] == "supported")]
    for c in MULTI:
        i = c["id"]
        rows.append({"id": i, "gold": GOLDM[i], "note": c["note"].split(":")[0], "nli_doc": nli_m[i],
                     "nli_scores": scores_m[i], "llm_panel": llm_m[i], "llm_votes": llm_votes_m[i],
                     "floor": floor_m[i], "consensus": cons_m[i]})
    mm = {k: metrics(v, MIDS, GOLDM) for k, v in
          {"nli_doc": nli_m, "llm_panel": llm_m, "floor": floor_m, "consensus": cons_m}.items()}

    # ---- 39-case regression for the consensus gate (incl. the #26 residual), reusing pinned verdicts ----
    C24 = json.load(open(os.path.join(HERE, "citations-real.json"), encoding="utf-8"))
    ext = os.path.join(HERE, "citations-real-ext.json")
    if os.path.exists(ext):
        C24 += json.load(open(ext, encoding="utf-8"))
    HARD = json.load(open(os.path.join(HERE, "citations-hard.json"), encoding="utf-8"))
    gold39 = {c["id"]: c["gold"] for c in C24 + HARD}
    ids39 = list(gold39)
    V2 = json.load(open(os.path.join(HERE, "citation-panel-prompt-v2-receipt.json"), encoding="utf-8"))
    refined39 = {r["id"]: r["refined"] for r in V2["rows"]}
    NREC = json.load(open(os.path.join(HERE, "citation-panel-nli-receipt.json"), encoding="utf-8"))
    HREC = json.load(open(os.path.join(HERE, "citation-panel-hard-receipt.json"), encoding="utf-8"))
    nli39 = {r["id"]: r["verdict"] for r in NREC["nli_rows"]}
    nli39.update({r["id"]: r["nli_doc"] for r in HREC["hard_rows"]})
    cons39 = {i: consensus(refined39[i], nli39[i]) for i in ids39}
    reg = {"refined_panel": metrics(refined39, ids39, gold39),
           "consensus": metrics(cons39, ids39, gold39)}
    esc39 = [i for i in ids39 if (refined39[i] == "supported") != (nli39[i] == "supported")]
    case26 = {"refined_panel": refined39.get(26), "nli_doc": nli39.get(26), "consensus": cons39.get(26),
              "gold": gold39.get(26)}

    # ---- print ----
    print("\n=== multi-domain (17 physics cases) — accuracy / fc / over-escalation ===")
    for k, m in mm.items():
        print(f"  {k:12} acc={m['accuracy']:>5}%  fc={m['n_fc']}{m['false_confirms']}  over-esc={m['n_over']}{m['over_escalation']}")
    print(f"  consensus escalations (NLI vs panel disagreed): {escalated_m}")
    print("\n=== 39-case regression — consensus vs refined panel ===")
    for k, m in reg.items():
        print(f"  {k:14} acc={m['accuracy']:>5}%  fc={m['n_fc']}{m['false_confirms']}  over-esc={m['n_over']}")
    print(f"  consensus escalations on the 39: {esc39}")
    print(f"  #26 residual: gold={case26['gold']} refined_panel={case26['refined_panel']} "
          f"nli={case26['nli_doc']} -> consensus={case26['consensus']} (escalated for review, not auto-refuted)")

    receipt = {
        "schema": "tensor-engine-knowledge/citation-panel-multidomain-receipt/v1",
        "kind": "verifier-generality-and-consensus-gate", "wave": 13, "date": DATE,
        "multidomain_dataset": "citations-multidomain.json",
        "multidomain_sha256": hashlib.sha256(json.dumps(MULTI, sort_keys=True).encode()).hexdigest(),
        "domains": "physical sciences (gravitational waves / particle physics / cosmology / BH imaging)",
        "n_multidomain": len(MIDS), "nli_seat": {"model": nli.MODEL, "tau_support": nli.TAU_SUPPORT},
        "llm_seats": offload.PANEL_SEATS,
        "verify_prompt_sha256": hashlib.sha256(offload._V_SYS.encode()).hexdigest(),
        "source_pins": [{"arxiv_id": k, "title": v["title"], "abstract_sha256": v["sha256"]} for k, v in SRCM.items()],
        "multidomain_metrics": mm, "multidomain_rows": rows, "multidomain_escalations": escalated_m,
        "regression_39": reg, "regression_39_escalations": esc39, "case_26": case26,
        "consensus_zero_fc": (all(mm[k]["n_fc"] == 0 for k in mm) and reg["consensus"]["n_fc"] == 0),
    }
    out = os.path.join(HERE, "citation-panel-multidomain-receipt.json")
    json.dump(receipt, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("\n=== verdict ===")
    print(f"  NLI doc-level generality (physics, 17 cases): {mm['nli_doc']['accuracy']}% acc, {mm['nli_doc']['n_fc']} false-confirms")
    print(f"  consensus gate holds 0 false-confirms (multi-domain + 39-case): {receipt['consensus_zero_fc']}")
    print(f"receipt -> {out}")


if __name__ == "__main__":
    run()
