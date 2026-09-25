#!/usr/bin/env python3
"""Ingest vocology-knowledge research-raw.json into findings.db.

research-raw.json shape:
{
  "wave": <int>, "date": "YYYY-MM-DD", "title": "...", "domain_scope": "...",
  "agent_count": <int>, "verifier_note": "...",
  "lanes": [{
    "laneSlug": "<categories.slug>", "title": "...",
    "findings": [{
      n, authors, year, title, id, url, finding, implication
    }]
  }]
}

Verified=1 only for identifiers listed as abstract-supported accept in
waves/wave-01-foundation/verification.md (nine accepts). Default unverified.

Idempotent per wave_number. UTF-8 required on Windows.
"""
import json
import os
import re
import sqlite3
import sys

from refresh_meta import set_meta_currency

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "findings.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

# Abstract-supported accepts from wave-01 verification.md — do not invent extras.
ACCEPT_IDS = {
    "10.1121/1.1914609",   # Sundberg 1974
    "10.1121/1.1791717",   # Joliveau 2004
    "10.1121/1.2832337",   # Titze 2008
    "10.1121/1.410141",    # Prame 1994
    "10.1121/1.398894",    # Klatt 1990
    "2110.08813",          # VISinger 2022
    "2106.10045",          # Zhang & Zhu 2021
    "2510.01812",          # SingMOS-Pro 2026
    "10.2307/3345186",     # Green 1990
}


