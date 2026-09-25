# Wave 04 — UniRig deep dive

**KB #9 `sprite-motion-knowledge` · dispatched 2026-06-25 · focused 4-agent deep-dive swarm (Sonnet) on ONE tool.**
Verification receipt (cross-family PoLL jury): [`verification.md`](verification.md). Raw verified output: [`research-raw.json`](research-raw.json).

A targeted enrichment of the `rigging` lane: 25 recipes investigating **UniRig** (`VAST-AI-Research/UniRig`, Tsinghua +
Tripo/VAST-AI, SIGGRAPH 2025) — the studio's auto-rig backbone for the mesh game-asset line. Complements the two
pre-existing recipes (`unirig-blackwell-wsl2-skeleton-skin-measured` = the measured-on-rig WSL2/Blackwell install;
`unirig-ai-auto-rigger-mit` = the wave-1 overview) without duplicating them.

## The 4 facets — findings

**Architecture & models (8).** Two stages: (1) **autoregressive skeleton prediction** — an OPT-125M decoder over a
**tokenized skeleton tree** (DFS order, 256-bin coord discretization, type/template/branch tokens) conditioned on a
3DShape2Vecset shape encoding of a 65k-point cloud; (2) **bone-point cross-attention skinning** (Point Transformer V3 +
bone MLP + voxel-geodesic distance) → per-vertex weights, with failure propagating skeleton→skin. I/O: OBJ/FBX/GLB/VRM
in, Y-up, no watertight requirement, three-script inference (skeleton → skin → merge) → merged rigged GLB. Downloadable
now: the **Articulation-XL2.0 checkpoint** (~11.5 GB, separate skeleton/ + skin/); Rig-XL + VRoid variants "coming
soon." Paper: **arXiv:2504.12451** (DOI 10.1145/3730930) — and the swarm caught that the **existing wave-1 recipe's
author citation was wrong** (correct: Zhang, Pu, Guo, Cao, Hu — not "Wang, Lingteng").

**License & commercial (5) — the decisive verdict: GO.** MIT on **both** the GitHub code (raw LICENSE confirmed) **and**
the released HuggingFace weights (VAST-AI/UniRig card) — the only SIGGRAPH-class AI auto-rigger the studio can ship
commercially with zero license obligation; rigged GLB/FBX output is the studio's own IP. One due-diligence note: the
training data is **Articulation-XL2.0 (CC-BY-4.0, from Objaverse-XL)** — NC-propagation-to-outputs is unsettled law, but
VAST-AI's MIT weight release is the operative grant. **Operational rule: pin the checkpoint by HF commit hash** (MIT is
irrevocable on the granted artifact; verify the unreleased Rig-XL checkpoint's license independently before pulling it).

**Quality, limitations & alternatives (6) — honest ceiling.** Geometry-predicted skeletons make UniRig the right tool
for the exotic species (tortle/kenku/sahuagin) that humanoid-template riggers can't touch — but the output is an
**80-90% draft**: five sourced failure modes (premature chain termination, spatial discontinuity, mis-placed limb
bones, joint skinning artifacts, stylized-proportion breakdown; Auto-Connect arXiv:2506.11430 + the README). The
headline 215%/194% benchmark numbers are on **VRoid anime + Objaverse**, not TRELLIS creature meshes — expect a ~20% OOD
gap. So: **decimate the dense TRELLIS mesh (800k → 30-50k tris)**, run UniRig, then a **~30-60 min/species manual
cleanup** (extend tail/wing chains, re-parent, fix roll axes, re-run skin). Comparison table vs Rigify / AccuRIG /
Auto-Rig-Pro / Mixamo / Blender automatic-weights with a when-to-use-which decision tree.

**Integration & ecosystem (6).** The studio slot: TRELLIS.2 GLB → `generate_skeleton.sh` → `generate_skin.sh` →
`merge.sh` → rigged GLB → append the `weapon_grip→weapon_tip` rigid chain → Blender NLA actions → 8-dir render.
Corrections from the swarm: the **"Blender addon" is a narrow VRM-I/O fork**, NOT a rig-in-Blender button (studio_fit
low); a **real, maintained ComfyUI wrapper exists** (`PozzettiAndrea/ComfyUI-UniRig`, GPL-3.0, 16 nodes, outputs not
GPL-encumbered). **UniRig's bone names are non-standard** → a one-time ARP/Blender **remap preset per species family** is
required before wave-2 mocap (Mixamo/CMU/100STYLE) can retarget onto a UniRig skeleton. Verified successor:
**SkinTokens/TokenRig** (arXiv:2602.04805, Feb 2026, MIT — unifies skeleton+skin into one token stream; watch, not yet
rig-measured).

## Net for the studio

UniRig is **commercial-clean (MIT code+weights), confirmed** — ship UniRig-rigged assets freely. It is the auto-rig
**first pass** for every non-humanoid roster mesh (the one tool that handles arbitrary topology), producing an 80-90%
draft that needs a short Blender cleanup + a per-species mocap-remap preset. Pin the checkpoint by commit hash; watch
SkinTokens as the successor. Pairs with the measured WSL2/Blackwell install recipe + the weapon_grip rigid chain.

## Provenance

All 25 recipes route to the `rigging` lane (wave 4), cross-referencing the two pre-existing UniRig recipes + the
`weapon-grip-rigid-bone-chain`. Verified by the cross-family PoLL jury (`deepseek-v4-pro` + `glm-5.2` + `minimax-m3`) —
see [`verification.md`](verification.md). Recent 2026 papers (Auto-Connect, SkinTokens) postdate the jurors' training,
so the live retrieval is the currency authority; the jury down-weights to `unverified` rather than refuting what it
cannot confirm.
