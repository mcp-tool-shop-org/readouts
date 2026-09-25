"""Wave-5 recipe-proving pass II — hands-on measured records. Idempotent on ids/wave_number."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()

# --- Wave 5 (hands-on, no swarm) ---
c.execute("DELETE FROM waves WHERE wave_number=5")
c.execute("""INSERT INTO waves (wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
VALUES (5,?,?,?,?,?,?,?,?)""", (
  "Recipe-proving II (hands-on) - native-Win llama.cpp->llama-swap serving, SageAttention 2.2.x, Unsloth LLM-LoRA on the RTX 5090",
  "2026-06-03",
  "llm-serving, attention-kernels/diffusion, training",
  0,
  "HANDS-ON MEASURED on the live RTX 5090 (llama-bench pp/tg, llama-swap OpenAI-proxy timings, nvidia-smi telemetry) - direct measurement IS the verifier. The one researched claim (the official prebuilt CUDA-12 llama.cpp ships working sm_120 MMQ) was empirically confirmed: pp512=7251 t/s = 7.3x the cuBLAS-fallback level.",
  "synthesized",
  "(hands-on session, no dispatch swarm)",
  "Continues the recipe-proving pass begun under wave 4 (#147-151)."
))
wave5 = c.execute("SELECT id FROM waves WHERE wave_number=5").fetchone()[0]
print("wave5 id =", wave5)

# --- #152 baseline (cat 2 serving, engine 15 llama-swap) ---
body152 = (
"llama.cpp -> llama-swap NATIVE-WINDOWS SERVING BASELINE (MEASURED hands-on 2026-06-03; RTX 5090 / sm_120 / 32 GB / driver 610.47). "
"Closes the wave-4 #149 gap (llama-swap was BLOCKED on a missing llama.cpp binary).\n\n"
"ENGINE: llama.cpp build b9484 (63e66fdd2), OFFICIAL PREBUILT 'Windows x64 (CUDA 12)' zip "
"(llama-b9484-bin-win-cuda-12.4-x64.zip) + matching cudart-llama-bin-win-cuda-12.4-x64.zip, extracted to E:\\AI-Models\\llama.cpp. "
"NO compile / NO CUDA toolkit / NO cmake -- the prebuilt + cudart pack are self-contained (cudart64_12 / cublas64_12 / ggml-cuda.dll 538MB). "
"This is recipe #43's no-compile path, now PROVEN Blackwell-correct by measurement. Chosen over a source build because the rig has NO CUDA "
"toolkit installed and VS 18 (2026) (recipe #8 warns 'VS 2026 too new for some CUDA installers').\n\n"
"MMQ CONFIRMED ENGAGED (decisive check): llama-bench Qwen3-30B-A3B-Q4_K_M (qwen3moe, Apache-2.0) -ngl 99 -fa 1 -> pp512=7251 t/s, tg128=334 t/s. "
"pp512 is 7.3x the cuBLAS-fallback level (KB ref #42 cuBLAS pp=989) and ABOVE the KB's MMQ range (5611-6566) => the prebuilt CUDA-12.4 build runs the "
"sm_120 MMQ integer kernels, not a cuBLAS fallback (a fallback would give pp~990). Qwen3-4B-Q4_K_M (qwen3 dense): pp512=19383, tg128=342. llama32-3b-Q8 sanity tg128=327. "
"NOTE: native llama.cpp MMQ decode 334 t/s for a 30B-A3B MoE is ~2.4x Ollama's 138 t/s (wave-4) for the same MoE class -- native llama.cpp markedly faster than Ollama at single-stream MoE decode.\n\n"
"SERVING (llama-swap v222 native-Win portable, E:\\AI-Models\\llama-swap, listen 127.0.0.1:9090; config E:\\AI-Models\\llama-swap\\config.yaml, 3 name-routed models, per-model ttl). "
"Measured via the OpenAI /v1/chat/completions proxy:\n"
"- warm decode (resident): qwen3-4b 286 tok/s, qwen3-30b-a3b 257 tok/s (full path proxy->llama-server->OpenAI API; slightly under raw llama-bench tg due to prompt-eval + HTTP).\n"
"- SWAP latency (auto unload current + load next + ready), steady-state warm-kernel: load 4b from idle 2.4s; swap 4b->30b (18.5GB) 9.8-11.6s (NVMe-read bound, page cache helps repeat); swap 30b->4b (2.5GB) 4.1s. First-ever load 12.8s (one-time CUDA-ctx + 538MB ggml-cuda.dll init).\n"
"- VRAM: desktop floor 2811 MiB; qwen3-4b resident 6995 (~4.2GB); qwen3-30b-a3b resident 21813 (~19GB); after POST /api/models/unload -> 2832 MiB = FULL reclaim to floor. /running confirms exactly ONE model resident across swaps (single 32GB card = one-at-a-time; ttl idle-unload frees VRAM).\n"
"- peak telemetry during 30b llama-bench: 374 W, 37 C, 92% util, 21278 MiB (short bench, not a sustained soak). Raw: baselines/llamacpp-30b-dmon.log."
)
c.execute("DELETE FROM config_recipes WHERE id IN (152,153)")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (152,?,?,?,?,?,?,?,?)""", (
  "llm-serving-llamacpp-b9484-prebuilt-cuda12-to-llamaswap-baseline-5090",
  "llama.cpp b9484 prebuilt CUDA-12.4 -> llama-swap: native-Win serving baseline (MEASURED, MMQ confirmed)",
  2, 15, "baseline",
  "https://github.com/ggml-org/llama.cpp/releases/tag/b9484",
  body152, wave5))

