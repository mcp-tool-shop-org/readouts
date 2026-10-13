# Dataset Production Doctrine
**Swarm ID:** `brainstorm-dataset-2026-09-27`  
**Date:** 2026-09-27  
**Agent Roster:** Agent 1 (Code/Text), Agent 2 (Visual), Agent 3 (Multi-Modal / Synthetic), Agent 4 (Eval / Benchmarks), Agent 5 (Provenance / Licensing), Agent 6 (Citation Verification), Agent 7 (Synthesis / Gap Detection), Agent 8 (Author — this document)

---

## 1. Taxonomy of Dataset Types

The org produces five dataset families. Each family shares the same canonical pipeline stages but requires modality-specific tooling.

| Type | Description | Example Formats |
|------|-------------|-----------------|
| **Code / Text** | Instruction-following, pre-training, and repo-level completion data | Alpaca, ShareGPT, OpenAI Messages, raw file + `<\|endoftext\|>` (Agent 1) |
| **Visual / Image** | Diffusion training, LoRA fine-tuning, and segmentation masks | ImageFolder + sidecar JSON, WebDataset `.tar` shards, Parquet (Agent 2) |
| **Multi-Modal** | Paired text-image, video-caption, audio-transcript, 3D-description | WebDataset / Parquet, JSONL metadata, Kaldi Audio, glTF/USDZ (Agent 3) |
| **Evaluation / Benchmark** | Held-out test sets and live eval surfaces | Static splits (GLUE, MMLU), dynamic platforms (HELM, Dynabench) (Agent 4) |
| **Synthetic** | Model-generated or procedurally rendered training data | Any of the above, with mandatory generational tags (Agents 1–3) |

---

## 2. Canonical Pipeline

Every dataset—regardless of type—passes through six stages:

**Ingest → Validate → Transform → Package → Version → Publish**

| Stage | Code / Text | Visual / Image | Multi-Modal |
|-------|-------------|----------------|-------------|
| **Ingest** | Clone repos, extract commit diffs (CommitPack), docstring pairs (CodeSearchNet), or instruction triples (Agent 1) | Scrape, upload, or synthesize images; collect source URLs and licenses (Agent 2) | Aggregate URL/caption Parquets, video clips, audio FLAC, or 3D assets (Agent 3) |
| **Validate** | License scan (SPDX), exact + near dedup (MinHash + AST), contamination check vs. eval sets (Agent 1) | CLIP-score / aesthetic threshold, perceptual hash dedup (pHash), EXIF audit (Agent 2) | Schema validation, synthetic-collapse entropy check, PII scan (Agents 3, 5) |
| **Transform** | Normalize to target schema (Alpaca → OpenAI Messages), filter by language, prune over-represented repos (Agent 1) | Aspect-ratio bucketing, captioning (BLIP / WD14), tag normalization, VAE latent caching (Agent 2) | Align modalities by timestamp or ID, resize / transcribe, generate synthetic variants (Agent 3) |
| **Package** | JSONL shards with sidecar metadata | ImageFolder or WebDataset `.tar` shards + Croissant manifest (Agent 2) | Parquet metadata + blob store, or WebDataset shards for streaming (Agent 3) |
| **Version** | Git commit + DVC hash / HF Hub revision (Agent 3) | Immutable snapshot hash, CAS (IPFS/DVC) (Agents 2–3) | Same as visual; treat metadata and blobs as separate revisioned layers (Agent 3) |
| **Publish** | Push to HuggingFace Hub with README datasheet (Agents 1, 4) | Push to Hub with aesthetic distribution and tag-frequency reports (Agent 2) | Upload to Hub; enable streaming via `datasets` library (Agent 3) |

Agents 1–4 converge on **HuggingFace Hub** as the de facto distribution layer (Agent 7, Convergence 4).

---

## 3. Metadata Schema

Every sample must carry **minimum viable provenance**. Agents 1, 2, and 5 each produced incompatible field lists. The doctrine resolves this by adopting **Croissant** (MLCommons, 2024) as the machine-readable backbone (Agent 5) and mapping modality-specific extensions into it (Agent 7, Recommendation 2).

