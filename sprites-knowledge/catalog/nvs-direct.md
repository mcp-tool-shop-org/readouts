# NVS-direct turnaround (no mesh)
_Image -> multiple consistent 2D views via multi-view diffusion / novel-view synthesis. License-decisive (Zero123 lineage is NC)._ · wave 5 · 2026-09-07 · [‹ catalog index](README.md)

8 recipes · 1 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | MV-Adapter | comfyui | turnaround | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 6 | CharacterGen | python | turnaround | ▸ reproduced | ✅ yes | 4 | 4 | ✓ |
| 6 | Hunyuan3D-2mv | comfyui | turnaround | ▸ reproduced | ⚠ cond | 4 | 2 | ✓ |
| 6 | Stable Zero123 (and Zero123C variant) | comfyui | turnaround | ▸ reproduced | ⚠ cond | 4 | 2 | ✓ |
| 6 | Wonder3D | python | turnaround | ▸ reproduced | ✅ yes | 4 | 2 | ✓ |
| 8 | SV3D (Stable Video 3D) | comfyui | turnaround | · single-run | ⚠ cond | 4 | 2 | ✓ |
| 11 | Era3D | python | turnaround | ▸ reproduced | ⛔ no | 4 | 1 | ✓ |
| 11 | Zero123++ | comfyui | turnaround | ▸ reproduced | ⛔ no | 5 | 1 | ✓ |

## Detail

### MV-Adapter · `recommended` · ▸ reproduced
**Apache-2.0 adapter that turns ANY anime/community SDXL checkpoint (Animagine XL 3.1 shown) plus LoRAs into a multi-view generator, so the base license you already cleared is the license you keep.**
A plug-in attention adapter (not a finetuned base model) that converts a frozen text-to-image SDXL/SD2.1 model into a 6- or 10-view consistent generator at 768px, including image-to-arbitrary-views and ControlNet/LoRA stacking. Because it is an adapter, the commercial-use license is inherited from your chosen base checkpoint rather than imposed by MV-Adapter (which is Apache-2.0). The README explicitly demonstrates anime SDXL (Animagine XL 3.1) and multi-LoRA personalization, which is exactly the JRPG-sprite style path. ICCV 2025.
- **For the pipeline:** This is the one entry on the list that is purely 2D-direct AND commercial-clean AND anime/SDXL-native. For a 2.5D JRPG turnaround pipeline, train/curate your style LoRA on a permissive anime SDXL base, then drive MV-Adapter for front/3-4/side/back plates. The 5090's 32GB runs SDXL+adapter with headroom for higher view counts and batch. Consistency is real but not perfect at >6 views, so treat it as a draft-then-clean-up step, not final pixels.
- **Engine:** comfyui · **Applies to:** turnaround · **Base:** SDXL · **Kind:** model
- **VRAM:** 10-16
- **Output license:** commercial **yes** (license: Apache-2.0 (adapter); effective license = base checkpoint license) — MV-Adapter code is Apache-2.0; it imposes no usage restriction. Commercial-use status is inherited from the base SDXL checkpoint + any LoRAs you load (a LoRA inherits its base model license). Pair with a permissively-licensed anime SDXL base and the whole stack is commercial-clear. This decoupling is the single biggest reason it beats the Zero123 lineage for a commercial studio.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| views | 6 or 10 | ○ | 6 is the consistency sweet spot; 10 strains back/3-4 coherence |
| resolution | 768px | ○ | SDXL path; upscale after |
| base_model | any diffusers SDXL | ○ | Animagine XL 3.1, Dreamshaper, real-dream-sdxl all demonstrated |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| back-of-head / occluded-side detail drifts from front | single front-image conditioning under-constrains unseen geometry (Janus-family weakness shared by all 2D-direct methods) | use a reference image + ControlNet pose/scribble for the back; or condition on 2 input views; clean up in post |  |
| style LoRA identity weakens at extreme azimuths | adapter attention dilutes per-view conditioning | lower view count to 6, raise LoRA weight, or run per-view img2img refinement at low denoise |  |

