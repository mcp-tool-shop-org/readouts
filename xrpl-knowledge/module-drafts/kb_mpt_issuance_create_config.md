---
id: kb_mpt_issuance_create_config
title: "MPTokenIssuanceCreate — issuer config for a game currency (XLS-33)"
track: tokens
summary: "MPTokenIssuanceCreate is the single transaction that defines a game currency's entire on-chain policy in one…"
time: 15-20 min
level: beginner
mode: testnet
requires: []
produces:
  - txid
  - report
checks:
  - "Understood: MPTokenIssuanceCreate — issuer config for a game currency"
  - "Transaction performed on testnet (txid produced)"
  - "Verified the key fields: MaximumAmount (UInt64, optional cap); AssetScale (UInt8 0..255 decimals,…"
  - "Avoided the gotcha: All config is immutable after create — there is no 'edit the currency'…"
---
<!-- DRAFT auto-seeded from xrpl-knowledge capability `mpt-issuance-create-config` (Tokens & issued assets, mainnet-live, verified) · amendment `MPTokensV1`.
     Edit forward: write the prose, wire the core action, set requires/checks. -->

MPTokenIssuanceCreate is the single transaction that defines a game currency's entire on-chain policy in one shot: supply cap, decimals, transfer fee, capability flags, and metadata. Because every field is IMMUTABLE after creation (until/unless XLS-94 mutable-fields ships), this transaction is the most consequential design decision in the whole token economy — get the flags right or re-issue a…

## Step 1: Ensure your wallet is ready

You need a funded wallet. If you completed an earlier module it loads automatically.

<!-- action: ensure_wallet -->

## Step 2: MPTokenIssuanceCreate — issuer config for a game currency

**Key fields / API to know:** MaximumAmount (UInt64, optional cap); AssetScale (UInt8 0..255 decimals, default 0); TransferFee (UInt16 0..50000 = 0.000%..50.000% in 0.001% increments, requires tfMPTCanTransfer if non-zero); MPTokenMetadata (Blob <=1024 bytes, conventionally JSON); flags tfMPTCanLock(2)/tfMPTRequireAuth(4)/tfMPTCanEscrow(8)/tfMPTCanTrade(16)/tfMPTCanTransfer(32)/tfMPTCanClawback(64); DomainID (requires tfMPTRequireAuth); 0.2 XRP issuer owner reserve per issuance

<!-- TODO: wire the core action for this module. The KB describes WHAT happens; pick the
     matching xrpl-lab action (see `xrpl-lab lint` for the registered action schema), e.g.:
       <!-- action: ensure_funded -->
       <!-- action: submit_payment destination=ADDRESS amount=10 -->
       <!-- action: set_trust_line currency=LAB limit=1000 -->
     Until wired, this module is dry-run/teaching-only. -->

## Step 3: Verify on-ledger

Inspect what happened on the explorer — turn the result into evidence you can read.

## Checkpoint: What you proved

You now understand **MPTokenIssuanceCreate — issuer config for a game currency**.

**Watch out:** All config is immutable after create — there is no 'edit the currency' transaction in mid-2026 (XLS-94 still proposed). A non-transferable MPT (tfMPTCanTransfer off) CANNOT have a transfer fee and is only usable issuer<->holder. tfMPTCanClawback and tfMPTCanLock MUST be chosen at create time; you cannot retrofit clawback or freeze onto an already-minted MPT, so an anti-exploit recall lever must be opted in up front. Decide AssetScale carefully: integer-only math means scale defines your smallest spendable unit forever.

**Learn more (verified sources):**
- [MPTokenIssuanceCreate](https://xrpl.org/docs/references/protocol/transactions/types/mptokenissuancecreate) — Flags tfMPTCanLock(0x2), tfMPTRequireAuth(0x4), tfMPTCanEscrow(0x8), tfMPTCanTrade(0x10),…
- [Issue a Multi-Purpose Token (tutorial)](https://xrpl.org/docs/tutorials/how-tos/use-tokens/issue-a-multi-purpose-token) — An MPT issuance ledger entry counts as one object toward the issuer's owner reserve (0.2…

Run `xrpl-lab proof-pack` when you're ready to export your work.
