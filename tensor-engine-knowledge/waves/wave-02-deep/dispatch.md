# Wave 2 — Deep: close the verifier queue + version-pinned config recipes

**Study-swarm wave 2** · dispatched 2026-06-02 · 7 lanes · 14 agents (one researcher + one reasoning-stripped retrieval-verifier per lane) · **+18 new engines (after dedup), +56 config-recipes**. Run `wf_2a301300-342`. Builds on [wave 1](../wave-01-foundation/dispatch.md) — read that first for the cross-cutting Blackwell frame; this wave deepens it.

## What wave 2 did

Two jobs: **(A)** close the 21-engine queue the wave-1 verifier flagged (each researcher got the per-lane "already covered" list so it *appends* instead of duplicating), and **(B)** — the headline — produce **version-pinned, copy-pasteable config recipes** per lane. The KB went from "which engine" to "exactly how to build, launch, and tune it on this rig." Recipes live in the `config_recipes` table and render under **"Config recipes, tools & resources"** in each lane catalog.

After ingest, a dedup pass removed 9 rows (8 engines re-listed in a second lane + 1 stray "lane note" loaded as an engine) — see [verification.md](verification.md). Net KB: **95 engines · 94 verified · 33 recommended · 97 config-recipes · 2 waves.**

## The headline finding: one lever dominates every lane — pin CUDA 12.8 / cu128

Wave 1 named the gotcha; wave 2 *benchmarked* it across lanes and it is the single highest-leverage knob in the whole KB:

