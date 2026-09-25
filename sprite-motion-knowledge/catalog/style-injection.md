# House-style injection
_Applying the painterly house style during repaint: the studio sfhd_style LoRA, IP-Adapter style-reference, img2img denoise ranges, content/style separation, palette/color-grade matching to the approved look._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

8 recipes · 6 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | B-LoRA: content/style-separated LoRA training (SDXL blocks 4 + 5) | comfyui | LoRA training and inference — separate style injection from content fidelity on SDXL | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 2 | House-palette color-grade transfer — post-repaint color lock | comfyui | post-repaint pass — runs after the LoRA/IP-Adapter repaint to lock output to the approved house palette | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | IP-Adapter Plus — style-transfer mode from a reference sprite | comfyui | repaint — inject painterly style from an approved reference sprite; complements ControlNet structure | ▸ reproduced | ⚠ cond | 5 | 4 | ✓ |
| 2 | Studio house-style LoRA injected during the repaint pass | comfyui | repaint — any frame: idle, walk, attack, death; works alongside ControlNet-depth | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | img2img denoise strength — style/fidelity tradeoff window | comfyui | any img2img repaint pass; tuning the balance between injected style and preserved mesh layout | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 6 | Avoiding style-bleed and over-stylization — selective block targeting for LoRAs | comfyui | LoRA inference — prevent house LoRA from over-stylizing face or weapon regions | · community | ✅ yes | 5 | 5 | ✓ |
| 8 | IP-Adapter Style & Composition SDXL — combined style + layout control | comfyui | repaint — when both style AND loose layout need to be taken from the reference, not just style | · single-run | ⚠ cond | 5 | 3 | ✓ |
| 10 | Reference-only ControlNet — self-attention style injection without a structural map | comfyui | repaint — inject style feel from a reference sprite when no structural map is desired or when pairing with depth ControlNet at low weight | · community | ⚠ cond | 5 | 3 | ✓ |

## Detail

### B-LoRA: content/style-separated LoRA training (SDXL blocks 4 + 5) · `recommended` · ▸ reproduced
**B-LoRA trains LoRA weights on only two specific SDXL transformer blocks (block 4 = content, block 5 = style), achieving implicit style/content separation that allows the style B-LoRA to be applied alone without the content B-LoRA modifying the character's identity.**
Frenkel et al. (ECCV 2024) discovered that jointly training LoRA on SDXL transformer blocks 4 and 5 implicitly separates content (block 4: ΔW⁴ → semantic structure) from style (block 5: ΔW⁵ → visual texture/palette/brushwork). Once trained, the two B-LoRAs can be used independently: apply only the style B-LoRA (block 5) to repaint a new character in the house style without pulling in the training image's content. The studio's existing content/style-separated LoRA approach is a practical instantiation of this principle. Training targets only these two blocks rather than full cross-attention — reducing overfitting on small datasets. Inference: load only the style B-LoRA at weight 0.8–1.2 to inject painterly appearance while the content path remains free for the mesh render.
- **For the pipeline:** Directly validates the studio's content/style-separated LoRA approach. When retraining sfhd_style or building pack-specific style variants, target only block 5 as the style adapter; keep block 4 content-neutral or separate it into its own adapter for character-identity injection. This enables mixing style from one reference with character identity from another — critical for the studio's multi-pack sprite consistency.
- **Engine:** comfyui · **Applies to:** LoRA training and inference — separate style injection from content fidelity on SDXL · **Base:** SDXL · **Kind:** technique
- **VRAM:** 12-24
- **Output license:** commercial **conditional** (license: Technique is research (ECCV 2024, no license constraint on the method); implementation inherits SDXL base license) — The B-LoRA method itself is published research — free to implement. The trained B-LoRA weights inherit the BASE SDXL checkpoint license used during training. Studio-trained B-LoRA on a commercial-clean SDXL base is commercially clean. Paper code at b-lora.github.io does not carry a restrictive license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| train_blocks: [4, 5] only (joint training required for separation to emerge) |  | ○ |  |
| style_lora_weight at inference: 0.8–1.2 |  | ○ |  |
| content_lora_weight: 0.0 when doing style-only injection |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Training blocks 4 and 5 independently (not jointly) fails to produce separation — joint training is required |  |  |  |
| Training on a highly-stylized custom checkpoint causes style-bleed from the base into the B-LoRA |  |  |  |
| Does not help if the studio's base model already has strong style baked in — style B-LoRA competes with base style |  |  |  |

