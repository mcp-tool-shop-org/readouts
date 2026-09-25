#!/usr/bin/env python3
"""Rebuild every KB's FTS index so its rowids match the base table's ids.

THE DEFECT THIS REPAIRS. Every loader built its FTS with an INSERT that omitted
`rowid`, so FTS5 assigned its own sequential rowids 1..N. That is only correct when
the base table's ids happen to be 1..N contiguous. Where they are not, the documented
access path — MATCH the index, then join the base row by rowid — breaks:

    blender      recipes.id 239..390  vs fts rowid 1..152  -> join returns 0 rows
    sprites      recipes.id 390..582  vs fts rowid 1..193  -> join returns 0 rows
    xrpl    capabilities.id 581..993  vs fts rowid 1..413  -> join returns 0 rows
    tensor-engine  8 deleted ids left the index SHIFTED    -> 85 of 171 rows joined
                                                              to the WRONG engine

The last one is the dangerous shape: not an empty result a caller might notice, but a
confident answer about a different record. Row counts matched (171 = 171) throughout,
so count parity was never a valid integrity signal.

The loaders are fixed, but re-ingesting every wave to pick that up would churn ids and
slugs across the whole corpus. Instead this lifts each loader's OWN FTS rebuild SQL out
of its source and re-executes it against the built DB. The authoritative statement stays
in one place — the loader — and this cannot drift from it.

    python shared/rebuild_fts.py --check    # report alignment, change nothing
    python shared/rebuild_fts.py            # repair, then verify
"""
from __future__ import annotations

import argparse
import glob
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DELETE_RE = re.compile(r'cur\.execute\(\s*"DELETE FROM (\w+_fts)"\s*\)')
INSERT_RE = re.compile(r'"""(INSERT INTO \w+_fts\(rowid,.*?)"""', re.S)


def kb_dirs() -> list[str]:
    return sorted(d for d in glob.glob(os.path.join(ROOT, "*-knowledge"))
                  if os.path.isfile(os.path.join(d, "scripts", "load_db.py")))


def pick_db(kb: str) -> str | None:
    best = None
    for p in sorted(glob.glob(os.path.join(kb, "*.db"))):
        if os.path.getsize(p) and (best is None or os.path.getsize(p) > os.path.getsize(best)):
            best = p
    return best


def alignment(db: str) -> tuple[str, str, int, int, int] | None:
    """(base, fts, base_rows, joined, mismatched) — or None if the KB has no FTS."""
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    con.text_factory = lambda b: b.decode("utf-8", "replace")
    tabs = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    fts = next((t for t in sorted(tabs) if t.endswith("_fts")), None)
    if not fts or fts[:-4] not in tabs:
        con.close()
        return None
    base = fts[:-4]
    n = con.execute(f"SELECT COUNT(*) FROM {base}").fetchone()[0]
    joined = con.execute(
        f"SELECT COUNT(*) FROM {fts} x JOIN {base} e ON e.id = x.rowid").fetchone()[0]
    try:
        wrong = con.execute(
            f"SELECT COUNT(*) FROM {fts} x JOIN {base} e ON e.id = x.rowid "
            f"WHERE x.slug IS NOT e.slug").fetchone()[0]
    except sqlite3.OperationalError:
        wrong = 0
    con.close()
    return base, fts, n, joined, wrong


def rebuild(kb: str, db: str) -> str:
    """Re-execute the loader's own DELETE + INSERT for its FTS table."""
    src = open(os.path.join(kb, "scripts", "load_db.py"), encoding="utf-8").read()
    dm, im = DELETE_RE.search(src), INSERT_RE.search(src)
    if not dm or not im:
        return "loader FTS statements not found — not rebuilt"
    con = sqlite3.connect(db)
    con.execute(f"DELETE FROM {dm.group(1)}")
    con.execute(im.group(1))
    con.commit()
    con.close()
    return "rebuilt"


def report(rows) -> int:
    bad = 0
    print(f"{'knowledge base':<28}{'rows':>6}{'joined':>8}{'wrong':>7}   state")
    print("-" * 68)
    for name, n, joined, wrong in rows:
        if joined == n and wrong == 0:
            state = "aligned"
        elif joined == 0:
            state = "BROKEN — join returns nothing"
            bad += 1
        elif wrong:
            state = f"BROKEN — {wrong} rows resolve to the wrong record"
            bad += 1
        else:
            state = f"BROKEN — {n - joined} rows unjoinable"
            bad += 1
        print(f"{name:<28}{n:>6}{joined:>8}{wrong:>7}   {state}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report only; change nothing")
    args = ap.parse_args()

    targets = []
    for kb in kb_dirs():
        db = pick_db(kb)
        if not db:
            continue
        a = alignment(db)
        if a:
            targets.append((kb, db, a))

    before = [(os.path.basename(kb), a[2], a[3], a[4]) for kb, _, a in targets]
    print("BEFORE\n")
    bad = report(before)

    if args.check:
        print(f"\n{bad} KB(s) with a broken index." if bad else "\nAll indexes aligned.")
        return 1 if bad else 0
    if not bad:
        print("\nNothing to repair.")
        return 0

    print("\nREBUILDING\n")
    for kb, db, a in targets:
        if a[3] == a[2] and a[4] == 0:
            continue
        print(f"  {os.path.basename(kb):<28} {rebuild(kb, db)}")

    after = []
    for kb, db, _ in targets:
        a = alignment(db)
        after.append((os.path.basename(kb), a[2], a[3], a[4]))
    print("\nAFTER\n")
    bad = report(after)
    if bad:
        print(f"\n::error:: HALT — {bad} KB(s) still broken after rebuild")
        return 2
    print("\nAll indexes aligned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
