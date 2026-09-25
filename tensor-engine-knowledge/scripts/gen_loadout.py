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
DB = os.path.join(ROOT, "engines.db")
OUTDIR = os.path.join(ROOT, ".claude", "loadout")
DATE_FALLBACK = "2026-06-02"

# curated single-token keywords per lane (single tokens = best match recall)
KW = {
    'llm-inference': ['llm', 'inference', 'llama', 'llamacpp', 'vllm', 'sglang', 'exllama', 'exllamav2', 'exllamav3',
                      'tensorrt', 'tensorrtllm', 'ollama', 'ktransformers', 'mlc', 'tgi', 'lmdeploy', 'aphrodite',
                      'gguf', 'serve', 'decode', 'throughput', 'latency', 'offload'],
    'llm-serving': ['serving', 'server', 'batching', 'router', 'routing', 'triton', 'ray', 'llamaswap', 'litellm',
                    'kserve', 'bentoml', 'openllm', 'tei', 'infinity', 'embedding', 'embeddings', 'rerank', 'reranker',
                    'openai', 'proxy', 'multimodel', 'hotswap'],
    'quantization': ['quant', 'quantization', 'quantize', 'gguf', 'gptq', 'awq', 'exl2', 'exl3', 'bitsandbytes', 'bnb',
                     'fp8', 'nvfp4', 'mxfp4', 'fp4', 'int4', 'int8', 'hqq', 'autoround', 'smoothquant', 'llmcompressor',
                     'imatrix', 'kquant', 'calibration'],
    'attention-kernels': ['attention', 'kernel', 'kernels', 'flashattention', 'flashattn', 'flashinfer', 'xformers',
                          'sageattention', 'sage', 'pagedattention', 'flexattention', 'triton', 'tritonwindows',
                          'marlin', 'machete', 'cudnn', 'gemm', 'prefill', 'decode'],
    'training': ['training', 'train', 'finetune', 'finetuning', 'lora', 'qlora', 'rlhf', 'dpo', 'fsdp', 'fsdp2',
                 'deepspeed', 'zero', 'megatron', 'unsloth', 'axolotl', 'llamafactory', 'torchtune', 'peft', 'trl',
                 'trainer', 'liger', 'nemo', 'checkpointing'],
    'diffusion-engines': ['diffusion', 'comfyui', 'comfy', 'diffusers', 'stablefast', 'tensorrt', 'xdit', 'nunchaku',
                          'svdquant', 'onediff', 'deepcache', 'fbcache', 'sageattention', 'compile', 'cache',
                          'accelerator', 'flux', 'sdxl', 'wan'],
    'runtime-foundations': ['runtime', 'pytorch', 'torch', 'torchcompile', 'inductor', 'jax', 'xla', 'onnx',
                            'onnxruntime', 'directml', 'tensorrt', 'mlx', 'metal', 'ggml', 'openvino', 'tvm', 'triton',
                            'cuda', 'cudnn', 'cublas', 'compiler', 'sm120', 'blackwell'],
    'structured-output': ['structured', 'output', 'constrained', 'decoding', 'grammar', 'gbnf', 'json', 'schema',
                          'tool', 'toolcall', 'function', 'outlines', 'xgrammar', 'guidance', 'instructor',
                          'jsonformer', 'regex', 'ebnf', 'pydantic', 'guided'],
    'speech-engines': ['speech', 'asr', 'tts', 'whisper', 'voice', 'transcribe', 'transcription', 'stt', 'piper',
                       'parakeet', 'sherpa', 'fasterwhisper', 'whisperx', 'kokoro', 'xtts', 'moonshine', 'voiceover',
                       'narration', 'audio'],
    'profiling-bench': ['profiling', 'profile', 'benchmark', 'bench', 'observability', 'monitor', 'nvitop', 'nsight',
                        'nvidiasmi', 'gpustat', 'dcgm', 'genaiperf', 'aiperf', 'pyspy', 'phoenix', 'langfuse',
                        'tracing', 'metrics', 'latency', 'vram', 'utilization', 'measure'],
}
PAT = {
    'llm-inference': ['local_llm', 'throughput', 'low_vram', 'windows', 'blackwell'],
    'llm-serving': ['production_serving', 'openai_api', 'multi_model', 'embeddings'],
    'quantization': ['vram_reduction', 'format_compat', 'fp4', 'calibration'],
    'attention-kernels': ['speedup', 'blackwell', 'long_context', 'diffusion'],
    'training': ['lora_training', 'qlora', 'single_gpu', 'multi_gpu'],
    'diffusion-engines': ['comfyui_accel', 'vram_reduction', 'compile', 'quant'],
    'runtime-foundations': ['cross_platform', 'windows', 'blackwell', 'compile'],
    'structured-output': ['tool_calling', 'json_schema', 'agent', 'constrained'],
    'speech-engines': ['asr', 'tts', 'voiceover', 'transcription'],
    'profiling-bench': ['benchmark', 'profiling', 'observability', 'measure'],
}

