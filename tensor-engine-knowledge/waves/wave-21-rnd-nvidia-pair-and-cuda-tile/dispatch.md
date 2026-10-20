# Wave 21 — promoted from rnd: NVIDIA PAIR, a LAN inference router, and CUDA Tile C++

**Promotion wave** · 2026-10-20 · **not a research swarm.** This wave promotes two rnd entries:
- [`2026-10-13-nvidia-pair-a-lan-inference-router-and-how-it-compares-with-`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-13-nvidia-pair-a-lan-inference-router-and-how-it-compares-with-.md)
- [`2026-10-07-cuda-tile-programming`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-07-cuda-tile-programming.md)

The R&D seat chose them from the 2026-10-20 promotion queue.

## What it adds (4 rows in `sources`)

| Row | Lane | Source |
|---|---|---|
| PAIR 1.0.0: a LAN router in front of Ollama (11434 → 11435+), LM Studio (1234 → 1235+) and llama.cpp; Apache-2.0; launch options such as context size; CORS now per engine | llm-serving | PAIR v1.0.0 release notes and architecture.mdx |
| PAIR's scheduler: pending jobs plus coarse GPU pressure; VRAM, latency and loaded models aren't inputs | llm-serving | architecture.mdx lines 312–327 and 404–423 |
| PAIR's node telemetry is plaintext and readable by anything on the subnet; "local-first" doesn't prove nothing leaves the LAN | llm-serving | architecture.mdx lines 172–185; SECURITY.md lines 87–89 |
| CUDA Tile C++ is in the toolkit from 13.3; tile dimensions are powers of two, fixed at compile time | runtime-foundations | CUDA Programming Guide, Writing Tile Kernels |

**For the rig:** PAIR would route by queue depth, not by which machine is faster or already holds the model. Its
telemetry should stay off networks where hostname and hardware inventory mustn't be readable.

## What the promotion changed

- **Corrected:** the bench's "[unverified] no telemetry beyond paired nodes" is replaced by NVIDIA's own statement:
  telemetry is plaintext and readable on the subnet.
- **Not loaded:**
  - CUDA Tile's "13.4 adds programmatic dependent launch for tile kernels": the tile guide, the PDL page and the 13.4
    release notes' Tile sections don't state it, so it stays unverified on the bench;
  - PAIR's community-contributed Anthropic Messages support, which wasn't read at the source.

## The honest limit

- All four rows are NVIDIA's own documentation, not measured on the rig. PAIR hasn't been installed here.

## Method

The R&D seat read PAIR's repository at tag v1.0.0 (the architecture document, SECURITY.md, the release notes and the
licence) and NVIDIA's CUDA Programming Guide (v13.4.2) on 2026-10-20, after a Sonnet subagent's first pass. See
[verification.md](verification.md).
