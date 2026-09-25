#!/usr/bin/env python3
"""Generate an ai-loadout index at .claude/loadout/index.json over the catalog, from the DB.

Progressive disclosure (so all the data isn't dumped on the agent at once):
  - ONE tiny `core` entry (the catalog index + shortlist) — always loaded for orientation.
  - one `domain` entry per catalog file — keyword-routed, loaded only when the task matches.
  - the wave dispatch/verification docs as `domain` entries.
  - the raw swarm json as `manual` — never auto-loaded.

Re-run after each wave. QA with:  ai-loadout validate|overlaps|budget .claude/loadout/index.json
"""
import json
import os
import re
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "recipes.db")
OUTDIR = os.path.join(ROOT, ".claude", "loadout")
DATE_FALLBACK = "2026-06-07"

# curated single-token keywords per lane (single tokens = best match recall)
KW = {
    'mesh-360': ['mesh', '3d', 'recon', 'reconstruction', 'trellis', 'trellis2', 'image-to-3d', 'multiview',
                 'turnaround', 'render', 'textured', 'hunyuan', 'stable3d', 'gaussian', 'glb', 'mesh360',
                 'photogrammetry', 'single-image', 'direction'],
    'render-light': ['render', 'blender', 'lighting', 'headless', 'camera', 'rig', 'tonemap', 'colormanagement',
                     'passes', 'outline', 'toon', 'cel', 'shading', 'normal', 'depth', 'eevee', 'cycles',
                     'parented', 'value', 'shadow'],
    'downsample-finish': ['downsample', 'downscale', 'pixel', 'pixelart', 'lanczos', 'area', 'quantize',
                          'quantization', 'dither', 'dithering', 'palette', 'footanchor', 'bbox', '48px', '64px',
                          'master', 'finish', 'resize', 'cleanup', 'antialias'],
    'nvs-direct': ['nvs', 'novelview', 'multiview', 'turnaround', 'zero123', 'zero123plus', 'consistent', 'views',
                   'diffusion', 'syncdreamer', 'wonder3d', 'noncommercial', 'license', 'pose', 'direction',
                   'mvdream', 'imagedream', 'azimuth', 'elevation', 'meshfree'],
    'sheet-direct': ['spritesheet', 'sheet', 'charturn', 'pixelart', 'lora', 'controlnet', 'pose', 'eightdirection',
                     'diffusion', 'direct', 'character', 'turn', 'animation', 'frames', 'tile', 'walk',
                     'directional', 'reference', 'consistent'],
    'eval-qa': ['eval', 'qa', 'gate', 'verifier', 'siglip', 'siglip2', 'clip', 'lpips', 'ssim', 'consistency',
                'perceptual', 'aijudge', 'metric', 'turnaround', 'fidelity', 'acceptance', 'threshold', 'score',
                'quality', 'inspection'],
    'animation-locomotion': ['animation', 'locomotion', 'walk', 'walkcycle', 'cycle', 'frames', 'sequence', 'rig',
                             'autorig', 'interpolation', 'inbetween', 'rife', 'imagetoanimation', 'sprite',
                             'motion', 'pose', 'skeleton', 'render', 'loop', 'frame'],
}
PAT = {
    'mesh-360': ['mesh', 'image_to_3d', 'multiview', 'render'],
    'render-light': ['render', 'lighting', 'blender', 'toon'],
    'downsample-finish': ['downsample', 'pixel_art', 'palette', 'finish'],
    'nvs-direct': ['novel_view', 'multiview', 'license', 'turnaround'],
    'sheet-direct': ['sprite_sheet', 'diffusion', 'controlnet', 'character_turn'],
    'eval-qa': ['eval', 'verifier', 'metric', 'gate'],
    'animation-locomotion': ['animation', 'walk_cycle', 'locomotion', 'frames'],
}

