#!/usr/bin/env python3
"""Deterministic constraint + artifact extraction from recipe prose bodies.

High-precision / abstain-on-doubt: only emits a constraint or artifact when the body
states it unambiguously. Fills recipe_constraints + recipe_artifacts for the 160 backfilled
recipes. Idempotent: clears both tables, re-derives. Nuanced enrichment (summaries, fuzzy
constraints) is a later ollama-intern pass; this nails the structured signals.

Run:  $env:PYTHONUTF8='1'; python recipes/_extract_fields.py
"""
import os, re, sqlite3

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")

def constraints_for(t):
    """t = lower(name+' '+body). Returns list of (ctype, expr, reason)."""
    out = []
    if re.search(r'cuda[\s\-]*12\.8|cu128', t):
        out.append(('requires_when', 'cuda_toolkit==12.8', 'body pins CUDA 12.8 / cu128'))
    if re.search(r'(13\.\d|cuda\s*13|13\.x)', t) and re.search(r'segfault|mmq|avoid|breaks|slower|do not|don.t|13\.x', t):
        out.append(('conflicts_when', 'cuda_toolkit>=13.0', 'body warns 13.x is wrong/slower on sm_120'))
    if re.search(r'cu130|cuda[\s\-]*13\.0', t) and re.search(r'pytorch|torch 2\.1[12]|use cu130|requires cu130', t):
        out.append(('requires_when', 'torch_cuda==cu130', 'PyTorch path pins cu130'))
    if re.search(r'sm_?120|blackwell', t):
        out.append(('capability', 'gpu_arch>=sm_120', 'Blackwell / sm_120'))
    if re.search(r'wsl2?\s*2\.7|wddm', t) and re.search(r'hang|graph[\s\-]*capture|2\.7\.0|>=\s*2\.7', t):
        out.append(('defect_floor', 'wsl2>=2.7.0', 'WDDM graph-capture hang below 2.7.0'))
    if 'xformers' in t and re.search(r'never|don.t|avoid|no sm_120|downgrade', t):
        out.append(('conflicts_when', 'pkg==xformers', 'no sm_120 wheel; silently downgrades torch'))
    if re.search(r'flashattention[\s\-]*3|\bfa3\b', t) and re.search(r"cannot|can.t|sm_?120|tmem|physically", t):
        out.append(('defect_floor', 'fa_version<3 on sm_120', 'FA3 needs TMEM (sm_100); desktop Blackwell is sm_120'))
    if re.search(r'black output|hard[\s\-]*crash|crashes|importerror|dll', t):
        m = re.search(r'([^.]*?(?:black output|hard[\s\-]*crash|crashes|importerror|dll)[^.]*)', t)
        out.append(('conflicts_when', 'see-note', (m.group(1).strip()[:120] if m else 'known crash/conflict in body')))
    return out

URLRE = re.compile(r'https?://[^\s)>\]"\']+')
WHLRE = re.compile(r'[\w.\-]+\.whl')
DIGRE = re.compile(r'[\w./\-]+@sha256:[0-9a-f]{8,}')

def classify_url(u):
    ul = u.lower()
    if 'download.pytorch.org' in ul or 'pypi.org' in ul or 'wheels.vllm.ai' in ul:
        return 'wheel', 'index'
    if 'huggingface.co' in ul:
        return 'model-weights', 'index'
    if 'ghcr.io' in ul or 'docker' in ul:
        return 'docker-image', 'index'
    if 'github.com' in ul:
        return ('release-asset' if '/releases/' in ul else 'git-ref'), 'index'
    return 'git-ref', 'index'

def artifacts_for(body, url):
    out = []   # (kind, ref, sha256, store_expect, note)
    seen = set()
    def add(kind, ref, store, note, sha=None):
        key = ref.strip().rstrip('.,);')
        if key and key not in seen:
            seen.add(key); out.append((kind, key, sha, store, note))
    for dig in DIGRE.findall(body or ''):
        add('docker-image', dig, 'index', 'digest-pinned image (vendor to make reproducible)')
    for whl in WHLRE.findall(body or ''):
        add('wheel', whl, 'index', 'wheel filename in body (vendor to make reproducible)')
    for u in URLRE.findall(body or ''):
        k, st = classify_url(u); add(k, u, st, 'url in body')
    if url:
        k, st = classify_url(url); add(k, url, st, 'recipe url')
    return out

