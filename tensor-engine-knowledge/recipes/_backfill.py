#!/usr/bin/env python3
"""Backfill the 177 prose config_recipes into the typed `recipes` layer.

Deterministic v1: classify recipe_kind / backend_kind / measured_axis from
category + name/body keywords, carry engine_slug + wave_id + the prose body
verbatim, and parse measured numbers from kind='baseline' rows into
recipe_baselines. Low-confidence classifications get a verify_note ending in '?'
so the LLM/Mike refinement pass (constraints + artifacts from prose) can target them.

Idempotent: clears the recipe layer first (FK ON DELETE CASCADE), re-runnable.
recipes.slug reuses config_recipes.slug for traceability.

Run:  $env:PYTHONUTF8='1'; python recipes/_backfill.py
"""
import os, re, sqlite3

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")

def classify_kind(cat, t):
    if any(k in t for k in ['llama-swap', 'litellm', 'router mode', ' proxy', 'route to', 'front-door', 'front door', 'multi-model']):
        return 'router-fleet', 'kw:router'
    if cat == 'training' or any(k in t for k in ['quantize', 'imatrix', 'convert_hf', 'gptqmodel', 'autoawq', 'nvfp4 checkpoint', 'export_path', ' lora', 'finetune', 'fine-tune', 'qlora', 'train ']):
        return 'batch-producer', 'kw:producer'
    if cat == 'attention-kernels' or any(k in t for k in ['sageattention', 'flashattention', 'flashinfer', 'attention backend', '--use-sage', 'first block cache', 'wavespeed', 'nunchaku', 'torchao', 'overlay', ' kernel']):
        return 'modifier', 'kw:modifier'
    if cat in ('llm-inference', 'llm-serving', 'speech-engines', 'diffusion-engines', 'structured-output'):
        return 'launchable-server', 'cat:server'
    if cat == 'runtime-foundations':
        return 'modifier', 'cat:runtime?'        # substrate/setup — low confidence
    if cat == 'profiling-bench':
        return 'batch-producer', 'cat:profiling?' # benchmarks produce a measurement
    if cat == 'quantization':
        return 'batch-producer', 'cat:quant'
    return 'launchable-server', 'default?'

def classify_backend(kind, t):
    if kind == 'modifier':
        return None                               # inherits target's backend
    if any(k in t for k in ['wsl2', 'wsl ', 'docker', 'vllm', 'sglang', 'lmdeploy', 'aphrodite']): return 'wsl2-docker'
    if any(k in t for k in ['portable', 'run_nvidia_gpu', 'python_embeded', 'embedded python']): return 'portable-bundle'
    if any(k in t for k in ['onnx', 'tensorrt', '.engine', 'trtexec']): return 'onnx-compile'
    if kind == 'router-fleet' or 'litellm' in t or ' proxy' in t: return 'python-proxy'
    if any(k in t for k in ['uv venv', 'uv pip', 'venv', 'pip install', 'conda ']): return 'venv'
    if any(k in t for k in ['cmake', '-dggml', 'from source', 'msvc', 'cargo', 'prebuilt', '.whl', 'wheel', 'cu128', 'cu130', 'cuda 12.8']): return 'native-win-compile'
    return None

AXIS = {'launchable-server': 'tok_s', 'batch-producer': 'build_wall_clock', 'modifier': 'delta_pct', 'router-fleet': 'none'}

# baseline number parsing — (regex, axis, unit, bound)
BPATS = [
    (re.compile(r'([\d.]+)\s*tok/s', re.I), 'tok_s', 'tok/s', 'lower'),
    (re.compile(r'([\d.]+)\s*t/s', re.I), 'tok_s', 'tok/s', 'lower'),
    (re.compile(r'([\d.]+)\s*s/img', re.I), 's_per_img', 's/img', 'upper'),
    (re.compile(r'([\d.]+)\s*it/s', re.I), 'it_s', 'it/s', 'lower'),
    (re.compile(r'([\d.]+)\s*GB', re.I), 'vram', 'GB', 'upper'),
]
MODEL = re.compile(r'(qwen[\w.\-]*|gemma[\w.\-]*|chroma[\w.\-]*|z-image[\w.\-]*|qwen-image[\w.\-]*|granite[\w.\-]*|llama[\w.\-]*|sdxl|flux[\w.\-]*)', re.I)

def parse_baseline(body):
    out = []
    if not body:
        return out
    model = None
    m = MODEL.search(body)
    if m:
        model = m.group(1)
    for pat, axis, unit, bound in BPATS:
        mm = pat.search(body)
        if mm and axis != 'vram':
            try:
                out.append((model, axis, bound, float(mm.group(1)), unit))
            except ValueError:
                pass
    return out

def main():
    con = sqlite3.connect(DB); con.execute('PRAGMA foreign_keys=ON')
    cur = con.cursor()
    cur.execute('DELETE FROM recipes')             # cascade clears recipe_* children

    cats = {cid: slug for cid, slug in cur.execute('select id, slug from categories')}
    eng_slug = {eid: slug for eid, slug in cur.execute('select id, slug from engines')}

    rows = cur.execute(
        'select id, slug, name, category_id, engine_id, kind, url, body, wave_id from config_recipes').fetchall()

    n_rec = n_base = 0
    kind_dist, backend_dist, lowconf = {}, {}, []
    for rid, slug, name, cat_id, eng_id, ckind, url, body, wave_id in rows:
        cat = cats.get(cat_id, '')
        t = (name + ' ' + (body or '')).lower()
        kind, knote = classify_kind(cat, t)
        backend = classify_backend(kind, t)
        axis = AXIS[kind]
        es = eng_slug.get(eng_id)
        note = knote if knote.endswith('?') else None
        if note:
            lowconf.append((slug, cat, kind, knote))
        cur.execute(
            """INSERT INTO recipes(slug,name,engine_slug,category_id,recipe_kind,backend_kind,
               measured_axis,summary,body,verified,verify_note,wave_id,created_date)
               VALUES(?,?,?,?,?,?,?,?,?,0,?,?,?)""",
            (slug, name, es, cat_id, kind, backend, axis, None, body, note, wave_id, None))
        rec_id = cur.lastrowid
        n_rec += 1
        kind_dist[kind] = kind_dist.get(kind, 0) + 1
        backend_dist[backend or '(none)'] = backend_dist.get(backend or '(none)', 0) + 1
        if ckind == 'baseline':
            for model, baxis, bound, val, unit in parse_baseline(body):
                cur.execute(
                    """INSERT INTO recipe_baselines(recipe_id,model_name,axis,bound_dir,value,unit,measured_date,measured_note,verified)
                       VALUES(?,?,?,?,?,?,?,?,0)""",
                    (rec_id, model, baxis, bound, val, unit, None, 'parsed from prose body'))
                n_base += 1

    con.commit()
    print(f"backfilled {n_rec} recipes, {n_base} parsed baselines")
    print("\nrecipe_kind distribution:")
    for k, v in sorted(kind_dist.items(), key=lambda x: -x[1]):
        print(f"  {k:18s} {v}")
    print("\nbackend_kind distribution:")
    for k, v in sorted(backend_dist.items(), key=lambda x: -x[1]):
        print(f"  {k:20s} {v}")
    print(f"\nlow-confidence classifications flagged for review: {len(lowconf)}")
    for slug, cat, kind, knote in lowconf[:20]:
        print(f"  [{knote:14s}] {cat:20s} -> {kind:18s} {slug[:48]}")
    con.close()

if __name__ == "__main__":
    main()
