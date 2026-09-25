# Verifier brief — rust-knowledge wave 5 (si-jam-sessions P2, after the lock)

Read `E:/AI/readouts-consolidate/rust-knowledge/briefs/VERIFIER-BRIEF.md` first. Its rules hold: what you
check by retrieving, the verdict vocabulary, currency, the output shape, and the refusal to soften. This
brief changes only what follows.

## Paths (this wave lives in the readouts-internal worktree)

- **Your input:** `E:/AI/readouts-consolidate/rust-knowledge/verification/sweep-2026-09-25-w5/lanes/<lane>.input.json`.
  You receive only the recipes, their checks and their citations. Do not open the lane's packet or the
  `waves/` folder.
- **Your output:** the same folder, `<lane>.json`, in the shape VERIFIER-BRIEF.md gives, except
  `"bucket": "<lane>@wave-5"` (wave 4 used the same lane names on the same date).
- **Counter-examples:** `python E:/AI/readouts-consolidate/rust-knowledge/scripts/compile_oracle.py file <file.rs> ...`
  Write your files in your own temp directory, never in the repository.

## The lock is signed

si-jam-sessions signed its Phase 0 lock (`docs/PHASE-0.md` @ `e3cc85e`,
https://github.com/mcp-tool-shop-org/si-jam-sessions/blob/main/docs/PHASE-0.md). An `engine_note` must
be consistent with these pins, and presenting a pin wrongly is a defect:

- edition 2024 `wasm32-unknown-unknown` cdylib, raw `extern "C"` + `#[unsafe(no_mangle)]` exports;
  status codes cross the boundary, panics do not; every export argument and return is at most 64 bits;
- integer ticks at **PPQ 3360**; tick → sample = floor(tick × tempo_us_per_quarter × 48000 /
  (PPQ × 10^6)) in `u128` with the remainder carried across tempo segments; `checked_*` with a refusal;
  `overflow-checks = true` in release; no f64 in the time path;
- `midly` 0.5.3 with `default-features = false, features = ["alloc", "strict"]`; SMPTE-timed files
  refused;
- native host: `cpal` 0.18.2 WASAPI shared mode, an `rtrb` SPSC ring, no allocation on the audio
  callback.

## Dependency sets

A check names its set in `oracle_set`:

- `jam`: `midly` 0.5.3 with `alloc` only (NOT `strict`), plus the wave-4 parsers; host only: `cpal`,
  `midir`, `rtrb`, `ringbuf`, `assert_no_alloc`.
- `jam-strict` (new this wave): `midly` 0.5.3 with `alloc` + `strict`, host and wasm32. Nothing else.

Pass the same set to a counter-example: `--oracle jam-strict --deps midly`. A claim that midly behaves
differently with and without `strict` is checkable by running the same file under both sets.

## Arithmetic claims

Several recipes in this wave are arithmetic: tuplet divisibility, overflow bounds, remainder carry. The
compiler runs their checks, but you judge whether a check proves the prose. Recompute any number the
prose states, from the definitions, before you accept it. A bound or table that the check does not
actually assert (it prints a value nobody compares, say) is a check that proves something weaker.
