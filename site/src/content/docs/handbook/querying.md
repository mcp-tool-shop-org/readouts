---
title: Querying
description: Search a knowledge base, keep only verified entries, and follow an entry back to its sources and its wave.
sidebar:
  order: 2
---

Every KB follows the same shape, so the same few queries work everywhere. Only the table names change.

## The tables

| Table | What it holds |
|---|---|
| the entity table | The entries. It is named for what the KB collects: `recipes`, `findings`, `models`, `engines`, `techniques` or `capabilities`. Every entity table has `id`, `slug`, `name` and `verified`. |
| `<entity>_fts` | The FTS5 full-text index over the entries. Its `rowid` is the entry's `id`. |
| `sources` | One row per cited source: `title`, `url` and `claim`, keyed to the entry by `<entity>_id` (for example `recipe_id`). docker-knowledge and vocology-knowledge name this table `finding_sources`, keyed by `finding_id`. |
| `waves` | One row per research wave: `wave_number`, `title` and `verifier_note`, which says who verified it. |
| `categories` | The domains. Each entry's `category_id` points here. |

[`index.md`](https://github.com/mcp-tool-shop-org/readouts/blob/main/index.md) lists every KB's database file and full-text table.

## Search, then join

Search the index, then join each hit back to its entry by `rowid`:

```sql
-- sqlite3 rust-knowledge/rust.db
SELECT r.name, r.verified
FROM recipes_fts f
JOIN recipes r ON r.id = f.rowid
WHERE recipes_fts MATCH 'rapier'
LIMIT 5;
```

Always join on `rowid`, never by position or by count. An index whose rowids drift from the entry ids returns plausible rows that belong to a different entry. `verify.py` checks every index for exactly that on every push.

## Keep only what was verified

```sql
SELECT r.name
FROM recipes_fts f
JOIN recipes r ON r.id = f.rowid
WHERE recipes_fts MATCH 'determinism'
  AND r.verified = 1;
```

Most KBs also provide a `v_recommended` view, and docker-knowledge and vocology-knowledge provide `v_load_bearing` instead. These views select by the KB's own recommendation field, such as `status IN ('recommended', 'runner-up')` or `currency IN ('solid', 'plausible')`. Only rust-knowledge's view filters on `verified`. A recommended entry is not necessarily a verified one, so read a view's definition before you rely on it:

```sql
SELECT name, sql FROM sqlite_master WHERE type = 'view';
```

## Full-text syntax

`MATCH` takes FTS5 query syntax:

| Query | Matches |
|---|---|
| `'rapier AND restore'` | entries with both words |
| `'rapier OR bevy'` | entries with either word |
| `'determin*'` | any word starting with `determin` |
| `'"broad phase"'` | the exact phrase |
| `'NEAR(wasm export, 5)'` | both words within five tokens of each other |

In Python, pass the query as a parameter rather than formatting it into the SQL string.

## Follow an entry to its sources

```sql
SELECT s.title, s.url, s.claim
FROM sources s
JOIN recipes r ON r.id = s.recipe_id
WHERE r.slug = 'split-a-crate-into-file-modules-with-mod-name-and-share-internals-via-pub-crate-pub-super-not-pub';
```

Each source row pairs a URL with the claim it supports, which is what the verifier checked.

## Follow an entry to its wave

```sql
SELECT w.wave_number, w.title, w.verifier_note
FROM recipes r
JOIN waves w ON w.id = r.wave_id
WHERE r.verified = 1
LIMIT 3;
```

`verifier_note` records who researched the wave and who verified it. The wave's full record is in the KB's `waves/` folder, under the same wave number: `dispatch.md`, `research-raw.json` and, where the wave has one, `verification.md`.

## From Python

```python
import sqlite3

def search(db, table, query, verified_only=True):
    """Full-text search one KB and return (name, verified) pairs."""
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)  # read-only
    sql = (
        f"SELECT e.name, e.verified FROM {table}_fts f "
        f"JOIN {table} e ON e.id = f.rowid "
        f"WHERE {table}_fts MATCH ?"
    )
    if verified_only:
        sql += " AND e.verified = 1"
    return con.execute(sql, (query,)).fetchall()

print(search("vocology-knowledge/findings.db", "findings", "formant"))
```

Opening the file with `mode=ro` keeps a script from ever writing to the corpus.
