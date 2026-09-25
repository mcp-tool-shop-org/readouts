# Infrastructure & tooling
_rippled, Clio, public nodes & data APIs, explorers, wallets, price oracles (XLS-47), indexers, dev networks._ · wave 10 · 2026-09-07 · [‹ catalog index](README.md)

28 capabilities · 12 mainnet-live · 21 cross-family verified.

| ↓ | Capability | Kind | Network | Chain | XLS | Fit | Use | ✓ |
|---|------------|------|---------|-------|-----|-----|-----|---|
| 1 | Bithomp (explorer + Explorer-as-a-Service) | service | ● live | xrpl-mainnet |  | 4 | recommended | ✓ |
| 1 | Clio (read-optimized API server) | service | ● live | xrpl-mainnet |  | 5 | recommended | ✓ |
| 1 | Configure amendment voting | docs | · n/a | off-ledger |  | 3 | recommended | ✓ |
| 1 | Crossmark (browser-extension XRPL wallet) | service | ● live | xrpl-mainnet |  | 4 | recommended | ✓ |
| 1 | GemWallet (browser-extension XRPL wallet) | service | ● live | xrpl-mainnet |  | 4 | recommended | ✓ |
| 1 | Official XRPL Explorer (livenet.xrpl.org) | service | ● live | all |  | 3 | recommended | ✓ |
| 1 | Public RPC node providers (QuickNode, GetBlock, public clusters) | service | ● live | xrpl-evm-sidechain |  | 4 | recommended | ✓ |
| 1 | rippled (core XRPL server) | service | ● live | xrpl-mainnet |  | 5 | recommended | ✓ |
| 1 | rippled admin feature method | docs | · n/a | off-ledger |  | 3 | recommended | ✓ |
| 1 | Xaman (formerly XUMM) wallet + developer platform | service | ● live | xahau |  | 5 | recommended | ✓ |
| 1 | XLS-47 Native Price Oracles | amendment | ● live | xrpl-mainnet | XLS-47 | 4 | recommended | ✓ |
| 1 | XRPL Client SDKs (xrpl.js / xrpl-py / xrpl4j / xrpl-go) | standard | ● live | all |  | 5 | recommended | ✓ |
| 1 | XRPL Dev Networks (Testnet / Devnet / specialty devnets) | concept | ○ devnet | xahau |  | 5 | recommended | ✓ |
| 1 | XRPL Ledger Entry: Amendments | docs | · n/a | off-ledger |  | 3 | recommended | ✓ |
| 1 | XRPSCAN (explorer + analytics API) | service | ● live | xrpl-mainnet |  | 4 | recommended | ✓ |
| 2 | XRPL EVM Sidechain (RPC + smart contracts) | service | ● live | xrpl-evm-sidechain |  | 4 | recommended | ✓ |
| 4 | Bitcoin Speedy Trial soft-fork activation | analog | · n/a | off-ledger |  | 3 | situational | ✓ |
| 4 | Chrome Origin Trials | analog | · n/a | off-ledger |  | 3 | situational | ✓ |
| 4 | Kubernetes Feature Gates | analog | · n/a | off-ledger |  | 3 | situational | ✓ |
| 4 | Semantic Versioning (SemVer) | analog | · n/a | off-ledger |  | 3 | situational | ✓ |
| 5 | Cross-chain CCI Survey — Cosmos IBC Hub-and-Zone | concept | · n/a | off-ledger |  | 3 | situational | · |
| 5 | Parallel Networks (Hooks V3 Testnet ≠ Mainnet Hooks) | doc | ○ devnet | xrpl-mainnet |  | 3 | situational | · |
| 5 | Parallel Networks Mainnet/Testnet/Devnet (process) | concept | · n/a | xrpl-mainnet |  | 3 | situational | · |
| 5 | SoK Cross-chain Bridges — lock-and-mint / OP / Axelar | concept | · n/a | off-ledger |  | 3 | situational | · |
| 5 | WebAssembly (portable sandboxed VM ≠ EVM opcodes hold) | analog | · n/a | off-ledger |  | 3 | situational | · |
| 7 | Hooks (Xahau L1 programmability) | amendment | × deprecated | xahau |  | 2 | situational | ✓ |
| 13 | Finch percentage / feature-flag analogy (fail-transfer) | analog | · n/a | off-ledger |  | 3 | avoid | · |
| 13 | LaunchDarkly feature flags (fail-transfer) | analog | · n/a | off-ledger |  | 3 | avoid | · |

## Detail

