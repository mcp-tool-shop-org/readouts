# Diffusion sprite-sheet direct
_Text/image -> sprite sheet or 8-direction set directly via diffusion: charturn + pixel-art LoRAs, ControlNet pose sheets._ · wave 5 · 2026-09-07 · [‹ catalog index](README.md)

28 recipes · 5 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | ControlNet OpenPose pose-grid / concept-sheet (SDXL, thibaud) | comfyui | both | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 2 | PixelArtRedmond SDXL LoRA (artificialguybr) | comfyui | both | ▸ reproduced | ⚠ cond | 5 | 3 | ✓ |
| 2 | PixelLab.ai (commercial SaaS, native 4/8-direction + skeleton animation) | custom | both | ▸ reproduced | ✅ yes | 0 | 4 | ✓ |
| 2 | SDXL / Pony / Illustrious / NoobAI base-license axis (the inheritance rule) | comfyui | both | ▸ reproduced | ⚠ cond | 5 | 5 | ✓ |
| 6 | IP-Adapter FaceID + OpenPose identity-locked multi-pose | comfyui | both | · community | ⚠ cond | 5 | 4 | ✓ |
| 6 | SD_PixelArt_SpriteSheet_Generator (Onodofthenorth) | comfyui | game-sprite | ▸ reproduced | ✅ yes | 5 | 2 | ✓ |
| 8 | FLUX.1 Kontext [dev] character turnaround LoRA (single-image → 5-view sheet) | comfyui | turnaround | · single-run | ⚠ cond | 4 | 2 | ✓ |
| 8 | Pixel Art XL (nerijs) | comfyui | both | · single-run | ? unk | 5 | 2 | ✓ |
| 9 | APES — articulated part extraction from sprite sheets (Xu et al. 2022) | comfy | all | paper | check | 4 | 4 | · |
| 9 | Aseprite CLI — sheet export | blender | sprites | docs | check | 4 | 4 | ✓ |
| 9 | BLOCK — MLLM→atlas→NN pixel skin (Guo 2026) | comfy | all | paper | check | 4 | 4 | · |
| 9 | ControlNet spatial conditioning (Zhang et al. 2023) | comfy | sprites | paper | check | 4 | 4 | ✓ |
| 9 | ControlNet++ consistency feedback (Li et al. 2024) | comfy | sprites | paper | check | 4 | 4 | ✓ |
| 9 | DWPose whole-body keypoints (Yang et al. 2023) | comfy | sprites | paper | check | 4 | 4 | ✓ |
| 9 | Diffusers/Comfy ControlNet pose tooling stack | comfy | sprites | docs | check | 4 | 4 | ✓ |
| 9 | IP-Adapter image-prompt companion (Ye et al. 2023) | comfy | sprites | paper | check | 4 | 4 | ✓ |
| 9 | InstantCharacter GH — tuning-free DiT char from one ref | comfy | all | docs | check | 4 | 4 | · |
| 9 | InstantCharacter — DiT identity under pose/text (Tao et al. 2025) | comfy | all | paper | check | 4 | 4 | · |
| 9 | InstantCharacter — identity sheet floor | blender | sprites | paper | check | 4 | 4 | ✓ |
| 9 | InstantID identity under pose (Wang et al. 2024) | comfy | sprites | paper | check | 4 | 4 | ✓ |
| 9 | OpenPose Part Affinity Fields (Cao et al. 2018) | comfy | sprites | paper | check | 4 | 4 | ✓ |
| 9 | Rotate Your Character — video-diffusion turnaround (Wang et al. 2026) | comfy | all | paper | check | 4 | 4 | · |
| 9 | SDXL high-res latent diffusion base (Podell et al. 2023) | comfy | sprites | paper | check | 4 | 4 | ✓ |
| 9 | Sprite Sheet Diffusion — pose-grid sheet-direct | blender | sprites | paper | check | 4 | 4 | ✓ |
| 9 | Sprite Sheet Diffusion — sheet-direct deepen (Hsieh et al. 2024) | comfy | all | paper | check | 4 | 4 | · |
| 9 | T2I-Adapter lightweight spatial control (Mou et al. 2023) | comfy | sprites | paper | check | 4 | 4 | ✓ |
| 9 | thibaud + xinsir SDXL OpenPose ControlNet peers | comfy | sprites | docs | check | 4 | 4 | ✓ |
| 10 | Charturn / Multi-View Turnaround LoRA (Chamber, Illustrious/SDXL) | comfyui | turnaround | · community | ⚠ cond | 5 | 3 | ✓ |

## Detail

