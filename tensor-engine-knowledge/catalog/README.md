# Catalog — tensor / inference / training engines

Generated from `engines.db` · wave 17 · 2026-09-07. Narrative + install plan: [wave-01 dispatch](../waves/wave-01-foundation/dispatch.md). Verification receipt: [verification.md](../waves/wave-01-foundation/verification.md).

The engines that **run and train** models on this rig (RTX 5090 · Blackwell · 32 GB VRAM · 64 GB RAM · Win 11). Sibling KB [model-knowledge](../../model-knowledge/catalog/README.md) catalogs the *models*; this one catalogs the *engines*.

## Fastest install shortlist

Top `recommended` picks per lane, install-priority order. `BW` = confirmed Blackwell/Windows-ready; `✓` = retrieval-verified this wave.

| Lane | ↓ | Engine | License | BW | Rig | Studio | ✓ |
|---|---|---|---|----|-----|--------|---|
| LLM inference engines | 1 | [LM Studio engine (llama.cpp + MLX backends)](llm-inference.md) | Proprietary (free for personal + commercial use; engine wraps MIT llama.cpp / Apache MLX) | ✓ | 5 | 4 | ✓ |
| LLM inference engines | 1 | [Ollama](llm-inference.md) | MIT | ✓ | 5 | 5 | ✓ |
| LLM inference engines | 1 | [llama.cpp (+ GGUF ecosystem)](llm-inference.md) | MIT | ✓ | 5 | 5 | ✓ |
| Serving, batching & routing | 1 | [llama.cpp server (llama-server)](llm-serving.md) | MIT | ✓ | 5 | 5 | ✓ |
| Serving, batching & routing | 3 | [TabbyAPI (ExLlamaV3 / EXL3)](llm-serving.md) | AGPL-3.0 (TabbyAPI); ExLlamaV3 MIT | ✓ | 5 | 4 | ✓ |
| Serving, batching & routing | 3 | [Text Embeddings Inference (TEI)](llm-serving.md) | Apache-2.0 | ✓ | 4 | 4 | ✓ |
| Structured output & constrained decoding | 1 | [Instructor](structured-output.md) | MIT | ✓ | 5 | 5 | ✓ |
| Structured output & constrained decoding | 1 | [XGrammar (XGrammar-2)](structured-output.md) | Apache-2.0 | ✓ | 5 | 5 | ✓ |
| Structured output & constrained decoding | 1 | [llama.cpp GBNF grammars + JSON-schema](structured-output.md) | MIT | ✓ | 5 | 4 | ✓ |
| Quantization frameworks & formats | 1 | [NVIDIA ModelOpt (TensorRT Model Optimizer)](quantization.md) | Apache-2.0 | ✓ | 5 | 4 | ✓ |
| Quantization frameworks & formats | 1 | [llama.cpp (GGUF + llama-quantize, k-quants / i-quants / imatrix)](quantization.md) | MIT | ✓ | 5 | 5 | ✓ |
| Quantization frameworks & formats | 3 | [ExLlamaV3 (EXL3 format)](quantization.md) | MIT | ✓ | 5 | 5 | ✓ |
| Attention backends & GPU kernels | 1 | [FlexAttention (PyTorch)](attention-kernels.md) | BSD-3-Clause (PyTorch license) | ✓ | 4 | 4 | ✓ |
| Attention backends & GPU kernels | 1 | [SageAttention (1 / 2 / 2++ / 3)](attention-kernels.md) | Apache-2.0 | ✓ | 5 | 5 | ✓ |
| Attention backends & GPU kernels | 1 | [cuDNN Fused Attention (SDPA backend)](attention-kernels.md) | NVIDIA cuDNN proprietary EULA (redistributable runtime; frontend Apache-2.0) | ✓ | 5 | 5 | ✓ |
| Training & fine-tuning engines | 1 | [Hugging Face TRL + PEFT](training.md) | Apache-2.0 | ✓ | 5 | 5 | ✓ |
| Training & fine-tuning engines | 1 | [OpenRLHF](training.md) | Apache-2.0 | ✓ | 3 | 2 | ✓ |
| Training & fine-tuning engines | 1 | [Unsloth](training.md) | Apache-2.0 (core); AGPL-3.0 (Unsloth Studio UI component) | ✓ | 5 | 5 | ✓ |
| Speech engines (ASR / TTS runtimes) | 1 | [Chatterbox TTS (Resemble AI)](speech-engines.md) | MIT (engine + weights) | ✓ | 5 | 5 | ✓ |
| Speech engines (ASR / TTS runtimes) | 1 | [Piper (OHF-Voice / piper1-gpl)](speech-engines.md) | GPLv3 (piper1-gpl); original rhasspy/piper was MIT | ✓ | 5 | 4 | ✓ |
| Speech engines (ASR / TTS runtimes) | 1 | [faster-whisper (CTranslate2)](speech-engines.md) | MIT (faster-whisper) / MIT (CTranslate2) | ✓ | 4 | 5 | ✓ |
| Diffusion inference engines | 1 | [ComfyUI](diffusion-engines.md) | GPL-3.0 | ✓ | 5 | 5 | ✓ |
| Diffusion inference engines | 1 | [InvokeAI](diffusion-engines.md) | Apache-2.0 | ✓ | 4 | 5 | ✓ |
| Diffusion inference engines | 3 | [Comfy-WaveSpeed (First Block Cache / TeaCache)](diffusion-engines.md) | MIT (per repo; verify) | ✓ | 4 | 5 | ✓ |
| Foundational runtimes & compilers | 1 | [CUDA Toolkit + cuDNN + cuBLAS (the substrate)](runtime-foundations.md) | Proprietary (NVIDIA CUDA Toolkit EULA); cuDNN/cuBLAS proprietary | ✓ | 5 | 5 | ✓ |
| Foundational runtimes & compilers | 1 | [PyTorch (eager + torch.compile / TorchInductor)](runtime-foundations.md) | BSD-3-Clause | ✓ | 5 | 5 | ✓ |
| Foundational runtimes & compilers | 1 | [ggml / llama.cpp](runtime-foundations.md) | MIT | ✓ | 5 | 5 | ✓ |
| Profiling, benchmarking & observability | 1 | [Arize Phoenix](profiling-bench.md) | Elastic License v2.0 (ELv2) | ✓ | 4 | 5 | ✓ |
| Profiling, benchmarking & observability | 1 | [NVIDIA Nsight Systems](profiling-bench.md) | Proprietary (free, NVIDIA SLA for Developer Tools) | ✓ | 5 | 4 | ✓ |
| Profiling, benchmarking & observability | 1 | [PyTorch Profiler (torch.profiler) + Holistic Trace Analysis](profiling-bench.md) | BSD-3-Clause (PyTorch); BSD-3-Clause (HTA) | ✓ | 4 | 4 | ✓ |

