# Wave 21 — verification

**Dispatch:** [`dispatch.md`](dispatch.md)

**Runner:** a Sonnet subagent made the first pass on 2026-10-20. The R&D seat then re-read the load-bearing sources
itself:
- PAIR's architecture.mdx at v1.0.0, lines 172–185, 312–327, 404–423 and the port table;
- the v1.0.0 release notes;
- SECURITY.md lines 87–89;
- the licence through the GitHub API.

**Verifier maturity, stated plainly:** retrieval against NVIDIA's own pages only. No second model family. These are
vendor statements, not rig measurements.

## Result

| row | verdict | checked against |
|---|---|---|
| PAIR 1.0.0 overview | confirmed | release v1.0.0, published 2026-10-13T12:08Z (What's New, Compatibility Notes); architecture.mdx port table and the proxy paragraph (Ollama to 11435+, LM Studio to 1235+); licence Apache-2.0 (GitHub API) |
| PAIR's scheduler | confirmed | architecture.mdx lines 312–327 (pending plus pressure, 0–3 units at 40/70/85%, stale telemetry neutral at 1) and 404–423 (no VRAM, latency or GPU model; every workload counts as one; load state not considered) |
| PAIR's telemetry | corrected from the bench | architecture.mdx lines 172–185 (telemetry plaintext, not authenticated, readable on the subnet); SECURITY.md lines 87–89. The bench's unverified "no telemetry beyond paired nodes" is contradicted for the subnet. |
| CUDA Tile C++ | confirmed | CUDA Programming Guide v13.4.2, Writing Tile Kernels: introduction ("from version 13.3 onward"), section 2.4.3 (powers of two; compile-time shape and type) and 2.4.5 |

## Reasons for leaving claims out, checked

- **PDL for tile kernels in 13.4:** the subagent searched the tile guide, the PDL page (4.5) and the 13.4 Update 2
  release notes' CUDA Tile and Tile IR sections, and found none that state it. The bench's only source is a social-media
  post. It stays unverified.
- **Anthropic Messages via Ollama and LM Studio:** this is a community contribution listed in the release. I didn't
  re-read it at the source, so it isn't loaded.

**Net:** 4 rows, 3 confirmed and 1 corrected from the bench; 0 fabricated.
