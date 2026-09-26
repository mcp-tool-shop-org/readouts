# rust-knowledge

Verified Rust knowledge for building **si-rpg-engine**, the studio's deterministic 3D simulation
engine. Its physics law is Rust (`rapier3d-f64` 0.35.3 + `enhanced-determinism`), compiled to one
`wasm32-unknown-unknown` binary pinned by its digest. A fourth tier serves **si-jam-sessions**, a
deterministic music law built the same way, whose design lock is now signed. The KB has four tiers. Each
has one research wave, except si-jam-sessions, which has two:

| Tier | Wave | What it holds |
|---|---|---|
| **essentials** | `wave-01-essentials` | The Rust a builder must never get wrong: ownership and borrowing, types and patterns, traits and generics, errors and panics, collections and iterators, Cargo and editions, testing and tooling. |
| **advanced** | `wave-02-advanced` | The parts of the language that decide design: the type system, memory and layout, unsafe and FFI, concurrency and async, macros and const evaluation, performance, and what changed from Rust 1.80 to 1.98. |
| **si-rpg-engine** | `wave-03-si-rpg-engine` | How Rust is and will be used in the engine: the raw wasm ABI, float determinism, the Rapier pipeline, the state a restore must carry (T2), shapes and the character controller, the binary lint and the controller limits (T3/T4), simulation architecture, host embedding (Godot, Unreal), and CI with reproducible bytes. |
| **si-jam-sessions** | `wave-04-si-jam-sessions`, `wave-05-si-jam-p2` | Rust for a deterministic music law. Wave 4 came before the lock signed, so each of its recipes states the lock item it assumes. It covers score ingest inside a wasm law (SMF, MusicXML, ABC), integer musical time (ticks, tempo maps, samples), the native audio and MIDI host, and crate licences for a shipped MIT/Apache product. Wave 5 answers the signed lock's questions: PPQ 3360's tuplet table, overflow bound and remainder carry; what midly's `strict` refuses; and an allocation-free audio callback, measured. |

Start at [catalog/README.md](catalog/README.md). Engine-facing notes (every recipe that names a file,
function, pin or slice of si-rpg-engine) are indexed in [catalog/engine.md](catalog/engine.md). An agent
routes through `.claude/loadout/index.json`, which loads one lane at a time.

## Two verdicts per recipe

Every recipe is judged twice, by two verifiers that do not share a failure mode:

1. **Currency**, from an adversarial retrieval verifier. This is Claude Sonnet, a different model from
   every research seat, and it never sees a research seat's reasoning. It opens every cited page
   and checks each API, lint, flag and version claim against Rust **1.98.1** stable / edition 2024 and
   the pinned crate versions. The verdicts are solid, plausible, shaky, stale or wrong. Brief:
   [briefs/VERIFIER-BRIEF.md](briefs/VERIFIER-BRIEF.md). Wave 5 used
   [briefs/VERIFIER-BRIEF-W5.md](briefs/VERIFIER-BRIEF-W5.md), which quotes the signed lock.
2. **Compile**, from the compiler itself. Every code check a recipe carries runs under
   `rustc 1.98.1 (48a229cea 2026-09-01)` through [scripts/compile_oracle.py](scripts/compile_oracle.py).
   A check is a complete Rust file with an expectation. It compiles (optionally with no warnings), fails
   with a named error code, lint or stderr text, or prints an exact output. A wasm check can also assert
   the module's exports and exact imports, the result of a call through node, or a trap. Each code
   page's caption lists every gate its check carries. Checks may link a
   pinned dependency set that includes rapier3d-f64 0.35.3 + enhanced-determinism, the exact build the
   engine links (see [oracle/Cargo.toml](oracle/Cargo.toml)). The compiler is not a model, so it cannot
   be talked into anything.

