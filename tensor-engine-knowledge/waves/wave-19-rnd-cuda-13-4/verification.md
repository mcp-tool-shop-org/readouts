# Wave 19 — verification

**Proportional verification:**
- These are claims about a vendor's release, so the check is retrieval against the vendor's own pages.
- No model verifier ran. The R&D seat read both pages on 2026-10-20.

| Row | Checked against | Result |
|---|---|---|
| WDDM memory-pool IPC | [CUDA Toolkit 13.4 release notes](https://docs.nvidia.com/cuda/archive/13.4.1/cuda-toolkit-release-notes/index.html), New Features, CUDA Platform | stated: memory-pool IPC supported on Windows WDDM for stream-ordered allocations |
| Driver not bundled | same page, 2.2 CUDA Driver | stated: not bundled on Windows from 13.1, on Linux from 13.4 |
| cuda-checkpoint to storage | same page, New Features, CUDA Platform | stated |
| nvcc `--fmax-errors` and `--Wconversion` | [nvcc 13.4 documentation](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html), 4.2.8.7 and 4.2.8.11 | documented. Neither is described as new in 13.4, or as applying to device code |

## Corrections made to the bench copy

The rnd entry's three verified claims all cite the livestream slide:
1. **"-fmax-errors applies to device code; a narrowing-conversion warning."** The nvcc 13.4 docs document both
   options, but don't say they're new or device-code-specific. Loaded only as "documented".
2. **"IPC for stream-ordered memory pools on Windows WDDM."** Confirmed by the release notes.
3. **"Fabric Manager, IMEX and nvidia-fs posted separately from 13.4."** The release notes say the driver isn't
   bundled, on Windows since 13.1 and on Linux since 13.4. They don't name those components. Loaded as stated by the
   release notes.

The rnd entry is corrected on the bench in a follow-up change, which re-sources its claims to these pages.

**Net:** 4 rows, all stated by NVIDIA's pages; 2 of the entry's 3 claims restated; 8 slide-only items not loaded.