### Bithomp (explorer + Explorer-as-a-Service) · `service` · ● live ✓
Bithomp is a long-standing XRPL explorer with broad coverage (accounts, transactions, tokens, NFTs) plus known-address lookups and statistics. It offers API services and an Explorer-as-a-Service (EaaS) — a fully hosted, fully managed block-explorer solution you can deploy for your own chain/sidechain. It also runs a Testnet explorer + faucet (test.bithomp.com) that dispenses test XRP and RLUSD, making it useful across dev and prod.
- **Chain:** xrpl-mainnet · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["account / tx / token / NFT views", "known-address (username) registry", "API services for stats and analytics", "Explorer-as-a-Service (hosted/managed)", "Testnet explorer + faucet (test XRP & RLUSD)"]
- **Gotchas:** ["Some richer data and API access sit behind paid tiers / API keys — check pricing before designing around it.", "Known-address usernames are user-claimed labels, not identity proof.", "Use test.bithomp.com for testnet; the main domain is Mainnet-oriented.", "Verify the canonical domain (bithomp.com) — clones and phishing exist in the XRPL space."]
- **Build-focus tracks:** [identity-compliance](track-identity-compliance.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | Bithomp provides mainnet explorer services and EaaS offerings with testnet support via test.bithomp.com.
- **Sources:** [Bithomp — XRP Explorer](https://bithomp.com/) — Bithomp is an XRPL explorer covering transactions, accounts, and NFTs with known-address lookups and statistics. ; [Bithomp Explorer-as-a-Service (EaaS)](https://bithomp.com/en/eaas) — Bithomp offers a fully hosted, fully managed block-explorer solution with API services for analytics and statistics.

### Clio (read-optimized API server) · `service` · ● live ✓
Clio is the XRPLF API server purpose-built for reads: it ingests validated ledger/transaction data from designated rippled nodes and stores it in Cassandra/ScyllaDB using up to 4x less space than rippled, enabling scalable read throughput and HA clusters that share one dataset. It exposes the full rippled API but defaults to validated data; requests needing the P2P network (fee, submit, current ledger) are auto-forwarded to a backing rippled. Pair Clio with rippled for any data-heavy app instead of hammering a rippled node with account_tx/book_offers queries.
- **Chain:** xrpl-mainnet · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["Cassandra/ScyllaDB backend", "ledger_index defaults to validated (not current)", "auto-forwarding of submit/fee to rippled", "shared dataset across multiple Clio nodes", "requires >=1 backing rippled node", "WS + JSON-RPC interface"]
- **Gotchas:** ["Clio defaults ledger_index to 'validated' — add ledger_index:'current' to read pending/non-validated state.", "Clio cannot submit transactions itself; it forwards to a rippled node which must be reachable.", "Backfilling full history into Cassandra/Scylla is operationally heavy; budget storage and ingestion time.", "Clio only has data from the point its backing rippled started supplying it — it is not magically full-history unless fed full-history."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [identity-compliance](track-identity-compliance.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | Clio is a validated read-optimized server that is production-ready and widely used on mainnet.
- **Sources:** [The Clio Server — xrpl.org](https://xrpl.org/docs/concepts/networks-and-servers/the-clio-server) — Clio offers the full rippled API, defaults to validated data, and auto-forwards fee/submit to a rippled node. ; [XRPLF/clio — An XRP Ledger API Server](https://github.com/XRPLF/clio) — Clio stores validated historical ledger/transaction data ~4x more space-efficiently than rippled and can use Cassandra/ScyllaDB for scalable reads.

### Configure amendment voting · `docs` · · n/a ✓
Operator docs for amendment voting config; amendment-pending stays unverified for Batch/PermissionDelegation.
- **Chain:** off-ledger · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** STUDY-010 Verifier-pass; network_status n/a (do not invent-enabled)
- **Gotchas:** Do not flip Batch/PermissionDelegation (915/916). Amendment-pending stays unverified.
- **Verify:** cross-family(study-010-verifier-pass)=confirmed | net-check: n/a (STUDY-020) | currency=2026-09 | STUDY-010 Verifier retrieval-pass. No mainnet. No funds.
- **Sources:** [Configure amendment voting](https://xrpl.org/docs/infrastructure/configuration/configure-amendment-voting) — Operator docs for amendment voting config; amendment-pending stays unverified for Batch/PermissionDelegation.

### Crossmark (browser-extension XRPL wallet) · `service` · ● live ✓
Crossmark is a browser-extension XRPL wallet supporting most major browsers, with an SDK that lets applications integrate signing directly. It has many existing integrations (e.g. XRP Cafe, the XRPL NFT marketplace) and is one of the three commonly supported browser/dApp wallets (with GemWallet and Xaman) in XRPL wallet-connect stacks. A solid second browser-wallet option to support for broad user coverage.
- **Chain:** xrpl-mainnet · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["browser extension (multi-browser)", "Crossmark SDK for app integration", "dApp signing API", "existing integrations (XRP Cafe, marketplaces)", "Mainnet + Testnet support"]
- **Gotchas:** ["Each browser wallet (Crossmark/Gem/Xaman) exposes a different connect/sign API — abstract them behind one connector layer rather than coding to Crossmark only.", "Extension-based; no mobile-native flow.", "Verify the official extension listing to avoid clones."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | Crossmark is a functional browser extension wallet for XRPL Mainnet and Testnet.
- **Sources:** [XRPL Wallets — Crossmark overview](https://medium.com/@LachlanTodd/xrpl-wallets-b253bdc7d818) — Crossmark is a browser-based XRPL wallet supporting most major browsers with app-build integrations such as XRP Cafe. ; [xrpl-wallet-connect (Xaman/Gem/Crossmark template)](https://github.com/Aaditya-T/xrpl-wallet-connect) — Crossmark is supported alongside Xaman and GemWallet in standard XRPL dApp wallet-connect integrations.

### GemWallet (browser-extension XRPL wallet) · `service` · ● live ✓
GemWallet (released Nov 2022 as the first browser-based XRPL wallet) is an open-source, decentralization-focused extension that brings a Web3-style experience to the XRPL: users sign transactions while browsing dApps via an injected provider API. It is a common default for browser dApp signing alongside Crossmark. Open-source code makes it auditable and a good reference for extension integration.
- **Chain:** xrpl-mainnet · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["browser extension (Chrome/Firefox)", "injected provider API for dApps", "open-source codebase", "transaction signing while browsing", "Mainnet + Testnet support"]
- **Gotchas:** ["CRITICAL: scam 'GemWallet airdrop' / 'free XRP' sites actively impersonate it — only install from the official site/extension store and verify the open-source repo; never enter a seed into an 'airdrop' page.", "Extension-only UX; no native mobile app flow like Xaman.", "Confirm the dApp connector API surface (it differs from Crossmark and Xaman) before building a multi-wallet connect layer."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | GemWallet is a browser extension wallet that supports XRPL Mainnet and Testnet operations.
- **Sources:** [XRPL Wallets — GemWallet overview](https://medium.com/@LachlanTodd/xrpl-wallets-b253bdc7d818) — GemWallet, released Nov 2022, was the first browser-based XRPL wallet, is open-source, and provides a Web3-style transaction-signing experience. ; [xrpl-wallet-connect (Xaman/Gem/Crossmark template)](https://github.com/Aaditya-T/xrpl-wallet-connect) — GemWallet is one of the standard XRPL wallets supported in dApp wallet-connect integrations alongside Xaman and Crossmark.

### Official XRPL Explorer (livenet.xrpl.org) · `service` · ● live ✓
The open-source XRP Ledger Explorer (source at github.com/ripple/explorer, hosted at livenet.xrpl.org with testnet.xrpl.org / devnet.xrpl.org variants) is the canonical, neutral explorer for browsing ledgers, transactions, accounts, validators, and network/amendment status. Being open source, it doubles as a deployable explorer for your own network and as the reference for amendment voting and validator UNL visibility. Cleaner and less feature-rich than XRPSCAN/Bithomp, but the trust anchor.
- **Chain:** all · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["livenet.xrpl.org (Mainnet)", "testnet.xrpl.org / devnet.xrpl.org", "validators + UNL view", "amendment voting status", "ledger/account/tx browse", "open-source (self-deployable)"]
- **Gotchas:** ["No public REST analytics API like XRPSCAN — it is a UI/explorer, not a data-API product.", "Pick the correct subdomain per network (livenet vs testnet vs devnet) or you will read the wrong chain.", "Fewer token/NFT/AMM conveniences than third-party explorers."]
- **Build-focus tracks:** [identity-compliance](track-identity-compliance.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | livenet.xrpl.org is the official XRPL mainnet explorer with support for all XRPL networks.
- **Sources:** [XRPL Explorer — livenet.xrpl.org](https://livenet.xrpl.org/) — livenet.xrpl.org is the official XRP Ledger explorer for ledgers, transactions, accounts, and validators. ; [ripple/explorer — Open Source XRP Ledger Explorer](https://github.com/ripple/explorer) — The XRPL block explorer hosted at livenet.xrpl.org is open source and self-deployable.

### Public RPC node providers (QuickNode, GetBlock, public clusters) · `service` · ● live ✓
Managed providers give immediate XRPL Mainnet/Testnet (and XRPL EVM) endpoints without running infrastructure. QuickNode offers managed XRPL and XRPL-EVM endpoints (Ripple Custody itself relies on QuickNode for institutional clients); GetBlock and ~24 other providers (per comparenodes) offer XRP Ledger RPC with latency/uptime stats. Free community clusters (xrplcluster.com, honeycluster.io) provide full-history Clio access for light use. Use a paid provider or self-host for production; treat Ripple's s1/s2 as dev-only.
- **Chain:** xrpl-evm-sidechain · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["WS (wss://) + JSON-RPC (https://) endpoints", "xrplcluster.com / honeycluster.io full-history Clio", "Ripple s1 (general) / s2 (full-history)", "QuickNode managed XRPL + EVM endpoints", "rate limits / SLA tiers", "auth tokens for paid plans"]
- **Gotchas:** ["Ripple's public servers are explicitly NOT for sustained/business use and may disappear at any time — never ship production on s1/s2.", "Free clusters can rate-limit or go down without notice; have a fallback endpoint and retry logic.", "Verify a provider actually serves the API method you need (some only expose a subset, or only validated data via Clio).", "Provider endpoints differ between XRPL Mainnet and XRPL EVM (Ethereum JSON-RPC) — do not mix them."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [identity-compliance](track-identity-compliance.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | Multiple public RPC providers offer XRPL Mainnet access, including QuickNode and xrplcluster.com.
- **Sources:** [Public Servers — xrpl.org](https://xrpl.org/docs/tutorials/public-servers) — Lists Mainnet/Testnet/Devnet endpoints (s1/s2, xrplcluster.com, honeycluster Clio) and warns Ripple's public servers are not for sustained or business use. ; [XRP Ledger & QuickNode — QuickNode blog](https://blog.quicknode.com/xrp-ledger-xrpl-blockchain-quicknode/) — QuickNode provides managed XRPL Mainnet/Testnet and XRPL EVM endpoints; Ripple Custody relies on QuickNode for institutional clients. ; [24 XRP Ledger RPC Providers (comparenodes)](https://www.comparenodes.com/protocols/xrp-ledger/) — Around 24 providers offer XRP Ledger RPC nodes/APIs with latency, uptime, and pricing comparisons in 2026.

### rippled (core XRPL server) · `service` · ● live ✓
rippled is the reference C++ server that forms the XRPL peer-to-peer network: it processes transactions, participates in consensus, and can run as a tracking/full node or as a validator. The current line is 3.x (3.0.0 resolved data-processing issues around tokens, escrow, and price). Running your own rippled is the trust-minimized path for transaction submission and fee/server-state queries, and is required if you want to validate. Full-history requires substantial disk; most teams run a tracking node with limited history and pair it with Clio for reads.
- **Chain:** xrpl-mainnet · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["rippled.cfg config", "node_size", "ledger_history (full vs N)", "admin vs public ports (51234 RPC / 6006 WS / 51235 peer)", "validator_keys / validation seed", "amendment voting", "online_delete + advisory_delete for pruning"]
- **Gotchas:** ["Full-history nodes need terabytes of fast SSD and aggressive online_delete tuning; do not assume a default node keeps history.", "Validators must keep keys offline (validator-keys-tool) and use a separate exposed node — never validate directly on a public-facing box.", "Operators must upgrade promptly when a new major (e.g. 3.0.0) ships or risk amendment-blocked / desync.", "submit and fee require P2P reachability — a read-only Clio cannot replace it.", "Public Ripple servers (s1/s2) are rate-limited and not for production."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [identity-compliance](track-identity-compliance.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | rippled is the official XRPL server implementation and has been mainnet-live since the network's inception.
- **Sources:** [Networks and Servers — xrpl.org](https://xrpl.org/docs/concepts/networks-and-servers) — rippled runs the peer-to-peer network that processes transactions and reaches consensus on their outcome. ; [XRPLF/rippled — GitHub](https://github.com/XRPLF/rippled) — rippled is the official C++ reference implementation of the XRP Ledger server. ; [XRPL Version 3.0.0 release coverage](https://www.comparenodes.com/protocols/xrp-ledger/) — XRPL 3.0.0 resolves data-processing issues related to tokens, escrow, and price, and node operators must update promptly.

### rippled admin feature method · `docs` · · n/a ✓
Admin feature API shows amendment support/majority
- **Chain:** off-ledger · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** STUDY-010 Verifier-pass; network_status n/a (do not invent-enabled)
- **Gotchas:** Do not flip Batch/PermissionDelegation (915/916). Amendment-pending stays unverified.
- **Verify:** cross-family(study-010-verifier-pass)=confirmed | net-check: n/a (STUDY-020) | currency=2026-09 | STUDY-010 Verifier retrieval-pass. No mainnet. No funds.
- **Sources:** [rippled admin feature method](https://xrpl.org/docs/references/http-websocket-apis/admin-api-methods/status-and-debugging-methods/feature) — Admin feature API shows amendment support/majority

### Xaman (formerly XUMM) wallet + developer platform · `service` · ● live ✓
Xaman (the rebrand of XUMM, by XRPL Labs) is the mobile-first self-custody wallet with the deepest native XRPL/Xahau feature coverage — trustlines, DEX, NFTs, AMM, and Hooks (on Xahau). For builders it is also a platform: the Xaman SDK/API, xApps (in-wallet apps), and sign-requests via deep links / QR let any dApp request user signatures and 'Sign in with Xaman' without handling keys. Tangem NFC hardware cards extend it to cold storage. The default integration target for XRPL apps that need real user wallets.
- **Chain:** xahau · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["Xaman SDK / API (payload-based sign requests)", "xApps (in-wallet web apps)", "deep links + QR signing", "Sign-in with Xaman", "Tangem NFC hardware cards", "trustline/DEX/NFT/AMM support", "Hooks support on Xahau"]
- **Gotchas:** ["Backend signing flow is payload/webhook-based via the Xaman API — design for async user approval, not a synchronous signer.", "Mobile-first; there is no browser extension, so pure desktop dApp flows rely on QR/deep-link handoff.", "API has key tiers/quotas; register a Xaman app and read current limits.", "Hooks features apply on Xahau, not XRPL Mainnet — don't promise Hooks on Mainnet."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [identity-compliance](track-identity-compliance.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | Xaman is a mainnet-live self-custody wallet supporting both XRPL Mainnet and Xahau networks.
- **Sources:** [Xaman — XRP Wallet](https://xaman.app/) — Xaman is the rebrand of XUMM, a self-custody XRPL/Xahau wallet with an SDK, xApps, deep-link sign requests, and Tangem hardware support. ; [Xaman (XUMM) Wallet Guide 2026](https://www.minexrponline.com/blog/how-to-use-xaman-xumm-wallet) — Xaman natively supports XRPL features including trustlines, DEX trading, NFTs, AMM interactions, and Hooks.

### XLS-47 Native Price Oracles · `amendment` · ● live ✓
XLS-47 (author Gregory Tsipenyuk) added native price oracles to the XRPL via the PriceOracle amendment, LIVE on Mainnet since 2024-11-02. Off-chain providers publish prices on-chain through OracleSet (create/modify) and OracleDelete transactions, stored in a PriceOracle ledger object (up to 10 base/quote pairs each, scaledPrice = price x 10^scale, scale 0-20). Apps read aggregated values via the get_aggregate_price method (mean/median/trimmed-mean across multiple oracles to reduce single-source risk). Band Protocol and DIA are live integrated providers feeding DeFi (AMM, lending) pricing.
- **Chain:** xrpl-mainnet · **XLS:** XLS-47 · **Amendment:** PriceOracle · **Enabled:** 2024-11-02 · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["PriceOracle ledger object", "OracleSet / OracleDelete transactions", "OracleDocumentID", "Provider + AssetClass fields", "PriceDataSeries (base/quote, AssetPrice, Scale)", "get_aggregate_price method (mean/median/trimmed mean)", "LastUpdateTime freshness"]
- **Gotchas:** ["Oracles are only as trustworthy as their providers — always query multiple oracles and use get_aggregate_price with trimming, not a single source.", "Check LastUpdateTime / freshness before trusting a price; stale feeds are a known DeFi attack surface.", "fixPriceOracleOrder (a follow-up bug-fix amendment) was Open for Voting as of mid-2026 — verify its status if asset-pair ordering matters to you.", "Scale handling (10^scale) is easy to get wrong; misreading scale produces order-of-magnitude price errors."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | XLS-47 PriceOracle amendment was enabled on XRPL Mainnet on November 2, 2024, providing native on-chain oracle functionality.
- **Sources:** [XLS-0047 Price Oracles — XRPLF/XRPL-Standards](https://github.com/XRPLF/XRPL-Standards/blob/master/XLS-0047-PriceOracles/README.md) — XLS-47 (author Gregory Tsipenyuk) defines the PriceOracle ledger object, OracleSet/OracleDelete transactions, and get_aggregate_price; status is Final and requires an amendment. ; [Price Oracles — xrpl.org](https://xrpl.org/docs/concepts/decentralized-storage/price-oracles) — Off-chain oracles send data to XRPL oracles which store it on-chain; apps can query multiple oracles to minimize risk. ; [XRPL Oracle pricing amendment goes live (RippleX)](https://www.tradingview.com/news/u_today:d0e82255b094b:0-xrp-ledger-makes-major-leap-for-institutional-grade-defi-as-this-feature-launches/) — The XLS-47 PriceOracle amendment went live on Mainnet on 2024-11-02 with Band Protocol and DIA as integrated providers.

### XRPL Client SDKs (xrpl.js / xrpl-py / xrpl4j / xrpl-go) · `standard` · ● live ✓
Official XRPLF client libraries wrap the rippled/Clio API into language-native conventions for connecting, building/signing transactions, and processing ledger data. xrpl.js (JS/TS, on the 4.x line — e.g. 4.5.0) is the most feature-complete (IOUs, payment paths, DEX, account settings); xrpl-py (Python), xrpl4j (Java, org.xrpl), and xrpl-go (Go) cover other stacks. These are the primary way apps talk to the XRPL and are kept current with new amendments (AMM, NFT, MPT, oracles).
- **Chain:** all · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["xrpl.js 4.x (npm 'xrpl')", "xrpl-py (Python)", "xrpl4j (Java, org.xrpl)", "xrpl-go (Go)", "Client connect to rippled/Clio WS", "tx autofill/sign/submit", "wallet/keypair generation", "amendment-aware tx types"]
- **Gotchas:** ["Pin SDK versions and read release notes — major lines (xrpl.js 3.x to 4.x) carry breaking changes.", "An SDK supporting a transaction type does NOT mean that amendment is enabled on your target network — check amendment status separately.", "There is a community fork (xrpscan/xrpl.js) distinct from the canonical XRPLF/xrpl.js — confirm you are depending on the official package 'xrpl' from XRPLF.", "Signing locally vs via a wallet (Xaman) are different trust models — choose deliberately for production."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [identity-compliance](track-identity-compliance.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | Official XRPL client libraries are maintained and support all XRPL networks including mainnet.
- **Sources:** [Client Libraries — xrpl.org](https://xrpl.org/docs/references/client-libraries) — XRPLF maintains official client libraries (xrpl.js, xrpl-py, xrpl4j, xrpl-go) that wrap the XRPL API in language-native conventions. ; [XRPLF/xrpl.js — releases](https://github.com/XRPLF/xrpl.js/releases) — xrpl.js is on the 4.x line (e.g. 4.5.0) and is the recommended JS/TS library for IOUs, payment paths, DEX, and account settings.

### XRPL Dev Networks (Testnet / Devnet / specialty devnets) · `concept` · ○ devnet ✓
XRPL parallel networks for development: Testnet (mainnet-like, stable feature set), Devnet (previews upcoming amendments), plus specialty networks — Lending-Devnet (XLS-66d lending protocol), WASM-Devnet (XLS-100d smart escrows / WASM programmability), and Xahau-Testnet (Hooks / L1 smart contracts). Faucets dispense up to 100 XRP by default (max 1000/request) via web UI or programmatically (faucet.altnet.rippletest.net, faucet.devnet.rippletest.net). Testnet resets ~every 90 days; Devnet may reset without warning.
- **Chain:** xahau · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["Testnet (s.altnet.rippletest.net) + Clio (clio.altnet)", "Devnet (s.devnet.rippletest.net) + Clio", "Lending-Devnet (XLS-66d)", "WASM-Devnet (XLS-100d Smart Escrows)", "Xahau-Testnet (Hooks)", "faucets: 100 XRP default / 1000 max", "Testnet reset ~90 days; Devnet resets anytime"]
- **Gotchas:** ["Testnet/Devnet balances and accounts are wiped on reset (~90 days Testnet; anytime Devnet) — never store anything you need to keep.", "Devnet may have amendments enabled that are NOT on Mainnet — code that works on Devnet can fail on Mainnet (and vice versa). Always confirm amendment parity.", "Hooks live on Xahau-Testnet, not XRPL Testnet — pick the right network for the feature.", "Use programmatic faucet endpoints (xrpl.js wiki) in CI rather than the web faucet to avoid rate limits."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [identity-compliance](track-identity-compliance.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: testnet-devnet | currency=current | XRPL maintains multiple development networks including Testnet, Devnet, and specialized devnets for testing.
- **Sources:** [XRP Faucets — xrpl.org](https://xrpl.org/resources/dev-tools/xrp-faucets) — Testnet and Devnet faucets dispense up to 100 XRP by default (max 1000 per request), with Testnet resetting roughly every 90 days. ; [Testnet and Devnet Resets Upcoming — xrpl.org](https://xrpl.org/blog/2024/testnet-reset) — XRPL maintains parallel Testnet/Devnet networks plus specialty devnets, with periodic resets of ledgers and balances. ; [Xahau Testnet Faucet (Hooks) — XRPL Labs](https://hooks-testnet-v3.xrpl-labs.com/) — The Xahau Testnet has Hooks (L1 smart contracts) enabled for developer testing.

### XRPL Ledger Entry: Amendments · `docs` · · n/a ✓
On-ledger Amendments object documents enabled/majority amendments; process literacy, not flip of 915/916.
- **Chain:** off-ledger · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** STUDY-010 Verifier-pass; network_status n/a (do not invent-enabled)
- **Gotchas:** Do not flip Batch/PermissionDelegation (915/916). Amendment-pending stays unverified.
- **Verify:** cross-family(study-010-verifier-pass)=confirmed | net-check: n/a (STUDY-020) | currency=2026-09 | STUDY-010 Verifier retrieval-pass. No mainnet. No funds.
- **Sources:** [XRPL Ledger Entry: Amendments](https://xrpl.org/docs/references/protocol/ledger-data/ledger-entry-types/amendments) — On-ledger Amendments object documents enabled/majority amendments; process literacy, not flip of 915/916.

### XRPSCAN (explorer + analytics API) · `service` · ● live ✓
XRPSCAN is a leading XRPL explorer and network-analysis platform covering accounts, transactions, NFTs, AMM pools, validator nodes, network metrics, and the XRP rich list in real time. Beyond the web UI it offers a clean REST API to look up accounts, transactions, ledgers, and NFTs, and runs an indexing pipeline that stores XRPL transactions in a distributed search/analytics engine for aggregation and trend discovery. Strong choice for dashboards, address labeling, and programmatic deep search.
- **Chain:** xrpl-mainnet · **Maturity:** stable · **Use:** recommended
- **Key fields / API:** ["REST API (docs.xrpscan.com)", "account / tx / ledger / NFT endpoints", "AMM pool + validator views", "XRP rich list", "well-known address labels", "analytics/aggregation indexing"]
- **Gotchas:** ["Mainnet-focused — confirm testnet/devnet coverage before relying on it for non-mainnet work.", "API rate limits apply; cache and respect terms for heavy ingestion.", "Address labels are curated heuristics, not ground truth — verify before using for compliance decisions.", "Beware impersonation/clone sites; the canonical domain is xrpscan.com and repos live under github.com/xrpscan."]
- **Build-focus tracks:** [identity-compliance](track-identity-compliance.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | XRPSCAN is a fully functional mainnet explorer with real-time analytics and API services.
- **Sources:** [XRPSCAN — XRP Ledger Explorer](https://xrpscan.com/) — XRPSCAN covers accounts, transactions, NFTs, AMM pools, validator nodes, network metrics, and the XRP rich list, updated in real time. ; [Build with XRPSCAN — API docs](https://docs.xrpscan.com/) — XRPSCAN provides a REST-based API to look up accounts, transactions, ledgers, and NFTs on the XRP Ledger.

### XRPL EVM Sidechain (RPC + smart contracts) · `service` · ● live ✓
The XRPL EVM Sidechain (Ripple + Peersyst + Axelar, on a Cosmos/Evmos stack) went LIVE on Mainnet 2025-06-30, bringing full Ethereum-compatible smart contracts to the XRPL world. It exposes a standard Ethereum JSON-RPC interface (Mainnet chainId 1440000, RPC https://rpc.xrplevm.org, explorer https://explorer.xrplevm.org), uses XRP as the gas token, and connects to XRPL Mainnet and 55+ chains via the Axelar bridge. This is the path for Solidity/Hardhat/Foundry/MetaMask tooling and cross-chain DeFi; Testnet is chainId 1449000.
- **Chain:** xrpl-evm-sidechain · **Enabled:** 2025-06-30 · **Maturity:** new · **Use:** recommended
- **Key fields / API:** ["Mainnet chainId 1440000 / RPC https://rpc.xrplevm.org", "Testnet chainId 1449000", "explorer https://explorer.xrplevm.org", "XRP as gas token", "Ethereum JSON-RPC (MetaMask/Hardhat/Foundry)", "Axelar bridge (XRPL + 55+ chains)", "Cosmos/Evmos consensus with 25+ validators"]
- **Gotchas:** ["This is a SEPARATE chain from XRPL Mainnet — XRPL transactions/SDKs (xrpl.js) do NOT work here; use ethers/web3 + EVM tooling.", "Moving value between XRPL Mainnet and XRPL EVM requires the Axelar bridge — bridging adds latency, fees, and a trust assumption.", "Use the correct chainId (1440000 mainnet vs 1449000 testnet); Chainlist entries exist for both.", "It is new (2025) relative to battle-tested XRPL L1 — treat contract/bridge maturity accordingly."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [nft-assets](track-nft-assets.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: mainnet-live | currency=current | XRPL EVM Sidechain launched on mainnet June 30, 2025, with chainId 1440000 and standard Ethereum RPC interface.
- **Sources:** [XRPL EVM Sidechain Mainnet is Live — Ripple](https://ripple.com/insights/xrpl-evm-sidechain-mainnet-is-live/) — The XRPL EVM Sidechain launched on Mainnet on 2025-06-30 with XRP as gas and an Axelar bridge, built by Ripple, Peersyst, and Axelar. ; [XRPL EVM — official site/docs](https://www.xrplevm.org/) — XRPL EVM exposes a standard Ethereum JSON-RPC interface and is live on Mainnet. ; [Chainlist — XRPL EVM (1440000 / 1449000)](https://chainlist.org/chain/1449000) — XRPL EVM Mainnet chainId is 1440000 (RPC https://rpc.xrplevm.org) and Testnet chainId is 1449000.

### Bitcoin Speedy Trial soft-fork activation · `analog` · · n/a ✓
Adjacent: time-bounded signaling for soft-fork activation — analog to XRPL amendment majority windows.
- **Chain:** off-ledger · **Maturity:** stable · **Use:** situational
- **Key fields / API:** STUDY-010 Verifier-pass; network_status n/a (do not invent-enabled)
- **Gotchas:** Analog only. No funds.
- **Verify:** cross-family(study-010-verifier-pass)=confirmed | net-check: n/a (STUDY-020) | currency=2026-09 | STUDY-010 Verifier retrieval-pass. No mainnet. No funds.
- **Sources:** [Bitcoin Speedy Trial soft-fork activation](https://github.com/bitcoin/bitcoin/pull/21377) — Adjacent: time-bounded signaling for soft-fork activation — analog to XRPL amendment majority windows.

### Chrome Origin Trials · `analog` · · n/a ✓
Adjacent: time-boxed experimental enablement — analog to XRPL testnet/devnet feature exposure.
- **Chain:** off-ledger · **Maturity:** stable · **Use:** situational
- **Key fields / API:** STUDY-010 Verifier-pass; network_status n/a (do not invent-enabled)
- **Gotchas:** Analog only. No funds.
- **Verify:** cross-family(study-010-verifier-pass)=confirmed | net-check: n/a (STUDY-020) | currency=2026-09 | STUDY-010 Verifier retrieval-pass. No mainnet. No funds.
- **Sources:** [Chrome Origin Trials](https://developer.chrome.com/docs/web-platform/origin-trials) — Adjacent: time-boxed experimental enablement — analog to XRPL testnet/devnet feature exposure.

### Kubernetes Feature Gates · `analog` · · n/a ✓
Adjacent: staged feature enablement with explicit gates — maps to XRPL amendment maturity without inventing enablement.
- **Chain:** off-ledger · **Maturity:** stable · **Use:** situational
- **Key fields / API:** STUDY-010 Verifier-pass; network_status n/a (do not invent-enabled)
- **Gotchas:** Analog only. No funds.
- **Verify:** cross-family(study-010-verifier-pass)=confirmed | net-check: n/a (STUDY-020) | currency=2026-09 | STUDY-010 Verifier retrieval-pass. No mainnet. No funds.
- **Sources:** [Kubernetes Feature Gates](https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/) — Adjacent: staged feature enablement with explicit gates — maps to XRPL amendment maturity without inventing enablement.

### Semantic Versioning (SemVer) · `analog` · · n/a ✓
Adjacent: version-gated compatibility contracts — maps to rippled version / amendment coupling without invent-enabled.
- **Chain:** off-ledger · **Maturity:** stable · **Use:** situational
- **Key fields / API:** STUDY-010 Verifier-pass; network_status n/a (do not invent-enabled)
- **Gotchas:** Analog only. No funds.
- **Verify:** cross-family(study-010-verifier-pass)=confirmed | net-check: n/a (STUDY-020) | currency=2026-09 | STUDY-010 Verifier retrieval-pass. No mainnet. No funds.
- **Sources:** [Semantic Versioning (SemVer)](https://semver.org/) — Adjacent: version-gated compatibility contracts — maps to rippled version / amendment coupling without invent-enabled.

### Cross-chain CCI Survey — Cosmos IBC Hub-and-Zone · `concept` · · n/a
Cosmos IBC Hub-and-Zone; sidechain plane≠Hooks L1. Invent Mainnet Hooks: 0.
- **Chain:** off-ledger · **Maturity:** new · **Use:** situational
- **Key fields / API:** STUDY-057 deepen; invent-enabled: 0; invent Mainnet Hooks: 0; no mainnet; no funds
- **Gotchas:** No mainnet. No funds.
- **Verify:** cross-family seat: pending
- **Sources:** [Cross-chain CCI Survey — Deng et al., 2025 — arXiv:2505.04934](https://arxiv.org/abs/2505.04934) — Cosmos IBC Hub-and-Zone; sidechain plane≠Hooks L1.

### Parallel Networks (Hooks V3 Testnet ≠ Mainnet Hooks) · `doc` · ○ devnet
One XRPL Mainnet; Hooks V3 Testnet separate preview. ≠ Mainnet Hooks. Invent Mainnet Hooks: 0.
- **Chain:** xrpl-mainnet · **Maturity:** new · **Use:** situational
- **Key fields / API:** STUDY-057 deepen; invent-enabled: 0; invent Mainnet Hooks: 0; no mainnet; no funds
- **Gotchas:** No mainnet. No funds.
- **Verify:** cross-family seat: pending
- **Sources:** [Parallel Networks](https://xrpl.org/docs/concepts/networks-and-servers/parallel-networks) — One XRPL Mainnet; Hooks V3 Testnet separate preview. ≠ Mainnet Hooks.

### Parallel Networks Mainnet/Testnet/Devnet (process) · `concept` · · n/a
One production Mainnet; Testnet mirrors; Devnet experimental; Hooks V3 Testnet separate — Altnets ≠ invent Mainnet-live.
- **Chain:** xrpl-mainnet · **Maturity:** new · **Use:** situational
- **Key fields / API:** STUDY-036 Verifier ✅; invent-enabled: 0
- **Gotchas:** No funds.
- **Verify:** cross-family seat: pending
- **Sources:** [Parallel Networks](https://xrpl.org/docs/concepts/networks-and-servers/parallel-networks) — Mainnet/Testnet/Devnet roles; Hooks V3 Testnet separate.

### SoK Cross-chain Bridges — lock-and-mint / OP / Axelar · `concept` · · n/a
Lock-and-mint / OP / Axelar; bridge≠L1 enable. Invent Mainnet Hooks: 0.
- **Chain:** off-ledger · **Maturity:** new · **Use:** situational
- **Key fields / API:** STUDY-057 deepen; invent-enabled: 0; invent Mainnet Hooks: 0; no mainnet; no funds
- **Gotchas:** No mainnet. No funds.
- **Verify:** cross-family seat: pending
- **Sources:** [SoK Cross-chain Bridges — Zhang et al., 2023 — arXiv:2312.12573](https://arxiv.org/abs/2312.12573) — Lock-and-mint / OP / Axelar; bridge≠L1 enable.

### WebAssembly (portable sandboxed VM ≠ EVM opcodes hold) · `analog` · · n/a
Portable sandboxed VM ≠ EVM opcodes. Holds for Hooks WASM lane.
- **Chain:** off-ledger · **Maturity:** new · **Use:** situational
- **Key fields / API:** STUDY-057 deepen; invent-enabled: 0; invent Mainnet Hooks: 0; no mainnet; no funds
- **Gotchas:** No mainnet. No funds.
- **Verify:** cross-family seat: pending
- **Sources:** [WebAssembly](https://webassembly.org/) — Portable sandboxed VM ≠ EVM opcodes. Holds for Hooks WASM lane.

### Hooks (Xahau L1 programmability) · `amendment` · × deprecated ✓
Hooks add lightweight WebAssembly-based 'smart contract' logic that executes on transactions at the protocol layer. They are LIVE on Xahau (an XRPL-core L1 fork) and Xahau-Testnet, but NOT enabled on XRPL Mainnet — the community is gaining confidence before any Mainnet governance vote. For native XRPL programmability the forward path is instead XLS-100d (WASM smart contracts, on WASM-Devnet) and smart escrows. Use Hooks only if you are deliberately targeting Xahau, not XRPL Mainnet. (network_status marked 'deprecated' only in the sense of 'not the Mainnet path' — it remains active on Xahau.)
- **Chain:** xahau · **Amendment:** Hooks · **Maturity:** experimental · **Use:** situational
- **Key fields / API:** ["WASM Hooks on Xahau L1", "Xahau-Testnet for testing", "xrpl-hooks-ide builder", "NOT on XRPL Mainnet", "XLS-101d XRPL Smart Contracts (Draft) as native successor", "XLS-100d WASM Smart Escrows on WASM-Devnet"]
- **Gotchas:** ["Do NOT promise 'XRPL Mainnet smart contracts via Hooks' — Hooks are Xahau-only as of mid-2026.", "Xahau is a separate network with its own token/economics; targeting it is a distinct decision from XRPL Mainnet.", "For native XRPL programmability, track XLS-100d (WASM Devnet) and XLS-101d (Draft) rather than assuming Hooks will land on Mainnet.", "Hooks tooling (xrpl-hooks-ide) is community-maintained and experimental."]
- **Build-focus tracks:** [game-economies](track-game-economies.md), [payments](track-payments.md)
- **Verify:** cross-family(deepseek-v3.1:671b)=confirmed | net-check: xahau-mainnet-live | currency=current | fix: Hooks are live on Xahau mainnet, not deprecated - the claim incorrectly states deprecated status | Hooks are actively used on Xahau mainnet, providing L1 smart contract functionality, contrary to the deprecated claim.
- **Sources:** [Hooks — Xahau Network docs](https://docs.xahau.network/readme-1) — Hooks run directly on Xahau, a Layer-1 XRPL-core fork, providing smart-contract-like functionality. ; [XLS-0101 XRPL Smart Contracts](https://xls.xrpl.org/xls/XLS-0101-smart-contracts.html) — XLS-101d proposes native L1 smart contracts for the XRP Ledger and is in Draft/Proposal status as of 2025-07-28; Hooks remain Xahau-only, not on XRPL Mainnet.

### Finch percentage / feature-flag analogy (fail-transfer) · `analog` · · n/a
Analogist Finch-% rollout analog. Verifier fail-transfer — no XRPL enablement claim.
- **Chain:** off-ledger · **Maturity:** experimental · **Use:** avoid
- **Key fields / API:** STUDY-010 Verifier-pass; network_status n/a (do not invent-enabled)
- **Gotchas:** Verifier fail-transfer. Amendment-pending stays unverified.
- **Verify:** cross-family(study-010-verifier-pass)=fail-transfer | net-check: n/a — fail-transfer; | currency=2026-09 | fix: leave unverified | STUDY-010 Verifier flag: Finch+% / LaunchDarkly fail-transfer.
- **Sources:** [Finch percentage / feature-flag analogy (fail-transfer)](https://developer.chrome.com/docs/web-platform/chrome-variations) — Analogist Finch-% rollout analog. Verifier fail-transfer — no XRPL enablement claim.

### LaunchDarkly feature flags (fail-transfer) · `analog` · · n/a
Analogist LaunchDarkly analog. Verifier fail-transfer.
- **Chain:** off-ledger · **Maturity:** experimental · **Use:** avoid
- **Key fields / API:** STUDY-010 Verifier-pass; network_status n/a (do not invent-enabled)
- **Gotchas:** Verifier fail-transfer. Amendment-pending stays unverified.
- **Verify:** cross-family(study-010-verifier-pass)=fail-transfer | net-check: n/a — fail-transfer; | currency=2026-09 | fix: leave unverified | STUDY-010 Verifier flag: Finch+% / LaunchDarkly fail-transfer.
- **Sources:** [LaunchDarkly feature flags (fail-transfer)](https://launchdarkly.com/docs/home) — Analogist LaunchDarkly analog. Verifier fail-transfer.

