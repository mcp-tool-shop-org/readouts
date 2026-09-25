---
title: Getting started
description: Clone readouts, check the corpus, and run a first query.
sidebar:
  order: 1
---

## What you need

- **git**, to clone the repository.
- **Python 3.10 or newer**, for `verify.py` and the generators. They use only the standard library.
- **Any SQLite client**: the `sqlite3` command line, Python's `sqlite3` module, DB Browser for SQLite, or anything else that opens SQLite 3 files. The full-text indexes use FTS5, which current SQLite builds include.

There is nothing to install and nothing runs on its own.

## 1. Clone and check

```bash
git clone https://github.com/mcp-tool-shop-org/readouts
cd readouts
python verify.py
```

`verify.py` prints one line per check. A clean run ends with `Clean.` or, when known warnings are present, `Clean on every blocking check; warnings are known and recorded.` Warnings are real defects that are already recorded, and they do not block. [Verification](../verification/) explains what each check proves.

On Windows, set UTF-8 first. Entries carry em dashes and other non-ASCII text, which the default console code page cannot print:

```powershell
$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'
```

## 2. Find the knowledge base you want

Open [`index.md`](https://github.com/mcp-tool-shop-org/readouts/blob/main/index.md) at the root. It lists every KB with its database file, its full-text table, what it covers and how many entries are verified. [`index.json`](https://github.com/mcp-tool-shop-org/readouts/blob/main/index.json) holds the same map for programs. [The knowledge bases](../knowledge-bases/) describes each one.

## 3. Read before you query

Every KB has a `catalog/` folder of markdown pages generated from its database, one page per domain. Each page lists its entries with their details, their verdicts and their sources. `catalog/README.md` is the table of contents. On GitHub these pages read like documentation, and for browsing they are often faster than SQL.

## 4. Run a first query

Open a database and search its full-text index:

```sql
-- sqlite3 rust-knowledge/rust.db
SELECT r.name, r.verified
FROM recipes_fts f
JOIN recipes r ON r.id = f.rowid
WHERE recipes_fts MATCH 'rapier'
LIMIT 5;
```

The same query from Python:

```python
import sqlite3

con = sqlite3.connect("rust-knowledge/rust.db")
rows = con.execute(
    "SELECT r.name, r.verified FROM recipes_fts f "
    "JOIN recipes r ON r.id = f.rowid "
    "WHERE recipes_fts MATCH ? LIMIT 5",
    ("rapier",),
).fetchall()
for name, verified in rows:
    print("verified" if verified else "lead    ", name)
```

A row with `verified = 0` is a lead, not a fact. [Querying](../querying/) covers the rest: verified-only queries, sources, provenance and full-text syntax.

## 5. Point an agent at it

If your agent uses loadout indexes, check the root index and resolve it:

```bash
npx @mcptoolshop/loadout-os validate .claude/loadout/index.json
npx @mcptoolshop/loadout-os resolve --project .
```

The root index routes a task to one KB, and that KB's own index routes it to one catalog page. `resolve` also merges your own global loadout layer, if you have one. [Maintaining](../maintaining/) describes the index format.
