---
title: Maintaining
description: How routing works, what is generated and what is authored, how a wave is added, and how a publication reaches this repository.
sidebar:
  order: 5
---

[MAINTENANCE.md](https://github.com/mcp-tool-shop-org/readouts/blob/main/MAINTENANCE.md) is the full runbook, and [CONVENTIONS.md](https://github.com/mcp-tool-shop-org/readouts/blob/main/CONVENTIONS.md) describes the shape every KB shares. This page is the overview.

## Routing: two loadout indexes

An agent should read the one slice a task needs, never the whole corpus. Two indexes make that possible:

1. **The root index**, `.claude/loadout/index.json`, has one entry per KB. It points at the KB's catalog and carries the keywords that route a task to it.
2. **Each KB's index**, `<kb>/.claude/loadout/index.json`, has one entry per domain. It points at one catalog page, with its own keywords and a token estimate.

Each entry looks like this (abridged):

```json
{
  "id": "types-patterns",
  "path": "catalog/types-patterns.md",
  "keywords": ["struct", "enum", "match", "pattern", "let-else"],
  "priority": "domain",
  "summary": "[essentials] Structs, enums & pattern matching: 10 recipes.",
  "triggers": { "task": true, "plan": true, "edit": true },
  "tokens_est": 14373
}
```

[loadout-os](https://github.com/mcp-tool-shop-org/loadout-os) validates and resolves the layers:

```bash
npx @mcptoolshop/loadout-os validate .claude/loadout/index.json
npx @mcptoolshop/loadout-os resolve --project .
```

Both indexes are generated from the databases. Never edit them by hand.

## Generated or authored

The databases are the source of truth, and almost everything else is derived from them. A hand edit to a generated file is silently reverted by the next rebuild.

| Authored: edit these | Generated: never edit by hand |
|---|---|
| each wave's `research-raw.json` (and `lanes/*.json` where a KB uses them), `dispatch.md` and `verification.md` | `<kb>.db` |
| each KB's `README.md`, `schema.sql` and `scripts/` | `catalog/*.md` |
| `verification/verdicts.json`, through its merge script | every `.claude/loadout/index.json` |
| | `readout/*`, the root `index.{md,html,json}`, and the table in the root `README.md` |

The rule of thumb: if a file states a count, it is generated.

## Adding a wave

A wave appends. It never overwrites another wave's rows.

1. Run the research. Every entry needs at least one `{url, claim}` source.
2. Verify before ingesting. With no confirmation the entry stays unverified; nothing passes on faith.
3. Stage the result as `waves/wave-NN-name/research-raw.json`.
4. Rebuild the KB: its `scripts/regen.py` where it has one, or `load_db.py`, `gen_catalog.py` and `gen_loadout.py` in that order. Then run `shared/gen_root_index.py` and `shared/gen_root_loadout.py` at the root.
5. Run `python verify.py`. Nothing is published while it fails.

**A wave number is a replace key.** `load_db.py` replaces every row of the wave it loads. Loading a new study under an existing wave number deletes the old one without an error, so check `SELECT wave_number, title FROM waves` before you pick a number.

## How a publication reaches this repository

The corpus is maintained in a private working repository and published here as a mirror. Each publication is exported by a script that copies an allow-list of tracked files, regenerates the root index, the README table and the root loadout inside the exported tree, and refuses to finish unless four gates pass:

1. **Identity.** The studio's identity scanner must report the tree clean.
2. **Home paths.** No Windows, Git Bash or macOS home-directory path, in any spelling, including escaped and doubled backslashes.
3. **Private names.** No name from the studio's unpublished projects.
4. **Dead links.** No link may point at a file that does not ship. Handbook links are checked the way the site resolves them.

It then runs `verify.py` on the exported tree, and a single FAIL halts the publication.

Because this repository is regenerated from the working one, a pull request here cannot be merged as-is. Open an [issue](https://github.com/mcp-tool-shop-org/readouts/issues) instead, and the change will arrive with the next publication.
