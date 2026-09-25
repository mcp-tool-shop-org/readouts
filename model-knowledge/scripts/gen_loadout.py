#!/usr/bin/env python3
"""Generate an ai-loadout index at .claude/loadout/index.json over the catalog, from the DB.

Progressive disclosure (so all the data isn't dumped on the agent at once):
  - ONE tiny `core` entry (the catalog index + shortlist) — always loaded for orientation.
  - one `domain` entry per catalog file — keyword-routed, loaded only when the task matches.
  - the wave dispatch/verification docs as `domain` entries.
  - the raw swarm json as `manual` — never auto-loaded.

An agent calls planLoad(task) / `ai-loadout resolve` to pull only the matching slice within budget.
Re-run after each wave. QA with:  ai-loadout validate|overlaps|budget .claude/loadout/index.json
"""
import json
import os
import re
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "models.db")
OUTDIR = os.path.join(ROOT, ".claude", "loadout")
DATE_FALLBACK = "2026-06-02"

# curated single-token keywords per domain (single tokens = best match recall)
KW = {
    'image-base': ['image', 'base', 'checkpoint', 'txt2img', 'flux', 'sdxl', 'qwen', 'illustrious', 'chroma',
                   'photoreal', 'anime', 'illustration', 'concept', 'sprite', 'hidream'],
    'image-control': ['controlnet', 'control', 'ipadapter', 'lora', 'train', 'training', 'upscale', 'upscaler',
                      'inpaint', 'outpaint', 'detailer', 'pose', 'depth', 'canny', 'consistency'],
    'image-edit': ['edit', 'editing', 'kontext', 'instruction', 'variant', 'reference', 'relight', 'modify'],
    'video': ['video', 'wan', 'hunyuanvideo', 'ltx', 'ltxv', 'cogvideo', 'mochi', 'animate', 'i2v', 't2v',
              'motion', 'cutscene', 'interpolation'],
    '3d': ['3d', 'mesh', 'trellis', 'hunyuan3d', 'triposg', 'triposr', 'texture', 'prop', 'sculpt', 'glb',
           'retopo', 'pbr'],
    'audio': ['audio', 'music', 'sfx', 'foley', 'voice', 'tts', 'song', 'sound', 'narration', 'chatterbox',
              'kokoro', 'stem', 'loop', 'diffrhythm'],
    'llm': ['llm', 'ollama', 'text', 'reasoning', 'coding', 'prompt', 'chat', 'qwen3', 'gemma', 'mistral',
            'deepseek', 'vision', 'vlm'],
    'caption': ['caption', 'captioning', 'tag', 'tagger', 'tagging', 'booru', 'dataset', 'label', 'florence',
                'joycaption', 'internvl', 'minicpm', 'ocr'],
    'comfy': ['comfyui', 'comfy', 'install', 'setup', 'node', 'nodes', 'custom', 'workflow', 'manager',
              'blackwell', 'portable', 'sageattention'],
}
PAT = {
    'image-base': ['game_asset', 'marketing', 'commercial_safe', 'text_in_image'],
    'image-control': ['lora_training', 'character_consistency', 'commercial_safe', 'upscaling'],
    'image-edit': ['concept_iteration', 'asset_variant', 'instruction_edit'],
    'video': ['image_to_video', 'clip_motion', 'marketing_video'],
    '3d': ['game_asset', 'game_ready', 'kitbashing'],
    'audio': ['soundtrack_sfx', 'voiceover', 'adaptive_music'],
    'llm': ['captioning', 'prompt_enhancement', 'coding'],
    'caption': ['dataset_building', 'lora_training', 'tagging'],
    'comfy': ['install', 'workflow', 'node_setup'],
}


# generic tokens that leak from model names but make poor routing keywords
STOP = {'family', 'and', 'with', 'the', 'plus', 'base', 'dev', 'full', 'model', 'models',
        'image', 'open', 'weights', 'version', 'sdxl', 'qwen', 'anime', 'turbo', 'xl'}


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
    wave = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()[0]
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUTDIR, exist_ok=True)
    entries = []

    # core — tiny always-on orientation
    t, l = est(os.path.join(ROOT, "catalog", "README.md"))
    entries.append({"id": "catalog-index", "path": "catalog/README.md",
                    "keywords": ["catalog", "model", "models", "loadout"], "patterns": [], "priority": "core",
                    "summary": "Catalog index + commercial-safe re-download shortlist; drill into per-domain entries.",
                    "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    # one domain entry per catalog file
    for cat in cats:
        full = os.path.join(ROOT, "catalog", cat["slug"] + ".md")
        if not os.path.exists(full):
            continue
        nmodels = c.execute("SELECT COUNT(*) FROM models WHERE category_id=?", (cat["id"],)).fetchone()[0]
        t, l = est(full)
        kw = list(KW.get(cat["slug"], []))
        for (nm,) in c.execute("SELECT name FROM models WHERE category_id=? AND status='recommended' "
                               "ORDER BY download_priority LIMIT 4", (cat["id"],)):
            for w in re.split(r"[^a-z0-9]+", (nm or "").lower()):
                if len(w) > 2 and w not in kw and w not in STOP:
                    kw.append(w)
        summ = f"{cat['name']}: {nmodels} models. {cat['description']}"[:120]
        entries.append({"id": cat["slug"], "path": f"catalog/{cat['slug']}.md", "keywords": kw,
                        "patterns": PAT.get(cat["slug"], []), "priority": "domain", "summary": summ,
                        "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    # wave docs
    wave_docs = [
        ("wave-01-dispatch", "waves/wave-01-foundation/dispatch.md",
         ["download", "recommend", "recommended", "license", "commercial", "shortlist", "plan", "best", "priority"],
         ["re_download", "commercial_safe", "game_asset"],
         "Wave-1 narrative: findings + the ordered re-download plan by priority."),
        ("wave-01-verification", "waves/wave-01-foundation/verification.md",
         ["verify", "verification", "license", "correction", "source", "citation", "superseded", "trust"],
         ["verification"],
         "Wave-1 verifier receipt: verdicts, license corrections, currency flags, wave-2 candidates."),
    ]
    for wid, wpath, kw, pat, summ in wave_docs:
        full = os.path.join(ROOT, wpath.replace("/", os.sep))
        if not os.path.exists(full):
            continue
        t, l = est(full)
        entries.append({"id": wid, "path": wpath, "keywords": kw, "patterns": pat, "priority": "domain",
                        "summary": summ[:120], "triggers": {"task": True, "plan": True, "edit": False},
                        "tokens_est": t, "lines": l})

    # manual — raw json, never auto-loaded
    full = os.path.join(ROOT, "waves", "wave-01-foundation", "research-raw.json")
    if os.path.exists(full):
        t, l = est(full)
        entries.append({"id": "wave-01-raw", "path": "waves/wave-01-foundation/research-raw.json",
                        "keywords": ["raw", "json"], "patterns": [], "priority": "manual",
                        "summary": "Raw verified wave-1 swarm output (large) — manual lookup only.",
                        "triggers": {"task": False, "plan": False, "edit": False}, "tokens_est": t, "lines": l})

    core = sum(e["tokens_est"] for e in entries if e["priority"] == "core")
    ondemand = sum(e["tokens_est"] for e in entries if e["priority"] != "core")
    domain_toks = sorted((e["tokens_est"] for e in entries if e["priority"] == "domain"), reverse=True)
    avg = core + sum(domain_toks[:2])  # orientation + ~2 matched domain entries
    index = {"version": "1.0.0", "generated": date + "T00:00:00Z",
             "source": f"models.db (wave {wave})", "lazyLoad": True,
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
