#!/usr/bin/env python3
"""assemble_lanes.py — stitch per-lane research files into a wave research-raw.json.

The direct-dispatch research path writes one file per lane (waves/wave-NN/lane-<slug>.json, each =
{slug,name,domain,notes,capabilities}). This wraps them into the load_db contract:
  research-raw.json = {date, wave, lanes:[{slug, name, research:{domain,notes,capabilities}}]}
verify_cloud.py then appends cloud_verify per lane; load_db.py ingests.

Usage:  $env:PYTHONUTF8='1'; python scripts/assemble_lanes.py <wave-dir> [date] [wave]
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main(wave_dir, date, wave):
    files = sorted(glob.glob(os.path.join(wave_dir, "lane-*.json")))
    if not files:
        sys.exit(f"no lane-*.json in {wave_dir}")
    lanes = []
    total = 0
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            d = json.load(fh)
        caps = d.get("capabilities") or []
        total += len(caps)
        lanes.append({"slug": d.get("slug") or os.path.basename(f)[5:-5],
                      "name": d.get("name") or d.get("slug"),
                      "research": {"domain": d.get("domain"), "notes": d.get("notes"), "capabilities": caps}})
    out = {"date": date, "wave": int(wave), "lanes": lanes}
    dest = os.path.join(wave_dir, "research-raw.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"assembled {len(lanes)} lanes, {total} capabilities -> {os.path.relpath(dest, ROOT)}")


if __name__ == "__main__":
    wd = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "waves", "wave-01-foundation")
    dt = sys.argv[2] if len(sys.argv) > 2 else "2026-06-14"
    wv = sys.argv[3] if len(sys.argv) > 3 else "1"
    main(wd, dt, wv)
