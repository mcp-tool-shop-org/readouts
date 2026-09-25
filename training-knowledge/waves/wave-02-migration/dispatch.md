# Wave 2 — Migration (rig-measured training-craft recipes from tensor-engine)

> Migration dispatch · 2026-06-06 · training-knowledge KB.

**Goal:** execute the boundary decision — move the portable TRAINING-CRAFT recipes out of tensor-engine `config_recipes` and into training-knowledge as techniques, leaving engine setup/toolchain + baseline measurement receipts where they belong.

**Method:** a classify → dedup/assemble → adversarial-verify (Sonnet) workflow over the 28 training-shaped recipe rows. Each candidate was classified migrate (craft) vs stays (setup/baseline); craft rows were structured into techniques (hparams extracted from the measured body), deduplicated across engine lanes and against wave 1, then verified.

**Result:** **12 techniques** migrated into the `llm-finetune` lane (all verified, 0 refuted). The six engine-lane copies of the Unsloth QLoRA-14B recipe collapsed into one; the kohya/chroma/ms-swift/fsdp2 recipes already anchored in wave 1 were dropped as duplicates. RL/GRPO methods (verl, openrlhf, skyrl, open-instruct) and the llama.cpp export bridge were shelved in `llm-finetune` (the lane that covers SFT + preference + RL).

**What stayed in tensor-engine:** engine setup/toolchain (driver/CUDA, cu128 torch base, WSL2 setup, cu128 nightly) and the baseline measurement receipts (#150/#165/#167) — those are engine territory, not portable training craft.

_Note: the classify phase's input list didn't reach the workflow (an args-passing glitch); the assemble agent recovered by reading `engines.db` directly and produced the migration, which was then verified._

## Wave-2 evidence-strength distribution

| Tier | Count |
|---|--:|
| measured-on-rig | 1 |
| reproduced-from-source | 11 |
