# Wave 1 — Foundation: best tensor / inference / training engines for a single RTX 5090 (Blackwell, Windows 11)

**Study-swarm wave 1** · dispatched 2026-06-02 · 7 lanes · 14 agents (one web-grounded researcher + one reasoning-stripped retrieval-verifier per lane) · **77 engines, 235 sources, 41 config-recipes, 21 wave-2 candidates**. Run `wf_e9dc4dd4-db1`.

## Context

- **Rig:** HP OMEN 45L · RTX 5090 · Blackwell **sm_120** · **32 GB VRAM** · Core Ultra 9 · **64 GB system RAM** · Windows 11. The only machine — no Mac, no second box. Apple-Silicon/MLX is catalogued as cross-platform *reference*, not a rig to fit.
- **Use:** a local-first, single-human + LLM-crew game studio. Local inference, local-LLM delegation, local diffusion/ComfyUI, and LoRA/style fine-tuning are the real workloads — *not* datacenter-scale multi-node serving. Every engine is scored `rig_fit` (this exact rig) + `studio_fit` (single-workstation usefulness vs datacenter-only).
- **Method:** one web-grounded research agent per lane; each output handed to a **reasoning-stripped adversarial verifier** (different model tier) that used live web retrieval as an existence/license/spec/currency oracle *before* the data was trusted. Full receipt → [verification.md](verification.md).
- **Currency:** everything confirmed live on 2026-06-02. The assistant's training cutoff predates the current versions (PyTorch 2.12, vLLM 0.22, llama.cpp b9484, ExLlamaV3, SageAttention 3, CUDA 13.3) — none of that is from memory.

## The finding that reorganizes the whole catalog: the decisive axis is native-Windows Blackwell survivability, not throughput

For a single-human studio on one Windows 5090, **the question is not "which engine is fastest" — it's "which engine runs natively, today, on sm_120/Windows without a WSL2 + nightly-wheel maintenance tax."** The field splits cleanly and counter-intuitively:

- **Native-Windows, Blackwell-ready, install-and-go** (the studio core): **llama.cpp / Ollama / LM Studio / ExLlamaV3** (inference), **llama-swap** (serving/routing), **GGUF + EXL3** (quant), **cuDNN-SDPA + SageAttention + triton-windows + FlexAttention** (kernels), **TRL + PEFT + Liger + kohya_ss** (training, native), **ComfyUI + Nunchaku + ComfyUI-GGUF** (diffusion), **PyTorch (cu130) + ggml + TensorRT-RTX** (foundations).
- **Linux-first → WSL2-only on this box** (the throughput kings — use only when you genuinely need fleet-scale batching): **vLLM, SGLang, TensorRT-LLM, LMDeploy, Aphrodite** (inference/serving), **TEI** (embeddings), **Unsloth, Axolotl, LLaMA-Factory** (smoothest in WSL2), **llm-compressor** (FP8/NVFP4 producer). WSL2 2.7.0 + recent driver finally makes vLLM CUDA-graph capture work on sm_120 (~140 tok/s Qwen3-14B-AWQ vs ~17 eager), so it's *usable* — but it's still a Linux VM, not native.
- **Avoid / dead / wrong-silicon on this rig:** **NVIDIA Triton Server** (Windows DEPRECATED at 2.51.0), **HF TGI** (repo archived Mar 2026, relicensed HFOIL at v1.0 — do not build on it), **TorchServe** (archived read-only Aug 2025), **torchtune** (deprecated, final v0.6.1), **stable-fast / OneDiff / DeepCache** (superseded — use Comfy-WaveSpeed/Nunchaku/FBCache), **DeepSpeed / Megatron / NeMo** (datacenter, painful on Windows), **JAX/XLA** (WSL2-only on Windows), **OpenVINO** (Intel-silicon-first), **TVM/MLX** (reference only).

The trap mirrors the model KB's "the most-tutorialed model is the non-commercial one": here, **the most-recommended-in-benchmarks engines (vLLM, TensorRT-LLM, FlashAttention-3/4, Triton Server) are exactly the ones that are Linux-only or physically can't run on the 5090.** They're right for a datacenter; they're the wrong default for this workstation.

