# Permissions & containment
_Permission rules (deny/allow, path anchors), what they do and do not contain, OS-level containment_ · wave 1 · 2026-10-20 · [‹ catalog index](README.md)

7 findings · 4 load-bearing · 7 verified.

| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |
|------|---------|-------|--------|------------|------|---|
| gotcha | A Grep rooted above a Read-denied tree lists the denied files (2.1.197) | On Claude Code 2.1.197, a Grep whose path is a directory above a Read-denied tree returns the names of files inside the tree, with both `Read(~/**)` and `Read(//X/**)`. | both sentinels listed, 3 of 3 runs | Claude Code 2.1.197; `Read(~/**)` and `Read(//X/**)` | ●●● | ✓ |
| gotcha | A one-slash permission path anchors at the settings source, not the filesystem root | In a Claude Code permission rule, `Read(/home/…)` with one leading slash is anchored at the settings source, so it does not deny that absolute path; an absolute path is written `//home/…`. | every Grep leaked with the one-slash form | Claude Code 2.1.197 and 2.1.280 | ●●● | ✓ |
| method | An unprivileged user with root-only trees contained every route | Running the CLI as an unprivileged user, with every tree it must not see owned by root and closed to others, stopped every route a containment probe tried: Read, Grep, Glob and Bash, 29 of 29 calls, 0 leaks. | 29 of 29 calls, 0 leaks | Claude Code 2.1.197 in a Docker sandbox | ●●● | ✓ |
| gotcha | With `Read(~/**)`, a Grep at `~` itself lists the denied files (2.1.197) | On Claude Code 2.1.197 with `Read(~/**)` denied, a Grep whose path is the home directory itself returns the names of files under it. | 2 of 2 runs | Claude Code 2.1.197; `Read(~/**)` | ●●● | ✓ |
| behaviour | Claude Code 2.1.280 filters a Grep above a Read-denied tree | On Claude Code 2.1.280 with `Read(//X/**)` denied, a Grep rooted above X returned "No files found" for files that exist only inside X. | no denied file listed | Claude Code 2.1.280; `Read(//X/**)` only | ●●● | ✓ |
| constraint | Claude Code documents Read rules on search tools as best-effort | Claude Code's permissions documentation says Read rules are applied to Grep and Glob as a best-effort attempt, against the directory a search's path resolves to, and points to its sandbox for OS-level enforcement. |  | Claude Code permissions documentation (read 2026-10-20) | ●●● | ✓ |
| behaviour | With `Read(//X/**)`, a Grep at X or inside it is refused | On Claude Code 2.1.197 and 2.1.280, with `Read(//X/**)` denied, a Grep whose path is X itself or a directory inside X is refused with "Permission to read … has been denied". | refused, 2 versions | Claude Code 2.1.197 and 2.1.280; `Read(//X/**)` | ●●● | ✓ |

## Detail

