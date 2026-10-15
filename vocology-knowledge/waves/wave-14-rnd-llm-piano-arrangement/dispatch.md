# Wave 14 — Piano arrangements by a model, accepted by machine (promoted from rnd)

**KB** `vocology-knowledge` · **dispatched** 2026-10-13 · **0** research agents (a promotion) · lane `music-as-seconds-grid` · trigger: the readouts promotion queue. The Director approved promoting this topic from the studio's research bench, [rnd](https://github.com/mcp-tool-shop-org/rnd), into vocology-knowledge on 2026-10-13.

**Consumer:** `ai-jam-sessions`, the sung-exemplar runbook. Every sung exemplar needs a piano part under the voice, and the score clock times the voice against it.

**Headline.** A reasoning model can write a hymn's whole piano arrangement as LilyPond code, and the arrangement can be trusted when machine gates accept it. Three gates decide: the file compiles, the melody is in the piano at its written time, and no sung note is left without a piano note under it. Two hymns went through for $1.31 in all, and the Director approved both recordings by ear.

**Where this sits.** Wave 2 found that a model writes music more reliably as code than as tokens or audio prompts (ChatMusician, ABC notation, music21). This wave is the studio's own measurement of that idea, run end to end on two hymns, with the receipts committed.

---

## Research grounding

1. **The gates accept the arrangement, not the model.** Kimi-K3 at temperature 0 and reasoning effort high wrote Amazing Grace and America the Beautiful: an introduction, one pass per stanza with a texture that builds, and a coda. LilyPond 2.24 compiled both with no error or warning, one after a recorded one-line fix. The MIDI import found every verse's melody, and the score clock refused nothing. [ai-jam-sessions PR 109](https://github.com/mcp-tool-shop-org/ai-jam-sessions/pull/109). **Implication:** write the brief's rules so a machine can check them (the melody as the top voice at its written time; no `\partial` after the start; no pedal marks, repeats, tuplets or `\ottava`), and keep each arrangement's brief, prompt, raw answer, compiled file and meta.json.

2. **The brief is generated from the hymn data.** `scripts/arrange-hymn.ts` writes the melody bar by bar with chords per beat, every stanza, the form, a texture plan and the rules. America the Beautiful's brief came from the script, and its answer compiled as returned. Amazing Grace's brief was written by hand before the script existed, and its answer needed the hand fix. **Implication:** generate the brief from the data the score clock reads. One pair each way is a direction, not a rate.

3. **The cost is output, and most of the output is reasoning.**

   | | prompt tokens | completion tokens (reasoning) | cost | wall time |
   |---|---|---|---|---|
   | Amazing Grace | 1,728 | 19,510 (13,023) | $0.298 | 196 s |
   | America the Beautiful | 1,956 | 67,147 (36,692) | $1.013 | 528 s |

   Both calls were served by the provider Modal at $3.00 per million input tokens and $15 per million output tokens. Completion was over 98% of each bill. **Implication:** budget an arrangement as max_tokens × the output price (about $3.00 at 200,000), print the estimate first, and spend only on an explicit yes.

4. **Expect one-line slips.** Two of the studio's three model-written arrangements needed one: `\key g major` without the backslash before the mode (Amazing Grace, twice), and a missing `\language "english"` (the Battle Hymn, by an earlier route). **Implication:** the compile gate catches them, and a recorded fix costs less than a second call.

5. **Rights.** The Kimi K3 License governs the weights, code and documentation and claims nothing in outputs; its display duty (§3) applies only to large commercial products. OpenRouter's Terms take a non-exclusive licence in content. The tunes and texts are public domain (editions of 1919 or earlier, authors dead before 1930), and each brief carries only the hymn's own melody and chords. **Implication:** check all three things for each model and each hymn before dedicating CC0, because terms change. This records what the terms say; it is not legal advice.

## What the promotion corrected

The rnd entry was the bench copy. Re-reading its numbers against the receipts changed two things before they entered this knowledge base:
- **Only one brief was generated.** rnd said both briefs were generated from the score. Amazing Grace's was written by hand, as its meta.json records.
- **The input price was $3.00 per million tokens, not $0.72.** The billed cost of the prompt tokens gives the rate. Input is under a cent per arrangement either way, so the totals stand.

## The honest limit

Two arrangements, one model, one script and one listener. Nothing here compares models, measures how often a generated brief compiles first time, or tests listeners beyond the Director's approval.

## Provenance

Promoted from rnd entry [`2026-10-08-llm-piano-arrangement-from-a-generated-brief`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-08-llm-piano-arrangement-from-a-generated-brief.md). It was re-read against the committed receipts on 2026-10-13. Full receipt in [`verification.md`](verification.md).
