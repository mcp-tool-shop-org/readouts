# Maintaining readouts

The operator runbook. [CONVENTIONS.md](CONVENTIONS.md) describes what a knowledge base
*is*; this describes what you actually run, in what order, and which mistakes have
already cost someone an afternoon.

**One rule above all the others:** the databases are the source of truth, and almost
everything else in this repo is derived from them. Catalogs, loadout indexes, the root
front door, the README's own status table — all generated. If you hand-edit a generated
file, the next `regen.py` silently reverts it and you lose the change without an error.

```powershell
$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'
```

Set that first, every session, on Windows. Entries carry em-dashes and the default
console codepage (cp1252) raises `UnicodeEncodeError` mid-write, which can leave a
half-written artifact behind. Every command below assumes it.

---

## What is generated vs authored

| | |
|---|---|
| **Authored — edit these** | `waves/wave-NN-*/research-raw.json` (and `lanes/*.json` where a KB uses them), `waves/wave-NN-*/dispatch.md`, `waves/wave-NN-*/verification.md`, each KB's `README.md`, `schema.sql`, `scripts/*`, `verification/verdicts.json` (via its merge script) |
| **Generated — never hand-edit** | `<kb>.db`, `catalog/*.md`, `.claude/loadout/index.json` (root and per-KB), `readout/*`, root `index.{md,html,json}`, the KB table inside the root `README.md` |

The rule of thumb: if a file states a count, it is generated. Counts drift the moment
you type them by hand — that is why the README table is produced by
`shared/sync_readme_table.py` and gated by `--check`.

---

## Add a wave to an existing KB

The common case. A wave *appends*; it never overwrites another wave's rows.

1. Run the research. Every entry needs at least one `{url, claim}` source.
2. Verify **before** ingesting. The default verdict on non-confirmation is
   *unverified*, not pass-on-faith.
3. Stage the output at `waves/wave-NN-name/research-raw.json` in that KB's loader shape
   — read the loader's module docstring, the shapes differ slightly per KB.
4. Ingest and regenerate:

```powershell
cd <kb>-knowledge
python scripts/load_db.py waves/wave-NN-name/research-raw.json
python scripts/regen.py        # catalog + loadout + root routers + validate
# docker-knowledge and vocology-knowledge have no regen.py — for those run:
#   python scripts/gen_catalog.py; python scripts/gen_loadout.py; python scripts/refresh_meta.py
#   python ../shared/gen_root_index.py; python ../shared/gen_root_loadout.py
```

`load_db.py` is idempotent per wave: re-running deletes that wave's rows and reinserts
them, leaving other waves untouched. `regen.py` rebuilds every derived artifact from
the DB, so run it rather than the individual generators.

5. Commit the wave provenance **with** the data. `dispatch.md`, `research-raw.json` and
   `verification.md` are the receipt; a wave without them is unauditable.

---

## Add a knowledge base

1. Clone the layout of an existing KB — `godot-knowledge` is the smallest complete one.
2. Write `schema.sql` (idempotent), then `scripts/load_db.py`, `gen_catalog.py`,
   `gen_loadout.py`, `refresh_meta.py`, `regen.py`. They are `__file__`-relative so the
   folder stays portable.
3. Run wave 1 through the flow above.
4. Refresh the root:

```powershell
python shared/gen_root_loadout.py     # the router: which KB?
python shared/gen_root_index.py       # the front door: index.{html,md,json}
python shared/sync_readme_table.py    # the README status table
```

5. Optionally add a profile to `shared/readout_profiles.py`. Without one the KB is
   still discovered and still appears on the front door — it is just a lean
   catalog+loadout KB with no `readout/` pages, which is a normal and supported shape.

A KB is discovered by having **both** a `.claude/loadout/index.json` and a non-empty
`.db`. That is the whole gate, in both root generators.

---

## Remove a KB, a wave, or an entry

**A KB.** Delete the folder, then re-run the three root commands above. Nothing else
references it — that is the point of the two-level router.

**A wave.** Delete `waves/wave-NN-*/`, then rebuild the DB from scratch, because
`load_db.py` only ever removes the wave it is currently ingesting:

```powershell
cd <kb>-knowledge
rm <kb>.db
foreach ($w in Get-ChildItem waves/*/research-raw.json) { python scripts/load_db.py $w }
python scripts/regen.py
```

**An entry.** Remove it from its wave's `research-raw.json` and rebuild as above. Do
not `DELETE FROM` the database — the next reload brings it straight back, and you will
have spent the interim believing it was gone.

---

## Run a verification sweep

For findings that were ingested but never actually checked. `vocology-knowledge` has a
worked example under `verification/sweep-2026-09-09/`.

1. Export the unverified entries, bucketed by domain, one file per lane.
2. Run one adversarial retrieval agent per bucket. Each checks three things
   independently — that the work **exists**, that **authors and year** are right, and
   that the source supports **the specific claim**, numbers and all. Non-confirmation
   is `unfindable`, never a pass.
3. Merge the lane verdicts into the ledger and rebuild:

