# Cross-family verification — Foundation — the sprite-motion pipeline (architecture · rigging · AI-motion · inbetween · cloud · combat · verify)

Jury: **deepseek-v4-pro:cloud + glm-5.2:cloud + minimax-m3:cloud** (disjoint families, off-box via the local Ollama Cloud daemon) · 2026-06-24

Reasoning-stripped, refute-by-default PoLL re-adjudication of each recipe (existence / license / claim-support / currency). `verified=1` when the recipe is **measured-on-rig** (rig-authoritative — a web juror cannot see the rig, so it false-flags recent variants) OR a **clear majority confirms** (>=2 jurors, <=1 dissent). `refuted` (status `avoid`, kept visible) only when CORROBORATED — >=2 jurors not-found OR >=2 refute; a LONE dissent -> `unverified` lead (the agent's web source stands). A license flagged wrong is applied only toward MORE restrictive; a juror's looser read is recorded, never auto-upgrades commercial_use.

| Lane | confirmed | unverified | refuted | no-verdict |
|---|---|---|---|---|
| ai-motion | 9 | 0 | 0 | 0 |
| cloud-workers | 7 | 0 | 0 | 0 |
| combat-craft | 9 | 0 | 0 | 0 |
| inbetween | 6 | 2 | 0 | 0 |
| motion-arch | 9 | 0 | 0 | 0 |
| motion-verify | 10 | 0 | 0 | 0 |
| rigging | 10 | 0 | 0 | 0 |
| **total** | 60 | 2 | 0 | 0 |

_No recipe refuted — every recipe either confirmed (>=2 jurors) or held as an unverified lead._

## License corrections (the decisive axis)

| Lane | Recipe | commercial_use | Correction |
|---|---|---|---|
| inbetween | Practical-RIFE v4.x (hzwer / Megvii, ECCV 2022) — smooth low-displacement motion | conditional | Commercial use is 'yes' (MIT license for both code and weights), not 'conditional'.; claimed_commercial_use should be 'yes' not 'conditional'; MIT explicitly permits commercial use |
| inbetween | EMA-VFI: Extracting Motion and Appearance via Inter-Frame Attention (CVPR 2023) | conditional | Commercial use is 'yes' (Apache-2.0 license), not 'conditional'. |
| motion-verify | Foot-contact / no-slide detector | conditional | RAFT code (princeton-vl/RAFT) is MIT-licensed, not Apache-2.0. Correct claimed_license to 'MIT (RAFT code)'; weights remain research-use so commercial_use stays conditional.; RAFT  |
| motion-verify | Frame-to-frame temporal LPIPS / SSIM consistency | yes | torchmetrics is Apache-2.0, not BSD/MIT; scikit-image is BSD-3-Clause, not MIT. LPIPS (lpips package) is BSD-2-Clause. |
| motion-verify | Optical-flow warping error for temporal coherence | conditional | RAFT code is MIT-licensed at princeton-vl/RAFT, not BSD-3-Clause. Update claimed_license to 'MIT (RAFT code); weights research-use, check repo for current terms'. |
| rigging | UniRig — VAST-AI/Tsinghua autoregressive skeleton predictor (SIGGRAPH 2025, MIT) | conditional | Verify the actual license file on github.com/VAST-AI-Research/UniRig and the model card on HuggingFace (VAST-AI/UniRig) before claiming weights are MIT; research repos often releas |