## Lanes

- [LLM inference engines](llm-inference.md) — Engines that load and run text/code/reasoning LLMs locally (16 engines)
- [Serving, batching & routing](llm-serving.md) — Production serving / batching / routing / multi-model + embedding & reranker servers (36 engines)
- [Structured output & constrained decoding](structured-output.md) — Grammar/JSON/tool-call engines that force LLMs to emit reliable structured output (8 engines)
- [Quantization frameworks & formats](quantization.md) — Quant algorithms, tools, and weight formats (GGUF/GPTQ/AWQ/EXL/FP8/FP4) (17 engines)
- [Attention backends & GPU kernels](attention-kernels.md) — FlashAttention/SageAttention/FlashInfer + attention & quantized-GEMM kernel libs (20 engines)
- [Training & fine-tuning engines](training.md) — Full / LoRA / QLoRA / RLHF / DPO training frameworks (20 engines)
- [Speech engines (ASR / TTS runtimes)](speech-engines.md) — Local speech-to-text & text-to-speech inference runtimes (the engine layer, not the models) (11 engines)
- [Diffusion inference engines](diffusion-engines.md) — Image/video diffusion runtimes & accelerators (the engine layer, not the models) (14 engines)
- [Foundational runtimes & compilers](runtime-foundations.md) — PyTorch/JAX/ONNX/TensorRT/MLX/ggml/Triton — what every other engine sits on (23 engines)
- [Profiling, benchmarking & observability](profiling-bench.md) — Tools to measure throughput / latency / VRAM and observe engines on this rig (28 engines)

## Legend

- **↓** install priority (lower = set up first; derived from status + maturity tier).
- **Comm** commercial use: ✅ yes / ⚠ conditional (read notes) / ⛔ no / ? unknown. (A permissive engine can still load a restrictively-licensed model — license is decided per-model too.)
- **BW** Blackwell/Windows-ready: ✓ runs on RTX 5090 / sm_120 / CUDA 12.8+ on Windows today / ✗ no / ? unconfirmed.
- **Rig** fit 0–5 for this exact rig (RTX 5090 · 32 GB VRAM · 64 GB RAM · Win 11). **Studio** fit 0–5 for the local single-user studio workload (vs datacenter-only tooling).
- **✓** retrieval-verified this wave (existence + license + specs). Blank/· = unverified lead.
