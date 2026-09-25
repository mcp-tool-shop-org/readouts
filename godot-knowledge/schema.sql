-- godot-knowledge — KB #7 of the readouts monorepo
-- Primary entity: a RECIPE (an actionable, current Godot-4 dev practice / API / pattern) + its
-- Godot-4-CURRENCY verdict. Scope: building a 2.5D turn-based tactical RPG in Godot 4.
-- DECISIVE AXIS: `currency` — the adversarial Godot-4 verdict (solid / plausible / shaky / godot3_stale / wrong).
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

-- PRIMARY ENTITY: a Godot-4 recipe
CREATE TABLE IF NOT EXISTS recipes (
  id            INTEGER PRIMARY KEY,
  slug          TEXT UNIQUE NOT NULL,
  name          TEXT NOT NULL,
  category_id   INTEGER REFERENCES categories(id),
  what          TEXT,                 -- one-line: what it is
  how           TEXT,                 -- concrete, current Godot-4 API / steps
  godot_version TEXT,                 -- e.g. "4.x", "4.3+"
  gotchas       TEXT,

  -- Godot-4 CURRENCY = the decisive axis (adversarial verifier verdict):
  currency      TEXT,                 -- solid | plausible | shaky | godot3_stale | wrong
  verify_note   TEXT,
  verified      INTEGER DEFAULT 0,    -- 1 if currency in (solid, plausible)
  status        TEXT,                 -- recommended | situational | avoid  (derived from currency)

  wave_id       INTEGER REFERENCES waves(id),
  created_date  TEXT
);

CREATE TABLE IF NOT EXISTS sources (
  id          INTEGER PRIMARY KEY,
  recipe_id   INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
  title       TEXT,
  url         TEXT NOT NULL,
  claim       TEXT,
  verified    INTEGER DEFAULT 0,      -- retrieval oracle / verifier confirmed
  wave_id     INTEGER REFERENCES waves(id)
);

CREATE VIRTUAL TABLE IF NOT EXISTS recipes_fts USING fts5(
  slug, name, what, how, gotchas, category
);

CREATE INDEX IF NOT EXISTS idx_recipes_category ON recipes(category_id);
CREATE INDEX IF NOT EXISTS idx_recipes_currency ON recipes(currency);
CREATE INDEX IF NOT EXISTS idx_sources_recipe   ON sources(recipe_id);

-- ---- Views ----

-- the trustworthy half: current, verified Godot-4 practice
CREATE VIEW IF NOT EXISTS v_recommended AS
  SELECT c.name AS category, r.name, r.godot_version, r.currency, r.verified, r.what
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
  WHERE r.currency IN ('shaky', 'godot3_stale', 'wrong')
  ORDER BY c.sort, r.name;

-- ---- Seed the 6 lanes ----
INSERT OR IGNORE INTO categories(slug, name, description, sort) VALUES
  ('architecture',        'Project & scene architecture',  'Godot 4 scene/node composition, autoload singletons, signals/event-bus, the Resource (.tres) data-driven pattern for units/abilities/parts, state management, save/load.', 10),
  ('grid-movement',       'Grid & tactical movement',      'TileMapLayer grid, coordinate systems, AStarGrid2D vs flood-fill movement range, range highlighting, cursor/selection, + the open-source Godot-4 tactical-RPG frameworks (license + 4.x compat).', 20),
  ('turn-combat',         'Turn-based combat architecture','Turn/initiative ordering, action-point economy, the turn state machine, deterministic damage/effects, ability/status as Resources, part/called-shot targeting, enemy AI.', 30),
  ('rendering-2.5d',      'Rendering & 2.5D sprites',      '2D rendering of painterly sprites, Y-sort/depth, 2D lighting (CanvasModulate/Light2D/normal maps/glow), AnimatedSprite2D vs AnimationPlayer, atlases, the renderer choice.', 40),
  ('ui-tactical',         'Tactical UI (legibility)',      'Control nodes & containers, the Theme system, the legibility-critical HUD (shown outcomes, loot panels, collateral indicator, range/AP), tooltips, responsive layout.', 50),
  ('tooling-test-export', 'Tooling, test, export, CI',     'GUT unit testing, debugging/profiling, headless + GitHub-Actions CI, export templates + Windows/Steam, performance for tactical grids, the Godot .gitignore + version control, the LLM-crew data-authoring workflow.', 60);
