#!/usr/bin/env python3
"""Assemble a wave's per-lane research files into the loader's research-raw.json.

Each research lane writes `waves/wave-NN-name/lanes/<laneSlug>.json` independently;
this concatenates them under one wave header. The lane files may carry extra keys the
loader ignores (`licence_notes`, `gaps`) - those are kept in the assembled file, since
a lane's recorded gaps are a deliverable, not an apology.

    python scripts/assemble_wave.py waves/wave-08-expansion --wave 8 \
        --title "Wave 8 - ..." --scope "..."

Re-runnable: overwrites research-raw.json from whatever lanes are currently present,
so a late lane is picked up by re-running rather than by hand-merging.
"""
from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REQUIRED = ("authors", "year", "title", "id", "url", "finding")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("wave_dir")
    ap.add_argument("--wave", type=int, required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--scope", default="")
    ap.add_argument("--verifier-note", default="")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    args = ap.parse_args()

    wdir = args.wave_dir if os.path.isabs(args.wave_dir) else os.path.join(ROOT, args.wave_dir)
    paths = sorted(p for p in glob.glob(os.path.join(wdir, "lanes", "*.json"))
                   if not p.endswith(".input.json"))
    if not paths:
        sys.exit(f"no lane files under {os.path.join(wdir, 'lanes')}")

    lanes, total, bad = [], 0, 0
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            lane = json.load(fh)
        slug = lane.get("laneSlug") or os.path.basename(p).rsplit(".", 1)[0]
        findings = lane.get("findings") or []
        for i, f in enumerate(findings, 1):
            missing = [k for k in REQUIRED if not f.get(k)]
            if missing:
                print(f"  ::error:: {slug}#{i}: missing {', '.join(missing)}")
                bad += 1
            f.setdefault("n", i)
        lanes.append({k: v for k, v in {
            "laneSlug": slug,
            "title": lane.get("title") or slug.replace("-", " ").title(),
            "findings": findings,
            "licence_notes": lane.get("licence_notes"),
            "gaps": lane.get("gaps"),
        }.items() if v})
        print(f"  {slug:<28} {len(findings):>3} findings")
        total += len(findings)

    if bad:
        print(f"\n::error:: HALT - {bad} finding(s) missing required fields")
        return 2

    out = {
        "wave": args.wave,
        "date": args.date,
        "title": args.title,
        "domain_scope": args.scope,
        "agent_count": len(lanes),
        "verifier_note": args.verifier_note,
        "lanes": lanes,
    }
    dest = os.path.join(wdir, "research-raw.json")
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"\n{len(lanes)} lanes, {total} findings -> {os.path.relpath(dest, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
