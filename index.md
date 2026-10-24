# readouts

> A monorepo of verified, ai-loadout-routed SQLite knowledge bases for the studio. Each KB grows in waves of parallel research cross-checked by an adversarial retrieval verifier — full per-wave provenance, every fact flagged verified, two-level progressive-disclosure routing so an agent reads only the slice it needs, never the whole corpus.
>
> **12 knowledge bases · 2644 entries · 1876 verified · 143 domains · 134 waves · generated 2026-10-24.**

## Knowledge bases

| Knowledge base | What | Domains | Entries | Verified | Waves | Front door |
|---|---|--:|--:|--:|--:|---|
| [agent-tooling-knowledge](agent-tooling-knowledge/) | Measured and documented behaviour of the harnesses that run AI agents: Claude Code headless and MCP, permissions and containment, agent sandboxes, agent tracing. | 4 | 18 findings | 18/18 | 1 | [index.md](agent-tooling-knowledge/catalog/README.md) · [json](agent-tooling-knowledge/.claude/loadout/index.json) |
| [blender-knowledge](blender-knowledge/) | current, web-grounded Blender 4.x practice for the studio's headless sprite-turnaround render pipeline (import a TRELLIS-generated GLB → render 8-direction sprites via blender --background --python → composite into a 2.5D game) plus general game-asset prep. | 10 | 219 recipes | 83/219 | 8 | [index.md](blender-knowledge/catalog/README.md) · [json](blender-knowledge/.claude/loadout/index.json) |
| [docker-knowledge](docker-knowledge/) | The knowledge base behind the gpu-container product — how to package, measure, and place models honestly on one GPU. | 6 | 160 findings | 73/160 | 9 | [index.md](docker-knowledge/catalog/README.md) · [json](docker-knowledge/.claude/loadout/index.json) |
| [godot-knowledge](godot-knowledge/) | current, adversarially-verified Godot 4 dev knowledge for building a 2.5D turn-based tactical RPG. | 6 | 177 recipes | 108/177 | 7 | [index.md](godot-knowledge/catalog/README.md) · [json](godot-knowledge/.claude/loadout/index.json) |
| [model-knowledge](model-knowledge/readout/index.html) | Verified knowledge base of the best local generative-AI MODELS per purpose (image / edit / control / video / 3D / audio / LLM / caption) for the RTX 5090 rig — commercial-license-first. | 9 | 130 models | 127/130 | 23 | [index.md](model-knowledge/readout/index.md) · [json](model-knowledge/readout/index.json) |
| [rust-knowledge](rust-knowledge/) | Verified Rust for building si-rpg-engine (essentials, advanced, and how the engine uses it: raw wasm ABI, float determinism, Rapier 0.35 state and restore, reproducible bytes) and a first tier for si-jam-sessions' music law, with every code check run by the pinned rustc 1.98.1. | 27 | 280 recipes | 279/280 | 5 | [index.md](rust-knowledge/catalog/README.md) · [json](rust-knowledge/.claude/loadout/index.json) |
| [sprite-motion-knowledge](sprite-motion-knowledge/) | The portable animate-the-sprite craft for this rig | 19 | 246 recipes | 170/246 | 8 | [index.md](sprite-motion-knowledge/catalog/README.md) · [json](sprite-motion-knowledge/.claude/loadout/index.json) |
| [sprites-knowledge](sprites-knowledge/) | The portable concept-art → game-ready 2.5D JRPG sprite craft for this rig | 8 | 215 recipes | 182/215 | 6 | [index.md](sprites-knowledge/catalog/README.md) · [json](sprites-knowledge/.claude/loadout/index.json) |
| [tensor-engine-knowledge](tensor-engine-knowledge/readout/index.html) | Verified knowledge base of the ENGINES that run & train AI models locally on the RTX 5090 (Blackwell / sm_120 / Windows) rig. | 10 | 193 engines | 134/193 | 21 | [index.md](tensor-engine-knowledge/readout/index.md) · [json](tensor-engine-knowledge/readout/index.json) |
| [training-knowledge](training-knowledge/readout/index.html) | Verified knowledge base of portable TRAINING CRAFT — methods, recipes, hyperparameter values, dataset & eval know-how — for training LoRAs / fine-tunes on the single RTX 5090 (Blackwell / Windows / WSL2) rig. The how-to-train layer between the weights (model-knowledge) and the software (tensor-engine-knowledge). | 13 | 222 techniques | 119/222 | 19 | [index.md](training-knowledge/readout/index.md) · [json](training-knowledge/readout/index.json) |
| [vocology-knowledge](vocology-knowledge/) | sung-voice craft: vocology (source-filter, registers, singers formant), musical vs speech prosody, lyric-to-note alignment, score-controllable SVS vs lyrics-to-song generators, admission/teaching evaluation | 19 | 324 findings | 221/324 | 15 | [index.md](vocology-knowledge/catalog/README.md) · [json](vocology-knowledge/.claude/loadout/index.json) |
| [xrpl-knowledge](xrpl-knowledge/readout/index.html) | Verified knowledge base of the XRP Ledger ECOSYSTEM for a builder — protocol features, transaction types, XLS standards, client libraries & tooling — each tagged with its current mainnet / amendment status. Whole-ecosystem: XRPL mainnet + Xahau/Hooks + the XRPL EVM sidechain + the institutional layer (RLUSD, compliance). | 12 | 460 capabilities | 362/460 | 12 | [index.md](xrpl-knowledge/readout/index.md) · [json](xrpl-knowledge/readout/index.json) |

