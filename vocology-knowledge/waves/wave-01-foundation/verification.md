# Wave 1 — citation verification

**Dispatch:** [`dispatch.md`](dispatch.md)  
**Receipt:** [`citation-receipt.json`](citation-receipt.json) (pass 2)  
**Pass-1 refuse (kept):** [`citation-receipt.pass1-refuse.json`](citation-receipt.pass1-refuse.json)

Protocol: `roleos verify-citations` → `prism verify --type citations --provider ollama` (family-different from the Grok synthesizer, reasoning-stripped, arXiv/Crossref existence oracle + abstract groundedness). Local signing via `PRISM_DEV=1` (no persistent studio key in this session).

## Pass 1 — refuse (blocking)

- Prism receipt `prism-01m1nd9s8y7xhy4nmy4wyfc0dd`
- **0 papers fabricated as papers.** One identifier failed Crossref: `DOI:10.1121/1.2829014` (Titze 2008 theory) flagged `fabricated`.
- That is a **misattribution**, not a fake paper. Live retrieval: Titze 2008 *Nonlinear source–filter coupling in phonation: Theory*, JASA 123:2733, **DOI:10.1121/1.2832337**, PMC2811547. Companion exercises DOI:10.1121/1.2832339.
- Protocol: MISATTRIBUTED may be corrected **once**. Corrected. UniVoice `arXiv:2606.05852` was `unresolvable` on this pass (export API); not read as fabrication.

## Pass 2 — escalate (advisory, non-blocking)

- Prism receipt `prism-01m1ndcs5e3zmbptcj3dfre1tb`
- `citations_sha256` `4b2fe657d2bd807fd90ba4fe1cd9395dbedcff3643cdfdc4cbe6090d3fc7e5ed`
- `chain_sha256` `b5148fed5e248eb6fe51dde3c6641265b0f276c683950bca2b3d3d0dcd4b4321`
- Titze `10.1121/1.2832337`: **resolved + supported + accept**
- UniVoice `arXiv:2606.05852`: **resolved** (retry); groundedness `not_addressed` (PER ablation lives in the body, not the abstract) → left **out of Step 5**
- **0 fabricated. 0 refuse.**

Abstract-supported **accept** (load-bearing without caveat):

| id | source | claim prism grounded |
|---|---|---|
| Sundberg 1974 | 10.1121/1.1914609 | singer's formant from larynx-tube mismatch (≥6× pharynx) |
| Joliveau 2004 | 10.1121/1.1791717 | R1 tracks F0 once F0 exceeds speech R1 |
| Titze 2008 | 10.1121/1.2832337 | instabilities when harmonics pass through formants |
| Prame 1994 | 10.1121/1.410141 | mean vibrato 6.0 Hz; rate rises at endings |
| Klatt 1990 | 10.1121/1.398894 | aspiration noise > H1 as breathiness cue |
| VISinger 2022 | arXiv:2110.08813 | speech-style duration fails; score-locked duration |
| Zhang & Zhu 2021 | arXiv:2106.10045 | English vowel beat near mid-vowel |
| SingMOS-Pro 2026 | arXiv:2510.01812 | lyrics vs melody MOS are separate; speech MOS predictors fail |
| Green 1990 | 10.2307/3345186 | vocal-model identity changes pitch-matching accuracy |

All other parsed citations **exist** (arXiv/Crossref resolved) but the numeric/body claims are `RETRIEVE FULL TEXT` — the same advisory class as the protocol's own v1.1 dispatch. They stay **directional**: existence is gated; the specific numbers (MOS, RMSE, RTF, licenses fetched from HF/GitHub by the lane agents) are not abstract-NLI-supported.

## Contrastive leftovers (you may have expected these to be load-bearing)

- **Finding 16 (UniVoice PER 12.31/23.45 vs 5.26/16.22)** — paper exists; those percentages are not in the abstract prism saw. C8 does **not** cite it. Override if you want the body numbers in the architecture.
- **Fant 1960** — book DOI resolved; no abstract → RETRIEVE FULL TEXT. Lane retrieved publisher preview + Diehl 2008 restatement. Directional only.
- **Spec/PDF-only items** (LF 1985 QPSR PDF, Zhang & Wang 2020 ISCA PDF, RMSSinger ACL URL, ITU-R BS.1534, so-vits-svc GitHub, Li 2025 PMC) — `unparsed` by the arXiv/Crossref extractor. Retrieval-checked out of band by the lane agents; not in the prism table.

## What the gate proved

The gate *discriminated*: it refused a wrong JASA DOI, accepted the correction, and did not rubber-stamp body-only MOS numbers. Architectural connections C1–C8 are allowed to lean on the nine abstract-supported findings; the directional SVS-route table (DiffSinger / ACE-Step / DiffRhythm / YuE licenses and MIDI-lock) is existence-confirmed and license-page-fetched by the lane, not abstract-NLI-confirmed — treat those as **route evidence with a re-fetch before any npm pin**.
