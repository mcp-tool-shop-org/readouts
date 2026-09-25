# Container & runtime layer
_Docker + NVIDIA Container Toolkit + WSL2 GPU passthrough; base images; CUDA toolkit; what changes inside a container (the "Docker" lane)_ · wave 9 · 2026-09-07 · [‹ catalog index](README.md)

69 findings · 7 load-bearing · 15 verified.

| Kind | Finding | Claim | Metric | Applies to | Conf | ✓ |
|------|---------|-------|--------|------------|------|---|
| craft | A comprehensive evaluation of spatial co-execution on GPUs using MPS and MIG technologies | Evaluates **MPS** (flexible SM share, memory contention) vs **MIG** (full isolation) including **Blackwell B200** among Ampere/Hopper/Blackwell — profile before choose (wave-06 69 deepen). |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Absences on CDI support page | **Absent:** string “Blackwell”; sm_120 / CUDA 12.8 image floor; MPS sharing policy; decisive_axis language. Blackwell MIG mins live on MIG guide; CDI page only notes MIG **reconfig → manual regenerate**. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | CDI SPEC.md | Vendor JSON (`cdiVersion`, `kind`, `devices[].name`, `containerEdits`: env/deviceNodes/mounts/hooks/additionalGIDs). Well-known paths `/etc/cdi`, `/var/run/cdi`. Explains what `nvidia.yaml` must satisfy — not NVIDIA GPU-specific. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | CIR: Lightweight Container Image for Cross-Platform Deployment | Lazy-builder assembles OCI with CNI plus **NVIDIA Container Toolkit**; reuses GPU components via **libnvidia-container** — toolkit inject as portable GPU package craft. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| analog | CNCF Container Device Interface (CDI) | Runtime-agnostic device package via JSON/YAML specs; does not invent a new gpu-container decisive axis. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | CRIUgpu — CDI + NVIDIA Container Toolkit | GPU container checkpoint/restore integrates CDI + NVIDIA Container Toolkit; libnvidia-container injects devices/libs — package surface is CDI/toolkit, not image-baked drivers. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | CRIUgpu: Transparent Checkpointing of GPU-Accelerated Workloads | GPU container C/R integrates **CDI** and the **NVIDIA Container Toolkit**; libnvidia-container injects devices/libraries into the mount namespace — CDI+toolkit as the package surface (not an invented axis). |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | CUDA C++ Best Practices (theoretical vs effective) | Analog: theoretical link rate != effective measured bandwidth. Holds PCIe honesty. Limit: guide != invent 5090 GB/s. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | CUDA Compatibility (forward / minor) | Analog: toolkit/app can run across driver versions under defined forward/minor rules. Holds for toolkit-currency pins (image/toolkit match arch). Limit: compat matrix ≠ inventing a new axis. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Compose GPU devices | Place GPUs via deploy.resources.reservations.devices; capabilities:[gpu] mandatory; count and device_ids mutually exclusive. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | Compose GPU support | Compose GPU path: **driver: nvidia**, capabilities [gpu]; example nvidia/cuda:12.9.0-base-ubuntu22.04 — dated Compose package currency. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Compose deploy devices spec | Device reservations require capabilities; count/device_ids exclusive. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | Container Device Interface SPEC | Analog: OCI runtimes inject third-party devices via CDI edits (nodes/hooks beyond a bare device node). Holds for wave-06 CDI package path. Limit: CDI ≠ a new gpu-container decisive_axis. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Container Device Interface SPEC | Analog: CNCF CDI device inject via containerEdits/OCI transform. Holds CDI path. Limit: CDI SPEC != new decisive_axis. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Dissecting the NVIDIA Blackwell Architecture with Microbenchmarks | **CUDA 12.8** and **PTX 8.7** expand support for Blackwell 5th-gen tensor instructions (`tcgen05`); older wgmma/FP8 paths are not Blackwell-compatible — toolkit/PTX currency gate (omit STUDY-028’s other Blackwell microbench). |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Docker Engine --gpus | Expose with docker run --gpus all or device=<index/UUID>; requires NVIDIA driver + toolkit on the host. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | Docker Engine 28.2.0 release notes | Docker Engine **28.2.0** dated **2025-05-28**; **CDI enabled by default** — Engine CDI default currency beyond STUDY-028/048/049. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Docker Engine 28.x release notes | Dated Engine patches: **28.4.0** 2025-09-03; **28.5.2** 2025-11-05 — package currency trail (Axis invented: 0; Numbers invented: 0). |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Docker Engine GPU access (`--gpus`) | Analog: expose GPUs via `--gpus` when host has driver + toolkit. Holds for Engine place alongside CDI. Limit: flag presence ≠ honest isolation (MIG vs share). |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| docs | Docker container run — CDI devices | CDI on by default for Linux; place via --device=<fully-qualified CDI name>. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | Dockerfile FROM pin | Analog: pin tag or digest; omit tag implies latest. Holds Dockerfile digest honesty. Limit: digest pin != NVML honesty. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | ElastiCo: Elastic Configuration and Interference-Aware Orchestration for GPU Clusters | Kubernetes-native middleware for training/inference co-location; when MPS is enabled, sets per-client CUDA_MPS_PINNED_DEVICE_MEM_LIMIT and profiles with MPS disabled — place/package under MPS, not inventing a singleton axis or farm numbers. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | EnclaveX: End-to-End Confidential AI with CPU/GPU TEEs | End-to-end CPU+GPU TEEs with **confidential containers** on Kubernetes and NVIDIA Hopper/H200 confidential GPU via CVM-contained driver — confidential package boundary deepen, not a new catalog axis. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Gaps (on-page) | Refresh auto-path misses MIG geometry changes; CDI schema v0.7.0 vs old engines needs feature-flag; no toolkit page equates generate to Blackwell compute readiness. Do not invent axis. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Gaps vs still-current package catalog | Meta Gaps: CTK **1.20.0** + Docker CDI default **28.2** + Compose nvidia path; Axis invented: 0; Numbers invented: 0 — no invent axis/numbers. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Getting Started with MIG | **B200** MIG: CUDA 12, driver **R570≥570.133.20**; **RTX PRO Blackwell** editions: R575+. Container path: CTK ≥v2.5.0-era; `NVIDIA_VISIBLE_DEVICES` / `--gpus` MIG UUID formats. **MPS+MIG:** per-MIG `CUDA_MPS_PIPE_DIRECTORY`; EXCLUSIVE_PROCESS not with MIG. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Getting Started with MIG | MIG container path: Container Toolkit / nvidia-docker2 **v2.5.0+**; B200/R570 floors on-page — MIG container currency, not invent axis. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | HPC Containers for EBRAINS: Towards Portable Cross-Domain Software Environment | GPU containers still bind host drivers/libraries (ABI across boundary); deliberately builds against older **CUDA 12.2** for newer host drivers — CUDA currency / ABI gate without crowning an axis. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Install guide | UNVERIFIED install-guide 1.20.0-1 pin — do not treat as verified. Pin packages `NVIDIA_CONTAINER_TOOLKIT_VERSION=1.20.0-1`; `nvidia-ctk runtime configure --runtime=docker` rewrites daemon.json. Podman: prefer CDI. Config: `nvidia-ctk config --in-place --set …`. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | K8s schedule GPUs | Expose vendor device resources (nvidia.com/gpu) and schedule via limits=requests. Holds for honest device placement; limit: cluster ≠ single-card. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | KIS-S: A GPU-Aware Kubernetes Inference Simulator with RL-Based Auto-Scaling | GPU-aware K8s inference simulator on MicroK8s + single NVIDIA GPU; contrasts default **HPA** (CPU/memory) vs GPU metrics via Prometheus/DCGM Exporter — autoscaling currency for containerized GPU services. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| analog | Kubernetes Resource Quotas — GPU capacity caps | Hard requests.nvidia.com/gpu caps are absolute. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | Leveraging Multi-Instance GPUs through moldable task scheduling | MIG on Ampere/Hopper/**Blackwell**; contrasts MPS SM-share vs MIG isolated compute+memory; B100/B200 keep A100/H100-style MIG slice limits — MIG schedule craft under reconfiguration constraints. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | MIG User Guide | Analog: partition GPU into **isolated** instances with dedicated compute/memory. Holds for place craft when isolation is required. Limit: MIG hardware profiles ≠ Compose syntax alone. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | MedFoundationHub: A Lightweight and Secure Toolkit for Deploying Medical Vision Language Foundation Models | On-prem VLM toolkit with **Docker-orchestrated** inference/workload plane (Dockerfile to isolated containers) on a single NVIDIA workstation GPU — package surface is containerized local deploy, not a new decisive axis. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Multi-Process Service (MPS) | Analog: **shared** co-operative CUDA multi-process scheduling for utilization. Holds as the share/time-slice class adjacent to place. Limit: MPS share ≠ MIG isolation guarantees. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | NVIDIA CDI support | From toolkit v1.12.0 CDI specs; v1.18.0 nvidia-cdi-refresh auto-writes nvidia.yaml; devices nvidia.com/gpu=all/0/…. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | NVIDIA CDI support | Analog: from toolkit v1.12.0, `nvidia-ctk cdi generate` writes host-driver injection (`nvidia.com/gpu=…`, MIG names). Holds for toolkit-currency → CDI → runtime. Limit: generate on host ≠ image-baked drivers. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | NVIDIA CDI support (analog) | Analog: CDI generate **v1.12.0**; nvidia-cdi-refresh **v1.18.0**. Holds CDI toolkit inject pin. Limit: generate on host != invent decisive_axis. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | NVIDIA CTK install guide | Install packages then nvidia-ctk runtime configure --runtime=docker rewriting daemon.json — host-side prerequisite before --gpus. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| docs | NVIDIA CTK specialized configs — IMEX channels | NVIDIA_IMEX_CHANNELS requests host IMEX channels; CDI validates channel nodes. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| craft | NVIDIA Container Toolkit latest index | Docs branded **1.20.0** tip tree — CTK currency pin for still-current docker package path. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | NVIDIA Container Toolkit release notes | Tip **1.20.0**; **1.18.0** JIT-CDI + nvidia-cdi-refresh; **1.19.1** CDI schema **v0.7.0** needs docker>=26.1.0 — dated CTK currency (Axis invented: 0; Numbers invented: 0). |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | NVIDIA k8s-device-plugin | Analog: DaemonSet advertises/allocates device nodes + health; host driver stays outside the image. Holds for toolkit inject pattern. Limit: cluster plugin ≠ single-host Docker CDI only. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Performance Characterization of Containerized DNN Training and Inference on Edge Accelerators | Compares **Docker** vs bare-metal DNN train/infer on Jetson-class edges; notes CUDA MPS/MIG as related sharing mechanisms — containerization overhead craft without crowning an axis. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Private LLM Inference on Consumer Blackwell GPUs: A Practical Guide for Cost-Effective Local Deployment in SMEs | Releases a **Docker image** (vLLM/AIPerf/DCGM stack); requires NVIDIA **driver 570.x+**, **CUDA 12.9**, cuDNN 9.x for NVFP4 on consumer Blackwell — currency pin for image/driver/CUDA match (no invented measured numbers here). |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Q-GEAR: Improving quantum simulation framework | Deploys **Podman** container plus NERSC **NVIDIA public image** for Cuda-Q GPU simulation — Podman/NVIDIA image package path adjacent to Docker toolkit inject. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Release notes | UNVERIFIED install-guide 1.20.0-1 pin — do not treat as verified. **1.18.0**: auto CDI refresh systemd + default JIT-CDI. **1.19.1**: CDI schema **v0.7.0** default (needs containerd≥1.7.16 / docker≥26.1 / podman≥5.1); `--feature-flag no-additional-gids-for-device-nodes` for older; MIG `/dev/dri*` injection. **1.20.0**: app-profile hook, WSL2 broader discovery. Generate loads select `config.toml` settings. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | SPEC CPU 2017 Overview | Analog: honest data vs marketing hype; SPECspeed != SPECrate. Holds measurement honesty. Limit: SPEC suites != invent tok/s. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Scalable APT Malware Classification via Parallel Feature Extraction and GPU-Accelerated Learning | Repro path: install toolkit then `nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml`, run Podman with `--device nvidia.com/gpu=all` — names **cdi generate** as the compose contract. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Seekable OCI: Lazy-Loading Container Images via Range-Request Indexing | SOCI lazy-loads unmodified **OCI** images; production path notes EKS Auto Mode uses SOCI parallel pull for **GPU instances** — image-pull package craft for GPU pods (no invented axis). |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Semantic Versioning | Analog: MAJOR.MINOR.PATCH; MUST NOT mutate released versions. Holds SemVer package pin. Limit: SemVer != invent GB/s. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Subedar — nvidia-ctk cdi generate contract | Repro path: nvidia-ctk cdi generate then Podman --device nvidia.com/gpu=all — CDI generate as compose/runtime attach contract. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| craft | Support for CDI | CDI generate since **v1.12.0**. From **v1.18.0**: `nvidia-cdi-refresh` writes `/var/run/cdi/nvidia.yaml` on toolkit/driver install/upgrade and reboot. Knobs: `nvidia-ctk cdi list`; manual `nvidia-ctk cdi generate --output=/var/run/cdi/nvidia.yaml`; env overrides in `/etc/nvidia-container-toolkit/nvidia-cdi-refresh.env`. **Known limits:** refresh does **not** handle driver removal or **MIG reconfiguration** — regenerate manually. Devices: `nvidia.com/gpu=all`, `=0`, MIG e.g. `nvidia.com/gpu=1:0`. JIT-CDI + `--disable-hook`. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Support for CDI | CDI generate since **v1.12.0**; auto refresh **v1.18.0**; example status Fri 2025-06-27; MIG reconfig requires manual regen — CDI pin craft, not invent axis. |  | docker; container-runtime; CDI; CTK; package-pin | ●●· | · |
| craft | Taming GPU Underutilization via Static Partitioning and Fine-grained CPU Offloading | Frames MPS (compute-only partition) vs MIG (compute+memory) as spatial-sharing options with different isolation/flexibility; includes B200 capacity table — underutilization/partition craft, not a singleton axis invent. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | Troubleshooting | CDI inject survives cgroup updates better than legacy hook. Generate flags: `--feature-flag no-additional-gids-for-device-nodes`; refresh env `NVIDIA_CTK_CDI_GENERATE_FEATURE_FLAGS=…`. |  | docker; nvidia-ctk; CDI; MIG; MPS | ●●· | · |
| craft | k8s-device-plugin — host inject analog | DaemonSet injects device nodes + health; host driver not in the image. Holds for NVIDIA Container Toolkit --gpus injection; limit: k8s ≠ Docker CDI on WSL2. |  | docker; nvidia-ctk; gpu-container | ●●● | · |
| docs | nvidia-container-toolkit v1.20.0 release | IMEX channel validation in CDI/JIT-CDI; application-profile CDI hook limiting EGL/Vulkan to assigned GPUs. |  | docker; nvidia-ctk; gpu-container | ●●● | ✓ |
| constraint | Even on Linux, UVM oversubscription is wrong for decode | On-demand page-migrated UVM collapses effective bandwidth by orders of magnitude — fatal for bandwidth-bound decode. | up to 100x variation; ~8-10 -> ~1 GB/s at 2x oversub; random to hundreds of KB/s | linux; windows-wsl2 | ●●● | ✓ |
| constraint | No CUDA UVM oversubscription on Windows/WSL2 | Full managed-memory oversubscription is unavailable on Windows native and WSL2 by driver design (WDDM). | cudaDevAttrConcurrentManagedAccess == 0 on Windows/WSL/Tegra | windows-wsl2 | ●●● | ✓ |
| gotcha | cuda-128-minimum-for-sm120-image | On Blackwell sm_120 the in-image CUDA toolkit must be >=12.8 or compute fails ('device kernel image is invalid') even though nvidia-smi reports a higher CUDA and runs fine. | CUDA 12.8 = minimum toolkit for Blackwell sm_120 | in-container | ●●● | ✓ |
| constraint | devel-image-required-for-cudaMemcpy-bench | A cudaMemcpy bandwidth benchmark must be compiled with nvcc, which only exists in the nvidia/cuda:*-devel image — :base (libcudart only) and :runtime (+ CUDA shared libs) cannot compile it. | base=libcudart only; runtime=+CUDA shared libs; devel=+nvcc/headers/static libs | in-container | ●●● | ✓ |
| technique | layered-container-and-wsl2-detection-order | Detect in-container via /.dockerenv and /proc/1/cgroup FIRST; detect WSL2 via 'microsoft' in /proc/version — but record both as independent booleans because a Docker container on WSL2 inherits 'microsoft' from the host kernel. | signals: /.dockerenv, /proc/1/cgroup tokens (docker/containerd/lxc), /proc/version 'microsoft' | windows-wsl2 | ●●● | ✓ |
| technique | nvidia-smi-and-driver-injected-from-host | nvidia-smi and the GPU driver libraries are NOT in the container image — the NVIDIA Container Toolkit injects them from the host at `--gpus all`, along with /dev/nvidia* device nodes. | injects /dev/nvidia*, /dev/nvidiactl, /dev/nvidia-uvm + host driver libs at --gpus all | in-container | ●●● | ✓ |
| gotcha | wsl2-pinned-memory-cap-biases-htod-bandwidth | Under WSL2, cudaHostAlloc/cudaMallocHost (pinned host memory) is severely capped (user reports failure around ~300MB vs multiple GB on native Linux), and Unified/Managed Memory is unsupported — a host-to-device bandwidth bench that allocates a large pinned buffer will fail or silently fall back to slower pageable memory. | ~300MB pinned ceiling (WSL2 report) vs multi-GB native; pinned HtoD ~5.8 vs pageable ~2.3 GB/s | windows-wsl2 | ●●· | ✓ |
| constraint | wsl2-host-driver-stub-and-gpus-all-only | Under WSL2 the GPU is reached through WDDM with the Windows host driver stubbed as libcuda.so via /usr/lib/wsl/lib; you must never install a Linux GPU driver in WSL, and only `--gpus all` is supported (no per-index GPU selection). | only --gpus all supported on WSL2; libcuda stub at /usr/lib/wsl/lib | windows-wsl2 | ●●● | ✓ |
| benchmark | wsl2-host-interaction-overhead-tag-the-vantage | WSL2 adds host-interaction overhead vs native Linux even when GPU kernel time is identical — one report measured ~73% slower application-level frame time (19ms vs 11ms) — so every in-container/WSL2 bandwidth/latency number must be labeled with its vantage, not presented as bare-host truth. | ~73% slower app-level frame time under WSL2 (19ms vs 11ms); kernel time ~equal | in-container | ●●· | ✓ |
| gotcha | consumer-blackwell-wsl2-init-and-cudagraph-bug | On consumer Blackwell (RTX 5090 sm_120) under WSL2, pre-2.7.0 WSL crashed CUDA graph capture with cudaErrorUnknown and nvidia-cdi-refresh races driver init ~11s into boot; WSL2 2.7.0 + CUDA 12.8 is the known-good baseline, with documented systemd workarounds. | WSL2 2.7.0 fix; nvidia-cdi-refresh race ~11s; ExecStartPre sleep 45s; --enforce-eager ~8x throughput loss | windows-wsl2 | ●●● | ✓ |

## Detail

### A comprehensive evaluation of spatial co-execution on GPUs using MPS and MIG technologies · `directional` · craft
**Evaluates **MPS** (flexible SM share, memory contention) vs **MIG** (full isolation) including **Blackwell B200** among Ampere/Hopper/Blackwell — profile before choose (wave-06 69 deepen).**
Evaluates **MPS** (flexible SM share, memory contention) vs **MIG** (full isolation) including **Blackwell B200** among Ampere/Hopper/Blackwell — profile before choose (wave-06 69 deepen).
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [A comprehensive evaluation of spatial co-execution on GPUs using MPS and MIG tec](https://arxiv.org/abs/2604.22430)

### Absences on CDI support page · `directional` · craft
****Absent:** string “Blackwell”; sm_120 / CUDA 12.8 image floor; MPS sharing policy; decisive_axis language. Blackwell MIG mins live on MIG guide; CDI page only notes MIG **reconfig → manual regenerate**.**
**Absent:** string “Blackwell”; sm_120 / CUDA 12.8 image floor; MPS sharing policy; decisive_axis language. Blackwell MIG mins live on MIG guide; CDI page only notes MIG **reconfig → manual regenerate**.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0

### CDI SPEC.md · `directional` · craft
**Vendor JSON (`cdiVersion`, `kind`, `devices[].name`, `containerEdits`: env/deviceNodes/mounts/hooks/additionalGIDs). Well-known paths `/etc/cdi`, `/var/run/cdi`. Explains what `nvidia.yaml` must satisfy — not NVIDIA GPU-specific.**
Vendor JSON (`cdiVersion`, `kind`, `devices[].name`, `containerEdits`: env/deviceNodes/mounts/hooks/additionalGIDs). Well-known paths `/etc/cdi`, `/var/run/cdi`. Explains what `nvidia.yaml` must satisfy — not NVIDIA GPU-specific.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [CDI SPEC.md](https://raw.githubusercontent.com/cncf-tags/container-device-interface/main/SPEC.md)

### CIR: Lightweight Container Image for Cross-Platform Deployment · `directional` · craft
**Lazy-builder assembles OCI with CNI plus **NVIDIA Container Toolkit**; reuses GPU components via **libnvidia-container** — toolkit inject as portable GPU package craft.**
Lazy-builder assembles OCI with CNI plus **NVIDIA Container Toolkit**; reuses GPU components via **libnvidia-container** — toolkit inject as portable GPU package craft.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [CIR: Lightweight Container Image for Cross-Platform Deployment](https://arxiv.org/abs/2604.10411)

### CNCF Container Device Interface (CDI) · `directional` · analog
**Runtime-agnostic device package via JSON/YAML specs; does not invent a new gpu-container decisive axis.**
Runtime-agnostic device package via JSON/YAML specs; does not invent a new gpu-container decisive axis.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Hold-with-limit
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [CNCF Container Device Interface (CDI)](https://github.com/cncf-tags/container-device-interface) — SUPPORTED

### CRIUgpu — CDI + NVIDIA Container Toolkit · `directional` · craft
**GPU container checkpoint/restore integrates CDI + NVIDIA Container Toolkit; libnvidia-container injects devices/libs — package surface is CDI/toolkit, not image-baked drivers.**
GPU container checkpoint/restore integrates CDI + NVIDIA Container Toolkit; libnvidia-container injects devices/libs — package surface is CDI/toolkit, not image-baked drivers.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Package = host toolkit + CDI; no image-baked driver.
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [CRIUgpu — CDI + NVIDIA Container Toolkit](https://arxiv.org/abs/2502.16631) — Stoyanov et al. 2025; SUPPORTED

### CRIUgpu: Transparent Checkpointing of GPU-Accelerated Workloads · `directional` · craft
**GPU container C/R integrates **CDI** and the **NVIDIA Container Toolkit**; libnvidia-container injects devices/libraries into the mount namespace — CDI+toolkit as the package surface (not an invented axis).**
GPU container C/R integrates **CDI** and the **NVIDIA Container Toolkit**; libnvidia-container injects devices/libraries into the mount namespace — CDI+toolkit as the package surface (not an invented axis).
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [CRIUgpu: Transparent Checkpointing of GPU-Accelerated Workloads](https://arxiv.org/abs/2502.16631)

### CUDA C++ Best Practices (theoretical vs effective) · `directional` · craft
**Analog: theoretical link rate != effective measured bandwidth. Holds PCIe honesty. Limit: guide != invent 5090 GB/s.**
Analog: theoretical link rate != effective measured bandwidth. Holds PCIe honesty. Limit: guide != invent 5090 GB/s.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [CUDA C++ Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html) — NVIDIA

### CUDA Compatibility (forward / minor) · `directional` · craft
**Analog: toolkit/app can run across driver versions under defined forward/minor rules. Holds for toolkit-currency pins (image/toolkit match arch). Limit: compat matrix ≠ inventing a new axis.**
Analog: toolkit/app can run across driver versions under defined forward/minor rules. Holds for toolkit-currency pins (image/toolkit match arch). Limit: compat matrix ≠ inventing a new axis.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [CUDA Compatibility (forward / minor)](https://docs.nvidia.com/deploy/cuda-compatibility/index.html)

### Compose GPU devices · `directional` · craft
**Place GPUs via deploy.resources.reservations.devices; capabilities:[gpu] mandatory; count and device_ids mutually exclusive.**
Place GPUs via deploy.resources.reservations.devices; capabilities:[gpu] mandatory; count and device_ids mutually exclusive.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [Compose GPU devices](https://docs.docker.com/compose/how-tos/gpu-support/) — 2026; SUPPORTED

### Compose GPU support · `directional` · craft
**Compose GPU path: **driver: nvidia**, capabilities [gpu]; example nvidia/cuda:12.9.0-base-ubuntu22.04 — dated Compose package currency.**
Compose GPU path: **driver: nvidia**, capabilities [gpu]; example nvidia/cuda:12.9.0-base-ubuntu22.04 — dated Compose package currency.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Compose GPU support](https://docs.docker.com/compose/how-tos/gpu-support/) — Docker

### Compose deploy devices spec · `directional` · craft
**Device reservations require capabilities; count/device_ids exclusive.**
Device reservations require capabilities; count/device_ids exclusive.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [Compose deploy devices spec](https://docs.docker.com/reference/compose-file/deploy/#devices) — 2026; SUPPORTED

### Container Device Interface SPEC · `directional` · craft
**Analog: OCI runtimes inject third-party devices via CDI edits (nodes/hooks beyond a bare device node). Holds for wave-06 CDI package path. Limit: CDI ≠ a new gpu-container decisive_axis.**
Analog: OCI runtimes inject third-party devices via CDI edits (nodes/hooks beyond a bare device node). Holds for wave-06 CDI package path. Limit: CDI ≠ a new gpu-container decisive_axis.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Container Device Interface SPEC](https://github.com/cncf-tags/container-device-interface/blob/main/SPEC.md)

### Container Device Interface SPEC · `directional` · craft
**Analog: CNCF CDI device inject via containerEdits/OCI transform. Holds CDI path. Limit: CDI SPEC != new decisive_axis.**
Analog: CNCF CDI device inject via containerEdits/OCI transform. Holds CDI path. Limit: CDI SPEC != new decisive_axis.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Container Device Interface SPEC](https://github.com/cncf-tags/container-device-interface/blob/main/SPEC.md) — CNCF

### Dissecting the NVIDIA Blackwell Architecture with Microbenchmarks · `directional` · craft
****CUDA 12.8** and **PTX 8.7** expand support for Blackwell 5th-gen tensor instructions (`tcgen05`); older wgmma/FP8 paths are not Blackwell-compatible — toolkit/PTX currency gate (omit STUDY-028’s other Blackwell microbench).**
**CUDA 12.8** and **PTX 8.7** expand support for Blackwell 5th-gen tensor instructions (`tcgen05`); older wgmma/FP8 paths are not Blackwell-compatible — toolkit/PTX currency gate (omit STUDY-028’s other Blackwell microbench).
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Dissecting the NVIDIA Blackwell Architecture with Microbenchmarks](https://arxiv.org/abs/2507.10789)

### Docker Engine --gpus · `directional` · craft
**Expose with docker run --gpus all or device=<index|UUID>; requires NVIDIA driver + toolkit on the host.**
Expose with docker run --gpus all or device=<index|UUID>; requires NVIDIA driver + toolkit on the host.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [Docker Engine --gpus](https://docs.docker.com/engine/containers/gpu/) — 2026; SUPPORTED

### Docker Engine 28.2.0 release notes · `directional` · craft
**Docker Engine **28.2.0** dated **2025-05-28**; **CDI enabled by default** — Engine CDI default currency beyond STUDY-028/048/049.**
Docker Engine **28.2.0** dated **2025-05-28**; **CDI enabled by default** — Engine CDI default currency beyond STUDY-028/048/049.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Docker Engine 28.2.0](https://docs.docker.com/engine/release-notes/28/#2820) — Docker

### Docker Engine 28.x release notes · `directional` · craft
**Dated Engine patches: **28.4.0** 2025-09-03; **28.5.2** 2025-11-05 — package currency trail (Axis invented: 0; Numbers invented: 0).**
Dated Engine patches: **28.4.0** 2025-09-03; **28.5.2** 2025-11-05 — package currency trail (Axis invented: 0; Numbers invented: 0).
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Docker Engine 28.x release notes](https://docs.docker.com/engine/release-notes/28/) — Docker

### Docker Engine GPU access (`--gpus`) · `directional` · craft
**Analog: expose GPUs via `--gpus` when host has driver + toolkit. Holds for Engine place alongside CDI. Limit: flag presence ≠ honest isolation (MIG vs share).**
Analog: expose GPUs via `--gpus` when host has driver + toolkit. Holds for Engine place alongside CDI. Limit: flag presence ≠ honest isolation (MIG vs share).
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Docker Engine GPU access (`--gpus`)](https://docs.docker.com/engine/containers/gpu/)

### Docker container run — CDI devices · `directional` · docs
**CDI on by default for Linux; place via --device=<fully-qualified CDI name>.**
CDI on by default for Linux; place via --device=<fully-qualified CDI name>.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Deepens package/place
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [Docker container run — CDI devices](https://docs.docker.com/reference/cli/docker/container/run/) — SUPPORTED

### Dockerfile FROM pin · `directional` · craft
**Analog: pin tag or digest; omit tag implies latest. Holds Dockerfile digest honesty. Limit: digest pin != NVML honesty.**
Analog: pin tag or digest; omit tag implies latest. Holds Dockerfile digest honesty. Limit: digest pin != NVML honesty.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Dockerfile FROM](https://docs.docker.com/reference/dockerfile/#from) — Docker

### ElastiCo: Elastic Configuration and Interference-Aware Orchestration for GPU Clusters · `directional` · craft
**Kubernetes-native middleware for training/inference co-location; when MPS is enabled, sets per-client CUDA_MPS_PINNED_DEVICE_MEM_LIMIT and profiles with MPS disabled — place/package under MPS, not inventing a singleton axis or farm numbers.**
Kubernetes-native middleware for training/inference co-location; when MPS is enabled, sets per-client CUDA_MPS_PINNED_DEVICE_MEM_LIMIT and profiles with MPS disabled — place/package under MPS, not inventing a singleton axis or farm numbers.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [ElastiCo: Elastic Configuration and Interference-Aware Orchestration for GPU Clusters](https://arxiv.org/abs/2608.07971) — Wang, Zhou, Sun, Hu et al. 2026

### EnclaveX: End-to-End Confidential AI with CPU/GPU TEEs · `directional` · craft
**End-to-end CPU+GPU TEEs with **confidential containers** on Kubernetes and NVIDIA Hopper/H200 confidential GPU via CVM-contained driver — confidential package boundary deepen, not a new catalog axis.**
End-to-end CPU+GPU TEEs with **confidential containers** on Kubernetes and NVIDIA Hopper/H200 confidential GPU via CVM-contained driver — confidential package boundary deepen, not a new catalog axis.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [EnclaveX: End-to-End Confidential AI with CPU/GPU TEEs](https://arxiv.org/abs/2606.31408) — Schambach, Le, Arnautov, Fetzer 2026

### Gaps (on-page) · `directional` · craft
**Refresh auto-path misses MIG geometry changes; CDI schema v0.7.0 vs old engines needs feature-flag; no toolkit page equates generate to Blackwell compute readiness. Do not invent axis.**
Refresh auto-path misses MIG geometry changes; CDI schema v0.7.0 vs old engines needs feature-flag; no toolkit page equates generate to Blackwell compute readiness. Do not invent axis.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0

### Gaps vs still-current package catalog · `directional` · craft
**Meta Gaps: CTK **1.20.0** + Docker CDI default **28.2** + Compose nvidia path; Axis invented: 0; Numbers invented: 0 — no invent axis/numbers.**
Meta Gaps: CTK **1.20.0** + Docker CDI default **28.2** + Compose nvidia path; Axis invented: 0; Numbers invented: 0 — no invent axis/numbers.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0

### Getting Started with MIG · `directional` · craft
****B200** MIG: CUDA 12, driver **R570≥570.133.20**; **RTX PRO Blackwell** editions: R575+. Container path: CTK ≥v2.5.0-era; `NVIDIA_VISIBLE_DEVICES` / `--gpus` MIG UUID formats. **MPS+MIG:** per-MIG `CUDA_MPS_PIPE_DIRECTORY`; EXCLUSIVE_PROCESS not with MIG.**
**B200** MIG: CUDA 12, driver **R570≥570.133.20**; **RTX PRO Blackwell** editions: R575+. Container path: CTK ≥v2.5.0-era; `NVIDIA_VISIBLE_DEVICES` / `--gpus` MIG UUID formats. **MPS+MIG:** per-MIG `CUDA_MPS_PIPE_DIRECTORY`; EXCLUSIVE_PROCESS not with MIG.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Getting Started with MIG](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/getting-started-with-mig.html)

### Getting Started with MIG · `directional` · craft
**MIG container path: Container Toolkit / nvidia-docker2 **v2.5.0+**; B200/R570 floors on-page — MIG container currency, not invent axis.**
MIG container path: Container Toolkit / nvidia-docker2 **v2.5.0+**; B200/R570 floors on-page — MIG container currency, not invent axis.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Getting Started with MIG](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/getting-started-with-mig.html) — NVIDIA

### HPC Containers for EBRAINS: Towards Portable Cross-Domain Software Environment · `directional` · craft
**GPU containers still bind host drivers/libraries (ABI across boundary); deliberately builds against older **CUDA 12.2** for newer host drivers — CUDA currency / ABI gate without crowning an axis.**
GPU containers still bind host drivers/libraries (ABI across boundary); deliberately builds against older **CUDA 12.2** for newer host drivers — CUDA currency / ABI gate without crowning an axis.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [HPC Containers for EBRAINS: Towards Portable Cross-Domain Software Environment](https://arxiv.org/abs/2603.12044)

### Install guide · `directional` · craft
**UNVERIFIED install-guide 1.20.0-1 pin — do not treat as verified. Pin packages `NVIDIA_CONTAINER_TOOLKIT_VERSION=1.20.0-1`; `nvidia-ctk runtime configure --runtime=docker` rewrites daemon.json. Podman: prefer CDI. Config: `nvidia-ctk config --in-place --set …`.**
UNVERIFIED install-guide 1.20.0-1 pin — do not treat as verified. Pin packages `NVIDIA_CONTAINER_TOOLKIT_VERSION=1.20.0-1`; `nvidia-ctk runtime configure --runtime=docker` rewrites daemon.json. Podman: prefer CDI. Config: `nvidia-ctk config --in-place --set …`.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

### K8s schedule GPUs · `directional` · craft
**Expose vendor device resources (nvidia.com/gpu) and schedule via limits=requests. Holds for honest device placement; limit: cluster ≠ single-card.**
Expose vendor device resources (nvidia.com/gpu) and schedule via limits=requests. Holds for honest device placement; limit: cluster ≠ single-card.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [K8s schedule GPUs](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/) — 2026; SUPPORTED

### KIS-S: A GPU-Aware Kubernetes Inference Simulator with RL-Based Auto-Scaling · `directional` · craft
**GPU-aware K8s inference simulator on MicroK8s + single NVIDIA GPU; contrasts default **HPA** (CPU/memory) vs GPU metrics via Prometheus/DCGM Exporter — autoscaling currency for containerized GPU services.**
GPU-aware K8s inference simulator on MicroK8s + single NVIDIA GPU; contrasts default **HPA** (CPU/memory) vs GPU metrics via Prometheus/DCGM Exporter — autoscaling currency for containerized GPU services.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [KIS-S: A GPU-Aware Kubernetes Inference Simulator with RL-Based Auto-Scaling](https://arxiv.org/abs/2507.07932) — Zhang, Guo, Tan, Guan, Jiang 2025

### Kubernetes Resource Quotas — GPU capacity caps · `directional` · analog
**Hard requests.nvidia.com/gpu caps are absolute.**
Hard requests.nvidia.com/gpu caps are absolute.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Refuse false-green over-admit
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [Kubernetes Resource Quotas — GPU capacity caps](https://kubernetes.io/docs/concepts/policy/resource-quotas/) — SUPPORTED

### Leveraging Multi-Instance GPUs through moldable task scheduling · `directional` · craft
**MIG on Ampere/Hopper/**Blackwell**; contrasts MPS SM-share vs MIG isolated compute+memory; B100/B200 keep A100/H100-style MIG slice limits — MIG schedule craft under reconfiguration constraints.**
MIG on Ampere/Hopper/**Blackwell**; contrasts MPS SM-share vs MIG isolated compute+memory; B100/B200 keep A100/H100-style MIG slice limits — MIG schedule craft under reconfiguration constraints.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Leveraging Multi-Instance GPUs through moldable task scheduling](https://arxiv.org/abs/2507.13601)

### MIG User Guide · `directional` · craft
**Analog: partition GPU into **isolated** instances with dedicated compute/memory. Holds for place craft when isolation is required. Limit: MIG hardware profiles ≠ Compose syntax alone.**
Analog: partition GPU into **isolated** instances with dedicated compute/memory. Holds for place craft when isolation is required. Limit: MIG hardware profiles ≠ Compose syntax alone.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [MIG User Guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/index.html)

### MedFoundationHub: A Lightweight and Secure Toolkit for Deploying Medical Vision Language Foundation Models · `directional` · craft
**On-prem VLM toolkit with **Docker-orchestrated** inference/workload plane (Dockerfile to isolated containers) on a single NVIDIA workstation GPU — package surface is containerized local deploy, not a new decisive axis.**
On-prem VLM toolkit with **Docker-orchestrated** inference/workload plane (Dockerfile to isolated containers) on a single NVIDIA workstation GPU — package surface is containerized local deploy, not a new decisive axis.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [MedFoundationHub: A Lightweight and Secure Toolkit for Deploying Medical Vision Language Foundation Models](https://arxiv.org/abs/2508.20345) — Li, Zhu, Deng, Wei et al. 2025

### Multi-Process Service (MPS) · `directional` · craft
**Analog: **shared** co-operative CUDA multi-process scheduling for utilization. Holds as the share/time-slice class adjacent to place. Limit: MPS share ≠ MIG isolation guarantees.**
Analog: **shared** co-operative CUDA multi-process scheduling for utilization. Holds as the share/time-slice class adjacent to place. Limit: MPS share ≠ MIG isolation guarantees.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Multi-Process Service (MPS)](https://docs.nvidia.com/deploy/mps/index.html)

### NVIDIA CDI support · `directional` · craft
**From toolkit v1.12.0 CDI specs; v1.18.0 nvidia-cdi-refresh auto-writes nvidia.yaml; devices nvidia.com/gpu=all|0|….**
From toolkit v1.12.0 CDI specs; v1.18.0 nvidia-cdi-refresh auto-writes nvidia.yaml; devices nvidia.com/gpu=all|0|….
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [NVIDIA CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html) — 2026; SUPPORTED

### NVIDIA CDI support · `directional` · craft
**Analog: from toolkit v1.12.0, `nvidia-ctk cdi generate` writes host-driver injection (`nvidia.com/gpu=…`, MIG names). Holds for toolkit-currency → CDI → runtime. Limit: generate on host ≠ image-baked drivers.**
Analog: from toolkit v1.12.0, `nvidia-ctk cdi generate` writes host-driver injection (`nvidia.com/gpu=…`, MIG names). Holds for toolkit-currency → CDI → runtime. Limit: generate on host ≠ image-baked drivers.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [NVIDIA CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html)

### NVIDIA CDI support (analog) · `directional` · craft
**Analog: CDI generate **v1.12.0**; nvidia-cdi-refresh **v1.18.0**. Holds CDI toolkit inject pin. Limit: generate on host != invent decisive_axis.**
Analog: CDI generate **v1.12.0**; nvidia-cdi-refresh **v1.18.0**. Holds CDI toolkit inject pin. Limit: generate on host != invent decisive_axis.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [NVIDIA CDI support](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html) — NVIDIA

### NVIDIA CTK install guide · `directional` · craft
**Install packages then nvidia-ctk runtime configure --runtime=docker rewriting daemon.json — host-side prerequisite before --gpus.**
Install packages then nvidia-ctk runtime configure --runtime=docker rewriting daemon.json — host-side prerequisite before --gpus.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [NVIDIA CTK install guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) — 2026; SUPPORTED

### NVIDIA CTK specialized configs — IMEX channels · `directional` · docs
**NVIDIA_IMEX_CHANNELS requests host IMEX channels; CDI validates channel nodes.**
NVIDIA_IMEX_CHANNELS requests host IMEX channels; CDI validates channel nodes.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** Deepens package/place
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [NVIDIA CTK specialized configs — IMEX channels](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/docker-specialized.html) — SUPPORTED

### NVIDIA Container Toolkit latest index · `directional` · craft
**Docs branded **1.20.0** tip tree — CTK currency pin for still-current docker package path.**
Docs branded **1.20.0** tip tree — CTK currency pin for still-current docker package path.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html) — NVIDIA

### NVIDIA Container Toolkit release notes · `directional` · craft
**Tip **1.20.0**; **1.18.0** JIT-CDI + nvidia-cdi-refresh; **1.19.1** CDI schema **v0.7.0** needs docker>=26.1.0 — dated CTK currency (Axis invented: 0; Numbers invented: 0).**
Tip **1.20.0**; **1.18.0** JIT-CDI + nvidia-cdi-refresh; **1.19.1** CDI schema **v0.7.0** needs docker>=26.1.0 — dated CTK currency (Axis invented: 0; Numbers invented: 0).
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [NVIDIA Container Toolkit release notes](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/release-notes.html) — NVIDIA

### NVIDIA k8s-device-plugin · `directional` · craft
**Analog: DaemonSet advertises/allocates device nodes + health; host driver stays outside the image. Holds for toolkit inject pattern. Limit: cluster plugin ≠ single-host Docker CDI only.**
Analog: DaemonSet advertises/allocates device nodes + health; host driver stays outside the image. Holds for toolkit inject pattern. Limit: cluster plugin ≠ single-host Docker CDI only.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [NVIDIA k8s-device-plugin](https://github.com/NVIDIA/k8s-device-plugin)

### Performance Characterization of Containerized DNN Training and Inference on Edge Accelerators · `directional` · craft
**Compares **Docker** vs bare-metal DNN train/infer on Jetson-class edges; notes CUDA MPS/MIG as related sharing mechanisms — containerization overhead craft without crowning an axis.**
Compares **Docker** vs bare-metal DNN train/infer on Jetson-class edges; notes CUDA MPS/MIG as related sharing mechanisms — containerization overhead craft without crowning an axis.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Performance Characterization of Containerized DNN Training and Inference on Edge Accelerators](https://arxiv.org/abs/2312.07220) — Prashanthi, Hegde, Patchava, Das, Simmhan 2023

### Private LLM Inference on Consumer Blackwell GPUs: A Practical Guide for Cost-Effective Local Deployment in SMEs · `directional` · craft
**Releases a **Docker image** (vLLM/AIPerf/DCGM stack); requires NVIDIA **driver 570.x+**, **CUDA 12.9**, cuDNN 9.x for NVFP4 on consumer Blackwell — currency pin for image/driver/CUDA match (no invented measured numbers here).**
Releases a **Docker image** (vLLM/AIPerf/DCGM stack); requires NVIDIA **driver 570.x+**, **CUDA 12.9**, cuDNN 9.x for NVFP4 on consumer Blackwell — currency pin for image/driver/CUDA match (no invented measured numbers here).
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Private LLM Inference on Consumer Blackwell GPUs: A Practical Guide for Cost-Effective Local Deployment in SMEs](https://arxiv.org/abs/2601.09527) — Knoop, Holtmann 2026

### Q-GEAR: Improving quantum simulation framework · `directional` · craft
**Deploys **Podman** container plus NERSC **NVIDIA public image** for Cuda-Q GPU simulation — Podman/NVIDIA image package path adjacent to Docker toolkit inject.**
Deploys **Podman** container plus NERSC **NVIDIA public image** for Cuda-Q GPU simulation — Podman/NVIDIA image package path adjacent to Docker toolkit inject.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Q-GEAR: Improving quantum simulation framework](https://arxiv.org/abs/2504.03967) — Guo, Pan, Balewski 2025

### Release notes · `directional` · craft
**UNVERIFIED install-guide 1.20.0-1 pin — do not treat as verified. **1.18.0**: auto CDI refresh systemd + default JIT-CDI. **1.19.1**: CDI schema **v0.7.0** default (needs containerd≥1.7.16 / docker≥26.1 / podman≥5.1); `--feature-flag no-additional-gids-for-device-nodes` for older; MIG `/dev/dri*` injection. **1.20.0**: app-profile hook, WSL2 broader discovery. Generate loads select `config.toml` settings.**
UNVERIFIED install-guide 1.20.0-1 pin — do not treat as verified. **1.18.0**: auto CDI refresh systemd + default JIT-CDI. **1.19.1**: CDI schema **v0.7.0** default (needs containerd≥1.7.16 / docker≥26.1 / podman≥5.1); `--feature-flag no-additional-gids-for-device-nodes` for older; MIG `/dev/dri*` injection. **1.20.0**: app-profile hook, WSL2 broader discovery. Generate loads select `config.toml` settings.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Release notes](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/release-notes.html)

### SPEC CPU 2017 Overview · `directional` · craft
**Analog: honest data vs marketing hype; SPECspeed != SPECrate. Holds measurement honesty. Limit: SPEC suites != invent tok/s.**
Analog: honest data vs marketing hype; SPECspeed != SPECrate. Holds measurement honesty. Limit: SPEC suites != invent tok/s.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [SPEC CPU 2017 Overview](https://www.spec.org/cpu2017/Docs/overview.html) — SPEC

### Scalable APT Malware Classification via Parallel Feature Extraction and GPU-Accelerated Learning · `directional` · craft
**Repro path: install toolkit then `nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml`, run Podman with `--device nvidia.com/gpu=all` — names **cdi generate** as the compose contract.**
Repro path: install toolkit then `nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml`, run Podman with `--device nvidia.com/gpu=all` — names **cdi generate** as the compose contract.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Scalable APT Malware Classification via Parallel Feature Extraction and GPU-Acce](https://arxiv.org/abs/2504.15497)

### Seekable OCI: Lazy-Loading Container Images via Range-Request Indexing · `directional` · craft
**SOCI lazy-loads unmodified **OCI** images; production path notes EKS Auto Mode uses SOCI parallel pull for **GPU instances** — image-pull package craft for GPU pods (no invented axis).**
SOCI lazy-loads unmodified **OCI** images; production path notes EKS Auto Mode uses SOCI parallel pull for **GPU instances** — image-pull package craft for GPU pods (no invented axis).
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Seekable OCI: Lazy-Loading Container Images via Range-Request Indexing](https://arxiv.org/abs/2607.06868) — Thompson, Mesard, Butler, Rajakumar, Wang 2026

### Semantic Versioning · `directional` · craft
**Analog: MAJOR.MINOR.PATCH; MUST NOT mutate released versions. Holds SemVer package pin. Limit: SemVer != invent GB/s.**
Analog: MAJOR.MINOR.PATCH; MUST NOT mutate released versions. Holds SemVer package pin. Limit: SemVer != invent GB/s.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Semantic Versioning](https://semver.org/) — semver.org

### Subedar — nvidia-ctk cdi generate contract · `directional` · craft
**Repro path: nvidia-ctk cdi generate then Podman --device nvidia.com/gpu=all — CDI generate as compose/runtime attach contract.**
Repro path: nvidia-ctk cdi generate then Podman --device nvidia.com/gpu=all — CDI generate as compose/runtime attach contract.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [Subedar — nvidia-ctk cdi generate contract](https://arxiv.org/abs/2504.15497) — Subedar et al. 2025; SUPPORTED

### Support for CDI · `directional` · craft
**CDI generate since **v1.12.0**. From **v1.18.0**: `nvidia-cdi-refresh` writes `/var/run/cdi/nvidia.yaml` on toolkit/driver install/upgrade and reboot. Knobs: `nvidia-ctk cdi list`; manual `nvidia-ctk cdi generate --output=/var/run/cdi/nvidia.yaml`; env overrides in `/etc/nvidia-container-toolkit/nvidia-cdi-refresh.env`. **Known limits:** refresh does **not** handle driver removal or **MIG reconfiguration** — regenerate manually. Devices: `nvidia.com/gpu=all`, `=0`, MIG e.g. `nvidia.com/gpu=1:0`. JIT-CDI + `--disable-hook`.**
CDI generate since **v1.12.0**. From **v1.18.0**: `nvidia-cdi-refresh` writes `/var/run/cdi/nvidia.yaml` on toolkit/driver install/upgrade and reboot. Knobs: `nvidia-ctk cdi list`; manual `nvidia-ctk cdi generate --output=/var/run/cdi/nvidia.yaml`; env overrides in `/etc/nvidia-container-toolkit/nvidia-cdi-refresh.env`. **Known limits:** refresh does **not** handle driver removal or **MIG reconfiguration** — regenerate manually. Devices: `nvidia.com/gpu=all`, `=0`, MIG e.g. `nvidia.com/gpu=1:0`. JIT-CDI + `--disable-hook`.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Support for CDI](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html)

### Support for CDI · `directional` · craft
**CDI generate since **v1.12.0**; auto refresh **v1.18.0**; example status Fri 2025-06-27; MIG reconfig requires manual regen — CDI pin craft, not invent axis.**
CDI generate since **v1.12.0**; auto refresh **v1.18.0**; example status Fri 2025-06-27; MIG reconfig requires manual regen — CDI pin craft, not invent axis.
- **Applies to:** docker; container-runtime; CDI; CTK; package-pin · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen docker still-current package/CDI/CTK. Axis invented: 0. Numbers invented: 0.
- **Verify:** verdict=unverified | STUDY-063 deepen; Numbers invented: 0
- **Sources:** [Support for CDI](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html) — NVIDIA

### Taming GPU Underutilization via Static Partitioning and Fine-grained CPU Offloading · `directional` · craft
**Frames MPS (compute-only partition) vs MIG (compute+memory) as spatial-sharing options with different isolation/flexibility; includes B200 capacity table — underutilization/partition craft, not a singleton axis invent.**
Frames MPS (compute-only partition) vs MIG (compute+memory) as spatial-sharing options with different isolation/flexibility; includes B200 capacity table — underutilization/partition craft, not a singleton axis invent.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Taming GPU Underutilization via Static Partitioning and Fine-grained CPU Offload](https://arxiv.org/abs/2604.08451)

### Troubleshooting · `directional` · craft
**CDI inject survives cgroup updates better than legacy hook. Generate flags: `--feature-flag no-additional-gids-for-device-nodes`; refresh env `NVIDIA_CTK_CDI_GENERATE_FEATURE_FLAGS=…`.**
CDI inject survives cgroup updates better than legacy hook. Generate flags: `--feature-flag no-additional-gids-for-device-nodes`; refresh env `NVIDIA_CTK_CDI_GENERATE_FEATURE_FLAGS=…`.
- **Applies to:** docker; nvidia-ctk; CDI; MIG; MPS · **Confidence:** medium · **Rig relevance:** 3/5
- **Design implication:** Deepen wave-06 package/place. Axis invented: 0. Do not invent decisive_axis.
- **Verify:** verdict=unverified | STUDY-048 deepen; Axis invented: 0
- **Sources:** [Troubleshooting](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/troubleshooting.html)

### k8s-device-plugin — host inject analog · `directional` · craft
**DaemonSet injects device nodes + health; host driver not in the image. Holds for NVIDIA Container Toolkit --gpus injection; limit: k8s ≠ Docker CDI on WSL2.**
DaemonSet injects device nodes + health; host driver not in the image. Holds for NVIDIA Container Toolkit --gpus injection; limit: k8s ≠ Docker CDI on WSL2.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** STUDY-004 Verifier-verified
- **Verify:** STUDY-014 from STUDY-004 Verifier ✅; default verified=0
- **Sources:** [k8s-device-plugin — host inject analog](https://github.com/NVIDIA/k8s-device-plugin) — 2026; SUPPORTED

### nvidia-container-toolkit v1.20.0 release · `directional` · docs
**IMEX channel validation in CDI/JIT-CDI; application-profile CDI hook limiting EGL/Vulkan to assigned GPUs.**
IMEX channel validation in CDI/JIT-CDI; application-profile CDI hook limiting EGL/Vulkan to assigned GPUs.
- **Applies to:** docker; nvidia-ctk; gpu-container · **Confidence:** high · **Rig relevance:** 4/5
- **Design implication:** CTK 1.20 currency; Vulkan A4/A6 Cloudflare omit separately
- **Verify:** verdict=confirmed | STUDY-028 Verifier ✅
- **Sources:** [nvidia-container-toolkit v1.20.0 release](https://github.com/NVIDIA/nvidia-container-toolkit/releases) — SUPPORTED

### Even on Linux, UVM oversubscription is wrong for decode · `load-bearing` · constraint
**On-demand page-migrated UVM collapses effective bandwidth by orders of magnitude — fatal for bandwidth-bound decode.**
NVIDIA's own oversubscription blog reports performance can vary up to 100x; on-demand migration falls from ~8-10 GB/s to ~1 GB/s at 2x oversubscription, and random access drops to a few hundred KB/s — vs the hundreds of GB/s decode needs. Chien et al. measured basic UM 9-14x slower than explicit even before oversubscription; GPUVM (2024) confirms stock demand-paging is a known bottleneck being re-engineered. Decode is bandwidth-bound (the Memory Wall).
- **Applies to:** linux; windows-wsl2 · **Metric:** up to 100x variation; ~8-10 -> ~1 GB/s at 2x oversub; random to hundreds of KB/s · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Explicit declared placement beats blind demand-paging decisively even where UVM exists — confirms the architecture, not just the platform constraint.
- **Verify:** verdict=confirmed | NVIDIA blog author corrected to Garg & Sakharnykh (was 'Chien/Markidis'); content + magnitudes confirmed.
- **Sources:** [Improving GPU Memory Oversubscription Performance (NVIDIA Technical Blog)](https://developer.nvidia.com/blog/improving-gpu-memory-oversubscription-performance/) — Garg & Sakharnykh (NVIDIA) 2021; up to 100x; ~1 GB/s at 2x oversub; SUPPORTED ; [Performance Evaluation of Advanced Features in CUDA Unified Memory](https://arxiv.org/abs/1910.09598) — Chien, Peng & Markidis 2019; 9-14x slower; SUPPORTED ; [AI and Memory Wall](https://arxiv.org/abs/2403.14123) — Gholami et al. 2024; decode bandwidth-bound; SUPPORTED

### No CUDA UVM oversubscription on Windows/WSL2 · `load-bearing` · constraint
**Full managed-memory oversubscription is unavailable on Windows native and WSL2 by driver design (WDDM).**
NVIDIA's CUDA-on-WSL guide states verbatim that Full Managed Memory is unavailable on Windows native and WSL2 'for the foreseeable future' and warns of reduced performance / high host-memory use. The CUDA C++ Programming Guide formalizes the split: Linux allows managed-memory oversubscription; Windows/WSL/Tegra do not (cudaDevAttrConcurrentManagedAccess == 0), and such devices cannot allocate more managed memory than physical VRAM (oversubscription needs CC 6.0+ page faulting).
- **Applies to:** windows-wsl2 · **Metric:** cudaDevAttrConcurrentManagedAccess == 0 on Windows/WSL/Tegra · **Confidence:** high · **Rig relevance:** 5/5
- **Design implication:** Explicit, declared placement is the ONLY honest route on the target platform — this is NOT 'Docker VRAM overflow'. The whole product positioning rests here, and it is primary-sourced.
- **Verify:** verdict=confirmed | NVIDIA docs quoted verbatim by the oracle; both mistral + granite SUPPORT=YES. Strongest-verified finding in the study.
- **Sources:** [CUDA on WSL User Guide (NVIDIA)](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA 2025; no managed-memory oversubscription; SUPPORTED ; [CUDA C++ Programming Guide — Unified/System Memory + Oversubscription](https://docs.nvidia.com/cuda/cuda-programming-guide/) — NVIDIA 2025; Linux yes / Windows-WSL no; SUPPORTED

### cuda-128-minimum-for-sm120-image · `load-bearing` · gotcha
**On Blackwell sm_120 the in-image CUDA toolkit must be >=12.8 or compute fails ('device kernel image is invalid') even though nvidia-smi reports a higher CUDA and runs fine.**
nvidia-smi shows the MAXIMUM CUDA version the HOST DRIVER supports (driver API), which is decoupled from the toolkit (cudart/nvcc) baked into the image. A new-enough host driver will make nvidia-smi succeed in any container, masking the fact that an old image (e.g. CUDA 12.4) cannot generate or load sm_120 kernels. The minimum toolkit with sm_120 codegen/runtime support is CUDA 12.8. A profiler that only checks nvidia-smi will think the rig is healthy, then the cudaMemcpy/kernel bench fails at launch with cudaErrorNoKernelImageForDevice / 'device kernel image is invalid'.
- **Applies to:** in-container · **Metric:** CUDA 12.8 = minimum toolkit for Blackwell sm_120 · **Confidence:** high
- **Design implication:** The profiler must check the IMAGE's CUDA toolkit version (e.g. from cudart / `nvcc --version` / the CUDA_VERSION env) independently of nvidia-smi, and assert >=12.8 for sm_120. On mismatch, emit a structured error distinguishing 'image toolkit too old for this GPU' from 'driver too old' — do not silently produce a bandwidth number from a fallback path.
- **Verify:** verdict=confirmed-with-fixes | a source NOT_SUPPORTED (flagged); oracle retrieval + family-different (mistral + granite)
- **Sources:** [Discrepancy in NVIDIA-SMI and Driver Version, CUDA Installation Issues](https://forums.developer.nvidia.com/t/discrepancy-in-nvidia-smi-and-driver-version-cuda-installation-issues/304136) — NVIDIA Developer Forums 2024; NOT_SUPPORTED ; [RTX 5090 D v2 (Blackwell SM_120): MMQ CUDA kernel crash — device kernel image is invalid](https://github.com/ollama/ollama/issues/14374) — ollama / community 2025; SUPPORTED

### devel-image-required-for-cudaMemcpy-bench · `load-bearing` · constraint
**A cudaMemcpy bandwidth benchmark must be compiled with nvcc, which only exists in the nvidia/cuda:*-devel image — :base (libcudart only) and :runtime (+ CUDA shared libs) cannot compile it.**
NVIDIA's official container-image layering: base = bare minimum (libcudart) to run a pre-built CUDA app; runtime = base + all CUDA-toolkit shared libraries; devel = runtime + compiler toolchain (nvcc), debugging tools, headers, and static libraries. To compile-and-run a cudaMemcpy / bandwidthTest-style bench inside the container you need devel (nvcc + headers + runtime). If the profiler ships a precompiled bench binary instead, :runtime suffices; if it compiles at build time, the Dockerfile build stage needs devel even if the final stage is slimmer (multi-stage).
- **Applies to:** in-container · **Metric:** base=libcudart only; runtime=+CUDA shared libs; devel=+nvcc/headers/static libs · **Confidence:** high
- **Design implication:** Project Dockerfile FROM should be nvidia/cuda:12.8.x-devel-ubuntu22.04 (or newer, >=12.8 for sm_120). If slimming the final image, use a multi-stage build: compile the bench in a devel stage, copy the binary into a runtime stage. Do not pick :base — it lacks even the full toolkit libs the bench links against.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [Container images — NVIDIA Cloud Native Products documentation](https://nvidia.github.io/container-wiki/toolkit/container-images.html) — NVIDIA 2024; base=libcudart; runtime=+shared libs; devel=+nvcc+headers+static; SUPPORTED ; [difference between runtime tag and devel tag — nvidia/container-images/cuda issue #45](https://gitlab.com/nvidia/container-images/cuda/-/issues/45) — NVIDIA / community 2020; PARTIAL

### layered-container-and-wsl2-detection-order · `load-bearing` · technique
**Detect in-container via /.dockerenv and /proc/1/cgroup FIRST; detect WSL2 via 'microsoft' in /proc/version — but record both as independent booleans because a Docker container on WSL2 inherits 'microsoft' from the host kernel.**
Reliable container detection: presence of /.dockerenv, OR docker/containerd/lxc tokens in /proc/1/cgroup (or /proc/self/cgroup). Caveat: under cgroup v2 the cgroup path may no longer contain 'docker', so /.dockerenv is the more robust primary signal; systemd-detect-virt --container is a fallback. WSL2 detection: /proc/version (and /proc/sys/kernel/osrelease) contains 'microsoft'/'WSL2'. The trap (confirmed by git-credential-manager #1813): a container running under Docker Desktop's WSL2 backend ALSO has 'microsoft' in /proc/version because it shares the WSL2 host kernel — so the two conditions are NOT mutually exclusive. The profiler genuinely lives in 'in-container AND under-WSL2' and both flags change the measurement (toolkit injection + WDDM caveats), so it must store both, not pick one.
- **Applies to:** windows-wsl2 · **Metric:** signals: /.dockerenv, /proc/1/cgroup tokens (docker|containerd|lxc), /proc/version 'microsoft' · **Confidence:** high
- **Design implication:** profile.json platform block should carry separate fields: in_container (bool), container_runtime (docker|containerd|null), under_wsl2 (bool), wsl2_version (string). Order checks container-first so logging/labels are correct, but never use container-detection to SUPPRESS the WSL2 flag — both caveats apply simultaneously and both gate the bandwidth interpretation.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [GCM Misidentifies Docker Containers Running on WSL2 Due to /proc/version](https://github.com/git-ecosystem/git-credential-manager/issues/1813) — git-credential-manager / community 2022; SUPPORTED ; [How to Check if a Process is Running Inside a Docker Container (/proc/self/cgroup, /.dockerenv)](https://www.codestudy.net/blog/how-to-check-if-a-process-is-running-inside-docker-container/) — community 2023; PARTIAL

### nvidia-smi-and-driver-injected-from-host · `load-bearing` · technique
**nvidia-smi and the GPU driver libraries are NOT in the container image — the NVIDIA Container Toolkit injects them from the host at `--gpus all`, along with /dev/nvidia* device nodes.**
At `docker run --gpus all`, the nvidia-container-runtime (a wrapper around runC, registered in /etc/docker/daemon.json) inserts a prestart hook that calls nvidia-container-cli (libnvidia-container) to mount host driver libraries and create /dev/nvidia*, /dev/nvidiactl, /dev/nvidia-uvm inside the container. nvidia-smi itself is provided by the host driver package, not the image. Consequence: the profiler can call nvidia-smi inside ANY of base/runtime/devel as long as `--gpus all` was passed and the toolkit is installed on the host. If nvidia-smi is missing in-container, the failure is a toolkit/registration problem (host-side), not a base-image choice.
- **Applies to:** in-container · **Metric:** injects /dev/nvidia*, /dev/nvidiactl, /dev/nvidia-uvm + host driver libs at --gpus all · **Confidence:** high
- **Design implication:** The profiler should treat a missing nvidia-smi or empty /dev/nvidia* as a 'GPU not injected' platform error (toolkit not installed / `--gpus all` omitted / wrong runtime in daemon.json), distinct from a CUDA-version error. Probe /dev/nvidiactl existence and `nvidia-smi -L` as the first GPU-presence gate before any bandwidth bench.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [Architecture Overview — NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/arch-overview.html) — NVIDIA 2024; SUPPORTED ; [nvidia/cuda Docker Hub overview & NVIDIA Container Toolkit docs](https://hub.docker.com/r/nvidia/cuda) — NVIDIA 2024; PARTIAL

### wsl2-pinned-memory-cap-biases-htod-bandwidth · `load-bearing` · gotcha
**Under WSL2, cudaHostAlloc/cudaMallocHost (pinned host memory) is severely capped (user reports failure around ~300MB vs multiple GB on native Linux), and Unified/Managed Memory is unsupported — a host-to-device bandwidth bench that allocates a large pinned buffer will fail or silently fall back to slower pageable memory.**
NVIDIA's CUDA-on-WSL guide states Full Managed (Unified) Memory is unavailable on Windows-native and thus WSL2, pinned system memory is limited, and concurrent CPU/GPU access is unsupported. A community report (NVIDIA forum) puts the practical cudaHostAlloc ceiling around 300MB in WSL2 before allocation fails, where native Linux handles many GB; NVIDIA's njuffa confirms max pinned memory is an OS-internal property (WDDM here), not a CUDA constant. Pinned vs pageable matters a lot for the number: pinned HtoD is ~2x+ faster than pageable (NVIDIA's data-transfer blog: ~5.8 vs ~2.3 GB/s on one GPU). So an honest profiler measuring 'PCIe host-to-device GB/s' inside WSL2 must control the buffer size and the pinned/pageable mode, or it will report a pageable-fallback number and call it PCIe bandwidth.
- **Applies to:** windows-wsl2 · **Metric:** ~300MB pinned ceiling (WSL2 report) vs multi-GB native; pinned HtoD ~5.8 vs pageable ~2.3 GB/s · **Confidence:** medium
- **Design implication:** The bandwidth bench should: (a) request a modest pinned buffer (e.g. <=128MB) so cudaHostAlloc succeeds under WSL2; (b) check the cudaHostAlloc return code and, on failure, either shrink or fall back to pageable AND set a 'pinned_fallback: pageable' flag in profile.json; (c) tag each bandwidth figure with the allocation mode and the in-container/WSL2 vantage so the +/-10% receipt is honest; never publish a pageable-fallback figure as the pinned PCIe ceiling. Do NOT rely on Unified Memory for any probe under WSL2.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [CUDA on WSL User Guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA 2024; Unified Memory unsupported; pinned memory limited; SUPPORTED ; [cudaHostAlloc limitations in WSL2](https://forums.developer.nvidia.com/t/cudahostalloc-limitations-in-wsl2/142288) — NVIDIA Developer Forums (user 'hardvark') 2021; ~300MB pinned ceiling in WSL2; SUPPORTED ; [How to Optimize Data Transfers in CUDA C/C++](https://developer.nvidia.com/blog/how-optimize-data-transfers-cuda-cc/) — Mark Harris, NVIDIA 2012; pinned ~5.8 GB/s vs pageable ~2.3 GB/s; SUPPORTED

### wsl2-host-driver-stub-and-gpus-all-only · `supporting` · constraint
**Under WSL2 the GPU is reached through WDDM with the Windows host driver stubbed as libcuda.so via /usr/lib/wsl/lib; you must never install a Linux GPU driver in WSL, and only `--gpus all` is supported (no per-index GPU selection).**
NVIDIA's CUDA-on-WSL guide: the Windows host CUDA driver is stubbed inside WSL2 as libcuda.so; do NOT install any Linux display/GPU driver in WSL2; bare-metal tools live at /usr/lib/wsl/lib (e.g. /usr/lib/wsl/lib/nvidia-smi). With the NVIDIA Container Toolkit on WSL2, only `--gpus all` works — multi-GPU filtering by index is not available. This means the profiler cannot assume standard /usr/lib/x86_64-linux-gnu driver paths and cannot select a specific GPU by index on this rig. The path also implies the libcuda.so the bench links against comes from the WSL stub, so version checks should consider /usr/lib/wsl/lib.
- **Applies to:** windows-wsl2 · **Metric:** only --gpus all supported on WSL2; libcuda stub at /usr/lib/wsl/lib · **Confidence:** high
- **Design implication:** Profiler must (a) not attempt per-GPU-index selection on WSL2 (single-GPU assumption is fine for this rig anyway); (b) ensure /usr/lib/wsl/lib is on the library/PATH search when resolving nvidia-smi/libcuda; (c) never recommend installing a Linux driver in its setup docs; (d) record driver source as 'WSL stub (host WDDM)' in the platform block.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [CUDA on WSL User Guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA 2024; --gpus all only; /usr/lib/wsl/lib stub; SUPPORTED

### wsl2-host-interaction-overhead-tag-the-vantage · `supporting` · benchmark
**WSL2 adds host-interaction overhead vs native Linux even when GPU kernel time is identical — one report measured ~73% slower application-level frame time (19ms vs 11ms) — so every in-container/WSL2 bandwidth/latency number must be labeled with its vantage, not presented as bare-host truth.**
NVIDIA forum (pinned-memory thread) and the WSL guide together establish that GPU kernel execution under WSL2 is expected to match native, but anything crossing the WDDM/host boundary (transfers, allocations, submission latency) can be markedly slower; a cited case shows ~73% higher per-frame application time under WSL2 (19ms vs 11ms) on identical hardware. This is exactly the regime a host-to-device PCIe bandwidth and small-copy-latency probe measures. The profiler's stated honesty contract (+/-10% receipt, refuse below 1 tok/s) is only honest if the receipt carries the vantage label, because the same rig can read meaningfully different transfer numbers in-container/WSL2 vs bare host.
- **Applies to:** in-container · **Metric:** ~73% slower app-level frame time under WSL2 (19ms vs 11ms); kernel time ~equal · **Confidence:** medium
- **Design implication:** profile.json must stamp every bandwidth/latency measurement with vantage = 'wsl2-container' (and WSL2 version + container runtime). Do not extrapolate a bare-host number from a WSL2 measurement. Where possible, run a fixed warm-up + multiple iterations and report median +/- spread so the +/-10% receipt reflects measured variance in THIS vantage rather than an assumed native figure.
- **Verify:** verdict=confirmed | oracle retrieval + family-different (mistral + granite)
- **Sources:** [What are the pinned memory limitations on CUDA for WSL2?](https://forums.developer.nvidia.com/t/what-are-the-pinned-memory-limitations-on-cuda-for-wsl2/255472) — NVIDIA Developer Forums (incl. NVIDIA 'njuffa') 2023; ~73% slower app time (19ms vs 11ms); pinned cap is OS-dependent; SUPPORTED ; [CUDA on WSL User Guide — performance caveats](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA 2024; SUPPORTED

### consumer-blackwell-wsl2-init-and-cudagraph-bug · `watch` · gotcha
**On consumer Blackwell (RTX 5090 sm_120) under WSL2, pre-2.7.0 WSL crashed CUDA graph capture with cudaErrorUnknown and nvidia-cdi-refresh races driver init ~11s into boot; WSL2 2.7.0 + CUDA 12.8 is the known-good baseline, with documented systemd workarounds.**
Confirmed in microsoft/WSL #14452: CUDA graph capture failed with cudaErrorUnknown during capture on RTX 5090 + WSL2 before WSL 2.7.0; the workaround was vLLM --enforce-eager (disables CUDA graphs) at ~8x throughput loss. Two boot races: nvidia-cdi-refresh probes CUDA devices ~11s into boot and races Blackwell driver init (mask it by symlinking nvidia-cdi-refresh.path and.service to /dev/null + daemon-reload); CUDA services need ExecStartPre=/bin/sleep 45 to avoid racing dxgkrnl init. With WSL2 2.7.0 + CUDA 12.8, the rig is stable (issue reports ~140 tok/s Qwen3-14B-AWQ with full graphs). A measuring tool that runs at boot or that uses CUDA graphs can intermittently fail or hang on this exact rig class if the environment is below baseline.
- **Applies to:** windows-wsl2 · **Metric:** WSL2 2.7.0 fix; nvidia-cdi-refresh race ~11s; ExecStartPre sleep 45s; --enforce-eager ~8x throughput loss · **Confidence:** high
- **Design implication:** Profiler should (a) read WSL2 version and warn/lower confidence if < 2.7.0 on sm_120; (b) avoid CUDA-graph-dependent probes for the bandwidth bench (use plain cudaMemcpy timing) so it is immune to the graph-capture bug; (c) catch cudaErrorUnknown around any graph use and degrade gracefully rather than hang; (d) document the nvidia-cdi-refresh mask + ExecStartPre sleep 45 in setup notes if the profiler is ever run as a boot service; (e) if it cannot confirm a known-good environment, emit a low-confidence receipt rather than a falsely precise number.
- **Verify:** verdict=confirmed-with-fixes | oracle retrieval + family-different (mistral + granite)
- **Sources:** [WSL2 2.7.0 enables CUDA graph capture on RTX 5090 (Blackwell sm_120) — nvidia-cdi-refresh fix documented](https://github.com/Microsoft/WSL/issues/14452) — microsoft/WSL community 2025; WSL2 2.7.0; ~11s boot race; sleep 45; ~8x throughput loss; ~140 tok/s Qwen3-14B-AWQ after fix; SUPPORTED ; [CUDA on WSL User Guide — WDDM mode / supported GPUs](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — NVIDIA 2024; Pascal+; R495+ driver; WDDM only; SUPPORTED