**Wave 4 is written by generators outside the Claude family.** Kimi k2.6 wrote three lanes through the
local Ollama daemon (Ollama Cloud), and Gemini 3.1 Pro wrote one through OpenRouter at a dated id. Two
Grok 4.7 attempts produced nothing usable and are recorded in the wave's verification record. The work is
driven by [scripts/openrouter_lane.py](scripts/openrouter_lane.py) under
[briefs/GENERATOR-BRIEF.md](briefs/GENERATOR-BRIEF.md). The harness grounds each generator in source
excerpts read from the local cargo registry at pinned versions, plus reference pages it fetches and hashes
when the model has no search tool, and admits a source only when the conversation shows it was opened. It runs every check through the compiler for bounded revision rounds
and removes what never passes. Its checks link a separate dependency set, `oracle-jam/` (host and
wasm32), selected per check with `"oracle_set": "jam"`. The engine's set is untouched. The same Claude
Sonnet verifier then judges the lane, now across model families.

**Wave 5 is also written outside the Claude family.** Kimi k2.6 wrote two lanes through the same harness,
under [briefs/GENERATOR-BRIEF-W5.md](briefs/GENERATOR-BRIEF-W5.md). The third lane, integer-time, came
from Grok 4.7 in a Cursor chat seat, after Kimi's rounds on it returned no JSON. The seat ran through
[scripts/seat_lane.py](scripts/seat_lane.py), which gives a chat model the harness's own prompts and
applies the harness's own gates to its reply: source admission, the lint, the compiler and the final
admission.

`verified = 1` requires both: a confirming verdict in the ledger (`verification/verdicts.json`, built
by [scripts/build_ledger.py](scripts/build_ledger.py)) **and** no failing code check (the compile gate).
A recipe whose own example fails the compiler is never verified, whatever the retrieval verifier said.
Operator notes (`verification/operator-notes.json`) annotate a verdict and never change it. A recipe
may carry one note or a list. Each note records one of four things:

- `void-correction`: a pipeline defect the verifier could not see;
- `citation-anchor`: the engine commit a citation was checked against;
- `later-measurement`: a later measurement that narrows a verified claim;
- `consumed-pin`: a signed design lock took this recipe as a pin. si-jam-sessions' Phase 0 lock
  (`docs/PHASE-0.md` @ `e3cc85e`) consumed 32 recipes. An edit to one of them is a lock change, raised
  with that project before it lands.

**Wave 5 answers si-jam-sessions' questions after its lock signed.** It has 13 recipes and 19 checks, all
verified. It covers PPQ 3360's tuplet table, the u128 overflow bound and the remainder carry; what midly's
`strict` refuses that the alloc-only build accepts; and an allocation-free audio callback, measured with
a counting allocator. Its checks can link a third dependency set, `oracle-jam-strict/`, which is midly
0.5.3 with `alloc` + `strict`, the law's own configuration. It lives in a separate crate because cargo
unifies features within one build: adding `strict` to the jam set would have changed what every wave-4
midly check measured.

One wave-5 recipe, the SMPTE-refusal export, is marked avoid. A later measurement found that midly 0.5.3
panics on a division word starting 0x80, and the recipe's correction says to refuse before calling midly.
The wave's [verification record](waves/wave-05-si-jam-p2/verification.md) has the evidence.

## Rebuild and extend

```powershell
$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'
python scripts/compile_oracle.py setup                        # once per machine: build the oracle's dependency set
python scripts/assemble_lanes.py --wave N --dir <wave-dir> --date <d> --stage   # lint lanes, write verifier inputs
python scripts/compile_oracle.py run waves/<wave-dir> --date <d>                # the authoritative compiler run
python scripts/assemble_lanes.py --wave N --dir <wave-dir> --date <d> --final   # join verdicts + compiler -> research-raw.json
python scripts/regen.py                                       # ledger -> DB -> catalog -> loadout -> root routers
python ../verify.py                                           # the repo's deterministic floor
```

A research lane follows [briefs/LANE-BRIEF.md](briefs/LANE-BRIEF.md) with its scope from
[briefs/lanes.json](briefs/lanes.json). Its seat runs the oracle on its own lane before handing it in;
that self-check does not count as verification, and the authoritative `run` is made separately.
Generated files are `rust.db`, `catalog/`, `.claude/loadout/index.json` and each wave's
`research-raw.json`. Never hand-edit any of them. Edit the lane files, the verifier files or the
scripts, then rebuild.

## Standards compliance

Scored against the six workflow standards (0 missing, 1 partial, 2 present, 3 exemplary).

