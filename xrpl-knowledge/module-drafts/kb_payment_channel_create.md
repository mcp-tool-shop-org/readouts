---
id: kb_payment_channel_create
title: "PaymentChannelCreate"
track: payments
summary: "Opens and funds a unidirectional XRP payment channel from the sending account (source) to a fixed…"
time: 15-20 min
level: beginner
mode: testnet
requires: []
produces:
  - txid
  - report
checks:
  - "Understood: PaymentChannelCreate"
  - "Transaction performed on testnet (txid produced)"
  - "Verified the key fields: ['Amount (XRP drops escrowed into the channel; locked until claimed or…"
  - "Avoided the gotcha: ['Unidirectional only: this funds source->destination; a return flow needs a…"
---
<!-- DRAFT auto-seeded from xrpl-knowledge capability `payment-channel-create` (Advanced payments, mainnet-live, verified) · amendment `PayChan`.
     Edit forward: write the prose, wire the core action, set requires/checks. -->

Opens and funds a unidirectional XRP payment channel from the sending account (source) to a fixed Destination. Sets the escrowed Amount (drops), the SettleDelay grace period, the PublicKey the source will sign claims with, and optionally an immutable CancelAfter. This is the one on-ledger setup transaction that enables an unbounded off-ledger micropayment stream afterward.

## Step 1: Ensure your wallet is ready

You need a funded wallet. If you completed an earlier module it loads automatically.

<!-- action: ensure_wallet -->

## Step 2: PaymentChannelCreate

**Key fields / API to know:** ["Amount (XRP drops escrowed into the channel; locked until claimed or returned)", "Destination (the only account that can receive from this channel; cannot equal source)", "SettleDelay (UInt32 seconds the source must wait before a forced close completes if funds remain)", "PublicKey (33-byte hex; secp256k1 or Ed25519 key the source uses to sign all claims)", "CancelAfter (optional UInt32 Ripple-epoch seconds; IMMUTABLE hard expiry, cannot be extended)", "DestinationTag / SourceTag (optional routing tags)"]

<!-- TODO: wire the core action for this module. The KB describes WHAT happens; pick the
     matching xrpl-lab action (see `xrpl-lab lint` for the registered action schema), e.g.:
       <!-- action: ensure_funded -->
       <!-- action: submit_payment destination=ADDRESS amount=10 -->
       <!-- action: set_trust_line currency=LAB limit=1000 -->
     Until wired, this module is dry-run/teaching-only. -->

## Step 3: Verify on-ledger

Inspect what happened on the explorer — turn the result into evidence you can read.

## Checkpoint: What you proved

You now understand **PaymentChannelCreate**.

**Watch out:** ["Unidirectional only: this funds source->destination; a return flow needs a second, separately-funded channel.", "XRP-only: Amount must be XRP drops. There is no token/IOU/MPT channel on mainnet as of mid-2026.", "CancelAfter is immutable once set — pick it carefully; only the mutable Expiration (set later via Fund/Claim) can change.", "Since fixPayChanCancelAfter (~2025-08-29), a CancelAfter in the past fails with tecEXPIRED instead of creating then auto-expiring.", "Costs one owner-reserve item (0.2 XRP) PLUS the escrowed Amount; both are locked, not spent.", "Fails with tecNO_PERMISSION if the destination has DisallowIncoming set for payment channels."]

**Learn more (verified sources):**
- [PaymentChannelCreate - XRPL.org](https://xrpl.org/docs/references/protocol/transactions/types/paymentchannelcreate) — Required fields are Amount, Destination, SettleDelay, and PublicKey; CancelAfter is…
- [Payment Channels concept - XRPL.org](https://xrpl.org/docs/concepts/payment-types/payment-channels) — Payment channels are unidirectional and XRP-only; the source sets aside XRP and signs…

Run `xrpl-lab proof-pack` when you're ready to export your work.
