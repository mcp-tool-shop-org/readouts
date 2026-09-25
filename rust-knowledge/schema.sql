-- rust-knowledge — readouts KB: Rust for building si-rpg-engine
-- Primary entity: a RECIPE (an actionable Rust practice / API / pattern / measured fact) + two verdicts:
--   currency  — the adversarial verifier's verdict against Rust 1.98.1 stable / edition 2024 and the
--               pinned crate versions (solid / plausible / shaky / stale / wrong)
--   compile   — the NON-MODEL verdict: every code check the recipe carries, run by the pinned compiler
--               (scripts/compile_oracle.py, rustc 1.98.1), pass / fail / none
-- Four tiers, one wave each: essentials, advanced, si-rpg-engine, si-jam-sessions.
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
  tier        TEXT,                   -- essentials | advanced | si-rpg-engine | si-jam-sessions
  sort        INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS recipes (
  id             INTEGER PRIMARY KEY,
  slug           TEXT UNIQUE NOT NULL,
  name           TEXT NOT NULL,
  category_id    INTEGER REFERENCES categories(id),
  tier           TEXT,
  what           TEXT,                 -- one line: the finding
  how            TEXT,                 -- concrete current practice
  rust_version   TEXT,                 -- e.g. "1.82+", "edition 2024", "rapier3d-f64 0.35.3"
  gotchas        TEXT,
  engine_note    TEXT,                 -- how it bears on si-rpg-engine (file / function / slice)

  currency       TEXT,                 -- solid | plausible | shaky | stale | wrong  (verifier)
  verify_note    TEXT,
  verified       INTEGER DEFAULT 0,    -- 1 iff the ledger says so (external verdict AND compile gate)
  status         TEXT,                 -- recommended | situational | directional | avoid

  compile_status TEXT,                 -- pass | fail | none   (the compiler, not a model)
  compile_note   TEXT,

  wave_id        INTEGER REFERENCES waves(id),
  created_date   TEXT
);

-- One row per code check a recipe carries, with the oracle's result.
CREATE TABLE IF NOT EXISTS checks (
  id              INTEGER PRIMARY KEY,
  recipe_id       INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
  idx             INTEGER NOT NULL,
  label           TEXT,
  edition         TEXT,
  target          TEXT,
  crate_type      TEXT,
  deps            TEXT,                -- JSON array
  rustc_flags     TEXT,                -- JSON array
  expect          TEXT,                -- compiles | compile_fail | runs
  error_codes     TEXT,                -- JSON array
  lints           TEXT,                -- JSON array
  expected_stdout TEXT,
  gates           TEXT,                -- JSON object: every other gate the oracle enforced (no_warnings, wasm_*, …)
  source          TEXT NOT NULL,
  oracle_ok       INTEGER,             -- 1 pass, 0 fail, NULL not run
  oracle_note     TEXT,
  rustc           TEXT,
  wave_id         INTEGER REFERENCES waves(id)
);

CREATE TABLE IF NOT EXISTS sources (
  id          INTEGER PRIMARY KEY,
  recipe_id   INTEGER REFERENCES recipes(id) ON DELETE CASCADE,
  title       TEXT,
  url         TEXT NOT NULL,
  claim       TEXT,
  year        INTEGER,
  kind        TEXT,
  identifier  TEXT,
  verified    INTEGER,                 -- the verifier's PER-SOURCE result: 1 supported, 0 not, NULL unchecked
  wave_id     INTEGER REFERENCES waves(id)
);

CREATE VIRTUAL TABLE IF NOT EXISTS recipes_fts USING fts5(
  slug, name, what, how, gotchas, engine_note, category
);

CREATE INDEX IF NOT EXISTS idx_recipes_category ON recipes(category_id);
CREATE INDEX IF NOT EXISTS idx_recipes_currency ON recipes(currency);
CREATE INDEX IF NOT EXISTS idx_sources_recipe   ON sources(recipe_id);
CREATE INDEX IF NOT EXISTS idx_checks_recipe    ON checks(recipe_id);

