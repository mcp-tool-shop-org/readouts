#!/usr/bin/env python3
"""Fetch real arXiv title+abstract for a list of IDs and cache them (PIN: content-hashed, replayable).

The cache is the EVIDENCE the wave-6 citation-panel eval judges claims against — we fetch the real
source so gold labels are defensible against the actual abstract, never paraphrased from memory.
One batched request (arXiv asks callers to batch + be gentle). stdlib only.
"""
import json, os, hashlib, sys, time, urllib.request, urllib.parse
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "abstracts-cache.json")

# Real arXiv papers role-os's citation gate actually cares about (its design-doc bibliography).
IDS = [
    "2402.01817",  # Kambhampati — LLMs Can't Plan / LLM-Modulo
    "2310.01798",  # Huang — Large Language Models Cannot Self-Correct Reasoning Yet
    "2402.08115",  # Stechly — On the Self-Verification Limitations of LLMs
    "2004.14974",  # Wadden — Fact or Fiction: Verifying Scientific Claims (SciFact)
    "2404.13076",  # Panickssery — LLM Evaluators Recognize and Favor Their Own Generations
    "2408.02442",  # Tam — Let Me Speak Freely? (format restrictions hurt)
    "2501.10868",  # Geng — JSONSchemaBench
    "2102.09692",  # Bucinca — To Trust or to Think (cognitive forcing)
]

ATOM = "{http://www.w3.org/2005/Atom}"

def fetch(ids):
    """Semantic Scholar batch (Tier-1 scholarly source) — title+abstract by arXiv id, one request.
    arXiv's own API hard-rate-limited this host; S2 is the resilient path. Papers S2 has no abstract
    for are dropped (we only label against a real, present source)."""
    url = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,abstract,externalIds"
    body = json.dumps({"ids": [f"arXiv:{i}" for i in ids]}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "tensor-engine-knowledge-verifier/1.0 (research; mcp-tool-shop)"})
    raw = None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                raw = json.loads(r.read())
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 4:
                wait = 3 * (attempt + 1)
                print(f"  {e.code} rate-limited; backing off {wait}s (attempt {attempt+1}/5)", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    if raw is None:
        raise RuntimeError("Semantic Scholar fetch failed after retries")
    out = {}
    for i, paper in zip(ids, raw):
        if not paper:
            continue
        abstract = " ".join((paper.get("abstract") or "").split())
        if not abstract:
            continue  # no source text -> cannot label against it; drop
        title = " ".join((paper.get("title") or "").split())
        out[i] = {
            "arxiv_id": i,
            "title": title,
            "abstract": abstract,
            "sha256": hashlib.sha256(abstract.encode("utf-8")).hexdigest(),
            "source": "semanticscholar",
            "query": f"{url} (arXiv:{i})",
        }
    return out

if __name__ == "__main__":
    data = fetch(IDS)
    json.dump(data, open(CACHE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    missing = [i for i in IDS if i not in data]
    print(f"fetched {len(data)}/{len(IDS)} -> {CACHE}")
    if missing:
        print(f"MISSING (dropped): {missing}")
    for i, d in data.items():
        print(f"\n[{i}] {d['title']}")
        print(f"  {d['abstract'][:320]}{'...' if len(d['abstract'])>320 else ''}")
