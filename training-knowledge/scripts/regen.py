#!/usr/bin/env python3
"""regen.py — regenerate EVERY derived artifact from training.db. Run after a wave's load_db.py.

The four pillars rebuilt from the single source of truth (training.db):
  data    : training.db                        (load_db.py ingests a wave's research-raw.json — run separately)
  catalog : catalog/*.md                       (gen_catalog.py)
  output  : readout/*.html + index.{md,json}   (shared gen_readout.py [all domains] + gen_index.py)  <- product face
  index   : .claude/loadout/index.json (+root)  (gen_loadout.py + ../shared/gen_root_loadout.py)
  root    : ../index.{html,md,json}            (../shared/gen_root_index.py)                          <- monorepo front door

One command, idempotent — same DB in, byte-identical artifacts out (modulo the generated date stamp).

Usage:  python scripts/load_db.py waves/wave-NN/research-raw.json   # ingest the wave
        python scripts/regen.py                                     # rebuild everything
"""
import subprocess, sys, os, shutil, sqlite3
try:  # parent console may be cp1252 (Win/py3.14); make our own prints UTF-8 + ordered vs subprocess output
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # import sibling scripts (refresh_meta)
from refresh_meta import verify_meta, MetaDriftError, DB
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = sys.executable
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")

STEPS = [
    # FIRST + non-skippable: re-derive meta.latest_wave/updated from MAX(waves.wave_number)
    # so every regen self-heals the currency pointer BEFORE the generators read it.
    ("meta     (DB -> latest_wave/updated, derived from MAX(wave))", [PY, "scripts/refresh_meta.py"]),
    ("catalog  (DB -> catalog/*.md)",            [PY, "scripts/gen_catalog.py"]),
    ("readouts (DB -> readout/readout-*.html)",  [PY, "../shared/gen_readout.py"]),       # shared, profile-driven, all domains
    ("index    (DB -> readout/index.{html,md,json})", [PY, "../shared/gen_index.py"]),     # shared, profile-driven
    ("reports  (DB -> readout/waves+verification.{html,md})", [PY, "../shared/gen_reports.py"]),  # dispatch + receipt
    ("loadout  (DB -> .claude/loadout/index.json)", [PY, "scripts/gen_loadout.py"]),
    ("root     (-> ../.claude/loadout/index.json)", [PY, "../shared/gen_root_loadout.py"]),
    ("root idx (-> ../index.{html,md,json})",       [PY, "../shared/gen_root_index.py"]),   # monorepo front door
    ("curric   (DB -> curriculum.json for role-os S6 training programs)", [PY, "scripts/gen_curriculum.py"]),
]

def run(label, cmd):
    print(f"\n› {label}")
    r = subprocess.run(cmd, env=ENV)
    if r.returncode != 0:
        sys.exit(f"✗ FAILED at: {label}  ({' '.join(cmd)})")

def main():
    for label, cmd in STEPS:
        run(label, cmd)
    # validate both loadout indexes (ai-loadout is a global CLI; best-effort)
    al = shutil.which("ai-loadout")
    print("\n› validate (ai-loadout)")
    if al:
        for idx in [".claude/loadout/index.json", "../.claude/loadout/index.json"]:
            subprocess.run([al, "validate", idx], env=ENV)
    else:
        print("  (ai-loadout not on PATH — skipping validate; run it manually)")
    # Final end-state guard: meta.latest_wave MUST equal MAX(waves.wave_number).
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
    print("\n✓ regen complete — all four pillars rebuilt from training.db")

if __name__ == "__main__":
    main()
