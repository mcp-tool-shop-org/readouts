-- sprite-motion-knowledge — KB #9 of the readouts monorepo
-- Primary entity: a RECIPE (a sprite-MOTION / character-animation procedure or model/tool choice + its proof).
-- The animation layer atop sprites-knowledge (KB #5): motion truth (rig/mesh/proxy) -> AI polish -> sprite-sheet export -> verify.
-- Proven (rig-measured) vs research (study-swarm) is encoded by evidence_strength (ordinal) + status + verified.
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
  predecessor_recipe_id INTEGER REFERENCES recipes(id) ON DELETE SET NULL,
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
  superseded_by      INTEGER REFERENCES recipes(id) ON DELETE SET NULL,

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
  ('motion-arch',   'Motion architecture & contracts', 'The rig-truth-first doctrine: motion truth -> AI polish -> sprite-sheet export; per-character animation contracts/manifests (views, frame counts, loop flags, anchors, layers); the 3-lane production model; one shared motion cage rendered per-direction, NOT 80 independent images.', 10),
  ('rigging',       'Rigging & skeletons',             'Blender armatures + 2.5D proxy/mesh rigs as the deterministic motion source: bone hierarchies, hand->weapon_grip->weapon_tip rigid-attach chains (the fix for per-view weapon drift), auto-riggers (UniRig/Rigify/AccuRIG/Auto-Rig Pro/Mixamo).', 20),
  ('ai-motion',     'AI motion models',                'Character-animation models that propose or drive motion: video-diffusion + pose-conditioned generation, AnimateDiff, image-to-animation DiTs. LICENSE-DECISIVE (research/academic-only weights are the trap; base-model license is inherited).', 30),
  ('inbetween',     'Inbetweening & interpolation',    'Keyframe -> tween frame generation: FILM, RIFE/Practical-RIFE, optical-flow interpolation; multiply sparse keyposes into a smooth cycle; large-displacement vs smooth-motion tradeoffs.', 40),
  ('cloud-workers', 'Cloud GPU workers',               'Run bigger-than-VRAM animation/edit models as a pipeline worker, not a website: RunPod / Modal / fal.ai / Replicate / HF Inference Endpoints; ComfyUI-as-serverless, cold starts, model caching, cost. Source-of-truth stays in the repo.', 50),
  ('combat-craft',  'Combat animation craft',          'The designed-not-generated principles: anticipation -> active/hit frame -> follow-through -> recovery; smears, hit-stop, readable silhouettes, attack timing -- the animation principles that make combat game-readable.', 60),
  ('motion-verify', 'Motion verification & QA',        'The local verifier gate for motion: root/anchor stability, foot-contact (no slide), hand-to-weapon attachment + weapon length/tip continuity, no frame-to-frame face mutation, silhouette readability, canvas/size consistency; automatable temporal-consistency metrics.', 70),
  -- wave 2 — commercial motion sources & data (the CONTENT/DATA layer; license-decisive)
  ('mocap-libraries',  'Commercial mocap & animation libraries', 'Ready-made mocap/animation packs licensed for commercial games: Mixamo, Reallusion ActorCore, Rokoko, marketplace/asset-store packs — coverage, license terms for shipping, FBX/BVH formats, humanoid-skeleton fit.', 80),
  ('mocap-datasets',   'Open mocap datasets & license traps',    'Open/research motion-capture datasets and their licenses: CMU, AMASS, LAFAN1, Motion-X, 100STYLE, HumanML3D — which are commercial-safe vs RESEARCH-ONLY (the NC trap that poisons every downstream model trained on them).', 90),
  ('motion-gen',       'Text-to-motion & motion synthesis',      'Generative motion models (text->motion / motion synthesis): MDM, MoMask, MotionGPT, T2M-GPT, OmniControl — existence + license-decisive (many TRAIN on AMASS and inherit its non-commercial terms in the output).', 100),
  ('driving-video',    'Driving & reference video sources',      'Sourcing commercial-safe driving/reference video for pose-transfer animation, the license implications, and the shoot-your-own-reference recipe (always license-clean).', 110),
  ('retarget',         'Retargeting onto stylized rigs',         'Getting external mocap onto the studio stylized / non-humanoid 2.5D rigs: Blender Rokoko / Auto-Rig-Pro remap, UE5 IK Retargeter, proportion mismatch (the JRPG / exotic-species silhouette problem), foot-IK cleanup.', 120),
  ('motion-licensing', 'Motion data licensing doctrine',         'How motion-capture DATA licensing actually works for shipping a commercial game: royalty-free vs no-raw-redistribution vs research-only; whether you may train a model on it; Mixamo must-incorporate; the AMASS-NC downstream-poison trap.', 130),
  -- wave 3 — painterly repaint & temporal coherence (the AI-POLISH stage: mesh/proxy render -> house style, held across frames)
  ('repaint-controlnet',  'Structure-preserving repaint (ControlNet)', 'Repaint a 3D mesh/proxy render to the painterly house style while HOLDING structure: ControlNet depth/lineart/canny/tile/softedge stacks on Qwen-Image-Edit-2511; denoise + control-strength schedules. The mesh-render -> painterly-skin core that closes the §D style gap.', 140),
  ('style-injection',     'House-style injection',                    'Applying the painterly house style during repaint: the studio sfhd_style LoRA, IP-Adapter style-reference, img2img denoise ranges, content/style separation, palette/color-grade matching to the approved look.', 150),
  ('identity-preserve',   'Identity & face preservation',             'Keeping the APPROVED face/character through repaint + across frames: face-preserve (de-lit), IP-Adapter-FaceID, inpaint-only / low-denoise face regions, ArcFace-guided locks. License-aware (InsightFace weights are NC).', 160),
  ('weapon-composite',    'Rigid-weapon compositing',                 'The §D Lane B: segment the mesh rigid weapon per view, align it to the painterly view, composite + harmonize (ControlNet-depth / inpaint / tile) — keep the weapon RIGID through the repaint.', 170),
  ('temporal-coherence',  'Cross-frame & cross-direction coherence',  'The motion-specific hard part: style + identity stable across 8 directions AND animation frames — batch-consistent seeds, reference-frame propagation, AnimateDiff / video temporal modules for repaint, flicker/shimmer reduction, optical-flow-guided consistency.', 180),
  ('repaint-eval',        'Repaint QA gate',                          'QA specific to repaint: identity preserved (face-distance), weapon continuity, style-match to the house reference (SigLIP/CLIP), no over-smoothing / detail-loss, palette adherence. Extends motion-verify to the repaint stage.', 190);
