# Build-focus: Payments & micropayments
_The XRPL capabilities you assemble for **payments & micropayments** — across every feature domain._ · wave 10 · 2026-09-07 · [‹ catalog index](README.md)

230 capabilities (92 depth-curated) · 210 mainnet-live · 211 cross-family verified.

## Curated — the building blocks
_From the focused depth wave for this folder, ranked by builder fitness._

| Capability | Feature domain | Kind | Network | Fit | ✓ |
|------------|----------------|------|---------|-----|---|
| [Account abstraction (ERC-4337) for gasless player UX](programmability-evm.md) | Programmability — XRPL EVM sidechain | pattern | ● live | 5 | ✓ |
| [Anyone-can-finish & owner-reserve mechanics of escrow](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [Atomic cross-currency swap via OfferCreate (Fill-or-Kill)](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Auto-route marketplace fees / tax / burn on transfer via a Hook](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 5 | ✓ |
| [Checks (CheckCreate / CheckCash / CheckCancel) — deferred pull payments](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [Conditional escrow via PREIMAGE-SHA-256 crypto-condition](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [Credential-based deposit preauthorization](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | · |
| [Cross-currency Payment (send A, deliver B atomically)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [DepositAuth account flag (block unsolicited deposits)](identity-compliance.md) | Identity & compliance | concept | ● live | 5 | ✓ |
| [DepositPreauth — address allow-list](identity-compliance.md) | Identity & compliance | transaction | ● live | 5 | ✓ |
| [Destination tags & InvoiceID for custodial sub-account crediting](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Destination tags for custodial player sub-accounts](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [Direct token Payment with trustline (player <-> game value transfer)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [Emitted transactions — emit() / etxn_reserve / burden & generation](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 5 | ✓ |
| [Hook API conventions & primitives (hook_account / otxn_* / return codes)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [Hook accept/rollback as a pre-transaction economy gate](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [Hook-enforced escrow, vesting and rate-limited release](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 5 | ✓ |
| [Hooks execution model (Layer-1 WASM transaction interceptor)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [Idempotent retry on transaction results (tem/tef/ter/tec)](transactions.md) | Transactions & accounts | pattern | ● live | 5 | ✓ |
| [Idempotent submission: sequence + LastLedgerSequence + persisted hash](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [KYC/AML-gated economy via Credentials + DepositPreauth + Permissioned Domains](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | ✓ |
| [Loop guards — _g() / GUARD macro (bounded-execution requirement)](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 5 | ✓ |
| [Micropayment tipping & streaming via payment channels (XRP-only)](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Native-vs-EVM currency decision: IOU/MPT vs ERC-20](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [Off-ledger signed Claim (the micropayment unit)](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [On-chain enforcement vs custodial backend: the compliance split decision](identity-compliance.md) | Identity & compliance | concept | · n/a | 5 | ✓ |
| [Open-ledger fee escalation & transaction queue](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [Parallel payout via Ticket pool](transactions.md) | Transactions & accounts | pattern | ● live | 5 | ✓ |
| [Partial-payment-safe crediting (delivered_amount / DeliverMax)](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [Pathfinding (ripple_path_find / path_find)](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [PaymentChannelClaim (redeem or close)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [PaymentChannelCreate](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [PaymentChannelFund (extend funds & Expiration)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [Player cash-in / cash-out (on-ramp / off-ramp) pattern](stablecoins-institutional.md) | Stablecoins & institutional | pattern | ● live | 5 | ✓ |
| [Quality limits & slippage control (tfLimitQuality)](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [RLUSD as in-game store of value / premium-currency backing](stablecoins-institutional.md) | Stablecoins & institutional | concept | ● live | 5 | ✓ |
| [Real-time inflow detection: subscribe streams vs account_tx polling](payments-advanced.md) | Advanced payments | service | ● live | 5 | ✓ |
| [Reconciliation via transaction metadata (AffectedNodes + result codes)](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Regulated reward payouts to verified players only](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | · |
| [RequireDest — force destination tags](identity-compliance.md) | Identity & compliance | concept | ● live | 5 | ✓ |
| [Reward-distribution architecture: per-tx vs batched](transactions.md) | Transactions & accounts | pattern | ● live | 5 | ✓ |
| [Sanction and recall handling: freeze-then-clawback workflow](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | ✓ |
| [Sequence vs Ticket submission management](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [SetHook transaction (definitions, install/update/delete)](programmability-hooks.md) | Programmability — Hooks (Xahau) | transaction | ● live | 5 | ✓ |
| [SettleDelay & closure / cancel mechanics](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [Settling player payouts in RLUSD over XRPL](stablecoins-institutional.md) | Stablecoins & institutional | pattern | ● live | 5 | ✓ |
| [Single-treasury payout in player-preferred currency](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Stablecoin-pegged / stablecoin-backed in-game currency](stablecoins-institutional.md) | Stablecoins & institutional | pattern | ● live | 5 | ✓ |
| [Tickets (out-of-order sequence reservation)](transactions.md) | Transactions & accounts | transaction | ● live | 5 | ✓ |
| [Time-based escrow (FinishAfter / CancelAfter)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [TokenEscrow — escrow of IOUs and MPTs (XLS-85)](payments-advanced.md) | Advanced payments | standard | ● live | 5 | ✓ |
| [Treasury hardening recipe (KYC-gated deposits)](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | · |
| [Vesting / lockup schedule via escrow ladder](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Watchtower / claim-redemption pattern](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [channel_authorize (sign a claim)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [channel_verify (verify a claim signature)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [delivered_amount (DeliverMax) — authoritative credited amount](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [delivered_amount safety rule (never trust Amount on a backend)](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [tfPartialPayment & the partial-payment exploit](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [Amount -> DeliverMax rename (rippled API v2)](payments-advanced.md) | Advanced payments | concept | ● live | 4 | ✓ |
| [Auto-bridging through XRP](payments-advanced.md) | Advanced payments | concept | ● live | 4 | ✓ |
| [Batch transaction (XLS-56)](transactions.md) | Transactions & accounts | transaction | ◐ pending | 4 | ✓ |
| [Channel reserve & XRP-only economics](payments-advanced.md) | Advanced payments | concept | ● live | 4 | ✓ |
| [Conditional quest reward (crypto-condition escrow)](payments-advanced.md) | Advanced payments | pattern | ● live | 4 | ✓ |
| [Cross-chain game economy via Axelar Interchain Token Service](programmability-evm.md) | Programmability — XRPL EVM sidechain | service | ● live | 4 | ✓ |
| [DeliverMin (floor on a partial delivery)](payments-advanced.md) | Advanced payments | transaction | ● live | 4 | ✓ |
| [Deposit Authorization gate (DepositAuth + credential-based XLS-70)](payments-advanced.md) | Advanced payments | concept | ● live | 4 | · |
| [DisallowIncoming flags (spam shield)](identity-compliance.md) | Identity & compliance | concept | ● live | 4 | ✓ |
| [ERC-20 in-game currency contract on the sidechain](programmability-evm.md) | Programmability — XRPL EVM sidechain | standard | ● live | 4 | ✓ |
| [Escrow as marketplace / trade settlement (counterparty-risk-free)](payments-advanced.md) | Advanced payments | pattern | ● live | 4 | ✓ |
| [Escrow-secured player-to-player trade (token escrow)](payments-advanced.md) | Advanced payments | pattern | ● live | 4 | ✓ |
| [Hook State (key-value store, namespaces, foreign reads)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [Hook chaining (up to 10 hooks per account)](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 4 | ✓ |
| [Hook-emitted reward distribution (autonomous payouts)](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 4 | ✓ |
| [HookOn bitmap (active-low transaction-type trigger mask)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [Hooks vs EVM sidechain vs native objects — choosing the game-logic layer](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [MPT allow-listing for compliant game currencies](identity-compliance.md) | Identity & compliance | pattern | ● live | 4 | · |
| [Marketplace fee routing to studio treasury](payments-advanced.md) | Advanced payments | pattern | ● live | 4 | ✓ |
| [Owner reserve accounting for payment objects (Checks/Escrows/Channels/Preauth)](payments-advanced.md) | Advanced payments | concept | ● live | 4 | ✓ |
| [Permissioned DEX for compliant secondary markets](identity-compliance.md) | Identity & compliance | pattern | ● live | 4 | · |
| [RequireAuth — authorized trust lines](identity-compliance.md) | Identity & compliance | concept | ● live | 4 | ✓ |
| [Shared allowlist / blocklist registries via foreign state + HookGrants](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 4 | ✓ |
| [Transactional stakeholders — strong vs weak execution](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [What Hooks CANNOT do — the deliberate non-Turing-complete envelope](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [Batch reward distribution / mass payout (Batch — NOT on mainnet)](payments-advanced.md) | Advanced payments | transaction | ● live | 3 | · |
| [DeFi composability for game economies (Band price oracle, AMMs)](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 3 | ✓ |
| [Deferred / installment payout via time-locked escrow (XRP & token)](payments-advanced.md) | Advanced payments | pattern | ● live | 3 | ✓ |
| [Hook fees & resource limits (deterministic up-front pricing)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 3 | ✓ |
| [Time / rate limiting actions by ledger sequence](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 3 | ✓ |
| [fixTokenEscrowV1 — MPT transfer-fee accounting fix](payments-advanced.md) | Advanced payments | concept | ● live | 3 | ✓ |
| [Multi-chain RLUSD liquidity & XRPL EVM bridging](stablecoins-institutional.md) | Stablecoins & institutional | concept | ● live | 2 | ✓ |
| [fixBatchInnerSigs amendment](transactions.md) | Transactions & accounts | standard | ● live | 1 | ✓ |

## Broader — also relevant
_Tagged by the foundation wave (wide net). Curation happens in this folder's depth wave._

| Capability | Feature domain | Kind | Network | Fit | ✓ |
|------------|----------------|------|---------|-----|---|
| [AMM (XLS-30 Automated Market Maker)](dex-amm.md) | DEX & AMM | amendment | ● live | 5 | ✓ |
| [AMM <> CLOB Integration (auto-routing)](dex-amm.md) | DEX & AMM | pattern | ● live | 5 | ✓ |
| [AMMDeposit (single & double asset)](dex-amm.md) | DEX & AMM | transaction | ● live | 5 | ✓ |
| [AMMWithdraw](dex-amm.md) | DEX & AMM | transaction | ● live | 5 | ✓ |
| [Account & owner reserves](protocol-consensus.md) | Protocol & consensus | concept | ● live | 5 | ✓ |
| [Account Sequence & Fee Model](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [AccountSet Flags](transactions.md) | Transactions & accounts | transaction | ● live | 5 | ✓ |
| [Amendment process (2/3 supermajority, 2-week activation)](protocol-consensus.md) | Protocol & consensus | concept | ● live | 5 | ✓ |
| [Axelar bridge (XRPL ⇄ EVM sidechain)](programmability-evm.md) | Programmability — XRPL EVM sidechain | service | ● live | 5 | ✓ |
| [Clio (read-optimized API server)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 5 | ✓ |
| [Clio API server (history & read scaling)](protocol-consensus.md) | Protocol & consensus | service | ● live | 5 | ✓ |
| [Credentials (on-chain attestations)](identity-compliance.md) | Identity & compliance | amendment | ● live | 5 | · |
| [Cross-currency payments & pathfinding](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Crypto-conditions (PREIMAGE-SHA-256)](payments-advanced.md) | Advanced payments | standard | ● live | 5 | ✓ |
| [Deposit Authorization (DepositAuth flag)](identity-compliance.md) | Identity & compliance | concept | ● live | 5 | ✓ |
| [DepositPreauth (account + credential preauthorization)](identity-compliance.md) | Identity & compliance | transaction | ● live | 5 | · |
| [Destination tags & source tags](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [EVM mainnet network parameters (chain ID & RPC)](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [Emitted transactions (autonomous on-ledger actions)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [Escrow (XRP) — time-based & conditional](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [Faucet / test-network helpers (fundWallet)](client-libraries.md) | Client libraries & SDKs | service | · n/a | 5 | ✓ |
| [GemWallet (browser-extension XRPL wallet)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 5 | ✓ |
| [Hardhat deployment toolchain](programmability-evm.md) | Programmability — XRPL EVM sidechain | library | ● live | 5 | ✓ |
| [Hook API (C primitives / function categories)](programmability-hooks.md) | Programmability — Hooks (Xahau) | library | ● live | 5 | ✓ |
| [Hook developer tooling (Hooks Builder, SDKs, testnet)](programmability-hooks.md) | Programmability — Hooks (Xahau) | service | ● live | 5 | ✓ |
| [Hooks (WASM smart-contract layer)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [IOU vs MPT — Decision Guide](tokens.md) | Tokens & issued assets | pattern | ● live | 5 | ✓ |
| [Issued Currencies (IOUs) & Trust Lines](tokens.md) | Tokens & issued assets | concept | ● live | 5 | ✓ |
| [Ledger structure & ledger objects](protocol-consensus.md) | Protocol & consensus | concept | ● live | 5 | ✓ |
| [MPTokenAuthorize (Hold / Authorize an MPT)](tokens.md) | Tokens & issued assets | transaction | ● live | 5 | ✓ |
| [MPTokenIssuanceCreate (Issue an MPT)](tokens.md) | Tokens & issued assets | transaction | ● live | 5 | ✓ |
| [Multi-Purpose Tokens (MPTokensV1)](protocol-consensus.md) | Protocol & consensus | amendment | ● live | 5 | ✓ |
| [Multi-Purpose Tokens (MPTs)](stablecoins-institutional.md) | Stablecoins & institutional | standard | ● live | 5 | ✓ |
| [Multi-Purpose Tokens (MPTs)](tokens.md) | Tokens & issued assets | standard | ● live | 5 | ✓ |
| [Multisigning (SignerListSet)](transactions.md) | Transactions & accounts | transaction | ● live | 5 | ✓ |
| [NFTokenAcceptOffer (Direct + Brokered)](nfts.md) | NFTs | transaction | ● live | 5 | ✓ |
| [OfferCreate (native order-book DEX)](dex-amm.md) | DEX & AMM | transaction | ● live | 5 | ✓ |
| [Pathfinding & Cross-Currency Payments (Flow engine)](dex-amm.md) | DEX & AMM | concept | ● live | 5 | ✓ |
| [Payment Channels (PaymentChannelCreate / Fund / Claim)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [Payment transaction (direct & cross-currency)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [Permissioned Domains](identity-compliance.md) | Identity & compliance | amendment | ● live | 5 | · |
| [Public RPC node providers (QuickNode, GetBlock, public clusters)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 5 | ✓ |
| [RLUSD (Ripple USD) on XRPL](stablecoins-institutional.md) | Stablecoins & institutional | service | ● live | 5 | ✓ |
| [Reliable Transaction Submission Lifecycle (autofill -> sign -> submit -> verify)](transactions.md) | Transactions & accounts | pattern | ● live | 5 | ✓ |
| [Rippling, NoRipple & Default Ripple](tokens.md) | Tokens & issued assets | concept | ● live | 5 | ✓ |
| [SetHook transaction](programmability-hooks.md) | Programmability — Hooks (Xahau) | transaction | ● live | 5 | ✓ |
| [SetRegularKey (Regular Key Pair)](transactions.md) | Transactions & accounts | transaction | ● live | 5 | ✓ |
| [Solidity / EVM smart contracts](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [Source & Destination Tags](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [Token Clawback](stablecoins-institutional.md) | Stablecoins & institutional | amendment | ● live | 5 | ✓ |
| [Token Escrow (XLS-85) — IOU & MPT escrow](payments-advanced.md) | Advanced payments | amendment | ● live | 5 | ✓ |
| [Transaction Common Fields](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [Transaction Results & Metadata (tes / tec / tef / tem / tel / ter)](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [Transaction cost & fee escalation](protocol-consensus.md) | Protocol & consensus | concept | ● live | 5 | ✓ |
| [Transfer Fees / Royalties](nfts.md) | NFTs | concept | ● live | 5 | ✓ |
| [TrustSet Transaction](tokens.md) | Tokens & issued assets | transaction | ● live | 5 | ✓ |
| [When to use EVM sidechain vs native XRPL vs Xahau](programmability-evm.md) | Programmability — XRPL EVM sidechain | pattern | ● live | 5 | ✓ |
| [XLS-47 Native Price Oracles](infrastructure-tooling.md) | Infrastructure & tooling | amendment | ● live | 5 | ✓ |
| [XRP Ledger Consensus Protocol (XRP LCP)](protocol-consensus.md) | Protocol & consensus | concept | ● live | 5 | ✓ |
| [XRP as native gas token](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [XRP native asset](protocol-consensus.md) | Protocol & consensus | concept | ● live | 5 | ✓ |
| [XRPL Client SDKs (xrpl.js / xrpl-py / xrpl4j / xrpl-go)](infrastructure-tooling.md) | Infrastructure & tooling | standard | ● live | 5 | ✓ |
| [XRPL Dev Networks (Testnet / Devnet / specialty devnets)](infrastructure-tooling.md) | Infrastructure & tooling | concept | ○ devnet | 5 | ✓ |
| [XRPL EVM Sidechain (standalone Cosmos L1)](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [XRPL Wallet & seed handling (Wallet class)](client-libraries.md) | Client libraries & SDKs | concept | · n/a | 5 | ✓ |
| [XRPL stablecoin issuer pattern (trust-line issued currency)](stablecoins-institutional.md) | Stablecoins & institutional | pattern | ● live | 5 | ✓ |
| [XRPSCAN (explorer + analytics API)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 5 | ✓ |
| [Xahau vs XRPL mainnet (when to choose Xahau)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [Xaman (formerly XUMM) wallet + developer platform](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 5 | ✓ |
| [rippled (core XRPL server)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 5 | ✓ |
| [rippled / xrpld core server (v3.2.0 rebrand)](protocol-consensus.md) | Protocol & consensus | service | ● live | 5 | · |
| [tfImmediateOrCancel / tfFillOrKill / tfSell (offer execution flags)](dex-amm.md) | DEX & AMM | pattern | ● live | 5 | ✓ |
| [xrpl-py](client-libraries.md) | Client libraries & SDKs | library | · n/a | 5 | ✓ |
| [xrpl.js](client-libraries.md) | Client libraries & SDKs | library | · n/a | 5 | ✓ |
| [xrpl4j](client-libraries.md) | Client libraries & SDKs | library | · n/a | 5 | ✓ |
| [AMM Clawback](stablecoins-institutional.md) | Stablecoins & institutional | amendment | ● live | 4 | ✓ |
| [AMMBid (continuous auction slot)](dex-amm.md) | DEX & AMM | transaction | ● live | 4 | ✓ |
| [AMMCreate](dex-amm.md) | DEX & AMM | transaction | ● live | 4 | ✓ |
| [AccountDelete](transactions.md) | Transactions & accounts | transaction | ● live | 4 | ✓ |
| [Authorized Trust Lines (RequireAuth)](tokens.md) | Tokens & issued assets | concept | ● live | 4 | ✓ |
| [Auto-Bridging (XRP as bridge currency)](dex-amm.md) | DEX & AMM | concept | ● live | 4 | ✓ |
| [Axelar Interchain Token Service (ITS)](programmability-evm.md) | Programmability — XRPL EVM sidechain | service | ● live | 4 | ✓ |
| [Bithomp (explorer + Explorer-as-a-Service)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 4 | ✓ |
| [Checks (CheckCreate / CheckCash / CheckCancel)](payments-advanced.md) | Advanced payments | transaction | ● live | 4 | ✓ |
| [Clawback (Issued Currencies)](tokens.md) | Tokens & issued assets | amendment | ● live | 4 | ✓ |
| [Compliance freeze controls (Freeze / Deep Freeze / Clawback)](identity-compliance.md) | Identity & compliance | concept | ● live | 4 | ✓ |
| [CronSet (scheduled hook callbacks)](programmability-hooks.md) | Programmability — Hooks (Xahau) | transaction | ◐ pending | 4 | ✓ |
| [Crossmark (browser-extension XRPL wallet)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 4 | ✓ |
| [Deep Freeze](tokens.md) | Tokens & issued assets | amendment | ● live | 4 | ✓ |
| [DisallowIncoming flags](identity-compliance.md) | Identity & compliance | concept | ● live | 4 | · |
| [Foundry deployment toolchain](programmability-evm.md) | Programmability — XRPL EVM sidechain | library | ● live | 4 | ✓ |
| [Guard / weak-guard (_g) and bounded execution](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 4 | ✓ |
| [Hook State (namespaced key-value storage)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [Hook fees & execution metering](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [Invoice ID (InvoiceID field)](payments-advanced.md) | Advanced payments | concept | ● live | 4 | ✓ |
| [LPToken (AMM liquidity-provider token)](dex-amm.md) | DEX & AMM | concept | ● live | 4 | ✓ |
| [Lending Protocol & Single Asset Vaults](protocol-consensus.md) | Protocol & consensus | amendment | ◐ pending | 4 | ✓ |
| [MPT Controls (Lock, RequireAuth, Clawback, Transfer Fee, Metadata)](tokens.md) | Tokens & issued assets | concept | ● live | 4 | ✓ |
| [NFTokenCreateOffer](nfts.md) | NFTs | transaction | ● live | 4 | ✓ |
| [OfferCancel](dex-amm.md) | DEX & AMM | transaction | ● live | 4 | ✓ |
| [Official XRPL Explorer (livenet.xrpl.org)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 4 | ✓ |
| [Partial payments (tfPartialPayment) & delivered_amount](payments-advanced.md) | Advanced payments | concept | ● live | 4 | ✓ |
| [Permissioned DEX](stablecoins-institutional.md) | Stablecoins & institutional | amendment | ● live | 4 | · |
| [Permissioned DEXes](identity-compliance.md) | Identity & compliance | amendment | ● live | 4 | · |
| [Permissioned Domains](protocol-consensus.md) | Protocol & consensus | amendment | ● live | 4 | ✓ |
| [Permissioned Domains](stablecoins-institutional.md) | Stablecoins & institutional | amendment | ● live | 4 | · |
| [Proof-of-Authority / CometBFT consensus](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 4 | ✓ |
| [RLUSD XRPL issuer flag configuration](stablecoins-institutional.md) | Stablecoins & institutional | pattern | ● live | 4 | ✓ |
| [Remix + MetaMask quick path](programmability-evm.md) | Programmability — XRPL EVM sidechain | pattern | ● live | 4 | ✓ |
| [RequireAuth (authorized trust lines)](identity-compliance.md) | Identity & compliance | concept | ● live | 4 | ✓ |
| [Tickets (TicketCreate / TicketSequence)](transactions.md) | Transactions & accounts | transaction | ● live | 4 | ✓ |
| [Token Escrow (IOU & MPT)](tokens.md) | Tokens & issued assets | amendment | ● live | 4 | ✓ |
| [Token Freeze (individual, global, deep freeze)](stablecoins-institutional.md) | Stablecoins & institutional | concept | ● live | 4 | ✓ |
| [Tokenized real-world assets (RWA) on XRPL](stablecoins-institutional.md) | Stablecoins & institutional | pattern | ● live | 4 | ✓ |
| [Transfer Fees (TransferRate)](tokens.md) | Tokens & issued assets | concept | ● live | 4 | ✓ |
| [XRPL EVM Sidechain (RPC + smart contracts)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 4 | ✓ |
| [XRPL EVM sidechain dev stack (ethers / web3 / viem)](client-libraries.md) | Client libraries & SDKs | concept | ● live | 4 | ✓ |
| [ripple-address-codec](client-libraries.md) | Client libraries & SDKs | library | · n/a | 4 | ✓ |
| [ripple-binary-codec](client-libraries.md) | Client libraries & SDKs | library | · n/a | 4 | ✓ |
| [ripple-keypairs](client-libraries.md) | Client libraries & SDKs | library | · n/a | 4 | ✓ |
| [AMM Clawback](tokens.md) | Tokens & issued assets | amendment | ● live | 3 | ✓ |
| [AMM Fix Amendments (fixAMMv1_1/v1_2/v1_3/OverflowOffer)](dex-amm.md) | DEX & AMM | amendment | ● live | 3 | ✓ |
| [AMMClawback](dex-amm.md) | DEX & AMM | amendment | ● live | 3 | ✓ |
| [AMMVote (governable trading fee)](dex-amm.md) | DEX & AMM | transaction | ● live | 3 | ✓ |
| [Account Permission Delegation (DelegateSet / Delegate)](transactions.md) | Transactions & accounts | amendment | ○ devnet | 3 | · |
| [Batch Transactions (XLS-56)](transactions.md) | Transactions & accounts | amendment | ○ devnet | 3 | · |
| [Batch transactions (BatchV1_1 revival)](protocol-consensus.md) | Protocol & consensus | amendment | ◐ pending | 3 | ✓ |
| [Decentralized Identifiers (DID)](identity-compliance.md) | Identity & compliance | amendment | ● live | 3 | ✓ |
| [Hooks (Xahau L1 programmability)](infrastructure-tooling.md) | Infrastructure & tooling | amendment | × deprecated | 3 | ✓ |
| [JS Hooks (JSHooks — JavaScript authoring)](programmability-hooks.md) | Programmability — Hooks (Xahau) | library | ○ devnet | 3 | ✓ |
| [Native Cosmos IBC interoperability](programmability-evm.md) | Programmability — XRPL EVM sidechain | service | ● live | 3 | ✓ |
| [Negative UNL](protocol-consensus.md) | Protocol & consensus | concept | ● live | 3 | ✓ |
| [Permissioned DEX (XLS-81)](dex-amm.md) | DEX & AMM | amendment | ● live | 3 | · |
| [Token Freeze (Individual, Global, NoFreeze)](tokens.md) | Tokens & issued assets | concept | ● live | 3 | ✓ |
| [Xahau / Hooks SDK note (xahau.js)](client-libraries.md) | Client libraries & SDKs | library | ● live | 3 | · |
| [hooks-rs (Rust authoring)](programmability-hooks.md) | Programmability — Hooks (Xahau) | library | ○ devnet | 3 | ✓ |
| [xrpl-secret-numbers](client-libraries.md) | Client libraries & SDKs | library | · n/a | 3 | ✓ |
| [AMMDelete](dex-amm.md) | DEX & AMM | transaction | ● live | 2 | ✓ |

_Each capability's full detail (key fields, gotchas, sources) lives in its feature-domain readout, linked above._

