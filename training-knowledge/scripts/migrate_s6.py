#!/usr/bin/env python3
"""Idempotent S6 schema migration for training.db.

schema.sql is the source of truth; this brings an EXISTING db up to it. Two steps:
  1. re-apply schema.sql (CREATE TABLE IF NOT EXISTS creates technique_edges + any new tables/indexes);
  2. ALTER-add the new `techniques` columns — CREATE TABLE IF NOT EXISTS does NOT add columns to a
     table that already exists, so a guarded ALTER is the only way to evolve the existing core table.

Additive + nullable only; safe to run repeatedly. load_db.py and gen_curriculum.py both call this, so
every wave load and every export self-heals the schema. Contract:
role-os/design/specialist-training-programs.md (study-swarm wf_9b6208e9-b97).

Run standalone:  python scripts/migrate_s6.py
"""
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.environ.get("TRAINING_DB") or os.path.join(ROOT, "training.db")
SCHEMA = os.path.join(ROOT, "schema.sql")

# The S6 per-technique GUARANTEE columns (must mirror the additions in schema.sql's CREATE techniques).
TECH_COLS = [
    ("difficulty_signal", "TEXT"),
    ("mixing_law_coefficients", "TEXT"),
    ("calibration_params", "INTEGER"),
    ("calibration_tokens", "INTEGER"),
    ("replay_fraction", "REAL"),
    ("measured_forgetting", "REAL"),
    ("task_embedding_ref", "TEXT"),
    ("task_vector_ref", "TEXT"),
]

# The S6.3 honesty-gate columns on technique_edges (mirror schema.sql's CREATE technique_edges).
EDGE_COLS = [
    ("consistent_sign", "INTEGER"),
    ("per_seed_deltas", "TEXT"),
]


def migrate_s6(con):
    """Apply the S6 schema additions idempotently. Returns the list of columns actually added."""
    with open(SCHEMA, "r", encoding="utf-8") as f:
        con.executescript(f.read())  # creates technique_edges + indexes; no-op for what already exists
    cur = con.cursor()
    have = {r[1] for r in cur.execute("PRAGMA table_info(techniques)")}
    added = []
    for col, typ in TECH_COLS:
        if col not in have:
            cur.execute(f"ALTER TABLE techniques ADD COLUMN {col} {typ}")
            added.append(col)
    have_edge = {r[1] for r in cur.execute("PRAGMA table_info(technique_edges)")}
    for col, typ in EDGE_COLS:
        if col not in have_edge:
            cur.execute(f"ALTER TABLE technique_edges ADD COLUMN {col} {typ}")
            added.append(col)
    con.commit()
    return added


if __name__ == "__main__":
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    added = migrate_s6(con)
    n_edges = con.execute("SELECT COUNT(*) FROM technique_edges").fetchone()[0]
    print(f"migrate_s6: techniques columns added {added or '(none — already present)'}; "
          f"technique_edges ensured ({n_edges} rows).")
    con.close()
