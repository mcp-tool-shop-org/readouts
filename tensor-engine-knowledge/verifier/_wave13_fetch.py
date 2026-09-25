"""Wave-13: fetch real physical-sciences abstracts (a domain shift from AI/ML) into a SEPARATE cache,
so the multi-domain generality set is grounded in real, sha-pinned source text (never paraphrased)."""
import json, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("fa", os.path.join(HERE, "fetch_abstracts.py"))
fa = importlib.util.module_from_spec(spec); spec.loader.exec_module(fa)
IDS = [
    "1602.03837",  # LIGO — Observation of Gravitational Waves from a Binary Black Hole Merger (gr-qc)
    "1207.7214",   # ATLAS — Observation of a new particle ~125 GeV (Higgs) (hep-ex)
    "1207.7235",   # CMS — Observation of a new boson at 125 GeV (hep-ex)
    "1502.01589",  # Planck 2015 results XIII — cosmological parameters (astro-ph.CO)
    "1906.11238",  # Event Horizon Telescope — First M87 image, paper I (astro-ph.GA)
]
data = fa.fetch(IDS)
out = os.path.join(HERE, "abstracts-cache-multidomain.json")
json.dump(data, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"fetched {len(data)}/{len(IDS)} -> {out}")
for i, d in data.items():
    print(f"\n[{i}] {d['title']}\n{d['abstract']}")