| Field | Source | Required For |
|-------|--------|--------------|
| `source_url` | Agent 1 (`source_url`), Agent 2 (Source URL) | All |
| `license` / `spdx_license` | Agent 1 (SPDX preferred), Agent 2 (License), Agent 5 (all licenses) | All |
| `content_hash` / `commit_hash` | Agent 1 (`commit_hash`), Agent 3 (CAS) | Code, synthetic |
| `extraction_timestamp` / `capture_date` | Agent 1, Agent 2 | All |
| `modality` / `language` | Agent 1 (`language`), Agent 3 (modality) | All |
| `file_path` / `relative_path` | Agent 1 (`file_paths`) | Code, multi-modal |
| `synthetic_flag` | Agent 2 (synthetic flag), Agent 3 (provenance tagging) | All synthetic |
| `generation_prompt` | Agent 2 (Generation prompt) | Synthetic visual, text |
| `model_version` / `checkpoint` | Agent 2 (Model / checkpoint) | Synthetic |
| `seed`, `sampler`, `cfg` | Agent 2 | Synthetic visual |
| `post_processing` | Agent 2 | Visual |
| `provenance_chain` | Agent 5 (Data Provenance Initiative) | Aggregated datasets (100+ sources) |

[INFERRED] For aggregated datasets, a top-level Croissant manifest should reference the Data Provenance Initiative explorer (Longpre et al., 2023) to verify commercial openness per slice (Agent 5).

---

## 4. Format Recommendations

### 4.1 Code / Text: JSONL
JSONL is the interoperability standard for text (Agent 1). Alpaca, ShareGPT, and OpenAI Messages are all line-delimited JSON. JSONL is trivial to parse, stream, and diff. The org should default to JSONL for all code and text datasets.

### 4.2 Visual / Multi-Modal at Scale: WebDataset
WebDataset (sequential `.tar` shards) is the dominant format for high-throughput visual training (Agent 2). LAION-5B and img2dataset use it because it avoids random-seek index files and streams efficiently from object storage (Agents 2–3). For multi-modal text-image pairs, WebDataset or Parquet + blob storage should be used (Agent 3).

### 4.3 The Schism and Resolution
**Contradiction:** Agents 1 and 2 treat JSONL and WebDataset as mutually exclusive defaults (Agent 7, High severity). This blocks a unified pipeline.

**Resolution:** Adopt a **per-modality format policy with an explicit translation layer**.
- Code / text → JSONL (default)
- Visual / multi-modal → WebDataset or Parquet (default)
- At training time, a thin converter maps JSONL samples into WebDataset shards (or vice versa) so that cross-modal experiments can mix modalities without re-architecting storage.

[SPECULATIVE] The exact converter implementation (streaming vs. batch) was not evaluated by this swarm and should be prototyped in the next phase.

---

## 5. Quality Gates

A dataset does not ship if any of the following are true:

| Gate | Rule | Source |
|------|------|--------|
| **Contamination** | 13-gram exact-match check against all known eval sets; embedding-similarity audit for near-matches (Agent 1). For visual corpora, perceptual-hash check against ImageNet / COCO test splits [INFERRED from Agent 7 gap]. | Agent 1 (Chen et al., 2021; Lai et al., 2022); Agent 4 (Rajpurkar et al., 2016) |
| **License Conflict** | Every slice must have a verifiable SPDX identifier or explicit license text. Aggregated datasets must isolate copyleft slices (CC BY-SA, CDLA-Sharing) from permissive ones (Agent 5). | Agent 5 (Creative Commons, 2013; Linux Foundation, 2017) |
| **No Evidence** | Every sample must trace back to a `source_url` or `generation_prompt`. Datasets with >5% unattributed samples are rejected (Agent 5). | Agent 5 (Longpre et al., 2023; Gebru et al., 2021) |
| **Low Diversity** | Entropy of embedding-space clusters must not drop below baseline. N-gram novelty (text) or perceptual diversity (image) must be logged. Synthetic data requires generational tags and a real-data mixing ratio >0 [SPECULATIVE: exact ratio unquantified] (Agent 3). | Agent 3 (Shumailov et al., 2023); Agent 2 (pHash) |
| **Toxicity / PII** | Text: Perspective API or Detoxify scan + Microsoft Presidio PII audit (Agent 5). Visual: [SPECULATIVE] no tool was nominated for face/license-plate biometric scrubbing in this swarm (Agent 7 gap). | Agent 5 (Jigsaw, 2017; Unitary, 2021; Microsoft, 2020) |

---

## 6. Tool Assignments

