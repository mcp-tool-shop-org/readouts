#!/usr/bin/env python3
"""Ingest a study-swarm wave's research-raw.json into tensor-engine-knowledge/engines.db.

Idempotent per wave: deletes any existing rows for the wave_number before inserting,
so re-running a wave (after a re-dispatch) cleanly replaces it.

Usage:
    python load_db.py [path/to/research-raw.json]
Default path: ../waves/wave-01-foundation/research-raw.json

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
DB = os.path.join(ROOT, "engines.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

WAVE_TITLES = {
    1: "Foundation — best tensor / inference / training engines per lane",
    2: "Deep — close the verifier queue + version-pinned config recipes",
    3: "Expansion — 3 new lanes (structured-output, speech, profiling) + deepen kernels & training",
    4: "Measured rig baseline — RTX 5090 thermals / power / throughput via Ollama",
}

# maturity tier -> install-priority rank (lower = grab first)
TIER_RANK = {"production": 0, "mature": 1, "stable": 2, "experimental": 4, "legacy": 7, "avoid": 9}
STATUS_RANK = {"recommended": 0, "runner-up": 2, "situational": 4, "legacy": 7, "avoid": 9}


def slugify(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def priority(status, tier):
    return 1 + STATUS_RANK.get(status, 5) + TIER_RANK.get(tier, 5)


def uniq_slug(cur, table, base):
    s, k = base, 2
    while cur.execute(f"SELECT 1 FROM {table} WHERE slug=?", (s,)).fetchone():
        s, k = f"{base}-{k}", k + 1
    return s


def tri(v):
    """boolean-ish -> 1/0/None for blackwell_ready."""
    if v is True:
        return 1
    if v is False:
        return 0
    if isinstance(v, str):
        t = v.strip().lower()
        if t in ("yes", "true", "1"):
            return 1
        if t in ("no", "false", "0"):
            return 0
    return None


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
    # recipe layer (engine-room knowledge side) — folded so a fresh load recreates its tables.
    # DDL lives in recipes/recipes.schema.sql (single source); data is populated by recipes/_*.py.
    _rec = os.path.join(ROOT, "recipes", "recipes.schema.sql")
    if os.path.exists(_rec):
        with open(_rec, "r", encoding="utf-8") as f:
            con.executescript(f.read())
    cur = con.cursor()

    row = cur.execute("SELECT id FROM waves WHERE wave_number=?", (wave_no,)).fetchone()
    if row:
        wave_id = row[0]
        for t in ("engines", "sources", "config_recipes"):
            cur.execute(f"DELETE FROM {t} WHERE wave_id=?", (wave_id,))
        cur.execute("UPDATE waves SET dispatched_date=?, status='synthesized' WHERE id=?", (date, wave_id))
    else:
        cur.execute(
            """INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path)
               VALUES(?,?,?,?,?,?,?,?)""",
            (wave_no, WAVE_TITLES.get(wave_no, f"Wave {wave_no}"), date,
             "all (llm-inference, llm-serving, quantization, attention-kernels, training, diffusion-engines, runtime-foundations)",
             len(lanes) * 2,
             "Reasoning-stripped adversarial verifier per lane (different model tier); WebFetch/WebSearch as retrieval oracle "
             "(existence/license/specs/currency). Family-different prism/roleos path deferred to a later wave.",
             "synthesized", f"waves/{os.path.basename(os.path.dirname(os.path.abspath(path)))}/dispatch.md"))
        wave_id = cur.lastrowid

    cat = {s: i for s, i in cur.execute("SELECT slug,id FROM categories")}

    def purpose_id(name, category_id):
        sl = slugify(name)
        r = cur.execute("SELECT id FROM purposes WHERE slug=?", (sl,)).fetchone()
        if r:
            return r[0]
        cur.execute("INSERT INTO purposes(slug,name,category_id) VALUES(?,?,?)", (sl, name, category_id))
        return cur.lastrowid

    n_eng = n_src = n_rec = 0
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
        verdicts = {(v.get("model") or "").strip().lower(): v for v in (verify.get("verdicts") or [])}

        for m in (research.get("engines") or []):
            name = m.get("name")
            eslug = uniq_slug(cur, "engines", slugify(m.get("slug") or name))
            v = verdicts.get((name or "").strip().lower(), {})
            overall = v.get("overall")
            verified = 1 if overall in ("confirmed", "confirmed-with-fixes") else 0
            parts = []
            if overall:
                parts.append(f"verdict={overall}")
            if v.get("currency"):
                parts.append(f"currency={v['currency']}")
            if v.get("license_status") == "corrected" and v.get("license_correction"):
                parts.append(f"license-correction: {v['license_correction']}")
            if v.get("fixes"):
                parts.append(f"fixes: {v['fixes']}")
            if v.get("note"):
                parts.append(v["note"])
            vnote = " | ".join(parts) or None

            status, tier = m.get("status"), m.get("maturity_tier")
            cur.execute(
                """INSERT INTO engines(slug,name,category_id,engine_type,developer,language,latest_version,release_date,
                   license,commercial_use,commercial_notes,maturity_tier,platforms,accelerators,model_formats,
                   blackwell_ready,optimization_for,multi_gpu,speed_note,repo_url,status,rig_fit,studio_fit,
                   download_priority,summary,verified,verify_note,wave_id,created_date)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (eslug, name, category_id, m.get("engine_type"), m.get("developer"), m.get("language"),
                 m.get("latest_version"), m.get("release_date"), m.get("license"), m.get("commercial_use"),
                 m.get("commercial_notes"), tier, m.get("platforms"), m.get("accelerators"), m.get("model_formats"),
                 tri(m.get("blackwell_ready")), m.get("optimization_for"), m.get("multi_gpu"), m.get("speed_note"),
                 m.get("repo_url"), status, m.get("rig_fit"), m.get("studio_fit"), priority(status, tier),
                 m.get("summary"), verified, vnote, wave_id, date))
            engine_id = cur.lastrowid
            n_eng += 1

            for bf in (m.get("best_for") or []):
                pn = bf.get("purpose")
                if not pn:
                    continue
                cur.execute(
                    "INSERT OR REPLACE INTO engine_purposes(engine_id,purpose_id,fitness,rank,use_tag,note) VALUES(?,?,?,?,?,?)",
                    (engine_id, purpose_id(pn, category_id), bf.get("fitness"), None, bf.get("use_tag"), None))

            for s in (m.get("sources") or []):
                if not s.get("url"):
                    continue
                cur.execute(
                    "INSERT INTO sources(engine_id,kind,title,url,claim,retrieved_date,verified,wave_id) VALUES(?,?,?,?,?,?,?,?)",
                    # NULL, not a copy of the parent's verdict. These wave files carry no
                    # per-source check at all, and stamping the entity's verdict onto every
                    # source produced 100.0% correlation across 934 rows — a copy presented
                    # as an independent seat. NULL means unchecked, which is the truth.
                    (engine_id, s.get("kind"), s.get("title"), s.get("url"), s.get("claim"), date, None, wave_id))
                n_src += 1

        for e in (research.get("extras") or []):
            kind = (e.get("kind") or "").lower()
            name, url, note = e.get("name"), e.get("url"), e.get("note")
            if "recipe" in kind or "baseline" in kind:
                rslug = uniq_slug(cur, "config_recipes", slugify(f"{lslug}-{name}"))
                cur.execute(
                    "INSERT INTO config_recipes(slug,name,category_id,kind,url,body,wave_id) VALUES(?,?,?,?,?,?,?)",
                    (rslug, name, category_id, "baseline" if "baseline" in kind else "recipe", url, note, wave_id))
                n_rec += 1
            elif url:  # tool | resource -> evidence trail
                cur.execute("INSERT INTO sources(subject,kind,title,url,claim,retrieved_date,wave_id) VALUES(?,?,?,?,?,?,?)",
                            (name, kind or "resource", name, url, note, date, wave_id))
                n_src += 1

    cur.execute("DELETE FROM engines_fts")
    cur.execute(
        """INSERT INTO engines_fts(rowid,slug,name,engine_type,summary,best_for,license,category,model_formats)
           SELECT e.id, e.slug, e.name, COALESCE(e.engine_type,''), COALESCE(e.summary,''),
                  COALESCE((SELECT group_concat(p.name,' ') FROM engine_purposes ep
                            JOIN purposes p ON p.id=ep.purpose_id WHERE ep.engine_id=e.id),''),
                  COALESCE(e.license,''),
                  COALESCE((SELECT name FROM categories c WHERE c.id=e.category_id),''),
                  COALESCE(e.model_formats,'')
           FROM engines e""")

    # Static identity keys. The currency pointer (latest_wave/updated) is NOT set
    # from this wave — set_meta_currency derives it from MAX(waves.wave_number) so
    # re-ingesting an old wave, or appending waves via one-off scripts, can never
    # make meta lie about how current the KB is.
    meta = {
        "kb_name": "tensor-engine-knowledge",
        "rig": "OMEN 45L · RTX 5090 · Blackwell sm_120 · 32 GB VRAM · Core Ultra 9 · 64 GB RAM · Windows 11 (the only machine)",
        "scope": "Tensor/inference/training engines — the software that runs & trains models. Models themselves live in the model-knowledge KB.",
    }
    for k, vv in meta.items():
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (k, vv))
    set_meta_currency(cur)  # latest_wave = MAX(wave_number), updated = that wave's date

    con.commit()
    print(f"wave {wave_no}: {n_eng} engines, {n_src} sources, {n_rec} config_recipes.")
    for r in cur.execute(
        """SELECT c.name, COUNT(*), COALESCE(SUM(e.verified),0)
           FROM engines e JOIN categories c ON c.id=e.category_id
           WHERE e.wave_id=? GROUP BY c.name ORDER BY c.sort""", (wave_id,)):
        print(f"  {r[0]:34s} {r[1]:2d} engines  ({r[2]} verified)")
    con.close()


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-foundation", "research-raw.json")
    main(p)
