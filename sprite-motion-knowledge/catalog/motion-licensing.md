# Motion data licensing doctrine
_How motion-capture DATA licensing actually works for shipping a commercial game: royalty-free vs no-raw-redistribution vs research-only; whether you may train a model on it; Mixamo must-incorporate; the AMASS-NC downstream-poison trap._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

8 recipes · 8 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | "Royalty-free" ≠ "do anything" — the Mixamo case | n/a | licensing | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 2 | Academic mocap datasets are non-commercial — AMASS, Human3.6M, HumanAct12 | n/a | licensing | ▸ reproduced | ⛔ no | 5 | 5 | ✓ |
| 2 | Creative Commons license variants — which are shippable in a commercial game | n/a | licensing | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 2 | Engine marketplace motion grants — incorporated-use only, no raw redistribution | n/a | licensing | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 2 | The SMPL / SMPL-X body-model poison — research-only even with clean motion data | n/a | licensing | ▸ reproduced | ⛔ no | 5 | 5 | ✓ |
| 2 | The non-commercial training-data poison rule (AMASS / HumanML3D) | n/a | licensing | ▸ reproduced | ⛔ no | 5 | 5 | ✓ |
| 2 | The safe-harbor recipe for shippable motion | n/a | all-motion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 6 | Data license governs — not the code license | n/a | licensing | · community | ⚠ cond | 5 | 5 | ✓ |

## Detail

### "Royalty-free" ≠ "do anything" — the Mixamo case · `recommended` · ▸ reproduced
**Mixamo animations are royalty-free for use in commercial games when incorporated as rendered output, but the raw FBX/BVH files cannot be redistributed, and bulk-downloading for ML training is explicitly prohibited.**
Adobe's Mixamo service grants a broad royalty-free license for commercial use of character animations inside shipped products — you may sell a game containing Mixamo-driven characters. The license has two hard limits: you cannot distribute the raw animation files as a standalone asset (e.g., as part of an asset pack, template, or to end-users), and you explicitly cannot use the content to train machine-learning models. The phrase 'royalty-free' means no per-unit payment, not that any use is permitted. Studios that want to use Mixamo clips as ML training data — to fine-tune a motion generator or build a retargeting dataset — cannot do so legally.
- **For the pipeline:** Mixamo is safe for in-game character animation (royalty-free commercial incorporation). It is NOT safe as a source of ML training data for motion generation. Do not include Mixamo clips in any training pipeline, even if the output model's code is MIT-licensed.
- **Engine:** n/a · **Applies to:** licensing · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **conditional** (license: Adobe Mixamo Terms of Service / Creative Cloud EULA) — Commercial use allowed only when animations are incorporated into the shipped product. Raw-file redistribution and ML training are prohibited regardless of commercial intent.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| cease-and-desist for using Mixamo BVH files as a motion-generator training corpus | interpreted 'royalty-free commercial use' as permission for any downstream purpose | never use Mixamo files as ML training data; use only for in-game character animation as incorporated output | commercial_use |

