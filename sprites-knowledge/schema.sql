-- sprites-knowledge — KB #5 of the readouts monorepo
-- Primary entity: a RECIPE (a sprite-pipeline procedure or model choice + its proof).
-- Proven vs unproven is encoded by evidence_strength (ordinal) + status + verified.
-- Idempotent: CREATE ... IF NOT EXISTS + INSERT OR IGNORE. load_db.py replaces a wave's rows.

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meta (
  key   TEXT PRIMARY KEY,
  value TEXT
);

CREATE TABLE IF NOT EXISTS waves (
  id              INTEGER PRIMARY KEY,
  wave_number     INTEGER NOT NULL UNIQUE,
  title           TEXT NOT NULL,
  dispatched_date TEXT NOT NULL,
  domain_scope    TEXT,
  agent_count     INTEGER,
  verifier_note   TEXT,
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

-- PRIMARY ENTITY: a sprite recipe (procedure / model choice + proof)
CREATE TABLE IF NOT EXISTS recipes (
  id                 INTEGER PRIMARY KEY,
  slug               TEXT UNIQUE NOT NULL,
  name               TEXT NOT NULL,
  category_id        INTEGER REFERENCES categories(id),
  kind               TEXT,                 -- model | technique | workflow | post-process | pipeline | eval
  engine_family      TEXT,                 -- comfyui | blender | python | trellis2 | sd-webui | custom | n/a
  applicable_to      TEXT,                 -- game-sprite | turnaround | animation | tile | both
  base_model_family  TEXT,                 -- SDXL | Flux | Chroma | TRELLIS | n/a
  claim              TEXT,                 -- one-line load-bearing statement
  summary            TEXT,                 -- the how / what
  design_implication TEXT,                 -- what it means for the studio's sprite pipeline

  -- reproducibility / proof (PIN_PER_STEP):
  evidence_strength  TEXT,                 -- ORDINAL: measured-on-rig > reproduced-from-source > single-reported-run > community-claim > untested
  seed               TEXT,
  num_runs           INTEGER,
  variance_note      TEXT,
  tuning_budget      TEXT,
  measured_conditions TEXT,                -- the exact rig/env when evidence_strength = measured-on-rig

  -- cross-KB seams (never restate measured numbers that live in another KB):
  engine_recipe_ref  TEXT,                 -- -> tensor-engine-knowledge config/recipe slug
  base_model_slug    TEXT,                 -- -> model-knowledge model slug

  -- multi-stage pipeline chaining:
  predecessor_recipe_id INTEGER REFERENCES recipes(id),
  stage_order        INTEGER,

  -- license (THE DECISIVE AXIS) + fit:
  license            TEXT,
  commercial_use     TEXT,                 -- yes | conditional | no | unknown
  commercial_notes   TEXT,
  vram_gb            TEXT,                  -- approx peak (ranges allowed, e.g. "15-24")
  rig_fit            INTEGER,               -- 0-5 fit for RTX 5090 32GB
  studio_fit         INTEGER,               -- 0-5 fit for commercial 2.5D JRPG sprite production
  download_priority  INTEGER,

  status             TEXT,                  -- recommended | runner-up | situational | legacy | superseded | avoid
  verified           INTEGER DEFAULT 0,     -- external/ retrieval verifier confirmed
  verify_note        TEXT,
  license_correction TEXT,                  -- verifier's license fix, if any
  superseded_by      INTEGER REFERENCES recipes(id),

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

CREATE TABLE IF NOT EXISTS recipe_purposes (
  recipe_id   INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  purpose_id  INTEGER NOT NULL REFERENCES purposes(id) ON DELETE CASCADE,
  fitness     INTEGER,                      -- 0-5
  rank        INTEGER,                      -- 1 = best-in-class
  use_tag     TEXT,
  note        TEXT,
  PRIMARY KEY (recipe_id, purpose_id)
);

CREATE TABLE IF NOT EXISTS recipe_hparams (
  id        INTEGER PRIMARY KEY,
  recipe_id INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  name      TEXT NOT NULL,
  value     TEXT,
  unit      TEXT,
  required  INTEGER DEFAULT 0,
  note      TEXT
);

CREATE TABLE IF NOT EXISTS recipe_failures (
  id          INTEGER PRIMARY KEY,
  recipe_id   INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
  symptom     TEXT NOT NULL,
  cause       TEXT,
  remediation TEXT,
  recipe_field TEXT,
  severity    TEXT,                         -- blocker | quality | cosmetic
  wave_id     INTEGER REFERENCES waves(id)
);

CREATE TABLE IF NOT EXISTS recipe_evals (
  id              INTEGER PRIMARY KEY,
  recipe_id       INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
  eval_kind       TEXT,                     -- visual-inspection | metric | ai-judge | human-ab
  metric          TEXT,                     -- LPIPS | SSIM | SigLIP2-score | perceptual ...
  harness         TEXT,
  result          TEXT,
  threshold       TEXT,
  accepted        INTEGER,
  note            TEXT
);

CREATE TABLE IF NOT EXISTS datasets (
  id           INTEGER PRIMARY KEY,
  slug         TEXT UNIQUE NOT NULL,
  name         TEXT NOT NULL,
  kind         TEXT,                        -- reference-sprites | training-set | eval-set | hdri
  count        INTEGER,
  description  TEXT,
  license      TEXT,
  url          TEXT,
  verified     INTEGER DEFAULT 0,
  wave_id      INTEGER REFERENCES waves(id),
  created_date TEXT
);

CREATE TABLE IF NOT EXISTS recipe_datasets (
  recipe_id  INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  dataset_id INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
  role       TEXT,                          -- training | reference | eval
  note       TEXT,
  PRIMARY KEY (recipe_id, dataset_id, role)
);

CREATE TABLE IF NOT EXISTS sources (
  id                INTEGER PRIMARY KEY,
  recipe_id         INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
  subject           TEXT,
  kind              TEXT,                   -- paper | docs | github | model-card | blog | video | community | receipt
  title             TEXT,
  authors           TEXT,
  year              TEXT,
  identifier        TEXT,                   -- arXiv:NNNN | DOI
  url               TEXT NOT NULL,
  claim             TEXT,                   -- the one fact this source backs
  retrieved_date    TEXT,
  verified          INTEGER DEFAULT 0,      -- retrieval oracle confirmed it resolves
  finding_supported TEXT,                   -- SUPPORTED | PARTIAL | NOT_SUPPORTED | CANT_TELL
  verifier_note     TEXT,
  target_table      TEXT,                   -- optional: recipe_hparams | recipe_failures | recipe_evals
  target_id         INTEGER,
  wave_id           INTEGER REFERENCES waves(id)
);

CREATE VIRTUAL TABLE IF NOT EXISTS recipes_fts USING fts5(
  slug, name, engine_family, applicable_to, base_model_family, summary, claim, category
);

CREATE INDEX IF NOT EXISTS idx_recipes_category ON recipes(category_id);
CREATE INDEX IF NOT EXISTS idx_recipes_status   ON recipes(status);
CREATE INDEX IF NOT EXISTS idx_recipes_engine   ON recipes(engine_family);
CREATE INDEX IF NOT EXISTS idx_recipes_evidence ON recipes(evidence_strength);
CREATE INDEX IF NOT EXISTS idx_sources_recipe   ON sources(recipe_id);
CREATE INDEX IF NOT EXISTS idx_rp_purpose       ON recipe_purposes(purpose_id);
CREATE INDEX IF NOT EXISTS idx_hparams_recipe   ON recipe_hparams(recipe_id);

-- ---- Views ----

-- recommended/runner-up recipes, any evidence level
CREATE VIEW IF NOT EXISTS v_recommended AS
  SELECT c.name AS category, r.download_priority AS dl, r.name, r.engine_family,
         r.applicable_to, r.status, r.evidence_strength, r.license, r.commercial_use,
         r.vram_gb, r.rig_fit AS rig, r.studio_fit AS studio, r.verified
  FROM recipes r JOIN categories c ON c.id = r.category_id
  WHERE r.status IN ('recommended', 'runner-up')
  ORDER BY c.sort, r.download_priority, r.name;

CREATE VIEW IF NOT EXISTS v_best_for AS
  SELECT p.name AS purpose, r.name AS recipe, rp.rank, rp.fitness, rp.use_tag,
         r.applicable_to, r.evidence_strength, r.commercial_use, r.rig_fit AS rig, r.verified
  FROM recipe_purposes rp
  JOIN recipes r ON r.id = rp.recipe_id
  JOIN purposes p ON p.id = rp.purpose_id
  ORDER BY p.name, rp.rank, rp.fitness DESC;

CREATE VIEW IF NOT EXISTS v_pipeline AS
  SELECT r.id, r.slug, r.name, r.stage_order, r.predecessor_recipe_id,
         pre.name AS builds_on, r.applicable_to, r.engine_family
  FROM recipes r LEFT JOIN recipes pre ON pre.id = r.predecessor_recipe_id
  WHERE r.predecessor_recipe_id IS NOT NULL OR r.stage_order IS NOT NULL
  ORDER BY r.applicable_to, r.stage_order;

-- sprites-specific: the PROVEN half (validated on this rig)
CREATE VIEW IF NOT EXISTS v_proven AS
  SELECT c.name AS category, r.name, r.engine_family, r.applicable_to, r.status,
         r.commercial_use, r.vram_gb, r.measured_conditions, r.verified
  FROM recipes r JOIN categories c ON c.id = r.category_id
  WHERE r.evidence_strength = 'measured-on-rig'
  ORDER BY c.sort, r.name;

-- sprites-specific: the RESEARCH half (study-swarm sourced, not yet rig-measured)
CREATE VIEW IF NOT EXISTS v_research AS
  SELECT c.name AS category, r.name, r.engine_family, r.applicable_to, r.status,
         r.evidence_strength, r.license, r.commercial_use, r.verified
  FROM recipes r JOIN categories c ON c.id = r.category_id
  WHERE r.evidence_strength IS NULL OR r.evidence_strength <> 'measured-on-rig'
  ORDER BY c.sort, r.status, r.name;

-- ---- Seed the 7 lanes ----
INSERT OR IGNORE INTO categories(slug, name, description, sort) VALUES
  ('mesh-360',            'Mesh-path 360 (image to 3D to multi-view)', 'Single image -> textured 3D mesh -> rendered multi-direction sprites. The recon-model landscape + the proven TRELLIS.2 path.', 10),
  ('render-light',        'Render & lighting',                          'Blender headless render: camera-parented rig, color-management/tonemap per character value, render passes, outline/toon.', 20),
  ('downsample-finish',   'Downsample & pixel finish',                  '512px master -> 48/64px game sprite: Lanczos/area downscale, foot-anchor, union bbox, quantization/dithering, palette.', 30),
  ('nvs-direct',          'NVS-direct turnaround (no mesh)',            'Image -> multiple consistent 2D views via multi-view diffusion / novel-view synthesis. License-decisive (Zero123 lineage is NC).', 40),
  ('sheet-direct',        'Diffusion sprite-sheet direct',              'Text/image -> sprite sheet or 8-direction set directly via diffusion: charturn + pixel-art LoRAs, ControlNet pose sheets.', 50),
  ('eval-qa',             'Sprite evaluation / QA gate',                'Grounded evaluators (SigLIP2/CLIP), turnaround-consistency + perceptual metrics, AI-judge gates for an automatable sprite verifier.', 60),
  ('animation-locomotion','Animation & locomotion',                     'Walk cycles / locomotion / frame sequences for sprites: auto-rig + animated render, image-to-animation diffusion, interpolation.', 70),
  ('prompt-craft',        'Prompt craft & text encoders',               'How each text encoder (CLIP / T5 / Qwen) actually reads a prompt: token & character truncation limits, what it attends to, depictability, negative prompts, and the anti-patterns -- the rules that stop a session from prose-dumping an encoder.', 80);
