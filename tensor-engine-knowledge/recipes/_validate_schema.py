#!/usr/bin/env python3
"""Prove the PROPOSED recipe schema (recipes.schema.sql) is polymorphic enough to hold the
three archetypes the engine-room adversarial pass said the original (launchable+port+tok/s)
schema CANNOT represent. Scratch only — builds a throwaway in-memory DB, inserts exemplars
grounded in REAL wave-4/5 measured data, runs the queries that would have failed before.

Run:  $env:PYTHONUTF8='1'; python recipes/_validate_schema.py
Exits 0 on PASS. Touches nothing on disk and never opens engines.db.
"""
import os, sqlite3, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(HERE, "recipes.schema.sql")

STUBS = """
CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, slug TEXT UNIQUE, name TEXT, sort INTEGER);
CREATE TABLE IF NOT EXISTS engines    (id INTEGER PRIMARY KEY, slug TEXT UNIQUE, name TEXT);
CREATE TABLE IF NOT EXISTS waves       (id INTEGER PRIMARY KEY, wave_number INTEGER, title TEXT);
INSERT INTO categories(id,slug,name,sort) VALUES
  (1,'llm-inference','LLM inference engines',10),(2,'quantization','Quantization',30),
  (3,'attention-kernels','Attention backends & GPU kernels',40),(4,'diffusion-engines','Diffusion',60);
INSERT INTO waves(id,wave_number,title) VALUES (5,15,'recipe-layer demo');
"""