```powershell
cd vocology-knowledge
python scripts/merge_verdicts.py 'verification/sweep-*/lanes/*.json'
rm findings.db
foreach ($w in Get-ChildItem waves/*/research-raw.json) { python scripts/load_db.py $w }
python scripts/regen.py
```

**Why a ledger and not a database update.** The DB is derived. A sweep that only writes
`verified=1` into SQLite is erased by the next reload, silently. `verification/verdicts.json`
is authored state that `load_db.py` reads, so the verified flags survive a rebuild and
the next sweep extends the ledger instead of replacing it.

---

## Traps

Each of these has actually happened.

**A 0-byte `.db` shadows the real one.** Both root generators used to take
`glob("*.db")[0]`. A stray empty `recipes.db` sorted ahead of `training.db` and the
front door reported **0 of 127 entries** for that KB — no error, just a zero. They now
take the largest DB that actually holds tables. If a KB reads 0, look for a second
`.db` file before you look at anything else.

**Word-boundary regexes do not fire inside identifiers.** `\bfoo\b` does not match
`dataset_foo_v3` or `_on_foo`, because `_` is a word character. Any scanner that looks
for a forbidden string must treat `_` and digits as boundaries, or it will report clean
while the string is right there. Make a detector **broader** than the rewriter that
feeds it, so an unhandled case halts the run instead of shipping.

**Never collapse the space before every `.`** in a text-cleanup pass.
`ai-loadout validate .claude/...` becomes `validate.claude/...` and a sentence about
packing textures `into .blend` becomes `into.blend`. Require that nothing word-like
follows the dot.

**Scrub the load source, not the artifact.** Editing a `catalog/*.md` or the DB is
undone by the next regen. Editing `research-raw.json` — and, where a KB uses them, the
`lanes/*.json` the wave is assembled from — survives, because everything downstream is
rebuilt from it.

**Watch the line endings.** The generators write LF. On Windows, git may report every
generated file as modified after a checkout; that is `core.autocrlf`, not a real diff.

---

## Before publishing anything

`shared/export_public.py` builds the public mirror and refuses to finish unless four
gates pass: an identity scan, a home-path scan, a forbidden-term scan, and a dead-link
check across every markdown and HTML file. After the gates, the exported tree's own
`verify.py` must pass on it. The export copies an allow-list of git-tracked paths and
performs **no** content transformation. It cannot be the last line of defence, so it
is built to halt rather than to fix.

Two things are not plain copies, and neither scrubs anything:

- **The `public/` overlay.** Files that exist only for the public repo are published at
  the root without the prefix: its README and translations, SECURITY, CHANGELOG, the
  ship gate, the `site/` landing page and handbook, and `.github/workflows/`. An overlay
  path wins over the same path from the allow-list. The internal README lists KBs that
  do not ship, and the Pages workflow must not run on the private repo, which is why
  neither lives at the internal root.
- **The root files are regenerated in the export.** `gen_root_index.py`,
  `sync_readme_table.py` and `gen_root_loadout.py` run inside the exported tree, so the
  front door, the README table and the root router list exactly the KBs that ship.

`verify.py` skips `site/` (and `public/site/` here) in its dead-link check, because
handbook links resolve by URL, not by file. The export's dead-link gate checks them the
way Starlight resolves them.

Three things it taught us, worth repeating anywhere else:

**Assert the good state, never grep for the bad one.** The identity scanner exits 0
even when it prints `RESULT HIT`, so `scan && push` does not gate anything. Require
`RESULT CLEAN` to be present — then a crash, a timeout or empty output halts too.

**Source from `git ls-files`, not a filesystem walk.** The walk pulled in 10.6 GB of
gitignored run artifacts. `.gitignore` already draws the content/scratch line; inherit
that decision rather than making a second, weaker one. The rule is for choosing what
to *copy*. A gate that *scans* the exported tree must walk the filesystem: freshly
copied files are untracked in the destination clone, and a scanner that read only
`git ls-files` there let 97 new paths through unscanned in the 2026-09-14 publication.

**A database is more than its cells.** `CREATE TABLE IF NOT EXISTS` never alters an
existing table, so a column removed from `schema.sql` lives on in a built database until
it is rebuilt from scratch, and SQLite keeps the CREATE text, comments included, in
`sqlite_master`. Text deleted by an in-place edit also survives in free pages. godot.db
shipped an emptied private-project column both ways while every cell scanned clean. The
export now copies each database with `VACUUM INTO` (same content, no free pages), and
its scans read `sqlite_master` and the raw bytes as well as the cells. When a schema
changes, rebuild the KB's database fresh: move the `.db` aside, run its `regen.py`, and
compare the content with the old copy.

**A gate is only as good as its patterns.** The identity scanner's home-path pattern
allowed exactly one separator. A path whose backslashes are doubled (a JSON string, a
Python repr in a log, a Debug-formatted linker command) passed it as clean, and two
public ComfyUI logs carried a home path from the first publication until 2026-09-25.
The export now runs its own home-path gate, which accepts any run of separators, any
drive letter and the Git Bash and macOS spellings, and scans database cells too. The
scanner was fixed the same day. Test every gate with a planted positive in each
spelling the data can take.
