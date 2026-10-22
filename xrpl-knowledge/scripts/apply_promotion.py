#!/usr/bin/env python3
"""Apply a PROMOTION wave: append verified gotchas to EXISTING capability rows, and (optionally)
insert NEW capability rows from `new_capabilities[]` (wave 12 onward; no verifier, verified=0).

load_db.py only inserts new rows per wave. A promotion from rnd usually refines rows the KB
already holds, so this script reads waves/wave-NN/research-raw.json's `updates[]`, inserts the
waves row, appends each `gotcha_append` to the named capability's `gotchas` (existing text kept),
stamps `verify_note`, adds the wave's sources, and rebuilds FTS. Idempotent: a gotcha already
present is not appended twice, and the wave's sources are replaced.
Network: none. No verifier is called (Standing Rule 1: no cloud seat).
Usage: PYTHONUTF8=1 python scripts/apply_promotion.py waves/wave-NN/research-raw.json ; then scripts/regen.py
"""
import json
import os
import sqlite3
import sys

from load_db import norm_chain, norm_network, priority
from refresh_meta import set_meta_currency

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "xrpl.db")


def main(path):
    data = json.load(open(path, encoding="utf-8"))
    n, date = int(data["wave"]), data["date"]
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    cur = con.cursor()
    r = cur.execute("SELECT id FROM waves WHERE wave_number=?", (n,)).fetchone()
    if r:
        wid = r[0]
        cur.execute("UPDATE waves SET title=?,dispatched_date=?,domain_scope=?,agent_count=?,verifier_note=?,dispatch_path=? WHERE id=?",
                    (data["title"], date, data["domain_scope"], data["agent_count"], data["verifier_note"], data["dispatch_path"], wid))
        cur.execute("DELETE FROM sources WHERE wave_id=?", (wid,))
    else:
        cur.execute("INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path) VALUES(?,?,?,?,?,?,?,?)",
                    (n, data["title"], date, data["domain_scope"], data["agent_count"], data["verifier_note"], "synthesized", data["dispatch_path"]))
        wid = cur.lastrowid
    for u in data.get("updates", []):
        row = cur.execute("SELECT id,gotchas,verify_note FROM capabilities WHERE slug=?", (u["slug"],)).fetchone()
        if not row:
            sys.exit(f"no capability row with slug {u['slug']}")
        cid, got, vn = row
        add = u["gotcha_append"]
        if add not in (got or ""):
            got = ((got or "").rstrip() + " " + add).strip()
        tag = f"wave {n}: {u['verify_note']}"
        if tag not in (vn or ""):
            vn = ((vn + " | ") if vn else "") + tag
        cur.execute("UPDATE capabilities SET gotchas=?, verify_note=? WHERE id=?", (got, vn, cid))
        for s in u["sources"]:
            cur.execute("INSERT INTO sources(capability_id,kind,title,url,claim,retrieved_date,verified,wave_id) VALUES(?,?,?,?,?,?,?,?)",
                        (cid, s["kind"], s["title"], s["url"], s["claim"], date, None, wid))
    for m in data.get("new_capabilities", []):
        cat = cur.execute("SELECT id FROM categories WHERE slug=?", (m["category"],)).fetchone()
        if not cat:
            sys.exit(f"no category {m['category']}")
        vals = (m["name"], cat[0], m["kind"], norm_network(m["network_status"]), norm_chain(m.get("chain")),
                m.get("xls_standard"), m.get("amendment_name"), m.get("enabled_date"), m["maturity_tier"], m["status"],
                m["builder_fit"], m.get("commercial_use"), m["summary"], m["key_fields"], m["gotchas"],
                priority(m["status"], m["maturity_tier"]), 0, m["verify_note"], wid, date)
        row = cur.execute("SELECT id,wave_id FROM capabilities WHERE slug=?", (m["slug"],)).fetchone()
        if row and row[1] != wid:
            sys.exit(f"slug {m['slug']} already belongs to another wave; list it under updates[] instead")
        if row:
            cid = row[0]
            cur.execute("""UPDATE capabilities SET name=?,category_id=?,kind=?,network_status=?,chain=?,xls_standard=?,amendment_name=?,
                enabled_date=?,maturity_tier=?,status=?,builder_fit=?,commercial_use=?,summary=?,key_fields=?,gotchas=?,
                download_priority=?,verified=?,verify_note=?,wave_id=?,created_date=? WHERE id=?""", vals + (cid,))
        else:
            cur.execute("""INSERT INTO capabilities(name,category_id,kind,network_status,chain,xls_standard,amendment_name,
                enabled_date,maturity_tier,status,builder_fit,commercial_use,summary,key_fields,gotchas,
                download_priority,verified,verify_note,wave_id,created_date,slug) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                vals + (m["slug"],))
            cid = cur.lastrowid
        cur.execute("DELETE FROM capability_purposes WHERE capability_id=?", (cid,))
        for tr in m.get("tracks", []):
            pr = cur.execute("SELECT id FROM purposes WHERE slug=?", (f"track-{tr}",)).fetchone()
            if not pr:
                sys.exit(f"no track purpose track-{tr}")
            cur.execute("INSERT INTO capability_purposes(capability_id,purpose_id,fitness) VALUES(?,?,?)", (cid, pr[0], m["builder_fit"]))
        for s in m["sources"]:
            cur.execute("INSERT INTO sources(capability_id,kind,title,url,claim,retrieved_date,verified,wave_id) VALUES(?,?,?,?,?,?,?,?)",
                        (cid, s["kind"], s["title"], s["url"], s["claim"], date, None, wid))
    cur.execute("DELETE FROM capabilities_fts")
    cur.execute("""INSERT INTO capabilities_fts(rowid,slug,name,kind,summary,network_status,xls_standard,category)
        SELECT cap.id,cap.slug,cap.name,COALESCE(cap.kind,''),COALESCE(cap.summary,''),COALESCE(cap.network_status,''),
               COALESCE(cap.xls_standard,''),COALESCE((SELECT name FROM categories c WHERE c.id=cap.category_id),'')
        FROM capabilities cap""")
    set_meta_currency(cur)
    con.commit()
    nsrc = cur.execute("select count(*) from sources where wave_id=?", (wid,)).fetchone()[0]
    print(f"wave {n}: {len(data.get('updates', []))} rows updated, {len(data.get('new_capabilities', []))} rows added, {nsrc} sources")
    con.close()


if __name__ == "__main__":
    main(sys.argv[1])
