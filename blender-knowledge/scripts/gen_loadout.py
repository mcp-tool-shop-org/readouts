#!/usr/bin/env python3
"""Generate an ai-loadout index at .claude/loadout/index.json over the catalog, from blender.db.

Progressive disclosure: one tiny `core` (the catalog index) + one `domain` per lane (keyword-routed,
loaded only when a Blender task matches) + the wave dispatch/verification docs (domain) + raw json (manual).
Re-run after each wave. QA with:  ai-loadout validate .claude/loadout/index.json
"""
import glob as _glob
import json
import os
import re
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "blender.db")
OUTDIR = os.path.join(ROOT, ".claude", "loadout")
DATE_FALLBACK = "2026-06-18"

KW = {
    'headless-bpy': ['headless', 'background', 'bpy', 'python', 'script', 'cli', 'commandline', 'render', 'batch',
                     'operator', 'ops', 'data', 'context', 'factory', 'version', 'automation', 'module', 'pip', 'expr'],
    'render-engines': ['render', 'engine', 'eevee', 'eeveenext', 'cycles', 'gpu', 'optix', 'cuda', 'hip', 'metal',
                       'samples', 'denoise', 'denoising', 'filmtransparent', 'alpha', 'transparent', 'resolution', 'rendering'],
    'color-management': ['color', 'colormanagement', 'viewtransform', 'agx', 'standard', 'filmic', 'pbrneutral',
                         'exposure', 'gamma', 'look', 'ocio', 'opencolorio', 'tonemapping', 'saturation', 'washed', 'colorspace', 'srgb'],
    'import-export': ['import', 'export', 'gltf', 'glb', 'fbx', 'obj', 'usd', 'interchange', 'vertexcolor', 'draco',
                      'axis', 'scale', 'orientation', 'mesh', 'material', 'io'],
    'lighting-camera': ['light', 'lighting', 'lamp', 'area', 'sun', 'point', 'spot', 'hdri', 'world', 'environment',
                        'camera', 'orthographic', 'perspective', 'ortho', 'fov', 'lens', 'rig', 'orbit', 'pivot', 'shadow', 'trackto'],
    'mesh-ops': ['mesh', 'modifier', 'decimate', 'remesh', 'boolean', 'normals', 'smooth', 'autosmooth', 'smoothbyangle',
                 'merge', 'fillholes', 'cleanup', 'retopo', 'poly', 'geometry', 'edit'],
    'materials-baking': ['material', 'shader', 'principled', 'bsdf', 'pbr', 'bake', 'baking', 'texture', 'normal',
                         'roughness', 'metallic', 'ao', 'selectedtoactive', 'uv', 'unwrap', 'vertexcolor', 'colorspace', 'node'],
    'geometry-nodes': ['geometry', 'geometrynodes', 'gn', 'procedural', 'node', 'instance', 'scatter', 'distribute',
                       'attribute', 'namedattribute', 'repeat', 'simulation', 'modifier', 'realize', 'points'],
    'rigging-animation': ['rig', 'rigging', 'armature', 'bone', 'bonecollection', 'weight', 'weightpaint', 'skin',
                          'constraint', 'ik', 'driver', 'animation', 'keyframe', 'action', 'nla', 'slottedaction', 'gltf', 'export'],
    'addons-pipeline': ['addon', 'addons', 'extension', 'extensions', 'plugin', 'manifest', 'register', 'nodewrangler',
                        'gpl', 'license', 'pipeline', 'install', 'preferences', 'bpy', 'api'],
}
PAT = {
    'headless-bpy': ['headless', 'background', 'bpy', 'render_cli'],
    'render-engines': ['eevee', 'cycles', 'samples', 'transparent'],
    'color-management': ['agx', 'view_transform', 'exposure', 'colorspace'],
    'import-export': ['gltf', 'import', 'export', 'vertex_color'],
    'lighting-camera': ['light', 'camera', 'hdri', 'orbit'],
    'mesh-ops': ['decimate', 'remesh', 'normals', 'cleanup'],
    'materials-baking': ['principled', 'bake', 'pbr', 'uv'],
    'geometry-nodes': ['geometry_nodes', 'scatter', 'instance', 'attribute'],
    'rigging-animation': ['armature', 'bone', 'weight', 'animation'],
    'addons-pipeline': ['addon', 'extension', 'register', 'manifest'],
}
STOP = {'recipe', 'recipes', 'blender', 'the', 'and', 'with', 'for', 'via', 'from', 'into', 'use', 'using', 'pattern', 'that'}


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
                    "keywords": ["blender", "blender4", "bpy", "catalog", "render", "sprite", "pipeline", "studio", "asset", "3d"],
                    "patterns": [], "priority": "core",
                    "summary": "Blender-4.x KB index: per-lane currency rollup + flagged list; drill into a lane for recipes.",
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

    DISP_KW = ["blender", "blender4", "bpy", "render", "mesh", "material", "rig", "addon", "import", "plan", "recipe", "lane"]
    VER_KW = ["verify", "verification", "currency", "blender3", "stale", "deprecated", "trust", "source"]
    for wdir in sorted(_glob.glob(os.path.join(ROOT, "waves", "wave-*"))):
        if not os.path.isdir(wdir):
            continue
        wname = os.path.basename(wdir)
        for fname, sid, kw, pri, summ, pat in [
            ("dispatch.md", f"{wname}-dispatch", DISP_KW, "domain",
             f"{wname}: Blender-4 findings + recommendations per lane.", ["blender", "recipe"]),
            ("verification.md", f"{wname}-verification", VER_KW, "domain",
             f"{wname} verifier receipt: per-recipe Blender-4 currency verdicts.", ["verification"]),
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
    index = {"version": "1.0.0", "generated": date + "T00:00:00Z", "source": f"blender.db (wave {wave})",
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
