-- xrpl-knowledge :: schema
-- A wave-appended knowledge base of the XRP Ledger ECOSYSTEM for a builder: the protocol
-- features, transaction types, XLS standards, client libraries and tooling you actually use,
-- each tagged with its CURRENT mainnet / amendment status. One SQLite file; the "cluster" is
-- the linked-table graph:
--   waves -> capabilities -> {capability_purposes -> purposes, sources} ; categories
-- Two organizing structures, both first-class:
--   categories          = the FEATURE domains (the ingest/provenance backbone)
--   purposes.track      = the four BUILD-FOCUS folders (game-economies / nft-assets /
--                         payments / identity-compliance) — a cross-cutting builder lens.
-- Every fact carries a wave_id (provenance); capabilities/sources carry a verified flag.
-- The verified flag is written by the EXTERNAL_VERIFIER: seat 1 = Claude+WebFetch retrieval
-- oracle (live docs), seat 2 = a cross-family Ollama Cloud large model (deepseek-v3.1:671b)
-- as the AUTHORITATIVE family-decorrelated judge. Decisive axis: network_status — is this
-- ACTUALLY enabled on XRPL mainnet right now, vs amendment-pending / devnet / deprecated.

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meta (
  key   TEXT PRIMARY KEY,
  value TEXT
);

-- One row per study-swarm wave. New waves append; nothing is overwritten.
CREATE TABLE IF NOT EXISTS waves (
  id              INTEGER PRIMARY KEY,
  wave_number     INTEGER NOT NULL UNIQUE,
  title           TEXT NOT NULL,
  dispatched_date TEXT NOT NULL,          -- ISO date, passed in (workflows have no clock)
  domain_scope    TEXT,
  agent_count     INTEGER,
  verifier_note   TEXT,                    -- how citations were verified this wave
  status          TEXT DEFAULT 'synthesized',
  dispatch_path   TEXT,
  notes           TEXT
);

-- FEATURE domains (the ingest backbone). Seeded below; load_db auto-creates any new lane slug.
CREATE TABLE IF NOT EXISTS categories (
  id          INTEGER PRIMARY KEY,
  slug        TEXT UNIQUE NOT NULL,
  name        TEXT NOT NULL,
  description TEXT,
  sort        INTEGER DEFAULT 0
);

-- PRIMARY ENTITY: an XRPL capability — "a thing you can do on the ledger", typed by `kind`.
CREATE TABLE IF NOT EXISTS capabilities (
  id                INTEGER PRIMARY KEY,
  slug              TEXT UNIQUE NOT NULL,
  name              TEXT NOT NULL,
  category_id       INTEGER REFERENCES categories(id),
  kind              TEXT,                  -- concept|transaction|standard|amendment|library|service|pattern
  network_status    TEXT,                  -- mainnet-live|amendment-pending|testnet-devnet|deprecated|n/a  (DECISIVE AXIS)
  chain             TEXT,                  -- xrpl-mainnet|xahau|xrpl-evm-sidechain|all
  xls_standard      TEXT,                  -- e.g. XLS-20, XLS-33, XLS-70
  amendment_name    TEXT,                  -- on-ledger amendment name if applicable
  enabled_date      TEXT,                  -- ISO date it went live on mainnet, if known
  maturity_tier     TEXT,                  -- stable|new|experimental|deprecated
  status            TEXT,                  -- recommended|situational|legacy|avoid (builder guidance for USING it)
  builder_fit       INTEGER,               -- 0-5 overall usefulness to a builder
  commercial_use    TEXT,                  -- carried for the shared index renderer; XRPL is permissionless -> usually NULL
  summary           TEXT,
  key_fields        TEXT,                  -- the tx fields / API methods / params a builder must know
  gotchas           TEXT,                  -- reserves, fees, common mistakes
  download_priority INTEGER,               -- lower = surface first (derived from status + maturity)
  verified          INTEGER DEFAULT 0,     -- AUTHORITATIVE cross-family cloud seat confirmed existence/status/currency
  verify_note       TEXT,                  -- combined seat verdicts (cloud 671b + retrieval oracle)
  wave_id           INTEGER REFERENCES waves(id),
  created_date      TEXT
);

-- Purposes = fine-grained "best for X". `track` groups a purpose into one of the four BUILD-FOCUS folders.
CREATE TABLE IF NOT EXISTS purposes (
  id          INTEGER PRIMARY KEY,
  slug        TEXT UNIQUE NOT NULL,
  name        TEXT NOT NULL,
  track       TEXT,                         -- game-economies|nft-assets|payments|identity-compliance|NULL
  description TEXT
);

