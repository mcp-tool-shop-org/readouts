---
id: kb_did_transactions
title: "DIDSet / DIDDelete transactions (XLS-40)"
track: identity
summary: "DIDSet creates a new DID ledger entry for the sending account or updates an existing one; DIDDelete removes…"
time: 15-20 min
level: beginner
mode: testnet
requires: []
produces:
  - txid
  - report
checks:
  - "Understood: DIDSet / DIDDelete transactions"
  - "Transaction performed on testnet (txid produced)"
  - "Verified the key fields: ['Account', 'DIDDocument', 'Data', 'URI', 'DIDDelete']"
  - "Avoided the gotcha: ['DIDSet requires at least one of DIDDocument / URI / Data — an empty DIDSet…"
---
<!-- DRAFT auto-seeded from xrpl-knowledge capability `did-transactions` (Identity & compliance, mainnet-live, verified) · amendment `DID`.
     Edit forward: write the prose, wire the core action, set requires/checks. -->

DIDSet creates a new DID ledger entry for the sending account or updates an existing one; DIDDelete removes it. DIDSet must set at least one of DIDDocument, Data, or URI. These are the only two transaction types in the DID feature, giving a minimal CRUD surface.

## Step 1: Ensure your wallet is ready

You need a funded wallet. If you completed an earlier module it loads automatically.

<!-- action: ensure_wallet -->

## Step 2: DIDSet / DIDDelete transactions

**Key fields / API to know:** ["Account", "DIDDocument", "Data", "URI", "DIDDelete"]

<!-- TODO: wire the core action for this module. The KB describes WHAT happens; pick the
     matching xrpl-lab action (see `xrpl-lab lint` for the registered action schema), e.g.:
       <!-- action: ensure_funded -->
       <!-- action: submit_payment destination=ADDRESS amount=10 -->
       <!-- action: set_trust_line currency=LAB limit=1000 -->
     Until wired, this module is dry-run/teaching-only. -->

## Step 3: Verify on-ledger

Inspect what happened on the explorer — turn the result into evidence you can read.

## Checkpoint: What you proved

You now understand **DIDSet / DIDDelete transactions**.

**Watch out:** ["DIDSet requires at least one of DIDDocument / URI / Data — an empty DIDSet fails.", "Each of DIDDocument/Data/URI is hex-encoded blob data with size limits; large documents must live off-ledger and be referenced by URI.", "DIDDelete frees the owner reserve but irrevocably removes the on-ledger document; off-ledger references are unaffected and must be cleaned up separately."]

**Learn more (verified sources):**
- [DIDSet — xrpl.org transaction reference](https://xrpl.org/docs/references/protocol/transactions/types/didset) — DIDSet creates or updates a DID ledger entry and must include at least one of…

Run `xrpl-lab proof-pack` when you're ready to export your work.
