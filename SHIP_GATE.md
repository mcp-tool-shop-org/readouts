# Ship Gate

> No repo is "done" until every applicable line is checked.
> Copy this into your repo root. Check items off per-release.

**Tags:** `[all]` every repo · `[npm]` `[pypi]` `[vsix]` `[desktop]` `[container]` published artifacts · `[mcp]` MCP servers · `[cli]` CLI tools

**This repo:** `[all]` only. readouts is a data corpus (SQLite databases, markdown, JSON) with standard-library Python maintenance scripts and a static site. It publishes no package. Each publication is a commit on `main` (see CHANGELOG.md).

---

## A. Security Baseline

- [x] `[all]` SECURITY.md exists (report email, supported versions, response timeline) — executed by `npx @mcptoolshop/shipcheck security-docs` (A1: present + reporting contact, not an empty stub) (2026-09-25; reports go to GitHub issues, because the org's noreply address cannot receive mail and private vulnerability reporting is off)
- [x] `[all]` README includes threat model paragraph (data touched, data NOT touched, permissions required) — executed by `npx @mcptoolshop/shipcheck security-docs` (A2: trust/threat-model section present + non-empty; *quality* is not machine-checkable) (2026-09-25; separates the local read path from the research tooling that can call model APIs)
- [x] `[all]` No secrets, tokens, or credentials in source or diagnostics output — executed by `npx @mcptoolshop/shipcheck secrets` (scans every publishable tarball; matches redacted; not a manual attestation) (2026-09-25; there is no tarball, so the executed checks are the export's gates: the studio identity scanner, a home-path class gate over files and database cells, and a private-name gate, all clean on the published tree)
- [x] `[all]` No telemetry by default — state it explicitly even if obvious (2026-09-25; stated in README and SECURITY.md)

### Default safety posture

- [ ] `[cli|mcp|desktop]` SKIP: not a CLI, MCP server or desktop app. `verify.py` is read-only, and the generators write only derived files inside the checkout.
- [ ] `[cli|mcp|desktop]` SKIP: not a CLI, MCP server or desktop app. Every script resolves its paths relative to its own file, inside the checkout.
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[mcp]` SKIP: not an MCP server

## B. Error Handling

- [x] `[all]` Errors follow the Structured Error Shape: `code`, `message`, `hint`, `cause?`, `retryable?` (2026-09-25; every FAIL and WARN from `verify.py` carries a stable code and a hint, and `--json` emits `level`, `check`, `code`, `message`, `hint`, `retryable`)
- [ ] `[cli]` SKIP: not a CLI product. `verify.py` documents its own exit codes: 0 clean, 1 FAIL, 2 a check crashed.
- [ ] `[cli]` SKIP: not a CLI product. `verify.py` catches a crashing check and reports it as `RUNTIME_CHECK_CRASHED` instead of a stack trace.
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[desktop]` SKIP: not a desktop app
- [ ] `[vscode]` SKIP: not a VS Code extension

## C. Operator Docs

- [x] `[all]` README is current: what it does, install, usage, supported platforms + runtime versions (2026-09-25; Python 3.10+, any SQLite 3 client with FTS5; the KB table is generated and checked by `verify.py`)
- [x] `[all]` CHANGELOG.md (Keep a Changelog format) (2026-09-25; dated publications, since the corpus is unversioned)
- [x] `[all]` LICENSE file present and repo states support status (2026-09-25; MIT; SECURITY.md states that `main` is the only supported version)
- [ ] `[cli]` SKIP: not a CLI product
- [ ] `[cli|mcp|desktop]` SKIP: not a CLI, MCP server or desktop app; the scripts print to stdout only
- [ ] `[mcp]` SKIP: not an MCP server
- [ ] `[complex]` SKIP: no daemons, state files or operational modes. The handbook covers querying, verification and maintenance.

## D. Shipping Hygiene

- [x] `[all]` `verify` script exists (test + build + smoke in one command) (2026-09-25; `python verify.py`, twelve checks, run in CI by `verify.yml` and by the export on the published tree)
- [ ] `[all]` SKIP: no manifest version and no tags. readouts is a rolling corpus; each publication is a dated CHANGELOG entry and a commit on `main`.
- [x] `[all]` Dependency scanning runs in CI (ecosystem-appropriate) — executed by `npx @mcptoolshop/shipcheck ci` (D3: a recognized scanner is *configured* in CI, or dependabot is present) (2026-09-25; `npm audit --audit-level=high` runs before every Pages build. `shipcheck ci` reports "skipped" here because it looks for a root manifest and the only npm tree is `site/`; `shipcheck deps --no-alerts` audits that tree and passes. The Python scripts have no third-party dependencies)
- [ ] `[all]` No known high/critical vulnerabilities in any dependency tree, and Dependabot alerts are enabled — executed by `npx @mcptoolshop/shipcheck deps` (the OUTCOME: audits **every** tree incl. subtrees, not just the root; `ci` only proves a scanner is configured) — OPEN: `site/` audits clean (0 high or critical), but Dependabot alerts are off. Enabling them is a repository security setting for the owner: `gh api -X PUT repos/mcp-tool-shop-org/readouts/vulnerability-alerts`
- [ ] `[all]` SKIP: the org rule restricts automated update PRs to explicit requests. `npm audit` gates every site build instead.
- [ ] `[npm]` SKIP: publishes no npm package
- [ ] `[npm]` SKIP: publishes no npm package
- [ ] `[npm]` SKIP: publishes no npm or PyPI package
- [ ] `[npm]` SKIP: publishes no npm or PyPI package (`site/package-lock.json` is committed for the site build)
- [ ] `[vsix]` SKIP: not a VS Code extension
- [ ] `[desktop]` SKIP: not a desktop app

## E. Identity (soft gate — does not block ship)

- [x] `[all]` Logo in README header (2026-09-25; brand `logos/readouts/readme.png`)
- [x] `[all]` Translations (polyglot-mcp, 8 languages) (2026-09-25; README in English plus seven translations, TranslateGemma 27B run locally)
- [x] `[org]` Landing page (@mcptoolshop/site-theme) (2026-09-25; https://mcp-tool-shop-org.github.io/readouts/ with a Starlight handbook)
- [x] `[all]` GitHub repo metadata: description, homepage, topics (2026-09-25)

---

## Gate Rules

**Hard gate (A–D):** Must pass before any version is tagged or published.
If a section doesn't apply, mark `SKIP:` with justification — don't leave it unchecked.

**Soft gate (E):** Should be done. Product ships without it, but isn't "whole."

**Executed vs attested.** `shipcheck audit` only *counts these checkboxes* — it does not read your repo, so a box can be green while the fact is false. The lines that say **"executed by `npx @mcptoolshop/shipcheck <gate>`"** are backed by a command that reads the real artifact and exits 1 on the real defect. Run those gates (they are wired into shipcheck's own `verify`); don't just tick their boxes. Executed today: **A1/A2** (`security-docs`), **A3** (`secrets`), **D2/D6/D7** (`manifest`), **D3-config + OIDC/provenance** (`ci`), **real vulnerabilities + alerting** (`deps`), **D5** (`pack`), plus front-door (`front-door`) and dogfood freshness (`dogfood`). Every other line is still an attestation you are vouching for. Note the two dependency layers: `ci` proves a scanner is *configured*; `deps` proves there are *no known vulnerabilities* — a repo can pass the first while failing the second.

**Checking off:**
```
- [x] `[all]` SECURITY.md exists (2026-02-27)
```

**Skipping:**
```
- [ ] `[pypi]` SKIP: not a Python project
```
