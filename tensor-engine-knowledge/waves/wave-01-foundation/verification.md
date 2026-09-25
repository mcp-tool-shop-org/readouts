# Wave 1 — Verification receipt

The study-swarm **EXTERNAL_VERIFIER** stage, applied to this wave's own output before any row was trusted.

## Method

Each research lane's findings were handed to a **separate, reasoning-stripped** agent — it saw only the bare claims (engine name, developer, license, version, Blackwell/platform flags) + source URLs, never the researcher's reasoning or recommendations — that used **`WebFetch`/`WebSearch` as a retrieval oracle** to check, per engine: **exists** (does the repo/page resolve?), **license + commercial-use** correctness (with a correction if wrong), **spec plausibility** (latest version, `blackwell_ready` on sm_120/Windows, platforms, model_formats), and **currency** (current vs superseded/deprecated as of 2026-06-02). The default verdict on non-confirmation was `unverified`, not pass-on-faith.

**Honest scope.** The verifier is a **different model tier** (Sonnet) than the researcher (Opus), not a different *family* — both are Claude. The decorrelating element is the **retrieval oracle** (the live page), which is independent of the researcher's parametric claims and is what catches what same-lens LLM reasoning structurally cannot. The **family-different** upgrade (route through `prism verify` / `roleos verify-citations`, ideally a *local non-Claude* model on this rig per `hardware-omen-45l`) is the planned next-wave improvement — consistent with the protocol's documented P1 backlog. Treat this receipt as "retrieval-grounded, tier-different," not "family-different verified."

## Verdict distribution

**77 engines · 13 `confirmed` · 63 `confirmed-with-fixes` · 1 `unverified` · 0 `refuted`.**

Every engine but one resolved to a real, current repo/page — nothing was fabricated. The high rate of `confirmed-with-fixes` (not a quality problem) reflects how **fast this field moves**: the verifier corrected a version number or a Blackwell-status nuance on nearly every entry, because the assistant's training data predates the mid-2026 release wave. Per-engine verdicts are stored in `engines.verify_note` and surfaced in the catalog (`✓` column).

The single `unverified`: **MLC-LLM** — the claimed `v0.19.0` could not be confirmed from any live source (GitHub shows only a `v0.1.dev0` pre-release tag; no PyPI history retrieved). Kept in the DB as a lead with `verified=0`, not as a trusted row.

## Material corrections the verifier caught

### Blackwell status *inverted* (the researcher under-claimed — these DO work on sm_120)

The most valuable catch this wave: several engines were marked `blackwell_ready: false` that the live evidence **refutes**. Getting this wrong would have wrongly steered the studio away from working tools.

| Engine | Correction |
|---|---|
| **vLLM** | `false` is REFUTED — v0.17.0+ ships dedicated **SM120 FP8 GEMM**; RTX 5090 confirmed working (still Linux/WSL2 on Windows). |
| **SGLang** | `false` PARTIALLY WRONG — NGC 26.04 line + community builds run on consumer Blackwell. |
| **LMDeploy** | `false` REFUTED — v0.13.0 release notes explicitly add Blackwell (grouped-GEMM for Qwen3.5 MoE). |
| **TensorRT-LLM** | Active 1.3.x RC series with Blackwell support; the "1.x through ~2026-04" claim was stale/imprecise. |

### Blackwell status *over-claimed* (the researcher over-claimed — `true` lacked repo evidence)