- **PIN_PER_STEP: 3.** Every seat is pinned per step. Research is Opus in waves 1-3. In wave 4 it is
  Kimi (`kimi-k2.6:cloud`, digest recorded) and Gemini (`google/gemini-3.1-pro-preview-20260219`) at
  temperature 0. In wave 5 it is Kimi, plus Grok 4.7 in a chat seat, whose receipt hashes the exact
  prompts it was given. Verification is Sonnet. The prompts are the committed `briefs/LANE-BRIEF.md`,
  `briefs/GENERATOR-BRIEF.md`, `briefs/lanes.json` and `briefs/VERIFIER-BRIEF.md`, with wave 5's own
  `-W5` briefs. The receipts for waves 4 and 5 hash each prompt and each source excerpt, and record each
  call's tokens and cost where the seat exposes them. The tool schema is the lane contract in the brief plus the check format in
  the oracle's docstring. The compiler is exact: the oracle refuses any rustc other than 1.98.1, and its
  dependency set is pinned by `oracle/Cargo.lock`, which starts from si-rpg-engine's solver lockfile. The
  receipts record the rustc string of every run.
- **ANDON_AUTHORITY: 3.** Any stage halts the line. The assembler halts on a lint error, a missing
  verifier verdict or an unrun check. The ledger merge halts on a malformed verdict. The compile gate
  refuses `verified` to any recipe whose code fails. `verify.py` blocks publication. Each of these is
  exercised by the smoke run recorded in wave 1's verification record.
- **NAMED_COMPENSATORS: 2.** Building the KB performs no irreversible call: every write is local, and
  git reverts it. The publishing steps are listed below with their undo.
- **DECOMPOSE_BY_SECRETS: 2.** Each lane owns one topic, and each scope names the neighbouring lanes
  that own its exclusions. Research, retrieval verification and compilation are three separate seats
  with separate inputs. The verifier sees citations and checks, never the packet.
- **UNCERTAINTY_GATED_HUMANS: 2.** Humans are asked only about what the gates leave open: refuted or
  shaky recipes, and findings that contradict a dispatch pin. These go to the coordinating session
  (si-rpg-engine or si-jam-sessions), each with a "consistent with / contradicts pin N" line.
- **EXTERNAL_VERIFIER: 3.** The generator never verifies itself. Prose claims go to a different model
  that retrieves the live page; in waves 4 and 5 that is also a different model family. Code claims go to the compiler, which is not a model. Any arXiv or DOI
  citations can additionally pass the prism citation gate.

**Compensators (publishing steps):**

| Action | Undo | State after undo | Owner |
|---|---|---|---|
| `git push` of the KB branch to `readouts-internal` | `git push origin --delete <branch>` (or revert the merge) | branch gone, no KB on the remote | readouts operator |
| Answers sent to the si-rpg-engine coordinator (committed by that seat) | a follow-up message naming the wrong answer; the coordinator reverts its commit | the engine's `docs/rust-kb-answers.md` corrected | this KB's advisor seat |
| Deltas sent to the si-jam-sessions session (waves 4 and 5; its agents turned some into tests) | a follow-up message naming the wrong delta; that session reverts the test or pin that used it | that session's lock and tests corrected | this KB's advisor seat |
| Bug report filed upstream (dimforge/rapier#1019, the character-controller stall) | a comment withdrawing it, then `gh issue close 1019 -R dimforge/rapier` | the issue closed with the reason stated; the public record remains | this KB's advisor seat |
| Generator calls for wave 4 (OpenRouter metered credit: about $5.0, including two Grok calls that produced nothing; Ollama Cloud plan usage for Kimi) | none: spent credit is not returned. Each lane is capped by `--budget`, now also after every call. Every call's tokens and cost are in `waves/wave-04-si-jam-sessions/receipts/`, and the two failed Grok calls are in the verification record | credit spent, receipts kept | this KB's advisor seat |
| Generator calls for wave 5 (Ollama Cloud plan usage for Kimi; one reply from a Cursor chat seat; no OpenRouter spend) | none: plan usage is not returned. Kimi's tokens are in `waves/wave-05-si-jam-p2/receipts/`, and the chat seat's receipt holds its prompt and reply hashes | usage spent, receipts kept | this KB's advisor seat |
| Public mirror via `shared/export_public.py` | revert the export commit on the public repo | the public mirror without this KB | readouts operator |
