# Wave 20 — promoted from rnd: CUDA Python libraries on the RTX 5090

**Promotion wave** · 2026-10-20 · **not a research swarm.** This wave promotes the rnd entry
[`2026-10-20-cuda-python-on-5090`](https://github.com/mcp-tool-shop-org/rnd/blob/main/entries/2026/2026-10-20-cuda-python-on-5090.md)
and its rung folder,
[`experiments/cuda-python-5090-rung`](https://github.com/mcp-tool-shop-org/rnd/tree/main/experiments/cuda-python-5090-rung).
The R&D seat chose it from the 2026-10-20 promotion queue. It is the installability gate for rnd-data's optional GPU
layer.

## What it adds (3 rows in `sources`, lane runtime-foundations)

| Row | Evidence |
|---|---|
| Six CUDA Python libraries run a correct kernel at compute capability 12.0: cuda.core, CuPy, numba-cuda, cuda.compute, nvmath-python and cuTile, with exact pins | the smoke rung, 2026-10-19: both runs' result rows and the environment freeze |
| numba-cuda 0.30.4 with numba 0.68.0 fails on NumPy 2.5 (`row_stack` was removed), so hold `numpy<2.5` | the same rung, run on NumPy 2.5.4 and on 2.4.6 |
| CuPy 14.2.0 uses its own built-in CUDA 13.2 runtime; NVRTC and cuBLASLt come from the 13.x wheels | a DLL listing under the Publisher's GPU grant, 2026-10-20 |

**For the rig:** cuTile runs on consumer Blackwell, and a shared GPU environment must pin NumPy below 2.5 while numba
is in it.

**Licences:** the libraries are Apache-2.0, MIT and BSD-2-Clause. The CUDA runtime wheels they pull carry NVIDIA's
[CUDA EULA](https://docs.nvidia.com/cuda/eula/index.html). Depend on the wheels from PyPI; never vendor them.

## The honest limit

- A smoke rung: one small kernel per library. It shows each library installs and runs here. It says nothing about
  speed, or which features rnd-data should build on.
- One rig, one driver (617.42), one Python version.

## Method

The R&D seat ran the rung on 2026-10-19 (threads capped at 4, peak VRAM about 340 MiB above idle) and the CuPy
follow-up on 2026-10-20. Both are committed in rnd with their scripts and outputs. See
[verification.md](verification.md).
