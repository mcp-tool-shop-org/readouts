-- training-knowledge :: schema
-- A long-lived, wave-appended knowledge base of TRAINING CRAFT — the portable HOW-TO-TRAIN
-- knowledge layer for the studio's single-RTX-5090 pipeline. It sits BETWEEN the weights
-- (model-knowledge KB) and the software (tensor-engine-knowledge KB): it owns the methods,
-- recipes, hyperparameter VALUES, dataset construction/curation/license craft, evaluation
-- methodology, and the symptom->cause->fix debugging taxonomy for two workloads — SDXL/Flux
-- style-LoRA training (priority) and light 24-34B Q-quant local LLM fine-tuning.
--
-- It owns NO weights and NO software. Rig-MEASURED engine receipts (exact CLI, measured it/s,
-- VRAM peaks, engine-version gotchas) stay in tensor-engine-knowledge and are REFERENCED here via
-- engine_recipe_ref, never restated — the Parnas seam that keeps the same number from drifting
-- across two KBs.
--
-- The atomic entity is a `technique`: a parameterized, evidence-backed, REPLAYABLE procedure.
-- That is the key divergence from the engine schema: an engine's currency is "is the binary
-- current"; a technique's currency is "do the reported results still hold and is the provenance
-- honest" — so a technique carries first-class REPRODUCIBILITY columns (seed/runs/variance/
-- tuning-budget/evidence_strength) and a predecessor link (so QLoRA->DPO is one queryable chain),
-- which engines never need because only here is the entity RUN and replayed.
--
-- One SQLite file (training.db); the "cluster" is the linked-table graph:
--   waves -> techniques -> {technique_purposes -> purposes, technique_hparams, technique_failures,
--                           technique_evals, technique_datasets -> datasets, sources}
--   ; categories
-- Every fact carries a wave_id (provenance); every entity a verified flag (the study-swarm
-- EXTERNAL_VERIFIER stage writes it). New waves append; nothing is overwritten.

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

-- A datasets table FIRST-CLASS (not inline per recipe): a dataset is reused across many recipes,
-- and Datasheets-for-Datasets (Gebru 2021) says the datasheet is maintained ONCE per dataset.
-- technique_datasets is the many-to-one join; a recipe references a dataset by stable slug.
CREATE TABLE IF NOT EXISTS datasets (
  id                   INTEGER PRIMARY KEY,
  slug                 TEXT UNIQUE NOT NULL,
  name                 TEXT NOT NULL,
  base_model_target    TEXT,               -- which model family this set is captioned/built FOR (SDXL|Flux|Qwen3...)
  modality             TEXT,               -- image|text|paired-preference|...
  image_count          INTEGER,
  caption_format       TEXT,               -- wd14-tags|natural-language|booru|chatml|... (keyed to base model)
  caption_strategy     TEXT,               -- trigger words, style-vs-subject pruning rule, etc.
  pruning_rule         TEXT,               -- the style-bleed lever: which tags to prune so style binds to trigger
  dedup_method         TEXT,               -- clip-cosine|phash|minhash|...
  dedup_threshold      TEXT,
  reg_image_count      INTEGER,            -- prior-preservation / regularization set size (nullable for pure-style)
  reg_source           TEXT,
  real_synthetic_ratio TEXT,               -- + accumulate-don't-replace note (model-collapse guard)
  -- Datasheets-for-Datasets sections (commercial-clean gate lives here):
  motivation           TEXT,
  collection_process   TEXT,
  preprocessing        TEXT,               -- cleaning / labeling / latent-cache
  intended_uses        TEXT,
  license              TEXT,               -- a dataset row cannot be verified without a non-null license
  redistribution       TEXT,               -- yes|no|conditional
  maintained           TEXT,               -- maintenance plan / cadence
  train_eval_overlap_checked INTEGER,      -- 0/1 : contamination check done
  verified             INTEGER DEFAULT 0,
  verify_note          TEXT,
  wave_id              INTEGER REFERENCES waves(id),
  created_date         TEXT
);