# --- #153 recipe (cat 2 serving, engine 15 llama-swap) ---
body153 = (
"PROVEN end-to-end (2026-06-03): native-Windows name-routed multi-model LLM serving on the 5090 WITHOUT WSL2 and WITHOUT compiling. For this rig this supersedes the 'build from source' framing.\n\n"
"STEP 1 - Blackwell-correct llama.cpp WITHOUT a toolkit (recipe #43 path, proven):\n"
"  gh release download b9484 --repo ggml-org/llama.cpp --pattern 'llama-b9484-bin-win-cuda-12.4-x64.zip' --pattern 'cudart-llama-bin-win-cuda-12.4-x64.zip'\n"
"  Expand BOTH zips into the SAME folder. PICK THE CUDA-12 BUILD for Blackwell, NEVER CUDA-13 (13.x crashes sm_120 MMQ -> ~5x slower cuBLAS). "
"VERIFY MMQ: llama-bench -m <MoE-Q4_K_M.gguf> -ngl 99 -fa 1  => expect pp512 in the THOUSANDS (a 30B-A3B gave 7251). If pp~1000 it fell back to cuBLAS -> only THEN source-build with CUDA 12.8 (recipe #42/#66).\n\n"
"STEP 2 - GGUF GOTCHA (earned, high-value): the Ollama blob store (E:\\AI-Models\\Ollama\\blobs) is NOT a drop-in GGUF source for stock llama.cpp/llama-swap. The newest archs FAIL in stock b9484: qwen3.6 (arch qwen35 / qwen35moe) AND gemma4 all error 'key <arch>.rope.dimension_sections has wrong array length; expected 4, got 3' -- Ollama runs its OWN engine and its GGUF conversion diverges from upstream for cutting-edge models. Fix: pull CLEAN GGUFs from HuggingFace (Qwen/Qwen3-30B-A3B-GGUF, Qwen/Qwen3-4B-GGUF; arch qwen3moe/qwen3 load fine). Commercial-safe: Qwen3 = Apache-2.0.\n\n"
"STEP 3 - llama-swap (recipe #7 pattern): winget install llama-swap OR portable zip (gh release download v222 --repo mostlygeek/llama-swap --pattern '*windows_amd64.zip'). "
"config.yaml: healthCheckTimeout 500; startPort 10001; macros for the llama-server.exe path + gpu-flags '-ngl 99 -fa 1 --cache-type-k q8_0 --cache-type-v q8_0'; per model a cmd block: <llama-server> -m <path> --port ${PORT} <gpu-flags> -c 16384, plus ttl 120-300s for idle VRAM reclaim. "
"Run: llama-swap.exe -config config.yaml -listen 127.0.0.1:9090. Any OpenAI client hitting /v1/chat/completions with model=<name> triggers auto load/swap. Endpoints: /v1/models, /running, POST /api/models/unload[/:id], /ui, /metrics. "
"VALIDATED: 286/257 tok/s warm (4b/30b), swap 2.4-11.6s by model size, full VRAM reclaim to floor, single-model residency confirmed. Config lives at E:\\AI-Models\\llama-swap\\config.yaml."
)
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (153,?,?,?,?,?,?,?,?)""", (
  "llm-serving-llamacpp-prebuilt-cuda12-fastpath-to-llamaswap-proven",
  "llama.cpp prebuilt CUDA-12 fast-path -> llama-swap (PROVEN, native-Win) + Ollama-blob-wont-load gotcha",
  2, 15, "recipe",
  "https://github.com/mostlygeek/llama-swap",
  body153, wave5))

# --- update #149: flip llama-swap from BLOCKED to DONE ---
row = c.execute("SELECT body FROM config_recipes WHERE id=149").fetchone()
if row:
    b = row[0]
    marker = "\n\n[UPDATE 2026-06-03 wave-5]: llama-swap is now STOOD UP + VALIDATED (#152 baseline, #153 recipe). The blocker is resolved: NOT by a source build but by the official PREBUILT 'Windows x64 (CUDA 12)' llama.cpp b9484 (MMQ confirmed live, pp512=7251 on a 30B-A3B). llama-swap v222 serves 3 name-routed GGUFs from E:\\AI-Models\\llama-swap\\config.yaml with TTL VRAM reclaim. Caveat earned: Ollama's own blobs do NOT load in stock llama.cpp for the newest archs (qwen3.6/gemma4 rope.dimension_sections mismatch) -- llama-swap uses clean HF GGUFs."
    if "[UPDATE 2026-06-03 wave-5]" not in b:
        c.execute("UPDATE config_recipes SET body=? WHERE id=149", (b + marker,))
        print("updated #149")

db.commit()
print("recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE id IN (149,152,153) ORDER BY id"):
    print(" ", r[0], r[1], "|", r[2][:70])
db.close()
