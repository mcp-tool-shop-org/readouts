---
id: kb_escrow_xrp
title: "Escrow (XRP) — time-based & conditional"
track: payments
summary: "Escrow locks XRP on-ledger to be released only when conditions are met. Three release models exist:…"
time: 15-20 min
level: beginner
mode: testnet
requires: []
produces:
  - txid
  - report
checks:
  - "Understood: Escrow (XRP) — time-based & conditional"
  - "Transaction performed on testnet (txid produced)"
  - "Verified the key fields: ['EscrowCreate: Amount, Destination, FinishAfter, CancelAfter, Condition…"
  - "Avoided the gotcha: ['PREIMAGE-SHA-256 is the ONLY supported crypto-condition type.', 'EscrowFinish…"
---
<!-- DRAFT auto-seeded from xrpl-knowledge capability `escrow-xrp` (Advanced payments, mainnet-live, verified) · amendment `Escrow`.
     Edit forward: write the prose, wire the core action, set requires/checks. -->

Escrow locks XRP on-ledger to be released only when conditions are met. Three release models exist: time-based (FinishAfter), conditional (a PREIMAGE-SHA-256 crypto-condition whose fulfillment must be supplied), and combination (both). EscrowCreate locks the funds, EscrowFinish releases them to the destination once conditions hold, and EscrowCancel returns them to the sender after CancelAfter…

## Step 1: Ensure your wallet is ready

You need a funded wallet. If you completed an earlier module it loads automatically.

<!-- action: ensure_wallet -->

## Step 2: Escrow (XRP) — time-based & conditional

**Key fields / API to know:** ["EscrowCreate: Amount, Destination, FinishAfter, CancelAfter, Condition (PREIMAGE-SHA-256), DestinationTag", "EscrowFinish: Owner, OfferSequence, Condition, Fulfillment", "EscrowCancel: Owner, OfferSequence", "ledger object: Escrow"]

<!-- TODO: wire the core action for this module. The KB describes WHAT happens; pick the
     matching xrpl-lab action (see `xrpl-lab lint` for the registered action schema), e.g.:
       <!-- action: ensure_funded -->
       <!-- action: submit_payment destination=ADDRESS amount=10 -->
       <!-- action: set_trust_line currency=LAB limit=1000 -->
     Until wired, this module is dry-run/teaching-only. -->

## Step 3: Verify on-ledger

Inspect what happened on the explorer — turn the result into evidence you can read.

## Checkpoint: What you proved

You now understand **Escrow (XRP) — time-based & conditional**.

**Watch out:** ["PREIMAGE-SHA-256 is the ONLY supported crypto-condition type.", "EscrowFinish with a Fulfillment costs an elevated fee proportional to the fulfillment size (anti-spam).", "Release times are granular to ledger close (~3–5s); FinishAfter is 'earliest', not exact.", "An escrow without FinishAfter or Condition is pointless (would be immediately finishable); the ledger requires at least one release mechanism.", "Locked XRP still counts toward the owner's reserve obligations."]

**Learn more (verified sources):**
- [Escrow (xrpl.org)](https://xrpl.org/docs/concepts/payment-types/escrow) — Escrow supports time-based, conditional (PREIMAGE-SHA-256 the sole supported…
- [Known Amendments (xrpl.org)](https://xrpl.org/resources/known-amendments) — The Escrow amendment enabling conditional and time-based escrows of XRP is enabled on…

Run `xrpl-lab proof-pack` when you're ready to export your work.
