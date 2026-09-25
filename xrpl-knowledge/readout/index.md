# readouts — xrpl-knowledge

> Verified knowledge base of the XRP Ledger ECOSYSTEM for a builder — protocol features, transaction types, XLS standards, client libraries & tooling — each tagged with its current mainnet / amendment status. Whole-ecosystem: XRPL mainnet + Xahau/Hooks + the XRPL EVM sidechain + the institutional layer (RLUSD, compliance).
>
> **457 capabilities · 362 verified · 880 sources · 10 waves · generated 2026-09-25.**  
> Decisive axis: network_status — is this feature ACTUALLY enabled on XRPL mainnet right now (vs amendment-pending / devnet-only / deprecated), and which standard/library is current — plus which of the four build-focus tracks (game economies / NFT assets / payments / identity-compliance) it serves.

## Domains

| Domain | Capabilities | Verified | Top pick | License | Readout |
|---|--:|--:|---|---|---|
| Protocol & consensus | 48 | 22/48 | Account & owner reserves | — | [`readout-protocol-consensus.html`](readout-protocol-consensus.html) |
| Transactions & accounts | 20 | 18/20 | Account Sequence & Fee Model | — | [`readout-transactions.html`](readout-transactions.html) |
| Tokens & issued assets | 37 | 34/37 | Authorized Trust Lines (RequireAuth) | — | [`readout-tokens.html`](readout-tokens.html) |
| Stablecoins & institutional | 21 | 19/21 | RLUSD (Ripple USD) on XRPL | — | [`readout-stablecoins-institutional.html`](readout-stablecoins-institutional.html) |
| DEX & AMM | 29 | 24/29 | AMM (XLS-30 Automated Market Maker) | — | [`readout-dex-amm.html`](readout-dex-amm.html) |
| NFTs | 57 | 50/57 | Arweave permanent storage (service) | — | [`readout-nfts.html`](readout-nfts.html) |
| Programmability — Hooks (Xahau) | 45 | 35/45 | Emitted transactions (autonomous on-ledger actions) | — | [`readout-programmability-hooks.html`](readout-programmability-hooks.html) |
| Programmability — XRPL EVM sidechain | 54 | 40/54 | EVM mainnet network parameters (chain ID & RPC) | — | [`readout-programmability-evm.html`](readout-programmability-evm.html) |
| Advanced payments | 56 | 51/56 | Cross-currency payments & pathfinding | — | [`readout-payments-advanced.html`](readout-payments-advanced.html) |
| Identity & compliance | 51 | 38/51 | CredentialCreate / CredentialAccept / CredentialDelete | — | [`readout-identity-compliance.html`](readout-identity-compliance.html) |
| Client libraries & SDKs | 11 | 10/11 | Faucet / test-network helpers (fundWallet) | — | [`readout-client-libraries.html`](readout-client-libraries.html) |
| Infrastructure & tooling | 28 | 21/28 | Bithomp (explorer + Explorer-as-a-Service) | — | [`readout-infrastructure-tooling.html`](readout-infrastructure-tooling.html) |

## Install-first shortlist (recommended, by KB download priority)

1. **Account & owner reserves** (Protocol & consensus) — —
2. **Account Sequence & Fee Model** (Transactions & accounts) — —
3. **AccountSet Flags** (Transactions & accounts) — —
4. **Amendment process (2/3 supermajority, 2-week activation)** (Protocol & consensus) — —
5. **AMM (XLS-30 Automated Market Maker)** (DEX & AMM) — —
6. **AMM <> CLOB Integration (auto-routing)** (DEX & AMM) — —
7. **AMM Fix Amendments (fixAMMv1_1/v1_2/v1_3/OverflowOffer)** (DEX & AMM) — —
8. **AMM-vs-CLOB choice for a game economy (architecture pattern)** (DEX & AMM) — —
9. **AMMCreate** (DEX & AMM) — —
10. **AMMCreate (stand up the canonical game-token pool)** (DEX & AMM) — —
11. **AMMDeposit (single & double asset)** (DEX & AMM) — —
12. **AMMDeposit single-asset (bootstrap/deepen treasury liquidity)** (DEX & AMM) — —
13. **AMMVote — set/govern the swap fee as studio revenue** (DEX & AMM) — —
14. **AMMWithdraw** (DEX & AMM) — —
15. **Arweave permanent storage (service)** (NFTs) — —
16. **At-scale minting throughput — Tickets & sequence pipelining** (NFTs) — —
17. **Authorized minter (asfAuthorizedNFTokenMinter)** (NFTs) — —
18. **Authorized Minter Delegation** (NFTs) — —

## Go deeper

- **Per-domain readout:** `readout-<slug>.html` — filterable table + sources + verify trail
- **Wave dispatches** (research log): `waves.md` / `waves.html`
- **Verification receipt** (trust trail): `verification.md` / `verification.html`
- **Query the DB:** `xrpl.db (views v_recommended, v_best_for; FTS capabilities_fts)`
- **Resolve via loadout:** `ai-loadout resolve --project ./xrpl-knowledge`
- **Programmatic map:** `index.json`

## Provenance

Every fact carries a **wave id** and a **verified** flag; sources are retrieval-checked by a different-family verifier. 10 waves; 362/457 capabilities verified.
