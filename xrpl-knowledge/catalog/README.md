# Catalog — xrpl-knowledge

Generated from `xrpl.db` · wave 10 · 2026-09-07. NEVER hand-edited — regenerated from the DB.

The **XRP Ledger ecosystem for a builder** — protocol features, transaction types, XLS standards, client libraries and tooling — each tagged with its **current mainnet/amendment status** (the decisive axis). Whole-ecosystem: XRPL mainnet + Xahau/Hooks + the XRPL EVM sidechain + the institutional layer (RLUSD, compliance). Sibling KBs live in the same [readouts](../../index.md) monorepo.

**457 capabilities · 362 cross-family verified · 880 sources · wave 10.**

## Decisive axis — what's live

XRPL moves by amendment. The first question for any feature is whether it is **enabled on mainnet right now** vs amendment-pending vs devnet-only vs deprecated. Counts by `network_status`:

| network_status | capabilities |
|---|--:|
| ● live | 341 |
| · n/a | 65 |
| ◐ pending | 29 |
| ○ devnet | 21 |
| × deprecated | 1 |

## Feature domains

The ingest backbone — every capability lives in exactly one.

| Domain | Capabilities | Live | Verified |
|---|--:|--:|--:|
| [Protocol & consensus](protocol-consensus.md) | 48 | 13 | 22/48 |
| [Transactions & accounts](transactions.md) | 20 | 17 | 18/20 |
| [Tokens & issued assets](tokens.md) | 37 | 29 | 34/37 |
| [Stablecoins & institutional](stablecoins-institutional.md) | 21 | 21 | 19/21 |
| [DEX & AMM](dex-amm.md) | 29 | 27 | 24/29 |
| [NFTs](nfts.md) | 57 | 48 | 50/57 |
| [Programmability — Hooks (Xahau)](programmability-hooks.md) | 45 | 30 | 35/45 |
| [Programmability — XRPL EVM sidechain](programmability-evm.md) | 54 | 40 | 40/54 |
| [Advanced payments](payments-advanced.md) | 56 | 53 | 51/56 |
| [Identity & compliance](identity-compliance.md) | 51 | 49 | 38/51 |
| [Client libraries & SDKs](client-libraries.md) | 11 | 2 | 10/11 |
| [Infrastructure & tooling](infrastructure-tooling.md) | 28 | 12 | 21/28 |

## Build-focus folders

The four builder lenses — cross-cutting views that assemble the relevant capabilities from across the feature domains. **Curated** = tagged by that folder's focused depth wave (the building blocks); **total** also includes the foundation wave's wider net. A capability appears in every folder it serves.

| Folder | Curated | Total | Live | Verified |
|---|--:|--:|--:|--:|
| [Game token economies](track-game-economies.md) | 146 | 253 | 227 | 230/253 |
| [NFT game assets & marketplaces](track-nft-assets.md) | 58 | 127 | 110 | 116/127 |
| [Payments & micropayments](track-payments.md) | 92 | 230 | 210 | 211/230 |
| [Identity & compliance](track-identity-compliance.md) | 61 | 163 | 150 | 142/163 |
## Proven on-ledger

