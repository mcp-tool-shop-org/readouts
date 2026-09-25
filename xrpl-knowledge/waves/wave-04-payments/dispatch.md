# Wave 4 — Payments & micropayments (depth)

**Dispatched 2026-06-14 · 5 depth sub-lanes · 41 capabilities · build-focus folder: payments.**

## Scope

Depth wave curating the `payments` folder — the payment PRIMITIVES in depth (distinct from Wave 3's
game-economy *flows*). Sub-lanes by home domain:
- **channels** → `payments-advanced` (off-ledger streaming micropayments; XRP-only)
- **escrow** → `payments-advanced` (time-based + crypto-conditional; TokenEscrow XLS-85 for IOU/MPT)
- **crosscurrency** → `payments-advanced` (pathfinding, auto-bridging, partial-payment `delivered_amount` safety)
- **batch** → `transactions` (mass payouts: Batch XLS-56, Tickets, throughput)
- **checks** → `payments-advanced` (deferred pull payments, backend integration, reconciliation, deposit-auth)

## Method

Direct synchronous dispatch + discriminating fitness; authoritative cross-family verification by
`deepseek-v3.1:671b-cloud` (`scripts/verify_cloud.py`). **40/41 confirmed** (37 · 3 with-fixes · 1 refuted · 0 unverified).

## Results

- **41 capabilities · 40/41 cross-family verified.** KB now 290 capabilities / 4 waves. The `payments` folder
  is **56 depth-curated / 194 total**.
- **Studio building blocks:** payment-channel off-ledger claim flow (sign-many-settle-once for high-frequency
  tipping), crypto-condition + time-based escrow (TokenEscrow now covers IOU/MPT), cross-currency Payment
  (send A → deliver B atomically via the DEX), the **`delivered_amount` partial-payment safety rule** (never
  trust `Amount`/`DeliverMax` on a backend), Batch (XLS-56) + Ticket-based mass payouts, Checks for deferred
  pull payments, and destination-tag/InvoiceID custodial sub-account crediting with idempotent reconciliation.
- Payment-channel **XRP-only** constraint captured (channels do not carry tokens — use escrow for token value).

## Provenance

`research-raw.json` (research + `cloud_verify`), rows `wave_id=4`. Ingested by `scripts/load_db.py`, rebuilt by
`scripts/regen.py`.