### A Grep rooted above a Read-denied tree lists the denied files (2.1.197) · `load-bearing` · gotcha
**On Claude Code 2.1.197, a Grep whose path is a directory above a Read-denied tree returns the names of files inside the tree, with both `Read(~/**)` and `Read(//X/**)`.**
The deny rule is checked against the directory a search starts from, not each file the walk reaches. Sentinel files with random suffixes were listed by name.
- **Applies to:** Claude Code 2.1.197; `Read(~/**)` and `Read(//X/**)` · **Metric:** both sentinels listed, 3 of 3 runs · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Deny rules are not a containment boundary. Keep files an agent must not see out of its reach at OS level (a separate user, root-owned trees, or nothing on its filesystem); use deny rules only as a second layer.
- **Verify:** verdict=confirmed | via live re-probe 2026-10-20 (b2abs-pin.jsonl, b2home-pin-1/2.jsonl), 2026-10-20
- **Sources:** [rnd: a Read deny rule doesn't stop a Grep walk over the denied tree](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-claude-code-read-deny-rules-do-not-stop-a-grep-walk.md) — SUPPORTED ; [Claude Code: Configure permissions](https://code.claude.com/docs/en/permissions) — SUPPORTED

### A one-slash permission path anchors at the settings source, not the filesystem root · `load-bearing` · gotcha
**In a Claude Code permission rule, `Read(/home/…)` with one leading slash is anchored at the settings source, so it does not deny that absolute path; an absolute path is written `//home/…`.**
Measured: with `Read(/home/agent/b2probe/**)`, every Grep (root, above and inside) listed the sentinels on 2.1.197 and 2.1.280. The permissions documentation states the anchoring rule.
- **Applies to:** Claude Code 2.1.197 and 2.1.280 · **Metric:** every Grep leaked with the one-slash form · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Lint deny rules: an absolute path must start with `//` (or `~/` for home).
- **Verify:** verdict=confirmed | via live re-probe 2026-10-20 (b2-pin.jsonl, b2-cur.jsonl); Claude Code permissions documentation read 2026-10-20, 2026-10-20
- **Sources:** [Claude Code: Configure permissions](https://code.claude.com/docs/en/permissions) — SUPPORTED ; [rnd: a Read deny rule doesn't stop a Grep walk over the denied tree](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-claude-code-read-deny-rules-do-not-stop-a-grep-walk.md) — SUPPORTED

### An unprivileged user with root-only trees contained every route · `load-bearing` · method
**Running the CLI as an unprivileged user, with every tree it must not see owned by root and closed to others, stopped every route a containment probe tried: Read, Grep, Glob and Bash, 29 of 29 calls, 0 leaks.**
The studio's agent A/B harness (amendment 8) adopted it.
- **Applies to:** Claude Code 2.1.197 in a Docker sandbox · **Metric:** 29 of 29 calls, 0 leaks · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Use OS file permissions as the containment for agent runs that must not see answer keys or credentials.
- **Verify:** verdict=confirmed | via the harness's pilot probe reports of 2026-10-13/14, recovered read-only from the sandbox 2026-10-20 (jobA2), 2026-10-20
- **Sources:** [rnd: a Read deny rule doesn't stop a Grep walk over the denied tree](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-claude-code-read-deny-rules-do-not-stop-a-grep-walk.md) — SUPPORTED

### With `Read(~/**)`, a Grep at `~` itself lists the denied files (2.1.197) · `load-bearing` · gotcha
**On Claude Code 2.1.197 with `Read(~/**)` denied, a Grep whose path is the home directory itself returns the names of files under it.**
Seen in the 2026-10-13 containment probe and in 2 of 2 runs on 2026-10-20. With the absolute form `Read(//X/**)`, a Grep at X is refused instead, so which root leaks depends on how the rule is written.
- **Applies to:** Claude Code 2.1.197; `Read(~/**)` · **Metric:** 2 of 2 runs · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Don't treat `Read(~/**)` as hiding the home directory from a search tool.
- **Verify:** verdict=confirmed | via live re-probe 2026-10-20 (b2home-pin-1/2.jsonl); the 2026-10-13 probe as recorded by the Publisher, 2026-10-20
- **Sources:** [rnd: a Read deny rule doesn't stop a Grep walk over the denied tree](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-claude-code-read-deny-rules-do-not-stop-a-grep-walk.md) — SUPPORTED

### Claude Code 2.1.280 filters a Grep above a Read-denied tree · `supporting` · behaviour
**On Claude Code 2.1.280 with `Read(//X/**)` denied, a Grep rooted above X returned "No files found" for files that exist only inside X.**
The `~` form was not tested on 2.1.280.
- **Applies to:** Claude Code 2.1.280; `Read(//X/**)` only · **Metric:** no denied file listed · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Pin a CLI version for any harness that relies on deny rules, and re-probe after an upgrade.
- **Verify:** verdict=confirmed | via live re-probe 2026-10-20 (b2abs-cur.jsonl), 2026-10-20
- **Sources:** [rnd: a Read deny rule doesn't stop a Grep walk over the denied tree](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-claude-code-read-deny-rules-do-not-stop-a-grep-walk.md) — SUPPORTED

### Claude Code documents Read rules on search tools as best-effort · `supporting` · constraint
**Claude Code's permissions documentation says Read rules are applied to Grep and Glob as a best-effort attempt, against the directory a search's path resolves to, and points to its sandbox for OS-level enforcement.**
So the leaks above are documented behaviour, not an undisclosed gap.
- **Applies to:** Claude Code permissions documentation (read 2026-10-20) · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Design containment at OS level from the start.
- **Verify:** verdict=confirmed | via Claude Code permissions documentation, read by the R&D seat 2026-10-20, 2026-10-20
- **Sources:** [Claude Code: Configure permissions](https://code.claude.com/docs/en/permissions) — SUPPORTED

### With `Read(//X/**)`, a Grep at X or inside it is refused · `supporting` · behaviour
**On Claude Code 2.1.197 and 2.1.280, with `Read(//X/**)` denied, a Grep whose path is X itself or a directory inside X is refused with "Permission to read … has been denied".**
Inside the tree was also refused with `Read(~/**)` on 2.1.197.
- **Applies to:** Claude Code 2.1.197 and 2.1.280; `Read(//X/**)` · **Metric:** refused, 2 versions · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Write absolute deny paths with `//`, and still don't rely on them for containment.
- **Verify:** verdict=confirmed | via live re-probe 2026-10-20 (b2abs-pin.jsonl, b2abs-cur.jsonl), 2026-10-20
- **Sources:** [rnd: a Read deny rule doesn't stop a Grep walk over the denied tree](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-claude-code-read-deny-rules-do-not-stop-a-grep-walk.md) — SUPPORTED

