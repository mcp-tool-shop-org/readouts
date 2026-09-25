# Wave 1 — Foundation (thin, prove-the-partition)

> Study-swarm dispatch · 2026-06-06 · training-knowledge KB · 8 lanes, breadth-first.

**Goal:** stand up KB #4 and PROVE the lane partition is MECE by seeding every lane with current (2026) training craft, deeply sourced and adversarially verified — not exhaustively, but enough that the schema and boundary hold under real data.

**Method:** 8 parallel lane researchers (general-purpose, web-grounded) → one adversarial verifier per lane (different tier: Sonnet; currency + boundary-vs-sibling-KBs + citation-evidence lenses) → assembled into `research-raw.json`. Diffusion/LLM/efficiency lanes anchored at least one **measured-on-rig** technique to a tensor-engine `config_recipes` slug via `engine_recipe_ref` (the cross-KB seam; measured it/s + VRAM peaks stay in tensor-engine, referenced not restated).

**Boundary discipline:** base weights referenced by slug only (model-knowledge owns them); trainer software and rig-measured receipts stay in tensor-engine; eval tools cited as instruments, not catalogued; no per-recipe VRAM scalar (efficiency lane owns the arithmetic).

## Lanes dispatched

| # | Lane | Techniques | Datasets | Cross-cut failures |
|---|---|--:|--:|--:|
| 1 | PEFT methods & adapter theory | 5 | 0 | 3 |
| 2 | SDXL style-LoRA recipes (priority) | 4 | 2 | 4 |
| 3 | Flux-family style-LoRA recipes | 4 | 2 | 2 |
| 4 | Dataset construction & caption craft | 4 | 1 | 3 |
| 5 | Local LLM fine-tuning (SFT + preference + RL) | 3 | 3 | 3 |
| 6 | Single-GPU efficiency & training-VRAM technique | 4 | 0 | 3 |
| 7 | Training evaluation & validation methodology | 4 | 1 | 4 |
| 8 | Failure modes & debugging | 4 | 2 | 6 |

## Standards compliance (workflow-standards.md), 0–3

- **PIN_PER_STEP 3** — every technique carries seed/runs/tuning-budget/evidence_strength + engine_recipe_ref version pin; evals pin task/prompt/n_shot/precision/seed.
- **EXTERNAL_VERIFIER 3** — a different-tier (Sonnet) adversarial verifier per lane, reasoning-stripped; the generator never graded itself.
- **ANDON_AUTHORITY 3** — a refuted core claim is halted at the gate: `load_db.py` EXCLUDES refuted techniques from the KB (1 excluded this wave).
- **DECOMPOSE_BY_SECRETS 3** — portable craft here; measured numbers in tensor-engine; weights in model-knowledge; placement in docker-knowledge. `engine_recipe_ref` is the seam.
- **UNCERTAINTY_GATED_HUMANS 2** — evidence_strength ordinal + verified flag surface low-confidence rows for human review; gate not yet automated.
- **NAMED_COMPENSATORS 3** — read-only/idempotent build (waves append; load_db replaces only its own wave; undo = re-run regen or git checkout).

