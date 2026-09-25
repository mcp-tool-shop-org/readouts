# Wave 3 — Game token economies (depth)

**Dispatched 2026-06-14 · 5 depth sub-lanes · 51 capabilities · build-focus folder: game-economies.**

## Scope

Depth wave curating the `game-economies` folder. Unlike NFTs (one domain), a game economy spans domains, so
each sub-lane deepened its **home feature domain** while tagging `game-economies`:
- **issuance** + **patterns** → `tokens` (MPT-vs-IOU game currency, supply control, economy-design patterns)
- **markets** → `dex-amm` (AMM pools & CLOB for player currency trading)
- **rails** → `stablecoins-institutional` (RLUSD store-of-value, cash-in/out)
- **flows** → `payments-advanced` (P2P trades, batch payouts, micropayment tipping, conditional rewards)

## Method

Direct synchronous dispatch (no Workflow orchestrator) + discriminating fitness. Authoritative verification by
the cross-family `deepseek-v3.1:671b-cloud` seat (`scripts/verify_cloud.py`), refute-by-default:
**45/51 confirmed** (43 · 2 with-fixes · 6 refuted · 0 unverified).

## Results

- **51 capabilities · 114 sources · 45/51 cross-family verified.** KB now 249 capabilities / 3 waves. The
  `game-economies` folder is **74 depth-curated / 181 total**.
- **Grounded on real mid-2026 amendment dates:** MPTokensV1 (XLS-33) mainnet 2025-10-01 · Clawback 2024-02-08 ·
  DeepFreeze (XLS-77) 2025-05-05 · TokenEscrow (XLS-85) 2026-02-12.
- **Load-bearing gotcha the cross-family seat enforced:** MPT **DEX trading (MPTokensV2 / XLS-82) is NOT live**
  on mainnet as of mid-2026 — the seat refuted markets capabilities that assumed tradeable MPTs. So a *tradeable*
  game currency must be an **IOU** today; MPTs are for non-traded soft/earned currency until XLS-82 ships.
- **Studio building blocks surfaced:** dual-currency mapping (MPT soft-earned / IOU hard-tradeable / XRP
  gas-settlement), AMMCreate for the canonical game-token pool, single-asset AMMDeposit to bootstrap treasury
  liquidity, Clawback/Deep-Freeze as economy-management levers, conditional quest-reward escrow (crypto-conditions),
  destination tags for custodial player sub-accounts, and sink/faucet implementation patterns.

## Provenance

`research-raw.json` (research + `cloud_verify`), rows `wave_id=3`. Ingested by `scripts/load_db.py`, rebuilt by
`scripts/regen.py`. The 6 refuted items stay `verified=0` and surface in the verification receipt.
