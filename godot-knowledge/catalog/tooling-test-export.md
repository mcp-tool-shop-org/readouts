# Tooling, test, export, CI
_GUT unit testing, debugging/profiling, headless + GitHub-Actions CI, export templates + Windows/Steam, performance for tactical grids, the Godot .gitignore + version control, the LLM-crew data-authoring workflow._ · wave 7 · 2026-09-07 · [‹ catalog index](README.md)

50 recipes · 25 solid.

| Recipe | Godot | Currency | ✓ | What |
|--------|-------|----------|---|------|
| Beyond Test Presence — agent-generated test quality | 4.x | ✅ solid | · | Agent-generated tests can pass with weak coverage/oracles. |
| Canonical Godot 4 .gitignore + .gitattributes (Git LFS) for version control | Godot 4.x — ignore `.godot/` (4.x cache dir; the 3.x `.import/` no longer applies) | ✅ solid | · | A Godot-4-correct `.gitignore` (exclude regenerable caches) plus `.gitattributes |
| Compaction as Epistemic Failure — killed-process false-green | 4.x | ✅ solid | · | Partial stdout from timed-out commands (exit 143) recorded as confirmed success. |
| Cross-project flakiness — OpenStack case study | 4.x | ✅ solid | · | Flakiness erodes trust and wastes CI across ecosystems. |
| Data-driven design with custom Resources (.tres) — the LLM-crew authoring substrate | Godot 4.x (`@export` annotation, `class_name`, ResourceLoader/ResourceSaver) | ✅ solid | · | Define game data as custom `Resource` subclasses serialized to `.tres` (human-re |
| Dataset of reproducible flaky-test failures | 4.x | ✅ solid | · | Reproducing flaky failures hard due to nondeterminism; releases reproducible dat |
| Debugger toolkit: remote scene tree, breakpoints, and headless debug flags | Godot 4.x Debugger panel + CLI (`--headless --debug --verbose --quit-after`) | ✅ solid | · | Godot 4's Debugger panel gives a live Remote Scene Tree (inspect/edit running no |
| Environmental flakiness in JavaScript tests | 4.x | ✅ solid | · | Environmental configuration changes induce flakiness. |
| GUT 9.6.0 release — headless auto-exit | 4.x | ✅ solid | · | Headless ignores pause_before_teardown and exits when finished. |
| GUT Export Test Results — JUnit XML | 4.x | ✅ solid | · | -gjunit_xml_file / -gjunit_xml_timestamp for CI parsers. |
| GUT README — version matrix GUT 9.x ↔ Godot 4.x | 4.x | ✅ solid | · | GUT 9.x maps to Godot 4.x lines; GUT 7.x ↔ Godot 3.x. |
| GUT docs index — GUT 9 requires Godot 4 | 4.x | ✅ solid | · | Asset Library shows GUT 9 (Godot 4) and GUT 7 (Godot 3.4+). |
| Godot #83449 — headless exit-code bugs | 4.x | ✅ solid | · | Engine can exit 0 on error paths in headless scenarios. |
| Godot #85062 — headless import exit traps | 4.x | ✅ solid | · | Import/headless exit-code traps for CI sequencing. |
| Godot PR #90431 — --import CLI | 4.x | ✅ solid | · | Documented --import switch for honest CI warm-up. |
| Godot PR #99254 — --fail-on-error | 4.x | ✅ solid | · | Documented fail switch for CI honesty. |
| Headless command-line export for Windows + steamcmd upload pipeline | Godot 4.5.x/4.6.x (`--export-release`/`--export-debug`, `--headless`) | ✅ solid | · | Drive Godot exports from the CLI (no editor GUI) reading `export_presets.cfg`, t |
| Illusion of Success — silent CI failures | 4.x | ✅ solid | · | Silent failures: jobs marked success/exit 0 while tasks incomplete; ignored exit |
| Install GUT 9.x as the unit-test framework and structure tests as data-checkable specs | GUT 9.x for Godot 4.x (9.5.0 docs target 4.5; works on 4.6) | ✅ solid | · | GUT (Godot Unit Test) is the GDScript-native unit-testing framework. The 9.x lin |
| Jest CLI — documented empty-suite exit policy | 4.x | ✅ solid | · | --passWithNoTests is an explicit documented flag. |
| Limits of code-based flaky-test detection | 4.x | ✅ solid | · | Flaky tests pass/fail on same code; flakiness not static property of test code a |
| POSIX shell exit contract (Issue 7 utilities) | 4.x | ✅ solid | · | Pipelines fail on non-zero unless explicitly ignored. |
| Profile with the built-in Profiler + custom performance monitors before optimizing | Godot 4.x built-in Profiler + custom monitors (custom monitors since 4.0; Visual Profiler folding 4.7-dev) | ✅ solid | · | Godot 4 ships a built-in GDScript Profiler and a Monitors tab in the Debugger pa |
| Target Godot 4.5.x as production baseline; track 4.6 as the upgrade lane | 4.5.2 (support ended 2026-03) or 4.6.3 (active) — recommend 4.6.3 for a fresh 2026 start | ✅ solid | · | Pick one pinned 4.x stable to build against, with a deliberate policy for when t |
| TileMapLayer (not TileMap) for the tactical grid, with deliberate overlay-layer budgeting | Godot 4.3+ for TileMapLayer (4.6 has further 2D/tilemap improvements); REQUIRED on 4.4+ | ✅ solid | · | Build the combat grid on `TileMapLayer` nodes — the current API. `TileMap` was D |
| A Standardized Machine-readable Dataset Documentation Format for Responsible AI | 4.x | ⚠ shaky | · | Croissant-RAI machine-readable RAI metadata extension — structured docs so disco |
| Command line tutorial | 4.x | ⚠ shaky | · | Official `--headless` (“display-driver headless + Dummy audio”); `--import` star |
| Croissant Baker: Metadata Generation for Discoverable, Governable, and Reusable ML Datasets | 4.x | ⚠ shaky | · | Automates Croissant metadata so discovery/ingestion is machine-checkable — favor |
| Cross-check note | 4.x | ⚠ shaky | · | **do not flip**. |
| Datasheets Aren't Enough: DataRubrics for Automated Quality Metrics and Accountability | 4.x | ⚠ shaky | · | Datasheets alone miss quality/accountability; DataRubrics add automated checks — |
| FAIR principles for AI models with a practical application for accelerated high energy diffraction microscopy | 4.x | ⚠ shaky | · | Extends FAIR to AI models with measurable stewardship — catalog 155 · 88/155 hon |
| GPUAlert: A Zero-Instrumentation Process-Boundary Monitor for Diagnosing GPU Training-Job Failures | 4.x | ⚠ shaky | · | Notifier isolation: wrapper exit code is a pure function of the child status acr |
| GUT Command Line (official pair for 49) | 4.x | ⚠ shaky | · | Official GUT CLI documents -gexit and -gexit_on_success only — no -gexit_on_comp |
| GUT README | 4.x | ⚠ shaky | · | GUT 9.7.1 targets Godot **4.7.x**; main branch 4.6.x. Blog sample pins **4.2.2** |
| Gradle #8739 System.exit false-green | 4.x | ⚠ shaky | · | Analog: wrong exit path → BUILD SUCCESSFUL while tests never finished. Holds for |
| Open Datasheets: Machine-readable Documentation for Open Datasets and Responsible AI Assessments | 4.x | ⚠ shaky | · | No-code machine-readable open-dataset documentation for RAI assessments — suppor |
| Pytest exit codes | 4.x | ⚠ shaky | · | Analog: named public exit-code contract. Holds: recipe 49 CI must consume docume |
| Regulatory compliance-readiness in the AI Supply Chain: examining datasets in Hugging Face | 4.x | ⚠ shaky | · | Audits HF datasets for regulatory readiness gaps — claim vs documented readiness |
| Run GUT headlessly in GitHub Actions with cache + import warm-up (the green-CI pattern) | Godot 4.5.x/4.6.x headless; GUT 9.x; actions/checkout@v4, actions/cache@v4 | ⚠ shaky | · | A reliable GitHub Actions workflow that installs a pinned Godot binary, warms th |
| SetGo: Metadata Readiness for Scientific AI Datasets | 4.x | ⚠ shaky | · | Separates computational readiness from metadata readiness — README status must m |
| The Importance of Discerning Flaky from Fault-triggering Test Failures: A Case Study on the Chromium CI | 4.x | ⚠ shaky | · | Flaky tests pass/fail on same version and create false alerts; CI must separate  |
| Understanding and Detecting Flaky Builds in GitHub Actions | 4.x | ⚠ shaky | · | Large-scale GHA study: reruns; 67.73% of rerun builds flaky (outcome changes wit |
| Workflow Cards: Structured Summaries of Workflow Executions Using Provenance Data | 4.x | ⚠ shaky | · | Extends Model/Data Cards to workflow provenance for executions — wave/load recei |
| helpmetest Godot CI blog (id 49 URL) | 4.x | ⚠ shaky | · | **On page:** `--headless`, binary+import cache, `gut_cmdln.gd`, workflow sample, |
| GUT CLI -gexit / -gexit_on_success (4.7.x) | 4.7.x |  | · | CLI documents -gexit / -gexit_on_success only (no -gexit_on_complete); GUT 9.7.1 |
| GameCraft-Bench — Godot 4 end-to-end agent bench | 4.x |  | · | Instantiates end-to-end game gen in Godot 4 (text scenes, native 2D, headless CL |
| GameDevBench — Godot 4 tutorial agent tasks | 4.x |  | · | 333 Godot 4 tutorial tasks; agents ~51% on gameplay vs ~33% on 2D graphics/anima |
| Gradle #8739 System.exit false-green analog | 4.x |  | · | Analog: wrong exit path yields BUILD SUCCESSFUL while tests never ran. Holds for |
| JAMER — Godot 4.x headless jam verify | 4.x |  | · | Godot 4.x headless L1–L3 pipeline verifies 8,133 jam projects; text.tscn/.gd + h |
| Pytest exit codes — named exit contract analog | 4.x |  | · | Analog: named exit-code contract is public API. Holds: CI must use documented fl |

## Detail

### Beyond Test Presence — agent-generated test quality · `✅ solid` · Godot 4.x
**Agent-generated tests can pass with weak coverage/oracles.**
- **How:** Pass-rate ≠ verification quality for crew GUT specs.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Beyond Test Presence — agent-generated test quality](https://arxiv.org/abs/2607.12068) — Pass-rate ≠ verification quality

### Canonical Godot 4 .gitignore + .gitattributes (Git LFS) for version control · `✅ solid` · Godot Godot 4.x — ignore `.godot/` (4.x cache dir; the 3.x `.import/` no longer applies)
**A Godot-4-correct `.gitignore` (exclude regenerable caches) plus `.gitattributes` (force LF endings, route binary assets to Git LFS). Gets the studio's git hygiene right from commit one so the crew + CI never fight cache churn or line-ending diffs.**
- **How:** gitignore essentials for Godot 4: ignore `.godot/` (the 4.x import/cache dir — NOT the old 3.x `.import/`), `export.cfg`, `export_presets.cfg` is KEPT (commit it), plus `*.translation`, build/export output dirs, and OS cruft (`.DS_Store`, `Thumbs.db`)..gitattributes: set `* text=auto eol=lf` to normalize line endings (critical cross-platform — the studio runs Windows now, Mac M5 later), and route large binaries through Git LFS: `*.png filter=lfs diff=lfs merge=lfs -text` and likewise for `*.ogg *.wav *.mp3 *.glb *.ttf *.psd`. Commit the `.tres`/`.gd`/`.tscn` as normal text (diffable). Use the maintained karbassi Godot-4.3 gist as the starting template.
- **Gotchas:** STALE: Godot-3 `.gitignore` templates ignore `.import/` — on Godot 4 the cache dir is `.godot/`. Ignoring the wrong one means either committing the cache (bloat) or breaking CI's expected cache path. Set up LFS BEFORE committing large binaries — retroactively moving files into LFS requires history rewriting. Do NOT gitignore `.tres`/`.tscn` (they're source). Keep `.godot/` ignored but expect CI to regenerate it via the import warm-up step (see CI recipe). The official Godot docs 'Version control systems' page documents the recommended ignore set.
- **Verify (solid):** Official version-control docs confirm: ignore.godot/ (4.x cache dir, NOT the 3.x/4.0.import/), ignore *.translation, and the.gitattributes LFS routing for png/ogg/wav/glb/ttf etc. export_presets.cfg is safe to commit on 4.1+ (3.x/4.0 could store credentials there) — recipe's 'commit it' guidance is correct for 4.x. LF normalization + set-up-LFS-before-committing all sound. Stale.import/ warning correct. [no external verdict — not checked]
- **Sources:** [Version control systems — Godot Engine (stable) docs](https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html) ; [Godot 4.3 .gitignore + Git LFS gist — karbassi](https://gist.github.com/karbassi/ce1f3cb68b3c6fc3c471cf992aed0053) ; [Godot 4 — Adding Git/GitLFS to your existing Project — Matt Barrett](https://mbarrett.dev/godot-4-adding-git-gitlfs-to-your-existing-project/)

### Compaction as Epistemic Failure — killed-process false-green · `✅ solid` · Godot 4.x
**Partial stdout from timed-out commands (exit 143) recorded as confirmed success.**
- **How:** Treat non-zero/killed exits as untrusted, not green.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Compaction as Epistemic Failure — killed-process false-green](https://arxiv.org/abs/2607.13071) — Killed-process false-green

### Cross-project flakiness — OpenStack case study · `✅ solid` · Godot 4.x
**Flakiness erodes trust and wastes CI across ecosystems.**
- **How:** Multi-project CI reliability frame for Godot/GUT.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Cross-project flakiness — OpenStack case study](https://arxiv.org/abs/2602.09311) — Cross-project flakiness

### Data-driven design with custom Resources (.tres) — the LLM-crew authoring substrate · `✅ solid` · Godot Godot 4.x (`@export` annotation, `class_name`, ResourceLoader/ResourceSaver)
**Define game data as custom `Resource` subclasses serialized to `.tres` (human-readable text) files. This is the core pattern that makes content crew-authorable: units, loot parts, abilities, enemies, and combat rules become plain-text Resources the LLM crew can generate and a human can diff-review.**
- **How:** Write a script `extends Resource` with `class_name AbilityData` and typed `@export` vars (`@export var ap_cost: int`, `@export var loot_tier: int`, `@export var collateral: int`). In the FileSystem panel right-click > New Resource > pick your class > save as `.tres`. Load with `load("res://data/abilities/disable_arm.tres")` or `ResourceLoader.load(path)`; for runtime-flexible loading use `ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_REPLACE)`. `.tres` is the dev/authoring format (text, diffable, version-controllable); convert to `.res` (binary, faster load, smaller) for release if load time matters. Type the `@export` so the inspector validates and the crew gets a schema to target. Nest Resources (an `EnemyData` holding an array of `AbilityData`) to compose content.
- **Gotchas:** Do NOT use Resources for PLAYER SAVE DATA — serialize saves to plain JSON containing only the values you need. Reason: loading a `.tres`/`.res` can instantiate arbitrary embedded scripts (a security + forward-compat hazard for save files), and Resource saves are brittle across class changes. JSON caveat: JSON has only float numbers (no int) and no native Vector2/Color — convert types manually on save/load. Godot-3 used the bare `export` keyword; on 4.x it's the `@export` annotation — generated code using `export var` is stale.
- **Verify (solid):** extends Resource + class_name + typed @export, New Resource flow, load()/ResourceLoader.load() with CACHE_MODE_REPLACE,.tres(text)-vs-.res(binary), nesting — all current 4.x. The save-data gotcha is fully verified: Resources can embed arbitrary scripts (code-execution hazard on untrusted load), JSON is the safe save format, and the JSON-has-only-floats / no-native-Vector2-Color caveat is correct. @export (not Godot-3 bare export) correct. [no external verdict — not checked]
- **Sources:** [Custom Resources in Godot Engine 4.x — Simon Dalvai](https://simondalvai.org/blog/godot-custom-resources/) ; [Saving and Loading Games in Godot 4 (with resources) — GDQuest](https://www.gdquest.com/library/save_game_godot4/) ; [Custom Resources are OP in Godot 4 — Ezcha](https://ezcha.net/news/3-1-23-custom-resources-are-op-in-godot-4)

### Dataset of reproducible flaky-test failures · `✅ solid` · Godot 4.x
**Reproducing flaky failures hard due to nondeterminism; releases reproducible dataset.**
- **How:** Measurement substrate for flaky CI craft.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Dataset of reproducible flaky-test failures](https://arxiv.org/abs/2605.21677) — Reproducible flaky-failure dataset

### Debugger toolkit: remote scene tree, breakpoints, and headless debug flags · `✅ solid` · Godot Godot 4.x Debugger panel + CLI (`--headless --debug --verbose --quit-after`)
**Godot 4's Debugger panel gives a live Remote Scene Tree (inspect/edit running nodes), breakpoints + the Stack Trace / Stack Variables view, the Errors/Warnings monitor, and Network/Video monitors. Plus the CLI debug flags for reproducing CI failures locally. This is the day-to-day inspection loop for combat bugs.**
- **How:** Run the game from the editor (F5); the Debugger panel auto-attaches. Use the 'Remote' tab in the Scene dock to inspect the LIVE tree and tweak node properties at runtime (e.g. watch a unit's AP/HP change mid-fight). Set breakpoints by clicking the gutter or `breakpoint` keyword / `assert(cond)` in GDScript; when hit, read Stack Trace + Stack Variables. The Errors tab surfaces runtime errors/warnings with stack context. For headless/CI-style repro from a terminal: `godot --headless --debug --verbose --path. <scene_or_main>` to see verbose logs; `-d` enables the debugger, `--verbose` (`-v`) prints detailed engine output, `--quit-after N` exits after N frames for scripted runs. To debug an export, do a debug export and run with `--verbose` to capture the same logs a CI runner would.
- **Gotchas:** STALE: Godot-3 used `--no-window` for windowless runs; on 4.x use `--headless`. `assert()` is stripped in release/optimized builds — rely on it for dev invariant-checking, not as runtime production validation. The Remote tree edits affect the running instance only (not saved). Verbose logging is noisy — use it to diagnose, not as a standing setting. For native/engine-level crashes the GDScript debugger won't help; that's the separate C++ profiler/debugger path.
- **Verify (solid):** Remote Scene Tree, breakpoints/Stack Trace/Stack Variables, Errors/Warnings + Network/Video monitors all current 4.x. CLI flags --headless --debug(-d) --verbose(-v) --quit-after N confirmed; --no-window→--headless migration correct. assert() stripped in release builds is accurate. Native-crash-needs-C++-debugger caveat correct. [no external verdict — not checked]
- **Sources:** [Debugger panel — Godot Engine (stable) docs (overview of debug tools)](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html) ; [Debugging and profiling — Godot Engine (4.4) docs](https://docs.godotengine.org/en/4.4/contributing/development/debugging/index.html) ; [Command line tutorial — Godot Engine (stable) docs (CLI flags)](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)

### Environmental flakiness in JavaScript tests · `✅ solid` · Godot 4.x
**Environmental configuration changes induce flakiness.**
- **How:** Same class as Godot headless import-cache flakiness.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Environmental flakiness in JavaScript tests](https://arxiv.org/abs/2602.19098) — Environmental flakiness

### GUT 9.6.0 release — headless auto-exit · `✅ solid` · Godot 4.x
**Headless ignores pause_before_teardown and exits when finished.**
- **How:** CI-friendly DisplayServer headless default.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [GUT 9.6.0 release — headless auto-exit](https://github.com/bitwes/Gut/releases) — Headless auto-exit

### GUT Export Test Results — JUnit XML · `✅ solid` · Godot 4.x
**-gjunit_xml_file / -gjunit_xml_timestamp for CI parsers.**
- **How:** Documented artifact path.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [GUT Export Test Results — JUnit XML](https://gut.readthedocs.io/en/latest/Export-Test-Results.html) — JUnit XML export

### GUT README — version matrix GUT 9.x ↔ Godot 4.x · `✅ solid` · Godot 4.x
**GUT 9.x maps to Godot 4.x lines; GUT 7.x ↔ Godot 3.x.**
- **How:** Pin GUT tag to engine line.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [GUT README — version matrix GUT 9.x ↔ Godot 4.x](https://github.com/bitwes/Gut/blob/main/README.md) — Version matrix

### GUT docs index — GUT 9 requires Godot 4 · `✅ solid` · Godot 4.x
**Asset Library shows GUT 9 (Godot 4) and GUT 7 (Godot 3.4+).**
- **How:** Match editor version.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [GUT docs index — GUT 9 requires Godot 4](https://gut.readthedocs.io/en/latest/) — GUT 9 / Godot 4

### Godot #83449 — headless exit-code bugs · `✅ solid` · Godot 4.x
**Engine can exit 0 on error paths in headless scenarios.**
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Godot #83449 — headless exit-code bugs](https://github.com/godotengine/godot/issues/83449) — Headless exit 0 on error

### Godot #85062 — headless import exit traps · `✅ solid` · Godot 4.x
**Import/headless exit-code traps for CI sequencing.**
- **How:** Recipe 49 import+GUT sequencing caution; stay ·.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Godot #85062 — headless import exit traps](https://github.com/godotengine/godot/issues/85062) — Import exit traps

### Godot PR #90431 — --import CLI · `✅ solid` · Godot 4.x
**Documented --import switch for honest CI warm-up.**
- **How:** Warm-up without fake quit hacks.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Godot PR #90431 — --import CLI](https://github.com/godotengine/godot/pull/90431) — --import merged

### Godot PR #99254 — --fail-on-error · `✅ solid` · Godot 4.x
**Documented fail switch for CI honesty.**
- **How:** Honest CI needs documented fail switches.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Godot PR #99254 — --fail-on-error](https://github.com/godotengine/godot/pull/99254) — --fail-on-error

### Headless command-line export for Windows + steamcmd upload pipeline · `✅ solid` · Godot Godot 4.5.x/4.6.x (`--export-release`/`--export-debug`, `--headless`)
**Drive Godot exports from the CLI (no editor GUI) reading `export_presets.cfg`, then push the Windows build to Steam via steamcmd. This is the release path for a Steam-wishlist-building tactical RPG.**
- **How:** Create export presets ONCE in-editor (Project > Export > add 'Windows Desktop'); this writes `export_presets.cfg` (commit it). Export headlessly with: `godot --headless --export-release "Windows Desktop" build/game.exe` (use `--export-debug` for debug builds; `--export-pack` for just the.pck). Note: as of current 4.x you export ONE preset per invocation (a PR to export all presets in one command exists but isn't the stable default) — script a loop over presets. For Steam: install steamcmd, write an app-build VDF script, then `steamcmd +login <user> <pass> +run_app_build_http <path-to-app-build.vdf> +quit`. This uploads to a Steam build but does NOT auto-publish to the public/default branch (Steam blocks automatic public release) — a human sets the live build in the partner backend. Off-the-shelf CI option: `firebelley/godot-export` (GitHub Marketplace 'Godot Export') reads `export_presets.cfg` and produces artifacts.
- **Gotchas:** Export FAILS without the matching export templates installed (and they must match the editor version exactly). On bare CI/Linux runners you need the Linux headless Godot to perform a Windows export. If using GodotSteam via the MODULE build you must point Custom Templates > Release/Debug at the GodotSteam-enabled templates; if using the GodotSteam GDEXTENSION, use NORMAL Godot templates (mixing them up breaks the Steam API binding). Don't commit the built `.exe`/`.pck` or the Steam content depot to git — those are build artifacts. Godot-3 used `--export` (no `-release`/`-debug` suffix split the same way); on 4.x use the explicit `--export-release`/`--export-debug`.
- **Verify (solid):** --export-release/--export-debug/--export-pack/--headless all confirmed in current 4.x CLI docs (--export-debug/--export-pack imply --import). One-preset-per-invocation accurate. --no-window→--headless migration correct. GodotSteam module-vs-GDExtension template rule and steamcmd run_app_build_http + no-auto-publish-to-default-branch are accurate; templates-must-match-editor-version is the real top export failure. [no external verdict — not checked]
- **Sources:** [Automatic Godot game export and upload to Steam and Itch — MrEliptik](http://mreliptik.dev/godot-auto-export/) ; [Exporting and Shipping — GodotSteam (templates vs GDExtension)](https://godotsteam.com/tutorials/exporting_shipping/) ; [Godot (Steamworks Documentation)](https://partner.steamgames.com/doc/steamframe/engines/godot)

### Illusion of Success — silent CI failures · `✅ solid` · Godot 4.x
**Silent failures: jobs marked success/exit 0 while tasks incomplete; ignored exit codes.**
- **How:** False-green pole for GUT CI; keep recipe 49 ·.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Illusion of Success — silent CI failures](https://arxiv.org/abs/2509.14347) — Silent CI failures / ignored exits

### Install GUT 9.x as the unit-test framework and structure tests as data-checkable specs · `✅ solid` · Godot GUT 9.x for Godot 4.x (9.5.0 docs target 4.5; works on 4.6)
**GUT (Godot Unit Test) is the GDScript-native unit-testing framework. The 9.x line is the Godot-4 line (current docs 9.5.0/9.6.0; GUT 9.x = Godot 4.x, GUT 7.x = Godot 3.x). It provides asserts, doubling (full + partial), stubbing, spies, scene/inner-class tests, and a CLI — everything needed to verify deterministic combat math without a human in the loop.**
- **How:** Install via the Godot Asset Library (search 'GUT', asset 1709/9.x) OR drop the `addons/gut/` directory into the project, then Project > Project Settings > Plugins > enable 'GUT', and relaunch. Write tests as scripts that `extends GutTest`, name files `test_*.gd`, methods `test_*()`. Core asserts: `assert_eq(actual, expected)`, `assert_almost_eq`, `assert_true/false`, `assert_null`, `assert_has`, `assert_signal_emitted(obj, 'signal')`. Doubling: `var dbl = double(MyClass).new()` then `stub(dbl, 'method').to_return(value)`; spy with `assert_called(dbl, 'method')`. Run in-editor via the GUT bottom panel, or headless via CLI (see CI recipe). GUT returns exit code 0 = all pass, 1 = any fail.
- **Gotchas:** GUT 9 changed CLI flag handling vs GUT 7 — old `-gtest`/`-s` invocation patterns from Godot-3 tutorials may throw 'Unrecognized options'. Use the documented 9.x flags. Don't confuse GUT (this) with GdUnit4 (a separate, also-valid Godot-4 framework with an embedded inspector + C# support) — pick ONE; GUT is the lighter GDScript-first choice and the better fit for a GDScript/.tres crew workflow. The `godot_4` branch / 9.x is correct; the master/default branch history references Godot 3.
- **Verify (solid):** Verified on bitwes/Gut: 9.x=Godot 4.x, 7.x=Godot 3.x, MIT license, asset ID 1709 (current 9.6.0 on main, 2026-02-24). extends GutTest, test_*/test_*(), the listed asserts, and double()/stub()/spy all current 4.x API. GdUnit4 correctly named as a separate valid Godot-4 framework (MIT, C#-capable). godot_4 branch / master-references-3 caveat accurate. [no external verdict — not checked]
- **Sources:** [GUT — bitwes/Gut (GitHub, Godot 4 on godot_4 branch)](https://github.com/bitwes/Gut) ; [GUT Wiki — Godot 4 Home](https://bitwes.github.io/GutWiki/Godot4/Home.html) ; [GUT Command Line — v9.5.0 (Godot 4.5)](https://gut.readthedocs.io/en/v9.5.0/Command-Line.html)

### Jest CLI — documented empty-suite exit policy · `✅ solid` · Godot 4.x
**--passWithNoTests is an explicit documented flag.**
- **How:** Only documented switches change CI pass/fail semantics.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Jest CLI — documented empty-suite exit policy](https://jestjs.io/docs/cli) — Documented empty-suite flag

### Limits of code-based flaky-test detection · `✅ solid` · Godot 4.x
**Flaky tests pass/fail on same code; flakiness not static property of test code alone.**
- **How:** Limits detectors for GUT nondeterminism.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [Limits of code-based flaky-test detection](https://arxiv.org/abs/2607.09345) — Flaky detection limits

### POSIX shell exit contract (Issue 7 utilities) · `✅ solid` · Godot 4.x
**Pipelines fail on non-zero unless explicitly ignored.**
- **How:** Require real non-zero from GUT in Actions.
- **Gotchas:** Recipe 49 stays verified=0.
- **Verify (solid):** STUDY-025 Verifier ✅ [no external verdict — not checked]
- **Sources:** [POSIX shell exit contract (Issue 7 utilities)](https://pubs.opengroup.org/onlinepubs/9699919799/) — POSIX exit / set -e class

### Profile with the built-in Profiler + custom performance monitors before optimizing · `✅ solid` · Godot Godot 4.x built-in Profiler + custom monitors (custom monitors since 4.0; Visual Profiler folding 4.7-dev)
**Godot 4 ships a built-in GDScript Profiler and a Monitors tab in the Debugger panel, plus the ability to declare CUSTOM performance monitors (new in 4.0). Measure first — this is how you find a slow turn-resolution or pathfinding hotspot instead of guessing.**
- **How:** Open the Debugger bottom panel > Profiler sub-tab > press Start, then run the scene; the Profiler splits frame time into Script/Physics/Idle layers and shows per-function self/total time so you can find the costliest GDScript functions. Use the Monitors tab for FPS, draw calls, object/node counts, and memory over time. For game-specific metrics, register custom monitors: connect to `Performance.add_custom_monitor("game/ai_turn_ms", Callable(self, "_get_ai_turn_ms"))` (Godot 4.0+) so your own timings appear alongside engine stats. The newer Visual Profiler (frame-timeline view) gained tree-folding in 4.7-dev, making complex frames readable. For deep C++/native hotspots there's a separate 'Using C++ profilers' path, but the in-editor profiler covers GDScript game logic.
- **Gotchas:** The Profiler must be Started BEFORE you run the scene to capture from frame 0. Profiler overhead skews absolute numbers — compare relative hotspots, not absolutes, and profile release-ish builds for real figures. Don't micro-optimize off editor-only lag (the editor adds its own cost). Godot-3 had a profiler too but lacked custom performance monitors — the `Performance.add_custom_monitor` API is a 4.0+ feature, so it's a safe 'current' pattern.
- **Verify (solid):** Performance.add_custom_monitor(name, Callable) confirmed in current docs (callable must return number >=0; get_custom_monitor to read at runtime); custom monitors are a 4.0+ feature, correctly flagged as a safe 'current' pattern vs Godot 3 which lacked them. Profiler/Monitors tabs accurate. Visual Profiler folding 'in 4.7-dev' is forward-looking but plausible (4.7 is in active dev) and hedged appropriately. [no external verdict — not checked]
- **Sources:** [The Profiler — Godot Engine (stable) docs](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html) ; [Custom performance monitors — Godot Engine (stable) docs](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/custom_performance_monitors.html) ; [How to Profile GDScript Performance in Godot 4 (2026 Guide) — DEV](https://dev.to/ziva/how-to-profile-gdscript-performance-in-godot-4-a-2026-guide-16jn)

### Target Godot 4.5.x as production baseline; track 4.6 as the upgrade lane · `✅ solid` · Godot 4.5.2 (support ended 2026-03) or 4.6.3 (active) — recommend 4.6.3 for a fresh 2026 start
**Pick one pinned 4.x stable to build against, with a deliberate policy for when to jump. As of June 2026 the release landscape is: 4.6 (released 2026-01-26, latest stable, patch 4.6.3 on 2026-05-20, in active support), 4.5 (released 2025-09-15, regular support ended 2026-03-19, final patch 4.5.2), and 3.6 is the only LTS (3.x branch — NOT relevant to this project). There is NO 4.x LTS yet; the 4.x series only becomes LTS when 5.0 ships.**
- **How:** Concrete call: build on 4.5.2 if you want maximum addon/CI ecosystem maturity right now (GUT 9.5.0 docs target 4.5, most CI actions tested there), OR adopt 4.6.3 to ride active support and the newer 2D/TileMapLayer improvements. Recommended for a fresh project starting mid-2026: target 4.6.3 — it is in active support, 4.5 already left regular support, and starting fresh avoids a forced migration later. Pin the EXACT patch version in a repo file (e.g. a `.godot-version` text file or a README badge) and in your CI setup-action `version:` field so every crew member and every CI run uses byte-identical engine. Treat an engine bump as its own dedicated branch + full GUT pass + export smoke-test, never an incidental change. Re-export templates must match the editor version exactly (mismatched templates are a top export failure).
- **Gotchas:** Do NOT target any 3.x version — the entire Godot-3 API is stale for this project (CharacterBody2D not KinematicBody2D, await not yield, Node3D not Spatial, TileMapLayer not TileMap, @export not export). 3.6 being 'LTS' is a trap: it's the 3.x LTS, irrelevant to a 4.x game. Also: editor version and export-template version must match to the patch; a 4.6.1 editor with 4.6.3 templates can fail or silently misbehave.
- **Verify (solid):** Every dated fact verified against endoflife.date: 4.6 released 2026-01-26 (latest stable, 4.6.3 on 2026-05-20, active support), 4.5 released 2025-09-15 with regular support ended 2026-03-19 (final 4.5.2), 3.6 the only LTS, no 4.x LTS until 5.0. Godot-3-isms list (CharacterBody2D/await/Node3D/TileMapLayer/@export) all correct. Note:.godot-version is a repo/CI convention not an engine-read file, but the recipe describes it exactly that way (a pin for crew+CI), so it's accurate. [no external verdict — not checked]
- **Sources:** [Godot / endoflife.date (release/EOL table)](https://endoflife.date/godot) ; [Godot 4.6 Arrives With Major CG-Friendly Updates](https://digitalproduction.com/2026/01/28/godot-4-6-arrives-with-major-cg-friendly-updates/) ; [Godot (game engine) — Wikipedia (version history)](https://en.wikipedia.org/wiki/Godot_(game_engine))

### TileMapLayer (not TileMap) for the tactical grid, with deliberate overlay-layer budgeting · `✅ solid` · Godot Godot 4.3+ for TileMapLayer (4.6 has further 2D/tilemap improvements); REQUIRED on 4.4+
**Build the combat grid on `TileMapLayer` nodes — the current API. `TileMap` was DEPRECATED in Godot 4.3 and replaced by individual `TileMapLayer` nodes (one node per layer). Tactical games stack overlay layers (movement range, attack zone, part-target highlight), and layer count + update strategy is the main perf lever.**
- **How:** Use one `TileMapLayer` node per logical layer: ground, cover, and one each for the dynamic tactical overlays. Read/write cells with the layer's own methods (`set_cell`, `get_cell_source_id`, `get_cell_tile_data`, `local_to_map`/`map_to_local`) — these now live on `TileMapLayer`, not on a parent TileMap with a layer index. For movement/attack highlights, update ONLY the overlay layer's changed cells per unit move (e.g. clear+repaint the highlight layer), not the terrain layers, and avoid full-layer rebuilds every frame. For an existing TileMap scene, the editor auto-converts: select the TileMap, open its bottom panel, click the toolbox icon > 'Extract TileMap layers as individual TileMapLayer nodes'.
- **Gotchas:** STALE: `TileMap` the node and its `set_cell(layer,...)` signature are Godot-3/early-4 — any crew-generated code using `TileMap` or passing a layer index into cell calls is deprecated; use `TileMapLayer`. Perf notes: scene files bloat hugely when hand-painted (KB to MB) which slows LOAD time (not runtime); editor brush lags past ~500x500 tiles but runtime is fine — don't over-optimize a small tactical map. Many stacked layers DO cost: budget the overlay layers, don't spawn one per unit. For very large continuous worlds you'd need chunked loading, but a bounded tactical battle map does not.
- **Verify (solid):** Verified: TileMap deprecated in 4.3, replaced by individual TileMapLayer nodes; cell methods (set_cell/get_cell_source_id/get_cell_tile_data/local_to_map/map_to_local) now live on TileMapLayer with no layer-index arg. The editor 'Extract TileMap layers as individual TileMapLayer nodes' toolbox flow is described exactly as the docs/migration guides state. Stale-warning about TileMap.set_cell(layer,...) is correct. [no external verdict — not checked]
- **Sources:** [Godot TileMap Replaced with TileMapLayers — GameFromScratch](https://gamefromscratch.com/godot-tilemap-replaced-with-tilelayers/) ; [Godot Tilemap in 2026: TileMapLayer Migration Guide — Ziva](https://ziva.sh/blogs/godot-tilemap) ; [Using TileMaps — Godot Engine (stable) docs](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html)

### A Standardized Machine-readable Dataset Documentation Format for Responsible AI · `⚠ shaky` · Godot 4.x
**Croissant-RAI machine-readable RAI metadata extension — structured docs so discoverable counts track declared provenance, not invented Godot APIs.**
- **How:** Catalog/README count honesty deepen; no flip 37/42/49; no invent APIs.
- **Gotchas:** STUDY-065. Flips 37/42/49: 0. APIs invented: 0.
- **Verify (shaky):** STUDY-065; flips 37/42/49: 0; APIs invented: 0; default unverified [no external verdict — not checked]
- **Sources:** [A Standardized Machine-readable Dataset Documentation Format for Responsible AI](https://arxiv.org/abs/2407.16883) — Croissant-RAI machine-readable RAI metadata extension — structured docs so discoverable counts track declared provenance, not invented Godot APIs.

### Command line tutorial · `⚠ shaky` · Godot 4.x
**Official `--headless` (“display-driver headless + Dummy audio”); `--import` starts editor, waits for import, quits; `-s`/`--script` for scripts. Supports headless CI substrate; does not endorse blog’s `-gexit_on_complete`.**
- **How:** URL-open / official support deepen; 37/42/49 verified=0 stays.
- **Gotchas:** STUDY-044 deepen note. Do not flip 37/42/49. Do not invent -gexit_on_complete as official.
- **Verify (shaky):** STUDY-044 deepen; flips 37/42/49: 0; default unverified [no external verdict — not checked]
- **Sources:** [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html) — Official `--headless` (“display-driver headless + Dummy audio”); `--import` starts editor, waits for import, quits; `-s`/`--script` for scripts. Supports headless CI substrate; does not endorse blog’s

### Croissant Baker: Metadata Generation for Discoverable, Governable, and Reusable ML Datasets · `⚠ shaky` · Godot 4.x
**Automates Croissant metadata so discovery/ingestion is machine-checkable — favors generated catalog from DB over hand-edited verified counts.**
- **How:** Catalog/README count honesty deepen; no flip 37/42/49; no invent APIs.
- **Gotchas:** STUDY-065. Flips 37/42/49: 0. APIs invented: 0.
- **Verify (shaky):** STUDY-065; flips 37/42/49: 0; APIs invented: 0; default unverified [no external verdict — not checked]
- **Sources:** [Croissant Baker: Metadata Generation for Discoverable, Governable, and Reusable ML Datasets](https://arxiv.org/abs/2605.15079) — Automates Croissant metadata so discovery/ingestion is machine-checkable — favors generated catalog from DB over hand-edited verified counts.

### Cross-check note · `⚠ shaky` · Godot 4.x
****do not flip**.**
- **How:** URL-open / official support deepen; 37/42/49 verified=0 stays.
- **Gotchas:** STUDY-044 deepen note. Do not flip 37/42/49. Do not invent -gexit_on_complete as official.
- **Verify (shaky):** STUDY-044 deepen; flips 37/42/49: 0; default unverified [no external verdict — not checked]

### Datasheets Aren't Enough: DataRubrics for Automated Quality Metrics and Accountability · `⚠ shaky` · Godot 4.x
**Datasheets alone miss quality/accountability; DataRubrics add automated checks — count honesty needs measurable gates; 37/42/49 stay verified=0.**
- **How:** Catalog/README count honesty deepen; no flip 37/42/49; no invent APIs.
- **Gotchas:** STUDY-065. Flips 37/42/49: 0. APIs invented: 0.
- **Verify (shaky):** STUDY-065; flips 37/42/49: 0; APIs invented: 0; default unverified [no external verdict — not checked]
- **Sources:** [Datasheets Aren't Enough: DataRubrics for Automated Quality Metrics and Accountability](https://arxiv.org/abs/2506.01789) — Datasheets alone miss quality/accountability; DataRubrics add automated checks — count honesty needs measurable gates; 37/42/49 stay verified=0.

### FAIR principles for AI models with a practical application for accelerated high energy diffraction microscopy · `⚠ shaky` · Godot 4.x
**Extends FAIR to AI models with measurable stewardship — catalog 155 · 88/155 honesty as findable verified vs unreused unverified rows.**
- **How:** Catalog/README count honesty deepen; no flip 37/42/49; no invent APIs.
- **Gotchas:** STUDY-065. Flips 37/42/49: 0. APIs invented: 0.
- **Verify (shaky):** STUDY-065; flips 37/42/49: 0; APIs invented: 0; default unverified [no external verdict — not checked]
- **Sources:** [FAIR principles for AI models with a practical application for accelerated high energy diffraction microscopy](https://arxiv.org/abs/2207.00611) — Extends FAIR to AI models with measurable stewardship — catalog 155 · 88/155 honesty as findable verified vs unreused unverified rows.

### GPUAlert: A Zero-Instrumentation Process-Boundary Monitor for Diagnosing GPU Training-Job Failures · `⚠ shaky` · Godot 4.x
**Notifier isolation: wrapper exit code is a pure function of the child status across failure modes — exit-contract craft against silent/wrong greens for recipe 49 (no flip).**
- **How:** Literature deepen for leftover 37/42/49; no verified flip.
- **Gotchas:** STUDY-044 deepen note. Do not flip 37/42/49. Do not invent -gexit_on_complete as official.
- **Verify (shaky):** STUDY-044 deepen; flips 37/42/49: 0; default unverified [no external verdict — not checked]
- **Sources:** [GPUAlert: A Zero-Instrumentation Process-Boundary Monitor for Diagnosing GPU Tra](https://arxiv.org/abs/2607.01409) — Notifier isolation: wrapper exit code is a pure function of the child status across failure modes — exit-contract craft against silent/wrong greens for recipe 49 (no flip).

### GUT Command Line (official pair for 49) · `⚠ shaky` · Godot 4.x
**Official GUT CLI documents -gexit and -gexit_on_success only — no -gexit_on_complete. Do not invent that flag. Documents **`-gexit`** and **`-gexit_on_success` only**. **No `-gexit_on_complete`.** Returns 0 on pass / 1 on fail. **Hard mismatch with blog (4):** invented/wrong exit flag → false-green risk. verified=0 stays for 49.**
- **How:** URL-open / official support deepen; 37/42/49 verified=0 stays.
- **Gotchas:** STUDY-044 deepen note. Do not flip 37/42/49. Do not invent -gexit_on_complete as official.
- **Verify (shaky):** STUDY-044 deepen; flips 37/42/49: 0; default unverified [no external verdict — not checked]
- **Sources:** [GUT Command Line (official pair for 49)](https://gut.readthedocs.io/en/latest/Command-Line.html) — Official GUT CLI documents -gexit and -gexit_on_success only — no -gexit_on_complete. Do not invent that flag. Documents **`-gexit`** and **`-gexit_on_success` only**. **No `-gexit_on_complete`.** Ret

### GUT README · `⚠ shaky` · Godot 4.x
**GUT 9.7.1 targets Godot **4.7.x**; main branch 4.6.x. Blog sample pins **4.2.2** — version skew vs current 4.7 docs.**
- **How:** URL-open / official support deepen; 37/42/49 verified=0 stays.
- **Gotchas:** STUDY-044 deepen note. Do not flip 37/42/49. Do not invent -gexit_on_complete as official.
- **Verify (shaky):** STUDY-044 deepen; flips 37/42/49: 0; default unverified [no external verdict — not checked]
- **Sources:** [GUT README](https://raw.githubusercontent.com/bitwes/Gut/main/README.md) — GUT 9.7.1 targets Godot **4.7.x**; main branch 4.6.x. Blog sample pins **4.2.2** — version skew vs current 4.7 docs.

### Gradle #8739 System.exit false-green · `⚠ shaky` · Godot 4.x
**Analog: wrong exit path → BUILD SUCCESSFUL while tests never finished. Holds for recipe 49 (missing `-gexit` / invented flags → false CI green; note 60). Limit: JVM System.exit ≠ Godot/GUT process model.**
- **How:** Adjacent analog hold-with-limit; flips 37/42/49: 0.
- **Gotchas:** STUDY-044 deepen note. Do not flip 37/42/49. Do not invent -gexit_on_complete as official.
- **Verify (shaky):** STUDY-044 deepen; flips 37/42/49: 0; default unverified [no external verdict — not checked]
- **Sources:** [Gradle #8739 System.exit false-green](https://github.com/gradle/gradle/issues/8739) — Analog: wrong exit path → BUILD SUCCESSFUL while tests never finished. Holds for recipe 49 (missing `-gexit` / invented flags → false CI green; note 60). Limit: JVM System.exit ≠ Godot/GUT process mod

### Open Datasheets: Machine-readable Documentation for Open Datasets and Responsible AI Assessments · `⚠ shaky` · Godot 4.x
**No-code machine-readable open-dataset documentation for RAI assessments — supports README/catalog counts that mirror declared fields, not silent verified invent.**
- **How:** Catalog/README count honesty deepen; no flip 37/42/49; no invent APIs.
- **Gotchas:** STUDY-065. Flips 37/42/49: 0. APIs invented: 0.
- **Verify (shaky):** STUDY-065; flips 37/42/49: 0; APIs invented: 0; default unverified [no external verdict — not checked]
- **Sources:** [Open Datasheets: Machine-readable Documentation for Open Datasets and Responsible AI Assessments](https://arxiv.org/abs/2312.06153) — No-code machine-readable open-dataset documentation for RAI assessments — supports README/catalog counts that mirror declared fields, not silent verified invent.

### Pytest exit codes · `⚠ shaky` · Godot 4.x
**Analog: named public exit-code contract. Holds: recipe 49 CI must consume documented GUT codes (`-gexit` / `-gexit_on_success` only; gut.readthedocs.io Command-Line). Limit: pytest integers ≠ GUT `-g*` spelling.**
- **How:** Adjacent analog hold-with-limit; flips 37/42/49: 0.
- **Gotchas:** STUDY-044 deepen note. Do not flip 37/42/49. Do not invent -gexit_on_complete as official.
- **Verify (shaky):** STUDY-044 deepen; flips 37/42/49: 0; default unverified [no external verdict — not checked]
- **Sources:** [Pytest exit codes](https://docs.pytest.org/en/stable/reference/exit-codes.html) — Analog: named public exit-code contract. Holds: recipe 49 CI must consume documented GUT codes (`-gexit` / `-gexit_on_success` only; gut.readthedocs.io Command-Line). Limit: pytest integers ≠ GUT `-g*