def slugify(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def uniq_slug(cur, base):
    s, k = base, 2
    while cur.execute("SELECT 1 FROM findings WHERE slug=?", (s,)).fetchone():
        s, k = f"{base}-{k}", k + 1
    return s


def load_verdicts():
    """The retrieval sweep's durable verdicts, keyed by finding slug.

    Absent on a fresh checkout of a KB that has had no sweep; that is not an error,
    it just means every finding falls back to the ACCEPT_IDS default.
    """
    path = os.path.join(ROOT, "verification", "verdicts.json")
    if not os.path.isfile(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh).get("verdicts", {})


VERDICTS = load_verdicts()


def is_accept(identifier):
    ident = (identifier or "").strip()
    for needle in ACCEPT_IDS:
        if needle in ident:
            return True
    return False


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "lanes" not in data and isinstance(data.get("result"), dict):
        data = data["result"]
    wave_no = int(data.get("wave", 1))
    date = data.get("date", "")
    title = data.get("title") or f"Wave {wave_no}"
    lanes = data.get("lanes", [])

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    with open(SCHEMA, "r", encoding="utf-8") as f:
        con.executescript(f.read())
    cur = con.cursor()

    row = cur.execute("SELECT id FROM waves WHERE wave_number=?", (wave_no,)).fetchone()
    if row:
        wave_id = row[0]
        cur.execute("DELETE FROM finding_sources WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM findings WHERE wave_id=?", (wave_id,))
        cur.execute(
            "UPDATE waves SET title=?, dispatched_date=?, domain_scope=?, agent_count=?, "
            "verifier_note=?, status='synthesized' WHERE id=?",
            (title, date, data.get("domain_scope"), data.get("agent_count"),
             data.get("verifier_note"), wave_id))
    else:
        folder = os.path.basename(os.path.dirname(os.path.abspath(path)))
        cur.execute(
            """INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,agent_count,
               verifier_note,status,dispatch_path)
               VALUES(?,?,?,?,?,?,?,?)""",
            (wave_no, title, date, data.get("domain_scope"),
             data.get("agent_count") or len(lanes), data.get("verifier_note"),
             "synthesized", f"waves/{folder}/dispatch.md"))
        wave_id = cur.lastrowid

    cat = {s: i for s, i in cur.execute("SELECT slug,id FROM categories")}
    n_find = n_src = n_ver = 0

    for lane in lanes:
        lslug = lane.get("laneSlug") or lane.get("slug")
        category_id = cat.get(lslug)
        if category_id is None and lslug:
            cur.execute(
                "INSERT OR IGNORE INTO categories(slug,name,description,sort) VALUES(?,?,?,?)",
                (lslug, lane.get("title") or lslug.replace("-", " ").title(),
                 "auto-created from wave lane", 99))
            category_id = cur.execute(
                "SELECT id FROM categories WHERE slug=?", (lslug,)).fetchone()[0]
            cat[lslug] = category_id

        for fnd in (lane.get("findings") or []):
            name = fnd.get("title") or f"finding-{fnd.get('n')}"
            base = slugify(f"{fnd.get('n')}-{name}")[:80]
            fslug = uniq_slug(cur, base)
            cid = fnd.get("id") or ""
            claim = fnd.get("finding")
            authors = fnd.get("authors")
            year = str(fnd.get("year") or "")

            # The verdict ledger (verification/verdicts.json) is the source of truth
            # for `verified`, written by a retrieval sweep and merged by
            # merge_verdicts.py. ACCEPT_IDS remains only as the wave-01 fallback for
            # findings no sweep has reached yet. Without the ledger a sweep would be
            # undone by the next reload, because the DB is derived, not authored.
            vd = VERDICTS.get(fslug)
            verdict_word = (vd or {}).get("verdict")
            evidence_url = (vd or {}).get("evidence_url")
            if vd:
                verified = int(vd["verified"])
                status = vd["status"]
                vnote = vd.get("verify_note") or vd["verdict"]
                corr = vd.get("corrections") or {}
                authors = corr.get("authors", authors)
                year = str(corr.get("year", year) or "")
                cid = corr.get("citation_id", cid)
                claim = corr.get("claim", claim)
            else:
                # No ledger entry means no sweep has reached this finding. That is
                # `directional`, never a pass. ACCEPT_IDS — nine citation ids matched
                # by SUBSTRING — was retired once the sweeps covered every finding.
                verified = 0
                vnote = "no external verdict — not yet swept"
                status = "directional"

            cur.execute(
                """INSERT INTO findings(slug,name,category_id,kind,claim,detail,design_implication,
                   citation_id,authors,year,status,verified,verify_note,wave_id,created_date)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (fslug, name, category_id, "paper", claim, None,
                 fnd.get("implication"), cid, authors,
                 year, status, verified, vnote, wave_id, date))
            finding_id = cur.lastrowid
            n_find += 1
            n_ver += verified

            url = fnd.get("url")
            if url:
                cur.execute(
                    """INSERT INTO finding_sources(finding_id,title,authors,year,identifier,url,claim,
                       exists_verified,finding_supported,verifier_note,wave_id)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                    (finding_id, fnd.get("title"), authors,
                     year, cid, url, claim,
                     # "retrieved" and "supported" are different facts. A refuted
                     # claim WAS reached and was NOT supported; writing 0/NULL made
                     # it indistinguishable from a source nobody could open.
                     1 if verdict_word in ("confirmed", "corrected", "refuted") else 0,
                     {"confirmed": "SUPPORTED", "corrected": "SUPPORTED",
                      "refuted": "NOT_SUPPORTED",
                      "unfindable": "CANT_TELL"}.get(verdict_word),
                     f"{vnote} [evidence: {evidence_url}]" if evidence_url else vnote,
                     wave_id))
                n_src += 1

    cur.execute("DELETE FROM findings_fts")
    cur.execute(
        """INSERT INTO findings_fts(rowid,slug,name,claim,detail,design_implication,category)
           SELECT f.id, f.slug, f.name, COALESCE(f.claim,''), COALESCE(f.detail,''),
                  COALESCE(f.design_implication,''),
                  COALESCE((SELECT name FROM categories c WHERE c.id=f.category_id),'')
           FROM findings f""")

    for k, vv in {
        "kb_name": "vocology-knowledge",
        "scope": "Sung-voice craft for score-lock SVS vs song generators; not a models table.",
        "noun": "findings",
        "decisive_axis": "score-lock",
    }.items():
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (k, vv))
    set_meta_currency(cur)

    con.commit()
    print(f"wave {wave_no}: {n_find} findings, {n_src} sources, {n_ver} verified.")
    for r in cur.execute(
        """SELECT c.name, COUNT(*), COALESCE(SUM(f.verified),0)
           FROM findings f JOIN categories c ON c.id=f.category_id
           WHERE f.wave_id=? GROUP BY c.name ORDER BY c.sort""", (wave_id,)):
        print(f"  {r[0]:40s} {r[1]:2d} findings  ({r[2]} verified)")
    con.close()


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        ROOT, "waves", "wave-01-foundation", "research-raw.json")
    if not os.path.exists(p):
        sys.exit(f"missing research-raw: {p}")
    main(p)