-- "best capability for what" matrix (many-to-many) — also the join the four track folders are built from.
CREATE TABLE IF NOT EXISTS capability_purposes (
  capability_id INTEGER NOT NULL REFERENCES capabilities(id) ON DELETE CASCADE,
  purpose_id    INTEGER NOT NULL REFERENCES purposes(id) ON DELETE CASCADE,
  fitness       INTEGER,                    -- 0-5
  rank          INTEGER,                    -- 1 = best-in-class for this purpose
  note          TEXT,
  PRIMARY KEY (capability_id, purpose_id)
);

-- citation / evidence trail (study-swarm sourcing standard)
CREATE TABLE IF NOT EXISTS sources (
  id                INTEGER PRIMARY KEY,
  capability_id     INTEGER REFERENCES capabilities(id) ON DELETE CASCADE,
  subject           TEXT,                  -- when not tied to a capability row
  kind              TEXT,                  -- docs|xls-spec|release-notes|repo|api-ref|community
  title             TEXT,
  url               TEXT NOT NULL,
  claim             TEXT,                  -- one-sentence finding this source backs
  retrieved_date    TEXT,
  verified          INTEGER DEFAULT 0,     -- retrieval oracle confirmed it resolves
  finding_supported INTEGER,               -- groundedness: source actually states the claim
  verifier_note     TEXT,
  wave_id           INTEGER REFERENCES waves(id)
);

-- full-text search (matches the repo-knowledge FTS5 convention; <table>_fts naming)
CREATE VIRTUAL TABLE IF NOT EXISTS capabilities_fts USING fts5(
  slug, name, kind, summary, network_status, xls_standard, category
);

CREATE INDEX IF NOT EXISTS idx_cap_category ON capabilities(category_id);
CREATE INDEX IF NOT EXISTS idx_cap_status   ON capabilities(status);
CREATE INDEX IF NOT EXISTS idx_cap_network  ON capabilities(network_status);
CREATE INDEX IF NOT EXISTS idx_src_cap      ON sources(capability_id);
CREATE INDEX IF NOT EXISTS idx_cp_purpose   ON capability_purposes(purpose_id);

-- convenience views ----------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_recommended AS
  SELECT c.name AS category, cap.download_priority AS dl, cap.name, cap.kind,
         cap.network_status, cap.chain, cap.xls_standard, cap.status, cap.maturity_tier,
         cap.builder_fit AS fit, cap.verified
  FROM capabilities cap JOIN categories c ON c.id = cap.category_id
  WHERE cap.status IN ('recommended', 'situational')
  ORDER BY c.sort, cap.download_priority, cap.name;

CREATE VIEW IF NOT EXISTS v_best_for AS
  SELECT p.name AS purpose, p.track, cap.name AS capability, cp.rank, cp.fitness,
         cap.network_status, cap.chain, cap.verified
  FROM capability_purposes cp
  JOIN capabilities cap ON cap.id = cp.capability_id
  JOIN purposes p       ON p.id  = cp.purpose_id
  ORDER BY p.track, p.name, cp.rank, cp.fitness DESC;

-- decisive-axis view: what's actually live vs pending vs gone
CREATE VIEW IF NOT EXISTS v_by_network AS
  SELECT cap.network_status, c.name AS category, cap.name, cap.kind, cap.xls_standard,
         cap.chain, cap.status, cap.verified
  FROM capabilities cap JOIN categories c ON c.id = cap.category_id
  ORDER BY (cap.network_status <> 'mainnet-live'), cap.network_status, c.sort, cap.name;

-- the four BUILD-FOCUS folders as a query (capability x track)
CREATE VIEW IF NOT EXISTS v_tracks AS
  SELECT p.track, c.name AS category, cap.name AS capability, cap.kind,
         cap.network_status, cp.fitness, cap.verified
  FROM capability_purposes cp
  JOIN purposes p       ON p.id  = cp.purpose_id
  JOIN capabilities cap ON cap.id = cp.capability_id
  JOIN categories c     ON c.id  = cap.category_id
  WHERE p.track IS NOT NULL
  ORDER BY p.track, c.sort, (cp.fitness IS NULL), cp.fitness DESC, cap.name;