-- Every technique: a parameterized, evidence-backed, replayable procedure.
CREATE TABLE IF NOT EXISTS techniques (
  id                 INTEGER PRIMARY KEY,
  slug               TEXT UNIQUE NOT NULL,
  name               TEXT NOT NULL,
  category_id        INTEGER REFERENCES categories(id),
  kind               TEXT,                 -- recipe|method-theory|protocol|curation|eval-method|failure-fix
  method_family      TEXT,                 -- lora|qlora|dora|locon|lokr|loha|dreambooth|sft|dpo|orpo|kto|simpo|grpo|rlvr|distillation
  applicable_to      TEXT,                 -- diffusion|llm|both  (MECE modality split for routing)
  base_model_family  TEXT,                 -- SDXL|Flux|Chroma|Qwen3|Llama|...  (recipe KEY; references model-knowledge by family)
  claim              TEXT,                 -- one-line load-bearing statement
  summary            TEXT,                 -- the how-to / what it is
  design_implication TEXT,                 -- what it means for THIS pipeline
  -- reproducibility (PIN_PER_STEP; Pineau/Henderson/Dodge). A row with NULL seed+num_runs caps evidence_strength.
  evidence_strength  TEXT,                 -- ORDINAL: measured-on-rig > reproduced-from-source > single-reported-run > community-claim > untested
  seed               TEXT,
  num_runs           INTEGER,
  variance_note      TEXT,
  tuning_budget      TEXT,                 -- how much search produced this (can flip a conclusion)
  search_method      TEXT,                 -- grid|manual|bayes|none
  measured_conditions TEXT,                -- the validated envelope (Model Cards): "SDXL only, 1024px, 24-img set"
  -- the cross-KB seam: the tensor-engine config_recipes slug + version-pin this was MEASURED against.
  engine_recipe_ref  TEXT,                 -- e.g. "training-kohya-sdxl-lora-...-5090 @ sd-scripts vXX" (numbers live THERE)
  base_model_slug    TEXT,                 -- optional pointer to a model-knowledge slug (the base trained ON)
  -- recipe sequencing: a multi-stage run (QLoRA-SFT -> DPO) is ONE queryable chain, not two loose rows.
  predecessor_technique_id INTEGER REFERENCES techniques(id),
  stage_order        INTEGER,              -- 1,2,3... within a pipeline; NULL = standalone
  commercial_use     TEXT,                 -- yes|conditional|no|unknown : is the OUTPUT commercial-clean (inherits base + dataset)
  commercial_notes   TEXT,
  rig_fit            INTEGER,              -- 0-5 fit for the single-5090 studio (32 GB Blackwell / Windows / WSL2)
  studio_fit         INTEGER,              -- 0-5 fit for the studio's actual workloads
  download_priority  INTEGER,              -- lower = try first (derived from status + evidence_strength)
  status             TEXT,                 -- recommended|runner-up|situational|legacy|superseded|avoid
  verified           INTEGER DEFAULT 0,    -- external verifier confirmed existence/attribution/currency
  verify_note        TEXT,
  superseded_by      INTEGER REFERENCES techniques(id),  -- retired, not deleted (Datasheets Maintenance)
  -- S6 training-programs GUARANTEE fields (recipe-preview inputs; populated in S6.3-GPU; all nullable).
  -- Contract: role-os/design/specialist-training-programs.md (study-swarm wf_9b6208e9-b97). migrate_s6.py
  -- ALTER-adds these to an EXISTING db (CREATE TABLE IF NOT EXISTS does not add columns to one).
  difficulty_signal        TEXT,     -- the difficulty metric used; reject perplexity/loss-only (finding 1)
  mixing_law_coefficients  TEXT,     -- JSON: fitted data-mixing-law coefficients (Ye 2024; finding 6)
  calibration_params       INTEGER,  -- calibration scale (params): out-of-band-prediction guard (finding 11)
  calibration_tokens       INTEGER,  -- calibration scale (tokens)
  replay_fraction          REAL,     -- forgetting-mitigation replay fraction (Bethune 2025; finding 10)
  measured_forgetting      REAL,     -- measured forgetting at that replay fraction (Kalajdzievski 2024; finding 9)
  task_embedding_ref       TEXT,     -- task-embedding fingerprint ref (Vu 2020; finding 19)
  task_vector_ref          TEXT,     -- task-vector fingerprint ref (Ilharco 2023; finding 21)
  wave_id            INTEGER REFERENCES waves(id),
  created_date       TEXT
);

-- queryable hyperparameters (NOT a prose blob): "what rank/alpha did the best SDXL style-LoRA use".
-- Optimizer<->LR stored as linked rows so LR=1.0 (Prodigy sentinel) is never read as a bare rate.
-- Controlled key vocab (keep consistent): network_type, rank, alpha, unet_lr, te_lr, learning_rate,
-- optimizer, scheduler, warmup, batch_size, grad_accum, steps, epochs, repeats, resolution, precision,
-- min_snr_gamma, network_dim, target_modules, beta (dpo), loss_type, group_size (grpo)...
CREATE TABLE IF NOT EXISTS technique_hparams (
  id           INTEGER PRIMARY KEY,
  technique_id INTEGER NOT NULL REFERENCES techniques(id) ON DELETE CASCADE,
  name         TEXT NOT NULL,
  value        TEXT,
  unit         TEXT,
  required     INTEGER DEFAULT 0,
  note         TEXT
);

