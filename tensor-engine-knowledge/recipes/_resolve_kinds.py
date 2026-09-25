#!/usr/bin/env python3
"""Goal 4 + finish Goal 3: carve out non-engine rows, then sharper end-state re-classify with
a 3-METHOD CONSENSUS verified flag.

(1) CARVE-OUT: rows that aren't provisionable engine recipes get executable=0:
    - measurement receipts (profiling-bench rig measurements: idle/baseline/soak/loadout/context/calibration/fans)
    - tooling/reference (offload CLI, verifier/NLI wiring, decision matrices, crew-serving-decision)
(2) SHARPER RE-CLASSIFY (executable rows only): a deterministic END-STATE classifier that encodes
    what the panel taught — training->batch-producer, serving/inference->launchable-server,
    routers->router-fleet, kernels/overlays/toolchain->modifier, build-an-artifact->batch-producer.
(3) CONSENSUS verified: three mechanistically-different classifiers — backfill (keyword regex),
    panel (3-family LLM), end-state (these rules). verified=1 iff the end-state kind agrees with at
    least one prior method on record (>=2 of 3 agree); else verified=0 (genuine 3-way split, review).

Idempotent. Run:  $env:PYTHONUTF8='1'; python recipes/_resolve_kinds.py
"""
import os, re, sqlite3

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")
AXIS = {"launchable-server": "tok_s", "batch-producer": "build_wall_clock", "modifier": "delta_pct", "router-fleet": "none"}

# --- carve-out detection -----------------------------------------------------
# reference/tooling slug markers — PRECISE (note: bare 'offload' would wrongly hit RAM/CPU-offload
# engine recipes like partial-offload / moe-cpu-offload / fsdp2-cpuoffload, which ARE engine recipes)
REF = ["tool-offload", "offload-local", "offload-panel", "offload-compress", "offload-ollama", "offload-real-wave",
       "verifier", "nli-floor", "numeric-floor", "numeric-unit-floor", "orthogonal-nli", "citation-panel",
       "format-to-consumer", "producer-format-consumer", "decision", "survival-card", "crew-pattern"]
def carve_reason(cat, slug, name):
    s = slug.lower()
    if cat == "profiling-bench" and any(k in s for k in ["baseline", "soak", "idle", "loadout", "context-capability", "calibration", "fans", "bytefit-predicted"]):
        return "measurement receipt — belongs as recipe_baselines, not a provisioning recipe"
    if any(k in s for k in REF):
        return "tooling/reference note — not an engine to provision"
    return None

# --- sharper end-state classifier (executable rows) --------------------------
def sharper_kind(cat, slug, name, body):
    t = (name + " " + (body or "")).lower(); s = slug.lower()
    if any(k in s for k in ["llama-swap", "litellm", "router-mode"]) or ("router mode" in t) or (" proxy" in t and "rout" in t):
        return "router-fleet"
    if cat == "training" or any(k in s for k in ["kohya", "unsloth", "qlora", "-lora", "finetune", "fine-tune",
                                                 "-sft", "-dpo", "-grpo", "-orpo", "-kto", "rlhf", "trl-", "axolotl",
                                                 "llama-factory", "verl", "openrlhf", "ms-swift"]):
        return "batch-producer"
    if cat == "quantization":
        if "serve" in s or "tabbyapi" in s:        # a quant-lane recipe whose job is SERVING the quant
            return "launchable-server"
        if any(k in t for k in ["quantize", "imatrix", "export", "convert", "produce", "checkpoint"]):
            return "batch-producer"
        return "batch-producer"
    if any(k in t for k in ["tensorrt", "onnx", "trtexec"]) and any(k in t for k in ["build", "compile", "export", "convert"]):
        return "batch-producer"
    if cat == "profiling-bench":   # non-carved profiling = a tool that RUNS and produces a measurement
        return "batch-producer"
    if cat == "attention-kernels" or any(k in t for k in ["sageattention", "flashattention", "flashinfer",
                                                          "attention backend", "--use-sage", "first block cache",
                                                          "wavespeed", "nunchaku", "torchao"]):
        return "modifier"
    if cat in ("llm-inference", "llm-serving", "speech-engines", "diffusion-engines", "structured-output"):
        if any(k in t for k in ["export to onnx", "export-to-onnx"]):
            return "batch-producer"
        return "launchable-server"
    if cat == "runtime-foundations":
        if "llama" in s and ("serve" in t or "server" in t):
            return "launchable-server"
        if any(k in t for k in ["tensorrt", "onnx"]):
            return "batch-producer"
        return "modifier"   # pytorch/cuda/triton install = toolchain setup
    return "launchable-server"

