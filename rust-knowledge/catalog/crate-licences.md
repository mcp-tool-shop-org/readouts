# Crate licences for a shipped MIT/Apache product
_Licence allowlists, weak copyleft decisions, attribution output, and which licences reach a shipped binary._ · tier **si-jam-sessions** · wave 5 · 2026-09-25 · [‹ catalog index](README.md)

10 recipes · 10 verified · 0 compiler-checked.

| Recipe | Rust | Currency | ✓ | Code | What |
|--------|------|----------|---|------|------|
| Configure cargo-deny explicit allowlist for MIT/Apache products | 1.98.1 | ✅ solid | ✓ | · | cargo-deny denies all licences by default and only permits those listed in [licenses] allo |
| Plan for MPL-2.0 file-level copyleft if introduced later | 1.98.1 | ✅ solid | ✓ | · | Inference: MPL-2.0 is a file-level copyleft licence; under a default-deny MIT/Apache cargo |
| Preserve MIT copyright notices for abc-parser and midir | abc-parser 0.4.0, midir 0.11.0 | ✅ solid | ✓ | · | MIT-licensed crates require the copyright and permission notice to be included in all copi |
| Retain BSD-1-Clause copyright notice for assert_no_alloc source | assert_no_alloc 1.1.2 | ✅ solid | ✓ | · | assert_no_alloc 1.1.2 is under BSD-1-Clause, which requires retaining the copyright notice |
| Ship Apache-2.0 licence copy for cpal and reproduce NOTICE if present | cpal 0.18.2 | ✅ solid | ✓ | · | cpal 0.18.2 is Apache-2.0-only; the licence text requires giving recipients a copy of the  |
| Treat midly as public domain under Unlicense | midly 0.5.3 | ✅ solid | ✓ | · | midly 0.5.3 is dedicated to the public domain via the Unlicense, imposing no licence repro |
| Add per-crate licence exceptions in cargo-deny | 1.98.1 | ⚠ shaky | ✓ | · | The exceptions field allows a licence only for a specific crate version, preventing implic |
| Clarify ambiguous crate licences with hashed file assertions | 1.98.1 | ⚠ shaky | ✓ | · | When a crate lacks machine-readable licence metadata, [[licenses.clarify]] assigns an SPDX |
| Enumerate native host-only Apache-2.0 and BSD-1-Clause dependencies | cpal 0.18.2, assert_no_alloc 1.1.2 | ▸ plausible | ✓ | · | The native host links cpal under Apache-2.0-only and assert_no_alloc under BSD-1-Clause, w |
| List permissive licences linked into the wasm32 law binary | midly 0.5.3, abc-parser 0.4.0 | ▸ plausible | ✓ | · | The wasm law links midly under Unlicense and abc-parser under MIT, with no copyleft obliga |

## Detail

### Configure cargo-deny explicit allowlist for MIT/Apache products
`✅ solid` · ✓ verified · · no code check · Rust 1.98.1

**cargo-deny denies all licences by default and only permits those listed in [licenses] allow.**

- **How:** Populate allow = ["MIT", "Apache-2.0", "Unlicense", "BSD-1-Clause", "0BSD", "Zlib"] and set confidence-threshold = 0.95.
- **Gotchas:** GNU licences are treated pedantically; SPDX identifiers must match exactly. No MPL-2.0 is in the current set, so it need not be allowed yet.
- **In si-jam-sessions:** Bears on CI/licence scanning for both wasm and native targets; configure cargo-deny to enforce the product's MIT/Apache allowlist.

