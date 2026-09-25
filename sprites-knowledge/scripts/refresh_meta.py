#!/usr/bin/env python3
"""refresh_meta.py — derive meta's currency pointer FROM the DB, then verify it.

The single source of truth for "how current is this KB" is the meta table's
`latest_wave` / `updated` keys. Those must always equal the high-water mark of
the waves table — NOT whatever wave a given ingest script happened to load last.

This guard is in place from wave 1 on purpose: the sibling tensor-engine-knowledge
KB froze meta at wave 4 while its DB grew to 14 because load_db.py stamped
`latest_wave = str(wave_no)` from the wave being ingested. Here the pointer is
always recomputed from MAX(waves.wave_number), so re-ingesting an old wave — or
appending a wave via a one-off script — can never make meta lie.

  set_meta_currency(cur) -> writes latest_wave = MAX(wave_number),
                            updated = that wave's dispatched_date.
  verify_meta(cur)       -> raises MetaDriftError if meta disagrees with the DB.

Both are importable (load_db.py calls set_meta_currency inside its transaction);
this file also runs standalone as a non-skippable regen step (set + verify).

Run with UTF-8 forced on Windows (cp1252 console):
    $env:PYTHONUTF8='1'; python scripts/refresh_meta.py
"""
import os
import sqlite3
import sys

try:  # parent console may be cp1252 (Win/py3.14)
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "recipes.db")


class MetaDriftError(RuntimeError):
    """meta.latest_wave does not match MAX(waves.wave_number)."""


def _high_water(cur):
    """(wave_number, dispatched_date) of the latest wave, or (None, None) if empty."""
    row = cur.execute(
        "SELECT wave_number, dispatched_date FROM waves ORDER BY wave_number DESC LIMIT 1"
    ).fetchone()
    return (row[0], row[1]) if row else (None, None)


def set_meta_currency(cur):
    """Write meta.latest_wave + meta.updated from the waves high-water mark.

    Idempotent. Returns (latest_wave:int, updated:str), or None on an empty
    waves table. Caller owns the transaction (commit)."""
    wave_no, date = _high_water(cur)
    if wave_no is None:
        return None
    cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('latest_wave',?)", (str(wave_no),))
    cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('updated',?)", (date or "",))
    return (wave_no, date)


def verify_meta(cur):
    """Raise MetaDriftError if meta.latest_wave != MAX(waves.wave_number)."""
    wave_no, _ = _high_water(cur)
    if wave_no is None:
        return  # empty KB — nothing to verify
    row = cur.execute("SELECT value FROM meta WHERE key='latest_wave'").fetchone()
    meta_val = row[0] if row else None
    if meta_val != str(wave_no):
        behind = wave_no - int(meta_val) if (meta_val or "").lstrip("-").isdigit() else "?"
        raise MetaDriftError(
            f"meta.latest_wave={meta_val!r} but MAX(waves.wave_number)={wave_no} "
            f"(stale by {behind} wave(s)). Run scripts/refresh_meta.py (or regen.py) to correct it."
        )


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    result = set_meta_currency(cur)
    if result is None:
        con.close()
        sys.exit("✗ refresh_meta: waves table is empty — load a wave first (scripts/load_db.py).")
    con.commit()
    try:
        verify_meta(cur)
    except MetaDriftError as e:
        con.close()
        sys.exit(f"✗ {e}")
    con.close()
    print(f"  meta.latest_wave = {result[0]}   meta.updated = {result[1]}   (verified vs MAX(waves.wave_number))")


if __name__ == "__main__":
    main()
