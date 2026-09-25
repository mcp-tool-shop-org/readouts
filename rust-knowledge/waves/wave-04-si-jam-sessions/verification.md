# Wave 4 — verification record

**Date:** 2026-09-25 · **Wave:** `wave-04-si-jam-sessions` · 4 lanes · 37 recipes · 74 warrant-source rows · 27 code checks.

Tallies come from `scripts/wave_tallies.py --wave-dir wave-04-si-jam-sessions --date 2026-09-25`.

## Who generated, who verified

This is the first wave written by generators outside the Claude family. It ran through `scripts/openrouter_lane.py` under `briefs/GENERATOR-BRIEF.md`.

| Lane | Generator | Calls | Tokens in / out | OpenRouter cost | Harness |
|---|---|---|---|---|---|
| midi-notation-ingest | Gemini 3.1 Pro, `google/gemini-3.1-pro-preview-20260219` | 2 | 187,278 / 16,195 | $0.569 | v1, then re-admitted under v3 rules |
| integer-time | Kimi k2.6, `kimi-k2.6:cloud` (Ollama Cloud, digest `a90cd0d1…`) | 3 + 1 revision | 112,180 / 40,816, then 36,811 / 8,954 | none (plan) | v3, then `--revise` |
| host-audio-and-midi | Kimi k2.6 | 2 | 161,930 / 29,465 | none (plan) | v3 |
| crate-licences | Kimi k2.6 | 1 | 16,094 / 19,754 | none (plan) | v3 |

The attempts that did not produce a lane are recorded here, because they cost money or changed the harness:

- **Grok 4.7** (`x-ai/grok-4.7-20260916`), for integer-time and host-audio-and-midi.
  - Each call returned two JSON objects instead of one lane, so neither lane was produced.
  - The two calls cost $1.759 and $2.254. The first harness wrote no receipt when it halted; the costs come from its logs.
- **Gemini 3.1 Pro, first licences draft** ($0.214). It was superseded because it padded its checks with empty programs and cited pages that do not state its claims. Its lane, packet and receipt are in `superseded/`.
- **Two harness-v2 re-runs** were refused with HTTP 402: the account's in-flight budget was exhausted, so nothing was spent.
- **Totals.** OpenRouter spend for the wave was about $5.0 including probes. The account then had $3.50 of credit left, and the operator moved generation to Kimi on Ollama Cloud.

The verifier is unchanged from waves 1–3: Claude Sonnet, reasoning-stripped, reading only citations and checks. For this wave it is also a different model family from every generator.

The non-model witness is `rustc 1.98.1` through `scripts/compile_oracle.py`, with the new `jam` dependency set (see `dispatch.md`).

## Gate 1 — retrieval verifier

| Lane | Confirmed | Corrected | Refuted | Unfindable | Solid / plausible / shaky-or-worse | Sources ✓ / ✗ |
|---|---|---|---|---|---|---|
| midi-notation-ingest | 4 | 2 | 1 | 0 | 4 / 2 / 1 | 14 / 0 |
| integer-time | 7 | 3 | 0 | 0 | 3 / 7 / 0 | 18 / 2 |
| host-audio-and-midi | 6 | 4 | 0 | 0 | 6 / 3 / 1 | 20 / 0 |
| crate-licences | 8 | 2 | 0 | 0 | 6 / 2 / 2 | 20 / 0 |
| **total** | **25** | **11** | **1** | **0** | 19 / 14 / 4 | 72 / 2 |

**Refuted (1).** In midi-notation-ingest, the ABC recipe's determinism guard cannot be written against abc-parser 0.4.0. `Length` wraps an `f32` in a private field and has no `Mul` impl. The verifier's compiler counter-examples gave E0369 and E0616.

**Corrected (11):**

- **midi-notation-ingest ×2:**
  - quick-xml 0.42 is not no_std; it uses std unconditionally.
  - Without midly's `strict` feature, malformed input never errors, so "treat Err as fatal" is no substitute for `strict`.
- **integer-time ×3.** All three are citation precision.
  - The u24 tempo and u28 delta are defined in midly's `event.rs`, not `primitive.rs`.
  - The u128 doc page was used as a filler second source.
  - The u128-in-an-export recipe missed the i128 ABI note. The verifier confirmed that recipe's gotcha with its own counter-example: an `extern "C" fn(u128) -> u128` compiles with no lint, and its wasm export takes 3 parameters.
- **host-audio-and-midi ×4.** Each is an uncited platform explanation added on top of correct code facts.
  - `StreamInvalidated` maps AUDCLNT_E_RESOURCES_INVALIDATED; it does not mean a default-device change.
  - rtrb's methods are `push`/`pop` (the `try_*` names belong to ringbuf), and ringbuf's `HeapRb` needs `alloc`, not `std`.
  - midir's stable port `id()` comes from `DRV_QUERYDEVICEINTERFACE`.
  - The assert_no_alloc check never registered `AllocDisabler`.
- **crate-licences ×2.** Both are cargo-deny TOML syntax. Exceptions are keyed by `name`, not `crate`. `clarify` takes a top-level `name` and `expression`, with `license-files = [{ path, hash }]`.