## Blackwell rules for THIS rig (the load-bearing, cross-lane gotchas)

These recur across the inference, quant, kernels, diffusion, and foundations lanes — get them wrong and you lose 5× or silently break your install:

1. **CUDA-toolkit version is the #1 footgun, and the right answer differs by layer.** For **llama.cpp**: build/run with the **CUDA 12.8** toolchain (`-DGGML_CUDA_ARCHITECTURES=120`) — CUDA 13.x MMQ kernels segfault on sm_120 and throw "invalid resource handle"; 12.8 + MMQ is ~5× faster than the wrong toolkit. For **PyTorch**: the matrix moved on — **2.12 DROPPED `cu128`; use `cu130` (CUDA 13)**, `cu126` only for old drivers. The years-old `pip install torch --index-url .../cu128` command now **installs nothing**.
2. **sm_120 (desktop Blackwell / GB202) ≠ datacenter Blackwell (sm_100 B200 / sm_103 B300).** The 5090 physically lacks the TMEM tensor-memory subsystem the warp-specialized **FlashAttention-3 and FlashAttention-4 are built on — they cannot run on it, no software patch fixes it.** Fall back to **FA2-class + cuDNN-SDPA** (the *fastest* attention on this card, ~97% speed-of-light, free in PyTorch) **+ SageAttention** (the diffusion win).
3. **NEVER `pip install xformers`** into a Blackwell venv / ComfyUI's embedded Python. It has no sm_120 wheel *and* silently force-downgrades your cu128/cu130 torch to an older CPU/CUDA build — the single biggest hidden trap on Windows Blackwell. The sanctioned stack is **PyTorch cu130 + triton-windows + SageAttention + torch.compile + SDPA**.
4. **64 GB system RAM is a real capability axis, not just headroom.** It turns "a bit over 32 GB VRAM" into "runs": **KTransformers** (hot experts on GPU, cold experts in RAM → 100B+ MoE at ~20 tok/s on one card), **llama.cpp `--n-cpu-moe` / `-ngl` partial offload** (spill a 40–50 GB GGUF), and **paged optimizers** in training (push 30–70B QLoRA optimizer state to RAM).

## The install plan (set up in this order)

### Tier 0 — foundations
**PyTorch** (cu130 build) + the **CUDA 13.x toolkit / cuDNN / cuBLAS** substrate; **ggml/llama.cpp** prebuilt Windows CUDA binaries (the offload king, ships every few days); **triton-windows** (now official at `triton-lang/triton-windows`, sm_120 first-class — the enabling layer for SageAttention/FlexAttention without WSL2). Optionally **TensorRT-RTX** (the *consumer* TensorRT — `pip install tensorrt-rtx`, JIT engine build, no fragile per-GPU AOT step) for the last 1.5–2× on a frozen ONNX/diffusion model.

### Tier 1 — the studio stack (native Windows unless noted)

