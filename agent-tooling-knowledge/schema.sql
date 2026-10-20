-- agent-tooling-knowledge :: schema
-- A wave-appended knowledge base of MEASURED and DOCUMENTED behaviour of the harnesses that run AI agents:
-- Claude Code headless/print mode and MCP lifecycle, permissions and containment, agent sandboxes, agent tracing.
-- What a studio harness must know so an agent run does what it claims.
--
-- Shape copied from docker-knowledge (findings + finding_sources + measurements); siblings:
--   model-knowledge          -> the models (a model's serving settings live there, even under a harness)
--   docker-knowledge         -> GPU inference placement in containers
--   agent-tooling-knowledge  -> THIS: agent harness behaviour
--
-- One SQLite file; waves -> findings -> {finding_sources}; categories; measurements.
-- Every fact carries a wave_id; findings carry a verified flag set only from a verdict block. Waves APPEND.

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meta (
  key   TEXT PRIMARY KEY,
  value TEXT
);

-- One row per study-swarm wave.
CREATE TABLE IF NOT EXISTS waves (
  id              INTEGER PRIMARY KEY,
  wave_number     INTEGER NOT NULL UNIQUE,
  title           TEXT NOT NULL,
  dispatched_date TEXT NOT NULL,          -- ISO date, passed in (workflows have no clock)
  domain_scope    TEXT,
  agent_count     INTEGER,
  verifier_note   TEXT,                   -- how citations were verified this wave
  status          TEXT DEFAULT 'synthesized',
  dispatch_path   TEXT,
  notes           TEXT
);

CREATE TABLE IF NOT EXISTS categories (
  id          INTEGER PRIMARY KEY,
  slug        TEXT UNIQUE NOT NULL,
  name        TEXT NOT NULL,
  description TEXT,
  sort        INTEGER DEFAULT 0
);

-- The core entity: a finding about how an agent harness behaves (measured or documented).
CREATE TABLE IF NOT EXISTS findings (
  id                 INTEGER PRIMARY KEY,
  slug               TEXT UNIQUE NOT NULL,
  name               TEXT NOT NULL,        -- short title of the finding/technique
  category_id        INTEGER REFERENCES categories(id),
  kind               TEXT,                 -- behaviour|gotcha|constraint|method|policy
  claim              TEXT,                 -- one-sentence load-bearing statement
  detail             TEXT,                 -- the explanation / how-to
  applies_to         TEXT,                 -- scope: the CLI/tool versions and rule forms the finding was measured on
  design_implication TEXT,                 -- what a studio harness should do about it
  metric             TEXT,                 -- headline count if any ("3 of 3 starts", "13 plan turns")
  confidence         TEXT,                 -- high|medium|low
  rig_relevance      INTEGER,              -- 0-5 relevance to the studio's agent harnesses
  status             TEXT,                 -- load-bearing|supporting|watch|refuted
  verified           INTEGER DEFAULT 0,    -- 1 only from a verdict block naming what checked it (a re-probe receipt or a primary doc)
  verify_note        TEXT,
  wave_id            INTEGER REFERENCES waves(id),
  created_date       TEXT
);

-- citation / evidence trail (study-swarm sourcing standard; mirrors the feasibility-swarm record)
CREATE TABLE IF NOT EXISTS finding_sources (
  id                INTEGER PRIMARY KEY,
  finding_id        INTEGER REFERENCES findings(id) ON DELETE CASCADE,
  subject           TEXT,                  -- when not tied to a finding row
  kind              TEXT,                  -- paper|docs|repo|benchmark|release-notes|article|community
  title             TEXT,
  authors           TEXT,
  year              TEXT,
  identifier        TEXT,                  -- arXiv:NNNN.NNNNN | DOI | repo | url-id
  url               TEXT NOT NULL,
  claim             TEXT,                  -- one-sentence finding this source backs
  quant             TEXT,                  -- the number the source reports, if any
  retrieved_date    TEXT,
  exists_verified   INTEGER DEFAULT 0,     -- retrieval oracle confirmed it resolves + attribution
  finding_supported TEXT,                  -- SUPPORTED|PARTIAL|NOT_SUPPORTED|CANT_TELL (groundedness)
  verifier_note     TEXT,
  wave_id           INTEGER REFERENCES waves(id)
);

-- measured rig readouts (the "baselines/" companion, in queryable form).
-- This is where the Milestone-1 profiler's own output lands — knowledge <-> measurement loop.
CREATE TABLE IF NOT EXISTS measurements (
  id            INTEGER PRIMARY KEY,
  metric        TEXT NOT NULL,             -- pcie_h2d_gbps|nvme_seq_read_gbps|nvme_rand_qd1_iops|vram_total_gb|pinnable_ram_gb|decode_tok_s ...
  value         REAL,
  unit          TEXT,
  context       TEXT,                      -- sandbox|host|<cli version>
  tool          TEXT,                      -- the command or probe
  source_file   TEXT,                      -- receipt file name
  note          TEXT,
  wave_id       INTEGER REFERENCES waves(id),
  measured_date TEXT
);

-- full-text search over findings (matches the siblings' FTS5 convention)
CREATE VIRTUAL TABLE IF NOT EXISTS findings_fts USING fts5(
  slug, name, claim, detail, applies_to, design_implication, category
);

CREATE INDEX IF NOT EXISTS idx_findings_category ON findings(category_id);
CREATE INDEX IF NOT EXISTS idx_findings_status   ON findings(status);
CREATE INDEX IF NOT EXISTS idx_fsrc_finding      ON finding_sources(finding_id);
CREATE INDEX IF NOT EXISTS idx_meas_metric       ON measurements(metric);

-- convenience views ----------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_load_bearing AS
  SELECT c.name AS category, f.name, f.kind, f.claim, f.metric, f.applies_to,
         f.design_implication, f.confidence, f.verified, f.status
  FROM findings f JOIN categories c ON c.id = f.category_id
  WHERE f.status IN ('load-bearing', 'supporting')
  ORDER BY c.sort, f.status, f.name;

CREATE VIEW IF NOT EXISTS v_gotchas AS
  SELECT c.name AS category, f.name, f.claim, f.applies_to, f.design_implication, f.verified
  FROM findings f JOIN categories c ON c.id = f.category_id
  WHERE f.kind IN ('gotcha', 'constraint')
  ORDER BY c.sort, f.name;

CREATE VIEW IF NOT EXISTS v_baseline AS
  SELECT metric, value, unit, context, tool, measured_date, source_file
  FROM measurements
  ORDER BY metric, context;

-- seed the lanes -------------------------------------------------------------
INSERT OR IGNORE INTO categories(slug, name, description, sort) VALUES
  ('claude-code-headless',    'Claude Code headless & MCP',    'Print/stream-json mode, the init event, MCP server lifecycle at the first turn, versions',                10),
  ('permissions-containment', 'Permissions & containment',     'Permission rules (deny/allow, path anchors), what they do and do not contain, OS-level containment',     20),
  ('agent-sandboxes',         'Agent sandboxes',               'Docker Sandboxes (sbx): setup, credentials, network policy, reaching host services, operational gotchas', 30),
  ('agent-tracing',           'Agent tracing',                 'Tracing agent runs (NeMo Relay): what is recorded locally, what leaves the machine, privacy of traces',   40);