-- symptom -> cause -> remediation taxonomy, each mapped back to the recipe FIELD that causes/cures it.
-- technique_id is nullable: a failure mode can be cross-cutting (the debugging lane) or pinned to a recipe.
CREATE TABLE IF NOT EXISTS technique_failures (
  id           INTEGER PRIMARY KEY,
  technique_id INTEGER REFERENCES techniques(id) ON DELETE CASCADE,
  symptom      TEXT NOT NULL,
  cause        TEXT,
  remediation  TEXT,
  recipe_field TEXT,                        -- the hparam/field this fix touches (rank|lr|epochs|captions|inference_weight...)
  severity     TEXT,                        -- blocker|quality|cosmetic
  wave_id      INTEGER REFERENCES waves(id)
);

-- eval method + PINNED provenance + an acceptance bar ("how do I know it WORKED").
CREATE TABLE IF NOT EXISTS technique_evals (
  id                 INTEGER PRIMARY KEY,
  technique_id       INTEGER REFERENCES techniques(id) ON DELETE CASCADE,
  eval_kind          TEXT,                  -- diffusion-style|llm-task|llm-judge|human-ab|...
  metric             TEXT,                  -- CMMD|HPSv2|PickScore|LPIPS|lm-eval:<task>|...
  harness            TEXT,                  -- the instrument (a tensor-engine tool; cited, not catalogued here)
  task_version       TEXT,
  prompt_template    TEXT,
  n_shot             INTEGER,
  precision          TEXT,
  seed               TEXT,
  judge_model_family TEXT,                  -- MUST differ from the model-under-test (EXTERNAL_VERIFIER)
  result             TEXT,
  threshold          TEXT,                  -- the acceptance bar (a bare score is meaningless without it)
  accepted           INTEGER,               -- 0/1 : did it clear the bar
  note               TEXT
);

-- many-to-one: a technique references a (reusable) dataset; the datasheet lives once on datasets.
CREATE TABLE IF NOT EXISTS technique_datasets (
  technique_id INTEGER NOT NULL REFERENCES techniques(id) ON DELETE CASCADE,
  dataset_id   INTEGER NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
  role         TEXT,                         -- training|regularization|preference|eval
  note         TEXT,
  PRIMARY KEY (technique_id, dataset_id, role)
);

CREATE TABLE IF NOT EXISTS purposes (
  id          INTEGER PRIMARY KEY,
  slug        TEXT UNIQUE NOT NULL,
  name        TEXT NOT NULL,
  category_id INTEGER REFERENCES categories(id),
  description TEXT
);

-- "best technique for what" matrix (many-to-many)
CREATE TABLE IF NOT EXISTS technique_purposes (
  technique_id INTEGER NOT NULL REFERENCES techniques(id) ON DELETE CASCADE,
  purpose_id   INTEGER NOT NULL REFERENCES purposes(id) ON DELETE CASCADE,
  fitness      INTEGER,                      -- 0-5
  rank         INTEGER,                      -- 1 = best-in-class for this purpose
  use_tag      TEXT,                         -- diffusion|llm|sdxl|flux|dataset|eval|single-gpu
  note         TEXT,
  PRIMARY KEY (technique_id, purpose_id)
);

-- citation / evidence trail. target_table/target_id let a source back a SPECIFIC sub-claim
-- (a single hparam value or a failure->fix), not just the whole technique.
CREATE TABLE IF NOT EXISTS sources (
  id                INTEGER PRIMARY KEY,
  technique_id      INTEGER REFERENCES techniques(id) ON DELETE CASCADE,
  subject           TEXT,                   -- when not tied to a technique row
  kind              TEXT,                   -- paper|docs|benchmark|model-card|dataset-card|article|community|receipt
  title             TEXT,
  authors           TEXT,
  year              TEXT,
  identifier        TEXT,                   -- arXiv id / DOI / RFC
  url               TEXT NOT NULL,
  claim             TEXT,                   -- one-sentence finding this source backs
  retrieved_date    TEXT,
  verified          INTEGER DEFAULT 0,      -- retrieval oracle confirmed it resolves
  finding_supported TEXT,                   -- SUPPORTED|PARTIAL|NOT_SUPPORTED|CANT_TELL (groundedness)
  verifier_note     TEXT,
  target_table      TEXT,                   -- optional: technique_hparams|technique_failures|technique_evals|datasets
  target_id         INTEGER,                -- optional: the specific sub-row this source backs
  wave_id           INTEGER REFERENCES waves(id)
);

