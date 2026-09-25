-- vocology-knowledge :: schema
-- Sung-voice craft KB: vocology, musical vs speech prosody, lyric-to-note alignment,
-- score-controllable SVS vs lyrics-to-song generators, admission/teaching evaluation.
-- Consumer: ai-jam-sessions (MIDI practice companion). Adjacent: vocal-synth-engine.
-- Not a models table — ACE-Step / DiffRhythm / Kokoro live in model-knowledge.
--
-- Linked-table graph: waves -> findings -> finding_sources ; categories
-- Every fact carries a wave_id; findings + sources carry a verified flag.
-- Waves append. Idempotent CREATE IF NOT EXISTS; load_db.py replaces a wave's rows by wave_number.

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

CREATE TABLE IF NOT EXISTS findings (
  id                 INTEGER PRIMARY KEY,
  slug               TEXT UNIQUE NOT NULL,
  name               TEXT NOT NULL,
  category_id        INTEGER REFERENCES categories(id),
  kind               TEXT,                 -- paper|method|route|eval|constraint
  claim              TEXT,
  detail             TEXT,
  design_implication TEXT,
  citation_id        TEXT,                 -- DOI / arXiv / other identifier from the wave
  authors            TEXT,
  year               TEXT,
  status             TEXT,                 -- load-bearing|directional|supporting
  verified           INTEGER DEFAULT 0,
  verify_note        TEXT,
  wave_id            INTEGER REFERENCES waves(id),
  created_date       TEXT
);

CREATE TABLE IF NOT EXISTS finding_sources (
  id                INTEGER PRIMARY KEY,
  finding_id        INTEGER REFERENCES findings(id) ON DELETE CASCADE,
  title             TEXT,
  authors           TEXT,
  year              TEXT,
  identifier        TEXT,
  url               TEXT NOT NULL,
  claim             TEXT,
  exists_verified   INTEGER DEFAULT 0,
  finding_supported TEXT,
  verifier_note     TEXT,
  wave_id           INTEGER REFERENCES waves(id)
);

CREATE VIRTUAL TABLE IF NOT EXISTS findings_fts USING fts5(
  slug, name, claim, detail, design_implication, category
);

CREATE INDEX IF NOT EXISTS idx_findings_category ON findings(category_id);
CREATE INDEX IF NOT EXISTS idx_findings_status   ON findings(status);
CREATE INDEX IF NOT EXISTS idx_fsrc_finding      ON finding_sources(finding_id);

CREATE VIEW IF NOT EXISTS v_load_bearing AS
  SELECT c.name AS category, f.name, f.claim, f.design_implication, f.verified, f.status
  FROM findings f JOIN categories c ON c.id = f.category_id
  WHERE f.status IN ('load-bearing', 'directional')
  ORDER BY c.sort, f.status, f.name;

INSERT OR IGNORE INTO categories(slug, name, description, sort) VALUES
  ('vocology-source-filter', 'Vocology / source-filter floor',
   'Source–filter theory, singer formant, registers, vibrato, breathiness cues', 10),
  ('musical-vs-speech-prosody', 'Musical vs speech prosody',
   'Duration, F0, and prosody differences that break speech-TTS copied onto lyrics', 20),
  ('lyric-to-note-alignment', 'Lyric-to-note alignment',
   'Vowel-on-beat, phoneme×MIDI×duration, melisma and onset timing', 30),
  ('svs-vs-song-generator', 'SVS vs lyrics-to-song routes',
   'Score-conditioned singing synthesis vs mixed-song generators; MIDI-lock and licenses', 40),
  ('eval-and-teaching-hci', 'Singing eval and teaching HCI',
   'MUSHRA/MOS for singing, vocal-model identity, teaching / practice HCI', 50);
