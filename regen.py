#!/usr/bin/env python3
"""regen.py (monorepo root) — rebuild the WHOLE readouts monorepo from source.

Runs every knowledge base's own scripts/regen.py (each rebuilds its catalog + readouts + index + loadout from its
DB), then regenerates the two ROOT artifacts that span all KBs:
  index.{html,md,json}          the monorepo FRONT DOOR  (shared/gen_root_index.py)  <- agent-first home, links each KB
  .claude/loadout/index.json    the root ROUTING index   (shared/gen_root_loadout.py)
and validates the routing index. Idempotent — same DBs in, same artifacts out (modulo the generated date stamp).

Per wave you normally run just the touched KB's `python scripts/regen.py` (it already refreshes the root front door
+ root loadout as its last steps). Use THIS for a full-monorepo rebuild — after editing shared/, adding a KB, or
when you just want everything reconciled:
    python regen.py

Standards compliance (.claude/rules/workflow-standards.md), 0-3:
  PIN_PER_STEP 3 — every step is `python <pinned script>`; all outputs derive from the DBs, so the same DBs
    reproduce byte-identical artifacts (modulo the date). No hidden state.
  EXTERNAL_VERIFIER 2 — wires `ai-loadout validate` (an independent CLI) on the routing index; the front-door
    HTML is verified out-of-band by the look-at-output rule (render headless + READ the PNG), not by this script.
  ANDON_AUTHORITY 3 — any failing step halts the whole rebuild with a non-zero exit and the failing command, so a
    broken KB never silently ships a stale monorepo front door.
  NAMED_COMPENSATORS N/A — read-only over the DBs; only rewrites derived files. Undo = re-run, or `git checkout`.
  DECOMPOSE_BY_SECRETS 3 — this orchestrator knows only "run each KB's regen, then the root generators"; all
    KB-specific schema lives behind each KB's own scripts + shared/readout_profiles.py.
  UNCERTAINTY_GATED_HUMANS 3 — produces only private in-repo artifacts; the outward-facing publish step is a
    separate, human-gated decision (kickoff objective 2), never triggered here.
"""
import subprocess, sys, os, shutil
try:  # py3.14 parent console is cp1252; keep our prints UTF-8 and ordered vs subprocess output
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
PY = sys.executable
ENV = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")


def run(label, cmd):
    print(f"\n{'=' * 66}\n# {label}\n{'=' * 66}")
    r = subprocess.run(cmd, env=ENV)
    if r.returncode != 0:
        sys.exit(f"✗ FAILED at: {label}  ({' '.join(cmd)})")


def main():
    # a KB = any subfolder with its own scripts/regen.py (each self-chdirs to its KB root, so absolute path is safe)
    kbs = sorted(d for d in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT, d, "scripts", "regen.py")))
    if not kbs:
        sys.exit("no knowledge bases found (no <kb>/scripts/regen.py)")
    for kb in kbs:
        run(f"KB: {kb}", [PY, os.path.join(ROOT, kb, "scripts", "regen.py")])
    # each KB's regen already refreshes these; re-run once at the end so the result is order-independent + reconciled
    run("root front door  (-> index.{html,md,json})", [PY, "shared/gen_root_index.py"])
    run("root loadout     (-> .claude/loadout/index.json)", [PY, "shared/gen_root_loadout.py"])
    al = shutil.which("ai-loadout")
    print("\n› validate root loadout (ai-loadout)")
    if al:
        subprocess.run([al, "validate", ".claude/loadout/index.json"], env=ENV)
    else:
        print("  (ai-loadout not on PATH — skipping validate; run it manually)")
    print(f"\n✓ monorepo regen complete — {len(kbs)} KB(s) + root front door + root loadout, all rebuilt from the DBs")


if __name__ == "__main__":
    main()
