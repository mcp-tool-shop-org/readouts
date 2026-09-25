# Wave 2 — Verification receipt

The EXTERNAL_VERIFIER stage for wave 2, plus the post-ingest **dedup pass** (this wave's andon action). Method identical to [wave 1](../wave-01-foundation/verification.md): a separate, reasoning-stripped, **different-tier (Sonnet)** verifier per lane using live web retrieval as the existence/license/spec/currency oracle. Family-different (`prism verify` / local non-Claude) remains the deferred P1.

## Verdict distribution

**27 new engines verified · 3 `confirmed` · 22 `confirmed-with-fixes` · 2 `unverified` · 0 `refuted`.** Currency: 20 current, 1 superseded, 1 deprecated, 1 unknown (+4 n/a). License: 26 ok, **1 corrected** (AMD ROCm).

As in wave 1, the high `confirmed-with-fixes` rate is version-currency churn, not quality problems. Both `unverified` rows were removed in the dedup pass below (the stray "lane note" + the wave-2 MLC-LLM duplicate), so **every kept wave-2 engine is verified**; the KB's lone `verified=0` row remains the wave-1 MLC-LLM lead.

## Dedup pass (9 rows removed before catalog regen)

Wave 2 was told the per-lane "already covered" list, but researchers still re-listed engines in a *second* lane (an engine can plausibly belong to two), and one agent emitted a lane note as an engine. To keep **one row per distinct project** (honest counts, no divergent double-entries), 9 rows were deleted post-ingest — all wave-2 rows; no wave-1 row was touched. Cross-lane relevance is preserved via the config-recipes and prose, not duplicate engine rows.

| Removed (wave 2) | Reason — kept canonical row |
|---|---|
| NVIDIA Triton (→llm-inference) | dup of wave-1 Triton in llm-serving (its real lane) |
| Ollama (→llm-serving) | dup of wave-1 Ollama in llm-inference |
| Aphrodite Engine (→llm-serving) | dup of wave-1 Aphrodite in llm-inference |
| KTransformers (→runtime-foundations) | dup of wave-1 KTransformers in llm-inference |
| TensorRT-LLM (→quantization) | dup of wave-1 TensorRT-LLM in llm-inference (quant facet kept in recipes) |
| torchao (→diffusion-engines) | dup of the wave-2 torchao in quantization (its primary home) |
| Nunchaku (→diffusion-engines) | within-lane dup of wave-1 Nunchaku |
| MLC-LLM (→runtime-foundations) | dup of wave-1 MLC-LLM; wave-2 entry was *also* `verified=0`, so no gain |
| "ThunderKittens-class note…" | not an engine — a lane note emitted into the engines list |

## Material corrections the verifier caught

**Blackwell status over-claimed (sm_120 specifically):**
- **veRL** — `blackwell_ready` refuted by open issue #3664 (FSDP `RuntimeError` on sm_120, unresolved); runs, but not clean on a 5090.
- **torchtitan** — MXFP8 Blackwell support is **B200 / sm_100 (datacenter) only**, not RTX-50 sm_120.
- **InvokeAI** — `blackwell_ready` refuted by open crash bug #9164 on RTX 50-series (unresolved as of v6.13.0).
- **NATTEN** — fast FNA/FMHA kernels documented in source but **not in prebuilt wheels**, and sm_120 absent from all docs (falls back to CUTLASS/Flex on a 5090; Linux-only wheels).
- **trtllm-gen FMHA / flashinfer-cubin** — shipped only Sm100a/Sm100f/Sm103a cubins; on a 5090 the loader fell through to a wrong-arch cubin and **emitted garbage tokens with no error** (flashinfer #3294). Do not chase this path on stock wheels.

**License + attribution:**
- **AMD ROCm** — `license_status: corrected`: "mostly MIT/Apache-2.0" *understates* the diversity; the live per-component table mixes MIT (HIP), Apache-2.0, and closed firmware blobs. Catalogued as reference (no AMD GPU on this rig) regardless.
- **Aphrodite** maintaining org is **dphnAI** (not PygmalionAI); **Nunchaku** repo is **nunchaku-ai** (not nunchaku-tech) — both stale attributions corrected.
- Version drift corrected on most rows (mistral.rs v0.8.3, ModelOpt v0.44.0, torchao v0.17.0, TensorRT-LLM v1.2.1, OpenRLHF v0.10.3, veRL v0.8.0, InvokeAI v6.13.0, tinygrad v0.13.0).

## Currency flags

- **trlX** (CarperAI) — `deprecated`: last release June 2023, no 2026 activity. Kept as a legacy-reference RL entry only; use veRL/OpenRLHF/TRL.
- **GPUStack** — native-Windows workers dropped in v2 (WSL2-only now); situational on this rig.
- **TensorRT-LLM** — native Windows **deprecated at v0.18.0** (Linux/WSL2 only); the FP4 fast lane is a WSL2 path.

## The lone unverified row (carried)

**MLC-LLM** (wave-1, llm-inference, `verified=0`) — wave 2 re-researched it and *still* couldn't confirm a clean semver release cadence (nightly-only/JIT). It stays as a documented lead, not gospel. Everything else in the KB is retrieval-verified.

## Wave-3 candidates

Filtering out re-proposals of engines already in the KB (vLLM, SGLang, TGI, Triton, GGML, TVM, Diffusers, ComfyUI, LM Studio, HF TRL), the genuinely-new leads:

- **attention-kernels:** **SageAttention 3** (deepen the existing entry — FP4/FP8/INT8 quantized attention, the diffusion win) · **FlashMLA** (DeepSeek MLA kernels, Hopper+Blackwell) · **FlashKDA** (Moonshot Kimi Delta Attention, SM90+).
- **training:** **NeMo-Aligner** (Megatron-scale alignment with TRT-LLM rollout).

> **Wave-3 suggestion — the "recipe-proving" pass:** wave 2 produced 56 config recipes from documentation + benchmarks. Wave 3 should *run* the top recipes on the actual rig and record measured tok/s + peak VRAM back into `config_recipes`, plus add SageAttention 3 / FlashMLA. That turns the operations manual from sourced-claims into rig-measured truth — and is the natural place to finally stand up the **family-different verifier** (a local non-Claude model on the 5090) the protocol has on its P1 backlog.
