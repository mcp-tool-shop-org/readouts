#!/usr/bin/env python3
"""Ingest a study-swarm wave's research-raw.json into sprites-knowledge/recipes.db.

Idempotent per wave: deletes any existing rows for the wave_number before inserting,
so re-running a wave (after a re-dispatch) cleanly replaces it and leaves other waves
untouched.

research-raw.json shape (the contract the wave swarm produces):
{
  "wave": <int>, "date": "YYYY-MM-DD", "title": "...", "domain_scope": "...",
  "agent_count": <int>, "verifier_note": "...",
  "lanes": [{
    "laneSlug": "<categories.slug>", "title": "...",
    "recipes": [{
      slug,name,kind,engine_family,applicable_to,base_model_family,claim,summary,design_implication,
      evidence_strength,seed,num_runs,variance_note,tuning_budget,measured_conditions,
      engine_recipe_ref,base_model_slug,predecessor_slug,stage_order,
      license,commercial_use,commercial_notes,vram_gb,rig_fit,studio_fit,download_priority,status,
      verified,verify_note,license_correction,
      purposes:[{purpose_slug,purpose_name,fitness,rank,use_tag,note}],
      hparams:[{name,value,unit,note,required}],
      failures:[{symptom,cause,remediation,severity,recipe_field}],
      evals:[{eval_kind,metric,harness,result,threshold,accepted,note}],
      sources:[{kind,title,authors,year,identifier,url,claim,finding_supported,verified}]
    }]
  }]
}

category_id resolves laneSlug -> categories.slug (the 7 lanes are seeded by schema.sql).
predecessor_slug -> predecessor_recipe_id is resolved in a second pass once all recipes exist.

Run with UTF-8 forced on Windows (entries carry em-dashes):
    $env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'; python scripts/load_db.py waves/wave-01-foundation/research-raw.json
"""
import json
import os
import re
import sqlite3
import sys

from refresh_meta import set_meta_currency  # currency pointer is derived from the DB, never the ingest wave

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "recipes.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

# One definition of `verified`, shared by every KB — see shared/verdicts.py.
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "shared"))
from verdicts import Verdicts, note_with_corrections  # noqa: E402


# status + evidence ordinals -> try-first ordering (lower = try first)
STATUS_RANK = {"recommended": 0, "runner-up": 2, "situational": 4, "legacy": 7, "superseded": 8, "avoid": 9}
EV_RANK = {"measured-on-rig": 0, "reproduced-from-source": 1, "single-reported-run": 3,
           "community-claim": 5, "untested": 7}


