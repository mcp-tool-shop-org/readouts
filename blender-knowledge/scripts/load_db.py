#!/usr/bin/env python3
"""Ingest a Blender-knowledge study-swarm wave's research-raw.json into blender-knowledge/blender.db.

Idempotent per wave: deletes existing rows for the wave_number before inserting, so re-running a
wave cleanly replaces it and leaves other waves untouched.

research-raw.json shape (the contract the wave swarm produces):
{
  "wave": <int>, "date": "YYYY-MM-DD", "title": "...", "domain_scope": "...",
  "agent_count": <int>, "verifier_note": "...",
  "lanes": [{
    "laneSlug": "<categories.slug>", "title": "...",
    "recipes": [{
      slug, name, what, how, blender_version, gotchas, studio_use,
      currency,        # solid | plausible | shaky | blender3_stale | wrong  (the adversarial verdict)
      verify_note, verified, status,
      sources: [{ title, url, claim, verified }]
    }]
  }]
}

Run with UTF-8 forced on Windows (entries carry em-dashes):
    $env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'; python scripts/load_db.py waves/wave-01-foundation/research-raw.json
"""
import json
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "blender.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

# One definition of `verified`, shared by every KB — see shared/verdicts.py.
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "shared"))
from verdicts import Verdicts  # noqa: E402


VERIFIED_VERDICTS = {"solid", "plausible"}
STATUS_BY_CURRENCY = {"solid": "recommended", "plausible": "recommended", "shaky": "situational",
                      "blender3_stale": "avoid", "wrong": "avoid"}


def slugify(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "x"


def uniq_slug(cur, base):
    s, k = base, 2
    while cur.execute("SELECT 1 FROM recipes WHERE slug=?", (s,)).fetchone():
        s, k = f"{base}-{k}", k + 1
    return s


def b(v):
    if v in (True, 1):
        return 1
    if v in (False, 0):
        return 0
    if isinstance(v, str) and v.strip().lower() in ("yes", "true", "1", "solid", "plausible"):
        return 1
    return 0


def txt(v):
    """Coerce list-valued fields (some research agents emit gotchas/how/studio_use as arrays) to one string."""
    if isinstance(v, list):
        return "; ".join(str(x) for x in v if x not in (None, ""))
    return v


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if "lanes" not in data and isinstance(data.get("result"), dict):  # tolerate harness envelope
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
    VERD = Verdicts(ROOT)

    row = cur.execute("SELECT id FROM waves WHERE wave_number=?", (wave_no,)).fetchone()
    if row:
        wave_id = row[0]
        cur.execute("DELETE FROM recipes WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM sources WHERE wave_id=?", (wave_id,))
        cur.execute(
            "UPDATE waves SET title=?, dispatched_date=?, domain_scope=?, agent_count=?, verifier_note=?, "
            "status='synthesized' WHERE id=?",
            (title, date, data.get("domain_scope"), data.get("agent_count"), data.get("verifier_note"), wave_id))
    else:
        cur.execute(
            """INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path)
               VALUES(?,?,?,?,?,?,?,?)""",
            (wave_no, title, date, data.get("domain_scope"), data.get("agent_count") or len(lanes),
             data.get("verifier_note") or "Adversarial Blender-4-currency verifier per lane (web-grounded; flags "
             "Blender-3 staleness, deprecated nodes, version-wrong APIs). Default unverified on non-confirmation.",
             "synthesized", f"waves/{os.path.basename(os.path.dirname(os.path.abspath(path)))}/dispatch.md"))
        wave_id = cur.lastrowid

    cat = {s: i_ for s, i_ in cur.execute("SELECT slug,id FROM categories")}
    n_rec = n_src = 0

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
            name = t.get("name") or t.get("title")
            rslug = uniq_slug(cur, slugify(t.get("slug") or name))
            currency = ((t.get("currency") or "").strip().lower()) or None
            # `verified` is external-only now. "plausible" is the adversarial
            # verdict for "could not falsify", never "checked out", and the old
            # else-branch read the research agent's own field.
            verified, vstatus, vnote, _ = VERD.for_entry(rslug, name)
            # Keep the entry's own evidence note AND who decided the flag —
            # the note says what was checked, the tally says by whom.
            own = txt(t.get("verify_note"))
            vnote = f"{own} [{vnote}]" if own else vnote
            status = ("avoid" if vstatus == "avoid"
                      else t.get("status") or STATUS_BY_CURRENCY.get(currency or ""))
            cur.execute(
                """INSERT INTO recipes(slug,name,category_id,what,how,blender_version,gotchas,studio_use,
                   currency,verify_note,verified,status,wave_id,created_date)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (rslug, name, category_id, txt(t.get("what")), txt(t.get("how")), txt(t.get("blender_version")),
                 txt(t.get("gotchas")), txt(t.get("studio_use")), currency, vnote,
                 verified, status, wave_id, date))
            rid = cur.lastrowid
            n_rec += 1
            for s in (t.get("sources") or []):
                if not s.get("url"):
                    continue
                cur.execute("INSERT INTO sources(recipe_id,title,url,claim,verified,wave_id) VALUES(?,?,?,?,?,?)",
                            (rid, s.get("title"), s.get("url"), s.get("claim"), b(s.get("verified")), wave_id))
                n_src += 1

    cur.execute("DELETE FROM recipes_fts")
    cur.execute(
        """INSERT INTO recipes_fts(rowid,slug,name,what,how,gotchas,studio_use,category)
           SELECT r.id, r.slug, r.name, COALESCE(r.what,''), COALESCE(r.how,''), COALESCE(r.gotchas,''),
                  COALESCE(r.studio_use,''), COALESCE((SELECT name FROM categories c WHERE c.id=r.category_id),'')
           FROM recipes r""")

    latest = max([w[0] for w in cur.execute("SELECT wave_number FROM waves")] or [wave_no])
    updated = cur.execute("SELECT dispatched_date FROM waves ORDER BY wave_number DESC LIMIT 1").fetchone()[0]
    meta = {
        "kb_name": "blender-knowledge",
        "scope": "Current Blender-4.x practice for the studio's HEADLESS sprite-turnaround render pipeline "
                 "(import a TRELLIS GLB -> render 8-direction sprites via `blender --background --python` -> 2.5D "
                 "game) plus game-asset prep: headless/bpy scripting, EEVEE Next/Cycles render engines, color "
                 "management, import/export (glTF/FBX/OBJ/USD), lighting & camera rigs, mesh cleanup, materials & "
                 "baking, geometry nodes, rigging/animation, and add-ons. DECISIVE AXIS = Blender-4.x CURRENCY (the "
                 "adversarial verdict; flags Blender-3 staleness). A code/practice KB — license/VRAM/rig-fit do not apply.",
        "latest_wave": str(latest),
        "updated": updated,
    }
    for k, vv in meta.items():
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (k, vv))

    con.commit()
    print(f"wave {wave_no}: {n_rec} recipes, {n_src} sources.")
    for r in cur.execute(
        """SELECT c.name, COUNT(*), COALESCE(SUM(rec.verified),0)
           FROM recipes rec JOIN categories c ON c.id=rec.category_id
           WHERE rec.wave_id=? GROUP BY c.name ORDER BY c.sort""", (wave_id,)):
        print(f"  {r[0]:34s} {r[1]:2d} recipes  ({r[2]} verified)")
    con.close()


if __name__ == "__main__":
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-foundation", "research-raw.json")
    main(p)