- **llama.cpp** on a 5090: CUDA **12.8 + MMQ** = **5611 pp / 211 tg tok/s**; the *same code* on CUDA 13.1 = **772 / 121** (5.7× slower prefill) because the Blackwell MMQ kernel segfaults under 13.x and silently falls back to cuBLAS. Build with `-DCMAKE_CUDA_ARCHITECTURES=120`, keep `GGML_CUDA_FORCE_CUBLAS=OFF`, and `rm -rf build` when fixing a bad config (CMake caches the slow path).
- **vLLM / serving**: never run **eager mode** — Qwen3-14B-AWQ measured **~17 tok/s `--enforce-eager` vs ~140 with CUDA graphs (8×)**. CUDA graphs / FlashInfer are not optional on Blackwell.
- **The torch ecosystem** (PyTorch, vLLM, Unsloth, ComfyUI, TRL): stable wheels still compile only to sm_90 (pytorch#164342 open) → install the **cu128/cu130 nightly** index, NGC container, or build with `TORCH_CUDA_ARCH_LIST=12.0`, and install torch **last** so a stray `requirements.txt` can't drag in a cu126/sm_90 wheel that silently CPU-falls-back.
- **The one nuance:** llama.cpp wants the **CUDA 12.8 *toolkit*** (13.x breaks MMQ), but **diffusion NVFP4 wants the cu130 *nightly torch*** (cu128 runs but lacks the NVFP4 kernels). Right pin differs by layer — the recipes spell out which per engine.

> Quantize the KV cache (`-fa --cache-type-k q8_0` / `OLLAMA_KV_CACHE_TYPE=q8_0` / TabbyAPI Q6–Q8), keep CUDA graphs on, pin sm_120 at build time — that trio is what turns 32 GB into a 32B-class serving box.

## New engines by lane (the queue, closed)

- **llm-inference (+1 kept):** **mistral.rs** — the standout: Rust-native, **Windows-native, single-binary**, Blackwell-ready, with **ISQ** (quantize any HF model in-situ at load → run a new model the day it ships, no GGUF wait), FP8 KV-cache, PagedAttention. Slots between Ollama (easiest) and vLLM (fastest). *(Triton → demoted to llm-serving/situational; MLX → reference; both deduped here.)*
- **llm-serving (+3):** **TabbyAPI** (the OpenAI server for EXL3 — single-GPU INT4 throughput king on consumer NVIDIA, native Windows), **llama-server Router Mode** (`--models-dir` + LRU eviction built into llama.cpp → makes the external llama-swap optional), **GPUStack** (cluster orchestration — but v2 dropped native-Windows workers → WSL2 only).
- **quantization (+2):** **NVIDIA ModelOpt** (the production NVFP4/FP8 PTQ that emits unified HF checkpoints vLLM/TRT-LLM consume) + **torchao** (the PyTorch-native mechanism under INT4/FP8/NVFP4 in vLLM/SGLang/Diffusers). Together they complete the **PRODUCER→FORMAT→CONSUMER spine** for FP4 on consumer Blackwell.
- **attention-kernels (+3):** **ThunderKittens 2.0** (CUDA DSL that explicitly targets sm_120 — but for kernel authors, not a drop-in runtime), **NATTEN** (sparse/neighborhood attention — but its fast kernels are Hopper+datacenter-Blackwell only; on a 5090 it falls back), **trtllm-gen FMHA** (cautionary: shipped no sm_120 cubins → emitted **garbage tokens silently** on a 5090 via wrong-arch fallback).
- **training (+3):** the **RL post-training layer** wave 1 lacked — **veRL** (the 2026 de-facto standard: PPO/GRPO/GSPO/DAPO, FSDP+Megatron × vLLM/SGLang rollout), **OpenRLHF** (Ray+vLLM+DeepSpeed, 70B+), **torchtitan** (Meta's PyTorch-native 4D-parallel pre-training, successor to deprecated torchtune).
- **diffusion-engines (+3):** **stable-diffusion.cpp** (the llama.cpp of diffusion — `--offload-to-cpu` streams FLUX.2-dev Q8 weights from the **64 GB RAM**, no Torch), **torchao** (the NVFP4/MXFP8 on-ramp for Diffusers/ComfyUI), **InvokeAI** (Apache-2.0 — the license-clean escape from ComfyUI's GPL for commercial work).
- **runtime-foundations (+3):** **KTransformers** (formally — runs a **671B-class MoE on ONE 5090 + 64 GB RAM** at 20+ tok/s via hot-expert-on-GPU/cold-in-RAM; SOSP'25), **MLC-LLM** (TVM-based, the only engine that compiles one model to CUDA *and* WebGPU/Vulkan/Metal → the WebLLM path), **tinygrad** (reference compiler). **AMD ROCm** catalogued as the non-NVIDIA substrate (reference — no AMD GPU here).

## Cross-lane refinements that update wave-1 advice

- **The FP4 produce→serve loop now closes locally:** this rig can PRODUCE its own NVFP4 weights (ModelOpt or llm-compressor/torchao) and SERVE them at FP4 speed (vLLM natively on Windows for AWQ/GPTQ; TRT-LLM in WSL2 for peak NVFP4 — but TRT-LLM **deprecated native Windows at v0.18.0**, and GeForce NVFP4 GEMM only unlocked at 0.20.0rc3).
- **sm_120 ≠ datacenter Blackwell (sm_100), reaffirmed harder:** NATTEN's fast FNA/FMHA and trtllm-gen cubins are sm_90/sm_100 only; "Blackwell support" in a README is **not** automatically 5090 support — verify sm_120 specifically.
- **WSL2 FP8 is SLOWER than INT4 on this rig:** under WSL2, dxgkrnl doesn't expose Blackwell FP8/FP4 tensor cores, so FP8 quant runs **~3× slower than `awq_marlin` INT4** — the opposite of bare-metal intuition. Prefer AWQ-Marlin on WSL2.
- **FLUX.2-dev (32B) does not fit 32 GB natively** — every workflow must quantize (Nunchaku NVFP4, GGUF Q8) or offload (stable-diffusion.cpp `--offload-to-cpu` → RAM). There is no "just load it" path.
- **RL on one 5090 is bounded:** veRL/OpenRLHF shine at 8×GPU; locally the practical ceiling is **GRPO/DPO on a 1.5–7B policy** with a colocated vLLM rollout in WSL2 (gpu-mem-util ~0.4–0.5), or **TRL/Unsloth DPO** as the cheap no-Ray path.

## Standards compliance (the six)

Same posture as [wave 1](../wave-01-foundation/dispatch.md#standards-compliance), with two notes. **ANDON_AUTHORITY — 2→ enacted:** the verifier's `unverified`/`refuted` flags plus a **post-load dedup pass** (9 rows removed before catalog regen — defects did not propagate downstream) is andon in action this wave. **NAMED_COMPENSATORS — 3:** no irreversible external calls; the dedup was a logged `DELETE` + FTS-rebuild + regenerate, and `load_db.py <wave-json>` remains the idempotent replace. **EXTERNAL_VERIFIER — 2:** tier-different (Sonnet) + retrieval oracle, family-different still the deferred P1. PIN_PER_STEP — 3 (script `scripts/wave-swarm.workflow.js`-derived, self-contained with embedded per-lane data). DECOMPOSE_BY_SECRETS — 2, UNCERTAINTY_GATED_HUMANS — 2.

## Wave-3 candidates

The verifier surfaced genuinely-new leads (filtering out re-proposals of already-covered engines like vLLM/SGLang/Triton/GGML/Diffusers/ComfyUI/TVM): **SageAttention 3** (deepen — FP4 attention, the diffusion win), **FlashMLA** (DeepSeek MLA kernels), **FlashKDA** (Moonshot Kimi Delta Attention), **NeMo-Aligner** (Megatron-scale alignment). Suggested wave-3 theme: **"the recipe-proving pass"** — actually run the top recipes on the rig and record measured tok/s + VRAM in `config_recipes`, turning the manual into a benchmarked one. See [verification.md](verification.md) for the full list + corrections.
