#!/usr/bin/env python3
"""Assemble per-lane research files (waves/<wave>/lanes/*.json) into the wave's research-raw.json
that load_db.py ingests. Each lane file = {laneSlug, title, recipes:[...]}; lanes are collected
(filename-sorted) and wrapped with wave metadata. Order doesn't matter — load_db maps by laneSlug
and gen_catalog orders by category.sort.

    python _assemble_lanes.py <wave_dir> --wave N --date YYYY-MM-DD --title "..." [--scope "..."] [--verifier "..."]
"""
import argparse, glob, json, os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wave_dir")
    ap.add_argument("--wave", type=int, required=True)
    ap.add_argument("--date", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--scope", default="")
    ap.add_argument("--verifier", default="")
    args = ap.parse_args()

    lanes, n = [], 0
    for p in sorted(glob.glob(os.path.join(args.wave_dir, "lanes", "*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        recs = d.get("recipes", [])
        lanes.append({"laneSlug": d["laneSlug"], "title": d.get("title", d["laneSlug"]), "recipes": recs})
        n += len(recs)

    out = {
        "wave": args.wave, "date": args.date, "title": args.title,
        "domain_scope": args.scope or ", ".join(l["laneSlug"] for l in lanes),
        "agent_count": len(lanes),
        "verifier_note": args.verifier,
        "lanes": lanes,
    }
    op = os.path.join(args.wave_dir, "research-raw.json")
    json.dump(out, open(op, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    solid = sum(1 for l in lanes for r in l["recipes"] if (r.get("currency") or "").lower() == "solid")
    print(f"assembled {op}: {len(lanes)} lanes, {n} recipes ({solid} self-rated solid)")


if __name__ == "__main__":
    main()