### Regulatory compliance-readiness in the AI Supply Chain: examining datasets in Hugging Face · `⚠ shaky` · Godot 4.x
**Audits HF datasets for regulatory readiness gaps — claim vs documented readiness mismatch; supports refusing silent verified mass-flips.**
- **How:** Catalog/README count honesty deepen; no flip 37/42/49; no invent APIs.
- **Gotchas:** STUDY-065. Flips 37/42/49: 0. APIs invented: 0.
- **Verify (shaky):** STUDY-065; flips 37/42/49: 0; APIs invented: 0; default unverified [no external verdict — not checked]
- **Sources:** [Regulatory compliance-readiness in the AI Supply Chain: examining datasets in Hugging Face](https://arxiv.org/abs/2607.03310) — Audits HF datasets for regulatory readiness gaps — claim vs documented readiness mismatch; supports refusing silent verified mass-flips.

### Run GUT headlessly in GitHub Actions with cache + import warm-up (the green-CI pattern) · `⚠ shaky` · Godot Godot 4.5.x/4.6.x headless; GUT 9.x; actions/checkout@v4, actions/cache@v4
**A reliable GitHub Actions workflow that installs a pinned Godot binary, warms the import cache, then runs GUT headlessly so a single failing test fails the job. This is the external-verifier gate for every crew-authored change.**
- **How:** Use a setup action — `chickensoft-games/setup-godot` or `SolarLabyrinth/Action-Setup-Godot` — pinned to your exact version (e.g. 4.6.3) WITH export templates. Then two steps: (1) IMPORT WARM-UP: `godot --headless --import` (or `--headless --import --quit-after 100`) with `continue-on-error: true` — Godot's headless import is flaky and may exit non-zero even on success, so tolerate it here and only here. (2) TEST RUN: `godot --headless -s res://addons/gut/gut_cmdln.gd -gdir=res://test -gprefix=test_ -gsuffix=.gd -glog=2 -gexit_on_complete` (NO continue-on-error — let exit code 1 fail the job). Cache two things with `actions/cache@v4`: the Godot binary keyed by version, and the `.godot/` import directory keyed by a hash of project files (saves 30-60s/run). Required GUT CI flags: `-gexit_on_complete` (exit when done), `-gdir` (test dir), and `-glog=2`. Always add `workflow_dispatch` for manual runs and `paths:` filters so CI only fires on script/scene/test changes.
- **Gotchas:** Godot-3 CI tutorials use `-s` script execution differently and lack `--headless` (3.x used `--no-window`); on 4.x always use `--headless`. The single biggest CI failure mode is a cold asset cache: run the import warm-up BEFORE tests or the first headless run can crash. Some setups also need `--audio-driver Dummy`/`--display-driver headless` on bare runners, and `GODOT_DISABLE_LEAK_CHECKS=1` to avoid leak-check false negatives failing the job. Use `ubuntu-latest` (Linux ≈ 1× cost) for the test job — Windows/macOS runners are only needed for platform-specific EXPORT, not for running tests.
- **Verify (shaky):** Defect: the headline CI command and 'Required GUT CI flags' list both rely on -gexit_on_complete, which does NOT exist in the official GUT 9.5.0/9.6.0 readthedocs docs — they list only -gexit and -gexit_on_success. The flag propagates from the recipe's own cited helpmetest.com blog, not GUT docs. -gexit already returns exit code 1 on any failure (the exact CI behavior wanted), so the command should use -gexit. As written it risks the 'Unrecognized options' error the recipe's OWN gotcha warns about. Everything else (setup-godot pinning+templates confirmed maintained 4.x, --headless --import warm-up, continue-on-error only on import, actions/cache@v4, ubuntu-latest) is solid. [no external verdict — not checked]
- **Sources:** [CI/CD for Godot Projects: GUT + GitHub Actions (2026)](https://helpmetest.com/blog/godot-ci-cd-testing/) ; [chickensoft-games/setup-godot (headless CI setup action)](https://github.com/chickensoft-games/setup-godot) ; [CI-tested GUT for Godot 4: fast, green, and reliable — Kpicaza](https://medium.com/@kpicaza/ci-tested-gut-for-godot-4-fast-green-and-reliable-c56f16cde73d)

### SetGo: Metadata Readiness for Scientific AI Datasets · `⚠ shaky` · Godot 4.x
**Separates computational readiness from metadata readiness — README status must match metadata readiness, not invent flips for leftover 37/42/49.**
- **How:** Catalog/README count honesty deepen; no flip 37/42/49; no invent APIs.
- **Gotchas:** STUDY-065. Flips 37/42/49: 0. APIs invented: 0.
- **Verify (shaky):** STUDY-065; flips 37/42/49: 0; APIs invented: 0; default unverified [no external verdict — not checked]
- **Sources:** [SetGo: Metadata Readiness for Scientific AI Datasets](https://arxiv.org/abs/2607.22677) — Separates computational readiness from metadata readiness — README status must match metadata readiness, not invent flips for leftover 37/42/49.

### The Importance of Discerning Flaky from Fault-triggering Test Failures: A Case Study on the Chromium CI · `⚠ shaky` · Godot 4.x
**Flaky tests pass/fail on same version and create false alerts; CI must separate flaky failures from fault-triggering ones — false-signal CI frame for recipe 49 (no flip).**
- **How:** Literature deepen for leftover 37/42/49; no verified flip.
- **Gotchas:** STUDY-044 deepen note. Do not flip 37/42/49. Do not invent -gexit_on_complete as official.
- **Verify (shaky):** STUDY-044 deepen; flips 37/42/49: 0; default unverified [no external verdict — not checked]
- **Sources:** [The Importance of Discerning Flaky from Fault-triggering Test Failures: A Case S](https://arxiv.org/abs/2302.10594) — Flaky tests pass/fail on same version and create false alerts; CI must separate flaky failures from fault-triggering ones — false-signal CI frame for recipe 49 (no flip).

### Understanding and Detecting Flaky Builds in GitHub Actions · `⚠ shaky` · Godot 4.x
**Large-scale GHA study: reruns; 67.73% of rerun builds flaky (outcome changes without code change) — unreliable green/rerun CI for recipe 49 deepen (omit STUDY-025 eight; no flip).**
- **How:** Literature deepen for leftover 37/42/49; no verified flip.
- **Gotchas:** STUDY-044 deepen note. Do not flip 37/42/49. Do not invent -gexit_on_complete as official.
- **Verify (shaky):** STUDY-044 deepen; flips 37/42/49: 0; default unverified [no external verdict — not checked]
- **Sources:** [Understanding and Detecting Flaky Builds in GitHub Actions](https://arxiv.org/abs/2602.02307) — Large-scale GHA study: reruns; 67.73% of rerun builds flaky (outcome changes without code change) — unreliable green/rerun CI for recipe 49 deepen (omit STUDY-025 eight; no flip).

### Workflow Cards: Structured Summaries of Workflow Executions Using Provenance Data · `⚠ shaky` · Godot 4.x
**Extends Model/Data Cards to workflow provenance for executions — wave/load receipts as structured provenance without inventing APIs or flipping gated rows.**
- **How:** Catalog/README count honesty deepen; no flip 37/42/49; no invent APIs.
- **Gotchas:** STUDY-065. Flips 37/42/49: 0. APIs invented: 0.
- **Verify (shaky):** STUDY-065; flips 37/42/49: 0; APIs invented: 0; default unverified [no external verdict — not checked]
- **Sources:** [Workflow Cards: Structured Summaries of Workflow Executions Using Provenance Data](https://arxiv.org/abs/2608.11022) — Extends Model/Data Cards to workflow provenance for executions — wave/load receipts as structured provenance without inventing APIs or flipping gated rows.

### helpmetest Godot CI blog (id 49 URL) · `⚠ shaky` · Godot 4.x
****On page:** `--headless`, binary+import cache, `gut_cmdln.gd`, workflow sample, flags table including **`-gexit_on_complete`**. Blog SEO — distrust alone.**
- **How:** URL-open / official support deepen; 37/42/49 verified=0 stays.
- **Gotchas:** STUDY-044 deepen note. Do not flip 37/42/49. Do not invent -gexit_on_complete as official.
- **Verify (shaky):** STUDY-044 deepen; flips 37/42/49: 0; default unverified [no external verdict — not checked]
- **Sources:** [helpmetest Godot CI blog (id 49 URL)](https://helpmetest.com/blog/godot-ci-cd-testing/) — **On page:** `--headless`, binary+import cache, `gut_cmdln.gd`, workflow sample, flags table including **`-gexit_on_complete`**. Blog SEO — distrust alone.

### GUT CLI -gexit / -gexit_on_success (4.7.x) · `?` · Godot 4.7.x
**CLI documents -gexit / -gexit_on_success only (no -gexit_on_complete); GUT 9.7.1 targets Godot 4.7.x — recipe 49 stays verified=0.**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Gotchas:** recipe 49 stays verified=0.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 (do not flip 37/42/49) [no external verdict — not checked]
- **Sources:** [GUT CLI -gexit / -gexit_on_success (4.7.x)](https://gut.readthedocs.io/en/latest/Command-Line.html) — official GUT exit flags; recipe 49 stays

### GameCraft-Bench — Godot 4 end-to-end agent bench · `?` · Godot 4.x
**Instantiates end-to-end game gen in Godot 4 (text scenes, native 2D, headless CLI); strongest agent 41.46%; chooses Godot over Unity/Unreal for reproducible 2D engine grounding.**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Gotchas:** No invent 5.x.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 (do not flip 37/42/49) [no external verdict — not checked]
- **Sources:** [GameCraft-Bench — Godot 4 end-to-end agent bench](https://arxiv.org/abs/2606.17861) — Godot 4 default 2D bench; headless+text

### GameDevBench — Godot 4 tutorial agent tasks · `?` · Godot 4.x
**333 Godot 4 tutorial tasks; agents ~51% on gameplay vs ~33% on 2D graphics/animation (spritesheets, AnimatedSprite2D patterns); headless GDScript tests verify animation/physics without flipping recipe 37.**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Gotchas:** No invent 5.x.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 (do not flip 37/42/49) [no external verdict — not checked]
- **Sources:** [GameDevBench — Godot 4 tutorial agent tasks](https://arxiv.org/abs/2602.11103) — agents weak on 2D graphics/animation; recipe 37 not auto-green

### Gradle #8739 System.exit false-green analog · `?` · Godot 4.x
**Analog: wrong exit path yields BUILD SUCCESSFUL while tests never ran. Holds for recipe 49 (invented -gexit_on_complete → false CI green).**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 (do not flip 37/42/49) [no external verdict — not checked]
- **Sources:** [Gradle #8739 System.exit false-green analog](https://github.com/gradle/gradle/issues/8739) — false-green exit; recipe 49 stays

### JAMER — Godot 4.x headless jam verify · `?` · Godot 4.x
**Godot 4.x headless L1–L3 pipeline verifies 8,133 jam projects; text.tscn/.gd + headless runtime remains the scalable professional-engine eval surface (tooling/CI currency).**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Gotchas:** No invent 5.x.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 (do not flip 37/42/49) [no external verdict — not checked]
- **Sources:** [JAMER — Godot 4.x headless jam verify](https://arxiv.org/abs/2606.19830) — text+headless professional-engine eval

### Pytest exit codes — named exit contract analog · `?` · Godot 4.x
**Analog: named exit-code contract is public API. Holds: CI must use documented flags/codes; inventing names fails closed.**
- **How:** See source URL; STUDY-002 Verifier-verified finding.
- **Gotchas:** No invent 5.x.
- **Verify ():** STUDY-012 from STUDY-002 Verifier ✅; default verified=0 (do not flip 37/42/49) [no external verdict — not checked]
- **Sources:** [Pytest exit codes — named exit contract analog](https://docs.pytest.org/en/stable/reference/exit-codes.html) — documented exit flags; recipe 49 stays

