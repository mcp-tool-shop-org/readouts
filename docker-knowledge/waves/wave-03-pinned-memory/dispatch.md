# Wave 3 — Pinned-memory re-check: the WSL2 cudaHostAlloc ceiling across driver versions

**Study-swarm wave 3** · dispatched 2026-06-04 · 1 lane (hw-measurement) · run `wf_280fb07f-a91` (26 agents). **22 raw findings → 8 consolidated · 20 citations · 0 fabricated · 0 refuted.** Verifier receipt: [verification.md](verification.md).

## Why this wave
The Milestone-1 profiler (gpu-container) measured the pinnable host-RAM ceiling INSIDE a Docker-on-WSL2 container and an escalating `cudaHostAlloc` probe succeeded to **≥22.5 GiB** on **NVIDIA driver 610.47** (RTX 5090, ~31 GiB WSL2 VM) — with no failure, safety-capped at 75% of VM RAM. That is **~45× the wave-2 finding** "WSL2 collapses pinnable to ~300–500 MB" and **exceeds** the Windows-native ~50%-of-RAM rule. This wave asks: is that lift real, documented, and version-bounded — so the KB can be reconciled rather than left self-contradicting?

## What we found (the answer is more interesting than "a driver lifted it")

1. **NVIDIA still documents the limit — but never as a number.** The CUDA-on-WSL User Guide STILL lists "pinned system memory … availability for applications is limited" as a Known Limitation in **v13.3 (2026-05-21)**, verbatim-unchanged since **v12.0 (2022)**. NVIDIA never attached a figure. *(NVIDIA, [CUDA-on-WSL v13.3](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) + [v12.0 archive](https://docs.nvidia.com/cuda/archive/12.0.0/wsl-user-guide/index.html).)* → the KB's 300–500 MB was always community-observed, never a vendor spec.

2. **The limit is Windows/WDDM-managed, not an NVIDIA driver cap.** NVIDIA staff: "the limit is entirely managed by Windows … the NVIDIA driver doesn't control or set the limit," and (2023) max pinned "depends on internal details of the operating system, not CUDA." So **no NVIDIA driver-version boundary exists** to cite for a "fix." *(NVIDIA forums, [255472](https://forums.developer.nvidia.com/t/what-are-the-pinned-memory-limitations-on-cuda-for-wsl2/255472), [228235](https://forums.developer.nvidia.com/t/change-limit-of-50-for-cudahostalloc-pinned-memory-on-windows-10-11/228235).)*

3. **The ~300–500 MB cap is a CONTAINER artifact, not an inherent WSL2 ceiling.** In microsoft/WSL **#14078**, native Windows pinned ~4000 MB single / ~5600 MB total on the **same rig** where the Docker container was held to ~500 MB; bare WSL2 pins small buffers fine. The gate is the container's **RLIMIT_MEMLOCK** + extra **WSL2→WDDM paravirtualization (GPU-PV)** machinery. *(GPU-PV named by NVIDIA; memlock the repeatedly-cited lever.)* → **this is the load-bearing mechanism.**

4. **The harsh cap still reproduced as of Jan 2026 (driver 572.83) inside Docker** — issue #14078, closed 2026-01-27 as a stale/no-activity auto-close, NOT via a documented fix. So it is **version/config-bound, not universally abolished**; the rig's 610.47 result is a config/version delta, not proof the cap is gone everywhere.

5. **Nearest documented capability boundary: CUDA 13.2 / driver R595 (2026-03).** NVIDIA officially added "Native (and WSL) containers are supported" + `cuMemCreate`/`cudaMallocAsync` (VMM/async allocators) for WSL/MCDM. The rig's 610.47 **post-dates R595**, consistent with running the improved WSL-container path — **but the note names container + VMM support, NOT the legacy `cudaHostAlloc` API.** *(NVIDIA, [CUDA 13.2 blog](https://developer.nvidia.com/blog/cuda-13-2-introduces-enhanced-cuda-tile-support-and-new-python-features/).)*

6. **The effective ceiling tracks the WSL2 VM's assigned RAM (`.wslconfig memory=`).** Consistent with the native ~50%-of-RAM behavior scaling with present RAM. This rig's **≥72% of VM RAM** exceeds the 50% rule — consistent with the container layer being the only real gate once memlock is unconstrained.

## Reconciliation applied to the KB (this wave)
- `wsl2-collapses-…-300-mb`: **load-bearing → watch** + superseded note (held only for ≤572.83 / constrained containers; MEASURE per-rig).
- `wsl2-pinned-memory-cap` (~50%, lower under WSL2): **kept** + nuance (mechanism reaffirmed; "lower" is a container gate; this rig exceeded 50%).
- `native-windows-pins-50%…`: **kept** + nuance (this rig exceeded 50%; ceiling tracks VM RAM).
- `cuda-on-wsl-guide-…-limited`: **kept + REAFFIRMED** (wording persists in v13.3, still numberless).

## Method, confidence, next
- 3-lens, reasoning-stripped: WebFetch retrieval oracle (existence + attribution + groundedness) + `mistral-small:24b` + `granite4.1:30b`. 0 fabricated, 0 refuted. See [verification.md](verification.md).
- **The product thesis, doubly vindicated:** the documented limit is qualitative, the famous number is a container-config artifact, and the true ceiling is a function of (container memlock × VM RAM × driver × Docker version). It is therefore **not a documentable constant — it must be probed per-rig**, which the Milestone-1 profiler now does.
- NEXT: none required for Phase 1 — the warm-tier pinned staging budget on this rig is **ample (≥22.5 GiB), not the feared few-hundred MB**. If gpu-container ever runs on an older stack (≤572.83 / constrained memlock), the probe will catch the low ceiling and the receipt will explain it via the `.wslconfig`/memlock context.