# generic tokens that leak from engine names but make poor routing keywords
STOP = {'engine', 'engines', 'the', 'and', 'with', 'for', 'llm', 'model', 'models', 'inference', 'runtime',
        'gpu', 'cuda', 'open', 'source', 'framework', 'library', 'lib', 'version', 'based', 'server', 'fast'}


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
                    "keywords": ["catalog", "engine", "engines", "tensor", "loadout"], "patterns": [], "priority": "core",
                    "summary": "Catalog index + fastest-install shortlist; drill into per-lane entries.",
                    "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    # one domain entry per catalog file
    for cat in cats:
        full = os.path.join(ROOT, "catalog", cat["slug"] + ".md")
        if not os.path.exists(full):
            continue
        neng = c.execute("SELECT COUNT(*) FROM engines WHERE category_id=?", (cat["id"],)).fetchone()[0]
        t, l = est(full)
        kw = list(KW.get(cat["slug"], []))
        for (nm,) in c.execute("SELECT name FROM engines WHERE category_id=? AND status='recommended' "
                               "ORDER BY download_priority LIMIT 4", (cat["id"],)):
            for w in re.split(r"[^a-z0-9]+", (nm or "").lower()):
                if len(w) > 2 and w not in kw and w not in STOP:
                    kw.append(w)
        summ = f"{cat['name']}: {neng} engines. {cat['description']}"[:120]
        entries.append({"id": cat["slug"], "path": f"catalog/{cat['slug']}.md", "keywords": kw,
                        "patterns": PAT.get(cat["slug"], []), "priority": "domain", "summary": summ,
                        "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})

    # wave docs — every wave's dispatch + verification (domain) and raw json (manual)
    import glob as _glob
    DISP_KW = ["install", "recommend", "recommended", "license", "blackwell", "windows", "shortlist",
               "plan", "best", "priority", "optimize", "configure", "config", "recipe", "tune", "build", "launch"]
    VER_KW = ["verify", "verification", "license", "correction", "source", "citation", "superseded", "deprecated", "trust"]
    for wdir in sorted(_glob.glob(os.path.join(ROOT, "waves", "wave-*"))):
        if not os.path.isdir(wdir):
            continue
        wname = os.path.basename(wdir)
        disp = os.path.join(wdir, "dispatch.md")
        if os.path.exists(disp):
            t, l = est(disp)
            entries.append({"id": f"{wname}-dispatch", "path": f"waves/{wname}/dispatch.md", "keywords": DISP_KW,
                            "patterns": ["install", "blackwell", "windows", "config"], "priority": "domain",
                            "summary": f"{wname} narrative: findings + install/config plan per lane."[:120],
                            "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l})
        ver = os.path.join(wdir, "verification.md")
        if os.path.exists(ver):
            t, l = est(ver)
            entries.append({"id": f"{wname}-verification", "path": f"waves/{wname}/verification.md", "keywords": VER_KW,
                            "patterns": ["verification"], "priority": "domain",
                            "summary": f"{wname} verifier receipt: verdicts, corrections, currency, next-wave candidates."[:120],
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
    avg = core + sum(domain_toks[:2])  # orientation + ~2 matched domain entries
    index = {"version": "1.0.0", "generated": date + "T00:00:00Z",
             "source": f"engines.db (wave {wave})", "lazyLoad": True,
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
