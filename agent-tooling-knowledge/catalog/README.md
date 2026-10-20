# Catalog — agent-tooling-knowledge (agent harness behaviour)

Generated from `findings.db` · wave 1 · 2026-10-20. Measured and documented behaviour of the harnesses that run AI agents: Claude Code headless and MCP, permissions and containment, agent sandboxes, agent tracing. Siblings: [model-knowledge](../../model-knowledge) (the models), [docker-knowledge](../../docker-knowledge) (GPU placement).

## Load-bearing shortlist

The findings that drive a design decision. `✓` = verified, with what checked it in each row's Verify line.

| Lane | Finding | Claim | Metric | ✓ |
|---|---|---|---|---|
| Claude Code headless & MCP | [A headless first turn starts before its MCP server connects (2.1.197)](claude-code-headless.md) | In print mode with stream-json input, Claude Code 2.1.197 on Anthropic's endpoint starts the first turn as soon as the message arrives: the init event shows the MCP server `pending` and none of its tools are offered. | 0 of 7 tools offered with no hold | ✓ |
| Permissions & containment | [A Grep rooted above a Read-denied tree lists the denied files (2.1.197)](permissions-containment.md) | On Claude Code 2.1.197, a Grep whose path is a directory above a Read-denied tree returns the names of files inside the tree, with both `Read(~/**)` and `Read(//X/**)`. | both sentinels listed, 3 of 3 runs | ✓ |
| Permissions & containment | [A one-slash permission path anchors at the settings source, not the filesystem root](permissions-containment.md) | In a Claude Code permission rule, `Read(/home/…)` with one leading slash is anchored at the settings source, so it does not deny that absolute path; an absolute path is written `//home/…`. | every Grep leaked with the one-slash form | ✓ |
| Permissions & containment | [An unprivileged user with root-only trees contained every route](permissions-containment.md) | Running the CLI as an unprivileged user, with every tree it must not see owned by root and closed to others, stopped every route a containment probe tried: Read, Grep, Glob and Bash, 29 of 29 calls, 0 leaks. | 29 of 29 calls, 0 leaks | ✓ |
| Permissions & containment | [With `Read(~/**)`, a Grep at `~` itself lists the denied files (2.1.197)](permissions-containment.md) | On Claude Code 2.1.197 with `Read(~/**)` denied, a Grep whose path is the home directory itself returns the names of files under it. | 2 of 2 runs | ✓ |
| Agent tracing | [Relay's local ATOF file carries the account's identity](agent-tracing.md) | NeMo Relay's local ATOF event file contained the signed-in account's email address, with `enable_full_payloads = false`. |  | ✓ |

## Lanes

- [Claude Code headless & MCP](claude-code-headless.md) — Print/stream-json mode, the init event, MCP server lifecycle at the first turn, versions (3 findings)
- [Permissions & containment](permissions-containment.md) — Permission rules (deny/allow, path anchors), what they do and do not contain, OS-level containment (7 findings)
- [Agent sandboxes](agent-sandboxes.md) — Docker Sandboxes (sbx): setup, credentials, network policy, reaching host services, operational gotchas (4 findings)
- [Agent tracing](agent-tracing.md) — Tracing agent runs (NeMo Relay): what is recorded locally, what leaves the machine, privacy of traces (4 findings)

## Legend

- **Kind** behaviour | gotcha | constraint | method | policy.
- **Conf** confidence ●●● high / ●●· medium / ●·· low.
- **✓** verified (a live re-probe receipt or a primary document, named in the row). · = unverified.
