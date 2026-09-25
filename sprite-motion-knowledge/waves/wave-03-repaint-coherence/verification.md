# Cross-family verification — Painterly repaint & temporal coherence (controlnet · style · identity · weapon-composite · temporal · repaint-eval)

Jury: **deepseek-v4-pro:cloud + glm-5.2:cloud + minimax-m3:cloud** (disjoint families, off-box via the local Ollama Cloud daemon) · 2026-06-25

Reasoning-stripped, refute-by-default PoLL re-adjudication of each recipe (existence / license / claim-support / currency). `verified=1` when the recipe is **measured-on-rig** (rig-authoritative — a web juror cannot see the rig, so it false-flags recent variants) OR a **clear majority confirms** (>=2 jurors, <=1 dissent). `refuted` (status `avoid`, kept visible) only when CORROBORATED — >=2 jurors not-found OR >=2 refute; a LONE dissent -> `unverified` lead (the agent's web source stands). A license flagged wrong is applied only toward MORE restrictive; a juror's looser read is recorded, never auto-upgrades commercial_use.

| Lane | confirmed | unverified | refuted | no-verdict |
|---|---|---|---|---|
| identity-preserve | 6 | 2 | 0 | 0 |
| repaint-controlnet | 7 | 1 | 0 | 0 |
| repaint-eval | 5 | 3 | 0 | 0 |
| style-injection | 8 | 0 | 0 | 0 |
| temporal-coherence | 8 | 0 | 0 | 0 |
| weapon-composite | 8 | 0 | 0 | 0 |
| **total** | 42 | 6 | 0 | 0 |

_No recipe refuted — every recipe either confirmed (>=2 jurors) or held as an unverified lead._

## License corrections (the decisive axis)

| Lane | Recipe | commercial_use | Correction |
|---|---|---|---|
| identity-preserve | PuLID-Flux with FaceNet backend — commercial-safe face-ID conditioning | no | The arXiv 2404.16022 PuLID paper and the lldacing/ComfyUI_PuLID_Flux_ll plugin both exist, but the 'PuLID-Flux II' name and the claim that the plugin ships a 'FaceNet-based face an |
| identity-preserve | Face-restoration avoidance — GFPGAN / CodeFormer WRONG for painterly sprites | no | GFPGAN's code AND its shipped pretrained face-restoration weights are Apache 2.0 (TencentARC/GFPGAN LICENSE) — there is no NC-flagged dependency in the main package. CodeFormer und |
| repaint-eval | Temporal-flicker metric for repainted cycle (LPIPS frame-delta + optical-flow warping error) | conditional | RAFT original repo (princeton-vl/RAFT) does not carry an Apache-2.0 license; use torchvision's RAFT implementation (BSD-3-Clause) for commercial-clean access. The RWE citation (arX |
| temporal-coherence | AnimateDiff temporal module for vid2vid repaint (not generation) | conditional | AnimateDiff motion module is Apache-2.0, which permits commercial use; base SDXL/SD1.5 also allow commercial use. Changed commercial_use from 'conditional' to 'yes'. |
| temporal-coherence | RAFT optical flow warp-and-blend for temporal smoothing post-pass | conditional | RAFT code and weights are BSD-3-Clause, which allows commercial use. Changed commercial_use from 'conditional' to 'yes'. |
| weapon-composite | Extract weapon mask from Blender mesh via Cryptomatte / Object-Index pass | yes | Blender is GPL-2.0/3.0, not Apache-2.0. The output/render exemption (Blender's longstanding policy that rendered output is not bound by the GPL) does make commercial use of the ren |
