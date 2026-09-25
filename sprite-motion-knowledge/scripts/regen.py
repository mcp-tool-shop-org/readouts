#!/usr/bin/env python3
"""regen.py — regenerate EVERY derived artifact from recipes.db.

Discovers wave files under waves/*/research-raw.json (sorted) and ingests each via load_db.py,
then rebuilds the catalog and the KB's own loadout, then refreshes the ROOT routers, then validates.

The pillars rebuilt from the single source of truth (recipes.db):
  data    : recipes.db                          (load_db.py ingests each wave's research-raw.json)
  meta    : latest_wave/updated                 (refresh_meta.py, derived from MAX(wave))
  catalog : catalog/*.md                         (gen_catalog.py)
  index   : .claude/loadout/index.json (+root)   (gen_loadout.py + ../shared/gen_root_loadout.py)
  root    : ../index.{html,md,json}              (../shared/gen_root_index.py)   <- monorepo front door
  output  : readout/*.html + index.{md,json}     (shared gen_readout.py / gen_index.py) — best-effort,
            skipped unless a readout profile exists for recipes.db

One command, idempotent — same DB in, byte-identical artifacts out (modulo the generated date stamp).

Usage:  python scripts/regen.py
"""
import glob
import os
import shutil
import sqlite3
import subprocess
import sys

try:  # parent console may be cp1252 (Win/py3.14); keep our own prints UTF-8 + ordered vs subprocess output
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # import sibling scripts (refresh_meta)
from refresh_meta import verify_meta, MetaDriftError, DB
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = sys.executable
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")


def run(label, cmd, required=True):
    print(f"\n› {label}")
    r = subprocess.run(cmd, env=ENV)
    if r.returncode != 0:
        if required:
            sys.exit(f"✗ FAILED at: {label}  ({' '.join(cmd)})")
        print(f"  (non-fatal: {label} returned {r.returncode} — skipping)")


def main():
    # fresh rebuild from the wave files (the source of truth): avoids cross-wave predecessor-FK
    # delete-order errors + stale companion rows. recipes.db is fully derived, so dropping it is safe.
    for _f in glob.glob("recipes.db*"):
        try:
            os.remove(_f)
        except OSError:
            pass
    # 1. ingest every wave (sorted) — idempotent per wave
    waves = sorted(glob.glob(os.path.join("waves", "*", "research-raw.json")))
    if waves:
        for w in waves:
            run(f"load_db  ({w})", [PY, "scripts/load_db.py", w])
    else:
        print("\n› load_db  (no waves/*/research-raw.json yet — DB stays schema-only, categories seeded)")

    # 2. meta FIRST (self-heal the currency pointer before generators read it) — only if a wave exists
    if waves:
        run("meta     (DB -> latest_wave/updated, derived from MAX(wave))", [PY, "scripts/refresh_meta.py"])

    # 3. catalog + KB loadout
    run("catalog  (DB -> catalog/*.md)", [PY, "scripts/gen_catalog.py"])
    run("loadout  (DB -> .claude/loadout/index.json)", [PY, "scripts/gen_loadout.py"])

    # 4. shared readout/index/reports — profile-driven; best-effort (skips if recipes.db has no profile)
    run("readouts (DB -> readout/readout-*.html)", [PY, "../shared/gen_readout.py"], required=False)
    run("index    (DB -> readout/index.{html,md,json})", [PY, "../shared/gen_index.py"], required=False)
    run("reports  (DB -> readout/waves+verification.{html,md})", [PY, "../shared/gen_reports.py"], required=False)

    # 5. root routers (these MUST recognize a recipes-table KB)
    run("root     (-> ../.claude/loadout/index.json)", [PY, "../shared/gen_root_loadout.py"])
    run("root idx (-> ../index.{html,md,json})", [PY, "../shared/gen_root_index.py"])

    # 6. validate both loadout indexes (ai-loadout is a global CLI; best-effort)
    al = shutil.which("ai-loadout")
    print("\n› validate (ai-loadout)")
    if al:
        for idx in [".claude/loadout/index.json", "../.claude/loadout/index.json"]:
            subprocess.run([al, "validate", idx], env=ENV)
    else:
        print("  (ai-loadout not on PATH — skipping validate; run it manually)")

    # 7. final end-state guard: meta.latest_wave MUST equal MAX(waves.wave_number) (only meaningful once loaded)
    if waves:
        print("\n› verify   (meta.latest_wave == MAX(waves.wave_number))")
        con = sqlite3.connect(DB)
        try:
            verify_meta(con.cursor())
        except MetaDriftError as e:
            con.close()
            sys.exit(f"✗ FAILED at: meta drift verify — {e}")
        finally:
            con.close()
        print("  ok")

    print("\n✓ regen complete — artifacts rebuilt from recipes.db")


if __name__ == "__main__":
    main()
