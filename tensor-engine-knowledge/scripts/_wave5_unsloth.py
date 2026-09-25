"""Wave-5 #155 — Unsloth LLM-QLoRA baseline, measured native-Win. Idempotent on id 155."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()
wave5 = c.execute("SELECT id FROM waves WHERE wave_number=5").fetchone()[0]

body = (
"Unsloth LLM-QLoRA STOOD UP + VALIDATED end-to-end, NATIVE WINDOWS (no WSL2), RTX 5090 sm_120, 2026-06-03. "
"Completes the studio training PAIR: kohya = visual SDXL LoRA (#150/#151); Unsloth = LLM QLoRA (this). Both native-Win; commercial-safe bases (a LoRA inherits the base license).\n\n"
"ENV (fresh uv venv E:\\AI\\training\\unsloth-env, py3.11): the proven sm_120 stack -- torch 2.12.0+cu130, torchvision 0.27.0+cu130, bitsandbytes 0.49.2 (4-bit NF4 verified on sm_120), triton-windows 3.7.0.post26, unsloth 2026.5.10, unsloth_zoo 2026.5.5, transformers 5.5.0, trl 0.24.0, peft 0.19.1, accelerate 1.13.0.\n\n"
"INSTALL GOTCHAS (high-value, earned):\n"
"  1) `pip install unsloth unsloth_zoo` TRANSITIVELY pulls xformers 0.0.35, which SILENTLY DOWNGRADES torch to 2.10.0+CPU (a CPU build -> no CUDA). This is the KB's 'NEVER pip xformers on Blackwell' trap, sprung via unsloth's dep tree. FIX: `pip uninstall -y xformers` then reinstall `torch==2.12.0 --index-url https://download.pytorch.org/whl/cu130`. Unsloth does NOT need xformers on Blackwell.\n"
"  2) After restoring torch 2.12, unsloth's import-time check fails: 'torch==2.12.0+cu130 requires torchvision>=0.27.0' (xformers had pulled 0.25.0). FIX: `pip install torchvision==0.27.0 --index-url .../cu130` (MUST be the cu130 wheel, not the CPU default, or torch mismatches again).\n"
"  3) Unsloth warns 'Flash Attention 2 installation seems broken. Using Xformers instead' -- but with NEITHER FA2 nor xformers installed it falls back to torch SDPA (cuDNN on Blackwell) and trains fine. Consistent with the no-FA3-on-sm120 / cuDNN-SDPA rule. Ignore the warning.\n"
"  => install order that AVOIDS the churn: torch(cu130)+torchvision(cu130) FIRST, then bitsandbytes==0.49.2 triton-windows numpy, then `unsloth unsloth_zoo`, then uninstall xformers + (re)assert torch/torchvision cu130.\n\n"
"MEASURED (unsloth/Qwen3-4B-bnb-4bit; Qwen3 = Apache-2.0; QLoRA r=16 lora_alpha=16 on all 7 linear modules q/k/v/o/gate/up/down, max_seq_len=2048, per_device_bs=2 x grad_accum=4, optim=paged_adamw_8bit, bf16, use_gradient_checkpointing='unsloth'):\n"
"  - throughput ~2.28 s / optimizer-step (0.438 steps/s, 3.506 samples/s) for the 4B; cold model load ~ a few s after the one-time ~2.5GB 4-bit download.\n"
"  - PEAK VRAM ~6.1 GB total process (nvidia-smi 6271 MiB; torch-alloc 3.19 GB) -- matches recipe #75's QLoRA budget (4-8B ~5-6 GB) => a 4B leaves ~26 GB for longer context / bigger ranks; per the budget a 14B fits ~8.5 GB and a 32B ~26 GB just fits.\n"
"  - LEARNS: train loss 7.01 -> 2.90 monotonic over 15 steps. Full pipeline proven: load 4-bit base -> attach LoRA -> train -> save 143.6 MB adapter (reloadable). 169 W / 37 C (tiny-scale, not power-bound; real runs push higher).\n"
"Repo/venv E:\\AI\\training\\unsloth-env; smoke script E:\\AI\\training\\unsloth_qlora_smoke.py; result E:\\AI\\training\\unsloth_qlora_result.json; telem baselines/unsloth-dmon.log. "
"This is the native-Win answer to recipe #75 (which proposed a cu128 base); on torch 2.12 the base is cu130, and the xformers/torchvision churn above is the real install path."
)
c.execute("DELETE FROM config_recipes WHERE id=155")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (155,?,?,?,?,?,?,?,?)""", (
  "training-unsloth-llm-qlora-baseline-native-win-5090-qwen3-4b",
  "Unsloth LLM-QLoRA baseline (MEASURED native-Win 5090): Qwen3-4B-bnb-4bit, ~6GB VRAM, + the xformers/torchvision install gotchas",
  5, 45, "baseline",
  "https://unsloth.ai/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth",
  body, wave5))
db.commit()
print("inserted #155; recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE wave_id=? ORDER BY id",(wave5,)):
    print(" ", r[0], r[1], "|", r[2][:64])
db.close()
