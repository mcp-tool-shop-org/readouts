#!/usr/bin/env python3
"""Ingest a study-swarm wave's research-raw.json into xrpl-knowledge/xrpl.db.

Idempotent per wave: deletes the wave's rows before inserting, so a re-dispatch (or a re-run
of verify_cloud.py) cleanly replaces it.

The wave json carries up to three signals per capability:
  research.capabilities[]      — the Claude web-grounded researcher's claims + sources
  verify.verdicts[]            — seat 1: Claude+WebFetch retrieval oracle (does the live doc exist/say it)
  cloud_verify.verdicts[]      — seat 2: a cross-family Ollama Cloud large model (AUTHORITATIVE for `verified`)

`capabilities.verified` is set by the CROSS-FAMILY cloud seat (no Claude-judges-Claude). `sources.verified`
(does it resolve) is set by the retrieval oracle. When the cloud seat is missing for an item, verified=0 and
verify_note flags "cross-family seat: pending" — re-run scripts/verify_cloud.py then re-ingest to flip it.

Usage:  $env:PYTHONUTF8='1'; python scripts/load_db.py [waves/wave-NN/research-raw.json]
"""
import json
import os
import re
import sqlite3
import sys

from refresh_meta import set_meta_currency

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "xrpl.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

WAVE_TITLES = {1: "Foundation — the XRPL ecosystem, with current mainnet/amendment status"}
STATUS_RANK = {"recommended": 0, "situational": 3, "legacy": 7, "avoid": 9}
MATURITY_RANK = {"stable": 0, "new": 1, "experimental": 3, "deprecated": 7}
CONFIRMED = ("confirmed", "confirmed-with-fixes")


def txt(v):
    """Coerce a free-text field to str — agents sometimes return a dict/list where prose was asked for."""
    if v is None or isinstance(v, str):
        return v
    if isinstance(v, (dict, list)):
        try:
            return json.dumps(v, ensure_ascii=False)
        except Exception:
            return str(v)
    return str(v)


NET_ENUM = ("mainnet-live", "amendment-pending", "testnet-devnet", "deprecated", "n/a")


def norm_network(v):
    """Normalize a free-text network_status to the decisive-axis enum (agents write rich prose here)."""
    s = txt(v)
    if not s:
        return "n/a"
    l = s.strip().lower()
    if l in NET_ENUM:
        return l
    if "deprecat" in l:
        return "deprecated"
    if "devnet" in l or "testnet" in l:
        return "testnet-devnet"
    if "draft" in l or "pending" in l or "voting" in l or "proposed" in l or "await" in l:
        return "amendment-pending"
    if "live" in l or "enabled" in l or "mainnet" in l or "production" in l:
        return "mainnet-live"
    return "n/a"


def norm_chain(v):
    """Normalize a free-text chain to the enum: xrpl-mainnet | xahau | xrpl-evm-sidechain | all | off-ledger."""
    s = txt(v)
    if not s:
        return "xrpl-mainnet"
    l = s.strip().lower()
    if l in ("xrpl-mainnet", "xahau", "xrpl-evm-sidechain", "all", "off-ledger"):
        return l
    if "evm" in l:
        return "xrpl-evm-sidechain"
    if "xahau" in l:
        return "xahau"
    if any(k in l for k in ("off-ledger", "off-chain", "ipfs", "arweave", "permaweb")):
        return "off-ledger"
    if l.startswith("all") or l.startswith("multi") or "cross-chain" in l:
        return "all"
    if "xrpl" in l or "ledger" in l or "mainnet" in l or "testnet" in l or "devnet" in l:
        return "xrpl-mainnet"
    return "xrpl-mainnet"


