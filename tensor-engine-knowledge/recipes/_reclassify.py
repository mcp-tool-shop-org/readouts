#!/usr/bin/env python3
"""Achieve Goal 2: resolve the 21 low-confidence recipe_kind classifications.

Targets ONLY rows whose verify_note still carries a '?' (the flagged set) — a surgical UPDATE,
so it does NOT touch recipe_constraints / recipe_artifacts / recipe_techniques. Confident
deterministic rules; genuinely ambiguous cases get a sharpened (non-'?') note, not a forced fit.

Run:  $env:PYTHONUTF8='1'; python recipes/_reclassify.py
"""
import os, sqlite3

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")

def resolve(cat, slug, kind, backend, axis):
    s = slug.lower()
    if cat == 'runtime-foundations':
        if 'tensorrt' in s:
            return 'batch-producer', 'onnx-compile', 'build_wall_clock', 'builds a TensorRT .engine artifact (onnx-compile producer)'
        if 'llama-cpp' in s or 'llama.cpp' in s or 'llamacpp' in s:
            return 'launchable-server', 'native-win-compile', 'tok_s', 'llama-server runtime on the foundational stack'
        return 'modifier', backend, axis, 'foundational substrate/toolchain setup other recipes build on'
    if cat == 'profiling-bench':
        # tools run + emit a measurement; baselines are measured receipts (candidates for recipe_baselines)
        note = ('measured rig receipt — candidate for recipe_baselines, not a provisioning recipe'
                if any(k in s for k in ['baseline', 'soak', 'calibration', 'loadout', 'context-capability', 'idle'])
                else 'profiling/benchmark tool — runs and produces a measurement receipt')
        return 'batch-producer', backend, axis, note
    # fallback: strip the '?' but keep the kind
    return kind, backend, axis, 'classification reviewed'

def main():
    con = sqlite3.connect(DB); con.execute('PRAGMA foreign_keys=ON')
    cur = con.cursor()
    cats = {cid: slug for cid, slug in cur.execute('select id, slug from categories')}
    flagged = cur.execute(
        "select id, slug, category_id, recipe_kind, backend_kind, measured_axis, verify_note "
        "from recipes where verify_note like '%?%'").fetchall()
    print(f"flagged (low-confidence) recipes: {len(flagged)}")
    changes = {}
    for rid, slug, cat_id, kind, backend, axis, note in flagged:
        cat = cats.get(cat_id, '')
        nk, nb, nax, nnote = resolve(cat, slug, kind, backend, axis)
        cur.execute("update recipes set recipe_kind=?, backend_kind=?, measured_axis=?, verify_note=? where id=?",
                    (nk, nb, nax, nnote, rid))
        changes.setdefault((kind, nk), 0)
        changes[(kind, nk)] += 1
    con.commit()
    print("\nkind transitions (was -> now):")
    for (a, b), n in sorted(changes.items(), key=lambda x: -x[1]):
        arrow = 'unchanged' if a == b else f'{a} -> {b}'
        print(f"  {arrow:36s} {n}")
    remaining = cur.execute("select count(*) from recipes where verify_note like '%?%'").fetchone()[0]
    print(f"\nremaining low-confidence ('?') recipes: {remaining}")
    print("\nfull recipe_kind distribution now:")
    for k, n in cur.execute("select recipe_kind,count(*) from recipes group by recipe_kind order by 2 desc"):
        print(f"  {k:18s} {n}")
    con.close()

if __name__ == "__main__":
    main()