| Org Tool | Pipeline Stage | Scope |
|----------|---------------|-------|
| **`repo-dataset`** | Ingest → Validate | Code/text repo extraction, commit-diff pairing, AST dedup, language tagging (Agent 1) |
| **`style-dataset-lab`** | Ingest → Transform → Package | Visual dataset production: captioning, aspect-ratio bucketing, tag pruning, latent caching, Croissant manifest export (Agent 2) |
| **`ollama-intern-mcp`** | Validate → Package | Bulk-analysis eval packs (`repo_pack`, `change_pack`, `incident_pack`) used as job-shaped validation surfaces; contamination checks via local LLM delegation (Agent 4) |
| **`ai-eyes-mcp`** | Validate | [INFERRED] Visual quality gates: CLIP-score distribution, aesthetic scoring, perceptual dedup. Not explicitly covered in Phase 1 reports; assigned by logical fit to close the visual-evaluation gap. |
| **`plain-sight`** | Publish | [INFERRED] License audit, provenance transparency, and EU AI Act documentation export. Not explicitly covered in Phase 1 reports; assigned by logical fit for governance finalization. |

---

## 7. Open Questions

The swarm could not resolve the following:

1. **Synthetic-to-real mixing ratio.** Agents 1 and 3 cite Shumailov et al. (2023) to warn against collapse, but no report quantifies the minimum real-data fraction required to preserve distribution tails in code or visual corpora.
2. **Visual PII and biometric risk.** Agent 5 covers text PII (Presidio), but no agent identified a standard tool or protocol for scrubbing faces, license plates, or sensitive EXIF from image corpora.
3. **EU AI Act metadata mandate.** Whether the Act's "detailed summary" requirement (Article 53) will be interpreted as mandating Croissant-format or similar structured metadata remains [SPECULATIVE]; regulatory guidance is pending (Agent 5).
4. **Cross-modal quality scorecard.** No agent proposed a unified metric that spans text perplexity, CLIP alignment, and audio-transcript WER. A cross-modal scorecard does not yet exist in the reports.
5. **Storage cost and tiering.** Petabyte-scale hot/warm/cold decisions were not modeled (Agent 7 gap).

---

## 8. Source Attribution Appendix

Every claim traces to a Phase 1 or Phase 2 report. Sources are grouped by agent.

**Agent 1 — Code / Text:** Allal et al. 2023 (SantaCoder); Chen et al. 2021 (HumanEval); Husain et al. 2019 (CodeSearchNet); Kocetkov et al. 2022 (The Stack); Lai et al. 2022 (DS-1000); Lee et al. 2021 (deduplication); Li et al. 2023 (StarCoder); Liu et al. 2023 (RepoBench); lm-sys 2023 (FastChat); Muennighoff et al. 2023 (CommitPack); OpenAI 2023 (fine-tuning API); Sahil 2023 (Code Alpaca); Shi et al. 2023 (contamination detection); Shumailov et al. 2023 (model collapse); Taori et al. 2023 (Alpaca); Wang et al. 2022 (Self-Instruct); Zhang et al. 2023 (RepoCoder).

**Agent 2 — Visual / Image:** Beaumont 2022 (img2dataset); Buchner 2013 (imagehash); bmaltais 2023 (kohya_ss); Gebru et al. 2021 (Datasheets); Hu et al. 2021 (LoRA); Kirstain et al. 2023 (Pick-a-Pic); LAION 2022 (LAION-5B); Li et al. 2022 (BLIP); Lin et al. 2014 (COCO); Mihcak et al. 2008 (perceptual hashing); MLCommons / Google 2023 (Croissant); Murray et al. 2012 (AVA); NovelAI 2022 (diffusion docs); Radford et al. 2021 (CLIP); Rombach et al. 2022 (Stable Diffusion); Saharia et al. 2022 (Imagen); Schuhmann et al. 2022 (LAION-5B); SmilingWolf 2022 (WD14 Tagger); von Platen et al. 2022 (Diffusers); Wu et al. 2023 (HPSv2); Yandex 2019 (WebDataset).

**Agent 3 — Multi-Modal / Synthetic:** Chang et al. 2015 (ShapeNet); Deitke et al. 2023 (Objaverse-XL); Denninger et al. 2019 (BlenderProc); DVC Docs 2024; Git LFS 2024; Goyal et al. 2017 (VQAv2); Hugging Face 2024; Li et al. 2022 (AlphaCode); Liu et al. 2023 (MMBench); Mathew et al. 2021 (DocVQA); Mozilla 2017 (Common Voice); NVIDIA 2024 (Isaac Sim); Panayotov et al. 2015 (LibriSpeech); Wang et al. 2023 (InternVid); Yue et al. 2023 (MMMU).

