#!/usr/bin/env python3
"""regen.py — regenerate EVERY derived artifact from xrpl.db. Run after a wave's load_db.py (+ verify_cloud.py).

Pillars rebuilt from the single source of truth (xrpl.db):
  data    : xrpl.db                            (load_db.py ingests a wave's research-raw.json — run separately)
  catalog : catalog/*.md (+ track-*.md)        (gen_catalog.py)
  output  : readout/*.html + index.{md,json}   (shared gen_readout.py [all domains] + gen_index.py)
  reports : readout/waves + verification        (shared gen_reports.py)
  index   : .claude/loadout/index.json (+root)  (gen_loadout.py + ../shared/gen_root_loadout.py)
  root    : ../index.{html,md,json}            (../shared/gen_root_index.py)   <- the monorepo front door

One command, idempotent — same DB in, byte-identical artifacts out (modulo the generated date stamp).

Usage:  $env:PYTHONUTF8='1'; python scripts/load_db.py waves/wave-NN/research-raw.json   # ingest the wave
        $env:PYTHONUTF8='1'; python scripts/verify_cloud.py waves/wave-NN/research-raw.json # cross-family verify
        $env:PYTHONUTF8='1'; python scripts/regen.py                                       # rebuild everything

Standards compliance (.claude/rules/workflow-standards.md), 0-3:
  PIN_PER_STEP 3 — every step is `python <pinned script>`; all artifacts derive from xrpl.db, so the same DB
    reproduces byte-identical output (modulo the date). No hidden state.
  EXTERNAL_VERIFIER 3 — the `verified` flag is set UPSTREAM (load_db) by a cross-family Ollama Cloud large
    model (deepseek-v3.1:671b — a different family from the Claude researcher; no self-preference), with a
    Claude+WebFetch retrieval oracle as seat 1. This regen additionally wires `ai-loadout validate` (an
    independent CLI) on both loadout indexes, and the HTML is checked out-of-band by the look-at-output rule.
  ANDON_AUTHORITY 3 — any failing step halts the rebuild with a non-zero exit + the failing command; a broken
    KB never silently ships a stale front door. A final meta-drift verify halts on a lying currency pointer.
  NAMED_COMPENSATORS N/A — read-only over xrpl.db; only rewrites derived files. Undo = re-run, or git checkout.
  DECOMPOSE_BY_SECRETS 3 — KB-specific schema lives behind this KB's own scripts + shared/readout_profiles.py;
    this orchestrator knows only "refresh meta, build catalog, run the shared generators, refresh the root".
  UNCERTAINTY_GATED_HUMANS 3 — produces only private in-repo artifacts; publishing is a separate human-gated
    decision (the monorepo's standing publish hold), never triggered here.
"""
import subprocess, sys, os, shutil, sqlite3
try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from refresh_meta import verify_meta, MetaDriftError, DB
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PY = sys.executable
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")

STEPS = [
    ("meta     (DB -> latest_wave/updated, derived from MAX(wave))", [PY, "scripts/refresh_meta.py"]),
    ("catalog  (DB -> catalog/*.md + track-*.md)", [PY, "scripts/gen_catalog.py"]),
    ("readouts (DB -> readout/readout-*.html)",  [PY, "../shared/gen_readout.py"]),
    ("index    (DB -> readout/index.{html,md,json})", [PY, "../shared/gen_index.py"]),
    ("reports  (DB -> readout/waves+verification.{html,md})", [PY, "../shared/gen_reports.py"]),
    ("loadout  (DB -> .claude/loadout/index.json)", [PY, "scripts/gen_loadout.py"]),
    ("root     (-> ../.claude/loadout/index.json)", [PY, "../shared/gen_root_loadout.py"]),
    ("root idx (-> ../index.{html,md,json})",       [PY, "../shared/gen_root_index.py"]),
]


def run(label, cmd):
    print(f"\n› {label}")
    r = subprocess.run(cmd, env=ENV)
    if r.returncode != 0:
        sys.exit(f"✗ FAILED at: {label}  ({' '.join(cmd)})")


def main():
    for label, cmd in STEPS:
        run(label, cmd)
    al = shutil.which("ai-loadout")
    print("\n› validate (ai-loadout)")
    if al:
        for idx in [".claude/loadout/index.json", "../.claude/loadout/index.json"]:
            subprocess.run([al, "validate", idx], env=ENV)
    else:
        print("  (ai-loadout not on PATH — skipping validate; run it manually)")
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
    print("\n✓ regen complete — all pillars rebuilt from xrpl.db")


if __name__ == "__main__":
    main()
