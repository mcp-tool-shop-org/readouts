#!/usr/bin/env python3
"""Assemble a blender-knowledge wave swarm output ({research, verify}) into the load_db
research-raw.json contract. Merges each recipe's adversarial verdict (currency) + note by
title match, and maps the parallel lanes (in order) to the 6 category slugs.

Usage: python scripts/_assemble_wave.py <workflow-output.json> [wave_number] [date]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

LANE_SLUGS = ["architecture", "grid-movement", "turn-combat", "rendering-2.5d", "ui-tactical", "tooling-test-export"]
LANE_TITLES = {
    "architecture": "Project & scene architecture",
    "grid-movement": "Grid & tactical movement",
    "turn-combat": "Turn-based combat architecture",
    "rendering-2.5d": "Rendering & 2.5D sprites",
    "ui-tactical": "Tactical UI (legibility)",
    "tooling-test-export": "Tooling, test, export, CI",
}


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def main(path, wave_no=1, date="2026-06-18"):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    res = data.get("result", data)
    research = res.get("research") or []
    verify = res.get("verify") or []
    agent_count = data.get("agentCount") or res.get("agentCount") or 12

    out_dir = os.path.join(ROOT, "waves", f"wave-0{wave_no}-foundation")
    out_path = os.path.join(out_dir, "research-raw.json")

    lanes_out = []
    n_solid = n_total = 0
    for i, r in enumerate(research):
        if not r:
            continue
        slug = LANE_SLUGS[i] if i < len(LANE_SLUGS) else norm(r.get("lane"))
        vmap = {}
        v = verify[i] if i < len(verify) and verify[i] else None
        if v:
            for chk in v.get("checks", []):
                vmap[norm(chk.get("recipe_title"))] = chk
        recipes = []
        for rec in (r.get("recipes") or []):
            chk = vmap.get(norm(rec.get("title")))
            currency = chk.get("verdict") if chk else None
            recipes.append({
                "name": rec.get("title"),
                "what": rec.get("what"),
                "how": rec.get("how"),
                "blender_version": rec.get("blender_version"),
                "gotchas": rec.get("gotchas"),
                "studio_use": rec.get("studio_use"),
                "currency": currency,
                "verify_note": chk.get("note") if chk else None,
                "sources": [{"title": s.get("title"), "url": s.get("url")}
                            for s in (rec.get("sources") or []) if s.get("url")],
            })
            n_total += 1
            if currency == "solid":
                n_solid += 1
        lanes_out.append({"laneSlug": slug, "title": LANE_TITLES.get(slug, slug), "recipes": recipes})

    out = {
        "wave": wave_no,
        "date": date,
        "title": "Wave 1 — Blender-4 tactical-RPG dev knowledge for Studio (study swarm)",
        "domain_scope": ", ".join(LANE_SLUGS),
        "agent_count": agent_count,
        "verifier_note": (f"6 web-grounded Blender-4 research lanes, each adversarially verified against current "
                          f"Blender 4.x docs for CURRENCY (flags Blender-3 staleness, deprecated nodes, version-wrong "
                          f"APIs). {n_solid}/{n_total} recipes verdict 'solid'. Same-family verifier + live-docs "
                          f"retrieval oracle per readouts convention; cross-family cloud verify is the planned "
                          f"hardening pass."),
        "lanes": lanes_out,
    }
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"wrote {out_path}: {len(lanes_out)} lanes, {n_total} recipes ({n_solid} solid).")


if __name__ == "__main__":
    p = sys.argv[1]
    wn = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    dt = sys.argv[3] if len(sys.argv) > 3 else "2026-06-18"
    main(p, wn, dt)
