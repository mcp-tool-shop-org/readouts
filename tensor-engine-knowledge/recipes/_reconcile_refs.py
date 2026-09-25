#!/usr/bin/env python3
"""Triage the dangling engine_recipe_ref pointers from training-knowledge.

For each KB#4 engine_recipe_ref slug that does NOT resolve to a current tensor-engine
recipe, find the closest current recipe slug (difflib). High similarity => a RENAME
(repoint the ref); low => GENUINELY MISSING (the engine recipe was pruned / never added).
Read-only. Decision (repoint KB#4 refs vs re-add tensor-engine recipes) stays with Mike.

Run:  $env:PYTHONUTF8='1'; python recipes/_reconcile_refs.py
"""
import os, re, sqlite3, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINES_DB = os.path.join(os.path.dirname(HERE), "engines.db")
TRAINING_DB = os.path.join(os.path.dirname(os.path.dirname(HERE)), "training-knowledge", "training.db")
SLUG = re.compile(r'[a-z0-9][a-z0-9-]{6,}')

def parse_refs(ref):
    if not ref:
        return []
    extra = []
    m = re.search(r'\((?:primary[^:]*)?:?\s*also:\s*(.*?)\)', ref, re.I) or re.search(r'\(primary[^:]*:\s*(.*?)\)', ref, re.I)
    main = ref
    if m:
        extra = re.split(r'[;,]', m.group(1)); main = ref[:m.start()]
    out = []
    for c in [main] + extra:
        c = c.split('@')[0].strip().strip('(),;. ')
        if c and SLUG.fullmatch(c): out.append(c)
        else:
            toks = SLUG.findall(c)
            if toks: out.append(max(toks, key=len))
    seen, res = set(), []
    for s in out:
        if s not in seen: seen.add(s); res.append(s)
    return res

tk = sqlite3.connect(f"file:{TRAINING_DB}?mode=ro", uri=True)
techs = tk.execute("select slug, engine_recipe_ref from techniques where engine_recipe_ref is not null and engine_recipe_ref<>''").fetchall()
tk.close()
con = sqlite3.connect(f"file:{ENGINES_DB}?mode=ro", uri=True)
recipe_slugs = [s for (s,) in con.execute("select slug from recipes")]
con.close()
rset = set(recipe_slugs)

dangling = []
for tslug, ref in techs:
    for cand in parse_refs(ref):
        if cand not in rset:
            dangling.append((tslug, cand))

print(f"dangling refs: {len(dangling)}\n")
renames, missing = [], []
for tslug, cand in dangling:
    m = difflib.get_close_matches(cand, recipe_slugs, n=1, cutoff=0.0)
    best = m[0] if m else None
    score = difflib.SequenceMatcher(None, cand, best).ratio() if best else 0.0
    (renames if score >= 0.72 else missing).append((cand, best, score))

print(f"=== LIKELY RENAMES (repoint KB#4 ref -> current slug)  [{len(renames)}] ===")
for cand, best, score in sorted(renames, key=lambda x: -x[2]):
    print(f"  {score:.2f}  {cand}\n        -> {best}")
print(f"\n=== LIKELY MISSING (engine recipe pruned / never added)  [{len(missing)}] ===")
for cand, best, score in sorted(missing, key=lambda x: -x[2]):
    print(f"  {score:.2f}  {cand}\n        closest: {best}")