Capabilities an [xrpl-lab](https://github.com/mcp-tool-shop-org/xrpl-lab) module has executed LIVE, with a real txid — the strongest verification tier (research-verified < retrieval-confirmed < proven-on-ledger).

| Capability | Domain | Network | txid |
|---|---|---|---|
| Direct token Payment with trustline (player <-> game value transfer) | Advanced payments | testnet | [C356C4551EB06DE6C8…](https://testnet.xrpl.org/transactions/C356C4551EB06DE6C8093B273806419606C2BA2CC30D636B62EF4D4AABD25A46) |
| Escrow as marketplace / trade settlement (counterparty-risk-free) | Advanced payments | testnet | [C0DFD2B14B43E29B44…](https://testnet.xrpl.org/transactions/C0DFD2B14B43E29B4443B5329D3D9FB15AA635B6610DE11441AD9562921849B2) |
| IOU trust-line token as uncapped soft currency | Tokens & issued assets | testnet | [C356C4551EB06DE6C8…](https://testnet.xrpl.org/transactions/C356C4551EB06DE6C8093B273806419606C2BA2CC30D636B62EF4D4AABD25A46) |
| NFTokenAcceptOffer (Direct + Brokered) | NFTs | testnet | [6A05C8AEE476BB41F2…](https://testnet.xrpl.org/transactions/6A05C8AEE476BB41F2589AD066F87F6D0FBE6B8DF5FC91F302956A6B591B666E) |
| NFTokenBurn | NFTs | testnet | [231D09D29F5C4BD4F7…](https://testnet.xrpl.org/transactions/231D09D29F5C4BD4F76096D1B8E28A8E272DB41B2C60D9FDCDA5199E10EB1914) |
| NFTokenCreateOffer | NFTs | testnet | [8F06D1A6F1A3882D59…](https://testnet.xrpl.org/transactions/8F06D1A6F1A3882D5955B18451FE4E0EF0A39CE5293E8CE96DAC04C54C065B98) |
| NFTokenModify Transaction | NFTs | testnet | [0ECEB77E4585842DA1…](https://testnet.xrpl.org/transactions/0ECEB77E4585842DA14C02D66E506B3D79633DED37B790D8DD4E40DEE151F6D9) |
| Token Escrow (XLS-85) — IOU & MPT escrow | Advanced payments | testnet | [C0DFD2B14B43E29B44…](https://testnet.xrpl.org/transactions/C0DFD2B14B43E29B4443B5329D3D9FB15AA635B6610DE11441AD9562921849B2) |
| Direct token Payment with trustline (player <-> game value transfer) | Advanced payments | testnet | [B0370EFAE3617C37EF…](https://testnet.xrpl.org/transactions/B0370EFAE3617C37EF1E783E078495E44E6AB273F0806C14B81D6C321913B171) |
| IOU trust-line token as uncapped soft currency | Tokens & issued assets | testnet | [953C9246E9E6CE4045…](https://testnet.xrpl.org/transactions/953C9246E9E6CE4045BB302BDFD830E878094AFA0C45D1216279C9F1526D6959) |
| Transaction Common Fields | Transactions & accounts | testnet | [4254BCCDB3EF67F62B…](https://testnet.xrpl.org/transactions/4254BCCDB3EF67F62B1AB19EAA2EAE0E4913EFE144745DCE045AABFEA4826FFF) |
| Transaction Common Fields | Transactions & accounts | testnet | [B310D13755617F2BEF…](https://testnet.xrpl.org/transactions/B310D13755617F2BEF251F4DE1EAE009428FD771C9DB3D0D83464BAA9020BC32) |
| DIDSet / DIDDelete transactions | Identity & compliance | testnet | [A34E6ABABD6CFE6426…](https://testnet.xrpl.org/transactions/A34E6ABABD6CFE64267C0146874B508D70E033EC46BF616DFD6192389D1A24F4) |
| Escrow (XRP) — time-based & conditional | Advanced payments | testnet | [685A81D64CD1D845B5…](https://testnet.xrpl.org/transactions/685A81D64CD1D845B54D6948E2A8ED1C8A0DF4715A4121F2203FBB8C09FB7B9A) |
| MPTokenIssuanceCreate — issuer config for a game currency | Tokens & issued assets | testnet | [5E650A26B875980E9D…](https://testnet.xrpl.org/transactions/5E650A26B875980E9D3D2E7F0D82E1F2A1AB5BF93C2952D3DB3724902585A8CA) |
| NFTokenMint | NFTs | testnet | [3A60E25806DBE04D7D…](https://testnet.xrpl.org/transactions/3A60E25806DBE04D7DF1A9B5195D81527474501EEC98C617BBF46B438CCF07E2) |


## Legend

- **Network:** ● mainnet-live (amendment enabled) · ◐ amendment-pending · ○ testnet/devnet · × deprecated. The decisive axis — a builder ships against what's live.
- **Kind:** concept · transaction · standard (XLS) · amendment · library · service · pattern.
- **Fit:** builder usefulness 0–5. **Use:** recommended / situational / legacy / avoid.
- **✓** cross-family verified: the AUTHORITATIVE seat is a large Ollama Cloud model (different family from the Claude researcher — no self-preference); a Claude+WebFetch retrieval oracle checks the live docs as seat 1. Blank/· = pending or unconfirmed.
- **Chains:** xrpl-mainnet · xahau (Hooks) · xrpl-evm-sidechain · all.