- **Best for:** style-content-separation (-, fit -) ; targeted-style-injection (-, fit -) ; lora-architecture (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Implicit Style-Content Separation using B-LoRA](https://arxiv.org/abs/2403.14572) (Yarden Frenkel, Yael Vinker, Ariel Shamir, Daniel Cohen-Or, 2024) — Jointly training LoRA on SDXL transformer blocks 4 (content) and 5 (style) achieves implicit style-content separation; block 5 B-LoRA encodes visual appearance/texture independently of content. ECCV 2024. ; [B-LoRA project page](https://b-lora.github.io/B-LoRA/) (Yarden Frenkel, Yael Vinker, Ariel Shamir, Daniel Cohen-Or, 2024) — Confirms block identities (block 4 = content ΔW⁴, block 5 = style ΔW⁵); demonstrates style transfer, text-based stylization, style-content mixing tasks.

### House-palette color-grade transfer — post-repaint color lock · `recommended` · ▸ reproduced
**A Reinhard L*a*b* color transfer from a house-palette reference image, run post-repaint, corrects generation-drift and locks every output frame to the studio's approved color signature without re-running the full diffusion pass.**
After the LoRA/IP-Adapter repaint pass, generation drift can shift colors away from the approved palette — particularly hue and saturation. The Reinhard (2001) algorithm matches the mean and standard deviation of L*, a*, b* channels between the repainted frame and a curated house-palette reference sprite. The jrosebr1/color_transfer Python library (MIT, pip-installable) implements this efficiently without per-pixel lookup. Run as a ComfyUI custom node or a standalone post-process script. A second option is GIMP/Photoshop Indexed Mode (manual workflow for QA) which forces output to a hard palette via quantization. For a 2.5D sprite at 512×512, color transfer runs in milliseconds — suitable for batch processing all animation frames.
- **For the pipeline:** Acts as the palette QA gate at the end of the repaint pipeline: ensures no frame ships with an out-of-palette color signature. Particularly important for the studio since multiple packs must share a consistent palette across face, armor, weapon, and background. Run after composition but before final alpha-channel cleanup.
- **Engine:** comfyui · **Applies to:** post-repaint pass — runs after the LoRA/IP-Adapter repaint to lock output to the approved house palette · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: jrosebr1/color_transfer: MIT. Algorithm: public-domain academic (Reinhard et al., 2001, IEEE CG&A).) — MIT library, public-domain algorithm. No license constraints on the color transfer tool itself. Applied as post-processing to a generated image does not alter the generated image's license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| clip: True (default) — prevents out-of-range values from clipping to neutral grey |  | ○ |  |
| source: house-palette reference sprite (pre-approved ship-quality frame) |  | ○ |  |
| target: repainted frame |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Reinhard is a statistical/global transfer — it can shift all colors but cannot enforce a hard discrete palette (use Indexed Mode for hard quantization) |  |  |  |
| Transfer from a dark reference to a light frame (or vice versa) can produce visible hue contamination — choose a reference with similar luminance range |  |  |  |
| Does not handle transparency (alpha) channel — must strip/restore alpha around the transfer |  |  |  |

