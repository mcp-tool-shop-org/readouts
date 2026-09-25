#!/usr/bin/env python3
"""Generate an ai-loadout index at .claude/loadout/index.json over the catalog, from godot.db.

Progressive disclosure: one tiny `core` (the catalog index) + one `domain` per lane (keyword-routed,
loaded only when a Godot task matches) + the wave dispatch/verification docs (domain) + raw json (manual).
Re-run after each wave. QA with:  ai-loadout validate .claude/loadout/index.json
"""
import glob as _glob
import json
import os
import re
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "godot.db")
OUTDIR = os.path.join(ROOT, ".claude", "loadout")
DATE_FALLBACK = "2026-06-18"

KW = {
    'architecture': ['architecture', 'scene', 'node', 'autoload', 'singleton', 'signal', 'eventbus', 'resource', 'tres',
                     'datadriven', 'state', 'statemachine', 'save', 'load', 'resourcesaver', 'composition', 'structure', 'gdscript'],
    'grid-movement': ['grid', 'tilemap', 'tilemaplayer', 'movement', 'astar', 'astargrid2d', 'pathfinding', 'floodfill',
                      'range', 'cursor', 'selection', 'coordinate', 'tactical', 'gdquest', 'framework', 'template', 'cell', 'map'],
    'turn-combat': ['turn', 'combat', 'initiative', 'actionpoint', 'statemachine', 'deterministic', 'damage',
                    'ability', 'status', 'targeting', 'calledshot', 'loot', 'ai', 'enemy', 'effect'],
    'rendering-2.5d': ['rendering', 'render', 'sprite', 'ysort', 'depth', 'lighting', 'light2d', 'canvasmodulate',
                       'normalmap', 'glow', 'animatedsprite2d', 'animationplayer', 'atlas', 'forwardplus',
                       'glcompatibility', 'renderer', 'shader'],
    'ui-tactical': ['ui', 'control', 'container', 'theme', 'hud', 'tooltip', 'label', 'panel', 'layout', 'responsive',
                    'legibility', 'display', 'menu', 'button'],
    'tooling-test-export': ['tooling', 'test', 'gut', 'unittest', 'debug', 'profile', 'headless', 'githubactions',
                            'export', 'template', 'windows', 'steam', 'performance', 'gitignore', 'versioncontrol', 'build'],
}
PAT = {
    'architecture': ['scene', 'autoload', 'resource', 'state_machine'],
    'grid-movement': ['tilemap', 'astar', 'pathfinding', 'movement_range'],
    'turn-combat': ['turn', 'action_point', 'targeting', 'damage'],
    'rendering-2.5d': ['rendering', 'lighting', 'sprite', 'y_sort'],
    'ui-tactical': ['ui', 'control', 'theme', 'hud'],
    'tooling-test-export': ['test', 'export', 'ci', 'headless'],
}
STOP = {'recipe', 'recipes', 'godot', 'the', 'and', 'with', 'for', 'via', 'from', 'into', 'use', 'using', 'pattern', 'that'}


def est(path):
    if not os.path.exists(path):
        return 0, 0
    txt = open(path, encoding="utf-8").read()
    return max(0, len(txt) // 4), txt.count("\n") + 1


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    dr = c.execute("SELECT value FROM meta WHERE key='updated'").fetchone()
    date = dr[0] if dr else DATE_FALLBACK
    wr = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()
    wave = wr[0] if wr and wr[0] is not None else 0
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUTDIR, exist_ok=True)
    entries = []

    t, l = est(os.path.join(ROOT, "catalog", "README.md"))
    entries.append({"id": "catalog-index", "path": "catalog/README.md",
                    "keywords": ["godot", "godot4", "gdscript", "catalog", "tactical", "rpg", "engine"],
                    "patterns": [], "priority": "core",
                    "summary": "Godot-4 KB index: per-lane currency rollup + flagged list; drill into a lane for recipes.",
                    "triggers": {"task": True, "plan": True, "edit": True}, "tokens_est": t, "lines": l})

    for cat in cats:
        full = os.path.join(ROOT, "catalog", cat["slug"] + ".md")
        if not os.path.exists(full):
            continue
        n = c.execute("SELECT COUNT(*) FROM recipes WHERE category_id=?", (cat["id"],)).fetchone()[0]
        t, l = est(full)
        kw = list(KW.get(cat["slug"], []))
        for (sl, wh) in c.execute("SELECT slug, COALESCE(what,'') FROM recipes WHERE category_id=?", (cat["id"],)):
            for src in (sl, wh):
                for w in re.split(r"[^a-z0-9]+", (src or "").lower()):
                    if len(w) > 2 and w not in kw and w not in STOP:
                        kw.append(w)
        summ = f"{cat['name']}: {n} recipes. {cat['description']}"[:120]
        entries.append({"id": cat["slug"], "path": f"catalog/{cat['slug']}.md", "keywords": kw[:60],
                        "patterns": PAT.get(cat["slug"], []), "priority": "domain", "summary": summ,
                        "triggers": {"task": True, "plan": True, "edit": True}, "tokens_est": t, "lines": l})

    DISP_KW = ["godot", "godot4", "architecture", "grid", "combat", "render", "ui", "tooling", "plan", "recipe", "lane"]
    VER_KW = ["verify", "verification", "currency", "godot3", "stale", "deprecated", "trust", "source"]
    for wdir in sorted(_glob.glob(os.path.join(ROOT, "waves", "wave-*"))):
        if not os.path.isdir(wdir):
            continue
        wname = os.path.basename(wdir)
        for fname, sid, kw, pri, summ, pat in [
            ("dispatch.md", f"{wname}-dispatch", DISP_KW, "domain",
             f"{wname}: Godot-4 findings + recommendations per lane.", ["godot", "recipe"]),
            ("verification.md", f"{wname}-verification", VER_KW, "domain",
             f"{wname} verifier receipt: per-recipe Godot-4 currency verdicts.", ["verification"]),
            ("research-raw.json", f"{wname}-raw", ["raw", "json"], "manual",
             f"Raw verified {wname} swarm output (large) — manual lookup only.", []),
        ]:
            fp = os.path.join(wdir, fname)
            if not os.path.exists(fp):
                continue
            t, l = est(fp)
            entries.append({"id": sid, "path": f"waves/{wname}/{fname}", "keywords": kw, "patterns": pat,
                            "priority": pri, "summary": summ[:120],
                            "triggers": {"task": pri != "manual", "plan": pri != "manual", "edit": False},
                            "tokens_est": t, "lines": l})

    core = sum(e["tokens_est"] for e in entries if e["priority"] == "core")
    ondemand = sum(e["tokens_est"] for e in entries if e["priority"] != "core")
    domain_toks = sorted((e["tokens_est"] for e in entries if e["priority"] == "domain"), reverse=True)
    avg = core + sum(domain_toks[:2])
    index = {"version": "1.0.0", "generated": date + "T00:00:00Z", "source": f"godot.db (wave {wave})",
             "lazyLoad": True,
             "budget": {"always_loaded_est": core, "on_demand_total_est": ondemand, "avg_task_load_est": avg,
                        "avg_task_load_observed": None},
             "entries": entries}
    with open(os.path.join(OUTDIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    con.close()
    print(f"loadout index: {len(entries)} entries — core {core} tok always-on, "
          f"{ondemand} tok on-demand, ~{avg} tok/typical task. -> .claude/loadout/index.json")


if __name__ == "__main__":
    main()
