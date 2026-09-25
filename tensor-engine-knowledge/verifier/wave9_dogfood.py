#!/usr/bin/env python3
"""Wave-9 Move #3 — dogfood BOTH offload paths on a REAL study-swarm wave, measured end-to-end.

The wave: 3 parallel research agents grounded the wave-9 finding (does family diversity fix
correlated verifier errors?). This script runs that wave's real artifacts through the wiring:

  PREREAD  — compress each agent's large output (waves/wave-09.../research-raw.md sections) to a
             word-budget digest via `offload compress`; report aggregate Claude-token savings (the
             "before/after across a real wave" the offload kickoff asked for).
  VERIFY   — the citations the swarm produced go through the wave-9 hardened panel (offload
             PANEL_SEATS, conservative majority) against the cited papers' REAL abstracts (Semantic
             Scholar); report per-citation verdicts + CATCHES: overstated claims (panel != supported)
             and unfetchable/fabricated citations (the existence floor — never silently dropped).

stdlib + offload + fetch_abstracts only. llama-swap (:9090) + network required.
  python wave9_dogfood.py
"""
import json, os, sys, subprocess, importlib.util, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-06-03"
OFFLOAD = os.environ.get("OFFLOAD_SCRIPT", "E:/AI-Models/studio-local/offload.py")
RESEARCH = os.path.join(HERE, "..", "waves", "wave-09-verifier-hardening", "research-raw.md")

_spec = importlib.util.spec_from_file_location("offload", OFFLOAD)
offload = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(offload)
_fa = importlib.util.spec_from_file_location("fetch_abstracts", os.path.join(HERE, "fetch_abstracts.py"))
fetch_abstracts = importlib.util.module_from_spec(_fa); _fa.loader.exec_module(fetch_abstracts)

# The citations the swarm produced (one-sentence finding per cited paper). Two IDs (2602.*, 2603.*)
# are future-dated preprints the agents flagged as UNCONFIRMED — included on purpose to exercise the
# existence floor (a citation gate must catch a non-resolving id, never wave it through).
CITS = [
    {"id": "A1", "arxiv_id": "2506.07962", "claim": "Across more than 350 LLMs, models tend to agree with each other even when both are wrong, and larger, more-accurate models show more correlated errors even across different providers and architectures."},
    {"id": "A2", "arxiv_id": "2602.08003", "claim": "Choosing ensemble members by mutual-information diversity produces a collectively more accurate panel than choosing the individually strongest models."},
    {"id": "A3", "arxiv_id": "2603.17111", "claim": "Family-correlated errors reduce a multi-member model ensemble to only about three effectively-independent voters."},
    {"id": "A4", "arxiv_id": "2404.18796", "claim": "A panel of several smaller, diverse-family judges reduces evaluation bias and can outperform a single larger judge."},
    {"id": "A5", "arxiv_id": "2410.21819", "claim": "LLM judges show self-preference bias, scoring text that is familiar or low-perplexity to them more highly."},
    {"id": "A6", "arxiv_id": "2406.07791", "claim": "Position bias in LLM-as-a-judge evaluation is systematic rather than random and varies by judge and task."},
    {"id": "B1", "arxiv_id": "2311.01740", "claim": "Sampling a single model for self-consistency cannot detect hallucinations the model makes consistently; cross-checking with reworded questions and a different model detects more."},
    {"id": "B2", "arxiv_id": "2508.17536", "claim": "In multi-agent LLM systems the diversity of the agents is the key factor determining whether voting or debate improves decisions."},
    {"id": "B3", "arxiv_id": "2112.12870", "claim": "Attribution to identified sources requires that each generated statement be entailed by the independent source it cites."},
    {"id": "B4", "arxiv_id": "2305.14251", "claim": "FActScore decomposes generated text into atomic facts and checks each one against a knowledge source to score factual precision."},
    {"id": "C1", "arxiv_id": "2305.04388", "claim": "Chain-of-thought explanations are often plausible but unfaithful, justifying an answer the model actually reached for a different, undisclosed reason."},
    {"id": "C2", "arxiv_id": "2310.13548", "claim": "Models trained with RLHF show sycophancy, tending to agree with a user's stated opinion even when it is wrong."},
    {"id": "C3", "arxiv_id": "2503.01670", "claim": "An LLM judge's own background knowledge biases its assessment of hallucinations when the provided context is mixed."},
    {"id": "C4", "arxiv_id": "2210.04695", "claim": "Language models are weak at directional inference, often failing to tell which of two statements entails the other."},
    {"id": "C5", "arxiv_id": "2305.14540", "claim": "On fine-grained factual-consistency benchmarks most large language models perform close to chance."},
    {"id": "C6", "arxiv_id": "2506.07446", "claim": "Verifying a claim by splitting it into atomic facts and checking each against the source improves verification precision."},
    {"id": "C7", "arxiv_id": "2508.06225", "claim": "LLM judges are systematically overconfident, so a 'confirmed' verdict carries inflated certainty."},
]