| Job | Install | Why |
|---|---|---|
| Everyday local LLM | **Ollama** (or **LM Studio**) | Native Windows installer, day-1 5090 support, zero CUDA fiddling, OpenAI-compatible server for crew/`ollama-intern` delegation. The "it just works" baseline. |
| Heavy / oversized LLM | **llama.cpp** direct | `-ngl` + `--n-cpu-moe` spills a 40–50 GB GGUF across 32 GB VRAM + 64 GB RAM. Build CUDA 12.8 / sm_120. |
| Max quality-per-VRAM | **ExLlamaV3** (EXL3) | QTIP-coded ~3.5–4 bpw = best perplexity-per-byte on one 5090; ships Windows cu128 wheels. (ExLlamaV2 is **archived** — use V3.) |
| Giant MoE wildcard | **KTransformers** | Apache-2.0, native Windows, CPU/GPU heterogeneous MoE — the engine that monetizes the 64 GB RAM. |
| Multi-model front door | **llama-swap** over **llama-server** | The one native-Windows router that solves "one OpenAI endpoint, many models, load-on-demand, unload-on-idle" on 32 GB. Add **LiteLLM** only to blend local + hosted (Claude/OpenAI) behind one key. |
| Quant (produce + run) | **GGUF** via `llama-quantize` (Q4_K_M daily; IQ4_XS+imatrix for tight VRAM; Q5/Q6 when it fits) + **EXL3** | The two native-Windows first-class formats. **FP4 (NVFP4) = watch, not production** — llama.cpp's NVFP4 accel dispatch (PR #22196) was still open; consumer FP4 is WSL2/community-patched today. |
| Attention/kernels | **cuDNN-SDPA** (free, fastest) + **SageAttention** (2++/3) + **FlexAttention** (custom masks) | Skip xformers/FlashInfer/Marlin (Linux-first or server-side, wrapped automatically by the engine). |
| LLM fine-tune | **Unsloth** (in WSL2) + **TRL + PEFT + Liger-Kernel** (native Windows, for DPO/GRPO) | bitsandbytes now ships official Windows sm_120 wheels → native QLoRA works, but Unsloth's smooth path is still WSL2. |
| **Style / character LoRA** | **kohya_ss / sd-scripts** | THE studio's real training payload (SDXL trivial, Flux comfortable at FP8). Ties directly to style-dataset-lab. |
| Diffusion runtime | **ComfyUI** (portable) + **Nunchaku** (NVFP4 FLUX/Qwen, ~3× + ~3.6× VRAM cut) + **ComfyUI-GGUF** (offload big Wan/Flux video) + **SageAttention** + **Comfy-WaveSpeed** (FBCache) | The model KB's `comfy.md` catalogs the *models*; this is the accelerator layer beneath them. |

## Per-lane grounding (findings → recommendations)

