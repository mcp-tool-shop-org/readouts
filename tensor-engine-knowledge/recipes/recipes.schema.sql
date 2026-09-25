-- tensor-engine-knowledge :: PROPOSED typed recipe layer  (engine-room knowledge side)
-- =====================================================================================
-- STATUS: PROPOSAL — not yet merged into ../schema.sql. For Mike's review before integration.
--
-- WHY THIS EXISTS
-- The KB holds 177 PROSE config_recipes (freeform `body`, kind in {recipe,baseline}).
-- engine-room (the executor — a SEPARATE org tool, mcp-tool-shop-org/engine-room) needs
-- to READ a recipe and materialize / launch / measure it. That needs structure. This
-- layer is the KNOWLEDGE half of the Parnas split: the verified, sourced, ABSTRACT recipe
-- + its measured baseline TARGETS + its declared compensators. The ACTION half (the
-- resolved lock, the ledger, the live instance_id, the reconcile loop, the measurement
-- harness) lives in engine-room, NOT here — a knowledge DB must not carry rig-state that
-- changes when a driver bumps (driver already moved 581.xx -> 610.47 between waves).
--
-- DESIGN IS POST-ADVERSARIAL. Every non-obvious table answers a specific break the
-- engine-room design study-swarm's adversarial pass found in the live engines.db
-- (run wf_46ad6900-7d9, 2026-06-06):
--   * recipe_kind enum + recipe_targets  -> HETEROGENEITY break #1: 22 kernel-lib rows
--     (SageAttention, Nunchaku, cuDNN-SDPA, torchao; several rig_fit=5) are MODIFIERS,
--     not port-serving engines; their value is a DELTA vs another recipe (SA: +8% @1024²,
--     +29% @2048²), not a self-baseline. "What port does SageAttention serve?" -> none.
--   * recipe_kind 'batch-producer' + per-recipe measured_axis -> break #2: quantizers
--     (nvidia-modelopt NVFP4, GGUF-imatrix) and trainers (kohya/Unsloth) TERMINATE after
--     writing a file; metric is perplexity / bits / it-s / wall-clock, NOT tok/s.
--   * recipe_baselines keyed by (recipe, MODEL, ctx) -> break #3: the SAME llama.cpp/Ollama
--     binary measured 138 (qwen3.6:35b-a3b) vs 60 (gemma4:31b) vs 57 (qwen3.6:27b) tok/s;
--     a recipe-only baseline false-halts or false-passes. (Confirmed by wave-4/5 data.)
--   * recipe_baselines.compat_band -> repro-drift: hash a SEMANTIC band (driver>=R570,
--     cuda_toolkit==12.8), NOT the literal driver (581->610.47 already happened = treadmill).
--   * recipe_artifacts.store_expect + sha256 -> repro-drift: cu128 wheel URLs are DEAD
--     (torch 2.12 dropped the channel — the KB says so verbatim in 3 rows); a URL+hash
--     against a CURATED index 404s. Only 'mirror'/'local-vendored' pins are reproducible.
--   * recipe_artifacts.abi_tuple + recipe_constraints 'abi_equal'/'defect_floor' -> the
--     MOST COMMON Blackwell failure is a wheel/torch ABI mismatch that passes every >=
--     capability check then DLL-fails (e.g. SageAttention wheel pinned to a torch nightly
--     date); needs cross-artifact EQUALITY, not inequality. defect_floor names known-bad
--     versions (wsl2>=2.7.0 WDDM hang) distinctly from capability floors.
--   * recipe_golden.modality -> diffusion/speech have NO torch.allclose golden (seed/
--     scheduler-sensitive; SA itself trades quality for speed); gate must be pluggable
--     (numeric | perceptual SSIM/CLIP | WER | audio-fingerprint | file-hash).
--   * recipe_compensators.compensatable enum -> no-skip standard: NAME even the
--     non-undoable ops. PATH mutation on Windows is a shared 1024-char registry value
--     (revert-under-concurrency corrupts it) -> prefer per-instance shims; `wsl --update`
--     is machine-global (can't downgrade WSL for one engine) -> 'non-compensatable',
--     owner=human, undo=NULL — named, not omitted.
--   * verified + resolvable_* columns -> config_recipes has NO verified column today;
--     and the KB's family-different verifier checks PROSE GROUNDEDNESS (grounded entailment),
--     never whether a pinned artifact still INSTALLS. Resolvability is a SEPARATE
--     deterministic floor in the KB's own defense-in-depth tradition (existence floor /
--     numeric floor / NLI floor -> + a recipe-RESOLVABILITY floor): refute-or-abstain,
--     a 404/yanked artifact is a PROOF, else abstain — it cannot add a false-confirm.
--
-- All CREATE ... IF NOT EXISTS so this is idempotent and safe to fold into schema.sql.
-- FK refs (categories, engines, waves) assume the existing schema.sql tables are present.