-- proof-by-artifact tier: on-ledger receipts (txids) from xrpl-lab that PROVE a capability
-- works live. NOT wave-scoped — load_db never deletes it; keyed by capability slug so it
-- survives re-ingestion. The strongest verification tier:
--   research-verified (cross-family seat) < retrieval-confirmed < PROVEN-ON-LEDGER (a real txid).
CREATE TABLE IF NOT EXISTS proofs (
  id              INTEGER PRIMARY KEY,
  capability_slug TEXT NOT NULL,
  txid            TEXT NOT NULL,
  network         TEXT,                  -- testnet | mainnet | devnet
  explorer_url    TEXT,
  module_id       TEXT,                  -- the xrpl-lab module that produced it
  proved_date     TEXT,
  source          TEXT DEFAULT 'xrpl-lab',
  UNIQUE(capability_slug, txid)
);

CREATE VIEW IF NOT EXISTS v_proven AS
  SELECT cap.name, cap.slug, c.name AS category, cap.network_status, cap.verified,
         p.txid, p.network, p.explorer_url, p.module_id, p.proved_date
  FROM proofs p
  JOIN capabilities cap ON cap.slug = p.capability_slug
  JOIN categories c     ON c.id = cap.category_id
  ORDER BY (p.proved_date IS NULL), p.proved_date DESC, cap.name;

-- seed the four BUILD-FOCUS track anchors (purposes with a track) ---------------
INSERT OR IGNORE INTO purposes(slug, name, track, description) VALUES
  ('track-game-economies',     'Game token economies',           'game-economies',     'In-game currencies, sinks & faucets, soft/hard money via IOUs / MPTs / RLUSD'),
  ('track-nft-assets',         'NFT game assets & marketplaces',  'nft-assets',         'Mint, trade, royalties, brokered sales, dynamic NFTs for game assets'),
  ('track-payments',           'Payments & micropayments',        'payments',           'Player payouts, payment channels, escrow, cross-currency value transfer'),
  ('track-identity-compliance','Identity & compliance',           'identity-compliance','Player DID, credentials, permissioned domains, KYC / region-gated features');

-- seed the wave-1 FEATURE domains (load_db auto-creates any extra lane the swarm surfaces) -------
INSERT OR IGNORE INTO categories(slug, name, description, sort) VALUES
  ('protocol-consensus',        'Protocol & consensus',                'XRP LCP, validators & UNL, ledger objects, fees & reserves, the XRP asset, the amendment process.',                        10),
  ('transactions',              'Transactions & accounts',             'The transaction model & fields, autofill/sign/submit lifecycle, results & metadata, tickets, multisign, batch, delegation.', 20),
  ('tokens',                    'Tokens & issued assets',              'Issued currencies (IOUs) & trust lines, rippling, freeze/deep-freeze, clawback, Multi-Purpose Tokens (MPTs).',               30),
  ('stablecoins-institutional', 'Stablecoins & institutional',         'RLUSD, stablecoin issuance patterns, institutional rails, tokenized RWAs, on-chain compliance building blocks.',            40),
  ('dex-amm',                   'DEX & AMM',                           'Native order-book DEX, auto-bridging, pathfinding, the AMM (XLS-30), permissioned DEX.',                                   50),
  ('nfts',                      'NFTs',                                'XLS-20 NFTokens: mint/burn, offers, brokered vs direct sales, royalties, collections, dynamic NFTs.',                      60),
  ('programmability-hooks',     'Programmability — Hooks (Xahau)',     'Hooks on the Xahau network: the Hooks API, SetHook, Xahau vs XRPL mainnet, when to use it.',                               70),
  ('programmability-evm',       'Programmability — XRPL EVM sidechain','The XRPL EVM sidechain: Solidity contracts, the Axelar bridge, EVM tooling, when to use it vs native XRPL.',              80),
  ('payments-advanced',         'Advanced payments',                   'Escrow, payment channels (micropayments), checks, partial & cross-currency payments, destination tags.',                   90),
  ('identity-compliance',       'Identity & compliance',               'DID (XLS-40), Credentials (XLS-70), permissioned domains, deposit auth, account flags, the on-chain KYC toolkit.',        100),
  ('client-libraries',          'Client libraries & SDKs',             'xrpl.js, xrpl-py, xrpl4j, ripple-binary-codec, keypairs/signing, wallets, faucets, which lib for which stack.',           110),
  ('infrastructure-tooling',    'Infrastructure & tooling',            'rippled, Clio, public nodes & data APIs, explorers, wallets, price oracles (XLS-47), indexers, dev networks.',            120);
