# readouts — tensor-engine-knowledge

> Verified knowledge base of the ENGINES that run & train AI models locally on the RTX 5090 (Blackwell / sm_120 / Windows) rig.
>
> **193 engines · 134 verified · 491 sources · 17 waves · generated 2026-09-25.**  
> Decisive axis: native-Windows Blackwell survivability + commercial license (a LoRA/app inherits its engine's license).

## Domains

| Domain | Engines | Verified | Top pick | License | Readout |
|---|--:|--:|---|---|---|
| LLM inference engines | 16 | 15/16 | llama.cpp (+ GGUF ecosystem) | commercial | [`readout-llm-inference.html`](readout-llm-inference.html) |
| Serving, batching & routing | 36 | 14/36 | llama.cpp server (llama-server) | commercial | [`readout-llm-serving.html`](readout-llm-serving.html) |
| Structured output & constrained decoding | 8 | 8/8 | Instructor | commercial | [`readout-structured-output.html`](readout-structured-output.html) |
| Quantization frameworks & formats | 17 | 11/17 | llama.cpp (GGUF + llama-quantize, k-quants / i-quants / imatrix) | commercial | [`readout-quantization.html`](readout-quantization.html) |
| Attention backends & GPU kernels | 20 | 17/20 | cuDNN Fused Attention (SDPA backend) | commercial | [`readout-attention-kernels.html`](readout-attention-kernels.html) |
| Training & fine-tuning engines | 20 | 20/20 | Hugging Face TRL + PEFT | commercial | [`readout-training.html`](readout-training.html) |
| Speech engines (ASR / TTS runtimes) | 11 | 11/11 | Chatterbox TTS (Resemble AI) | commercial | [`readout-speech-engines.html`](readout-speech-engines.html) |
| Diffusion inference engines | 14 | 14/14 | ComfyUI | conditional | [`readout-diffusion-engines.html`](readout-diffusion-engines.html) |
| Foundational runtimes & compilers | 23 | 12/23 | CUDA Toolkit + cuDNN + cuBLAS (the substrate) | conditional | [`readout-runtime-foundations.html`](readout-runtime-foundations.html) |
| Profiling, benchmarking & observability | 28 | 12/28 | Arize Phoenix | conditional | [`readout-profiling-bench.html`](readout-profiling-bench.html) |

## Install-first shortlist (recommended, by KB download priority)

1. **Arize Phoenix** (Profiling, benchmarking & observability) — conditional
2. **bytefit** (Profiling, benchmarking & observability) — commercial
3. **Chatterbox TTS (Resemble AI)** (Speech engines (ASR / TTS runtimes)) — commercial
4. **ComfyUI** (Diffusion inference engines) — conditional
5. **CUDA Toolkit + cuDNN + cuBLAS (the substrate)** (Foundational runtimes & compilers) — conditional
6. **cuDNN Fused Attention (SDPA backend)** (Attention backends & GPU kernels) — commercial
7. **faster-whisper (CTranslate2)** (Speech engines (ASR / TTS runtimes)) — commercial
8. **FlexAttention (PyTorch)** (Attention backends & GPU kernels) — commercial
9. **ggml / llama.cpp** (Foundational runtimes & compilers) — commercial
10. **Hugging Face TRL + PEFT** (Training & fine-tuning engines) — commercial
11. **Instructor** (Structured output & constrained decoding) — commercial
12. **InvokeAI** (Diffusion inference engines) — commercial
13. **llama-bench (llama.cpp)** (Profiling, benchmarking & observability) — commercial
14. **llama.cpp (+ GGUF ecosystem)** (LLM inference engines) — commercial
15. **llama.cpp (GGUF + llama-quantize, k-quants / i-quants / imatrix)** (Quantization frameworks & formats) — commercial
16. **llama.cpp GBNF grammars + JSON-schema** (Structured output & constrained decoding) — commercial
17. **llama.cpp server (llama-server)** (Serving, batching & routing) — commercial
18. **LM Studio engine (llama.cpp + MLX backends)** (LLM inference engines) — conditional

## Go deeper

- **Per-domain readout:** `readout-<slug>.html` — filterable table + sources + verify trail
- **Wave dispatches** (research log): `waves.md` / `waves.html`
- **Verification receipt** (trust trail): `verification.md` / `verification.html`
- **Query the DB:** `engines.db (views v_recommended, v_best_for; FTS engines_fts)`
- **Resolve via loadout:** `ai-loadout resolve --project ./tensor-engine-knowledge`
- **Programmatic map:** `index.json`

## Provenance

Every fact carries a **wave id** and a **verified** flag; sources are retrieval-checked by a different-family verifier. 17 waves; 134/193 engines verified.
