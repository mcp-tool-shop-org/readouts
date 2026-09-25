#!/usr/bin/env python3
"""Re-classify backend_kind with a local LLM (contextual reading beats keyword matching).

backend is a "where does this engine actually run / how is it installed" question that hinges on
negation + context ("native Windows is UNSUPPORTED -> run under WSL2" = wsl2-docker; "native
Windows, NO WSL2" = native-win-compile) — exactly what a keyword classifier gets wrong. A local
model reads the body and picks. Default DRY-RUN (report current->LLM diff + reason). --apply writes.
An OVERRIDES dict lets me adjudicate specific rows after review (Claude is the final arbiter).

Run:  $env:PYTHONUTF8='1'; python recipes/_backend_llm.py [--apply]
"""
import os, sys, re, json, sqlite3, urllib.request

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "engines.db")
OLLAMA = "http://localhost:11434/api/generate"
MODEL = "mistral-small:24b"
VALID = {"native-win-compile", "wsl2-docker", "portable-bundle", "venv", "onnx-compile", "python-proxy", "raw-cmd"}

DEFS = (
  "native-win-compile = the engine is built-from-source or installed as a prebuilt compiled wheel/binary "
  "and runs on NATIVE Windows, no WSL2 (llama.cpp build, ExLlamaV3 cu128 wheel, mistral.rs, TabbyAPI on Windows, Ollama); "
  "wsl2-docker = the engine runs INSIDE WSL2 and/or Docker because Windows is unsupported (vLLM, SGLang, TEI, LMDeploy, "
  "Aphrodite, TensorRT-LLM); portable-bundle = a zip with its own embedded Python (ComfyUI portable); "
  "venv = a Python pip/uv venv tool on native Windows (kohya, Unsloth-native, diffusers/training scripts, "
  "pip-installed quantizers like gptqmodel/nvidia-modelopt/hqq); onnx-compile = compiles ONNX -> a TensorRT .engine "
  "(TensorRT-RTX); python-proxy = a routing front that proxies to OTHER engines (LiteLLM, llama-swap) — only if THIS "
  "recipe IS the proxy; raw-cmd = none of the above.")

GUIDE = ("Decide where the engine ACTUALLY runs. 'Native Windows is unsupported - run under WSL2' => wsl2-docker. "
         "'native Windows, no WSL2' / 'without WSL2' / 'no-compile prebuilt' => native-win-compile (or venv if a pure "
         "Python tool). Merely MENTIONING another tool (llama-swap, llama.cpp) as a component does NOT make this recipe "
         "that backend.")

PROMPT = ("Pick the single backend for this engine recipe. Backends: " + DEFS + "\n" + GUIDE +
          '\nRespond ONLY JSON: {{"backend":"<one>","reason":"<=12 words"}}.\n\nRecipe: {name}\nBody:\n{body}')

# Claude adjudication overrides applied after review (slug -> backend) — Claude is the final arbiter.
OVERRIDES = {
    "diffusion-chroma1-hd-fp8mixed-baseline-measured-5090": "portable-bundle",                 # runs in ComfyUI portable
    "diffusion-qwen-image-2512-fp8-baseline-and-sa-measured-5090": "portable-bundle",           # runs in ComfyUI portable
    "llm-serving-litellm-proxy-local-first-with-hosted-fallback-under-one-key-config-yaml": "python-proxy",  # IS the proxy
    "llm-serving-llama-swap-config-yaml-for-a-32-gb-vram-windows-rig-ttl-based-vram-reclaim-groups": "python-proxy",  # IS the router
    "runtime-foundations-ktransformers-deepseek-moe-offload-671b-class-moe-on-one-5090-64-gb-ram": "wsl2-docker",  # recipe: best in WSL2
    "training-ms-swift-dpo-preference-tuning-single-5090": "venv",                              # pip python framework
    "training-ms-swift-qlora-sft-7b-32gb-qwen3-lora-single-5090-windows-native": "venv",        # pip python framework
}

def ask(name, body):
    payload = {"model": MODEL, "prompt": PROMPT.format(name=name, body=(body or "")[:1900]),
               "stream": False, "think": False, "format": "json", "options": {"temperature": 0.1, "num_predict": 60}}
    req = urllib.request.Request(OLLAMA, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    out = json.loads(urllib.request.urlopen(req, timeout=120).read())["response"]
    try:
        j = json.loads(out)
    except Exception:
        m = re.search(r"\{.*\}", out, re.S); j = json.loads(m.group(0)) if m else {}
    b = (j.get("backend") or "").strip()
    return (b if b in VALID else "raw-cmd"), (j.get("reason") or "")[:60]

def main():
    apply = "--apply" in sys.argv
    con = sqlite3.connect(DB); con.execute("PRAGMA foreign_keys=ON"); cur = con.cursor()
    rows = cur.execute("""select id, slug, name, backend_kind, body from recipes
                          where executable=1 and recipe_kind!='modifier' order by slug""").fetchall()
    diff = []
    for rid, slug, name, cur_b, body in rows:
        nb = OVERRIDES.get(slug)
        why = "claude-override" if nb else None
        if nb is None:
            nb, why = ask(name, body)
        if nb != cur_b:
            diff.append((slug, cur_b, nb, why))
        if apply:
            cur.execute("update recipes set backend_kind=? where id=?", (nb, rid))
    if apply:
        con.commit()
    print(f"recipes: {len(rows)}   changes: {len(diff)}\n")
    for slug, old, new, why in diff:
        print(f"  {(old or 'None'):18s} -> {new:18s} {slug[:44]:44s} {why}")
    print(f"\n{'APPLIED' if apply else 'DRY-RUN'}")
    print("backend distribution (executable non-modifier):")
    for b, n in cur.execute("""select coalesce(backend_kind,'None'),count(*) from recipes
                               where executable=1 and recipe_kind!='modifier' group by backend_kind order by 2 desc"""):
        print(f"  {b:18s} {n}")
    con.close()

if __name__ == "__main__":
    main()
