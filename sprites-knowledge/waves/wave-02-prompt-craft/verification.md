# Wave 2 — Verification receipt

**Method:** Three study swarms (encoder mechanics · negative prompts · seed-vs-prompt). Each research lane was followed by a separate adversarial retrieval-verifier (different lens, researcher reasoning hidden) that WebFetched the cited papers/docs and returned a per-finding verdict: CONFIRMED / CORRECTED / FOLKLORE / UNVERIFIABLE. The domain is a known folklore minefield, so the verifier was instructed to be hard on round-number token claims, "magic words," mega-negative-block efficacy, negative-embedding transfer, and "magic seed" claims, defaulting to FOLKLORE/UNVERIFIABLE without a real source.

## Result
- **103 findings → 103 recipes; 102 verified (1 unverifiable lead).**
- **195 sources**, retrieval-checked.
- **6 debunked myths** retained as `kind=anti-pattern / status=avoid` (so the myth is queryable): T5 `(word:1.4)` weighting, "more detail/emotion always better," quality-tag stacking (x2), masterpiece/best-quality on non-anime bases, and the cross-lane folklore list.
- Grounding mix: ~empirical-paper dominant on the load-bearing claims (CFG, attention, reporting-bias, DDPM/LDM, Long-CLIP, "All Seeds Are Not Equal"), official-docs for pipeline token limits, strong-community for dialect/workflow practice.

## Notable verifier actions
- **Sharpened**, not just confirmed: the CLIP geometric ceiling (cannot do even *two* of {binding, spatial, negation} at once, stronger than originally stated); the "two effects of CFG" framing corrected to *one* extrapolation knob.
- **Stale-citation flags (honest):** the diffusers `weighted_prompts` page was rewritten and no longer states the negative occupies the unconditional branch — the *claim* is independently corroborated (aiphotogenerator), only the HF citation is stale; and the front-loading A1111 discussion #2905 thread is about emphasis, not token order — re-source to a positional guide. The underlying mechanics (Ho & Salimans 2022, Long-CLIP) are valid.
- **Mechanism-level confirmations** against primary papers: CFG linear extrapolation (Ho & Salimans 2022); high-w std inflation → over-exposure + the RescaleCFG fix (Lin et al. 2023); reverse process from Gaussian noise (DDPM 2020) in latent space (LDM 2022); seed→composition bias (All Seeds Are Not Equal 2024).

## Caveat
evidence_strength here is research-level (reproduced-from-source / community-claim), NOT on-rig-measured. These are *mechanism + craft* rules grounded in papers/docs; the studio should still spot-check a rule on the rig before treating it as gospel (e.g., the Chroma comma-vs-period style claim is strong-community, worth one A/B). "Verified" means the source resolves and the mechanism is accurately stated, not that we re-ran the experiment.
