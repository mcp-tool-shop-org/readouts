#!/usr/bin/env python3
"""Wave-12: refine the verify prompt's added-specific-check with a QUANTITY EXCEPTION so the LLM panel stops
over-escalating legitimate numeric PARAPHRASES (wave-11 #25/#26/#27), and re-measure for regressions.

Wave-11 found the hardened prompt's added-specific-check is too aggressive on numeric paraphrases: it stamped
'fewer than two-thirds' (of 23/36), 'more than half', and 'roughly 200' (of N=199) as INSUFFICIENT, where
NLI doc-level correctly said SUPPORTED. The fix is a surgical prompt change (verify_sys_numeric.txt): a
number that is a faithful restatement / rounding / one-step arithmetic consequence of a STATED quantity is
not 'added' — but a contradictory number is still refuted, and a genuinely-absent number is still insufficient.

This must FIX the numeric paraphrases WITHOUT regressing the numeric TRAPS (#8 'over 100,000' vs 1.4K -> refuted;
#20 'all 36' vs 23/36 -> refuted; #39 '70%' absent -> insufficient) or the correlated traps (#21/#22/#23), and
introduce NO new false-confirms. The labeled sets + the NLI doc seat are the external verifier.

Loads the override via OFFLOAD_VERIFY_SYS_FILE (set BEFORE importing offload — no edit to the frozen tool).
Reuses the pinned HARDENED panel verdicts + the pinned NLI doc verdicts (sha-pinned, same abstracts); runs
only the REFINED panel live. Needs llama-swap up (:9090).

  set HF_HOME=E:\\AI-Models\\hf-cache
  E:\\AI\\training\\unsloth-env\\Scripts\\python.exe citation_panel_eval_prompt_v2.py
"""
import json, os, hashlib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-06-03"
PROMPT = os.path.join(HERE, "verify_sys_numeric.txt")
os.environ["OFFLOAD_VERIFY_SYS_FILE"] = PROMPT  # MUST precede the offload import (it reads _V_SYS at load)
ofspec = importlib.util.spec_from_file_location("offload", os.environ.get("OFFLOAD_SCRIPT", "E:/AI-Models/studio-local/offload.py"))
offload = importlib.util.module_from_spec(ofspec); ofspec.loader.exec_module(offload)

C24 = json.load(open(os.path.join(HERE, "citations-real.json"), encoding="utf-8"))
ext = os.path.join(HERE, "citations-real-ext.json")
if os.path.exists(ext):
    C24 += json.load(open(ext, encoding="utf-8"))
HARD = json.load(open(os.path.join(HERE, "citations-hard.json"), encoding="utf-8"))
ALL = C24 + HARD
SRC = json.load(open(os.path.join(HERE, "abstracts-cache.json"), encoding="utf-8"))
GOLD = {c["id"]: c["gold"] for c in ALL}
IDS24 = [c["id"] for c in C24]
IDSH = [c["id"] for c in HARD]
NUMERIC_FIX = [25, 26, 27]                          # the over-escalations the refinement should recover
TRAPS = [8, 20, 21, 22, 23, 39]                     # must STAY not-supported (numeric + correlated + absent)


def panel_verdict(votes):
    sup = votes.count("supported")
    if sup > len(votes) / 2:
        return "supported"
    return "refuted" if votes.count("refuted") > votes.count("insufficient") else "insufficient"


# pinned HARDENED panel verdicts (24-case from the hardening receipt; hard-set recomputed from its llm votes)
H9 = json.load(open(os.path.join(HERE, "prompt-hardening-receipt.json"), encoding="utf-8"))
HREC = json.load(open(os.path.join(HERE, "citation-panel-hard-receipt.json"), encoding="utf-8"))
hardened = {row["id"]: row["panel"] for row in H9["panel"]["hardened"]["rows"]}
hardened.update({int(i): panel_verdict(list(v.values())) for i, v in HREC["hard_llm_votes"].items()})
# pinned NLI doc verdicts (24-case from the wave-10 nli receipt; hard-set from the wave-11 hard receipt)
NREC = json.load(open(os.path.join(HERE, "citation-panel-nli-receipt.json"), encoding="utf-8"))
nli_doc = {r["id"]: r["verdict"] for r in NREC["nli_rows"]}
nli_doc.update({r["id"]: r["nli_doc"] for r in HREC["hard_rows"]})


def evidence_for(case):
    s = SRC[case["arxiv_id"]]
    return f"{s['title']}. {s['abstract']}"


def metrics(pred, ids):
    corr = sum(1 for i in ids if pred[i] == GOLD[i])
    fc = sorted(i for i in ids if pred[i] == "supported" and GOLD[i] != "supported")
    over = sorted(i for i in ids if GOLD[i] == "supported" and pred[i] != "supported")
    return {"n": len(ids), "accuracy": round(100 * corr / len(ids), 1),
            "false_confirms": fc, "n_fc": len(fc), "over_escalation": over, "n_over": len(over)}


