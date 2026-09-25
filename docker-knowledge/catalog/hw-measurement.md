# Hardware measurement methodology
_How to measure VRAM / PCIe / NVMe (seq + rand QD1) / pinnable-RAM truthfully — especially from inside a WSL2 GPU container_ · wave 9 · 2026-09-07 · [‹ catalog index](README.md)

57 findings · 23 load-bearing · 31 verified.

| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |
|------|---------|-------|--------|------------|------|---|
| craft | A Method for Layer Bit-Width Allocation in LLM Quantization via Performance Maximization Under a Quality-Degradation Constraint | Explicitly names **RTX 5090 (Blackwell, sm_120)** and notes kernel-selection differs from Ampere sm_86 — consumer sm_120 is the named compute target for 5090-class claims. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | Blackwell Compatibility Guide | Toolkit **12.8** `nvcc` emits native **compute_100 / sm_100** cubin (+ PTX). Apps need PTX or sm_100 cubin for Blackwell. Page focuses **CC 10.0**; does not name 5090 or quote measured bandwidth. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | Blackwell Tuning Guide | Documents **CC 10.0 and 12.0** (warps/SM, shared-mem caps differ). B200 as CC 10.0 example. Establishes **10.0 ≠ 12.0** on the same architecture family — relevant vs catalog sm_100 vs sm_120 distinction. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| docs | CUDA 12.8 Blackwell compatibility — sm_100 | Toolkit 12.8 emits native sm_100/compute_100; PTX forward-compat. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | CUDA C++ Best Practices | Pinned via `cudaHostAlloc`; cites **~12 GB/s on PCIe x16 Gen3** as illustrative; points to `bandwidthTest` sample. Timing via `cudaEventElapsedTime`. Gen3 example only — **not** a 5090/Gen5 measurement. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | CUDA C++ Best Practices | Analog: theoretical link rate ≠ effective measured bandwidth; pinned Host↔Device must be timed. Holds for PCIe honesty vs SKU “Gen5 x16” marketing. Limit: guide cites Gen3-class examples. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | CUDA Demo Suite | Measures D2D / H2D / D2H for **pageable** and **pinned**; knobs `--memory=pinned/pageable`, `--mode=quick/range/shmoo`, `--htod`/`--dtoh`/`--dtod`, `--device`, `--wc`. **No default transfer size or GB/s figures on this page.** |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | CUDA on WSL User Guide 13.3 | Known limits: **pinned system memory availability limited** (no numeric cap); unified/managed memory unsupported; **NVML**: utilization + active compute process queries unsupported; ECC/compute/persistence mode not modifiable. Measure free/total-style queries separately from util. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | Characterizing Warp Divergence from Pascal to Blackwell | Labels Blackwell **server sm_110** vs **consumer sm_120** (RTX 5080); static SASS spans sm_80–sm_120 including sm_100/110/120 — consumer vs server compute-cap are distinct labels. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | Darzi — host-side eBPF + NVML/NCCL | eBPF host signals correlated with NVML + NCCL for GPU tail latency RCA. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | ESS: An Offload-Centric Latent-Cache Management Architecture for DeepSeek-V3.2-Exp | PCIe 5.0 unidirectional theoretical ceiling does not equal effective cudaMemcpyAsync under fine-grained non-contiguous pages — measurement honesty: theoretical Gen5 ≠ fragmented effective BW. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | Evaluating CUDA Tile for AI Workloads on Hopper and Blackwell GPUs | Table contrasts H100 NVL **sm_90**, RTX PRO 6000 Blackwell **sm_120**, and B200 **sm_100**; warns workstation sm_120 CuTile/compiler immaturity vs datacenter Blackwell — sm_100 ≠ sm_120 (wave-06/77 deepen). |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | Evaluating CUDA Tile… | Analog: B200 `sm_100` vs RTX PRO 6000 `sm_120` are distinct stacks; cross-arch gaps are real. Holds: **sm_100 ≠ sm_120**. Limit: CuTile paper ≠ container profiler receipt format. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | Gaps vs hw-measurement catalog | On these primary pages: **Absent** product-named RTX 5090 / RTX PRO 6000 measured H2D/D2H GB/s; absent numeric WSL pin ceiling; compatibility guide’s build recipe is sm_100-centric (sm_120 targeting lives mainly in tuning CC 12.0 notes / other CUDA docs). Catalog’s “measure yourself / no invented GB/s” matches the page silence. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | Kernel AIO / O_DIRECT caveats | Async without O_DIRECT quietly becomes sync — headline sequential >> realistic QD1 pattern. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | Microbenchmarking NVIDIA Blackwell B200 | Microbenchmarks B200 (5th-gen tensor cores, TMEM, dual-chip) — image/toolkit must match architecture features. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| docs | NGC TensorFlow 25.01 — CUDA 12.8 / driver ≥570 | Container ships CUDA 12.8.0; driver ≥570; Blackwell-optimized NGC DL containers. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | NVIDIA/nvbandwidth README | / raw README — Successor tool: named cases e.g. `host_to_device_memcpy_ce`, `device_to_host_memcpy_ce`; CE vs SM copies; default buffer **512 MiB**, `--testSamples` median; reports **current measured** GB/s on the system (not a published 5090 floor). |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | NVML Device Queries | `nvmlDeviceGetMemoryInfo` / `_v2`; `nvmlDeviceGetCudaComputeCapability` (major/minor); `nvmlDeviceGetCurrPcieLinkWidth` / Generation; BAR1 memory. Fields for VRAM/PCIe/CC — not bandwidth numbers. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | Non-Uniform L2 Cache Latency Across the Streaming Multiprocessors of an NVIDIA L40 | Same probe on **RTX 5090 (Blackwell GB202)** shows L2-hit latency varies by physical SM; device-specific fingerprints — 5090 microarchitecture measurement ≠ transplanting B200/datacenter numbers. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | OOM-Free Alpamayo via CPU-GPU Memory Swapping for Vision-Language-Action Models | Consumer Blackwell-class PCIe Gen5 path: measures with **pinned** memory and names Gen5 vs Gen3 DMA shifts — catalog PCIe claims need pinned + measured, not spec-sheet alone. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | RLIMIT_MEMLOCK — package cap | Unprivileged lockable RAM ceiling (mlock/pinned). Holds for container-gated cudaHostAlloc caps. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | SPEC CPU 2017 Overview | Analog: SPECspeed = one copy (latency-ish); SPECrate = multi-copy throughput. Holds: do not sell a throughput SKU metric as the single-workload honesty number. Limit: CPU suites ≠ GPU VRAM/PCIe probes. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | SPEC “honest data vs marketing hype” | Analog: standardized, reproducible workload over brochure claims. Holds for catalog methodology over 5090/6000 marketing sheets. Limit: SPEC philosophy ≠ NVML field names. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | The Serialized Bridge: Understanding and Recovering LLM Serving Performance under Blackwell GPU Confidential Computing | RTX Pro 6000 Blackwell SE as **PCIe Gen5** / no-NVLink baseline vs B300 HGX; Pro 6000 vLLM build **does not run on SM100** — cross-SKU image/stack mismatch is a measurement caveat. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | XFP: Quality-Targeted Adaptive Codebook Quantization with Sparse Outlier Separation for LLM Inference | Workstation Blackwell **SM120/121** (RTX PRO 6000) lacks datacenter **SM100+** NVFP4 Tensor Core path; CUTLASS/FlashInfer/vLLM needed community patches; SMEM/CTA budget lower on workstation tier — stack-tier gate, not one Blackwell. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | fio O_DIRECT / libaio honesty | O_DIRECT + async engine or you measure page cache / sync fallback. Holds for NVMe honesty. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | fio `direct` / `iodepth` | Analog: `direct` ⇒ O_DIRECT; `iodepth` sets queue depth. Holds: seq/high-QD headlines ≠ QD1 random honesty for offload math. Limit: fio ≠ CUDA Event timing. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| craft | nvbandwidth | Analog: measure H2D/D2H with timed copies, not brochure PCIe ceilings. Holds as the canonical measure path for catalog. Limit: tool output ≠ LLM tok/s. |  | docker; hw-measurement; Blackwell; sm_120; PCIe | ●●· | · |
| constraint | CUDA-on-WSL guide officially warns pinned + managed memory are limited | NVIDIA's CUDA-on-WSL User Guide states pinned-system-memory availability is limited and full managed/unified memory is unsupported on WSL2, and that some deep-learning workloads may exceed the pinned limit and not work. | no number stated (qualitative 'limited') | windows-wsl2 | ●●● | ✓ |
| technique | Canonical tool: bandwidthTest / nvbandwidth (cudaMemcpy timed by cudaEvent) | The canonical way to measure PCIe H2D/D2H bandwidth is the CUDA bandwidthTest sample (now NVIDIA/nvbandwidth), which times cudaMemcpy with cudaEvent and computes GB/s = bytes / elapsed_time. | 16 MB default quick-mode transfer; GB/s = bytes/time | pcie | ●●● | ✓ |
| constraint | Headline sequential >> realistic random-QD1 — use QD1-4 for offload math | Headline sequential bandwidth (Gen5 ~14 GB/s, Gen4 ~7 GB/s) overstates offload throughput by roughly an order of magnitude versus realistic 4k random QD1-4, which is latency-bound and is the regime mmap'd shard faulting and KV spill actually hit. | Gen5 ~14 GB/s seq, Gen4 ~7 GB/s; random hi-QD ~1.2-1.5M IOPS; QD1 4k far lower (latency-bound) | nvme | ●●● | ✓ |
| constraint | NVIDIA still documents the WSL2 pinned-memory limit (v13.3) — but never as a number | NVIDIA's CUDA-on-WSL User Guide STILL lists 'pinned system memory... availability for applications is limited' as a Known Limitation as of v13.3 (2026-05-21), verbatim-unchanged since v12.0 (2022) — and has NEVER attached a number to it. | v13.3 (2026-05-21) wording == v12.0 (2022-12-08); no numeric cap ever published | windows-wsl2 | ●●● | ✓ |
| constraint | Nearest documented boundary: CUDA 13.2 / driver R595 (2026-03) added native+WSL container support + VMM allocators (not cudaHostAlloc) | The strongest citable capability lift near the rig's result is CUDA 13.2 / driver R595 (2026-03): NVIDIA officially announced 'Native (and WSL) containers are supported' plus cuMemCreate / cudaMallocAsync (advanced/VMM memory-management API) for WSL/MCDM — but this names container + VMM/async allocators, NOT the legacy cudaHostAlloc API. | CUDA 13.2 / R595 (2026-03-09): WSL container support + cuMemCreate/cudaMallocAsync; rig driver 610.47 post-dates it | windows-wsl2 | ●●● | ✓ |
| gotcha | Overlay2 writable layer breaks O_DIRECT and mismeasures — benchmark a mounted volume | Running fio --direct=1 inside a container against the overlay2 writable layer commonly fails with 'destination does not support O_DIRECT', and even where it works the union filesystem mismeasures — so the profiler must target a bind-mounted or named NVMe volume. | overlay2 = union fs overhead; volumes/bind mounts write directly to host fs | in-container | ●●● | ✓ |
| gotcha | Pinned (page-locked) memory is >2x pageable; measure both | Pinned/page-locked host memory attains the highest H2D/D2H bandwidth and is more than 2x faster than pageable, because pageable transfers are staged through a driver-managed pinned bounce buffer. | pinned >2x pageable (2.3 -> 5.8 GB/s H2D on Gen2) | all | ●●● | ✓ |
| technique | Query NVML directly (pynvml) for free/total VRAM, not nvidia-smi text | nvidia-smi is a thin wrapper over NVML, so the profiler should call nvmlDeviceGetMemoryInfo via pynvml/nvidia-ml-py to get free/total/used VRAM in bytes without parsing subprocess text. | 3 fields: total/free/used (bytes) | all | ●●● | ✓ |
| benchmark | Realistic PCIe pinned numbers: Gen3 ~12, Gen4 ~25, Gen5 ~50-55 GB/s (theoretical 64 != measured) | Achieved pinned unidirectional bandwidth is well below the marketed theoretical: ~12 GB/s (Gen3 x16), ~25 GB/s (Gen4 x16), and roughly 50-55 GB/s (Gen5 x16) against a 64 GB/s BIDIRECTIONAL theoretical ceiling. | Gen3 ~12 GB/s; Gen4 ~25 GB/s; Gen5 theoretical 64 GB/s bidir (~50-55 GB/s achievable unidir) | pcie | ●●· | ✓ |
| constraint | The effective WSL2 GPU-accessible host-memory ceiling tracks the VM's assigned RAM (.wslconfig memory=) | Evidence points to the WSL2/container GPU-accessible host-memory ceiling being governed by the WSL2 VM's assigned RAM (.wslconfig 'memory='), consistent with the native ~50%-of-RAM behavior scaling with whatever RAM the VM has — not a fixed NVIDIA number. | ceiling scales with WSL2 VM RAM (.wslconfig memory=); native rule ~50% of RAM | windows-wsl2 | ●●● | ✓ |
| benchmark | The harsh cap still reproduced as of Jan 2026 (driver 572.83) inside Docker — version/config-bound, not universally fixed | The cap is NOT globally fixed: the most recent measured report (microsoft/WSL #14078, 2026-01-17, driver 572.83, WSL 2.4.10) still reproduces ~500 MB single / ~400 MB total pin_memory inside Docker-on-WSL2, and the original 2020 NVIDIA-forum ~300 MB report was confirmed still-blocking in 2021. | ~300 MB (2020) -> ~500 MB single / ~400 MB total (Jan 2026, driver 572.83, Docker) | windows-wsl2 | ●●● | ✓ |
| constraint | The pinned limit is Windows/WDDM-managed, not an NVIDIA driver cap; no official 'lift' changelog exists | An NVIDIA engineer states the pinned-memory limit is 'entirely managed by Windows' (WDDM<->CUDA interop) and 'the NVIDIA driver doesn't control or set the limit'; no NVIDIA/Microsoft release note (2023-2026) announces raising or lifting it. | njuffa (NVIDIA): limit 'depends on internal details of the operating system, not CUDA' | windows-wsl2 | ●●● | ✓ |
| gotcha | The ~300-500 MB cap is a container locked-memory (RLIMIT_MEMLOCK) + WSL2-PV artifact, not an inherent WSL2/driver ceiling | The harsh cap is a CONTAINER / locked-memory artifact, not a WSL2 GPU-driver ceiling: in microsoft/WSL #14078, NATIVE Windows pinned ~4000 MB single / ~5600 MB total on the same rig where the Docker container was held to ~500 MB, and bare (non-container) WSL2 pins small buffers fine. | same rig: native Windows ~4000 MB vs Docker container ~500 MB (#14078, driver 572.83) | in-container | ●●● | ✓ |
| benchmark | This rig probed >=22.5 GiB pinnable on a 31 GiB VM (>=72%) — exceeding the native 50% rule, consistent with the container being the only gate | On driver 610.47 the gpu-container cudaHostAlloc probe succeeded to >=22.5 GiB inside Docker-on-WSL2 (a 31 GiB VM, >=72% of VM RAM) with no failure — exceeding even the Windows-native ~50%-of-RAM cap, consistent with the container layer being the only real gate and the ceiling tracking VM RAM. | >=22.5 GiB / 31 GiB VM (>=72%); vs prior KB 300-500 MB; vs native ~50% rule | windows-wsl2 | ●●● | ✓ |
| method | Three-axis fio measurement: seq throughput, random IOPS, QD1 latency | Correct NVMe characterization needs three distinct fio passes — sequential (large bs, high QD), random IOPS (4k, high QD), and QD1 latency (4k, iodepth=1) — because each isolates a different bottleneck. | seq bs=256k-1M iodepth=64; random bs=4k; latency iodepth=1; QD4 for realistic offload | nvme | ●●● | ✓ |
| gotcha | Under WSL2, NVML utilization + per-process memory are unsupported (N/A); free/total/PCIe/compute-cap are fine | The CUDA-on-WSL guide says NVML does not yet support all queries — GPU utilization and active-compute-process queries are unsupported, and per-process GPU memory returns N/A inside WSL2. | utilization + per-process mem = unsupported/N/A under WSL2 | in-container | ●●● | ✓ |
| method | Use large transfers + warmup + median to saturate the link | Per-call overhead dominates small transfers, so a stable, link-saturating measurement requires large buffers (tens to hundreds of MB), a warmup copy, and a median over repeated runs. | >=64-256 MB buffer; median of >=5 runs after 1 warmup | all | ●●● | ✓ |
| gotcha | Use nvmlDeviceGetMemoryInfo_v2 so 'reserved' VRAM is not counted as 'used' | The v1 nvmlDeviceGetMemoryInfo folds driver-reserved VRAM into the 'used' field, so v1 'free' under-reports and v1 'used' over-reports; v2 exposes reserved separately. | v2 adds a 4th field: reserved | vram | ●●● | ✓ |
| constraint | WSL2 collapses the pinnable host-RAM ceiling to a few hundred MB | Under WSL2 (including Docker-on-WSL2), cudaHostAlloc/pin_memory fails far below the native limit — reproducibly at roughly 300-500 MB versus several GB on native Linux/Windows. | ~300-500 MB pinnable in WSL2 vs 4 GB native | windows-wsl2 | ●●● | ✓ |
| constraint | WSL2/WDDM caps pinned memory LOWER than native Windows (~50% RAM, less under WSL2) | cudaHostAlloc pinning is capped by Windows at ~50% of system RAM, and that cap is even LOWER under WSL2 due to extra WDDM machinery -- so a large pinned buffer can fail inside the container. | ~50% RAM native Windows (15.04 GB of 32 GB measured); lower under WSL2 | windows-wsl2 | ●●● | ✓ |
| gotcha | WSL2: measure on the ext4 vdisk, never /mnt/c (9p/drvfs is ~5-10x slower) | Inside a WSL2 Linux container, benchmarking a /mnt/c (drvfs/9p) path reports NVMe bandwidth 5-10x lower than reality; the test path must live on the Linux ext4 vdisk (or a volume bind-mounted from it). | /mnt/c via 9p ~5-10x slower than native WSL2 ext4 (issue #4197: >10x) | windows-wsl2 | ●●● | ✓ |
| technique | direct=1 + libaio is mandatory to bypass the page cache | Without --direct=1 (and a test size larger than RAM) fio measures the OS page cache, not the NVMe — and libaio queueing only works with non-buffered I/O. | test file size > 64 GB RAM on this rig | nvme | ●●● | ✓ |
| gotcha | nvidia-smi/NVML is degraded under WSL2: pcie.link.gen/width often N/A -- do not trust as ground truth | Under WSL2 the NVML backend behind nvidia-smi does not support all queries; pcie.link.gen / pcie.link.width and several utilization fields commonly return N/A or are unreliable inside the container. | pcie.link.gen/width => N/A in WSL2; NVML queries partially unsupported | in-container | ●●● | ✓ |
| method | Fragmentation is invisible in free/total; probe the largest contiguous block, not the sum | Total free VRAM is not the same as the largest allocatable contiguous block; cudaMalloc can fail despite ample total-free, so fragmentation must be probed, not inferred from NVML free. | no NVML largest-block field; cudaMalloc can fail with free>request | vram | ●●· | ✓ |
| benchmark | Native Windows pins ~50% of system RAM; WSL2 is lower (NVIDIA-confirmed) | On native Windows the cudaHostAlloc pinnable ceiling is ~50% of system RAM (WDDM-imposed), and NVIDIA staff state WSL2 limits are lower than the Windows-side number. | ~50% of RAM native Windows (measured 47% / 15.04 GB on 32 GB); WSL2 lower | windows-wsl2 | ●●● | ✓ |
| gotcha | WDDM submission latency penalizes WSL2 vs bare-metal Linux on small/short work | WSL2 runs the GPU through the Windows WDDM driver, adding launch/submission latency and memory-allocation overhead, so short or small-transfer measurements are slower and noisier inside WSL2 than on native Linux. | 11 ms (bare Linux) vs 19 ms/frame (WSL2/Windows) app-level | windows-wsl2 | ●●· | ✓ |
| constraint | WSL2 GPU CUDA caveats don't cover disk — profiler owns disk fidelity | NVIDIA's CUDA-on-WSL guide documents GPU/pinned-memory caveats but says nothing about disk I/O, so the burden of measuring NVMe truthfully from inside the WSL2 container falls entirely on the profiler's own discipline. | no disk-I/O guidance in CUDA-on-WSL guide | windows-wsl2 | ●●· | ✓ |
| constraint | WSL2 is more restrictive than native Windows because of GPU-PV (paravirtualization) between guest and WDDM | NVIDIA explicitly attributes WSL2's lower pinning to extra 'WSL2->WDDM machinery' — GPU paravirtualization (GPU-PV) sitting between the guest and the host WDDM driver is the named mechanism that historically made WSL2 pinning lower than native Windows. | qualitative: GPU-PV adds a guest->host WDDM hop | windows-wsl2 | ●●● | ✓ |

## Detail

### A Method for Layer Bit-Width Allocation in LLM Quantization via Performance Maximization Under a Quality-Degradation Constraint · `directional` · craft
**Explicitly names **RTX 5090 (Blackwell, sm_120)** and notes kernel-selection differs from Ampere sm_86 — consumer sm_120 is the named compute target for 5090-class claims.**
Explicitly names **RTX 5090 (Blackwell, sm_120)** and notes kernel-selection differs from Ampere sm_86 — consumer sm_120 is the named compute target for 5090-class claims.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [A Method for Layer Bit-Width Allocation in LLM Quantization via Performance Maxi](https://arxiv.org/abs/2608.28003)

### Blackwell Compatibility Guide · `directional` · craft
**Toolkit **12.8** `nvcc` emits native **compute_100 / sm_100** cubin (+ PTX). Apps need PTX or sm_100 cubin for Blackwell. Page focuses **CC 10.0**; does not name 5090 or quote measured bandwidth.**
Toolkit **12.8** `nvcc` emits native **compute_100 / sm_100** cubin (+ PTX). Apps need PTX or sm_100 cubin for Blackwell. Page focuses **CC 10.0**; does not name 5090 or quote measured bandwidth.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [Blackwell Compatibility Guide](https://docs.nvidia.com/cuda/archive/12.8.2/blackwell-compatibility-guide/index.html)

### Blackwell Tuning Guide · `directional` · craft
**Documents **CC 10.0 and 12.0** (warps/SM, shared-mem caps differ). B200 as CC 10.0 example. Establishes **10.0 ≠ 12.0** on the same architecture family — relevant vs catalog sm_100 vs sm_120 distinction.**
Documents **CC 10.0 and 12.0** (warps/SM, shared-mem caps differ). B200 as CC 10.0 example. Establishes **10.0 ≠ 12.0** on the same architecture family — relevant vs catalog sm_100 vs sm_120 distinction.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [Blackwell Tuning Guide](https://docs.nvidia.com/cuda/blackwell-tuning-guide/index.html)

### CUDA 12.8 Blackwell compatibility — sm_100 · `directional` · docs
**Toolkit 12.8 emits native sm_100/compute_100; PTX forward-compat.**
Toolkit 12.8 emits native sm_100/compute_100; PTX forward-compat.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** B200-class currency pin
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [CUDA 12.8 Blackwell compatibility — sm_100](https://docs.nvidia.com/cuda/archive/12.8.2/blackwell-compatibility-guide/index.html) — SUPPORTED

### CUDA C++ Best Practices · `directional` · craft
**Pinned via `cudaHostAlloc`; cites **~12 GB/s on PCIe x16 Gen3** as illustrative; points to `bandwidthTest` sample. Timing via `cudaEventElapsedTime`. Gen3 example only — **not** a 5090/Gen5 measurement.**
Pinned via `cudaHostAlloc`; cites **~12 GB/s on PCIe x16 Gen3** as illustrative; points to `bandwidthTest` sample. Timing via `cudaEventElapsedTime`. Gen3 example only — **not** a 5090/Gen5 measurement.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [CUDA C++ Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)

### CUDA C++ Best Practices · `directional` · craft
**Analog: theoretical link rate ≠ effective measured bandwidth; pinned Host↔Device must be timed. Holds for PCIe honesty vs SKU “Gen5 x16” marketing. Limit: guide cites Gen3-class examples.**
Analog: theoretical link rate ≠ effective measured bandwidth; pinned Host↔Device must be timed. Holds for PCIe honesty vs SKU “Gen5 x16” marketing. Limit: guide cites Gen3-class examples.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [CUDA C++ Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)

### CUDA Demo Suite · `directional` · craft
**Measures D2D / H2D / D2H for **pageable** and **pinned**; knobs `--memory=pinned|pageable`, `--mode=quick|range|shmoo`, `--htod`/`--dtoh`/`--dtod`, `--device`, `--wc`. **No default transfer size or GB/s figures on this page.****
Measures D2D / H2D / D2H for **pageable** and **pinned**; knobs `--memory=pinned|pageable`, `--mode=quick|range|shmoo`, `--htod`/`--dtoh`/`--dtod`, `--device`, `--wc`. **No default transfer size or GB/s figures on this page.**
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [CUDA Demo Suite](https://docs.nvidia.com/cuda/demo-suite/index.html)

### CUDA on WSL User Guide 13.3 · `directional` · craft
**Known limits: **pinned system memory availability limited** (no numeric cap); unified/managed memory unsupported; **NVML**: utilization + active compute process queries unsupported; ECC/compute/persistence mode not modifiable. Measure free/total-style queries separately from util.**
Known limits: **pinned system memory availability limited** (no numeric cap); unified/managed memory unsupported; **NVML**: utilization + active compute process queries unsupported; ECC/compute/persistence mode not modifiable. Measure free/total-style queries separately from util.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [CUDA on WSL User Guide 13.3](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)

### Characterizing Warp Divergence from Pascal to Blackwell · `directional` · craft
**Labels Blackwell **server sm_110** vs **consumer sm_120** (RTX 5080); static SASS spans sm_80–sm_120 including sm_100/110/120 — consumer vs server compute-cap are distinct labels.**
Labels Blackwell **server sm_110** vs **consumer sm_120** (RTX 5080); static SASS spans sm_80–sm_120 including sm_100/110/120 — consumer vs server compute-cap are distinct labels.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [Characterizing Warp Divergence from Pascal to Blackwell](https://arxiv.org/abs/2607.23402)

### Darzi — host-side eBPF + NVML/NCCL · `directional` · craft
**eBPF host signals correlated with NVML + NCCL for GPU tail latency RCA.**
eBPF host signals correlated with NVML + NCCL for GPU tail latency RCA.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [Darzi — host-side eBPF + NVML/NCCL](https://arxiv.org/abs/2510.16946) — Darzi et al. 2025; SUPPORTED

### ESS: An Offload-Centric Latent-Cache Management Architecture for DeepSeek-V3.2-Exp · `directional` · craft
**PCIe 5.0 unidirectional theoretical ceiling does not equal effective cudaMemcpyAsync under fine-grained non-contiguous pages — measurement honesty: theoretical Gen5 ≠ fragmented effective BW.**
PCIe 5.0 unidirectional theoretical ceiling does not equal effective cudaMemcpyAsync under fine-grained non-contiguous pages — measurement honesty: theoretical Gen5 ≠ fragmented effective BW.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [ESS: An Offload-Centric Latent-Cache Management Architecture for DeepSeek-V3.2-E](https://arxiv.org/abs/2512.10576)

### Evaluating CUDA Tile for AI Workloads on Hopper and Blackwell GPUs · `directional` · craft
**Table contrasts H100 NVL **sm_90**, RTX PRO 6000 Blackwell **sm_120**, and B200 **sm_100**; warns workstation sm_120 CuTile/compiler immaturity vs datacenter Blackwell — sm_100 ≠ sm_120 (wave-06/77 deepen).**
Table contrasts H100 NVL **sm_90**, RTX PRO 6000 Blackwell **sm_120**, and B200 **sm_100**; warns workstation sm_120 CuTile/compiler immaturity vs datacenter Blackwell — sm_100 ≠ sm_120 (wave-06/77 deepen).
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [Evaluating CUDA Tile for AI Workloads on Hopper and Blackwell GPUs](https://arxiv.org/abs/2604.23466)

### Evaluating CUDA Tile… · `directional` · craft
**Analog: B200 `sm_100` vs RTX PRO 6000 `sm_120` are distinct stacks; cross-arch gaps are real. Holds: **sm_100 ≠ sm_120**. Limit: CuTile paper ≠ container profiler receipt format.**
Analog: B200 `sm_100` vs RTX PRO 6000 `sm_120` are distinct stacks; cross-arch gaps are real. Holds: **sm_100 ≠ sm_120**. Limit: CuTile paper ≠ container profiler receipt format.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [Evaluating CUDA Tile…](https://arxiv.org/abs/2604.23466)

### Gaps vs hw-measurement catalog · `directional` · craft
**On these primary pages: **Absent** product-named RTX 5090 / RTX PRO 6000 measured H2D/D2H GB/s; absent numeric WSL pin ceiling; compatibility guide’s build recipe is sm_100-centric (sm_120 targeting lives mainly in tuning CC 12.0 notes / other CUDA docs). Catalog’s “measure yourself / no invented GB/s” matches the page silence.**
On these primary pages: **Absent** product-named RTX 5090 / RTX PRO 6000 measured H2D/D2H GB/s; absent numeric WSL pin ceiling; compatibility guide’s build recipe is sm_100-centric (sm_120 targeting lives mainly in tuning CC 12.0 notes / other CUDA docs). Catalog’s “measure yourself / no invented GB/s” matches the page silence.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen

### Kernel AIO / O_DIRECT caveats · `directional` · craft
**Async without O_DIRECT quietly becomes sync — headline sequential >> realistic QD1 pattern.**
Async without O_DIRECT quietly becomes sync — headline sequential >> realistic QD1 pattern.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [Kernel AIO / O_DIRECT caveats](http://lse.sourceforge.net/io/aio.html) — 2026; SUPPORTED

### Microbenchmarking NVIDIA Blackwell B200 · `directional` · craft
**Microbenchmarks B200 (5th-gen tensor cores, TMEM, dual-chip) — image/toolkit must match architecture features.**
Microbenchmarks B200 (5th-gen tensor cores, TMEM, dual-chip) — image/toolkit must match architecture features.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Blackwell currency: toolkit/image match architecture
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [Microbenchmarking NVIDIA Blackwell B200](https://arxiv.org/abs/2512.02189) — Jarmusch & Chandrasekaran 2025; SUPPORTED

### NGC TensorFlow 25.01 — CUDA 12.8 / driver ≥570 · `directional` · docs
**Container ships CUDA 12.8.0; driver ≥570; Blackwell-optimized NGC DL containers.**
Container ships CUDA 12.8.0; driver ≥570; Blackwell-optimized NGC DL containers.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Deepens package/place
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [NGC TensorFlow 25.01 — CUDA 12.8 / driver ≥570](https://docs.nvidia.com/deeplearning/frameworks/tensorflow-release-notes/rel-25-01.html) — SUPPORTED

### NVIDIA/nvbandwidth README · `directional` · craft
**/ raw README — Successor tool: named cases e.g. `host_to_device_memcpy_ce`, `device_to_host_memcpy_ce`; CE vs SM copies; default buffer **512 MiB**, `--testSamples` median; reports **current measured** GB/s on the system (not a published 5090 floor).**
/ raw README — Successor tool: named cases e.g. `host_to_device_memcpy_ce`, `device_to_host_memcpy_ce`; CE vs SM copies; default buffer **512 MiB**, `--testSamples` median; reports **current measured** GB/s on the system (not a published 5090 floor).
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [NVIDIA/nvbandwidth README](https://github.com/NVIDIA/nvbandwidth)

### NVML Device Queries · `directional` · craft
**`nvmlDeviceGetMemoryInfo` / `_v2`; `nvmlDeviceGetCudaComputeCapability` (major/minor); `nvmlDeviceGetCurrPcieLinkWidth` / Generation; BAR1 memory. Fields for VRAM/PCIe/CC — not bandwidth numbers.**
`nvmlDeviceGetMemoryInfo` / `_v2`; `nvmlDeviceGetCudaComputeCapability` (major/minor); `nvmlDeviceGetCurrPcieLinkWidth` / Generation; BAR1 memory. Fields for VRAM/PCIe/CC — not bandwidth numbers.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [NVML Device Queries](https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceQueries.html)

### Non-Uniform L2 Cache Latency Across the Streaming Multiprocessors of an NVIDIA L40 · `directional` · craft
**Same probe on **RTX 5090 (Blackwell GB202)** shows L2-hit latency varies by physical SM; device-specific fingerprints — 5090 microarchitecture measurement ≠ transplanting B200/datacenter numbers.**
Same probe on **RTX 5090 (Blackwell GB202)** shows L2-hit latency varies by physical SM; device-specific fingerprints — 5090 microarchitecture measurement ≠ transplanting B200/datacenter numbers.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [Non-Uniform L2 Cache Latency Across the Streaming Multiprocessors of an NVIDIA L](https://arxiv.org/abs/2606.22588)

### OOM-Free Alpamayo via CPU-GPU Memory Swapping for Vision-Language-Action Models · `directional` · craft
**Consumer Blackwell-class PCIe Gen5 path: measures with **pinned** memory and names Gen5 vs Gen3 DMA shifts — catalog PCIe claims need pinned + measured, not spec-sheet alone.**
Consumer Blackwell-class PCIe Gen5 path: measures with **pinned** memory and names Gen5 vs Gen3 DMA shifts — catalog PCIe claims need pinned + measured, not spec-sheet alone.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [OOM-Free Alpamayo via CPU-GPU Memory Swapping for Vision-Language-Action Models](https://arxiv.org/abs/2605.11678)

### RLIMIT_MEMLOCK — package cap · `directional` · craft
**Unprivileged lockable RAM ceiling (mlock/pinned). Holds for container-gated cudaHostAlloc caps.**
Unprivileged lockable RAM ceiling (mlock/pinned). Holds for container-gated cudaHostAlloc caps.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [RLIMIT_MEMLOCK — package cap](https://www.man7.org/linux/man-pages/man2/setrlimit.2.html) — 2026; SUPPORTED

### SPEC CPU 2017 Overview · `directional` · craft
**Analog: SPECspeed = one copy (latency-ish); SPECrate = multi-copy throughput. Holds: do not sell a throughput SKU metric as the single-workload honesty number. Limit: CPU suites ≠ GPU VRAM/PCIe probes.**
Analog: SPECspeed = one copy (latency-ish); SPECrate = multi-copy throughput. Holds: do not sell a throughput SKU metric as the single-workload honesty number. Limit: CPU suites ≠ GPU VRAM/PCIe probes.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [SPEC CPU 2017 Overview](https://www.spec.org/cpu2017/Docs/overview.html)

### SPEC “honest data vs marketing hype” · `directional` · craft
**Analog: standardized, reproducible workload over brochure claims. Holds for catalog methodology over 5090/6000 marketing sheets. Limit: SPEC philosophy ≠ NVML field names.**
Analog: standardized, reproducible workload over brochure claims. Holds for catalog methodology over 5090/6000 marketing sheets. Limit: SPEC philosophy ≠ NVML field names.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen

### The Serialized Bridge: Understanding and Recovering LLM Serving Performance under Blackwell GPU Confidential Computing · `directional` · craft
**RTX Pro 6000 Blackwell SE as **PCIe Gen5** / no-NVLink baseline vs B300 HGX; Pro 6000 vLLM build **does not run on SM100** — cross-SKU image/stack mismatch is a measurement caveat.**
RTX Pro 6000 Blackwell SE as **PCIe Gen5** / no-NVLink baseline vs B300 HGX; Pro 6000 vLLM build **does not run on SM100** — cross-SKU image/stack mismatch is a measurement caveat.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [The Serialized Bridge: Understanding and Recovering LLM Serving Performance unde](https://arxiv.org/abs/2606.23969)

### XFP: Quality-Targeted Adaptive Codebook Quantization with Sparse Outlier Separation for LLM Inference · `directional` · craft
**Workstation Blackwell **SM120/121** (RTX PRO 6000) lacks datacenter **SM100+** NVFP4 Tensor Core path; CUTLASS/FlashInfer/vLLM needed community patches; SMEM/CTA budget lower on workstation tier — stack-tier gate, not one Blackwell.**
Workstation Blackwell **SM120/121** (RTX PRO 6000) lacks datacenter **SM100+** NVFP4 Tensor Core path; CUTLASS/FlashInfer/vLLM needed community patches; SMEM/CTA budget lower on workstation tier — stack-tier gate, not one Blackwell.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [XFP: Quality-Targeted Adaptive Codebook Quantization with Sparse Outlier Separat](https://arxiv.org/abs/2605.14844)

### fio O_DIRECT / libaio honesty · `directional` · craft
**O_DIRECT + async engine or you measure page cache / sync fallback. Holds for NVMe honesty.**
O_DIRECT + async engine or you measure page cache / sync fallback. Holds for NVMe honesty.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [fio O_DIRECT / libaio honesty](https://manpages.debian.org/unstable/fio/fio.1.en.html) — 2026; SUPPORTED

### fio `direct` / `iodepth` · `directional` · craft
**Analog: `direct` ⇒ O_DIRECT; `iodepth` sets queue depth. Holds: seq/high-QD headlines ≠ QD1 random honesty for offload math. Limit: fio ≠ CUDA Event timing.**
Analog: `direct` ⇒ O_DIRECT; `iodepth` sets queue depth. Holds: seq/high-QD headlines ≠ QD1 random honesty for offload math. Limit: fio ≠ CUDA Event timing.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [fio `direct` / `iodepth`](https://fio.readthedocs.io/en/latest/fio_doc.html)

### nvbandwidth · `directional` · craft
**Analog: measure H2D/D2H with timed copies, not brochure PCIe ceilings. Holds as the canonical measure path for catalog. Limit: tool output ≠ LLM tok/s.**
Analog: measure H2D/D2H with timed copies, not brochure PCIe ceilings. Holds as the canonical measure path for catalog. Limit: tool output ≠ LLM tok/s.
- **Applies to:** docker; hw-measurement; Blackwell; sm_120; PCIe · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen hw-measurement honesty. Do not equate sm_100↔sm_120.
- **Verify:** verdict=unverified | STUDY-049 deepen
- **Sources:** [nvbandwidth](https://github.com/NVIDIA/nvbandwidth)

### CUDA-on-WSL guide officially warns pinned + managed memory are limited · `load-bearing` · constraint
**NVIDIA's CUDA-on-WSL User Guide states pinned-system-memory availability is limited and full managed/unified memory is unsupported on WSL2, and that some deep-learning workloads may exceed the pinned limit and not work.**
Exact wording: 'Pinned system memory... availability for applications is limited' and 'some deep learning training workloads... can exceed this limit and may not work.' Also: 'Unified Memory - Full Managed Memory Support is not available on Windows native and therefore WSL 2 will not support it... applications using Managed Memory could see reduced performance and high system memory usage.' This is the authoritative confirmation that the rig's container vantage has a real, documented pinned/UVM ceiling — no number given in the guide, hence the need to probe.
- **Applies to:** windows-wsl2 · **Metric:** no number stated (qualitative 'limited') · **Confidence:** high
- **Design implication:** Profiler treats the pinned ceiling as a measured-not-assumed quantity on WSL2, and should avoid any plan path that relies on cudaMallocManaged/UVM oversubscription for bandwidth since full UVM is unsupported there.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [CUDA on WSL User Guide — Features Not Yet Supported / Known Limitations](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA 2025; qualitative: pinned 'limited', full UVM unsupported; SUPPORTED

### Canonical tool: bandwidthTest / nvbandwidth (cudaMemcpy timed by cudaEvent) · `load-bearing` · technique
**The canonical way to measure PCIe H2D/D2H bandwidth is the CUDA bandwidthTest sample (now NVIDIA/nvbandwidth), which times cudaMemcpy with cudaEvent and computes GB/s = bytes / elapsed_time.**
bandwidthTest measures host-to-device, device-to-host, and device-to-device memcpy bandwidth, with --memory=pinned|pageable, --mode=quick|range|shmoo, --device=N, and --wc (write-combined). Default quick mode uses a 16 MB transfer. The modern actively-maintained successor is NVIDIA/nvbandwidth, which exposes named test cases host_to_device_memcpy_ce / device_to_host_memcpy_ce (plus bidirectional and kernel-copy variants) and likewise computes bandwidth as (data size)/(time) from CUDA events. A minimal hand-rolled loop is equivalent: cudaHostAlloc a buffer, cudaEventRecord before/after cudaMemcpy(H2D then D2H), cudaEventElapsedTime, GB/s = bytes*1e-9/seconds.
- **Applies to:** pcie · **Metric:** 16 MB default quick-mode transfer; GB/s = bytes/time · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** measure_bandwidth() should replicate bandwidthTest/nvbandwidth semantics: a pinned buffer, cudaEvent timing around cudaMemcpy, separate H2D and D2H passes. Either shell out to nvbandwidth and parse its GB/s, or implement the minimal cudaEvent loop directly for full control over buffer size and repetition.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [CUDA Demo Suite documentation (bandwidthTest utility)](https://docs.nvidia.com/cuda/demo-suite/index.html) — NVIDIA Corporation 2026; 16 MB default quick-mode transfer size; SUPPORTED ; [NVIDIA/nvbandwidth - A tool for bandwidth measurements on NVIDIA GPUs](https://github.com/NVIDIA/nvbandwidth) — NVIDIA 2026; GB/s = (size of data) / (time); SUPPORTED ; [How to Optimize Data Transfers in CUDA C/C++ (NVIDIA Technical Blog)](https://developer.nvidia.com/blog/how-optimize-data-transfers-cuda-cc/) — Mark Harris, NVIDIA 2012; 16 MB transfer; bandwidth = bytes * 1e-6 / time; SUPPORTED

### Headline sequential >> realistic random-QD1 — use QD1-4 for offload math · `load-bearing` · constraint
**Headline sequential bandwidth (Gen5 ~14 GB/s, Gen4 ~7 GB/s) overstates offload throughput by roughly an order of magnitude versus realistic 4k random QD1-4, which is latency-bound and is the regime mmap'd shard faulting and KV spill actually hit.**
Vendor/aggregate data: Gen4 NVMe ~7 GB/s seq read, Gen5 ~14 GB/s; high-QD random ~1.2-1.5M IOPS (~5-6 GB/s). But real offload (page-faulting mmap'd weight shards, KV spill) issues mostly QD1, rarely >QD4, where throughput is latency-bound and far lower — tens to low-hundreds of MB/s. Reviewers consistently flag 4k QD1 as the realistic single-user metric and note generation-to-generation random-QD1 gains are modest (<1.5x), unlike the ~2x sequential jump. The planner's tok/s honesty (refuse below 1 tok/s, +/-10% receipt) depends on streaming math using the random-QD1-4 number, not the seq headline.
- **Applies to:** nvme · **Metric:** Gen5 ~14 GB/s seq, Gen4 ~7 GB/s; random hi-QD ~1.2-1.5M IOPS; QD1 4k far lower (latency-bound) · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Profiler computes cold-expert/weight-streaming feasibility from the random-QD1 (and QD4) figure, and uses the sequential figure only as a labeled optimistic ceiling. Both stored in profile.json; the streaming/refusal decision keys off the random number.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [What is PCIe Gen 4 for SSDs, and how does it compare to Gen 3 and Gen 5?](https://insights.samsung.com/2024/03/07/what-is-pcie-gen-4-for-ssds-and-how-does-it-compare-to-gen-3-and-gen-5/) — Samsung Business Insights 2024; Gen4 ~7,000 MB/s; Gen5 ~14,000 MB/s sequential read; PARTIAL ; [What is more relevant for best performance? Random Read 4KB QD=32 vs QD=1 vs 512KB](https://www.overclock.net/threads/what-is-more-relevant-for-best-performance-random-read-4kb-qd-32-random-read-4kb-qd-1-or-random-read-512kb.1522106/) — Overclock.net community 2020; real-world random QD mostly 1, rarely >4; SUPPORTED

### NVIDIA still documents the WSL2 pinned-memory limit (v13.3) — but never as a number · `load-bearing` · constraint
**NVIDIA's CUDA-on-WSL User Guide STILL lists 'pinned system memory... availability for applications is limited' as a Known Limitation as of v13.3 (2026-05-21), verbatim-unchanged since v12.0 (2022) — and has NEVER attached a number to it.**
The qualitative limitation is current and un-retracted across >=3.5 years of doc revisions; the same DL-workload caveat ('some training workloads... can exceed this limit and may not work') persists. The '~300-500 MB' figure the KB carried is therefore NOT an NVIDIA spec — it is a community-observed, version/config-bound measurement, never an official ceiling.
- **Applies to:** windows-wsl2 · **Metric:** v13.3 (2026-05-21) wording == v12.0 (2022-12-08); no numeric cap ever published · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Treat the documented limitation as a qualitative WORST-CASE PRIOR to be overridden by a live cudaHostAlloc probe — never as a hard numeric ceiling. The KB's 300-500 MB number must be reframed as community-observed and version-bound, not a vendor spec.
- **Verify:** verdict=confirmed | oracle retrieval (existence+groundedness) + family-different (granite4.1:30b: confirmed | mistral-small:24b: confirmed/1x cant_confirm (2026-source recency)); 0 refutations
- **Sources:** [CUDA on WSL User Guide — CUDA on WSL 13.3 documentation (Known Limitations 5.1)](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA Corporation 2026; SUPPORTED ; [CUDA on WSL User Guide (archived v12.0)](https://docs.nvidia.com/cuda/archive/12.0.0/wsl-user-guide/index.html) — NVIDIA Corporation 2022; SUPPORTED

### Nearest documented boundary: CUDA 13.2 / driver R595 (2026-03) added native+WSL container support + VMM allocators (not cudaHostAlloc) · `load-bearing` · constraint
**The strongest citable capability lift near the rig's result is CUDA 13.2 / driver R595 (2026-03): NVIDIA officially announced 'Native (and WSL) containers are supported' plus cuMemCreate / cudaMallocAsync (advanced/VMM memory-management API) for WSL/MCDM — but this names container + VMM/async allocators, NOT the legacy cudaHostAlloc API.**
The rig's driver 610.47 post-dates R595, so it runs the improved WSL-container code path — consistent with a Docker-on-WSL2 container now behaving far better than the 572.83-era reports. But the release note does not literally say 'cudaHostAlloc limit raised', so this is an ANCHOR for 'WSL container memory improved in early 2026', not proof of a pinned-API fix.
- **Applies to:** windows-wsl2 · **Metric:** CUDA 13.2 / R595 (2026-03-09): WSL container support + cuMemCreate/cudaMallocAsync; rig driver 610.47 post-dates it · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Cite R595 as the plausible 'why it improved' boundary with the correct caveat (container/VMM support, not the pinned API). Frames the receipt honestly: the lift is real and roughly dateable, but not attributable to a documented cudaHostAlloc change.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval (existence+groundedness) + family-different (granite4.1:30b: confirmed | mistral-small:24b: confirmed); 0 refutations
- **Sources:** [CUDA 13.2 Introduces Enhanced CUDA Tile Support and New Python Features (NVIDIA Technical Blog)](https://developer.nvidia.com/blog/cuda-13-2-introduces-enhanced-cuda-tile-support-and-new-python-features/) — NVIDIA Corporation 2026; SUPPORTED ; [Extended GPU Memory / cuMemCreate host-NUMA allocation (CUDA C++ Programming Guide & Runtime API)](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__MEMORY.html) — NVIDIA Corporation 2026; PARTIAL

### Overlay2 writable layer breaks O_DIRECT and mismeasures — benchmark a mounted volume · `load-bearing` · gotcha
**Running fio --direct=1 inside a container against the overlay2 writable layer commonly fails with 'destination does not support O_DIRECT', and even where it works the union filesystem mismeasures — so the profiler must target a bind-mounted or named NVMe volume.**
fio GitHub issue #120 (and #145) report 'fio: looks like your file system does not support direct=1/buffered=0' / 'destination does not support O_DIRECT' when run from inside a Docker container on overlayfs. Docker's own storage docs: 'The storage driver provides a union filesystem... This extra abstraction reduces performance as compared to using volumes, which write directly to the host filesystem.' So the planner's profiler must (a) write its fio test file into a bind-mounted host NVMe directory or a named volume (which bypass the storage driver), NOT into the container's working dir on overlay; (b) detect the O_DIRECT-unsupported error and FAIL LOUD — silently switching to direct=0 would measure page cache and produce a dishonest number.
- **Applies to:** in-container · **Metric:** overlay2 = union fs overhead; volumes/bind mounts write directly to host fs · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Profiler asserts the fio target path is on a mounted volume (not overlay) before measuring — e.g. check the mount type — and treats an O_DIRECT failure as a hard refusal/andon, never an auto-fallback to buffered I/O.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [Running FIO in a Docker Container? (issue #120)](https://github.com/axboe/fio/issues/120) — axboe/fio contributors 2016; direct=1 unsupported on container overlayfs; SUPPORTED ; [libaio and direct=1 error with panfs (issue #145)](https://github.com/axboe/fio/issues/145) — axboe/fio contributors 2016; libaio+direct=1 fails on non-O_DIRECT filesystems; SUPPORTED ; [Volumes / Docker Docs (storage)](https://docs.docker.com/engine/storage/volumes/) — Docker Inc. 2025; union fs (overlay2) slower than direct-to-host volumes; SUPPORTED

### Pinned (page-locked) memory is >2x pageable; measure both · `load-bearing` · gotcha
**Pinned/page-locked host memory attains the highest H2D/D2H bandwidth and is more than 2x faster than pageable, because pageable transfers are staged through a driver-managed pinned bounce buffer.**
NVIDIA-measured: on a constrained PCIe Gen2 laptop, pageable H2D was 2.3 GB/s vs pinned 5.8 GB/s (D2H 2.3 vs 6.0); on a Gen2 desktop pageable 5.4 vs pinned 6.2 (H2D). The CUDA C++ Best Practices Guide states flatly: 'Page-locked or pinned memory transfers attain the highest bandwidth between the host and the device.' A pageable-only measurement therefore understates the true link capability. Pinned is allocated via cudaHostAlloc / cudaMallocHost.
- **Applies to:** all · **Metric:** pinned >2x pageable (2.3 -> 5.8 GB/s H2D on Gen2) · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** measure_bandwidth() must report PINNED H2D and D2H as the headline numbers (they reflect link capability), and may additionally report a pageable number as a sanity floor. The +/-10% receipt and any 'refuse below 1 tok/s' logic should be anchored to the PINNED figure, not the pageable one. Always record which buffer type produced each number.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [How to Optimize Data Transfers in CUDA C/C++ (NVIDIA Technical Blog)](https://developer.nvidia.com/blog/how-optimize-data-transfers-cuda-cc/) — Mark Harris, NVIDIA 2012; pageable 2.3 GB/s -> pinned 5.8 GB/s H2D; pinned >2x pageable; SUPPORTED ; [CUDA C++ Best Practices Guide - Data Transfer Between Host and Device](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html) — NVIDIA Corporation 2026; ~12 GB/s pinned on PCIe x16 Gen3; SUPPORTED

### Query NVML directly (pynvml) for free/total VRAM, not nvidia-smi text · `load-bearing` · technique
**nvidia-smi is a thin wrapper over NVML, so the profiler should call nvmlDeviceGetMemoryInfo via pynvml/nvidia-ml-py to get free/total/used VRAM in bytes without parsing subprocess text.**
Use the Python binding nvidia-ml-py (pynvml): nvmlInit(); h = nvmlDeviceGetHandleByIndex(0); m = nvmlDeviceGetMemoryInfo(h) returns a struct with.total,.free,.used in BYTES. The binding talks to the NVML C library directly and is faster than and avoids the fragile text-parsing of shelling out to nvidia-smi. nvidia-smi itself uses NVML underneath, so there is no fidelity gain from the CLI.
- **Applies to:** all · **Metric:** 3 fields: total/free/used (bytes) · **Confidence:** high
- **Design implication:** Profiler reads VRAM free/total through pynvml (bytes), treats the values as bytes, and does not shell out to nvidia-smi or screen-scrape its output.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [NVML API Reference Guide — Device Queries (nvmlDeviceGetMemoryInfo)](https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceQueries.html) — NVIDIA 2024; 3 fields (total/free/used); SUPPORTED ; [pynvml — Python access to the NVML library for GPU diagnostics](https://github.com/gpuopenanalytics/pynvml) — gpuopenanalytics 2024; PARTIAL

### Realistic PCIe pinned numbers: Gen3 ~12, Gen4 ~25, Gen5 ~50-55 GB/s (theoretical 64 != measured) · `load-bearing` · benchmark
**Achieved pinned unidirectional bandwidth is well below the marketed theoretical: ~12 GB/s (Gen3 x16), ~25 GB/s (Gen4 x16), and roughly 50-55 GB/s (Gen5 x16) against a 64 GB/s BIDIRECTIONAL theoretical ceiling.**
Best Practices cites ~12 GB/s pinned on Gen3 x16. NVIDIA forum data on A100 Gen4 x16 (pinned, unidirectional) shows ~24.8 GB/s H2D and ~25.9 GB/s D2H per GPU. RTX 5090 is PCIe 5.0 x16 = 64 GB/s bidirectional (i.e. ~32 GB/s per direction at protocol rate, ~50-55 GB/s achievable unidirectional with encoding/overhead accounted for the way vendors quote 64). Consumer 5090 reviews report ONLY the theoretical 64 GB/s; no primary forum surfaced a single measured 5090 bandwidthTest GB/s this session, so the achieved figure must come from the profiler's own in-container measurement. Bidirectional H2D can also collapse (A100 case: H2D dropped 56%, 24.8 -> ~11 GB/s under concurrent D2H), so unidirectional and bidirectional are different numbers.
- **Applies to:** pcie · **Metric:** Gen3 ~12 GB/s; Gen4 ~25 GB/s; Gen5 theoretical 64 GB/s bidir (~50-55 GB/s achievable unidir) · **Confidence:** medium · **Rig relevance:** 5/5
- **Design implication:** The profiler must MEASURE and report the achieved pinned number; it must never substitute the 64 GB/s theoretical for a measurement. Expect ~50+ GB/s per direction on this rig; if the measured H2D is far below that (e.g. <30 GB/s), flag it (possible x8 link, WSL2 perturbation, or a downclocked link) rather than silently trusting it. Report H2D and D2H separately; do not assume symmetry.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [Asymmetric PCIe bandwidth in bidirectional transfers: H2D drops 56% while D2H maintains (NVIDIA Developer Forums)](https://forums.developer.nvidia.com/t/asymmetric-pcie-bandwidth-in-bidirectional-transfers-h2d-drops-56-while-d2h-maintains-performance/352186) — NVIDIA Developer Forums users 2025; H2D 24.8 GB/s, D2H 25.9 GB/s unidir; H2D 11 GB/s bidir (Gen4 x16); SUPPORTED ; [CUDA C++ Best Practices Guide - PCIe Gen3 pinned bandwidth reference](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html) — NVIDIA Corporation 2026; ~12 GB/s pinned, Gen3 x16; SUPPORTED ; [NVIDIA GeForce RTX 5090 PCI-Express Scaling / spec coverage (theoretical 64 GB/s)](https://www.techpowerup.com/review/nvidia-geforce-rtx-5090-pci-express-scaling/) — TechPowerUp 2025; 64 GB/s bidirectional theoretical (PCIe 5.0 x16); SUPPORTED

### The effective WSL2 GPU-accessible host-memory ceiling tracks the VM's assigned RAM (.wslconfig memory=) · `load-bearing` · constraint
**Evidence points to the WSL2/container GPU-accessible host-memory ceiling being governed by the WSL2 VM's assigned RAM (.wslconfig 'memory='), consistent with the native ~50%-of-RAM behavior scaling with whatever RAM the VM has — not a fixed NVIDIA number.**
The closest documented analog is ROCm-in-WSL2 reporting a GPU pool size derived from VM RAM; the NVIDIA 50%-of-RAM rule is itself RAM-relative. This predicts that a larger WSL2 VM yields a proportionally larger pinnable ceiling — so the figure is a fraction of the VM's RAM, not an absolute.
- **Applies to:** windows-wsl2 · **Metric:** ceiling scales with WSL2 VM RAM (.wslconfig memory=); native rule ~50% of RAM · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** The profiler's RAM-aware probe is correct: it caps at a fraction of the VM's RAM rather than a fixed MB figure. The planner should express the warm-tier budget relative to the measured VM RAM, and note that raising.wslconfig memory= raises the ceiling.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval (existence+groundedness) + family-different (granite4.1:30b: confirmed | mistral-small:24b: confirmed); 0 refutations
- **Sources:** [[Issue]: librocdxg fails to map Dedicated VRAM in WSL2; ROCm pool size is limited by .wslconfig memory setting (ROCm/ROCm Issue #6022)](https://github.com/ROCm/ROCm/issues/6022) — ROCm project / community reporter 2025; SUPPORTED ; [Advanced settings configuration in WSL (.wslconfig memory=)](https://learn.microsoft.com/en-us/windows/wsl/wsl-config) — Microsoft 2026; SUPPORTED ; [What are the pinned memory limitations on CUDA for WSL2?](https://forums.developer.nvidia.com/t/what-are-the-pinned-memory-limitations-on-cuda-for-wsl2/255472) — boxerab (OP) and njuffa, NVIDIA Developer Forums 2023; PARTIAL

### The harsh cap still reproduced as of Jan 2026 (driver 572.83) inside Docker — version/config-bound, not universally fixed · `load-bearing` · benchmark
**The cap is NOT globally fixed: the most recent measured report (microsoft/WSL #14078, 2026-01-17, driver 572.83, WSL 2.4.10) still reproduces ~500 MB single / ~400 MB total pin_memory inside Docker-on-WSL2, and the original 2020 NVIDIA-forum ~300 MB report was confirmed still-blocking in 2021.**
So the cap was real and reproducing on an early-2026 driver in a constraining container config; the issue was closed 2026-01-27 as an automatic stale/no-author-activity close, NOT via a documented Microsoft/NVIDIA fix. The rig's >=22.5 GiB on driver 610.47 is therefore a config/version delta, not evidence the cap was abolished everywhere.
- **Applies to:** windows-wsl2 · **Metric:** ~300 MB (2020) -> ~500 MB single / ~400 MB total (Jan 2026, driver 572.83, Docker) · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Refusing to generalize is the whole point: a rig on 572.83 in a constrained container may still see the harsh cap. The planner must NOT hardcode EITHER 500 MB or 22 GiB — it probes. Record the probe's driver/Docker context in the receipt so a low result on an old stack is explainable, not mysterious.
- **Verify:** verdict=confirmed | oracle retrieval (existence+groundedness) + family-different (granite4.1:30b: confirmed | mistral-small:24b: confirmed); 0 refutations
- **Sources:** [Pinned Memory Allocation Fails Above 500 MB in Docker on WSL2 (Issue #14078)](https://github.com/microsoft/WSL/issues/14078) — microsoft/WSL reporter 2026; SUPPORTED ; [cudaHostAlloc limitations in WSL2 · NVIDIA Developer Forums (thread 142288)](https://forums.developer.nvidia.com/t/cudahostalloc-limitations-in-wsl2/142288) — NVIDIA Developer Forums (user hardvark; moderator rboissel) 2020; SUPPORTED

### The pinned limit is Windows/WDDM-managed, not an NVIDIA driver cap; no official 'lift' changelog exists · `load-bearing` · constraint
**An NVIDIA engineer states the pinned-memory limit is 'entirely managed by Windows' (WDDM<->CUDA interop) and 'the NVIDIA driver doesn't control or set the limit'; no NVIDIA/Microsoft release note (2023-2026) announces raising or lifting it.**
Because the limit is a Windows/WDDM property, there is no NVIDIA driver-version boundary to cite for a 'fix'. The 2020 forum origin gave no mechanism and no fix-version; the limit was long acknowledged but never owned by a numeric NVIDIA commitment.
- **Applies to:** windows-wsl2 · **Metric:** njuffa (NVIDIA): limit 'depends on internal details of the operating system, not CUDA' · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Do NOT claim 'driver X lifted the cap'. Record the measured driver/CUDA/WSL triple as the EMPIRICAL boundary, because NVIDIA provides no official one for cudaHostAlloc. The planner's per-rig probe is the only authority on this rig's ceiling.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval (existence+groundedness) + family-different (granite4.1:30b: confirmed | mistral-small:24b: confirmed/1x cant_confirm (2026-source recency)); 0 refutations
- **Sources:** [What are the pinned memory limitations on CUDA for WSL2? (NVIDIA Developer Forums)](https://forums.developer.nvidia.com/t/what-are-the-pinned-memory-limitations-on-cuda-for-wsl2/255472) — NVIDIA Developer Forums (moderator njuffa) 2023; SUPPORTED ; [Leveling up CUDA Performance on WSL2 with New Enhancements (NVIDIA Technical Blog)](https://developer.nvidia.com/blog/leveling-up-cuda-performance-on-wsl2-with-new-enhancements/) — NVIDIA Corporation 2021; PARTIAL ; [Change limit of 50% for cudaHostAlloc pinned memory on Windows 10/11 (NVIDIA Developer Forums)](https://forums.developer.nvidia.com/t/change-limit-of-50-for-cudahostalloc-pinned-memory-on-windows-10-11/228235) — Robert_Crovella (NVIDIA), forum OP 2022; SUPPORTED ; [cudaHostAlloc limitations in WSL2 (NVIDIA Developer Forums)](https://forums.developer.nvidia.com/t/cudahostalloc-limitations-in-wsl2/142288) — forum OP, rboissel (NVIDIA), alwils 2020; SUPPORTED

### The ~300-500 MB cap is a container locked-memory (RLIMIT_MEMLOCK) + WSL2-PV artifact, not an inherent WSL2/driver ceiling · `load-bearing` · gotcha
**The harsh cap is a CONTAINER / locked-memory artifact, not a WSL2 GPU-driver ceiling: in microsoft/WSL #14078, NATIVE Windows pinned ~4000 MB single / ~5600 MB total on the same rig where the Docker container was held to ~500 MB, and bare (non-container) WSL2 pins small buffers fine.**
The failure localizes to the container path: page-locked allocations are gated by the container's RLIMIT_MEMLOCK and by extra WSL2->WDDM paravirtualization (GPU-PV) machinery between guest and host. memlock ulimits are the repeatedly-cited 'fix' lever (though one #14078 commenter reported memlock=-1 alone didn't lift it — a Docker-Desktop-on-WSL2-specific path). This is why a different container/Docker-Desktop vintage can pin far more.
- **Applies to:** in-container · **Metric:** same rig: native Windows ~4000 MB vs Docker container ~500 MB (#14078, driver 572.83) · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** The pinnable ceiling is a function of (container memlock x WSL2 VM RAM x driver x Docker-Desktop version) — NOT a portable constant. It MUST be probed per-rig/per-container (which the profiler's cudaHostAlloc probe now does); a static assumed number silently corrupts the warm-tier staging budget in either direction.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval (existence+groundedness) + family-different (granite4.1:30b: confirmed | mistral-small:24b: confirmed/1x cant_confirm (2026-source recency)); 0 refutations
- **Sources:** [Pinned Memory Allocation Fails Above 500 MB in Docker on WSL2 (Issue #14078)](https://github.com/microsoft/WSL/issues/14078) — microsoft/WSL reporter 2026; PARTIAL ; [Issues with cudaHostAlloc - Pinned Memory in Container (Issue #226)](https://github.com/NVIDIA/nvidia-container-toolkit/issues/226) — NVIDIA/nvidia-container-toolkit reporter 2023; PARTIAL ; [What are the pinned memory limitations on CUDA for WSL2? (NVIDIA Developer Forums)](https://forums.developer.nvidia.com/t/what-are-the-pinned-memory-limitations-on-cuda-for-wsl2/255472) — NVIDIA Developer Forums (OP + njuffa) 2023; SUPPORTED

### This rig probed >=22.5 GiB pinnable on a 31 GiB VM (>=72%) — exceeding the native 50% rule, consistent with the container being the only gate · `load-bearing` · benchmark
**On driver 610.47 the gpu-container cudaHostAlloc probe succeeded to >=22.5 GiB inside Docker-on-WSL2 (a 31 GiB VM, >=72% of VM RAM) with no failure — exceeding even the Windows-native ~50%-of-RAM cap, consistent with the container layer being the only real gate and the ceiling tracking VM RAM.**
This is ~45x the KB's prior 300-500 MB assumption and above the 50% native rule. It is the empirical override the whole MEASURE-don't-assume thesis predicts: the documented limitation is qualitative, the historical number was a constrained-container artifact, and this rig's actual ceiling is ample. The probe was safety-capped at 75% of VM RAM, so the true ceiling may be higher.
- **Applies to:** windows-wsl2 · **Metric:** >=22.5 GiB / 31 GiB VM (>=72%); vs prior KB 300-500 MB; vs native ~50% rule · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** The warm-tier KV/prefetch staging budget on this rig is AMPLE, not the feared few-hundred MB — a Phase-1 assumption flips. The receipt records >=22.5 GiB (probe-capped lower bound) + the driver/Docker context, and the planner sizes warm-tier staging from the measured value, never the stale assumption.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval (existence+groundedness) + family-different (granite4.1:30b: confirmed | mistral-small:24b: confirmed/1x cant_confirm (2026-source recency)); 0 refutations
- **Sources:** [Change limit of 50% for cudaHostAlloc pinned memory on Windows 10/11 (NVIDIA Developer Forums)](https://forums.developer.nvidia.com/t/change-limit-of-50-for-cudahostalloc-pinned-memory-on-windows-10-11/228235) — NVIDIA Developer Forums 2023; PARTIAL ; [gpu-container Milestone-1 measured baseline (RTX 5090, driver 610.47)](https://github.com/mcp-tool-shop-org/readouts/blob/main/docker-knowledge/baselines/2026-06-04-nvidia-geforce-rtx-5090.json) — gpu-container profiler 2026; SUPPORTED

### Three-axis fio measurement: seq throughput, random IOPS, QD1 latency · `load-bearing` · method
**Correct NVMe characterization needs three distinct fio passes — sequential (large bs, high QD), random IOPS (4k, high QD), and QD1 latency (4k, iodepth=1) — because each isolates a different bottleneck.**
Canonical command shapes (Oracle Block Volume fio reference): SEQUENTIAL THROUGHPUT: fio --filename=<target> --direct=1 --rw=read --bs=256k --ioengine=libaio --iodepth=64 --numjobs=4 --runtime=120 --time_based --group_reporting --name=throughput --readonly. RANDOM IOPS: same but --rw=randread --bs=4k --iodepth=256. LATENCY/QD1: --rw=randread --bs=4k --iodepth=1 --numjobs=1. For the offload profiler, use bs=1M for the sequential ceiling and add a QD4 random pass (iodepth=4) since real offload sits at QD1-4. Always add --ramp_time to discard warm-up and --size >> RAM to defeat the page cache.
- **Applies to:** nvme · **Metric:** seq bs=256k-1M iodepth=64; random bs=4k; latency iodepth=1; QD4 for realistic offload · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Profiler runs two-to-three fio invocations and records each result separately in profile.json (seq_read_gbps, rand_read_qd1_mbps, rand_read_qd4_mbps). Do NOT collapse to a single 'disk bandwidth' number.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [Sample FIO Commands for Block Volume Performance Tests on Linux-Based Instances](https://docs.oracle.com/en-us/iaas/Content/Block/References/samplefiocommandslinux.htm) — Oracle 2024; seq bs=256k iodepth=64; randread bs=4k iodepth=256; latency bs=4k iodepth=1; SUPPORTED ; [fio - Flexible I/O tester documentation (rev 3.41)](https://fio.readthedocs.io/en/latest/fio_doc.html) — Jens Axboe / fio project 2025; bs default 4096; iodepth applies only to async ioengines; PARTIAL

### Under WSL2, NVML utilization + per-process memory are unsupported (N/A); free/total/PCIe/compute-cap are fine · `load-bearing` · gotcha
**The CUDA-on-WSL guide says NVML does not yet support all queries — GPU utilization and active-compute-process queries are unsupported, and per-process GPU memory returns N/A inside WSL2.**
CUDA-on-WSL guide: 'NVML (nvidia-smi) does not support all the queries yet. GPU utilization, active compute process are some queries that are not yet supported. Modifiable state features (ECC, Compute mode, Persistence mode) will not be supported.' Corroborated by nvtop #432: nvidia-smi --query-compute-apps=...,used_gpu_memory returns [N/A] per process under WSL2. What IS reliable: device memory free/total (nvmlDeviceGetMemoryInfo), PCIe link width (nvmlDeviceGetCurrPcieLinkWidth), and compute capability (nvmlDeviceGetCudaComputeCapability).
- **Applies to:** in-container · **Metric:** utilization + per-process mem = unsupported/N/A under WSL2 · **Confidence:** high
- **Design implication:** Profiler may trust NVML free/total VRAM, PCIe link width, and compute capability inside the WSL2 container, but must skip/flag GPU-utilization and per-process-memory fields as unavailable rather than recording zeros or N/A as real data.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [CUDA on WSL User Guide — NVML/nvidia-smi support limitations](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA 2025; SUPPORTED ; [WSL2: nvtop shows incorrect GPU memory and per-process memory N/A (Syllo/nvtop #432)](https://github.com/Syllo/nvtop/issues/432) — Syllo/nvtop contributors 2024; per-process mem = N/A; 17179869184 bytes mis-shown as GiB; SUPPORTED

### Use large transfers + warmup + median to saturate the link · `load-bearing` · method
**Per-call overhead dominates small transfers, so a stable, link-saturating measurement requires large buffers (tens to hundreds of MB), a warmup copy, and a median over repeated runs.**
Best Practices: 'batching many small transfers into one larger transfer performs significantly better than making each transfer separately.' bandwidthTest's default 16 MB already amortizes setup cost; for a Gen5 link that moves ~50 GB/s, a 16 MB copy completes in ~0.3 ms, so use >=64-256 MB to make the timed region large relative to launch/WDDM submission latency and to fully ramp the link. Discard the first (cold) copy as warmup, then take median of N (>=5) to reject WDDM scheduling jitter. Faster links need larger buffers to leave the small-transfer-overhead regime.
- **Applies to:** all · **Metric:** >=64-256 MB buffer; median of >=5 runs after 1 warmup · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** measure_bandwidth() should use a >=64 MB (ideally 128-256 MB) pinned buffer, do one untimed warmup copy per direction, then time >=5 copies and report the median GB/s (not the max, not the mean). Scale buffer size up if the measured time is below ~1 ms.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [CUDA C++ Best Practices Guide - Batching Transfers](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html) — NVIDIA Corporation 2026; ~12 GB/s pinned Gen3 x16 reference figure; SUPPORTED ; [How to Optimize Data Transfers in CUDA C/C++ (NVIDIA Technical Blog)](https://developer.nvidia.com/blog/how-optimize-data-transfers-cuda-cc/) — Mark Harris, NVIDIA 2012; 16 MB default transfer size; SUPPORTED

### Use nvmlDeviceGetMemoryInfo_v2 so 'reserved' VRAM is not counted as 'used' · `load-bearing` · gotcha
**The v1 nvmlDeviceGetMemoryInfo folds driver-reserved VRAM into the 'used' field, so v1 'free' under-reports and v1 'used' over-reports; v2 exposes reserved separately.**
nvmlDeviceGetMemoryInfo_v2 returns nvmlMemory_v2_t which adds a 'reserved' field. In v1, reserved memory is included in 'used', so on a 32 GB card you can see a chunk already 'used' on a fresh boot. Prefer v2 to get an honest free number and a separate reserved accounting; fall back to v1 only if the driver is too old to expose v2.
- **Applies to:** vram · **Metric:** v2 adds a 4th field: reserved · **Confidence:** high
- **Design implication:** Profiler calls nvmlDeviceGetMemoryInfo_v2 when available and records reserved separately from used; the 'usable VRAM' figure in profile.json is v2.free, not (total - v1.used).
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [NVML API Reference Guide — Device Queries (nvmlDeviceGetMemoryInfo_v2)](https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceQueries.html) — NVIDIA 2024; reserved field added in v2; SUPPORTED

### WSL2 collapses the pinnable host-RAM ceiling to a few hundred MB · `load-bearing` · constraint
**Under WSL2 (including Docker-on-WSL2), cudaHostAlloc/pin_memory fails far below the native limit — reproducibly at roughly 300-500 MB versus several GB on native Linux/Windows.**
Two independent primary reports: an NVIDIA dev-forum thread says cudaHostAlloc 'starts failing at roughly 300MB' in WSL while native Linux handles multiple GB; microsoft/WSL issue #14078 reports PyTorch pin_memory() failing above ~500 MB single / 400-500 MB total inside Docker on WSL2 (driver 572.83, WSL 2.4.10, Ubuntu 22.04) vs 4 GB native. Privileged mode, ulimits.memlock=-1, and bigger shm did NOT lift the ceiling — it is a WSL2/driver limitation, not a container ulimit.
- **Applies to:** windows-wsl2 · **Metric:** ~300-500 MB pinnable in WSL2 vs 4 GB native · **Confidence:** high
- **Design implication:** On this WSL2 rig the profiler MUST NOT assume a large pinnable buffer. Empirically probe with an escalating cudaHostAlloc loop (alloc, free, record last success); if probing is unavailable, default the pinnable ceiling to a conservative ~256-512 MB and set a 'wsl2_pinned_limited: true' flag in profile.json so any pinned-transfer bandwidth estimate is honest.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [Pinned Memory Allocation Fails Above 500 MB in Docker on WSL2 (microsoft/WSL #14078)](https://github.com/microsoft/WSL/issues/14078) — microsoft/WSL contributors 2025; 500 MB (Docker/WSL2) vs 4 GB (native); driver 572.83; SUPPORTED ; [cudaHostAlloc limitations in WSL2 — NVIDIA Developer Forums](https://forums.developer.nvidia.com/t/cudahostalloc-limitations-in-wsl2/142288) — NVIDIA Developer Forums (user report, NVIDIA staff rboissel engaged) 2020; ~300 MB pinnable in WSL2; SUPPORTED

### WSL2/WDDM caps pinned memory LOWER than native Windows (~50% RAM, less under WSL2) · `load-bearing` · constraint
**cudaHostAlloc pinning is capped by Windows at ~50% of system RAM, and that cap is even LOWER under WSL2 due to extra WDDM machinery -- so a large pinned buffer can fail inside the container.**
NVIDIA staff (Robert_Crovella): 'The limit is entirely managed by Windows, and a typical limit is 50% of system memory' and 'the pinning limits on WSL2 are likely to be lower than what you would observe strictly on the windows side.' njuffa measured the largest successful pinned alloc on a 32 GB box at ~15.04 GB (47%). The CUDA-on-WSL User Guide independently states: 'Pinned system memory... availability for applications is limited' and apps that exceed it 'may not work.' On this 64 GB rig that implies ~30 GB pinnable on native Windows and less under WSL2 -- and the profiler's test allocation must stay well under that. Note this is the HOST pinned-RAM cap, separate from the 32 GB VRAM budget.
- **Applies to:** windows-wsl2 · **Metric:** ~50% RAM native Windows (15.04 GB of 32 GB measured); lower under WSL2 · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** measure_bandwidth() must use a modest pinned buffer (hundreds of MB, not multi-GB) and wrap cudaHostAlloc/cudaMallocHost in error handling for cudaErrorMemoryAllocation -- on failure, shrink the buffer and retry, or fall back to a pageable measurement with a flag. Never size the pinned test buffer as a fraction of total RAM.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [Change limit of 50% for cudaHostAlloc pinned memory on Windows 10/11 (NVIDIA Developer Forums)](https://forums.developer.nvidia.com/t/change-limit-of-50-for-cudahostalloc-pinned-memory-on-windows-10-11/228235) — Robert_Crovella, njuffa (NVIDIA Developer Forums) 2022; ~50% of RAM; 15.04 GB of 32 GB (47%) measured; WSL2 lower; SUPPORTED ; [CUDA on WSL User Guide - Features Not Yet Supported / pinned memory](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA Corporation 2026; qualitative: pinned availability 'limited'; SUPPORTED

### WSL2: measure on the ext4 vdisk, never /mnt/c (9p/drvfs is ~5-10x slower) · `load-bearing` · gotcha
**Inside a WSL2 Linux container, benchmarking a /mnt/c (drvfs/9p) path reports NVMe bandwidth 5-10x lower than reality; the test path must live on the Linux ext4 vdisk (or a volume bind-mounted from it).**
Microsoft's WSL filesystem doc explicitly recommends against working across OSes and to store files in the Linux fs (/home/<user>/...), not /mnt/c, for fastest speed. Cross-OS access goes through the 9p protocol (serialize -> virtual transport -> deserialize), reported across multiple sources as ~5-10x slower than native ext4 (WSL issue #4197: '/mnt over 10x slower than native WSL2 filesystem'; community measurements ~9x). Docker Desktop on the WSL2 backend stores its data on the ext4 vdisk by default, so a named volume or a bind mount rooted on the WSL distro's filesystem is on fast ext4 — but a bind mount of a Windows path (/mnt/c/...) is on slow drvfs.
- **Applies to:** windows-wsl2 · **Metric:** /mnt/c via 9p ~5-10x slower than native WSL2 ext4 (issue #4197: >10x) · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Profiler refuses (or loudly warns) if its fio target resolves to a /mnt/<letter> drvfs path; it must place the test file on the ext4 vdisk / a WSL-rooted volume. Record which filesystem was measured in profile.json so the receipt is auditable.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [Working across file systems (WSL)](https://learn.microsoft.com/en-us/windows/wsl/filesystems) — Microsoft 2025; store on Linux fs, not /mnt/c, for fastest speed; SUPPORTED ; [[wsl2] filesystem performance is much slower than wsl1 in /mnt (issue #4197)](https://github.com/microsoft/WSL/issues/4197) — microsoft/WSL contributors 2019; >10x slower for /mnt vs native ext4; SUPPORTED ; [WSL2 I/O measurements (WSL1 vs WSL2, local and host files)](https://vxlabs.com/2019/12/06/wsl2-io-measurements/) — Charl Botha (vxlabs) 2019; ~5x slower for WSL2 host-file (/mnt) access; SUPPORTED

### direct=1 + libaio is mandatory to bypass the page cache · `load-bearing` · technique
**Without --direct=1 (and a test size larger than RAM) fio measures the OS page cache, not the NVMe — and libaio queueing only works with non-buffered I/O.**
fio docs: 'If value is true, use non-buffered I/O. This is usually O_DIRECT' and for libaio 'Linux may only support queued behavior with non-buffered I/O (set direct=1 or buffered=0).' So the offload benchmark MUST set direct=1 AND use ioengine=libaio together. Belt-and-suspenders: also make --size far exceed the 64 GB host RAM so even a buffered fallback can't be fully served from cache. Use ramp_time to drop the first seconds.
- **Applies to:** nvme · **Metric:** test file size > 64 GB RAM on this rig · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Profiler hardcodes --direct=1 --ioengine=libaio and sizes the test file > RAM. If it ever has to fall back to direct=0, it must flag the result as page-cache-contaminated and untrustworthy, not report it as disk bandwidth.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [fio - Flexible I/O tester documentation (rev 3.41)](https://fio.readthedocs.io/en/latest/fio_doc.html) — Jens Axboe / fio project 2025; libaio requires direct=1/buffered=0 for queued behavior; PARTIAL

### nvidia-smi/NVML is degraded under WSL2: pcie.link.gen/width often N/A -- do not trust as ground truth · `load-bearing` · gotcha
**Under WSL2 the NVML backend behind nvidia-smi does not support all queries; pcie.link.gen / pcie.link.width and several utilization fields commonly return N/A or are unreliable inside the container.**
CUDA-on-WSL User Guide: 'NVML (nvidia-smi) does not support all the queries yet. GPU utilization, active compute process are some queries that are not yet supported.' Forum/issue reports add that pcie.link.gen.current / pcie.link.width.current frequently show N/A in the virtualized WSL2 environment, and there are NVML init failures inside Docker-in-WSL2 ('Failed to initialize NVML: GPU access blocked by the operating system') depending on driver/toolkit vintage. Even on bare metal these link fields legitimately downclock at idle (link drops to lower gen/width to save power), so the queried value is not a reliable statement of capability anywhere.
- **Applies to:** in-container · **Metric:** pcie.link.gen/width => N/A in WSL2; NVML queries partially unsupported · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** The profiler must DERIVE the effective PCIe capability from MEASURED bandwidth, not from nvidia-smi --query-gpu=pcie.link.gen.current,pcie.link.width.current. Capture those fields advisory-only and explicitly flag/handle N/A; never let a missing or downclocked pcie field block or skew the bandwidth receipt. Confirm NVML actually initializes inside the container at startup and degrade gracefully if it does not.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [CUDA on WSL User Guide - NVML/nvidia-smi unsupported queries](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA Corporation 2026; qualitative: subset of NVML queries unsupported in WSL2; SUPPORTED ; [nvidia-smi pcie.link.gen / pcie.link.width current values (NVIDIA Developer Forums + WSL issue corroboration)](https://forums.developer.nvidia.com/t/setting-locking-pcie-link-configuration/216723) — NVIDIA Developer Forums users 2022; link gen/width downclock at idle; N/A under WSL2; PARTIAL ; [In WSL2's docker container: GPU access blocked by the operating system (microsoft/WSL #9962)](https://github.com/microsoft/WSL/issues/9962) — microsoft/WSL contributors 2023; qualitative: NVML init failure in Docker-in-WSL2; SUPPORTED

### Fragmentation is invisible in free/total; probe the largest contiguous block, not the sum · `supporting` · method
**Total free VRAM is not the same as the largest allocatable contiguous block; cudaMalloc can fail despite ample total-free, so fragmentation must be probed, not inferred from NVML free.**
Each cudaMalloc is an independent allocation that can never merge with another, so a live block wedged between free blocks prevents a large contiguous alloc even when NVML 'free' looks big. There is NO official NVML 'largest free block' API. Practical probe: binary-search a single cudaMalloc downward from NVML-free until it succeeds (record the largest success), or inspect PyTorch's torch.cuda.memory_snapshot() segment/block layout. Crucially, a FRESH container with no other GPU process has ~0 fragmentation, so for the profiler's clean-room vantage NVML free is a good proxy and a single confirmatory cudaMalloc near NVML-free is enough.
- **Applies to:** vram · **Metric:** no NVML largest-block field; cudaMalloc can fail with free>request · **Confidence:** medium
- **Design implication:** In its fresh container the profiler can treat NVML v2.free as usable VRAM, optionally validate with ONE large cudaMalloc-then-free probe; it should not attempt to derive a fragmentation number from NVML totals (no such field exists) and should note that fragmentation only matters when a model engine is already resident.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [When does fragmentation occur in the CUDA caching allocator? — PyTorch DevLog](https://docs.pytorch.org/devlogs/eager/2026-06-01-cuda-caching-allocator/) — PyTorch (Zachary DeVito et al.) 2026; PARTIAL ; [A guide to PyTorch's CUDA Caching Allocator](https://zdevito.github.io/2022/08/04/cuda-caching-allocator.html) — Zachary DeVito 2022; PARTIAL

### Native Windows pins ~50% of system RAM; WSL2 is lower (NVIDIA-confirmed) · `supporting` · benchmark
**On native Windows the cudaHostAlloc pinnable ceiling is ~50% of system RAM (WDDM-imposed), and NVIDIA staff state WSL2 limits are lower than the Windows-side number.**
NVIDIA's Robert_Crovella: 'The limit is entirely managed by Windows, and a typical limit is 50% of system memory' and 'the NVIDIA driver doesn't control or set the limit.' Measured by njuffa: max successful pin = 15.04 GB on a 32 GB system = 47%. Crovella added the WSL2 ceiling is 'likely to be lower than what you would observe strictly on the windows side' due to extra WSL2-to-WDDM machinery. So even the optimistic Windows half-of-RAM figure is an UPPER bound the WSL2 container will not reach.
- **Applies to:** windows-wsl2 · **Metric:** ~50% of RAM native Windows (measured 47% / 15.04 GB on 32 GB); WSL2 lower · **Confidence:** high
- **Design implication:** Profiler may record the Windows-native ~50% figure as context, but the in-container pinnable ceiling it writes to profile.json must come from its own probe, which will land far below 50% of the 64 GB host on this rig.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [Change limit of 50% for cudaHostAlloc pinned memory on Windows 10/11 — NVIDIA Developer Forums](https://forums.developer.nvidia.com/t/change-limit-of-50-for-cudahostalloc-pinned-memory-on-windows-10-11/228235) — NVIDIA Developer Forums (Robert_Crovella, NVIDIA; njuffa) 2022; 50% RAM (Windows); 15.04 GB / 47% measured on 32 GB; WSL2 lower; SUPPORTED

### WDDM submission latency penalizes WSL2 vs bare-metal Linux on small/short work · `supporting` · gotcha
**WSL2 runs the GPU through the Windows WDDM driver, adding launch/submission latency and memory-allocation overhead, so short or small-transfer measurements are slower and noisier inside WSL2 than on native Linux.**
The CUDA-on-WSL guide and NVIDIA's 'Leveling up CUDA Performance on WSL2' blog document that the gap between native Linux and WSL2 grows when the submitted work is too short to overcome per-launch latency, and that memory allocation overhead and CPU-side launch cost are the main WSL2 penalties. A user-reported data point: identical app at 19 ms/frame on WSL2/native Windows vs 11 ms/frame on bare-metal Linux. This is exactly the regime a naive small-buffer or single-shot bandwidth test would fall into, producing an artificially low and unstable number that does not reflect the link.
- **Applies to:** windows-wsl2 · **Metric:** 11 ms (bare Linux) vs 19 ms/frame (WSL2/Windows) app-level · **Confidence:** medium · **Rig relevance:** 4/5
- **Design implication:** Reinforces the large-buffer + warmup + median policy: measure_bandwidth() must amortize WDDM submission latency by using big transfers and discarding the cold run, and should treat the in-container number as the honest vantage (it is what the engine will actually see) rather than trying to back out a 'true bare-host' figure. Optionally record that the measurement was taken under WSL2 so the receipt is self-describing.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [Leveling up CUDA Performance on WSL2 with New Enhancements (NVIDIA Technical Blog)](https://developer.nvidia.com/blog/leveling-up-cuda-performance-on-wsl2-with-new-enhancements/) — NVIDIA 2021; qualitative: gap grows as submitted work shrinks below latency threshold; SUPPORTED ; [What are the pinned memory limitations on CUDA for WSL2? (NVIDIA Developer Forums)](https://forums.developer.nvidia.com/t/what-are-the-pinned-memory-limitations-on-cuda-for-wsl2/255472) — NVIDIA Developer Forums users 2023; 19 ms/frame WSL2 vs 11 ms/frame bare-metal Linux; SUPPORTED

### WSL2 GPU CUDA caveats don't cover disk — profiler owns disk fidelity · `supporting` · constraint
**NVIDIA's CUDA-on-WSL guide documents GPU/pinned-memory caveats but says nothing about disk I/O, so the burden of measuring NVMe truthfully from inside the WSL2 container falls entirely on the profiler's own discipline.**
The CUDA on WSL User Guide documents pinned-system-memory limits, no full managed/unified-memory support, and no concurrent CPU/GPU access under WSL2 — relevant to the broader profiler but it provides zero guidance on disk/filesystem measurement. There is no vendor-blessed disk-benchmark path for WSL2 containers; the profiler must self-enforce the overlay/9p avoidances above and self-document what it measured.
- **Applies to:** windows-wsl2 · **Metric:** no disk-I/O guidance in CUDA-on-WSL guide · **Confidence:** medium · **Rig relevance:** 4/5
- **Design implication:** Don't expect a vendor tool to validate the disk number. The profiler must self-assert mount type + filesystem and embed those assertions in the profile.json receipt so the +/-10% honesty claim is auditable rather than assumed.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [CUDA on WSL User Guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA 2025; pinned-memory limited; managed memory unsupported on WSL2; SUPPORTED

### WSL2 is more restrictive than native Windows because of GPU-PV (paravirtualization) between guest and WDDM · `supporting` · constraint
**NVIDIA explicitly attributes WSL2's lower pinning to extra 'WSL2->WDDM machinery' — GPU paravirtualization (GPU-PV) sitting between the guest and the host WDDM driver is the named mechanism that historically made WSL2 pinning lower than native Windows.**
This is the mechanistic 'why WSL2 < native' — distinct from the container memlock gate. It explains the directional rule (WSL2 historically <= native) without fixing a number, and is consistent with improvements when the paravirtualization/container path is upgraded (see the R595 container support).
- **Applies to:** windows-wsl2 · **Metric:** qualitative: GPU-PV adds a guest->host WDDM hop · **Confidence:** high · **Rig relevance:** 3/5
- **Design implication:** Reinforces that the ceiling is a stack property (guest VM + GPU-PV + WDDM + container), so it is measured from inside the actual container, the only vantage that sees the whole stack.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval (existence+groundedness) + family-different (granite4.1:30b: confirmed | mistral-small:24b: confirmed/1x cant_confirm (2026-source recency)); 0 refutations
- **Sources:** [Change limit of 50% for cudaHostAlloc pinned memory on Windows 10/11 (NVIDIA Developer Forums)](https://forums.developer.nvidia.com/t/change-limit-of-50-for-cudahostalloc-pinned-memory-on-windows-10-11/228235) — Robert_Crovella (NVIDIA) 2022; PARTIAL ; [GPU paravirtualization (Windows Drivers documentation)](https://learn.microsoft.com/en-us/windows-hardware/drivers/display/gpu-paravirtualization) — Microsoft 2024; PARTIAL