-- S6 first-class prerequisite EDGE: a foundation technique makes a successor cheaper/faster to
-- certify. The edge is a WITNESSED, falsifiable claim (role-os/design/specialist-training-programs.md):
-- a directional witness that it is real (findings 12,13) + the measured cheaper-after-foundation delta
-- (findings 15,16, measured on the rig in S6.3). predecessor_technique_id on `techniques` is the
-- structural skeleton; this table carries the edge METADATA role-os reads and S6.3 fills.
CREATE TABLE IF NOT EXISTS technique_edges (
  id                 INTEGER PRIMARY KEY,
  predecessor_id     INTEGER NOT NULL REFERENCES techniques(id) ON DELETE CASCADE,
  successor_id       INTEGER NOT NULL REFERENCES techniques(id) ON DELETE CASCADE,
  witness_score      REAL,                 -- directional witness 0-1 (RefD-style asymmetry); NULL until computed
  witness_signals    TEXT,                 -- JSON: which signals fired (explicit_predecessor, stage_chain, shared_datasets...)
  steps_saved_frac   REAL,                 -- cheaper-after-foundation delta: fraction of GPU-steps saved (finding 16)
  outcome_n_receipts INTEGER DEFAULT 0,    -- how many rig runs back the delta (0 = unverified)
  edge_kind          TEXT,                 -- 'cheaper' | 'prerequisite-required'  (findings 1,2)
  validated_as       TEXT,                 -- 'sequence' | 'merge'  (LoRA prefers sequenced; TC-LoRA Su 2025, finding 22)
  verifier_note      TEXT,
  -- S6.3 honesty gate (cross-family adversarial verify, 2026-06-13): the verdict is computed from the
  -- RAW per-seed deltas, never a hand-authored scalar. record_measurement.py writes a non-NULL
  -- steps_saved_frac ONLY when n>=3 receipts agree in sign AND clear the preregistered magnitude floor;
  -- otherwise NULL (unverified). role-os re-checks (classifyEdge), so neither layer can surface a false confirm.
  consistent_sign    INTEGER,              -- 0/1 : all per-seed deltas agree in sign; NULL = not measured
  per_seed_deltas    TEXT,                 -- JSON array of the raw per-seed steps_saved_frac (auditable / re-derivable)
  wave_id            INTEGER REFERENCES waves(id),
  UNIQUE (predecessor_id, successor_id)
);

