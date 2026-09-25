# readouts conventions

How every knowledge base in this monorepo is built and maintained, so the tooling and the loadout router work uniformly across KBs.

## The shape of a knowledge base

A KB is a self-contained folder:

- `models.db` — SQLite; a linked-table graph (`waves` → entries → {entry↔purpose, `sources`}; `categories`; companion tables). `schema.sql` defines it and is idempotent.
- `catalog/` — human-readable per-domain markdown, **generated from the DB** (never hand-edited).
- `waves/wave-NN-*/` — per-wave provenance: `dispatch.md` (narrative + findings → recommendations), `research-raw.json` (the verified swarm output, the load source), `verification.md` (the verifier receipt).
- `workflows/` — optional companion files (e.g. ComfyUI graphs).
- `scripts/` — `load_db.py` (idempotent wave ingester), `gen_catalog.py` (DB→catalog), `gen_loadout.py` (DB→ai-loadout index). `__file__`-relative, so the folder is portable.
- `.claude/loadout/index.json` — the KB's own progressive-disclosure router.

## Waves — how a KB grows

1. Identify the load-bearing questions / domains (the study-swarm / research-grounded protocol).
2. Dispatch parallel research agents, one per lane, each web-grounded and **sourced** (every entry ≥ 1 `{url, claim}`).
3. **Verify** — a reasoning-stripped adversarial agent retrieval-checks every entry (existence / license / specs / currency) *before* it is trusted. Default verdict `unverified` on non-confirmation, not pass-on-faith.
4. Stage the verified output at `waves/wave-NN-name/research-raw.json` as `{ wave, date, lanes }`.
5. `python scripts/load_db.py waves/wave-NN-name/research-raw.json` (idempotent — re-running replaces that wave's rows) → `python scripts/gen_catalog.py` → `python scripts/gen_loadout.py`.
6. Root generator pair: `python ../shared/gen_root_loadout.py` to refresh the root router, AND `python ../shared/gen_root_index.py` to refresh the root readout (`index.{html,md,json}`, generated from the DBs). `ai-loadout validate` both the KB index and the root index.

Run Python with `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'` — entries carry em-dashes that the default Windows codepage chokes on.

## Provenance + verification (non-negotiable)

- Every row carries a `wave_id`. Nothing silently overwrites; **waves append**.
- Every claim links to a `source`; every entry carries a `verified` flag.
- **Verifier maturity:** currently a *same-model-family* verifier plus a **retrieval oracle** (the live page is the decorrelating element that catches what a parametric LLM can't). The planned upgrade is *family-different* verification — route citations through `prism verify` / `roleos verify-citations`, ideally a local non-Claude model on this rig.

In-group, **Verifier** is the retrieval-check (existence / license / specs / currency on named extra-reads). `prism verify` / `roleos verify-citations` stays an operator path on the rig, not an in-group seat.

Study-swarm seats: Coordinator names three load-bearing questions; Scholar, Practitioner, and Analogist each receive four fields (stop / prerequisite / owner / fallback) via **SendToAgent on their own threads** (not group @ as the work dispatch); wait three ✅; Verifier retrieval-checks all three packs; Coordinator writes Research grounding in chat; Builder lands. Missing Practitioner or Analogist → 🛑 operator (do not Scholar-only sequential-fake).

## Naming

KB folders are kebab-case, typically `<topic>-knowledge` (e.g. `model-knowledge`). Each is self-contained and independently loadable; the root loadout stitches them into one router.
