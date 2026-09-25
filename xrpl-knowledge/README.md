# xrpl-knowledge

**Status:** Waves through 10 (STUDY-057 Hooks vs EVM builder track 2026-09-07). Catalog **457 · 362/457 · 10 waves**. Invent-enabled: 0. Invent Mainnet Hooks: 0.

- **Wave 10 (STUDY-057 Hooks vs EVM builder track)** — [dispatch](waves/wave-10-study-057-hooks-evm/dispatch.md) · [research-raw](waves/wave-10-study-057-hooks-evm/research-raw.json) — invent-enabled: 0; invent Mainnet Hooks: 0; no mainnet; no funds; Scholar #6 unverified; Analogist #7–#8 fail-transfer omitted.
- **Wave 9 (STUDY-056 amendment-pending)** — [dispatch](waves/wave-09-study-056-amendment-pending/dispatch.md) · [research-raw](waves/wave-09-study-056-amendment-pending/research-raw.json) — invent-enabled: 0; no mainnet; no funds.
- **Wave 8 (STUDY-036 Hooks/sidechain deepen)** — [dispatch](waves/wave-08-study-036-hooks-sidechain-deepen/dispatch.md) · [research-raw](waves/wave-08-study-036-hooks-sidechain-deepen/research-raw.json) — 14 caps; invent-enabled: 0; no mainnet-live invent.

A verified, wave-appended knowledge base of the **XRP Ledger ecosystem for a builder** — the protocol
features, transaction types, XLS standards, client libraries and tooling you actually use — each tagged with
its **current mainnet / amendment status**. Part of the [readouts](../README.md) monorepo.

**Whole-ecosystem:** XRPL mainnet + Xahau/Hooks + the XRPL EVM sidechain + the institutional layer
(RLUSD, compliance).

## Decisive axis

`network_status` — **is this feature actually enabled on XRPL mainnet right now** (vs amendment-pending /
devnet-only / deprecated), and which standard/library is current. XRPL moves by amendment; a builder ships
against what's live.

## Two ways in

- **Feature domains** (the ingest backbone, one capability lives in exactly one): protocol-consensus ·
  transactions · tokens · stablecoins-institutional · dex-amm · nfts · programmability-hooks ·
  programmability-evm · payments-advanced · identity-compliance · client-libraries · infrastructure-tooling.
- **Build-focus folders** (cross-cutting lenses, a capability appears in every one it serves):
  [game token economies](catalog/track-game-economies.md) · [NFT game assets](catalog/track-nft-assets.md) ·
  [payments & micropayments](catalog/track-payments.md) ·
  [identity & compliance](catalog/track-identity-compliance.md).

Front door: [`catalog/README.md`](catalog/README.md) (text) · [`readout/index.html`](readout/index.html)
(branded) · [`readout/index.json`](readout/index.json) (programmatic).

## Query it

```powershell
# resolve the right slice via ai-loadout (two-level: root -> this KB -> domain/track)
ai-loadout resolve --project xrpl-knowledge

# or open the DB directly (views v_recommended, v_best_for, v_by_network, v_tracks; FTS capabilities_fts)
sqlite3 xrpl.db "SELECT * FROM v_by_network WHERE network_status='mainnet-live';"
```

## Verification (cross-family)

Research is web-grounded (Claude agents over xrpl.org + the XLS specs). The authoritative `verified` flag is
set by a **different model family** — a large Ollama Cloud model (`deepseek-v3.1:671b-cloud`,
`scripts/verify_cloud.py`), run refute-by-default. Same-family judges over-rate via self-preference; a
cross-family seat catches over-claimed status on the newest amendments. `verified` means the cross-family seat
confirmed; blank means refuted, unverified, or pending.

## Add a wave

```powershell
$env:PYTHONUTF8='1'
# research lanes -> waves/wave-NN/lane-*.json, then:
python scripts/assemble_lanes.py waves/wave-NN <date> <N>     # -> research-raw.json
python scripts/verify_cloud.py  waves/wave-NN/research-raw.json   # cross-family seat -> cloud_verify
python scripts/load_db.py       waves/wave-NN/research-raw.json   # cloud seat sets verified
python scripts/regen.py                                            # rebuild catalog + readouts + loadout + root
```

See [`../CONVENTIONS.md`](../CONVENTIONS.md) for the shared KB recipe.