-- ---- Views ----

-- the trustworthy half: current, externally verified, compiler-clean where code is shown
CREATE VIEW IF NOT EXISTS v_recommended AS
  SELECT c.tier, c.name AS category, r.name, r.rust_version, r.currency, r.compile_status, r.what
  FROM recipes r JOIN categories c ON c.id = r.category_id
  WHERE r.verified = 1
  ORDER BY c.sort, r.name;

-- per-lane rollup
CREATE VIEW IF NOT EXISTS v_by_lane AS
  SELECT c.tier, c.name AS category, c.slug, COUNT(r.id) AS recipes,
         SUM(CASE WHEN r.currency='solid' THEN 1 ELSE 0 END) AS solid,
         COALESCE(SUM(r.verified), 0) AS verified,
         SUM(CASE WHEN r.compile_status='pass' THEN 1 ELSE 0 END) AS compiled,
         SUM(CASE WHEN r.compile_status='fail' THEN 1 ELSE 0 END) AS compile_failed
  FROM categories c LEFT JOIN recipes r ON r.category_id = c.id
  GROUP BY c.id ORDER BY c.sort;

-- the flagged half: never silently trusted
CREATE VIEW IF NOT EXISTS v_flagged AS
  SELECT c.tier, c.name AS category, r.name, r.currency, r.compile_status, r.status, r.verify_note, r.compile_note
  FROM recipes r JOIN categories c ON c.id = r.category_id
  WHERE r.currency IN ('shaky', 'stale', 'wrong') OR r.compile_status = 'fail' OR r.status = 'avoid'
  ORDER BY c.sort, r.name;

-- every recipe that names a place in si-rpg-engine
CREATE VIEW IF NOT EXISTS v_engine AS
  SELECT c.tier, c.name AS category, r.name, r.engine_note, r.verified
  FROM recipes r JOIN categories c ON c.id = r.category_id
  WHERE COALESCE(TRIM(r.engine_note), '') <> ''
  ORDER BY c.sort, r.name;

