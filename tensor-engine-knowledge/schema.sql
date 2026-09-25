-- tensor-engine-knowledge :: schema
-- A long-lived, wave-appended knowledge base of TENSOR / INFERENCE / TRAINING ENGINES
-- (the software frameworks that run and train AI models — NOT the models themselves;
-- those live in the sibling model-knowledge KB). It records what each engine is, what
-- it's best at, the formats it runs, whether it's Blackwell/Windows-ready, how it's
-- licensed, how it fits this rig, and the source backing every claim.
--
-- One SQLite file; the "cluster" is the linked-table graph:
--   waves -> engines -> {engine_purposes -> purposes, sources} ; categories ; config_recipes
-- Every fact carries a wave_id (provenance) and engines/sources carry a verified flag
-- (the study-swarm EXTERNAL_VERIFIER stage writes it). New waves append; nothing is overwritten.

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

-- Every engine + how it runs, what it runs, how it's licensed, and how it fits this rig.
CREATE TABLE IF NOT EXISTS engines (
  id                 INTEGER PRIMARY KEY,
  slug               TEXT UNIQUE NOT NULL,
  name               TEXT NOT NULL,
  category_id        INTEGER REFERENCES categories(id),
  engine_type        TEXT,                 -- inference-server|runtime|kernel-lib|quant-format|quant-tool|training-framework|serving-layer|compiler
  developer          TEXT,
  language           TEXT,                 -- primary implementation language(s)
  latest_version     TEXT,
  release_date       TEXT,
  license            TEXT,
  commercial_use     TEXT,                 -- yes|no|conditional|unknown
  commercial_notes   TEXT,
  maturity_tier      TEXT,                 -- production|mature|stable|experimental|legacy|avoid
  platforms          TEXT,                 -- windows|linux|macos (combos)
  accelerators       TEXT,                 -- cuda|rocm|metal|cpu|vulkan|xpu
  model_formats      TEXT,                 -- gguf|safetensors|gptq|awq|exl2|exl3|fp8|nvfp4 (loads/produces)
  blackwell_ready    INTEGER,              -- 0/1/null : runs on RTX 5090 / sm_120 / CUDA 12.8+ on Windows today
  optimization_for   TEXT,                 -- throughput|latency|memory|flexibility|portability
  multi_gpu          TEXT,                 -- none|tensor-parallel|pipeline-parallel|data-parallel|fsdp|zero
  speed_note         TEXT,
  repo_url           TEXT,
  status             TEXT,                 -- recommended|runner-up|situational|legacy|avoid
  rig_fit            INTEGER,              -- 0-5 fit for THE rig (RTX 5090 / Blackwell / Windows / 32 GB VRAM + 64 GB RAM)
  studio_fit         INTEGER,              -- 0-5 fit for the local single-user studio workload (vs datacenter-only)
  download_priority  INTEGER,              -- lower = install first (derived from status + maturity)
  summary            TEXT,
  verified           INTEGER DEFAULT 0,    -- external verifier confirmed existence/license/specs
  verify_note        TEXT,
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

-- "best engine for what" matrix (many-to-many)
CREATE TABLE IF NOT EXISTS engine_purposes (
  engine_id  INTEGER NOT NULL REFERENCES engines(id) ON DELETE CASCADE,
  purpose_id INTEGER NOT NULL REFERENCES purposes(id) ON DELETE CASCADE,
  fitness    INTEGER,                      -- 0-5
  rank       INTEGER,                      -- 1 = best-in-class for this purpose
  use_tag    TEXT,                         -- nvidia|windows|local|server|training|reference
  note       TEXT,
  PRIMARY KEY (engine_id, purpose_id)
);

-- citation / evidence trail (study-swarm sourcing standard)
CREATE TABLE IF NOT EXISTS sources (
  id                INTEGER PRIMARY KEY,
  engine_id         INTEGER REFERENCES engines(id) ON DELETE CASCADE,
  subject           TEXT,                  -- when not tied to an engine row
  kind              TEXT,                  -- repo|docs|release-notes|benchmark|model-card|article|community
  title             TEXT,
  url               TEXT NOT NULL,
  claim             TEXT,                  -- one-sentence finding this source backs
  retrieved_date    TEXT,
  verified          INTEGER DEFAULT 0,     -- retrieval oracle confirmed it resolves
  finding_supported INTEGER,              -- groundedness: source actually states the claim
  verifier_note     TEXT,
  wave_id           INTEGER REFERENCES waves(id)
);

-- the "how to configure / optimize PROPERLY" companion (parallels comfy custom_nodes/workflows):
-- named, sourced config recipes, optional tools/resources.
CREATE TABLE IF NOT EXISTS config_recipes (
  id          INTEGER PRIMARY KEY,
  slug        TEXT UNIQUE,
  name        TEXT NOT NULL,
  category_id INTEGER REFERENCES categories(id),
  engine_id   INTEGER REFERENCES engines(id),   -- optional link to an engine
  kind        TEXT,                              -- recipe|tool|resource
  url         TEXT,
  body        TEXT,                              -- the recipe / note text
  wave_id     INTEGER REFERENCES waves(id)
);

-- full-text search over engines (matches model-knowledge's FTS5 convention)
CREATE VIRTUAL TABLE IF NOT EXISTS engines_fts USING fts5(
  slug, name, engine_type, summary, best_for, license, category, model_formats
);

CREATE INDEX IF NOT EXISTS idx_engines_category ON engines(category_id);
CREATE INDEX IF NOT EXISTS idx_engines_status   ON engines(status);
CREATE INDEX IF NOT EXISTS idx_sources_engine   ON sources(engine_id);
CREATE INDEX IF NOT EXISTS idx_ep_purpose       ON engine_purposes(purpose_id);
CREATE INDEX IF NOT EXISTS idx_recipes_category ON config_recipes(category_id);

-- convenience views ----------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_recommended AS
  SELECT c.name AS category, e.download_priority AS dl, e.name, e.engine_type,
         e.status, e.maturity_tier, e.license, e.commercial_use,
         e.blackwell_ready AS bw, e.platforms, e.rig_fit AS rig, e.studio_fit AS studio,
         e.verified, e.repo_url
  FROM engines e JOIN categories c ON c.id = e.category_id
  WHERE e.status IN ('recommended', 'runner-up')
  ORDER BY c.sort, e.download_priority, e.name;

CREATE VIEW IF NOT EXISTS v_best_for AS
  SELECT p.name AS purpose, e.name AS engine, ep.rank, ep.fitness, ep.use_tag,
         e.commercial_use, e.blackwell_ready AS bw, e.rig_fit AS rig, e.verified
  FROM engine_purposes ep
  JOIN engines e   ON e.id = ep.engine_id
  JOIN purposes p  ON p.id = ep.purpose_id
  ORDER BY p.name, ep.rank, ep.fitness DESC;

-- seed the wave-1 lanes -------------------------------------------------------
INSERT OR IGNORE INTO categories(slug, name, description, sort) VALUES
  ('llm-inference',       'LLM inference engines',             'Engines that load and run text/code/reasoning LLMs locally',                       10),
  ('llm-serving',         'Serving, batching & routing',       'Production serving / batching / routing / multi-model + embedding & reranker servers', 20),
  ('quantization',        'Quantization frameworks & formats', 'Quant algorithms, tools, and weight formats (GGUF/GPTQ/AWQ/EXL/FP8/FP4)',           30),
  ('attention-kernels',   'Attention backends & GPU kernels',  'FlashAttention/SageAttention/FlashInfer + attention & quantized-GEMM kernel libs',  40),
  ('training',            'Training & fine-tuning engines',    'Full / LoRA / QLoRA / RLHF / DPO training frameworks',                              50),
  ('diffusion-engines',   'Diffusion inference engines',       'Image/video diffusion runtimes & accelerators (the engine layer, not the models)', 60),
  ('runtime-foundations', 'Foundational runtimes & compilers', 'PyTorch/JAX/ONNX/TensorRT/MLX/ggml/Triton — what every other engine sits on',      70),
  ('structured-output',   'Structured output & constrained decoding', 'Grammar/JSON/tool-call engines that force LLMs to emit reliable structured output', 25),
  ('speech-engines',      'Speech engines (ASR / TTS runtimes)',      'Local speech-to-text & text-to-speech inference runtimes (the engine layer, not the models)', 55),
  ('profiling-bench',     'Profiling, benchmarking & observability',  'Tools to measure throughput / latency / VRAM and observe engines on this rig',  80);