def slugify(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def priority(status, evidence):
    return 1 + STATUS_RANK.get(status, 5) + EV_RANK.get(evidence, 4)


def uniq_slug(cur, table, base):
    s, k = base, 2
    while cur.execute(f"SELECT 1 FROM {table} WHERE slug=?", (s,)).fetchone():
        s, k = f"{base}-{k}", k + 1
    return s


def i(v):
    """int-or-None."""
    try:
        return int(v) if v is not None and str(v).strip() != "" else None
    except (ValueError, TypeError):
        return None


def b(v):
    """bool-ish -> 1/0/None."""
    if v in (True, 1):
        return 1
    if v in (False, 0):
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
    if "lanes" not in data and isinstance(data.get("result"), dict):  # tolerate harness envelope
        data = data["result"]
    wave_no = int(data.get("wave", 1))
    date = data.get("date", "")
    title = data.get("title") or f"Wave {wave_no}"
    domain_scope = data.get("domain_scope")
    agent_count = i(data.get("agent_count"))
    verifier_note = data.get("verifier_note")
    lanes = data.get("lanes", [])

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    with open(SCHEMA, "r", encoding="utf-8") as f:
        con.executescript(f.read())
    cur = con.cursor()
    VERD = Verdicts(ROOT)

    # wave row (insert or refresh) ------------------------------------------------
    row = cur.execute("SELECT id FROM waves WHERE wave_number=?", (wave_no,)).fetchone()
    if row:
        wave_id = row[0]
        # clean replace: cascade clears recipe-linked rows; explicitly clear wave-scoped orphans
        cur.execute("DELETE FROM recipes WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM datasets WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM recipe_failures WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM sources WHERE wave_id=?", (wave_id,))
        cur.execute(
            "UPDATE waves SET title=?, dispatched_date=?, domain_scope=?, agent_count=?, verifier_note=?, "
            "status='synthesized' WHERE id=?",
            (title, date, domain_scope, agent_count, verifier_note, wave_id))
    else:
        cur.execute(
            """INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path)
               VALUES(?,?,?,?,?,?,?,?)""",
            (wave_no, title, date, domain_scope, agent_count if agent_count is not None else len(lanes),
             verifier_note or "Reasoning-stripped adversarial verifier + retrieval oracle per lane (existence / "
             "license / specs / currency). Default verdict unverified on non-confirmation.",
             "synthesized", f"waves/{os.path.basename(os.path.dirname(os.path.abspath(path)))}/dispatch.md"))
        wave_id = cur.lastrowid

    cat = {s: i_ for s, i_ in cur.execute("SELECT slug,id FROM categories")}

    def purpose_id(slug, name, category_id):
        sl = slugify(slug or name)
        r = cur.execute("SELECT id FROM purposes WHERE slug=?", (sl,)).fetchone()
        if r:
            return r[0]
        cur.execute("INSERT INTO purposes(slug,name,category_id) VALUES(?,?,?)",
                    (sl, name or sl.replace("-", " ").title(), category_id))
        return cur.lastrowid

    def add_sources(rows, recipe_id, subject=None, target_table=None, target_id=None):
        n = 0
        for s in (rows or []):
            if not s.get("url"):
                continue
            fs = s.get("finding_supported")
            # an explicit per-source `verified` wins; else infer from finding_supported
            ver = b(s.get("verified"))
            if ver is None:
                ver = 1 if fs in ("SUPPORTED", "PARTIAL") else 0
            cur.execute(
                """INSERT INTO sources(recipe_id,subject,kind,title,authors,year,identifier,url,claim,
                   retrieved_date,verified,finding_supported,target_table,target_id,wave_id)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (recipe_id, subject, s.get("kind"), s.get("title"), s.get("authors"),
                 str(s.get("year") or "") or None, s.get("identifier"), s.get("url"), s.get("claim"), date,
                 ver, fs, target_table, target_id, wave_id))
            n += 1
        return n

    n_rec = n_hp = n_fail = n_eval = n_src = 0
    pending_pred = []   # (recipe_id, predecessor_slug) resolved after all recipes exist
    rec_ids = {}        # source slug -> id

    for lane in lanes:
        lslug = lane.get("laneSlug") or lane.get("slug")
        category_id = cat.get(lslug)
        if category_id is None and lslug:  # safety net for a brand-new lane slug
            cur.execute("INSERT OR IGNORE INTO categories(slug,name,description,sort) VALUES(?,?,?,?)",
                        (lslug, lslug.replace("-", " ").title(), "auto-created from wave lane", 99))
            category_id = cur.execute("SELECT id FROM categories WHERE slug=?", (lslug,)).fetchone()[0]
            cat[lslug] = category_id

        VERD.use_lane(lane)
        for t in (lane.get("recipes") or []):
            name = t.get("name")
            rslug = uniq_slug(cur, "recipes", slugify(t.get("slug") or name))
            verified, vstatus, vnote, corr = VERD.for_entry(rslug, name)
            own = t.get("verify_note")
            if corr:
                # A corrected verdict leads: the research seat's own note is what was corrected.
                vnote = note_with_corrections(vnote, corr) + (f" [research note: {own}]" if own else "")
            else:
                vnote = f"{own} [{vnote}]" if own else vnote
            status = "avoid" if vstatus == "avoid" else t.get("status")
            ev = t.get("evidence_strength")
            cur.execute(
                """INSERT INTO recipes(slug,name,category_id,kind,engine_family,applicable_to,base_model_family,
                   claim,summary,design_implication,evidence_strength,seed,num_runs,variance_note,tuning_budget,
                   measured_conditions,engine_recipe_ref,base_model_slug,stage_order,license,commercial_use,
                   commercial_notes,vram_gb,rig_fit,studio_fit,download_priority,status,verified,verify_note,
                   license_correction,wave_id,created_date)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (rslug, name, category_id, t.get("kind"), t.get("engine_family"), t.get("applicable_to"),
                 t.get("base_model_family"), t.get("claim"), t.get("summary"), t.get("design_implication"), ev,
                 t.get("seed"), i(t.get("num_runs")), t.get("variance_note"), t.get("tuning_budget"),
                 t.get("measured_conditions"), t.get("engine_recipe_ref"), t.get("base_model_slug"),
                 i(t.get("stage_order")), t.get("license"), t.get("commercial_use"), t.get("commercial_notes"),
                 t.get("vram_gb"), i(t.get("rig_fit")), i(t.get("studio_fit")),
                 i(t.get("download_priority")) if t.get("download_priority") is not None
                 else priority(status, ev),
                 status, verified, vnote, t.get("license_correction"),
                 wave_id, date))
            rid = cur.lastrowid
            rec_ids[t.get("slug") or rslug] = rid
            n_rec += 1
            if t.get("predecessor_slug"):
                pending_pred.append((rid, t["predecessor_slug"]))

            for hp in (t.get("hparams") or []):
                cur.execute("INSERT INTO recipe_hparams(recipe_id,name,value,unit,required,note) VALUES(?,?,?,?,?,?)",
                            (rid, hp.get("name"), str(hp.get("value")) if hp.get("value") is not None else None,
                             hp.get("unit"), b(hp.get("required")) or 0, hp.get("note")))
                n_hp += 1
            for fa in (t.get("failures") or []):
                cur.execute(
                    "INSERT INTO recipe_failures(recipe_id,symptom,cause,remediation,recipe_field,severity,wave_id) "
                    "VALUES(?,?,?,?,?,?,?)",
                    (rid, fa.get("symptom"), fa.get("cause"), fa.get("remediation"), fa.get("recipe_field"),
                     fa.get("severity"), wave_id))
                n_fail += 1
            for ev_row in (t.get("evals") or []):
                cur.execute(
                    """INSERT INTO recipe_evals(recipe_id,eval_kind,metric,harness,result,threshold,accepted,note)
                       VALUES(?,?,?,?,?,?,?,?)""",
                    (rid, ev_row.get("eval_kind"), ev_row.get("metric"), ev_row.get("harness"),
                     ev_row.get("result"), ev_row.get("threshold"), b(ev_row.get("accepted")), ev_row.get("note")))
                n_eval += 1
            for pu in (t.get("purposes") or []):
                psl = pu.get("purpose_slug")
                pn = pu.get("purpose_name")
                if not (psl or pn):
                    continue
                cur.execute(
                    "INSERT OR REPLACE INTO recipe_purposes(recipe_id,purpose_id,fitness,rank,use_tag,note) "
                    "VALUES(?,?,?,?,?,?)",
                    (rid, purpose_id(psl, pn, category_id), i(pu.get("fitness")), i(pu.get("rank")),
                     pu.get("use_tag"), pu.get("note")))
            n_src += add_sources(t.get("sources"), rid)

    # resolve predecessor links now that every recipe exists ----------------------
    for rid, pred_slug in pending_pred:
        pid = rec_ids.get(pred_slug) or (
            lambda r: r[0] if r else None)(cur.execute("SELECT id FROM recipes WHERE slug=?", (slugify(pred_slug),)).fetchone())
        if pid:
            cur.execute("UPDATE recipes SET predecessor_recipe_id=? WHERE id=?", (pid, rid))

    # rebuild FTS ----------------------------------------------------------------
    cur.execute("DELETE FROM recipes_fts")
    cur.execute(
        """INSERT INTO recipes_fts(rowid,slug,name,engine_family,applicable_to,base_model_family,summary,claim,category)
           SELECT r.id, r.slug, r.name, COALESCE(r.engine_family,''), COALESCE(r.applicable_to,''),
                  COALESCE(r.base_model_family,''), COALESCE(r.summary,''), COALESCE(r.claim,''),
                  COALESCE((SELECT name FROM categories c WHERE c.id=r.category_id),'')
           FROM recipes r""")

    # meta: static identity + DB-derived currency pointer ------------------------
    meta = {
        "kb_name": "sprites-knowledge",
        "rig": "OMEN 45L · RTX 5090 · Blackwell sm_120 · 32 GB VRAM · Core Ultra 9 · 64 GB RAM · Windows 11 / WSL2 (the only machine)",
        "scope": "The sprite PIPELINE craft — recipes (procedures + model choices) that turn concept art into "
                 "game-ready 2.5D JRPG sprites: image->3D->multi-view, headless render & lighting, downsample & "
                 "pixel finish, NVS-direct turnaround, diffusion sprite-sheets, sprite QA/eval, animation. Proven "
                 "(measured-on-rig) vs research (study-swarm sourced) is encoded by evidence_strength. Rig-measured "
                 "engine receipts stay in tensor-engine, referenced via engine_recipe_ref; base weights via "
                 "base_model_slug -> model-knowledge; never restated.",
    }
    for k, vv in meta.items():
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (k, vv))
    set_meta_currency(cur)  # latest_wave = MAX(wave_number), updated = that wave's date

    con.commit()
    print(f"wave {wave_no}: {n_rec} recipes, {n_hp} hparams, {n_fail} failures, "
          f"{n_eval} evals, {n_src} sources.")
    for r in cur.execute(
        """SELECT c.name, COUNT(*), COALESCE(SUM(r.verified),0)
           FROM recipes r JOIN categories c ON c.id=r.category_id
           WHERE r.wave_id=? GROUP BY c.name ORDER BY c.sort""", (wave_id,)):
        print(f"  {r[0]:42s} {r[1]:2d} recipes  ({r[2]} verified)")
    con.close()


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-foundation", "research-raw.json")
    main(p)