-- Lanes. An upsert keeps each lane's id stable and its name/description/tier/sort current.
INSERT INTO categories(slug, name, description, tier, sort) VALUES
  ('ownership-borrowing',    'Ownership, moves & borrowing',            'Moves, Copy/Clone, the borrow rule, NLL, reborrowing, elision, and the borrow errors with their fixes.', 'essentials', 10),
  ('types-patterns',         'Structs, enums & pattern matching',       'Sum types over flags, exhaustive match, let-else, let chains, newtypes, casts vs TryFrom.', 'essentials', 20),
  ('traits-generics',        'Traits & generics — the working set',     'Standard trait contracts, f64 and PartialOrd, generics vs dyn, operator traits, the orphan rule.', 'essentials', 30),
  ('errors-panics',          'Errors, panics & arithmetic safety',      'Result and ?, error enums, panic=abort, overflow behaviour, status codes at an FFI edge.', 'essentials', 40),
  ('collections-iterators',  'Collections, iterators & closures',       'Vec, BTreeMap vs HashMap order, sorting and ties, iterator laziness, closures, float sums.', 'essentials', 50),
  ('cargo-modules',          'Cargo, crates, modules & editions',       'Manifests, the lockfile, feature unification, profiles, editions, toolchain and rustflags precedence.', 'essentials', 60),
  ('testing-tooling',        'Testing, lints & dev tooling',            'Unit/integration/doc tests for a cdylib, wasm test runners, clippy, proptest, mutants.', 'essentials', 70),
  ('traits-advanced',        'Advanced traits & the type system',       'Associated types, GATs, dyn compatibility, coherence, auto traits, variance, upcasting, precise capture.', 'advanced', 110),
  ('memory-layout',          'Memory, smart pointers & layout',         'Box/Rc/Arc, cells and lazies, repr and layout, niches, Pin, arenas and handles, reallocation.', 'advanced', 120),
  ('unsafe-ffi',             'Unsafe Rust, UB & FFI',                   'The UB catalogue, &raw, static mut under 2024, unsafe attributes, C ABI and unwinding, Miri.', 'advanced', 130),
  ('concurrency-async',      'Concurrency, parallelism & async',        'Send/Sync, threads, locks, atomics and orderings, parallel float reductions, async basics.', 'advanced', 140),
  ('macros-const',           'Macros, const evaluation & build scripts','macro_rules!, proc macros, build.rs, cfg/check-cfg, const fn and const floats, compile-time asserts.', 'advanced', 150),
  ('performance',            'Performance & profiling',                 'Profile knobs, bounds checks, allocation reuse, layout, profilers, why a pinned artifact avoids native tuning.', 'advanced', 160),
  ('rust-currency',          'What changed in Rust 1.80 → 1.98',        'Edition 2024 and every stabilization since 1.80 that changes how engine code is written.', 'advanced', 170),
  ('wasm-raw-abi',           'Rust → WebAssembly without bindgen',      'Raw extern "C" exports over linear memory, traps, views, targets and features, module inspection.', 'si-rpg-engine', 210),
  ('float-determinism',      'Floating point & cross-platform determinism', 'What is bit-identical across hosts, contraction, libm, NaN/zero canonicalisation, deterministic maps.', 'si-rpg-engine', 220),
  ('rapier-core',            'Rapier 0.35: pipeline, determinism & upgrades', 'The step, integration parameters, body types, events, features, the determinism promise, bump policy.', 'si-rpg-engine', 230),
  ('restore-internals',      'Rapier state for restore (T2)',           'Warm-start impulses, activation and islands, broad-phase order, serde canonicality — what solver_restore must carry.', 'si-rpg-engine', 240),
  ('rapier-shapes-kcc',      'Rapier shapes, meshes & the character controller', 'Parry shapes, trimesh flags, hulls, heightfields, the controller end to end, sight queries.', 'si-rpg-engine', 250),
  ('binary-and-limits',      'Binary lint, CCD and controller limits (T3/T4)', 'Fixed memory and memory.grow, relaxed-SIMD encoding, CCD guarantees, controller limit comparisons.', 'si-rpg-engine', 260),
  ('sim-architecture',       'Deterministic simulation architecture',   'Save/restore/rerun, canonical encoding, stable hashes, handles and order, law versioning.', 'si-rpg-engine', 270),
  ('host-embedding',         'Embedding the law in hosts',              'One pinned wasm in wasmtime/Wasmer/WAMR vs native gdext/C ABI builds, for Godot and Unreal.', 'si-rpg-engine', 280),
  ('ci-reproducible-builds', 'Rust CI, reproducible binaries & supply chain', 'Toolchain pins, caching, reproducible bytes, Rust-side gates, bump policy, scheduled jobs.', 'si-rpg-engine', 290),
  ('midi-notation-ingest',   'Score ingest inside a wasm law: SMF, MusicXML, ABC', 'Parsing score bytes with no files or clocks: midly, quick-xml, roxmltree, musicxml, abc-parser; one PPQ; canonical re-encoding.', 'si-jam-sessions', 310),
  ('integer-time',           'Integer musical time: ticks, tempo maps, samples', 'Tick to microsecond and sample through an SMF tempo map with u64/u128 math, exact rounding, PPQ choice, bars under meter changes.', 'si-jam-sessions', 320),
  ('host-audio-and-midi',    'Native audio and MIDI host', 'cpal output on WASAPI, lock-free event delivery to the audio callback, midir input timestamps mapped onto the law clock.', 'si-jam-sessions', 330),
  ('crate-licences',         'Crate licences for a shipped MIT/Apache product', 'Licence allowlists, weak copyleft decisions, attribution output, and which licences reach a shipped binary.', 'si-jam-sessions', 340)
ON CONFLICT(slug) DO UPDATE SET
  name = excluded.name, description = excluded.description, tier = excluded.tier, sort = excluded.sort;