- **Verify:** Both sources resolve. GitHub repo huanngzh/MV-Adapter confirmed Apache-2.0, official ICCV 2025 impl by Zehuan Huang, supports SDXL/Animagine XL 3.1, image-to-arbitrary-views, ControlNet, multi-LoRA at 768px. arXiv:2412.03632 title/authors/parallel-attention-adapter/frozen-base/768px all confirmed. License Apache-2.0 (adapter) with effective license = base checkpoint is accurate; commercial_use=yes correct for a permissively-licensed base. [LICENSE is plain Apache-2.0, no added clauses. Abstract: 'multi-view generation at 768 resolution on SDXL', base kept frozen ('without altering the original network structure or feature space'). Animagine XL 3.1, multi-LoRA and ControlNet a]
- **Sources:** [huanngzh/MV-Adapter (official impl, ICCV 2025)](https://github.com/huanngzh/MV-Adapter) (Zehuan Huang et al., 2025) — Repository is Apache-2.0 and supports SDXL/SD2.1/community models including anime SDXL (Animagine XL 3.1), arbitrary-view image-to-multiview, ControlNet, and multiple LoRAs. ; [MV-Adapter: Multi-view Consistent Image Generation Made Easy (arXiv:2412.03632)](https://arxiv.org/abs/2412.03632) (Zehuan Huang, Yuan-Chen Guo, Haoran Wang, Ran Yi, Lizhuang Ma, Yan-Pei Cao, Lu Sheng, 2024) — Introduces a parallel attention adapter that adapts a frozen T2I model to 768px multi-view generation without retraining the base, preserving the base model's quality and personalization.

### CharacterGen · `situational` · ▸ reproduced
**Apache-2.0, explicitly anime-character-trained (Anime3D/VRM dataset), and uses multi-view pose canonicalization to force a clean A-pose front/side/back — the one purpose-built character-turnaround model that is commercially licensed.**
SIGGRAPH 2024 pipeline (Apache-2.0) that takes a single anime character image and produces canonicalized multi-view images (front/side/back in a normalized A-pose) before lifting to 3D via TripoSR. The pose-canonicalization stage is specifically designed to suppress the Janus/inconsistent-view failure by re-posing the subject into a known canonical layout. Trained on an Anime3D / VRM character dataset, so it is anime-native rather than Objaverse-object-native.
- **For the pipeline:** The only model here engineered FOR character turnarounds with anime priors AND a commercial license. Its 2D multi-view stage (before the 3D lift) is directly usable as a turnaround generator; you do not need the mesh. The canonical A-pose output is a double-edged sword for a JRPG: great for a neutral reference sheet, but it normalizes away authored poses, so it is a reference-generation tool, not a final-sprite tool. Base SD backbone is older/lower-fidelity than SDXL, so MV-Adapter on a modern anime SDXL will usually look better; keep CharacterGen for its canonicalization trick.
- **Engine:** python · **Applies to:** turnaround · **Base:** SD (Tune-A-Video) + TripoSR · **Kind:** model
- **VRAM:** 12-16 (unstated; estimate)
- **Output license:** commercial **yes** (license: Apache-2.0 (verify dataset terms for weight redistribution)) — Code is Apache-2.0. Caveat: verify the training-data (Anime3D / VRM characters) terms separately if you redistribute weights; the code license is clean for commercial use of outputs. Distinct from the unrelated consumer SaaS 'CharacterGen.app' — that is a different product with its own paid commercial plan.
- **Fit:** rig 4/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| views | 4 (canonical front/side/back/3-4) | ○ | fixed canonical layout |
| pose | canonicalized A-pose | ○ | Janus mitigation by construction |
| domain | anime characters | ○ | Anime3D / VRM training data |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| authored/dynamic input pose is flattened to A-pose | pose canonicalization is intentional | accept for reference sheets; do action poses elsewhere |  |
| lower texture fidelity than SDXL pipelines | SD-era Tune-A-Video backbone | upscale / img2img refine on an SDXL anime model after |  |

- **Verify:** Both sources resolve. arXiv:2402.17214 title/authors/multi-view pose canonicalization for anime characters confirmed. GitHub zjp-shadow/CharacterGen confirmed Apache-2.0, official SIGGRAPH'24 (TOG), built on Tune-A-Video + TripoSR, anime VRM dataset. Note: VRM raw data cannot be redistributed per policy (repo flags this) and weights are trained on it — the entry's 'verify dataset terms for weight redistribution' caveat is well-founded. Code/commercial_use=yes is accurate for the Apache-2.0 code/weights. [Apache-2.0 confirmed twice: repo LICENSE and HF zjpshadow/CharacterGen licence field. SIGGRAPH(TOG) 2024; canonicalization and TripoSR real. But the 2D stage emits FOUR views, 'A-pose' is stated nowhere, and raw VRM data is non-redistributa]
- **Sources:** [CharacterGen: Efficient 3D Character Generation from Single Images with Multi-View Pose Canonicalization (arXiv:2402.17214)](https://arxiv.org/abs/2402.17214) (Hao-Yang Peng, Jia-Peng Zhang, Meng-Hao Guo, Yan-Pei Cao, Shi-Min Hu, 2024) — Uses multi-view pose canonicalization to generate consistent canonical-pose multi-view images of anime characters from a single input, explicitly mitigating multi-view inconsistency. ; [zjp-shadow/CharacterGen (SIGGRAPH'24 official)](https://github.com/zjp-shadow/CharacterGen) (Jia-Peng Zhang et al., 2024) — Repository is Apache-2.0, builds on Tune-A-Video and TripoSR, and is trained on an Anime3D/VRM character dataset for anime-style multi-view character generation.

### Hunyuan3D-2mv · `situational` · ▸ reproduced
**Multi-view-CONTROLLED shape model: you FEED it your own front/side/back views (so you control consistency upstream) — commercial allowed under 1M MAU, but the license excludes the EU, UK, and South Korea, a hard distribution constraint for a game.**
A finetune of Hunyuan3D-2 (Mar 2025) that takes multiple input views (front/back/etc.) to condition shape generation — the inverse direction from the other entries: it consumes a turnaround rather than inventing one. For a studio that already produces consistent 2D turnarounds (via MV-Adapter), this is the model that turns them into geometry while preserving your authored views, sidestepping the Janus problem because YOU supply the back view.
- **For the pipeline:** Conceptually the right consumer of a 2D turnaround: instead of one image guessing the back, you author all views in MV-Adapter then condition Hunyuan3D-2mv on them, which is the cleanest Janus mitigation available (control the inputs). But it is a 3D-shape model, so it belongs in the 3D-mesh lane, not the pure 2D-direct lane; and the EU/UK/Korea geo-carveout undermines its value for a globally-shipped JRPG. Use only if you (a) need geometry and (b) can satisfy the territory and MAU terms.
- **Engine:** comfyui · **Applies to:** turnaround · **Base:** Hunyuan3D-2 DiT (flow-matching) · **Kind:** model
- **VRAM:** ~10-16 (estimate)
- **Output license:** commercial **conditional** (license: Tencent Hunyuan Community (commercial <1M MAU; EXCLUDES EU/UK/South Korea)) — Tencent Hunyuan Community License: commercial use permitted below 1 million monthly active users (above that requires a license from Tencent). Critically, the license states it DOES NOT APPLY in the European Union, United Kingdom, and South Korea — meaning you cannot rely on it to ship in those markets. For a commercial game with global distribution (incl. EU storefronts), this geo-exclusion is a serious blocker; treat as conditional and confirm with legal.
- **Fit:** rig 4/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| conditioning | multiple input views | ○ | you supply front/back -> controls consistency |
| arch | DiT + flow matching | ○ | finetune of Hunyuan3D-2 |
| mau_cap | 1,000,000 MAU | ○ | above = request Tencent license |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| cannot legally ship in EU/UK/South Korea | license territory exclusion | confirm with legal; geofence or choose another model for those markets |  |
| output is a mesh, not 2D views | it is a 3D shape model (mesh lane, not 2D-direct) | use upstream MV-Adapter for the 2D turnaround itself |  |

- **Verify:** Both sources resolve. HF tencent/Hunyuan3D-2mv confirmed finetuned from Hunyuan3D-2 for multiview-controlled shape generation (front/left/back inputs), tencent-hunyuan-community license, active (~3.1k downloads/mo). LICENSE confirms royalty-free commercial use below 1M MAU AND explicit exclusion of EU/UK/South Korea ('THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA'). commercial_use=conditional with the MAU + territory caveats is fully accurate. [LICENSE file is 'TENCENT HUNYUAN 3D 2.0 COMMUNITY LICENSE AGREEMENT' (HF field: tencent-hunyuan-community). Verbatim: 'DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA', plus the 1 million monthly-active-user cap. Multi-]
- **Sources:** [tencent/Hunyuan3D-2mv (Hugging Face)](https://huggingface.co/tencent/Hunyuan3D-2mv) (Tencent Hunyuan, 2025) — Finetuned from Hunyuan3D-2 to support multiview-controlled shape generation, consuming several input views to produce detailed geometry. ; [Tencent Hunyuan3D 2.0 Community License](https://huggingface.co/tencent/Hunyuan3D-2mv/blob/main/LICENSE) (Tencent, 2025) — Grants royalty-free commercial use below 1,000,000 MAU but explicitly does not apply in the European Union, United Kingdom, and South Korea.

### Stable Zero123 (and Zero123C variant) · `situational` · ▸ reproduced
**Default Stable Zero123 is Non-Commercial Research only; the separate Zero123C ('Commercially-available') variant is conditional commercial under a Stability membership — so 'Zero123' commercial status depends entirely on WHICH checkpoint.**
Stability's improved single-image novel-view model, finetuned from an SD image-variations backbone. Two checkpoints with different licenses: the standard one trained partly on CC-BY-NC objects (Non-Commercial Research License) and Zero123C trained only on CC-BY/CC0 objects (Stability Community License, commercial-OK with membership). It is object/orbit oriented rather than anime-character oriented.
- **For the pipeline:** Even the commercial Zero123C is trained on 3D objects, so it produces orbit-style novel views of objects/props well but is weak on stylized anime characters and prone to the back-of-head Janus failure. For a JRPG, it is more useful for prop/item turnarounds than for hero-character sprite sheets. If you go this route, use Zero123C only, never the NC default, and verify your revenue tier against the Stability Community License.
- **Engine:** comfyui · **Applies to:** turnaround · **Base:** SD image-variations · **Kind:** model
- **VRAM:** ~8-12 (unstated; estimate)
- **Output license:** commercial **conditional** (license: Non-Commercial Research (standard); Stability Community License (Zero123C)) — Standard Stable Zero123 = NON-COMMERCIAL (Stability AI Non-Commercial Research Community License). Zero123C = commercial allowed under the Stability AI Community License, which is free for orgs under $1M annual revenue and requires a paid Enterprise license above that. You MUST pick the C checkpoint and accept the membership/revenue terms to be commercial-clean.
- **Fit:** rig 4/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| checkpoint | stable-zero123 vs zero123c | ○ | only zero123c is commercial |
| task | single-image orbit novel view | ○ | object-centric |
| backbone | sd-image-variations | ○ | finetuned |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| wrong checkpoint = license violation | two near-identically-named models with opposite licenses | use ONLY Zero123C for commercial |  |
| anime character identity / back view degrades | object-centric training, Janus | prefer for props; use MV-Adapter/CharacterGen for characters |  |

- **Verify:** Both sources resolve. HF stabilityai/stable-zero123 confirms standard Stable Zero123 uses CC-BY-NC objects under Stability AI Non-Commercial Research Community License (strictly non-commercial), finetuned from lambdalabs/sd-image-variations-diffusers. Blog confirms Zero123C trained only on CC-BY/CC0 for commercial use. The bundled 'conditional' label is fair: standard variant is non-commercial, Zero123C is commercial under the Community License (blog notes commercial use tied to active Stability membership). Accurate. [Both checkpoints confirmed inside ONE repo: stable_zero123.ckpt (sai-nc-community, NC research) and stable_zero123_c.ckpt. But LICENSE_stable_zero123_c.md is the STABILITY AI COMMUNITY LICENSE — free commercial below USD $1,000,000 annual r]
- **Sources:** [stabilityai/stable-zero123 (Hugging Face)](https://huggingface.co/stabilityai/stable-zero123) (Stability AI, 2023) — Standard Stable Zero123 includes CC-BY-NC objects and is released under the Stability AI Non-Commercial Research Community License (not for commercial use); finetuned from lambdalabs/sd-image-variations-diffusers. ; [Introducing Stable Zero123: Quality 3D Object Generation from Single Images](https://stability.ai/news-updates/stable-zero123-3d-generation) (Stability AI, 2023) — Announces Stable Zero123C trained only on CC-BY and CC0 objects so it can be used commercially under the Stability AI Community License.

### Wonder3D · `situational` · ▸ reproduced
**MIT-licensed cross-domain diffusion that emits 6 consistent color + normal views from one image — the most permissive license in the set — but it is object-reconstruction native and weak on stylized anime characters.**
Cross-domain diffusion model (MIT license) that generates 6 consistent multi-view color images AND matching normal maps from a single image, then fuses them to a mesh in 2-3 minutes. The simultaneous normal-map output is useful if you later want lighting/relighting on 2.5D sprites. Object/photogrammetry oriented; Wonder3D++ extends fidelity (2024-2025).
- **For the pipeline:** License is ideal, and the bonus normal maps are genuinely useful for 2.5D lighting — but Wonder3D is trained for object reconstruction and tends to flatten anime style and hallucinate the back. For a JRPG studio it is a solid prop/environment-asset turnaround + normal-map source, not a hero-sprite generator. If you want normals on characters, generate the turnaround with MV-Adapter (anime SDXL) and derive normals separately rather than relying on Wonder3D's character fidelity.
- **Engine:** python · **Applies to:** turnaround · **Base:** SD 2.x cross-domain diffusion · **Kind:** model
- **VRAM:** ~10-16 (estimate)
- **Output license:** commercial **yes** (license: MIT) — MIT license = fully permissive, commercial use allowed with acknowledgement. Cleanest license of the lineage alongside MV-Adapter's Apache-2.0. Caveat: confirm the released weights are covered by the same MIT terms (some research repos MIT the code but leave weight terms to the training data); the repo states MIT for the project.
- **Fit:** rig 4/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| views | 6 color + 6 normal | ○ | cross-domain output |
| runtime | 2-3 min to mesh | ○ | fast |
| domain | objects | ○ | not anime-character tuned |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| anime style flattened / detail loss on characters | object-reconstruction training | use for props/environments; characters via MV-Adapter |  |
| back view inconsistent with front | single-view conditioning (Janus family) | supply back reference; post-clean |  |

- **Verify:** Both sources resolve. GitHub xxlong0/Wonder3D confirmed MIT ('free to use with acknowledgement'), official, 6-view normal+color cross-domain diffusion, textured mesh in 2-3 min. commercial_use=yes correct. Minor attribution note: arXiv:2511.01767 (Wonder3D++) lead author is Yuxiao Yang (Xiao-Xiao Long is co-author), so 'Xiaoxiao Long et al.' mislabels the lead; paper exists and content claim is accurate. License axis fully verified. [LICENSE is plain MIT with no added restrictions and no separate weights carve-out — the most permissive in this bucket, as claimed. 6 colour views plus matching normal maps confirmed. Wonder3D++ is real: arXiv 2511.01767 (Nov 2025, IEEE TPA]
- **Sources:** [xxlong0/Wonder3D (official)](https://github.com/xxlong0/Wonder3D) (Xiaoxiao Long et al., 2023) — Released under MIT license; generates 6 consistent multi-view normal maps and color images from a single image via cross-domain diffusion, reconstructing a textured mesh in 2-3 minutes. ; [Wonder3D++: Cross-domain Diffusion for High-fidelity 3D Generation from a Single Image (arXiv:2511.01767)](https://arxiv.org/abs/2511.01767) (Xiaoxiao Long et al., 2025) — Extends Wonder3D's cross-domain (color+normal) multi-view diffusion for higher-fidelity single-image 3D generation.

### SV3D (Stable Video 3D) · `situational` · · single-run
**Video-diffusion orbits give the smoothest, most temporally-consistent 360 views of the lineage, and the 2024 Stability Community License makes it commercial-OK free under $1M revenue — but it is object-orbit native, not anime-character native.**
Adapts Stable Video Diffusion to novel-view synthesis: SV3D_u generates an orbital video from a single image, SV3D_p follows a specified camera path. Because it is a video model, frame-to-frame (view-to-view) consistency around an orbit is notably smoother than tiled multi-view diffusers. Now under the Stability AI Community License (free commercial under $1M annual revenue; paid Enterprise above).
- **For the pipeline:** Its superpower is smooth orbital consistency, which for a sprite studio means you can sample a clean front/3-4/side/back from a continuous orbit rather than stitching independent views. But it is trained on objects, leans photoreal/3D, and does not respect 2D anime style; characters tend to get plasticized and the far side still guesses. Best used for rotating props, vehicles, and item icons where you want a turntable, not for stylized hero sprites. Heaviest VRAM here, but comfortable on the 5090's 32GB.
- **Engine:** comfyui · **Applies to:** turnaround · **Base:** Stable Video Diffusion · **Kind:** model
- **VRAM:** ~16-24 (estimate; video-diffusion)
- **Output license:** commercial **conditional** (license: Stability AI Community License (free commercial under $1M revenue)) — Stability AI Community License: free for research/non-commercial AND commercial use for individuals/orgs with annual revenue under $1,000,000; above $1M requires a paid Enterprise license. This is materially more permissive than the original 'membership-only' framing and clears most small studios. Verify the current LICENSE.md on the HF repo before shipping.
- **Fit:** rig 4/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| variant | SV3D_u / SV3D_p | ○ | u = auto orbit, p = path-conditioned |
| frames | 21-view orbit | ○ | video-style temporal consistency |
| domain | objects / orbit | ○ | not anime-character tuned |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| anime style turns photoreal/plastic | SVD object/photoreal prior | not suitable for stylized characters; use for props |  |
| occluded far side invented | single-view conditioning | use SV3D_p with a constrained path; post-clean |  |

- **Verify:** All sources resolve. sv3d.github.io confirms SV3D adapts Stable Video Diffusion for orbital novel-view synthesis (title/authors confirmed). HF LICENSE.md confirms the actual license is the Stability AI Community License Agreement granting royalty-free commercial use, terminating above USD $1M annual revenue. The HF 'sv3d-nc-community' tag is only a slug; license text permits tiered commercial use. commercial_use=conditional and 'free commercial under $1M revenue' are accurate. [LICENSE.md is the STABILITY AI COMMUNITY LICENSE AGREEMENT carrying the USD $1,000,000 annual-revenue termination clause verbatim. sv3d_u (orbital) and sv3d_p (camera path) both confirmed; 21 frames at 576x576. NOTE: the HF tag still reads ]
- **Sources:** [SV3D: Novel Multi-view Synthesis and 3D Generation from a Single Image using Latent Video Diffusion](https://sv3d.github.io/) (Vikram Voleti, Chun-Han Yao, Mark Boss, Adam Letts, David Pankratz, Dmitry Tochilkin, Christian Laforte, Robin Rombach, Varun Jampani, 2024) — Adapts Stable Video Diffusion for orbital novel-view synthesis, achieving improved multi-view consistency via temporal video priors over prior image-based methods. ; [stabilityai/sv3d LICENSE (Hugging Face)](https://huggingface.co/stabilityai/sv3d) (Stability AI, 2024) — SV3D weights are distributed under the Stability AI Community License, which permits commercial use free for entities under $1M annual revenue.

### Era3D · `avoid` · ▸ reproduced
**Technically strong (1024x512, 6 views, orthographic-camera variant that aligns the generated front to the input to suppress Janus) but the code/weights are AGPL-3.0 — a copyleft trap that endangers a closed-source commercial game pipeline.**
NeurIPS 2024 high-resolution multi-view diffusion using efficient row-wise attention; outputs 6 views including an orthographic variant designed to keep the generated front view aligned with the input, which helps view consistency. The blocker is licensing: AGPL-3.0 requires that downstream solutions incorporating the code or pretrained model remain open-source.
- **For the pipeline:** The orthographic-camera trick is exactly the kind of Janus mitigation a turnaround pipeline wants, and 1024x512 is the highest native res in this set — so it is painful that AGPL makes it unusable for a closed commercial product. Use it only to study the technique. The same orthographic-front-alignment idea can be reproduced on a commercial-clean stack (Era3D-style row-wise attention concepts informing an MV-Adapter workflow) without inheriting AGPL.
- **Engine:** python · **Applies to:** turnaround · **Base:** SD-based multiview diffusion · **Kind:** model
- **VRAM:** ~16-24 (1024x512 multiview; estimate)
- **Output license:** commercial **no** (license: AGPL-3.0 (copyleft)) — AGPL-3.0 is a strong copyleft / network-copyleft license. Embedding the model or code in a proprietary game or asset-generation service can trigger an obligation to release your derivative under AGPL. For a CLOSED-source commercial studio this is effectively disqualifying unless you obtain a separate commercial license from the authors or keep it strictly to throwaway, non-shipped internal reference (legally gray). Mark as not-commercial-safe by default.
- **Fit:** rig 4/5 · studio 1/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| resolution | 1024x512 | ○ | highest native in set |
| views | 6 (ortho variant available) | ○ | 512-6view-ortho |
| camera | orthographic alignment | ○ | Janus mitigation for low-distortion inputs |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| AGPL forces source disclosure of derivative | copyleft license | do not embed in closed product; seek separate license |  |
| ortho model only suits low-perspective inputs | orthographic assumption | feed flat, centered, low-distortion references |  |

- **Verify:** Both sources resolve. GitHub pengHTYX/Era3D confirmed official, AGPL-3.0 repo AND pretrained model (downstream must open-source) — license and commercial_use=no are CORRECT (decisive axis verified). Minor non-license inaccuracies: paper abstract states up to 512x512 (HF model is MacLab-Era3D-512-6view), not the claimed '1024x512'; the abstract surfaced does not mention the 'orthographic-camera variant.' Row-wise attention 12x compute cut and NeurIPS 2024 confirmed. Verified on license; flag the resolution/orthographic claims for correction. [AGPL-3.0 on the CODE confirmed via GitHub licence API (SPDX agpl-3.0, file 'LICENCE'). But resolution is 512x512 max, not 1024x512 — so it is NOT the highest-res entry — and the HF weights repo is tagged apache-2.0, contradicting 'code/weig]
- **Sources:** [Era3D: High-Resolution Multiview Diffusion using Efficient Row-wise Attention (arXiv:2405.11616, NeurIPS 2024)](https://arxiv.org/abs/2405.11616) (Peng Li, Yuan Liu, Xiaoxiao Long, Feihu Zhang, Cheng Lin, Mengfei Li, Xingqun Qi, Shanghang Zhang, Wenhan Luo, Ping Tan, Wenping Wang, Qifeng Liu, Yike Guo, 2024) — Generates 1024x512 6-view images with an orthographic-camera variant that aligns generated and input front views, reducing multi-view inconsistency while cutting attention compute 12x. ; [pengHTYX/Era3D (official)](https://github.com/pengHTYX/Era3D) (Peng Li et al., 2024) — Repository and pretrained model are released under AGPL-3.0, requiring downstream incorporating solutions to remain open-source.

### Zero123++ · `avoid` · ▸ reproduced
**Strong single-image 6-view generator, but the WEIGHTS are CC-BY-NC 4.0 — non-commercial — which disqualifies it as a base for a commercial sprite pipeline even though the code is Apache-2.0.**
Single-image-to-6-consistent-views diffusion model (6 fixed azimuths in a tiled grid, alternating elevations) built on a Stable-Diffusion image-variation backbone, with an optional depth ControlNet. Very efficient (~5-6GB VRAM). The decisive problem for a commercial studio is the license split: Apache-2.0 code but CC-BY-NC-4.0 weights, so any LoRA or product built on these weights inherits the non-commercial restriction.
- **For the pipeline:** Technically the lineage that made tiled-6-view popular and it sips VRAM on a 5090, but the NC weight license makes it a non-starter for commercial JRPG assets. Treat as a research/prototyping reference only. If you find a workflow you love here, replicate the approach with a commercial-clean base (MV-Adapter on anime SDXL) rather than shipping anything touched by these weights.
- **Engine:** comfyui · **Applies to:** turnaround · **Base:** SD 2.x (image-conditioned) · **Kind:** model
- **VRAM:** 5-6
- **Output license:** commercial **no** (license: code Apache-2.0; weights CC-BY-NC 4.0 (non-commercial)) — Weights are CC-BY-NC 4.0 = non-commercial. Per the authors, you may use the OUTPUTS freely, but you cannot ship the model (or a derivative/LoRA on it) inside a commercial product pipeline. For a studio whose decisive axis is commercial_use, the model itself is out; at most its outputs are a gray-area reference, which is legally risky to rely on for a shipping product.
- **Fit:** rig 5/5 · studio 1/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| views | 6 (tiled grid) | ○ | azimuths 30/90/150/210/270/330 |
| elevations | 20/-10 alternating | ○ | v1.2 |
| min_input | >=320x320 | ○ | low VRAM ~5-6GB |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| commercial product blocked by license | CC-BY-NC weights | do not use weights in a commercial pipeline; switch base |  |
| back/occluded views still hallucinate detail | single-view conditioning | post-clean; not a Janus-solved model |  |

- **Verify:** Both sources resolve. GitHub SUDO-AI-3D/zero123plus confirms code Apache-2.0, weights CC-BY-NC-4.0 (non-commercial), 6 fixed views, ~5GB VRAM (~5.7GB with depth ControlNet sudo-ai/controlnet-zp11-depth-v1). arXiv:2310.15110 title/authors confirmed. License split and commercial_use=no are accurate — weights are non-commercial. [Repo README states verbatim 'code is released under Apache 2.0 and the model weights are released under CC-BY-NC 4.0' — but HF sudo-ai/zero123plus-v1.1 is tagged 'openrail' and v1.2 shows no licence field at all. Contradictory. VRAM ~5GB, ~]
- **Sources:** [SUDO-AI-3D/zero123plus](https://github.com/SUDO-AI-3D/zero123plus) (Ruoxi Shi, Hansheng Chen, Zhuoyang Zhang, Minghua Liu, Chao Xu, Xinyue Wei, Linghao Chen, Chong Zeng, Hao Su, 2023) — Code is Apache-2.0 and model weights are CC-BY-NC-4.0; outputs 6 fixed views; ~5-6GB VRAM with optional depth ControlNet. ; [Zero123++: a Single Image to Consistent Multi-view Diffusion Base Model (arXiv:2310.15110)](https://arxiv.org/abs/2310.15110) (Ruoxi Shi et al., 2023) — Tiles 6 views into one image and uses reference attention to improve cross-view consistency over the original Zero123.

