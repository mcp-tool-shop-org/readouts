# Agent sandboxes
_Docker Sandboxes (sbx): setup, credentials, network policy, reaching host services, operational gotchas_ · wave 1 · 2026-10-20 · [‹ catalog index](README.md)

4 findings · 0 load-bearing · 4 verified.

| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |
|------|---------|-------|--------|------------|------|---|
| behaviour | A local sandbox reaches the host's 127.0.0.1 Ollama at host.docker.internal | An sbx sandbox with a rule for `localhost:11434` reaches an Ollama on the host that listens on 127.0.0.1 only, at `host.docker.internal:11434`. |  | sbx 0.48.0; Ollama 0.40.4 | ●●● | ✓ |
| gotcha | A sandbox-scoped deny `**` overrides every allow, even a sandbox-scoped one | In sbx, adding a sandbox-scoped deny rule for `**` makes `sbx policy check` deny every host, including one with its own sandbox-scoped allow rule, so an allowlist can't be built as deny-all plus allows. |  | sbx 0.48.0 | ●●● | ✓ |
| gotcha | Run sbx from a C: working directory on the rig | On the rig, an sbx daemon launched from a shell whose working directory was on E: could not start sandboxes ("failed to connect to console socket: dial unix vm\console.sock"); relaunched from %USERPROFILE% it started them first time. |  | sbx 0.48.0 on Windows, state on C: | ●●● | ✓ |
| behaviour | The claude kit's real OAuth token stays on the host | In a Docker Sandboxes (sbx) claude-kit sandbox signed in on a Claude plan, the sandbox's credentials file holds only placeholder tokens and every start reports `apiKeySource: none`; the real token is injected outside it. | 13 of 13 starts apiKeySource none | sbx 0.48.0, claude kit | ●●● | ✓ |

## Detail

### A local sandbox reaches the host's 127.0.0.1 Ollama at host.docker.internal · `supporting` · behaviour
**An sbx sandbox with a rule for `localhost:11434` reaches an Ollama on the host that listens on 127.0.0.1 only, at `host.docker.internal:11434`.**
Ollama 0.40.4 with OLLAMA_HOST unset answered /api/version from the sandbox. The egress filter names the target localhost:11434.
- **Applies to:** sbx 0.48.0; Ollama 0.40.4 · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Local-model agents can run inside a sandbox without exposing Ollama on the LAN.
- **Verify:** verdict=confirmed | via live check 2026-10-20 (b3-ollama-binding.txt), 2026-10-20
- **Sources:** [rnd: Docker Sandboxes on the rig](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-docker-sandboxes-on-the-rig-from-signup-to-a-pinned-pilot-wo.md) — SUPPORTED

### A sandbox-scoped deny `**` overrides every allow, even a sandbox-scoped one · `supporting` · gotcha
**In sbx, adding a sandbox-scoped deny rule for `**` makes `sbx policy check` deny every host, including one with its own sandbox-scoped allow rule, so an allowlist can't be built as deny-all plus allows.**
Measured with api.anthropic.com:443 allowed and `**` denied: both it and github.com came back Denied. The Balanced default already denies hosts outside its lists.
- **Applies to:** sbx 0.48.0 · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** To tighten a sandbox, start from Balanced and deny specific groups; verify with `sbx policy check`.
- **Verify:** verdict=confirmed | via live check with `sbx policy check` 2026-10-20 (test rules removed after), 2026-10-20
- **Sources:** [sbx CLI reference (and `sbx policy deny network --help`, sbx 0.48.0)](https://docs.docker.com/reference/cli/sbx/) — SUPPORTED

### Run sbx from a C: working directory on the rig · `supporting` · gotcha
**On the rig, an sbx daemon launched from a shell whose working directory was on E: could not start sandboxes ("failed to connect to console socket: dial unix vm\console.sock"); relaunched from %USERPROFILE% it started them first time.**
The shim listens at a relative socket path; the sandbox state is on C:. Fixed by the Publisher, confirmed by R&D's start.
- **Applies to:** sbx 0.48.0 on Windows, state on C: · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Run every sbx command from a C: working directory.
- **Verify:** verdict=confirmed | via two starts 2026-10-20 (16:56Z failed from E:, 17:00Z succeeded from C:); the daemon log, 2026-10-20
- **Sources:** [rnd: Docker Sandboxes on the rig](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-docker-sandboxes-on-the-rig-from-signup-to-a-pinned-pilot-wo.md) — SUPPORTED

### The claude kit's real OAuth token stays on the host · `supporting` · behaviour
**In a Docker Sandboxes (sbx) claude-kit sandbox signed in on a Claude plan, the sandbox's credentials file holds only placeholder tokens and every start reports `apiKeySource: none`; the real token is injected outside it.**
Checked by shape only (two 26-character placeholder tokens); no value was read out. 13 plan-route starts all reported apiKeySource none.
- **Applies to:** sbx 0.48.0, claude kit · **Metric:** 13 of 13 starts apiKeySource none · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** A plan-route agent in a sandbox can't exfiltrate the real token from its own filesystem.
- **Verify:** verdict=confirmed | via live check 2026-10-20 (b3-credentials.txt and the init events of the Job B starts), 2026-10-20
- **Sources:** [rnd: Docker Sandboxes on the rig](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-docker-sandboxes-on-the-rig-from-signup-to-a-pinned-pilot-wo.md) — SUPPORTED