**Agent 4 — Evaluation / Benchmarks:** Bowman et al. 2015 (SNLI); Gao et al. 2020 (The Pile); Hendrycks et al. 2021 (MMLU); Jurafsky & Martin 2023; Kiela et al. 2021 (Dynabench); Krippendorff 2004; Liang et al. 2022 (HELM); Nie et al. 2020 (ANLI); Ouyang et al. 2022 (InstructGPT); Rajpurkar et al. 2016 (SQuAD); Wallace et al. 2019; Wang et al. 2018 (GLUE); mcp-tool-shop-org 2026 (swarm brief); ollama-intern-mcp v1.0.2.

**Agent 5 — Provenance / Licensing / Governance:** Apache Software Foundation 2004; Carlini et al. 2021 (training-data extraction); Creative Commons 2009/2013 (CC0, CC BY, CC BY-SA); European Parliament 2024 (EU AI Act); Holland et al. 2018 (Data Nutrition Labels); Jigsaw / Google 2017 (Perspective API); Linux Foundation 2017 (CDLA); Longpre et al. 2023 (Data Provenance Initiative); Lozhkov et al. 2024 (The Stack v2); Microsoft 2020 (Presidio); MIT 1980s; MLCommons 2024 (Croissant); Open Data Commons 2012 (ODC-BY); Penedo et al. 2023 (RefinedWeb); Together Computer 2023 (RedPajama); Unitary 2021 (Detoxify).

**Agent 6 — Citation Verification:** Verification results used to flag Agent 1's fabricated co-author and missing source-list entries.

**Agent 7 — Synthesis / Gap Detection:** Contradiction and coverage-gap tables used to structure Sections 4, 7, 10, and 11.

---

## 9. Contradictions Log

| # | Topic | Agents | Status |
|---|-------|--------|--------|
| 1 | **JSONL vs. WebDataset as canonical format** | Agent 1 advocates JSONL; Agents 2–3 advocate WebDataset / Parquet. | **Resolved:** Per-modality defaults with a translation layer at training time. Do not force visual pipelines into JSONL or text pipelines into `.tar` shards. |
| 2 | **Synthetic data risk tolerance** | Agents 1 & 3 warn strongly against model collapse and mandate generational provenance. Agent 2 describes BLIP-caption and SD-generation pipelines as standard LoRA practice without flagging collapse as a visual-domain risk. | **Partially resolved:** Doctrine adopts the stricter stance—generational tags are mandatory for all synthetic data, including visual. Agent 2's pipeline must be updated to include entropy/diversity checks and provenance tags. |
| 3 | **Deduplication interface** | Agents 1 (MinHash/AST), 2 (pHash), and 5 (fuzzy/exact substring) each propose modality-specific dedup algorithms. No agent designed a unified interface. | **Acknowledged, not resolved:** The org currently lacks a single dedup abstraction. Each tool owns its own algorithm. A future swarm should evaluate whether a generic "near-dedup" service is worth building. |
| 4 | **Quality metric currency** | Agent 2 uses CLIP-score / aesthetic-score for visual alignment. Agent 4 uses perplexity, downstream accuracy, and IAA for text/benchmarks. | **Acknowledged, not resolved:** Metrics are correctly modality-specific, but no cross-modal scorecard exists. See Open Question 4. |

---

## 10. Next Swarm

Agent 7 identified the largest uncovered gaps. The recommended follow-up work is:

1. **Storage, Streaming & Cost (2-agent mini-swarm).** Design the streaming DataLoader contract for WebDataset + JSONL hybrid runs, and model cloud-cost tradeoffs for TB-scale shards (Agent 7, Recommendation 3).
2. **Visual Contamination & Benchmark Leakage (1-agent follow-up).** Extend Agent 4's eval coverage to include perceptual dedup against ImageNet / COCO test sets and embedding-similarity checks for vision-language benchmarks (Agent 7, Recommendation 4).
3. **Cross-Modal Training Alignment (1-agent mini-swarm).** Specify how code snippets, images, and captions are batched together in a single forward pass—currently untouched in all reports (Agent 7 gap).
4. **Citation Hygiene Cleanup.** Agent 1 must correct the Code Alpaca author string and supply DOI/arXiv IDs for unverified entries before any dataset ships (Agent 6, Recommendation 1).
5. **Scaling-Law Guidance (1-agent mini-swarm).** Quantify data-volume requirements per modality. No agent discussed Chinchilla-optimal equivalents for code or vision (Agent 7 gap).
