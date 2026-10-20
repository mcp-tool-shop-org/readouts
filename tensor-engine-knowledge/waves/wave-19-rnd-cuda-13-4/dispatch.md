# Wave 19 — promoted from rnd: CUDA 13.4's developer-experience changes, re-sourced from NVIDIA

**Promotion wave** · 2026-10-20 · **not a research swarm.** This wave promotes the rnd entry
[`2026-10-07-cuda-13-4-developer-experience`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-07-cuda-13-4-developer-experience.md).
The Director approved the promotion on 2026-10-20.

## Why it was re-sourced

The rnd entry's claims rested on a slide from NVIDIA's CUDA 13.4 livestream. A slide previews a release; it isn't the
release. So every row here is taken from NVIDIA's own CUDA Toolkit 13.4 release notes or its nvcc 13.4 documentation.
A slide item that neither source states isn't loaded.

## What it adds (4 rows in `sources`, lane runtime-foundations)

| Row | Source |
|---|---|
| Memory-pool IPC works on Windows WDDM for stream-ordered allocations | release notes, New Features, CUDA Platform |
| The driver isn't bundled with the toolkit: on Windows since 13.1, on Linux since 13.4 | release notes, 2.2 CUDA Driver |
| cuda-checkpoint can write checkpoint state to persistent storage | release notes, New Features, CUDA Platform |
| nvcc documents `--fmax-errors=<n>` and `--Wconversion`, a narrowing-conversion warning | nvcc 13.4 documentation, 4.2.8.7 and 4.2.8.11 |

**The one that touches the rig is WDDM memory-pool IPC.** The RTX 5090 runs under WDDM. Two rig processes could share
pool-allocated GPU buffers without a host round trip, which used to be Linux-only. It hasn't been tested on the rig.

## Not loaded: slide-only items

Neither NVIDIA source states these, so they aren't loaded:
- that `-fmax-errors` is new in 13.4 and now applies to device code;
- `-fno-signed-zeros` and `-ffinite-math-only`;
- UTF-8 source files;
- nvdisasm source lines in JSON;
- libNVVM PTX-version selection;
- event creation no longer waiting behind pageable copies;
- GPUDirect Storage RAID1/RAID10;
- the driver's components (Fabric Manager, IMEX, nvidia-fs) named as posted separately. The release notes say only
  that the driver isn't bundled.

They stay in rnd as slide-sourced claims.

## Method

The R&D seat read the archived 13.4 GA release notes (versioned 13.4.1, which supersedes the 13.4.0 developer preview)
and the nvcc 13.4 documentation on 2026-10-20. See [verification.md](verification.md).
