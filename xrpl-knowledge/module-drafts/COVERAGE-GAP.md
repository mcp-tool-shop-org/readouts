# xrpl-lab coverage gap — sourced from xrpl-knowledge
Generated from `xrpl.db` + `E:\AI\xrpl-lab\modules`. The KB is the curriculum source; a high-value capability no module teaches is a candidate module.

**xrpl-lab today: 28 modules** across tracks amm, audit, capstone, dex, foundations, identity, nfts, payments, reserves, tokens.

## Domain coverage

| KB domain | Caps | Recommended | Mainnet-live | xrpl-lab track | Covered? |
|---|--:|--:|--:|---|---|
| Protocol & consensus | 15 | 11 | 13 | reserves/foundations | ✅ yes |
| Transactions & accounts | 20 | 12 | 17 | foundations/audit | ✅ yes |
| Tokens & issued assets | 37 | 16 | 29 | foundations | 🟡 partial |
| Stablecoins & institutional | 21 | 9 | 21 | payments (proposed) | ❌ none |
| DEX & AMM | 27 | 20 | 27 | dex/amm | ✅ yes |
| NFTs | 57 | 28 | 45 | nfts (proposed) | ❌ none |
| Programmability — Hooks (Xahau) | 35 | 18 | 30 | programmability (proposed) | ❌ none |
| Programmability — XRPL EVM sidechain | 41 | 8 | 40 | programmability (proposed) | ❌ none |
| Advanced payments | 53 | 13 | 53 | payments (proposed) | 🟡 partial |
| Identity & compliance | 51 | 13 | 49 | identity (proposed) | 🟡 partial |
| Client libraries & SDKs | 11 | 5 | 2 | foundations (reference) | ❌ none |
| Infrastructure & tooling | 14 | 13 | 12 | ops (proposed) | ❌ none |

## Module backlog — top untaught capabilities per gap domain

Ranked by builder_fit then verified. Each is a candidate `xrpl-lab` module (`scaffold --from-kb <slug>`). Capabilities already echoed in a module's title/summary are skipped.

### Tokens & issued assets → track `foundations` _(currently partial)_  ·  4 candidates
- **IOU vs MPT — Decision Guide** [XLS-33] `iou-vs-mpt-decision` — fit 5/5 ✓ · pattern · Choosing between trust-line IOUs and MPTs is the central token decision in mid-2026. Pick MPTs for NEW issuances that want native on-chain m
- **MPT as fixed-supply hard currency (MaximumAmount cap)** [XLS-33] `mpt-fixed-supply-hard-currency` — fit 5/5 ✓ · pattern · An MPToken issuance carries a protocol-enforced MaximumAmount (1 to 2^63-1 integer units), making it the natural primitive for a HARD in-gam
- **MPT Controls (Lock, RequireAuth, Clawback, Transfer Fee, Metadata)** [XLS-33] `mpt-controls` — fit 4/5 ✓ · concept · MPTs bundle their issuer controls into per-issuance capability flags and fields rather than separate account-wide settings. lsfMPTCanLock en
- **Rippling, NoRipple & Default Ripple** `rippling-noripple` — fit 4/5 ✓ · concept · Rippling is atomic net settlement of balances among parties who hold the same issuer's currency, letting one holder pay another with the iss