def main():
    con = sqlite3.connect(":memory:")
    con.execute("PRAGMA foreign_keys=ON")
    con.executescript(STUBS)
    with open(SCHEMA, encoding="utf-8") as f:
        con.executescript(f.read())
    cur = con.cursor()

    def recipe(**k):
        cols = ",".join(k); qs = ",".join("?" * len(k))
        cur.execute(f"INSERT INTO recipes({cols}) VALUES({qs})", tuple(k.values()))
        return cur.lastrowid

    # ── 1. LAUNCHABLE-SERVER — llama.cpp -> llama-swap (wave 5: prebuilt b9484, native-Windows) ──
    r1 = recipe(slug="llamacpp-llamaswap-blackwell-cu12.8", name="llama.cpp + llama-swap (native-Win Blackwell, CUDA 12.8)",
                engine_slug="llama-cpp", category_id=1, recipe_kind="launchable-server",
                backend_kind="native-win-compile", measured_axis="tok_s", toolchain_ref="cuda-12.8-sm120",
                summary="Prebuilt CUDA-12 llama.cpp + llama-swap name-routed serving with TTL VRAM reclaim",
                verified=1, resolvable_ok=1, resolvable_checked="2026-06-06", wave_id=5, created_date="2026-06-06")
    # break #3 fix: baselines are MODEL-keyed, and carry a semantic COMPAT BAND not a literal driver
    cur.executemany("""INSERT INTO recipe_baselines
        (recipe_id,model_name,model_quant,context_len,axis,bound_dir,value,unit,vram_peak_gb,compat_band,measured_date,measured_note,verified)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,1)""", [
        (r1,"Qwen3-30B-A3B","Q4_K_M",4096,"tok_s","lower",334.0,"tg tok/s",None,
         "driver>=R570; cuda_toolkit==12.8; sm_120; os=native-win","2026-06-03","llama-bench tg128; MMQ confirmed (pp512=7251)"),
        (r1,"Qwen3-4B","Q4_K_M",4096,"tok_s","lower",286.0,"warm tok/s",None,
         "driver>=R570; cuda_toolkit==12.8; sm_120; os=native-win","2026-06-03","llama-swap warm decode"),
    ])
    cur.executemany("INSERT INTO recipe_constraints(recipe_id,ctype,expr,reason) VALUES(?,?,?,?)", [
        (r1,"capability","gpu_arch>=sm_120","desktop Blackwell"),
        (r1,"requires_when","cuda_toolkit==12.8","13.x MMQ segfaults sm_120 -> 5.7x slower cuBLAS fallback"),
        (r1,"conflicts_when","cuda_toolkit>=13.0","known-wrong: silent MMQ fallback"),
    ])
    # break #-repro fix: the pin is a deletion-prone GitHub release asset -> MUST be vendored, not index
    cur.execute("""INSERT INTO recipe_artifacts(recipe_id,kind,ref,sha256,store_expect,resolvable_ok,checked_date,note)
        VALUES(?,?,?,?,?,?,?,?)""",
        (r1,"release-asset","github.com/ggml-org/llama.cpp/releases/.../llama-b9484-bin-win-cuda-12.x64.zip",
         "<sha256>","local-vendored",1,"2026-06-06","release assets get GC'd -> vendor to _artifact-cache"))
    # break compensator fix: NO global PATH mutation; per-instance shim. discard_staging is a real undo.
    cur.executemany("""INSERT INTO recipe_compensators(recipe_id,step,undo_cmd,post_state,owner,compensatable,note)
        VALUES(?,?,?,?,?,?,?)""", [
        (r1,"materialize (unzip prebuilt)","rm -r E:/engines/llama-cpp/<instance_id>","staging dir gone","executor-module","auto","disposable unit"),
        (r1,"register (launch shim)","rm E:/engines/bin/llama-server-<slug>.cmd","shim removed; global PATH never touched","executor-module","auto","per-instance shim, NOT setx PATH"),
        (r1,"activate (start server)","stop iff /health cookie matches; else halt-and-ask","server stopped iff identity matches","executor-module","auto","identity-verify before kill (PID reuse safe)"),
    ])
    cur.execute("INSERT INTO recipe_golden(recipe_id,modality,spec_json,note) VALUES(?,?,?,?)",
        (r1,"numeric",'{"prompt":"2+2=","n_tokens":4,"atol":0.0}',"LLM lane: deterministic next-token golden"))

    # ── 2. BATCH-PRODUCER — GGUF imatrix quantize (terminates after writing a file; no port) ──
    r2 = recipe(slug="gguf-imatrix-quantize", name="Quantize HF model -> GGUF with imatrix (best low-bit quality)",
                engine_slug="llama-cpp", category_id=2, recipe_kind="batch-producer",
                backend_kind="venv", measured_axis="bits_per_weight", toolchain_ref="cuda-12.8-sm120",
                summary="convert_hf_to_gguf + imatrix + quantize; deliverable is a .gguf file, not a server",
                verified=1, resolvable_ok=1, resolvable_checked="2026-06-06", wave_id=5, created_date="2026-06-06")
    cur.execute("INSERT INTO recipe_targets(recipe_id,relation,target_slug,note) VALUES(?,?,?,?)",
        (r2,"produces","gguf","the artifact this recipe yields"))
    cur.executemany("""INSERT INTO recipe_baselines(recipe_id,model_name,axis,bound_dir,value,unit,measured_date,measured_note,verified)
        VALUES(?,?,?,?,?,?,?,?,1)""", [
        (r2,"Qwen3-4B","bits_per_weight","upper",4.5,"bpw","2026-06-06","Q4_K_M target size"),
        (r2,"Qwen3-4B","build_wall_clock","upper",600.0,"s","2026-06-06","convert+imatrix+quantize wall time"),
    ])  # axis is NOT tok/s (break #2)
    cur.execute("INSERT INTO recipe_golden(recipe_id,modality,spec_json,note) VALUES(?,?,?,?)",
        (r2,"file-hash",'{"artifact":"gguf","verify":["sha256","perplexity<=baseline+0.1"]}',
         "producer golden: file integrity + perplexity tolerance, NOT torch.allclose"))
    cur.execute("""INSERT INTO recipe_compensators(recipe_id,step,undo_cmd,post_state,owner,compensatable,note)
        VALUES(?,?,?,?,?,?,?)""",
        (r2,"materialize (uv venv)","rm -r E:/engines/gguf-quant/<instance_id> (NEVER pip-uninstall)",
         "venv + per-instance caches gone","executor-module","auto","caches pinned under instance dir so rm reclaims them"))

    # ── 3. MODIFIER — SageAttention 2.2 (no port, no self-baseline; a DELTA on another recipe) ──
    r3 = recipe(slug="sageattention-2.2-comfyui", name="SageAttention 2.2 (ComfyUI attention overlay)",
                engine_slug="sageattention", category_id=3, recipe_kind="modifier",
                backend_kind=None,                       # break #1: a modifier has NO backend of its own
                measured_axis="delta_pct", toolchain_ref="cuda-13.0-sm120",
                summary="Drop-in attention backend; speeds a diffusion recipe by a measured DELTA, serves nothing",
                verified=1, resolvable_ok=1, resolvable_checked="2026-06-06", wave_id=5, created_date="2026-06-06")
    cur.execute("INSERT INTO recipe_targets(recipe_id,relation,target_slug,note) VALUES(?,?,?,?)",
        (r3,"modifies","comfyui-zimage-turbo","patches the base diffusion recipe; baseline is a delta vs ITS instance_id"))
    cur.executemany("""INSERT INTO recipe_baselines(recipe_id,model_name,context_len,axis,bound_dir,value,unit,measured_date,measured_note,verified)
        VALUES(?,?,?,?,?,?,?,?,?,1)""", [
        (r3,"Z-Image-Turbo",1024,"delta_pct","upper",8.3,"% faster vs cuDNN-SDPA","2026-06-03","gain scales with attention share"),
        (r3,"Z-Image-Turbo",2048,"delta_pct","upper",29.3,"% faster vs cuDNN-SDPA","2026-06-03","attention-dominated -> bigger win"),
    ])
    cur.executemany("INSERT INTO recipe_constraints(recipe_id,ctype,expr,reason) VALUES(?,?,?,?)", [
        (r3,"abi_equal","wheel.torch_abi==env.torch_abi","SA wheel pinned to a torch build; ABI mismatch = DLL load fail"),
        (r3,"conflicts_when","backend==sageattn_qk_int8_pv_fp16_cuda","HARD-CRASHES ComfyUI on Z-Image/Qwen-Image; fp8_cuda is the safe backend"),
    ])
    cur.execute("""INSERT INTO recipe_artifacts(recipe_id,kind,ref,sha256,store_expect,abi_tuple,resolvable_ok,checked_date,note)
        VALUES(?,?,?,?,?,?,?,?,?)""",
        (r3,"release-asset","github.com/woct0rdho/SageAttention/releases/.../cp39-abi3-cu130torch2.9.whl",
         "<sha256>","local-vendored","cp39-abi3 / torch2.9+ / cu130",1,"2026-06-06","community wheel = deletion-prone -> vendor"))

    con.commit()

    # ─────────────────── PROVE IT ───────────────────
    ok = True
    print("=== polymorphism: one schema, four recipe kinds ===")
    for k, n in cur.execute("SELECT recipe_kind, COUNT(*) FROM recipes GROUP BY recipe_kind"):
        print(f"  {k:18s} {n}")

    print("\n=== v_recipes headline (note: modifier backend_kind is NULL, axis varies per recipe) ===")
    for row in cur.execute("SELECT slug,recipe_kind,COALESCE(backend_kind,'(inherits target)'),measured_axis,n_baselines,n_pins FROM v_recipes"):
        print(f"  {row[0]:34s} {row[1]:16s} {row[2]:20s} axis={row[3]:14s} baselines={row[4]} pins={row[5]}")

    # break #1: a modifier is representable — has a target + a DELTA baseline + no backend
    m = cur.execute("""SELECT r.backend_kind, t.relation, t.target_slug, b.value, b.unit
                       FROM recipes r JOIN recipe_targets t ON t.recipe_id=r.id
                       JOIN recipe_baselines b ON b.recipe_id=r.id
                       WHERE r.recipe_kind='modifier' ORDER BY b.value DESC LIMIT 1""").fetchone()
    print(f"\n[break#1] modifier: backend={m[0]} relation={m[1]}->{m[2]} top-delta={m[3]}{m[4]}")
    ok &= (m[0] is None and m[1] == "modifies")

    # break #2: a producer is representable — produces an artifact, axis is NOT tok/s, golden is file-hash
    p = cur.execute("""SELECT r.measured_axis, t.target_slug, g.modality
                       FROM recipes r JOIN recipe_targets t ON t.recipe_id=r.id
                       JOIN recipe_golden g ON g.recipe_id=r.id
                       WHERE r.recipe_kind='batch-producer'""").fetchone()
    print(f"[break#2] producer: axis={p[0]} produces={p[1]} golden={p[2]}")
    ok &= (p[0] != "tok_s" and p[1] == "gguf" and p[2] == "file-hash")

    # break #3: baselines are model-keyed — same recipe, two models, two different floors
    rows = cur.execute("""SELECT model_name,value,compat_band FROM recipe_baselines b
                          JOIN recipes r ON r.id=b.recipe_id
                          WHERE r.recipe_kind='launchable-server' AND b.axis='tok_s'""").fetchall()
    print(f"[break#3] launchable: {len(rows)} model-keyed tok/s baselines (compat-band, not literal driver):")
    for mn, v, cb in rows:
        print(f"            {mn:14s} {v} tok/s   band='{cb}'")
    ok &= (len(rows) >= 2 and all(cb and "driver>=" in cb for _, _, cb in rows))

    # repro floor: any 'index'-only pin is NOT reproducible; ours are all vendored
    bad = cur.execute("SELECT COUNT(*) FROM recipe_artifacts WHERE store_expect='index'").fetchone()[0]
    print(f"\n[repro]   index-only (non-reproducible) pins: {bad}  (all exemplars vendored)")
    ok &= (bad == 0)

    # compensator honesty: no recipe mutates global PATH; non-compensatable ops would be NAMED (none here)
    path_mut = cur.execute("SELECT COUNT(*) FROM recipe_compensators WHERE undo_cmd LIKE '%setx%' OR step LIKE '%PATH%'").fetchone()[0]
    print(f"[comp]    global-PATH-mutating steps: {path_mut}  (per-instance shims instead)")
    ok &= (path_mut == 0)

    print("\n" + ("PASS - the typed schema holds launchable + producer + modifier; the three HIGH breaks are representable."
                  if ok else "FAIL - an archetype did not round-trip."))
    con.close()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
