#!/usr/bin/env python3
"""build_ledger.py — build verification/verdicts.json for rust-knowledge from its two verifiers.

  1. The adversarial retrieval verifiers (Claude Sonnet, reasoning-stripped), one file per lane under
     verification/sweep-*/lanes/<lane>.json. Merged by the shared tool, shared/merge_verdicts.py, which
     owns the verdict -> verified/status mapping and refuses malformed rows.
  2. The compiler (rustc 1.98.1 through scripts/compile_oracle.py `run`), one file per wave under
     verification/compile-*/<wave-dir>.json. Not a model.

THE COMPILE GATE. A recipe whose own code check does not do what the recipe says it does is not
verified, whatever the retrieval verifier concluded: its ledger row is set to verified = 0 and status
`directional`, and the failure is written into its note. A recipe whose checks all pass keeps the
retrieval verdict and gains a `compile` record. A recipe with no checks is judged by retrieval alone.

Always run this script, never merge_verdicts.py on its own: merge_verdicts rewrites every row it
merges, which would silently drop the compile gate.

  python scripts/build_ledger.py            # merge + gate, write the ledger
  python scripts/build_ledger.py --dry-run  # report only
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
LEDGER = os.path.join(ROOT, "verification", "verdicts.json")


def latest_compile_results() -> dict[str, dict]:
    """slug -> {"results": [...], "rustc": str, "run": path}, the newest run that covered the slug."""
    out: dict[str, dict] = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "verification", "compile-*", "*.json"))):
        with open(p, encoding="utf-8") as fh:
            payload = json.load(fh)
        by_slug: dict[str, list] = {}
        for r in payload.get("results", []):
            by_slug.setdefault(r["slug"], []).append(r)
        for slug, results in by_slug.items():
            out[slug] = {"results": results, "rustc": payload.get("rustc"),
                         "run": os.path.relpath(p, ROOT).replace("\\", "/")}
    return out


def append_note(base: str, tail: str, cap: int) -> str:
    """base + tail within cap characters, trimming the base and never the tail.

    The tail is what this script knows and the verifier could not: a failing check, or an
    operator's note. Cutting the whole string at cap published four operator notes that
    stopped mid-sentence, before the sentence that said the recipe stands (2026-09-25).
    """
    room = cap - len(tail)
    if len(base) > room:
        base = base[:max(0, room - 1)].rstrip() + "…"
    return (base + tail)[:cap]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    cmd = [sys.executable, os.path.join(REPO, "shared", "merge_verdicts.py"), "--kb", "rust-knowledge"]
    if args.dry_run:
        cmd.append("--dry-run")
    print("› shared/merge_verdicts.py (retrieval verifiers)")
    r = subprocess.run(cmd, env=env)
    if r.returncode != 0:
        print("HALT: merge_verdicts refused the verifier files; ledger not gated")
        return r.returncode
    if args.dry_run and not os.path.isfile(LEDGER):
        print("(dry run, no ledger on disk yet — compile gate not previewed)")
        return 0

    with open(LEDGER, encoding="utf-8") as fh:
        ledger = json.load(fh)
    verdicts = ledger.get("verdicts", {})
    compiled = latest_compile_results()
    gated = passed = 0
    for slug, entry in verdicts.items():
        c = compiled.get(slug)
        if not c:
            entry.pop("compile", None)
            continue
        n = len(c["results"])
        ok = sum(1 for x in c["results"] if x.get("ok"))
        entry["compile"] = {"checks": n, "passed": ok, "rustc": c["rustc"], "run": c["run"]}
        if ok == n:
            passed += 1
            continue
        gated += 1
        first = next((x.get("note") for x in c["results"] if not x.get("ok")), "")
        entry["verified"] = 0
        if entry.get("status") != "avoid":
            entry["status"] = "directional"
        base = (entry.get("verify_note") or "").split(" · compile gate:")[0]
        entry["verify_note"] = append_note(base, f" · compile gate: {ok}/{n} checks pass — {first}", 400)
    ledger["compile_gate"] = {"recipes_with_checks": sum(1 for s in verdicts if s in compiled),
                              "all_pass": passed, "gated_to_unverified": gated}

    # OPERATOR NOTES — authored, dated annotations on a verdict (verification/operator-notes.json).
    # They never change verified / status / verdict; they only append what the operator knows that
    # the verifier could not (e.g. a staging defect that hid a field from the verifier's input).
    notes_path = os.path.join(ROOT, "verification", "operator-notes.json")
    n_notes = 0
    if os.path.isfile(notes_path):
        with open(notes_path, encoding="utf-8") as fh:
            notes = json.load(fh).get("notes", {})
        for slug, n in notes.items():
            entry = verdicts.get(slug)
            if not entry:
                print(f"  ::error:: operator note for unknown slug {slug!r}")
                return 2
            # One note, or a list when a recipe carries more than one (a citation anchor and a
            # consumed-pin mark, for instance).
            items = n if isinstance(n, list) else [n]
            base = (entry.get("verify_note") or "").split(" · [operator")[0]
            tail = "".join(f" · [operator {x.get('date', '')}: {x['note']}]" for x in items)
            # 600: merge_verdicts caps the verifier's own note at 240, so one note of up to ~330
            # characters fits beside it untrimmed; each further note gets its own 300.
            entry["verify_note"] = append_note(base, tail, 600 + 300 * (len(items) - 1))
            entry["operator_note"] = items[0] if len(items) == 1 else items
            n_notes += len(items)
    print(f"› operator notes applied: {n_notes}")
    print(f"› compile gate: {passed} recipes all-pass, {gated} set unverified by a failing check")
    print(f"  ledger verified=1: {sum(1 for e in verdicts.values() if e.get('verified'))} of {len(verdicts)}")
    if args.dry_run:
        print("(dry run — ledger not rewritten with the gate)")
        return 0
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(ledger, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    print(f"wrote {os.path.relpath(LEDGER, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
