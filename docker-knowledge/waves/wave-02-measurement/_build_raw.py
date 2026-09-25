#!/usr/bin/env python3
"""One-off: transform the wave-02 study-swarm output into research-raw.json (loader shape).

Joins each finding's sources to their retrieval-oracle verdict (existence/attribution/
groundedness), folds in the family-different (mistral+granite) correction notes, derives a
per-finding verify verdict, groups findings by lane. NOT committed (reads an ephemeral
session-temp path); research-raw.json is the durable artifact.
"""
import json
import os
import re

SRC = r"C:\Users\<user>\AppData\Local\Temp\claude\E--AI-gpu-container\3c8b5617-653d-47d6-be9d-1f0e3470cfe0\tasks\w566gc1l0.output"
OUT = r"docker-knowledge/waves/wave-02-measurement/research-raw.json"

d = json.load(open(SRC, encoding="utf-8"))["result"]
research, oracle = d["research"], d["oracle"]
orc = {o["identifier"]: o for o in oracle}

# family-different (granite) correction folded in by source identifier substring
SRC_NOTES = {
    "techpowerup.com/review/nvidia-geforce-rtx-5090-pci-express-scaling":
        "Family lens (granite) flag: '64 GB/s' is PER-DIRECTION (~63) for PCIe 5.0 x16; ~128 GB/s aggregate. "
        "Achieved pinned ~50-55 GB/s/dir. The profiler must treat 64 as per-direction theoretical, never a measured value.",
}

LANE_NAME = {"hw-measurement": "Hardware measurement methodology", "container-runtime": "Container & runtime layer"}


def slugify(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


lanes = {}
for r in research:
    lane = r.get("lane") or "hw-measurement"
    L = lanes.setdefault(lane, {"findings": [], "verdicts": []})
    for f in (r.get("findings") or []):
        srcs, any_supported, any_fix, any_ns = [], False, False, False
        for s in (f.get("sources") or []):
            ident = s.get("identifier", "")
            o = orc.get(ident, {})
            ex, am, sc = o.get("exists"), o.get("attribution_match"), o.get("supports_claim")
            if sc in ("SUPPORTED", "PARTIAL"):
                any_supported = True
            if sc == "NOT_SUPPORTED":
                any_ns = True
            if am == "MISMATCH" or sc in ("PARTIAL", "NOT_SUPPORTED", "CANT_TELL"):
                any_fix = True
            vbits = []
            if o.get("notes"):
                vbits.append(o["notes"][:300])
            for key, note in SRC_NOTES.items():
                if key in ident:
                    vbits.append(note)
            srcs.append({
                "kind": s.get("kind"), "title": s.get("title"), "authors": s.get("authors"),
                "year": s.get("year"), "identifier": ident, "url": s.get("url"),
                "claim": s.get("claim"), "quant": s.get("quant"),
                "exists_verified": 1 if ex == "YES" else 0,
                "finding_supported": sc, "verifier_note": " | ".join(vbits) or None,
            })
        L["findings"].append({
            "name": f.get("name"), "slug": slugify(f.get("slug") or f.get("name")),
            "kind": f.get("kind"), "claim": f.get("claim"), "detail": f.get("detail"),
            "applies_to": f.get("applies_to"), "design_implication": f.get("design_implication"),
            "metric": f.get("metric"), "confidence": f.get("confidence"),
            "rig_relevance": f.get("rig_relevance"), "status": f.get("status"), "sources": srcs,
        })
        overall = "thin" if not any_supported else ("confirmed-with-fixes" if any_fix else "confirmed")
        note = ("a source NOT_SUPPORTED (flagged); " if any_ns else "") + "oracle retrieval + family-different (mistral + granite)"
        L["verdicts"].append({"name": f.get("name"), "overall": overall, "note": note})

out = {
    "date": "2026-06-04", "wave": 2,
    "title": "Container & measurement — measuring truth inside a WSL2 GPU container",
    "domain_scope": "hw-measurement (PCIe / NVMe / VRAM / pinnable-RAM) + container-runtime gotchas, for the Milestone-1 profiler",
    "agent_count": 11,
    "verifier_note": (
        "3-lens, reasoning-stripped: WebFetch retrieval oracle (existence + attribution + content-groundedness; "
        "41/41 resolved, 0 fabricated) + mistral-small:24b + granite4.1:30b family-different groundedness. Ollama was "
        "briefly down and was RESTARTED before the family pass (ANDON: held, never skipped). granite caught a PCIe "
        "per-direction-vs-bidirectional terminology imprecision (#6, folded in); mistral was an over-skeptic (priors-"
        "not-knowledge S=N on oracle-confirmed forum/doc facts, discarded). 1 oracle NOT_SUPPORTED source flagged; "
        "7 attribution fixes (mostly 2025->2026 issue-year drift); 9 PARTIAL."
    ),
    "notes": "docker-knowledge wave 2 — fills the hw-measurement lane + container-runtime measurement gotchas. The design_implications are the spec for the profiler's measure_bandwidth() + platform detection.",
    "lanes": [
        {"slug": slug, "name": LANE_NAME.get(slug, slug),
         "research": {"domain": LANE_NAME.get(slug, slug), "notes": "", "findings": v["findings"]},
         "verify": {"verdicts": v["verdicts"]}}
        for slug, v in lanes.items()
    ],
    "measurements": [],
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote", OUT)
print("lanes:", {s: len(v["findings"]) for s, v in lanes.items()})
print("total findings:", sum(len(v["findings"]) for v in lanes.values()))
print("verified:", sum(1 for v in lanes.values() for vd in v["verdicts"] if vd["overall"] in ("confirmed", "confirmed-with-fixes")))
print("thin/unverified:", [vd["name"] for v in lanes.values() for vd in v["verdicts"] if vd["overall"] == "thin"])
