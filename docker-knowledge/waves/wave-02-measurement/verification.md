# Wave 2 — Verification receipt

3-lens, reasoning-stripped, applied before any row was trusted.

## Method
1. **Retrieval oracle** (`WebFetch`) — existence + attribution + content-groundedness. The authority on existence (and, for docs/forum sources, the load-bearing groundedness lens too — it fetched the actual pages).
2. **mistral-small:24b** (Mistral) — family-different groundedness.
3. **granite4.1:30b** (IBM Granite) — family-different groundedness.

**ANDON note:** Ollama was unreachable when the family pass began. It was RESTARTED (`ollama serve`) and the pass completed — verifier-unavailable was NOT read as "fine", and the wave was NOT loaded until the family lens ran (per doctrine: restore the verifier, don't skip it).

## Verdict distribution
**41 unique citations · 41/41 exist · 0 fabricated.** Oracle groundedness: 31 SUPPORTED, 9 PARTIAL, 1 NOT_SUPPORTED. Attribution: 34 MATCH, 7 MISMATCH. Source types are mostly NVIDIA docs, GitHub issues, forum threads, and vendor blogs (not papers), so the retrieval oracle is the load-bearing lens; the LLM families are decorrelating corroboration.

## Family-different outcome
- **granite** — 0 fabrication flags; caught one real terminology imprecision: #6, PCIe "64 GB/s bidirectional" is per-direction (~63; ~128 aggregate). Folded into the finding's `verifier_note` + the dispatch. (granite's own counter-figure of 32 was itself wrong; the *catch*, not the number, was the value.)
- **mistral** — 0 fabrication flags; ~8 `S=N` were priors-not-knowledge on oracle-confirmed facts (e.g. it denied that WSL2 containers carry "microsoft" in `/proc/version` — the oracle fetched the issue proving they do). Discarded where the oracle read the page.
- **Union** — no genuine refutation; 0 fabrications across all three lenses. The decorrelation worked: granite surfaced the one fix; mistral's over-skeptic noise was filtered by the oracle.

## Material actions
- **FLAGGED (not dropped wholesale):** `forums.developer.nvidia.com/t/.../304136` — a real thread, but about an nvidia-smi-tool-vs-driver version mismatch, NOT the cited "driver-API max-CUDA" claim. The source is marked `finding_supported=NOT_SUPPORTED`; the claim itself is independently true and its finding stands on other sourcing.
- **7 attribution corrections**, almost all 2025→2026 issue-year drift (recent GitHub issues opened Jan 2026), plus one byline (the PyTorch caching-allocator devlog is ezyang, not DeVito). Substance SUPPORTED in every case; stored in `verifier_note`.
- **9 PARTIAL** — a sub-claim unverified or scope-narrowed; findings retained, partial recorded per source.
