# Wave 1 — promoted from rnd: Claude Code, permissions, Docker Sandboxes and NeMo Relay, re-probed live

**KB** `agent-tooling-knowledge` (new) · **dispatched** 2026-10-20 · **0** research agents (a promotion) · trigger: the
readouts promotion queue had two Claude Code notes with no knowledge base to go to. The Director ruled that this KB be
made for them, and that it be public.

**The bar for loading.** The Director ruled that wave 1 waits for live re-probes. Every finding here was re-checked on
2026-10-20, and an unverified claim doesn't load. So the wave is smaller than the rnd entries it comes from.

## Research grounding

1. **A Read deny rule doesn't contain a recursive Grep** (Claude Code 2.1.197).
   - **Above the tree:** a Grep rooted above a denied tree lists the files inside it, with both `Read(~/**)` and
     `Read(//X/**)`.
   - **At the root:** with `Read(~/**)`, a Grep at `~` itself leaks too. With `Read(//X/**)`, a Grep at `X` is refused.
   - **2.1.280:** with the `//` form, a Grep above returns no denied files.
   - **The docs:** Claude Code's permissions page calls Read rules on search tools "best-effort", so this is documented
     behaviour.
   - **Implication:** contain agents at OS level. Use deny rules only as a second layer, and write absolute paths with
     `//`. A one-slash path anchors at the settings source, and in the probe it denied nothing.
2. **The first headless turn can start before an MCP server connects** (2.1.197).
   - With no hold, the server was `pending` and offered none of its tools. After a 10 s hold, it was `connected`.
   - 2.1.280 was `connected` with no hold in 3 of 3 starts.
   - **Implication:** hold the first message, and check `mcp_servers` in the init event, on any version.
3. **Docker Sandboxes keep the plan's token on the host.**
   - The sandbox holds placeholder tokens only, and every start reports `apiKeySource: none`.
   - A sandbox reaches the host's 127.0.0.1 Ollama through `host.docker.internal`.
   - **Two operational gotchas:**
     - a sandbox-scoped deny `**` overrides every allow, so it can't anchor an allowlist;
     - on the rig, sbx must be run from a C: working directory.
4. **NeMo Relay traces locally, but its traces carry identity.**
   - Relay 0.10.1 wrote ATOF and ATIF files with OpenTelemetry off. One run contacted only Anthropic's hosts.
   - Its ATOF file held the signed-in account's email, even with full payloads off.
   - **Implication:** treat trace files as private.

## What the re-probe changed

- **The deny-rule finding.** The rnd entry was corrected twice on 2026-10-20: first narrowed to "the root itself", then
  restored to "at or above", with the rule form stated. The live probe showed each earlier reading held for one rule
  form.
- **MCP on 2.1.280.** The entry's report that 2.1.280 was also `pending` didn't reproduce. It's marked disputed in rnd
  and isn't loaded here.
- **Left in rnd, unverified or not re-probed:**
  - Relay's cost overhead (n = 1);
  - Hermes integration (its docs page is gone);
  - the sandbox image's shipped CLI version (disputed);
  - the setup claims that weren't re-checked.

## The honest limit

- One rig, two CLI versions, and small counts: 1 to 3 starts per cell.
- The `~` rule form wasn't tested on 2.1.280.
- Relay's "only Anthropic's hosts" is one run under a policy that would have allowed other AI-service hosts. It's an
  observation, not a guarantee.

## Provenance

Promoted from five rnd entries (agent-tooling field). They were re-probed in the `atlas-pilot` Docker sandbox on
2026-10-20, in two planned jobs the Publisher approved: Job A, read-only, and Job B, the re-probes. See
[verification.md](verification.md).
