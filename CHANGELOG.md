# Changelog

Notable changes to the published corpus. The format follows [Keep a Changelog](https://keepachangelog.com/). readouts has no version numbers: it is a rolling corpus, so each entry is a dated publication, and the commit on `main` is its identifier.

## 2026-09-26

### Added

- **rust-knowledge wave 5** answers si-jam-sessions' questions after its design lock was signed. It adds 13 recipes across three lanes, all verified by Claude Sonnet, with every code check passing under the pinned `rustc 1.98.1`:
  - PPQ 3360's tuplet table, the u128 overflow bound and the remainder carry;
  - what midly's `strict` feature refuses that the alloc-only build accepts;
  - an audio callback measured to allocate nothing, with a negative control.

  Kimi k2.6 wrote two lanes. Grok 4.7 wrote the third in a chat seat that ran under the generator harness's own gates. rust-knowledge goes from 267 to 280 recipes (266 → 279 verified), and the corpus from 1,819 to 1,832 verified entries.
- One of the new recipes is marked avoid: the wasm32 export that refuses SMPTE-timed files. As written, it panics or hangs on a MIDI division word starting 0x80. Its correction says to read bit 15 of the division word and refuse the file before calling midly.
- Two measurement records in `rust-knowledge/verification/measurements/`:
  - midly 0.5.3 panics on a division word starting 0x80, and what a wasm32 export does on that panic under three panic-handler setups (one hangs, two trap);
  - how cargo unifies a dependency's features across the packages one command builds.

### Changed

- rust-knowledge wave 4's `parse-smf-formats-and-timing` recipe gained a note. Checking for SMPTE timing after parsing misses a division word starting 0x80, which panics inside midly 0.5.3's parser, so refuse any division word with bit 15 set before calling midly.

### Fixed

- rust-knowledge had not been rebuilt for two changes made after its first publication:
  - The second publication put each verifier's correction at the front of the entry's note, but 30 corrected rust-knowledge recipes still did not show theirs. They now open with it.
  - 32 recipes that si-jam-sessions' signed design lock took as pins carried that mark only in `verification/operator-notes.json`. It now shows on their pages and in the database.
- rust-knowledge wave 4's verification record credited its research to Claude Opus. Kimi k2.6 and Gemini 3.1 Pro wrote it, and the record now says so.

## 2026-09-25 (third publication)

### Fixed

- Sixteen source links in godot-knowledge and vocology-knowledge pointed at the private working repository, so every reader who followed one got a 404. They came from the two count-audit waves (godot STUDY-065, vocology STUDY-064) and had spread into the catalog pages and databases built from them. Each now points at the same file in this repository, or, for the one folder, at its tree view. No entry, verdict or verified flag changed.

### Added

- A fifth export gate halts on any URL into the private working repository, in any file or database cell. Text that merely names the repository still passes. The gate fails on the previous publication's tree (48 hits across waves, catalogs and databases) and passes on this one.

## 2026-09-25 (second publication)

### Changed

- The last unverified lanes of the 2026-09-10 sweep were checked by an external verifier. godot-knowledge went from 50 to 108 verified entries of 177, and sprites-knowledge from 92 to 182 of 215: 1,671 → 1,819 verified across the corpus.
- A verifier's correction now leads the entry's verify note: the corrected claim, then any corrected authors, year or id. Until now the loaders stored a corrected verdict as verified but dropped the correction, so the entry kept the wording that had just been corrected.
- Operator scaffolding was removed from entry text in ten knowledge bases. Some notes were addressed to the authoring agent ("Do not flip 37/42/49", "Recipe 49 stays verified=0"); others were receipts of its compliance ("Recipes invented: 0"). They belong to each wave's record, where they stay. No entry, verdict or verified flag changed; only text.

### Fixed

- godot-knowledge's AStarGrid2D recipe said to mark solid cells and then call `update()`. `update()` rebuilds the grid and clears them, so the order is now reversed.
- godot-knowledge's GUT CI recipe required a `-gexit_on_complete` flag that no GUT release has. The recipe is now marked avoid.
- sprites-knowledge had 13 corrections. One of them: FILM's Apache-2.0 licence covers its code but not its weights, while Practical-RIFE's weights are MIT, so the licence comparison between the two ran the wrong way.

### Added

- `shared/rebuild_fts.py --force` rebuilds every full-text index. The alignment check cannot see text edited in place, so a plain run would leave the index matching the old words.

### Security

- Dependabot vulnerability alerts are enabled.

## 2026-09-25

### Added

- **rust-knowledge**, a new knowledge base: verified Rust for building si-rpg-engine (essentials, advanced Rust, and how the engine uses it), plus a first tier for si-jam-sessions' music law. It has four waves, and every code check was compiled, and where it says so run, by the pinned `rustc 1.98.1`. Its fourth wave was written by generators outside the Claude family (Kimi k2.6 and Gemini 3.1 Pro) and verified by Claude.
- **training-knowledge wave 16** (RLVR and GRPO): 193 → 204 techniques, 90 → 101 verified.
- A landing page and a handbook at https://mcp-tool-shop-org.github.io/readouts/.
- README translations, `SECURITY.md`, `SHIP_GATE.md`, `SCORECARD.md` and this changelog.
- `verify.py`: every FAIL and WARN now carries a stable code and a hint, `--json` prints one object per check, and a check that crashes exits 2 as documented.
- CI: `verify.yml` runs `verify.py` on every push that changes the corpus, and `pages.yml` audits the site's npm dependencies before it builds.

### Changed

- The README was rewritten for readers outside the studio. Routing examples now use `@mcptoolshop/loadout-os`; the older `ai-loadout` package is deprecated.
- The public export (`shared/export_public.py`, kept in the private working repository) now regenerates the root index, the README table and the root loadout inside the published tree, so they list exactly the knowledge bases that ship.

### Fixed

- Home-directory paths were removed from two tensor-engine-knowledge ComfyUI logs, where they had been public since 2026-09-10. The identity scanner missed them because their backslashes were doubled. The export now runs its own home-path gate, which accepts any run of separators.
- Two third-party contact email addresses, quoted from dataset licence pages, were removed from a vocology-knowledge verification file, where they had been public since 2026-09-14.
- rust-knowledge's compile oracle now replaces machine-local paths in recorded compiler output with `<work>`, `<tmp>` and `~`.
- godot-knowledge's database was rebuilt without an empty column left over from a private project; its name and comment still sat in the schema. The content is otherwise identical.
- Every database now ships compacted with `VACUUM INTO`: the same content, without the free pages where text deleted by an in-place edit survives.

### Security

- **The repository history was rewritten.** The two earlier publications' commits carried the exposed data above, so `main` now starts from a single commit containing this publication, and those commits are no longer reachable from any branch. If you cloned before 2026-09-25, re-clone, or run `git fetch` and then `git reset --hard origin/main`. The 2026-09-14 and 2026-09-10 entries below describe what those publications contained.

## 2026-09-14

### Changed

- Updated all ten knowledge bases: 112 waves and 2,306 entries. The verified count fell from 1,562 to 1,394 because `verified` now means an external verdict only (`shared/verdicts.py`); it was not a regression.

### Fixed

- Two README links that had been dead since the first publication (`oss-ecosystem-dispatch.md` and its citation set).

## 2026-09-10

### Added

- First publication: ten verified knowledge bases, published as a fresh repository with a single author identity.
- `verify.py`, the corpus's deterministic floor.
