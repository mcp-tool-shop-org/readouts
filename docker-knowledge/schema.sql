-- docker-knowledge :: schema
-- A wave-appended knowledge base for HONEST INFERENCE MEMORY PLACEMENT on a single
-- consumer GPU: how to PACKAGE (Docker / NVIDIA Container Toolkit / WSL2), how to
-- MEASURE the rig truthfully (especially from INSIDE the container), and how to PLACE
-- a model across VRAM / pinned RAM / NVMe with a measured receipt and an honest refusal.
-- Backs the gpu-container product (github.com/mcp-tool-shop-org/gpu-container).
--
-- Complements the siblings, does NOT duplicate them:
--   model-knowledge          -> the models
--   tensor-engine-knowledge  -> the engines that run them (llama.cpp/vLLM/KTransformers...)
--   docker-knowledge         -> THIS: the placement + runtime-measurement layer
--
-- One SQLite file; the linked-table graph:
--   waves -> findings -> {finding_sources} ; categories ; measurements
-- Every fact carries a wave_id (provenance); findings + sources carry a verified flag
-- (the study-swarm EXTERNAL_VERIFIER stage writes it). New waves APPEND; nothing is overwritten.

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

-- The core entity: a load-bearing finding / technique / constraint about placement or measurement.
CREATE TABLE IF NOT EXISTS findings (
  id                 INTEGER PRIMARY KEY,
  slug               TEXT UNIQUE NOT NULL,
  name               TEXT NOT NULL,        -- short title of the finding/technique
  category_id        INTEGER REFERENCES categories(id),
  kind               TEXT,                 -- technique|gotcha|constraint|benchmark|method|policy
  claim              TEXT,                 -- one-sentence load-bearing statement
  detail             TEXT,                 -- the explanation / how-to
  applies_to         TEXT,                 -- scope: windows-wsl2|linux|llama.cpp|vllm|moe|dense|nvme|pcie|all
  design_implication TEXT,                 -- what it means for the gpu-container planner/profiler
  metric             TEXT,                 -- headline number if any ("~12x energy", ">88% hit", "3.33% P95 error")
  confidence         TEXT,                 -- high|medium|low
  rig_relevance      INTEGER,              -- 0-5 relevance to THE rig (RTX 5090 / 32 GB / WSL2)
  status             TEXT,                 -- load-bearing|supporting|watch|refuted
  verified           INTEGER DEFAULT 0,    -- external verifier confirmed (retrieval + family-different)
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
  context       TEXT,                      -- in-container|host|wsl2|<model+config>
  tool          TEXT,                      -- nvidia-smi|cudaMemcpy-bench|fio|llama-bench ...
  source_file   TEXT,                      -- baselines/<file> provenance
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
  ('container-runtime',     'Container & runtime layer',          'Docker + NVIDIA Container Toolkit + WSL2 GPU passthrough; base images; CUDA toolkit; what changes inside a container (the "Docker" lane)', 10),
  ('hw-measurement',        'Hardware measurement methodology',   'How to measure VRAM / PCIe / NVMe (seq + rand QD1) / pinnable-RAM truthfully — especially from inside a WSL2 GPU container',              20),
  ('moe-placement',         'MoE expert placement & prefetch',    'Hot/warm/cold expert tiering, router-lookahead prefetch, staleness eviction, workload-representative calibration',                       30),
  ('dense-offload',         'Dense-model offload envelope',       'Partial RAM/NVMe offload throughput, the latency-vs-throughput tension, the sub-1-tok/s refusal cliff',                                  40),
  ('throughput-prediction', 'Throughput & memory prediction',     'KV/weight memory math (closed-form), roofline + measured calibration, prediction error bands, the receipt',                            50),
  ('refusal-receipt',       'Honest refusal & receipts',          'The >1 tok/s floor, contrastive refusal framing, the measured-receipt -> recalibration loop',                                          60);
