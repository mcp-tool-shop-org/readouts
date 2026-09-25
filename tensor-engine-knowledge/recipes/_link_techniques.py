#!/usr/bin/env python3
"""Generate the cross-KB reverse links: tensor-engine recipe -> training-knowledge technique.

training-knowledge.techniques.engine_recipe_ref is the SINGLE SOURCE OF TRUTH (the forward
pointer). This derives the REVERSE pointer into tensor-engine's recipe_techniques table so the
join is explicit + bidirectional. Idempotent: clears recipe_techniques, re-derives.

Also an integrity check: any engine_recipe_ref that doesn't resolve to a tensor-engine recipe
slug is reported (dangling pointers, e.g. after a rearrange).

Run:  $env:PYTHONUTF8='1'; python recipes/_link_techniques.py
"""
import os, re, sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINES_DB = os.path.join(os.path.dirname(HERE), "engines.db")
TRAINING_DB = os.path.join(os.path.dirname(os.path.dirname(HERE)), "training-knowledge", "training.db")

SLUG = re.compile(r'[a-z0-9][a-z0-9-]{6,}')   # plausible recipe slug shape

def parse_refs(ref):
    """A free-text engine_recipe_ref -> list of candidate tensor-engine recipe slugs.
    Handles 'slug @ version', '(primary; also: a, b, c)', and stray punctuation."""
    if not ref:
        return []
    # pull any '(primary ...: a, b, c)' extras
    extra = []
    m = re.search(r'\((?:primary[^:]*)?:?\s*also:\s*(.*?)\)', ref, re.I)
    if not m:
        m = re.search(r'\(primary[^:]*:\s*(.*?)\)', ref, re.I)
    main = ref
    if m:
        extra = re.split(r'[;,]', m.group(1))
        main = ref[:m.start()]
    cands = [main] + extra
    out = []
    for c in cands:
        c = c.split('@')[0].strip().strip('(),;. ')
        # if a candidate still holds extra words, keep the longest slug-shaped token
        toks = SLUG.findall(c)
        if c and SLUG.fullmatch(c):
            out.append(c)
        elif toks:
            out.append(max(toks, key=len))
    # dedup preserve order
    seen, res = set(), []
    for s in out:
        if s not in seen:
            seen.add(s); res.append(s)
    return res

def main():
    if not os.path.exists(TRAINING_DB):
        raise SystemExit(f"training.db not found at {TRAINING_DB}")
    tk = sqlite3.connect(f"file:{TRAINING_DB}?mode=ro", uri=True)
    cats = {cid: slug for cid, slug in tk.execute("select id, slug from categories")}
    techs = tk.execute(
        "select slug, name, category_id, engine_recipe_ref from techniques "
        "where engine_recipe_ref is not null and engine_recipe_ref <> ''").fetchall()
    tk.close()

    con = sqlite3.connect(ENGINES_DB); con.execute("PRAGMA foreign_keys=ON")
    cur = con.cursor()
    recipe_ids = {slug: rid for rid, slug in cur.execute("select id, slug from recipes")}
    cur.execute("DELETE FROM recipe_techniques")

    linked = 0
    matched_techs = set()
    unmatched = []   # (technique_slug, candidate_slug)
    for tslug, tname, tcat_id, ref in techs:
        tcat = cats.get(tcat_id, "")
        cands = parse_refs(ref)
        any_match = False
        for cand in cands:
            rid = recipe_ids.get(cand)
            if rid:
                cur.execute(
                    "INSERT INTO recipe_techniques(recipe_id,kb,technique_slug,technique_name,technique_cat,note) "
                    "VALUES(?,?,?,?,?,?)",
                    (rid, "training-knowledge", tslug, tname, tcat, "derived from techniques.engine_recipe_ref"))
                linked += 1; any_match = True; matched_techs.add(tslug)
            else:
                unmatched.append((tslug, cand))
        if not cands:
            unmatched.append((tslug, "(unparseable ref)"))
    con.commit()

    # report
    print(f"techniques with engine_recipe_ref : {len(techs)}")
    print(f"reverse links written             : {linked}")
    print(f"techniques matched >=1 recipe      : {len(matched_techs)} / {len(techs)}")
    print(f"recipes now carrying technique(s)  : {cur.execute('select count(distinct recipe_id) from recipe_techniques').fetchone()[0]}")
    if unmatched:
        print(f"\nDANGLING refs (engine_recipe_ref -> no tensor-engine recipe slug): {len(unmatched)}")
        for ts, cand in unmatched[:25]:
            print(f"  {ts[:36]:36s} -> {cand}")
    # bidirectional spot-check
    print("\n--- bidirectional spot-check (recipe -> techniques) ---")
    for rslug, tname, tcat in cur.execute(
        "select r.slug, rt.technique_name, rt.technique_cat from recipe_techniques rt "
        "join recipes r on r.id=rt.recipe_id order by r.slug limit 8"):
        print(f"  {rslug[:46]:46s} <- {tcat:20s} {tname}")
    con.close()

if __name__ == "__main__":
    main()