- **LLM inference.** Decisive axis = native-Windows Blackwell, not tokens/sec. Install **Ollama/LM Studio** (daily) + **llama.cpp** (offload) + **ExLlamaV3** (quality-per-VRAM); **KTransformers** for giant MoE. Native-Windows vLLM still doesn't exist; ExLlamaV2 is archived; TGI is dead. [catalog/llm-inference.md](../../catalog/llm-inference.md)
- **Serving.** The old "use Triton/Ray for serious serving" is wrong on a Windows workstation. The native winner is **llama-swap over llama-server**, with **WSL2 vLLM/SGLang** as the batching escalation and **TEI** (Docker/WSL2) as the embed/rerank sidecar. Triton deprecated Windows; TorchServe is archived. [catalog/llm-serving.md](../../catalog/llm-serving.md)
- **Quantization.** A producer→format→consumer split. Native-Windows first-class: **GGUF** (`llama-quantize`) and **EXL3** (ExLlamaV3). NVFP4/MXFP4 are the headline reason to own a 5090 but the consumer-Windows path is still immature (kernels merged, Blackwell accel dispatch open) — **treat FP4 as experimental, Q4_K_M/EXL3 win today.** [catalog/quantization.md](../../catalog/quantization.md)
- **Attention & kernels.** The 5090 is sm_120 (no TMEM) → **FA3/FA4 can't run**; the practical speed king is **cuDNN-SDPA** (free in PyTorch), the diffusion win is **SageAttention** (2++ now, 3 for FP4), the flexible tool is **FlexAttention**. Enabling layer: **triton-windows**. Never install xformers. [catalog/attention-kernels.md](../../catalog/attention-kernels.md)
- **Training.** bitsandbytes now ships official Windows sm_120 wheels (native QLoRA lives). Use **Unsloth** (WSL2) for fast LLM LoRA + **TRL/PEFT/Liger** (native) for flexible/RLHF + **kohya_ss** for the diffusion style-LoRA that is the studio's real payload. DeepSpeed/Megatron/NeMo are datacenter; torchtune is deprecated. [catalog/training.md](../../catalog/training.md)
- **Diffusion engines.** ComfyUI portable pins its own Blackwell torch (this is *why* the rig rule says don't hand-install nightly). **Nunchaku** (NVFP4) is the single-GPU win; **ComfyUI-GGUF** spills big video to RAM; **SageAttention + Comfy-WaveSpeed** stack on top. stable-fast retired → Comfy-WaveSpeed; OneDiff's best quant is paywalled. [catalog/diffusion-engines.md](../../catalog/diffusion-engines.md)
- **Runtime foundations.** "Stable Blackwell on Windows" is now boring/solved at the PyTorch layer (2.7→2.12) — but **use cu130, not cu128** (dropped). **ggml/llama.cpp** is the offload workhorse; **TensorRT-RTX** (consumer, native pip) is the latency play (TRT-LLM is WSL2-only on GeForce). JAX/TVM/OpenVINO/MLX are reference-only here. [catalog/runtime-foundations.md](../../catalog/runtime-foundations.md)

## Method, confidence, and what's deferred

- **Verification:** 77/77 engines resolved to real pages; 76 confirmed (1 `unverified` — MLC-LLM, whose claimed version couldn't be confirmed live). The verifier's value-add was **version currency and license/Blackwell-status precision** — it caught vLLM/SGLang/LMDeploy Blackwell status *inverted to false* (they DO work), Ollama's version off by ~24 releases, FA3/FA4 ruled out on sm_120, and several "blackwell_ready:true" claims that lacked repo evidence. Details in [verification.md](verification.md).
- **Caveats (re-verify before relying commercially):** "blackwell_ready" is nuanced — many engines *run* on sm_120 via CUDA 12.8 but ship no sm_120-specific kernels (so you get correctness, not peak speed). Open the repo's own install matrix before committing. FP4 quality-vs-Q4_K_M has no settled independent benchmark yet.
- **21 verifier-proposed additions → wave 2** (e.g. mistral.rs, TabbyAPI, NVIDIA ModelOpt, torchao, ThunderKittens 2.0, NATTEN, veRL, OpenRLHF, torchtitan, stable-diffusion.cpp, InvokeAI, AMD ROCm). Listed in [verification.md](verification.md). A focused "WSL2 throughput-serving + FP4 producers + RL post-training" wave would close most.

## Standards compliance (the six workflow standards)

Scored 0–3 per `.claude/rules/workflow-standards.md`:

- **PIN_PER_STEP — 3.** The wave is a saved Workflow script (`scripts/wave-swarm.workflow.js`) pinning model per step (research=Opus inherited, verify=Sonnet), prompt per lane, and `RESEARCH_SCHEMA`/`VERIFY_SCHEMA` tool-schemas; byte-replayable via `resumeFromRunId`.
- **ANDON_AUTHORITY — 2.** The verifier's `unverified`/`refuted` default and `verified` flag tag every row; the catalog surfaces it (`✓` column) so defects don't silently propagate. (Flag-and-surface, not hard-halt — acceptable for a read-only research wave.)
- **NAMED_COMPENSATORS — 3.** This wave makes **no irreversible external calls** — all writes are local, git-tracked files. The named undo is `load_db.py <wave-json>` (idempotent — re-running *replaces* that wave's rows) + `git checkout`. No `npm publish` / `gh release` / external write occurred.
- **DECOMPOSE_BY_SECRETS — 2.** Lanes decompose by engine category, which groups what version-churns together (inference/serving move fast; foundations are stable) so a re-dispatch touches one volatility class at a time.
- **UNCERTAINTY_GATED_HUMANS — 2.** `verified=0` / `confirmed-with-fixes` / `currency=superseded` are the uncertainty signals flagged for human review ("treat verified=0 as a lead, not gospel"); lane notes use contrastive framing throughout ("old advice said X; now Y because…").
- **EXTERNAL_VERIFIER — 2.** A separate, reasoning-stripped verifier per lane (different *tier*: Sonnet vs Opus) with the researcher's reasoning hidden and live web retrieval as the decorrelating oracle. **Family-different** verification (route through `prism verify` / `roleos verify-citations`, ideally a local non-Claude model on this rig) is the documented P1 upgrade for a later wave — matching the model-knowledge KB's stance.

## Querying this wave

```powershell
# the install shortlist
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'tensor-engine-knowledge/engines.db').execute('SELECT category,dl,name,license,bw,rig,studio FROM v_recommended')]"
# everything Blackwell/Windows-ready that loads GGUF
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'tensor-engine-knowledge/engines.db').execute(\"SELECT name,category_id FROM engines WHERE blackwell_ready=1 AND model_formats LIKE '%gguf%'\")]"
```
