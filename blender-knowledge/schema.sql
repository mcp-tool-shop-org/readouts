-- blender-knowledge — KB #8 of the readouts monorepo
-- Primary entity: a RECIPE (an actionable, current Blender-4.x practice / API / pattern) + its
-- Blender-4-CURRENCY verdict. Scope: the studio's HEADLESS sprite-turnaround render pipeline
-- (import a TRELLIS-generated GLB -> render 8-direction sprites via `blender --background --python`
-- -> composite into a 2.5D game) + general game-asset prep.
-- DECISIVE AXIS: `currency` — the adversarial Blender-4.x verdict (solid / plausible / shaky / blender3_stale / wrong).
--   This is a CODE/practice KB, so license/VRAM/rig-fit (the sprites/model axes) do NOT apply.
-- Idempotent: CREATE ... IF NOT EXISTS; load_db.py replaces a wave's rows by wave_number.

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

-- PRIMARY ENTITY: a Blender-4.x recipe
CREATE TABLE IF NOT EXISTS recipes (
  id              INTEGER PRIMARY KEY,
  slug            TEXT UNIQUE NOT NULL,
  name            TEXT NOT NULL,
  category_id     INTEGER REFERENCES categories(id),
  what            TEXT,                 -- one-line: what it is
  how             TEXT,                 -- concrete, current Blender-4.x API / steps
  blender_version TEXT,                 -- e.g. "4.x", "4.2+", "4.2 EEVEE Next"
  gotchas         TEXT,
  studio_use      TEXT,                 -- how it serves the studio's render/asset pipeline

  -- Blender-4.x CURRENCY = the decisive axis (adversarial verifier verdict):
  currency        TEXT,                 -- solid | plausible | shaky | blender3_stale | wrong
  verify_note     TEXT,
  verified        INTEGER DEFAULT 0,    -- 1 if currency in (solid, plausible)
  status          TEXT,                 -- recommended | situational | avoid  (derived from currency)

  wave_id         INTEGER REFERENCES waves(id),
  created_date    TEXT
);

CREATE TABLE IF NOT EXISTS sources (
  id          INTEGER PRIMARY KEY,
  recipe_id   INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
  title       TEXT,
  url         TEXT NOT NULL,
  claim       TEXT,
  verified    INTEGER DEFAULT 0,        -- retrieval oracle / verifier confirmed
  wave_id     INTEGER REFERENCES waves(id)
);

CREATE VIRTUAL TABLE IF NOT EXISTS recipes_fts USING fts5(
  slug, name, what, how, gotchas, studio_use, category
);

CREATE INDEX IF NOT EXISTS idx_recipes_category ON recipes(category_id);
CREATE INDEX IF NOT EXISTS idx_recipes_currency ON recipes(currency);
CREATE INDEX IF NOT EXISTS idx_sources_recipe   ON sources(recipe_id);

-- ---- Views ----

-- the trustworthy half: current, verified Blender-4.x practice
CREATE VIEW IF NOT EXISTS v_recommended AS
  SELECT c.name AS category, r.name, r.blender_version, r.currency, r.verified, r.what
  FROM recipes r JOIN categories c ON c.id = r.category_id
  WHERE r.currency IN ('solid', 'plausible')
  ORDER BY c.sort, r.currency, r.name;

-- per-lane currency rollup
CREATE VIEW IF NOT EXISTS v_by_lane AS
  SELECT c.name AS category, COUNT(*) AS recipes,
         SUM(CASE WHEN r.currency='solid' THEN 1 ELSE 0 END) AS solid,
         SUM(r.verified) AS verified
  FROM recipes r JOIN categories c ON c.id = r.category_id
  GROUP BY c.name ORDER BY c.sort;

-- the flagged half: needs care (stale / shaky / wrong) — never silently trusted
CREATE VIEW IF NOT EXISTS v_flagged AS
  SELECT c.name AS category, r.name, r.currency, r.verify_note
  FROM recipes r JOIN categories c ON c.id = r.category_id
  WHERE r.currency IN ('shaky', 'blender3_stale', 'wrong')
  ORDER BY c.sort, r.name;

-- ---- Seed the 10 lanes (wave 1 = pipeline-core, wave 2 = asset-creation) ----
INSERT OR IGNORE INTO categories(slug, name, description, sort) VALUES
  ('headless-bpy',      'Headless rendering & bpy scripting', 'blender --background --python, the bpy API (ops/data/context), CLI render flags, reproducible scene setup, installing python modules, 3.x->4.x API changes — how the studio''s turnaround rig actually runs.', 10),
  ('render-engines',    'Render engines: EEVEE Next & Cycles', 'EEVEE Next (4.2+, replaced legacy EEVEE) vs Cycles, GPU backends, samples/denoising, film_transparent alpha output, fast sprite-render settings.', 20),
  ('color-management',  'Color management & tone mapping',    'AgX (4.0 default) / Standard / Filmic / Khronos PBR Neutral view transforms, exposure/look, OpenColorIO — and the AgX-washes-stylized-art fix for sprite renders.', 30),
  ('import-export',     'Import/export interchange',          'glTF/GLB (the TRELLIS mesh input), FBX, OBJ (rewritten C++ importer), USD; vertex colors/materials, axis/scale conventions, the bpy import operators.', 40),
  ('lighting-camera',   'Lighting & camera rigs',             'Area/Sun/HDRI lighting, camera-parented 3-point rigs, orthographic vs perspective cameras, the fixed 3/4-down ~35deg turnaround orbit, EEVEE Next shadows.', 50),
  ('mesh-ops',          'Mesh editing & cleanup',             'Decimate/Remesh/Boolean, normals & the 4.1 Smooth-by-Angle change, merge/fill/clean — preparing imported TRELLIS meshes for render & export.', 60),
  ('materials-baking',  'Materials & texture baking',         'Principled BSDF v2 (4.0 reorg), PBR setup, Cycles texture baking (Selected-to-Active, bake types), vertex-color->texture, UV & color-space for baking.', 70),
  ('geometry-nodes',    'Geometry Nodes (procedural)',        'The GN modifier/editor, scattering/instancing, named attributes, the Repeat/Simulation zones (4.x), procedural props & asset variation for the game world.', 80),
  ('rigging-animation', 'Rigging & animation',                'Armatures, Bone Collections (4.0, replaced bone layers), weighting, constraints/IK, drivers, the 4.4 Slotted Actions, glTF animation export to the engine.', 90),
  ('addons-pipeline',   'Add-ons & ecosystem',                'The 4.2 Extensions platform, bundled pipeline add-ons, the bpy add-on API, enabling add-ons headlessly, and the GPL licensing caveat for shipped add-ons.', 100);
