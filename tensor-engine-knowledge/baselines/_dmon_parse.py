#!/usr/bin/env python3
"""Slice diff-dmon.log by the per-run epoch windows in diff-results.json -> per-config power/temp/VRAM peaks."""
import json, time, os
D = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(D, "diff-dmon.log")) as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        p = line.split()
        # Date Time gpu pwr gtemp mtemp sm mem enc dec jpg ofa mclk pclk fb bar1 ccpm
        try:
            dt = time.strptime(p[0] + " " + p[1], "%Y%m%d %H:%M:%S")
            ep = time.mktime(dt)
            rows.append({"ep": ep, "pwr": float(p[3]), "gtemp": float(p[4]),
                         "sm": float(p[6]), "mclk": float(p[12]), "pclk": float(p[13]), "fb": float(p[14])})
        except (ValueError, IndexError):
            continue

res = json.load(open(os.path.join(D, "diff-results.json")))

def agg(sel, key, fn):
    vals = [r[key] for r in sel]
    return fn(vals) if vals else 0

print(f"{'config':34} {'n':>3} {'pkW':>5} {'pkC':>4} {'pkSM%':>6} {'pkClk':>6} {'pkVRAM':>7} {'medVRAM':>8}")
for r in res["runs"]:
    if "error" in r:
        print(f"{r['label']:34}  (failed — no window)")
        continue
    sel = [x for x in rows if r["win_start"] - 0.5 <= x["ep"] <= r["win_end"] + 0.5]
    sel_active = [x for x in sel if x["sm"] > 5]  # exclude idle samples for median VRAM
    medv = sorted(x["fb"] for x in sel_active)[len(sel_active)//2] if sel_active else 0
    print(f"{r['label']:34} {len(sel):>3} {agg(sel,'pwr',max):>5.0f} {agg(sel,'gtemp',max):>4.0f} "
          f"{agg(sel,'sm',max):>6.0f} {agg(sel,'pclk',max):>6.0f} {agg(sel,'fb',max):>7.0f} {medv:>8.0f}")

allr = rows
print(f"\nOVERALL active peak: {max((r['pwr'] for r in allr), default=0):.0f}W  "
      f"{max((r['gtemp'] for r in allr), default=0):.0f}C  "
      f"{max((r['fb'] for r in allr), default=0):.0f}MB VRAM  "
      f"{max((r['pclk'] for r in allr), default=0):.0f}MHz core")
print(f"idle floor in log: {min((r['pwr'] for r in allr), default=0):.0f}W  "
      f"{min((r['fb'] for r in allr), default=0):.0f}MB VRAM")
