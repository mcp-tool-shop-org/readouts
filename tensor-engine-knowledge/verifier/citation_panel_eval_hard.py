#!/usr/bin/env python3
"""Wave-11: stress the orthogonal NLI seat BEYOND NLI-canonical traps + add sentence-level evidence
selection, and measure where the COMBINATION (LLM panel + NLI floor) actually wins.

Wave-10's 24-case set was NLI-canonical (inversions->contradiction, unstated->neutral) and the NLI seat
aced it (100%). To find the seat's real limits we add `citations-hard.json` (15 cases grounded in the SAME
sha-pinned abstracts) that stress NUMERIC/arithmetic, MULTI-HOP, SCOPE/added-entity, subtle PARAPHRASE, and
harder inversions — the reasoning an encoder NLI classifier is theoretically weak at and where the LLM panel
should earn its seat.

Two questions, measured (not assumed):
  1. Does sentence-level (FEVER-style: NLI claim-vs-each-sentence, max-aggregate) help or hurt vs document-
     level (NLI over the whole abstract)? Helps buried single-sentence evidence; can hurt multi-hop.
  2. The floor's cost. Two veto rules:
       floor_notsup     : downgrade an LLM 'supported' whenever the NLI seat != supported  (0-fc by construction)
       floor_contra     : downgrade only on NLI 'refuted' (a STRONG contradiction signal)  (less over-escalation)
     The hard set should reveal the safety (false-confirm) vs recall (over-escalation) trade between them.

The LLM panel runs LIVE on the hard set (these cases are NOT in any pinned receipt); the 24-case regression
reuses the wave-9 hardened panel votes. Needs torch+transformers (unsloth-env) AND llama-swap up (:9090).

  set HF_HOME=E:\\AI-Models\\hf-cache
  E:\\AI\\training\\unsloth-env\\Scripts\\python.exe citation_panel_eval_hard.py
"""
import json, os, hashlib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-06-03"

spec = importlib.util.spec_from_file_location("nli_verify", os.path.join(HERE, "nli_verify.py"))
nli = importlib.util.module_from_spec(spec); spec.loader.exec_module(nli)
ofspec = importlib.util.spec_from_file_location("offload", os.environ.get("OFFLOAD_SCRIPT", "E:/AI-Models/studio-local/offload.py"))
offload = importlib.util.module_from_spec(ofspec); ofspec.loader.exec_module(offload)

SRC = json.load(open(os.path.join(HERE, "abstracts-cache.json"), encoding="utf-8"))
HARD = json.load(open(os.path.join(HERE, "citations-hard.json"), encoding="utf-8"))
GOLD = {c["id"]: c["gold"] for c in HARD}
HARD_IDS = [c["id"] for c in HARD]
# 24-case regression (sentence-level vs doc-level on the canonical traps); LLM votes reused from wave-9.
C24 = json.load(open(os.path.join(HERE, "citations-real.json"), encoding="utf-8"))
ext = os.path.join(HERE, "citations-real-ext.json")
if os.path.exists(ext):
    C24 += json.load(open(ext, encoding="utf-8"))
GOLD24 = {c["id"]: c["gold"] for c in C24}
HARDENED = json.load(open(os.path.join(HERE, "prompt-hardening-receipt.json"), encoding="utf-8"))
llm24 = {row["id"]: row["panel"] for row in HARDENED["panel"]["hardened"]["rows"]}


def evidence_for(case):
    s = SRC[case["arxiv_id"]]
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


def floor_contra(llm_v, nli_v):
    return "refuted" if (llm_v == "supported" and nli_v == "refuted") else llm_v


