# agent-tooling-knowledge

**Status:** Wave 1 (2026-10-20). Catalog **18 findings · 18/18 verified · 1 wave**. Every finding was re-checked on
2026-10-20; nothing loads unverified.

Measured and documented behaviour of the harnesses that run AI agents: Claude Code headless and MCP, permissions and containment, agent sandboxes, agent tracing. What a studio harness must know so an agent run does what it claims.

- **Wave 1 (promoted from rnd, re-probed live)** — [dispatch](waves/wave-01-rnd-agent-harness-reprobes/dispatch.md) ·
  [verification](waves/wave-01-rnd-agent-harness-reprobes/verification.md) · [research-raw](waves/wave-01-rnd-agent-harness-reprobes/research-raw.json) — 18 findings, 18 verified.

## Lanes

| Lane | What it covers |
|---|---|
| [Claude Code headless & MCP](catalog/claude-code-headless.md) | print/stream-json mode, the init event, MCP servers at the first turn |
| [Permissions & containment](catalog/permissions-containment.md) | deny rules and their path anchors, what they don't contain, OS-level containment |
| [Agent sandboxes](catalog/agent-sandboxes.md) | Docker Sandboxes (sbx): credentials, network policy, reaching host services, gotchas |
| [Agent tracing](catalog/agent-tracing.md) | NeMo Relay: what it records locally, what left the machine, trace privacy |

## What belongs here, and what doesn't

- **Here:** how an agent harness behaves, measured on the rig or stated in a primary document, with the versions it
  was measured on.
- **model-knowledge:** a model's own facts, even when measured under a harness (a local model's context setting
  under Claude Code is there).
- **docker-knowledge:** GPU inference placement in containers.

## Build

```
python scripts/load_db.py waves/<wave>/research-raw.json
python scripts/gen_catalog.py
python scripts/gen_loadout.py
python scripts/refresh_meta.py
python ../shared/gen_root_index.py && python ../shared/gen_root_loadout.py
```

Verification follows the repo's [conventions](../CONVENTIONS.md): a finding is verified only by a verdict that names
what checked it.
