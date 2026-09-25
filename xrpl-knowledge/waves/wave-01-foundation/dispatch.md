# Wave 1 — Foundation: the XRPL ecosystem, with current mainnet/amendment status

**Dispatched 2026-06-14 · 12 feature lanes · whole-ecosystem scope · 153 capabilities.**

## Scope

The foundation wave maps the **whole XRP Ledger ecosystem for a builder** across 12 feature lanes —
protocol-consensus, transactions, tokens, stablecoins-institutional, dex-amm, nfts, programmability-hooks
(Xahau), programmability-evm (XRPL EVM sidechain), payments-advanced, identity-compliance,
client-libraries, infrastructure-tooling — capturing for each capability its **current mainnet/amendment
status** (the decisive axis), its chain, the XLS standard / amendment, key fields, gotchas, and which of the
four **build-focus tracks** (game-economies / nft-assets / payments / identity-compliance) it serves.

## Method

- **Research:** 12 web-grounded agents (one per lane), each instructed that its training is stale and to
  web-verify the current (mid-2026) state against authoritative sources — xrpl.org docs, the XRPLF /
  XRPL-Standards GitHub (XLS specs), rippled & Clio release notes, Xahau / XRPL-EVM docs. Every capability
  carries ≥1 resolvable source with a one-sentence claim.
  - *Operational note:* the wave was first dispatched via the Workflow orchestrator, which silently stalled
    after 2/12 lanes. It was recovered with **direct synchronous agent dispatch** (each agent wrote its lane
    file; assembled via `scripts/assemble_lanes.py`). The direct path cannot silent-stall — it returns within
    the turn — and is the durable recovery pattern when the background orchestrator is unreliable.
- **Verification (EXTERNAL_VERIFIER):** the authoritative `verified` flag is set by a **cross-family** seat —
  `deepseek-v3.1:671b-cloud` (671B, DeepSeek family, via the local Ollama daemon's cloud routing), run
  refute-by-default against a rubric declared separately from the claims (`scripts/verify_cloud.py`). No
  Claude-judges-Claude: same-family judges over-rate via mechanistic self-preference (Panickssery et al. 2024,
  arXiv:2404.13076; cross-family juries mitigate — Verga et al. 2024, arXiv:2404.18796).

## Results

- **153 capabilities · 287 sources · 138/153 cross-family verified** (134 confirmed · 4 confirmed-with-fixes ·
  7 refuted · 8 unverified).
- **Network status:** 135 mainnet-live · 5 testnet/devnet · 3 amendment-pending · 1 deprecated · 9 n/a (libs/tools).

## What the cross-family seat caught (the value of a different family)

The 671B seat refused to rubber-stamp the **newest amendments**, concentrating its 15 non-confirmations where
"is this actually mainnet-enabled?" is genuinely uncertain:

- **Identity & compliance** — only 5/11 confirmed. Credentials (XLS-70), Permissioned Domains (XLS-80),
  DepositPreauth, and Permissioned DEXes were left **unverified/refuted** — the researcher labeled them
  mainnet-live; the cross-family seat would not confirm. **Open item for Wave 5 (identity depth) to settle
  against the live amendment table.**
- **Transactions** (2 refuted) and **NFTs** (2 refuted) — likely overstated status on a recent feature
  (e.g., Batch / Delegation / dynamic-NFT specifics). Re-examine in the depth waves.
- A strong currency catch the research surfaced and the seat confirmed: **Token Escrow (XLS-85 / TokenEscrow
  amendment) went live on mainnet 2026-02-12** (rippled v3.0.0) — escrow now supports IOUs and MPTs
  (issuer opt-in; CancelAfter mandatory). Payment Channels remain XRP-only.

## Known refinement for the depth waves

The four build-focus folders are **populated but broad** this wave — the research agents tagged
`best_for.track` generously (payments touches 138/153 capabilities), and rated almost everything fitness 4–5,
so a fitness gate doesn't discriminate. The folders are fitness-ranked, so the most-relevant capabilities
surface first. **Curation is the job of the depth waves** (Wave 2 game-economies, Wave 3 nft-assets,
Wave 4 payments, Wave 5 identity-compliance), each producing the authoritative ranked membership for its
folder plus deeper per-capability detail (patterns, code, standards).

## Provenance

`research-raw.json` is the verified load source (research + `cloud_verify`). Ingested by `scripts/load_db.py`
(cloud seat authoritative for `verified`), rebuilt by `scripts/regen.py`. Every row carries `wave_id=1`.