-- full-text search over techniques (matches the siblings' FTS5 convention)
CREATE VIRTUAL TABLE IF NOT EXISTS techniques_fts USING fts5(
  slug, name, method_family, applicable_to, base_model_family, summary, claim, best_for, category
);

CREATE INDEX IF NOT EXISTS idx_tech_category   ON techniques(category_id);
CREATE INDEX IF NOT EXISTS idx_tech_status     ON techniques(status);
CREATE INDEX IF NOT EXISTS idx_tech_applicable ON techniques(applicable_to);
CREATE INDEX IF NOT EXISTS idx_tech_pred       ON techniques(predecessor_technique_id);
CREATE INDEX IF NOT EXISTS idx_hparams_tech    ON technique_hparams(technique_id);
CREATE INDEX IF NOT EXISTS idx_failures_tech   ON technique_failures(technique_id);
CREATE INDEX IF NOT EXISTS idx_evals_tech      ON technique_evals(technique_id);
CREATE INDEX IF NOT EXISTS idx_tp_purpose      ON technique_purposes(purpose_id);
CREATE INDEX IF NOT EXISTS idx_sources_tech    ON sources(technique_id);
CREATE INDEX IF NOT EXISTS idx_edges_pred      ON technique_edges(predecessor_id);
CREATE INDEX IF NOT EXISTS idx_edges_succ      ON technique_edges(successor_id);

-- convenience views ----------------------------------------------------------
CREATE VIEW IF NOT EXISTS v_recommended AS
  SELECT c.name AS category, t.download_priority AS dl, t.name, t.method_family, t.applicable_to,
         t.base_model_family, t.kind, t.status, t.evidence_strength, t.commercial_use,
         t.rig_fit AS rig, t.studio_fit AS studio, t.verified, t.engine_recipe_ref
  FROM techniques t JOIN categories c ON c.id = t.category_id
  WHERE t.status IN ('recommended', 'runner-up')
  ORDER BY c.sort, t.download_priority, t.name;

CREATE VIEW IF NOT EXISTS v_best_for AS
  SELECT p.name AS purpose, t.name AS technique, tp.rank, tp.fitness, tp.use_tag,
         t.applicable_to, t.evidence_strength, t.commercial_use, t.rig_fit AS rig, t.verified
  FROM technique_purposes tp
  JOIN techniques t ON t.id = tp.technique_id
  JOIN purposes p   ON p.id = tp.purpose_id
  ORDER BY p.name, tp.rank, tp.fitness DESC;

-- a multi-stage pipeline as one chain (QLoRA-SFT -> DPO -> ...)
CREATE VIEW IF NOT EXISTS v_pipeline AS
  SELECT t.id, t.slug, t.name, t.stage_order, t.predecessor_technique_id,
         pre.name AS builds_on, t.applicable_to, t.method_family
  FROM techniques t LEFT JOIN techniques pre ON pre.id = t.predecessor_technique_id
  WHERE t.predecessor_technique_id IS NOT NULL OR t.stage_order IS NOT NULL
  ORDER BY t.applicable_to, t.stage_order;

-- seed the 8 lanes -----------------------------------------------------------
INSERT OR IGNORE INTO categories(slug, name, description, sort) VALUES
  ('peft-methods',        'PEFT methods & adapter theory',          'Cross-cutting parameter-efficient fine-tuning theory both domains share — LoRA/QLoRA/DoRA/LoRA+/rsLoRA, diffusion LyCORIS (LoKr/LoHa/LoCon), LLM PiSSA/GaLore + merging. Rank vs alpha as a coupled scaling pair. Weights->model-knowledge; library-as-software->tensor-engine.', 10),
  ('diffusion-sdxl-lora', 'SDXL style-LoRA recipes (priority)',     'The studio #1 workload: full hyperparameter recipes for SDXL-family style LoRAs (kohya/ComfyUI as engine references only). rank+alpha, optimizer<->LR, booru-tag captioning + style-tag pruning, regularization, 1024px bucketing, repeats/epochs, min-SNR-gamma, per-rank quality signature.', 20),
  ('diffusion-flux-lora', 'Flux-family style-LoRA recipes',         'A SEPARATE recipe space from SDXL (flow-matching, not DDPM). Commercial-safe Apache-2.0 bases only (FLUX.2 [klein], Chroma1-HD); FLUX.1-dev/FLUX.2-dev are non-commercial and must not be a training base here. Higher rank, NL captions, frozen T5, fp8 base, no prior-preservation by default.', 30),
  ('dataset-caption',     'Dataset construction & caption craft',   'The inputs that drive outcome more than hyperparameters: curation/dedup, caption format keyed to base model, style-vs-subject pruning, regularization sets, real:synthetic discipline, and Datasheets-style license/provenance (commercial-clean gate). Captioner weights->model-knowledge; pipeline tooling->tensor-engine.', 40),
  ('llm-finetune',        'Local LLM fine-tuning (SFT + preference + RL)', '24-34B at Q-quant on one 32 GB GPU: QLoRA-NF4 SFT + chat templates, then the preference/RL family selected by the DATA you have — DPO/ORPO/KTO/SimPO and GRPO/RLVR. Light reverse-KL/on-policy distillation lives here too.', 50),
  ('efficiency',          'Single-GPU efficiency & training-VRAM technique', 'Fitting TRAINING on one 32 GB Blackwell GPU — the binding constraint, orthogonal to method choice. The training-VRAM arithmetic (optimizer-state + gradient + activation sizing) and the decision heuristics; paged/8-bit optimizers, gradient checkpointing/accumulation, FSDP2 CPU-offload, NF4 vs fp8 training. Measured peaks->tensor-engine; inference placement->docker-knowledge.', 60),
  ('evaluation',          'Training evaluation & validation methodology', 'How to attest a trained adapter with receipts. Diffusion STYLE eval (CMMD/HPSv2/PickScore/LPIPS + ai-eyes A/B, not DreamBooth subject metrics); LLM eval via pinned lm-eval-harness + a bias-controlled DIFFERENT-FAMILY judge. Never a bare FID/CLIP scalar. Eval tool-as-software->tensor-engine.', 70),
  ('debugging',           'Failure modes & debugging',              'The symptom->cause->fix taxonomy that closes the recipe->result->fix loop, portable across engines: overfit/replication, frying/saturation, style-bleed, NaN/loss-spike, catastrophic forgetting, OOM-on-32GB, reward-hacking. Each maps back to the recipe field that causes and cures it. Engine-version crash receipts->tensor-engine.', 80);
