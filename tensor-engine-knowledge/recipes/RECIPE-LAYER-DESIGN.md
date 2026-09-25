# Typed recipe layer — design (engine-room knowledge side)

> **STATUS: PROPOSAL for Mike's review.** Nothing merged into `../schema.sql`, nothing
> loaded into `engines.db`, nothing committed. This is the "schema first" slice: lock the
> shape, prove it's polymorphic, *then* backfill + wire the executor.

## What this is

`engine-room` (the executor — a separate org tool, `mcp-tool-shop-org/engine-room`) needs to
**read a recipe and materialize / launch / measure it**. The 177 `config_recipes` we have are
**prose** (`body` text a human hand-runs). This layer is the structured form.

It is the **KNOWLEDGE half** of the Parnas split (the design study-swarm's load-bearing call):

| | KNOWLEDGE — lives **here** (`tensor-engine-knowledge`) | ACTION — lives in **engine-room** |
|---|---|---|
| What | the verified, sourced, **abstract** recipe + measured baseline **targets** + declared compensators | the resolved **lock**, the **ledger**, the live `instance_id`, the reconcile loop, the measure harness |
| Changes when | an **upstream engine** changes (new llama.cpp build, a CUDA rule flips) | the **rig** changes (driver bump, CUDA swap, WSL version) |
| Nature | re-verifiable, replayable, read-only | side-effecting, partly irreversible, rig-specific |

The seam: engine-room reads a recipe row → resolves it against the live rig into a lock + `instance_id` → runs the lifecycle → writes the measured result **back** as a new baseline observation. Knowledge is audited; action is compensated.

## The schema

Full DDL: [`recipes.schema.sql`](recipes.schema.sql) (idempotent `CREATE … IF NOT EXISTS`, foldable into `../schema.sql`). The spine is `recipes`, polymorphic over `recipe_kind`; everything else hangs off it.

Every non-obvious table answers a **specific break** the adversarial pass found in the live DB (run `wf_46ad6900-7d9`):

| Table / column | Adversarial break it closes |
|---|---|
| `recipe_kind` enum + `recipe_targets` | **#1 (HIGH)** the 22 `kernel-lib` rows (SageAttention, Nunchaku, cuDNN-SDPA, torchao) are **modifiers**, not port-serving engines — value is a *delta* on another recipe |
| `recipe_kind='batch-producer'` + per-recipe `measured_axis` | **#2 (HIGH)** quantizers/trainers **terminate after writing a file**; metric is perplexity/bits/it-s, not tok/s |
| `recipe_baselines` keyed by `(recipe, model, ctx)` | **#3 (HIGH)** same binary = 138 vs 60 vs 57 tok/s across models — a recipe-only baseline false-halts |
| `recipe_baselines.compat_band` | repro-drift: hash a **semantic band** (`driver>=R570`), not the literal driver (581→610.47 already happened) |
| `recipe_artifacts.store_expect` + `sha256` | repro-drift: cu128 wheel URLs are **dead**; only `mirror`/`local-vendored` pins are reproducible |
| `recipe_constraints` (`abi_equal`, `defect_floor`) | the most common Blackwell failure is a wheel/torch **ABI mismatch** that passes every `>=` check then DLL-fails |
| `recipe_golden.modality` | diffusion/speech have **no `torch.allclose` golden** — gate is pluggable (numeric \| perceptual \| WER \| audio-fp \| file-hash) |
| `recipe_compensators.compensatable` | no-skip: **name** even the non-undoable (`wsl --update` is machine-global → `non-compensatable`, owner=human) |
| `verified` + `resolvable_*` | `config_recipes` has no `verified` today; and **resolvability ≠ groundedness** — see below |

## Resolvability is a new deterministic floor (not a new bolt-on)

The KB's verifier arc (waves 9–14) is defense-in-depth: deterministic existence/numeric floors → 3-family LLM panel → orthogonal NLI floor → **0-false-confirm** across domains. That panel checks **prose groundedness** — it can't tell you a pinned wheel got yanked.

So the recipe layer adds **one more deterministic floor in the same tradition**: a **resolvability floor** (`recipe_artifacts.resolvable_ok`, set by HTTP HEAD / `docker manifest inspect` / `pip download --dry-run`). It's **refute-or-abstain** like the existence/numeric floors — a 404 is a *proof* of un-resolvability; otherwise it abstains — so it **cannot add a false-confirm**. A recipe can be `verified=1` (prose grounded) yet `resolvable_ok=0` (un-installable); both signals matter, and they're orthogonal.

## Cross-KB seam (training-knowledge KB #4)

A training job isn't self-contained in tensor-engine — it's **(engine recipe → tensor-engine) ×
(technique + hparams + dataset + eval → training-knowledge)**. KB #4 already points back via
`techniques.engine_recipe_ref` (a tensor-engine recipe slug, set on 20/70 techniques). That
forward ref is the **single source of truth**; the reverse pointer is *generated*, not
hand-maintained:

- `recipe_techniques` (recipe_id → KB #4 `technique_slug`, denormalized name + lane) is the
  reverse mirror. **Do not hand-edit** — `recipes/_link_techniques.py` derives it from KB #4's
  `engine_recipe_ref` (idempotent), so the two sides can't drift.
- The join is now explicit + bidirectional: a recipe resolves its techniques, and a technique
  resolves its engine recipe — engine-room reads both KBs to run a training `batch-producer`.

**Integrity dividend:** making the join explicit immediately caught **17 dangling forward-refs**
— KB #4 techniques pointing at tensor-engine recipe slugs that don't exist in the current corpus
(triaged by `recipes/_reconcile_refs.py`: all "missing," 0 renames). These are training-engine
recipes KB #4 expects (axolotl, llama-factory, verl, openrlhf, skyrl, open-instruct, the unsloth
native-win/wsl2 variants, ms-swift-install, trl-unsloth-dpo, llamacpp-lora-export) that
tensor-engine hasn't authored yet. Reconciliation (add the engine recipes vs repoint the refs)
is a content decision, tracked separately from this schema work.

## Proof it's polymorphic

[`_validate_schema.py`](_validate_schema.py) builds a throwaway DB and inserts three exemplars from **real wave-4/5 data** — a launchable server (llama.cpp→llama-swap), a batch-producer (GGUF imatrix quantize), and a modifier (SageAttention 2.2) — then runs the queries the old launchable-only schema would have failed. `PASS`, exit 0:

```
[break#1] modifier: backend=None relation=modifies->comfyui-zimage-turbo top-delta=29.3% faster
[break#2] producer: axis=bits_per_weight produces=gguf golden=file-hash
[break#3] launchable: 2 model-keyed tok/s baselines (compat-band, not literal driver)
[repro]   index-only (non-reproducible) pins: 0  (all exemplars vendored)
[comp]    global-PATH-mutating steps: 0  (per-instance shims instead)
```

## Backfill + integration plan (after sign-off)

1. **Fold** `recipes.schema.sql` into `../schema.sql` (idempotent — safe).
2. **Backfill** the 177 prose `config_recipes` → `recipes` rows; the `kind='baseline'` rows (the measured wave-4/5 numbers) → `recipe_baselines`. The `body` prose is preserved verbatim as the human source of truth. This is a bulk classify+extract job — a good candidate for the **ollama-intern** (local 8B) so it doesn't burn Claude context; every extracted row gets the resolvability floor + a `verified` pass.
3. **Extend** `load_db.py` to ingest a typed recipe payload (don't fork it — add a `recipes` branch alongside the `extras→config_recipes` one).
4. **Extend** `gen_catalog.py` / the shared `gen_readout.py` profile to render the recipe layer (the readout already renders the KB; recipes become a new section, not a new generator).
5. `config_recipes` stays as the prose archive until the backfill is verified, then is deprecated (not dropped — provenance).

## Standards compliance (per `.claude/rules/workflow-standards.md`)

This file is a **schema + a read-only validator** — it performs no irreversible tool calls itself. Scores below are for the recipe-layer *design*; the runtime enforcement (the 3s) lands in engine-room's executor, a named future phase.

| Standard | Score | Evidence |
|---|---|---|
| **PIN_PER_STEP** | **2** | Schema carries the pins (`recipe_artifacts.sha256` + `store_expect`), the `compat_band`, and **model in the baseline closure**. The actual lock-vendoring + `instance_id` hashing is action-side. *Remediation:* engine-room lock/vendor (executor phase). |
| **ANDON_AUTHORITY** | **2** | Halt **inputs** are first-class data (`resolvable_ok`, `verified`, baseline `bound_dir`, `golden`). A recipe with `resolvable_ok=0` is a halt signal. Enforcement of the halt is action-side. *Remediation:* executor reconcile loop. |
| **NAMED_COMPENSATORS** | **2** | `recipe_compensators` **requires** every recipe to declare undo + post_state + owner + `compensatable`; the exemplar shows per-instance shims (no PATH mutation) and identity-verified kill. Declaration is here; no-skip *execution* is action-side. *Remediation:* executor runs them newest-first from the ledger. |
| **DECOMPOSE_BY_SECRETS** | **3** | The whole design is this — the schema deliberately **excludes** lock/ledger/`instance_id`/status (action-side) and keeps only knowledge. Parnas, earned. |
| **UNCERTAINTY_GATED_HUMANS** | **2** | Schema supports it (`verified`, `resolvable_ok`, `compensatable='human-gated'` for `wsl --update`). The contrastive checkpoint is executor-side. *Remediation:* executor gate + contrastive framing. |
| **EXTERNAL_VERIFIER** | **3** | Two orthogonal floors: the KB's existing **family-different groundedness panel** sets `verified`; a **new resolvability floor** (refute-or-abstain, can't add a false-confirm) sets `resolvable_ok`. Different mechanism, in the wave-9–14 tradition. |

No score below 2; each `2` has a named remediation owned by the engine-room executor phase. **Compensators note:** this file makes no irreversible calls, so the no-skip *execution* bar doesn't bind it — but it is the substrate where each recipe's compensators are declared, which the executor enforces.

## Open questions (from the design synthesis, for the executor phase)

- **Baseline re-bless authority** when a re-measure lands outside tolerance for a *legitimate* rig change (driver bump) — auto-append a new `instance_id` baseline, or human checkpoint? (Lane-4 says never auto-overwrite a golden.)
- **Cross-recipe ordering** for `router-fleet`/`python-proxy` (LiteLLM→upstreams): `recipe_targets.depends_on` + `start_order` express it, but the executor's reconcile loop must refcount shared upstreams before teardown — bounded DAG, not a general scheduler.
- **Lock staleness policy**: a 6-month-old lock may point at a yanked wheel. The `resolvable_ok` floor *detects* it; the executor needs a designed **re-resolve → new `instance_id` → re-measure** lifecycle with logged lineage (not hard-fail-forever).
