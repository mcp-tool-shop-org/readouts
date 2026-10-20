# Wave 19 — promoted from rnd: nemotron-3.5-lightning needs its context raised under Claude Code

**KB** `model-knowledge` · **dispatched** 2026-10-20 · **0** research agents (a promotion) · lane `llm` · trigger: the
readouts promotion queue. The Director approved the promotion on 2026-10-20, with n stated.

**Headline:**
- A local model behind Claude Code needs its context window raised past the CLI's own overhead before its answers mean
  anything.
- Claude Code's system prompt and tools take about 25,000 to 28,000 tokens of Ollama's default 32,768.
- nemotron-3.5-lightning in a derived model with `num_ctx 131072` answered 11 of 12 on a small code-reading task set.

## What it adds (3 rows in `sources`, lane llm)

| Row | Status |
|---|---|
| The 131k derived model: 4/4 on RC03; 11/12 on four tasks; later rounds 9/12 (11 answered) and 9/12 (10 answered) | verified against the run records |
| The default 32k context: 1/4 on RC03 | a halted shakedown, not a result |
| Fully resident on the RTX 5090, peak near 28 GB (27,862 MiB; 27,986 MiB at a 65,538-token prompt) | unverified: raw records not kept |

**Make the derived model:** a Modelfile with `FROM nemotron-3.5-lightning:latest` and `PARAMETER num_ctx 131072`,
then `ollama create`.

**Check what loaded:** Ollama's `/api/ps` reports `context_length` per loaded model.

## The honest limit

- A four-task code-reading set from a withdrawn experiment's shakedowns, one CLI version (2.1.197) and one model.
- It isn't a benchmark or a ranking.
- The fill-check figures are as reported on 2026-10-13. Their log wasn't kept.

## Provenance

Promoted from rnd entry
[`2026-10-13-nemotron-lightning-needs-its-context-set-for-claude-code`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-nemotron-lightning-needs-its-context-set-for-claude-code.md).
The run records were recovered read-only from the stopped `atlas-pilot` sandbox on 2026-10-20, under a planned job the
Publisher approved. See [`verification.md`](verification.md).