- **Best for:** license-audit (-, fit -) ; in-game-animation (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Mixamo FAQ — Licensing, Royalties, Ownership, EULA and TOS (Adobe Community)](https://community.adobe.com/t5/mixamo-discussions/mixamo-faq-licensing-royalties-ownership-eula-and-tos/td-p/13234775) (Adobe / Mixamo Team, 2023) — Animations may be used in commercial projects; raw file redistribution is prohibited; 'the only research application Mixamo content can't be used in is training machine-learning models.' ; [Mixamo License for Machine Learning Datasets (Adobe Community)](https://community.adobe.com/questions-696/mixamo-license-for-machine-learning-datasets-589715) (Adobe Support, 2022) — Bulk downloading Mixamo content to use for machine learning applications is explicitly not allowed under the license.

### Academic mocap datasets are non-commercial — AMASS, Human3.6M, HumanAct12 · `recommended` · ▸ reproduced
**AMASS, Human3.6M, and HumanAct12 are licensed for non-commercial scientific research only; using them — or any model trained on them — in a commercial game is a license violation.**
The three most widely-used academic motion-capture datasets all carry explicit non-commercial restrictions. AMASS (Max-Planck) prohibits commercial use and explicitly bans training ML models for commercial use. Human3.6M (IMAR Bucharest) limits access to academic institutions and prohibits commercial use. HumanAct12, co-authored with AMASS, inherits the same restriction. These datasets collectively underlie the vast majority of published text-to-motion and motion-diffusion research, making their non-commercial status a pipeline-wide concern, not a narrow edge case.
- **For the pipeline:** Treat any motion dataset that requires an academic-email access request, or that references Max Planck / IMAR licensing, as non-commercial until documented otherwise. Build a whitelist of confirmed-permissive datasets rather than a blacklist.
- **Engine:** n/a · **Applies to:** licensing · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **no** (license: AMASS Non-Commercial License (Max-Planck) / Human3.6M Academic License) — Non-commercial restriction applies to both direct use (training data) and to models whose weights were produced from these datasets.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| shipping a commercial title that used AMASS data in the motion pipeline | assumed academic-paper dataset availability implied permissive licensing | read every dataset's access agreement before incorporating into any pipeline step; require ps-license@tue.mpg.de commercial license for AMASS | commercial_use |

- **Best for:** license-audit (-, fit -) ; dataset-selection (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [AMASS Dataset License — Max-Planck-Gesellschaft](https://amass.is.tue.mpg.de/license.html) (MPI-IS / Max-Planck, 2023) — AMASS grants a non-exclusive, non-transferable right for non-commercial scientific research, education, or artistic projects only; 'this license also prohibits the use of the Dataset to train methods/algorithms/neural networks/etc. for commercial use of any kind.' ; [Human3.6M Dataset — License Overview (Encord summary citing official access terms)](https://encord.com/blog/15-best-free-pose-estimation-datasets/) (Encord / IMAR Bucharest, 2024) — Human3.6M licenses free of charge are limited to academic use only; the dataset may not be rented, leased, lent, sub-licensed, or transferred.

### Creative Commons license variants — which are shippable in a commercial game · `recommended` · ▸ reproduced
**CC0 and CC-BY are shippable in commercial games (with attribution for CC-BY); CC-BY-NC and CC-BY-ND are not — the NC variant explicitly prohibits commercial use and the ND variant blocks the derivatives any retargeting pipeline produces.**
Creative Commons offers a family of licenses with different commercial and derivative-work restrictions. CC0 (public domain dedication) waives all rights worldwide and permits any use including commercial without restriction. CC-BY 4.0 permits commercial use and adaptations, requiring only attribution. CC-BY-NC 4.0 explicitly prohibits use 'primarily intended for commercial advantage or monetary compensation' — a commercial Steam game is unambiguously commercial. CC-BY-ND 4.0 prohibits adapted or transformed works, which means retargeted or processed motion clips are technically derivative works and prohibited. CC-BY-SA requires derivatives to share the same license (copyleft), which is problematic for a shipped game binary. For motion data: only CC0 and CC-BY are safe for a commercial shipping pipeline.
- **For the pipeline:** When evaluating a motion dataset, map its CC variant to the above decision tree before ingesting. Treat CC-BY-NC, CC-BY-NC-SA, and CC-BY-ND as blockers. Treat CC0 and CC-BY as green with attribution tracking. Treat CC-BY-SA as needing legal review before use in shipped binary.
- **Engine:** n/a · **Applies to:** licensing · **Kind:** reference
- **VRAM:** n/a
- **Output license:** commercial **conditional** (license: Creative Commons License Suite (CC0, CC-BY, CC-BY-NC, CC-BY-ND, CC-BY-SA — each a distinct instrument)) — CC0: yes, unrestricted. CC-BY: yes with attribution. CC-BY-NC: no. CC-BY-ND: no (derivatives blocked). CC-BY-SA: requires legal review.
- **Fit:** rig 5/5 · studio 5/5
- **Best for:** license-audit (-, fit -) ; dataset-selection (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [CC0 1.0 Universal — Creative Commons](https://creativecommons.org/publicdomain/zero/1.0/) (Creative Commons, 2009) — CC0 dedicates the work to the public domain; you may copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission. ; [CC BY 4.0 — Creative Commons](https://creativecommons.org/licenses/by/4.0/) (Creative Commons, 2013) — CC BY 4.0 permits copying, adapting, and commercial distribution of the material, provided appropriate credit is given. ; [CC BY-NC 4.0 — Creative Commons](https://creativecommons.org/licenses/by-nc/4.0/) (Creative Commons, 2013) — CC BY-NC 4.0 explicitly prohibits use for commercial purposes, defined as 'primarily intended for commercial advantage or monetary compensation.'

### Engine marketplace motion grants — incorporated-use only, no raw redistribution · `recommended` · ▸ reproduced
**Fab (Epic/Unreal) and Unity Asset Store animation clips are licensed for commercial use only when incorporated into a shipped product; raw file redistribution and ML training are not permitted under the standard marketplace EULA.**
The Fab Standard License (which replaced the Unreal Engine Marketplace EULA in October 2024) permits commercial use of animation assets in games, films, and VFX projects across any engine. The Unity Asset Store EULA similarly permits commercial game use when assets are embedded in a shipped product. Both platforms share two hard limits: (1) you cannot redistribute the raw asset files as a standalone product (asset packs, templates, direct file delivery to customers), and (2) Fab assets tagged with the NoAI meta tag must not be used for generative AI data collection — meaning ML training is contingent on the absence of that tag. Neither marketplace explicitly grants ML training rights as a default. For Unity, this means the animation BVH or FBX cannot be extracted and sold or distributed separately. For Fab, a Standard License grants the purchaser rights to use in their project, not to re-sell the files.
- **For the pipeline:** Marketplace motion clips are safe for in-game character animation as long as the clips are baked into the shipped game (not distributed as separate downloadable files). They are not safe as ML training data unless the specific asset has no NoAI tag and the publisher explicitly permits it — check per-asset. Do not use marketplace clips as a training corpus for a motion generator.
- **Engine:** n/a · **Applies to:** licensing · **Kind:** reference
- **VRAM:** n/a
- **Output license:** commercial **conditional** (license: Fab Standard License (Epic Games) / Unity Asset Store EULA) — Commercial use allowed for incorporated in-game use. Raw file redistribution and ML training are excluded from the grant. Verify per-asset NoAI tagging on Fab.
- **License correction (verifier):** ML training is not universally prohibited under the standard Fab EULA; only assets with the NoAI meta tag are restricted. Unity's EULA does not explicitly address ML training. Raw redistribution is prohibited on both platforms.
- **Fit:** rig 5/5 · studio 5/5
- **Best for:** license-audit (-, fit -) ; in-game-animation (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed-with-fixes glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [license -> commercial_use=conditional] [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Fab Standard License — Epic Games](https://www.fab.com/eula) (Epic Games / Fab, 2024) — The Fab Standard License permits commercial use of assets in games, animations, and VFX; the NoAI meta tag indicates an asset must not be used for generative AI data collection. ; [Unity Asset Store Terms of Service and EULA](https://unity.com/legal/as-terms) (Unity Technologies, 2024) — Asset Store assets may be used in commercial games when incorporated and embedded in the shipped product; redistribution, resale, or sublicensing of the raw asset files is prohibited. ; [Licenses and Pricing in Fab — Epic Developer Community Documentation](https://dev.epicgames.com/documentation/fab/licenses-and-pricing-in-fab) (Epic Games, 2024) — The NoAI meta tag on Fab assets indicates the asset must not be used for generative AI data collection, restricting ML training use on a per-asset basis.

### The SMPL / SMPL-X body-model poison — research-only even with clean motion data · `recommended` · ▸ reproduced
**The SMPL and SMPL-X body models from Max Planck are research-only; any pipeline that emits or depends on SMPL/SMPL-X parameters is non-commercial regardless of the motion data's license, unless a separate commercial license is obtained via Meshcapade.**
SMPL (Skinned Multi-Person Linear Model, Loper et al., SIGGRAPH Asia 2015) and SMPL-X are parametric body models distributed under a Max Planck non-commercial research license. Practically every academic motion-capture dataset that has been fit to a body model uses SMPL parameters as its representation — AMASS stores motions as SMPL-H/SMPL-X sequences. Text-to-motion models that output joint rotations in SMPL format, or any retargeting pipeline that fits to SMPL, therefore carry this license even if the upstream motion data were permissive. The license prohibits commercial products, commercial services, and training commercial ML models. Commercial licensing is available through Meshcapade.com.
- **For the pipeline:** Audit every motion source for SMPL/SMPL-X dependency. Any pipeline step that fits to or emits SMPL parameters requires a Meshcapade commercial license. Prefer pipelines that output directly to skeleton formats (BVH, joint angles in engine-native rig) without SMPL as an intermediate representation.
- **Engine:** n/a · **Applies to:** licensing · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **no** (license: SMPL / SMPL-X Non-Commercial Research License (Max Planck Innovation)) — Commercial licensing available through Meshcapade.com (smpl@max-planck-innovation.de). Without it, any pipeline step touching SMPL/SMPL-X parameters is non-commercial.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| shipped a motion retargeting pipeline that uses SMPL as an intermediate representation without a Meshcapade commercial license | motion data was permissively licensed but body model was overlooked as a separate license layer | obtain Meshcapade commercial license or rebuild pipeline to output BVH/joint angles without SMPL intermediate | commercial_use |

- **Best for:** license-audit (-, fit -) ; pipeline-design (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [SMPL Model License — Max-Planck-Gesellschaft](https://smpl.is.tue.mpg.de/modellicense.html) (MPI-IS / Max-Planck Innovation, 2023) — The SMPL body model is licensed for non-commercial scientific research, non-commercial education, or non-commercial artistic projects only; any commercial use is prohibited; commercial licensing is available via Meshcapade. ; [SMPL-X Model License — Max-Planck-Gesellschaft](https://smpl-x.is.tue.mpg.de/modellicense.html) (MPI-IS / Max-Planck Innovation, 2023) — SMPL-X permits use 'for the sole purpose of performing non-commercial scientific research, non-commercial education, or non-commercial artistic projects'; incorporation in a commercial product or service is explicitly prohibited.

### The non-commercial training-data poison rule (AMASS / HumanML3D) · `recommended` · ▸ reproduced
**A generative motion model trained on non-commercial data (AMASS/HumanML3D) propagates that restriction to its outputs, so an MIT code license on a text-to-motion repo does NOT make its generated clips shippable in a commercial game.**
Most published text-to-motion models — MDM, MotionDiffuse, MoMask, T2M-GPT, and their derivatives — were trained on HumanML3D, which is built from AMASS and HumanAct12, both non-commercial. AMASS explicitly prohibits training commercial ML models. Even when the repo's source code is MIT/Apache, the weights encode the non-commercial training data and are therefore non-commercial by the terms of the upstream license. The generated motion clips themselves are outputs of those weights and inherit the same restriction. 'Clean code' does not launder unclean training data. The only safe generated motion is from a model with fully documented clean-data provenance.
- **For the pipeline:** For every generated-motion source — API or local model — trace the TRAINING SET before trusting the output. If the paper cites HumanML3D as its benchmark/training corpus, default to non-shippable. Require a written statement of clean-data provenance from any commercial motion-gen vendor before shipping.
- **Engine:** n/a · **Applies to:** licensing · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **no** (license: n/a — doctrine (AMASS NC + HumanML3D NC)) — Applies to any model trained on AMASS-derived data. The code license is irrelevant to the output's commercial usability.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| shipped generated motion that infringes AMASS terms because the code repo had an MIT license | trusted the code license without checking training data provenance | trace training set; require documented clean-data provenance; default generated motion to non-shippable absent proof | commercial_use |

- **Best for:** license-audit (-, fit -) ; motion-generation-vetting (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [AMASS Dataset License — Max-Planck-Gesellschaft](https://amass.is.tue.mpg.de/license.html) (MPI-IS / Max-Planck, 2023) — The AMASS license explicitly prohibits using the dataset to train methods or neural networks for commercial use of any kind. ; [HumanML3D: A Large and Diverse 3D Human Motion-Language Dataset (GitHub README)](https://github.com/EricGuo5513/HumanML3D) (Eric Guo et al., 2022) — HumanML3D is composed from AMASS and HumanAct12, both released for academic research only and free for non-commercial purposes; the repo's MIT code license does not override the dataset's non-commercial terms. ; [AMASS: Unified Motion Capture Dataset — Dataset Overview](https://www.roboticscenter.ai/datasets/amass-motion-capture) (Robotics Center AI / Max-Planck summary, 2024) — AMASS serves as the default training corpus for motion generation models (MDM, MotionDiffuse, MoMask); all carry the upstream non-commercial restriction.

### The safe-harbor recipe for shippable motion · `recommended` · ▸ reproduced
**The only unambiguously shippable motion pipeline for a commercial game combines: own-capture or confirmed-permissive source data (CMU mocap, CC0, CC-BY), zero SMPL/SMPL-X intermediate representation, and documented chain-of-title records for every asset.**
Given the license restrictions on academic datasets (AMASS, Human3.6M), body models (SMPL, SMPL-X), Mixamo ML training, and most text-to-motion outputs, the safe-harbor path for a commercial studio has three components. First, motion source: own-studio mocap (performer releases + ownership of the capture) or datasets with confirmed permissive terms — the CMU Motion Capture Database is explicitly 'free for use in research and commercial projects worldwide' with no additional restrictions. Second, body representation: avoid SMPL parameters as an intermediate; output directly to BVH or engine-native joint angles (or obtain a Meshcapade commercial license). Third, provenance records: maintain a per-asset chain-of-title document (source dataset or performer release → processing steps → final game asset) sufficient to answer a legal inquiry or a due-diligence question from an acquirer.
- **For the pipeline:** Build a motion asset registry that records for each animation: (a) source dataset or performer release date, (b) license name and URL, (c) processing steps applied, (d) body model used (if any) and its license status, (e) whether it has been cleared for commercial shipping. Default any undocumented asset to 'blocked' until cleared. Perform a clean-source audit before each gold release.
- **Engine:** n/a · **Applies to:** all-motion · **Kind:** reference
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a — doctrine (CMU open + CC0 + own-capture)) — Applies when all three conditions are met: permissive source, no non-commercial body model, and documented chain of title. Any gap defaults the asset to non-shippable.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| failed IP due diligence before an acquisition or publishing deal because motion assets lack provenance records | no chain-of-title documentation maintained during development | establish motion asset registry at project start; retroactively audit and document existing assets; block undocumented assets from gold build | commercial_use |

- **Best for:** pipeline-design (-, fit -) ; release-readiness (-, fit -) ; legal-due-diligence (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [CMU Motion Capture Database — READMEFIRST (BVH conversion by Bruce Hahne)](https://github.com/una-dinosauria/cmu-mocap/blob/master/READMEFIRST.txt) (Carnegie Mellon University / Bruce Hahne, 2003) — CMU mocap data is 'free for use in research and commercial projects worldwide'; the BVH conversion places no additional restrictions; attribution to mocap.cs.cmu.edu and NSF EIA-0196217 is requested for publications. ; [CC0 1.0 Universal — Creative Commons](https://creativecommons.org/publicdomain/zero/1.0/) (Creative Commons, 2009) — CC0 permits all uses including commercial with no restrictions. ; [SMPL Model License — Max-Planck-Gesellschaft (commercial licensing via Meshcapade)](https://smpl.is.tue.mpg.de/modellicense.html) (MPI-IS / Max-Planck Innovation, 2023) — Commercial licensing for SMPL is available through Meshcapade.com, providing the clean-body-model path for studios that require SMPL-based pipelines.

### Data license governs — not the code license · `recommended` · · community
**An MIT or Apache LICENSE file in a motion-gen repo covers the source code only; the trained weights and the dataset used to produce them are governed by their own separate instruments, which may be strictly non-commercial.**
Open-source code licenses (MIT, Apache 2.0, BSD) attach to software source text — algorithms, training scripts, inference code. They say nothing about the legality of the weights produced by running that code, nor about the dataset the code consumed. When a text-to-motion repo ships an MIT LICENSE, that license covers the Python files. The HumanML3D data it trained on is non-commercial (AMASS terms), and the SMPL parameters it emits are research-only (Max Planck terms). A commercial studio that ships generated clips from such a model has violated two separate instruments while correctly reading the code license. This confusion is the primary trap in the motion-generation space.
- **For the pipeline:** For every motion source — library, generative model, or dataset — evaluate THREE licenses independently: (1) the code/tool license, (2) the data/dataset license, (3) the body-model or output-representation license. Only when all three are green does the source become shippable.
- **Engine:** n/a · **Applies to:** licensing · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **conditional** (license: n/a — doctrine) — Conditional on all three license layers being permissive. The code being MIT is necessary but not sufficient.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| ship motion clips from a 'MIT-licensed' generative model and receive a cease-and-desist from Max Planck | confused the code license for the data and body-model license | audit all three license layers; treat non-MIT data/body-model as non-commercial regardless of code license | commercial_use |

- **Best for:** license-audit (-, fit -) ; due-diligence (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Licensing Machine Learning Models — The Turing Way](https://book.the-turing-way.org/reproducible-research/licensing/licensing-ml/) (The Turing Way Community, 2024) — Different components of an ML system (data, source code, weights, applications) may have separate licenses; a permissive code license does not govern the dataset or the weights produced from it.

