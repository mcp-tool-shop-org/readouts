-- model-knowledge :: schema
-- A long-lived, wave-appended knowledge base of local generative-AI models,
-- their best-fit purposes, the workflows that use them, and the sources that
-- back every claim. One SQLite file; the "cluster" is the linked-table graph:
--   waves -> models -> {model_purposes -> purposes, sources} ; categories ; workflows ; custom_nodes
-- Every fact carries a wave_id (provenance) and models/sources carry a verified flag
-- (the study-swarm EXTERNAL_VERIFIER stage writes it).

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

CREATE TABLE IF NOT EXISTS categories (
  id          INTEGER PRIMARY KEY,
  slug        TEXT UNIQUE NOT NULL,
  name        TEXT NOT NULL,
  description TEXT,
  sort        INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS models (
  id                 INTEGER PRIMARY KEY,
  slug               TEXT UNIQUE NOT NULL,
  name               TEXT NOT NULL,
  category_id        INTEGER REFERENCES categories(id),
  base_arch          TEXT,
  developer          TEXT,
  release_date       TEXT,
  params             TEXT,
  disk_size_gb       REAL,
  min_vram_gb        REAL,
  recommended_vram_gb REAL,
  runs_on_32gb       INTEGER,              -- 0/1
  license            TEXT,
  commercial_use     TEXT,                 -- yes|no|conditional|unknown
  commercial_notes   TEXT,
  quality_tier       TEXT,                 -- frontier|strong|solid|legacy|avoid
  speed_note         TEXT,
  repo_url           TEXT,
  status             TEXT,                 -- recommended|runner-up|situational|legacy|avoid
  game_asset_fit     INTEGER,              -- 0-5
  marketing_fit      INTEGER,              -- 0-5
  download_priority  INTEGER,              -- lower = grab first (derived from status+tier)
  summary            TEXT,
  verified           INTEGER DEFAULT 0,    -- external verifier confirmed existence/specs
  verify_note        TEXT,
  cloud_feasible     TEXT,                 -- yes|partial|local|unknown (Comfy Cloud allowlist axis, wave 6+)
  cloud_note         TEXT,                 -- why / constraints / measured facts for the cloud axis
  wave_id            INTEGER REFERENCES waves(id),
  created_date       TEXT
);

CREATE TABLE IF NOT EXISTS purposes (
  id          INTEGER PRIMARY KEY,
  slug        TEXT UNIQUE NOT NULL,
  name        TEXT NOT NULL,
  category_id INTEGER REFERENCES categories(id),
  description TEXT
);

-- "best model for what" matrix (many-to-many)
CREATE TABLE IF NOT EXISTS model_purposes (
  model_id   INTEGER NOT NULL REFERENCES models(id) ON DELETE CASCADE,
  purpose_id INTEGER NOT NULL REFERENCES purposes(id) ON DELETE CASCADE,
  fitness    INTEGER,                      -- 0-5
  rank       INTEGER,                      -- 1 = best-in-class for this purpose
  use_tag    TEXT,                         -- game-asset|marketing|both
  note       TEXT,
  PRIMARY KEY (model_id, purpose_id)
);

-- citation / evidence trail (study-swarm sourcing standard)
CREATE TABLE IF NOT EXISTS sources (
  id                INTEGER PRIMARY KEY,
  model_id          INTEGER REFERENCES models(id) ON DELETE CASCADE,
  subject           TEXT,                  -- when not tied to a model row
  kind              TEXT,                  -- model-card|benchmark|leaderboard|release-notes|paper|community
  title             TEXT,
  url               TEXT NOT NULL,
  claim             TEXT,                  -- one-sentence finding this source backs
  retrieved_date    TEXT,
  verified          INTEGER DEFAULT 0,     -- retrieval oracle confirmed it resolves
  finding_supported INTEGER,               -- groundedness: source actually states the claim
  verifier_note     TEXT,
  wave_id           INTEGER REFERENCES waves(id)
);

CREATE TABLE IF NOT EXISTS custom_nodes (
  id        INTEGER PRIMARY KEY,
  name      TEXT NOT NULL,
  url       TEXT,
  note      TEXT,
  essential INTEGER DEFAULT 0,
  wave_id   INTEGER REFERENCES waves(id)
);

CREATE TABLE IF NOT EXISTS workflows (
  id              INTEGER PRIMARY KEY,
  slug            TEXT UNIQUE,
  name            TEXT NOT NULL,
  category_id     INTEGER REFERENCES categories(id),
  kind            TEXT,                    -- workflow | workflow-source
  file_path       TEXT,                    -- local path under workflows/ if saved
  url             TEXT,
  description     TEXT,
  required_models TEXT,
  status          TEXT,
  wave_id         INTEGER REFERENCES waves(id)
);

-- full-text search over models (matches repo-knowledge's FTS5 convention)
CREATE VIRTUAL TABLE IF NOT EXISTS models_fts USING fts5(
  slug, name, base_arch, summary, best_for, license, category
);

CREATE INDEX IF NOT EXISTS idx_models_category ON models(category_id);
CREATE INDEX IF NOT EXISTS idx_models_status   ON models(status);
CREATE INDEX IF NOT EXISTS idx_sources_model   ON sources(model_id);
CREATE INDEX IF NOT EXISTS idx_mp_purpose      ON model_purposes(purpose_id);

-- convenience views ----------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_recommended AS
  SELECT c.name AS category, m.download_priority AS dl, m.name, m.base_arch,
         m.status, m.quality_tier, m.license, m.commercial_use,
         m.min_vram_gb AS vram, m.game_asset_fit AS game, m.marketing_fit AS mkt,
         m.verified, m.repo_url
  FROM models m JOIN categories c ON c.id = m.category_id
  WHERE m.status IN ('recommended', 'runner-up')
  ORDER BY c.sort, m.download_priority, m.name;

CREATE VIEW IF NOT EXISTS v_best_for AS
  SELECT p.name AS purpose, m.name AS model, mp.rank, mp.fitness, mp.use_tag,
         m.commercial_use, m.min_vram_gb AS vram, m.verified
  FROM model_purposes mp
  JOIN models m   ON m.id = mp.model_id
  JOIN purposes p ON p.id = mp.purpose_id
  ORDER BY p.name, mp.rank, mp.fitness DESC;

-- seed the wave-1 domains -----------------------------------------------------
INSERT OR IGNORE INTO categories(slug, name, description, sort) VALUES
  ('image-base',    'Image — base models',        'Text-to-image base checkpoints',                                     10),
  ('image-edit',    'Image — editing',            'Instruction / in-context image editing',                             15),
  ('image-control', 'Image — control & utility',  'ControlNet/IP-Adapter, inpaint, upscalers, detailers, LoRA training', 20),
  ('video',         'Video generation',           'Text/image-to-video models',                                         30),
  ('3d',            '3D asset generation',        'Image/text-to-3D mesh + texture',                                    40),
  ('audio',         'Audio generation',           'Music, SFX/foley, TTS/voice',                                        50),
  ('llm',           'Local LLM + vision',         'Ollama text/code/reasoning + vision/captioning',                     60),
  ('caption',       'Captioning & tagging',       'VLM captioners + booru taggers for dataset building',                65),
  ('comfy',         'ComfyUI + workflows',        'ComfyUI runtime, custom nodes, workflow sources',                    70);
