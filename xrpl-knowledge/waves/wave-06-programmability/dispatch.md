# Wave 6 — Programmability: Hooks + EVM (depth)

**Dispatched 2026-06-14 · 5 depth sub-lanes · 52 capabilities · feature domains: programmability-hooks, programmability-evm.**

## Scope

A depth wave on the two **programmability feature domains** (not a build-focus folder) — on-chain game logic.
Sub-lanes: Hooks fundamentals & API (Xahau) · Hooks patterns for games · EVM sidechain fundamentals & tooling ·
EVM bridge & interoperability · EVM contracts for games. Capabilities tag the build-focus tracks where a hook
or contract genuinely serves one (e.g. fee-routing hook → game-economies).

## Method

Direct synchronous dispatch + discriminating fitness; authoritative cross-family verification by
`deepseek-v3.1:671b-cloud` (`scripts/verify_cloud.py`). **51/52 confirmed** (47 · 4 with-fixes · 0 refuted ·
1 unverified) — the highest confirmation rate of any wave; Hooks went 23/23.

## Results

- **52 capabilities · 51/52 cross-family verified.** KB now **382 capabilities / 6 waves**. Domains:
  programmability-hooks 35 · programmability-evm 41.
- **Two distinct programmable surfaces, clearly separated by `chain`:**
  - **Hooks (Xahau, chain=xahau):** the Hooks API (otxn_*, state, the `_g()` guard), SetHook, WASM/C toolchain,
    resource limits, and game patterns — on-chain fee routing to treasury, conditional transfers, anti-cheat
    invariants, hook-based allowlists/vesting. Lightweight, ledger-native logic; NOT full smart contracts.
  - **XRPL EVM sidechain (chain=xrpl-evm-sidechain):** Solidity/EVM contracts, chain ID 1440000, XRP as gas,
    Hardhat/Foundry/MetaMask tooling, the Axelar bridge (XRP/token/NFT movement + GMP cross-chain calls), and
    ERC-20/721/1155 for game assets.
- **Load-bearing decision captured:** native-XRPL vs Hooks vs EVM-contract per asset/logic type — XLS-20 NFT vs
  ERC-721, MPT/IOU vs ERC-20, ledger-native cost/finality vs EVM composability/DeFi.

## Provenance & tooling fix

`research-raw.json` (research + `cloud_verify`), rows `wave_id=6`. This wave surfaced free-text `chain` values
(like `network_status` earlier), so `load_db.py` gained a `norm_chain()` normalizer (xrpl-mainnet | xahau |
xrpl-evm-sidechain | all | off-ledger) and all 6 waves were re-ingested to clean the axis.
