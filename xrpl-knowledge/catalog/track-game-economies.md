# Build-focus: Game token economies
_The XRPL capabilities you assemble for **game token economies** — across every feature domain._ · wave 10 · 2026-09-07 · [‹ catalog index](README.md)

253 capabilities (146 depth-curated) · 227 mainnet-live · 230 cross-family verified.

## Curated — the building blocks
_From the focused depth wave for this folder, ranked by builder fitness._

| Capability | Feature domain | Kind | Network | Fit | ✓ |
|------------|----------------|------|---------|-----|---|
| [AMM-vs-CLOB choice for a game economy (architecture pattern)](dex-amm.md) | DEX & AMM | pattern | ● live | 5 | ✓ |
| [AMMCreate (stand up the canonical game-token pool)](dex-amm.md) | DEX & AMM | transaction | ● live | 5 | ✓ |
| [AMMDeposit single-asset (bootstrap/deepen treasury liquidity)](dex-amm.md) | DEX & AMM | transaction | ● live | 5 | ✓ |
| [Atomic cross-currency swap via OfferCreate (Fill-or-Kill)](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Authorized minter (asfAuthorizedNFTokenMinter)](nfts.md) | NFTs | transaction | ● live | 5 | ✓ |
| [Auto-route marketplace fees / tax / burn on transfer via a Hook](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 5 | ✓ |
| [Axelar bridge (Amplifier integration) for XRPL ↔ EVM](programmability-evm.md) | Programmability — XRPL EVM sidechain | service | ● live | 5 | ✓ |
| [Channel reserve & XRP-only economics](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [Clawback as an economy-recall lever (IOU + MPT)](tokens.md) | Tokens & issued assets | transaction | ● live | 5 | ✓ |
| [Conditional quest reward (crypto-condition escrow)](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Destination tags for custodial player sub-accounts](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [Direct token Payment with trustline (player <-> game value transfer)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [Dual-currency mapping: MPT (soft/earned) vs IOU (hard/tradeable) vs XRP (gas/settlement)](tokens.md) | Tokens & issued assets | pattern | · n/a | 5 | ✓ |
| [Dynamic NFTs — mutable URI (NFTokenModify + tfMutable)](nfts.md) | NFTs | transaction | ● live | 5 | · |
| [DynamicNFT Amendment](nfts.md) | NFTs | amendment | ● live | 5 | ✓ |
| [ERC-1155 multi-token contract for mixed game inventories](programmability-evm.md) | Programmability — XRPL EVM sidechain | standard | ● live | 5 | ✓ |
| [ERC-20 in-game currency contract on the sidechain](programmability-evm.md) | Programmability — XRPL EVM sidechain | standard | ● live | 5 | ✓ |
| [Eager (scripted) vs lazy (mint-on-demand) minting](nfts.md) | NFTs | pattern | ● live | 5 | ✓ |
| [Escrow as marketplace / trade settlement (counterparty-risk-free)](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Escrow-secured player-to-player trade (token escrow)](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Evolving / Leveling Game-Item Pattern (dNFT)](nfts.md) | NFTs | pattern | ● live | 5 | ✓ |
| [Fungible Consumables & Currency as MPTs](nfts.md) | NFTs | service | ● live | 5 | · |
| [Game-item metadata schema (traits, rarity, stats)](nfts.md) | NFTs | pattern | · n/a | 5 | ✓ |
| [General Message Passing (GMP) — cross-chain contract calls](programmability-evm.md) | Programmability — XRPL EVM sidechain | service | ● live | 5 | ✓ |
| [Hook API conventions & primitives (hook_account / otxn_* / return codes)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [Hook accept/rollback as a pre-transaction economy gate](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [Hook-emitted reward distribution (autonomous payouts)](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 5 | ✓ |
| [Hook-enforced escrow, vesting and rate-limited release](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 5 | ✓ |
| [Hooks execution model (Layer-1 WASM transaction interceptor)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [Hooks vs EVM sidechain vs native objects — choosing the game-logic layer](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [IOU trust-line token as uncapped soft currency](tokens.md) | Tokens & issued assets | standard | ● live | 5 | ✓ |
| [Idempotent retry on transaction results (tem/tef/ter/tec)](transactions.md) | Transactions & accounts | pattern | ● live | 5 | ✓ |
| [Interchain Token Service (ITS) — XRP & IOU bridging](programmability-evm.md) | Programmability — XRPL EVM sidechain | service | ● live | 5 | ✓ |
| [KYC/AML-gated economy via Credentials + DepositPreauth + Permissioned Domains](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | ✓ |
| [LPToken as treasury liquidity receipt & yield instrument](dex-amm.md) | DEX & AMM | concept | ● live | 5 | ✓ |
| [Loop guards — _g() / GUARD macro (bounded-execution requirement)](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 5 | ✓ |
| [MPT as fixed-supply hard currency (MaximumAmount cap)](tokens.md) | Tokens & issued assets | pattern | ● live | 5 | ✓ |
| [MPT as soft-currency substrate (MPTokensV1)](tokens.md) | Tokens & issued assets | pattern | ● live | 5 | ✓ |
| [MPTokenIssuanceCreate — issuer config for a game currency](tokens.md) | Tokens & issued assets | transaction | ● live | 5 | ✓ |
| [Marketplace fee routing to studio treasury](payments-advanced.md) | Advanced payments | pattern | ● live | 5 | ✓ |
| [Mint-time flags & TransferFee (royalty) decisions](nfts.md) | NFTs | transaction | ● live | 5 | ✓ |
| [NFT vs MPT vs IOU — Per-Item Asset-Type Decision](nfts.md) | NFTs | concept | ● live | 5 | ✓ |
| [NFTokenBurn — supply & sink mechanics](nfts.md) | NFTs | transaction | ● live | 5 | ✓ |
| [NFTokenModify Transaction](nfts.md) | NFTs | transaction | ● live | 5 | ✓ |
| [NFTokenTaxon collection-identity strategy](nfts.md) | NFTs | pattern | ● live | 5 | ✓ |
| [Native CLOB order book for player-to-player markets (OfferCreate)](dex-amm.md) | DEX & AMM | transaction | ● live | 5 | ✓ |
| [Native XLS-20 ownership + EVM game logic (cross-chain pattern)](programmability-evm.md) | Programmability — XRPL EVM sidechain | pattern | ● live | 5 | ✓ |
| [Native transfer-fee burn as a currency sink (MPT TransferFee & IOU TransferRate)](tokens.md) | Tokens & issued assets | pattern | · n/a | 5 | ✓ |
| [Native-vs-EVM asset decision: XLS-20 NFT vs ERC-721](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [Native-vs-EVM currency decision: IOU/MPT vs ERC-20](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [Off-ledger signed Claim (the micropayment unit)](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [On-chain enforcement vs custodial backend: the compliance split decision](identity-compliance.md) | Identity & compliance | concept | · n/a | 5 | ✓ |
| [On-chain game logic in Solidity: crafting, marketplace, escrow](programmability-evm.md) | Programmability — XRPL EVM sidechain | pattern | ● live | 5 | ✓ |
| [On-chain invariant / anti-cheat checks at the ledger layer](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 5 | ✓ |
| [On-chain vs off-chain split (the load-bearing economy decision)](tokens.md) | Tokens & issued assets | concept | · n/a | 5 | ✓ |
| [Open-ledger fee escalation & transaction queue](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [Owner reserve & cost-per-NFT math (NFTokenPage packing)](nfts.md) | NFTs | concept | ● live | 5 | ✓ |
| [Parallel payout via Ticket pool](transactions.md) | Transactions & accounts | pattern | ● live | 5 | ✓ |
| [Partial-payment-safe crediting (delivered_amount / DeliverMax)](payments-advanced.md) | Advanced payments | concept | ● live | 5 | ✓ |
| [PaymentChannelClaim (redeem or close)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [PaymentChannelCreate](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [Per-holder owner reserve as a multi-currency design budget](tokens.md) | Tokens & issued assets | concept | ● live | 5 | ✓ |
| [Permissioned & hybrid Offers (DomainID on OfferCreate)](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | ✓ |
| [Permissioned DEX / credential-gated order books (XLS-81)](identity-compliance.md) | Identity & compliance | standard | ● live | 5 | ✓ |
| [Permissioned Domains (XLS-80)](identity-compliance.md) | Identity & compliance | standard | ● live | 5 | ✓ |
| [PermissionedDomainSet transaction](identity-compliance.md) | Identity & compliance | transaction | ● live | 5 | ✓ |
| [Player cash-in / cash-out (on-ramp / off-ramp) pattern](stablecoins-institutional.md) | Stablecoins & institutional | pattern | ● live | 5 | ✓ |
| [Price Oracle (XLS-47) for game-token price discovery](dex-amm.md) | DEX & AMM | standard | ● live | 5 | · |
| [Protocol-Enforced Royalties (TransferFee) & Brokered Sales](nfts.md) | NFTs | service | ● live | 5 | ✓ |
| [RLUSD as in-game store of value / premium-currency backing](stablecoins-institutional.md) | Stablecoins & institutional | concept | ● live | 5 | ✓ |
| [Region-locked / regulated game-economy build pattern](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | ✓ |
| [Region-locking and age-gating with credential types](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | ✓ |
| [Regulated reward payouts to verified players only](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | · |
| [Reserve-Cost Blowup Anti-Pattern (NFTokenPage Economics)](nfts.md) | NFTs | concept | ● live | 5 | ✓ |
| [Reward distribution at scale (and the Batch XLS-56 gap)](tokens.md) | Tokens & issued assets | pattern | · n/a | 5 | ✓ |
| [Reward-distribution architecture: per-tx vs batched](transactions.md) | Transactions & accounts | pattern | ● live | 5 | ✓ |
| [Sanction and recall handling: freeze-then-clawback workflow](identity-compliance.md) | Identity & compliance | pattern | ● live | 5 | ✓ |
| [Security & audit considerations for game contracts](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [Sequence vs Ticket submission management](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [SetHook transaction (definitions, install/update/delete)](programmability-hooks.md) | Programmability — Hooks (Xahau) | transaction | ● live | 5 | ✓ |
| [Settling player payouts in RLUSD over XRPL](stablecoins-institutional.md) | Stablecoins & institutional | pattern | ● live | 5 | ✓ |
| [Sink implementation (crafting costs, fee burns, redemption to issuer)](tokens.md) | Tokens & issued assets | pattern | · n/a | 5 | ✓ |
| [Stablecoin-pegged / stablecoin-backed in-game currency](stablecoins-institutional.md) | Stablecoins & institutional | pattern | ● live | 5 | ✓ |
| [Tickets (out-of-order sequence reservation)](transactions.md) | Transactions & accounts | transaction | ● live | 5 | ✓ |
| [Time-based escrow (FinishAfter / CancelAfter)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [TokenEscrow — escrow of IOUs and MPTs (XLS-85)](payments-advanced.md) | Advanced payments | standard | ● live | 5 | ✓ |
| [Two-currency design: premium MPT + earned IOU](tokens.md) | Tokens & issued assets | pattern | ● live | 5 | ✓ |
| [URI-Only Mutability Boundary](nfts.md) | NFTs | concept | ● live | 5 | ✓ |
| [Verifiable randomness for loot/gacha — VRF gap and commit-reveal](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | · |
| [What Hooks CANNOT do — the deliberate non-Turing-complete envelope](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [XRPL EVM Sidechain (execution layer)](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [XRPL Game-NFT Prior Art (CryptoLand, Space Mermaids, Distribution)](nfts.md) | NFTs | concept | ● live | 5 | ✓ |
| [tfMutable Mint Flag](nfts.md) | NFTs | concept | ● live | 5 | ✓ |
| [AMMVote — set/govern the swap fee as studio revenue](dex-amm.md) | DEX & AMM | transaction | ● live | 4 | ✓ |
| [Anti-RMT & compliance levers (clawback, freeze, RequireAuth allow-listing)](tokens.md) | Tokens & issued assets | pattern | · n/a | 4 | ✓ |
| [Anyone-can-finish & owner-reserve mechanics of escrow](payments-advanced.md) | Advanced payments | concept | ● live | 4 | ✓ |
| [At-scale minting throughput — Tickets & sequence pipelining](nfts.md) | NFTs | pattern | ● live | 4 | · |
| [Auto-bridging for cross-currency player trades](dex-amm.md) | DEX & AMM | concept | ● live | 4 | ✓ |
| [Axelar trust & security model (PoS committee, quadratic voting)](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 4 | ✓ |
| [C/WASM toolchain & hook-cleaner (build pipeline)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [Conditional escrow via PREIMAGE-SHA-256 crypto-condition](payments-advanced.md) | Advanced payments | transaction | ● live | 4 | ✓ |
| [Cross-chain game economy via Axelar Interchain Token Service](programmability-evm.md) | Programmability — XRPL EVM sidechain | service | ● live | 4 | ✓ |
| [DeFi composability for game economies (Band price oracle, AMMs)](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 4 | ✓ |
| [Deferred / installment payout via time-locked escrow (XRP & token)](payments-advanced.md) | Advanced payments | pattern | ● live | 4 | ✓ |
| [Deposit-auth + preauth-by-credential gating](identity-compliance.md) | Identity & compliance | pattern | ● live | 4 | ✓ |
| [Dynamic / Mutable-Metadata NFTs (Equipment Leveling)](nfts.md) | NFTs | pattern | ● live | 4 | ✓ |
| [Emitted transactions — emit() / etxn_reserve / burden & generation](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 4 | ✓ |
| [Faucet implementation (quest rewards & drops via issuer Payments)](tokens.md) | Tokens & issued assets | pattern | · n/a | 4 | ✓ |
| [Freeze tiers as sanction levers (Individual / Global / Deep Freeze)](tokens.md) | Tokens & issued assets | concept | ● live | 4 | · |
| [Hook State (key-value store, namespaces, foreign reads)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [Hook chaining (up to 10 hooks per account)](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 4 | ✓ |
| [HookOn bitmap (active-low transaction-type trigger mask)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [Issuer freeze & clawback controls for a real-value currency](stablecoins-institutional.md) | Stablecoins & institutional | standard | ● live | 4 | ✓ |
| [MPT allow-listing for compliant game currencies](identity-compliance.md) | Identity & compliance | pattern | ● live | 4 | · |
| [MPT authorized-holder gating (RequireAuth + MPTokenAuthorize)](tokens.md) | Tokens & issued assets | transaction | ● live | 4 | ✓ |
| [Micropayment tipping & streaming via payment channels (XRP-only)](payments-advanced.md) | Advanced payments | pattern | ● live | 4 | ✓ |
| [Off-Chain Metadata vs On-Chain Mutability (XLS-24d)](nfts.md) | NFTs | concept | ◐ pending | 4 | · |
| [On-chain randomness via deterministic nonce (and why true RNG is impossible)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [PaymentChannelFund (extend funds & Expiration)](payments-advanced.md) | Advanced payments | transaction | ● live | 4 | ✓ |
| [Permissioned DEX for compliant secondary markets](identity-compliance.md) | Identity & compliance | pattern | ● live | 4 | · |
| [Regulatory & compliance reality of paying players real value](stablecoins-institutional.md) | Stablecoins & institutional | concept | ● live | 4 | ✓ |
| [Shared allowlist / blocklist registries via foreign state + HookGrants](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 4 | ✓ |
| [Time / rate limiting actions by ledger sequence](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 4 | ✓ |
| [Treasury management via Token Escrow (XLS-85) for vesting & structured payouts](tokens.md) | Tokens & issued assets | pattern | ● live | 4 | ✓ |
| [Upgradeable game contracts (UUPS proxy, OpenZeppelin 5.x)](programmability-evm.md) | Programmability — XRPL EVM sidechain | pattern | ● live | 4 | ✓ |
| [Vesting / lockup schedule via escrow ladder](payments-advanced.md) | Advanced payments | pattern | ● live | 4 | ✓ |
| [Watchtower / claim-redemption pattern](payments-advanced.md) | Advanced payments | pattern | ● live | 4 | ✓ |
| [callContractWithToken — value + message in one hop](programmability-evm.md) | Programmability — XRPL EVM sidechain | pattern | ● live | 4 | ✓ |
| [AMMBid — auction slot for discounted-fee market making](dex-amm.md) | DEX & AMM | transaction | ● live | 3 | ✓ |
| [Batch reward distribution / mass payout (Batch — NOT on mainnet)](payments-advanced.md) | Advanced payments | transaction | ● live | 3 | · |
| [Batch transaction (XLS-56)](transactions.md) | Transactions & accounts | transaction | ◐ pending | 3 | ✓ |
| [Branded regulated stablecoin issuance via Brale](stablecoins-institutional.md) | Stablecoins & institutional | service | ● live | 3 | ✓ |
| [Hook fees & resource limits (deterministic up-front pricing)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 3 | ✓ |
| [JSHooks — JavaScript Hooks authoring (alpha, mid-2026)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ○ devnet | 3 | ✓ |
| [MPT escrow capability for time-locked currency (CanEscrow / XLS-85)](tokens.md) | Tokens & issued assets | concept | ● live | 3 | · |
| [MPT lock as the MPT-native freeze (CanLock)](tokens.md) | Tokens & issued assets | transaction | ● live | 3 | ✓ |
| [MPT transfer fee vs IOU TransferRate as a currency sink](tokens.md) | Tokens & issued assets | concept | ● live | 3 | ✓ |
| [Marketplace-fee routing to studio treasury](tokens.md) | Tokens & issued assets | pattern | · n/a | 3 | · |
| [Multi-chain RLUSD liquidity & XRPL EVM bridging](stablecoins-institutional.md) | Stablecoins & institutional | concept | ● live | 3 | ✓ |
| [Premium-currency liquidity via the native DEX & AMM (XLS-30)](tokens.md) | Tokens & issued assets | pattern | ● live | 3 | ✓ |
| [Squid router (Axelar-powered transfer UX & routing)](programmability-evm.md) | Programmability — XRPL EVM sidechain | service | ● live | 3 | ✓ |
| [Tokenized real-world reward assets on XRPL](stablecoins-institutional.md) | Stablecoins & institutional | concept | ● live | 3 | ✓ |
| [Burn + Remint Fallback (fixNFTokenRemint)](nfts.md) | NFTs | pattern | ● live | 2 | ✓ |
| [Cross-Game / Interoperable Assets (Cosmetic-Reality Pattern)](nfts.md) | NFTs | concept | ● live | 2 | ✓ |
| [JSHooks (JavaScript/QuickJS hooks) — alpha, testnet-only](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ○ devnet | 2 | ✓ |
| [Permissioned DEX (XLS-81) for regulated game economies](dex-amm.md) | DEX & AMM | amendment | ● live | 2 | · |

## Broader — also relevant
_Tagged by the foundation wave (wide net). Curation happens in this folder's depth wave._

| Capability | Feature domain | Kind | Network | Fit | ✓ |
|------------|----------------|------|---------|-----|---|
| [AMM (XLS-30 Automated Market Maker)](dex-amm.md) | DEX & AMM | amendment | ● live | 5 | ✓ |
| [AMMCreate](dex-amm.md) | DEX & AMM | transaction | ● live | 5 | ✓ |
| [Account & owner reserves](protocol-consensus.md) | Protocol & consensus | concept | ● live | 5 | ✓ |
| [Account Sequence & Fee Model](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [AccountSet Flags](transactions.md) | Transactions & accounts | transaction | ● live | 5 | ✓ |
| [Authorized Minter Delegation](nfts.md) | NFTs | pattern | ● live | 5 | ✓ |
| [Axelar bridge (XRPL ⇄ EVM sidechain)](programmability-evm.md) | Programmability — XRPL EVM sidechain | service | ● live | 5 | ✓ |
| [Batch Minting & NFTokenMintOffer](nfts.md) | NFTs | pattern | ● live | 5 | · |
| [Clio (read-optimized API server)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 5 | ✓ |
| [Clio API server (history & read scaling)](protocol-consensus.md) | Protocol & consensus | service | ● live | 5 | ✓ |
| [Credentials (on-chain attestations)](identity-compliance.md) | Identity & compliance | amendment | ● live | 5 | · |
| [Dynamic / Mutable NFTs (dNFTs)](nfts.md) | NFTs | amendment | ● live | 5 | · |
| [Dynamic NFTs (DynamicNFT / XLS-46)](protocol-consensus.md) | Protocol & consensus | amendment | ● live | 5 | ✓ |
| [EVM mainnet network parameters (chain ID & RPC)](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [Faucet / test-network helpers (fundWallet)](client-libraries.md) | Client libraries & SDKs | service | · n/a | 5 | ✓ |
| [Hardhat deployment toolchain](programmability-evm.md) | Programmability — XRPL EVM sidechain | library | ● live | 5 | ✓ |
| [Hook State (namespaced key-value storage)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [Hooks (WASM smart-contract layer)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [IOU vs MPT — Decision Guide](tokens.md) | Tokens & issued assets | pattern | ● live | 5 | ✓ |
| [Issued Currencies (IOUs) & Trust Lines](tokens.md) | Tokens & issued assets | concept | ● live | 5 | ✓ |
| [Ledger structure & ledger objects](protocol-consensus.md) | Protocol & consensus | concept | ● live | 5 | ✓ |
| [MPTokenIssuanceCreate (Issue an MPT)](tokens.md) | Tokens & issued assets | transaction | ● live | 5 | ✓ |
| [Multi-Purpose Tokens (MPTs)](stablecoins-institutional.md) | Stablecoins & institutional | standard | ● live | 5 | ✓ |
| [Multi-Purpose Tokens (MPTs)](tokens.md) | Tokens & issued assets | standard | ● live | 5 | ✓ |
| [Multisigning (SignerListSet)](transactions.md) | Transactions & accounts | transaction | ● live | 5 | ✓ |
| [NFTokenAcceptOffer (Direct + Brokered)](nfts.md) | NFTs | transaction | ● live | 5 | ✓ |
| [NFTokenBurn](nfts.md) | NFTs | transaction | ● live | 5 | ✓ |
| [NFTokenMint](nfts.md) | NFTs | transaction | ● live | 5 | ✓ |
| [NFTokenPage & Owner Reserve](nfts.md) | NFTs | concept | ● live | 5 | ✓ |
| [OfferCreate (native order-book DEX)](dex-amm.md) | DEX & AMM | transaction | ● live | 5 | ✓ |
| [Payment transaction (direct & cross-currency)](payments-advanced.md) | Advanced payments | transaction | ● live | 5 | ✓ |
| [Permissioned Domains](identity-compliance.md) | Identity & compliance | amendment | ● live | 5 | · |
| [Reliable Transaction Submission Lifecycle (autofill -> sign -> submit -> verify)](transactions.md) | Transactions & accounts | pattern | ● live | 5 | ✓ |
| [SetHook transaction](programmability-hooks.md) | Programmability — Hooks (Xahau) | transaction | ● live | 5 | ✓ |
| [Solidity / EVM smart contracts](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [Tickets (TicketCreate / TicketSequence)](transactions.md) | Transactions & accounts | transaction | ● live | 5 | ✓ |
| [Transaction Common Fields](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [Transaction Results & Metadata (tes / tec / tef / tem / tel / ter)](transactions.md) | Transactions & accounts | concept | ● live | 5 | ✓ |
| [Transaction cost & fee escalation](protocol-consensus.md) | Protocol & consensus | concept | ● live | 5 | ✓ |
| [Transfer Fees / Royalties](nfts.md) | NFTs | concept | ● live | 5 | ✓ |
| [TrustSet Transaction](tokens.md) | Tokens & issued assets | transaction | ● live | 5 | ✓ |
| [When to use EVM sidechain vs native XRPL vs Xahau](programmability-evm.md) | Programmability — XRPL EVM sidechain | pattern | ● live | 5 | ✓ |
| [XLS-20 Native NFTokens](nfts.md) | NFTs | standard | ● live | 5 | ✓ |
| [XRP as native gas token](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [XRP native asset](protocol-consensus.md) | Protocol & consensus | concept | ● live | 5 | ✓ |
| [XRPL Client SDKs (xrpl.js / xrpl-py / xrpl4j / xrpl-go)](infrastructure-tooling.md) | Infrastructure & tooling | standard | ● live | 5 | ✓ |
| [XRPL Dev Networks (Testnet / Devnet / specialty devnets)](infrastructure-tooling.md) | Infrastructure & tooling | concept | ○ devnet | 5 | ✓ |
| [XRPL EVM Sidechain (RPC + smart contracts)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 5 | ✓ |
| [XRPL EVM Sidechain (standalone Cosmos L1)](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 5 | ✓ |
| [XRPL Wallet & seed handling (Wallet class)](client-libraries.md) | Client libraries & SDKs | concept | · n/a | 5 | ✓ |
| [XRPL stablecoin issuer pattern (trust-line issued currency)](stablecoins-institutional.md) | Stablecoins & institutional | pattern | ● live | 5 | ✓ |
| [Xahau vs XRPL mainnet (when to choose Xahau)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 5 | ✓ |
| [Xaman (formerly XUMM) wallet + developer platform](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 5 | ✓ |
| [rippled (core XRPL server)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 5 | ✓ |
| [xrpl-py](client-libraries.md) | Client libraries & SDKs | library | · n/a | 5 | ✓ |
| [xrpl.js](client-libraries.md) | Client libraries & SDKs | library | · n/a | 5 | ✓ |
| [AMM <> CLOB Integration (auto-routing)](dex-amm.md) | DEX & AMM | pattern | ● live | 4 | ✓ |
| [AMMDeposit (single & double asset)](dex-amm.md) | DEX & AMM | transaction | ● live | 4 | ✓ |
| [AMMWithdraw](dex-amm.md) | DEX & AMM | transaction | ● live | 4 | ✓ |
| [Amendment process (2/3 supermajority, 2-week activation)](protocol-consensus.md) | Protocol & consensus | concept | ● live | 4 | ✓ |
| [CronSet (scheduled hook callbacks)](programmability-hooks.md) | Programmability — Hooks (Xahau) | transaction | ◐ pending | 4 | ✓ |
| [Cross-currency payments & pathfinding](payments-advanced.md) | Advanced payments | pattern | ● live | 4 | ✓ |
| [Crossmark (browser-extension XRPL wallet)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 4 | ✓ |
| [Destination tags & source tags](payments-advanced.md) | Advanced payments | concept | ● live | 4 | ✓ |
| [Emitted transactions (autonomous on-ledger actions)](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 4 | ✓ |
| [Escrow (XRP) — time-based & conditional](payments-advanced.md) | Advanced payments | transaction | ● live | 4 | ✓ |
| [Foundry deployment toolchain](programmability-evm.md) | Programmability — XRPL EVM sidechain | library | ● live | 4 | ✓ |
| [GemWallet (browser-extension XRPL wallet)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 4 | ✓ |
| [Guard / weak-guard (_g) and bounded execution](programmability-hooks.md) | Programmability — Hooks (Xahau) | pattern | ● live | 4 | ✓ |
| [Hook API (C primitives / function categories)](programmability-hooks.md) | Programmability — Hooks (Xahau) | library | ● live | 4 | ✓ |
| [Hook developer tooling (Hooks Builder, SDKs, testnet)](programmability-hooks.md) | Programmability — Hooks (Xahau) | service | ● live | 4 | ✓ |
| [JS Hooks (JSHooks — JavaScript authoring)](programmability-hooks.md) | Programmability — Hooks (Xahau) | library | ○ devnet | 4 | ✓ |
| [MPT Controls (Lock, RequireAuth, Clawback, Transfer Fee, Metadata)](tokens.md) | Tokens & issued assets | concept | ● live | 4 | ✓ |
| [MPTokenAuthorize (Hold / Authorize an MPT)](tokens.md) | Tokens & issued assets | transaction | ● live | 4 | ✓ |
| [Multi-Purpose Tokens (MPTokensV1)](protocol-consensus.md) | Protocol & consensus | amendment | ● live | 4 | ✓ |
| [NFTokenCreateOffer](nfts.md) | NFTs | transaction | ● live | 4 | ✓ |
| [NFTokenTaxon & Collections](nfts.md) | NFTs | concept | ● live | 4 | ✓ |
| [OfferCancel](dex-amm.md) | DEX & AMM | transaction | ● live | 4 | ✓ |
| [Payment Channels (PaymentChannelCreate / Fund / Claim)](payments-advanced.md) | Advanced payments | transaction | ● live | 4 | ✓ |
| [Permissioned DEXes](identity-compliance.md) | Identity & compliance | amendment | ● live | 4 | · |
| [Proof-of-Authority / CometBFT consensus](programmability-evm.md) | Programmability — XRPL EVM sidechain | concept | ● live | 4 | ✓ |
| [Public RPC node providers (QuickNode, GetBlock, public clusters)](infrastructure-tooling.md) | Infrastructure & tooling | service | ● live | 4 | ✓ |
| [Remix + MetaMask quick path](programmability-evm.md) | Programmability — XRPL EVM sidechain | pattern | ● live | 4 | ✓ |
| [RequireAuth (authorized trust lines)](identity-compliance.md) | Identity & compliance | concept | ● live | 4 | ✓ |
| [Rippling, NoRipple & Default Ripple](tokens.md) | Tokens & issued assets | concept | ● live | 4 | ✓ |
| [SetRegularKey (Regular Key Pair)](transactions.md) | Transactions & accounts | transaction | ● live | 4 | ✓ |
| [Token Escrow (XLS-85) — IOU & MPT escrow](payments-advanced.md) | Advanced payments | amendment | ● live | 4 | ✓ |
| [Transfer Fees (TransferRate)](tokens.md) | Tokens & issued assets | concept | ● live | 4 | ✓ |
| [XLS-47 Native Price Oracles](infrastructure-tooling.md) | Infrastructure & tooling | amendment | ● live | 4 | ✓ |
| [XRP Ledger Consensus Protocol (XRP LCP)](protocol-consensus.md) | Protocol & consensus | concept | ● live | 4 | ✓ |
| [XRPL EVM sidechain dev stack (ethers / web3 / viem)](client-libraries.md) | Client libraries & SDKs | concept | ● live | 4 | ✓ |
| [rippled / xrpld core server (v3.2.0 rebrand)](protocol-consensus.md) | Protocol & consensus | service | ● live | 4 | · |
| [tfImmediateOrCancel / tfFillOrKill / tfSell (offer execution flags)](dex-amm.md) | DEX & AMM | pattern | ● live | 4 | ✓ |
| [AMMBid (continuous auction slot)](dex-amm.md) | DEX & AMM | transaction | ● live | 3 | ✓ |
| [AMMVote (governable trading fee)](dex-amm.md) | DEX & AMM | transaction | ● live | 3 | ✓ |
| [Account Permission Delegation (DelegateSet / Delegate)](transactions.md) | Transactions & accounts | amendment | ○ devnet | 3 | · |
| [Batch Transactions (XLS-56)](transactions.md) | Transactions & accounts | amendment | ○ devnet | 3 | · |
| [Batch transactions (BatchV1_1 revival)](protocol-consensus.md) | Protocol & consensus | amendment | ◐ pending | 3 | ✓ |
| [Compliance freeze controls (Freeze / Deep Freeze / Clawback)](identity-compliance.md) | Identity & compliance | concept | ● live | 3 | ✓ |
| [Hook fees & execution metering](programmability-hooks.md) | Programmability — Hooks (Xahau) | concept | ● live | 3 | ✓ |
| [Hooks (Xahau L1 programmability)](infrastructure-tooling.md) | Infrastructure & tooling | amendment | × deprecated | 3 | ✓ |
| [LPToken (AMM liquidity-provider token)](dex-amm.md) | DEX & AMM | concept | ● live | 3 | ✓ |
| [NFTokenCancelOffer](nfts.md) | NFTs | transaction | ● live | 3 | ✓ |
| [Source & Destination Tags](transactions.md) | Transactions & accounts | concept | ● live | 3 | ✓ |
| [Token Escrow (IOU & MPT)](tokens.md) | Tokens & issued assets | amendment | ● live | 3 | ✓ |
| [Xahau / Hooks SDK note (xahau.js)](client-libraries.md) | Client libraries & SDKs | library | ● live | 3 | · |
| [hooks-rs (Rust authoring)](programmability-hooks.md) | Programmability — Hooks (Xahau) | library | ○ devnet | 2 | ✓ |

_Each capability's full detail (key fields, gotchas, sources) lives in its feature-domain readout, linked above._