def classify_backend(kind, t):
    if kind == "modifier": return None
    if any(k in t for k in ["wsl2", "wsl ", "docker", "vllm", "sglang", "lmdeploy", "aphrodite"]): return "wsl2-docker"
    if any(k in t for k in ["portable", "run_nvidia_gpu", "python_embeded"]): return "portable-bundle"
    if any(k in t for k in ["onnx", "tensorrt", ".engine", "trtexec"]): return "onnx-compile"
    if kind == "router-fleet" or "litellm" in t or " proxy" in t: return "python-proxy"
    if any(k in t for k in ["uv venv", "uv pip", "venv", "pip install", "conda "]): return "venv"
    if any(k in t for k in ["cmake", "-dggml", "from source", "msvc", "cargo", "prebuilt", ".whl", "wheel", "cu128", "cu130", "cuda 12.8"]): return "native-win-compile"
    return None

DISP = re.compile(r"backfill=(\S+), panel suggested (\S+)")
SPLIT = re.compile(r"panel-split: (\{.*\})")

def priors_for(kind, verified, note):
    """The kinds proposed by the prior methods (backfill + panel) on record for this row."""
    if not note:                      # panel-confirmed (backfill==panel) OR clean reclassify
        return {kind}
    m = DISP.search(note)
    if m:                             # disputed: backfill + panel suggestion
        return {m.group(1), m.group(2)}
    if note.startswith("panel-split"):
        pr = {kind}                   # current kind is the backfill kind (splits weren't corrected)
        ms = SPLIT.search(note)
        if ms:
            for k in ("launchable-server", "batch-producer", "modifier", "router-fleet"):
                if f"'{k}'" in ms.group(1):
                    pr.add(k)
        return pr
    return {kind}

def main():
    con = sqlite3.connect(DB); cur = con.cursor()
    try:
        cur.execute("ALTER TABLE recipes ADD COLUMN executable INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass  # already added
    cur.execute("UPDATE recipes SET executable=1")   # reset so carve-out is idempotent (un-carves prior false hits)
    cats = {cid: slug for cid, slug in cur.execute("select id, slug from categories")}
    rows = cur.execute("select id, slug, name, category_id, recipe_kind, verified, verify_note, body from recipes").fetchall()

    carved = []
    for rid, slug, name, cat_id, kind, verified, note, body in rows:
        cat = cats.get(cat_id, "")
        reason = carve_reason(cat, slug, name)
        if reason:
            cur.execute("update recipes set executable=0, verified=0, verify_note=? where id=?",
                        (f"out-of-taxonomy: {reason}", rid))
            carved.append((cat, kind, slug[:54], reason.split(" — ")[0]))

    # re-classify the executable rows with consensus verified
    reclass = []
    vcount = 0
    for rid, slug, name, cat_id, kind, verified, note, body in rows:
        cat = cats.get(cat_id, "")
        if carve_reason(cat, slug, name):
            continue
        s_kind = sharper_kind(cat, slug, name, body)
        priors = priors_for(kind, verified, note)
        agree = s_kind in priors
        t = (name + " " + (body or "")).lower()
        nb = None if s_kind == "modifier" else classify_backend(s_kind, t)
        if agree:
            nn = None; v = 1; vcount += 1
        else:
            nn = f"3-way split: backfill/panel={sorted(priors)} vs end-state={s_kind} — review"; v = 0
        if s_kind != kind:
            reclass.append((kind, s_kind, "✓" if agree else "✗", slug[:50]))
        cur.execute("update recipes set recipe_kind=?, measured_axis=?, backend_kind=?, verified=?, verify_note=? where id=?",
                    (s_kind, AXIS[s_kind], nb, v, nn, rid))
    con.commit()

    print(f"=== CARVE-OUT (executable=0): {len(carved)} rows ===")
    for cat, kind, slug, reason in carved:
        print(f"  [{cat:16s}] {slug:54s} {reason}")
    print(f"\n=== RE-CLASSIFIED (end-state changed the kind): {len(reclass)} ===")
    for old, new, ok, slug in reclass:
        print(f"  {ok} {old:16s} -> {new:18s} {slug}")
    print(f"\nexecutable recipes: {cur.execute('select count(*) from recipes where executable=1').fetchone()[0]}")
    print("kind distribution (executable only):")
    for k, n in cur.execute("select recipe_kind,count(*) from recipes where executable=1 group by recipe_kind order by 2 desc"):
        print(f"  {k:18s} {n}")
    n_exec = cur.execute("select count(*) from recipes where executable=1").fetchone()[0]
    n_disp = cur.execute("select count(*) from recipes where executable=1 and verified=0").fetchone()[0]
    print(f"verified=1 (>=2 of 3 methods agree): {vcount} / {n_exec} executable")
    print(f"still disputed (verified=0, executable): {n_disp}")
    con.close()

if __name__ == "__main__":
    main()
