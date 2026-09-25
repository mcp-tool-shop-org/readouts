# Cross-family verification — Commercial motion sources & data (mocap libraries · datasets · text-to-motion · driving video · retarget · licensing)

Jury: **deepseek-v4-pro:cloud + glm-5.2:cloud + minimax-m3:cloud** (disjoint families, off-box via the local Ollama Cloud daemon) · 2026-06-24

Reasoning-stripped, refute-by-default PoLL re-adjudication of each recipe (existence / license / claim-support / currency). `verified=1` when the recipe is **measured-on-rig** (rig-authoritative — a web juror cannot see the rig, so it false-flags recent variants) OR a **clear majority confirms** (>=2 jurors, <=1 dissent). `refuted` (status `avoid`, kept visible) only when CORROBORATED — >=2 jurors not-found OR >=2 refute; a LONE dissent -> `unverified` lead (the agent's web source stands). A license flagged wrong is applied only toward MORE restrictive; a juror's looser read is recorded, never auto-upgrades commercial_use.

| Lane | confirmed | unverified | refuted | no-verdict |
|---|---|---|---|---|
| driving-video | 8 | 0 | 0 | 0 |
| mocap-datasets | 9 | 0 | 0 | 0 |
| mocap-libraries | 9 | 0 | 0 | 0 |
| motion-gen | 7 | 0 | 1 | 0 |
| motion-licensing | 8 | 0 | 0 | 0 |
| retarget | 8 | 0 | 0 | 0 |
| **total** | 49 | 0 | 1 | 0 |

_No recipe refuted — every recipe either confirmed (>=2 jurors) or held as an unverified lead._

## License corrections (the decisive axis)

| Lane | Recipe | commercial_use | Correction |
|---|---|---|---|
| driving-video | Mixamo animations — prohibited for AI input/driving (Adobe explicit restriction) | conditional | The cited Adobe FAQ explicitly prohibits only 'training machine-learning models' — not 'driving signal' or inference-time use. Extending the restriction to all AI input/driving ove |
| motion-licensing | Engine marketplace motion grants — incorporated-use only, no raw redistribution | conditional | ML training is not universally prohibited under the standard Fab EULA; only assets with the NoAI meta tag are restricted. Unity's EULA does not explicitly address ML training. Raw  |

## Fabrication caught & dropped (the jury's crown-jewel catch)

The `motion-gen` agent fabricated a plausible-but-nonexistent model — **Kimodo ("NVIDIA Kinematic Motion Diffusion, Rempe et al. 2026")** — and presented it as the lone commercially-clean text-to-motion path. The cross-family jury REFUTED it (deepseek-v4-pro + glm-5.2 both returned `not-found`): the arXiv id (2603.15546), the GitHub repo (nv-tlabs/kimodo), the 'Bones Rigplay' / 'BONES-SEED' datasets, and the March-2026 release date are all unverifiable. Per the fabricated->drop rule it was removed from the catalog; this record preserves the catch. **Net: there is no verified commercially-clean generated-motion path — generated motion stays prototyping-only.**