- **Best for:** palette-consistency (-, fit -) ; color-grade (-, fit -) ; post-repaint-qa (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Color Transfer between Images](https://pyimagesearch.com/2014/06/30/super-fast-color-transfer-images/) (Erik Reinhard, Michael Ashikhmin, Bruce Gooch, Peter Shirley, 2001) — L*a*b* channel mean/std matching for perceptually uniform color transfer; fast, parameter-free, no per-pixel lookup required. ; [jrosebr1/color_transfer — Python OpenCV color transfer library](https://github.com/jrosebr1/color_transfer) (Adrian Rosebrock, 2014) — MIT-licensed Python/OpenCV implementation of Reinhard et al. 2001; pip-installable; confirmed for commercial use.

### IP-Adapter Plus — style-transfer mode from a reference sprite · `recommended` · ▸ reproduced
**IP-Adapter Plus (SDXL variant, weight_type='style transfer') can extract and transfer the painterly texture and color feel from an approved reference sprite without the reference's content bleeding into the repainted character.**
Load ip-adapter-plus_sdxl_vit-h into ComfyUI via cubiq/ComfyUI_IPAdapter_plus (GPL-3.0 node, Apache-2.0 model weights). Use the IPAdapterPreciseStyleTransfer node added in June 2024, which applies decoupled style and composition layers — set weight_type to 'style transfer (SDXL)' and start with style_boost=2.0, weight~0.7–0.85. Feed an approved reference sprite as the image prompt. The ViT-H patch-level embeddings pull fine-grained texture/brushwork from the reference rather than a blunt global embedding. Pair with a ControlNet depth/structure node to hold the repainted character's pose and silhouette. The IP-Adapter provides style guidance; ControlNet holds structure.
- **For the pipeline:** Useful when the studio reference sprite is more trustworthy than the house LoRA for a particular character variant — the reference image is the style oracle instead of a trained adapter. Combine with denoise 0.6–0.75; lower denoise prevents style overpowering the mesh layout.
- **Engine:** comfyui · **Applies to:** repaint — inject painterly style from an approved reference sprite; complements ControlNet structure · **Base:** SDXL · **Kind:** technique
- **VRAM:** 10-20
- **Output license:** commercial **conditional** (license: Model weights (h94/IP-Adapter): Apache-2.0. ComfyUI node (cubiq/ComfyUI_IPAdapter_plus): GPL-3.0. Outputs inherit the BASE SDXL checkpoint license — use only on a verified-commercial base.) — IP-Adapter model weights on HuggingFace (h94/IP-Adapter) are Apache-2.0 — confirmed on HuggingFace model card. The ComfyUI node code is GPL-3.0 (cubiq/ComfyUI_IPAdapter_plus); this governs the tool code, NOT the generated image outputs. Output images inherit the BASE SDXL checkpoint license — the studio must use a verified-commercial SDXL base (not SD-XL models with restricted LoRAs). FaceID variants require insightface which has a non-commercial restriction: DO NOT use FaceID node for commercial work — use plain Plus node only.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| node: IPAdapterPreciseStyleTransfer (added 2024-06-28) |  | ○ |  |
| weight_type: 'style transfer (SDXL)' |  | ○ |  |
| style_boost: 2.0 (start); raise to reduce composition bleed |  | ○ |  |
| weight: 0.75–0.85 |  | ○ |  |
| steps: 30–40 |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| FaceID variant is non-commercial (insightface dependency) — never use for commercial work |  |  |  |
| Global embedding variant (ip-adapter_sdxl.bin) bleeds reference composition into output — always use Plus variant for style-only mode |  |  |  |
| Weight >0.9 over-stylizes: character identity lost, mesh layout abandoned |  |  |  |
| Without ControlNet structure node, composition control is weak — always pair |  |  |  |

- **Best for:** style-transfer (-, fit -) ; reference-driven-repaint (-, fit -) ; painterly-injection (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models](https://arxiv.org/abs/2308.06721) (Hu Ye, Jun Zhang, Sibo Liu, Xiao Han, Wei Yang, 2023) — Decoupled cross-attention mechanism separates image features from text features, enabling style-only reference guidance; 22M parameters, compatible with any fine-tune of the same base. ; [h94/IP-Adapter model card](https://huggingface.co/h94/IP-Adapter) (Hu Ye et al., 2023) — Apache-2.0 license confirmed on HuggingFace; ip-adapter-plus_sdxl_vit-h.bin uses ViT-H patch-level embeddings for closer reference-image adherence; 'Precise Style Transfer' node added June 2024. ; [cubiq/ComfyUI_IPAdapter_plus — IPAdapterPreciseStyleTransfer node](https://github.com/cubiq/ComfyUI_IPAdapter_plus) (cubiq, 2024) — GPL-3.0 node code; IPAdapterPreciseStyleTransfer added 2024-06-28; 'less bleeding of embeds between style and composition layers'; SDXL start: style_boost=2, weight~0.8.

### Studio house-style LoRA injected during the repaint pass · `recommended` · ▸ reproduced
**Applying the studio's sfhd_style house LoRA during the ControlNet repaint (not as a separate generation) is what converts the mesh render's 3D-game-render look into the painterly house style while structure is held by depth ControlNet.**
Load the house LoRA on the editor model at a tuned weight (the existing pipeline uses ~1.75 on its SDXL base; validate the equivalent scale on Qwen-Image-Edit's architecture). Run img2img over the mesh render with ControlNet-depth holding silhouette and volume. The LoRA supplies the brushwork, warm-light shading, and house palette; ControlNet supplies the pose/silhouette. Tune denoise in the 0.55–0.75 range to let the style land without erasing the approved character design. Face region is preserved by the face-preserve pass described in the pipeline (do not apply LoRA at full weight over face crops).
- **For the pipeline:** This is the style half of the §D repaint decomposition (structure=ControlNet, style=LoRA); it reuses the already-trained studio house LoRA so the output matches shipped sprites. The LoRA inherits the Qwen-Image-Edit Apache-2.0 base license — output is the studio's.
- **Engine:** comfyui · **Applies to:** repaint — any frame: idle, walk, attack, death; works alongside ControlNet-depth · **Base:** Qwen-Image · **Kind:** technique
- **VRAM:** 16-28
- **Base model (model-knowledge):** `Qwen/Qwen-Image-Edit`
- **Output license:** commercial **yes** (license: LoRA studio-owned; base Qwen/Qwen-Image-Edit Apache-2.0) — Studio-owned LoRA on an Apache-2.0 base → output is the studio's. The established principle (confirmed by community practice and multiple HF model cards): a LoRA is a delta over the base; output inherits the BASE model license. The base here is Qwen/Qwen-Image-Edit (Apache-2.0), making output commercially clean. No anime models or NC base models touch this path.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| lora_weight: start 1.75, tune down to ~1.3 if design erases |  | ○ |  |
| denoise: 0.55–0.75 (lower preserves approved design, higher injects more style) |  | ○ |  |
| cfg: 6–8 |  | ○ |  |
| steps: 28–40 |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| LoRA weight >2.0 causes over-stylization: brushwork artifacts, loss of readable character silhouette |  |  |  |
| Applying to face crop at full weight blurs eye detail — face-preserve pass must run after |  |  |  |
| Style-bleed to weapon area if weapon is in main canvas; mask weapon region or run as separate layer |  |  |  |

- **Best for:** painterly-style-injection (-, fit -) ; house-style-consistency (-, fit -) ; repaint (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=unverified minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 2 of 3 juror(s) [confirmed, confirmed-with-fixes, unverified]]
- **Sources:** [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685) (Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, 2021) — Low-rank adapters inject a learned style/concept into a frozen base model at inference; output inherits the base model's license and generative distribution. ; [Qwen/Qwen-Image-Edit model card](https://huggingface.co/Qwen/Qwen-Image-Edit) (Qwen Team, Alibaba, 2025) — Apache-2.0 licensed image-editing model built on 20B Qwen-Image; supports semantic editing (style transfer, texture) and appearance editing; released December 2025.

### img2img denoise strength — style/fidelity tradeoff window · `recommended` · ▸ reproduced
**img2img denoise strength directly controls the style-vs-fidelity tradeoff in the repaint pass: ~0.4–0.55 preserves approved design with light style injection; ~0.6–0.75 is the main style-injection window; >0.8 discards the mesh structure and risks design drift.**
In Stable Diffusion img2img, denoise strength sets how much noise is added to the input latent before denoising — 0.0 = copy input unchanged, 1.0 = full noise (text-to-image). For the repaint pass over a mesh render, the practical style-injection window is 0.55–0.75: enough noise to let the house LoRA and/or IP-Adapter reshape the appearance toward the painterly style, while retaining the mesh's pose, volume, and silhouette. Iterative low-strength passes (e.g., 0.35 × 3 passes) can accumulate style while better preserving identity than a single 0.75 pass. For face+weapon regions run a separate lower-denoise pass (0.25–0.4) to preserve fine detail.
- **For the pipeline:** The denoise knob is the primary dial for the §D gap: too low = 3D-render look survives; too high = approved design lost. The recommended operating window for the main body canvas is 0.60–0.72 with the house LoRA active. Face/weapon crop passes run at 0.25–0.45.
- **Engine:** comfyui · **Applies to:** any img2img repaint pass; tuning the balance between injected style and preserved mesh layout · **Kind:** technique
- **VRAM:** 8-28
- **Output license:** commercial **yes** (license: Technique is intrinsic to Stable Diffusion DDIM/DPM samplers — no external license) — This is a sampler parameter, not a model. No license constraint. Output license is governed entirely by the base model.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| denoise 0.4–0.55: design-preserve mode (use for face/weapon crops) |  | ○ |  |
| denoise 0.6–0.75: main style-injection window (use for body canvas with house LoRA) |  | ○ |  |
| denoise 0.75–0.85: high-style mode; monitor for design drift |  | ○ |  |
| denoise >0.85: avoid for repaint — treats mesh as mere hint, structural loss likely |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Single high-denoise pass over the full canvas loses fine face detail — always mask or re-composite face separately |  |  |  |
| Low denoise on the body canvas leaves the 3D-render surface texture visible — underfills the §D gap |  |  |  |
| Iterative multi-pass with accumulating style is slower (3–4× compute) but higher fidelity than single pass |  |  |  |

- **Best for:** style-fidelity-balance (-, fit -) ; repaint-tuning (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Hugging Face Diffusers — Image-to-Image Pipeline documentation](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/img2img) (Hugging Face, 2023) — strength parameter in img2img sets the proportion of the input image to transform (0=no change, 1=complete redraw); documented as the primary fidelity/variation dial. ; [What is denoising strength? — Stable Diffusion Art](https://stable-diffusion-art.com/denoising-strength/) (Andrew (stable-diffusion-art.com), 2023) — Explains noise-level-to-strength mapping with practical examples; notes that iterative low-strength passes (e.g., 0.25×4) can accumulate style change with better identity retention than a single high-strength pass.

### Avoiding style-bleed and over-stylization — selective block targeting for LoRAs · `recommended` · · community
**Selectively enabling the house LoRA only on style-relevant SDXL transformer blocks (OUT1 and IN08, equivalent to the style block region) and disabling it on content/identity blocks reduces style-bleed to face and weapon regions while preserving the approved character design.**
Style LoRAs applied at full weight across all UNet/transformer blocks cause over-stylization: brushwork artifacts appear on faces, rigid weapon edges soften unacceptably, and character identity drifts toward the LoRA's training domain. The solution documented in the community (Civitai, 2024) is to target the LoRA only to the blocks proven to encode style (OUT1, IN08 in SDXL block notation — consistent with B-LoRA's block-5 finding). In ComfyUI, this is implemented via block-weight LoRA loaders (e.g., via the Advanced LoRA Loader in WAS Node Suite or similar). The face region additionally benefits from a separate lower-denoise inpaint pass (face-preserve, already part of the studio pipeline). The weapon region should be composited from the mesh render at full opacity rather than repainted — the LoRA should be masked off the weapon canvas entirely.
- **For the pipeline:** Maps directly to the studio's de-lit face-preserve pipeline. Style injection should be maximally active on the body/clothing canvas, minimally active on face (handled by face-preserve pass), and zero on the weapon (composited from mesh). The block-selective approach is the mechanism — not just weight reduction.
- **Engine:** comfyui · **Applies to:** LoRA inference — prevent house LoRA from over-stylizing face or weapon regions · **Kind:** technique
- **VRAM:** 12-24
- **Output license:** commercial **yes** (license: Technique — no license. Block-selective LoRA loaders in ComfyUI vary by node implementation.) — Pure inference technique. No license constraints. Block-selective loading is a parameter choice, not a model.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| style_lora_active_blocks: [OUT1, IN08] (style region of SDXL UNet) |  | ○ |  |
| style_lora_weight_on_face_region: 0.0 (rely on face-preserve pass) |  | ○ |  |
| style_lora_weight_on_weapon_region: 0.0 (composite from mesh instead) |  | ○ |  |
| style_lora_weight_on_body_clothing: 1.3–1.75 |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Block notation varies by LoRA loader implementation — verify block names match your ComfyUI node |  |  |  |
| Masked LoRA loading is not natively supported in all ComfyUI nodes — may require WAS Node Suite or custom implementation |  |  |  |
| Community evidence only — no peer-reviewed study quantifies the exact block impact for all SDXL fine-tunes |  |  |  |

- **Best for:** style-bleed-prevention (-, fit -) ; over-stylization-mitigation (-, fit -) ; face-weapon-preservation (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Preventing style bleeding from character LoRAs by selectively enabling blocks (SDXL)](https://civitai.com/articles/5301/preventing-style-bleeding-from-character-loras-by-selectively-enabling-blocks-sdxl) (Civitai community (unnamed author), 2024) — Enabling LoRA only on OUT1 and IN08 blocks (SDXL) stylizes images while preserving base model identity; full-weight application across all blocks degrades quality and variability. ; [Implicit Style-Content Separation using B-LoRA](https://arxiv.org/abs/2403.14572) (Yarden Frenkel, Yael Vinker, Ariel Shamir, Daniel Cohen-Or, 2024) — Formally establishes that SDXL block 5 encodes style and block 4 encodes content — provides theoretical grounding for block-selective style injection.

### IP-Adapter Style & Composition SDXL — combined style + layout control · `situational` · · single-run
**The IPAdapterStyleComposition node for SDXL separates style weight from composition weight on a single reference image, enabling the studio to blend how much layout vs. brushwork/color is pulled from a reference sprite — useful for maintaining pose family consistency across attack frames.**
The IPAdapterStyleComposition node (comfyui-ipadapter, added 2024) exposes separate style_weight and composition_weight parameters for SDXL. Style weight controls texture/palette/brushwork contribution; composition weight controls the loose spatial layout contribution. For the repaint pipeline: set composition_weight to 0.0 (structure comes from depth ControlNet, not the reference) and style_weight to 0.7–0.9 to get clean style injection. Alternatively, set composition_weight to 0.2–0.3 for a mild layout nudge toward the reference sprite's framing (e.g., ensuring attack-frame head position is consistent with the reference without fully copying it). This is distinct from the PreciseStyleTransfer node — this node is for simultaneous style+layout tasks.
- **For the pipeline:** Use IPAdapterStyleComposition when the approved reference sprite's composition (not just brushwork) should inform the repaint — for example, ensuring a pack's attack frames share the same diagonal lean as the reference even if the depth ControlNet is only providing rough depth. Set composition_weight low; let depth ControlNet dominate structure.
- **Engine:** comfyui · **Applies to:** repaint — when both style AND loose layout need to be taken from the reference, not just style · **Base:** SDXL · **Kind:** workflow
- **VRAM:** 10-20
- **Output license:** commercial **conditional** (license: Model weights (h94/IP-Adapter): Apache-2.0. ComfyUI node (cubiq/ComfyUI_IPAdapter_plus): GPL-3.0. Outputs inherit base SDXL checkpoint license.) — Same as ip-adapter-plus-style-transfer: Apache-2.0 model weights, GPL-3.0 node code (governs tool, not outputs), output inherits base SDXL license. Do not use FaceID variant — non-commercial (insightface dependency).
- **Fit:** rig 5/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| style_weight: 0.7–0.9 |  | ○ |  |
| composition_weight: 0.0 (style-only repaint) or 0.2–0.3 (mild layout nudge) |  | ○ |  |
| pair with depth ControlNet at 0.8–1.0 |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| composition_weight >0.4 competes with depth ControlNet and causes pose ambiguity |  |  |  |
| Evidence is single-reported-run — community reports; not formally benchmarked for sprite repaint specifically |  |  |  |
| Same FaceID/insightface commercial restriction as other IP-Adapter nodes |  |  |  |

- **Best for:** style-and-layout-reference (-, fit -) ; attack-frame-consistency (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [IPAdapter Style & Composition SDXL Node Documentation](https://comfyai.run/documentation/IPAdapterStyleComposition) (ComfyAI (node documentation), 2024) — Separate style_weight and composition_weight parameters on SDXL; style controls texture/brushwork, composition controls spatial layout transfer from reference. ; [IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models](https://arxiv.org/abs/2308.06721) (Hu Ye, Jun Zhang, Sibo Liu, Xiao Han, Wei Yang, 2023) — Decoupled cross-attention architecture enabling separate handling of style and composition image guidance.

### Reference-only ControlNet — self-attention style injection without a structural map · `situational` · · community
**The ControlNet 'reference_only' preprocessor injects the self-attention features of a reference image directly into the denoising process, producing style coherence with the reference without requiring an edge/depth/pose map as conditioning signal.**
Reference-only ControlNet (available via ComfyUI-Advanced-ControlNet and the ACN_ReferenceControlNet node) shares the reference image's self-attention features with the UNet denoising layers. This means the generated image adopts the texture, color arrangement, and compositional feel of the reference without the reference's content being composited in. Two sub-modes exist: 'reference_only' (attention injection) and 'reference_adain' (adaptive instance normalization for statistics-level style). In the repaint pipeline, this can pair with a depth ControlNet: depth controls pose/silhouette at full weight; reference-only runs at 0.4–0.7 to nudge style toward a target sprite. Simpler to set up than IP-Adapter when only a rough style hint is needed.
- **For the pipeline:** Lower-overhead style hint than IP-Adapter — no additional model weights to load. Use when a reference sprite is available and the style target is compositionally similar to the mesh render. Set strength 0.4–0.6 to avoid over-constraining the repaint toward the reference's content.
- **Engine:** comfyui · **Applies to:** repaint — inject style feel from a reference sprite when no structural map is desired or when pairing with depth ControlNet at low weight · **Kind:** technique
- **VRAM:** 8-16
- **Output license:** commercial **conditional** (license: ComfyUI-Advanced-ControlNet node: MIT. Reference-only is a ControlNet preprocessor mode — no separate weights. Outputs inherit base checkpoint license.) — The reference-only mode is a feature of the ControlNet architecture code (lllyasviel/ControlNet codebase); no additional model license applies. Output inherits the BASE SDXL or SD1.5 checkpoint license — use only on a verified-commercial base. ControlNet architecture paper (Zhang et al., Apache-2.0 code) does not restrict commercial outputs.
- **Fit:** rig 5/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| mode: 'reference_only' (attention injection) or 'reference_adain' (statistics matching) |  | ○ |  |
| strength: 0.4–0.7 (higher = closer to reference, risks content bleed) |  | ○ |  |
| pair with depth ControlNet at 0.8–1.0 for structure |  | ○ |  |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Strength >0.75 causes content bleed — reference character's face/clothing appears in output |  |  |  |
| Without a structure ControlNet, pose and silhouette are uncontrolled |  |  |  |
| Evidence_strength is community-claim — the reference-only mode is a community-documented feature, not formally described in the ControlNet paper itself |  |  |  |

- **Best for:** style-hint (-, fit -) ; reference-style-transfer (-, fit -)
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Adding Conditional Control to Text-to-Image Diffusion Models](https://arxiv.org/abs/2302.05543) (Lvmin Zhang, Anyi Rao, Maneesh Agrawala, 2023) — ControlNet architecture enabling conditional control of frozen T2I models; reference-only mode extends this by injecting reference self-attention directly into UNet layers. ; [ComfyUI Node: ACN_ReferenceControlNet (ComfyUI-Advanced-ControlNet)](https://www.runcomfy.com/comfyui-nodes/ComfyUI-Advanced-ControlNet/ACN_ReferenceControlNet) (Kosinkadink, 2024) — ComfyUI-Advanced-ControlNet node documentation for ReferenceControlNet — incorporates reference image or styles into the control network via self-attention injection.

