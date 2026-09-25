# Wave 2 — Measurement: reading the rig truthfully from inside a WSL2 GPU container

**Study-swarm wave 2** · dispatched 2026-06-04 · 4 lanes · 11 agents · run `wf_f5d21e00-080`. **28 findings (20 hw-measurement + 8 container-runtime), 41 citations, 0 fabricated.** This fills the empty `hw-measurement` lane and is the SPEC for the gpu-container profiler's `measure_bandwidth()` + platform detection. Verifier receipt: [verification.md](verification.md).

## Why this wave
The Milestone-1 profiler reads the rig but leaves PCIe/NVMe bandwidth + the pinnable-RAM ceiling as honest `None` stubs. This wave is HOW to fill them correctly — and where measuring from inside a container / under WSL2 changes the answer. Engines are out of scope (the `tensor-engine-knowledge` KB owns those).

## PCIe — measure, don't trust the spec sheet
- Measure H2D and D2H SEPARATELY with PINNED (page-locked) buffers, large transfers (>=64-256 MB), warmup + median-of-N, timed by cudaEvent. Pinned is >2x pageable (pageable stages through a driver bounce buffer). Canonical tool: `bandwidthTest`, superseded by **NVIDIA/nvbandwidth**.
- PCIe 5.0 x16 theoretical is **~64 GB/s PER DIRECTION** (~128 GB/s aggregate) — NOT "64 bidirectional". Realistic pinned achieved ~50-55 GB/s/dir. The profiler must NEVER emit 64 as a measured value.
- WSL2/WDDM: pinned-alloc cap is lower than native; `nvidia-smi pcie.link.gen/width` often return N/A in the VM → DERIVE the link truth by MEASURING throughput; keep `pcie.link.*` advisory-only.

## NVMe — sequential AND random-QD1, on the path that matters
- fio: sequential `--rw=read --bs=256k`; random `--rw=randread --bs=4k --iodepth=1` (QD1 is the realistic metric; headline sequential >> random-QD1). `--direct=1` to bypass the page cache.
- CONTAINER: benchmark the ACTUAL path the weights live on. Docker overlay union-fs is slower than a bind-mounted volume (which writes straight to the host fs), and `--direct=1` can FAIL on overlay ("does not support O_DIRECT"). WSL2: `/mnt/c` drvfs is >10x slower than native ext4 — measure the ext4 vdisk where shards actually sit.

## VRAM + pinnable RAM — the WSL2 ceiling is load-bearing
- VRAM free/total via NVML (`nvmlDeviceGetMemoryInfo`); probe fragmentation via a largest-contiguous-allocation test. `pynvml` binds NVML directly (faster than parsing nvidia-smi).
- PINNABLE host RAM is the key WSL2 limit: `cudaHostAlloc` starts failing ~300 MB and PyTorch `pin_memory()` ~500 MB inside Docker-on-WSL2, versus multiple GB native. MEASURE the ceiling by probing — do not assume — because it caps the warm-tier KV/prefetch staging budget.
- NVML in-container reporting has quirks (per-process memory N/A under WSL2) — treat per-process fields as advisory.

## Container-runtime — what a measuring profiler must get right
- The NVIDIA Container Toolkit injects `/dev/nvidia*` + host driver libs via a runC prestart hook on `--gpus all`. Base image: `:runtime` ships the CUDA libs to RUN; `:devel` adds `nvcc` to BUILD (needed only if compiling a cudaMemcpy bench — otherwise ship `nvbandwidth` / a prebuilt). sm_120 needs a CUDA build that targets it, or compute throws "device kernel image is invalid".
- Detect container via `/.dockerenv` + a docker token in `/proc/1/cgroup`; detect WSL2 via "microsoft" in `/proc/version`. GOTCHA: a container ON the WSL2 backend inherits "microsoft" too — so "microsoft" means "WSL2 kernel" regardless of container; combine with `/.dockerenv` to distinguish. WSL 2.7.0 fixed the consumer-Blackwell (5090) CUDA-graph hang.

## Method, confidence, next
- 41/41 citations resolved, 0 fabricated; family-different verified (oracle + mistral + granite). See [verification.md](verification.md).
- NEXT (a gpu-container code milestone): implement `measure_bandwidth()` against these methods — pinned cudaMemcpy/nvbandwidth for PCIe, fio QD1+seq on the right mount for NVMe, a cudaHostAlloc probe for the pinnable ceiling — run INSIDE the container, and write the results back into this KB's `measurements`/`baselines`.
