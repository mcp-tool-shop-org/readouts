# Wave 03 — Painterly repaint & temporal coherence

**KB #9 `sprite-motion-knowledge` · dispatched 2026-06-25 · 6 parallel lane agents (Sonnet), web-grounded + license-verified.**
Verification receipt (cross-family PoLL jury): [`verification.md`](verification.md). Raw verified output: [`research-raw.json`](research-raw.json).

The wave that closes the **§D style gap**. The captain prototype proved a TRELLIS.2 mesh → 8-view Blender render keeps
the **weapon rigid and the face intact** — but the render has a "3D game-render" look, not the painterly house style.
*"The one gap = STYLE: the remaining build is the repaint pass."* This wave is that pass — and its hard extension to
motion (holding style + identity across 8 directions AND animation frames). Waves 1–2 gave the tools + the content;
this wave is the **AI-polish middle of the spine** (`motion truth → AI repaint → sprite-sheet → verify`).

## The 6 lanes — findings → recommendation

**1. `repaint-controlnet` — structure-preserving repaint.** Render the **depth / normal / lineart pass DIRECTLY from
the mesh** (you own the geometry — cleaner than estimated depth, locks pose + weapon), then img2img over the mesh render
with **Qwen-Image-Edit-2511 + InstantX ControlNet-Union** (both Apache) at mid denoise. The governing principle:
**structure from ControlNet, style from the LoRA** — the decomposition that prevents drift. (xinsir controlnet-union-sdxl
is the Apache SDXL alternative; ControlNet v1.1 models are OpenRAIL-M; UltimateSDUpscale is GPL.) → The core repaint.

**2. `style-injection` — landing the house style.** Apply the studio **sfhd_style LoRA** during the repaint (style half
of the decomposition); **IP-Adapter Plus** style-transfer + **B-LoRA** content/style separation (validates the studio's
separated-LoRA approach); tuned **denoise windows** (~0.55–0.75 body, 0.25–0.45 face/weapon); **Reinhard L\*a\*b\*
palette transfer** as a zero-VRAM palette-lock post-pass. Watch base-checkpoint license inheritance; FaceID paths NC. →
House LoRA + palette-lock is the spine; IP-Adapter for reference matching.

**3. `identity-preserve` — keep the approved face.** The clean default is **masked-face differential-denoise** (face
at low denoise ~0.2–0.3, body higher — no face-recognition weights, so commercial-clean), building on the studio's
**de-lit face-preserve** pass. **3 face-ID paths are commercial-blocked** — IP-Adapter-FaceID (InsightFace NC), InstantID
(AntelopeV2 NC despite Apache code), ArcFace (NC weights); GFPGAN/CodeFormer are `avoid` (NC **and** they destroy
painterly style toward photoreal). → Mask + differential denoise; never a photoreal face-restorer.

**4. `weapon-composite` — §D Lane B (preferred for the pirate pack).** The **Blender material-ID / Cryptomatte pass**
gives a pixel-exact weapon matte for free at render time (no ML, deterministic across all 8 views) — beating SAM2 (the
RGB-only fallback). **MediaPipe** grip-keypoint alignment → alpha-composite the rigid weapon onto the validated painterly
body → **low-denoise (<0.3) ControlNet-tile harmonize on the weapon mask ONLY** (adopts brushwork without re-imagining
geometry) → Poisson seam at the hand contact → **Blender Z-depth pass** for per-view occlusion. A roster **subsystem-
routing gate** sends body-attached/sheathed weapons through plain NVS and only externally-projected props through this
lane. → Composite the rigid mesh weapon; never let diffusion re-imagine the blade.

**5. `temporal-coherence` — the motion-specific hard part (partially solved, stated honestly).** First-line:
**batch-consistent conditioning** (fixed seed + LoRA + per-frame ControlNet across all frames/directions). Then
**reference-frame IP-Adapter propagation** + **TokenFlow** (training-free feature propagation) for identity lock;
**AnimateDiff vid2vid** / **Wan2.1 VACE** (Apache, the commercial-safe video option) for joint processing; **RAFT
optical-flow** warp-blend + deflicker post-pass for residual shimmer. **The 8-direction identity problem is not fully
solved** — perfect cross-direction coherence on a stylized repaint remains open; set QA expectations accordingly. →
Batch-consistent + reference-propagation now; expect a manual cleanup tail.

**6. `repaint-eval` — the repaint admission gate (extends wave-1 `motion-verify`).** **SigLIP2 style-match to the house
baseline** (the core "did it land painterly" gate, via ai-eyes-mcp); identity via **CLIP/DINO face-crop** (ArcFace NC →
fallback); **weapon-rigidity** reuse of the wave-1 length/tip detector; **over-smoothing** via Laplacian-variance / GLCM;
**palette adherence** via Lab-histogram EMD; **temporal flicker** via frame-LPIPS + RAFT warping error; the **cross-family
vision-LLM jury** (the studio's `_concept_vision_qa` — minimax/kimi/gemini, gemini the strict canary) for the
"painterly / not-anime / on-model" call; all wired into one **accept/reject gate** with per-character thresholds. → The
gate that lets a repaint reach the sprite sheet.

## The assembled §D repaint recipe (the wave's synthesis)

```
TRELLIS.2 mesh  →  Blender render + AUX passes (depth · normal · material-ID matte · Z-depth)
   →  ControlNet-depth+tile repaint on Qwen-Image-Edit-2511 + sfhd_style LoRA   (structure from CN, style from LoRA)
   →  masked-face differential-denoise (low-denoise face)                        (identity, commercial-clean)
   →  WEAPON: material-ID matte → align → alpha-composite → low-denoise tile-harmonize   (§D Lane B, weapon stays rigid)
   →  batch-consistent conditioning across 8 dirs + frames → RAFT/deflicker        (temporal coherence; manual tail)
   →  repaint-eval gate: SigLIP2 style-match + identity + weapon-continuity + over-smoothing + palette + flicker + vision jury
   →  painterly, on-model, weapon-rigid sprite sheet
```

Every block is commercial-clean (Qwen-Edit / InstantX-ControlNet / SAM2 / Wan2.1-VACE Apache; Blender output unrestricted;
the house LoRA studio-owned) **except** the NC face-ID shortcuts, which the clean masked-face path routes around.

## Cross-KB seams

Builds on wave 1 (the rig-truth mesh render it repaints + `motion-verify` it extends) and the proven captain mesh-path
(`rigging` v_proven). Points at `sprites-knowledge` (static-sprite repaint shares these ControlNet/LoRA mechanics),
`model-knowledge` (weights), never restated. Verification: cross-family PoLL jury (`deepseek-v4-pro` + `glm-5.2` +
`minimax-m3`) — see [`verification.md`](verification.md).
