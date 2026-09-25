<p align="center">
  <a href="README.md">English</a> | <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/readouts/readme.png" alt="readouts" width="400" />
</p>

<h1 align="center">readouts</h1>

<p align="center">
  Verified, source-backed SQLite knowledge bases that an agent reads one slice at a time.
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/readouts/actions/workflows/verify.yml"><img src="https://github.com/mcp-tool-shop-org/readouts/actions/workflows/verify.yml/badge.svg" alt="verify" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License" /></a>
  <a href="https://mcp-tool-shop-org.github.io/readouts/"><img src="https://img.shields.io/badge/Landing_Page-live-34d399" alt="Landing Page" /></a>
</p>

---

readouts is a set of knowledge bases about the tools behind a small game studio: Rust, Godot, Blender, sprite and animation craft, local AI models and the engines that run and train them, the sung voice, GPU containers and the XRP Ledger.

Each knowledge base (KB) is one SQLite database with a full-text index. Every entry names its sources, records the research wave that produced it, and carries a `verified` flag. Only a verdict from a separate verifier can set that flag; the author's own opinion of its work never counts.

The name comes from [loadout-os](https://github.com/mcp-tool-shop-org/loadout-os), which *loads* the right knowledge for a task. readouts is what it reads from.

## The knowledge bases

| KB | What | Status |
|----|------|--------|
| [blender-knowledge](blender-knowledge/) | current, web-grounded Blender 4.x practice for the studio's headless sprite-turnaround render pipeline (import a TRELLIS-generated GLB → render 8-direction sprites via blender --background --python → composite into a 2.5D game) plus general game-asset prep. | **219 recipes · 10 domains · 8 waves · 83/219 verified** |
| [docker-knowledge](docker-knowledge/) | The knowledge base behind the gpu-container product — how to package, measure, and place models honestly on one GPU. | **160 findings · 6 domains · 9 waves · 73/160 verified** |
| [godot-knowledge](godot-knowledge/) | current, adversarially-verified Godot 4 dev knowledge for building a 2.5D turn-based tactical RPG. | **177 recipes · 6 domains · 7 waves · 50/177 verified** |
| [model-knowledge](model-knowledge/) | Verified knowledge base of the best local generative-AI MODELS per purpose (image / edit / control / video / 3D / audio / LLM / caption) for the RTX 5090 rig — commercial-license-first. | **129 models · 9 domains · 19 waves · 126/129 verified** |
| [rust-knowledge](rust-knowledge/) | Verified Rust for building si-rpg-engine (essentials, advanced, and how the engine uses it: raw wasm ABI, float determinism, Rapier 0.35 state and restore, reproducible bytes) and a first tier for si-jam-sessions' music law, with every code check run by the pinned rustc 1.98.1. | **267 recipes · 27 domains · 4 waves · 266/267 verified** |
| [sprite-motion-knowledge](sprite-motion-knowledge/) | The portable animate-the-sprite craft for this rig | **246 recipes · 19 domains · 8 waves · 170/246 verified** |
| [sprites-knowledge](sprites-knowledge/) | The portable concept-art → game-ready 2.5D JRPG sprite craft for this rig | **215 recipes · 8 domains · 6 waves · 92/215 verified** |
| [tensor-engine-knowledge](tensor-engine-knowledge/) | Verified knowledge base of the ENGINES that run & train AI models locally on the RTX 5090 (Blackwell / sm_120 / Windows) rig. | **193 engines · 10 domains · 17 waves · 134/193 verified** |
| [training-knowledge](training-knowledge/) | Verified knowledge base of portable TRAINING CRAFT — methods, recipes, hyperparameter values, dataset & eval know-how — for training LoRAs / fine-tunes on the single RTX 5090 (Blackwell / Windows / WSL2) rig. The how-to-train layer between the weights (model-knowledge) and the software (tensor-engine-knowledge). | **204 techniques · 13 domains · 16 waves · 101/204 verified** |
| [vocology-knowledge](vocology-knowledge/) | sung-voice craft: vocology (source-filter, registers, singers formant), musical vs speech prosody, lyric-to-note alignment, score-controllable SVS vs lyrics-to-song generators, admission/teaching evaluation | **317 findings · 19 domains · 13 waves · 214/317 verified** |
| [xrpl-knowledge](xrpl-knowledge/) | Verified knowledge base of the XRP Ledger ECOSYSTEM for a builder — protocol features, transaction types, XLS standards, client libraries & tooling — each tagged with its current mainnet / amendment status. Whole-ecosystem: XRPL mainnet + Xahau/Hooks + the XRPL EVM sidechain + the institutional layer (RLUSD, compliance). | **457 capabilities · 12 domains · 10 waves · 362/457 verified** |

The table is generated from [`index.json`](index.json) by `shared/sync_readme_table.py`, and `python verify.py` fails if it drifts. [`index.md`](index.md) is the same map written for agents, and [`index.html`](index.html) renders it.

Each KB folder holds its database, a `catalog/` of generated markdown pages per domain, a `waves/` folder with every wave's research and verification record, and its own `README.md`.

## Quick start

```bash
git clone https://github.com/mcp-tool-shop-org/readouts
cd readouts
python verify.py
```

`verify.py` needs Python 3.10 or newer and nothing outside the standard library. The databases are ordinary SQLite files, so any SQLite client can open them.

Search one KB through its full-text index, then join back to the entry:

```sql
-- sqlite3 rust-knowledge/rust.db
SELECT r.name, r.verified
FROM recipes_fts f
JOIN recipes r ON r.id = f.rowid
WHERE recipes_fts MATCH 'rapier'
LIMIT 5;
```

Add `AND r.verified = 1` to keep only what the verifier confirmed. The same pattern works in every KB. The entity table is named in [`index.md`](index.md): `recipes`, `findings`, `models`, `engines`, `techniques` or `capabilities`, each with a matching `<table>_fts` index. Most KBs also have a `v_recommended` view (docker-knowledge and vocology-knowledge have `v_load_bearing`). These views select by each KB's own recommendation field, not by `verified`.

## How an entry earns `verified`

1. **A wave of research.** One research lane per domain writes entries, and each entry cites its sources as `{url, claim}` pairs.
2. **A separate verifier.** A second agent, which never sees the researcher's reasoning, checks each entry against the pages it cites and returns a verdict. In most waves that verifier comes from the same model family as the researcher; some waves add a seat from a different family. Each wave's record says which.
3. **One definition of `verified`.** `verified = 1` only when that external verdict says so ([`shared/verdicts.py`](shared/verdicts.py)). An entry with no verdict stays unverified. Treat it as a lead, not a fact.
4. **A compiler, where there is code.** Every code check in rust-knowledge is compiled, and where it says so run, by `rustc 1.98.1`. A recipe whose own example fails the compiler is never verified.

Every wave keeps its record in the KB's `waves/` folder: `dispatch.md` (what was asked and what came back), `research-raw.json` (what was loaded) and, where the wave has one, `verification.md` (what the verifier and the compiler found). KBs that keep a durable verdict ledger keep it in `verification/verdicts.json`.

## Route an agent to one slice

Two loadout indexes keep an agent from reading the whole corpus:

1. The root [`.claude/loadout/index.json`](.claude/loadout/index.json) routes a task to the right KB.
2. Each KB's own `.claude/loadout/index.json` routes it to the right domain inside that KB.

```bash
npx @mcptoolshop/loadout-os validate .claude/loadout/index.json
npx @mcptoolshop/loadout-os resolve --project .
```

`resolve` also merges your own global loadout layer if you have one.

## Check the corpus yourself

`python verify.py` is the repository's floor. It checks that the generated files are true about the databases: that every full-text rowid joins to its own entry, that no verified entry lacks a source, that `verified` traces to an external verdict, that the front door and this README's table match the databases, and that no relative link is dead.

- `FAIL` breaks a contract or serves wrong data. It blocks publication.
- `WARN` is a real defect that is known, bounded and recorded.

Every FAIL and WARN carries a stable code and a hint for the next step. `python verify.py --json` prints one JSON object per check. The exit code is 0 when clean, 1 on a FAIL, and 2 if a check itself crashed. CI runs it on every push that changes the corpus.

## Security and threat model

- **What this repository is:** data. It holds SQLite databases, markdown, JSON and the Python scripts that built them. Nothing runs on install, and there is nothing to install.
- **The read path is local.** Querying a database, `verify.py`, and the generators (`regen.py`, `shared/gen_*.py`, each KB's `load_db.py`, `gen_catalog.py` and `gen_loadout.py`) read files in this checkout and write only derived files inside it. They open no network connection, read no credentials and send no telemetry. `verify.py` writes nothing at all.
- **The research tooling is not.** Scripts kept as the record of how the waves were made (for example each `verify_cloud.py`, rust-knowledge's `openrouter_lane.py`, and tensor-engine-knowledge's `verifier/`) call a model: a local Ollama daemon, or OpenRouter with an `OPENROUTER_API_KEY` you set in the environment. Some also fetch the pages they cite. No key is stored in the repository. `compile_oracle.py setup` downloads the pinned Rust crates through cargo, once. None of these runs unless you run it.
- **Permissions:** read access to the checkout; write access only if you regenerate.
- **No telemetry**, anywhere in the repository.
- **What the content is:** research notes with citations. An unverified entry is a lead, not a fact. Licence notes about models, datasets and crates are not legal advice; read the licence itself before you ship anything.

To report a problem, see [SECURITY.md](SECURITY.md).

## Maintain it

[MAINTENANCE.md](MAINTENANCE.md) is the runbook: adding a wave or a KB, running a verification sweep, and the traps that have already cost someone an afternoon. [CONVENTIONS.md](CONVENTIONS.md) describes the shape every KB shares. The [handbook](https://mcp-tool-shop-org.github.io/readouts/handbook/) walks through querying, verification and routing in more depth. Changes are listed in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)

---

Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