def floor_notsup(llm_v, nli_v):
    return nli_v if (llm_v == "supported" and nli_v != "supported") else llm_v


def run():
    print(f"refined prompt: {PROMPT}\n  sha256 {hashlib.sha256(offload._V_SYS.encode()).hexdigest()[:16]}…")
    refined_votes = {c["id"]: {} for c in ALL}
    for m in offload.PANEL_SEATS:  # seat-outer to minimize llama-swap swaps
        print(f"  refined seat: {m}")
        for c in ALL:
            refined_votes[c["id"]][m] = offload._verify_one(m, c["claim"], evidence_for(c))["verdict"]
    refined = {i: panel_verdict(list(refined_votes[i].values())) for i in refined_votes}
    floor_refined = {i: floor_notsup(refined[i], nli_doc[i]) for i in refined}

    sets = {"24-case (canonical traps)": IDS24, "hard-15 (numeric paraphrases)": IDSH, "combined-39": IDS24 + IDSH}
    print("\n=== hardened vs refined panel (accuracy / false-confirms / over-escalation) ===")
    summary = {}
    for label, ids in sets.items():
        mh, mr, mf = metrics(hardened, ids), metrics(refined, ids), metrics(floor_refined, ids)
        summary[label] = {"hardened": mh, "refined": mr, "refined_plus_nli_floor": mf}
        print(f"  {label}")
        print(f"    hardened       acc={mh['accuracy']:>5}%  fc={mh['n_fc']}{mh['false_confirms']}  over-esc={mh['n_over']}{mh['over_escalation']}")
        print(f"    refined        acc={mr['accuracy']:>5}%  fc={mr['n_fc']}{mr['false_confirms']}  over-esc={mr['n_over']}{mr['over_escalation']}")
        print(f"    refined+floor  acc={mf['accuracy']:>5}%  fc={mf['n_fc']}{mf['false_confirms']}  over-esc={mf['n_over']}{mf['over_escalation']}")

    print("\n=== numeric-paraphrase cases (should flip insufficient -> supported) ===")
    for i in NUMERIC_FIX:
        print(f"  #{i} gold={GOLD[i]:<10} hardened={hardened[i]:<12} refined={refined[i]:<12} "
              f"{'FIXED' if (hardened[i] != 'supported' and refined[i] == 'supported') else ''}")
    print("\n=== trap regression (MUST stay not-supported) ===")
    regress = []
    for i in TRAPS:
        bad = refined[i] == "supported" and GOLD[i] != "supported"
        if bad:
            regress.append(i)
        print(f"  #{i} gold={GOLD[i]:<12} hardened={hardened[i]:<12} refined={refined[i]:<12} "
              f"{'*** REGRESSION (new false-confirm) ***' if bad else 'ok'}")

    all_ids = IDS24 + IDSH
    new_fc = [i for i in all_ids if refined[i] == "supported" and GOLD[i] != "supported"
              and hardened[i] != "supported"]
    win = (metrics(refined, IDSH)["n_over"] < metrics(hardened, IDSH)["n_over"]) and not new_fc

    receipt = {
        "schema": "tensor-engine-knowledge/citation-panel-prompt-v2-receipt/v1",
        "kind": "verifier-numeric-paraphrase-prompt-refinement", "wave": 12, "date": DATE,
        "refined_prompt_file": "verify_sys_numeric.txt",
        "refined_prompt_sha256": hashlib.sha256(offload._V_SYS.encode()).hexdigest(),
        "hardened_prompt_sha256": "c7ea81d59d33a4bfeb2964889011a0bc3fe5d855c2a4bc74cda25afe973434a1",
        "llm_seats": offload.PANEL_SEATS,
        "n_cases": len(all_ids), "numeric_fix_cases": NUMERIC_FIX, "trap_regression_cases": TRAPS,
        "summary": summary,
        "refined_votes": refined_votes,
        "rows": [{"id": i, "gold": GOLD[i], "hardened": hardened[i], "refined": refined[i],
                  "nli_doc": nli_doc[i], "refined_plus_floor": floor_refined[i]} for i in all_ids],
        "numeric_fixed": [i for i in NUMERIC_FIX if hardened[i] != "supported" and refined[i] == "supported"],
        "new_false_confirms": new_fc,
        "regressions": regress,
        "clean_win": bool(win),
    }
    out = os.path.join(HERE, "citation-panel-prompt-v2-receipt.json")
    json.dump(receipt, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("\n=== verdict ===")
    print(f"  numeric paraphrases fixed: {receipt['numeric_fixed']}")
    print(f"  new false-confirms (anywhere): {new_fc or 'none'}   regressions on traps: {regress or 'none'}")
    print(f"  CLEAN WIN (numerics fixed, no new false-confirms): {win}")
    print(f"receipt -> {out}")


if __name__ == "__main__":
    run()