def slugify(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def priority(status, maturity):
    return 1 + STATUS_RANK.get(status, 5) + MATURITY_RANK.get(maturity, 2)


def uniq_slug(cur, table, base):
    s, k = base, 2
    while cur.execute(f"SELECT 1 FROM {table} WHERE slug=?", (s,)).fetchone():
        s, k = f"{base}-{k}", k + 1
    return s


def verdict_map(verify):
    return {(v.get("capability") or "").strip().lower(): v for v in ((verify or {}).get("verdicts") or [])}


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    wave_no = int(data.get("wave", 1))
    date = data.get("date", "")
    lanes = data.get("lanes", [])

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    with open(SCHEMA, "r", encoding="utf-8") as f:
        con.executescript(f.read())
    cur = con.cursor()

    cloud_model = next((l.get("cloud_verify", {}).get("model") for l in lanes if l.get("cloud_verify", {}).get("model")), None)
    vnote = ("Two-seat EXTERNAL_VERIFIER: seat 1 = Claude+WebFetch retrieval oracle (live xrpl.org / XLS docs); "
             f"seat 2 = cross-family Ollama Cloud {cloud_model or 'large model'} (AUTHORITATIVE, refute-by-default, "
             "no Claude-judges-Claude). verified flag set by the cross-family seat.")

    row = cur.execute("SELECT id FROM waves WHERE wave_number=?", (wave_no,)).fetchone()
    if row:
        wave_id = row[0]
        for t in ("capabilities", "sources"):
            cur.execute(f"DELETE FROM {t} WHERE wave_id=?", (wave_id,))  # capability_purposes cascade off capabilities
        cur.execute("UPDATE waves SET dispatched_date=?, status='synthesized', verifier_note=? WHERE id=?",
                    (date, vnote, wave_id))
    else:
        cur.execute(
            """INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path)
               VALUES(?,?,?,?,?,?,?,?)""",
            (wave_no, WAVE_TITLES.get(wave_no, f"Wave {wave_no}"), date,
             "whole XRPL ecosystem (protocol, tx, tokens, dex/amm, nfts, programmability, payments, identity, libs, infra)",
             len(lanes) * 2, vnote, "synthesized", f"waves/wave-{wave_no:02d}-foundation/dispatch.md"))
        wave_id = cur.lastrowid

    cat = {s: i for s, i in cur.execute("SELECT slug,id FROM categories")}
    track_anchor = {t: i for t, i in cur.execute("SELECT track,id FROM purposes WHERE track IS NOT NULL")}

    def purpose_id(name, track=None):
        sl = slugify(name)
        r = cur.execute("SELECT id FROM purposes WHERE slug=?", (sl,)).fetchone()
        if r:
            return r[0]
        cur.execute("INSERT INTO purposes(slug,name,track) VALUES(?,?,?)", (sl, name, track))
        return cur.lastrowid

    n_caps = n_src = n_links = 0
    for lane in lanes:
        lslug = lane.get("slug")
        category_id = cat.get(lslug)
        if category_id is None and lslug:  # safety net for a brand-new lane the swarm surfaced
            cur.execute("INSERT OR IGNORE INTO categories(slug,name,description,sort) VALUES(?,?,?,?)",
                        (lslug, (lane.get("name") or lslug.replace("-", " ").title()), "auto-created from wave lane", 99))
            category_id = cur.execute("SELECT id FROM categories WHERE slug=?", (lslug,)).fetchone()[0]
            cat[lslug] = category_id

        research = lane.get("research") or {}
        retrieval = verdict_map(lane.get("verify"))          # seat 1 (Claude)
        cloud = verdict_map(lane.get("cloud_verify"))        # seat 2 (cross-family — AUTHORITATIVE)

        for m in (research.get("capabilities") or []):
            name = txt(m.get("name"))
            key = (name or "").strip().lower()
            cslug = uniq_slug(cur, "capabilities", slugify(m.get("slug") or name))
            cv = cloud.get(key, {})
            rv = retrieval.get(key, {})
            cloud_overall = (cv.get("overall") or "").strip()
            verified = 1 if cloud_overall in CONFIRMED else 0

            parts = []
            if cv:
                parts.append(f"cross-family({cloud_model or 'cloud'})={cloud_overall or 'unverified'}")
                if cv.get("network_status_check"):
                    parts.append(f"net-check: {cv['network_status_check']}")
                if cv.get("currency"):
                    parts.append(f"currency={cv['currency']}")
                if cv.get("fixes"):
                    parts.append(f"fix: {cv['fixes']}")
                if cv.get("note"):
                    parts.append(cv["note"])
            else:
                parts.append("cross-family seat: pending")
            if rv:
                rparts = [f"retrieval(claude)={(rv.get('overall') or '?')}"]
                if rv.get("fixes"):
                    rparts.append(f"fix: {rv['fixes']}")
                if rv.get("note"):
                    rparts.append(rv["note"])
                parts.append(" ".join(rparts))
            verify_note = " | ".join(p for p in parts if p) or None

            status, maturity = txt(m.get("status")), txt(m.get("maturity_tier"))
            bf = m.get("builder_fit")
            bf = int(bf) if isinstance(bf, (int, float)) else None
            cur.execute(
                """INSERT INTO capabilities(slug,name,category_id,kind,network_status,chain,xls_standard,amendment_name,
                   enabled_date,maturity_tier,status,builder_fit,commercial_use,summary,key_fields,gotchas,
                   download_priority,verified,verify_note,wave_id,created_date)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (cslug, name, category_id, txt(m.get("kind")), norm_network(m.get("network_status")), norm_chain(m.get("chain")),
                 txt(m.get("xls_standard")), txt(m.get("amendment_name")), txt(m.get("enabled_date")), maturity, status, bf,
                 txt(m.get("commercial_use")), txt(m.get("summary")), txt(m.get("key_fields")), txt(m.get("gotchas")),
                 priority(status, maturity), verified, verify_note, wave_id, date))
            cap_id = cur.lastrowid
            n_caps += 1

            # build-focus tracks (coarse) -> link the seeded track-anchor purpose
            for tr in (m.get("tracks") or []):
                tr = (txt(tr) or "").strip()
                if not tr:
                    continue
                aid = track_anchor.get(tr)
                if aid is None and tr:  # unseen track value -> create an anchor so it still folders
                    cur.execute("INSERT OR IGNORE INTO purposes(slug,name,track) VALUES(?,?,?)",
                                (f"track-{slugify(tr)}", tr.replace("-", " ").title(), tr))
                    aid = cur.execute("SELECT id FROM purposes WHERE slug=?", (f"track-{slugify(tr)}",)).fetchone()[0]
                    track_anchor[tr] = aid
                if aid:
                    cur.execute("INSERT OR IGNORE INTO capability_purposes(capability_id,purpose_id,fitness) VALUES(?,?,?)",
                                (cap_id, aid, bf))
                    n_links += 1

            # fine-grained best_for -> upsert a purpose (tagged with its track) and link with fitness
            for b in (m.get("best_for") or []):
                if not isinstance(b, dict):
                    continue
                pn = txt(b.get("purpose"))
                if not pn:
                    continue
                pid = purpose_id(pn, (txt(b.get("track")) or "").strip() or None)
                fit = b.get("fitness")
                fit = int(fit) if isinstance(fit, (int, float)) else None
                cur.execute("INSERT OR REPLACE INTO capability_purposes(capability_id,purpose_id,fitness,note) VALUES(?,?,?,?)",
                            (cap_id, pid, fit, None))
                n_links += 1

            # sources — sources.verified = does it RESOLVE (retrieval oracle / seat 1)
            src_resolves = 1 if cloud_overall in CONFIRMED else 0  # tie source trust to the authoritative cross-family seat
            for s in (m.get("sources") or []):
                if not isinstance(s, dict) or not s.get("url"):
                    continue
                cur.execute(
                    """INSERT INTO sources(capability_id,kind,title,url,claim,retrieved_date,verified,wave_id)
                       VALUES(?,?,?,?,?,?,?,?)""",
                    (cap_id, txt(s.get("kind")), txt(s.get("title")), txt(s.get("url")), txt(s.get("claim")),
                    # NULL, not a copy of the parent's verdict. These wave files carry no
                    # per-source check at all, and stamping the entity's verdict onto every
                    # source produced 100.0% correlation across 934 rows — a copy presented
                    # as an independent seat. NULL means unchecked, which is the truth.
                     date, None, wave_id))
                n_src += 1

    # FTS rebuild
    cur.execute("DELETE FROM capabilities_fts")
    cur.execute(
        """INSERT INTO capabilities_fts(rowid,slug,name,kind,summary,network_status,xls_standard,category)
           SELECT cap.id, cap.slug, cap.name, COALESCE(cap.kind,''), COALESCE(cap.summary,''),
                  COALESCE(cap.network_status,''), COALESCE(cap.xls_standard,''),
                  COALESCE((SELECT name FROM categories c WHERE c.id=cap.category_id),'')
           FROM capabilities cap""")

    for k, vv in {"kb_name": "xrpl-knowledge",
                  "verifier": ("seat1=claude+webfetch retrieval oracle ; "
                               f"seat2={cloud_model or 'ollama-cloud-large'} cross-family (authoritative)"),
                  "decisive_axis": "network_status — mainnet-live vs amendment-pending / devnet / deprecated"}.items():
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (k, vv))
    set_meta_currency(cur)
    con.commit()

    print(f"wave {wave_no}: {n_caps} capabilities, {n_src} sources, {n_links} purpose-links.")
    for r in cur.execute(
        """SELECT c.name, COUNT(*), COALESCE(SUM(cap.verified),0)
           FROM capabilities cap JOIN categories c ON c.id=cap.category_id
           WHERE cap.wave_id=? GROUP BY c.name ORDER BY c.sort""", (wave_id,)):
        print(f"  {r[0]:34s} {r[1]:2d} caps  ({r[2]} cross-family verified)")
    nstat = cur.execute("SELECT network_status, COUNT(*) FROM capabilities WHERE wave_id=? GROUP BY network_status", (wave_id,)).fetchall()
    print("  by network_status: " + " · ".join(f"{(s or '?')}={n}" for s, n in nstat))
    con.close()


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-foundation", "research-raw.json")
    main(p)