| Engine | Correction |
|---|---|
| **FlashAttention 3 / 4** | Cannot run on sm_120 at all — the 5090 lacks the TMEM subsystem the warp-specialized FA3/FA4 kernels require. FA4 beta added SM120 code paths but they fall back to SM80-style MMA, not the fast path. |
| **FlashInfer** | `true` OVERSTATED — AOT cubin wheels ship **zero sm_120/sm_121 cubins** (issue #3294); unreliable on consumer Blackwell. |
| **Marlin / Machete** | `true` MISLEADING — Machete is Hopper-specific (SM90a wgmma PTX); only Marlin W4A16 carries to Blackwell. |
| **ExLlamaV3, ik_llama.cpp, llamafile, GPTQModel, AutoRound** | `true` UNVERIFIED by repo — they run on Blackwell (≥Turing baseline) but document no sm_120-specific kernels; correctness, not guaranteed peak speed. |
| **llama.cpp NVFP4** | `true` overstated *for NVFP4* — the Blackwell-native accel dispatch (PR #22196) was still **open**; MXFP4 is in master, NVFP4 acceleration is not. |
| **PyTorch / FSDP2 (Windows)** | `true` overstated for *Windows-native* — sm_120 is prototype on Linux/CUDA-12.8; stable Windows wheels still lacked it (nightly/source build required). |

### License corrections (4)

| Engine | Correction |
|---|---|
| **ComfyUI** | `commercial_use` should be **`yes` (with GPL-3.0 copyleft on redistribution)**, not `conditional`. GPL explicitly permits commercial use; the obligation is source-disclosure on distributing a modified binary, not a commercial cap. |
| **SageAttention** | Uniformly **Apache-2.0, commercial `yes`** — the "conditional / verify per-variant" claim is unsupported by the live LICENSE. |
| **ComfyUI_TensorRT** | The node repo is cleanly **MIT** (not "MIT-style"); the bundled TensorRT SDK carries NVIDIA's proprietary SLA. Developer is `comfyanonymous`, not `Comfy-Org`. |
| **HF TGI** | The HFOIL-1.0 claim was historically correct for v1.0+, but the archived (Mar 2026) main branch's LICENSE **now reads Apache-2.0** — possibly reverted on archival. Moot for new work (repo is dead), but verify the LICENSE file directly before relying on any TGI code. |

### Stale attributions / versions worth knowing

- **Nunchaku** org moved `nunchaku-tech` → **`nunchaku-ai`** (stale repo_url).
- **triton-windows** moved `woct0rdho` (archived Feb 2026) → official **`triton-lang/triton-windows`** (3.7.0.post26).
- **Ollama** version was off by ~24 releases (claimed v0.6.2; live v0.30.x). **Aphrodite** six majors behind (v0.10→v0.21, repo moved to `dphnAI/`). Smaller version drift on LM Studio, llamafile, TRL, kohya, Megatron, LLaMA-Factory, JAX, Triton, ParaAttention — all corrected in `verify_note`.

## Currency flags (7 — real, but prefer the newer pick)

`deprecated` — do not start new work:
- **Hugging Face TGI** (repo archived Mar 2026; relicensed then reverted) → use vLLM/SGLang (WSL2) or llama.cpp/Ollama (native).
- **TorchServe** (repo archived read-only Aug 2025) → BentoML or a vLLM/llama-server endpoint.
- **torchtune** (final v0.6.1; development wound down) → Unsloth / TRL+PEFT (and **torchtitan** for pre-training, a wave-2 candidate).
- **stable-fast** (author moved on) → **Comfy-WaveSpeed** (FBCache/TeaCache).

`superseded` — keep only with a specific reason:
- **HQQ** (last release Oct 2025; possible org transfer to `dropbox/`) → GGUF/EXL3/AutoRound.
- **OneDiff** (no release since Jul 2024; best quant is paywalled) → Nunchaku / ComfyUI-GGUF.
- **DeepCache** (SD1.5/SDXL-UNet era, no DiT support) → FBCache/TeaCache for modern FLUX/Wan/Qwen DiT models.

## Confidence caveats (carried from the lanes)

- **`blackwell_ready` is nuanced**, not binary. Many engines *run* on sm_120 via CUDA 12.8 but ship no sm_120-specific kernels — you get correctness, not peak throughput. The catalog's `BW` column means "runs on the rig today"; open each repo's install matrix before assuming peak performance.
- **FP4 (NVFP4/MXFP4)** is the headline reason to own a 5090, but consumer-Windows support is immature (kernels merged, Blackwell accel dispatch open; production path is WSL2/community-patched). No settled NVFP4-vs-Q4_K_M quality benchmark exists yet. Treat as a high-upside lane to watch.
- **WSL2 on consumer Blackwell** carried a known WDDM-paravirtualization hang bug (NVIDIA $1,000 bounty); WSL2 2.7.0 + recent driver largely fixes it but it is not zero-config.

## Verifier-proposed additions → wave 2 candidates

Each verifier was asked for up to 3 must-have engines the researcher omitted. 21 surfaced (none added this wave; these scope wave 2):

- **llm-inference:** mistral.rs (Rust-native, PagedAttention + FA2/3) · NVIDIA Triton Server (production serving layer) · Apple MLX / mlx-lm (Apple-Silicon reference).
- **llm-serving:** Ollama (cross-lane — the dominant local server) · TabbyAPI (the OpenAI-compatible EXL2/EXL3 server) · llama-server Router Mode (llama.cpp's built-in multi-model dispatch, competes with llama-swap).
- **quantization:** NVIDIA ModelOpt (the canonical NVFP4/FP8 PTQ producer) · torchao / pytorch-ao (the upstream PyTorch-native quant mechanism) · TensorRT-LLM built-in quantization (mature FP4 produce+serve).
- **attention-kernels:** ThunderKittens 2.0 (Blackwell CUDA DSL, MXFP8/NVFP4) · NATTEN (neighborhood/sparse attention, Blackwell FMHA) · TensorRT-LLM trtllm-gen FMHA (the source of the datacenter-Blackwell cubins FlashInfer/vLLM consume).
- **training:** veRL (the dominant RL post-training framework at 70B+) · OpenRLHF (Ray+vLLM+DeepSpeed RLHF reference) · torchtitan (Meta's active PyTorch-native pre-training successor to torchtune).
- **diffusion-engines:** stable-diffusion.cpp (the C/C++ GGUF diffusion engine — FLUX.2/Wan/Qwen) · torchao (the upstream FP4/FP8 mechanism) · InvokeAI (Apache-2.0, commercially friendlier than GPL ComfyUI).
- **runtime-foundations:** AMD ROCm (the AMD substrate analog) · MLC-LLM (TVM-based cross-platform runtime — promote/resolve its version) · tinygrad (emerging pure-Python compiler/runtime).

> **Wave 2 suggestion:** a focused **"WSL2 throughput-serving + FP4 producers + RL post-training"** pass would close most of these and deepen the two thinnest areas — the datacenter-class serving path (when the studio genuinely needs fleet batching) and the FP4 produce→serve pipeline as it matures on consumer Blackwell.
