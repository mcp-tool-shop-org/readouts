#!/usr/bin/env python3
"""Adjudicate the 15 flagged (3-way-split) recipe_kinds by end-state judgment (the 4th method).
Resolves every dispute -> verified=1 with a one-line rationale. Idempotent (keyed by id).

Run:  $env:PYTHONUTF8='1'; python recipes/_adjudicate.py
"""
import os, sqlite3

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")
AXIS = {"launchable-server": "tok_s", "batch-producer": "build_wall_clock", "modifier": "delta_pct", "router-fleet": "none"}

# id -> (kind, axis_override|None, rationale)
DEC = {
    25:  ("modifier", "delta_pct", "RAM-offload launch-config overlay on llama.cpp/Ollama — modifies a base runtime"),
    2:   ("modifier", "delta_pct", "partial-offload launch config for llama.cpp — overlays a base runtime"),
    33:  ("modifier", "delta_pct", "GGUF partial-offload config for ComfyUI — overlays a base diffusion runtime"),
    102: ("batch-producer", "build_wall_clock", "AIPerf — runs and produces serving-metric receipts"),
    101: ("batch-producer", "build_wall_clock", "llama-bench — runs and produces throughput + optimal-flag receipts"),
    104: ("batch-producer", "build_wall_clock", "Nsight Systems — runs and produces a profiling trace"),
    106: ("batch-producer", "build_wall_clock", "py-spy — samples a running process and produces a profile"),
    105: ("batch-producer", "build_wall_clock", "torch.profiler — runs and exports a chrome trace"),
    103: ("batch-producer", "build_wall_clock", "vLLM bench — runs and produces serving metrics"),
    100: ("modifier", "delta_pct", "installs the profiling lane (venv) — environment/toolchain setup, no artifact"),
    107: ("launchable-server", "none", "Arize Phoenix — a long-running local observability server (no perf axis)"),
    130: ("launchable-server", "tok_s", "the working vLLM-nightly WSL2 install — end state is a serveable vLLM"),
    16:  ("launchable-server", "tok_s", "ExLlamaV3 + TabbyAPI — serves EXL3 on a port"),
    55:  ("launchable-server", "tok_s", "vLLM AWQ-Marlin in WSL2 — serves on a port"),
    82:  ("launchable-server", "tok_s", "KTransformers — serving runtime for frontier MoE (offload-backed)"),
}

def classify_backend(kind, t):
    if kind == "modifier": return None
    if any(k in t for k in ["wsl2", "wsl ", "docker", "vllm", "sglang"]): return "wsl2-docker"
    if any(k in t for k in ["portable", "run_nvidia_gpu", "python_embeded"]): return "portable-bundle"
    if any(k in t for k in ["onnx", "tensorrt", ".engine", "trtexec"]): return "onnx-compile"
    if any(k in t for k in ["uv venv", "uv pip", "venv", "pip install"]): return "venv"
    if any(k in t for k in ["cmake", "prebuilt", ".whl", "wheel", "cu128", "cu130"]): return "native-win-compile"
    return None

def main():
    con = sqlite3.connect(DB); con.execute("PRAGMA foreign_keys=ON"); cur = con.cursor()
    changed = 0
    for rid, (kind, axis, why) in DEC.items():
        row = cur.execute("select recipe_kind, name, body, backend_kind from recipes where id=?", (rid,)).fetchone()
        if not row:
            print(f"  #{rid} not found"); continue
        old, name, body, backend = row
        t = (name + " " + (body or "")).lower()
        nb = None if kind == "modifier" else (backend or classify_backend(kind, t))
        cur.execute("update recipes set recipe_kind=?, measured_axis=?, backend_kind=?, verified=1, verify_note=? where id=?",
                    (kind, axis, nb, f"adjudicated: {why}", rid))
        if old != kind:
            changed += 1
            print(f"  #{rid}: {old} -> {kind}")
    con.commit()
    print(f"\nadjudicated {len(DEC)} (changed {changed} kinds)")
    print("remaining disputed (executable, verified=0):",
          cur.execute("select count(*) from recipes where executable=1 and verified=0").fetchone()[0])
    print("executable kind distribution:")
    for k, n in cur.execute("select recipe_kind,count(*) from recipes where executable=1 group by recipe_kind order by 2 desc"):
        print(f"  {k:18s} {n}")
    print("verified=1 / executable:",
          cur.execute("select count(*) from recipes where executable=1 and verified=1").fetchone()[0], "/",
          cur.execute("select count(*) from recipes where executable=1").fetchone()[0])
    con.close()

if __name__ == "__main__":
    main()