**Systemic weaknesses the verifiers named:**

- **midi-notation-ingest:** the jam set builds only midly in its law configuration. The other crates are built with default features, so non-default configurations are mechanically untested. Both corrections sat there.
- **integer-time:** citation imprecision inside a correct lane. Every number reproduced exactly; 18 counter-examples found nothing wrong.
- **host-audio-and-midi:** correct code facts, plus uncited platform semantics layered on top. All four corrections were in that layer.
- **crate-licences:** no machine check. A cargo-deny dry run would have caught both TOML errors, but cargo-deny is not installed here and was not installed.

## Gate 2 — the compiler

`rustc 1.98.1` ran **27 checks: 27 pass, 0 fail.** By lane:

| Lane | Checks | Recipes with checks |
|---|---|---|
| host-audio-and-midi | 11 | 10 |
| integer-time | 9 | 9 |
| midi-notation-ingest | 7 | 7 |
| crate-licences | 0 | 0 (licence terms are not code; correctly left unchecked) |

Results are in `verification/compile-2026-09-25/wave-04-si-jam-sessions.json`.

**One operator check was added after the verdicts.** It was added through `scripts/tighten_checks.py`, like wave 3's wasm-raw-abi checks. It turns the host lane's weakest claim into a compiler-shown fact:

- **Setup:** `AllocDisabler` is registered as `#[global_allocator]`.
- **Result:** an allocation outside `assert_no_alloc` is allowed, and one inside aborts. stdout is exactly `before`, and the exit status is 3221226505, Windows' abort status, as in two wave-1 checks.
- **Planted run:** expecting exit 0, it failed.
- **Scope:** this is the oracle's debug build. The crate's default `disable_release` makes the guard a no-op in release, which the recipe already says.
- **Operator error:** the first attempt used `stderr_contains` for the runtime abort message. That gate reads rustc's stderr, not the program's, so the check failed until the gate was removed.

## Pipeline notes

**The OpenRouter web plugin's default engine did nothing for Gemini.** The prompt was 27 tokens and there were no citations. `engine: "exa"` injected results and citations for Gemini and Grok alike (probed). The harness now pins `exa`.

**Generators pad.** Gemini's first licences draft carried checks that assert nothing (`fn main() {}`, `use midly as _;`). It also answered the downgrade of its unbacked citations by citing other excerpts that do not state the claim. The fixes:

- The harness refuses a `compiles` check with no gate and only empty bodies.
- The lint (`assemble_lanes.py`) now requires two **distinct** warrant URLs. The midi lane had one recipe citing the same page twice; none of waves 1–3 did.
- The feedback now tells the model to drop a recipe rather than pad it.

**An expected output on a check that never runs was never compared.** Kimi's first integer-time draft put `stdout` values on three `compiles` checks, including the two central conversions.

- The oracle now refuses `stdout`, `stdout_contains` or `exit_code` on a check whose `expect` is not `runs`. No check in waves 1–3 had the pattern.
- `--revise` sent Kimi only the three objections. It returned real wasm32 runs, called through node: 500000, 24000 and 1.

**Grok 4.7 was expensive and unparseable here.** Each call cost 7–9× the lane estimate, and each emitted two JSON objects. The fixes:

- The harness now takes the first object that holds `recipes`.
- It writes a receipt on every exit.
- It stops right after any call that alone exceeds the lane budget.

**Ollama Cloud has no search tool.** For Kimi, the harness fetched a pinned list of reference pages, stripped each to text, cut it at a named section, and hashed it into the receipt:

- the Cargo profiles and Rust reference pages, and the std integer docs;
- rustc's wasm32 platform page;
- Microsoft Learn's WASAPI and WinMM pages;
- the cargo-deny and cargo-about docs;
- SPDX BSD-1-Clause and Unlicense, and the MPL-2.0 FAQ.

This is more reproducible than a search plugin: the receipt names exactly which bytes the model saw.

**Receipts.** Each lane's receipt records every call's model, tokens and cost, the prompt and brief hashes, the pack manifest with a SHA-256 per excerpt, and the harness's own hash. It also records whether the lane was re-admitted (`--readmit`) or revised (`--revise`).

## Post-ingest

`load_db.py` ingested 37 recipes, 27 checks and 74 source rows. 36 are verified; the refuted ABC recipe is not. `meta.latest_wave` is 4. The knowledge base now holds:

- 267 recipes, 266 of them verified;
- 970 checks, all passing.

## What may lock architecture

Nothing in this tier locks yet: every recipe names an item of si-jam-sessions' unsigned lock. When the lock signs:

- **Candidates to become load-bearing:** the 19 solid recipes, above all the integer-time rules and midly's law configuration. The integer-time rules are the u128 floor, the remainder carry, the tuplet divisibility, checked overflow, and no u128 in an export.
- **Advisory:**
  - the 14 plausible recipes;
  - the four at shaky or worse, among them the refuted ABC recipe and the corrected WASAPI error-mapping recipe;
  - every behaviour claim about the audio and MIDI crates, which the oracle cannot run without a device;
  - every licence claim, which is not legal advice.
