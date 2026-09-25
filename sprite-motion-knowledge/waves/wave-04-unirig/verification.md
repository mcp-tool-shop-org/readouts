# Cross-family verification — UniRig deep dive (architecture · license · quality · integration)

Jury: **deepseek-v4-pro:cloud + glm-5.2:cloud + minimax-m3:cloud** (disjoint families, off-box via the local Ollama Cloud daemon) · 2026-06-25

Reasoning-stripped, refute-by-default PoLL re-adjudication of each recipe (existence / license / claim-support / currency). `verified=1` when the recipe is **measured-on-rig** (rig-authoritative — a web juror cannot see the rig, so it false-flags recent variants) OR a **clear majority confirms** (>=2 jurors, <=1 dissent). `refuted` (status `avoid`, kept visible) only when CORROBORATED — >=2 jurors not-found OR >=2 refute; a LONE dissent -> `unverified` lead (the agent's web source stands). A license flagged wrong is applied only toward MORE restrictive; a juror's looser read is recorded, never auto-upgrades commercial_use.

| Lane | confirmed | unverified | refuted | no-verdict |
|---|---|---|---|---|
| rigging | 7 | 1 | 0 | 0 |
| rigging | 5 | 1 | 0 | 0 |
| rigging | 5 | 0 | 0 | 0 |
| rigging | 5 | 1 | 0 | 0 |
| **total** | 22 | 3 | 0 | 0 |

_No recipe refuted — every recipe either confirmed (>=2 jurors) or held as an unverified lead._

## License corrections (the decisive axis)

| Lane | Recipe | commercial_use | Correction |
|---|---|---|---|
| rigging | UniRig stage 2: bone-point cross-attention skinning with geodesic distance refinement | conditional | Point Transformer V3 / SAMPart3D license is not MIT and must be verified independently; the recipe itself flags this but still claims commercial_use=yes which is premature.; commer |
| rigging | SkinTokens / TokenRig: unified autoregressive successor to UniRig (arXiv:2602.04805, 2026, MIT) | unknown | arXiv:2602.04805 corresponds to February 2026, which is a future date; no such paper or repo (VAST-AI-Research/SkinTokens) can be confirmed to exist. |
| rigging | SkinTokens / TokenRig — VAST-AI UniRig successor (arXiv Feb 2026, MIT) | unknown | No verifiable arXiv paper (2602.04805), GitHub repo, or model named SkinTokens/TokenRig from VAST-AI-Research exists; this appears to be a fabricated future model. |
| rigging | UniRig paper benchmarks — what the numbers mean and what they do not cover | unknown | The paper is not MIT-licensed; the recipe's license claim is inaccurate. The benchmark information itself is freely available but not under an MIT license. |
