---
id: kb_nftokenmint
title: "NFTokenMint (XLS-20)"
track: nfts
summary: "NFTokenMint creates a new NFToken and assigns it to the minting account (or to the Issuer if minting on…"
time: 15-20 min
level: beginner
mode: testnet
requires: []
produces:
  - txid
  - report
checks:
  - "Understood: NFTokenMint"
  - "Transaction performed on testnet (txid produced)"
  - "Verified the key fields: NFTokenTaxon (required, 0-0xFFFFFFFF collection id), URI (optional, up to 256…"
  - "Avoided the gotcha: Flags and TransferFee are permanent once minted. TransferFee only takes effect…"
---
<!-- DRAFT auto-seeded from xrpl-knowledge capability `nftokenmint` (NFTs, mainnet-live, verified) · amendment `NonFungibleTokensV1_1`.
     Edit forward: write the prose, wire the core action, set requires/checks. -->

NFTokenMint creates a new NFToken and assigns it to the minting account (or to the Issuer if minting on behalf via authorized minter). It sets the immutable properties of the NFT: flags, transfer fee, taxon, and URI. This is the single entry point for putting a new NFT on the ledger.

## Step 1: Ensure your wallet is ready

You need a funded wallet. If you completed an earlier module it loads automatically.

<!-- action: ensure_wallet -->

## Step 2: NFTokenMint

**Key fields / API to know:** NFTokenTaxon (required, 0-0xFFFFFFFF collection id), URI (optional, up to 256 bytes hex, not validated), TransferFee (0-50000 = 0%-50% in 0.001% steps), Issuer (optional, for authorized-minter mode), Flags. Flags: tfBurnable 0x1, tfOnlyXRP 0x2, tfTransferable 0x8, tfMutable 0x10. Optional Amount/Destination/Expiration to also create a sell offer (NFTokenMintOffer).

<!-- TODO: wire the core action for this module. The KB describes WHAT happens; pick the
     matching xrpl-lab action (see `xrpl-lab lint` for the registered action schema), e.g.:
       <!-- action: ensure_funded -->
       <!-- action: submit_payment destination=ADDRESS amount=10 -->
       <!-- action: set_trust_line currency=LAB limit=1000 -->
     Until wired, this module is dry-run/teaching-only. -->

## Step 3: Verify on-ledger

Inspect what happened on the explorer — turn the result into evidence you can read.

## Checkpoint: What you proved

You now understand **NFTokenMint**.

**Watch out:** Flags and TransferFee are permanent once minted. TransferFee only takes effect if tfTransferable is set. URI is stored as hex and never checked for validity, so dead links are possible. Each mint increments the issuer's MintedNFTokens; with fixNFTokenRemint, sequence = FirstNFTSequence + MintedNFTokens. Max NFTs per issuer is 2^32-1.

**Learn more (verified sources):**
- [NFTokenMint (XRPL.org)](https://xrpl.org/docs/references/protocol/transactions/types/nftokenmint) — NFTokenMint sets immutable flags, TransferFee (0-50000 = 0-50%), NFTokenTaxon, and an…

Run `xrpl-lab proof-pack` when you're ready to export your work.