- **Verifier (solid):** cfg.html: 'Licenses not in this list are denied by default.' Gotcha 'GNU licences treated pedantically' is a literal current-docs quote. confidence-threshold is real (default 0.8); 0.95 is valid stricter config, not a false default. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 8 (crate-licences): cargo-deny allowlist MIT / Apache-2.0 / Unlicense / BSD-1-Clause plus one scoped exception for unicode-ident. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [config - cargo-deny](https://embarkstudios.github.io/cargo-deny/checks/licenses/cfg.html) (2026) — All licenses are denied unless explicitly allowed in the allow list.
  - ✓ [licenses - cargo-deny](https://embarkstudios.github.io/cargo-deny/checks/licenses/index.html) (2026) — cargo-deny evaluates the license requirements specified by each crate against the configuration to determine if the project meets that crate's license requirements.

### Plan for MPL-2.0 file-level copyleft if introduced later
`✅ solid` · ✓ verified · · no code check · Rust 1.98.1

**Inference: MPL-2.0 is a file-level copyleft licence; under a default-deny MIT/Apache cargo-deny allowlist it would be rejected unless explicitly allowed, and modifications to files containing MPL-licensed code would have to be shared while the larger static binary would not.**

- **How:** If an MPL-2.0 crate is added, list MPL-2.0 in allow or exceptions; ensure any modified MPL files are published under MPL-2.0, but new files and the overall binary may remain proprietary.
- **Gotchas:** MPL-2.0 is absent from the current dependency set; this recipe is forward-looking for future dependency additions.
- **In si-jam-sessions:** Bears on future dependency additions; an MPL-2.0 crate would trigger file-level copyleft obligations on its own files.

- **Verifier (solid):** Mozilla FAQ confirms file-level copyleft, static-link-into-proprietary permission, and modified-MPL-files-vs-whole-binary obligation split verbatim. MPL-2.0 confirmed absent from all 10 pinned tier crates' declared licences.
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [MPL 2.0 FAQ — Mozilla](https://www.mozilla.org/en-US/MPL/2.0/FAQ/) (2026) — The MPL is a file-level copyleft license that allows programs using MPL-licensed code to be statically linked to and distributed as part of a larger proprietary piece of software.
  - ✓ [config - cargo-deny](https://embarkstudios.github.io/cargo-deny/checks/licenses/cfg.html) (2026) — All licenses are denied unless explicitly allowed.

### Preserve MIT copyright notices for abc-parser and midir
`✅ solid` · ✓ verified · · no code check · Rust abc-parser 0.4.0, midir 0.11.0

**MIT-licensed crates require the copyright and permission notice to be included in all copies or substantial portions of the Software.**

- **How:** Include the LICENSE file text for abc-parser, midir, quick-xml, musicxml, and other MIT crates in the product's attribution output (e.g., generated by cargo-about).
- **Gotchas:** Substantial portions is interpreted broadly; include the full MIT licence text for each crate to be safe.
- **In si-jam-sessions:** Bears on attribution output for shipped binaries; MIT notices must be preserved in binary distributions.

- **Verifier (solid):** abc-parser and midir LICENSE files both quoted live: 'copyright notice and this permission notice shall be included in all copies or substantial portions' -- exact match, word for word, on both. quick-xml/musicxml also confirmed MIT.
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [abc-parser 0.4.0 LICENSE](https://docs.rs/crate/abc-parser/0.4.0/source/LICENSE) (2026) — The MIT license text states that the copyright notice and permission notice shall be included in all copies or substantial portions of the Software.
  - ✓ [midir 0.11.0 LICENSE](https://docs.rs/crate/midir/0.11.0/source/LICENSE) (2026) — The MIT license text states that the copyright notice and permission notice shall be included in all copies or substantial portions of the Software.

### Retain BSD-1-Clause copyright notice for assert_no_alloc source
`✅ solid` · ✓ verified · · no code check · Rust assert_no_alloc 1.1.2

**assert_no_alloc 1.1.2 is under BSD-1-Clause, which requires retaining the copyright notice and disclaimer in source redistributions but places no conditions on binary distributions.**

- **How:** Preserve the LICENSE file text when distributing source; for binary shipments of the native host no additional BSD-1-Clause action is required.
- **Gotchas:** Assumption: the native host binary is the primary shipped artifact; source distribution is separate.
- **In si-jam-sessions:** Bears on the shipped native host binary; assert_no_alloc is BSD-1-Clause and requires source redistribution to retain copyright.

- **Verifier (solid):** assert_no_alloc's own shipped LICENSE (registry, version 1.1.2) is the literal 1-clause BSD form: source-retention clause only, zero binary-form clause -- exact match to both the claim and the SPDX BSD-1-Clause canonical text.
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [assert_no_alloc 1.1.2 Cargo.toml](https://docs.rs/crate/assert_no_alloc/1.1.2/source/Cargo.toml) (2026) — assert_no_alloc 1.1.2 declares license = "BSD-1-Clause".
  - ✓ [BSD 1-Clause License / SPDX](https://spdx.org/licenses/BSD-1-Clause.html) (2026) — BSD-1-Clause requires redistributions of source code to retain the above copyright notice, this list of conditions and the following disclaimer.

### Ship Apache-2.0 licence copy for cpal and reproduce NOTICE if present
`✅ solid` · ✓ verified · · no code check · Rust cpal 0.18.2

**cpal 0.18.2 is Apache-2.0-only; the licence text requires giving recipients a copy of the licence and reproducing any NOTICE file contents if the Work includes one.**

- **How:** Include the Apache-2.0 licence text in attribution output; cpal 0.18.2 ships only a LICENSE file and no NOTICE file, so there is no cpal NOTICE text to reproduce.
- **Gotchas:** Assumption: cpal 0.18.2 ships no NOTICE file (the crate contains only LICENSE). Future cpal versions must be re-checked.
- **In si-jam-sessions:** Bears on the shipped native host binary; cpal is Apache-2.0 and requires licence copy and NOTICE reproduction if present.

- **Verifier (solid):** cpal 0.18.2's LICENSE is the unmodified 201-line Apache-2.0 text; clause 4(a) requires a licence copy, 4(d) the NOTICE clause quoted matches verbatim. Full package directory listing shows LICENSE present, no NOTICE file anywhere.
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [cpal 0.18.2 Cargo.toml](https://docs.rs/crate/cpal/0.18.2/source/Cargo.toml) (2026) — cpal 0.18.2 declares license = "Apache-2.0".
  - ✓ [cpal 0.18.2 LICENSE](https://docs.rs/crate/cpal/0.18.2/source/LICENSE) (2026) — Section 4(d) of the Apache-2.0 text states that if the Work includes a NOTICE text file, any Derivative Works must include a readable copy of the attribution notices contained within such NOTICE file.

### Treat midly as public domain under Unlicense
`✅ solid` · ✓ verified · · no code check · Rust midly 0.5.3

**midly 0.5.3 is dedicated to the public domain via the Unlicense, imposing no licence reproduction obligations on shipped binaries.**

- **How:** The crate's Cargo.toml states license = "Unlicense"; the Unlicense text dedicates all copyright interest to the public domain and permits unrestricted use.
- **Gotchas:** Some tools may not recognise Unlicense automatically and may require a cargo-deny clarification or manual allowlist entry.
- **In si-jam-sessions:** Bears on the shipped wasm32 law binary; midly is public domain and requires no licence reproduction.

- **Verifier (solid):** midly Cargo.toml license="Unlicense" confirmed. SPDX text: 'released into the public domain...for any purpose...by any means', dedicates 'copyright interest'; no notice-reproduction clause, so the no-obligation claim holds.
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 Cargo.toml](https://docs.rs/crate/midly/0.5.3/source/Cargo.toml) (2026) — midly 0.5.3 declares license = "Unlicense".
  - ✓ [The Unlicense / SPDX](https://spdx.org/licenses/Unlicense.html) (2026) — The Unlicense is a public domain dedication releasing software into the public domain with no conditions.

### Add per-crate licence exceptions in cargo-deny
`⚠ shaky` · ✓ verified · · no code check · Rust 1.98.1

**The exceptions field allows a licence only for a specific crate version, preventing implicit acceptance elsewhere.**

- **How:** Add exceptions = [{ allow = ["BSD-1-Clause"], crate = "assert_no_alloc", version = "1.1.2" }] to signal that BSD-1-Clause is accepted only for this crate.
- **Gotchas:** Unused allowed licences trigger warnings by default; exceptions keep the global allowlist minimal.
- **In si-jam-sessions:** Bears on CI/licence scanning; use exceptions to isolate non-global licences like BSD-1-Clause or Unlicense.

- **Verifier (shaky):** CORRECTED: how's example used `crate = "assert_no_alloc"`; the real PackageSpec key is `name` (docs' own literal example: `name = "adler32", version = "0.1.1"`). The per-crate exception concept is correct; only the field name is wrong. · Mechanism confirmed by both sources, but the worked example's `crate = "assert_no_alloc"` key does not exist in cargo-deny's schema. The docs' own example uses `name = "adler32"` -- the PackageSpec key is `name`, not `crate`. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 8 (crate-licences): cargo-deny allowlist MIT / Apache-2.0 / Unlicense / BSD-1-Clause plus one scoped exception for unicode-ident. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [config - cargo-deny](https://embarkstudios.github.io/cargo-deny/checks/licenses/cfg.html) (2026) — The exceptions field is meant to allow additional licenses only for particular crates.
  - ✓ [licenses - cargo-deny](https://embarkstudios.github.io/cargo-deny/checks/licenses/index.html) (2026) — All licenses are denied unless explicitly allowed.

### Clarify ambiguous crate licences with hashed file assertions
`⚠ shaky` · ✓ verified · · no code check · Rust 1.98.1

**When a crate lacks machine-readable licence metadata, [[licenses.clarify]] assigns an SPDX expression tied to a hash of a source file.**

- **How:** Provide expression, path, and hash in deny.toml; cargo-deny uses the expression while the source file matches the recorded hash.
- **Gotchas:** Clarifications are temporary patches; if the crate updates and the file changes, the hash mismatch will fail the check.
- **In si-jam-sessions:** Bears on CI/licence scanning; use clarify for crates with missing SPDX metadata.

- **Verifier (shaky):** CORRECTED: how omits the required `name` key (target crate) and lists path/hash as flat keys. Real schema: `name`+`expression` top-level, `license-files = [{ path = "...", hash = 0x... }]` nested (docs' own `ring` example). · Concept confirmed by both sources, but how's 'provide expression, path, and hash' omits the required `name` key and misstates structure: real schema is top-level name+expression, with path/hash nested in `license-files = [{path,hash}]`.
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [config - cargo-deny](https://embarkstudios.github.io/cargo-deny/checks/licenses/cfg.html) (2026) — Clarify lets you manually assign an SPDX expression based on one or more files in the crate's source, valid as long as the source files exactly match the clarification's hashes.
  - ✓ [licenses - cargo-deny](https://embarkstudios.github.io/cargo-deny/checks/licenses/index.html) (2026) — cargo-deny provides a mechanism for manually specifying the license requirements for crates.

### Enumerate native host-only Apache-2.0 and BSD-1-Clause dependencies
`▸ plausible` · ✓ verified · · no code check · Rust cpal 0.18.2, assert_no_alloc 1.1.2

**The native host links cpal under Apache-2.0-only and assert_no_alloc under BSD-1-Clause, which do not appear in the wasm law.**

- **How:** cpal 0.18.2 declares license Apache-2.0; assert_no_alloc 1.1.2 declares license BSD-1-Clause. Assumption: these are native-host-only dependencies per the wave's target filter.
- **Gotchas:** Apache-2.0-only is distinct from MIT OR Apache-2.0 dual licences; it must be allowed explicitly and its NOTICE requirement checked per crate.
- **In si-jam-sessions:** Bears on the shipped native host binary; cpal and assert_no_alloc carry Apache-2.0 and BSD-1-Clause obligations respectively.

- **Verifier (plausible):** cpal=Apache-2.0, assert_no_alloc=BSD-1-Clause reconfirmed. Host-only claim self-flagged 'Assumption' in how; plausible since cpal needs OS audio APIs incompatible with a files/clocks/threads-free wasm32 cdylib, not independently proven.
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [cpal 0.18.2 Cargo.toml](https://docs.rs/crate/cpal/0.18.2/source/Cargo.toml) (2026) — cpal 0.18.2 declares license = "Apache-2.0".
  - ✓ [assert_no_alloc 1.1.2 Cargo.toml](https://docs.rs/crate/assert_no_alloc/1.1.2/source/Cargo.toml) (2026) — assert_no_alloc 1.1.2 declares license = "BSD-1-Clause".

### List permissive licences linked into the wasm32 law binary
`▸ plausible` · ✓ verified · · no code check · Rust midly 0.5.3, abc-parser 0.4.0

**The wasm law links midly under Unlicense and abc-parser under MIT, with no copyleft obligations.**

- **How:** Read the license field in each crate's Cargo.toml; midly 0.5.3 is Unlicense and abc-parser 0.4.0 is MIT. Both are normal dependencies linked into the wasm cdylib.
- **Gotchas:** Assumption: the measured dependency graph correctly identifies these as normal (binary-linked) edges for wasm32-unknown-unknown.
- **In si-jam-sessions:** Bears on the shipped wasm32 law binary; verify that all linked crate licences are permissive and documented.

- **Verifier (plausible):** midly Cargo.toml: license="Unlicense"; abc-parser Cargo.toml: license="MIT" -- both confirmed live+local, exact match. Wasm-cdylib linkage itself is self-flagged 'Assumption' in gotchas, not independently checkable pre-lock. · [operator 2026-09-25: CONSUMED PIN: si-jam-sessions docs/PHASE-0.md @ e3cc85e, pin 8 (crate-licences): cargo-deny allowlist MIT / Apache-2.0 / Unlicense / BSD-1-Clause plus one scoped exception for unicode-ident. An edit to this recipe is a lock change: raise it with si-jam-sessions before it lands.]
- **Compiler:** no code check (a claim code cannot show)
- **Sources** (✓ supported · ✗ not supported · · unchecked):
  - ✓ [midly 0.5.3 Cargo.toml](https://docs.rs/crate/midly/0.5.3/source/Cargo.toml) (2026) — midly 0.5.3 declares license = "Unlicense".
  - ✓ [abc-parser 0.4.0 Cargo.toml](https://docs.rs/crate/abc-parser/0.4.0/source/Cargo.toml) (2026) — abc-parser 0.4.0 declares license = "MIT".

