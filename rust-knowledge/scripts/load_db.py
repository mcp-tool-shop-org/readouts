#!/usr/bin/env python3
"""Ingest a rust-knowledge wave's research-raw.json into rust-knowledge/rust.db.

Idempotent per wave: deletes the wave's rows (recipes, checks, sources) before inserting, so
re-running a wave cleanly replaces it and leaves other waves untouched.

research-raw.json shape (written by scripts/assemble_lanes.py --final, never by hand):
{
  "wave": <int>, "date": "YYYY-MM-DD", "title": "...", "domain_scope": "...",
  "agent_count": <int>, "verifier_note": "...",
  "lanes": [{
    "laneSlug": "<categories.slug>", "title": "...", "tier": "...",
    "recipes": [{
      slug, name, what, how, rust_version, gotchas, engine_note,
      currency,                       # the verifier's verdict (solid|plausible|shaky|stale|wrong)
      verify_note,
      compile_status, compile_note,   # the compiler's verdict (pass|fail|none)
      checks: [{label, edition, target, crate_type, deps, rustc_flags, expect, error_codes, lints,
                stdout, source, oracle: {ok, note, rustc}}],
      sources: [{title, url, claim, year, kind, identifier, verified}],   # verified = per-source check
      background_sources: [...]
    }]
  }]
}

`verified` on a recipe is NOT read from this file. It comes from verification/verdicts.json through
shared/verdicts.py (the external verdict) — built by scripts/build_ledger.py, which also applies the
compile gate. A flag the research agent set about its own output is a restatement, not a check.

Run with UTF-8 forced on Windows:
    $env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'; python scripts/load_db.py waves/wave-01-essentials/research-raw.json
"""
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "rust.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "shared"))
from verdicts import Verdicts, note_with_corrections  # noqa: E402

STATUS_BY_CURRENCY = {"solid": "recommended", "plausible": "recommended", "shaky": "situational",
                      "stale": "avoid", "wrong": "avoid"}
SCOPE = ("Rust for building si-rpg-engine and si-jam-sessions, in four tiers: essentials (ownership, types, traits, errors, "
         "collections, Cargo, testing), advanced (type system, memory and layout, unsafe and FFI, concurrency, "
         "macros and const, performance, what changed in 1.80-1.98), si-rpg-engine (raw wasm ABI, float "
         "determinism, Rapier 0.35 pipeline, restore internals, shapes and the character controller, binary "
         "lint and limits, simulation architecture, host embedding, CI and reproducible bytes), and si-jam-sessions "
         "(score ingest inside a wasm law, integer musical time, the native audio and MIDI host, crate licences). "
         "DECISIVE AXES = "
         "currency against Rust 1.98.1 / edition 2024 / pinned crates (adversarial verifier) AND every code "
         "check run by the pinned compiler (a non-model verifier).")


def tri(v):
    """Per-source flag: True -> 1, False -> 0, anything else -> NULL (unchecked)."""
    if v is True or v == 1:
        return 1
    if v is False or v == 0:
        return 0
    return None


def jdump(v):
    return json.dumps(v or [], ensure_ascii=False)