### Stablecoins & institutional → track `payments (proposed)`  ·  2 candidates
- **RLUSD (Ripple USD) on XRPL** `rlusd-on-xrpl` — fit 5/5 ✓ · service · Ripple's USD-pegged, fully-reserved stablecoin, issued NATIVELY on XRPL mainnet as a standard trust-line fungible token (not an MPT). It is 
- **Tokenized real-world assets (RWA) on XRPL** [XLS-33] `rwa-tokenization` — fit 4/5 ✓ · pattern · The institutional pattern of representing off-chain assets (treasuries, money-market funds, equity, fixed income, real estate, commercial pa

### NFTs → track `nfts (proposed)`  ·  12 candidates
- **Authorized minter (asfAuthorizedNFTokenMinter)** [XLS-20] `authorized-nftoken-minter` — fit 5/5 ✓ · transaction · An account can delegate minting to another account so a hot 'minting service' wallet can issue NFTs on behalf of a cold issuer/brand account
- **Eager (scripted) vs lazy (mint-on-demand) minting** [XLS-20] `lazy-vs-eager-minting` — fit 5/5 ✓ · pattern · Two minting strategies with opposite trade-offs. Eager/scripted minting pre-mints the whole collection on-ledger so provenance and serials e
- **NFTokenAcceptOffer (Direct + Brokered)** [XLS-20] `nftokenacceptoffer` — fit 5/5 ✓ · transaction · NFTokenAcceptOffer settles a sale. In direct mode a buyer accepts a sell offer (or a seller accepts a buy offer) by referencing one offer. I
- **NFTokenMint** [XLS-20] `nftokenmint` — fit 5/5 ✓ · transaction · NFTokenMint creates a new NFToken and assigns it to the minting account (or to the Issuer if minting on behalf via authorized minter). It se
- **NFTokenPage & Owner Reserve** [XLS-20] `nftokenpage-owner-reserve` — fit 5/5 ✓ · concept · NFTs are stored in NFTokenPage objects, each holding up to 32 NFTs owned by the same account. Owner reserve is charged per page (currently 0
- **NFTokenTaxon collection-identity strategy** [XLS-20] `nftokentaxon-collection-strategy` — fit 5/5 ✓ · pattern · XRPL has no native 'collection' ledger object. Collection identity is the pair (Issuer account, NFTokenTaxon) — every NFT minted by the same
- **Authorized Minter Delegation** [XLS-20] `authorized-minter` — fit 4/5 ✓ · pattern · An issuer can authorize a separate account to mint NFTs on its behalf by setting the NFTokenMinter field with the asfAuthorizedNFTokenMinter
- **NFTokenBurn** [XLS-20] `nftokenburn` — fit 4/5 ✓ · transaction · NFTokenBurn permanently destroys an NFToken, removing it from the ledger and freeing the owner reserve once the NFTokenPage empties. The cur

### Programmability — Hooks (Xahau) → track `programmability (proposed)`  ·  14 candidates
- **Hook API conventions & primitives (hook_account / otxn_* / return codes)** `hook-api-conventions` — fit 5/5 ✓ · concept · The Hook API is a fixed set of host functions the WASM module imports. Context accessors include hook_account (the account the hook is insta
- **Hooks (WASM smart-contract layer)** `hooks-overview` — fit 5/5 ✓ · concept · Hooks are small, efficient WebAssembly modules attached to a Xahau account that execute BEFORE and/or AFTER transactions affect that account
- **Hooks execution model (Layer-1 WASM transaction interceptor)** `hooks-execution-model` — fit 5/5 ✓ · concept · Hooks are small WebAssembly modules installed on a Xahau account that execute as part of consensus whenever a transaction touches that accou
- **Xahau vs XRPL mainnet (when to choose Xahau)** `xahau-vs-xrpl` — fit 5/5 ✓ · concept · Xahau is a distinct Layer-1 network forked from XRPL Core (xrpld), not a Layer-2 of XRPL. It adds the Hooks smart-contract layer, its own na
- **C/WASM toolchain & hook-cleaner (build pipeline)** `hook-c-wasm-toolchain` — fit 4/5 ✓ · concept · The blessed production path is C compiled to WebAssembly. Toolkits (hooks-toolkit / @xahau/hooks-cli) compile contracts in a contracts/ dire
- **Hook API (C primitives / function categories)** `hook-api` — fit 4/5 ✓ · library · The Hook API is the set of host functions a hook calls to read the originating transaction, manage state, do math, and emit transactions. Ca
- **Hook chaining (up to 10 hooks per account)** `hook-chaining` — fit 4/5 ✓ · pattern · An account can install a chain of up to 10 hooks at positions 0–9, executed in order; the chain succeeds only if every installed hook reache
- **Hook developer tooling (Hooks Builder, SDKs, testnet)** `hook-tooling` — fit 4/5 ✓ · service · A maturing tooling ecosystem supports hook development: the Hooks Builder browser IDE (compile C → WASM, deploy, debug), the C Hook macro he

### Programmability — XRPL EVM sidechain → track `programmability (proposed)`  ·  8 candidates
- **Axelar bridge (XRPL ⇄ EVM sidechain)** `axelar-bridge` — fit 5/5 ✓ · service · Axelar is the exclusive launch bridge connecting XRPL mainnet to the EVM sidechain and to 80+ other chains. It is a decentralized proof-of-s
- **EVM mainnet network parameters (chain ID & RPC)** `evm-network-params` — fit 5/5 ✓ · concept · The connection settings a builder needs to point any EVM tool (wallet, RPC client, deploy script) at the chain. Mainnet uses chain ID 144000
- **Hardhat deployment toolchain** `hardhat-toolchain` — fit 5/5 ✓ · library · Hardhat works unchanged against the XRPL EVM sidechain — add a network entry with the chain's RPC + chain ID and deploy Solidity contracts v
- **Solidity / EVM smart contracts** `solidity-evm-contracts` — fit 5/5 ✓ · concept · Full Ethereum Virtual Machine compatibility lets you write, deploy and call Solidity contracts exactly as on Ethereum, using OpenZeppelin li
- **XRPL EVM Sidechain (standalone Cosmos L1)** `xrpl-evm-sidechain-chain` — fit 5/5 ✓ · concept · The XRPL EVM sidechain is a standalone Layer-1 blockchain that runs Ethereum-compatible smart contracts with XRP as the native gas token. It
- **Foundry deployment toolchain** `foundry-toolchain` — fit 4/5 ✓ · library · Foundry (forge/cast) works against the sidechain like any EVM chain — compile, test and deploy ERC-20/contracts by pointing forge at the RPC
- **Axelar Interchain Token Service (ITS)** `axelar-its` — fit 4/5 ✓ · service · The Interchain Token Service is the Axelar primitive that lets a single token exist canonically across many chains with consistent supply ac
- **Remix + MetaMask quick path** `remix-metamask` — fit 4/5 ✓ · pattern · The fastest on-ramp: configure MetaMask with the sidechain's network params, then deploy directly from the Remix browser IDE using MetaMask 

### Advanced payments → track `payments (proposed)` _(currently partial)_  ·  8 candidates
- **Destination tags & source tags** `destination-tags` — fit 5/5 ✓ · concept · Source and destination tags are 32-bit unsigned integers attached to payments (and other transactions like escrows and checks) that let a si
- **PaymentChannelClaim (redeem or close)** `payment-channel-claim` — fit 5/5 ✓ · transaction · The on-ledger transaction that actually moves XRP out of a channel, or renews/closes it. The destination submits it with the channel's large
- **PaymentChannelCreate** `payment-channel-create` — fit 5/5 ✓ · transaction · Opens and funds a unidirectional XRP payment channel from the sending account (source) to a fixed Destination. Sets the escrowed Amount (dro
- **SettleDelay & closure / cancel mechanics** `settledelay-closure-mechanics` — fit 4/5 ✓ · concept · The trust model of a channel rests on its closure rules. SettleDelay is the minimum seconds the source must wait, after requesting closure o
- **PaymentChannelFund (extend funds & Expiration)** `payment-channel-fund` — fit 4/5 ✓ · transaction · Source-only transaction to top up an existing channel with more XRP and/or extend its mutable Expiration, keeping a long-lived streaming cha
- **Checks (CheckCreate / CheckCash / CheckCancel)** `checks` — fit 3/5 ✓ · transaction · Checks are deferred, pull-style payments: the sender writes a Check authorizing a maximum amount, and the recipient later pulls funds by cas
- **Crypto-conditions (PREIMAGE-SHA-256)** `crypto-conditions` — fit 3/5 ✓ · standard · Crypto-conditions are the cryptographic locking mechanism used by conditional Escrow. The XRPL implements the IETF crypto-conditions draft b
- **Invoice ID (InvoiceID field)** `invoice-id` — fit 3/5 ✓ · concept · InvoiceID is an optional 256-bit (64 hex char) field on Payment and Check transactions used to reference an external invoice, order, or off-

### Identity & compliance → track `identity (proposed)` _(currently partial)_  ·  8 candidates
- **DID amendment (XLS-40)** [XLS-40 (XLS-40d)] `did-amendment-xls40` — fit 5/5 ✓ · standard · The protocol amendment that adds native W3C-conformant Decentralized Identifiers to XRPL. It introduces the DID ledger object plus the DIDSe
- **Off-chain document & credential linking (URI pattern)** [XLS-40] `did-offchain-linking-pattern` — fit 5/5 ✓ · pattern · The canonical XLS-40 pattern: keep the DID anchor on-ledger but store the rich DID document and any credentials off-chain (IPFS/STORJ/HTTPS)
- **CredentialCreate / CredentialAccept / CredentialDelete** [XLS-70] `credential-transactions` — fit 5/5 · · transaction · The three-transaction lifecycle of a credential. CredentialCreate (sent by the issuer) mints a credential for a Subject with a CredentialTyp
- **DIDSet / DIDDelete transactions** [XLS-40] `did-transactions` — fit 4/5 ✓ · transaction · DIDSet creates a new DID ledger entry for the sending account or updates an existing one; DIDDelete removes it. DIDSet must set at least one
- **RequireAuth (authorized trust lines)** `require-auth` — fit 4/5 ✓ · concept · An issuer account flag (asfRequireAuth, value 2) that requires the issuer to explicitly authorize each trust line before a holder can receiv
- **did:xrpl method & DID document resolution** [XLS-40] `did-xrpl-method-resolution` — fit 4/5 ✓ · standard · The did:xrpl method defines how an XRPL DID string is formed and resolved to a W3C DID document. The identifier carries a network number and
- **Portable cross-game player identity (DID anchor)** [XLS-40] `did-portable-cross-game-identity` — fit 4/5 ✓ · pattern · The studio-level application of XLS-40: use one wallet-bound DID as a stable identity anchor a player carries across multiple games/titles, 
- **DisallowIncoming flags** `disallow-incoming-flags` — fit 3/5 · · concept · A family of account flags that block specific unsolicited inbound objects: asfDisallowIncomingCheck (13), asfDisallowIncomingNFTokenOffer (1

### Client libraries & SDKs → track `foundations (reference)`  ·  2 candidates
- **XRPL EVM sidechain dev stack (ethers / web3 / viem)** `xrpl-evm-dev-stack` — fit 4/5 ✓ · concept · The XRPL EVM sidechain is an Ethereum-compatible chain (Cosmos SDK + CometBFT, Proof-of-Authority) whose mainnet went live 2025-06-30, using
- **Xahau / Hooks SDK note (xahau.js)** `xahau-hooks-sdk` — fit 2/5 · · library · Xahau is a separate, XRPL-derived network that adds Hooks (lightweight on-ledger smart-contract logic in WebAssembly). It is interacted with

### Infrastructure & tooling → track `ops (proposed)`  ·  12 candidates
- **Clio (read-optimized API server)** `clio-api-server` — fit 5/5 ✓ · service · Clio is the XRPLF API server purpose-built for reads: it ingests validated ledger/transaction data from designated rippled nodes and stores 
- **XRPL Client SDKs (xrpl.js / xrpl-py / xrpl4j / xrpl-go)** `xrpl-client-sdks` — fit 5/5 ✓ · standard · Official XRPLF client libraries wrap the rippled/Clio API into language-native conventions for connecting, building/signing transactions, an
- **XRPL Dev Networks (Testnet / Devnet / specialty devnets)** `xrpl-dev-networks` — fit 5/5 ✓ · concept · XRPL parallel networks for development: Testnet (mainnet-like, stable feature set), Devnet (previews upcoming amendments), plus specialty ne
- **Xaman (formerly XUMM) wallet + developer platform** `xaman-wallet` — fit 5/5 ✓ · service · Xaman (the rebrand of XUMM, by XRPL Labs) is the mobile-first self-custody wallet with the deepest native XRPL/Xahau feature coverage — trus
- **rippled (core XRPL server)** `rippled-core-server` — fit 5/5 ✓ · service · rippled is the reference C++ server that forms the XRPL peer-to-peer network: it processes transactions, participates in consensus, and can 
- **Bithomp (explorer + Explorer-as-a-Service)** `bithomp-explorer` — fit 4/5 ✓ · service · Bithomp is a long-standing XRPL explorer with broad coverage (accounts, transactions, tokens, NFTs) plus known-address lookups and statistic
- **Crossmark (browser-extension XRPL wallet)** `crossmark-wallet` — fit 4/5 ✓ · service · Crossmark is a browser-extension XRPL wallet supporting most major browsers, with an SDK that lets applications integrate signing directly. 
- **GemWallet (browser-extension XRPL wallet)** `gemwallet` — fit 4/5 ✓ · service · GemWallet (released Nov 2022 as the first browser-based XRPL wallet) is an open-source, decentralization-focused extension that brings a Web

## Recommended new tracks

xrpl-lab's tracks (foundations/dex/reserves/audit/amm) mirror today's coverage. The KB reveals whole-ecosystem depth that needs new tracks:

- **nfts** — mint, collections, marketplaces, royalties, dynamic NFTs (game assets)
- **payments** — escrow, payment channels, checks, batch payouts, cross-currency
- **identity** — DID, Credentials, permissioned domains, deposit-auth (KYC-gated)
- **programmability** — Hooks (Xahau) + EVM sidechain contracts
- **tokens** (or extend foundations) — MPTs, clawback, freeze, issuance depth beyond IOU trust lines

Adopting a track = add it to `xrpl_lab/curriculum.py::TRACKS`.

**Total auto-detected backlog: 70 candidate modules.**