def run():
    # ---- NLI doc + sentence on the HARD set ----
    nli_doc, nli_sent, rows = {}, {}, []
    print("=== HARD set — NLI doc vs sentence ===")
    for c in HARD:
        ev = evidence_for(c)
        d = nli.verify_one(c["claim"], ev)
        s = nli.verify_one_sentencewise(c["claim"], ev)
        nli_doc[c["id"]], nli_sent[c["id"]] = d["verdict"], s["verdict"]
        rows.append({"id": c["id"], "gold": GOLD[c["id"]], "note": c["note"].split(":")[0],
                     "nli_doc": d["verdict"], "doc_scores": d["scores"],
                     "nli_sentence": s["verdict"], "sent_max_ent": s["max_entailment"],
                     "sent_max_con": s["max_contradiction"]})
        f = "" if d["verdict"] == GOLD[c["id"]] else " doc-MISS"
        g = "" if s["verdict"] == GOLD[c["id"]] else " sent-MISS"
        print(f"  [{c['id']:>2}] {c['note'].split(':')[0]:<22} gold={GOLD[c['id']]:<12} "
              f"doc={d['verdict']:<12}{f:<9} sent={s['verdict']:<12}{g}")

    # ---- LLM panel LIVE on the HARD set (seat-outer to minimize llama-swap swaps) ----
    print("\n=== HARD set — LLM panel (live, hardened prompt) ===")
    llm_votes = {i: {} for i in HARD_IDS}
    for m in offload.PANEL_SEATS:
        print(f"  seat: {m}")
        for c in HARD:
            r = offload._verify_one(m, c["claim"], evidence_for(c))
            llm_votes[c["id"]][m] = r["verdict"]
    llm_panel = {i: panel_verdict(list(llm_votes[i].values())) for i in HARD_IDS}

    # ---- combine: 4 floor variants on the HARD set ----
    combos = {
        "llm_panel":            llm_panel,
        "nli_doc":              nli_doc,
        "nli_sentence":         nli_sent,
        "floor_doc_notsup":     {i: floor_notsup(llm_panel[i], nli_doc[i]) for i in HARD_IDS},
        "floor_sent_notsup":    {i: floor_notsup(llm_panel[i], nli_sent[i]) for i in HARD_IDS},
        "floor_doc_contra":     {i: floor_contra(llm_panel[i], nli_doc[i]) for i in HARD_IDS},
        "floor_sent_contra":    {i: floor_contra(llm_panel[i], nli_sent[i]) for i in HARD_IDS},
    }
    hard_metrics = {k: metrics(v, HARD_IDS, GOLD) for k, v in combos.items()}

    # ---- 24-case regression: does sentence-level keep the canonical traps? ----
    print("\n=== 24-case regression — NLI doc vs sentence ===")
    n24_doc, n24_sent = {}, {}
    for c in C24:
        ev = evidence_for(c)
        n24_doc[c["id"]] = nli.verify_one(c["claim"], ev)["verdict"]
        n24_sent[c["id"]] = nli.verify_one_sentencewise(c["claim"], ev)["verdict"]
    reg = {"nli_doc": metrics(n24_doc, [c["id"] for c in C24], GOLD24),
           "nli_sentence": metrics(n24_sent, [c["id"] for c in C24], GOLD24),
           "floor_doc_notsup": metrics({i: floor_notsup(llm24[i], n24_doc[i]) for i in GOLD24},
                                       list(GOLD24), GOLD24),
           "floor_sent_notsup": metrics({i: floor_notsup(llm24[i], n24_sent[i]) for i in GOLD24},
                                        list(GOLD24), GOLD24)}

    # ---- print summary ----
    print("\n=== HARD set — accuracy / false-confirms / over-escalation ===")
    for k in combos:
        m = hard_metrics[k]
        print(f"  {k:20} acc={m['accuracy']:>5}%  fc={m['n_fc']}{m['false_confirms']}  over-esc={m['n_over']}{m['over_escalation']}")
    print("\n=== 24-case regression ===")
    for k, m in reg.items():
        print(f"  {k:20} acc={m['accuracy']:>5}%  fc={m['n_fc']}{m['false_confirms']}  over-esc={m['n_over']}")

    # disagreements: where NLI (doc) and the LLM panel differ on the hard set
    disagree = [{"id": i, "gold": GOLD[i], "llm_panel": llm_panel[i], "nli_doc": nli_doc[i],
                 "nli_sentence": nli_sent[i]} for i in HARD_IDS if llm_panel[i] != nli_doc[i]]

    receipt = {
        "schema": "tensor-engine-knowledge/citation-panel-hard-receipt/v1",
        "kind": "verifier-hard-set-and-sentence-level-eval", "wave": 11, "date": DATE,
        "hard_dataset": "citations-hard.json",
        "hard_dataset_sha256": hashlib.sha256(json.dumps(HARD, sort_keys=True).encode()).hexdigest(),
        "n_hard": len(HARD_IDS), "n_24": len(C24),
        "nli_seat": {"model": nli.MODEL, "tau_support": nli.TAU_SUPPORT, "tau_contra": nli.TAU_CONTRA},
        "llm_seats": offload.PANEL_SEATS,
        "verify_prompt_sha256": hashlib.sha256(offload._V_SYS.encode()).hexdigest(),
        "source_pins": [{"arxiv_id": k, "abstract_sha256": v["sha256"]} for k, v in SRC.items()
                        if any(c["arxiv_id"] == k for c in HARD)],
        "hard_rows": rows,
        "hard_llm_votes": llm_votes,
        "hard_metrics": hard_metrics,
        "regression_24case": reg,
        "nli_llm_disagreements": disagree,
    }
    out = os.path.join(HERE, "citation-panel-hard-receipt.json")
    json.dump(receipt, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\nreceipt -> {out}")


if __name__ == "__main__":
    run()
