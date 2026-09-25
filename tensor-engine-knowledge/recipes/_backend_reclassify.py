#!/usr/bin/env python3
"""Re-classify backend_kind with a NEGATION-AWARE end-state classifier.

The original classify_backend was keyword-blind: "ExLlamaV3 ... WITHOUT WSL2" -> wsl2-docker
(it saw the substring 'wsl2'). backend drives the executor's provider dispatch, so it must
distinguish "the engine RUNS IN wsl2" (-> wsl2-docker) from "native Windows, NO wsl2" (-> native).

Default = DRY-RUN: print the current->new diff + body excerpts for changed rows. Pass --apply to write.

Run:  $env:PYTHONUTF8='1'; python recipes/_backend_reclassify.py [--apply]
"""
import os, sys, sqlite3

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")

def backend_for(kind, name, body):
    if kind == "modifier":
        return None                       # a modifier inherits its target's backend
    t = (name + " " + (body or "")).lower()

    # WSL2 disambiguation — the load-bearing fix
    needs_wsl = any(p in t for p in [
        "no native windows", "has no native windows", "not supported on windows",
        "windows is not supported", "linux-first", "wsl2 only", "wsl2-only",
        "wsl2/docker", "wsl/docker", "docker/wsl2"])
    runs_native = any(p in t for p in [
        "without wsl2", "no wsl2", "no-wsl2", "native windows", "native-windows",
        "windows-native", "windows native", "not wsl2", "no wsl"])
    in_wsl = any(p in t for p in [
        "in wsl2", "under wsl2", "inside wsl2", "wsl2 ubuntu", "wsl2 (ubuntu",
        "ubuntu on wsl2", "run it in wsl2", "run under wsl2", "run in wsl2"])
    docker = "docker " in t or "@sha256" in t or "docker compose" in t

    # most specific first
    if any(p in t for p in ["tensorrt", "trtexec", ".engine"]) and any(p in t for p in ["onnx", "build", "compile", "export"]):
        return "onnx-compile"
    if any(p in t for p in ["portable build", "windows portable", "run_nvidia_gpu", "python_embeded", "embedded python"]):
        return "portable-bundle"
    if any(p in t for p in ["litellm", "llama-swap"]):
        return "python-proxy"
    # WSL2: positive context AND not explicitly native
    if needs_wsl or ((in_wsl or docker) and not runs_native):
        return "wsl2-docker"
    # compiled / prebuilt-wheel ENGINE on native Windows
    if any(p in t for p in ["cmake", "-dggml", "cargo", "prebuilt", "cu128 wheel", "cu130 wheel",
                            ".whl", "from source", "msvc", "llama.cpp", "exllama", "mistral.rs",
                            "build/bin", "tabbyapi"]):
        return "native-win-compile"
    # python venv tool/framework
    if any(p in t for p in ["uv venv", "uv pip", "kohya", "unsloth", "sd-scripts", "diffusers",
                            "trl", "peft", "pip install", "venv", "conda "]):
        return "venv"
    if runs_native:
        return "native-win-compile"
    return "raw-cmd"

def main():
    apply = "--apply" in sys.argv
    con = sqlite3.connect(DB); con.execute("PRAGMA foreign_keys=ON"); cur = con.cursor()
    rows = cur.execute("""select id, slug, name, recipe_kind, backend_kind, body
                          from recipes where executable=1 and recipe_kind!='modifier' order by slug""").fetchall()
    diff = []
    for rid, slug, name, kind, cur_b, body in rows:
        nb = backend_for(kind, name, body)
        if nb != cur_b:
            diff.append((rid, slug, cur_b, nb, " ".join((body or "").split())[:130]))
        if apply and nb != cur_b:
            cur.execute("update recipes set backend_kind=? where id=?", (nb, rid))
    if apply:
        con.commit()
    print(f"executable non-modifier recipes: {len(rows)}")
    print(f"backend changes: {len(diff)}\n")
    for rid, slug, old, new, ex in diff:
        print(f"  {(old or 'None'):18s} -> {new:18s} {slug[:46]}")
        print(f"        {ex}")
    print(f"\n{'APPLIED' if apply else 'DRY-RUN (pass --apply to write)'}")
    print("backend distribution (executable non-modifier):")
    for b, n in cur.execute("""select coalesce(backend_kind,'None'),count(*) from recipes
                               where executable=1 and recipe_kind!='modifier' group by backend_kind order by 2 desc"""):
        print(f"  {b:18s} {n}")
    con.close()

if __name__ == "__main__":
    main()
