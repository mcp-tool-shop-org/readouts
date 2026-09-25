#!/usr/bin/env python3
"""Ingest a study-swarm wave's research-raw.json into model-knowledge/models.db.

Idempotent per wave: deletes any existing rows for the wave_number before inserting,
so re-running a wave (after a re-dispatch) cleanly replaces it.

Usage:
    python load_db.py [path/to/research-raw.json]
Default path: ../waves/wave-01-foundation/research-raw.json
"""
import json
import os
import re
import sqlite3
import sys

from refresh_meta import set_meta_currency  # currency pointer is derived from the DB, never the ingest wave

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "models.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

WAVE_TITLES = {1: "Foundation — best current models per domain"}

TIER_RANK = {"frontier": 0, "strong": 1, "solid": 2, "legacy": 7, "avoid": 9}
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


def ensure_cloud_columns(cur):
    """Migrate a pre-wave-6 DB in place: schema.sql's CREATE TABLE IF NOT EXISTS
    cannot add columns to an existing table."""
    cols = {c[1] for c in cur.execute("PRAGMA table_info(models)")}
    for col in ("cloud_feasible", "cloud_note"):
        if col not in cols:
            cur.execute(f"ALTER TABLE models ADD COLUMN {col} TEXT")


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
    ensure_cloud_columns(cur)

    # Wave metadata: prefer the wave file's own top-level fields (title, domain_scope,
    # agent_count, verifier_note, dispatch_path — present from wave 5 on), falling back
    # to the wave-1-era defaults for older files that lack them.
    w_title = data.get("title") or WAVE_TITLES.get(wave_no, f"Wave {wave_no}")
    w_scope = data.get("domain_scope") or "all (image, control, video, 3d, audio, llm, comfy)"
    w_agents = data.get("agent_count", len(lanes) * 2)
    w_vnote = data.get("verifier_note") or (
        "Reasoning-stripped adversarial verifier per lane; WebFetch as retrieval oracle "
        "(existence/license/specs). Family-different prism/roleos path deferred to a later wave.")
    w_dpath = data.get("dispatch_path") or "waves/wave-01-foundation/dispatch.md"

    row = cur.execute("SELECT id FROM waves WHERE wave_number=?", (wave_no,)).fetchone()
    if row:
        wave_id = row[0]
        for t in ("models", "sources", "custom_nodes", "workflows"):
            cur.execute(f"DELETE FROM {t} WHERE wave_id=?", (wave_id,))
        cur.execute(
            """UPDATE waves SET title=?, dispatched_date=?, domain_scope=?, agent_count=?,
               verifier_note=?, dispatch_path=?, status='synthesized' WHERE id=?""",
            (w_title, date, w_scope, w_agents, w_vnote, w_dpath, wave_id))
    else:
        cur.execute(
            """INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path)
               VALUES(?,?,?,?,?,?,?,?)""",
            (wave_no, w_title, date, w_scope, w_agents, w_vnote, "synthesized", w_dpath))
        wave_id = cur.lastrowid

    cat = {s: i for s, i in cur.execute("SELECT slug,id FROM categories")}

    def purpose_id(name, category_id):
        sl = slugify(name)
        r = cur.execute("SELECT id FROM purposes WHERE slug=?", (sl,)).fetchone()
        if r:
            return r[0]
        cur.execute("INSERT INTO purposes(slug,name,category_id) VALUES(?,?,?)", (sl, name, category_id))
        return cur.lastrowid

    n_models = n_sources = n_nodes = n_wf = 0
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

        for m in (research.get("models") or []):
            name = m.get("name")
            mslug = uniq_slug(cur, "models", slugify(m.get("slug") or name))
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

            r32 = m.get("runs_on_32gb")
            r32 = 1 if r32 is True else (0 if r32 is False else None)
            status, tier = m.get("status"), m.get("quality_tier")
            cur.execute(
                """INSERT INTO models(slug,name,category_id,base_arch,developer,release_date,params,
                   disk_size_gb,min_vram_gb,recommended_vram_gb,runs_on_32gb,license,commercial_use,commercial_notes,
                   quality_tier,speed_note,repo_url,status,game_asset_fit,marketing_fit,download_priority,summary,
                   verified,verify_note,cloud_feasible,cloud_note,wave_id,created_date)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (mslug, name, category_id, m.get("base_arch"), m.get("developer"), m.get("release_date"),
                 m.get("params"), m.get("disk_size_gb"), m.get("min_vram_gb"), m.get("recommended_vram_gb"),
                 r32, m.get("license"), m.get("commercial_use"), m.get("commercial_notes"), tier,
                 m.get("speed_note"), m.get("repo_url"), status, m.get("game_asset_fit"), m.get("marketing_fit"),
                 priority(status, tier), m.get("summary"), verified, vnote,
                 m.get("cloud_feasible"), m.get("cloud_note"), wave_id, date))
            model_id = cur.lastrowid
            n_models += 1

            for bf in (m.get("best_for") or []):
                pn = bf.get("purpose")
                if not pn:
                    continue
                cur.execute(
                    "INSERT OR REPLACE INTO model_purposes(model_id,purpose_id,fitness,rank,use_tag,note) VALUES(?,?,?,?,?,?)",
                    (model_id, purpose_id(pn, category_id), bf.get("fitness"), None, bf.get("use_tag"), None))

            for s in (m.get("sources") or []):
                if not s.get("url"):
                    continue
                cur.execute(
                    "INSERT INTO sources(model_id,kind,title,url,claim,retrieved_date,verified,wave_id) VALUES(?,?,?,?,?,?,?,?)",
                    # NULL, not a copy of the parent's verdict. These wave files carry no
                    # per-source check at all, and stamping the entity's verdict onto every
                    # source produced 100.0% correlation across 934 rows — a copy presented
                    # as an independent seat. NULL means unchecked, which is the truth.
                    (model_id, s.get("kind"), s.get("title"), s.get("url"), s.get("claim"), date, None, wave_id))
                n_sources += 1

        for e in (research.get("extras") or []):
            kind = (e.get("kind") or "").lower()
            name, url, note = e.get("name"), e.get("url"), e.get("note")
            if "node" in kind:
                cur.execute("INSERT INTO custom_nodes(name,url,note,essential,wave_id) VALUES(?,?,?,?,?)",
                            (name, url, note, 1, wave_id))
                n_nodes += 1
            elif "workflow" in kind:
                wfslug = uniq_slug(cur, "workflows", slugify(f"{lslug}-{name}"))
                cur.execute(
                    "INSERT INTO workflows(slug,name,category_id,kind,url,description,wave_id) VALUES(?,?,?,?,?,?,?)",
                    (wfslug, name, category_id, "workflow-source" if "source" in kind else "workflow", url, note, wave_id))
                n_wf += 1
            else:
                if url:
                    cur.execute("INSERT INTO sources(subject,kind,title,url,claim,retrieved_date,wave_id) VALUES(?,?,?,?,?,?,?)",
                                (name, kind or "resource", name, url, note, date, wave_id))
                    n_sources += 1

    # model_updates: cross-cutting axis updates to models ingested by EARLIER waves
    # (wave 6+). Applied by slug; an unmatched slug is a hard error (a silently
    # dropped fact), so ingest waves in order — wave 6 updates wave-5 models, etc.
    # NOTE: re-ingesting an older wave replaces its model rows, which DISCARDS any
    # updates later waves applied to them — after re-ingesting wave N, re-run every
    # wave > N that carries model_updates.
    n_upd, unmatched = 0, []
    for u in (data.get("model_updates") or []):
        uslug = u.get("slug")
        cur.execute("UPDATE models SET cloud_feasible=?, cloud_note=? WHERE slug=?",
                    (u.get("cloud_feasible"), u.get("cloud_note"), uslug))
        if cur.rowcount == 0:
            unmatched.append(uslug)
        else:
            n_upd += 1
    if unmatched:
        con.rollback()
        sys.exit(f"ANDON: {len(unmatched)} model_updates slugs match no model row — "
                 f"nothing committed. Ingest earlier waves first or fix the slugs: {unmatched}")

    cur.execute("DELETE FROM models_fts")
    cur.execute(
        """INSERT INTO models_fts(rowid,slug,name,base_arch,summary,best_for,license,category)
           SELECT m.id, m.slug, m.name, COALESCE(m.base_arch,''), COALESCE(m.summary,''),
                  COALESCE((SELECT group_concat(p.name,' ') FROM model_purposes mp
                            JOIN purposes p ON p.id=mp.purpose_id WHERE mp.model_id=m.id),''),
                  COALESCE(m.license,''),
                  COALESCE((SELECT name FROM categories c WHERE c.id=m.category_id),'')
           FROM models m""")

    # Static identity keys. The currency pointer (latest_wave/updated) is NOT set
    # from this wave — set_meta_currency derives it from MAX(waves.wave_number) so
    # re-ingesting an old wave, or appending waves via one-off scripts, can never
    # make meta lie about how current the KB is. (wave 0 = local-workflows seed.)
    meta = {
        "kb_name": "model-knowledge",
        "storage_convention": (r"checkpoints/unets/loras -> E:\AI-Models\ComfyUI\models\<class>\ ; "
                               r"HF cache -> E:\AI-Models\hf-cache (set HF_HOME) ; Ollama -> E:\AI-Models\Ollama"),
        "runtime_ref": r"comfyui-setup.md (memory): runtime E:\AI-Models\ComfyUI-runtime ; comfy-headless client v2.5.2",
    }
    for k, vv in meta.items():
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (k, vv))
    set_meta_currency(cur)  # latest_wave = MAX(wave_number), updated = that wave's date

    con.commit()
    print(f"wave {wave_no}: {n_models} models, {n_sources} sources, {n_nodes} custom_nodes, "
          f"{n_wf} workflows, {n_upd} model_updates.")
    for r in cur.execute(
        """SELECT c.name, COUNT(*), COALESCE(SUM(m.verified),0)
           FROM models m JOIN categories c ON c.id=m.category_id
           WHERE m.wave_id=? GROUP BY c.name ORDER BY c.sort""", (wave_id,)):
        print(f"  {r[0]:30s} {r[1]:2d} models  ({r[2]} verified)")
    con.close()


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-foundation", "research-raw.json")
    main(p)
