# Wave 5 — Identity & compliance (depth)

**Dispatched 2026-06-14 · 5 depth sub-lanes · 40 capabilities · build-focus folder: identity-compliance.**

## Scope

The final depth wave — curates the `identity-compliance` folder AND settles the Wave-1 items the cross-family
seat would not confirm at foundation. Sub-lanes (all `identity-compliance` domain): DID · Credentials ·
Permissioned Domains & gated access · Deposit authorization & account controls · compliance toolkit patterns.

## Method

Direct synchronous dispatch + discriminating fitness; authoritative cross-family verification by
`deepseek-v3.1:671b-cloud` (`scripts/verify_cloud.py`). **33/40 confirmed** (33 · 4 refuted · 3 unverified) —
identity/compliance remains the most-scrutinized area, as it should (newest amendments).

## Results — and the Wave-1 settlements

- **40 capabilities · 33/40 cross-family verified.** KB now **330 capabilities / 5 waves**; all four
  build-focus folders are curated (game-economies 106 · nft-assets 45 · payments 69 · identity 49 depth-curated).
- **Settled the Wave-1 open items** (Wave 1's seat would not confirm these; Wave 5 resolved them with dates,
  and the cross-family seat CONFIRMED the depth entries):
  - **Credentials (XLS-70): mainnet-live 2025-09-04** — CredentialCreate/Accept/Delete, issuer→subject
    attestation model. The authoritative w5 entries are cross-family verified; the broad w1 entries remain
    unverified (historical first pass).
  - **Credential-based DepositPreauth: mainnet 2025-09-04** (DepositPreauth.AuthorizeCredentials) — the on-chain
    KYC-gated deposit primitive. (Address-based DepositAuth/DepositPreauth live since 2018; DisallowIncoming 2023-08-21.)
  - **Permissioned Domains (XLS-80) / Permissioned DEX** — status captured per the live amendment table (a few
    specifics the seat still would not fully confirm remain `verified=0` — honest residual uncertainty).
- **Studio building blocks:** player DID (portable cross-game identity), credential-gated access (age/region
  verification), KYC/AML-gated economy (Credentials + Permissioned Domains + DepositPreauth + Freeze/Clawback),
  region-locking & age-gating patterns, and the on-chain-vs-custodial compliance decision (PII stays off-ledger).

## Provenance

`research-raw.json` (research + `cloud_verify`), rows `wave_id=5`. Ingested by `scripts/load_db.py`, rebuilt by
`scripts/regen.py`. The 7 non-confirmed items stay `verified=0` and surface in the verification receipt.
