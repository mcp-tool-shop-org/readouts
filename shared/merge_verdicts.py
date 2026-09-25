#!/usr/bin/env python3
"""Merge a verification sweep's per-lane verdicts into the durable verdict ledger.

WHY A LEDGER. `verified` used to come from ACCEPT_IDS - nine citation IDs hardcoded
in load_db.py from wave-01's abstract-NLI pass. Everything else defaulted to
`verified=0, status=directional, "existence may be gated"`, which is why the KB read
12/159 verified while carrying 147 findings nobody had actually checked. A retrieval
sweep that only touched the DB would be undone by the next `load_db.py` run, because
the DB is derived. The ledger is the source of truth the loader reads, so a rebuild
reproduces the verified state and the next sweep extends it instead of replacing it.

  python shared/merge_verdicts.py --kb godot-knowledge
  python shared/merge_verdicts.py --kb sprites-knowledge --dry-run

Verdict semantics, set by the verifier and enforced here:
  confirmed  -> verified 1, load-bearing   (source retrieved, claim supported as stated)
  corrected  -> verified 1, load-bearing   (supported after the recorded corrections)
  refuted    -> verified 0, avoid          (source retrieved, claim NOT supported)
  unfindable -> verified 0, directional    (source could not be reached; no judgement)
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys

SHARED = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SHARED)

MAPPING = {
    "confirmed": (1, "load-bearing"),
    "corrected": (1, "load-bearing"),
    "refuted": (0, "avoid"),
    "unfindable": (0, "directional"),
}
CORRECTABLE = ("authors", "year", "citation_id", "claim")

# A verifier reading a licence page will faithfully quote the contact address on it.
# Republishing a third party's mailbox invites scraping and adds nothing to the
# finding, so it is redacted at ingest rather than caught later by a publish gate.
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')


def redact(text):
    return EMAIL.sub('<address on the source page>', text) if text else text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kb", required=True,
                    help="KB directory, e.g. godot-knowledge")
    ap.add_argument("lanes", nargs="*",
                    help="lane verdict JSON files (globs ok); "
                         "defaults to <kb>/verification/sweep-*/lanes/*.json")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    kb_root = args.kb if os.path.isabs(args.kb) else os.path.join(REPO, args.kb)
    if not os.path.isdir(kb_root):
        sys.exit(f"no such KB directory: {kb_root}")
    ledger_path = os.path.join(kb_root, "verification", "verdicts.json")
    if not args.lanes:
        args.lanes = [os.path.join(kb_root, "verification", "sweep-*", "lanes", "*.json")]

    paths: list[str] = []
    for pat in args.lanes:
        paths.extend(sorted(glob.glob(pat)) or [pat])
    paths = [p for p in paths if not p.endswith(".input.json")]

    ledger = {"schema": 1, "verdicts": {}}
    if os.path.isfile(ledger_path):
        with open(ledger_path, encoding="utf-8") as fh:
            ledger = json.load(fh)
    verdicts = ledger.setdefault("verdicts", {})

    added = updated = bad = 0
    notes: dict[str, str] = ledger.setdefault("lane_notes", {})
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            lane = json.load(fh)
        bucket = lane.get("bucket") or os.path.basename(path).rsplit(".", 1)[0]
        notes[bucket] = lane.get("verifier_note", "")
        for v in lane.get("verdicts", []):
            slug, verdict = v.get("slug"), v.get("verdict")
            if not slug or verdict not in MAPPING:
                print(f"  ::error:: {bucket}: bad row {slug!r} verdict={verdict!r}")
                bad += 1
                continue
            verified, status = MAPPING[verdict]
            # Trust the mapping, not the lane's own verified/status fields: a verifier
            # that mislabels one row must not be able to mark a refuted claim verified.
            entry = {
                "verdict": verdict,
                "verified": verified,
                "status": status,
                "verify_note": redact((v.get("verify_note") or "").strip())[:240],
                "evidence_url": v.get("evidence_url") or None,
                "bucket": bucket,
            }
            corr = {k: (redact(v["corrections"][k]) if isinstance(v["corrections"][k], str)
                        else v["corrections"][k])
                    for k in CORRECTABLE
                    if isinstance(v.get("corrections"), dict) and v["corrections"].get(k)}
            if corr:
                if verdict != "corrected":
                    print(f"  ::error:: {bucket}/{slug}: corrections on a '{verdict}' row")
                    bad += 1
                    continue
                entry["corrections"] = corr
            elif verdict == "corrected":
                print(f"  ::error:: {bucket}/{slug}: 'corrected' with no corrections")
                bad += 1
                continue
            if slug in verdicts:
                updated += 1
            else:
                added += 1
            verdicts[slug] = entry

    tally: dict[str, int] = {}
    for e in verdicts.values():
        tally[e["verdict"]] = tally.get(e["verdict"], 0) + 1
    print(f"lanes merged      {len(paths)}")
    print(f"verdicts added    {added}")
    print(f"verdicts updated  {updated}")
    print(f"ledger total      {len(verdicts)}")
    print("  " + "  ".join(f"{k}={v}" for k, v in sorted(tally.items())))
    print(f"  -> verified=1 for {sum(1 for e in verdicts.values() if e['verified'])}")

    if bad:
        print(f"\n::error:: HALT - {bad} malformed verdict row(s); ledger not written")
        return 2
    if args.dry_run:
        print("\n(dry run - nothing written)")
        return 0

    os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
    with open(ledger_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(ledger, fh, indent=2, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    print(f"\nwrote {os.path.relpath(ledger_path, REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