# Check keys with a column of their own; any other key the wave file carries is a gate (checks.gates).
CHECK_COLUMNS = {"label", "edition", "target", "crate_type", "deps", "rustc_flags", "expect", "error_codes",
                 "lints", "stdout", "source", "oracle"}


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    wave_no = int(data["wave"])
    date = data.get("date", "")
    title = data.get("title") or f"Wave {wave_no}"
    lanes = data.get("lanes", [])

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    with open(SCHEMA, "r", encoding="utf-8") as f:
        con.executescript(f.read())
    # checks.gates arrived after the first build; CREATE TABLE IF NOT EXISTS does not add it to an old DB.
    if "gates" not in {r[1] for r in con.execute("PRAGMA table_info(checks)")}:
        con.execute("ALTER TABLE checks ADD COLUMN gates TEXT")
    cur = con.cursor()
    verd = Verdicts(ROOT)

    row = cur.execute("SELECT id FROM waves WHERE wave_number=?", (wave_no,)).fetchone()
    dispatch_path = f"waves/{os.path.basename(os.path.dirname(os.path.abspath(path)))}/dispatch.md"
    if row:
        wave_id = row[0]
        cur.execute("DELETE FROM checks WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM sources WHERE wave_id=?", (wave_id,))
        cur.execute("DELETE FROM recipes WHERE wave_id=?", (wave_id,))
        cur.execute(
            "UPDATE waves SET title=?, dispatched_date=?, domain_scope=?, agent_count=?, verifier_note=?, "
            "status='synthesized', dispatch_path=? WHERE id=?",
            (title, date, data.get("domain_scope"), data.get("agent_count"), data.get("verifier_note"),
             dispatch_path, wave_id))
    else:
        cur.execute(
            """INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path)
               VALUES(?,?,?,?,?,?,?,?)""",
            (wave_no, title, date, data.get("domain_scope"), data.get("agent_count") or len(lanes),
             data.get("verifier_note"), "synthesized", dispatch_path))
        wave_id = cur.lastrowid

    cat = {s: (i, t) for s, i, t in cur.execute("SELECT slug, id, tier FROM categories")}
    n_rec = n_src = n_chk = 0
    for lane in lanes:
        lslug = lane.get("laneSlug")
        if lslug not in cat:
            sys.exit(f"HALT: lane {lslug!r} has no category row in schema.sql — add it there, do not auto-create")
        category_id, tier = cat[lslug]
        verd.use_lane(lane)
        for t in lane.get("recipes") or []:
            slug, name = t["slug"], t["name"]
            currency = ((t.get("currency") or "").strip().lower()) or None
            verified, vstatus, vnote, corr = verd.for_entry(slug, name)
            # The ledger note already carries the verifier's words (and any compile-gate failure); the
            # wave file's copy is only a fallback for a row the ledger has never seen.
            own = (t.get("verify_note") or "").strip()
            note = vnote if vnote and not vnote.startswith("no external verdict") else (own or vnote)
            note = note_with_corrections(note, corr)
            if vstatus in ("avoid", "directional"):
                status = vstatus
            else:
                status = STATUS_BY_CURRENCY.get(currency or "", "directional")
            cur.execute(
                """INSERT INTO recipes(slug,name,category_id,tier,what,how,rust_version,gotchas,engine_note,
                   currency,verify_note,verified,status,compile_status,compile_note,wave_id,created_date)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (slug, name, category_id, tier, t.get("what"), t.get("how"), t.get("rust_version"),
                 t.get("gotchas"), (t.get("engine_note") or "").strip() or None, currency, note, verified,
                 status, t.get("compile_status") or "none", t.get("compile_note"), wave_id, date))
            rid = cur.lastrowid
            n_rec += 1
            for i, c in enumerate(t.get("checks") or []):
                o = c.get("oracle") or {}
                ok = o.get("ok")
                gates = {k: v for k, v in c.items() if k not in CHECK_COLUMNS}
                cur.execute(
                    """INSERT INTO checks(recipe_id,idx,label,edition,target,crate_type,deps,rustc_flags,expect,
                       error_codes,lints,expected_stdout,gates,source,oracle_ok,oracle_note,rustc,wave_id)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (rid, i, c.get("label"), str(c.get("edition") or "2024"), c.get("target") or "host",
                     c.get("crate_type"), jdump(c.get("deps")), jdump(c.get("rustc_flags")), c.get("expect"),
                     jdump(c.get("error_codes")), jdump(c.get("lints")), c.get("stdout"),
                     json.dumps(gates, ensure_ascii=False, sort_keys=True) if gates else None,
                     c.get("source") or "", None if ok is None else (1 if ok else 0), o.get("note"),
                     o.get("rustc"), wave_id))
                n_chk += 1
            for s in t.get("sources") or []:
                if not s.get("url"):
                    continue
                y = s.get("year")
                cur.execute(
                    """INSERT INTO sources(recipe_id,title,url,claim,year,kind,identifier,verified,wave_id)
                       VALUES(?,?,?,?,?,?,?,?,?)""",
                    (rid, s.get("title"), s["url"], s.get("claim"), y if isinstance(y, int) else None,
                     s.get("kind"), s.get("identifier") or None, tri(s.get("verified")), wave_id))
                n_src += 1

    # FTS rowid MUST equal the recipe id (verify.py's critical check).
    cur.execute("DELETE FROM recipes_fts")
    cur.execute(
        """INSERT INTO recipes_fts(rowid,slug,name,what,how,gotchas,engine_note,category)
           SELECT r.id, r.slug, r.name, COALESCE(r.what,''), COALESCE(r.how,''), COALESCE(r.gotchas,''),
                  COALESCE(r.engine_note,''), COALESCE((SELECT name FROM categories c WHERE c.id=r.category_id),'')
           FROM recipes r""")

    latest = cur.execute("SELECT MAX(wave_number) FROM waves").fetchone()[0]
    updated = cur.execute("SELECT dispatched_date FROM waves ORDER BY wave_number DESC LIMIT 1").fetchone()[0]
    for k, v in {"kb_name": "rust-knowledge", "scope": SCOPE, "latest_wave": str(latest), "updated": updated,
                 "toolchain": "rustc 1.98.1 (48a229cea 2026-09-01)",
                 "pinned_crates": "rapier3d-f64 0.35.3 (enhanced-determinism), parry3d-f64 0.30.2"}.items():
        cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (k, v))

    con.commit()
    print(f"wave {wave_no}: {n_rec} recipes, {n_chk} checks, {n_src} sources.")
    for r in cur.execute(
            """SELECT c.name, COUNT(*), COALESCE(SUM(rec.verified),0),
                      SUM(CASE WHEN rec.compile_status='pass' THEN 1 ELSE 0 END),
                      SUM(CASE WHEN rec.compile_status='fail' THEN 1 ELSE 0 END)
               FROM recipes rec JOIN categories c ON c.id=rec.category_id
               WHERE rec.wave_id=? GROUP BY c.id ORDER BY c.sort""", (wave_id,)):
        print(f"  {r[0]:48s} {r[1]:2d} recipes  ({r[2]} verified, {r[3]} compile-pass, {r[4]} compile-fail)")
    con.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python scripts/load_db.py waves/<wave-dir>/research-raw.json")
    main(sys.argv[1])
