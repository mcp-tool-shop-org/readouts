# Agent tracing
_Tracing agent runs (NeMo Relay): what is recorded locally, what leaves the machine, privacy of traces_ · wave 1 · 2026-10-20 · [‹ catalog index](README.md)

4 findings · 1 load-bearing · 4 verified.

| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |
|------|---------|-------|--------|------------|------|---|
| gotcha | Relay's local ATOF file carries the account's identity | NeMo Relay's local ATOF event file contained the signed-in account's email address, with `enable_full_payloads = false`. |  | NeMo Relay 0.10.1 | ●●● | ✓ |
| policy | NeMo Relay and its plugins are Apache-2.0 | NVIDIA/NeMo-Relay and NVIDIA/NeMo-Relay-Plugins are licensed Apache-2.0. |  | NeMo Relay repositories | ●●● | ✓ |
| behaviour | NeMo Relay writes ATOF and ATIF traces of a Claude Code run locally | NeMo Relay 0.10.1's transparent `nemo-relay claude` wraps Claude Code and, with its observability plugin, writes ATOF events and an ATIF trajectory to local files with OpenTelemetry off. |  | NeMo Relay 0.10.1; Claude Code 2.1.197 | ●●● | ✓ |
| behaviour | One Relay run contacted only Anthropic's hosts | Under sbx's Balanced policy, the before-and-after policy log of one Relay run showed no host other than Anthropic's (api.anthropic.com, mcp-proxy.anthropic.com, platform.claude.com). | 1 run | NeMo Relay 0.10.1; sbx Balanced | ●●● | ✓ |

## Detail

### Relay's local ATOF file carries the account's identity · `load-bearing` · gotcha
**NeMo Relay's local ATOF event file contained the signed-in account's email address, with `enable_full_payloads = false`.**
Found by the identity scan of the re-run's output; the value is not recorded anywhere public.
- **Applies to:** NeMo Relay 0.10.1 · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Treat Relay trace files as private: never commit or publish them without redaction.
- **Verify:** verdict=confirmed | via identity scan of the 2026-10-20 re-run's ATOF file, 2026-10-20
- **Sources:** [rnd: NeMo Relay's first trial](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-nemo-relay-first-trial-in-the-sandbox.md) — SUPPORTED

### NeMo Relay and its plugins are Apache-2.0 · `supporting` · policy
**NVIDIA/NeMo-Relay and NVIDIA/NeMo-Relay-Plugins are licensed Apache-2.0.**
Read from the GitHub API.
- **Applies to:** NeMo Relay repositories · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Licence-compatible with studio tooling.
- **Verify:** verdict=confirmed | via GitHub API, 2026-10-20, 2026-10-20
- **Sources:** [NVIDIA/NeMo-Relay](https://github.com/NVIDIA/NeMo-Relay) — SUPPORTED ; [rnd: NVIDIA NeMo Relay](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-nvidia-nemo-relay-tracing-agent-harnesses-claude-code-includ.md) — SUPPORTED

### NeMo Relay writes ATOF and ATIF traces of a Claude Code run locally · `supporting` · behaviour
**NeMo Relay 0.10.1's transparent `nemo-relay claude` wraps Claude Code and, with its observability plugin, writes ATOF events and an ATIF trajectory to local files with OpenTelemetry off.**
One run on 2026-10-20 (13 ATOF events, one trajectory) and the 2026-10-13 trial.
- **Applies to:** NeMo Relay 0.10.1; Claude Code 2.1.197 · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Relay can trace studio harness runs without a collector.
- **Verify:** verdict=confirmed | via live re-run 2026-10-20 (b4-start.txt, the trace files listed in the sandbox), 2026-10-20
- **Sources:** [rnd: NeMo Relay's first trial](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-nemo-relay-first-trial-in-the-sandbox.md) — SUPPORTED ; [NeMo Relay: Claude Code](https://docs.nvidia.com/nemo/relay/latest/nemo-relay-cli/claude-code) — SUPPORTED

### One Relay run contacted only Anthropic's hosts · `watch` · behaviour
**Under sbx's Balanced policy, the before-and-after policy log of one Relay run showed no host other than Anthropic's (api.anthropic.com, mcp-proxy.anthropic.com, platform.claude.com).**
An observation of what the run did, not a restriction: Balanced allows other AI-service hosts.
- **Applies to:** NeMo Relay 0.10.1; sbx Balanced · **Metric:** 1 run · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** No NVIDIA telemetry was seen; re-check after any Relay upgrade.
- **Verify:** verdict=confirmed | via live re-run 2026-10-20 (b4-policylog-before/after.json), 2026-10-20
- **Sources:** [rnd: NeMo Relay's first trial](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-nemo-relay-first-trial-in-the-sandbox.md) — SUPPORTED

