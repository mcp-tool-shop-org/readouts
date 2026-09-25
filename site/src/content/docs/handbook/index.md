---
title: The readouts handbook
description: What readouts is, how it is built, and how to query, trust and maintain it.
sidebar:
  order: 0
---

readouts is a set of knowledge bases about the tools behind a small game studio: Rust, Godot, Blender, sprite and animation craft, local AI models and the engines that run and train them, the sung voice, GPU containers and the XRP Ledger.

Each knowledge base (KB) is one SQLite database. Every entry in it names its sources, records the research wave that produced it, and carries a `verified` flag. Only a verdict from a separate verifier can set that flag.

## Who it is for

- **Agents.** The corpus is built to be read in slices. Two loadout indexes route a task to one KB and then to one domain inside it, so an agent never has to load the whole thing.
- **People building the same things.** The entries are practical: how to do something, the gotchas, and what the sources actually say. You can read them as markdown or query them as SQL.
- **Anyone who wants to check a claim.** Every verdict can be traced to the pages it was checked against, and the checks that keep the corpus honest run on every push.

## What is in a knowledge base

| Part | What it is |
|---|---|
| `<kb>.db` | The SQLite database: entries, their sources, the waves they came from, and a full-text index. |
| `catalog/` | Markdown pages generated from the database, one per domain. |
| `waves/` | One folder per research wave: what was asked, what came back, and what the verifier found. |
| `.claude/loadout/index.json` | The KB's router: which catalog page answers which kind of task. |
| `README.md` | What the KB covers and how it was built. |

Some KBs keep more, such as a `verification/` folder with the verdict ledger, or the scripts and benchmarks that produced a wave.

## Where to go next

- [Getting started](./getting-started/): clone, check the corpus, and run a first query.
- [Querying](./querying/): the search-then-join pattern, verified-only queries, sources and provenance.
- [The knowledge bases](./knowledge-bases/): what each KB covers and what it optimises for.
- [Verification](./verification/): how an entry earns `verified`, and what the flag does not promise.
- [Maintaining](./maintaining/): routing, adding a wave, and how a publication reaches this repository.
- [Reference](./reference/): every `verify.py` check and code, the file layout, and the loadout fields.