PRAGMA foreign_keys = ON;

-- The spine: one row per recipe. Polymorphic over recipe_kind.
CREATE TABLE IF NOT EXISTS recipes (
  id            INTEGER PRIMARY KEY,
  slug          TEXT UNIQUE NOT NULL,
  name          TEXT NOT NULL,
  engine_slug   TEXT,                 -- the primary engine this recipe concerns (-> engines.slug); NULL for cross-engine modifiers
  category_id   INTEGER REFERENCES categories(id),
  -- THE polymorphism (heterogeneity breaks #1/#2). Not everything serves a port.
  recipe_kind   TEXT NOT NULL CHECK (recipe_kind IN
                  ('launchable-server','batch-producer','modifier','router-fleet')),
  -- the pluggable executor provider; NULL for 'modifier' (inherits its target's backend)
  backend_kind  TEXT CHECK (backend_kind IS NULL OR backend_kind IN
                  ('native-win-compile','wsl2-docker','portable-bundle','venv',
                   'onnx-compile','python-proxy','raw-cmd')),
  -- the measured axis is PER-RECIPE, not hard-coded tok/s (break #2)
  measured_axis TEXT CHECK (measured_axis IS NULL OR measured_axis IN
                  ('tok_s','it_s','s_per_img','perplexity','bits_per_weight','wer',
                   'build_wall_clock','delta_pct','none')),
  toolchain_ref TEXT,                 -- shared toolchain profile (e.g. cuda-12.8-sm120); EasyBuild-style reuse
  summary       TEXT,                 -- one-line human summary
  body          TEXT,                 -- the prose recipe (migrated from config_recipes.body; human-readable source of truth)
  -- knowledge-quality signals (config_recipes has neither today)
  verified            INTEGER DEFAULT 0,   -- groundedness verifier confirmed the prose matches a source
  verify_note         TEXT,
  resolvable_ok       INTEGER,             -- resolvability floor: do ALL pinned artifacts still resolve? (NULL=unchecked)
  resolvable_checked  TEXT,                -- ISO date of last resolvability check
  executable          INTEGER DEFAULT 1,   -- 1 = a provisionable engine recipe; 0 = receipt/reference (not provisioned by engine-room)
  wave_id       INTEGER REFERENCES waves(id),
  created_date  TEXT
);

-- Relationships to OTHER recipes/artifacts. Answers the modifier + cross-recipe-dep breaks.
CREATE TABLE IF NOT EXISTS recipe_targets (
  id          INTEGER PRIMARY KEY,
  recipe_id   INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  relation    TEXT NOT NULL CHECK (relation IN ('modifies','depends_on','produces')),
  target_slug TEXT NOT NULL,          -- base recipe slug (modifies) | upstream recipe slug (depends_on) | artifact kind (produces: 'gguf','nvfp4-checkpoint','lora','trt-engine')
  start_order INTEGER,                -- for depends_on: bring-up order in a router/proxy stack
  note        TEXT
);

-- Typed variant axes (Spack variants). Expand to many concrete builds.
CREATE TABLE IF NOT EXISTS recipe_variants (
  id          INTEGER PRIMARY KEY,
  recipe_id   INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  name        TEXT NOT NULL,          -- e.g. 'cuda','quant','attn'
  values_csv  TEXT,                   -- allowed values, comma-separated
  default_val TEXT,
  multi       INTEGER DEFAULT 0,      -- may select more than one?
  description TEXT
);

-- Two-tier params (Ansible defaults vs vars).
CREATE TABLE IF NOT EXISTS recipe_params (
  id          INTEGER PRIMARY KEY,
  recipe_id   INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  tier        TEXT NOT NULL CHECK (tier IN ('default','locked')),  -- default=user-flippable, locked=protect the measured stack
  key         TEXT NOT NULL,
  value       TEXT,
  note        TEXT
);

-- Constraints AS DATA, not prose. Includes cross-artifact equality + defect floors.
CREATE TABLE IF NOT EXISTS recipe_constraints (
  id          INTEGER PRIMARY KEY,
  recipe_id   INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  ctype       TEXT NOT NULL CHECK (ctype IN
                ('capability','requires_when','conflicts_when','abi_equal','defect_floor')),
  expr        TEXT NOT NULL,          -- 'gpu_arch>=sm_120' | 'cuda==12.8' | 'wheel.torch_abi==env.torch_abi' | 'wsl2>=2.7.0'
  reason      TEXT                    -- human 'why' — distinguish capability-floor from known-defect-floor
);

-- The phased lifecycle / setup steps, with platform selectors + idempotence guards.
CREATE TABLE IF NOT EXISTS recipe_steps (
  id          INTEGER PRIMARY KEY,
  recipe_id   INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  phase       TEXT NOT NULL CHECK (phase IN ('prepare','configure','activate','measure','teardown')),
  seq         INTEGER NOT NULL,
  selector    TEXT,                   -- when-expr: 'wsl2' | 'native_win' | 'docker' | 'portable' | NULL (always)
  cmd         TEXT NOT NULL,
  creates     TEXT,                   -- idempotence guard (path/sentinel) — executor must CONTENT-verify, not just exist-check
  removes     TEXT
);

-- The measured-baseline TARGET. Keyed by MODEL + context (break #3) and a COMPAT BAND (drift).
CREATE TABLE IF NOT EXISTS recipe_baselines (
  id            INTEGER PRIMARY KEY,
  recipe_id     INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  model_name    TEXT,                 -- NULL only for genuinely model-independent recipes (rare)
  model_quant   TEXT,
  model_sha     TEXT,                 -- pin the exact weights when known
  context_len   INTEGER,
  axis          TEXT NOT NULL,        -- tok_s | s_per_img | it_s | perplexity | bits_per_weight | wer | delta_pct ...
  bound_dir     TEXT CHECK (bound_dir IN ('lower','upper')),  -- tok/s=lower; s_per_img/VRAM/temp=upper
  value         REAL,
  unit          TEXT,
  vram_peak_gb  REAL,                 -- upper-bound (must hold in 32 GB)
  temp_peak_c   REAL,                 -- upper-bound
  power_peak_w  REAL,                 -- upper-bound
  samples       INTEGER,
  threshold_model TEXT CHECK (threshold_model IN ('static-floor','t-test')),
  compat_band   TEXT,                 -- semantic band the measurement holds across: 'driver>=R570; cuda_toolkit==12.8; sm_120; os=native-win'
  measured_date TEXT,
  measured_note TEXT,
  verified      INTEGER DEFAULT 0
);

-- Per-modality correctness gate spec (diffusion/speech break). The golden, declared.
CREATE TABLE IF NOT EXISTS recipe_golden (
  id          INTEGER PRIMARY KEY,
  recipe_id   INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  modality    TEXT NOT NULL CHECK (modality IN
                ('numeric','perceptual','wer','audio-fingerprint','file-hash')),
  spec_json   TEXT,                   -- {"prompt":"2+2=","n_tokens":4,"atol":1e-2} | {"seed":42,"metric":"ssim","threshold":0.97}
  golden_ref  TEXT,                   -- path/hash of the human-blessed reference (NEVER auto-overwritten)
  note        TEXT
);

-- Declared compensators (the no-skip standard, at the KNOWLEDGE level). Execution is action-side.
CREATE TABLE IF NOT EXISTS recipe_compensators (
  id            INTEGER PRIMARY KEY,
  recipe_id     INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  step          TEXT NOT NULL,        -- the irreversible op this undoes
  undo_cmd      TEXT,                 -- the named undo (NULL allowed ONLY when compensatable='non-compensatable')
  post_state    TEXT,                 -- HONEST post-rollback state ('my entry removed IF value unchanged; else halt-and-ask')
  owner         TEXT,                 -- executor-module | human
  compensatable TEXT NOT NULL CHECK (compensatable IN ('auto','human-gated','non-compensatable')),
  note          TEXT
);

-- The pins the RESOLVABILITY floor checks; bridges knowledge<->action. (dead-cu128-URL break)
CREATE TABLE IF NOT EXISTS recipe_artifacts (
  id            INTEGER PRIMARY KEY,
  recipe_id     INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  kind          TEXT CHECK (kind IN ('wheel','docker-image','git-ref','archive','release-asset','model-weights')),
  ref           TEXT NOT NULL,        -- URL | image@sha256 | git url+ref
  sha256        TEXT,
  store_expect  TEXT CHECK (store_expect IN ('index','mirror','local-vendored')),  -- only mirror/local-vendored count as reproducible
  abi_tuple     TEXT,                 -- python_abi / torch_build_tag / cuda_tag — for abi_equal constraints
  resolvable_ok INTEGER,              -- last resolvability probe (HEAD / manifest-inspect / pip-dry-run)
  checked_date  TEXT,
  note          TEXT
);

-- Cross-KB seam: a recipe (esp. a training batch-producer) -> training-knowledge technique(s).
-- The MIRROR of training-knowledge.techniques.engine_recipe_ref. That forward ref is the SINGLE
-- SOURCE OF TRUTH; these reverse rows are GENERATED from it by recipes/_link_techniques.py
-- (idempotent — DO NOT hand-edit; re-run the sync). Makes the join explicit + bidirectional so
-- engine-room resolves a training job = this engine recipe x the KB#4 technique + its hparams.
CREATE TABLE IF NOT EXISTS recipe_techniques (
  id             INTEGER PRIMARY KEY,
  recipe_id      INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
  kb             TEXT NOT NULL DEFAULT 'training-knowledge',
  technique_slug TEXT NOT NULL,        -- -> training-knowledge techniques.slug (the forward ref's source of truth)
  technique_name TEXT,                 -- denormalized for display
  technique_cat  TEXT,                 -- the KB#4 lane (peft-methods / diffusion-sdxl-lora / ...)
  note           TEXT
);
CREATE INDEX IF NOT EXISTS idx_rtech_recipe ON recipe_techniques(recipe_id);

-- Evidence trail for recipe rows reuses the existing `sources` table via subject = recipe.slug
-- (no new column on sources; recipe sources set sources.subject to the recipe's slug).

CREATE INDEX IF NOT EXISTS idx_recipes_engine    ON recipes(engine_slug);
CREATE INDEX IF NOT EXISTS idx_recipes_kind      ON recipes(recipe_kind);
CREATE INDEX IF NOT EXISTS idx_rtargets_recipe   ON recipe_targets(recipe_id);
CREATE INDEX IF NOT EXISTS idx_rbaselines_recipe ON recipe_baselines(recipe_id);
CREATE INDEX IF NOT EXISTS idx_rartifacts_recipe ON recipe_artifacts(recipe_id);

-- Convenience view: a recipe's headline (kind, backend, axis, baseline + pin counts, resolvability)
CREATE VIEW IF NOT EXISTS v_recipes AS
  SELECT r.slug, r.name, r.recipe_kind, r.backend_kind, r.measured_axis,
         r.engine_slug, r.verified, r.resolvable_ok,
         (SELECT COUNT(*) FROM recipe_baselines b WHERE b.recipe_id=r.id) AS n_baselines,
         (SELECT COUNT(*) FROM recipe_artifacts  a WHERE a.recipe_id=r.id) AS n_pins
  FROM recipes r;