## For agents

- **Route to the right KB:** `ai-loadout resolve --project .` — the root loadout picks the KB, then the KB's own loadout picks the domain slice (two-level progressive disclosure; the corpus is never dumped whole).
- **Each KB's front door:** `<kb>/readout/index.md` (text map) · `index.json` (programmatic) · `index.html` (branded landing).
- **Query a KB directly** — open its SQLite DB (views `v_recommended`, `v_best_for`; FTS `<table>_fts`):
  - `agent-tooling-knowledge/findings.db` — FTS `findings_fts`
  - `blender-knowledge/blender.db` — FTS `recipes_fts`
  - `docker-knowledge/findings.db` — FTS `findings_fts`
  - `godot-knowledge/godot.db` — FTS `recipes_fts`
  - `model-knowledge/models.db` — FTS `models_fts`
  - `rust-knowledge/rust.db` — FTS `recipes_fts`
  - `sprite-motion-knowledge/recipes.db` — FTS `recipes_fts`
  - `sprites-knowledge/recipes.db` — FTS `recipes_fts`
  - `tensor-engine-knowledge/engines.db` — FTS `engines_fts`
  - `training-knowledge/training.db` — FTS `techniques_fts`
  - `vocology-knowledge/findings.db` — FTS `findings_fts`
  - `xrpl-knowledge/xrpl.db` — FTS `capabilities_fts`
- **Programmatic monorepo map:** `index.json` (the data backing this page).

## How each KB decides

- **agent-tooling-knowledge** — decisive axis: Measured and documented behaviour of the harnesses that run AI agents: Claude Code headless and MCP, permissions and containment, agent sandboxes, agent tracing.
- **blender-knowledge** — decisive axis: currency — the Blender-4.x verdict (solid / plausible / shaky / blender3_stale / wrong).
- **docker-knowledge** — decisive axis: The knowledge base behind the gpu-container product — how to package, measure, and place models honestly on one GPU.
- **godot-knowledge** — decisive axis: currency — the adversarial Godot-4 verdict (solid / plausible / shaky / godot3_stale / wrong).
- **model-knowledge** — decisive axis: commercial license (a LoRA/asset inherits its base model's license) + fits 32 GB VRAM.
- **rust-knowledge** — decisive axis: two verdicts: currency against Rust 1.98.1 / edition 2024 / the pinned crates (adversarial retrieval verifier), and every code check compiled and run by the pinned compiler (a non-model verifier).
- **sprite-motion-knowledge** — decisive axis: how do I make an approved 2.5D JRPG sprite walk, swing, idle, and die — without melting the character or detaching the weapon — and how well does this exact approach hold up?
- **sprites-knowledge** — decisive axis: how do I turn a concept-art frame into a finished game sprite, and how well does this exact approach work on this exact rig?
- **tensor-engine-knowledge** — decisive axis: native-Windows Blackwell survivability + commercial license (a LoRA/app inherits its engine's license).
- **training-knowledge** — decisive axis: single-RTX-5090 training viability + reproducibility (fits 32 GB, commercial-clean output, complete replay provenance) — which method/recipe/data/eval you feed the engine and why, not which weights or which software.
- **vocology-knowledge** — decisive axis: score-lock — honor MIDI notes + lyrics as hard constraint vs mixed-song generator; secondary commercial-safe weights
- **xrpl-knowledge** — decisive axis: network_status — is this feature ACTUALLY enabled on XRPL mainnet right now (vs amendment-pending / devnet-only / deprecated), and which standard/library is current — plus which of the four build-focus tracks (game economies / NFT assets / payments / identity-compliance) it serves.

## Provenance

Every fact in every KB carries a **wave id** and a **verified** flag. Sources are retrieval-checked against the live page; some waves add a cross-family seat, and each wave's own receipt says which — see `waves.verifier_note`. Family-different verification across every wave is the planned upgrade, not the current state. 134 research waves across 12 knowledge bases; 1876/2644 entries verified.
