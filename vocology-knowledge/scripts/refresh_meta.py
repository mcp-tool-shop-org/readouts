#!/usr/bin/env python3
"""refresh_meta.py — derive meta currency FROM the DB (MAX wave), never the ingest wave."""
import os
import sqlite3
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "findings.db")


class MetaDriftError(RuntimeError):
    pass


def _high_water(cur):
    row = cur.execute(
        "SELECT wave_number, dispatched_date FROM waves ORDER BY wave_number DESC LIMIT 1"
    ).fetchone()
    return (row[0], row[1]) if row else (None, None)


def set_meta_currency(cur):
    wave_no, date = _high_water(cur)
    if wave_no is None:
        return None
    cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('latest_wave',?)", (str(wave_no),))
    cur.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('updated',?)", (date or "",))
    return (wave_no, date)


def verify_meta(cur):
    wave_no, _ = _high_water(cur)
    if wave_no is None:
        return
    row = cur.execute("SELECT value FROM meta WHERE key='latest_wave'").fetchone()
    meta_val = row[0] if row else None
    if meta_val != str(wave_no):
        raise MetaDriftError(
            f"meta.latest_wave={meta_val!r} but MAX(waves.wave_number)={wave_no}"
        )


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    result = set_meta_currency(cur)
    if result is None:
        con.close()
        sys.exit("✗ refresh_meta: waves table is empty")
    con.commit()
    try:
        verify_meta(cur)
    except MetaDriftError as e:
        con.close()
        sys.exit(f"✗ {e}")
    con.close()
    print(f"  meta.latest_wave = {result[0]}   meta.updated = {result[1]}")


if __name__ == "__main__":
    main()