### ControlNet OpenPose pose-grid / concept-sheet (SDXL, thibaud) · `recommended` · ▸ reproduced
**Build an explicit multi-pose/multi-direction OpenPose skeleton grid and condition SDXL on it so the model lays out all views at fixed positions — the deterministic layout floor for sprite sheets.**
Rather than hoping a LoRA arranges views, you author an OpenPose control map containing N skeletons (front/side/back/diagonals) on a grid; SDXL with thibaud/controlnet-openpose-sdxl-1.0 fills each pose. Community 'Quick OpenPose Character Concept Sheet Creator' workflows generate the skeleton grid for you. Gives precise control of WHERE each direction lands; identity across cells must come from an added IP-Adapter or character LoRA. Recommended turnaround ControlNet strength 0.4-0.65.
- **For the pipeline:** This is the deterministic-layout floor that satisfies PIN_PER_STEP — the pose grid is an explicit, replayable control artifact, not a prompt gamble. For 8-direction JRPG sprites, author one skeleton grid with all 8 headings and reuse it as a pinned input across the roster. Pair with IP-Adapter/character LoRA for identity (the ceiling). The strongest single building block for a studio pipeline.
- **Engine:** comfyui · **Applies to:** both · **Base:** SDXL · **Kind:** technique
- **VRAM:** 10-14
- **Output license:** commercial **yes** (license: OpenRAIL (ControlNet) + base checkpoint license) — thibaud/controlnet-openpose-sdxl-1.0 is distributed under OpenRAIL (commercial use permitted with RAIL use-restrictions). Base SDXL is Open RAIL++-M. No share-alike. This is a commercially clean lane provided the chosen checkpoint/LoRA layered on top is also commercial-OK.
- **License correction (verifier):** ControlNet license: 'other' (page states it refers to OpenPose's license, NOT explicitly OpenRAIL) + base checkpoint license; commercial_use: unknown (page does not confirm)
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| ControlNet strength (turnaround) | 0.4-0.65 | ○ | third-party guide |
| directions controllable | any (author the skeleton grid) | ○ | 4 or 8 via grid layout |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| identity differs per cell | OpenPose constrains pose, not identity | add IP-Adapter FaceID + character LoRA |  |
| cells bleed into each other | single diffusion canvas | Regional Prompter or per-cell latent masking; or generate cells separately |  |

- **Verify:** Both components resolve: thibaud/controlnet-openpose-sdxl-1.0 exists; OpenArt workflow exists (live slug is.../quick-openpose-character-concept-sheet-creator-v12/F0Cz1ZX0xU7UebTQFyPs, same workflow ID; description of head/body OpenPose grid for concept sheets matches). NOT verified because the license claim is inaccurate: HF page shows 'License: other' deferring to OpenPose's terms, not 'OpenRAIL', and does not affirm commercial use. commercial_use='yes' is overstated. [MOST DAMAGING ERROR IN THE BUCKET. The named checkpoint thibaud/controlnet-openpose-sdxl-1.0 is license: other and its card says it 'refers to the OpenPose's one'; CMU's OpenPose LICENSE permits only 'noncommercial internal research purpose]
- **Sources:** [thibaud/controlnet-openpose-sdxl-1.0](https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0) (Thibaud Zamora, 2023) — OpenPose ControlNet for SDXL 1.0 that conditions generation on a keypoint skeleton control map. ; [Quick OpenPose Character Concept Sheet Creator V1.2 (ComfyUI workflow)](https://openart.ai/workflows/lord_lethris/quick-openpose-character-concept-sheet-creator-v1/F0Cz1ZX0xU7UebTQFyPs) (lord_lethris (OpenArt), 2024) — Workflow auto-generates an OpenPose skeleton grid of multiple head/body positions to drive a multi-pose character concept sheet.

### PixelArtRedmond SDXL LoRA (artificialguybr) · `recommended` · ▸ reproduced
**A widely-used SDXL pixel-art style LoRA under the bespoke-lora-trained-license with allowCommercialUse=Rent — style only, no native directional/sheet output.**
PixelArtRedmond is the most-used general pixel-art LoRA for SDXL (and a separate SD1.5 version). It imposes a pixel-art look; it does NOT generate sprite sheets or directional views on its own. In this lane it is the styling layer you stack on top of a charturn/ControlNet pose-grid lane. The SD1.5 card publishes a bespoke-lora-trained-license with allowCommercialUse=Rent, allowDerivatives=True, no credit required.
- **For the pipeline:** This is the style coat, not the sheet engine. For a 2.5D JRPG, pair it with a ControlNet pose-grid or charturn LoRA to get directional layouts, then PixelArtRedmond gives the consistent pixel aesthetic. Downscale 8x for pixel-perfect output. License is commercial-OK for outputs but confirm the exact SDXL version flag before shipping; default to the SD1.5 card's documented Rent terms as the known-good baseline.
- **Engine:** comfyui · **Applies to:** both · **Base:** SDXL · **Kind:** model
- **VRAM:** 8-12
- **Output license:** commercial **conditional** (license: bespoke-lora-trained-license (allowCommercialUse=Rent) on SD1.5; SDXL version flag unstated; base SDXL Open RAIL++-M) — SD1.5 version's card carries the Civitai bespoke-lora-trained-license: allowCommercialUse=Rent (commercial output OK), allowDerivatives=True, allowDifferentLicense=False. 'Rent' permits using outputs commercially but flags monetizing the model-as-a-service tiers — read the multimodal.art Civitai license matrix. The SDXL version's commercial flag is NOT explicitly stated on the page and must be confirmed per-version on Civitai. Base SDXL 1.0 is Open RAIL++-M (commercial OK).
- **Fit:** rig 5/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| downscale | 8x | ○ | author guidance for pixel-perfect output |
| trigger | Pixel Art / PixArFK | ○ | version-dependent |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| no directional sheet from this LoRA alone | it is a style LoRA, not a layout/turnaround LoRA | stack with ControlNet pose-grid or charturn LoRA |  |

- **Verify:** Both URLs resolve. SDXL Civitai page exists (artificialguybr, pixel-art LoRA). Decisive license metadata confirmed on the SD1.5 README: bespoke-lora-trained-license, allowCommercialUse=Rent, allowDerivatives=True, allowNoCredit=True. SDXL-version flag unstated as the entry admits; 'conditional' is accurate. ['SDXL version flag unstated' is false. Civitai API: PixelArtRedmond (id 144684) = allowCommercialUse [Image, RentCivit, Rent], allowDerivatives true; the 1.5V (id 205955) carries the identical set. Sell is NOT granted on either — sell gener]
- **Sources:** [PixelArtRedmond - Pixel Art Loras for SD XL](https://civitai.com/models/144684/pixelartredmond-pixel-art-loras-for-sd-xl) (artificialguybr, 2023) — Pixel-art style LoRA for SDXL 1.0 by artificialguybr (style conditioning, not sheet generation). ; [PixelArtRedmond (SD1.5) README — license metadata](https://huggingface.co/artificialguybr/pixelartredmond-1-5v-pixel-art-loras-for-sd-1-5/blob/main/README.md) (artificialguybr, 2023) — Carries bespoke-lora-trained-license with allowCommercialUse=Rent, allowDerivatives=True, no credit required.

### PixelLab.ai (commercial SaaS, native 4/8-direction + skeleton animation) · `recommended` · ▸ reproduced
**Purpose-built game-asset SaaS that natively outputs 4/8-directional sprites with one-click rotation and skeleton-based walk/run/attack animation, with a commercial license and full output ownership on paid plans.**
PixelLab is the most production-shaped option: it directly targets RPG sprite work — 4 and 8 directional views, single-click sprite rotation from concept art, skeleton-based animation (walk/run/attack/idle), and map generation. It is a hosted subscription, not a local model, so it does not use the 5090, but it is the only entry that delivers true 8-direction game sprites end-to-end with clear commercial terms.
- **For the pipeline:** For a studio that wants shipped 8-direction sprites without local pipeline-building, PixelLab is the fastest path with the cleanest rights. The catch for THIS studio: the 'do not train models on the images' clause means PixelLab output cannot become style-dataset-lab training data — so it is a direct asset producer, not a canon/training feeder. Runs off-rig (no 5090 use), $12/mo entry tier, 320x320 cap on tier 1.
- **Engine:** custom · **Applies to:** both · **Base:** n/a (hosted) · **Kind:** pipeline
- **Output license:** commercial **yes** (license: Proprietary SaaS terms — user owns outputs, commercial OK on paid plans; no model-training on outputs) — Per PixelLab's terms: you own the copyright to your creations and may use them commercially with no permission needed; commercial licensing is included with all paid plans; the only restriction is you may not train new models on the generated images. The platform itself references the Open RAIL-M license framework for use. This is a clean commercial path — but the no-training restriction directly conflicts with feeding outputs into style-dataset-lab training.
- **Fit:** rig 0/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| directions | 4 and 8 | ○ | native isometric/top-down |
| animation | skeleton-based walk/run/attack/idle | ○ | rig + animate |
| tier-1 resolution cap | 320x320 | ○ | $12/mo Pixel Apprentice |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| cannot use outputs as training data | ToS forbids training models on generated images | keep PixelLab as direct-asset lane, not a style-dataset-lab feeder |  |
| no local/offline use | hosted SaaS | use for direct production; use local lanes where on-rig control/canon binding is required |  |

- **Verify:** Both pages resolve. pixellab.ai confirms 4 & 8 directional views + skeleton-based walk/run/attack animations and one-click rotation from concept art. ToS (dated 2025-11-23) Section 3.3 confirms users retain ownership and may use outputs commercially for any purpose; sole material restriction is no training other models on outputs. License accurate. [Site confirms '4 or 8 directional views', one-click rotation and skeleton-based animation. ToS 3.3: 'You retain ownership of any content you create ... free to use, modify, and distribute the outputs ... for any purpose'; 1.2 bars using out]
- **Sources:** [PixelLab — AI Generator for Pixel Art Game Assets](https://www.pixellab.ai/) (PixelLab, 2025) — Generates 4 and 8 directional views and skeleton-based walk/run/attack animations, with one-click sprite rotation from concept art. ; [PixelLab Terms of Service / commercial-use summary](https://www.pixellab.ai/termsofservice) (PixelLab, 2025) — Users own copyright to their creations and may use them commercially with no permission; only restriction is not training new models on the images.

### SDXL / Pony / Illustrious / NoobAI base-license axis (the inheritance rule) · `recommended` · ▸ reproduced
**Because a LoRA inherits its base model's license, the commercial-use answer for every charturn/pixel-art LoRA is decided by which SDXL-family base it sits on — and those bases differ materially.**
This entry is the decisive cross-cutting axis, not a tool. Every LoRA above inherits its base. The bases: SDXL 1.0 = CreativeML Open RAIL++-M (commercial OK). Illustrious-XL = now redistributed under CreativeML Open RAIL (SDXL) (commercial OK; older v0.1 was FAIPL 1.0). NoobAI = built on Illustrious under Fair AI Public License 1.0-SD (SHARE-ALIKE: derivatives must pass on the same freedoms; no new restrictions; image outputs unrestricted). Pony Diffusion V6 = its own permissive terms allowing commercial output. The practical rule: trace the LoRA -> base -> base license, then ALSO check the Civitai card's per-version allowCommercialUse flag, because a permissive base does not override a restrictive LoRA card.
- **For the pipeline:** Make 'base + Civitai flag' a pinned, recorded field in every sprite asset's provenance (PIN_PER_STEP / repo-knowledge entry). Prefer LoRAs on SDXL 1.0 or Illustrious bases for the cleanest commercial answer; treat NoobAI-based LoRAs as fine for output but watch the share-alike clause if you redistribute trained weights; avoid putting FLUX-dev anywhere in the production path without BFL's paid license. This axis, not image quality, is what gates a commercial JRPG ship.
- **Engine:** comfyui · **Applies to:** both · **Base:** SDXL / Pony / Illustrious / NoobAI · **Kind:** eval
- **VRAM:** 8-14
- **Output license:** commercial **conditional** (license: Open RAIL++-M (SDXL) / Open RAIL (Illustrious) / FAIPL 1.0-SD (NoobAI) / Pony terms) — SDXL 1.0 = Open RAIL++-M (commercial OK, RAIL use-restrictions apply). Illustrious-XL = CreativeML Open RAIL (commercial OK). NoobAI = FAIPL 1.0-SD share-alike (commercial OK on outputs, but derivative MODELS must keep the same license — relevant if you train + redistribute a LoRA on NoobAI). Pony V6 = permissive, commercial output OK. RAIL-class licenses never restrict the images themselves, only model use. Decisive workflow: (1) identify base, (2) read base license, (3) confirm Civitai per-version allowCommercialUse flag — the stricter of the two governs.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| license-trace rule | LoRA -> base -> base license + Civitai flag | ○ | stricter of the two governs |
| RAIL image restriction | none on outputs | ○ | RAIL restricts model use, not generated images |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| assume commercial OK from base alone | ignoring the LoRA card's own allowCommercialUse flag | always confirm per-version Civitai flag; stricter term wins |  |
| share-alike surprise on redistributed weights | training/redistributing a LoRA on a NoobAI/FAIPL base | keep redistributed derivatives under FAIPL; or train on Open RAIL base instead |  |

- **Verify:** SDXL LICENSE.md resolves: CreativeML Open RAIL++-M (dated 2023-07-26), royalty-free commercial use with use-based restrictions, no rights claimed in outputs - all confirmed. Illustrious-XL-v2.0 discussion resolves and confirms redistribution under CreativeML Open RAIL (SDXL) permitting commercial use. Caveat: that specific discussion does NOT mention NoobAI or FAIPL 1.0-SD share-alike inheritance (only covers Illustrious); the NoobAI/FAIPL part of the claim is not supported by the cited source, though documented elsewhere. Core SDXL/Illustrious axis verified; NoobAI sub-claim is undersourced. [Three of four bases verified exactly as claimed: SDXL 1.0 = CreativeML Open RAIL++-M; Illustrious-XL v0.1 = fair-ai-public-license-1.0-sd and v1.0 = sdxl-license (the relicensing is real); NoobAI-XL v1.1 = fair-ai-public-license-1.0-sd. Pon]
- **Sources:** [stabilityai/stable-diffusion-xl-base-1.0 LICENSE.md (CreativeML Open RAIL++-M)](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/LICENSE.md) (Stability AI, 2023) — SDXL 1.0 is licensed under CreativeML Open RAIL++-M, granting royalty-free commercial use with use-based restrictions and no restrictions on generated images. ; [What The License?! (Civitai) + Illustrious-XL v2.0 license discussion](https://huggingface.co/OnomaAIResearch/Illustrious-XL-v2.0/discussions/1) (Civitai / OnomaAIResearch, 2025) — Illustrious-XL is redistributed under CreativeML Open RAIL (SDXL) permitting commercial use; NoobAI built on it inherits Fair AI Public License 1.0-SD share-alike terms.

### IP-Adapter FaceID + OpenPose identity-locked multi-pose · `recommended` · · community
**Lock identity with IP-Adapter FaceID (no training) while OpenPose drives each direction; community reports >95% identity accuracy when both are combined.**
The training-free identity lane: feed one (or several averaged) reference images into IP-Adapter + FaceID to fix face/structure, and use OpenPose ControlNet to place each directional pose. Community workflows report >95% identity accuracy when FaceID is combined with OpenPose, with tuning around IPAdapter weight ~0.75 / FaceID ~0.6 (raise to ~1.2 to stabilize identity in hard poses). The complement to the ControlNet pose-grid: grid = where, FaceID = who.
- **For the pipeline:** For a studio, prefer plain IP-Adapter (image-prompt) over FaceID to sidestep InsightFace's non-commercial models, accepting slightly lower face lock and compensating with a trained character LoRA from style-dataset-lab. This is the identity ceiling on top of the OpenPose floor — together they implement the deterministic-floor + learned-ceiling pattern. Average multiple reference angles to avoid single-view fixation.
- **Engine:** comfyui · **Applies to:** both · **Base:** SDXL · **Kind:** technique
- **VRAM:** 10-14
- **Output license:** commercial **conditional** (license: IP-Adapter Apache-2.0; FaceID depends on InsightFace (non-commercial); base checkpoint license) — The IP-Adapter weights (h94/IP-Adapter, FaceID) are Apache-2.0-class for the adapter, but FaceID variants depend on InsightFace, whose models are released for NON-COMMERCIAL research use — this is the catch for a commercial studio. Plain IP-Adapter (image prompt, no FaceID/InsightFace) avoids that restriction and is the safer commercial path. Base checkpoint license also applies. Verify the InsightFace dependency before shipping.
- **Fit:** rig 5/5 · studio 4/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| IPAdapter weight | ~0.75 | ○ | community default |
| FaceID weight | ~0.6 | ○ | community default; raise to 1.2 for hard poses |
| identity accuracy (FaceID+OpenPose) | >95% | ○ | community claim, not measured |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| plastic / distorted faces | IPAdapter weight too high | lower to ~0.7, enable FaceDetailer with bbox detection |  |
| InsightFace license blocks commercial ship | FaceID depends on non-commercial InsightFace models | use plain IP-Adapter image-prompt + trained character LoRA instead |  |

- **Verify:** Both sources resolve. sozee.ai tutorial confirms IPAdapter FaceID + OpenPose ControlNet combo and the >95% face-accuracy figure, and references InsightFace embeddings. InsightFace GitHub confirms the decisive constraint: code is MIT but pretrained models are 'available for non-commercial research purposes only' — so 'conditional' license is accurate. (Note: the Medium/SophieZ source does NOT describe 'averaging multiple reference angles'; author abandons that approach for Flux+template. Secondary source claim is loose, but primary technique+license verify.) [Licence chain confirmed and worse than stated: h94/IP-Adapter-FaceID says 'released exclusively for research purposes and is not intended for commercial use', and the OpenPose half is CMU-noncommercial unless swapped to xinsir. The '>95% id]
- **Sources:** [How to Use IPAdapter FaceID with Stable Diffusion](https://sozee.ai/resources/ipadapter-faceid-stable-diffusion-tutorial/) (sozee.ai, 2025) — Combining IPAdapter FaceID with OpenPose ControlNet is reported to reach over 95% identity accuracy across poses. ; [How I Solved Character Consistency in ComfyUI (ControlNet and IPAdapter)](https://medium.com/@sophie_62065/how-i-solved-character-consistency-in-comfyui-after-trying-controlnet-and-ipadapter-fcd9eda25109) (SophieZ (Medium), 2025) — Averaging multiple reference angles into IPAdapter captures a character from multiple views and reduces single-image fixation across poses.

### SD_PixelArt_SpriteSheet_Generator (Onodofthenorth) · `situational` · ▸ reproduced
**A finetuned SD checkpoint with four directional trigger tokens (Front/Right/Back/Left) that emits 4-direction pixel sprites and is released under Apache 2.0 — the cleanest commercial license in this lane.**
A purpose-built SD checkpoint for RPG sprite work: prompt with PixelartFSS / RSS / BSS / LSS to pull front, right, back, left views. Author advises merging it with a character-trained model to get consistent identity per view, then cleaning up in Krita/Photoshop. It is old (SD 1.x era) and low-res, but it is the only model in this survey under an unambiguous permissive license.
- **For the pipeline:** License is perfect for a commercial studio, but SD 1.x quality and 4 (not 8) directions make it a legacy fallback, not a primary lane. Useful as a clean-license seed model to merge a style-dataset-lab-trained character into for true directional pixel sprites without license risk. Only 4 directions — diagonals must come from elsewhere.
- **Engine:** comfyui · **Applies to:** game-sprite · **Base:** SD 1.x · **Kind:** model
- **VRAM:** 4-6
- **Output license:** commercial **yes** (license: Apache 2.0) — Apache 2.0 — explicit, unambiguous commercial use, derivatives, and redistribution permitted. No share-alike, no RAIL use-restrictions. This is the only model in the lane with a fully clean OSI license; everything else is RAIL-class or non-commercial-model.
- **Fit:** rig 5/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| trigger tokens | PixelartFSS / RSS / BSS / LSS | ○ | front/right/back/left |
| directions | 4 | ○ | no native diagonals |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| character identity varies per view | base model has no identity lock | merge with a character-trained model before generating |  |
| low fidelity / dated look | SD 1.x lineage | use as a directional scaffold, restyle via SDXL/Sprite Foundry |  |

- **Verify:** HF page resolves; SD checkpoint by Onodofthenorth generating pixel-art sprites from four angles (front/back/left/right via trigger words) confirmed. Apache 2.0 stated on the card; commercial use permitted. Accurate. [HF card declares license: apache-2.0 — the unambiguous permissive licence, as claimed. All four trigger tokens confirmed on the card: PixelartFSS (front), PixelartRSS (right), PixelartBSS (back), PixelartLSS (left); four directions, no diag]
- **Sources:** [SD_PixelArt_SpriteSheet_Generator](https://huggingface.co/Onodofthenorth/SD_PixelArt_SpriteSheet_Generator) (Onodofthenorth, 2022) — SD checkpoint generating pixel-art sprites from four angles via trigger words, released under Apache 2.0 (commercial use permitted).

### FLUX.1 Kontext [dev] character turnaround LoRA (single-image → 5-view sheet) · `situational` · · single-run
**The strongest 2026 single-image-to-turnaround lane (one illustration → front/profile/3-4/back in one shot) — but the FLUX.1 Kontext [dev] MODEL is non-commercial, so a studio needs BFL's paid license to use it in production.**
FLUX.1 Kontext [dev] is an image-editing/instruction model; a community turnaround LoRA (reverentelusarca, via Ostris AI-Toolkit) turns a single character illustration into a 5-view turnaround sheet in one pass, with markedly better structural consistency than SDXL prompting. This is the most capable single-image->multi-view lane in the survey. The decisive issue is licensing, not quality.
- **For the pipeline:** Best-in-class single-image turnaround, but the non-commercial model license is the hard gate for a commercial studio on this rig. Two clean paths: (1) purchase BFL's self-serve commercial license and use Kontext-dev legitimately in production, or (2) confine it to non-commercial R&D/look-dev and ship via SDXL/Apache-licensed lanes. The 'cannot train a competitor on outputs' clause specifically threatens using its turnarounds as style-dataset-lab training data — read before ingesting.
- **Engine:** comfyui · **Applies to:** turnaround · **Base:** Flux (Kontext dev) · **Kind:** workflow
- **VRAM:** 16-24
- **Output license:** commercial **conditional** (license: FLUX.1 Non-Commercial License (model); outputs unrestricted; commercial pipeline needs BFL paid license) — DECISIVE: FLUX.1 [dev] and FLUX.1 Kontext [dev] models are licensed under the FLUX.1 Non-Commercial License — the MODEL may not be used for commercial/production purposes. BFL claims no ownership of OUTPUTS (outputs usable commercially), but running the model inside a commercial production pipeline requires a paid self-serve commercial license from Black Forest Labs. A LoRA inherits the base license, so this turnaround LoRA is non-commercial-model. For a commercial JRPG studio: either buy BFL's commercial license or do not put Kontext-dev in the production path. Also: license forbids using outputs to train a competing model — relevant if feeding style-dataset-lab.
- **Fit:** rig 4/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| views per generation | 5 (front/profile/3-4/back) | ○ | from one input image |
| VRAM (Flux-class) | 16-24GB typical | ○ | fits comfortably on 32GB 5090 |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| poor results on photos / tight headshots | LoRA trained on full-body stylized illustration | feed full-body stylized character art |  |
| commercial-license violation | Kontext-dev model is non-commercial | acquire BFL self-serve commercial license or keep out of production path |  |

- **Verify:** RunComfy workflow resolves: single illustration -> five-view turnaround (front/profile/3-4/back), by reverentelusarca, trained with Ostris AI-Toolkit, all confirmed. BFL LICENSE.md resolves and confirms: non-commercial use only, BFL claims no ownership of outputs, commercial model use requires a separate license from BFL. License accurate. [LoRA is real (HF reverentelusarca/kontext-turnaround-sheet-lora-v1, licence flux-kontext-dev-license; Civitai 1753109; Ostris AI-Toolkit confirmed) but it is a SIX-pose sheet, not five. Base licence is 'FLUX.1 [dev] Non-Commercial License v]
- **Sources:** [FLUX.1 Kontext [dev] character turnaround sheet LoRA (ComfyUI workflow)](https://www.runcomfy.com/comfyui-workflows/flux-kontext-character-turnaround-sheet-lora) (reverentelusarca / RunComfy, 2026) — Transforms a single character illustration into a five-view turnaround sheet (front/profile/3-4/back) via a Kontext LoRA trained with Ostris AI-Toolkit. ; [FLUX.1-Kontext-dev LICENSE.md (FLUX.1 Non-Commercial License)](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/blob/main/LICENSE.md) (Black Forest Labs, 2025) — Model licensed for non-commercial purposes only; BFL claims no ownership of outputs but commercial production use of the model requires a separate license.

### Pixel Art XL (nerijs) · `situational` · · single-run
**The other dominant SDXL pixel-art style LoRA; high quality and works at low step counts, but its Civitai page publishes no license terms — a commercial-use unknown.**
nerijs's Pixel Art XL is a top-tier SDXL pixel-art style LoRA (notably effective with LCM/low steps), used as the aesthetic layer in pixel sprite pipelines. Like PixelArtRedmond it is style-only — no directional or sheet logic. The decisive problem for a commercial studio is that its Civitai page does not state a license or commercial-use flag.
- **For the pipeline:** Quality rivals PixelArtRedmond, but the missing license makes it the riskier choice for shipping product. Prefer PixelArtRedmond (documented Rent terms) or the Apache-2.0 sprite-sheet model for anything that reaches a commercial build, unless/until you confirm Pixel Art XL's flag. Fine for prototyping/look-dev.
- **Engine:** comfyui · **Applies to:** both · **Base:** SDXL · **Kind:** model
- **VRAM:** 8-12
- **Output license:** commercial **unknown** (license: Unstated on model page) — No license or allowCommercialUse value is published on the model page at fetch time. For a commercial studio this is a hard blocker until the per-version Civitai flag is confirmed. Base SDXL is Open RAIL++-M, but the LoRA author's own terms govern and are absent here. Do not assume commercial OK.
- **Fit:** rig 5/5 · studio 2/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| downscale | 8x | ○ | author: downscale 8x for pixel-perfect |
| trigger avoidance | avoid 'pixel art' in prompt | ○ | author guidance |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| cannot clear legal review | no published license | contact author / confirm Civitai flag, or substitute a documented-license LoRA |  |

- **Verify:** Civitai page resolves; Pixel Art XL by nerijs/NeriJS, SDXL 1.0 LoRA confirmed. Page genuinely states no license / commercial-use terms, so the entry's commercial_use='unknown' is itself the accurate finding. Verified. ['No license terms published' is false on BOTH platforms. Civitai API model 120096 returns allowCommercialUse: [] (empty — none granted), allowDerivatives false, allowNoCredit false. HF nerijs/pixel-art-xl declares creativeml-openrail-m. The]
- **Sources:** [Pixel Art XL - v1.1](https://civitai.com/models/120096/pixel-art-xl) (nerijs (NeriJS), 2023) — SDXL pixel-art style LoRA by nerijs; page provides no license or commercial-use terms.

### APES — articulated part extraction from sprite sheets (Xu et al. 2022) · `situational` · paper
**Articulated part extraction from sprite sheets — sheet-direct part structure deepen; flip 486: 0.**
STUDY-059 Scholar deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** comfy · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [APES](https://arxiv.org/abs/2206.02015) — Articulated part extraction from sprite sheets.

### Aseprite CLI — sheet export · `situational` · docs
**Batch -b export: --sheet + --data (json-hash/json-array); sheet-type horizontal/vertical/rows/columns/packed.**
Batch -b export: --sheet + --data (json-hash/json-array); sheet-type horizontal/vertical/rows/columns/packed.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [Every flag confirmed verbatim in the official CLI docs: -b/--batch, --sheet <file.png>, --data <file.json>, --format json-hash (default) | json-array, and --sheet-type horizontal|vertical|rows|columns|packed. Licence: Aseprite EULA — propri]
- **Sources:** [Aseprite CLI — sheet export](https://www.aseprite.org/docs/cli/) — Batch -b export: --sheet + --data (json-hash/json-array); sheet-type horizontal/vertical/rows/columns/packed.

### BLOCK — MLLM→atlas→NN pixel skin (Guo 2026) · `situational` · paper
**MLLM→atlas→NN pixel skin pipeline — sheet-direct pixel finish deepen; flip 486: 0.**
STUDY-059 Scholar deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** comfy · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [BLOCK](https://arxiv.org/abs/2603.03964) — MLLM→atlas→NN pixel skin pipeline.

### ControlNet spatial conditioning (Zhang et al. 2023) · `situational` · paper
**ControlNet locks pose/edges/depth onto frozen T2I — sheet-direct OpenPose floor**
STUDY-038 Scholar deepen.
- **For the pipeline:** STUDY-038 Verifier ✅.
- **Engine:** comfy · **Applies to:** sprites · **Base:** SDXL|SD15|general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-038 deepen; verified=0; flip 486: 0; 486 stays avoid.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-038 deepen [arXiv 2302.05543 = 'Adding Conditional Control to Text-to-Image Diffusion Models', Lvmin Zhang, 2023 — ID, author and year all match. Abstract verbatim: 'ControlNet locks the production-ready large diffusion models'. Repo lllyasviel/Control]
- **Sources:** [ControlNet](https://arxiv.org/abs/2302.05543) — Conditional control for T2I diffusion.

### ControlNet++ consistency feedback (Li et al. 2024) · `situational` · paper
**Consistency-feedback training to tighten control adherence — pose fidelity deepen; no invent thibaud weights.**
STUDY-038 Scholar deepen.
- **For the pipeline:** STUDY-038 Verifier ✅.
- **Engine:** comfy · **Applies to:** sprites · **Base:** SDXL|SD15|general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-038 deepen; verified=0; flip 486: 0; 486 stays avoid.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-038 deepen [arXiv 2404.07987 = 'ControlNet++: Improving Conditional Controls with Efficient Consistency Feedback', Ming Li, 2024 — ID, author and year match. Abstract confirms pixel-level cycle consistency optimised via a pretrained discriminative rewa]
- **Sources:** [ControlNet++](https://arxiv.org/abs/2404.07987) — Efficient consistency feedback for controls.

### DWPose whole-body keypoints (Yang et al. 2023) · `situational` · paper
**Two-stage distillation for whole-body keypoints — richer pose maps for combat silhouette readability.**
STUDY-038 Scholar deepen.
- **For the pipeline:** STUDY-038 Verifier ✅.
- **Engine:** comfy · **Applies to:** sprites · **Base:** SDXL|SD15|general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-038 deepen; verified=0; flip 486: 0; 486 stays avoid.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-038 deepen [arXiv 2307.15880 = 'Effective Whole-body Pose Estimation with Two-stages Distillation', Zhendong Yang, 2023 — matches Yang et al. 2023. DWPose = Distillation for Whole-body Pose; two-stage distillation confirmed (RTMPose-l whole-body AP 64.]
- **Sources:** [DWPose](https://arxiv.org/abs/2307.15880) — Effective whole-body pose estimation.

### Diffusers/Comfy ControlNet pose tooling stack · `situational` · docs
**Diffusers SDXL ControlNet API + Comfy ControlNet/Pose examples + lllyasviel SD15 openpose preprocessor — sourced peers.**
STUDY-038 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-038 Verifier ✅.
- **Engine:** comfy · **Applies to:** sprites · **Base:** SDXL|SD15|general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-038 deepen; verified=0; flip 486: 0; 486 stays avoid.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-038 deepen [All three legs verified. Diffusers officially documents StableDiffusionXLControlNetPipeline; ComfyUI_examples publishes Pose/Scribble/Depth/Mixed ControlNet workflows; lllyasviel/sd-controlnet-openpose exists on SD1.5 under CreativeML OpenR]
- **Sources:** [Diffusers ControlNet using guide](https://huggingface.co/docs/diffusers/en/using-diffusers/controlnet) — SDXL Multi-ControlNet / conditioning_scale. ; [Diffusers ControlNet API](https://huggingface.co/docs/diffusers/en/api/pipelines/controlnet) — Spatial conditioning via control image. ; [ComfyUI ControlNet examples](https://comfyanonymous.github.io/ComfyUI_examples/controlnet/) — Pose ControlNet example; preprocess separately. ; [lllyasviel/control_v11p_sd15_openpose](https://huggingface.co/lllyasviel/control_v11p_sd15_openpose) — CN v1.1 OpenPose hand+face.

### IP-Adapter image-prompt companion (Ye et al. 2023) · `situational` · paper
**Decoupled image-prompt adapter compatible with text — identity-lock companion to OpenPose; no flip 486.**
STUDY-038 Scholar deepen.
- **For the pipeline:** STUDY-038 Verifier ✅.
- **Engine:** comfy · **Applies to:** sprites · **Base:** SDXL|SD15|general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-038 deepen; verified=0; flip 486: 0; 486 stays avoid.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-038 deepen [arXiv 2308.06721 = 'IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models', Hu Ye, 2023 — matches Ye et al. 2023. Decoupled cross-attention confirmed verbatim; 22M params. HF h94/IP-Adapter declares license: ap]
- **Sources:** [IP-Adapter](https://arxiv.org/abs/2308.06721) — Text-compatible image prompt adapter.

### InstantCharacter GH — tuning-free DiT char from one ref · `situational` · docs
**Tuning-free DiT char from one ref; SigLIP+DINOv2 on FLUX — identity peer; flip 486: 0.**
STUDY-059 Practitioner deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** comfy · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [InstantCharacter GH](https://github.com/Tencent/InstantCharacter) — Tuning-free DiT char from one ref; SigLIP+DINOv2 on FLUX.

### InstantCharacter — DiT identity under pose/text (Tao et al. 2025) · `situational` · paper
**DiT identity under pose/text edits — sheet-direct identity deepen; flip 486: 0.**
STUDY-059 Scholar deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** comfy · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [InstantCharacter](https://arxiv.org/abs/2504.12395) — DiT identity under pose/text edits.

### InstantCharacter — identity sheet floor · `situational` · paper
**DiT full-transformer character adapter (SigLIP+DINOv2) keeps open-domain identity under pose/text edits — sheet-direct identity floor.**
DiT full-transformer character adapter (SigLIP+DINOv2) keeps open-domain identity under pose/text edits — sheet-direct identity floor.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [Architecture confirmed (arXiv 2504.12395, Tao 2025; repo pins google/siglip-so400m-patch14-384 + facebook/dinov2-giant on FLUX.1-dev). But Tencent's License.txt limits it to 'academic, research and education purposes' and says to 'refrain f]
- **Sources:** [InstantCharacter — identity sheet floor](https://arxiv.org/abs/2504.12395) — DiT full-transformer character adapter (SigLIP+DINOv2) keeps open-domain identity under pose/text edits — sheet-direct identity floor.

### InstantID identity under pose (Wang et al. 2024) · `situational` · paper
**Zero-shot identity-preserving generation with ID tokens + ControlNet-compatible pose — sheet-direct identity under pose edits.**
STUDY-038 Scholar deepen.
- **For the pipeline:** STUDY-038 Verifier ✅.
- **Engine:** comfy · **Applies to:** sprites · **Base:** SDXL|SD15|general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-038 deepen; verified=0; flip 486: 0; 486 stays avoid.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-038 deepen [arXiv 2401.07519 = 'InstantID: Zero-shot Identity-Preserving Generation in Seconds', Qixun Wang, 2024 — matches Wang et al. 2024. IdentityNet with strong semantic and weak spatial conditions confirmed. Licence chain: repo is Apache-2.0 BUT ]
- **Sources:** [InstantID](https://arxiv.org/abs/2401.07519) — Zero-shot identity-preserving generation.

### OpenPose Part Affinity Fields (Cao et al. 2018) · `situational` · paper
**Multi-person 2D pose via PAFs — canonical skeleton maps for ControlNet OpenPose pose-grids.**
STUDY-038 Scholar deepen.
- **For the pipeline:** STUDY-038 Verifier ✅.
- **Engine:** comfy · **Applies to:** sprites · **Base:** SDXL|SD15|general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-038 deepen; verified=0; flip 486: 0; 486 stays avoid.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-038 deepen [arXiv 1812.08008 = 'OpenPose: Realtime Multi-Person 2D Pose Estimation using Part Affinity Fields', Zhe Cao, 2018 — matches Cao et al. 2018; PAFs confirmed verbatim. Licence is the load-bearing fact: CMU's LICENSE permits use only 'for your]
- **Sources:** [OpenPose](https://arxiv.org/abs/1812.08008) — Realtime multi-person 2D pose estimation.

### Rotate Your Character — video-diffusion turnaround (Wang et al. 2026) · `situational` · paper
**Video-diffusion turnaround for 3D characters — sheet-direct/turnaround deepen; flip 486: 0.**
STUDY-059 Scholar deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** comfy · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [Rotate Your Character](https://arxiv.org/abs/2601.05722) — Video-diffusion turnaround for 3D characters.

### SDXL high-res latent diffusion base (Podell et al. 2023) · `situational` · paper
**SDXL architecture for high-res synthesis — base axis for OpenPose SDXL ControlNets; not a named checkpoint recipe.**
STUDY-038 Scholar deepen.
- **For the pipeline:** STUDY-038 Verifier ✅.
- **Engine:** comfy · **Applies to:** sprites · **Base:** SDXL|SD15|general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-038 deepen; verified=0; flip 486: 0; 486 stays avoid.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-038 deepen [arXiv 2307.01952 = 'SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis', Dustin Podell, 2023 — matches Podell et al. 2023. Abstract confirms the three-times-larger UNet and second text encoder. stabilityai/stable-di]
- **Sources:** [SDXL](https://arxiv.org/abs/2307.01952) — Improving latent diffusion for high-res.

### Sprite Sheet Diffusion — pose-grid sheet-direct · `situational` · paper
**Animate-Anyone-style ReferenceNet + Pose Guider + Motion Module fine-tuned on game sprite+pose pairs — pose-grid sheet-direct as discrete frames.**
Animate-Anyone-style ReferenceNet + Pose Guider + Motion Module fine-tuned on game sprite+pose pairs — pose-grid sheet-direct as discrete frames.
- **For the pipeline:** STUDY-007 Verifier-verified. Sheet craft / ortho / palette / identity floors.
- **Engine:** blender · **Applies to:** sprites · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-017 reopen; verified=0 until ACCEPT.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-017 from STUDY-007 Verifier ✅; default verified=0 [Real and better-licensed than 'see-source': arXiv 2412.03685 (Hsieh, Zhang, Yan 2024), repo chenganhsieh/Sprite-Sheet-Diffusion is MIT with CC0 training data, built on Moore-AnimateAnyone. But it generates ANIMATION motion frames (run/walk/]
- **Sources:** [Sprite Sheet Diffusion — pose-grid sheet-direct](https://arxiv.org/abs/2412.03685) — Animate-Anyone-style ReferenceNet + Pose Guider + Motion Module fine-tuned on game sprite+pose pairs — pose-grid sheet-direct as discrete frames.

### Sprite Sheet Diffusion — sheet-direct deepen (Hsieh et al. 2024) · `situational` · paper
**Game sprite+pose sheet-direct diffusion — leftover deepen beyond STUDY-038; flip 486: 0.**
STUDY-059 Scholar deepen. Flip 486: 0. Recipes invented: 0.
- **For the pipeline:** STUDY-059 Verifier ✅. Flip 486: 0. Recipes invented: 0.
- **Engine:** comfy · **Applies to:** all · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-059 deepen; verified=0; flip 486: 0; recipes invented: 0.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-059 deepen; flip 486: 0; recipes invented: 0 [no external verdict — not checked]
- **Sources:** [Sprite Sheet Diffusion](https://arxiv.org/abs/2412.03685) — Game sprite+pose sheet-direct diffusion.

### T2I-Adapter lightweight spatial control (Mou et al. 2023) · `situational` · paper
**Lightweight sketch/pose/depth adapters — alternate spatial-control class for sheet-direct pose grids.**
STUDY-038 Scholar deepen.
- **For the pipeline:** STUDY-038 Verifier ✅.
- **Engine:** comfy · **Applies to:** sprites · **Base:** SDXL|SD15|general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-038 deepen; verified=0; flip 486: 0; 486 stays avoid.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-038 deepen [arXiv 2302.08453 = 'T2I-Adapter: Learning Adapters to Dig out More Controllable Ability for Text-to-Image Diffusion Models', Chong Mou, 2023 — matches Mou et al. 2023. Abstract confirms lightweight adapters 'while freezing the original larg]
- **Sources:** [T2I-Adapter](https://arxiv.org/abs/2302.08453) — Adapters for controllable T2I.

### thibaud + xinsir SDXL OpenPose ControlNet peers · `situational` · docs
**SDXL OpenPose ControlNets (thibaud + Apache xinsir) on SDXL base — sourced pose-grid tooling**
STUDY-038 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-038 Verifier ✅.
- **Engine:** comfy · **Applies to:** sprites · **Base:** SDXL|SD15|general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-038 deepen; verified=0; flip 486: 0; 486 stays avoid.
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-038 deepen [Both exist and xinsir/controlnet-openpose-sdxl-1.0 is apache-2.0 as claimed. The error is pairing them as interchangeable peers: thibaud/controlnet-openpose-sdxl-1.0 is license: other and its card says it 'refers to the OpenPose's one' (CMU]
- **Sources:** [thibaud/controlnet-openpose-sdxl-1.0](https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0) — SDXL OpenPose CN + Comfy workflow. ; [xinsir/controlnet-openpose-sdxl-1.0](https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0) — Apache-2.0 SDXL OpenPose peer. ; [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) — SDXL base Open RAIL++-M. ; [ComfyUI #1184 SDXL ControlNet](https://github.com/comfyanonymous/ComfyUI/issues/1184) — Use SDXL ControlNets; thibaud cited working.

### Charturn / Multi-View Turnaround LoRA (Chamber, Illustrious/SDXL) · `situational` · · community
**A LoRA trained on ~80 3D-render turntables that forces a single generation to emit front/side/back/3-4 views with shared identity, but needs stacked helper LoRAs to hold face/clothing.**
Chamber's Charturn family (IL/XL merged + Pony + XL variants) is the de-facto community turnaround LoRA. Trained on ~80 3D-model render turntables, it conditions one image into a multi-view model sheet. Identity holds at the 'model-sheet' level but the author explicitly says body/face/mechanical turns still need a secondary 'Helper LoRA' (main ~0.7, helper ~0.15). Designed around the author's own ComfyUI workflows; outside them consistency degrades. Best on Illustrious base, with a weaker SDXL 1.0 variant.
- **For the pipeline:** Highest-leverage open turnaround LoRA for a JRPG studio doing 4-view character sheets as reference plates, but it is a 'sheet generator,' not a clean 8-direction game sprite. Treat output as concept/reference upstream of Sprite Foundry, not as ship-ready directional sprites. Budget for helper-LoRA stacking and 10-20 gens + hand-pick. Pin the exact Illustrious base version for license certainty (study-swarm: verify the Civitai allowCommercialUse flag per version).
- **Engine:** comfyui · **Applies to:** turnaround · **Base:** SDXL (Illustrious) · **Kind:** model
- **VRAM:** 8-12
- **Output license:** commercial **conditional** (license: Base: CreativeML Open RAIL (Illustrious) / Open RAIL++-M (SDXL); LoRA card commercial flag unstated) — License inheritance: a LoRA carries its BASE model's license. Illustrious-XL is now redistributed under CreativeML Open RAIL (SDXL) which permits commercial use (older v0.1 was FAIPL 1.0). So the Illustrious-based Charturn is commercially usable IF the Civitai model card's own allowCommercialUse flag also permits it — the card itself does NOT state explicit commercial terms, so confirm the per-version flag on Civitai before shipping. The SDXL-1.0 variant inherits Open RAIL++-M (commercial OK). Helper LoRAs may carry separate terms.
- **Fit:** rig 5/5 · studio 3/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| main turn LoRA weight | ~0.7 | ○ | author recommendation |
| secondary helper LoRA weight | ~0.15 | ○ | needed for face/clothing consistency |
| view consistency (LoRA-trained char) | 85-92% | ○ | third-party guide estimate, not measured here |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| face/clothing drift between views | single turn LoRA insufficient for identity lock | stack a second helper LoRA at low weight; add IP-Adapter FaceID |  |
| consistency collapses outside author's workflow | LoRA tuned to embedded ComfyUI graph | load the author's published image to import the exact workflow |  |

- **Verify:** Civitai page resolves; model exists (Chamber, Illustrious primary + SDXL experimental, ~80 3D-render training images, Helper-LoRA note all confirmed). Card states no explicit commercial flag, so 'conditional' (base-license inheritance) is accurate. Apatero secondary source resolves and contains the 85-92% vs 65-75% consistency figures as claimed. [Not a fabrication and NOT flag-unstated. Chamber's Charturn is real (Civitai 362559 IL/XL Merged; 694887 XL, pub 2024-08-28) and both return allowCommercialUse [Image, RentCivit, Rent, Sell] + allowDerivatives true + no credit — the most pe]
- **Sources:** [IL/XL Charturn Merged, Multi-View, Turnaround, Model Sheet, Character Design](https://civitai.com/models/362559/ilxl-charturn-merged-multi-view-turnaround-model-sheet-character-design) (Chamber (ChamberSu1996), 2024) — LoRA built from ~80 3D-model render images that generates multi-view turnarounds; author notes body/face turns still need a special Helper LoRA. ; [AI Character Turnaround Sheet Guide 2026](https://apatero.com/blog/ai-character-turnaround-sheet-generation-guide-2026) (Apatero Blog, 2026) — LoRA-trained characters achieve 85-92% view consistency vs 65-75% for pure prompting with reference images.