STOP = {'recipe', 'recipes', 'technique', 'techniques', 'sprite', 'sprites', 'the', 'and', 'with', 'for', 'model',
        'models', 'based', 'pipeline', 'via', 'from', 'into'}


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

    # core — tiny always-on orientation
    t, l = est(os.path.join(ROOT, "catalog", "README.md"))
    entries.append({"id": "catalog-index", "path": "catalog/README.md",
                    "keywords": ["catalog", "sprite", "recipe", "pipeline", "loadout"], "patterns": [], "priority": "core",
                    "summary": "Catalog index + proven-on-rig table + recommended shortlist; drill into per-lane entries.",
                    "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    # one domain entry per catalog file
    for cat in cats:
        full = os.path.join(ROOT, "catalog", cat["slug"] + ".md")
        if not os.path.exists(full):
            continue
        n = c.execute("SELECT COUNT(*) FROM recipes WHERE category_id=?", (cat["id"],)).fetchone()[0]
        t, l = est(full)
        kw = list(KW.get(cat["slug"], []))
        # harvest curated keywords from recipe slugs / engine_family / applicable_to (minus stopwords)
        for (sl, ef, ap) in c.execute(
                "SELECT slug, COALESCE(engine_family,''), COALESCE(applicable_to,'') FROM recipes "
                "WHERE category_id=? ORDER BY download_priority", (cat["id"],)):
            for src in (sl, ef, ap):
                for w in re.split(r"[^a-z0-9]+", (src or "").lower()):
                    if len(w) > 2 and w not in kw and w not in STOP:
                        kw.append(w)
        summ = f"{cat['name']}: {n} recipes. {cat['description']}"[:120]
        entries.append({"id": cat["slug"], "path": f"catalog/{cat['slug']}.md", "keywords": kw,
                        "patterns": PAT.get(cat["slug"], []), "priority": "domain", "summary": summ,
                        "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    # wave docs — every wave's dispatch + verification (domain) and raw json (manual)
    import glob as _glob
    DISP_KW = ["recipe", "sprite", "mesh", "render", "downsample", "turnaround", "spritesheet", "animation", "eval",
               "pipeline", "plan", "best", "recommended", "lane", "stage"]
    VER_KW = ["verify", "verification", "evidence", "source", "citation", "currency", "superseded", "reproduce", "trust"]
    for wdir in sorted(_glob.glob(os.path.join(ROOT, "waves", "wave-*"))):
        if not os.path.isdir(wdir):
            continue
        wname = os.path.basename(wdir)
        disp = os.path.join(wdir, "dispatch.md")
        if os.path.exists(disp):
            t, l = est(disp)
            entries.append({"id": f"{wname}-dispatch", "path": f"waves/{wname}/dispatch.md", "keywords": DISP_KW,
                            "patterns": ["recipe", "sprite", "render", "eval"], "priority": "domain",
                            "summary": f"{wname} narrative: sprite-pipeline findings + plan per lane."[:120],
                            "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})
        ver = os.path.join(wdir, "verification.md")
        if os.path.exists(ver):
            t, l = est(ver)
            entries.append({"id": f"{wname}-verification", "path": f"waves/{wname}/verification.md", "keywords": VER_KW,
                            "patterns": ["verification"], "priority": "domain",
                            "summary": f"{wname} verifier receipt: verdicts, currency, evidence strength, corrections."[:120],
                            "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})
        rawj = os.path.join(wdir, "research-raw.json")
        if os.path.exists(rawj):
            t, l = est(rawj)
            entries.append({"id": f"{wname}-raw", "path": f"waves/{wname}/research-raw.json", "keywords": ["raw", "json"],
                            "patterns": [], "priority": "manual",
                            "summary": f"Raw verified {wname} swarm output (large) — manual lookup only.",
                            "triggers": {"task": False, "plan": False, "edit": False}, "tokens_est": t, "lines": l})

    core = sum(e["tokens_est"] for e in entries if e["priority"] == "core")
    ondemand = sum(e["tokens_est"] for e in entries if e["priority"] != "core")
    domain_toks = sorted((e["tokens_est"] for e in entries if e["priority"] == "domain"), reverse=True)
    avg = core + sum(domain_toks[:2])
    index = {"version": "1.0.0", "generated": date + "T00:00:00Z",
             "source": f"recipes.db (wave {wave})", "lazyLoad": True,
             "budget": {"always_loaded_est": core, "on_demand_total_est": ondemand,
                        "avg_task_load_est": avg, "avg_task_load_observed": None},
             "entries": entries}
    with open(os.path.join(OUTDIR, "index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    con.close()
    print(f"loadout index: {len(entries)} entries — core {core} tok always-on, "
          f"{ondemand} tok on-demand, ~{avg} tok/typical task. -> .claude/loadout/index.json")


if __name__ == "__main__":
    main()
