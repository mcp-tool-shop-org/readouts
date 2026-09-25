# Wave 2 — Verification receipt (migration)

> Adversarial verifier (Sonnet): faithfulness to the measured recipe + correct lane + boundary · 2026-06-06.

## Verdict distribution

| Verdict | Count |
|---|--:|
| confirmed | 11 |
| confirmed-with-fixes | 1 |

## Hard-deleted from tensor-engine `config_recipes` (Mike's call, 2026-06-06)

The craft of these **17** rig-measured recipes now lives in training-knowledge; the rows were removed from `engines.db` (177 → 160) so a recipe is authoritative in exactly one KB. Each migrated technique carries the measured specifics it established; its `engine_recipe_ref` now reads as **historical provenance** (the receipt was migrated and removed), not a live pointer. The pre-deletion engine state is recoverable from commit `632166e`.

- `training-unsloth-windows-native-qlora-14b-32gb-daily-driver`
- `runtime-foundations-unsloth-qlora-14b-wsl2-fine-tune-a-14b-in-32-gb-vram-paged-adamw-8bit`
- `llm-serving-unsloth-qlora-14b-in-32gb-vram-windows-or-wsl2`
- `llm-inference-unsloth-blackwell-qlora-14b-in-32gb-vram`
- `quantization-unsloth-qlora-14b-32gb-blackwell`
- `attention-kernels-recipe-unsloth-qlora-14b-32gb-paged-adamw8bit`
- `training-unsloth-llm-qlora-baseline-native-win-5090-qwen3-4b`
- `training-native-windows-qlora-on-the-5090-no-wsl2-trl-peft-bitsandbytes-liger`
- `training-axolotl-wsl2-qlora-yaml-flash-attn-cu128`
- `training-llama-factory-wsl2-qlora-yaml-32b-and-full-sft-8b`
- `training-trl-unsloth-dpo-preference-tuning-no-ray-cheapest-path`
- `training-ms-swift-install-windows-native-the-one-to-run-first-on-this-rig`
- `training-llamacpp-blackwell-build-and-lora-export-merge`
- `training-verl-wsl2-single-5090-grpo-lora-qwen-1-5b-to-7b`
- `training-openrlhf-wsl2-ray-vllm-deepspeed-7b-grpo`
- `training-skyrl-wsl2-agentic-rl-setup-research-wsl2-only`
- `training-open-instruct-wsl2-rlvr-reference-study-adapt-wsl2`
