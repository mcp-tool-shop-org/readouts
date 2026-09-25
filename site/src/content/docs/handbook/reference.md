---
title: Reference
description: verify.py's checks, codes and exit codes, the repository layout, and the environment the scripts expect.
sidebar:
  order: 6
---

## verify.py

```bash
python verify.py            # run every check
python verify.py --strict   # count warnings as failures
python verify.py --list     # list the checks and why each exists
python verify.py --json     # one JSON object per check
```

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean, or warnings only (without `--strict`). |
| 1 | At least one FAIL, or a warning under `--strict`. |
| 2 | A check crashed. The harness is broken; fix `verify.py` before trusting any result. |

### JSON output

`--json` prints one object per line. A passing check has `level`, `check` and `message`. A failing or warning check adds `code`, `hint` and `retryable` (always `false`: re-running without a fix gives the same result).

```json
{"level": "FAIL", "check": "README table current", "message": "stale — run shared/sync_readme_table.py", "code": "STATE_README_TABLE_STALE", "hint": "Run `python shared/sync_readme_table.py`.", "retryable": false}
```

### Codes

| Code | Check | Next step |
|---|---|---|
| `STATE_SHADOW_DB` | no shadow DB | Delete the empty `.db` file; each KB keeps one real database. |
| `STATE_DB_CORRUPT` | sqlite integrity | Restore the KB's `.db` from git, or rebuild it from its wave files. |
| `STATE_FTS_MISALIGNED` | FTS rowid alignment | Run `python shared/rebuild_fts.py`, then re-run `verify.py`. |
| `STATE_VERIFIED_UNSOURCED` | verified implies a source | Add the entry's sources, or clear `verified`, then rebuild the KB. |
| `STATE_VERIFIED_NOT_EXTERNAL` | verified is external | `verified = 1` needs an external verdict in the KB's `verification/verdicts.json` or its wave file. |
| `STATE_META_STALE` | meta.latest_wave current | Rebuild the KB. |
| `STATE_FRONT_DOOR_STALE` | front door matches DBs | Run `python shared/gen_root_index.py`. |
| `STATE_README_TABLE_STALE` | README table current | Run `python shared/sync_readme_table.py`. |
| `IO_DEAD_LINK` | no dead relative links | Fix the link, or restore the file it points at. |
| `STATE_SOURCE_FLAG_COPIED` | source flag is independent (WARN) | Known and recorded. |
| `STATE_ENTRY_UNSOURCED` | every entry has a source (WARN) | Known and recorded; the next wave for that KB adds sources. |
| `STATE_SLUG_FORKED` | no collision-forked slugs (WARN) | Review the pairs before re-ingesting a wave. |
| `RUNTIME_CHECK_CRASHED` | any | A check raised instead of reporting: a bug in `verify.py`. |

Codes are part of the output contract. A code is renamed only with a [CHANGELOG](https://github.com/mcp-tool-shop-org/readouts/blob/main/CHANGELOG.md) entry.

## Layout

```text
readouts/
  index.md, index.json, index.html    the corpus map, generated from the databases
  .claude/loadout/index.json          root router: a task to a KB
  verify.py                           the floor
  regen.py                            rebuild every KB and the root files
  shared/                             generators shared by every KB
  <kb>/
    <kb>.db                           the database
    catalog/                          one generated page per domain
    waves/wave-NN-name/               dispatch.md, research-raw.json, verification.md
    verification/                     verdict ledger and sweep records, where kept
    readout/                          the KB's own front door
    .claude/loadout/index.json        KB router: a task to a domain
    scripts/                          load_db.py, gen_catalog.py, gen_loadout.py, and more
    README.md
  site/                               this handbook and the landing page
```

## Environment

- **Python 3.10 or newer**, standard library only, for `verify.py`, `regen.py` and the generators.
- **UTF-8 on Windows.** Set `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'` before running anything. The entries carry non-ASCII text, and the default console code page can fail halfway through writing a file.
- **Line endings.** The generators write LF. With git's `core.autocrlf` on Windows, freshly generated files can show as modified with no real change.
- **Research tooling** is optional and needs more: rust-knowledge's compile oracle needs `rustup` with Rust 1.98.1 and `node`, and the generator harness needs a local Ollama daemon or an `OPENROUTER_API_KEY`. Each KB's README describes its own tools.
