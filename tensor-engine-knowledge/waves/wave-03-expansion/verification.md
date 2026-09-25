# Wave 3 — Verification receipt

The EXTERNAL_VERIFIER stage for wave 3. Method identical to waves 1–2: a separate, reasoning-stripped, **different-tier (Sonnet)** verifier per lane using live web retrieval as the existence/license/spec/currency oracle. Family-different (local non-Claude on the 5090) remains the deferred P1 — and the new `profiling-bench` lane now gives the rig the tooling to stand it up.

## Verdict distribution

**39 new engines verified · 10 `confirmed` · 29 `confirmed-with-fixes` · 0 `unverified` · 0 `refuted`** — the cleanest wave yet (every new engine resolved to a real, current page). Currency: 37 current, 2 deprecated. License: 34 ok, **5 corrected**.

**No dedup pass was needed.** The 3 new lanes are fresh categories; the 2 deepen lanes were handed their "already covered" lists and added only genuinely-new rows. A near-dup scan confirmed the only shared name-stems are distinct tools/facets (PyTorch Profiler ≠ PyTorch; llama-bench ≠ llama.cpp; vLLM benchmark suite ≠ vLLM; llama.cpp GBNF ≠ the llama.cpp engine) — all legitimately separate entries in their own lanes.

## Material corrections

### Blackwell status over-claimed (the recurring sm_120 trap)
- **FlashMLA / DeepGEMM / TLX Block Attention / trtllm-gen FMHA** — all emit `tcgen05`/`wgmma` (SM100/SM90 only); **they do not run on sm_120**. TLX's `blackwell_ready:false` was itself corrected to "Blackwell-exclusive for SM100, sm_120 unconfirmed" (it's a B200 kernel, not a no-Blackwell one). Route 5090 MLA through FlashInfer XQA instead.
- **ms-swift** — `blackwell_ready:true` **refuted** by issue #4834 (sm_120 not supported); corrected to false. (MLLM count corrected 300→400+.)
- **faster-whisper** — `blackwell_ready:true` **refuted**: default `int8_float16` crashes on the 5090 (CUBLAS_STATUS_NOT_SUPPORTED, CTranslate2 INT8 padding bug; fix merged upstream but not in the 4.7.2 wheel). Works at `compute_type="float16"`.
- **structured-output libs** — `blackwell_ready:true` across all 8 was flagged speculative: these are CPU-side logits processors, so the flag is meaningless at the library level (Blackwell-readiness belongs to the host inference engine). Catalogued accordingly.
- **ONNX-dependent speech engines** (sherpa-onnx, Piper, Kokoro-ONNX, Moonshine) — CUDA sm_120 path unverified (ONNX Runtime sm_120 gap, onnxruntime #26177/#27875); **DirectML is the working non-CUDA GPU path on Windows**.

### License corrections (5)
| Engine | Correction |
|---|---|
| **TLX Block Attention** | `unknown` → **Apache-2.0** (commercial: yes), confirmed via LICENSE file. |
| **Holistic Trace Analysis** (in the PyTorch Profiler entry) | **MIT**, not BSD-3-Clause (PyTorch itself is BSD-3; HTA is a separate MIT repo). |
| **LMFlow** | `yes` → **conditional**: Apache-2.0 code, but the README adds an explicit commercial-authorization-form requirement. |
| **Coqui XTTS-v2** | Engine fork is **MPL-2.0** (confirmed); the **model weights are Coqui Public Model License = non-commercial** — ship with Kokoro/Piper, not XTTS. |
| **Kyutai STT/TTS** | code is **dual Apache-2.0/MIT**; the **tts-1.6b weights are CC-BY-4.0** (attribution required) — precise, not "typically MIT/Apache". |

### Currency + version drift
- **Deprecated:** **Jsonformer** (no commits since 2023, no releases) and **NeMo-Aligner** (archived Nov 2025 → use **NeMo-RL** v0.6.0). Both kept only as historical reference.
- Version corrections: **llguidance** 1.0.0 → **1.7.5** (7 minors stale), **AIPerf** 0.8 → **0.9.0**, **Arize Phoenix** 15.1 → **17.0**, guidance 0.3.1→0.3.2, LM Format Enforcer confirmed 0.11.3; **gpustat** "2026-03 update" refuted (last is 1.1.1 from 2023).
- **Misleading citations caught:** the whisper.cpp discussion #3460 cited by a researcher is about **AMD ROCm, not Blackwell**; the SkyRL arXiv 2511.16108 resolves to the SkyRL-**Agent** paper, not the core RL library. Both flagged in `verify_note`.

## Wave-4 candidates

Filtering out re-proposals of engines already in the KB (Unsloth, LLaMA-Factory, SGLang, vLLM guided decoding, Triton, CUTLASS):

- **structured-output:** llama-cpp-python (the Python GBNF/JSON-schema binding — the missing Python-on-Windows path).
- **speech-engines:** Vosk (offline kaldi-derived ASR, Apache-2.0), StyleTTS 2 (MIT high-quality TTS), Parakeet→ONNX-for-sherpa (the commercial-safe NVIDIA-ASR-without-NeMo path).
- **profiling-bench:** GuideLLM (Red Hat/vLLM's own recommended server-benchmark), MLflow Tracing, NVIDIA DCGM (note: Linux-only, reference).
- **attention-kernels:** CUTLASS 3.x (the FP8/FP4 GEMM primitive layer under FlashKDA/DeepGEMM), the in-progress FlashAttention-3 Blackwell port.
- **training:** NeMo-RL (formal row — the active NeMo-Aligner successor).

> **Wave-4 = the recipe-proving pass.** Three waves have built 134 engines + 133 sourced config recipes. Wave 4 is the moment to *measure*: with `profiling-bench` now catalogued (nvitop, llama-bench, AIPerf, Nsight), run the top recipes on the actual 5090 and write measured tok/s + peak VRAM back into `config_recipes` — turning sourced-claims into rig-truth — and stand up the long-deferred **family-different verifier** (a local non-Claude model) using the engines this KB now documents. That closes the loop the protocol has wanted since wave 1.
