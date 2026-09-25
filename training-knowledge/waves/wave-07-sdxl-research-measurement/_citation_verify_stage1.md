# Concept-B study-swarm — Step-4 citation verification (Stage 1: retrieval oracle)

Stage-1 = WebFetch retrieval against arXiv (existence + attribution). Run 2026-06-07 during the Chroma dim8 training window.
Stage-2 (family-different ollama groundedness) is deferred to a GPU-free window before the wave-07 fold.

## High-risk subset (postdate-training / less-famous) — ALL REAL, 2 attribution fixes
| arXiv | swarm attribution | retrieval verdict | fix for fold |
|---|---|---|---|
| 2512.12963 | "SCAdapter authors (building on IP-Adapter, Ye et al.)" 2025 | ✅ real — *SCAdapter: Content-Style Disentanglement for Diffusion Style Transfer* | authors = **Trinh, Doi, Osanai** 2025 |
| 2508.09814 | "Jiang, et al." 2025 | ✅ real, topic matches — but **MISATTRIBUTED** | authors = **Hernández-Cámara, Jaén-Lorites, Gómez-Villa, Vila-Tomás, Laparra, Malo** 2025 |
| 2405.14908 | Ge, Ma, Chen, Li, Ding 2024 (BiMix) | ✅ exact match | — |
| 2404.01413 | Gerstgrasser et al. 2024 | ✅ exact match | — |
| 2403.14572 | Frenkel, Vinker, Shamir, Cohen-Or 2024 (B-LoRA) | ✅ exact match | — |

No FABRICATED verdicts. The two fixes are MISATTRIBUTION/loose-attribution (real paper, wrong/vague author) — correct in the
wave-07 research-raw.json sources, not blockers.

## Still to verify before the fold (Batch B)
- Classics (high confidence, real, but run the oracle for completeness): Custom Diffusion 2212.04488, Mix-of-Show 2305.18292,
  ZipLoRA 2311.13600, Cones2 2305.19327, OFT 2306.07280, StyleDrop 2306.00983, CMMD 2401.09603, Carlini 2301.13188,
  Shumailov 2305.17493 + Nature 10.1038/s41586-024-07566-y, DoReMi 2305.10429, Data Mixing Laws 2403.16952.
- Stage-2 family-different groundedness (ollama-intern two-family, GPU-free window): does each one-sentence finding match
  what the source actually claims (NLI-style). Per research-grounded-advisor-protocol Step 4.
