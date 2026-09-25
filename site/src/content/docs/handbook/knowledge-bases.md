---
title: The knowledge bases
description: What each knowledge base covers, what it optimises for, and where to start reading.
sidebar:
  order: 3
---

Each KB was built for a job the studio actually had, so each one has a **deciding question**: the axis its verdicts are measured on. Knowing it tells you how to read an entry. A model can be excellent and still rank low in model-knowledge because of its licence.

Current counts live in [`index.md`](https://github.com/mcp-tool-shop-org/readouts/blob/main/index.md), which is regenerated from the databases on every publication. They are not repeated here, so they cannot go stale.

## Game development

### rust-knowledge

Rust for building a deterministic game engine, in three tiers: the essentials, advanced Rust, and how the engine uses it (a raw WebAssembly ABI, float determinism, Rapier physics state and restore, reproducible builds). A fourth tier covers a deterministic music engine: integer time, MIDI and notation ingest, host audio and MIDI, and crate licences.

- **Deciding question:** is it current for Rust 1.98.1, edition 2024 and the pinned crates, and does its code do what it says? Every code check is compiled, and where it says so run, by the pinned compiler.
- **Database:** `rust.db`, entity table `recipes`. **Start at:** `catalog/README.md`.

### godot-knowledge

Godot 4 practice for building a 2.5D turn-based tactical RPG.

- **Deciding question:** currency. Each recipe gets a Godot 4 verdict (solid, plausible, shaky, stale from Godot 3, or wrong).
- **Database:** `godot.db`, entity table `recipes`. **Start at:** `catalog/README.md`.

### blender-knowledge

Blender 4.x practice for a headless sprite-turnaround pipeline (import a generated 3D model, render eight-direction sprites from the command line, composite them into a 2.5D game), plus general game-asset preparation.

- **Deciding question:** currency. Each recipe gets a Blender 4.x verdict, in the same scale as godot-knowledge.
- **Database:** `blender.db`, entity table `recipes`. **Start at:** `catalog/README.md`.

### sprites-knowledge

The craft of turning concept art into a finished 2.5D JRPG sprite on a single-GPU workstation.

- **Deciding question:** how do you get from a concept frame to a game-ready sprite, and how well does this exact approach work on this exact hardware?
- **Database:** `recipes.db`, entity table `recipes`. **Start at:** `catalog/README.md`.

### sprite-motion-knowledge

Animating an approved sprite: walk, swing, idle and death cycles.

- **Deciding question:** how do you make a sprite move without melting the character or detaching its weapon, and how well does the approach hold up?
- **Database:** `recipes.db`, entity table `recipes`. **Start at:** `catalog/README.md`.

## Local AI

### model-knowledge

The best local generative models per purpose (image, editing, control, video, 3D, audio, language, captioning) for a workstation with one 32 GB GPU.

- **Deciding question:** can you use the output commercially (a LoRA or an asset inherits its base model's licence), and does it fit in 32 GB of VRAM?
- **Database:** `models.db`, entity table `models`. **Start at:** `readout/index.md`.

### tensor-engine-knowledge

The engines that run and train AI models locally on an NVIDIA Blackwell GPU under Windows.

- **Deciding question:** does it survive native Windows on Blackwell, and is its licence commercially clean?
- **Database:** `engines.db`, entity table `engines`. **Start at:** `readout/index.md`.

### training-knowledge

The craft of training LoRAs and fine-tunes on one 32 GB GPU: methods, recipes, hyperparameter values, datasets and evaluation. It is the layer between the weights (model-knowledge) and the software (tensor-engine-knowledge).

- **Deciding question:** is the run viable on one GPU, and is it reproducible (fits in memory, commercially clean output, full replay provenance)?
- **Database:** `training.db`, entity table `techniques`. **Start at:** `readout/index.md`.

### docker-knowledge

How to package, measure and place models honestly on one GPU in containers.

- **Deciding question:** what is load-bearing for packaging and placing models on one GPU, measured rather than assumed?
- **Database:** `findings.db`, entity table `findings`. **Start at:** `catalog/README.md`.

## Voice and music

### vocology-knowledge

The sung voice: vocology (the source-filter model, registers, the singer's formant), musical versus speech prosody, aligning lyrics to notes, score-controllable singing synthesis versus lyrics-to-song generators, and how to evaluate them.

- **Deciding question:** does it honour the notes and lyrics of a score as hard constraints, rather than generate a whole song around them? Commercially safe weights come second.
- **Database:** `findings.db`, entity table `findings`. **Start at:** `catalog/README.md`.

## Ledgers

### xrpl-knowledge

The XRP Ledger ecosystem for a builder: protocol features, transaction types, XLS standards, client libraries and tooling, across mainnet, Xahau and Hooks, the XRPL EVM sidechain, and the institutional layer.

- **Deciding question:** is this feature actually enabled on mainnet right now, or pending, devnet-only or deprecated? Which standard or library is current?
- **Database:** `xrpl.db`, entity table `capabilities`. **Start at:** `readout/index.md`.