def preread():
    """Compress each agent section of research-raw.md; aggregate the token saving."""
    text = open(RESEARCH, encoding="utf-8").read()
    sections = re.split(r"^## Agent ", text, flags=re.M)[1:]
    out = []
    for i, sec in enumerate(sections):
        tmp = os.path.join(HERE, f"_wave9_src_{i}.txt")
        open(tmp, "w", encoding="utf-8").write("## Agent " + sec)
        r = subprocess.run([sys.executable, OFFLOAD, "compress", "--json", "--file", tmp, "--words", "90"],
                           capture_output=True, text=True, encoding="utf-8")
        os.remove(tmp)
        try:
            d = json.loads(r.stdout)
        except Exception:
            print(f"  compress failed for section {i}: {r.stderr[:200]}", file=sys.stderr); continue
        out.append({"source": f"agent-{chr(65+i)}", "in_tokens": d["in_tokens"],
                    "out_tokens": d["out_tokens"], "reduction_pct": d["reduction_pct"]})
        print(f"  agent-{chr(65+i)}: {d['in_tokens']} -> {d['out_tokens']} tok ({d['reduction_pct']}% smaller)")
    return out


def panel(votes):
    sup = votes.count("supported")
    if sup > len(votes) / 2:
        return "supported"
    return "refuted" if votes.count("refuted") > votes.count("insufficient") else "insufficient"


def verify():
    ids = sorted({c["arxiv_id"] for c in CITS})
    print(f"\nfetching {len(ids)} cited abstracts (Semantic Scholar)...")
    src = fetch_abstracts.fetch(ids)
    json.dump(src, open(os.path.join(HERE, "wave9-abstracts-cache.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)
    missing = [i for i in ids if i not in src]   # existence-floor catches (unresolved/fabricated)
    seats = offload.PANEL_SEATS
    verifiable = [c for c in CITS if c["arxiv_id"] in src]
    preds = {m: {} for m in seats}
    for m in seats:
        print(f"  panel seat: {m}")
        for c in verifiable:
            s = src[c["arxiv_id"]]
            ev = f"Title: {s['title']}\n\nAbstract: {s['abstract']}"
            preds[m][c["id"]] = offload._verify_one(m, c["claim"], ev)["verdict"]
    rows = []
    for c in verifiable:
        votes = [preds[m][c["id"]] for m in seats]
        rows.append({"id": c["id"], "arxiv_id": c["arxiv_id"], "claim": c["claim"],
                     "panel": panel(votes), "votes": {m: preds[m][c["id"]] for m in seats}})
    return src, missing, rows, seats


def run():
    print("=== PREREAD (token economy across the wave) ===")
    pre = preread()
    tin = sum(p["in_tokens"] for p in pre); tout = sum(p["out_tokens"] for p in pre)
    agg = round(100 * (1 - tout / tin), 1) if tin else None
    print(f"  AGGREGATE: {tin} -> {tout} Claude-tokens = {agg}% saved across {len(pre)} sources")

    print("\n=== VERIFY (citations through the wave-9 hardened panel) ===")
    src, missing, rows, seats = verify()
    supported = [r for r in rows if r["panel"] == "supported"]
    flagged = [r for r in rows if r["panel"] != "supported"]
    print(f"\n  seats (PIN): {seats}")
    print(f"  citations submitted: {len(CITS)}  fetched: {len(rows)}  unresolved(existence catch): {len(missing)} {missing}")
    print(f"  panel SUPPORTED: {len(supported)}/{len(rows)}")
    print(f"  panel FLAGGED (not supported -> escalate): {len(flagged)}")
    for r in flagged:
        print(f"    [{r['id']}] {r['arxiv_id']} -> {r['panel']}  votes={r['votes']}")

    receipt = {
        "schema": "tensor-engine-knowledge/wave9-dogfood-receipt/v1", "wave": 9, "date": DATE,
        "kind": "real-wave-dogfood",
        "preread": {"sources": pre, "aggregate_in_tokens": tin, "aggregate_out_tokens": tout,
                    "aggregate_reduction_pct": agg},
        "verify": {
            "panel_seats": seats,
            "verify_prompt_sha256": hashlib.sha256(offload._V_SYS.encode()).hexdigest(),
            "submitted": len(CITS), "fetched": len(rows),
            "unresolved_existence_catches": missing,
            "panel_supported": len(supported), "panel_flagged": len(flagged),
            "rows": rows,
            "source_pins": [{"arxiv_id": k, "title": v["title"], "abstract_sha256": v["sha256"]} for k, v in src.items()],
        },
    }
    out = os.path.join(HERE, "wave9-dogfood-receipt.json")
    json.dump(receipt, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"\nreceipt -> {out}")


if __name__ == "__main__":
    run()
