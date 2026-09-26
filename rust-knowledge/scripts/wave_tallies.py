#!/usr/bin/env python3
"""wave_tallies.py — per-lane verification tallies for a wave, from the verifier and compiler files.

Prints, per lane: verifier verdicts (confirmed/corrected/refuted/unfindable), currency counts,
per-source results (+ supported / - not supported / ? unchecked), and the compiler's check counts.
The numbers a wave's verification.md reports come from here, never from memory.

  python scripts/wave_tallies.py --wave-dir wave-01-essentials --date 2026-09-25
"""
import argparse
import collections
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave-dir", required=True)
    ap.add_argument("--date", required=True)
    # Wave 5 reused wave 4's lane slugs on the same date, so its verdicts live in their own sweep
    # folder; without this the tallies silently read wave 4's files (as assemble_lanes --sweep).
    ap.add_argument("--sweep", help="sweep folder under verification/ (default sweep-<date>)")
    a = ap.parse_args()
    lanes = [os.path.splitext(os.path.basename(p))[0]
             for p in sorted(glob.glob(os.path.join(ROOT, "waves", a.wave_dir, "lanes", "*.json")))]
    cp = os.path.join(ROOT, "verification", f"compile-{a.date}", f"{a.wave_dir}.json")
    comp = json.load(open(cp, encoding="utf-8")) if os.path.isfile(cp) else {"results": [], "rustc": "(not run)"}
    checks, fails, recs = collections.Counter(), collections.Counter(), collections.defaultdict(set)
    for r in comp["results"]:
        checks[r["lane"]] += 1
        fails[r["lane"]] += 0 if r["ok"] else 1
        recs[r["lane"]].add(r["slug"])
    print(f"wave dir {a.wave_dir} · compiler {comp['rustc']}")
    print(f"{'lane':24s} {'conf':>4s} {'corr':>4s} {'ref':>4s} {'unf':>4s}  {'solid':>5s} {'plaus':>5s} {'shaky':>5s}"
          f"  {'src+':>4s} {'src-':>4s} {'src?':>4s}  {'checks':>6s} {'fail':>4s} {'rec/chk':>7s}")
    tot = collections.Counter()
    for lane in lanes:
        vp = os.path.join(ROOT, "verification", a.sweep or f"sweep-{a.date}", "lanes", f"{lane}.json")
        if not os.path.isfile(vp):
            print(f"{lane:24s} (no verifier file yet)")
            continue
        v = json.load(open(vp, encoding="utf-8"))
        vc = collections.Counter(x["verdict"] for x in v["verdicts"])
        cc = collections.Counter(x.get("currency") for x in v["verdicts"])
        src = [s for x in v["verdicts"] for s in (x.get("sources") or []) if isinstance(s, dict)]
        sup = sum(1 for s in src if s.get("supported") is True)
        uns = sum(1 for s in src if s.get("supported") is False)
        nul = len(src) - sup - uns
        row = dict(conf=vc["confirmed"], corr=vc["corrected"], ref=vc["refuted"], unf=vc["unfindable"],
                   solid=cc["solid"], plaus=cc["plausible"], shaky=cc["shaky"] + cc["stale"] + cc["wrong"],
                   sp=sup, sm=uns, sq=nul, ch=checks[lane], fl=fails[lane], rc=len(recs[lane]))
        tot.update(row)
        print(f"{lane:24s} {row['conf']:4d} {row['corr']:4d} {row['ref']:4d} {row['unf']:4d}  {row['solid']:5d} "
              f"{row['plaus']:5d} {row['shaky']:5d}  {row['sp']:4d} {row['sm']:4d} {row['sq']:4d}  {row['ch']:6d} "
              f"{row['fl']:4d} {row['rc']:7d}")
    print(f"{'TOTAL':24s} {tot['conf']:4d} {tot['corr']:4d} {tot['ref']:4d} {tot['unf']:4d}  {tot['solid']:5d} "
          f"{tot['plaus']:5d} {tot['shaky']:5d}  {tot['sp']:4d} {tot['sm']:4d} {tot['sq']:4d}  {tot['ch']:6d} "
          f"{tot['fl']:4d} {tot['rc']:7d}")


if __name__ == "__main__":
    main()
