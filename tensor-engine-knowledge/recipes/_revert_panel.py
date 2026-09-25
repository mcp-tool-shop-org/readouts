#!/usr/bin/env python3
"""ANDON: revert the panel's 89 auto-corrections — they were not trustworthy enough to keep.

Meta-verification (reading corrections vs bodies) found the 3-family panel ~25% wrong (a
correlated TRAINING blind spot: kohya/unsloth PRODUCE a LoRA = batch-producer, but the panel
moved them to launchable/modifier on vllm/install keywords) + ~25% out-of-taxonomy force-fits
(CLIs, decision matrices, verifier-infra, measurement receipts are not engine recipes).

So: trust only AGREEMENT. The 64 the panel CONFIRMED stay verified=1. The 89 it CORRECTED revert
to the known backfill kind (parsed from the note), verified=0, with the panel's suggestion recorded
for a human review pass. Enrichment (summaries / constraints / artifacts / techniques) is untouched.

Run:  $env:PYTHONUTF8='1'; python recipes/_revert_panel.py
"""
import os, re, sqlite3

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")
AXIS = {"launchable-server": "tok_s", "batch-producer": "build_wall_clock", "modifier": "delta_pct", "router-fleet": "none"}
NOTE = re.compile(r"panel-corrected (\S+)->(\S+) \((\d)/3\)")

def classify_backend(kind, t):
    if kind == "modifier": return None
    if any(k in t for k in ["wsl2", "wsl ", "docker", "vllm", "sglang", "lmdeploy", "aphrodite"]): return "wsl2-docker"
    if any(k in t for k in ["portable", "run_nvidia_gpu", "python_embeded", "embedded python"]): return "portable-bundle"
    if any(k in t for k in ["onnx", "tensorrt", ".engine", "trtexec"]): return "onnx-compile"
    if kind == "router-fleet" or "litellm" in t or " proxy" in t: return "python-proxy"
    if any(k in t for k in ["uv venv", "uv pip", "venv", "pip install", "conda "]): return "venv"
    if any(k in t for k in ["cmake", "-dggml", "from source", "msvc", "cargo", "prebuilt", ".whl", "wheel", "cu128", "cu130", "cuda 12.8"]): return "native-win-compile"
    return None

def main():
    con = sqlite3.connect(DB); cur = con.cursor()
    rows = cur.execute("select id, name, body, verify_note from recipes where verify_note like 'panel-corrected%'").fetchall()
    reverted = 0
    for rid, name, body, note in rows:
        m = NOTE.search(note or "")
        if not m:
            continue
        old, new, wc = m.group(1), m.group(2), m.group(3)
        t = (name + " " + (body or "")).lower()
        nb = None if old == "modifier" else classify_backend(old, t)
        nn = f"panel-disputed: backfill={old}, panel suggested {new} ({wc}/3) — review"
        cur.execute("update recipes set recipe_kind=?, measured_axis=?, backend_kind=?, verified=0, verify_note=? where id=?",
                    (old, AXIS[old], nb, nn, rid))
        reverted += 1
    con.commit()
    print(f"reverted {reverted} panel corrections to backfill baseline (verified=0, disputed-note)")
    print("\nrecipe_kind distribution (restored baseline):")
    for k, n in cur.execute("select recipe_kind,count(*) from recipes group by recipe_kind order by 2 desc"):
        print(f"  {k:18s} {n}")
    print("\nverified=1 (panel CONFIRMED backfill — the trustworthy agreements):",
          cur.execute("select count(*) from recipes where verified=1").fetchone()[0], "/ 160")
    print("disputed (verified=0, needs review):",
          cur.execute("select count(*) from recipes where verify_note like 'panel-disputed%'").fetchone()[0])
    print("panel-split (verified=0):",
          cur.execute("select count(*) from recipes where verify_note like 'panel-split%'").fetchone()[0])
    con.close()

if __name__ == "__main__":
    main()
