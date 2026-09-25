# Wave 13 — Register classification from audio: the measured floor

**KB** `vocology-knowledge` · **dispatched** 2026-09-14 · **1** lane · trigger: a correction. An external research pass concluded that audio-only register classification is "contested, highly unreliable" and that a passaggio cannot be gated from audio. That conclusion was reached without the papers that measure it. This wave lands what the measurements actually say.

**Consumer:** `E:/AI/ai-jam-sessions` — the audio inspector's tier-1 deterministic gates. Wave 7 locked f0 in cents and onsets in milliseconds as gate-grade numbers and put the spectrogram picture at tier 3. Register was left open. This wave closes the question of whether register can be a gate at all.

**Headline.** It can. Two 2025 studies classify register from audio alone with no sensor, no EGG and no laryngoscopy, and both report high accuracy: a DE-tuned XGBoost over 14 TSFEL temporal features at 97.60% on 350 files, and an SVM over mel-spectrogram texture at 0.94 on held-out male pop. **The method is not the weak point — the ground truth is.** Both studies label by ear from pedagogy texts, so what is measured is agreement with trained annotators, not laryngeal state. Nothing in the 2024–2026 record validates an audio-only register classifier against EGG. That is the gap, and it is a different gap from the one the external pass named.

---

## Research grounding

1. **A Differential-Evolution-tuned Extreme Gradient Boosting model classified chest, mixed and head registers at 97.60% average accuracy from 14 TSFEL temporal features over 350 audio files.** Boratto et al. 2025 (DOI:10.3390/signals6010009), *Signals* 6(1) art. 9, CC BY 4.0. Implication: the front end is engineered temporal features, not a neural embedding — a deterministic pipeline can carry this. Treat 97.60% as an in-corpus number: 350 internally constructed files, voice type and genre unstated in the abstract.

2. **An SVM over mel-spectrogram texture reached 0.94 test accuracy on a four-class register scheme (0 chest / 1 mix / 2 head mix / 3 head) built from 1008 three-second male-pop lead-vocal clips; labels were assigned by ear from vocal-technique texts, and the authors ship a tool (AVRA).** Kim & Botha 2025 (arXiv:2505.11378v2), CC BY 4.0. Implication: adopt the four-class scheme — splitting mix into mix / head-mix is the load-bearing distinction near the passaggio, and a ternary output is what produces instability at the break. Treat 0.94 as an in-domain ceiling on one genre and one voice type.

3. **The same paper reports 7221 initial images in v2 and 4221 in v1 for the identical 1008 clips.** Kim & Botha 2025 (arXiv:2505.11378, v1 vs v2). Implication: cite the version, not just the identifier. A bare arXiv ID is not a stable reference for a number in this paper.

## What this corrects

The wave-8 entry for Kim & Botha recorded the four-class scheme and the TA–CT framing but carried **no performance number**, which left the question of whether the approach works unanswered in the KB. It is answered here: 0.94 in domain.

## The honest limit

Accuracy in both studies is agreement with human annotators working from pedagogy texts. Register is a pedagogical vocabulary before it is a physiological one, and no located 2024–2026 study measures an audio-only classifier against EGG or laryngoscopy. So a register gate built on this evidence is a gate on *what a trained listener would call it* — defensible for a practice tool, and not a claim about the larynx. Say which one the product is claiming.

## Provenance

Findings 1–3 originated from an external research pass (Gemini, running a patched instruction set that requires a retrieved title, first-author surname and year behind any "opened" claim, and that separates a source's claim from the model's own inference). Every identifier and both headline numbers were then resolved by the advisor against arXiv, Crossref and Semantic Scholar before anything entered this wave. The external pass's own numeric claims — 97.6%, 1008 clips — survived verification exactly; its *conclusion* did not, and is what this wave corrects. Full receipt in [`verification.md`](verification.md).
