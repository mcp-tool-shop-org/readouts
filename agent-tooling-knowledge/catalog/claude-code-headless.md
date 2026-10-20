# Claude Code headless & MCP
_Print/stream-json mode, the init event, MCP server lifecycle at the first turn, versions_ · wave 1 · 2026-10-20 · [‹ catalog index](README.md)

3 findings · 1 load-bearing · 3 verified.

| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |
|------|---------|-------|--------|------------|------|---|
| gotcha | A headless first turn starts before its MCP server connects (2.1.197) | In print mode with stream-json input, Claude Code 2.1.197 on Anthropic's endpoint starts the first turn as soon as the message arrives: the init event shows the MCP server `pending` and none of its tools are offered. | 0 of 7 tools offered with no hold | Claude Code 2.1.197; print mode, stream-json input; Anthropic endpoint | ●●● | ✓ |
| method | A 10 s hold gives a connected MCP start with its tools (2.1.197) | On Claude Code 2.1.197, holding the first message 10 s after starting the CLI gives an init event with the MCP server `connected` and its 7 tools offered. | 7 of 7 tools after 10 s | Claude Code 2.1.197; print mode, stream-json input | ●●● | ✓ |
| behaviour | Claude Code 2.1.280 has the MCP server connected at the first turn | On Claude Code 2.1.280 the init event showed the MCP server `connected` (source "dynamic") with its 7 tools at the first turn with no hold, in 3 of 3 starts. | 3 of 3 starts connected | Claude Code 2.1.280; print mode, stream-json input | ●●● | ✓ |

## Detail

### A headless first turn starts before its MCP server connects (2.1.197) · `load-bearing` · gotcha
**In print mode with stream-json input, Claude Code 2.1.197 on Anthropic's endpoint starts the first turn as soon as the message arrives: the init event shows the MCP server `pending` and none of its tools are offered.**
Measured with a local MCP server (atlas mcp) in a Docker sandbox, plan route, claude-haiku-5-5. Against a non-Anthropic base URL (a closed port, or Ollama) the server was connected at the start on 2026-10-13.
- **Applies to:** Claude Code 2.1.197; print mode, stream-json input; Anthropic endpoint · **Metric:** 0 of 7 tools offered with no hold · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Hold the first message (10 s in the studio harness) and check `mcp_servers` in the init event before relying on an MCP tool in the first turn.
- **Verify:** verdict=confirmed | via live re-probe 2026-10-20 (b1-pin-0.jsonl), and the 2026-10-14 capture plan-haiku-start.jsonl, 2026-10-20
- **Sources:** [rnd: Claude Code starts a print-mode turn before its MCP servers connect](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-claude-code-starts-a-turn-before-mcp-servers-connect.md) — SUPPORTED

### A 10 s hold gives a connected MCP start with its tools (2.1.197) · `supporting` · method
**On Claude Code 2.1.197, holding the first message 10 s after starting the CLI gives an init event with the MCP server `connected` and its 7 tools offered.**
The 2026-10-13 probe found 3 s enough; the studio harness uses 10 s.
- **Applies to:** Claude Code 2.1.197; print mode, stream-json input · **Metric:** 7 of 7 tools after 10 s · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Build the hold into any headless kickoff that needs an MCP tool at once.
- **Verify:** verdict=confirmed | via live re-probe 2026-10-20 (b1-pin-10.jsonl), 2026-10-20
- **Sources:** [rnd: Claude Code starts a print-mode turn before its MCP servers connect](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-claude-code-starts-a-turn-before-mcp-servers-connect.md) — SUPPORTED

### Claude Code 2.1.280 has the MCP server connected at the first turn · `supporting` · behaviour
**On Claude Code 2.1.280 the init event showed the MCP server `connected` (source "dynamic") with its 7 tools at the first turn with no hold, in 3 of 3 starts.**
A 2026-10-13 note reported 2.1.280 as pending too; it did not reproduce in three starts on 2026-10-20, and the rnd entry marks that report disputed.
- **Applies to:** Claude Code 2.1.280; print mode, stream-json input · **Metric:** 3 of 3 starts connected · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Still check `mcp_servers` in the init event; don't depend on the version alone.
- **Verify:** verdict=confirmed | via live re-probe 2026-10-20 (b1-cur-0.jsonl, b1rep-cur-0-1/2.jsonl), 2026-10-20
- **Sources:** [rnd: Claude Code starts a print-mode turn before its MCP servers connect](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-claude-code-starts-a-turn-before-mcp-servers-connect.md) — SUPPORTED

