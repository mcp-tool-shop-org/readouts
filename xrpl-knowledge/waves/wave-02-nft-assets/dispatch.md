# Wave 2 — NFT game assets (depth)

**Dispatched 2026-06-14 · 5 depth sub-lanes · 45 capabilities · build-focus folder: nft-assets.**

## Scope

The first **depth wave** — it curates the `nft-assets` build-focus folder and deepens the `nfts` feature
domain with net-new capability (Wave 1 covered the basics; this wave goes deeper, it does not re-list them).
Five sub-lanes: minting & collections · marketplaces & royalties · dynamic/mutable NFTs · metadata & storage ·
game-asset patterns & real projects.

## Method

- **Research:** 5 web-grounded agents (direct synchronous dispatch — NOT the Workflow orchestrator, which
  silent-stalled in Wave 1). Each instructed to build net-new depth and to use **discriminating fitness**
  (5 = core building block, 1 = peripheral) — the fix for Wave 1's over-tagging. Result: a real 1–5 fitness
  spread, so the folder curates instead of flattening.
- **Verification:** the cross-family `deepseek-v3.1:671b-cloud` seat (`scripts/verify_cloud.py`),
  refute-by-default. **40/45 confirmed** (39 confirmed · 1 with-fixes · 1 refuted · 4 unverified).

## Results

- **45 capabilities · 95 sources · 40/45 cross-family verified.** The `nfts` feature domain is now 57
  capabilities (12 foundation + 45 depth); the `nft-assets` folder is **45 depth-curated / 114 total**.
- **Settled the Wave-1 open item:** mutable/dynamic NFTs ARE live on XRPL mainnet via the **DynamicNFT
  amendment / XLS-46 (mainnet 2025-06-11)** — `tfMutable` at mint + `NFTokenModify`. So evolving/leveling
  game items (equipment that changes state) are buildable today, not burn-and-remint.
- **Studio-relevant building blocks surfaced:** authorized-minter delegation, collection/set modeling via
  NFTokenTaxon, broker-routed sales (destination-restricted offers), escrowless atomic settlement, eager-vs-lazy
  minting, on-chain metadata schemas for traits/rarity/stats, Arweave/IPFS storage tradeoffs, soulbound items,
  and the load-bearing decision **"fungible consumables & currency belong in MPTs, not NFTs."**

## Folder model (refinement applied this wave)

Build-focus folders are now **two-tiered**: a **Curated** section (capabilities a focused DEPTH wave tagged for
the folder — the building blocks, ranked by fitness) on top, and a **Broader** section (the foundation wave's
wider net) below. Folders are owned by their depth wave; the foundation wave is generous context. This is the
durable fix for Wave 1's indiscriminate folder tagging. game-economies / payments / identity-compliance show
0 curated until their depth waves (3 / 4 / 5) run.

## Provenance

`research-raw.json` (research + `cloud_verify`) is the load source; rows carry `wave_id=2`. Ingested by
`scripts/load_db.py`, rebuilt by `scripts/regen.py`. A robust `network_status` normalizer now runs at ingest
(agents write rich free-text status; it maps to the decisive-axis enum).
