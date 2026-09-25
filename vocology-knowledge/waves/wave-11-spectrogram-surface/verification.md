# Wave 11 — citation verification

**Dispatch:** [`dispatch.md`](dispatch.md)
**Receipt:** [`citation-receipt.json`](citation-receipt.json)
**Prism:** `prism-01m1z0rr8h868h51eswe428b38` · verdict **revise (advisory, non-blocking, 0 fabricated)** · `chain_sha256 dd54a5e2…` · `citations_sha256 18450cbd…`
*(Run against the final dispatch text. Two earlier runs on the same citation set — `prism-01m1z03955afxeqkv1s0ek7wzq`, then `prism-01m1z0c3h1c7qh9xdqn0e58j3x` after the finding-2 correction — carry the identical `citations_sha256`, so the prose edits between them did not touch a citation.)*
**Runner:** `roleos verify-citations` (role-os 2.10.0) → `prism verify --type citations --provider ollama` (prism 1.6.0), Ed25519-signed with the rig's existing key. Synthesizer family: anthropic (Fable coordinator, Opus lanes); verifier seat: non-Claude Ollama model, reasoning-stripped, plus the arXiv/Crossref retrieval oracle. Run 2026-09-07, 30.9 s.

## Result

| bucket | count | citations |
|---|---|---|
| existence resolved | **26 / 26** | every arXiv and DOI identifier in the dispatch |
| fabricated | **0** | — |
| accept (abstract supports the finding) | 14 | 1, 5, 6, 7, 8, 9, 10, 16, 18, 19, 20, 22, 24, 25 (prism ids c1, c5–c10, c16, c18–c20, c22, c24–c25) |
| escalate — retrieve full text (claim lives in the paper body) | 10 | c3 2511.13225 · c11 2203.09893 · c12 2212.04356 · c13 2104.01778 · c14 1710.11153 · c15 1802.06182 · c17 fpsyg.2026.1920074 · c21 2509.00051 · c23 2508.18440 · c26 2411.11123 |
| revise — abstract-level lens reads "contradicted" | 2 | c2 2411.12058 (ablation numbers) · c4 journal.pdig.0001179 (32.0 / 36.3 %) |
| unparsed (no arXiv/DOI — docs, specs, npm, vendor pages) | 16 | findings 11, 16, 17, 20–23, 25, 26, 32, 33, 39–49 URLs — retrieved by the lane agents |

## Settling the 12 non-accepts (full-text retrieval, 2026-09-07)

Same class as waves 1–2: the abstract-bounded lens cannot see a number that lives in a table or a methods paragraph. Each was settled by fetching the full text (`arxiv.org/html/<id>` or the PMC article) and locating the claim verbatim.

| id | source | what the full text says | outcome |
|---|---|---|---|
| c2 | Dixit 2024 ablation | Table: default 27.50 · linear frequency 35.00 · linear amplitude 30.00 · remove labels 26.25 · show colorbar 23.75 · magma 25.00 · mel 25.00 · MFCC 13.75 · low resolution 20.00; §2.2: default is viridis, log/log, "we added axis labels and removed the colormap scale"; few-shot 70.00, k-means 2-shot 76.25. | **Finding 2 restated** from the table (the first draft mis-read the label effect as 35→26). Render default flipped to viridis (L3, finding 20). The 50-class ESC-50 figure the lane reported (14%) was not found in the grep and is **dropped**. |
| c4 | Dietrich 2026 | "overall accuracy for zero-shot and few-shot strategies at 32.0% and 36.3%, respectively … a random-chance classifier would achieve an accuracy of 25%". The abstract's 96.0% is a different quantity. | supported as written |
| c3 | Loakman 2025 | "the ASR model achieves an accuracy of 87.56%"; human "accuracy of 75.00%"; "zero-shot and finetuned models rarely perform above chance". | supported |
| c11 | Basic Pitch 2022 | "a Constant-Q Transform (CQT) with 3 bins per semitone and a hop size of ≈ 11 ms"; harmonic stacking. | supported |
| c12 | Whisper 2022 | "an 80-channel log-magnitude Mel spectrogram … 25-millisecond windows with a stride of 10 milliseconds". | supported |
| c13 | AST 2021 | "128-dimensional log Mel filterbank … 25ms Hamming window every 10ms"; "0.485 mAP on AudioSet". | supported |
| c14 | Onsets and Frames 2018 | "229 logarithmically-spaced frequency bins, a hop length of 512, an FFT window of 2048, and a sample rate of 16kHz"; note F1 82.29. | supported |
| c15 | CREPE 2018 | Table 2: 50 cents 0.967 / 0.919; 10 cents 0.909 / 0.826 (MDB-stem-synth). | supported |
| c17 | Zhang 2026 | "teachers should position such tools as auxiliary means of observation rather than as standalone instructional interventions"; "thinly populated". | supported |
| c21 | Kader & Karmaker 2025 | "CLAP-score, FAD, and KLD, often align poorly with human preferences". | supported |
| c23 | SwiftF0 2025 | "91.80% harmonic mean (HM) at 10 dB SNR … over 12 percentage points … 95,842 parameters … approximately 42x faster than CREPE on CPU". | supported |
| c26 | Shi 2024 | Table: PS-SQA utterance SRCC 0.639, system 0.888. | supported |

**Net:** 26 exist, 0 fabricated, 25 findings supported as written after full-text retrieval, 1 finding (2) corrected and one number dropped. No MISATTRIBUTED. The unparsed 16 are library docs, specs, npm registry pages and vendor documentation; the lane agents opened each one, and the readouts convention treats those as out-of-band retrieval-verified (same as waves 1–2).

## Not retrievable (CANNOT_CONFIRM — surfaced in the dispatch, not load-bearing)

Liu & Heer 2018 (colormap accuracy); Schörkhuber & Klapuri 2010 and Brown & Puckette 1992 (CQT kernels); Sing&See efficacy studies; an MCD-vs-MOS coefficient; SuperFlux's per-dataset table; the pytorch/audio #1058 resolution recipe; the ESC-50 figure above.

## Gate decision

No blocking verdict. Architectural lock L1–L8 may proceed to the Director. L8 (the in-repo render A/B) is the uncertainty gate before L2/L3 are frozen.

To re-verify this receipt without the signing secret: `prism replay prism-01m1z0rr8h868h51eswe428b38` → `prism verify-receipt --public-key <pub.pem>`.
