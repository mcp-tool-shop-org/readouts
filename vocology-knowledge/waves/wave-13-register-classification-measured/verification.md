# Wave 13 — citation verification

**Dispatch:** [`dispatch.md`](dispatch.md)
**Runner:** manual retrieval oracle — arXiv (`arxiv.org/abs`, `arxiv.org/html`), Crossref REST (`api.crossref.org/works`), Semantic Scholar Graph API. Run 2026-09-14 by the advisor.
**Verifier maturity — stated plainly:** this wave was verified by a **retrieval oracle only**. No second model family reviewed the groundedness of the findings, so this is weaker than `prism verify` / `roleos verify-citations` (wave 7's path) and weaker than the protocol's family-different requirement. What the oracle can prove — that a paper exists, with these authors, this year, and these sentences in it — is proven. What it cannot prove is that the finding text is the most faithful reading of the paper.

## Result

| bucket | count | citations |
|---|---|---|
| existence resolved | **2 / 2** | DOI:10.3390/signals6010009 · arXiv:2505.11378 |
| fabricated | **0** | — |
| confirmed on full text | **2** | both findings, every headline number located verbatim |
| unresolved | 0 | — |

## Per-source

**DOI:10.3390/signals6010009 — Boratto et al. 2025.** Crossref returns the exact title, eight authors led by Boratto Tales, *Signals* 6(1) article 9, issued 2025-02-21, license `creativecommons.org/licenses/by/4.0/`. The Crossref abstract truncates mid-sentence at "…the Extreme Gradient Boosting model, optimized with DE, achieved"; Semantic Scholar's copy of the same abstract completes it: "an average classification accuracy of 97.60%". The 350-file corpus, the TSFEL library and the 14 temporal features are stated verbatim in the abstract. MDPI's own article page was unreachable from this rig (empty response), so every claim here rests on Crossref + Semantic Scholar rather than the publisher page.

**arXiv:2505.11378 — Kim & Botha 2025.** The abs page returns the exact title, authors Kim, Alexander and Botha, Charlotte, dated 2025-05-16, licence CC BY 4.0. The abstract supports SVM + CNN over "textural features of mel-spectrogram images" verbatim but names no class list and no accuracy, so both were settled on the HTML full text: §3.1 gives "A total of 1008 audio clips were rendered into mel-spectrograms which produced 7221 initial images before splitting and augmentation", the class indices 0 chest / 1 mix / 2 head mix / 3 head, the 80/20 split, the flip-plus-brightness augmentation, SVM test accuracy 0.94 with per-class metrics 0.91–0.99, six CNN epochs and 68.0% validation accuracy after epoch one. Labels trace to Peckham 2010 via the paper's own citation.

## Version discrepancy (recorded, not resolved)

v1 and v2 of 2505.11378 state **different image counts for the same 1008 clips** — 4221 in v1, 7221 in v2. Both were retrieved and read this session. The wave cites v2 and records the discrepancy; which is correct was not determined, and the authors do not flag the change.

## Note on provenance

Both findings entered as unverified output from an external model (Gemini). Its numeric claims — 97.6%, 1008 clips, the SVM/CNN pair, the four-class split — all survived retrieval verification exactly. Its *conclusion* (that audio-only register classification is unreliable and cannot gate a passaggio) did not survive and is corrected by this wave. This is the intended shape: an external pass generates candidate findings, the retrieval oracle admits them, and the synthesising conclusion is never inherited.

**Net:** 2 exist, 0 fabricated, 2 confirmed on full text, 1 version discrepancy recorded, 0 corrections needed to the numbers as supplied.
