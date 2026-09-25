#!/usr/bin/env python3
"""nli_verify.py — a MECHANISTICALLY-ORTHOGONAL verifier seat for the citation panel (wave-10).

The wave-9 panel is three decoder-only instruct LLMs (Qwen + Mistral + IBM Granite). Family-different,
but the SAME MECHANISM — so they share a CORRELATED credulity blind spot: on the 24-case adversarial set,
a majority across ALL families false-confirmed #21/#22/#23 (and #22, a stricter/looser inversion, fooled
all three). Ensemble accuracy is bounded by member CORRELATION, not member count (Kuncheva & Whitaker,
Machine Learning 2003), so the durable fix is a member that FAILS DIFFERENTLY: an encoder-based NLI
cross-encoder trained DISCRIMINATIVELY on entailment/contradiction (MNLI + FEVER + ANLI + LingNLI + WANLI),
not a generative LLM. No chain-of-thought, no prompt — a calibrated 3-way classifier. This is the
mechanistically-orthogonal seat the wave-9 close named as the wave-10 candidate.

Model: MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli  (DeBERTa-v3-large base, MIT; ~435M params).
  FEVER in the training mix = fact-verification (claim vs. evidence) — the exact shape of a citation check.

Mapping (NLI premise = EVIDENCE = title+abstract, hypothesis = CLAIM):
  entailment    -> supported       contradiction -> refuted       neutral -> insufficient

Calibrated, ASYMMETRIC abstention (a citation GATE must never wave through a false claim; over-escalation
is the safe failure): return 'supported' ONLY if it is the argmax AND P(entailment) >= TAU_SUPPORT
(default 0.55); else downgrade a would-be 'supported' to 'insufficient'. 'refuted'/'insufficient' are NOT
thresholded — being quick to escalate is safe, only false-CONFIRM is dangerous.

Designed as a conservative FLOOR/veto under the LLM panel: if the panel says 'supported' but this seat
does not, the combined verdict is downgraded. Orthogonal + reasoning-stripped = the strongest external
verifier (workflow-standards EXTERNAL_VERIFIER: a different family AND a different mechanism, no shared CoT).

Run with an env that has torch+transformers (the rig's unsloth-env). CLI:
  python nli_verify.py --smoke                 # load + print id2label + sanity cases (incl. #21/#22 types)
  python nli_verify.py "<claim>" "<evidence>"  # one verdict as JSON
"""
import os, sys, json, re, functools

MODEL = os.environ.get("NLI_MODEL", "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli")
TAU_SUPPORT = float(os.environ.get("NLI_TAU_SUPPORT", "0.55"))
TAU_CONTRA = float(os.environ.get("NLI_TAU_CONTRA", "0.5"))  # sentence-level: a sentence "clearly contradicts"


@functools.lru_cache(maxsize=1)
def _model():
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    model.eval()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(dev)
    id2label = {int(k): v.lower() for k, v in model.config.id2label.items()}  # robust to the model's own order
    return tok, model, dev, id2label


def nli_scores(premise, hypothesis):
    """P(entailment/neutral/contradiction) that PREMISE entails HYPOTHESIS."""
    import torch
    tok, model, dev, id2label = _model()
    inp = tok(premise, hypothesis, truncation=True, max_length=512, return_tensors="pt").to(dev)
    with torch.no_grad():
        logits = model(**inp).logits[0]
    probs = torch.softmax(logits, -1).tolist()
    return {id2label[i]: probs[i] for i in range(len(probs))}


def verify_one(claim, evidence, tau_support=TAU_SUPPORT):
    """Document-level: NLI over the WHOLE evidence (title + abstract) as a single premise."""
    s = nli_scores(evidence, claim)  # premise = evidence, hypothesis = claim
    ent = s.get("entailment", 0.0)
    top = max(s, key=s.get)
    if top == "entailment":
        verdict = "supported" if ent >= tau_support else "insufficient"
        abstained = ent < tau_support
    elif top == "contradiction":
        verdict, abstained = "refuted", False
    else:
        verdict, abstained = "insufficient", False
    return {"verdict": verdict, "abstained": abstained, "p_entailment": round(ent, 4),
            "scores": {k: round(v, 4) for k, v in s.items()}, "seat": "nli", "mode": "doc", "model": MODEL}


def split_sentences(text):
    """Lightweight sentence split for scientific abstracts (max-aggregation tolerates the odd mis-split)."""
    text = (text or "").replace("\n", " ").strip()
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\"'])", text)
    return [p.strip() for p in parts if len(p.strip()) > 1]


def verify_one_sentencewise(claim, evidence, tau_support=TAU_SUPPORT, tau_contra=TAU_CONTRA):
    """Sentence-level (FEVER-style): NLI claim vs EACH evidence sentence; aggregate max-entailment /
    max-contradiction. Helps when the entailing evidence is one sentence buried in a long abstract; can
    hurt multi-hop claims that no single sentence entails. Asymmetric safety: 'supported' only on a clearly
    entailing sentence; a clearly contradicting sentence -> 'refuted'."""
    sents = split_sentences(evidence) or [evidence]
    per = [{"sentence": s, "scores": nli_scores(s, claim)} for s in sents]
    max_ent = max(p["scores"].get("entailment", 0.0) for p in per)
    max_con = max(p["scores"].get("contradiction", 0.0) for p in per)
    best_ent = max(per, key=lambda p: p["scores"].get("entailment", 0.0))["sentence"]
    best_con = max(per, key=lambda p: p["scores"].get("contradiction", 0.0))["sentence"]
    if max_con >= tau_contra and max_con >= max_ent:
        verdict, abstained = "refuted", False
    elif max_ent >= tau_support:
        verdict, abstained = "supported", False
    else:
        verdict, abstained = "insufficient", True
    return {"verdict": verdict, "abstained": abstained, "p_entailment": round(max_ent, 4),
            "max_entailment": round(max_ent, 4), "max_contradiction": round(max_con, 4),
            "best_entail_sentence": best_ent, "best_contra_sentence": best_con,
            "n_sentences": len(sents), "seat": "nli", "mode": "sentence", "model": MODEL}


SMOKE = [
    ("entailment / supported",
     "The method improves accuracy on the benchmark.",
     "We propose a new approach and show it improves accuracy by 10% on the benchmark."),
    ("contradiction / refuted  (the #22 inversion type)",
     "Looser format constraints cause greater degradation in reasoning than stricter ones.",
     "We find that stricter format constraints lead to greater degradation in LLM reasoning performance."),
    ("neutral / insufficient  (the #21 unstated-entity type)",
     "The paper measures self-preference bias separately for GPT-4, Llama 2, and Claude.",
     "We measure self-preference bias for GPT-4 and Llama 2 on a summarization task."),
]


def smoke():
    tok, model, dev, id2label = _model()
    n_params = sum(p.numel() for p in model.parameters())
    print(f"model:   {MODEL}")
    print(f"device:  {dev}   params: {n_params/1e6:.0f}M   id2label: {id2label}   TAU_SUPPORT={TAU_SUPPORT}")
    print("-" * 88)
    for label, claim, evidence in SMOKE:
        r = verify_one(claim, evidence)
        print(f"[{label}]\n  claim:    {claim}\n  evidence: {evidence}\n"
              f"  -> verdict={r['verdict'].upper():13} scores={r['scores']}\n")


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        smoke()
    elif len(sys.argv) >= 3:
        print(json.dumps(verify_one(sys.argv[1], sys.argv[2]), indent=2))
    else:
        sys.exit("usage: python nli_verify.py --smoke | python nli_verify.py \"<claim>\" \"<evidence>\"")
