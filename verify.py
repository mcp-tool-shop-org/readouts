#!/usr/bin/env python3
"""verify.py — the deterministic floor for readouts.

This repo had no test suite, no CI and no package manifest, which meant nothing
mechanically checked the one thing it sells: that the generated artifacts are true
about the databases. Every defect below was found by hand or by an audit agent, and
every one of them was silent — plausible output, no error, wrong facts.

Two tiers:

  FAIL  breaks a documented contract or serves wrong data. Blocks publication.
  WARN  a real defect that is known, bounded and recorded. Does not block.

    python verify.py            # run everything
    python verify.py --strict   # WARN counts as FAIL too
    python verify.py --list     # what is checked, and why each check exists
    python verify.py --json     # one JSON object per check: level, check, code, message, hint

Every FAIL and WARN carries a stable code (CODES below) and a hint naming the next step.
Exit 0 clean, 1 on FAIL (or WARN under --strict), 2 if the harness itself broke.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sqlite3
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# Entities that carry sources, per KB DB filename: (entity table, source table, fk column)
ENTITY = {
    "blender.db": ("recipes", "sources", "recipe_id"),
    "findings.db": ("findings", None, None),          # two KBs share this name; resolved below
    "godot.db": ("recipes", "sources", "recipe_id"),
    "models.db": ("models", "sources", "model_id"),
    "engines.db": ("engines", "sources", "engine_id"),
    "recipes.db": ("recipes", "sources", "recipe_id"),
    "training.db": ("techniques", "sources", "technique_id"),
    "xrpl.db": ("capabilities", "sources", "capability_id"),
}

results: list[tuple[str, str, str]] = []   # (level, check, detail)


def ok(check: str, detail: str = "") -> None:
    results.append(("PASS", check, detail))


def fail(check: str, detail: str) -> None:
    results.append(("FAIL", check, detail))


def warn(check: str, detail: str) -> None:
    results.append(("WARN", check, detail))


# Singular of each entity table -> its FK column in the sources table. A generic
# "first column ending in _id" probe picks up `wave_id` instead and silently joins
# entities to waves, which reported 477 false "verified without a source" hits.
FK_FOR = {"recipes": "recipe_id", "findings": "finding_id", "models": "model_id",
          "engines": "engine_id", "techniques": "technique_id",
          "capabilities": "capability_id"}


def entity_fk(entity: str, cols: set[str]) -> str | None:
    fk = FK_FOR.get(entity)
    return fk if fk and fk in cols else None


def kb_dirs() -> list[str]:
    return sorted(glob.glob(os.path.join(ROOT, "*-knowledge")))


def pick_db(kb: str) -> str | None:
    """Largest non-empty DB. A 0-byte sibling once shadowed the real one via glob()[0]."""
    best = None
    for p in sorted(glob.glob(os.path.join(kb, "*.db"))):
        if os.path.getsize(p) and (best is None or os.path.getsize(p) > os.path.getsize(best)):
            best = p
    return best


def entity_of(con: sqlite3.Connection) -> str | None:
    tabs = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    for cand in ("engines", "models", "techniques", "capabilities", "recipes", "findings"):
        if cand in tabs:
            return cand
    return None


# --------------------------------------------------------------------------- checks

def check_no_shadow_db() -> None:
    """A 0-byte .db beside the real one silently zeroed a whole KB on the front door."""
    strays = [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "*-knowledge", "*.db"))
              if os.path.getsize(p) == 0]
    if strays:
        fail("no shadow DB", f"empty .db files present: {', '.join(strays)}")
    else:
        ok("no shadow DB", f"{len(kb_dirs())} KBs, one real DB each")


def check_sqlite_integrity() -> None:
    bad = []
    for kb in kb_dirs():
        db = pick_db(kb)
        if not db:
            continue
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            bad.append(f"{os.path.basename(kb)}: integrity_check")
        if con.execute("PRAGMA foreign_key_check").fetchall():
            bad.append(f"{os.path.basename(kb)}: foreign_key_check")
        con.close()
    fail("sqlite integrity", "; ".join(bad)) if bad else ok("sqlite integrity", "all DBs ok")


def check_fts_alignment() -> None:
    """THE critical one.

    The documented access path is MATCH the index, then join the base row by rowid.
    Every loader used to omit `rowid` from its FTS INSERT, so FTS5 assigned its own
    sequential ids. Where the base ids were not 1..N contiguous the join returned
    nothing (blender, sprites, xrpl — 758 entries) and where rows had been deleted the
    index was SHIFTED, so 85 of tensor-engine's 171 rows resolved to the wrong engine.
    Row counts matched throughout, so count parity never caught it.
    """
    bad, checked = [], 0
    for kb in kb_dirs():
        db = pick_db(kb)
        if not db:
            continue
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        con.text_factory = lambda b: b.decode("utf-8", "replace")
        tabs = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        fts = next((t for t in sorted(tabs) if t.endswith("_fts")), None)
        if not fts or fts[:-4] not in tabs:
            con.close()
            continue
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
        checked += 1
        if joined != n:
            bad.append(f"{os.path.basename(kb)}: {joined}/{n} rowids join")
        elif wrong:
            bad.append(f"{os.path.basename(kb)}: {wrong} rows resolve to the WRONG record")
    fail("FTS rowid alignment", "; ".join(bad)) if bad else \
        ok("FTS rowid alignment", f"{checked} indexes, every rowid resolves to its own row")


def check_verified_has_source() -> None:
    """A verified entry with no evidence is the claim this repo exists to not make."""
    bad = []
    for kb in kb_dirs():
        db = pick_db(kb)
        if not db:
            continue
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        ent = entity_of(con)
        tabs = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        src = "sources" if "sources" in tabs else ("finding_sources" if "finding_sources" in tabs else None)
        if not ent or not src:
            con.close()
            continue
        cols = {r[1] for r in con.execute(f"PRAGMA table_info({src})")}
        fk = entity_fk(ent, cols)
        if not fk or "verified" not in {r[1] for r in con.execute(f"PRAGMA table_info({ent})")}:
            con.close()
            continue
        n = con.execute(
            f"SELECT COUNT(*) FROM {ent} e WHERE e.verified=1 AND NOT EXISTS "
            f"(SELECT 1 FROM {src} s WHERE s.{fk}=e.id)").fetchone()[0]
        con.close()
        if n:
            bad.append(f"{os.path.basename(kb)}: {n}")
    fail("verified implies a source", "; ".join(bad)) if bad else \
        ok("verified implies a source", "no verified entry lacks a source")


def check_entries_have_sources() -> None:
    bad = []
    for kb in kb_dirs():
        db = pick_db(kb)
        if not db:
            continue
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        ent = entity_of(con)
        tabs = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        src = "sources" if "sources" in tabs else ("finding_sources" if "finding_sources" in tabs else None)
        if not ent or not src:
            con.close()
            continue
        cols = {r[1] for r in con.execute(f"PRAGMA table_info({src})")}
        fk = entity_fk(ent, cols)
        if not fk:
            con.close()
            continue
        n = con.execute(
            f"SELECT COUNT(*) FROM {ent} e WHERE NOT EXISTS "
            f"(SELECT 1 FROM {src} s WHERE s.{fk}=e.id)").fetchone()[0]
        con.close()
        if n:
            bad.append(f"{os.path.basename(kb)}: {n}")
    warn("every entry has a source", "; ".join(bad)) if bad else \
        ok("every entry has a source", "no unsourced entries")


def check_meta_wave() -> None:
    bad = []
    for kb in kb_dirs():
        db = pick_db(kb)
        if not db:
            continue
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        tabs = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if {"meta", "waves"} <= tabs:
            row = con.execute("SELECT value FROM meta WHERE key='latest_wave'").fetchone()
            mx = con.execute("SELECT MAX(wave_number) FROM waves").fetchone()[0]
            if row and mx is not None and str(row[0]) != str(mx):
                bad.append(f"{os.path.basename(kb)}: meta says {row[0]}, waves max is {mx}")
        con.close()
    fail("meta.latest_wave current", "; ".join(bad)) if bad else \
        ok("meta.latest_wave current", "matches MAX(wave_number) everywhere")


def check_front_door_counts() -> None:
    """index.json is generated from the DBs; drift means the front door is lying."""
    idx = os.path.join(ROOT, "index.json")
    if not os.path.isfile(idx):
        fail("front door matches DBs", "index.json missing")
        return
    claimed = {k["kb"]: k for k in json.load(open(idx, encoding="utf-8"))["knowledge_bases"]}
    bad = []
    for kb in kb_dirs():
        name = os.path.basename(kb)
        db = pick_db(kb)
        if not db or name not in claimed:
            continue
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        ent = entity_of(con)
        if ent:
            n = con.execute(f"SELECT COUNT(*) FROM {ent}").fetchone()[0]
            v = con.execute(f"SELECT COUNT(*) FROM {ent} WHERE verified=1").fetchone()[0]
            if n != claimed[name]["entries"] or v != claimed[name]["verified"]:
                bad.append(f"{name}: DB {v}/{n} vs index {claimed[name]['verified']}"
                           f"/{claimed[name]['entries']}")
        con.close()
    fail("front door matches DBs", "; ".join(bad)) if bad else \
        ok("front door matches DBs", f"{len(claimed)} KBs reconcile")


def check_readme_table() -> None:
    r = subprocess.run([sys.executable, os.path.join(ROOT, "shared", "sync_readme_table.py"), "--check"],
                       capture_output=True, text=True,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"))
    fail("README table current", "stale — run shared/sync_readme_table.py") if r.returncode else \
        ok("README table current", "matches index.json")


def check_dead_links() -> None:
    md_link = re.compile(r"\[[^\]]*\]\(([^)#\s]+)\)")
    bad = []
    for dp, dn, fn in os.walk(ROOT):
        # site/ is the published repo's landing page and handbook. Its pages link by
        # URL (Starlight serves page.md at page/), not by file, so a file-relative
        # check misreads every correct link; shared/export_public.py checks them.
        # The private repo keeps the same tree at public/site/.
        skip = {".git", "__pycache__", ".swarm", "node_modules"}
        if os.path.normpath(dp) in (os.path.normpath(ROOT), os.path.join(ROOT, "public")):
            skip.add("site")
        dn[:] = [d for d in dn if d not in skip]
        # The export publishes public/X at X, so an overlay file's links are written for
        # the published root. Resolve them there as well: read from public/, every
        # README translation's link to a KB folder looked dead (160 of them).
        rel_dp = os.path.relpath(dp, ROOT)
        published = (os.path.join(ROOT, os.path.relpath(dp, os.path.join(ROOT, "public")))
                     if rel_dp == "public" or rel_dp.startswith("public" + os.sep) else None)
        for name in fn:
            if not name.endswith(".md"):
                continue
            p = os.path.join(dp, name)
            try:
                body = open(p, encoding="utf-8").read()
            except (OSError, UnicodeDecodeError):
                continue
            for target in md_link.findall(body):
                if target.startswith(("http://", "https://", "mailto:", "#", "//")):
                    continue
                if re.match(r"^[A-Za-z]:[\\/]", target):
                    continue  # absolute rig path — a separate finding, not a dead link
                if not os.path.exists(os.path.normpath(os.path.join(dp, target))) and not (
                        published and os.path.exists(os.path.normpath(os.path.join(published, target)))):
                    bad.append(f"{os.path.relpath(p, ROOT)} -> {target}")
    if bad:
        fail("no dead relative links", f"{len(bad)}: " + "; ".join(bad[:6]))
    else:
        ok("no dead relative links", "every relative markdown link resolves")


def check_duplicate_slugs() -> None:
    """`uniq_slug` appends -2 on collision, so a re-ingest silently forks an entry."""
    bad = []
    for kb in kb_dirs():
        db = pick_db(kb)
        if not db:
            continue
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        con.text_factory = lambda b: b.decode("utf-8", "replace")
        ent = entity_of(con)
        if ent:
            slugs = {r[0] for r in con.execute(f"SELECT slug FROM {ent}")}
            forked = [s for s in slugs if re.search(r"-[2-9]$", s) and re.sub(r"-[2-9]$", "", s) in slugs]
            if forked:
                bad.append(f"{os.path.basename(kb)}: {len(forked)}")
        con.close()
    warn("no collision-forked slugs", "; ".join(bad)) if bad else \
        ok("no collision-forked slugs", "no entry forked by a uniq_slug suffix")



def check_verified_is_external() -> None:
    """`verified` must trace to an EXTERNAL verdict, never the author's own field.

    The strong form of the invariant: the count of verified entries in the DB must
    equal what shared/verdicts.py resolves from the wave files and the ledger. If a
    loader ever reintroduces a self-report path, the two diverge and this fails.
    """
    sys.path.insert(0, os.path.join(ROOT, "shared"))
    try:
        from verdicts import Verdicts, lane_items  # noqa: PLC0415
    except Exception as exc:
        fail("verified is external", f"shared/verdicts.py unusable: {exc}")
        return
    import re as _re
    bad = []
    for kb in kb_dirs():
        name = os.path.basename(kb)
        db = pick_db(kb)
        waves = sorted(glob.glob(os.path.join(kb, "waves", "*", "research-raw.json")))
        if not db or not waves:
            continue
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        ent = entity_of(con)
        cols = {r[1] for r in con.execute(f"PRAGMA table_info({ent})")} if ent else set()
        if not ent or "verified" not in cols:
            con.close()
            continue
        namecol = "name" if "name" in cols else ("title" if "title" in cols else None)
        sel = f"SELECT slug, {namecol} FROM {ent} WHERE verified=1" if namecol else               f"SELECT slug, '' FROM {ent} WHERE verified=1"
        db_rows = list(con.execute(sel))
        con.close()

        # Every slug/name an EXTERNAL verdict grants verified=1 — the durable ledger
        # plus each wave lane's own verifier block.
        res = Verdicts(kb)
        granted_slugs = {s for s, v in (res.ledger or {}).items() if int(v.get("verified", 0))}
        granted_names = set()
        for w in waves:
            try:
                data = json.load(open(w, encoding="utf-8"))
            except Exception:
                continue
            for lane in data.get("lanes", []):
                res.use_lane(lane)
                for idx, item in enumerate(lane_items(lane), 1):
                    nm = item.get("name") or item.get("title") or ""
                    slug = item.get("slug") or ""
                    if not slug:
                        base = f"{item.get('n', idx)}-{nm}" if item.get("n") else nm
                        slug = _re.sub(r"[^a-z0-9]+", "-", base.strip().lower()).strip("-")[:80]
                    if res.for_entry(slug, nm)[0]:
                        granted_slugs.add(slug)
                        if nm:
                            granted_names.add(nm.strip().lower())

        # A loader may fork a colliding slug to `<base>-2`; de-fork before judging.
        orphans = []
        for slug, nm in db_rows:
            base = _re.sub(r"-\d+$", "", slug or "")
            if (slug in granted_slugs or base in granted_slugs
                    or (nm or "").strip().lower() in granted_names):
                continue
            orphans.append(slug or nm)
        if orphans:
            shown = "; ".join(orphans[:3]) + (f"; +{len(orphans) - 3} more" if len(orphans) > 3 else "")
            bad.append(f"{name}: {len(orphans)} verified row(s) with no external verdict ({shown})")
    fail("verified is external", "; ".join(bad)) if bad else         ok("verified is external", "every verified row traces to an external verdict")


def check_source_flag_independent() -> None:
    """sources.verified must be a check, not a copy of the parent's verdict.

    Stamping the entity's verdict onto every source gave 100.0%% agreement across
    934 rows in two KBs and read as a second, independent seat. NULL now means
    unchecked, and a perfect correlation is treated as evidence of a copy.
    """
    bad = []
    for kb in kb_dirs():
        db = pick_db(kb)
        if not db:
            continue
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        ent = entity_of(con)
        tabs = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        src = "sources" if "sources" in tabs else ("finding_sources" if "finding_sources" in tabs else None)
        if not ent or not src:
            con.close()
            continue
        scols = {r[1] for r in con.execute(f"PRAGMA table_info({src})")}
        flag = "verified" if "verified" in scols else ("exists_verified" if "exists_verified" in scols else None)
        fk = entity_fk(ent, scols)
        if not flag or not fk:
            con.close()
            continue
        rows = con.execute(
            f"SELECT COUNT(*), SUM(CASE WHEN s.{flag}=e.verified THEN 1 ELSE 0 END) "
            f"FROM {src} s JOIN {ent} e ON e.id=s.{fk} WHERE s.{flag} IS NOT NULL").fetchone()
        con.close()
        n, same = rows[0] or 0, rows[1] or 0
        if n >= 50 and same == n:
            bad.append(f"{os.path.basename(kb)}: {n}/{n} match the parent exactly")
    warn("source flag is independent", "; ".join(bad)) if bad else         ok("source flag is independent", "no KB's source flag mirrors its parent verdict")


CHECKS = [
    ("no shadow DB", check_no_shadow_db),
    ("sqlite integrity", check_sqlite_integrity),
    ("FTS rowid alignment", check_fts_alignment),
    ("verified implies a source", check_verified_has_source),
    ("verified is external", check_verified_is_external),
    ("source flag is independent", check_source_flag_independent),
    ("meta.latest_wave current", check_meta_wave),
    ("front door matches DBs", check_front_door_counts),
    ("README table current", check_readme_table),
    ("no dead relative links", check_dead_links),
    ("every entry has a source", check_entries_have_sources),
    ("no collision-forked slugs", check_duplicate_slugs),
]

# A stable code and a next step for every check that can fail or warn. Codes are part
# of the output contract: rename one only with a CHANGELOG entry.
CODES = {
    "no shadow DB": ("STATE_SHADOW_DB",
                     "Delete the empty .db file; each KB keeps one real database."),
    "sqlite integrity": ("STATE_DB_CORRUPT",
                         "Restore the KB's .db from git, or rebuild it from its wave files."),
    "FTS rowid alignment": ("STATE_FTS_MISALIGNED",
                            "Run `python shared/rebuild_fts.py`, then re-run this."),
    "verified implies a source": ("STATE_VERIFIED_UNSOURCED",
                                  "Add the entry's sources, or clear verified, then rebuild the KB."),
    "verified is external": ("STATE_VERIFIED_NOT_EXTERNAL",
                             "verified=1 needs an external verdict in the KB's verification/verdicts.json."),
    "source flag is independent": ("STATE_SOURCE_FLAG_COPIED",
                                   "Known and recorded: these source flags copy the entry's verdict."),
    "meta.latest_wave current": ("STATE_META_STALE",
                                 "Rebuild the KB (its scripts/regen.py, where it has one)."),
    "front door matches DBs": ("STATE_FRONT_DOOR_STALE",
                               "Run `python shared/gen_root_index.py`."),
    "README table current": ("STATE_README_TABLE_STALE",
                             "Run `python shared/sync_readme_table.py`."),
    "no dead relative links": ("IO_DEAD_LINK",
                               "Fix the link, or restore the file it points at."),
    "every entry has a source": ("STATE_ENTRY_UNSOURCED",
                                 "Known and recorded: the next wave for that KB adds sources."),
    "no collision-forked slugs": ("STATE_SLUG_FORKED",
                                  "Known and recorded: a colliding slug gets a -2 suffix on load, "
                                  "so review the pairs before re-ingesting a wave."),
}
HARNESS = ("RUNTIME_CHECK_CRASHED", "A check raised instead of reporting; this is a bug in verify.py.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--strict", action="store_true", help="treat WARN as FAIL")
    ap.add_argument("--list", action="store_true", help="list the checks and exit")
    ap.add_argument("--json", action="store_true",
                    help="print one JSON object per check: level, check, code, message, hint")
    args = ap.parse_args()

    if args.list:
        for name, fn in CHECKS:
            doc = (fn.__doc__ or "").strip().split("\n")[0] or "—"
            print(f"  {name:<30} {doc}")
        return 0

    for _, fn in CHECKS:
        try:
            fn()
        except Exception as exc:                      # a broken check is not a pass
            results.append(("ERROR", fn.__name__, f"{type(exc).__name__}: {exc}"))

    errors = sum(1 for l, _, _ in results if l == "ERROR")
    fails = sum(1 for l, _, _ in results if l == "FAIL") + errors
    warns = sum(1 for l, _, _ in results if l == "WARN")

    if args.json:
        for level, check, detail in results:
            code, hint = HARNESS if level == "ERROR" else CODES.get(check, ("", ""))
            row = {"level": level, "check": check, "message": detail}
            if level != "PASS":
                row.update(code=code, hint=hint, retryable=False)
            print(json.dumps(row, ensure_ascii=False))
        return 2 if errors else 1 if fails or (warns and args.strict) else 0

    width = max(len(c) for _, c, _ in results)
    for level, check, detail in results:
        mark = {"PASS": "ok  ", "WARN": "warn", "FAIL": "FAIL", "ERROR": "ERR "}[level]
        if level == "PASS":
            print(f"  {mark}  {check:<{width}}  {detail}")
            continue
        code, hint = HARNESS if level == "ERROR" else CODES.get(check, ("", ""))
        print(f"  {mark}  {check:<{width}}  [{code}] {detail}")
        print(f"        {'':<{width}}  hint: {hint}")

    print(f"\n{len(results)} checks — {fails} failing, {warns} warning")
    if errors:
        print("::error:: a check crashed — the harness is broken, fix verify.py first")
        return 2
    if fails:
        print("::error:: verification FAILED — do not publish")
        return 1
    if warns and args.strict:
        print("::error:: warnings present and --strict was given")
        return 1
    if warns:
        print("Clean on every blocking check; warnings are known and recorded.")
    else:
        print("Clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