# wave-4 MEASURED env-facts that the prose body can't yield (campaign findings) — injected so they
# survive re-derivation. Keyed by recipe slug. Mirror of KB#4's lycoris-GC technique (cross-KB seam).
CAMPAIGN_FACTS = {
    "training-kohya-sdxl-lora-proven-blackwell-5090": [
        ("defect_floor", "lycoris.kohya requires --gradient_checkpointing",
         "without GC, DoRA/LoKr peak spills past 32 GB -> WDDM paging (~33 s/it); with GC ~14.5 GB / 1.06 s/it [wave-4 measured]"),
        ("requires_when", "dora/lokr via lycoris>=3.4.0",
         "this sd-scripts has no native DoRA; route network-type (DoRA/LoKr) through lycoris 3.4.0 [wave-4 measured]"),
    ],
}

def main():
    con = sqlite3.connect(DB); con.execute('PRAGMA foreign_keys=ON')
    cur = con.cursor()
    cur.execute('DELETE FROM recipe_constraints')
    cur.execute('DELETE FROM recipe_artifacts')
    # recipes carry body; original url lives on config_recipes (join by slug)
    rows = cur.execute("""select r.id, r.name, r.body, cr.url
                          from recipes r left join config_recipes cr on cr.slug=r.slug""").fetchall()
    nc = na = 0
    rc_recipes = ra_recipes = 0
    for rid, name, body, url in rows:
        t = (name + ' ' + (body or '')).lower()
        cons = constraints_for(t)
        for ctype, expr, reason in cons:
            cur.execute("INSERT INTO recipe_constraints(recipe_id,ctype,expr,reason) VALUES(?,?,?,?)",
                        (rid, ctype, expr, reason)); nc += 1
        if cons: rc_recipes += 1
        arts = artifacts_for(body, url)
        for kind, ref, sha, store, note in arts:
            cur.execute("""INSERT INTO recipe_artifacts(recipe_id,kind,ref,sha256,store_expect,note)
                           VALUES(?,?,?,?,?,?)""", (rid, kind, ref, sha, store, note)); na += 1
        if arts: ra_recipes += 1
    # inject wave-4 measured env-facts (cross-KB mirror of KB#4's lycoris-GC technique on the same recipe)
    nf = 0
    for slug, facts in CAMPAIGN_FACTS.items():
        row = cur.execute("select id from recipes where slug=?", (slug,)).fetchone()
        if not row:
            print(f"  CAMPAIGN_FACTS: slug not found -> {slug}"); continue
        for ctype, expr, reason in facts:
            cur.execute("INSERT INTO recipe_constraints(recipe_id,ctype,expr,reason) VALUES(?,?,?,?)",
                        (row[0], ctype, expr, reason)); nf += 1
    nc += nf
    con.commit()
    print(f"injected {nf} wave-4 measured env-facts as constraints")
    print(f"constraints: {nc} across {rc_recipes}/160 recipes")
    print(f"artifacts  : {na} across {ra_recipes}/160 recipes")
    print("\nconstraint type distribution:")
    for ctype, n in cur.execute("select ctype,count(*) from recipe_constraints group by ctype order by 2 desc"):
        print(f"  {ctype:16s} {n}")
    print("\nartifact kind distribution:")
    for kind, n in cur.execute("select kind,count(*) from recipe_artifacts group by kind order by 2 desc"):
        print(f"  {kind:16s} {n}")
    print("\nstore_expect (reproducibility) distribution:")
    for st, n in cur.execute("select store_expect,count(*) from recipe_artifacts group by store_expect order by 2 desc"):
        print(f"  {st:16s} {n}  <- all 'index' until vendored")
    print("\nsample (llama.cpp-ish recipe constraints):")
    for slug, ctype, expr in cur.execute("""select r.slug, c.ctype, c.expr from recipe_constraints c
        join recipes r on r.id=c.recipe_id where r.slug like '%llama%cpp%' limit 8"""):
        print(f"  {slug[:46]:46s} {ctype:14s} {expr}")
    con.close()

if __name__ == "__main__":
    main()
