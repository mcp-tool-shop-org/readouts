#!/usr/bin/env python3
"""Ingest a study-swarm wave's research-raw.json into docker-knowledge/findings.db.

Idempotent per wave: deletes existing rows for the wave_number before inserting,
so re-running a wave (after a re-dispatch) cleanly replaces it.

Usage:
    python load_db.py [path/to/research-raw.json]
Default: ../waves/wave-01-feasibility/research-raw.json

Run with UTF-8 forced on Windows (entries carry em-dashes):
    $env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'; python load_db.py ...
"""
import json
import os
import re
import sqlite3
import sys

from refresh_meta import set_meta_currency  # currency pointer is derived from the DB, never the ingest wave

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "findings.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

WAVE_TITLES = {
    1: "Feasibility — research-grounded study-swarm verdict (seeded from wf_965f110f-e24)",
    2: "Container & measurement — measuring truth inside a WSL2 GPU container",
}


def slugify(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def uniq_slug(cur, table, base):
    s, k = base, 2
    while cur.execute(f"SELECT 1 FROM {table} WHERE slug=?", (s,)).fetchone():
        s, k = f"{base}-{k}", k + 1
    return s


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # tolerate the harness envelope: payload may be at .result
    if "lanes" not in data and isinstance(data.get("result"), dict):
        data = data["result"]
    wave_no = int(data.get("wave", 1))
    date = data.get("date", "")
    lanes = data.get("lanes", [])

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    with open(SCHEMA, "r", encoding="utf-8") as f:
        con.executescript(f.read())
    cur = con.cursor()

    row = cur.execute("SELECT id FROM waves WHERE wave_number=?", (wave_no,)).fetchone()
    if row:
        wave_id = row[0]
        # findings cascade-delete their finding_sources; clear measurements too
        cur.execute("DELETE FROM finding_sources WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM findings WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM measurements WHERE wave_id=?", (wave_id,))
        cur.execute("UPDATE waves SET dispatched_date=?, status='synthesized' WHERE id=?", (date, wave_id))
    else:
        cur.execute(
            """INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
               VALUES(?,?,?,?,?,?,?,?,?)""",
            (wave_no, data.get("title") or WAVE_TITLES.get(wave_no, f"Wave {wave_no}"), date,
             data.get("domain_scope"), data.get("agent_count"), data.get("verifier_note"),
             "synthesized",
             f"waves/{os.path.basename(os.path.dirname(os.path.abspath(path)))}/dispatch.md",
             data.get("notes")))
        wave_id = cur.lastrowid

    cat = {s: i for s, i in cur.execute("SELECT slug,id FROM categories")}

    n_find = n_src = n_meas = 0
    for lane in lanes:
        lslug = lane.get("slug")
        category_id = cat.get(lslug)
        if category_id is None and lslug:  # safety net for a brand-new lane slug
            cur.execute("INSERT OR IGNORE INTO categories(slug,name,description,sort) VALUES(?,?,?,?)",
                        (lslug, lslug.replace("-", " ").title(), "auto-created from wave lane", 99))
            category_id = cur.execute("SELECT id FROM categories WHERE slug=?", (lslug,)).fetchone()[0]
            cat[lslug] = category_id
        research = lane.get("research") or {}
        verify = lane.get("verify") or {}
        verdicts = {(v.get("name") or "").strip().lower(): v for v in (verify.get("verdicts") or [])}

        for fnd in (research.get("findings") or []):
            name = fnd.get("name")
            fslug = uniq_slug(cur, "findings", slugify(fnd.get("slug") or name))
            v = verdicts.get((name or "").strip().lower(), {})
            overall = (v.get("overall") or "").strip().lower()
            if overall:
                verified = 1 if overall in ("confirmed", "confirmed-with-fixes", "supported") else 0
            else:
                verified = 1 if fnd.get("verified") else 0
            vparts = []
            if overall:
                vparts.append(f"verdict={overall}")
            if v.get("note"):
                vparts.append(v["note"])
            vnote = " | ".join(vparts) or fnd.get("verify_note")

            cur.execute(
                """INSERT INTO findings(slug,name,category_id,kind,claim,detail,applies_to,design_implication,
                   metric,confidence,rig_relevance,status,verified,verify_note,wave_id,created_date)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (fslug, name, category_id, fnd.get("kind"), fnd.get("claim"), fnd.get("detail"),
                 fnd.get("applies_to"), fnd.get("design_implication"), fnd.get("metric"),
                 fnd.get("confidence"), fnd.get("rig_relevance"), fnd.get("status"),
                 verified, vnote, wave_id, date))
            finding_id = cur.lastrowid
            n_find += 1

            for s in (fnd.get("sources") or []):
                if not s.get("url"):
                    continue
                cur.execute(
                    """INSERT INTO finding_sources(finding_id,kind,title,authors,year,identifier,url,claim,quant,
                       retrieved_date,exists_verified,finding_supported,verifier_note,wave_id)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (finding_id, s.get("kind"), s.get("title"), s.get("authors"), s.get("year"),
                     s.get("identifier"), s.get("url"), s.get("claim"), s.get("quant"), date,
                     1 if s.get("exists_verified") else 0, s.get("finding_supported"),
                     s.get("verifier_note"), wave_id))
                n_src += 1

    # measurements (top-level array); the Milestone-1 profiler's baselines also land here
    for m in (data.get("measurements") or []):
        cur.execute(
            """INSERT INTO measurements(metric,value,unit,context,tool,source_file,note,wave_id,measured_date)
               VALUES(?,?,?,?,?,?,?,?,?)""",
            (m.get("metric"), m.get("value"), m.get("unit"), m.get("context"), m.get("tool"),
             m.get("source_file"), m.get("note"), wave_id, m.get("measured_date") or date))
        n_meas += 1

    cur.execute("DELETE FROM findings_fts")
    cur.execute(
        """INSERT INTO findings_fts(rowid,slug,name,claim,detail,applies_to,design_implication,category)
           SELECT f.id, f.slug, f.name, COALESCE(f.claim,''), COALESCE(f.detail,''),
                  COALESCE(f.applies_to,''), COALESCE(f.design_implication,''),
                  COALESCE((SELECT name FROM categories c WHERE c.id=f.category_id),'')
           FROM findings f""")

    # Static identity keys. The currency pointer (latest_wave/updated) is NOT set
    # from this wave — set_meta_currency derives it from MAX(waves.wave_number) so
    # re-ingesting an old wave, or appending waves via one-off scripts, can never
    # make meta lie about how current the KB is (the gpu-container write-back
    # depends on this pointer telling the truth).
    meta = {
        "kb_name": "docker-knowledge",
        "rig": "OMEN 45L · RTX 5090 · Blackwell sm_120 · 32 GB VRAM · Core Ultra 9 · 64 GB RAM · Windows 11 / WSL2",
        "scope": "Honest inference memory placement + container/runtime measurement. Backs the gpu-container product. "
                 "Siblings: model-knowledge (models), tensor-engine-knowledge (engines).",
    }
    for k, vv in meta.items():
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (k, vv))
    set_meta_currency(cur)  # latest_wave = MAX(wave_number), updated = that wave's date

    con.commit()
    print(f"wave {wave_no}: {n_find} findings, {n_src} sources, {n_meas} measurements.")
    for r in cur.execute(
        """SELECT c.name, COUNT(*), COALESCE(SUM(f.verified),0)
           FROM findings f JOIN categories c ON c.id=f.category_id
           WHERE f.wave_id=? GROUP BY c.name ORDER BY c.sort""", (wave_id,)):
        print(f"  {r[0]:34s} {r[1]:2d} findings  ({r[2]} verified)")
    con.close()


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-feasibility", "research-raw.json")
    main(p)
